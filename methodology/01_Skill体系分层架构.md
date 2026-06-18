# 01 — Skill System Layered Architecture | Skill体系分层架构

> **Part of**: Enterprise-Grade Full AI Development Methodology
> **Prerequisite**: 00_核心方法论白皮书

---

## 1. Why a Layered Architecture? | 为什么需要分层架构？

Single-file AI rules (like .cursorrules) suffer from three fatal flaws:

| Flaw | Description |
|---|---|
| **Flat context** | Everything in one file — AI can't distinguish routing rules from code rules from evolution rules |
| **No delegation** | One big rules file means every task loads all rules, even irrelevant ones |
| **Static** | Rules don't improve — they're written once and rot |

The solution is a **five-layer architecture (Classification → Routing → Decomposition → Execution → Evolution)** where each layer has a distinct responsibility:
## 2. Layer 0: Classification | 分类层

**Skill**: `ai-project-classifier`

### Responsibility
Classify every project at inception across four dimensions:
- **Origin**: Brownfield (existing) vs Greenfield (new)
- **Quality Target**: Rapid Prototype vs AI-Native vs Enterprise
- **Deploy Targets**: Web / Mobile / WeChat / MCP / All platforms
- **Scale**: Monolith vs Atomic Services vs Microservices

### Why It's Separate
Classification happens exactly ONCE at project start (and re-runs on scope change). It determines which skills to load, which architecture to apply, and what "done" means. Without explicit classification, the methodology over-engineers prototypes and under-engineers production systems.

### Key Design Decision
**Default to AI-Native when unclear.** It's easier to downgrade from AI-Native to Rapid Prototype than to upgrade a prototype to production quality later.

---


`
+--------------------------------------------------+
|  LAYER 1: ROUTING                                 |
|  "Which rules, skills, and docs apply to THIS     |
|   specific task?"                                 |
|  Owner: ai-rule-dispatcher                        |
+--------------------------------------------------+
                         |
                         v
+--------------------------------------------------+
|  LAYER 2: DECOMPOSITION                           |
|  "How do we break THIS task into safe,            |
|   executable batches?"                            |
|  Owner: ai-task-decomposer                        |
+--------------------------------------------------+
                         |
                         v
+--------------------------------------------------+
|  LAYER 3: EXECUTION                               |
|  "Write the code. Follow the 13-step order.       |
|   Use the right tech skill."                      |
|  Owners: tech-specific skills (e.g., java-springboot, vue)|
|          mysql-best-practices, etc.               |
+--------------------------------------------------+
                         |
                         v
+--------------------------------------------------+
|  LAYER 4: EVOLUTION                               |
|  "What did we learn? Which skill needs updating?" |
|  Owner: ai-skill-evolver                          |
+--------------------------------------------------+
`

---

## 3. Layer 1: Routing | 路由层

**Skill**: i-rule-dispatcher

### Responsibility
Determine the execution context before any code is written:
- Which project line (mainline, governance, audit, research)?
- Which rules and docs must be loaded first?
- Which skill should lead execution?
- What factual checks must happen first?

### Why It's Separate
Routing is a **meta-concern** — it doesn't write code, it tells other layers what to do. If routing logic is mixed into execution rules, the AI wastes context loading irrelevant instructions.

### Key Design Decision
**One lead skill per task.** Never assign multiple lead skills. Support skills can be loaded as needed, but routing produces exactly one primary execution path.

---

## 4. Layer 2: Decomposition | 分解层

**Skill**: i-task-decomposer

### Responsibility
Convert complex tasks into independent, dependency-aware batches:
- Scope freeze (in/out)
- Current-state verification → target design → implementation → verification
- Batch table with priority, dependency, and acceptance criteria
- Decision: internal pack (single developer) or external dispatch (parallel agents)

### Why It's Separate
Decomposition is a **planning concern** — it produces a plan, not code. Separating it from execution means:
- Plans can be reviewed before code is written
- Batches can be dispatched to different agents
- Failed batches can be re-planned without re-executing all work

---

## 5. Layer 3: Execution | 执行层

**Skills**: Domain-specific core skills (ai-task-decomposer, ai-command-executor, ai-tool-bootstrapper, ai-library-first, ai-architect-governor, ai-atomic-architect, ai-foundation-governor) and governance skills (ai-single-truth-enforcer, ai-component-standardizer, ai-frontend-audit, ai-runtime-verify, ai-ui-ux-governor, ai-flow-closure-audit, ai-domain-boundary-mapper, ai-field-package-governor)

### Responsibility
Execute the batch plan following **mandatory engineering discipline**:
- 13-step development order (enforced)
- Check-before-execute on every step
- Data-driven: DB is the single source of truth
- Verification after every step

### Why It's Separate
Execution skills are **domain-specific** — a Vue developer skill should not contain Docker deployment rules. Each tech skill is self-contained and loadable independently.

### How Skills Are Selected
The dispatcher selects the execution skill based on task type:
- Database changes → mysql-best-practices
- Backend API → java-springboot or equivalent
- Frontend page → ue or equivalent
- Full-stack → sequential dispatch through backend → frontend

---

## 6. Layer 4: Evolution | 进化层

**Skill**: i-skill-evolver

### Responsibility
After task completion, improve the skill system:
- Detect repeated patterns
- Classify gaps (skill update, new skill, rule change, doc only)
- Update SKILL.md files
- Record evolution in archive
- Sync changes to AI tools

### Why It's Separate
Evolution is a **meta-meta concern** — it modifies the very rules that govern execution. Without a dedicated evolution layer, skills stagnate and the methodology decays.

---

## 6. Governance Layer (Horizontal) | 治理层（横向）

In addition to the four vertical layers, there is a **horizontal governance layer** that audits quality across all layers:

| Skill | Audits |
|---|---|
| i-flow-closure-audit | Business chain: page → API → DB → writeback → report |
| i-frontend-audit | Page availability, UI consistency, performance |
| i-domain-boundary-mapper | Object ownership, schema placement, cross-domain chains |
| i-competitor-analyst | Feature gaps vs market leaders |

Governance skills are **triggered periodically** (not on every task) and produce structured audit reports with prioritized fix tasks.

---

## 7. Skill Lifecycle | Skill 生命周期

Every skill passes through maturity stages:

`
declared → callable → effective → in-closure → evolving
`

| Stage | Meaning | Evidence Required |
|---|---|---|
| declared | SKILL.md exists | File exists on disk |
| callable | Can be invoked by name | Successfully loaded by AI |
| ffective | Produces correct results | 5+ successful task completions |
| in-closure | Has acceptance criteria | Evidence rules documented |
| volving | Actively being improved | Evolution history has entries |

The i-skill-evolver tracks and upgrades maturity ratings.

---

## 9. Anti-Patterns | 反模式（不要这样做）

| Anti-Pattern | Why It Fails |
|---|---|
| **One giant rules file** | Context overload, irrelevant rules loaded for every task |
| **Mixing routing and execution** | AI can't distinguish "what to do" from "how to do it" |
| **No evolution layer** | Skills stagnate, methodology decays within weeks |
| **Tech skills that reference other tech skills directly** | Creates circular dependencies, defeats modularity |
| **Governance mixed into execution** | Every task loads audit rules, wasting context |

---

## 10. Design Principles | 设计原则

1. **Separation of Concerns**: Each layer has one job. No overlap.
2. **Progressive Loading**: Only load the skills relevant to the current task
3. **Evidence-Driven**: Every claim must be verifiable
4. **Self-Improving**: The system gets better with every completed task
5. **Tool-Agnostic**: Works with Codex, Cursor, Copilot, or any AI coding tool

---

*Next: [02_自动寻路与任务调度.md] — Deep dive into how ai-rule-dispatcher routes tasks*




