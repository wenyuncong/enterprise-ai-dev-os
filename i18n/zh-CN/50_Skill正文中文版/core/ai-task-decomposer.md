# `ai-task-decomposer` — 复杂任务拆解引擎

> **源文件**：skills/core/ai-task-decomposer/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-task-decomposer
description: "Break complex work into safe executable batches with dependencies, scope boundaries, acceptance criteria, evidence requirements, and handoff-ready task slices. Use for multi-module tasks, long-running work, parallel execution, or ambiguous implementation requests."
```

**中文描述**：把复杂工作拆成安全的可执行批次（executable batch），带依赖、范围边界、验收标准、证据要求，以及可直接交接（handoff-ready）的任务切片。用于多模块任务、长周期工作、并行执行，或实现要求含糊的请求。

---

## Purpose | 目的

把宽泛或混合的工作转换为：

- 范围冻结、可独立执行的任务批次
- 现状 / 目标 / 实现三者分离
- 依赖感知排序，并识别阻塞项
- 每个批次自带验收标准与证据规则
- 内部任务包（internal pack）与外部派发包（external dispatch）的输出形态判定

本 Skill 用于**拆解（decomposition）**，不负责顶层路由，也不负责执行本身。

## Rule | 规则

**禁止凭想象拆分。**

拆分之前，先核实足够的仓库事实，把三类内容分开：

1. 现状事实（现在存在什么）
2. 目标态决策（我们要什么）
3. 可执行实现工作（怎样到达那里）

## When to Use | 触发条件

- 跨模块或跨端（前端 + 后端 + 数据库）任务
- 单个 AI 会话无法安全完成的大任务
- 因依赖顺序不清而被阻塞
- 计划用于并行会话或分阶段派发
- 用户提出：“把这个拆一下”“拆解这个任务”“给这项工作做个计划”

## Check-Before-Execute | 前置检查

拆分之前，先核实：

1. 当前分支与工作区（working-tree）状态
2. 已有任务包、执行记录
3. 同一主题是否已经存在拆解包
4. 热点文件或协作边界
5. 哪些工作属于事实核查、设计、实现还是验收

## Standard Workflow | 标准工作流

### 1. Freeze Scope | 冻结范围

明确写清：

- **范围内（In scope）**：确切的模块、文件、领域
- **范围外（Out of scope）**：明确排除的区域
- **受影响区域（Impacted areas）**：受影响的模块/文件/领域

### 2. Reuse Existing Artifacts | 复用已有产物

优先扩展现有拆解包，而不是另建并行包。

### 3. Separate into Layers | 分层分离

必须区分：

| 层 | 说明 |
|---|---|
| **Current-State Verification（现状核查）** | 开工前要核查什么 |
| **Target Design / Decision（目标设计/决策）** | 动手构建前要决定什么 |
| **Implementation Work（实现工作）** | 实际的代码/文档改动 |
| **Verification & Backfill（验证与回填）** | 如何证明做对了 |

### 4. Build Executable Batches | 构建可执行批次

每个批次必须：

- 可独立理解（可交给另一个智能体）
- 足够小，能在一个专注轮次内完成（约 30–60 分钟工作量）
- 归属与写入范围清晰
- 明确写出验收与证据
- 当领域行为或缺陷回归可测试时，明确写出其公开可测试边界（public test seam）
- 当属于 L2/L3、并行或高风险工作时，明确写出其任务自有 DeliveryContract 路径与写入白名单（write allowlist）

### 5. Mark Dependencies | 标记依赖

使用阻塞优先排序：

- Type A：必须先于 B 完成，B 才能开始
- Type B：可以与 C 并行
- Type C：应当等 A 和 B 完成

### 6. Choose Output Form | 选择输出形式

| 形式 | 何时使用 |
|---|---|
| **Internal Decomposition Pack（内部拆解包）** | 单开发者、顺序执行 |
| **External Dispatch Pack（外部派发包）** | 多开发者/多智能体、并行执行 |
| **Handoff Block（交接块）** | 交接给另一个 AI 会话 |

## Required Output Structure | 必需输出结构

```markdown
## Task Decomposition: [Task Name]

### 1. Scope & Verified Inputs
- In scope: [...]
- Out of scope: [...]
- Verified facts: [...]

### 2. Main Blockers & Current Facts
- [blocker-1]
- [blocker-2]

### 3. Current / Target / Implementation Split
| Layer | Status | Details |
|---|---|---|
| Current-State Verification | [pending/complete] | [...] |
| Target Design | [pending/complete] | [...] |
| Implementation | [pending/complete] | [...] |
| Verification | [pending/complete] | [...] |

### 4. Task Batch Table
| ID | Priority | Batch | Dependency | Est. Time | Acceptance |
|---|---|---|---|---|---|
| B-01 | P0 | [...] | None | 30m | [...] |
| B-02 | P1 | [...] | B-01 | 45m | [...] |

### 5. Acceptance & Evidence Rules
- [rule-1]
- [rule-2]
- Testable seam and red-green evidence: [focused test or justified alternative]
- Fresh final evidence: [command/check run after the final relevant change]
- Two-axis review: [standards/truth result] + [product acceptance/non-goals result]
- Delivery contract: [not required / contract path + validator result]

### 6. Output Form
[Internal / External / Handoff]
```

**模板字段中文对照**（字段名保持英文，照抄为上表即可套用）：

| 字段 / 小节 | 中文含义 | 填写要求 |
|---|---|---|
| `Task Decomposition: [Task Name]` | 任务拆解：〔任务名〕 | 任务名用业务语言，不用文件名 |
| `1. Scope & Verified Inputs` | 范围与已核实输入 | `In scope`/`Out of scope` 逐条列；`Verified facts` 只写已核实的仓库事实 |
| `2. Main Blockers & Current Facts` | 主要阻塞项与现状事实 | 每条阻塞项写明卡点与解除条件 |
| `3. Current / Target / Implementation Split` | 现状 / 目标 / 实现三分 | `Status` 取 `pending` 或 `complete` |
| `4. Task Batch Table` | 任务批次表 | `ID` 用 `B-01` 形式；`Priority` 用 P0/P1/P2；`Dependency` 写 `None` 或批次 ID；`Est. Time` 用分钟；`Acceptance` 写可判定的验收条件 |
| `5. Acceptance & Evidence Rules` | 验收与证据规则 | 必须含可测试边界与红绿测试（red-green test）证据、最终新鲜证据（fresh evidence）、双轴（two independent axes）审查结论、DeliveryContract 判定 |
| `6. Output Form` | 输出形式 | 取 Internal / External / Handoff 三者之一 |

## Guardrails | 防护规则

- 当工作并非原子时，禁止输出一个巨型任务
- 禁止拆得过细，以致业务含义消失
- 除非紧耦合，禁止把现状核查与实现混在一起
- 并行工作时，禁止忽略热点文件冲突风险
- 禁止不先检查已有任务包就动手拆解

## Maturity | 成熟度

**Stage**：effective —— 在 GERP ERP 项目上经 100+ 次拆解实战检验。

## Evolution History | 进化记录

- v1.0.0：提炼自 gerp-task-decomposer，并通用化为普适用法
- 来源：GERP Enterprise ERP，PDCA 驱动的拆解模板器（decomposition templater）

---

## 译注

1. **代码围栏缺陷（原样保留）**：源文件两个模板代码块使用单个反引号作围栏（`` `markdown `` 开头、`` ` `` 结尾），而非三个反引号。这是源文件的格式缺陷；按“代码块原样复制、不译”的口径，中文版把围栏改为标准三反引号以便正常渲染，**块内所有内容一字未改**。此条为唯一一处非内容性改动，特此声明。
2. **源版本**：源文件 frontmatter 只有 `name` 与 `description`，无版本号/日期标注，故记「未标注」；`## Evolution History` 的 v1.0.0 是 Skill 内容自身的演进记录，不等于源文件版本标注。
3. **`DeliveryContract` 落点可解析**：源文件要求“任务自有 DeliveryContract 路径与写入白名单”，仓库中对应模板为 `docs/_templates/全项目总控/task_contract.json`，模式（Schema）为 `docs/全项目总控/schemas/governance/delivery-contract.schema.json`，校验脚本为 `scripts/py/validate_delivery_contract.py`，三者均存在。
4. **门禁代号范围**：源文件只出现 `L2/L3` 与 P0/P1（未出现 `L0`/`L1`，未出现 P2/P3、`Q0`–`Q3`）。中文版按源文件原样保留，未补写未出现的代号。
5. **`Type A/B/C` 与 P 代号含义**：源文件第 5 步的 `Type A/B/C` 指依赖关系类型，与项目原型 `A/B/C`（Archetype A/B/C）不是同一概念，译文按源文语义分别处理，未做术语合并。
6. **无断链引用**：`DeliveryContract`、`write allowlist`、`public test seam`、`red-green`、`two independent axes` 等英文断言短语均按术语表口径保留英文原文。
7. **存在未被引用的配套参考文件**：本 Skill 目录下有 `skills/core/ai-task-decomposer/references/decomposition-template.md`，但 SKILL.md 正文从未提到 `references`，读者从正文无法得知它存在。该参考文件比正文的「必需输出结构」更完整，建议英文源在后续版本中补一条指向关系。与正文的差异如下（供对照时参考，不代表中文版扩大了译文范围）：
   - 正文「必需输出结构」是 6 段式骨架；参考文件是 8 节表格化模板（含 `Scope Freeze` 表、`Verified Current-State Facts` 四类事实表、10 列 `Batch Table`、`Internal Pack vs External Dispatch` 选择表、`Handoff Block Template`、`Typical batch order`）。
   - 优先级取值：正文批次表示例只出现 `P0`、`P1`；参考文件写的是 `P0/P1/P2`。中文版正文按正文原样译出，未混入参考文件的取值。
   - 参考文件第 7 节 `Handoff Block Template` 用 `text` 代码块给出 12 个英文字段（`Task ID` 至 `Do-not-touch boundaries`），正文没有该模板。
   - 参考文件引用的 `AGENTS.md`、`docs/全项目总控/TASK_BACKLOG.md`、`docs/全项目总控/MASTER_INDEX.md` 在仓库中均存在；其中「claim-pool row」「master task-table row」在仓库中未见同名文件，属参考文件自身的描述性说法。
