"""T10 screening arithmetic: potassium in the Lemon Soda cube against kidney, medicine and diet guidance.

Writes t10_potassium_cover_results.json next to this file. No random numbers are used (deterministic bounds), so
no seed is needed; every number in the T10 record comes from the JSON this script writes.

Part 1: serve arithmetic (mg, mmol, mEq, shares of references, comparison foods, comparison products, claim thresholds
        including the per-100-kilocalorie basis of Notification 445 Annex 4 Table 2).
Part 2: share of people covered by a potassium caution, by age band, for men 25 to 34, men 25 to 59 and adults 25
        and over. Union bounds: lowest = largest single group (full overlap), highest = sum of groups (no overlap),
        mid = independence. Overlaps are not double counted: the union is never the plain sum except as the upper bound.
        The kidney input is built from two Thai national surveys that differ in equation and year (NHES V 2014 with
        CKD-EPI, NHES III 2004 with MDRD). The headline range ("span") takes NHES V for the low and mid values and the
        higher of NHES V and NHES III for the high value, for every band. Two comparator runs are written as well:
        NHES V only, and NHES III only. A sensitivity run varies the 60 and over kidney mid value.

        The coverage range is a set of model bounds, not a statistical interval. A driver block ("coverage_range_drivers")
        moves one input at a time from its low to its high value with the others at their mid values, and shows the effect
        of the overlap rule alone, so the sources of the width can be named.
Part 3: comparison foods use USDA FoodData Central values read through the official API and the site data endpoint (P); densities come from USDA's
        own portion weights.

Fourth pass (verifier findings): population weights corrected for age 60 counted twice (block
population_weights_correction_age_60); the young-adult treated share is a PROXY estimate, not a floor; the claim test adds the
solid per 100 g basis of Annex 4 Table 2; the judge-facing texts take their coverage numbers from the results computed above.

Run: python -I -X utf8 t10_potassium_cover.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "t10_potassium_cover_results.json")
K_ATOMIC = 39.098  # g/mol, potassium

# ---------------------------------------------------------------- inputs: the serve
with open(os.path.join(HERE, "handover_figures_results.json"), encoding="utf-8") as f:
    handover = json.load(f)
K_MG = handover["per_330ml_recipe"]["potassium_mg"]          # 316.6 mg, desk model (DERIVED)
KHCO3_G = handover["per_330ml_recipe"]["potassium_bicarbonate_g"]
CITRIC_G = handover["per_330ml_recipe"]["citric_acid_total_for_pH_target_g"]   # 2.10 g
BINDER_G = handover["per_330ml_recipe"]["binder_filler_g"]                      # 0.80 g
FLAVOUR_G = handover["per_330ml_recipe"]["flavour_g"]                           # 0.05 g
SUCRALOSE_G = handover["per_330ml_recipe"]["sucralose_mg"] / 1000.0             # 0.033 g
CUBE_G = handover["per_330ml_recipe"]["cube_mass_g"]                            # 3.794 g
VOLUME_ML = 330.0

serve = {
    "base_value_note": "316.6 mg is the handover value (handover_figures_results.json) and is the base of every share below; the script's own recomputation from 0.811 g potassium bicarbonate (a few lines down) is 316.7 mg. The two round to 317 mg and give the same shares to one decimal.",
    "potassium_mg": K_MG,
    "potassium_bicarbonate_g": KHCO3_G,
    "recomputed_k_mg_from_khco3_g": round(KHCO3_G * K_ATOMIC / 100.115 * 1000, 1),
    "mmol_or_mEq": round(K_MG / K_ATOMIC, 2),
    "mg_per_ml": round(K_MG / VOLUME_ML, 3),
    "mmol_per_litre": round(K_MG / K_ATOMIC / (VOLUME_ML / 1000.0), 1),
    "thai_label_rounded_mg_step10": int(round(K_MG / 10.0) * 10),
}

refs = {
    "thai_rdi_3500_notification_445": 3500.0,
    "eu_nrv_2000_reg_1169_2011": 2000.0,
    "efsa_ai_adult_3500": 3500.0,
    "us_ai_men_3400": 3400.0,
    "us_ai_women_2600": 2600.0,
}
serve["pct_of_reference"] = {k: round(100 * K_MG / v, 1) for k, v in refs.items()}
serve["pct_of_thai_rdi_unrounded"] = round(100 * K_MG / 3500.0, 3)
serve["pct_of_thai_rdi_from_printed_317"] = round(100 * 317.0 / 3500.0, 3)   # the 9.1% in the submission files comes from the rounded 317 mg

ckd_ceilings = {
    "thai_nephrology_ckd_diet_1500": 1500.0,
    "thai_nephrology_ckd_diet_2000": 2000.0,
    "thai_nephrology_haemodialysis_2000": 2000.0,
    "thai_nephrology_haemodialysis_2500": 2500.0,
    # UK Kidney Association 2023 (P), p. 37: the historical low-potassium diet is 2 to 3 g a day, and for CKD with persistent
    # serum potassium of 5.5 mmol/L or more a restriction below 3 g a day (or 1 mmol per kg ideal body weight) is recommended
    "ukka_historical_low_k_diet_2000": 2000.0,
    "ukka_historical_low_k_diet_and_persistent_hyperkalaemia_3000": 3000.0,
}
serve["pct_of_daily_ceiling"] = {k: round(100 * K_MG / v, 1) for k, v in ckd_ceilings.items()}
serve["ceiling_scope_note"] = ("The Thai 1,500 to 2,000 mg a day (recommendation 4.4.3, p. 27) is a low-potassium diet for CKD before dialysis; "
                               "its explanation (p. 28) ties the limit to a high blood potassium and warns against over-restriction. "
                               "KDIGO 2024 and KDOQI 2020 set no daily figure. The Thai guideline has no stage-specific ceiling. "
                               "The shares apply to patients on such a limit; they are not per-serve limits and do not describe the general population.")

# ---------------------------------------------------------------- comparison foods and products
# USDA FoodData Central, official API (https://api.nal.usda.gov/fdc/v1/food/<id>?api_key=DEMO_KEY&nutrients=306), read 20 Oct 2026 (P).
# SR Legacy values are per 100 g. Saved in raw/diligence_2026-10-20/T10/usda_fdc_api_potassium_2026-10-20.md.
foods = {
    "coconut_water_mg_per_100g": 250.0,       # FDC 170174, SR Legacy "Nuts, coconut water (liquid from coconuts)"
    "orange_juice_mg_per_100g": 200.0,        # FDC 169098, SR Legacy "Orange juice, raw"
    "banana_mg_per_100g_sr_legacy": 358.0,    # FDC 173944, SR Legacy "Bananas, raw"
    "banana_mg_per_100g_foundation": 326.0,   # FDC 1105314, Foundation "Bananas, ripe and slightly ripe, raw"
    "lemon_lime_soda_mg_per_100g": 1.00,      # FDC 173206, SR Legacy "Beverages, carbonated, SPRITE, lemon-lime, without caffeine"
    "gatorade_packet_mg": 70.0,               # maker label, one packet makes 15 to 20 oz (P, maker)
    "who_ors_mmol_per_litre": 20.0,           # WHO reduced osmolarity ORS (S via Wikipedia)
    # Thai DMSc statement via news report (S, undated): one range given for the minerals together; the sentence does not say
    # whether it is a sum of potassium and chloride or the range for each mineral
    "thai_dmsc_coconut_k_and_cl_low_mg_per_100g": 133.81,
    "thai_dmsc_coconut_k_and_cl_high_mg_per_100g": 215.20,
    "fda_potassium_dv_mg": 4700.0,            # 21 CFR 101.9(c)(8)(iv) RDI table, Cornell LII copy of the CFR text (S copy)
}
# Densities from USDA's own portion weights (FDC foodPortions): coconut water 1 cup = 240 g; orange juice 1 cup = 248 g;
# Sprite 12 fl oz = 369 g. US customary cup 236.588 mL and fluid ounce 29.5735 mL are the volume units (the nutrition-labelling
# cup of 240 mL would give a density lower by 1.4 percent; the effect is under 2 percent on every ratio and is not carried).
ML_CUP = 236.588
ML_FLOZ = 29.5735
DENSITY = {
    "coconut_water": 240.0 / ML_CUP,
    "orange_juice": 248.0 / ML_CUP,
    "lemon_lime_soda": 369.0 / (12 * ML_FLOZ),
}
comp = {"density_g_per_ml_from_usda_portions": {k: round(v, 4) for k, v in DENSITY.items()}}
comp["coconut_water_330ml_mg"] = round(foods["coconut_water_mg_per_100g"] / 100 * VOLUME_ML * DENSITY["coconut_water"], 0)
comp["coconut_water_ml_with_same_potassium"] = round(K_MG / (foods["coconut_water_mg_per_100g"] / 100 * DENSITY["coconut_water"]), 0)
comp["coconut_water_mmol_per_litre"] = round(foods["coconut_water_mg_per_100g"] / 100 * DENSITY["coconut_water"] * 1000 / K_ATOMIC, 1)
comp["orange_juice_330ml_mg"] = round(foods["orange_juice_mg_per_100g"] / 100 * VOLUME_ML * DENSITY["orange_juice"], 0)
comp["orange_juice_ml_with_same_potassium"] = round(K_MG / (foods["orange_juice_mg_per_100g"] / 100 * DENSITY["orange_juice"]), 0)
comp["orange_juice_mg_per_us_cup_248g"] = round(foods["orange_juice_mg_per_100g"] / 100 * 248.0, 0)
comp["banana_g_with_same_potassium_sr_legacy_358"] = round(K_MG / (foods["banana_mg_per_100g_sr_legacy"] / 100), 0)
comp["banana_g_with_same_potassium_foundation_326"] = round(K_MG / (foods["banana_mg_per_100g_foundation"] / 100), 0)
comp["gatorade_packets_with_same_potassium"] = round(K_MG / foods["gatorade_packet_mg"], 1)
comp["who_ors_mg_per_330ml"] = round(foods["who_ors_mmol_per_litre"] * K_ATOMIC * VOLUME_ML / 1000, 0)
comp["cube_drink_to_who_ors_ratio"] = round(serve["mmol_per_litre"] / foods["who_ors_mmol_per_litre"], 2)
OJ_330_MG = foods["orange_juice_mg_per_100g"] / 100 * VOLUME_ML * DENSITY["orange_juice"]
COCO_330_MG = foods["coconut_water_mg_per_100g"] / 100 * VOLUME_ML * DENSITY["coconut_water"]
comp["cube_drink_to_orange_juice_ratio"] = round(K_MG / OJ_330_MG, 2)
comp["cube_drink_to_coconut_water_ratio"] = round(K_MG / COCO_330_MG, 2)
comp["coconut_water_over_cube_ratio"] = round(COCO_330_MG / K_MG, 2)
# lemon-lime soda (USDA SR Legacy, P)
SODA_330_MG = foods["lemon_lime_soda_mg_per_100g"] / 100 * VOLUME_ML * DENSITY["lemon_lime_soda"]   # unrounded, so the ratio is not rounded twice
comp["lemon_lime_soda_330ml_mg"] = round(SODA_330_MG, 2)
comp["cube_drink_to_lemon_lime_soda_ratio"] = round(K_MG / SODA_330_MG, 0)
# the same three values at the earlier assumed density of 1.0 g/mL, for traceability
comp["at_density_1_0"] = {
    "coconut_water_330ml_mg": round(foods["coconut_water_mg_per_100g"] / 100 * VOLUME_ML, 0),
    "orange_juice_330ml_mg": round(foods["orange_juice_mg_per_100g"] / 100 * VOLUME_ML, 0),
    "lemon_lime_soda_330ml_mg": round(foods["lemon_lime_soda_mg_per_100g"] / 100 * VOLUME_ML, 1),
    "cube_to_lemon_lime_soda_ratio": round(K_MG / (foods["lemon_lime_soda_mg_per_100g"] / 100 * VOLUME_ML), 0),
}
# Thai DMSc statement: one range for potassium and chloride; taken here at the coconut-water density from USDA
comp["thai_dmsc_coconut_range_330ml_low_mg"] = round(foods["thai_dmsc_coconut_k_and_cl_low_mg_per_100g"] / 100 * VOLUME_ML * DENSITY["coconut_water"], 0)
comp["thai_dmsc_coconut_range_330ml_high_mg"] = round(foods["thai_dmsc_coconut_k_and_cl_high_mg_per_100g"] / 100 * VOLUME_ML * DENSITY["coconut_water"], 0)
comp["usda_coconut_potassium_over_dmsc_range_low"] = round(foods["coconut_water_mg_per_100g"] / foods["thai_dmsc_coconut_k_and_cl_low_mg_per_100g"], 2)
comp["dmsc_note"] = ("If the Thai range is per mineral, potassium would be 134 to 215 mg per 100 g, below the USDA 250 mg per 100 g; if it is a sum with chloride, "
                     "no potassium value follows. Either way the USDA value (P) is the one used.")

products = {
    "klor_con_ef_25mEq_mg": 978.0,
    "effer_k_10mEq_mg": 391.0,
    "effer_k_20mEq_mg": 782.0,
    "sando_k_per_tablet_mg_derived": round(12 * K_ATOMIC, 0),   # 12 mmol implied by SmPC 2 to 4 tablets = 24 to 48 mmol
}
prod_cmp = {"cube_over_" + k: round(K_MG / v, 2) for k, v in products.items()}
fda = {
    # P: eCFR current text (versioner API, issue 2026-10-01 requested) and the official GPO print of the CFR 2014 edition (p. 81),
    # both read 20 Oct 2026; both give the 100 mg and 20 mg/mL lines. The section's own amendment note ends 67 FR 4906 (1 Feb 2002).
    "cfr_201_306_unit_line_mg": 100.0,               # paragraphs (a) and (b): tablets of 100 mg or more potassium per tablet
    "cfr_201_306_liquid_line_mg_per_ml": 20.0,       # paragraph (b): liquids of 20 mg or more potassium per mL
    "cube_vs_unit_line_ratio": round(K_MG / 100.0, 2),   # the sourced ratio (P line, DERIVED ratio)
    "drink_mg_per_ml_vs_liquid_line_ratio": round(serve["mg_per_ml"] / 20.0, 3),
    # S: Council for Responsible Nutrition (trade body) page, undated: "The upper limit of 99 mg per dose for potassium is specific to
    # OTC drugs"; OTC products need a warning above 100 mg per serving; FDA has not ruled on potassium in dietary supplements;
    # manufacturers have followed the limit in practice. 99 mg is a labelling convention just under the 100 mg line, not a text in 21 CFR 201.306.
    "otc_drug_convention_99mg_per_dose_crn_secondary": 99.0,
    "cube_vs_99mg_convention_ratio": round(K_MG / 99.0, 2),
    "mg_99_in_mEq": round(99.0 / K_ATOMIC, 2),
}

# FDA potassium daily value and nutrient-content claim lines (S copy of the CFR text; currency not shown on the copy)
us_dv = {
    "fda_potassium_dv_mg": foods["fda_potassium_dv_mg"],                       # 21 CFR 101.9(c)(8)(iv)
    "cube_pct_of_fda_dv": round(100 * K_MG / foods["fda_potassium_dv_mg"], 1), # DERIVED
    "good_source_line_mg": round(0.10 * foods["fda_potassium_dv_mg"], 0),      # 21 CFR 101.54(c)(1): 10 to 19 percent of DRV
    "high_line_mg": round(0.20 * foods["fda_potassium_dv_mg"], 0),             # 21 CFR 101.54(b)(1): 20 percent or more
    "good_source_met_per_330ml_serve": bool(K_MG >= 0.10 * foods["fda_potassium_dv_mg"]),
    "potassium_mandatory_in_us_vitamin_mineral_declaration": True,              # 21 CFR 101.9(c)(8)(ii), S copy
    "reference_amount_note": "The US reference amount customarily consumed was not read; the per 330 mL test is shown for orientation only.",
}

# ---------------------------------------------------------------- claim thresholds, including the per-100-kcal basis
# Energy per serve is not in the repo (the binder and filler is not yet named). The bound below uses the conversion
# factors in Notification 445 Annex 1 section 2.4 (read in the saved text): organic acid 3 kcal/g, fat 9 kcal/g (the
# highest factor in the table), protein and carbohydrate 4 kcal/g. Potassium bicarbonate is an inorganic salt with no
# factor in the table, so it is taken as 0 kcal.
KCAL_FAT = 9.0
KCAL_ORGANIC_ACID = 3.0
energy_upper_loose = CUBE_G * KCAL_FAT                                                    # whole cube at 9 kcal/g
energy_upper_tight = CITRIC_G * KCAL_ORGANIC_ACID + (BINDER_G + FLAVOUR_G + SUCRALOSE_G) * KCAL_FAT
PCT5_PER_100KCAL_MG = 0.05 * 3500.0
PCT10_PER_100KCAL_MG = 0.10 * 3500.0
claims = {
    "thai_table1_good_source_15pct_mg": 0.15 * 3500,
    "thai_table1_high_30pct_mg": 0.30 * 3500,
    "thai_table2_good_source_per_100ml_mg": 0.075 * 3500,
    "thai_table2_high_per_100ml_mg": 0.15 * 3500,
    "cube_mg_per_100ml": round(K_MG / VOLUME_ML * 100, 1),
    "pct_rdi_330ml": round(100 * K_MG / 3500, 1),
    "pct_rdi_200ml_reference_serving": round(100 * (K_MG * 200 / VOLUME_ML) / 3500, 1),
    "pct_rdi_per_100ml": round(100 * (K_MG / VOLUME_ML * 100) / 3500, 1),
    "per_serving_basis_met": (K_MG / 3500.0) > 0.15,
    "per_100ml_basis_met": (K_MG / VOLUME_ML * 100 / 3500.0) >= 0.075,
    "table2_per_100kcal_good_source_line_mg_per_100kcal": PCT5_PER_100KCAL_MG,
    "table2_per_100kcal_high_line_mg_per_100kcal": PCT10_PER_100KCAL_MG,
    "energy_per_serve_in_repo": "none; binder and filler not yet named (UNVERIFIED)",
    "energy_at_which_5pct_per_100kcal_is_just_met_kcal": round(K_MG / PCT5_PER_100KCAL_MG * 100, 1),
    "energy_at_which_10pct_per_100kcal_is_just_met_kcal": round(K_MG / PCT10_PER_100KCAL_MG * 100, 1),
    "energy_upper_bound_loose_kcal_cube_at_9_kcal_per_g": round(energy_upper_loose, 1),
    "energy_upper_bound_tight_kcal_citric_3_other_9": round(energy_upper_tight, 2),
    "mg_per_100kcal_at_loose_bound_or_more": round(K_MG / energy_upper_loose * 100, 0),
    "mg_per_100kcal_at_tight_bound_or_more": round(K_MG / energy_upper_tight * 100, 0),
    "pct_rdi_per_100kcal_at_loose_bound_or_more": round(100 * (K_MG / energy_upper_loose * 100) / 3500.0, 1),
    "pct_rdi_per_100kcal_at_tight_bound_or_more": round(100 * (K_MG / energy_upper_tight * 100) / 3500.0, 1),
    "per_100kcal_basis_met_at_both_bounds": (K_MG / energy_upper_loose * 100) >= PCT10_PER_100KCAL_MG,
    "eu_beverage_source_line_mg_per_100ml": 0.075 * 2000,
    "eu_single_portion_source_line_mg": 0.15 * 2000,
    "cube_above_eu_single_portion_line": K_MG > 0.15 * 2000,
    "cube_above_eu_beverage_line": (K_MG / VOLUME_ML * 100) > 0.075 * 2000,
    # Annex 4 Table 2, solid food column, vitamins and minerals excluding sodium (PDF page 65, read again in the fourth pass):
    # good source at least 15 percent of the Thai RDI per 100 g (or at least 5 percent per 100 kcal); high at least 30 percent
    # per 100 g (or at least 10 percent per 100 kcal). The cube as sold is a solid of 3.794 g carrying the serve's potassium.
    "solid_cube_mass_g": CUBE_G,
    "solid_mg_per_100g_as_sold": round(K_MG / CUBE_G * 100, 0),
    "solid_pct_rdi_per_100g_as_sold": round(100 * (K_MG / CUBE_G * 100) / 3500.0, 0),
    "table2_solid_good_source_line_mg_per_100g": 0.15 * 3500,
    "table2_solid_high_line_mg_per_100g": 0.30 * 3500,
    "solid_per_100g_good_source_met_as_sold": (K_MG / CUBE_G * 100) >= 0.15 * 3500,
    "solid_per_100g_high_met_as_sold": (K_MG / CUBE_G * 100) >= 0.30 * 3500,
    "solid_per_100g_multiple_of_high_line": round((K_MG / CUBE_G * 100) / (0.30 * 3500), 1),
    "solid_basis_note": ("As sold, the cube would exceed both solid per 100 g lines of Notification 445 Annex 4 Table 2 (525 and 1,050 mg per 100 g). "
                         "Conditions 1.1 and 2.2 of Annex 4 were not tested, and which basis applies to a dissolvable cube (per serving, per 100 mL as prepared, "
                         "or per 100 g as sold) is not settled by the text. The per 100 g basis therefore does not close a claim either: "
                         "the no-claim setting is the team's choice."),
}

# ---------------------------------------------------------------- design lever and repeat serves
CO2_VOL = handover["design"]["co2_volumes_per_330ml"]     # 0.55
levers = {
    "co2_volumes_design": CO2_VOL,
    "co2_mmol_design": handover["per_330ml_recipe"]["co2_mmol"],
    "k_mmol_equals_co2_mmol_check": abs(handover["per_330ml_recipe"]["co2_mmol"] - serve["mmol_or_mEq"]) < 0.05,
    "mg_potassium_per_0_1_volume": round(K_MG / (CO2_VOL / 0.1), 1),
    "mg_potassium_at_0_40_volume": round(K_MG * 0.40 / CO2_VOL, 1),
    "mg_potassium_at_0_30_volume": round(K_MG * 0.30 / CO2_VOL, 1),
    "two_cubes_mg": round(2 * K_MG, 1),
    "three_cubes_mg": round(3 * K_MG, 1),
    "three_cubes_pct_thai_rdi": round(100 * 3 * K_MG / 3500.0, 1),
    "three_cubes_pct_of_1500_ceiling": round(100 * 3 * K_MG / 1500.0, 1),
    "three_cubes_coconut_water_ml_with_same_potassium": round(3 * K_MG / (foods["coconut_water_mg_per_100g"] / 100 * DENSITY["coconut_water"]), 0),
}

# ---------------------------------------------------------------- inputs: coverage model
# Population weights, persons, central value, DOPA Nov B.E. 2568 as held in screen/segment_potency_mc.py
# (not re-opened in T10). Both sexes; used as weights for men as well (assumption: similar age structure).
# The DOPA five-year bands start at 26, so the repo's "25-34" band is ages 26 to 35, "35-44" is 36 to 45, "45-59" is
# 46 to 60 in full (46-50, 51-55 and 56-60) and "60+" is 61 and over plus one fifth of the 56 to 60 band (see
# segment_potency_mc.py). One fifth of the 56 to 60 band (age 60) is therefore in both "45-59" and "60+": about one year of
# age is counted twice (verifier finding, fourth pass). The 56 to 60 band count itself is not in the repo.
# Correction used in this script: remove the duplicated age from the "45-59" band, so that "45-59" is ages 46 to 59 and
# "60+" is age 60 and over. The 56 to 60 band is estimated as one third of the held 46 to 60 total (ASSUMPTION: the three
# five-year bands are equal; the real 56 to 60 band is probably a little larger, see the sensitivity block).
POP_AS_HELD = {"25-34": 9384203, "35-44": 9407482, "45-59": 14904550, "60+": 14100138}
DUP_AGE60_ESTIMATE = POP_AS_HELD["45-59"] / 3.0 / 5.0          # one fifth of one third of the held 45-59 total, persons
POP = dict(POP_AS_HELD)
POP["45-59"] = int(round(POP_AS_HELD["45-59"] - DUP_AGE60_ESTIMATE))
BANDS = ["25-34", "35-44", "45-59", "60+"]

# NHES V (2014) eGFR < 60, percent, Table 2 of Aekplakorn 2021: men / both sexes (CKD-EPI)
CKD_MEN = {"20-39": 0.08, "40-49": 0.67, "50-59": 3.4, "60-69": 8.8, "70+": 25.1}
CKD_ALL = {"20-39": 0.20, "40-49": 0.81, "50-59": 2.6, "60-69": 12.2, "70+": 32.7}
# NHES III (2004) CKD stage 3 to 5, percent, Table 2 of Ong-ajyooth 2009, both sexes only (MDRD x 1.233 Asian factor).
# The paper gives no age table by sex (men 5.5 and women 12.3 percent age-standardised, all ages).
# Mapping to the repo's bands, the NHES III row that holds most of the band's ages (ASSUMPTION; a ceiling for the
# youngest band, whose ages 26 to 29 sit in the 15 to 29 row at 0.4 percent and 30 to 35 in the 30 to 44 row at 2.3).
CKD_NHES3 = {"25-34": 2.3, "35-44": 2.3, "45-59": 13.1, "60+": 39.8}
NHES3_ALL_AGES_MEN = 5.5
NHES3_ALL_AGES_ALL = 8.9
SEEK_STAGE3_PLUS4 = 8.6   # Thai SEEK 2010 (abstract): stage III 7.5 plus stage IV 1.1; sample mean age 45.2; not age-specific


def ckd_band(tab, band, mode="span", mid60="mid"):
    """Return (low, mid, high) percent of CKD stage 3 to 5 for a band.

    mode "nhes5": NHES V only (high = the next older row of the NHES V table).
    mode "span": NHES V for low and mid; high = the higher of the NHES V high and the NHES III row for the band.
    mode "nhes3": NHES III row for low, mid and high (both sexes, older equation).
    mid60 sets the 60 and over mid value: "mid" (plain midpoint of the 60-69 and 70+ rows, ASSUMPTION), "low" (60-69
    row) or "high" (70+ row)."""
    if band == "25-34":
        lo, mid, hi = tab["20-39"], tab["20-39"], tab["20-39"]
    elif band == "35-44":
        lo, hi = tab["20-39"], tab["40-49"]
        lo, mid, hi = lo, 0.5 * lo + 0.5 * hi, hi          # interpolated between the 20-39 and 40-49 rows (ASSUMPTION)
    elif band == "45-59":
        mid = (tab["40-49"] * 5 + tab["50-59"] * 10) / 15.0   # five-year ages, equal weight per year
        lo, mid, hi = tab["40-49"], mid, tab["50-59"]
    else:
        lo, hi = tab["60-69"], tab["70+"]
        mid = {"mid": 0.5 * (lo + hi), "low": lo, "high": hi}[mid60]   # plain midpoint (ASSUMPTION)
    if mode == "nhes5":
        return (lo, mid, hi)
    if mode == "span":
        return (lo, mid, max(hi, CKD_NHES3[band]))
    if mode == "nhes3":
        v = CKD_NHES3[band]
        return (v, v, v)
    raise ValueError(mode)


# NHES VI (2019-2020), both sexes. Hypertension crude by age; diabetes age-standardised by age.
HT = {"20-39": 7.7, "40-59": 25.6, "60+": 60.6}
HT_STD = {"all": 25.7, "men": 26.8}
DM = {"20-39": (2.1, 3.2, 4.4), "40-59": (9.1, 10.4, 11.6), "60+": (19.0, 20.3, 21.8)}
DM_STD = {"all": 10.1, "men": 9.3}
TREATED_SHARE = 0.479            # NHES VI: treated share of people with hypertension (all ages)
# Young adults are less often treated than the all-age 47.9 percent; the age table was not read. A PROXY estimate of the
# young-adult treated share is taken from the NHSO hospital sample (Luangmonkong 2022, 2015 table 1): 176 of 31,808 treated
# patients were 25-34 and 1,399 were 35-44. Scaling that age distribution to the model's national treated count gives an
# implied treated share. It is a proxy estimate (a public-hospital sample, patients on treatment, mean age about 65), not a
# floor or lower bound for the national share; nothing in the source makes it one. The young-adult treated share is an
# ASSUMPTION: this proxy is used as the low value, the midpoint of it and 47.9 percent as the mid value, and 47.9 percent as the
# high value.
NHSO_2015_N = {"25-34": 176, "35-44": 1399}
NHSO_2015_TOTAL = 31808
ACEI_ARB_LOW = 0.347             # NHSO under-55 monotherapy ACEI 28.40 + ARB 6.33 (2015); rural 2024 gives 35.6 (single therapy 20-44)
ACEI_ARB_HIGH = 0.4101 + 0.1735 - 0.0018   # NHSO 2015 all treated: ACEI 41.01, ARB 17.35; 0.18 = ACEI+ARB rate among patients without co-morbidity, used only as a small overlap proxy
ACEI_ARB_MID = 0.5 * (ACEI_ARB_LOW + ACEI_ARB_HIGH)
HT_MEN_FACTOR = (1.0, HT_STD["men"] / HT_STD["all"], 1.5)   # high 1.5 is an ASSUMPTION for young men
DM_MEN_FACTOR = DM_STD["men"] / DM_STD["all"]


def ht_band(band):
    if band == "25-34":
        return HT["20-39"]
    if band == "35-44":
        return 0.5 * HT["20-39"] + 0.5 * HT["40-59"]
    if band == "45-59":
        return HT["40-59"]
    return HT["60+"]


def dm_band(band):
    if band == "25-34":
        return DM["20-39"]
    if band == "35-44":
        return tuple(0.5 * a + 0.5 * b for a, b in zip(DM["20-39"], DM["40-59"]))
    if band == "45-59":
        return DM["40-59"]
    return DM["60+"]


def treated_young_low():
    nat_treated = sum(ht_band(b) / 100.0 * POP[b] for b in BANDS) * TREATED_SHARE
    out = {}
    for b, n in NHSO_2015_N.items():
        implied = n / NHSO_2015_TOTAL * nat_treated
        out[b] = implied / (ht_band(b) / 100.0 * POP[b])
    return nat_treated, out


NAT_TREATED_25PLUS, TREATED_YOUNG_PROXY = treated_young_low()


def cap(x):
    return max(0.0, min(1.0, x))


def groups(band, sex, mode="span", mid60="mid"):
    """Return dict of group -> (low, mid, high) as fractions for a band and sex ('men' or 'all')."""
    ckd = ckd_band(CKD_MEN if sex == "men" else CKD_ALL, band, mode, mid60)
    ckd = tuple(v / 100.0 for v in ckd)
    ht = ht_band(band) / 100.0
    if sex == "men":
        fl, fm, fh = HT_MEN_FACTOR
        if band in ("45-59", "60+"):
            fh = fm   # the 1.5 assumption is for the young bands only
        ht_t = (cap(ht * fl), cap(ht * fm), cap(ht * fh))
    else:
        ht_t = (ht, ht, ht)
    if band in TREATED_YOUNG_PROXY:
        lo_t = TREATED_YOUNG_PROXY[band]
        tr = (lo_t, 0.5 * (lo_t + TREATED_SHARE), TREATED_SHARE)
    else:
        tr = (TREATED_SHARE, TREATED_SHARE, TREATED_SHARE)
    treated = tuple(a * b for a, b in zip(ht_t, tr))
    on_raas = (treated[0] * ACEI_ARB_LOW, treated[1] * ACEI_ARB_MID, treated[2] * ACEI_ARB_HIGH)
    dm = tuple(v / 100.0 for v in dm_band(band))
    if sex == "men":
        dm = tuple(v * DM_MEN_FACTOR for v in dm)
    return {"ckd35": ckd, "htn_any": ht_t, "htn_treated": treated, "htn_on_acei_arb": on_raas, "diabetes": dm}


def union(parts):
    """parts: list of (low, mid, high). Return (low, mid, high) of the union without double counting."""
    low = max(p[0] for p in parts)                 # full overlap: the largest single group
    high = cap(sum(p[2] for p in parts))           # no overlap: sum of the groups at their high values
    mid = 1.0
    for p in parts:
        mid *= (1.0 - p[1])
    mid = 1.0 - mid                                # independence at mid values
    return (low, mid, high)


def band_result(band, sex, mode="span", mid60="mid"):
    g = groups(band, sex, mode, mid60)
    narrow = union([g["ckd35"], g["htn_on_acei_arb"]])
    broad = union([g["ckd35"], g["htn_treated"], g["diabetes"]])
    return g, narrow, broad


def pct(t):
    return [round(100 * v, 2) for v in t]


def weighted(bands, sex, key, mode="span", mid60="mid"):
    w = [POP[b] for b in bands]
    tot = float(sum(w))
    out = [0.0, 0.0, 0.0]
    for b, wi in zip(bands, w):
        _, n, br = band_result(b, sex, mode, mid60)
        sel = n if key == "narrow" else br
        for i in range(3):
            out[i] += sel[i] * wi / tot
    return tuple(out)


AGGS = {
    "men_25_34": ("men", ["25-34"]),
    "men_25_59": ("men", ["25-34", "35-44", "45-59"]),
    "men_45_59": ("men", ["45-59"]),
    "adults_25_plus": ("all", BANDS),
    "adults_25_59": ("all", ["25-34", "35-44", "45-59"]),
}
TOT_ADULTS = float(sum(POP[b] for b in BANDS))


def aggregates(mode, mid60="mid"):
    res = {}
    for name, (sex, bands) in AGGS.items():
        nar = weighted(bands, sex, "narrow", mode, mid60)
        bro = weighted(bands, sex, "broad", mode, mid60)
        entry = {
            "narrow_pct_low_mid_high": pct(nar),
            "broad_pct_low_mid_high": pct(bro),
            "weights_persons": {b: POP[b] for b in bands},
        }
        if name == "adults_25_plus":
            pop = sum(POP[b] for b in bands)
            entry["population_persons"] = pop
            entry["narrow_persons_millions_low_mid_high"] = [round(v * pop / 1e6, 2) for v in nar]
            entry["broad_persons_millions_low_mid_high"] = [round(v * pop / 1e6, 2) for v in bro]
        res[name] = entry
    return res


coverage = {"by_band": {}, "aggregates": {}}
for sex in ("men", "all"):
    for b in BANDS:
        g, n, br = band_result(b, sex, "span")
        coverage["by_band"][f"{sex}_{b}"] = {
            "groups_pct_low_mid_high": {k: pct(v) for k, v in g.items()},
            "narrow_ckd35_or_acei_arb_pct_low_mid_high": pct(n),
            "broad_ckd35_or_treated_htn_or_diabetes_pct_low_mid_high": pct(br),
        }
coverage["aggregates"] = aggregates("span")

# comparator runs: kidney input from one survey only
scenarios = {
    "nhes5_only": aggregates("nhes5"),
    "nhes3_only": aggregates("nhes3"),
}

# sensitivity of the adult headline to the 60 and over kidney mid value, and the share of the headline that 60 and over supplies
sens60 = {}
for opt in ("low", "mid", "high"):
    agg = aggregates("span", opt)
    sens60[f"ckd_60plus_mid_at_{ {'low': '60_69_row', 'mid': 'plain_midpoint', 'high': '70plus_row'}[opt] }"] = {
        "adults_25_plus_narrow_pct_low_mid_high": agg["adults_25_plus"]["narrow_pct_low_mid_high"],
        "adults_25_plus_broad_pct_low_mid_high": agg["adults_25_plus"]["broad_pct_low_mid_high"],
        "adults_25_plus_narrow_millions_low_mid_high": agg["adults_25_plus"]["narrow_persons_millions_low_mid_high"],
        "men_25_59_narrow_pct_low_mid_high": agg["men_25_59"]["narrow_pct_low_mid_high"],
    }
share60 = {}
for i, label in enumerate(("low", "mid", "high")):
    contrib = {}
    for b in BANDS:
        _, n, _br = band_result(b, "all", "span")
        contrib[b] = n[i] * POP[b] / TOT_ADULTS
    tot = sum(contrib.values())
    share60[label] = {
        "weighted_points_by_band": {b: round(100 * v, 2) for b, v in contrib.items()},
        "total_points": round(100 * tot, 2),
        "share_of_total_from_60plus_pct": round(100 * contrib["60+"] / tot, 1),
    }

# cross-check: kidney stage 3 to 5 alone, adults 25 and over, by survey
def ckd_alone(mode):
    out = [0.0, 0.0, 0.0]
    for b in BANDS:
        v = ckd_band(CKD_ALL, b, mode)
        for i in range(3):
            out[i] += v[i] * POP[b] / TOT_ADULTS
    return [round(x, 2) for x in out]


ckd_crosscheck = {
    "adults_25_plus_ckd35_pct_low_mid_high_nhes5": ckd_alone("nhes5"),
    "adults_25_plus_ckd35_pct_nhes3": ckd_alone("nhes3")[1],
    "adults_25_plus_ckd35_pct_low_mid_high_span": ckd_alone("span"),
    "nhes3_age_standardised_all_ages_both_sexes_pct": NHES3_ALL_AGES_ALL,
    "nhes3_men_to_all_ratio_all_ages": round(NHES3_ALL_AGES_MEN / NHES3_ALL_AGES_ALL, 3),
    "seek_stage3_plus4_pct_sample_mean_age_45": SEEK_STAGE3_PLUS4,
    "nhes5_all_ages_egfr_below_60_pct_both_sexes": 5.3,
    "nhes5_all_ages_egfr_below_60_pct_men": 4.1,
    "nhes3_to_nhes5_ratio_by_band_both_sexes": {
        b: round(CKD_NHES3[b] / ckd_band(CKD_ALL, b, "nhes5")[1], 1) for b in BANDS
    },
}

# ---------------------------------------------------------------- what drives the width of the coverage range
# The headline low is every input at its low value with full overlap; the headline high is every input at its high value with
# no overlap. Both are corners of assumed bounds, not statistical limits. Each driver below is moved alone from low to high with
# the other inputs at mid values and the independence rule, so its own effect on the width can be read.
def union_rule(parts, rule):
    if rule == "low":
        return max(parts)
    if rule == "high":
        return cap(sum(parts))
    m = 1.0
    for x in parts:
        m *= (1.0 - x)
    return 1.0 - m


def narrow_custom(band, sex, lv, rule, ckd_mode="span"):
    """Narrow group (CKD stage 3 to 5, or treated hypertension on an ACE inhibitor or ARB) for one band.
    lv: indices 0 (low), 1 (mid), 2 (high) for 'ckd', 'fac' (men's hypertension factor), 'tr' (treated share), 'raas' (ACEI/ARB share)."""
    ckd = ckd_band(CKD_MEN if sex == "men" else CKD_ALL, band, ckd_mode)[lv["ckd"]] / 100.0
    ht = ht_band(band) / 100.0
    if sex == "men":
        fl, fm, fh = HT_MEN_FACTOR
        if band in ("45-59", "60+"):
            fh = fm
        ht = cap(ht * (fl, fm, fh)[lv["fac"]])
    if band in TREATED_YOUNG_PROXY:
        lo_t = TREATED_YOUNG_PROXY[band]
        tr = (lo_t, 0.5 * (lo_t + TREATED_SHARE), TREATED_SHARE)[lv["tr"]]
    else:
        tr = TREATED_SHARE
    raas = (ACEI_ARB_LOW, ACEI_ARB_MID, ACEI_ARB_HIGH)[lv["raas"]]
    return union_rule([ckd, ht * tr * raas], rule)


def agg_custom(bands, sex, lv, rule, ckd_mode="span"):
    tot = float(sum(POP[b] for b in bands))
    return round(100 * sum(narrow_custom(b, sex, lv, rule, ckd_mode) * POP[b] / tot for b in bands), 2)


MID = {"ckd": 1, "fac": 1, "tr": 1, "raas": 1}
DRIVER_LABELS = {
    "ckd": "kidney input (NHES V low and mid; high is the higher of NHES V and NHES III)",
    "tr": "share of hypertensive adults who are treated (young-adult PROXY estimate from a hospital sample as the low value, up to the all-age 47.9%)",
    "fac": "men's hypertension factor (1.0 low, age-standardised men to all ratio mid, 1.5 high for ages under 45; ASSUMPTION)",
    "raas": "ACE inhibitor or ARB share of treated patients (34.7% low, 58.2% high; hospital sample with mean age 65; PROXY)",
}
drivers = {}
for name, (sex, bands) in AGGS.items():
    if name not in ("men_25_34", "men_25_59", "adults_25_plus"):
        continue
    head = coverage["aggregates"][name]["narrow_pct_low_mid_high"]
    all_low = {k: 0 for k in MID}
    all_high = {k: 2 for k in MID}
    entry = {
        "headline_low_mid_high": head,
        "reproduces_headline": [agg_custom(bands, sex, all_low, "low"), agg_custom(bands, sex, MID, "mid"), agg_custom(bands, sex, all_high, "high")] == head,
        "overlap_rule_alone_mid_inputs_low_mid_high": [agg_custom(bands, sex, MID, r) for r in ("low", "mid", "high")],
        "all_inputs_low_or_high_with_independence_rule": [agg_custom(bands, sex, all_low, "mid"), agg_custom(bands, sex, MID, "mid"), agg_custom(bands, sex, all_high, "mid")],
        "one_input_alone_low_mid_high": {},
    }
    for d in ("ckd", "tr", "fac", "raas"):
        if sex == "all" and d == "fac":
            continue
        vals = []
        for lvl in (0, 1, 2):
            lv = dict(MID)
            lv[d] = lvl
            vals.append(agg_custom(bands, sex, lv, "mid"))
        entry["one_input_alone_low_mid_high"][d] = {"low_mid_high": vals, "width_points": round(vals[2] - vals[0], 2), "what": DRIVER_LABELS[d]}
    lv_n5 = dict(MID)
    lv_n5["ckd"] = 2
    entry["kidney_high_from_nhes5_only_alone"] = agg_custom(bands, sex, lv_n5, "mid", "nhes5")
    entry["kidney_high_from_nhes3_only_alone"] = agg_custom(bands, sex, lv_n5, "mid", "nhes3")
    entry["headline_width_points"] = round(head[2] - head[0], 2)
    drivers[name] = entry

# individual group prevalences stated plainly for the record
coverage["inputs_used"] = {
    "ckd_men_nhes5_pct": CKD_MEN,
    "ckd_all_nhes5_pct": CKD_ALL,
    "ckd_nhes3_row_used_per_band_pct_both_sexes": CKD_NHES3,
    "ckd_nhes3_rows_as_published_pct": {"15-29": 0.4, "30-44": 2.3, "45-59": 13.1, "60+": 39.8},
    "hypertension_crude_pct_by_age_nhes6": HT,
    "hypertension_age_std_pct": HT_STD,
    "diabetes_pct_by_age_nhes6_low_mid_high": DM,
    "diabetes_age_std_pct": DM_STD,
    "treated_share_nhes6": TREATED_SHARE,
    "treated_share_young_nhso_proxy_used_as_low_value": {b: round(v, 4) for b, v in TREATED_YOUNG_PROXY.items()},
    "national_treated_hypertensives_25plus_persons": round(NAT_TREATED_25PLUS),
    "nhso_2015_patients_by_band": NHSO_2015_N,
    "acei_arb_share_low_mid_high": [round(ACEI_ARB_LOW, 4), round(ACEI_ARB_MID, 4), round(ACEI_ARB_HIGH, 4)],
    "htn_men_factor_low_mid_high": [round(v, 4) for v in HT_MEN_FACTOR],
    "dm_men_factor": round(DM_MEN_FACTOR, 4),
    "population_weights": POP,
    "population_band_ages_note": "DOPA bands start at 26: '25-34' is ages 26 to 35, '35-44' is 36 to 45, '45-59' is 46 to 60; both-sex weights used for men",
}

# ---------------------------------------------------------------- population weights: age 60 counted twice in the held bands
# The held "45-59" band is ages 46 to 60 in full and the held "60+" band includes one fifth of the 56 to 60 band, so age 60 is in
# both. The main run above uses the corrected weights (duplicate removed from 45-59, where age 60 does not belong: the kidney
# rows for "45-59" are the 40-49 and 50-59 rows, and the rows for "60+" start at 60). This block re-runs the headline with the
# weights as held, with the duplicate removed from 60+ instead, and with the 56 to 60 band 10 percent smaller and larger than the
# equal-thirds assumption, so the effect of the correction is visible. Population weights are restored afterwards.
POP_MAIN = dict(POP)


def _set_pop(newpop):
    global POP, TOT_ADULTS, NAT_TREATED_25PLUS, TREATED_YOUNG_PROXY
    POP = dict(newpop)
    TOT_ADULTS = float(sum(POP[b] for b in BANDS))
    NAT_TREATED_25PLUS, TREATED_YOUNG_PROXY = treated_young_low()


def _pop_run(note, newpop):
    _set_pop(newpop)
    agg = aggregates("span")
    out = {"note": note, "weights_persons": {b: int(round(v)) for b, v in POP.items()}, "adults_25_plus_total_persons": int(round(TOT_ADULTS))}
    for nm in ("men_25_34", "men_25_59", "adults_25_plus"):
        out[nm] = {"narrow_pct_low_mid_high": agg[nm]["narrow_pct_low_mid_high"], "broad_pct_low_mid_high": agg[nm]["broad_pct_low_mid_high"]}
    out["adults_25_plus"]["narrow_persons_millions_low_mid_high"] = agg["adults_25_plus"]["narrow_persons_millions_low_mid_high"]
    out["adults_25_plus"]["broad_persons_millions_low_mid_high"] = agg["adults_25_plus"]["broad_persons_millions_low_mid_high"]
    out["treated_share_young_proxy_25_34_and_35_44"] = {b: round(v, 4) for b, v in TREATED_YOUNG_PROXY.items()}
    return out


def _w(k45, k60):
    w = dict(POP_AS_HELD)
    w["45-59"] = POP_AS_HELD["45-59"] - k45 * DUP_AGE60_ESTIMATE
    w["60+"] = POP_AS_HELD["60+"] - k60 * DUP_AGE60_ESTIMATE
    return w


pop_correction = {
    "problem": ("In the held weights (segment_potency_mc.py, DOPA Nov B.E. 2568) '45-59' is 46-50, 51-55 and 56-60 in full and '60+' is 61 and over "
                "plus one fifth of 56-60, so age 60 (one fifth of the 56 to 60 band) is counted in both bands."),
    "duplicate_estimate_persons": int(round(DUP_AGE60_ESTIMATE)),
    "duplicate_estimate_basis": "ASSUMPTION: the 46-50, 51-55 and 56-60 bands are equal thirds of the held 45-59 total; the 56-60 band count is not in the repo (DOPA table not re-opened).",
    "scenarios": {
        "as_held_age_60_counted_twice": _pop_run("weights as held in segment_potency_mc.py (the earlier T10 runs)", _w(0, 0)),
        "corrected_removed_from_45_59_used_in_this_record": _pop_run("duplicate removed from 45-59 (used)", _w(1, 0)),
        "removed_from_60plus_instead": _pop_run("duplicate removed from 60+ instead (the alternative a reviewer may prefer)", _w(0, 1)),
        "corrected_with_56_60_band_10pct_smaller": _pop_run("duplicate 10 percent smaller than the equal-thirds estimate, removed from 45-59", _w(0.9, 0)),
        "corrected_with_56_60_band_10pct_larger": _pop_run("duplicate 10 percent larger than the equal-thirds estimate, removed from 45-59", _w(1.1, 0)),
    },
    "why_remove_from_45_59": ("The kidney rows used for '45-59' are the 40-49 and 50-59 rows and those for '60+' start at 60, so a person aged 60 belongs in "
                              "'60+'. Removing the duplicate from 60+ would keep age 60 in the lower-prevalence band and lowers the adult value."),
}
_set_pop(POP_MAIN)   # restore the corrected weights
assert coverage["aggregates"]["adults_25_plus"]["narrow_pct_low_mid_high"] == aggregates("span")["adults_25_plus"]["narrow_pct_low_mid_high"]

# ---------------------------------------------------------------- proposed judge-facing text (numbers are written from the results above)
_m34 = coverage["aggregates"]["men_25_34"]["narrow_pct_low_mid_high"]
_ad = coverage["aggregates"]["adults_25_plus"]["narrow_pct_low_mid_high"]
_ad_m = coverage["aggregates"]["adults_25_plus"]["narrow_persons_millions_low_mid_high"]
COV = {
    "men_25_34_mid": f"{round(_m34[1])}%",
    "adults_mid": f"{round(_ad[1])}%",
    "men_25_34_bounds": f"{_m34[0]:.1f}% to {_m34[2]:.1f}%",
    "adults_bounds": f"{round(_ad[0])}% to {round(_ad[2])}%",
    "adults_millions_mid": f"{round(_ad_m[1])} million",
}
PROPOSED_TEXT = {
    "slide_7_caveat": ("Potassium is about 317 mg a serve, 9% of the Thai 3,500 mg reference, or 16% to 21% of the 1,500 to 2,000 mg a day "
                       "a Thai guideline gives kidney patients on a low-potassium diet. Medicines that raise potassium add risk. "
                       "Gate 2 requires a medical view."),
    "slide_7_speaker_note": ("State the medical caveat aloud. One serve is about 9% of the Thai reference of 3,500 mg a day. A Thai nutrition guideline "
                             "recommends a low-potassium diet of not more than 1,500 to 2,000 mg a day for chronic kidney disease before dialysis, and its "
                             "explanation applies that limit when blood potassium is high; for a patient on that limit one serve is about 16% to 21% of the day. "
                             "KDIGO 2024 sets no daily figure, a secondary review reports the same for KDOQI 2020, and the Thai guideline gives no figure by "
                             "kidney disease stage. KDIGO 2024 reports about 90% absorption for potassium salts in processed foods, against 50% to 60% for "
                             "plant foods; applying the 90% to the cube is our extrapolation. "
                             f"Who the caution covers: about {COV['men_25_34_mid']} of men aged 25 to 34 and about {COV['adults_mid']} of adults aged 25 and over, "
                             f"about {COV['adults_millions_mid']} people, counting kidney disease at stage 3 to 5 and ACE inhibitor or ARB treatment for high blood "
                             f"pressure only (model bounds {COV['men_25_34_bounds']} and {COV['adults_bounds']}; derived). "
                             "The bounds are our model bounds, not a statistical interval: the central value is a midpoint of assumed bounds, and the "
                             "width comes mainly from the kidney input (the survey chosen and, for adults, the split of people aged 60 and over), the share of young "
                             "adults who are treated, the factor for young men's high blood pressure, the ACE inhibitor and ARB share (taken from a hospital "
                             "sample with mean age 65) and the overlap rule. About three quarters of the adult figure is people aged 60 "
                             "and over. A reviewer may reject the serve, require the precaution, or ask for less carbonation: potassium falls by about 58 mg "
                             "for each 0.1 volume of carbon dioxide removed (derived)."),
    "stated_limit": ("Potassium and kidney disease are a stated limit of this proposal. One serve contains about 317 mg of potassium, about 9% of the Thai "
                     "reference intake of 3,500 mg a day. A Thai nutrition guideline recommends a low-potassium diet of not more than 1,500 to 2,000 mg a day "
                     "for adults with chronic kidney disease before dialysis, and its explanation applies that limit when blood potassium is high. For a "
                     "patient on that limit one serve is about 16% to 21% of the day. KDIGO 2024 sets no daily figure, a secondary review reports the same "
                     "for KDOQI 2020, the Thai guideline gives no figure by kidney disease stage, and the UK Kidney Association (2023) describes the "
                     "historical low-potassium diet as 2 to 3 g a day and does not recommend a blanket restriction. KDIGO 2024 reports absorption of about 90% "
                     "for potassium salts added to processed foods. We apply that figure to the dissolved cube as our own extrapolation, and the cube has not "
                     "been tested for absorption. US medicine labels and the UK Kidney Association guideline name potassium supplements and salt substitutes "
                     "as adding to the risk of high blood potassium for people taking ACE inhibitors, ARBs and similar medicines. Our model, built from Thai "
                     f"survey data, puts the share of men aged 25 to 34 who have kidney disease at stage 3 to 5 or take an ACE inhibitor or ARB for high blood "
                     f"pressure at about {COV['men_25_34_mid']}, and the share of adults aged 25 and over at about {COV['adults_mid']}. The model bounds are "
                     f"{COV['men_25_34_bounds']} and {COV['adults_bounds']}. They are the extremes of our assumptions, not a statistical interval, and the "
                     "central values are midpoints of those assumptions. Other potassium-raising medicines and heart failure are not counted, because no Thai "
                     "figure was found. The kidney count includes people who do not know they have kidney disease (in Thai SEEK only 1.9% of people with kidney "
                     "disease of any stage were aware of it), so a warning that begins with a diagnosis reaches few of them. No clinician has reviewed the "
                     "serve. The proposal therefore carries a precaution, makes no potassium claim, and holds sale until a medical review is complete."),
    "slide_7_source_line": ("Thai reference: Notification of the Ministry of Public Health No. 445 B.E. 2566, Annex 3, English translation published by the Thai FDA "
                            "(primary). Kidney guidance: KDIGO 2024 (primary); UK Kidney Association, Management of Hyperkalaemia in Adults, October 2023 (primary); "
                            "KDOQI 2020 as reported in secondary reviews (Molina et al., Frontiers in Medicine 2021; Lambert et al., Nephrology 2022); "
                            "Clinical Practice Recommendation for Nutritional Management in Adult Kidney Patients, B.E. 2561 (updated B.E. 2563), Thai Society for "
                            "Parenteral and Enteral Nutrition with the Nephrology Society of Thailand, recommendation 4.4.3 (primary). Medicine labels on DailyMed "
                            "(primary): Cozaar, Aldactone, Inspra, amiloride, Zestril. Food values: USDA FoodData Central (primary). Coverage: NHES V, NHES III, "
                            "NHES VI, Thai SEEK and National Health Security Office prescribing data (primary; derived, with proxies named)."),
}
text_counts = {k: len(v.split()) for k, v in PROPOSED_TEXT.items()}
banned = ["—", "–", "·"]   # em dash, en dash, middle dot
text_check = {"em_en_dash_or_middle_dot_found": any(b in v for v in PROPOSED_TEXT.values() for b in banned)}

results = {
    "serve": serve,
    "comparison_foods": comp,
    "foods_input": foods,
    "rx_effervescent_products_mg": products,
    "cube_as_fraction_of_product": prod_cmp,
    "us_21cfr201_306_and_99mg": fda,
    "us_fda_dv_and_claims": us_dv,
    "claim_thresholds": claims,
    "levers_and_repeat_serves": levers,
    "coverage": coverage,
    "coverage_comparator_runs": scenarios,
    "coverage_range_drivers": drivers,
    "population_weights_correction_age_60": pop_correction,
    "proposed_text": PROPOSED_TEXT,
    "proposed_text_word_counts": text_counts,
    "proposed_text_check": text_check,
    "coverage_sensitivity_60plus_ckd_mid": sens60,
    "coverage_60plus_share_of_adult_headline": share60,
    "ckd_crosscheck": ckd_crosscheck,
    "notes": [
        "Heart failure is not in the model: no Thai population prevalence was found (stated limit).",
        "Other potassium-raising medicines (potassium-sparing diuretics, MRAs, trimethoprim, NSAIDs, heparin, calcineurin inhibitors, beta blockers) are not in the model: no Thai use shares were found. The narrow group counts ACEI and ARB users for hypertension only; ACEI or ARB use for other indications is not counted.",
        "Union bounds: low = full overlap (largest group), high = no overlap (sum at high inputs), mid = independence at mid inputs. The range is a set of model bounds, not a statistical interval, and the mid value is a midpoint of assumed bounds (see coverage_range_drivers). Independence at mid overstates the union if kidney disease and hypertension are positively correlated (expected; no Thai joint distribution was read).",
        "Kidney input: low and mid from NHES V (CKD-EPI, 2014); high is the higher of NHES V and the NHES III (MDRD, 2004) row for the band, both sexes, for men too (a ceiling; NHES III gives no age table by sex and its men to all ratio is 0.62).",
        "Men factors for hypertension and diabetes scale both-sex age tables by the age-standardised men to all ratio; the 1.5 upper factor for young men is an assumption.",
        "The 60 and over kidney mid is a plain midpoint of the 60 to 69 and 70 and over rows (ASSUMPTION; no 60 to 69 versus 70 and over population split was read). The 35 to 44 band is interpolated between the 20 to 39 and 40 to 49 rows.",
        "The caution would also reach people outside these groups (history of high blood potassium, adrenal disease, people told to avoid potassium); they are not counted.",
        "The per-100-kcal claim basis is a bound, not an energy value: energy per serve is not known because the binder and filler is not named.",
        "99 mg is not a figure in 21 CFR 201.306 (read in the eCFR current text and the official CFR 2014 print): the regulation's lines are 100 mg per tablet or unit and 20 mg per mL for liquids. The Council for Responsible Nutrition (trade body, S, undated page) says the 99 mg per dose limit is specific to over-the-counter drugs, that FDA has not ruled on potassium in dietary supplements, and that manufacturers have followed the limit in practice.",
        "Thai DMSc statement on coconut water (news report, S, undated; the picture path in the page points to April 2021): the one-coconut-a-day limit follows the Department of Health sugar guideline of 32 g a day and is tied to sugar and blood sugar, not potassium; the kidney warning is tied to diuresis and dehydration; potassium is named only for the irregular heartbeat warning. It gives one range of 133.81 to 215.20 mg per 100 g for potassium and chloride together (sum or per mineral not stated). It is not used as a potassium value, and not as support for any daily limit on the cube.",
        "Population weights: the held bands count age 60 twice (block population_weights_correction_age_60). This run removes the estimated duplicate (one fifth of one third of the held 45-59 total, ASSUMPTION) from the 45-59 band; removing it from 60+ instead gives a lower adult value, shown in the block.",
        "Treated share of hypertensive young adults: the NHSO hospital sample implies 5.3% (ages 25-34) and 19.4% (35-44); this is a PROXY estimate used as the low value of an assumed range, not a floor or lower bound for the national share.",
        "Notification 467 B.E. 2568 (English translation read): amends only paragraph one of clause 2.1 of Annex 1 of Notification 445 (white background, font sizes); potassium is still a Section 3 Part 1 nutrient in its font-size table. Annex 3 and Annex 4 are not touched.",
        "Solid per 100 g basis (Annex 4 Table 2, solid column): the cube as sold is about 8,345 mg of potassium per 100 g, 238 percent of the Thai RDI, above the 15 percent and 30 percent lines; the basis that applies to a dissolvable cube is not settled.",
        "Comparison foods are USDA FoodData Central values read on 20 October 2026 through the official API (first read) and the FoodData Central site's data endpoint (second read, raw JSON saved) (P). Densities come from USDA's own portion weights (US customary cup and fluid ounce taken as 236.588 mL and 29.5735 mL); at 1.0 g/mL the ratios are shown in comparison_foods.at_density_1_0.",
        "UK Kidney Association guideline (October 2023, P): historical low-potassium diet 2 to 3 g a day; blanket restriction not recommended; below 3 g a day or 1 mmol per kg ideal body weight for persistent serum potassium of 5.5 mmol/L or more (page 37).",
    ],
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("wrote", OUT)
for name in AGGS:
    e = coverage["aggregates"][name]
    print(name, "narrow", e["narrow_pct_low_mid_high"], "broad", e["broad_pct_low_mid_high"])
print("comparators")
for sc, agg in scenarios.items():
    for name in ("men_25_34", "men_25_59", "adults_25_plus"):
        print(" ", sc, name, "narrow", agg[name]["narrow_pct_low_mid_high"])
print("sens60", {k: v["adults_25_plus_narrow_pct_low_mid_high"] for k, v in sens60.items()})
print("share60", {k: v["share_of_total_from_60plus_pct"] for k, v in share60.items()})
print("ckd crosscheck", ckd_crosscheck)
print("claims", {k: v for k, v in claims.items() if "kcal" in k})
print("foods", comp)
print("ceilings", serve["pct_of_daily_ceiling"])
for nm, e in drivers.items():
    print("drivers", nm, e["headline_low_mid_high"], "overlap alone", e["overlap_rule_alone_mid_inputs_low_mid_high"], "all-low/high indep", e["all_inputs_low_or_high_with_independence_rule"],
          {k: v["low_mid_high"] for k, v in e["one_input_alone_low_mid_high"].items()}, "nhes5 high alone", e["kidney_high_from_nhes5_only_alone"], "nhes3 high alone", e["kidney_high_from_nhes3_only_alone"])
print("text word counts", text_counts, text_check)
print("population weights, held and corrected", POP_AS_HELD, POP, "duplicate estimate", pop_correction["duplicate_estimate_persons"])
for k, v in pop_correction["scenarios"].items():
    print(" ", k, v["adults_25_plus"]["narrow_pct_low_mid_high"], v["adults_25_plus"]["narrow_persons_millions_low_mid_high"], v["men_25_59"]["narrow_pct_low_mid_high"])
print("solid per 100 g", {k: v for k, v in claims.items() if k.startswith("solid") and k != "solid_basis_note"})
