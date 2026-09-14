# `ai-rule-dispatcher` — 智能任务路由引擎

> **源文件**：skills/core/ai-rule-dispatcher/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-rule-dispatcher
description: "Route tasks to the correct methodology rules, skills, first checks, source documents, and safe execution order. Use at the start of each non-trivial task, especially when a request spans frontend, backend, data, deployment, governance, or documentation."
```

**中文描述**：把任务路由到正确的方法论规则、Skill、前置检查、源文档与安全执行顺序。在每个非平凡任务开始时使用，尤其当请求横跨前端、后端、数据、部署、治理或文档时。

---

## Purpose | 目的

在任何 AI 智能体执行任务之前，本 Skill 回答五个问题：

1. 这个任务属于哪条项目线？（mainline、governance、audit、research）
2. 必须先加载哪些规则与文档？
3. 应当由哪个 Skill 主导执行？
4. 在写任何代码之前，必须完成哪些事实检查（数据库、代码、运行时）？
5. 安全的执行顺序是什么？

本 Skill 用于**路由与首次进入判断（first-entry judgment）**，不做拆解，也不做实现。

## Rule | 规则

**当任务线（task line）、治理文档或主导 Skill 仍不清晰时，禁止把任务直接送去执行。**

先把任务路由到正确的上下文，再让其他 Skill 接管。

## When to Use | 触发条件

- 用户请求含糊，或横跨多个领域
- 任务同时涉及前端与后端
- 不确定该由哪个 Skill 处理该请求
- 新会话中的第一次交互
- 用户问“我该从哪里开始？”

## Standard Workflow | 标准工作流

### Step 1: Classify the Task Line | 判断任务线

判断任务属于哪条项目线：

| 项目线 | 说明 | 示例 |
|---|---|---|
| mainline | 活跃的开发工作 | 特性开发、缺陷修复、重构 |
| governance | 架构/质量治理 | 跨领域决策、边界映射 |
| audit | 质量检查 | 代码评审、流程收口审计、前端审计 |
| research | 调研与分析 | 竞品调研、技术评估 |
| release | 部署与发布 | CI/CD、部署脚本、发布说明 |

### Step 2: Classify the Task Type | 判断任务类型

| 类型 | 主导 Skill |
|---|---|
| 复杂/多模块 | ai-task-decomposer |
| 架构/设计 | ai-architect-governor |
| 项目规划 | ai-chief-planner |
| 命令执行 | ai-command-executor |
| 前端开发 | {stack}-frontend-dev（例如 vue） |
| 后端开发 | {stack}-backend-dev（例如 java-springboot） |
| 数据库变更 | mysql-best-practices（或等价 Skill） |
| 质量审计 | ai-flow-closure-audit 或 ai-frontend-audit |
| 调研 | ai-competitor-analyst 或 ai-market-researcher |
| Skill 改进 | ai-skill-evolver |

### Step 3: Select First Documents | 选择首要文档

执行之前，先确定权威文档：

1. rules/AGENTS.md —— 始终第一
2. rules/project_rules.md —— 项目专属规则（如存在）
3. 相关 Skill 的 SKILL.md
4. 相关 docs/ 分类文档

### Step 4: Define First Factual Checks | 定义前置事实检查

写任何代码之前，先核实：

| 检查类型 | 核实方式 |
|---|---|
| 数据库 | SHOW TABLES; DESCRIBE table; SELECT COUNT(*) |
| 代码是否存在 | 文件路径检查、按模式 grep |
| 运行时状态 | 端口检查、进程列表、健康端点 |
| 配置 | 读取配置文件、环境变量 |
| 文档 | 检查现有文档是否已覆盖本任务 |

### Step 5: Produce Routing Result | 输出路由结果

```markdown
## Task Routing Result

**Task Line**: [mainline / governance / audit / research / release]
**Lead Skill**: [skill-name]
**Support Skills**: [skill-names]

**First Documents to Read**:
1. [path/to/doc1]
2. [path/to/doc2]

**First Checks to Run**:
1. [check-1]
2. [check-2]

**Recommended Execution Order**:
1. [step-1]
2. [step-2]

**Boundary Warnings**:
- [warning-1]
```

**路由结果模板字段中文对照**（字段名保持英文，照抄上方模板即可套用）：

| 字段 | 中文含义 | 填写要求 |
|---|---|---|
| `Task Line` | 任务线 | 五选一：mainline / governance / audit / research / release |
| `Lead Skill` | 主导 Skill | **只能填一个**，用 `skills/SKILL_MANIFEST.json` 登记的正式名 |
| `Support Skills` | 支撑 Skill | 可多个；不得与主导 Skill 并列主导 |
| `First Documents to Read` | 首要阅读文档 | 从 rules/ 与相关 SKILL.md 起，按加载顺序编号 |
| `First Checks to Run` | 前置检查 | 每条必须是可执行、可读出结果的检查（SQL、grep、端口、健康端点） |
| `Recommended Execution Order` | 建议执行顺序 | 按依赖排序；未解除阻塞不得进入实现 |
| `Boundary Warnings` | 边界告警 | 写明不得触碰的文件、领域或真相源 |

## Mid-Task Re-Enforcement | 任务中强制重读

### Problem: Context Decay | 问题：上下文衰减

在长会话（>100 条消息）中，会话启动时加载的 Skill 可能已不在活跃上下文中。派发器（dispatcher）必须对抗这一衰减。

### Re-Enforcement Triggers | 强制重读触发点

在这些时点，派发器应当指示 AI 重读治理 Skill：

| 触发点 | 重读对象 |
|---|---|
| 从后端工作切换到前端工作 | ai-single-truth-enforcer、ai-library-first、ai-component-standardizer |
| 在同一领域累计 50+ 条消息后 | 该领域相关的治理 Skill |
| 向新文件写入代码之前 | 该领域的治理 Skill |
| 把任何任务标记为“complete”之前 | ai-runtime-verify、ai-single-truth-enforcer |
| 工具报错或出现意外结果之后 | ai-tool-bootstrapper、相关技术栈 Skill |

### Re-Enforcement Command | 强制重读指令

触发条件命中时，派发器输出：

```
⚠️ Context Decay Warning: >50 messages since last governance re-read.
Re-reading: ai-single-truth-enforcer, ai-library-first
```

---

## Guardrails | 防护规则

- 禁止跳过 check-before-execute（先检查后执行）
- 禁止推荐多个主导 Skill——只能选一个（ONE）
- 入口事实仍缺失时，禁止路由到实现
- 禁止把治理支撑线（governance support lines）当作当前主线（mainline）
- 若不确定，上报 `ai-chief-planner` 做排期决策

## Maturity | 成熟度

**Stage**：effective —— 在 GERP ERP 项目上经 2000+ 次任务派发实战检验。

## Evolution History | 进化记录

- v1.0.0：提炼自 gerp-rule-dispatcher，并通用化为普适用法
- 来源：GERP Enterprise ERP，3 个多月的每日派发实践

---

## 译注

1. **代码围栏缺陷（内容未改）**：源文件 `## Task Routing Result` 模板使用单个反引号作围栏（`` `markdown `` 开头、`` ` `` 结尾），而非三个反引号。按“路由结果模板必须保留可套用形态”的要求，中文版把围栏改为标准三反引号以便正常渲染，**块内字段与占位符一字未改**（`## Task Routing Result` 及其全部字段名保持英文原样）。`⚠️ Context Decay Warning` 代码块在源文件中已使用三反引号，原样保留未动。
2. **断链引用：`rules/project_rules.md` 不存在**。源文件 Step 3 要求读 `rules/project_rules.md`（项目专属规则，“如存在”）。仓库 `rules/` 目录下实际只有 `AGENTS.md`、`AGENTS.global.md`、`rules.json`，没有该文件；项目级规则目前落在 `AGENTS.md` 与 `rules/rules.json`。源文件自身已用 “if exists” 做了条件限定，因此不构成硬性断链，但实践者不应期待该文件存在。
3. **断链引用：`ai-market-researcher` 不存在**。源文件 Step 2 把“调研”路由到 `ai-competitor-analyst` 或 `ai-market-researcher`。仓库中不存在 `skills/governance/ai-market-researcher/`；`skills/SKILL_MANIFEST.json` 的 `rawOnlySkills` 里只有一个 `gerp-market-researcher`，属于“仅作原始证据保留、不计入正式发布”的条目。调研类任务当前可用的正式 Skill 是 `ai-competitor-analyst`。
4. **占位命名不是真实 Skill 名**：Step 2 中的 `{stack}-frontend-dev`、`{stack}-backend-dev` 是模板占位符，仓库中并不存在同名 Skill。实际存在的是 `skills/tech/vue`、`skills/tech/react-frontend` 与 `skills/tech/java-springboot`、`skills/tech/node-backend`、`skills/tech/python-fastapi` 等；调用时必须使用 `skills/SKILL_MANIFEST.json` 中登记的正式名，不得直接使用 `{stack}-frontend-dev` 这类占位串。
5. **源文件拼写错误**：`## Evolution History` 第二行源文为 “3+ months of daily dispatchesr”，末词 `dispatchesr` 是 `dispatches` 的拼写错误。中文版按语义译为“每日派发”，不复制拼写错误；此处记录原文形态以便对照。
6. **源版本**：源文件 frontmatter 只有 `name` 与 `description`，无版本号/日期标注，故记「未标注」。Step 1 表列了 5 条项目线（含 `release`），而 Purpose 第 1 问只列举 4 条（mainline、governance、audit、research），源文件两处不一致，中文版各自照实翻译、未做合并。
7. **门禁代号范围**：源文件未出现 `L0`–`L3`、`Q0`–`Q3`、`P0`–`P3` 代号（仅出现 Skill 名与技术栈名），故译文无对应代号保留项，未补写未出现的代号。
8. **存在未被引用的配套参考文件**：本 Skill 目录下有 `skills/core/ai-rule-dispatcher/references/routing-map.md`，但 SKILL.md 正文从未提到 `references`，读者从正文无法得知它存在。该参考文件实际承载了修正后的路由映射，与本正文的路由表存在差异，建议英文源在后续版本中补一条指向关系：
   - 第 4 节「Lead-skill routing map」把竞品对标（competitor benchmarking）的主责 Skill 定为 `ai-competitor-analyst`、支撑 Skill 为 `ai-reference-researcher`，**不含 `ai-market-researcher`**——即参考文件已修正第 2 步的断链项。
   - 第 3 节「Primary document routing」给出的首要文档是 `docs/全项目总控/MASTER_INDEX.md`、`docs/全项目总控/TASK_BACKLOG.md`、`docs/业务流程全案/` 下的任务包、`docs/架构决策记录/` 下的 ADR、`scripts/`，**不含 `rules/project_rules.md`**——同样已修正第 3 步的断链项。
   - 第 6 节「Required routing output」列出 7 项要素（任务线判断、主导 Skill、支撑 Skill、权威文档、前置事实检查、安全执行顺序、不得逾越的边界），比本正文 Step 5 模板多出「不得逾越的边界（do-not-cross boundaries）」一项，与正文的 `Boundary Warnings` 呼应。
   - 上述参考文件中的 `docs/全项目总控/TASK_BACKLOG.md`、`MASTER_INDEX.md`、`docs/业务流程全案/`、`docs/架构决策记录/`、`skills/governance/ai-reference-researcher/` 在仓库中均存在。
