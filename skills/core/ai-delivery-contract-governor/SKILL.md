---
name: ai-delivery-contract-governor
description: "Create and enforce machine-readable delivery contracts that bound write scope, stage transitions, test seams, fresh evidence, and independent two-axis review. Use for L2/L3 work, parallel agents, risky changes, or any task that needs rules to fail closed instead of relying on prose alone."
---

## Rule

No governed task may advance because an agent says it is ready. It advances only when its delivery contract permits the next state and the required evidence is present. The contract is fail-closed.

# ai-delivery-contract-governor - Executable Delivery Contract

## Purpose

Turn the existing 5S lifecycle into a small, machine-checkable task boundary:

```text
scope contract
-> approved write boundary
-> implementation
-> fresh evidence
-> independent two-axis review
-> safeguarded / completed
```

This skill complements `ai-5s-delivery-governor`. It does not replace a project's business rules, CI, release process, permission system, or runtime source of truth.

## When to Use

- L2/L3 delivery, shared capability, schema, permission, release, or cross-module write path.
- Parallel or handoff work where agents need non-overlapping write boundaries.
- A task needs enforceable proof that it stayed in scope.
- A project wants local/CI rejection for stale evidence, missing review, or changed files outside the agreed boundary.

L0/L1 work may use the same contract when useful, but should not be burdened with ceremony that does not reduce real risk.

## Contract Assets

Use the project-owned assets:

- Schema: `docs/全项目总控/schemas/governance/delivery-contract.schema.json`
- Template: `docs/_templates/全项目总控/task_contract.json`
- Validator: `scripts/py/validate_delivery_contract.py`

Create one task-local contract from the template. Keep it with the task pack or project-owned delivery record; never place it in a generic temporary directory.

## Required Contract Content

Before writing, record:

1. product outcome, acceptance steps, and non-goals;
2. change type, target line/version, affected flow, and L0-L3 gate;
3. authoritative truth owner;
4. exact write allowlist, forbidden paths, and destructive classification;
5. focused public test seam or justified alternative evidence;
6. final proof commands/checks that must run after the last relevant change;
7. separate standards/truth and product/spec reviews.

For `review_required` or `explicit_owner_confirmation`, do not perform destructive work until the contract records the required decision.

## State and Gate Rules

| Status | Meaning | Minimum gate to enter |
| --- | --- | --- |
| `draft` | Initial idea only | No implementation |
| `scoped` | Outcome, scope, truth owner, and evidence plan exist | Scope validator passes |
| `approved` | Required owner/destructive decision is recorded | Approved task may write only within allowlist |
| `implementing` | Scoped work is underway | Changed files remain within allowlist |
| `safeguarded` | Final proofs are fresh and both reviews pass | Validator passes with `--check-freshness` |
| `completed` | Project integration/release conditions are also satisfied | 5S closure plus safeguarded contract |
| `blocked` / `cancelled` | Work may not silently continue | Record blocker or cancellation reason in the task pack |

For L2/L3, `verification_owner` must differ from `implementer` before `safeguarded` or `completed`. The independent verifier may use project-owned CI, another agent, or a reviewer, but must review actual evidence rather than the implementer's summary alone.

## Validation Workflow

1. Validate the task record before implementation:

```text
py scripts/py/validate_delivery_contract.py --contract <task-contract.json>
```

2. Validate observed or staged paths before integration:

```text
py scripts/py/validate_delivery_contract.py --contract <task-contract.json> --changed-file <repo-relative-path>
```

3. After the final relevant change, append evidence records and run:

```text
py scripts/py/validate_delivery_contract.py --contract <task-contract.json> --check-freshness
```

4. Run the project's actual tests, runtime checks, database readbacks, and release gates. This validator checks the contract discipline; it does not fabricate domain evidence.

## Guardrails

- Do not use broad allowlists such as `**` to hide unrelated work.
- Do not put an out-of-scope file into the allowlist after implementation merely to make validation pass; reopen Scope/Specify and record the reason.
- Do not claim final evidence from a run that predates the final relevant change.
- Do not let a passing standards/truth review waive failed product acceptance, or the reverse.
- Do not allow the implementer to self-certify L2/L3 safeguarding without an independent verifier.
- Do not treat this JSON record as a replacement for owner approval on business ambiguity, destructive work, or release authorization.

## Evolution History

- v1.0.0: Introduced executable delivery contracts from GSD-style phase gates and role-separated review practices, adapted to AI-OS 5S, product-directed delivery, and backend-truth governance.
