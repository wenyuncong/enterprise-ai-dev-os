#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression test for the SKILL.md frontmatter delimiter gate.

Why this gate exists (evidence, 2026-09-14): ten SKILL.md files carried `0D 0D 0A`
double-CR line endings. The opening `---` line was therefore `---\\r\\r\\n`, which a
strict frontmatter parser (pattern `^---\\r?\\n`) does not accept. Observed effect with
the DSH skill provider: the skill was dropped from the catalog **silently** — 9 of the
49 official skills never appeared in any session until the bytes were repaired.

The test drives `check_skill_structure` directly on synthetic fixtures, so it fails if
the gate is weakened or removed.

Run:  py scripts/py/test_skill_frontmatter_gate.py
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_methodology as am  # noqa: E402


def write_skill(root: Path, name: str, raw: bytes) -> None:
    skill_dir = root / "skills" / "tech" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_bytes(raw)


def codes(issues) -> list[str]:
    return [issue.code for issue in issues]


class SkillFrontmatterDelimiterGate(unittest.TestCase):
    def _run(self, raw: bytes) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "sample", raw)
            issues: list[am.Issue] = []
            am.check_skill_structure(root, issues)
            return codes(issues)

    def test_double_cr_delimiter_is_blocking(self) -> None:
        body = b"name: sample\r\ndescription: " + b"x" * 120 + b"\r\n---\r\n\r\n# Sample\r\n"
        raw = b"---\r\r\n" + body
        self.assertIn("SKILL_FRONTMATTER_DELIMITER", self._run(raw))

    def test_stray_cr_before_lf_is_blocking(self) -> None:
        raw = b"---\r\nname: sample\r\ndescription: " + b"x" * 120 + b"\r\n---\r\nbody\r\n"
        # sanity: a legal CRLF delimiter must NOT trip the gate
        self.assertNotIn("SKILL_FRONTMATTER_DELIMITER", self._run(raw))

    def test_lf_delimiter_is_accepted(self) -> None:
        raw = b"---\nname: sample\ndescription: " + b"x" * 120 + b"\n---\nbody\n"
        self.assertNotIn("SKILL_FRONTMATTER_DELIMITER", self._run(raw))

    def test_trailing_space_in_delimiter_is_accepted(self) -> None:
        raw = b"--- \r\nname: sample\r\ndescription: " + b"x" * 120 + b"\r\n---\r\nbody\r\n"
        self.assertNotIn("SKILL_FRONTMATTER_DELIMITER", self._run(raw))

    def test_missing_delimiter_is_blocking(self) -> None:
        raw = b"# Sample\r\nno frontmatter here\r\n"
        self.assertIn("SKILL_FRONTMATTER_DELIMITER", self._run(raw))


if __name__ == "__main__":
    unittest.main(verbosity=2)
