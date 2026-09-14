# 01 — Skill 体系分层架构 | Skill System Layered Architecture

> **源文件**：methodology/01_Skill体系分层架构.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。
> **所属（Part of）**：企业级全 AI 开发方法论（Enterprise-Grade Full AI Development Methodology）
> **前置（Prerequisite）**：00_核心方法论白皮书

---

## 1. 为什么需要分层架构？ | Why a Layered Architecture?

单文件形式的 AI 规则（例如 .cursorrules）存在三个致命缺陷：

| 缺陷 | 说明 |
|---|---|
| **扁平上下文** | 所有内容挤在一个文件里——AI 无法区分路由规则、代码规则与进化规则 |
| **无法委派** | 一个大规则文件意味着每个任务都要加载全部规则，哪怕绝大多数毫不相关 |
| **静态** | 规则不会自我改进——写一次就开始腐烂 |

解决之道是一套**五层架构（Classification → Routing → Decomposition → Execution → Evolution）**，每层职责各不相同：

## 2. 第 0 层：分类层 | Layer 0: Classification

**Skill**：`ai-project-classifier`

### 职责 | Responsibility
在项目启动时按四个维度对每个项目分类：
- **来源（Origin）**：老项目（Brownfield，存量）vs 新项目（Greenfield，全新）
- **质量目标（Quality Target）**：快速原型（Rapid Prototype）vs AI 原生（AI-Native）vs 企业级（Enterprise）
- **部署目标（Deploy Targets）**：Web / Mobile / WeChat / MCP / 全平台
- **规模（Scale）**：单体（Monolith）vs 原子服务（atomic service）vs 微服务（Microservices）

### 为什么单独成层 | Why It's Separate
分类在项目启动时**只发生一次（exactly ONCE）**（范围变更时重跑）。它决定加载哪些 Skill、采用哪种架构，以及“完成”到底指什么。若没有显式分类，方法论会把原型过度工程化，又会把生产系统做得欠工程化。

### 关键设计决策 | Key Design Decision
**不确定时默认 AI 原生（AI-Native）。** 从 AI 原生降级为快速原型，比事后把原型升级到生产质量要容易得多。

---

```text
+--------------------------------------------------+
|  LAYER 1: ROUTING                                 |
|  "Which rules, skills, and docs apply to THIS     |
|   specific task?"                                 |
|  Owner: ai-rule-dispatcher                        |
+--------------------------------------------------+
                         |
                         v
+--------------------------------------------------+
|  LAYER 2: DECOMPOSITION                           |
|  "How do we break THIS task into safe,            |
|   executable batches?"                            |
|  Owner: ai-task-decomposer                        |
+--------------------------------------------------+
                         |
                         v
+--------------------------------------------------+
|  LAYER 3: EXECUTION                               |
|  "Write the code. Follow the 13-step order.       |
|   Use the right tech skill."                      |
|  Owners: tech-specific skills (e.g., java-springboot, vue)|
|          mysql-best-practices, etc.               |
+--------------------------------------------------+
                         |
                         v
+--------------------------------------------------+
|  LAYER 4: EVOLUTION                               |
|  "What did we learn? Which skill needs updating?" |
|  Owner: ai-skill-evolver                          |
+--------------------------------------------------+
```

---

## 3. 第 1 层：路由层 | Layer 1: Routing

**Skill**：ai-rule-dispatcher

### 职责 | Responsibility
在写任何代码之前确定执行上下文：
- 属于哪条项目线（主线、治理、审计、研究）？
- 必须先加载哪些规则与文档？
- 应由哪个 Skill 主导执行？
- 必须先完成哪些事实核查？

### 为什么单独成层 | Why It's Separate
路由是一个**元关注点**——它不写代码，而是告诉其他层该做什么。如果路由逻辑混进执行规则里，AI 就会把上下文浪费在加载无关指令上。

### 关键设计决策 | Key Design Decision
**一个任务只有一个主导 Skill。** 绝不指派多个主导 Skill。支撑类 Skill 可以按需加载，但路由只产出唯一一条主执行路径。

---

## 4. 第 2 层：分解层 | Layer 2: Decomposition

**Skill**：ai-task-decomposer

### 职责 | Responsibility
把复杂任务转换为相互独立、依赖感知的批次：
- 范围冻结（Scope freeze，范围内 / 范围外）
- 现状核验 → 目标设计 → 实现 → 验证
- 批次表，含优先级、依赖与验收标准
- 决策：内部任务包（单个开发者）还是外部派发（并行智能体）

### 为什么单独成层 | Why It's Separate
分解是一个**计划关注点**——它产出计划，不产出代码。把它与执行分离意味着：
- 计划可以在写代码之前被评审
- 批次可以派发给不同的智能体
- 失败的批次可以重新规划，而不必重跑全部工作

---

## 5. 第 3 层：执行层 | Layer 3: Execution

**Skills**：领域专用核心 Skill（ai-task-decomposer、ai-command-executor、ai-tool-bootstrapper、ai-library-first、ai-architect-governor、ai-atomic-architect、ai-foundation-governor）与治理类 Skill（ai-single-truth-enforcer、ai-component-standardizer、ai-frontend-audit、ai-runtime-verify、ai-ui-ux-governor、ai-flow-closure-audit、ai-domain-boundary-mapper、ai-field-package-governor）

### 职责 | Responsibility
按照**强制工程纪律**执行批次计划：
- 13 步开发顺序（强制执行）
- 每一步都先检查后执行
- 数据驱动：数据库是唯一真相源
- 每一步之后都要验证

### 为什么单独成层 | Why It's Separate
执行类 Skill 是**领域专用**的——Vue 开发 Skill 不应包含 Docker 部署规则。每个技术 Skill 都自包含，可独立加载。

### Skill 如何被选中 | How Skills Are Selected
路由者依据任务类型选择执行 Skill：
- 数据库变更 → mysql-best-practices
- 后端 API → java-springboot 或等价 Skill
- 前端页面 → vue 或等价 Skill
- 全栈 → 按 后端 → 前端 的顺序依次派发

---

## 6. 第 4 层：进化层 | Layer 4: Evolution

**Skill**：ai-skill-evolver

### 职责 | Responsibility
任务完成后改进 Skill 体系：
- 识别重复出现的模式
- 对缺口分类（更新 Skill、新建 Skill、修改规则、仅更新文档）
- 更新 SKILL.md 文件
- 在归档中记录进化
- 把变更同步到各 AI 工具

### 为什么单独成层 | Why It's Separate
进化是一个**元-元关注点**——它修改的正是约束执行的那些规则。没有专门的进化层，Skill 会停滞，方法论会在数周内衰减。

---

## 6. 治理层（横向） | Governance Layer (Horizontal)

除了四个纵向层之外，还有一层**横向治理层**，跨所有层审计质量：

| Skill | 审计对象 |
|---|---|
| ai-flow-closure-audit | 业务链：页面 → API → DB → 回写 → 报表 |
| ai-frontend-audit | 页面可用性、UI 一致性、性能 |
| ai-domain-boundary-mapper | 对象归属、Schema 摆放、跨领域链路 |
| ai-competitor-analyst | 与市场领先者的功能差距 |

治理类 Skill **周期性触发**（不是每个任务都触发），产出带优先级修复任务的结构化审计报告。

---

## 7. Skill 生命周期 | Skill Lifecycle

每个 Skill 都要经过若干成熟度阶段：

```text
declared → callable → effective → in-closure → evolving
```

| 阶段 | 含义 | 所需证据 |
|---|---|---|
| declared | SKILL.md 存在 | 磁盘上文件存在 |
| callable | 可以按名称调用 | 被 AI 成功加载 |
| effective | 产出正确结果 | 5+ 次成功完成任务 |
| in-closure | 具备验收标准 | 证据规则已文档化 |
| evolving | 正在被持续改进 | 进化记录中已有条目 |

ai-skill-evolver 负责跟踪并升级成熟度评级。

---

## 9. 反模式（不要这样做） | Anti-Patterns

| 反模式 | 为什么会失败 |
|---|---|
| **一个巨型规则文件** | 上下文过载，每个任务都加载无关规则 |
| **把路由与执行混在一起** | AI 无法区分「做什么」与「怎么做」 |
| **没有进化层** | Skill 停滞，方法论数周内衰减 |
| **技术 Skill 之间直接互相引用** | 形成循环依赖，破坏模块化 |
| **把治理混进执行** | 每个任务都加载审计规则，浪费上下文 |

---

## 10. 设计原则 | Design Principles

1. **关注点分离**：每层只做一件事，不重叠。
2. **渐进加载**：只加载与当前任务相关的 Skill
3. **证据驱动**：每个主张都必须可验证
4. **自我改进**：系统每完成一项任务就变得更好
5. **工具无关**：可用于 Codex、Cursor、Copilot 或任意 AI 编码工具

---

*下一篇：[02_自动寻路与任务调度.md] —— 深入解析 ai-rule-dispatcher 如何路由任务*

---

## 译注

### 编号与结构异常（照原样翻译，未改号）

1. **`## 6.` 编号重复**：源文件先有 `## 6. Layer 4: Evolution | 进化层`，随后又出现 `## 6. Governance Layer (Horizontal) | 治理层（横向）`。译文保留两个 `## 6.`，未改为 `## 7.`。
2. **缺 `## 8.`，且 `## 7.` 直接跳到 `## 9.`**：源文件序列为 `## 6.`、`## 6.`、`## 7. Skill Lifecycle`、`## 9. Anti-Patterns`、`## 10. Design Principles`，其中 `8` 号缺失。译文保留原编号，未补号、未重排。
3. **`###` 子标题只有英文**：源文件 §2–§6 的子标题为 `### Responsibility`、`### Why It's Separate`、`### Key Design Decision`、`### How Skills Are Selected`，均无中文对照；而同文件 `##` 级标题是「英文 | 中文」双语。译文按中文版标题口径补出中文标题，层级与顺序未变。
4. **ASCII 分层图位置与内容**：源文件中该图位于 §2（第 0 层）结束之后、§3（第 1 层）之前，且图中只有 `LAYER 1`–`LAYER 4` 四个画框，**没有 Layer 0 的画框**，与 §1 所称「五层架构」不完全对应。译文按原位置、原内容逐字复制该图（含空格对齐），未补画 Layer 0，也未前移。
5. **伪代码块围栏不合法**：源文件全文的代码块都用**单个反引号行**作围栏——ASCII 分层图（第 39–70 行）与 Skill 生命周期链（第 171–173 行）均以单独一行 `` ` `` 开头和结尾，而非三反引号围栏，CommonMark 渲染会丢失等宽与换行。译文把两处规范化为 ```text 围栏，**围栏内文本逐字复制**（含对齐空格与换行），未改动一字。
6. **§1 表格与 §2 标题之间缺空行**：源文件第 18 行（表格最后一行）与第 19 行 `## 2. Layer 0: Classification` 之间没有空行，部分 Markdown 渲染器会吞掉该标题。译文补空行以保证渲染，编号与内容未变。
7. **标题语序与文件号前缀**：源文件 `##` 级标题为「英文 | 中文」，译文统一为「中文 | English」；文件内标题保留源文件的 `01 —` 前缀。

### 内容一致性观察（供总控核对，不属于编号问题）

1. **§5 把 `ai-task-decomposer` 列为执行层 Skill**，而 §4 明确 `ai-task-decomposer` 是**第 2 层（分解层）**的所有者，两者相互矛盾。译文照原样翻译该清单。
2. **§5 的 Skills 列表**把「领域专用核心 Skill」与「治理类 Skill」两条清单压在同一行内，未分行、未分小标题，可读性差；译文照原样保留单行结构。
3. **「四个纵向层」与「五层架构」的表述不一致**：§6（治理层）称「除了四个纵向层之外」，而 §1 与第 0 层被计入后共五层。译文照原样保留「四个纵向层」。
4. **§9 与 §10 之间跳号**导致的编号空洞（缺 `8`），与第 2 条异常同源，提醒总控：若后续英文源补写 `## 8.`，中文版须在同一位置同步补译。

### ⚑ 英文断言短语覆盖（以源文件实际出现为准）

**源文件出现、译文中原样保留英文的 ⚑ 项**：

| ⚑ 短语 | 源文件位置 | 译文处理 |
|---|---|---|
| `atomic service` | §2「Scale: Monolith vs Atomic Services vs Microservices」 | 保留英文：`原子服务（atomic service）` |
| `Scope` | §4「Scope freeze (in/out)」 | 保留英文：`范围冻结（Scope freeze，范围内 / 范围外）` |

**源文件未出现、因而无从保留的 ⚑ 项**（本篇源文件不含这些断言短语，列出供总控核对覆盖口径）：`product owner`、`5S Delivery Governance`、`Specify`、`Ship`、`Safeguard`、`Sell`、`qualification`、`saleability`、`Q0`–`Q3`、`product-directed AI delivery`、`business-flow acceptance`、`business ambiguity`、`shared language`、`fresh evidence`、`two independent axes`、`safe AI change and code location`、`code location`、`read, prove, then change`、`working-tree`、`destructive`、`impact`、`exact task-owned`、`exact file or hunk staging`、`review two independent axes`、`fresh evidence before claims`、`command gateway`、`atomic orchestration`、`aggregate interface`、`ui atom`、`Host`、`host page`、`l0`–`l3`、`complete`、`blocked`、`fail-closed`。

**保留英文的标识符与代码块**：`ai-project-classifier`、`ai-rule-dispatcher`、`ai-task-decomposer`、`ai-command-executor`、`ai-tool-bootstrapper`、`ai-library-first`、`ai-architect-governor`、`ai-atomic-architect`、`ai-foundation-governor`、`ai-single-truth-enforcer`、`ai-component-standardizer`、`ai-frontend-audit`、`ai-runtime-verify`、`ai-ui-ux-governor`、`ai-flow-closure-audit`、`ai-domain-boundary-mapper`、`ai-field-package-governor`、`ai-competitor-analyst`、`ai-skill-evolver`、`mysql-best-practices`、`java-springboot`、`vue`、`SKILL.md`、`.cursorrules`、`LAYER 1`–`LAYER 4`、`declared → callable → effective → in-closure → evolving`、`02_自动寻路与任务调度.md`。
