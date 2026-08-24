#!/usr/bin/env python3
"""Regression tests for the runtime assets added by the research-driven builds.

Pure stdlib (unittest + subprocess), no external deps, so CI can run it with
any Python 3.10+.

Run: python scripts/py/test_runtime_assets.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable


def run(script: str, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(ROOT / "scripts" / "py" / script), *args],
                          capture_output=True, text=True, cwd=str(cwd), timeout=120)


class TestRuleRegistry(unittest.TestCase):
    def test_rules_json_valid_and_keys_match(self):
        registry = json.loads((ROOT / "rules" / "rules.json").read_text(encoding="utf-8"))
        keys = {r["key"] for r in registry["rules"]}
        # built-in rule keys surfaced by rule_lint --json
        proc = run("rule_lint.py", "--project-root", str(ROOT), "--json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        builtin = {r["key"] for r in json.loads(proc.stdout)["rules"]}
        self.assertEqual(keys, builtin, "rules.json keys must match built-in rules")
        for r in registry["rules"]:
            self.assertIn("severity", r)
            self.assertIn("trigger", r)
            self.assertIn("writeBlock", r)

    def test_rule_lint_passes(self):
        proc = run("rule_lint.py", "--project-root", str(ROOT))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


class TestDagPlanner(unittest.TestCase):
    def test_example_dag_plans(self):
        dag = ROOT / "docs" / "_templates" / "全项目总控" / "task_dag.json"
        proc = run("orchestrate_dag.py", "--dag", str(dag), "--json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["nodes"], 4)
        self.assertGreaterEqual(out["layers"], 2, "dependency chain must produce multiple layers")

    def test_cycle_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dag = Path(tmp) / "cycle.json"
            dag.write_text(json.dumps({"nodes": [
                {"id": "a", "depends": ["b"]},
                {"id": "b", "depends": ["a"]},
            ]}), encoding="utf-8")
            proc = run("orchestrate_dag.py", "--dag", str(dag))
            self.assertEqual(proc.returncode, 1)
            self.assertIn("cycle", proc.stdout)


class TestEvolutionCounter(unittest.TestCase):
    def test_threshold_triggers(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for i in range(3):
                proc = run("evolution_counter.py", "--project-root", tmp,
                           "record", "--pattern", "p1", "--context", f"c{i}")
                self.assertEqual(proc.returncode, 0)
            proc = run("evolution_counter.py", "--project-root", tmp, "report", "--json")
            out = json.loads(proc.stdout)
            self.assertEqual(len(out["candidates"]), 1)
            self.assertEqual(out["candidates"][0]["count"], 3)
            self.assertTrue(out["suggestion"])


class TestEventTrace(unittest.TestCase):
    def test_init_append_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            trace = Path(tmp) / "t.jsonl"
            self.assertEqual(run("event_trace.py", "init", "--trace", str(trace),
                                 "--delivery", "d").returncode, 0)
            self.assertEqual(run("event_trace.py", "append", "--trace", str(trace),
                                 "--phase", "Scope", "--action", "a").returncode, 0)
            self.assertEqual(run("event_trace.py", "append", "--trace", str(trace),
                                 "--phase", "Ship", "--action", "b",
                                 "--status", "fail").returncode, 0)
            replay = run("event_trace.py", "replay", "--trace", str(trace)).stdout
            self.assertIn("[FAIL]", replay)
            self.assertIn("2 event(s) replayed", replay)


class TestConstitution(unittest.TestCase):
    def test_constitution_passes(self):
        proc = run("check_constitution.py", "--project-root", str(ROOT), "--json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        out = json.loads(proc.stdout)
        self.assertTrue(out["passed"])
        self.assertEqual(len(out["musts"]), 8)


class TestAciAndEvidence(unittest.TestCase):
    def test_aci_json_valid(self):
        aci = json.loads((ROOT / "tools" / "aci_commands.json").read_text(encoding="utf-8"))
        self.assertIn("allowed", aci)
        self.assertIn("blocked", aci)
        self.assertIn("write", aci)

    def test_aggregate_cached(self):
        # Without cached evidence it should degrade gracefully; with --live it must pass.
        proc = run("aggregate_evidence.py", "--project-root", str(ROOT), "--live", "--json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        out = json.loads(proc.stdout)
        self.assertTrue(out["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
