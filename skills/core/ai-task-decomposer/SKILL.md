---
name: ai-task-decomposer
description: "Break complex work into safe executable batches with dependencies, scope boundaries, acceptance criteria, evidence requirements, and handoff-ready task slices. Use for multi-module tasks, long-running work, parallel execution, or ambiguous implementation requests."
---

# ai-task-decomposer — Complex Task Decomposition Engine

## Purpose | 用途

Convert broad or mixed work into:

- Scope-frozen, independently executable task batches
- current / target / implementation separation
- Dependency-aware ordering with blocker identification
- Acceptance criteria and evidence rules per batch
- Internal-pack vs external-dispatch output decisions

This skill is for **decomposition**, not top-level routing or execution itself.

## Core Rule | 核心规则

**Do not split from imagination.**

Before decomposing, verify enough repo facts to separate:
1. Current-state facts (what exists now)
2. Target-state decisions (what we want)
3. Executable implementation work (how to get there)

## When to Use | 触发条件

- Cross-module or cross-end (frontend + backend + DB) tasks
- Tasks too large for one safe AI session
- Blocked by unclear dependency order
- Intended for parallel dialogs or staged dispatch
- User asks: "break this down", "split this task", "plan this work"

## Check-Before-Execute | 前置检查

Before splitting, verify:
1. Current branch and working tree state
2. Existing task packs, execution records
3. Whether the same topic already has a decomposition pack
4. Hot files or collaboration boundaries
5. Which work is factual check, design, implementation, or acceptance

## Standard Workflow | 标准工作流

### 1. Freeze Scope | 冻结范围

State clearly:
- **In scope**: exact modules, files, domains
- **Out of scope**: explicitly excluded areas
- **Impacted areas**: modules/files/domains affected

### 2. Reuse Existing Artifacts | 复用已有产物

Prefer extending existing decomposition packs over creating parallel ones.

### 3. Separate into Layers | 分层分离

Always distinguish:

| Layer | Description |
|---|---|
| **Current-State Verification** | What to check before starting |
| **Target Design / Decision** | What to decide before building |
| **Implementation Work** | The actual code/doc changes |
| **Verification & Backfill** | How to prove it's done right |

### 4. Build Executable Batches | 构建可执行批次

Each batch must be:
- Independently understandable (can be given to a different agent)
- Small enough for one focused round (~30-60 min of work)
- Clear about ownership and write scope
- Explicit about acceptance and evidence

### 5. Mark Dependencies | 标记依赖

Use blocker-first ordering:
- Type A: Must complete before B can start
- Type B: Can run in parallel with C
- Type C: Should wait for A and B to complete

### 6. Choose Output Form | 选择输出形式

| Form | When to Use |
|---|---|
| **Internal Decomposition Pack** | Single developer, sequential execution |
| **External Dispatch Pack** | Multiple developers/agents, parallel execution |
| **Handoff Block** | Passing to another AI session |

## Required Output Structure | 必需输出结构

`markdown
## Task Decomposition: [Task Name]

### 1. Scope & Verified Inputs
- In scope: [...]
- Out of scope: [...]
- Verified facts: [...]

### 2. Main Blockers & Current Facts
- [blocker-1]
- [blocker-2]

### 3. Current / Target / Implementation Split
| Layer | Status | Details |
|---|---|---|
| Current-State Verification | [pending/complete] | [...] |
| Target Design | [pending/complete] | [...] |
| Implementation | [pending/complete] | [...] |
| Verification | [pending/complete] | [...] |

### 4. Task Batch Table
| ID | Priority | Batch | Dependency | Est. Time | Acceptance |
|---|---|---|---|---|---|
| B-01 | P0 | [...] | None | 30m | [...] |
| B-02 | P1 | [...] | B-01 | 45m | [...] |

### 5. Acceptance & Evidence Rules
- [rule-1]
- [rule-2]

### 6. Output Form
[Internal / External / Handoff]
`

## Guardrails | 防护规则

- Do not output one giant task when work is not atomic
- Do not split so finely that business meaning disappears
- Do not mix current-state check and implementation unless tightly coupled
- Do not ignore hot-file collision risk in parallel work
- Do not decompose without checking existing packs first

## Maturity | 成熟度

**Stage**: ffective — Battle-tested on GERP ERP project across 100+ decompositions.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-task-decomposer, generalized for universal use
- Source: GERP Enterprise ERP, PDCA-driven decomposition template
