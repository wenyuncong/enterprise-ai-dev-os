---
name: ai-foundation-governor
description: "Govern stable project foundations including version control, permissions, routes, feature switches, menus, API contracts, configuration ownership, release gates, and single-source platform rules. Use when foundational behavior or shared project infrastructure changes."
---

# ai-foundation-governor — Stable Foundation & Single Source of Truth Governor

## Purpose | 用途

Govern the project's stable foundation layer — the infrastructure that every feature depends on but no single feature owns:

- Version control, module/plugin management
- Permission system, role-based access control
- Menu/routing, unified navigation
- API standardization, unified login/SSO
- Field/metadata frameworks
- System/business parameters and configuration
- Database schema governance (versions, migrations, seeds)
- Runtime snapshots and compiled profiles
- Release gates and evidence collection

This skill is mandatory for tasks touching **any** foundation-layer component. Foundation breaks cascade into every feature.

## Core Rule | 核心规则

**Every capability has a single source of truth. Missing loops are closed before page patches.**

Never patch a feature at the surface layer (UI, API endpoint) when the root cause is in the foundation (permissions, schema, parameters, configuration). Classify first, then fix.

---

## 1. Classify the Source of Truth | 真相来源分类

Before modifying any foundation component, classify its authoritative source:

| Category | Typical Source of Truth | Verification Method |
|---|---|---|
| Version/module/plugin | Package registry, dependency manifests | Check package manager, entitlements |
| Feature flags/toggles | Feature flag service, config database | Check flag status, rollout rules |
| Permissions/RBAC | Permission tables, role assignments | Verify role-permission mapping |
| Authentication/SSO | Identity provider, token service | Check auth middleware, token validation |
| Field definitions | Field metadata registry | Verify field schemas, constraints |
| System parameters | Parameter/config service | Read runtime config, compile result |
| Business parameters | Domain-specific parameter tables | Check parameter templates, validation |
| Reports | Report service, fact tables | Verify report queries, data freshness |
| Database schema | Migration files, schema baselines | Check formal scripts, tenant schemas |
| Runtime profiles | Compiled AccessProfile, runtime policy | Verify profile snapshots |
| Audit/evidence | Audit logs, release evidence docs | Check audit trail completeness |

**If a task cannot be classified, do not write code. Inspect docs, database, and existing code first.**

---

## 2. Check Reality | 现实检查

Before making any foundation change, run the check-before-execute protocol:

| Check | Method | Minimum Verification |
|---|---|---|
| **Database** | `SHOW TABLES`, `DESCRIBE`, `SELECT COUNT(*)` | Table exists, columns match expectation |
| **Database governance** | Verify change belongs to `schema/`, `seed/`, `patch/`, or `templates/` | Correct formal source directory |
| **Code** | Locate service/controller/interceptor consumers | Understand all consumers before changing |
| **Documentation** | Read master control docs, release docs | Existing docs don't contradict the change |
| **Runtime** | API probes, browser checks, log inspection | Running system matches code state |

Never infer from naming conventions alone. Verify against actual database tables, actual code paths, and actual runtime behavior.

---

## 3. Backend Truth Rule | 后端真相规则

**Business truth must live in backend services, not in frontend entry layers.**

| Layer | Role | Allowed Actions |
|---|---|---|
| **Backend application services** | Source of truth | Validation, calculation, persistence, writeback |
| **Backend domain services** | Domain logic | Business rules, invariants, state transitions |
| **Backend atomic services** | Single-responsibility operations | Atomic writes, fact recording |
| **Frontend (Web/Mobile)** | Entry layer | Display, input collection, lightweight preview |
| **API adapters / AI tools** | Entry layer | Format translation, task dispatch |
| **External integrations** | Entry layer | Data ingestion, webhook handling |

**Acceptance check**: The same business action from any entry layer must produce identical validation, persisted result, writeback behavior, and audit facts.

---

## 4. Release Gates | 发布闸门

Every release must pass two minimum gates:

### DB Gate
- Formal schema scripts are in correct directories
- Baseline schemas match expected state
- Required tables, columns, indices exist
- Key seed rows are present
- System/business parameter values are correct

### Core Flow Gate
- Target tenant can authenticate and load runtime profile
- Core pages render without error
- Key API endpoints respond correctly
- Critical business flows (create, read, update, report) function
- Writebacks and audit trails complete

**A passing DB gate with a failing core flow gate is still a release blocker.**

---

## 5. Foundation Change Impact Checklist | 基础变更影响清单

Before merging any foundation change, verify:

- [ ] Permissions: RBAC tables, role assignments match
- [ ] Menus/Routes: Navigation structure intact
- [ ] APIs: Endpoints registered, auth middleware active
- [ ] Fields: Metadata registry consistent
- [ ] Parameters: Runtime compilation succeeds
- [ ] Schema: Migrations in correct directory, baselines updated
- [ ] Reports: Queries reference correct sources
- [ ] Tenants: All active tenants pass schema sync
- [ ] Release docs: Evidence collected

---

## Guardrails | 防护规则

- Do not modify foundation components without checking all consumers
- Do not create a second source of truth for any capability
- Do not skip the DB gate even for "small" changes
- Do not treat "works on my machine" as passing the core flow gate
- Do not delete audit evidence — classify and commit it

## Maturity | 成熟度

**Stage**: Effective — Extracted from enterprise ERP governance with 65KB of validated patterns and release gate procedures.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-stable-foundation-governor (65KB original)
- v1.1.0: Generalized to universal enterprise foundation patterns
- Source: 12+ months of enterprise ERP foundation governance
