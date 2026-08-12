# skills

**AI CLI 维护技能集合 / AI CLI Maintenance Skills Collection**

[中文](#中文) | [English](#english)

## 中文

本仓库用于存放与 AI CLI 长期工作记忆相关的维护技能。当前收录 `agents-updater`（最新版 v2.5，2026-08-12）。

### 这个 skill 是做什么的

`agents-updater/` 是一个通用的 AI CLI 维护技能，面向 Claude Code、Codex、Cursor、Windsurf、Augment、OpenCode 等主流 AI CLI，不绑定任一 CLI 的目录结构或命名。它维护 AI CLI 的长期工作记忆：

- 项目指令文件（`AGENTS.md` / `CLAUDE.md` / `.cursorrules` / `.windsurfrules` 等）
- skills（frontmatter、别名、渐进披露、按需 references）
- hooks、commands、tools 与 MCP 配置
- references 与 scripts

核心目标是：**可复用规则进全局，项目事实留在项目内，CLI 通用配置有清晰归属和审计路径**，减少以后因为缺索引、缺指导或缺脚本造成的上下文浪费。

### 何时触发

满足以下任一情况时使用本 skill：

- 用户要求更新、迁移、重命名、合并、删除或审计项目指令文件、skills、hooks、commands、tools、`references/`、`scripts/`。
- 用户说"更新 skill / 记到 skill / 同步 skill / 下次别踩坑 / 以后按这个来"。
- 用户说"加个 hook / 配置 hook / hook 不生效 / 迁移 hooks"。
- 用户说"加个 command / 斜杠命令 / 快捷指令 / 自定义命令"。
- 用户说"加个 tool / MCP tool / 工具配置 / 工具权限"。
- 用户要求扫描 CLI 历史记录、最近对话或重复需求来判断 Skill / Hook / Command / Tool / Prompt 候选。
- 任务结束前需要复盘本轮工作流并判断发现是否值得沉淀。
- 工作中反复读取同类文件、做大范围搜索、被旧路径误导、或因为缺少脚本重复写一次性工具。
- 跨 CLI 迁移或同步配置时。

### 三种维护模式（先选 profile）

开工前先为本轮选择一个 profile，避免把不同风险等级的规则混在一起：

| profile | 适用场景 | 关键要求 |
|---------|---------|---------|
| `strict-skill` | 新建或实质重写 skill | 遵循 `skill-creator`；清晰 frontmatter、渐进披露、最小正文、按需 references、可执行验证和必要的 forward-test |
| `compat-skillshare` | 维护 skillshare 已管理的已有技能 | 保留同步入口和本地兼容约定；只修复已确认的噪声、过期引用或行为缺口；不因追求统一格式而批量重写无关 skill |
| `agents-report` | 审计或治理 `AGENTS.md` | 先基于路径、消费者和冲突取证；用户已明确要求清理或改写时可据此直接实施，只有未决设计冲突会实质改变结果时才暂停询问 |

### 工作流程

1. 定义维护对象：项目指令文件、skill、hook、command、tool、reference、script，或**不沉淀**。
2. 判断全局/私有边界：跨项目、跨 CLI 不变才进全局；带项目业务、凭据、端口、地图、插件选择、路径默认值的留在项目。
3. 选择 `strict-skill`、`compat-skillshare` 或 `agents-report` profile，并读取对应参考文件。
4. 审 frontmatter 和正文噪声：`description` 只写触发入口，`aliases` 只留核心别名；同名全局/项目 skill 必查分层。
5. 查重与验真：搜索同义规则、旧路径、旧命令和消费者；确定唯一权威源后删除或替换旧索引，不保留新旧并列 fallback。
6. 写最小长期信息：只记录索引、约定、踩坑、脚本入口和判断规则，不记录一次性过程。
7. 判断 Prompt/Command 候选时只统计真实用户消息，排除子 Agent 任务单、工具调用、shell、系统上下文、浏览器上下文和 trace 重复；复盘执行效率时则检查本轮可见的搜索、读取、临时命令、改道和验证证据。
8. 任务结尾自动复盘：把证据分为过期或冲突信息、工作流低效、真实踩坑、一次性或证据不足；**优先删污染源或优化流程，最后才记录踩坑**。
9. 对工作流修复写出"原路径 → 根因 → 最小修复 → 下次理想路径"，并用可见轨迹验证；无法取证时不编造复盘结论。
10. 验证：运行可用的静态检查、脚本 `--help` 或轻量样例；对于 hooks/commands/tools，检查配置文件语法和 CLI 是否识别；至少 grep 旧名和新名确认引用收敛。

### 上下文污染控制

- `context-budget`：开工先压缩本轮目标、成功证据和最小必读范围；未进入范围的文件默认延后读取。
- 用**可观察信号**而非固定 token 或时间阈值判断污染：连续读取无关文件、重复搜索同一问题、发现多个权威源、计划反复改道，或读取很多规则却没有执行动作。
- 同时出现两个以上信号时触发 `pollution-breaker`：停止扩展搜索，收缩到直接相关来源并继续可安全完成的工作。
- 只有来源歧义或权威冲突**直接阻断安全完成**时才暂停，并提出一个能决定路线的具体问题；普通降噪不强制生成独立污染报告。
- 污染不阻塞当前目标时标记 `deferred-cleanup`，任务结尾必须重新处理：有直接证据且在授权范围内就实施最小流程修复，否则明确判为不沉淀或保留具名候选。

### AGENTS.md 证据式处理

- 默认先记录 `AGENTS.md` 的路径、行号、规则类别、证据来源、消费者、冲突和建议；用户明确要求审计、清理或改写时，这份取证直接服务于实施，不需要追加一次批准。
- 设计意图、兼容策略、权威源和敏感信息出现冲突时，列出候选及影响并等待用户取舍；仓库事实能证明过期的路径或命令才可直接替换。
- 用户明确要求保留的本地凭据可以保留在项目指令文件，但**不得复制进全局 skill**；报告和终端输出只显示存在性、路径和行号，不回显凭据。

### 版本控制边界

- 运行数据、插件目录或本地服务器工作区默认不执行 `git add`、提交、重置、清理或全库取消跟踪。
- 项目 `AGENTS.md` 明确禁止 Git 时，按项目规则执行；人工复制备份属于历史恢复副本，不自动扫描、合并、回迁或视为第二权威源。
- 只有项目规则允许且用户明确要求清理误跟踪文件时，才对指定索引项执行可逆的 `git rm --cached`，用精确 ignore 规则防止再次跟踪，保留磁盘文件并报告目标。

### 写入门槛

- 同时满足"未来会重复使用、关键配置会持续维护、缺少约定会明显降低效率"，才新建或保留 skill。
- 一次性改动、很小的单文件配置、首轮接入后基本冻结、临时迁移/活动/试验内容，不单独建 skill。
- `SKILL.md` 建议 150 行、硬上限 250 行；单个 `references/*.md` 建议 200 行、硬上限 350 行。
- 可复用脚本放对应 skill 的 `scripts/`；`SKILL.md` 只写何时执行、命令入口、输入输出和失败处理，不贴脚本代码。

### 任务结束前自检（要点）

1. 是否发现过期路径、命令、事实或旧项目残留？有就删改源头并清残留。
2. 是否新增长期字段、值域、插件入口或脚本入口？有且会复用才写。
3. 异常属于四类中的哪一类？根因明确且正确流程仍需规避时，才按"现象、根因、正确做法"三段式写踩坑。
4. 是否涉及 2 个以上插件或系统？有就核对项目 linkage 是否对齐。
5. 是否暴露项目指令文件缺少硬规则？有就写项目私有规则。
6. 结果正确但仍有重复搜索、无关阅读、临时命令或反复改道？先修工作流，不能把绕路沉淀下来。
7. 结论应全局复用、项目私有还是不沉淀？写入前再确认一次。
8. 是否暴露 frontmatter 噪声？有就同步审同名全局/项目 skill 的 desc 和 aliases。
9. 涉及 hook？确认归属、验证语法、确认不冲突。
10. 涉及 command？确认命名不冲突、作用域正确、参数清晰。
11. 涉及 tool？确认凭据不进入项目指令文件或全局 skill、描述足够让 CLI 正确调用。

### 目录结构

```
agents-updater/
├── SKILL.md                     # 核心：触发条件、三种维护模式、工作流程、污染控制、自检、源文件索引
├── CHANGELOG.md                 # 版本变更记录（v2.3 初始发布 → v2.5）
├── references/
│   ├── maintenance-matrix.md    # 全局/项目分流、hooks/commands/tools 判断、任务末工作流复盘、常见错误、文件职责速查
│   └── eval-cases.md            # 真实维护场景评估用例（Case 1–14），用于抽样验证维护行为
├── scripts/
│   └── audit_agent_skill.py     # 结构化静态审计脚本：frontmatter、引用、行数、项目事实污染、agents metadata
└── agents/
    └── openai.yaml              # OpenAI 兼容 CLI 的 agent 适配配置
```

### 版本历史

- **v2.5（2026-08-12）**
  - 任务末工作流复盘：证据分类（过期/冲突信息、工作流低效、真实踩坑、一次性或证据不足），优先删污染源或优化流程，最后才记录踩坑；写出"原路径 → 根因 → 最小修复 → 下次理想路径"并用可见轨迹验证。
  - `agents-report` 改为证据式处理：先取证，用户明确要求清理/改写时直接实施，只有未决设计冲突才暂停询问。
  - "上下文污染门禁/熔断"调整为"上下文污染控制"：偏离时收缩到直接相关来源继续，不再默认生成污染报告并中断。
  - `maintenance-matrix.md` 新增"任务末工作流复盘"章节；`eval-cases.md` 新增 Case 13/14；`openai.yaml` 更新 `default_prompt`。
- **v2.3（2026-08-06）**
  - 初始发布：AGENTS/skills/hooks/commands/tools/references/scripts 的维护与审计流程、维护 profile、上下文污染门禁、版本控制边界与写入门槛，附审计脚本、维护矩阵与评估用例。

### 使用方式

这个 skill 不绑定任何项目或 CLI，任何项目都可以接入使用。

1. **安装/接入**：把 `agents-updater/` 目录放进项目的 skill 目录，例如 `.skillshare/skills/agents-updater/`，或对应 CLI 的 skills 路径（Codex 用 `.codex/skills/`，Claude Code 用 `.claude/skills/`）；也可以全局安装，让所有项目共用。
2. **在 `AGENTS.md` 加规则**：和注册其它 skill 的方式一样，在 `AGENTS.md` 里按任务登记入口，例如：

```markdown
## 技能与工作流

- 需要新增、更新、迁移、重命名、合并、删除或审计 AGENTS.md、skills、hooks、commands、tools、references、scripts 时，使用 `agents-updater` skill（入口 `.skillshare/skills/agents-updater/SKILL.md`）。
```

3. **验证接入**：让 Agent 执行一次 skill 维护任务（例如"更新 skill / 记到 skill / 审计 AGENTS"），确认它会按本 skill 的流程走；也可以用下面的审计脚本体检 skill 本身。
4. **升级**：用新版本替换 `agents-updater/` 目录内容，并按 `CHANGELOG.md` 对照升级说明。

### 审计验证

```bash
PYTHONUTF8=1 python agents-updater/scripts/audit_agent_skill.py agents-updater
```

### 赞助支持

本项目由个人维护。如果对你有帮助，可以通过以下方式支持：

- 中转站（赞助）：<https://claudenb.com>
- 推荐注册：<https://claudenb.com/register?aff=EGVS96QN3PEY>
- QQ 群：`314854554`

## English

This repository hosts maintenance skills for AI CLI long-term working memory. It currently ships `agents-updater` (latest v2.5, 2026-08-12).

### What this skill does

`agents-updater/` is a general-purpose AI CLI maintenance skill for mainstream AI CLIs such as Claude Code, Codex, Cursor, Windsurf, Augment, and OpenCode. It is not tied to any specific CLI directory layout or naming convention. It maintains the long-term working memory of an AI CLI:

- Project instruction files (`AGENTS.md` / `CLAUDE.md` / `.cursorrules` / `.windsurfrules`, etc.)
- Skills (frontmatter, aliases, progressive disclosure, on-demand references)
- Hooks, commands, tools, and MCP configuration
- References and scripts

The core goal: **reusable rules go global, project facts stay in the project, and CLI-wide configuration gets a clear home and audit trail**, reducing context waste caused by missing indexes, guidance, or scripts.

### When to trigger

Use this skill when any of the following happens:

- The user asks to add, update, migrate, rename, merge, delete, or audit project instruction files, skills, hooks, commands, tools, `references/`, or `scripts/`.
- The user says "update skill", "remember this in a skill", "sync skill", "don't step on this again", or "follow this from now on".
- The user asks to add, configure, fix, or migrate a hook, a command (slash command / shortcut), or a tool (MCP).
- The user asks to scan CLI history, recent conversations, or repeated needs to decide Skill / Hook / Command / Tool / Prompt candidates.
- A retrospective review of the current round's workflow is needed before the task ends.
- Work repeatedly reads the same kind of files, does broad searches, is misled by old paths, or re-writes one-off tools because a script is missing.
- Migrating or syncing configuration across CLIs.

### Maintenance profiles (pick one first)

Pick a profile before starting so rules with different risk levels are not mixed:

| profile | Use for | Key requirements |
|---------|---------|------------------|
| `strict-skill` | Creating or substantially rewriting a skill | Follow `skill-creator`; clean frontmatter, progressive disclosure, minimal body, on-demand references, executable verification, and forward-test when needed |
| `compat-skillshare` | Maintaining an existing skill already managed by skillshare | Keep sync entry points and local compatibility conventions; only fix confirmed noise, stale references, or behavior gaps; do not mass-rewrite unrelated skills |
| `agents-report` | Auditing or governing `AGENTS.md` | Gather evidence by path, consumers, and conflicts first; implement directly when the user explicitly asked to clean or rewrite; only pause to ask when an unresolved design conflict materially changes the outcome |

### Workflow

1. Define the maintenance target: project instruction file, skill, hook, command, tool, reference, script, or **do not persist**.
2. Decide the global/private boundary: only go global if unchanged across projects and CLIs; keep project business, credentials, ports, maps, plugin choices, and default paths in the project.
3. Select the profile (`strict-skill` / `compat-skillshare` / `agents-report`) and read the relevant references.
4. Review frontmatter and body noise: `description` only states the trigger entry, `aliases` keeps only core aliases; always check layering of same-name global/project skills.
5. Deduplicate and verify: search for synonymous rules, old paths, old commands, and consumers; once a unique source of truth is determined, delete or replace old indexes; never keep old/new parallel fallbacks.
6. Write minimal long-term information: only indexes, conventions, pitfalls, script entry points, and decision rules — never one-off process detail.
7. Count only real user messages when deciding Prompt/Command candidates (exclude sub-agent task sheets, tool calls, shell, system/developer/environment context, browser context, and trace repeats). When reviewing execution efficiency, use visible evidence: searches, reads, one-off commands, detours, and verification output.
8. At task end, automatically classify evidence into: stale/conflicting info, inefficient workflow, real pitfall, one-off/insufficient evidence. **Delete pollution sources or optimize the workflow first; record pitfalls last.**
9. Write workflow fixes as "original path → root cause → minimal fix → ideal next path", verified with visible traces; never fabricate retrospective conclusions.
10. Verify: run available static checks, script `--help`, or lightweight samples; for hooks/commands/tools check config syntax and CLI recognition; grep old and new names to confirm references converged.

### Context pollution control

- `context-budget`: compress the round's goal, success evidence, and minimal required reading at the start; defer files outside scope.
- Use **observable signals** instead of fixed token/time thresholds: reading unrelated files repeatedly, re-searching the same question, discovering multiple sources of truth, planning repeated detours, or reading many rules without taking action.
- When two or more signals appear at once, trigger `pollution-breaker`: stop expanding the search, shrink to directly relevant sources, and continue safely completable work.
- Pause only when source ambiguity or authority conflicts directly block safe completion, and ask one concrete question that decides the route; normal cleanup does not require a separate pollution report.
- When pollution does not block the goal, mark `deferred-cleanup` and re-handle it at task end: implement the minimal workflow fix when evidence exists and it is in scope, otherwise explicitly mark as "do not persist" or keep a named candidate.

### Evidence-based `AGENTS.md` handling

- By default record the path, line numbers, rule category, evidence source, consumers, conflicts, and suggestions for `AGENTS.md`; when the user explicitly asks for an audit, cleanup, or rewrite, this evidence serves the implementation directly without an extra approval round.
- When design intent, compatibility strategy, source of truth, or sensitive information conflicts, list candidates and impact and wait for the user's decision; only replace paths or commands directly when repo facts prove them stale.
- Local credentials explicitly kept by the user may stay in the project instruction file but must **not** be copied into a global skill; reports and terminal output only show existence, path, and line numbers, never the credential value.

### Version-control boundaries

- Runtime data, plugin directories, and local server workspaces are not `git add`ed, committed, reset, cleaned, or untracked by default.
- Follow project rules when the project `AGENTS.md` explicitly forbids Git; manual copy backups are historical recovery copies, not to be auto-scanned, merged, migrated, or treated as a second source of truth.
- Only when project rules allow and the user explicitly asks to clean wrongly tracked files, run a reversible `git rm --cached` on the named index entries with precise ignore rules, keep files on disk, and report the targets.

### Writing threshold

- Create or keep a skill only when it will be reused, its key config keeps being maintained, and missing conventions would clearly lower efficiency.
- Do not create a skill for one-off changes, tiny single-file configs, frozen setups, or temporary migrations/activities/experiments.
- `SKILL.md`: ~150 lines recommended, 250 hard limit; a single `references/*.md`: ~200 lines recommended, 350 hard limit.
- Reusable checks go into the skill's `scripts/`; `SKILL.md` only states when to run, the command entry, inputs/outputs, and failure handling — no script code.

### End-of-task self-check (highlights)

1. Found stale paths, commands, facts, or old project remnants? Fix the source and clean remnants.
2. Added long-term fields, value domains, plugin entries, or script entries? Write only if reused.
3. Which category does the anomaly belong to? Write a pitfall in "symptom, root cause, correct practice" only when the root cause is clear and the correct flow still needs guarding.
4. Involved 2+ plugins or systems? Check project linkage alignment.
5. Found missing hard rules in the project instruction file? Write project-private rules.
6. Correct result but repeated searches, unrelated reads, one-off commands, or detours remain? Fix the workflow first; never persist the detour itself.
7. Global, project-private, or not persisted? Confirm before writing.
8. Frontmatter noise exposed? Audit same-name global/project skill desc and aliases.
9. Hook added or changed? Confirm ownership, validate syntax, ensure no conflicts.
10. Command added or changed? Confirm unique naming, correct scope, clear arguments.
11. Tool added or changed? Confirm credentials never appear in project instruction files or global skills, and the description is sufficient for the CLI to call it.

### Directory layout

```
agents-updater/
├── SKILL.md                     # Core: triggers, three profiles, workflow, pollution control, self-check, source index
├── CHANGELOG.md                 # Version history (v2.3 initial release → v2.5)
├── references/
│   ├── maintenance-matrix.md    # Global/private split, hooks/commands/tools decisions, end-of-task review, common errors, file responsibilities
│   └── eval-cases.md            # Real maintenance scenarios (Case 1–14) for sampling maintenance behavior
├── scripts/
│   └── audit_agent_skill.py     # Structured static audit: frontmatter, references, line limits, project-fact pollution, agents metadata
└── agents/
    └── openai.yaml              # Agent adaptation config for OpenAI-compatible CLIs
```

### Version history

- **v2.5 (2026-08-12)**
  - End-of-task workflow review: classify evidence (stale/conflicting info, inefficient workflow, real pitfall, one-off/insufficient evidence); delete pollution sources or optimize the workflow first, record pitfalls last; write "original path → root cause → minimal fix → ideal next path" and verify with visible traces.
  - `agents-report` is now evidence-based: gather evidence first, implement directly when explicitly requested, and only pause to ask on unresolved design conflicts.
  - "Context-pollution gate/circuit-breaker" became "context pollution control": on deviation, shrink to directly relevant sources and continue; no longer emits a pollution report and interrupts by default.
  - `maintenance-matrix.md` gained the "end-of-task workflow review" section; `eval-cases.md` gained Case 13/14; `openai.yaml` updated its `default_prompt`.
- **v2.3 (2026-08-06)**
  - Initial release: maintenance/audit workflow for AGENTS/skills/hooks/commands/tools/references/scripts; maintenance profiles; context-pollution gate; version-control boundaries and writing thresholds; ships the audit script, maintenance matrix, and eval cases.

### How to use

This skill is not tied to any project or CLI; any project can adopt it.

1. **Install**: put the `agents-updater/` directory into your project's skill directory, e.g. `.skillshare/skills/agents-updater/`, or a CLI-specific path (`.codex/skills/` for Codex, `.claude/skills/` for Claude Code). You can also install it globally so all projects share it.
2. **Add a rule to `AGENTS.md`**: just like how other skills are registered, add a task entry, e.g.:

```markdown
## Skills & Workflow

- Use the `agents-updater` skill (entry: `.skillshare/skills/agents-updater/SKILL.md`) when adding, updating, migrating, renaming, merging, deleting, or auditing AGENTS.md, skills, hooks, commands, tools, references, or scripts.
```

3. **Verify**: ask the agent to run a maintenance task (for example "update this skill", "remember this into a skill", or "audit AGENTS"), or audit the skill itself with the script below.
4. **Upgrade**: replace the `agents-updater/` directory with the new version and follow `CHANGELOG.md`.

### Audit verification

```bash
PYTHONUTF8=1 python agents-updater/scripts/audit_agent_skill.py agents-updater
```

### Sponsorship

This project is maintained by an individual. If it helps you, you can show support in the following ways:

- Relay station (sponsor): <https://claudenb.com>
- Referral signup: <https://claudenb.com/register?aff=EGVS96QN3PEY>
- QQ Group: `314854554`
