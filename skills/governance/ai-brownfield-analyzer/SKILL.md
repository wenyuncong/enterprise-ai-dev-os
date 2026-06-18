---
name: ai-brownfield-analyzer
description: "Analyze existing projects before changing them by discovering architecture, scripts, conventions, risks, intervention level, and safe extension points. Use for brownfield codebases, inherited systems, migrations, or unfamiliar repository work."
---

# ai-brownfield-analyzer — Legacy Project Analysis & Pattern Extraction Engine

## Purpose | 用途

Before modifying any existing project, execute a structured audit: analyze the current state, classify the intervention level, extract patterns (good and bad), and produce a surgical modification plan. This skill ensures that the methodology learns FROM the project before imposing ON the project.

**Problem it solves**: AI treats every project like a greenfield canvas. It rewrites code that worked, breaks conventions that existed for good reasons, and imposes patterns that don't fit. Brownfield analysis prevents all of this by forcing the AI to understand before acting.

---

## Trigger | 触发条件

- **ALWAYS** when entering any existing project for the first time
- When the user says "fix this bug in my project", "add a feature to my app", "refactor this module"
- When `ai-project-classifier` returns Origin = Brownfield
- When inheriting semi-finished work from another team
- When the project has no README, no tests, or unclear architecture

---

## Core Rule | 核心规则

**The existing project is the teacher. The methodology is the student.**

```
DO NOT: See messy code → "I'll rewrite this properly"
DO:      See messy code → "What was the original intent? What pattern exists here?"
```

---

## Analysis Workflow | 分析流程


### Step 0: Tool Discovery (BEFORE Quick Scan) | 工具发现

**Before analyzing code, discover what tools already exist.** Existing projects often have hundreds of battle-tested scripts. Don't reinvent them.

```bash
# Discover all scripts in the project
py scripts/py/discover_tools.py {project_path} --by-purpose
```

**Output**: Catalog of all existing scripts, grouped by purpose:
- database/migration, database/check, database/sync, database/seed
- build/compile, service/start, service/stop
- deploy/release, test/api, test/unit
- utility/cleanup, utility/generate

**What this tells you**:
- Which tasks already have automation (don't write new scripts)
- Which tasks are done manually (opportunity to add automation)
- How mature the project's tooling is
- What the project's operational patterns are

**Rule**: If a purpose category has 5+ scripts, the project has established patterns. Match them.

---

### Step 1: Quick Scan (5 minutes)
Get the lay of the land before diving deep.

```bash
# What we're dealing with
ls -la                    # Root structure
git log --oneline -20     # Recent activity
cat package.json          # Dependencies (Node)
cat pom.xml               # Dependencies (Java)
```

**Output**: One-paragraph summary of project type, size, activity level.

### Step 2: Deep Audit (15-30 minutes)
See methodology/09_老项目改造方法论.md Phase 1 for full audit dimensions.

```markdown
## Audit Summary

### Project Profile
- Type: [Web app / API / Mobile / Desktop / Mixed]
- Stack: [Framework + Language + Database]
- Age: [First commit → last commit]
- Team size: [Estimated from commit authors]

### Health Scorecard
| Dimension | Score (1-10) | Evidence |
|---|---|---|
| Code organization | [1-10] | [Brief evidence] |
| Test coverage | [1-10] | [Brief evidence] |
| Documentation | [1-10] | [Brief evidence] |
| Dependency freshness | [1-10] | [Brief evidence] |
| Consistency | [1-10] | [Brief evidence] |
| **OVERALL** | **[1-10]** | |
```

### Step 3: Classify Intervention Level
See methodology/09_老项目改造方法论.md §2.

```
Based on audit + user goal → Level [1-5]
- Level 1 (Quick Fix): [Conditions met?]
- Level 2 (Feature Addition): [Conditions met?]
- Level 3 (Module Upgrade): [Conditions met?]
- Level 4 (Deep Renovation): [Conditions met?]
- Level 5 (Takeover): [Conditions met?]
```

### Step 4: Extract Patterns
See methodology/09_老项目改造方法论.md Phase 3.

**Good patterns → keep and formalize into skills:**
```
Pattern: [Name]
Found in: [Files]
Why good: [Analysis]
Skill to update: [Skill name]
```

**Bad patterns → note for fixing:**
```
Anti-pattern: [Name]
Found in: [Files]
Impact: [What it breaks]
Fix priority: [P0/P1/P2]
```

### Step 5: Produce Modification Plan
See methodology/09_老项目改造方法论.md Phase 4.

```markdown
## Modification Plan

### Intervention: Level [1-5]
### Scope:
- IN: [What we will change]
- OUT: [What we will NOT touch]

### Batches
| # | Task | Risk | Dependencies | Estimate |
|---|---|---|---|---|
| 1 | [Task] | [Low/Med/High] | [None/Deps] | [Time] |

### Safety Measures
- [ ] Database backed up
- [ ] Regression tests pass before starting
- [ ] Feature branch created
- [ ] Rollback plan documented
```

---

## Special Case: Semi-Finished Projects | 半成品项目

### Detection Signals
- "It should work but..." comments throughout code
- README describes features that don't exist
- `TODO` and `FIXME` markers everywhere
- No git history (single "initial commit" or fresh clone)
- Mixed levels of completion (login works perfectly, but dashboard is empty divs)

### Handling Semi-Finished Projects
```
1. DOCUMENT REALITY (not aspirations)
   - "The README says it supports file upload. Actually: route exists, handler is empty."

2. MAP WHAT EXISTS (not what's planned)
   - Working features: [List]
   - Partially working: [List with details]
   - Not implemented: [List]

3. BUILD FINISH ORDER (dependency-first)
   - What must work before what?
   - Not: "What would be cool to have?"

4. SET REALISTIC EXPECTATIONS
   - "This project is 40% complete. The remaining 60% will take X weeks."
```

---


## Special Cases Not to Miss | 容易遗漏的场景

### Missing Original Team | 原始团队不在
- Don't assume intent behind "weird" code
- Git blame is your historian
- Add tests as documentation for the next developer
- Build a bus-factor map: which modules have zero surviving knowledge?

### Data Migration Required | 需要数据迁移
- Audit source data quality BEFORE migration
- Map old→new schema explicitly
- Idempotent scripts + dry-run mode
- Test on data copy, never on live data

### Environment Drift | 环境不一致
- Compare configs across all environments
- Check: dependency versions, runtime versions, DB versions, hard-coded paths
- Standardize: one config template + env overrides

### When to Rebuild | 何时放弃重做
- Weighted score: tests(20%) + deps(15%) + architecture(20%) + team knowledge(15%) + features(20%) + security(10%)
- Score < 2.5 → consider rebuild
- Extract all business rules before rebuilding (they are the real asset)

Full details: methodology/09_老项目改造方法论.md §5b

---

## Pattern Extraction → Skill Evolution | 模式提炼→技能进化

### What Patterns to Extract

| Category | What to Look For | Feeds To |
|---|---|---|
| **Naming** | Consistent class/file/table naming patterns | ai-component-standardizer |
| **Structure** | Module organization, folder hierarchy | ai-atomic-architect, methodology/08 |
| **Error handling** | How errors are caught, logged, returned | ai-single-truth-enforcer |
| **API design** | Endpoint naming, request/response format | Backend tech skills |
| **Component patterns** | How pages are structured (list/form/report) | ai-component-standardizer |
| **Library choices** | What libraries are used and why | ai-library-first |
| **Auth pattern** | How authentication/authorization works | Backend tech skills |
| **Database patterns** | Table naming, indexing, migration strategy | mysql-best-practices |
| **Testing patterns** | How tests are organized, what's tested | Test tech skills |

### Extraction Rules

| Rule | Rationale |
|---|---|
| Extract both good AND bad patterns | Anti-patterns teach what NOT to do |
| One pattern per extraction entry | Keep it focused |
| Cite specific files/lines | Evidence-based, not opinion-based |
| Don't extract from one occurrence | A pattern = at least 3 consistent examples |
| Feed to ai-skill-evolver immediately | Don't batch pattern updates |

---

## Integration | 集成

| Step | Action |
|---|---|
| `ai-project-classifier` | Detects Brownfield → routes to ai-brownfield-analyzer |
| `ai-brownfield-analyzer` | Phase 1-3 (Audit → Classify → Extract) |
| `ai-chief-planner` | Phase 4 (Plan) |
| `ai-task-decomposer` | Phase 5 (Execute batches) |
| `ai-skill-evolver` | Phase 6 (Feed patterns back to skills) |
| `ai-reference-researcher` | Optional: find reference projects for comparison |

---

## Guardrails | 防护规则

- **Audit before you act** — never write code in an unfamiliar project
- **Match existing style, even if ugly** — consistency beats aesthetics
- **Don't fix what isn't broken** — if it works and isn't in scope, leave it
- **Trust running code over documentation** — docs lie, code doesn't
- **One change type per commit** — refactor OR feature, never both
- **Extract patterns, don't impose them** — the project sets the standard
- **Database changes are a separate batch** — never mix DB + code changes
- **Semi-finished ≠ garbage** — document reality, build a finish order

## Maturity | 成熟度

**Stage**: New — Extracted from real brownfield ERP project analysis patterns.

## Evolution History | 进化记录

- v1.0.0: Initial creation — 5-step analysis workflow, 5 intervention levels, pattern extraction, semi-finished project handling
