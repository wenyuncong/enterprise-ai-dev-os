# `ai-competitor-analyst` — 竞品对标与市场研究引擎

> **源文件**：skills/governance/ai-competitor-analyst/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-competitor-analyst
description: "Research competitors, market references, product positioning, benchmark gaps, and decision implications while separating facts, inference, and project choices. Use for market analysis, product strategy, pricing, feature comparison, or investor-facing positioning."
```

**中文描述**：研究竞品、市场参照、产品定位、对标差距及决策含义，并在全过程中把事实、推断与项目选择三者分开表述。适用于市场分析、产品策略、定价、功能对比，或面向投资人的定位工作。

---

## Purpose | 目标

研究与对比产品、功能与市场定位：

- 竞品功能对标
- 面向市场的功能映射
- 产品打包与版本策略分析
- 技术栈对比
- 行业趋势分析

本 Skill 用于**竞品研究与对标（benchmark）**，不用于产品策略决策。

---

## Rule | 规则

**对标必须依据产品实际行为，禁止依据营销材料。**

按以下方式核实竞品宣称：

- 直接使用产品（试用 / demo）
- 阅读技术文档
- 到社区论坛查看真实用户反馈
- 在可获得时对比公开 API / 架构

---

## Benchmark Framework | 对标框架

### 1. Feature Matrix | 功能矩阵

```markdown
| 功能 | 我们的产品 | 竞品 A | 竞品 B | 竞品 C |
|---|---|---|---|---|
| [分类]：[功能] | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ |
```

评级：

- ✅ 完整支持，达到生产级
- ⚠️ 部分支持或开发中
- ❌ 不具备

### 2. Pricing & Packaging | 定价与打包

```markdown
| 维度 | 我们的产品 | 竞品 A | 竞品 B |
|---|---|---|---|
| 免费版 | [细节] | [细节] | [细节] |
| 入门价 | [价格] | [价格] | [价格] |
| 企业版 | [价格] | [价格] | [价格] |
| 定价模式 | [模式] | [模式] | [模式] |
```

### 3. Technology & Architecture | 技术与架构

```markdown
| 维度 | 我们的产品 | 竞品 A | 竞品 B |
|---|---|---|---|
| 技术栈 | [技术栈] | [技术栈] | [技术栈] |
| 部署方式 | [可选项] | [可选项] | [可选项] |
| API/SDK | [是否具备] | [是否具备] | [是否具备] |
| 多租户 | [模式] | [模式] | [模式] |
```

### 4. Market Positioning | 市场定位

```markdown
| 维度 | 我们的产品 | 竞品 A | 竞品 B |
|---|---|---|---|
| 目标客群 | [客群] | [客群] | [客群] |
| 关键差异点 | [差异点] | [差异点] | [差异点] |
| 地域重点 | [区域] | [区域] | [区域] |
| GTM 策略 | [策略] | [策略] | [策略] |
```

---

## Research Methodology | 研究方法

### Primary Research (Recommended) | 一手研究（推荐）

1. **产品试用**：注册竞品的试用 / demo
2. **文档研读**：阅读官方文档、API 参考
3. **社区分析**：查看论坛、GitHub issue、Stack Overflow
4. **客户访谈**：与竞品产品的使用者交流

### Secondary Research | 二手研究

1. **评测平台**：G2、Capterra、TrustRadius
2. **行业报告**：Gartner、Forrester、IDC
3. **技术博客**：工程博客、案例研究
4. **会议演讲**：近期演讲、路线图披露

---

## Benchmark Decision Template | 对标决策模板

```markdown
## 对标：[功能 / 产品领域]

### 研究日期
[YYYY-MM-DD]

### 研究方法
- [ ] 产品试用
- [ ] 文档研读
- [ ] 社区分析
- [ ] 二手来源

### 关键发现
1. [发现 1] — 影响：[高/中/低]
2. [发现 2] — 影响：[高/中/低]

### 差距分析
| 差距 | 严重度 | 已具备该能力的竞品 | 建议动作 |
|---|---|---|---|

### 决策
[自建 / 采购 / 合作 / 暂缓]

### 时间线
[立即 / Q1 / Q2 / 未来]
```

---

## Standard Workflow | 标准工作流

1. **定义范围**：要对标哪个产品领域或功能？
2. **确定竞品**：对比哪 3–5 个竞品？
3. **研究**：用一手与二手方法收集数据
4. **打分**：填写对标框架的各张表
5. **分析差距**：识别优势、劣势、机会
6. **给出建议**：产出可落地的行动建议

---

## Guardrails | 防护规则

- 禁止拿营销话术当对标依据 —— 必须用实际产品使用来核实
- 禁止对比过期的竞品版本
- 禁止忽略竞品的社区 / 生态强度
- 禁止跳过定价模式分析 —— 它往往就是关键差异点
- 禁止在对标表中没有证据的情况下产出建议

## Maturity | 成熟度

**阶段**：有效（Effective）—— 提炼自企业级 ERP 竞品分析工作流。

## Evolution History | 进化记录

- v1.0.0：从 gerp-competitor-analyst 提炼
- v1.1.0：通用化，形成通用对标框架

---

## 译注

- 「源版本」源文件未标注版本号；`Evolution History` 内记录的最新条目为 v1.1.0。
- 对标框架中的 ✅ / ⚠️ / ❌ 评级符号、`GTM`、`API/SDK`、`Q1` / `Q2` 等标识符原样保留。
- 所有表格模板均为 Markdown 代码块内的模板，按中文对照译出；表头译中文，单元格内的英文占位标识符保留。
