# Governance

Enterprise AI Development OS is maintained as a portable methodology and adapter framework.

## Maintainer Responsibilities

Maintainers are responsible for:

- protecting the open-source boundary
- reviewing compatibility claims
- keeping `skills/` and `rules/AGENTS.md` as the canonical source
- keeping generated adapter outputs out of source control
- requiring verification before merge

## Source Of Truth

Canonical source:

- `rules/AGENTS.md`
- `skills/`
- `skills/SKILL_MANIFEST.json`
- `docs/_templates/`
- `tools/adapters.json`
- `tools/deploy.ps1`

Generated outputs are not source of truth.

## Decision Rules

Use evidence before public claims:

- tool adapters require official docs or live behavior
- new skills require a clear trigger and workflow
- release-facing docs must stay free of private paths and strategy
- audit failures block release

## Compatibility Status

Compatibility status is managed in `tools/adapters.json`:

- `verified`
- `experimental`
- `pending-verification`

Do not upgrade a tool to `verified` without documented evidence.
