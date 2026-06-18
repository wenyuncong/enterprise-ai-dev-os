#!/usr/bin/env python3
"""Score whether a project can support controlled AI development."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CHECKS = [
    {
        "key": "rules_entry",
        "name": "规则入口",
        "weight": 10,
        "paths": ["AGENTS.md", "rules/AGENTS.md"],
        "hint": "Add AGENTS.md and rules/AGENTS.md as session entrypoints.",
    },
    {
        "key": "project_memory",
        "name": "项目记忆",
        "weight": 15,
        "paths": ["docs/全项目总控/TASK_BACKLOG.md", "docs/全项目总控/MASTER_INDEX.md", "docs/_templates/每日调研回写/DAILY_WRITEBACK_TEMPLATE.md"],
        "hint": "Add backlog, master index, and daily writeback template.",
    },
    {
        "key": "capability_units",
        "name": "能力单元",
        "weight": 15,
        "paths": ["skills/SKILL_MANIFEST.json", "skills/core", "skills/governance"],
        "hint": "Create a manifest and verified capability units.",
    },
    {
        "key": "task_orchestration",
        "name": "任务编排",
        "weight": 10,
        "paths": ["skills/core/ai-rule-dispatcher/SKILL.md", "skills/core/ai-task-decomposer/SKILL.md"],
        "hint": "Add routing and decomposition capabilities.",
    },
    {
        "key": "tool_adapters",
        "name": "工具适配",
        "weight": 10,
        "paths": ["tools/deploy.ps1", "tools/adapters.json", "scripts/py/discover_tools.py"],
        "hint": "Add multi-tool deployment and tool discovery scripts.",
    },
    {
        "key": "verification_gates",
        "name": "验证门禁",
        "weight": 15,
        "paths": ["scripts/py/audit_methodology.py", "scripts/py/check_open_source_boundary.py", "skills/governance/ai-runtime-verify/SKILL.md"],
        "hint": "Add audit scripts, boundary checks, and runtime verification skill.",
    },
    {
        "key": "risk_governance",
        "name": "风险治理",
        "weight": 10,
        "paths": ["skills/governance/ai-single-truth-enforcer/SKILL.md", "skills/core/ai-foundation-governor/SKILL.md"],
        "hint": "Add source-of-truth and stable-foundation governance.",
    },
    {
        "key": "evolution_loop",
        "name": "进化闭环",
        "weight": 10,
        "paths": ["skills/core/ai-skill-evolver/SKILL.md", "docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md"],
        "hint": "Add a skill evolution mechanism and delivery-loop documentation.",
    },
    {
        "key": "token_economy",
        "name": "Token 经济",
        "weight": 5,
        "paths": ["docs/公开材料/OPEN_SOURCE_PACKAGE.md"],
        "hint": "Add token-saving or rework-reduction metrics.",
    },
]


def exists(root: Path, item: str) -> bool:
    return (root / item).exists()


def level(score: int) -> str:
    if score < 40:
        return "L0 随机生成"
    if score < 60:
        return "L1 有规则"
    if score < 75:
        return "L2 可协作"
    if score < 90:
        return "L3 可交付"
    return "L4 可进化"


def main() -> int:
    parser = argparse.ArgumentParser(description="Score AI development readiness.")
    parser.add_argument("--project-root", default=".", help="Project root to score.")
    parser.add_argument("--json", action="store_true", help="Print JSON.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    rows = []
    total = 0

    for check in CHECKS:
        found = [p for p in check["paths"] if exists(root, p)]
        ratio = len(found) / len(check["paths"])
        score = round(check["weight"] * ratio)
        total += score
        rows.append(
            {
                "key": check["key"],
                "name": check["name"],
                "weight": check["weight"],
                "score": score,
                "found": found,
                "missing": [p for p in check["paths"] if p not in found],
                "hint": check["hint"],
            }
        )

    result = {"projectRoot": str(root), "score": total, "level": level(total), "dimensions": rows}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"AI development readiness: {total}/100 ({level(total)})")
        for row in rows:
            status = "OK" if row["score"] == row["weight"] else "GAP"
            print(f"[{status}] {row['name']}: {row['score']}/{row['weight']}")
            if row["missing"]:
                print(f"  missing: {', '.join(row['missing'])}")
                print(f"  hint: {row['hint']}")

    return 0 if total >= 75 else 1


if __name__ == "__main__":
    raise SystemExit(main())
