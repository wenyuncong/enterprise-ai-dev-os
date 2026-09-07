#!/usr/bin/env python3
"""Audit public governance JSON Schema contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SCHEMA_DIR = Path("docs") / "全项目总控" / "schemas" / "governance"


@dataclass
class Issue:
    severity: str
    code: str
    path: Path
    message: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def rel(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def schema_files(root: Path) -> list[Path]:
    base = root / SCHEMA_DIR
    if not base.exists():
        return []
    return sorted(base.glob("*.schema.json"))


def extract_readme_schema_refs(readme: Path) -> set[str]:
    if not readme.exists():
        return set()
    text = read_text(readme)
    return set(re.findall(r"`([^`]+\.schema\.json)`", text))


def audit(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    base = root / SCHEMA_DIR
    readme = base / "README.md"
    files = schema_files(root)

    if not base.exists():
        return [Issue("FAIL", "SCHEMA_DIR_MISSING", SCHEMA_DIR, "governance schema directory is missing.")]

    if not readme.exists():
        issues.append(Issue("FAIL", "README_MISSING", rel(readme, root), "schema README is required."))

    if not files:
        issues.append(Issue("FAIL", "SCHEMA_EMPTY", rel(base, root), "no *.schema.json files found."))

    ids: dict[str, Path] = {}
    filenames = {path.name for path in files}
    for path in files:
        try:
            data = json.loads(read_text(path))
        except Exception as exc:
            issues.append(Issue("FAIL", "SCHEMA_JSON_INVALID", rel(path, root), f"invalid JSON: {exc}"))
            continue

        schema_id = data.get("$id")
        title = data.get("title")
        if not schema_id:
            issues.append(Issue("FAIL", "SCHEMA_ID_MISSING", rel(path, root), "$id is required."))
        elif schema_id in ids:
            issues.append(Issue("FAIL", "SCHEMA_ID_DUPLICATE", rel(path, root), f"$id duplicates {rel(ids[schema_id], root)}."))
        else:
            ids[schema_id] = path

        if not title:
            issues.append(Issue("FAIL", "SCHEMA_TITLE_MISSING", rel(path, root), "title is required."))
        if data.get("type") != "object":
            issues.append(Issue("FAIL", "SCHEMA_TYPE", rel(path, root), "top-level type must be object."))
        if data.get("additionalProperties") is not False:
            issues.append(Issue("FAIL", "SCHEMA_ADDITIONAL_PROPERTIES", rel(path, root), "top-level additionalProperties must be false."))
        if not data.get("required"):
            issues.append(Issue("FAIL", "SCHEMA_REQUIRED_MISSING", rel(path, root), "top-level required fields are required."))

    readme_refs = extract_readme_schema_refs(readme)
    for missing in sorted(readme_refs - filenames):
        issues.append(Issue("FAIL", "README_STALE_REF", rel(readme, root), f"README references missing schema: {missing}"))
    for unlisted in sorted(filenames - readme_refs):
        issues.append(Issue("FAIL", "README_MISSING_REF", rel(readme, root), f"README does not list schema: {unlisted}"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit public governance JSON Schema contracts.")
    parser.add_argument("--project-root", default=".", help="Repository root.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    issues = audit(root)
    result = {
        "projectRoot": str(root),
        "schemaDir": str(SCHEMA_DIR).replace("\\", "/"),
        "passed": not any(issue.severity == "FAIL" for issue in issues),
        "failCount": sum(1 for issue in issues if issue.severity == "FAIL"),
        "warnCount": sum(1 for issue in issues if issue.severity == "WARN"),
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
        status = "PASS" if result["passed"] else "FAIL"
        print(f"Governance schema audit: {status}")
        print(f"Failures: {result['failCount']} | Warnings: {result['warnCount']}")
        for issue in issues:
            print(f"[{issue.severity}] {issue.code} {str(issue.path).replace(chr(92), '/')}: {issue.message}")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
