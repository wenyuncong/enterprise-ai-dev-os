---
name: ai-domain-boundary-mapper
description: "Map domain boundaries, object ownership, source-of-truth placement, write paths, read consumers, schema ownership, and cross-domain risks. Use when data, identity, permissions, documents, reports, or business objects cross module boundaries."
metadata:
  requires:
    scope: universal
    declared-by: enterprise-ai-dev-os
---

# ai-domain-boundary-mapper — Domain Boundary & Object Ownership Mapper

## Purpose

Map domain boundaries at the object level:

- Which domain owns each identity concept?
- Which domain owns each master/reference object?
- Which domain owns each business document?
- Which domain owns each platform/shared data structure?
- Which domain is the writeback target for each action?

This skill is for **domain boundary mapping**, not implementation or architecture design from scratch.

---

## Rule

**Every object (data structure, service, contract) has one owning domain. Cross-domain access must be explicit and traceable.**

---

## Domain Boundary Template | 领域边界模板

The rows below use neutral placeholders. Replace them with the project's own objects; do not assume a fixed business vocabulary.

```markdown
## Domain: [Domain Name]

### Identity & Tenant
| Object | Owner | Access Pattern |
|---|---|---|
| User identity | [Domain] | Shared — read by all, write by [Domain] |
| Tenant/partition | [Domain] | Shared — read by all, write by [Domain] |
| Organization unit | [Domain] | Owned by [Domain] |
| Role/permission | [Domain] | Shared — read by all, write by [Domain] |

### Master / Reference Data
| Object | Owner | Consumers |
|---|---|---|
| Reference object A | [Domain] | consuming domains (read-only) |
| Reference object B | [Domain] | consuming domains (read-only) |
| Reference object C | [Domain] | consuming domains (read-only) |

### Business Documents
| Object | Owner | Writeback Targets |
|---|---|---|
| Document A | [Domain] | downstream domain action (or none) |
| Document B | [Domain] | downstream domain action (or none) |
| Document C | [Domain] | downstream domain action (or none) |

### Platform Structures
| Object | Owner | Notes |
|---|---|---|
| System parameters | [Domain] | Platform infra |
| Audit log | [Domain] | Cross-cutting |
| File storage | [Domain] | Shared service |
| Notifications | [Domain] | Shared service |
```

---

## Mapping Workflow | 映射工作流

### Step 1: List Objects
List all data structures, services, and contracts in scope.

### Step 2: Assign Ownership
For each object, determine the single owning domain based on:
- Which domain creates/updates the authoritative record?
- Which domain defines the validation rules?
- Which domain triggers state transitions?

### Step 3: Map Writeback Paths
For each business action, trace:
- Source object -> writeback action -> target object
- Verify: does the target domain have a consumer for this writeback?

### Step 4: Identify Violations
Flag any:
- Multiple domains writing to the same structure directly
- Entry layer (frontend) containing business rules
- Missing writeback consumers
- Circular writeback dependencies

---

## Common Domain Patterns | 常见领域模式

| Pattern | Description | Example |
|---|---|---|
| **Shared-Read, Single-Write** | Multiple domains read, one domain writes | identity data: all read, the identity domain writes |
| **Event-Driven Writeback** | Source domain emits event, target consumes asynchronously | a document is created -> the downstream domain receives the event |
| **Anti-Corruption Layer** | Translation layer between domain models | external contract -> internal domain model adapter |
| **Shared Kernel** | Limited shared model between closely related domains | shared value objects between two cooperating domains |

---

## Guardrails | 防护规则

- Do not assign an object to a domain based on naming alone — verify actual code ownership
- Do not allow multiple domains to write to the same structure without explicit governance
- Do not skip writeback path verification
- Do not create domain boundaries that don't match actual code reality
- Do not treat shared structures as "no owner" — every one has an owner

## Maturity | 成熟度

**Stage**: Effective — generalized from real multi-domain enterprise boundary mapping.

## Evolution History | 进化记录

- v1.0.0: Generalized from real enterprise boundary mapping evidence (project-specific names removed)
- v1.1.0: Generalized with universal domain patterns and neutral placeholders
