# `ai-architect-governor` — 跨域架构治理（Cross-Domain Architecture Governor）

> **源文件**：skills/core/ai-architect-governor/SKILL.md
> **源版本**：未标注（源文件 frontmatter 无版本字段；进化记录最新条目为 v1.1.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-architect-governor
description: "Govern cross-domain architecture decisions, ADRs, domain boundaries, source-of-truth ownership, identity/tenant models, integration patterns, and architecture risk. Use when a task changes architecture, crosses modules or platforms, defines ownership, or needs an architecture decision record."
```

**中文描述**：治理跨域架构决策、ADR、领域边界、真相源归属、身份/租户模型、集成模式与架构风险。当任务会改变架构、跨越模块或平台、定义归属，或需要架构决策记录时使用。

---

## Purpose | 目的

治理跨域架构决策：

- 领域边界的核实与强制
- 身份/租户/权限的归属规则
- 主数据与业务真相的归属映射
- 跨域链路定义
- 系统集成模式
- 架构决策记录（ADR）

本 Skill 服务于**架构治理**，不是单模块实现。

## Rule | 规则

**禁止靠想象设计架构。**

在给出任何架构结论之前：

1. 核实当前文档
2. 核实当前代码现实
3. 分离：当前已验证状态 → 目标结构 → 治理决策 → 实现任务
4. 区分：真相源（source-of-truth）系统、入口层（entry layer）、使能层（enablement layer）、对象归属方（object owner）、回写消费方（writeback consumer）

---

## Architecture Decision Layers | 架构决策分层

### Layer 1: Domain Boundaries | 第 1 层：领域边界

- 每个身份概念（用户、租户、组织）归哪个领域所有？
- 每个主数据对象（产品、客户、供应商）归哪个领域所有？
- 每张业务单据（订单、发票、收据）归哪个领域所有？
- 每张平台表（配置、审计日志）归哪个领域所有？

### Layer 2: Identity & Access | 第 2 层：身份与访问

- 单点登录（SSO）的范围与边界
- 租户隔离模型（共享库 shared DB、一租户一 schema、一租户一库）
- 权限模型（RBAC、ABAC、混合）
- API 认证与授权流程

### Layer 3: Data Ownership | 第 3 层：数据归属

- 每种数据类型的权威来源（authoritative source）是谁？
- 回写路径：哪个系统更新哪个下游真相？
- 跨域数据的缓存/失效策略
- 事件溯源（event sourcing）与最终一致性（eventual consistency）的边界

### Layer 4: Integration Patterns | 第 4 层：集成模式

- 同步 API 调用 vs 异步事件/消息
- shared-nothing vs shared-kernel vs shared-core
- 防腐层（anti-corruption layer）要求
- API 版本化与向后兼容

---

## Architecture Decision Record Template | ADR 模板

```markdown
# ADR-[NNN]: [Title]

## Status
[Proposed / Accepted / Deprecated / Superseded]

## Context
[What is the issue that we're seeing that is motivating this decision?]

## Decision
[What is the change that we're proposing and/or doing?]

## Consequences
[What becomes easier or more difficult to do because of this change?]

## Alternatives Considered
- [Alternative 1]: [Why rejected]
- [Alternative 2]: [Why rejected]
```

模板占位符说明（占位符本身保持原样，可直接套用）：

| 占位符 | 填写内容 |
|---|---|
| `[NNN]` | ADR 序号，与文件名中的编号一致 |
| `[Title]` | 决策标题，一句话说清决策对象 |
| `[Proposed / Accepted / Deprecated / Superseded]` | 状态，四选一：提议中 / 已接受 / 已弃用 / 已被取代 |
| Context 段 | 触发本次决策的问题是什么 |
| Decision 段 | 提议和/或正在做的变更是什么 |
| Consequences 段 | 因为这次变更，哪些事变得更容易、哪些变得更困难 |
| `[Alternative 1]`/`[Alternative 2]` | 被考虑过的备选方案及其被否决的原因 |

---

## Check-Before-Architecture | 架构决策前检查

| 检查项 | 方法 |
|---|---|
| 已有 ADR | 读 `docs/架构决策记录/`，找相关决策 |
| 当前代码 | 在代码里核实真实的领域归属，而不是只看文档 |
| 数据库模式（schema） | 检查表的位置、外键、共享表 |
| API 契约 | 复核现有 API 边界与版本策略 |
| 团队归属 | 弄清哪个团队负责哪个领域 |

---

## Source-of-Truth vs Entry Layer | 真相源 vs 入口层

每一项业务能力都必须区分：

| 角色 | 职责 | 示例 |
|---|---|---|
| **Source of Truth（真相源）** | 数据/规则的权威系统 | 持有规范数据库（canonical database）的后端服务 |
| **Entry Layer（入口层）** | 面向用户或集成的接口 | Web UI、移动 App、API 网关 |
| **Writeback Consumer（回写消费方）** | 接收更新的系统 | 报表系统、分析系统、下游服务 |
| **Enablement Layer（使能层）** | 共享基础设施 | 认证服务、文件存储、通知 |

---

## Guardrails | 防护规则

- **禁止**未在实际代码中核实就划出领域边界
- **禁止**仅凭命名推断归属 —— 必须在数据库与服务层核实
- **禁止**对影响多个领域的决策跳过 ADR 编写
- **禁止**把入口层当作真相源
- **禁止**在受影响领域的归属方不知情时合并跨域改动

## Maturity | 成熟度

**Stage**：Effective —— 提炼自企业级 ERP 架构治理，含跨域边界映射模式。

## Evolution History | 进化记录

- v1.0.0：提炼自 gerp-architect-governor（原始 15KB）
- v1.1.0：通用化为普适的架构治理模式
- 来源：多领域企业级系统（ERP + Mall + App + Agent + SaaS）

---

## 译注

1. **源版本**：源文件 frontmatter 只有 `name`/`description` 两个键，未标注版本；本译文按「进化记录」最新条目注记 v1.1.0。
2. **引用路径存在性核对**（源文件引用的路径/脚本）：
   - `docs/架构决策记录/`：本仓库内存在该目录，引用有效。
   - `gerp-architect-governor`：源文件引用的历史 Skill 名（原始 15KB），当前 `skills/` 下已不存在该目录，属历史来源注记。
   - 全文未引用任何脚本或命令，故无脚本存在性风险。
3. **ADR 模板处理**：模板代码块按口径原样复制，`[NNN]`、`[Title]`、`[Alternative 1]`、`[Alternative 2]` 等占位符保持原样；模板后用一张中文表说明每个位置的填写内容，模板本身可直接套用。
4. **术语保留自检**：本译文保留了 `ADR`、`SSO`、`RBAC`、`ABAC`、`shared-nothing`、`shared-kernel`、`shared-core`、`Entry Layer`、`Source of Truth`、`Writeback Consumer`、`Enablement Layer` 等英文标识符；源文件未出现 `atomic service`、`atomic orchestration`、`aggregate interface`、`command gateway`、`Host`、`DeclarationAtom`、`ExecutorAtom`、`FieldPackage`、`BusinessProfile`、`fail-closed`、`L0`–`L5`、`Q0`–`Q3`、`P0`–`P3`，本译文不引入源文件没有的概念，这些标识符在术语表中仍保持英文写法。
5. **语义强度**：源文件的 `Do not` 一律译为「禁止」，未弱化为建议；「必须区分/必须核实」等强制表述与源文件一致。
