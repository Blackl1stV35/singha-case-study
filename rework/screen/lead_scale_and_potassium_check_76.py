"""Check of two figures in record 76 (second pass, 20 October 2026).

No random draw and no seed: every value is a closed-form calculation, so the run is repeatable.

1. Potassium per serve. The design mass of potassium bicarbonate (KHCO3) is 0.81 g per serve
   (submissions 05 and 09). The potassium mass is 0.81 g times the potassium share of KHCO3.
   The atomic weights typed below are standard values; they are not read from a saved source
   (a stated limit in the record). The script also reports the bicarbonate mass that would be
   needed for the 317 mg figure used in the submissions.

2. Lead size at a 30 percent baseline (cell B), for the ratios of submission 12:
   ratio A (men 25 to 34 over men 35 to 44): median 1.04, 90 percent interval 1.00 to 1.09;
   ratio B (men 25 to 34 over men 45 to 59): median 1.15, 90 percent interval 1.03 to 1.28.
   Two readings are computed:
   - share scale: the ratio multiplies the share (the reading used by the simulation in submission 12,
     where a cell A person is top-2-box with probability p times R);
   - odds scale: the ratio is an odds ratio (the reading that submission 01's model uses).
   The lead is reported in percentage points.

Run: python rework/screen/lead_scale_and_potassium_check_76.py   (well under 50 MB of memory)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

ATOMIC_WEIGHT = {"K": 39.098, "H": 1.008, "C": 12.011, "O": 15.999}
KHCO3_MOLAR_MASS = ATOMIC_WEIGHT["K"] + ATOMIC_WEIGHT["H"] + ATOMIC_WEIGHT["C"] + 3 * ATOMIC_WEIGHT["O"]
K_FRACTION = ATOMIC_WEIGHT["K"] / KHCO3_MOLAR_MASS
RECORD_K_FRACTION = 39.10 / 100.12  # the rounded values used in the record's hand calculation

BICARB_G_PER_SERVE = 0.81
SUBMISSION_K_MG = 317.0

BASELINE = 0.30  # cell B share, as in submission 12


def potassium():
    k_mg_exact = BICARB_G_PER_SERVE * K_FRACTION * 1000.0
    k_mg_record = BICARB_G_PER_SERVE * RECORD_K_FRACTION * 1000.0
    bicarb_needed_for_317 = SUBMISSION_K_MG / (K_FRACTION * 1000.0)
    return {
        "khco3_molar_mass_g_per_mol": round(KHCO3_MOLAR_MASS, 3),
        "potassium_mass_fraction_exact": round(K_FRACTION, 5),
        "potassium_mass_fraction_record_rounding": round(RECORD_K_FRACTION, 5),
        "bicarbonate_g_per_serve": BICARB_G_PER_SERVE,
        "potassium_mg_per_serve_exact_weights": round(k_mg_exact, 1),
        "potassium_mg_per_serve_record_rounding": round(k_mg_record, 1),
        "bicarbonate_g_needed_for_317_mg": round(bicarb_needed_for_317, 4),
        "submission_figure_mg": SUBMISSION_K_MG,
        "note": "The submissions state 317 mg. From 0.81 g the script gives about 316 mg. "
                "317 mg needs about 0.812 g of bicarbonate. The team must choose one figure.",
    }


def share_lead_points(ratio, base=BASELINE):
    return (base * ratio - base) * 100.0


def odds_p(ratio, base=BASELINE):
    odds = base / (1.0 - base) * ratio
    return odds / (1.0 + odds)


def odds_lead_points(ratio, base=BASELINE):
    return (odds_p(ratio, base) - base) * 100.0


def ratio_for_odds_lead(target_points, base=BASELINE):
    # Bisection on the odds-scale lead; the lead rises with the ratio.
    lo, hi = 1.0, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if odds_lead_points(mid, base) < target_points:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def ratio_for_share_lead(target_points, base=BASELINE):
    return 1.0 + target_points / 100.0 / base


def lead_table():
    out = {}
    cases = {
        "ratio_A_men25_34_over_35_44": [("lower_bound", 1.00), ("median", 1.04), ("upper_bound", 1.09)],
        "ratio_B_men25_34_over_45_59": [("lower_bound", 1.03), ("median", 1.15), ("upper_bound", 1.28)],
    }
    for name, rows in cases.items():
        out[name] = []
        for label, r in rows:
            out[name].append({
                "bound": label,
                "ratio": r,
                "share_scale_lead_points": round(share_lead_points(r), 2),
                "odds_scale_lead_points": round(odds_lead_points(r), 2),
            })
    return out


def reverse_checks():
    # Which ratio would give the leads quoted in submission 01 (earlier model) on each scale?
    return {
        "submission_01_odds_scale_0_6_points_needs_ratio": round(ratio_for_odds_lead(0.6), 4),
        "submission_01_share_scale_0_9_points_needs_ratio": round(ratio_for_share_lead(0.9), 4),
        "submission_12_share_scale_1_23_points_needs_ratio": round(ratio_for_share_lead(1.23), 4),
    }


def main():
    pk = potassium()
    leads = lead_table()
    rev = reverse_checks()
    results = {
        "check": "Lead scale and potassium per serve, record 76 (second pass)",
        "date": "2026-10-20",
        "seed": "none (closed-form arithmetic, no random draw)",
        "baseline_share": BASELINE,
        "potassium": pk,
        "lead_by_ratio_and_scale": leads,
        "reverse_checks_ratio_needed": rev,
        "reading": {
            "record_lead_point_estimate": "1.2 points on the share scale at the median ratio 1.04 (submission 12 quotes 1.23 from its simulation, not reproduced exactly here)",
            "odds_scale_at_median": leads["ratio_A_men25_34_over_35_44"][1]["odds_scale_lead_points"],
            "share_scale_at_median": leads["ratio_A_men25_34_over_35_44"][1]["share_scale_lead_points"],
            "ratio_B_share_scale_at_median": leads["ratio_B_men25_34_over_45_59"][1]["share_scale_lead_points"],
            "submission_12_ratio_B_quoted_points": 4.4,
            "conflict": "Submission 01 gives 0.6 points (odds scale) and 0.9 points (share scale) with 1.2 from the power simulation; submission 12 gives 1.23 on the share scale. The two submissions use different model versions.",
        },
    }
    out_json = os.path.join(HERE, "lead_scale_and_potassium_check_76_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("potassium:", {k: pk[k] for k in ("khco3_molar_mass_g_per_mol", "potassium_mg_per_serve_exact_weights",
                                              "potassium_mg_per_serve_record_rounding", "bicarbonate_g_needed_for_317_mg")})
    for name, rows in leads.items():
        for row in rows:
            print(name, row)
    print("reverse checks:", rev)


if __name__ == "__main__":
    main()
