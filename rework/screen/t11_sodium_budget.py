"""T11 sodium budget for the Singha Lemon Soda Cube (one cube in 330 mL). Revised twice on 20 October 2026 after verifier findings.

Deterministic arithmetic only. No random draws, so no seed is used (fixed seed 20261020 recorded for the record).
Inputs are tiered in the results JSON:
  P          regulator text, monograph or maker specification read (the value is printed in the source)
  DERIVED    our arithmetic on a P input (a bound, not a measurement)
  ASSUMPTION planning value, not sourced
  S          secondary or a different grade of the same maker (indicator only)
  UNVERIFIED not read

Change from the first version: the sodium high case now uses a bound derived from the JECFA sulfated-ash limit where one
was read (citric acid, sucralose, mannitol, isomalt), and a planning value (ASSUMPTION) only where no limit was read
(potassium bicarbonate food grade, lemon flavour with carrier). Water is shown both counted and not counted, on three
claim bases: Case 1 at 330 mL consumed, Case 1 at two-fold reference serving (400 mL made up), and Case 2 per 100 mL.

Second revision adds: both water ceilings (consumed-serving basis and two-fold reference basis) for every claim; a water sensitivity table
(WHO typical, the Thai Department of Health figure reported in the press, and the WHO taste threshold); Case 2 shown as a hypothetical only; a
binder price spread by origin from the saved Comtrade rows; a formula mass check (no lubricant in the 3.79 g cube); a contingent PEG lubricant line
(JECFA sulfated ash 0.1 percent, Thai 468 level); and a check of the cube against the Thai electrolyte drink standard (Notification 195, B.E. 2543).

Run:  python -I rework/screen/t11_sodium_budget.py
Writes: rework/screen/t11_sodium_results.json
"""
import json
import os

SEED = 20261020  # recorded for the record; no random numbers are drawn
SERVE_ML = 330.0          # declared consumed serving (cube made up to 330 mL)
RS_ML = 200.0             # Notification 445 Annex 2, category 2 No. 3: "defined amount for preparing the beverage of 200 milliliters"
TWOFOLD_RS_ML = 2 * RS_ML  # Annex 4, clause 2.1 Case 1 (2): two-fold reference serving if the reference amount is not more than 30 g

# Mass of sodium per mass of Na2SO4 (sulphated ash is weighed as sulphates). Na 22.98977, Na2SO4 142.04214.
NA_IN_NA2SO4 = 2 * 22.98977 / 142.04214

# Molar masses for the potassium line (standard atomic weights): K 39.0983, KHCO3 100.1151.
K_IN_KHCO3 = 39.0983 / 100.1151


def ash_bound(ash_pct):
    """Sodium weight fraction if all sulphated ash (given in percent) were sodium sulphate (upper bound)."""
    return ash_pct / 100.0 * NA_IN_NA2SO4


# Components per serve (grams). Masses from the repo submission set; the primary binder is mannitol, the fallback isomalt.
components = [
    {
        "name": "Potassium bicarbonate (INS 501(ii)), food grade", "mass_g": 0.81, "mass_tier": "DERIVED (stoichiometry, repo basis B)",
        "na_low_frac": 0.0, "na_high_frac": 0.001, "na_high_tier": "ASSUMPTION",
        "na_basis": "Maker food-grade sales specification (Armand Products, rev. 05/22, read 20 Oct 2026) lists no sodium limit. "
                    "Planning high case 0.1 wt% Na. Indicator only (S, different grade): the same maker's ACS-grade sheet limits Na to 0.03 wt% max.",
        "indicator_frac": 0.0003, "indicator_note": "S: Armand ACS-grade sheet, Na 0.03 wt% max (higher grade than food grade; sheet undated)",
    },
    {
        "name": "Citric acid (INS 330)", "mass_g": 2.10, "mass_tier": "DERIVED (repo basis B)",
        "na_low_frac": 0.0, "na_high_frac": ash_bound(0.05), "na_high_tier": "DERIVED from P",
        "na_basis": "FAO JECFA Monographs 16 (2014): sulfated ash not more than 0.05%. No sodium limit in the monograph text. "
                    "Bound assumes all residue is sodium sulphate.",
    },
    {
        "name": "Sucralose (INS 955)", "mass_g": 0.033, "mass_tier": "ASSUMPTION (about 33 mg, repo design)",
        "na_low_frac": 0.0, "na_high_frac": ash_bound(0.7), "na_high_tier": "DERIVED from P",
        "na_basis": "FAO JECFA Monograph (prepared 41st JECFA 1993, metals revised 63rd JECFA 2004), Additive 444: sulfated ash not more than 0.7%. "
                    "Bound assumes all residue is sodium sulphate.",
    },
    {
        "name": "Lemon flavour (incl. carrier)", "mass_g": 0.05, "mass_tier": "ASSUMPTION",
        "na_low_frac": 0.0, "na_high_frac": 0.01, "na_high_tier": "ASSUMPTION",
        "na_basis": "No flavour or carrier specification read (UNVERIFIED). 1 wt% planning value only.",
    },
    {
        "name": "Binder and filler: mannitol, tableting grade (INS 421), primary", "mass_g": 0.80, "mass_tier": "ASSUMPTION (0.80 g, repo design)",
        "na_low_frac": 0.0, "na_high_frac": ash_bound(0.1), "na_high_tier": "DERIVED from P",
        "na_basis": "FAO JECFA Monographs 1, Additive 275 (46th JECFA 1996; metals revised 2001): sulfated ash not more than 0.1%, chlorides not more than 70 mg/kg. "
                    "Bound assumes all residue is sodium sulphate. A supplier tableting-grade sheet was not read.",
    },
    {
        "name": "Pouch film (migration to the cube during shelf life)", "mass_g": 0.0, "mass_tier": "ASSUMPTION (no sodium-bearing layer assumed; migration not tested)",
        "na_low_frac": 0.0, "na_high_frac": 0.0, "na_high_tier": "ASSUMPTION",
        "na_basis": "Film specification not supplied. No sodium-bearing layer assumed (ASSUMPTION), so the line is set to 0. The cube touches the film during shelf life, so the pouch being "
                    "discarded before use does not remove the route. A sodium partial-salt ionomer seal layer is a permitted food-contact resin (21 CFR 177.1330, P), so the film "
                    "specification must exclude it or a migration test must show no sodium. Migration was not tested (stated limit).",
    },
]

# Fallback binder, computed beside the primary (not added to the primary total).
FALLBACK = {
    "name": "Binder and filler: isomalt (INS 953), fallback", "mass_g": 0.80,
    "na_high_frac": ash_bound(0.05), "na_high_tier": "DERIVED from P",
    "na_basis": "FAO JECFA Monographs 5 (69th JECFA 2008), Isomalt: sulfated ash not more than 0.05%; water not more than 7.0%; reducing sugars not more than 0.3%. "
                "Bound assumes all residue is sodium sulphate.",
}

# Water used to make up the drink. WHO: sodium in potable water is "typically less than 20 mg/l" but "can greatly exceed this in some countries" (P).
# 20 mg/L is a typical value, NOT a ceiling. A Thai Department of Health nutritionist is reported (Thai PBS World, 23 Feb 2021, S) to say tap water
# normally holds 100 to 200 mg of sodium per litre. WHO notes a taste concern above 200 mg/L. Thai tap or bottled water was not measured.
WATER = {"name": "Water to 330 mL", "volume_ml": SERVE_ML,
         "na_low_mg_per_l": 0.0, "na_high_mg_per_l": 20.0,
         "tier": "P for the WHO typical value only (typically under 20 mg/L; can greatly exceed this); Thai water not measured",
         "thai_reported_mg_per_l_range": [100.0, 200.0],
         "thai_reported_tier": "S (news report of a Department of Health nutritionist, Thai PBS World, 23 Feb 2021; page read through a fetch tool extraction)",
         "who_taste_threshold_mg_per_l": 200.0}
WATER_LEVELS_MG_PER_L = [0.0, 20.0, 100.0, 200.0]

# Thai Notification 445 Table 1 (per reference serving and per consumed serving), strict "less than" limits, mg
TABLE1 = {"sodium-free (free of sodium)": 5.0, "very low sodium": 35.0, "low sodium": 140.0}
# Thai Notification 445 Table 2 (per 100 mL), "not more than" limits, mg per 100 mL (only if Case 2 applied)
TABLE2_PER100ML = {"sodium-free (free of sodium)": 5.0, "very low sodium": 20.0, "low sodium": 60.0}
# Codex CAC/GL 23 (per 100 g), mg
CODEX_PER100G = {"sodium-free": 5.0, "very low sodium": 40.0, "low sodium": 120.0}


def per_component():
    rows = []
    for c in components:
        m_mg = c["mass_g"] * 1000.0
        low_mg = m_mg * c["na_low_frac"]
        high_mg = m_mg * c["na_high_frac"]
        row = {
            "component": c["name"],
            "mass_g_per_serve": c["mass_g"],
            "mass_tier": c["mass_tier"],
            "sodium_wt_fraction_low": c["na_low_frac"],
            "sodium_wt_fraction_high": round(c["na_high_frac"], 8),
            "sodium_high_tier": c["na_high_tier"],
            "sodium_mg_per_serve_low": round(low_mg, 3),
            "sodium_mg_per_serve_high": round(high_mg, 3),
            "sodium_mg_per_100ml_low": round(low_mg / SERVE_ML * 100.0, 3),
            "sodium_mg_per_100ml_high": round(high_mg / SERVE_ML * 100.0, 3),
            "na_fraction_that_alone_reaches_5mg_per_serve_pct": (
                round(5.0 / m_mg * 100.0, 4) if m_mg > 0 else None),
            "basis": c["na_basis"],
        }
        if "indicator_frac" in c:
            row["indicator_sodium_mg_per_serve"] = round(m_mg * c["indicator_frac"], 3)
            row["indicator_note"] = c["indicator_note"]
        rows.append(row)
    return rows


def fallback_row():
    m_mg = FALLBACK["mass_g"] * 1000.0
    high = m_mg * FALLBACK["na_high_frac"]
    return {
        "component": FALLBACK["name"], "mass_g_per_serve": FALLBACK["mass_g"],
        "sodium_wt_fraction_high": round(FALLBACK["na_high_frac"], 8), "sodium_high_tier": FALLBACK["na_high_tier"],
        "sodium_mg_per_serve_low": 0.0, "sodium_mg_per_serve_high": round(high, 3),
        "sodium_mg_per_100ml_high": round(high / SERVE_ML * 100.0, 3), "basis": FALLBACK["na_basis"],
    }


def water_range():
    low = WATER["na_low_mg_per_l"] * SERVE_ML / 1000.0
    high = WATER["na_high_mg_per_l"] * SERVE_ML / 1000.0
    return {"low_mg_per_serve": round(low, 3), "high_mg_per_serve": round(high, 3),
            "low_mg_per_100ml": round(low / SERVE_ML * 100.0, 3),
            "high_mg_per_100ml": round(high / SERVE_ML * 100.0, 3),
            "tier": WATER["tier"],
            "high_case_basis": "the WHO typical value of 20 mg per litre, used as the high end of the range for water at or below that level. It is not a ceiling: "
                               "the WHO text says concentrations can greatly exceed it in some countries, and a Thai Department of Health nutritionist is reported to put "
                               "tap water at 100 to 200 mg per litre (S). See water_sensitivity.",
            "thai_reported_mg_per_l_range": WATER["thai_reported_mg_per_l_range"],
            "thai_reported_tier": WATER["thai_reported_tier"],
            "thai_reported_mg_per_serve_range": [round(v * SERVE_ML / 1000.0, 2) for v in WATER["thai_reported_mg_per_l_range"]]}


def totals(rows, water, fb):
    formula_low = sum(r["sodium_mg_per_serve_low"] for r in rows)
    formula_high = sum(r["sodium_mg_per_serve_high"] for r in rows)
    sourced_part = sum(r["sodium_mg_per_serve_high"] for r in rows if r["sodium_high_tier"].startswith("DERIVED from P"))
    assumed_part = sum(r["sodium_mg_per_serve_high"] for r in rows if r["sodium_high_tier"] == "ASSUMPTION")
    total_low = formula_low + water["low_mg_per_serve"]
    total_high = formula_high + water["high_mg_per_serve"]
    mannitol_high = next(r["sodium_mg_per_serve_high"] for r in rows if "mannitol" in r["component"])
    formula_high_fallback = formula_high - mannitol_high + fb["sodium_mg_per_serve_high"]
    return {
        "formula_ingredients_mg_per_serve": [round(formula_low, 3), round(formula_high, 3)],
        "formula_high_part_bounded_by_P_limits_mg": round(sourced_part, 3),
        "formula_high_part_planning_values_mg": round(assumed_part, 3),
        "total_with_water_mg_per_serve": [round(total_low, 3), round(total_high, 3)],
        "total_with_water_mg_per_100ml": [round(total_low / SERVE_ML * 100.0, 3), round(total_high / SERVE_ML * 100.0, 3)],
        "total_with_water_mg_per_litre": [round(total_low / SERVE_ML * 1000.0, 3), round(total_high / SERVE_ML * 1000.0, 3)],
        "formula_high_with_isomalt_fallback_mg_per_serve": round(formula_high_fallback, 3),
        "total_high_with_isomalt_fallback_mg_per_serve": round(formula_high_fallback + water["high_mg_per_serve"], 3),
        "total_high_includes_assumed_planning_values": True,
    }


def claim_tests(rows, total_low, total_high):
    """Case 1 (Table 1), consumed serving 330 mL, water counted."""
    out = {}
    formula_high = sum(r["sodium_mg_per_serve_high"] for r in rows)
    for name, lim in TABLE1.items():
        out[name] = {
            "table1_limit_mg_per_serve_below": lim,
            "limit_mg_per_litre_made_up_drink": round(lim / SERVE_ML * 1000.0, 2),
            "range_meets_on_estimate": ("yes for whole range" if total_high < lim
                                        else ("only at low end" if total_low < lim else "no")),
            "measured_value_needed": "a measured sodium value for the made-up drink, below %s mg per 330 mL" % lim,
        }
    out["water_sodium_ceiling_mg_per_l_if_formula_at_high_case"] = {
        name: round(max(0.0, (lim - formula_high) / SERVE_ML * 1000.0), 2) for name, lim in TABLE1.items()
    }
    out["water_sodium_ceiling_mg_per_l_if_formula_at_zero"] = {
        name: round(lim / SERVE_ML * 1000.0, 2) for name, lim in TABLE1.items()
    }
    out["water_ceilings_both_bases_mg_per_l"] = water_ceilings(formula_high)
    return out


def water_ceilings(formula_high):
    """Highest water sodium (mg per litre) at which the whole made-up drink still passes Table 1 (strict less-than), on each Case 1 basis.
    Consumed serving: formula high plus water over 330 mL. Two-fold reference serving: the product amount for 400 mL (formula scaled by 400/330)
    plus water over 400 mL. The stricter of the two binds if both apply."""
    scale = TWOFOLD_RS_ML / SERVE_ML
    out = {}
    for name, lim in TABLE1.items():
        c330_hi = max(0.0, (lim - formula_high) / SERVE_ML * 1000.0)
        c330_0 = lim / SERVE_ML * 1000.0
        c400_hi = max(0.0, (lim - formula_high * scale) / TWOFOLD_RS_ML * 1000.0)
        c400_0 = lim / TWOFOLD_RS_ML * 1000.0
        out[name] = {
            "limit_mg": lim,
            "consumed_330ml_formula_at_high_case": round(c330_hi, 2),
            "consumed_330ml_formula_at_zero": round(c330_0, 2),
            "two_fold_reference_400ml_formula_at_high_case": round(c400_hi, 2),
            "two_fold_reference_400ml_formula_at_zero": round(c400_0, 2),
            "binding_ceiling_if_both_bases_apply_formula_at_high_case": round(min(c330_hi, c400_hi), 2),
        }
    return out


def water_sensitivity(rows):
    """Total sodium of the made-up drink for water at several sodium levels (formula at its high case), with the verdict on each basis.
    Levels: 0; 20 (WHO typical value); 100 and 200 (the Thai Department of Health figure reported in the press, S; 200 is also the WHO taste threshold)."""
    f_high = sum(r["sodium_mg_per_serve_high"] for r in rows)
    scale = TWOFOLD_RS_ML / SERVE_ML
    table = []
    for w in WATER_LEVELS_MG_PER_L:
        t330 = f_high + w * SERVE_ML / 1000.0
        t400 = f_high * scale + w * TWOFOLD_RS_ML / 1000.0
        per100 = t330 / SERVE_ML * 100.0
        row = {"water_mg_per_litre": w, "water_mg_per_330ml": round(w * SERVE_ML / 1000.0, 2),
               "total_mg_per_330ml_formula_high": round(t330, 2), "total_mg_per_400ml_two_fold_basis": round(t400, 2),
               "total_mg_per_100ml_330ml_basis": round(per100, 2)}
        for name, lim in TABLE1.items():
            row["case1_330ml_" + name] = "passes" if t330 < lim else "fails"
            row["case1_two_fold_" + name] = "passes" if t400 < lim else "fails"
        for name, lim in TABLE2_PER100ML.items():
            row["case2_hypothetical_" + name] = "passes" if per100 <= lim else "fails"
        table.append(row)
    return {"formula_high_mg_per_330ml": round(f_high, 3), "rows": table,
            "note": "Water counted in the claim. Case 2 is a hypothetical (the cube has a prescribed reference serving, so Case 1 applies on our reading). "
                    "If the regulator does not count the plain water, the formula alone decides: 0 to 1.98 mg per 330 mL and 0 to 2.40 mg on the two-fold basis, "
                    "which passes all three claim limits."}


def claim_scenarios(rows, water):
    """Three claim bases, each with water counted (WHO high case) and not counted (formula only)."""
    f_low = sum(r["sodium_mg_per_serve_low"] for r in rows)
    f_high = sum(r["sodium_mg_per_serve_high"] for r in rows)
    w_high_per_ml = WATER["na_high_mg_per_l"] / 1000.0  # mg per mL
    scen = {}

    def verdict(value_high, lim, strict_less):
        ok = value_high < lim if strict_less else value_high <= lim
        return "passes across the estimated range" if ok else "passes only part of the estimated range"

    # Case 1, consumed serving 330 mL (Table 1, strict less-than)
    c1 = {}
    for name, lim in TABLE1.items():
        c1[name] = {
            "limit_mg": lim,
            "water_not_counted_high_mg": round(f_high, 3), "water_not_counted": verdict(f_high, lim, True),
            "water_counted_high_mg": round(f_high + SERVE_ML * w_high_per_ml, 3),
            "water_counted": verdict(f_high + SERVE_ML * w_high_per_ml, lim, True),
        }
    scen["case1_consumed_serving_330ml"] = c1

    # Case 1, two-fold reference serving: the product amount for 400 mL (cube mass scaled 400/330), if the reference amount is <= 30 g
    scale = TWOFOLD_RS_ML / SERVE_ML
    c1b = {}
    for name, lim in TABLE1.items():
        fh = f_high * scale
        wh = TWOFOLD_RS_ML * w_high_per_ml
        c1b[name] = {
            "limit_mg": lim,
            "product_scale_vs_one_cube": round(scale, 4),
            "water_not_counted_high_mg": round(fh, 3), "water_not_counted": verdict(fh, lim, True),
            "water_counted_high_mg": round(fh + wh, 3), "water_counted": verdict(fh + wh, lim, True),
        }
    scen["case1_two_fold_reference_serving_400ml_if_reference_amount_not_over_30g"] = c1b

    # Case 2, per 100 mL (Table 2, not more than). HYPOTHETICAL: Annex 4 clause 2.1 sends foods without a prescribed reference serving to Case 2;
    # the cube has one (Annex 2, category 2, item 3), so Case 2 applies only if the regulator rules the cube outside Case 1.
    c2 = {}
    for name, lim in TABLE2_PER100ML.items():
        per100_not = f_high / SERVE_ML * 100.0
        per100_cnt = (f_high + SERVE_ML * w_high_per_ml) / SERVE_ML * 100.0
        c2[name] = {
            "limit_mg_per_100ml_not_more_than": lim,
            "water_not_counted_high_mg_per_100ml": round(per100_not, 3), "water_not_counted": verdict(per100_not, lim, False),
            "water_counted_high_mg_per_100ml": round(per100_cnt, 3), "water_counted": verdict(per100_cnt, lim, False),
        }
    scen["case2_per_100ml_hypothetical_only"] = c2
    scen["note"] = ("Case 1 applies on our reading (Annex 2, category 2, item 3 gives the cube a prescribed reference serving). The second Case 1 basis "
                    "(two-fold reference serving) applies only if the reference amount counts as not more than 30 g; the regulator's reading is UNVERIFIED. "
                    "Case 2 is shown as a hypothetical for the case in which the regulator rules the cube outside Case 1; it is not a current basis. "
                    "The water ceilings are in claim_tests_table1_case1.water_ceilings_both_bases_mg_per_l and the water levels in water_sensitivity.")
    return scen


def potassium_line():
    """Potassium per serve (clause 2.3 marks Potassium* mandatory in the standard format) and its rounding under clause 2.6."""
    k_mg = 0.81 * 1000.0 * K_IN_KHCO3
    def round_label(mg):
        if mg < 5:
            return 0
        if mg <= 140:
            return int(5 * round(mg / 5.0 + 1e-12))
        return int(10 * round(mg / 10.0 + 1e-12))
    declared = round_label(k_mg)
    return {
        "potassium_mg_per_serve_from_0p81g_KHCO3": round(k_mg, 2),
        "repo_figure_mg": 317,
        "declared_after_clause_2_6_rounding_mg": declared,
        "thai_rdi_potassium_mg_annex3": 3500,
        "percent_of_thai_rdi_declared_value": round(declared / 3500.0 * 100.0, 2),
        "thai_rdi_sodium_mg_annex3": 2000,
        "note": "Notification 445 Annex 1 clause 2.3 asterisks Potassium as mandatory in the standard format; Notification 446 replaced clause 5(1) of "
                "Notification 394 so that the panel follows Annex 1 of 445 (FDA unofficial English text). A potassium line is therefore expected on the panel.",
    }


def binder_sugar_and_excise(rows):
    # JECFA mannitol: total sugars not more than 1.0% (as glucose), reducing sugars not more than 0.3%
    m_g = 0.80
    total_sugar_mg = m_g * 1000.0 * 0.010
    reducing_mg = m_g * 1000.0 * 0.003
    iso_reducing_mg = m_g * 1000.0 * 0.003  # JECFA isomalt: reducing sugars not more than 0.3%
    polyol_g_per_100ml = m_g / SERVE_ML * 100.0
    flavour_g_per_100ml = 0.05 / SERVE_ML * 100.0
    return {
        "mannitol_total_sugars_bound_mg_per_serve": round(total_sugar_mg, 2),
        "mannitol_total_sugars_bound_g_per_100ml": round(total_sugar_mg / 1000.0 / SERVE_ML * 100.0, 5),
        "mannitol_reducing_sugars_bound_mg_per_serve": round(reducing_mg, 2),
        "isomalt_reducing_sugars_bound_mg_per_serve": round(iso_reducing_mg, 2),
        "binder_if_all_counted_as_sugar_g_per_100ml": round(polyol_g_per_100ml, 4),
        "flavour_if_all_counted_as_sugar_g_per_100ml": round(flavour_g_per_100ml, 4),
        "tier_ceiling_g_per_100ml_lowest_tier": 6.0,
        "tier_stays_lowest_even_if_all_polyol_counted": (polyol_g_per_100ml + flavour_g_per_100ml) <= 6.0,
        "mannitol_solubility_g_per_l_25c_pubchem_secondary": 216.0,
        "mannitol_dose_g_per_l": round(m_g / SERVE_ML * 1000.0, 3),
        "mannitol_fraction_of_saturation": round((m_g / SERVE_ML * 1000.0) / 216.0, 4),
        "eu_laxative_benchmark_polyols_g_per_day": 20.0,
        "binder_dose_fraction_of_20g": round(m_g / 20.0, 3),
        "water_in_binder_limit_mg_per_serve": {
            "mannitol_loss_on_drying_max_0p3pct": round(m_g * 1000.0 * 0.003, 2),
            "isomalt_water_max_7pct": round(m_g * 1000.0 * 0.07, 2),
            "ratio_isomalt_to_mannitol": round(0.07 / 0.003, 1),
        },
    }


def peg_check():
    """Thai 468 row for PEG (INS 1521) in category 14.1.4: 500 mg/kg, condition 127 (level applies to the drink as ready to drink)."""
    drink_kg = (SERVE_ML * 1.0 + 3.79) / 1000.0  # water at 1 g/mL plus the 3.79 g cube; CO2 loss ignored (DERIVED convention)
    limit_mg = 500.0 * drink_kg
    binder_mg = 800.0
    return {
        "thai_468_peg_limit_mg_per_kg_ready_to_drink": 500.0,
        "drink_mass_kg_convention": round(drink_kg, 5),
        "max_peg_mg_per_cube_at_limit": round(limit_mg, 1),
        "peg_at_0p80g_mg_per_kg_of_drink": round(binder_mg / drink_kg, 0),
        "peg_at_0p80g_times_the_limit": round(binder_mg / limit_mg, 2),
        "note": "PEG at the Thai level can be a lubricant at no more than about %d mg per cube; it cannot be the 0.80 g binder and filler." % round(limit_mg),
    }


def energy_and_rounding(rows):
    # Thai Notification 445 Annex 1, 2.4 conversion factors (P): organic acid 3 kcal/g; mannitol 1.6; isomalt 2; erythritol 0
    citric_kcal = 2.10 * 3.0
    mannitol_kcal = 0.80 * 1.6
    isomalt_kcal = 0.80 * 2.0
    erythritol_kcal = 0.80 * 0.0

    def round_energy(x):
        if x < 5:
            return 0
        if x < 50:
            return int(5 * round(x / 5.0 + 1e-12))
        return int(10 * round(x / 10.0 + 1e-12))

    def round_sodium_label(mg):
        if mg < 5:
            return 0
        if mg <= 140:
            return int(5 * round(mg / 5.0 + 1e-12))
        return int(10 * round(mg / 10.0 + 1e-12))
    return {
        "energy_kcal_per_serve_with_mannitol_binder": round(citric_kcal + mannitol_kcal, 2),
        "energy_kcal_per_serve_with_isomalt_binder": round(citric_kcal + isomalt_kcal, 2),
        "energy_kcal_per_serve_with_erythritol_binder": round(citric_kcal + erythritol_kcal, 2),
        "energy_declared_rounded_with_mannitol": round_energy(citric_kcal + mannitol_kcal),
        "energy_declared_rounded_with_isomalt": round_energy(citric_kcal + isomalt_kcal),
        "energy_declared_rounded_with_erythritol": round_energy(citric_kcal + erythritol_kcal),
        "rounding_rule_note": "Notification 445 clause 2.6: energy 5 to under 50 kcal rounded to a step of 5; under 5 kcal declared as 0.",
        "sodium_declared_rounded_low_mg": round_sodium_label(0.0),
        "sodium_declared_rounded_high_mg": round_sodium_label(
            totals(rows, water_range(), fallback_row())["total_with_water_mg_per_serve"][1]),
        "sodium_declared_rounded_as_sold_high_mg": round_sodium_label(sum(r["sodium_mg_per_serve_high"] for r in rows)),
        "sodium_rounding_note": "Clause 2.6: sodium under 5 mg declared as 0; 5 to 140 mg in steps of 5; over 140 mg in steps of 10.",
        "sugar_alcohol_line_note": "Clause 2.3 remark ** : a sugar alcohols line is displayed if energy is calculated with the clause 2.4 2) 2.2 conversion factors "
                                   "(0.80 g of mannitol per cube).",
    }


def binder_price_proxy():
    # UN Comtrade HS 290543 (mannitol), Thailand imports 2025, World, CIF USD 2,095,441.421 over 476,781 kg (P; re-read 20 Oct 2026).
    # Mid rate 33.5495 THB/USD (Bank of Thailand, 15 Oct 2026, repo raw file; DERIVED mid of buying sight and selling transfer).
    usd_per_kg = 2095441.421 / 476781.0
    fx = 33.5495
    thb_per_kg = usd_per_kg * fx
    # Binder-only break-even: contribution THB 4.91 per cube (six-cube carton) less stop threshold THB 3.51 = THB 1.40 per cube.
    # The submission already assigns that THB 1.40 to the pouch high case (THB 2.70 pouch), so this break-even assumes the pouch at base cost.
    gap = 4.91 - 3.51
    breakeven = gap / 0.80 * 1000.0
    # Spread by origin, from the saved Comtrade rows (comtrade_thai_imports_polyols_2025.md; CIF USD over net kg; small-volume origins are less reliable).
    world_u = 2095441.421 / 476781.0
    rows_origin = [("World", 2095441.421, 476781.0), ("China", 1299035.829, 427232.0), ("France", 297949.194, 24375.0),
                   ("Japan", 257495.476, 19951.0), ("Germany", 233269.068, 4929.0)]
    spread = []
    for name, cif, kg in rows_origin:
        u = cif / kg
        thb_kg = u * fx
        per_cube = thb_kg * 0.80 / 1000.0
        spread.append({"origin": name, "net_kg": kg, "usd_per_kg": round(u, 3), "thb_per_kg": round(thb_kg, 1),
                       "thb_per_cube_0p8g": round(per_cube, 3), "times_world_unit_value": round(u / world_u, 2),
                       "share_of_1p40_headroom": round(per_cube / gap, 3)})
    return {
        "comtrade_hs290543_world_usd_per_kg": round(usd_per_kg, 4),
        "fx_thb_per_usd_mid": fx,
        "proxy_thb_per_kg": round(thb_per_kg, 1),
        "proxy_thb_per_cube_0p8g": round(thb_per_kg * 0.80 / 1000.0, 3),
        "premium_assumption_low_x": 1,
        "premium_assumption_high_x": 3,
        "thb_per_cube_at_3x_premium": round(thb_per_kg * 3 * 0.80 / 1000.0, 3),
        "binder_alone_takes_contribution_to_stop_threshold_at_thb_per_kg": round(breakeven, 0),
        "gap_contribution_to_stop_threshold_thb_per_cube": round(gap, 2),
        "gap_note": "THB 4.91 less THB 3.51. The submission already uses this gap for the pouch high case (THB 2.70 pouch), so it cannot be spent twice.",
        "breakeven_usd_per_kg": round(breakeven / fx, 2),
        "breakeven_over_proxy_ratio": round(breakeven / thb_per_kg, 1),
        "isomalt_price": "UNVERIFIED (no Thai or import figure found; HS code not established). Same ceiling applies.",
        "origin_spread_from_saved_rows": spread,
        "origin_spread_note": "Thailand imports 2025, HS 290543, CIF USD over net kg, from the saved Comtrade page (rows as extracted; the page records that the fetch tool "
                              "returned a model-written extraction, not the verbatim JSON). The unit value runs from the world average to about 10.8 times it (Germany, 4,929 kg). "
                              "A tableting grade could sit anywhere in that spread, including near the break-even. The grade premium of 1 to 3 times is an ASSUMPTION; "
                              "the spread is the only data on the page.",
        "tier": "PROXY (bulk import unit value; grade premium is ASSUMPTION)",
    }


def formula_mass_check(rows):
    """The five specified components add to the central dry mass; the formula carries no lubricant, glidant or other excipient."""
    total_g = sum(r["mass_g_per_serve"] for r in rows)
    return {"sum_of_specified_components_g": round(total_g, 3), "central_dry_cube_mass_g_repo": 3.79,
            "difference_g": round(total_g - 3.79, 3),
            "lubricant_in_formula": "none specified (the five components account for the whole 3.79 g)",
            "sodium_salt_lubricants_excluded_by_specification": ["sodium stearyl fumarate", "sodium benzoate", "sodium lauryl sulfate",
                                                                 "monosodium citrate or other sodium-coated acid grades"],
            "tier": "DERIVED (arithmetic on the repo masses); the exclusion list is the team's specification (ASSUMPTION until supplier declarations)"}


def peg_lubricant_contingent():
    """If a non-sodium soluble lubricant is ever added: PEG (INS 1521), Thai 468 level 500 mg/kg as ready to drink (P); JECFA sulfated ash not more than 0.1 percent (P).
    Not part of the 3.79 g formula and not added to the totals."""
    drink_kg = (SERVE_ML * 1.0 + 3.79) / 1000.0
    max_mg = 500.0 * drink_kg
    na_bound = max_mg * ash_bound(0.1)
    bw = 60.0  # ASSUMPTION body weight, kg
    adi_mg = 10.0 * bw
    return {"thai_468_level_mg_per_kg": 500.0, "max_peg_mg_per_cube_at_thai_level": round(max_mg, 1),
            "jecfa_sulfated_ash_max_pct": 0.1, "sodium_upper_bound_mg_per_cube_at_max_peg": round(na_bound, 3),
            "jecfa_adi_mg_per_kg_bw": 10.0, "assumed_body_weight_kg": bw, "peg_at_max_as_pct_of_adi_per_serve": round(max_mg / adi_mg * 100.0, 1),
            "note": "Contingent only. The formula as specified has no lubricant, so nothing is added to the totals. If a lubricant proves necessary at the bench "
                    "trial, PEG up to about 167 mg per cube adds at most 0.054 mg of sodium (DERIVED from the JECFA ash limit) and would be entered as a new line. "
                    "The body weight is an ASSUMPTION."}


def electrolyte_standard_check(rows):
    """Thai Notification 195 (B.E. 2543), clause 4 (1), per litre of electrolyte drink: sodium 460 to 920 mg; sugar glucose or fructose at least 2 percent by weight
    or sucrose at least 4 percent; potassium not more than 195 mg (if present); bicarbonate not more than 793 mg; citrate not more than 819 mg.
    The cube made up in 330 mL is compared with it. This shows why the drink cannot be presented as an electrolyte drink; it does not decide the classification."""
    f_high = sum(r["sodium_mg_per_serve_high"] for r in rows)
    k_mg = 0.81 * 1000.0 * K_IN_KHCO3
    litre = 1000.0 / SERVE_ML
    hco3_mg = 0.81 * 1000.0 * 61.0168 / 100.1151  # bicarbonate anion share of KHCO3 (HCO3 61.0168, KHCO3 100.1151), before reaction with the acid
    citric_mg = 2.10 * 1000.0
    return {
        "sodium_mg_per_litre_formula_only_range": [0.0, round(f_high * litre, 1)],
        "sodium_required_min_max_mg_per_litre": [460.0, 920.0],
        "sodium_below_minimum": True,
        "potassium_mg_per_litre": round(k_mg * litre, 0), "potassium_max_mg_per_litre": 195.0,
        "bicarbonate_before_reaction_mg_per_litre": round(hco3_mg * litre, 0), "bicarbonate_max_mg_per_litre": 793.0,
        "citric_acid_total_mg_per_litre_as_added": round(citric_mg * litre, 0), "citrate_max_mg_per_litre": 819.0,
        "citrate_basis_note": "The notification does not say how citrate is expressed; the citric acid added is shown as a magnitude only.",
        "sugar_required": "glucose or fructose at least 2 percent by weight, or sucrose at least 4 percent",
        "sugar_in_cube": "none added (mannitol is not a sugar in the Thai nutrition definition)",
        "reading": "The cube drink is far outside the clause 4 (1) composition of an electrolyte drink on sodium, sugar and potassium. If a regulator classed it as an "
                   "electrolyte drink it could not meet that standard, and condition TH3 would also require the polyol to be used together with sugar. "
                   "The recipe therefore must not be named or presented as an electrolyte drink; the classification is part of the Gate 1 opinion.",
        "tier": "P for the standard (Thai original, rendered pages); DERIVED for the cube values",
    }


def as_sold_cube_check(rows):
    # Notification 445 Annex 1, 1.7 (dual display): the as-sold panel is per cube (dry), water excluded.
    formula_low = sum(r["sodium_mg_per_serve_low"] for r in rows)
    formula_high = sum(r["sodium_mg_per_serve_high"] for r in rows)
    return {
        "per_cube_mg_low": round(formula_low, 3),
        "per_cube_mg_high": round(formula_high, 3),
        "declared_rounded_high_mg": (0 if formula_high < 5 else int(5 * round(formula_high / 5.0 + 1e-12))),
        "rule": "Notification 445 clause 2.6: under 5 mg declared as 0.",
    }


def main():
    rows = per_component()
    fb = fallback_row()
    water = water_range()
    tot = totals(rows, water, fb)
    tl, th = tot["total_with_water_mg_per_serve"]
    result = {
        "task": "T11 sodium check, binder choice and label thresholds (second revision, 20 October 2026)",
        "date_run": "2026-10-20",
        "seed_recorded": SEED,
        "units": "mg per 330 mL serve unless stated",
        "serve_ml": SERVE_ML,
        "reference_serving_ml_case1": RS_ML,
        "na_fraction_in_sodium_sulphate": round(NA_IN_NA2SO4, 5),
        "components": rows,
        "fallback_binder_isomalt": fb,
        "water": water,
        "totals": tot,
        "claim_tests_table1_case1": claim_tests(rows, tl, th),
        "claim_scenarios": claim_scenarios(rows, water),
        "table2_per100ml_case2_limits_mg": TABLE2_PER100ML,
        "codex_gl23_per100g_limits_mg": CODEX_PER100G,
        "energy_and_label_rounding": energy_and_rounding(rows),
        "potassium_panel_line": potassium_line(),
        "binder_sugar_excise_and_tolerance": binder_sugar_and_excise(rows),
        "peg_6000_limit_check": peg_check(),
        "peg_lubricant_contingent": peg_lubricant_contingent(),
        "formula_mass_and_lubricant_check": formula_mass_check(rows),
        "electrolyte_drink_standard_check_notification_195": electrolyte_standard_check(rows),
        "water_sensitivity": water_sensitivity(rows),
        "binder_price_proxy": binder_price_proxy(),
        "as_sold_cube_panel_check": as_sold_cube_check(rows),
        "limits": [
            "No measured sodium value exists for any component or for the made-up drink.",
            "Potassium bicarbonate (food grade) and lemon flavour high cases are planning values (ASSUMPTION), not specifications. "
            "The citric acid, sucralose, mannitol and isomalt high cases are upper bounds derived from JECFA sulfated-ash limits (DERIVED from P).",
            "Thai Notification 468 rows for mannitol, isomalt, maltodextrin and erythritol in category 14.1.4 were read from rendered pages on 20 October 2026 "
            "(quantum satis; TH3 on mannitol, isomalt and erythritol applies to electrolyte drinks only).",
            "Water sodium is the largest open term. The WHO typical value (under 20 mg/L) is not a ceiling: WHO says concentrations can greatly exceed it in some countries, "
            "and a Thai Department of Health nutritionist is reported to put tap water at 100 to 200 mg/L (S). Thai tap and bottled water were not measured. "
            "Whether the Thai rule counts the plain water in the claim calculation is not settled (Annex 2 category 2 item 3 sets the reference serving as the defined amount "
            "for preparing 200 mL; the Thai FAQ section 8 (1) treats water of insignificant nutrient content separately).",
            "Whether the two-fold reference serving basis applies (reference amount not over 30 g) is a regulatory reading, UNVERIFIED. If it applies, the stricter water ceiling binds.",
            "Case 2 (per 100 mL) is a hypothetical: the cube has a prescribed reference serving, so Case 1 applies on our reading.",
            "Binder price is a PROXY (world import unit value, with a spread by origin), not a Thai supplier price; the grade premium is ASSUMPTION; isomalt price UNVERIFIED.",
            "The formula has no lubricant; whether a 14 mm cube can be pressed without one is untested (bench trial). A PEG lubricant is shown as a contingent line only.",
            "Pouch film sodium and migration were not tested; the film specification is not supplied.",
            "Notification 467 (B.E. 2568) was read in English in the T10 record (replaces only paragraph one of clause 2.1 of Annex 1: white background and font sizes; potassium unchanged).",
            "The Thai excise schedule is read from the B.E. 2560 primary extract and a press report of the phase 4 rates (S); the later decree was not opened.",
        ],
    }
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "t11_sodium_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    print("wrote", out_path)
    print("formula mg/serve", tot["formula_ingredients_mg_per_serve"], "total mg/serve", tot["total_with_water_mg_per_serve"])
    print("total mg/100 mL", tot["total_with_water_mg_per_100ml"], "mg/L", tot["total_with_water_mg_per_litre"])
    print("sourced part", tot["formula_high_part_bounded_by_P_limits_mg"], "planning part", tot["formula_high_part_planning_values_mg"])
    wc = result["claim_tests_table1_case1"]["water_ceilings_both_bases_mg_per_l"]
    for k, v in wc.items():
        print("water ceiling", k, v)
    for r in result["water_sensitivity"]["rows"]:
        print("water", r["water_mg_per_litre"], "mg/L -> total330", r["total_mg_per_330ml_formula_high"], "total400", r["total_mg_per_400ml_two_fold_basis"])
    for r in result["binder_price_proxy"]["origin_spread_from_saved_rows"]:
        print("price", r["origin"], r["thb_per_kg"], r["thb_per_cube_0p8g"], r["share_of_1p40_headroom"])


if __name__ == "__main__":
    main()
