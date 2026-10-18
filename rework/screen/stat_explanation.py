"""Statistical explanation of the conversion lead (men 25-34 against men 35-44 and 45-59).

Per-person potency for a band b is  P_b = d_b * s0 * OR^(mid_b - 40)  where
  d_b   = current drinking share 2024 (NSO), sex-specific cell,
  s0    = daily sugar-sweetened share at age 40 (2021 survey, 25-59 pooled),
  OR    = odds ratio per year of age for daily consumption (2021 survey),
  mid_b = mid-age of the band.

Ratios (both bands in the same sex):
  A = P(25-34) / P(35-44) = (d25/d35) * OR^(-10)         (drink cell is shared: d25 = d35)
  B = P(25-34) / P(45-59) = (d25/d45) * OR^(-22.5)

Uncertainty (assumptions, stated):
  OR     ~ log-normal from the published 95% interval 0.991 to 1.001 (sampling error only)
  d_b    ~ uniform, published value +/- 3 points (no 2024 interval published)
  s0     ~ uniform 15.5 to 16.2 percent (published 2021 interval)

Outputs: probabilities that each ratio exceeds 1, the log-ratio decomposition, and Sobol
total-order indices for ratio B. Writes segment_stat_results.json and a PNG chart.
"""
import json
import math
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_JSON = os.path.join(HERE, "segment_stat_results.json")
OUT_PNG = os.path.join(REPO, "rework", "charts", "conversion_statistics.png")

SEED = 20261019
N = 200000
rng = np.random.default_rng(SEED)

OR_LO, OR_HI = 0.991, 1.001
OR_MID = 0.996
LOG_OR_MEAN = math.log(OR_MID)
LOG_OR_SD = (math.log(OR_HI) - math.log(OR_LO)) / (2 * 1.96)

D25 = 68.6   # men 25-44 cell (applies to 25-34 and 35-44)
D35 = 68.6
D45 = 65.4   # men 45-59
DRINK_PM = 3.0
S0_LO, S0_HI = 15.5, 16.2
MID = {"25-34": 29.5, "35-44": 39.5, "45-59": 52.0}


def draws():
    or_ = np.exp(rng.normal(LOG_OR_MEAN, LOG_OR_SD, N))
    d25 = rng.uniform(D25 - DRINK_PM, D25 + DRINK_PM, N)
    d45 = rng.uniform(D45 - DRINK_PM, D45 + DRINK_PM, N)
    s0 = rng.uniform(S0_LO, S0_HI, N) / 100.0
    return or_, d25, d45, s0


def ratio_a(or_, d25):
    # drink cell shared between 25-34 and 35-44, so it cancels
    return or_ ** (MID["25-34"] - MID["35-44"])


def ratio_b(or_, d25, d45):
    return (d25 / d45) * or_ ** (MID["25-34"] - MID["45-59"])


def sobol_total(f, inputs, n_base=4096):
    """Saltelli total-order indices for a function of k independent inputs.
    inputs: list of (sampler, name) where sampler(size) draws one input."""
    k = len(inputs)
    A = np.column_stack([s(n_base) for s, _ in inputs])
    B = np.column_stack([s(n_base) for s, _ in inputs])
    fA = f(*[A[:, i] for i in range(k)])
    fB = f(*[B[:, i] for i in range(k)])
    var = np.var(np.concatenate([fA, fB]))
    out = {}
    for i, (_, name) in enumerate(inputs):
        ABi = A.copy()
        ABi[:, i] = B[:, i]
        fABi = f(*[ABi[:, j] for j in range(k)])
        st = 0.5 * np.mean((fA - fABi) ** 2) / var
        out[name] = float(st)
    return out


def main():
    or_, d25, d45, s0 = draws()
    ra = ratio_a(or_, d25)
    rb = ratio_b(or_, d25, d45)

    p_a = float(np.mean(ra > 1.0))
    p_b = float(np.mean(rb > 1.0))

    # Log-ratio decomposition at central values (drink cells and s0 at published central values).
    lr_drink = math.log(D25 / D45)
    lr_or = (MID["25-34"] - MID["45-59"]) * math.log(OR_MID)
    lr_total = lr_drink + lr_or

    # Sobol total-order indices for ratio B (log scale), inputs: OR, d25, d45, s0.
    def f_logb(o, a, b, s):
        return np.log((a / b) * o ** (MID["25-34"] - MID["45-59"]))

    sampler_or = lambda n: np.exp(rng.normal(LOG_OR_MEAN, LOG_OR_SD, n))
    sampler_d25 = lambda n: rng.uniform(D25 - DRINK_PM, D25 + DRINK_PM, n)
    sampler_d45 = lambda n: rng.uniform(D45 - DRINK_PM, D45 + DRINK_PM, n)
    sampler_s0 = lambda n: rng.uniform(S0_LO, S0_HI, n) / 100.0
    sobol = sobol_total(f_logb, [(sampler_or, "OR per year"), (sampler_d25, "drinking 25-34"),
                                 (sampler_d45, "drinking 45-59"), (sampler_s0, "sugar base s0")])

    # Sensitivity of ratio A: only OR matters (drink cell shared, s0 cancels).
    sobol_a = {"OR per year": 1.0, "drinking cell (shared)": 0.0, "sugar base s0": 0.0}

    result = {
        "seed": SEED,
        "draws": N,
        "P_ratio_A_25_34_over_35_44_gt_1": p_a,
        "P_ratio_B_25_34_over_45_59_gt_1": p_b,
        "ratio_A_median": float(np.median(ra)),
        "ratio_A_p05": float(np.percentile(ra, 5)),
        "ratio_A_p95": float(np.percentile(ra, 95)),
        "ratio_B_median": float(np.median(rb)),
        "ratio_B_p05": float(np.percentile(rb, 5)),
        "ratio_B_p95": float(np.percentile(rb, 95)),
        "log_ratio_B_decomposition_central": {
            "drinking_cells": lr_drink,
            "age_gradient": lr_or,
            "total": lr_total,
            "share_drinking_pct": 100.0 * lr_drink / lr_total,
            "share_age_gradient_pct": 100.0 * lr_or / lr_total,
        },
        "sobol_total_order_ratio_B_log": sobol,
        "sobol_ratio_A": sobol_a,
        "or_interval_published": [OR_LO, OR_HI],
        "or_log_sd_derived": LOG_OR_SD,
        "assumptions": [
            "OR log-normal from the published 95% interval (sampling error only).",
            "Drinking shares uniform published value +/- 3 points (no 2024 interval published).",
            "Sugar base s0 uniform 15.5 to 16.2 (published 2021 interval).",
            "Age gradient applied to mid-ages 29.5, 39.5 and 52.0.",
        ],
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.0))

    ax = axes[0]
    bins = np.linspace(0.85, 1.35, 120)
    ax.hist(ra, bins=bins, alpha=0.6, color="#A7C6E5", label=f"A: 25-34 vs 35-44  (P>1 = {p_a:.2f})", density=True)
    ax.hist(rb, bins=bins, alpha=0.6, color="#185FA5", label=f"B: 25-34 vs 45-59  (P>1 = {p_b:.2f})", density=True)
    ax.axvline(1.0, color="black", lw=1)
    ax.set_xlabel("Per-person potency ratio (25-34 over comparator)")
    ax.set_ylabel("Density")
    ax.set_title("A. Is men 25-34 ahead per person?")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(alpha=0.3)

    ax = axes[1]
    names = list(sobol.keys())
    vals = [sobol[n] for n in names]
    yy = np.arange(len(names))[::-1]
    ax.barh(yy, vals, color="#185FA5")
    ax.set_yticks(yy)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("Total-order sensitivity index (log ratio B)")
    ax.set_title("B. What drives 25-34 vs 45-59")
    ax.set_xlim(0, 1)
    ax.grid(axis="x", alpha=0.3)

    ax = axes[2]
    parts = [("drinking cells", lr_drink), ("age gradient (OR)", lr_or)]
    ax.bar([p[0] for p in parts], [p[1] for p in parts], color=["#2E7D5B", "#B5462E"])
    ax.axhline(0, color="black", lw=0.8)
    ax.set_ylabel("Contribution to log ratio")
    ax.set_title(f"C. Decomposition of B (total {lr_total:.3f})")
    ax.grid(axis="y", alpha=0.3)

    fig.suptitle("Conversion lead: how robust is men 25-34 per person? (200,000 draws)", fontsize=12, y=1.02)
    fig.text(0.01, -0.03, "Sources: NSO Smoking and Drinking survey 2024 (drinking by sex and age); 2021 Health Behaviour survey (daily sugar-sweetened share, odds ratio per year). Drinking +/-3 points and sugar base are assumptions where no interval is published.", fontsize=8, color="#444")
    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=160, bbox_inches="tight")

    print("wrote", OUT_JSON)
    print("wrote", OUT_PNG)
    print(f"P(A > 1) = {p_a:.3f}   median A = {np.median(ra):.3f} [{np.percentile(ra,5):.3f}, {np.percentile(ra,95):.3f}]")
    print(f"P(B > 1) = {p_b:.3f}   median B = {np.median(rb):.3f} [{np.percentile(rb,5):.3f}, {np.percentile(rb,95):.3f}]")
    print("B log decomposition: drinking", round(lr_drink, 4), " age gradient", round(lr_or, 4), " total", round(lr_total, 4))
    print("Sobol total-order (log B):", {k: round(v, 3) for k, v in sobol.items()})


if __name__ == "__main__":
    main()
