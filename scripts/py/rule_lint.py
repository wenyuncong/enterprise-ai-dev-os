#!/usr/bin/env python3
"""Rule Lint: executable checks for the methodology's own forbidden patterns.

Turns the non-negotiable rules in AGENTS.md into runnable checks. This is the
first executable slice of the Rule Runtime Lite direction: file/path-level
and text-level checks before any AST work.

Scope mirrors audit_methodology.py: official scan roots only; private local
archives (reference/, 备用/, verification-demo/, internal doc folders) are
excluded from the release package and therefore not linted.

Exit code: 1 when any FAIL-severity rule has hits, 0 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

OFFICIAL_SCAN_ROOTS = ["AGENTS.md", "rules", "skills", "methodology", "docs", "README.md"]
PORTABILITY_EXCLUDES = {
    Path("docs/ERP_TERM_AUDIT.md"),
    Path("docs/每日调研回写/2026-06-17_可行性分析.md"),
}
PRIVATE_LOCAL_DOC_PREFIXES = (("docs", "本地知识中心"),)
PRIVATE_ARCHIVE_PREFIXES = ("reference", "备用", "verification-demo")
ROOT_ALLOWED_FILES = {
    # methodology and repo essentials
    "AGENTS.md", "CLAUDE.md", "README.md", "LICENSE", "NOTICE",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "GOVERNANCE.md", "SECURITY.md",
    "SUPPORT.md", "package.json", "package-lock.json", ".editorconfig",
    ".gitignore", ".gitattributes", ".npmrc",
    # generated adapter outputs kept at root by tool conventions
    ".cursorrules", ".clinerules", ".windsurfrules", "CONVENTIONS.md",
}
CONTROL_CHAR_PATTERN = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
DRIVE_PATH_PATTERN = re.compile(r"\b[A-Z]:[\\/][^\s`\"']+", re.IGNORECASE)
HEX_COLOR_PATTERN = re.compile(r"#[0-9a-fA-F]{3,8}\b")
EMPTY_CATCH_PATTERN = re.compile(r"catch\s*(\([^)]*\))?\s*\{\s*\}")
SILENT_EXCEPT_PATTERN = re.compile(r"except\s+[^:]*:\s*(pass\s*)?(#.*)?\n(\s+pass\b)")


class Hit:
    def __init__(self, path: str, line: int, snippet: str):
        self.path = path
        self.line = line
        self.snippet = snippet

    def to_dict(self):
        return {"path": self.path, "line": self.line, "snippet": self.snippet[:160]}


def iter_scan_files(root: Path):
    """Yield (relative_path, text) for official scan roots, excluding private dirs."""
    for target in OFFICIAL_SCAN_ROOTS:
        path = root / target
        if not path.exists():
            continue
        files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()]
        for f in files:
            rpath = f.relative_to(root)
            if rpath in PORTABILITY_EXCLUDES:
                continue
            if any(rpath.parts[: len(p)] == p for p in PRIVATE_LOCAL_DOC_PREFIXES):
                continue
            if rpath.parts and rpath.parts[0] in PRIVATE_ARCHIVE_PREFIXES:
                continue
            if f.suffix.lower() not in {".md", ".json", ".py", ".ps1", ".mjs", ".js", ".yml", ".yaml"}:
                continue
            try:
                text = f.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                yield rpath, None  # encoding failure reported by rule
                continue
            yield rpath, text


def build_rules():
    rules = []

    def rule(key, name, severity, fn, hint):
        rules.append({"key": key, "name": name, "severity": severity, "check": fn, "hint": hint})

    def root_clutter(root):
        hits = []
        if (root / "AGENTS.md").exists():
            for f in sorted(root.iterdir()):
                if f.is_file() and f.name not in ROOT_ALLOWED_FILES:
                    hits.append(Hit(str(f.relative_to(root)), 1, "loose root file"))
        return hits

    def control_chars(root):
        hits = []
        for rpath, text in iter_scan_files(root):
            if text is None:
                hits.append(Hit(str(rpath), 1, "invalid UTF-8"))
                continue
            m = CONTROL_CHAR_PATTERN.search(text)
            if m:
                line = text.count("\n", 0, m.start()) + 1
                hits.append(Hit(str(rpath), line, f"control char U+{ord(m.group(0)):04X}"))
        return hits

    def drive_paths(root):
        hits = []
        for rpath, text in iter_scan_files(root):
            if text is None:
                continue
            for m in DRIVE_PATH_PATTERN.finditer(text):
                if m.group(0).startswith(("C:\\Program", "C:/Program")):
                    continue  # tooling references, not repo paths
                line = text.count("\n", 0, m.start()) + 1
                hits.append(Hit(str(rpath), line, m.group(0)))
        return hits

    def hardcoded_colors(root):
        hits = []
        for rpath, text in iter_scan_files(root):
            if text is None or not str(rpath).endswith((".css", ".vue", ".html", ".scss")):
                continue
            if ":root" in text and re.search(r"--[\w-]+\s*:\s*#[0-9a-fA-F]{3,8}", text):
                # theme variables exist: hard-coded colors outside variables are violations
                for m in HEX_COLOR_PATTERN.finditer(text):
                    line = text.count("\n", 0, m.start()) + 1
                    hits.append(Hit(str(rpath), line, m.group(0)))
        return hits

    def empty_catches(root):
        hits = []
        for rpath, text in iter_scan_files(root):
            if text is None or rpath.suffix not in {".js", ".mjs", ".ts"}:
                continue
            for m in EMPTY_CATCH_PATTERN.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                hits.append(Hit(str(rpath), line, "empty catch block"))
            for m in SILENT_EXCEPT_PATTERN.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                hits.append(Hit(str(rpath), line, "silent except"))
        return hits

    def stale_repo_paths(root):
        """detect references to the private GERP workspace in portable assets."""
        hits = []
        for rpath, text in iter_scan_files(root):
            if text is None:
                continue
            for m in re.finditer(r"(H:|G:)[\\/](gerp|企业级|梦境)[^\s`\"']*", text, re.IGNORECASE):
                line = text.count("\n", 0, m.start()) + 1
                hits.append(Hit(str(rpath), line, m.group(0)))
        return hits

    rule("root_clutter", "根目录散落文件", "WARN", root_clutter,
         "Project root must only hold AGENTS.md, .editorconfig, build files, and generated adapters.")
    rule("control_chars", "控制字符", "FAIL", control_chars,
         "Files must not contain forbidden control characters.")
    rule("drive_paths", "硬编码盘符路径", "FAIL", drive_paths,
         "Portable assets must not hard-code local drive paths.")
    rule("stale_repo_paths", "私有仓库路径残留", "FAIL", stale_repo_paths,
         "Portable assets must not reference the private GERP workspace.")
    rule("hardcoded_colors", "硬编码颜色", "WARN", hardcoded_colors,
         "Theme variables only; no hard-coded colors when a theme exists.")
    rule("empty_catches", "静默失败", "WARN", empty_catches,
         "Empty catch/except blocks hide failures; surface them at the correct severity.")
    return rules


def load_rule_registry(root: Path) -> dict:
    """Load rules/rules.json metadata (trigger/severity/write-block) if present.

    The registry is optional metadata; built-in rules remain the executable
    source. Returns {key: {trigger, writeBlock, severity, name}}.
    """
    path = root / "rules" / "rules.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return {r.get("key"): r for r in data.get("rules", []) if r.get("key")}


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the methodology's own forbidden patterns.")
    parser.add_argument("--project-root", default=".", help="Repository root to lint.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    rules = build_rules()
    registry = load_rule_registry(root)
    results = []
    fail_count = 0
    warn_count = 0

    for r in rules:
        hits = [h.to_dict() for h in r["check"](root)]
        if r["severity"] == "FAIL":
            fail_count += len(hits)
        else:
            warn_count += len(hits)
        meta = registry.get(r["key"], {})
        results.append({"key": r["key"], "name": r["name"], "severity": r["severity"],
                        "hits": hits, "hint": r["hint"],
                        "trigger": meta.get("trigger", ""),
                        "writeBlock": bool(meta.get("writeBlock", False))})

    passed = fail_count == 0
    out = {"projectRoot": str(root), "passed": passed, "failCount": fail_count,
           "warnCount": warn_count, "rules": results}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Rule lint: {'PASS' if passed else 'FAIL'}")
        print(f"Failures: {fail_count} | Warnings: {warn_count}")
        for r in results:
            if r["hits"]:
                print(f"[{r['severity']}] {r['key']}: {len(r['hits'])} hit(s)")
                for h in r["hits"][:5]:
                    print(f"    {h['path']}:{h['line']}  {h['snippet']}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
