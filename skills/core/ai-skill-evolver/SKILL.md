---
name: ai-skill-evolver
description: "Improve the skill system from concrete evidence by updating existing skills, classifying gaps, recording evolution, and proposing new skill candidates. Use when reviewing skill quality, fixing ineffective skills, or turning repeated task patterns into reusable capability."
---

# ai-skill-evolver — Self-Evolving Skill Engine

## Purpose | 用途

Turn repeated work into stronger reusable assets:

- Skill updates (improve existing SKILL.md)
- New skill candidates (create new skills when patterns repeat)
- Archive updates (record evolution history)
- Project skill docs (update project-specific documentation)
- Evolution logs (track what changed and why)

This skill is for **capability evolution**, not ordinary task execution.

## Core Rule | 核心规则

**Do not evolve skills from vague impressions. Only evolve from concrete evidence.**

Evidence sources:
- Repeated task patterns across modules
- Repeated mistakes or missing-context moments
- Stable output templates that should be formalized
- Project path / rule changes
- User feedback that a skill is not actually effective

Always distinguish:
- declared skill (exists on disk)
- callable skill (can be invoked by name)
- ffective skill (produces correct results consistently)
- volving skill (actively being improved)

## When to Use | 触发条件

- After completing a batch of related tasks
- When a pattern repeats 3+ times across different modules
- User asks: "improve the skills", "what skills are missing", "why didn't the skill work"
- After significant project structure changes
- During regular methodology health checks

## Continuous Repair-To-Skill Loop | 持续修复-技能循环

After every implementation round:

1. **Finish** the concrete code/doc task first
2. **Identify** whether the task exposed a reusable rule, repeated defect, or missing pattern
3. **Classify** — does this belong to an existing skill or need a new one?
4. **Update** the relevant SKILL.md (extend, don't replace)
5. **Record** the evolution in the skill archive
6. **Sync** to the active AI tool if needed

## Standard Workflow | 标准工作流

### Step 1: Gather Evidence | 收集证据

Read the current skill governance chain:
- All existing SKILL.md files
- Recent task logs and execution records
- User feedback from completed tasks
- Documentation writebacks

### Step 2: Classify the Gap | 分类差距

| Gap Type | Action |
|---|---|
| Existing skill needs refinement | Update SKILL.md |
| New pattern crosses 2+ task types | Create new skill |
| Single-page issue | Record in task doc, not skill |
| Rule needs updating | Update ules/AGENTS.md |
| Skill exists but not effective | Investigate and fix root cause |

### Step 3: Choose the Right Action | 选择正确动作

Possible actions:
- Update SKILL.md (add new section, extend references)
- Update reference files
- Add or update project-specific docs
- Update skill archive table
- Create a new governance task

### Step 4: Record the Evolution | 记录进化

Always record:
- What triggered the change
- Current maturity stage
- What was updated (file path + line range)
- What remains missing
- Whether a real skill asset was changed or only docs

### Step 5: Feed the Next Round | 反馈下一轮

Convert evolution result into:
- New task IDs for skill improvement
- Updated templates for future use
- Clearer routing rules
- Next-batch skill backlog

## Maturity Rating System | 成熟度评级

| Stage | Meaning |
|---|---|
| declared | SKILL.md exists but never used |
| callable | Can be invoked by name, basic instructions work |
| ffective | Produces correct results consistently |
| in-closure | Has acceptance criteria and evidence rules |
| volving | Actively being improved based on feedback |


## Scheduled Governance Trigger | 定期治理触发

### When to trigger ai-skill-governor

| Trigger | Action |
|---|---|
| Every ~20 completed tasks | Run full ai-skill-governor audit |
| Weekly (regardless of task count) | Light audit (contradictions + orphans) |
| Monthly | Full audit (all 5 dimensions) |
| After adding 3+ new skills | Contradiction scan against existing skills |
| After methodology doc update | Verify skill alignment with updated docs |

### Auto-Trigger
ai-skill-evolver should automatically invoke ai-skill-governor when it detects:
- 2+ skills with overlapping Purpose lines
- A skill not updated in > 3 months
- A skill that was loaded 0 times in the last 50 tasks

---

## Guardrails | 防护规则

- Do not create a new skill when a template or existing skill update is enough
- Do not evolve a skill without concrete repeated evidence (minimum 3 occurrences)
- Do not forget to update both the skill file AND the archive
- Do not claim a skill has evolved if no formal asset was updated
- Do not stop at naming a gap — convert it into a concrete update or task

## Maturity | 成熟度

**Stage**: ffective — Battle-tested on GERP ERP with documented evolution cycles.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-skill-evolver, generalized for universal use
- Source: GERP Enterprise ERP, Continuous Repair-To-Skill loop validated
