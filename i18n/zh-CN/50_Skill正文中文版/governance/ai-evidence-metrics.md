# `ai-evidence-metrics` — 证据度量（Skill 即代码）

> **源文件**：skills/governance/ai-evidence-metrics/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-11-08
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、公式与函数名原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-evidence-metrics
description: "Apply the evidence-gate measurement discipline as executable code: proportion point estimates with Wilson and Jeffreys intervals, sample-size/power, evidence grading E0-E3, data-clock adjudication, and cost/cache constructs. Use before reporting any rate, block percentage, success percentage, or cost figure so numbers have a denominator, intervals, and a clear claim boundary."
```

**中文描述**：把证据门测量纪律做成可执行代码——比例点估计并附 Wilson 与 Jeffreys 区间、样本量/功效、证据分级 E0–E3、数据时钟裁决，以及成本/缓存构造。在报告任何比率、阻断百分比、成功率或成本数字之前使用，确保数字带分母、带区间、带清晰的主张边界。

---

## Rule | 规则

每个被报告的比例或成本数字都必须通过可执行度量模块产出，带分母和区间，并声明其证据分级与裁决状态。绝不报告裸点估计，也不把阻断率当成质量保证。

---

## Purpose | 目标

方法论宪法要求新鲜证据并禁止无支撑的效果主张，但用 prose 写的比率没有分母、没有不确定边界，且容易被误读。本 Skill 让 AGENTS.md 6B 的测量纪律**可直接执行**。本 Skill 不是独立的文字描述：它的可运行实现是版本化代码。

**可执行实现（唯一真相源）**：`scripts/py/evidence_metrics.py`——仅用 Python 标准库，全新克隆可离线运行。测试：`scripts/py/test_evidence_metrics.py`。

---

## Trigger | 触发条件

- 报告任何阻断率、成功率、失败率、自恢复率、缓存命中率或单任务成本之前。
- 评审某个测量窗口是否满足数据时钟时。
- 校验某条主张的 E0–E3 证据分级时。

---

## Formula → Function Mapping | 公式到函数的映射（公式已代码化）

| 论文公式 | 函数 | 返回 |
|---|---|---|
| 点估计 p = k/n | `point_rate(k, n)` | float |
| Wilson score 区间 | `wilson_interval(k, n)` | (low, high) |
| Jeffreys Beta(k+1/2, n-k+1/2) 后验 | `jeffreys_interval(k, n)` | (low, high) |
| 点估计 + 两套区间一次给出 | `summarize_rate(k, n)` | RateSummary |
| 样本量 n = z² p(1-p)/d² | `required_sample_size(margin, p=0.5)` | int（向上取整） |
| 证据分级 E0–E3 | `validate_grade(grade)` | 分级 + supports_conclusion |
| 数据时钟裁决 | `adjudication_status(events, days)` | Measured / Underpowered / Not-instrumented |
| 缓存 token 命中 h_c = cached/prompt | `cache_token_hit_rate(...)` | float |
| 净输入 N_in = uncached + cache_write | `net_input_tokens(...)` | int |
| token 节省 S_t = max(cached − write, 0) | `token_savings(...)` | int |
| 单任务成本 C_t = cost/tasks | `per_task_cost(...)` | float |

Jeffreys 区间由真实的正则化不完全 Beta 函数（`betainc`）及其反函数（`beta_ppf`）计算，不是正态近似。

---

## Mandatory Discipline | 强制纪律

1. **两套区间，相互印证。** 比例报告同时包含 Wilson（频率派）区间与 Jeffreys（贝叶斯）区间。
2. **数据时钟。** 效果主张需要连续至少 28 天且至少 200 事件的窗口；低于此，状态为 Underpowered，数字仅作描述。独立分析单位是 task，不是会话内的单个请求。
3. **阻断率不是质量保证。** 没有 TP/FP 的 resolution 标签和 CI 事件，精确率、召回率、逃逸率不可识别。阻断率只说明门触发的频率。
4. **全分母比率。** 把超时和失败计入分母。隐藏超时占位的 100% 调用成功率无效。
5. **分母缺失 fail-closed。** 空或非法的分母会抛错，绝不静默返回零。

---

## Usage | 用法

命令行：

```bash
python scripts/py/evidence_metrics.py --rate 37 655
python scripts/py/evidence_metrics.py --sample-size 0.05
python scripts/py/evidence_metrics.py --status 655 33
python scripts/py/evidence_metrics.py --demo
```

作为库导入：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts/py").resolve()))
import evidence_metrics as em

summary = em.summarize_rate(37, 655)      # 点估计 + Wilson + Jeffreys
n = em.required_sample_size(0.05)          # 基于功效的样本量
```

---

## Anchored Real Figures | 锚定真实数字（无虚构）

- 655 中阻断 37：点 0.0565，Wilson [0.0413, 0.0769]，Jeffreys [0.0407, 0.0762]。
- 148 中端到端成功 127：0.8581（含 21 个超时占位）。
- 71 中自恢复 69：0.9718。
- 样本量：半宽 0.05 向上取整为 385（论文："约 384"）；半宽 0.03 向上取整为 1068（论文："约 1067"）。

---

## 译注

- 函数名、常量（`Measured` / `Underpowered` / `Not-instrumented`）、证据分级代号 `E0–E3`、四性质与不变量代号一律保持英文原样。
- 样本量差异已在源文件与测试中说明：论文用取整的 z=1.96 报告"约 384/1067"，代码用精确 z 值并向上取整为 385/1068，以保证实际半宽不超过目标。
- 所有期望值均锚定论文与三模型报告的真实数字，未引入任何虚构效果。
