---
name: ai-architecture-knowledge-and-delivery
description: "Use when scanning an existing project into a language-neutral Architecture IR, generating an applicable 13-step delivery plan and task DAG, or publishing bounded static knowledge-center evidence without treating the graph as runtime truth."
---

# ai-architecture-knowledge-and-delivery

## Rule

Architecture discovery is read-only evidence. It must preserve source ownership,
show confidence and limitations, and never substitute for runtime, database,
authorization, business-flow, or release evidence.

## When to Use

- After onboarding an existing project and before planning implementation work.
- When the project uses more than one language, framework, client, service, or
  database and the dependency boundary is not documented.
- When a project needs an automatically refreshed technical knowledge center or
  a generated delivery task pack.
- Do not use the generated graph as permission to modify code, execute
  migrations, or declare a business flow complete.

## Workflow

```text
Project Scan -> Technology Profile -> Architecture IR
-> 13-Step Applicability Plan -> Task DAG -> Knowledge Center -> Incremental Refresh
```

Use the existing onboarding workflow before this skill when methodology assets,
external skills, or project knowledge infrastructure are being introduced.

## Required outputs

`py scripts/py/architecture_delivery.py --project-root <project> --output knowledge/architecture`

- `architecture-ir.json`: language-neutral nodes and edges with source and confidence.
- `delivery-plan.json`: all 13 steps marked `applicable`, `not_applicable`, or
  `needs_confirmation`.
- `task-dag.json`: dependency-ordered execution nodes.
- `index.html`: read-only static knowledge center.

## Supported evidence

The scanner currently uses manifests, source files, imports, common route
declarations, SQL `CREATE TABLE` statements, tests, and deployment markers.
Adapters can extend detection for other languages without changing the IR.

## Guardrails

- Do not execute migrations or modify application source during scanning.
- Do not infer business truth, permissions, runtime health, or production
  closure from static nodes.
- Do not mark destructive, migration, release, or business acceptance work as
  automatic; it remains `needs_confirmation`.
- Refresh incrementally after meaningful source, dependency, script, or skill
  changes and retain scan limits and timestamps.
