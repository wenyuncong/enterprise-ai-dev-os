#!/usr/bin/env python3
"""Focused regression tests for the evidence-metrics measurement module.

All expected figures are anchored to the real numbers in the papers and the
three-model report; no fabricated effect claims are introduced.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import evidence_metrics as em  # noqa: E402


class TestNumericalBeta(unittest.TestCase):
    def test_betainc_known_cdfs(self) -> None:
        # Beta(1,1) is uniform: I_x(1,1) = x.
        self.assertAlmostEqual(em.betainc(1, 1, 0.37), 0.37, places=9)
        # Beta(2,1) CDF is x^2.
        self.assertAlmostEqual(em.betainc(2, 1, 0.5), 0.25, places=9)
        # Beta(1,2) CDF is 1 - (1-x)^2.
        self.assertAlmostEqual(em.betainc(1, 2, 0.5), 0.75, places=9)

    def test_betainc_boundaries(self) -> None:
        self.assertEqual(em.betainc(3, 2, 0.0), 0.0)
        self.assertEqual(em.betainc(3, 2, 1.0), 1.0)

    def test_beta_ppf_inverts_cdf(self) -> None:
        self.assertAlmostEqual(em.beta_ppf(1, 1, 0.5), 0.5, places=7)
        # Beta(2,1) quantile is sqrt(q).
        self.assertAlmostEqual(em.beta_ppf(2, 1, 0.25), 0.5, places=7)

    def test_ppf_then_inc_roundtrip(self) -> None:
        for q in (0.025, 0.5, 0.975):
            x = em.beta_ppf(37.5, 618.5, q)
            self.assertAlmostEqual(em.betainc(37.5, 618.5, x), q, places=6)


class TestProportionIntervals(unittest.TestCase):
    def test_point_rate_real_figures(self) -> None:
        self.assertAlmostEqual(em.point_rate(37, 655), 0.056489, places=5)
        self.assertAlmostEqual(em.point_rate(127, 148), 0.858108, places=5)
        self.assertAlmostEqual(em.point_rate(69, 71), 0.971831, places=5)

    def test_point_rate_failclosed(self) -> None:
        with self.assertRaises(ValueError):
            em.point_rate(1, 0)
        with self.assertRaises(ValueError):
            em.point_rate(5, 4)

    def test_wilson_known_interval(self) -> None:
        lo, hi = em.wilson_interval(37, 655)
        self.assertAlmostEqual(lo, 0.041257, places=5)
        self.assertAlmostEqual(hi, 0.076892, places=5)
        self.assertTrue(0.0 <= lo < hi <= 1.0)

    def test_jeffreys_corroborates_wilson(self) -> None:
        jlo, jhi = em.jeffreys_interval(37, 655)
        wlo, whi = em.wilson_interval(37, 655)
        # The two independent intervals should be close (mutual corroboration).
        self.assertAlmostEqual(jlo, wlo, delta=0.002)
        self.assertAlmostEqual(jhi, whi, delta=0.002)

    def test_extreme_counts_do_not_degenerate(self) -> None:
        # Jeffreys prior keeps endpoints away from exact 0/1.
        lo0, hi0 = em.jeffreys_interval(0, 100)
        lon, hin = em.jeffreys_interval(100, 100)
        self.assertGreater(lo0, 0.0)
        self.assertLess(hin, 1.0)

    def test_summary_structure(self) -> None:
        s = em.summarize_rate(37, 655)
        d = s.to_dict()
        for key in ("successes", "total", "point", "wilson_low", "wilson_high",
                    "jeffreys_low", "jeffreys_high"):
            self.assertIn(key, d)


class TestSampleSize(unittest.TestCase):
    def test_ceil_sample_size(self) -> None:
        # Exact ceil of z^2 p(1-p)/d^2 with the precise 95% z value.
        self.assertEqual(em.required_sample_size(0.05), 385)
        self.assertEqual(em.required_sample_size(0.03), 1068)

    def test_raw_formula_matches_paper_approx(self) -> None:
        # Paper reports "about 384 / 1067" using the rounded z=1.96 before ceil.
        z = 1.96
        raw_05 = z * z * 0.25 / 0.05 ** 2
        raw_03 = z * z * 0.25 / 0.03 ** 2
        self.assertAlmostEqual(raw_05, 384.16, places=1)
        self.assertAlmostEqual(raw_03, 1067.11, places=1)

    def test_invalid_margin(self) -> None:
        with self.assertRaises(ValueError):
            em.required_sample_size(0.0)


class TestGradeAndStatus(unittest.TestCase):
    def test_grade_supports_conclusion(self) -> None:
        self.assertTrue(em.validate_grade("E1")["supports_conclusion"])
        self.assertTrue(em.validate_grade("e2")["supports_conclusion"])
        self.assertFalse(em.validate_grade("E3")["supports_conclusion"])
        self.assertFalse(em.validate_grade("E0")["supports_conclusion"])

    def test_grade_unknown(self) -> None:
        with self.assertRaises(ValueError):
            em.validate_grade("E9")

    def test_adjudication_three_way(self) -> None:
        self.assertEqual(em.adjudication_status(0, 0), em.STATUS_NOT_INSTRUMENTED)
        self.assertEqual(em.adjudication_status(148, 4), em.STATUS_UNDERPOWERED)
        self.assertEqual(em.adjudication_status(655, 33), em.STATUS_MEASURED)

    def test_data_clock_thresholds(self) -> None:
        # Enough events but too short a window stays underpowered.
        self.assertEqual(em.adjudication_status(300, 10), em.STATUS_UNDERPOWERED)
        # Long window but too few events stays underpowered.
        self.assertEqual(em.adjudication_status(50, 40), em.STATUS_UNDERPOWERED)


class TestCostCacheConstructs(unittest.TestCase):
    def test_cache_hit_rates(self) -> None:
        self.assertAlmostEqual(em.cache_token_hit_rate(80, 100), 0.8)
        self.assertAlmostEqual(em.cache_request_hit_rate(9, 10), 0.9)

    def test_net_input_and_savings(self) -> None:
        self.assertEqual(em.net_input_tokens(70, 20), 90)
        self.assertEqual(em.token_savings(80, 20), 60)
        self.assertEqual(em.token_savings(10, 20), 0)

    def test_per_task_cost(self) -> None:
        self.assertAlmostEqual(em.per_task_cost(3.70, 10), 0.37)
        with self.assertRaises(ValueError):
            em.per_task_cost(3.70, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
