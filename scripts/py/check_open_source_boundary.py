#!/usr/bin/env python3
"""Check that internal materials are not staged for open-source publishing."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


BLOCKED_PREFIXES = (
    "docs/内部商业化/",
    "docs/商业化/",
    "reference/",
    "备用/",
    "verification-demo/",
    ".agents/",
    ".claude/",
    ".codebuddy/",
    ".qoder/",
    ".trae/",
    "temp/",
    "tmp/",
)

BLOCKED_FILES = {
    "tools/tool-registry.json",
}


def git(args: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check open-source boundary before commit/push.")
    parser.add_argument("--project-root", default=".", help="Repository root.")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()

    inside = git(["rev-parse", "--is-inside-work-tree"], root)
    if inside.returncode != 0:
        print("Not a git repository yet. Run after git init.", file=sys.stderr)
        return 2

    listed = git(["ls-files", "--cached", "--others", "--exclude-standard"], root)
    if listed.returncode != 0:
        print(listed.stderr, file=sys.stderr)
        return listed.returncode

    files = [line.strip().replace("\\", "/") for line in listed.stdout.splitlines() if line.strip()]
    blocked = []
    for item in files:
        if item in BLOCKED_FILES or any(item.startswith(prefix) for prefix in BLOCKED_PREFIXES):
            blocked.append(item)

    if blocked:
        print("Open-source boundary check: FAIL")
        for item in blocked:
            print(f"blocked: {item}")
        return 1

    print("Open-source boundary check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
