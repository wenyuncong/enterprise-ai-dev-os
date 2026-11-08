# Enterprise Page Patterns | 企业级页面通用模式

> Scope: universal. This reference states reusable page patterns in layer-neutral terms.
> No language, framework, component library, project, or business domain is named; all
> visual values refer to design tokens, never hard-coded colors.

---

## 1. Report / Analytics Page Contract (Mandatory) | 报表/分析页规范

1. **Template selection**: report and analytics pages use the report template of the
   component system, not the generic list or document shell, identified by a declared page key.
2. **Dimension switching**: multi-dimension statistics (by any entity the adopting project
   defines) are carried by a secondary tab control; switching tabs preserves shared filter
   context such as date ranges.
3. **Default view**: the page opens on the **table** view; the chart view is an auxiliary
   toggle among the view options.
4. **Table requirements**: a sequence column, measurable columns (with drill-down where
   applicable), amount columns, and a summary row in the table footer. Pagination is enabled
   by default.
5. **Category filtering**: where a category hierarchy applies, a stable-width category tree
   is provided as a side filter driven by hierarchy data; it does not participate in
   server-side pagination.
6. **Filter reuse**: shared filters (date range, brand-equivalent, location-equivalent) are
   common across dimension tabs; dimension-specific filters appear only inside their own tab.

---

## 2. Drill-Down from Table Cells | 表格单元格下钻

1. **Indication**: columns that support drill-down are marked in the column configuration.
2. **Trigger**: clicking the cell itself navigates; no extra icon or button is required.
3. **Target**: measurable columns navigate to the corresponding detail view, automatically
   carrying the dimension filters (entity identifiers plus time range).
4. **Visual feedback**: clickable text uses the theme's interactive-color token and an
   affordance on hover. A hard-coded color is prohibited.

---

## 3. Extension Priority When a Component Is Missing | 组件缺失时的扩展优先级

1. **Priority order**: shared/base components → platform-native components → newly built components.
2. **Native-use condition**: confirm no shared component exists, and mark the location in
   the code with a tracked TODO to encapsulate it later.
3. **Placement of new components**: a shared base folder for generic components, or a
   domain folder for specialized ones.
4. **No broad bypass**: repeated direct use of native components beyond a small, defined
   threshold requires encapsulating a shared component first.

---

## 4. Reliability for Asynchronous Operations | 异步操作可靠性

1. Every asynchronous operation uses explicit error handling with user-facing error feedback.
2. Data-load failures retry automatically up to a defined maximum with increasing intervals,
   and offer explicit retry / dismiss actions.
3. Search input changes use a defined debounce.
4. All timers are cleaned up when the component is disposed.

---

## 5. Blocking Feedback | 阻塞反馈

When an action is blocked by rules, permissions, version restrictions, read-only state,
missing upstream data, or missing route identifiers, the page raises a blocking modal with
an explicit confirm button — it never downgrades to a disappearing toast. Validation errors,
empty-export reminders, duplicate-row hints, and degraded fallback notices remain inline or
warning-level feedback. See the main SKILL.md for the severity policy.
