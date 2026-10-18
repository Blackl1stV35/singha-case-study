"""Conversion test on a synthesis basis (no respondents, no outside contact).

The test is a model-based comparison: men aged 25 to 34 (lead cell) against men aged 35 to 44
(comparison cell), and against men aged 45 to 59 as a reference. It uses only the published
inputs already in the repo (rework/47) and states every assumption that no source provides.

Per-person potency for a band b:  P_b = d_b * s0 * OR^(mid_b - 40)
  d_b   current drinking share (NSO 2024, sex-specific cell); 25-34 and 35-44 share one cell
  s0    daily sugar-sweetened share at age 40 (cancels in every ratio used here)
  OR    odds ratio per year of age for daily consumption (2021 survey)

Synthesised purchase intent in the comparison cell is taken as a stated baseline B (top-2-box,
percent; no source gives it, so a grid is used). For cell b:
  intent_b = B * (P_b / P_35-44) ^ e
  e         the intent-to-potency link (ELASTICITY): an ASSUMPTION, uniform 0.5 to 1.0.
            e = 0 would mean no link at all, and then no test result is possible.

Point difference, lead minus comparison, in percentage points:
  diff_A = B * ((OR^-10)^e - 1)                  (drinking cell shared, so it cancels)
  diff_C = B * ((d25/d45 * OR^-22.5)^e - 1)      (reference only; volume item, pended)

Uncertainty: OR log-normal from the published 95% interval (0.991 to 1.001); drinking shares
+/- 3 points (no 2024 interval published); elasticity e uniform 0.5 to 1.0.

Decision rules, fixed before the run (rework/49):
  direction: "lead supported" if P(diff_A > 0) >= 0.90; "lead not supported" if P(diff_A < 0) >= 0.90;
             otherwise "direction undetermined"
  size:      "5-point lead supported" if P(diff_A >= 5) >= 0.90, otherwise "5-point lead not supported"

The probabilities are model probabilities under the stated assumptions, not sampling probabilities.
Nothing here is a consumer finding.

Writes rework/screen/conversion_synthesis_results.json and prints a summary.
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "conversion_synthesis_results.json")
STAT_JSON = os.path.join(HERE, "segment_stat_results.json")

SEED = 20261018
N = 200000

OR_LO, OR_HI, OR_MID = 0.991, 1.001, 0.996
LOG_OR_MEAN = math.log(OR_MID)
LOG_OR_SD = (math.log(OR_HI) - math.log(OR_LO)) / (2 * 1.96)

D25, D45, DRINK_PM = 68.6, 65.4, 3.0   # NSO 2024 men 25-44 and 45-59 cells, +/- 3 points
ELAST_LO, ELAST_HI = 0.5, 1.0          # intent-to-potency link, ASSUMPTION
BASELINES = [20.0, 30.0, 40.0, 50.0]   # comparison-cell top-2-box, percent, NO source (grid)
MATERIAL_PTS = 5.0                     # the design size from rework/screen/conversion_test_design.md
DIRECTION_P = 0.90

rng = np.random.default_rng(SEED)


def draws():
    or_ = np.exp(rng.normal(LOG_OR_MEAN, LOG_OR_SD, N))
    d25 = rng.uniform(D25 - DRINK_PM, D25 + DRINK_PM, N)
    d45 = rng.uniform(D45 - DRINK_PM, D45 + DRINK_PM, N)
    e = rng.uniform(ELAST_LO, ELAST_HI, N)
    return or_, d25, d45, e


def summarise(x):
    return {
        "median": round(float(np.median(x)), 4),
        "p05": round(float(np.percentile(x, 5)), 4),
        "p95": round(float(np.percentile(x, 95)), 4),
    }


def direction_label(p_pos, p_neg):
    if p_pos >= DIRECTION_P:
        return "lead supported"
    if p_neg >= DIRECTION_P:
        return "lead not supported"
    return "direction undetermined"


def main():
    or_, d25, d45, e = draws()

    # Ratio A: men 25-34 over men 35-44. The drinking cell is shared, so d25 cancels.
    ratio_a_pot = or_ ** (-10.0)          # P25 / P35 before the elasticity
    ratio_c_pot = (d25 / d45) * or_ ** (-22.5)  # P25 / P45 before the elasticity

    # Consistency check against the earlier Monte Carlo (rework/47, ratio A median 1.04)
    ratio_a_median_pot = float(np.median(ratio_a_pot))
    with open(STAT_JSON, encoding="utf-8") as fh:
        stat = json.load(fh)
    stat_median = stat.get("ratio_A_median")
    consistent = stat_median is None or abs(ratio_a_median_pot - stat_median) < 0.01

    by_baseline = {}
    for b in BASELINES:
        odds = b / (100.0 - b)
        ra = ratio_a_pot ** e
        rc = ratio_c_pot ** e
        # Share scale: the ratio multiplies the share.
        diff_a = b * (ra - 1.0)
        diff_c = b * (rc - 1.0)
        # Odds scale: the ratio multiplies the odds, the usual reading of an odds ratio.
        odds_a = 100.0 * (odds * ra) / (1.0 + odds * ra) - b
        scales = {}
        for name, x in (("share_scale", diff_a), ("odds_scale", odds_a)):
            p_pos = float(np.mean(x > 0))
            p_neg = float(np.mean(x < 0))
            p_mat = float(np.mean(x >= MATERIAL_PTS))
            scales[name] = {
                "diff_25_34_minus_35_44_pts": summarise(x),
                "P_diff_gt_0": round(p_pos, 4),
                "P_diff_lt_0": round(p_neg, 4),
                "P_diff_ge_5": round(p_mat, 4),
                "direction": direction_label(p_pos, p_neg),
                "size": "5-point lead supported" if p_mat >= DIRECTION_P else "5-point lead not supported",
            }
        by_baseline[f"{int(b)}"] = {
            "comparison_cell_top2_box_pct": b,
            **scales,
            "diff_25_34_minus_45_59_pts_reference_share_scale": summarise(diff_c),
        }

    result = {
        "basis": "synthesis (model-based); no respondents; no outside contact",
        "seed": SEED,
        "draws": N,
        "inputs": {
            "OR_per_year_mid": OR_MID,
            "OR_per_year_interval_95": [OR_LO, OR_HI],
            "drinking_25_44_pct": D25,
            "drinking_45_59_pct": D45,
            "drinking_uncertainty_pts": DRINK_PM,
            "elasticity_range": [ELAST_LO, ELAST_HI],
            "baselines_pct": BASELINES,
            "material_size_pts": MATERIAL_PTS,
            "direction_probability_threshold": DIRECTION_P,
        },
        "ratio_A_potency_median": round(ratio_a_median_pot, 4),
        "consistent_with_rework_47": consistent,
        "results_by_baseline": by_baseline,
        "assumptions": [
            "Intent-to-potency link: intent proportional to potency^e, e uniform 0.5 to 1.0. No source. e = 0 would make the test empty.",
            "Comparison-cell top-2-box baseline: no source; grid 20, 30, 40, 50 percent.",
            "Age gradient applied to mid-ages 29.5, 39.5 and 52.0, from the 2021 survey (per-year OR, sampling error only).",
            "Drinking cell shared by 25-34 and 35-44 (NSO publishes 25-44 only).",
            "Sugar base cancels in all ratios.",
        ],
    }

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    print("wrote", OUT_JSON)
    print(f"ratio A (potency, before elasticity) median = {ratio_a_median_pot:.4f}; consistent with rework/47: {consistent}")
    for key, row in by_baseline.items():
        for name in ("share_scale", "odds_scale"):
            s = row[name]
            d = s["diff_25_34_minus_35_44_pts"]
            print(f"{row['comparison_cell_top2_box_pct']:>4.0f}% {name:<11} median {d['median']:>5.2f}  "
                  f"90% [{d['p05']:>6.2f}, {d['p95']:>6.2f}]  P>0 {s['P_diff_gt_0']:.3f}  P>=5 {s['P_diff_ge_5']:.3f}  "
                  f"{s['direction']} / {s['size']}")


if __name__ == "__main__":
    main()
