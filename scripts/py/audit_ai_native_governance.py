#!/usr/bin/env python3
"""Audit the minimum machine-readable governance contracts for AI-native delivery."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path


SCHEMA_DIR = Path("docs") / "全项目总控" / "schemas" / "governance"
PROTOCOL_PATH = Path("docs") / "全项目总控" / "AI_NATIVE_CANDIDATE_CAPABILITY_PROTOCOL.md"

CONTRACTS = {
    "candidate-capability-evaluation.schema.json": {
        "title": "CandidateCapabilityEvaluation",
        "properties": {"candidate_id", "candidate_kind", "fit_assessment", "verification_plan", "decision"},
    },
    "delegation-grant.schema.json": {
        "title": "DelegationGrant",
        "properties": {"grantor", "grantee", "scope", "risk_level", "expires_at", "status"},
    },
    "execution-attestation.schema.json": {
        "title": "ExecutionAttestation",
        "properties": {"executor", "action", "environment", "outcome", "started_at", "finished_at"},
    },
    "delivery-contract.schema.json": {
        "title": "DeliveryContract",
        "properties": {
            "delivery",
            "product_contract",
            "truth_owner",
            "scope",
            "test_strategy",
            "evidence_plan",
            "reviews",
        },
    },
}


@dataclass
class Issue:
    severity: str
    code: str
    path: Path
    message: str


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def audit(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    protocol = root / PROTOCOL_PATH
    if not protocol.exists():
        issues.append(Issue("FAIL", "PROTOCOL_MISSING", PROTOCOL_PATH, "candidate capability protocol is required."))

    for filename, expected in CONTRACTS.items():
        path = root / SCHEMA_DIR / filename
        if not path.exists():
            issues.append(Issue("FAIL", "CONTRACT_MISSING", path.relative_to(root), "required governance schema is missing."))
            continue
        try:
            data = read_json(path)
        except Exception as exc:
            issues.append(Issue("FAIL", "CONTRACT_JSON_INVALID", path.relative_to(root), f"invalid JSON: {exc}"))
            continue

        if data.get("title") != expected["title"]:
            issues.append(
                Issue(
                    "FAIL",
                    "CONTRACT_TITLE",
                    path.relative_to(root),
                    f"expected title {expected['title']!r}, found {data.get('title')!r}.",
                )
            )
        if data.get("additionalProperties") is not False:
            issues.append(Issue("FAIL", "CONTRACT_ADDITIONAL_PROPERTIES", path.relative_to(root), "top-level additionalProperties must be false."))
        missing = expected["properties"] - set(data.get("properties", {}))
        if missing:
            issues.append(
                Issue(
                    "FAIL",
                    "CONTRACT_REQUIRED_PROPERTIES",
                    path.relative_to(root),
                    f"missing required governance properties: {', '.join(sorted(missing))}.",
                )
            )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AI-native governance contracts.")
    parser.add_argument("--project-root", default=".", help="Repository root.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    issues = audit(root)
    result = {
        "projectRoot": str(root),
        "passed": not any(issue.severity == "FAIL" for issue in issues),
        "failCount": sum(1 for issue in issues if issue.severity == "FAIL"),
        "issues": [
            {
                "severity": issue.severity,
                "code": issue.code,
                "path": str(issue.path).replace("\\", "/"),
                "message": issue.message,
            }
            for issue in issues
        ],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"AI-native governance audit: {'PASS' if result['passed'] else 'FAIL'}")
        print(f"Failures: {result['failCount']}")
        for issue in issues:
            print(f"[{issue.severity}] {issue.code} {str(issue.path).replace(chr(92), '/')}: {issue.message}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
