#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconcile practice-project activity against methodology freshness.

This is the executable driver behind the Repair-To-Skill loop. The skill
documents describe *that* practice should flow back into the methodology;
this script makes the gap measurable and schedulable instead of relying on
someone remembering to check.

It answers one question: has the practice project produced substantial new
delivery evidence while the methodology stayed untouched long enough that a
writeback is overdue?

Commands:
  check          Measure practice commits since the last resolved point and
                 compare against methodology freshness; exit 1 when a
                 writeback is overdue, otherwise 0.
  mark-resolved  Record the current practice HEAD as the new baseline after a
                 writeback has actually been completed.

The practice project path is always supplied explicitly; nothing project
specific is hard-coded. Local state (real paths, commit hashes) is kept under
evidence/ which is git-ignored, so it never enters the portable release.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_REL = Path("evidence/writeback_reconcile/state.json")
DEFAULT_STALE_DAYS = 14
DEFAULT_COMMIT_THRESHOLD = 10


def run_git(repo: Path, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo)] + args,
                          capture_output=True, text=True, timeout=60)


def git_head(repo: Path) -> str:
    return run_git(repo, ["rev-parse", "HEAD"]).stdout.strip()


def git_head_time(repo: Path) -> datetime | None:
    out = run_git(repo, ["log", "-1", "--format=%cI"]).stdout.strip()
    return parse_time(out) if out else None


def parse_time(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    except ValueError:
        return None


def load_state(root: Path) -> dict:
    path = root / STATE_REL
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(root: Path, state: dict) -> None:
    path = root / STATE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def commits_since(repo: Path, baseline: str) -> tuple[int, list[str]]:
    """Count commits strictly after baseline (baseline excluded)."""
    rng = f"{baseline}..HEAD" if baseline else "HEAD"
    proc = run_git(repo, ["log", rng, "--format=%h %cI %s"])
    if proc.returncode != 0:
        # baseline may be unreachable from this repo; fall back to full history
        proc = run_git(repo, ["log", "HEAD", "--format=%h %cI %s"])
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    return len(lines), lines


def methodology_last_commit(root: Path) -> datetime | None:
    proc = run_git(root, ["log", "-1", "--format=%cI", "--", "methodology", "skills"])
    return parse_time(proc.stdout.strip()) if proc.stdout.strip() else None


def has_uncommitted_methodology(root: Path) -> bool:
    proc = run_git(root, ["status", "--porcelain", "--", "methodology", "skills"])
    return bool(proc.stdout.strip())


def cmd_check(root: Path, practice: Path, stale_days: int,
              commit_threshold: int, as_json: bool) -> int:
    if not practice.exists():
        print(f"practice root not found: {practice}", file=sys.stderr)
        return 2
    state = load_state(root)
    baseline = state.get("practiceHead", "")

    head = git_head(practice)
    practice_head_time = git_head_time(practice)
    new_commits, commit_lines = commits_since(practice, baseline)
    methodology_time = methodology_last_commit(root)
    dirty = has_uncommitted_methodology(root)

    now = datetime.now(timezone.utc)
    methodology_age_days = (
        round((now - methodology_time).total_seconds() / 86400, 1)
        if methodology_time else None
    )

    active = new_commits >= commit_threshold
    stale = methodology_age_days is not None and methodology_age_days >= stale_days
    overdue = active and stale and not dirty

    report = {
        "checkedAt": now.isoformat(),
        "practiceRoot": str(practice),
        "practiceHead": head,
        "practiceHeadTime": practice_head_time.isoformat() if practice_head_time else None,
        "baselineHead": baseline or None,
        "newCommitsSinceBaseline": new_commits,
        "commitThreshold": commit_threshold,
        "methodologyLastCommit": methodology_time.isoformat() if methodology_time else None,
        "methodologyAgeDays": methodology_age_days,
        "staleDays": stale_days,
        "uncommittedMethodologyChanges": dirty,
        "status": "overdue" if overdue else "ok",
        "recommendation": (
            "Generalize new practice evidence and write it back into the methodology, "
            "then run mark-resolved."
            if overdue else "No writeback currently due."
        ),
        "recentCommits": commit_lines[:10],
    }

    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Writeback reconciliation:", report["status"].upper())
        base = baseline or "(none)"
        print(f"  practice head        : {head} (baseline {base})")
        print(f"  new commits          : {new_commits} (threshold {commit_threshold})")
        print(f"  methodology last     : {report['methodologyLastCommit']} "
              f"({methodology_age_days} days old, stale after {stale_days})")
        if dirty:
            print("  note                 : uncommitted methodology changes present")
        print(f"  recommendation       : {report['recommendation']}")
    return 1 if overdue else 0


def cmd_mark_resolved(root: Path, practice: Path) -> int:
    if not practice.exists():
        print(f"practice root not found: {practice}", file=sys.stderr)
        return 2
    head = git_head(practice)
    head_time = git_head_time(practice)
    state = load_state(root)
    state.update({
        "practiceRoot": str(practice),
        "practiceHead": head,
        "resolvedAt": datetime.now(timezone.utc).isoformat(),
        "practiceHeadTime": head_time.isoformat() if head_time else None,
    })
    save_state(root, state)
    print(json.dumps({"marked": True, "practiceHead": head}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile practice activity vs methodology freshness.")
    parser.add_argument("--project-root", default=".", help="Methodology repository root.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="Check whether a writeback is overdue.")
    c.add_argument("--practice-root", required=True, help="Path to the practice project.")
    c.add_argument("--stale-days", type=int, default=DEFAULT_STALE_DAYS)
    c.add_argument("--commit-threshold", type=int, default=DEFAULT_COMMIT_THRESHOLD)
    c.add_argument("--json", action="store_true")

    m = sub.add_parser("mark-resolved", help="Record current practice HEAD as the baseline.")
    m.add_argument("--practice-root", required=True)

    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    practice = Path(args.practice_root).resolve()

    if args.cmd == "check":
        return cmd_check(root, practice, args.stale_days,
                         args.commit_threshold, args.json)
    return cmd_mark_resolved(root, practice)


if __name__ == "__main__":
    sys.exit(main())
