#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Methodology MCP server (stdio, zero dependencies).

Exposes the methodology as four callable tools so any MCP-capable harness (DSH via
`@deepseek-ai/dsh-mcp-client`, or any other client) can route work, pre-check writes,
run gates, and read bilingual sync status — instead of relying on a model to remember
rules from prose.

Tools
  methodology_route     任务 -> 该加载什么（技能切片/文档/风险级别/门禁）
  methodology_precheck  写入前静态拦截（禁写清单、越界路径、盘符/颜色/双 CR/BOM）
  methodology_gate      按级别跑仓库门禁，返回逐项 exit code
  methodology_sync      中英双语同步状态（哈希基线比对）

Transport: MCP stdio — newline-delimited JSON-RPC 2.0 on stdin/stdout.

Run standalone (any MCP client):
  {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}
  {"jsonrpc":"2.0","id":2,"method":"tools/list"}
  {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"methodology_route","arguments":{"task":"修复采购退货按钮"}}}

Self-test:
  py scripts/py/methodology_mcp_server.py --selftest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from methodology_rules import (  # noqa: E402  (规则单点：与 PreToolUse 钩子共用)
    check_bytes,
    check_name,
    force_utf8,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_INFO = {"name": "methodology-mcp", "version": "1.0.0"}
FALLBACK_PROTOCOL = "2025-06-18"

# ---------------------------------------------------------------- helpers

def _json(payload) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest().upper()


# ---------------------------------------------------------------- tools


def tool_route(args: dict) -> dict:
    """任务 -> 路由结果（技能切片 / 文档 / 风险级别 / 门禁）。"""
    task = str(args.get("task", "")).strip()
    project_root = Path(args.get("project_root") or REPO_ROOT).resolve()
    change_type = str(args.get("change_type") or "").strip().upper() or None

    table = None
    for candidate in (
        project_root / "task-routing.json",
        REPO_ROOT / "bootstrap" / "02_机读三件套" / "examples" / "gerp" / "task-routing.json",
    ):
        if candidate.exists():
            try:
                table = json.loads(candidate.read_text(encoding="utf-8-sig"))
                table["_source"] = str(candidate)
                break
            except json.JSONDecodeError:
                continue

    if not table:
        return {
            "matched_route_id": None,
            "risk_level": "L1",
            "load": {"skills": [{"name": "ai-rule-dispatcher", "lines": 50}]},
            "note": "未找到 task-routing.json，返回默认路由：先读 ai-rule-dispatcher 前 50 行。",
        }

    lowered = task.lower()
    scored: list[tuple[int, dict]] = []
    for entry in table.get("entries", []):
        match = entry.get("match", {})
        score = 0
        for kw in match.get("keywords", []):
            if kw and kw.lower() in lowered:
                score += 2
        for p in match.get("paths", []):
            if p and p.lower() in lowered:
                score += 1
        if change_type and change_type in (match.get("change_types") or []):
            score += 1
        if score:
            scored.append((score, entry))

    if not scored:
        defaults = table.get("defaults", {})
        return {
            "matched_route_id": None,
            "risk_level": defaults.get("risk_level", "L1"),
            "load": defaults.get("load", {}),
            "first_checks": defaults.get("pre_checks", []),
            "note": "未命中任何路由条目，返回 defaults。",
            "_source": table.get("_source"),
        }

    scored.sort(key=lambda item: item[0], reverse=True)
    best = scored[0][1]
    return {
        "matched_route_id": best.get("id"),
        "title": best.get("title"),
        "risk_level": best.get("risk_level"),
        "load": best.get("load", {}),
        "first_checks": best.get("pre_checks", []),
        "gates": best.get("gates", []),
        "notes": best.get("notes"),
        "also_matched": [entry.get("id") for _, entry in scored[1:4]],
        "_source": table.get("_source"),
    }


def tool_precheck(args: dict) -> dict:
    """写入前静态拦截：禁写清单 + 越界 + 内容级缺陷。"""
    project_root = Path(args.get("project_root") or REPO_ROOT).resolve()
    raw_paths = args.get("paths") or []
    if isinstance(raw_paths, str):
        raw_paths = [raw_paths]

    violations: list[dict] = []
    checked: list[str] = []

    for raw in raw_paths:
        path = Path(raw)
        if not path.is_absolute():
            path = (project_root / path).resolve()
        rel = str(path.relative_to(project_root)) if project_root in path.parents or path == project_root else str(path)
        checked.append(rel)

        if project_root not in path.parents and path != project_root:
            violations.append({
                "rule": "scope-escape",
                "file": rel,
                "hint": f"路径在项目根之外（{project_root.name}）：任务自有精确改动不得越界。",
            })

        for name_violation in check_name(path.name):
            violations.append({**name_violation, "file": rel})

        if path.exists() and path.is_file():
            for content_violation in check_bytes(rel, path.read_bytes()):
                violations.append(content_violation)

    return {"allow": not violations, "violations": violations, "checked": checked,
            "project_root": str(project_root)}


GATE_SETS = {
    "L1": ["rule_lint", "check_constitution"],
    "L2": ["rule_lint", "check_constitution", "audit_methodology", "audit_skill_health"],
    "L3": ["rule_lint", "check_constitution", "audit_methodology", "audit_skill_health",
           "audit_ai_native_governance", "audit_governance_contracts",
           "check_open_source_boundary", "audit_reference_links",
           "test_methodology_scenarios", "test_skill_frontmatter_gate",
           "test_delivery_contract_validator", "test_methodology_guard"],
}

GATE_COMMANDS = {
    "rule_lint": ["scripts/py/rule_lint.py", "--project-root", "."],
    "check_constitution": ["scripts/py/check_constitution.py", "--project-root", "."],
    "audit_methodology": ["scripts/py/audit_methodology.py", "--project-root", "."],
    "audit_skill_health": ["scripts/py/audit_skill_health.py", "--project-root", "."],
    "audit_ai_native_governance": ["scripts/py/audit_ai_native_governance.py", "--project-root", "."],
    "audit_governance_contracts": ["scripts/py/audit_governance_contracts.py", "--project-root", "."],
    "check_open_source_boundary": ["scripts/py/check_open_source_boundary.py", "--project-root", "."],
    "audit_reference_links": ["scripts/py/audit_reference_links.py", "--project-root", "."],
    "test_methodology_scenarios": ["scripts/py/test_methodology_scenarios.py", "--project-root", "."],
    "test_skill_frontmatter_gate": ["scripts/py/test_skill_frontmatter_gate.py"],
    "test_delivery_contract_validator": ["scripts/py/test_delivery_contract_validator.py"],
    "test_methodology_guard": ["scripts/py/test_methodology_guard.py"],
}


def tool_gate(args: dict) -> dict:
    """按级别跑仓库门禁；只取 exit code（不抓管道输出，避免沙箱与缓冲问题）。"""
    project_root = Path(args.get("project_root") or REPO_ROOT).resolve()
    level = str(args.get("level") or "L2").upper()
    selected = args.get("gates") or GATE_SETS.get(level, GATE_SETS["L2"])

    results = []
    for gid in selected:
        cmd = GATE_COMMANDS.get(gid)
        if not cmd:
            results.append({"id": gid, "exit": None, "error": "unknown gate id"})
            continue
        script = project_root / cmd[0]
        if not script.exists():
            results.append({"id": gid, "exit": None, "error": f"missing script: {cmd[0]}"})
            continue
        started = time.time()
        proc = subprocess.run(
            [sys.executable, str(script), *cmd[1:]],
            cwd=str(project_root),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        results.append({"id": gid, "exit": proc.returncode,
                        "duration_ms": int((time.time() - started) * 1000)})

    failed = [r["id"] for r in results if r.get("exit") not in (0,)]
    return {"level": level, "pass": not failed, "results": results, "failed": failed,
            "project_root": str(project_root)}


def tool_sync(args: dict) -> dict:
    """中英双语同步状态：哈希基线 vs 当前英文源。"""
    edition = Path(args.get("edition_root") or (REPO_ROOT / "i18n" / "zh-CN")).resolve()
    baseline = edition / "90_校验" / "source_hash_baseline.txt"
    if not baseline.exists():
        return {"error": f"baseline not found: {baseline}"}

    synced, stale, missing = [], [], []
    for line in baseline.read_text(encoding="utf-8-sig").splitlines():
        if "|" not in line:
            continue
        rel, digest = line.rsplit("|", 1)
        rel = rel.strip()
        target = REPO_ROOT / rel
        if not target.exists():
            missing.append(rel)
        elif _hash(target) != digest.strip().upper():
            stale.append(rel)
        else:
            synced.append(rel)

    return {"edition": edition.name, "synced": len(synced), "stale": stale,
            "missing": missing, "in_sync": not stale and not missing,
            "site_present": (edition / "site" / "index.html").exists()}


TOOLS = [
    {
        "name": "methodology_route",
        "description": "任务路由：给出该任务应加载的技能切片、必读文档、风险级别与门禁。命中 task-routing.json。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "任务描述或报错文本"},
                "project_root": {"type": "string", "description": "项目根目录（默认本仓库）"},
                "change_type": {"type": "string", "enum": ["U", "B", "E", "N"]},
            },
            "required": ["task"],
        },
    },
    {
        "name": "methodology_precheck",
        "description": "写入前静态拦截：禁写文件名、越界路径、盘符路径、硬编码颜色、控制字符、双 CR、BOM、SKILL.md frontmatter 定界行。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "paths": {"type": "array", "items": {"type": "string"},
                          "description": "将要写入/修改的文件路径"},
                "project_root": {"type": "string"},
            },
            "required": ["paths"],
        },
    },
    {
        "name": "methodology_gate",
        "description": "按风险级别运行仓库门禁（L1/L2/L3），返回每项 exit code 与失败清单。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "level": {"type": "string", "enum": ["L1", "L2", "L3"]},
                "gates": {"type": "array", "items": {"type": "string"},
                          "description": "显式指定门禁 id（可选）"},
                "project_root": {"type": "string"},
            },
        },
    },
    {
        "name": "methodology_sync",
        "description": "中英双语同步状态：对比翻译基线与英文源当前哈希，列出待重同步文件。",
        "inputSchema": {
            "type": "object",
            "properties": {"edition_root": {"type": "string"}},
        },
    },
]

DISPATCH = {
    "methodology_route": tool_route,
    "methodology_precheck": tool_precheck,
    "methodology_gate": tool_gate,
    "methodology_sync": tool_sync,
}


# ---------------------------------------------------------------- JSON-RPC


def handle(request: dict) -> dict | None:
    method = request.get("method")
    rid = request.get("id")
    params = request.get("params") or {}

    if method == "initialize":
        requested = str(params.get("protocolVersion") or FALLBACK_PROTOCOL)
        return {
            "jsonrpc": "2.0",
            "id": rid,
            "result": {
                "protocolVersion": requested,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method in ("notifications/initialized", "initialized"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        fn = DISPATCH.get(name)
        if not fn:
            return {"jsonrpc": "2.0", "id": rid,
                    "error": {"code": -32602, "message": f"unknown tool: {name}"}}
        try:
            payload = fn(arguments)
            is_error = bool(payload.get("error"))
            return {
                "jsonrpc": "2.0",
                "id": rid,
                "result": {
                    "content": [{"type": "text", "text": _json(payload)}],
                    "isError": is_error,
                },
            }
        except Exception as exc:  # noqa: BLE001 - surface any tool failure to the client
            return {
                "jsonrpc": "2.0",
                "id": rid,
                "result": {
                    "content": [{"type": "text", "text": _json({"error": f"{type(exc).__name__}: {exc}"})}],
                    "isError": True,
                },
            }
    if rid is None:
        return None
    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": -32601, "message": f"method not found: {method}"}}


def serve() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = handle(request)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False))
            sys.stdout.write("\n")
            sys.stdout.flush()
    return 0


def selftest() -> int:
    """自检：不依赖任何 MCP 客户端，直接驱动 handle()。"""
    checks = []

    def check(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    init = handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-06-18"}})
    check("initialize echoes protocolVersion",
          init["result"]["protocolVersion"] == "2025-06-18", init["result"]["serverInfo"]["name"])

    listing = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    names = [t["name"] for t in listing["result"]["tools"]]
    check("tools/list exposes 4 tools", len(names) == 4, ", ".join(names))

    route = handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                    "params": {"name": "methodology_route",
                               "arguments": {"task": "修复采购退货已记账单据的按钮不一致"}}})
    route_body = json.loads(route["result"]["content"][0]["text"])
    check("route matches a route id", bool(route_body.get("matched_route_id")),
          str(route_body.get("matched_route_id")))

    pre = handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                  "params": {"name": "methodology_precheck",
                             "arguments": {"paths": ["scripts/py/_temp_x.py", "../outside.txt"]}}})
    pre_body = json.loads(pre["result"]["content"][0]["text"])
    rules = {v["rule"] for v in pre_body["violations"]}
    check("precheck blocks forbidden names and scope escape",
          "forbidden-name" in rules and "scope-escape" in rules, ", ".join(sorted(rules)))

    gate = handle({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
                   "params": {"name": "methodology_gate", "arguments": {"level": "L1"}}})
    gate_body = json.loads(gate["result"]["content"][0]["text"])
    check("gate L1 passes on this repo", gate_body.get("pass") is True,
          str([r.get("id") for r in gate_body.get("results", [])]))

    sync = handle({"jsonrpc": "2.0", "id": 6, "method": "tools/call",
                   "params": {"name": "methodology_sync", "arguments": {}}})
    sync_body = json.loads(sync["result"]["content"][0]["text"])
    check("sync reports in_sync", sync_body.get("in_sync") is True,
          f"synced={sync_body.get('synced')} stale={len(sync_body.get('stale', []))}")

    failed = [name for name, ok, _ in checks if not ok]
    for name, ok, detail in checks:
        print(f"  [{'OK' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    print(f"\n自检: {len(checks) - len(failed)}/{len(checks)} 通过")
    return 1 if failed else 0


def main() -> int:
    force_utf8()
    ap = argparse.ArgumentParser(description="Methodology MCP server (stdio)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    return serve()


if __name__ == "__main__":
    raise SystemExit(main())
