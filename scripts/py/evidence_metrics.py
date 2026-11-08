#!/usr/bin/env python3
"""Evidence metrics: code implementation of the paper's measurement formulas.

This module turns the statistical and measurement discipline described in the
methodology evidence gate (AGENTS.md section 6B) into executable, dependency-free
functions. It uses only the Python standard library so it runs on a fresh clone,
offline, in the same way the in-repository delivery gate does.

Implemented constructs (each maps to a formula in the papers / three-model report):
  * Proportion point estimate, Wilson score interval, Jeffreys Beta posterior
    credible interval (with a regularized incomplete Beta function and its inverse).
  * Sample-size / power requirement n = z^2 p(1-p) / d^2.
  * Evidence grading E0-E3 and the Measured / Underpowered / Not-instrumented
    adjudication status, including the data clock (>= 28 days and >= 200 events).
  * Reliability rate summaries (success, block, failure, self-recovery).
  * Cost and cache constructs (cache hit rate, net input tokens, token savings,
    per-task cost).

Usage:
  evidence_metrics.py --rate 37 655
  evidence_metrics.py --sample-size 0.05
  evidence_metrics.py --demo
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, asdict
from typing import Iterable

# --- Constants -------------------------------------------------------------

# Two-sided z value for a 95% interval.
Z_95 = 1.959963984540054
# Data-clock thresholds for effect claims (section 6B).
MIN_EVENTS = 200
MIN_DAYS = 28

# Evidence grades (03_证据核查与数据台账.md).
EVIDENCE_GRADES = {
    "E1": "Measured / computed directly this session; reproducible by script.",
    "E2": "Stated in repository documents; first-party claim needing cross-check.",
    "E3": "Marketing / financing material; must not be treated as fact.",
    "E0": "Missing / to be collected; must not enter a conclusion.",
}
# Adjudication status three-way classification (three-model report section 4).
STATUS_MEASURED = "Measured"
STATUS_UNDERPOWERED = "Underpowered"
STATUS_NOT_INSTRUMENTED = "Not-instrumented"


# --- Numerical helpers: regularized incomplete Beta and its inverse --------

def _beta_cf(a: float, b: float, x: float, max_iter: int = 200,
             eps: float = 3e-14) -> float:
    """Lentz's continued-fraction evaluation for the incomplete Beta function."""
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        # Even step.
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        # Odd step.
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    """Regularized incomplete Beta function I_x(a, b), value in [0, 1]."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    log_beta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(a * math.log(x) + b * math.log(1.0 - x) - log_beta)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _beta_cf(a, b, x) / a
    # Symmetry relation to evaluate the better-converging tail.
    return 1.0 - front * _beta_cf(b, a, 1.0 - x) / b


def beta_ppf(a: float, b: float, q: float, tol: float = 1e-9) -> float:
    """Inverse regularized incomplete Beta (quantile / ppf) via bisection."""
    if q <= 0.0:
        return 0.0
    if q >= 1.0:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if betainc(a, b, mid) < q:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2.0


# --- Proportion statistics -------------------------------------------------

def point_rate(successes: int, total: int) -> float:
    """Point estimate p = k / n. Fails closed on an empty denominator."""
    if total <= 0:
        raise ValueError("total must be positive (no denominator)")
    if successes < 0 or successes > total:
        raise ValueError("successes must be in [0, total]")
    return successes / total


def wilson_interval(successes: int, total: int, z: float = Z_95) -> tuple[float, float]:
    """Wilson score interval (frequency-practice), symmetric on the score scale."""
    p = point_rate(successes, total)
    z2 = z * z
    denom = 1.0 + z2 / total
    center = (p + z2 / (2.0 * total)) / denom
    half = (z / denom) * math.sqrt(
        p * (1.0 - p) / total + z2 / (4.0 * total * total)
    )
    return max(0.0, center - half), min(1.0, center + half)


def jeffreys_interval(successes: int, total: int,
                      credibility: float = 0.95) -> tuple[float, float]:
    """Jeffreys posterior Beta(k+1/2, n-k+1/2) credible interval (Bayesian)."""
    if not 0.0 < credibility < 1.0:
        raise ValueError("credibility must be in (0, 1)")
    alpha = successes + 0.5
    beta = total - successes + 0.5
    tail = (1.0 - credibility) / 2.0
    return beta_ppf(alpha, beta, tail), beta_ppf(alpha, beta, 1.0 - tail)


@dataclass
class RateSummary:
    """Structured rate report with two mutually corroborating intervals."""

    successes: int
    total: int
    point: float
    wilson_low: float
    wilson_high: float
    jeffreys_low: float
    jeffreys_high: float

    def to_dict(self) -> dict:
        return asdict(self)


def summarize_rate(successes: int, total: int, z: float = Z_95,
                   credibility: float = 0.95) -> RateSummary:
    """Point estimate plus Wilson and Jeffreys intervals for one proportion."""
    wlo, whi = wilson_interval(successes, total, z)
    jlo, jhi = jeffreys_interval(successes, total, credibility)
    return RateSummary(
        successes=successes,
        total=total,
        point=point_rate(successes, total),
        wilson_low=wlo,
        wilson_high=whi,
        jeffreys_low=jlo,
        jeffreys_high=jhi,
    )


# --- Sample size / power ---------------------------------------------------

def required_sample_size(margin: float, p: float = 0.5, z: float = Z_95) -> int:
    """Minimum n for a target 95% CI half-width: n = z^2 p(1-p) / d^2.

    The conservative default p = 0.5 maximizes p(1-p).
    """
    if margin <= 0.0:
        raise ValueError("margin must be positive")
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0, 1]")
    return math.ceil(z * z * p * (1.0 - p) / (margin * margin))


# --- Evidence grade and adjudication status -------------------------------

def validate_grade(grade: str) -> dict:
    """Validate an E0-E3 label and state whether it may support a conclusion."""
    key = grade.strip().upper()
    if key not in EVIDENCE_GRADES:
        raise ValueError(f"unknown evidence grade: {grade}")
    return {"grade": key, "meaning": EVIDENCE_GRADES[key],
            "supports_conclusion": key in ("E1", "E2")}


def adjudication_status(events: int, span_days: int,
                        min_events: int = MIN_EVENTS,
                        min_days: int = MIN_DAYS) -> str:
    """Three-way status. An instrument with no events is not yet instrumented;
    a running instrument below the data clock is underpowered; only a window
    meeting the clock supports an effect claim.
    """
    if events <= 0:
        return STATUS_NOT_INSTRUMENTED
    if events < min_events or span_days < min_days:
        return STATUS_UNDERPOWERED
    return STATUS_MEASURED


# --- Reliability rate summaries -------------------------------------------

def success_rate(successes: int, requests: int) -> RateSummary:
    """Success proportion over all attempts; count timeouts as the denominator."""
    return summarize_rate(successes, requests)


def block_rate(blocked: int, evaluations: int) -> RateSummary:
    """Block proportion. This is how often a gate fires, not a quality guarantee."""
    return summarize_rate(blocked, evaluations)


def self_recovery_rate(recovered: int, failed_threads: int) -> RateSummary:
    """Share of failed threads the agent recovered without human escalation."""
    return summarize_rate(recovered, failed_threads)


# --- Cost and cache constructs (three-model report section 3.1) ------------

def cache_token_hit_rate(cached_prompt_tokens: int, prompt_tokens: int) -> float:
    """h_c = cached_prompt_tokens / prompt_tokens."""
    if prompt_tokens <= 0:
        raise ValueError("prompt_tokens must be positive")
    return cached_prompt_tokens / prompt_tokens


def cache_request_hit_rate(cached_requests: int, requests: int) -> float:
    """h_r = cached_requests / requests."""
    if requests <= 0:
        raise ValueError("requests must be positive")
    return cached_requests / requests


def net_input_tokens(uncached_prompt_tokens: int,
                     cache_write_tokens: int) -> int:
    """N_in = uncached prompt tokens + cache write tokens (billed input)."""
    if uncached_prompt_tokens < 0 or cache_write_tokens < 0:
        raise ValueError("token counts must be non-negative")
    return uncached_prompt_tokens + cache_write_tokens


def token_savings(cached_prompt_tokens: int, cache_write_tokens: int) -> int:
    """S_t = max(cached read tokens - cache write tokens, 0)."""
    return max(cached_prompt_tokens - cache_write_tokens, 0)


def per_task_cost(total_cost: float, tasks: int) -> float:
    """C_t = total cost / tasks (the project currency, not assumed USD)."""
    if tasks <= 0:
        raise ValueError("tasks must be positive")
    return total_cost / tasks


# --- Demo on real paper figures -------------------------------------------

def _demo() -> dict:
    """Reproduce the real figures used in the papers (no fabricated numbers)."""
    gate = summarize_rate(37, 655)              # 5.65% block rate, 33-day window
    end_to_end = summarize_rate(127, 148)        # 85.8% incl. 21 timeout placeholders
    recovery = summarize_rate(69, 71)            # 97.2% self-recovery (n=71)
    return {
        "gate_block_37_of_655": gate.to_dict(),
        "end_to_end_success_127_of_148": end_to_end.to_dict(),
        "self_recovery_69_of_71": recovery.to_dict(),
        "sample_size_margin_0.05": required_sample_size(0.05),
        "sample_size_margin_0.03": required_sample_size(0.03),
        "adjudication_33d_655_events": adjudication_status(655, 33),
        "adjudication_4d_148_events": adjudication_status(148, 4),
        "example_cost_per_task": per_task_cost(3.70, 10),
    }


def _round_floats(obj, digits: int = 6):
    if isinstance(obj, float):
        return round(obj, digits)
    if isinstance(obj, dict):
        return {k: _round_floats(v, digits) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_round_floats(v, digits) for v in obj]
    return obj


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evidence metrics: paper formulas as executable functions.")
    parser.add_argument("--rate", nargs=2, type=int, metavar=("SUCCESSES", "TOTAL"),
                        help="Point estimate with Wilson and Jeffreys intervals.")
    parser.add_argument("--sample-size", type=float, metavar="MARGIN",
                        help="Required n for a 95% CI half-width (p=0.5).")
    parser.add_argument("--grade", help="Validate an E0-E3 evidence grade.")
    parser.add_argument("--status", nargs=2, type=int, metavar=("EVENTS", "DAYS"),
                        help="Adjudication status for a measurement window.")
    parser.add_argument("--demo", action="store_true",
                        help="Run the real paper figures as a worked example.")
    args = parser.parse_args()

    if args.demo:
        print(json.dumps(_round_floats(_demo()), ensure_ascii=False, indent=2))
        return 0
    if args.rate:
        summary = summarize_rate(args.rate[0], args.rate[1]).to_dict()
        print(json.dumps(_round_floats(summary), ensure_ascii=False, indent=2))
        return 0
    if args.sample_size is not None:
        print(json.dumps({"margin": args.sample_size,
                          "required_n": required_sample_size(args.sample_size)},
                         indent=2))
        return 0
    if args.grade:
        print(json.dumps(validate_grade(args.grade), ensure_ascii=False, indent=2))
        return 0
    if args.status:
        print(json.dumps({
            "events": args.status[0], "days": args.status[1],
            "status": adjudication_status(args.status[0], args.status[1])},
            indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
