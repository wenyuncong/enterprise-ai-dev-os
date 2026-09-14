# `ai-domain-boundary-mapper` — 领域边界与对象归属映射

> **源文件**：skills/governance/ai-domain-boundary-mapper/SKILL.md
> **源版本**：未标注（源文件无版本字段；`## Evolution History` 最新记录为 v1.1.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-domain-boundary-mapper
description: "Map domain boundaries, object ownership, source-of-truth placement, write paths, read consumers, schema ownership, and cross-domain risks. Use when data, identity, permissions, documents, reports, or business objects cross module boundaries."
```

**中文描述**：映射领域边界、对象归属、真相源置放、写入路径、读取消费方、模式（schema）归属与跨域风险。当数据、身份、权限、单据、报表或业务对象跨模块边界时使用。

---

## Purpose | 目的

在对象级映射领域边界：

- 每个身份概念归哪个领域所有？
- 每个主数据对象归哪个领域所有？
- 每张业务单据归哪个领域所有？
- 每张平台/共享表归哪个领域所有？
- 每个动作的 `writeback` 目标是哪个领域？

本 Skill 用于**领域边界映射**，不做实现，也不从零做架构设计。

---

## Rule | 规则

**每个对象（表、服务、API）只有一个归属领域。跨域访问必须显式且可追溯。**

---

## Domain Boundary Template | 领域边界模板

模板按四个分组组织，分组名以中文+英文并列写法给出：`Identity & Tenant`（身份与租户）、`Master Data`（主数据）、`Business Documents`（业务单据）、`Platform Tables`（平台表）。

```markdown
## Domain: [Domain Name]

### Identity & Tenant | 身份与租户
| Object | Owner | Access Pattern |
|---|---|---|
| User | [Domain] | Shared — read by all, write by [Domain] |
| Tenant | [Domain] | Shared — read by all, write by [Domain] |
| Organization | [Domain] | Owned by [Domain] |
| Role | [Domain] | Shared — read by all, write by [Domain] |

### Master Data | 主数据
| Object | Owner | Consumers |
|---|---|---|
| Product | [Domain] | Sales, Purchase, Inventory (read-only) |
| Customer | [Domain] | Sales, Finance, Reports (read-only) |
| Supplier | [Domain] | Purchase, Finance, Reports (read-only) |
| Warehouse | [Domain] | Sales, Purchase, Inventory (read-only) |

### Business Documents | 业务单据
| Object | Owner | Writeback Targets |
|---|---|---|
| Sales Order | [Domain] | Inventory (reservation), Finance (none) |
| Sales Delivery | [Domain] | Inventory (decrease), Finance (COGS) |
| Purchase Order | [Domain] | Inventory (none), Finance (none) |
| Purchase Receipt | [Domain] | Inventory (increase), Finance (AP) |

### Platform Tables | 平台表
| Object | Owner | Notes |
|---|---|---|
| System Parameters | [Domain] | Platform infra |
| Audit Log | [Domain] | Cross-cutting |
| File Storage | [Domain] | Shared service |
| Notifications | [Domain] | Shared service |
```

---

## Mapping Workflow | 映射工作流

### Step 1: Inventory Objects | 第 1 步：盘点对象

列出范围内的所有表、服务与 API。

### Step 2: Assign Ownership | 第 2 步：分配归属

对每个对象，依据以下问题确定唯一的归属领域：
- 哪个领域创建/更新权威记录？
- 哪个领域定义校验规则？
- 哪个领域触发状态流转？

### Step 3: Map Writeback Paths | 第 3 步：映射回写路径

对每个业务动作，追踪：
- 源对象 → `writeback` 动作 → 目标对象
- 验证：目标领域是否存在该 `writeback` 的消费方？

### Step 4: Identify Violations | 第 4 步：识别违规

标记以下任一项：
- 多个领域直接写同一张表
- 入口层（前端）承载业务规则
- 缺少 `writeback` 消费方
- 循环 `writeback` 依赖

---

## Common Domain Patterns | 常见领域模式

| 模式 | 描述 | 示例 |
|---|---|---|
| **Shared-Read, Single-Write** | 多个领域读取，一个领域写入 | User 表：所有领域读，Identity 领域写 |
| **Event-Driven Writeback** | 源领域发事件，目标领域异步消费 | 订单创建 → 库存领域接收事件 |
| **Anti-Corruption Layer** | 领域模型之间的翻译层 | 外部 API → 内部领域模型适配器 |
| **Shared Kernel** | 紧密相关领域之间的有限共享模型 | Order 与 Shipment 之间共享的值对象 |

---

## Guardrails | 防护规则

- **禁止**仅凭命名把对象分配给某个领域——必须核对真实代码归属
- **禁止**在没有显式治理的情况下允许多个领域写同一张表
- **禁止**跳过回写路径（`writeback` path）验证
- **禁止**建立与真实代码不符的领域边界
- **禁止**把共享表当成「无归属」——每张表都有归属

## Maturity | 成熟度

**Stage**：Effective —— 提炼自多领域企业级 ERP 的边界映射实践。

## Evolution History | 进化记录

- v1.0.0：从 gerp-domain-boundary-mapper 提炼
- v1.1.0：泛化并补充通用领域模式

---

## 译注 | Translator's Notes

1. 源文件 `## Domain Boundary Template` 的示例块为便于中西对照，仅把四个分组标题写成 `Identity & Tenant | 身份与租户`、`Master Data | 主数据`、`Business Documents | 业务单据`、`Platform Tables | 平台表`；块内其余内容（列名、对象名、取值）逐字照抄源文件，未作翻译。
2. 源文件未提供独立的 `## Trigger` 小节；触发条件见上方 `description` 的中文描述。
3. 源文件未标注版本号，故「源版本」写「未标注」。
