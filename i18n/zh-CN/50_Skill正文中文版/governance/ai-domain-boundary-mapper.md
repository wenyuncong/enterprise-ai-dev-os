# `ai-domain-boundary-mapper` — 领域边界与对象归属映射

> **源文件**：skills/governance/ai-domain-boundary-mapper/SKILL.md
> **源版本**：1.0.0
> **译文日期**：2026-11-08
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
- 每个主数据/参考对象归哪个领域所有？
- 每张业务单据归哪个领域所有？
- 每个平台/共享数据结构归哪个领域所有？
- 每个动作的 `writeback` 目标是哪个领域？

本 Skill 用于**领域边界映射**，不做实现，也不从零做架构设计。

---

## Rule | 规则

**每个对象（数据结构、服务、契约）只有一个归属领域。跨域访问必须显式且可追溯。**

---

## Domain Boundary Template | 领域边界模板

下面使用中立占位符。把它们替换为项目自己的对象；不要假设一份固定业务词汇。

```markdown
## Domain: [Domain Name]

### Identity & Tenant | 身份与租户
| Object | Owner | Access Pattern |
|---|---|---|
| User identity | [Domain] | Shared — read by all, write by [Domain] |
| Tenant/partition | [Domain] | Shared — read by all, write by [Domain] |
| Organization unit | [Domain] | Owned by [Domain] |
| Role/permission | [Domain] | Shared — read by all, write by [Domain] |

### Master / Reference Data | 主数据/参考数据
| Object | Owner | Consumers |
|---|---|---|
| Reference object A | [Domain] | consuming domains (read-only) |
| Reference object B | [Domain] | consuming domains (read-only) |
| Reference object C | [Domain] | consuming domains (read-only) |

### Business Documents | 业务单据
| Object | Owner | Writeback Targets |
|---|---|---|
| Document A | [Domain] | downstream domain action (or none) |
| Document B | [Domain] | downstream domain action (or none) |
| Document C | [Domain] | downstream domain action (or none) |

### Platform Structures | 平台结构
| Object | Owner | Notes |
|---|---|---|
| System parameters | [Domain] | Platform infra |
| Audit log | [Domain] | Cross-cutting |
| File storage | [Domain] | Shared service |
| Notifications | [Domain] | Shared service |
```

---

## Mapping Workflow | 映射工作流

### Step 1: List Objects | 第 1 步：盘点对象

列出范围内的所有数据结构、服务与契约。

### Step 2: Assign Ownership | 第 2 步：分配归属

对每个对象，依据以下问题确定唯一的归属领域：
- 哪个领域创建/更新权威记录？
- 哪个领域定义校验规则？
- 哪个领域触发状态流转？

### Step 3: Map Writeback Paths | 第 3 步：映射回写路径

对每个业务动作，追踪：
- 源对象 -> `writeback` 动作 -> 目标对象
- 验证：目标领域是否存在该 `writeback` 的消费方？

### Step 4: Identify Violations | 第 4 步：识别违规

标记以下任一项：
- 多个领域直接写同一结构
- 入口层（前端）承载业务规则
- 缺少 `writeback` 消费方
- 循环 `writeback` 依赖

---

## Common Domain Patterns | 常见领域模式

| 模式 | 描述 | 示例 |
|---|---|---|
| **Shared-Read, Single-Write** | 多个领域读取，一个领域写入 | 身份数据：所有领域读，身份领域写 |
| **Event-Driven Writeback** | 源领域发事件，目标领域异步消费 | 单据创建 -> 下游领域接收事件 |
| **Anti-Corruption Layer** | 领域模型之间的翻译层 | 外部契约 -> 内部领域模型适配器 |
| **Shared Kernel** | 紧密相关领域之间的有限共享模型 | 两个协作领域之间共享的值对象 |

---

## Guardrails | 防护规则

- **禁止**仅凭命名把对象分配给某个领域——必须核对真实代码归属
- **禁止**在没有显式治理的情况下允许多个领域写同一结构
- **禁止**跳过回写路径（`writeback` path）验证
- **禁止**建立与真实代码不符的领域边界
- **禁止**把共享结构当成「无归属」——每个都有归属

## Maturity | 成熟度

**Stage**：Effective —— 提炼自真实多领域企业边界映射实践。

## Evolution History | 进化记录

- v1.0.0：从真实企业边界映射证据提炼并通用化
- v1.1.0：泛化并补充通用领域模式与中立占位
