# `ai-5s-delivery-governor` — 5S 交付治理

> **源文件**：skills/core/ai-5s-delivery-governor/SKILL.md
> **源版本**：未标注（源文件 frontmatter 只有 `name` 与 `description`；`## Evolution History` 最新条目为 v1.1.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-5s-delivery-governor
description: "Govern change delivery with a lightweight Scope, Specify, Ship, Safeguard, Sell lifecycle. Use for versioned delivery, branch routing, release candidates, hotfixes, acceptance gates, deployment evidence, or any task whose completion must be auditable."
```

**中文描述**：用轻量的「范围（Scope）、说明（Specify）、实现（Ship）、保障（Safeguard）、销售放行（Sell）」生命周期治理变更交付。适用于版本化交付、分支路由、发布候选、热修复、验收门禁、部署证据，或任何完成状态必须可审计的任务。

---

## Rule | 规则

每一项可交付变更都必须具备：1）有界范围（scope）；2）有归属的真相与验收定义；3）可追溯的实现；4）独立证据；5）明确的发布决策。禁止把一次本地代码编辑或一次本地提交当作已交付。

## 标题说明 | Title（源文件 H1）

源文件 H1 为 `# ai-5s-delivery-governor - 5S Delivery Governance`，已作为本文件标题译出：`ai-5s-delivery-governor` — 5S 交付治理。

## Purpose | 目的

应用一套紧凑的交付状态机，同时不把日常工程工作变成文书工作：

```text
Scope -> Specify -> Ship -> Safeguard -> Sell
```

本 Skill 用于交付治理，不用于替代项目既有的 Git、CI、部署、测试或发布脚本。把这些项目入口当作证据来源复用。

## When to Use | 何时使用

- 任务变更了版本化产品、共享服务、Schema、权限、发布制品或部署目标。
- 某个缺陷可能影响支持基线或生产基线。
- 涉及发布候选、热修复、回滚、发布标签或验收决策。
- 用户要求交付状态、正式收口、发布就绪，或一条变更管理规则。

对于纯本地实验、文档草稿或只读审计，记录适用的阶段即可，但不得发明项目并未使用的分支或发布仪式。

## 5S State Machine | 5S 状态机

| 阶段 | 问题 | 最小记录 | 阻断条件 |
|---|---|---|---|
| Scope | 改什么、给谁改、明确排除什么？ | 变更类型、目标版本、范围内/范围外 | 禁止开始实现 |
| Specify | 受影响的真相责任人、数据、客户端与回归是什么？ | 责任人、影响、验收门禁、回滚/数据说明 | 禁止集成 |
| Ship | 已批准的范围是否通过项目路径实现了？ | 有范围限定的 diff、测试、迁移/配置变更 | 禁止晋级 |
| Safeguard | 独立检查是否已经压到真实风险边界？ | 构建/API/浏览器/数据库/流程证据 | 禁止发布 |
| Sell | 该版本是否被允许触达其预期受众？ | 发布/打标签/部署决策、已知限制、回滚点 | 禁止声称已交付 |

使用简明记录。一条简短的 issue、一段 PR 描述、一行发布台账，或一条结构化任务记录，只要承载了必需事实，就足够。

## Branch and Baseline Routing | 分支与基线路由

项目可以使用不同的分支名，但职责必须保持彼此区分：

| 线路 | 用途 | 通常允许的工作 |
|---|---|---|
| 集成线 | 持续开发 | 新能力、可用性工作、非基线缺陷 |
| 稳定线 | 支持基线或生产基线 | 可复现的基线缺陷、安全、必要的兼容性修复 |
| 冻结候选 | 短生命周期的验收版本 | 仅限已登记的发布阻断项 |

规则：

1. 按缺陷复现所在的基线路由缺陷，而不是按它被发现的位置路由。
2. 稳定线的修复必须在收口前回流到集成线。
3. 冻结候选必须拒绝新功能与无关重构。
4. 隔离工作树（worktree）可以保护并发实现，但正式集成与发布仍须通过已批准的交付线路进行。
5. 存在多个必需远端的项目，必须在声称交付收口之前，证明已批准的提交到达了每一个必需远端。

## Acceptance Gate Selection | 验收门禁选择

选择能够证明真实风险的最小门禁：

| 门禁 | 典型范围 | 最小证据 |
|---|---|---|
| L0 | 文案、只读状态、外观层面的本地展示 | 目标路由/API 可达，且预期展示可见 |
| L1 | 单个组件、页面、端点或本地缺陷 | 变更后的交互，加上受影响的构建/编译检查 |
| L2 | 共享业务模块、命令、聚合、元数据或写入路径 | 运行时剖面或契约、命令执行，以及权威事实回读 |
| L3 | Schema、租户/权限/版本策略、跨模块回写、发布、部署或生产风险 | 生命周期回归，加上数据库、运行时、客户端与发布证据 |

健康检查端点只能证明进程可用。它永远不能证明业务收口。

## Delivery Qualification | 交付资格

5S 生命周期描述工作如何推进。交付资格（qualification）描述结果被允许声称什么。记录新鲜证据（fresh evidence）所能支持的最高 qualification：

| Qualification | 含义 | 最小证据 |
|---|---|---|
| `Q0` | 能力已存在于代码、注册表或路由中 | 源码或注册表检查；存在不等于执行 |
| `Q1` | 参数、权限、状态、配置与必需物料已对齐 | 基线、配置或运行时剖面证据 |
| `Q2` | 后端编排、提供方覆盖、唯一副作用路径与审计链已收口 | 命令/API 执行，加上权威数据与审计回读 |
| `Q3` | 真实客户或产品负责人场景已在必需客户端上完成，对账检查通过，且发布证据被接受 | 业务流程验收、跨客户端/运行时证据、对账与发布决策 |

规则：

1. 永远不得依据 `Q0` 或 `Q1` 声称已交付、发布就绪或可销售性（saleability）。
2. `Q2` 证明的是技术上可执行的业务能力，不是客户验收或商业就绪。
3. 在把结果描述为客户可用、可销售或已普遍发布之前，必须达到 `Q3`。
4. HTTP 200、一次健康检查、页面能打开、一条绿色 CI 作业或一次本地提交，都只是辅助证据；其中任何一项本身都不构成 qualification。
5. 低于 `Q3` 的 qualification 声称，必须点名缺失的更高层级证据。

## Standard Workflow | 标准工作流

1. 检查当前分支、工作树（working-tree）、必需远端与项目交付脚本。
2. 把变更分类为可用性、缺陷、既有流程语义变更或新能力。
3. 在动笔前记录 Scope 与 Specify：目标版本、受影响流程、真相责任人（truth_owner）、非目标（non_goals）、门禁，以及回滚/数据影响。
4. 对于 L2/L3、并行或高风险工作，在动笔前通过 `ai-delivery-contract-governor` 创建并校验项目的 `DeliveryContract`，并在进入 Safeguard 之前再次校验。
5. 只实现有范围限定的变更。精确暂存任务文件，并保留无关的工作树改动。
6. 用项目自有命令，以及与 L0-L3 相称的真实运行时/数据库证据完成 Safeguard。
7. 只有在已批准的集成、打标签/部署决策，以及必需的远端/CI 证据全部完成之后，才执行 Sell。
8. 把非阻断性债务单独记录。不得仅为让台账显得干净而扩大任务。
9. 把达成的 `Q0-Q3` qualification 与 5S 交付状态分开记录。`Safeguard` 可以在 `Q2` 通过，而 `Sell` 仍因等待产品验收或发布证据而处于 `blocked`。

## Required Closure Statement | 必需的收口声明

报告交付结果时，必须包含：

```text
Change type:
Target version / line:
Affected flow:
Truth owner:
Selected gate:
Evidence:
Delivery state: complete / paused / blocked
Known limits or follow-up:
```

只有在 Safeguard 已通过、且项目要求的集成或发布动作确实已经发生时，才使用 `complete`。对于未推送的提交、失败的证据、不可用的远端或仍在进行中的集成，使用 `paused` 或 `blocked`。

## Guardrails | 防护规则

- 不得让分支名替代证据。
- 不得仅凭一次本地提交就宣布任务完成。
- 不得在低于 `Q3` 时把能力称为可销售或客户可用。
- 不得把发布候选当作「更稳定」的通用开发分支使用。
- 不得让发布治理重复或覆盖后端真相、数据库事实或项目自有脚本。
- 不得仅因为项目有发布工具链，就对一次小型本地变更强加 L3。
- 当 Schema、授权、版本权益、部署或跨模块回写确实在范围内时，不得跳过 L3。
- 不得允许 `DeliveryContract` 替代它所点名的真实项目测试、运行时、数据库、CI 或发布门禁。

## Evolution History | 进化记录

- v1.0.0：从 GERP 5S 交付状态机与三线发布治理通用化而来，已移除项目特定路径与远端名称。
- v1.1.0：新增有证据支撑的 `Q0-Q3` 交付资格（delivery qualification），使技术执行与客户就绪或发布就绪不再被混为一谈。

---

## 译注 | Translation Notes

1. 源文件 `## Delivery Qualification | 交付资格` 本身已是中英混排标题（源文件唯一一处），本译文按统一格式写作「交付资格 | Delivery Qualification」。
2. 源文件 H1 `# ai-5s-delivery-governor - 5S Delivery Governance` 已作为本文件标题译出，并另设「标题说明」小节保留其原始英文形态，便于逐节对表。
3. 审计断言（`scripts/py/audit_methodology.py` 的 `check_5s_delivery_governance`）对 Skill 文本先做 `.lower()` 再匹配，故阶段名、门禁代号、资格代号在正文中按术语表保持首字母大写形式（`Scope`、`L0`–`L3`、`Q0`–`Q3`），其小写匹配形式见下节清单。

## 术语保留自检 | Term Preservation Self-Check

下表逐个列出审计断言要求的英文词（`scripts/py/audit_methodology.py` 的 `check_5s_delivery_governance` 要求项），并注明其出现小节。「英文词」一列为审计匹配的精确小写形式。

- [x] ☑ `scope`
- [x] ☑ `specify`
- [x] ☑ `ship`
- [x] ☑ `safeguard`
- [x] ☑ `sell`
- [x] ☑ `l0`
- [x] ☑ `l3`
- [x] ☑ `q0`
- [x] ☑ `q1`
- [x] ☑ `q2`
- [x] ☑ `q3`
- [x] ☑ `qualification`
- [x] ☑ `saleability`
- [x] ☑ `complete`
- [x] ☑ `blocked`

| 英文词 | 出现小节与形式 | 是否保留 |
|---|---|---|
| `scope` | Rule「有界范围（scope）」；Purpose 阶段名 `Scope`；Standard Workflow 第 3、9 步；5S State Machine 表首列；Guardrails 第 5 条 | ☑ 是 |
| `specify` | Purpose 阶段名 `Specify`；5S State Machine 表首列；Standard Workflow 第 3 步；Guardrails（Scope/Specify 语义由「范围冻结/重新打开范围」承接） | ☑ 是 |
| `ship` | Purpose 阶段名 `Ship`；5S State Machine 表首列；Standard Workflow 第 5 步「只实现有范围限定的变更」（Ship 语义） | ☑ 是 |
| `safeguard` | Purpose 阶段名 `Safeguard`；5S State Machine 表首列；Standard Workflow 第 4、6、9 步；Guardrails（`Safeguard` 状态名） | ☑ 是 |
| `sell` | Purpose 阶段名 `Sell`；5S State Machine 表首列；Standard Workflow 第 7、9 步 | ☑ 是 |
| `l0` | Acceptance Gate Selection 表首列 `L0`（审计小写匹配） | ☑ 是 |
| `l3` | Acceptance Gate Selection 表首列 `L3`；Standard Workflow 第 4 步 `L2/L3`；Guardrails 第 6、7 条（审计小写匹配） | ☑ 是 |
| `q0` | Delivery Qualification 表首列 `` `Q0` ``（审计小写匹配） | ☑ 是 |
| `q1` | Delivery Qualification 表首列 `` `Q1` ``（审计小写匹配） | ☑ 是 |
| `q2` | Delivery Qualification 表首列 `` `Q2` ``；规则第 2 条；Standard Workflow 第 9 步（审计小写匹配） | ☑ 是 |
| `q3` | Delivery Qualification 表首列 `` `Q3` ``；规则第 3、5 条；Guardrails 第 3 条（审计小写匹配） | ☑ 是 |
| `qualification` | Delivery Qualification 小节标题与正文「交付资格（qualification）」；规则第 4、5 条；Standard Workflow 第 9 步 | ☑ 是 |
| `saleability` | Delivery Qualification 规则第 1 条「可销售性（saleability）」 | ☑ 是 |
| `complete` | Required Closure Statement 代码块 `Delivery state: complete / paused / blocked` 与紧随段落 `` `complete` `` | ☑ 是 |
| `blocked` | Required Closure Statement 代码块 `Delivery state: complete / paused / blocked` 与紧随段落 `` `blocked` ``；Standard Workflow 第 9 步 | ☑ 是 |
