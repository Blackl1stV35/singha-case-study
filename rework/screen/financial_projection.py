"""Financial projection for the Singha lime cube (team-only record, rework/56).

Scope (user brief): operating subsidiaries (EBITDA, gross margin and price, working
capital, capex), capital allocation (acquisition and ROIC), holding company (overhead,
debt, interest, cash available for reinvestment), consolidation with intragroup
elimination and unrealised profit, and a sum-of-parts (SOTP) equity bridge.
Base case and one downside case, five projection years.

Units: million THB (MTHB) unless stated. Year 0 is the base year (proxy FY2025 values);
Years 1 to 5 are projection years, not calendar years. Servings are in millions.

Every input in INPUT_LIST carries a label: SOURCED (with a URL or team record),
PROXY (what it stands in for), or ASSUMPTION. Derived ratios are computed in derive().

Run from any directory:
    python financial_projection.py
Writes:
    financial_projection_results.json   (in this folder, screen/)
    ../charts/sotp_bridge_base.png      (the one chart, in rework/charts/)
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "financial_projection_results.json")
OUT_PNG = os.path.normpath(os.path.join(HERE, "..", "charts", "sotp_bridge_base.png"))

N = 5
YEARS = list(range(0, N + 1))  # index 0 = base year, 1..5 = projection years

# ---------------------------------------------------------------- source URLs
URL_TB_IS = "https://stockanalysis.com/quote/sgx/Y92/financials/income-statement/"
URL_TB_CF = "https://stockanalysis.com/quote/sgx/Y92/financials/cash-flow-statement/"
URL_TB_BS = "https://stockanalysis.com/quote/sgx/Y92/financials/balance-sheet/"
URL_TB_SEG = ("https://www.foodbusinessmea.com/"
              "thai-beverage-records-0-4-revenue-decline-amid-spirits-weakness/")
URL_TB_EV = "https://ca.marketscreener.com/quote/stock/THAI-BEVERAGE-6498120/valuation/"
URL_TB_FIN = "https://ca.marketscreener.com/quote/stock/THAI-BEVERAGE-6498120/finances/"
URL_SCGP_IS = "https://stockanalysis.com/quote/bkk/SCGP/financials/"
URL_SCGP_BS = "https://stockanalysis.com/quote/bkk/SCGP/financials/balance-sheet/"
URL_SCGP_CF = "https://stockanalysis.com/quote/bkk/SCGP/financials/cash-flow-statement/"
URL_S_BS = "https://stockanalysis.com/quote/bkk/S/financials/balance-sheet/"
URL_S_CF = "https://stockanalysis.com/quote/bkk/S/financials/cash-flow-statement/"
URL_S_PR = ("https://investor.singhaestate.co.th/en/newsroom/press-releases/187640/"
            "singha-estate-leverages-strength-of-recurring-income-portfolio-reports-"
            "all-time-high-normalized-profit-of-thb-531-million-ready-to-announces-"
            "dividend-of-thb-0015-per-share")
URL_INFOBEL = "https://www.infobelpro.com/companies/thailand/breweries"
URL_ZOOM = "https://www.zoominfo.com/c/boon-rawd-brewery-co-ltd/426420413"
URL_TAX = ("https://www.forvismazars.com/th/en/insights/doing-business-in-thailand/"
           "tax/corporate-income-tax-in-thailand")
REC_CUBE = "rework/53_unit_cost_and_value_chain.md (team record)"


def I(key, base, down=None, unit="", label="", source="", note=""):
    """One input row. down=None means the downside case uses the base value."""
    return dict(key=key, base=base, down=down, unit=unit, label=label, source=source, note=note)


# ---------------------------------------------------------------- inputs
INPUT_LIST = [
    # Market, tax, discounting
    I("fx", 33.4573, unit="THB/USD", label="SOURCED", source=REC_CUBE + "; XE mid-market 18 Oct 2026, as in screen/unit_cost_value_chain.py"),
    I("tax", 0.20, unit="ratio", label="SOURCED", source=URL_TAX + " (secondary: KPMG 2018 profile; Revenue Department not reached)"),
    I("wacc", 0.08, unit="ratio", label="ASSUMPTION", note="hurdle rate for ROIC comparison; not sourced"),
    I("rate_shock", 0.0, 0.01, unit="ratio", label="ASSUMPTION", note="added to all debt rates in the downside"),

    # Beverage operating company (beer and non-alcoholic; the cube sits here)
    I("infobel_sbc_usd_m", 1100.0, unit="USD m", label="PROXY",
      source=URL_INFOBEL + " (Singha Beverage Company Ltd, directory estimate, no fiscal year). Stands in for beverage subsidiary revenue"),
    I("infobel_brb_usd_m", 341.0, unit="USD m", label="PROXY", source=URL_INFOBEL + " (The Boon Rawd Brewery Co Ltd). Used in sensitivity only"),
    I("zoom_brb_usd_m", 578.5, unit="USD m", label="PROXY", source=URL_ZOOM + " (aggregator estimate). Used in sensitivity only"),
    I("tb_rev", 334704.0, unit="MTHB", label="PROXY", source=URL_TB_IS + " (ThaiBev FY2025). Stands in for the beverage operating company's margin structure"),
    I("tb_gp", 104926.0, unit="MTHB", label="PROXY", source=URL_TB_IS + " (ThaiBev FY2025 gross profit)"),
    I("tb_ebitda", 50654.0, unit="MTHB", label="PROXY", source=URL_TB_IS + " (ThaiBev FY2025 EBITDA; The Edge reports 57.01bn, a conflict; see limits)"),
    I("tb_da", 10346.0, unit="MTHB", label="PROXY", source=URL_TB_CF + " (ThaiBev FY2025 D&A)"),
    I("tb_capex", 12998.0, unit="MTHB", label="PROXY", source=URL_TB_CF + " (ThaiBev FY2025 capex)"),
    I("tb_ar", 17856.0, unit="MTHB", label="PROXY", source=URL_TB_BS + " (ThaiBev FY2025 total receivables)"),
    I("tb_ap", 13423.0, unit="MTHB", label="PROXY", source=URL_TB_BS + " (ThaiBev FY2025 accounts payable)"),
    I("tb_cash", 43845.0, unit="MTHB", label="PROXY", source=URL_TB_BS + " (ThaiBev FY2025 cash)"),
    I("tb_debt", 234545.0, unit="MTHB", label="PROXY", source=URL_TB_BS + " (ThaiBev FY2025 total debt, read as including leases)"),
    I("tb_lease", 7012.0, unit="MTHB", label="PROXY", source=URL_TB_BS + " (ThaiBev FY2025 lease liabilities)"),
    I("tb_beer_rev_9m", 96500.0, unit="MTHB", label="PROXY", source=URL_TB_SEG + " (beer, nine months to 30 Jun 2025, THB 96.50bn)"),
    I("tb_beer_ebitda_9m", 12570.0, unit="MTHB", label="PROXY", source=URL_TB_SEG + " (beer EBITDA, nine months to 30 Jun 2025, THB 12.57bn)"),
    I("tb_nab_rev_9m", 49330.0, unit="MTHB", label="PROXY", source=URL_TB_SEG + " (NAB revenue, nine months to 30 Jun 2025, THB 49.33bn)"),
    I("tb_nab_ebitda_9m", 8720.0, unit="MTHB", label="PROXY", source=URL_TB_SEG + " (NAB EBITDA, nine months to 30 Jun 2025, THB 8.72bn)"),
    I("tb_food_rev_9m", 16560.0, unit="MTHB", label="PROXY", source=URL_TB_SEG + " (food revenue, nine months to 30 Jun 2025, THB 16.56bn)"),
    I("tb_food_ebitda_9m", 1580.0, unit="MTHB", label="PROXY", source=URL_TB_SEG + " (food EBITDA, nine months to 30 Jun 2025, THB 1.58bn)"),
    I("bev_mult", 8.8, unit="x", label="SOURCED", source=URL_TB_EV + " (ThaiBev FY2025 EV/EBITDA, vendor figure); applied to the beverage subsidiary as a PROXY multiple"),
    I("bev_dio", 40.0, unit="days", label="ASSUMPTION", note="beer and NAB inventory days on COGS. ThaiBev group figure (about 104 days) reflects spirits ageing, so not used"),
    I("bev_growth", 0.02, -0.02, unit="ratio", label="ASSUMPTION", note="anchored to ThaiBev beer and NAB 9M revenue of -0.3% and -0.7%"),
    I("bev_margin_shock", 0.0, -0.015, unit="pp", label="ASSUMPTION", note="downside margin cut versus proxy margin"),

    # Packaging subsidiary (pouch film; acquired at start of Year 1)
    I("pkg_rev0", 4000.0, unit="MTHB", label="ASSUMPTION", note="external revenue scale; no sourced figure for a group packaging entity"),
    I("scgp_rev", 124374.0, unit="MTHB", label="PROXY", source=URL_SCGP_IS + " (SCG Packaging FY2025 revenue)"),
    I("scgp_gp", 22254.0, unit="MTHB", label="PROXY", source=URL_SCGP_IS + " (SCG Packaging FY2025 gross profit)"),
    I("scgp_op", 8456.0, unit="MTHB", label="PROXY", source=URL_SCGP_IS + " (SCG Packaging FY2025 operating income)"),
    I("scgp_da", 8759.0, unit="MTHB", label="PROXY", source=URL_SCGP_CF + " (SCG Packaging FY2025 D&A)"),
    I("scgp_oth_amort", 209.25, unit="MTHB", label="PROXY", source=URL_SCGP_CF + " (SCG Packaging FY2025 other amortisation)"),
    I("scgp_capex", 4922.0, unit="MTHB", label="PROXY", source=URL_SCGP_CF + " (SCG Packaging FY2025 capex)"),
    I("scgp_ar", 22152.0, unit="MTHB", label="PROXY", source=URL_SCGP_BS + " (SCG Packaging FY2025 receivables)"),
    I("scgp_inv", 17356.0, unit="MTHB", label="PROXY", source=URL_SCGP_BS + " (SCG Packaging FY2025 inventory)"),
    I("scgp_ap", 14582.0, unit="MTHB", label="PROXY", source=URL_SCGP_BS + " (SCG Packaging FY2025 payables)"),
    I("pkg_growth", 0.03, 0.0, unit="ratio", label="ASSUMPTION"),
    I("pkg_margin_shock", 0.0, -0.01, unit="pp", label="ASSUMPTION"),
    I("pkg_mult", 7.0, unit="x", label="ASSUMPTION", note="SOTP multiple; not sourced"),
    I("pkg_acq_mult", 7.0, unit="x", label="ASSUMPTION", note="acquisition price, EV over Year 0 EBITDA; not sourced"),
    I("pkg_nd0", 0.0, unit="MTHB", label="ASSUMPTION", note="sub debt refinanced by holding company at acquisition, so the acquisition price is an EV"),

    # Property subsidiary (listed; group control and stake NOT confirmed)
    I("s_rev", 13988.0, unit="MTHB", label="PROXY", source=URL_S_PR + " (Singha Estate FY2025 core operating revenue). Stands in for the group's property arm"),
    I("s_ebitda_norm", 3649.0, unit="MTHB", label="PROXY", source=URL_S_PR + " (Singha Estate FY2025 normalized EBITDA)"),
    I("s_da", 1301.0, unit="MTHB", label="PROXY", source=URL_S_CF + " (Singha Estate FY2025 D&A)"),
    I("s_capex", 888.99, unit="MTHB", label="PROXY", source=URL_S_CF + " (Singha Estate FY2025 capex)"),
    I("s_ar", 1098.0, unit="MTHB", label="PROXY", source=URL_S_BS + " (Singha Estate FY2025 receivables, total)"),
    I("s_inv", 10764.0, unit="MTHB", label="PROXY", source=URL_S_BS + " (Singha Estate FY2025 inventory; property held for sale)"),
    I("s_ap", 313.99, unit="MTHB", label="PROXY", source=URL_S_BS + " (Singha Estate FY2025 accounts payable)"),
    I("s_st_debt", 3213.0, unit="MTHB", label="PROXY", source=URL_S_BS + " (Singha Estate FY2025 short-term debt)"),
    I("s_cpltd", 5574.0, unit="MTHB", label="PROXY", source=URL_S_BS + " (Singha Estate FY2025 current portion of long-term debt)"),
    I("s_ltd", 24323.0, unit="MTHB", label="PROXY", source=URL_S_BS + " (Singha Estate FY2025 long-term debt; leases excluded)"),
    I("s_cash", 2726.0, unit="MTHB", label="PROXY", source=URL_S_BS + " (Singha Estate FY2025 cash)"),
    I("prop_gm", 0.45, unit="ratio", label="ASSUMPTION", note="gross margin for the property arm; no COGS line sourced"),
    I("prop_growth", 0.03, 0.0, unit="ratio", label="ASSUMPTION"),
    I("prop_margin_shock", 0.0, -0.02, unit="pp", label="ASSUMPTION"),
    I("prop_mult", 9.0, unit="x", label="ASSUMPTION", note="EV/EBITDA; not sourced. Sensitivity 7x to 11x"),

    # Food subsidiary
    I("food_rev0", 3000.0, unit="MTHB", label="ASSUMPTION", note="scale; no sourced figure"),
    I("food_growth", 0.0, -0.03, unit="ratio", label="ASSUMPTION", note="ThaiBev food 9M revenue was -1.4% year on year"),
    I("food_margin_shock", 0.0, -0.01, unit="pp", label="ASSUMPTION"),
    I("food_gm", 0.30, unit="ratio", label="ASSUMPTION"),
    I("food_da", 0.03, unit="ratio", label="ASSUMPTION"),
    I("food_capex", 0.02, unit="ratio", label="ASSUMPTION"),
    I("food_dso", 30.0, unit="days", label="ASSUMPTION"),
    I("food_dio", 40.0, unit="days", label="ASSUMPTION"),
    I("food_dpo", 35.0, unit="days", label="ASSUMPTION"),
    I("food_lev", 1.5, unit="x", label="ASSUMPTION", note="net debt over EBITDA"),
    I("food_mult", 8.0, unit="x", label="ASSUMPTION"),

    # Cube (sits in the beverage operating company)
    I("cube_retail", 15.0, unit="THB/serving", label="ASSUMPTION", note="set equal to the can's launch shelf price (LISTED, rework/53 section 3)"),
    I("cube_ret_m", 0.30, 0.35, unit="ratio", label="ASSUMPTION", note="retailer margin; mid and high cases of rework/53"),
    I("cube_dist_m", 0.15, 0.20, unit="ratio", label="ASSUMPTION", note="distributor margin; mid and high cases of rework/53"),
    I("cube_serv_base", [2.0, 4.0, 6.0, 7.0, 8.0], unit="million servings", label="ASSUMPTION",
      note="scenario input. No volume is taken from the consumer study: rework/55 does not exist"),
    I("cube_serv_scale", 1.0, 0.5, unit="ratio", label="ASSUMPTION", note="multiplier on the scenario volume"),
    I("cube_fixed", 15.0, 20.0, unit="MTHB/yr", label="ASSUMPTION", note="launch marketing, registration, trademark, listing; excluded by rework/53"),
    I("cube_capex", 25.0, unit="MTHB", label="ASSUMPTION", note="filling and compaction line, placed in service at start of Year 1"),
    I("cube_life", 5.0, unit="years", label="ASSUMPTION"),
    I("cube_ar_days", 30.0, unit="days", label="ASSUMPTION"),
    I("cube_inv_days", 45.0, 45.0, unit="days", label="ASSUMPTION", note="also the holding period for intragroup pouch film"),
    I("cube_ap_days", 30.0, unit="days", label="ASSUMPTION"),
    I("cube_cost_case", "mid", "high", unit="case", label="ASSUMPTION", note="mid is the midpoint of the rework/53 low and high cases"),
    I("khc_usd", 242.0, unit="USD", label="SOURCED", source=REC_CUBE + ": potassium bicarbonate, USD 242 for 22.68 kg (US listing)"),
    I("khc_kg", 22.68, unit="kg", label="SOURCED", source=REC_CUBE),
    I("khc_high_mult", 2.0, unit="x", label="ASSUMPTION", note="high-cost case doubles the low price, per rework/53"),
    I("khc_g", 2.58, unit="g/serving", label="SOURCED", source=REC_CUBE + " (design mass at 1.75 volumes)"),
    I("citric_g", 1.65, unit="g/serving", label="SOURCED", source=REC_CUBE),
    I("citric_low", 115.0, unit="THB/kg", label="SOURCED", source=REC_CUBE + " (US listings, converted)"),
    I("citric_high", 142.0, unit="THB/kg", label="SOURCED", source=REC_CUBE),
    I("sucr_thb_kg", 655.0, unit="THB/kg", label="SOURCED", source=REC_CUBE + " (Lazada TH listing, sucralose)"),
    I("sucr_low_g", 0.01, unit="g/serving", label="ASSUMPTION", note="sweetener dose"),
    I("sucr_high_g", 0.10, unit="g/serving", label="ASSUMPTION", note="sweetener dose"),
    I("pouch_usd_low", 0.030, unit="USD/piece", label="SOURCED", source=REC_CUBE + " (non-Thai listing, spec unconfirmed)"),
    I("pouch_usd_high", 0.050, unit="USD/piece", label="SOURCED", source=REC_CUBE + " (non-Thai listing, spec unconfirmed)"),
    I("print_low", 0.0, unit="THB/serving", label="ASSUMPTION", note="print placeholder, no public price"),
    I("print_high", 1.50, unit="THB/serving", label="ASSUMPTION", note="print placeholder, no public price"),

    # Holding company
    I("hold_oh0", 150.0, unit="MTHB/yr", label="ASSUMPTION", note="corporate overhead; no sourced figure"),
    I("hold_oh_g", 0.03, unit="ratio", label="ASSUMPTION"),
    I("hold_debt0", 12000.0, unit="MTHB", label="ASSUMPTION", note="holding company senior debt; not sourced"),
    I("hold_rate", 0.045, unit="ratio", label="ASSUMPTION"),
    I("hold_amort", 1000.0, unit="MTHB/yr", label="ASSUMPTION"),
    I("hold_cash0", 3000.0, unit="MTHB", label="ASSUMPTION"),
    I("hold_min_cash", 1000.0, unit="MTHB", label="ASSUMPTION"),
    I("acq_debt_share", 0.60, unit="ratio", label="ASSUMPTION", note="share of the packaging acquisition funded by new holding debt"),
    I("acq_rate", 0.05, unit="ratio", label="ASSUMPTION"),
    I("sub_rate", 0.045, unit="ratio", label="ASSUMPTION", note="interest on each subsidiary's own net debt"),
    I("payout", 0.60, unit="ratio", label="ASSUMPTION", note="share of positive subsidiary FCF to equity paid to the holding company"),
]

def base_params(case):
    """Pick the base or downside value for each input row."""
    p = {}
    for row in INPUT_LIST:
        if case == "downside" and row["down"] is not None:
            p[row["key"]] = row["down"]
        else:
            p[row["key"]] = row["base"]
    return p


def derive(p):
    """Ratios and unit values derived from the raw inputs."""
    d = {}
    fx = p["fx"]
    # beverage operating company
    d["bev_rev0"] = p["infobel_sbc_usd_m"] * fx
    d["tb_cogs"] = p["tb_rev"] - p["tb_gp"]
    d["bev_gm"] = p["tb_gp"] / p["tb_rev"]
    d["bev_margin0"] = (p["tb_beer_ebitda_9m"] + p["tb_nab_ebitda_9m"]) / (p["tb_beer_rev_9m"] + p["tb_nab_rev_9m"])
    d["bev_margin"] = d["bev_margin0"] + p["bev_margin_shock"]
    d["bev_da_pct"] = p["tb_da"] / p["tb_rev"]
    d["bev_capex_pct"] = p["tb_capex"] / p["tb_rev"]
    d["bev_dso"] = p["tb_ar"] / p["tb_rev"] * 365
    d["bev_dpo"] = p["tb_ap"] / d["tb_cogs"] * 365
    d["bev_lev"] = (p["tb_debt"] - p["tb_lease"] - p["tb_cash"]) / p["tb_ebitda"]
    # packaging
    d["pkg_cogs0"] = p["scgp_rev"] - p["scgp_gp"]
    d["pkg_gm"] = p["scgp_gp"] / p["scgp_rev"]
    d["pkg_margin0"] = (p["scgp_op"] + p["scgp_da"] + p["scgp_oth_amort"]) / p["scgp_rev"]
    d["pkg_margin"] = d["pkg_margin0"] + p["pkg_margin_shock"]
    d["pkg_da_pct"] = (p["scgp_da"] + p["scgp_oth_amort"]) / p["scgp_rev"]
    d["pkg_capex_pct"] = p["scgp_capex"] / p["scgp_rev"]
    d["pkg_dso"] = p["scgp_ar"] / p["scgp_rev"] * 365
    d["pkg_dio"] = p["scgp_inv"] / d["pkg_cogs0"] * 365
    d["pkg_dpo"] = p["scgp_ap"] / d["pkg_cogs0"] * 365
    # property
    d["prop_margin0"] = p["s_ebitda_norm"] / p["s_rev"]
    d["prop_margin"] = d["prop_margin0"] + p["prop_margin_shock"]
    d["prop_da_pct"] = p["s_da"] / p["s_rev"]
    d["prop_capex_pct"] = p["s_capex"] / p["s_rev"]
    d["prop_dso"] = p["s_ar"] / p["s_rev"] * 365
    d["prop_dio"] = p["s_inv"] / p["s_rev"] * 365   # revenue basis: no COGS line sourced
    d["prop_dpo"] = p["s_ap"] / p["s_rev"] * 365    # revenue basis
    d["prop_nd0"] = p["s_st_debt"] + p["s_cpltd"] + p["s_ltd"] - p["s_cash"]
    # food
    d["food_margin0"] = p["tb_food_ebitda_9m"] / p["tb_food_rev_9m"]
    d["food_margin"] = d["food_margin0"] + p["food_margin_shock"]
    # cube unit costs (THB per serving), low / mid / high, from rework/53 constants
    khc_low_g = p["khc_usd"] / p["khc_kg"] * fx / 1000.0
    khc_high_g = khc_low_g * p["khc_high_mult"]
    ingr = {"low": p["khc_g"] * khc_low_g + p["citric_g"] * p["citric_low"] / 1000.0,
            "high": p["khc_g"] * khc_high_g + p["citric_g"] * p["citric_high"] / 1000.0}
    sweet = {"low": p["sucr_low_g"] * p["sucr_thb_kg"] / 1000.0,
             "high": p["sucr_high_g"] * p["sucr_thb_kg"] / 1000.0}
    pouch = {"low": p["pouch_usd_low"] * fx, "high": p["pouch_usd_high"] * fx}
    prnt = {"low": p["print_low"], "high": p["print_high"]}
    comp = {}
    for k in ("low", "high"):
        comp[k] = {"ingredients": ingr[k], "sweetener": sweet[k], "pouch_film": pouch[k], "print": prnt[k]}
    comp["mid"] = {c: (comp["low"][c] + comp["high"][c]) / 2.0 for c in comp["low"]}
    d["cube_comp"] = comp
    cc = p["cube_cost_case"]
    d["cube_cost_ps"] = sum(comp[cc].values())
    d["cube_pouch_ps"] = comp[cc]["pouch_film"]
    d["cube_price"] = p["cube_retail"] * (1 - p["cube_ret_m"]) * (1 - p["cube_dist_m"])
    return d


def build_sub(rev0, growth, gm, m0, m, da_pct, capex_pct, dso, dio, dpo, inv_on_cogs=True):
    """Standalone P&L and working-capital arrays for one operating company."""
    rev = [rev0 * (1 + growth) ** t for t in YEARS]
    cogs = [r * (1 - gm) for r in rev]
    ebitda = [rev[0] * m0] + [rev[t] * m for t in YEARS[1:]]
    da = [r * da_pct for r in rev]
    capex = [r * capex_pct for r in rev]
    ar = [r * dso / 365.0 for r in rev]
    base = cogs if inv_on_cogs else rev
    inv = [b * dio / 365.0 for b in base]
    ap = [b * dpo / 365.0 for b in base]
    nwc = [a + i - q for a, i, q in zip(ar, inv, ap)]
    return dict(rev=rev, cogs=cogs, gp=[r - c for r, c in zip(rev, cogs)], ebitda=ebitda,
                da=da, capex=capex, nwc=nwc)


def build_cube(p, d):
    """Cube P&L at transfer price (pouch film bought from the packaging subsidiary)."""
    s = [0.0] + [x * p["cube_serv_scale"] for x in p["cube_serv_base"]]
    price, cost_ps, pouch_ps = d["cube_price"], d["cube_cost_ps"], d["cube_pouch_ps"]
    rev = [x * price for x in s]
    cogs = [x * cost_ps for x in s]
    fixed = [0.0] + [p["cube_fixed"]] * N
    tp_ebitda = [r - c - f for r, c, f in zip(rev, cogs, fixed)]
    film_purch = [x * pouch_ps for x in s]                     # P_t, intragroup purchases at transfer price
    film_inv = [x * p["cube_inv_days"] / 365.0 for x in film_purch]
    up = [x * d["pkg_gm"] for x in film_inv]                  # unrealised profit in closing inventory
    dup = [0.0] + [up[t] - up[t - 1] for t in YEARS[1:]]
    pkg_margin_on_film = [x * d["pkg_gm"] for x in film_purch]
    group_ebitda = [tp_ebitda[t] + pkg_margin_on_film[t] - dup[t] for t in YEARS]
    da_per_yr = p["cube_capex"] / p["cube_life"]
    da = [0.0] + [da_per_yr] * N
    capex = [0.0, p["cube_capex"]] + [0.0] * (N - 1)
    ppe = [p["cube_capex"]] + [max(0.0, p["cube_capex"] - da_per_yr * t) for t in YEARS[1:]]
    ar = [r * p["cube_ar_days"] / 365.0 for r in rev]
    inv = [c * p["cube_inv_days"] / 365.0 for c in cogs]
    ap = [c * p["cube_ap_days"] / 365.0 for c in cogs]
    nwc = [a + i - q for a, i, q in zip(ar, inv, ap)]
    return dict(serv=s, rev=rev, cogs=cogs, fixed=fixed, tp_ebitda=tp_ebitda, film_purch=film_purch,
                film_inv=film_inv, up=up, dup=dup, pkg_margin_on_film=pkg_margin_on_film,
                group_ebitda=group_ebitda, da=da, capex=capex, ppe=ppe, nwc=nwc)


def finance(sub, nd0, rate, payout):
    """Subsidiary net debt roll, interest, tax and dividends to the holding company."""
    nd, intr, ni, fcfe, div = [nd0], [0.0], [0.0], [0.0], [0.0]
    for t in YEARS[1:]:
        i_t = nd[t - 1] * rate
        pbt = sub["ebitda"][t] - sub["da"][t] - i_t
        tax_t = max(0.0, pbt) * TAX_RATE
        n_t = pbt - tax_t
        f_t = n_t + sub["da"][t] - sub["capex"][t] - (sub["nwc"][t] - sub["nwc"][t - 1])
        d_t = payout * max(0.0, f_t)
        nd.append(nd[t - 1] - (f_t - d_t))
        intr.append(i_t)
        ni.append(n_t)
        fcfe.append(f_t)
        div.append(d_t)
    return dict(nd=nd, interest=intr, net_income=ni, fcfe=fcfe, dividend=div)


TAX_RATE = 0.20


def run(case="base", ov=None):
    global TAX_RATE
    p = base_params(case)
    p.update(ov or {})
    TAX_RATE = p["tax"]
    d = derive(p)
    rate_all = p["sub_rate"] + p["rate_shock"]

    # ---- operating subsidiaries
    bev_core = build_sub(d["bev_rev0"], p["bev_growth"], d["bev_gm"], d["bev_margin0"], d["bev_margin"],
                         d["bev_da_pct"], d["bev_capex_pct"], d["bev_dso"], p["bev_dio"], d["bev_dpo"])
    cube = build_cube(p, d)
    pkg_core = build_sub(p["pkg_rev0"], p["pkg_growth"], d["pkg_gm"], d["pkg_margin0"], d["pkg_margin"],
                         d["pkg_da_pct"], d["pkg_capex_pct"], d["pkg_dso"], d["pkg_dio"], d["pkg_dpo"])
    prop = build_sub(p["s_rev"], p["prop_growth"], p["prop_gm"], d["prop_margin0"], d["prop_margin"],
                     d["prop_da_pct"], d["prop_capex_pct"], d["prop_dso"],
                     d["prop_dio"], d["prop_dpo"], inv_on_cogs=False)
    food = build_sub(p["food_rev0"], p["food_growth"], p["food_gm"], d["food_margin0"], d["food_margin"],
                     p["food_da"], p["food_capex"], p["food_dso"], p["food_dio"], p["food_dpo"])

    # packaging with intragroup film sales to the cube (P_t) added to revenue, COGS and EBITDA
    P = cube["film_purch"]
    gm_p = d["pkg_gm"]
    pkg = {
        "rev": [a + b for a, b in zip(pkg_core["rev"], P)],
        "cogs": [a + b * (1 - gm_p) for a, b in zip(pkg_core["cogs"], P)],
        "ebitda": [a + b * gm_p for a, b in zip(pkg_core["ebitda"], P)],
        "da": pkg_core["da"], "capex": pkg_core["capex"], "nwc": pkg_core["nwc"],
    }
    pkg["gp"] = [r - c for r, c in zip(pkg["rev"], pkg["cogs"])]

    # beverage total = core + cube (cube at transfer price)
    bev = {
        "rev": [a + b for a, b in zip(bev_core["rev"], cube["rev"])],
        "cogs": [a + b for a, b in zip(bev_core["cogs"], cube["cogs"])],
        "ebitda": [a + b for a, b in zip(bev_core["ebitda"], cube["tp_ebitda"])],
        "da": [a + b for a, b in zip(bev_core["da"], cube["da"])],
        "capex": [a + b for a, b in zip(bev_core["capex"], cube["capex"])],
        "nwc": [a + b for a, b in zip(bev_core["nwc"], cube["nwc"])],
    }
    bev["gp"] = [r - c for r, c in zip(bev["rev"], bev["cogs"])]

    subs = {"beverage": bev, "packaging": pkg, "property": prop, "food": food}
    nd0_bev = d["bev_lev"] * bev_core["ebitda"][0]
    nd0_food = p["food_lev"] * food["ebitda"][0]
    fin = {
        "beverage": finance(bev, nd0_bev, rate_all, p["payout"]),
        "packaging": finance(pkg, p["pkg_nd0"], rate_all, p["payout"]),
        "property": finance(prop, d["prop_nd0"], rate_all, p["payout"]),
        "food": finance(food, nd0_food, rate_all, p["payout"]),
    }

    # ---- capital allocation: packaging acquisition at start of Year 1
    ev_acq = p["pkg_acq_mult"] * pkg_core["ebitda"][0]
    acq_debt = ev_acq * p["acq_debt_share"]
    acq_equity = ev_acq - acq_debt

    # ---- holding company
    oh = [p["hold_oh0"] * (1 + p["hold_oh_g"]) ** t for t in YEARS]
    debt_old = [p["hold_debt0"]]
    cash = [p["hold_cash0"] - acq_equity]
    int_old, int_acq, amort, div_in, car = [0.0], [0.0], [0.0], [0.0], [cash[0] - p["hold_min_cash"]]
    for t in YEARS[1:]:
        io = debt_old[t - 1] * (p["hold_rate"] + p["rate_shock"])
        ia = acq_debt * (p["acq_rate"] + p["rate_shock"])
        am = min(p["hold_amort"], debt_old[t - 1])
        dv = sum(fin[k]["dividend"][t] for k in fin)
        debt_old.append(debt_old[t - 1] - am)
        cash.append(cash[t - 1] + dv - oh[t] - io - ia - am)
        int_old.append(io)
        int_acq.append(ia)
        amort.append(am)
        div_in.append(dv)
        car.append(cash[t] - p["hold_min_cash"])
    holdco = dict(overhead=oh, debt_old=debt_old, debt_acq=[acq_debt] * (N + 1),
                  debt_total=[a + acq_debt for a in debt_old], cash=cash,
                  interest_old=int_old, interest_acq=int_acq, amortisation=amort,
                  dividends_in=div_in, cash_available_for_reinvestment=car,
                  ebitda=[-x for x in oh], acq_ev=ev_acq, acq_debt=acq_debt, acq_equity=acq_equity)

    # ---- consolidation and intragroup elimination
    dup = cube["dup"]
    up = cube["up"]
    rev_sum = [sum(subs[k]["rev"][t] for k in subs) for t in YEARS]
    cogs_sum = [sum(subs[k]["cogs"][t] for k in subs) for t in YEARS]
    ebitda_sum = [sum(subs[k]["ebitda"][t] for k in subs) + holdco["ebitda"][t] for t in YEARS]
    elim_rev = [-x for x in P]
    elim_cogs = [-P[t] + dup[t] for t in YEARS]          # purchases removed, plus change in unrealised profit
    rev_cons = [rev_sum[t] + elim_rev[t] for t in YEARS]
    cogs_cons = [cogs_sum[t] + elim_cogs[t] for t in YEARS]
    # opex = gp - ebitda per sub, plus holdco overhead; consolidated EBITDA = consolidated GP - opex
    opex_sum = [sum(subs[k]["gp"][t] - subs[k]["ebitda"][t] for k in subs) + holdco["overhead"][t] for t in YEARS]
    ebitda_cons = [(rev_cons[t] - cogs_cons[t]) - opex_sum[t] for t in YEARS]
    nd_cons = [sum(fin[k]["nd"][t] for k in fin) + holdco["debt_total"][t] - holdco["cash"][t] for t in YEARS]

    consolidated = dict(
        revenue_sum_of_parts=rev_sum, intragroup_revenue_eliminated=elim_rev, revenue=rev_cons,
        cogs_sum_of_parts=cogs_sum, intragroup_cogs_eliminated=elim_cogs, cogs=cogs_cons,
        ebitda_sum_of_parts=ebitda_sum, unrealised_profit_closing=up, unrealised_profit_change=dup,
        net_elimination_ebitda=[-x for x in dup], ebitda=ebitda_cons, net_debt=nd_cons,
    )

    # ---- cube contribution to group EBITDA (group basis) and value
    group_ebitda_cube = cube["group_ebitda"]
    share_cube = [group_ebitda_cube[t] / ebitda_cons[t] if ebitda_cons[t] else 0.0 for t in YEARS]

    # ---- sum of parts (valuation at start of Year 1, pro forma for acquisition, on Year 1 EBITDA)
    mult_bev, mult_prop = p["bev_mult"], p["prop_mult"]
    sotp_lines = [
        ("Beverage core (beer and NAB)", bev_core["ebitda"][1] * mult_bev, mult_bev),
        ("Cube (SOTP line, transfer-price EBITDA)", cube["tp_ebitda"][1] * mult_bev, mult_bev),
        ("Packaging (acquired)", pkg["ebitda"][1] * p["pkg_mult"], p["pkg_mult"]),
        ("Property", prop["ebitda"][1] * mult_prop, mult_prop),
        ("Food", food["ebitda"][1] * p["food_mult"], p["food_mult"]),
        ("Holding company overhead (capitalised)", -oh[1] * mult_bev, mult_bev),
        ("Unrealised profit adjustment (capitalised)", -dup[1] * mult_bev, mult_bev),
    ]
    sum_ev = sum(v for _, v, _ in sotp_lines)
    cash_pf = holdco["cash"][0]
    debt_pf = holdco["debt_total"][0]
    equity_spec = sum_ev + cash_pf - debt_pf
    sub_nd0 = {"beverage": fin["beverage"]["nd"][0], "packaging": fin["packaging"]["nd"][0],
               "property": fin["property"]["nd"][0], "food": fin["food"]["nd"][0]}
    sub_nd_total = sum(sub_nd0.values())
    equity_full = equity_spec - sub_nd_total

    # ---- ROIC: packaging acquisition
    pkg_da = pkg["da"]
    ic = [ev_acq]
    roic_acq = [None]
    nopat_acq = [None]
    for t in YEARS[1:]:
        nop = (pkg["ebitda"][t] - pkg_da[t]) * (1 - TAX_RATE)
        ic_t = ic[t - 1] + pkg["capex"][t] - pkg_da[t] + (pkg["nwc"][t] - pkg["nwc"][t - 1])
        ic.append(ic_t)
        nopat_acq.append(nop)
        roic_acq.append(nop / ((ic[t - 1] + ic_t) / 2.0))
    breakeven_mult = (nopat_acq[1] / p["wacc"]) / pkg_core["ebitda"][0]

    # ---- ROIC and NPV: cube (group basis)
    ic_c = [cube["ppe"][t] + cube["nwc"][t] for t in YEARS]
    roic_cube = [None]
    nopat_cube = [None]
    ufcf = [None]
    for t in YEARS[1:]:
        ebit_c = group_ebitda_cube[t] - cube["da"][t]
        nop = ebit_c * (1 - TAX_RATE)
        nopat_cube.append(nop)
        roic_cube.append(nop / ((ic_c[t - 1] + ic_c[t]) / 2.0))
        dn = cube["nwc"][t] - cube["nwc"][t - 1]
        ufcf.append(group_ebitda_cube[t] - TAX_RATE * max(0.0, ebit_c) - cube["capex"][t] - dn)
    tv = group_ebitda_cube[N] * mult_bev
    w = p["wacc"]
    npv_cube = sum(ufcf[t] / (1 + w) ** t for t in YEARS[1:]) + tv / (1 + w) ** N

    # ---- break-even servings (steady state, group basis)
    unit_margin = d["cube_price"] - d["cube_cost_ps"] + d["cube_pouch_ps"] * d["pkg_gm"]
    s_breakeven = p["cube_fixed"] / unit_margin
    s_one_pct = (p["cube_fixed"] + 0.01 * ebitda_cons[N]) / unit_margin

    result = dict(
        case=case,
        derived=dict(bev_rev0=d["bev_rev0"], bev_gm=d["bev_gm"], bev_margin=d["bev_margin"],
                     bev_lev=d["bev_lev"], pkg_gm=d["pkg_gm"], pkg_margin=d["pkg_margin"],
                     prop_margin=d["prop_margin"], food_margin=d["food_margin"],
                     prop_nd0=d["prop_nd0"], cube_price=d["cube_price"], cube_cost_ps=d["cube_cost_ps"],
                     cube_pouch_ps=d["cube_pouch_ps"], cube_comp=d["cube_comp"],
                     bev_dso=d["bev_dso"], bev_dpo=d["bev_dpo"], pkg_dso=d["pkg_dso"], pkg_dio=d["pkg_dio"],
                     pkg_dpo=d["pkg_dpo"], prop_dso=d["prop_dso"], prop_dio=d["prop_dio"], prop_dpo=d["prop_dpo"],
                     bev_da_pct=d["bev_da_pct"], bev_capex_pct=d["bev_capex_pct"],
                     pkg_da_pct=d["pkg_da_pct"], pkg_capex_pct=d["pkg_capex_pct"],
                     prop_da_pct=d["prop_da_pct"], prop_capex_pct=d["prop_capex_pct"]),
        operating=dict(beverage_core=bev_core, beverage=bev, cube=cube, packaging=pkg,
                       property=prop, food=food),
        financing=fin,
        holding_company=holdco,
        intercompany=dict(film_purchases_at_transfer=P, film_inventory_at_transfer=cube["film_inv"],
                          unrealised_profit_closing=up, unrealised_profit_change=dup,
                          packaging_margin_on_film=cube["pkg_margin_on_film"]),
        consolidation=consolidated,
        sotp=dict(lines=[dict(name=n, value=v, multiple=m) for n, v, m in sotp_lines],
                  sum_of_parts_ev=sum_ev, holdco_cash_pro_forma=cash_pf, holdco_debt_pro_forma=debt_pf,
                  equity_as_specified=equity_spec, subsidiary_net_debt=sub_nd0,
                  subsidiary_net_debt_total=sub_nd_total, equity_after_subsidiary_debt=equity_full),
        capital_allocation=dict(acquisition_ev=ev_acq, acquisition_debt=acq_debt, acquisition_equity=acq_equity,
                                acquisition_ev_over_ebitda0=ev_acq / pkg_core["ebitda"][0],
                                invested_capital=ic, nopat=nopat_acq, roic=roic_acq, wacc=p["wacc"],
                                breakeven_multiple_at_wacc=breakeven_mult),
        cube_value=dict(group_ebitda=group_ebitda_cube, share_of_group_ebitda=share_cube,
                        invested_capital=ic_c, nopat=nopat_cube, roic=roic_cube, ufcf=ufcf,
                        terminal_value_y5=tv, npv=npv_cube,
                        sotp_line_value=sotp_lines[1][1]),
        break_even=dict(unit_margin_group=unit_margin, servings_for_zero_ebitda_m=s_breakeven,
                        servings_for_one_pct_of_group_ebitda_m=s_one_pct),
        summary=dict(group_ebitda=ebitda_cons, group_revenue=rev_cons, equity_as_specified=equity_spec,
                     equity_after_subsidiary_debt=equity_full, sum_of_parts_ev=sum_ev,
                     cube_group_ebitda=group_ebitda_cube, cube_npv=npv_cube,
                     min_cash_available_for_reinvestment=min(car), cash_available_for_reinvestment=car),
    )
    return result


def checks(res):
    """Identity checks. Each returns the largest absolute gap, which must be near zero."""
    c = res["consolidation"]
    gaps = {}
    gaps["ebitda_cons_equals_sum_less_dUP"] = max(abs(c["ebitda"][t] - (c["ebitda_sum_of_parts"][t] - c["unrealised_profit_change"][t])) for t in YEARS)
    gaps["elim_revenue_plus_cogs_net_is_minus_dUP"] = max(abs((c["intragroup_revenue_eliminated"][t] - c["intragroup_cogs_eliminated"][t]) + c["unrealised_profit_change"][t]) for t in YEARS)
    sp = res["sotp"]
    gaps["sotp_bridge"] = abs(sp["equity_as_specified"] - (sp["sum_of_parts_ev"] + sp["holdco_cash_pro_forma"] - sp["holdco_debt_pro_forma"]))
    gaps["holdco_cash_roll"] = max(abs(res["holding_company"]["cash"][t] - (res["holding_company"]["cash"][t - 1]
                                   + res["holding_company"]["dividends_in"][t] - res["holding_company"]["overhead"][t]
                                   - res["holding_company"]["interest_old"][t] - res["holding_company"]["interest_acq"][t]
                                   - res["holding_company"]["amortisation"][t])) for t in YEARS[1:])
    return gaps


def sensitivities():
    rows = []
    base = run("base")
    def take(label, res):
        s = res["summary"]
        rows.append(dict(
            sensitivity=label,
            equity_after_subsidiary_debt=s["equity_after_subsidiary_debt"],
            equity_as_specified=s["equity_as_specified"],
            sum_of_parts_ev=s["sum_of_parts_ev"],
            group_ebitda_y1=s["group_ebitda"][1],
            group_ebitda_y5=s["group_ebitda"][N],
            cube_group_ebitda_y5=s["cube_group_ebitda"][N],
            cube_share_y5=s["cube_group_ebitda"][N] / s["group_ebitda"][N],
            cube_npv=s["cube_npv"],
        ))
    take("base case", base)
    for m in (7.0, 10.0):
        take(f"beverage EV/EBITDA {m}x (base 8.8x, proxy)", run("base", {"bev_mult": m}))
    for m in (7.0, 11.0):
        take(f"property EV/EBITDA {m}x (base 9.0x, assumption)", run("base", {"prop_mult": m}))
    for usd, lab in ((341.0, "Boon Rawd Brewery directory US$341m"), (578.5, "aggregator US$578.5m")):
        take(f"beverage revenue anchor: {lab}", run("base", {"infobel_sbc_usd_m": usd}))
    for sc, lab in ((0.0, "no cube sales"), (0.5, "half volume"), (3.0, "3x volume"), (10.0, "10x volume")):
        take(f"cube volume scale {sc} ({lab})", run("base", {"cube_serv_scale": sc}))
    for cc in ("low", "high"):
        take(f"cube cost case {cc} (rework/53)", run("base", {"cube_cost_case": cc}))
    for dd in (15.0, 90.0):
        take(f"inventory days {int(dd)} (cube and intragroup film)", run("base", {"cube_inv_days": dd}))
    take("holding debt rate +1 pp", run("base", {"rate_shock": 0.01}))
    take("downside case (for reference)", run("downside"))
    return rows


def make_chart(res):
    bg, ink, ink2, grid = "#fcfcfb", "#0b0b0b", "#52514e", "#e1e0d9"
    c_total, c_pos, c_neg = "#52514e", "#2a78d6", "#e34948"
    sp = res["sotp"]
    lines = sp["lines"]
    steps = []
    steps += [(lbl, v / 1000.0, "delta") for lbl, v in [
        ("Beverage\ncore", lines[0]["value"]), ("Cube\n(SOTP)", lines[1]["value"]),
        ("Packaging", lines[2]["value"]), ("Property", lines[3]["value"]), ("Food", lines[4]["value"]),
        ("Holdco\noverhead", lines[5]["value"]), ("Unrealised\nprofit", lines[6]["value"])]]
    steps.append(("Sum of\nparts EV", sp["sum_of_parts_ev"] / 1000.0, "total"))
    steps.append(("Holdco\ncash", sp["holdco_cash_pro_forma"] / 1000.0, "delta"))
    steps.append(("Holdco\ndebt", -sp["holdco_debt_pro_forma"] / 1000.0, "delta"))
    steps.append(("Equity\n(bridge as\nspecified)", sp["equity_as_specified"] / 1000.0, "total"))
    steps.append(("Subsidiary\nnet debt", -sp["subsidiary_net_debt_total"] / 1000.0, "delta"))
    steps.append(("Equity after\nsubsidiary debt", sp["equity_after_subsidiary_debt"] / 1000.0, "total"))

    fig, ax = plt.subplots(figsize=(12, 6.2), facecolor=bg)
    ax.set_facecolor(bg)
    running = 0.0
    xs = range(len(steps))
    for i, (lbl, v, kind) in enumerate(steps):
        if kind == "total":
            bottom, height, color = 0.0, v, c_total
            running = v
        else:
            bottom = running if v >= 0 else running + v
            height = abs(v)
            color = c_pos if v >= 0 else c_neg
            running += v
        ax.bar(i, height, bottom=bottom, color=color, width=0.62, edgecolor=bg, linewidth=2)
        top = bottom + height
        if kind == "total":
            txt = f"{v:.1f}"
        elif abs(v) < 0.005:
            txt = "0.0"
        elif abs(v) < 0.5:
            txt = f"{v:+.2f}"
        else:
            txt = f"{v:+.1f}"
        ax.text(i, top + 0.8, txt, ha="center", va="bottom", color=ink, fontsize=9)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([s[0] for s in steps], fontsize=8, color=ink2)
    ax.set_ylabel("THB bn", color=ink2, fontsize=9)
    ax.tick_params(axis="y", colors=ink2, labelsize=8)
    ax.grid(axis="y", color=grid, linewidth=0.8)
    ax.set_axisbelow(True)
    for sp_ in ("top", "right", "left"):
        ax.spines[sp_].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.axhline(0, color="#c3c2b7", linewidth=0.8)
    ax.set_title("Base case: sum-of-parts bridge to equity (THB bn, proxy inputs)", loc="left",
                 color=ink, fontsize=12, pad=14)
    fig.text(0.01, 0.01,
             "Valuation on Year 1 EBITDA at start of Year 1, pro forma for the packaging acquisition. "
             "Beverage and property inputs are PROXY. Multiples except beverage are ASSUMPTION. "
             "Team-only record, rework/56.",
             fontsize=7.5, color=ink2, ha="left")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
    fig.savefig(OUT_PNG, dpi=150, facecolor=bg)
    plt.close(fig)


def main():
    base = run("base")
    down = run("downside")
    gaps_b = checks(base)
    gaps_d = checks(down)
    sens = sensitivities()
    input_rows = []
    for row in INPUT_LIST:
        input_rows.append(dict(key=row["key"], base=row["base"], downside=row["down"], unit=row["unit"],
                               label=row["label"], source=row["source"], note=row["note"]))
    out = dict(
        basis=("Team-only record (rework/56). Proxy inputs for Boon Rawd / Singha group entities; group-level "
               "figures not reachable. All values in million THB unless stated. Year 0 = base year (proxy FY2025 values); "
               "Years 1-5 are projection years. Volume is a scenario input: rework/55 (consumer study) does not exist."),
        inputs=input_rows,
        cases=dict(base=base, downside=down),
        checks=dict(base=gaps_b, downside=gaps_d),
        sensitivities=sens,
    )
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    make_chart(base)

    def f(x):
        return round(x, 1) if isinstance(x, float) else x
    for name, res in (("BASE", base), ("DOWNSIDE", down)):
        s = res["summary"]
        print(name)
        print("  group EBITDA Y0..Y5:", [round(x) for x in s["group_ebitda"]])
        print("  group revenue Y1, Y5:", round(s["group_revenue"][1]), round(s["group_revenue"][N]))
        print("  cube group EBITDA Y1..Y5:", [round(x, 1) for x in s["cube_group_ebitda"][1:]])
        print("  cube share of group EBITDA Y5: {:.3%}".format(s["cube_group_ebitda"][N] / s["group_ebitda"][N]))
        print("  cube NPV:", round(s["cube_npv"], 1))
        print("  SOTP EV:", round(s["sum_of_parts_ev"]), " equity as specified:", round(s["equity_as_specified"]),
              " equity after sub net debt:", round(s["equity_after_subsidiary_debt"]))
        print("  intercompany P Y1..Y5:", [round(x, 2) for x in res["intercompany"]["film_purchases_at_transfer"][1:]])
        print("  unrealised profit closing Y1..Y5:", [round(x, 3) for x in res["intercompany"]["unrealised_profit_closing"][1:]])
        print("  holdco cash Y0..Y5:", [round(x) for x in res["holding_company"]["cash"]])
        print("  cash available for reinvestment Y1..Y5:", [round(x) for x in res["holding_company"]["cash_available_for_reinvestment"][1:]])
        print("  packaging ROIC Y1..Y5:", [round(x, 3) for x in res["capital_allocation"]["roic"][1:]],
              " breakeven multiple at WACC:", round(res["capital_allocation"]["breakeven_multiple_at_wacc"], 2))
        print("  checks:", {k: float("{:.2e}".format(v)) for k, v in (gaps_b if name == "BASE" else gaps_d).items()})
    print("break-even servings (m) for zero cube EBITDA:", round(base["break_even"]["servings_for_zero_ebitda_m"], 2),
          " for 1% of group EBITDA Y5:", round(base["break_even"]["servings_for_one_pct_of_group_ebitda_m"], 1))
    print("wrote", OUT_JSON)
    print("wrote", OUT_PNG)


if __name__ == "__main__":
    main()
