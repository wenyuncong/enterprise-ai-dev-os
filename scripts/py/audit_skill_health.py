#!/usr/bin/env python3
"""Skill health audit: score every official skill beyond structural checks.

audit_methodology.py verifies skill *structure*; this script scores skill
*health*: broken references, missing trigger language, anti-pattern
phrasing, thin content, and stale metadata. It feeds the ai-skill-governor
evolution loop with per-skill scores.

Exit code: 1 if any FAIL-severity issue exists, otherwise 0.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

MIN_LENGTH = 800
STALE_DAYS = 180
ANTI_PATTERNS = [
    (re.compile(r"前端[^。\n]*(计算|校验|判断|决定|算[^。\n]*金额)"), "frontend business logic encouraged"),
    (re.compile(r"(临时绕过|暂时绕过|workaround[^。\n]*优先|先绕过)"), "degradation encouraged"),
    (re.compile(r"硬编码[^。\n]*(颜色|路径|文案)[^。\n]*(可以|允许|可接受)"), "hard-coding encouraged"),
    (re.compile(r"(写死|写死状态)"), "hard-coding encouraged"),
]


def load_manifest(root: Path) -> dict:
    path = root / "skills" / "SKILL_MANIFEST.json"
    return json.loads(path.read_text(encoding="utf-8-sig"))


def extract_refs(text: str, skill_dir: Path, root: Path) -> list[Path]:
    refs = []
    for m in re.finditer(r"`([^`]+)`", text):
        raw = m.group(1)
        if not raw.startswith(("skills/", "docs/", "scripts/", "methodology/", "tools/", "references/", "rules/")):
            continue
        if "{" in raw or raw.startswith("http"):
            continue
        base = skill_dir if raw.startswith("references/") else root
        refs.append(base.joinpath(*[p for p in raw.split("/") if p]))
    return refs


def score_skill(root: Path, item: dict) -> dict:
    name = item.get("name", "?")
    rel_path = Path(item.get("path", ""))
    skill_path = root / rel_path
    result = {"name": name, "layer": item.get("layer", ""), "maturity": item.get("maturity", ""),
              "score": 100, "issues": []}
    deductions = 0

    def issue(severity, code, msg, cost):
        nonlocal deductions
        result["issues"].append({"severity": severity, "code": code, "message": msg})
        deductions += cost

    if not skill_path.exists():
        issue("FAIL", "SKILL_MISSING", "SKILL.md does not exist", 100)
        result["score"] = max(0, 100 - deductions)
        return result

    text = skill_path.read_text(encoding="utf-8-sig")
    meta, body = {}, text
    if text.startswith("---"):
        m = re.match(r"(?s)^---\s*\n(.*?)\n---\s*\n?(.*)$", text)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            body = m.group(2)

    if not meta.get("name"):
        issue("FAIL", "FRONTMATTER_NAME", "missing frontmatter name", 20)
    if not meta.get("description"):
        issue("FAIL", "FRONTMATTER_DESC", "missing frontmatter description", 20)
    elif len(meta["description"]) < 80:
        issue("WARN", "DESC_SHORT", f"description only {len(meta['description'])} chars", 5)

    if len(text.strip()) < MIN_LENGTH:
        issue("WARN", "THIN", f"only {len(text.strip())} chars (min {MIN_LENGTH})", 15)

    for ref in extract_refs(text, skill_path.parent, root):
        if not ref.exists():
            issue("WARN", "BROKEN_REF", f"referenced path missing: {ref.relative_to(root).as_posix()}", 5)

    desc_lower = meta.get("description", "").lower()
    if not re.search(r"\buse[ds]?\s+(when|for|at|before|to)\b|\b(trigger|when to use|适用|触发)\b", desc_lower):
        issue("WARN", "NO_TRIGGER", "description lacks use-when/trigger language", 10)

    combined = (meta.get("description", "") + "\n" + body).lower()
    for pat, label in ANTI_PATTERNS:
        if pat.search(combined):
            issue("WARN", "ANTI_PATTERN", f"anti-pattern phrasing: {label}", 10)

    for key in ("version", "updated", "date", "lastUpdated"):
        val = meta.get(key, "")
        m = re.search(r"(20\d{2})[-/](\d{2})", val)
        if m:
            try:
                d = date(int(m.group(1)), int(m.group(2)), 1)
                age = (date.today() - d).days
                if age > STALE_DAYS:
                    issue("WARN", "STALE", f"{key}={val} is {age} days old", 5)
            except ValueError:
                pass
            break

    result["score"] = max(0, 100 - deductions)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Score skill health beyond structural checks.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-score", type=int, default=60, help="exit 1 if any skill scores below this")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    manifest = load_manifest(root)
    skills = [score_skill(root, item) for item in manifest.get("officialSkills", [])]
    skills.sort(key=lambda s: s["score"])

    fail_issues = [s for s in skills if any(i["severity"] == "FAIL" for i in s["issues"])]
    low = [s for s in skills if s["score"] < args.min_score]
    avg = round(sum(s["score"] for s in skills) / len(skills), 1) if skills else 0

    out = {
        "projectRoot": str(root),
        "totalSkills": len(skills),
        "averageScore": avg,
        "minScore": args.min_score,
        "belowMin": [s["name"] for s in low],
        "failSkills": [s["name"] for s in fail_issues],
        "skills": skills,
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Skill health: avg {avg}/100 across {len(skills)} skills")
        print(f"Below {args.min_score}: {[s['name'] for s in low] or 'none'}")
        print(f"FAIL issues: {[s['name'] for s in fail_issues] or 'none'}")
        for s in skills[:8]:
            print(f"  {s['score']:>3}  {s['name']}  {[i['code'] for i in s['issues']]}")
    return 0 if not fail_issues and not low else 1


if __name__ == "__main__":
    sys.exit(main())
