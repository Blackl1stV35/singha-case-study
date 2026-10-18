"""Migration from the PET inner pouch into the drink, from physical reasoning.

Model: short-time Fickian diffusion from a semi-infinite PET layer into a food with a sink condition
(food as an infinite sink, partition coefficient near zero). Migrant per area M/A = 2 C0 sqrt(D t / pi).
Frozen storage: diffusion is slow enough to ignore; only the 2-hour thawed contact is counted.

Antimony is special: it is a catalyst residue bound in the PET, and leaches by surface processes, not by
bulk diffusion. For antimony the bound is the fraction of residual antimony that can leach in 2 hours,
so the result is expressed as the leach fraction that would breach the limit.

All diffusivities, residual levels and leach fractions are physics-based assumptions by substance class.
The compliance limits are read separately from the Thai and EU sources (rework/32).

Run:  python pet_migration.py   (writes pet_migration_results.json)
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "pet_migration_results.json")

RHO_PET = 1380.0                 # kg/m3
PET_THICKNESS = 25e-6            # m, pouch film (assumed)
POUCH_AREA = 0.02                # m2 per serving
SERVING_KG = 0.170               # kg of drink per serving
T_CONTACT = 2.0 * 3600.0         # s, thawed contact time
T_FROZEN_FACTOR = 1e-3           # diffusion slowdown at -18 C relative to 30 C (physics, assumed)

# substance: residual mass fraction in PET (kg/kg), diffusivity in PET at 30 C (m2/s), limit (mg/kg food) or None
SUBSTANCES = {
    "PET oligomers (overall migration)": dict(w=0.01, D=1e-16, limit_mg_per_kg=60.0,
                                              basis="EU overall migration 60 mg/kg food (10 mg/dm2)"),
    "acetaldehyde": dict(w=1e-5, D=1e-13, limit_mg_per_kg=6.0, basis="specific migration limit 6 mg/kg"),
    "ethylene glycol (residual)": dict(w=1e-3, D=1e-14, limit_mg_per_kg=None,
                                       basis="limit not yet verified (rework/32); no margin stated"),
}


def migrant_per_area(w, D, t):
    """Migrant mass per unit pouch area after time t (kg/m2), sink condition."""
    c0 = RHO_PET * w
    return 2.0 * c0 * math.sqrt(D * t / math.pi)


def concentration_in_food_mg_per_kg(m_per_area):
    food_per_area = SERVING_KG / POUCH_AREA           # kg of food per m2 of pouch
    return m_per_area * 1e6 / food_per_area           # mg/kg


def main():
    results = {"assumptions": {"rho_PET_kg_m3": RHO_PET, "PET_thickness_m": PET_THICKNESS,
                               "pouch_area_m2": POUCH_AREA, "serving_kg": SERVING_KG,
                               "thawed_contact_h": T_CONTACT / 3600.0, "frozen_factor": T_FROZEN_FACTOR,
                               "model": "Fickian short-time, sink condition"},
               "substances": {}, "antimony": {}}

    for name, s in SUBSTANCES.items():
        m = migrant_per_area(s["w"], s["D"], T_CONTACT)
        c = concentration_in_food_mg_per_kg(m)
        frozen_m = migrant_per_area(s["w"], s["D"] * T_FROZEN_FACTOR, 24 * 3600.0)
        results["substances"][name] = {
            "migrant_mg_per_dm2_2h": round(m * 1e6 / 100.0, 4),
            "food_mg_per_kg_2h": round(c, 4),
            "limit_mg_per_kg": s["limit_mg_per_kg"],
            "margin_times": round(s["limit_mg_per_kg"] / c, 1) if (c > 0 and s["limit_mg_per_kg"]) else None,
            "frozen_24h_food_mg_per_kg": round(concentration_in_food_mg_per_kg(frozen_m), 8),
            "basis": s["basis"],
        }

    # antimony: residual Sb and the leach fraction that would breach the specific migration limit
    sb_residual_mg_per_kg = 300.0                     # typical Sb catalyst residue range 150 to 300 mg/kg (assumed upper)
    pet_mass_g = RHO_PET * POUCH_AREA * PET_THICKNESS * 1000.0
    sb_in_pouch_mg = pet_mass_g * sb_residual_mg_per_kg / 1000.0
    sb_if_all_leach_mg_per_kg = sb_in_pouch_mg / SERVING_KG / 1000.0 * 1000.0
    sb_limit = 0.04                                   # mg/kg (EU specific migration limit for antimony)
    leach_fraction_at_limit = sb_limit / sb_if_all_leach_mg_per_kg
    results["antimony"] = {
        "PET_mass_per_pouch_g": round(pet_mass_g, 3),
        "residual_Sb_mg_per_kg_PET": sb_residual_mg_per_kg,
        "Sb_in_pouch_mg": round(sb_in_pouch_mg, 4),
        "food_mg_per_kg_if_all_leach": round(sb_if_all_leach_mg_per_kg, 3),
        "limit_mg_per_kg": sb_limit,
        "leach_fraction_at_limit": round(leach_fraction_at_limit, 4),
        "decision": "specify antimony-free PET (titanium or germanium catalysed); the antimony route is not compliant "
                    "if more than the leach fraction above is released in 2 h",
    }

    # breach measurement: cells to scan per breach, at each breach fraction (for the measurement question)
    cells_per_cm2 = 1.0 / (30e-6) ** 2 / 1e4
    results["measurement"] = {}
    for f in (1e-4, 1e-5, 1e-6, 1e-7, 1e-8):
        cells_needed = 1.0 / f
        results["measurement"]["%.0e" % f] = {
            "cells_to_scan_per_breach": cells_needed,
            "epidermis_area_cm2_per_breach": round(cells_needed / cells_per_cm2, 3),
        }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    print("Migration into a 170 mL serving, 2 h thawed contact (sink condition):")
    for name, s in results["substances"].items():
        print("  %-48s %s mg/kg vs limit %s (margin %sx)" % (name, s["food_mg_per_kg_2h"], s["limit_mg_per_kg"], s["margin_times"]))
    a = results["antimony"]
    print("Antimony: %.3f g PET, %.3f mg Sb per pouch; if all leaches %.3f mg/kg vs 0.04; leach fraction at the limit %.4f" % (
        a["PET_mass_per_pouch_g"], a["Sb_in_pouch_mg"], a["food_mg_per_kg_if_all_leach"], a["leach_fraction_at_limit"]))
    print("Breach measurement (cells to scan per breach):")
    for f, m in results["measurement"].items():
        print("  f=%s: scan %.0e cells = %.3g cm2 of epidermis" % (f, m["cells_to_scan_per_breach"], m["epidermis_area_cm2_per_breach"]))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
