# AI 交付 Skill 职责矩阵 | AI Delivery Skill Responsibility Matrix

> **源文件**：docs/全项目总控/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

> **本文件是 `AGENTS.md` 0.8 强制要求阅读的文件**：任何产品主导或多步交付，都必须先读本矩阵，并为当前阶段选出**一个**主责 Skill。

---

## 1 目的 | Purpose

本矩阵为每一个非平凡（non-trivial）的 AI 交付任务，在每个交付阶段指定**唯一一个主责 Skill（primary owner）**。它防止 Skill 重叠演变为重复的计划、互相矛盾的规则，或反复的验证。

本矩阵适用于方法论自身的工作，也适用于采用本方法论的项目。它**不替代**项目专属规则、技术栈 Skill 或领域验收标准。

---

## 2 交付阶段 | Delivery Stages

| 阶段（Stage） | 主责 Skill（Primary skill） | 支撑 Skill（Supporting skills） | 负责（Owns） | 不得负责（Must not own） |
| --- | --- | --- | --- | --- |
| 分类（Classify） | `ai-project-classifier` | `ai-brownfield-analyzer` | 项目来源（origin）、质量目标（quality target）、平台（platforms）、规模（scale）、基线 Skill 集（baseline skill set） | 详细任务计划或实现 |
| 路由（Route） | `ai-rule-dispatcher` | `ai-project-classifier` | 任务线（task line）、一个主导 Skill（lead skill）、首批文档、首批事实核查 | 批次拆分或代码改动 |
| 发现（Discover） | `ai-brownfield-analyzer` | `ai-reference-researcher`、技术栈 Skill | 既有架构、脚本、约定、扩展点（extension points）、干预级别（intervention level） | 重写无关的、正在正常工作的代码 |
| 定义产品结果（Define product outcome） | `ai-product-directed-delivery` | `ai-competitor-analyst`、`ai-ui-ux-governor` | `product owner` 契约、场景、可用性、业务验收（business-flow acceptance）、交接件（handoffs） | 无证据的内部实现选型 |
| 规划项目群（Plan program） | `ai-chief-planner` | `ai-task-decomposer`、`ai-5s-delivery-governor` | 里程碑、待办台账（backlog）状态、依赖顺序、收口状态 | 文件级实现细节 |
| 拆分执行（Split execution） | `ai-task-decomposer` | `ai-chief-planner`、`ai-command-executor` | 原子批次（atomic batches）、写入边界、依赖、批次验收 | 发布授权或业务策略发明 |
| 强制执行交付契约（Enforce delivery contract） | `ai-delivery-contract-governor` | `ai-5s-delivery-governor`、`ai-command-executor` | 机器可读的写入范围（write scope）、阶段流转、`fresh evidence`、独立审查 | 替代项目 CI、业务真相，或 `product owner` 授权 |
| 设计架构（Design architecture） | `ai-architect-governor` | `ai-atomic-architect`、`ai-domain-boundary-mapper` | 架构决策、取舍（trade-offs）、ADR、归属边界（ownership boundaries） | 产品验收，或传输层专属实现 |
| 定义能力链（Define capability chain） | `ai-atomic-architect` | `ai-single-truth-enforcer`、`ai-foundation-governor` | 真相 -> 原子（atom）-> 编排（orchestration）-> 聚合（aggregate）-> `command gateway` -> 适配器（adapter）-> `Host` 契约 | 页面局部业务规则，或重复的真相 |
| 安全实施（Implement safely） | `ai-command-executor` | 技术栈 Skill、`ai-library-first`、相关治理 Skill | 已批准的命令、工具使用、`working-tree` 门禁、限定范围的执行证据 | 任务路由、产品策略、发布决策 |
| 治理真相与字段（Govern truth and fields） | `ai-single-truth-enforcer` | `ai-field-package-governor`、`ai-foundation-governor` | 后端/数据真相、策略边界、字段来源、错误分级 | 视觉布局归属 |
| 构建 UI（Build UI） | `ai-component-standardizer` | `ai-ui-ux-governor`、前端技术栈 Skill | UI atom、组合（composition）、标准模板、`Host` 边界 | 领域计算、授权、写入策略 |
| 验证业务流程（Verify business flow） | `ai-flow-closure-audit` | `ai-runtime-verify`、`ai-frontend-audit` | 页面 -> API -> 真相 -> 回写（writeback）-> 报表收口；标准/真相与产品/规格的 `two independent axes` 双轴审查 | 发布/版本晋升 |
| 验证运行时（Verify runtime） | `ai-runtime-verify` | 技术栈 Skill、`ai-command-executor` | 实际执行的运行时路径，以及浏览器/API/日志/副作用（side-effect）证据 | 静态架构判断 |
| 治理交付（Govern delivery） | `ai-5s-delivery-governor` | `ai-chief-planner`、`ai-command-executor` | Scope/Specify/Ship/Safeguard/Sell 状态、L0-L3 门禁、发布证据 | 业务领域真相 |
| 进化方法论（Evolve methodology） | `ai-skill-evolver` | `ai-skill-governor` | 重复模式出现后，基于证据的 Skill/规则/模板更新 | 日常项目实现 |
| 审计方法论健康度（Audit methodology health） | `ai-skill-governor` | `ai-skill-evolver`、`ai-rule-dispatcher` | 矛盾、重叠、过期规则、孤儿项（orphan）、路由覆盖度复核 | 自动合并或删除 Skill |

---

## 3 边界规则 | Boundary Rules

1. `ai-rule-dispatcher` **只选出一个主导 Skill（one lead skill）**。支撑 Skill 只提供建议，**不得**另立竞争性计划。
2. `ai-chief-planner` 负责项目群级别的排序；`ai-task-decomposer` 负责执行粒度的批次。
3. `ai-architect-governor` 决定架构取舍；`ai-atomic-architect` 在该决策之后定义可复用的能力链。
4. `ai-product-directed-delivery` 负责人与 AI 的职责契约；`ai-5s-delivery-governor` 负责交付状态与发布证据。
5. `ai-runtime-verify` 证明一条正在运行的路径；`ai-flow-closure-audit` 证明端到端的业务链。
6. `ai-skill-governor` 只报告重叠。**没有明确的限定范围决策，它绝不合并或删除任何 Skill。**
7. 当项目采用机器可读的交付契约时，`ai-delivery-contract-governor` 对 L2/L3、并行或高风险工作是**强制（mandatory）**的。

> **硬约束提醒**：每个交付阶段**只能有一个主责 Skill**。任何阶段出现两个竞争性主责 Skill，或重复任务绕过既定主责 Skill，都触发第 5 节的复核。

---

## 4 必要交接件 | Required Handoff

每一次交接只能携带下一位责任人所需的事实：

```text
Outcome and non-goals:
Current-state evidence:
Truth owner:
Selected lead skill and support skills:
Write boundary:
Acceptance and gate:
Known risks / rollback:
```

---

## 5 复核触发条件 | Review Trigger

出现下列任一情况时，复核本矩阵：

- 新增了一个正式 Skill（official skill）；
- 一次交付中改动了三个或更多 Skill；
- 一个任务被指派了两个竞争性的主导 Skill；
- 重复出现的任务绕过了既定的主导 Skill；
- 方法论场景回归（methodology scenario regression）失败。

---

## 译注

- 源文件未标注版本号，故「源版本」写作「未标注」。
- 源文件 5 个章节（Purpose、Delivery Stages、Boundary Rules、Required Handoff、Review Trigger）逐节对应，**未删章节**；交付阶段表 17 行逐行对应，边界规则 7 条、复核触发条件 5 条逐条对应。
- 交付阶段表的 5 列表头译为「阶段 / 主责 Skill / 支撑 Skill / 负责 / 不得负责」，其中 `Owns` 与 `Must not own` 保留英文原词于括号内，避免语义强度损失。
- 表内所有 Skill 名、`Host`、`command gateway`、`working-tree`、`two independent axes`、`fresh evidence`、`product owner`、`business-flow acceptance`、L0-L3 门禁代号一律原样保留英文。
- 第 3 节末尾的「硬约束提醒」为译文新增的对照提示块，用于显式固化源文件「每阶段一个主责 Skill」的约束；源文件正文未改动，源文件本身未被修改。
- 源文件未规定阶段编号；本译文按源文件出现顺序编号 1–5，便于与英文源逐条对表。
