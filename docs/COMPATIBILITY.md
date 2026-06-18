# AI Tool Compatibility Matrix

This matrix records how well each AI coding tool can consume Enterprise AI Development OS.

## Compatibility Dimensions

| Dimension | Meaning |
|---|---|
| Rules | Whether the tool can load persistent project instructions automatically. |
| Skills | Whether the tool can consume multi-file `SKILL.md` capability units. |
| References | Whether the tool can follow `references/` files linked by a skill. |
| Terminal | Whether the tool can run project verification commands. |
| Persistence | Whether rules remain active across new sessions. |
| Adapter status | Whether this repository has a verified deploy target. |

## Matrix

| Tool | Rules | Skills | References | Terminal | Persistence | Adapter status |
|---|---|---|---|---|---|---|
| Codex | Strong | Strong | Strong | Strong | Strong | Verified |
| Claude Code | Strong | Strong | Strong | Strong | Strong | Verified |
| Trae | Strong | Experimental | Experimental | Strong | Strong | Verified rules |
| Qoder / Qoder CN | Strong | Strong | Strong | Strong | Strong | Verified |
| Cursor | Strong | Experimental | Limited | Strong | Strong | Verified rules |
| GitHub Copilot / VS Code | Strong | Not native | Limited | Limited | Strong | Verified rules |
| Windsurf | Medium | Experimental | Limited | Strong | Medium | Experimental |
| Cline / Roo Code | Medium | Experimental | Limited | Strong | Medium | Experimental |
| Aider | Medium | Not native | Limited | Strong | Medium | Experimental |
| Continue.dev | Medium | Experimental | Limited | Strong | Medium | Experimental |
| Trae Solo | Unknown | Unknown | Unknown | Unknown | Unknown | Pending verification |
| Tongyi Lingma | Unknown | Unknown | Unknown | Unknown | Unknown | Pending verification |
| WorkBuddy | Unknown | Unknown | Unknown | Unknown | Unknown | Pending verification |

## Key Findings

### Best full-system carriers

Codex and Claude Code are the strongest carriers for the full operating-system model because they can work with an entry rule file and multi-file skill folders.

### Strong rule carriers

Trae, Qoder, Cursor, GitHub Copilot, and VS Code are good rule carriers. They are important for market reach even when their skill-directory behavior is weaker than Codex or Claude Code.

### Why adapters matter

The value is not that every tool has identical native behavior. The value is that the same rules, skills, memory structure, and audit gates can be projected into many tools without rewriting the methodology.

## Recommended Rollout Order

| Priority | Tools | Goal |
|---|---|---|
| P0 | Codex, Claude Code, Trae, Qoder | Full daily engineering loop |
| P1 | Cursor, GitHub Copilot, VS Code | Global mainstream developer reach |
| P2 | Windsurf, Cline, Roo Code, Aider, Continue.dev | Community and power-user coverage |
| P3 | Trae Solo, Tongyi Lingma, WorkBuddy | Verify before public claims |

See `docs/TOOL_ADAPTERS.md` for exact adapter paths and deploy commands.

## Public References

- Codex Skills: https://developers.openai.com/codex/skills
- Qoder Rules: https://docs.qoder.com/user-guide/rules
- Qoder Skills: https://docs.qoder.com/zh/extensions/skills
- Cursor Rules: https://cursor.com/docs/rules
- GitHub Copilot custom instructions: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- VS Code custom instructions: https://code.visualstudio.com/docs/copilot/customization/custom-instructions
