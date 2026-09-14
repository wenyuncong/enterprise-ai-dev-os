# 工具适配器 | Tool Adapters

> **源文件**：docs/TOOL_ADAPTERS.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

企业级 AI 开发操作系统（Enterprise AI Development OS）使用**一个正式方法论源（canonical methodology source）**，并生成**多个适配器目标（adapter targets）**。

---

## 1 正式源 | Source Of Truth

| 资产（Asset） | 正式路径（Canonical path） |
|---|---|
| 会话规则（Session rules） | `rules/AGENTS.md` |
| Skill | `skills/` |
| 文档模板（Documentation templates） | `docs/_templates/` |
| 适配器注册表（Adapter registry） | `tools/adapters.json` |
| 适配器部署脚本（Adapter deploy script） | `tools/deploy.ps1` |

`.trae/`、`.qoder/`、`.cursor/`、`.github/copilot-instructions.md`、`.windsurfrules`、`CONVENTIONS.md` 等适配器产物都是**生成的交付文件（generated delivery files）**，它们被有意排除在 Git 之外（intentionally ignored by Git）。

---

## 2 适配器状态 | Adapter Status

| 层级（Tier） | 工具（Tool） | 状态（Status） | 规则目标（Rule target） | Skill 目标（Skill target） |
|---|---|---|---|---|
| P0 | Codex | 已验证（Verified） | `AGENTS.md` | `.agents/skills` |
| P0 | Claude Code | 已验证（Verified） | `CLAUDE.md` | `.claude/skills` |
| P0 | Trae | 规则已验证，Skill 实验性（Verified rules, experimental skills） | `.trae/rules/project_rules.md` | `.trae/skills` |
| P0 | Qoder / Qoder CN | 规则与 Skill 已验证（Verified rules and skills） | `.qoder/rules/enterprise-ai-dev-os.md` | `.qoder/skills/{skill-name}` |
| P1 | Cursor | 规则已验证，Skill 实验性（Verified rules, experimental skills） | `.cursor/rules/enterprise-ai-dev-os.mdc`、`.cursorrules` | `.cursor/skills` |
| P1 | GitHub Copilot / VS Code | 规则已验证，无 Skill（Verified rules, no skills） | `.github/copilot-instructions.md`、`.github/instructions/*.instructions.md` | 不支持（Not supported） |
| P1 | CodeBuddy | 已验证（Verified） | `.codebuddy/rules.md` | `.codebuddy/skills` |
| P2 | Windsurf | 实验性（Experimental） | `.windsurfrules`、`.windsurf/rules.md` | `.windsurf/skills` |
| P2 | Cline | 实验性（Experimental） | `.clinerules` | `.cline/skills` |
| P2 | Roo Code | 实验性（Experimental） | `.roo/rules.md` | `.roo/skills` |
| P2 | Aider | 实验性（Experimental） | `CONVENTIONS.md` | 不支持（Not supported） |
| P2 | Continue.dev | 实验性（Experimental） | `.continue/rules.md` | `.continue/skills` |
| P3 | Trae Solo | 待验证（Pending verification） | `.trae/rules/project_rules.md` | `.trae/skills` |
| P3 | Tongyi Lingma | 待验证（Pending verification） | `.lingma/rules.md` | `.lingma/skills` |
| P3 | WorkBuddy | 待验证（Pending verification） | 未知（Unknown） | 未知（Unknown） |

---

## 3 部署命令 | Deploy Commands

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

> **部署命令对照**：`AGENTS.md` 第 12 节步骤 10 给出的部署命令是 `pwsh tools/deploy.ps1 -Tool all -Force`。按本文件第 5 节的验证契约，`-Tool all` 默认**不包含**待验证（`pending-verification`）工具，需要部署它们时必须显式追加 `-IncludePending`。

---

## 4 全局（用户级）部署 | Global (User-Level) Deploy

把共享的方法论内核（shared methodology kernel）部署到用户级位置，使**这台机器上的每个项目**都加载同一套规则，而无需把它们逐个复制进各项目。覆盖前，已有的用户文件会备份到 `~/.enterprise-ai-dev-os/backup/`；首次部署时会创建一个全局记忆文件 `~/.enterprise-ai-dev-os/user-preferences.md`，用于存放跨项目偏好、跨项目 `shared language`（共享语言）与教训。

```powershell
# Preview global deploy
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Scope global -DryRun

# Deploy global rules (codex -> ~/.codex/AGENTS.md, claude -> ~/.claude/CLAUDE.md)
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Scope global -Force

# Project + global in one run
powershell -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -Scope both -Force
```

全局目标在 `tools/adapters.json` 的 `globalTargets` 下注册；其来源是 `rules/AGENTS.global.md`。项目级规则（仓库内的 `AGENTS.md` / `CLAUDE.md`）优先于全局规则。

---

## 5 验证契约 | Verification Contract

一个工具只有在全部检查通过之后，才能从 `pending-verification` 或 `experimental` 移动为 `verified`：

1. 官方文档或产品的实际行为确认该规则路径。
2. 生成出来的适配器文件能在新会话中被**自动加载**。
3. 该工具至少遵守会话启动（session-start）、任务连续性（task-continuity）与验证门禁（verification-gate）这三类规则。
4. 如果声明支持 Skill，该工具必须能访问 `SKILL.md` 及其链接的 `references/` 文件。像 Qoder 这类期望 `.qoder/skills/{skill-name}/SKILL.md` 的工具，收到的是对正式分层 `skills/` 目录树的**扁平化投影（flattened projection）**。
5. 适配器产物始终是生成文件，**不得**变成真相源（source of truth）。

---

## 6 策略 | Strategy

不要为每个 IDE 单独制作一次性的提示词包（one-off prompt packs）。保持核心操作系统稳定，然后为每个工具生成所需的最小适配器。这样产品才能与普通的规则合集形成差异化，未来支持新工具的成本也更低。

---

## 7 公开参考 | Public References

- Codex Skills: https://developers.openai.com/codex/skills
- Qoder Rules: https://docs.qoder.com/user-guide/rules
- Qoder Skills: https://docs.qoder.com/zh/extensions/skills
- Cursor Rules: https://cursor.com/docs/rules
- GitHub Copilot custom instructions: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- VS Code custom instructions: https://code.visualstudio.com/docs/copilot/customization/custom-instructions

---

## 译注

- 源文件未标注版本号，故「源版本」写作「未标注」。
- 源文件 7 个章节（Source Of Truth、Adapter Status、Deploy Commands、Global (User-Level) Deploy、Verification Contract、Strategy、Public References）逐节对应，**未删章节**；适配器状态表 15 行逐行对应，验证契约 5 条逐条对应，部署命令块 5 条、全局部署命令块 3 条原样保留。
- 所有状态值（`verified`、`experimental`、`pending-verification`、`Verified`、`Experimental`、`Pending verification`）、层级代号 `P0`–`P3`、目录名（`.agents/`、`.trae/`、`.qoder/`、`.claude/`、`.codebuddy/`、`.cursor/`、`.windsurf/`、`.cline/`、`.roo/`、`.continue/`、`.lingma/`）、命令与路径一律保留英文原文，中文仅作注释并列出现。
- PowerShell 代码块按口径**原样复制、不译**（含块内英文注释）。
- 第 4 节原文「every project on this machine」按其本机含义译为「这台机器上的每个项目」，未引入盘符路径。
