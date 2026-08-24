#!/usr/bin/env python3
"""Build a symbol map (repomap) for fast AI code location.

Aider-style repomap, simplified: scan source files and extract top-level
symbols (classes, functions, components, tables) into a JSON index + a
readable summary. An AI can read the map to locate code instead of scanning
the whole tree.

Usage:
  build_repomap.py --project-root . [--roots src app] [--json] [--out <path>]
Exit code: 0 always (map generation is informational).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXTS = {".py", ".js", ".mjs", ".ts", ".jsx", ".tsx", ".java", ".vue", ".sql"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "target", "__pycache__",
             ".venv", "venv", "temp", "tmp", "evidence", "reference", "备用"}

PATTERNS = [
    ("py", re.compile(r"^(?:async\s+)?(?:def|class)\s+([A-Za-z_]\w*)")),
    ("js", re.compile(r"^(?:export\s+(?:default\s+)?)?(?:class|function|const|let|var|async\s+function)\s+([A-Za-z_$\w]*)")),
    ("java", re.compile(r"^\s*(?:public|private|protected)?\s*(?:abstract\s+|static\s+|final\s+)*(?:class|interface|enum)\s+([A-Za-z_]\w*)")),
    ("sql", re.compile(r"^CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+([`\"\w.]+)")),
]


def collect(root: Path, roots: list[str]) -> list[Path]:
    files = []
    for r in roots:
        base = root / r
        if not base.exists():
            continue
        if base.is_file():
            files.append(base)
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in EXTS and not any(
                    part in SKIP_DIRS for part in p.relative_to(base).parts):
                files.append(p)
    return files


def symbols_for(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return []
    out = []
    suffix = path.suffix.lower()
    if suffix == ".vue":
        m = re.search(r"<script[^>]*>([\s\S]*?)</script>", text)
        if m:
            for line in m.group(1).splitlines():
                mm = re.match(r"\s*(?:export\s+default\s+)?(?:const|function)\s+([A-Za-z_]\w*)", line)
                if mm:
                    out.append(mm.group(1))
        return out[:20]
    for ext, pat in PATTERNS:
        if suffix == f".{ext}":
            for line in text.splitlines():
                m = pat.match(line)
                if m and m.group(1):
                    out.append(m.group(1))
            break
    return out[:40]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a symbol map for fast code location.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--roots", nargs="*", default=["src", "app", "backend", "frontend", "scripts", "."],
                        help="Directories to scan (relative to project root).")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", default=None, help="Write JSON map to this path.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    files = collect(root, args.roots)
    index = {}
    total_symbols = 0
    for f in files:
        syms = symbols_for(f)
        if syms:
            rel = str(f.relative_to(root)).replace("\\", "/")
            index[rel] = syms
            total_symbols += len(syms)

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"ok": True, "files": len(index), "symbols": total_symbols,
                          "out": str(out_path)}))
        return 0

    if args.json:
        print(json.dumps({"files": len(index), "symbols": total_symbols, "index": index},
                         ensure_ascii=False, indent=2))
    else:
        print(f"Repomap: {len(index)} files, {total_symbols} symbols")
        for rel, syms in sorted(index.items())[:15]:
            print(f"  {rel}: {', '.join(syms[:6])}{'...' if len(syms) > 6 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
