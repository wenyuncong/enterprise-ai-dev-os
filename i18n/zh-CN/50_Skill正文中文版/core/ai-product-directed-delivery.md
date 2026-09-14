# `ai-product-directed-delivery` — AI 原生产品交付操作模型

> **源文件**：skills/core/ai-product-directed-delivery/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-product-directed-delivery
description: "Run AI-native product delivery where a product owner defines outcomes, usability, and business acceptance while AI agents perform analysis, research, architecture, implementation, verification, and delivery evidence. Use for product-led enterprise delivery, non-programmer-led development, end-to-end feature work, or explaining human and agent responsibilities."
```

**中文描述**：运行 AI 原生产品交付：由产品负责人（product owner）定义结果、可用性与业务验收，AI 智能体负责分析、调研、架构、实现、验证与交付证据。适用于产品主导的企业级交付、非程序员主导的开发、端到端功能工作，或需要说明人与智能体职责边界的场合。

---

## Rule | 规则

产品负责人（product owner）决定业务结果、可用性、范围与最终验收。AI 智能体拥有工程执行路径，并且必须用代码、运行时、数据与发布证据证明该路径。禁止强迫产品负责人写代码，也禁止 AI 智能体代替负责人臆造产品意图、业务策略或验收结论。

# ai-product-directed-delivery - AI 原生产品交付操作模型（AI-Native Product Delivery Operating Model）

## Purpose | 目的

让不写代码的产品负责人也能获得产品交付能力，同时保持高标准的工程严谨性：

```text
Product intent and acceptance
  -> AI analysis and benchmark
  -> architecture and truth boundary
  -> implementation and verification
  -> product-owner business acceptance
  -> governed release
```

这不是「提示词生成页面」。这是一套受控的操作模型：人的判断保留在产品决策上，AI 智能体执行一个可验证的工程系统。

## Responsibility Boundary | 职责边界

| 角色 | 拥有 | 不拥有 |
|---|---|---|
| 产品负责人（product owner） | 业务目标、目标用户、工作流结果、产品呈现、可用性判断、优先级、非目标、最终业务验收 | 写代码、设计数据库表、选择内部框架模式、绕过验证 |
| AI 产品分析师 | 需求澄清、场景地图、验收草稿、歧义台账（ambiguity log） | 替代负责人的业务决策 |
| AI 调研员 | 竞品/参考实现证据与可选方案 | 把竞品行为当作产品决策 |
| AI 架构师 | 真相归属、领域边界、原子/编排/聚合设计、迁移风险 | 把业务真相搬进客户端，或臆造未获批的范围 |
| AI 交付智能体 | 数据库、后端、前端、测试、脚本、文档、精确暂存（exact staging） | 在没有证据与负责人确认的情况下宣布业务验收 |
| AI 验证者/审计员 | 独立的运行时、API、数据库、回写（writeback）、浏览器与发布检查 | 为失败的门禁找解释、把它说成通过 |
| 验收环节的产品负责人 | 确认目标流程对实际工作是易懂、高效且正确的 | 接受一个证据或业务结果缺失的流程 |

产品负责人可以只提供自然语言、示例、截图、参考产品，以及一条已完成的业务流程测试。AI 系统把这些输入翻译成工程工作，并用产品语言回传证据。

## Product-to-Engineering Contract | 产品到工程契约

动手实现之前，先固化最小可用的契约：

```text
Business outcome:
Primary user and scenario:
Expected visible result:
Usability constraints:
Business-flow acceptance:
Non-goals:
Known examples or references:
```

AI 团队补充：

```text
Truth owner:
Affected domain and clients:
Change type and delivery gate:
Technical acceptance:
Data/writeback/report impact:
Risk and rollback notes:
```

如果业务结果不清楚，就向产品负责人（product owner）请求澄清。如果工程路径不清楚，由 AI 自行调查；禁止把这份负担退回给产品负责人，把它变成一项编程任务。

## Shared Language and Decision Context | 共享语言与决策上下文

当一次交付引入或依赖含糊的业务术语、稳定缩写，或跨会话决策时，在 `docs/` 下创建或更新简洁的、项目自有的上下文（shared language）：

- 术语表/上下文记录定义领域术语与缩写的约定含义。
- ADR 或决策记录固化一项持久的架构或范围决策，并写明备选方案与后果。
- 规格、测试名称、API 与代码复用这套约定的语言，使智能体与人不会各造一套并行命名。

此事与风险成比例。不要为一行本地修复要求术语表，也不要让术语表变成第二个业务真相源。数据库/领域模型与已验收的业务规则仍然是权威。

## Twelve-Step Product Delivery Map | 十二步产品交付地图

| 步骤 | 产品负责人的贡献 | AI 智能体职责 | 出口证据 |
|---|---|---|---|
| 1. 结果（Outcome） | 说明用户可见的业务结果 | 把意图转成场景与非目标 | 已确认的结果契约 |
| 2. 流程（Process） | 描述真实业务流程或用例 | 映射状态、角色、输入、输出、异常 | 流程地图与验收用例 |
| 3. 对标（Benchmark） | 有用时提供参考资料 | 核实竞品行为，区分事实与选择 | 对标决策 |
| 4. 架构（Architecture） | 确认影响产品范围的取舍 | 定义领域边界、真相归属与接口 | ADR 或架构说明 |
| 5. 数据（Data） | 澄清字段的业务含义 | 核实模式（Schema）与数据归属 | 数据库/元数据证据 |
| 6. 原子后端（Atomic backend） | 只评审可见行为 | 实现或复用原子服务（atomic service）与校验 | 单元/API 证据 |
| 7. 编排（Orchestration） | 确认预期的工作流结果 | 编排原子服务（atomic service）并完成回写 | 命令流证据 |
| 8. 聚合与命令（Aggregate and command） | 确认对外动作与阻断原因合理 | 发布聚合画像/API 与命令网关（command gateway）契约 | 运行时画像与权限证据 |
| 9. 前端组合（Frontend composition） | 评审呈现与易用性 | 构建 UI 原子（ui atom）、组合、模板与 Host 页面（host page） | 浏览器证据 |
| 10. 集成（Integration） | 执行目标业务流程 | 验证页面 -> API -> 数据库 -> 回写 -> 报表 | 流程闭环证据 |
| 11. 验收（Acceptance） | 测试已完成的业务流程 | 记录缺陷、修复并重跑受影响的门禁 | 产品验收记录 |
| 12. 交付（Delivery） | 判定结果是否可以到达用户 | 跑 5S 的保障（Safeguard）/销售放行（Sell）收口并记录限制 | 发布/部署证据 |

这些步骤是依赖感知的，不是纸面流程。一次小的本地可用性改动可以走短路径；数据、权限、跨客户端命令与发布必须执行相关的完整链条。

## Backend Delivery Chain | 后端交付链

每一项可复用的业务能力都遵循这条归属路径：

```text
Database and domain facts
  -> atomic service
  -> atomic orchestration or application service
  -> aggregate interface
  -> command gateway
  -> Web / App / AI / MCP / OpenAPI adapters
  -> Host page or client surface
```

定义：

- **原子服务（atomic service）** 拥有一项内聚的业务能力：校验、持久化、计算、审计或事实生产。
- **原子编排（atomic orchestration）** 为一条业务工作流组合原子，并拥有事务、时序、补偿与下游回写。
- **聚合接口（aggregate interface）** 返回客户端就绪的读模型：运行时画像、字段、权限、支持的命令、阻断原因与相关事实。
- **命令网关（command gateway）** 是可复用业务命令的唯一可执行入口。派发之前，它检查身份、租户、授权、数据范围、版本策略、状态、幂等、确认要求、审计与提供方覆盖。
- **适配器（Adapters）** 只做传输翻译。REST、Web、App、MCP、OpenAPI、桌面端或连接器禁止重建业务规则。
- **Host** 加载并渲染聚合契约，采集被允许的输入，请求命令，并展示结果。

不要因为界面上存在一个按钮就对外暴露一条命令。只有当后端网关证明了它的契约与前置条件之后，命令才可执行。

## Frontend Delivery Chain | 前端交付链

前端有自己的复用架构，但它绝不成为第二个业务引擎：

```text
Backend runtime / FieldPackage / aggregate profile
  -> UI atom
  -> UI orchestration
  -> standard page template
  -> Host page
  -> user interaction and feedback
```

定义：

- **UI 原子（ui atom）** 是一项聚焦、可复用的视觉或交互能力，例如字段渲染器、选择器、行表格、状态标签、动作栏、筛选器、结果汇总或阻断式对话框。
- **UI 编排（UI orchestration）** 依据后端返回的运行时/画像事实组合 UI 原子。它可以协调加载、本地输入状态、导航、可访问性与呈现反馈。
- **标准模板（Standard template）** 为资料列表页、单据录入页、报表页、看板或设置页提供稳定外壳。
- **Host 页面（host page）** 选择模板并组合受支持的 UI 原子。禁止定义另一套状态机、复制字段真相、计算业务值、决定权限，或实现第二条命令路径。

前端可以为即时可用性反馈做必填项校验，但业务校验与每一次写入决策的权威仍在后端。

## Required Handoffs | 必要交接件

| 交接件 | 必需内容 |
|---|---|
| 负责人 -> AI | 结果、场景、示例、可用性期望、验收测试 |
| 分析师 -> 架构师 | 歧义点、验收标准、流程地图、对标事实 |
| 架构师 -> 交付 | 真相归属、后端链、客户端契约、受影响模板、所选门禁 |
| 交付 -> 验证者 | 范围化改动、命令/测试、预期事实、已知风险 |
| 验证者 -> 负责人 | 产品可见结果、通过/失败证据、已知限制、验收测试说明 |
| 负责人 -> 发布 | 对被测试业务流程给出 接受 / 拒绝 / 修订 决策 |

## Testable Seams and Fresh Evidence | 可测试边界与新鲜证据

对于新增或变更的领域规则、缺陷回归、命令/编排行为，以及其他可测试的公共接口：

1. 实现之前，先命名公共边界（seam）与预期行为。
2. 先写一个针对目标行为会失败的聚焦测试。
3. 实现能通过该测试的最小改动。
4. 在最后一次相关改动之后，重跑该聚焦测试与受影响的回归测试。

不要把红绿测试（red-green）强加给只改文案、生成物、纯配置或探索性任务——对这些任务，聚焦的行为测试没有意义。改为记录所选的替代证据。

在下达完成、提交、发布或就绪结论之前，必须在**最后一次相关改动之后**运行那条能证明该结论的命令、运行时检查、API 调用、数据库回读或 diff 检查。更早的通过输出、一个健康检查端点，或一份智能体报告，都不构成充分的新鲜证据（fresh evidence）。

## Standard Workflow | 标准工作流

1. 从产品结果出发，而不是从实现措辞出发。
2. 把结果转成简短场景与业务验收契约。
3. 检索当前项目已有模式，并且只在能改变真实产品决策时才做对标。
4. 设计页面前，先声明后端真相归属。
5. 复用或构建 后端原子（atomic service）-> 编排（atomic orchestration）-> 聚合（aggregate interface）-> 命令网关（command gateway）链。
6. 构建前端 运行时 -> UI 原子（ui atom）-> 组合 -> 模板 -> Host 链。
7. 独立验证技术闭环。
8. 让产品负责人（product owner）从目标用户视角执行业务流程验收（business-flow acceptance）。
9. 用 `ai-5s-delivery-governor` 确定最终交付状态与发布证据。
10. 在两条独立轴（two independent axes）上评审改动：标准/真相/架构合规性，以及原始产品结果、验收流程与非目标。
11. 把反复出现的经验回灌到已有的归属 Skill，而不是新建一套并行规则。

## Safe Change Protocol | 安全修改协议（safe change）

AI 主导的交付必须对一个不读代码的产品负责人是安全的。默认原则是**先读、先证、再改**。智能体禁止仅仅因为自己能写文件，就把仓库当成可随意处置的一次性产物。

### 1. Establish the Change Boundary | 建立改动边界

在写入、重命名、删除、迁移或执行命令之前，智能体记录：

```text
Requested business result:
Suspected truth owner and execution path:
Candidate files and why each is relevant:
Expected impact boundary:
Existing unrelated working-tree changes:
Selected verification and rollback evidence:
```

在创建替代实现之前，智能体必须搜索已有的实现、测试、路由、脚本与共享组件。一个页面上的症状，不能证明该页面就是问题归属（impact 判断需要证据）。

### 2. Classify Deletions and Destructive Operations | 对删除与破坏性操作分类

| 类别 | 示例 | 默认动作 |
|---|---|---|
| A：可丢弃 | 已确认的生成物输出、任务自有的临时证据、可复现的缓存 | 只有在证明它属于生成物或可重建之后才删除 |
| B：任务自有源文件 | 新建文件，或被已验收改动完全取代的源文件 | 删除前检查入向引用、测试、构建影响与回滚路径 |
| C：共享或来源不明 | 共享组件、服务、模式、脚本、配置、历史迁移，或归属不清的文件 | 默认保留；删除或破坏性重写前必须取得负责人明确决策 |
| D：持久化/破坏性 | 数据库行、模式、生产配置、租户数据、发布产物、`git reset --hard`、`git clean -fdx` | 未经明确确认，且没有成文的备份、范围与恢复路径，禁止执行 |

重命名与批量替换在可能打断引用或掩盖语义时，属于破坏性（destructive）操作。它们遵循与删除相同的 impact 检查。

### 3. Prove Impact Before the Change | 改动前证明影响

对于源代码删除、重命名、共享重构、模式变更或大范围替换，至少检查：

1. 用项目搜索列出引用与导入。
2. 行为对用户可见时，检查路由/菜单/运行时入口路径。
3. 依赖它的测试、构建脚本、迁移、发布脚本与生成产物。
4. 工作区（working-tree）与已暂存改动，确保不相关的在途工作不会被顺带吞掉。
5. 回滚方式：可还原补丁、保留的迁移、备份，或已知可用的提交。

禁止仅因为一个文件没有明显的直接导入就删除它。它可能被配置、反射、代码生成、构建工具、部署流程或运行时路由加载。

### 4. Use Patch-Level Control | 使用补丁级控制

- 只修改能够拥有目标结果的最小文件集合。
- 每个有意义的批次之后评审 diff，确认它只表达了已声明的改动边界。
- 在脏的工作区（working-tree）里，只暂存任务自有精确改动（exact task-owned files 或 exact hunks）；提交前检查已暂存 diff，并运行一次暂存 diff 检查。
- 禁止用仓库级清理让工作区看起来干净。不相关的改动保持原样不动。
- 未经明确确认，禁止使用 `reset --hard`、`clean -fdx` 这类破坏性（destructive）Git 命令。
- 如果证据自相矛盾，或负责人的意图含糊，停止破坏性路径，并用业务语言把该决策摆到负责人面前。

## Code Location Protocol | 精准代码定位协议（code location）

产品负责人（product owner）用业务语言描述一个缺陷或一项新能力。AI 智能体把它翻译成一条经过验证的交付路径；禁止要求负责人自己去找文件或说出类名。

### Trace Order | 追踪顺序

```text
Business symptom or requested result
  -> menu / route / permission entry
  -> actual rendered Host page
  -> standard template and shared UI component
  -> frontend service / API wrapper
  -> controller or transport adapter
  -> command gateway / aggregate interface
  -> orchestration / atomic service
  -> domain fact, FieldPackage / BusinessProfile / permission
  -> mapper / database / migration history
  -> focused tests, runtime gate, release gate
```

对于一条直接路由，要验证真实的已认证导航与实际渲染的组件。多个菜单可能共享同一个 Host；一个视觉上相似的页面，背后可能是不同的命令或不同的真相归属。

### Required Location Report Before Editing | 编辑前的必填定位报告

动手实现之前，智能体在内部、或用紧凑的产品语言向负责人报告：

```text
Suspected business flow:
Evidence found:
Exact candidate files:
Chosen owner of the fix:
Expected affected surfaces:
Verification path:
```

编码前先对结果定性：

| 发现 | 正确响应 |
|---|---|
| 仅呈现层的 UI 问题 | 在确认没有后端事实出错之后，只改共享 UI 原子/模板/Host |
| 后端真相或业务规则问题 | 修领域服务、编排、聚合接口（aggregate interface）或命令网关（command gateway）；客户端渲染返回结果 |
| 共享字段、权限、状态或命令问题 | 修权威的元数据/画像/策略，并测试所有已知客户端 |
| 跨领域副作用 | 打补丁前先追踪回写链、事务边界、审计/历史与受影响报表 |
| 业务歧义（business ambiguity） | 只向产品负责人索取所需的最小决策；禁止自行臆造业务规则 |

## Major Project Autopilot | 重大项目自动驾驶

对于企业级项目，产品负责人不需要变成开发人员，也不需要变成源文件的项目经理。负责人提供结果、示例、优先级、可用性反馈与已完成的业务流程验收。AI 智能体维护工程地图，并以可验证的批次执行它。

### Operating Loop | 运行循环

1. **框定（Frame）**：把产品结果转成场景、非目标、风险与验收流程。
2. **绘图（Map）**：发现既有架构、代码位置、依赖、脚本、数据真相与受影响客户端。
3. **分批（Batch）**：把工作拆成依赖安全的批次，并通过 `ai-5s-delivery-governor` 指定 L0-L3 门禁。
4. **执行（Execute）**：只用安全修改（safe change）与代码定位（code location）协议实现当前批次。
5. **证明（Prove）**：运行与风险相称的单元、API、数据库、浏览器、工作流、构建与发布检查。
6. **呈现（Present）**：给负责人一个可决策的结果：可见变化、已验收流程、证据、限制，以及下一个业务决策。
7. **发布或迭代（Release or iterate）**：只有在负责人验收且必需的保障完成后才发布；否则把缺陷退回正确的批次。

只有在出现真实的业务歧义（business ambiguity）、不可逆/破坏性决策、实质性范围取舍，或最终发布授权时，AI 系统才停下来询问产品负责人。工程上的不确定性属于智能体的调查责任。

## Guardrails | 防护规则

- 禁止把产品负责人降格为写工单的人；产品呈现与可用性是一等验收输入。
- 禁止要求产品负责人调试、写代码、选择 ORM 映射，或手工连接架构分层。
- 禁止在证明受影响的归属与引用边界之前，进行编辑、删除、重命名、迁移或批量替换。
- 禁止让产品负责人去定位代码文件；追踪「路由到真相」链并报告证据。
- 禁止让重大项目变成一条无人追踪的提示词流水；必须维护批次、门禁、证据与决策点。
- 禁止 AI 把截图、原型或竞品参考当成完整的业务语义。
- 禁止把业务状态、计算、授权或命令策略放进前端 UI 原子（ui atom）、编排、模板或 Host。
- 禁止让聚合接口（aggregate interface）或 Host 绕过命令网关（command gateway）直接写入。
- 禁止用静态评审代替负责人验收；必须执行业务流程测试。
- 禁止用一项通过的技术门禁去覆盖失败的产品可用性或流程验收（business-flow acceptance）。

## Integration | 集成

| 需求 | 主责 Skill |
|---|---|
| 产品计划、批次与收口 | `ai-chief-planner` |
| 竞品与参考证据 | `ai-competitor-analyst` |
| 领域/原子/聚合/命令架构 | `ai-atomic-architect` |
| 后端真相与客户端边界 | `ai-single-truth-enforcer` |
| UI 原子、模板与 Host 页面（host page） | `ai-component-standardizer` |
| 端到端业务验收证据 | `ai-flow-closure-audit` |
| 版本与发布状态 | `ai-5s-delivery-governor` |

## Evolution History | 进化记录

- v1.0.0：从反复出现的 GERP 交付证据中提炼：由一位非程序员产品负责人主导产品结果与业务验收，AI 智能体完成全栈实现、验证与受治理的发布收口。
- v1.1.0：新增安全修改（safe change）、代码定位（code location）与重大项目自动驾驶协议，来源是 GERP 在脏工作区（working-tree）、共享组件、路由追踪与证据门禁交付上的实践。

## 术语保留自检

本节逐项核对本译文保留的英文断言短语（审计脚本 FAIL 级断言），并给出首次/主要出现位置。

| # | 英文短语 | 出现在哪一小节 |
|---|---|---|
| 1 | `product owner` | `## Rule 规则`、`## Purpose 目的`（代码块内）、`## Responsibility Boundary 职责边界`、`## Product-to-Engineering Contract 产品到工程契约`、`## Twelve-Step Product Delivery Map 十二步产品交付地图`、`## Required Handoffs 必要交接件`、`## Standard Workflow 标准工作流`、`## Safe Change Protocol 安全修改协议`、`## Code Location Protocol 精准代码定位协议`、`## Major Project Autopilot 重大项目自动驾驶` |
| 2 | `atomic service` | `## Backend Delivery Chain 后端交付链`、`## Twelve-Step Product Delivery Map 十二步产品交付地图`（第 6 步）、`## Code Location Protocol 精准代码定位协议`、`## Standard Workflow 标准工作流` |
| 3 | `atomic orchestration` | `## Backend Delivery Chain 后端交付链`、`## Twelve-Step Product Delivery Map 十二步产品交付地图`（第 7 步）、`## Standard Workflow 标准工作流` |
| 4 | `aggregate interface` | `## Backend Delivery Chain 后端交付链`、`## Code Location Protocol 精准代码定位协议`、`## Guardrails 防护规则` |
| 5 | `command gateway` | `## Backend Delivery Chain 后端交付链`、`## Twelve-Step Product Delivery Map 十二步产品交付地图`（第 8 步）、`## Code Location Protocol 精准代码定位协议`、`## Guardrails 防护规则` |
| 6 | `ui atom` | `## Frontend Delivery Chain 前端交付链`、`## Twelve-Step Product Delivery Map 十二步产品交付地图`（第 9 步）、`## Standard Workflow 标准工作流`、`## Guardrails 防护规则` |
| 7 | `host page` | `## Backend Delivery Chain 后端交付链`、`## Frontend Delivery Chain 前端交付链`、`## Twelve-Step Product Delivery Map 十二步产品交付地图`（第 9 步）、`## Code Location Protocol 精准代码定位协议`、`## Integration 集成` |
| 8 | `business-flow acceptance` | `## Product-to-Engineering Contract 产品到工程契约`、`## Twelve-Step Product Delivery Map 十二步产品交付地图`（第 11 步）、`## Required Handoffs 必要交接件`、`## Standard Workflow 标准工作流`、`## Major Project Autopilot 重大项目自动驾驶`、`## Guardrails 防护规则` |
| 9 | `safe change` | `## Safe Change Protocol 安全修改协议`（标题与正文）、`## Major Project Autopilot 重大项目自动驾驶`（第 4 步）、`## Evolution History 进化记录`（v1.1.0） |
| 10 | `code location` | `## Code Location Protocol 精准代码定位协议`（标题与正文）、`## Major Project Autopilot 重大项目自动驾驶`（第 2、4 步）、`## Evolution History 进化记录`（v1.1.0） |
| 11 | `working-tree` | `## Safe Change Protocol 安全修改协议`（第 1、3、4 小节）、`## Evolution History 进化记录`（v1.1.0） |
| 12 | `destructive` | `## Safe Change Protocol 安全修改协议`（第 2、4 小节）、`## Major Project Autopilot 重大项目自动驾驶`（运行循环第 7 条） |
| 13 | `impact` | `## Product-to-Engineering Contract 产品到工程契约`（Data/writeback/report impact）、`## Safe Change Protocol 安全修改协议`（第 1、2、3 小节） |
| 14 | `exact task-owned` | `## Safe Change Protocol 安全修改协议`（第 4 小节） |
| 15 | `business ambiguity` | `## Code Location Protocol 精准代码定位协议`（结果定性表）、`## Major Project Autopilot 重大项目自动驾驶` |
| 16 | `shared language` | `## Shared Language and Decision Context 共享语言与决策上下文` |
| 17 | `fresh evidence` | `## Testable Seams and Fresh Evidence 可测试边界与新鲜证据` |
| 18 | `two independent axes` | `## Standard Workflow 标准工作流`（第 10 条） |

**专有标识符保留核对**：`Host`、`FieldPackage`、`BusinessProfile`、`L0-L3`（`## Major Project Autopilot 重大项目自动驾驶`）在正文中原样保留；`DeliveryContract`、`Q0`–`Q3`、`P0`–`P3` 在本 Skill 源文件中未出现，故本译文不注入其语义，仅在需要时按术语表口径保持英文形态。Skill 名（`ai-chief-planner`、`ai-competitor-analyst`、`ai-atomic-architect`、`ai-single-truth-enforcer`、`ai-component-standardizer`、`ai-flow-closure-audit`、`ai-5s-delivery-governor`）、路径（`skills/core/ai-product-directed-delivery/SKILL.md`、`docs/`）与命令（`git reset --hard`、`git clean -fdx`）均按原样保留。
