#!/usr/bin/env python3
"""Final gate simulation for the sodium-free potassium-bicarbonate lime fizz cube.

Replaces the bench test (G1 sodium, G2 fizz) and the medical test (G3 potassium) with a
physics and mass-balance screen. This screen does NOT establish medical safety for potassium;
that question stays a stated limit.

Standard library only. Reproduce with:
    python final_gate_sim.py
Writes final_gate_sim_results.json beside this file and prints a summary.

Status tags: sourced, derived, assumed, snippet, limit.
PASS_RULE and CALIBRATION are defined below, before any case is evaluated.
Claim policy: no sugar claim of any kind; sweetness is disclosed as an intensive sweetener.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "final_gate_sim_results.json")
READ_DATE = "2026-10-18"

# ------------------------------------------------------------ sources
SOURCES = {
    "lange_bunsen_table": {
        "url": "https://en.wikipedia.org/wiki/Carbon_dioxide_(data_page)",
        "content": ("Bunsen volumes of CO2 in water at 101.3 kPa: 0 C 1.713; 4 C 1.473; 5 C 1.424; "
                    "20 C 0.878; 25 C 0.759. Cited to Lange's Handbook, 10th ed."),
        "status": "sourced (read in effervescent_cube_screen.py, WebFetch 2026-10-18; secondary page)",
    },
    "thai_p445": {
        "url": "https://food.fda.moph.go.th/media.php?id=689363893683888128&name=P445_EN.pdf",
        "content": ("Notification 445 (2023), English text: Table 1 sodium free less than 5 mg per reference "
                    "serving; Annex 2 reference serving for carbonated beverages 200 ml; Annex 3 Thai RDI "
                    "sodium 2000 mg and potassium 3500 mg."),
        "status": ("sourced earlier (English PDF text recorded in effervescent_cube_screen.py, 2026-10-18); "
                   "re-fetch on 2026-10-18 returned a binary PDF, not re-read; Thai text not read; the "
                   "sodium-free threshold conflicts with the US 21 CFR 101.61 values flagged in rework/44 "
                   "(unresolved)"),
    },
    "chemlinked_thai_labelling": {
        "url": "https://food.chemlinked.com/news/food-news/thailand-implements-new-nutrition-labeling-regulations",
        "content": ("Trade summary (secondary): nine mandatory nutrients on the Thai nutrition panel, listed as "
                    "energy, total fat, saturated fat, cholesterol, protein, carbohydrate, total sugars, sodium "
                    "and potassium; potassium newly added. Says Thai RDIs were updated against Codex NRVs; "
                    "gives no numeric potassium RDI; points to Notification 445 Attachment 3."),
        "status": "snippet and secondary (WebFetch and WebSearch 2026-10-18; not the Thai FDA text)",
    },
    "ifas_carbonation": {
        "url": "https://ask.ifas.ufl.edu/publication/FS379",
        "content": "Minimum detectable carbonation about 0.6 volumes; most soft drinks carbonated to 3 to 3.5 volumes.",
        "status": "sourced earlier (lime_cube_screen.py SOURCES, WebFetch 2026-10-18); not re-read in this run",
    },
    "bionumbers_co2_diffusion_25C": {
        "url": "https://bionumbers.hms.harvard.edu/bionumber.aspx?id=102625",
        "content": ("Title: coefficient for diffusion of CO2 in water at 25 C. Search snippet lists about "
                    "1.88e-9 m2/s (1980 wetted-wall study)."),
        "status": "snippet (WebSearch 2026-10-18; page not read)",
    },
    "lu_2013_speedy_angell_fit": {
        "url": "not recorded (WebSearch summary citing Lu et al. 2013, 2026-10-18)",
        "content": ("Speedy-Angell fit D = D0 (T/Ts - 1)^m, D0 = 13.942e-9 m2/s, Ts = 227.0 K, m = 1.7094, "
                    "measured 268 to 473 K. Recomputed here: 1.92e-9 m2/s at 298.15 K, about 1.05e-9 at 277.15 K."),
        "status": "snippet (fit parameters from a search summary; original page not read)",
    },
    "plos_one_2012_liger_belair": {
        "url": "https://doi.org/10.1371/journal.pone.0030628",
        "content": ("Champagne CO2 release by bubble and free-surface routes. No numeric mass-transfer coefficient "
                    "or degassing rate constant on the page (WebFetch 2026-10-18)."),
        "status": "read (no numeric value used; context only)",
    },
    "penetration_theory_estimate": {
        "url": "derived in final_gate_sim.py (no external source)",
        "content": ("Quiescent-surface penetration theory k_L = 2 sqrt(D/(pi t)) with D = 2e-9 m2/s and "
                    "t = 10 to 60 s gives about 6e-6 to 2e-5 m/s."),
        "status": "derived (own calculation; not a sourced value)",
    },
    "us_bottled_water_snippet": {
        "url": "https://getfoodfacts.com/food/water-bottled-non-carbonated-naya-173657",
        "content": "Database snippet: non-carbonated bottled water about 1 mg sodium per 100 g. US entry, not Thai.",
        "status": "snippet (WebSearch 2026-10-18; page not read); sensitivity only",
    },
    "thai_bottled_water_sodium": {
        "url": "not found",
        "content": ("No Thai bottled-water sodium label value found (two WebSearch queries on 2026-10-18, "
                    "including Singha drinking water). No page read; no bot check bypassed."),
        "status": "limit (value not found; water sodium is set as a specification in this screen)",
    },
    "thai_rdi_potassium_recheck": {
        "url": "https://food.chemlinked.com/news/food-news/thailand-implements-new-nutrition-labeling-regulations",
        "content": ("The potassium Thai RDI 3500 mg is the earlier repo read of the P445 English text. This run "
                    "did not reconfirm it, and the Codex-NRV remark above means the figure should be checked."),
        "status": "limit (Thai potassium RDI not reconfirmed; 2000 mg kept as a sensitivity only)",
    },
}

# ------------------------------------------------------------ constants
R_GAS = 8.314462618                                # J/(mol K), exact
P_STD_PA = 101325.0                                # Pa
T_STD_K = 273.15                                   # K
VM_L = R_GAS * T_STD_K / P_STD_PA * 1000.0         # L/mol, ideal gas at 0 C, 1 atm (derived, ~22.414)
M_C, M_H, M_O = 12.011, 1.008, 15.999
M_HCO3 = M_H + M_C + 3 * M_O                       # 61.016 g/mol (derived)
M_KHCO3 = 100.115                                  # g/mol (sourced, Wikipedia infobox via effervescent screen)
M_K = M_KHCO3 - M_HCO3                             # 39.099 g/mol (derived)
M_CITRIC = 192.123                                 # g/mol anhydrous (sourced, Wikipedia via screen)
CITRIC_PER_CO2 = 1.0 / 3.0                         # C6H8O7 + 3 KHCO3 -> K3C6H5O7 + 3 CO2 + 3 H2O (derived)

SERVING_ML = 330.0                                 # team computed task
REF_SERVING_ML = 200.0                             # Thai reference serving, carbonated beverages (sourced earlier)
NA_FREE_MG = 5.0                                   # Thai Table 1, sodium free per serving (sourced earlier; conflict open)
RDI_K_MG = 3500.0                                  # Thai RDI potassium (sourced earlier; not reconfirmed)
RDI_K_ALT_MG = 2000.0                              # sensitivity only (unverified alternative denominator)
K_GOOD_PCT = 15.0                                  # Thai Table 1 good source threshold (sourced earlier)
K_HIGH_PCT = 30.0                                  # Thai Table 1 high threshold (sourced earlier)

BUNSEN = {0: 1.713, 4: 1.473, 5: 1.424, 20: 0.878, 25: 0.759}   # volumes at 1 atm pure CO2 (sourced)
P_AIR_ATM = 0.00042                                # assumed ~420 ppm headspace CO2; C_eq is negligible
SA_D0, SA_TS, SA_M = 13.942e-9, 227.0, 1.7094      # Speedy-Angell fit for CO2 diffusivity (snippet)
A_OVER_V = 10.0                                    # m^-1, assumed 3.3e-3 m2 surface over 3.3e-4 m3 liquid

# Ingredient-side assumptions
SWEETENER_NA_MG = 0.0                              # assumed sodium-free intensive sweetener
FLAVOUR_NA_MG = 0.0                                # assumed
WATER_NA_MG_PER_L = {                              # Thai label not found; specification and sensitivity cases
    "design_spec_5_mg_per_L": 5.0,                 # the spec this screen proposes for the base water
    "us_snippet_10_mg_per_L": 10.0,                # US snippet, roughly 1 mg per 100 g; not Thai
    "stress_20_mg_per_L": 20.0,                    # stress case, assumed
}

# ------------------------------------------------------------ pass rule (fixed before any case is evaluated)
PASS_RULE = {
    "release_min_ml_at_2min": 5.0,                 # R2: measurable release by water displacement (assumed resolution)
    "dissolved_floor_vol_at_10min": 0.6,           # R3: still carbonated at 10 min (IFAS minimum detectable, sourced)
    "dissolution_spec_max_s": 60.0,                # R1: design spec, cube fully dissolved within 60 s (assumed)
    "measure_times_s": [120.0, 600.0],             # 2 and 10 minutes after the cube is dropped
    "sensitivity_release_ml": [1.0, 10.0],         # alternative measurable thresholds, sensitivity only
}
# R4 (construction check): no CO2 release at any time before the cube dissolves.

CALIBRATION = {
    "kl25_base_m_per_s": 2e-5,                     # calibration parameter; no sourced value found
    "kl25_low_m_per_s": 5e-6,
    "kl25_high_m_per_s": 1e-4,
    "f0_base": 1.0,                                # fraction of generated CO2 dissolved at generation (upper bound, untested)
    "f0_sens": 0.5,
    "t_dissolve_base_s": 60.0,
    "t_dissolve_sens_s": 120.0,
}
TEMPS_C = [4.0, 25.0]
VOLS_MAIN = [1.0, 1.5, 2.0]
FINE_STEP = 0.05


# ------------------------------------------------------------ helpers
def bunsen(t_c):
    """Bunsen volumes at 1 atm pure CO2, linear between sourced points."""
    pts = sorted(BUNSEN.items())
    if t_c <= pts[0][0]:
        return pts[0][1]
    if t_c >= pts[-1][0]:
        return pts[-1][1]
    for (t1, v1), (t2, v2) in zip(pts, pts[1:]):
        if t1 <= t_c <= t2:
            return v1 + (v2 - v1) * (t_c - t1) / (t2 - t1)
    raise ValueError("unreachable")


def dose(v_vol):
    """Cube reactant and potassium per 330 ml serving for v_vol volumes generated."""
    n = v_vol * (SERVING_ML / 1000.0) / VM_L
    return {
        "co2_mol_per_330ml": n,
        "khco3_g": n * M_KHCO3,
        "citric_acid_g_stoich": n * CITRIC_PER_CO2 * M_CITRIC,
        "potassium_mg_per_330ml": n * M_K * 1000.0,
    }


def sodium_mg(water_na_mg_per_l, ml):
    """Sodium per serving of ml. The carbonate contributes zero (KHCO3 has no sodium)."""
    return water_na_mg_per_l * ml / 1000.0 + SWEETENER_NA_MG + FLAVOUR_NA_MG


def d_co2(t_c):
    return SA_D0 * ((t_c + T_STD_K) / SA_TS - 1.0) ** SA_M


def kl_at(t_c, kl25):
    """Liquid-side coefficient scaled as sqrt(D) with temperature (penetration-theory scaling, assumed)."""
    return kl25 * math.sqrt(d_co2(t_c) / d_co2(25.0))


def fizz_state(v_vol, t_c, kl25, f0, t_d, t_s):
    """Cumulative gas released (ml STP) and dissolved CO2 (volumes) at t_s seconds after drop."""
    if t_s < t_d:
        return {"released_ml": 0.0, "dissolved_vol": 0.0}
    dt = t_s - t_d
    c_eq = bunsen(t_c) * P_AIR_ATM
    k = kl_at(t_c, kl25) * A_OVER_V                # s^-1
    c0 = f0 * v_vol
    c = c_eq + (c0 - c_eq) * math.exp(-k * dt)     # first-order degassing to headspace equilibrium
    return {"released_ml": (v_vol - c) * SERVING_ML, "dissolved_vol": c}


def no_release_before_dissolution(v_vol, t_c, kl25, f0, t_d):
    """R4: construction check that the model releases nothing before the cube dissolves."""
    checks = [0.0, 0.5 * t_d, t_d - 1.0]
    return all(fizz_state(v_vol, t_c, kl25, f0, t_d, t)["released_ml"] == 0.0 for t in checks)


def evaluate(v_vol, t_c, kl25, f0, t_d, rel_min):
    s2 = fizz_state(v_vol, t_c, kl25, f0, t_d, PASS_RULE["measure_times_s"][0])
    s10 = fizz_state(v_vol, t_c, kl25, f0, t_d, PASS_RULE["measure_times_s"][1])
    r1 = t_d <= PASS_RULE["dissolution_spec_max_s"]
    r2 = s2["released_ml"] >= rel_min
    r3 = s10["dissolved_vol"] >= PASS_RULE["dissolved_floor_vol_at_10min"]
    return {
        "volumes": v_vol,
        "temp_C": t_c,
        "kl_m_per_s": kl_at(t_c, kl25),
        "released_ml_at_2min": round(s2["released_ml"], 2),
        "released_ml_at_10min": round(s10["released_ml"], 2),
        "dissolved_vol_at_2min": round(s2["dissolved_vol"], 3),
        "dissolved_vol_at_10min": round(s10["dissolved_vol"], 3),
        "R1_dissolution_within_spec": r1,
        "R2_release_at_2min_measurable": r2,
        "R3_dissolved_floor_at_10min": r3,
        "pass": bool(r1 and r2 and r3),
    }


def fine_grid():
    n = int(round((2.0 - 1.0) / FINE_STEP))
    return [round(1.0 + FINE_STEP * i, 2) for i in range(n + 1)]


def lowest_passing(kl25, f0, t_d, rel_min):
    for v in fine_grid():
        if all(evaluate(v, t, kl25, f0, t_d, rel_min)["pass"] for t in TEMPS_C):
            return v
    return None


def equilibrium_pco2_atm(v_vol, t_c):
    """Partial pressure of CO2 (atm) needed for equilibrium at v_vol; above 1 means supersaturated in open glass."""
    return v_vol / bunsen(t_c)


# ------------------------------------------------------------ main
def main():
    cb = CALIBRATION
    kl_base = cb["kl25_base_m_per_s"]

    # G1 sodium
    sodium_rows = []
    for label, na_l in WATER_NA_MG_PER_L.items():
        na330 = sodium_mg(na_l, SERVING_ML)
        na200 = sodium_mg(na_l, REF_SERVING_ML)
        sodium_rows.append({
            "water_case": label,
            "water_sodium_mg_per_L": na_l,
            "sodium_mg_per_330ml": round(na330, 3),
            "sodium_mg_per_200ml": round(na200, 3),
            "pass_sodium_free_lt5mg_330ml": na330 < NA_FREE_MG,
            "pass_sodium_free_lt5mg_200ml": na200 < NA_FREE_MG,
        })
    max_water_na_330 = NA_FREE_MG / (SERVING_ML / 1000.0)
    max_water_na_200 = NA_FREE_MG / (REF_SERVING_ML / 1000.0)

    # Fizz, base case and sensitivity
    base_rows = []
    for v in VOLS_MAIN:
        for t in TEMPS_C:
            base_rows.append(evaluate(v, t, kl_base, cb["f0_base"], cb["t_dissolve_base_s"],
                                      PASS_RULE["release_min_ml_at_2min"]))
    v_design = lowest_passing(kl_base, cb["f0_base"], cb["t_dissolve_base_s"], PASS_RULE["release_min_ml_at_2min"])

    sens = []
    for kl_label, kl in [("kl_low", cb["kl25_low_m_per_s"]), ("kl_base", kl_base), ("kl_high", cb["kl25_high_m_per_s"])]:
        for f0_label, f0 in [("f0_base", cb["f0_base"]), ("f0_sens", cb["f0_sens"])]:
            for td_label, td in [("td_base", cb["t_dissolve_base_s"]), ("td_sens", cb["t_dissolve_sens_s"])]:
                for rel in [PASS_RULE["release_min_ml_at_2min"]] + PASS_RULE["sensitivity_release_ml"]:
                    grid_pass = {}
                    for v in VOLS_MAIN:
                        grid_pass["%.1f" % v] = all(
                            evaluate(v, t, kl, f0, td, rel)["pass"] for t in TEMPS_C)
                    sens.append({
                        "kl_case": kl_label,
                        "f0_case": f0_label,
                        "dissolution_case": td_label,
                        "release_min_ml": rel,
                        "pass_at_1.0_1.5_2.0_both_temps": grid_pass,
                        "lowest_passing_vol_fine_grid": lowest_passing(kl, f0, td, rel),
                    })

    # R4 construction check
    r4 = all(no_release_before_dissolution(v, t, kl_base, cb["f0_base"], cb["t_dissolve_base_s"])
             for v in VOLS_MAIN for t in TEMPS_C)

    # G2 verdict is set by the calibration spread: any calibration case without a passing dose on the grid
    base_only = [s for s in sens if s["kl_case"] == "kl_base" and s["f0_case"] == "f0_base"
                 and s["dissolution_case"] == "td_base" and s["release_min_ml"] == PASS_RULE["release_min_ml_at_2min"]][0]
    low_only = [s for s in sens if s["kl_case"] == "kl_low" and s["f0_case"] == "f0_base"
                and s["dissolution_case"] == "td_base" and s["release_min_ml"] == PASS_RULE["release_min_ml_at_2min"]][0]
    high_only = [s for s in sens if s["kl_case"] == "kl_high" and s["f0_case"] == "f0_base"
                 and s["dissolution_case"] == "td_base" and s["release_min_ml"] == PASS_RULE["release_min_ml_at_2min"]][0]
    g2_resolution = "stated_limit" if low_only["lowest_passing_vol_fine_grid"] is None else "resolved_with_design_change"

    # G3 potassium at the design dose and at the grid
    pot_rows = []
    for v in sorted(set(VOLS_MAIN + [v_design])):
        d = dose(v)
        k330 = d["potassium_mg_per_330ml"]
        k200 = k330 * REF_SERVING_ML / SERVING_ML
        pot_rows.append({
            "volumes": v,
            "co2_mol_per_330ml": round(d["co2_mol_per_330ml"], 5),
            "khco3_g_per_330ml": round(d["khco3_g"], 3),
            "citric_acid_g_per_330ml": round(d["citric_acid_g_stoich"], 3),
            "potassium_mg_per_330ml": round(k330, 1),
            "potassium_pct_RDI_330ml_3500": round(100.0 * k330 / RDI_K_MG, 1),
            "potassium_pct_RDI_330ml_2000_alt": round(100.0 * k330 / RDI_K_ALT_MG, 1),
            "potassium_mg_per_200ml_reference": round(k200, 1),
            "potassium_pct_RDI_200ml_3500": round(100.0 * k200 / RDI_K_MG, 1),
            "good_source_flag_gt15pct_330ml": 100.0 * k330 / RDI_K_MG > K_GOOD_PCT,
            "high_flag_ge30pct_330ml": 100.0 * k330 / RDI_K_MG >= K_HIGH_PCT,
            "claim_made": False,
            "label_declaration": "potassium declared on the nutrition panel as a fact (secondary source: mandatory)",
        })
    d_design = dose(v_design) if v_design is not None else None

    g1_resolution = "resolved_with_design_change"
    g1_basis = ("Carbonate contributes 0 mg sodium (KHCO3). With base water at 5 mg per litre (specification, not "
                "a Thai label value), sodium is %.2f mg per 330 ml and %.2f mg per 200 ml, below 5 mg on both bases. "
                "Passes only if base water is at or below %.2f mg per litre (330 ml basis). A 20 mg per litre water "
                "fails. Design change: water specification and a sodium-free intensive sweetener. Calculation only; "
                "the Thai 5 mg threshold stays conflicted in rework/44." % (
                    sodium_mg(5.0, SERVING_ML), sodium_mg(5.0, REF_SERVING_ML), max_water_na_330))

    g2_basis = ("Calibration parameter, not measured: k_L25 base 2e-5 m/s (no sourced value; derived bracket "
                "6e-6 to 2e-5 m/s, sensitivity 5e-6 to 1e-4). Base case: lowest dose passing both temperatures is %s "
                "volumes (design dose). Low calibration (5e-6 m/s): no dose up to 2.0 passes. High calibration: lowest "
                "pass %s. Retained-fizz check (R3) binds at high calibration; release check (R2) can be met by bubbles "
                "that do not stay in the drink (f0 0.5 case). Dissolution time (60 s) is an untested design spec; at "
                "120 s no release is measured at 2 min. Open-glass equilibrium needs %.2f atm at 2.0 volumes, 25 C, so "
                "the drink is supersaturated; the fizz gate is kinetic. Stated limit until a measured k_L or a "
                "comparable beverage record exists." % (
                    v_design, high_only["lowest_passing_vol_fine_grid"], equilibrium_pco2_atm(2.0, 25.0)))

    g3_resolution = "resolved_with_design_change"
    g3_basis = ("Design: lowest carbonate dose that passes the base-case fizz rule, %s volumes, gives %s mg potassium "
                "per 330 ml (%s percent of the Thai RDI of 3500 mg, not reconfirmed). Potassium declared on the panel "
                "as a fact; no potassium claim. Medical question NOT resolved by this simulation: safety for people "
                "with reduced potassium excretion or on potassium-retaining medicines needs a medical reviewer. "
                "Acesulfame potassium (if used as sweetener) adds potassium, unquantified here." % (
                    v_design,
                    round(d_design["potassium_mg_per_330ml"], 1) if d_design else "none",
                    round(100.0 * d_design["potassium_mg_per_330ml"] / RDI_K_MG, 1) if d_design else "none"))

    gate_verdicts = [
        {"gate": "G1 sodium-free", "resolution": g1_resolution, "basis": g1_basis},
        {"gate": "G2 fizz", "resolution": g2_resolution, "basis": g2_basis},
        {"gate": "G3 potassium", "resolution": g3_resolution, "basis": g3_basis},
    ]

    open_items = [
        "Thai bottled-water sodium label value not found; base water sodium is a specification (5 mg per litre).",
        "Degassing coefficient k_L not sourced; treated as a calibration parameter with a 2e-5 m/s base and a 5e-6 to 1e-4 m/s bracket.",
        "Fraction of generated CO2 dissolved at generation (f0) and cube dissolution time are untested; the fizz result depends on both.",
        "Thai potassium RDI (3500 mg) from the earlier repo read; not reconfirmed; a Codex-NRV-based value may differ.",
        "Thai sodium-free threshold (5 mg per serving) read from the English text only; conflicts with the US values flagged in rework/44.",
        "Medical potassium safety is not resolved by physics; needs a medical reviewer and a stated label wording.",
        "Acesulfame potassium or other potassium-containing sweeteners would add potassium; not quantified.",
        ("Conversion test (men 25-34 against men 35-44, rework/46): design confirmed as pended. It needs a panel, which is "
         "outside contact and needs approval; not run here. rework/47 finds ratio A has a 0.94 probability of being "
         "ahead, with a 90 percent interval of 1.00 to 1.09, from the age gradient alone, and no survey source for the "
         "25-34 against 35-44 split (rework/47 section 7). The conversion lead stays an estimate."),
    ]

    limits = [
        "No Thai bottled-water sodium label found (two searches, 2026-10-18). Water sodium is set as a specification.",
        "No sourced surface degassing coefficient for a beverage found; the screen treats it as a calibration parameter.",
        "The cube dissolution time and the dissolved fraction at generation are assumed; no measurement is available in this run.",
        "The Thai potassium RDI and the sodium-free threshold were not reconfirmed on the Thai primary text in this run.",
        "No medical safety conclusion is drawn from the potassium figures.",
    ]

    results = {
        "meta": {
            "screen": "final_gate_sim.py",
            "product": "sodium-free potassium-bicarbonate lime fizz cube, 330 ml serving, Thailand domestic",
            "read_date": READ_DATE,
            "claim_policy": ("No sugar claim of any kind. Sweetness is disclosed as an intensive sweetener. "
                             "No sodium-free claim is made unless G1 passes on the stated water specification."),
            "method": ("Stoichiometry for potassium; first-order degassing mass balance for fizz; calculation for "
                       "sodium. Replaces the bench and medical tests per team decision of 18 October 2026."),
            "public_info_only": True,
        },
        "sources": SOURCES,
        "pass_rule_fixed_before_run": PASS_RULE,
        "calibration": CALIBRATION,
        "constants": {
            "R_GAS": R_GAS, "T_std_K": T_STD_K, "P_std_Pa": P_STD_PA,
            "molar_volume_L_per_mol": round(VM_L, 4),
            "M_KHCO3": M_KHCO3, "M_K_derived": round(M_K, 3), "M_citric": M_CITRIC,
            "A_over_V_m_inv": A_OVER_V, "P_air_atm_assumed": P_AIR_ATM,
            "SA_D0": SA_D0, "SA_Ts": SA_TS, "SA_m": SA_M,
            "D_CO2_25C_m2_s": d_co2(25.0), "D_CO2_4C_m2_s": d_co2(4.0),
            "kl_ratio_4C_over_25C": round(kl_at(4.0, 1.0) / kl_at(25.0, 1.0), 4),
            "Thai_RDI_potassium_mg_sourced_not_reconfirmed": RDI_K_MG,
            "Thai_NA_free_threshold_mg": NA_FREE_MG,
        },
        "G1_sodium": {
            "carbonate_sodium_mg": 0.0,
            "sweetener_sodium_mg_assumed": SWEETENER_NA_MG,
            "flavour_sodium_mg_assumed": FLAVOUR_NA_MG,
            "rows": sodium_rows,
            "max_water_sodium_mg_per_L_for_pass_330ml": round(max_water_na_330, 2),
            "max_water_sodium_mg_per_L_for_pass_200ml": round(max_water_na_200, 2),
        },
        "G2_fizz": {
            "base_case": {"kl25_m_per_s": kl_base, "f0": cb["f0_base"], "t_dissolve_s": cb["t_dissolve_base_s"],
                          "release_min_ml_at_2min": PASS_RULE["release_min_ml_at_2min"]},
            "rows_base": base_rows,
            "design_dose_lowest_passing_base_vol": v_design,
            "R4_no_release_before_dissolution_checked": r4,
            "sensitivity": sens,
            "equilibrium_pco2_atm_needed": dict(
                [("%.1f_vol_4C" % v, round(equilibrium_pco2_atm(v, 4.0), 3)) for v in VOLS_MAIN]
                + [("%.1f_vol_25C" % v, round(equilibrium_pco2_atm(v, 25.0), 3)) for v in VOLS_MAIN]),
            "interpretation": ("R2 counts gas that leaves the drink at generation as release, so a low f0 can pass "
                               "R2 while the drink is flat. R3 (dissolved CO2 at 10 min) is the retained-fizz check."),
        },
        "G3_potassium": {
            "rows": pot_rows,
            "design_dose_volumes": v_design,
            "design_potassium_mg_per_330ml": round(d_design["potassium_mg_per_330ml"], 1) if d_design else None,
            "claim_policy": "no potassium claim; potassium declared as a fact; medical question stated as a limit",
        },
        "gate_verdicts": gate_verdicts,
        "open_items": open_items,
        "limits": limits,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)

    # summary
    print("Final gate simulation (sodium-free KHCO3 lime fizz cube, 330 ml)")
    print("G1 sodium per 330 ml, carbonate 0 mg; water 5 mg/L -> %.2f mg; 20 mg/L -> %.2f mg" % (
        sodium_mg(5.0, SERVING_ML), sodium_mg(20.0, SERVING_ML)))
    print("G1 max water Na for pass (330 ml basis): %.2f mg/L" % max_water_na_330)
    print("G2 base case (k_L25 %.1e m/s, f0 %.1f, dissolution %.0f s)" % (kl_base, cb["f0_base"], cb["t_dissolve_base_s"]))
    for r in base_rows:
        print("   V %.1f T %4.1f C  release 2min %6.2f ml  10min %6.2f ml  dissolved10 %5.3f vol  pass %s" % (
            r["volumes"], r["temp_C"], r["released_ml_at_2min"], r["released_ml_at_10min"],
            r["dissolved_vol_at_10min"], r["pass"]))
    print("G2 design dose (lowest passing base, fine grid): %s vol" % v_design)
    print("G2 low-k lowest passing: %s; high-k lowest passing: %s" % (
        low_only["lowest_passing_vol_fine_grid"], high_only["lowest_passing_vol_fine_grid"]))
    print("G2 R4 construction check: %s" % r4)
    for r in pot_rows:
        print("G3 V %.2f  K %.1f mg per 330 ml  %.1f pct RDI 3500  (200 ml %.1f mg)" % (
            r["volumes"], r["potassium_mg_per_330ml"], r["potassium_pct_RDI_330ml_3500"],
            r["potassium_mg_per_200ml_reference"]))
    for g in gate_verdicts:
        print("VERDICT %s: %s" % (g["gate"], g["resolution"]))
    print("Wrote %s" % OUT_PATH)


if __name__ == "__main__":
    main()
