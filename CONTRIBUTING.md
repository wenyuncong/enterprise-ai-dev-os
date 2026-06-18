# Contributing

Thanks for considering a contribution to Enterprise AI Development OS.

## What To Contribute

Good first contribution areas:

- fix unclear rules or documentation
- improve an existing skill
- add verification examples
- improve tool adapters
- add compatibility evidence for a tool version
- improve audit scripts without weakening the boundary checks

Please avoid submitting:

- private customer/project material
- unredacted screenshots, logs, or local paths
- generated adapter output such as `.trae/`, `.qoder/`, `.cursor/`, `.agents/`
- large raw archives or copied third-party repositories
- claims about a tool integration without evidence

## Contribution Flow

1. Fork the repository.
2. Create a branch from `main`.
3. Make a focused change.
4. Run the required checks.
5. Open a pull request using the PR template.

## Required Checks

Run these before opening a PR:

```powershell
py scripts/py/audit_methodology.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
py scripts/py/score_ai_development_readiness.py --project-root .
powershell -NoProfile -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -DryRun
```

For website changes, also check:

```powershell
node -e "const fs=require('fs'); const html=fs.readFileSync('site/index.html','utf8'); if(!html.includes('Enterprise AI Development OS')) process.exit(1); console.log('site ok')"
```

## Updating Rules

Rules live in `rules/AGENTS.md`. If you change rules:

- keep them tool-agnostic
- do not add private project paths
- keep generated adapter outputs out of source control
- update `AGENTS.md` and `CLAUDE.md` only when they intentionally need to mirror the rule entrypoint
- run the audit scripts

## Updating Skills

Skills live under `skills/`.

Each skill should have:

- a `SKILL.md`
- clear trigger conditions
- workflow or checklist guidance
- guardrails
- references only when they are needed

If you add, remove, or rename a skill, update:

- `skills/SKILL_MANIFEST.json`
- `docs/全项目总控/MASTER_INDEX.md`
- relevant compatibility or adapter docs if needed

## Updating Tool Adapters

Adapter source lives in:

- `tools/adapters.json`
- `tools/deploy.ps1`
- `docs/TOOL_ADAPTERS.md`
- `docs/COMPATIBILITY.md`

Do not commit generated adapter directories. If a tool requires a different generated layout, update `tools/deploy.ps1` and document the verified behavior.

Adapter status rules:

- `verified`: official docs or live behavior proves the rule path and loading behavior
- `experimental`: likely works, but needs version-specific verification
- `pending-verification`: do not make public support claims yet

## Open-Source Boundary

This repository intentionally excludes private strategy, raw archives, process logs, local tool state, and unredacted case material. See:

- `docs/公开材料/OPEN_SOURCE_PACKAGE.md`
- `docs/公开材料/OPEN_SOURCE_READINESS.md`
- `docs/全项目总控/DISCLOSURE_BOUNDARY.md`

When in doubt, open an issue before submitting the material.

## Pull Request Expectations

A PR should include:

- what changed
- why it changed
- which checks passed
- whether compatibility or public claims changed
- screenshots only when they are safe and relevant

Small, focused PRs are preferred.
