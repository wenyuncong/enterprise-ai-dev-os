# 全 AI 原生开发白皮书 | Full AI-Native Development Whitepaper

> 阅读优化说明：本文件为早期双语混排稿。正式外发建议优先使用同目录下的中文独立版 `FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_CN.md` 或英文独立版 `FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_EN.md`。
> Reading note: this is an earlier mixed bilingual draft. For external sharing, prefer `FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_CN.md` or `FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_EN.md`.

> 版本：Draft 1.0  
> 日期：2026-08-09  
> 公开边界：本文为可外发版本，不包含客户名称、仓库路径、本机路径、私有运行证据或未经验证的固定收益数字。  
> Language: Chinese first, English second.

## 0. 摘要 | Executive Summary

全 AI 原生开发不是让软件项目里堆叠更多大模型、更多智能体或更多提示词。它是一套面向 AI 协作时代的软件开发标准：让软件系统从设计之初就具备可被 AI 理解、调用、治理、验证和进化的结构。

这套标准的核心价值不是替代人，而是重新分工：人负责想法、目标、业务判断和最终验收；AI 与智能体负责在标准约束下完成代码、方案、创意实现和重复性工程执行；runtime 负责真相、权限、状态、证据和风险边界；门控和测试负责把“看起来完成”变成“可以复核”。

因此，全 AI 原生开发的目标不是更快生成代码，而是让 AI 生成的代码、流程和能力可以进入真实业务系统，并保持可控、可验、可演进。

Full AI-Native Development is not about adding more large language models, more agents, or more prompts into a software project. It is a development standard for the age of AI collaboration: software should be designed from the beginning to be understandable, callable, governable, verifiable, and evolvable by AI.

The core value is not replacing humans, but redefining collaboration. Humans own ideas, goals, business judgment, and final acceptance. AI and agents implement code, solutions, creative variations, and repetitive engineering work under a governed standard. The runtime owns truth, permission, state, evidence, and risk boundaries. Gates and tests turn "it looks done" into "it can be reviewed and trusted".

The goal is not merely faster code generation. The goal is to let AI-generated code, workflows, and capabilities enter real business systems while remaining controlled, verifiable, and evolvable.

## 1. 起点：为什么普通 AI 编程会失控 | Why Ordinary AI Coding Loses Control

AI 编程工具可以快速生成代码、页面、接口、文档和测试，但在复杂业务系统中，速度并不等于交付能力。缺少统一标准时，常见问题会反复出现：

- 文档很多，但没有统一真相源，AI 不知道哪个规则优先。
- 代码增长很快，但架构边界不清，登录、权限、状态、数据回写等基础能力容易反复出错。
- 前端、后端、脚本、文档各自生成，最后彼此不一致。
- AI 会根据旧上下文、局部文件或错误记忆直接修改代码，导致问题被放大。
- 功能看似完成，但缺少可复核的测试、API、浏览器、日志或业务流证据。
- 多个 AI 工具协作时，每个工具都有自己的上下文和习惯，项目规则无法稳定继承。

这说明企业级 AI 开发的核心问题不是“AI 会不会写代码”，而是“AI 在什么结构内写代码、调用能力、留下证据、接受治理”。

AI coding tools can quickly generate code, pages, APIs, documentation, and tests. In complex business systems, however, speed is not the same as delivery capability. Without a shared standard, recurring problems appear:

- Documentation exists, but there is no single source of truth for AI to follow.
- Code grows quickly, but architecture boundaries remain unclear. Authentication, authorization, state transitions, and data writeback can repeatedly fail.
- Frontend, backend, scripts, and documents are generated separately and drift apart.
- AI may edit code based on stale context, partial files, or wrong memory, amplifying mistakes.
- A feature may look complete, but lacks test, API, browser, log, or business-flow evidence.
- Multiple AI tools each carry different context and habits, so project rules cannot be inherited reliably.

This shows that the core enterprise AI development problem is not "can AI write code". The real question is: within what structure does AI write code, call capabilities, leave evidence, and accept governance?

## 2. 核心定义 | Core Definition

全 AI 原生开发是一套让软件系统从设计之初具备 AI 协作能力的开发标准。它要求系统中的业务事实、服务能力、编排流程、操作入口、界面承载、运行时治理和验证证据都可以被 AI 读取、解释、调用、审计和持续改进。

简化定义：

```text
全 AI 原生开发 =
让软件生来具备可被 AI 理解、调用、治理、验证和进化的结构。
```

它不是：

- 不是简单使用 AI IDE。
- 不是提示词工程的堆叠。
- 不是让智能体直接绕过业务系统执行动作。
- 不是把所有代码都交给大模型自由发挥。
- 不是宣称 AI 可以替代产品负责人、业务负责人或最终验收人。

它是：

- 一套开发标准。
- 一套架构约束。
- 一套治理机制。
- 一套证据闭环。
- 一套让 AI 能稳定参与真实软件交付的工程方法。

Full AI-Native Development is a development standard that makes software systems AI-collaboration-ready from the beginning. It requires business facts, service capabilities, orchestration flows, action entrances, host surfaces, runtime governance, and verification evidence to be readable, explainable, callable, auditable, and improvable by AI.

Short definition:

```text
Full AI-Native Development =
software designed to be understandable, callable, governable, verifiable, and evolvable by AI.
```

It is not:

- Merely using an AI IDE.
- A pile of prompt engineering tricks.
- Allowing agents to bypass business systems.
- Giving all code to a model without constraints.
- Claiming that AI replaces product owners, business owners, or final human acceptance.

It is:

- A development standard.
- An architecture discipline.
- A governance mechanism.
- An evidence loop.
- An engineering method that lets AI participate in real software delivery reliably.

## 3. 认知演进：解释、标准、发挥 | Cognitive Evolution: Explain, Standardize, Amplify

全 AI 原生开发的认知演进可以概括为三步：

```text
解释 -> 标准 -> 发挥
```

第一阶段是解释。人把业务想法、目标、例子、截图、验收结果交给 AI，AI 尝试把它解释成需求、任务和代码。

第二阶段是标准。系统把解释过程沉淀为可复用的规则、技能、文档结构、注册表、网关、runtime 和验证门禁。AI 不再靠临时理解工作，而是在结构内工作。

第三阶段是发挥。当标准稳定后，AI 与智能体获得更大的发挥空间。它们可以实现代码、生成方案、编排流程、提出优化建议，但所有动作都经过注册、权限、状态、证据和验收。

This cognitive evolution can be summarized as:

```text
Explain -> Standardize -> Amplify
```

The first stage is explanation. Humans provide business ideas, goals, examples, screenshots, and acceptance results. AI tries to translate them into requirements, tasks, and code.

The second stage is standardization. The system turns repeated explanation into reusable rules, skills, documentation structures, registries, gateways, runtime mechanisms, and verification gates. AI no longer relies on temporary understanding. It works inside a structure.

The third stage is amplification. Once the standard is stable, AI and agents gain more room to act. They can implement code, generate solutions, compose workflows, and suggest improvements. Every action still passes through registration, permission, state checks, evidence, and acceptance.

## 4. 参考架构 | Reference Architecture

全 AI 原生开发建议将能力链路拆成两条主线：后端真相链和前端承载链。

后端真相链：

```text
truth
-> atomic service
-> orchestration
-> aggregate interface
-> command gateway
-> adapters
-> Host / AI / MCP / OpenAPI
```

前端承载链：

```text
runtime / field truth
-> UI atom
-> UI orchestration
-> standard template
-> Host page
```

这两条链路的关键点是：业务真相、字段真相、权限真相、状态迁移和写入动作必须由后端和 runtime 管理。Host 页面、App、AI 客户端、MCP 客户端和 OpenAPI 客户端只加载、展示、收集输入、请求命令和展示反馈，不应成为第二套业务逻辑。

Full AI-Native Development separates capability delivery into two main chains: the backend truth chain and the frontend host chain.

Backend truth chain:

```text
truth
-> atomic service
-> orchestration
-> aggregate interface
-> command gateway
-> adapters
-> Host / AI / MCP / OpenAPI
```

Frontend host chain:

```text
runtime / field truth
-> UI atom
-> UI orchestration
-> standard template
-> Host page
```

The key principle is this: business truth, field truth, permission truth, state transitions, and write actions must be owned by the backend and runtime. Host pages, apps, AI clients, MCP clients, and OpenAPI clients load, render, collect input, request commands, and display feedback. They must not become a second source of business logic.

## 5. 核心对象 | Core Objects

| 中文对象 | English Object | 核心职责 |
|---|---|---|
| 真相源 | Source of Truth | 定义业务事实、字段、权限、状态和数据归属 |
| 原子服务 | Atomic Service | 承载最小稳定业务能力 |
| 原子编排 | Atomic Orchestration | 把多个原子组合成业务流程 |
| 聚合接口 | Aggregate Interface | 向 Host、AI、MCP 提供可理解的业务能力画像 |
| 命令网关 | Command Gateway | 作为唯一动作入口，处理权限、状态、幂等、审计和风险 |
| 注册表 | Registry | 登记能力、版本、状态、提供方、权限和可调用边界 |
| Host | Host Surface | 加载和展示聚合接口，收集输入并调用命令网关 |
| Runtime | Runtime | 执行标准、维护真相、记录证据、管理风险和演进 |
| 证据闭环 | Evidence Loop | 用测试、日志、API、浏览器和业务流证明结果 |

| Chinese Object | English Object | Responsibility |
|---|---|---|
| 真相源 | Source of Truth | Defines business facts, fields, permissions, state, and ownership |
| 原子服务 | Atomic Service | Holds the smallest stable business capability |
| 原子编排 | Atomic Orchestration | Composes atoms into business workflows |
| 聚合接口 | Aggregate Interface | Provides AI-readable and Host-ready capability profiles |
| 命令网关 | Command Gateway | The only action entrance for permission, state, idempotency, audit, and risk checks |
| 注册表 | Registry | Records capabilities, versions, status, providers, permissions, and callable boundaries |
| Host | Host Surface | Loads aggregate interfaces, renders UI, collects input, and calls the command gateway |
| Runtime | Runtime | Executes the standard, maintains truth, records evidence, manages risk and evolution |
| 证据闭环 | Evidence Loop | Proves results through tests, logs, APIs, browser checks, and business-flow evidence |

## 6. AI 治理不是限制，而是放大空间 | AI Governance Amplifies Capability

传统语境中的治理常被理解为限制、审批和阻碍。但在全 AI 原生开发中，治理的目的不是压制 AI，而是让 AI 可以在更大的空间中安全发挥。

治理通过以下方式扩大 AI 的可用范围：

- 用规则说明项目边界，让 AI 不必每次重新猜测。
- 用 Skill 封装高频任务，让 AI 能复用成熟路径。
- 用注册表告诉 AI 哪些能力存在、由谁提供、是否可执行。
- 用命令网关保证所有动作通过同一入口。
- 用 runtime 记录状态、权限、证据和风险。
- 用门控脚本和测试把经验转成可复核标准。
- 用文档回写和技能进化把重复问题沉淀为长期能力。

因此，治理的本质是：给 AI 定义一个可发挥、可追踪、可恢复、可升级的空间。

In traditional contexts, governance is often seen as restriction, approval, and friction. In Full AI-Native Development, governance does not suppress AI. It gives AI a larger and safer space to act.

Governance expands AI capability by:

- Using rules to define project boundaries so AI does not guess every time.
- Packaging recurring tasks into skills so AI can reuse mature paths.
- Using registries to tell AI which capabilities exist, who provides them, and whether they are executable.
- Using command gateways to ensure all actions pass through one controlled entrance.
- Using runtime to record state, permission, evidence, and risk.
- Turning repeated experience into reviewable standards through gates and tests.
- Feeding documentation writeback and skill evolution into long-term capability.

Governance defines a space where AI can act, be traced, recover from errors, and evolve.

## 7. 人、AI、Runtime 的分工 | Human, AI, and Runtime Responsibilities

全 AI 原生开发不是“人退出开发”，而是让人从代码细节中上移到意图、业务判断和验收。

| 角色 | 负责 | 不负责 |
|---|---|---|
| 人 | 目标、业务结果、优先级、取舍、最终验收 | 手工定位所有代码、重复执行机械验证 |
| AI / 智能体 | 需求分析、方案生成、代码实现、测试补充、文档提炼 | 擅自定义业务政策、绕过治理执行高风险动作 |
| Runtime | 真相、状态、权限、证据、风险、执行边界 | 替代人的商业判断 |
| 门控 / 测试 | 可复核证据、回归保护、发布前检查 | 替代真实业务验收 |

Full AI-Native Development does not remove humans from development. It moves humans upward from code details to intent, business judgment, and acceptance.

| Role | Owns | Does Not Own |
|---|---|---|
| Human | Goals, business results, priorities, trade-offs, final acceptance | Manually locating every code file or repeating mechanical verification |
| AI / Agent | Requirement analysis, solution generation, code implementation, test support, documentation extraction | Inventing business policy or bypassing governance for high-risk actions |
| Runtime | Truth, state, permission, evidence, risk, execution boundaries | Replacing human business judgment |
| Gates / Tests | Reviewable evidence, regression protection, pre-release checks | Replacing real business acceptance |

## 8. 来自复杂 ERP 实战的启示 | Lessons From Complex ERP Practice

全 AI 原生开发标准来自复杂企业业务系统的长期实践。ERP 是天然的高压场景：它包含登录认证、权限、多租户、字段体系、采购、销售、库存、资金、审批、消息、打印、报表、版本、发布和回退。仅靠“让 AI 多写代码”无法稳定交付这样的系统。

实践中的关键启示包括：

- 前端只负责加载和展示，业务计算、权限、状态和写入必须由后端和 runtime 决定。
- 字段、页面、按钮、动作、权限不能散落在多个页面中，应由字段包、业务画像、注册表和 runtime profile 提供。
- 可执行动作不能因为界面上有按钮就可执行，必须通过命令网关进行状态、权限、幂等和审计检查。
- 聚合接口应向 Web、App、AI、MCP 和 OpenAPI 提供同一份能力画像，减少多端重复逻辑。
- 发生重复错误后，应升级规则、Skill、脚本、测试或文档，而不是只在一次对话中修补。
- 删除、迁移、发布、数据库变更、生产动作等高风险操作必须有明确边界、证据和确认机制。

这些实践说明，全 AI 原生开发不是理论装饰，而是从真实业务压力中反向提炼出来的工程标准。

The standard is derived from long-term practice in complex enterprise business systems. ERP is a high-pressure environment by nature. It includes authentication, authorization, multi-tenancy, fields, purchasing, sales, inventory, capital, approval, notifications, printing, reports, versions, release, and rollback. Simply asking AI to write more code cannot reliably deliver such a system.

Key lessons include:

- The frontend should load and render. Business calculation, permission, state, and writeback must be decided by the backend and runtime.
- Fields, pages, buttons, actions, and permissions should not be scattered across pages. They should come from field packages, business profiles, registries, and runtime profiles.
- An action is not executable just because a button exists. It must pass command gateway checks for state, permission, idempotency, and audit.
- Aggregate interfaces should provide the same capability profile to Web, App, AI, MCP, and OpenAPI surfaces.
- Repeated errors should become stronger rules, skills, scripts, tests, or documents instead of being patched only in one conversation.
- Deletion, migration, release, database changes, and production actions must have clear boundaries, evidence, and confirmation mechanisms.

These lessons show that Full AI-Native Development is not theoretical decoration. It is an engineering standard extracted from real business pressure.

## 9. 商业价值 | Business Value

全 AI 原生开发的商业价值不应被表述为固定比例的效率提升，而应表述为可验证的方向性收益：

- 减少重复解释：项目规则、Skill 和文档结构让 AI 更快进入上下文。
- 减少返工：门控、测试、运行验证和回归规则在更早阶段发现问题。
- 降低人员依赖：知识不只停留在个人脑中或聊天记录里，而是沉淀为标准资产。
- 支持多端复用：Web、App、AI、MCP 和 OpenAPI 共享后端聚合接口和命令网关。
- 提高交付可审计性：每个关键动作都能留下证据、状态和责任边界。
- 支持持续进化：重复问题可以升级为规则、Skill、脚本、测试和 runtime 能力。

The business value should not be described as a fixed efficiency percentage before benchmark evidence exists. It should be described as measurable directional value:

- Fewer repeated explanations: rules, skills, and documentation structures help AI enter context faster.
- Less rework: gates, tests, runtime checks, and regression rules expose problems earlier.
- Lower dependency on individual memory: knowledge becomes standard assets instead of staying in personal memory or chat history.
- Multi-surface reuse: Web, App, AI, MCP, and OpenAPI share backend aggregate interfaces and command gateways.
- Better auditability: key actions leave evidence, state, and responsibility boundaries.
- Continuous evolution: repeated issues become rules, skills, scripts, tests, and runtime capabilities.

## 10. 边界与非主张 | Boundaries and Non-Claims

为了保持可信，公开表达应避免以下误解：

- 不宣称 AI 可以完全替代人类产品判断。
- 不宣称零缺陷、固定节省比例或固定通过率。
- 不把数字生命解释为已有意识。
- 不把训练自有大模型作为当前标准的必要条件。
- 不把特定工具、模型或供应商作为标准前提。
- 不把大型 ERP 私有细节、客户数据、本机路径或未脱敏证据对外发布。

正确表述应是：

```text
全 AI 原生开发是一套工程标准。
它让 AI 在可治理结构内发挥能力，而不是让 AI 无边界地替代所有角色。
```

To remain credible, public communication should avoid these misunderstandings:

- Do not claim that AI fully replaces human product judgment.
- Do not claim zero defects, fixed savings, or fixed pass rates without benchmark evidence.
- Do not describe digital life as proven consciousness.
- Do not make training a proprietary foundation model a prerequisite of the current standard.
- Do not make any specific AI tool, model, or vendor a prerequisite.
- Do not publish private ERP details, customer data, local paths, or unredacted evidence.

The correct statement is:

```text
Full AI-Native Development is an engineering standard.
It lets AI act inside a governable structure instead of replacing all roles without boundaries.
```

## 11. 路线图 | Roadmap

全 AI 原生开发可以分阶段落地：

| 阶段 | 目标 |
|---|---|
| S0 人工辅助 | 使用 AI 工具生成代码和文档，但缺少统一标准 |
| S1 规则化 | 建立项目规则、目录边界、开发顺序和基础验证 |
| S2 Skill 化 | 把高频任务沉淀为可复用 Skill、模板和检查脚本 |
| S3 架构原生 | 建立真相源、原子服务、编排、聚合接口、命令网关和 Host |
| S4 Runtime 治理 | 通过 runtime 管理权限、状态、证据、风险和多端调用 |
| S5 可进化系统 | 重复问题自动沉淀为规则、原子、测试、Skill 或治理策略 |

Full AI-Native Development can be adopted in stages:

| Stage | Goal |
|---|---|
| S0 AI-assisted | Use AI tools to generate code and documents without a shared standard |
| S1 Rule-based | Establish project rules, directory boundaries, development order, and basic verification |
| S2 Skill-based | Package recurring tasks into reusable skills, templates, and check scripts |
| S3 Architecture-native | Establish truth sources, atomic services, orchestration, aggregate interfaces, command gateways, and Hosts |
| S4 Runtime-governed | Use runtime to manage permission, state, evidence, risk, and multi-surface invocation |
| S5 Evolvable system | Convert repeated issues into rules, atoms, tests, skills, or governance policies |

## 12. 对外一句话 | One-Sentence External Positioning

中文：

> 全 AI 原生开发不是让 AI 多写代码，而是用标准化的软件结构，让 AI 能稳定理解、调用、治理、验证和进化真实业务系统。

English:

> Full AI-Native Development is not about making AI write more code. It is about standardizing software structure so AI can reliably understand, call, govern, verify, and evolve real business systems.
