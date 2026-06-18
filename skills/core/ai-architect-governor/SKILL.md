---
name: ai-architect-governor
description: "Govern cross-domain architecture decisions, ADRs, domain boundaries, source-of-truth ownership, identity/tenant models, integration patterns, and architecture risk. Use when a task changes architecture, crosses modules or platforms, defines ownership, or needs an architecture decision record."
---

# ai-architect-governor — Cross-Domain Architecture Governor

## Purpose | 用途

Govern cross-domain architecture decisions:

- Domain boundary verification and enforcement
- Identity/tenant/permission ownership rules
- Master-data and business-truth ownership mapping
- Cross-domain chain definitions
- System integration patterns
- Architecture decision records (ADR)

This skill is for **architecture governance**, not single-module implementation.

## Core Rule | 核心规则

**Do not design architecture from imagination.**

Before making any architecture conclusion:
1. Verify current documentation
2. Verify current code reality
3. Separate: current verified state → target structure → governance decisions → implementation tasks
4. Distinguish: source-of-truth system, entry layer, enablement layer, object owner, writeback consumer

---

## Architecture Decision Layers | 架构决策分层

### Layer 1: Domain Boundaries
- Which domain owns each identity concept (user, tenant, organization)?
- Which domain owns each master data object (product, customer, supplier)?
- Which domain owns each business document (order, invoice, receipt)?
- Which domain owns each platform table (configuration, audit log)?

### Layer 2: Identity & Access
- Single sign-on (SSO) scope and boundaries
- Tenant isolation model (shared DB, schema-per-tenant, DB-per-tenant)
- Permission model (RBAC, ABAC, hybrid)
- API authentication and authorization flow

### Layer 3: Data Ownership
- Who is the authoritative source for each data type?
- Writeback paths: which system updates which downstream truth?
- Cache/invalidation strategy for cross-domain data
- Event sourcing and eventual consistency boundaries

### Layer 4: Integration Patterns
- Synchronous API calls vs async events/messages
- Shared-nothing vs shared-kernel vs shared-core
- Anti-corruption layer requirements
- API versioning and backward compatibility

---

## Architecture Decision Record Template | ADR模板

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

---

## Check-Before-Architecture | 架构决策前检查

| Check | Method |
|---|---|
| Existing ADRs | Read `docs/架构决策记录/` for relevant decisions |
| Current code | Verify actual domain ownership in code, not just docs |
| Database schema | Check table placement, foreign keys, shared tables |
| API contracts | Review existing API boundaries and versioning |
| Team ownership | Understand which team owns which domain |

---

## Source-of-Truth vs Entry Layer | 真相源 vs 入口层

Every business capability must distinguish:

| Role | Responsibility | Example |
|---|---|---|
| **Source of Truth** | Authoritative system for data/rules | Backend service with the canonical database |
| **Entry Layer** | User-facing or integration interface | Web UI, mobile app, API gateway |
| **Writeback Consumer** | System that receives updates | Reporting system, analytics, downstream services |
| **Enablement Layer** | Shared infrastructure | Authentication service, file storage, notification |

---

## Guardrails | 防护规则

- Do not create a domain boundary without verifying it in actual code
- Do not assume ownership from naming — verify in database and service layers
- Do not skip writing an ADR for decisions affecting multiple domains
- Do not treat the entry layer as the source of truth
- Do not merge cross-domain changes without affected domain owners' awareness

## Maturity | 成熟度

**Stage**: Effective — Extracted from enterprise ERP architecture governance with cross-domain boundary mapping patterns.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-architect-governor (15KB original)
- v1.1.0: Generalized to universal architecture governance patterns
- Source: Multi-domain enterprise system (ERP + Mall + App + Agent + SaaS)
