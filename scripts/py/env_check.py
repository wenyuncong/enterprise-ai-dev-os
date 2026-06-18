#!/usr/bin/env python3
"""
env_check.py — Proactive Environment Verification

Detects all development tools, updates the tool registry, and reports gaps.
Run at session start. Run before any task. Run when things "don't work."

Usage:
    python scripts/py/env_check.py              # Check + update registry
    python scripts/py/env_check.py --json       # JSON output
    python scripts/py/env_check.py --quick      # Fast check only (skip version queries)
"""

import json
import os
import subprocess
import sys; import io; sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import sys
from pathlib import Path
from datetime import datetime

REGISTRY_PATH = Path(__file__).parent.parent.parent / "tools" / "tool-registry.json"

TOOLS = {
    "node":       {"cmd": "node",       "args": ["--version"], "win_paths": [r"C:\Program Files\nodejs\node.exe"]},
    "npm":        {"cmd": "npm",        "args": ["--version"], "win_paths": [r"C:\Program Files\nodejs\npm.cmd"]},
    "python":     {"cmd": "python",     "args": ["--version"], "win_paths": [r"C:\Python3*\python.exe"]},
    "git":        {"cmd": "git",        "args": ["--version"], "win_paths": [r"C:\Program Files\Git\bin\git.exe"]},
    "java":       {"cmd": "java",       "args": ["--version"], "win_paths": [r"C:\Program Files\Eclipse Adoptium\*\bin\java.exe"]},
    "mysql":      {"cmd": "mysql",      "args": ["--version"], "win_paths": [r"C:\Program Files\MySQL\*\bin\mysql.exe"]},
    "docker":     {"cmd": "docker",     "args": ["--version"], "win_paths": [r"C:\Program Files\Docker\Docker\resources\bin\docker.exe", r"C:\Program Files\Docker\Docker\Docker Desktop.exe"]},
    "curl":       {"cmd": "curl",       "args": ["--version"], "win_paths": [r"C:\Windows\System32\curl.exe"]},
    "playwright": {"cmd": "npx.cmd",    "args": ["playwright", "--version"], "win_paths": []},
    "edge":       {"cmd": None,         "args": [],             "win_paths": [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                                                                               r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]},
}

def run_cmd(cmd, args, timeout=10):
    """Run a command and return (success, output, error)."""
    try:
        result = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=timeout)
        output = (result.stdout + result.stderr).strip()
        return True, output, ""
    except FileNotFoundError:
        return False, "", f"{cmd} not found on PATH"
    except subprocess.TimeoutExpired:
        return False, "", f"{cmd} timed out"
    except Exception as e:
        return False, "", str(e)

def find_tool_path(tool_name, known_paths):
    """Find tool executable by checking known paths or PATH."""
    # Check known paths first
    import glob
    for pattern in known_paths:
        for found in glob.glob(pattern):
            if os.path.exists(found):
                return found
    
    # Check PATH
    cmd = TOOLS[tool_name]["cmd"]
    if cmd:
        result = subprocess.run(["where", cmd], capture_output=True, text=True)
        if result.returncode == 0:
            paths = result.stdout.strip().split("\n")
            if paths:
                return paths[0].strip()
    return ""

def check_tools():
    """Check all tools and return results."""
    results = {}
    for name, config in TOOLS.items():
        success, version, error = False, "", ""
        exe_path = ""
        
        if config["cmd"]:
            success, version, error = run_cmd(config["cmd"], config["args"])
        
        if not success and config["win_paths"]:
            exe_path = find_tool_path(name, config["win_paths"])
            if exe_path:
                # Try running with full path
                success, version, error = run_cmd(exe_path, config["args"])
        
        if not exe_path:
            exe_path = find_tool_path(name, config["win_paths"])
        
        results[name] = {
            "available": success,
            "version": version[:50] if version else "",
            "path": exe_path,
            "error": error[:100] if error else ""
        }
    return results

def load_registry():
    """Load existing registry."""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"tools": {}, "_schema": "1.0"}

def save_registry(registry):
    """Save updated registry."""
    registry["last_updated"] = datetime.now().isoformat()
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

def update_registry(results, registry):
    """Update registry with check results."""
    today = datetime.now().strftime("%Y-%m-%d")
    for name, result in results.items():
        if name not in registry["tools"]:
            registry["tools"][name] = {}
        tool = registry["tools"][name]
        if result["available"]:
            tool["version"] = result["version"]
            tool["path"] = result["path"] or tool.get("path", "")
            tool["verified"] = today
        else:
            if "verified" not in tool or not tool.get("verified"):
                tool["path"] = ""
                tool["version"] = ""
                tool["verified"] = ""

def main():
    quick = "--quick" in sys.argv
    json_out = "--json" in sys.argv
    
    if not json_out:
        print("=" * 60)
        print("  ENVIRONMENT CHECK")
        print("=" * 60)
    
    results = check_tools()
    registry = load_registry()
    update_registry(results, registry)
    save_registry(registry)
    
    if json_out:
        print(json.dumps(results, indent=2))
        return
    
    available = 0
    missing = 0
    for name, result in results.items():
        status = "[OK]" if result["available"] else "[MISSING] MISSING"
        version_info = f"({result['version']})" if result["version"] else ""
        print(f"  {status} {name:<15} {version_info}")
        if result["available"]:
            available += 1
        else:
            missing += 1
    
    print("-" * 60)
    print(f"  Available: {available}  |  Missing: {missing}")
    print(f"  Registry: {REGISTRY_PATH}")
    print("=" * 60)
    
    if missing > 0:
        print("\n[WARN]  Run the bootstrapper to install missing tools:")
        print("   ai-tool-bootstrapper will auto-install missing tools")
        sys.exit(1)
    else:
        print("\n[OK] All tools available. Ready to work.")
        sys.exit(0)

if __name__ == "__main__":
    main()
