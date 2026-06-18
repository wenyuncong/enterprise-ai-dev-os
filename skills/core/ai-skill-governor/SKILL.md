---
name: ai-skill-governor
description: "Audit the health of a skill ecosystem for contradictions, overlap, stale assumptions, missing triggers, orphan skills, quality drift, and maturity gaps. Use for weekly/monthly methodology reviews or after major skill, rule, or project-structure changes."
---

# ai-skill-governor — Skill System Health & Governance Engine

## Purpose | 用途

Proactively audit, deduplicate, and maintain the skill system. Unlike `ai-skill-evolver` (which reacts to completed tasks), this skill performs **scheduled health checks** on the entire skill library — detecting rot, contradictions, redundancy, and effectiveness gaps.

**Problem it solves**: 37 skills (and growing) with no quality control. Skills can:
- Contradict each other (two skills say opposite things)
- Overlap (two skills cover the same ground differently)
- Rot (patterns become outdated, libraries change, best practices evolve)
- Become unused (created but never triggered)
- Lose effectiveness (ratings never updated after initial creation)

---

## Trigger | 触发条件

- **Scheduled**: Every ~20 tasks completed, or weekly (whichever comes first)
- **On-demand**: When user asks "audit skills", "check skill quality", "are skills still good?"
- **Auto**: When a new skill is added (check for conflicts with existing)
- **After major methodology update**: When methodology docs change, verify skills still align

---

## Audit Dimensions | 审计维度

### Dimension 1: Contradiction Detection | 矛盾检测

Skills that say opposite things about the same topic.

**Detection method**:
```
1. Extract all "Guardrails" / "Rules" sections from every skill
2. Group by topic domain (frontend, backend, database, testing, etc.)
3. Flag pairs that make conflicting claims
```

**Example of a contradiction**:
```
ai-single-truth-enforcer: "All validation in backend, never in frontend"
  vs
ai-component-standardizer: "Client-side validation for instant feedback"

→ These need reconciliation: "Client-side for UX feedback only. 
  Backend re-validates everything. Frontend validation is cosmetic, 
  not authoritative."
```

### Dimension 2: Overlap Detection | 重叠检测

Two or more skills covering the same ground with different approaches.

**Detection method**:
```
1. Compare "Purpose | 用途" sections for keyword overlap
2. If > 60% keyword overlap → flag for review
3. Decision: merge, split, or clarify boundaries
```

**Example of overlap**:
```
ai-ui-ux-governor §State Handling: "Loading, Empty, Error, Edge Cases"
  vs
ai-frontend-audit §Error States: "Loading state, empty state, error state"

→ Both cover the same thing. Either merge into one authoritative source,
  or cross-reference with clear ownership.
```

### Dimension 3: Rot Detection | 腐蚀检测

Skills that reference outdated patterns, deprecated libraries, or obsolete practices.

**Detection method**:
```
1. Check last modified date of each SKILL.md
2. Flag skills not updated in > 3 months
3. For each flagged skill, verify:
   - Libraries mentioned: still current versions?
   - Patterns described: still best practice?
   - Guardrails: still enforceable?
```

### Dimension 4: Effectiveness Scoring | 有效性评分

How effective is each skill at preventing real problems?

**Scoring method**:
```
Score = (times_triggered × 0.3) + (problems_prevented × 0.5) + (user_satisfaction × 0.2)

Where:
- times_triggered: How often was this skill loaded?
- problems_prevented: How many issues did it catch before production?
- user_satisfaction: Did the skill's guidance lead to good outcomes?
```

**Score interpretation**:
| Score | Rating | Action |
|---|---|---|
| 8-10 | Effective | Keep, minor updates only |
| 5-7 | Needs improvement | Review guardrails, strengthen weak areas |
| 2-4 | Weak | Major rewrite or split into multiple focused skills |
| 0-1 | Ineffective | Archive or completely rewrite |

### Dimension 5: Orphan Detection | 孤儿检测

Skills that exist but are never triggered.

**Detection method**:
```
1. Track which skills ai-rule-dispatcher routes to
2. Skills not routed to in last 50 tasks → flag
3. Reason: never needed, or dispatcher doesn't know about it?
```

---

## Audit Output | 审计输出

```markdown
## Skill Governance Audit — [YYYY-MM-DD]

### Health Summary
| Metric | Value |
|---|---|
| Total skills | 37 |
| Contradictions found | [N] |
| Overlaps found | [N] |
| Rotting skills (>3 months) | [N] |
| Orphan skills (never used) | [N] |
| Average effectiveness score | [N.N] |

### Contradictions
| Skill A | Skill B | Conflict | Resolution |
|---|---|---|---|
| ai-single-truth-enforcer | ai-component-standardizer | Validation location | Clarified: client-side = cosmetic only |

### Overlaps
| Skills | Overlap % | Recommendation |
|---|---|---|
| ai-ui-ux-governor + ai-frontend-audit | 35% on state handling | Cross-reference, don't merge |
| ai-architect-governor + ai-atomic-architect | 25% on architecture | Clarify: governor = decisions, atomic = patterns |

### Rotting Skills
| Skill | Last Updated | Issues Found | Action |
|---|---|---|---|
| ai-competitor-analyst | 2026-03-15 | Benchmark framework still valid | Minor update: add AI tools to research methods |

### Effectiveness Ratings
| Skill | Score | Rating |
|---|---|---|
| ai-single-truth-enforcer | 8.5 | Effective |
| ai-component-standardizer | 7.2 | Needs improvement |
| ... | ... | ... |

### Recommendations
1. [Action item 1]
2. [Action item 2]
```

---

## Governance Cycle | 治理周期

```
WEEKLY (Light Audit):
  - Quick scan for new contradictions (compare new/modified skills)
  - Orphan detection
  - ~10 minutes

MONTHLY (Full Audit):
  - All 5 dimensions
  - Effectiveness re-scoring
  - Rot detection with library version checks
  - ~30 minutes

POST-MAJOR-UPDATE (Triggered):
  - After methodology doc changes → verify skill alignment
  - After adding 3+ new skills → contradiction scan
```

---

## Auto-Fix Rules | 自动修复规则

Some issues can be auto-fixed without human review:

| Issue | Auto-Fix |
|---|---|
| Skill references outdated skill name | Update reference (e.g., "ai-frontend-availability-audit" → "ai-frontend-audit") |
| Missing "Evolution History" section | Add template section |
| SKILL.md > 500 lines | Flag for splitting (no auto-split) |
| Two skills with identical Purpose line | Flag for merge review |

---

## Integration | 集成

| Skill | Relationship |
|---|---|
| `ai-skill-evolver` | Governor triggers evolver for specific skill updates |
| `ai-rule-dispatcher` | Governor provides updated effectiveness scores for routing |
| `ai-chief-planner` | Governor audit results feed into methodology improvement plans |
| All skills | Governor is the quality control layer above all skills |

---

## Guardrails | 防护规则

- **Audit on a schedule, not just on demand** — rot happens silently
- **Contradictions are bugs** — two skills saying opposite things is a system defect
- **Effectiveness is measured by outcomes, not intentions** — a skill that "should work" but doesn't prevent problems is ineffective
- **Orphan skills are waste** — if nobody uses it, archive it
- **Don't auto-merge skills** — overlap detection flags for human review, never auto-merges

## Maturity | 成熟度

**Stage**: New — Created to fill the proactive governance gap in the skill ecosystem.

## Evolution History | 进化记录

- v1.0.0: Initial creation — 5 audit dimensions, weekly/monthly cycles, auto-fix rules
