#!/usr/bin/env python3
"""Event trace: record an append-only action-observation stream for delivery.

Turns the 5S delivery lifecycle into a checkpointable, replayable event log
(OpenHands EventStream / LangGraph checkpoint style). Every action is appended
with its observation and status, so a delivery can be resumed from any point
and replayed for audit. Append-only: entries are never rewritten.

Commands:
  event_trace.py init --trace <path.jsonl> --delivery <id>
  event_trace.py append --trace <path.jsonl> --phase S --action A --observation O [--status ok|fail|blocked]
  event_trace.py list --trace <path.jsonl> [--json]
  event_trace.py replay --trace <path.jsonl>
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PHASES = ["Scope", "Specify", "Ship", "Safeguard", "Sell"]


def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def cmd_init(path: Path, delivery: str) -> int:
    if path.exists() and path.stat().st_size > 0:
        print(json.dumps({"error": f"{path} already has events"}, ensure_ascii=False))
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    header = {"type": "delivery", "id": delivery,
              "startedAt": datetime.now(timezone.utc).isoformat(),
              "schemaVersion": "1.0.0"}
    path.write_text(json.dumps(header, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "trace": str(path)}))
    return 0


def cmd_append(path: Path, phase: str, action: str, observation: str, status: str) -> int:
    if phase not in PHASES:
        print(json.dumps({"error": f"phase must be one of {PHASES}"}, ensure_ascii=False))
        return 1
    if not path.exists():
        print(json.dumps({"error": "trace not initialized; run init first"}, ensure_ascii=False))
        return 1
    event = {"ts": datetime.now(timezone.utc).isoformat(), "phase": phase,
             "action": action, "observation": observation, "status": status}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(json.dumps({"ok": True, "event": event}, ensure_ascii=False))
    return 0


def cmd_list(path: Path, as_json: bool) -> int:
    events = read_events(path)
    body = [e for e in events if e.get("type") != "delivery"]
    counts = {p: sum(1 for e in body if e["phase"] == p) for p in PHASES}
    if as_json:
        print(json.dumps({"total": len(body), "byPhase": counts, "events": body},
                         ensure_ascii=False, indent=2))
    else:
        print(f"Events: {len(body)}")
        for p in PHASES:
            print(f"  {p}: {counts[p]}")
    return 0


def cmd_replay(path: Path) -> int:
    events = read_events(path)
    body = [e for e in events if e.get("type") != "delivery"]
    for i, e in enumerate(body, 1):
        mark = {"ok": "[OK]", "fail": "[FAIL]", "blocked": "[BLOCKED]"}.get(e.get("status"), "[?]")
        print(f"{i:>3} [{e['phase']}] {mark} {e['action']}")
        if e.get("observation"):
            print(f"      ↳ {e['observation'][:140]}")
    print(f"--- {len(body)} event(s) replayed ---")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Append-only delivery event trace.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--trace", required=True)
    i.add_argument("--delivery", required=True)
    a = sub.add_parser("append")
    a.add_argument("--trace", required=True)
    a.add_argument("--phase", required=True, choices=PHASES)
    a.add_argument("--action", required=True)
    a.add_argument("--observation", default="")
    a.add_argument("--status", default="ok", choices=["ok", "fail", "blocked"])
    l = sub.add_parser("list")
    l.add_argument("--trace", required=True)
    l.add_argument("--json", action="store_true")
    r = sub.add_parser("replay")
    r.add_argument("--trace", required=True)
    args = parser.parse_args()

    path = Path(args.trace).resolve()
    if args.cmd == "init":
        return cmd_init(path, args.delivery)
    if args.cmd == "append":
        return cmd_append(path, args.phase, args.action, args.observation, args.status)
    if args.cmd == "list":
        return cmd_list(path, args.json)
    return cmd_replay(path)


if __name__ == "__main__":
    sys.exit(main())
