# `ai-brownfield-analyzer` — 老项目分析与模式提炼引擎

> **源文件**：skills/governance/ai-brownfield-analyzer/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-brownfield-analyzer
description: "Analyze existing projects before changing them by discovering architecture, scripts, conventions, risks, intervention level, and safe extension points. Use for brownfield codebases, inherited systems, migrations, or unfamiliar repository work."
```

**中文描述**：在改动既有项目之前先做分析——发现架构、脚本、约定、风险、干预级别与安全扩展点。适用于老项目（brownfield）代码库、接手他人系统、迁移，或不熟悉的仓库工作。

---

## Purpose | 目标

在修改任何既有项目之前，执行一次结构化审计：分析当前状态、定级干预级别（intervention level）、提炼模式（好的与坏的），并产出外科手术式修改计划。本 Skill 确保方法论在"强加于项目"之前，先"向项目学习"。

**它解决的问题**：AI 把每个项目都当成新项目（greenfield）的一张白纸。它会重写本来能跑的代码、破坏原本有其合理原因的既有约定、强加并不适配的模式。老项目（brownfield）分析通过强制 AI"先理解、后动手"，把这些全部挡在门外。

---

## Trigger | 触发条件

- 首次进入任何既有项目时 **必须（ALWAYS）** 触发
- 用户说"修一下我项目里这个 Bug"、"给我的应用加个功能"、"重构这个模块"时
- `ai-project-classifier` 返回 Origin = Brownfield 时
- 接手其他团队留下的半成品工作时
- 项目没有 README、没有测试，或架构不清时

---

## Rule | 规则

**既有项目是老师，方法论是学生。**

| 编号 | 强制约束（保留原文 MUST 强度） |
|---|---|
| **MUST-1** | **MUST** 先审计、后改代码。审计（Step 0–5）未完成之前，**MUST NOT** 向项目写入任何代码。 |
| **MUST-2** | **MUST** 匹配既有风格，即使它很丑；**MUST NOT** 以"顺手美化"为名改动既有约定。 |
| **MUST-3** | **MUST** 复用并匹配既有脚本与工具模式；既有工具能做的事，**MUST NOT** 另写新脚本。 |
| **MUST-4** | **MUST NOT** 修改任何不在本次范围内的既有代码。 |

```
DO NOT（MUST NOT）: 看到混乱代码 → “我来把它好好重写一遍”
DO（MUST）:         看到混乱代码 → “原本的意图是什么？这里已经存在什么模式？”
```

---

## Analysis Workflow | 分析流程

### Step 0: Tool Discovery (BEFORE Quick Scan) | 工具发现（在快速扫描之前）

**在分析代码之前，先发现已经存在什么工具。** 既有项目往往已有成百上千个经过实战检验的脚本。禁止重新发明它们。

```bash
# 发现项目中的全部脚本
py scripts/py/discover_tools.py {project_path} --by-purpose
```

**输出**：所有既有脚本的清单，按用途分组：

- database/migration、database/check、database/sync、database/seed
- build/compile、service/start、service/stop
- deploy/release、test/api、test/unit
- utility/cleanup、utility/generate

**这条输出告诉你**：

- 哪些任务已经有自动化（禁止再写新脚本）
- 哪些任务还是手工做的（可以补自动化的机会点）
- 项目工具链的成熟度
- 项目的运维模式是什么

**规则**：若某个用途分类下有 5 个以上脚本，说明该项目已经形成了稳定模式。**MUST 匹配它们，MUST NOT 另起一套。**

---

### Step 1: Quick Scan (5 minutes) | 快速扫描（5 分钟）

深入之前先摸清地形。

```bash
# 我们面对的是什么
ls -la                    # 根目录结构
git log --oneline -20     # 近期活动
cat package.json          # 依赖（Node）
cat pom.xml               # 依赖（Java）
```

**输出**：一段话总结项目类型、规模、活跃度。

### Step 2: Deep Audit (15-30 minutes) | 深度审计（15–30 分钟）

完整审计维度见 methodology/09_老项目改造方法论.md Phase 1。

```markdown
## 审计摘要

### 项目画像
- 类型：[Web 应用 / API / 移动端 / 桌面端 / 混合]
- 技术栈：[框架 + 语言 + 数据库]
- 年龄：[首次提交 → 最近提交]
- 团队规模：[依据提交作者估算]

### 健康度记分卡
| 维度 | 评分（1-10） | 证据 |
|---|---|---|
| 代码组织 | [1-10] | [简要证据] |
| 测试覆盖 | [1-10] | [简要证据] |
| 文档 | [1-10] | [简要证据] |
| 依赖新鲜度 | [1-10] | [简要证据] |
| 一致性 | [1-10] | [简要证据] |
| **总体** | **[1-10]** | |
```

### Step 3: Classify Intervention Level | 定级干预级别

见 methodology/09_老项目改造方法论.md §2。

```
依据审计结果 + 用户目标 → Level [1-5]
- Level 1（快速修复 Quick Fix）：[条件是否满足？]
- Level 2（功能追加 Feature Addition）：[条件是否满足？]
- Level 3（模块升级 Module Upgrade）：[条件是否满足？]
- Level 4（深度改造 Deep Renovation）：[条件是否满足？]
- Level 5（接管 Takeover）：[条件是否满足？]
```

### Step 4: Extract Patterns | 提炼模式

见 methodology/09_老项目改造方法论.md Phase 3。

**好的模式 → 保留，并正式化进 Skill：**

```
模式：[名称]
发现位置：[文件]
为什么好：[分析]
需要更新的 Skill：[Skill 名]
```

**坏的模式 → 记录待修：**

```
反模式：[名称]
发现位置：[文件]
影响：[它会破坏什么]
修复优先级：[P0/P1/P2]
```

### Step 5: Produce Modification Plan | 产出修改计划

见 methodology/09_老项目改造方法论.md Phase 4。

```markdown
## 修改计划

### 干预级别：Level [1-5]
### 范围：
- IN（纳入）：[我们会改什么]
- OUT（排除）：[我们绝不触碰什么]

### 批次
| # | 任务 | 风险 | 依赖 | 预估 |
|---|---|---|---|---|
| 1 | [任务] | [低/中/高] | [无/依赖项] | [时间] |

### 安全措施
- [ ] 数据库已备份
- [ ] 开工前回归测试通过
- [ ] 已创建功能分支
- [ ] 回滚方案已文档化
```

---

## Special Case: Semi-Finished Projects | 半成品项目

### Detection Signals | 检测信号

- 代码里到处是 "It should work but..." 这类注释
- README 描述了并不存在的功能
- 满屏 `TODO` 与 `FIXME` 标记
- 没有 git 历史（只有一个 "initial commit" 或全新 clone）
- 完成度参差不齐（登录完美可用，但看板是空的 div）

### Handling Semi-Finished Projects | 半成品项目的处理方式

```
1. 记录现实（不是愿望）
   - "README 说支持文件上传。实际情况：路由存在，handler 是空的。"

2. 描绘已存在的东西（不是计划中的东西）
   - 可用功能：[列表]
   - 部分可用：[带细节的列表]
   - 未实现：[列表]

3. 制定完成顺序（依赖优先）
   - 什么必须先工作，才能让什么工作？
   - 不是："有哪些功能做了会很酷？"

4. 设定现实预期
   - "这个项目完成度 40%。剩余 60% 需要 X 周。"
```

---

## Special Cases Not to Miss | 容易遗漏的场景

### Missing Original Team | 原始团队不在

- 不要替"奇怪"的代码脑补意图
- `git blame` 就是你的历史学家
- 补测试，把它当作留给下一位开发者的文档
- 建立 bus-factor 图：哪些模块已经没有幸存的领域知识？

### Data Migration Required | 需要数据迁移

- 迁移**之前**先审计源数据质量
- 显式映射 旧→新 schema
- 幂等脚本 + dry-run 模式
- 在数据副本上测试，**永远禁止**在线上数据上测试

### Environment Drift | 环境不一致（环境漂移）

- 比对所有环境的配置
- 检查：依赖版本、运行时版本、数据库版本、硬编码路径
- 统一：一份配置模板 + 环境覆盖

### When to Rebuild | 何时放弃重做

- 加权评分：tests(20%) + deps(15%) + architecture(20%) + team knowledge(15%) + features(20%) + security(10%)
- 得分 < 2.5 → 可以考虑重做
- 重做之前先把所有业务规则抽出来（它们才是真正的资产）

完整细节：methodology/09_老项目改造方法论.md §5b

---

## Pattern Extraction → Skill Evolution | 模式提炼 → Skill 进化

### What Patterns to Extract | 提炼哪些模式

| 分类 | 要找什么 | 流向 |
|---|---|---|
| **命名** | 一致的类/文件/表命名模式 | ai-component-standardizer |
| **结构** | 模块组织、目录层级 | ai-atomic-architect、`methodology/08_项目文件夹结构标准.md` |
| **错误处理** | 错误如何被捕获、记录、返回 | ai-single-truth-enforcer |
| **API 设计** | 端点命名、请求/响应格式 | 后端技术类 Skill |
| **组件模式** | 页面如何组织（列表/单据/报表） | ai-component-standardizer |
| **库选型** | 用了哪些库、为什么用 | ai-library-first |
| **鉴权模式** | 认证/授权如何工作 | 后端技术类 Skill |
| **数据库模式** | 表命名、索引、迁移策略 | mysql-best-practices |
| **测试模式** | 测试如何组织、测了什么 | 测试类技术 Skill |

### Extraction Rules | 提炼规则

| 规则 | 依据 |
|---|---|
| 好模式与坏模式都要提炼 | 反模式教的是"禁止做什么" |
| 一条提炼记录只写一个模式 | 保持聚焦 |
| 引用具体文件/行号 | 基于证据，不基于主观看法 |
| 不得只凭一次出现就提炼 | 一个模式 = 至少 3 个一致的实例 |
| 立即喂给 ai-skill-evolver | 禁止攒批次再更新模式 |

---

## Integration | 集成

| 步骤 | 动作 |
|---|---|
| `ai-project-classifier` | 识别为 Brownfield → 路由到 ai-brownfield-analyzer |
| `ai-brownfield-analyzer` | Phase 1-3（审计 → 定级 → 提炼） |
| `ai-chief-planner` | Phase 4（计划） |
| `ai-task-decomposer` | Phase 5（执行批次） |
| `ai-skill-evolver` | Phase 6（把模式回喂给 Skill） |
| `ai-reference-researcher` | 可选：找参考项目做对比 |

---

## Guardrails | 防护规则

- **先审计、后动手** — **MUST NOT** 在不熟悉的项目里写代码
- **匹配既有风格，即使它很丑** — **MUST** 一致性优先于美观
- **不要修没坏的东西** — 如果它能跑且不在范围内，就放着别动
- **相信跑得起来的代码，而不是文档** — 文档会撒谎，代码不会
- **一次提交只做一类改动** — 重构 **或** 新功能，绝不同时做
- **只提炼模式，不强加模式** — 标准由项目来定
- **数据库变更必须是独立批次** — 绝不允许把数据库改动和代码改动混在一起
- **半成品 ≠ 垃圾** — 记录现实，排出完成顺序

## Maturity | 成熟度

**阶段**：新（New）—— 提炼自真实的老项目（brownfield）ERP 项目分析模式。

## Evolution History | 进化记录

- v1.0.0：首次创建 —— 5 步分析流程、5 个干预级别、模式提炼、半成品项目处理

---

## 译注

- 「源版本」源文件未标注版本号；`Evolution History` 内记录的最新条目为 v1.0.0。
- 所有命令（如 `py scripts/py/discover_tools.py {project_path} --by-purpose`）原样保留；代码块内仅把英文说明性注释译为中文。
- 源文件中的 `## Rule` 使用 `DO NOT` / `DO` 强制语气，译文以「禁止 / 应当 / 必须」等强度词一一对应，未做弱化。
