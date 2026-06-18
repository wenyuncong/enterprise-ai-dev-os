---
name: ai-flow-closure-audit
description: "Audit whether a business flow is closed across page, API, database, parameters, permissions, downstream writeback, reports, evidence, and regression tests. Use before declaring a business process complete or when checking end-to-end readiness."
---

# ai-flow-closure-audit — End-to-End Business Flow Closure Auditor

## Purpose | 用途

Audit whether a business chain is truly closed — from entry layer to API to database to downstream writeback to reporting.

This skill detects gaps where:
- An entry action has no backend validation
- A database write has no downstream writeback
- Business rules exist only in frontend code
- Reports query stale or incomplete data
- Parameters/switches are not consumed correctly

**Core principle**: Do not call a flow "closed" without evidence at every layer.

---

## Audit Layers | 审计层级

A business chain is only "closed" when evidence exists at ALL layers:

| Layer | Check | Evidence Required | Gap Severity if Missing |
|---|---|---|---|
| **Entry/UI** | Action available? Correct validation? | Screenshot or page verification | P2 (UX gap) |
| **API** | Endpoint exists? Correct method/auth? | curl test, API response log | P0 (blocker) |
| **Service/Logic** | Business logic complete? Transactional? | Code review + unit test | P0 (blocker) |
| **Database** | Tables/columns correct? Constraints? | `DESCRIBE` + `SELECT` samples | P0 (blocker) |
| **Parameters/Switches** | Config consumed correctly? | Parameter audit, switch check | P1 (data risk) |
| **Writeback** | Downstream truth updated? | Trace data flow end-to-end | P1 (data risk) |
| **Report/Analytics** | Reports reflect writeback? | Query comparison, freshness check | P1 (data risk) |
| **Audit/Evidence** | Actions recorded? Trail complete? | Audit log verification | P2 (compliance) |

---

## Business Chain Categories | 业务链分类

| Chain | Description | Typical Scope |
|---|---|---|
| O2C (Order to Cash) | Sales order → delivery → invoice → payment | Sales, Inventory, Finance |
| S2P (Source to Pay) | Purchase req → order → receipt → payment | Procurement, Inventory, Finance |
| R2R (Record to Report) | Transaction → ledger → financial report | Finance, Reporting |
| L2C (Lead to Cash) | Lead → opportunity → quote → order | CRM, Sales |
| Fulfillment | Order → pick → pack → ship | WMS, Logistics |
| Subscription | Signup → activate → bill → renew/cancel | SaaS, Billing |

---

## Standard Workflow | 标准工作流

### Step 1: Map the Chain
- Identify all nodes: entry → API → service → DB → writeback → report
- Identify all parameters/switches affecting the chain
- Document the expected state transitions

### Step 2: Verify Each Node
For each node, collect concrete evidence:
- **Entry**: Screenshot of available action, verify form validation
- **API**: `curl` response with expected status code and body
- **Service**: Code review of business logic path, transaction boundaries
- **Database**: `DESCRIBE table`, sample rows before and after action
- **Writeback**: Trace data from source table to downstream table
- **Report**: Query report output, compare with source data freshness

### Step 3: Identify Gaps
Where is the chain broken? Classify:
- **P0 (Blocker)**: Missing backend validation, broken API, missing table
- **P1 (Data Risk)**: Incomplete writeback, stale reports, missing parameter gating
- **P2 (UX/Compliance)**: Missing audit trail, inconsistent UI behavior

### Step 4: Produce Fix Tasks
Convert each gap into a concrete task:
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

### Gap Summary
- P0: [count] blockers
- P1: [count] data risks
- P2: [count] UX/compliance issues
```

---

## Guardrails | 防护规则

- Do not claim closure without evidence at every layer
- Do not accept "frontend handles it" as closure for business rules
- Do not skip writeback verification — it's the most common hidden gap
- Do not audit from imagination — verify against actual running code and database
- Do not treat a passing API test as full closure without database/writeback verification

## Maturity | 成熟度

**Stage**: Effective — Extracted from enterprise ERP flow closure audits across purchase/sales/inventory/finance chains.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-flow-closure-audit (12.5KB original)
- v1.1.0: Generalized to universal business chain closure framework
- Source: O2C, S2P, R2R chain audits in enterprise ERP
