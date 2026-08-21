# AI Product Delivery Task Pack

> Product owner fills only sections 1-2. AI agents complete sections 3-9
> from verified project evidence. Do not ask the product owner to locate code,
> choose a framework, or describe internal implementation.
>
> For L2/L3, parallel, or high-risk work, create a companion machine-readable
> contract from `task_contract.json` and validate it with
> `scripts/py/validate_delivery_contract.py`.

## 1. Product Owner Input

| Item | Input |
| --- | --- |
| Business outcome | |
| Primary user and scenario | |
| Expected visible result | |
| Usability expectation | |
| Priority | P0 / P1 / P2 |
| Non-goals | |
| References, examples, screenshots | |
| Business-flow acceptance steps | |

## 2. Product Decision Log

| Decision | Options considered | Owner decision | Date |
| --- | --- | --- |
| Business rule ambiguity | | | |
| Scope trade-off | | | |
| Destructive operation / release authorization | | | |

## 3. AI Discovery and Routing

| Item | Evidence |
| --- | --- |
| Project classification | |
| Selected lead skill | |
| Supporting skills | |
| Existing pattern / reuse candidate | |
| Scripts and tools discovered | |
| Working-tree boundary | |
| Shared language / ADR context | None required / [path and terms] |
| Delivery contract | Not required / [task-local contract path] |

## 4. Code Location and Truth Map

```text
User flow / route:
Rendered Host and shared template:
Frontend service or client adapter:
Controller / transport adapter:
Aggregate interface and command gateway:
Orchestration and atomic service:
Domain truth / metadata / permissions:
Persistence / migration / external side effect:
Focused tests and release gates:
```

## 5. Scope, Safety, and Architecture

| Item | Decision |
| --- | --- |
| In scope | |
| Out of scope | |
| Truth owner | |
| Affected clients | |
| Candidate files and reason | |
| Delete / rename / migration classification | None / A / B / C / D |
| Rollback path | |
| L0-L3 gate | |
| Write allowlist / forbidden paths | |
| Destructive classification / owner confirmation | |

## 6. Executable Batches

| ID | Dependency | Write boundary | Public test seam / justified alternative | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| B-01 | None | | | | | |
| B-02 | B-01 | | | | | |

## 7. Verification Record

| Layer | Check | Result | Evidence path / command |
| --- | --- | --- | --- |
| Static | | | |
| Unit / contract | | | |
| API / database | | | |
| Browser / runtime | | | |
| Business-flow closure | | | |
| Fresh final evidence | Claim: | | command/check run after final relevant change |
| Release / deployment | | | |

## 8. Two-Axis Review

| Axis | Question | Result | Evidence / blockers |
| --- | --- | --- | --- |
| Standards / truth | Repository standards, truth ownership, architecture, quality gates | | |
| Product / spec | Outcome, business-flow acceptance, explicit non-goals | | |

## 9. Product Acceptance

| Acceptance flow | Expected | Actual | Owner decision |
| --- | --- | --- | --- |
| | | | Accept / Revise / Reject |

## 10. Delivery Closure

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
