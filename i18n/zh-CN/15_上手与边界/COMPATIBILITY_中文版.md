# AI 工具兼容矩阵 | AI Tool Compatibility Matrix

> **源文件**：docs/COMPATIBILITY.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

本矩阵记录每个 AI 编码工具消费企业级 AI 开发操作系统（Enterprise AI Development OS）的能力强弱。

---

## 1 兼容维度 | Compatibility Dimensions

| 维度（Dimension） | 含义（Meaning） |
|---|---|
| Rules（规则） | 该工具能否自动加载持久化的项目指令。 |
| Skills（Skill） | 该工具能否消费多文件的 `SKILL.md` 能力单元。 |
| References（引用文件） | 该工具能否跟进 Skill 链接的 `references/` 文件。 |
| Terminal（终端） | 该工具能否运行项目验证命令。 |
| Persistence（持久性） | 规则能否在新会话中持续生效。 |
| Adapter status（适配器状态） | 本仓库是否为该工具提供已验证的部署目标。 |

---

## 2 矩阵 | Matrix

| 工具（Tool） | Rules | Skills | References | Terminal | Persistence | 适配器状态（Adapter status） |
|---|---|---|---|---|---|---|
| Codex | 强（Strong） | 强（Strong） | 强（Strong） | 强（Strong） | 强（Strong） | 已验证（Verified） |
| Claude Code | 强（Strong） | 强（Strong） | 强（Strong） | 强（Strong） | 强（Strong） | 已验证（Verified） |
| Trae | 强（Strong） | 实验性（Experimental） | 实验性（Experimental） | 强（Strong） | 强（Strong） | 规则已验证（Verified rules） |
| Qoder / Qoder CN | 强（Strong） | 强（Strong） | 强（Strong） | 强（Strong） | 强（Strong） | 已验证（Verified） |
| Cursor | 强（Strong） | 实验性（Experimental） | 有限（Limited） | 强（Strong） | 强（Strong） | 规则已验证（Verified rules） |
| CodeBuddy | 强（Strong） | 实验性（Experimental） | 有限（Limited） | 强（Strong） | 强（Strong） | 已验证（Verified） |
| GitHub Copilot / VS Code | 强（Strong） | 非原生（Not native） | 有限（Limited） | 有限（Limited） | 强（Strong） | 规则已验证（Verified rules） |
| Windsurf | 中（Medium） | 实验性（Experimental） | 有限（Limited） | 强（Strong） | 中（Medium） | 实验性（Experimental） |
| Cline / Roo Code | 中（Medium） | 实验性（Experimental） | 有限（Limited） | 强（Strong） | 中（Medium） | 实验性（Experimental） |
| Aider | 中（Medium） | 非原生（Not native） | 有限（Limited） | 强（Strong） | 中（Medium） | 实验性（Experimental） |
| Continue.dev | 中（Medium） | 实验性（Experimental） | 有限（Limited） | 强（Strong） | 中（Medium） | 实验性（Experimental） |
| Trae Solo | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 待验证（Pending verification） |
| Tongyi Lingma | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 待验证（Pending verification） |
| WorkBuddy | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 未知（Unknown） | 待验证（Pending verification） |

---

## 3 关键结论 | Key Findings

### 3.1 最佳全系统承载者 | Best full-system carriers

Codex 与 Claude Code 是「完整操作系统模型」最强的承载者，因为它们既能使用单个入口规则文件，也能使用多文件的 Skill 目录。

### 3.2 强规则承载者 | Strong rule carriers

Trae、Qoder、Cursor、GitHub Copilot 与 VS Code 都是优秀的规则承载者。即便它们的 Skill 目录行为弱于 Codex 或 Claude Code，它们对市场覆盖仍然重要。

### 3.3 适配器为何重要 | Why adapters matter

价值不在于每个工具都有完全相同的原生行为。价值在于：同一套规则、Skill、记忆结构与审计门禁，可以**在不重写方法论的前提下**投影到众多工具中。

---

## 4 推荐推广顺序 | Recommended Rollout Order

| 优先级（Priority） | 工具（Tools） | 目标（Goal） |
|---|---|---|
| P0 | Codex、Claude Code、Trae、Qoder | 完整的日常工程闭环（Full daily engineering loop） |
| P1 | Cursor、GitHub Copilot、VS Code | 覆盖全球主流开发者（Global mainstream developer reach） |
| P2 | Windsurf、Cline、Roo Code、Aider、Continue.dev | 社区与进阶用户覆盖（Community and power-user coverage） |
| P3 | Trae Solo、Tongyi Lingma、WorkBuddy | 公开声明之前先验证（Verify before public claims） |

精确的适配器路径与部署命令见 `docs/TOOL_ADAPTERS.md`。

---

## 5 公开参考 | Public References

- Codex Skills: https://developers.openai.com/codex/skills
- Qoder Rules: https://docs.qoder.com/user-guide/rules
- Qoder Skills: https://docs.qoder.com/zh/extensions/skills
- Cursor Rules: https://cursor.com/docs/rules
- GitHub Copilot custom instructions: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- VS Code custom instructions: https://code.visualstudio.com/docs/copilot/customization/custom-instructions

---

## 译注

- 源文件未标注版本号，故「源版本」写作「未标注」。
- 源文件 5 个章节（Compatibility Dimensions、Matrix、Key Findings、Recommended Rollout Order、Public References）逐节对应，**未删章节**；兼容维度表 6 行、矩阵 14 行、推广顺序表 4 行逐行对应，关键结论 3 个小节逐条对应。
- 矩阵表头保留英文维度名（`Rules`、`Skills`、`References`、`Terminal`、`Persistence`、`Adapter status`），单元格内的评级值采用「中文（English）」并列形式，不损失原评级语义。
- **源文件内部不一致（译注记录，不改源文件）**：第 2 节矩阵把 CodeBuddy 的 Skills 评为「实验性（Experimental）」，而 `tools/adapters.json` 中 CodeBuddy 的 `skills.status` 为 `verified`、`docs/TOOL_ADAPTERS.md` 亦标注 CodeBuddy 为「已验证（Verified）」。另：CodeBuddy 在 `docs/TOOL_ADAPTERS.md` 中属 P1 层级，却未出现在第 4 节的 P1 推广行中。以上均属源文件之间的口径差异，本译文如实照译，未作修正。
