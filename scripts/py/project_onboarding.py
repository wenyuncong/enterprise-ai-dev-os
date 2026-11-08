#!/usr/bin/env python3
"""Inspect projects and safely stage methodology skills for governed adoption."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXCLUDED_DIRS = {
    ".git", ".agents", ".claude", ".codebuddy", ".continue", ".cursor", ".qoder",
    ".trae", ".windsurf", "node_modules", "dist", "build", "target", "temp", "tmp",
    "reference", "备用", "__pycache__",
    # Dependency caches and virtual environments: generated artifacts, same class as node_modules.
    ".m2", ".gradle", ".nuget", ".pytest_cache", ".cache", ".venv", "venv", "env",
}
INSTALL_EXCLUDED_DIRS = EXCLUDED_DIRS | {"candidates", "quarantine", "project"}
TECH_MARKERS = {
    "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "javascript": ["package.json"],
    "python": ["pyproject.toml", "requirements.txt", "Pipfile", "setup.py"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
    "dotnet": ["*.csproj", "*.fsproj"],
    "php": ["composer.json"],
    "ruby": ["Gemfile"],
}
DATABASE_MARKERS = {
    "mysql": ["mysql", "mariadb"],
    "postgresql": ["postgres", "postgresql"],
    "sqlite": ["sqlite"],
    "mongodb": ["mongodb", "mongoose"],
    "redis": ["redis"],
}
# AI development tool adapter signals, mapped to the tool ids used in tools/adapters.json.
# Each signal is a project-root-relative directory or file that proves an adapter is present.
AI_TOOL_SIGNALS = {
    "codebuddy": [".codebuddy"],
    "claude": [".claude", "CLAUDE.md"],
    "codex": [".agents", "AGENTS.md"],
    "trae": [".trae"],
    "qoder": [".qoder"],
    "cursor": [".cursor", ".cursorrules"],
    "copilot": [".github/copilot-instructions.md"],
    "windsurf": [".windsurf", ".windsurfrules"],
    "cline": [".cline", ".clinerules"],
    "roo": [".roo"],
    "aider": ["CONVENTIONS.md"],
    "continue": [".continue"],
    "lingma": [".lingma"],
}
# File names that indicate orchestration of more than one independently deployable unit.
SERVICE_ORCHESTRATION_MARKERS = {
    "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml",
}
# Directories that conventionally hold multiple independently built applications or services.
MULTI_APP_DIRS = {"services", "apps", "packages"}
# Host suffix -> platform family. The detector stays neutral: it only classifies what it sees.
GIT_HOST_FAMILIES = {
    "github.com": "github",
    "gitee.com": "gitee",
    "gitlab.com": "gitlab",
    "bitbucket.org": "bitbucket",
}
CNB_HOST_SUFFIX = "cnb.cool"
# Build/dependency descriptors that determine the stack. They are collected first in a
# dedicated pass so traversal order can never starve a large later module (e.g. frontend).
KEY_MANIFEST_NAMES = {
    "pom.xml", "build.gradle", "build.gradle.kts", "package.json", "pyproject.toml",
    "requirements.txt", "pipfile", "setup.py", "go.mod", "cargo.toml", "composer.json",
    "gemfile", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock",
    "cargo.lock", "go.sum", "docker-compose.yml", "docker-compose.yaml", "compose.yml",
    "compose.yaml",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def is_excluded(path: Path, root: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts)


def tracked_files(root: Path, max_files: int = 5000) -> list[Path]:
    # Two-phase collection. Phase 1 gathers every build/dependency descriptor regardless of
    # traversal order; phase 2 fills the remaining budget with ordinary files. This prevents a
    # large early module (thousands of sources) from starving a later module's stack markers.
    manifests: list[Path] = []
    others: list[Path] = []
    for current_root, directories, names in os.walk(root):
        current = Path(current_root)
        directories[:] = [
            directory
            for directory in directories
            if directory not in EXCLUDED_DIRS
        ]
        for name in names:
            path = current / name
            if not path.is_file() or is_excluded(path, root):
                continue
            if name.lower() in KEY_MANIFEST_NAMES:
                manifests.append(path)
            else:
                others.append(path)
    return (manifests + others)[:max_files]


def marker_matches(path: Path, pattern: str) -> bool:
    if "*" not in pattern:
        return path.name == pattern
    return re.fullmatch(pattern.replace(".", r"\.").replace("*", ".*"), path.name) is not None


def dependency_text(files: list[Path]) -> str:
    parts = []
    for name in ("package.json", "pom.xml", "build.gradle", "build.gradle.kts", "pyproject.toml",
                 "requirements.txt", "composer.json", "go.mod", "Cargo.toml", "Gemfile"):
        parts.extend(read_text(path) for path in files if path.name == name)
    return "\n".join(parts).lower()


def detect_profile(files: list[Path]) -> dict[str, Any]:
    dependency = dependency_text(files)
    languages = [
        language for language, markers in TECH_MARKERS.items()
        if any(marker_matches(path, marker) for marker in markers for path in files)
    ]
    frameworks = []
    for name, tokens in {
        "spring-boot": ["spring-boot"],
        "vue": ['"vue"', "vue@"],
        "react": ['"react"', "react@"],
        "fastapi": ["fastapi"],
        "django": ["django"],
        "express": ['"express"', "express@"],
        "nestjs": ["@nestjs"],
        "flutter": ["flutter"],
    }.items():
        if any(token in dependency for token in tokens):
            frameworks.append(name)
    databases = [
        database for database, tokens in DATABASE_MARKERS.items()
        if any(token in dependency for token in tokens)
    ]
    package_managers = []
    for name, marker in {
        "npm": "package-lock.json", "pnpm": "pnpm-lock.yaml", "yarn": "yarn.lock",
        "maven": "pom.xml", "gradle": "build.gradle", "pip": "requirements.txt",
        "poetry": "poetry.lock", "cargo": "Cargo.lock", "go": "go.sum",
    }.items():
        if any(path.name == marker for path in files):
            package_managers.append(name)
    return {
        "languages": languages,
        "frameworks": frameworks,
        "databases": databases,
        "package_managers": package_managers,
    }


def detect_ai_tools(root: Path) -> dict[str, Any]:
    """Identify which AI tool adapters are actually present in the project root."""
    found = []
    evidence_map = {}
    for tool, signals in AI_TOOL_SIGNALS.items():
        present = [signal for signal in signals if (root / signal).exists()]
        if present:
            found.append(tool)
            evidence_map[tool] = present
    return {
        "detected_tools": sorted(found),
        "signals": evidence_map,
        "note": "Presence only. Run tools/deploy.ps1 -Tool <id> to refresh an adapter; adapters are generated, not source.",
    }


def detect_architecture(root: Path, files: list[Path]) -> dict[str, Any]:
    """Infer deployment shape from objective build/orchestration signals, with bounded confidence."""
    file_names = {path.name for path in files}
    orchestration = sorted(name for name in file_names if name in SERVICE_ORCHESTRATION_MARKERS)
    multi_app_dirs = []
    for top in MULTI_APP_DIRS:
        candidate = root / top
        if candidate.is_dir():
            children = [child for child in candidate.iterdir() if child.is_dir()]
            if len(children) > 1:
                multi_app_dirs.append({"dir": top, "unit_count": len(children)})
    # Independently deployable build manifests at more than one top-level unit.
    build_manifests = [
        path.relative_to(root).as_posix()
        for path in files
        if path.name in {"pom.xml", "build.gradle", "package.json", "pyproject.toml", "go.mod", "Cargo.toml"}
    ]
    signals = {
        "orchestration_files": orchestration,
        "multi_app_dirs": multi_app_dirs,
        "build_manifest_count": len(build_manifests),
    }
    if orchestration or multi_app_dirs:
        inferred = "service-oriented"
        confidence = "high"
    elif len(build_manifests) > 1:
        inferred = "modular"
        confidence = "medium"
    elif build_manifests:
        inferred = "monolith"
        confidence = "medium"
    else:
        inferred = "unknown"
        confidence = "low"
    return {"inferred": inferred, "confidence": confidence, "signals": signals}


def git_run(root: Path, args: list[str]) -> tuple[bool, str]:
    completed = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=False
    )
    output = (completed.stdout or "").strip()
    return completed.returncode == 0, output


def classify_git_host(url: str) -> str:
    cleaned = url.split("@", 1)[-1]
    cleaned = cleaned.removeprefix("ssh://").removeprefix("https://").removeprefix("http://")
    host = cleaned.split("/", 1)[0].split(":", 1)[0].lower()
    if host.endswith(CNB_HOST_SUFFIX):
        return "cnb"
    for suffix, family in GIT_HOST_FAMILIES.items():
        if host == suffix or host.endswith("." + suffix):
            return family
    return host or "unknown"


def detect_git(root: Path) -> dict[str, Any]:
    """Read remotes, current branch, and upstream binding without changing anything."""
    is_repo, _ = git_run(root, ["rev-parse", "--is-inside-work-tree"])
    if not is_repo:
        return {"is_git_repo": False}
    _, remote_lines = git_run(root, ["remote", "-v"])
    remotes: dict[str, dict[str, Any]] = {}
    for line in remote_lines.splitlines():
        match = re.match(r"^(\S+)\s+(\S+)\s+\((fetch|push)\)$", line.strip())
        if not match:
            continue
        name, url, kind = match.groups()
        entry = remotes.setdefault(name, {"url": url, "platform": classify_git_host(url), "kinds": []})
        entry["kinds"].append(kind)
    _, branch = git_run(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    upstream_ok, upstream = git_run(root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    return {
        "is_git_repo": True,
        "current_branch": branch,
        "remotes": remotes,
        "upstream": upstream if upstream_ok else None,
        "has_upstream": upstream_ok,
    }


def skill_inventory(root: Path) -> dict[str, Any]:
    skills = []
    for skill in root.glob("skills/**/SKILL.md"):
        relative = skill.relative_to(root).as_posix()
        if relative.startswith("skills/candidates/"):
            state = "candidate"
        elif relative.startswith("skills/quarantine/"):
            state = "quarantined"
        elif relative.startswith("skills/project/"):
            state = "project-private"
        else:
            state = "active-or-unclassified"
        skills.append({"path": relative, "state": state, "sha256": sha256(skill)})
    return {"count": len(skills), "skills": sorted(skills, key=lambda item: item["path"])}


def build_index(root: Path, max_files: int) -> dict[str, Any]:
    files = tracked_files(root, max_files)
    groups: dict[str, int] = {}
    for path in files:
        first = path.relative_to(root).parts[0] if path.relative_to(root).parts else "."
        groups[first] = groups.get(first, 0) + 1
    return {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "project_root": str(root),
        "scan_mode": "bounded-full",
        "file_limit": max_files,
        "truncated": len(files) >= max_files,
        "technology_profile": detect_profile(files),
        "architecture": detect_architecture(root, files),
        "ai_tools": detect_ai_tools(root),
        "git": detect_git(root),
        "top_level_file_counts": dict(sorted(groups.items())),
        "skill_inventory": skill_inventory(root),
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def install_paths(source_root: Path, mode: str) -> list[str]:
    if mode == "lite":
        return ["AGENTS.md", "rules", "docs/_templates"]
    return ["AGENTS.md", "CLAUDE.md", "rules", "skills", "docs/_templates", "tools", "scripts/py", "scripts/js"]


def status_for_copy(source: Path, target: Path) -> str:
    if not target.exists():
        return "add"
    if source.is_file() and target.is_file() and sha256(source) == sha256(target):
        return "same"
    return "conflict"


def install_files(source_root: Path, mode: str) -> list[Path]:
    files = []
    for relative in install_paths(source_root, mode):
        source = source_root / relative
        if source.is_file():
            files.append(source)
        elif source.is_dir():
            files.extend(
                path
                for path in source.rglob("*")
                if path.is_file() and not any(part in INSTALL_EXCLUDED_DIRS for part in path.relative_to(source_root).parts)
            )
    return sorted(files)


def copy_plan(source_root: Path, target_root: Path, mode: str) -> dict[str, Any]:
    if not (source_root / "AGENTS.md").exists():
        raise ValueError(f"source does not contain AGENTS.md: {source_root}")
    rows = []
    for source in install_files(source_root, mode):
        relative = source.relative_to(source_root)
        rows.append({
            "path": relative.as_posix(),
            "status": status_for_copy(source, target_root / relative),
            "source_sha256": sha256(source),
            "reason": "methodology installation asset",
        })
    conflicts = [row["path"] for row in rows if row["status"] == "conflict"]
    return {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "source_root": str(source_root),
        "target_root": str(target_root),
        "mode": mode,
        "policy": "add-only by default; conflicts require an explicit merge or overwrite decision",
        "rows": rows,
        "conflicts": conflicts,
        "rollback": "No target files are changed by preflight. Apply only from a reviewed plan and retain the generated plan as evidence.",
    }


def git_value(root: Path, args: list[str]) -> str:
    completed = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def stage_github_candidate(args: argparse.Namespace) -> dict[str, Any]:
    destination = Path(args.project_root).resolve() / "skills" / "candidates" / args.name
    if destination.exists():
        raise ValueError(f"candidate already exists: {destination}")
    if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+(?:\.git)?", args.repository):
        raise ValueError("repository must be an explicit github.com owner/repository URL")
    destination.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", args.ref, args.repository, str(destination)],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(completed.stderr.strip() or "git clone failed")
    license_files = [path.name for path in destination.iterdir() if path.name.lower().startswith(("license", "copying"))]
    commit = git_value(destination, ["rev-parse", "HEAD"])
    lock = {
        "schema_version": "1.0",
        "state": "candidate",
        "repository": args.repository,
        "requested_ref": args.ref,
        "resolved_commit": commit,
        "license_files": license_files,
        "staged_at": utc_now(),
        "activation": "prohibited until governance passes and an owner records an integration decision",
    }
    write_json(destination / "skill-source-lock.json", lock)
    return {"candidate": str(destination), "lock": lock}


def govern_candidates(root: Path) -> dict[str, Any]:
    candidate_root = root / "skills" / "candidates"
    findings = []
    for candidate in sorted(path for path in candidate_root.iterdir() if path.is_dir()) if candidate_root.exists() else []:
        lock = candidate / "skill-source-lock.json"
        skill_files = list(candidate.rglob("SKILL.md"))
        issues = []
        lock_value = {}
        if not lock.exists():
            issues.append("missing skill-source-lock.json")
        else:
            try:
                lock_value = json.loads(read_text(lock))
            except json.JSONDecodeError:
                issues.append("invalid skill-source-lock.json")
        if lock_value:
            if not lock_value.get("repository") or not lock_value.get("resolved_commit"):
                issues.append("source lock lacks repository or resolved commit")
            if not lock_value.get("license_files"):
                issues.append("source lock lacks a license file")
        if not skill_files:
            issues.append("no SKILL.md found")
        for skill in skill_files:
            raw = skill.read_bytes()[:16]
            if raw.startswith(b"\xef\xbb\xbf"):
                issues.append(f"BOM frontmatter: {skill.relative_to(root).as_posix()}")
            if not re.match(rb"^---[ \t]*(\r\n|\n)", raw.lstrip(b"\xef\xbb\xbf")):
                issues.append(f"invalid frontmatter delimiter: {skill.relative_to(root).as_posix()}")
        findings.append({
            "candidate": candidate.relative_to(root).as_posix(),
            "state": "ready-for-review" if not issues else "quarantined",
            "issues": issues,
        })
    return {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "activation_rule": "Candidates remain non-callable until the manifest, ownership decision, compatibility review, and audit gates pass.",
        "candidates": findings,
        "passed": not any(item["issues"] for item in findings),
    }


def bind_remote(root: Path, name: str, url: str, apply: bool) -> dict[str, Any]:
    """Plan (or apply) a platform-neutral git remote binding. The URL is always supplied explicitly."""
    is_repo, _ = git_run(root, ["rev-parse", "--is-inside-work-tree"])
    if not is_repo:
        raise ValueError("target is not a git repository")
    if not url or not re.match(r"^(https?://|ssh://|git@|git://)", url):
        raise ValueError("a valid explicit remote URL is required; no platform URL is hard-coded")
    existing_ok, existing_url = git_run(root, ["remote", "get-url", name])
    platform = classify_git_host(url)
    _, branch = git_run(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    plan: dict[str, Any] = {
        "schema_version": "1.0",
        "remote": name,
        "url": url,
        "platform": platform,
        "current_branch": branch,
    }
    if existing_ok:
        if existing_url == url:
            plan["status"] = "already-bound"
            plan["commands"] = []
        else:
            raise ValueError(
                f"remote {name} already exists with a different URL ({existing_url}); "
                "choose another name or resolve the conflict deliberately"
            )
    else:
        plan["status"] = "will-add"
        plan["commands"] = [f"git remote add {name} {url}"]
        # Upstream binding is a push (confirmation-gated), so it is emitted as a command, never auto-run.
        if branch:
            plan["upstream_command"] = f"git push -u {name} {branch}"
    plan["applied"] = False
    if apply and plan["commands"]:
        for command in plan["commands"]:
            parts = command.split()
            ok, output = git_run(root, parts[1:])
            if not ok:
                raise ValueError(f"command failed: {command} ({output})")
        plan["applied"] = True
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Controlled project onboarding and skill integration.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Generate a technology profile and bounded knowledge index.")
    inspect_parser.add_argument("--project-root", default=".")
    inspect_parser.add_argument("--output", default="knowledge/project-index.json")
    inspect_parser.add_argument("--max-files", type=int, default=5000)

    preflight_parser = subparsers.add_parser("preflight", help="Generate a non-mutating methodology copy plan.")
    preflight_parser.add_argument("--source-root", required=True)
    preflight_parser.add_argument("--project-root", required=True)
    preflight_parser.add_argument("--mode", choices=["lite", "full"], default="lite")
    preflight_parser.add_argument("--output", default="docs/全项目总控/methodology-install-plan.json")

    stage_parser = subparsers.add_parser("stage-github", help="Stage a GitHub skill candidate without activating it.")
    stage_parser.add_argument("--project-root", default=".")
    stage_parser.add_argument("--name", required=True)
    stage_parser.add_argument("--repository", required=True)
    stage_parser.add_argument("--ref", required=True)

    govern_parser = subparsers.add_parser("govern-candidates", help="Check staged candidates and emit a governance report.")
    govern_parser.add_argument("--project-root", default=".")
    govern_parser.add_argument("--output", default="knowledge/skill-candidate-governance.json")

    bind_parser = subparsers.add_parser("bind-remote", help="Plan or apply a platform-neutral remote binding (URL supplied explicitly).")
    bind_parser.add_argument("--project-root", default=".")
    bind_parser.add_argument("--name", default="origin")
    bind_parser.add_argument("--url", required=True)
    bind_parser.add_argument("--apply", action="store_true", help="Execute git remote add. Without it, only the plan is shown.")

    args = parser.parse_args()
    try:
        if args.command == "inspect":
            root = Path(args.project_root).resolve()
            result = build_index(root, args.max_files)
            write_json(root / args.output, result)
        elif args.command == "preflight":
            root = Path(args.project_root).resolve()
            result = copy_plan(Path(args.source_root).resolve(), root, args.mode)
            write_json(root / args.output, result)
        elif args.command == "stage-github":
            result = stage_github_candidate(args)
        elif args.command == "bind-remote":
            root = Path(args.project_root).resolve()
            result = bind_remote(root, args.name, args.url, args.apply)
        else:
            root = Path(args.project_root).resolve()
            result = govern_candidates(root)
            write_json(root / args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("passed", True) else 1
    except (OSError, ValueError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
