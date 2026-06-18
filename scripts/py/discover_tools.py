#!/usr/bin/env python3
"""
discover_tools.py — Project Tool & Script Discovery Engine

Scans an existing project for all scripts, tools, and automation.
Discovers what the project ALREADY has before writing anything new.

Usage:
    py scripts/py/discover_tools.py .                    # Scan current project
    py scripts/py/discover_tools.py ../your-project      # Scan specific project
    py scripts/py/discover_tools.py . --json             # JSON output
    py scripts/py/discover_tools.py . --by-purpose       # Group by inferred purpose
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Patterns that suggest a script's purpose
PURPOSE_PATTERNS = {
    "database/migration":  [r"migrat", r"schema", r"init_", r"V\d+__", r"alter_", r"create_"],
    "database/seed":       [r"seed", r"test_data", r"sample", r"fixture"],
    "database/check":      [r"check_", r"verify_", r"describe_", r"query_"],
    "database/sync":       [r"sync_", r"patch_", r"migration_"],
    "build/compile":       [r"build", r"compile", r"mvn", r"npm run"],
    "service/start":       [r"start", r"启动", r"launch", r"run"],
    "service/stop":        [r"stop", r"关闭", r"kill", r"shutdown"],
    "deploy/release":      [r"deploy", r"release", r"publish"],
    "test/api":            [r"test_api", r"api_test", r"test_endpoint"],
    "test/unit":           [r"test_", r"_test", r"spec"],
    "data/export":         [r"export", r"extract", r"dump"],
    "data/import":         [r"import", r"load", r"restore"],
    "health/monitor":      [r"health", r"monitor", r"check_port", r"status"],
    "utility/cleanup":     [r"clean", r"fix", r"format", r"optimize"],
    "utility/generate":    [r"generat", r"init_"],
}

def infer_purpose(filename):
    """Infer script purpose from filename patterns."""
    name_lower = filename.lower()
    for purpose, patterns in PURPOSE_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in name_lower:
                return purpose
    return "other"

def scan_directory(root_path, base_path=""):
    """Recursively scan for scripts and tools."""
    scripts = []
    script_extensions = {'.bat', '.ps1', '.sh', '.py', '.js', '.cjs', '.mjs', '.sql'}
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip node_modules, .git, venv, etc.
        dirnames[:] = [d for d in dirnames if d not in {'node_modules', '.git', '__pycache__', '.venv', 'venv', 'target', 'dist', 'build', 'output'}]
        
        rel_dir = os.path.relpath(dirpath, root_path)
        if rel_dir == '.':
            rel_dir = ''
        
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in script_extensions:
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.join(rel_dir, f) if rel_dir else f
                size = os.path.getsize(full_path)
                
                scripts.append({
                    "name": f,
                    "path": rel_path,
                    "extension": ext,
                    "size": size,
                    "purpose": infer_purpose(f),
                    "directory": rel_dir or "(root)"
                })
    
    return scripts

def summarize(scripts):
    """Generate summary statistics."""
    by_purpose = defaultdict(list)
    by_ext = defaultdict(int)
    by_dir = defaultdict(int)
    
    for s in scripts:
        by_purpose[s["purpose"]].append(s)
        by_ext[s["extension"]] += 1
        by_dir[s["directory"]] += 1
    
    return {
        "total": len(scripts),
        "by_purpose": {k: len(v) for k, v in sorted(by_purpose.items())},
        "by_extension": dict(sorted(by_ext.items())),
        "by_directory": dict(sorted(by_dir.items(), key=lambda x: -x[1])[:20])
    }

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    json_out = "--json" in sys.argv
    by_purpose = "--by-purpose" in sys.argv
    
    root = Path(target).resolve()
    if not root.exists():
        print(f"Error: {target} not found")
        sys.exit(1)
    
    scripts = scan_directory(str(root))
    summary = summarize(scripts)
    
    if json_out:
        output = {
            "project": str(root),
            "scanned_at": datetime.now().isoformat(),
            "summary": summary,
            "scripts": scripts if not by_purpose else None,
            "by_purpose": {p: [s["path"] for s in slist] for p, slist in 
                          defaultdict(list, {s["purpose"]: [] for s in scripts}).items()}
        }
        if by_purpose:
            output["by_purpose"] = {}
            for s in scripts:
                if s["purpose"] not in output["by_purpose"]:
                    output["by_purpose"][s["purpose"]] = []
                output["by_purpose"][s["purpose"]].append(s["path"])
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return
    
    print(f"Project: {root}")
    print(f"Scripts found: {summary['total']}")
    print()
    
    if by_purpose:
        print("=== By Purpose ===")
        purposed = defaultdict(list)
        for s in scripts:
            purposed[s["purpose"]].append(s["path"])
        for purpose, paths in sorted(purposed.items()):
            print(f"\n  [{purpose}] ({len(paths)} scripts)")
            for p in paths[:5]:
                print(f"    {p}")
            if len(paths) > 5:
                print(f"    ... and {len(paths)-5} more")
        return
    
    print("=== By Purpose ===")
    for purpose, count in sorted(summary["by_purpose"].items()):
        bar = "█" * max(1, count // max(1, summary["total"] // 40))
        print(f"  {purpose:<25} {count:>4} {bar}")
    
    print(f"\n=== By Extension ===")
    for ext, count in sorted(summary["by_extension"].items(), key=lambda x: -x[1]):
        print(f"  {ext:<10} {count:>4}")
    
    print(f"\n=== Top Directories ===")
    for directory, count in sorted(summary["by_directory"].items(), key=lambda x: -x[1])[:10]:
        print(f"  {directory:<40} {count:>4}")

if __name__ == "__main__":
    main()
