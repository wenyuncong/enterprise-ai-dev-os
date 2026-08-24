#!/usr/bin/env python3
"""Check the project constitution (docs/全项目总控/CONSTITUTION.md).

Each MUST principle maps to a machine check: structural assertions that the
canonical rules declare the principle, plus reuse of rule_lint's violation
scanner for the executable principles. Fail-closed: any violated MUST fails.

Usage:
  check_constitution.py --project-root . [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Import the rule scanner from rule_lint (same package dir).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule_lint  # noqa: E402

MUSTS = [
    {"id": "MUST-1", "name": "前端纯展示",
     "ruleTerms": ["frontend = display only", "前端纯展示"]},
    {"id": "MUST-2", "name": "单一真相源",
     "ruleTerms": ["single source of truth", "单一真相源", "sole source of truth"]},
    {"id": "MUST-3", "name": "库优先",
     "ruleTerms": ["library first", "库优先"]},
    {"id": "MUST-4", "name": "无静默失败",
     "ruleTerms": ["no silent failures", "无静默失败"]},
    {"id": "MUST-5", "name": "完成前验证",
     "ruleTerms": ["runtime verify", "完成前验证", "no test = not done"]},
    {"id": "MUST-6", "name": "破坏性操作确认",
     "ruleTerms": ["destructive actions = modal confirmation", "破坏性操作"]},
    {"id": "MUST-7", "name": "目录边界",
     "ruleTerms": ["never create files in the project root", "禁止在项目根"]},
    {"id": "MUST-8", "name": "禁止硬编码",
     "ruleTerms": ["theme variables only", "no hard-coded", "硬编码"]},
]


def rules_text(root: Path) -> str:
    p = root / "rules" / "AGENTS.md"
    return p.read_text(encoding="utf-8-sig").lower() if p.exists() else ""


def check_rules_declare(text: str, terms: list[str]) -> bool:
    return any(t.lower() in text for t in terms)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the project constitution.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    text = rules_text(root)
    constitution_exists = (root / "docs" / "全项目总控" / "CONSTITUTION.md").exists()
    aci_exists = (root / "tools" / "aci_commands.json").exists()

    # Run rule_lint to feed the executable principles.
    lint = rule_lint.build_rules()
    lint_hits = {r["key"]: [h.to_dict() for h in r["check"](root)] for r in lint}

    results = []
    for m in MUSTS:
        declared = check_rules_declare(text, m["ruleTerms"])
        if m["id"] == "MUST-4":
            executable = len(lint_hits.get("empty_catches", [])) == 0
        elif m["id"] == "MUST-7":
            executable = len(lint_hits.get("root_clutter", [])) == 0
        elif m["id"] == "MUST-8":
            executable = (len(lint_hits.get("drive_paths", [])) == 0
                          and len(lint_hits.get("hardcoded_colors", [])) == 0)
        elif m["id"] == "MUST-6":
            executable = aci_exists
        else:
            executable = True  # structural declaration is the check for MUST-1/2/3/5
        passed = declared and executable
        results.append({"id": m["id"], "name": m["name"], "declared": declared,
                        "executable": executable, "passed": passed})

    failed = [r for r in results if not r["passed"]]
    out = {"projectRoot": str(root), "constitution": constitution_exists,
           "aci": aci_exists, "passed": not failed,
           "failed": [r["id"] for r in failed], "musts": results}

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Constitution: {'PASS' if out['passed'] else 'FAIL'} ({len(failed)} violated)")
        for r in results:
            print(f"  {r['id']} {r['name']}: {'PASS' if r['passed'] else 'FAIL'}")
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
