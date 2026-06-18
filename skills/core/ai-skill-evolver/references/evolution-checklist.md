# Skill Evolution Checklist

## Evidence sources

Read the current methodology skill-governance chain first:

- `AGENTS.md`
- `rules/AGENTS.md`
- `skills/SKILL_MANIFEST.json`
- `docs/全项目总控/MASTER_INDEX.md`
- `docs/全项目总控/TASK_BACKLOG.md`
- `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- current task log, test report, audit output, and approved private source material

## Decision tree

1. Is the pattern repeated?
   - no -> record as observation
   - yes -> continue
2. Is the skill only declared, or already effective?
   - declared only -> verify whether the actual skill asset exists and can be called
   - effective -> continue to evolution decision
3. Can an existing skill absorb it?
   - yes -> update that skill
   - no -> create a new skill candidate
4. Is a full skill necessary?
   - no -> create or update template / doc / rule
   - yes -> create a governance task and update the skill asset

## Required updates

- archive table
- skill-specific doc
- task or log entry
- if needed, project or runtime `SKILL.md`
- next-round backlog
