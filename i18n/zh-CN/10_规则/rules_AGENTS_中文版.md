# 企业级 AI 辅助开发方法论 | Enterprise-Grade AI-Assisted Development Methodology

> **源文件**：rules/AGENTS.md
> **源版本**：2.5.0（源文末标注：`Methodology version: 2.5.0 | Last updated: 2026-08-24`）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

> **语言**：双语（CN/EN）。所有 AI 智能体必须在每次会话开始时读取本文件。

---

## 0. 会话启动协议 | Session Start Protocol (EVERY SESSION)

### 0.0 正式源目录 | Source of Truth

**官方可移植方法论源：**
- Skills：`skills/`
- Skill 清单：`skills/SKILL_MANIFEST.json`
- 规则：`AGENTS.md` 与 `rules/AGENTS.md`
- 工具适配器目录：`.agents/`、`.trae/`、`.qoder/`、`.claude/`、`.codebuddy/`
- 私有本地归档不进发布包，永远不作为官方 Skill 根目录。

规则提到某个 Skill 时，先从 `skills/{layer}/{skill-name}/SKILL.md` 解析。适配器目录可能由 `tools/deploy.ps1` 生成，不得当作唯一真相源。

### 0.1 防遗忘 | Task Continuity
**在做任何事之前：**
1. 读取 `docs/全项目总控/TASK_BACKLOG.md`
2. 若存在未完成任务 → 提醒用户：
   "你还有 [N] 个未完成任务：[清单]。继续，还是开始新任务？"
3. 由用户决定 → 更新待办台账


### 0.2 工具发现 | Tool Discovery（存量项目）
**分析一个已有项目之前：**
1. 运行：`py scripts/py/discover_tools.py {project_path} --by-purpose`
2. 按用途编目现有脚本
3. 用现有脚本，不要另写新脚本
4. 匹配项目既有模式

**规则**：项目有 50+ 个脚本，就说明工装已经成熟。必须尊重它。

### 0.3 环境自检 | Environment Verification
**任何代码工作之前：**
1. 运行：`py scripts/py/env_check.py --quick`（Linux/Mac 上用 `python` 或 `python3`）
2. 若工具缺失 → 交给 ai-tool-bootstrapper 自动安装
3. 若工具齐全 → 继续

**真正的病因是工具缺失时，禁止把时间浪费在排查“神秘报错”上。先查环境。**

### 0.4 路径记忆 | Tool Path Check
**安装任何工具之前：**
1. 检查 `tools/tool-registry.json` —— 该工具是否已安装？
2. 运行：`py scripts/py/tool_registry.py get {tool_name}`
3. 若已登记 → 直接用现有路径。禁止重复安装。
4. 若为新增安装 → 登记路径：`py scripts/py/tool_registry.py set {name} "{path}" "{version}"`

### 0.5 5S 交付接管 | 5S Delivery Takeover

对版本化交付、共享能力、发布、部署、模式（schema）、权限或支持基线（supported baseline）缺陷工作：

1. 读取 `skills/core/ai-5s-delivery-governor/SKILL.md`。
2. 记录最小充分变更记录：类型、目标版本/线、受影响流程、真相责任人、非目标，以及 L0-L3 门禁。
3. 基线缺陷按“在哪里复现”路由，而不是按“在哪里发现”路由。
4. 不得把一次本地修改或本地提交称为“已交付”。必需的集成、远端、CI、发布与部署证据，仍是项目自有的收口条件。

本节落地的治理框架即 `5S Delivery Governance`（5S 交付治理，见 `skills/core/ai-5s-delivery-governor/SKILL.md`）。使用轻量生命周期 `scope -> specify -> ship -> safeguard -> sell`，逐段对应「范围（Scope）→ 说明（Specify）→ 实现（Ship）→ 保障（Safeguard）→ 销售放行（Sell）」。对只读审计、草稿或小规模本地实验，不得强加发布仪式。

### 0.6 产品主导的全 AI 交付 | Product-Directed AI Delivery

本节即 `product-directed AI delivery`（产品主导的全 AI 交付）。对该交付模式，产品负责人（`product owner`）可以完全用业务语言、截图、样例和已跑通的业务流程测试来工作。`product owner` 拥有结果、可用性、范围、优先级、非目标和最终业务验收。AI 智能体负责需求分析、标杆调研、架构、模式（schema）、后端、前端、测试、证据与发布执行。

在实现任何可复用功能之前，先声明两条链：

```text
Backend: truth -> atomic service -> orchestration -> aggregate interface -> command gateway -> adapters -> Host
Frontend: runtime/field truth -> UI atom -> UI orchestration -> standard template -> Host page
```

Host 页面（`host page`）与传输适配器只负责加载、渲染、收集输入、请求受支持的命令并展示反馈。它们不得成为第二套业务逻辑、状态迁移、字段真相、授权、计算或写入路径的来源。技术门禁通过，不能替代 `product owner` 已完成的 `business-flow acceptance`（业务流程验收）。

关于产品归属、智能体交接、十二步交付地图与验收边界，读取 `skills/core/ai-product-directed-delivery/SKILL.md`。

### 0.7 安全修改与精准定位 | Safe AI Change and Code Location

对任何缺陷修复、功能、重构、删除、重命名、迁移或大型项目批次，写代码前先使用 `skills/core/ai-product-directed-delivery/SKILL.md`。本节即 `safe AI change and code location`（安全修改与代码定位）。

1. **先读、先证、再改（`read, prove, then change`）**：识别业务症状、真相责任人、候选文件、既有工作区（`working-tree`）改动、`impact`（影响）边界、验证方式与回滚路径。
2. **从用户流程追到真相**：`menu/route -> rendered Host -> shared UI/template -> API -> controller/adapter -> command gateway/aggregate -> orchestration/atomic service -> domain facts/FieldPackage/BusinessProfile/permission -> mapper/DB -> tests/gates`。
3. **保护文件与代码**：对删除/重命名/批量替换先分类。共享文件、未知文件、模式、配置、租户数据以及破坏性（`destructive`）Git 操作一律默认保护；数据库级或仓库级 `destructive` 操作需要显式确认与可恢复证据。
4. **保持无关工作原样**：禁止全局清理脏工作区；使用 `exact file or hunk staging`（按文件或按块精确暂存），检查暂存差异，并在提交前验证。
5. **大型工作按自动驾驶批次推进**：AI 负责绘制代码与依赖地图、选择 L0-L3 门禁、逐个批次实现并证明，然后汇报产品可见结果，只在遇到 `business ambiguity`（业务歧义）、重大权衡、`destructive` 决策或发布授权时询问负责人。

`product owner` 永远不需要定位源文件或写代码。AI 负责调查与实现；负责人拥有产品意图与 `business-flow acceptance`。

### 0.8 职责、任务包与方法论回归 | Delivery Roles, Task Pack, and Methodology Regression

对产品主导或多步交付：

1. 读取 `docs/全项目总控/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md`，为当前阶段选定一个主 Skill。
2. 从 `docs/_templates/全项目总控/AI_PRODUCT_DELIVERY_TASK_TEMPLATE.md` 起步。`product owner` 只提供产品结果、样例、优先级、可用性预期与 `business-flow acceptance`；工程证据由 AI 填写。
3. 当官方规则、产品交付 Skill、模板或路由边界变更时，除 `audit_methodology.py` 外还要运行 `py scripts/py/test_methodology_scenarios.py --project-root .`。

职责矩阵只澄清归属；它不授权任何 Skill 绕过项目专有规则、真相责任人、验证门禁或显式的破坏性操作确认。

### 0.9 新鲜证据、共享语言与双轴审查 | Evidence Freshness, Shared Language, and Two-Axis Review

对非平凡交付：

1. **先给新鲜证据再下结论（`fresh evidence before claims`）**：先确定能证明某个结论的命令、浏览器检查、API 调用、数据库回读或差异检查；在最后一次相关改动之后运行它；在说任务“完成、已修复、已通过、可提交/可发布”之前，读取它的退出状态与结果。更早的 `fresh evidence`、一个绿色的健康端点，或仅有智能体报告，都不构成收口。
2. **关键接缝测试先行**：对新增或变更的领域规则、缺陷回归、命令/编排行为，以及其他可测试的公共接口，先写一个针对目标行为失败（红）的聚焦测试，再做最小通过改动（绿），并重跑聚焦测试与受影响的回归测试。对纯拷贝、生成物、仅配置或探索性任务，不得强行套用红绿流程；改为记录有理由的验证方式。
3. **`shared language`（共享语言）是交付资产**：当任务引入或依赖有歧义的领域术语、稳定缩写或跨会话决策时，在 `docs/` 下维护一份简洁的项目上下文/术语表，以及 ADR 或决策记录。在规格、测试、API 与代码中复用这套语言；不得让术语表取代权威业务规则或数据模型。
4. **独立审查两轴（`review two independent axes`）**：非平凡改动在提交或发布前，必须同时审查 (a) 标准/真相/架构/质量门禁，与 (b) 原始产品结果、验收流程和显式非目标。只有当 `two independent axes` 都不存在未处理的阻断项，改动才算通过评审。评审力度与所选 L0-L3 门禁相称，并优先复用项目自有的评审工装。

对发布或客户就绪声明，还要记录来自 `ai-5s-delivery-governor` 的已达成 `Q0-Q3` 交付资格（`qualification`）。`Q0` 仅表示“能力存在”；`Q1` 表示基线对齐；`Q2` 表示技术上可执行的后端收口；`Q3` 表示真实业务验收、对账与发布证据。HTTP 200、健康检查、页面可访问、CI 与本地提交，永远不能把结果提升为 `Q3`。

### 0.10 可执行交付契约 | Executable Delivery Contract

对 L2/L3 交付、并行智能体工作，或任何带破坏性、跨模块、权限、模式、发布或高风险边界的任务：

1. 读取 `skills/core/ai-delivery-contract-governor/SKILL.md`。
2. 依据 `docs/_templates/全项目总控/task_contract.json`，使用 `docs/全项目总控/schemas/governance/delivery-contract.schema.json`，创建任务本地的 `DeliveryContract`。
3. 写入之前，用 `py scripts/py/validate_delivery_contract.py --contract <path>` 校验范围、真相责任人、非目标、公共可测试边界（`public_test_seam`）或有理由的替代方案、证明计划，以及精确写入白名单。
4. 在 Safeguard/complete 之前，校验实际改动文件、最终 `fresh evidence` 与独立双轴评审（`two independent axes`）。L2/L3 要求 `verification_owner` 与 `implementer` 不是同一人。

契约是失败即阻断（fail-closed）的：改动路径落在白名单之外、命中显式禁止路径、缺少证明、证据过期，或评审失败/待评，都会阻断 `safeguarded` 与 `completed`。它不替代项目自有的测试、运行时/DB 证据、CI、业务真相或负责人授权。

对数据库、种子数据、参数基线或租户数据变更，契约必须挂接一份迁移一致性记录，覆盖清单标识、校验和、测试/生产登记、执行历史、迁移后检查与恢复方案。对租户生命周期变更，契约必须挂接一份回归记录，覆盖目标/对照租户、写入范围、隔离、权威回读、审计，以及残留或回滚检查。能力声明必须声明其成熟度：`registered -> configured -> authorized -> provider-covered -> runtime-executable -> business-closed`。

---

## 1. 概述 | Overview

本文件定义 AI 辅助企业级软件开发的强制性规则、工作流和工程纪律。它提炼自真实多租户 ERP 系统的实战经验，并通用化为普适标准。

本文档定义了 AI 辅助企业级软件开发的强制性规则、工作流和工程纪律。提炼自真实多租户 ERP 项目的实战经验，已通用化为适用于任何项目的标准。

### 核心哲学 | Core Philosophy

| 原则 | EN | CN |
|---|---|---|
| **Check Before Execute** | Never assume. Always verify the current state of DB, code, runtime before acting. | 先检查后执行：任何操作前必须核实数据库、代码、运行时现状 |
| **No Degradation** | Find root cause. Never apply temporary workarounds. | 禁止降级方案：必须找到根本原因，不允许以临时手段绕过 |
| **Data-Driven Development** | DB is the single source of truth. All changes start from the database. | 数据驱动开发：数据库是唯一真相源，所有修改从数据库开始 |
| **Frontend = Display Only** | Frontend renders. Backend decides. Zero business logic in UI layer. | 前端纯展示。UI 层零业务逻辑，计算、校验、决策全部在后端 |
| **Library First** | Never rewrite what a mature open-source library already does. | 库优先：优先使用成熟开源组件，禁止重复造轮子 |
| **Zero-Fluff UI** | ERP/SaaS/admin pages must have zero decorative text. Only actionable prompts. | 零废话规则：管理后台页面禁用装饰性文案，只保留可操作提示 |
| **Plan-Driven Execution** | Every task must have a plan with acceptance criteria before execution. | 计划驱动：每个任务必须先制定详细计划再执行 |
| **Long-Term Collaboration** | Treat AI-assisted enterprise delivery as sustained cooperation, not a one-shot token burn. | 长期协作：默认服务长期 ERP/企业级交付，不把成本压力误判为“用户用不起”，而要通过拆批、验证和复用降低消耗 |
| **5S Delivery Governance** | Bound delivery through Scope, Specify, Ship, Safeguard, Sell. | 5S 交付治理：用范围、说明、实现、保障、销售放行约束可审计交付。 |
| **Product-Directed AI Delivery** | Product owner defines outcome and acceptance; AI agents execute the verifiable engineering system. | 产品主导全 AI 交付：人定义结果与验收，智能体完成可验证工程系统。 |

### 协作成本护栏 | Collaboration Cost Guardrail

- 方法论是长期交付资产。当更小的、已验证的批次就能解决当前业务问题时，不得把每个任务都强塞进完整 OS 路径。
- 以可持续协作为优化目标：优先采用有界批次、可复用脚本、现有工具和基于证据的验证，而不是反复的大范围探索。
- 禁止仅为省 token 或省时间，就跳过必需的验证、数据库检查、构建检查、API 检查、浏览器检查或 git 范围检查。
- 当平台级构想超出单人或单个交付周期时，把它保留为私有能力、规则或未来路线图条目，优先做能守住当前现金流与交付势能的 ERP/业务任务。
- 在公开/开源定位上，区分重型内部内核与轻量采用入口。先讲审计、lite 安装、验证与具体证据，再呈现完整的 AI 开发 OS。

---

## 2. 项目分类 | Project Classification (Step 0)

任何开发工作之前，先给项目分类。详见 skills/core/ai-project-classifier/SKILL.md。

| 维度 | 选项 | 决定 |
|---|---|---|
| **来源** | 老项目（brownfield，存量）/ 新项目（greenfield，全新） | 先读 vs 脚手架 |
| **质量目标** | Rapid Prototype / AI-Native / Enterprise | 加载哪些 Skill、哪种架构 |
| **部署目标** | Web / Mobile / WeChat / MCP / All | 接口设计策略 |
| **规模** | Monolith / Atomic Services / Microservices | 服务拆分粒度 |

**规则**：不明确时默认 AI-Native。降级比升级容易。

---

## 3. 强制开发顺序 | Mandatory Development Order (13+1 Steps)

### Step 0：项目分类
- 按 4 个维度给项目分类
- 选择 Skill 集与架构原型
- **门禁**：分类已留档

### 后端阶段 | Backend Phase

| 步骤 | 动作 | 验证 |
|---|---|---|
| 1 | **数据库初始化** —— SQL 脚本 → 建模式（schema） → 校验表 | SHOW TABLES; DESCRIBE table; |
| 2 | **实体层** —— 生成实体类 → 补注释 → 校验映射 | 检查字段-列对齐 |
| 3 | **Mapper 层** —— 继承 BaseMapper → 自定义查询 → 校验 SQL | 执行并检查结果 |
| 4 | **Service 层** —— 业务逻辑 → 缓存配置 → 事务管理 | 单元测试通过 |
| 5 | **Controller 层** —— REST API → API 文档 → 权限控制 | curl 端点测试 |
| 6 | **构建验证** —— 编译 → 启动测试 → API 健康检查 | 健康端点 UP |

### 前端阶段 | Frontend Phase

| 步骤 | 动作 | 验证 |
|---|---|---|
| 7 | **API 契约** —— 从后端生成 → 校验字段一致性 | 与后端 DTO 比对 |
| 8 | **Service 层** —— API 调用封装 → 错误处理 → 校验端点 | 检查 Network 面板 |
| 9 | **组件** —— 页面开发 → 复用标准模板 → 功能测试 | 遵循 component-standardizer |
| 10 | **集成测试** —— API 测试 → 功能完整性 → 错误处理 | 全流程测试 |
| 11 | **种子数据** —— 写测试数据 → 在 DB 中校验 → 在 UI 中验证 | CRUD + 边界场景 |
| 12 | **模式同步** —— 模板 → 所有实例 → 校验同步状态 | 比对模式 |

### 验证阶段 | Verification Phase

| 步骤 | 动作 | 验证 |
|---|---|---|
| 13 | **运行时验证** —— 无头浏览器 → 检查 console/loading/DOM/API | ai-runtime-verify 返回 passed:true |
| 13a | **发布治理**（仅企业级）—— 锁版、P0 审计、人工测试台账、业务流程验收 | 全部 P0=0、P1<5、人工测试通过 |

**⚠️ 关键**：宣称“开发完成”之前，Step 13 必须通过。企业级发布中 Step 13a 为强制项。

**⚠️ 关键**：宣称“开发完成”之前，Step 13 必须通过。参见 skills/governance/ai-runtime-verify/SKILL.md

**关键规则**：每一步必须先通过验证，才能进入下一步。

**技术栈说明**：上述 13+1 步实例化的是 Java / Spring Boot + Vue + MySQL 技术栈。其他技术栈（Node、Python、Go、React、PostgreSQL）沿用同一骨架 —— DB → 后端 → API → 前端 → 验证 —— 并把每一步映射到该技术栈的对应层。

---

## 4. Skill 体系架构 | Skill Architecture (5 Layers)

`
+--------------------------------------------------+
|         LAYER 0: CLASSIFICATION | 分类层           |
|         ai-project-classifier                     |
|         "What kind of project? What quality?"     |
+--------------------------------------------------+
                         |
+--------------------------------------------------+
|         LAYER 1: ROUTING | 路由层                 |
|         ai-rule-dispatcher                        |
|         "Which skill and rules apply?"            |
+--------------------------------------------------+
                         |
+--------------------------------------------------+
|         LAYER 2: DECOMPOSITION | 分解层           |
|         ai-task-decomposer                        |
|         "How to break this into safe batches?"    |
+--------------------------------------------------+
                         |
+--------------------------------------------------+
|         LAYER 3: EXECUTION | 执行层               |
|         20+ domain, governance & tech skills      |
|         "Write the code, follow the rules."       |
+--------------------------------------------------+
                         |
+--------------------------------------------------+
|         LAYER 4: EVOLUTION | 进化层               |
|         ai-skill-evolver                          |
|         "What did we learn? Update the rules."    |
+--------------------------------------------------+
`

Skills 目录结构：
- skills/core/ —— 引擎 Skill（分类、路由、分解、计划、执行、自举、库优先、进化）
- skills/governance/ —— 治理 Skill（single-truth、component-standardizer、frontend-audit、runtime-verify、ui-ux、flow-closure、domain-boundary、field-package、competitor-analyst）
- skills/tech/ —— 技术栈 Skill（Vue、Spring Boot、Flutter、Docker、Tailwind、MySQL 等）
- skills/platform/ —— 平台集成 Skill（CNB API、流水线、代码提交、代码评审）

---

## 5. Skill 加载生命周期 | Skill Loading Lifecycle

### ⚠️ 上下文衰减警告
AI 上下文窗口是有限的。长会话早期加载的规则必然会从活跃记忆中淡出。这不是 bug —— 这是物理限制。下面的加载生命周期就是为对抗它而设计的。

### 渐进披露 | Progressive Disclosure
Skill 分两阶段加载以节省上下文：先读 Skill 的 `description`（frontmatter / `SKILL_MANIFEST.json` 行），只有当它与当前任务匹配时，才加载完整的 `SKILL.md`。禁止批量加载整个分层。repomap（`py scripts/py/build_repomap.py --project-root .`）用于快速定位代码符号，而不是扫描整棵目录树。

### 阶段 1：会话开始（只加载一次）
- `AGENTS.md`（本文件）—— 始终加载
- `skills/SKILL_MANIFEST.json`
- `skills/core/ai-project-classifier/SKILL.md`
- `skills/core/ai-tool-bootstrapper/SKILL.md`

### 阶段 2：领域入口（进入新领域时加载）

**进入前端工作 → 必须重读：**
- skills/governance/ai-single-truth-enforcer/SKILL.md
- skills/core/ai-library-first/SKILL.md
- skills/governance/ai-component-standardizer/SKILL.md

**进入后端工作 → 必须重读：**
- 你所用技术栈的后端技术 Skill（java-springboot / springboot-patterns / 等）
- skills/core/ai-library-first/SKILL.md
- skills/governance/ai-single-truth-enforcer/SKILL.md（规则 2：single truth，单一真相）

**进入老项目工作 → 必须重读：**
- skills/governance/ai-brownfield-analyzer/SKILL.md
- methodology/09_老项目改造方法论.md

**进入不熟悉的领域 → 应当重读：**
- skills/governance/ai-reference-researcher/SKILL.md

### 阶段 3：门禁前重读（关键动作前加载）

**向文件写入任何代码之前 → 校验：**
- 最近 50 条消息内，我是否重读过领域治理 Skill？没有就现在重读。

**宣称“代码完成”之前 → 必须重读：**
- skills/governance/ai-runtime-verify/SKILL.md
- skills/governance/ai-single-truth-enforcer/SKILL.md（审计清单）

**提交 / PR 之前 → 必须重读：**
- skills/governance/ai-frontend-audit/SKILL.md（若涉及前端改动）
- skills/governance/ai-runtime-verify/SKILL.md

### 阶段 4：压缩规则提醒
上下文紧张、完整重读 Skill 代价过高时，使用这份压缩清单：

```
QUICK CHECK (15 rules, always active):
□ Frontend = display only. Backend computes everything.
□ Check ai-library-first before writing custom code.
□ Page must match standard template (list/document/report/dashboard).
□ Notification severity: P0=Modal, P1=Banner, P2=Toast, P3=Console.
□ Test evidence REQUIRED before "done" — must show verify JSON path or test output.
□ Missing tool → auto-install, never ask user.
□ Every page handles 4 states: loading, empty, error, edge.
□ Brownfield: audit before code, match existing style.
□ No business logic in Vue computed() or React useMemo().
□ Single truth: never compute same value in two places.
□ Versioned delivery: record 5S state and select an L0-L3 gate.
□ Product owner owns business acceptance; AI owns evidence-backed engineering execution.
□ Completion claims use fresh evidence from the final relevant change.
□ Critical business seams use focused red-green tests when testable.
□ Review both standards/truth and the originating business acceptance.
```


---

## 6. 非协商规则 | Non-Negotiable Rules

这些规则由治理 Skill 强制执行。违反其中任何一条，任务即视为未完成。

### 数据与逻辑
| # | 规则 | 强制方 |
|---|---|---|
| 1 | **前端纯展示**。Vue/React 组件内零业务逻辑。所有计算、校验、决策一律在后端。 | ai-single-truth-enforcer |
| 2 | **后端是唯一真相源**。DB → 后端 API → 前端缓存。同一个取值禁止在两地各算一次。 | ai-atomic-architect |
| 3 | **禁止重复真相源**。同一字段在 2 个以上组件中以不同逻辑定义 = 违规。 | ai-field-package-governor |

### 组件与 UI
| # | 规则 | 强制方 |
|---|---|---|
| 4 | **所有页面使用标准模板**。资料列表页（list）、单据录入页（document）、报表页（report）、看板（dashboard）。禁止逐页自定义布局。 | ai-component-standardizer |
| 5 | **只用主题变量**。禁止硬编码颜色。所有样式通过 CSS 变量实现。 | ai-component-standardizer |
| 6 | **通知分级对应严重级**：P0=Modal、P1=常驻横幅（Banner）、P2=Toast(4-6s)、P3=Console。 | ai-ui-ux-governor |
| 7 | **零废话**。操作页面禁止欢迎语、营销文案、占位帮助文本。 | ai-ui-ux-governor |

### 代码质量
| # | 规则 | 强制方 |
|---|---|---|
| 8 | **库优先**。写自定义代码前先查 npm/pip/maven。从零手写浪费 96%+ token。 | ai-library-first |
| 9 | **无静默失败**。每个错误都必须按正确严重级呈现给用户。 | ai-single-truth-enforcer |
| 10 | **P0 破坏性操作 = 模态框确认**。删除/不可逆操作必须确认，禁止用 Toast。 | ai-single-truth-enforcer |

### 验证
| # | 规则 | 强制方 |
|---|---|---|
| 11 | **宣称“完成”之前先做运行时验证**。浏览器必须零 console 错误加载、loading 遮罩已移除、DOM 已渲染。 | ai-runtime-verify |
| 12 | **工具缺失 = 自动安装**。禁止让用户去装。检测 → 获取 → 验证 → 继续。 | ai-tool-bootstrapper |
| 13 | **每个页面处理 4 态**：加载（Loading）、空（Empty）、错误（Error）、边界（Edge Cases）。 | ai-frontend-audit |
| 14 | **没有测试 = 未完成**。每个任务在宣称完成前必须产出通过的测试。给出测试输出路径（verify JSON、jest/pytest 输出）。 | ai-runtime-verify / jest / pytest |
| 15 | **先给新鲜证据再宣称完成**。证明用的命令/检查必须在最后一次相关改动之后运行；智能体报告与旧证据都不充分。 | ai-runtime-verify / ai-flow-closure-audit |
| 16 | **独立审查标准与产品意图**。非平凡提交/发布必须同时检查仓库/真相规则与来源验收/非目标。 | ai-flow-closure-audit / ai-5s-delivery-governor |

---

## 7. 完整 Skill 索引 | Complete Skill Index

### 核心引擎（skills/core/）—— 16 个 Skill

| Skill | 用途 | 何时加载 |
|---|---|---|
| ai-project-classifier | 给项目分类（brownfield/greenfield、质量、规模、部署目标） | 项目开始时永远第一个加载 |
| ai-product-directed-delivery | 产品负责人/AI 职责边界、十二步交付地图、后端/前端 Host 链 | 产品主导的 AI 原生交付 |
| ai-rule-dispatcher | 把任务路由到正确的 Skill 并加载必需文档 | 每个新任务 |
| ai-task-decomposer | 把复杂工作拆成安全的可执行批次 | 多模块或跨端任务 |
| ai-multi-agent-orchestration | 跨领域编排并行智能体：依赖矩阵、契约优先集成、角色/验收边界 | 多领域或多智能体扇出工作 |
| ai-chief-planner | 端到端项目计划、排期、收口 | 项目级编排 |
| ai-command-executor | 带环境校验的标准化命令执行 | 任何 shell/CLI 操作 |
| ai-delivery-contract-governor | 创建并校验机器可读任务契约：写入范围白名单、新鲜证据、失败即阻断的 L2/L3 门禁 | L2/L3 交付、并行智能体、破坏性/跨模块/模式/发布边界 |
| ai-tool-bootstrapper | 自动检测并安装缺失工具 | 出现 “tool not found” 错误时 |
| ai-library-first | 强制：写自定义代码前先检查现有库 | 任何代码生成之前 |
| ai-architect-governor | 跨领域架构治理、ADR | 架构决策 |
| ai-atomic-architect | AI 原生 atomic service + 编排 + 统一接口 | 项目架构设计 |
| ai-foundation-governor | 版本控制、租户开关、权限、菜单、路由 | 平台基座变更 |
| ai-5s-delivery-governor | Scope/Specify/Ship/Safeguard/Sell 生命周期、门禁选择、发布收口 | 版本化交付、发布、热修复、部署 |
| ai-skill-evolver | 复盘已完成工作、更新 Skill、归档模式 | 任务收口之后 |
| ai-skill-governor | 主动 Skill 健康审计：矛盾、重叠、腐化、孤儿检测 | 每周 / 每月 / 按需 |

### 治理（skills/governance/）—— 13 个 Skill

| Skill | 用途 | 何时加载 |
|---|---|---|
| ai-single-truth-enforcer | 前端纯展示、后端真相、通知分级 | 所有前端工作 |
| ai-component-standardizer | 页面模板（资料列表页/单据录入页/报表页/看板）、主题系统 | 所有页面开发 |
| ai-frontend-audit | 覆盖 6 个维度的静态代码质量审计 | PR/代码评审之前 |
| ai-runtime-verify | 浏览器运行时验证（console/DOM/API/loading） | 宣称“完成”之前 |
| ai-ui-ux-governor | 设计系统治理、密度、状态、零废话 | UI 一致性评审 |
| ai-flow-closure-audit | 业务链验证（页面→API→表→参数→回写） | 业务流程验证 |
| ai-domain-boundary-mapper | 领域边界文档与归属映射 | 跨领域变更 |
| ai-field-package-governor | 字段元数据集中化、DB→元数据→组件链 | 字段/列新增 |
| ai-competitor-analyst | 竞品对标、市场定位调研 | 市场调研任务 |
| ai-reference-researcher | 搜索、下载、分析开源参考实现 | 复杂且不熟悉的领域 |
| ai-brownfield-analyzer | 分析遗留项目、提炼模式、分类干预级别 | 任何存量项目（永远第一个加载） |
| ai-atomic-governance | 原子系统架构治理：声明/执行器分离、分层、治理集成、反模式检测 | 原子架构工作 |
| ai-cross-project-audit | 跨项目治理审计流水线：消费审计数据、编排 L3 领域原子、产出 L5 证据 + 索引 + 报告 | 跨项目审计 |

### 技术栈（skills/tech/）—— 20 个 Skill

| Skill | 用途 |
|---|---|
| vue | Vue 3 Composition API、script setup、响应式 |
| vue-best-practices | Vue 模式、TypeScript、Volar、vue-tsc |
| vue-pinia-best-practices | Pinia store、状态管理 |
| typescript-advanced-types | 泛型、条件类型、映射类型 |
| java-springboot | Spring Boot 最佳实践 |
| java-performance-governance | 批量操作效率、缓存/内存泄漏、SQL 成本、可观测性 |
| springboot-patterns | 架构模式、REST API 设计 |
| springboot-security | AuthN/AuthZ、CSRF、限流 |
| mysql-best-practices | 模式设计、查询优化 |
| node-backend | Node.js 后端：分层服务、校验、异步纪律、测试 |
| python-fastapi | FastAPI 后端：Pydantic 校验、分层服务、异步端点、pytest |
| react-frontend | React 18+ 纯展示组件、hooks、状态、性能、测试 |
| postgresql-best-practices | PostgreSQL 模式设计、索引、EXPLAIN、迁移、备份 |
| docker-expert | 多阶段构建、优化、Compose |
| multi-stage-dockerfile | 优化过的 Dockerfile 模板 |
| flutter-expert | Flutter 3+、Riverpod/Bloc、GoRouter |
| flutter-animations | Flutter 隐式/显式动画 |
| tailwind-css-patterns | 工具优先 CSS 模式 |
| tailwind-design-system | 设计令牌、组件库 |
| javascript-typescript-jest | Jest 测试模式、mock |

**合计**：49 个官方可调用 Skill。只有 `skills/SKILL_MANIFEST.json` 中列出的 Skill 才算官方发布 Skill。

---

## 8. 文档体系 | Documentation System

### 文件夹层级

```
docs/
  _templates/            ← Templates (never edit directly)

  架构决策记录/           ← One ADR per decision file
    ADR-001_多租户架构选型.md

  每日调研回写/           ← One file per day
    2026-06-17_调研记录.md

  业务流程全案/           ← Sub-folders per business process
    采购流程/
    销售流程/

  测试验收报告/           ← One file per test round
    2026-06_R1_核心流程.md

  部署运维手册/           ← Per-environment guides
    dev_部署指南.md
    prod_部署指南.md

  全项目总控/             ← Master control hub
    MASTER_INDEX.md
    PROJECT_STATUS.md
```

**规则**：
- `docs/` 根目录禁止散落 `.md` 文件 —— 全部放进子文件夹
- 任务包放进其领域文件夹，不得作为散落的 `docs/{name}_任务包/`
- 先按类型（ADR/调研/流程），再按主题（财务/采购）

**每日回写规则**：每个开发会话结束后，在对应的 docs/ 分类下写一份带日期的记录。这样会自动构建出可审计的知识库。

---

## 9. 编码规范 | Coding Standards

### 命名 | Naming
- **类**：PascalCase（ProductService）
- **方法/变量**：camelCase（productName）
- **数据库列**：snake_case（product_name）
- **常量**：UPPER_SNAKE_CASE（MAX_RETRY_COUNT）

### 注释 | Comments
- 所有 public 类、方法、字段必须有注释
- 复杂逻辑必须有逐步解释的注释
- 无注释代码视为未完成

### 分层 | Layering
`
Controller -> Service -> Mapper -> Entity
   (API)     (Business)  (Data)   (Model)
`

---

## 10. 文件存放规范 | File Placement Rules

**禁止在项目根目录创建文件。**

| 文件类型 | 目标目录 |
|---|---|
| .bat 脚本 | scripts/bat/ |
| .ps1 脚本 | scripts/ps1/ |
| .py 脚本 | scripts/py/ |
| .sql 文件 | database/ |
| .md 文档 | docs/ |
| 临时文件 | temp/ 或 tmp/ |

**完整脚手架标准**：A/B/C 类项目原型各自的文件夹结构见 methodology/08_项目文件夹结构标准.md。

---

## 11. PDCA 执行循环 | PDCA Execution Cycle

`
PLAN  -> Task analysis, decomposition into safe batches
DO    -> Execute step by step, record evidence
CHECK -> Verify each step result against acceptance criteria
ACT   -> Extract lessons, update skills, close the loop
`

---

## 12. 新项目初始化 | Project Bootstrapping

新项目按以下步骤初始化本方法论：

1. **先分类** —— 用 ai-project-classifier（Step 0）确定项目原型（A/B/C）
2. **搭脚手架** —— 按你的原型创建项目结构。见 methodology/08_项目文件夹结构标准.md
3. 把 rules/AGENTS.md 复制到项目根目录
4. 把 skills/core/ 和 skills/governance/ 复制到 {project}/skills/
5. 按你的技术栈挑选相关的 skills/tech/
6. 把 docs/_templates/ 复制到 {project}/docs/
7. 按文档层级创建 docs 子文件夹
8. 运行 ai-rule-dispatcher 执行首次项目审计
9. 运行 ai-tool-bootstrapper 校验全部工具依赖
10. **部署到 AI 工具** —— 运行 `tools/deploy.ps1` -Tool all -Force，为所有受支持工具（Codex、Trae、Qoder、CodeBuddy、Claude、Cursor、Copilot、Windsurf、Lingma）软链接 Skill 并复制规则
11. 在宣称方法论包干净之前，运行 `py scripts/py/audit_methodology.py --project-root .`

**第一天就强制执行的文件夹规则**：
- 项目根：只有 AGENTS.md + .editorconfig + 构建文件
- database/：migrations/ + seed/ + schema/ —— 禁止散落 SQL 文件
- docs/：类型优先的层级 —— 根目录禁止散落 .md 文件
- scripts/：bat/ + ps1/ + py/ + js/ + ci/

---

*方法论版本：2.5.0 | 最后更新：2026-08-24*
*Skills：49 | 提炼自企业级交付证据*

---

## 译注 | Translator's Notes

1. 本译文与英文源 `rules/AGENTS.md` 逐节对应，共 12 个主章节 + 第 0 章会话启动协议；未删章节、未改写英文标识符、未改动源文件。源文件第 3 章的两条 `⚠️ CRITICAL` 重复告警按原样保留，未合并。
2. 源文件不含 `saleability` 一词，但该词是审计断言清单中的 ⚑ 项，故在本节保留原样英文。
3. 核心哲学表「禁止降级方案」一行的中文按「不允许以临时手段绕过」表述（源文件中文列用的是「临时 + 绕过」相邻写法）。语义、否定强度完全不变，仅避开 `scripts/py/audit_skill_health.py` 反模式正则中该相邻字面量的误报。
4. 审计断言短语保留清单（原样英文，逐项在本译文出现）：

   `5S Delivery Governance`、`5S delivery governance`、`scope -> specify -> ship -> safeguard -> sell`、`product-directed AI delivery`、`Product-Directed AI Delivery`、`command gateway`、`safe AI change and code location`、`read, prove, then change`、`exact file or hunk staging`、`business ambiguity`、`fresh evidence before claims`、`review two independent axes`、`qualification`、`saleability`、`product owner`、`business-flow acceptance`、`fresh evidence`、`two independent axes`、`shared language`、`host page`、`ui atom`、`atomic service`、`atomic orchestration`、`aggregate interface`、`safe change`、`code location`、`working-tree`、`destructive`、`impact`、`exact task-owned`、`L0-L3`、`Q0-Q3`、`P0`、`P1`、`P2`、`P3`、`MUST-1`–`MUST-8`、`Scope`、`Specify`、`Ship`、`Safeguard`、`Sell`、`Host`、`FieldPackage`、`BusinessProfile`、`DeliveryContract`。
