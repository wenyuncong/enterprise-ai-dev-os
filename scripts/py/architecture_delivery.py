#!/usr/bin/env python3
"""Generate a language-neutral architecture graph and delivery plan.

The scanner is deliberately evidence-oriented. It infers structure from files,
manifests, imports, route declarations, SQL tables, and test/deploy markers; it
does not claim runtime authorization, business truth, or production closure.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git", ".venv", "venv", "node_modules", "dist", "build", "target",
    "__pycache__", "temp", "tmp", "reference", "skills", "knowledge",
    "备用", ".idea", ".vscode",
}
SOURCE_EXTS = {".py", ".js", ".mjs", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".cs", ".vue"}
MANIFEST_NAMES = {
    "package.json", "pyproject.toml", "requirements.txt", "pom.xml",
    "build.gradle", "build.gradle.kts", "go.mod", "Cargo.toml",
    "composer.json", "Gemfile",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def files(root: Path) -> list[Path]:
    result: list[Path] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        for name in names:
            path = Path(current) / name
            if path.is_file():
                result.append(path)
    return result


def technology(all_files: list[Path]) -> dict[str, Any]:
    names = {path.name for path in all_files}
    text = "\n".join(read(path) for path in all_files if path.name in MANIFEST_NAMES).lower()
    languages: list[str] = []
    markers = {
        "python": {"pyproject.toml", "requirements.txt", "setup.py", "Pipfile"},
        "javascript": {"package.json"},
        "java": {"pom.xml", "build.gradle", "build.gradle.kts"},
        "go": {"go.mod"},
        "rust": {"Cargo.toml"},
        "dotnet": {".csproj", ".fsproj"},
        "php": {"composer.json"},
        "ruby": {"Gemfile"},
    }
    for language, required in markers.items():
        if any(name in names for name in required) or (
            language == "dotnet" and any(path.suffix in required for path in all_files)
        ):
            languages.append(language)
    framework_tokens = {
        "fastapi": ("fastapi",), "django": ("django",), "flask": ("flask",),
        "vue": ('"vue"', "vue@"), "react": ('"react"', "react@"),
        "express": ('"express"', "express@"), "nestjs": ("@nestjs",),
        "spring-boot": ("spring-boot",), "flutter": ("flutter",),
        "gin": ("gin-gonic",), "actix": ("actix-web",),
        "aspnet-core": ("microsoft.aspnetcore",),
    }
    frameworks = [name for name, tokens in framework_tokens.items() if any(token in text for token in tokens)]
    database_tokens = {
        "mysql": ("mysql", "mariadb"), "postgresql": ("postgres", "postgresql"),
        "sqlite": ("sqlite",), "mongodb": ("mongodb", "mongoose"),
        "redis": ("redis",),
    }
    databases = [name for name, tokens in database_tokens.items() if any(token in text for token in tokens)]
    package_managers = []
    for manager, marker in {
        "npm": "package-lock.json", "pnpm": "pnpm-lock.yaml", "yarn": "yarn.lock",
        "maven": "pom.xml", "gradle": "build.gradle", "pip": "requirements.txt",
        "poetry": "poetry.lock", "cargo": "Cargo.lock", "go": "go.sum",
    }.items():
        if marker in names:
            package_managers.append(manager)
    return {
        "languages": sorted(languages),
        "frameworks": sorted(frameworks),
        "databases": sorted(databases),
        "package_managers": sorted(package_managers),
    }


def add_node(nodes: list[dict[str, Any]], seen: set[str], node_id: str, node_type: str,
             label: str, source: str, confidence: str = "observed") -> None:
    if node_id in seen:
        return
    seen.add(node_id)
    nodes.append({"id": node_id, "type": node_type, "label": label, "source": source, "confidence": confidence})


def scan_ir(root: Path) -> dict[str, Any]:
    all_files = files(root)
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    seen: set[str] = set()
    profile = technology(all_files)
    for path in all_files:
        relative = rel(path, root)
        if path.suffix.lower() in SOURCE_EXTS:
            parts = Path(relative).parts
            module = parts[0] if len(parts) > 1 else "."
            module_id = f"module:{module}"
            add_node(nodes, seen, module_id, "module", module, relative)
            file_id = f"file:{relative}"
            add_node(nodes, seen, file_id, "file", relative, relative)
            edges.append({"from": file_id, "to": module_id, "type": "belongs_to", "source": relative})
            text = read(path)
            imports = re.findall(r"^\s*(?:from|import)\s+([A-Za-z_][\w.]*)|^\s*import\s+([A-Za-z_][\w.]*)", text, re.M)
            for pair in imports:
                imported = next((item for item in pair if item), "")
                if imported:
                    target = imported.split(".")[0]
                    target_id = f"module:{target}"
                    add_node(nodes, seen, target_id, "module", target, relative, "inferred")
                    edges.append({"from": file_id, "to": target_id, "type": "imports", "source": relative})
            route_patterns = [
                r"@\s*(?:router\.)?(?:get|post|put|patch|delete)\s*\(\s*['\"]([^'\"]+)",
                r"(?:app|router)\.(?:get|post|put|patch|delete)\s*\(\s*['\"]([^'\"]+)",
                r"@(Get|Post|Put|Patch|Delete)Mapping\s*\(\s*['\"]([^'\"]+)",
            ]
            for pattern in route_patterns:
                for match in re.finditer(pattern, text, re.I):
                    route = next((value for value in reversed(match.groups()) if value), "")
                    api_id = f"api:{route}"
                    add_node(nodes, seen, api_id, "api", route, relative)
                    edges.append({"from": api_id, "to": module_id, "type": "api_to_module", "source": relative})
        if path.suffix.lower() == ".sql":
            for table in re.findall(r"CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+[`\"]?([A-Za-z_][\w]*)", read(path), re.I):
                table_id = f"db:{table}"
                add_node(nodes, seen, table_id, "database_table", table, relative)
        if path.name.lower().startswith(("test_", "tests_")) or "test" in path.parts:
            add_node(nodes, seen, f"test:{relative}", "test", relative, relative)
        if path.name.lower() in {"dockerfile", "docker-compose.yml", "docker-compose.yaml"} or path.name.endswith((".yml", ".yaml")):
            if any(token in path.name.lower() for token in ("docker", "compose", "ci", "workflow")):
                add_node(nodes, seen, f"deploy:{relative}", "deploy", relative, relative)
    for path in all_files:
        if path.name in MANIFEST_NAMES:
            add_node(nodes, seen, f"manifest:{rel(path, root)}", "dependency_manifest", rel(path, root), rel(path, root))
    return {
        "schema_version": "1.0",
        "generated_at": now(),
        "project_root": str(root),
        "scan_mode": "read-only-bounded",
        "technology": profile,
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": edges,
        "limitations": [
            "Static inference may miss dynamic routes, generated code, runtime configuration, and database state.",
            "The graph is discovery evidence, not authorization, business truth, or release evidence.",
        ],
    }


def delivery_plan(ir: dict[str, Any]) -> dict[str, Any]:
    node_types = {node["type"] for node in ir["nodes"]}
    has_db = "database_table" in node_types or bool(ir["technology"]["databases"])
    has_backend = bool({"api", "module"} & node_types)
    has_frontend = any(node["label"].endswith((".vue", ".tsx", ".jsx")) for node in ir["nodes"])
    has_tests = "test" in node_types
    has_deploy = "deploy" in node_types
    checks = [
        ("database", has_db), ("model", has_backend), ("repository", has_db and has_backend),
        ("service", has_backend), ("api", "api" in node_types), ("build", bool(ir["technology"]["package_managers"])),
        ("types", has_frontend and has_backend), ("frontend_service", has_frontend and "api" in node_types),
        ("frontend_page", has_frontend), ("integration", has_tests), ("seed", has_db),
        ("schema_sync", has_db), ("runtime", has_deploy or has_frontend),
    ]
    descriptions = [
        "Database initialization and schema verification", "Model/entity layer alignment",
        "Repository/mapper query verification", "Service and orchestration behavior",
        "API/controller contract and permission review", "Build and startup verification",
        "Client type contract generation", "Client service/API adapter verification",
        "UI Host/page integration and state coverage", "Integration and edge-case tests",
        "Seed data and business-flow validation", "Schema drift and instance synchronization",
        "Runtime/browser/API verification",
    ]
    steps = []
    for index, ((key, applicable), description) in enumerate(zip(checks, descriptions), start=1):
        status = "applicable" if applicable else "not_applicable"
        if key in {"schema_sync", "seed", "runtime"} and applicable:
            status = "needs_confirmation"
        steps.append({
            "id": f"step-{index:02d}", "number": index, "name": description,
            "status": status, "evidence_hint": f"project evidence for {key}",
            "source": "architecture_ir",
        })
    return {
        "schema_version": "1.0",
        "generated_at": now(),
        "basis": "Architecture IR static evidence",
        "steps": steps,
        "human_confirmation_required": [
            "business outcome, acceptance flow, destructive operations, migration and release authorization",
        ],
    }


def task_dag(plan: dict[str, Any]) -> dict[str, Any]:
    nodes = [{"id": "scan-architecture", "name": "Scan project and build Architecture IR", "depends": []}]
    previous = "scan-architecture"
    for step in plan["steps"]:
        if step["status"] == "not_applicable":
            continue
        node_id = step["id"]
        nodes.append({"id": node_id, "name": step["name"], "depends": [previous]})
        previous = node_id
    return {
        "schema_version": "1.0",
        "generated_at": now(),
        "nodes": nodes,
        "contracts": [{"from": "scan-architecture", "to": "step-01", "contract": "Architecture IR and evidence limits"}],
    }


def site_html(ir: dict[str, Any], plan: dict[str, Any], dag: dict[str, Any]) -> str:
    profile = ir["technology"]
    rows = "".join(
        f"<tr><td>{html.escape(node['type'])}</td><td>{html.escape(node['label'])}</td>"
        f"<td>{html.escape(node['source'])}</td><td>{html.escape(node['confidence'])}</td></tr>"
        for node in ir["nodes"]
    )
    steps = "".join(
        f"<li><strong>{step['id']}</strong> {html.escape(step['name'])} "
        f"<span class='status {step['status']}'>{step['status']}</span></li>"
        for step in plan["steps"]
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Architecture Knowledge Center</title>
<style>body{{font-family:system-ui,sans-serif;margin:2rem;color:#17202a}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #ddd;padding:.5rem;text-align:left}}.status{{padding:.15rem .4rem;border-radius:3px;background:#eee}}.applicable{{color:#176b3a}}.needs_confirmation{{color:#8a5b00}}.not_applicable{{color:#777}}</style></head>
<body><h1>Architecture Knowledge Center</h1>
<p>Read-only discovery evidence. It is not runtime authorization, database truth, or business closure.</p>
<h2>Technology</h2><p>Languages: {html.escape(", ".join(profile["languages"]) or "unknown")} |
Frameworks: {html.escape(", ".join(profile["frameworks"]) or "unknown")} |
Databases: {html.escape(", ".join(profile["databases"]) or "unknown")}</p>
<h2>13-step delivery plan</h2><ol>{steps}</ol>
<h2>Architecture nodes ({len(ir["nodes"])}) and edges ({len(ir["edges"])})</h2>
<table><thead><tr><th>Type</th><th>Label</th><th>Source</th><th>Confidence</th></tr></thead><tbody>{rows}</tbody></table>
<p>Task DAG nodes: {len(dag["nodes"])}</p></body></html>"""


def generate_bundle(root: Path, output_dir: Path) -> dict[str, Any]:
    ir = scan_ir(root)
    plan = delivery_plan(ir)
    dag = task_dag(plan)
    output_dir.mkdir(parents=True, exist_ok=True)
    payloads = {
        "architecture-ir.json": ir,
        "delivery-plan.json": plan,
        "task-dag.json": dag,
    }
    for name, payload in payloads.items():
        (output_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "index.html").write_text(site_html(ir, plan, dag), encoding="utf-8")
    return {"output_dir": str(output_dir), "architecture_ir": ir, "delivery_plan": plan, "task_dag": dag}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Architecture IR, delivery plan, task DAG, and knowledge center.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output", default="knowledge/architecture")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    result = generate_bundle(root, root / args.output)
    print(json.dumps({
        "passed": True, "output_dir": result["output_dir"],
        "nodes": len(result["architecture_ir"]["nodes"]),
        "edges": len(result["architecture_ir"]["edges"]),
        "steps": len(result["delivery_plan"]["steps"]),
        "dag_nodes": len(result["task_dag"]["nodes"]),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
