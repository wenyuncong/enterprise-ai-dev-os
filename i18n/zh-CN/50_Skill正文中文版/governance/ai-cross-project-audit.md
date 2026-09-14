# `ai-cross-project-audit` — 跨项目治理审计器

> **源文件**：skills/governance/ai-cross-project-audit/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-cross-project-audit
description: "Cross-project governance audit pipeline: consume existing audit data, orchestrate L3 domain atoms, produce L5 evidence + index + report. Supports read-only (report only) and active (modify target) modes. Use when auditing one project from another project's atomic governance system."
```

**中文描述**：跨项目治理审计流水线：消费既有审计数据、编排 L3 领域原子、产出 L5 证据 + 索引 + 报告。支持只读模式（仅出报告）与主动模式（修改目标项目）。适用于用某个项目的原子治理系统去审计另一个项目的场景。

---

## Purpose | 目标

用原子治理系统跨独立项目编排治理审计。本 Skill 支撑这一模式：**一个项目的原子系统去审计另一个项目的代码库** —— 且不修改目标项目。

**它解决的问题**：治理审计通常被封闭在单个项目内。跨项目审计需要人工搬运数据、格式不统一、没有可复用的流水线。本 Skill 定义了标准流水线：消费既有审计数据、编排多来源发现、产出统一的治理报告。

---

## The Pipeline | 流水线

```
既有审计数据（gaps.json, result.json）
        │
        ▼
┌───────────────────────────────────┐
│  L3 领域原子（Domain Atoms）      │
│  domain_code_audit                │
│  domain_erp_field_check           │
│  domain_sql_validate              │
│  domain_api_test                  │
│  domain_config_diff               │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  L5 治理编排器（Orchestrator）    │
│  app_governance_orchestrator      │
│  audit → evidence → index → report│
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  输出（Outputs）                  │
│  evidence.json  (audit trail)     │
│  knowledge_index.json (searchable)│
│  report.md      (human readable)  │
└───────────────────────────────────┘
```

---

## Rule 1: Read-Only by Default (P0) | 规则 1：默认只读（P0）

审计另一个项目时，默认采用**只读模式**：

- 消费既有审计数据文件（不重新扫描目标项目）
- 产出报告与建议
- **禁止**修改目标项目代码
- 给所有证据打上来源项目与审计周期 ID 标签

**例外**：若被审计项目的团队明确要求主动整改，则切换到主动模式，并给出显式的范围边界。

---

## Rule 2: Data Reuse (P1) | 规则 2：数据复用（P1）

在生成新的审计数据之前，先在证据目录中查找既有审计产出：

```
evidence/{target_project}/
  {audit_name}/
    gaps.json        ← 代码审计发现
    result.json      ← 字段 / 规则审计结果
    casepack.json    ← 复核队列 / 建议
```

既有数据可以被 L3 原子直接消费，无需重新扫描目标项目。这既能省算力，也能保证审计一致性。

---

## Rule 3: Evidence Chain Integrity (P0) | 规则 3：证据链完整性（P0）

每次跨项目审计**必须**产出完整的证据链：

| 阶段 | 产出 | 验证 |
|-------|--------|-------------|
| 1. 审计 | L3 原子产出的结构化发现 | 发现数 > 0 |
| 2. 证据 | 含 cycle_id、stages、findings_sample 的 JSON 文件 | 文件存在且为合法 JSON |
| 3. 索引 | 含可检索条目的 JSON 索引 | entries_added > 0 |
| 4. 报告 | 带执行摘要的 Markdown 报告 | 报告路径存在 |

---

## Audit Types | 审计类型

### Code Audit (domain_code_audit) | 代码审计（domain_code_audit）

消费 gaps.json，其中的发现形如：

- direct_db_write_in_controller
- action_endpoint_without_command_pattern

产出：按模块分组的发现组、风险评分、整改建议。

### Field Audit (domain_erp_field_check) | 字段审计（domain_erp_field_check）

消费来自 field_package_truth_audit 规则包（rulepack）的 result.json。

产出：字段模式违规、FieldPackage 缺口、前端重复字段定义。

### SQL Audit (domain_sql_validate) | SQL 审计（domain_sql_validate）

消费 SQL 迁移文件。

产出：schema 漂移、缺失的迁移、命名约定违规。

### API Audit (domain_api_test) | API 审计（domain_api_test）

消费 API 端点清单。

产出：端点健康度、响应 schema 一致性、鉴权覆盖。

### Config Audit (domain_config_diff) | 配置审计（domain_config_diff）

消费配置文件。

产出：环境漂移、缺失的租户配置、硬编码值。

---

## Governance Orchestrator Usage | 治理编排器用法

```python
from atoms.application.governance_orchestrator_executor import GovernanceOrchestratorExecutor
from runtime.governance import RiskActionMatrixService

gov = RiskActionMatrixService()
orch = GovernanceOrchestratorExecutor()

result = orch.execute(
    project_root="/path/to/ai-os",
    gaps_path="/path/to/evidence/target_project/audit/gaps.json",
    audit_types=["code", "erp_field"],
    output_dir="/path/to/evidence/target_project/cross_project_audit",
    tag="cross_project_audit_cycle",
    governance=gov,
)

# result = {
#     "cycle_id": "gov_20260705_163740",
#     "stages_completed": ["code_audit", "evidence_writeback", "knowledge_index", "report_generated"],
#     "total_findings": 623,
#     "evidence_path": "...",
#     "report_path": "...",
#     "index_entries": 34,
# }
```

---

## Report Structure Template | 报告结构模板

每份跨项目审计报告都必须包含：

```markdown
# {Target Project} 跨项目治理审计报告

## 执行摘要
- 发现总数、严重度分布、模块覆盖

## 1. 代码审计 — 模块分布
- 逐模块拆解，附风险等级
- 受影响最严重的文件

## 2. 字段封装审计
- 字段模式违规
- FieldPackage 缺口

## 3. 修复路线图
- P0：立即修复（架构违规）
- P1：短期修复（模式补齐）
- P2：长期改进（覆盖面扩展）

## 4. 方法论洞察
- 已验证的跨项目治理模式
- 与其他被审计项目的对比
```

---

## Verification Checklist | 验证清单

在宣布某次跨项目审计完成之前：

- [ ] 已识别并消费所有既有审计数据文件
- [ ] L3 原子已执行，且未修改目标项目
- [ ] 证据文件已写入，且含完整周期元数据
- [ ] 知识索引已填充可检索条目
- [ ] 报告已生成，且包含全部必需章节
- [ ] 目标项目内没有任何文件被修改
- [ ] 审计周期 ID 已记录，可追溯

---

## Case Study: ERP Cross-Project Audit (2026-07-05) | 案例：ERP 跨项目审计（2026-07-05）

**来源**：ai-os 原子治理系统（L0–L5）
**目标**：企业级 ERP 生产仓库
**模式**：只读

**输入**：

- gaps.json：623 条代码审计发现（document_action_backend_truth_audit）
- result.json：100 条字段审计发现（field_package_truth_audit）

**流水线**：

1. L3 domain_code_audit → 623 条发现，7 个模块，含风险评分
2. L3 domain_erp_field_check → 100 条字段发现，249 个候选
3. L5 governance_orchestrator → 证据 + 索引（34 条）+ 报告

**产出**：

- 证据：cross_project_audit_20260705/evidence_gov_*.json
- 索引：knowledge_index.json（34 条）
- 报告：ERP_跨项目治理审计_20260705.md

**关键洞察**：此前 ERP 审计产生的既有审计数据可被 L3 原子直接复用 —— 无需重新扫描。L5 编排器在一次执行中把 L3 产出串联为 证据 → 索引 → 报告。

---

## 译注

- 「源版本」源文件未标注版本号；案例日期为 2026-07-05。
- 审计类型标识符 `domain_code_audit`、`domain_erp_field_check`、`domain_sql_validate`、`domain_api_test`、`domain_config_diff`，以及 `app_governance_orchestrator`、`gaps.json`、`result.json`、`casepack.json`、`knowledge_index.json` 一律保持英文原样。
- `## Rule 1/2/3` 的分级标注 `(P0)`、`(P1)`、`(P0)` 原样保留。
- `## Governance Orchestrator Usage` 的 Python 代码块（含标注为 `#` 的结果示例）整体原样复制，未作翻译；其中的 `/path/to/...` 为源文件自带的占位路径。
- 源文件 `## Report Structure Template` 中的示例报告标题原本即为中文，译文保持其原有措辞。
