---
name: ai-flow-closure-audit
description: "Audit whether a business flow is closed across page, API, database, parameters, permissions, downstream writeback, reports, evidence, and regression tests. Use before declaring a business process complete or when checking end-to-end readiness."
metadata:
  requires:
    scope: universal
    declared-by: enterprise-ai-dev-os
---

## Rule

Closure audit checks: 1) Task has defined acceptance criteria, 2) Evidence of completion exists, 3) Verification step was executed, 4) Output matches expected output, 5) No unresolved issues remain. Never mark done without closure evidence.

# ai-flow-closure-audit — End-to-End Business Flow Closure Auditor

## Purpose

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
| **Product Acceptance** | Intended user can complete the real business flow efficiently? | Product-owner acceptance record | P1 (delivery risk) |

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
- **Product acceptance**: Execute the owner-defined business-flow test and record accept/reject/revise feedback

### Step 2b: Write-back Consistency Cross-check | 写回一致性交叉校验

A writeback is only closed when the numbers reconcile across layers. For any flow that moves quantities, amounts, balances, or status, add a **consistency cross-check** that scans for mismatches instead of trusting a single sample row:

1. **Map the reconciliation pairs**: source table → downstream table for every writeback (e.g., a receipt increments both inventory and payable).
2. **Design the check**: aggregate each side independently and compare; for calculated values (averages, balances) also recompute from raw rows.
3. **Run a full-table scan**: locate rows where source and downstream disagree; a single pass often surfaces hidden drift that sample-based checks miss.
4. **Record the discrepancy**: table, row, expected vs actual, and the likely root cause.
5. **Fix and rerun**: after the fix, the cross-check must return zero mismatches before closure.

```text
Example (domain-specific, from ERP): purchase receipt -> inventory + payable
  SELECT aggregate(inventory_qty) FROM inventory WHERE receipt_id = :id;
  SELECT aggregate(payable_amount) FROM payable WHERE receipt_id = :id;
  -- both must reconcile with the receipt line totals; any drift is a P1 data risk
```

This step is stack- and domain-neutral: the pattern is "reconcile every writeback with a cross-check, not a sample", whatever the business numbers are.

### Step 2a: Review Two Independent Axes

Before calling a non-trivial flow ready, keep these findings separate:

| Axis | Question | Minimum evidence |
|---|---|---|
| **Standards / truth** | Does the change follow repository standards, source-of-truth ownership, architecture boundaries, security/quality gates, and the selected L0-L3 gate? | Scoped diff review, relevant audit/build/test/runtime evidence |
| **Product / spec** | Does the flow deliver the originating business outcome and acceptance steps without violating explicit non-goals or adding unapproved behavior? | Product contract, acceptance record, observed behavior |

Neither axis masks the other. A technically clean implementation that misses the business outcome fails the audit; a behaviorally correct implementation that violates truth or architecture boundaries also fails.

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
| Product acceptance | ✅/❌/⚠️ | [Business-flow test record] | [notes] |

### Two-Axis Review
| Axis | Status | Evidence | Blockers / Notes |
|---|---|---|---|
| Standards / truth | ✅/❌/⚠️ | [diff, audit, test, runtime evidence] | [notes] |
| Product / spec | ✅/❌/⚠️ | [outcome, acceptance, non-goals evidence] | [notes] |

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
- Do not treat technical verification as a substitute for product-owner business-flow acceptance
- Do not merge standards/truth findings with product/spec findings; report and resolve both axes independently
- Do not use stale output or an agent report as closure evidence; rerun the proving check after the final relevant change

## Maturity | 成熟度

**Stage**: Effective — Extracted from enterprise ERP flow closure audits across purchase/sales/inventory/finance chains.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-flow-closure-audit (12.5KB original)
- v1.1.0: Generalized to universal business chain closure framework
- v1.2.0: Added product-owner business-flow acceptance as an explicit closure layer
- Source: O2C, S2P, R2R chain audits in enterprise ERP
