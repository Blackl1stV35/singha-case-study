"""Migration from the PET inner pouch into the drink, against the verified Thai and EU limits.

Physics: short-time Fickian diffusion from a semi-infinite PET layer into a food with a sink condition
(food as an infinite sink, partition coefficient near zero). Migrant per area M/A = 2 C0 sqrt(D t / pi).
Frozen storage: diffusion is slow enough to ignore; only the 2-hour thawed contact is counted.

Limits (verified in rework/32 against Thai MoPH Notification No. 435 (B.E. 2565), in force from 18 June 2022):
  overall migration, PET: 10 mg/dm2 of food-contact surface
  antimony: 0.04 mg/kg (Table 2, all plastics)
  acetaldehyde: 6 mg/kg (Table 4, section 4.7)
  ethylene glycol: 30 mg/kg (Table 4, section 4.7)
  diethylene glycol: 30 mg/kg (Table 4, section 4.7)
No PET oligomer limit exists, so overall migration is the operative limit for oligomers.

Antimony leaches by surface processes, not bulk diffusion. For antimony the screen gives the leach fraction
that would reach the specific limit. Fat content above 20 % changes the simulant and can raise migration of
lipophilic substances; the screen shows how large that rise must be to remove the margin.

Run:  python pet_migration.py   (writes pet_migration_results.json)
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "pet_migration_results.json")

RHO_PET = 1380.0                 # kg/m3
PET_THICKNESS = 25e-6            # m, pouch film (assumed)
POUCH_AREA = 0.02                # m2 per serving (2 dm2)
SERVING_KG = 0.170               # kg of drink per serving
T_CONTACT = 2.0 * 3600.0         # s, thawed contact time
T_FROZEN_FACTOR = 1e-3           # diffusion slowdown at -18 C relative to 30 C (physics, assumed)

LIMIT_OVERALL_MG_DM2 = 10.0
LIMIT_ANTIMONY = 0.04            # mg/kg
SPECIFIC = {
    # substance: (residual mass fraction in PET, diffusivity in PET at 30 C, limit mg/kg, basis)
    "acetaldehyde": (1e-5, 1e-13, 6.0, "Thai Table 4 s4.7 item 1; EU group restriction"),
    "ethylene glycol (residual)": (1e-3, 1e-14, 30.0, "Thai Table 4 s4.7 item 12; EU group restriction"),
    "diethylene glycol (residual)": (1e-3, 1e-14, 30.0, "Thai Table 4 s4.7 item 5"),
}
OLIGOMERS = dict(w=0.01, D=1e-16)   # PET oligomers, overall migration (assumed residual 1 % w/w)


def migrant_per_area(w, D, t):
    """Migrant mass per unit pouch area after time t (kg/m2), sink condition."""
    c0 = RHO_PET * w
    return 2.0 * c0 * math.sqrt(D * t / math.pi)


def food_mg_per_kg(m_per_area):
    food_per_area = SERVING_KG / POUCH_AREA           # kg of food per m2 of pouch
    return m_per_area * 1e6 / food_per_area           # mg/kg


def main():
    results = {"limits": {"overall_mg_per_dm2": LIMIT_OVERALL_MG_DM2, "antimony_mg_per_kg": LIMIT_ANTIMONY,
                          "source": "Thai MoPH Notification No. 435 (B.E. 2565), verified in rework/32"},
               "assumptions": {"rho_PET_kg_m3": RHO_PET, "PET_thickness_m": PET_THICKNESS,
                               "pouch_area_m2": POUCH_AREA, "serving_kg": SERVING_KG,
                               "thawed_contact_h": T_CONTACT / 3600.0, "frozen_factor": T_FROZEN_FACTOR,
                               "model": "Fickian short-time, sink condition"},
               "overall_migration": {}, "specific_migration": {}, "antimony": {}, "fat_sensitivity": {}}

    # overall migration, in mg per dm2 of contact surface (the Thai and EU basis)
    m_oli = migrant_per_area(OLIGOMERS["w"], OLIGOMERS["D"], T_CONTACT)
    mg_dm2 = m_oli * 1e6 / 100.0                      # kg/m2 -> mg/dm2
    margin = LIMIT_OVERALL_MG_DM2 / mg_dm2
    results["overall_migration"] = {
        "migrant_mg_per_dm2_2h": round(mg_dm2, 3),
        "limit_mg_per_dm2": LIMIT_OVERALL_MG_DM2,
        "margin_times": round(margin, 2),
        "frozen_24h_mg_per_dm2": round(migrant_per_area(OLIGOMERS["w"], OLIGOMERS["D"] * T_FROZEN_FACTOR, 86400.0) * 1e6 / 100.0, 6),
    }

    for name, (w, D, limit, basis) in SPECIFIC.items():
        m = migrant_per_area(w, D, T_CONTACT)
        c = food_mg_per_kg(m)
        results["specific_migration"][name] = {
            "food_mg_per_kg_2h": round(c, 4),
            "limit_mg_per_kg": limit,
            "margin_times": round(limit / c, 1),
            "basis": basis,
        }

    # antimony: residual Sb and the leach fraction that would reach the specific limit
    sb_residual_mg_per_kg = 300.0                     # upper end of the usual catalyst residue range (assumed)
    pet_mass_g = RHO_PET * POUCH_AREA * PET_THICKNESS * 1000.0
    sb_in_pouch_mg = pet_mass_g * sb_residual_mg_per_kg / 1000.0
    sb_if_all_leach_mg_per_kg = sb_in_pouch_mg / SERVING_KG
    results["antimony"] = {
        "PET_mass_per_pouch_g": round(pet_mass_g, 3),
        "residual_Sb_mg_per_kg_PET": sb_residual_mg_per_kg,
        "Sb_in_pouch_mg": round(sb_in_pouch_mg, 4),
        "food_mg_per_kg_if_all_leach": round(sb_if_all_leach_mg_per_kg, 3),
        "limit_mg_per_kg": LIMIT_ANTIMONY,
        "leach_fraction_at_limit": round(LIMIT_ANTIMONY / sb_if_all_leach_mg_per_kg, 4),
        "decision": "specify antimony-free PET (titanium or germanium catalysed); antimony would otherwise need "
                    "a leach test below the fraction above",
    }

    # fat sensitivity: how much fat-driven migration the overall margin can absorb
    results["fat_sensitivity"] = {
        "overall_margin_times": round(margin, 2),
        "statement": "migration into a fatty food (fat above 20 %, EU fat correction and olive-oil simulant) "
                     "must rise by less than this factor to stay within 10 mg/dm2; the fat content of the drink "
                     "must be measured",
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    print("Overall migration (oligomers, 2 h, mg/dm2): %.3f vs limit 10 (margin %.1fx)" % (mg_dm2, margin))
    for name, s in results["specific_migration"].items():
        print("  %-30s %s mg/kg vs %s (margin %sx)" % (name, s["food_mg_per_kg_2h"], s["limit_mg_per_kg"], s["margin_times"]))
    a = results["antimony"]
    print("Antimony: %.3f g PET, %.3f mg per pouch; if all leaches %.3f mg/kg vs 0.04; leach fraction at the limit %.4f" % (
        a["PET_mass_per_pouch_g"], a["Sb_in_pouch_mg"], a["food_mg_per_kg_if_all_leach"], a["leach_fraction_at_limit"]))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
