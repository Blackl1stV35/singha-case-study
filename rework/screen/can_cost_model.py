"""Cost per 330 ml can, excluding aluminium, and production scenarios. Desk model for a student competition.

Updated 20 October 2026 (task T7, record rework/70_singha_internal_estimates.md).

- The non-aluminium inputs are taken from rework/screen/singha_internal_estimates.py (its INPUTS table), so there is
  one set of inputs in the repo.
- The LME aluminium reading used before (records 58, 61; this model's earlier LME input of USD 3,013 to 3,014 a tonne)
  is REMOVED. Its route is not authorised (record 69, section 7.4 item 3), and the live LME page returned HTTP 403 on
  20 October 2026. Aluminium is given here only as a slope (THB a can per USD 100 a tonne) and as the break-even
  price at which contribution is zero.
- The earlier mid-input result of THB 4.94 a can (range 3.73 to 6.14) included the LME reading. It is superseded and
  is kept in the results file only as a record of the earlier figure.
- Utilisation: the earlier 58.4 to 63.3 per cent PROXY range is replaced by Thai Beverage Can's printed utilisation for
  2024 and 2025 (58.57 and 59.46 per cent; P, BJC One Report 2025). It is a third-party figure, not the Boon Rawd group.

It is not Singha's cost: no Singha or Boon Rawd can cost was found.
Run: python can_cost_model.py            (writes can_cost_model_results.json)
     python can_cost_model.py --chart    (also writes can_cost_non_aluminium.png beside this file; optional)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from singha_internal_estimates import INPUTS as EST, PRICE_MODE, PRICE_SINGLE, net_price  # noqa: E402

OUT_JSON = HERE / "can_cost_model_results.json"
OUT_PNG = HERE / "can_cost_non_aluminium.png"
CAN_L = 0.33  # litres per can


def pair(name):
    """(low, high) from the shared INPUTS table, for a uniform input."""
    return (EST[name]["lo"], EST[name]["hi"])


# ---- Non-aluminium inputs (from singha_internal_estimates.py) ----------------------------------------------------
FX = pair("fx_thb_per_usd")                 # THB per USD (BOT 15 Oct 2026, P as saved)
SHEET_G = pair("sheet_g_per_can")           # g of aluminium sheet per can (ASSUMPTION bound; used for the slope only)
CONV_NONMETAL = pair("conversion_nonmetal_usd")  # USD per can (PROXY, US 2024, S)
FILL_CONSUM = pair("filling_usd")           # USD per can (ASSUMPTION bound)
SEAM = pair("seaming_usd")                  # USD per can (ASSUMPTION bound)
CO2 = pair("co2_usd")                       # USD per can (PROXY, S)
LIQUID = pair("liquid_usd")                 # USD per can (ASSUMPTION; built on a sugar proxy)

# Production (group level; PROXY unless noted)
NAMEPLATE_ML = EST["group_nameplate_ml"]["value"]   # million litres a year (PROXY; scope unclear)
CANNED_SHARE = EST["canned_share_proxy"]["value"]    # canned share of output (PROXY, a Vietnamese peer, S)
UTIL = (0.5857, 0.5946)                     # Thai Beverage Can utilisation 2024 and 2025 (P, third party)
FIXED_THB_M = (0.0, 300.0, 600.0)           # annual fixed cost, THB million (ASSUMPTION scenarios, not sourced)
PREMIUM_USD_T = (0.0, 100.0, 200.0)         # aluminium regional premium scenarios (ASSUMPTION, not sourced)


def nonmetal_usd(i):
    """Non-aluminium variable cost per can in USD; i = 0 for the low pairing, 1 for the high pairing."""
    items = {
        "conversion_nonmetal": CONV_NONMETAL[i],
        "filling_consumables": FILL_CONSUM[i],
        "seaming": SEAM[i],
        "co2": CO2[i],
        "liquid_sugar_flavour": LIQUID[i],
    }
    return sum(items.values()), items


def aluminium_thb_per_can(sheet_g, price_usd_t, fx):
    """Sheet metal cost per can in THB: grams times USD a tonne divided by 1e6 times the exchange rate."""
    return sheet_g * price_usd_t / 1e6 * fx


def cans_per_year(util):
    """Cans a year at group nameplate times canned share times utilisation."""
    litres = NAMEPLATE_ML * 1e6 * CANNED_SHARE * util
    return litres / CAN_L


def main():
    res = {
        "basis": "Desk estimate. No Singha or Boon Rawd can cost found. Tiers: P primary, S secondary, PROXY, ASSUMPTION.",
        "superseded": {
            "thb_per_can_mid": 4.94, "range": [3.73, 6.14],
            "note": "Earlier result including the LME reading (USD 3,013 to 3,014 a tonne), which is not authorised. Superseded by the "
                    "non-aluminium cost below and the aluminium slope. Do not quote."},
        "excluded_or_missing": [
            "aluminium price (LME route not authorised; slope and break-even only)",
            "aluminium regional premium and sheet rolling (scenarios only)",
            "scrap credit (not netted, so cost is overstated by the credit)",
            "end and tab conversion; lacquer-curing gas; secondary packaging (carton, shrink, pallet)",
            "excise on sugar-sweetened drinks (not read; record 69 section 6)",
            "freight, distribution, marketing, overheads, depreciation, line capex",
            "lacquer and ink, labour and electricity: sub-components of conversion, not added",
            "binder and flavour for the cube (not part of a can; not priced)"],
        "inputs_from_singha_internal_estimates": {
            "fx_thb_per_usd": FX, "sheet_g_per_can": SHEET_G, "conversion_nonmetal_usd": CONV_NONMETAL,
            "filling_usd": FILL_CONSUM, "seaming_usd": SEAM, "co2_usd": CO2, "liquid_usd": LIQUID,
            "nameplate_ML": NAMEPLATE_ML, "canned_share": CANNED_SHARE, "utilisation_tbc_2024_2025": UTIL,
            "fixed_thb_m_scenarios": FIXED_THB_M, "premium_usd_t_scenarios": PREMIUM_USD_T},
    }

    # ---- non-aluminium variable cost per can, low and high pairing
    var = {}
    for i, case in enumerate(("low", "high")):
        usd, items = nonmetal_usd(i)
        var[case] = {"usd": round(usd, 5), "thb": round(usd * FX[i], 3),
                     "items_usd": {k: round(v, 5) for k, v in items.items()}}
    # central value: every input at its midpoint (the same convention as singha_internal_estimates.py)
    mid = lambda p: (p[0] + p[1]) / 2  # noqa: E731
    usd_mid = mid(CONV_NONMETAL) + mid(FILL_CONSUM) + mid(SEAM) + mid(CO2) + mid(LIQUID)
    v_mid_thb = usd_mid * mid(FX)
    res["variable_cost_excl_aluminium_per_can"] = var
    res["variable_cost_excl_aluminium_bounding_cases_note"] = (
        "low and high are the bounding cases (every input at its low or high bound), not a 90 per cent interval. "
        "The 90 per cent interval from the Monte Carlo in singha_internal_estimates.py is narrower.")
    res["variable_cost_excl_aluminium_mid_thb"] = round(v_mid_thb, 3)

    # ---- aluminium: slope and break-even (no LME price used)
    sheet_mid = (SHEET_G[0] + SHEET_G[1]) / 2
    fx_mid = (FX[0] + FX[1]) / 2
    slope_per_100 = aluminium_thb_per_can(sheet_mid, 100.0, fx_mid)
    _, net_c = net_price(PRICE_MODE, EST["vat"]["value"], EST["retail_margin"]["mode"],
                         EST["distributor_margin"]["mode"], EST["excise_ad_valorem"]["value"])
    contrib_pre_al = net_c - v_mid_thb
    breakeven = contrib_pre_al * 1e6 / (sheet_mid * fx_mid)
    res["aluminium"] = {
        "status": "LME route not authorised. Slope and break-even only; no aluminium price is used.",
        "thb_per_can_per_usd_100_per_tonne_mid": round(slope_per_100, 4),
        "premium_scenarios_thb_per_can_mid_sheet": {str(p): round(aluminium_thb_per_can(sheet_mid, p, fx_mid), 4)
                                                   for p in PREMIUM_USD_T},
        "listing_price_basis_thb_per_can": round(PRICE_MODE, 4),
        "net_after_excise_thb_per_can": round(net_c, 3),
        "contribution_pre_aluminium_thb_per_can": round(contrib_pre_al, 3),
        "zero_contribution_price_usd_per_tonne_mid": round(breakeven, 0),
        "single_can_17_price_basis_zero_contribution_usd_per_tonne": round(
            (net_price(PRICE_SINGLE, EST["vat"]["value"], EST["retail_margin"]["mode"], EST["distributor_margin"]["mode"],
                       EST["excise_ad_valorem"]["value"])[1] - v_mid_thb) * 1e6 / (sheet_mid * fx_mid), 0),
        "note": "Price basis: mean of four online multipack listing prices read 20 October 2026 (record 68d). The 7-Eleven 24-can "
                "reading (THB 330) is a promotional selling price (the page prints 408 struck through; promotion valid to 20 October 2026). "
                "The THB 17.00 single-can basis is shown for comparison only. The price affects the aluminium break-even, not the variable cost."}

    # ---- production: cans a year and fixed-cost dilution per can (non-aluminium variable cost)
    volumes = {"at_util_low": cans_per_year(UTIL[0]), "at_util_high": cans_per_year(UTIL[1]),
               "at_nameplate_100pct": cans_per_year(1.0)}
    res["cans_per_year"] = {k: round(v) for k, v in volumes.items()}
    grid_volumes = [5e8, 1e9, round(volumes["at_nameplate_100pct"])]
    grid = []
    for q in grid_volumes:
        row = {"cans_per_year": round(q)}
        for f in FIXED_THB_M:
            row[f"fixed_{int(f)}m_thb_per_can_excl_aluminium"] = round(v_mid_thb + f * 1e6 / q, 3)
        grid.append(row)
    res["cost_per_can_grid_excl_aluminium"] = {"variable_mid_thb": round(v_mid_thb, 3), "rows": grid}

    OUT_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")

    if "--chart" in sys.argv:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        qs = [i * 1e8 / 1e9 for i in range(3, 18)]
        fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=150)
        ax.fill_between(qs, [var["low"]["thb"]] * len(qs), [var["high"]["thb"]] * len(qs), color="#A8CF3A", alpha=0.35,
                        label="non-aluminium variable cost, low to high (THB per can)")
        for f, style in zip(FIXED_THB_M, ["-", "--", ":"]):
            ax.plot(qs, [v_mid_thb + f * 1e6 / (q * 1e9) for q in qs], style, color="#17191C",
                    label="fixed THB %d m a year (central variable cost)" % f)
        ax.set_xlabel("cans per year (billion)")
        ax.set_ylabel("THB per can")
        ax.set_title("Cost per 330 ml can excluding aluminium (desk estimate)")
        ax.legend(fontsize=7, loc="upper right")
        fig.text(0.01, 0.01, "Excludes aluminium (no LME price used). Desk estimate; not Singha figures.", fontsize=6)
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(OUT_PNG)

    print(json.dumps({"variable_excl_al_thb": {k: v["thb"] for k, v in var.items()},
                      "mid_thb": round(v_mid_thb, 3), "slope_per_usd100": round(slope_per_100, 4),
                      "zero_contribution_usd_t": round(breakeven), "cans_per_year": res["cans_per_year"]}, indent=1))


if __name__ == "__main__":
    main()
