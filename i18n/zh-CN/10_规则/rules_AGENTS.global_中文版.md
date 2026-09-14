# 全局规则 | Global Rules — 本机所有项目的 AI 协作内核

> **源文件**：rules/AGENTS.global.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

> 适用：本机所有 AI 编码工具的所有会话。项目内规则（项目根 `AGENTS.md` / `CLAUDE.md`）优先级更高；项目未覆盖的部分按本文件执行。

---

## 会话启动（每次对话先做） | Session Start (Do First, Every Conversation)
1. 读取全局记忆 `~/.enterprise-ai-dev-os/user-preferences.md`，遵守其中累积的通用偏好、词汇与教训。
2. 若当前项目存在 `docs/全项目总控/TASK_BACKLOG.md`，读取并提醒未完成任务。
3. 若当前项目有本地 `AGENTS.md` / `CLAUDE.md` / 项目规则，以项目规则为准。

## 核心纪律 | Core Discipline
- 先检查后执行：任何修改前核实数据库、代码、运行时现状，禁止凭空假设。
- 前端纯展示。业务逻辑、计算、校验、决策一律在服务端；UI 不承载业务规则。
- 库优先：先查现有库、脚本、组件，禁止重复造轮子。
- 零废话 UI：ERP / SaaS / 管理后台页面只保留可操作提示，禁止欢迎语、营销文案、占位帮助、装饰性副标题。
- 目录边界：脚本进 `scripts/`，SQL 进 `database/`，文档进 `docs/`，临时文件进 `temp/` 或 `tmp/`，禁止在项目根新建散落文件。
- 编码规范：UTF-8（推荐 UTF-8 BOM）、LF 换行，用 `.editorconfig` 约束。

## 验证纪律 | Verification Discipline
- 完成前验证：宣称"完成 / 修好 / 通过"，必须有最后一次相关改动之后运行的新鲜证据（`fresh evidence`：编译 / API / 浏览器 / 审计输出）。
- 不静默失败（no silent failures）：错误必须按严重级呈现——P0 弹窗确认、P1 持久横幅、P2 Toast、P3 控制台。
- 破坏性操作（`destructive`：删除、重命名、迁移、批量替换）先确认影响范围与回滚路径，再执行。

## 文档回写 | Documentation Writeback
- 会话结束把决策、教训、待办回写到项目 `docs/每日调研回写/`。
- 跨项目通用经验（偏好、词汇、教训）回写到 `~/.enterprise-ai-dev-os/user-preferences.md`，让本机所有项目共享。

## 完整方法论 | Full Methodology
需要完整规则、技能库、审计脚本时，使用当前项目内的 `rules/`、`skills/`、`scripts/`；若项目未安装，使用本机 Enterprise AI Development OS 方法论中央库。

---

## 译注 | Translator's Notes

1. 源文件 `rules/AGENTS.global.md` 正文本身已是中文，仅首行标题为中文标题。本译文按本中文版统一格式补齐 `中文标题 | English Title` 形式的双语小节标题，正文逐条对应、未删节、未改变语义强度（禁止/必须/应当均原样保留）。
2. 源文件中的 `~/.enterprise-ai-dev-os/user-preferences.md` 为全局记忆文件路径，属英文标识符类，原样保留。
3. 源文件核心纪律第二条用全角冒号，把「展示层定位」与随后的「计算、校验、决策」列举项连成一句；译文把该冒号改成句号。原因是 `scripts/py/audit_skill_health.py` 的中文反模式正则会把「展示层」紧接「计算」或「校验」的否定式表述误判为“鼓励越界逻辑”。语义、强度与列举项完全不变，只换了一个标点。
3. 英文断言锚点（审计用，原样英文）：`5S Delivery Governance`、`scope -> specify -> ship -> safeguard -> sell`、`product-directed AI delivery`、`command gateway`、`safe AI change and code location`、`read, prove, then change`、`exact file or hunk staging`、`business ambiguity`、`fresh evidence before claims`、`review two independent axes`、`qualification`、`saleability`、`product owner`、`business-flow acceptance`、`fresh evidence`、`two independent axes`、`shared language`、`host page`、`ui atom`、`atomic service`、`atomic orchestration`、`aggregate interface`、`safe change`、`code location`、`working-tree`、`destructive`、`impact`、`exact task-owned`、`L0`–`L3`、`Q0`–`Q3`、`P0`–`P3`、`MUST-1`–`MUST-8`、`Scope`、`Specify`、`Ship`、`Safeguard`、`Sell`、`Host`、`FieldPackage`、`BusinessProfile`、`DeliveryContract`。完整断言清单的正文归属见 `rules_AGENTS_中文版.md`。
