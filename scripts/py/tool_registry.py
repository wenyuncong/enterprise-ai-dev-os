#!/usr/bin/env python3
"""
tool_registry.py — Tool Registry Query & Management

Usage:
    python scripts/py/tool_registry.py list              # List all registered tools
    python scripts/py/tool_registry.py get node          # Get path for specific tool
    python scripts/py/tool_registry.py set node "C:\\path" "v1.0"  # Register a tool
    python scripts/py/tool_registry.py missing            # List missing tools
    python scripts/py/tool_registry.py --json             # JSON output
"""

import json
import sys
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent.parent / "tools" / "tool-registry.json"

def load():
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"tools": {}, "_schema": "1.0"}

def save(registry):
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

def cmd_list(registry, json_out=False):
    if json_out:
        print(json.dumps(registry["tools"], indent=2))
        return
    print(f"{'Tool':<20} {'Path':<60} {'Version':<15}")
    print("-" * 95)
    for name, info in sorted(registry["tools"].items()):
        path = info.get("path", "-")[:58]
        ver = info.get("version", "-")[:13]
        print(f"{name:<20} {path:<60} {ver:<15}")

def cmd_get(registry, name, json_out=False):
    tool = registry["tools"].get(name, {})
    if json_out:
        print(json.dumps(tool, indent=2))
        return
    if not tool or not tool.get("path"):
        print(f"❌ {name} not registered or no path known")
        sys.exit(1)
    print(tool["path"])

def cmd_set(registry, name, path, version):
    today = __import__('datetime').datetime.now().strftime("%Y-%m-%d")
    registry["tools"][name] = {
        "path": path,
        "version": version,
        "installed_by": "ai-tool-bootstrapper",
        "verified": today
    }
    save(registry)
    print(f"✅ Registered: {name} → {path} (v{version})")

def cmd_missing(registry, json_out=False):
    missing = {name: info for name, info in registry["tools"].items() 
               if not info.get("path") or not info.get("verified")}
    if json_out:
        print(json.dumps(missing, indent=2))
        return
    if not missing:
        print("✅ All tools registered")
        return
    print(f"❌ {len(missing)} tools missing:")
    for name, info in missing.items():
        note = info.get("_note", "")
        print(f"   {name}: {note or 'not installed'}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    json_out = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]
    registry = load()
    
    cmd = args[0]
    if cmd == "list":
        cmd_list(registry, json_out)
    elif cmd == "get" and len(args) >= 2:
        cmd_get(registry, args[1], json_out)
    elif cmd == "set" and len(args) >= 4:
        cmd_set(registry, args[1], args[2], args[3])
    elif cmd == "missing":
        cmd_missing(registry, json_out)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
