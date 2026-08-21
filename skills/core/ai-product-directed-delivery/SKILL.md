---
name: ai-product-directed-delivery
description: "Run AI-native product delivery where a product owner defines outcomes, usability, and business acceptance while AI agents perform analysis, research, architecture, implementation, verification, and delivery evidence. Use for product-led enterprise delivery, non-programmer-led development, end-to-end feature work, or explaining human and agent responsibilities."
---

## Rule

The product owner decides business outcome, usability, scope, and final acceptance. AI agents own the engineering execution path and must prove it with code, runtime, data, and release evidence. Never force a product owner to write code, and never let an AI agent invent product intent, business policy, or acceptance on the owner's behalf.

# ai-product-directed-delivery - AI-Native Product Delivery Operating Model

## Purpose

Make product delivery accessible to a product owner who does not program while keeping engineering rigor high:

```text
Product intent and acceptance
  -> AI analysis and benchmark
  -> architecture and truth boundary
  -> implementation and verification
  -> product-owner business acceptance
  -> governed release
```

This is not "prompt to page generation." It is a controlled operating model in which human judgment stays with product decisions and AI agents execute a verifiable engineering system.

## Responsibility Boundary

| Role | Owns | Does not own |
|---|---|---|
| Product owner | Business goal, target user, workflow result, product presentation, usability judgment, priorities, non-goals, final business acceptance | Writing code, designing database tables, selecting internal framework patterns, bypassing verification |
| AI product analyst | Requirement clarification, scenario map, acceptance draft, ambiguity log | Replacing the owner's business decision |
| AI researcher | Competitor/reference evidence and options | Treating competitor behavior as the product decision |
| AI architect | Truth ownership, domain boundary, atom/orchestration/aggregate design, migration risk | Moving business truth into a client or inventing unapproved scope |
| AI delivery agent | Database, backend, frontend, tests, scripts, documentation, exact staging | Declaring business acceptance without evidence and owner confirmation |
| AI verifier/auditor | Independent runtime, API, DB, writeback, browser, and release checks | Explaining away a failed gate |
| Product owner at acceptance | Confirms the intended flow is understandable, efficient, and correct for actual work | Accepting a flow whose evidence or business result is missing |

The product owner can provide plain language, examples, screenshots, reference products, and a completed business-flow test. The AI system translates those inputs into engineering work and returns evidence in product language.

## Product-to-Engineering Contract

Before implementation, capture the smallest useful contract:

```text
Business outcome:
Primary user and scenario:
Expected visible result:
Usability constraints:
Business-flow acceptance:
Non-goals:
Known examples or references:
```

The AI team adds:

```text
Truth owner:
Affected domain and clients:
Change type and delivery gate:
Technical acceptance:
Data/writeback/report impact:
Risk and rollback notes:
```

If the business outcome is unclear, ask for clarification. If the engineering path is unclear, the AI investigates it; it must not send that burden back to the product owner as a programming task.

## Shared Language and Decision Context | 共享语言与决策上下文

When a delivery introduces or depends on ambiguous business terms, stable abbreviations, or cross-session decisions, create or update concise project-owned context under `docs/`:

- A glossary/context record defines the agreed meaning of domain terms and abbreviations.
- An ADR or decision record captures a durable architectural or scope decision with alternatives and consequences.
- Specifications, test names, APIs, and code reuse the agreed language so agents and people do not invent parallel names.

This is proportional to risk. Do not require a glossary for a one-line local fix, and do not let a glossary become a second source of business truth. The database/domain model and accepted business rules remain authoritative.

## Twelve-Step Product Delivery Map

| Step | Product owner contribution | AI agent responsibility | Exit evidence |
|---|---|---|---|
| 1. Outcome | State the user-visible business result | Convert intent into scenarios and non-goals | Approved outcome contract |
| 2. Process | Describe the real business flow or test case | Map states, roles, inputs, outputs, exceptions | Flow map and acceptance cases |
| 3. Benchmark | Provide references when useful | Verify competitor behavior and separate fact from choice | Benchmark decision |
| 4. Architecture | Confirm trade-offs that affect product scope | Define domain boundary, truth owner, and interfaces | ADR or architecture note |
| 5. Data | Clarify business meaning of fields | Verify schema and data ownership | DB/metadata evidence |
| 6. Atomic backend | Review only visible behavior | Implement or reuse atomic services and validation | Unit/API evidence |
| 7. Orchestration | Confirm expected workflow outcome | Compose atomic services and writeback | Command-flow evidence |
| 8. Aggregate and command | Confirm exposed actions and blockers make sense | Publish aggregate profile/API and command-gateway contract | Runtime profile and permission evidence |
| 9. Frontend composition | Review presentation and ease of use | Build UI atoms, composition, templates, and Host page | Browser evidence |
| 10. Integration | Execute the intended business flow | Verify page -> API -> DB -> writeback -> report | Flow-closure evidence |
| 11. Acceptance | Test the completed business flow | Record defects, fix, and rerun affected gates | Product acceptance record |
| 12. Delivery | Decide whether the result may reach users | Run 5S safeguard/sell closure and record limits | Release/deployment evidence |

Steps are dependency-aware, not paperwork. A small local usability change may use a short path; data, permissions, cross-client commands, and releases must execute the relevant full chain.

## Backend Delivery Chain

Every reusable business capability follows this ownership path:

```text
Database and domain facts
  -> atomic service
  -> atomic orchestration or application service
  -> aggregate interface
  -> command gateway
  -> Web / App / AI / MCP / OpenAPI adapters
  -> Host page or client surface
```

Definitions:

- **Atomic service** owns one cohesive business capability: validation, persistence, calculation, audit, or fact production.
- **Atomic orchestration** composes atoms for a business workflow and owns transaction, sequencing, compensation, and downstream writeback.
- **Aggregate interface** returns the client-ready read model: runtime profile, fields, permissions, supported commands, blockers, and relevant facts.
- **Command gateway** is the only executable entry for a reusable business command. It checks identity, tenant, authorization, data scope, version policy, state, idempotency, confirmation requirement, audit, and provider coverage before dispatch.
- **Adapters** translate transport only. REST, Web, App, MCP, OpenAPI, desktop, or connectors must not recreate business rules.
- **Host** loads and renders the aggregate contract, collects permitted input, requests commands, and displays results.

Do not expose a command because a button exists. A command is executable only after the backend gateway proves its contract and prerequisites.

## Frontend Delivery Chain

The frontend has its own reuse architecture, but it never becomes a second business engine:

```text
Backend runtime / FieldPackage / aggregate profile
  -> UI atom
  -> UI orchestration
  -> standard page template
  -> Host page
  -> user interaction and feedback
```

Definitions:

- **UI atom** is a focused reusable visual or interaction capability such as a field renderer, selector, line table, status tag, action bar, filter, result summary, or blocking dialog.
- **UI orchestration** composes UI atoms from backend-returned runtime/profile facts. It may coordinate loading, local input state, navigation, accessibility, and presentation feedback.
- **Standard template** supplies the stable shell for list, document, report, dashboard, or settings pages.
- **Host page** chooses the template and composes the supported UI atoms. It must not define an alternative state machine, duplicate field truth, calculate business values, decide permissions, or implement a second command path.

The frontend may validate required input for immediate usability feedback, but the backend remains authoritative for business validation and every write decision.

## Required Handoffs

| Handoff | Required content |
|---|---|
| Owner -> AI | Outcome, scenario, examples, usability expectation, acceptance test |
| Analyst -> architect | Ambiguities, acceptance criteria, flow map, benchmark facts |
| Architect -> delivery | Truth owner, backend chain, client contract, affected templates, selected gate |
| Delivery -> verifier | Scoped changes, commands/tests, expected facts, known risks |
| Verifier -> owner | Product-visible result, passed/failed evidence, known limits, acceptance test instructions |
| Owner -> release | Accept / reject / revise decision for the tested business flow |

## Testable Seams and Fresh Evidence | 可测试边界与新鲜证据

For new or changed domain rules, bug regressions, command/orchestration behavior, and other testable public interfaces:

1. Name the public seam and expected behavior before implementation.
2. Write a focused test that fails for the intended behavior.
3. Implement the smallest change that passes it.
4. Rerun the focused test and affected regressions after the final relevant change.

Do not force red-green work onto copy-only, generated, configuration-only, or exploratory tasks where a focused behavioral test is not meaningful. Record the selected alternative evidence instead.

Before a completion, commit, release, or readiness claim, run the command, runtime check, API call, database readback, or diff inspection that proves the claim **after the final relevant change**. Earlier passing output, a health endpoint, or an agent report is not sufficient evidence.

## Standard Workflow

1. Start from product outcome, not implementation wording.
2. Convert the outcome into a short scenario and business acceptance contract.
3. Search current project patterns and benchmark only when it changes a real product decision.
4. Declare backend truth ownership before designing a page.
5. Reuse or build the backend atom -> orchestration -> aggregate -> command-gateway chain.
6. Build the frontend runtime -> UI atom -> composition -> template -> Host chain.
7. Verify technical closure independently.
8. Let the product owner run the business-flow acceptance from the intended user's perspective.
9. Use `ai-5s-delivery-governor` for final delivery state and release evidence.
10. Review the change on two independent axes: standards/truth/architecture compliance and the originating product outcome, acceptance flow, and non-goals.
11. Feed recurring lessons into the existing owning skill instead of creating parallel rule sets.

## Safe Change Protocol | 安全修改协议

AI-led delivery must be safe for a product owner who does not read code. The default is **read, prove, then change**. An agent must not treat a repository as disposable just because it can write files.

### 1. Establish the Change Boundary

Before a write, rename, deletion, migration, or command execution, the agent records:

```text
Requested business result:
Suspected truth owner and execution path:
Candidate files and why each is relevant:
Expected impact boundary:
Existing unrelated working-tree changes:
Selected verification and rollback evidence:
```

The agent must search for existing implementations, tests, routes, scripts, and shared components before creating replacements. A symptom on one page is not proof that the page owns the problem.

### 2. Classify Deletions and Destructive Operations

| Class | Examples | Default action |
|---|---|---|
| A: disposable | Confirmed generated output, task-owned temporary evidence, reproducible cache | Delete only after proving it is generated or replaceable |
| B: task-owned source | A newly created file or a source file exclusively superseded by the accepted change | Check inbound references, tests, build impact, and rollback path before deletion |
| C: shared or unknown source | Shared component, service, schema, script, configuration, historical migration, or a file with unclear ownership | Preserve by default; require explicit owner decision before delete or destructive rewrite |
| D: persistent/destructive | Database rows, schema, production configuration, tenant data, release artifacts, `git reset --hard`, `git clean -fdx` | Never execute without explicit confirmation and a documented backup, scope, and recovery path |

Rename and bulk replacement are destructive when they can break references or hide semantics. They follow the same impact check as deletion.

### 3. Prove Impact Before the Change

For a source deletion, rename, shared refactor, schema change, or broad replacement, inspect at least:

1. References and imports with project search.
2. Route/menu/runtime entry path where the behavior is user-visible.
3. Tests, build scripts, migrations, release scripts, and generated artifacts that depend on it.
4. Working-tree and staged changes so unrelated work is not absorbed.
5. A rollback method: revertible patch, retained migration, backup, or known-good commit.

Do not delete a file merely because it has no obvious direct import. It may be loaded by configuration, reflection, code generation, build tooling, deployment, or a runtime route.

### 4. Use Patch-Level Control

- Modify the smallest set of files that can own the requested outcome.
- Review the diff after every meaningful batch; verify that it only expresses the declared change boundary.
- In a dirty working tree, stage exact task-owned files or exact hunks only; inspect the staged diff and run a staged diff check before commit.
- Never use repository-wide cleanup to make a working tree look clean. Unrelated changes remain untouched.
- Never use destructive Git commands such as `reset --hard` or `clean -fdx` without explicit confirmation.
- If evidence conflicts or the owner is ambiguous, stop the destructive path and present the decision in business language.

## Code Location Protocol | 精准代码定位协议

The product owner describes a defect or new capability in business language. AI agents translate it into a verified delivery path; they do not ask the owner to hunt files or name classes.

### Trace Order

```text
Business symptom or requested result
  -> menu / route / permission entry
  -> actual rendered Host page
  -> standard template and shared UI component
  -> frontend service / API wrapper
  -> controller or transport adapter
  -> command gateway / aggregate interface
  -> orchestration / atomic service
  -> domain fact, FieldPackage / BusinessProfile / permission
  -> mapper / database / migration history
  -> focused tests, runtime gate, release gate
```

For a direct route, verify real authenticated navigation and the actual rendered component. Multiple menus may share one Host; a visually similar page may be backed by a different command or truth owner.

### Required Location Report Before Editing

Before implementation, the agent reports internally or to the owner in compact product language:

```text
Suspected business flow:
Evidence found:
Exact candidate files:
Chosen owner of the fix:
Expected affected surfaces:
Verification path:
```

Classify the outcome before coding:

| Finding | Correct response |
|---|---|
| UI-only presentation issue | Change a shared UI atom/template/Host only after confirming no backend fact is wrong |
| Backend truth or business rule issue | Fix the domain service, orchestration, aggregate, or command gateway; clients render the returned result |
| Shared field, permission, status, or command issue | Fix the authoritative metadata/profile/policy and test all known clients |
| Cross-domain side effect | Trace the writeback chain, transaction boundary, audit/history, and affected reports before patching |
| Business ambiguity | Return the smallest decision needed from the product owner; do not invent a business rule |

## Major Project Autopilot | 重大项目自动驾驶

For an enterprise project, the product owner does not need to become a developer or a project manager of source files. The owner provides outcomes, examples, priorities, usability feedback, and completed business-flow acceptance. AI agents maintain the engineering map and execute it in verified batches.

### Operating Loop

1. **Frame**: turn the product outcome into a scenario, non-goals, risks, and acceptance flow.
2. **Map**: discover the existing architecture, code locations, dependencies, scripts, data truth, and affected clients.
3. **Batch**: split work into dependency-safe batches and assign an L0-L3 gate through `ai-5s-delivery-governor`.
4. **Execute**: implement only the current batch using the safe change and code location protocols.
5. **Prove**: run proportionate unit, API, database, browser, workflow, build, and release checks.
6. **Present**: give the owner a decision-ready result: visible change, accepted flow, evidence, limits, and the next business decision.
7. **Release or iterate**: release only after owner acceptance and required safeguards; otherwise return defects to the correct batch.

The AI system stops and asks the product owner only for a real business ambiguity, an irreversible/destructive decision, a material scope trade-off, or final release authorization. Engineering uncertainty is the agent's investigation responsibility.

## Guardrails

- Do not reduce the product owner to a ticket writer; product presentation and usability are first-class acceptance inputs.
- Do not require the product owner to debug, code, choose ORM mappings, or manually connect architecture layers.
- Do not edit, delete, rename, migrate, or bulk-replace before proving the impacted ownership and reference boundary.
- Do not make a product owner locate code files; trace the route-to-truth chain and report the evidence.
- Do not allow a major project to become an untracked stream of prompts; maintain batches, gates, evidence, and decision points.
- Do not let the AI treat a screenshot, prototype, or competitor reference as complete business semantics.
- Do not put business state, calculations, authorization, or command policy in frontend UI atoms, orchestration, templates, or Hosts.
- Do not let an aggregate interface or Host bypass the command gateway for writes.
- Do not claim owner acceptance from static review; execute the business-flow test.
- Do not let a passed technical gate override a failed product usability or process acceptance.

## Integration

| Need | Primary skill |
|---|---|
| Product plan, batches, and closure | `ai-chief-planner` |
| Competitor and reference evidence | `ai-competitor-analyst` |
| Domain/atomic/aggregate/command architecture | `ai-atomic-architect` |
| Backend truth and client boundaries | `ai-single-truth-enforcer` |
| UI atoms, templates, and Host pages | `ai-component-standardizer` |
| End-to-end business acceptance evidence | `ai-flow-closure-audit` |
| Version and release state | `ai-5s-delivery-governor` |

## Evolution History

- v1.0.0: Extracted from repeated GERP delivery evidence where a non-programmer product owner directed product outcome and business acceptance while AI agents performed full-stack implementation, verification, and governed release closure.
- v1.1.0: Added safe change, code location, and major-project autopilot protocols from GERP dirty-worktree, shared-component, route-tracing, and evidence-gated delivery practice.
