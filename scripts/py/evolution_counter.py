#!/usr/bin/env python3
"""Evolution counter: turn "same error 3 times" into a measurable trigger.

This is the Reflexion-style fingerprint counter behind the methodology's
evolution loop. Record an error fingerprint when a task closes; when a
pattern reaches the threshold, report it as a candidate for ai-skill-evolver.

Commands:
  evolution_counter.py record --pattern "..." --context "..."
  evolution_counter.py report [--threshold N] [--json]

The ledger lives at docs/全项目总控/pattern_ledger.json. This script only
suggests upgrades; it never edits rules/skills automatically (that stays an
explicit, reviewed step).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LEDGER = "docs/全项目总控/pattern_ledger.json"
DEFAULT_THRESHOLD = 3


def load(root: Path) -> dict:
    path = root / LEDGER
    if not path.exists():
        return {"schemaVersion": "1.0.0", "threshold": DEFAULT_THRESHOLD, "patterns": {}}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(root: Path, ledger: dict) -> None:
    path = root / LEDGER
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_record(root: Path, pattern: str, context: str) -> int:
    ledger = load(root)
    now = datetime.now(timezone.utc).isoformat()
    entry = ledger["patterns"].get(pattern)
    if entry:
        entry["count"] = int(entry.get("count", 0)) + 1
        entry["lastSeen"] = now
        if context:
            entry["lastContext"] = context
    else:
        ledger["patterns"][pattern] = {
            "count": 1, "firstSeen": now, "lastSeen": now, "lastContext": context,
        }
    save(root, ledger)
    print(json.dumps({"pattern": pattern, "count": ledger["patterns"][pattern]["count"]},
                     ensure_ascii=False))
    return 0


def cmd_report(root: Path, threshold: int, as_json: bool) -> int:
    ledger = load(root)
    if threshold is None:
        threshold = int(ledger.get("threshold", DEFAULT_THRESHOLD))
    hits = []
    for pattern, entry in sorted(ledger.get("patterns", {}).items(),
                                 key=lambda kv: -int(kv[1].get("count", 0))):
        count = int(entry.get("count", 0))
        if count >= threshold:
            hits.append({"pattern": pattern, "count": count,
                         "lastContext": entry.get("lastContext", "")})
    out = {"threshold": threshold, "candidates": hits,
           "suggestion": [f"Upgrade pattern '{h['pattern']}' (x{h['count']}) via ai-skill-evolver"
                          for h in hits]}
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Evolution candidates (count >= {threshold}): {len(hits)}")
        for h in hits:
            print(f"  [{h['count']}x] {h['pattern']}  -- {h['lastContext'][:120]}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Record and report error-pattern fingerprints.")
    parser.add_argument("--project-root", default=".")
    sub = parser.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record", help="Record one occurrence of a pattern.")
    r.add_argument("--pattern", required=True)
    r.add_argument("--context", default="")
    p = sub.add_parser("report", help="Report patterns at or above the threshold.")
    p.add_argument("--threshold", type=int, default=None)
    p.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if args.cmd == "record":
        return cmd_record(root, args.pattern, args.context)
    return cmd_report(root, args.threshold, args.json)


if __name__ == "__main__":
    sys.exit(main())
