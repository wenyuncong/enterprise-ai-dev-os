# 05 — Skill Auto-Evolution Mechanism | Skill自动进化机制

> **Part of**: Enterprise-Grade Full AI Development Methodology
> **Prerequisites**: 00_核心方法论白皮书, 01_Skill体系分层架构

---

## 1. The Problem with Static Rules | 静态规则的问题

Most AI coding rules (.cursorrules, AGENTS.md) are written once and never updated. This causes:

| Problem | Consequence |
|---|---|
| **Rule rot** | Rules reference deleted files, renamed modules, obsolete patterns |
| **Missing context** | New patterns emerge but rules don't capture them |
| **False confidence** | AI trusts outdated rules, makes wrong decisions |
| **No improvement** | The same mistakes repeat because rules never learn |

---

## 2. The Evolution Loop | 进化循环

`
+-----------------------+
|                       |
|  1. TASK COMPLETED    |
|                       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|                       |
|  2. EVIDENCE GATHERING |
|  - Repeated patterns? |
|  - Repeated mistakes? |
|  - Missing context?   |
|                       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|                       |
|  3. GAP CLASSIFICATION |
|  - Update skill?     |
|  - New skill?        |
|  - Rule change?      |
|  - Doc only?         |
|                       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|                       |
|  4. EXECUTE UPDATE   |
|  - Modify SKILL.md   |
|  - Update archive    |
|  - Sync to AI tool   |
|                       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|                       |
|  5. NEXT TASK BENEFITS|
|  - Loads updated skill|
|  - Avoids past mistakes|
|                       |
+-----------------------+
`

---

## 3. Evolution Triggers | 进化触发条件

The evolver activates when:

### Trigger 1: Repeated Pattern (3+ occurrences)
`
Pattern: "Every time we add a new report page, we forget to add the permission entry"
Evidence: 3 completed tasks all had a follow-up permission fix
Action: Add "permission check" to the report development workflow
Target skill: The tech skill used for report development
`

### Trigger 2: Repeated Mistake (2+ occurrences)
`
Mistake: "AI generates frontend code referencing API endpoints that don't exist yet"
Evidence: 2 tasks had to redo frontend work after backend API changed
Action: Enforce Step 5 (Controller) before Step 7 (Frontend TS)
Target: rules/AGENTS.md — Update 13-step enforcement
`

### Trigger 3: Missing Context
`
Symptom: "AI doesn't know about the custom pagination wrapper"
Evidence: AI tried to use standard pagination, broke the custom implementation
Action: Add pagination pattern to the relevant tech skill
Target: vue/SKILL.md or equivalent
`

### Trigger 4: Structural Change
`
Change: Project moved from microservices to monolith
Evidence: Old skill references microservice patterns that no longer exist
Action: Update all skills that reference deployment/service architecture
Target: Multiple skills
`

### Trigger 5: User Feedback
`
Feedback: "The skill tells me to use X but the project actually uses Y"
Action: Investigate, update skill if feedback is correct
Target: The skill that was mentioned
`

---

## 4. Gap Classification Decision Tree | 差距分类决策树

`
Finding detected
    |
    v
Is this a one-off note? ── YES ──> Record in task doc only. Skip evolution.
    |
    NO
    |
    v
Does an existing skill already cover this pattern? ── YES ──> Update that SKILL.md
    |
    NO
    |
    v
Does this pattern cross 2+ task types? ── YES ──> Create new skill
    |
    NO
    |
    v
Is this a project-wide rule? ── YES ──> Update rules/AGENTS.md
    |
    NO
    |
    v
Template or reference update is enough ──> Update relevant reference file
`

---

## 5. Evolution Record Format | 进化记录格式

Every evolution must be recorded at the bottom of the affected SKILL.md:

`markdown
## Evolution History | 进化记录

- v1.0.1 (2026-06-18): Added pagination pattern after 3 tasks used custom pagination
- v1.0.0 (2026-06-17): Initial extraction from GERP project
`

The skill archive (docs/_templates/全项目总控/MASTER_INDEX.md) tracks all skills:

`markdown
## Skill Maturity Matrix — 2026-06-17

| Skill | Stage | Last Evolved | Evolution Count | Next Review |
|---|---|---|---|---|
| ai-rule-dispatcher | effective | 2026-06-17 | 1 | 2026-07-17 |
| ai-task-decomposer | effective | 2026-06-17 | 1 | 2026-07-17 |
| vue | evolving | 2026-06-16 | 3 | 2026-06-30 |
`

---

## 6. Evolution Anti-Patterns | 进化反模式

| Anti-Pattern | Why It Fails |
|---|---|
| **Evolving without evidence** | Creates rules based on speculation, not reality |
| **Creating skills for single-use patterns** | Proliferates useless skills, clogs the system |
| **Evolving too frequently** | Churn makes skills unstable, AI can't keep up |
| **Evolving too rarely** | Skills rot, methodology decays |
| **Not recording evolution** | No audit trail, can't track what changed or why |
| **Evolving only docs, not skills** | Documents improve but AI behavior doesn't change |

---

## 7. Evolution Cadence | 进化节奏

| Frequency | Action |
|---|---|
| **After every task** | Check for evolution triggers |
| **Weekly** | Review skill maturity matrix |
| **Monthly** | Full skill audit — remove unused, merge overlapping, upgrade mature |
| **Per release** | Version-lock all skills, record baseline |

---

*Next: [06_企业级部署与验收标准.md] — Deployment gates and acceptance criteria*

