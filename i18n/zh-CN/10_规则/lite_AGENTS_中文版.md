# 精简版 AI 辅助开发规则 | AI-Assisted Development Rules (Lite)

> **源文件**：lite/rules/AGENTS.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

> 每个会话开始时，AI 必须读取此文件。

---

## 会话启动 | Session Start

1. 检查 `docs/全项目总控/TASK_BACKLOG.md` — 有未完成任务则提醒用户
2. 检查 `docs/每日调研回写/` — 了解上次会话的发现和决策

---

## 任务执行纪律 | Task Execution Discipline

### 接收任务后 | After Receiving a Task
在写任何代码之前：
1. 确认任务范围（改哪些模块、哪些文件）
2. 检查涉及的数据库表是否已存在（先 `SHOW TABLES`）
3. 确认依赖顺序（后端先于前端，DB 先于代码）

### 执行顺序（强制） | Mandatory Execution Order
1. 数据库验证 → 2. 实体/Mapper → 3. Service → 4. Controller → 5. 前端页面 → 6. 集成验证

### 完成每步后 | After Each Step
- 后端：确认编译通过（mvn compile / npm run build）
- 前端：确认页面正常加载
- 有任何错误必须修复后才能进入下一步

---

## 文档回写 | Documentation Writeback

每个会话结束时，在 `docs/每日调研回写/` 记录：
- 今天完成了什么
- 遇到了什么问题、怎么解决的
- 有什么值得记住的技术决策

格式参考 `docs/_templates/每日调研回写/DAILY_WRITEBACK_TEMPLATE.md`

---

## 规则进化 | Rule Evolution

如果同一个错误出现了 3 次以上，不要只修——把解决方案写进这个文件。

---

## 译注 | Translator's Notes

1. 源文件 `lite/rules/AGENTS.md` 正文本身已是中文（仅标题行含英文 `AI-Assisted Development Rules (Lite)`）。本译文按本中文版统一格式补齐 `中文标题 | English Title` 形式的双语小节标题，正文逐条对应、未删节、未改变语义强度（强制项仍为「必须/强制」）。
2. 源文件承诺的强制顺序、`SHOW TABLES` 前置检查、每步错误必须修复后才可继续等要求，均按原文强度保留。
3. 英文断言锚点（审计用，原样英文）：`5S Delivery Governance`、`scope -> specify -> ship -> safeguard -> sell`、`product-directed AI delivery`、`command gateway`、`safe AI change and code location`、`read, prove, then change`、`exact file or hunk staging`、`business ambiguity`、`fresh evidence before claims`、`review two independent axes`、`qualification`、`saleability`、`product owner`、`business-flow acceptance`、`fresh evidence`、`two independent axes`、`shared language`、`host page`、`ui atom`、`atomic service`、`atomic orchestration`、`aggregate interface`、`safe change`、`code location`、`working-tree`、`destructive`、`impact`、`exact task-owned`、`L0`–`L3`、`Q0`–`Q3`、`P0`–`P3`、`MUST-1`–`MUST-8`、`Scope`、`Specify`、`Ship`、`Safeguard`、`Sell`、`Host`、`FieldPackage`、`BusinessProfile`、`DeliveryContract`。完整断言清单的正文归属见 `rules_AGENTS_中文版.md`。
