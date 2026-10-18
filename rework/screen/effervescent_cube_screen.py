#!/usr/bin/env python3
"""Effervescent lime soda cube screen: carbonate choice, cation load, Thai claim checks, 1 atm limit.

Question screened (Singha Ultimate Challenge 2026 entry, Thailand domestic only):
a dissolvable cube of citric acid plus a carbonate, dosed into a 330 ml sweetened drink (no sugar-free claim; see rework/45 S1).
Which carbonate gives the lowest sodium load at a usable fizz, and what do the Thai
nutrition-claim rules say about the result?

Standard library only. Reproduce with:
    python effervescent_cube_screen.py
Writes effervescent_cube_screen_results.json beside this file and prints a summary.

Status tags used in the output:
    sourced   value read from a public URL listed in SOURCES (read 2026-10-18)
    derived   computed here from sourced and/or assumed inputs
    assumed   chosen for this screen; basis stated; not measured
    snippet   seen only in a search snippet; page not read; not verified
    limit     could not be verified from available sources; closed as a stated limit
Prices: every price is a "public price" with page and read date, or "none".
No price is invented.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "effervescent_cube_screen_results.json")
READ_DATE = "2026-10-18"

# ---------------------------------------------------------------- sources
SOURCES = {
    "lange_bunsen_table": {
        "url": "https://en.wikipedia.org/wiki/Carbon_dioxide_(data_page)",
        "content": ("CO2 solubility in water at 101.3 kPa, volumes per volume at the given temperature: "
                    "0 C 1.713; 4 C 1.473; 5 C 1.424; 20 C 0.878; 25 C 0.759. Footnote: volume as measured "
                    "at 101.3 kPa and 0 C. Cited to Lange's Handbook of Chemistry, 10th ed., p. 1100."),
        "status": "sourced (WebFetch 2026-10-18; secondary page; same values as lime_cube_screen.py)",
    },
    "molar_mass_NaHCO3": {
        "url": "https://en.wikipedia.org/wiki/Sodium_bicarbonate",
        "content": "Infobox molar mass 84.006 g/mol (no reference marker on the value).",
        "status": "sourced (WebFetch 2026-10-18)",
    },
    "molar_mass_KHCO3": {
        "url": "https://en.wikipedia.org/wiki/Potassium_bicarbonate",
        "content": "Infobox molar mass 100.115 g/mol.",
        "status": "sourced (WebFetch 2026-10-18)",
    },
    "molar_mass_CaCO3": {
        "url": "https://en.wikipedia.org/wiki/Calcium_carbonate",
        "content": "Infobox molar mass 100.0869 g/mol.",
        "status": "sourced (WebFetch 2026-10-18)",
    },
    "molar_mass_citric_acid": {
        "url": "https://en.wikipedia.org/wiki/Citric_acid",
        "content": "Infobox molar mass 192.123 g/mol (anhydrous); 210.14 g/mol (monohydrate).",
        "status": "sourced (WebFetch 2026-10-18)",
    },
    "molar_mass_CO2_and_density": {
        "url": "https://en.wikipedia.org/wiki/Carbon_dioxide",
        "content": "Molar mass 44.009 g/mol; gas density 1.977 kg/m3 at 1 atm and 0 C.",
        "status": "sourced (WebFetch 2026-10-18)",
    },
    "calcium_citrate_solubility": {
        "url": "https://en.wikipedia.org/wiki/Calcium_citrate",
        "content": ("Anhydrous molar mass 498.4334 g/mol. Solubility in water 0.95 g/L at 25 C and "
                    "0.85 g/L at 18 C. Described as sparingly soluble."),
        "status": "sourced (WebFetch 2026-10-18; secondary page; solubility at 4 C not given)",
    },
    "atmospheric_CO2": {
        "url": "https://en.wikipedia.org/wiki/Carbon_dioxide_in_Earth%27s_atmosphere",
        "content": "In 2026 the CO2 concentration reached 432 ppm (0.0432 percent, molar basis); cites NASA Earth Science.",
        "status": "sourced (WebFetch 2026-10-18; secondary page)",
    },
    "thai_P445_nutrition_labelling": {
        "url": "https://food.fda.moph.go.th/media.php?id=689363893683888128&name=P445_EN.pdf",
        "content": ("Notification No. 445 B.E. 2566 (2023), English translation. Clause 2.1: a nutrition claim "
                    "follows Table 1 (per reference serving size and per consumed serving) for foods with a "
                    "reference serving, otherwise Table 2 (per 100 g or 100 mL). Annex 2 Category 2 No. 2: "
                    "carbonated and non-carbonated beverages, reference serving 200 mL. Table 1: free of sodium "
                    "less than 5 mg; very low sodium less than 35 mg; low sodium less than 140 mg (per serving); "
                    "sugar free less than 0.5 g (per serving). Table 2: sodium free not more than 5 mg, very low "
                    "40 mg (per 100 g) or 20 mg (per 100 mL), low 120 mg or 60 mg; sugar free not more than 0.5 g "
                    "(per 100 g and per 100 mL). Table 1 vitamins and minerals excluding sodium: good source more "
                    "than 15 percent of Thai RDI; high at least 30 percent. Clause 2.2: a claim needs an attached "
                    "statement when sodium exceeds 300 mg per serving. Annex 3 Thai RDI: sodium 2000 mg, "
                    "potassium 3500 mg, calcium 1000 mg. Clause 8: in force 180 days after gazette publication."),
        "status": "sourced (English PDF text extracted with pdftotext 2026-10-18; the Thai text is authoritative; "
                  "clause-to-table wording on dual basis needs a Thai adviser)",
    },
    "thai_P447_health_claims": {
        "url": "https://food.fda.moph.go.th/media.php?id=607838556769099776&name=P447_EN.pdf",
        "content": ("Notification No. 447 B.E. 2566 (2023), health claims. Clause 2(4): nutrition claims comply with "
                    "the Nutrition labelling notification (No. 445). Clause 3(3): function claims with sodium more "
                    "than 300 mg, total sugar more than 13 g, or other listed nutrients need a disclosure statement."),
        "status": "sourced (English PDF text extracted with pdftotext 2026-10-18); FDA list gives effective date 02/07/67",
    },
    "thai_P467_amendment": {
        "url": "https://food.fda.moph.go.th/media.php?id=841484892608012288&name=P467_EN.pdf",
        "content": ("Notification No. 467 B.E. 2568 (2025), Nutrition labelling (No. 2). Replaces only the display "
                    "font and format text in Annex 1 section 2.1 of No. 445. The claim tables (Table 1, Table 2) "
                    "are not mentioned. FDA list gives effective date 12/12/68."),
        "status": "sourced (English unofficial translation extracted with pdftotext 2026-10-18)",
    },
    "thai_fda_notification_list": {
        "url": "https://food.fda.moph.go.th/food-law/category/food-labeling-and-nutrition-labeling",
        "content": ("Lists P182 (1998, repealed), P445 (2023), P447 (2023, health claims), P466 (2025, GDA), "
                    "P467 (2025, nutrition labelling No. 2)."),
        "status": "sourced (WebFetch 2026-10-18)",
    },
    "healthier_choice_beverage": {
        "url": "https://food.chemlinked.com/news/food-news/thailand-updates-the-criteria-for-labeling-healthier-choice-nutritional-logo",
        "content": ("Healthier Choice logo, from 3 Jan 2025: beverages except 100 percent juice, sugar at most 5 g per "
                    "100 mL and 15 g per serving. No beverage sodium limit stated in the article."),
        "status": "sourced (WebFetch 2026-10-18; trade summary of the Thai FDA change; logo scheme, not a claim rule)",
    },
    "thai_sodium_intake_2021": {
        "url": "https://doaj.org/article/ecceca0bd5744d8f9dcc0c9a1782440a",
        "content": ("Estimated dietary sodium intake in Thailand, nationwide 24-hour urine study, J Clin Hypertens 2021: "
                    "mean 3636 mg/day (SD 1722) in 1599 completers; urinary potassium 1221 mg/day (excretion, not intake)."),
        "status": "snippet (WebSearch snippet only; the page was not read); unverified",
    },
    "thai_low_sugar_consumer": {
        "url": "https://www.kantar.com/inspiration/fmcg/60-of-thai-shoppers-are-still-consuming-no-sugar-carbonated-soft-drinks-out-of-the-home",
        "content": ("Kantar: 60 percent of Thai shoppers still consume no-sugar carbonated soft drinks out of home; most "
                    "Thai consumers want less or zero sugar that still tastes good (article c. 2023-2024)."),
        "status": "snippet (WebSearch snippet only; page not read); unverified; date older than 2026",
    },
    "singha_company_claim": {
        "url": "https://www.nationthailand.com/pr-news/40063747",
        "content": ("Company release: Singha Sparkling Water 330 ml, 0 percent calorie, 15 baht, March 2026; company cites "
                    "over 57 percent of Thai consumers cutting sugary drinks over five years."),
        "status": "snippet (company-cited claim; not read on page); unverified; treat as company claim",
    },
    "euromonitor_thailand_soft_drinks": {
        "url": "https://www-euromonitor-com.lib.ezproxy.hkust.edu.hk/hw-soft-drinks-in-thailand/report",
        "content": ("Euromonitor January 2026 overview: health and wellness shaped soft drinks in 2024; reformulation "
                    "ahead of phase 4 of the sugar tax in 2025."),
        "status": "snippet (overview only; full report paywalled); unverified",
    },
    "makro_pro_sodium_bicarbonate_search": {
        "url": "https://www.makro.pro/en/c/search?q=sodium+bicarbonate",
        "content": ("Makro PRO search page read via Claude Browser 2026-10-18 (page banner: 'Login to see accurate price "
                    "and promotions'). Listed prices shown without login: McGarrett Baking Soda 1 kg 107 baht (list 110); "
                    "BEST ODOUR Baking Soda 500 g 36 baht; Peter Rich Baking Soda 300 g 45 baht."),
        "status": "sourced (read on page 2026-10-18); public price, accurate member price not read",
    },
    "makro_pro_potassium_bicarbonate_search": {
        "url": "https://www.makro.pro/en/c/search?q=potassium+bicarbonate",
        "content": ("Makro PRO search, 576 hits, first page read 2026-10-18: no potassium bicarbonate product on the "
                    "first page. Same page lists 'Mizae PURE Food Grade baking soda 750 g, sodium bicarbonate 100 "
                    "percent' at 99 baht."),
        "status": "sourced (first page read 2026-10-18); potassium bicarbonate: none found on page 1",
    },
    "makro_pro_citric_acid_search": {
        "url": "https://www.makro.pro/en/c/search?q=citric+acid",
        "content": ("Makro PRO search, 355 hits, first page read 2026-10-18: 'Pack of 2, McGarrett citric acid (lemon "
                    "acid) 100 g' at 95 baht (list 100 baht)."),
        "status": "sourced (read on page 2026-10-18); public price; accurate member price not read",
    },
    "makro_pro_calcium_carbonate_search": {
        "url": "https://www.makro.pro/en/c/search?q=calcium+carbonate+food+grade",
        "content": ("Makro PRO search, 889 hits, first page read 2026-10-18: no food-grade calcium carbonate product; "
                    "results are supplements and milk powders."),
        "status": "sourced (first page read 2026-10-18); food-grade calcium carbonate: none found on page 1",
    },
    "retail_lazada_blocked": {
        "url": "https://www.lazada.co.th/catalog/?q=sodium%20bicarbonate%20food%20grade",
        "content": "Claude Browser navigation to lazada.co.th was denied or failed on 2026-10-18; no page read.",
        "status": "limit (site not read; site permission or access failed in this run; not bypassed)",
    },
    "pubchem_blocked": {
        "url": "https://pubchem.ncbi.nlm.nih.gov/compound/Sodium-bicarbonate",
        "content": ("WebFetch returned a browser verification screen ('Checking your browser') for PubChem pages on "
                    "2026-10-18. Not bypassed. Molar masses taken from Wikipedia infoboxes instead."),
        "status": "limit (bot check; not bypassed)",
    },
}

# ---------------------------------------------------------------- constants
R_GAS = 8.314462618                      # J/(mol K), exact SI value
P_STD_PA = 101325.0                      # Pa, 1 atm
T_STD_K = 273.15                         # K, 0 C
VM_IDEAL_L = R_GAS * T_STD_K / P_STD_PA * 1000.0   # L/mol, ideal gas at 0 C, 1 atm (derived, ~22.414)
RHO_CO2_STP = 1.977                      # g/L, CO2 gas at 0 C, 1 atm (sourced)
M_CO2 = 44.009                           # g/mol (sourced)
VM_REAL_L = M_CO2 / RHO_CO2_STP          # L/mol, real-gas alternative (derived, ~22.26)

# Standard atomic masses (assumed; used only to split sourced compound masses into element masses)
M_H, M_C, M_O = 1.008, 12.011, 15.999
M_CO3 = M_C + 3 * M_O                    # 60.008 (derived)
M_HCO3 = M_H + M_CO3                     # 61.016 (derived)

M_NA = 84.006 - M_HCO3                   # 22.990 (derived from sourced NaHCO3)
M_K = 100.115 - M_HCO3                   # 39.099 (derived from sourced KHCO3)
M_CA = 100.0869 - M_CO3                  # 40.079 (derived from sourced CaCO3)

M_NAHCO3 = 84.006                        # g/mol (sourced)
M_KHCO3 = 100.115                        # g/mol (sourced)
M_CACO3 = 100.0869                       # g/mol (sourced)
M_NA2CO3 = 2 * M_NA + M_CO3              # 105.988 (derived; comparator only)
M_CITRIC = 192.123                       # g/mol, C6H8O7 anhydrous (sourced)
M_CA_CITRATE = 498.4334                  # g/mol, Ca3(C6H5O7)2 anhydrous (sourced)
CA_CITRATE_SOL_25C = 0.95                # g/L (sourced, secondary page)
CA_CITRATE_SOL_18C = 0.85                # g/L (sourced, secondary page)

BUNSEN = {0: 1.713, 4: 1.473, 5: 1.424, 20: 0.878, 25: 0.759}   # volumes at 1 atm pure CO2 (sourced)
P_AIR_ATM = 0.000432                     # atm CO2 in open-air headspace, 432 ppm (sourced)

RDI = {"sodium_mg": 2000.0, "potassium_mg": 3500.0, "calcium_mg": 1000.0}   # Thai RDI, P445 Annex 3 (sourced)

# Case parameters (all assumed unless stated)
TARGET_VOLS = [1.5, 2.0, 3.5]            # volumes of CO2 retained as dissolved at serving (team brief range)
TEMPS_C = [4, 25]                        # serving temperatures (team computed task)
SERVING_ML = 330.0                       # drink volume per serving (team computed task)
REF_SERVING_ML = 200.0                   # Thai reference serving, carbonated beverage (sourced, P445 Annex 2)
F_RET_CASES = [1.0, 0.5, 0.25]           # fraction of generated CO2 still dissolved at serving (assumed; not measured)
E_ACID_BASE = 0.0                        # citric acid molar excess over stoichiometry, base case (assumed)
E_ACID_SENS = [0.10, 0.20]               # sensitivity cases (assumed)
USABLE_FIZZ_VOL = 1.5                    # lowest target in the brief; used as the "usable fizz" floor (assumed)

# Retail prices read from Makro PRO (public price, read 2026-10-18)
PUBLIC_PRICES = {
    "sodium_bicarbonate_food_grade_Mizae": {
        "price_baht": 99.0, "pack_g": 750.0,
        "label": "Mizae PURE Food Grade baking soda, sodium bicarbonate 100 percent, 750 g",
        "source": "makro_pro_potassium_bicarbonate_search",
        "status": "public price (read 2026-10-18; shown without login)",
    },
    "citric_acid_McGarrett_pack": {
        "price_baht": 95.0, "pack_g": 200.0,
        "label": "McGarrett citric acid (lemon acid) 100 g, pack of 2 (200 g total)",
        "source": "makro_pro_citric_acid_search",
        "status": "public price (read 2026-10-18; shown without login)",
    },
    "sodium_bicarbonate_McGarrett_1kg": {
        "price_baht": 107.0, "pack_g": 1000.0,
        "label": "McGarrett Baking Soda 1 kg (baking soda; food-grade status not stated)",
        "source": "makro_pro_sodium_bicarbonate_search",
        "status": "public price (read 2026-10-18; shown without login)",
    },
}

# ---------------------------------------------------------------- carbonate choices
CHOICES = [
    {
        "id": "NaHCO3",
        "name": "sodium bicarbonate",
        "citric_per_mol_CO2": 1.0 / 3.0,
        "reaction": "C6H8O7 + 3 NaHCO3 -> Na3C6H5O7 + 3 CO2 + 3 H2O",
        "components": [{"formula": "NaHCO3", "mol_per_mol_CO2": 1.0, "M": M_NAHCO3,
                        "cations": [("Na", 1, M_NA)]}],
    },
    {
        "id": "KHCO3",
        "name": "potassium bicarbonate",
        "citric_per_mol_CO2": 1.0 / 3.0,
        "reaction": "C6H8O7 + 3 KHCO3 -> K3C6H5O7 + 3 CO2 + 3 H2O",
        "components": [{"formula": "KHCO3", "mol_per_mol_CO2": 1.0, "M": M_KHCO3,
                        "cations": [("K", 1, M_K)]}],
    },
    {
        "id": "CaCO3",
        "name": "calcium carbonate",
        "citric_per_mol_CO2": 2.0 / 3.0,
        "reaction": "2 C6H8O7 + 3 CaCO3 -> Ca3(C6H5O7)2 + 3 CO2 + 3 H2O",
        "components": [{"formula": "CaCO3", "mol_per_mol_CO2": 1.0, "M": M_CACO3,
                        "cations": [("Ca", 1, M_CA)]}],
    },
    {
        "id": "NaHCO3_KHCO3_50_50",
        "name": "50:50 mol blend of sodium and potassium bicarbonate",
        "citric_per_mol_CO2": 1.0 / 3.0,
        "reaction": "C6H8O7 + 1.5 NaHCO3 + 1.5 KHCO3 -> 3 CO2 + Na1.5K1.5C6H5O7 + 3 H2O (mol-weighted)",
        "components": [
            {"formula": "NaHCO3", "mol_per_mol_CO2": 0.5, "M": M_NAHCO3, "cations": [("Na", 1, M_NA)]},
            {"formula": "KHCO3", "mol_per_mol_CO2": 0.5, "M": M_KHCO3, "cations": [("K", 1, M_K)]},
        ],
    },
    {
        "id": "Na2CO3",
        "name": "sodium carbonate (comparator only)",
        "citric_per_mol_CO2": 2.0 / 3.0,
        "reaction": "2 C6H8O7 + 3 Na2CO3 -> 2 Na3C6H5O7 + 3 CO2 + 3 H2O",
        "components": [{"formula": "Na2CO3", "mol_per_mol_CO2": 1.0, "M": M_NA2CO3,
                        "cations": [("Na", 2, M_NA)]}],
    },
]


# ---------------------------------------------------------------- functions
def bunsen(t_c):
    """Bunsen volumes (1 atm pure CO2) at t_c, linear between sourced points."""
    pts = sorted(BUNSEN.items())
    if t_c <= pts[0][0]:
        return pts[0][1]
    if t_c >= pts[-1][0]:
        return pts[-1][1]
    for (t1, v1), (t2, v2) in zip(pts, pts[1:]):
        if t1 <= t_c <= t2:
            return v1 + (v2 - v1) * (t_c - t1) / (t2 - t1)
    raise ValueError("unreachable")


def co2_mol(vol_v, serving_ml, vm=VM_IDEAL_L):
    """Moles of CO2 for vol_v volumes (STP) in serving_ml of liquid."""
    return vol_v * (serving_ml / 1000.0) / vm


def stoich_per_mol_co2(choice):
    """Per mol CO2: carbonate mass (g), cation mass by element (g), citric acid mass (g)."""
    carb_g = 0.0
    cat_g = {}
    for c in choice["components"]:
        carb_g += c["mol_per_mol_CO2"] * c["M"]
        for el, n_per, m_el in c["cations"]:
            cat_g[el] = cat_g.get(el, 0.0) + c["mol_per_mol_CO2"] * n_per * m_el
    acid_g = choice["citric_per_mol_CO2"] * M_CITRIC
    return carb_g, cat_g, acid_g


def dose(choice, vol_gen, serving_ml, e_acid=E_ACID_BASE, vm=VM_IDEAL_L):
    """Reactant masses and cation load for vol_gen volumes of CO2 generated in serving_ml."""
    n = co2_mol(vol_gen, serving_ml, vm)
    carb_per, cat_per, acid_per = stoich_per_mol_co2(choice)
    carb_g = n * carb_per
    acid_g = n * acid_per * (1.0 + e_acid)
    cations_mg = {el: n * g * 1000.0 for el, g in cat_per.items()}
    return {
        "co2_generated_mol": n,
        "carbonate_g": carb_g,
        "citric_acid_g": acid_g,
        "cube_reactant_g": carb_g + acid_g,
        "cation_mg": cations_mg,
        "gas_generated_ml_STP": vol_gen * serving_ml,
    }


def thai_check(cation_mg, serving_ml):
    """Thai nutrition-claim checks for the carbonate-derived cations only."""
    na = cation_mg.get("Na", 0.0)
    k = cation_mg.get("K", 0.0)
    ca = cation_mg.get("Ca", 0.0)
    na100 = na * 100.0 / serving_ml
    k_pct = 100.0 * k / RDI["potassium_mg"]
    ca_pct = 100.0 * ca / RDI["calcium_mg"]
    return {
        "sodium_scope_note": "carbonate-derived sodium only; sodium in the base drink was not read",
        "sodium_mg": round(na, 1),
        "sodium_mg_per_100ml": round(na100, 1),
        "sodium_free_claim_table1_lt5mg": na < 5.0,
        "sodium_very_low_claim_table1_lt35mg": na < 35.0,
        "sodium_low_claim_table1_lt140mg": na < 140.0,
        "sodium_low_claim_table2_le60mg_per_100ml": na100 <= 60.0,
        "sodium_disclosure_triggered_gt300mg": na > 300.0,
        "potassium_mg": round(k, 1),
        "potassium_pct_thai_rdi": round(k_pct, 1),
        "potassium_good_source_gt15pct": k_pct > 15.0,
        "potassium_high_ge30pct": k_pct >= 30.0,
        "calcium_mg": round(ca, 1),
        "calcium_pct_thai_rdi": round(ca_pct, 1),
        "calcium_good_source_gt15pct": ca_pct > 15.0,
        "calcium_high_ge30pct": ca_pct >= 30.0,
    }


def saturation_check(vol_target, t_c):
    b = bunsen(t_c)
    eq_open = b * P_AIR_ATM
    return {
        "temperature_C": t_c,
        "bunsen_volumes_at_1atm_pure_CO2_sourced": b,
        "required_CO2_partial_pressure_atm_linear_henry_assumed": round(vol_target / b, 4),
        "feasible_at_1atm_pure_CO2_headspace": vol_target <= b,
        "open_glass_equilibrium_dissolved_vol_air_432ppm_derived": round(eq_open, 6),
        "target_over_open_glass_equilibrium_x": round(vol_target / eq_open, 0),
    }


def calcium_check(vol_target, serving_ml=SERVING_ML):
    """Calcium citrate formed if the CaCO3 route is run to vol_target; compare with sourced solubility."""
    n = co2_mol(vol_target, serving_ml)
    ca_g = n * M_CA
    cit_salt_g = ca_g * M_CA_CITRATE / (3.0 * M_CA)
    conc = cit_salt_g / (serving_ml / 1000.0)
    return {
        "calcium_mg_per_serving": round(ca_g * 1000.0, 1),
        "calcium_citrate_salt_g_per_serving": round(cit_salt_g, 3),
        "calcium_citrate_g_per_L": round(conc, 3),
        "ratio_to_25C_solubility": round(conc / CA_CITRATE_SOL_25C, 2),
        "within_25C_solubility": conc <= CA_CITRATE_SOL_25C,
    }


def calcium_max_vol(serving_ml=SERVING_ML):
    """Largest CO2 volume the CaCO3 route can reach before calcium citrate reaches 25 C solubility."""
    cit_max = CA_CITRATE_SOL_25C * (serving_ml / 1000.0)
    ca_max_g = cit_max * 3.0 * M_CA / M_CA_CITRATE
    n_max = ca_max_g / M_CA
    return n_max * VM_IDEAL_L / (serving_ml / 1000.0)


def find_row(rows, choice, v, f):
    for r in rows:
        if r["choice"] == choice and r["retained_target_vol"] == v and r["fraction_retained_assumed"] == f:
            return r
    raise KeyError((choice, v, f))


# ---------------------------------------------------------------- main
def main():
    # 1 stoichiometry per mol CO2
    stoich = {}
    for ch in CHOICES:
        carb_per, cat_per, acid_per = stoich_per_mol_co2(ch)
        stoich[ch["id"]] = {
            "name": ch["name"],
            "reaction": ch["reaction"],
            "citric_mol_per_mol_CO2": round(ch["citric_per_mol_CO2"], 6),
            "carbonate_g_per_mol_CO2": round(carb_per, 4),
            "citric_acid_g_per_mol_CO2": round(acid_per, 4),
            "cation_g_per_mol_CO2": {k: round(v, 4) for k, v in cat_per.items()},
        }

    # 2 saturation (1 atm) check
    saturation = []
    for v in TARGET_VOLS:
        for t in TEMPS_C:
            saturation.append({"target_retained_vol": v, **saturation_check(v, t)})

    # 3 dose table: carbonate mass and cation load per serving, with Thai checks
    dose_rows = []
    for ch in CHOICES:
        for v in TARGET_VOLS:
            for f in F_RET_CASES:
                vol_gen = v / f
                d330 = dose(ch, vol_gen, SERVING_ML)
                d200 = dose(ch, vol_gen, REF_SERVING_ML)
                dose_rows.append({
                    "choice": ch["id"],
                    "retained_target_vol": v,
                    "fraction_retained_assumed": f,
                    "generated_vol_required": round(vol_gen, 4),
                    "escaped_vol_assumed": round(vol_gen - v, 4),
                    "serving_330ml": {
                        "co2_generated_mol": round(d330["co2_generated_mol"], 6),
                        "carbonate_g": round(d330["carbonate_g"], 4),
                        "citric_acid_g_stoich": round(d330["citric_acid_g"], 4),
                        "cube_reactant_g": round(d330["cube_reactant_g"], 4),
                        "gas_generated_ml_STP": round(d330["gas_generated_ml_STP"], 1),
                        "cation_mg": {k: round(x, 1) for k, x in d330["cation_mg"].items()},
                        "thai_check": thai_check(d330["cation_mg"], SERVING_ML),
                    },
                    "reference_200ml": {
                        "cation_mg": {k: round(x, 1) for k, x in d200["cation_mg"].items()},
                        "thai_check": thai_check(d200["cation_mg"], REF_SERVING_ML),
                    },
                })

    # 4 citric acid excess sensitivity (acid only; cation load unchanged)
    excess = []
    for ch in CHOICES:
        for e in [E_ACID_BASE] + E_ACID_SENS:
            d = dose(ch, USABLE_FIZZ_VOL, SERVING_ML, e_acid=e)
            excess.append({
                "choice": ch["id"],
                "citric_excess_fraction_assumed": e,
                "citric_acid_g_per_330ml_at_1.5vol_f1": round(d["citric_acid_g"], 4),
                "cation_mg_unchanged": {k: round(x, 1) for k, x in d["cation_mg"].items()},
            })

    # 5 volume-definition sensitivity (ideal gas vs real-gas density basis)
    vol_def = []
    for ch in CHOICES[:2]:
        d_i = dose(ch, USABLE_FIZZ_VOL, SERVING_ML, vm=VM_IDEAL_L)
        d_r = dose(ch, USABLE_FIZZ_VOL, SERVING_ML, vm=VM_REAL_L)
        vol_def.append({
            "choice": ch["id"],
            "cation_mg_ideal_22.414": {k: round(x, 1) for k, x in d_i["cation_mg"].items()},
            "cation_mg_real_density_22.26": {k: round(x, 1) for k, x in d_r["cation_mg"].items()},
            "difference_pct": round(100.0 * (d_r["cation_mg"][list(d_r["cation_mg"])[0]]
                                             / d_i["cation_mg"][list(d_i["cation_mg"])[0]] - 1.0), 2),
        })

    # 6 calcium citrate precipitation check (CaCO3 route)
    ca_check = {str(v): calcium_check(v) for v in TARGET_VOLS}
    ca_check["max_CO2_volumes_before_25C_saturation"] = round(calcium_max_vol(), 3)

    # 7 ranking at the usable fizz floor
    ranking = {}
    for f in F_RET_CASES:
        rows = []
        for ch in CHOICES:
            r = find_row(dose_rows, ch["id"], USABLE_FIZZ_VOL, f)
            ca_ok = True
            if "Ca" in r["serving_330ml"]["cation_mg"]:
                ca_ok = calcium_check(USABLE_FIZZ_VOL)["within_25C_solubility"]
            rows.append({
                "choice": ch["id"],
                "sodium_mg_per_330ml": r["serving_330ml"]["cation_mg"].get("Na", 0.0),
                "potassium_mg_per_330ml": r["serving_330ml"]["cation_mg"].get("K", 0.0),
                "calcium_mg_per_330ml": r["serving_330ml"]["cation_mg"].get("Ca", 0.0),
                "cube_reactant_g_per_330ml": r["serving_330ml"]["cube_reactant_g"],
                "calcium_citrate_within_25C_solubility": ca_ok,
            })
        eligible = [x for x in rows if x["calcium_citrate_within_25C_solubility"]]
        best = min(eligible, key=lambda x: (x["sodium_mg_per_330ml"], x["cube_reactant_g_per_330ml"]))
        ranking["f_ret_%s" % f] = {
            "rows": rows,
            "lowest_sodium_passing_solubility": best["choice"],
            "lowest_sodium_value_mg": best["sodium_mg_per_330ml"],
        }

    # 8 public price cost, ingredient only (derived from public prices above)
    price_per_g = {k: v["price_baht"] / v["pack_g"] for k, v in PUBLIC_PRICES.items()}
    cost_rows = []
    for v in TARGET_VOLS:
        r = find_row(dose_rows, "NaHCO3", v, 1.0)
        carb = r["serving_330ml"]["carbonate_g"]
        acid = r["serving_330ml"]["citric_acid_g_stoich"]
        carb_baht = carb * price_per_g["sodium_bicarbonate_food_grade_Mizae"]
        acid_baht = acid * price_per_g["citric_acid_McGarrett_pack"]
        cost_rows.append({
            "choice": "NaHCO3",
            "retained_target_vol": v,
            "fraction_retained_assumed": 1.0,
            "carbonate_g": round(carb, 4),
            "carbonate_baht_public_price_derived": round(carb_baht, 3),
            "citric_acid_g": round(acid, 4),
            "citric_acid_baht_public_price_derived": round(acid_baht, 3),
            "ingredient_total_baht_derived": round(carb_baht + acid_baht, 3),
            "scope": "ingredient only; excludes tablet forming, packaging, flavour, sweetener, freight and margin",
        })
    cost_rows.append({
        "choice": "KHCO3", "cost": "none (no potassium bicarbonate on the first page of the Makro PRO search)"})
    cost_rows.append({
        "choice": "CaCO3", "cost": "none (no food-grade calcium carbonate on the first page of the Makro PRO search)"})

    # 9 headline numbers for the verdict
    n15 = find_row(dose_rows, "NaHCO3", 1.5, 1.0)
    k15 = find_row(dose_rows, "KHCO3", 1.5, 1.0)
    k20 = find_row(dose_rows, "KHCO3", 2.0, 1.0)
    na15_f05 = find_row(dose_rows, "NaHCO3", 1.5, 0.5)
    na15_f025 = find_row(dose_rows, "NaHCO3", 1.5, 0.25)
    verdict = {
        "lowest_sodium_at_usable_fizz": (
            "Potassium bicarbonate (KHCO3) with citric acid. The carbonate itself delivers 0 mg sodium. "
            "At the 1.5 volume floor and full retention it delivers %.0f mg potassium per 330 ml (%.1f percent of Thai RDI). "
            "Calcium carbonate also delivers 0 mg sodium, but calcium citrate reaches its 25 C solubility at about %.2f volumes, "
            "so the calcium route cannot reach the 1.5 volume floor without precipitate." % (
                k15["serving_330ml"]["cation_mg"]["K"],
                k15["serving_330ml"]["thai_check"]["potassium_pct_thai_rdi"],
                ca_check["max_CO2_volumes_before_25C_saturation"])),
        "sodium_based_routes_at_1.5vol": {
            "NaHCO3_f1": n15["serving_330ml"]["cation_mg"]["Na"],
            "NaHCO3_f0.5": na15_f05["serving_330ml"]["cation_mg"]["Na"],
            "NaHCO3_f0.25": na15_f025["serving_330ml"]["cation_mg"]["Na"],
            "NaHCO3_KHCO3_blend_f1": find_row(dose_rows, "NaHCO3_KHCO3_50_50", 1.5, 1.0)["serving_330ml"]["cation_mg"]["Na"],
            "Na2CO3_f1": find_row(dose_rows, "Na2CO3", 1.5, 1.0)["serving_330ml"]["cation_mg"]["Na"],
        },
        "sodium_scales_with_1_over_f_retained": True,
        "thai_claim_consequence": (
            "Sodium-bicarbonate routes exceed the 140 mg low-sodium limit per 330 ml at every usable target (508 mg at 1.5 volumes, "
            "full retention), and exceed 300 mg per 200 ml reference serving at 1.5 volumes, which triggers the sodium "
            "disclosure rule. The potassium route has 0 mg carbonate sodium. Its potassium is %.1f percent of Thai RDI per "
            "330 ml and %.1f percent per 200 ml at 1.5 volumes (good source needs more than 15 percent; high needs at least "
            "30 percent). At 2.0 volumes it is %.1f percent per 330 ml (high per 330 ml) and %.1f percent per 200 ml. "
            "Potassium is printed on the Thai nutrition panel." % (
                k15["serving_330ml"]["thai_check"]["potassium_pct_thai_rdi"],
                k15["reference_200ml"]["thai_check"]["potassium_pct_thai_rdi"],
                k20["serving_330ml"]["thai_check"]["potassium_pct_thai_rdi"],
                k20["reference_200ml"]["thai_check"]["potassium_pct_thai_rdi"])),
        "reading_caveat": ("The dual-basis wording of Table 1 (reference serving and consumed serving) is read here as: both "
                           "must hold. A Thai adviser must confirm it."),
        "bench_test_first": [
            "Dissolved CO2 at 4 C and 25 C in open glass, sampled at 0, 30, 60 and 120 s (f_ret per carbonate). This is the "
            "measurement that replaces the f_ret assumption.",
            "Gas yield per cube in a closed flask by mass loss, against stoichiometry (confirms 3 CO2 per citric acid for "
            "bicarbonate and 3 CO2 per 2 citric acid for carbonate).",
            "Cation content per serving by ICP-OES or flame photometry (Na, K, Ca), with the base drink's own sodium measured "
            "separately.",
            "Calcium route only: visible precipitate or turbidity after 24 h at 4 C.",
            "Pass rule to be set before the run by the team; no rule is set in this screen.",
        ],
    }

    open_items = [
        "Base drink sodium (Singha Sparkling Water Lime label not read). The sodium-free claim for the potassium route depends on it.",
        "Dual-basis reading of Thai Table 1 (reference serving and consumed serving) needs a Thai adviser.",
        "Whether a dissolvable cube is classed as a food under the nutrition-labelling rules, or under another category, is not settled here.",
        "f_ret (fraction of generated CO2 still dissolved at serving) is assumed, not measured. Every sodium and potassium figure scales as 1/f_ret.",
        "Calcium citrate solubility at 4 C is not sourced. The 25 C value is used. Acid, pH and other solutes in a flavoured drink may change it.",
        "Potassium bicarbonate price: none found. Calcium carbonate price: none found on Makro PRO first page. Lazada and PubChem were not read.",
        "Potassium citrate solubility is not sourced. Potassium citrate concentration is not checked against solubility.",
        "Henry's law is taken linear from 1 atm to the required pressure. The real pressure dependence is not checked.",
        "Thai Notification 447 and 445 text was read in English translation. The Thai text is authoritative and was not read.",
        "Healthier Choice logo beverage sugar limit (5 g per 100 ml) is a logo scheme, not a claim rule. Not applied here.",
    ]

    limits = [
        "Lazada: navigation denied or failed in Claude Browser; not read.",
        "PubChem: bot check on WebFetch; not bypassed; molar masses taken from Wikipedia.",
        "Makro PRO: prices shown without login, but the page says accurate prices need login; login not used; prices are public prices only.",
        "Potassium bicarbonate and food-grade calcium carbonate: not found on the first search page of Makro PRO.",
        "Snippet-only sources (sodium intake, Kantar, Singha claim, Euromonitor) are marked unverified.",
    ]

    result = {
        "meta": {
            "screen": "effervescent_cube_screen.py",
            "scope": "Thailand domestic only; Singapore and Korea excluded",
            "product": "Sweetened dissolvable lime cube (citric acid plus carbonate), dosed into 330 ml",
            "read_date": READ_DATE,
            "double_blind_note": "Public information only. No team or group data is used. Repo notes were treated as leads.",
            "cost_rule": ("Public price: Makro PRO listed prices read 2026-10-18 (shown without login). Derived "
                          "ingredient cost is labelled as derived. Potassium bicarbonate and calcium carbonate: none."),
            "limits_rule": "Items that could not be verified are closed as stated limits in 'limits'.",
            "claim_basis": ("Thai nutrition claims: Notification 445 (2023) Tables 1 and 2, read in English translation. "
                            "Notification 467 (2025) changes display format only."),
            "constants": {
                "R_GAS_J_per_mol_K": R_GAS,
                "P_std_Pa": P_STD_PA,
                "T_std_K": T_STD_K,
                "Vm_ideal_STP_L_per_mol": round(VM_IDEAL_L, 4),
                "Vm_real_density_basis_L_per_mol": round(VM_REAL_L, 4),
                "M_CO2_g_per_mol": M_CO2,
                "M_NaHCO3": M_NAHCO3, "M_KHCO3": M_KHCO3, "M_CaCO3": M_CACO3, "M_Na2CO3_derived": round(M_NA2CO3, 3),
                "M_citric_anhydrous": M_CITRIC, "M_Ca_citrate_anhydrous": M_CA_CITRATE,
                "element_Na_derived": round(M_NA, 3), "element_K_derived": round(M_K, 3), "element_Ca_derived": round(M_CA, 3),
                "P_air_atm_432ppm": P_AIR_ATM,
                "Thai_RDI_mg": RDI,
            },
            "fizz_definition": ("Usable fizz floor = 1.5 volumes retained as dissolved CO2 at serving (lowest target in the team "
                                "brief). This is an assumption for the screen."),
        },
        "sources": SOURCES,
        "assumptions": [
            {"id": "A1", "text": "Sodium, potassium and calcium load is set by CO2 generated, not retained; f_ret = retained/generated", "status": "assumed"},
            {"id": "A2", "text": "f_ret cases 1.0 (upper bound), 0.5 and 0.25. No source; to be measured", "status": "assumed"},
            {"id": "A3", "text": "Citric acid molar excess 0 in base case; sensitivity 10 and 20 percent", "status": "assumed"},
            {"id": "A4", "text": "Stoichiometric reactions: 3 CO2 per citric acid with 3 bicarbonate; 3 CO2 per 2 citric acid with 3 carbonate", "status": "derived"},
            {"id": "A5", "text": "1 volume = 1 L CO2 at 0 C and 1 atm per litre of liquid; ideal molar volume 22.414 L/mol (real-gas density basis 22.26 also shown)", "status": "derived"},
            {"id": "A6", "text": "Serving 330 ml; drink volume equals serving volume; cube volume ignored", "status": "assumed"},
            {"id": "A7", "text": "Thai reference serving for carbonated beverages 200 ml (P445 Annex 2)", "status": "sourced"},
            {"id": "A8", "text": "Henry's law linear to the required pressure; required pressure = V / Bunsen(T)", "status": "assumed"},
            {"id": "A9", "text": "Open-glass headspace CO2 is 432 ppm (0.000432 atm); equilibrium dissolved CO2 = Bunsen(T) x 0.000432", "status": "derived"},
            {"id": "A10", "text": "Base drink sodium is zero for the carbonate-only sodium count; actual base drink not read", "status": "assumed"},
            {"id": "A11", "text": "Cube contains no sugar and no sodium other than the carbonate; sweetener and flavour are outside this screen", "status": "assumed"},
            {"id": "A12", "text": "Calcium citrate solubility 0.95 g/L at 25 C applied at serving temperature (4 C value not sourced)", "status": "assumed"},
            {"id": "A13", "text": "Atomic masses: H 1.008, C 12.011, O 15.999; element masses derived from sourced compound masses", "status": "derived"},
        ],
        "stoichiometry_per_mol_CO2": stoich,
        "saturation_1atm_check": saturation,
        "dose_table": dose_rows,
        "citric_excess_sensitivity_at_1.5vol_f1": excess,
        "volume_definition_sensitivity": vol_def,
        "calcium_citrate_precipitation_check_CaCO3_route": ca_check,
        "ranking_at_usable_fizz_floor": ranking,
        "public_price_cost_derived": {"prices": PUBLIC_PRICES, "price_per_g_baht": {k: round(v, 5) for k, v in price_per_g.items()},
                                      "rows": cost_rows},
        "verdict": verdict,
        "open_items": open_items,
        "limits": limits,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)

    # human-readable summary
    print("Effervescent cube screen (Thailand domestic)")
    print("Bunsen 4 C %.3f, 25 C %.3f volumes at 1 atm pure CO2; open-glass equilibrium at 4 C %.5f volumes" % (
        bunsen(4), bunsen(25), bunsen(4) * P_AIR_ATM))
    print("Stoichiometry per mol CO2 (carbonate g, citric g, cation g):")
    for ch in CHOICES:
        s = stoich[ch["id"]]
        print("  %-22s carbonate %.3f g  citric %.3f g  cation %s" % (
            ch["id"], s["carbonate_g_per_mol_CO2"], s["citric_acid_g_per_mol_CO2"], s["cation_g_per_mol_CO2"]))
    print("Per 330 ml, full retention (f=1.0):")
    for v in TARGET_VOLS:
        for ch in CHOICES:
            r = find_row(dose_rows, ch["id"], v, 1.0)
            s330 = r["serving_330ml"]
            print("  %.1f vol %-22s carbonate %6.3f g  citric %6.3f g  cation mg %s" % (
                v, ch["id"], s330["carbonate_g"], s330["citric_acid_g_stoich"], s330["cation_mg"]))
    print("Sodium mg per 330 ml at 1.5 vol by retention f (NaHCO3): f1.0 %.0f, f0.5 %.0f, f0.25 %.0f" % (
        n15["serving_330ml"]["cation_mg"]["Na"], na15_f05["serving_330ml"]["cation_mg"]["Na"],
        na15_f025["serving_330ml"]["cation_mg"]["Na"]))
    print("Calcium citrate: max CO2 before 25 C saturation %.3f volumes" % ca_check["max_CO2_volumes_before_25C_saturation"])
    print("Lowest sodium passing solubility, by f: %s" % {k: (v["lowest_sodium_passing_solubility"], v["lowest_sodium_value_mg"])
                                                       for k, v in ranking.items()})
    print("Wrote %s" % OUT_PATH)


if __name__ == "__main__":
    main()
