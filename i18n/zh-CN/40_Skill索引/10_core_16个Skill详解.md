# core 层 16 个 Skill 中文详解 | Core Layer Skills

> **源文件**：skills/core/*/SKILL.md、skills/SKILL_MANIFEST.json
> **源版本**：SKILL_MANIFEST.json updatedAt 2026-07-28
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：Skill 名、路径、门禁代号保持英文；本文件为中文摘要，不是正文全文（正文中文版见 50_Skill正文中文版/core/）。

---

## 0. 一览表

| Skill | 层 | 中文名 | 一句话职责 | 何时加载 |
|---|---|---|---|---|
| `ai-5s-delivery-governor` | core | 5S 交付治理 | 用范围（Scope）/说明（Specify）/实现（Ship）/保障（Safeguard）/销售放行（Sell）生命周期治理版本化交付、分支路由与发布收口 | 变更版本化产品、共享服务、schema、权限、发布物或部署目标时 |
| `ai-architect-governor` | core | 跨域架构治理 | 治理跨域架构决策、领域边界、真相归属与 ADR | 任务改动架构、跨模块跨平台或需要架构决策记录时 |
| `ai-atomic-architect` | core | AI 原生原子架构 | 定义 `atomic service` + `atomic orchestration` + 统一接口，并以 `aggregate interface`/`command gateway` 收口 | 设计服务拆分、后端真相归属、可复用业务命令或 Host 客户端时 |
| `ai-chief-planner` | core | 端到端项目规划与收口 | 做项目级规划、依赖调度、进度跟踪与收口验证 | 需要项目级协调、多步交付、待办台账治理或最终收口规划时 |
| `ai-command-executor` | core | 标准化命令执行 | 把执行请求转成标准化、可审计、可诊断的命令运行 | 任何 shell/CLI 操作、运行时排障或工具安装决策之前 |
| `ai-delivery-contract-governor` | core | 可执行交付契约治理 | 创建并校验机器可读的 `DeliveryContract`，用写入白名单与 `fresh evidence` 做失败即阻断（fail-closed）门禁 | L2/L3 交付、并行智能体、破坏性/跨模块/schema/发布边界任务 |
| `ai-foundation-governor` | core | 稳定基座与唯一真相治理 | 治理版本控制、权限、菜单路由、参数、Schema 迁移等共享基座 | 改动基座行为或共享项目基础设施时 |
| `ai-library-first` | core | 库优先开发治理 | 强制写自研代码前先核查成熟库、框架内建能力与项目既有工具 | 任何新写逻辑、解析器、UI 组件、引擎、集成或脚本之前 |
| `ai-multi-agent-orchestration` | core | 多智能体编排 | 按领域拆分并把依赖矩阵、契约优先集成、验收边界分配给多个智能体 | 任务跨多模块/多领域，或要把工作扇出给多个智能体时 |
| `ai-product-directed-delivery` | core | 产品主导的全 AI 交付 | 划定 `product owner` 与 AI 智能体的职责边界，给出十二步交付地图与双链契约 | 产品主导的企业级交付、非程序员主导开发或端到端功能交付 |
| `ai-project-classifier` | core | 项目分类器 | 按来源/质量目标/部署目标/规模四维分类，确定方法论路径与 Skill 集 | 项目启动、接入新代码库或范围发生重大变化时（永远最先运行） |
| `ai-rule-dispatcher` | core | 规则与任务路由 | 把任务路由到正确规则、Skill、首要文档、前置事实检查与安全执行顺序 | 每个非平凡任务开始时，特别是请求跨端跨域或语义含糊时 |
| `ai-skill-evolver` | core | Skill 进化引擎 | 从具体证据改进 Skill、分类差距、记录进化并提出新 Skill 候选 | 完成一批相关任务后、某一模式重复 3 次以上或用户要求改进 Skill 时 |
| `ai-skill-governor` | core | Skill 体系健康治理 | 按周期审计 Skill 体系的矛盾、重叠、腐蚀、有效性与孤儿 | 每周/每月方法论评审，或 Skill、规则、项目结构重大变更之后 |
| `ai-task-decomposer` | core | 复杂任务分解 | 把宽泛工作拆成范围冻结、依赖感知、可独立执行的可执行批次 | 跨模块跨端任务、单次会话装不下的大任务或需要并行分发时 |
| `ai-tool-bootstrapper` | core | 工具自举与环境自愈 | 检测、获取、注册并验证缺失工具，先查工具注册表再安装 | 出现「命令找不到/模块找不到」、版本不对或环境自检失败时 |

---

## 1. `ai-5s-delivery-governor` — 5S 交付治理

- **源文件**：`skills/core/ai-5s-delivery-governor/SKILL.md`
- **成熟度**：verified（`SKILL_MANIFEST.json` 标为 verified）
- **用途**：为可审计的变更交付提供一套紧凑的生命周期状态机：范围（Scope）→ 说明（Specify）→ 实现（Ship）→ 保障（Safeguard）→ 销售放行（Sell）。它只管交付治理，禁止替代项目既有的 Git、CI、部署、测试或发布脚本；项目自有入口脚本才是证据来源。
- **触发条件**：任务改动版本化产品、共享服务、schema、权限、发布物或部署目标时；缺陷可能影响支持基线与生产基线时；涉及 release candidate、热修复（hotfix）、回滚（rollback）、release tag 或验收决策时；用户询问交付状态、正式收口、发布就绪或变更管理规则时。纯本地实验、文档草稿、只读审计只记录适用阶段，不得虚构项目并不使用的分支或发布仪式。
- **核心规则**：每个可交付变更必须同时具备五项：1）有界范围；2）归属真相与验收定义；3）可追溯的实现；4）独立证据；5）显式的发布决策。禁止把本地代码编辑或本地提交当作「已交付」。轻量记录即可（issue、PR 描述、发布台账行或结构化任务记录），但必须承载所需事实。
- **关键流程/检查点**（`## Standard Workflow`，9 步）：
  1. 检查当前分支、工作区（working-tree）、必需远端与项目交付脚本。
  2. 归类变更：可用性、缺陷、既有流程语义变更，还是新能力。
  3. 写代码前记录 Scope 与 Specify：目标版本、受影响流程、真相责任人、非目标、门禁、回滚与数据影响。
  4. L2/L3、并行或高风险工作，必须通过 `ai-delivery-contract-governor` 创建并校验 `DeliveryContract`（写前一次、Safeguard 前再一次）。
  5. Ship 只放行范围内的改动：按精确任务文件暂存，保留无关工作区改动。
  6. Safeguard 使用项目自有命令与真实运行时/数据库证据，规模匹配 L0–L3。
  7. Sell 只在既定集成、tag/部署决策与必需远端/CI 证据齐备后进行。
  8. 非阻断性欠债单独记录；不得为了让台账好看而扩大任务。
  9. `Q0`–`Q3` 交付资格单独记录，不与 5S 交付状态混写；`Safeguard` 可以在 `Q2` 通过，而 `Sell` 因等待产品验收或发布证据仍处于阻断。
- **门禁与资格**：
  - 阶段阻断语义：Scope 未定不得开始实现；Specify 未定不得集成；Ship 未过不得 promoted；Safeguard 未过不得发布；Sell 未定不得声称交付。
  - 三条线（分支/基线路由）：Integration line（持续开发）/ Stable line（支持或生产基线）/ Frozen candidate（短期验收版本，只收已登记发布阻断项）。规则：按缺陷**复现**的基线路由，而非按发现位置；稳定线修复必须在收口前回流集成分支；冻结候选必须拒绝新功能与无关重构；多必需远端项目必须证明既定提交到达每个必需远端才算收口。
  - `L0`–`L3` 门禁：`L0` 复制、只读状态、本地展示类改动 —— 最小证据为目标路由/API 可达且预期展示可见；`L1` 单组件/页面/接口或本地缺陷 —— 变更交互加上受影响的构建/编译检查；`L2` 共享业务模块、命令、聚合、元数据或写入路径 —— 运行时 profile 或契约、命令执行与权威事实回读；`L3` schema、租户/权限/版本策略、跨模块回写、发布、部署或生产风险 —— 生命周期回归加上数据库、运行时、客户端与发布证据。仅健康端点只证明进程存活，永远不证明业务收口。
  - `Q0`–`Q3` 交付资格（delivery qualification）：`Q0` 能力存在于代码/注册表/路由中（存在不等于执行）；`Q1` 参数、权限、状态、配置与必需材料对齐；`Q2` 后端编排、provider 覆盖、唯一副作用路径与审计链闭合；`Q3` 真实客户或 `product owner` 场景在所需客户端完成、对账通过且发布证据被接受。规则：禁止用 `Q0`/`Q1` 声称交付、发布就绪或 saleability；`Q2` 只证明技术可执行业务能力，不等于客户验收或商业就绪；`Q3` 是描述为「客户可用/可销售/正式发布」的前置条件；HTTP 200、健康检查、页面能打开、CI 绿、本地提交一律只是支撑证据；低于 `Q3` 的资格声明必须点名缺失的更高层证据。
- **必交产出**：`Required Closure Statement` 收口声明，字段为 Change type、Target version / line、Affected flow、Truth owner、Selected gate、Evidence、Delivery state: `complete` / `paused` / `blocked`、Known limits or follow-up。只有在 Safeguard 通过且项目必需的集成或发布动作真实发生后才可用 `complete`；未推送提交、证据失败、远端不可用或集成进行中一律用 `paused` 或 `blocked`。
- **防护规则**（`## Guardrails`）：
  1. 禁止让分支名替代证据。
  2. 禁止仅凭本地提交就宣布任务 `complete`。
  3. 禁止在低于 `Q3` 时称能力可销售或客户可用。
  4. 禁止把 release candidate 当成「更稳定」的通用开发分支。
  5. 禁止让发布治理重复或覆盖后端真相、数据库事实或项目自有脚本。
  6. 禁止仅因项目有发布工具就对小改动强推 `L3`。
  7. 禁止在 schema、授权、版本权益、部署或跨模块回写**实际在范围内**时跳过 `L3`。
  8. 禁止让 `DeliveryContract` 取代它所指的真实项目测试、运行时、数据库、CI 或发布门禁。

---

## 2. `ai-architect-governor` — 跨域架构治理

- **源文件**：`skills/core/ai-architect-governor/SKILL.md`
- **成熟度**：verified
- **用途**：治理跨域架构决策，覆盖领域边界校验与执行、身份/租户/权限归属规则、主数据与业务真相归属映射、跨域链路定义、系统集成模式与架构决策记录（ADR）。它面向架构治理，不负责单模块实现。
- **触发条件**：任务改动架构、跨模块或跨平台、需要定义归属，或需要产出架构决策记录时（源 frontmatter description 明确列出）。该 Skill 的正文未单独给出 `## When to Use` 小节，触发条件取自 frontmatter。
- **核心规则**：**禁止凭想象设计架构（Do not design architecture from imagination）。** 任何架构结论之前必须：1）核实当前文档；2）核实当前代码现实；3）分离「当前已验证状态 → 目标结构 → 治理决策 → 实现任务」；4）区分真相源系统（source-of-truth system）、入口层、使能层、对象所有者与回写消费方。
- **关键流程/检查点**：
  1. 架构决策前检查：读 `docs/架构决策记录/` 是否已有相关决策。
  2. 核实代码中的实际领域归属，而不是只看文档。
  3. 核对数据库 Schema：表位置、外键、共享表。
  4. 复核既有 API 边界与版本策略。
  5. 明确哪个团队拥有哪个领域。
  6. 按 `## Architecture Decision Layers` 分层落地：Layer 1 领域边界（谁拥有身份概念、主数据对象、业务单据、平台表）；Layer 2 身份与访问（SSO 范围、租户隔离模型、权限模型、API 鉴权流程）；Layer 3 数据归属（权威源、回写路径、缓存/失效策略、事件溯源与最终一致性边界）；Layer 4 集成模式（同步 API vs 异步事件、shared-nothing/shared-kernel/shared-core、防腐层、API 版本与向后兼容）。
  7. 每个业务能力必须区分四类角色：Source of Truth（数据与规则的权威系统）、Entry Layer（面向用户或集成的界面）、Writeback Consumer（接收更新的下游系统）、Enablement Layer（共享基础设施）。
  8. 影响多个领域的决策必须落 ADR，模板含 Status（Proposed / Accepted / Deprecated / Superseded）、Context、Decision、Consequences、Alternatives Considered。
- **门禁与资格**：源文件未明确 `L0`–`L3` / `Q0`–`Q3` 门禁代号与资格等级；本 Skill 以「先核实文档与代码再下结论」作为前置门禁。
- **必交产出**：架构决策记录（ADR，模板见正文 `## Architecture Decision Record Template | ADR模板`）；领域归属与真相源/入口层/回写消费方/使能层角色划分表。源文件未明确其他强制产出路径。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. 禁止在未于真实代码中核实前就划定领域边界。
  2. 禁止仅凭命名假设归属 —— 必须在数据库与服务层核实。
  3. 禁止对影响多个领域的决策跳过 ADR 撰写。
  4. 禁止把入口层当作真相源。
  5. 禁止在未告知受影响领域所有者的情况下合并跨域改动。

---

## 3. `ai-atomic-architect` — AI 原生原子架构

- **源文件**：`skills/core/ai-atomic-architect/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 New）
- **用途**：定义并执行 AI 原生架构模式：`atomic service` + `atomic orchestration` + 统一接口（unified interfaces）。目标是让按此方法论构建的项目能从单一 Web 前端演进为多平台系统（Web、移动 App、小程序、MCP server、API），且不必重写业务逻辑；它解决的是业务逻辑与展示层紧耦合导致的重复实现问题。
- **触发条件**：定义服务拆分、后端真相归属、可复用业务命令、Host 客户端或 MCP/智能体能力面时（源 frontmatter description 明确列出）。正文未单列 `## When to Use` 小节。
- **核心规则**（原文 Rule 全文意译，保留强度）：**声明（DECLARATION）= 只有契约（CONTRACT ONLY）**：只允许 schema、meta、relations。**执行器（EXECUTOR）= 全部业务逻辑**：必须可测试、可替换。**治理（GOVERNANCE）= 每个执行器上的强制参数**。**禁止在 DeclarationAtom 上写 `run()`**。**每个 atom 都必须有独立的执行器文件**。
- **关键流程/检查点**：
  1. 三大支柱落地：原子服务（`atomic service`：最小可独立理解/测试/治理/替换的业务逻辑单元，只做一件事，有显式真相归属与数据边界，只通过定义好的接口通信，禁止直连数据库）；原子编排（`atomic orchestration`：用 Direct Call / Event-Driven / Saga(Choreography) / Workflow Engine / API Gateway 组合服务而不耦合，业务工作流是组合而非单体）；统一接口（同一原子服务经多传输协议暴露逻辑而不重复实现）。
  2. 交付主干（Delivery Spine）：domain facts → `atomic service` → `atomic orchestration`/application service → `aggregate interface` → `command gateway` → 传输适配器 → Web/App/AI/MCP/OpenAPI `Host`。
  3. `aggregate interface` 是面向客户端就绪的契约，可含 runtime/profile 事实、字段元数据与展示/编辑约束、权限与租户/版本/数据范围结果、当前状态与可用命令/阻断项、以及面向展示的读模型；禁止把持久化、计算、生命周期流转或授权下移到客户端。
  4. `command gateway` 是可复用业务写入的唯一可执行入口。派发前必须评估六项：1）已认证操作者与租户；2）权限、版本策略与数据范围；3）当前业务状态与上下游阻断；4）幂等与确认/风险要求；5）provider/handler 覆盖；6）审计轨迹与规范响应。仅因适配器或 `Host` 渲染出按钮并不等于动作可执行；不支持、已推迟或被阻断的动作必须保持显式不可执行并给出稳定原因。
  5. 能力执行成熟度链（Atoms、Skills、工具、AI 任务、插件、业务能力共用）：`registered` → `configured` → `authorized` → `provider-covered` → `runtime-executable` → `business-closed`，每级转换都要各自证据与稳定失败原因。
  6. `Host` 与适配器边界：两者只做协议、身份、输入输出转换与加载渲染/收集输入/请求命令/展示反馈；禁止组合领域服务、跑裸查询、计算业务事实或另造状态机。
  7. 领域模块分解：每个模块 = 一个原子服务；任何模块不得依赖超过 3 个其他模块。
  8. 接口先行：先写 OpenAPI/GraphQL schema，再写实现。
- **门禁与资格**：本 Skill 不使用 `L0`–`L3`/`Q0`–`Q3` 代号；它定义能力成熟度链 `registered`/`configured`/`authorized`/`provider-covered`/`runtime-executable`/`business-closed`。规则：低阶状态不得谎报为高阶状态；注册表或目录中存在只证明 `registered`，看得见的按钮什么后续状态都不证明；被推迟/阻断/不支持的动作必须显式不可执行并给出稳定原因；同一条链适用于 Web、App、AI、MCP、OpenAPI 与后台任务适配器，适配器不得提升能力成熟度。
- **必交产出**：接口定义文件（如 `api/task-service.openapi.yaml`，先于实现）；`aggregate interface` 与 `command gateway` 契约；ADR 或架构说明（与 `ai-architect-governor` 衔接）。源文件未明确其他强制路径。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. **禁止把业务逻辑放进展示层**（Vue 组件、Flutter widget）。
  2. **必须先定义接口再实现**（OpenAPI/GraphQL schema 先行）。
  3. **一个 `atomic service` = 一个显式数据边界**；schema-per-service 只有在独立部署与隔离足以抵偿运维成本时才是恰当的。
  4. **传输只是细节** —— 核心业务逻辑不知道调用方是 REST、MCP 还是 WebSocket。
  5. **Aggregate before Host** —— 客户端消费单一聚合契约，而不是自己去组合后端服务。
  6. **写入必须走 `command gateway`** —— 适配器与 `Host` 不得绕过授权、状态、幂等或审计检查。
  7. **先简单，需要时再拆** —— Archetype A 是合法选择，禁止过度设计。
  8. **每个 `atomic service` 必须在其他服务不运行时也能独立测试。**

---

## 4. `ai-chief-planner` — 端到端项目规划与收口

- **源文件**：`skills/core/ai-chief-planner/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 Effective）
- **用途**：在完整生命周期上编排项目任务：规划（范围定义、任务拆解、依赖映射）、调度（优先级排序、资源分配、里程碑）、跟踪（进度监控、阻断识别、状态汇报）、收口（验证、文档回写、证据收集）与研究（竞品基准、技术评估、市场分析）。它面向**项目级编排**，不负责单任务执行。
- **触发条件**：需要项目级协调、多步交付、待办台账（backlog）治理与最终收口规划时（源 frontmatter description 明确列出）。正文未单列触发小节。
- **核心规则**：每个计划必须：1）把目标拆成原子可验证步骤；2）按依赖排序；3）为每步定义清晰的完成判据；4）增量跟踪进度；5）在标记完成前做验证。**禁止跳过任何验证步骤。**
- **关键流程/检查点**（`## Planning Workflow`，五阶段）：
  1. Phase 1 Discovery：理解请求范围与约束、识别干系人与受影响领域、核查既有文档与历史决策、做初步环境自检。
  2. Phase 2 Task Decomposition：拆成可执行批次（委派 `ai-task-decomposer`）、标注批次间依赖、估算工作量与风险、分配优先级（`P0`/`P1`/`P2`）。
  3. Phase 3 Scheduling：按依赖与优先级排序、识别可并行工作流、设置里程碑与检查点、分配资源与时间盒。
  4. Phase 4 Execution Tracking：监控批次完成状态、识别并升级阻断、更新总控文档、据发现调整计划。
  5. Phase 5 Closure Verification：对每个批次跑验收标准、收集证据（API 响应、截图、日志）、把结论回写文档、把改进反馈给 `ai-skill-evolver`。
  6. 八条核心原则贯穿全程：先检查后执行、找根因而非打补丁、证据驱动、闭环（Plan → Execute → Verify → Document → Re-check）、禁止重复劳动、功能优先、单一真相源、边界意识。
  7. 任务状态模型：`backlog` → `planned` → `in_progress` → `review` → `verified` → `closed`，另有 `blocked`（因依赖或问题无法推进，需升级并解除阻断）。
  8. 收尾检查清单：验收标准全通过、证据已收集、文档已更新、工作区干净（只暂存当前任务文件）、模式浮现时已更新相关 Skill、作为依赖时已解除下一批次的阻断。
  9. 调度模式：Sequential（严格依赖顺序）/ Parallel（独立批次）/ Staggered（重叠但有同步点）/ Wave-based（按开发波次分组）。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 门禁代号；本 Skill 的门禁体现在任务状态模型与「未经验证的工作不算完成」。优先级使用 `P0`/`P1`/`P2`。
- **必交产出**：更新后的总控文档（master control）进度记录；每批次的验收证据（截图、API 日志、SQL 结果）；回写 `ai-skill-evolver` 的改进建议。源文件未明确固定的文件路径。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. 禁止在未核实当前状态前开始执行。
  2. 禁止跳过收口验证 —— 未经验证的工作不算「完成」。
  3. 禁止重复劳动 —— 先检查既有任务包。
  4. 禁止超出可用信息做计划 —— 拆成「发现 + 执行」两个阶段。
  5. 禁止无视阻断 —— 必须升级处理而不是绕过。

---

## 5. `ai-command-executor` — 标准化命令执行

- **源文件**：`skills/core/ai-command-executor/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 Effective）
- **用途**：把执行请求转成标准化、可审计的命令运行：选择已批准的入口（优先既有脚本）、执行前检查、脚本与命令执行记录、从日志与输出做根因诊断、给出最安全的下一步建议。它面向执行与诊断，不负责任务路由或项目调度。
- **触发条件**：任何 shell/CLI 工作、运行时调试或工具安装决策之前（源 frontmatter description 明确列出）。正文未单列触发小节。
- **核心规则**：**当项目已提供已批准的入口时，禁止自创新的命令流程。**执行优先级依次为：1）项目标准脚本（如 `scripts/bat/`、`scripts/ps1/`、`scripts/py/`）；2）项目内可复用辅助脚本；3）有明确理由的文档化单行命令；4）仅在给出显式理由并留记录时才用自定义 shell 命令。
- **关键流程/检查点**：
  1. 执行前协议三问：目标是什么确切结果？哪个既有脚本已覆盖？执行前必须满足哪些环境事实？
  2. 环境事实检查表：Git 可用性、Node.js 版本、Java 版本、端口占用、进程状态、磁盘空间（诊断命令见正文表格）。
  3. Phase 1 环境验证：确认工具依赖可用；**任一工具缺失即调用 `ai-tool-bootstrapper` 自动安装**；启服务前检查端口；确认工作目录与权限。
  4. Phase 2 脚本选择：先查 `scripts/` 目录；优先项目标准脚本；若无脚本则把命令沉淀为新的可复用脚本。
  5. Phase 3 执行：带合适参数运行、分别捕获 stdout 与 stderr、记录执行时间与退出码。
  6. Phase 4 诊断：匹配已知错误模式、查日志补充上下文、分类为环境问题/代码问题/配置问题。
  7. Phase 5 建议：成功则报告结果并建议验证步骤；失败则归类根因、给出修复方案与确切命令。
  8. 工作树闸门（Working Tree Gate）：新任务开始前与提交前核验工作区 —— 检查意外脏文件、只暂存当前任务文件、用 diff 复核暂存内容、把未跟踪文件分类为证据/临时/放错位置。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 代号；本 Skill 的前置门禁是「执行前检查 + 工作树闸门」，即未通过环境与工作区核验不得执行与提交。
- **必交产出**：命令执行记录（含执行时间、退出码、stdout/stderr 分离结果）；缺失时沉淀的新可复用脚本；失败时的根因分类与精确修复命令。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. 禁止在同一工作区并行跑构建（共享输出目录）。
  2. 禁止未查端口就假设服务没在运行。
  3. 禁止在可能有旧进程仍占用端口时只信健康端点。
  4. 禁止在上一步失败后跳过环境验证。
  5. 禁止在未获用户明确确认时使用破坏性（destructive）命令，如 `reset --hard`、`clean -fdx`。
  6. 针对无关脏文件，禁止做整仓库清理；只暂存当前任务文件并在提交前验证；必要时对无关改动显式 stash 并写明信息。

---

## 6. `ai-delivery-contract-governor` — 可执行交付契约治理

- **源文件**：`skills/core/ai-delivery-contract-governor/SKILL.md`
- **成熟度**：verified
- **用途**：把既有 5S 生命周期压缩成一个小的、机器可校验的任务边界：scope contract → approved write boundary → implementation → `fresh evidence` → independent two-axis review → safeguarded / completed。它补强 `ai-5s-delivery-governor`，但禁止取代项目的业务规则、CI、发布流程、权限系统或运行时唯一真相源。
- **触发条件**：L2/L3 交付、共享能力、schema、权限、发布或跨模块写入路径；并行或交接式工作中智能体需要互不重叠的写入边界；任务需要可强制执行的「未越界」证明；项目希望本地/CI 能拒绝过期证据、缺失评审或越界改动文件。L0/L1 工作可按需使用同一契约，但不得施加不降低真实风险的仪式负担。
- **核心规则**：**没有任何受治理任务可以因为智能体自称就绪而推进。**只有当其交付契约允许下一状态且所需证据齐备时才推进。**该契约失败即阻断（fail-closed）。**
- **关键流程/检查点**：
  1. 使用项目自有资产：Schema `docs/全项目总控/schemas/governance/delivery-contract.schema.json`、模板 `docs/_templates/全项目总控/task_contract.json`、校验器 `scripts/py/validate_delivery_contract.py`。
  2. 从模板创建任务本地契约，随任务包或项目自有交付记录存放；禁止放在通用临时目录。
  3. 写代码前必须记录七项：1）产品结果、验收步骤与非目标；2）变更类型、目标线/版本、受影响流程与 `L0`-`L3` 门禁；3）权威真相责任人；4）精确写入白名单、禁止路径与破坏性（destructive）分类；5）聚焦的公共可测试边界（test seam）或经论证的替代证据；6）必须在最后一次相关改动之后运行的最终证明命令/检查；7）分离的「标准/真相」与「产品/规格」评审。
  4. `review_required` 或 `explicit_owner_confirmation` 未记录所需决策前，禁止执行破坏性（destructive）工作。
  5. 校验工作流：实现前 `py scripts/py/validate_delivery_contract.py --contract <task-contract.json>`；集成前加 `--changed-file <repo-relative-path>` 校验观测/暂存路径；最终相关改动后追加证据记录并跑 `--check-freshness`。
  6. 必须运行项目真实测试、运行时检查、数据库回读与发布门禁 —— 校验器只检查契约纪律，不伪造领域证据。
  7. 状态机与最低进入门禁：`draft`（仅有初步想法，无实现）、`scoped`（结果/范围/真相责任人/证据计划齐备，Scope 校验器通过）、`approved`（所需负责人或破坏性决策已记录，已批准任务只在白名单内写入）、`implementing`（变更文件保持在白名单内）、`safeguarded`（最终证明是 `fresh evidence` 且两项评审通过，`--check-freshness` 校验通过）、`completed`（项目集成/发布条件也满足，即 5S 收口加已 safeguard 的契约）、`blocked` / `cancelled`（不得静默继续，必须在任务包记录阻断或取消原因）。
- **门禁与资格**：L2/L3 在进入 `safeguarded` 或 `completed` 之前，`verification_owner` 必须与 `implementer` 不同；独立验证人可用项目自有 CI、另一个智能体或评审者，但必须审阅真实证据而非仅看实施人的总结。契约状态名不译：`draft`/`scoped`/`approved`/`implementing`/`safeguarded`/`completed`/`blocked`/`cancelled`；失败即阻断（fail-closed）。
- **必交产出**：任务本地 `DeliveryContract`（源自 `task_contract.json`，用 delivery-contract schema 校验）；证据记录与 `--check-freshness` 校验结果；两轴（`two independent axes`）独立评审记录。
- **防护规则**（`## Guardrails`）：
  1. 禁止用 `**` 这类宽泛白名单掩盖无关工作。
  2. 禁止在实现之后为了通过校验而把越界文件塞进白名单；应重开 Scope/Specify 并记录原因。
  3. 禁止用早于最终相关改动的运行结果声称最终证据（即禁止 stale evidence 冒充 `fresh evidence`）。
  4. 禁止让通过的「标准/真相」评审豁免失败的产品验收，反向亦然。
  5. 禁止实施人在无独立验证人的情况下自我认证 L2/L3 的 safeguard。
  6. 禁止把这份 JSON 记录当作业务歧义、破坏性（destructive）工作或发布授权的负责人批准替代品。

---

## 7. `ai-foundation-governor` — 稳定基座与唯一真相治理

- **源文件**：`skills/core/ai-foundation-governor/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 Effective）
- **用途**：治理项目稳定基座层 —— 每个功能都依赖、但没有单个功能拥有的基础设施：版本控制与模块/插件管理、权限系统与 RBAC、菜单/路由与统一导航、API 标准化与统一登录/SSO、字段/元数据框架、系统与业务参数、数据库 Schema 治理（版本、迁移、种子）、运行时快照与编译后 profile、发布门禁与证据收集。对触及**任何**基座组件的任务，加载本 Skill 是强制的：基座一破，所有功能级联受损。
- **触发条件**：基座行为或共享项目基础设施发生变化时（源 frontmatter description 明确列出）；正文补充：任务触及任何基座层组件时本 Skill 为强制。
- **核心规则**：**每个能力只有一个唯一真相源。缺失的回路必须在页面打补丁之前补齐。**当根因位于基座（权限、Schema、参数、配置）时，禁止在表层（UI、API 端点）给功能打补丁。先分类，再修复。
- **关键流程/检查点**：
  1. 真相来源分类：修改任何基座组件前，先按表分类其权威来源（版本/模块/插件、功能开关、权限/RBAC、认证/SSO、字段定义、系统参数、业务参数、报表、数据库 Schema、运行时 profile、审计/证据）。
  2. **若任务无法分类，禁止写代码**；先查文档、数据库与既有代码。
  3. 现实检查（check-before-execute）：数据库（`SHOW TABLES`、`DESCRIBE`、`SELECT COUNT(*)`）、数据库治理归属（改动属于 `schema/`、`seed/`、`patch/` 还是 `templates/`）、代码（定位 service/controller/interceptor 消费方）、文档（总控与发布文档不得与新改动矛盾）、运行时（API 探测、浏览器检查、日志）。禁止仅凭命名约定推断。
  4. 后端真相规则：业务真相必须位于后端服务，不得位于前端入口层。验收检查：同一业务动作从任何入口层发起，必须产生完全一致的校验、持久化结果、回写行为与审计事实。
  5. 发布门禁：每次发布必须通过两道最低门禁 —— DB Gate（正式 schema 脚本位于正确目录、基线 schema 与预期一致、必需表/列/索引存在、关键种子行存在、系统与业务参数值正确）与 Core Flow Gate（目标租户可认证并加载 runtime profile、核心页面无错渲染、关键 API 正确响应、关键业务流程 CRUD 与报表可用、回写与审计轨迹完整）。
  6. 基座变更影响清单（合并前逐项核验）：权限、菜单/路由、API、字段、参数、Schema、迁移、报表、租户、发布文档十项。
- **门禁与资格**：本 Skill 使用 DB Gate 与 Core Flow Gate；**DB 门禁通过而核心流程门禁失败，仍然是发布阻断项**。数据库迁移一致性门禁（失败即阻断 fail-closed）：对任何 schema、种子、参数基线或租户数据迁移，把迁移清单与各环境执行登记表当作同一份发布契约，须核对清单身份（迁移 id、版本、源路径、依赖/顺序、校验和）、环境登记（测试/预发与生产登记同一预期迁移）、安全性（幂等、显式替换/取代关系或书面一次性前置条件）、执行历史（状态、时间戳、操作者/任务、提交/版本）、迁移后状态（schema、种子、参数、运行时 profile、租户范围检查通过）、恢复（可逆补丁、补偿迁移、备份或显式恢复决策）。当迁移只存在于源码、只在一个环境登记而另一个没有、缺校验和/历史、或无迁移后验证时，该门禁失败即阻断；部署任务成功不替代这些检查。源文件未使用 `L0`–`L3`/`Q0`–`Q3` 代号。
- **必交产出**：发布证据文档与审计证据（源文件要求「收集证据」，并禁止删除审计证据 —— 应分类并提交）；数据库迁移清单与环境执行登记记录；基座变更影响清单核验结果。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. 禁止在未核查全部消费方的情况下修改基座组件。
  2. 禁止为任何能力创建第二真相源。
  3. 禁止因为改动「很小」就跳过 DB 门禁。
  4. 禁止把「在我机器上能跑」当作通过核心流程门禁。
  5. 禁止删除审计证据 —— 必须分类并提交。

---

## 8. `ai-library-first` — 库优先开发治理

- **源文件**：`skills/core/ai-library-first/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 New）
- **用途**：强制一条规则：**在写第一行自研代码之前，先检查成熟开源库是否已经做了这件事。**它针对 AI 辅助开发中 token 浪费与代码不稳定的头号成因 —— 重新发明 npm/pip/maven 里已有的组件（自研日期选择器、表格组件、表单校验、图表、甚至状态管理），导致成千上万 token 被浪费并产出难以维护的代码。
- **触发条件**：任何新写逻辑、解析器、UI 组件、引擎、集成或脚本之前（源 frontmatter description 明确列出）。正文未单列触发小节。
- **核心规则**：创建任何新东西之前必须依次：1）搜索既有库/组件；2）检查既有物能否扩展；3）只有都不匹配时才新建；4）把新增登记进共享目录；5）记录复用决策。**禁止在没有明确理由的情况下重复造轮子。**最高指令：**永远不要从零写一个库已经实现的东西**（`Check → Choose → Install → Configure → Use` 约 10 token，对比从零重写 5000+ token）。
- **关键流程/检查点**：
  1. 决策流程：标准库是否存在？成熟吗？→ 直接使用；不成熟 → 找更好的替代；不存在 → 判断是否真novel → 是则自研，否则继续更努力地搜索（你多半漏了一个）。
  2. 标准库目录按栈给出「该用这个 / 永远别从零写」对照表：前端（Vue/React：日期选择、表格/DataGrid、表单校验、图表、图标、状态管理、拖拽、富文本、上传、Toast/通知、模态框、HTTP 客户端、路由、i18n、虚拟滚动）、后端 Java/Spring Boot（ORM、校验、缓存、限流、日志、JSON、Excel、API 文档、任务调度、安全、代码生成、短信/邮件）、后端 Node.js/Express（Web 框架、ORM、校验、认证、上传、队列、实时、日志、测试、限流）。
  3. Token 成本分析：自研数据表格约 8000 token 对比库约 200 token（省约 97.5%），富文本约 15000 对比约 300（约 98%），平均省约 96%，且库版本更稳定并有文档。
  4. 审计：对任何 PR 或已完成任务跑四步检查 —— 列出自研工具函数/模块；逐个判断标准库是否已存在；存在则**拒绝：替换为库**；不存在则记录为何必须自研。
  5. 与 `ai-chief-planner`（Phase 1 库目录核查）、`ai-task-decomposer`（每批次列出所需库）、`ai-tool-bootstrapper`（自动安装声明的库依赖）、`ai-skill-evolver`（把新发现的库加入目录）集成。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 代号；本 Skill 的门禁是「写码前必须先查库目录」这一前置条件。
- **必交产出**：复用决策记录；声称「真正novel」时必须列出检查过的 3 个库及各自被否决的理由；共享库目录的更新条目。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. **写任何代码之前**检查库目录 —— 不是之后。
  2. **优先项目既有的库** —— 项目已用 Element Plus，就不要为一个组件再装 Ant Design。
  3. **库版本必须锁定** —— 生产环境禁止 `^` 或 `~`，使用精确版本。
  4. **一个问题域只用一个库** —— 禁止在一个项目里用 3 个不同的日期库。
  5. **禁止包装式库** —— 禁止把 axios 再包一层毫无增益的「自研 HTTP 客户端」。
  6. 允许自研的仅三种情形：真正全新（罕见且必须彻底核实）、许可证不兼容（如专有软件中的 GPL）、性能差距 10 倍以上（必须做基准测试）。

---

## 9. `ai-multi-agent-orchestration` — 多智能体编排

- **源文件**：`skills/core/ai-multi-agent-orchestration/SKILL.md`
- **成熟度**：verified
- **用途**：单智能体分解（`ai-task-decomposer`）把一个任务拆成有序批次；多智能体编排则把一个**项目**拆成可并行推进的领域而不产生合并混乱。它补齐方法论中「多 Agent 编排」这一缺失层：通过钉住领域边界、依赖方向与契约优先集成，让并行 AI 工作变得确定。
- **触发条件**（`## Trigger | 触发条件`）：任务跨多个模块/领域，或计划把工作扇出给多个智能体时使用；在启动并行智能体或判断两个任务能否并发之前使用；用于易产生合并冲突的工作、跨域集成或跨智能体的大批量规划。
- **核心规则**（原文 Rule 五条，逐条意译）：
  1. 按领域归属而非文件类型划分：每个智能体拥有一个有界领域和单一真相责任人。
  2. 契约先行：任何跨域集成点必须在并行工作开始前定义为读/写契约。
  3. 仅当不存在共享表写入时才并行；只读依赖可以并行。
  4. 当一个领域写入另一个领域下游要读的数据，或 API 契约尚未定义时，必须串行。
  5. 每个智能体都得到显式验收边界与非目标清单；禁止任何智能体静默跨领域扩大范围。
- **关键流程/检查点**（`## Workflow`，6 步）：
  1. 按归属与真相责任人划分领域，记录领域清单与各自所有者。
  2. 画依赖图：哪个领域读哪个领域的数据。
  3. 用并行/串行矩阵逐对分类：无数据依赖 → 并行（独立真相）；经 API 的只读依赖 → 并行（无写冲突）；共享表写入 → 串行（数据竞争/锁冲突）；下游读上游写 → 串行（上游必须先提交）；契约未定义 → 串行（先定义契约）。
  4. 契约先行：为每个跨域边界定义请求/响应形状、字段真相、错误码与幂等键。
  5. 分配智能体时同时下发：领域范围、读/写白名单、验收标准、非目标与契约文档。
  6. 在契约边界上串行集成；宣布完成前跑回归与跨域收口审计。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 门禁代号；本 Skill 的门禁是「并行/串行矩阵裁决 + 契约先行 + 跨域收口审计」。
- **必交产出**：领域清单与所有者；依赖图；每个跨域边界的读写契约文档；每个智能体的范围/读写白名单/验收标准/非目标；跨域收口审计结果。
- **防护规则**（`## Guardrails`）：
  1. 禁止两个智能体并发写同一张表或同一真相源。
  2. 禁止在集成契约写完之前启动并行工作。
  3. 禁止在缺少该领域自身通过证据与跨域契约检查的情况下合并其产出。
  4. 禁止把「两个智能体都做完了」当成集成完成 —— 必须端到端验证契约成立。

---

## 10. `ai-product-directed-delivery` — 产品主导的全 AI 交付

- **源文件**：`skills/core/ai-product-directed-delivery/SKILL.md`
- **成熟度**：verified
- **用途**：让不写代码的 `product owner` 也能主导产品交付，同时保持工程严谨：产品意图与验收 → AI 分析与基准 → 架构与真相边界 → 实现与验证 → `product owner` 业务验收 → 受治理发布。它不是「提示词生成页面」，而是一个受控运营模型：人的判断留在产品决策，智能体执行可验证的工程系统。
- **触发条件**：产品主导的企业级交付、非程序员主导的开发、端到端功能工作，或需要解释人与智能体职责边界时（源 frontmatter description 明确列出）。
- **核心规则**：`product owner` 决定业务结果、可用性、范围与最终验收；AI 智能体拥有工程执行路径，并必须用代码、运行时、数据与发布证据证明它。**禁止强迫 `product owner` 写代码，也禁止 AI 智能体代替负责人发明产品意图、业务政策或验收。**
- **关键流程/检查点**：
  1. 职责边界表：`product owner` 拥有业务目标、目标用户、流程结果、产品呈现、可用性判断、优先级、非目标与最终验收；工程师都不拥有。其余角色分工为 AI 产品分析员（需求澄清、场景图、验收草稿、业务歧义日志）、AI 研究员（竞品/参考证据与选项）、AI 架构师（真相归属、领域边界、atom/编排/聚合设计、迁移风险）、AI 交付智能体（数据库、后端、前端、测试、脚本、文档、精确暂存）、AI 验证/审计者（独立运行时、API、DB、回写、浏览器与发布检查）、验收时的 `product owner`（确认流程可理解、高效且对真实工作正确）。
  2. 产品到工程契约：实现前先写最小可用契约（Business outcome、Primary user and scenario、Expected visible result、Usability constraints、Business-flow acceptance、Non-goals、Known examples or references），AI 团队再补（Truth owner、Affected domain and clients、Change type and delivery gate、Technical acceptance、Data/writeback/report impact、Risk and rollback notes）。业务结果不清就问；工程路径不清由 AI 自己查，禁止把包袱变成 `product owner` 的编程任务。
  3. `shared language` 与决策上下文：引入或依赖含糊业务术语、稳定缩写、跨会话决策时，在 `docs/` 下维护简洁的项目自有上下文（术语/上下文记录、ADR 或决策记录），并在规格、测试名、API 与代码中复用同一套约定语言；该要求与风险成比例，一行本地修复不要求术语表，且术语表不得成为第二业务真相源。
  4. 十二步产品交付地图（每步含 `product owner` 贡献、AI 职责与退出证据）：1 Outcome；2 Process；3 Benchmark；4 Architecture；5 Data；6 Atomic backend；7 Orchestration；8 Aggregate and command；9 Frontend composition；10 Integration；11 Acceptance；12 Delivery。步骤按依赖而非文书推进：小的本地可用性改动可走短路径；数据、权限、跨客户端命令与发布必须走完整链路。
  5. 后端交付链：Database and domain facts → `atomic service` → `atomic orchestration`/application service → `aggregate interface` → `command gateway` → Web/App/AI/MCP/OpenAPI 适配器 → `Host` 页面或客户端面。**禁止因为按钮存在就暴露命令**：只有当后端 `command gateway` 证明其契约与前置条件后，命令才可执行。
  6. 前端交付链：后端 runtime/FieldPackage/aggregate profile → `ui atom` → UI orchestration → 标准页面模板 → `host page` → 用户交互与反馈。`ui atom` 是聚焦可复用的视觉或交互能力（字段渲染器、选择器、行表格、状态标签、动作条、过滤器、结果汇总、阻断对话框）；`host page` 选择模板并组合受支持的 `ui atom`，禁止定义替代状态机、重复字段真相、计算业务值、决定权限或实现第二命令路径。前端可为即时可用性反馈校验必填输入，但业务校验与每一次写入决策仍然后端权威。
  7. 必要交接件（Required Handoffs）：Owner→AI、Analyst→architect、Architect→delivery、Delivery→verifier、Verifier→owner、Owner→release 六种，各自有必需内容。
  8. 可测试边界与 `fresh evidence`：对新增或变更的领域规则、缺陷回归、命令/编排行为及其他可测试公共接口，先命名公共边界与预期行为 → 写一个对预期行为失败的聚焦测试 → 实现最小通过改动 → 在最终相关改动后重跑聚焦测试与受影响回归。仅复制、生成、纯配置或探索性任务不强行红绿，改记录经论证的替代证据。在完成、提交、发布或就绪声明之前，必须在**最后一次相关改动之后**运行证明该声明的命令、运行时检查、API 调用、数据库回读或 diff 检查；更早的通过输出、健康端点或智能体报告都不足以作为证据。
  9. 标准工作流（11 步）：从产品结果而非实现措辞出发 → 转成短场景与业务验收契约 → 只在会改变真实产品决策时做基准 → 设计页面前声明后端真相归属 → 复用或构建后端 atom → 编排 → 聚合 → `command gateway` 链 → 构建前端 runtime → `ui atom` → 组合 → 模板 → `Host` 链 → 独立验证技术收口 → 由 `product owner` 以目标用户视角跑 `business-flow acceptance` → 用 `ai-5s-delivery-governor` 定最终交付状态与发布证据 → 按 `two independent axes` 评审（标准/真相/架构合规；原始产品结果、验收流程与非目标）→ 把反复出现的经验回灌到既有归属 Skill，而不是另建平行规则集。
  10. 安全修改协议（read, prove, then change）：变更边界记录（Requested business result、Suspected truth owner and execution path、Candidate files and why each is relevant、Expected impact boundary、Existing unrelated working-tree changes、Selected verification and rollback evidence）；破坏性（destructive）四级分类 A 可弃置 / B 任务自有源码 / C 共享或归属不明源码（默认保留，需明确负责人决策）/ D 持久化或破坏性（数据库行、schema、生产配置、租户数据、发布物、`git reset --hard`、`git clean -fdx`，未获明确确认与书面备份/范围/恢复路径前禁止执行）；改动前证明 impact（引用与导入、路由/菜单/运行时入口、测试与构建/迁移/发布脚本、工作区与暂存改动、回滚手段）；补丁级控制（改最小文件集、每批复核 diff、脏工作区只暂存 `exact task-owned` 文件或块并做 staged diff 检查、禁止整仓库清理、禁止未确认的 `reset --hard`/`clean -fdx`）。
  11. 精准代码定位协议（`code location`）：追踪顺序为 业务症状或请求结果 → 菜单/路由/权限入口 → 实际渲染的 `Host` 页面 → 标准模板与共享 UI 组件 → 前端服务/API 封装 → controller 或传输适配器 → `command gateway`/`aggregate interface` → 编排/`atomic service` → 领域事实、FieldPackage/BusinessProfile/权限 → mapper/数据库/迁移历史 → 聚焦测试、运行时门禁、发布门禁。编辑前必须产出定位报告（疑似业务流、已找到的证据、确切候选文件、选定的修复归属、预期受影响面、验证路径）。
  12. 重大项目自动驾驶（Major Project Autopilot）循环：Frame → Map → Batch（经 `ai-5s-delivery-governor` 分配 `L0`-`L3` 门禁）→ Execute → Prove → Present → Release or iterate。AI 只在真实业务歧义、不可逆/破坏性决策、重大范围取舍或最终发布授权时停下来问 `product owner`；工程不确定性是智能体的调查责任。
- **门禁与资格**：使用 `L0`-`L3` 门禁（由 `ai-5s-delivery-governor` 分配）；「技术门禁通过」不替代 `product owner` 完成的 `business-flow acceptance`。本 Skill 不定义独立的 `Q0`–`Q3` 资格表。
- **必交产出**：产品到工程契约（业务结果 + 工程补充字段）；十二步地图各步的退出证据；必要交接件（handoff）；`business-flow acceptance` 记录；`two independent axes` 评审结果；精简产品语言版的代码定位报告。
- **防护规则**（`## Guardrails`）：
  1. 禁止把 `product owner` 降格为写工单的人 —— 产品呈现与可用性是一等验收输入。
  2. 禁止要求 `product owner` 调试、写代码、选 ORM 映射或手工连接架构层。
  3. 禁止在证明受影响归属与引用边界之前编辑、删除、重命名、迁移或批量替换。
  4. 禁止让 `product owner` 去找代码文件 —— 必须追踪路由到真相的链路并汇报证据。
  5. 禁止让重大项目退化成无跟踪的提示词洪流 —— 必须维持批次、门禁、证据与决策点。
  6. 禁止把截图、原型或竞品参考当作完整业务语义。
  7. 禁止把业务状态、计算、授权或命令策略放进前端 `ui atom`、编排、模板或 `Host`。
  8. 禁止让 `aggregate interface` 或 `Host` 绕过 `command gateway` 写入。
  9. 禁止用静态评审声称负责人已验收 —— 必须执行业务流测试。
  10. 禁止让通过的技术门禁覆盖失败的产品可用性或流程验收。

---

## 11. `ai-project-classifier` — 项目分类器

- **源文件**：`skills/core/ai-project-classifier/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 New）
- **用途**：在项目起步时按四个关键维度分类。这决定加载哪些 Skill、用什么架构、遵循哪些步骤，以及「完成」的定义。它解决的问题是：没有显式分类时，方法论会把同一套规则套在 1 天的原型和 6 个月的企业系统上，导致小项目过度工程化、大项目工程不足。
- **触发条件**（`## Trigger | 触发条件`）：**永远**在项目上启动任何其他 Skill 之前运行；用户说「新项目」「开始构建」「创建应用」时；首次遇到既有项目时；项目范围发生重大变化时。
- **核心规则**：分类必须确定：1）主领域（代码/文档/DevOps/安全/数据/治理）；2）复杂度层级（简单/中等/复杂）；3）风险等级（低/中/高/危急）；4）所需 Skill；5）执行策略。**禁止未经分类就开始执行。**
- **关键流程/检查点**：
  1. Dimension 1 项目来源：老项目（brownfield，有 `package.json`、`.git`、数据库、既有结构）→ 先读后写、提炼既有模式而非强加新约定、增量升级方法论层、**禁止破坏既有功能**；新项目（greenfield，空目录）→ 先按维度 2–4 分类，再按分类搭脚手架，从 Step 1 起走完整方法论。
  2. Dimension 2 质量目标：Rapid Prototype（MVP/演示/概念验证，< 1 周，1–2 人；单体仓库可接受、最小测试、UI 先行；只加载 core 类 Skill；走精简 13 步、跳过深度架构与 ADR；Archetype A）；AI-Native（真实产品、用户会依赖、> 1 月、2–5 人；第一天就有原子服务边界、完整测试覆盖、接口先行、全量方法论文档、多平台就绪；加载全部 core + governance；走完整 13 步含全部门禁；Archetype B）；Enterprise（多租户、合规、SLA、5+ 人团队；完整原子服务架构与事件驱动编排、多区域部署、安全审计与渗透测试、HA/DR、完整 CI/CD 与部署门禁；加载全部 Skill；完整 13 步 + 部署门禁 + 安全扫描；Archetype C）。
  3. Dimension 3 部署目标：Web only / Web + Mobile / Web + WeChat / Web + MCP Server / All platforms 各自影响接口策略。规则：**永远按 Web + 1 个额外目标设计** —— 前期多花 10%，后期省下 90% 重写成本。
  4. Dimension 4 规模：Monolith/Modular Monolith（< 10K 用户、< 50 接口、单团队；任一模块核心逻辑超过 500 行再拆）；Microservices（> 10K 用户、> 50 接口、多团队；要求投入监控、服务网格、分布式追踪）。判定规则：团队 1 人且接口 < 20 → Monolith；团队 ≥ 3 人或接口 ≥ 50 → Atomic Services；团队 ≥ 5 且需要合规 → Enterprise Microservices。
  5. 分类输出：每次项目启动必须产出分类摘要表（Origin / Quality / Deploy Targets / Scale + Rationale）与 Implications（架构、Skill、步骤、DB、API、移动端）。
  6. 集成点：`ai-chief-planner` Phase 1 在任何规划前运行分类器；`ai-rule-dispatcher` 用分类选 Skill 集；`ai-architect-governor` 用分类选 archetype；`ai-atomic-architect` 按质量目标与规模落地。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 代号；本 Skill 的门禁是 Step 0 的「分类已记录」这一前置门禁，未分类不得进入执行。
- **必交产出**：Project Classification 摘要（四维取值 + 理由 + Implications）。源文件未明确固定文件路径。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. **先分类再写码** —— 禁止在没有分类的情况下开始实现。
  2. **老项目不等于随便改** —— 既有代码有约定，必须遵守。
  3. **快速原型不等于垃圾** —— 快速意味着更简单，不是更差。
  4. **默认 AI-Native** —— 不确定时选 AI-Native（降级比升级容易）。
  5. **范围变化就重新分类** —— 从原型变成产品需要重新分类。

---

## 12. `ai-rule-dispatcher` — 规则与任务路由

- **源文件**：`skills/core/ai-rule-dispatcher/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 effective）
- **用途**：在任何智能体执行任务之前回答五个问题：1）任务属于哪条项目线（mainline、governance、audit、research、release）？2）必须先加载哪些规则与文档？3）哪个 Skill 应当主导执行？4）写任何代码前必须做哪些事实检查（DB、代码、运行时）？5）安全执行顺序是什么？它面向**路由与首入判断**，不做分解或实现。
- **触发条件**（`## When to Use | 触发条件`）：用户请求含糊或跨多个领域；任务同时涉及前端与后端；不确定该由哪个 Skill 处理；新会话的首次交互；用户问「我该从哪儿开始」。
- **核心规则**：**当任务线、治理文档或主导 Skill 仍不清晰时，禁止把任务直接送进执行。**先把任务路由到正确上下文，再让其他 Skill 接手。
- **关键流程/检查点**（`## Standard Workflow`，5 步）：
  1. Step 1 判断任务线：mainline（活跃开发：功能、缺陷修复、重构）、governance（架构/质量治理）、audit（质量检查：代码评审、流程收口审计、前端审计）、research（调研分析：竞品、技术评估）、release（部署与发布：CI/CD、部署脚本、发布说明）。
  2. Step 2 判断任务类型并选定唯一主导 Skill：复杂/多模块 → `ai-task-decomposer`；架构/设计 → `ai-architect-governor`；项目规划 → `ai-chief-planner`；命令执行 → `ai-command-executor`；前端开发 → `{stack}-frontend-dev`（如 vue）；后端开发 → `{stack}-backend-dev`（如 java-springboot）；数据库变更 → mysql-best-practices（或等价）；质量审计 → `ai-flow-closure-audit` 或 `ai-frontend-audit`；研究 → `ai-competitor-analyst` 或 `ai-market-researcher`；Skill 改进 → `ai-skill-evolver`。
  3. Step 3 选择首要文档：`rules/AGENTS.md`（永远第一）→ `rules/project_rules.md`（若存在）→ 相关 Skill 的 `SKILL.md` → 相关 `docs/` 类目文档。
  4. Step 4 定义前置事实检查：数据库（`SHOW TABLES`、`DESCRIBE`、`SELECT COUNT(*)`）、代码存在性（路径检查、grep 模式）、运行时状态（端口、进程列表、健康端点）、配置（配置文件与环境变量）、文档（既有文档是否已覆盖）。
  5. Step 5 输出路由结果：Task Line、Lead Skill、Support Skills、First Documents to Read、First Checks to Run、Recommended Execution Order、Boundary Warnings。
  6. 任务中强制重读（`## Mid-Task Re-Enforcement`）以对抗上下文衰减：后端切前端时重读 `ai-single-truth-enforcer`、`ai-library-first`、`ai-component-standardizer`；同领域 50+ 条消息后重读该领域治理 Skill；向新文件写码前重读领域治理 Skill；标记任何任务「完成」前重读 `ai-runtime-verify`、`ai-single-truth-enforcer`；工具报错或结果异常后重读 `ai-tool-bootstrapper` 与相关技术 Skill。触发时输出上下文衰减警告（`⚠️ Context Decay Warning`）。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 门禁代号；本 Skill 的门禁是「路由结果产出前不得进入实现」以及上下文衰减重读触发点。
- **必交产出**：`## Task Routing Result` 路由结果块（任务线、主导与支撑 Skill、首要文档清单、前置检查清单、建议执行顺序、边界警告）。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. 禁止跳过先检查后执行。
  2. 禁止推荐多个主导 Skill —— 只能选一个。
  3. 入口事实仍缺失时，禁止路由到实现。
  4. 禁止把治理支撑线当成活跃主线。
  5. 不确定时升级给 `ai-chief-planner` 做调度决策。

---

## 13. `ai-skill-evolver` — Skill 进化引擎

- **源文件**：`skills/core/ai-skill-evolver/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 effective）
- **用途**：把重复劳动转化为更强的可复用资产：Skill 更新（改进既有 `SKILL.md`）、新 Skill 候选（模式重复时新建）、归档更新（记录进化记录）、项目 Skill 文档、进化日志。它面向**能力进化**，不做普通任务执行。
- **触发条件**（`## When to Use | 触发条件`）：完成一批相关任务之后；某一模式在不同模块重复出现 3 次以上；用户问「改进 Skill」「缺哪些 Skill」「为什么这个 Skill 没起作用」；项目结构发生重大变化之后；定期方法论健康检查期间。
- **核心规则**：**禁止凭模糊印象进化 Skill，只能从具体证据进化。**证据来源：跨模块重复出现的任务模式、重复的错误或缺上下文时刻、应当固化的稳定输出模板、项目路径/规则变更、用户反馈某 Skill 实际无效。必须始终区分：declared skill（磁盘上存在）、callable skill（可按名调用）、effective skill（稳定产出正确结果）、evolving skill（正在被主动改进）。
- **关键流程/检查点**：
  1. 持续修复-技能循环（每轮实现之后）：先完成具体代码/文档任务 → 判断该任务是否暴露了可复用规则、重复缺陷或缺失模式 → 分类（属既有 Skill 还是需要新 Skill）→ 更新相关 `SKILL.md`（扩展而非替换）→ 在 Skill 归档中记录进化 → 必要时同步到在用 AI 工具。
  2. Step 1 收集证据：读取全部既有 `SKILL.md`、近期任务日志与执行记录、已完成任务的用户反馈、文档回写。
  3. Step 2 分类差距：既有 Skill 需细化 → 更新 `SKILL.md`；新模式跨越 2 个以上任务类型 → 新建 Skill；单页面问题 → 记入任务文档而非 Skill；规则需更新 → 更新 `rules/AGENTS.md`；Skill 存在但无效 → 调查并修根因。
  4. Step 3 选择正确动作：更新 `SKILL.md`、更新参考文件、增改项目专属文档、更新 Skill 归档表、创建治理任务。
  5. Step 4 记录进化：必须记录触发原因、当前成熟度阶段、更新内容（文件路径 + 行范围）、仍缺什么、以及改动的是真实 Skill 资产还是仅文档。
  6. Step 5 反馈下一轮：转化为新任务 ID、可复用模板更新、更清晰的路由规则、下一批 Skill 待办。
  7. 成熟度评级制：declared（`SKILL.md` 存在但从未使用）→ callable（可按名调用，基础指令可用）→ effective（稳定产出正确结果）→ in-closure（有验收标准与证据规则）→ evolving（正基于反馈主动改进）。
  8. 定期治理触发：每约 20 个完成任务跑完整 `ai-skill-governor` 审计；每周（不论任务量）做轻量审计（矛盾 + 孤儿）；每月做全量审计（全部 5 个维度）；新增 3 个以上 Skill 后做矛盾扫描；方法论文档更新后校验 Skill 对齐。自动触发条件：2 个以上 Skill 的 Purpose 行重叠、某 Skill 超过 3 个月未更新、某 Skill 在最近 50 个任务中加载 0 次。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 门禁代号；本 Skill 的门禁是「具体重复证据（至少 3 次）」。它自身使用 Skill 成熟度分级 declared/callable/effective/in-closure/evolving。
- **必交产出**：更新后的 `SKILL.md`；Skill 归档（archive）进化记录；进化日志（记录改了什么、为什么）；新任务 ID 与下一批 Skill 待办。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. 当更新模板或既有 Skill 就足够时，禁止新建 Skill。
  2. 禁止在没有具体重复证据（至少 3 次出现）的情况下进化 Skill。
  3. 禁止忘记同时更新 Skill 文件**与**归档。
  4. 若未更新任何正式资产，禁止声称某 Skill 已进化。
  5. 禁止止步于「指出差距」—— 必须转化为具体更新或任务。

---

## 14. `ai-skill-governor` — Skill 体系健康治理

- **源文件**：`skills/core/ai-skill-governor/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 New）
- **用途**：主动审计、去重与维护 Skill 体系。与对已完成任务作出反应的 `ai-skill-evolver` 不同，本 Skill 对整个 Skill 库做**定期健康检查**，检测腐蚀、矛盾、冗余与有效性缺口。它解决的问题是：49 个正式 Skill（还在增长）需要持续质量控制 —— 它们可能互相矛盾、重叠、腐蚀、变成从未被触发的孤儿，或失去有效性。
- **触发条件**（`## Trigger | 触发条件`）：定期 —— 每完成约 20 个任务或每周（以先到者为准）；按需 —— 用户问「审计 Skill」「检查 Skill 质量」「这些 Skill 还好用吗」；自动 —— 新增 Skill 时检查与既有 Skill 的冲突；重大方法论更新后 —— 校验 Skill 仍与文档对齐。
- **核心规则**：每个 Skill 必须：1）有合法 frontmatter（`name`、`description`）；2）符合命名约定；3）已登记在 `SKILL_MANIFEST.json`；4）有清晰的生命周期状态；5）通过结构校验。**禁止激活未经校验的 Skill。**
- **关键流程/检查点**（`## Audit Dimensions`，5 个维度）：
  1. Dimension 1 矛盾检测：抽取每个 Skill 的 Guardrails/Rules，按主题域分组，标出相互冲突的配对。矛盾必须被调和（例如「前端校验仅用于 UX 反馈，后端重新校验一切，前端校验是装饰性而非权威」）。
  2. Dimension 2 重叠检测：比较 Purpose | 用途 小节的关键词重叠，超过 60% 即标记评审，决策为合并、拆分或厘清边界。
  3. Dimension 3 腐蚀检测（rot）：检查每个 `SKILL.md` 最后修改日期，标记超过 3 个月未更新者，并逐项核实库版本是否仍当前、模式是否仍是最佳实践、防护规则是否仍可执行。
  4. Dimension 4 有效性评分：Score = (times_triggered × 0.3) + (problems_prevented × 0.5) + (user_satisfaction × 0.2)。分值解读：8–10 Effective（保留，仅小改）；5–7 Needs improvement（复核防护规则、加固弱项）；2–4 Weak（大改或拆成多个聚焦 Skill）；0–1 Ineffective（归档或彻底重写）。
  5. Dimension 5 孤儿检测：跟踪 `ai-rule-dispatcher` 路由到哪些 Skill，最近 50 个任务未被路由到的即标记，并判断是「确实不需要」还是「dispatcher 不知道它」。
  6. 审计输出模板：Health Summary（正式 Skill 总数、矛盾数、重叠数、腐蚀数、孤儿数、平均有效性分）、Contradictions 表、Overlaps 表、Rotting Skills 表、Effectiveness Ratings 表、Recommendations。
  7. 治理周期：每周轻量审计（约 10 分钟：新矛盾快速扫描 + 孤儿检测）；每月全量审计（约 30 分钟：全部 5 维度 + 有效性重评 + 含库版本检查的腐蚀检测）；重大更新后触发（方法论文档变更后校验对齐；新增 3 个以上 Skill 后做矛盾扫描）。
  8. 自动修复规则：失效的 Skill 名引用直接更新（如 `ai-frontend-availability-audit` → `ai-frontend-audit`）；缺 `Evolution History` 小节则补模板小节；`SKILL.md` 超过 500 行则标记待拆（不自动拆）；两个 Skill 的 Purpose 行完全相同则标记待合并评审。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 门禁代号；本 Skill 的门禁是 5 项结构校验，未通过校验的 Skill 不得激活。成熟度沿用 `SKILL_MANIFEST.json` 的 raw/generalized/callable/verified/deprecated。
- **必交产出**：Skill Governance Audit 审计报告（含 Health Summary 与五个维度表格）；更新后的有效性分（供 `ai-rule-dispatcher` 路由使用）；方法论改进计划输入。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. **按周期审计，而不是只按需审计** —— 腐蚀是静默发生的。
  2. **矛盾就是缺陷** —— 两个 Skill 说相反的话是系统级缺陷。
  3. **有效性由结果衡量，不由意愿衡量** —— 「本该有用」但没能阻止问题的 Skill 就是无效。
  4. **孤儿 Skill 就是浪费** —— 没人用的就归档。
  5. **禁止自动合并 Skill** —— 重叠检测只标记给人工评审，永不自动合并。

---

## 15. `ai-task-decomposer` — 复杂任务分解

- **源文件**：`skills/core/ai-task-decomposer/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 effective）
- **用途**：把宽泛或混杂的工作转化为：范围冻结、可独立执行的任务批次；current / target / implementation 三层分离；带阻断识别的依赖感知排序；每批次的验收标准与证据规则；内部包与外部派发包的输出决策。它面向**分解**，不做顶层路由，也不亲自执行。
- **触发条件**（`## When to Use | 触发条件`）：跨模块或跨端（前端 + 后端 + DB）任务；单次安全的 AI 会话装不下的任务；被不清晰的依赖顺序阻断；准备并行对话或分阶段派发；用户说「拆一下这个」「把这个任务分开」「规划这项工作」。
- **核心规则**：**禁止凭想象拆分。**分解之前必须核实足够的仓库事实，以分离三层：1）当前状态事实（现在有什么）；2）目标状态决策（我们想要什么）；3）可执行实现工作（怎么到达）。
- **关键流程/检查点**：
  1. 前置检查（Check-Before-Execute）：当前分支与工作区（working-tree）状态；既有任务包与执行记录；同一主题是否已有分解包；热点文件或协作边界；哪些属于事实检查、设计、实现或验收。
  2. 1. 冻结范围：明确 In scope（确切模块、文件、领域）、Out of scope（显式排除区）、Impacted areas（受影响的模块/文件/领域）。
  3. 2. 复用已有产物：优先扩展既有分解包，而不是另建平行的。
  4. 3. 分层分离：始终区分 Current-State Verification（开始前要检查什么）、Target Design / Decision（构建前要决策什么）、Implementation Work（实际代码/文档改动）、Verification & Backfill（如何证明做对了）。
  5. 4. 构建可执行批次：每批次必须可被不同智能体独立理解；小到能在一轮专注工作内完成（约 30–60 分钟）；明确归属与写入范围；明确验收与证据；当领域行为或缺陷回归可测时，明确其公共可测试边界；当适用 L2/L3、并行或高风险工作时，明确其任务本地 `DeliveryContract` 路径与写入白名单。
  6. 5. 标记依赖（阻断优先排序）：Type A 必须先于 B 完成；Type B 可与 C 并行；Type C 应等待 A 与 B 完成。
  7. 6. 选择输出形式：Internal Decomposition Pack（单人、顺序执行）/ External Dispatch Pack（多人或多智能体、并行执行）/ Handoff Block（交接给另一个 AI 会话）。
  8. 必需输出结构：Scope & Verified Inputs、Main Blockers & Current Facts、Current / Target / Implementation Split 表、Task Batch Table（ID、Priority、Batch、Dependency、Est. Time、Acceptance）、Acceptance & Evidence Rules（含可测试边界与红绿证据、`fresh evidence`、`two independent axes` 评审、`DeliveryContract` 路径与校验结果）、Output Form。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 代号；批次优先级使用 `P0`/`P1`。证据规则要求点名可测试边界与红绿证据、最终 `fresh evidence`、`two independent axes` 评审结果，以及 `DeliveryContract` 是否必需。
- **必交产出**：Task Decomposition 文档（六段结构）；任务批次表；验收与证据规则；内部包/派发包/交接块。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. 当工作并不原子时，禁止输出一个巨型任务。
  2. 禁止拆得过细以致业务含义消失。
  3. 除非紧密耦合，禁止把当前状态检查与实现混在一起。
  4. 禁止在并行工作中忽视热点文件碰撞风险。
  5. 禁止不先检查既有分解包就开始分解。

---

## 16. `ai-tool-bootstrapper` — 工具自举与环境自愈

- **源文件**：`skills/core/ai-tool-bootstrapper/SKILL.md`
- **成熟度**：verified（正文 `## Maturity` 自述 Stage 为 New）
- **用途**：自动检测、获取、安装并验证缺失的开发工具，让方法论具备**自愈自身环境**的能力：工具缺失时不失败，而是找到、下载、安装并验证。它解决的是 AI 常因「tool not found」失败、或需要手工 `npm install` / `pip install` / `apt-get install` 而中断自主流程的问题。
- **触发条件**（`## Trigger | 触发条件`）：任何 Skill 或任务遇到「command not found」「module not found」「cannot find module」；`ai-command-executor` 环境检查失败；`ai-runtime-verify` 检测到 Playwright 浏览器缺失；开始任何声明了工具依赖的任务之前；用户说「安装 X」「搭环境」「初始化项目」。
- **核心规则**：自举必须：1）检测当前环境；2）识别缺失工具；3）按版本锁定安装；4）配置项目专属设置；5）端到端验证工具链。**禁止在未验证的情况下假定工具可用。**核心原则：**永远不要让用户去装工具。检测缺口、解决它、验证它、继续。**
- **关键流程/检查点**：
  1. 自愈循环：Detect → Research → Acquire → Install → Verify → Record → Continue。
  2. 注册表优先规则（Registry-First Rule）：安装**任何**工具之前先查持久注册表 —— `python scripts/py/tool_registry.py get {tool_name}`；已登记则直接使用既有路径，**不要重装**；未登记则安装后执行 `python scripts/py/tool_registry.py set {tool_name} "{install_path}" "{version}"`。注册表 `tools/tool-registry.json` 是跨会话的持久记忆。
  3. 标准工作流 9 步：接收「需要工具 X」→ 1a 先查注册表 → 1b 已登记则返回路径结束（省时且避免重装）→ 2 检查是否已安装（是则返回路径/版本）→ 3 分类工具类别 → 4 检索记忆（装过则复用既有策略）→ 5 检索互联网找标准安装方法 → 6 用合适的包管理器执行安装 → 7 验证安装成功 → 8 记录并缓存安装策略 → 9 返回工具已可用。
  4. 工具类别与获取策略五类：包管理器（npm/pip/Playwright 浏览器）、系统工具（`git`、`curl`、`jq`，Windows 用 `winget`、Linux 用 `apt-get`）、运行时环境（Node.js、Python、Java/JDK、.NET SDK）、数据库与服务（MySQL CLI、Docker、Redis）、浏览器自动化（Playwright、Edge/Chrome 回退 channel）。
  5. 自我进化机制：遇到已知类别之外的新工具时 —— 检测缺什么/什么包格式 → 调研安装说明（互联网、npm/pip registry、winget/chocolatey/apt）→ 执行安装 → 重新跑版本/检测检查 → 记录进知识库 → 把新模式喂给 `ai-skill-evolver`。
  6. 集成点：`ai-command-executor` 环境检查失败时先委派给 bootstrapper 再重试；`ai-runtime-verify` 发现 Playwright 浏览器缺失时触发 bootstrapper；`ai-chief-planner` 在项目搭建阶段自举全部声明依赖；`ai-skill-evolver` 接收新工具模式。
- **门禁与资格**：源文件未明确 `L0`–`L3`/`Q0`–`Q3` 门禁代号；本 Skill 的门禁是「先查注册表 → 安装 → 安装后必须验证」。
- **必交产出**：工具注册表条目（`tools/tool-registry.json` 中的名称、路径、版本）；安装记录（缺了什么、怎么修、耗时多久）；沉淀的安装策略；反馈给 `ai-skill-evolver` 的新工具模式。
- **防护规则**（`## Guardrails | 防护规则`）：
  1. **未经用户知悉不得安装系统级工具**（包级工具通知但不阻断）。
  2. **优先项目本地安装**，而非全局安装。
  3. **记录每一次安装** —— 缺了什么、怎么修、耗时多久。
  4. **优雅处理网络失败** —— 离线检测、退避重试。
  5. **尊重操作系统边界** —— Windows 用 `winget`/`choco`，Linux 用 `apt`/`yum`，macOS 用 `brew`。
  6. **安装后必须验证** —— 永远不要假定安装成功。

---

## 附录 A：core 层加载顺序建议

本层在方法论中承担「分类 → 路由 → 分解 → 执行 → 进化」的主干。建议的加载顺序：

| 次序 | 阶段 | Skill | 加载理由 |
|---|---|---|---|
| 1 | 会话启动 | `ai-project-classifier` | Step 0 分类先行；未分类不得执行（`AGENTS.md` 亦将其列为会话启动必读） |
| 2 | 会话启动 | `ai-tool-bootstrapper` | 环境自检发现缺失工具即自愈，避免后续「神秘报错」 |
| 3 | 每个任务开始 | `ai-rule-dispatcher` | 判定任务线、主导 Skill、首要文档与前置事实检查 |
| 4 | 产品主导交付 | `ai-product-directed-delivery` | 先划清 `product owner` 与智能体职责，产出产品到工程契约 |
| 5 | 规划 | `ai-chief-planner` | 项目级范围、调度、跟踪与收口 |
| 6 | 分解 | `ai-task-decomposer` | 冻结范围、分层、构建可执行批次 |
| 7 | 并行扇出 | `ai-multi-agent-orchestration` | 跨领域并行时先定领域边界与契约 |
| 8 | 架构 | `ai-architect-governor` → `ai-atomic-architect` | 先做跨域架构决策与 ADR，再落地 `atomic service`/`atomic orchestration`/`aggregate interface`/`command gateway` |
| 9 | 执行前 | `ai-library-first` | 写任何代码前先查成熟库与项目既有组件 |
| 10 | 执行 | `ai-command-executor` | 统一命令入口、执行前检查与工作树闸门 |
| 11 | 基座改动 | `ai-foundation-governor` | 触及权限、菜单路由、参数、Schema 迁移时强制加载 |
| 12 | L2/L3 交付 | `ai-delivery-contract-governor` | 建立可机器校验的写入边界与失败即阻断门禁 |
| 13 | 交付收口 | `ai-5s-delivery-governor` | 选择风险分级门禁、记录 `Q0`–`Q3` 资格与收口声明 |
| 14 | 任务后 | `ai-skill-evolver` | 把重复模式沉淀为 Skill 更新 |
| 15 | 周期性 | `ai-skill-governor` | 每周/每月审计矛盾、重叠、腐蚀、有效性与孤儿 |

约定：

1. 上述次序是**依赖顺序**而非每次全量加载；按任务实际风险裁剪（见 `03_翻译口径与同步规则.md` 与 `AGENTS.md` 的成本护栏）。
2. `ai-project-classifier` 与 `ai-tool-bootstrapper` 属 `AGENTS.md` 定义的会话启动阶段（Phase 1）必读。
3. 进入前端/后端/老项目等新领域时，按 `AGENTS.md` Phase 2 追加治理层 Skill，不要整层批量加载。

---

## 附录 B：本层涉及的门禁代号速查

| 代号 | 名称 | 出处 Skill | 含义 |
|---|---|---|---|
| `L0` | 最小门禁 | `ai-5s-delivery-governor`、`ai-delivery-contract-governor`、`ai-product-directed-delivery`、`ai-task-decomposer` | 复制、只读状态、外观类本地展示；证据为目标路由/API 可达且预期展示可见 |
| `L1` | 局部门禁 | 同上 | 单组件、页面、接口或本地缺陷；证据为变更交互 + 受影响构建/编译检查 |
| `L2` | 共享门禁 | 同上 | 共享业务模块、命令、聚合、元数据或写入路径；证据为运行时 profile/契约 + 命令执行 + 权威事实回读 |
| `L3` | 高风险门禁 | 同上 | schema、租户/权限/版本策略、跨模块回写、发布、部署或生产风险；证据为生命周期回归 + DB/运行时/客户端/发布证据 |
| `Q0` | 交付资格：能力存在 | `ai-5s-delivery-governor` | 能力存在于代码、注册表或路由中；存在不等于执行 |
| `Q1` | 交付资格：配置对齐 | `ai-5s-delivery-governor` | 参数、权限、状态、配置与必需材料对齐 |
| `Q2` | 交付资格：技术可执行 | `ai-5s-delivery-governor` | 后端编排、provider 覆盖、唯一副作用路径与审计链闭合 |
| `Q3` | 交付资格：业务闭合 | `ai-5s-delivery-governor` | 真实客户或 `product owner` 场景跨所需客户端完成、对账通过、发布证据被接受 |
| `P0` | 最高优先级 | `ai-chief-planner`（优先级）、`ai-task-decomposer`（批次优先级） | 计划与批次优先级最高级；通知分级语境下 `P0` 对应模态框 |
| `P1` | 高优先级 | 同上 | 计划与批次优先级次高级；通知分级语境下对应常驻横幅 |
| `P2` | 中优先级 | 同上 | 计划与批次优先级第三级；通知分级语境下对应轻提示（Toast） |
| `P3` | 低优先级 | 通知分级通用 | 通知分级语境下对应控制台 |
| `complete` | 交付状态：完成 | `ai-5s-delivery-governor`、`ai-delivery-contract-governor` | 仅在 Safeguard 通过且项目必需集成/发布动作真实发生后使用 |
| `paused` | 交付状态：暂停 | `ai-5s-delivery-governor` | 未推送提交、远端不可用或集成进行中 |
| `blocked` | 交付状态：阻断 | `ai-5s-delivery-governor`、`ai-delivery-contract-governor` | 证据失败或存在未解阻断；不得静默继续 |
| `fail-closed` | 失败即阻断 | `ai-delivery-contract-governor`、`ai-foundation-governor` | 缺少证据、越界改动、过期证据或评审失败即阻断状态推进 |
| `draft` / `scoped` / `approved` / `implementing` / `safeguarded` / `completed` / `cancelled` | `DeliveryContract` 状态机 | `ai-delivery-contract-governor` | 契约状态名不译；`safeguarded` 需 `--check-freshness` 通过且两轴评审通过 |
| `registered` → `configured` → `authorized` → `provider-covered` → `runtime-executable` → `business-closed` | 能力执行成熟度链 | `ai-atomic-architect` | 低阶状态不得谎报为高阶；适配器不得提升成熟度 |
| `backlog` / `planned` / `in_progress` / `review` / `verified` / `closed` | 任务状态模型 | `ai-chief-planner` | 项目任务从待办到归档的状态流转 |
| raw / generalized / callable / verified / deprecated | Skill 成熟度等级 | `SKILL_MANIFEST.json`、`ai-skill-governor` | 本层 16 个 Skill 全部为 verified |
| declared / callable / effective / in-closure / evolving | Skill 有效性评级 | `ai-skill-evolver` | 用于区分「存在」「可调用」与「真正有效」 |

代号使用约定：

1. `L0`–`L3` 是**风险分级门禁**，选择「能证明实际风险的最小门禁」；仅因项目有发布工具不得强推 `L3`，schema/授权/版本权益/部署/跨模块回写实际在范围内时不得跳过 `L3`。
2. 健康端点、HTTP 200、页面能打开、CI 绿、本地提交只是支撑证据，都不构成 `Q2`/`Q3` 资格。
3. `complete` 与 `safeguarded` 是**两个轴**：`Safeguard` 可在 `Q2` 通过，而 `Sell` 因等待 `business-flow acceptance` 或发布证据仍处于阻断。

---

## 译注

1. 本文件是**中文详摘索引**，不是正文全量译文。逐节全量对应的正文中文版按规划放在 `50_Skill正文中文版/core/`；本文件的目标是让读者不打开英文源也能独立读懂 16 个 core Skill 的职责、规则强度、门禁与产出。
2. 源文件本身没有中文章节的小节（如 `ai-architect-governor`、`ai-chief-planner`、`ai-command-executor`、`ai-library-first` 未单列 `## When to Use`），其触发条件取自 frontmatter `description`，已在对应条目中注明。
3. `ai-5s-delivery-governor` 的 `## Required Closure Statement` 只有 `complete` / `paused` / `blocked` 三个状态；`ai-delivery-contract-governor` 的契约状态机另含 `draft`/`scoped`/`approved`/`implementing`/`safeguarded`/`completed`/`cancelled`。两者不合并使用，均在附录 B 中列出。
4. 源文件中的源代号（如 `gerp-*`）与抽取来源仅出现在各 `SKILL.md` 的 `## Evolution History` 与 `SKILL_MANIFEST.json` 的 `source` 字段；本摘要未展开进化记录，以免与正文中文版重复。
5. 未在本层源文件中出现的门禁代号（如治理层与外层使用的 `L4`–`L5`）不在本文件展开。
