#!/usr/bin/env python3
"""Focused regression tests for controlled project onboarding."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_onboarding import build_index, copy_plan, govern_candidates, write_json  # noqa: E402


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
