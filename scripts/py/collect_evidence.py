#!/usr/bin/env python3
"""Collect structured delivery evidence for the methodology.

Runs the verification suite and stores machine-readable evidence under
evidence/runs/<timestamp>/ so value claims (first-pass completion, rework,
defect escape, verification coverage) can be tracked over time instead of
staying TBD.

Commands:
  collect_evidence.py --run [--project-root .]   run all checks, save evidence
  collect_evidence.py --task NAME [--project-root .]  record a task-level
                      before/after evidence file from an interactive template
  collect_evidence.py --compare [--project-root .]    diff vs the latest run

Exit code: 1 if any check fails, otherwise 0.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

CHECKS = [
    {"key": "audit_methodology", "name": "方法论审计", "script": "scripts/py/audit_methodology.py", "args": []},
    {"key": "methodology_scenarios", "name": "方法论场景回归", "script": "scripts/py/test_methodology_scenarios.py", "args": []},
    {"key": "open_source_boundary", "name": "开源边界", "script": "scripts/py/check_open_source_boundary.py", "args": []},
    {"key": "readiness_score", "name": "就绪评分", "script": "scripts/py/score_ai_development_readiness.py", "args": ["--json"]},
    {"key": "rule_lint", "name": "规则 Lint", "script": "scripts/py/rule_lint.py", "args": ["--json"]},
    {"key": "cli_syntax", "name": "CLI 语法", "cmd": ["node", "--check", "scripts/js/cli.mjs"], "args": []},
]


def git_head(root: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=30)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def git_status_short(root: Path) -> list[str]:
    try:
        out = subprocess.run(["git", "-C", str(root), "status", "--short"],
                             capture_output=True, text=True, timeout=30)
        return [l for l in out.stdout.splitlines() if l.strip()]
    except Exception:
        return []


def run_check(root: Path, check: dict) -> dict:
    start = time.monotonic()
    result = {"key": check["key"], "name": check["name"]}
    try:
        if check.get("script"):
            cmd = [sys.executable, str(root / check["script"]), "--project-root", str(root)] + check["args"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        else:
            cmd = list(check["cmd"]) + check["args"]
            cmd[0] = cmd[0]  # keep as-is; paths resolved below
            resolved = [str(root / c) if c.startswith(("scripts/", "tools/", "skills/")) else c for c in cmd]
            proc = subprocess.run(resolved, capture_output=True, text=True, timeout=120)
        result["exitCode"] = proc.returncode
        tail = (proc.stdout + proc.stderr).strip().splitlines()
        result["outputTail"] = tail[-12:]
    except Exception as exc:  # pragma: no cover - defensive
        result["exitCode"] = -1
        result["outputTail"] = [str(exc)]
    result["status"] = "pass" if result["exitCode"] == 0 else "fail"
    result["durationMs"] = int((time.monotonic() - start) * 1000)
    return result


def cmd_run(root: Path) -> int:
    evidence_dir = root / "evidence" / "runs"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = evidence_dir / stamp
    run_dir.mkdir(parents=True, exist_ok=True)

    checks = [run_check(root, c) for c in CHECKS]
    failed = [c for c in checks if c["status"] == "fail"]
    doc = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "projectRoot": str(root),
        "gitHead": git_head(root),
        "dirty": git_status_short(root),
        "passed": not failed,
        "failCount": len(failed),
        "checks": checks,
    }
    json_path = run_dir / "evidence.json"
    json_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")

    md = ["# Evidence Run", "",
          f"- timestamp: `{doc['timestamp']}`",
          f"- git head: `{doc['gitHead']}`",
          f"- dirty files: {len(doc['dirty'])}",
          f"- result: {'PASS' if doc['passed'] else 'FAIL'}",
          "", "## Checks", "", "| Check | Status | Exit | Duration |", "|---|---|---|---|"]
    for c in checks:
        md.append(f"| {c['name']} | {c['status']} | {c['exitCode']} | {c['durationMs']}ms |")
    md.append("")
    for c in checks:
        if c["outputTail"]:
            md.append(f"### {c['name']}")
            md.append("```text")
            md.extend(c["outputTail"])
            md.append("```")
    (run_dir / "summary.md").write_text("\n".join(md), encoding="utf-8")

    print(json.dumps({"timestamp": doc["timestamp"], "passed": doc["passed"],
                      "failCount": doc["failCount"], "evidenceJson": str(json_path.relative_to(root)),
                      "summaryMd": str((run_dir / "summary.md").relative_to(root))},
                     ensure_ascii=False, indent=2))
    return 0 if doc["passed"] else 1


def cmd_task(root: Path, name: str) -> int:
    task_dir = root / "evidence" / "tasks" / name
    task_dir.mkdir(parents=True, exist_ok=True)
    template = {
        "task": name,
        "project_type": "",
        "tool_used": "",
        "mode": "lite|full|full+adapters",
        "before": {"first_pass_completion": "", "rework_count": "", "major_defects": "",
                   "verification_result": "", "token_direction": ""},
        "after": {"first_pass_completion": "", "rework_count": "", "major_defects": "",
                  "verification_result": "", "token_direction": ""},
        "conclusion": {"improved": "", "unchanged": "", "worse": "", "evidence_path": ""},
    }
    out = task_dir / "task-evidence.json"
    out.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"task": name, "template": str(out.relative_to(root))}, ensure_ascii=False))
    return 0


def cmd_compare(root: Path) -> int:
    runs = sorted((root / "evidence" / "runs").glob("*")) if (root / "evidence" / "runs").exists() else []
    if len(runs) < 2:
        print(json.dumps({"error": "need at least 2 runs to compare", "runs": [r.name for r in runs]}))
        return 1
    prev = json.loads((runs[-2] / "evidence.json").read_text(encoding="utf-8"))
    cur = json.loads((runs[-1] / "evidence.json").read_text(encoding="utf-8"))
    diff = []
    for c in cur["checks"]:
        old = next((p for p in prev["checks"] if p["key"] == c["key"]), None)
        if old and old["status"] != c["status"]:
            diff.append({"check": c["key"], "before": old["status"], "after": c["status"]})
    print(json.dumps({"before": runs[-2].name, "after": runs[-1].name,
                      "dirty": cur["dirty"], "changed": diff}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect structured delivery evidence.")
    parser.add_argument("--project-root", default=".", help="Repository root.")
    parser.add_argument("--run", action="store_true", help="Run the verification suite and save evidence.")
    parser.add_argument("--task", metavar="NAME", help="Create a task-level evidence template.")
    parser.add_argument("--compare", action="store_true", help="Compare the two latest evidence runs.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if args.run:
        return cmd_run(root)
    if args.task:
        return cmd_task(root, args.task)
    if args.compare:
        return cmd_compare(root)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
