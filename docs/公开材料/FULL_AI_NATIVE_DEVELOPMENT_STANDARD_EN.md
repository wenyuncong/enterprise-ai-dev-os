# Full AI-Native Development Standard

> Version: Draft 1.1
> Date: 2026-08-09
> Scope: AI-assisted software delivery, enterprise business systems, project runtime governance, agent capability governance, and multi-surface business capability reuse.
> Disclosure boundary: this is a standard explanation document. It does not include private repository paths, customer data, unredacted evidence, or unverified benefit metrics.

## 0. Standard Positioning

Full AI-Native Development Standard defines a new software engineering structure. It makes software systems understandable, callable, governable, verifiable, and evolvable by AI from the beginning.

It is not a specific development tool, model, framework, or prompt method. It is a structural standard across tools, languages, and business systems.

The goals are:

1. Humans express goals, boundaries, and acceptance in business language.
2. AI analyzes, implements, tests, and delivers inside an understandable structure.
3. The target project's backend/runtime manages truth, permission, state, evidence, and risk; this repository supplies the methodology and gates.
4. Repeated issues become rules, skills, scripts, atoms, tests, or governance policies.

## 1. Normative Terms

This document uses the following terms:

- MUST: required for conformance.
- SHOULD: recommended by default unless a justified exception exists.
- MAY: allowed but not required.
- MUST NOT: prohibited.

## 2. Overall Structure

The main collaboration chain is:

```text
human intent
-> explanation layer
-> standard layer
-> AI amplification layer
-> runtime governance
-> evidence verification
-> human acceptance
-> evolution writeback
```

The engineering chain is:

```text
truth
-> atomic service
-> orchestration
-> aggregate interface
-> command gateway
-> registry
-> adapters
-> Host / AI / MCP / OpenAPI
-> evidence
-> evolution
```

These two chains solve different problems:

- The collaboration chain defines the division of responsibility among humans, AI, runtime, and evidence.
- The engineering chain defines how business capabilities are standardized, invoked, governed, and reused.

## 3. Standard Object Definitions

### 3.1 Human Intent

Human intent is the source of product goals, business outcomes, user experience, priorities, non-goals, and final acceptance criteria.

Requirements:

- Humans MUST own final business judgment.
- AI MAY draft requirements but MUST NOT replace humans in defining business policy.
- When business meaning is unclear, AI SHOULD ask for the smallest necessary clarification.

### 3.2 Explanation Layer

The explanation layer converts natural language, screenshots, examples, and acceptance descriptions into executable tasks, scenarios, boundaries, and risks.

Requirements:

- It MUST record business goals, inputs, outputs, non-goals, and acceptance methods.
- It SHOULD convert vague descriptions into verifiable statements.
- It MUST NOT push engineering uncertainty back to the business owner as code-search work.

### 3.3 Source of Truth

The source of truth is the authoritative source for business facts, fields, permissions, state, and data ownership.

Requirements:

- Every business fact MUST have one authoritative owner.
- Fields, permissions, state, amounts, inventory, approval, and writeback MUST NOT be recalculated independently in multiple clients.
- Frontend, AI clients, MCP clients, and OpenAPI clients MUST consume truth instead of creating a second truth.

### 3.4 Atomic Service

An atomic service is the smallest independently understandable, testable, governable, and replaceable stable business capability unit. It should have clear input, output, permission, error, evidence, and test boundaries.

Requirements:

- An atomic service MUST have a single responsibility.
- An atomic service MUST be independently testable.
- An atomic service MUST NOT depend on a Host page for business judgment.
- An atomic service MAY be reused by multiple orchestration flows, aggregate interfaces, or adapters.
- Atomicity is a capability boundary, not a mandatory deployment boundary.
- An atomic service MAY run in a modular monolith, service cluster, or edge runtime. Deployment and data isolation are chosen from performance, organization, isolation, and operational-cost needs.

### 3.5 Atomic Orchestration

Atomic orchestration composes atomic services into business workflows such as save, approve, push-down, post, rollback, notify, and release.

Requirements:

- Multi-step business workflows MUST be expressed through orchestration, not scattered in clients or pages.
- Orchestration MUST handle transaction boundaries, failure rollback, compensation, idempotency, and evidence.
- Orchestration MUST NOT bypass atomic services to manipulate multiple business facts directly.

### 3.6 Aggregate Interface

An aggregate interface is a capability profile for Host, AI, MCP, and OpenAPI. It returns not only data, but also fields, state, actions, permissions, prompts, risks, and executable boundaries.

Requirements:

- An aggregate interface MUST be centered around a business object or workflow.
- It SHOULD return displayable facts and executable capabilities needed by clients.
- It MUST NOT bypass the command gateway to perform write actions.
- It SHOULD allow AI to understand what can be done, what cannot be done, and why.

### 3.7 Command Gateway

The command gateway is the only action entrance. Any action that changes business state, data, permissions, files, releases, or external systems must pass through the command gateway or an equivalent governed entrance.

Requirements:

- Write actions MUST pass through the command gateway.
- The command gateway MUST check permission, state, idempotency, risk, audit, and evidence policy.
- The command gateway MUST return clear failure reasons.
- High-risk actions MUST support human confirmation, dry-run, rollback, or compensation mechanisms.

### 3.8 Registry

The registry records capabilities, versions, status, providers, permissions, adapters, risk levels, and invocation boundaries.

Requirements:

- Callable capabilities MUST be registered.
- Capability status MUST be explicit, such as draft, supported, deferred, blocked, deprecated, or retired.
- The registry MUST distinguish "exists" from "executable".
- AI and Hosts SHOULD read the registry instead of guessing capabilities.

### 3.9 Host

A Host is a Web, App, desktop, AI console, MCP client, or OpenAPI surface.

Requirements:

- A Host loads, renders, collects input, requests commands, and displays feedback.
- A Host MUST NOT define a second business state machine.
- A Host MUST NOT recalculate business amounts, inventory, permissions, or approval state.
- A Host SHOULD use standard templates and UI atoms instead of page-local logic.

### 3.10 Runtime

The runtime is a target-project architecture component that may execute the adopted standard. It manages truth, uniqueness, memory, learning, state, permission, evidence, risk, and evolution. This repository does not include a universal runtime implementation.

Requirements:

- Runtime MUST maintain execution state and evidence.
- Runtime MUST make capability invocation traceable.
- Runtime SHOULD support rule loading, skill routing, registry lookup, command execution, evidence recording, and risk judgment.
- Runtime MUST NOT replace final human business acceptance.

### 3.11 Evidence Loop

The evidence loop turns task results into reviewable facts.

Requirements:

- Task completion MUST include evidence.
- Evidence MAY come from tests, builds, APIs, browsers, logs, database checks, screenshots, audit scripts, or business-flow replay.
- Evidence MUST describe scope and limitations.
- "Code has been written" MUST NOT replace "result has been verified".

### 3.12 Evolution Writeback

Evolution writeback converts repeated issues, effective patterns, and failures into long-term assets.

Requirements:

- Repeated issues SHOULD become rules, skills, scripts, tests, templates, or governance policies.
- Experience writeback MUST be traceable.
- Evolution MUST NOT directly modify core capabilities without governance.
- Learning results SHOULD become candidate assets first and be promoted only after verification.

### 3.13 Candidate Capability Evaluation and Verification

Web pages, skills, code snippets, tool output, model suggestions, third-party libraries, and existing project assets may enter a candidate pool. They are not accepted or rejected solely because a source is labeled "trusted" or "untrusted". They are inputs awaiting evaluation.

Requirements:

- Candidate assets MUST describe the problem to solve, scope, project context, dependencies, and potential impact.
- Evaluation MUST cover outcome fit, architecture fit, domain-rule fit, data boundary, operational cost, verifiability, and rollback path.
- Source, author, signature, historical behavior, and citations MAY be used as evidence, but MUST NOT replace project-local validation.
- Unevaluated or unverified candidates MUST NOT be promoted directly to official rules, official skills, executable commands, or production capabilities.
- Evaluation outcomes MUST produce traceable decisions, evidence, and stated limitations.

Core principle:

```text
Source is not a conclusion.
Trust is only one evaluation input.
Project fit, verifiability, and reversibility determine admission.
```

## 4. Standard Requirements

| ID | Requirement |
|---|---|
| AI-NATIVE-01 | The system MUST define business truth owners |
| AI-NATIVE-02 | Frontends and clients MUST NOT become business truth owners |
| AI-NATIVE-03 | Reusable business capabilities MUST be atomic |
| AI-NATIVE-04 | Multi-step workflows MUST be expressed through orchestration |
| AI-NATIVE-05 | Hosts, AI, MCP, and OpenAPI SHOULD share aggregate interfaces |
| AI-NATIVE-06 | Write actions MUST pass through command gateways |
| AI-NATIVE-07 | Callable capabilities MUST be registered |
| AI-NATIVE-08 | Runtime MUST record state, permission, risk, and evidence |
| AI-NATIVE-09 | Task completion MUST include reviewable evidence |
| AI-NATIVE-10 | Repeated issues MUST enter an evolution writeback mechanism |
| AI-NATIVE-11 | High-risk actions MUST support confirmation, dry-run, rollback, or compensation |
| AI-NATIVE-12 | Public materials MUST be desensitized and avoid private paths, customer data, or unverified metrics |
| AI-NATIVE-13 | External and internal candidate assets MUST pass fit evaluation and controlled verification before promotion |
| AI-NATIVE-14 | Agent execution MUST have traceable identity, delegated authorization, and scope boundaries |
| AI-NATIVE-15 | Critical execution MUST produce reproducible evidence artifacts that record versions, inputs, decisions, and results |

## 5. Maturity Model

| Level | Description | Typical State |
|---|---|---|
| S0 | AI-assisted coding | AI writes code, but project rules are unstable |
| S1 | Rule-based delivery | Project rules, directory boundaries, development order, and basic verification exist |
| S2 | Skill-based delivery | Recurring tasks become skills, templates, and scripts |
| S3 | Architecture-native | Truth owners, atomic services, orchestration, aggregate interfaces, command gateways, and Hosts exist |
| S4 | Runtime-governed | A project runtime manages permission, state, risk, evidence, and multi-surface invocation |
| S5 | Evolvable system | Repeated issues become rules, atoms, tests, and governance policies automatically or semi-automatically |

## 6. Acceptance Gates

| Gate | Definition |
|---|---|
| G0 Static consistency | Files, directories, rules, references, and registry declarations are consistent |
| G1 Build consistency | Backend, frontend, scripts, or model packages pass basic build checks |
| G2 Interface consistency | APIs, aggregate interfaces, command gateways, permissions, and response shapes are verified |
| G3 Runtime consistency | Browser, API, logs, database checks, or business-flow replay prove real runtime behavior |
| G4 Release consistency | Version, tag, migration, rollback, deployment evidence, and disclosure boundaries are complete |

## 7. Typical Flow

```text
business goal
-> explain into scenario, boundary, and acceptance
-> locate truth owner and existing capabilities
-> evaluate references, skills, and tool output as candidate capabilities
-> select or add atomic services
-> orchestrate workflow
-> expose aggregate interface
-> register callable capability
-> execute through command gateway
-> Host / AI / MCP renders or invokes
-> verify runtime
-> write back documents and skills
```

## 8. Anti-Patterns

| Anti-Pattern | Why It Is Dangerous |
|---|---|
| Frontend calculates business facts | Multi-surface inconsistency and unclear truth |
| Page directly writes state | Bypasses permission, audit, rollback, and state machine |
| Calling unregistered capabilities | AI and Hosts can only guess capability boundaries |
| Writing code without verification | Cannot prove the result works |
| Treating chat history as long-term knowledge | Future sessions cannot inherit it reliably |
| Patching repeated issues only once | The system does not evolve and errors repeat |
| Publishing unredacted materials | Leaks paths, customers, evidence, or strategy boundaries |
| Replacing evidence with large numbers | External readers cannot verify the claim and trust decreases |
| Accepting or rejecting a capability only by source label | Ignores project fit, architecture impact, and verifiability |

## 9. Minimum Adoption Checklist

A project reaches the minimum usable state when it has at least:

- Project rule entry.
- Task classification and routing rules.
- Source-of-truth description.
- Atomic services or equivalent business capability boundaries.
- Aggregate interfaces or equivalent capability profiles.
- Command gateway or equivalent governed write entrance.
- Registry or capability catalog.
- Host boundary description.
- Tests, scripts, or runtime evidence.
- Documentation writeback and experience capture.
- Candidate capability evaluation, verification, and promotion records.
- Agent identity, delegated authorization, and execution evidence boundaries.
- Public/private disclosure boundary.

## 10. External Explanation Template

```text
Our definition of Full AI-Native Development is not replacing all developers with AI.
It is designing software systems to be understandable, callable, governable, verifiable, and evolvable by AI.

Humans own business goals and final acceptance.
AI implements and creates under the standard.
Runtime owns truth, permission, state, evidence, and risk.

This allows AI-generated capabilities to enter real business systems instead of remaining one-off code generation.
```

## 11. Conclusion

The key to Full AI-Native Development is not "stronger AI", but "clearer standards". The clearer the standard, the larger the space for AI to act. The stronger the evidence, the more the system can evolve. The more stable the runtime, the safer AI can enter real business.

The final goal is not to replace humans. It is to free humans from repetitive engineering details and let them focus on ideas, business outcomes, taste, trade-offs, and acceptance.
