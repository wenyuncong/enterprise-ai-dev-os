---
name: ai-domain-boundary-mapper
description: "Map domain boundaries, object ownership, source-of-truth placement, write paths, read consumers, schema ownership, and cross-domain risks. Use when data, identity, permissions, documents, reports, or business objects cross module boundaries."
---

# ai-domain-boundary-mapper — Domain Boundary & Object Ownership Mapper

## Purpose | 用途

Map domain boundaries at the object level:

- Which domain owns each identity concept?
- Which domain owns each master data object?
- Which domain owns each business document?
- Which domain owns each platform/shared table?
- Which domain is the writeback target for each action?

This skill is for **domain boundary mapping**, not implementation or architecture design from scratch.

---

## Core Rule | 核心规则

**Every object (table, service, API) has one owning domain. Cross-domain access must be explicit and traceable.**

---

## Domain Boundary Template | 领域边界模板

```markdown
## Domain: [Domain Name]

### Identity & Tenant
| Object | Owner | Access Pattern |
|---|---|---|
| User | [Domain] | Shared — read by all, write by [Domain] |
| Tenant | [Domain] | Shared — read by all, write by [Domain] |
| Organization | [Domain] | Owned by [Domain] |
| Role | [Domain] | Shared — read by all, write by [Domain] |

### Master Data
| Object | Owner | Consumers |
|---|---|---|
| Product | [Domain] | Sales, Purchase, Inventory (read-only) |
| Customer | [Domain] | Sales, Finance, Reports (read-only) |
| Supplier | [Domain] | Purchase, Finance, Reports (read-only) |
| Warehouse | [Domain] | Sales, Purchase, Inventory (read-only) |

### Business Documents
| Object | Owner | Writeback Targets |
|---|---|---|
| Sales Order | [Domain] | Inventory (reservation), Finance (none) |
| Sales Delivery | [Domain] | Inventory (decrease), Finance (COGS) |
| Purchase Order | [Domain] | Inventory (none), Finance (none) |
| Purchase Receipt | [Domain] | Inventory (increase), Finance (AP) |

### Platform Tables
| Object | Owner | Notes |
|---|---|---|
| System Parameters | [Domain] | Platform infra |
| Audit Log | [Domain] | Cross-cutting |
| File Storage | [Domain] | Shared service |
| Notifications | [Domain] | Shared service |
```

---

## Mapping Workflow | 映射工作流

### Step 1: Inventory Objects
List all tables, services, and APIs in scope.

### Step 2: Assign Ownership
For each object, determine the single owning domain based on:
- Which domain creates/updates the authoritative record?
- Which domain defines the validation rules?
- Which domain triggers state transitions?

### Step 3: Map Writeback Paths
For each business action, trace:
- Source object → writeback action → target object
- Verify: does the target domain have a consumer for this writeback?

### Step 4: Identify Violations
Flag any:
- Multiple domains writing to the same table directly
- Entry layer (frontend) containing business rules
- Missing writeback consumers
- Circular writeback dependencies

---

## Common Domain Patterns | 常见领域模式

| Pattern | Description | Example |
|---|---|---|
| **Shared-Read, Single-Write** | Multiple domains read, one domain writes | User table: all read, Identity domain writes |
| **Event-Driven Writeback** | Source domain emits event, target consumes asynchronously | Order created → Inventory receives event |
| **Anti-Corruption Layer** | Translation layer between domain models | External API → internal domain model adapter |
| **Shared Kernel** | Limited shared model between closely related domains | Shared value objects between Order and Shipment |

---

## Guardrails | 防护规则

- Do not assign an object to a domain based on naming alone — verify actual code ownership
- Do not allow multiple domains to write to the same table without explicit governance
- Do not skip writeback path verification
- Do not create domain boundaries that don't match actual code reality
- Do not treat shared tables as "no owner" — every table has an owner

## Maturity | 成熟度

**Stage**: Effective — Extracted from multi-domain enterprise ERP boundary mapping.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-domain-boundary-mapper
- v1.1.0: Generalized with universal domain patterns
