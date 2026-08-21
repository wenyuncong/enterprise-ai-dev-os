---
name: ai-5s-delivery-governor
description: "Govern change delivery with a lightweight Scope, Specify, Ship, Safeguard, Sell lifecycle. Use for versioned delivery, branch routing, release candidates, hotfixes, acceptance gates, deployment evidence, or any task whose completion must be auditable."
---

## Rule

Every deliverable change must have: 1) a bounded scope, 2) an owning truth and acceptance definition, 3) a traceable implementation, 4) independent evidence, and 5) an explicit release decision. Never treat a local code edit or local commit as delivered.

# ai-5s-delivery-governor - 5S Delivery Governance

## Purpose

Apply a compact delivery state machine without turning ordinary engineering work into paperwork:

```text
Scope -> Specify -> Ship -> Safeguard -> Sell
```

This skill is for delivery governance, not for replacing the project's existing Git, CI, deployment, test, or release scripts. Reuse those project entrypoints as the evidence source.

## When to Use

- A task changes a versioned product, shared service, schema, permission, release artifact, or deployment target.
- A bug may affect a supported or production baseline.
- A release candidate, hotfix, rollback, release tag, or acceptance decision is involved.
- The user asks for delivery status, formal closure, release readiness, or a change-management rule.

For a purely local experiment, documentation draft, or read-only audit, record the applicable stages but do not invent branch or release ceremony that the project does not use.

## 5S State Machine

| Stage | Question | Minimum record | Blocking condition |
|---|---|---|---|
| Scope | What changes, for whom, and what is explicitly out? | Change type, target version, in/out scope | Do not start implementation |
| Specify | Which truth owner, data, clients, and regressions are affected? | Owner, impact, acceptance gate, rollback/data notes | Do not integrate |
| Ship | Was the approved scope implemented through the project path? | Scoped diff, tests, migration/config changes | Do not promote |
| Safeguard | Has an independent check exercised the real risk boundary? | Build/API/browser/DB/flow evidence | Do not release |
| Sell | Is the version allowed to reach its intended audience? | Release/tag/deploy decision, known limits, rollback point | Do not claim delivery |

Use concise records. A short issue, PR description, release ledger row, or structured task record is sufficient when it carries the required facts.

## Branch and Baseline Routing

Projects may use different branch names, but the responsibilities must remain distinct:

| Line | Purpose | Typical allowed work |
|---|---|---|
| Integration line | Continuous development | New capability, usability work, non-baseline bugs |
| Stable line | Supported or production baseline | Reproducible baseline bugs, security, necessary compatibility fixes |
| Frozen candidate | Short-lived acceptance version | Registered release blockers only |

Rules:

1. Route a bug by the baseline where it reproduces, not by where it was discovered.
2. A stable fix must be returned to the integration line before closure.
3. A frozen candidate must reject new features and unrelated refactors.
4. Isolated worktrees can protect concurrent implementation, but formal integration and release still occur through the approved delivery lines.
5. A project with multiple required remotes must prove the approved commit reached each required remote before calling the delivery closed.

## Acceptance Gate Selection

Choose the smallest gate that proves the actual risk:

| Gate | Typical scope | Minimum evidence |
|---|---|---|
| L0 | Copy, read-only status, cosmetic local display | Target route/API is reachable and the intended display is visible |
| L1 | One component, page, endpoint, or local bug | Changed interaction plus the affected build/compile check |
| L2 | Shared business module, command, aggregate, metadata, or write path | Runtime profile or contract, command execution, and authoritative fact readback |
| L3 | Schema, tenant/permission/version policy, cross-module writeback, release, deployment, or production risk | Lifecycle regression plus DB, runtime, client, and release evidence |

A health endpoint only proves process availability. It never proves business closure.

## Standard Workflow

1. Inspect the current branch, working tree, required remotes, and project delivery scripts.
2. Classify the change as usability, bug, existing-flow semantic change, or new capability.
3. Record Scope and Specify before writing: target version, affected flow, truth owner, non-goals, gate, and rollback/data impact.
4. For L2/L3, parallel, or high-risk work, create and validate the project `DeliveryContract` through `ai-delivery-contract-governor` before writing and again before Safeguard.
5. Ship only the scoped change. Stage exact task files and preserve unrelated worktree changes.
6. Safeguard with project-owned commands and real runtime/DB evidence appropriate to L0-L3.
7. Sell only after the approved integration, tag/deploy decision, and required remote/CI evidence are complete.
8. Record non-blocking debt separately. Do not expand the task merely to make the ledger look clean.

## Required Closure Statement

When reporting a delivery result, include:

```text
Change type:
Target version / line:
Affected flow:
Truth owner:
Selected gate:
Evidence:
Delivery state: complete / paused / blocked
Known limits or follow-up:
```

Use `complete` only when Safeguard has passed and the project's required integration or release action has actually happened. Use `paused` or `blocked` for unpushed commits, failed evidence, unavailable remotes, or ongoing integration.

## Guardrails

- Do not let a branch name replace evidence.
- Do not declare a task complete from a local commit alone.
- Do not use a release candidate as a general "more stable" development branch.
- Do not let release governance duplicate or override backend truth, database facts, or project-owned scripts.
- Do not force L3 on a small local change merely because the project has release tooling.
- Do not skip L3 when schema, authorization, version entitlement, deployment, or cross-module writeback is actually in scope.
- Do not allow a DeliveryContract to replace the real project test, runtime, database, CI, or release gate it names.

## Evolution History

- v1.0.0: Generalized from the GERP 5S delivery state machine and three-line release governance, with project-specific paths and remote names removed.
