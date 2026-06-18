---
name: ai-tool-bootstrapper
description: "Detect, acquire, register, and verify missing development tools without wasting time on environment confusion. Use when commands are missing, versions are wrong, tool paths are unknown, or project automation depends on local runtimes."
---

# ai-tool-bootstrapper — Self-Healing Environment & Tool Acquisition Engine

## Purpose | 用途

Automatically detect, acquire, install, and verify missing development tools. This skill gives the methodology the ability to **self-heal its own environment** — when a required tool is missing, it doesn't fail; it finds, downloads, installs, and verifies.

**Problem it solves**: AI often fails with "tool not found" or requires manual `npm install` / `pip install` / `apt-get install` steps that break the autonomous flow. This skill removes that friction.

## Trigger | 触发条件

- Any skill or task encounters "command not found", "module not found", "cannot find module"
- `ai-command-executor` environment check fails
- `ai-runtime-verify` detects missing Playwright browsers
- Before starting any task that declares tool dependencies
- User says "install X", "setup environment", "bootstrap project"

---

## Core Principle | 核心原则

**Never ask the user to install a tool. Detect the gap, solve it, verify it, and continue.**

```
Detect → Research → Acquire → Install → Verify → Record → Continue
```

---

## Tool Categories & Acquisition Strategies | 工具分类与获取策略

### Category 1: Package Managers (npm/pip/cargo/composer)
| Tool | Detection | Install Command | Post-Install |
|---|---|---|---|
| npm package | `require("pkg")` fails | `npm install pkg` | `node -e "require('pkg')"` |
| pip package | `import pkg` fails | `pip install pkg` | `python -c "import pkg"` |
| Playwright browsers | `npx playwright --version` | `npx playwright install chromium` | Launch test |

### Category 2: System Tools (git, curl, wget, jq)
| Tool | Detection | Install Strategy |
|---|---|---|
| git | `where git` / `which git` | `winget install Git.Git` (Win) / `apt-get install git` (Linux) |
| curl | `curl --version` | `winget install curl.curl` (Win) |
| jq | `jq --version` | `winget install jqlang.jq` (Win) / `apt-get install jq` (Linux) |

### Category 3: Runtime Environments (Node, Python, Java, .NET)
| Runtime | Detection | Install Strategy |
|---|---|---|
| Node.js | `node --version` | `winget install OpenJS.NodeJS.LTS` / `nvm install --lts` |
| Python | `python --version` | `winget install Python.Python.3` |
| Java/JDK | `java --version` | `winget install EclipseAdoptium.Temurin.17.JDK` |
| .NET SDK | `dotnet --version` | `winget install Microsoft.DotNet.SDK.8` |

### Category 4: Database & Services (MySQL, PostgreSQL, Redis, Docker)
| Tool | Detection | Install Strategy |
|---|---|---|
| MySQL CLI | `mysql --version` | `winget install Oracle.MySQL` |
| Docker | `docker --version` | `winget install Docker.DockerDesktop` |
| Redis | `redis-cli ping` | `winget install Redis.Redis` |

### Category 5: Browser Automation (Playwright, Puppeteer, Selenium)
| Tool | Detection | Install Strategy |
|---|---|---|
| Playwright | `npx playwright --version` | `npm install playwright && npx playwright install chromium` |
| Edge fallback | Use Playwright `channel: "msedge"` or resolve via OS browser registry | Use `channel: "msedge"` as fallback |
| Chrome | Use Playwright `channel: "chrome"` or resolve via OS browser registry | Use `channel: "chrome"` as fallback |

---

## Self-Evolution Mechanism | 自我进化机制

When a new tool is encountered that isn't in the known categories:

1. **Detect**: What tool is missing? What package format?
2. **Research**: Search for install instructions (internet search, npm/pip registry, winget/chocolatey/apt)
3. **Acquire**: Execute the install command
4. **Verify**: Run the version/detection check again
5. **Record**: Add the tool to the knowledge base for future use
6. **Evolve**: Feed the new tool pattern to `ai-skill-evolver`

---


## Registry-First Rule | 注册表优先规则

**Before installing ANY tool**, check the persistent registry:

```bash
# 1. Check if tool is already registered
python scripts/py/tool_registry.py get {tool_name}

# 2. If registered → USE existing path. Do NOT re-install.
# 3. If NOT registered → install, then register:
python scripts/py/tool_registry.py set {tool_name} "{install_path}" "{version}"
```

**Why**: Tools installed in one session must be remembered in the next. The registry at `tools/tool-registry.json` is the persistent memory.

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

---

## Integration Points | 集成点

| Skill | Integration |
|---|---|
| `ai-command-executor` | When env check fails, delegate to bootstrapper before retrying |
| `ai-runtime-verify` | When Playwright browsers missing, trigger bootstrapper |
| `ai-chief-planner` | During project setup phase, bootstrap all declared dependencies |
| `ai-skill-evolver` | Feed new tool patterns back for method evolution |

---

## Guardrails | 防护规则

- **Never install system-level tools without user awareness** (notify but don't block for package-level tools)
- **Prefer project-local installs** over global installs when possible
- **Record every install** — what was missing, how it was fixed, how long it took
- **Handle network failures gracefully** — offline detection, retry with backoff
- **Respect OS boundaries** — Windows uses `winget` / `choco`, Linux uses `apt` / `yum`, macOS uses `brew`
- **Verify after install** — never assume install succeeded

## Maturity | 成熟度

**Stage**: New — Created to fill the self-healing environment gap in AI autonomous development.

## Evolution History | 进化记录

- v1.0.0: Initial creation — 5 tool categories, auto-detection, winget/npm/pip install strategies, self-evolution recording
