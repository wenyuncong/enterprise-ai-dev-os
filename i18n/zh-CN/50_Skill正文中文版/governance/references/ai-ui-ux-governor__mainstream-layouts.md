# 主流 ERP 布局要点 | Mainstream ERP Layout Notes

> **源文件**：skills/governance/ai-ui-ux-governor/references/mainstream-layouts.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-ui-ux-governor` 的配套参考文件中中文对照版，不是正式加载源。

---

来源（官方设计系统）：

- SAP Fiori：Shell Bar + Dynamic Page 模式（全局页头 + 以内容为中心的页面）
- Microsoft Fluent：NavigationView（分区左侧导航，自适应）
- Dynamics 365 设计原则：清晰、一致、高效、降低认知负荷

关键结论：

1. 常驻全局页头，承载身份、搜索与个人资料操作。
2. 一级模块使用左侧导航；压缩层级深度；对分区分组。
3. 内容页使用页头区域承载关键操作与状态，其后是可滚动的内容区块。
4. 数据密集页面：摘要 KPI 置于筛选与表格之上；筛选始终保持可达。
5. 响应式行为：收起导航，并保留首要行动召唤（primary call-to-action）。

链接：

- [SAP Fiori Shell Bar](https://experience.sap.com/fiori-design-web/shell-bar/)（SAP Fiori 顶栏）
- [SAP Fiori Dynamic Page](https://experience.sap.com/fiori-design-web/dynamic-page/)（SAP Fiori 动态页面）
- [Microsoft NavigationView](https://learn.microsoft.com/en-us/windows/apps/design/controls/navigationview)（微软导航视图）
- [Dynamics 365 design principles](https://learn.microsoft.com/en-us/dynamics365/get-started/design)（Dynamics 365 设计原则）
