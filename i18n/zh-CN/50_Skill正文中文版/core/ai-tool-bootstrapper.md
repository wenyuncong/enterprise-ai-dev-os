# `ai-tool-bootstrapper` — 自愈环境与工具获取引擎

> **源文件**：skills/core/ai-tool-bootstrapper/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-tool-bootstrapper
description: "Detect, acquire, register, and verify missing development tools without wasting time on environment confusion. Use when commands are missing, versions are wrong, tool paths are unknown, or project automation depends on local runtimes."
```

**中文描述**：检测、获取、注册并验证缺失的开发工具，避免在环境混乱上浪费时间。当命令缺失、版本不对、工具路径未知，或项目自动化依赖本地运行时，使用本 Skill。

---

## Rule | 规则

工具自举必须做到：1）检测当前环境；2）识别缺失工具；3）按锁定版本安装；4）配置项目专属设置；5）端到端验证工具链。禁止在未核实的情况下假定工具可用。

# ai-tool-bootstrapper — Self-Healing Environment & Tool Acquisition Engine | 自愈环境与工具获取引擎

## Purpose | 用途

自动检测、获取、安装并验证缺失的开发工具。本 Skill 让方法论具备**自愈自身环境**的能力——当必需工具缺失时，它不会失败，而是去查找、下载、安装并验证。

**它解决的问题**：AI 经常因 "tool not found" 而失败，或需要人工执行 `npm install` / `pip install` / `apt-get install`，从而打断自主流程。本 Skill 消除这类摩擦。

## Trigger | 触发条件

- 任何 Skill 或任务遇到 "command not found"、"module not found"、"cannot find module"
- `ai-command-executor` 的环境检查失败
- `ai-runtime-verify` 检测到 Playwright 浏览器缺失
- 在开始任何声明了工具依赖的任务之前
- 用户说 "install X"、"setup environment"、"bootstrap project"

---

## Core Principle | 核心原则

**禁止要求用户去安装工具。检测缺口、解决缺口、验证结果，然后继续。**

```
Detect → Research → Acquire → Install → Verify → Record → Continue
```

---

## Tool Categories & Acquisition Strategies | 工具分类与获取策略

### Category 1: Package Managers (npm/pip/cargo/composer) | 类别 1：包管理器（npm/pip/cargo/composer）

| 工具 | 检测方式 | 安装命令 | 安装后验证 |
|---|---|---|---|
| npm 包 | `require("pkg")` 失败 | `npm install pkg` | `node -e "require('pkg')"` |
| pip 包 | `import pkg` 失败 | `pip install pkg` | `python -c "import pkg"` |
| Playwright 浏览器 | `npx playwright --version` | `npx playwright install chromium` | 启动测试 |

### Category 2: System Tools (git, curl, wget, jq) | 类别 2：系统工具（git、curl、wget、jq）

| 工具 | 检测方式 | 安装策略 |
|---|---|---|
| git | `where git` / `which git` | `winget install Git.Git`（Windows）/ `apt-get install git`（Linux） |
| curl | `curl --version` | `winget install curl.curl`（Windows） |
| jq | `jq --version` | `winget install jqlang.jq`（Windows）/ `apt-get install jq`（Linux） |

### Category 3: Runtime Environments (Node, Python, Java, .NET) | 类别 3：运行时环境（Node、Python、Java、.NET）

| 运行时 | 检测方式 | 安装策略 |
|---|---|---|
| Node.js | `node --version` | `winget install OpenJS.NodeJS.LTS` / `nvm install --lts` |
| Python | `python --version` | `winget install Python.Python.3` |
| Java/JDK | `java --version` | `winget install EclipseAdoptium.Temurin.17.JDK` |
| .NET SDK | `dotnet --version` | `winget install Microsoft.DotNet.SDK.8` |

### Category 4: Database & Services (MySQL, PostgreSQL, Redis, Docker) | 类别 4：数据库与服务（MySQL、PostgreSQL、Redis、Docker）

| 工具 | 检测方式 | 安装策略 |
|---|---|---|
| MySQL CLI | `mysql --version` | `winget install Oracle.MySQL` |
| Docker | `docker --version` | `winget install Docker.DockerDesktop` |
| Redis | `redis-cli ping` | `winget install Redis.Redis` |

### Category 5: Browser Automation (Playwright, Puppeteer, Selenium) | 类别 5：浏览器自动化（Playwright、Puppeteer、Selenium）

| 工具 | 检测方式 | 安装策略 |
|---|---|---|
| Playwright | `npx playwright --version` | `npm install playwright && npx playwright install chromium` |
| Edge 兜底 | 使用 Playwright `channel: "msedge"`，或通过操作系统浏览器注册表解析 | 用 `channel: "msedge"` 作为兜底 |
| Chrome | 使用 Playwright `channel: "chrome"`，或通过操作系统浏览器注册表解析 | 用 `channel: "chrome"` 作为兜底 |

---

## Self-Evolution Mechanism | 自我进化机制

当遇到不在已知分类中的新工具时：

1. **检测（Detect）**：缺的是哪个工具？包格式是什么？
2. **调研（Research）**：检索安装说明（互联网搜索、npm/pip registry、winget/chocolatey/apt）
3. **获取（Acquire）**：执行安装命令
4. **验证（Verify）**：再次运行版本/检测检查
5. **记录（Record）**：把该工具加入知识库，供后续复用
6. **进化（Evolve）**：把新的工具模式回灌给 `ai-skill-evolver`

---

## Registry-First Rule | 注册表优先规则

**在安装任何工具之前**，先检查持久化注册表：

```bash
# 1. Check if tool is already registered
python scripts/py/tool_registry.py get {tool_name}

# 2. If registered → USE existing path. Do NOT re-install.
# 3. If NOT registered → install, then register:
python scripts/py/tool_registry.py set {tool_name} "{install_path}" "{version}"
```

**为什么**：一个会话里安装的工具必须被下一个会话记住。位于 `tools/tool-registry.json` 的注册表就是这份持久记忆。

---

## Standard Workflow | 标准工作流

```
1. Receive request: "Need tool X"
1a. Check registry FIRST: `python scripts/py/tool_registry.py get X`
1b. If registered → return path. DONE. (saves time, avoids re-install)
2. Check: Is X already installed? → YES: Return path/version. DONE.
3. Classify: What category is X?
4. Search memory: Have we installed X before? → YES: Reuse known strategy
5. Search internet: What's the canonical install method?
6. Execute: Run install command with appropriate package manager
7. Verify: Check installation succeeded
8. Record: Cache install strategy for next time
9. Return: Tool is now available
```

**中文对照**：

1. 接收请求："Need tool X"。
2. 先查注册表：`python scripts/py/tool_registry.py get X`。
3. 若已注册 → 返回路径。完成。（省时，避免重复安装。）
4. 检查：X 是否已安装？→ 是：返回路径/版本。完成。
5. 分类：X 属于哪个类别？
6. 检索记忆：我们以前装过 X 吗？→ 是：复用已知策略。
7. 检索互联网：该工具的规范安装方法是什么？
8. 执行：用合适的包管理器运行安装命令。
9. 验证：确认安装成功。
10. 记录：缓存安装策略，供下次使用。
11. 返回：工具现已可用。

---

## Integration Points | 集成点

| Skill | 集成方式 |
|---|---|
| `ai-command-executor` | 环境检查失败时，先委派给 bootstrapper，再重试 |
| `ai-runtime-verify` | Playwright 浏览器缺失时，触发 bootstrapper |
| `ai-chief-planner` | 项目搭建阶段，自举所有已声明的依赖 |
| `ai-skill-evolver` | 把新工具模式回灌，用于方法论进化 |

---

## Guardrails | 防护规则

- **禁止在用户不知情的情况下安装系统级工具**（包级工具只做通知，不阻塞）
- **能装项目本地就优先项目本地安装**，而不是全局安装
- **每次安装都必须记录** —— 缺了什么、怎么修的、花了多久
- **优雅处理网络失败** —— 离线检测、带退避的重试
- **尊重操作系统边界** —— Windows 用 `winget` / `choco`，Linux 用 `apt` / `yum`，macOS 用 `brew`
- **安装后必须验证** —— 禁止假定安装成功

## Maturity | 成熟度

**Stage**：New（新建）—— 为填补 AI 自主开发中自愈环境的空白而创建。

## Evolution History | 进化记录

- v1.0.0：初始创建 —— 5 个工具分类、自动检测、winget/npm/pip 安装策略、自进化记录

---

## 译注

- 源文件 frontmatter 未标注版本号；`skills/SKILL_MANIFEST.json` 中该 Skill 的 `maturity` 为 `verified`，正文 `## Maturity` 自述 Stage 为 `New`，两者口径不同，本译文如实保留原文。
- 源文件 H1 前先有 `## Rule`；本译文保持源文件的章节顺序。
- 源文件 `### Category 1` 标题写作 `(npm/pip/cargo/composer)`，但表内只给出 npm、pip、Playwright 三类，未出现 `cargo`/`composer` 示例；本译文照抄源标题，不加推断。
- 源文件 `### Category 5` 中 `Edge 兜底`、`Chrome` 两行的「检测方式」单元格填的是兜底方案而非检测命令，属源文件结构瑕疵，本译文按原意照译。
- 源文件使用 `python scripts/py/tool_registry.py`，而仓库规则文件（`AGENTS.md`）使用 `py scripts/py/tool_registry.py`；两种入口写法不一致，本译文保留源文件的 `python` 写法。
