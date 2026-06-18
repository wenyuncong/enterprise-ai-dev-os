#!/usr/bin/env python3
"""Audit the portable AI development methodology repository.

The script checks the release-facing knowledge base and skips private local
archives that are intentionally excluded from the publishable package.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


OFFICIAL_SCAN_ROOTS = [
    "AGENTS.md",
    "rules",
    "skills",
    "methodology",
    "docs",
    "README.md",
]

PORTABILITY_EXCLUDES = {
    Path("docs/ERP_TERM_AUDIT.md"),
    Path("docs/每日调研回写/2026-06-17_可行性分析.md"),
}

PRIVATE_ARCHIVE_PREFIXES = (
    "reference",
    "备用",
    "verification-demo",
)

BLOCKED_PATTERNS = [
    (re.compile(r"\b[A-Z]:[/\\][^\s`\"']+", re.IGNORECASE), "hard-coded local workspace path"),
    (re.compile("gerp" + r"[-_]" + "enterprise" + r"[-_]" + "mainline", re.IGNORECASE), "hard-coded source repository name"),
    (re.compile(r"docs[/\\]全项目总控_20260331"), "legacy GERP control-doc path"),
]


@dataclass
class Issue:
    severity: str
    code: str
    path: Path
    message: str


def rel(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def iter_files(root: Path, target: str) -> list[Path]:
    path = root / target
    if not path.exists():
        return []
    if path.is_file():
        return [path]
    return [p for p in path.rglob("*") if p.is_file()]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"(?s)^---\s*\n(.*?)\n---\s*\n?(.*)$", text)
    if not match:
        return {}, text
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, match.group(2)


def load_manifest(root: Path, issues: list[Issue]) -> dict:
    manifest_path = root / "skills" / "SKILL_MANIFEST.json"
    if not manifest_path.exists():
        issues.append(Issue("FAIL", "MANIFEST_MISSING", rel(manifest_path, root), "skills/SKILL_MANIFEST.json is required."))
        return {}
    try:
        return json.loads(read_text(manifest_path))
    except Exception as exc:  # pragma: no cover - defensive CLI error report
        issues.append(Issue("FAIL", "MANIFEST_INVALID", rel(manifest_path, root), f"manifest is not valid JSON: {exc}"))
        return {}


def check_manifest(root: Path, manifest: dict, issues: list[Issue]) -> None:
    skill_files = sorted((root / "skills").rglob("SKILL.md"))
    official = manifest.get("officialSkills", [])
    manifest_paths = {item.get("path") for item in official}
    actual_paths = {str(rel(path, root)).replace("\\", "/") for path in skill_files}

    if manifest.get("officialSkillRoot") != "skills/":
        issues.append(Issue("FAIL", "MANIFEST_ROOT", Path("skills/SKILL_MANIFEST.json"), "officialSkillRoot must be skills/."))

    if len(official) != len(actual_paths):
        issues.append(
            Issue(
                "FAIL",
                "MANIFEST_COUNT",
                Path("skills/SKILL_MANIFEST.json"),
                f"manifest lists {len(official)} official skills but filesystem has {len(actual_paths)} SKILL.md files.",
            )
        )

    for missing in sorted(actual_paths - manifest_paths):
        issues.append(Issue("FAIL", "MANIFEST_MISSING_SKILL", Path(missing), "skill exists on disk but is not listed in manifest."))
    for extra in sorted(manifest_paths - actual_paths):
        issues.append(Issue("FAIL", "MANIFEST_STALE_SKILL", Path(extra), "manifest lists a skill that does not exist on disk."))

    for item in official:
        name = item.get("name", "")
        layer = item.get("layer", "")
        maturity = item.get("maturity", "")
        if not name or not layer or not maturity:
            issues.append(Issue("FAIL", "MANIFEST_FIELD", Path("skills/SKILL_MANIFEST.json"), f"incomplete manifest row: {item!r}"))
        if maturity not in {"raw", "generalized", "callable", "verified", "deprecated"}:
            issues.append(Issue("FAIL", "MANIFEST_MATURITY", Path("skills/SKILL_MANIFEST.json"), f"invalid maturity for {name}: {maturity}"))


def check_portability(root: Path, issues: list[Issue]) -> None:
    for target in OFFICIAL_SCAN_ROOTS:
        for path in iter_files(root, target):
            rpath = rel(path, root)
            if rpath in PORTABILITY_EXCLUDES:
                continue
            if rpath.parts and rpath.parts[0] in PRIVATE_ARCHIVE_PREFIXES:
                continue
            if path.suffix.lower() not in {".md", ".json", ".py", ".ps1", ".mjs", ".js", ".yml", ".yaml"}:
                continue
            try:
                text = read_text(path)
            except UnicodeDecodeError as exc:
                issues.append(Issue("FAIL", "ENCODING", rpath, f"file is not valid UTF-8: {exc}"))
                continue
            for regex, label in BLOCKED_PATTERNS:
                if regex.search(text):
                    issues.append(Issue("FAIL", "PORTABILITY_RESIDUE", rpath, label))


def check_skill_structure(root: Path, issues: list[Issue]) -> None:
    for skill in sorted((root / "skills").rglob("SKILL.md")):
        rpath = rel(skill, root)
        text = read_text(skill)
        metadata, body = parse_frontmatter(text)
        if len(text.strip()) < 800:
            issues.append(Issue("WARN", "SKILL_THIN", rpath, "SKILL.md is short; confirm it is not only a placeholder."))
        if not metadata.get("name"):
            issues.append(Issue("WARN", "SKILL_FRONTMATTER", rpath, "missing frontmatter name."))
        description = metadata.get("description", "")
        if not description:
            issues.append(Issue("WARN", "SKILL_FRONTMATTER", rpath, "missing frontmatter description."))
        elif len(description) < 80:
            issues.append(Issue("WARN", "SKILL_DESCRIPTION", rpath, "description is short; include what the skill does and when to use it."))

        combined = f"{description}\n{body}".lower()
        body_lower = body.lower()
        desc_lower = description.lower()
        use_triggers = [
            "use when",
            "use for",
            "use before",
            "use at",
            "use to",
            "invoke for",
            "must be used",
        ]
        checks = {
            "purpose": bool(description) or "purpose" in body_lower or "goal" in body_lower,
            "when to use": any(term in desc_lower for term in use_triggers) or "when to use" in body_lower or "use when" in body_lower,
            "workflow": any(term in body_lower for term in ["workflow", "process", "steps", "checklist", "template", "contract", "core", "patterns"]),
            "guardrail": any(term in combined for term in ["guardrail", "guardrails", "do not", "never", "must", "always", "avoid", "prefer"]),
        }
        missing = [item for item, passed in checks.items() if not passed]
        if missing:
            issues.append(Issue("WARN", "SKILL_STRUCTURE", rpath, f"missing common sections/terms: {', '.join(missing)}"))


def check_agent_paths(root: Path, issues: list[Issue]) -> None:
    for agent_file in [root / "AGENTS.md", root / "rules" / "AGENTS.md"]:
        if not agent_file.exists():
            issues.append(Issue("FAIL", "AGENTS_MISSING", rel(agent_file, root), "required rule file missing."))
            continue
        text = read_text(agent_file)
        for match in re.finditer(r"`([^`]+(?:SKILL\.md|\.md|\.py|\.ps1))`", text):
            raw = match.group(1)
            if raw.startswith("{") or raw.startswith("http") or raw.startswith("G:"):
                continue
            if "{" in raw or "}" in raw:
                continue
            candidate = root / raw.replace("/", "\\")
            if not candidate.exists() and raw.startswith(("skills/", "docs/", "scripts/", "methodology/", "rules/")):
                issues.append(Issue("FAIL", "AGENTS_PATH", rel(agent_file, root), f"referenced path does not exist: {raw}"))


def check_private_archive_notice(root: Path, issues: list[Issue]) -> None:
    readme = root / "备用" / "README.md"
    if not readme.exists():
        issues.append(Issue("FAIL", "PRIVATE_ARCHIVE_NOTICE", rel(readme, root), "private archive must explain that it is not the official skill root."))


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the AI methodology repository.")
    parser.add_argument("--project-root", default=".", help="Repository root to audit.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    issues: list[Issue] = []

    manifest = load_manifest(root, issues)
    if manifest:
        check_manifest(root, manifest, issues)
    check_portability(root, issues)
    check_skill_structure(root, issues)
    check_agent_paths(root, issues)
    check_private_archive_notice(root, issues)

    result = {
        "projectRoot": str(root),
        "passed": not any(issue.severity == "FAIL" for issue in issues),
        "failCount": sum(1 for issue in issues if issue.severity == "FAIL"),
        "warnCount": sum(1 for issue in issues if issue.severity == "WARN"),
        "issues": [
            {
                "severity": issue.severity,
                "code": issue.code,
                "path": str(issue.path).replace("\\", "/"),
                "message": issue.message,
            }
            for issue in issues
        ],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"Methodology audit: {status}")
        print(f"Failures: {result['failCount']} | Warnings: {result['warnCount']}")
        for issue in issues:
            print(f"[{issue.severity}] {issue.code} {str(issue.path).replace(chr(92), '/')}: {issue.message}")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
