# AI-Native Methodology Routing Map

## 1. Authoritative rule layer

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/rules/AGENTS.md`

These two define check-before-execute, execution boundaries, restart timing, and project-wide constraints.

## 2. Current line hierarchy

### 2.1 Current enterprise mainline

Freeze the current execution line through:

- `{PROJECT_ROOT}/docs/全项目总控/TASK_BACKLOG.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- the current task pack under `{PROJECT_ROOT}/docs/业务流程全案/`

Current order:

1. classify the task
2. load the required rules and skills
3. verify current state
4. decompose work into batches
5. execute through existing tools or scripts
6. verify runtime / tests
7. write back evidence and evolution notes

### 2.2 Support and special lines

- governance support line -> methodology, rules, skills, audit scripts
- product-completion line -> documentation, launch kit, packaging, evidence
- runtime support line -> environment, tools, build, deploy, verification
- domain implementation line -> database, backend, frontend, integration

## 3. Primary document routing

| Task type | First documents |
| --- | --- |
| Whole-project governance / planning | `docs/全项目总控/MASTER_INDEX.md` + `docs/全项目总控/TASK_BACKLOG.md` |
| Current enterprise execution line | current task pack under `docs/业务流程全案/` |
| Local execution pack under business flow | relevant pack under `docs/业务流程全案` |
| Command / runtime / compile | `AGENTS.md` + `scripts/` |
| Product-design pre-freeze | relevant ADR under `docs/架构决策记录/` |
| Competitor / market | existing `竞品 / 对标 / 调研` docs under `docs/` |

## 4. Lead-skill routing map

| Dominant task type | Lead skill | Common support skill |
| --- | --- | --- |
| total-control planning / dispatch / backfill | `ai-chief-planner` | `ai-task-decomposer` |
| complex task splitting | `ai-task-decomposer` | `ai-chief-planner` |
| command execution / runtime diagnosis | `ai-command-executor` | `ai-rule-dispatcher` |
| route / rule / doc ambiguity | `ai-rule-dispatcher` | `ai-chief-planner` |
| competitor benchmarking | `ai-competitor-analyst` | `ai-reference-researcher` |
| boundary / source-of-truth conflict | `ai-domain-boundary-mapper` | `ai-architect-governor` |
| flow closure audit | `ai-flow-closure-audit` | `ai-chief-planner` |
| frontend availability / usability audit | `ai-frontend-audit` | `ai-ui-ux-governor` |
| UI/UX improvement | `ai-ui-ux-governor` | `ai-frontend-audit` |

## 5. First-check templates

| Situation | First checks |
| --- | --- |
| DB-related | table / field / row-count / schema confirmation |
| Code-related | file existence, route/controller/service search |
| Runtime-related | approved script entry, log path, port, process |
| Doc-related | existing pack, execution record, claim-pool row, master task row |
| Mainline ambiguity | whether the task belongs to current mainline, support line, or special line |

## 6. Required routing output

Every routing answer should provide:

1. task-line judgment
2. lead skill
3. support skills
4. authoritative docs
5. first factual checks
6. safe execution order
7. do-not-cross boundaries
