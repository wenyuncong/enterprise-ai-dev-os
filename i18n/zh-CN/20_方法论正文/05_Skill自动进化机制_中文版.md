# 05 — Skill 自动进化机制 | Skill Auto-Evolution Mechanism

> **源文件**：methodology/05_Skill自动进化机制.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。
> **所属**：Enterprise-Grade Full AI Development Methodology（企业级全 AI 开发方法论）
> **前置文档**：00_核心方法论白皮书、01_Skill体系分层架构

---

## 1 静态规则的问题 | The Problem with Static Rules

大多数 AI 编码规则（`.cursorrules`、`AGENTS.md`）写一次之后就再也不更新。这会导致：

| 问题 | 后果 |
|---|---|
| **规则腐化** | 规则引用了已删除的文件、已改名的模块、已废弃的模式 |
| **上下文缺失** | 新模式出现了，但规则没有收录 |
| **虚假信心** | AI 相信过期规则，做出错误决策 |
| **没有改进** | 同样的错误反复发生，因为规则从不学习 |

---

## 2 进化循环 | The Evolution Loop

```text
+-----------------------+
|                       |
|  1. TASK COMPLETED    |
|                       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|                       |
|  2. EVIDENCE GATHERING |
|  - Repeated patterns? |
|  - Repeated mistakes? |
|  - Missing context?   |
|                       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|                       |
|  3. GAP CLASSIFICATION |
|  - Update skill?     |
|  - New skill?        |
|  - Rule change?      |
|  - Doc only?         |
|                       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|                       |
|  4. EXECUTE UPDATE   |
|  - Modify SKILL.md   |
|  - Update archive    |
|  - Sync to AI tool   |
|                       |
+-----------+-----------+
            |
            v
+-----------+-----------+
|                       |
|  5. NEXT TASK BENEFITS|
|  - Loads updated skill|
|  - Avoids past mistakes|
|                       |
+-----------------------+
```

---

## 3 进化触发条件 | Evolution Triggers

进化器（evolver）在以下情况激活：

### 触发条件 1：重复模式（出现 3 次及以上）| Trigger 1: Repeated Pattern (3+ occurrences)

```text
Pattern: "Every time we add a new report page, we forget to add the permission entry"
Evidence: 3 completed tasks all had a follow-up permission fix
Action: Add "permission check" to the report development workflow
Target skill: The tech skill used for report development
```

### 触发条件 2：重复错误（出现 2 次及以上）| Trigger 2: Repeated Mistake (2+ occurrences)

```text
Mistake: "AI generates frontend code referencing API endpoints that don't exist yet"
Evidence: 2 tasks had to redo frontend work after backend API changed
Action: Enforce Step 5 (Controller) before Step 7 (Frontend TS)
Target: rules/AGENTS.md — Update 13-step enforcement
```

### 触发条件 3：上下文缺失 | Trigger 3: Missing Context

```text
Symptom: "AI doesn't know about the custom pagination wrapper"
Evidence: AI tried to use standard pagination, broke the custom implementation
Action: Add pagination pattern to the relevant tech skill
Target: vue/SKILL.md or equivalent
```

### 触发条件 4：结构性变更 | Trigger 4: Structural Change

```text
Change: Project moved from microservices to monolith
Evidence: Old skill references microservice patterns that no longer exist
Action: Update all skills that reference deployment/service architecture
Target: Multiple skills
```

### 触发条件 5：用户反馈 | Trigger 5: User Feedback

```text
Feedback: "The skill tells me to use X but the project actually uses Y"
Action: Investigate, update skill if feedback is correct
Target: The skill that was mentioned
```

---

## 4 差距分类决策树 | Gap Classification Decision Tree

```text
Finding detected
    |
    v
Is this a one-off note? ── YES ──> Record in task doc only. Skip evolution.
    |
    NO
    |
    v
Does an existing skill already cover this pattern? ── YES ──> Update that SKILL.md
    |
    NO
    |
    v
Does this pattern cross 2+ task types? ── YES ──> Create new skill
    |
    NO
    |
    v
Is this a project-wide rule? ── YES ──> Update rules/AGENTS.md
    |
    NO
    |
    v
Template or reference update is enough ──> Update relevant reference file
```

---

## 5 进化记录格式 | Evolution Record Format

每次进化都必须在受影响 SKILL.md 的末尾记录：

```markdown
## 进化记录 | Evolution History

- v1.0.1（2026-06-18）：3 个任务使用了自定义分页后，补充分页模式
- v1.0.0（2026-06-17）：从 GERP 项目首次提炼
```

Skill 档案（`docs/全项目总控/MASTER_INDEX.md`）跟踪全部 Skill：

```markdown
## Skill 成熟度矩阵（Skill Maturity Matrix）— 2026-06-17

| Skill | 阶段 | 最近进化 | 进化次数 | 下次复核 |
|---|---|---|---|---|
| ai-rule-dispatcher | effective（生效） | 2026-06-17 | 1 | 2026-07-17 |
| ai-task-decomposer | effective（生效） | 2026-06-17 | 1 | 2026-07-17 |
| vue | evolving（进化中） | 2026-06-16 | 3 | 2026-06-30 |
```

---

## 6 进化反模式 | Evolution Anti-Patterns

| 反模式 | 为什么失败 |
|---|---|
| **没有证据就进化** | 依据臆测而非事实建立规则 |
| **为一次性模式创建 Skill** | 无用 Skill 泛滥，拖垮体系 |
| **进化过于频繁** | 频繁改动让 Skill 不稳定，AI 跟不上 |
| **进化过于稀少** | Skill 腐化，方法论衰退 |
| **不记录进化** | 没有审计轨迹，无法追踪改了什么、为什么改 |
| **只进化文档，不进化 Skill** | 文档变好了，但 AI 行为没有改变 |

---

## 7 进化节奏 | Evolution Cadence

| 频率 | 动作 |
|---|---|
| **每个任务之后** | 检查进化触发条件 |
| **每周** | 复核 Skill 成熟度矩阵 |
| **每月** | 全量 Skill 审计 —— 删除未使用的、合并重叠的、升级成熟的 |
| **每次发布** | 对全部 Skill 锁版，记录基线 |

---

*下一篇：[06_企业级部署与验收标准.md] — 部署门禁与验收标准*

---

**译注**

1. **代码块围栏规范化**：英文源使用单反引号作为围栏，语言标注处写作 `` `markdown ``。译文统一改为标准三反引号围栏；`markdown` 标注照抄源文件，无标注的 ASCII 结构图标注为 `text`。ASCII 图、触发条件示例块、决策树一律逐字保留。
2. **`markdown` 块的处理**：两处 `markdown` 块不是 Shell/JSON/YAML/SQL，而是「进化记录格式」与「Skill 成熟度矩阵」的文档样例，按任务要求逐行译出：表头、说明文字与阶段取值译出，`Skill` 名、版本号、日期、数值、路径 `docs/全项目总控/MASTER_INDEX.md` 保持原样。阶段取值写作 `effective（生效）`、`evolving（进化中）`，保留英文枚举值。
3. **`##` 级章节计数**：源文件含代码块内的 `## Evolution History` 与 `## Skill Maturity Matrix` 两行，按行首 `##` 统计共 9 行；译文保持同样 9 行（见 `90_校验` 校验口径）。
4. **阈值精确保留**：触发条件 1 的「3+ occurrences」译作「出现 3 次及以上」，触发条件 2 的「2+ occurrences」译作「出现 2 次及以上」；ASCII 块内的 `3 completed tasks`、`2 tasks`、`3+`、`2+` 原样保留。
5. **源文件 `## 3. Evolution Triggers` 的触发条件编号**已在译文中显式写为「触发条件 1」至「触发条件 5」，与源文件 `Trigger 1`–`Trigger 5` 一一对应。
