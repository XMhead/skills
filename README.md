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

### Audit verification

```bash
PYTHONUTF8=1 python agents-updater/scripts/audit_agent_skill.py agents-updater
```

### Sponsorship

This project is maintained by an individual. If it helps you, you can show support in the following ways:

- Relay station (sponsor): <https://www.findcg.com>
- Referral signup: <https://www.findcg.com/register?aff=HRTH3YQDCCAY>
- QQ Group: `314854554`
