"""Sodium per serve for the Singha Lemon Soda Cube, binder screen arithmetic (T11, 20 October 2026).

Deterministic arithmetic only (no random numbers, so no seed is needed). Writes sodium_check_results.json
next to this file. Every input carries a tier:
  SOURCED   read in a saved page under rework/raw/diligence_2026-10-20/T11/
  DERIVED   our arithmetic on the inputs shown
  ASSUMPTION a design setting or ceiling chosen for this model, not sourced

Run: python rework/screen/sodium_check.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- cube recipe, basis B (rework/64, ASSUMPTION for binder and flavour; reactants DERIVED earlier) ----
VOLUME_ML = 330.0
MASS_G = {
    "potassium_bicarbonate": 0.81,
    "citric_acid": 2.10,
    "sucralose": 0.033,
    "binder_filler": 0.80,
    "lemon_flavour": 0.05,
}
CUBE_MASS_G = sum(MASS_G.values())

# ---- sodium ceilings per component (purchase-specification design, ASSUMPTION) ----
NA_PER_NA2SO4 = 2 * 22.98977 / (2 * 22.98977 + 32.06 + 4 * 15.9994)  # 0.3238, mass fraction of Na in sodium sulphate
# For organic components the sodium is bounded by the sulphated ash: all of it as sodium sulphate at most.
ASH_CEILING = {            # mass fraction of the component (ASSUMPTION; supplier certificate to replace)
    "citric_acid": 0.001,   # 0.10 percent
    "sucralose": 0.010,     # 1.0 percent
    "binder_filler": 0.001, # 0.10 percent (mannitol or isomalt, crystalline polyol)
}
NA_FRACTION_CEILING = {    # mass fraction of Na in the component (ASSUMPTION)
    "potassium_bicarbonate": 0.001,  # 0.10 percent, the proposed purchase limit (the supplier sheet read has none)
    "lemon_flavour": 0.005,          # 0.5 percent, flavour powder on maltodextrin or gum acacia carrier, no sodium salt added
}
# Pouch: overall migration limit for PET 10 mg/dm2 (SOURCED rework/32, Notification 435 Annex 1 Table 1 item 6)
OML_MG_PER_DM2 = 10.0
POUCH_FACE_CM2 = 63.0          # front 70 x 90 mm (rework/mockup style tokens, ASSUMPTION for the print panel)
POUCH_CONTACT_DM2 = 2 * POUCH_FACE_CM2 / 100.0   # both faces, seals ignored
POUCH_NA_SHARE_OF_MIGRANTS = 0.01   # ASSUMPTION: sodium is at most 1 percent of the migrants
LOW_FRACTION_OF_CEILING = 0.10      # ASSUMPTION: lots usually run an order below the purchase ceiling


def na_ceiling_mg(component):
    g = MASS_G.get(component, 0.0)
    if component in NA_FRACTION_CEILING:
        return g * 1000.0 * NA_FRACTION_CEILING[component]
    if component in ASH_CEILING:
        return g * 1000.0 * ASH_CEILING[component] * NA_PER_NA2SO4
    raise KeyError(component)


rows = []
total_high = 0.0
for comp in ["potassium_bicarbonate", "citric_acid", "sucralose", "binder_filler", "lemon_flavour"]:
    hi = na_ceiling_mg(comp)
    lo = hi * LOW_FRACTION_OF_CEILING
    basis = ("Na mass fraction ceiling %.3f percent" % (NA_FRACTION_CEILING[comp] * 100)
             if comp in NA_FRACTION_CEILING
             else "sulphated ash ceiling %.2f percent x 0.3238 (Na share of sodium sulphate) = %.4f percent Na"
                  % (ASH_CEILING[comp] * 100, ASH_CEILING[comp] * NA_PER_NA2SO4 * 100))
    rows.append({
        "component": comp, "mass_g": MASS_G[comp], "basis": basis,
        "na_mg_low": round(lo, 4), "na_mg_high": round(hi, 4),
        "tier": "ASSUMPTION (ceiling) with DERIVED arithmetic",
    })
    total_high += hi

pouch_oml_total_mg = OML_MG_PER_DM2 * POUCH_CONTACT_DM2
pouch_high = pouch_oml_total_mg * POUCH_NA_SHARE_OF_MIGRANTS
rows.append({
    "component": "pouch_film_migration", "mass_g": None,
    "basis": "overall migration cap %.1f mg/dm2 x %.2f dm2 contact = %.2f mg of all migrants; sodium at most %.0f percent of it"
             % (OML_MG_PER_DM2, POUCH_CONTACT_DM2, pouch_oml_total_mg, POUCH_NA_SHARE_OF_MIGRANTS * 100),
    "na_mg_low": round(pouch_high * LOW_FRACTION_OF_CEILING, 4), "na_mg_high": round(pouch_high, 4),
    "tier": "ASSUMPTION (sodium share) on a SOURCED overall migration limit",
})
total_high += pouch_high
total_low = sum(r["na_mg_low"] for r in rows)

for r in rows:
    r["na_mg_per_100ml_low"] = round(r["na_mg_low"] / VOLUME_ML * 100, 4)
    r["na_mg_per_100ml_high"] = round(r["na_mg_high"] / VOLUME_ML * 100, 4)

summary = {
    "total_na_mg_per_serve_low": round(total_low, 3),
    "total_na_mg_per_serve_high": round(total_high, 3),
    "total_na_mg_per_100ml_low": round(total_low / VOLUME_ML * 100, 4),
    "total_na_mg_per_100ml_high": round(total_high / VOLUME_ML * 100, 4),
    "percent_of_thai_sodium_free_limit_5mg_high": round(total_high / 5.0 * 100, 1),
    "percent_thai_rdi_2000mg_high": round(total_high / 2000.0 * 100, 3),
}

# ---- stress and break-even on potassium bicarbonate sodium ----
others_high = total_high - na_ceiling_mg("potassium_bicarbonate")
kb_mg = MASS_G["potassium_bicarbonate"] * 1000.0
sensitivity = []
for pct in [0.02, 0.10, 0.25, 0.50, 1.00]:
    na = kb_mg * pct / 100.0
    sensitivity.append({
        "khco3_na_percent": pct, "khco3_na_mg": round(na, 3),
        "total_with_others_at_ceiling_mg": round(na + others_high, 3),
        "passes_thai_below_5mg": (na + others_high) < 5.0,
        "passes_internal_release_3_5mg": (na + others_high) < 3.5,
    })
breakeven = {
    "others_at_ceiling_mg": round(others_high, 3),
    "khco3_na_percent_for_total_5mg": round((5.0 - others_high) / kb_mg * 100, 3),
    "khco3_na_percent_for_total_3_5mg": round((3.5 - others_high) / kb_mg * 100, 3),
}

# ---- Thai claim basis: reference serving and labelled serving ----
ref_fraction = 200.0 / VOLUME_ML   # defined amount for preparing 200 mL (Notification 445 Annex 2 category 2 item 3)
claim_basis = {
    "labelled_serving_ml": VOLUME_ML,
    "reference_serving_ml": 200.0,
    "labelled_as_percent_of_reference": round(VOLUME_ML / 200.0 * 100, 1),
    "cap_percent_of_reference": 200,
    "reference_portion_of_one_cube": round(ref_fraction, 3),
    "na_mg_per_reference_portion_high": round(total_high * ref_fraction, 3),
    "na_mg_per_labelled_serving_high": round(total_high, 3),
    "binding_limit": "the labelled serving (one cube): the reference portion holds less sodium than the whole cube",
    "thai_sodium_free_limit_mg": 5, "thai_very_low_limit_mg": 35, "thai_low_limit_mg": 140,
    "internal_release_limit_mg": 3.5,
    "internal_release_limit_basis": "70 percent of the Thai limit (ASSUMPTION: room for analytical uncertainty and lot spread)",
    "codex_sodium_free_mg_per_100g": 5, "codex_very_low_mg_per_100g": 40, "codex_low_mg_per_100g": 120,
    "codex_margin_x_at_high": round(5.0 / (total_high / VOLUME_ML * 100), 1),
    "codex_margin_x_at_low": round(5.0 / (total_low / VOLUME_ML * 100), 1),
    "thai_5mg_per_330ml_equals_mg_per_100ml": round(5.0 / VOLUME_ML * 100, 3),
    "ratio_codex_free_to_thai_basis_at_330ml": round(5.0 / (5.0 / VOLUME_ML * 100), 2),
}

# ---- water sodium sensitivity (water is outside the cube; illustrative values, not Thai measurements) ----
water = [{"water_na_mg_per_l": w, "added_mg_per_330ml": round(w * VOLUME_ML / 1000.0, 3)} for w in (5, 10, 20, 50)]

# ---- binder candidates: dose, limits, energy, cost ----
USD_THB = 33.55  # Bank of Thailand midpoint, 15 October 2026 (SOURCED raw/bot_fx_primary_2026-10-15.md)
BODY_KG = 60.0   # ASSUMPTION, adult reference body weight
cands = {}
dose = MASS_G["binder_filler"]
drink_kg = (CUBE_MASS_G / 2.0 + VOLUME_ML) / 1000.0   # Thai 468 clarification Annex 4: C = A/D + B with D = 2 if unknown
cands["thai_ready_to_drink_mass_kg"] = round(drink_kg, 4)
cands["binder_level_as_ready_to_drink_mg_per_kg"] = round(dose * 1000.0 / drink_kg, 0)
peg_limit_mg_per_kg = 500.0
cands["peg_thai_limit_mg_per_kg_rtd"] = peg_limit_mg_per_kg
cands["peg_max_per_cube_mg"] = round(peg_limit_mg_per_kg * drink_kg, 1)
cands["peg_at_0_8g_over_limit_x"] = round(dose * 1000.0 / drink_kg / peg_limit_mg_per_kg, 2)
cands["peg_dose_mg_per_kg_bw_at_0_8g"] = round(dose * 1000.0 / BODY_KG, 2)
cands["peg_adi_jecfa_mg_per_kg_bw"] = 10
cands["peg_adi_scf_mg_per_kg_bw"] = 5
cands["peg_dose_as_percent_of_jecfa_adi_at_0_8g"] = round(dose * 1000.0 / BODY_KG / 10 * 100, 0)
cands["peg_dose_as_percent_of_scf_adi_at_0_8g"] = round(dose * 1000.0 / BODY_KG / 5 * 100, 0)

tol = {
    "mannitol_vs_laxative_20g_percent": round(dose / 20.0 * 100, 1),            # encyclopaedia S
    "mannitol_vs_lowest_trial_dose_50g_percent": round(dose / 50.0 * 100, 1),   # Spada 2022 P
    "isomalt_vs_30g_mild_symptoms_percent": round(dose / 30.0 * 100, 1),        # Koutsou 1996 P
    "erythritol_vs_child_noel_15g_percent": round(dose / 15.0 * 100, 1),        # Jacqz-Aigrain 2015 P
    "erythritol_vs_efsa_adi_0_5g_per_kg_at_60kg_percent": round(dose / (0.5 * BODY_KG) * 100, 1),
    "binder_concentration_g_per_100ml": round(dose / VOLUME_ML * 100, 3),
    "mannitol_study_solution_g_per_100ml_ajaj": 2.5,
    "mannitol_solubility_g_per_kg_water_25c": 250.0,                            # Fontenele 2025 P
    "mannitol_dose_g_per_kg_water_in_drink": round(dose / (VOLUME_ML / 1000.0), 2),
    "solubility_margin_x": round(250.0 / (dose / (VOLUME_ML / 1000.0)), 0),
}

energy = {  # Notification 445 Annex 1 section 2.4 factors (SOURCED)
    "mannitol_kcal_per_g": 1.6, "isomalt_kcal_per_g": 2.0, "erythritol_kcal_per_g": 0.0, "sorbitol_kcal_per_g": 2.6,
    "organic_acid_kcal_per_g": 3.0,
    "kcal_binder_mannitol": round(1.6 * dose, 2), "kcal_binder_isomalt": round(2.0 * dose, 2),
    "kcal_binder_erythritol": 0.0, "kcal_citric_acid_per_cube": round(3.0 * MASS_G["citric_acid"], 2),
}

unit = {  # UN Comtrade Thailand imports 2025, CIF value over net weight (SOURCED rows, DERIVED ratio)
    "mannitol_world": (2095441.421, 476781.0),
    "mannitol_china": (1299035.829, 427232.0),
    "polyol_basket_290549_world": (6535824.369, 3692852.63),
    "sorbitol_290544_world": (18870735.432, 27317175.591),
    "dextrin_350510_china": (6763776.52, 6676632.063),
}
cost = {}
for k, (cif, kg) in unit.items():
    usd = cif / kg
    thb_kg = usd * USD_THB
    cost[k] = {"usd_per_kg": round(usd, 3), "thb_per_kg": round(thb_kg, 1),
               "thb_per_cube_0_8g": round(thb_kg * dose / 1000.0, 4)}
cost["mannitol_world_dc_premium_x2_thb_per_cube"] = round(cost["mannitol_world"]["thb_per_cube_0_8g"] * 2, 4)
cost["mannitol_world_dc_premium_x3_thb_per_cube"] = round(cost["mannitol_world"]["thb_per_cube_0_8g"] * 3, 4)
cost["thb_per_cube_per_100_thb_per_kg_binder"] = round(100.0 * dose / 1000.0, 3)
cost["cube_cost_6_carton_thb_excl_binder"] = 4.09
cost["mannitol_world_share_of_cube_cost_percent"] = round(cost["mannitol_world"]["thb_per_cube_0_8g"] / 4.09 * 100, 1)
cost["mannitol_x3_share_of_cube_cost_percent"] = round(cost["mannitol_world_dc_premium_x3_thb_per_cube"] / 4.09 * 100, 1)
EX_FACTORY = 9.00   # THB per cube, ASSUMPTION in rework/56 (60 percent of a THB 15 shelf price)
for label, add in (("mannitol_world", cost["mannitol_world"]["thb_per_cube_0_8g"]),
                   ("mannitol_world_x3", cost["mannitol_world_dc_premium_x3_thb_per_cube"])):
    c = 4.09 + add
    cost["cube_cost_with_" + label] = round(c, 3)
    cost["contribution_with_" + label] = round(EX_FACTORY - c, 3)
    cost["margin_percent_with_" + label] = round((EX_FACTORY - c) / EX_FACTORY * 100, 1)
cost["contribution_excl_binder"] = round(EX_FACTORY - 4.09, 2)
cost["margin_percent_excl_binder"] = round((EX_FACTORY - 4.09) / EX_FACTORY * 100, 1)

# ---- excise arithmetic: even if the whole binder (or whole cube) counted as sugar ----
excise = {
    "binder_as_sugar_g_per_100ml": round(dose / VOLUME_ML * 100, 4),
    "whole_cube_as_sugar_g_per_100ml": round(CUBE_MASS_G / VOLUME_ML * 100, 4),
    "tier_a_boundary_g_per_100ml": 6.0,
    "binder_share_of_boundary_percent": round(dose / VOLUME_ML * 100 / 6.0 * 100, 1),
    "whole_cube_share_of_boundary_percent": round(CUBE_MASS_G / VOLUME_ML * 100 / 6.0 * 100, 1),
    "rate_baht_per_litre_tier_a": 0,
}

# ---- sodium in lemon-lime sodas read earlier (T8), for the 'naturally free' test ----
sodas = {   # per 100 ml (Sprite pages, P) or per 100 g (USDA SR Legacy via mirror, S); 1 ml taken as 1 g
    "sprite_india": 10.1, "sprite_hong_kong": 17.0, "usda_lemon_lime": 9.0,
}
sodas_330 = {k: round(v * 3.3, 1) for k, v in sodas.items()}
sodas_x = {k: round(v * 3.3 / 5.0, 1) for k, v in sodas.items()}

results = {
    "cube": {"mass_g": MASS_G, "dry_mass_g": round(CUBE_MASS_G, 3), "volume_ml": VOLUME_ML},
    "na_fraction_of_sodium_sulphate": round(NA_PER_NA2SO4, 4),
    "pouch": {"contact_dm2": POUCH_CONTACT_DM2, "overall_migration_cap_total_mg": round(pouch_oml_total_mg, 2)},
    "component_sodium": rows,
    "total": summary,
    "khco3_sensitivity": sensitivity,
    "khco3_breakeven": breakeven,
    "claim_basis": claim_basis,
    "water_sensitivity": water,
    "binder": {"limits": cands, "tolerance": tol, "energy": energy, "cost": cost},
    "excise": excise,
    "lemon_lime_sodas_sodium": {"per_100ml": sodas, "per_330ml_mg": sodas_330, "multiple_of_5mg": sodas_x},
    "assumption_flags": {
        "low_fraction_of_ceiling": LOW_FRACTION_OF_CEILING,
        "pouch_na_share_of_migrants": POUCH_NA_SHARE_OF_MIGRANTS,
        "body_weight_kg": BODY_KG,
        "usd_thb": USD_THB,
    },
}

out = os.path.join(HERE, "sodium_check_results.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("wrote", out)
print(json.dumps({"total": summary, "breakeven": breakeven}, indent=2))
