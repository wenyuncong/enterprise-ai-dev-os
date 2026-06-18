# Tool Adapters

Enterprise AI Development OS uses one canonical methodology source and many generated adapter targets.

## Source Of Truth

| Asset | Canonical path |
|---|---|
| Session rules | `rules/AGENTS.md` |
| Skills | `skills/` |
| Documentation templates | `docs/_templates/` |
| Adapter registry | `tools/adapters.json` |
| Adapter deploy script | `tools/deploy.ps1` |

Adapter outputs such as `.trae/`, `.qoder/`, `.cursor/`, `.github/copilot-instructions.md`, `.windsurfrules`, and `CONVENTIONS.md` are generated delivery files. They are intentionally ignored by Git.

## Adapter Status

| Tier | Tool | Status | Rule target | Skill target |
|---|---|---|---|---|
| P0 | Codex | Verified | `AGENTS.md` | `.agents/skills` |
| P0 | Claude Code | Verified | `CLAUDE.md` | `.claude/skills` |
| P0 | Trae | Verified rules, experimental skills | `.trae/rules/project_rules.md` | `.trae/skills` |
| P0 | Qoder / Qoder CN | Verified rules and skills | `.qoder/rules/enterprise-ai-dev-os.md` | `.qoder/skills/{skill-name}` |
| P1 | Cursor | Verified rules, experimental skills | `.cursor/rules/enterprise-ai-dev-os.mdc`, `.cursorrules` | `.cursor/skills` |
| P1 | GitHub Copilot / VS Code | Verified rules, no skills | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` | Not supported |
| P2 | Windsurf | Experimental | `.windsurfrules`, `.windsurf/rules.md` | `.windsurf/skills` |
| P2 | Cline | Experimental | `.clinerules` | `.cline/skills` |
| P2 | Roo Code | Experimental | `.roo/rules.md` | `.roo/skills` |
| P2 | Aider | Experimental | `CONVENTIONS.md` | Not supported |
| P2 | Continue.dev | Experimental | `.continue/rules.md` | `.continue/skills` |
| P3 | Trae Solo | Pending verification | `.trae/rules/project_rules.md` | `.trae/skills` |
| P3 | Tongyi Lingma | Pending verification | `.lingma/rules.md` | `.lingma/skills` |
| P3 | WorkBuddy | Pending verification | Unknown | Unknown |

## Deploy Commands

```powershell
# Show verified adapters only
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -DryRun

# Deploy verified adapters
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -Force

# Include experimental adapters for local testing
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -IncludeExperimental -DryRun

# Test a specific adapter
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool qoder,cursor -Force

# Inspect all registered adapters, including pending tools
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool all -IncludePending -DryRun
```

## Verification Contract

A tool can move from `pending-verification` or `experimental` to `verified` only after all checks pass:

1. Official documentation or live product behavior confirms the rule path.
2. A generated adapter file is loaded automatically in a new session.
3. The tool follows at least the session-start, task-continuity, and verification-gate rules.
4. If skills are declared, the tool can access `SKILL.md` and linked `references/` files. Tools such as Qoder that expect `.qoder/skills/{skill-name}/SKILL.md` receive a flattened projection of the canonical layered `skills/` tree.
5. Adapter outputs remain generated files and do not become the source of truth.

## Strategy

Do not make one-off prompt packs for each IDE. Keep the core operating system stable, then generate the smallest adapter needed for each tool. This keeps the product differentiated from ordinary rule collections and makes future tools cheaper to support.

## Public References

- Codex Skills: https://developers.openai.com/codex/skills
- Qoder Rules: https://docs.qoder.com/user-guide/rules
- Qoder Skills: https://docs.qoder.com/zh/extensions/skills
- Cursor Rules: https://cursor.com/docs/rules
- GitHub Copilot custom instructions: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- VS Code custom instructions: https://code.visualstudio.com/docs/copilot/customization/custom-instructions
