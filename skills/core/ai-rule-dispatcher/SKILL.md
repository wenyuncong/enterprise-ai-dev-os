---
name: ai-rule-dispatcher
description: "Route tasks to the correct methodology rules, skills, first checks, source documents, and safe execution order. Use at the start of each non-trivial task, especially when a request spans frontend, backend, data, deployment, governance, or documentation."
---

# ai-rule-dispatcher — Intelligent Task Routing Engine

## Purpose | 用途

Before any AI agent executes a task, this skill answers five questions:

1. Which project line does this task belong to? (mainline, governance, audit, research)
2. Which rules and documents must be loaded first?
3. Which skill should lead execution?
4. What factual checks (DB, code, runtime) must happen before writing any code?
5. What is the safe execution order?

This skill is for **routing and first-entry judgment**, not decomposition or implementation.

## Core Rule | 核心规则

**Do not send a task directly to execution when the task line, governing docs, or lead skill are still unclear.**

First route it to the right context, then let other skills take over.

## When to Use | 触发条件

- User request is ambiguous or spans multiple domains
- Task involves both frontend and backend
- Unsure which skill should handle the request
- First interaction in a new session
- User asks "where should I start?"

## Standard Workflow | 标准工作流

### Step 1: Classify the Task Line | 判断任务线

Determine which project line the task belongs to:

| Line | Description | Examples |
|---|---|---|
| mainline | Active development work | Feature development, bug fixes, refactoring |
| governance | Architecture/quality governance | Cross-domain decisions, boundary mapping |
| udit | Quality inspection | Code review, flow closure audit, frontend audit |
| esearch | Investigation & analysis | Competitor research, technology evaluation |
| elease | Deployment & release | CI/CD, deployment scripts, release notes |

### Step 2: Classify the Task Type | 判断任务类型

| Type | Lead Skill |
|---|---|
| Complex/multi-module | i-task-decomposer |
| Architecture/design | i-architect-governor |
| Project planning | i-chief-planner |
| Command execution | i-command-executor |
| Frontend development | {stack}-frontend-dev (e.g., ue) |
| Backend development | {stack}-backend-dev (e.g., java-springboot) |
| Database changes | mysql-best-practices (or equivalent) |
| Quality audit | i-flow-closure-audit or i-frontend-audit |
| Research | i-competitor-analyst or i-market-researcher |
| Skill improvement | i-skill-evolver |

### Step 3: Select First Documents | 选择首要文档

Before execution, identify the authoritative documents:

1. ules/AGENTS.md — Always first
2. ules/project_rules.md — Project-specific rules (if exists)
3. Relevant skill's SKILL.md
4. Relevant docs/ category documents

### Step 4: Define First Factual Checks | 定义前置事实检查

Before writing any code, verify:

| Check Type | Verification Method |
|---|---|
| Database | SHOW TABLES; DESCRIBE table; SELECT COUNT(*) |
| Code existence | File path check, grep for patterns |
| Runtime status | Port check, process list, health endpoint |
| Config | Read config files, env vars |
| Docs | Check if existing docs cover this task |

### Step 5: Produce Routing Result | 输出路由结果

`markdown
## Task Routing Result

**Task Line**: [mainline / governance / audit / research / release]
**Lead Skill**: [skill-name]
**Support Skills**: [skill-names]

**First Documents to Read**:
1. [path/to/doc1]
2. [path/to/doc2]

**First Checks to Run**:
1. [check-1]
2. [check-2]

**Recommended Execution Order**:
1. [step-1]
2. [step-2]

**Boundary Warnings**:
- [warning-1]
`


## Mid-Task Re-Enforcement | 任务中强制重读

### Problem: Context Decay
In long sessions (>100 messages), skills loaded at session start may no longer be in active context. The dispatcher must counteract this.

### Re-Enforcement Triggers
The dispatcher should instruct the AI to re-read governance skills at these points:

| Trigger | Re-Read |
|---|---|
| Switching from backend to frontend work | ai-single-truth-enforcer, ai-library-first, ai-component-standardizer |
| After 50+ messages in same domain | Relevant governance skills for that domain |
| Before writing code to a new file | Domain governance skills |
| Before marking any task "complete" | ai-runtime-verify, ai-single-truth-enforcer |
| After a tool error or unexpected result | ai-tool-bootstrapper, relevant tech skill |

### Re-Enforcement Command
When a trigger fires, the dispatcher outputs:

```
⚠️ Context Decay Warning: >50 messages since last governance re-read.
Re-reading: ai-single-truth-enforcer, ai-library-first
```

---

## Guardrails | 防护规则

- Do not skip check-before-execute
- Do not recommend multiple lead skills — pick ONE
- Do not route to implementation if entry facts are still missing
- Do not treat governance support lines as the active mainline
- If unsure, escalate to i-chief-planner for scheduling decision

## Maturity | 成熟度

**Stage**: ffective — Battle-tested on GERP ERP project across 2000+ task dispatches.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-rule-dispatcher, generalized for universal use
- Source: GERP Enterprise ERP, 3+ months of daily dispatches
