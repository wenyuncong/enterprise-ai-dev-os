# TASK BACKLOG — Task Anti-Amnesia Tracker

> **Purpose**: Prevent task loss when users jump between tasks. Every task is recorded.
> **Rule**: Check this file at the START of every session. Update at the END of every session.
> **Never**: Start a new task without checking if old ones are unfinished.

---

## Active Tasks | 进行中

| ID | Task | Started | Status | Last Activity | Priority |
|---|---|---|---|---|---|
| | | | | | |

## Pending Tasks | 待处理

| ID | Task | Created | Priority | Blocked By |
|---|---|---|---|---|
| GERP-AUDIT-01 | ERP 发布 SQL 覆盖门禁缺口登记：仅记录今天检查出的缺口，当前不处理、不作为发版前硬要求 | 2026-06-21 | Later | 等本项目有客户、资金恢复或专项治理窗口 |
| GERP-AUDIT-02 | ERP AI/MCP 单据命令主链缺口登记：仅记录 AI/MCP runtime profile / command dry-run 未完全接回统一后端命令入口 | 2026-06-21 | Later | 等本项目有客户、资金恢复或 AI 能力专项治理窗口 |
| GERP-AUDIT-03 | ERP 新代码架构准入门禁：从现在开始，新增/修改代码不得扩大跨域 mapper/entity import、裸 JdbcTemplate、字段静态回退 | 2026-06-21 | P0-now | 后续每次功能/修复必须执行 |
| GERP-AUDIT-04 | ERP P0 页面 FieldPackage 静态回退治理：记录采购/销售/库存/收付款核心页静态回退问题，当前不强行统一迁移 | 2026-06-21 | Later | 等本项目有客户、资金恢复或专项治理窗口 |
| GERP-AUDIT-05 | ERP 跨模块直连与 JdbcTemplate 白名单化：记录历史债务，只冻结新增债务，历史债务后期分批处理 | 2026-06-21 | Later | 等本项目有客户、资金恢复或专项治理窗口 |

## Recently Completed | 最近完成

| ID | Task | Completed | Notes |
|---|---|---|---|
| AI-NATIVE-GOV-01 | 全 AI 原生候选能力评估与验证协议 | 2026-08-09 | 将网页、Skill、工具输出等从可信标签判断升级为项目适配评估、受控验证、授权委托和执行证据契约 |
| AI-NATIVE-GOV-02 | 可执行交付契约门禁 | 2026-08-21 | 新增任务写入范围、阶段准入、新鲜证据与独立双轴复核的 Schema、Skill、校验器和场景回归 |
| BUG-01 | Rule 14: No test = not done 强制完成门禁 | 2026-06-17 | AGENTS.md §6 + verify.js --project-root 自动归档 |
| P5-ALL | P5 工作任务系统 | 2026-07-05 | 5 个原子 (inbox.receive, inbox.classify, task.transition, plan.generate, plan.adjust) + DigitalLifeService 集成 (daily_work_plan/get_daily_plan/execute_daily_plan) + tick_runtime 增强 + 51 测试 |
| TOOL-01 | Multi-tool deploy adapter | 2026-06-17 | tools/adapters.json + tools/deploy.ps1，已部署5个工具 |
| VERIFY-01 | verify.js 增强 | 2026-06-17 | 新增 --project-root 参数，自动保存证据到 docs/测试验收报告/ |
| VALUE-01 | 客户/投资人价值说明文档 | 2026-06-20 | docs/公开材料/CUSTOMER_INVESTOR_VALUE.md，已通过公开边界与方法论审计 |
| PROMO-01 | 图文推广文章 DOCX/PDF | 2026-06-21 | docs/公开材料/推广文章/，3 篇文章各含 docx/pdf/png，已通过基础内容校验 |

---

*Last updated: 2026-08-21*
