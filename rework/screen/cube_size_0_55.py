"""Cube size and mass at the recommended dose (0.55 volume of CO2 per 330 mL, target pH 3.5).

Desk derivation, no lab data. Reads no other file. Writes cube_size_0_55_results.json
next to this script. Inputs and their status are listed below. The check at the top
reproduces the 1.75-volume design figures (4.23 g reactants, 15 mm at 1.56 g/cm3),
so the stoichiometry is tied to the earlier record before the new dose is used.
"""
import json
import os

# Stoichiometry (SOURCED constants, tier P for molar masses; same basis as rework/63)
MOLAR_VOL_L = 22.414      # L per mol at standard conditions, as used in rework/63
KHCO3_M = 100.12          # g per mol, potassium bicarbonate
CITRIC_M = 192.12         # g per mol, citric acid
K_M = 39.098              # g per mol, potassium
SERVE_L = 0.330

# Dose and recipe inputs
DOSE_VOL = 0.55           # rework/52 D14 (user, 19 October 2026)
CITRIC_TOTAL_PH35_G = 2.10  # rework/63 section 3 and the handover (DERIVED from pKa; S, UNVERIFIED)
SUCRALOSE_MG = 33.0       # rework/63 (DERIVED: 6 g sugar per 100 mL, divided by 600)
POUCH_MASS_G = 1.5        # pack_economics.py POUCH_MASS_G (ASSUMPTION, no converter quote)

# Basis B additions (user, 19 October 2026; rework/64 section 8). Both are ASSUMPTION. Ranges are in
# rework/48 section 6.1: row "Binder and filler" 0.80 g (range 0.5 to 1.2) and row "Lemon flavour powder"
# 0.05 g (range 0.02 to 0.10). The 0.17 g of the 1.75-volume design is citric acid excess, not binder.
BINDER_FLAVOUR_G = 0.80 + 0.05           # binder and filler 0.80 g plus lemon flavour 0.05 g (ASSUMPTION)

# Density band (ASSUMPTION, rework/48 section 6.4). Mid-point is the arithmetic mean.
BAND_LOW, BAND_HIGH = 1.25, 1.60
BAND_MID = (BAND_LOW + BAND_HIGH) / 2


def reactants_g(vol):
    """Potassium bicarbonate, stoichiometric citric acid and the free-acid excess at pH 3.5."""
    mol_co2 = vol * SERVE_L / MOLAR_VOL_L
    khco3 = mol_co2 * KHCO3_M
    citric_stoich = mol_co2 / 3.0 * CITRIC_M
    return mol_co2, khco3, citric_stoich


def side_mm(mass_g, density):
    """Edge length in mm of a cube of the given mass at the given density."""
    return (mass_g / density) ** (1.0 / 3.0) * 10.0


def density_at(mass_g, side):
    """Density in g/cm3 of a cube of the given mass and edge length in mm."""
    return mass_g / ((side / 10.0) ** 3)


out = {}

# Check: 1.75 volumes must give the 4.23 g reactants and the 15 mm density in rework/48
mol_175, khco3_175, citric_175 = reactants_g(1.75)
r175 = khco3_175 + citric_175
out["check_1_75_volume"] = {
    "khco3_g": round(khco3_175, 3),
    "citric_stoichiometric_g": round(citric_175, 3),
    "reactants_g": round(r175, 3),
    "expected_reactants_g": 4.23,
    "density_at_15mm_for_5_28g": round(density_at(5.28, 15.0), 3),
    "expected_density": 1.56,
    "ok": abs(r175 - 4.23) < 0.01 and abs(density_at(5.28, 15.0) - 1.56) < 0.01,
}

# Recommended dose
mol_co2, khco3, citric_stoich = reactants_g(DOSE_VOL)
citric_free = CITRIC_TOTAL_PH35_G - citric_stoich
sucralose_g = SUCRALOSE_MG / 1000.0
reactants = khco3 + CITRIC_TOTAL_PH35_G + sucralose_g
potassium_mg = mol_co2 * K_M * 1000.0

out["recipe_0_55_volume"] = {
    "co2_mmol": round(mol_co2 * 1000.0, 2),
    "khco3_g": round(khco3, 3),
    "citric_stoichiometric_g": round(citric_stoich, 3),
    "citric_free_excess_g": round(citric_free, 3),
    "citric_total_g": CITRIC_TOTAL_PH35_G,
    "sucralose_g": round(sucralose_g, 4),
    "reactants_g": round(reactants, 3),
    "potassium_mg_per_serve": round(potassium_mg, 1),
    "packed_unit_g_with_pouch": round(reactants + POUCH_MASS_G, 2),   # basis A
    "cube_mass_g_basis_B": round(reactants + BINDER_FLAVOUR_G, 3),
    "packed_unit_g_basis_B_with_pouch": round(reactants + BINDER_FLAVOUR_G + POUCH_MASS_G, 2),
}

# Two mass bases. A: reactants only, as in the earlier models (pouch mass 4.44 g). B: A plus binder and
# filler and lemon flavour (basis B, the design basis from 19 October 2026; both ASSUMPTION).
bases = {
    "A_reactants_only": reactants,
    "B_with_binder_and_flavour": reactants + BINDER_FLAVOUR_G,
}

out["cube_side_by_basis"] = {}
for name, mass in bases.items():
    out["cube_side_by_basis"][name] = {
        "mass_g": round(mass, 3),
        "side_mm_at_band_low_1_25": round(side_mm(mass, BAND_LOW), 2),
        "side_mm_at_band_mid_1_425": round(side_mm(mass, BAND_MID), 2),
        "side_mm_at_band_high_1_60": round(side_mm(mass, BAND_HIGH), 2),
        "side_mm_at_old_design_density_1_56": round(side_mm(mass, 1.56), 2),
    }

# Density at candidate sides, per basis (is the cube inside the assumed band?)
candidates = [12.5, 13.0, 13.5, 14.0, 15.0]
out["density_at_candidate_side"] = {}
for name, mass in bases.items():
    out["density_at_candidate_side"][name] = {
        str(s): round(density_at(mass, s), 3) for s in candidates
    }

# Pack depth: cube plus 2.5 mm per face, the rule in rework/48 section 6.1
out["pack_depth_mm"] = {str(s): round(s + 5.0, 1) for s in candidates}

out["status"] = {
    "stoichiometry": "DERIVED from SOURCED molar masses",
    "citric_total": "DERIVED from pKa, S, UNVERIFIED in the handover",
    "sucralose": "DERIVED, S",
    "density_band": "ASSUMPTION",
    "binder_and_flavour": "ASSUMPTION (rework/48 section 6.1: binder 0.5 to 1.2 g, flavour 0.02 to 0.10 g)",
    "cube_mass_basis_B": "DERIVED on ASSUMPTION inputs",
    "pouch_mass": "ASSUMPTION",
}

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "cube_size_0_55_results.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(json.dumps(out, indent=2, ensure_ascii=False))
