#!/usr/bin/env python3
"""Validate a machine-readable AI-OS delivery contract and its observed scope."""

from __future__ import annotations

import argparse
import fnmatch
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Issue:
    code: str
    message: str


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("contract root must be a JSON object")
    return value


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def matches(path: str, patterns: list[str]) -> bool:
    normalized = path.replace("\\", "/")
    return any(fnmatch.fnmatchcase(normalized, pattern.replace("\\", "/")) for pattern in patterns)


def validate(contract: dict[str, Any], changed_files: list[str], check_freshness: bool) -> list[Issue]:
    issues: list[Issue] = []
    required = {
        "contract_id",
        "schema_version",
        "status",
        "project_id",
        "delivery",
        "product_contract",
        "truth_owner",
        "scope",
        "test_strategy",
        "evidence_plan",
        "reviews",
        "implementer",
        "created_at",
        "updated_at",
    }
    missing = sorted(required - set(contract))
    if missing:
        return [Issue("CONTRACT_REQUIRED", f"missing required keys: {', '.join(missing)}")]
    if contract["schema_version"] != "1.0":
        issues.append(Issue("CONTRACT_SCHEMA_VERSION", "schema_version must be 1.0."))

    status = contract["status"]
    valid_statuses = {"draft", "scoped", "approved", "implementing", "safeguarded", "completed", "blocked", "cancelled"}
    if status not in valid_statuses:
        issues.append(Issue("CONTRACT_STATUS", f"unsupported status: {status!r}."))

    delivery = contract["delivery"]
    scope = contract["scope"]
    product = contract["product_contract"]
    test_strategy = contract["test_strategy"]
    evidence_plan = contract["evidence_plan"]
    reviews = contract["reviews"]
    if not isinstance(delivery, dict) or delivery.get("gate") not in {"L0", "L1", "L2", "L3"}:
        issues.append(Issue("CONTRACT_GATE", "delivery.gate must be L0, L1, L2, or L3."))
    if not isinstance(product, dict) or not product.get("outcome") or not product.get("acceptance_steps") or not product.get("non_goals"):
        issues.append(Issue("CONTRACT_PRODUCT", "product outcome, acceptance_steps, and non_goals are required."))
    if not isinstance(scope, dict) or not scope.get("write_allowlist") or not scope.get("out_of_scope"):
        issues.append(Issue("CONTRACT_SCOPE", "write_allowlist and out_of_scope are required."))
        return issues

    allowlist = scope["write_allowlist"]
    forbidden = scope.get("forbidden_paths", [])
    if not isinstance(allowlist, list) or not all(isinstance(item, str) and item.strip() for item in allowlist):
        issues.append(Issue("CONTRACT_ALLOWLIST", "scope.write_allowlist must contain non-empty path patterns."))
    if any(pattern.strip() in {"*", "**", "/**"} for pattern in allowlist if isinstance(pattern, str)):
        issues.append(Issue("CONTRACT_ALLOWLIST_BROAD", "write_allowlist must not contain an unrestricted repository-wide pattern."))
    if scope.get("destructive_classification") not in {"none", "review_required", "explicit_owner_confirmation"}:
        issues.append(Issue("CONTRACT_DESTRUCTIVE", "scope.destructive_classification is invalid."))
    if scope.get("destructive_classification") == "explicit_owner_confirmation" and contract.get("owner_confirmation") != "confirmed":
        issues.append(Issue("CONTRACT_OWNER_CONFIRMATION", "explicit destructive work requires owner_confirmation=confirmed."))

    if not isinstance(test_strategy, dict) or test_strategy.get("mode") not in {"red_green", "alternative_evidence"}:
        issues.append(Issue("CONTRACT_TEST_MODE", "test_strategy.mode must be red_green or alternative_evidence."))
    elif not test_strategy.get("public_seam") or not test_strategy.get("rationale"):
        issues.append(Issue("CONTRACT_TEST_SEAM", "test_strategy requires public_seam and rationale."))
    elif test_strategy["mode"] == "red_green" and not test_strategy.get("focused_test_command"):
        issues.append(Issue("CONTRACT_TEST_COMMAND", "red_green test strategy requires focused_test_command."))

    final_proofs = evidence_plan.get("final_proofs", []) if isinstance(evidence_plan, dict) else []
    if not final_proofs:
        issues.append(Issue("CONTRACT_FINAL_PROOF", "evidence_plan.final_proofs must not be empty."))
    proof_ids = set()
    for proof in final_proofs:
        if not isinstance(proof, dict):
            issues.append(Issue("CONTRACT_PROOF_SHAPE", "each final proof must be an object."))
            continue
        proof_id = proof.get("proof_id")
        if not proof_id or proof_id in proof_ids:
            issues.append(Issue("CONTRACT_PROOF_ID", "final proof ids must be unique and non-empty."))
        proof_ids.add(proof_id)
        if proof.get("must_run_after_final_change") is not True:
            issues.append(Issue("CONTRACT_FRESHNESS_DECLARATION", f"proof {proof_id!r} must require post-change execution."))
        if not proof.get("claim") or not proof.get("command_or_check"):
            issues.append(Issue("CONTRACT_PROOF_CONTENT", f"proof {proof_id!r} requires claim and command_or_check."))

    for changed in changed_files:
        if matches(changed, forbidden):
            issues.append(Issue("CONTRACT_FORBIDDEN_PATH", f"changed path is explicitly forbidden: {changed}"))
        elif not matches(changed, allowlist):
            issues.append(Issue("CONTRACT_SCOPE_ESCAPE", f"changed path is outside write_allowlist: {changed}"))

    if status in {"safeguarded", "completed"}:
        if reviews.get("standards_truth", {}).get("status") != "passed":
            issues.append(Issue("CONTRACT_STANDARDS_REVIEW", "safeguarded/completed requires standards_truth review=passed."))
        if reviews.get("product_spec", {}).get("status") != "passed":
            issues.append(Issue("CONTRACT_PRODUCT_REVIEW", "safeguarded/completed requires product_spec review=passed."))
        gate = delivery.get("gate")
        if gate in {"L2", "L3"} and contract.get("verification_owner") in {None, "", contract["implementer"]}:
            issues.append(Issue("CONTRACT_INDEPENDENT_VERIFIER", "L2/L3 safeguarded/completed requires a verification_owner different from implementer."))

    if check_freshness:
        last_change = evidence_plan.get("last_relevant_change_at")
        if not last_change:
            issues.append(Issue("CONTRACT_LAST_CHANGE", "--check-freshness requires evidence_plan.last_relevant_change_at."))
        else:
            try:
                last_change_time = parse_time(last_change)
            except ValueError:
                issues.append(Issue("CONTRACT_LAST_CHANGE_TIME", "last_relevant_change_at must be an ISO-8601 timestamp."))
                last_change_time = None
            records = {record.get("proof_id"): record for record in evidence_plan.get("evidence_records", []) if isinstance(record, dict)}
            for proof_id in proof_ids:
                record = records.get(proof_id)
                if not record or record.get("status") != "passed":
                    issues.append(Issue("CONTRACT_EVIDENCE_MISSING", f"proof {proof_id!r} has no passing evidence record."))
                    continue
                try:
                    finished_at = parse_time(record["finished_at"])
                except (KeyError, ValueError):
                    issues.append(Issue("CONTRACT_EVIDENCE_TIME", f"proof {proof_id!r} has invalid finished_at."))
                    continue
                if last_change_time and finished_at <= last_change_time:
                    issues.append(Issue("CONTRACT_STALE_EVIDENCE", f"proof {proof_id!r} predates or equals last_relevant_change_at."))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI-OS delivery contract.")
    parser.add_argument("--contract", required=True, help="Path to task_contract.json.")
    parser.add_argument("--changed-file", action="append", default=[], help="Observed repo-relative changed path; repeat as needed.")
    parser.add_argument("--changed-files-from", help="Text file with one repo-relative changed path per line.")
    parser.add_argument("--check-freshness", action="store_true", help="Require passing evidence records newer than the final relevant change.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result.")
    args = parser.parse_args()

    changed_files = list(args.changed_file)
    if args.changed_files_from:
        changed_files.extend(
            line.strip() for line in Path(args.changed_files_from).read_text(encoding="utf-8-sig").splitlines() if line.strip()
        )
    try:
        contract = read_json(Path(args.contract))
        issues = validate(contract, changed_files, args.check_freshness)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        issues = [Issue("CONTRACT_READ", str(exc))]

    result = {
        "passed": not issues,
        "contract": args.contract,
        "checkedChangedFiles": changed_files,
        "issues": [{"code": issue.code, "message": issue.message} for issue in issues],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Delivery contract: {'PASS' if result['passed'] else 'FAIL'}")
        for issue in issues:
            print(f"[{issue.code}] {issue.message}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
