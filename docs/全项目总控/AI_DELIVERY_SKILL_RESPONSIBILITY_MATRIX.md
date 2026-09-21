# AI Delivery Skill Responsibility Matrix

## Purpose

This matrix gives every non-trivial AI delivery task one primary owner per
delivery stage. It prevents skill overlap from turning into duplicated plans,
contradictory rules, or repeated verification.

It applies to methodology work and to projects that adopt this methodology.
It does not replace project-specific rules, technology skills, or domain
acceptance criteria.

## Delivery Stages

| Stage | Primary skill | Supporting skills | Owns | Must not own |
| --- | --- | --- | --- | --- |
| Classify | `ai-project-classifier` | `ai-brownfield-analyzer` | Project origin, quality target, platforms, scale, baseline skill set | Detailed task plan or implementation |
| Onboard methodology | `ai-project-onboarding-and-skill-integration` | `ai-project-classifier`, `ai-brownfield-analyzer`, `ai-skill-governor` | Technology profile, non-mutating copy plan, external candidate quarantine, integration record, bounded knowledge index | Silent overwrite, direct activation of external content, runtime/business truth |
| Route | `ai-rule-dispatcher` | `ai-project-classifier` | Task line, one lead skill, first documents, first factual checks | Batch breakdown or code changes |
| Discover | `ai-brownfield-analyzer` | `ai-reference-researcher`, tech skills | Existing architecture, scripts, conventions, extension points, intervention level | Rewriting unrelated working code |
| Define product outcome | `ai-product-directed-delivery` | `ai-competitor-analyst`, `ai-ui-ux-governor` | Product-owner contract, scenario, usability, business acceptance, handoffs | Internal implementation choice without evidence |
| Plan program | `ai-chief-planner` | `ai-task-decomposer`, `ai-5s-delivery-governor` | Milestones, backlog state, dependency order, closure state | File-level implementation details |
| Split execution | `ai-task-decomposer` | `ai-chief-planner`, `ai-command-executor` | Atomic batches, write boundaries, dependencies, batch acceptance | Release authorization or business-policy invention |
| Enforce delivery contract | `ai-delivery-contract-governor` | `ai-5s-delivery-governor`, `ai-command-executor` | Machine-readable write scope, stage transitions, fresh evidence, independent review | Replacing project CI, business truth, or owner authorization |
| Design architecture | `ai-architect-governor` | `ai-atomic-architect`, `ai-domain-boundary-mapper` | Architectural decision, trade-offs, ADR, ownership boundaries | Product acceptance or transport-specific implementation |
| Define capability chain | `ai-atomic-architect` | `ai-single-truth-enforcer`, `ai-foundation-governor` | Truth -> atom -> orchestration -> aggregate -> command gateway -> adapter -> Host contract | Page-local business rules or duplicated truth |
| Implement safely | `ai-command-executor` | Stack skill, `ai-library-first`, relevant governance skill | Approved commands, tool use, working-tree gate, scoped execution evidence | Task routing, product policy, release decision |
| Govern truth and fields | `ai-single-truth-enforcer` | `ai-field-package-governor`, `ai-foundation-governor` | Backend/data truth, policy boundary, field source, error severity | Visual layout ownership |
| Build UI | `ai-component-standardizer` | `ai-ui-ux-governor`, frontend stack skill | UI atom, composition, standard template, Host boundary | Domain calculation, authorization, write policy |
| Verify business flow | `ai-flow-closure-audit` | `ai-runtime-verify`, `ai-frontend-audit` | Page -> API -> truth -> writeback -> report closure; standards/truth and product/spec two-axis review | Release/version promotion |
| Verify runtime | `ai-runtime-verify` | Stack skill, `ai-command-executor` | Executed runtime path, browser/API/log/side-effect evidence | Static architecture judgment |
| Govern delivery | `ai-5s-delivery-governor` | `ai-chief-planner`, `ai-command-executor` | Scope/Specify/Ship/Safeguard/Sell state, L0-L3 gate, release evidence | Business-domain truth |
| Evolve methodology | `ai-skill-evolver` | `ai-skill-governor` | Evidence-backed skill/rule/template updates after repeated patterns | Routine project implementation |
| Audit methodology health | `ai-skill-governor` | `ai-skill-evolver`, `ai-rule-dispatcher` | Contradiction, overlap, stale rule, orphan, routing coverage review | Automatic merge or deletion of skills |

## Boundary Rules

1. `ai-rule-dispatcher` selects one lead skill. Supporting skills advise but do
   not create competing plans.
2. `ai-chief-planner` owns program-level sequencing; `ai-task-decomposer` owns
   execution-sized batches.
3. `ai-architect-governor` decides architecture trade-offs; `ai-atomic-architect`
   defines the reusable capability chain after that decision.
4. `ai-product-directed-delivery` owns the human/AI responsibility contract;
   `ai-5s-delivery-governor` owns delivery state and release evidence.
5. `ai-runtime-verify` proves a running path; `ai-flow-closure-audit` proves
   the end-to-end business chain.
6. `ai-skill-governor` reports overlap. It never merges or deletes a skill
   without an explicit scoped decision.
7. `ai-delivery-contract-governor` is mandatory for L2/L3, parallel, or
   high-risk work when a project adopts machine-readable delivery contracts.

## Required Handoff

Every handoff must carry only the facts needed by the next owner:

```text
Outcome and non-goals:
Current-state evidence:
Truth owner:
Selected lead skill and support skills:
Write boundary:
Acceptance and gate:
Known risks / rollback:
```

## Review Trigger

Review this matrix when any of the following happens:

- a new official skill is added;
- three or more skills are changed in one delivery;
- a task receives two competing lead skills;
- a repeated task bypasses the intended lead skill;
- a methodology scenario regression fails.
