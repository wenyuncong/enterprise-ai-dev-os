---
name: ai-chief-planner
description: "Plan end-to-end project execution, task lines, batch sequencing, acceptance criteria, evidence requirements, blockers, and closure state. Use for project-level coordination, multi-step delivery, task backlog governance, and final closure planning."
---

# ai-chief-planner — End-to-End Project Planning & Closure Engine

## Purpose | 用途

Orchestrate project tasks across the full lifecycle:

- Planning: scope definition, task breakdown, dependency mapping
- Scheduling: priority ordering, resource allocation, milestone setting
- Tracking: progress monitoring, blocker identification, status reporting
- Closure: verification, documentation writeback, evidence collection
- Research: competitor benchmarks, technology evaluations, market analysis

This skill is for **project-level orchestration**, not single-task execution.

---

## Core Principles | 核心原则

1. **Check-before-execute**: Verify database, code, and configuration before making decisions.
2. **Root cause, not patches**: Find and fix root causes; avoid temporary workarounds that create technical debt.
3. **Evidence-driven**: Every conclusion must have proof (log, API response, SQL result, screenshot).
4. **Closed loop**: Plan → Execute → Verify → Document → Re-check.
5. **Non-duplication**: Always check existing task packs and execution logs to avoid repeating work.
6. **Function-first**: Prioritize real functional closure before proposing non-essential features.
7. **Single source of truth**: For data-centric modules, one authoritative page/API per concept.
8. **Boundary awareness**: Distinguish between different application contexts (web, mobile, API, admin).

---

## Planning Workflow | 规划工作流

### Phase 1: Discovery
- Understand the request scope and constraints
- Identify stakeholders and affected domains
- Check existing documentation and previous decisions
- Run preliminary environment verification

### Phase 2: Task Decomposition
- Break down work into executable batches (delegate to `ai-task-decomposer`)
- Mark dependencies between batches
- Estimate effort and identify risks
- Assign priorities (P0/P1/P2)

### Phase 3: Scheduling
- Order batches by dependency and priority
- Identify parallelizable work streams
- Set milestones and checkpoints
- Allocate resources and timeboxes

### Phase 4: Execution Tracking
- Monitor batch completion status
- Identify blockers and escalate as needed
- Update progress in master control documents
- Adjust schedule based on findings

### Phase 5: Closure Verification
- Run acceptance criteria against each batch
- Collect evidence (API responses, screenshots, logs)
- Update documentation with findings
- Feed improvements back to `ai-skill-evolver`

---

## Task Status Model | 任务状态模型

| Status | Meaning | Next Action |
|---|---|---|
| `backlog` | Identified but not yet scheduled | Move to `planned` when prioritized |
| `planned` | Scheduled with dependencies mapped | Move to `in_progress` when unblocked |
| `in_progress` | Currently being executed | Complete and move to `review` |
| `review` | Execution complete, awaiting verification | Move to `verified` or back to `in_progress` |
| `verified` | Acceptance criteria passed | Move to `closed` |
| `closed` | Evidence collected, docs updated | Archive |
| `blocked` | Cannot proceed due to dependency/issue | Escalate, resolve blocker |

---

## Closure Checklist | 收尾检查清单

Before marking any task batch as closed, verify:

- [ ] All acceptance criteria passed
- [ ] Evidence collected (screenshots, API logs, SQL results)
- [ ] Documentation updated (relevant docs reflect the change)
- [ ] Working tree clean (only current task files staged)
- [ ] Related skills updated if patterns emerged
- [ ] Next batch unblocked if this was a dependency

---

## Scheduling Patterns | 调度模式

| Pattern | When to Use |
|---|---|
| **Sequential** | Batches have strict dependency order |
| **Parallel** | Independent batches, different domains/files |
| **Staggered** | Overlapping work with synchronization points |
| **Wave-based** | Group related batches into development waves |

---

## Guardrails | 防护规则

- Do not start execution without verifying current state
- Do not skip closure verification — unverified work is not "done"
- Do not duplicate work — check existing task packs first
- Do not plan beyond available information — break into discovery + execution phases
- Do not ignore blockers — escalate rather than work around

## Maturity | 成熟度

**Stage**: Effective — Extracted from enterprise ERP project planning with 12+ core planning principles.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-chief-planner (10KB original)
- v1.1.0: Generalized with universal project planning patterns
