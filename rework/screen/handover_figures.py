"""Handover figures for the recommended design (record 52, D14 to D16): 0.55 volume of CO2 per 330 mL,
working target pH 3.5, sucralose as the sweetener. Desk only. Reuses formulation_desk_model.py and
pack_economics.py in this folder; standard library only. Run with: python -I handover_figures.py
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import formulation_desk_model as fdm  # noqa: E402
import pack_economics as pe  # noqa: E402

OUT = HERE / "handover_figures_results.json"

DOSE = 0.55          # volumes of CO2 per 330 mL (D14)
PH = 3.5             # working target pH (D15)
SERVES_C = [5, 10, 15, 20, 25, 30, 35]
ICE_CASES = [("30 C water, 30 g ice", 30.0, 30.0), ("30 C water, 60 g ice", 30.0, 60.0)]
PH_LIST = [2.8, 3.0, 3.5, 4.0, 4.5]
RDI_K_MG = 3500.0    # Thai RDI for potassium, Notification 182 (primary copy), record 63 section 1
# Basis B additions (user, 19 October 2026; rework/64 section 8). Both are ASSUMPTION; ranges are in
# rework/48 section 6.1. Neither is priced (rework/53, row "Flavour and binder").
BINDER_FILLER_G = 0.80   # row "Binder and filler": 0.80 g (range 0.5 to 1.2). ASSUMPTION
FLAVOUR_G = 0.05         # row "Lemon flavour powder": 0.05 g (range 0.02 to 0.10). ASSUMPTION


def serve_row(t_c, ice_g=0.0):
    m = fdm.serve_model(dose_vol=DOSE, serve_c=t_c, ice_g=ice_g, target_ph=PH)
    return {
        "serve_c": m["serve_c"],
        "prepared_ml": round(m["v_total_L"] * 1000.0),
        "dissolved_vol": m["dissolved_vol_at_serve"],
        "fraction_leaving_at_once": m["escaped_fraction"],
        "time_above_threshold_min_upper_bound": m["t_above_threshold_min"],
        "time_constant_min_upper_bound": m["tau_min"],
    }


def main():
    base = fdm.serve_model(dose_vol=DOSE, serve_c=25.0, target_ph=PH)
    k_mg = base["potassium_mg_per_serve"]
    khco3_g = base["khco3_g"]
    citric_stoich_g = base["citric_stoich_g"]
    citric_total_g = base["citric_total_for_target_g"]
    citric_free_g = base["citric_free_for_target_g"]
    sucr_mg = fdm.sucralose_mg_per_serve(330.0)

    # Cost per cube, base prices from pack_economics.PRICES (status there), pH 3.5 total citric.
    # Binder and filler and lemon flavour are unpriced, so this cost is on reactants only.
    P = pe.PRICES
    reactants_thb = (khco3_g / 1000.0 * P["khco3_thb_per_kg"]["base"]
                     + citric_total_g / 1000.0 * P["citric_thb_per_kg"]["base"]
                     + sucr_mg / 1e6 * P["sucralose_thb_per_kg"]["base"])
    per_pouch = reactants_thb + P["pouch_thb"]["base"] + P["print_thb"]["base"] + P["processing_thb"]["base"]

    # Mass, basis B. Reactants are the bicarbonate, the total citric acid at the pH target and the sucralose.
    # Binder and filler and lemon flavour are added on top. The cube mass is derived, not weighed.
    reactants_g = khco3_g + citric_total_g + sucr_mg / 1000.0
    cube_mass_g = reactants_g + BINDER_FILLER_G + FLAVOUR_G
    pouch_mass_g = cube_mass_g + pe.POUCH_MASS_G      # packed unit (cube plus pouch); used for container mass
    packs = {}
    for n in (6, 12, 24):
        carton_cost = P["carton_thb"][n]["base"]
        carton_vol = pe.CARTON_DIMS_M3[n]
        per_cube = per_pouch + carton_cost / n
        containers = {}
        for name, c in pe.CONTAINERS.items():
            vol = c["length_m"] * c["width_m"] * c["height_m"]
            cartons = math.floor(vol * pe.PACKING_EFFICIENCY / carton_vol)
            cubes = cartons * n
            # Container mass: packed units (basis B, pouch_mass_g) plus empty cartons. Volume sets the count.
            mass_kg = cubes * pouch_mass_g / 1000.0 + cartons * pe.CARTON_MASS_KG
            containers[name] = {
                "cartons": cartons,
                "cubes": cubes,
                "container_mass_kg": round(mass_kg, 1),
                "payload_limit_kg": c["payload_kg"],
                "limited_by": "volume" if mass_kg <= c["payload_kg"] else "payload",
            }
        packs[str(n)] = {
            "cost_per_cube_thb": round(per_cube, 2),
            "ex_factory_thb_per_cube": round(P["shelf_thb_per_cube"]["base"] * P["ex_factory_share"]["base"], 2),
            "containers": containers,
        }

    result = {
        "design": {
            "co2_volumes_per_330ml": DOSE,
            "target_ph_working_anchor": PH,
            "sweetener": "sucralose (recommended; permitted at 300 mg/kg in category 14.1.4, condition 127)",
            "carbonation_agents": "potassium bicarbonate (quantum satis in 14.1.4) and citric acid (quantum satis in 14.1.4)",
        },
        "per_330ml_recipe": {
            "co2_mmol": round(DOSE * 0.330 / 22.414 * 1000.0, 2),
            "potassium_bicarbonate_g": khco3_g,
            "citric_acid_stoichiometric_g": citric_stoich_g,
            "citric_acid_total_for_pH_target_g": citric_total_g,
            "citric_acid_free_excess_g": citric_free_g,
            "potassium_mg": k_mg,
            "potassium_pct_of_thai_rdi": round(100.0 * k_mg / RDI_K_MG, 1),
            "sucralose_mg": sucr_mg,
            "sucralose_mg_per_kg": round(sucr_mg / 0.330, 1),
            "sucralose_limit_mg_per_kg": 300,
            "reactants_g": round(reactants_g, 3),
            "binder_filler_g": BINDER_FILLER_G,
            "flavour_g": FLAVOUR_G,
            "cube_mass_g": round(cube_mass_g, 3),
        },
        "serve_temperature": [serve_row(t) for t in SERVES_C],
        "ice_cases": [dict(name=name, **serve_row(t, ice_g=g)) for name, t, g in ICE_CASES],
        "citric_by_target_ph_g_per_330ml": {
            str(ph): {
                "total": fdm.serve_model(dose_vol=DOSE, serve_c=25.0, target_ph=ph)["citric_total_for_target_g"],
                "free": fdm.serve_model(dose_vol=DOSE, serve_c=25.0, target_ph=ph)["citric_free_for_target_g"],
            }
            for ph in PH_LIST
        },
        "cost_and_containers": {
            "reactants_thb_per_cube": round(reactants_thb, 3),
            "pouch_thb": P["pouch_thb"]["base"],
            "print_thb": P["print_thb"]["base"],
            "processing_thb": P["processing_thb"]["base"],
            "per_pouch_before_carton_thb": round(per_pouch, 2),
            "pouch_mass_g": round(pouch_mass_g, 2),
            "packs": packs,
        },
        "limits": [
            "desk model only; no bench test; the fizz duration is a surface-only upper bound (no nucleation)",
            "the sweetness target (6 g sugar per 100 mL equivalent) is an assumption; no sensory test",
            "the pH target is a working anchor; taste is untested",
            "the pouch and print costs are assumptions or non-Thai listings; no Thai quote was requested",
            "the 0.55-volume gate is not set; it is for R&D to define",
            "product classification (beverage, edible ice or electrolyte drink) is open; condition TH3 applies to electrolyte drinks only",
            "basis B: binder and filler 0.80 g (range 0.5 to 1.2) and lemon flavour 0.05 g (range 0.02 to 0.10) are ASSUMPTION (rework/48 section 6.1); the cube mass is derived, not weighed; binder and flavour are not priced, so the cost per cube excludes them",
            "binder name and its sodium content are unconfirmed (gate G3, rework/57 item 8); no sodium-free claim is made",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", OUT.name)


if __name__ == "__main__":
    main()
