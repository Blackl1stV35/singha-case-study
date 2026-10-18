#!/usr/bin/env python3
"""Desk dose screen for finalist B: a labelled isoflavone total per 250 ml serving.

Python standard library only. Run with:
    python soy_isoflavone_dose_screen.py
Output: soy_isoflavone_dose_screen_results.json in the same folder, plus a short table on stdout.

Model
- Base soy isoflavones per 250 ml: uniform on [25.5, 63.5] mg.
  Source: Hirattanapun E, Teekachunhatean S. J Health Sci Med Res 2018;36(2):117-26,
  DOI 10.31584/jhsmr.2018.36.2.5. Four Thai soy-milk brands, two flavours each, Chiang Mai.
  The range is reported; the distribution is not. ASSUMPTION: uniform.
- Added standardised extract: nominal dose A mg per serving (input).
- Certificate-of-analysis tolerance on A: +/-10 percent, uniform, independent per serving.
  ASSUMPTION. Not sourced.
- Total per serving S = base + A * U(0.9, 1.1).
- A serving is inside the window for label T if 0.85 T <= S <= 1.15 T (window from the brief).
- The exact probability uses the closed form for the sum of two independent uniforms.
  A seeded Monte Carlo run cross-checks it.

Sourcing solve
- Base is centred on the 2018 midpoint m0 = 44.5 mg with full width w, uniform on
  [m0 - w/2, m0 + w/2]. The nominal label is T = m0 + A. ASSUMPTION.
- The solve returns the largest w that keeps the in-window share at or above TARGET_SHARE.
  ASSUMPTION: TARGET_SHARE = 0.90. This is the base spread a lot-testing or standardisation
  plan has to hold.
"""

import argparse
import json
import random
from pathlib import Path

# ---- sourced inputs -------------------------------------------------------
BASE_LOW_MG = 25.5
BASE_HIGH_MG = 63.5
SERVING_ML = 250
SOURCE_2018 = (
    "Hirattanapun E, Teekachunhatean S. Variability of Isoflavone Content in Soy Milk Products "
    "Commercially Available in Thailand. J Health Sci Med Res. 2018;36(2):117-26. "
    "DOI 10.31584/jhsmr.2018.36.2.5. https://he01.tci-thaijo.org/index.php/jhsmr/article/view/125491"
)

# ---- assumptions and brief parameters -------------------------------------
COA_TOL = 0.10          # ASSUMPTION: certificate-of-analysis tolerance on added extract (+/-10 percent)
WINDOW = 0.15           # brief: share of servings within +/-15 percent of the label
TARGET_SHARE = 0.90     # ASSUMPTION: used only in the sourcing solve
ADDED_MG_DEFAULT = [10.0, 20.0, 30.0, 40.0, 50.0]
LABELS_DEFAULT = [40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
MC_N_DEFAULT = 200000
SEED = 20261018

ASSUMPTIONS = [
    "Base soy isoflavones per 250 ml are uniform on 25.5 to 63.5 mg. ASSUMPTION: the 2018 study "
    "reports the range of eight products, not a distribution.",
    "The 2018 products were two flavours per brand. Whether a plain, unsweetened UHT product "
    "falls inside the range is unverified.",
    "Certificate-of-analysis tolerance on the added extract is +/-10 percent, uniform, and "
    "independent per serving. ASSUMPTION: not sourced.",
    "Base soy and added extract are independent. ASSUMPTION.",
    "The in-window test is 0.85 T to 1.15 T, where T is the labelled total per serving (brief).",
    "For the sourcing solve, the nominal label is the 2018 base midpoint (44.5 mg) plus the added "
    "dose. ASSUMPTION.",
    "The sourcing solve uses TARGET_SHARE = 0.90. ASSUMPTION.",
    "The extract's labelled content is accurate to its certificate of analysis. No supplier was "
    "verified. ASSUMPTION.",
    "No lot-to-lot shift in base content beyond the 2018 range. ASSUMPTION.",
]


def _ramp(u, c, d):
    """Integral over y in [c, d] of max(u - y, 0). Used for the sum-of-uniforms CDF."""
    if u <= c:
        return 0.0
    if u <= d:
        return (u - c) ** 2 / 2.0
    return (d - c) * (u - (c + d) / 2.0)


def cdf_sum(s, a, b, c, d):
    """Exact P(X + Y <= s) with X ~ U(a, b) and Y ~ U(c, d). If c == d, Y is constant."""
    if d - c <= 1e-12:
        return min(max((s - c - a) / (b - a), 0.0), 1.0)
    return (_ramp(s - a, c, d) - _ramp(s - b, c, d)) / ((b - a) * (d - c))


def share_exact(T, a, b, A, tol, window):
    """Exact share of servings with 0.85 T <= base + A*U(1-tol, 1+tol) <= 1.15 T."""
    lo = (1.0 - window) * T
    hi = (1.0 + window) * T
    c = A * (1.0 - tol)
    d = A * (1.0 + tol)
    return cdf_sum(hi, a, b, c, d) - cdf_sum(lo, a, b, c, d)


def share_mc(T, a, b, A, tol, window, n, seed):
    """Seeded Monte Carlo estimate of the same share."""
    rng = random.Random(seed)
    lo = (1.0 - window) * T
    hi = (1.0 + window) * T
    hits = 0
    for _ in range(n):
        s = rng.uniform(a, b) + A * rng.uniform(1.0 - tol, 1.0 + tol)
        if lo <= s <= hi:
            hits += 1
    return hits / n


def max_base_width(A, tol, window, target):
    """Largest full base width (mg) around the 2018 midpoint that keeps the share >= target.

    The nominal label is m0 + A. Share falls as the base widens, so bisection applies.
    """
    m0 = (BASE_LOW_MG + BASE_HIGH_MG) / 2.0
    full = BASE_HIGH_MG - BASE_LOW_MG
    T = m0 + A

    def share(w):
        return share_exact(T, m0 - w / 2.0, m0 + w / 2.0, A, tol, window)

    if share(full) >= target:
        return full
    lo, hi = 0.0, full
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if share(mid) >= target:
            lo = mid
        else:
            hi = mid
    return lo


def min_added_for_all_servings(a, b, tol, window):
    """Smallest added dose A (mg) for which every serving can sit inside one fixed window.

    Solves (b + A(1+tol))(1-window) <= (a + A(1-tol))(1+window) for A.
    """
    num = b * (1.0 - window) - a * (1.0 + window)
    den = (1.0 - tol) * (1.0 + window) - (1.0 + tol) * (1.0 - window)
    if den <= 0:
        return None
    return num / den


def floor_options(floors, a, b, tol):
    """For a 'at least F mg' floor label: smallest added dose A that keeps every serving >= F
    (worst case base = a, extract at 1 - tol), and the resulting upper end of the serving range."""
    out = []
    for F in floors:
        A = max((F - a) / (1.0 - tol), 0.0)
        out.append(
            {
                "floor_label_mg": F,
                "min_added_extract_mg": round(A, 4),
                "serving_range_mg_at_that_dose": [
                    round(a + A * (1.0 - tol), 4),
                    round(b + A * (1.0 + tol), 4),
                ],
            }
        )
    return out


def main():
    ap = argparse.ArgumentParser(description="Isoflavone labelled-dose desk screen (stdlib only).")
    ap.add_argument("--added-mg", type=float, nargs="+", default=ADDED_MG_DEFAULT)
    ap.add_argument("--labels", type=float, nargs="+", default=LABELS_DEFAULT)
    ap.add_argument("--mc-n", type=int, default=MC_N_DEFAULT)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("soy_isoflavone_dose_screen_results.json"),
    )
    args = ap.parse_args()

    a, b = BASE_LOW_MG, BASE_HIGH_MG
    m0 = (a + b) / 2.0

    # sanity checks: CDF limits and a mid-range value
    sanity = {
        "cdf_at_minus_inf_ok": abs(cdf_sum(a - 1000.0, a, b, 0.0, 10.0)) < 1e-9,
        "cdf_at_plus_inf_ok": abs(cdf_sum(b + 1000.0, a, b, 0.0, 10.0) - 1.0) < 1e-9,
        "exact_share_T80_A30": round(share_exact(80.0, a, b, 30.0, COA_TOL, WINDOW), 6),
        "mc_share_T80_A30": round(share_mc(80.0, a, b, 30.0, COA_TOL, WINDOW, args.mc_n, args.seed), 6),
    }

    grid = []
    for A in args.added_mg:
        for T in args.labels:
            exact = share_exact(T, a, b, A, COA_TOL, WINDOW)
            mc = share_mc(T, a, b, A, COA_TOL, WINDOW, args.mc_n, args.seed)
            grid.append(
                {
                    "added_extract_mg": A,
                    "labelled_total_mg": T,
                    "window_mg": [round((1 - WINDOW) * T, 4), round((1 + WINDOW) * T, 4)],
                    "share_within_15pct_exact": round(exact, 4),
                    "share_within_15pct_monte_carlo": round(mc, 4),
                    "mc_minus_exact": round(mc - exact, 4),
                }
            )

    solve = []
    for A in args.added_mg:
        nominal = m0 + A
        w = max_base_width(A, COA_TOL, WINDOW, TARGET_SHARE)
        share_full = share_exact(nominal, a, b, A, COA_TOL, WINDOW)
        solve.append(
            {
                "added_extract_mg": A,
                "nominal_label_mg": round(nominal, 4),
                "share_at_nominal_with_full_2018_range": round(share_full, 4),
                "target_share": TARGET_SHARE,
                "max_base_full_width_mg": round(w, 4),
                "max_base_half_width_mg": round(w / 2.0, 4),
                "max_base_half_width_pct_of_base_mid": round((w / 2.0) / m0 * 100.0, 2),
            }
        )

    a_all = min_added_for_all_servings(a, b, COA_TOL, WINDOW)

    result = {
        "script": "rework/screen/soy_isoflavone_dose_screen.py",
        "stdlib_only": True,
        "run_date": "2026-10-18",
        "seed": args.seed,
        "mc_n": args.mc_n,
        "source_inputs": {
            "base_low_mg_per_250ml": BASE_LOW_MG,
            "base_high_mg_per_250ml": BASE_HIGH_MG,
            "serving_ml": SERVING_ML,
            "source": SOURCE_2018,
            "status": "Range read from the journal article page abstract (2026-10-18). Full PDF not read.",
        },
        "parameters": {
            "coa_tolerance_on_added_extract": COA_TOL,
            "in_window_fraction_of_label": WINDOW,
            "target_share_for_solve": TARGET_SHARE,
            "added_mg_grid": args.added_mg,
            "labelled_totals_mg": args.labels,
        },
        "assumptions": ASSUMPTIONS,
        "sanity_checks": sanity,
        "grid_share_within_window": grid,
        "sourcing_solve_base_spread": solve,
        "min_added_mg_for_every_serving_inside_one_window": round(a_all, 4) if a_all else None,
        "floor_label_options_2018_range": floor_options([40.0, 50.0, 60.0], a, b, COA_TOL),
        "cross_check_mahidol_table_not_used_in_screen": {
            "table_value": 9.65,
            "unit": "UNVERIFIED. The PDF table header (mg per 100 g or per 100 ml) could not be decoded.",
            "scaled_to_250_ml_mg": round(9.65 * 2.5, 4),
            "note": "Arithmetic only. The result sits just under the 2018 lower bound of 25.5 mg.",
            "source": "https://pharmacy.mahidol.ac.th/knowledge/files/0002.pdf (undated; PDF metadata 2010-02-03)",
        },
    }

    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    # short stdout summary (ASCII only)
    print("Sanity:", sanity)
    print("")
    print(f"{'add_mg':>7} {'label_mg':>9} {'exact':>8} {'MC':>8} {'MC-exact':>9}")
    for row in grid:
        print(
            f"{row['added_extract_mg']:>7.1f} {row['labelled_total_mg']:>9.1f} "
            f"{row['share_within_15pct_exact']:>8.4f} {row['share_within_15pct_monte_carlo']:>8.4f} "
            f"{row['mc_minus_exact']:>9.4f}"
        )
    print("")
    print("Sourcing solve (target share {:.2f}):".format(TARGET_SHARE))
    for row in solve:
        print(
            f"  add {row['added_extract_mg']:>5.1f} mg  nominal label {row['nominal_label_mg']:>6.2f} mg  "
            f"share at full 2018 range {row['share_at_nominal_with_full_2018_range']:.4f}  "
            f"max base full width {row['max_base_full_width_mg']:.2f} mg "
            f"(+/-{row['max_base_half_width_pct_of_base_mid']:.1f} percent of base midpoint)"
        )
    print("")
    print("Added extract needed for every serving inside one fixed window: {:.2f} mg".format(a_all))
    print("Wrote", args.out)


if __name__ == "__main__":
    main()
