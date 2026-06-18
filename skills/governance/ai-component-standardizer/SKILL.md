---
name: ai-component-standardizer
description: "Enforce standard page and component templates, theme variables, layout contracts, action placement, and reusable UI patterns. Use when creating or reviewing list pages, document forms, reports, dashboards, or enterprise frontend components."
---

# ai-component-standardizer — Component & Page Template Standardization Engine

## Purpose | 用途

Define and enforce standardized component/page templates for both backend and frontend. Stop AI from reinventing the layout for every new page. Every list page looks the same. Every form page follows the same pattern. Every report page uses the same structure. Theme support for customer-level customization without breaking standards.

**Problem it solves**: AI creates each page from scratch with different layouts, different button placements, different field arrangements. One customer gets a sidebar form, another gets a modal. One list page has search at the top, another at the bottom. This is chaos, not a product.

---

## The Page Type Taxonomy | 页面类型分类

Every enterprise page MUST fit one of these templates. No exceptions.

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

---

## Template 1: List/Table Page | 资料列表页

**Use when**: Displaying a searchable, filterable list of records with CRUD actions.

### Layout Contract (MUST follow)

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

### Component Contract
| Position | Component | Props |
|---|---|---|
| Filter Bar | `SearchInput` + `FilterDropdown[]` + `DateRangePicker` | `searchPlaceholder`, `filters`, `onSearch` |
| Toolbar | `ActionButton[]` | `label`, `icon`, `onClick`, `variant` |
| Table | `DataTable` with `columns[]` | `data`, `loading`, `emptyText`, `onRowClick` |
| Row Actions | `RowActions` | `actions[]` with `icon`, `label`, `onClick`, `visible` |
| Pagination | `Pagination` | `current`, `total`, `pageSize`, `onChange` |

### Backend Contract
```java
// Every list page endpoint returns this exact shape:
{
  "data": [...],        // Array of records
  "total": 156,         // Total count for pagination
  "page": 1,            // Current page
  "pageSize": 20        // Page size
}
```

---

## Template 2: Document/Form Page | 单据录入页

**Use when**: Creating or editing a single record with header info + line items + footer actions.

### Layout Contract

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

### Critical Rules
- Footer action buttons are **pinned to bottom**, always visible
- Summary bar updates in real-time from backend (never computed in frontend)
- Line items have inline add/remove, not separate modal

---

## Template 3: Report/Analytics Page | 报表页

**Use when**: Displaying aggregated data with charts and export capability.

### Layout Contract

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

---

## Template 4: Dashboard/Workbench | 工作台

**Use when**: Landing page showing aggregated metrics and quick actions.

### Layout Contract

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

---

## Theme System | 主题系统

Different customers require different visual themes. The template structure stays the same; only CSS variables change.

### Theme Variables Contract
```css
:root {
  /* Every template component MUST use these variables, never hard-coded colors */
  --theme-primary: #2563eb;
  --theme-primary-hover: #1d4ed8;
  --theme-danger: #dc2626;
  --theme-success: #059669;
  --theme-warning: #d97706;
  --theme-bg: #f9fafb;
  --theme-surface: #ffffff;
  --theme-border: #e5e7eb;
  --theme-text: #111827;
  --theme-text-secondary: #6b7280;
  --theme-radius: 6px;
  --theme-font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --theme-density: compact;   /* compact | comfortable | spacious */
}
```

### Customer Theme Override
Each customer gets a theme file that overrides ONLY the variables they need:
```css
/* customer-acme-theme.css */
:root {
  --theme-primary: #e63946;
  --theme-radius: 4px;
  --theme-density: compact;
}
```

---

## Enforcement | 强制执行

### Detection: Is this page using a standard template?

| Check | Method |
|---|---|
| Page has filter bar? | Check for `.filter-bar` or `SearchInput` component |
| Table uses DataTable? | Check for `<DataTable` or standardized table component |
| Toolbar matches template? | Button order: New → Batch → Export → Refresh |
| Form has pinned footer? | Check for `position: sticky; bottom: 0` on footer |
| Summary computed by backend? | Check for no `computed()` in line items |

### Violation: When AI Creates a Non-Standard Page

| Violation | Fix |
|---|---|
| Search bar below table | Move to top (before toolbar) |
| Save button not pinned | Add `position: sticky; bottom: 0` |
| Report without summary row | Add summary row from backend aggregation |
| Hard-coded colors in component | Replace with `var(--theme-*)` |
| Custom table instead of DataTable | Replace with standard DataTable component |

---

## Integration | 集成

| Skill | How it uses ai-component-standardizer |
|---|---|
| `ai-chief-planner` | Selects template type before code generation |
| `ai-frontend-audit` | Verifies pages match their declared template type |
| `ai-single-truth-enforcer` | Template enforces backend-computed summaries |
| `ai-project-classifier` | Customer theme selection during project setup |

---


## Template Exemptions | 模板豁免

Templates are MANDATORY for AI-Native and Enterprise projects. They are OPTIONAL for:

| Scenario | Rule |
|---|---|
| **Rapid Prototype (Archetype A)** | Templates are suggestions, not requirements. Speed > consistency. |
| **Brownfield — existing page** | Match existing page patterns. Don't force template on old pages. |
| **Brownfield — NEW page in existing project** | Use the project's existing page patterns, not the methodology template. Consistency with the project > consistency with methodology. |
| **One-off utility page** (e.g., admin debug panel) | Free form. Not user-facing. |

---

## Guardrails | 防护规则

- **Every page MUST declare its template type** (list, document, report, dashboard)
- **Template structure is non-negotiable** — customer themes change colors, not layout
- **Backend computes, frontend displays** — summaries, totals, computed fields come from API
- **One component per role** — don't create DataTable2 because DataTable1 is "slightly different"
- **Theme variables or nothing** — no hard-coded colors anywhere

## Maturity | 成熟度

**Stage**: New — Extracted from enterprise ERP where 50+ pages had inconsistent layouts across the same page types.

## Evolution History | 进化记录

- v1.0.0: Initial creation — 4 page templates, theme system, enforcement rules
