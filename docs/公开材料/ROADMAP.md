# Roadmap | 路线图

This roadmap keeps the public project focused: Enterprise AI Development OS is a governance and adapter layer for AI-assisted development, not a generic AI application platform.

本路线图保持公开项目聚焦：Enterprise AI Development OS 是面向 AI 辅助开发的治理与适配层，不是通用 AI 应用平台。

## Positioning | 定位

**Current open-source scope:**

- portable rules and session entrypoints
- skill-based task routing and execution discipline
- documentation memory and writeback templates
- audit gates and readiness scoring
- one-click installation
- multi-tool adapters for AI coding tools

**Future advanced scope:**

- executable rule runtime
- rule hit and failure reports
- AI generation quality benchmarks
- MCP/tool-call audit model
- team governance and policy packs

The advanced scope is intentionally described as future work. Public claims must not imply these features are already implemented.

高级能力只作为未来方向描述。公开表述不得暗示这些能力已经实现。

## Near Term | 近期

| Item | Outcome | Public status |
|---|---|---|
| Clearer value proposition | Explain that the project makes AI coding tools follow project rules and verification gates | In progress |
| One-click install | Make adoption easy with lite/full installers | Done |
| Value evidence template | Track token, rework, defect, verification, and consistency data | Planned |
| Rule Runtime Lite design | Define the smallest executable rule engine worth building | Planned |
| GitHub community workflow | Issues, PRs, security, governance, contribution flow | Done |

## Next | 下一阶段

| Item | Outcome | Notes |
|---|---|---|
| Benchmark examples | Small reproducible before/after cases | Use sanitized examples only |
| Rule pack metadata | Describe rules in structured files before making a full engine | Avoid large platform rewrite |
| Tool compatibility evidence | Record which adapters are verified, experimental, or pending | Keep `tools/adapters.json` authoritative |
| Runtime verification evidence | Make verification outputs easier to compare across tools | Do not publish private project logs |

## Later | 后续

| Item | Outcome | Constraint |
|---|---|---|
| Rule Runtime Lite implementation | Execute a small set of rules against generated outputs | Start with file/path/schema checks before AST |
| AST / Tree-sitter rules | Add semantic checks for selected languages | Only after benchmark need is proven |
| MCP audit model | Define tool-call permission and audit records | Start as docs/spec before gateway implementation |
| VS Code extension | Visual rule feedback and install helper | Only if community demand appears |
| Team governance packs | Role-based rule bundles and approval gates | Keep business-specific content private |

## Out Of Scope For Now | 暂不做

- blockchain audit storage
- physical access-control integration
- Kubernetes/GPU scheduler
- full model lifecycle management platform
- large web admin console

These may sound enterprise-grade, but they would distract from the current value: making AI coding work more predictably inside real projects.

