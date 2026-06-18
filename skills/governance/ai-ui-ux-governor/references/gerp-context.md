# GERP Project Context (UI/UX)

Stack:
- Vue 3 + Vite + TypeScript
- Element Plus UI
- Fonts in use (see Login.vue): HarmonyOS Sans SC, MiSans, Source Han Sans SC
- Theme initialization: frontend/gerp-web/src/theme (reuse existing tokens)

Constraints:
- Use project base components (BasePage, BasicDataLayout, BaseTable, PageToolbar, ConditionBar, etc.).
- Prefer Composition API with <script setup>.
- Avoid adding new UI libraries; use Element Plus and existing styles.
- Keep changes incremental; avoid large rewrites.
- ERP business pages are action-first: expose toolbar, condition bar, table, form, primary result, operation entries, and status semantics before explanatory copy.
- Business semantics should be carried by buttons, operation columns, status tags, related-document links, shortcuts, and drawers instead of long paragraphs.
- Do not add large hero areas, long intro text, or oversized explanation blocks to list/history pages and other data-heavy ERP screens.
- Guidance should be compressed into one-line tips, tooltips, drawers, or help entries; do not let text occupy the first screen or replace interaction structure on an ERP operation page.
- The login page may use concise trust/brand copy, but that exception must not be expanded into ordinary business pages.
- Table-heavy pages should preserve data display space first: reduce inter-section gaps, category-tree/table gaps, filter container padding, pagination container padding, and page gutters through shared tokens or base components. Do not solve density by adding page-local overrides unless the base component cannot express the page type.
- When a user clicks an action and the action is blocked by business rules, permissions, version restrictions, read-only state, missing upstream data, or missing route identifiers, the frontend must use `feedback.blocking(...)` so the user sees a modal with an explicit confirm button. Do not downgrade these cases to a disappearing toast. Validation errors, empty-data export reminders, duplicate-row hints, and degraded fallback notices should remain as warning or inline feedback.

Entry points to inspect:
- Login: frontend/gerp-web/src/components/Login.vue
- Theme: frontend/gerp-web/src/theme
- Layout: check existing layout components if present (BasePage/BasicDataLayout).

---

## 报表/统计页面规范（强制）

1. **模板选用**: 统计报表页统一使用 `ReportTemplatePage`，不得使用 `BasePage` 或 `BasicDataLayout`。传 `page-key`（`ReportTemplatePage` 的约定 prop）。
2. **维度切换**: 多维度统计（按商品/客户/品牌/区域等）使用 `SecondaryTabs` 承载，Tab 切换时保留筛选条件上下文（日期范围等公共参数）。
3. **默认视图**: 报表页打开默认展示**表格**视图，图表视图作为 `view-options` 中的辅助切换项。
4. **表格要求**: 必须包含序号列（`:show-index="true"`）、数量列（可点击下钻到明细）、金额列、合计行（`footer-summary` slot）。分页必须开启（默认每页 20 条）。
5. **分类筛选**: 商品/客户维度报表页须在左侧提供分类树侧边栏筛选（使用分类树数据 + 前端本地过滤），宽度 220px，不参与服务端分页。
6. **筛选条件复用**: 各维度 Tab 共享日期范围、品牌、仓库等公共筛选条件，维度特有筛选（如"来源"维度的 `sourceType`）仅在其 Tab 内出现。

## 表格单元格可点击下钻

1. **标示方式**: 可点击下钻的列在列配置中设置 `cellClickable: true`。
2. **触发方式**: 点击单元格本身即可跳转，不额外放置图标或按钮。
3. **下钻目标**: 数量列点击后跳转到对应明细查询页（如 `SalesDetailQuery`），自动带入维度筛选条件（商品 ID / 客户 ID / 品牌 ID / 仓库 ID / 职员 ID + 时间范围）。
4. **视觉反馈**: 可点击列的文字颜色使用 `#409eff`，hover 时加下划线。

## 组件缺失时的扩展原则

1. **优先级**: 项目封装组件 → Element Plus 原生组件 → 自建新组件。
2. **使用原生组件前提**: 确认项目 `components/` 下无对应封装，并在代码中标注 `<!-- TODO: 待封装为项目组件 -->`。
3. **新组件放置**: `components/base/`（通用基础组件）或 `components/<module>/`（业务专用组件）。
4. **禁止大面积绕过**: 一个页面中直接使用 Element Plus 原生组件的次数不得超过 3 处，超过则必须先封装。
---

## 生产计划工作台规范

1. **页面定位**: 生产计划页为"生产计划工作台"，汇集销售驱动、预测补货、手工排产、BOM/MRP驱动、订单驱动等多来源计划。
2. **下推链路**: 
   - 生产计划（已审核/已下达）→ 生成生产工单（`ProductionOrder`）
   - 生产计划（已审核/已下达，且来源为 BOM/销售/订单）→ 生成采购申请（根据 BOM 计算物料短缺）
3. **仪表盘**: 顶部摘要卡展示待审核/已审核/执行中/已完成/计划量/合计，物料短缺时显示预警条。
4. **高可用性要求**:
   - 所有异步操作必须有 `try/catch` + `feedback.error`
   - 数据加载失败自动重试（最多 3 次，间隔递增）
   - 提供"重试"和"忽略"按钮
   - 搜索条件变化时 300ms 防抖
   - 组件卸载时清理所有 timer
