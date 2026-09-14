# Enterprise AI Development OS

[Website](https://wenyuncong.github.io/enterprise-ai-dev-os/) | [中文](#中文) | [English](#english) | [中文版全文 / Chinese Edition](i18n/zh-CN/README.md)

**Keep your attention on the business goal and the final outcome. Let agents and large language models handle the engineering work inside a governed, verifiable delivery system.**

Enterprise AI Development OS is a portable methodology and governance toolkit for AI-assisted software delivery. It gives AI agents shared rules, reusable skills, project memory, backend truth boundaries, verification gates, and evidence-driven closure across tools and projects.

This repository provides rules, skills, templates, schemas, audit scripts, installers, CLI utilities, and adapter definitions. It does not provide a universal AI runtime, scheduler, command sandbox, or autonomous business system. Those controls belong to the target project or its own runtime.

It is not an unrestricted promise of autonomous software delivery. People still own business intent, priorities, material trade-offs, risk acceptance, and final business acceptance. Agents and models own the repeatable engineering work: discovery, planning, implementation, testing, documentation, evidence collection, and controlled correction.

## English

### What It Is

Enterprise AI Development OS turns AI coding from isolated generation into governed delivery:

```text
Business goal and expected outcome
  -> project classification
  -> rule routing and task decomposition
  -> agent and model execution
  -> tests, runtime checks, and business-flow verification
  -> evidence writeback and capability evolution
```

The system is designed for teams that want AI to do most of the engineering work while keeping business truth, permissions, state, side effects, and acceptance under explicit control. The target project remains responsible for implementing and operating its backend and runtime controls.

### The Human-AI Boundary

| Responsibility | Human | Agents and models |
|---|---|---|
| Business goal and expected outcome | Owns | Clarifies and structures |
| Product priority and trade-offs | Owns | Proposes options |
| Architecture, schema, code, tests, and docs | Accepts the result | Discovers, implements, and verifies |
| Runtime truth, permissions, state, and audit | Owns the business decision | Enforces through the target project's backend/runtime |
| Final business acceptance | Owns | Produces evidence for review |

The intended experience is simple: the product owner describes what the business must achieve and what the final result must look like. The AI delivery system handles the engineering path and reports what was actually proven.

### Why It Exists

AI coding tools are powerful, but enterprise delivery needs more than code generation:

- persistent project memory across sessions
- rules loaded before changes
- brownfield discovery before intervention
- task routing and dependency-aware batches
- reusable skills and standard templates
- backend-owned truth and frontend display boundaries
- verification before a result is called complete
- audit, migration, tenant, and release evidence
- repeated failures converted into stronger rules, tests, or skills
- consistent delivery across multiple AI tools

### Five-Layer Operating Model

| Layer | Question | Primary capability |
|---|---|---|
| Classification | What kind of project and quality target is this? | `ai-project-classifier` |
| Routing | Which rules and skills apply? | `ai-rule-dispatcher` |
| Decomposition | How can the work be split safely? | `ai-task-decomposer` |
| Execution | How is the solution implemented and verified? | Core, Governance, Tech, and Platform skills |
| Evolution | What should become reusable next time? | `ai-skill-evolver`, `ai-skill-governor` |

### Backend Truth And Frontend Delivery

For business software, agents follow two connected chains:

```text
Backend:
truth -> atomic service -> orchestration -> aggregate interface
       -> command gateway -> adapters -> Host / AI / MCP / OpenAPI

Frontend:
runtime and field truth -> UI atom -> UI orchestration
                        -> standard template -> Host page
```

Host pages and transport adapters load truth, render it, collect input, request supported commands, and show feedback. They must not become a second source of business rules, calculations, authorization, state transitions, or write paths.

### Delivery Qualification

Capability presence is not business closure. The methodology records the highest level supported by fresh evidence:

| Level | Meaning |
|---|---|
| Q0 | Capability exists in source, registry, or route |
| Q1 | Parameters, permissions, state, configuration, and dependencies align |
| Q2 | Backend orchestration, provider coverage, unique side-effect path, audit, and authoritative readback close |
| Q3 | Real business acceptance, reconciliation, cross-client/runtime, and release evidence close |

The maturity chain is:

```text
registered -> configured -> authorized -> provider-covered
            -> runtime-executable -> business-closed
```

HTTP 200, health checks, page visibility, CI success, or a local commit do not individually prove Q3.

### What Is Included

| Area | Purpose |
|---|---|
| Rules | Session startup, execution order, safety boundaries, and delivery gates |
| Skills | Planning, architecture, governance, frontend, backend, data, testing, and deployment capabilities |
| Documentation memory | Backlog, master index, templates, ADRs, and optional project writeback |
| Audit gates | Methodology structure, open-source boundary, governance, and readiness checks |
| Tool adapters | Deploy rules and skills into supported AI coding tools |
| Evolution loop | Turn repeated failures into rules, templates, tests, or skills |

### Quick Start

Lite mode is the recommended starting point. It adds the AI entrypoint, rules, documentation templates, and task backlog scaffold.

PowerShell:

```powershell
iwr -UseBasicParsing https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/ps1/install.ps1 | iex
```

Bash:

```bash
curl -fsSL https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/sh/install.sh | bash
```

Full mode:

```powershell
$u = "https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/ps1/install.ps1"
$s = Join-Path $env:TEMP "enterprise-ai-dev-os-install.ps1"
iwr -UseBasicParsing $u -OutFile $s
powershell -NoProfile -ExecutionPolicy Bypass -File $s -TargetPath . -Mode full
```

Verify this repository:

```bash
py scripts/py/test_methodology_scenarios.py --project-root .
py scripts/py/audit_ai_native_governance.py --project-root .
py scripts/py/audit_skill_health.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
```

More installation options are documented in [docs/公开材料/INSTALL.md](docs/公开材料/INSTALL.md).

### Repository Layout

```text
AGENTS.md                 Main rule entrypoint
rules/                    Portable rule source
skills/                   Official skill source
methodology/              Methodology whitepapers
docs/_templates/          Documentation templates
docs/全项目总控/           Master index and delivery control
docs/公开材料/             Public release boundary and evidence notes
scripts/py/               Audit, verification, environment, and discovery scripts
scripts/ps1/              PowerShell installers and utilities
scripts/sh/               Bash installers
scripts/js/               CLI entrypoint
tools/                    Adapter registry and deployment scripts
lite/                     Lite rules and templates
site/                     GitHub Pages website
```

### Public Documentation

- [Full AI-Native Development Whitepaper](docs/公开材料/FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_EN.md)
- [全 AI 原生开发白皮书](docs/公开材料/FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_CN.md)
- [Full AI-Native Development Standard](docs/公开材料/FULL_AI_NATIVE_DEVELOPMENT_STANDARD_EN.md)
- [全 AI 原生开发标准](docs/公开材料/FULL_AI_NATIVE_DEVELOPMENT_STANDARD_CN.md)
- [Roadmap](docs/公开材料/ROADMAP.md)
- [Value Evidence](docs/公开材料/VALUE_EVIDENCE.md)
- [Tool Adapters](docs/TOOL_ADAPTERS.md)
- [Compatibility](docs/COMPATIBILITY.md)

### Open-Source Boundary

This repository follows an **Open-Core Methodology** model. The complete portable methodology kernel is open source: rules, official skills, whitepapers, schemas, templates, audit scripts, installers, CLI tools, adapter generators, and the evolution loop. Private commercialization notes, real project source code, customer or tenant data, production configuration, unredacted cases, process evidence, local paths, and local tool state remain outside the public release.

The boundary is between **reusable methodology** and **real delivery assets**, not between “complete” and “simplified” documentation. The public repository is intended to be a complete, installable, auditable methodology package.

Before publishing or pushing changes, run:

```bash
py scripts/py/check_open_source_boundary.py --project-root .
```

See [docs/公开材料/OPEN_SOURCE_PACKAGE.md](docs/公开材料/OPEN_SOURCE_PACKAGE.md), [docs/公开材料/OPEN_SOURCE_READINESS.md](docs/公开材料/OPEN_SOURCE_READINESS.md), and [docs/全项目总控/DISCLOSURE_BOUNDARY.md](docs/全项目总控/DISCLOSURE_BOUNDARY.md).

### Implementation Boundary

The architecture documents describe what an adopted project may implement. They are not claims that this repository already implements every architectural object. In particular, a runtime, command gateway, registry, backend truth model, and business acceptance flow are project-owned. `Rule Runtime Lite` remains a future direction for making selected rules more executable.

### Current Evidence

- Methodology scenario regression: passing
- AI-native governance audit: passing
- Skill health audit: passing; 49 skills, average `100.0/100` structural health score
- L2 delivery contract for the latest methodology upgrade: passing
- Full methodology audit: passing with no failures or warnings
- Independent external business-effect evidence: not yet available; current practice evidence is author-led and not a cross-project benchmark

The evidence status above is intentionally more precise than a blanket “everything passes”. Run the project-owned checks for the current result.

### Community And License

- Questions and adapter discussions: GitHub Discussions
- Reproducible bugs and documentation errors: GitHub Issues
- Rules, skills, scripts, and adapter changes: Pull Requests

Read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing. Public contents are licensed under the [Apache License 2.0](LICENSE).

---

## 中文

### 这是什么

Enterprise AI Development OS 是一套面向全 AI 原生软件交付的可迁移方法论和治理层。

**人的主要工作是关注业务目标和最终效果；智能体与大模型在治理边界内完成需求分析、方案设计、代码、测试、文档、验证和问题修复。**

人仍然负责业务意图、优先级、重大取舍、风险接受和最终业务验收。AI 负责可重复的工程执行，并必须报告哪些结果已经被证据证明。

### 全 AI 原生开发的协作闭环

```text
业务目标与预期效果
  -> 项目分类
  -> 规则路由与任务拆解
  -> 智能体与大模型执行
  -> 测试、运行时和业务流程验证
  -> 证据回写与能力进化
```

它不是放任 AI 自由生成代码，也不是承诺 AI 无条件替代产品负责人或业务负责人。它是在规则、Skill、项目自身的后端/Runtime、命令入口、审计和验收结构内，让 AI 完成尽可能多的工程工作。本仓库本身不提供通用 Runtime、调度器或命令执行沙箱。

### 人与 AI 的边界

| 责任 | 人 | 智能体与大模型 |
|---|---|---|
| 业务目标和预期效果 | 负责 | 协助澄清和结构化 |
| 产品优先级和取舍 | 负责 | 提供方案 |
| 架构、数据库、代码、测试、文档 | 接受结果 | 发现、实现和验证 |
| 真相、权限、状态和审计 | 负责业务决策 | 通过系统执行和留证 |
| 最终业务验收 | 负责 | 提供证据 |

### 五层 Skill 操作模型

| 层 | 要回答的问题 | 主要能力 |
|---|---|---|
| 分类层 | 这是什么项目，质量目标是什么 | `ai-project-classifier` |
| 路由层 | 应使用哪些规则和 Skill | `ai-rule-dispatcher` |
| 分解层 | 如何安全拆成执行批次 | `ai-task-decomposer` |
| 执行层 | 如何实现并验证 | Core、Governance、Tech、Platform Skill |
| 进化层 | 哪些经验应成为下次能力 | `ai-skill-evolver`、`ai-skill-governor` |

### 后端真相与前端承载

```text
后端：
真相 -> 原子服务 -> 编排 -> 聚合接口
     -> 命令网关 -> 适配器 -> Host / AI / MCP / OpenAPI

前端：
运行时和字段真相 -> UI 原子 -> UI 编排
                -> 标准模板 -> Host 页面
```

Host 页面和传输适配器只负责加载真相、展示、收集输入、请求受支持的命令和展示反馈，不得成为第二套业务规则、计算、授权、状态迁移或写入路径。

### 交付资格

能力存在不等于业务完成。方法论用新鲜证据记录最高资格：

| 级别 | 含义 |
|---|---|
| Q0 | 能力存在于源码、注册表或路由 |
| Q1 | 参数、权限、状态、配置和依赖基线一致 |
| Q2 | 后端编排、Provider、唯一副作用链、审计和权威回读闭合 |
| Q3 | 真实业务验收、对账、跨端/运行时和发布证据闭合 |

能力成熟度链：

```text
registered -> configured -> authorized -> provider-covered
            -> runtime-executable -> business-closed
```

HTTP 200、健康检查、页面打开、CI 通过或本地提交，都不能单独证明 Q3。

### 快速开始

推荐先使用 lite 模式：

```powershell
iwr -UseBasicParsing https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/ps1/install.ps1 | iex
```

完整安装、仓库结构、公开文档、工具适配和开源边界请直接查看上面的 English 部分及对应文档链接。

### 当前证据状态

- 方法论场景回归：通过
- AI 原生治理审计：通过
- Skill 健康审计：通过，49 个 Skill，平均 `100.0/100`，这是结构健康度自检分
- 最新方法论升级的 L2 交付契约：通过
- 总方法论审计：通过，失败项和警告项均为 0
- 独立外部业务效果证据：当前尚无；现有经验来自作者主导实践，不能当作跨项目基准

### 开源边界与许可

本仓库采用 **Open-Core Methodology（开放方法论内核）** 模式。完整、可迁移的方法论内核公开，包括规则、官方 Skill、白皮书、Schema、模板、审计脚本、安装器、CLI、适配器生成器和进化闭环。

公开边界划分在“可复用方法论”和“真实交付资产”之间，而不是划分在“完整”和“简化”文档之间。私有商业策略、真实项目源代码、客户或租户数据、生产配置、未脱敏案例、过程证据、本机路径和本地工具状态不属于公开范围。

公开内容采用 [Apache License 2.0](LICENSE)。

### 实现边界

公开文档中的 Runtime、命令网关、注册表、后端真相和业务闭环，是采用本方法论的项目可以实现的架构对象，不代表本仓库已经提供这些通用运行能力。`Rule Runtime Lite` 仍是将部分规则逐步变为可执行检查的未来方向。
