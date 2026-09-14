# `ai-chief-planner` — 端到端项目规划与收口引擎

> **源文件**：skills/core/ai-chief-planner/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-chief-planner
description: "Plan end-to-end project execution, task lines, batch sequencing, acceptance criteria, evidence requirements, blockers, and closure state. Use for project-level coordination, multi-step delivery, task backlog governance, and final closure planning."
```

**中文描述**：规划端到端项目执行——任务线（task line）、批次排序、验收标准、证据要求、阻塞项与收口状态。用于项目级协调、多步交付、待办台账（backlog）治理与最终收口规划。

---

## Rule | 规则

每份计划必须：1）把目标拆成可验证的原子步骤；2）按依赖关系排序步骤；3）为每一步定义清晰的完成判据（done criteria）；4）增量跟踪进度；5）标记完成之前先验证完成度。**禁止跳过验证步骤。**

## Purpose | 目的

在全生命周期内编排项目任务：

- 规划（Planning）：范围定义、任务拆解、依赖映射
- 排期（Scheduling）：优先级排序、资源分配、里程碑设定
- 跟踪（Tracking）：进度监控、阻塞识别、状态汇报
- 收口（Closure）：验证、文档回写、证据收集
- 调研（Research）：竞品基准、技术评估、市场分析

本 Skill 面向**项目级编排（project-level orchestration）**，不用于单任务执行。

---

## Core Principles | 核心原则

1. **先检查后执行（Check-before-execute）**：做决定前先核实数据库、代码与配置。
2. **定位根因，不打补丁（Root cause, not patches）**：找到并修复根因；禁止使用会制造技术债的临时绕过。
3. **证据驱动（Evidence-driven）**：每个结论都必须有证据（日志、API 响应、SQL 结果、截图）。
4. **闭环（Closed loop）**：计划 → 执行 → 验证 → 记录 → 复检。
5. **不重复劳动（Non-duplication）**：始终先检查已有任务包与执行记录，避免重复工作。
6. **功能优先（Function-first）**：优先完成真实功能收口，再提非必要特性。
7. **唯一真相源（Single source of truth）**：以数据为中心的模块，一个概念只允许一个权威页面/API。
8. **边界意识（Boundary awareness）**：区分不同应用语境（web、mobile、API、admin）。

---

## Planning Workflow | 规划工作流

### Phase 1: Discovery | 探查

- 明确请求的范围与约束
- 识别干系人与受影响领域
- 检查现有文档与既往决策
- 执行初步环境自检

### Phase 2: Task Decomposition | 任务拆解

- 把工作拆成可执行批次（委派给 `ai-task-decomposer`）
- 标注批次之间的依赖
- 估算工作量并识别风险
- 分配优先级（P0/P1/P2）

### Phase 3: Scheduling | 排期

- 按依赖与优先级对批次排序
- 识别可并行的工作流
- 设定里程碑与检查点
- 分配资源与时间盒（timebox）

### Phase 4: Execution Tracking | 执行跟踪

- 监控批次完成状态
- 识别阻塞项并按需上报
- 在总控文档中更新进度
- 依据发现调整排期

### Phase 5: Closure Verification | 收口验证

- 对每个批次执行验收标准
- 收集证据（API 响应、截图、日志）
- 把发现回写文档
- 把改进项回灌给 `ai-skill-evolver`

---

## Task Status Model | 任务状态模型

| 状态 | 含义 | 下一步动作 |
|---|---|---|
| `backlog` | 已识别但尚未排期 | 确定优先级后转到 `planned` |
| `planned` | 已排期并映射好依赖 | 解除阻塞后转到 `in_progress` |
| `in_progress` | 正在执行 | 完成后转到 `review` |
| `review` | 执行完成，等待验证 | 转到 `verified`，或退回 `in_progress` |
| `verified` | 验收标准已通过 | 转到 `closed` |
| `closed` | 证据已收集、文档已更新 | 归档 |
| `blocked` | 因依赖/问题无法推进 | 上报，解决阻塞项 |

---

## Closure Checklist | 收尾检查清单

把任何任务批次标记为 `closed` 之前，逐项核实：

- [ ] 全部验收标准通过
- [ ] 证据已收集（截图、API 日志、SQL 结果）
- [ ] 文档已更新（相关文档反映本次变更）
- [ ] 工作区（working-tree）干净（仅暂存当前任务的文件）
- [ ] 若提炼出新模式，相关 Skill 已更新
- [ ] 若本批次是被依赖项，下一批次已解除阻塞

---

## Scheduling Patterns | 调度模式

| 模式 | 何时使用 |
|---|---|
| **Sequential（顺序）** | 批次之间存在严格依赖顺序 |
| **Parallel（并行）** | 批次相互独立，领域/文件不同 |
| **Staggered（交错）** | 工作有重叠，并设置了同步点 |
| **Wave-based（分波）** | 把相关批次编成若干开发波次 |

---

## Guardrails | 防护规则

- 未核实当前状态，禁止开始执行
- 禁止跳过收口验证——未验证的工作不算“完成”
- 禁止重复劳动——先检查已有任务包
- 禁止超出已有信息做计划——拆成“探查 + 执行”两个阶段
- 禁止忽略阻塞项——必须上报，不得绕过

## Maturity | 成熟度

**Stage**：Effective —— 提炼自企业级 ERP 项目规划实践，含 12+ 条核心规划原则。

## Evolution History | 进化记录

- v1.0.0：提炼自 gerp-chief-planner（原始 10KB）
- v1.1.0：通用化，纳入通用项目规划模式

---

## 译注

1. **章节顺序**：源文件把 `## Rule` 放在 H1 标题之前（`## Rule` 出现在第 6 行，H1 出现在第 10 行）。中文版按本册固定结构把 H1 与元信息置顶，`## Rule` 紧随其后，各小节内容与相对顺序相对源文件不变，未删节、未合并。
2. **源版本**：源文件 frontmatter 只有 `name` 与 `description` 两个键，无版本号或日期标注，故「源版本」记「未标注」；`## Evolution History` 中存在版本条目 v1.0.0、v1.1.0，但那两行描述的是 Skill 内容自身的演进，不等于源文件版本标注。
3. **未给出具体文件名的引用**：源文件第 4 条防护规则与收尾清单提到“master control documents / 文档（documentation）”，未指名具体文件；中文版按仓库既有目录 `docs/全项目总控/` 与 `docs/` 理解，未虚构文件名。
4. **Maturity 状态词**：`Effective` 是受控状态词（另有 `New`、`effective` 等写法），术语表未收录，故保留英文状态词并加中文注解。
5. **依赖的 Skill 引用均可解析**：`ai-task-decomposer`（skills/core/ai-task-decomposer/SKILL.md）与 `ai-skill-evolver`（skills/core/ai-skill-evolver/SKILL.md）在仓库中均存在，无断链。
6. **优先级代号**：源文件只出现 P0/P1/P2（未出现 P3）；中文版按源文件原样保留，未补写未出现的代号。
7. **引用审计结论**：本 Skill 目录下只有 `SKILL.md` 一个文件，没有 `references/` 配套目录，也没有指向仓库内其他文件/路径的引用（正文只提到 Skill 名），**未发现断链引用**。作为对照：同层 `ai-task-decomposer` 与 `ai-rule-dispatcher` 各自带有未被正文引用的 `references/` 配套文件。
