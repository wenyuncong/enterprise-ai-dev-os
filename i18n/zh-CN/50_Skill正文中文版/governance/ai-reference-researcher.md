# `ai-reference-researcher` — 参考驱动的开发研究引擎

> **源文件**：skills/governance/ai-reference-researcher/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-reference-researcher
description: "Research primary references, official docs, open-source implementations, and comparable systems before designing unfamiliar features. Use when the domain is new, standards may have changed, or implementation should follow proven external practice."
```

**中文描述**：在设计陌生功能之前，先研究一手参考资料、官方文档、开源实现与同类系统。适用于领域全新、标准可能已变化，或实现应当遵循已验证的外部成熟做法的场景。

---

## Rule | 规则

研究**必须**做到：1）先检索官方文档；2）找到权威范本（canonical examples）；3）对比多个来源；4）标注版本适用性；5）产出带引用的总结。**禁止**在没有出处的情况下声称"最佳实践"。

---

## Purpose | 目标

在陌生领域开发复杂功能之前，搜索、下载、分析并提炼最优质开源参考实现中的模式。这把"AI 凭训练数据猜"变成"AI 从真实生产代码学"。

**它解决的问题**：AI 的训练数据广而浅。面对专业领域（ERP 工作流、财务计算、供应链、权限系统、多租户 SaaS），AI 常常发明次优模式，因为它从未见过成熟系统实际是怎么做的。参考研究通过在写代码之前给 AI 提供具体、高质量的样例来修复这一点。

---

## When to Trigger | 触发条件

### MUST trigger when | 必须触发的场景

- 建设团队从未做过的领域（例如第一个薪酬模块、第一个 WMS）
- 设计复杂子系统（认证、多租户、工作流引擎、报表引擎）
- AI 已经做出 2 个以上错误的架构假设
- 用户说"我不确定这应该怎么做"或"帮我找个参考"

### SHOULD trigger when | 应当触发的场景

- 在 3 个以上相互竞争的库/框架之间做选择
- 为新的业务领域设计数据库 schema
- 新项目初始化（脚手架搭建之前）
- `ai-library-first` 找到多个候选库 —— 参考研究有助于挑出最好的那个

### SKIP when | 可以跳过的场景

- 简单 CRUD 功能
- 团队已有大量经验的领域
- 紧急 Bug 修复（时间敏感）
- 快速原型（Rapid Prototype，Archetype A）

---

## Research Workflow | 研究流程

```
┌──────────────────────────────────────────────────────────────┐
│  PHASE 1: SEARCH | 检索                                      │
│  在 GitHub/GitLab/npm/PyPI 检索该领域头部项目                │
├──────────────────────────────────────────────────────────────┤
│  PHASE 2: EVALUATE | 评估                                    │
│  按 stars、维护活跃度、架构对候选项目打分                    │
├──────────────────────────────────────────────────────────────┤
│  PHASE 3: DOWNLOAD | 下载                                    │
│  把最好的 1-2 个项目克隆到本地用于分析                       │
├──────────────────────────────────────────────────────────────┤
│  PHASE 4: EXTRACT | 提取                                     │
│  分析：架构、模式、命名、库选型、schema                      │
├──────────────────────────────────────────────────────────────┤
│  PHASE 5: APPLY | 应用                                       │
│  把结论整合进架构设计 + Skill 更新                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Search | 搜索

### Search Sources | 检索来源

| 来源 | 检索方式 | 最适用于 |
|---|---|---|
| **GitHub** | `site:github.com {domain} {language} stars:>100` | 全栈应用、框架、库 |
| **npm** | `npm search {keyword}` 或 `npmjs.com` | 前端库、Node.js 工具 |
| **Maven Central** | `mvnrepository.com` | Java 库、Spring Boot starter |
| **PyPI** | `pypi.org` | Python 工具、ML 库 |
| **Awesome Lists** | `site:github.com awesome {domain}` | 精选的最佳项目清单 |

### Search Strategy | 检索策略

```bash
# 示例：调研 "multi-tenant SaaS ERP"
1. Search: site:github.com "multi-tenant" erp spring-boot stars:>50
2. Search: site:github.com "saas" "multi-tenant" java architecture
3. Search: site:github.com awesome erp
4. 按具体功能检索: site:github.com "purchase order" workflow engine
```

---

## Phase 2: Evaluate | 评估

### Scoring Criteria (weighted) | 评分标准（加权）

| 标准 | 权重 | 检查什么 |
|---|---|---|
| **Stars** | 25% | >100 = 好，>1000 = 优秀 |
| **维护活跃度** | 30% | 最近提交 < 6 个月，issue 正在被关闭 |
| **架构质量** | 20% | 模块分离清晰、README 明确、模式有文档 |
| **代码质量** | 15% | 有测试、lint 通过、复杂度合理 |
| **领域相关性** | 10% | 与我们的具体需求有多接近？ |

### Evaluation Output | 评估输出

```markdown
| 项目 | Stars | 最近提交 | 架构质量 | 总分 | 结论 |
|---|---|---|---|---|---|
| repo-owner/project-a | 1.2K | 3 days ago | ⭐⭐⭐⭐⭐ | 92% | **SELECT（选用）** |
| repo-owner/project-b | 450 | 2 months ago | ⭐⭐⭐⭐ | 78% | 仅作参考 |
| repo-owner/project-c | 89 | 1 year ago | ⭐⭐ | 45% | 跳过 |
```

---

## Phase 3: Download | 下载

### Clone Strategy | 克隆策略

```bash
# 把选中的项目克隆到参考目录
mkdir -p reference/ && cd reference/
git clone --depth 1 https://github.com/repo-owner/project-a.git
```

**规则**：

- 使用 `--depth 1` 做浅克隆（省时间、省磁盘）
- 存放于 `reference/` 目录（git-ignored，不提交）
- **禁止**把参考代码提交进项目仓库
- 分析完成后删除（或保留作为持续参考）

---

## Phase 4: Extract | 提取

### What to Analyze | 分析哪些维度

| 维度 | 要找什么 | 输出 |
|---|---|---|
| **目录结构** | 模块如何组织？单仓（monorepo）还是多仓？ | 推荐目录结构 |
| **架构模式** | 服务如何切分？事件驱动？CQRS？ | 架构决策输入 |
| **数据库 schema** | 表命名、关系、索引策略 | Schema 设计模式 |
| **API 设计** | REST 还是 GraphQL、端点命名、版本化 | API 约定 |
| **库选型** | 用了哪些库？为什么用这些？ | 供 ai-library-first 使用的选型结论 |
| **命名约定** | 类/表/端点命名的一致模式 | 命名标准 |
| **错误处理** | 错误如何被结构化与传播？ | 错误处理模式 |
| **测试模式** | 用了什么测试框架？测试如何组织？ | 测试策略 |
| **配置** | 环境变量、功能开关如何管理？ | 配置模式 |

### Extraction Output Format | 提炼输出格式

```markdown
## 参考分析：[项目名]

### 提炼出的关键模式
1. **模块组织**：[描述 + 示例路径]
2. **服务边界**：[他们如何切分服务]
3. **数据库设计**：[观察到的表模式]
4. **库技术栈**：[关键库及其版本]

### 应当采纳的模式
- [模式 1]：[为什么它对我们好]
- [模式 2]：[为什么它对我们好]

### 应当规避的模式
- [反模式 1]：[它为什么会造成问题]

### 推荐的架构决策
- ADR 候选：[基于参考结论的决策]
```

---

## Phase 5: Apply | 应用

### Integration Points | 集成点

| Skill / 产物 | 参考研究如何输入 |
|---|---|
| `ai-atomic-architect` | 参考项目的架构模式 → 原子服务设计 |
| `ai-library-first` | 参考项目的库选型 → 更新库目录 |
| `ai-component-standardizer` | 参考项目的目录结构 → 脚手架模板 |
| `ai-project-classifier` | 领域复杂度评估 → 质量目标选择 |
| `ai-architect-governor` | 基于参考结论的 ADR |
| `ai-skill-evolver` | 新模式 → Skill 更新 |
| `docs/架构决策记录/` | 引用参考项目的 ADR |

---

## Domain-Specific Reference Targets | 领域参考目标

### ERP / Enterprise Systems | ERP / 企业系统

| 领域 | 检索关键词 | 预期收获 |
|---|---|---|
| 多租户 SaaS | `multi-tenant spring boot saas` | 租户隔离模式、schema-per-tenant 与共享 schema 之争 |
| 库存 / WMS | `warehouse management system open source` | 库存移动模式、条码、库位层级 |
| 会计 / 财务 | `open source accounting double-entry` | 总账模式、对账、期间关账 |
| CRM | `open source crm node.js` | 销售漏斗、线索管理、联系人层级 |
| 工作流引擎 | `workflow engine open source bpmn` | 状态机、审批链、流程定义 |

### General Architecture | 通用架构

| 领域 | 检索关键词 | 预期收获 |
|---|---|---|
| 微服务 | `microservices reference architecture java` | 服务边界、事件总线、API 网关 |
| 权限 / RBAC | `rbac permission system open source` | 角色层级、基于资源的鉴权、租户隔离 |
| 报表引擎 | `report engine open source` | 模板渲染、数据源抽象、导出 |
| 实时 | `websocket real-time dashboard open source` | 事件流、推送模式 |

---

## License Awareness | 许可证意识

**研究模式，禁止抄代码。** 参考代码的用途是学习模式，不是复制代码。

**复用边界**：可以参考实现思路并采纳其架构模式；**禁止**把参考项目的代码原样搬进本项目。凡不满足许可证条件的项目，一律只做阅读、不做复用。

| 许可证 | 可以研究？ | 可以复制？ |
|---|---|---|
| MIT / Apache 2.0 / BSD | ✅ 可以 | ✅ 需署名 |
| GPL / AGPL | ✅ 可以 | ⚠️ 仅当本项目同样采用 GPL |
| 专有 / 无许可证 | ❌ 跳过 | ❌ 绝不 |

**默认规则**：只研究 MIT、Apache 2.0、BSD 许可证的项目。

---

## Integration with Methodology | 方法论集成

```
Step 0: 项目分类
    │
    ├── 复杂领域？是 → Step 0a: 参考研究
    │     ├── 在 GitHub 检索前 3 个项目
    │     ├── 评估 → 下载最好的 1-2 个
    │     ├── 提炼模式 → 喂给架构类 Skill
    │     └── 应用结论
    │
    └── 简单领域？跳过（SKIP）

Step 1: 数据库初始化（依据参考项目的 schema 模式）
Step 2-12: 标准开发流程
Step 13: 运行时验证
```

---

## Guardrails | 防护规则

- **只研究模式，绝不复制代码** — 这是学习，不是抄袭
- **先查许可证** — 跳过许可证不兼容或缺失的项目
- **质量优先于数量** — 深入研究 1-2 个项目 > 浅扫 10 个
- **浅克隆** — 始终 `--depth 1`，不要浪费磁盘
- **git-ignore `reference/`** — 禁止把参考代码提交进项目仓库
- **记录你学到了什么** — 每次研究都要在 `docs/每日调研回写/` 产出一份文档
- **给研究设定时间盒** — 每个领域上限 30 分钟；找不到好参考就直接往下做

## Maturity | 成熟度

**阶段**：新（New）—— 为填补竞品分析（产品层）与实际实现（代码层）之间的空档而创建。

## Evolution History | 进化记录

- v1.0.0：首次创建 —— 5 阶段研究流程、领域参考目标、许可证意识

---

## 译注

- 「源版本」源文件未标注版本号；`Evolution History` 内记录的最新条目为 v1.0.0。
- 源文件把 `## Rule` 小节写在 H1 标题之前；本对照版按固定结构把它放在描述块之后，正文内容与源文件完全一致。
- 代码块内的命令、检索语法、URL 一律原样保留；仅将英文说明性注释与模板占位文字译为中文。
- 触发条件三档标题保留英文 `MUST trigger when` / `SHOULD trigger when` / `SKIP when`，并附中文，强度未做弱化。
