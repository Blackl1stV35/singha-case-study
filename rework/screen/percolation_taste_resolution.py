"""Resolve the percolation question and the taste effect of the inner barrier from physical reasoning.

Percolation: two physical regimes bound the leak. (i) Local, cell-scale connection: damaged cells connect
only when separated by less than a connection distance d_c through the cell structure. Continuum
percolation of discs gives a critical areal density of about 4.51 / (pi d_c^2). (ii) Connected airspace
network: leaf mesophyll intercellular air spaces form one connected network, so any damaged cell that
opens to it connects to the rest of the leaf, and a single qualifying breach exposed to the melt leaks.
The leak probability is then 1 - exp(-N_q), with N_q the expected number of qualifying breaches per wrap.
Leaf anatomy supports (ii); (i) is shown as the optimistic bound.

Taste: aroma scalping into the inner film. The uptake fraction of an aroma compound from a drink in a
film pouch is approximately F = K (A/V) sqrt(D t / pi), with K the polymer-water partition coefficient,
D the diffusivity in the polymer, t the contact time, A/V the film area per unit drink volume.
Values are physics-based assumptions set by polymer class, with a tenfold sensitivity on D.

Run:  python percolation_taste_resolution.py   (writes percolation_taste_results.json)
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "percolation_taste_results.json")
RESOLVED = os.path.join(HERE, "resolved_parameters_results.json")

CELL_SIDE = 30e-6                          # m, mesophyll cell side (as in rework/30)
CELLS_PER_M2 = 1.0 / CELL_SIDE ** 2        # cells per m2 of wrap surface
P_QUAL = 0.62                              # probability a breach is a qualifying leak (rework/30)
LAMBDA_CRIT_FACTOR = 4.51                  # critical excluded-area value for 2D continuum percolation of discs
CELLS_PER_WRAP = 1.72e7                    # from rework/30

# drink-to-pouch geometry: 170 mL drink in a pouch of about 0.02 m2
A_OVER_V = 0.02 / 170e-6                   # m^-1
CONTACT_T = 2.0 * 3600.0                   # s, two-hour contact

POLYMERS = {
    # name: (K polymer-water partition for an aroma ester or terpene, D m2/s in polymer, basis)
    "polyethylene (PE)": (1.0e3, 1.0e-12, "non-polar; strong uptake of terpene-like aromas"),
    "polypropylene (PP)": (1.0e3, 1.0e-12, "non-polar; similar uptake to PE"),
    "PET": (10.0, 1.0e-15, "polar, dense, low diffusivity for small molecules"),
    "EVOH": (5.0, 1.0e-16, "polar barrier; very low uptake of aroma"),
}


def local_threshold_fraction(d_c):
    """Damaged-cell fraction at which local (cell-scale) connection percolates, for connection distance d_c."""
    lam_c = LAMBDA_CRIT_FACTOR / (math.pi * d_c ** 2)       # critical defects per m2
    f_c = lam_c / (CELLS_PER_M2 * P_QUAL)
    return f_c


EPI_FRACTION = 0.25                        # epidermal cells per mesophyll thickness: 2 of about 8 layers (0.24 mm / 30 um)
STOMATA_PER_M2 = 2.0e5                     # stomata per m2, abaxial-rich leaf order of magnitude (assumed)
WRAP_AREA = 0.0155                         # m2, from rework/30


def connected_leak_probability(f):
    """Leak needs a qualifying breach on both epidermal surfaces that connect through the airspace network.

    The inner surface is always wetted by the melt. The outer surface is connected by breaches or by open
    stomata. Closed stomata: both surfaces need breaches. Open stomata: the outer surface is always connected.
    """
    n_q = CELLS_PER_WRAP * f * P_QUAL
    n_inner = EPI_FRACTION * n_q
    n_outer = EPI_FRACTION * n_q
    p_inner = 1.0 - math.exp(-n_inner)
    p_outer_breach = 1.0 - math.exp(-n_outer)
    p_closed = p_inner * p_outer_breach
    p_open = p_inner                       # open stomata connect the outer surface
    return p_closed, p_open, n_q


def scalping_fraction(K, D, sensitivity=1.0):
    return K * A_OVER_V * math.sqrt(sensitivity * D * CONTACT_T / math.pi)


def main():
    results = {"percolation": {"local_cell_scale": {}, "connected_airspace": {}},
               "taste": {}, "assumptions": {"cells_per_m2": CELLS_PER_M2, "p_qual": P_QUAL,
                                            "lambda_crit_factor": LAMBDA_CRIT_FACTOR,
                                            "contact_time_h": CONTACT_T / 3600.0, "A_over_V_per_m": A_OVER_V}}

    for d_c_mm in (0.03, 0.1, 0.5):
        f_c = local_threshold_fraction(d_c_mm * 1e-3)
        results["percolation"]["local_cell_scale"]["d_c %.2f mm" % d_c_mm] = {
            "critical_damaged_fraction": float("%.3g" % f_c),
            "reachable": f_c <= 1.0,
            "note": "above one damaged cell per cell is impossible" if f_c > 1.0 else "",
        }

    grid = [1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4]
    for f in grid:
        p_closed, p_open, n_q = connected_leak_probability(f)
        results["percolation"]["connected_airspace"]["f %.0e" % f] = {
            "expected_qualifying_breaches_per_wrap": float("%.3g" % n_q),
            "leak_probability_stomata_closed": round(p_closed, 4),
            "leak_probability_stomata_open": round(p_open, 4),
        }
    # damaged fraction at 50 percent leak, by bisection on the closed-stomata and open-stomata cases
    def bisect(fun):
        lo, hi = 1e-12, 1e-2
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            if fun(mid) < 0.5:
                lo = mid
            else:
                hi = mid
        return hi
    f50_closed = bisect(lambda f: connected_leak_probability(f)[0])
    f50_open = bisect(lambda f: connected_leak_probability(f)[1])
    results["percolation"]["connected_airspace"]["f_50_percent_stomata_closed"] = float("%.3g" % f50_closed)
    results["percolation"]["connected_airspace"]["f_50_percent_stomata_open"] = float("%.3g" % f50_open)
    results["percolation"]["connected_airspace"]["stomata_per_wrap_if_open"] = round(STOMATA_PER_M2 * WRAP_AREA)

    for name, (K, D, basis) in POLYMERS.items():
        frac = scalping_fraction(K, D)
        results["taste"][name] = {
            "aroma_uptake_fraction_2h": float("%.3g" % frac),
            "uptake_fraction_if_D_tenfold": float("%.3g" % scalping_fraction(K, D, 10.0)),
            "basis": basis,
            "decision": "avoid" if frac >= 0.05 else "acceptable on physics",
        }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    print("Local (cell-scale) critical damaged fraction:")
    for k, v in results["percolation"]["local_cell_scale"].items():
        print("  %s: %s reachable=%s" % (k, v["critical_damaged_fraction"], v["reachable"]))
    print("Connected airspace network (both epidermal surfaces must connect):")
    for k, v in results["percolation"]["connected_airspace"].items():
        if isinstance(v, dict):
            print("  %s: N_q=%s  P_closed=%s  P_open=%s" % (k, v["expected_qualifying_breaches_per_wrap"],
                  v["leak_probability_stomata_closed"], v["leak_probability_stomata_open"]))
    ca = results["percolation"]["connected_airspace"]
    print("  f at 50 percent leak: closed stomata %s, open stomata %s; open stomata per wrap %s" % (
        ca["f_50_percent_stomata_closed"], ca["f_50_percent_stomata_open"], ca["stomata_per_wrap_if_open"]))
    print("Taste (aroma uptake fraction in 2 h):")
    for name, v in results["taste"].items():
        print("  %-20s %s (tenfold D: %s) -> %s" % (name, v["aroma_uptake_fraction_2h"],
                                                  v["uptake_fraction_if_D_tenfold"], v["decision"]))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
