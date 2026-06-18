# Enterprise AI Development OS

[中文](#中文) | [English](#english)

Enterprise AI Development OS turns AI-assisted coding from ad-hoc generation into deterministic engineering.

企业级全 AI 开发操作系统，用规则、Skill、文档记忆、验证门禁和多工具适配层，把 AI 编程从随机生成推进到可治理、可验证、可迁移的工程体系。

Website: https://wenyuncong.github.io/enterprise-ai-dev-os/ (available after GitHub Pages is enabled)

---

## 中文

### 这是什么

Enterprise AI Development OS 是一套面向 AI 编程工具的可迁移工程操作层。它把项目规则、Skill 能力单元、文档记忆、审计脚本、验证门禁和多工具适配器组织成一个统一系统，让 Codex、Claude Code、Trae、Qoder、Cursor、GitHub Copilot、VS Code 等工具在大项目中更稳定地协同工作。

它不是单个 prompt，也不只是传统意义上的 Skill 包。它更接近一个“AI 开发操作系统”：用统一入口、任务路由、能力调度、证据回写和进化闭环，降低 AI 开发中的遗忘、漂移、重复造轮子和验收不确定性。

### 为什么需要它

AI 编码工具很强，但企业级项目需要的不只是生成代码：

- 跨会话项目记忆
- 修改前规则加载
- 任务路由和拆解
- 可复用能力单元
- 完成前验证门禁
- 文档回写和证据链
- 重复问题反哺规则和 Skill
- 多工具之间的一致工作方式

本项目把这些实践打包成工具无关的方法论和适配器框架。

### 包含什么

| 层 | 作用 |
|---|---|
| Rules | 会话启动、执行顺序、目录边界、验证门禁 |
| Skills | 规划、架构、治理、前端、后端、数据、测试和部署能力单元 |
| Documentation memory | Backlog、总控索引、模板、ADR、调研回写结构 |
| Audit gates | 方法论结构检查、开源边界检查、就绪评分 |
| Tool adapters | 将规则和 Skill 投放到不同 AI 编程工具 |
| Evolution loop | 将重复问题升级为规则、模板或 Skill |

### 仓库结构

```text
AGENTS.md                 主规则入口
CLAUDE.md                 Claude Code 规则入口
rules/                    可迁移规则源
skills/                   官方 Skill 源
methodology/              方法论白皮书
docs/_templates/          文档模板
docs/全项目总控/           总控索引、披露边界、交付闭环
docs/公开材料/             开源发布边界和就绪清单
docs/TOOL_ADAPTERS.md     多工具适配矩阵和部署契约
scripts/py/               审计、评分、环境检查、工具发现脚本
scripts/js/               CLI 入口
tools/                    多工具适配器注册表和部署脚本
lite/                     精简版规则和模板
```

### 快速开始

复制规则入口：

```bash
cp rules/AGENTS.md your-project/AGENTS.md
```

复制所需 Skill 层：

```bash
cp -r skills/core your-project/skills/
cp -r skills/governance your-project/skills/
cp -r skills/tech/vue your-project/skills/        # 示例
cp -r skills/tech/java-springboot your-project/skills/
```

复制文档模板：

```bash
cp -r docs/_templates your-project/docs/
```

验证本仓库：

```bash
py scripts/py/audit_methodology.py --project-root .
py scripts/py/score_ai_development_readiness.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
```

预览多工具适配输出：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -DryRun
```

### 核心工作流

```text
需求输入
  -> 读取规则和项目记忆
  -> 任务路由
  -> 安全拆批
  -> 使用现有工具和脚本执行
  -> 通过测试、API、浏览器或审计验证
  -> 回写证据和结论
  -> 将重复问题进化为规则或 Skill
```

### 多工具适配

当前适配层支持：

- Codex
- Claude Code
- Trae
- Qoder / Qoder CN
- Cursor
- GitHub Copilot / VS Code
- Windsurf、Cline、Roo Code、Aider、Continue.dev 等实验适配

详见 [docs/TOOL_ADAPTERS.md](docs/TOOL_ADAPTERS.md) 和 [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)。

### 开源边界

本仓库只开源可迁移的方法论、规则、Skill、模板、审计脚本和适配器生成器。私有商业策略、过程记录、未脱敏案例、原始素材和本地工具状态不属于开源范围。

公开前检查：

```bash
py scripts/py/check_open_source_boundary.py --project-root .
```

边界文档：

- [docs/公开材料/OPEN_SOURCE_PACKAGE.md](docs/公开材料/OPEN_SOURCE_PACKAGE.md)
- [docs/公开材料/OPEN_SOURCE_READINESS.md](docs/公开材料/OPEN_SOURCE_READINESS.md)
- [docs/全项目总控/DISCLOSURE_BOUNDARY.md](docs/全项目总控/DISCLOSURE_BOUNDARY.md)

### 社区与贡献

- 问题、想法和工具适配讨论：GitHub Discussions
- 可复现缺陷和文档错误：GitHub Issues
- 代码、规则、Skill、适配器修改：Pull Request

贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。所有 PR 必须通过方法论审计、开源边界检查和适配器 dry-run。

### 当前状态

- 38 个 verified official skills
- Methodology audit: PASS, 0 failures, 0 warnings
- AI development readiness: 100/100, L4 可进化
- 多工具适配器注册表 v2
- 开源边界已文档化

### 协议

本仓库公开发布内容采用 [Apache License 2.0](LICENSE)。

注意：Apache-2.0 适用于本仓库中已经公开提交的代码、规则、文档模板和方法论材料；未提交到本仓库的私有商业策略、未脱敏案例、过程记录和本地素材不属于本开源发布范围。

---

## English

### What It Is

Enterprise AI Development OS is a portable operating layer for AI coding tools. It organizes project rules, skill units, documentation memory, audit gates, verification scripts, and multi-tool adapters into one coherent system so tools such as Codex, Claude Code, Trae, Qoder, Cursor, GitHub Copilot, and VS Code can work more consistently on large projects.

It is not just a prompt and not merely a traditional skill pack. It is closer to an AI development operating system: a shared entrypoint, routing layer, capability scheduler, evidence writeback loop, and evolution mechanism for controlled AI-assisted engineering.

### Why It Exists

AI coding tools are powerful, but enterprise-grade projects need more than code generation:

- persistent project memory across sessions
- rules loaded before code changes
- task routing and decomposition
- reusable capability units
- verification before "done"
- documentation writeback and evidence chains
- repeated mistakes converted into stronger rules or skills
- consistent behavior across multiple AI coding tools

This repository packages those practices into a tool-agnostic methodology and adapter framework.

### What Is Included

| Layer | Purpose |
|---|---|
| Rules | Session startup, execution order, file placement, verification gates |
| Skills | Capability units for planning, architecture, governance, frontend, backend, data, testing, and deployment |
| Documentation memory | Backlog, master index, templates, ADRs, writeback structure |
| Audit gates | Methodology audit, open-source boundary check, readiness scoring |
| Tool adapters | Deployment helpers for syncing rules and skills into AI coding tools |
| Evolution loop | Guidance for turning repeated failures into reusable capability |

### Repository Layout

```text
AGENTS.md                 Main rule entrypoint
CLAUDE.md                 Claude Code rule entrypoint
rules/                    Portable rule source
skills/                   Official skill source
methodology/              Methodology whitepapers
docs/_templates/          Documentation templates
docs/全项目总控/           Master index, disclosure boundary, delivery loop
docs/公开材料/             Public release boundary and readiness notes
docs/TOOL_ADAPTERS.md     Multi-tool adapter matrix and deploy contract
scripts/py/               Audit, scoring, environment, and tool-discovery scripts
scripts/js/               CLI entrypoint
tools/                    Adapter registry and deployment script
lite/                     Lite rules and templates
site/                     GitHub Pages website
```

### Quick Start

Copy the rule entrypoint:

```bash
cp rules/AGENTS.md your-project/AGENTS.md
```

Copy the skill layers you need:

```bash
cp -r skills/core your-project/skills/
cp -r skills/governance your-project/skills/
cp -r skills/tech/vue your-project/skills/        # example
cp -r skills/tech/java-springboot your-project/skills/
```

Copy documentation templates:

```bash
cp -r docs/_templates your-project/docs/
```

Verify this repository:

```bash
py scripts/py/audit_methodology.py --project-root .
py scripts/py/score_ai_development_readiness.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
```

Preview multi-tool adapter output:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -DryRun
```

### Core Workflow

```text
Requirement
  -> Read rules and project memory
  -> Route the task
  -> Decompose into safe batches
  -> Execute with existing tools and scripts
  -> Verify with tests, API checks, browser checks, or audits
  -> Write back evidence and decisions
  -> Evolve rules or skills when patterns repeat
```

### Tool Adapters

Current adapter coverage includes:

- Codex
- Claude Code
- Trae
- Qoder / Qoder CN
- Cursor
- GitHub Copilot / VS Code
- Experimental adapters for Windsurf, Cline, Roo Code, Aider, Continue.dev, and others

See [docs/TOOL_ADAPTERS.md](docs/TOOL_ADAPTERS.md) and [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md).

### Open-Source Boundary

This repository only publishes portable methodology assets, rules, skills, templates, audit scripts, and adapter generators. Private commercialization notes, process records, unredacted case studies, raw source archives, and local tool state are outside the open-source scope.

Before publishing or pushing changes, run:

```bash
py scripts/py/check_open_source_boundary.py --project-root .
```

Boundary documents:

- [docs/公开材料/OPEN_SOURCE_PACKAGE.md](docs/公开材料/OPEN_SOURCE_PACKAGE.md)
- [docs/公开材料/OPEN_SOURCE_READINESS.md](docs/公开材料/OPEN_SOURCE_READINESS.md)
- [docs/全项目总控/DISCLOSURE_BOUNDARY.md](docs/全项目总控/DISCLOSURE_BOUNDARY.md)

### Community And Contributions

- Questions, ideas, and adapter discussions: GitHub Discussions
- Reproducible bugs and documentation errors: GitHub Issues
- Code, rules, skills, and adapter changes: Pull Requests

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing. All PRs must pass methodology audit, open-source boundary checks, and adapter dry-run.

### Status

- 38 verified official skills
- Methodology audit: PASS, 0 failures, 0 warnings
- AI development readiness: 100/100, L4 evolvable
- Multi-tool adapter registry v2
- Public/private disclosure boundary documented

### License

The public contents of this repository are licensed under the [Apache License 2.0](LICENSE).

Note: Apache-2.0 applies to the code, rules, documentation templates, and methodology materials committed to this public repository. Private commercialization notes, unredacted case studies, process records, and local source archives that are not committed to this repository are not part of this open-source release.
