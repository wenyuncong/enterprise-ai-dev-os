# 全 AI 原生开发标准详解 | Full AI-Native Development Standard

> 阅读优化说明：本文件为早期双语混排稿。正式外发建议优先使用同目录下的中文独立版 `FULL_AI_NATIVE_DEVELOPMENT_STANDARD_CN.md` 或英文独立版 `FULL_AI_NATIVE_DEVELOPMENT_STANDARD_EN.md`。
> Reading note: this is an earlier mixed bilingual draft. For external sharing, prefer `FULL_AI_NATIVE_DEVELOPMENT_STANDARD_CN.md` or `FULL_AI_NATIVE_DEVELOPMENT_STANDARD_EN.md`.

> 版本：Draft 1.0  
> 日期：2026-08-09  
> 适用范围：AI 辅助软件交付、企业级业务系统、AI-OS runtime、智能体能力治理、多端业务能力复用。  
> 公开边界：本文为标准解释稿，不包含私有仓库路径、客户数据、未脱敏证据或未经验证的收益数字。  
> Language: Chinese first, English second.

## 0. 标准定位 | Standard Positioning

全 AI 原生开发标准用于定义一种新的软件工程结构，使软件系统从设计之初就能被 AI 理解、调用、治理、验证和进化。

它不是某一个开发工具、某一个大模型、某一个框架，也不是单纯的提示词方法。它是一套跨工具、跨语言、跨业务系统的结构标准。

本标准的目标是：

1. 让人以业务语言提出目标、边界和验收。
2. 让 AI 能在可理解的结构内分析、实现、测试和交付。
3. 让 runtime 管理真相、权限、状态、证据和风险。
4. 让重复问题能沉淀为规则、Skill、脚本、原子、测试或治理策略。

Full AI-Native Development Standard defines a new software engineering structure. It makes software systems understandable, callable, governable, verifiable, and evolvable by AI from the beginning.

It is not a specific development tool, model, framework, or prompt method. It is a structural standard across tools, languages, and business systems.

The goals are:

1. Humans express goals, boundaries, and acceptance in business language.
2. AI analyzes, implements, tests, and delivers inside an understandable structure.
3. Runtime manages truth, permission, state, evidence, and risk.
4. Repeated issues become rules, skills, scripts, atoms, tests, or governance policies.

## 1. 规范词 | Normative Terms

本文使用以下规范词：

- 必须：违反后系统不符合全 AI 原生开发标准。
- 应该：默认应遵守，除非有明确理由和证据说明例外。
- 可以：允许的实现方式，但不是强制要求。
- 不得：明确禁止。

This document uses the following terms:

- MUST: required for conformance.
- SHOULD: recommended by default unless a justified exception exists.
- MAY: allowed but not required.
- MUST NOT: prohibited.

## 2. 总体结构 | Overall Structure

全 AI 原生开发的主链路如下：

```text
人类意图
-> 解释层
-> 标准层
-> AI 发挥层
-> Runtime 治理
-> 证据验证
-> 人类验收
-> 进化回写
```

工程实现链路如下：

```text
truth
-> atomic service
-> orchestration
-> aggregate interface
-> command gateway
-> registry
-> adapters
-> Host / AI / MCP / OpenAPI
-> evidence
-> evolution
```

The main collaboration chain is:

```text
human intent
-> explanation layer
-> standard layer
-> AI amplification layer
-> runtime governance
-> evidence verification
-> human acceptance
-> evolution writeback
```

The engineering chain is:

```text
truth
-> atomic service
-> orchestration
-> aggregate interface
-> command gateway
-> registry
-> adapters
-> Host / AI / MCP / OpenAPI
-> evidence
-> evolution
```

## 3. 标准对象定义 | Standard Object Definitions

### 3.1 人类意图 | Human Intent

人类意图是产品目标、业务结果、用户体验、优先级、非目标和最终验收标准的来源。

要求：

- 人必须负责最终业务判断。
- AI 可以补全需求草案，但不得替代人定义业务政策。
- 当业务含义不清时，AI 应该请求最小必要澄清。

Human intent is the source of product goals, business outcomes, user experience, priorities, non-goals, and final acceptance criteria.

Requirements:

- Humans MUST own final business judgment.
- AI MAY draft requirements but MUST NOT replace humans in defining business policy.
- When business meaning is unclear, AI SHOULD ask for the smallest necessary clarification.

### 3.2 解释层 | Explanation Layer

解释层把人的自然语言、截图、样例和验收描述转成可执行任务、场景、边界和风险。

要求：

- 必须记录业务目标、输入、输出、非目标和验收方式。
- 应该把模糊表达转成可验证描述。
- 不得把工程不确定性转嫁给业务负责人，让业务负责人去找代码文件。

The explanation layer converts natural language, screenshots, examples, and acceptance descriptions into executable tasks, scenarios, boundaries, and risks.

Requirements:

- It MUST record business goals, inputs, outputs, non-goals, and acceptance methods.
- It SHOULD convert vague descriptions into verifiable statements.
- It MUST NOT push engineering uncertainty back to the business owner as code-search work.

### 3.3 真相源 | Source of Truth

真相源是业务事实、字段、权限、状态和数据归属的权威来源。

要求：

- 每个业务事实必须有唯一权威来源。
- 字段、权限、状态、金额、库存、审批、写回等业务事实不得在多个客户端重复计算。
- 前端、AI 客户端、MCP 客户端和 OpenAPI 客户端只能消费真相，不得制造第二套真相。

The source of truth is the authoritative source for business facts, fields, permissions, state, and data ownership.

Requirements:

- Every business fact MUST have one authoritative owner.
- Fields, permissions, state, amounts, inventory, approval, and writeback MUST NOT be recalculated independently in multiple clients.
- Frontend, AI clients, MCP clients, and OpenAPI clients MUST consume truth instead of creating a second truth.

### 3.4 原子服务 | Atomic Service

原子服务是最小稳定业务能力单元。它应具备清晰输入、输出、权限、错误、证据和测试边界。

要求：

- 原子服务必须单一职责。
- 原子服务必须可独立测试。
- 原子服务不得依赖 Host 页面才能完成业务判断。
- 原子服务可以被多个编排、聚合接口或 adapter 复用。

An atomic service is the smallest stable business capability unit. It should have clear input, output, permission, error, evidence, and test boundaries.

Requirements:

- An atomic service MUST have a single responsibility.
- An atomic service MUST be independently testable.
- An atomic service MUST NOT depend on a Host page for business judgment.
- An atomic service MAY be reused by multiple orchestration flows, aggregate interfaces, or adapters.

### 3.5 原子编排 | Atomic Orchestration

原子编排把多个原子服务组合成业务流程，例如保存、审核、下推、记账、回退、通知和发布。

要求：

- 多步业务流程必须通过编排表达，而不是散落在客户端或页面中。
- 编排必须处理事务边界、失败回滚、补偿、幂等和证据。
- 编排不得绕过原子服务直接操作多个业务事实。

Atomic orchestration composes atomic services into business workflows such as save, approve, push-down, post, rollback, notify, and release.

Requirements:

- Multi-step business workflows MUST be expressed through orchestration, not scattered in clients or pages.
- Orchestration MUST handle transaction boundaries, failure rollback, compensation, idempotency, and evidence.
- Orchestration MUST NOT bypass atomic services to manipulate multiple business facts directly.

### 3.6 聚合接口 | Aggregate Interface

聚合接口是面向 Host、AI、MCP 和 OpenAPI 的业务能力画像。它不只是返回数据列表，还应返回字段、状态、动作、权限、提示、风险和可执行边界。

要求：

- 聚合接口必须以业务对象或业务流程为中心。
- 聚合接口应该返回客户端所需的可展示事实和可执行能力。
- 聚合接口不得绕过命令网关直接执行写入动作。
- 聚合接口应该让 AI 能理解当前对象能做什么、不能做什么、为什么。

An aggregate interface is a capability profile for Host, AI, MCP, and OpenAPI. It returns not only data, but also fields, state, actions, permissions, prompts, risks, and executable boundaries.

Requirements:

- An aggregate interface MUST be centered around a business object or workflow.
- It SHOULD return displayable facts and executable capabilities needed by clients.
- It MUST NOT bypass the command gateway to perform write actions.
- It SHOULD allow AI to understand what can be done, what cannot be done, and why.

### 3.7 命令网关 | Command Gateway

命令网关是唯一动作入口。任何会改变业务状态、数据、权限、文件、发布结果或外部系统的动作，都必须通过命令网关或等价治理入口。

要求：

- 写入动作必须经过命令网关。
- 命令网关必须检查权限、状态、幂等、风险、审计和证据策略。
- 命令网关必须支持明确失败原因。
- 高风险动作必须支持人工确认、dry-run、回滚或补偿机制。

The command gateway is the only action entrance. Any action that changes business state, data, permissions, files, releases, or external systems must pass through the command gateway or an equivalent governed entrance.

Requirements:

- Write actions MUST pass through the command gateway.
- The command gateway MUST check permission, state, idempotency, risk, audit, and evidence policy.
- The command gateway MUST return clear failure reasons.
- High-risk actions MUST support human confirmation, dry-run, rollback, or compensation mechanisms.

### 3.8 注册表 | Registry

注册表记录能力、版本、状态、提供方、权限、适配器、风险等级和调用边界。

要求：

- 可调用能力必须登记。
- 能力状态必须明确，例如 draft、supported、deferred、blocked、deprecated、retired。
- 注册表必须区分“存在”与“可执行”。
- AI 和 Host 应优先读取注册表，而不是猜测能力。

The registry records capabilities, versions, status, providers, permissions, adapters, risk levels, and invocation boundaries.

Requirements:

- Callable capabilities MUST be registered.
- Capability status MUST be explicit, such as draft, supported, deferred, blocked, deprecated, or retired.
- The registry MUST distinguish "exists" from "executable".
- AI and Hosts SHOULD read the registry instead of guessing capabilities.

### 3.9 Host | Host Surface

Host 是 Web、App、桌面端、AI 控制台、MCP 客户端或 OpenAPI 客户端的承载面。

要求：

- Host 负责加载、展示、收集输入、请求命令和展示反馈。
- Host 不得定义第二套业务状态机。
- Host 不得重复计算业务金额、库存、权限或审批状态。
- Host 应该使用标准模板和 UI 原子，避免每个页面各写一套逻辑。

A Host is a Web, App, desktop, AI console, MCP client, or OpenAPI surface.

Requirements:

- A Host loads, renders, collects input, requests commands, and displays feedback.
- A Host MUST NOT define a second business state machine.
- A Host MUST NOT recalculate business amounts, inventory, permissions, or approval state.
- A Host SHOULD use standard templates and UI atoms instead of page-local logic.

### 3.10 Runtime | Runtime

Runtime 是执行标准的底层架构。它负责真相、唯一、记忆、学习、状态、权限、证据、风险和演进。

要求：

- Runtime 必须维护执行状态和证据。
- Runtime 必须让能力调用可追踪。
- Runtime 应支持规则加载、Skill 调度、注册表查询、命令执行、证据记录和风险判断。
- Runtime 不得替代人的最终业务验收。

The runtime is the substrate that executes the standard. It manages truth, uniqueness, memory, learning, state, permission, evidence, risk, and evolution.

Requirements:

- Runtime MUST maintain execution state and evidence.
- Runtime MUST make capability invocation traceable.
- Runtime SHOULD support rule loading, skill routing, registry lookup, command execution, evidence recording, and risk judgment.
- Runtime MUST NOT replace final human business acceptance.

### 3.11 证据闭环 | Evidence Loop

证据闭环把任务结果变成可复核事实。

要求：

- 任务完成必须有证据。
- 证据可以来自测试、编译、API、浏览器、日志、数据库检查、截图、审计脚本或业务流回放。
- 证据必须说明验证范围和限制。
- 不得用“代码已写”替代“结果已验证”。

The evidence loop turns task results into reviewable facts.

Requirements:

- Task completion MUST include evidence.
- Evidence MAY come from tests, builds, APIs, browsers, logs, database checks, screenshots, audit scripts, or business-flow replay.
- Evidence MUST describe scope and limitations.
- "Code has been written" MUST NOT replace "result has been verified".

### 3.12 进化回写 | Evolution Writeback

进化回写把重复问题、有效经验和失败案例沉淀为长期资产。

要求：

- 重复问题应该升级为规则、Skill、脚本、测试、模板或治理策略。
- 经验回写必须可追溯。
- 进化不得直接修改核心能力而不经过治理。
- 学习结果应该先成为候选资产，再经验证后晋升。

Evolution writeback converts repeated issues, effective patterns, and failures into long-term assets.

Requirements:

- Repeated issues SHOULD become rules, skills, scripts, tests, templates, or governance policies.
- Experience writeback MUST be traceable.
- Evolution MUST NOT directly modify core capabilities without governance.
- Learning results SHOULD become candidate assets first and be promoted only after verification.

## 4. 标准要求清单 | Standard Requirements

| 编号 | 中文要求 |
|---|---|
| AI-NATIVE-01 | 系统必须定义业务真相源 |
| AI-NATIVE-02 | 前端和客户端不得成为业务逻辑真相源 |
| AI-NATIVE-03 | 可复用业务能力必须原子化 |
| AI-NATIVE-04 | 多步业务流程必须通过编排表达 |
| AI-NATIVE-05 | Host、AI、MCP、OpenAPI 应共享聚合接口 |
| AI-NATIVE-06 | 写入动作必须通过命令网关 |
| AI-NATIVE-07 | 可调用能力必须登记到注册表 |
| AI-NATIVE-08 | Runtime 必须记录状态、权限、风险和证据 |
| AI-NATIVE-09 | 任务完成必须有可复核证据 |
| AI-NATIVE-10 | 重复问题必须进入进化回写机制 |
| AI-NATIVE-11 | 高风险动作必须有确认、dry-run、回滚或补偿 |
| AI-NATIVE-12 | 公开材料必须脱敏，不得发布私有路径、客户数据或未验证指标 |

| ID | English Requirement |
|---|---|
| AI-NATIVE-01 | The system MUST define business truth owners |
| AI-NATIVE-02 | Frontends and clients MUST NOT become business truth owners |
| AI-NATIVE-03 | Reusable business capabilities MUST be atomic |
| AI-NATIVE-04 | Multi-step workflows MUST be expressed through orchestration |
| AI-NATIVE-05 | Hosts, AI, MCP, and OpenAPI SHOULD share aggregate interfaces |
| AI-NATIVE-06 | Write actions MUST pass through command gateways |
| AI-NATIVE-07 | Callable capabilities MUST be registered |
| AI-NATIVE-08 | Runtime MUST record state, permission, risk, and evidence |
| AI-NATIVE-09 | Task completion MUST include reviewable evidence |
| AI-NATIVE-10 | Repeated issues MUST enter an evolution writeback mechanism |
| AI-NATIVE-11 | High-risk actions MUST support confirmation, dry-run, rollback, or compensation |
| AI-NATIVE-12 | Public materials MUST be desensitized and avoid private paths, customer data, or unverified metrics |

## 5. 成熟度模型 | Maturity Model

| 等级 | 中文说明 | 典型状态 |
|---|---|---|
| S0 | AI 辅助编码 | 能用 AI 写代码，但项目规则不稳定 |
| S1 | 规则化交付 | 有项目规则、目录边界、开发顺序和基础验证 |
| S2 | Skill 化交付 | 高频任务沉淀为 Skill、模板和脚本 |
| S3 | 架构原生 | 具备真相源、原子服务、编排、聚合接口、命令网关和 Host |
| S4 | Runtime 治理 | runtime 管理权限、状态、风险、证据和多端调用 |
| S5 | 可进化系统 | 重复问题可自动或半自动沉淀为规则、原子、测试和治理策略 |

| Level | English Description | Typical State |
|---|---|---|
| S0 | AI-assisted coding | AI writes code, but project rules are unstable |
| S1 | Rule-based delivery | Project rules, directory boundaries, development order, and basic verification exist |
| S2 | Skill-based delivery | Recurring tasks become skills, templates, and scripts |
| S3 | Architecture-native | Truth owners, atomic services, orchestration, aggregate interfaces, command gateways, and Hosts exist |
| S4 | Runtime-governed | Runtime manages permission, state, risk, evidence, and multi-surface invocation |
| S5 | Evolvable system | Repeated issues become rules, atoms, tests, and governance policies automatically or semi-automatically |

## 6. 验收门禁 | Acceptance Gates

| 门禁 | 中文定义 |
|---|---|
| G0 静态一致性 | 文件、目录、规则、引用路径、注册表声明一致 |
| G1 构建一致性 | 后端、前端、脚本或模型包能通过基础构建 |
| G2 接口一致性 | API、聚合接口、命令网关、权限和返回结构可验证 |
| G3 运行一致性 | 浏览器、API、日志、数据库或业务流能证明真实运行 |
| G4 发布一致性 | 版本、tag、迁移、回退、部署证据和公开边界齐全 |

| Gate | English Definition |
|---|---|
| G0 Static consistency | Files, directories, rules, references, and registry declarations are consistent |
| G1 Build consistency | Backend, frontend, scripts, or model packages pass basic build checks |
| G2 Interface consistency | APIs, aggregate interfaces, command gateways, permissions, and response shapes are verified |
| G3 Runtime consistency | Browser, API, logs, database checks, or business-flow replay prove real runtime behavior |
| G4 Release consistency | Version, tag, migration, rollback, deployment evidence, and disclosure boundaries are complete |

## 7. 典型流程 | Typical Flow

中文流程：

```text
业务目标
-> 解释为场景、边界、验收
-> 查找真相源和已有能力
-> 选择或新增原子服务
-> 编排业务流程
-> 输出聚合接口
-> 注册可调用能力
-> 通过命令网关执行动作
-> Host / AI / MCP 展示或调用
-> 运行验证
-> 文档和 Skill 回写
```

English flow:

```text
business goal
-> explain into scenario, boundary, and acceptance
-> locate truth owner and existing capabilities
-> select or add atomic services
-> orchestrate workflow
-> expose aggregate interface
-> register callable capability
-> execute through command gateway
-> Host / AI / MCP renders or invokes
-> verify runtime
-> write back documents and skills
```

## 8. 反模式 | Anti-Patterns

| 反模式 | 为什么危险 |
|---|---|
| 前端计算业务事实 | 多端不一致，AI 无法知道真相 |
| 页面直接写状态 | 绕过权限、审计、回滚和状态机 |
| 能力未注册就调用 | AI 和 Host 只能猜测能力边界 |
| 只写代码不验证 | 无法证明结果是否真实可用 |
| 把聊天记录当长期知识库 | 下次会话无法稳定继承 |
| 重复问题只临时修补 | 系统不会进化，同类错误会再次出现 |
| 对外发布未脱敏材料 | 泄露路径、客户、证据或战略边界 |
| 用巨大数字替代证据 | 外部读者难以验证，可信度下降 |

| Anti-Pattern | Why It Is Dangerous |
|---|---|
| Frontend calculates business facts | Multi-surface inconsistency and unclear truth |
| Page directly writes state | Bypasses permission, audit, rollback, and state machine |
| Calling unregistered capabilities | AI and Hosts can only guess capability boundaries |
| Writing code without verification | Cannot prove the result works |
| Treating chat history as long-term knowledge | Future sessions cannot inherit it reliably |
| Patching repeated issues only once | The system does not evolve and errors repeat |
| Publishing unredacted materials | Leaks paths, customers, evidence, or strategy boundaries |
| Replacing evidence with large numbers | External readers cannot verify the claim and trust decreases |

## 9. 最小落地清单 | Minimum Adoption Checklist

一个项目要进入全 AI 原生开发的最小可用状态，至少应具备：

- 项目规则入口。
- 任务分类与路由规则。
- 真相源说明。
- 原子服务或等价业务能力边界。
- 聚合接口或等价能力画像。
- 命令网关或等价写入治理入口。
- 注册表或能力清单。
- Host 边界说明。
- 测试、脚本或运行证据。
- 文档回写和经验沉淀机制。
- 公开和私有材料边界。

A project reaches the minimum usable state when it has at least:

- Project rule entry.
- Task classification and routing rules.
- Source-of-truth description.
- Atomic services or equivalent business capability boundaries.
- Aggregate interfaces or equivalent capability profiles.
- Command gateway or equivalent governed write entrance.
- Registry or capability catalog.
- Host boundary description.
- Tests, scripts, or runtime evidence.
- Documentation writeback and experience capture.
- Public/private disclosure boundary.

## 10. 对外解释模板 | External Explanation Template

中文：

```text
我们定义的全 AI 原生开发，不是让 AI 替代所有开发者，
而是把软件系统设计成 AI 能理解、调用、治理、验证和进化的结构。

人负责业务目标和最终验收；
AI 负责在标准约束下完成实现和创意；
runtime 负责真相、权限、状态、证据和风险。

这样，AI 生成的能力才能进入真实业务系统，而不是停留在一次性代码生成。
```

English:

```text
Our definition of Full AI-Native Development is not replacing all developers with AI.
It is designing software systems to be understandable, callable, governable, verifiable, and evolvable by AI.

Humans own business goals and final acceptance.
AI implements and creates under the standard.
Runtime owns truth, permission, state, evidence, and risk.

This allows AI-generated capabilities to enter real business systems instead of remaining one-off code generation.
```

## 11. 结论 | Conclusion

全 AI 原生开发的关键不是“AI 更强”，而是“标准更清楚”。标准越清楚，AI 的发挥空间越大；证据越完整，系统越能持续演进；runtime 越稳定，AI 越能安全进入真实业务。

最终目标不是让人被替代，而是让人从重复工程细节中释放出来，把注意力放在想法、业务结果、审美、取舍和验收上。

The key to Full AI-Native Development is not "stronger AI", but "clearer standards". The clearer the standard, the larger the space for AI to act. The stronger the evidence, the more the system can evolve. The more stable the runtime, the safer AI can enter real business.

The final goal is not to replace humans. It is to free humans from repetitive engineering details and let them focus on ideas, business outcomes, taste, trade-offs, and acceptance.
