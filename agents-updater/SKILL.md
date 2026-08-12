---
name: agents-updater
description: 维护或审计 AGENTS、skills、hooks、commands、tools、references、scripts；用于 skill 编写、上下文降噪、项目治理和权威源收敛。
metadata:
  aliases: ["agents-updater", "skill-updater", "更新skill", "更新AGENTS", "降噪", "补踩坑", "维护hooks", "维护commands"]
  version: 2.5
---

# Agents Updater（CLI 通用）

维护 AI CLI 的长期工作记忆：项目指令文件（`AGENTS.md` / `CLAUDE.md`）、skills、hooks、commands、tools、references 和 scripts。目标是让可复用规则进入全局，让项目事实留在项目内，让 CLI 通用配置有清晰归属和审计路径，减少以后因为缺索引、缺指导或缺脚本造成的上下文浪费。

本 skill 面向 Claude Code、Codex、Cursor、Windsurf、Augment、OpenCode 等主流 AI CLI，不绑定任一 CLI 的特定目录结构或命名。

## 触发条件

- 用户要求更新、迁移、重命名、合并、删除或审计项目指令文件、skills、hooks、commands、tools、`references/`、`scripts/`。
- 用户说"更新 skill / 记到 skill / 同步 skill / 下次别踩坑 / 以后按这个来"。
- 用户说"加个 hook / 配置 hook / hook 不生效 / 迁移 hooks"。
- 用户说"加个 command / 斜杠命令 / 快捷指令 / 自定义命令"。
- 用户说"加个 tool / MCP tool / 工具配置 / 工具权限"。
- 用户要求扫描 CLI 历史记录、最近对话或重复需求来判断 Skill / Hook / Command / Tool / Prompt 候选。
- 任务结束前需要复盘本轮工作流并判断发现是否值得沉淀。
- 工作中反复读取同类文件、做大范围搜索、被旧路径误导、或因为缺少脚本重复写一次性工具。
- 跨 CLI 迁移或同步配置时。

## 维护模式

先为本轮选择一个 profile，避免把不同风险等级的规则混在一起：

- **strict-skill**：新建或实质重写 skill 时使用。遵循 `skill-creator`，要求清晰 frontmatter、渐进披露、最小正文、按需 references、可执行验证和必要的 forward-test。
- **compat-skillshare**：维护已有 skillshare 技能时使用。保留其同步入口和本地兼容约定，只修复已确认的噪声、过期引用或行为缺口；不因追求统一格式而批量重写无关 skill。
- **agents-report**：审计或治理 `AGENTS.md` 时使用。先基于路径、消费者和冲突取证；用户已明确要求清理或改写时可据此直接实施，只有未决设计冲突会实质改变结果时才暂停询问。

## 必读顺序

1. 本文件。
2. 当前项目的项目指令文件：Codex 优先 `AGENTS.md`，Claude Code 优先 `CLAUDE.md`，Cursor 优先 `.cursorrules`，Windsurf 优先 `.windsurfrules`。
3. 目标 skill 的 `SKILL.md`；只在需要时读取相关 `references/*.md` 或 `scripts/`。
4. 涉及 hooks/commands/tools 时，读取当前 CLI 的对应配置文件或目录，例如 `.claude/settings.json`、`.codex/settings.json`、MCP 配置。
5. 创建或大改 skill 时，读取当前 CLI 官方/系统的 skill 创建指南。

## 工作流程

1. 定义维护对象：项目指令文件、skill、hook、command、tool、reference、script，或不沉淀。
2. 判断全局/私有边界：跨项目、跨 CLI 不变才进全局；带项目业务、凭据、端口、地图、插件选择、路径默认值的留在项目。
3. 选择 `strict-skill`、`compat-skillshare` 或 `agents-report` profile，并读取对应参考文件。
4. 审 frontmatter 和正文噪声：`description` 只写触发入口，`aliases` 只留核心别名；同名全局/项目 skill 必查分层。
5. 查重与验真：搜索同义规则、旧路径、旧命令和消费者；确定唯一权威源后删除或替换旧索引，不保留新旧并列 fallback。
6. 写最小长期信息：只记录索引、约定、踩坑、脚本入口和判断规则，不记录一次性过程。
7. 扫描重复需求以判断 Prompt/Command 候选时，只统计真实用户消息；排除子 Agent 任务单、工具调用、shell、系统/开发者/环境上下文、浏览器上下文和 trace 重复。复盘执行效率时则检查本轮可见的搜索、读取、临时命令、改道和验证证据。
8. 任务结尾调用本 skill 时，自动按维护矩阵把证据分为过期或冲突信息、工作流低效、真实踩坑、一次性或证据不足；优先删污染源或优化流程，最后才记录踩坑。
9. 对工作流修复写出“原路径 → 根因 → 最小修复 → 下次理想路径”，并验证直接来源、重复搜索、临时命令或无效改道确实减少；无法取证时不编造复盘结论。
10. 验证：运行可用的静态检查、脚本 `--help` 或轻量样例；对于 hooks/commands/tools，检查配置文件语法和 CLI 是否识别；至少 grep 旧名和新名确认引用收敛。

## 上下文污染控制

- `context-budget`：开工先压缩本轮目标、成功证据和最小必读范围；未进入范围的文件默认延后读取。
- 使用可观察信号而不是固定 token 或时间阈值：连续读取无关文件、重复搜索同一问题、发现多个权威源、计划反复改道，或读取很多规则却没有执行动作。
- 同时出现两个以上信号时触发 `pollution-breaker`：停止扩展搜索，收缩到直接相关来源并继续可安全完成的工作。
- 上下文偏离会影响用户判断时，简要报告原任务、直接相关来源、疑似重复或冲突、影响和当前收缩动作；不要求为普通降噪固定生成独立报告。
- 只有来源歧义或权威冲突直接阻断安全完成时才暂停，并提出一个能决定路线的具体问题。
- 污染不阻塞当前目标时标记 `deferred-cleanup`，完成最小交付后再记录治理候选；不得把治理任务混入当前执行流。
- 任务结尾调用本 skill 后必须重新处理 `deferred-cleanup`：有直接证据且在授权范围内就实施最小流程修复，否则明确判为不沉淀或保留具名候选，不让临时标签代替复盘。
- 用户已明确要求治理时，可在取证后直接清理；未授权的相邻治理仍留作候选，不扩大当前范围。

## References

- 需要判断全局/项目/不沉淀落点，或维护 hooks、commands、tools、短指令、常见错误、文件职责时，读 `references/maintenance-matrix.md`。
- 需要评测 skill 是否真的让 Agent 做出正确维护决策时，读 `references/eval-cases.md`，按其中场景执行或抽样 forward-test。
- 需要静态审计 skill 结构、frontmatter、引用、行数、项目事实污染和 agents metadata 时，运行 `scripts/audit_agent_skill.py <skill-dir>`；默认审计当前目录。

## 核心规则

- Skill 是长期索引和工作记忆，不是字段手册、官方文档镜像或一次性记录。
- 同一事实只保留一个权威位置；约定变更必须同时删除旧约定。
- 可由仓库事实证实过期的信息可直接删除或替换；涉及设计意图、兼容策略、业务取舍且证据不足的冲突，禁止自行保留、删除或合并，必须向用户列出冲突项与影响并等待决定。
- 根因未查清的失败不写成踩坑；可通过删旧信息避免的问题也不写成踩坑。
- 正确结果前的绕路、重复搜索和无关读取属于工作流低效，不得包装成领域踩坑或下一轮必做流程；先修路由、索引、reference、脚本或权威源。
- 不在全局 skill 写项目名、地图、RCON、端口、物品库选择、具体玩法经济或只对一个项目成立的默认路径。
- 全局 script 必须显式接收项目根目录或使用 CWD；不得内置项目路径，也不得从全局 skill 路径反推项目根。
- 多份配置并存时，明确一个 canonical source；其它文件只能标记为生成副本或显式测试覆盖，消费者不得隐式 fallback 到旧路径。
- Hook 只写"触发时机 / 做什么 / 不做什么"；复杂 hook 拆到 `scripts/`。
- Command 只写"命令名 / 参数 / 行为描述"；实现走 CLI 原生机制，不另建中间层。
- Tool 只写"工具名 / 用途 / 全局还是项目 / 凭据来源"；MCP tool 的 JSON schema 不贴进 skill。

## Skill 写作与降噪检查

- 新建或实质重写时，只保留 `name`、`description` 两个 frontmatter 字段；正文使用祈使句，先写核心流程，再按需链接一层 references。
- `compat-skillshare` 可以保留 skillshare 已约定的 `metadata`、`aliases` 等兼容字段，但不得把项目事实或功能清单塞进其中；改格式前先报告兼容影响。
- 把确定性、会重复执行的检查放进 `scripts/`；`SKILL.md` 只写触发条件、调用入口、输入输出和失败处理，不复制脚本正文或官方字段手册。
- 降噪已有 skill 时先区分行为规则、索引、示例和历史叙述；删除重复/过期内容，保留可验证的约束，不用整篇重写掩盖行为变化。
- 严格 profile 至少运行 frontmatter/结构校验和本地审计；复杂 skill 再抽样 forward-test。兼容 profile 至少运行该项目现有 skill doctor、脚本 `--help` 或等效轻量检查。

## AGENTS.md 证据式处理

- 默认先记录 `AGENTS.md` 的路径、行号、规则类别、证据来源、消费者、冲突和建议；用户明确要求审计、清理或改写时，这份取证直接服务于实施，不需要追加一次批准。
- 设计意图、兼容策略、权威源和敏感信息出现冲突时，列出候选及影响并等待用户取舍；仓库事实能证明过期的路径或命令才可直接替换。
- 用户明确要求保留的本地凭据可以保留在项目指令文件，但不得复制进全局 skill；报告和终端输出只显示存在性、路径和行号，不回显凭据。
- 用户当前请求已经明确授权修改时，做最小范围补丁，并复核无关工作区修改、规则行号和引用收敛。

## 版本控制边界

- 运行数据、插件目录或本地服务器工作区默认不执行 `git add`、提交、重置、清理或全库取消跟踪。
- 项目 `AGENTS.md` 明确禁止 Git 时，按项目规则执行；人工复制备份属于历史恢复副本，不自动扫描、合并、回迁或视为第二权威源。
- 只有项目规则允许且用户明确要求清理误跟踪文件时，才对指定索引项执行可逆的 `git rm --cached`，用精确 ignore 规则防止再次跟踪，保留磁盘文件并报告目标；这不等于把 Git 用作项目备份或开发流程。

## 写入门槛

- 同时满足未来会重复使用、关键配置会持续维护、缺少约定会明显降低效率，才新建或保留 skill。
- 一次性改动、很小的单文件配置、首轮接入后基本冻结、临时迁移/活动/试验内容，不单独建 skill。
- `SKILL.md` 建议 150 行、硬上限 250 行；单个 `references/*.md` 建议 200 行、硬上限 350 行。
- 可复用脚本放对应 skill 的 `scripts/`；`SKILL.md` 只写何时执行、命令入口、输入输出，不贴脚本代码。

## 任务结束前自检

1. 本轮是否发现过期路径、命令、事实或旧项目残留？有就删改源头并清残留。
2. 本轮是否新增长期字段、值域、插件入口或脚本入口？有且会复用才写。
3. 本轮异常属于过期或冲突信息、工作流低效、真实踩坑、一次性或证据不足中的哪一类？只有根因明确且优化后的正确流程仍需规避时，才按现象、根因、正确做法三段式写踩坑。
4. 本轮是否涉及 2 个以上插件或系统？有就核对项目 linkage 是否对齐。
5. 本轮是否暴露项目指令文件缺少硬规则？有就写项目私有规则。
6. 本轮即使成功，是否仍有重复搜索、无关阅读、临时命令或反复改道？有就先修工作流，写出下次理想路径并做与风险相称的验证，不能把绕路本身沉淀下来。
7. 本轮结论应全局复用、项目私有还是不沉淀？写入前再确认一次。
8. 本轮是否暴露 frontmatter 噪声？有就同步审同名全局/项目 skill 的 desc 和 aliases。
9. 本轮是否涉及新增/修改 hook？有就确认归属、验证语法、确认不会与已有 hook 冲突。
10. 本轮是否涉及新增/修改 command？有就确认命名不与已有 command 冲突、作用域正确、参数清晰。
11. 本轮是否涉及新增/修改 tool？有就确认凭据不出现在项目指令文件或全局 skill、工具描述足够让 CLI 正确调用。

## 验证命令

```bash
python scripts/audit_agent_skill.py .
```

在 Codex 环境中还要运行系统 skill 校验脚本；Windows 上如果遇到默认 GBK 读取 UTF-8 失败，先设置 `PYTHONUTF8=1` 再运行。

## 源文件索引

- `SKILL.md`：核心触发、流程、写入门槛、自检和资源入口。
- `references/maintenance-matrix.md`：全局/项目分流、hooks/commands/tools 判断、上下文浪费诊断、短指令落点、常见错误、文件职责速查。
- `references/eval-cases.md`：真实维护场景、期望决策、失败信号和抽样评测口径。
- `scripts/audit_agent_skill.py`：结构化静态审计脚本。
- `agents/openai.yaml`：OpenAI 兼容 CLI 的 agent 适配配置。
