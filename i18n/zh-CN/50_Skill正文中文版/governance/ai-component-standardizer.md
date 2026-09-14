# `ai-component-standardizer` — 组件与页面模板标准化引擎

> **源文件**：skills/governance/ai-component-standardizer/SKILL.md
> **源版本**：未标注（源文件 `## Evolution History` 最新记录为 v1.1.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-component-standardizer
description: "Enforce standard page and component templates, theme variables, layout contracts, action placement, and reusable UI patterns. Use when creating or reviewing list pages, document forms, reports, dashboards, or enterprise frontend components."
```

**中文描述**：强制标准的页面与组件模板、主题变量、布局契约、操作位置与可复用 UI 模式。用于创建或评审资料列表页、单据表单、报表、看板及企业级前端组件的场景。

---

## Rule | 规则

标准化**必须**：1）对照设计系统检查；2）校验 API 一致性；3）保证可访问性（a11y）；4）检查是否已有替代实现；5）在组件目录中登记。**禁止**创建未标准化的组件。

## Purpose | 用途

为后端与前端定义并强制标准的组件/页面模板。阻止智能体为每个新页面重新发明布局。每个列表页长得一样。每个表单页遵循同一模式。每个报表页使用同一结构。主题支持客户级定制，同时不破坏标准。

**它解决的问题**：智能体从零创建每个页面，布局不同、按钮位置不同、字段排布不同。一个客户拿到侧边栏表单，另一个客户拿到模态框。一个列表页搜索框在顶部，另一个在底部。这是混乱，不是产品。

---

## The Page Type Taxonomy | 页面类型分类

每个企业页面**必须**落入这些模板之一。没有例外。

```
┌──────────────────────────────────────────────────────────────┐
│                     PAGE TYPE TAXONOMY                        │
├──────────────┬──────────────┬──────────────┬─────────────────┤
│  LIST/TABLE  │  DOCUMENT    │   REPORT     │   DASHBOARD     │
│  (资料页)    │  (单据页)    │  (报表页)    │   (工作台)      │
├──────────────┼──────────────┼──────────────┼─────────────────┤
│ Search bar   │ Header info  │ Filter bar   │ Summary cards   │
│ Toolbar      │ Line items   │ Chart/Table  │ Quick actions   │
│ Data table   │ Summary bar  │ Drill-down   │ Todo list       │
│ Pagination   │ Footer btns  │ Export       │ Notifications   │
│ Detail drawer│ Validation   │ Date range   │ Shortcuts       │
└──────────────┴──────────────┴──────────────┴─────────────────┘
```

**中文对照**：`LIST/TABLE`（资料列表页）＝ 搜索栏 + 工具条 + 数据表 + 分页 + 详情抽屉；`DOCUMENT`（单据页）＝ 表头信息 + 行项目 + 汇总条 + 底部按钮 + 校验；`REPORT`（报表页）＝ 筛选栏 + 图表/表格 + 下钻 + 导出 + 日期范围；`DASHBOARD`（工作台）＝ 汇总卡片 + 快捷操作 + 待办列表 + 通知 + 快捷键。

---

## Frontend Composition Spine | 前端组合主链

企业前端复用**必须**遵循同一条组合链：

```text
backend runtime / field metadata / aggregate profile
  -> UI atoms
  -> UI orchestration
  -> standard page template
  -> Host page
```

| 层 | 职责 | 禁止（Must not do） |
|---|---|---|
| UI atom | 聚焦可复用的 UI 行为：字段渲染器、选择器、表格、状态、操作栏、筛选、汇总、对话框 | 承载业务策略、计算事实、授权命令 |
| UI orchestration | 从后端事实组合原子；协调加载、本地输入、导航、无障碍与反馈 | 自建第二套业务状态机或命令路径 |
| Standard template | 稳定的 list/document/report/dashboard/settings 外壳 | 重建页面级局部布局系统 |
| Host page | 绑定业务 code/profile、选择模板、装配受支持的原子与插槽 | 重复字段、权限、状态、计算或后端命令逻辑 |

`Host`（对应术语表中的 `host page`）是组合面，不是业务服务；它只组合受支持的 `ui atom` 与 `UI orchestration`，不自建业务能力。只有后端 aggregate/runtime 契约把某命令标记为可用时，`Host` 才可以显示该命令；它把所有写入发往后端 `command gateway` 或归属 API 路径。

---

## Template 1: List/Table Page | 资料列表页

**何时使用**：展示可搜索、可筛选的记录列表，并带 CRUD 操作。

### Layout Contract (MUST follow) | 布局契约（必须遵循）

```
┌─────────────────────────────────────────────────────┐
│  [Search Input]  [Filter Dropdown]  [Date Range]    │  ← Filter Bar
├─────────────────────────────────────────────────────┤
│  [+ New]  [Batch Delete]  [Export]       [Refresh]  │  ← Toolbar
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐    │
│  │ ID  │ Name    │ Status │ Date    │ Actions  │    │  ← Table
│  │ 001 │ Item A  │ Active │ 06-17   │ ✎ ✕     │    │
│  │ 002 │ Item B  │ Draft  │ 06-16   │ ✎ ✕     │    │
│  └─────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────┤
│  [<] [1] [2] [3] ... [>]   Showing 1-20 of 156     │  ← Pagination
└─────────────────────────────────────────────────────┘
```

**中文对照**：自上而下 **Filter Bar（筛选栏 / `filter bar`）** ＝ `[Search Input]` + `[Filter Dropdown]` + `[Date Range]`；**Toolbar（工具条）** ＝ `[+ New]`、`[Batch Delete]`、`[Export]`、`[Refresh]`；**Table（数据表）** 列为 `ID | Name | Status | Date | Actions`，行尾操作图标为编辑/删除；**Pagination（分页）** ＝ 页码器 + `Showing 1-20 of 156`。

### Component Contract | 组件契约

| 位置 | 组件 | Props |
|---|---|---|
| Filter Bar | `SearchInput` + `FilterDropdown[]` + `DateRangePicker` | `searchPlaceholder`, `filters`, `onSearch` |
| Toolbar | `ActionButton[]` | `label`, `icon`, `onClick`, `variant` |
| Table | 带 `columns[]` 的 `DataTable` | `data`, `loading`, `emptyText`, `onRowClick` |
| Row Actions | `RowActions` | `actions[]`，各项含 `icon`, `label`, `onClick`, `visible` |
| Pagination | `Pagination` | `current`, `total`, `pageSize`, `onChange` |

### Backend Contract | 后端契约

```java
// Every list page endpoint returns this exact shape:
{
  "data": [...],        // Array of records
  "total": 156,         // Total count for pagination
  "page": 1,            // Current page
  "pageSize": 20        // Page size
}
```

**中文对照**：每个列表页接口**必须**返回这一固定形状——`data`（记录数组）、`total`（分页总数）、`page`（当前页）、`pageSize`（每页条数）。

---

## Template 2: Document/Form Page | 单据录入页

**何时使用**：创建或编辑单条记录，结构为表头信息 + 行项目 + 底部操作。

### Layout Contract | 布局契约

```
┌─────────────────────────────────────────────────────┐
│  ← Back to List                                     │  ← Navigation
├─────────────────────────────────────────────────────┤
│  Document Header                                    │
│  ┌─────────────────────────────────────────────┐    │
│  │ Doc No: [Auto]   Date: [Picker]              │    │  ← Header Fields
│  │ Customer: [Select]   Status: [Tag]           │    │
│  └─────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────┤
│  Line Items                                         │
│  ┌─────────────────────────────────────────────┐    │
│  │ Item    │ Qty │ Price │ Amount │ Actions    │    │  ← Line Items Table
│  │ [Select]│ [  ]│ [   ] │ [Auto] │ [+][-]    │    │
│  └─────────────────────────────────────────────┘    │
│  [+ Add Line]                                       │
├─────────────────────────────────────────────────────┤
│  Summary:  Subtotal: $100  Tax: $13  Total: $113    │  ← Summary Bar
├─────────────────────────────────────────────────────┤
│  [Save Draft]  [Submit]  [Cancel]                   │  ← Footer (pinned)
└─────────────────────────────────────────────────────┘
```

**中文对照**：**Navigation（导航）** ＝ `← Back to List`；**Document Header（单据表头）** + **Header Fields（表头字段）** ＝ `Doc No: [Auto]`、`Date: [Picker]`、`Customer: [Select]`、`Status: [Tag]`；**Line Items（行项目）** + **Line Items Table（行项目表）** 列为 `Item | Qty | Price | Amount | Actions`，操作列为 `[+][-]`，下方 `[+ Add Line]`；**Summary Bar（汇总条）** ＝ `Subtotal / Tax / Total`；**Footer (pinned)（钉底底部操作）** ＝ `[Save Draft]`、`[Submit]`、`[Cancel]`。

### Critical Rules | 关键规则

- Footer action buttons are **pinned to bottom**, always visible
- Summary bar updates in real-time from backend (never computed in frontend)
- Line items have inline add/remove, not separate modal

**中文译文**：

- 底部操作按钮**必须钉在底部（pinned to bottom）**，始终可见
- 汇总条**必须**由后端实时更新（**禁止**在前端计算）
- 行项目**必须**内联增删，不使用独立的模态框

---

## Template 3: Report/Analytics Page | 报表页

**何时使用**：展示聚合数据，带图表与导出能力。

### Layout Contract | 布局契约

```
┌─────────────────────────────────────────────────────┐
│  [Date Range]  [Dimension]  [Metric]  [Generate]   │  ← Filter Bar
├─────────────────────────────────────────────────────┤
│  [Table View]  [Chart View]  [Export]               │  ← View Toggle
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐    │
│  │ Summary Row: Total: 1,234  Avg: 56  Max: 99 │    │  ← Summary
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │            [Chart / Table Content]           │    │  ← Main Content
│  └─────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────┤
│  This report generated: 2026-06-17 14:30             │  ← Footer
└─────────────────────────────────────────────────────┘
```

**中文对照**：**Filter Bar（筛选栏）** ＝ `[Date Range]`、`[Dimension]`、`[Metric]`、`[Generate]`；**View Toggle（视图切换）** ＝ `[Table View]`、`[Chart View]`、`[Export]`；**Summary（汇总）** ＝ `Summary Row: Total / Avg / Max`；**Main Content（主内容区）** ＝ 图表或表格内容；**Footer（页脚）** ＝ `This report generated: <生成时间>`。

---

## Template 4: Dashboard/Workbench | 工作台

**何时使用**：落地页，展示聚合指标与快捷操作。

### Layout Contract | 布局契约

```
┌──────────┬──────────┬──────────┬──────────┐
│ Card 1   │ Card 2   │ Card 3   │ Card 4   │  ← Summary Cards
│ Metric   │ Metric   │ Metric   │ Metric   │
└──────────┴──────────┴──────────┴──────────┘
┌─────────────────────┬──────────────────────┐
│ Recent Items Table  │ Quick Actions        │
│ (same as List)      │ [+ New Order]        │
│                     │ [+ New Invoice]      │
│                     │ [View Reports]       │
└─────────────────────┴──────────────────────┘
```

**中文对照**：**Summary Cards（汇总卡片）** ＝ `Card 1`–`Card 4`，每张卡一个 `Metric`；下方两栏：左侧 **Recent Items Table（最近记录表）**，与资料列表页同构；右侧 **Quick Actions（快捷操作）** ＝ `[+ New Order]`、`[+ New Invoice]`、`[View Reports]`。

---

## Theme System | 主题系统

不同客户需要不同的视觉主题。模板结构保持不变；只改 CSS 变量。

### Theme Variables Contract | 主题变量契约

```css
:root {
  /* Every template component MUST use these variables, never hard-coded colors */
  --theme-primary: <由主题文件定义>;
  --theme-primary-hover: <由主题文件定义>;
  --theme-danger: <由主题文件定义>;
  --theme-success: <由主题文件定义>;
  --theme-warning: <由主题文件定义>;
  --theme-bg: <由主题文件定义>;
  --theme-surface: <由主题文件定义>;
  --theme-border: <由主题文件定义>;
  --theme-text: <由主题文件定义>;
  --theme-text-secondary: <由主题文件定义>;
  --theme-radius: 6px;
  --theme-font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --theme-density: compact;   /* compact | comfortable | spacious */
}
```

**中文对照**：每个模板组件**必须**使用这些变量，**禁止**硬编码颜色。颜色类变量（`--theme-primary`、`--theme-primary-hover`、`--theme-danger`、`--theme-success`、`--theme-warning`、`--theme-bg`、`--theme-surface`、`--theme-border`、`--theme-text`、`--theme-text-secondary`）的取值一律由主题文件以**主题变量**形式提供；`--theme-radius`、`--theme-font`、`--theme-density`（`compact | comfortable | spacious`）为结构类令牌。原示例中的具体色值已按本中文版的禁项要求移除，说明见文末「译注」。

### Customer Theme Override | 客户主题覆盖

每个客户拿到一个主题文件，只覆盖它需要的变量：

```css
/* customer-acme-theme.css */
:root {
  --theme-primary: <由客户主题文件定义>;
  --theme-radius: 4px;
  --theme-density: compact;
}
```

**中文对照**：客户主题文件**禁止**改动布局，只覆盖其需要的主题变量；这份示例只覆盖 `--theme-primary`、`--theme-radius`、`--theme-density`。原示例中的具体色值已按本中文版的禁项要求移除，说明见文末「译注」。

---

## Enforcement | 强制执行

### Detection: Is this page using a standard template? | 检出：本页是否使用标准模板？

| 检查 | 方法 |
|---|---|
| 页面有筛选栏吗？ | 查找 `.filter-bar` 或 `SearchInput` 组件 |
| 表格使用 DataTable 吗？ | 查找 `<DataTable` 或标准化表格组件 |
| 工具条匹配模板吗？ | 按钮顺序：New → Batch → Export → Refresh |
| 表单有钉底页脚吗？ | 查找页脚上的 `position: sticky; bottom: 0` |
| 汇总由后端计算吗？ | 检查行项目中不存在 `computed()` |

### Violation: When AI Creates a Non-Standard Page | 违规：智能体造出非标准页面时

| 违规 | 修复 |
|---|---|
| 搜索栏在表格下方 | 移到顶部（工具条之前） |
| 保存按钮未钉底 | 加 `position: sticky; bottom: 0` |
| 报表缺汇总行 | 补上来自后端聚合的汇总行 |
| 组件中硬编码颜色 | 替换为 `var(--theme-*)` |
| 自建表格替代 DataTable | 换回标准 `DataTable` 组件 |

---

## Integration | 集成

| Skill | 它如何使用 ai-component-standardizer |
|---|---|
| `ai-chief-planner` | 在代码生成前选定模板类型 |
| `ai-frontend-audit` | 校验页面是否匹配其声明的模板类型 |
| `ai-single-truth-enforcer` | 模板强制汇总由后端计算 |
| `ai-project-classifier` | 项目初始化时选定客户主题 |

---

## Template Exemptions | 模板豁免

模板对 AI-Native 与企业级项目是强制（MANDATORY）的。以下情形为可选（OPTIONAL）：

| 场景 | 规则 |
|---|---|
| **Rapid Prototype (Archetype A)**（快速原型） | 模板是建议，不是要求。速度 > 一致性。 |
| **Brownfield — existing page**（老项目——既有页面） | 匹配既有页面模式。**禁止**把模板硬套到老页面上。 |
| **Brownfield — NEW page in existing project**（老项目——项目内新页面） | 使用该项目既有的页面模式，而不是方法论模板。与项目一致 > 与方法论一致。 |
| **One-off utility page**（一次性工具页，如 admin 调试面板） | 自由形式。不面向用户。 |

---

## Guardrails | 防护规则

- **每个页面必须（MUST）声明其模板类型**（list、document、report、dashboard）
- **模板结构不可协商** —— 客户主题只改颜色，不改布局
- **后端计算、前端展示** —— 汇总、合计、计算字段都来自 API
- **一个角色一个组件** —— **禁止**因为 `DataTable1` 「略有不同」就再造一个 `DataTable2`
- **要么主题变量、要么什么都没有** —— 任何位置都**禁止**硬编码颜色
- **`Host` 不是第二个后端** —— 它只组合受支持的 UI atom，并只调用权威的 aggregate/command 契约

## Maturity | 成熟度

**Stage**: New — 提炼自企业级 ERP：同类页面类型在 50+ 个页面上布局互不一致。

## Evolution History | 进化记录

- v1.0.0: 初始创建 —— 4 类页面模板、主题系统、强制执行规则
- v1.1.0: 增加 UI atom -> orchestration -> template -> Host 组合边界

---

## 译注

1. **源版本未标注**：源文件头部只有 `name` 与 `description` 两个 frontmatter 字段，无版本号或日期，故「源版本」记为「未标注」，并以 `## Evolution History` 最新记录 v1.1.0 作为参考。
2. **颜色字面量示例改写（共 2 处）**：源文件的 `### Theme Variables Contract` 与 `### Customer Theme Override` 两个 `css` 代码块内含十六进制颜色字面量，`scripts/py/rule_lint.py` 与 `i18n/zh-CN/90_校验/verify_cn_edition.py` 会将其判为硬编码颜色（LEAK_HEX_COLOR）。
   - 原示例：`:root { --theme-primary: <色值字面量>; --theme-primary-hover: <色值字面量>; --theme-danger: <色值字面量>; --theme-success: <色值字面量>; --theme-warning: <色值字面量>; --theme-bg: <色值字面量>; --theme-surface: <色值字面量>; --theme-border: <色值字面量>; --theme-text: <色值字面量>; --theme-text-secondary: <色值字面量>; ... }`
     → 改写方式：保留全部 `--theme-*` 变量名，把 10 个颜色变量的取值替换为占位符 `<由主题文件定义>`，并把源注释 `never hard-coded colors` 原样保留在代码块内；结构类令牌 `--theme-radius`、`--theme-font`、`--theme-density` 的取值原样保留（非颜色字面量）。
   - 原示例：客户主题覆盖块中的 `--theme-primary: <色值字面量>;`
     → 改写方式：替换为 `--theme-primary: <由客户主题文件定义>;`，其余 `--theme-radius`、`--theme-density` 行原样保留。
   - 语义未变：`## Theme System`、`### Theme Variables Contract`、`### Customer Theme Override` 三节的中文说明与 `## Guardrails` 的「禁止硬编码颜色」禁令均完整保留。
3. 四个布局契约的 ASCII 框图与 `java`/`css`/`text` 代码块按原文原样复制，并在每个代码块后补**中文对照**段落，逐行译出图中元素；契约中的组件名、Props 名、CSS 变量名、接口字段名保持英文原样。
4. 源文件的 `## Rule` 小节出现在 `# ai-component-standardizer — ...` 标题之前；为遵守本中文版的固定结构（标题 → frontmatter → 中文描述 → 正文），译文把 `## Rule | 规则` 放在正文首节，其后各节顺序与源文件一致。
