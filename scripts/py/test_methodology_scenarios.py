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
RESPONSIBILITY_MATRIX = Path("docs/全项目总控/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md")
AUDIT_SCRIPT = Path("scripts/py/audit_methodology.py")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def assert_contains(path: Path, required_terms: list[str]) -> list[str]:
    text = read_text(path).lower()
    return [term for term in required_terms if term.lower() not in text]


def write_fixture(root: Path, include_safety: bool) -> None:
    (root / "skills/core/ai-5s-delivery-governor").mkdir(parents=True)
    (root / "skills/core/ai-product-directed-delivery").mkdir(parents=True)
    (root / "rules").mkdir(parents=True)
    (root / "docs/全项目总控").mkdir(parents=True)
    (root / "docs/_templates/全项目总控").mkdir(parents=True)
    (root / "scripts/py").mkdir(parents=True)

    five_s = """---
name: ai-5s-delivery-governor
description: "Use for Scope Specify Ship Safeguard Sell delivery governance."
---
# 5S
Scope Specify Ship Safeguard Sell L0 L3 complete blocked.
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
"""
    product = f"""---
name: ai-product-directed-delivery
description: "Use for product owner AI delivery workflow and guardrails."
---
# Product Delivery
{product_terms}
Workflow guardrails: do not bypass checks.
"""
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
                "name": "ai-product-directed-delivery",
                "layer": "core",
                "path": "skills/core/ai-product-directed-delivery/SKILL.md",
                "maturity": "verified",
            },
        ],
    }
    (root / "skills/SKILL_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
    (root / "skills/core/ai-5s-delivery-governor/SKILL.md").write_text(five_s, encoding="utf-8")
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
product acceptance
delivery closure
""",
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

    temp_root = Path(tempfile.mkdtemp(prefix="methodology-scenarios-"))
    try:
        complete_fixture = temp_root / "complete"
        incomplete_fixture = temp_root / "missing-safety"
        write_fixture(complete_fixture, include_safety=True)
        write_fixture(incomplete_fixture, include_safety=False)

        complete_exit, complete_result = run_audit(root, complete_fixture)
        incomplete_exit, incomplete_result = run_audit(root, incomplete_fixture)
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

    failures: list[str] = []
    if missing_template:
        failures.append(f"task template missing: {', '.join(missing_template)}")
    if missing_matrix:
        failures.append(f"responsibility matrix missing: {', '.join(missing_matrix)}")
    if complete_exit != 0 or not complete_result.get("passed"):
        failures.append("complete fixture did not pass methodology audit")
    if incomplete_exit == 0 or incomplete_result.get("passed"):
        failures.append("missing-safety fixture was not rejected by methodology audit")
    if not any(issue.get("code") == "PRODUCT_DELIVERY_SKILL_STRUCTURE" for issue in incomplete_result.get("issues", [])):
        failures.append("missing-safety fixture did not fail product delivery skill structure check")
    if not any(issue.get("code") == "PRODUCT_DELIVERY_RULES" for issue in incomplete_result.get("issues", [])):
        failures.append("missing-safety fixture did not fail canonical rules check")

    result = {
        "passed": not failures,
        "scenarios": {
            "product_delivery_task_template": {"passed": not missing_template, "missing": missing_template},
            "skill_responsibility_matrix": {"passed": not missing_matrix, "missing": missing_matrix},
            "complete_fixture": {"passed": complete_result.get("passed"), "exitCode": complete_exit},
            "missing_safety_fixture_rejected": {
                "passed": not incomplete_result.get("passed") and incomplete_exit != 0,
                "exitCode": incomplete_exit,
                "issueCodes": [issue.get("code") for issue in incomplete_result.get("issues", [])],
            },
        },
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
