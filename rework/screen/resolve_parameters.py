"""Resolve the unknown parameters of the leak, spoilage and pathogen screens from physical reasoning.

Each parameter gets a value, its physical basis, and a sensitivity. Nothing here is a measurement.
The outputs feed the decision in rework/30_resolved_parameters.md.

Run:  python resolve_parameters.py   (writes resolved_parameters_results.json)
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LEAK = os.path.join(HERE, "pop_leak_simulation_results.json")
OUT = os.path.join(HERE, "resolved_parameters_results.json")

# --- geometry (from the pop model) -------------------------------------------
R_LEAF = 0.0205        # m, leaf wrap radius
H_WRAP = 0.100         # m, wrap height
WRAP_AREA = 2 * math.pi * R_LEAF * H_WRAP + 2 * math.pi * R_LEAF ** 2   # lateral + two caps, m2

# --- drink composition (physics and chemistry) -------------------------------
SUCROSE_WT = 0.08                       # 8 % sugar (assumed sweetened coconut-pandan drink)
M_SUC, M_WAT = 342.3, 18.02             # g/mol
n_s = SUCROSE_WT / M_SUC
n_w = (1 - SUCROSE_WT) / M_WAT
X_WATER = n_w / (n_w + n_s)             # ideal (Raoult) water activity
AW_RESOLVED = round(X_WATER, 3)
PH_RESOLVED = 6.3                       # coconut milk is near neutral; midpoint of the usual range

# --- lag and growth ----------------------------------------------------------
H0 = 2.0                                # Baranyi lag parameter h0 for cold-stressed cells (assumed)

# --- damaged paths: freeze-induced gaps ---------------------------------------
# Gap radius set by the order of plant cell-wall thickness (0.1 to 1 um after freeze rupture); log-uniform.
R_DAMAGE_LO, R_DAMAGE_HI = 0.1e-6, 1.0e-6

# --- cells per wrap and damage fraction ---------------------------------------
CELL_SIDE = 30e-6                       # m, mesophyll cell side (typical order)
N_CELLS = WRAP_AREA / (CELL_SIDE ** 2)  # cells in the wrap
DAMAGE_FRACTIONS = [1e-6, 1e-4, 1e-2]   # fraction of cells with a freeze-damaged gap (bracketing, assumed)

# --- stomata (open pores would wick at once) ---------------------------------
STOMATA_RADII = [5e-6, 10e-6, 15e-6]    # m, typical guard-cell pore radii (assumed)
ETA_DRINK, GAMMA_DRINK, COS_76 = 1.0e-3, 0.072, math.cos(math.radians(76.08))


def washburn_time_s(r):
    """Time for a path of radius r to wick the full wrap height (Washburn)."""
    return 2.0 * ETA_DRINK * H_WRAP ** 2 / (GAMMA_DRINK * COS_76 * r)


def p_leak_scan(scan, r):
    """Interpolate the single-path leak probability from the Monte Carlo scan (log r)."""
    pts = sorted((row["r_d_m"], row["P_leak"]) for row in scan)
    if r <= pts[0][0]:
        return pts[0][1]
    if r >= pts[-1][0]:
        return pts[-1][1]
    for (r0, p0), (r1, p1) in zip(pts, pts[1:]):
        if r0 <= r <= r1:
            f = (math.log(r) - math.log(r0)) / (math.log(r1) - math.log(r0))
            return p0 + f * (p1 - p0)
    return pts[-1][1]


def p_leak_loguniform(scan, lo, hi, n=400):
    """Average single-path leak probability over a log-uniform damage radius in [lo, hi]."""
    total = 0.0
    for i in range(n):
        u = (i + 0.5) / n
        r = math.exp(math.log(lo) + u * (math.log(hi) - math.log(lo)))
        total += p_leak_scan(scan, r)
    return total / n


def main():
    with open(LEAK, encoding="utf-8") as fh:
        leak = json.load(fh)
    scan = leak["monte_carlo"]["design_B_leak_probability_vs_damaged_radius"]

    p_single = p_leak_loguniform(scan, R_DAMAGE_LO, R_DAMAGE_HI)
    results = {
        "drink_composition": {"water_activity_ideal_raoult": AW_RESOLVED, "sucrose_wt": SUCROSE_WT,
                              "pH": PH_RESOLVED,
                              "basis": "near-neutral coconut milk; 8 % sugar; ideal water activity (Raoult); "
                                       "no preservative assumed"},
        "lag_h0": {"value": H0, "basis": "Baranyi lag parameter for cold-stressed cells, typical 1 to 3; "
                                         "lag = h0 / mu"},
        "damage_radius_m": {"lo": R_DAMAGE_LO, "hi": R_DAMAGE_HI,
                            "basis": "order of plant cell-wall thickness after freeze rupture; log-uniform"},
        "single_path_leak_probability_avg": round(p_single, 4),
        "cells_per_wrap": round(N_CELLS, -3),
        "wrap_area_m2": round(WRAP_AREA, 5),
        "damage_fractions": {},
        "stomata": {},
    }
    for f in DAMAGE_FRACTIONS:
        n_damaged = N_CELLS * f
        n_qual = n_damaged * p_single
        results["damage_fractions"]["%.0e" % f] = {
            "damaged_cells_per_wrap": round(n_damaged, 1),
            "expected_leaking_paths_per_wrap": round(n_qual, 2),
        }
    # damage fraction at which the expected number of leaking paths reaches one per wrap
    results["critical_damage_fraction_for_one_leaking_path"] = float("%.2e" % (1.0 / (N_CELLS * p_single)))

    for r in STOMATA_RADII:
        results["stomata"]["%.0f um" % (r * 1e6)] = {
            "washburn_climb_time_s": round(washburn_time_s(r), 0),
            "basis": "Washburn climb of the full 100 mm wrap, drink viscosity 1 mPa s, 76 degree contact angle",
        }

    # sensitivity: damage radius band
    results["sensitivity_single_path_leak"] = {
        "0.1 to 0.3 um": round(p_leak_loguniform(scan, 0.1e-6, 0.3e-6), 4),
        "0.1 to 1 um (resolved)": round(p_single, 4),
        "0.3 to 1 um": round(p_leak_loguniform(scan, 0.3e-6, 1.0e-6), 4),
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    print("water activity (Raoult, 8 percent sugar): %.3f | pH %.1f | h0 %.1f" % (AW_RESOLVED, PH_RESOLVED, H0))
    print("cells per wrap: %.2e | wrap area %.4f m2" % (N_CELLS, WRAP_AREA))
    print("single-path leak probability, log-uniform 0.1 to 1 um: %.3f" % p_single)
    for f, row in results["damage_fractions"].items():
        print("  damage fraction %s: %s damaged cells, %s expected leaking paths per wrap" % (
            f, row["damaged_cells_per_wrap"], row["expected_leaking_paths_per_wrap"]))
    print("critical damage fraction for one leaking path per wrap: %s" % results["critical_damage_fraction_for_one_leaking_path"])
    for r, row in results["stomata"].items():
        print("  stomata %s: wick the wrap in %s s" % (r, row["washburn_climb_time_s"]))
    print("sensitivity:", results["sensitivity_single_path_leak"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
