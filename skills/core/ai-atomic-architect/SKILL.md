---
name: ai-atomic-architect
description: "Design AI-native atomic services, capability units, orchestration boundaries, shared backend command paths, and multi-platform capability exposure. Use when defining service decomposition, MCP/agent capability surfaces, backend truth ownership, or reusable business command architecture."
---

# ai-atomic-architect — AI-Native Atomic Service Architecture

## Purpose | 用途

Define and enforce AI-native architecture patterns: **atomic services + atomic orchestration + unified interfaces**. This skill ensures that every project built with this methodology can evolve from a single web frontend into a multi-platform system (web, mobile app, WeChat mini-program, MCP server, API) without rewriting business logic.

**Problem it solves**: Traditional development creates tight coupling between business logic and presentation layer. When you need the same feature on a new platform (mobile, WeChat, MCP), you rewrite it. AI-native architecture prevents this by separating concerns from day one.

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

---

## Pillar 1: Atomic Services | 原子服务

### Definition
An atomic service is the **smallest independently deployable unit of business logic**. It:
- Does exactly ONE thing (single responsibility)
- Owns its own data (database-per-service or schema-per-service)
- Communicates only through defined interfaces (never direct DB access)
- Is stateless where possible, stateful only where necessary

### Atomic Service Template
```
atomic-service/
  ├── api/           # Interface definition (OpenAPI, GraphQL schema, MCP tools)
  ├── core/          # Business logic (pure, no framework dependency)
  ├── data/          # Data access (repository pattern)
  ├── transport/     # Transport adapters (REST, GraphQL, MCP, WebSocket)
  └── test/          # Unit + integration tests
```

### Anti-Patterns to Avoid
| ❌ Anti-Pattern | ✅ AI-Native Pattern |
|---|---|
| One giant "UserService" with 50 methods | `auth-service` + `profile-service` + `permission-service` |
| Business logic in Vue components | Business logic in `core/`, Vue components call API only |
| Direct DB queries from frontend | All DB access through atomic service API |
| "Utils" folder with mixed concerns | Each utility belongs to a specific atomic service |
| One API endpoint that does 5 things | One endpoint per atomic operation |

---

## Pillar 2: Atomic Orchestration | 原子编排

### Definition
Orchestration composes atomic services into business workflows without coupling them together.

### Orchestration Patterns

| Pattern | When to Use | Example |
|---|---|---|
| **Direct Call** | Simple 1:1 service dependency | `task-service` → `notify-service` |
| **Event-Driven** | Loose coupling, fire-and-forget | `task-completed` → `audit-log` + `stats-update` |
| **Saga (Choreography)** | Distributed transaction with compensation | `create-order` → `reserve-inventory` → `charge-payment` (with rollback) |
| **Workflow Engine** | Complex multi-step business process | Approval chain: submit → review → approve → notify |
| **API Gateway** | Client-facing aggregation | Mobile app calls one endpoint, gateway fans out to N services |

### Orchestration Rule
**Business workflows are compositions, not monoliths.**
```
❌ Monolith:        OrderService.processOrder() → does everything in one class
✅ AI-Native:       order-created event → inventory-service.reserve()
                    → payment-service.charge()
                    → notify-service.send()
```

---

## Pillar 3: Unified Interfaces | 统一接口

### Definition
The same atomic service exposes its business logic through multiple transport protocols **without duplicating logic**.

### Transport Adapter Pattern
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

### Interface Mapping by Platform

| Platform | Primary Interface | Notes |
|---|---|---|
| Web SPA (Vue/React) | REST + WebSocket | Standard JSON API, real-time via WS |
| Mobile App (Flutter/RN) | REST + WebSocket | Same API as web, different UI |
| WeChat Mini-Program | REST (wx.request) | Same API, WeChat auth adapter |
| MCP Server | MCP Tools Protocol | Expose same logic as MCP tools for AI agents |
| Third-party Integration | REST + Webhook | Public API with rate limiting |
| Admin/Internal Tools | GraphQL | Flexible querying for admin dashboards |


### Real-World Platform Matrix (Extracted from GERP)

GERP supports 7 platforms from a single backend. This is the template:

| Platform | Code | Type | Shared Components |
|---|---|---|---|
| Web Admin | `gerp-web` | Vue SPA (micro-frontend) | `gerp-common` (components, locales, utils) |
| Mobile | `gerp-mobile` | Flutter | Shared API layer |
| WeChat Mini-Program | `gerp-mall-miniprogram` | 微信小程序 | Shared API layer |
| Agent Web | `gerp-agent-web` | Vue SPA | `gerp-common` |
| Admin Web | `gerp-admin-web` | Vue SPA | `gerp-common` |
| Desktop | `gerp-desktop` | Electron | Shared API layer |
| Root Config | `root-config` | Micro-frontend orchestrator | N/A (orchestrates others) |

**Key pattern**: All platforms share the same REST API. The difference is only in the presentation layer.

---

### Domain Module Decomposition (Extracted from GERP)

A full ERP breaks down into these domain modules. Use as a reference for domain-driven design:

| Category | Modules |
|---|---|
| **Foundation** | base, masterdata, auth |
| **Core Business** | sale, purchase, inv (inventory), production, wms (warehouse) |
| **Finance** | finance, payment, capital |
| **Extended Business** | crm, mall, b2b, scm (supply chain), tms (transport), trade |
| **Operations** | report, print, oa, mes, qms |
| **Platform** | saas, agent, ai |

**Decomposition Rule**: Each module = one atomic service. No module should depend on more than 3 other modules.

---

### Interface Definition First
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

### Archetype A: Single-Service (Rapid Prototype)
**When**: MVP, proof-of-concept, solo developer, < 10 screens
**Architecture**: One service with clear internal boundaries, monorepo
**Evolution path**: Split into atomic services when any module exceeds 500 lines of core logic

### Archetype B: Atomic Services (Production SaaS)
**When**: Multi-tenant, team of 3+, expected to scale
**Architecture**: 5-15 atomic services, event-driven orchestration
**Platforms**: Web + Mobile + API

### Archetype C: Multi-Platform (Enterprise)
**When**: Web + App + WeChat + MCP + Third-party API
**Architecture**: Atomic services + API Gateway + Transport Adapters
**Platforms**: All of the above

---

## Integration with Existing Methodology | 方法论集成

| Step | How ai-atomic-architect applies |
|---|---|
| Project Start | `ai-project-classifier` selects archetype A/B/C |
| Step 1 (DB) | Each atomic service gets its own schema/module |
| Step 2 (Entity) | Entity = one atomic concept, not "God entity" |
| Step 4 (Service) | Service = atomic, single-responsibility |
| Step 5 (API) | Define interface first, transport adapters second |
| Step 7 (Frontend) | Frontend calls atomic service APIs, never DB directly |
| Step 13 (Verify) | Verify that each atomic service can be tested independently |

---

## Guardrails | 防护规则

- **Never put business logic in the presentation layer** (Vue components, Flutter widgets)
- **Define the interface before implementing** (OpenAPI/GraphQL schema first)
- **One atomic service = one database schema** (no cross-service DB joins)
- **Transport is a detail** — the core business logic doesn't know if it's called via REST, MCP, or WebSocket
- **Start simple, split when needed** — Archetype A is valid; don't over-engineer
- **Every atomic service must be independently testable** without other services running

## Maturity | 成熟度

**Stage**: New — Extracted from enterprise multi-platform architecture requirements.

## Evolution History | 进化记录

- v1.0.0: Initial creation — 3 pillars, 3 archetypes, unified interface mapping
