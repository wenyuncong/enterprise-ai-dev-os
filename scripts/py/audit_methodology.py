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
    (re.compile(r"docs[/\\]全项目总控[_-]\d{8}"), "legacy dated control-doc path"),
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


def repo_path(root: Path, raw: str) -> Path:
    """Resolve a repository-relative path with either slash style."""
    return root.joinpath(*[part for part in re.split(r"[/\\]+", raw) if part])


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


def check_5s_delivery_governance(root: Path, manifest: dict, issues: list[Issue]) -> None:
    skill_path = Path("skills/core/ai-5s-delivery-governor/SKILL.md")
    absolute_skill_path = root / skill_path
    if not absolute_skill_path.exists():
        issues.append(Issue("FAIL", "FIVE_S_SKILL_MISSING", skill_path, "5S delivery governance skill is required."))
        return

    official = manifest.get("officialSkills", [])
    registered = next((item for item in official if item.get("name") == "ai-5s-delivery-governor"), None)
    if not registered:
        issues.append(Issue("FAIL", "FIVE_S_MANIFEST", Path("skills/SKILL_MANIFEST.json"), "5S delivery skill is not registered."))
    elif registered.get("path") != str(skill_path).replace("\\", "/"):
        issues.append(Issue("FAIL", "FIVE_S_MANIFEST", Path("skills/SKILL_MANIFEST.json"), "5S delivery skill has an invalid manifest path."))

    text = read_text(absolute_skill_path).lower()
    required_terms = ["scope", "specify", "ship", "safeguard", "sell", "l0", "l3", "complete", "blocked"]
    missing = [term for term in required_terms if term not in text]
    if missing:
        issues.append(
            Issue(
                "FAIL",
                "FIVE_S_SKILL_STRUCTURE",
                skill_path,
                f"5S delivery skill is missing required lifecycle terms: {', '.join(missing)}",
            )
        )

    rules_path = Path("rules/AGENTS.md")
    rules_text = read_text(root / rules_path).lower() if (root / rules_path).exists() else ""
    if "5s delivery governance" not in rules_text or "scope -> specify -> ship -> safeguard -> sell" not in rules_text:
        issues.append(Issue("FAIL", "FIVE_S_RULES", rules_path, "canonical rules must define the 5S delivery lifecycle."))


def check_product_directed_delivery(root: Path, manifest: dict, issues: list[Issue]) -> None:
    skill_path = Path("skills/core/ai-product-directed-delivery/SKILL.md")
    absolute_skill_path = root / skill_path
    if not absolute_skill_path.exists():
        issues.append(Issue("FAIL", "PRODUCT_DELIVERY_SKILL_MISSING", skill_path, "product-directed delivery skill is required."))
        return

    official = manifest.get("officialSkills", [])
    registered = next((item for item in official if item.get("name") == "ai-product-directed-delivery"), None)
    if not registered:
        issues.append(Issue("FAIL", "PRODUCT_DELIVERY_MANIFEST", Path("skills/SKILL_MANIFEST.json"), "product-directed delivery skill is not registered."))
    elif registered.get("path") != str(skill_path).replace("\\", "/"):
        issues.append(Issue("FAIL", "PRODUCT_DELIVERY_MANIFEST", Path("skills/SKILL_MANIFEST.json"), "product-directed delivery skill has an invalid manifest path."))

    text = read_text(absolute_skill_path).lower()
    required_terms = [
        "product owner",
        "atomic service",
        "atomic orchestration",
        "aggregate interface",
        "command gateway",
        "ui atom",
        "host page",
        "business-flow acceptance",
        "safe change",
        "code location",
        "working-tree",
        "destructive",
        "impact",
        "exact task-owned",
        "business ambiguity",
    ]
    missing = [term for term in required_terms if term not in text]
    if missing:
        issues.append(
            Issue(
                "FAIL",
                "PRODUCT_DELIVERY_SKILL_STRUCTURE",
                skill_path,
                f"product-directed delivery skill is missing required terms: {', '.join(missing)}",
            )
        )

    rules_path = Path("rules/AGENTS.md")
    rules_text = read_text(root / rules_path).lower() if (root / rules_path).exists() else ""
    required_rule_terms = [
        "product-directed ai delivery",
        "command gateway",
        "safe ai change and code location",
        "read, prove, then change",
        "exact file or hunk staging",
        "business ambiguity",
    ]
    missing_rule_terms = [term for term in required_rule_terms if term not in rules_text]
    if missing_rule_terms:
        issues.append(
            Issue(
                "FAIL",
                "PRODUCT_DELIVERY_RULES",
                rules_path,
                f"canonical rules must define product-owner, safety, and code-location boundaries: {', '.join(missing_rule_terms)}",
            )
        )


def check_delivery_operating_assets(root: Path, issues: list[Issue]) -> None:
    matrix_path = Path("docs/全项目总控/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md")
    template_path = Path("docs/_templates/全项目总控/AI_PRODUCT_DELIVERY_TASK_TEMPLATE.md")
    scenario_path = Path("scripts/py/test_methodology_scenarios.py")

    required_files = {
        matrix_path: "delivery skill responsibility matrix is required.",
        template_path: "AI product delivery task template is required.",
        scenario_path: "methodology scenario regression runner is required.",
    }
    for path, message in required_files.items():
        if not (root / path).exists():
            issues.append(Issue("FAIL", "DELIVERY_OPERATING_ASSET_MISSING", path, message))

    if (root / matrix_path).exists():
        matrix_text = read_text(root / matrix_path).lower()
        required_matrix_terms = [
            "one primary owner",
            "ai-rule-dispatcher",
            "ai-chief-planner",
            "ai-task-decomposer",
            "ai-product-directed-delivery",
            "ai-5s-delivery-governor",
            "ai-runtime-verify",
        ]
        missing = [term for term in required_matrix_terms if term not in matrix_text]
        if missing:
            issues.append(
                Issue(
                    "FAIL",
                    "DELIVERY_RESPONSIBILITY_MATRIX",
                    matrix_path,
                    f"responsibility matrix is missing required ownership terms: {', '.join(missing)}",
                )
            )

    if (root / template_path).exists():
        template_text = read_text(root / template_path).lower()
        required_template_terms = [
            "product owner input",
            "code location and truth map",
            "delete / rename / migration classification",
            "executable batches",
            "verification record",
            "product acceptance",
            "delivery closure",
        ]
        missing = [term for term in required_template_terms if term not in template_text]
        if missing:
            issues.append(
                Issue(
                    "FAIL",
                    "DELIVERY_TASK_TEMPLATE",
                    template_path,
                    f"AI product delivery task template is missing required sections: {', '.join(missing)}",
                )
            )

    rules_path = Path("rules/AGENTS.md")
    rules_text = read_text(root / rules_path).lower() if (root / rules_path).exists() else ""
    required_rule_terms = [
        "delivery roles, task pack, and methodology regression",
        "ai_delivery_skill_responsibility_matrix.md",
        "ai_product_delivery_task_template.md",
        "test_methodology_scenarios.py",
    ]
    missing = [term for term in required_rule_terms if term not in rules_text]
    if missing:
        issues.append(
            Issue(
                "FAIL",
                "DELIVERY_OPERATING_RULES",
                rules_path,
                f"canonical rules must require delivery operating assets: {', '.join(missing)}",
            )
        )


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
            candidate = repo_path(root, raw)
            if not candidate.exists() and raw.startswith(("skills/", "docs/", "scripts/", "methodology/", "rules/")):
                issues.append(Issue("FAIL", "AGENTS_PATH", rel(agent_file, root), f"referenced path does not exist: {raw}"))


def check_private_archive_notice(root: Path, issues: list[Issue]) -> None:
    archive = root / "备用"
    if not archive.exists():
        return
    readme = archive / "README.md"
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
    check_5s_delivery_governance(root, manifest, issues)
    check_product_directed_delivery(root, manifest, issues)
    check_delivery_operating_assets(root, issues)
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
