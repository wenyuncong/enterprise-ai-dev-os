# AI 工具兼容矩阵 | Tool Compatibility Matrix

> 不同 AI 编码工具对本方法论的 Skill 文件的支持程度

---

## 兼容维度说明

| 维度 | 说明 | 为什么重要 |
|---|---|---|
| **SKILL.md 读取** | 工具能否读取并遵循 `skills/*/SKILL.md` 中的指令 | 核心功能——Skill 指令是方法论执行层的基础 |
| **多文件上下文** | 工具能否同时加载 SKILL.md + references/ 中的关联文件 | 复杂 Skill（如 ai-architect-governor）依赖 references/ 中的架构图 |
| **会话启动加载** | 工具是否在每次新对话时自动读取 AGENTS.md | 规则引擎和路由层的入口——如果靠手动粘贴则形同虚设 |
| **跨会话记忆** | 工具是否保留上次对话的上下文 | 直接影响文档回写的价值——有记忆则文档回写作用减半，无记忆则文档回写是唯一记忆来源 |
| **终端执行** | 工具能否执行 shell 命令（数据库验证、编译检查） | 13 步执行顺序的验证关卡依赖终端能力 |
| **规则持久性** | 规则文件是否在每次对话中自动生效（vs 用户需每次显式指定） | AGENTS.md 的威力取决于它是否自动生效 |

---

## 兼容矩阵

| 工具 | SKILL.md | 多文件上下文 | 会话启动加载 | 跨会话记忆 | 终端执行 | 规则持久性 | 综合评分 |
|---|---|---|---|---|---|---|---|
| **Codex (OpenAI)** | ✅ 原生支持 | ✅ 自动加载 | ✅ AGENTS.md 自动读取 | ❌ 每次新会话 | ✅ | ✅ | ⭐⭐⭐⭐ |
| **Cursor** | ⚠️ .cursorrules 格式不同 | ⚠️ 有限 | ✅ .cursorrules 自动加载 | ❌ 每次新会话 | ✅ | ✅ | ⭐⭐⭐ |
| **GitHub Copilot** | ⚠️ .github/copilot-instructions.md | ❌ 单文件 | ✅ 自动读取 | ❌ 每次新会话 | ⚠️ 仅 Chat 模式 | ✅ | ⭐⭐ |
| **Claude Code** | ✅ AGENTS.md 原生支持 | ✅ | ✅ AGENTS.md 自动读取 | ❌ 每次新会话 | ✅ | ✅ | ⭐⭐⭐⭐ |
| **Windsurf** | ⚠️ .windsurfrules | ❌ 单文件 | ✅ 自动读取 | ❌ 每次新会话 | ✅ | ✅ | ⭐⭐ |
| **Aider** | ⚠️ CONVENTIONS.md | ❌ 单文件 | ✅ 自动读取 | ❌ 每次新会话 | ✅ | ✅ | ⭐⭐ |
| **Cline / Roo Code** | ⚠️ .clinerules | ❌ 单文件 | ✅ 自动读取 | ❌ 每次新会话 | ✅ | ✅ | ⭐⭐ |
| **Continue.dev** | ⚠️ config.json rules | ❌ 单文件 | ✅ 自动读取 | ❌ 每次新会话 | ✅ | ✅ | ⭐⭐ |

**评分逻辑**：⭐⭐⭐⭐⭐ = 所有维度原生支持 | ⭐⭐⭐⭐ = 大部分支持，少量格式调整 | ⭐⭐⭐ = 需要格式迁移 | ⭐⭐ = 仅支持单文件规则

---

## 关键发现

### 方法论的最佳载体：Codex 和 Claude Code

这两个工具是目前唯一原生支持 AGENTS.md + 多文件 Skill 目录结构的。如果你打算部署完整版（42 Skill），这两个工具能直接使用，无需格式转换。

### Cursor 和 Copilot：需要适配层

Cursor 用 `.cursorrules`、Copilot 用 `copilot-instructions.md`——都是单文件。使用完整版时需要：
- 把 AGENTS.md 的核心内容合并进 `.cursorrules`
- 放弃多文件 Skill 结构，或手动在每次对话中粘贴 SKILL.md 内容

### 跨会话记忆：所有工具都是零

**这是关键。** 目前没有任何 AI 编码工具有真正的跨会话持久记忆。这意味着你的文档回写机制**对所有这些工具都有价值**——它是目前唯一可行的跨会话上下文传递方案。

### 对于精简版（lite）用户

Lite 版只需 AGENTS.md + 文档模板，**所有 8 个工具都能直接使用**，只需要把 AGENTS.md 内容放入对应工具的规则文件位置。

---

## 迁移指南速查

| 从 | 到 | 操作 |
|---|---|---|
| 本项目 (Codex/Claude) | Cursor | 合并 AGENTS.md → .cursorrules |
| 本项目 (Codex/Claude) | Copilot | 合并 AGENTS.md → .github/copilot-instructions.md |
| 本项目 (Codex/Claude) | Windsurf | 合并 AGENTS.md → .windsurfrules |
| 本项目 (Codex/Claude) | Aider | 合并 AGENTS.md → CONVENTIONS.md |
| Lite 版 | 任意工具 | 直接使用，按对应文件名放置 |

---

*最后更新：2026-06-17 | 基于各工具截至 2026-06 的公开文档*
