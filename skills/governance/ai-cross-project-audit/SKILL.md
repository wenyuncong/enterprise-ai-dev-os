---
name: ai-cross-project-audit
description: "Cross-project governance audit pipeline: consume existing audit data, orchestrate L3 domain atoms, produce L5 evidence + index + report. Supports read-only (report only) and active (modify target) modes. Use when auditing one project from another project's atomic governance system."
---

# ai-cross-project-audit — Cross-Project Governance Auditor

## Purpose

Orchestrate governance audits across independent projects using an atomic governance system. This skill enables the pattern: **one project's atomic system audits another project's codebase** — without modifying the target.

**Problem it solves**: Governance audits are typically siloed within a single project. Cross-project audits require manual data transfer, inconsistent formats, and no reusable pipeline. This skill defines the standard pipeline for consuming existing audit data, orchestrating multi-source findings, and producing unified governance reports.

---

## The Pipeline

`
Existing Audit Data (gaps.json, result.json)
        │
        ▼
┌───────────────────────────────────┐
│  L3 Domain Atoms                  │
│  domain_code_audit                │
│  domain_erp_field_check           │
│  domain_sql_validate              │
│  domain_api_test                  │
│  domain_config_diff               │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  L5 Governance Orchestrator       │
│  app_governance_orchestrator      │
│  audit → evidence → index → report│
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  Outputs                          │
│  evidence.json  (audit trail)     │
│  knowledge_index.json (searchable)│
│  report.md      (human readable)  │
└───────────────────────────────────┘
`

---

## Rule 1: Read-Only by Default (P0)

When auditing another project, default to **read-only mode**:

- Consume existing audit data files (no re-scan of target)
- Produce reports and recommendations
- Do NOT modify target project code
- Tag all evidence with source project and audit cycle ID

**Exception**: If the audited project's team explicitly requests active remediation, switch to active mode with explicit scope boundaries.

---

## Rule 2: Data Reuse (P1)

Before generating new audit data, search for existing audit outputs in the evidence directory:

`
evidence/{target_project}/
  {audit_name}/
    gaps.json        ← code audit findings
    result.json      ← field/rule audit results
    casepack.json    ← review queue / recommendations
`

Existing data can be directly consumed by L3 atoms without re-scanning the target project. This saves computation and ensures audit consistency.

---

## Rule 3: Evidence Chain Integrity (P0)

Every cross-project audit must produce a complete evidence chain:

| Stage | Output | Verification |
|-------|--------|-------------|
| 1. Audit | Structured findings from L3 atoms | Findings count > 0 |
| 2. Evidence | JSON file with cycle_id, stages, findings_sample | File exists and is valid JSON |
| 3. Index | JSON index with searchable entries | entries_added > 0 |
| 4. Report | Markdown report with executive summary | Report path exists |

---

## Audit Types

### Code Audit (domain_code_audit)

Consumes gaps.json with findings like:
- direct_db_write_in_controller
- action_endpoint_without_command_pattern

Produces: module-grouped finding groups, risk scores, remediation recommendations.

### Field Audit (domain_erp_field_check)

Consumes result.json from field_package_truth_audit rulepack.

Produces: field pattern violations, FieldPackage gaps, frontend duplicate field definitions.

### SQL Audit (domain_sql_validate)

Consumes SQL migration files.

Produces: schema drift, missing migrations, naming convention violations.

### API Audit (domain_api_test)

Consumes API endpoint list.

Produces: endpoint health, response schema consistency, auth coverage.

### Config Audit (domain_config_diff)

Consumes configuration files.

Produces: environment drift, missing tenant configs, hardcoded values.

---

## Governance Orchestrator Usage

`python
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
`

---

## Report Structure Template

Every cross-project audit report must include:

`markdown
# {Target Project} 跨项目治理审计报告

## 执行摘要
- Total findings, severity distribution, module coverage

## 1. 代码审计 — 模块分布
- Per-module breakdown with risk levels
- Top affected files

## 2. 字段封装审计
- Field pattern violations
- FieldPackage gaps

## 3. 修复路线图
- P0: Immediate fixes (architecture violations)
- P1: Short-term fixes (pattern completion)
- P2: Long-term improvements (coverage expansion)

## 4. 方法论洞察
- Cross-project governance patterns validated
- Comparison with other audited projects
`

---

## Verification Checklist

Before declaring a cross-project audit complete:

- [ ] All existing audit data files identified and consumed
- [ ] L3 atoms executed without modifying target project
- [ ] Evidence file written with complete cycle metadata
- [ ] Knowledge index populated with searchable entries
- [ ] Report generated with all required sections
- [ ] No files modified in target project
- [ ] Audit cycle ID recorded for traceability

---

## Case Study: GERP Cross-Project Audit (2026-07-05)

**Source**: ai-os atomic governance system (L0-L5)
**Target**: GERP enterprise mainline (H:\gerp-enterprise-mainline)
**Mode**: Read-only

**Inputs**:
- gaps.json: 623 code audit findings (document_action_backend_truth_audit)
- result.json: 100 field audit findings (field_package_truth_audit)

**Pipeline**:
1. L3 domain_code_audit → 623 findings, 7 modules, risk scores
2. L3 domain_erp_field_check → 100 field findings, 249 candidates
3. L5 governance_orchestrator → evidence + index (34 entries) + report

**Output**:
- Evidence: cross_project_audit_20260705/evidence_gov_*.json
- Index: knowledge_index.json (34 entries)
- Report: GERP_跨项目治理审计_20260705.md

**Key insight**: Existing audit data from previous GERP audits was directly reusable by L3 atoms — no re-scanning required. The L5 orchestrator chained L3 outputs through evidence → index → report in a single execution.