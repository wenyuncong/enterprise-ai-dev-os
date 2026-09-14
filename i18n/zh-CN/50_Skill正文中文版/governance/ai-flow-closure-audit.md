# `ai-flow-closure-audit` — 端到端业务流程闭环审计

> **源文件**：skills/governance/ai-flow-closure-audit/SKILL.md
> **源版本**：未标注（源文件无版本字段；`## Evolution History` 最新记录为 v1.2.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-flow-closure-audit
description: "Audit whether a business flow is closed across page, API, database, parameters, permissions, downstream writeback, reports, evidence, and regression tests. Use before declaring a business process complete or when checking end-to-end readiness."
```

**中文描述**：审计一条业务流程是否在 `page`、`API`、`database`、`parameters`、权限、下游 `writeback`、报表、证据与回归测试各个层面均已闭环。在宣布某个业务流程完成之前使用，或在检查端到端就绪度时使用。

---

## Rule | 规则

闭环审计检查：1) 任务有已定义的验收标准；2) 存在完成证据；3) 验证步骤已执行；4) 输出与预期输出一致；5) 无未解决问题残留。**禁止**在没有闭环证据的情况下标记完成。

## Purpose | 目的

审计一条业务链是否真正闭环——从入口层到 API、到数据库、到下游 `writeback`、再到报表。

**业务链五要素（按源文件实际用词原样保留英文）**：`Page`（入口页；源文件用词为 `page` 与层级名 `Entry/UI`）、`API`、`DB`（源文件用词为 `database`）、`parameter`（源文件用词为 `parameters` / `switches`）、`writeback`。缺任一层的证据，闭环判定即不成立。

闭环判定链：`Page` → `API` → `DB` → `parameter` → `writeback`。

本 Skill 检出以下缺口：
- 某个入口动作没有后端校验
- 某次数据库写入没有下游 `writeback`
- 业务规则只存在于前端代码里
- 报表查询的是过期或不完整数据
- 参数/开关（`parameter`/switch）未被正确消费

**核心原则**：没有每一层的证据，就**禁止**称一条流程「已闭环」。

---

## Audit Layers | 审计层级

只有**所有**层都有证据时，一条业务链才算「闭环」：

| 层 | 检查项 | 所需证据 | 缺失时的缺口等级 |
|---|---|---|---|
| **Entry/UI** | 动作可用？校验正确？ | 截图或页面验证 | P2（UX 缺口） |
| **API** | 端点存在？方法/鉴权正确？ | curl 测试、API 响应日志 | P0（阻断） |
| **Service/Logic** | 业务逻辑完整？有事务边界？ | 代码评审 + 单元测试 | P0（阻断） |
| **Database** | 表/列正确？约束齐全？ | `DESCRIBE` + `SELECT` 抽样 | P0（阻断） |
| **Parameters/Switches** | 配置被正确消费？ | 参数审计、开关检查 | P1（数据风险） |
| **Writeback** | 下游真相已更新？ | 端到端数据流追踪 | P1（数据风险） |
| **Report/Analytics** | 报表反映 `writeback`？ | 查询比对、新鲜度检查 | P1（数据风险） |
| **Audit/Evidence** | 动作已记录？轨迹完整？ | 审计日志验证 | P2（合规） |
| **Product Acceptance** | 目标用户能否高效完成真实业务流程？ | product owner 验收记录 | P1（交付风险） |

---

## Business Chain Categories | 业务链分类

| 业务链 | 描述 | 典型范围 |
|---|---|---|
| O2C (Order to Cash) | 销售订单 → 发货 → 开票 → 收款 | 销售、库存、财务 |
| S2P (Source to Pay) | 采购申请 → 订单 → 收货 → 付款 | 采购、库存、财务 |
| R2R (Record to Report) | 交易 → 总账 → 财务报表 | 财务、报表 |
| L2C (Lead to Cash) | 线索 → 商机 → 报价 → 订单 | CRM、销售 |
| Fulfillment | 订单 → 拣货 → 打包 → 发运 | WMS、物流 |
| Subscription | 注册 → 激活 → 计费 → 续订/取消 | SaaS、计费 |

---

## Standard Workflow | 标准工作流

### Step 1: Map the Chain | 第 1 步：绘制业务链

- 识别所有节点：entry → API → service → DB → writeback → report
- 识别影响该业务链的所有参数/开关（`parameter`/switch）
- 记录预期的状态流转

### Step 2: Verify Each Node | 第 2 步：逐节点验证

对每个节点收集具体证据：
- **Entry**：可用动作的截图，验证表单校验
- **API**：带预期状态码与响应体的 `curl` 响应
- **Service**：对业务逻辑路径与事务边界的代码评审
- **Database**：`DESCRIBE table`，以及动作前后的样例行
- **Writeback**：从源表到下游表的数据追踪
- **Report**：查询报表输出，并与源数据新鲜度比对
- **Product acceptance**：执行 product owner 定义好的 business-flow 测试，并记录 accept/reject/revise 反馈

### Step 2b: Write-back Consistency Cross-check | 回写一致性交叉校验

只有当数字在各层之间对账一致时，一次 `writeback` 才算闭环。对于任何会移动数量、金额、余额或状态的流程，都要增加**一致性交叉校验（consistency cross-check）**：扫描不匹配项，而不是只信一行采样：

1. **Map the reconciliation pairs（映射对账对）**：为每一次 `writeback` 列出源表 → 下游表（例如一次收货同时增加库存与应付）。
2. **Design the check（设计校验）**：独立聚合每一侧并比对；对计算值（平均数、余额）还要从原始行重新计算。
3. **Run a full-table scan（跑全表扫描）**：定位源与下游不一致的行；一次全扫常能暴露采样式检查漏掉的隐性漂移。
4. **Record the discrepancy（记录差异）**：表、行、预期值 vs 实际值，以及可能的根因。
5. **Fix and rerun（修复并重跑）**：修复后，交叉校验必须返回零不匹配才能收口。

```text
Example (domain-specific, from ERP): purchase receipt -> inventory + payable
  SELECT aggregate(inventory_qty) FROM inventory WHERE receipt_id = :id;
  SELECT aggregate(payable_amount) FROM payable WHERE receipt_id = :id;
  -- both must reconcile with the receipt line totals; any drift is a P1 data risk
```

这一步与技术栈、业务领域无关：模式就是「每一次 `writeback` 都要用交叉校验来对账，而不是抽样」，无论业务数字是什么。

### Step 2a: Review Two Independent Axes | 第 2a 步：独立审查 two independent axes

在宣布一条非平凡流程就绪之前，把这些发现分开保留：

| 轴 | 问题 | 最低证据 |
|---|---|---|
| **Standards / truth** | 改动是否遵循仓库标准、真相归属（source-of-truth ownership）、架构边界、安全/质量门禁以及所选定的 L0-L3 门禁？ | 范围内的 diff 评审、相关的审计/构建/测试/运行时证据 |
| **Product / spec** | 该流程是否交付了原始业务结果与验收步骤，且未违反显式非目标、未新增未经批准的行为？ | 产品契约、验收记录、实测行为 |

两轴互不掩盖。技术实现干净但遗漏业务结果的，审计不通过；行为正确但违反真相归属或架构边界的，同样不通过。

### Step 3: Identify Gaps | 第 3 步：识别缺口

业务链在哪里断了？按如下分级：
- **P0（阻断）**：缺少后端校验、API 损坏、缺表
- **P1（数据风险）**：`writeback` 不完整、报表过期、缺少 `parameter` 门控
- **P2（UX/合规）**：缺少审计轨迹、UI 行为不一致

### Step 4: Produce Fix Tasks | 第 4 步：产出修复任务

把每个缺口转成具体任务：

```markdown
| Gap | Severity | Root Cause | Fix Action | Acceptance |
|---|---|---|---|---|
| Submit has no backend validation | P0 | Missing service method | Implement validation in service | curl test passes |
| Inventory not updated on delivery | P1 | Missing writeback | Add inventory movement service | Inventory count matches |
```

---

## Evidence Collection Template | 证据收集模板

```markdown
## Flow: [Chain Name]

### Layer Evidence
| Layer | Status | Evidence | Notes |
|---|---|---|---|
| Entry/UI | ✅/❌/⚠️ | [Screenshot path] | [notes] |
| API | ✅/❌/⚠️ | [curl output] | [notes] |
| Service | ✅/❌/⚠️ | [Code reference] | [notes] |
| Database | ✅/❌/⚠️ | [SQL results] | [notes] |
| Writeback | ✅/❌/⚠️ | [Data trace] | [notes] |
| Report | ✅/❌/⚠️ | [Query comparison] | [notes] |
| Product acceptance | ✅/❌/⚠️ | [Business-flow test record] | [notes] |

### Two-Axis Review
| Axis | Status | Evidence | Blockers / Notes |
|---|---|---|---|
| Standards / truth | ✅/❌/⚠️ | [diff, audit, test, runtime evidence] | [notes] |
| Product / spec | ✅/❌/⚠️ | [outcome, acceptance, non-goals evidence] | [notes] |

### Gap Summary
- P0: [count] blockers
- P1: [count] data risks
- P2: [count] UX/compliance issues
```

---

## Guardrails | 防护规则

- **禁止**在没有每一层证据的情况下声称闭环
- **禁止**把「前端会处理」当作业务规则的闭环
- **禁止**跳过 `writeback` 验证——它是最常见的隐性缺口
- **禁止**凭想象审计——必须对照真实运行的代码与数据库验证
- **禁止**在没有数据库/`writeback` 验证的情况下，把一次通过的 API 测试当作完整闭环
- **禁止**用技术验证替代 product owner 的 business-flow acceptance
- **禁止**把 standards/truth 的发现与 product/spec 的发现合并；两轴必须独立上报、独立解决
- **禁止**用过期输出或智能体报告作为闭环证据；必须在最终相关改动之后重跑能证明该断言的检查（fresh evidence）

## Maturity | 成熟度

**Stage**：Effective —— 提炼自企业级 ERP 在采购/销售/库存/财务各链路上的流程闭环审计。

## Evolution History | 进化记录

- v1.0.0：从 gerp-flow-closure-audit 提炼（原始 12.5KB）
- v1.1.0：泛化为通用业务链闭环框架
- v1.2.0：新增 product owner 的 business-flow acceptance 作为显式闭环层
- Source：企业级 ERP 中的 O2C、S2P、R2R 业务链审计
