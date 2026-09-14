# governance 层 13 个 Skill 中文详解 | Governance Layer Skills

> **源文件**：skills/governance/*/SKILL.md、skills/SKILL_MANIFEST.json
> **源版本**：SKILL_MANIFEST.json updatedAt 2026-07-28
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：Skill 名、路径、门禁代号保持英文；本文件为中文摘要（正文中文版见 50_Skill正文中文版/governance/）。

---

## 0. 一览表

| Skill | 层 | 中文名 | 一句话职责 | 何时加载 |
|---|---|---|---|---|
| `ai-single-truth-enforcer` | governance | 唯一真相源治理 | 后端持有真相与业务逻辑，前端纯展示；通知必须匹配分级 | 一切前端与前后端分工工作 |
| `ai-atomic-governance` | governance | 原子系统架构治理 | 声明与执行器分离、L0–L5 分层、执行器强制接入治理、反模式检测 | 审计或建设原子系统、新增原子、给既有执行器补治理 |
| `ai-domain-boundary-mapper` | governance | 领域边界与对象归属映射 | 每个对象只有一个归属领域，跨域访问必须显式且可追溯 | 数据、身份、权限、单据、报表跨模块时 |
| `ai-field-package-governor` | governance | 字段元数据与组件配置治理 | 页面不拥有字段真相，字段真相走 DB → 元数据 → 组件配置链 | 加列、改表单/表格字段、集中元数据、审计硬编码字段 |
| `ai-component-standardizer` | governance | 页面与组件模板标准化 | 每个企业页面必须落入四类标准模板之一，主题只改变量不改布局 | 一切页面开发与模板合规审查 |
| `ai-ui-ux-governor` | governance | 企业级 UI/UX 设计系统治理 | 操作页是行动优先界面，密度、四态、零废话、主题令牌统一 | UI 一致性评审、页面设计评审 |
| `ai-frontend-audit` | governance | 前端质量与可用性审计 | 六维度静态审计前端可用性、完备性、一致性、性能、错误态、无障碍 | 提 PR、截图、发布前；页面存在但可能不可用 |
| `ai-runtime-verify` | governance | 浏览器运行时验证 | 无头浏览器实地验证控制台、加载遮罩、DOM、API，产出证据 JSON | 每次前端改动后、宣布 complete 之前、部署或重启服务后 |
| `ai-flow-closure-audit` | governance | 端到端业务流程闭环审计 | 逐层核对入口→API→服务→数据库→参数→回写→报表是否闭环 | 宣布业务流程完成前、检查端到端就绪度 |
| `ai-cross-project-audit` | governance | 跨项目治理审计流水线 | 用 A 项目的原子治理体系审计 B 项目代码库，默认只读 | 跨项目审计、复用既有审计数据出证据链 |
| `ai-brownfield-analyzer` | governance | 老项目分析与模式提炼 | 先审计再改动：审计现状、定干预级别、提炼模式、出外科手术式计划 | 首次进入任何存量项目；迁移、接管、继承半成品 |
| `ai-reference-researcher` | governance | 参考实现驱动的研究 | 不熟悉领域先找一手参考与开源实现，提炼模式再设计 | 新领域、标准可能变化、需要成熟外部实践 |
| `ai-competitor-analyst` | governance | 竞品对标与市场调研 | 以真实产品行为而非营销材料做对标，分离事实、推断与选择 | 市场分析、产品策略、定价、功能对比 |

---

## 1. `ai-single-truth-enforcer` — 唯一真相源治理

- **源文件**：`skills/governance/ai-single-truth-enforcer/SKILL.md`
- **成熟度**：verified

**用途**：确立并强制一条根本规则——唯一真相源（single source of truth）：**前端纯展示，后端决策**。所有业务逻辑、校验、计算、数据转换必须落在后端；UI 只是渲染层，仅此而已。要解决的问题是：智能体习惯把业务逻辑写进 Vue 组件、在 JavaScript 里算价格、只做客户端表单校验、把数据转换和渲染混在一起，一旦同一逻辑要跑在移动端、微信端或 MCP 端就整体崩塌。

**触发条件**：一切涉及前后端职责划分的工作；校验、计算、权限、状态流转、共享业务规则的实现或评审；前端代码审计；`ai-frontend-audit` 的审计维度扩展。

**核心规则**（`## The Prime Directive` 与 `## Rule` 完整译出）：

`## The Prime Directive`（最高指令）：

```text
前端 = 纯展示（FRONTEND = DISPLAY ONLY）
后端 = 唯一真相源（BACKEND = SOLE SOURCE OF TRUTH）

绝不：在 UI 层做计算、校验、转换或决策
始终：取数、展示、回传
```

**Rule 1：前端零业务逻辑。** 以下事项**必须（MUST）**只在后端实现，UI 层**禁止（MUST NOT）**承担：

| 关注点 | 后端职责 | UI 层禁止 |
|---|---|---|
| 计算 | 价格计算、税费、折扣、合计 | `computed(() => price * quantity)` |
| 校验 | 业务规则（信用额度、库存检查、重复检测） | `if (amount > 10000) show error` |
| 数据转换 | 格式化、单位换算、区域化格式 | 携带业务逻辑的 `date.toLocaleDateString()` |
| 授权 | 权限检查、基于角色的访问 | `v-if="user.role === 'admin'"`（应改用后端返回的权限） |
| 状态机 | 订单状态、工作流流转 | `if (status === 'pending' && ...)` |
| 业务决策 | 依据状态决定显示哪些字段 | 由后端状态标志驱动的条件渲染 |

UI 层**可以（MAY）**做：基于后端返回数据做 `v-if`；用 `v-for` 遍历后端返回数组；仅供展示的 `toLocaleDateString()`（绝不用于计算）；事件绑定后把数据回传后端 API；客户端路由与导航。

**Rule 2：数据唯一真相。** 层次为：Level 1 `DATABASE` 终极真相（规范取值）；Level 2 `BACKEND API` 计算真相（价格、状态、权限）；Level 3 `FRONTEND STATE` 仅展示副本，**永不是权威**。本 Skill 检出的违规包括：前端算价格、前端校验业务规则、同一字段在 2 个以上组件里用不同逻辑重复定义（duplicate truth sources）、展示前在前端改写数据。

**Rule 3：通知分级策略。** 通知**必须**匹配严重度，不得出现"需要确认却只闪一个轻提示就消失"。分级原样为 **`P0=Modal`、`P1=Banner`、`P2=Toast`、`P3=Console`**：

| 级别 | 名称 | 通知形式 | 示例 | 用户动作 |
|---|---|---|---|---|
| **P0** | 严重／破坏性 | **Modal** | 删除全部数据、变更套餐、不可逆操作 | 显式确认或取消 |
| **P1** | 重要／需行动 | **Banner**（常驻）或带操作按钮的 Modal | 支付失败、会话过期、权限不足 | 必须知悉或处理 |
| **P2** | 信息／成功 | **Toast**（4–6 秒自动消失，可选撤销） | 保存成功、文件已上传、设置已更新 | 可选：超时内撤销 |
| **P3** | 调试／瞬时 | **Console** 或静默 | API 调用成功、缓存已更新 | 无需动作 |

反模式对照：删除确认用一闪而过的轻提示 → 必须改为带显式"删除"按钮的 Modal；保存失败一闪而过 → 必须改为带"重试"的常驻横幅；保存成功却用 Modal 挡住屏幕 → 必须改为自动消失的轻提示；每个表单字段变化都问"确定吗" → 只对破坏性或高成本操作确认。

**审计/验证维度**（`## Audit Checklist`）：无携带业务公式（价格、税费、折扣、合计）的 `computed()`；无携带业务规则（信用额度、库存、资格）的 `if/else`；所有校验调用走后端 API 而非本地函数；所有数据转换在后端完成后才下发；权限检查使用服务端返回的权限而非本地角色字符串；删除等破坏性操作使用 Modal 确认，**禁止**用 Toast；保存错误使用常驻通知，**禁止**闪退式轻提示；成功事件使用 P2 轻提示而非 Modal。

**输出格式**：审计清单勾选结果 + 逐条违规定位（违规模式 → 正确写法），按 `P0`/`P1`/`P2` 分级；集成关系表说明 `ai-frontend-audit`、`ai-atomic-architect`、`ai-runtime-verify`、`ai-component-standardizer` 各自的消费方式。

**防护规则**：能在后端做的，**必须（MUST）**在后端做；前端状态是缓存，**永不是**权威；通知匹配严重度——严重用 Modal、信息用 Toast、调试用 Console；无静默失败，每个错误**必须**按正确分级暴露给用户；一个概念一个真相，同一个业务取值**禁止**在两地各算一次。

---

## 2. `ai-atomic-governance` — 原子系统架构治理

- **源文件**：`skills/governance/ai-atomic-governance/SKILL.md`
- **成熟度**：callable

**用途**：强制原子系统纪律——每个原子是纯声明（declaration），每个执行器（executor）可独立测试，每个执行器都接入治理。要防的是原子系统最常见的失效模式**分层衰减（layered decay）**：底层 L0 严格遵守模式，上层 L2/L3 却退化成"逻辑写在声明上"的反模式。典型问题是：把业务逻辑直接写在 `DeclarationAtom` 类上、把执行器写成单体大文件、跳过治理接入、L0 与 L3 模式混用不一致。

**触发条件**：审计或建设原子系统时；新增原子时；把治理接入既有原子执行器时（`description` 明示 "Use when auditing or building atomic systems, adding new atoms, or integrating governance into existing atom executors"）。源文件未提供独立的 `## Trigger` 小节。

**核心规则**（`## The Prime Directive` 完整译出）：

```text
声明（DECLARATION） = 只有契约（schema、meta、relations）
执行器（EXECUTOR）  = 全部业务逻辑（可测试、可替换）
治理（GOVERNANCE）   = 每个执行器上的强制参数

绝不：在 DeclarationAtom 上写 run()
始终：每个原子一个独立执行器文件
```

**Rule 1：声明与执行器分离（P0）。** `DeclarationAtom` **必须**包含：`_atom_name`、`_atom_provider`、`_atom_category`、`meta`（含 name、level、description、tags、version、lifecycle 的 `AtomMeta`）、`input_schema`、`output_schema`、`provider`、`category`。`DeclarationAtom` **禁止（MUST NOT）**包含：带业务逻辑的 `run()` 方法；对 service、store 或外部 API 的直接导入；构造业务对象的 `__post_init__`；`@dataclass` 装饰器（应使用标准类继承）。

**Rule 2：治理接入（P0）。** 每个执行器**必须**：1) 接受 `governance=None` 参数；2) 在入口调用 `governance.classify(action="...")`；3) 在**每一条**返回路径上返回 `evidence_id`；4) 处理 `auto_reject` 决策分支。守卫模板：

```python
def execute(self, ..., governance=None):
    if governance:
        result = governance.classify(action="atomic_execute")
        if result.get("decision") in ("auto_reject",):
            return {"evidence_id": f"ev_{uuid4().hex[:12]}",
                    "error": "Governance denied"}
    # ... normal execution
```

**Rule 3：原子分层（P1）。** `L0` Base Atom（纯函数、零外部依赖）、`L1` Operator（调外部 API/库）、`L2` Composite（编排 L0/L1 原子）、`L3` Domain App（完整业务场景）、`L4` Terminal（对外部世界的副作用）、`L5` Application（把 L3+L4 组合成工作流）。**关键规则**：上层**必须**通过执行器委托组合下层，**禁止**复制逻辑。

**审计/验证维度**：`L0`–`L5` 层级匹配；三类反模式检测——AP1 分层衰减（声明上带 `run()`、缺治理，用 `app_governance_orchestrator` 配 `audit_types=["code"]` 检出）、AP2 单体执行器文件（单文件 500 行以上含 18 个以上执行器类）、AP3 治理缺口（执行器功能正常但缺 `governance=` 参数，无法接入 L5 编排）；汇总的 `## Verification Checklist` 要求在宣布原子系统"已治理"前逐项勾选：所有 `DeclarationAtom` 纯净（无 `run()`、无业务导入）、每个执行器有 `governance=None`、每个执行器返回 `evidence_id`、所有原子匹配声明的 `L0`–`L5` 级别、`DeclarationAtom` 子类上无 `@dataclass`、原子目录无死文件、测试覆盖完整含治理集成测试、`L5` `app_governance_orchestrator` 能消费全部原子。

**输出格式**：审计运行的 `code` 审计结果（检出带 `run()` 与缺治理的原子清单）、反模式归类、修复动作（抽出执行器、补 `governance=None`、给返回值加 `evidence_id`）；批量治理注入使用基于 AST 的 `GovernanceInjector`（`ast.NodeTransformer` 访问 `execute` 方法，追加 `governance` 参数与守卫语句，再 `ast.unparse`）。案例记录格式为「Before / After / Key metric」，例如数字生命治理整改：21 个原子从 0 治理接入到 21 个接入，15 个新治理测试，151 个测试 0 失败。

**防护规则**：源文件未提供 `## Guardrails` 小节；其约束强度由 `## The Prime Directive`、`Rule 1`、`Rule 2`（均标 P0）与 `## Verification Checklist` 承担——声明上**禁止**写 `run()`，每个执行器**必须**接受并调用治理。

---

## 3. `ai-domain-boundary-mapper` — 领域边界与对象归属映射

- **源文件**：`skills/governance/ai-domain-boundary-mapper/SKILL.md`
- **成熟度**：verified

**用途**：在**对象级**映射领域边界。回答五个问题：每个身份概念归哪个领域？每个主数据对象归哪个领域？每张业务单据归哪个领域？每张平台/共享表归哪个领域？每个动作的写回（writeback）目标是谁？本 Skill 只做领域边界映射，不做实现，也不从零做架构设计。

**触发条件**：数据、身份、权限、单据、报表或业务对象跨模块边界时；新增跨域写回时；审计多个领域直接写同一张表时。源文件未提供独立的 `## Trigger` 小节。

**核心规则**（`## Rule` 完整译出）：**每个对象（表、服务、API）只有一个归属领域。跨域访问必须显式且可追溯。** 边界模板按四类对象组织：身份与租户（User、Tenant、Organization、Role，标注 Owner 与 Access Pattern，例如"Shared — read by all, write by [Domain]"）；主数据（Product、Customer、Supplier、Warehouse，标注 Owner 与只读消费者）；业务单据（Sales Order、Sales Delivery、Purchase Order、Purchase Receipt，标注 Owner 与 Writeback Targets，例如"Inventory（decrease）、Finance（COGS）"）；平台表（System Parameters、Audit Log、File Storage、Notifications）。

**审计/验证维度**（`## Mapping Workflow` 四步 + 第四步的违规清单）：Step 1 盘点范围内的所有表、服务、API；Step 2 按"哪个领域创建/更新权威记录、哪个领域定义校验规则、哪个领域触发状态流转"确定唯一归属领域；Step 3 为每个业务动作追踪「源对象 → 写回动作 → 目标对象」，并验证目标领域确有该写回的消费者；Step 4 标记违规：多个领域直接写同一张表、入口层（前端）承载业务规则、缺失写回消费者、循环写回依赖。常见领域模式用于判定：Shared-Read, Single-Write、Event-Driven Writeback、Anti-Corruption Layer、Shared Kernel。

**输出格式**：领域边界模板 Markdown 表（Identity & Tenant / Master Data / Business Documents / Platform Tables 四张表，列固定为 Object、Owner、Access Pattern 或 Consumers 或 Writeback Targets 或 Notes）；违规清单；对象归属结论。

**防护规则**：**禁止**仅凭命名把对象分配给某个领域，必须核对真实代码归属；**禁止**允许多个领域在没有显式治理的情况下写同一张表；**禁止**跳过写回路径验证；**禁止**建立与真实代码不符的领域边界；**禁止**把共享表当成"无归属"——每张表都有归属。

---

## 4. `ai-field-package-governor` — 字段元数据与组件配置治理

- **源文件**：`skills/governance/ai-field-package-governor/SKILL.md`
- **成熟度**：verified

**用途**：治理企业系统中的字段元数据层——把数据库模式连到 UI 组件的基础设施。覆盖：字段真相源层次（DB → 元数据 → 组件配置）、组件复用与组合强制、字段配置治理（可见性、校验、排序）、由元数据生成报表、页面个性化作为配置层而非主定义。适用于 ERP、CRM、SaaS admin、运营工具等"页面展示数据库结构化数据且字段定义必须集中而非逐页重复"的系统。

**触发条件**：新增列时；修改表单/表格字段时；集中字段元数据时；审计页面硬编码字段时；新增报表字段时。

**核心规则**（`## Rule` 完整译出）：**页面不拥有字段真相（The page does not own the field truth）。** 字段真相按四层流动：

| 层 | 职责 | 示例 |
|---|---|---|
| **Database** | 结构真相 | 列类型、约束、可空性 |
| **Field Metadata** | 业务真相 | 标签、校验规则、多语言名称 |
| **Component Config** | 展示真相 | 可见性、排序、宽度、必填状态 |
| **Page Personalization** | 用户偏好 | 保存的筛选器、列顺序、隐藏字段 |

UI 层**必须**接收 `businessCode` 或 `entityKey`，从元数据层消费字段；**禁止**在单个页面里硬编码字段名、标签或列定义。违规判定：同一字段标签出现在 3 个以上页面文件里，它就该进元数据层，而不是留在各页面。

**审计/验证维度**：四类配置来源核对——① Database-First（先核对真实模式：列存在、类型匹配、约束正确，来源 `DESCRIBE table` / `SHOW COLUMNS`）；② Metadata Registry（字段键匹配 DB 列、多语言标签、数据类型与格式、校验规则、默认值、关联映射如外键→选择器）；③ Component Binding（标准 CRUD 页用 `businessCode`、领域专用组件用 `entityKey`、报表分析页用 `reportCode`）；④ User Personalization（显隐可选字段、重排列、保存筛选预设、调整列宽，且不得破坏真相）。组件复用模式的验收点：新增一个数据库列**只**更新元数据注册表，所有消费该实体的页面**必须**自动反映变化，**不需要**改任何一个页面文件。报表生成模式：注册数据集（源表、字段白名单、维度、指标）→ 注册元数据（自动导入关系字段）→ 共享报表组件接收 `reportCode` 动态渲染 → 权限由后端报表引擎控制而非前端组件。文档身份模式：一个物理实体承载多个业务身份时，为每个身份注册正式实体类型与元数据别名，按身份而非表名路由决策，各自拥有编号、权限、字段可见性规则，复用共享组件并锁定/隐藏与身份无关的字段。

**输出格式**：字段真相源层次表；配置来源核对结果；组件复用对照表（"If you need to… / Use… / NOT…"）；报表生成与文档身份的落地步骤；新增/修改字段的标准工作流输出。

**防护规则**：**禁止**在单个页面里硬编码字段标签；**禁止**把页面个性化配置当成主字段定义；**禁止**只加数据库列而不在元数据层注册；**禁止**为同一字段建立第二真相源；**禁止**为"快速修复"绕过元数据——它会变成永久债务；**禁止**在同一实体的多个页面间重复筛选/列/表单逻辑。

---

## 5. `ai-component-standardizer` — 页面与组件模板标准化

- **源文件**：`skills/governance/ai-component-standardizer/SKILL.md`
- **成熟度**：verified

**用途**：为前后端定义并强制标准化的组件与页面模板，阻止智能体给每个新页面重新发明布局。每个列表页长得一样，每个表单页遵循同一模式，每个报表页使用同一结构；主题支持客户级定制而**不破坏**标准。要解决的问题是：各页面各写一套布局、按钮位置不一、字段排布不一，一个客户看到侧边栏表单、另一个看到 Modal，一个列表页搜索框在顶部、另一个在底部——那是混乱，不是产品。

**触发条件**：创建或评审资料列表页、单据录入页、报表页、看板及企业级前端组件时；页面代码生成前的模板选型；发布前的模板合规审查。

**核心规则**（`## Rule` 完整译出）：标准化**必须**：1) 对照设计系统检查；2) 校验 API 一致性；3) 保证可访问性（a11y）；4) 检查是否已有替代实现；5) 在组件目录中登记。**禁止**创建未标准化的组件。

**前端组合主链**（`## Frontend Composition Spine`）**必须**遵循同一条链：

```text
backend runtime / field metadata / aggregate profile
  -> UI atoms
  -> UI orchestration
  -> standard page template
  -> Host page
```

分工与禁令：`ui atom` 负责聚焦可复用的 UI 行为（字段渲染器、选择器、表格、状态、操作栏、筛选、汇总、对话框），**禁止**承载业务策略、计算事实、授权命令；UI orchestration 从后端事实组合原子，协调加载、本地输入、导航、无障碍与反馈，**禁止**自建第二套业务状态机或命令路径；standard template 提供稳定的 list/document/report/dashboard/settings 外壳，**禁止**重建页面级局部布局系统；`host page` 绑定业务 code/profile、选模板、装配受支持的原子与插槽，**禁止**重复字段、权限、状态、计算或后端 `command gateway` 逻辑。`Host` 是组合面，不是业务服务；只有后端 aggregate/runtime 契约标记某命令可用时 `Host` 才能显示该命令，所有写入**必须**发往后端 `command gateway` 或归属 API 路径。

**四类页面模板与布局契约（完整写出）**：

**Template 1：资料列表页（List/Table Page）**——展示可搜索、可筛选的记录列表并带 CRUD 操作。布局契约（**必须**遵循）：Filter Bar（`Search Input` + `Filter Dropdown` + `Date Range`）→ Toolbar（`+ New` / `Batch Delete` / `Export` / `Refresh`）→ Table（列：ID、Name、Status、Date、Actions）→ Pagination（`[<] [1] [2] [3] … [>]` + `Showing 1-20 of 156`）。组件契约：Filter Bar 用 `SearchInput` + `FilterDropdown[]` + `DateRangePicker`（props：`searchPlaceholder`、`filters`、`onSearch`）；Toolbar 用 `ActionButton[]`（`label`、`icon`、`onClick`、`variant`）；Table 用带 `columns[]` 的 `DataTable`（`data`、`loading`、`emptyText`、`onRowClick`）；行操作用 `RowActions`（`actions[]` 含 `icon`、`label`、`onClick`、`visible`）；分页用 `Pagination`（`current`、`total`、`pageSize`、`onChange`）。后端契约：每个列表页接口返回固定形状 `{ "data": [...], "total": 156, "page": 1, "pageSize": 20 }`。

**Template 2：单据录入页（Document/Form Page）**——以表头信息 + 行项目 + 底部操作创建或编辑单条记录。布局契约：Navigation（`← Back to List`）→ Document Header（Header Fields：`Doc No: [Auto]`、`Date: [Picker]`、`Customer: [Select]`、`Status: [Tag]`）→ Line Items（行项目表：Item、Qty、Price、Amount、Actions，附 `[+ Add Line]`）→ Summary Bar（`Subtotal / Tax / Total`）→ Footer（`[Save Draft] [Submit] [Cancel]`，pinned）。关键规则：底部操作按钮**必须**钉在底部（pinned to bottom）且始终可见；汇总条**必须**由后端实时更新，**禁止**在前端计算；行项目**必须**内联增删，不用独立 Modal。

**Template 3：报表页（Report/Analytics Page）**——展示聚合数据与图表并支持导出。布局契约：Filter Bar（`[Date Range] [Dimension] [Metric] [Generate]`）→ View Toggle（`[Table View] [Chart View] [Export]`）→ Summary（`Summary Row: Total / Avg / Max`）→ Main Content（图表或表格内容）→ Footer（`This report generated: …`）。

**Template 4：看板（Dashboard/Workbench）**——展示聚合指标与快捷动作的落地页。布局契约：Summary Cards（Card 1–4，各含一个 Metric）→ 下方两栏：`Recent Items Table`（与列表页同构）+ `Quick Actions`（`[+ New Order]`、`[+ New Invoice]`、`[View Reports]`）。

**主题系统**：不同客户需要不同视觉主题，模板结构保持不变，只改 CSS 变量。**主题变量契约**要求每个模板组件**必须**使用 `--theme-*` 变量，**禁止**硬编码颜色，可用变量族包括 `--theme-primary`、`--theme-primary-hover`、`--theme-danger`、`--theme-success`、`--theme-warning`、`--theme-bg`、`--theme-surface`、`--theme-border`、`--theme-text`、`--theme-text-secondary`、`--theme-radius`、`--theme-font`、`--theme-density`（`compact | comfortable | spacious`）。客户主题文件只覆盖其需要的变量。

**审计/验证维度**（`## Enforcement`）：页面是否有 filter bar（查 `.filter-bar` 或 `SearchInput`）；表格是否使用 `DataTable`（查 `<DataTable` 或标准表格组件）；工具条是否匹配模板（按钮顺序 **必须**为 New → Batch → Export → Refresh）；表单是否有 pinned footer（查 footer 上的 sticky bottom）；汇总是否由后端计算（查行项目中无 `computed()`）。违规修复对照：搜索栏在表格下方 → 移到顶部（工具条之前）；保存按钮未 pinned → 加 sticky bottom；报表缺汇总行 → 补后端聚合的汇总行；组件内硬编码颜色 → 替换为 `var(--theme-*)`；自建表格替代 `DataTable` → 换回标准 `DataTable`。

**输出格式**：模板类型声明（list / document / report / dashboard，**必须**显式声明）；布局契约与组件契约对照；后端返回契约（列表页固定四字段形状）；主题变量覆盖清单；违规与修复对照表。**模板豁免**：模板对 AI-Native 与企业级项目是强制的（MANDATORY）；对快速原型（Archetype A）只是建议；对老项目既有页面应匹配原有模式；对老项目中的**新**页面应沿用该项目既有页面模式而非方法论模板；对一次性工具页（如 admin 调试面板）可自由形式。

**防护规则**：每个页面**必须**声明其模板类型（list、document、report、dashboard）；模板结构不可协商——客户主题只改颜色不改布局；后端计算、前端展示，汇总与计算字段**必须**来自 API；一个角色一个组件，**禁止**因为"略有不同"就再造一个 `DataTable2`；要么主题变量、要么什么都没有，**禁止**任何位置出现硬编码颜色；`Host` 不是第二个后端——它只组合受支持的 `ui atom` 并调用权威的 aggregate/command 契约。

---

## 6. `ai-ui-ux-governor` — 企业级 UI/UX 设计系统治理

- **源文件**：`skills/governance/ai-ui-ux-governor/SKILL.md`
- **成熟度**：verified

**用途**：治理企业应用跨页面 UI/UX 一致性，覆盖：布局分类强制、密度与间距一致、状态处理（加载、空、错误、边界）、面向操作工具的行动优先表达、主题与令牌治理、性能 UX 标准。本 Skill 管的是设计系统，不是像素级设计，适用于 ERP、SaaS admin、运营看板及一切数据密集型企业工具。

**触发条件**：设计与评审 ERP/SaaS/admin 页面、表单、看板、报表与操作工作流时；UI 一致性评审；视觉变更合并前。

**核心规则**（`## Rule` 完整译出）：**企业操作页是行动优先界面，不是营销页。** 工具条、操作、状态指示与数据**必须**排在说明性文字之前；业务含义**必须**通过控件与结构表达——按钮、状态标签、流程链接——而不是散文段落。

**布局分类**：每个企业页面**必须**落入一类且带规定的布局倾向——**List / History**：filter bar + toolbar + table + batch actions + drilldown；**Document / Form**：header fields + line items + summary + pinned footer actions；**Report / Analytics**：dimension tabs + default table + chart toggle + summary row；**Workbench / Dashboard**：summary cards + todo list + quick actions；**Settings / Parameters**：grouped fields + toggles + defaults + compact help。违规判定：列表页出现 hero banner，或设置页出现多段解释文字，即为用错布局模式。

**零废话规则**：ERP、SaaS admin、运营工具**必须**移除一切不直接帮助完成任务的文案。删除：欢迎语、营销文案、占位帮助文字、"如何使用本页"区块、功能描述、页面级教程。保留：字段标签、校验规则、内联 tooltip、约束提示（如编码规则）、操作按钮、状态指示。例外：登录页与对外门户可带简短品牌/信任文案，该例外**不扩展到**内部操作页。

**状态处理**：每个数据驱动视图**必须**显式处理四态——**Loading**（稳定容器内的骨架屏或 spinner，数据拉取中）、**Empty**（情境化空状态插画 + 可选 CTA，无数据时）、**Error**（错误信息 + 重试动作，拉取或动作失败时）、**Edge Cases**（优雅处理：超长文本、空值、特殊字符）。规则：ERP 表格**禁止**逐行加载骨架或错峰动画，整表**必须**用同一个稳定加载态。

**密度标准**：企业操作页**必须**默认紧凑密度——页面内边距约 4px、区块间距约 3px、工具条按钮高约 26px、表格操作按钮约 22px、筛选/搜索按钮约 24px、分页间距约 4-6px。页面外壳（list、document、report 模板）**必须**通过共享令牌强制这些值，**禁止**页面级 CSS。

**表格视区规则**：每个数据表**必须**吃满可用页高——表体拥有纵向滚动；主要操作与分页钉在底部；底部顺序为 横向滚动条 → 汇总行 → 分页；表格合计放在底部区域并与列对齐；**禁止**用悬空右下角统计块替代列对齐合计。验收要求验证四态：少行、多行、多列带横向滚动、分页与汇总同时存在。

**主题治理**：所有视觉值**必须**来自 CSS 变量而非硬编码；**禁止**页面级覆盖——为品牌或主题令牌写页面级 CSS 属于违规；视觉变更合并前**必须**验证所有受支持主题；滚动条样式**禁止**使用硬编码颜色，**必须**用主题令牌。**性能 UX**：**必须**先做服务端分页再加列；**必须**批量 API 调用替代逐行请求；大列表（>100 行）**必须**虚拟滚动；加载/重试/轮询**禁止**产生并发重复请求；长表单**必须**拆分为编排、行表格、汇总。

**通知分级策略**（与 `ai-single-truth-enforcer` 一致）：每个面向用户的通知**必须**匹配其严重度，错误分级会摧毁信任并造成数据丢失。`P0` Critical/Destructive → **Modal** 带确认/取消，**永不**自动消失（删除全部记录、不可逆操作、套餐变更）；`P1` Important/Action Required → **Persistent banner** 或带操作按钮的 Modal，**永不**自动消失（支付失败、会话过期、同步错误）；`P2` Informational/Success → **Toast** 可选撤销，4–6 秒（保存成功、文件已上传）；`P3` Debug/Transient → Console 日志或静默。反模式：删除全部后用轻提示报"Deleted"（P0 动作 → P2 通知）应改为 Modal 确认；保存失败一闪而过（P1 → P2）应改为带 `[Retry] [Details]` 的常驻横幅；每个输入都弹确认框（P2 动作 → P0 通知）应静默保存；表单校验错误闪提示（P1 → P2）应改为字段下常驻内联错误。实现契约要求通知系统暴露 `modal(config): Promise<boolean>`（P0，返回用户选择）、`banner(config): { dismiss(): void }`（P1，常驻可关闭）、`toast(config): void`（P2，自动消失）、`debug(message): void`（P3，仅控制台）。

**审计/验证维度**（`## Standard Workflow`）：1) 页面分类——属于哪类布局；2) 找出违规——零废话、密度、状态处理、表格视区；3) 核对密度数值是否达到紧凑标准；4) 验证四态（loading、empty、error、edge cases）；5) 提出改动建议——**必须**是增量的、基于共享组件的，**禁止**页面级重写。

**输出格式**：页面类型判定；违规清单（按零废话/密度/状态/视区分类）；密度测量对照；四态验证结果；增量改动建议清单；主题令牌与性能 UX 核对结果。

**防护规则**：**禁止**用同一套布局模板套所有页面类型；**禁止**用页面级 CSS 解决布局问题——**必须**修共享外壳；**禁止**给 ERP 页面加装饰性文案（零废话规则）；**禁止**在数据密集页的表格加载上使用动画；**禁止**在页面 CSS 里硬编码滚动条、hover 或主题颜色；**禁止**为页面级品牌覆盖主题令牌。

---

## 7. `ai-frontend-audit` — 前端质量与可用性审计

- **源文件**：`skills/governance/ai-frontend-audit/SKILL.md`
- **成熟度**：verified

**用途**：跨全部关键维度系统性审计前端模块质量：**可用性**（每个菜单项与路由是否无错渲染）、**完备性**（所有声明字段是否存在且可用）、**一致性**（页面是否统一遵循设计系统）、**性能**（加载时间、渲染问题、阻塞操作）、**错误态**（加载、空、错误、边界是否处理）、**无障碍**（键盘导航、屏幕阅读器、对比度）。本 Skill 只做前端质量审计，不做功能实现，也不等同于代码评审。

**触发条件**：提 PR 前、截图前、发布前；当页面"存在但可能不可用"时；`description` 明示 "Use before PRs, screenshots, releases, or when a page exists but may not be usable"。源文件未提供独立的 `## Trigger` 小节。

**核心规则**（`## Rule` 完整译出）：前端审计**必须**：1) 检查页面加载指标；2) 运行无障碍审计；3) 测试响应式断点；4) 扫描控制台错误；5) 与视觉基线对比。**禁止**在前端审计未通过的情况下部署。

**审计/验证维度**（六个维度，括号内为源文件标注的分级）：

1. **可用性（P0）**：每个路由与菜单项**必须**无控制台错误地渲染——所有菜单项导航到正确路由；无空白页或未处理的路由错误；初次渲染无控制台错误；鉴权/权限门控正确生效。
2. **完备性（P0）**：所有声明字段、操作与功能**必须**可用——所有表单字段可渲染并接受输入；所有按钮触发正确动作；所有表格列正确显示数据；所有下拉/选择器填充选项；搜索/筛选功能可用。
3. **一致性（P1）**：页面应在全应用内遵循同一模式——工具条/筛选/表格/表单布局一致；按钮位置（主/次）一致；表单校验行为一致；加载指示一致；空状态展示一致。
4. **性能（P1）**：页面应在可接受阈值内加载与响应——首屏加载 < 阈值 ms；无阻塞式同步操作；大列表使用虚拟化；图片与静态资源已优化。
5. **错误态（P1）**：所有状态**必须**优雅处理——数据拉取时显示加载态；无数据时显示空态；拉取失败时显示带重试的错误态；表单校验错误内联显示；网络错误可恢复。
6. **无障碍（P2）**：基础无障碍**必须**维持——主要操作支持键盘导航；表单输入有关联标签；颜色对比度达到 WCAG AA 最低要求；焦点指示可见。

**输出格式**（`## Audit Output Format`）：报告标题为 `## Frontend Audit Report: [Module Name]`。① Summary 表：`Total Pages | Pass | Warn | Fail | P0 Issues | P1 Issues | P2 Issues`；② Page-Level Results 表：`Page | Route | Availability | Completeness | Consistency | Performance | Error States | Accessibility`，单元格用状态符号；③ Issue Details 表：`# | Page | Severity | Dimension | Description | Fix Recommendation`（Severity 使用 `P0`/`P1`/`P2`）。

**审计流程**：1) Inventory——列出范围内全部页面/路由；2) Crawl——在浏览器中打开每个页面验证渲染；3) Inspect——检查控制台错误与网络性能；4) Compare——对照设计系统参考页检查一致性；5) Score——为每条发现定级（`P0`/`P1`/`P2`）；6) Report——产出结构化审计报告与修复建议。

**防护规则**：**禁止**只看代码就审计——**必须**在浏览器中打开真实页面；页面抛控制台错误时**禁止**标记为"可用"；**禁止**跳过空态/错误态验证；**禁止**把"看起来还行"当作通过——**必须**用真实数据验证；**禁止**在没有参照（设计系统标准页）的情况下审计。

---

## 8. `ai-runtime-verify` — 浏览器运行时验证

- **源文件**：`skills/governance/ai-runtime-verify/SKILL.md`
- **成熟度**：verified

**用途**：在宣布开发完成前，于真实浏览器中自动验证前端页面渲染正确。本 Skill 是**可由 AI 执行**的——它运行无头浏览器（headless browser）检查，无需人工介入。要解决的问题是：智能体常仅凭静态代码分析就宣称"完成"，而页面实际上有运行时错误（`ReferenceError`、加载 spinner 卡死、白屏、无限刷新）。本 Skill 补上这个缺口。

**触发条件**：每次前端代码改动之后（`src/**/*.html`、`src/**/*.vue`、`src/**/*.jsx`、`src/**/*.tsx`）；任何"done / complete / finished"声明之前；`ai-frontend-audit` 完成静态分析之后；服务重启或部署之后。

**核心规则**（`## Rule` 完整译出）：运行时验证**必须**：1) 执行真实代码路径；2) 捕获输出/错误/日志；3) 对照预期行为校验；4) 检查副作用（DB、文件、API）；5) 记录证据。**禁止**在没有运行时证明的情况下声称可用。

**审计/验证维度**（按 `P0`/`P1`/`P2` 分级）：

**P0 —— 必须通过（失败即页面已损坏）**，六条判据：

| 判据 | 验证内容 |
|---|---|
| **No console errors（0 控制台错误）** | `console.error` 或未捕获异常**必须**为零 |
| **Loading overlay disappears（加载遮罩移除）** | 任何 `.loading-overlay.active` 或类似遮罩**必须**在超时内被移除 |
| **Core DOM renders（DOM 已渲染）** | 关键元素（`#app`、`#board`、主内容区）**必须**存在且可见 |
| **API responses OK** | 页面加载期间的 API 调用**禁止**出现 4xx/5xx |
| **No white screen** | body **必须**有可见文本内容，而不是一列空 div |
| **No infinite refresh** | 页面**禁止**循环刷新（检测连续导航） |

即：**浏览器必须 0 控制台错误、加载遮罩必须移除、DOM 必须已渲染**——三条全部为 `P0`，任一条失败即为页面损坏，**必须**修复后才能继续。

**P1 —— 应当通过（失败则体验降级）**：关键交互可用（主要 CTA 按钮可点击，未被禁用或遮挡）；表单输入可用（首个表单输入可获焦点并接受输入）；标签页切换可用（存在标签页时切换会更新内容）；网络调用完成（所有 fetch/XHR 完成且未挂起）。

**P2 —— 锦上添花**：无布局溢出（视口 <= 1920px 时无横向滚动条）；字体已加载（系统或自定义字体正常渲染，无不可见文字）；无 404 资源（所有 CSS/JS/图片加载成功）。

**输出格式**（`## Usage`）：AI 智能体按如下命令调用：

```bash
node skills/governance/ai-runtime-verify/scripts/verify.js --url http://localhost:3000 --project-root . [--selector "#app"] [--timeout 15000]
```

输出结构化 JSON，顶层字段为 `url`、`passed`、`checks`、`console_errors`、`failed_api_calls`、`screenshot`、`duration_ms`；`checks` 下逐项为 `no_console_errors`、`loading_overlay_removed`、`core_dom_renders`、`api_responses_ok`、`no_white_screen`、`no_infinite_refresh`，每项含 `passed` 与 `details`。仅在全部通过时输出 `passed:true`：

```json
{
  "url": "http://localhost:3000",
  "passed": true,
  "checks": {
    "no_console_errors": { "passed": true, "details": "0 errors" },
    "loading_overlay_removed": { "passed": true, "details": "Removed after 320ms" },
    "core_dom_renders": { "passed": true, "details": "#board visible with 3 columns" },
    "api_responses_ok": { "passed": true, "details": "4/4 API calls returned 2xx" },
    "no_white_screen": { "passed": true, "details": "Page has visible content" },
    "no_infinite_refresh": { "passed": true, "details": "Page stable" }
  },
  "console_errors": [],
  "failed_api_calls": [],
  "screenshot": "/path/to/screenshot.png",
  "duration_ms": 2340
}
```

**方法论位置**：本 Skill 位于开发执行引擎的 **Step 13**：Step 11 Code Implementation（写代码）→ Step 12 Static Audit（`ai-frontend-audit` 查代码质量）→ **Step 13 Runtime Verify（本 Skill 查浏览器行为）** → Step 14 Mark Complete（仅在 Step 13 通过后）。规则：除非 `ai-runtime-verify` 在**最终相关前端或运行时改动之后**运行并返回 `passed: true`，AI 智能体**禁止（MUST NOT）**声称"开发完成"。此前的报告、健康检查端点或智能体报告都不证明当前行为——这即 `fresh evidence` 要求。

**防护规则**：使用 `--project-root` 把证据 JSON 自动归档到 `docs/测试验收报告/`，这是任务完成证明；**必须**对真实运行中的服务执行，**禁止**对 mock 执行；**必须**明确要证明的具体断言，并在最终相关改动后运行能证明它的检查；`P0` 检查失败意味着页面已损坏，**必须**先修复再继续；**禁止**忽略"轻微"控制台错误——每个错误都是真实缺陷；失败时截图以便调试；超时即失败——永不稳定的页面就是坏的。依赖：Node.js >= 18、`playwright` npm 包（含 chromium 浏览器）、目标服务运行中且可访问。

---

## 9. `ai-flow-closure-audit` — 端到端业务流程闭环审计

- **源文件**：`skills/governance/ai-flow-closure-audit/SKILL.md`
- **成熟度**：verified

**用途**：审计一条业务链是否真正闭环——从入口层到 API、到数据库、到下游回写（writeback）、再到报表。本 Skill 检出这些缺口：某个入口动作没有后端校验；某次数据库写入没有下游回写；业务规则只存在于前端代码里；报表查询的是过期或不完整数据；参数/开关未被正确消费。**核心原则**：没有每一层的证据，就**禁止**称一条流程"已闭环"。

**触发条件**：宣布某个业务流程完成之前；需要检查端到端就绪度时；`description` 明示 "Use before declaring a business process complete or when checking end-to-end readiness"。源文件未提供独立的 `## Trigger` 小节。

**核心规则**（`## Rule` 完整译出）：闭环审计检查 5 项：1) 任务有已定义的验收标准；2) 存在完成证据；3) 验证步骤已执行；4) 输出与预期输出一致；5) 无未解决问题残留。**禁止**在没有闭环证据的情况下标记完成。

**审计/验证维度**（`## Audit Layers`：只有**所有**层都有证据，业务链才算"闭环"）：

| 层 | 检查项 | 所需证据 | 缺失时的缺口等级 |
|---|---|---|---|
| **Entry/UI** | 动作可用？校验正确？ | 截图或页面验证 | P2（UX 缺口） |
| **API** | 端点存在？方法/鉴权正确？ | `curl` 测试、API 响应日志 | P0（阻断） |
| **Service/Logic** | 业务逻辑完整？有事务边界？ | 代码评审 + 单元测试 | P0（阻断） |
| **Database** | 表/列正确？约束齐全？ | `DESCRIBE` + `SELECT` 抽样 | P0（阻断） |
| **Parameters/Switches** | 配置被正确消费？ | 参数审计、开关检查 | P1（数据风险） |
| **Writeback** | 下游真相已更新？ | 端到端数据流追踪 | P1（数据风险） |
| **Report/Analytics** | 报表反映回写？ | 查询比对、新鲜度检查 | P1（数据风险） |
| **Audit/Evidence** | 动作已记录？轨迹完整？ | 审计日志验证 | P2（合规） |
| **Product Acceptance** | 目标用户能否高效完成真实业务流程？ | product owner 验收记录 | P1（交付风险） |

**业务链分类**：O2C（Order to Cash：销售订单→发货→开票→收款）、S2P（Source to Pay：采购申请→订单→收货→付款）、R2R（Record to Report：交易→总账→财务报表）、L2C（Lead to Cash：线索→商机→报价→订单）、Fulfillment（订单→拣货→打包→发运）、Subscription（注册→激活→计费→续订/取消）。

**标准工作流**：Step 1 映射链路（识别所有节点 entry → API → service → DB → writeback → report，识别所有影响该链的参数/开关，记录预期状态流转）。Step 2 逐节点取证（Entry 截图 + 表单校验；API 用 `curl` 拿到预期状态码与响应体；Service 评审业务逻辑路径与事务边界；Database 用 `DESCRIBE table` 与动作前后抽样行；Writeback 从源表追踪到下游表；Report 查询报表输出并与源数据新鲜度比对；Product acceptance 执行 owner 定义的 `business-flow acceptance` 测试并记录接受/拒绝/修改反馈）。Step 2a 双轴审查（`two independent axes`，见下表）。Step 2b 写回一致性交叉校验。Step 3 识别缺口并按 `P0`（阻断：缺后端校验、API 损坏、缺表）、`P1`（数据风险：回写不完整、报表过期、缺参数门控）、`P2`（UX/合规：缺审计轨迹、UI 行为不一致）分级。Step 4 把每条缺口转成具体任务（Gap / Severity / Root Cause / Fix Action / Acceptance）。

**Step 2a：`two independent axes` 审查**——在称一条非平凡流程就绪之前，**必须**把两类发现分开：

| 轴 | 问题 | 最低证据 |
|---|---|---|
| **Standards / truth** | 改动是否遵循仓库标准、唯一真相源归属、架构边界、安全/质量门禁，以及所选 `L0`-`L3` 门禁？ | 限定范围的 diff 评审、相关审计/构建/测试/运行时证据 |
| **Product / spec** | 流程是否交付了原始业务结果与验收步骤，且未违反显式非目标、未添加未获批行为？ | 产品契约、验收记录、观察到的行为 |

任一轴都**禁止**掩盖另一轴。技术实现干净但错失业务结果的审计失败；行为正确但违反真相或架构边界的审计同样失败。

**Step 2b：写回一致性交叉校验**——只有当数字在各层之间对账一致时回写才算闭环。凡涉及数量、金额、余额或状态流转的流程，**必须**增加一致性交叉校验，扫描错配而不是相信单行抽样：① 映射对账配对（每个回写的源表 → 下游表）；② 设计校验（两侧各自独立聚合后比对；对计算值如均值、余额还要从原始行重算）；③ 全表扫描（定位源与下游不一致的行，一次全表扫描常能暴露抽样检查漏掉的隐性漂移）；④ 记录差异（表、行、期望值与实际值、可能根因）；⑤ 修复并重跑（修复后交叉校验**必须**返回零错配才能闭环）。该步骤与栈、领域无关：模式就是"每个回写都要交叉校验对账，而不是抽样"。示例（ERP 领域）：采购收货 → 库存 + 应付账款，两侧聚合值**必须**与收货行合计对账，任何漂移都是 `P1` 数据风险。

**输出格式**（`## Evidence Collection Template`）：① Layer Evidence 表——`Layer | Status | Evidence | Notes`，逐层列出 Entry/UI、API、Service、Database、Writeback、Report、Product acceptance，Status 用状态符号；② Two-Axis Review 表——`Axis | Status | Evidence | Blockers / Notes`，两行为 Standards / truth 与 Product / spec；③ Gap Summary——`P0: [count] blockers`、`P1: [count] data risks`、`P2: [count] UX/compliance issues`。修复任务表列固定为 `Gap | Severity | Root Cause | Fix Action | Acceptance`。

**防护规则**：**禁止**在没有每层证据的情况下声称闭环；**禁止**把"前端会处理"当作业务规则的闭环；**禁止**跳过回写验证——它是最常见的隐藏缺口；**禁止**凭想象审计——**必须**对照真实运行中的代码与数据库；**禁止**把通过的 API 测试当作完整闭环而不做数据库/回写验证；**禁止**把技术验证当作 product owner 的 `business-flow acceptance` 的替代品；**禁止**把 standards/truth 发现与 product/spec 发现混在一起——两轴**必须**独立报告并独立解决；**禁止**用过期的输出或智能体报告当作闭环证据——**必须**在最终相关改动后重跑证明性检查（`fresh evidence`）。

---

## 10. `ai-cross-project-audit` — 跨项目治理审计流水线

- **源文件**：`skills/governance/ai-cross-project-audit/SKILL.md`
- **成熟度**：callable

**用途**：用一套原子治理体系编排跨独立项目的治理审计——实现"**一个项目的原子系统审计另一个项目的代码库**"这一模式，且不修改目标项目。要解决的问题是：治理审计通常被困在单个项目内，跨项目审计需要人工搬数据、格式不一致、没有可复用流水线。本 Skill 定义标准流水线：消费既有审计数据、编排多来源发现、产出统一治理报告。

**触发条件**：跨项目审计时；需要从另一个项目的原子治理体系审计某个项目时；需要复用既有审计数据产出证据链时。`description` 明示模式为 "Use when auditing one project from another project's atomic governance system"。源文件未提供独立的 `## Trigger` 小节。

**核心规则**（`## Rule 1`–`Rule 3` 完整译出）：

**Rule 1：默认只读（P0）。** 审计另一个项目时**必须**默认**只读模式**：消费既有审计数据文件（不重新扫描目标）；产出报告与建议；**禁止**修改目标项目代码；所有证据**必须**打上来源项目与审计周期 ID 标签。**例外**：仅当被审计项目团队显式请求主动整改时，才切换到主动模式，并**必须**带显式范围边界。

**Rule 2：数据复用（P1）。** 生成新审计数据之前，**必须**先在证据目录中搜索既有审计产物：

```text
evidence/{target_project}/
  {audit_name}/
    gaps.json        ← 代码审计发现
    result.json      ← 字段/规则审计结果
    casepack.json    ← 复核队列 / 建议
```

既有数据可被 `L3` 原子直接消费，**无需**重新扫描目标项目，既省算力又保证审计一致性。

**Rule 3：证据链完整（P0）。** 每次跨项目审计**必须**产出完整证据链：① Audit——来自 `L3` 原子的结构化发现，验证条件为发现数 > 0；② Evidence——含 `cycle_id`、stages、findings_sample 的 JSON 文件，验证条件为文件存在且是合法 JSON；③ Index——含可搜索条目的 JSON 索引，验证条件为 `entries_added` > 0；④ Report——含执行摘要的 Markdown 报告，验证条件为报告路径存在。

**审计/验证维度**（`## Audit Types`，五种 `L3` 域原子）：**代码审计**（`domain_code_audit`）消费 `gaps.json`，发现形如 `direct_db_write_in_controller`、`action_endpoint_without_command_pattern`，产出按模块分组的发现组、风险评分、整改建议；**字段审计**（`domain_erp_field_check`）消费来自 `field_package_truth_audit` rulepack 的 `result.json`，产出字段模式违规、`FieldPackage` 缺口、前端字段定义重复；**SQL 审计**（`domain_sql_validate`）消费 SQL 迁移文件，产出模式（Schema）漂移、缺失迁移、命名规范违规；**API 审计**（`domain_api_test`）消费 API 端点清单，产出端点健康度、响应模式一致性、鉴权覆盖；**配置审计**（`domain_config_diff`）消费配置文件，产出环境漂移、缺失租户配置、硬编码值。

**输出格式**（`## The Pipeline` 与 `## Report Structure Template`）：流水线为「既有审计数据（`gaps.json`、`result.json`）→ `L3` 域原子 → `L5` Governance Orchestrator（`app_governance_orchestrator`，audit → evidence → index → report）→ 输出 `evidence.json`（审计轨迹）、`knowledge_index.json`（可搜索）、`report.md`（人可读）」。报告**必须**包含：执行摘要（总发现数、严重度分布、模块覆盖）；① 代码审计——模块分布（逐模块风险等级与受影响最多的文件）；② 字段封装审计（字段模式违规、`FieldPackage` 缺口）；③ 修复路线图（`P0` 立即修复的架构违规、`P1` 短期修复的模式补全、`P2` 长期改进的覆盖扩展）；④ 方法论洞察（经验证的跨项目治理模式、与其他受审项目的对比）。编排调用示例（Python）使用 `GovernanceOrchestratorExecutor()` 与 `RiskActionMatrixService()`，传入 `project_root`、`gaps_path`、`audit_types=["code", "erp_field"]`、`output_dir`、`tag`、`governance=gov`，返回 `cycle_id`、`stages_completed`、`total_findings`、`evidence_path`、`report_path`、`index_entries`。

**验证清单**：宣布跨项目审计完成前**必须**逐项勾选——既有审计数据文件已全部识别并消费；`L3` 原子执行且未修改目标项目；证据文件已写入完整周期元数据；知识索引已填充可搜索条目；报告已生成且含全部必需小节；目标项目中无任何文件被修改；审计周期 ID 已记录以便追溯。

**防护规则**：源文件未提供 `## Guardrails` 小节；其约束强度由 `Rule 1`（P0 只读、**禁止**改目标代码）与 `Rule 3`（P0 证据链完整）以及上述验证清单承担。案例：ERP 跨项目审计（2026-07-05），来源为 `L0`-`L5` 原子治理系统，目标为企业 ERP 生产仓库，模式为只读；输入为 623 条代码审计发现与 100 条字段审计发现；流水线为 `domain_code_audit` 产出 623 条发现覆盖 7 个模块、`domain_erp_field_check` 产出 100 条字段发现与 249 个候选、`L5` orchestrator 产出证据 + 34 条索引 + 报告；关键洞察是既有审计数据可被 `L3` 原子直接复用，无需重新扫描。

---

## 11. `ai-brownfield-analyzer` — 老项目分析与模式提炼

- **源文件**：`skills/governance/ai-brownfield-analyzer/SKILL.md`
- **成熟度**：verified

**用途**：在修改任何既有项目之前执行结构化审计：分析现状、判定干预级别（intervention level）、提炼模式（好的与坏的）、产出外科手术式修改计划。本 Skill 保证方法论先**向项目学习**，再**对项目施加**。要解决的问题是：智能体把每个项目都当成新项目（greenfield）画布，重写本来能跑的代码、破坏有其合理原因的约定、强加不适配的模式；老项目（brownfield）分析通过强制"先理解再动手"避免这一切。

**触发条件**：**始终（ALWAYS）**在首次进入任何既有项目时；用户说"修一下我项目里的这个 Bug""给我的应用加个功能""重构这个模块"时；`ai-project-classifier` 判定 Origin = Brownfield 时；从其他团队接手半成品工作时；项目没有 README、没有测试或架构不清时。

**核心规则**（`## Rule` 完整译出）：**既有项目是老师，方法论是学生。**

```text
禁止：看到乱代码 → “我把它重写规范”
应当：看到乱代码 → “原本意图是什么？这里存在什么模式？”
```

标准控制流为 Step 0 工具发现（`py scripts/py/discover_tools.py {project_path} --by-purpose`，按用途归类既有脚本，覆盖 database/migration、database/check、database/sync、database/seed、build/compile、service/start、service/stop、deploy/release、test/api、test/unit、utility/cleanup、utility/generate；若某一用途类别有 5 个以上脚本，说明项目已有既定模式，**必须**匹配它）→ Step 1 快速扫描（5 分钟：根结构、`git log --oneline -20`、依赖文件）→ Step 2 深度审计（15–30 分钟，产出 Health Scorecard：代码组织、测试覆盖、文档、依赖新鲜度、一致性五个 1–10 分维度加总分，每项**必须**附证据）→ Step 3 判定干预级别 → Step 4 提炼模式 → Step 5 产出修改计划。

**审计/验证维度**：**干预级别 Level 1–5**：Level 1 Quick Fix（快速修复）、Level 2 Feature Addition（功能追加）、Level 3 Module Upgrade（模块升级）、Level 4 Deep Renovation（深度改造）、Level 5 Takeover（接管），逐级核对条件是否满足。**模式提炼**：好模式（Pattern / Found in / Why good / Skill to update）**必须**保留并形式化进 Skill；坏模式（Anti-pattern / Found in / Impact / Fix priority，优先级用 `P0`/`P1`/`P2`）记录下来待修。提炼规则：好坏模式都要提炼（反模式教人"不要做什么"）；一条记录只放一个模式；**必须**引用具体文件/行（基于证据而非观点）；单次出现**禁止**当作模式（一个模式 = 至少 3 个一致示例）；**必须**立即喂给 `ai-skill-evolver`，**禁止**批量攒着更新。**修改计划格式**：Intervention Level、Scope（IN / OUT）、Batches 表（`# | Task | Risk | Dependencies | Estimate`）、Safety Measures（数据库已备份、动工前回归测试通过、已建特性分支、回滚方案已记录）。**半成品项目**识别信号：代码里遍布"应该能跑但是…"注释、README 描述了不存在的功能、到处是 `TODO`/`FIXME`、无 git 历史、完成度参差。处理方式：**记录现实而非愿望**（如"README 说支持文件上传，实际是路由存在、处理器为空"）；**映射已存在的而非计划中的**（可用的、部分可用的、未实现的）；**按依赖优先排定完工顺序**（不是"有什么会比较酷"）；**设定现实预期**。**容易遗漏的场景**：原始团队不在（不要臆测"怪代码"的意图、用 git blame 当史官、补测试作为给下一位开发者的文档、建立 bus-factor 地图找出零存留知识的模块）；需要数据迁移（迁移前**必须**审计源数据质量、显式映射旧→新模式、脚本幂等且带 dry-run、**必须**在数据副本上测试而**禁止**在生产数据上测试）；环境漂移（比对各环境配置，检查依赖版本、运行时版本、DB 版本、硬编码路径，标准化为一套配置模板 + 环境覆盖）；何时放弃重做（加权评分 = 测试 20% + 依赖 15% + 架构 20% + 团队知识 15% + 功能 20% + 安全 10%，低于 2.5 分考虑重建，重建前**必须**先抽取全部业务规则，那才是真资产）。

**输出格式**：项目画像（类型、技术栈、年龄、团队规模）；Health Scorecard 表（`Dimension | Score (1-10) | Evidence`）；干预级别判定；模式提炼条目（好模式与反模式两组）；修改计划（Scope IN/OUT + Batches 表 + Safety Measures 勾选）。集成链路：`ai-project-classifier` 检测到 Brownfield → 本 Skill Phase 1-3（Audit → Classify → Extract）→ `ai-chief-planner` Phase 4（Plan）→ `ai-task-decomposer` Phase 5（Execute batches）→ `ai-skill-evolver` Phase 6（把模式回灌进 Skill），可选 `ai-reference-researcher` 找参考项目对比。

**防护规则**：**先审计再行动**——在陌生项目里**禁止**写代码；**匹配既有风格，哪怕丑**——一致性优于审美；**不要修没坏的东西**——能跑且不在范围内就别碰；**信运行中的代码而不是文档**——文档会撒谎，代码不会；**一次提交只做一类改动**——重构或加功能，**禁止**同时做；**提炼模式而不是强加模式**——项目才是标准的制定者；**数据库改动是独立批次**——**禁止**把 DB 改动与代码改动混在一起；**半成品不等于垃圾**——记录现实，建立完工顺序。

---

## 12. `ai-reference-researcher` — 参考实现驱动的研究

- **源文件**：`skills/governance/ai-reference-researcher/SKILL.md`
- **成熟度**：verified

**用途**：在不熟悉的领域开发复杂功能之前，搜索、下载、分析并提炼最优秀的开源参考实现中的模式。这把"AI 凭训练数据猜"变成"AI 从真实生产代码学习"。要解决的问题是：AI 的训练数据广而不深，对 ERP 工作流、财务计算、供应链、权限系统、多租户 SaaS 等专门领域，它常因为没见过成熟系统的真实实现而发明次优模式；参考研究通过先给出具体高质量样本解决这个问题。

**触发条件**：**必须（MUST）**触发——团队从未做过的领域（如第一个薪酬模块、第一个 WMS）；设计复杂子系统（鉴权、多租户、工作流引擎、报表引擎）；AI 已做出 2 个以上错误架构假设；用户说"我不确定这该怎么做"或"帮我找个参考"。**应当（SHOULD）**触发——在 3 个以上竞争库/框架间选型；为新业务领域设计数据库模式（Schema）；新项目初始化（脚手架之前）；`ai-library-first` 找到多个候选库、需要参考研究帮助选优。**跳过（SKIP）**——简单 CRUD 功能；团队经验丰富的领域；紧急缺陷修复（时间敏感）；快速原型（Archetype A）。

**核心规则**（`## Rule` 完整译出）：研究**必须**：1) 先搜官方文档；2) 找到典范示例（canonical examples）；3) 对比多个来源；4) 标注版本适用性；5) 产出带引用的摘要。**禁止**在没有引用的情况下声称"最佳实践"。

**审计/验证维度**（`## Research Workflow` 五阶段）：**PHASE 1 SEARCH**——在 GitHub/GitLab/npm/PyPI 搜索领域内头部项目（搜索源：GitHub 用 `site:github.com {domain} {language} stars:>100`；npm 用 `npm search {keyword}`；Maven Central 用 `mvnrepository.com`；PyPI 用 `pypi.org`；Awesome Lists 用 `site:github.com awesome {domain}`）。**PHASE 2 EVALUATE**——按加权标准打分：Stars 25%（>100 良好、>1000 优秀）、Active maintenance 30%（最近提交 < 6 个月、issue 在被关闭）、Architecture quality 20%、Code quality 15%、Domain relevance 10%；输出评估表（`Project | Stars | Last Commit | Arch Quality | Overall | Verdict`，结论为 SELECT / Reference only / Skip）。**PHASE 3 DOWNLOAD**——把最好的 1–2 个项目克隆到本地分析（`mkdir -p reference/ && cd reference/` 后 `git clone --depth 1 <repo-url>`；**必须**用 `--depth 1` 浅克隆；存到 `reference/` 且加入 git-ignore；**禁止**把参考代码提交进项目仓库；分析完删除或保留备查）。**PHASE 4 EXTRACT**——按九个维度分析并产出：目录结构、架构模式（服务如何切分、是否事件驱动、是否 CQRS）、数据库模式（表命名、关系、索引策略）、API 设计（REST vs GraphQL、端点命名、版本化）、库选择、命名约定、错误处理、测试模式、配置管理。**PHASE 5 APPLY**——把发现接入 `ai-atomic-architect`（参考架构模式 → 原子服务设计）、`ai-library-first`（参考库选择 → 库目录更新）、`ai-component-standardizer`（参考目录结构 → 脚手架模板）、`ai-project-classifier`（领域复杂度评估 → 质量目标选择）、`ai-architect-governor`（基于参考发现写 ADR，落到 `docs/架构决策记录/`）、`ai-skill-evolver`（新模式 → Skill 更新）。

**输出格式**：评估表；`## Reference Analysis: [Project Name]` 分析文档，含 Key Patterns Extracted（编号列出模式 + 示例路径）、Patterns to Adopt（模式 + 为什么适合我们）、Patterns to Avoid（反模式 + 为什么会出问题）、Recommended Architecture Decisions（ADR 候选）。**许可证意识**：**学习，不要复制**；参考代码用于学模式而非抄代码——MIT / Apache 2.0 / BSD 可学习且可在署名前提下复制；GPL / AGPL 可学习但仅当本项目同为 GPL 才可复制；专有/无许可证**禁止**学习、**永禁止**复制；默认规则是只研究 MIT、Apache 2.0 或 BSD 许可的项目。领域参考目标表给出 ERP/企业系统（多租户 SaaS、库存/WMS、会计/财务、CRM、工作流引擎）与通用架构（微服务、权限/RBAC、报表引擎、实时）的搜索关键词与预期发现。

**防护规则**：**学模式，绝不抄代码**——这是学习，不是剽窃；**先查许可证**——跳过许可证不兼容或缺失的项目；**质量优于数量**——1–2 个深研项目胜过 10 个浅扫；**浅克隆**——永远 `--depth 1`，别浪费磁盘；**git-ignore `reference/`**——**禁止**把参考代码提交进项目仓库；**记录学到的东西**——每次研究**必须**在 `docs/每日调研回写/` 产出文档；**给研究定时限**——每个领域最多 30 分钟，找不到好参考就继续推进。

---

## 13. `ai-competitor-analyst` — 竞品对标与市场调研

- **源文件**：`skills/governance/ai-competitor-analyst/SKILL.md`
- **成熟度**：verified

**用途**：研究与对比产品、功能与市场定位，覆盖竞品功能对标、面向市场的功能映射、产品包装与版本策略分析、技术栈对比、行业趋势分析。本 Skill 只做**竞品研究与对标**，不做产品策略决策。

**触发条件**：市场分析任务；产品策略研究；定价与功能对比；面向投资人的定位材料。`description` 明示 "Use for market analysis, product strategy, pricing, feature comparison, or investor-facing positioning"。源文件未提供独立的 `## Trigger` 小节。

**核心规则**（`## Rule` 完整译出）：**对标真实产品行为，而不是营销材料。** 验证竞品宣称**必须**通过：直接使用产品（试用/演示）；阅读技术文档；查看社区论坛中的真实用户反馈；在可得时对比公开 API 与架构。

**审计/验证维度**（`## Benchmark Framework` 四张对标表）：① **功能矩阵**（`Feature | Our Product | Competitor A | Competitor B | Competitor C`），评级口径为完整支持且生产可用 / 部分支持或开发中 / 不可用；② **定价与包装**（`Dimension | Our Product | Competitor A | Competitor B`，维度含 Free Tier、Entry Price、Enterprise、Pricing Model）；③ **技术与架构**（维度含 Tech Stack、Deployment、API/SDK、Multi-tenancy）；④ **市场定位**（维度含 Target Segment、Key Differentiator、Geographic Focus、GTM Strategy）。研究方法分一手与二手：一手研究（推荐）为产品试用、文档评审、社区分析（论坛、GitHub issues、Stack Overflow）、客户访谈；二手研究为评审站点（G2、Capterra、TrustRadius）、行业报告（Gartner、Forrester、IDC）、技术博客与案例、会议演讲。

**输出格式**（`## Benchmark Decision Template`）：`## Benchmark: [Feature/Product Area]` 文档，含 Research Date、Research Method 勾选（Product trial / Documentation review / Community analysis / Secondary sources）、Key Findings（编号 + Impact：High/Medium/Low）、Gap Analysis 表（`Gap | Severity | Competitors With This | Recommended Action`）、Decision（Build / Buy / Partner / Defer）、Timeline（Immediate / Q1 / Q2 / Future）。

**标准工作流**：1) 定义范围——要标哪个产品域或功能；2) 识别竞品——对比哪 3–5 家；3) 研究——用一手与二手方法收集数据；4) 打分——填写对标框架各表；5) 分析差距——识别优势、劣势、机会；6) 建议——产出具体行动建议。

**防护规则**：**禁止**对标营销宣称——**必须**用真实产品使用验证；**禁止**与过时的竞品版本对比；**禁止**忽略竞品的社区/生态强度；**禁止**跳过定价模型分析——它常常是关键差异点；**禁止**在对标表中没有证据的情况下产出建议。

---

## 附录 A：governance 层触发矩阵（什么情况找哪个 Skill）

| 你面对的情况 | 找哪个 Skill | 门禁强度 |
|---|---|---|
| 有人想在组件里算金额、在客户端做业务校验、把删除确认做成轻提示 | `ai-single-truth-enforcer` | `P0` 阻断（禁令级） |
| 审计/建设原子系统、新增原子、给既有执行器补治理 | `ai-atomic-governance` | `P0`（Rule 1、Rule 2）、`P1`（分层） |
| 数据、身份、权限、单据、报表要跨模块 | `ai-domain-boundary-mapper` | 归属唯一，跨域必须显式可追溯 |
| 要加数据库列、改表单/表格字段、集中元数据 | `ai-field-package-governor` | 字段真相唯一，页面不得自持 |
| 要新建页面或评审页面是否符合模板 | `ai-component-standardizer` | 模板结构不可协商；主题只改变量 |
| 页面布局、密度、四态、文案、主题令牌要评审 | `ai-ui-ux-governor` | 零废话 + 密度 + 四态为硬约束 |
| 提 PR、截图、发布前要做前端质量审计 | `ai-frontend-audit` | 可用性与完备性 `P0`；一致性/性能/错误态 `P1`；无障碍 `P2` |
| 要声明"开发完成"、部署后、重启后 | `ai-runtime-verify` | 三条 `P0` 硬判据；未拿到 `passed: true` 禁止声称 complete |
| 要声明某业务流程完成、检查端到端就绪 | `ai-flow-closure-audit` | API/Service/DB 缺证据为 `P0`；写回/报表/参数/产品验收为 `P1` |
| 要跨项目审计、复用既有审计数据出证据链 | `ai-cross-project-audit` | 默认只读（`P0`）、证据链完整（`P0`） |
| 首次进入存量项目、迁移、接管、继承半成品 | `ai-brownfield-analyzer` | 先审计再改；数据库改动独立批次 |
| 进入不熟悉领域、在多个候选库间选型 | `ai-reference-researcher` | MUST/SHOULD/SKIP 三档触发，禁止无引用称"最佳实践" |
| 做市场分析、定价对比、投资人材料 | `ai-competitor-analyst` | 禁止用营销宣称对标，建议必须有表中证据 |

选型顺序建议：先判定"这是不是老项目"（`ai-brownfield-analyzer`）→ 再判定"这是什么页面/什么领域"（`ai-component-standardizer` 或 `ai-domain-boundary-mapper`）→ 开发中始终挂 `ai-single-truth-enforcer` 与 `ai-field-package-governor` → 提 PR 前 `ai-frontend-audit` → 声明完成前 `ai-runtime-verify` 与 `ai-flow-closure-audit`。

---

## 附录 B：与 core 层的配合关系

governance 层是执行层（Layer 3）里的"闸门与标尺"，它不产出交付物，只对 core 层产出的交付物做判定。主要配合关系如下：

| governance Skill | 配合的 core Skill | 配合方式 |
|---|---|---|
| `ai-single-truth-enforcer` | `ai-atomic-architect`、`ai-product-directed-delivery`、`ai-library-first`、`ai-component-standardizer` | 前端纯展示与后端真相的边界即为 `atomic service` → `aggregate interface` → `command gateway` → `Host` 这条后端链，以及 `ui atom` → UI 编排 → 标准模板 → `host page` 这条前端链；`Host` 显示某命令的前提是后端 aggregate/runtime 契约标记其可用，所有写入必须走 `command gateway` |
| `ai-component-standardizer` | `ai-product-directed-delivery`、`ai-chief-planner`、`ai-project-classifier` | 组合主链的最后一跳落在 `host page`；`Host` 是组合面而非业务服务，不得重复字段、权限、状态、计算 |
| `ai-field-package-governor` | `ai-product-directed-delivery`、`ai-foundation-governor` | 后端 runtime 的 `FieldPackage` / `BusinessProfile` / 权限是字段真相的载体，页面通过 `businessCode`/`entityKey`/`reportCode` 消费 |
| `ai-domain-boundary-mapper` | `ai-architect-governor`、`ai-foundation-governor`、`ai-multi-agent-orchestration` | 领域归属结论喂给架构决策记录（ADR）与多智能体领域切分 |
| `ai-atomic-governance` | `ai-atomic-architect`、`ai-delivery-contract-governor` | 声明/执行器分离与 `L0`–`L5` 分层是原子架构的验收面；执行器必须接受治理参数 |
| `ai-ui-ux-governor` | `ai-component-standardizer`、`ai-frontend-audit` | 设计系统规则由标准模板承载，由前端审计核查 |
| `ai-frontend-audit` | `ai-runtime-verify`、`ai-component-standardizer` | 先静态审计代码质量，再由运行时验证查浏览器行为 |
| `ai-runtime-verify` | `ai-5s-delivery-governor`、`ai-delivery-contract-governor` | 位于开发执行引擎 Step 13；其证据 JSON 是任务完成证明，也是 `fresh evidence` 要求的落地载体 |
| `ai-flow-closure-audit` | `ai-product-directed-delivery`、`ai-5s-delivery-governor`、`ai-delivery-contract-governor` | 承载 `two independent axes` 审查与 product owner 的 `business-flow acceptance`；技术门禁通过不等于业务验收通过 |
| `ai-cross-project-audit` | `ai-atomic-governance`、`ai-chief-planner` | 跨项目审计复用 `L3` 域原子与 `L5` orchestrator 的流水线 |
| `ai-brownfield-analyzer` | `ai-project-classifier`、`ai-chief-planner`、`ai-task-decomposer`、`ai-skill-evolver` | 分类层判定 Brownfield 后进入审计 → 计划 → 拆批 → 模式回灌 |
| `ai-reference-researcher` | `ai-library-first`、`ai-architect-governor`、`ai-skill-evolver` | 参考发现进入库选型、ADR 与 Skill 更新 |
| `ai-competitor-analyst` | `ai-chief-planner`、`ai-product-directed-delivery` | 竞品结论是产品范围与优先级决策的输入，不构成验收 |

配套的门禁与状态口径：`ai-5s-delivery-governor` 用 `L0`/`L1`/`L2`/`L3` 门禁分级（L0 只读与外观、L1 单组件/单端点、L2 共享业务模块与写入路径、L3 模式/权限/版本/跨模块回写/发布），并用 `Q0`/`Q1`/`Q2`/`Q3` 交付资格描述能力成熟度（能力存在 → 参数权限对齐 → 后端编排与副作用路径闭环 → 真实客户或 product owner 场景跨端完成且对账通过）；交付状态只能写 `complete`，未推送提交、证据失败、远端不可用或集成仍在进行时**必须**写 `paused` 或 `blocked`。`ai-delivery-contract-governor` 则把契约做成**失败即阻断（fail-closed）**：改写白名单之外的路径、缺少证明、证据过期或评审未通过，都会阻断 `safeguarded` 与 `completed`。governance 层为这两套代号提供证据来源——`ai-runtime-verify` 给运行时证据，`ai-flow-closure-audit` 给写回与对账证据，`ai-frontend-audit` 给静态质量证据，`ai-cross-project-audit` 给跨项目证据链（`evidence.json` + `knowledge_index.json` + `report.md`）。
