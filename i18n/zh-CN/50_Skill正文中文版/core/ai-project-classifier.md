# `ai-project-classifier` — 项目分类决策框架

> **源文件**：skills/core/ai-project-classifier/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-project-classifier
description: "Classify projects by origin, quality target, deployment targets, and scale to choose the correct methodology path and skill set. Use at project start, during onboarding, or before applying the methodology to a new or existing codebase."
```

**中文描述**：按项目来源（origin）、质量目标（quality target）、部署目标（deployment targets）与规模（scale）对项目分类，以选择正确的方法论路径与 Skill 集。在项目启动、接手（onboarding）时使用，或在对新项目（greenfield）/存量项目（brownfield）代码库套用方法论之前使用。

---

## Rule | 规则

分类必须确定：1）主领域（code/docs/devops/security/data/governance）；2）复杂度层级（simple/medium/complex）；3）风险级别（low/medium/high/critical）；4）所需 Skill；5）执行策略。**禁止未分类就执行。**

## Purpose | 目的

在项目起始阶段，沿四个关键维度对每个项目分类。这决定了加载哪些 Skill、使用哪种架构、遵循哪些步骤，以及“完成（done）”意味着什么。

**它解决的问题**：没有显式分类，方法论会对一个 1 天的原型和一个 6 个月的企业级系统套用同一套规则。这会造成小项目过度工程（over-engineering）、大项目工程不足（under-engineering）。

## Trigger | 触发条件

- 开始一个项目时，**ALWAYS（始终）**先于任何其他 Skill 运行
- 用户说“新项目”“开始构建”“创建一个应用”时
- 首次遇到一个存量项目时
- 项目范围发生显著变化时

---

## Classification Flow | 分类流程

```
                 ┌──────────────────┐
                 │  Project Start   │
                 └────────┬─────────┘
                          │
              ┌───────────▼───────────┐
              │ DIMENSION 1:          │
              │ Brownfield or         │
              │ Greenfield?           │
              └───────────┬───────────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
     ┌──────▼──────┐ ┌───▼────┐        │
     │ Brownfield  │ │Greenfield       │
     │ (Existing)  │ │(New)            │
     └──────┬──────┘ └───┬────┘        │
            │             │             │
            │    ┌────────▼────────┐    │
            │    │ DIMENSION 2:    │    │
            │    │ Quality Target? │    │
            │    └────────┬────────┘    │
            │             │             │
            │   ┌─────────┼─────────┐   │
            │   │         │         │   │
            │ ┌─▼───┐ ┌──▼──┐ ┌───▼──┐ │
            │ │Rapid│ │AI-  │ │Enter-│ │
            │ │Proto│ │Native│ │prise │ │
            │ └──┬──┘ └──┬──┘ └──┬───┘ │
            │    │       │       │     │
            │    │  ┌────▼───────▼──┐  │
            │    │  │ DIMENSION 3: │  │
            │    │  │ Deployment   │  │
            │    │  │ Targets?     │  │
            │    │  └────┬─────────┘  │
            │    │       │            │
            │    │  ┌────▼────┐       │
            │    │  │DIM 4:   │       │
            │    │  │Scale?   │       │
            │    └──┤         │       │
            │       └─────────┘       │
            └─────────────────────────┘
```

---

## Dimension 1: Project Origin | 项目来源

### Brownfield (Existing Project) | 老项目（brownfield）

**识别标志**：已有 `package.json`、`.git`、数据库、现存代码结构

**做法**：

1. 先 READ 再 WRITE —— 先审计现有架构
2. 提炼模式（EXTRACT patterns）—— 记录当前约定，不强行施加新约定
3. 增量升级（UPGRADE incrementally）—— 每次只加一层方法论
4. 绝不破坏现有功能

**关键问题**：

- 当前已在使用什么框架/技术栈？
- 是否已有编码约定？
- 是否有需要尊重的数据库模式（Schema）？
- 是否有需要保护的既有用户/数据？

### Greenfield (New Project) | 新项目（greenfield）

**识别标志**：空目录、无代码、“从零开始”

**做法**：

1. 先按维度 2–4 分类
2. 依据分类结果搭脚手架
3. 从 Step 1 起套用完整方法论
4. 架构决策是全新的 —— 要审慎选择

---

## Dimension 2: Quality Target | 质量目标

### Rapid Prototype | 快速原型

**何时适用**：MVP、demo、概念验证（proof-of-concept）、周期 < 1 周、1–2 名开发者

**特征**：

- 单一代码库（可接受 monorepo）
- 一个数据库，模式（Schema）简单
- 测试最小化（只做冒烟测试）
- UI 优先开发（先快速做出可见的东西）
- 文档：最小化（README + API 清单）

**加载的 Skill**：仅 core 层 Skill（planner、decomposer、command-executor）

**遵循的步骤**：精简版 13-step（跳过深度架构，跳过 ADR）

**架构**：Archetype A（Single-Service）

### AI-Native (Production Quality) | AI-Native（生产质量）

**何时适用**：真实产品、用户会依赖它、周期 > 1 个月、2–5 名开发者

**特征**：

- 从第一天起就划清 atomic service 边界
- 完整测试覆盖（单元 + 集成 + 运行时验证）
- 接口优先设计（实现之前先定 OpenAPI/GraphQL）
- 文档：完整方法论文档
- 多平台就绪（web + 至少规划一个其他目标平台）

**加载的 Skill**：全部 core + governance 层 Skill

**遵循的步骤**：完整 13-step，全部门禁

**架构**：Archetype B（Atomic Services）

### Enterprise | 企业级

**何时适用**：多租户、有合规要求、有 SLA 承诺、团队 5 人以上

**特征**：

- 完整 atomic service 架构，配事件驱动编排
- 考虑多区域部署
- 安全审计、渗透测试
- HA/DR 策略
- 带部署门禁的完整 CI/CD 流水线

**加载的 Skill**：全部 Skill（core + governance + platform + tech）

**遵循的步骤**：完整 13-step + 部署门禁 + 安全扫描

**架构**：Archetype C（Multi-Platform）

---

## Dimension 3: Deployment Targets | 部署目标

| 部署目标 | 含义 |
|---|---|
| **Web only** | 标准 SPA/SSR、REST API |
| **Web + Mobile** | API 优先设计，考虑移动端 SDK |
| **Web + WeChat** | 微信认证适配器、`wx.request` 兼容 |
| **Web + MCP Server** | 在 REST 之外并行提供 MCP Tools 协议 |
| **All platforms** | 统一接口层，每个传输通道各自的适配器（adapter） |

**规则**：始终按“Web + 1 个额外目标平台”设计。前期多花 10% 成本，后期省下 90% 重写成本。

---

## Dimension 4: Scale | 规模

### Monolith/Modular Monolith | 单体 / 模块化单体

**何时适用**：用户 < 10K、API 端点 < 50、单一团队

**模式**：一个可部署单元，但模块边界清晰

**演进**：当任一模块的核心逻辑超过 500 行代码（LOC）时，把模块拆成服务

### Microservices | 微服务

**何时适用**：用户 > 10K、API 端点 > 50、多团队

**模式**：atomic service、事件驱动、独立部署

**前提要求**：必须投入监控、服务网格（service mesh）、分布式追踪

### Decision Rule | 决策规则

```
If (team_size == 1 && endpoints < 20) → Monolith
If (team_size >= 3 || endpoints >= 50) → Atomic Services
If (team_size >= 5 && compliance_required) → Enterprise Microservices
```

---

## Classification Output | 分类输出

每次项目启动都必须产出这份结论摘要：

```markdown
## Project Classification

| Dimension | Value | Rationale |
|---|---|---|
| Origin | Greenfield | New project, no existing code |
| Quality | AI-Native | Production SaaS, real users |
| Deploy Targets | Web + Mobile | Web SPA now, mobile within 3 months |
| Scale | Atomic Services | Team of 3, expecting 30+ endpoints |

### Implications
- Architecture: Archetype B (Atomic Services)
- Skills: All core + governance
- Steps: Full 13-step with all gates
- DB: Schema-per-service
- API: REST + GraphQL (OpenAPI-first)
- Mobile: React Native with same API
```

**分类结论模板字段中文对照**（字段名保持英文，照抄上方模板即可套用）：

| 字段 | 中文含义 | 填写要求 |
|---|---|---|
| `Dimension` | 维度 | 四行固定对应 `Origin`、`Quality`、`Deploy Targets`、`Scale`，不得增删 |
| `Value` | 取值 | 必须取源文件维度 1–4 中列出的受控值（如 `Greenfield`、`AI-Native`、`Web + Mobile`、`Atomic Services`） |
| `Rationale` | 依据 | 一句话写清为什么这样判定，须基于已核实事实，不得凭感觉 |
| `### Implications` | 影响面 | 至少写清架构原型、加载的 Skill、遵循的步骤；数据库/API/移动端按实际填写 |

---

## Integration | 集成

| 入口 | 动作 |
|---|---|
| `ai-chief-planner` Phase 1 | 任何规划之前先跑分类器 |
| `ai-rule-dispatcher` | 用分类结果选择 Skill 集 |
| `ai-architect-governor` | 用分类结果选择架构原型（archetype） |
| `ai-atomic-architect` | 依据 Quality Target 与 Scale 落地 |

---

## Guardrails | 防护规则

- **先分类再写码（Classify before you code）** —— 未分类，禁止开始实现
- **老项目（brownfield）≠ 无约束（free-for-all）** —— 现有代码有其约定，必须尊重
- **快速原型（Rapid Prototype）≠ 垃圾** —— 快速意味着更简单，不是更差
- **默认选 AI-Native** —— 不清楚时选 AI-Native（降级比升级容易）
- **范围变化时重新分类** —— 原型一旦变成产品，就需要重新分类

## Maturity | 成熟度

**Stage**：New —— 为填补项目起始阶段的决策空白而创建。

## Evolution History | 进化记录

- v1.0.0：首次创建 —— 4 个维度、3 个质量目标、分类输出模板

---

## 译注

1. **章节顺序**：源文件把 `## Rule` 放在 H1 标题之前（`## Rule` 在第 6 行，H1 在第 10 行）。中文版按本册固定结构把 H1 与元信息置顶，`## Rule` 紧随其后；各小节内容与相对顺序相对源文件不变，未删节、未合并。
2. **两套分类口径并存（源文件不一致）**：`## Rule` 要求确定 5 项判据（主领域、复杂度层级、风险级别、所需 Skill、执行策略），`## Purpose` 与正文却只讲 4 个维度（来源、质量目标、部署目标、规模）。源文件没有说明两套口径的关系，中文版按原文分别照译，未擅自统一，也未删去任一套。
3. **`13-step` 与现行 `13+1` 的口径漂移**：源文件在 Rapid Prototype / AI-Native 两处写 “13-step”。仓库 `AGENTS.md` 现为「强制开发顺序（13+1 Steps）」，即在 13 步之外增加 `Step 13a` 发布治理（仅 Enterprise 强制）；`methodology/` 下的正文文件名为 `03_13步开发执行引擎.md`。中文版按源文件保留 `13-step` 原样，不擅自改写；差异在此记录，待英文源更新时按同步规则第 6 节处理。
4. **原型命名不一致（源文件不一致）**：维度 2 用 `Archetype A (Single-Service)`、`Archetype B (Atomic Services)`、`Archetype C (Multi-Platform)`；维度 4 用 `Monolith`/`Modular Monolith`、`Microservices`；决策规则又引入 `Atomic Services`、`Enterprise Microservices`。源文件未给出维度 4 与 A/B/C 原型之间的显式映射，中文版不补造映射。
5. **`LOC` 未展开**：维度 4 的“核心逻辑超过 500 LOC”中，`LOC` 为 lines of code 的通用缩写，源文件未展开；译文在首次出现处补注“行代码”以便阅读，缩写本身原样保留。
6. **可能造成误解的示例值**：`## Classification Output` 模板中的 `React Native`、`GraphQL`、`Schema-per-service`、`Team of 3` 等均为示例值（模板用途），不是强制约定。中文版原样保留模板，未替换为其他技术栈。
7. **源版本**：源文件 frontmatter 只有 `name` 与 `description`，无版本号/日期标注，故记「未标注」；`## Evolution History` 的 v1.0.0 是 Skill 内容自身的演进记录，不等于源文件版本标注。
8. **无断链的文件/路径引用**：本文件提到的 `ai-chief-planner`、`ai-rule-dispatcher`、`ai-architect-governor`、`ai-atomic-architect` 四个 Skill 在仓库中均存在（`skills/core/` 下各自有 SKILL.md），`package.json`、`.git` 属“识别标志”而非引用，未发现指向不存在文件/路径的引用。
9. **门禁代号范围**：源文件未出现 `L0`–`L3`、`Q0`–`Q3`、`P0`–`P3` 代号，故译文无对应代号保留项，未补写未出现的代号。
10. **引用审计结论**：本 Skill 目录下只有 `SKILL.md` 一个文件，没有 `references/` 配套目录；正文对文件的引用仅为 `package.json`、`.git` 这类「识别标志」，**未发现断链引用**。作为对照：同层 `ai-task-decomposer` 与 `ai-rule-dispatcher` 各自带有未被正文引用的 `references/` 配套文件。
