#!/usr/bin/env python3
"""Focused regression tests for controlled project onboarding."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_onboarding import (  # noqa: E402
    bind_remote,
    build_index,
    classify_git_host,
    copy_plan,
    detect_ai_tools,
    detect_architecture,
    detect_git,
    govern_candidates,
    write_json,
)


class TestProjectOnboarding(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def test_profile_detects_stack_and_database(self) -> None:
        root = self.make_root()
        (root / "package.json").write_text('{"dependencies":{"vue":"3.5.0","mysql2":"3.0.0"}}', encoding="utf-8")
        (root / "package-lock.json").write_text("{}", encoding="utf-8")
        result = build_index(root, 100)
        self.assertIn("javascript", result["technology_profile"]["languages"])
        self.assertIn("vue", result["technology_profile"]["frameworks"])
        self.assertIn("mysql", result["technology_profile"]["databases"])
        self.assertIn("npm", result["technology_profile"]["package_managers"])

    def test_preflight_reports_conflicts_without_writing(self) -> None:
        source = self.make_root()
        target = self.make_root()
        (source / "AGENTS.md").write_text("source", encoding="utf-8")
        (source / "rules").mkdir()
        (source / "rules" / "AGENTS.md").write_text("rules", encoding="utf-8")
        (source / "docs" / "_templates").mkdir(parents=True)
        (source / "docs" / "_templates" / "x.md").write_text("x", encoding="utf-8")
        (source / "scripts" / "py" / "__pycache__").mkdir(parents=True)
        (source / "scripts" / "py" / "__pycache__" / "generated.pyc").write_bytes(b"generated")
        (target / "AGENTS.md").write_text("target", encoding="utf-8")
        plan = copy_plan(source, target, "lite")
        self.assertIn("AGENTS.md", plan["conflicts"])
        self.assertIn("rules/AGENTS.md", [row["path"] for row in plan["rows"]])
        self.assertNotIn("scripts/py/__pycache__/generated.pyc", [row["path"] for row in plan["rows"]])
        self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), "target")

    def test_candidate_without_lock_is_quarantined(self) -> None:
        root = self.make_root()
        candidate = root / "skills" / "candidates" / "untrusted"
        candidate.mkdir(parents=True)
        (candidate / "SKILL.md").write_text("---\nname: untrusted\ndescription: test\n---\n", encoding="utf-8")
        report = govern_candidates(root)
        self.assertFalse(report["passed"])
        self.assertEqual(report["candidates"][0]["state"], "quarantined")

    def test_valid_candidate_is_only_ready_for_review(self) -> None:
        root = self.make_root()
        candidate = root / "skills" / "candidates" / "reviewable"
        candidate.mkdir(parents=True)
        (candidate / "SKILL.md").write_text("---\nname: reviewable\ndescription: test\n---\n", encoding="utf-8")
        write_json(candidate / "skill-source-lock.json", {
            "state": "candidate",
            "repository": "https://github.com/example/reviewable",
            "resolved_commit": "0123456789abcdef",
            "license_files": ["LICENSE"],
        })
        report = govern_candidates(root)
        self.assertTrue(report["passed"])
        self.assertEqual(report["candidates"][0]["state"], "ready-for-review")
        self.assertNotEqual(report["candidates"][0]["state"], "active")

    def test_candidate_without_license_is_quarantined(self) -> None:
        root = self.make_root()
        candidate = root / "skills" / "candidates" / "unlicensed"
        candidate.mkdir(parents=True)
        (candidate / "SKILL.md").write_text("---\nname: unlicensed\ndescription: test\n---\n", encoding="utf-8")
        write_json(candidate / "skill-source-lock.json", {
            "repository": "https://github.com/example/unlicensed",
            "resolved_commit": "0123456789abcdef",
            "license_files": [],
        })
        report = govern_candidates(root)
        self.assertFalse(report["passed"])
        self.assertIn("source lock lacks a license file", report["candidates"][0]["issues"])

    def test_detect_ai_tools_lists_present_adapters(self) -> None:
        root = self.make_root()
        (root / ".cursor").mkdir()
        (root / "CLAUDE.md").write_text("rules", encoding="utf-8")
        result = detect_ai_tools(root)
        self.assertIn("cursor", result["detected_tools"])
        self.assertIn("claude", result["detected_tools"])
        self.assertNotIn("qoder", result["detected_tools"])

    def test_architecture_detects_monolith_and_service_orientation(self) -> None:
        mono = self.make_root()
        (mono / "package.json").write_text("{}", encoding="utf-8")
        mono_files = [mono / "package.json"]
        self.assertEqual(detect_architecture(mono, mono_files)["inferred"], "monolith")

        oriented = self.make_root()
        (oriented / "docker-compose.yml").write_text("{}", encoding="utf-8")
        oriented_files = [oriented / "docker-compose.yml"]
        arch = detect_architecture(oriented, oriented_files)
        self.assertEqual(arch["inferred"], "service-oriented")
        self.assertEqual(arch["confidence"], "high")

    def test_classify_git_host_families(self) -> None:
        self.assertEqual(classify_git_host("https://github.com/owner/repo.git"), "github")
        self.assertEqual(classify_git_host("git@gitee.com:owner/repo.git"), "gitee")
        self.assertEqual(classify_git_host("https://gitlab.com/owner/repo"), "gitlab")
        self.assertEqual(classify_git_host("https://cnb.cool/owner/repo"), "cnb")

    def test_detect_git_reports_non_repository(self) -> None:
        root = self.make_root()
        self.assertFalse(detect_git(root)["is_git_repo"])

    def test_two_phase_scan_keeps_later_module_manifest_under_budget(self) -> None:
        from project_onboarding import tracked_files
        root = self.make_root()
        # A large early module with many ordinary files that would exhaust a naive budget.
        big = root / "big-module"
        big.mkdir()
        for index in range(60):
            (big / f"source_{index}.txt").write_text("x", encoding="utf-8")
        # A later module whose stack marker must survive even with a small file budget.
        later = root / "later-module"
        later.mkdir()
        (later / "package.json").write_text('{"dependencies":{}}', encoding="utf-8")
        files = tracked_files(root, max_files=30)
        self.assertTrue(any(f.name == "package.json" for f in files))
        profile = build_index(root, 30)
        self.assertIn("javascript", profile["technology_profile"]["languages"])

    def test_bind_remote_plans_without_apply_and_validates_url(self) -> None:
        import subprocess
        root = self.make_root()
        subprocess.run(["git", "init"], cwd=root, capture_output=True, check=True)
        plan = bind_remote(root, "origin", "https://example.com/owner/repo.git", apply=False)
        self.assertEqual(plan["status"], "will-add")
        self.assertFalse(plan["applied"])
        self.assertEqual(plan["commands"], ["git remote add origin https://example.com/owner/repo.git"])
        self.assertTrue(plan["upstream_command"].startswith("git push -u origin"))
        with self.assertRaises(ValueError):
            bind_remote(root, "origin", "not-a-url", apply=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
