"""Conversion test design for the Singha Lemon Soda Cube (lemon): power, expected cell sizes, outcome simulation.

Track: men 25-34 (cell A) against men 35-44 (cell B); men 45-59 as a reference cell (cell C).
Outcome: top-2-box purchase intent on a 5-point scale (4 or 5), per person exposed to the concept.
Stimulus: plain description and concept image with no health claim and no sugar-free claim.

This script does not contact anyone, fetch any web page, or recruit. It only computes from
inputs already in the repo:
- rework/47_statistical_explanation.md (population counts, 2024 drinking shares, ratio A and B)
- rework/screen/segment_stat_results.json (simulated ratio A and ratio B summaries)
- DDC population CSV (male rows, summed by band; values match rework/47 section 6). The CSV sits in
  the session scratchpad, not in the repo; the summed band totals are copied in as constants below.

Assumptions (stated, not sourced):
- Top-2-box baseline for men 35-44 is unknown; a grid of 20, 30, 40, 50 percent is used.
- Two-sided alpha 0.05, power 0.80, two independent cells, no design effect, no continuity correction.
- Top-2-box intent scales with per-person potency, so the intent ratio equals ratio A or B.
  Ratio A depends only on the age gradient (drinking cells cancel), so the intent-to-potency link
  does not change ratio A if intent scales with sugar share alone.

Run: python conversion_test_power_sim.py -> writes conversion_test_power_sim_results.json
"""
import json
import math
import os
from statistics import NormalDist

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "conversion_test_power_sim_results.json")

SEED = 20261018
REPS = 20000
ALPHA = 0.05
POWER = 0.80
NORM = NormalDist()
Z_ALPHA2 = NORM.inv_cdf(1 - ALPHA / 2)  # two-sided, 1.960
Z_ALPHA1 = NORM.inv_cdf(1 - ALPHA)      # one-sided, 1.645 (used for the 90% interval of ratios)
Z_BETA = NORM.inv_cdf(POWER)            # 0.842

BASELINES = [0.20, 0.30, 0.40, 0.50]
DIFFS = [0.05, 0.10, 0.15]
MEANINGFUL_LEAD = 0.05  # the team's minimum difference of practical interest (proposed)

# Simulated ratio summaries from rework/screen/segment_stat_results.json (200,000 draws, seed 20261019).
RATIO_SUMMARY = {
    "A_25_34_over_35_44": {"median": 1.0408829387485201, "p05": 0.9979060344946077,
                           "p95": 1.0854925999254845, "P_gt_1_reported": 0.94113},
    "B_25_34_over_45_59": {"median": 1.1474370914494973, "p05": 1.0260110469248869,
                           "p95": 1.2836928062547666, "P_gt_1_reported": 0.97867},
}

# Population counts, men, by band (persons).
# DOPA Nov 2568 (registration; Thai year 2568 = calendar 2025), rework/47 section 6.
POP_DOPA = {"25-34": 4_760_000, "35-44": 4_750_000, "45-59": 6_650_000}
# DDC mid-year series, men, band sums re-computed from the downloaded CSV (2,618 rows, male rows).
# The CSV carries no year label, so its year cannot be confirmed from the file.
POP_DDC = {"25-34": 4_705_326, "35-44": 4_649_860, "45-59": 7_126_743}
POP_DDC_BANGKOK = {"25-34": 370_367, "35-44": 370_960, "45-59": 563_815}
# 2021 population counts by band: none in rework/47 or in the repo. Left as None on purpose.
POP_2021 = None

# Current drinking, men, 2024 (rework/47 section 2). 25-34 and 35-44 share one published cell (25-44).
DRINK_MEN = {"25-34": 0.686, "35-44": 0.686, "45-59": 0.654}
# Occasion pass-through (share of drinkers who qualify on the occasion screen). No source.
# Upper bound 1.0 is the sourced ceiling; 0.5 is an illustrative planning value only.
OCCASION_PASS = {"upper_bound_1.0": 1.0, "illustrative_0.5": 0.5}


def n_per_cell(p1, p2, z_a=Z_ALPHA2, z_b=Z_BETA):
    """Per-cell n for a two-sample comparison of proportions (Fleiss-type, no continuity correction)."""
    pbar = (p1 + p2) / 2.0
    num = z_a * math.sqrt(2.0 * pbar * (1.0 - pbar)) + z_b * math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))
    return int(math.ceil(num ** 2 / (p1 - p2) ** 2))


def lognormal_from_interval(median, p05, p95):
    """Fit log-normal parameters from a median and a 90% interval; average the two tail estimates."""
    mu = math.log(median)
    sd_lo = (mu - math.log(p05)) / Z_ALPHA1
    sd_hi = (math.log(p95) - mu) / Z_ALPHA1
    return mu, (sd_lo + sd_hi) / 2.0, sd_lo, sd_hi


def power_table():
    rows = []
    for p0 in BASELINES:
        for d in DIFFS:
            p1 = p0 + d
            rows.append({
                "baseline_35_44": p0,
                "p_25_34": round(p1, 4),
                "difference_pp": int(round(d * 100)),
                "n_per_cell_two_sided_alpha05_power80": n_per_cell(p1, p0),
                "n_per_cell_one_sided_alpha05_power80": n_per_cell(p1, p0, z_a=Z_ALPHA1),
            })
    return rows


def ratio_effect_table(ratio_medians):
    rows = []
    for p0 in BASELINES:
        entry = {"baseline_35_44": p0}
        for name, med in ratio_medians.items():
            p1 = min(p0 * med, 0.999)
            d = p1 - p0
            entry[f"{name}_difference_pp"] = round(d * 100, 2)
            entry[f"{name}_n_per_cell_for_80pct_power"] = n_per_cell(p1, p0)
        rows.append(entry)
    return rows


def expected_cell_sizes():
    out = {}
    for band in ("25-34", "35-44", "45-59"):
        drink = DRINK_MEN[band]
        row = {
            "men_population_DOPA_Nov2568": POP_DOPA[band],
            "men_population_DDC_midyear": POP_DDC[band],
            "men_population_2021": POP_2021,
            "current_drinking_share_2024_men": drink,
            "drinkers_DOPA": round(POP_DOPA[band] * drink),
            "drinkers_DDC": round(POP_DDC[band] * drink),
            "drinkers_Bangkok_DDC": round(POP_DDC_BANGKOK[band] * drink),
        }
        out[band] = row
    return out


def screened_per_cell(n, q):
    """Screened persons needed for n completes in one cell, given drinker share and occasion pass q."""
    return int(math.ceil(n / (DRINK_MEN["25-34"] * q)))


def simulate_ratio(p0, n, ratio_key, ratio_params, reps=REPS, seed=SEED):
    """Outcome frequencies for two cells of size n each, with ratio drawn from its log-normal."""
    rng = np.random.default_rng(seed)
    if ratio_key is None:
        R = np.ones(reps)
    else:
        mu, sd = ratio_params
        R = np.exp(rng.normal(mu, sd, reps))
    p1 = np.clip(p0 * R, 1e-6, 1 - 1e-6)
    return _two_cell_outcomes(rng, p0, p1, n, reps)


def simulate_fixed(p0, p1, n, reps=REPS, seed=SEED):
    rng = np.random.default_rng(seed)
    p1v = np.full(reps, p1)
    return _two_cell_outcomes(rng, p0, p1v, n, reps)


def _two_cell_outcomes(rng, p0, p1, n, reps):
    x0 = rng.binomial(n, p0, reps)
    x1 = rng.binomial(n, p1, reps)
    h0 = x0 / n
    h1 = x1 / n
    pp = (x0 + x1) / (2.0 * n)
    se_pool = np.sqrt(np.maximum(pp * (1 - pp) * 2.0 / n, 1e-300))
    z = (h1 - h0) / se_pool
    diff = h1 - h0
    se_unp = np.sqrt(np.maximum(h1 * (1 - h1) / n + h0 * (1 - h0) / n, 1e-300))
    upper = diff + Z_ALPHA2 * se_unp
    confirm = float(np.mean(z > Z_ALPHA2))
    reverse = float(np.mean(z < -Z_ALPHA2))
    return {
        "confirm_lead_25_34_higher_significant": round(confirm, 4),
        "reverse_35_44_higher_significant": round(reverse, 4),
        "inconclusive": round(1.0 - confirm - reverse, 4),
        "rules_out_5pp_or_more_lead_upper_95_below_5pp": round(float(np.mean(upper < MEANINGFUL_LEAD)), 4),
        "median_observed_difference_pp": round(float(np.median(diff)) * 100, 2),
    }


def simulation_block():
    ratio_params = {k: lognormal_from_interval(v["median"], v["p05"], v["p95"])
                    for k, v in RATIO_SUMMARY.items()}
    blocks = []
    for p0 in BASELINES:
        n_by_diff = {f"n_for_{int(d * 100)}pp": n_per_cell(p0 + d, p0) for d in DIFFS}
        scen = {"baseline_35_44": p0, "cell_sizes": n_by_diff, "runs": []}
        # Power check: fixed 5 pp difference at the 5 pp cell size should give about 0.80 confirm.
        chk = simulate_fixed(p0, p0 + 0.05, n_by_diff["n_for_5pp"])
        scen["power_check_fixed_5pp_at_n_for_5pp"] = chk["confirm_lead_25_34_higher_significant"]
        for label, n in n_by_diff.items():
            for ratio_name in ("null_ratio_1", "A_25_34_over_35_44", "B_25_34_over_45_59"):
                key = None if ratio_name == "null_ratio_1" else ratio_name
                params = None if key is None else ratio_params[key][:2]
                res = simulate_ratio(p0, n, key, params)
                scen["runs"].append({"cell_size_label": label, "n_per_cell": n, "ratio": ratio_name, **res})
        # The n that gives 80 percent power for ratio A itself, and its simulated check.
        p1A = min(p0 * RATIO_SUMMARY["A_25_34_over_35_44"]["median"], 0.999)
        nA = n_per_cell(p1A, p0)
        resA = simulate_ratio(p0, nA, "A_25_34_over_35_44", ratio_params["A_25_34_over_35_44"][:2])
        scen["n_for_ratio_A_median_80pct_power"] = nA
        scen["runs_at_n_for_ratio_A"] = {"n_per_cell": nA, "ratio": "A_25_34_over_35_44", **resA}
        blocks.append(scen)
    return blocks, {k: {"mu": v[0], "sd": v[1], "sd_low_tail": v[2], "sd_high_tail": v[3]}
                    for k, v in ratio_params.items()}


def main():
    pw = power_table()
    ratio_medians = {k: v["median"] for k, v in RATIO_SUMMARY.items()}
    ratio_eff = ratio_effect_table(ratio_medians)
    cells = expected_cell_sizes()
    sims, fitted = simulation_block()

    cell_screening = {}
    for label, n in (("n_5pp_at_30pct", n_per_cell(0.35, 0.30)), ("n_10pp_at_30pct", n_per_cell(0.40, 0.30)),
                     ("n_15pp_at_30pct", n_per_cell(0.45, 0.30))):
        cell_screening[label] = {
            "completes_per_cell": n,
            "screened_persons_per_cell_occasion_upper_bound": screened_per_cell(n, OCCASION_PASS["upper_bound_1.0"]),
            "screened_persons_per_cell_illustrative_occasion_0.5": screened_per_cell(n, OCCASION_PASS["illustrative_0.5"]),
        }

    result = {
        "seed": SEED,
        "reps_per_simulation": REPS,
        "alpha_two_sided": ALPHA,
        "power_target": POWER,
        "z_alpha_two_sided": round(Z_ALPHA2, 4),
        "z_beta": round(Z_BETA, 4),
        "formula": "n per cell = [z_a*sqrt(2*pbar*qbar) + z_b*sqrt(p1*q1 + p2*q2)]^2 / (p1-p2)^2, no continuity correction",
        "power_table": pw,
        "ratio_effect_table": ratio_eff,
        "expected_cell_sizes_men": cells,
        "expected_cell_sizes_2021": "not available: no 2021 population count by band is in rework/47 or the repo",
        "screening_yield_for_completes": cell_screening,
        "ratio_inputs": RATIO_SUMMARY,
        "ratio_lognormal_fit": fitted,
        "simulation_by_baseline": sims,
        "assumptions": [
            "Baseline top-2-box for men 35-44 is not in any source; grid 20, 30, 40, 50 percent.",
            "Top-2-box intent scales with per-person potency, so intent ratio = ratio A or B (model link, unevidenced).",
            "Ratio A and B are log-normal, fitted to the median and 90% interval in rework/47 section 1.",
            "Ratio A uses only the age gradient (drinking cells cancel); its interval includes 1.0 at the OR CI.",
            "No design effect, no panel non-response, no continuity correction in the sample sizes.",
            "Drinking share for 25-34 and 35-44 is the shared 25-44 published cell (68.6%).",
            "Occasion pass-through is unknown; upper bound 1.0 and an illustrative 0.5 are shown.",
        ],
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    print("wrote", OUT_JSON)
    print("Power table (n per cell, two-sided alpha 0.05, power 0.80):")
    for r in pw:
        print(f"  baseline {r['baseline_35_44']:.2f}  diff {r['difference_pp']:>2} pp  n = {r['n_per_cell_two_sided_alpha05_power80']}")
    print("Ratio effect at median:")
    for r in ratio_eff:
        print(f"  baseline {r['baseline_35_44']:.2f}  A {r['A_25_34_over_35_44_difference_pp']} pp (n {r['A_25_34_over_35_44_n_per_cell_for_80pct_power']})  "
              f"B {r['B_25_34_over_45_59_difference_pp']} pp (n {r['B_25_34_over_45_59_n_per_cell_for_80pct_power']})")
    print("Simulation, ratio A, confirm / reverse / rules-out-5pp:")
    for blk in sims:
        for run in blk["runs"]:
            if run["ratio"] == "A_25_34_over_35_44":
                print(f"  baseline {blk['baseline_35_44']:.2f}  {run['cell_size_label']:>15} n={run['n_per_cell']:>6}  "
                      f"confirm {run['confirm_lead_25_34_higher_significant']:.3f}  reverse {run['reverse_35_44_higher_significant']:.3f}  "
                      f"rules_out_5pp {run['rules_out_5pp_or_more_lead_upper_95_below_5pp']:.3f}")
        ra = blk["runs_at_n_for_ratio_A"]
        print(f"  baseline {blk['baseline_35_44']:.2f}  n for ratio A (80% power) = {ra['n_per_cell']}  confirm {ra['confirm_lead_25_34_higher_significant']:.3f}")


if __name__ == "__main__":
    main()
