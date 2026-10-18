"""Monte Carlo potency index for Thailand age-band segments.

Index_b = Pop_b x P_sugar_b x P_alc_b x Fit x Reach_b

- Pop_b: DOPA Nov 2568 Thai-national counts, 5-year bands regrouped (sourced; +/-0.96 % gap range).
- P_sugar_b: daily sweet-drink share 15.8 % (15.5 to 16.2) at mean age 40 (25 to 59 pooled, NHES-type
  survey, 2021 fieldwork), adjusted by the per-year odds ratio 0.996 (0.991 to 1.001). Extrapolated outside
  25 to 59 for 15 to 24 and 60 and over; flagged as an assumption.
- P_alc_b: current drinking share 2024 (NSO Social Indicators 2025), used as the alcohol-occasion proxy.
  The 15 to 24 cell is a population-weighted mix of 15 to 19 and 20 to 24. The 25 to 34 and 35 to 44 bands
  share one published cell (25 to 44). Range +/-3 points (assumption; no interval published for 2024).
- Fit: cube-fit weight, uniform 0.6 to 1.0 (assumption; the largest unevidenced input).
- Reach_b: internet use share by band (NSO ICT 2569 Q2) mixed with channel share r (uniform 0.1 to 0.5,
  assumption): reach = (1 - r) + r x internet share.

Run: python segment_potency_mc.py  -> writes segment_potency_mc_results.json and the chart.
"""
import json
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_JSON = os.path.join(HERE, "segment_potency_mc_results.json")
OUT_PNG = os.path.join(REPO, "rework", "charts", "segment_potency_quant.png")

SEED = 20261018
N = 20000
rng = np.random.default_rng(SEED)

BANDS = ["15-24", "25-34", "35-44", "45-59", "60+"]

# DOPA Nov 2568, Thai nationals (low, central, high), persons.
POP = {
    "15-24": (7899061, 7975628, 8052194),   # 16-20 plus 21-25 bands
    "25-34": (9294114, 9384203, 9474291),   # 26-30 plus 31-35
    "35-44": (9317170, 9407482, 9497794),   # 36-40 plus 41-45
    "45-59": (14761466, 14904550, 15047634),  # 46-50, 51-55, 56-60
    "60+": (13964776, 14100138, 14235499),  # 61 and over plus one-fifth of 56-60
}
# Approximate mid-age for the sugar age gradient.
MID_AGE = {"15-24": 20.0, "25-34": 29.5, "35-44": 39.5, "45-59": 52.0, "60+": 68.0}

# Daily SSB share, 25-59 pooled, and its age odds ratio per year.
SSB_DAILY = (15.5, 15.8, 16.2)
SSB_MEAN_AGE = 40.0
OR_PER_YEAR = (0.991, 0.996, 1.001)

# Current drinking 2024 (NSO), percent of age group. 15-24 is built from 15-19 and 20-24.
DRINK_15_19 = 9.6
DRINK_20_24 = 37.8
DRINK_25_44 = 46.9
DRINK_45_59 = 41.9
DRINK_60P = 18.3
DRINK_RANGE_PTS = 3.0  # assumption: no published interval for 2024

# Internet use share by band, NSO ICT 2569 Q2 (percent), (low, central, high).
ICT = {
    "15-24": (98.9, 99.25, 99.6),
    "25-34": (99.0, 99.05, 99.2),
    "35-44": (98.2, 98.45, 98.7),
    "45-59": (96.1, 97.15, 98.2),
    "60+": (72.3, 74.8, 74.8),
}


def tri_or_uniform(lo, hi, size):
    return rng.uniform(lo, hi, size)


def drink_15_24_central():
    w_young = POP["15-24"][1] * 0  # placeholder for clarity
    # population weights: 16-20 and 21-25 bands
    w1, w2 = 3956268.0, 4019360.0
    return (DRINK_15_19 * w1 + DRINK_20_24 * w2) / (w1 + w2)


DRINK_15_24 = drink_15_24_central()
DRINK = {"15-24": DRINK_15_24, "25-34": DRINK_25_44, "35-44": DRINK_25_44, "45-59": DRINK_45_59, "60+": DRINK_60P}


def draw_inputs():
    inputs = {}
    for b in BANDS:
        lo, c, hi = POP[b]
        inputs[f"pop_{b}"] = tri_or_uniform(lo, hi, N)
    ssb = tri_or_uniform(SSB_DAILY[0], SSB_DAILY[2], N) / 100.0
    orr = tri_or_uniform(OR_PER_YEAR[0], OR_PER_YEAR[2], N)
    fit = tri_or_uniform(0.6, 1.0, N)
    r = tri_or_uniform(0.1, 0.5, N)
    for b in BANDS:
        age_adj = orr ** (MID_AGE[b] - SSB_MEAN_AGE)
        inputs[f"sugar_{b}"] = np.clip(ssb * age_adj, 0.0, 1.0)
        inputs[f"alc_{b}"] = np.clip(tri_or_uniform(DRINK[b] - DRINK_RANGE_PTS, DRINK[b] + DRINK_RANGE_PTS, N) / 100.0, 0.0, 1.0)
        ict = tri_or_uniform(ICT[b][0], ICT[b][2], N) / 100.0
        inputs[f"reach_{b}"] = (1 - r) + r * ict
    inputs["fit"] = fit
    inputs["channel_online_share"] = r
    inputs["or_per_year"] = orr
    inputs["ssb_daily_share"] = ssb
    return inputs


def index_draws(inputs):
    idx = {}
    for b in BANDS:
        idx[b] = inputs[f"pop_{b}"] * inputs[f"sugar_{b}"] * inputs[f"alc_{b}"] * inputs["fit"] * inputs[f"reach_{b}"]
    return idx


def central_index():
    vals = {}
    for b in BANDS:
        pop = POP[b][1]
        sugar = SSB_DAILY[1] / 100.0 * (OR_PER_YEAR[1] ** (MID_AGE[b] - SSB_MEAN_AGE))
        alc = DRINK[b] / 100.0
        ict = ICT[b][1] / 100.0
        reach = (1 - 0.3) + 0.3 * ict
        vals[b] = pop * sugar * alc * 0.8 * reach
    return vals


def main():
    inputs = draw_inputs()
    idx = index_draws(inputs)
    stacked = np.vstack([idx[b] for b in BANDS])
    med = {b: float(np.median(idx[b])) for b in BANDS}
    p05 = {b: float(np.percentile(idx[b], 5)) for b in BANDS}
    p95 = {b: float(np.percentile(idx[b], 95)) for b in BANDS}
    ranks = np.argsort(-stacked, axis=0)
    p_rank1 = {BANDS[i]: float(np.mean(ranks[0] == i)) for i in range(len(BANDS))}
    p_top2 = {BANDS[i]: float(np.mean((ranks[0] == i) | (ranks[1] == i))) for i in range(len(BANDS))}

    scale = max(med.values())
    med_scaled = {b: 100.0 * med[b] / scale for b in BANDS}
    p05_scaled = {b: 100.0 * p05[b] / scale for b in BANDS}
    p95_scaled = {b: 100.0 * p95[b] / scale for b in BANDS}

    top = max(med, key=med.get)
    second = sorted(med, key=med.get, reverse=True)[1]
    # Ratio of top to runner-up cancels the common factors (fit weight, online channel share),
    # so the sensitivity shows what separates the two bands.
    ratio = idx[top] / idx[second]
    sens = {}
    for name in ("pop_" + top, "pop_" + second, "sugar_" + top, "sugar_" + second,
                 "alc_" + top, "alc_" + second, "reach_" + top, "reach_" + second, "or_per_year"):
        sens[name] = float(np.corrcoef(inputs[name], ratio)[0, 1])
    sens_sorted = dict(sorted(sens.items(), key=lambda kv: -abs(kv[1])))

    result = {
        "seed": SEED,
        "draws": N,
        "bands": BANDS,
        "median_index_scaled_to_top_100": med_scaled,
        "p05_scaled": p05_scaled,
        "p95_scaled": p95_scaled,
        "probability_rank_1": p_rank1,
        "probability_top_2": p_top2,
        "top_band_by_median": top,
        "second_band": second,
        "sensitivity_correlation_with_top_over_second_ratio": sens_sorted,
        "central_check_index_raw": central_index(),
        "assumptions": [
            "Fit weight uniform 0.6 to 1.0 (no evidence; largest unevidenced input).",
            "Online channel share uniform 0.1 to 0.5 (no evidence).",
            "Alcohol 2024 range +/-3 points (no published interval).",
            "Sugar age gradient extrapolated to 15-24 and 60+ from the 25-59 pooled survey.",
            "Alcohol-occasion proxy: current drinking share (not a measure of alcohol-alternative demand).",
            "Segments are independent across the three propensity inputs (no joint data).",
        ],
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.2), gridspec_kw={"width_ratios": [1.4, 1, 1.2]})

    ax = axes[0]
    y = np.arange(len(BANDS))[::-1]
    meds = [med_scaled[b] for b in BANDS]
    lo = [med_scaled[b] - p05_scaled[b] for b in BANDS]
    hi = [p95_scaled[b] - med_scaled[b] for b in BANDS]
    ax.errorbar(meds, y, xerr=[lo, hi], fmt="o", color="#185FA5", ecolor="#7FA9D1", capsize=5, markersize=8)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{b}" for b in BANDS])
    ax.set_xlabel("Potency index (top band median = 100)")
    ax.set_title("A. Potency by age band (median, 90% interval)")
    ax.grid(axis="x", alpha=0.3)

    ax = axes[1]
    probs = [p_rank1[b] * 100 for b in BANDS]
    ax.barh(y, probs, color=["#185FA5" if b == top else "#A7C6E5" for b in BANDS])
    ax.set_yticks(y)
    ax.set_yticklabels(BANDS)
    ax.set_xlabel("Share of draws ranked first (%)")
    ax.set_title("B. Probability of ranking first")
    ax.set_xlim(0, 100)
    for yi, p in zip(y, probs):
        ax.text(p + 1.5, yi, f"{p:.0f}%", va="center", fontsize=9)
    ax.grid(axis="x", alpha=0.3)

    ax = axes[2]
    names = list(sens_sorted.keys())[:6]
    vals = [sens_sorted[n] for n in names]
    labels = [n.replace("_", " ") for n in names]
    yy = np.arange(len(names))[::-1]
    ax.barh(yy, vals, color=["#B5462E" if v < 0 else "#2E7D5B" for v in vals])
    ax.set_yticks(yy)
    ax.set_yticklabels(labels, fontsize=9)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel(f"Correlation with the {top} / {second} ratio")
    ax.set_title(f"C. What separates {top} from {second}")
    ax.set_xlim(-1, 1)
    ax.grid(axis="x", alpha=0.3)

    fig.suptitle("Thailand age-band potency, sugar-sweetened drinking proxy (not the sugar-free candidate; 20,000 draws)", fontsize=12, y=1.02)
    fig.text(0.01, -0.04, "Sources: DOPA Nov 2568 population; NHES-type survey 2021 (daily SSB); NSO Social Indicators 2025 (current drinking 2024); NSO ICT 2569 Q2. Fit weight and channel share are assumptions.", fontsize=8, color="#444")
    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=160, bbox_inches="tight")
    print("wrote", OUT_JSON)
    print("wrote", OUT_PNG)
    print("top band:", top)
    print("median scaled:", {b: round(v, 1) for b, v in med_scaled.items()})
    print("P(rank 1):", {b: round(v, 3) for b, v in p_rank1.items()})


if __name__ == "__main__":
    main()
