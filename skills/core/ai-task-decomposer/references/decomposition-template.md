# AI-Native Task Decomposition Template

## 1. Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/docs/全项目总控/TASK_BACKLOG.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- current parent task pack, execution record, claim-pool row, and master task-table row

## 2. Scope Freeze

| Item | Content |
| --- | --- |
| Parent task / package | |
| Related task line | current mainline / governance support / special line / local line |
| In scope | |
| Out of scope | |
| Impacted modules / paths | |
| Existing packs already checked | |
| Hot-file or collaboration boundary | |

## 3. Verified Current-State Facts

| Type | Source | Verified fact | Blocking impact |
| --- | --- | --- | --- |
| Doc fact | | | |
| Code fact | | | |
| DB fact | | | |
| Runtime fact | | | |

## 4. `Current / Target / Implementation` Split

| Layer | Must answer |
| --- | --- |
| Current | what exists today, what is broken, what evidence proves it |
| Target | what the frozen result should be |
| Implementation | which concrete work items close the gap |

## 5. Batch Table

| Batch ID | Priority | Domain / Module | Layer | Scope | Dependency / Blocker | Files / paths | Acceptance | Evidence | Suggested owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | P0/P1/P2 | | current / target / implementation / QA | | | | | | |

## 6. Internal Pack vs External Dispatch

| Output type | Use when | Must include |
| --- | --- | --- |
| Internal decomposition pack | still needs chief-planner control or detailed dependency breakdown | blockers, split logic, risk notes, route-back rules |
| External dispatch pack | can be claimed by another dialog or worker directly | executable batches, write scope, acceptance, evidence, no hidden assumptions |

## 7. Handoff Block Template

```text
Task ID:
Parent task:
Task line:
Priority:
Scope:
Current facts:
Target state:
Implementation items:
Dependency / blocker:
Files / paths:
Acceptance:
Evidence required:
Do-not-touch boundaries:
```

## 8. Typical batch order

1. current-state verification
2. design or rule freeze
3. backend / DB base work
4. frontend or page work
5. integration / runtime verification
6. documentation closure and backfill
