#!/usr/bin/env python3
"""T9 specification revalidation for slide 7 (Singha Lemon Soda Cube).

Computed from first principles in this script, stdlib only, deterministic (no
random draws, so no seed is used). Writes rework/screen/spec_revalidation_results.json
and prints a short summary.

Tiers in the comments follow rework/submission/appendix_a_tier_key.md:
P primary, S secondary, PROXY, ASSUMPTION, DERIVED (our arithmetic), UNVERIFIED.
All web sources were read on 2026-10-20 unless the comment says otherwise.

Method statement (revised 20 Oct 2026 after verification). The chemistry, the
stoichiometry, the geometry arithmetic and the cost arithmetic are computed from
constants and prices read from sources, not taken from the team's model files. The
following inputs are the team's own design values and are carried as stated ASSUMPTIONS
(they are not independently derived here): the binder and flavour allowances (the range
ends), the pouch footprint and laminate weight, the empty carton mass, the six-cube carton
price, and the SeaCube container dimensions. Checks that reproduce a team value from a team
allowance (the dry-mass range, the SeaCube count) are circular by construction and show
only that the stated figure is that arithmetic. Section 13 compares with saved team
outputs after the sections above ran; the team files are not inputs to any number above it.
This revision read the earlier script, results file and record before editing them.

Second revision (20 Oct 2026, after the second independent verification). Added to this script:
the 60 F (15.56 C) convention for a volume of CO2; the pH at exactly 0.52 g of citric acid;
dose-range bases for the dry-mass range computed here (citric acid held at 2.10 g, and citric
acid rescaled to keep pH 3.5), the pH that reproduces the range ends, and the dry mass at
pH 3.3 and 3.7; the pH comparison with measured soft drinks; mass per unit of punch face for
the cube and the sourced tablets; the hardness benchmarks read in newtons; a sum-of-ratios
check for the sweetener group; and the Notification 468 rows reread on 20 Oct 2026 (values
as read, not computed). No number reported in the record is typed by hand unless the record
says it is quoted from a source or from another team file.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "spec_revalidation_results.json")

# ------------------------------------------------------------ constants
R_GAS = 8.314462618            # J/(mol K), NIST CODATA 2022, exact (P)
P_ATM = 101325.0               # Pa
P_BAR = 100000.0               # Pa, IUPAC standard pressure
T_0C, T_20C, T_30C = 273.15, 293.15, 303.15   # K
T_60F = (60.0 - 32.0) / 1.8 + 273.15           # K, 60 F = 15.56 C (US 4,636,337 definition of a volume, S)
KW_25C = 1.0e-14               # ion product of water at 25 C (ASSUMPTION, textbook)
A_DEBYE = 0.509                # Davies constant at 25 C (ASSUMPTION, textbook)

# IUPAC CIAAW standard atomic weights, 2023 (P)
ATW = {"C": 12.011, "H": 1.008, "K": 39.0983, "O": 15.999}


def molar_mass(counts):
    return sum(ATW[el] * n for el, n in counts.items())


MM_KHCO3 = molar_mass({"K": 1, "H": 1, "C": 1, "O": 3})
MM_CITRIC = molar_mass({"C": 6, "H": 8, "O": 7})      # anhydrous C6H8O7
MM_CITRIC_MONO = MM_CITRIC + 18.015                   # monohydrate (DERIVED, +H2O)
MM_K = ATW["K"]
K_FRAC = MM_K / MM_KHCO3

# Citric acid pKa, 25 C, zero ionic strength: 3.128, 4.761, 6.396 (S, Wikipedia
# Citric acid, body text), read 2026-10-20.
PK_CITRIC = (3.128, 4.761, 6.396)
# Carbonic acid: pK2 10.33 (S, Wikipedia Carbonic acid infobox). pK1 6.35 is a
# textbook effective value (ASSUMPTION); the infobox apparent pKa1 3.75 is not used.
PK_CARBONIC = (6.35, 10.33)

# Solubility of CO2 at 20 C: 0.878 volume (measured at 101.3 kPa and 0 C) per
# volume of water (S, Wikipedia Carbon dioxide data page), read 2026-10-20.
BUNSEN_CO2_20C = 0.878

# Densities, g/cm3
DENS_KHCO3 = 2.17              # S, Wikipedia Potassium bicarbonate (25 C standard state)
DENS_CITRIC = 1.665            # S, Wikipedia Citric acid (anhydrous)
DENS_SUCRALOSE = 1.69          # ASSUMPTION (not sourced in this run)
DENS_BINDER = 1.50             # ASSUMPTION (binder and filler not named)
DENS_FLAVOUR = 1.00            # ASSUMPTION

# Potassium references
EFSA_K_AI = 3500.0             # mg/day, EFSA press release 25 Oct 2016 (P, press release)
NASEM_K_AI_MEN = 3400.0        # mg/day, NASEM 2019 Table 4-4 (P)
NASEM_K_AI_WOMEN = 2600.0      # mg/day, NASEM 2019 Table 4-4 (P)
THAI_K_RDI = 3500.0            # mg/day, MOPH Notification 445 B.E. 2566, Annex 3 row 32
                               # (P; saved English-translation page read by task T10)

# Sucralose
ADI_EU = 15.0                  # mg/kg bw/day, EFSA PLS 16 Feb 2026 (P)
ADI_US = 5.0                   # mg/kg bw/day, FDA, content current 27 Feb 2025 (P)
SWEET_X_SUCROSE = 600.0        # FDA (P)
THAI_SUCRALOSE_CAT14_1_4 = 300.0   # mg/kg, MOPH Notification 468, category 14.1.4, condition 127
                                   # (P; saved extract read 19 Oct 2026)

# Thai labelling rounding for potassium (mg), as summarised in the saved T10 page
# of Notification 445 (P): below 5 declared as 0; 5 to 140 in steps of 5; above 140
# in steps of 10.

# Exchange rates
FX_USD_THB = (33.3535 + 33.7455) / 2.0   # BOT average counter rates, 15 Oct 2026: mid of
                                         # buying (sight) and selling (transfer) = 33.5495 (P)
# Federal Reserve H.10 via FRED, latest observation 9 Oct 2026 in both series (re-read
# 20 Oct 2026): THB per USD 33.5500 and CNY per USD 6.6920. Cross rate (P series, DERIVED).
# The 8 Oct observations (33.69 and 6.7021) were used in the first version of this run and
# are kept below only as a sensitivity.
FX_THB_PER_CNY = 33.55 / 6.6920
FX_THB_PER_CNY_8OCT = 33.69 / 6.7021

# Container: ONE dry 20 ft (ONE page, company page, undated, read 2026-10-20) (P)
ONE_20 = dict(L=5.898, W=2.350, H=2.390, door_W=2.340, door_H=2.280,
              payload=28330.0, tare=2150.0, cubic_m3_stated=33.1)
# SeaCube 20 ft as used in the team's pack_economics.py (S; not reopened in this run)
SEACUBE_20 = dict(L=5.898, W=2.352, H=2.393)
# DSV 20 ft generic (P for DSV statement; rounded dimensions)
DSV_20 = dict(L=5.9, W=2.35, H=2.39, cubic_m3_stated=33.2, payload=25000.0)

# Guidechem price rows (S, price aggregator, ex-works China, CNY per tonne), opened
# and read by this run on 2026-10-20:
#   potassium bicarbonate 298-14-6 (page updated 18 Oct 2026)
#   citric acid 77-92-9 (page updated 19 Oct 2026)
#   sucralose 56038-13-2 (page updated 10 Oct 2026)
#   maltodextrin 9050-36-6 (page updated 3 Jun 2026: stale)
#   mannitol 69-65-8 (page updated 15 Oct 2026)
# Citric acid rows, October 2026 monthly table (page re-read 20 Oct 2026, page update 19 Oct 2026),
# CNY per tonne, midpoint of a printed range. Only rows labelled "Food Grade" (any form) and
# with content 99 percent or higher or no content printed are used for the food-grade basis;
# rows of 90 and 95 percent content are excluded.
CITRIC_FOOD_GRADE_ROWS = {
    "Shandong Food Grade 99%, 25 kg": 6500.0,
    "Shandong Food Grade": 6500.0,
    "Yingxuan Food Grade (4,967 to 5,200)": (4967.0 + 5200.0) / 2.0,
    "Locally Made Food Grade, Content 99.9% (5,400 to 6,700)": (5400.0 + 6700.0) / 2.0,
    "Gongyi, Henan Food Grade, Content 99%": 5500.0,
    "Seven Stars Food Grade, Content 99%": 6800.0,
    "Qixing Pai Food Grade, Content 99%": 6800.0,
    "Yijia Water Purification Food grade, monohydrate, 99.5%": 6300.0,
    "Locally Made Food Grade": 6500.0,
    "Yingxuan/Qixing Food Grade": 6400.0,
    "Shijian Chemical Anhydrous Citric Acid, Food Grade": 7000.0,
    "Shijian Chemical Citric Acid Monohydrate, Food Grade": 6300.0,
    "Shunzhi Bang Food Grade, Content 99%": 5000.0,
    "Shunzhi Bang Food Grade, Content 99.9%": 4800.0,
    "Huiyi Hai Food Grade": 4300.0,
}
# Rows labelled anhydrous (Oct 2026): not all are labelled food grade.
CITRIC_ANHYDROUS_ROWS = {
    "Shandong Yingxuan Anhydrous, 99.5% (5,200 to 6,200), not labelled food grade": (5200.0 + 6200.0) / 2.0,
    "Locally Made Anhydrous, 99.5% (6,000), not labelled food grade": 6000.0,
    "Locally Made anhydrous citric acid (5,000 to 6,600), not labelled food grade": (5000.0 + 6600.0) / 2.0,
    "Shijian Chemical Anhydrous Citric Acid, Food Grade (7,000)": 7000.0,
}


def _median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


CIT_FG_MED = _median(CITRIC_FOOD_GRADE_ROWS.values())
CIT_AN_MED = _median(CITRIC_ANHYDROUS_ROWS.values())

GC = {
    "khco3": {"low": 7900, "central": 7900, "high": 9800,
              "rows": "Zhejiang Dayang Food Grade 99% (7,900); Locally Made Food Grade 99% (9,800)"},
    "khco3_unlabelled": 5500,   # Shanxi 99%, grade not stated (sensitivity only)
    # Headline basis: food-grade-labelled rows (median of the 15 row midpoints; range is the
    # lowest and highest midpoint). The anhydrous-labelled set is the cross-check.
    "citric": {"low": min(CITRIC_FOOD_GRADE_ROWS.values()), "central": CIT_FG_MED,
               "high": max(CITRIC_FOOD_GRADE_ROWS.values()),
               "rows": "median of 15 food-grade-labelled row midpoints in the Oct 2026 monthly table"},
    "citric_anhydrous_rows_median": CIT_AN_MED,
    "citric_unlabelled": 6500,  # Shandong Food Grade 99% 25 kg, form not stated (sensitivity)
    "sucralose": {"low": 105000, "central": 105000, "high": 360000,
                  "rows": "Jiangsu Xin Su 99% (105,000); Senfida 98% (360,000); neither row is "
                          "labelled food grade"},
    "maltodextrin": {"low": 3500, "central": 3900, "high": 4300,
                     "rows": "Shandong Xiwang Food Grade 99% (3,500 to 3,600); Henan Food-Grade (4,200 to 4,300)"},
    "mannitol": 28000,          # Hubei 99% (28 CNY/kg), grade not labelled food (sensitivity)
}
# Trade-guide cross-check (S, Elchemy 9 Jul 2026, re-read 20 Oct 2026): food grade citric acid
# (form not stated), FOB, USD/kg 0.90 to 1.25; the page also says anhydrous typically costs
# 5 to 10 percent more per kg than monohydrate.
ELCHEMY_CITRIC_FOOD_USD = (0.90, 1.25)
ELCHEMY_ANHYDROUS_PREMIUM = (1.05, 1.10)
# Flavour: no source reached, ASSUMPTION THB per kg
FLAVOUR_THB_PER_KG = {"low": 300.0, "central": 800.0, "high": 1500.0}

# ------------------------------------------------------------ slide 7 inputs
SLIDE = {
    "dose_vol": 0.55,            # volumes of CO2 per 330 mL
    "khco3_g": 0.81,
    "potassium_mg": 317.0,
    "citric_stoich_g": 0.52,
    "citric_g": 2.10,
    "pH": 3.5,
    "sucralose_mg": 33.0,
    "sucralose_mg_per_kg": 100.0,
    "binder_g": 0.80,
    "flavour_g": 0.05,
    "dry_g": 3.79,
    "dry_range": (3.46, 4.24),
    "cube_mm": 14.0,
    "packed_g": 5.29,
    "pouch_g": 1.5,
    "net_g": 3.8,
    "carton_mm": (190.0, 150.0, 50.0),
    "cartons_20ft": 21431,
    "cubes_20ft": 128586,
    "pack_fraction": 0.92,
    "cost_total": 4.09,
    "cost_reactants": 0.12,
    "cost_pouch_print": 2.80,
    "cost_processing": 0.50,
    "cost_carton": 0.67,
    "contribution": 4.91,
    "planning_price": 9.00,
    "shelf_price_deck": 15.00,   # slide 9 note: planning price is 60% of a THB 15 shelf price
    "exfactory_share": 0.60,
}
SERVE_L = 0.330

# Team inputs carried as ASSUMPTIONS (the team's own choices; no source in this run)
POUCH_LAYOUT_MM = (90.0, 70.0, 20.0)     # flat pouch footprint and contents height
CARTON_MASS_KG = 0.10                    # empty carton
LAMINATE_G_PER_M2 = 96.0                 # laminate areal weight
CARTON_6_THB = 4.00                      # THB per six-cube carton (team ASSUMPTION)

# ------------------------------------------------------------ helpers


def molar_volume_L(T, P):
    """Ideal-gas molar volume in L/mol: V_m = R T / P."""
    return R_GAS * T / P * 1000.0


def polyprotic(h, pks):
    """Fractions by number of protons lost, i = 0..n, for an acid with pK list pks."""
    n = len(pks)
    ks = [10.0 ** (-p) for p in pks]
    terms = []
    for i in range(n + 1):
        prod = 1.0
        for k in range(i):
            prod *= ks[k]
        terms.append(prod * h ** (n - i))
    d = sum(terms)
    return [t / d for t in terms]


def davies_f(I):
    s = math.sqrt(I)
    return s / (1.0 + s) - 0.3 * I


def app_pks(pk0, I, activity):
    """Apparent pK values. With activity True, Davies correction: for step k the
    species charge goes from -(k-1) to -k, so pKa_app = pKa0 - A f (1 + k^2 - (k-1)^2)."""
    if not activity:
        return list(pk0)
    f = davies_f(I)
    return [p - A_DEBYE * f * (1.0 + k * k - (k - 1) * (k - 1))
            for k, p in enumerate(pk0, start=1)]


def solve_ph(m_citric_g, n_khco3_mol, V_L, pk_cit=PK_CITRIC, pk_carb=PK_CARBONIC,
             activity=False):
    """pH from charge balance in an open vessel.

    K+ (all potassium, fixed) + H+ = OH- + citrate charge + carbonate charge.
    Citric acid fixed at m / 192.123. CO2 leaves as it forms, so the carbonate left is
    max(0, n_KHCO3 - 3 n_citric).
    """
    C_K = n_khco3_mol / V_L
    n_cit = m_citric_g / MM_CITRIC
    C_cit = n_cit / V_L
    C_c = max(0.0, n_khco3_mol - 3.0 * n_cit) / V_L
    I = 0.5 * (C_K + 3.0 * C_cit + C_c)
    pH = None
    for _ in range(100):
        pk_c = app_pks(pk_cit, I, activity)
        pk_b = app_pks(pk_carb, I, activity)

        def gap(p):
            h = 10.0 ** (-p)
            a = polyprotic(h, pk_c)
            b = polyprotic(h, pk_b)
            zc = sum(i * a[i] for i in range(len(a)))
            zb = sum(i * b[i] for i in range(len(b)))
            return C_K + h - KW_25C / h - (C_cit * zc + C_c * zb)

        lo, hi = -2.0, 16.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if gap(mid) > 0.0:
                lo = mid
            else:
                hi = mid
        pH = 0.5 * (lo + hi)
        h = 10.0 ** (-pH)
        a = polyprotic(h, pk_c)
        b = polyprotic(h, pk_b)
        I_new = 0.5 * (C_K + h + KW_25C / h
                       + C_cit * sum(i * i * a[i] for i in range(len(a)))
                       + C_c * sum(i * i * b[i] for i in range(len(b))))
        if abs(I_new - I) < 1e-10:
            I = I_new
            break
        I = I_new
    # pH is -log10 of the H+ CONCENTRATION that solves the charge balance with Davies
    # apparent constants. A pH meter reads the H+ ACTIVITY, so the meter-equivalent value is
    # pH_conc + A f(I) (log gamma_H = -A f for a unit charge). With activity False the
    # two are the same ideal value.
    a_f = A_DEBYE * davies_f(I) if activity else 0.0
    return {"pH": round(pH, 4), "pH_conc": round(pH, 4), "pH_meter": round(pH + a_f, 4),
            "A_f": round(a_f, 4), "ionic_strength_M": round(I, 5)}


def mass_for_ph(target, n_khco3_mol, V_L, activity=False, basis="conc", iters=100):
    """Citric acid mass (g) that gives the target pH (bisection on mass).

    basis "conc" targets -log10 [H+]; basis "meter" targets -log10 a(H+), the quantity a pH
    meter reports (identical to "conc" when activity is False).
    """
    key = "pH_meter" if basis == "meter" else "pH_conc"
    lo, hi = 0.2, 6.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if solve_ph(mid, n_khco3_mol, V_L, activity=activity)[key] > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def label_round_mg(mg):
    """Thai nutrition-label rounding for sodium and potassium (T10 saved page, P)."""
    if mg < 5.0:
        return 0.0
    if mg <= 140.0:
        return 5.0 * round(mg / 5.0)
    return 10.0 * round(mg / 10.0)


def fmt(x, nd=3):
    return round(x, nd)


R = {}   # results

# ------------------------------------------------------------ 1. stoichiometry
n_dose = SLIDE["dose_vol"] * SERVE_L / molar_volume_L(T_0C, P_ATM) * 1.0    # mol CO2 at 0 C
n_khco3_dose = n_dose                                 # 1 mol CO2 per mol KHCO3
khco3_dose_g = n_khco3_dose * MM_KHCO3
citric_stoich_dose_g = n_khco3_dose / 3.0 * MM_CITRIC
n_khco3_slide = SLIDE["khco3_g"] / MM_KHCO3
citric_stoich_slide_g = n_khco3_slide / 3.0 * MM_CITRIC
R["stoichiometry"] = {
    "reaction": "3 KHCO3 + C6H8O7 -> K3C6H5O7 + 3 CO2 + 3 H2O",
    "MM_KHCO3_g_mol": fmt(MM_KHCO3, 4),
    "MM_citric_anhydrous_g_mol": fmt(MM_CITRIC, 4),
    "MM_citric_monohydrate_g_mol": fmt(MM_CITRIC_MONO, 4),
    "KHCO3_g_at_0p55_dose_0C": fmt(khco3_dose_g, 4),
    "KHCO3_g_slide_rounded_input": SLIDE["khco3_g"],
    "citric_stoich_g_at_0p55_dose": fmt(citric_stoich_dose_g, 4),
    "citric_stoich_g_from_0p81g": fmt(citric_stoich_slide_g, 4),
    "citric_stoich_monohydrate_g_from_0p81g": fmt(citric_stoich_slide_g * MM_CITRIC_MONO / MM_CITRIC, 4),
    "citric_excess_ratio_vs_stoich": fmt(SLIDE["citric_g"] / citric_stoich_slide_g, 3),
    "match_citric_stoich_0p52": round(citric_stoich_slide_g, 2) == SLIDE["citric_stoich_g"],
}

# ------------------------------------------------------------ 2. CO2 volume
co2 = {}
for label, T in (("0C", T_0C), ("20C", T_20C), ("30C", T_30C), ("60F_15p56C", T_60F)):
    Vm = molar_volume_L(T, P_ATM)
    V_mL = n_dose * Vm * 1000.0
    n_target = SLIDE["dose_vol"] * SERVE_L / Vm        # mol of CO2 that makes 0.55 volume on THIS basis
    co2[label] = {"T_K": T, "V_m_L_per_mol_1atm": fmt(Vm, 4),
                  "CO2_mL_for_0p55_dose": fmt(V_mL, 1),
                  "volumes_per_330mL": fmt(V_mL / 330.0, 4),
                  "KHCO3_g_for_0p55_volume_on_this_basis": fmt(n_target * MM_KHCO3, 4),
                  "potassium_mg_for_0p55_volume_on_this_basis": fmt(n_target * MM_K * 1000.0, 1)}
co2["0C_from_0p81g"] = fmt(SLIDE["khco3_g"] / MM_KHCO3 * molar_volume_L(T_0C, P_ATM) * 1000.0 / 330.0, 4)
R["co2_volume"] = {
    "basis": "Ideal gas V_m = R T / P, R = 8.314462618 J/(mol K) (NIST CODATA 2022, P); 1 atm.",
    "by_temperature": co2,
    "IUPAC_1bar_0C_V_m_L_per_mol": fmt(molar_volume_L(T_0C, P_BAR), 4),
    "bunsen_co2_20C_volumes_STP": BUNSEN_CO2_20C,
    "match_0p55_at_0C": round(co2["0C"]["volumes_per_330mL"], 2) == SLIDE["dose_vol"],
    "note": "0.55 volumes is the gas released at 0 C and 1 atm. At 20 C the same mole count "
            "gives 0.59 volumes and at 30 C 0.61. A second convention in use counts the volume at "
            "60 F (15.56 C; US 4,636,337, S), on which the same dose reads 0.58 volume (key "
            "60F_15p56C). The 0.878 Bunsen value is a capacity at 1 atm of "
            "pure CO2 (STP-normalised). Slide 7 must say that the figure is a gas volume at 0 C.",
}

# ------------------------------------------------------------ 3. potassium
K_dose_mg = n_khco3_dose * MM_K * 1000.0
K_slide_mg = SLIDE["khco3_g"] * K_FRAC * 1000.0
R["potassium"] = {
    "K_fraction_in_KHCO3": fmt(K_FRAC, 6),
    "K_mg_from_0p55_dose": fmt(K_dose_mg, 2),
    "K_mg_from_rounded_0p81g": fmt(K_slide_mg, 2),
    "slide_K_mg": SLIDE["potassium_mg"],
    "match_317_on_dose_basis": round(K_dose_mg) == SLIDE["potassium_mg"],
    "label_declared_mg_from_dose": label_round_mg(K_dose_mg),
    "label_declared_mg_from_0p81g": label_round_mg(K_slide_mg),
    "KHCO3_g_for_exact_317_mg": fmt(317.0 / 1000.0 / K_FRAC, 5),
    "share_of_Thai_RDI_3500_pct": fmt(100.0 * K_dose_mg / THAI_K_RDI, 2),
    "share_of_EFSA_AI_3500_pct": fmt(100.0 * K_dose_mg / EFSA_K_AI, 2),
    "share_of_NASEM_AI_men_3400_pct": fmt(100.0 * K_dose_mg / NASEM_K_AI_MEN, 2),
    "share_of_NASEM_AI_women_2600_pct": fmt(100.0 * K_dose_mg / NASEM_K_AI_WOMEN, 2),
    "share_of_3500_if_declared_320_pct": fmt(100.0 * 320.0 / THAI_K_RDI, 2),
    "note": f"317 mg is the exact 0.55-volume dose ({K_dose_mg:.1f} mg). The rounded 0.81 g gives "
            f"{K_slide_mg:.1f} mg. If potassium is declared on a Thai nutrition panel, the rounding "
            "rule (T10 saved page of Notification 445) gives 320 mg, so a panel would not read "
            "317 mg. Notification 445 Clause 3 requires a panel only for foods with a nutrition "
            "claim, a health claim or nutritional value used in promotion (or others the Minister "
            "notifies), so whether a panel is required is not settled. The caveat's 9 percent is "
            "right either way.",
}

# ------------------------------------------------------------ 4. citric acid and pH
n_dose_khco3 = n_khco3_dose
pH_ideal = solve_ph(SLIDE["citric_g"], n_dose_khco3, SERVE_L)
pH_davies = solve_ph(SLIDE["citric_g"], n_dose_khco3, SERVE_L, activity=True)
mass_targets = {}
for tgt in (3.0, 3.3, 3.5, 3.7, 4.0, 4.5):
    mass_targets[str(tgt)] = {
        "ideal_g": fmt(mass_for_ph(tgt, n_dose_khco3, SERVE_L), 3),
        "davies_conc_pH_g": fmt(mass_for_ph(tgt, n_dose_khco3, SERVE_L, activity=True, basis="conc"), 3),
        "davies_meter_pH_g": fmt(mass_for_ph(tgt, n_dose_khco3, SERVE_L, activity=True, basis="meter"), 3),
    }
curve = {}
for m in (0.0, 0.30, 0.40, citric_stoich_dose_g, 0.52, 0.80, 1.00, 1.50, 1.80, 2.00, 2.10,
          2.20, 2.50, 3.00):
    _d = solve_ph(m, n_dose_khco3, SERVE_L, activity=True)
    curve[f"{m:.3f}"] = {"ideal": solve_ph(m, n_dose_khco3, SERVE_L)["pH"],
                        "davies_conc": _d["pH_conc"], "davies_meter": _d["pH_meter"]}
sens = {}
for idx, name in enumerate(("pKa1", "pKa2", "pKa3")):
    for d in (-0.1, 0.1):
        pk = list(PK_CITRIC)
        pk[idx] += d
        sens[f"{name}{d:+.1f}"] = solve_ph(SLIDE["citric_g"], n_dose_khco3, SERVE_L,
                                           pk_cit=tuple(pk))["pH"]
R["citric_pH"] = {
    "slide_pH": SLIDE["pH"],
    "pH_ideal_at_2p10g": pH_ideal["pH"],
    "pH_davies_concentration_basis_at_2p10g": pH_davies["pH_conc"],
    "pH_davies_meter_equivalent_at_2p10g": pH_davies["pH_meter"],
    "davies_A_f_at_2p10g": pH_davies["A_f"],
    "ionic_strength_M_ideal": pH_ideal["ionic_strength_M"],
    "ionic_strength_M_davies": pH_davies["ionic_strength_M"],
    "mass_for_target_pH": mass_targets,
    "pH_vs_citric_mass": curve,
    "sensitivity_pKa_shift_pH_at_2p10g": sens,
    "bicarbonate_only_pH": curve["0.000"]["ideal"],
    "pH_at_stoichiometric_0p5186g_ideal": curve[f"{citric_stoich_dose_g:.3f}"]["ideal"],
    "pH_at_exactly_0p52g_ideal": curve["0.520"]["ideal"],
    "excess_acid_at_0p52g_pct_over_stoich": fmt(100.0 * (0.52 - citric_stoich_dose_g) / citric_stoich_dose_g, 2),
    "stoichiometric_point_note": "The potassium citrate point (all bicarbonate consumed, no excess acid) is "
                                 f"at {citric_stoich_dose_g:.4f} g and the pH there is the ideal value shown for key "
                                 f"{citric_stoich_dose_g:.3f}. At exactly 0.52 g there is "
                                 f"{100.0 * (0.52 - citric_stoich_dose_g) / citric_stoich_dose_g:.2f} percent excess acid, and the pH "
                                 "falls steeply to the value under key 0.520, so the slide's 0.52 g is not the "
                                 "pH of the stoichiometric point.",
    "match_pH_3p5": abs(pH_ideal["pH"] - SLIDE["pH"]) < 0.05,
    "note": "Open-vessel model, 25 C, pKa at zero ionic strength (S). CO2 leaves as it forms. "
            "The ideal value (3.50) treats activity as concentration and is the working value. "
            "With the Davies correction (ionic strength about 0.03 M) the solved -log10 of the H+ "
            "concentration is the 'concentration basis' value, and the quantity a pH meter reads "
            "(-log10 of the H+ activity) is higher by A f (about 0.07), the 'meter-equivalent' value. "
            "Both are sensitivities. Titratable acid at 2.10 g is 4.05 times the stoichiometric "
            "amount. Above 0.52 g the pH falls from 9 to about 3.2 as acid is added; below 0.52 g "
            "bicarbonate is in excess.",
}

# pH against measured soft drinks (Barac et al. 2023, Acta Medica Medianae 62(3), Table 2, P; one Serbian
# bottling each, pH read on opening; saved in raw/diligence_2026-10-20/T8/barac2023_sprite_pH_TA.md)
BARAC_PH = {"Sprite": 2.71, "Coca-Cola": 2.56, "Schweppes Bitter Lemon": 2.54}
R["ph_vs_soft_drinks"] = {
    "source": "Barac et al. 2023, Acta Med Medianae 62(3), Table 2 (P; one Serbian bottling each; "
              "T8 saved page barac2023_sprite_pH_TA.md)",
    "measured_pH": BARAC_PH,
    "cube_pH_ideal": pH_ideal["pH"],
    "cube_pH_meter_equivalent_davies": pH_davies["pH_meter"],
    "hydrogen_ion_ratio_drink_over_cube_ideal": {k: fmt(10.0 ** (pH_ideal["pH"] - v), 1) for k, v in BARAC_PH.items()},
    "hydrogen_ion_ratio_drink_over_cube_meter_equivalent": {k: fmt(10.0 ** (pH_davies["pH_meter"] - v), 1) for k, v in BARAC_PH.items()},
    "pH_units_above_measured_drinks_ideal": {k: fmt(pH_ideal["pH"] - v, 2) for k, v in BARAC_PH.items()},
    "note": "The cube drink at the ideal pH is above all three measured soft drinks by the pH units "
            "shown, so its hydrogen ion level is several times lower (ratios above). pH is not the "
            "sourness: the acid load of the cube is 6.36 g/L of citric acid (section taste_benchmarks) "
            "and the titratable acidity comparison with Sprite is in the team's chemistry record "
            "rework/71 (T8), which was not rerun here.",
}

# ------------------------------------------------------------ 5. sucralose
sucr_mg = SLIDE["sucralose_mg"]
drink_mass_g = SERVE_L * 1000.0 + SLIDE["dry_g"]
dry_components_dose = {"KHCO3": khco3_dose_g, "citric": SLIDE["citric_g"],
                       "sucralose": sucr_mg / 1000.0, "binder": SLIDE["binder_g"],
                       "flavour": SLIDE["flavour_g"]}
dry_dose_sum = sum(dry_components_dose.values())
sweet_sugar_g_per_100ml = (sucr_mg / SERVE_L) * SWEET_X_SUCROSE / 1000.0 / 10.0
R["sucralose"] = {
    "mg_per_L_on_330mL": fmt(sucr_mg / SERVE_L, 2),
    "mg_per_kg_on_330g_water": fmt(sucr_mg / 0.330, 2),
    "mg_per_kg_on_finished_drink": fmt(sucr_mg / drink_mass_g * 1000.0, 2),
    "slide_mg_per_kg": SLIDE["sucralose_mg_per_kg"],
    "w_w_percent_of_cube": fmt(100.0 * (sucr_mg / 1000.0) / dry_dose_sum, 3),
    "sugar_equivalent_g_per_100mL_at_600x": fmt(sweet_sugar_g_per_100ml, 2),
    "share_of_Thai_limit_300_mg_per_kg_pct": fmt(100.0 * (sucr_mg / 0.330) / (THAI_SUCRALOSE_CAT14_1_4 * 1.0) * 1.0, 1),
    "EU_ADI_share_pct": {
        "adult60kg": fmt(100.0 * (sucr_mg / 60.0) / ADI_EU, 2),
        "child15kg": fmt(100.0 * (sucr_mg / 15.0) / ADI_EU, 2),
    },
    "US_ADI_share_pct": {
        "adult60kg": fmt(100.0 * (sucr_mg / 60.0) / ADI_US, 2),
        "child15kg": fmt(100.0 * (sucr_mg / 15.0) / ADI_US, 2),
    },
    "note": "Mass basis: 330 g of water gives 100 mg/kg; the finished drink (330 mL water plus the "
            "3.79 g cube) gives about 99 mg/kg. Both round to about 100 mg/kg. The Thai limit "
            "(Notification 468, category 14.1.4, conditions 127 and TH3; 127 calculates as ready to "
            "drink) is 300 mg/kg, so the design is about one third of it. 33 mg is inside the 3.79 g "
            "dry mass.",
}

# Sweet and sour benchmarks (pages saved in T9 taste_and_acid_benchmarks.md, re-opened 20 Oct 2026)
INGREDION_CITRIC_PCT = 0.220     # S: Ingredion lemon-lime (no sugar added) starting formula, % as is
FOODS2020_CITRIC_PCT = 0.140     # P: Foods 2020;9(10):1425 Table 1, % w/v
FOODS2020_SUCROSE_PCT = 2.50     # P: same table, % w/v
FOODS2020_SWEET_S, FOODS2020_SWEET_SC = 6.32, 4.53   # P: same paper, mean sweetness, 9-point scale
design_citric_pct = SLIDE["citric_g"] / (SERVE_L * 1000.0) * 100.0      # g per 100 mL
R["taste_benchmarks"] = {
    "design_citric_acid_g_per_L": fmt(SLIDE["citric_g"] / SERVE_L, 3),
    "design_citric_acid_pct_w_v": fmt(design_citric_pct, 3),
    "design_sugar_equivalent_pct_w_v_at_600x": fmt(sweet_sugar_g_per_100ml, 2),
    "Ingredion_lemon_lime_citric_pct_S": INGREDION_CITRIC_PCT,
    "design_acid_over_Ingredion": fmt(design_citric_pct / INGREDION_CITRIC_PCT, 2),
    "Foods2020_citric_pct_P": FOODS2020_CITRIC_PCT,
    "design_acid_over_Foods2020": fmt(design_citric_pct / FOODS2020_CITRIC_PCT, 2),
    "Foods2020_sucrose_pct_P": FOODS2020_SUCROSE_PCT,
    "design_sugar_equivalent_over_Foods2020_sucrose": fmt(sweet_sugar_g_per_100ml / FOODS2020_SUCROSE_PCT, 2),
    "design_acid_per_sugar_equivalent": fmt(design_citric_pct / sweet_sugar_g_per_100ml, 4),
    "Foods2020_acid_per_sucrose": fmt(FOODS2020_CITRIC_PCT / FOODS2020_SUCROSE_PCT, 4),
    "design_acid_to_sweetness_ratio_over_Foods2020": fmt(
        (design_citric_pct / sweet_sugar_g_per_100ml) / (FOODS2020_CITRIC_PCT / FOODS2020_SUCROSE_PCT), 2),
    "Foods2020_sweetness_sucrose_alone_9pt": FOODS2020_SWEET_S,
    "Foods2020_sweetness_with_citric_9pt": FOODS2020_SWEET_SC,
    "Foods2020_sweetness_drop_pct": fmt(100.0 * (FOODS2020_SWEET_S - FOODS2020_SWEET_SC) / FOODS2020_SWEET_S, 1),
    "note": "The design acid load (0.64 percent w/v) is about 2.9 times the citric acid in an ingredient "
            "maker's lemon-lime starting formula (0.22 percent; S, undated; its sweetness, pH and "
            "carbonation are not stated) and about 4.5 times the 0.14 percent that cut the mean "
            "sweetness of 2.5 percent sucrose from 6.32 to 4.53 on a 9-point scale (28 percent; "
            "P, aqueous sucrose, consumer panel). The sugar equivalent of the design (6.0 g per 100 mL) "
            "is 2.4 times that sucrose sample, but the acid per unit of sweetness is about 1.9 times "
            "the Foods 2020 sample. 33 mg of sucralose may therefore be low against 2.10 g of citric "
            "acid. This is an untasted desk flag, not a finding: sucralose is not sucrose, and no "
            "sample of the cube has been tasted.",
}

# ------------------------------------------------------------ 6. dry mass and its range
dry_dose_total = dry_dose_sum
allow_low = khco3_dose_g + SLIDE["citric_g"] + 0.50 + 0.02 + sucr_mg / 1000.0
allow_high = khco3_dose_g + SLIDE["citric_g"] + 1.20 + 0.10 + sucr_mg / 1000.0
single = {}
lo_r, hi_r = SLIDE["dry_range"]
for name, val in (("binder_g", SLIDE["binder_g"]), ("citric_g", SLIDE["citric_g"]),
                  ("flavour_g", SLIDE["flavour_g"]), ("KHCO3_g", khco3_dose_g)):
    single[name] = {"value_g": val,
                    "needed_low": fmt(val + lo_r - dry_dose_total, 4),
                    "needed_high": fmt(val + hi_r - dry_dose_total, 4)}
dose_050 = (0.50 / SLIDE["dose_vol"]) * khco3_dose_g
dose_060 = (0.60 / SLIDE["dose_vol"]) * khco3_dose_g
n_20C_dose = SLIDE["dose_vol"] * SERVE_L / molar_volume_L(T_20C, P_ATM)


def dry_mass_for_dose(vol, citric_g):
    """Dry mass (g) for a dose in volumes of CO2 (counted at 0 C and 1 atm) and a citric acid mass."""
    n = vol * SERVE_L / molar_volume_L(T_0C, P_ATM)
    return n * MM_KHCO3 + citric_g + sucr_mg / 1000.0 + SLIDE["binder_g"] + SLIDE["flavour_g"]


def dry_mass_citric_rescaled(vol):
    """Dry mass when the citric acid is rescaled to keep the ideal-model pH of 3.5 at that dose."""
    n = vol * SERVE_L / molar_volume_L(T_0C, P_ATM)
    return dry_mass_for_dose(vol, mass_for_ph(SLIDE["pH"], n, SERVE_L, iters=45))


def dose_for_mass(target_g, fn):
    lo, hi = 0.15, 1.5
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if fn(mid) < target_g:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# Basis A: citric acid held at 2.10 g, dose changed (the KHCO3 mass that gives each range end).
vol_per_g_khco3 = SLIDE["dose_vol"] / khco3_dose_g
dose_A = [fmt(single["KHCO3_g"]["needed_low"] * vol_per_g_khco3, 3),
          fmt(single["KHCO3_g"]["needed_high"] * vol_per_g_khco3, 3)]
# Basis B: citric acid rescaled to keep pH 3.5 (ideal) at each dose.
dose_B_lo = dose_for_mass(lo_r, dry_mass_citric_rescaled)
dose_B_hi = dose_for_mass(hi_r, dry_mass_citric_rescaled)
dose_B_masses = {f"{v:.2f}_volume": fmt(dry_mass_citric_rescaled(v), 3) for v in (0.49, 0.50, 0.60, 0.64)}
# Target pH that reproduces the range ends (citric acid needed for each end, then its ideal pH).
pH_at_range_ends = [solve_ph(single["citric_g"]["needed_low"], n_dose_khco3, SERVE_L)["pH"],
                    solve_ph(single["citric_g"]["needed_high"], n_dose_khco3, SERVE_L)["pH"]]
dry_at_pH_3p3 = dry_dose_total - SLIDE["citric_g"] + mass_targets["3.3"]["ideal_g"]
dry_at_pH_3p7 = dry_dose_total - SLIDE["citric_g"] + mass_targets["3.7"]["ideal_g"]
drivers_offsets = [mass_targets["3.3"]["ideal_g"] - SLIDE["citric_g"], mass_targets["3.7"]["ideal_g"] - SLIDE["citric_g"],
                   mass_targets["3.5"]["davies_meter_pH_g"] - SLIDE["citric_g"],
                   mass_targets["3.5"]["davies_conc_pH_g"] - SLIDE["citric_g"],
                   dose_050 - khco3_dose_g, dose_060 - khco3_dose_g,
                   n_20C_dose * MM_KHCO3 - khco3_dose_g,
                   SLIDE["citric_g"] * (MM_CITRIC_MONO / MM_CITRIC - 1.0)]
range_offset_low = lo_r - SLIDE["dry_g"]
range_offset_high = hi_r - SLIDE["dry_g"]
R["dry_mass"] = {
    "sum_at_dose_basis_g": fmt(dry_dose_total, 4),
    "sum_at_slide_rounded_0p81g_g": fmt(SLIDE["khco3_g"] + SLIDE["citric_g"] + SLIDE["binder_g"]
                                        + SLIDE["flavour_g"] + sucr_mg / 1000.0, 4),
    "slide_dry_g": SLIDE["dry_g"],
    "match_3p79": round(dry_dose_total, 2) == SLIDE["dry_g"],
    "range_slide": list(SLIDE["dry_range"]),
    "range_from_allowances_low_high_g": [fmt(allow_low, 3), fmt(allow_high, 3)],
    "range_allowances_binder_0p5_1p2_flavour_0p02_0p10": "reproduces 3.46 and 4.24 g",
    "range_match": round(allow_low, 2) == lo_r and round(allow_high, 2) == hi_r,
    "single_driver_needed_for_range_ends": single,
    "pH_driver_mass_offsets_g": {
        "pH_3p3": fmt(mass_targets["3.3"]["ideal_g"] - SLIDE["citric_g"], 3),
        "pH_3p7": fmt(mass_targets["3.7"]["ideal_g"] - SLIDE["citric_g"], 3),
        # A meter reading of 3.5 (activity basis) needs 1.95 g; a concentration pH of 3.5 needs 1.85 g.
        "meter_pH_3p5_davies": fmt(mass_targets["3.5"]["davies_meter_pH_g"] - SLIDE["citric_g"], 3),
        "concentration_pH_3p5_davies": fmt(mass_targets["3.5"]["davies_conc_pH_g"] - SLIDE["citric_g"], 3),
    },
    "khco3_g_at_0p50_and_0p60_volume": [fmt(dose_050, 4), fmt(dose_060, 4)],
    "dose_driver_mass_offsets_g": {"0p50_volume": fmt(dose_050 - khco3_dose_g, 4),
                                   "0p60_volume": fmt(dose_060 - khco3_dose_g, 4),
                                   "dose_counted_at_20C": fmt(n_20C_dose * MM_KHCO3 - khco3_dose_g, 4)},
    "monohydrate_citric_offset_g": fmt(citric_stoich_dose_g * 0 + SLIDE["citric_g"] * (MM_CITRIC_MONO / MM_CITRIC - 1.0), 3),
    "range_offsets_from_central_g": [fmt(range_offset_low, 3), fmt(range_offset_high, 3)],
    "single_driver_offsets_inside_range": all(range_offset_low <= d <= range_offset_high for d in drivers_offsets),
    "single_driver_offsets_g": [fmt(d, 3) for d in drivers_offsets],
    "target_pH_range_that_reproduces_range_ends_ideal": [pH_at_range_ends[1], pH_at_range_ends[0]],
    "dry_mass_at_target_pH_3p3_and_3p7_ideal_g": [fmt(dry_at_pH_3p7, 3), fmt(dry_at_pH_3p3, 3)],
    "dose_volumes_for_range_ends": {
        "basis_A_citric_held_at_2p10g": dose_A,
        "basis_B_citric_rescaled_to_keep_pH_3p5_ideal": [fmt(dose_B_lo, 3), fmt(dose_B_hi, 3)],
        "dry_mass_basis_B_at_dose_volume_g": dose_B_masses,
    },
    "note": "Each single chemistry driver (target pH 3.3 or 3.7, meter pH, dose 0.50 or 0.60 volume, "
            "counting the dose at 20 C, monohydrate) moves the dry mass by an amount that lies inside "
            "the allowance range (single_driver_offsets_inside_range). A target pH of 3.3 to 3.7 "
            "nearly reproduces both ends of the range (dry_mass_at_target_pH_3p3_and_3p7_ideal_g against "
            "3.46 and 4.24 g). A dose range with the citric acid rescaled to keep pH 3.5 also lands "
            "near the ends (dose_volumes_for_range_ends, basis B); with the citric acid held at 2.10 g "
            "(basis A) the dose range needed is much wider. The ends themselves are set by the team's "
            "allowances, binder 0.5 to 1.2 g and flavour 0.02 to 0.10 g, added to the dose and citric "
            "acid used here, which give 3.46 and 4.24 g (ASSUMPTION, cited in "
            "rework/screen/cube_size_0_55.py from rework/48 section 6.1, not independently derived). "
            "That check is circular: it shows what the stated range is, not that the allowances are right.",
}

# ------------------------------------------------------------ 7. the 14 mm cube
cube_cm3 = (SLIDE["cube_mm"] / 10.0) ** 3
rho_tab = SLIDE["dry_g"] / cube_cm3
rho_tab_dose = dry_dose_total / cube_cm3
solid_v = (khco3_dose_g / DENS_KHCO3 + SLIDE["citric_g"] / DENS_CITRIC
           + SLIDE["binder_g"] / DENS_BINDER + SLIDE["flavour_g"] / DENS_FLAVOUR
           + (sucr_mg / 1000.0) / DENS_SUCRALOSE)
rho_true = dry_dose_total / solid_v


def porosity_with(rb):
    sv = (khco3_dose_g / DENS_KHCO3 + SLIDE["citric_g"] / DENS_CITRIC + SLIDE["binder_g"] / rb
          + SLIDE["flavour_g"] / DENS_FLAVOUR + (sucr_mg / 1000.0) / DENS_SUCRALOSE)
    return 1.0 - rho_tab_dose / (dry_dose_total / sv)


def cube_at(binder_g, flavour_g):
    """Dry mass, density and porosity of the 14 mm cube for a binder and flavour allowance (dose and
    citric acid as the central design)."""
    dry = khco3_dose_g + SLIDE["citric_g"] + sucr_mg / 1000.0 + binder_g + flavour_g
    sv = (khco3_dose_g / DENS_KHCO3 + SLIDE["citric_g"] / DENS_CITRIC + binder_g / DENS_BINDER
          + flavour_g / DENS_FLAVOUR + (sucr_mg / 1000.0) / DENS_SUCRALOSE)
    return {"dry_g": fmt(dry, 3), "density_g_cm3": fmt(dry / cube_cm3, 3),
            "porosity_pct": fmt(100.0 * (1.0 - sv / cube_cm3), 1)}


cube_range_ends = {"low_end_binder_0p5_flavour_0p02": cube_at(0.50, 0.02),
                   "central_binder_0p80_flavour_0p05": cube_at(SLIDE["binder_g"], SLIDE["flavour_g"]),
                   "high_end_binder_1p2_flavour_0p10": cube_at(1.20, 0.10)}
R["cube"] = {
    "range_ends_14mm_cube": cube_range_ends,
    "cube_volume_cm3": fmt(cube_cm3, 4),
    "density_g_cm3_at_3p79g": fmt(rho_tab, 4),
    "density_g_cm3_at_dose_basis": fmt(rho_tab_dose, 4),
    "true_density_mix_g_cm3": fmt(rho_true, 4),
    "porosity_pct": fmt(100.0 * (1.0 - rho_tab_dose / rho_true), 1),
    "porosity_pct_binder_1p2": fmt(100.0 * porosity_with(1.2), 1),
    "porosity_pct_binder_1p6": fmt(100.0 * porosity_with(1.6), 1),
    "reference_density_effervescent_g_cm3": "1.250 (UNVERIFIED: a conference-abstract snippet; the page returned HTTP 403)",
    "cube_side_mm_at_density_1p25": fmt((dry_dose_total / 1.25) ** (1 / 3) * 10, 2),
    "cube_side_mm_at_density_1p60": fmt((dry_dose_total / 1.60) ** (1 / 3) * 10, 2),
    "note": "Density 1.38 g/cm3 for a 14 mm cube at 3.79 g. Porosity follows from the true "
            "density of the mix (KHCO3 and citric acid are S; binder, flavour and sucralose "
            "densities are ASSUMPTIONS). The compaction benchmarks that were read are in "
            "R['compaction'].",
}

# Compaction plausibility (benchmarks read and saved in T9 effervescent_tablet_benchmarks.md)
FACE_MM2 = SLIDE["cube_mm"] ** 2              # 14 x 14 mm face of a square die (cube pressed in a square die)
PHARM_D_MM, PHARM_FORCE_KN, PHARM_MPA, PHARM_MASS_MG = 11.28, 20.0, 200.0, 350.0
PHARM_TRUE_DENS = 1.8246                      # P: Pharmaceutics 2025;17(5):676, calculated true density
RSC_POROSITY_UNCOATED_159MPA = 13.67          # P (saved extraction; PMC page returned a browser check on re-open)
JUNG_FORCE_KN, JUNG_D_MM = 70.0, 25.0         # S: Jungbunzlauer CITROCOAT EP white paper
pharm_area = math.pi * (PHARM_D_MM / 2.0) ** 2
jung_mpa = JUNG_FORCE_KN * 1000.0 / (math.pi * (JUNG_D_MM / 2.0) ** 2)
pharm_thick = {}
for por in (0.0, 0.10, 0.20):
    vol_mm3 = PHARM_MASS_MG / 1000.0 / (PHARM_TRUE_DENS * (1.0 - por)) * 1000.0   # mm3 (g / (g/cm3) = cm3 x 1000)
    pharm_thick[f"porosity_{int(por * 100)}pct_mm"] = fmt(vol_mm3 / pharm_area, 2)
force_kn = {f"{p:.1f}_MPa": fmt(p * FACE_MM2 / 1000.0, 1) for p in (jung_mpa, 159.0, 200.0)}
# Mass carried per unit of punch face (a proxy for the depth of the powder fill), cube against the
# sourced tablets. Tablet masses and diameters are as read (see effervescent_tablet_benchmarks.md and
# effervescent_hardness_benchmarks_N.md); the cube is 3.79 g on a 14 x 14 mm face.
cube_mg_per_mm2 = SLIDE["dry_g"] * 1000.0 / FACE_MM2
_tab = {"Pharmaceutics_2025_350mg_11p28mm_P": (PHARM_MASS_MG, pharm_area),
        "Jungbunzlauer_5g_25mm_S": (5000.0, math.pi * (25.0 / 2.0) ** 2),
        "Roquette_vitaminC_2400mg_20mm_S": (2400.0, math.pi * (20.0 / 2.0) ** 2)}
mass_per_face = {k: fmt(m / a, 2) for k, (m, a) in _tab.items()}
cube_over_tablet = {k: fmt(cube_mg_per_mm2 / (m / a), 2) for k, (m, a) in _tab.items()}
HARDNESS_BENCHMARKS_N = [
    {"source": "Ansar et al. 2009, Jurnal Teknologi dan Industri Pangan 20(1):25 (fruit juice effervescent tablet; abstract only)",
     "tier": "P (abstract; mass and diameter not stated)", "hardness_N": "40.53 (highest)", "compression_force_N": "2339.8 (highest hardness); 1417.6 (fastest dissolution, 41.99 s)"},
    {"source": "Taymouri et al. 2019, J Rep Pharm Sci 8(2):236 (bismuth subcitrate; abstract only)",
     "tier": "P (abstract; mass, diameter and force not stated)", "hardness_N": "72.3 +/- 5.5", "compression_force_N": "not stated"},
    {"source": "Jungbunzlauer CITROCOAT EP facts sheet, Figure 1 (5 g, 25 mm, 2 percent PEG 4000, n = 20)",
     "tier": "S (supplier sheet, undated; axis labelled N)", "hardness_N": "67.9 (hand mix, 70 kN); 117.8 (CITROCOAT EP, 70 kN); 70.2 (CITROCOAT EP, 44 kN)", "compression_force_N": "70000 and 44000"},
    {"source": "Roquette vitamin C effervescent tablet formulation page (2,400 mg, 20 mm flat punch)",
     "tier": "S (company technical page; thickness and force not stated)", "hardness_N": "100", "compression_force_N": "not stated"},
]
R["compaction"] = {
    "cube_face_mm2_square_die": FACE_MM2,
    "pressure_benchmarks_MPa": {"Pharmaceutics_2025_P": PHARM_MPA, "RSC_2019_max_P": 159.0,
                                "Jungbunzlauer_derived_S": fmt(jung_mpa, 1)},
    "force_on_14mm_face_kN_at_benchmark_pressures": force_kn,
    "Pharmaceutics_2025_check_20kN_over_area_MPa": fmt(PHARM_FORCE_KN * 1000.0 / pharm_area, 1),
    "design_porosity_pct": R["cube"]["porosity_pct"],
    "design_porosity_range_pct": [R["cube"]["porosity_pct_binder_1p2"], R["cube"]["porosity_pct_binder_1p6"]],
    "RSC_2019_porosity_uncoated_at_159MPa_pct": RSC_POROSITY_UNCOATED_159MPA,
    "design_relative_density": fmt(1.0 - R["cube"]["porosity_pct"] / 100.0, 3),
    "RSC_relative_density_at_159MPa": fmt(1.0 - RSC_POROSITY_UNCOATED_159MPA / 100.0, 4),
    "Pharmaceutics_2025_true_density_g_cm3": PHARM_TRUE_DENS,
    "design_true_density_g_cm3": R["cube"]["true_density_mix_g_cm3"],
    "Pharmaceutics_2025_tablet_thickness_mm_derived": pharm_thick,
    "Pharmaceutics_2025_height_to_diameter_range": [fmt(pharm_thick["porosity_0pct_mm"] / PHARM_D_MM, 3),
                                                    fmt(pharm_thick["porosity_20pct_mm"] / PHARM_D_MM, 3)],
    "cube_height_to_width": 1.0,
    "cube_mass_per_punch_face_mg_per_mm2": fmt(cube_mg_per_mm2, 2),
    "sourced_tablet_mass_per_punch_face_mg_per_mm2": mass_per_face,
    "cube_over_sourced_tablet_mass_per_face": cube_over_tablet,
    "hardness_benchmarks_in_newtons": HARDNESS_BENCHMARKS_N,
    "hardness_range_reported_N": [40.53, 117.8],
    "hardness_note": "Hardness values reported in newtons by effervescent tablet sources run from about 40 to "
                     "118 N (four sources, two of them peer-reviewed abstracts and two supplier pages). The "
                     "figures are diametral breaking forces of round flat tablets; a 14 mm cube has no "
                     "diameter, so its hardness is not comparable and is not predicted. No sourced bulk "
                     "density of a commercial effervescent tablet was found (the 1.250 g/cm3 lead stays "
                     "UNVERIFIED), because none of the opened sources gives tablet thickness.",
    "note": "Sourced effervescent tablets are round, flat and thin (mass about 350 mg at 11.28 mm, so "
            "roughly 2 mm thick, height to diameter about 0.2) and were pressed between 53 and 200 MPa. The "
            "design cube is 3.79 g with height equal to width (ratio 1.0), about 11 times the mass of "
            "the Pharmaceutics 2025 tablet. At those pressures the 196 mm2 face would need about 28 to "
            "39 kN (DERIVED). The design porosity (18.5 percent, estimated) is not tighter than the "
            "13.7 percent reached at 159 MPa by a different, 8.5 mm tablet, so the design density does "
            "not call for more compaction than a tablet reached. That does not show a 14 mm cube can "
            "be pressed: density gradients, die-wall friction, ejection, lamination, hardness and "
            "dissolution time of a cube-shaped body are not measured and no source for a cube was "
            "found. These are stated limits.",
}

# ------------------------------------------------------------ 8. pouch, pack and net weight
pouch_area_two_faces = 2.0 * POUCH_LAYOUT_MM[0] * POUCH_LAYOUT_MM[1] / 1e6   # m2
film_g = pouch_area_two_faces * LAMINATE_G_PER_M2
carton_m = [x / 1000.0 for x in SLIDE["carton_mm"]]
carton_m3 = carton_m[0] * carton_m[1] * carton_m[2]
per_layer = (int(SLIDE["carton_mm"][0] // POUCH_LAYOUT_MM[0]) * int(SLIDE["carton_mm"][1] // POUCH_LAYOUT_MM[1]))
per_layer_rot = (int(SLIDE["carton_mm"][0] // POUCH_LAYOUT_MM[1]) * int(SLIDE["carton_mm"][1] // POUCH_LAYOUT_MM[0]))
layers = int(SLIDE["carton_mm"][2] // POUCH_LAYOUT_MM[2])
CARTON_WALL_MM = 3.0     # ASSUMPTION, used only to test that eight pouches still fit inside
_in = [x - 2.0 * CARTON_WALL_MM for x in SLIDE["carton_mm"]]
per_layer_in = max(int(_in[0] // POUCH_LAYOUT_MM[0]) * int(_in[1] // POUCH_LAYOUT_MM[1]),
                   int(_in[0] // POUCH_LAYOUT_MM[1]) * int(_in[1] // POUCH_LAYOUT_MM[0]))
layers_in = int(_in[2] // POUCH_LAYOUT_MM[2])
R["pack"] = {
    "packed_calc_g": fmt(SLIDE["dry_g"] + SLIDE["pouch_g"], 3),
    "match_packed_5p29": round(SLIDE["dry_g"] + SLIDE["pouch_g"], 2) == SLIDE["packed_g"],
    "net_weight_rounding": round(SLIDE["dry_g"], 1) == SLIDE["net_g"],
    "pouch_mass_1p5_g_status": "ASSUMPTION (team value); cannot be checked from sources",
    "pouch_film_two_faces_m2": fmt(pouch_area_two_faces, 4),
    "pouch_film_mass_g_at_assumed_96_g_m2": fmt(film_g, 3),
    "pouch_mass_not_explained_by_film_g": fmt(SLIDE["pouch_g"] - film_g, 3),
    "carton_outside_volume_L": fmt(carton_m3 * 1000.0, 3),
    "carton_wall_mm_assumed_for_fit_test": CARTON_WALL_MM,
    "carton_inside_mm_at_assumed_wall": [x - 2.0 * CARTON_WALL_MM for x in SLIDE["carton_mm"]],
    "six_cube_volume_cm3": fmt(6.0 * cube_cm3, 2),
    "pouches_per_carton_layout_on_outside_size": {"per_layer": max(per_layer, per_layer_rot), "layers": layers,
                                                  "capacity": max(per_layer, per_layer_rot) * layers},
    "pouches_per_carton_layout_inside_assumed_wall": {"per_layer": per_layer_in, "layers": layers_in,
                                                      "capacity": per_layer_in * layers_in},
    "fits_six_pouches_outside_size": max(per_layer, per_layer_rot) * layers >= 6,
    "fits_six_pouches_inside_assumed_wall": per_layer_in * layers_in >= 6,
    "note": "The pouch size (90 x 70 x 20 mm) and mass (1.5 g) are the team's ASSUMPTIONS. The film at an "
            "assumed 96 g/m2 laminate weight (also an ASSUMPTION) explains about 1.21 g of the 1.5 g; "
            "the remaining 0.29 g is not explained by anything in this run, and no source was found "
            "for the pouch mass, so the 1.5 g cannot be checked. The carton 190 x 150 x 50 mm is the "
            "OUTSIDE size (submission 04); 1.425 L is the outside volume, which is the right basis for "
            "container packing. Two pouches fit across 190 mm and two down 150 mm, two layers at 50 mm "
            "height: eight on the outside size and still eight inside an assumed 3 mm wall; six are used.",
}

# ------------------------------------------------------------ 9. container
def container_numbers(dims, label, source):
    vol = dims["L"] * dims["W"] * dims["H"]
    carton_vol = carton_m3
    at92 = vol * SLIDE["pack_fraction"] / carton_vol
    implied = SLIDE["cartons_20ft"] * carton_vol / vol
    grid = {}
    for name, (along_L, along_W) in {"190_along_length": (190.0, 150.0),
                                      "150_along_length": (150.0, 190.0)}.items():
        nL = math.floor(dims["L"] * 1000.0 / along_L)
        nW = math.floor(dims["W"] * 1000.0 / along_W)
        nH_full = math.floor(dims["H"] * 1000.0 / 50.0)
        grid[name] = {"per_layer": nL * nW, "layers_full": nH_full,
                      "cartons_full_height": nL * nW * nH_full}
    door_layers = math.floor(ONE_20["door_H"] * 1000.0 / 50.0)
    door_counts = {k: v["per_layer"] * door_layers for k, v in grid.items()}
    mass_kg = at92 * (6.0 * (SLIDE["packed_g"] / 1000.0) + CARTON_MASS_KG)
    return {
        "source": source,
        "internal_volume_m3": fmt(vol, 4),
        "cartons_at_92pct": int(math.floor(at92)),
        "cubes_at_92pct": int(math.floor(at92)) * 6,
        "implied_packing_fraction_for_21431": fmt(implied, 4),
        "slide_cartons_difference_pct": fmt(100.0 * (SLIDE["cartons_20ft"] - math.floor(at92)) / math.floor(at92), 2),
        "grid_counts_full_height": grid,
        "grid_counts_door_height_2p28m": door_counts,
        "container_mass_kg_at_92pct_with_0p10kg_carton": fmt(mass_kg, 1),
        "mass_share_of_payload_28330_pct": fmt(100.0 * mass_kg / ONE_20["payload"], 1),
    }


R["container"] = {
    "ONE_page_P": container_numbers(ONE_20, "ONE", "ONE 20 ft dry page (P), read 2026-10-20"),
    "SeaCube_S": container_numbers(SEACUBE_20, "SeaCube", "SeaCube dimensions as in team's pack_economics.py (S, not reopened)"),
    "DSV_proxy_P": container_numbers(DSV_20, "DSV", "DSV generic 20 ft dry (P for DSV, rounded; PROXY)"),
    "slide_cartons": SLIDE["cartons_20ft"],
    "slide_cubes": SLIDE["cubes_20ft"],
    "cubes_check_6x": SLIDE["cartons_20ft"] * 6 == SLIDE["cubes_20ft"],
    "ONE_stated_cubic_m3": ONE_20["cubic_m3_stated"],
    "ONE_payload_kg": ONE_20["payload"],
    "payload_slide_t": 28.3,
    "payload_match_ONE": round(ONE_20["payload"] / 1000.0, 1) == 28.3,
    "door_height_layers_45": math.floor(ONE_20["door_H"] * 1000.0 / 50.0),
    "twelve_cube_carton_190x150x100_mm": {
        "outside_volume_L": fmt(0.190 * 0.150 * 0.100 * 1000.0, 3),
        "ONE_cartons_at_92pct": int(math.floor(ONE_20["L"] * ONE_20["W"] * ONE_20["H"] * SLIDE["pack_fraction"] / (0.190 * 0.150 * 0.100))),
        "ONE_cubes_at_92pct": 12 * int(math.floor(ONE_20["L"] * ONE_20["W"] * ONE_20["H"] * SLIDE["pack_fraction"] / (0.190 * 0.150 * 0.100))),
        "SeaCube_cartons_at_92pct": int(math.floor(SEACUBE_20["L"] * SEACUBE_20["W"] * SEACUBE_20["H"] * SLIDE["pack_fraction"] / (0.190 * 0.150 * 0.100))),
        "SeaCube_cubes_at_92pct": 12 * int(math.floor(SEACUBE_20["L"] * SEACUBE_20["W"] * SEACUBE_20["H"] * SLIDE["pack_fraction"] / (0.190 * 0.150 * 0.100))),
        "deck_and_submission_say": "128,580 cubes in 10,715 cartons (executive_summary line 30)",
    },
    "twenty_four_cube_carton_190x150x200_mm": {
        "ONE_cartons_at_92pct": int(math.floor(ONE_20["L"] * ONE_20["W"] * ONE_20["H"] * SLIDE["pack_fraction"] / (0.190 * 0.150 * 0.200))),
        "ONE_cubes_at_92pct": 24 * int(math.floor(ONE_20["L"] * ONE_20["W"] * ONE_20["H"] * SLIDE["pack_fraction"] / (0.190 * 0.150 * 0.200))),
        "SeaCube_cubes_at_92pct": 24 * int(math.floor(SEACUBE_20["L"] * SEACUBE_20["W"] * SEACUBE_20["H"] * SLIDE["pack_fraction"] / (0.190 * 0.150 * 0.200))),
        "team_copy_says": "128,568 (proposal/04_strategy.md line 93)",
    },
    "note": "ONE dimensions (P) give 21,386 cartons at 92 percent (a volume estimate); the slide's 21,431 "
            "is 92.0 percent of the SeaCube volume (S). The difference is 0.2 percent and is a source "
            "choice. The ONE page says individual containers may have different specifications. "
            "Full-height grid counts are about 21,850 to 22,000, but the 2.28 m door limits the "
            "stack to 45 layers (about 20,900 to 21,060 hand-loaded cartons), so the volume estimate "
            "is a ceiling to confirm with the carrier, not a loading plan. The carton is counted on its "
            "outside size.",
}

# ------------------------------------------------------------ 10. cost per cube
kg = lambda g: g / 1000.0
thb_per_kg = lambda cny_t: cny_t / 1000.0 * FX_THB_PER_CNY
cost_rows = {}
for name, mass_g, price in (
    ("KHCO3_food_grade", khco3_dose_g, GC["khco3"]),
    ("citric_acid_food_grade_rows", SLIDE["citric_g"], GC["citric"]),
    ("sucralose", sucr_mg / 1000.0, GC["sucralose"]),
    ("maltodextrin_binder", SLIDE["binder_g"], GC["maltodextrin"]),
):
    cost_rows[name] = {
        "mass_g": fmt(mass_g, 5),
        "THB_per_cube_low": fmt(kg(mass_g) * thb_per_kg(price["low"]), 5),
        "THB_per_cube_central": fmt(kg(mass_g) * thb_per_kg(price["central"]), 5),
        "THB_per_cube_high": fmt(kg(mass_g) * thb_per_kg(price["high"]), 5),
        "CNY_per_t_low_central_high": [price["low"], price["central"], price["high"]],
    }
reactants_low = sum(cost_rows[k]["THB_per_cube_low"] for k in ("KHCO3_food_grade", "citric_acid_food_grade_rows", "sucralose"))
reactants_central = sum(cost_rows[k]["THB_per_cube_central"] for k in ("KHCO3_food_grade", "citric_acid_food_grade_rows", "sucralose"))
reactants_high = sum(cost_rows[k]["THB_per_cube_high"] for k in ("KHCO3_food_grade", "citric_acid_food_grade_rows", "sucralose"))
reactants_unlabelled_citric = (cost_rows["KHCO3_food_grade"]["THB_per_cube_central"]
                               + kg(SLIDE["citric_g"]) * thb_per_kg(GC["citric_unlabelled"])
                               + cost_rows["sucralose"]["THB_per_cube_central"])
reactants_unlabelled_khco3 = (kg(khco3_dose_g) * thb_per_kg(GC["khco3_unlabelled"])
                              + cost_rows["citric_acid_food_grade_rows"]["THB_per_cube_central"]
                              + cost_rows["sucralose"]["THB_per_cube_central"])
elchemy_citric_thb = [kg(SLIDE["citric_g"]) * u * FX_USD_THB for u in ELCHEMY_CITRIC_FOOD_USD]
# Elchemy says food grade (form not stated) is USD 0.90 to 1.25 per kg and anhydrous costs 5 to 10
# percent more than monohydrate: the anhydrous reading of the range is 0.945 to 1.375 USD per kg.
elchemy_citric_anhydrous_thb = [kg(SLIDE["citric_g"]) * ELCHEMY_CITRIC_FOOD_USD[0] * ELCHEMY_ANHYDROUS_PREMIUM[0] * FX_USD_THB,
                                kg(SLIDE["citric_g"]) * ELCHEMY_CITRIC_FOOD_USD[1] * ELCHEMY_ANHYDROUS_PREMIUM[1] * FX_USD_THB]
# Cross-checks on the headline reactant total
_base_other = (cost_rows["KHCO3_food_grade"]["THB_per_cube_central"] + cost_rows["sucralose"]["THB_per_cube_central"])
reactants_anhydrous_rows = _base_other + kg(SLIDE["citric_g"]) * thb_per_kg(GC["citric_anhydrous_rows_median"])
reactants_monohydrate_mass = _base_other + kg(SLIDE["citric_g"] * MM_CITRIC_MONO / MM_CITRIC) * thb_per_kg(GC["citric"]["central"])
_cny_8 = lambda cny_t: cny_t / 1000.0 * FX_THB_PER_CNY_8OCT
reactants_fx_8oct = (kg(khco3_dose_g) * _cny_8(GC["khco3"]["central"])
                     + kg(SLIDE["citric_g"]) * _cny_8(GC["citric"]["central"])
                     + kg(sucr_mg / 1000.0) * _cny_8(GC["sucralose"]["central"]))
citric_price_cross = {"anhydrous_labelled_rows_median_CNY_t": GC["citric_anhydrous_rows_median"],
                      "food_grade_rows_median_CNY_t": GC["citric"]["central"],
                      "food_grade_rows_low_high_CNY_t": [GC["citric"]["low"], GC["citric"]["high"]],
                      "n_food_grade_rows": len(CITRIC_FOOD_GRADE_ROWS),
                      "n_anhydrous_rows": len(CITRIC_ANHYDROUS_ROWS)}
binder_mannitol_thb = kg(SLIDE["binder_g"]) * thb_per_kg(GC["mannitol"])
flavour_thb = {k: kg(SLIDE["flavour_g"]) * v for k, v in FLAVOUR_THB_PER_KG.items()}
priced_cost_central = SLIDE["cost_total"] - SLIDE["cost_reactants"] + reactants_central
priced_cost_mald = priced_cost_central + cost_rows["maltodextrin_binder"]["THB_per_cube_central"] + flavour_thb["central"]
priced_cost_mann = priced_cost_central + binder_mannitol_thb + flavour_thb["central"]
priced_cost_mald_low = (priced_cost_central + cost_rows["maltodextrin_binder"]["THB_per_cube_low"] + flavour_thb["low"])
priced_cost_mald_high = (priced_cost_central + cost_rows["maltodextrin_binder"]["THB_per_cube_high"] + flavour_thb["high"])
R["cost"] = {
    "slide_sum_check": fmt(SLIDE["cost_reactants"] + SLIDE["cost_pouch_print"] + SLIDE["cost_processing"]
                           + SLIDE["cost_carton"], 3),
    "match_4p09": round(SLIDE["cost_reactants"] + SLIDE["cost_pouch_print"] + SLIDE["cost_processing"]
                        + SLIDE["cost_carton"], 2) == SLIDE["cost_total"],
    "carton_per_cube_check_4p00_over_6": fmt(CARTON_6_THB / 6.0, 4),
    "carton_basis_is_per_cube_consistent": round(CARTON_6_THB / 6.0, 2) == SLIDE["cost_carton"],
    "FX_THB_per_CNY": fmt(FX_THB_PER_CNY, 4),
    "FX_THB_per_USD_BOT_mid": fmt(FX_USD_THB, 4),
    "reactant_rows": cost_rows,
    "reactants_THB_per_cube_low_central_high": [fmt(reactants_low, 4), fmt(reactants_central, 4), fmt(reactants_high, 4)],
    "reactants_slide_0p12_vs_central_diff": fmt(reactants_central - SLIDE["cost_reactants"], 4),
    "reactants_if_citric_unlabelled_6500": fmt(reactants_unlabelled_citric, 4),
    "reactants_if_KHCO3_unlabelled_5500": fmt(reactants_unlabelled_khco3, 4),
    "cross_check_elchemy_citric_food_grade_THB": [fmt(elchemy_citric_thb[0], 4), fmt(elchemy_citric_thb[1], 4)],
    "cross_check_elchemy_citric_anhydrous_THB": [fmt(elchemy_citric_anhydrous_thb[0], 4), fmt(elchemy_citric_anhydrous_thb[1], 4)],
    "citric_price_basis": citric_price_cross,
    "reactants_if_citric_from_anhydrous_labelled_rows_median": fmt(reactants_anhydrous_rows, 4),
    "reactants_if_citric_rows_are_monohydrate_mass_x1p094": fmt(reactants_monohydrate_mass, 4),
    "reactants_central_at_FX_8Oct_5p0275": fmt(reactants_fx_8oct, 4),
    "FX_THB_per_CNY_8Oct_sensitivity": fmt(FX_THB_PER_CNY_8OCT, 4),
    "binder_maltodextrin_THB_central": fmt(cost_rows["maltodextrin_binder"]["THB_per_cube_central"], 4),
    "binder_mannitol_unlabelled_THB": fmt(binder_mannitol_thb, 4),
    "flavour_THB_low_central_high": [fmt(flavour_thb["low"], 4), fmt(flavour_thb["central"], 4), fmt(flavour_thb["high"], 4)],
    "priced_cost_with_reactants_recomputed_THB": fmt(priced_cost_central, 4),
    "priced_cost_with_maltodextrin_and_flavour_THB": fmt(priced_cost_mald, 4),
    "priced_cost_with_mannitol_and_flavour_THB": fmt(priced_cost_mann, 4),
    "priced_cost_with_maltodextrin_and_flavour_low_high_THB": [fmt(priced_cost_mald_low, 4), fmt(priced_cost_mald_high, 4)],
    "note": "Prices: Guidechem rows (S) for China ex-works CNY per tonne, converted at the FRED H.10 "
            "cross rate of 9 Oct 2026, the latest observation in both series (P series). These are not "
            "Thai landed prices. Freight, duty, VAT on inputs and any Thai distributor price are not "
            "included. Potassium bicarbonate rows are labelled food grade. The citric central is the "
            "median of 15 food-grade-labelled rows (any form; the range is the lowest and highest "
            "row); the rows labelled anhydrous give a similar median but two of them are not labelled "
            "food grade. The sucralose rows are not labelled food grade, and the sucralose page looks "
            "like a static listing: both rows print the same price in every daily, weekly and monthly "
            "column (August to October) with zero change, and the page's update date (10 Oct 2026) is "
            "earlier than its daily columns (14 to 16 Oct). The reactant price basis therefore changes "
            "from the earlier UN Comtrade unit values (submission 02 line 50 and 07 line 38 describe "
            "0.118 and 0.12 that way) to Guidechem listing rows. The binder is not named; the "
            "maltodextrin page is dated 3 June 2026 (stale). Mannitol is priced from a row not "
            "labelled food grade. The flavour price (THB 300, 800 and 1,500 per kg) has no source and "
            "is an ASSUMPTION. The 4.09 total excludes binder and flavour (team's own note on slide 9).",
}

# ------------------------------------------------------------ 11. contribution
shelf_check = SLIDE["shelf_price_deck"] * SLIDE["exfactory_share"]
contrib_deck = SLIDE["planning_price"] - SLIDE["cost_total"]
R["contribution"] = {
    "planning_price_check_15x0p60": fmt(shelf_check, 3),
    "match_planning_price_9p00": round(shelf_check, 2) == SLIDE["planning_price"],
    "contribution_deck_9p00_minus_4p09": fmt(contrib_deck, 3),
    "match_contribution_4p91": round(contrib_deck, 2) == SLIDE["contribution"],
    "reading_if_9p00_were_shelf_wrong_reading": fmt(9.0 * 0.6 - SLIDE["cost_total"], 3),
    "VAT7_ex_shelf_15_then_60pct_minus_4p09": fmt(SLIDE["shelf_price_deck"] / 1.07 * 0.6 - SLIDE["cost_total"], 3),
    "with_repriced_reactants": fmt(SLIDE["planning_price"] - priced_cost_central, 3),
    "with_maltodextrin_and_flavour": fmt(SLIDE["planning_price"] - priced_cost_mald, 3),
    "with_mannitol_and_flavour": fmt(SLIDE["planning_price"] - priced_cost_mann, 3),
    "with_maltodextrin_and_flavour_low_high": [fmt(SLIDE["planning_price"] - priced_cost_mald_high, 3),
                                               fmt(SLIDE["planning_price"] - priced_cost_mald_low, 3)],
    "contribution_margin_pct_of_planning": fmt(100.0 * contrib_deck / SLIDE["planning_price"], 1),
    "note": "Planning ex-factory price 9.00 equals 60 percent of a THB 15 shelf price (ASSUMPTION, team "
            "slide 9 note). So 4.91 = 9.00 - 4.09 is correct on that basis. Applying the 60 percent to 9.00 "
            "again would be double counting. If the THB 15 shelf price includes 7 percent VAT, the "
            "VAT-exclusive base is 14.02, the ex-factory share gives 8.41, and the contribution 4.32. "
            "The 60 percent share is an ASSUMPTION with no sourced margin.",
}
sens_grid = {}
for share in (0.50, 0.55, 0.60, 0.65, 0.70):
    for shelf in (13.0, 15.0, 17.0):
        sens_grid[f"share{share:.2f}_shelf{shelf:.0f}"] = fmt(shelf * share - SLIDE["cost_total"], 3)
R["contribution"]["sensitivity_share_shelf_THB"] = sens_grid

# ------------------------------------------------------------ 11b. Thai mineral-salt beverage definition
# Thai FDA compilation copy of MoPH Notification 195 B.E. 2543, "Mineral-salt beverages"
# (https://exfood.fda.moph.go.th/law/data/complilation/Compi_195.pdf, page 1 read as an image on
# 20 Oct 2026; Thai text, our translation; tier P). Clause 3: a beverage in which mineral salts are
# the main ingredient. Clause 4(1), per litre: sodium 460 to 920 mg; glucose or fructose at least 2
# percent by weight, or sucrose at least 4 percent; potassium at most 195 mg (if present);
# bicarbonate at most 793 mg (if present); citrate at most 819 mg (if present).
N195 = {"Na_mg_per_L_min": 460.0, "Na_mg_per_L_max": 920.0, "K_mg_per_L_max": 195.0,
        "bicarbonate_mg_per_L_max": 793.0, "citrate_mg_per_L_max": 819.0,
        "glucose_or_fructose_pct_min": 2.0, "sucrose_pct_min": 4.0}
MM_CITRATE_ANION = molar_mass({"C": 6, "H": 5, "O": 7})                 # C6H5O7 (3-)
MM_K3CIT = 3.0 * MM_K + MM_CITRATE_ANION                               # tripotassium citrate
n_cit_dose = SLIDE["citric_g"] / MM_CITRIC
n_k3cit = n_khco3_dose / 3.0
k3cit_g = n_k3cit * MM_K3CIT
citric_left_g = (n_cit_dose - n_k3cit) * MM_CITRIC
solids_after_g = k3cit_g + citric_left_g + sucr_mg / 1000.0 + SLIDE["binder_g"] + SLIDE["flavour_g"]
citrate_anion_g = SLIDE["citric_g"] * MM_CITRATE_ANION / MM_CITRIC
R["thai_mineral_salt_beverage_195"] = {
    "limits_per_litre_as_read": N195,
    "design_potassium_mg_per_L_on_330mL": fmt(K_dose_mg / SERVE_L, 0),
    "potassium_over_195_limit_x": fmt(K_dose_mg / SERVE_L / N195["K_mg_per_L_max"], 2),
    "design_citrate_as_citric_acid_mg_per_L": fmt(SLIDE["citric_g"] * 1000.0 / SERVE_L, 0),
    "design_citrate_as_anion_mg_per_L": fmt(citrate_anion_g * 1000.0 / SERVE_L, 0),
    "citrate_over_819_limit_x_range": [fmt(citrate_anion_g * 1000.0 / SERVE_L / N195["citrate_mg_per_L_max"], 2),
                                       fmt(SLIDE["citric_g"] * 1000.0 / SERVE_L / N195["citrate_mg_per_L_max"], 2)],
    "design_sodium_mg_per_L": "0 by design (sodium-free); binder sodium not checked",
    "design_sugar_pct": 0.0,
    "meets_clause_4_composition": False,
    "potassium_citrate_g_formed": fmt(k3cit_g, 3),
    "citric_acid_left_g": fmt(citric_left_g, 3),
    "dissolved_solids_after_reaction_g": fmt(solids_after_g, 3),
    "potassium_citrate_share_of_solids_pct": fmt(100.0 * k3cit_g / solids_after_g, 1),
    "citric_acid_share_of_solids_pct": fmt(100.0 * citric_left_g / solids_after_g, 1),
    "citric_acid_share_of_cube_dry_mass_pct": fmt(100.0 * SLIDE["citric_g"] / dry_dose_total, 1),
    "note": "The cube drink does not meet the composition set for a mineral-salt beverage (no sodium, no "
            "sugar, about 4.9 times the potassium ceiling, about 7.6 to 7.8 times the citrate ceiling), "
            "so it could not be sold as one. Whether the Thai FDA treats a drink made from the cube "
            "as a flavoured drink (category 14.1.4) or as a mineral-salt beverage (Clause 3, mineral "
            "salts as the main ingredient) is not settled by the text read. Citric acid, not a mineral "
            "salt, is the largest solid in the glass. Classification is a stated limit. Condition TH3 "
            "in Notification 468 (annex list 2 part 2, printed page 835, read as a page image on 20 Oct "
            "2026) says that for mineral-salt beverage products the additive must be used together with "
            "sugar of the type and amount set in the mineral-salt beverage notification. The earlier "
            "saved reading of the repealed Notification 418 (TH3 excludes products under Notification "
            "195) is superseded: both tie TH3 to Notification 195, but the 468 text states the "
            "condition as a sugar-pairing duty on mineral-salt beverages. The cube drink has no sugar, "
            "so it could not be sold as a mineral-salt beverage with sucralose either.",
}
R["thai_notification_468_as_read_2026_10_20"] = {
    "source": "MoPH Notification 468 B.E. 2568 Annex (P468.pdf, 839 PDF pages, SHA-256 5BEB26FC...FF7C, "
              "identical to the file read on 19 Oct 2026); Thai text, our translation; page images read "
              "on 20 Oct 2026. PDF page = printed page + 1.",
    "rows_category_14_1_4_flavoured_drinks": {
        "sucralose_INS_955": {"max_mg_per_kg": 300, "conditions": ["127", "TH3"], "year_set_BE": 2559, "pdf_page": 678},
        "citric_acid_INS_330": {"max": "quantum satis", "conditions": [], "year_set_BE": 2559, "pdf_page": 197},
        "potassium_hydrogen_carbonate_INS_501ii": {"max": "quantum satis", "conditions": [], "year_set_BE": 2559, "pdf_page": 534},
    },
    "condition_127": "calculated in the ready-to-consume state (annex list 2 part 2, printed page 788, PDF 789)",
    "condition_TH3": "for mineral-salt beverage products, must be used together with sugar of the type and amount "
                     "prescribed in the MoPH notification on mineral-salt beverages (printed page 835, PDF 836)",
    "explanatory_announcement": {
        "source": "Announcement of the Office of the Food and Drug Board, explanatory statement of MoPH "
                  "Notification 468 (36 pages, 788 KB; dated 6 January B.E. 2569 = 6 January 2026 on page 5)",
        "quantum_satis_definition_page_2": "quantum satis means the lowest amount of the additive that gives the "
                                           "desired technological effect under GMP; it does not mean the additive "
                                           "may be added without limit; the operator must study its own product "
                                           "to find the lowest amount that gives the effect",
        "clause_4_page_2": "for additives in the same functional group that have numeric maxima, used together "
                           "(two or more), the sum of use-over-maximum ratios must not exceed one",
        "list_2_page_9": "additives whose maximum is quantum satis are not brought into the sum-of-ratios rule "
                         "even when in the same functional group",
    },
}
# Sum-of-ratios check for the sweetener group (only sucralose has a numeric maximum in the cube).
R["thai_notification_468_as_read_2026_10_20"]["sweetener_sum_of_ratios_for_the_design"] = {
    "sucralose_mg_per_kg_ready_to_drink": R["sucralose"]["mg_per_kg_on_330g_water"],
    "ratio_over_300": fmt(R["sucralose"]["mg_per_kg_on_330g_water"] / THAI_SUCRALOSE_CAT14_1_4, 3),
    "sum_of_ratios_one_numeric_sweetener": fmt(R["sucralose"]["mg_per_kg_on_330g_water"] / THAI_SUCRALOSE_CAT14_1_4, 3),
    "limit": 1.0,
    "note": "Only one numeric-maximum additive of the sweetener group is used, so the sum equals its ratio. "
            "Potassium bicarbonate and citric acid are quantum satis and are outside the sum.",
}
R["quantum_satis_citric_acid_basis"] = {
    "citric_acid_g_design": SLIDE["citric_g"],
    "citric_acid_g_stoichiometric": fmt(citric_stoich_dose_g, 4),
    "citric_acid_g_for_target_pH_ideal": {k: v["ideal_g"] for k, v in mass_targets.items()},
    "pH_at_stoichiometric_point_ideal": R["citric_pH"]["pH_at_stoichiometric_0p5186g_ideal"],
    "note": "Under quantum satis the 2.10 g has to be the lowest amount that gives the intended effect. "
            "The intended effect is the pH 3.5 target (an ASSUMPTION of the design); less acid gives a "
            "higher pH (citric_acid_g_for_target_pH_ideal), and the balance of that acid against 33 mg "
            "of sucralose is untasted. The stoichiometric mass alone leaves the drink alkaline.",
}

# ------------------------------------------------------------ 12. flags
R["flags"] = {
    "sweet_acid_ratio_note": "33 mg sucralose is about 6.0 g sugar equivalent per 100 mL. The added "
                             "citric acid is 6.36 g per litre, about 2.9 times an ingredient maker's "
                             "lemon-lime starting formula and 4.5 times the level that suppressed "
                             "sweetness by 28 percent in a published sucrose panel. The balance is an "
                             "untasted desk flag; the first lever is more sweetener or less acid.",
    "potassium_label_note": "If potassium is declared on a Thai nutrition panel, the rounding rule "
                            "gives 320 mg (9.1 percent of the Thai RDI). Whether a panel is required "
                            "is not settled: Notification 445 Clause 3 requires one only for foods with "
                            "a nutrition claim, a health claim or nutritional value used in promotion. "
                            "Potassium-retaining medicines and kidney disease need a medical view (Gate 2).",
    "sodium_note": "Sodium is not claimed: sodium-free wording is barred in the deck (deck_content.md) and "
                   "submission 09. The binder is not yet named, so its sodium content is unchecked.",
    "sucralose_child_note": "One serve is 2.2 mg/kg for a 15 kg child, about 15 percent of the EFSA ADI "
                            "and 44 percent of the FDA ADI.",
    "thai_regulation_note": "Notification 468 sets 300 mg/kg for category 14.1.4 (conditions 127 and "
                            "TH3; row reread on 20 Oct 2026 from page images). Potassium bicarbonate "
                            "and citric acid are quantum satis in that category, which the Thai FDA "
                            "explanatory announcement (page 2) defines as the lowest amount that gives the "
                            "technological effect under GMP, not an unlimited allowance. TH3 reads: for "
                            "mineral-salt beverage products the additive must be used together with sugar "
                            "of the type and amount prescribed in the mineral-salt beverage notification. "
                            "Classification (flavoured drink or mineral-salt beverage, Notification 195) "
                            "is a stated limit.",
    "net_weight_note": "Net weight 3.8 g is the rounded central dry mass 3.79 g, to be confirmed by "
                       "weighing before print; no pressing target above 3.79 g is proposed here.",
}

# ------------------------------------------------------------ 13. comparison with team files
# This block reads the team's saved outputs after every first-principles value above has been
# computed. It does not change any number above.
TEAM = {
    "handover_cost_6pack": 4.09,
    "handover_container_6pack_cartons": 21431,
    "handover_container_mass_kg": 2823.8,
    "handover_payload_kg_used": 28200.0,
    "handover_reactants_thb": 0.118,
    "valuation_cost_base_thb": 3.90,
    "valuation_contribution_base_thb": 5.10,
    "source": "rework/screen/handover_figures_results.json and project_valuation.py (read after "
              "computation; valuation comment '9.00 - 3.90 = 5.10' cites the 12-pack basis); "
              "rework/screen/pack_economics.py PRICES and CONTAINERS (payload 28,200 Maersk)",
}
R["team_comparison"] = {
    "team_container_mass_kg": TEAM["handover_container_mass_kg"],
    "team_payload_kg_used": TEAM["handover_payload_kg_used"],
    "payload_conflict_ONE_28330_vs_team_28200_kg": ONE_20["payload"] - TEAM["handover_payload_kg_used"],
    "valuation_cost_base_3p90_vs_slide_4p09_diff": fmt(TEAM["valuation_cost_base_thb"] - SLIDE["cost_total"], 3),
    "team_reactants_0p118_vs_repriced_central": fmt(TEAM["handover_reactants_thb"] - reactants_central, 4),
    "note": "Team container mass 2,823.8 kg is 10.0 percent of the ONE payload (28,330 kg); the team's "
            "payload input 28,200 kg is Maersk's figure, so the team files and the ONE page disagree by 130 kg. "
            "The valuation code comment '9.00 - 3.90 = 5.10' is stale: project_valuation_results.json "
            "uses the 6-pack base (cost 4.09, contribution 4.91), so the values agree and only the comment "
            "needs correcting.",
}

# ------------------------------------------------------------ write
out = {
    "meta": {
        "task": "T9 slide 7 specification revalidation (20 Oct 2026)",
        "script": os.path.join("rework", "screen", "spec_revalidation.py"),
        "python": sys.version.split()[0],
        "deterministic": True,
        "seed": "not applicable: no random draws",
        "revision": "second revision, 20 Oct 2026, after the second independent verification",
        "FX": {"THB_per_USD_BOT_mid_15Oct2026": fmt(FX_USD_THB, 4),
               "THB_per_CNY_FRED_cross_9Oct2026": fmt(FX_THB_PER_CNY, 4),
               "THB_per_CNY_FRED_cross_8Oct2026_sensitivity": fmt(FX_THB_PER_CNY_8OCT, 4)},
        "method": "First principles for chemistry, stoichiometry, geometry and cost arithmetic. Team "
                  "allowances (binder, flavour, pouch, laminate, carton mass and price, SeaCube "
                  "dimensions) are carried as stated ASSUMPTIONS; checks against them are circular.",
    },
    "inputs": {
        "slide": SLIDE, "ONE_20": ONE_20, "SEACUBE_20": SEACUBE_20, "DSV_20": DSV_20,
        "GC_rows": GC, "citric_food_grade_rows_CNY_per_t": CITRIC_FOOD_GRADE_ROWS,
        "citric_anhydrous_rows_CNY_per_t": CITRIC_ANHYDROUS_ROWS,
        "elchemy_citric_usd_per_kg": ELCHEMY_CITRIC_FOOD_USD,
        "elchemy_anhydrous_premium": ELCHEMY_ANHYDROUS_PREMIUM,
        "flavour_thb_per_kg": FLAVOUR_THB_PER_KG,
        "pouch_layout_mm": POUCH_LAYOUT_MM, "carton_mass_kg": CARTON_MASS_KG,
        "laminate_g_per_m2": LAMINATE_G_PER_M2, "carton_6_thb": CARTON_6_THB,
    },
    "results": R,
}
with open(OUT_JSON, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)

# ------------------------------------------------------------ summary
print("CO2 volumes per 330 mL at 0/20/30 C:", [co2[k]["volumes_per_330mL"] for k in ("0C", "20C", "30C")])
print("KHCO3 at 0.55 dose g:", fmt(khco3_dose_g, 4), " citric stoich g:", fmt(citric_stoich_dose_g, 4))
print("K mg dose basis:", fmt(K_dose_mg, 2), " from 0.81 g:", fmt(K_slide_mg, 2), " label mg:", label_round_mg(K_dose_mg))
print("pH ideal 2.10 g:", pH_ideal["pH"], " Davies conc:", pH_davies["pH_conc"], " Davies meter:", pH_davies["pH_meter"],
      " A f:", pH_davies["A_f"], " sensitivities:", sens)
print("mass for pH 3.5 (ideal, Davies conc, Davies meter):", mass_targets["3.5"])
print("taste:", {k: R["taste_benchmarks"][k] for k in ("design_citric_acid_g_per_L", "design_acid_over_Ingredion", "design_acid_over_Foods2020", "design_sugar_equivalent_over_Foods2020_sucrose", "design_acid_to_sweetness_ratio_over_Foods2020", "Foods2020_sweetness_drop_pct")})
print("compaction:", {k: R["compaction"][k] for k in ("force_on_14mm_face_kN_at_benchmark_pressures", "Pharmaceutics_2025_tablet_thickness_mm_derived", "Pharmaceutics_2025_height_to_diameter_range", "design_porosity_pct", "design_relative_density", "RSC_relative_density_at_159MPa")})
print("N195:", {k: R["thai_mineral_salt_beverage_195"][k] for k in ("design_potassium_mg_per_L_on_330mL", "potassium_over_195_limit_x", "citrate_over_819_limit_x_range", "potassium_citrate_share_of_solids_pct", "citric_acid_share_of_solids_pct", "citric_acid_share_of_cube_dry_mass_pct")})
print("sucralose mg/kg (330 g):", R["sucralose"]["mg_per_kg_on_330g_water"],
      " finished drink:", R["sucralose"]["mg_per_kg_on_finished_drink"])
print("dry mass dose basis:", fmt(dry_dose_total, 4), " allowance range:", fmt(allow_low, 3), fmt(allow_high, 3))
print("cube density:", R["cube"]["density_g_cm3_at_3p79g"], " porosity %:", R["cube"]["porosity_pct"])
print("pouches per carton outside/inside:", R["pack"]["pouches_per_carton_layout_on_outside_size"], R["pack"]["pouches_per_carton_layout_inside_assumed_wall"],
      " film g:", R["pack"]["pouch_film_mass_g_at_assumed_96_g_m2"], " unexplained g:", R["pack"]["pouch_mass_not_explained_by_film_g"])
print("12-cube carton:", R["container"]["twelve_cube_carton_190x150x100_mm"])
print("container ONE:", {k: R["container"]["ONE_page_P"][k] for k in ("cartons_at_92pct", "cubes_at_92pct", "implied_packing_fraction_for_21431", "container_mass_kg_at_92pct_with_0p10kg_carton", "mass_share_of_payload_28330_pct")})
print("container SeaCube:", R["container"]["SeaCube_S"]["cartons_at_92pct"], R["container"]["SeaCube_S"]["implied_packing_fraction_for_21431"])
print("door-limited grid (ONE):", R["container"]["ONE_page_P"]["grid_counts_door_height_2p28m"])
print("reactants THB low/central/high:", R["cost"]["reactants_THB_per_cube_low_central_high"],
      " unlabelled citric:", R["cost"]["reactants_if_citric_unlabelled_6500"],
      " unlabelled KHCO3:", R["cost"]["reactants_if_KHCO3_unlabelled_5500"])
print("reactants cross-checks: anhydrous rows", R["cost"]["reactants_if_citric_from_anhydrous_labelled_rows_median"],
      " monohydrate mass", R["cost"]["reactants_if_citric_rows_are_monohydrate_mass_x1p094"],
      " FX 8 Oct", R["cost"]["reactants_central_at_FX_8Oct_5p0275"],
      " Elchemy FG", R["cost"]["cross_check_elchemy_citric_food_grade_THB"], " Elchemy anhydrous", R["cost"]["cross_check_elchemy_citric_anhydrous_THB"],
      " citric basis", R["cost"]["citric_price_basis"])
print("binder maltodextrin:", R["cost"]["binder_maltodextrin_THB_central"], " mannitol:", R["cost"]["binder_mannitol_unlabelled_THB"])
print("priced cost:", R["cost"]["priced_cost_with_reactants_recomputed_THB"],
      R["cost"]["priced_cost_with_maltodextrin_and_flavour_THB"],
      R["cost"]["priced_cost_with_mannitol_and_flavour_THB"])
print("contribution deck:", R["contribution"]["contribution_deck_9p00_minus_4p09"],
      " VAT-ex:", R["contribution"]["VAT7_ex_shelf_15_then_60pct_minus_4p09"],
      " repriced:", R["contribution"]["with_repriced_reactants"],
      " with maltodextrin+flavour:", R["contribution"]["with_maltodextrin_and_flavour"],
      " with mannitol+flavour:", R["contribution"]["with_mannitol_and_flavour"])
print("CO2 volume at 60 F:", co2["60F_15p56C"]["volumes_per_330mL"], " pH at 0.52 g (ideal):", R["citric_pH"]["pH_at_exactly_0p52g_ideal"],
      " at stoich:", R["citric_pH"]["pH_at_stoichiometric_0p5186g_ideal"])
print("dry mass range checks:", {k: R["dry_mass"][k] for k in ("range_offsets_from_central_g", "single_driver_offsets_g", "single_driver_offsets_inside_range", "target_pH_range_that_reproduces_range_ends_ideal", "dry_mass_at_target_pH_3p3_and_3p7_ideal_g", "dose_volumes_for_range_ends")})
print("pH vs soft drinks:", {k: R["ph_vs_soft_drinks"][k] for k in ("pH_units_above_measured_drinks_ideal", "hydrogen_ion_ratio_drink_over_cube_ideal")})
print("mass per face:", R["compaction"]["cube_mass_per_punch_face_mg_per_mm2"], R["compaction"]["sourced_tablet_mass_per_punch_face_mg_per_mm2"], R["compaction"]["cube_over_sourced_tablet_mass_per_face"])
print("sweetener sum of ratios:", R["thai_notification_468_as_read_2026_10_20"]["sweetener_sum_of_ratios_for_the_design"]["sum_of_ratios_one_numeric_sweetener"])
print("cube at range ends:", R["cube"]["range_ends_14mm_cube"])
print("CO2 by temperature:", {k: (v["volumes_per_330mL"], v["KHCO3_g_for_0p55_volume_on_this_basis"], v["potassium_mg_for_0p55_volume_on_this_basis"]) for k, v in co2.items() if isinstance(v, dict)})
print("KHCO3 at 0.50 and 0.60 volume:", R["dry_mass"]["khco3_g_at_0p50_and_0p60_volume"])
print("Wrote", OUT_JSON)
