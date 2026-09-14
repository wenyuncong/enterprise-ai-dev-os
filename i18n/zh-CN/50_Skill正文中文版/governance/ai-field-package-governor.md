# `ai-field-package-governor` — 字段元数据与组件配置治理

> **源文件**：skills/governance/ai-field-package-governor/SKILL.md
> **源版本**：未标注（源文件无版本字段；`## Evolution History` 最新记录为 v1.0.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-field-package-governor
description: "Govern field metadata, database-authoritative fields, UI field packages, personalization config, report fields, and duplicate field definitions. Use when adding columns, changing form/table fields, centralizing metadata, or auditing hard-coded page fields."
```

**中文描述**：治理字段元数据、以数据库为权威的字段、UI 字段包（field package）、个性化配置、报表字段以及重复字段定义。在新增列、修改表单/表格字段、集中元数据、审计页面硬编码字段时使用。

---

## Purpose | 目的

治理企业系统中的字段元数据层——即把数据库模式（schema）连接到 UI 组件的基础设施：

- 字段真相源层次（DB → 元数据 → 组件配置）
- 组件复用与组合的强制要求
- 字段配置治理（可见性、校验、排序）
- 由元数据生成报表
- 页面个性化只作为配置层，而不是主定义

本 Skill 适用于任何「页面展示数据库中的结构化数据、且字段定义必须集中而非逐页重复」的企业系统（ERP、CRM、SaaS admin、运营工具）。

本 Skill 治理的正式对象是 `FieldPackage`（字段包）与 `BusinessProfile`（业务画像）：字段真相由 `FieldPackage` 承载，业务口径由 `BusinessProfile` 承载，二者都归后端所有，UI 只消费。

## Rule | 规则

**页面不拥有字段真相（The page does not own the field truth）。**

字段真相按如下顺序流动：
1. **Database schema（数据库模式）** —— 真实表结构、列类型、约束
2. **Field metadata registry（字段元数据注册表）** —— 业务标签、校验规则、UI 元数据、多语言标签
3. **Component configuration（组件配置）** —— 字段可见性、排序、必填状态、可编辑性
4. **Page personalization（页面个性化）** —— 用户级展示偏好（**不是**主字段定义）

前端**应当（SHOULD）**接收 `businessCode` 或 `entityKey`，并从元数据层消费字段——**禁止**在单个页面里硬编码字段名、标签或列定义。

---

## Field Truth Source Hierarchy | 字段真相源层次

| 层 | 职责 | 示例 |
|---|---|---|
| **Database** | 结构真相 | 列类型、约束、可空性 |
| **Field Metadata** | 业务真相 | 标签、校验规则、多语言名称 |
| **Component Config** | 展示真相 | 可见性、排序、宽度、必填状态 |
| **Page Personalization** | 用户偏好 | 保存的筛选器、列顺序、隐藏字段 |

**违规检测**：若同一字段标签出现在 3 个及以上页面文件里，它就属于元数据层，而不属于各个页面。

---

## Configuration Sources | 配置来源

四层配置来源的层级顺序固定为：**① Database-First → ② Metadata Registry → ③ Component Binding → ④ User Personalization**，越靠前的层级权威性越高。

### 1. Database-First（数据库优先）

在任何字段配置之前，先核实真实的数据库模式：

```
Check: column exists, type matches, constraints are correct
Source: DESCRIBE table / SHOW COLUMNS
```

### 2. Metadata Registry（元数据注册表）

集中式字段定义包含：
- Field key（字段键，与 DB 列一致）
- Display label（展示标签，多语言）
- Data type and format（数据类型与格式）
- Validation rules（校验规则）
- Default values（默认值）
- Relation mappings（关联映射：外键 → 选择器）

### 3. Component Binding（组件绑定）

页面通过标识符绑定到元数据：
- `businessCode` —— 用于标准 CRUD 页面
- `entityKey` —— 用于领域专用组件
- `reportCode` —— 用于报表与分析页面

### 4. User Personalization（用户个性化）

用户可以在不破坏真相的前提下自定义：
- 显示/隐藏可选字段
- 重排列顺序
- 保存筛选预设
- 调整列宽

---

## Component Reuse Pattern | 组件复用模式

| 如果你需要… | 使用… | 而不是… |
|---|---|---|
| 展示数据列表 | 共享列表组件 + `businessCode` | 带页面局部列的硬编码表格 |
| 展示表单 | 共享表单组件 + `entityKey` | 每个页面手写表单字段 |
| 生成报表 | 共享报表引擎 + `reportCode` | 页面局部 SQL + 自定义图表渲染 |
| 过滤数据 | 元数据驱动的筛选栏 | 逐页重复实现筛选组件 |

**验收检查**：新增一个数据库列**应当**只更新元数据注册表，所有消费该实体的页面**应当**随之反映该变化——**不需要**修改任何一个页面文件。

---

## Report Generation Pattern | 报表生成模式

对于可由元数据描述的标准列表/图表报表：

1. **Register dataset（注册数据集）** —— 定义源表、字段白名单、维度、指标
2. **Register metadata（注册元数据）** —— 自动导入关系字段（customer→customerId、product→productId）
3. **Generate frontend（生成前端）** —— 共享报表组件接收 `reportCode` 并动态渲染
4. **Enforce permissions（强制权限）** —— 由后端报表引擎控制访问，而不是前端组件

**只有满足以下条件时才创建自定义报表页**：该报表需要交互式工作流、多步命令，或元数据无法表达的专用 UX。

---

## Document Identity Pattern | 文档身份模式

当一个物理实体（表）承载多个业务身份时：

1. 把每个身份注册为正式实体类型，并各自拥有元数据别名
2. 让决策按身份路由，而不是按表名路由
3. 每个身份各自拥有编号规则、权限与字段可见性规则
4. 复用共享组件，锁定/隐藏与该身份无关的字段

---

## Standard Workflow | 标准工作流

### Adding a New Field | 新增字段

1. **DB**：向表中加列（迁移脚本）
2. **Metadata**：在字段元数据注册表中注册
3. **Configuration**：设置默认可见性、排序、校验
4. **Verification**：所有消费页面都正确显示该字段——至少验证 3 个及以上页面

### Modifying a Field | 修改字段

1. **Check consumers**：找出所有引用该字段的页面/组件
2. **Verify DB**：确认列类型与约束和元数据一致
3. **Update metadata**：集中修改标签、校验或展示规则
4. **Verify**：所有消费方都反映该变化，且没有任何页面局部覆盖被破坏

---

## Guardrails | 防护规则

- **禁止**在单个页面里硬编码字段标签
- **禁止**把页面个性化配置当作主字段定义
- **禁止**只新增数据库列而不在元数据层注册
- **禁止**为同一字段建立第二真相源
- **禁止**为「快速修复」绕过元数据——它们会变成永久债务
- **禁止**在同一实体的多个页面之间重复筛选/列/表单逻辑

## Maturity | 成熟度

**Stage**：Effective —— 提炼自 111KB 的企业级字段治理系统，采用元数据驱动的组件架构。

## Evolution History | 进化记录

- v1.0.0：从 gerp-atomic-component-fieldpackage 提炼（原始 111KB）
- Source：企业级 ERP 在采购/销售/库存/财务/资金模块上的元数据治理
