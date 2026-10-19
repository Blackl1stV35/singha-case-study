"""Cost per 330 ml can, and production scenarios, from the sourced inputs in rework/58.

Desk model for a student competition. It is not Singha's cost: no Singha or Boon Rawd can cost was
found. Every input carries a tier (P primary, S secondary) and a status (SOURCED, PROXY, ASSUMPTION).
Items the checker found missing are shown as sensitivities, not filled with invented values.
Run: python can_cost_model.py  (writes can_cost_model_results.json and ../charts/can_cost_per_unit.png)
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "can_cost_model_results.json"
OUT_PNG = HERE.parent / "charts" / "can_cost_per_unit.png"

CAN_L = 0.33  # litres per can

# ---- Inputs: (low, high), tier, status, source note -------------------------------------------
FX = (33.32, 33.44)                 # THB per USD, XE mid-market 18 Oct 2026 (S); low is a 16 Sep reading
LME = (2998.5, 3008.5)              # USD per tonne, LME cash bid (S, news report); high is a CFD (S)
SHEET_G = (14.4, 18.5)              # g of aluminium sheet per can (ASSUMPTION, from the can mass row)
CONV_NONMETAL = (0.04, 0.08)        # USD per can, non-metal conversion (PROXY, US 2024, S); corrected range
FILL_CONSUM = (0.001, 0.004)        # USD per can, filling consumables (ASSUMPTION)
SEAM = (0.0001, 0.0005)             # USD per can, seaming (ASSUMPTION)
CO2 = (0.0003, 0.0018)              # USD per can, carbonation (PROXY, S); high excludes 50% purge loss
LIQUID = (0.027, 0.040)             # USD per can, sugar and flavour (ASSUMPTION, built on a sugar PROXY, S)

# Production (group level; PROXY unless noted)
NAMEPLATE_ML = 1000.0               # million litres per year, group nameplate (PROXY; scope unclear, 2018 citation)
CANNED_SHARE = 0.553                # canned share of output (PROXY, a Vietnamese peer, S)
UTIL = (0.584, 0.633)               # capacity utilisation (PROXY, Thai industry and a beer plant, S)
FIXED_THB_M = (0.0, 300.0, 600.0)   # annual fixed cost, THB million (ASSUMPTION scenarios, not sourced)

# Sensitivities for items the checker found missing (scenarios only, labelled ASSUMPTION)
PREMIUM_USD_T = (0.0, 100.0, 200.0)  # regional premium scenarios, USD per tonne


def metal_usd(sheet_g, lme_usd_t, premium_usd_t=0.0):
    """Sheet metal cost per can: grams x (USD per tonne) / 1e6 gives USD."""
    return sheet_g * (lme_usd_t + premium_usd_t) / 1e6


def variable_usd(case, premium_usd_t=0.0):
    """Variable cost per can in USD. Low case pairs the low inputs, high case pairs the high inputs."""
    i = 0 if case == "low" else 1
    metal = metal_usd(SHEET_G[i], LME[i], premium_usd_t)
    items = {
        "sheet_metal": metal,
        "conversion_nonmetal": CONV_NONMETAL[i],
        "filling_consumables": FILL_CONSUM[i],
        "seaming": SEAM[i],
        "co2": CO2[i],
        "liquid_sugar_flavour": LIQUID[i],
    }
    return sum(items.values()), items


def cans_per_year(util):
    """Cans per year at nameplate times canned share times utilisation."""
    litres = NAMEPLATE_ML * 1e6 * CANNED_SHARE * util  # million litres to litres
    return litres / CAN_L


def main():
    res = {"basis": "Desk estimate. No Singha or Boon Rawd can cost found. Tiers: P primary, S secondary.",
           "excluded_or_missing": [
               "aluminium regional premium and sheet rolling (no input; see premium scenarios)",
               "scrap credit (no scrap price; not netted, so cost is overstated by the credit)",
               "end and tab conversion; lacquer-curing gas; secondary packaging (carton, shrink, pallet)",
               "excise on sugar-sweetened drinks (Thai sugar levy; primary law not read)",
               "freight, distribution, marketing, overheads, depreciation, line capex",
               "lacquer and ink, labour and electricity: sub-components of conversion, not added"],
           "inputs": {"fx_thb_per_usd": FX, "lme_usd_per_t": LME, "sheet_g_per_can": SHEET_G,
                      "conversion_nonmetal_usd": CONV_NONMETAL, "filling_usd": FILL_CONSUM,
                      "seaming_usd": SEAM, "co2_usd": CO2, "liquid_usd": LIQUID,
                      "nameplate_ML": NAMEPLATE_ML, "canned_share": CANNED_SHARE, "utilisation": UTIL,
                      "fixed_thb_m_scenarios": FIXED_THB_M}}

    # Variable cost per can, base case (no premium), in USD and THB
    var = {}
    for case in ("low", "high"):
        usd, items = variable_usd(case)
        i = 0 if case == "low" else 1
        var[case] = {"usd": round(usd, 5), "thb": round(usd * FX[i], 3),
                     "items_usd": {k: round(v, 5) for k, v in items.items()}}
    res["variable_cost_per_can"] = var

    # Premium sensitivity (scenario): mid case at mid inputs
    mid_fx = sum(FX) / 2
    res["premium_sensitivity_thb_per_can"] = {
        str(p): round(metal_usd((SHEET_G[0] + SHEET_G[1]) / 2, sum(LME) / 2, p) * mid_fx, 3)
        for p in PREMIUM_USD_T}

    # Production: cans per year at each utilisation; fixed-cost dilution per can
    volumes = {"at_util_low": cans_per_year(UTIL[0]), "at_util_high": cans_per_year(UTIL[1]),
               "at_nameplate_100pct": cans_per_year(1.0)}
    res["cans_per_year"] = {k: round(v) for k, v in volumes.items()}

    # Cost per can = variable + fixed / cans. Grid over volume and fixed cost, mid variable cost.
    v_mid_thb = (var["low"]["thb"] + var["high"]["thb"]) / 2
    grid_volumes = [5e8, 1e9, round(volumes["at_nameplate_100pct"])]
    grid = []
    for q in grid_volumes:
        row = {"cans_per_year": round(q)}
        for f in FIXED_THB_M:
            row[f"fixed_{int(f)}m_thb_per_can"] = round(v_mid_thb + f * 1e6 / q, 3)
        grid.append(row)
    res["cost_per_can_grid_thb"] = {"variable_mid_thb": round(v_mid_thb, 3), "rows": grid}

    # Chart
    qs = [q / 1e9 for q in [i * 1e8 for i in range(3, 18)]]
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=150)
    ax.fill_between(qs, [var["low"]["thb"]] * len(qs), [var["high"]["thb"]] * len(qs), color="#A8CF3A",
                    alpha=0.35, label="variable cost, low to high (THB per can)")
    for f, style in zip(FIXED_THB_M, ["-", "--", ":"]):
        ax.plot(qs, [var["low"]["thb"] + 0 * q + f * 1e6 / (q * 1e9) for q in qs], style, color="#17191C",
                label="fixed THB %d m/yr (low variable)" % f)
    ax.set_xlabel("cans per year (billion)")
    ax.set_ylabel("THB per can")
    ax.set_title("Cost per 330 ml can: variable cost and fixed-cost dilution (desk estimate)")
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, metadata={"Software": None})
    OUT_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"variable_thb": {k: v["thb"] for k, v in var.items()},
                      "cans_per_year": res["cans_per_year"],
                      "premium_thb": res["premium_sensitivity_thb_per_can"]}, indent=1))


if __name__ == "__main__":
    main()
