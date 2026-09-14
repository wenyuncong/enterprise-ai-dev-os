# `ai-skill-evolver` — 自我进化的 Skill 引擎

> **源文件**：skills/core/ai-skill-evolver/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-skill-evolver
description: "Improve the skill system from concrete evidence by updating existing skills, classifying gaps, recording evolution, and proposing new skill candidates. Use when reviewing skill quality, fixing ineffective skills, or turning repeated task patterns into reusable capability."
```

**中文描述**：基于具体证据改进 Skill 体系：更新既有 Skill、分类差距、记录进化、提出新的 Skill 候选。在评审 Skill 质量、修复失效 Skill，或把重复出现的任务模式转化为可复用能力时使用。

---

# ai-skill-evolver — Self-Evolving Skill Engine | 自我进化的 Skill 引擎

## Purpose | 用途

把重复劳动转化为更强的可复用资产：

- Skill 更新（改进既有 SKILL.md）
- 新 Skill 候选（模式反复出现时创建新 Skill）
- 归档更新（记录进化记录）
- 项目 Skill 文档（更新项目专属文档）
- 进化日志（跟踪改了什么、为什么改）

本 Skill 负责**能力进化**，不负责日常任务执行。

## Rule | 规则

**禁止凭模糊印象进化 Skill。只能基于具体证据进化。**

证据来源：
- 跨模块重复出现的任务模式
- 重复出现的错误，或反复缺失上下文的时刻
- 应当被正式化的稳定输出模板
- 项目路径 / 规则变更
- 用户反馈指出某 Skill 实际并不有效

始终区分：
- declared skill（已声明的 Skill：磁盘上存在）
- callable skill（可调用的 Skill：能按名称被调用）
- effective skill（有效的 Skill：能稳定产出正确结果）
- evolving skill（进化中的 Skill：正在被主动改进）

## When to Use | 触发条件

- 完成一批相关任务之后
- 当某个模式在不同模块间重复出现 3 次以上
- 用户提出："improve the skills"、"what skills are missing"、"why didn't the skill work"
- 项目结构发生重大变更之后
- 定期方法论健康检查期间

## Continuous Repair-To-Skill Loop | 持续修复-技能循环

在每一轮实现之后：

1. **先完成（Finish）**具体的代码/文档任务
2. **识别（Identify）**该任务是否暴露了可复用规则、重复缺陷或缺失模式
3. **分类（Classify）**——它属于既有 Skill，还是需要新建 Skill？
4. **更新（Update）**相关 SKILL.md（扩展，而不是替换）
5. **记录（Record）**进化，写入 Skill 归档
6. **同步（Sync）**到当前使用的 AI 工具（如需要）

## Standard Workflow | 标准工作流

### Step 1: Gather Evidence | 步骤 1：收集证据

阅读当前的 Skill 治理链：
- 所有既有 SKILL.md 文件
- 近期任务日志与执行记录
- 已完成任务中的用户反馈
- 文档回写

### Step 2: Classify the Gap | 步骤 2：分类差距

| 差距类型 | 动作 |
|---|---|
| 既有 Skill 需要细化 | 更新 SKILL.md |
| 新模式跨越 2 种以上任务类型 | 创建新 Skill |
| 单页面问题 | 记录在任务文档中，不进 Skill |
| 规则需要更新 | 更新 rules/AGENTS.md |
| Skill 存在但无效 | 调查并修复根因 |

### Step 3: Choose the Right Action | 步骤 3：选择正确动作

可选动作：
- 更新 SKILL.md（新增小节、扩展引用）
- 更新引用文件
- 新增或更新项目专属文档
- 更新 Skill 归档表
- 创建新的治理任务

### Step 4: Record the Evolution | 步骤 4：记录进化

必须记录：
- 触发本次变更的原因
- 当前成熟度阶段
- 更新了什么（文件路径 + 行范围）
- 仍然缺失什么
- 被改动的是真实 Skill 资产，还是只有文档

### Step 5: Feed the Next Round | 步骤 5：反馈下一轮

把进化结果转化为：
- 用于 Skill 改进的新任务 ID
- 供未来使用的更新后模板
- 更清晰的路由规则
- 下一批 Skill 待办台账

## Maturity Rating System | 成熟度评级

| Stage | 含义 |
|---|---|
| declared | SKILL.md 存在，但从未被使用过 |
| callable | 能按名称被调用，基本指令可用 |
| effective | 能稳定产出正确结果 |
| in-closure | 具备验收标准与证据规则 |
| evolving | 正在依据反馈主动改进 |

---

## Scheduled Governance Trigger | 定期治理触发

### When to trigger ai-skill-governor | 何时触发 ai-skill-governor

| 触发条件 | 动作 |
|---|---|
| 每完成约 20 个任务 | 运行完整的 ai-skill-governor 审计 |
| 每周（不论任务数量） | 轻量审计（矛盾 + 孤儿） |
| 每月 | 全量审计（全部 5 个维度） |
| 新增 3 个以上新 Skill 之后 | 对既有 Skill 做矛盾扫描 |
| 方法论文档更新之后 | 核实 Skill 与更新后文档的一致性 |

### Auto-Trigger | 自动触发

ai-skill-evolver 在检测到以下情况时，应当自动调用 ai-skill-governor：
- 2 个以上 Skill 的 Purpose 行内容重叠
- 某个 Skill 超过 3 个月未更新
- 某个 Skill 在最近 50 个任务中被加载 0 次

---

## Guardrails | 防护规则

- 当更新模板或既有 Skill 就足够时，禁止创建新 Skill
- 禁止在没有具体重复证据的情况下进化 Skill（最少 3 次出现）
- 禁止忘记同时更新 Skill 文件与归档
- 若没有更新任何正式资产，禁止声称某个 Skill 已进化
- 禁止停留在「指出差距」——必须转化为具体更新或任务

## Maturity | 成熟度

**Stage**：effective（有效）—— 已在 GERP ERP 上实战检验，且有文档化的进化周期。

## Evolution History | 进化记录

- v1.0.0：从 gerp-skill-evolver 提炼，泛化为通用能力
- Source：GERP Enterprise ERP, Continuous Repair-To-Skill loop validatedr

---

## 译注

- 源文件 frontmatter 未标注版本号；`skills/SKILL_MANIFEST.json` 中该 Skill 的 `maturity` 为 `verified`，正文 `## Maturity` 自述 Stage 为 `effective`（小写），两者口径不同，本译文如实保留原文。
- 源文件 `## Maturity Rating System` 使用 `declared` / `callable` / `effective` / `in-closure` / `evolving` 五级，与 `skills/SKILL_MANIFEST.json` 的 `maturityLevels`（`raw` / `generalized` / `callable` / `verified` / `deprecated`）不一致；按术语口径，成熟度等级名一律保留英文原样，不做对齐改写。
- 源文件 `Source` 行以 `validatedr` 结尾（第 148 行尾多余字符 `r`），属源文件笔误；本译文照抄英文原文，源文件未被改动。
