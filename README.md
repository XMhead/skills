# skills

**AI CLI 维护技能集合 / AI CLI Maintenance Skills Collection**

[中文](#中文) | [English](#english)

## 中文

本仓库用于存放与 AI CLI 长期工作记忆相关的维护技能。

### 这个 skill 是做什么的

`agents-updater/` 是一个通用的 AI CLI 维护技能，面向 Claude Code、Codex、Cursor、Windsurf、Augment、OpenCode 等主流 AI CLI，不绑定特定 CLI 的目录结构或命名。它负责维护或审计：

- 项目指令文件（`AGENTS.md` / `CLAUDE.md` 等）
- skills（frontmatter、别名、渐进披露与按需 references）
- hooks、commands、tools 与 MCP 配置
- references 与 scripts

目标是让可复用规则进入全局，让项目事实留在项目内，让 CLI 通用配置有清晰归属和审计路径，减少因缺索引、缺指导或缺脚本造成的上下文浪费。技能自带：

- `scripts/audit_agent_skill.py`：审计脚本，检查 frontmatter、资源引用、敏感模式与脚本规范。
- `references/eval-cases.md`：评估用例，用于验证维护行为。
- `references/maintenance-matrix.md`：维护矩阵，记录常见维护任务的归属与取舍。
- `agents/openai.yaml`：OpenAI Agent 元数据示例。

### 使用方式

这个 skill 不绑定任何项目或 CLI，任何项目都可以接入使用。

1. 安装/接入：把 `agents-updater/` 目录放进项目的 skill 目录，例如 `.skillshare/skills/agents-updater/`，或对应 CLI 的 skills 路径（Codex 用 `.codex/skills/`，Claude Code 用 `.claude/skills/`）；也可以全局安装，让所有项目共用。
2. 在 `AGENTS.md` 加规则：和注册其它 skill 的方式一样，在 `AGENTS.md` 里按任务登记入口，例如：

```markdown
## 技能与工作流

- 需要新增、更新、迁移、重命名、合并、删除或审计 AGENTS.md、skills、hooks、commands、tools、references、scripts 时，使用 `agents-updater` skill（入口 `.skillshare/skills/agents-updater/SKILL.md`）。
```

3. 验证接入：让 Agent 执行一次 skill 维护任务（例如“更新 skill / 记到 skill / 审计 AGENTS”），确认它会按本 skill 的流程走；也可以用下面的审计脚本体检 skill 本身。

### 审计验证

```bash
PYTHONUTF8=1 python agents-updater/scripts/audit_agent_skill.py agents-updater
```

### 赞助支持

本项目由个人维护。如果对你有帮助，可以通过以下方式支持：

- 中转站（赞助）：<https://www.findcg.com>
- 推荐注册：<https://www.findcg.com/register?aff=HRTH3YQDCCAY>
- QQ 群：`314854554`

## English

This repository hosts maintenance skills for AI CLI long-term working memory.

### What this skill does

`agents-updater/` is a general-purpose AI CLI maintenance skill for mainstream AI CLIs such as Claude Code, Codex, Cursor, Windsurf, Augment, and OpenCode. It is not tied to any specific CLI directory layout or naming convention. It maintains or audits:

- Project instruction files (`AGENTS.md` / `CLAUDE.md`, etc.)
- Skills (frontmatter, aliases, progressive disclosure, on-demand references)
- Hooks, commands, tools, and MCP configuration
- References and scripts

The goal is to keep reusable rules global, keep project facts in the project, and give CLI-wide configuration a clear home and audit trail, reducing context waste caused by missing indexes, guidance, or scripts. The skill ships with:

- `scripts/audit_agent_skill.py`: audit script that checks frontmatter, resource references, sensitive patterns, and script conventions.
- `references/eval-cases.md`: evaluation cases for validating maintenance behavior.
- `references/maintenance-matrix.md`: a maintenance matrix recording where common maintenance tasks belong and their trade-offs.
- `agents/openai.yaml`: an OpenAI Agent metadata example.

### How to use

This skill is not tied to any project or CLI; any project can adopt it.

1. Install: put the `agents-updater/` directory into your project's skill directory, e.g. `.skillshare/skills/agents-updater/`, or a CLI-specific path (`.codex/skills/` for Codex, `.claude/skills/` for Claude Code). You can also install it globally so all projects share it.
2. Add a rule to `AGENTS.md`: just like how other skills are registered, add a task entry, e.g.:

```markdown
## Skills & Workflow

- Use the `agents-updater` skill (entry: `.skillshare/skills/agents-updater/SKILL.md`) when adding, updating, migrating, renaming, merging, deleting, or auditing AGENTS.md, skills, hooks, commands, tools, references, or scripts.
```

3. Verify: ask the agent to run a maintenance task (for example "update this skill", "remember this into a skill", or "audit AGENTS"), or audit the skill itself with the script below.

### Audit verification

```bash
PYTHONUTF8=1 python agents-updater/scripts/audit_agent_skill.py agents-updater
```

### Sponsorship

This project is maintained by an individual. If it helps you, you can show support in the following ways:

- Relay station (sponsor): <https://www.findcg.com>
- Referral signup: <https://www.findcg.com/register?aff=HRTH3YQDCCAY>
- QQ Group: `314854554`
