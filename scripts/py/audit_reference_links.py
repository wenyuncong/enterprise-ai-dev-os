#!/usr/bin/env python3
"""Audit repository-relative asset references in Markdown documentation.

The audit is report-only by default. ``--strict-missing`` exits non-zero only
for a high-confidence missing asset, not for examples, generated local state,
or paths a target project creates after installation.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


REFERENCE_RE = re.compile(
    r"`?((?:skills|scripts|docs|rules|methodology|tools|lite)/[A-Za-z0-9_./\-一-鿿]+)"
)
TRAILING = ".,);:`"
GENERATED_OR_TEMPLATE = (
    re.compile(r"^tools/tool-registry\.json$"),
    re.compile(r"^skills/platform/?$"),
    re.compile(r"^docs/(架构决策记录|业务流程全案|部署运维手册|测试验收报告|每日调研回写)(/|$)"),
    re.compile(r"^docs/(copilot|rules|devops|upgrade-guide|tests)(/|$)"),
    re.compile(r"^scripts/(bat|ps1|logs)(/|$)"),
    re.compile(r"^rules/(project_rules|enterprise-ai-dev-os)\.(md|mdc)$"),
    re.compile(r"^skills/governance/ai-runtime-verify/screenshots/"),
    re.compile(r"^docs/(报表规划任务包_\d{8}|业务流程全案模板)/?"),
    re.compile(r"^docs/公开材料/"),
)
PLACEHOLDER = re.compile(r"XXX|YYYY|\{|\}|\*|/ci$|docs/spec$|lite/full$", re.IGNORECASE)
EXCLUDED_DOCUMENT_PREFIXES = (
    ".agents/",
    ".claude/",
    ".cline/",
    ".codebuddy/",
    ".continue/",
    ".cursor/",
    ".lingma/",
    ".qoder/",
    ".roo/",
    ".trae/",
    ".windsurf/",
    "docs/内部商业化/",
    "docs/商业化/",
    "docs/每日调研回写/",
    "docs/测试验收报告/",
    "reference/",
    "备用/",
    "temp/",
    "tmp/",
    "verification-demo/",
)


def classify(path: str) -> str:
    if PLACEHOLDER.search(path):
        return "placeholder"
    if any(pattern.search(path) for pattern in GENERATED_OR_TEMPLATE):
        return "generated_or_template"
    return "missing_asset"


def public_markdown_files(root: Path) -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        error = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(error or "git ls-files failed")
    paths = []
    for raw in completed.stdout.split(b"\0"):
        if not raw:
            continue
        relative = raw.decode("utf-8", errors="strict").replace("\\", "/")
        if relative.startswith(EXCLUDED_DOCUMENT_PREFIXES):
            continue
        paths.append(root / relative)
    return paths


def scan(root: Path) -> tuple[dict[str, dict[str, list[str]]], int]:
    findings: dict[str, defaultdict[str, set[str]]] = {
        "missing_asset": defaultdict(set),
        "generated_or_template": defaultdict(set),
        "placeholder": defaultdict(set),
    }
    reference_count = 0

    for document in public_markdown_files(root):
        text = document.read_text(encoding="utf-8-sig", errors="ignore")
        relative_document = document.relative_to(root).as_posix()
        for match in REFERENCE_RE.finditer(text):
            raw = match.group(1).strip(TRAILING).split("#", maxsplit=1)[0]
            if not raw:
                continue
            reference_count += 1
            if (root / raw).exists():
                continue
            findings[classify(raw)][relative_document].add(raw)

    normalized = {
        category: {
            document: sorted(paths)
            for document, paths in sorted(grouped.items())
        }
        for category, grouped in findings.items()
    }
    return normalized, reference_count


def count(grouped: dict[str, list[str]]) -> int:
    return sum(len(paths) for paths in grouped.values())


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit repository-relative Markdown references.")
    parser.add_argument("--project-root", default=".", help="Repository root.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--strict-missing", action="store_true", help="Fail when a concrete shipped asset is missing.")
    args = parser.parse_args()

    findings, references = scan(Path(args.project_root).resolve())
    counts = {category: count(grouped) for category, grouped in findings.items()}
    result = {"referenceCount": references, "counts": counts, "findings": findings}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Reference-link audit: scanned {references} repository-relative references")
        for category, total in counts.items():
            print(f"  {category:<22}: {total}")
        for document, paths in findings["missing_asset"].items():
            for path in paths:
                print(f"  missing: {document} -> {path}")

    if args.strict_missing and counts["missing_asset"]:
        print(f"FAIL: {counts['missing_asset']} concrete asset reference(s) unresolved.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
