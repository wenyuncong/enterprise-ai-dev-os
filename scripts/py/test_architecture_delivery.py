#!/usr/bin/env python3
"""Focused regression tests for architecture scanning and delivery-plan generation."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from architecture_delivery import generate_bundle  # noqa: E402


class TestArchitectureDelivery(unittest.TestCase):
    def make_project(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "backend" / "orders").mkdir(parents=True)
        (root / "frontend" / "src").mkdir(parents=True)
        (root / "database" / "migrations").mkdir(parents=True)
        (root / "tests").mkdir()
        (root / "pyproject.toml").write_text(
            "[project]\nname='demo'\ndependencies=['fastapi','sqlalchemy']\n",
            encoding="utf-8",
        )
        (root / "package.json").write_text(
            '{"dependencies":{"vue":"3.5.0","axios":"1.0.0"}}',
            encoding="utf-8",
        )
        (root / "backend" / "orders" / "api.py").write_text(
            "from .service import create_order\n"
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n"
            "@router.post('/orders')\n"
            "def create(): return create_order()\n",
            encoding="utf-8",
        )
        (root / "backend" / "orders" / "service.py").write_text(
            "from .repository import save_order\n"
            "def create_order(): return save_order()\n",
            encoding="utf-8",
        )
        (root / "backend" / "orders" / "repository.py").write_text(
            "def save_order(): return True\n",
            encoding="utf-8",
        )
        (root / "frontend" / "src" / "OrderPage.vue").write_text(
            "<script setup>import axios from 'axios'</script>\n"
            "<template><button>Order</button></template>\n",
            encoding="utf-8",
        )
        (root / "database" / "migrations" / "001_orders.sql").write_text(
            "CREATE TABLE orders (id INTEGER PRIMARY KEY, status TEXT);\n",
            encoding="utf-8",
        )
        (root / "tests" / "test_orders.py").write_text(
            "def test_create_order(): pass\n",
            encoding="utf-8",
        )
        return root

    def test_generates_language_neutral_ir_and_graph_edges(self) -> None:
        root = self.make_project()
        result = generate_bundle(root, root / "knowledge")
        ir = result["architecture_ir"]
        self.assertEqual(ir["schema_version"], "1.0")
        self.assertIn("python", ir["technology"]["languages"])
        self.assertIn("javascript", ir["technology"]["languages"])
        self.assertIn("fastapi", ir["technology"]["frameworks"])
        self.assertIn("vue", ir["technology"]["frameworks"])
        self.assertTrue(any(node["type"] == "api" for node in ir["nodes"]))
        self.assertTrue(any(node["type"] == "database_table" for node in ir["nodes"]))
        self.assertTrue(any(edge["type"] == "imports" for edge in ir["edges"]))
        self.assertTrue(any(edge["type"] == "api_to_module" for edge in ir["edges"]))

    def test_generates_applicable_steps_dag_and_site(self) -> None:
        root = self.make_project()
        result = generate_bundle(root, root / "knowledge")
        plan = result["delivery_plan"]
        self.assertEqual(len(plan["steps"]), 13)
        self.assertEqual(plan["steps"][0]["id"], "step-01")
        self.assertTrue(any(step["status"] == "applicable" for step in plan["steps"]))
        self.assertTrue(any(step["status"] == "not_applicable" for step in plan["steps"]))
        dag = result["task_dag"]
        self.assertTrue(any(node["id"] == "scan-architecture" for node in dag["nodes"]))
        self.assertTrue(any("depends" in node for node in dag["nodes"]))
        site = (root / "knowledge" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Architecture Knowledge Center", site)
        self.assertIn("orders", site)

    def test_outputs_are_machine_readable(self) -> None:
        root = self.make_project()
        output = root / "knowledge"
        result = generate_bundle(root, output)
        for name in ("architecture-ir.json", "delivery-plan.json", "task-dag.json"):
            loaded = json.loads((output / name).read_text(encoding="utf-8"))
            self.assertIsInstance(loaded, dict)
        self.assertEqual(result["output_dir"], str(output))


if __name__ == "__main__":
    unittest.main(verbosity=2)
