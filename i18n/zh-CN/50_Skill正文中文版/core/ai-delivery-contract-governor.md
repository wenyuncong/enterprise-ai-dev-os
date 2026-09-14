# `ai-delivery-contract-governor` — 可执行交付契约

> **源文件**：skills/core/ai-delivery-contract-governor/SKILL.md
> **源版本**：未标注（源文件 frontmatter 只有 `name` 与 `description`；`## Evolution History` 最新条目为 v1.0.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-delivery-contract-governor
description: "Create and enforce machine-readable delivery contracts that bound write scope, stage transitions, test seams, fresh evidence, and independent two-axis review. Use for L2/L3 work, parallel agents, risky changes, or any task that needs rules to fail closed instead of relying on prose alone."
```

**中文描述**：创建并强制执行机器可读的交付契约，用其约束写入范围（write scope）、状态迁移、可测试边界（test seam）、新鲜证据（fresh evidence）与独立双轴审查（independent two-axis review）。适用于 L2/L3 工作、并行智能体、风险变更，或任何需要规则失败即阻断（fail-closed）、而不是只依赖文字说明的任务。

---

## Rule | 规则

任何受治理的任务都不得因为某个智能体声称「已就绪」而推进。只有当其交付契约允许进入下一状态、且必需证据齐备时，任务才允许推进。契约是失败即阻断（fail-closed）的。

## 标题说明 | Title（源文件 H1）

源文件 H1 为 `# ai-delivery-contract-governor - Executable Delivery Contract`，已作为本文件标题译出：`ai-delivery-contract-governor` — 可执行交付契约。

## Purpose | 目的

把既有的 5S 生命周期转化为一个小型、可机器校验的任务边界：

```text
scope contract
-> approved write boundary
-> implementation
-> fresh evidence
-> independent two-axis review
-> safeguarded / completed
```

本 Skill 是 `ai-5s-delivery-governor` 的补充。它不替代项目的业务规则、CI、发布流程、权限系统或运行时唯一真相源。

## When to Use | 何时使用

- L2/L3 交付、共享能力、Schema、权限、发布或跨模块写入路径。
- 并行或交接工作，智能体之间需要互不重叠的写入边界。
- 任务需要可强制执行的证明，以证明确实留在范围内。
- 项目希望对过期证据、缺失审查，或超出约定边界的文件改动，在本地/CI 直接拒绝。

在有帮助时，L0/L1 工作可以使用同一契约，但不应被强加以不降低真实风险的仪式。

## Contract Assets | 契约资产

使用项目自有资产：

- 模式（Schema）：`docs/全项目总控/schemas/governance/delivery-contract.schema.json`
- 模板：`docs/_templates/全项目总控/task_contract.json`
- 校验器：`scripts/py/validate_delivery_contract.py`

从模板创建一个任务自有的契约。把它与任务包（task pack）或项目自有交付记录放在一起；禁止将它放入通用的临时目录。

## Required Contract Content | 契约必需内容

在动笔之前记录：

1. 产品结果、验收步骤与非目标（non_goals）；
2. 变更类型、目标线/版本、受影响流程与 L0-L3 门禁；
3. 权威真相责任人（truth_owner）；
4. 精确写入白名单（write allowlist）、禁止路径与破坏性分类；
5. 聚焦的公共可测试边界（public test seam），或有正当理由的替代证据；
6. 必须在最后一次相关变更之后运行的最终证明命令/检查；
7. 彼此分开的标准/真相审查与产品/规格审查。

对于 `review_required` 或 `explicit_owner_confirmation`，在契约记录所需决策之前，禁止执行破坏性工作。

## State and Gate Rules | 状态与门禁规则

| 状态（Status） | 含义 | 进入所需的最小门禁 |
| --- | --- | --- |
| `draft` | 仅初始想法 | 禁止实现 |
| `scoped` | 结果、范围、真相责任人与证据计划已存在 | 范围校验器通过 |
| `approved` | 所需的负责人/破坏性决策已记录 | 已批准的任务只能在白名单内写入 |
| `implementing` | 有范围限定的工作正在进行 | 改动文件保持在白名单内 |
| `safeguarded` | 最终证明是新鲜的，且两项审查均通过 | 校验器带 `--check-freshness` 通过 |
| `completed` | 项目集成/发布条件也已满足 | 5S 收口，加上已 safeguarded 的契约 |
| `blocked` / `cancelled` | 工作不得静默继续 | 在任务包中记录阻断或取消原因 |

对于 L2/L3，在进入 `safeguarded` 或 `completed` 之前，`verification_owner` 必须与 `implementer` 不同。独立验证者（independent verifier）可以使用项目自有 CI、另一个智能体或一名评审人，但必须审查实际证据，而不能只看实施人的总结。

## Validation Workflow | 校验工作流

1. 在实现之前校验任务记录：

```text
py scripts/py/validate_delivery_contract.py --contract <task-contract.json>
```

2. 在集成之前校验已观测或已暂存的路径：

```text
py scripts/py/validate_delivery_contract.py --contract <task-contract.json> --changed-file <repo-relative-path>
```

3. 在最后一次相关变更之后，追加证据记录并运行：

```text
py scripts/py/validate_delivery_contract.py --contract <task-contract.json> --check-freshness
```

4. 运行项目真实的测试、运行时检查、数据库回读与发布门禁。本校验器只检查契约纪律；它不会伪造领域证据。

## Guardrails | 防护规则

- 禁止使用 `**` 这类宽泛白名单来隐藏无关工作。
- 禁止在实现之后把范围外文件塞进白名单，只为让校验通过；必须重新打开 Scope/Specify 并记录原因。
- 禁止用早于最后一次相关变更的运行结果来声称最终证据。
- 禁止让通过的标准/真相审查豁免失败的产品验收，反向亦然。
- 禁止允许实施人在没有独立验证者的情况下自我认证 L2/L3 保障。
- 禁止把这份 JSON 记录当作对业务歧义、破坏性工作或发布授权的负责人批准的替代品。

## Evolution History | 进化记录

- v1.0.0：从 GSD 风格的阶段门禁与角色分离评审实践引入可执行交付契约，并适配到 AI-OS 5S、产品主导交付与后端真相治理。

---

## 译注 | Translation Notes

1. 源文件 H1 `# ai-delivery-contract-governor - Executable Delivery Contract` 已作为本文件标题译出，并另设「标题说明」小节保留其原始英文形态，便于逐节对表。
2. `safeguarded`、`completed`、`blocked`、`draft`、`scoped`、`approved`、`implementing`、`cancelled` 是契约状态名，按术语表与 `docs/_templates/全项目总控/task_contract.json` 的口径保持英文，不译。
3. 契约资产三项路径均已核对存在：`docs/全项目总控/schemas/governance/delivery-contract.schema.json`、`docs/_templates/全项目总控/task_contract.json`、`scripts/py/validate_delivery_contract.py`。

## 术语保留自检 | Term Preservation Self-Check

下表逐个列出本译文必须原样保留的英文词，并注明其出现小节。

- [x] ☑ `write allowlist`
- [x] ☑ `fresh evidence`
- [x] ☑ `independent verifier`
- [x] ☑ `safeguarded`
- [x] ☑ `completed`
- [x] ☑ `fail-closed`
- [x] ☑ `validate_delivery_contract.py`

| 英文词 | 出现小节与形式 | 是否保留 |
|---|---|---|
| `write allowlist` | Required Contract Content 第 4 条「精确写入白名单（write allowlist）」；Contract Assets 语境（允许写入边界） | ☑ 是 |
| `fresh evidence` | 中文描述「新鲜证据（fresh evidence）」；Purpose 代码块 `-> fresh evidence`；State and Gate Rules 表 `safeguarded` 行「最终证明是新鲜的」 | ☑ 是 |
| `independent verifier` | State and Gate Rules 表后段落「独立验证者（independent verifier）」；Guardrails 第 5 条 | ☑ 是 |
| `safeguarded` | Purpose 代码块 `-> safeguarded / completed`；State and Gate Rules 表状态行 `` `safeguarded` ``；表后段落；Guardrails 第 5 条 | ☑ 是 |
| `completed` | Purpose 代码块 `-> safeguarded / completed`；State and Gate Rules 表状态行 `` `completed` ``；表后段落 | ☑ 是 |
| `fail-closed` | Rule「失败即阻断（fail-closed）」；中文描述「失败即阻断（fail-closed）」（源文件 `## Rule` 末句 `The contract is fail-closed.`） | ☑ 是 |
| `validate_delivery_contract.py` | Contract Assets 校验器条目 `scripts/py/validate_delivery_contract.py`；Validation Workflow 第 1、2、3 步的三个 `text` 代码块 | ☑ 是 |
