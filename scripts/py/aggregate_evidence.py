#!/usr/bin/env python3
"""Aggregate L0-L3 delivery gates into one fail-closed verdict.

Maps the methodology's verification suite to delivery-gate levels and returns
a single fail-closed result: any failed gate blocks "done", regardless of how
many other gates pass. Reads the latest evidence run produced by
collect_evidence.py and re-runs gates live when --live is given.

Usage:
  aggregate_evidence.py --project-root . [--live] [--json]
Exit code: 1 if any gate fails.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

# L0-L3 gate mapping: (level, gate, check key, live command)
GATES = [
    {"level": "L0", "gate": "方法论结构审计", "key": "audit_methodology",
     "cmd": ["scripts/py/audit_methodology.py", "--project-root", "{root}"]},
    {"level": "L1", "gate": "规则 Lint", "key": "rule_lint",
     "cmd": ["scripts/py/rule_lint.py", "--project-root", "{root}"]},
    {"level": "L1", "gate": "开源边界", "key": "open_source_boundary",
     "cmd": ["scripts/py/check_open_source_boundary.py", "--project-root", "{root}"]},
    {"level": "L2", "gate": "方法论场景回归", "key": "methodology_scenarios",
     "cmd": ["scripts/py/test_methodology_scenarios.py", "--project-root", "{root}"]},
    {"level": "L2", "gate": "技能健康", "key": "skill_health",
     "cmd": ["scripts/py/audit_skill_health.py", "--project-root", "{root}"]},
    {"level": "L3", "gate": "就绪评分", "key": "readiness_score",
     "cmd": ["scripts/py/score_ai_development_readiness.py", "--project-root", "{root}"]},
]


def latest_evidence(root: Path) -> dict:
    runs = sorted((root / "evidence" / "runs").glob("*")) if (root / "evidence" / "runs").exists() else []
    if not runs:
        return {}
    return json.loads((runs[-1] / "evidence.json").read_text(encoding="utf-8"))


def live_check(root: Path, gate: dict) -> dict:
    cmd = [sys.executable] + [c.replace("{root}", str(root)) for c in gate["cmd"]]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return {"status": "pass" if proc.returncode == 0 else "fail", "exit": proc.returncode}


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate L0-L3 gates into one verdict.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--live", action="store_true", help="Re-run gates instead of reading cached evidence.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    cached = latest_evidence(root)
    results = []
    for gate in GATES:
        if args.live:
            r = live_check(root, gate)
        else:
            check = next((c for c in cached.get("checks", []) if c["key"] == gate["key"]), None)
            r = {"status": check["status"] if check else "missing",
                 "exit": check.get("exitCode", -1) if check else -1}
        results.append({**gate, **r})

    failed = [r for r in results if r["status"] != "pass"]
    out = {"mode": "live" if args.live else "cached",
           "passed": not failed,
           "failClosed": not failed,
           "failedGates": [f"{r['level']} {r['gate']}" for r in failed],
           "byLevel": {lv: [r for r in results if r["level"] == lv] for lv in ["L0", "L1", "L2", "L3"]},
           "gates": results}

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Gate aggregation ({out['mode']}): {'PASS' if out['passed'] else 'FAIL'} — fail-closed")
        for r in results:
            print(f"  [{r['level']}] {r['gate']}: {r['status']}")
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
