"""Taste chemistry model for the Singha Lemon Soda Cube (T8 part a).

Chemistry only. No sensory result is claimed. Standard library only.
Run with: python -I cube_chemistry_taste.py
Writes cube_chemistry_taste_results.json next to this file.

Method
- Equilibrium pH by charge balance. Citric acid pK 3.128, 4.761, 6.396 at 298.15 K and I = 0
  (Goldberg et al. 2002, Table 7.22, tier P), moved to other temperatures with the Goldberg form
  ln K(T) = ln K0 + (dH0 - dCp T0)/R (1/T0 - 1/T) + (dCp/R) ln(T/T0).
- Carbonic acid apparent pK1 6.351 and pK2 10.329 (Wikipedia potassium bicarbonate, tier S).
  No temperature shift is sourced, so none is applied (ASSUMPTION).
- Activities: Davies equation, log10 gamma_z = -A z^2 (sqrt(I)/(1 + sqrt(I)) - 0.3 I), A = 0.5 (form
  printed on the Wikipedia Davies page, tier S). Ionic strength from all ions, solved by iteration.
- pH is the operational (activity) pH, pH = -log10 a_H, which is what a pH meter reads and what Barac et al.
  report for Sprite. The acid constants in terms of species concentrations then follow from the
  thermodynamic constant Ka = a_H a_A / a_HA:  K'a = a_H [A] / [HA] = Ka gamma_HA / gamma_A, so
      pK'a = pKa + log10 gamma_A - log10 gamma_HA.
  The anion is more highly charged than the acid, so log gamma_A < log gamma_HA and the apparent pK FALLS as
  the ionic strength rises. (An earlier version of this script had the opposite sign; the unit checks below now
  stop the script if the sign is wrong.) The hydrogen ion concentration in the charge balance is
  [H+] = a_H / gamma_H.
- Titratable acidity: mmol/L of base to move the drink from its pH to a target pH. Two treatments of the
  ionic strength are computed: constant at the starting value (start_I) and iterated at the end point with
  the added sodium counted (end_I; the headline; the iterated end point ionic strength is 0.13 to 0.22 mol/L).
- Sweetness: sucralose potency 600 central, 400 and 700 range (Wiet and Beyts 1992 abstract, S).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cube_chemistry_taste_results.json")

R_GAS = 8.314462618          # J/(mol K), CONSTANT (SI exact)
T0 = 298.15                  # K, reference temperature of the Goldberg table
PKW = 14.0                   # CONSTANT at 25 C; Kw temperature effect is negligible at pH 2 to 8
DAVIES_A = 0.5               # S form (0.5 z^2), temperature independence ASSUMPTION; sensitivity 0.49 to 0.53

# ---------------- inputs (value, tier, status) ----------------
MW_KHCO3 = 100.115           # g/mol, S (Wikipedia potassium bicarbonate, read 2026-10-20)
MW_CITRIC = 192.124          # g/mol, S (Wikipedia citric acid, printed 192.123)
MW_K = 39.098               # g/mol, CONSTANT (standard atomic weight, not opened)
MW_CO2 = 44.01               # g/mol, CONSTANT
MW_SUCRALOSE = 397.63        # g/mol, S (Wikipedia sucralose)
MOLAR_VOL_STP = 22.414       # L/mol at 0 C and 1 atm, CONSTANT (standard definition)

PK_CIT = (3.128, 4.761, 6.396)          # P, Goldberg 2002 Table 7.22
DH_CIT = (4070.0, 2230.0, -3380.0)      # J/mol, P, same table
DCP_CIT = (-131.0, -178.0, -254.0)      # J/(K mol), P, same table
PK_CARB = (6.351, 10.329)               # S, Wikipedia potassium bicarbonate (apparent, 25 C)

KHCO3_G = 0.81               # design input (deck slide 7 and handover)
CITRIC_G = 2.10              # design input (handover; the design basis pH 3.5)
SUCRALOSE_MG = 33.0          # design input today; the team proposes 55 mg (this model)
SERVE_L = 0.330              # design, serve volume
DOSE_VOL = 0.55              # design CO2 dose, volumes per serve
POTENCY = {"low": 400.0, "central": 600.0, "high": 700.0}   # S (Wiet and Beyts 1992 abstract; Wikipedia 600)
SUCRALOSE_LIMIT_MG_PER_KG = 300.0   # via submission 09 (P, SOURCED there; Thai notification condition 127; not re-read here)
PROPOSED_SUCRALOSE_MG = 55.0        # DERIVED below: matches 10 g sugar equivalent per 100 mL at potency 600

# Benchmarks (as recorded in rework/raw/diligence_2026-10-20/T8/)
SPRITE_PH = 2.71             # P, Barac et al. 2023 Table 2 (Serbian bottling)
SPRITE_TA55_ML = 1.87        # P, same table, mL of 0.9613 M NaOH per 50 mL to pH 5.5
SPRITE_TA70_ML = 2.85        # P, same table, to pH 7.0
NAOH_M = 0.9613              # P, same paper
TA_SAMPLE_ML = 50.0          # P, same paper
SPRITE_BRIX = 10.0           # S, Ali et al. 2022 abstract (Peshawar), g sugar per 100 mL
SPRITE_SUGAR_INDIA = 11.7    # P, Coca-Cola India brand page, total sugars g per 100 mL
SPRITE_SUGAR_HK = 8.6        # P, Coca-Cola Hong Kong brand page (read earlier on 2026-10-20; not re-opened)
SPRITE_CITRIC_GL = 1.1968    # S, Ali et al. 2022 abstract, citric acid 1196.8 mg/L
SPRITE_CO2_VOL = 3.80        # S, Ali et al. 2022 abstract, CO2 gas volume (Sprite)
SEVENUP_BRIX = 10.7          # S, Ali et al. 2022 abstract
SEVENUP_CITRIC_GL = 1.4592   # S, Ali et al. 2022 abstract, 1459.2 mg/L
SEVENUP_CO2_VOL = 3.70       # S, Ali et al. 2022 abstract
BANGLA_PH_RANGE = (3.2, 4.0) # S, Sarwar et al. abstract (five Bangladeshi brands)
PATENT_LEMONLIME_PH = 3.55   # P (patent US 7,572,471 example 2, syrup basis), PROXY

# Thresholds (detection, taste and bite)
KCL_DETECT_MM = 2.42         # S, Schiffman et al. 1995 record (mean detection threshold, KCl, salt molarity)
KCIT_DETECT_MM = 0.300       # S, same record, potassium citrate (salt form not stated in the abstract)
KCARB_DETECT_MM = 2.86       # S, same record, potassium carbonate
CITRIC_SOUR_DETECT_GL = (0.057, 0.082)  # S, Mao et al. 2022 abstract, in sucrose solutions
CITRIC_SOUR_STOCK_DI_GL = 0.12          # S, Hoehl et al. 2014: the stock concentration of the most dilute group C in deionized water. It is
                                        # NOT a threshold (thresholds are in log micromol); sour detection occurs below it, so ratios to it are LOWER bounds
TORRICO_BITTER_G_100ML = (0.0242, 0.0586)  # S, Torrico et al. 2015 abstract: bitterness recognition of caffeine and KCl COMBINED in solution (not separable)
MW_KCL = 74.55               # g/mol, CONSTANT (K 39.098 + Cl 35.45)
BITE_NO_DIFF_CO2_GL = 1.2    # S, McMahon et al. 2017 abstract: 1.2 g/L did not differ from the 0 g/L control (wine PROXY)
BITE_DIFF_CO2_GL = 2.0       # S, same abstract: differences significant from 2.0 g/L (carbonation, burn, tingly); bite from 2.8 g/L (2016 poster)
BITE_POSTER_GL = 2.8         # S, McMahon et al. 2016 poster (trained panel): bite first differs at 2.8 g/L
RISK_RATIO_SOUR = 1.2        # ASSUMPTION of the flag rule: buffered acidity above 1.2 times Sprite
RISK_RATIO_SWEET = 0.8       # ASSUMPTION of the flag rule: sweetness to acid ratio below 0.8 times Sprite


def pk_at_T(pk0, dh, dcp, t_c):
    """Goldberg relation (2002): pK at t_c (C) from the 298.15 K value."""
    T = t_c + 273.15
    lnratio = (dh - dcp * T0) / R_GAS * (1.0 / T0 - 1.0 / T) + dcp / R_GAS * math.log(T / T0)
    return pk0 - lnratio / math.log(10.0)


def log_gamma(z, ionic_strength):
    """Davies activity coefficient (log10) for an ion of charge magnitude z."""
    s = math.sqrt(ionic_strength)
    return -DAVIES_A * z * z * (s / (1.0 + s) - 0.3 * ionic_strength)


def apparent_constants(t_c, ionic):
    """Apparent pKs for operational (activity) pH: pK'a = pKa + log gamma_A - log gamma_HA."""
    pk_c = [pk_at_T(PK_CIT[i], DH_CIT[i], DCP_CIT[i], t_c) for i in range(3)]
    g_cit = [log_gamma(z, ionic) for z in (0, 1, 2, 3)]
    g_carb = [log_gamma(z, ionic) for z in (0, 1, 2)]
    pka_app = [
        pk_c[0] + (g_cit[1] - g_cit[0]),
        pk_c[1] + (g_cit[2] - g_cit[1]),
        pk_c[2] + (g_cit[3] - g_cit[2]),
    ]
    pkc_app = [
        PK_CARB[0] + (g_carb[1] - g_carb[0]),
        PK_CARB[1] + (g_carb[2] - g_carb[1]),
    ]
    return pka_app, pkc_app


def charge_terms(ph, cit_m, co2_m, pka_app, pkc_app, ionic):
    """Anion charge magnitude (M) and species at operational pH ph, for the given apparent constants."""
    K1, K2, K3 = (10.0 ** -p for p in pka_app)
    C1, C2 = (10.0 ** -p for p in pkc_app)
    a_h = 10.0 ** -ph
    g1 = 10.0 ** log_gamma(1, ionic)            # gamma of H+ (and OH-)
    h_conc = a_h / g1
    d = a_h ** 3 + K1 * a_h ** 2 + K1 * K2 * a_h + K1 * K2 * K3
    f = [a_h ** 3 / d, K1 * a_h ** 2 / d, K1 * K2 * a_h / d, K1 * K2 * K3 / d]
    q_cit = cit_m * (K1 * a_h ** 2 + 2 * K1 * K2 * a_h + 3 * K1 * K2 * K3) / d
    dc = a_h * a_h + C1 * a_h + C1 * C2
    q_carb = co2_m * (C1 * a_h + 2 * C1 * C2) / dc
    hco3 = co2_m * C1 * a_h / dc
    co3 = co2_m * C1 * C2 / dc
    h2co3 = co2_m * a_h * a_h / dc
    oh = 10.0 ** -PKW / (a_h * g1)
    return {"h": h_conc, "a_h": a_h, "oh": oh, "f": f, "q_cit": q_cit, "q_carb": q_carb,
            "hco3": hco3, "co3": co3, "h2co3": h2co3, "q": q_cit + q_carb + oh}


def solve_ph(k_m, cit_m, co2_m, pka_app, pkc_app, ionic):
    def resid(ph):
        t = charge_terms(ph, cit_m, co2_m, pka_app, pkc_app, ionic)
        return k_m + t["h"] - t["q"]

    lo, hi = 1.0, 11.0
    flo, fhi = resid(lo), resid(hi)
    if flo * fhi > 0:
        raise ValueError("no pH root between 1 and 11")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = resid(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def ionic_from(k_m, t, cit_m, na_m=0.0):
    cit_sp = [cit_m * x for x in t["f"]]
    return 0.5 * (k_m + na_m + t["h"] + t["oh"] + t["hco3"] + 4 * t["co3"]
                  + cit_sp[1] * 1 + cit_sp[2] * 4 + cit_sp[3] * 9)


def speciate(t_c, k_m, cit_m, co2_m):
    """pH and species by charge balance with Davies activities; ionic strength iterated."""
    ionic = 0.5 * (k_m + 2 * cit_m + co2_m)
    ph = None
    for _ in range(300):
        pka_app, pkc_app = apparent_constants(t_c, ionic)
        ph = solve_ph(k_m, cit_m, co2_m, pka_app, pkc_app, ionic)
        t = charge_terms(ph, cit_m, co2_m, pka_app, pkc_app, ionic)
        i_new = ionic_from(k_m, t, cit_m)
        if abs(i_new - ionic) < 1e-10:
            ionic = i_new
            break
        ionic = 0.5 * (ionic + i_new)
    pka_app, pkc_app = apparent_constants(t_c, ionic)
    ph = solve_ph(k_m, cit_m, co2_m, pka_app, pkc_app, ionic)
    t = charge_terms(ph, cit_m, co2_m, pka_app, pkc_app, ionic)
    resid = k_m + t["h"] - t["q"]
    return {
        "pH": ph, "ionic_strength_M": ionic, "h_mM": t["h"] * 1000.0,
        "pKa_app_citric": pka_app, "pKa_app_carbonic": pkc_app,
        "charge_balance_residual_M": resid,
        "citric_species_mM": {"H3L": t["f"][0] * cit_m * 1000, "H2L-": t["f"][1] * cit_m * 1000,
                              "HL2-": t["f"][2] * cit_m * 1000, "L3-": t["f"][3] * cit_m * 1000},
        "carbonate_mM": {"HCO3-": t["hco3"] * 1000, "CO3_2-": t["co3"] * 1000,
                         "H2CO3_dissolved": t["h2co3"] * 1000},
        "anion_charge_mM": t["q"] * 1000.0,
    }


def titratable_acidity(t_c, k_m, cit_m, co2_m, target_ph, mode="end_I"):
    """mmol/L of monovalent base (Na+) from the sample pH to target_ph.

    start_I: apparent constants frozen at the starting ionic strength, B = (Q_t - Q_0) + H_0 - H_t.
    end_I: ionic strength iterated at the end point with the added sodium counted, B = Q_t - K - H_t.
    """
    s0 = speciate(t_c, k_m, cit_m, co2_m)
    ionic0 = s0["ionic_strength_M"]
    if mode == "start_I":
        pka_app, pkc_app = s0["pKa_app_citric"], s0["pKa_app_carbonic"]
        t0 = charge_terms(s0["pH"], cit_m, co2_m, pka_app, pkc_app, ionic0)
        tt = charge_terms(target_ph, cit_m, co2_m, pka_app, pkc_app, ionic0)
        return ((tt["q"] - t0["q"]) + t0["h"] - tt["h"]) * 1000.0
    ionic = ionic0
    na = 0.0
    for _ in range(300):
        pka_app, pkc_app = apparent_constants(t_c, ionic)
        tt = charge_terms(target_ph, cit_m, co2_m, pka_app, pkc_app, ionic)
        na = tt["q"] - k_m - tt["h"]
        i_new = ionic_from(k_m, tt, cit_m, na_m=na)
        if abs(i_new - ionic) < 1e-10:
            ionic = i_new
            break
        ionic = 0.5 * (ionic + i_new)
    return na * 1000.0, ionic


def recipe_concentrations(khco3_g=KHCO3_G, citric_g=CITRIC_G, serve_l=SERVE_L, retained=True):
    """Molar totals in the serve. CO2 generated equals KHCO3 moles (1:1)."""
    k_m = khco3_g / MW_KHCO3 / serve_l
    cit_m = citric_g / MW_CITRIC / serve_l
    co2_m = (khco3_g / MW_KHCO3 / serve_l) if retained else 0.0
    return k_m, cit_m, co2_m


def citric_stoich_g(khco3_g):
    """Citric acid needed to take all the CO2 out of KHCO3 (1 citric per 3 bicarbonate)."""
    return khco3_g / MW_KHCO3 / 3.0 * MW_CITRIC


def sweetness(sucralose_mg, potency, serve_l=SERVE_L):
    """Sucrose-equivalent grams per 100 mL."""
    return (sucralose_mg / 1000.0) * potency / (serve_l * 1000.0) * 100.0


def sprite_ta(ml):
    return ml * NAOH_M / TA_SAMPLE_ML * 1000.0


def ta7(t_c, kk, cc, co, mode="end_I"):
    r = titratable_acidity(t_c, kk, cc, co, 7.0, mode)
    return r[0] if isinstance(r, tuple) else r


def unit_checks():
    """Checks that stop the script if the activity treatment has the wrong sign or the solver is off."""
    global DAVIES_A
    checks = {}
    keep = DAVIES_A
    try:
        DAVIES_A = 0.5
        p0, _ = apparent_constants(25.0, 1e-12)
        p26, _ = apparent_constants(25.0, 0.026)
        p100, _ = apparent_constants(25.0, 0.100)
        checks["apparent_pK_at_I_0_equals_Goldberg_25C"] = all(abs(p0[i] - PK_CIT[i]) < 1e-3 for i in range(3))
        checks["apparent_pK_falls_as_I_rises_all_three"] = all(p100[i] < p26[i] < p0[i] for i in range(3))
        checks["pK3_apparent_at_I_0.1"] = round(p100[2], 3)
        checks["pK3_apparent_at_I_0.1_between_5.7_and_6.0"] = bool(5.7 < p100[2] < 6.0)
        checks["pK1_apparent_at_I_0.026"] = round(p26[0], 3)
        checks["pK2_apparent_at_I_0.026"] = round(p26[1], 3)
        checks["pK3_apparent_at_I_0.026"] = round(p26[2], 3)
        checks["gamma_below_one_and_falls_with_charge"] = bool(log_gamma(1, 0.026) > log_gamma(2, 0.026) > log_gamma(3, 0.026))
        kk, cc, co = recipe_concentrations()
        s = speciate(20.0, kk, cc, co)
        checks["charge_balance_residual_below_1e-9_M"] = bool(abs(s["charge_balance_residual_M"]) < 1e-9)
        DAVIES_A = 0.0
        s0 = speciate(25.0, kk, cc, co)
        checks["pH_ideal_solution_25C_2.10g"] = round(s0["pH"], 3)
        checks["ideal_pH_matches_design_basis_3.5_within_0.02"] = bool(abs(s0["pH"] - 3.5) < 0.02)
    finally:
        DAVIES_A = keep
    for k, v in checks.items():
        if isinstance(v, bool) and not v:
            raise AssertionError("unit check failed: " + k)
    return checks


def main():
    global DAVIES_A
    checks = unit_checks()
    out = {
        "task": "T8 part a, taste chemistry model (no sensory result claimed)",
        "date": "2026-10-20",
        "status": "desk chemistry model; no sensory data; no taste result is claimed",
        "revision_note": ("Revised 2026-10-20: the Davies activity correction had the wrong sign "
                          "(apparent pKs rose with ionic strength); corrected to pK' = pK + log gamma_A - log gamma_HA, "
                          "unit checks added, titration end point ionic strength iterated, benchmark CO2 added. "
                          "Second revision 2026-10-20: Sprite acid basis from a citric acid assay added, potassium bitterness range added, "
                          "citric acid needed for pH 3.0 and 3.5 at 20 and 25 C added."),
        "unit_checks": checks,
        "inputs": {
            "KHCO3_g": {"value": KHCO3_G, "tier": "design (deck slide 7, handover)"},
            "citric_total_g": {"value": CITRIC_G, "tier": "design (handover; the working pH 3.5 basis)"},
            "sucralose_mg_today": {"value": SUCRALOSE_MG, "tier": "design today; DERIVED (6 g per 100 mL over 600)"},
            "sucralose_mg_proposed": {"value": PROPOSED_SUCRALOSE_MG, "tier": "DERIVED here (10 g per 100 mL over 600), the team proposal"},
            "serve_L": {"value": SERVE_L, "tier": "design"},
            "CO2_dose_volumes": {"value": DOSE_VOL, "tier": "design (ASSUMPTION of the deck)"},
            "pKa_citric_25C_I0": {"value": list(PK_CIT), "tier": "P, Goldberg et al. 2002 Table 7.22 (read in the PDF image 2026-10-20)"},
            "dH_citric_J_mol": {"value": list(DH_CIT), "tier": "P, same table"},
            "dCp_citric_J_K_mol": {"value": list(DCP_CIT), "tier": "P, same table"},
            "pK_carbonic_25C": {"value": list(PK_CARB), "tier": "S, Wikipedia potassium bicarbonate (read 2026-10-20)"},
            "carbonic_T_shift": {"value": "none", "tier": "ASSUMPTION (no sourced shift)"},
            "Davies_A": {"value": DAVIES_A, "tier": "S form (Wikipedia Davies page, constant 0.5); T independence ASSUMPTION"},
            "MW_KHCO3": {"value": MW_KHCO3, "tier": "S, Wikipedia"},
            "MW_citric": {"value": MW_CITRIC, "tier": "S, Wikipedia"},
            "MW_K": {"value": MW_K, "tier": "CONSTANT (standard atomic weight, not opened)"},
            "MW_sucralose": {"value": MW_SUCRALOSE, "tier": "S, Wikipedia"},
            "sucralose_potency": {"value": POTENCY, "tier": "S, Wiet and Beyts 1992 abstract (400 to 700); 600 from Wikipedia and EFSA news summary"},
            "sucralose_limit_mg_per_kg": {"value": SUCRALOSE_LIMIT_MG_PER_KG, "tier": "P, via submission 09 (P, SOURCED there); not re-read in this task; sub-category rows unread"},
        },
        "benchmarks": {
            "Sprite_pH": {"value": SPRITE_PH, "tier": "P, Barac et al. 2023 Table 2 (Serbian bottling, one bottling)"},
            "Sprite_TA_to_5.5_mmol_L": {"value": round(sprite_ta(SPRITE_TA55_ML), 2), "tier": "DERIVED from P (0.9613 M NaOH, 50 mL)"},
            "Sprite_TA_to_7.0_mmol_L": {"value": round(sprite_ta(SPRITE_TA70_ML), 2), "tier": "DERIVED from P"},
            "Sprite_sugar_g_100mL_Brix": {"value": SPRITE_BRIX, "tier": "S, Ali et al. 2022 (journal page opened 2026-10-20; Brix)"},
            "Sprite_sugar_g_100mL_India": {"value": SPRITE_SUGAR_INDIA, "tier": "P, Coca-Cola India brand page (read 2026-10-20 and read again on the same day)"},
            "Sprite_sugar_g_100mL_HK": {"value": SPRITE_SUGAR_HK, "tier": "P, Coca-Cola Hong Kong brand page (read once on 2026-10-20 and not re-verified)"},
            "Sprite_citric_g_L": {"value": SPRITE_CITRIC_GL, "tier": "S, Ali et al. 2022"},
            "Sprite_CO2_gas_volumes": {"value": SPRITE_CO2_VOL, "tier": "S, Ali et al. 2022"},
            "7Up_Brix": {"value": SEVENUP_BRIX, "tier": "S, Ali et al. 2022"},
            "7Up_citric_g_L": {"value": SEVENUP_CITRIC_GL, "tier": "S, Ali et al. 2022"},
            "7Up_CO2_gas_volumes": {"value": SEVENUP_CO2_VOL, "tier": "S, Ali et al. 2022"},
            "Bangladesh_pH_range": {"value": list(BANGLA_PH_RANGE), "tier": "S, Sarwar et al. abstract"},
            "lemon_lime_patent_pH": {"value": PATENT_LEMONLIME_PH, "tier": "P (patent), PROXY (syrup basis)"},
        },
        "thresholds": {
            "KCl_detection_mM": {"value": KCL_DETECT_MM, "tier": "S, Schiffman et al. 1995 record (detection only; salt molarity)"},
            "potassium_citrate_detection_mM": {"value": KCIT_DETECT_MM, "tier": "S, same record (salt form not stated)"},
            "potassium_carbonate_detection_mM": {"value": KCARB_DETECT_MM, "tier": "S, same record"},
            "citric_sour_detection_g_L_sucrose": {"value": list(CITRIC_SOUR_DETECT_GL), "tier": "S, Mao et al. 2022 abstract"},
            "citric_sour_stock_group_C_deionized_g_L": {"value": CITRIC_SOUR_STOCK_DI_GL, "tier": "S, Hoehl et al. 2014: stock concentration of the most dilute group, NOT a threshold; detection occurs below it"},
            "bitterness_recognition_caffeine_and_KCl_combined_g_100mL": {"value": list(TORRICO_BITTER_G_100ML), "tier": "S, Torrico et al. 2015 abstract (water; caffeine and KCl not separated; PROXY for potassium bicarbonate and citrate in a drink)"},
            "CO2_no_mouthfeel_difference_g_L": {"value": BITE_NO_DIFF_CO2_GL, "tier": "S, McMahon et al. 2017 abstract (wine PROXY): 1.2 g/L did not differ from the control"},
            "CO2_mouthfeel_difference_from_g_L": {"value": BITE_DIFF_CO2_GL, "tier": "S, same abstract (wine PROXY): differences from 2.0 g/L"},
            "CO2_bite_difference_from_g_L_trained_panel": {"value": BITE_POSTER_GL, "tier": "S, McMahon et al. 2016 poster (trained panel, wine PROXY)"},
        },
    }

    # 1. Stoichiometry and dose
    co2_mmol = KHCO3_G / MW_KHCO3 * 1000.0
    k_mM = KHCO3_G / MW_KHCO3 / SERVE_L * 1000.0
    cit_free_g = CITRIC_G - citric_stoich_g(KHCO3_G)
    co2_gL = co2_mmol / 1000.0 * MW_CO2 / SERVE_L
    sprite_co2_gL = SPRITE_CO2_VOL / MOLAR_VOL_STP * MW_CO2
    out["recipe_stoichiometry"] = {
        "CO2_mmol_per_serve": round(co2_mmol, 3),
        "CO2_volumes_STP_per_serve_basis": round(co2_mmol / 1000.0 * MOLAR_VOL_STP / SERVE_L, 4),
        "CO2_g_per_L_from_0.81_g_KHCO3": round(co2_gL, 4),
        "CO2_g_per_L_from_exactly_0.55_volumes": round(DOSE_VOL / MOLAR_VOL_STP * MW_CO2, 4),
        "CO2_note": "0.81 g KHCO3 gives 0.5495 volumes (1.079 g/L); exactly 0.55 volumes is 1.080 g/L. The 0.1 percent gap is rounding of the design dose.",
        "K_mM": round(k_mM, 3),
        "K_mg_per_serve": round(KHCO3_G / MW_KHCO3 * MW_K * 1000.0, 1),
        "K_mg_per_L": round(KHCO3_G / MW_KHCO3 * MW_K * 1000.0 / SERVE_L, 0),
        "citric_stoich_g_for_CO2": round(citric_stoich_g(KHCO3_G), 3),
        "citric_free_g_after_CO2": round(cit_free_g, 3),
        "citric_total_mM": round(CITRIC_G / MW_CITRIC / SERVE_L * 1000.0, 3),
    }

    # 2. Equilibrium pH at 5, 20, 30 C
    k_m, cit_m, co2_m = recipe_concentrations(retained=True)
    eq = {}
    for t_c in (5.0, 20.0, 30.0):
        s = speciate(t_c, k_m, cit_m, co2_m)
        s_deg = speciate(t_c, k_m, cit_m, 0.0)
        eq[str(int(t_c))] = {
            "pH_with_CO2_retained": round(s["pH"], 3),
            "pH_degassed": round(s_deg["pH"], 3),
            "ionic_strength_M": round(s["ionic_strength_M"], 4),
            "pKa_app_citric": [round(x, 3) for x in s["pKa_app_citric"]],
            "pKa_app_carbonic": [round(x, 3) for x in s["pKa_app_carbonic"]],
            "H_mM": round(s["h_mM"], 4),
            "citric_species_mM": {k: round(v, 3) for k, v in s["citric_species_mM"].items()},
            "carbonate_mM_with_CO2": {k: round(v, 3) for k, v in s["carbonate_mM"].items()},
        }
    out["equilibrium_pH"] = eq
    keep_a = DAVIES_A
    DAVIES_A = 0.0
    s_ideal = {str(int(t)): round(speciate(t, k_m, cit_m, co2_m)["pH"], 3) for t in (5.0, 20.0, 30.0)}
    DAVIES_A = keep_a
    out["pH_ideal_no_activity_correction"] = {
        "pH_by_temperature": s_ideal,
        "note": "With all activity coefficients set to 1 the 25 C value is the 3.5 of the design basis; the Davies correction lowers it by about 0.1 because the ionic strength (0.03 mol/L) lowers the apparent pKs.",
    }

    # 3. Titratable acidity at 20 C (two ionic-strength treatments, with and without retained CO2)
    sprite_ta7 = sprite_ta(SPRITE_TA70_ML)
    sprite_ta7_cit = sprite_ta7 / 3.0 / 1000.0 * MW_CITRIC
    tit = {}
    for label, co2 in (("with_CO2", co2_m), ("degassed", 0.0)):
        row = {}
        for pht in (5.5, 7.0, 8.2):
            ta_end, i_end = titratable_acidity(20.0, k_m, cit_m, co2, pht, "end_I")
            ta_start = titratable_acidity(20.0, k_m, cit_m, co2, pht, "start_I")
            row[f"TA_to_{pht}_mmol_L"] = round(ta_end, 2)
            row[f"TA_to_{pht}_mmol_L_start_I_variant"] = round(ta_start, 2)
            row[f"end_point_ionic_strength_to_{pht}_M"] = round(i_end, 3)
            row[f"TA_to_{pht}_citric_eq_g_L"] = round(ta_end / 3.0 / 1000.0 * MW_CITRIC, 3)
        tit[label] = row
    out["titratable_acidity_20C"] = tit
    cube_ta7_cg = tit["degassed"]["TA_to_7.0_mmol_L"]
    cube_ta7_co2 = tit["with_CO2"]["TA_to_7.0_mmol_L"]
    # Basis note: how much of Sprite's measured TA could be carbonic acid
    frac_hco3_ph7 = 1.0 / (1.0 + 10.0 ** (PK_CARB[0] - 7.0))
    sprite_co2_mM = SPRITE_CO2_VOL / MOLAR_VOL_STP * 1000.0
    out["TA_ratio_to_Sprite_pH7"] = {
        "Sprite_TA7_mmol_L": round(sprite_ta7, 2),
        "cube_degassed_over_Sprite_headline": round(cube_ta7_cg / sprite_ta7, 3),
        "cube_with_all_CO2_retained_over_Sprite_upper_edge": round(cube_ta7_co2 / sprite_ta7, 3),
        "cube_degassed_over_Sprite_start_I_variant": round(tit["degassed"]["TA_to_7.0_mmol_L_start_I_variant"] / sprite_ta7, 3),
        "cube_with_CO2_over_Sprite_start_I_variant": round(tit["with_CO2"]["TA_to_7.0_mmol_L_start_I_variant"] / sprite_ta7, 3),
        "Sprite_dissolved_CO2_mM_at_3.8_volumes": round(sprite_co2_mM, 1),
        "base_to_take_Sprite_CO2_alone_to_pH7_mmol_L_if_retained": round(sprite_co2_mM * frac_hco3_ph7, 1),
        "note": ("Barac et al. titrated 50 mL of Sprite opened and stirred in a beaker; the paper does not say whether the sample was degassed "
                 "and does not report CO2 loss. Sprite at 3.8 volumes (Ali 2022) would need about 138 mmol/L of base to take its CO2 alone to pH 7, "
                 "yet the measured total is 54.8 mmol/L, so most of the CO2 had left during the titration (INFERENCE, not stated by the paper). "
                 "The like-for-like basis for the cube is therefore the degassed value (headline); the all-CO2-retained value is an upper edge. "
                 "Because the measured Sprite value may still contain some carbonic acid, the ratio of the cube to the acid-only part of Sprite "
                 "is higher than the headline."),
    }

    # 3b. Sprite acid basis from the Peshawar citric acid assay (acid only, no carbonic acid): a second Sprite sample
    sp_cit_mM = SPRITE_CITRIC_GL / MW_CITRIC * 1000.0
    s_sp = speciate(20.0, 0.0, sp_cit_mM / 1000.0, 0.0)
    ta_sp_ali = ta7(20.0, 0.0, sp_cit_mM / 1000.0, 0.0)
    out["TA_ratio_to_Sprite_citric_assay_basis"] = {
        "Sprite_citric_mM_Ali2022": round(sp_cit_mM, 3),
        "pH_of_that_citric_acid_alone_20C_model": round(s_sp["pH"], 3),
        "Sprite_pH_Barac2023": SPRITE_PH,
        "Sprite_acid_only_TA_to_7_mmol_L": round(ta_sp_ali, 2),
        "Sprite_acid_only_TA_to_7_citric_eq_g_L": round(ta_sp_ali / 3.0 / 1000.0 * MW_CITRIC, 3),
        "cube_degassed_over_Sprite_acid_only": round(cube_ta7_cg / ta_sp_ali, 2),
        "cube_with_CO2_over_Sprite_acid_only": round(cube_ta7_co2 / ta_sp_ali, 2),
        "Barac_total_TA7_over_acid_only_TA7": round(sprite_ta7 / ta_sp_ali, 2),
        "note": ("The two Sprite samples disagree on how much acid Sprite holds: the Serbian titration (54.8 mmol/L to pH 7, 3.5 g/L citric equivalent) is about "
                 "3 times what the Peshawar citric assay (1.2 g/L citric acid) can supply as acid alone (%.1f mmol/L). If the Peshawar assay is the better "
                 "guide, most of the Serbian total would be carbonic acid and the cube carries about %.1f times Sprite's acid; if the Serbian total is all acid, "
                 "the ratio is %.2f (degassed cube). Both samples are single bottlings (one Serbian, one Pakistani), so the ratio is bracketed, not fixed. "
                 "Sprite also lists sodium citrate (Serbian label), which this acid-only count does not include (INFERENCE that it would raise the buffer)."
                 % (ta_sp_ali, cube_ta7_cg / ta_sp_ali, cube_ta7_cg / sprite_ta7)),
    }

    # 4. Sweetness and sweet to acid
    out["sweetness_sucrose_eq_g_per_100mL"] = {
        name: round(sweetness(SUCRALOSE_MG, pot), 2) for name, pot in POTENCY.items()
    }
    out["sweetness_at_proposed_55_mg_g_per_100mL"] = {
        name: round(sweetness(PROPOSED_SUCRALOSE_MG, pot), 2) for name, pot in POTENCY.items()
    }
    # simple direct form for clarity: mg = target g/100 mL x 330 mL /100 /potency x 1000
    out["sucralose_mg_per_serve_to_match_sugar_eq"] = {
        str(target): {name: round(target * (SERVE_L * 1000.0) / 100.0 / pot * 1000.0, 1)
                      for name, pot in POTENCY.items()}
        for target in (SPRITE_SUGAR_HK, SPRITE_BRIX, SPRITE_SUGAR_INDIA)
    }
    out["sucralose_limit_mg_per_serve"] = round(SUCRALOSE_LIMIT_MG_PER_KG * 0.330, 1)
    out["sucralose_mg_per_kg_of_drink"] = {
        "33_mg": round(33.0 / 0.330, 1),
        "55_mg": round(PROPOSED_SUCRALOSE_MG / 0.330, 1),
        "note": "Drink mass taken as 0.330 kg (density near 1.0); the 300 mg/kg limit is from submission 09 and was not re-read here. Submission 07 (line 65) says the design holds only if no sub-category sets a level below the design level; at 55 mg that level is about 167 mg/kg, not about 100 mg/kg.",
    }

    def sweet_ratio(sucr_mg, ta7_cube_mmol):
        sug = sweetness(sucr_mg, POTENCY["central"]) * 10.0
        cube_cit = ta7_cube_mmol / 3.0 / 1000.0 * MW_CITRIC
        return (sug / cube_cit) / (SPRITE_BRIX * 10.0 / sprite_ta7_cit)

    cube_sugar_gL = sweetness(SUCRALOSE_MG, POTENCY["central"]) * 10.0
    sprite_sugar_gL = SPRITE_BRIX * 10.0
    out["sweet_to_acid"] = {
        "cube_sugar_eq_g_L_33mg": round(cube_sugar_gL, 1),
        "Sprite_sugar_g_L": sprite_sugar_gL,
        "cube_TA7_citric_eq_g_L_degassed": round(cube_ta7_cg / 3.0 / 1000.0 * MW_CITRIC, 3),
        "Sprite_TA7_citric_eq_g_L": round(sprite_ta7_cit, 3),
        "ratio_to_Sprite_titratable_basis_degassed_33mg_headline": round(sweet_ratio(33.0, cube_ta7_cg), 3),
        "ratio_to_Sprite_titratable_basis_degassed_55mg": round(sweet_ratio(PROPOSED_SUCRALOSE_MG, cube_ta7_cg), 3),
        "ratio_to_Sprite_titratable_basis_with_CO2_33mg": round(sweet_ratio(33.0, cube_ta7_co2), 3),
        "ratio_to_Sprite_titratable_basis_with_CO2_55mg": round(sweet_ratio(PROPOSED_SUCRALOSE_MG, cube_ta7_co2), 3),
        "cube_citric_total_g_L": round(CITRIC_G / SERVE_L, 3),
        "Sprite_citric_g_L_Ali2022": SPRITE_CITRIC_GL,
        "cube_citric_total_over_Sprite_mass": round((CITRIC_G / SERVE_L) / SPRITE_CITRIC_GL, 2),
        "mass_basis_sugar_over_citric_cube_33mg": round(cube_sugar_gL / (CITRIC_G / SERVE_L), 2),
        "mass_basis_sugar_over_citric_Sprite": round(sprite_sugar_gL / SPRITE_CITRIC_GL, 2),
        "mass_basis_ratio_cube_over_Sprite_33mg": round((cube_sugar_gL / (CITRIC_G / SERVE_L)) / (sprite_sugar_gL / SPRITE_CITRIC_GL), 3),
        "mass_basis_ratio_cube_over_Sprite_55mg": round((sweetness(PROPOSED_SUCRALOSE_MG, 600.0) * 10.0 / (CITRIC_G / SERVE_L)) / (sprite_sugar_gL / SPRITE_CITRIC_GL), 3),
        "note": "Two Sprite acid values disagree (mass 1.2 g/L citric from a Peshawar sample; titratable 3.5 g/L citric equivalent from a Serbian bottling); both bases are shown. Thin sweetness is flagged on both.",
    }

    # 5. Potassium, citric and bite comparisons
    out["potassium_vs_threshold"] = {
        "K_mM": round(k_mM, 2),
        "KCl_detection_mM": KCL_DETECT_MM,
        "ratio_to_KCl_detection": round(k_mM / KCL_DETECT_MM, 2),
        "potassium_citrate_detection_mM_salt": KCIT_DETECT_MM,
        "ratio_to_K_citrate_if_tripotassium_3K_per_salt": round(k_mM / (3 * KCIT_DETECT_MM), 1),
        "ratio_to_K_citrate_per_mole_of_salt_1K": round(k_mM / KCIT_DETECT_MM, 1),
        "potassium_carbonate_detection_mM_salt": KCARB_DETECT_MM,
        "ratio_to_K_carbonate_on_K_basis_2K_per_salt": round(k_mM / (2 * KCARB_DETECT_MM), 1),
        "Sprite_potassium_mg_per_L_USDA_mirror": 10,
        "cube_potassium_mg_per_L": round(KHCO3_G / MW_KHCO3 * MW_K * 1000.0 / SERVE_L, 0),
        "note": ("Detection thresholds in water for the salt, not bitter or metallic recognition thresholds. The abstract does not say which citrate salt "
                 "was used. Sprite's potassium is about 1 mg per 100 g (USDA via a mirror, S)."),
    }
    k_as_kcl_gl = k_mM / 1000.0 * MW_KCL
    out["potassium_vs_bitterness_recognition"] = {
        "K_as_KCl_mass_g_L": round(k_as_kcl_gl, 3),
        "caffeine_and_KCl_combined_bitter_recognition_g_L": [TORRICO_BITTER_G_100ML[0] * 10.0, TORRICO_BITTER_G_100ML[1] * 10.0],
        "ratio_range": [round(k_as_kcl_gl / (TORRICO_BITTER_G_100ML[1] * 10.0), 1), round(k_as_kcl_gl / (TORRICO_BITTER_G_100ML[0] * 10.0), 1)],
        "note": ("PROXY, order of magnitude only: the Torrico range is for caffeine and KCl together in water (not separable), and the cube's potassium is "
                 "bicarbonate and citrate potassium in a sweet and sour drink. Metallic recognition: no threshold sourced (stated limit)."),
    }
    free_gl = cit_free_g / SERVE_L
    out["citric_vs_threshold"] = {
        "free_citric_g_L": round(free_gl, 3),
        "ratio_to_sour_detection_sucrose_range": [round(free_gl / CITRIC_SOUR_DETECT_GL[1], 1), round(free_gl / CITRIC_SOUR_DETECT_GL[0], 1)],
        "ratio_to_sour_stock_deionized_lower_bound": round(free_gl / CITRIC_SOUR_STOCK_DI_GL, 1),
        "note": ("Detection thresholds are not intensity levels; ratios give the order of magnitude only: at least %.0f times in deionized water "
                 "(the 0.12 g/L stock is above the threshold, so this is a lower bound) and about %.0f to %.0f times in sucrose solution."
                 % (free_gl / CITRIC_SOUR_STOCK_DI_GL, free_gl / CITRIC_SOUR_DETECT_GL[1], free_gl / CITRIC_SOUR_DETECT_GL[0])),
    }
    out["bite"] = {
        "CO2_g_L_from_0.81g_KHCO3": round(co2_gL, 3),
        "Sprite_CO2_g_L_at_3.8_volumes": round(sprite_co2_gL, 2),
        "cube_over_Sprite_CO2": round(co2_gL / sprite_co2_gL, 3),
        "ratio_to_1.2_g_L_no_difference_level": round(co2_gL / BITE_NO_DIFF_CO2_GL, 3),
        "below_2.0_g_L_where_wine_mouthfeel_first_differed": bool(co2_gL < BITE_DIFF_CO2_GL),
        "note": ("Wine PROXY (ethanol matrix, trained and consumer panels): 1.2 g/L did not differ from the 0 g/L control; differences began at 2.0 g/L "
                 "(and at 2.8 g/L for bite in the trained panel). The cube at 1.08 g/L is below both; the benchmark soft drink carries about 7.5 g/L. "
                 "Sparkling sensation threshold 0.44 g/L from Puleo et al. 2021 abstract (PROXY, mineral water)."),
    }

    # 6. Adjustment grid on citric acid at fixed KHCO3 (20 C), degassed headline basis
    grid = []
    for cit_g in (1.40, 1.60, 1.80, 2.00, 2.10, 2.20, 2.40):
        kk, cc, co = recipe_concentrations(citric_g=cit_g, retained=True)
        s = speciate(20.0, kk, cc, co)
        ta_cg = ta7(20.0, kk, cc, 0.0)
        ta_co = ta7(20.0, kk, cc, co)
        grid.append({
            "citric_total_g": cit_g,
            "free_citric_g": round(cit_g - citric_stoich_g(KHCO3_G), 3),
            "pH_20C": round(s["pH"], 3),
            "H_mM": round(s["h_mM"], 4),
            "TA_to_7_degassed_mmol_L": round(ta_cg, 2),
            "TA7_degassed_over_Sprite": round(ta_cg / sprite_ta7, 3),
            "TA_to_7_with_CO2_mmol_L": round(ta_co, 2),
            "TA7_with_CO2_over_Sprite": round(ta_co / sprite_ta7, 3),
            "sweet_ratio_at_55mg_degassed": round(sweet_ratio(PROPOSED_SUCRALOSE_MG, ta_cg), 3),
            "CO2_complete": cit_g >= citric_stoich_g(KHCO3_G),
        })
    out["adjust_citric_grid_20C"] = grid

    # citric acid mass for given pH by bisection (20 C)
    def citric_for_ph(target):
        lo, hi = 0.6, 4.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            kk, cc, co = recipe_concentrations(citric_g=mid, retained=True)
            if speciate(20.0, kk, cc, co)["pH"] > target:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    out["citric_acid_g_for_target_pH_20C"] = {str(p): round(citric_for_ph(p), 3) for p in (3.3, 3.4, 3.5, 3.6, 3.8, 4.0)}

    def citric_for_ph_at(target, t_c, a_val):
        global DAVIES_A
        keep_a3 = DAVIES_A
        DAVIES_A = a_val
        try:
            lo, hi = 0.3, 6.0
            for _ in range(70):
                mid = 0.5 * (lo + hi)
                kk, cc, co = recipe_concentrations(citric_g=mid, retained=True)
                if speciate(t_c, kk, cc, co)["pH"] > target:
                    lo = mid
                else:
                    hi = mid
            return 0.5 * (lo + hi)
        finally:
            DAVIES_A = keep_a3

    out["citric_acid_g_for_target_pH_by_temperature_and_activity"] = {
        "note": "KHCO3 0.81 g and CO2 retained. Davies = with activity correction (this model); ideal = all activity coefficients 1 (the design basis of the 3.5 and the 3.0 in submission 05 line 102).",
        "rows": {
            "%s C, %s, pH %s" % (int(t_c), lab, tp): round(citric_for_ph_at(tp, t_c, a_val), 3)
            for t_c in (20.0, 25.0) for lab, a_val in (("Davies", 0.5), ("ideal", 0.0)) for tp in (3.0, 3.5, 4.0)
        },
    }

    # 7. Adjust carbonation (dose) and the K+ it brings
    dose_rows = []
    for vol in (0.55, 0.61):
        co2_gl_v = vol / MOLAR_VOL_STP * MW_CO2
        khco3 = vol / MOLAR_VOL_STP * SERVE_L * MW_KHCO3
        kk, cc, co = recipe_concentrations(khco3_g=khco3, retained=True)
        s = speciate(20.0, kk, cc, co)
        dose_rows.append({
            "dose_volumes": vol,
            "CO2_g_L": round(co2_gl_v, 3),
            "KHCO3_g_needed": round(khco3, 3),
            "K_mM": round(kk * 1000.0, 2),
            "citric_stoich_g": round(citric_stoich_g(khco3), 3),
            "pH_20C_at_2.10g_citric": round(s["pH"], 3),
        })
    out["adjust_carbonation_rows"] = dose_rows

    # 8. Sensitivity (one at a time) on pH 20 C, TA to 7 (degassed), sweet ratio, K
    def metrics(**kw):
        global DAVIES_A, PK_CIT
        khco3 = kw.get("khco3", KHCO3_G)
        citric = kw.get("citric", CITRIC_G)
        sucr = kw.get("sucralose", SUCRALOSE_MG)
        t_c = kw.get("t", 20.0)
        a_val = kw.get("A", 0.5)
        pk_shift = kw.get("pk1_shift", 0.0)
        keep_a2, keep_pk = DAVIES_A, PK_CIT
        DAVIES_A = a_val
        try:
            kk, cc, co = recipe_concentrations(khco3_g=khco3, citric_g=citric, retained=True)
            if pk_shift:
                PK_CIT = (keep_pk[0] + pk_shift, keep_pk[1], keep_pk[2])
            s = speciate(t_c, kk, cc, co)
            ta_cg = ta7(t_c, kk, cc, 0.0)
        finally:
            DAVIES_A, PK_CIT = keep_a2, keep_pk
        sug = sweetness(sucr, POTENCY["central"]) * 10.0
        return {
            "pH": round(s["pH"], 3),
            "TA7_degassed_mmol_L": round(ta_cg, 2),
            "TA7_degassed_over_Sprite": round(ta_cg / sprite_ta7, 3),
            "sweet_to_acid_ratio": round((sug / (ta_cg / 3.0 / 1000.0 * MW_CITRIC)) / (sprite_sugar_gL / sprite_ta7_cit), 3),
            "K_mM": round(kk * 1000.0, 2),
        }

    base = metrics()
    tornado_inputs = [
        ("citric acid total +/-10 percent (1.89 to 2.31 g)", {"citric": 1.89}, {"citric": 2.31}),
        ("KHCO3 +/-10 percent (0.73 to 0.89 g; CO2 and K move together)", {"khco3": 0.73}, {"khco3": 0.89}),
        ("sucralose 33 mg, potency 400 to 700 (sweet ratio only)", {"sucralose": 33.0 * 400.0 / 600.0}, {"sucralose": 33.0 * 700.0 / 600.0}),
        ("activity model: ideal (A = 0) against Davies A = 0.5", {"A": 0.0}, {"A": 0.5}),
        ("Davies A 0.49 to 0.53", {"A": 0.49}, {"A": 0.53}),
        ("citric pK1 shift -0.05 to +0.05", {"pk1_shift": -0.05}, {"pk1_shift": 0.05}),
        ("temperature 5 C to 30 C", {"t": 5.0}, {"t": 30.0}),
    ]
    torn = []
    for name, lo_kw, hi_kw in tornado_inputs:
        lo = metrics(**lo_kw)
        hi = metrics(**hi_kw)
        torn.append({"input": name, "pH_low": lo["pH"], "pH_high": hi["pH"],
                     "pH_swing": round(abs(hi["pH"] - lo["pH"]), 3),
                     "TA7_ratio_low": lo["TA7_degassed_over_Sprite"], "TA7_ratio_high": hi["TA7_degassed_over_Sprite"],
                     "sweet_ratio_low": lo["sweet_to_acid_ratio"], "sweet_ratio_high": hi["sweet_to_acid_ratio"],
                     "K_mM_low": lo["K_mM"], "K_mM_high": hi["K_mM"]})
    out["sensitivity_one_at_a_time"] = {"base": base, "rows": torn}
    pH_vals = [r["pH_low"] for r in torn] + [r["pH_high"] for r in torn]
    out["robustness"] = {
        "pH_range_over_all_single_changes": [min(pH_vals), max(pH_vals)],
        "TA7_ratio_min_over_all_single_changes": min(min(r["TA7_ratio_low"], r["TA7_ratio_high"]) for r in torn),
        "TA7_ratio_above_Sprite_in_every_single_change": bool(min(min(r["TA7_ratio_low"], r["TA7_ratio_high"]) for r in torn) > 1.0),
        "TA7_ratio_above_1.2_rule_in_every_single_change": bool(min(min(r["TA7_ratio_low"], r["TA7_ratio_high"]) for r in torn) > RISK_RATIO_SOUR),
        "thin_sweetness_below_0.8_rule_in_every_single_change_at_33mg": bool(max(max(r["sweet_ratio_low"], r["sweet_ratio_high"]) for r in torn) < RISK_RATIO_SWEET),
        "sweet_ratio_max_over_all_single_changes_at_33mg": max(max(r["sweet_ratio_low"], r["sweet_ratio_high"]) for r in torn),
        "K_ratio_to_KCl_min_over_changes": round(min(min(r["K_mM_low"], r["K_mM_high"]) for r in torn) / KCL_DETECT_MM, 2),
        "flag_rule_basis_test": {
            "TA7_ratio_degassed_headline": out["TA_ratio_to_Sprite_pH7"]["cube_degassed_over_Sprite_headline"],
            "TA7_ratio_with_CO2_upper_edge": out["TA_ratio_to_Sprite_pH7"]["cube_with_all_CO2_retained_over_Sprite_upper_edge"],
            "flag_fires_on_both_bases_at_rule_1.2": bool(
                out["TA_ratio_to_Sprite_pH7"]["cube_degassed_over_Sprite_headline"] > RISK_RATIO_SOUR
                and out["TA_ratio_to_Sprite_pH7"]["cube_with_all_CO2_retained_over_Sprite_upper_edge"] > RISK_RATIO_SOUR),
        },
    }

    # 9. Risk flags (rules as stated; thresholds are ASSUMPTIONS)
    flags = []
    ratio_cg = out["TA_ratio_to_Sprite_pH7"]["cube_degassed_over_Sprite_headline"]
    ratio_co = out["TA_ratio_to_Sprite_pH7"]["cube_with_all_CO2_retained_over_Sprite_upper_edge"]
    if ratio_cg > RISK_RATIO_SOUR:
        flags.append("TOO SOUR (buffered): TA to pH 7 is %.2f times Sprite on the degassed basis (%.2f with all CO2 retained) against the Serbian titration, and %.1f times the acid that the Peshawar citric assay can supply; rule 1.2 is an ASSUMPTION" % (ratio_cg, ratio_co, out["TA_ratio_to_Sprite_citric_assay_basis"]["cube_degassed_over_Sprite_acid_only"]))
    if out["potassium_vs_threshold"]["ratio_to_KCl_detection"] > 1.0:
        flags.append("SALTY OR BITTER RISK: K+ is about %.0f times the KCl detection threshold (and about %.0f times potassium citrate on a tripotassium basis); off-note not quantified" % (
            out["potassium_vs_threshold"]["ratio_to_KCl_detection"], out["potassium_vs_threshold"]["ratio_to_K_citrate_if_tripotassium_3K_per_salt"]))
    sw = out["sweet_to_acid"]["ratio_to_Sprite_titratable_basis_degassed_33mg_headline"]
    if sw < RISK_RATIO_SWEET:
        flags.append("THIN SWEETNESS: sweet to acid ratio is %.2f of Sprite on the titratable basis (%.2f on the citric mass basis); 6.0 against about 10 g sugar equivalent per 100 mL" % (
            sw, out["sweet_to_acid"]["mass_basis_ratio_cube_over_Sprite_33mg"]))
    if out["bite"]["below_2.0_g_L_where_wine_mouthfeel_first_differed"]:
        flags.append("WEAK BITE: CO2 of %.2f g/L is below the 2.0 g/L where a wine mouthfeel difference began and about %.0f percent of Sprite's %.1f g/L (wine and benchmark PROXIES)" % (
            co2_gL, 100.0 * co2_gL / sprite_co2_gL, sprite_co2_gL))
    flags.append("SOFTER ACID HIT: pH %.2f is above Sprite's 2.71 (hydrogen ion activity about %.0f times lower, a weaker sharp acid note); it is inside the 3.2 to 4.0 range of five Bangladeshi brands (S)" % (
        eq["20"]["pH_with_CO2_retained"], 10.0 ** (eq["20"]["pH_with_CO2_retained"] - SPRITE_PH)))
    out["risk_flags"] = flags

    out["adjustments_arithmetic"] = {
        "sweetener": {
            "from_mg": 33.0, "to_mg": PROPOSED_SUCRALOSE_MG,
            "sugar_eq_g_per_100mL": [round(sweetness(33.0, 600.0), 2), round(sweetness(PROPOSED_SUCRALOSE_MG, 600.0), 2)],
            "range_over_potency_400_to_700_at_55mg": [round(sweetness(PROPOSED_SUCRALOSE_MG, 400.0), 2), round(sweetness(PROPOSED_SUCRALOSE_MG, 700.0), 2)],
            "mg_needed_for_10_g_over_potency_700_600_400": [round(10.0 * 3.3 / p * 1000.0, 1) for p in (700.0, 600.0, 400.0)],
            "sweet_ratio_titratable_basis": [out["sweet_to_acid"]["ratio_to_Sprite_titratable_basis_degassed_33mg_headline"],
                                             out["sweet_to_acid"]["ratio_to_Sprite_titratable_basis_degassed_55mg"]],
            "mg_per_kg": [round(33.0 / 0.33, 0), round(PROPOSED_SUCRALOSE_MG / 0.33, 0)],
        },
        "acid": {"note": "see adjust_citric_grid_20C: lowering citric acid cuts buffered acid but raises pH; about 2.0 g gives pH 3.5 and the working anchor; about 1.4 g is needed for pH 4"},
        "flavour": {"note": "Not modelled: lemon flavour (0.05 g) has no chemistry model here; no flavour threshold or composition is sourced"},
        "blend": {"note": "Sweetener blend synergy is not modelled (no sourced data read); acesulfame potassium would add potassium"},
    }

    out["conclusions"] = [
        "Equilibrium pH is about 3.4 at serve (3.40 to 3.47 over 5 to 30 C) once the ionic strength is counted, so the working pH of 3.5 stands within about 0.1; about 2.0 g of citric acid would give 3.5. CO2 retention does not move pH.",
        "33 mg sucralose gives about 6.0 g sucrose-equivalent per 100 mL (range 4.0 to 7.0); Sprite is about 10 g per 100 mL (8.6 to 11.7 on brand pages).",
        "Matching 10 g with sucralose alone needs about 55 mg per serve (47 to 83 mg over the potency range), about 167 mg/kg, below the 99 mg per serve that 300 mg/kg allows (limit taken from submission 09, not re-read here; sub-category rows unread).",
        "The cube has a higher pH than Sprite (fewer hydrogen ions) and more citric acid and more buffered acid: degassed titratable acid to pH 7 is about 1.3 times the Serbian Sprite titration (1.7 times with all CO2 retained) and about 4 times the acid that the Peshawar citric assay can supply, so the drink carries more acid on every basis and the size of the gap depends on which Sprite sample is used. The taste is not measured.",
    ]
    out["limits"] = [
        "No sensory data. No taste result is claimed. Thresholds are detection values only.",
        "No metallic recognition threshold for K+ and no sourness intensity threshold is in any source read. The only bitterness figure is a combined caffeine and KCl recognition range in water (Torrico et al. 2015 abstract), a PROXY.",
        "The two Sprite samples disagree on the amount of acid (Serbian titration against the Peshawar citric assay); the cube-to-Sprite acid ratio is bracketed from about 1.3 to about 4 (see TA_ratio_to_Sprite_citric_assay_basis), not fixed.",
        "Sprite titratable acidity was measured in a stirred open beaker with unreported CO2 loss (Barac 2023); the ratio basis is stated, and the paper does not say the sample was degassed.",
        "No temperature shift is applied to carbonic acid, and the Davies constant is taken as independent of temperature (ASSUMPTION). The Davies equation is used at I = 0.03 and up to 0.13 to 0.22 at the titration end point (within its stated range of about 0.5; about 2 percent deviation at 0.1 M for 1:1 electrolytes).",
        "Sprite benchmarks are a Serbian bottling (P) and one Peshawar sample (S). The US and Thai formulas were not read. The Singha Lemon Soda can was not found with acid, pH or Brix data.",
    ]

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)

    print("unit checks:", checks)
    print("pH 5/20/30 C with CO2:", [eq[k]["pH_with_CO2_retained"] for k in ("5", "20", "30")])
    print("pH degassed 20 C:", eq["20"]["pH_degassed"], "I 20 C:", eq["20"]["ionic_strength_M"])
    print("ideal pH:", s_ideal)
    print("apparent pK 20 C:", eq["20"]["pKa_app_citric"])
    print("TA7 cube degassed / with CO2:", cube_ta7_cg, cube_ta7_co2, "Sprite TA7:", round(sprite_ta7, 2))
    print("TA ratio block:", {k: v for k, v in out["TA_ratio_to_Sprite_pH7"].items() if k != "note"})
    print("sweet central g/100 mL:", out["sweetness_sucrose_eq_g_per_100mL"]["central"], "sweet ratio:", out["sweet_to_acid"]["ratio_to_Sprite_titratable_basis_degassed_33mg_headline"], out["sweet_to_acid"]["ratio_to_Sprite_titratable_basis_degassed_55mg"])
    print("grid:", [(g["citric_total_g"], g["pH_20C"], g["TA7_degassed_over_Sprite"]) for g in grid])
    print("citric for pH:", out["citric_acid_g_for_target_pH_20C"])
    print("base:", base)
    print("robustness:", out["robustness"])
    print("flags:", len(flags))
    for f in flags:
        print("  -", f)
    print("wrote", os.path.basename(OUT))


if __name__ == "__main__":
    main()
