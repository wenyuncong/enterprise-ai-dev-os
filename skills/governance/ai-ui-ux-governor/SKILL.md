---
name: ai-ui-ux-governor
description: "Govern enterprise UI/UX density, zero-fluff wording, action semantics, states, hierarchy, usability, visual consistency, and design-system fit. Use when designing or reviewing ERP/SaaS/admin pages, forms, dashboards, reports, and operational workflows."
---

# ai-ui-ux-governor — Enterprise UI/UX Design System Governor

## Purpose | 用途

Govern enterprise application UI/UX consistency across all pages:

- Layout taxonomy enforcement (list, form, report, workbench, settings)
- Density and spacing consistency
- State handling (loading, empty, error, edge cases)
- Action-first expression for operations tools
- Theme and token governance
- Performance UX standards

This skill is for **design system governance**, not pixel-level design. It applies to ERP, SaaS admin, operations dashboards, and any data-heavy enterprise tool.

## Core Rule | 核心规则

**Enterprise operation pages are action-first screens, not marketing pages.**

Show toolbar, actions, status indicators, and data before explanatory text. Express business meaning through controls and structure — buttons, status tags, process links — not prose paragraphs.

---

## Layout Taxonomy | 页面布局分类

Every enterprise page falls into one of these types. Each has a required layout bias:

| Page Type | Required Layout | Key Elements |
|---|---|---|
| **List / History** | filter bar + toolbar + table + batch actions + drilldown | Search, status filters, CRUD actions, pagination |
| **Document / Form** | header fields + line items + summary + pinned footer actions | Field groups, validation, save/submit actions |
| **Report / Analytics** | dimension tabs + default table + chart toggle + summary row | Filters, drilldown, export |
| **Workbench / Dashboard** | summary cards + todo list + quick actions | Aggregated metrics, shortcuts |
| **Settings / Parameters** | grouped fields + toggles + defaults + compact help | Configuration, system params |

**Violation**: If a list page has a hero banner, or a settings page has multi-paragraph explanations, it's using the wrong layout pattern.

---

## Zero-Fluff Rule | 零废话规则

For ERP, SaaS admin, and operations tools, remove ALL content that does not directly assist task completion:

| Remove | Keep |
|---|---|
| Welcome messages | Field labels |
| Marketing copy | Validation rules |
| Placeholder help text | Inline tooltips |
| "How to use this page" blocks | Constraint hints (e.g., encoding rules) |
| Feature descriptions | Action buttons |
| Page-level tutorials | Status indicators |

**Exception**: Login pages and public-facing portals may carry brief brand/trust copy. This exception does NOT extend to internal operation pages.

---

## State Handling | 状态处理

Every data-driven view must handle four states explicitly:

| State | Visual | When |
|---|---|---|
| **Loading** | Skeleton or spinner in stable container | Data fetch in progress |
| **Empty** | Contextual empty illustration + optional CTA | No data exists |
| **Error** | Error message + retry action | Fetch or action failed |
| **Edge Cases** | Graceful handling | Max-length text, null values, special chars |

**Rule**: Do not use row-by-row loading skeletons or staggered animations for ERP tables. Use one stable loading state for the whole table.

---

## Density Standards | 密度标准

Enterprise operation pages should default to compact density:

| Element | Guideline |
|---|---|
| Page padding | ~4px |
| Section gaps | ~3px |
| Toolbar button height | ~26px |
| Table action buttons | ~22px |
| Filter/search buttons | ~24px |
| Pagination gutter | ~4-6px |

**Page shells** (list, document, report templates) must enforce these via shared tokens, not page-local CSS.

---

## Table Viewport Rule | 表格视区规则

Every data table must consume available page height:

- Table body owns vertical scrolling
- Primary actions and pagination pinned to bottom
- Footer order: horizontal scrollbar → summary row → pagination
- Table totals in footer area, aligned with columns
- No detached right-bottom statistic blocks as substitute for column-aligned totals

**Acceptance**: Verify four states — few rows, many rows, many columns with horizontal scroll, pagination + summary together.

---

## Theme Governance | 主题治理

| Rule | Detail |
|---|---|
| **Token-driven** | All visual values from CSS variables, not hard-coded |
| **No page-local overrides** | Page-local CSS for branding or theme tokens is forbidden |
| **Multi-theme testing** | Verify all supported themes before merging visual changes |
| **Scrollbar consistency** | Use theme tokens for scrollbar styling, not hard-coded colors |

---

## Performance UX | 性能UX

Usability includes runtime smoothness:

| Rule | Detail |
|---|---|
| **Pagination first** | Server-side pagination before adding more columns |
| **Batch over serial** | Batch API calls instead of row-by-row requests |
| **Virtualization** | Virtual scrolling for large lists (>100 rows) |
| **No duplicate requests** | Loading/retry/polling must not spawn concurrent requests |
| **Component splitting** | Long forms split into orchestration, line tables, summaries |
---

## Notification Severity Policy | 通知分级策略

Every user-facing notification MUST match its severity level. Wrong severity destroys trust and causes data loss.

| Level | Name | UX Pattern | Auto-Dismiss | Example |
|---|---|---|---|---|
| **P0** | Critical / Destructive | **Modal** with confirm/cancel buttons | Never | Delete all records, irreversible action, plan change |
| **P1** | Important / Action Required | **Persistent banner** or modal with action button | Never | Payment failed, session expired, sync error |
| **P2** | Informational / Success | **Toast** with optional undo | 4-6 seconds | Save successful, file uploaded, settings saved |
| **P3** | Debug / Transient | Console log or silent | N/A | Cache updated, analytics event |

### Anti-Patterns (Common AI Mistakes)

| ❌ Wrong | Severity Mismatch | ✅ Correct |
|---|---|---|
| showToast('Deleted') after delete all | P0 action → P2 notification | Modal: "Delete 500 records? This cannot be undone." |
| ElMessage.error('Save failed') that disappears | P1 action → P2 notification | Persistent banner: "Save failed. [Retry] [Details]" |
| ElMessageBox.confirm('Field changed') on every input | P2 action → P0 notification | Silent save or no confirmation needed |
| Flash-toast on form validation error | P1 → P2 | Inline error under the field, stays until fixed |

### Implementation Contract

`	ypescript
// Every notification system must expose these:
interface NotificationAPI {
  modal(config: ModalConfig): Promise<boolean>;     // P0: returns user choice
  banner(config: BannerConfig): { dismiss(): void }; // P1: persistent, dismissable
  toast(config: ToastConfig): void;                  // P2: auto-dismiss
  debug(message: string): void;                       // P3: console only
}
`


---

## Standard Workflow | 标准工作流

1. **Classify the page** — which layout type?
2. **Identify violations** — zero-fluff, density, state handling, table viewport
3. **Check density** — measurements against compact standards
4. **Verify states** — loading, empty, error, edge cases
5. **Propose changes** — incremental, shared-component-based, not page-local rewrites

---

## Guardrails | 防护规则

- Do not reuse a single layout template across all page types
- Do not solve layout problems with page-local CSS — fix the shared shell
- Do not add decorative text to ERP pages (zero-fluff rule)
- Do not use animations for table loading on data-heavy pages
- Do not hard-code scrollbar, hover, or theme colors in page CSS
- Do not override theme tokens for page-local branding

## Maturity | 成熟度

**Stage**: Effective — Extracted from 19KB enterprise ERP UI/UX governance with layout taxonomy and density standards.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-ui-ux (19KB original + 2 references)
- Source: Enterprise ERP UI/UX governance across 50+ page types

