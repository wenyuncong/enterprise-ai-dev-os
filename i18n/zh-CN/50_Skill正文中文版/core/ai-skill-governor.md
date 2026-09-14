# `ai-skill-governor` — Skill 体系健康与治理引擎

> **源文件**：skills/core/ai-skill-governor/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-skill-governor
description: "Audit the health of a skill ecosystem for contradictions, overlap, stale assumptions, missing triggers, orphan skills, quality drift, and maturity gaps. Use for weekly/monthly methodology reviews or after major skill, rule, or project-structure changes."
```

**中文描述**：审计 Skill 生态的健康度，覆盖矛盾、重叠、过期假设、缺失触发条件、孤儿 Skill、质量漂移与成熟度缺口。用于每周/每月方法论评审，或 Skill、规则、项目结构发生重大变更之后。

---

## Rule | 规则

每个 Skill 必须：1）具备合法的 frontmatter（`name`、`description`）；2）遵守命名约定；3）在 `SKILL_MANIFEST.json` 中登记；4）具备清晰的生命周期状态；5）通过结构校验。禁止启用未经验证的 Skill。

# ai-skill-governor — Skill System Health & Governance Engine | Skill 体系健康与治理引擎

## Purpose | 用途

主动审计、去重并维护 Skill 体系。与 `ai-skill-evolver`（对已完成任务作出反应）不同，本 Skill 对整个 Skill 库执行**周期性的健康检查**——检测腐蚀、矛盾、冗余与有效性缺口。

**它解决的问题**：49 个正式 Skill（且仍在增长）需要持续的质量控制。Skill 可能出现以下问题：
- 相互矛盾（两个 Skill 说的正好相反）
- 重叠（两个 Skill 以不同方式覆盖同一领域）
- 腐蚀（模式过时、库已变更、最佳实践演进）
- 变成无人使用（创建了但从未被触发）
- 失去有效性（初次创建后评级从未更新）

---

## Trigger | 触发条件

- **周期性**：每完成约 20 个任务，或每周（以先到者为准）
- **按需**：用户提出 "audit skills"、"check skill quality"、"are skills still good?"
- **自动**：新增 Skill 时（检查与既有 Skill 是否冲突）
- **重大方法论更新之后**：方法论文档变更时，核实 Skill 是否仍然对齐

---

## Audit Dimensions | 审计维度

### Dimension 1: 矛盾检测 | Contradiction Detection

对同一主题给出相反说法的 Skill。

**检测方法**：

```
1. Extract all "Guardrails" / "Rules" sections from every skill
2. Group by topic domain (frontend, backend, database, testing, etc.)
3. Flag pairs that make conflicting claims
```

**中文对照**：

1. 从每个 Skill 中抽取所有 "Guardrails" / "Rules" 小节。
2. 按主题域分组（前端、后端、数据库、测试等）。
3. 标出给出冲突主张的配对。

**矛盾示例**：

```
ai-single-truth-enforcer: "All validation in backend, never in frontend"
  vs
ai-component-standardizer: "Client-side validation for instant feedback"

→ These need reconciliation: "Client-side for UX feedback only. 
  Backend re-validates everything. Frontend validation is cosmetic, 
  not authoritative."
```

**中文对照**：`ai-single-truth-enforcer` 要求「所有校验都在后端，前端绝不校验」，而 `ai-component-standardizer` 提到「客户端校验以获得即时反馈」。两者需要调和为：「客户端仅用于 UX 反馈。后端重新校验一切。前端校验只是外观性的，不是权威的。」

### Dimension 2: 重叠检测 | Overlap Detection

两个或更多 Skill 以不同方式覆盖同一领域。

**检测方法**：

```
1. Compare "Purpose | 用途" sections for keyword overlap
2. If > 60% keyword overlap → flag for review
3. Decision: merge, split, or clarify boundaries
```

**中文对照**：

1. 比对 "Purpose | 用途" 小节的关键词重叠度。
2. 若关键词重叠 > 60% → 标记待评审。
3. 决策：合并、拆分，还是厘清边界。

**重叠示例**：

```
ai-ui-ux-governor §State Handling: "Loading, Empty, Error, Edge Cases"
  vs
ai-frontend-audit §Error States: "Loading state, empty state, error state"

→ Both cover the same thing. Either merge into one authoritative source,
  or cross-reference with clear ownership.
```

**中文对照**：`ai-ui-ux-governor` 的 §State Handling 与 `ai-frontend-audit` 的 §Error States 覆盖同一件事。要么合并为一个权威源，要么做交叉引用并明确归属。

### Dimension 3: 腐蚀检测 | Rot Detection

引用了过时模式、已废弃库或陈旧实践的 Skill。

**检测方法**：

```
1. Check last modified date of each SKILL.md
2. Flag skills not updated in > 3 months
3. For each flagged skill, verify:
   - Libraries mentioned: still current versions?
   - Patterns described: still best practice?
   - Guardrails: still enforceable?
```

**中文对照**：

1. 检查每个 SKILL.md 的最后修改日期。
2. 标出超过 3 个月未更新的 Skill。
3. 对每个被标记的 Skill 核实：提到的库是否仍为当前版本；描述的模式是否仍是最佳实践；防护规则是否仍可执行。

### Dimension 4: 有效性评分 | Effectiveness Scoring

每个 Skill 在阻止真实问题上的有效程度如何？

**评分方法**：

```
Score = (times_triggered × 0.3) + (problems_prevented × 0.5) + (user_satisfaction × 0.2)

Where:
- times_triggered: How often was this skill loaded?
- problems_prevented: How many issues did it catch before production?
- user_satisfaction: Did the skill's guidance lead to good outcomes?
```

**中文对照**：

```
得分 = （被触发次数 × 0.3）+ （阻止的问题数 × 0.5）+ （用户满意度 × 0.2）

其中：
- 被触发次数：该 Skill 被加载的频率
- 阻止的问题数：它在进入生产前拦下了多少问题
- 用户满意度：该 Skill 的指引是否带来了好结果
```

**得分解读**：

| 得分 | 评级 | 动作 |
|---|---|---|
| 8-10 | Effective（有效） | 保留，仅做小幅更新 |
| 5-7 | Needs improvement（需改进） | 复查防护规则，强化薄弱环节 |
| 2-4 | Weak（薄弱） | 大幅重写，或拆分为多个聚焦的 Skill |
| 0-1 | Ineffective（无效） | 归档，或彻底重写 |

### Dimension 5: 孤儿检测 | Orphan Detection

存在但从未被触发的 Skill。

**检测方法**：

```
1. Track which skills ai-rule-dispatcher routes to
2. Skills not routed to in last 50 tasks → flag
3. Reason: never needed, or dispatcher doesn't know about it?
```

**中文对照**：

1. 跟踪 `ai-rule-dispatcher` 路由到了哪些 Skill。
2. 最近 50 个任务中未被路由到的 Skill → 标记。
3. 原因判断：从不需要，还是 dispatcher 不知道它的存在？

---

## Audit Output | 审计输出

```markdown
## Skill Governance Audit — [YYYY-MM-DD]

### Health Summary
| Metric | Value |
|---|---|
| Total official skills | 42 |
| Contradictions found | [N] |
| Overlaps found | [N] |
| Rotting skills (>3 months) | [N] |
| Orphan skills (never used) | [N] |
| Average effectiveness score | [N.N] |

### Contradictions
| Skill A | Skill B | Conflict | Resolution |
|---|---|---|---|
| ai-single-truth-enforcer | ai-component-standardizer | Validation location | Clarified: client-side = cosmetic only |

### Overlaps
| Skills | Overlap % | Recommendation |
|---|---|---|
| ai-ui-ux-governor + ai-frontend-audit | 35% on state handling | Cross-reference, don't merge |
| ai-architect-governor + ai-atomic-architect | 25% on architecture | Clarify: governor = decisions, atomic = patterns |

### Rotting Skills
| Skill | Last Updated | Issues Found | Action |
|---|---|---|---|
| ai-competitor-analyst | 2026-03-15 | Benchmark framework still valid | Minor update: add AI tools to research methods |

### Effectiveness Ratings
| Skill | Score | Rating |
|---|---|---|
| ai-single-truth-enforcer | 8.5 | Effective |
| ai-component-standardizer | 7.2 | Needs improvement |
| ... | ... | ... |

### Recommendations
1. [Action item 1]
2. [Action item 2]
```

**模板字段中文对照**：

| 英文模板字段 | 中文含义 |
|---|---|
| `## Skill Governance Audit — [YYYY-MM-DD]` | Skill 治理审计报告（日期） |
| `### Health Summary` | 健康度摘要 |
| `Total official skills` | 正式 Skill 总数 |
| `Contradictions found` | 发现的矛盾数 |
| `Overlaps found` | 发现的重叠数 |
| `Rotting skills (>3 months)` | 腐蚀中的 Skill 数（超过 3 个月未更新） |
| `Orphan skills (never used)` | 孤儿 Skill 数（从未被使用） |
| `Average effectiveness score` | 平均有效性得分 |
| `### Contradictions`（Skill A / Skill B / Conflict / Resolution） | 矛盾清单（Skill A / Skill B / 冲突点 / 处置结论） |
| `### Overlaps`（Skills / Overlap % / Recommendation） | 重叠清单（涉及 Skill / 重叠度 / 建议） |
| `### Rotting Skills`（Skill / Last Updated / Issues Found / Action） | 腐蚀清单（Skill / 最后更新日期 / 发现的问题 / 动作） |
| `### Effectiveness Ratings`（Skill / Score / Rating） | 有效性评级（Skill / 得分 / 评级） |
| `### Recommendations` | 建议事项 |

---

## Governance Cycle | 治理周期

```
WEEKLY (Light Audit):
  - Quick scan for new contradictions (compare new/modified skills)
  - Orphan detection
  - ~10 minutes

MONTHLY (Full Audit):
  - All 5 dimensions
  - Effectiveness re-scoring
  - Rot detection with library version checks
  - ~30 minutes

POST-MAJOR-UPDATE (Triggered):
  - After methodology doc changes → verify skill alignment
  - After adding 3+ new skills → contradiction scan
```

**中文对照**：

- **每周（轻量审计）**：对新增/修改的 Skill 做新矛盾快速扫描；执行孤儿检测；约 10 分钟。
- **每月（全量审计）**：全部 5 个维度；有效性重新评分；带库版本检查的腐蚀检测；约 30 分钟。
- **重大更新后（触发式）**：方法论文档变更后 → 核实 Skill 对齐情况；新增 3 个以上新 Skill 后 → 矛盾扫描。

---

## Auto-Fix Rules | 自动修复规则

部分问题无需人工评审即可自动修复：

| 问题 | 自动修复 |
|---|---|
| Skill 引用了过时的 Skill 名 | 更新引用（例如把 "ai-frontend-availability-audit" → "ai-frontend-audit"） |
| 缺少 "Evolution History" 小节 | 补充模板小节 |
| SKILL.md 超过 500 行 | 标记待拆分（不自动拆分） |
| 两个 Skill 的 Purpose 行完全相同 | 标记待合并评审 |

---

## Integration | 集成

| Skill | 关系 |
|---|---|
| `ai-skill-evolver` | governor 针对具体 Skill 更新触发 evolver |
| `ai-rule-dispatcher` | governor 为路由提供更新后的有效性得分 |
| `ai-chief-planner` | governor 的审计结果输入方法论改进计划 |
| 所有 Skill | governor 是位于所有 Skill 之上的质量控制层 |

---

## Guardrails | 防护规则

- **按周期审计，而不是只按需审计** —— 腐蚀是静默发生的
- **矛盾就是缺陷（bug）** —— 两个 Skill 说相反的话，是系统性缺陷
- **有效性以结果衡量，而不是以意图衡量** —— 一个「本应有效」却没能阻止问题的 Skill 是无效的
- **孤儿 Skill 就是浪费** —— 如果没人用，就归档它
- **禁止自动合并 Skill** —— 重叠检测只做标记供人工评审，永不自动合并

## Maturity | 成熟度

**Stage**：New（新建）—— 为填补 Skill 生态中主动治理的空白而创建。

## Evolution History | 进化记录

- v1.0.0：初始创建 —— 5 个审计维度、每周/每月周期、自动修复规则

---

## 译注

- 源文件 frontmatter 未标注版本号；`skills/SKILL_MANIFEST.json` 中该 Skill 的 `maturity` 为 `verified`，正文 `## Maturity` 自述 Stage 为 `New`，两者口径不同，本译文如实保留原文。
- `## Audit Output` 的审计报告模板为 fenced 代码块，按翻译口径原样复制不译；其后补「模板字段中文对照」表以满足全量对照要求。
- 模板内 `Total official skills | 42` 与当前 `skills/SKILL_MANIFEST.json` 的 `counts.official = 49` 不一致（源文件为示例值，未随 Skill 数量增长同步）；本译文照抄示例，未改写为 49。`Purpose` 小节自述为 49 个正式 Skill。
- 五个审计维度的标题按术语口径统一为「中文 | English」并列写法：矛盾检测 | Contradiction Detection、重叠检测 | Overlap Detection、腐蚀检测 | Rot Detection、有效性评分 | Effectiveness Scoring、孤儿检测 | Orphan Detection。
- 源文件 H1 前先有 `## Rule`；本译文保持源文件的章节顺序。
- `ai-frontend-availability-audit` 为源文件示例中的历史 Skill 名，当前 `skills/` 下不存在该目录（现名为 `ai-frontend-audit`），本译文按源文件原样保留。
