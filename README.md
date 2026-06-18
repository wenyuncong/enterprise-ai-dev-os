# Enterprise AI Development OS

Turn AI-assisted coding from ad-hoc generation into deterministic engineering.

This repository provides a portable operating layer for AI development tools: rules, skills, documentation memory, audit gates, and an evolution loop that help teams use tools such as Codex, Claude Code, Cursor, Copilot, Trae, Qoder, and VS Code more consistently.

## Why This Exists

AI coding tools are powerful, but large software projects need more than generation:

- persistent project memory across sessions
- clear rules before code changes
- task routing and decomposition
- reusable capability units
- verification before "done"
- documentation writeback
- continuous improvement when the same mistake repeats

This project packages those practices into a tool-agnostic methodology.

## What Is Included

| Layer | Purpose |
|---|---|
| Rules | Session startup, execution order, file placement, verification gates |
| Skills | Reusable capability units for planning, architecture, governance, frontend, backend, data, testing, and deployment topics |
| Documentation memory | Backlog, master index, templates, ADRs, writeback structure |
| Audit gates | Scripts that check methodology structure and open-source boundaries |
| Tool adapters | Deployment helpers for syncing rules and skills into supported AI tools |
| Evolution loop | Guidance for turning repeated mistakes into stronger reusable capability |

## Repository Layout

```text
AGENTS.md                 Main agent entrypoint
rules/                    Portable rule files
skills/                   Official skill source
methodology/              Methodology whitepapers
docs/_templates/          Documentation templates
docs/全项目总控/           Master index, disclosure boundary, delivery loop
docs/公开材料/             Public release notes and open-source package boundary
docs/TOOL_ADAPTERS.md      Multi-tool adapter matrix and deploy contract
scripts/py/               Audit, scoring, environment, and tool-discovery scripts
scripts/js/               CLI entrypoint
tools/                    Multi-tool deployment adapters
```

## Quick Start

### 1. Copy the Rule Entrypoint

```bash
cp rules/AGENTS.md your-project/AGENTS.md
```

### 2. Copy the Skill Layers You Need

```bash
cp -r skills/core your-project/skills/
cp -r skills/governance your-project/skills/
cp -r skills/tech/vue your-project/skills/        # example
cp -r skills/tech/java-springboot your-project/skills/
```

### 3. Copy Documentation Templates

```bash
cp -r docs/_templates your-project/docs/
```

### 4. Verify the Package

```bash
py scripts/py/audit_methodology.py --project-root .
py scripts/py/score_ai_development_readiness.py --project-root .
```

Expected for this repository:

```text
Methodology audit: PASS
Failures: 0 | Warnings: 0

AI development readiness: 100/100 (L4 可进化)
```

## Core Workflow

```text
Requirement
  -> Read rules and project memory
  -> Route the task
  -> Decompose into safe batches
  -> Execute with existing tools and scripts
  -> Verify with tests, API checks, browser checks, or audits
  -> Write back evidence
  -> Evolve skills when patterns repeat
```

## Key Commands

```bash
# Audit methodology structure
py scripts/py/audit_methodology.py --project-root .

# Score AI development readiness
py scripts/py/score_ai_development_readiness.py --project-root .

# Discover existing project tools
py scripts/py/discover_tools.py . --by-purpose

# Check local environment
py scripts/py/env_check.py --quick

# Check open-source publishing boundary
py scripts/py/check_open_source_boundary.py --project-root .

# Preview verified AI tool adapters
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -DryRun
```

## Open-Source Boundary

This repository separates public methodology assets from private/internal materials.

Before publishing or pushing changes, run:

```bash
py scripts/py/check_open_source_boundary.py --project-root .
```

See [docs/公开材料/OPEN_SOURCE_PACKAGE.md](docs/公开材料/OPEN_SOURCE_PACKAGE.md) and [docs/全项目总控/DISCLOSURE_BOUNDARY.md](docs/全项目总控/DISCLOSURE_BOUNDARY.md).

Current publish readiness is tracked in [docs/公开材料/OPEN_SOURCE_READINESS.md](docs/公开材料/OPEN_SOURCE_READINESS.md).

## Status

- 38 verified official skills
- methodology audit passing with 0 failures and 0 warnings
- AI development readiness score: 100/100 for repository structure
- tool-agnostic rules and multi-tool adapter registry
- public/private disclosure boundary documented

## Repository Description

Recommended GitHub description:

```text
Enterprise AI Development OS: rules, skills, documentation memory, audit gates, and evolution loops for deterministic AI-assisted engineering.
```

## License

Choose a license before publishing. Recommended options:

- Apache-2.0 for permissive use with explicit patent grant
- MIT for maximum simplicity
- Polyform / source-available terms if you want stronger commercial control
