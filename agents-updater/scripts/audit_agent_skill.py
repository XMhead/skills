#!/usr/bin/env python3
"""Audit an agent maintenance skill folder.

The script intentionally avoids project-specific defaults. Pass the skill
directory explicitly or run it from inside the skill directory.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SKILL_LINE_LIMIT = 250
SKILL_RECOMMENDED_LINES = 150
REFERENCE_LINE_LIMIT = 350
REFERENCE_RECOMMENDED_LINES = 200
DESCRIPTION_WARN_CHARS = 90
ALIASES_MAX = 8

REQUIRED_FOR_AGENTS_UPDATER = (
    "references/maintenance-matrix.md",
    "references/eval-cases.md",
    "scripts/audit_agent_skill.py",
    "agents/openai.yaml",
)

PROJECT_PRIVATE_PATTERNS = (
    r"\b127\.0\.0\.1:\d+",
    r"\b\d{2,5}/\d{2,5}\b",
    r"[A-Za-z]:\\",
    r"RCON\s*密码\s*[:：]",
    r"webhook\s*[:=]\s*https?://",
    r"token\s*[:=]\s*[A-Za-z0-9_\-]{16,}",
    r"password\s*[:=]\s*[^,\s]+",
)


@dataclass
class Finding:
    level: str
    message: str


class Audit:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def fail(self, message: str) -> None:
        self.findings.append(Finding("FAIL", message))

    def warn(self, message: str) -> None:
        self.findings.append(Finding("WARN", message))

    def ok(self, message: str) -> None:
        self.findings.append(Finding("OK", message))

    @property
    def has_failures(self) -> bool:
        return any(f.level == "FAIL" for f in self.findings)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str, audit: Audit) -> tuple[dict[str, str], list[str]]:
    if not text.startswith("---\n"):
        audit.fail("SKILL.md missing YAML frontmatter")
        return {}, []
    end = text.find("\n---\n", 4)
    if end == -1:
        audit.fail("SKILL.md frontmatter is not closed")
        return {}, []

    raw_lines = text[4:end].splitlines()
    data: dict[str, str] = {}
    aliases: list[str] = []
    in_aliases = False

    for line in raw_lines:
        if re.match(r"^[A-Za-z0-9_-]+:", line):
            in_aliases = False
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
            if key.strip() == "aliases":
                aliases.extend(extract_aliases(value))
        elif re.match(r"^\s+aliases:", line):
            in_aliases = True
            _, value = line.split(":", 1)
            aliases.extend(extract_aliases(value))
        elif line.strip().startswith("aliases:"):
            in_aliases = True
            _, value = line.split(":", 1)
            aliases.extend(extract_aliases(value))
        elif in_aliases and line.strip().startswith("-"):
            aliases.extend(re.findall(r"-\s*['\"]?([^'\"]+)['\"]?", line.strip()))

    if "aliases" in data and not aliases:
        aliases.extend(extract_aliases(data["aliases"]))
    return data, aliases


def extract_aliases(value: str) -> list[str]:
    matches = re.findall(r'"([^"]+)"|\'([^\']+)\'|([^,\[\]\s]+)', value)
    return [next(part for part in match if part) for match in matches]


def audit_frontmatter(skill_md: Path, text: str, audit: Audit) -> str | None:
    data, aliases = parse_frontmatter(text, audit)
    name = data.get("name")
    description = data.get("description")

    if not name:
        audit.fail("frontmatter missing required name")
    elif not re.fullmatch(r"[a-z0-9-]+", name):
        audit.fail(f"frontmatter name should use lowercase letters, digits, and hyphens: {name}")
    else:
        audit.ok(f"frontmatter name: {name}")

    if not description:
        audit.fail("frontmatter missing required description")
    elif "\n" in description:
        audit.fail("description must be a single line")
    elif len(description) > DESCRIPTION_WARN_CHARS:
        audit.warn(f"description is {len(description)} chars; prefer <= {DESCRIPTION_WARN_CHARS}")
    else:
        audit.ok(f"description length: {len(description)} chars")

    if aliases:
        if len(aliases) > ALIASES_MAX:
            audit.fail(f"aliases count is {len(aliases)}; max {ALIASES_MAX}")
        else:
            audit.ok(f"aliases count: {len(aliases)}")

    frontmatter_body = text.split("\n---\n", 1)[0]
    if "description: |" in frontmatter_body or "description: >" in frontmatter_body:
        audit.fail("description uses block style; keep it one-line")

    return name


def line_count(text: str) -> int:
    return len(text.splitlines())


def audit_line_counts(root: Path, skill_text: str, audit: Audit) -> None:
    skill_lines = line_count(skill_text)
    if skill_lines > SKILL_LINE_LIMIT:
        audit.fail(f"SKILL.md has {skill_lines} lines; hard limit {SKILL_LINE_LIMIT}")
    elif skill_lines > SKILL_RECOMMENDED_LINES:
        audit.warn(f"SKILL.md has {skill_lines} lines; recommended <= {SKILL_RECOMMENDED_LINES}")
    else:
        audit.ok(f"SKILL.md line count: {skill_lines}")

    references = sorted((root / "references").glob("*.md")) if (root / "references").exists() else []
    for ref in references:
        lines = line_count(read_text(ref))
        rel = ref.relative_to(root).as_posix()
        if lines > REFERENCE_LINE_LIMIT:
            audit.fail(f"{rel} has {lines} lines; hard limit {REFERENCE_LINE_LIMIT}")
        elif lines > REFERENCE_RECOMMENDED_LINES:
            audit.warn(f"{rel} has {lines} lines; recommended <= {REFERENCE_RECOMMENDED_LINES}")
        else:
            audit.ok(f"{rel} line count: {lines}")


def audit_required_files(root: Path, skill_text: str, skill_name: str | None, audit: Audit) -> None:
    if skill_name != "agents-updater":
        return
    for rel in REQUIRED_FOR_AGENTS_UPDATER:
        path = root / rel
        if not path.exists():
            audit.fail(f"missing required resource: {rel}")
        else:
            audit.ok(f"resource exists: {rel}")
        if rel != "agents/openai.yaml" and rel not in skill_text:
            audit.fail(f"SKILL.md does not index {rel}")


def audit_openai_yaml(root: Path, audit: Audit) -> None:
    path = root / "agents" / "openai.yaml"
    if not path.exists():
        audit.warn("agents/openai.yaml not found")
        return
    text = read_text(path)
    for key in ("display_name:", "short_description:", "default_prompt:"):
        if key not in text:
            audit.fail(f"agents/openai.yaml missing {key}")
    if all(key in text for key in ("display_name:", "short_description:", "default_prompt:")):
        audit.ok("agents/openai.yaml has required UI metadata")


def audit_project_private_leaks(root: Path, audit: Audit) -> None:
    checked_files = [root / "SKILL.md"]
    if (root / "references").exists():
        checked_files.extend(sorted((root / "references").glob("*.md")))

    for path in checked_files:
        if not path.exists():
            continue
        text = read_text(path)
        for pattern in PROJECT_PRIVATE_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                rel = path.relative_to(root).as_posix()
                audit.warn(f"{rel} matches possible project-private pattern: {pattern}")


def audit_script_help(root: Path, audit: Audit) -> None:
    script = root / "scripts" / "audit_agent_skill.py"
    if not script.exists():
        return
    text = read_text(script)
    hardcoded_path = re.search(r"(?i)\b[A-Z]:\\[^\"'\s]+", text)
    if hardcoded_path:
        audit.fail(f"audit script contains a hardcoded Windows path: {hardcoded_path.group(0)}")
    else:
        audit.ok("audit script has no hardcoded Windows path literals")
    if "argparse" in text and "--strict" in text:
        audit.ok("audit script exposes argparse CLI and --strict")
    else:
        audit.warn("audit script should expose argparse CLI and --strict")


def run(root: Path, strict: bool) -> int:
    audit = Audit()
    root = root.resolve()
    skill_md = root / "SKILL.md"

    if not skill_md.exists():
        audit.fail(f"missing SKILL.md in {root}")
    else:
        skill_text = read_text(skill_md)
        skill_name = audit_frontmatter(skill_md, skill_text, audit)
        audit_line_counts(root, skill_text, audit)
        audit_required_files(root, skill_text, skill_name, audit)
        audit_openai_yaml(root, audit)
        audit_project_private_leaks(root, audit)
        audit_script_help(root, audit)

    for finding in audit.findings:
        print(f"{finding.level}: {finding.message}")

    if audit.has_failures:
        return 1
    if strict and any(f.level == "WARN" for f in audit.findings):
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit an AI agent skill folder.")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Skill directory to audit; defaults to current directory.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as exit code 2.")
    args = parser.parse_args(argv)
    return run(Path(args.skill_dir), args.strict)


if __name__ == "__main__":
    sys.exit(main())
