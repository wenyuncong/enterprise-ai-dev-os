#!/usr/bin/env python3
"""Focused regression tests for the fail-closed delivery-contract validator."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_delivery_contract import validate  # noqa: E402


def base_contract() -> dict:
    return {
        "contract_id": "dc_unittest01",
        "schema_version": "1.0",
        "status": "approved",
        "project_id": "unit-test-project",
        "delivery": {
            "change_type": "bug",
            "target_line": "integration",
            "affected_flow": "order save",
            "gate": "L1",
        },
        "product_contract": {
            "outcome": "Refresh the list after a successful order save.",
            "acceptance_steps": ["A saved order appears in the list."],
            "non_goals": ["Do not change payments."],
        },
        "truth_owner": "order-service",
        "scope": {
            "write_allowlist": ["src/order/**"],
            "forbidden_paths": ["src/pay/**"],
            "out_of_scope": ["payments"],
            "destructive_classification": "none",
        },
        "test_strategy": {
            "mode": "alternative_evidence",
            "public_seam": "authoritative order API readback",
            "rationale": "Use an API readback for this narrow defect fix.",
        },
        "evidence_plan": {
            "final_proofs": [
                {
                    "proof_id": "proof_one",
                    "claim": "The saved order can be read back.",
                    "command_or_check": "POST /api/order then GET /api/order",
                    "must_run_after_final_change": True,
                }
            ]
        },
        "reviews": {
            "standards_truth": {"status": "pending", "evidence": "pending"},
            "product_spec": {"status": "pending", "evidence": "pending"},
        },
        "implementer": "agent-a",
        "created_at": "2026-09-01T00:00:00Z",
        "updated_at": "2026-09-01T00:00:00Z",
    }


def codes(contract: dict, changed: list[str] | None = None, freshness: bool = False) -> set[str]:
    return {issue.code for issue in validate(contract, changed or [], freshness)}


class TestDeliveryContractValidator(unittest.TestCase):
    def test_valid_approved_contract_passes(self) -> None:
        self.assertEqual(validate(base_contract(), ["src/order/a.py"], False), [])

    def test_missing_required_top_level_key_fails(self) -> None:
        contract = base_contract()
        del contract["truth_owner"]
        self.assertIn("CONTRACT_REQUIRED", codes(contract))

    def test_change_inside_allowlist_passes(self) -> None:
        self.assertNotIn("CONTRACT_SCOPE_ESCAPE", codes(base_contract(), ["src/order/sub/x.py"]))

    def test_change_outside_allowlist_fails(self) -> None:
        self.assertIn("CONTRACT_SCOPE_ESCAPE", codes(base_contract(), ["src/other/x.py"]))

    def test_forbidden_path_fails(self) -> None:
        self.assertIn("CONTRACT_FORBIDDEN_PATH", codes(base_contract(), ["src/pay/refund.py"]))

    def test_broad_allowlist_stars_fails(self) -> None:
        for broad in ("*", "**", "/**"):
            contract = base_contract()
            contract["scope"]["write_allowlist"] = [broad]
            self.assertIn("CONTRACT_ALLOWLIST_BROAD", codes(contract))

    def test_destructive_needs_explicit_owner_confirmation(self) -> None:
        contract = base_contract()
        contract["scope"]["destructive_classification"] = "explicit_owner_confirmation"
        self.assertIn("CONTRACT_OWNER_CONFIRMATION", codes(contract))
        contract["owner_confirmation"] = "confirmed"
        self.assertNotIn("CONTRACT_OWNER_CONFIRMATION", codes(contract))

    def test_red_green_requires_focused_test_command(self) -> None:
        contract = base_contract()
        contract["test_strategy"] = {
            "mode": "red_green",
            "public_seam": "public order service method",
            "rationale": "New behavior needs a focused test.",
        }
        self.assertIn("CONTRACT_TEST_COMMAND", codes(contract))
        contract["test_strategy"]["focused_test_command"] = "pytest tests/order"
        self.assertNotIn("CONTRACT_TEST_COMMAND", codes(contract))

    def safeguarded(self, gate: str = "L2", verifier: str | None = "agent-b") -> dict:
        contract = base_contract()
        contract["status"] = "safeguarded"
        contract["delivery"]["gate"] = gate
        if verifier is not None:
            contract["verification_owner"] = verifier
        contract["reviews"] = {
            "standards_truth": {"status": "passed", "evidence": "authoritative readback"},
            "product_spec": {"status": "passed", "evidence": "acceptance replayed"},
        }
        return contract

    def test_safeguarded_requires_both_reviews_passed(self) -> None:
        contract = self.safeguarded()
        self.assertEqual(codes(contract), set())
        contract["reviews"]["product_spec"]["status"] = "pending"
        self.assertIn("CONTRACT_PRODUCT_REVIEW", codes(contract))

    def test_l2_self_review_rejected(self) -> None:
        self.assertIn("CONTRACT_INDEPENDENT_VERIFIER", codes(self.safeguarded(verifier=None)))
        self.assertIn("CONTRACT_INDEPENDENT_VERIFIER", codes(self.safeguarded(verifier="agent-a")))
        self.assertNotIn("CONTRACT_INDEPENDENT_VERIFIER", codes(self.safeguarded(verifier="agent-b")))

    def test_l1_does_not_require_independent_verifier(self) -> None:
        self.assertNotIn("CONTRACT_INDEPENDENT_VERIFIER", codes(self.safeguarded(gate="L1", verifier="agent-a")))

    def test_freshness_requires_last_change_timestamp(self) -> None:
        self.assertIn("CONTRACT_LAST_CHANGE", codes(self.safeguarded(), freshness=True))

    def test_stale_evidence_rejected_fresh_evidence_passes(self) -> None:
        stale = self.safeguarded()
        stale["evidence_plan"]["last_relevant_change_at"] = "2026-09-05T10:00:00Z"
        stale["evidence_plan"]["evidence_records"] = [{
            "proof_id": "proof_one",
            "status": "passed",
            "finished_at": "2026-09-05T09:00:00Z",
            "reference": "run-1",
        }]
        self.assertIn("CONTRACT_STALE_EVIDENCE", codes(stale, freshness=True))

        fresh = copy.deepcopy(stale)
        fresh["evidence_plan"]["evidence_records"][0]["finished_at"] = "2026-09-05T11:00:00Z"
        self.assertEqual(validate(fresh, [], True), [])

    def test_evidence_record_must_be_passed(self) -> None:
        contract = self.safeguarded()
        contract["evidence_plan"]["last_relevant_change_at"] = "2026-09-05T10:00:00Z"
        contract["evidence_plan"]["evidence_records"] = [{
            "proof_id": "proof_one",
            "status": "failed",
            "finished_at": "2026-09-05T11:00:00Z",
            "reference": "run-x",
        }]
        self.assertIn("CONTRACT_EVIDENCE_MISSING", codes(contract, freshness=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
