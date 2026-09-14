# `ai-atomic-architect` — AI 原生原子服务架构

> **源文件**：skills/core/ai-atomic-architect/SKILL.md
> **源版本**：未标注（源文件 frontmatter 无版本字段；进化记录最新条目为 v1.2.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-atomic-architect
description: "Design AI-native atomic services, atomic orchestration, aggregate interfaces, command gateways, and multi-platform capability exposure. Use when defining service decomposition, backend truth ownership, reusable business commands, Host clients, or MCP/agent capability surfaces."
```

**中文描述**：设计 AI 原生的 atomic service、atomic orchestration、aggregate interface、command gateway 与多平台能力暴露。当你要定义服务拆分、后端真相归属、可复用业务命令、Host 客户端，或 MCP/智能体能力面时使用。

---

## Rule | 规则

DECLARATION = 仅契约（schema、meta、relations）。EXECUTOR = 全部业务逻辑（可测试、可替换）。GOVERNANCE = 每个 EXECUTOR 上的必填参数。**禁止**在 DeclarationAtom 上编写 `run()`。**必须**为每个 atom 拆分独立的 executor 文件。

---

## Purpose | 目的

定义并强制 AI 原生架构模式：**atomic service + atomic orchestration + 统一接口**。本 Skill 确保用这套方法论构建的每个项目，都能从单一 Web 前端演进为多平台系统（Web、移动 App、微信小程序、MCP 服务器、API），而无需重写业务逻辑。

**它解决的问题**：传统开发把业务逻辑与表现层紧紧耦合在一起。当你需要在新平台（移动端、微信、MCP）提供同一功能时，只能重写。AI 原生架构从第一天起就分离关注点，从而避免这件事。

---

## The Three Pillars | 三大支柱

```
┌─────────────────────────────────────────────────────────┐
│                  UNIFIED INTERFACES                      │
│   REST · GraphQL · MCP · WebSocket · gRPC · WeChat API  │
├─────────────────────────────────────────────────────────┤
│               ATOMIC ORCHESTRATION                       │
│        Workflow Engine · Event Bus · Saga Pattern        │
├─────────────────────────────────────────────────────────┤
│                 ATOMIC SERVICES                          │
│    Auth · User · Task · Note · File · Notify · Audit     │
└─────────────────────────────────────────────────────────┘
```

图示自下而上对应三层：

| 支柱 | 职责 | 组成 |
|---|---|---|
| atomic service（原子服务） | 最小可独立理解、可测试、可治理、可替换的业务逻辑单元 | Auth · User · Task · Note · File · Notify · Audit |
| atomic orchestration（原子编排） | 把 atomic service 组合成业务工作流，而不把它们彼此耦合 | 工作流引擎（Workflow Engine）· 事件总线（Event Bus）· Saga 模式（Saga Pattern） |
| 统一接口（UNIFIED INTERFACES） | 同一套业务逻辑经多种传输协议暴露，且不复制逻辑 | REST · GraphQL · MCP · WebSocket · gRPC · 微信 API（WeChat API） |

---

## Pillar 1: Atomic Services | 原子服务

### Definition | 定义

atomic service 是**最小可独立理解、可测试、可治理、可替换的业务逻辑单元**。它：

- 只做一件事（单一职责）
- 有明确的真相归属方（truth owner）与数据边界
- 只通过已定义的接口通信（**禁止**直连数据库）
- 尽可能无状态，只在必要时有状态

**重要边界**：原子性是能力边界，不是强制的部署边界。一个 atomic service **可以**跑在模块化单体、服务集群或边缘运行时（edge runtime）里。部署与数据库隔离按实际的性能、组织、隔离与运维成本需要来选择；不被 "atomic" 这个词强制。

### Atomic Service Template | 原子服务模板

```
atomic-service/
  ├── api/           # Interface definition (OpenAPI, GraphQL schema, MCP tools)
  ├── core/          # Business logic (pure, no framework dependency)
  ├── data/          # Data access (repository pattern)
  ├── transport/     # Transport adapters (REST, GraphQL, MCP, WebSocket)
  └── test/          # Unit + integration tests
```

各目录职责：`api/` 接口定义（OpenAPI、GraphQL schema、MCP tools）；`core/` 业务逻辑（纯逻辑，不依赖框架）；`data/` 数据访问（仓储模式）；`transport/` 传输适配器（REST、GraphQL、MCP、WebSocket）；`test/` 单元测试与集成测试。

### Anti-Patterns to Avoid | 要避免的反模式

| ❌ 反模式 | ✅ AI 原生模式 |
|---|---|
| 一个拥有 50 个方法的巨型 "UserService" | `auth-service` + `profile-service` + `permission-service` |
| 业务逻辑写在 Vue 组件里 | 业务逻辑放在 `core/`，Vue 组件只调用 API |
| 前端直接查询数据库 | 所有数据库访问都经 atomic service API |
| 混杂多种关注点的 "Utils" 目录 | 每个工具都属于某个明确的 atomic service |
| 一个 API 端点做 5 件事 | 每个原子操作一个端点 |

---

## Pillar 2: Atomic Orchestration | 原子编排

### Definition | 定义

编排把 atomic service 组合成业务工作流，而不把它们彼此耦合在一起。

### Orchestration Patterns | 编排模式

| 模式 | 何时使用 | 示例 |
|---|---|---|
| **Direct Call（直接调用）** | 简单的 1:1 服务依赖 | `task-service` → `notify-service` |
| **Event-Driven（事件驱动）** | 松耦合、发后即忘 | `task-completed` → `audit-log` + `stats-update` |
| **Saga (Choreography)（Saga 编排）** | 带补偿的分布式事务 | `create-order` → `reserve-inventory` → `charge-payment`（含回滚） |
| **Workflow Engine（工作流引擎）** | 复杂的多步业务流程 | 审批链：submit → review → approve → notify |
| **API Gateway（API 网关）** | 面向客户端的聚合 | 移动 App 调一个端点，网关扇出到 N 个服务 |

### Orchestration Rule | 编排规则

**业务工作流是组合，不是单体。**

```
❌ Monolith:        OrderService.processOrder() → does everything in one class
✅ AI-Native:       order-created event → inventory-service.reserve()
                    → payment-service.charge()
                    → notify-service.send()
```

读法：反模式是把所有逻辑塞进 `OrderService.processOrder()` 一个类里；AI 原生模式是 `order-created` 事件驱动 `inventory-service.reserve()` → `payment-service.charge()` → `notify-service.send()` 依次协作。

---

## Pillar 3: Unified Interfaces | 统一接口

### Definition | 定义

同一个 atomic service 通过多种传输协议暴露其业务逻辑，**且不复制逻辑**。

### Transport Adapter Pattern | 传输适配器模式

```
                    ┌──────────────┐
                    │  ATOMIC      │
Web Browser ──────→│  SERVICE     │
React Native ─────→│              │
WeChat MP ────────→│  core/       │──────→ Database
MCP Client ───────→│  business    │
REST Client ──────→│  logic       │
GraphQL Client ───→│              │
                    └──────────────┘
```

图示读法：Web 浏览器、React Native、微信小程序（WeChat MP）、MCP 客户端、REST 客户端、GraphQL 客户端都接入同一个 `core/` 业务逻辑；数据库只在这一侧被访问。

### Interface Mapping by Platform | 按平台划分的接口映射

| 平台 | 主要接口 | 说明 |
|---|---|---|
| Web SPA (Vue/React) | REST + WebSocket | 标准 JSON API，实时能力走 WS |
| 移动 App (Flutter/RN) | REST + WebSocket | 与 Web 同一套 API，仅 UI 不同 |
| 微信小程序（WeChat Mini-Program） | REST (wx.request) | 同一套 API，配微信认证适配器 |
| MCP Server | MCP Tools Protocol | 把同一套逻辑暴露为 MCP tools，供 AI 智能体使用 |
| 第三方集成 | REST + Webhook | 公开 API，带限流 |
| 管理/内部工具 | GraphQL | 为管理看板提供灵活查询 |

### Real-World Platform Matrix (Extracted from GERP) | 真实平台矩阵（提炼自 GERP）

GERP 用一套后端支撑 7 个平台。这就是模板：

| 平台 | 代码 | 类型 | 共享组件 |
|---|---|---|---|
| Web Admin | `gerp-web` | Vue SPA（微前端） | `gerp-common`（组件、语言包、工具） |
| Mobile | `gerp-mobile` | Flutter | 共享 API 层 |
| WeChat Mini-Program | `gerp-mall-miniprogram` | 微信小程序 | 共享 API 层 |
| Agent Web | `gerp-agent-web` | Vue SPA | `gerp-common` |
| Admin Web | `gerp-admin-web` | Vue SPA | `gerp-common` |
| Desktop | `gerp-desktop` | Electron | 共享 API 层 |
| Root Config | `root-config` | 微前端编排器 | N/A（编排其余平台） |

**关键模式**：所有平台共享同一套 REST API。差异只存在于表现层。

---

## Delivery Spine: Aggregate Interface and Command Gateway | 交付主干：聚合接口与命令网关

atomic service 与编排不会直接丢给客户端去拼装。可复用的业务能力必须走这条主干：

```text
domain facts
  -> atomic service
  -> atomic orchestration/application service
  -> aggregate interface
  -> command gateway
  -> transport adapters
  -> Web/App/AI/MCP/OpenAPI Host
```

中文读法：领域事实（domain facts）→ atomic service → atomic orchestration/应用服务 → aggregate interface → command gateway → 传输适配器 → Web/App/AI/MCP/OpenAPI 的 Host。

### Aggregate Interface | 聚合接口

aggregate interface 是面向客户端、开箱可用的契约，对应一个业务对象或一条工作流。它可以包含：

- 运行时/profile 事实；
- 字段元数据与展示/编辑约束；
- 权限、租户/版本/数据范围结果；
- 当前状态、可用命令、阻断项与相关事实；
- Host 需要的、面向展示的读模型。

它**不**把持久化、计算、生命周期流转或授权搬到客户端。

### Command Gateway | 命令网关

command gateway 是可复用业务写入的**唯一**可执行入口。派发之前它必须评估：

1. 已认证的操作者与租户；
2. 权限、版本策略与数据范围；
3. 当前业务状态与上下游阻断项；
4. 幂等性以及确认/风险要求；
5. provider/handler 覆盖情况；
6. 审计轨迹与规范响应。

一个动作**不会**只因为某个适配器或 Host 把它渲染出来就可执行。未支持、延迟或阻断的动作必须保持明确的不可执行状态，并给出稳定原因。

### Capability Execution Maturity | 能力执行成熟度

对 Atom、Skill、工具、AI 任务、插件与业务能力，统一使用同一条成熟度链：

```text
registered
  -> configured
  -> authorized
  -> provider-covered
  -> runtime-executable
  -> business-closed
```

每一次跃迁都需要自己的证据与稳定的失败原因：

| 状态 | 含义 | 证据 |
|---|---|---|
| `registered` | 身份、版本、归属方与声明的契约已存在 | 注册表或清单 |
| `configured` | 必需参数、依赖与运行时 profile 均可解析 | 配置或 profile 回读 |
| `authorized` | 操作者、租户、角色、版本授权与数据范围允许使用 | 权限判定 |
| `provider-covered` | 有真实 provider、handler 或 command 覆盖所声明的操作 | provider 或 command 覆盖审计 |
| `runtime-executable` | 受支持的入口点以预期状态与副作用执行 | 运行时/API 执行与权威回读 |
| `business-closed` | 原始业务流程、对账、审计与验收均已完成 | 端到端收口与产品或客户验收 |

规则：

1. 低阶状态**禁止**上报为高阶状态。
2. 注册表或目录中的存在只证明 `registered`；一个可见按钮不能证明后续任何状态。
3. 延迟、阻断或不支持的动作保持明确的不可执行状态，并暴露稳定原因。
4. 同一条链适用于 Web、App、AI、MCP、OpenAPI 与后台任务适配器；适配器**不会**提升能力成熟度。

### Host and Adapter Boundary | Host 与适配器边界

Web、App、AI、MCP、OpenAPI、桌面端与各类连接器，都是同一套聚合契约与命令契约之上的适配器：

- 适配器负责转换协议、身份、输入与输出；
- Host 负责加载/渲染被许可的事实、采集输入、调用 gateway 并展示反馈；
- 适配器与 Host 都**不得**自行编排领域服务、执行裸查询、计算业务事实，或另造一个状态机。

---

### Domain Module Decomposition (Extracted from GERP) | 领域模块拆分（提炼自 GERP）

一套完整 ERP 拆成以下领域模块。可作为领域驱动设计的参照：

| 类别 | 模块 |
|---|---|
| **Foundation（基座）** | base, masterdata, auth |
| **Core Business（核心业务）** | sale, purchase, inv (inventory), production, wms (warehouse) |
| **Finance（财务）** | finance, payment, capital |
| **Extended Business（扩展业务）** | crm, mall, b2b, scm (supply chain), tms (transport), trade |
| **Operations（运营）** | report, print, oa, mes, qms |
| **Platform（平台）** | saas, agent, ai |

**拆分规则**：每个模块 = 一个 atomic service。任何模块依赖的其他模块**不得超过** 3 个。

---

### Interface Definition First | 接口先行

```yaml
# api/task-service.openapi.yaml — Define interface BEFORE implementation
openapi: 3.0.0
paths:
  /tasks:
    get:
      operationId: listTasks
      summary: List tasks (used by web, mobile, WeChat, MCP)
    post:
      operationId: createTask
      summary: Create task (used by all platforms)
  /tasks/{id}/status:
    patch:
      operationId: updateTaskStatus
      summary: Update status (drag & drop, mobile swipe, MCP tool)
```

---

## Project Archetypes | 项目原型

### Archetype A: Single-Service (Rapid Prototype) | 原型 A：单服务（快速原型）

**何时（When）**：MVP、概念验证（proof-of-concept）、单人开发、页面数 < 10
**架构（Architecture）**：一个服务，内部边界清晰，单一仓库（monorepo）
**演进路径（Evolution path）**：任一模块的核心逻辑超过 500 行时，拆分为 atomic service

### Archetype B: Atomic Services (Production SaaS) | 原型 B：原子服务（生产级 SaaS）

**何时（When）**：多租户、3 人以上团队、预期要扩容
**架构（Architecture）**：5–15 个 atomic service，事件驱动编排
**平台（Platforms）**：Web + Mobile + API

### Archetype C: Multi-Platform (Enterprise) | 原型 C：多平台（企业级）

**何时（When）**：Web + App + 微信 + MCP + 第三方 API
**架构（Architecture）**：atomic service + API Gateway + Transport Adapters
**平台（Platforms）**：以上全部

---

## Integration with Existing Methodology | 与现有方法论的集成

| 步骤 | ai-atomic-architect 如何介入 |
|---|---|
| 项目启动 | `ai-project-classifier` 选定原型 A/B/C |
| Step 1 (DB) | 每个 atomic service 拥有自己的 schema/模块 |
| Step 2 (Entity) | 实体 = 一个原子概念，而不是 "上帝实体" |
| Step 4 (Service) | Service = 原子、单一职责 |
| Step 5 (API) | 先定义接口，再做传输适配器 |
| Step 7 (Frontend) | 前端只调用 atomic service API，**禁止**直连数据库 |
| Step 13 (Verify) | 验证每个 atomic service 都能独立测试 |

---

## Guardrails | 防护规则

- **禁止把业务逻辑放进表现层**（Vue 组件、Flutter widget）
- **先定义接口再实现**（先写 OpenAPI/GraphQL schema）
- **一个 atomic service = 一个明确的数据边界** —— 只有在独立部署与隔离足以证明其运维成本合理时，schema-per-service 才是合适的
- **传输只是细节** —— 核心业务逻辑不知道自己是经 REST、MCP 还是 WebSocket 被调用
- **先聚合再交给 Host** —— 客户端消费一份 aggregate interface 契约，而不是自己编排后端服务
- **写入必须经 command gateway** —— 适配器与 Host **不得**绕过授权、状态、幂等或审计检查
- **先简单起步，需要时再拆** —— 原型 A 是合法的；**不要**过度设计
- **每个 atomic service 必须能在其他服务都不运行时独立测试**

## Maturity | 成熟度

**Stage**：New —— 提炼自企业级多平台架构需求。

## Evolution History | 进化记录

- v1.0.0：初版 —— 3 大支柱、3 种原型、统一接口映射
- v1.1.0：加入来自企业级多客户端交付证据的 aggregate interface、command gateway、adapter 与 Host 边界
- v1.2.0：为 Atom、Skill、工具、任务、插件与业务适配器等能力，加入共享的 registered → business-closed 成熟度链

---

## 译注

1. **源版本**：源文件 frontmatter 只有 `name`/`description` 两个键，未标注版本；本译文按「进化记录」最新条目注记 v1.2.0。
2. **引用路径存在性核对**（源文件引用的路径/脚本）：
   - `api/task-service.openapi.yaml`、`atomic-service/`：源文件中的模板/示例路径，仓库内不存在，属可套用的示意结构，非缺失文件。
   - `gerp-web`、`gerp-mobile`、`gerp-mall-miniprogram`、`gerp-agent-web`、`gerp-admin-web`、`gerp-desktop`、`root-config`：源文件引用的历史企业项目代号，不是本仓库路径。
   - `ai-project-classifier`：以 Skill 名引用，正式源位于 `skills/core/ai-project-classifier/SKILL.md`（存在）。
   - 全文未引用任何脚本或命令，故无脚本存在性风险。
3. **代码块处理**：源文件 7 个代码块（Three Pillars 图示、`atomic-service/` 目录结构、单体 vs AI 原生对照、传输适配器图示、交付主干、能力成熟度链、OpenAPI YAML）按口径原样复制，图示内的英文标签未改写；为便于阅读，在每个图示后补了中文对照说明。
4. **术语保留自检**：本译文保留了 `atomic service`、`atomic orchestration`、`aggregate interface`、`command gateway`、`Host`、`DeclarationAtom`、`ExecutorAtom`、`Provider`/`handler` 等英文标识符；`fail-closed`、`FieldPackage`、`BusinessProfile`、`L0`–`L5`、`Q0`–`Q3`、`P0`–`P3` 未在本源文件出现，本译文不引入源文件没有的概念，仅在术语表中保持其英文写法。
5. **语义强度**：源文件的 `Never`/`Always`/`MUST`（含 `must not`）分别译为「禁止」/「必须」，`MAY` 译为「可以」，未弱化任何禁令。
