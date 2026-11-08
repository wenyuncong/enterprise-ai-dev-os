---
name: ai-evidence-metrics
description: "Apply the evidence-gate measurement discipline as executable code: proportion point estimates with Wilson and Jeffreys intervals, sample-size/power, evidence grading E0-E3, data-clock adjudication, and cost/cache constructs. Use before reporting any rate, block percentage, success percentage, or cost figure so numbers have a denominator, intervals, and a clear claim boundary."
metadata:
  requires:
    bins: [python]
    scope: runtime
    declared-by: enterprise-ai-dev-os
---

## Rule

Every reported proportion or cost figure must be produced through the executable
measurement module, carry a denominator and an interval, and state its evidence
grade and adjudication status. Never report a bare point estimate or convert a
block rate into a quality guarantee.

# ai-evidence-metrics — Evidence Measurement (Skill-as-Code)

## Purpose

The methodology constitution requires fresh evidence and forbids unsupported
effect claims, but a rate written as prose has no denominator, no uncertainty
bound, and is easy to misread. This skill makes the measurement discipline of
AGENTS.md section 6B **directly executable**. The skill is not a separate prose
description: its operational implementation is versioned code.

**Executable implementation (single source of truth):**
`scripts/py/evidence_metrics.py` — Python standard library only, runs offline on
a fresh clone. Tests: `scripts/py/test_evidence_metrics.py`.

## Trigger

- Before reporting any block rate, success rate, failure rate, self-recovery
  rate, cache hit rate, or per-task cost.
- When reviewing whether a measurement window meets the data clock.
- When validating an E0-E3 evidence grade on a claim.

## Formula → Function Mapping (the formulas, coded)

| Paper formula | Function | Returns |
|---|---|---|
| Point estimate p = k/n | `point_rate(k, n)` | float |
| Wilson score interval | `wilson_interval(k, n)` | (low, high) |
| Jeffreys Beta(k+1/2, n-k+1/2) posterior | `jeffreys_interval(k, n)` | (low, high) |
| Point + both intervals at once | `summarize_rate(k, n)` | RateSummary |
| Sample size n = z² p(1-p)/d² | `required_sample_size(margin, p=0.5)` | int (ceil) |
| Evidence grade E0-E3 | `validate_grade(grade)` | grade + supports_conclusion |
| Data-clock adjudication | `adjudication_status(events, days)` | Measured / Underpowered / Not-instrumented |
| Cache token hit h_c = cached/prompt | `cache_token_hit_rate(...)` | float |
| Net input N_in = uncached + cache_write | `net_input_tokens(...)` | int |
| Token savings S_t = max(cached − write, 0) | `token_savings(...)` | int |
| Per-task cost C_t = cost/tasks | `per_task_cost(...)` | float |

The Jeffreys interval is computed from a real regularized incomplete Beta
function (`betainc`) and its inverse (`beta_ppf`), not a normal approximation.

## Mandatory Discipline

1. **Two intervals, mutually corroborating.** Proportion reports include both
   the Wilson (frequency) interval and the Jeffreys (Bayesian) interval.
2. **Data clock.** Effect claims require a continuous window of at least 28 days
   and at least 200 events; below that, the status is Underpowered and the figure
   is descriptive only. The independent analysis unit is the task, not individual
   in-session requests.
3. **A block rate is not a quality guarantee.** Without TP/FP resolution labels
   and CI events, precision, recall, and escape rate are not identifiable. The
   block rate only states how often the gate fired.
4. **Full-denominator rates.** Count timeouts and failures in the denominator.
   A 100% call-success figure that hides timeout placeholders is invalid.
5. **Fail closed on missing denominator.** An empty or invalid denominator
   raises, never silently returns zero.

## Usage

Command line:

```bash
python scripts/py/evidence_metrics.py --rate 37 655
python scripts/py/evidence_metrics.py --sample-size 0.05
python scripts/py/evidence_metrics.py --status 655 33
python scripts/py/evidence_metrics.py --demo
```

Import as a library:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts/py").resolve()))
import evidence_metrics as em

summary = em.summarize_rate(37, 655)      # point + Wilson + Jeffreys
n = em.required_sample_size(0.05)          # power-based sample size
```

## Anchored Real Figures (no fabricated numbers)

- 37 of 655 blocked: point 0.0565, Wilson [0.0413, 0.0769], Jeffreys
  [0.0407, 0.0762].
- 127 of 148 end-to-end success: 0.8581 (21 timeout placeholders included).
- 69 of 71 self-recovery: 0.9718.
- Sample size: margin 0.05 gives ceil 385 (paper: "about 384"); margin 0.03 gives
  ceil 1068 (paper: "about 1067").
