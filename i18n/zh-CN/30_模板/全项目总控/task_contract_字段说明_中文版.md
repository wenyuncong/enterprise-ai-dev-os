# DeliveryContract 交付契约字段说明 | task_contract.json Field Reference

> **源文件**：docs/_templates/全项目总控/task_contract.json
> **源版本**：未标注（文件内 `schema_version` 为 1.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

> 本文件是**字段说明文档**，不是契约本身。原样 JSON 模板见第 10 节，直接复制即可套用。
> 机器可读模式（Schema）：`docs/全项目总控/schemas/governance/delivery-contract.schema.json`
> 校验命令：`py scripts/py/validate_delivery_contract.py --contract <契约路径>`

---

## 1. 用途 | Purpose

`task_contract.json` 是 L2/L3 交付、并行智能体工作，以及任何带破坏性（destructive）、跨模块、权限、Schema 或发布边界的工作所使用的机器可读契约（DeliveryContract）。

它把范围（scope）、真相责任人（truth_owner）、非目标（non_goals）、公共可测试边界、证明计划（proof plan）与精确写入白名单（write_allowlist）固定下来，供校验脚本做 fail-closed 判定。

**它不替代**项目自有的测试、运行时 / 数据库证据、CI、业务真相或负责人授权。

---

## 2. 顶层字段 | Top-Level Fields

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `contract_id` | 必须 | 字符串，正则 `^dc_[a-z0-9][a-z0-9_-]{7,95}$` | 契约唯一 ID，必须以 `dc_` 开头 |
| `schema_version` | 必须 | 常量 `"1.0"` | 模式版本；校验器只接受 `1.0` |
| `status` | 必须 | `draft` / `scoped` / `approved` / `implementing` / `safeguarded` / `completed` / `blocked` / `cancelled` | 契约生命周期状态；状态名保持英文 |
| `project_id` | 必须 | 字符串，3–160 字符 | 项目标识 |
| `delivery` | 必须 | 对象，见第 3 节 | 交付元信息与门禁级别 |
| `product_contract` | 必须 | 对象，见第 4 节 | 产品结果、验收步骤、非目标 |
| `truth_owner` | 必须 | 字符串，3–500 字符 | 真相责任人：谁拥有该行为的权威真相与权威回读路径 |
| `scope` | 必须 | 对象，见第 5 节 | 写入白名单、禁止路径、范围外、破坏性分类、回滚 |
| `test_strategy` | 必须 | 对象，见第 6 节 | 测试模式与公共可测试边界 |
| `evidence_plan` | 必须 | 对象，见第 7 节 | 证明计划（proof plan）与证据记录 |
| `reviews` | 必须 | 对象，见第 8 节 | 双轴审查（two independent axes）状态 |
| `implementer` | 必须 | 字符串，3–160 字符 | 实施人 |
| `verification_owner` | 条件必填 | 字符串，3–160 字符 | 验证责任人；L2/L3 且 `status` 为 `safeguarded` / `completed` 时，必须存在且**不得等于** `implementer` |
| `owner_confirmation` | 可选 | `not_required` / `pending` / `confirmed` / `rejected` | 负责人确认；当 `scope.destructive_classification` 为 `explicit_owner_confirmation` 时必须为 `confirmed` |
| `created_at` | 必须 | ISO-8601 日期时间 | 创建时间 |
| `updated_at` | 必须 | ISO-8601 日期时间 | 最近更新时间 |

> 模式声明 `additionalProperties: false`：**不得新增模式外的键**。

---

## 3. `delivery` | 交付元信息

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `change_type` | 必须 | `usability` / `bug` / `existing_flow_change` / `new_capability` / `governance` | 改动类型 |
| `target_line` | 必须 | 字符串，1–160 字符 | 目标线（如 `develop`、`main`） |
| `target_version` | 可选 | 字符串，≤160 字符 | 目标版本 |
| `affected_flow` | 必须 | 字符串，3–500 字符 | 受影响的业务流程或能力流程 |
| `gate` | 必须 | `L0` / `L1` / `L2` / `L3` | 风险分级门禁代号，不译 |

---

## 4. `product_contract` | 产品契约

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `outcome` | 必须 | 字符串，3–1000 字符 | 产品结果：本次交付要让业务变成什么样 |
| `acceptance_steps` | 必须 | 字符串数组，≥1 项、≤500 字符/项、不得重复 | 业务流程验收（business-flow acceptance）步骤 |
| `non_goals` | 必须 | 字符串数组，≥1 项、≤500 字符/项、不得重复 | 非目标：明确不做的事，防止范围漂移 |

---

## 5. `scope` | 范围与安全

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `write_allowlist` | 必须 | 字符串数组，≥1 项、每项非空、≤320 字符/项、不得重复 | 写入白名单：允许改动的路径通配模式。**禁止** `*` / `**` / `/**` 这类仓库级全量模式 |
| `forbidden_paths` | 可选 | 字符串数组，≤320 字符/项、不得重复 | 禁止路径：命中即直接判定失败（优先级高于白名单） |
| `out_of_scope` | 必须 | 字符串数组，≥1 项、≥3 字符/项、不得重复 | 范围外事项 |
| `destructive_classification` | 必须 | `none` / `review_required` / `explicit_owner_confirmation` | 破坏性（destructive）分类 |
| `rollback_or_recovery` | 可选 | 字符串，≤1000 字符 | 回滚或恢复路径 |

---

## 6. `test_strategy` | 测试策略

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `mode` | 必须 | `red_green` / `alternative_evidence` | 测试模式：红绿测试（先红后绿），或写明替代证据 |
| `public_seam` | 必须 | 字符串，3–500 字符 | 公共可测试边界（即 `public_test_seam` 契约字段）：先在公共契约边界上让测试变红 |
| `rationale` | 必须 | 字符串，3–1000 字符 | 选择该边界或替代证据的理由 |
| `focused_test_command` | `red_green` 时必填 | 字符串，≤1000 字符 | 聚焦测试命令；模式为 `red_green` 时缺失即失败 |

---

## 7. `evidence_plan` | 证据计划（proof plan）

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `final_proofs` | 必须 | 对象数组，≥1 项，见下表 | 最终证明列表，不得为空 |
| `last_relevant_change_at` | 用 `--check-freshness` 时必填 | ISO-8601 日期时间 | 最后一次相关改动的时间；新鲜证据必须**晚于**该时间 |
| `evidence_records` | 可选 | 对象数组，见下表 | 实际证据记录 |

**`final_proofs[]` 元素**

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `proof_id` | 必须 | 正则 `^proof_[a-z0-9][a-z0-9_-]{3,95}$`，同一契约内唯一 | 证明 ID |
| `claim` | 必须 | 字符串，3–500 字符 | 该证明要证成的主张（claim） |
| `command_or_check` | 必须 | 字符串，3–1000 字符 | 证明用的命令或检查 |
| `must_run_after_final_change` | 必须 | 常量 `true` | 强制在最终相关改动之后运行，否则失败 |

**`evidence_records[]` 元素**

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `proof_id` | 必须 | 同 `final_proofs[].proof_id` 格式 | 对应哪条证明 |
| `status` | 必须 | 常量 `passed` | 证据状态；只有 `passed` 才算证据 |
| `finished_at` | 必须 | ISO-8601 日期时间 | 完成时间；不晚于 `last_relevant_change_at` 即判为过期证据（stale evidence） |
| `reference` | 必须 | 字符串，3–1000 字符 | 证据引用（日志路径、回读结果等） |

---

## 8. `reviews` | 双轴审查

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `standards_truth` | 必须 | 对象：`status` + `evidence`（+ 可选 `blockers`） | 轴一：标准 / 真相 / 架构 / 质量门禁 |
| `product_spec` | 必须 | 对象：`status` + `evidence`（+ 可选 `blockers`） | 轴二：产品结果 / 业务流程验收 / 显式非目标 |

**审查对象字段**

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `status` | 必须 | `pending` / `passed` / `failed` / `blocked` | 审查状态；`safeguarded` / `completed` 要求两轴均为 `passed` |
| `evidence` | 必须 | 字符串，3–1000 字符 | 审查证据 |
| `blockers` | 可选 | 字符串数组，≥3 字符/项、不得重复 | 阻塞项 |

---

## 9. fail-closed 判定规则 | Fail-Closed Rules

以下任一情况都会阻断 `safeguarded` 与 `completed`：

1. 缺失必填键，或 `schema_version` 不是 `1.0`。
2. 改动路径落在 `forbidden_paths` 内，或落在 `write_allowlist` 之外。
3. `write_allowlist` 含 `*` / `**` / `/**` 这类无限制模式。
4. `delivery.gate` 不是 `L0`–`L3`。
5. `product_contract` 的 `outcome` / `acceptance_steps` / `non_goals` 任一为空。
6. `test_strategy.mode` 为 `red_green` 但缺 `focused_test_command`。
7. `evidence_plan.final_proofs` 为空，或有证明的 `must_run_after_final_change` 不为 `true`。
8. 两轴审查任一不是 `passed`。
9. L2/L3 的 `safeguarded` / `completed` 缺 `verification_owner`，或 `verification_owner` 等于 `implementer`。
10. `destructive_classification` 为 `explicit_owner_confirmation` 但 `owner_confirmation` 不是 `confirmed`。
11. 带 `--check-freshness` 时：缺 `last_relevant_change_at`，或证据完成时间早于 / 等于该时间（过期证据）。

---

## 10. 完整 JSON 模板 | Full JSON Template（原样保留，键名与取值不译）

```json
{
  "contract_id": "dc_example_delivery_contract",
  "schema_version": "1.0",
  "status": "scoped",
  "project_id": "example-project",
  "delivery": {
    "change_type": "governance",
    "target_line": "develop",
    "target_version": "v1.0.0",
    "affected_flow": "example delivery contract adoption",
    "gate": "L2"
  },
  "product_contract": {
    "outcome": "A governed change is bounded, verified, and independently reviewed before completion.",
    "acceptance_steps": [
      "The approved change produces the requested result."
    ],
    "non_goals": [
      "This contract does not replace project-specific CI, release, or business rules."
    ]
  },
  "truth_owner": "Project-owned delivery rules and the authoritative runtime/data paths named by the task.",
  "scope": {
    "write_allowlist": [
      "src/example/**",
      "tests/example/**",
      "docs/changes/example/**"
    ],
    "forbidden_paths": [
      "database/production/**"
    ],
    "out_of_scope": [
      "Unrelated refactors and changes outside the approved capability."
    ],
    "destructive_classification": "none",
    "rollback_or_recovery": "Revert the scoped commit through the project-approved recovery process."
  },
  "test_strategy": {
    "mode": "red_green",
    "public_seam": "Example public command or API behavior",
    "rationale": "The behavior is testable at a public contract seam.",
    "focused_test_command": "npm test -- example-contract"
  },
  "evidence_plan": {
    "final_proofs": [
      {
        "proof_id": "proof_example_runtime",
        "claim": "The scoped behavior works through its real entrypoint.",
        "command_or_check": "Run the project-owned focused test and runtime check.",
        "must_run_after_final_change": true
      }
    ]
  },
  "reviews": {
    "standards_truth": {
      "status": "pending",
      "evidence": "Awaiting scoped diff and authoritative-path review."
    },
    "product_spec": {
      "status": "pending",
      "evidence": "Awaiting product acceptance replay against the stated non-goals."
    }
  },
  "implementer": "agent-delivery-owner",
  "owner_confirmation": "not_required",
  "created_at": "2026-08-21T00:00:00Z",
  "updated_at": "2026-08-21T00:00:00Z"
}
```

---

## 11. 套用步骤 | How to Reuse

1. 复制第 10 节 JSON 到任务目录，重命名为项目自定的契约文件名。
2. 逐字段替换：`contract_id`（保留 `dc_` 前缀）、`project_id`、`delivery.*`、`product_contract.*`、`truth_owner`、`scope.*`。
3. 若门禁为 L2/L3，补 `verification_owner`，且必须与 `implementer` 不同。
4. 运行校验：`py scripts/py/validate_delivery_contract.py --contract <契约路径> --json`。
5. 改动完成后追加 `evidence_records`，再带 `--check-freshness` 复跑一次。

---

## 译注与待确认 | Notes and Open Points

- **模板本身不完整**：源模板缺少可选的 `verification_owner`，但 L2/L3 的 `safeguarded` / `completed` 判定强制要求它；同时 `created_at` / `updated_at` 是示例时间，套用前必须改为真实时间。
- **命名对照**：任务包（`AI_PRODUCT_DELIVERY_TASK_TEMPLATE.md`）里写作 `public_test_seam` 与 `proof_plan`；机器可读契约里对应的键是 `test_strategy.public_seam` 与 `evidence_plan`。本说明同时保留两套写法，实际校验以本文件的键名为准。
- **必填标记的依据**：`是否必填` 一列取自 `delivery-contract.schema.json` 的 `required` 列表与 `validate_delivery_contract.py` 的运行时判定（两者不完全一致：`verification_owner`、`owner_confirmation` 在模式里可选，在校验器里按条件强制）。
