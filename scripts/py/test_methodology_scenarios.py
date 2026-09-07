#!/usr/bin/env python3
"""Run focused scenario regressions for the AI development methodology."""

from __future__ import annotations

import argparse
import json
import locale
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


TASK_TEMPLATE = Path("docs/_templates/全项目总控/AI_PRODUCT_DELIVERY_TASK_TEMPLATE.md")
MIGRATION_TEMPLATE = Path("docs/_templates/部署运维手册/DATABASE_MIGRATION_GATE_TEMPLATE.md")
TENANT_TEMPLATE = Path("docs/_templates/测试验收报告/TENANT_LIFECYCLE_REGRESSION_TEMPLATE.md")
RESPONSIBILITY_MATRIX = Path("docs/全项目总控/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md")
AUDIT_SCRIPT = Path("scripts/py/audit_methodology.py")
CONTRACT_TEMPLATE = Path("docs/_templates/全项目总控/task_contract.json")
CONTRACT_VALIDATOR = Path("scripts/py/validate_delivery_contract.py")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def assert_contains(path: Path, required_terms: list[str]) -> list[str]:
    text = read_text(path).lower()
    return [term for term in required_terms if term.lower() not in text]


def write_fixture(
    root: Path,
    include_safety: bool,
    include_control_character: bool = False,
    include_operating_assets: bool = True,
) -> None:
    (root / "skills/core/ai-5s-delivery-governor").mkdir(parents=True)
    (root / "skills/core/ai-delivery-contract-governor").mkdir(parents=True)
    (root / "skills/core/ai-product-directed-delivery").mkdir(parents=True)
    (root / "rules").mkdir(parents=True)
    (root / "docs/全项目总控").mkdir(parents=True)
    (root / "docs/全项目总控/schemas/digital-life").mkdir(parents=True)
    (root / "docs/_templates/全项目总控").mkdir(parents=True)
    (root / "scripts/py").mkdir(parents=True)

    five_s = """---
name: ai-5s-delivery-governor
description: "Use for Scope Specify Ship Safeguard Sell delivery governance."
---
# 5S
Scope Specify Ship Safeguard Sell L0 L3 Q0 Q1 Q2 Q3 qualification saleability complete blocked.
"""
    product_terms = """
product owner
atomic service
atomic orchestration
aggregate interface
command gateway
ui atom
host page
business-flow acceptance
"""
    if include_safety:
        product_terms += """
safe change
code location
working-tree
destructive
impact
exact task-owned
business ambiguity
shared language
fresh evidence
two independent axes
"""
    product = f"""---
name: ai-product-directed-delivery
description: "Use for product owner AI delivery workflow and guardrails."
---
# Product Delivery
{product_terms}
Workflow guardrails: do not bypass checks.
"""
    delivery_contract = """---
name: ai-delivery-contract-governor
description: "Use for write allowlist, fresh evidence, independent review, and fail-closed delivery contracts."
---
# Delivery Contract
write allowlist
fresh evidence
independent verifier
safeguarded
completed
fail-closed
validate_delivery_contract.py
"""
    if include_control_character:
        product += "\x07"
    rules = """# Rules
## 5S Delivery Governance
Scope -> Specify -> Ship -> Safeguard -> Sell
## Product-Directed AI Delivery
command gateway
"""
    if include_safety:
        rules += """
## Safe AI Change and Code Location
Read, prove, then change.
Use exact file or hunk staging.
Escalate business ambiguity.
## Evidence Freshness, Shared Language, and Two-Axis Review
Fresh evidence before claims.
Review two independent axes.
## Executable Delivery Contract
ai-delivery-contract-governor
DeliveryContract
write allowlist
verification_owner
fail-closed
## Delivery Roles, Task Pack, and Methodology Regression
AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md
AI_PRODUCT_DELIVERY_TASK_TEMPLATE.md
test_methodology_scenarios.py
"""

    manifest = {
        "officialSkillRoot": "skills/",
        "officialSkills": [
            {
                "name": "ai-5s-delivery-governor",
                "layer": "core",
                "path": "skills/core/ai-5s-delivery-governor/SKILL.md",
                "maturity": "verified",
            },
            {
                "name": "ai-delivery-contract-governor",
                "layer": "core",
                "path": "skills/core/ai-delivery-contract-governor/SKILL.md",
                "maturity": "verified",
            },
            {
                "name": "ai-product-directed-delivery",
                "layer": "core",
                "path": "skills/core/ai-product-directed-delivery/SKILL.md",
                "maturity": "verified",
            },
        ],
    }
    (root / "skills/SKILL_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
    (root / "skills/core/ai-5s-delivery-governor/SKILL.md").write_text(five_s, encoding="utf-8")
    (root / "skills/core/ai-delivery-contract-governor/SKILL.md").write_text(delivery_contract, encoding="utf-8")
    (root / "skills/core/ai-product-directed-delivery/SKILL.md").write_text(product, encoding="utf-8")
    (root / "rules/AGENTS.md").write_text(rules, encoding="utf-8")
    (root / "AGENTS.md").write_text("# Generated rules\n", encoding="utf-8")
    if include_safety:
        (root / "docs/全项目总控/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md").write_text(
            """# Matrix
one primary owner
ai-rule-dispatcher
ai-chief-planner
ai-task-decomposer
ai-delivery-contract-governor
ai-product-directed-delivery
ai-5s-delivery-governor
ai-runtime-verify
""",
            encoding="utf-8",
        )
        (root / "docs/_templates/全项目总控/AI_PRODUCT_DELIVERY_TASK_TEMPLATE.md").write_text(
            """# Task Pack
product owner input
code location and truth map
delete / rename / migration classification
executable batches
verification record
fresh final evidence
two-axis review
product acceptance
delivery closure
delivery qualification
capability maturity
database migration consistency gate
tenant lifecycle regression
""",
            encoding="utf-8",
        )
        (root / "docs/_templates/全项目总控/task_contract.json").write_text(
            """{"contract_id":"dc_fixture","schema_version":"1.0","status":"scoped","project_id":"fixture","delivery":{"gate":"L2"},"product_contract":{"outcome":"outcome","acceptance_steps":["accept"],"non_goals":["non-goal"]},"truth_owner":"owner","scope":{"write_allowlist":["src/**"],"out_of_scope":["out"],"destructive_classification":"none"},"test_strategy":{"mode":"red_green","public_seam":"public seam","rationale":"reason","focused_test_command":"test"},"evidence_plan":{"final_proofs":[{"proof_id":"proof_fixture","claim":"claim","command_or_check":"test","must_run_after_final_change":true}]},"reviews":{"standards_truth":{"status":"pending","evidence":"pending"},"product_spec":{"status":"pending","evidence":"pending"}},"implementer":"implementer","created_at":"2026-08-21T00:00:00Z","updated_at":"2026-08-21T00:00:00Z"}""",
            encoding="utf-8",
        )
        (root / "docs/全项目总控/schemas/digital-life/delivery-contract.schema.json").write_text(
            """{"title":"DeliveryContract","additionalProperties":false,"properties":{"delivery":{},"product_contract":{},"truth_owner":{},"scope":{},"test_strategy":{},"evidence_plan":{},"reviews":{}}}""",
            encoding="utf-8",
        )
        if include_operating_assets:
            (root / "docs/_templates/部署运维手册").mkdir(parents=True, exist_ok=True)
            (root / "docs/_templates/测试验收报告").mkdir(parents=True, exist_ok=True)
            (root / MIGRATION_TEMPLATE).write_text(
                """# Database Migration Consistency Gate
Migration Identity checksum Environment Registration Execution History Post-Migration Checks Recovery.
""",
                encoding="utf-8",
            )
            (root / TENANT_TEMPLATE).write_text(
                """# Tenant Lifecycle Regression
Tenant Lifecycle Regression Load Profile Authoritative Facts Audit Rollback / Residue Cross-tenant access is denied.
""",
                encoding="utf-8",
            )
        (root / "scripts/py/validate_delivery_contract.py").write_text(
            "# delivery contract validator placeholder\n",
            encoding="utf-8",
        )
        (root / "scripts/py/test_methodology_scenarios.py").write_text(
            "# scenario regression placeholder\n",
            encoding="utf-8",
        )


def run_audit(repo_root: Path, fixture: Path) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(repo_root / AUDIT_SCRIPT), "--project-root", str(fixture), "--json"],
        capture_output=True,
        check=False,
    )
    encoding = locale.getpreferredencoding(False) or "utf-8"
    stdout = completed.stdout.decode(encoding, errors="replace")
    return completed.returncode, json.loads(stdout)


def run_contract_validator(repo_root: Path, contract: Path, *args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(repo_root / CONTRACT_VALIDATOR), "--contract", str(contract), "--json", *args],
        capture_output=True,
        check=False,
    )
    encoding = locale.getpreferredencoding(False) or "utf-8"
    stdout = completed.stdout.decode(encoding, errors="replace")
    return completed.returncode, json.loads(stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run methodology scenario regressions.")
    parser.add_argument("--project-root", default=".", help="Methodology repository root.")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()

    missing_template = assert_contains(
        root / TASK_TEMPLATE,
        [
            "product owner input",
            "code location and truth map",
            "delete / rename / migration classification",
            "executable batches",
            "verification record",
            "fresh final evidence",
            "two-axis review",
            "product acceptance",
            "delivery closure",
        ],
    )
    missing_matrix = assert_contains(
        root / RESPONSIBILITY_MATRIX,
        [
            "ai-rule-dispatcher",
            "ai-chief-planner",
            "ai-task-decomposer",
            "ai-product-directed-delivery",
            "ai-5s-delivery-governor",
            "ai-runtime-verify",
            "one primary owner",
        ],
    )
    missing_contract_template = assert_contains(
        root / CONTRACT_TEMPLATE,
        [
            "write_allowlist",
            "non_goals",
            "test_strategy",
            "final_proofs",
            "standards_truth",
            "product_spec",
        ],
    )
    missing_migration_template = assert_contains(
        root / MIGRATION_TEMPLATE,
        ["migration identity", "checksum", "environment registration", "execution history", "post-migration checks", "recovery"],
    )
    missing_tenant_template = assert_contains(
        root / TENANT_TEMPLATE,
        ["tenant lifecycle regression", "load profile", "authoritative facts", "audit", "rollback / residue", "cross-tenant access is denied"],
    )

    temp_root = Path(tempfile.mkdtemp(prefix="methodology-scenarios-"))
    try:
        complete_fixture = temp_root / "complete"
        incomplete_fixture = temp_root / "missing-safety"
        missing_assets_fixture = temp_root / "missing-operating-assets"
        control_character_fixture = temp_root / "control-character"
        write_fixture(complete_fixture, include_safety=True)
        write_fixture(incomplete_fixture, include_safety=False)
        write_fixture(missing_assets_fixture, include_safety=True, include_operating_assets=False)
        write_fixture(control_character_fixture, include_safety=True, include_control_character=True)

        complete_exit, complete_result = run_audit(root, complete_fixture)
        incomplete_exit, incomplete_result = run_audit(root, incomplete_fixture)
        missing_assets_exit, missing_assets_result = run_audit(root, missing_assets_fixture)
        control_exit, control_result = run_audit(root, control_character_fixture)

        valid_contract = json.loads(read_text(root / CONTRACT_TEMPLATE))
        valid_contract["status"] = "safeguarded"
        valid_contract["verification_owner"] = "independent-verifier"
        valid_contract["reviews"]["standards_truth"] = {"status": "passed", "evidence": "scoped diff reviewed"}
        valid_contract["reviews"]["product_spec"] = {"status": "passed", "evidence": "acceptance replayed"}
        valid_contract["evidence_plan"]["last_relevant_change_at"] = "2026-08-21T00:00:00Z"
        valid_contract["evidence_plan"]["evidence_records"] = [
            {
                "proof_id": "proof_example_runtime",
                "status": "passed",
                "finished_at": "2026-08-21T00:01:00Z",
                "reference": "focused runtime test",
            }
        ]
        valid_path = temp_root / "valid-contract.json"
        valid_path.write_text(json.dumps(valid_contract), encoding="utf-8")
        valid_exit, valid_result = run_contract_validator(root, valid_path, "--check-freshness", "--changed-file", "src/example/feature.ts")

        scope_exit, scope_result = run_contract_validator(root, valid_path, "--changed-file", "secrets/production.env")

        self_review = dict(valid_contract)
        self_review["verification_owner"] = self_review["implementer"]
        self_review_path = temp_root / "self-review-contract.json"
        self_review_path.write_text(json.dumps(self_review), encoding="utf-8")
        self_review_exit, self_review_result = run_contract_validator(root, self_review_path)

        stale_evidence = json.loads(json.dumps(valid_contract))
        stale_evidence["evidence_plan"]["evidence_records"][0]["finished_at"] = "2026-08-20T23:59:59Z"
        stale_path = temp_root / "stale-contract.json"
        stale_path.write_text(json.dumps(stale_evidence), encoding="utf-8")
        stale_exit, stale_result = run_contract_validator(root, stale_path, "--check-freshness")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

    failures: list[str] = []
    if missing_template:
        failures.append(f"task template missing: {', '.join(missing_template)}")
    if missing_matrix:
        failures.append(f"responsibility matrix missing: {', '.join(missing_matrix)}")
    if missing_contract_template:
        failures.append(f"delivery contract template missing: {', '.join(missing_contract_template)}")
    if missing_migration_template:
        failures.append(f"migration gate template missing: {', '.join(missing_migration_template)}")
    if missing_tenant_template:
        failures.append(f"tenant regression template missing: {', '.join(missing_tenant_template)}")
    if complete_exit != 0 or not complete_result.get("passed"):
        failures.append("complete fixture did not pass methodology audit")
    if incomplete_exit == 0 or incomplete_result.get("passed"):
        failures.append("missing-safety fixture was not rejected by methodology audit")
    if not any(issue.get("code") == "PRODUCT_DELIVERY_SKILL_STRUCTURE" for issue in incomplete_result.get("issues", [])):
        failures.append("missing-safety fixture did not fail product delivery skill structure check")
    if not any(issue.get("code") == "PRODUCT_DELIVERY_RULES" for issue in incomplete_result.get("issues", [])):
        failures.append("missing-safety fixture did not fail canonical rules check")
    if missing_assets_exit == 0 or missing_assets_result.get("passed"):
        failures.append("missing-operating-assets fixture was not rejected by methodology audit")
    if not any(issue.get("code") == "DELIVERY_OPERATING_ASSET_MISSING" for issue in missing_assets_result.get("issues", [])):
        failures.append("missing-operating-assets fixture did not fail operating asset check")
    if control_exit == 0 or control_result.get("passed"):
        failures.append("control-character fixture was not rejected by methodology audit")
    if not any(issue.get("code") == "CONTROL_CHARACTER" for issue in control_result.get("issues", [])):
        failures.append("control-character fixture did not fail control-character check")
    if valid_exit != 0 or not valid_result.get("passed"):
        failures.append("valid safeguarded delivery contract did not pass")
    if scope_exit == 0 or scope_result.get("passed") or not any(
        issue.get("code") == "CONTRACT_SCOPE_ESCAPE" for issue in scope_result.get("issues", [])
    ):
        failures.append("scope escape was not rejected by delivery contract validator")
    if self_review_exit == 0 or self_review_result.get("passed") or not any(
        issue.get("code") == "CONTRACT_INDEPENDENT_VERIFIER" for issue in self_review_result.get("issues", [])
    ):
        failures.append("L2 self-review was not rejected by delivery contract validator")
    if stale_exit == 0 or stale_result.get("passed") or not any(
        issue.get("code") == "CONTRACT_STALE_EVIDENCE" for issue in stale_result.get("issues", [])
    ):
        failures.append("stale final evidence was not rejected by delivery contract validator")

    result = {
        "passed": not failures,
        "scenarios": {
            "product_delivery_task_template": {"passed": not missing_template, "missing": missing_template},
            "skill_responsibility_matrix": {"passed": not missing_matrix, "missing": missing_matrix},
            "delivery_contract_template": {"passed": not missing_contract_template, "missing": missing_contract_template},
            "migration_gate_template": {"passed": not missing_migration_template, "missing": missing_migration_template},
            "tenant_regression_template": {"passed": not missing_tenant_template, "missing": missing_tenant_template},
            "complete_fixture": {"passed": complete_result.get("passed"), "exitCode": complete_exit},
            "missing_safety_fixture_rejected": {
                "passed": not incomplete_result.get("passed") and incomplete_exit != 0,
                "exitCode": incomplete_exit,
                "issueCodes": [issue.get("code") for issue in incomplete_result.get("issues", [])],
            },
            "missing_operating_assets_fixture_rejected": {
                "passed": not missing_assets_result.get("passed") and missing_assets_exit != 0,
                "exitCode": missing_assets_exit,
                "issueCodes": [issue.get("code") for issue in missing_assets_result.get("issues", [])],
            },
            "control_character_fixture_rejected": {
                "passed": not control_result.get("passed") and control_exit != 0,
                "exitCode": control_exit,
                "issueCodes": [issue.get("code") for issue in control_result.get("issues", [])],
            },
            "valid_delivery_contract": {"passed": valid_result.get("passed"), "exitCode": valid_exit},
            "scope_escape_rejected": {
                "passed": not scope_result.get("passed") and scope_exit != 0,
                "issueCodes": [issue.get("code") for issue in scope_result.get("issues", [])],
            },
            "self_review_rejected": {
                "passed": not self_review_result.get("passed") and self_review_exit != 0,
                "issueCodes": [issue.get("code") for issue in self_review_result.get("issues", [])],
            },
            "stale_evidence_rejected": {
                "passed": not stale_result.get("passed") and stale_exit != 0,
                "issueCodes": [issue.get("code") for issue in stale_result.get("issues", [])],
            },
        },
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
