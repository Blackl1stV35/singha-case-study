"""Estimates derived from public data; not Singha figures.

Task T7 (record rework/70_singha_internal_estimates.md), revised 20 October 2026 after the second independent check.

Seven estimates. Each has a central value, a 90 per cent interval (5th and 95th percentiles of a fixed-seed
Monte Carlo over the stated input ranges, seed 20261020, 200,000 draws), a tier, and two derivations where the
brief asks for them. The intervals are ranges from the stated input bounds, not calibrated statistical intervals.

Price basis. The top-down volume and the price chain use the listing price per can: the mean of the four
multipack per-can prices read on 20 October 2026 (record 68d, S): D06 Makro PRO 24-can THB 13.54; D01 7-Eleven
ALL Online 24-can THB 13.75 (a promotional selling price; the page prints 408 struck through, a minus 19 per cent
badge, a saving of 78, and a promotion valid to 20 October 2026); D12 Lotus's 24-can THB 13.75; D13 Lotus's
six-can THB 14.17. Sensitivity cases: the undiscounted 408 list reading for D01 (THB 17.00 a can, mean 14.615);
the mean of the three readings without the promotional D01 reading (13.82); the single-can online list price of
THB 17.00 (Lotus's, record 68d S01, top of the triangular range); the Lotus's six-can and the Makro PRO 24-can
readings alone.

Excluded: the 7-Eleven six-pack at THB 172 (28.67 a can, record 68d D02) and the Makro PRO six-pack at THB 82
(13.67 a can, one-pack reading not settled, record 70 section 3.1).

Aluminium is NOT an input. The LME route is not authorised (record 69 section 7.4 item 3). The aluminium cost is
reported as a slope (THB a can per USD 100 a tonne) and as the break-even price at which contribution is zero.

Cube (pilot) inputs are the team's planning figures (records 64, 72, submission 05), not sourced.
Binder and flavour are not priced in the cube cost.

Run: python singha_internal_estimates.py   (writes singha_internal_estimates_results.json next to this file)
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "singha_internal_estimates_results.json"
SEED = 20261020
N = 200_000
CAN_L = 0.33

rng = np.random.default_rng(SEED)


def tri(lo, mode, hi, n=N):
    return rng.triangular(lo, mode, hi, n)


def uni(lo, hi, n=N):
    return rng.uniform(lo, hi, n)


def pct(x):
    return {"p5": float(np.percentile(x, 5)), "p50": float(np.percentile(x, 50)),
            "p95": float(np.percentile(x, 95)), "mean": float(np.mean(x))}


# ---------------------------------------------------------------- listing price per can (record 68d, S, read 20 Oct 2026)
MULTIPACK_PRICES = {
    "D06 Makro PRO, Singha Lemon Soda 24-can case, THB 325 for 24 (68d D06)": 13.54,
    "D01 7-Eleven ALL Online, Singha Lemon Soda 24-can case, THB 330 selling price with a promotion "
    "(68d D01; page prints 408 struck through, minus 19 per cent, saving 78, promotion valid to 20 Oct 2026)": 13.75,
    "D12 Lotus's Shop Online, Singha Lemon Soda 24-can case, THB 330 for 24 (68d D12)": 13.75,
    "D13 Lotus's Shop Online, Singha Lemon Soda six-can, THB 85 for 6 (68d D13)": 14.17,
}
_VALS = list(MULTIPACK_PRICES.values())
PRICE_LOW = min(_VALS)                                          # 13.54
PRICE_MODE = round(sum(_VALS) / len(_VALS), 4)                   # 13.8025 (mean of the four readings; central)
PRICE_SINGLE = 17.00                                             # Lotus's online single can (68d S01)
PRICE_D01_LIST = round(408 / 24, 4)                              # 7-Eleven undiscounted list for 24 cans, 17.00 a can
PRICE_408_MEAN = round((_VALS[0] + PRICE_D01_LIST + _VALS[2] + _VALS[3]) / 4, 4)   # 14.615
PRICE_EX_PROMO_MEAN = round((_VALS[0] + _VALS[2] + _VALS[3]) / 3, 4)              # 13.82
PRICE_SIX = 14.17                                                # Lotus's six-can (68d D13)

# ---------------------------------------------------------------- inputs (central value, interval, tier, status, source)
INPUTS = {
    # Market and share (top-down)
    "csd_market_2025_thb_m": {"dist": "tri", "lo": 67000, "mode": 70000, "hi": 76900, "tier": "S", "status": "SOURCED",
                              "source": "Five press values for the carbonated soft-drink market, read as a mix of windows: 67,000 "
                                        "(Bangkokbiznews 13 Oct 2025, 2025, no source named); 68,000 (ThaiBev executive, labelled 2024); "
                                        "70,000 (Marketeer 17 Apr 2026 compilation, NielsenIQ and brand forecasts, 2025); 70,772 (NielsenIQ, "
                                        "12 months to November 2024, as printed by Thansettakij 14 Jan 2025; not used as the mode); "
                                        "76,900 (KResearch, 2025 forecast, via Thansettakij 8 Sep 2025). Central = median = 70,000. "
                                        "The central is not a 2025 actual: it mixes 2024 and 2025 values and one forecast (record 67). "
                                        "The market basis (retail or manufacturer) is not stated"},
    "lemon_soda_share_csd": {"dist": "tri", "lo": 0.015, "mode": 0.0235, "hi": 0.030, "tier": "S", "status": "ASSUMPTION",
                             "source": "Positioning, 4 July 2022 (https://positioningmag.com/strategic-move/88360; saved in "
                                       "rework/raw/diligence_2026-10-20/T7/positioning_2022_07_04_csd_share.md): Singha Lemon Soda 2.4 per cent "
                                       "of total carbonated soft drinks, and 1,450 million baht, given two years after launch. The article's "
                                       "1,450 divided by its 62,725 (2021) is 2.31 per cent. The central 2.35 is the midpoint of the printed and "
                                       "computed shares. The year of the measurement is unresolved: 2021 or 2022 (launch dated August 2020 in "
                                       "record 69, so two years after launch is about 2022). The article's market value is for 2021. The 12 per "
                                       "cent share in the same article does not reconcile (1,450 over 13,172 is 11.0 per cent) and is not used. "
                                       "The band 1.5 to 3.0 per cent is an assumption of change between the measurement and 2025"},
    # Listing price per can (shelf, incl. VAT). Central is the mean of four online readings.
    "listing_price_thb_per_can": {"dist": "tri", "lo": PRICE_LOW, "mode": PRICE_MODE, "hi": PRICE_SINGLE,
                                  "tier": "S", "status": "DERIVED",
                                  "source": "Online retailer listing prices read 20 Oct 2026 (record 68d, S): 13.54 (Makro PRO 24-can), "
                                            "13.75 (7-Eleven ALL Online 24-can, promotional selling price), 13.75 (Lotus's 24-can), 14.17 "
                                            "(Lotus's six-can). Central = mean of these four = 13.80. Top of range = single-can online list price "
                                            "THB 17.00 (Lotus's, S01, read 20 Oct 2026). The mix of pack sizes sold is not sourced, so the central is "
                                            "an unweighted mean. Not a store shelf price (none read)"},
    # Bottom-up
    "stores_7eleven": {"dist": "fixed", "value": 15945, "tier": "P", "status": "SOURCED",
                       "source": "CP ALL listed-company snapshot, year-end 2025 (page prints Published on 24/03/2026; read 20 Oct 2026): 15,945 "
                                 "stores by the end of 2025 (P). Thailand scope inferred, not stated on the page "
                                 "(rework/raw/diligence_2026-10-20/T7/cpall_ye68_publication_date_check_2026-10-20.md)"},
    "stock_share_7eleven": {"dist": "tri", "lo": 0.5, "mode": 0.8, "hi": 1.0, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                            "source": "Share of 7-Eleven stores that stock the 330 mL can. No outlet count published. Assumption bound"},
    "cans_per_store_per_day": {"dist": "tri", "lo": 2.0, "mode": 6.0, "hi": 12.0, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                               "source": "Sales per stocking store per day. No source. Assumption bound. (A 2021 check is indicative only: "
                                         "the 2021 press volume of 28 million litres would be about 7 a store a day if 7-Eleven carried half of it, "
                                         "but no 2021 store count is sourced, so the check is not used)"},
    "seven_eleven_channel_share": {"dist": "tri", "lo": 0.40, "mode": 0.55, "hi": 0.70, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                                   "source": "7-Eleven share of total can volume. No channel split found. Assumption bound"},
    # Price chain
    "vat": {"dist": "fixed", "value": 0.07, "tier": "P", "status": "SOURCED",
            "source": "Revenue Department, rd.go.th/59.html, read 20 Oct 2026: VAT 7 per cent, extended to 30 September 2027 "
                      "(raw/diligence_2026-10-20/T9/rd_vat_7_percent_2026.md)"},
    "retail_margin": {"dist": "tri", "lo": 0.161, "mode": 0.216, "hi": 0.317, "tier": "S", "status": "PROXY",
                      "source": "Retailer gross margin, all categories, FY2025: CP Axtra 16.1, BJC (Big C) 21.6, CRC 31.7 per cent "
                                "(stockanalysis aggregator, S; raw/diligence_2026-10-20/T4/retail_groups_financials_stockanalysis_2026-10-20.md). "
                                "Mode = the median of the three group values (Big C is the middle value). Group-wide, not beverage-specific. "
                                "No 7-Eleven operator margin read (CP ALL margin: open, stated limit)"},
    "distributor_margin": {"dist": "tri", "lo": 0.10, "mode": 0.15, "hi": 0.20, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                           "source": "UNSOURCED ASSUMPTION. No Thai beverage distributor margin was read. The 10 to 20 per cent band is the "
                                     "team's assumption (records 53, 76, submission 10). Open: the distributor search could not be run this turn "
                                     "(web search budget used up)"},
    "excise_ad_valorem": {"dist": "fixed", "value": 0.14, "tier": "P", "status": "SOURCED",
                          "source": "Royal Gazette item 02.02, 14 per cent ad valorem, P as saved (raw/gazette_sugar_drink_excise_primary_2560_A095_111.md). "
                                    "The saved text was read from page images; a second reader should check the Thai numerals before public use; "
                                    "later amendments were not searched. Base not read: the Gazette PDF returned HTTP 403 on 20 Oct 2026. "
                                    "Applied to the ex-VAT invoice (ASSUMPTION)"},
    # Variable cost (non-aluminium lines, from records 58 and 61, reused)
    "fx_thb_per_usd": {"dist": "uni", "lo": 33.3535, "hi": 33.7455, "tier": "P", "status": "SOURCED",
                       "source": "Bank of Thailand, 15 Oct 2026: buying sight 33.3535 and selling transfer 33.7455 (saved copy, P as saved). "
                                 "Not re-verified on 20 Oct 2026: the BOT page read that day prints no rate table"},
    "sheet_g_per_can": {"dist": "uni", "lo": 14.4, "hi": 18.5, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                        "source": "Aluminium sheet mass per 330 mL can. No maker's spec found. Assumption bound (records 58, 61)"},
    "conversion_nonmetal_usd": {"dist": "uni", "lo": 0.04, "hi": 0.08, "tier": "S", "status": "PROXY",
                                "source": "Non-metal can conversion (labour, energy, coating and printing in one proxy), US 2024 consultancy "
                                          "figure (record 58, S). Proxy for a Thai line"},
    "filling_usd": {"dist": "uni", "lo": 0.001, "hi": 0.004, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                    "source": "Filling consumables. Asian can-factory project profile (S) used as an assumption bound (record 61)"},
    "seaming_usd": {"dist": "uni", "lo": 0.0001, "hi": 0.0005, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                    "source": "Seaming. Seamer vendor page used as an assumption bound (record 61)"},
    "co2_usd": {"dist": "uni", "lo": 0.0003, "hi": 0.0018, "tier": "S", "status": "PROXY",
                "source": "Carbon dioxide for carbonation: CO2 price news (S), a proxy (record 58); the high excludes a 50 per cent purge loss"},
    "liquid_usd": {"dist": "uni", "lo": 0.027, "hi": 0.040, "tier": "S", "status": "ASSUMPTION",
                   "source": "Sugar-and-flavour liquid line, built on a sugar proxy (record 61). The Lemon Soda uses a sugar-free sweetener system; "
                             "no sweetener price sourced"},
    # Cube (pilot) inputs: team planning figures
    "cube_cost_per_cube_thb": {"dist": "fixed", "value": 4.09, "tier": "DERIVED", "status": "DERIVED",
                               "source": "Six-cube carton cost per cube, THB 4.09 (records 64, 72, submission 05). Binder and flavour not priced"},
    "cube_ex_factory_model_thb": {"dist": "fixed", "value": 9.00, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                                  "source": "60 per cent of a THB 15 shelf price (submission 05). Team assumption. Before excise"},
    "cube_shelf_model_thb": {"dist": "fixed", "value": 15.0, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                             "source": "Planning shelf price (submission 05). Not benchmarked. Record 68d: THB 15 sits 9.1 per cent above the "
                                       "sourced 24-can Lemon Soda price (13.75) and 6.8 per cent below the single-can median (16.25 to 18.00 range)"},
    "pilot_fixed_cost_thb": {"dist": "fixed", "value": 500000, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                             "source": "Base fixed cost of the pilot, THB 500,000 a year (submission 05 and 11)"},
    "pilot_npv_breakeven_cubes_model": {"dist": "fixed", "value": 146230, "tier": "DERIVED", "status": "DERIVED",
                                        "source": "Model NPV break-even at THB 500,000 fixed cost (record 05; five years, 10 per cent, pre-tax)"},
    # Capacity anchors
    "group_nameplate_ml": {"dist": "fixed", "value": 1000.0, "tier": "PROXY", "status": "PROXY",
                           "source": "Group nameplate, million litres a year (record 61; Wikipedia and a 2012 news report; scope unclear)"},
    "canned_share_proxy": {"dist": "fixed", "value": 0.553, "tier": "S", "status": "PROXY",
                           "source": "Canned share of output, a Vietnamese peer (record 58, S)"},
    "tbc_capacity_cans_m": {"dist": "fixed", "value": 3880, "tier": "P", "status": "SOURCED",
                            "source": "Thai Beverage Can, BJC One Report 2025, maximum capacity 2025 (raw/diligence_2026-10-20/T6/08)"},
    "tbc_actual_cans_m": {"dist": "fixed", "value": 2307, "tier": "P", "status": "SOURCED",
                          "source": "Thai Beverage Can, output 2025 (same source)"},
    "bangrenlen_ml": {"dist": "fixed", "value": 925.0, "tier": "S", "status": "SOURCED",
                      "source": "Singha Beverage, Bang Len plant: 'currently has a capacity of 925 million litres a year' (Boon Rawd plant history page, undated; no mention of cans)"},
    # Singha Corporation (press; not filings)
    "sing_corp_revenue_2025_thb_m": {"dist": "fixed", "value": 3892.0, "tier": "S", "status": "SOURCED",
                                     "source": "MGR Online, 23 May 2026 (no source named): total revenue THB 3,892 million, printed with the year 2568 (2025)"},
    "sing_corp_net_profit_2025_thb_m": {"dist": "fixed", "value": 3085.0, "tier": "S", "status": "SOURCED",
                                        "source": "Same article: net profit THB 3,085 million, printed in the same sentence with the year 2568 (2025). No source named"},
    # Co-packer
    "moq_low_units": {"dist": "fixed", "value": 500000, "tier": "COMPANY CLAIM", "status": "SOURCED",
                      "source": "Arnifo OEM beverage page, https://www.arnifo.com/oem-beverage/, read 20 Oct 2026 by WebFetch (extract, not full text): "
                                "MOQ 500,000 to 1,500,000 per SKU and formula, phased within 12 months; the page also lists a pilot batch step and "
                                "states no small trial, pilot or pre-commercial sales production (raw/diligence_2026-10-20/T7/arnifo_oem_moq_recheck_2026-10-20.md)"},
    "moq_high_units": {"dist": "fixed", "value": 1500000, "tier": "COMPANY CLAIM", "status": "SOURCED", "source": "Same page"},
    # Line speed (no source; assumption bounds)
    "pouch_line_efficiency": {"dist": "fixed", "value": 0.70, "tier": "ASSUMPTION", "status": "ASSUMPTION",
                              "source": "Overall line efficiency. No source (open: line speed search not run this turn)"},
    "cube_serve_khco3_g": {"dist": "fixed", "value": 0.81, "tier": "DERIVED", "status": "DERIVED",
                           "source": "Team specification: potassium bicarbonate 0.81 g per 330 mL serve (record 72)"},
    "cube_serve_citric_g": {"dist": "fixed", "value": 2.10, "tier": "DERIVED", "status": "DERIVED",
                            "source": "Team specification: citric acid 2.10 g per serve (record 72)"},
}

# Peer gross margins (saved records; latest year). Brand owner, bottler and retailer roles are not comparable.
PEERS = [
    {"entity": "The Coca-Cola Company (brand owner), FY2025", "gm": 0.616, "tier": "P", "where": "record 68a section 6.1"},
    {"entity": "PepsiCo (brand owner and franchisor, global), FY2025", "gm": 0.5415, "tier": "P, DERIVED", "where": "record 68b section 7.2"},
    {"entity": "ThaiNamthip (Coca-Cola bottler), FY2024, on sales of goods", "gm": 0.385, "tier": "P, DERIVED", "where": "record 68a section 6.2"},
    {"entity": "Haad Thip (Coca-Cola bottler, South), FY2025", "gm": 0.422, "tier": "P", "where": "record 68a section 6.3"},
    {"entity": "Sermsuk (soft drink maker and bottler), FY2024", "gm": 0.2925, "tier": "P, DERIVED", "where": "record 68b section 7.1"},
    {"entity": "ThaiBev non-alcoholic segment (group segment), FY2025", "gm": 0.3658, "tier": "P, DERIVED", "where": "record 68c section 5.3"},
    {"entity": "Osotspa (whole company, four segments), FY2025", "gm": 0.401, "tier": "P (company page; year end S)", "where": "record 68c section 5.1"},
]


def draw(name):
    spec = INPUTS[name]
    if spec["dist"] == "tri":
        return tri(spec["lo"], spec["mode"], spec["hi"])
    if spec["dist"] == "uni":
        return uni(spec["lo"], spec["hi"])
    return np.full(N, float(spec["value"]))


def central(name):
    spec = INPUTS[name]
    if spec["dist"] == "tri":
        return float(spec["mode"])
    if spec["dist"] == "uni":
        return float((spec["lo"] + spec["hi"]) / 2)
    return float(spec["value"])


def net_price(price, vat, retail, dist, excise):
    """Maker invoice = price / (1 + VAT) x (1 - retail margin) x (1 - distributor margin); net = invoice x (1 - excise)."""
    invoice = price / (1.0 + vat) * (1.0 - retail) * (1.0 - dist)
    net = invoice * (1.0 - excise)
    return invoice, net


def nonaluminium_usd(conv, fill, seam, co2, liquid):
    """Non-aluminium variable cost per can in USD: conversion, filling, seaming, CO2 and the liquid."""
    return conv + fill + seam + co2 + liquid


def main():
    res = {"basis": "Estimates derived from public data; not Singha figures.",
           "run": {"seed": SEED, "draws": N,
                   "method": "fixed-seed Monte Carlo over the triangular and uniform inputs; central values use the modes and midpoints; "
                             "90 per cent intervals are the 5th and 95th percentiles of the draws, i.e. ranges from the stated input bounds, "
                             "not calibrated statistical intervals",
                   "price_basis": "listing price per can = mean of four online multipack prices read 20 Oct 2026 (record 68d); the D01 reading "
                                  "is a promotional selling price (408 struck through). Sensitivity cases are in price_cases."},
           "inputs": INPUTS,
           "price_points": {"multipack_prices_thb_per_can": MULTIPACK_PRICES, "central_mean_of_four": PRICE_MODE,
                            "lowest_reading": PRICE_LOW, "single_can_online_list_thb": PRICE_SINGLE,
                            "d01_undiscounted_list_thb_per_can": PRICE_D01_LIST,
                            "mean_of_four_with_d01_at_undiscounted_list": PRICE_408_MEAN,
                            "mean_of_three_excluding_promotional_d01": PRICE_EX_PROMO_MEAN,
                            "lotus_six_can_thb_per_can": PRICE_SIX}}

    # ---------------------------------------------------------- central values (deterministic)
    c = {k: central(k) for k in INPUTS}
    price_c = c["listing_price_thb_per_can"]
    inv_c, net_c = net_price(price_c, c["vat"], c["retail_margin"], c["distributor_margin"], c["excise_ad_valorem"])
    _, net_single_c = net_price(PRICE_SINGLE, c["vat"], c["retail_margin"], c["distributor_margin"], c["excise_ad_valorem"])
    fx = c["fx_thb_per_usd"]
    sheet_c = c["sheet_g_per_can"]
    nonal_usd_c = nonaluminium_usd(c["conversion_nonmetal_usd"], c["filling_usd"], c["seaming_usd"], c["co2_usd"], c["liquid_usd"])
    nonal_thb_c = nonal_usd_c * fx
    contrib_pre_c = net_c - nonal_thb_c
    gm_pre_c = contrib_pre_c / net_c
    alu_per_100usd_t_c = sheet_c * 100.0 / 1e6 * fx          # THB a can per USD 100 a tonne
    alu_breakeven_c = contrib_pre_c * 1e6 / (sheet_c * fx)   # USD a tonne at which contribution is zero

    cans_td_c = c["csd_market_2025_thb_m"] * 1e6 * c["lemon_soda_share_csd"] / price_c
    cans_bu_c = (c["stores_7eleven"] * c["stock_share_7eleven"] * c["cans_per_store_per_day"] * 365.0
                 / c["seven_eleven_channel_share"])
    retail_val_c = c["csd_market_2025_thb_m"] * c["lemon_soda_share_csd"]     # THB million, retail basis assumed
    rev_td_c = cans_td_c * net_c / 1e6
    rev_bu_c = cans_bu_c * net_c / 1e6
    ctb_td_c = cans_td_c * contrib_pre_c / 1e6
    ctb_bu_c = cans_bu_c * contrib_pre_c / 1e6
    chain_ratio_c = net_c / price_c                            # net per can / listing price

    # ---------------------------------------------------------- Monte Carlo draws (main block; order unchanged from the earlier run)
    d = {k: draw(k) for k in INPUTS}
    price = d["listing_price_thb_per_can"]
    inv, net = net_price(price, d["vat"], d["retail_margin"], d["distributor_margin"], d["excise_ad_valorem"])
    nonal_thb = nonaluminium_usd(d["conversion_nonmetal_usd"], d["filling_usd"], d["seaming_usd"], d["co2_usd"],
                                 d["liquid_usd"]) * d["fx_thb_per_usd"]
    contrib = net - nonal_thb
    cans_td = d["csd_market_2025_thb_m"] * 1e6 * d["lemon_soda_share_csd"] / price
    cans_bu = (d["stores_7eleven"] * d["stock_share_7eleven"] * d["cans_per_store_per_day"] * 365.0
               / d["seven_eleven_channel_share"])
    retail_val = d["csd_market_2025_thb_m"] * d["lemon_soda_share_csd"]
    rev_td = cans_td * net / 1e6
    rev_bu = cans_bu * net / 1e6
    ctb_td = cans_td * contrib / 1e6
    ctb_bu = cans_bu * contrib / 1e6
    share_rev_td = rev_td / d["sing_corp_revenue_2025_thb_m"]
    share_rev_bu = rev_bu / d["sing_corp_revenue_2025_thb_m"]
    share_np_td = ctb_td / d["sing_corp_net_profit_2025_thb_m"]
    share_np_bu = ctb_bu / d["sing_corp_net_profit_2025_thb_m"]
    alu_breakeven = contrib * 1e6 / (d["sheet_g_per_can"] * d["fx_thb_per_usd"])
    alu_per_100 = d["sheet_g_per_can"] * 100.0 / 1e6 * d["fx_thb_per_usd"]

    # cube net per cube under the two price bases, and the cube contribution (THB per cube)
    cube_cost = c["cube_cost_per_cube_thb"]
    cube_model_contrib_c = c["cube_ex_factory_model_thb"] - cube_cost                     # 4.91, before excise, model basis
    _, cube_chain15_net_c = net_price(c["cube_shelf_model_thb"], c["vat"], c["retail_margin"], c["distributor_margin"],
                                      c["excise_ad_valorem"])
    cube_chain15_contrib_c = cube_chain15_net_c - cube_cost                               # 3.94, after excise
    cube_parity_contrib_c = net_c - cube_cost                                             # cube sold at the can's listing price
    cube_chain15_contrib = (net_price(d["cube_shelf_model_thb"], d["vat"], d["retail_margin"], d["distributor_margin"],
                                      d["excise_ad_valorem"])[1] - d["cube_cost_per_cube_thb"])
    cube_parity_contrib = net - d["cube_cost_per_cube_thb"]

    # ---------------------------------------------------------- extra draws (after the main block, so earlier draws are unchanged)
    speed = tri(20.0, 60.0, 120.0)            # pouches a minute: ASSUMPTION (triangular, mode at the central 60)
    eff = uni(0.50, 0.85)                     # overall line efficiency: ASSUMPTION
    moq = uni(c["moq_low_units"], c["moq_high_units"])   # co-packer minimum: COMPANY CLAIM range

    # ---------------------------------------------------------- estimate 1: cans and revenue
    res["estimate_1_can_volume_and_revenue"] = {
        "top_down_cans_central_modal": round(cans_td_c),
        "top_down_cans_90": {k: round(v) for k, v in pct(cans_td).items()},
        "bottom_up_cans_central": round(cans_bu_c),
        "bottom_up_cans_90": {k: round(v) for k, v in pct(cans_bu).items()},
        "bottom_up_to_top_down_ratio_central": round(cans_bu_c / cans_td_c, 3),
        "top_down_cans_at_single_can_17_central": round(c["csd_market_2025_thb_m"] * 1e6 * c["lemon_soda_share_csd"] / PRICE_SINGLE),
        "top_down_cans_at_408_mean_central": round(c["csd_market_2025_thb_m"] * 1e6 * c["lemon_soda_share_csd"] / PRICE_408_MEAN),
        "top_down_cans_at_ex_promo_mean_central": round(c["csd_market_2025_thb_m"] * 1e6 * c["lemon_soda_share_csd"] / PRICE_EX_PROMO_MEAN),
        "top_down_cans_at_low_13_54_central": round(c["csd_market_2025_thb_m"] * 1e6 * c["lemon_soda_share_csd"] / PRICE_LOW),
        "retail_value_top_down_thb_m_central": round(retail_val_c, 1),
        "retail_value_top_down_thb_m_90": {k: round(v, 1) for k, v in pct(retail_val).items()},
        "net_revenue_top_down_thb_m_central": round(rev_td_c, 1),
        "net_revenue_top_down_thb_m_90": {k: round(v, 1) for k, v in pct(rev_td).items()},
        "net_revenue_bottom_up_thb_m_central": round(rev_bu_c, 1),
        "net_revenue_bottom_up_thb_m_90": {k: round(v, 1) for k, v in pct(rev_bu).items()},
        "identity_note": "Top-down net revenue = retail value x (net per can / listing price). The price level cancels, so the "
                         "top-down revenue does not depend on which price is chosen; the price choice moves cans and the per-can economics.",
        "overlap_of_90_intervals_cans": bool(np.percentile(cans_bu, 95) >= np.percentile(cans_td, 5)),
        "check_2021_press_volume_cans_m": round(28e6 / CAN_L / 1e6, 2),
        "check_2021_press_value_at_16_thb_m_derived": round(28e6 / CAN_L * 16 / 1e6, 1),
        "check_2021_press_value_thb_m_printed_in_T6_09_no_year": 1357,
        "check_2021_value_note": "The 1,357 million figure has no year printed in the saved text (T6/09). It equals the press volume of 28 million "
                                 "litres at THB 16 a can to within 0.04 per cent, so it may be a derived value, not an independent sales figure.",
        "check_positioning_value_thb_m_printed": 1450,
        "check_1450_vs_1357_gap_pct": round((1450 / 1357 - 1) * 100, 2),
        "check_2022_positioning_share_printed_vs_computed": {"printed_pct": 2.4, "computed_pct_of_62725": round(1450 / 62725 * 100, 2),
                                                            "computed_pct_of_13172_canned": round(1450 / 13172 * 100, 2),
                                                            "printed_12_pct_of_13172": round(0.12 * 13172, 1)},
        "basis_note": "Market value level (retail or manufacturer) is not stated by any source; retail basis assumed. "
                      "A manufacturer-value basis would lower the top-down cans. Not modelled as a separate case (stated limit).",
    }

    # ---------------------------------------------------------- estimate 2: share of Singha Corporation
    res["estimate_2_share_of_singha_corporation"] = {
        "singha_corp_revenue_2025_thb_m": c["sing_corp_revenue_2025_thb_m"],
        "singha_corp_net_profit_2025_thb_m": c["sing_corp_net_profit_2025_thb_m"],
        "share_of_revenue_top_down_central": round(rev_td_c / c["sing_corp_revenue_2025_thb_m"], 4),
        "share_of_revenue_top_down_90": {k: round(v, 4) for k, v in pct(share_rev_td).items()},
        "share_of_revenue_bottom_up_central": round(rev_bu_c / c["sing_corp_revenue_2025_thb_m"], 4),
        "share_of_revenue_bottom_up_90": {k: round(v, 4) for k, v in pct(share_rev_bu).items()},
        "share_of_net_profit_top_down_central": round(ctb_td_c / c["sing_corp_net_profit_2025_thb_m"], 4),
        "share_of_net_profit_top_down_90": {k: round(v, 4) for k, v in pct(share_np_td).items()},
        "share_of_net_profit_bottom_up_central": round(ctb_bu_c / c["sing_corp_net_profit_2025_thb_m"], 4),
        "share_of_net_profit_bottom_up_90": {k: round(v, 4) for k, v in pct(share_np_bu).items()},
        "caveat": "Conditional shares: they hold only if Singha Corporation booked the can. The booking entity is not identified. "
                  "Press figures; no source named. The article prints the year 2568 (2025) for both revenue and net profit in the same sentence. "
                  "Net profit share uses contribution before aluminium, labour, overhead, depreciation and tax, so it is not like for like "
                  "with net profit. The two derivations share the same can volume, so they are not independent of estimate 1.",
    }

    # ---------------------------------------------------------- estimate 3: variable cost and price chain
    bottlers = [p for p in PEERS if "bottler" in p["entity"] or "maker" in p["entity"]]
    cogs_rows = []
    for p in bottlers:
        cogs = (1.0 - p["gm"]) * net_c
        cogs_rows.append({"entity": p["entity"], "gross_margin": p["gm"],
                          "implied_full_cost_thb_per_can": round(cogs, 3),
                          "room_for_aluminium_and_fixed_cost_thb": round(cogs - nonal_thb_c, 3)})
    res["estimate_3_variable_cost_and_price"] = {
        "listing_price_central_thb_per_can": round(price_c, 4),
        "listing_price_range_thb_per_can": [PRICE_LOW, PRICE_SINGLE],
        "vat": c["vat"], "retail_margin_central": c["retail_margin"], "distributor_margin_central": c["distributor_margin"],
        "distributor_margin_status": "UNSOURCED ASSUMPTION (open)",
        "excise_ad_valorem": c["excise_ad_valorem"],
        "invoice_before_excise_central_thb": round(inv_c, 3),
        "invoice_before_excise_90": {k: round(v, 3) for k, v in pct(inv).items()},
        "net_after_excise_central_thb": round(net_c, 3),
        "net_after_excise_90": {k: round(v, 3) for k, v in pct(net).items()},
        "invoice_as_share_of_listing_price_central": round(inv_c / price_c, 4),
        "variable_cost_excl_aluminium_central_thb": round(nonal_thb_c, 3),
        "variable_cost_excl_aluminium_90": {k: round(v, 3) for k, v in pct(nonal_thb).items()},
        "aluminium_thb_per_can_per_usd_100_per_tonne_central": round(alu_per_100usd_t_c, 4),
        "aluminium_thb_per_can_per_usd_100_per_tonne_90": {k: round(v, 4) for k, v in pct(alu_per_100).items()},
        "aluminium_zero_contribution_price_usd_per_tonne_central": round(alu_breakeven_c, 0),
        "aluminium_zero_contribution_price_usd_per_tonne_90": {k: round(v, 0) for k, v in pct(alu_breakeven).items()},
        "zero_contribution_formula": "(net revenue after VAT, margins and excise, less all non-aluminium variable cost) divided by "
                                     "(sheet mass times FX); no aluminium price used",
        "contribution_pre_aluminium_central_thb": round(contrib_pre_c, 3),
        "contribution_pre_aluminium_90": {k: round(v, 3) for k, v in pct(contrib).items()},
        "single_can_17_case": {
            "net_after_excise_thb": round(net_single_c, 3),
            "contribution_pre_aluminium_thb": round(net_single_c - nonal_thb_c, 3),
            "aluminium_zero_contribution_price_usd_per_tonne": round((net_single_c - nonal_thb_c) * 1e6 / (sheet_c * fx), 0)},
        "superseded_model_value_thb_per_can": {"mid": 4.94, "range": [3.73, 6.14],
                                               "note": "records 58 and 61 model; includes aluminium at the 19 October saved LME reading, which "
                                                       "is not authorised. Superseded by the non-aluminium cost above and the aluminium slope"},
        "derivation_A": "Component build from records 58 and 61 with the aluminium line removed (bottom-up).",
        "derivation_B_status": "NOT an independent cost derivation. Peer full-cost check: each peer's full cost per can implied by its gross "
                               "margin on the same net price. Peer margins include fixed production cost and are on sales of goods. The check "
                               "shows the room left for aluminium and fixed cost; it does not test the component build. Stated limit: no "
                               "independent second cost source for the can's non-aluminium cost was found.",
        "top_down_cost_check": {
            "rows": cogs_rows},
        "note": "Variable cost only. Excludes labour, overhead, depreciation, freight, distributor and marketing costs. Not comparable with full-cost peer margins.",
    }

    # ---------------------------------------------------------- estimate 4: margin against peers (two derivations, different bases)
    peer_median = float(np.median([p["gm"] for p in PEERS]))
    cogs_median_c = (1.0 - peer_median) * net_c
    room_median_c = cogs_median_c - nonal_thb_c
    room_median_90 = pct((1.0 - peer_median) * net - nonal_thb)
    res["estimate_4_margin_vs_peers"] = {
        "derivation_A_bottom_up_variable_margin": {
            "can_gross_margin_pre_aluminium_central": round(gm_pre_c, 4),
            "can_gross_margin_pre_aluminium_90": {k: round(v, 4) for k, v in pct(contrib / net).items()},
            "contribution_pre_aluminium_central_thb": round(contrib_pre_c, 3)},
        "derivation_B_top_down_peer_implied": {
            "peer_median_gross_margin": round(peer_median, 4),
            "implied_full_cost_per_can_at_peer_median_thb": round(cogs_median_c, 3),
            "room_for_aluminium_and_fixed_cost_at_peer_median_thb_central": round(room_median_c, 3),
            "room_for_aluminium_and_fixed_cost_at_peer_median_thb_90": {k: round(v, 3) for k, v in room_median_90.items()},
            "read": "Different bases: A is variable margin on the can; B is a full-cost margin implied by the peers. B is a basis check, "
                    "not a second estimate of the same quantity. The room at the peer median is the amount left for aluminium and fixed cost. "
                    "It is not a threshold."},
        "peers": [{"entity": p["entity"], "gross_margin": p["gm"], "tier": p["tier"], "where": p["where"]} for p in PEERS],
        "peer_median": peer_median,
        "peer_bottler_mean": float(np.mean([p["gm"] for p in PEERS if "bottler" in p["entity"] or "maker" in p["entity"]])),
        "read": "The can margin is variable only and is not a ranking against brand owners, bottlers or retailers. A full-cost can margin would be lower."}

    # ---------------------------------------------------------- estimate 5: capacity and co-packer
    nameplate_cans_m = c["group_nameplate_ml"] * 1e6 * c["canned_share_proxy"] / CAN_L / 1e6
    util_tbc = c["tbc_actual_cans_m"] / c["tbc_capacity_cans_m"]
    used_cans_m = nameplate_cans_m * util_tbc
    unused_cans_m = nameplate_cans_m - used_cans_m
    avail = {"two shifts, 250 days (ASSUMPTION)": 4000.0, "24 hours, 365 days (ASSUMPTION)": 8760.0}
    speeds = [20, 60, 120]
    volumes = [200000, 500000, 1000000]
    grid = []
    for v in volumes:
        for s in speeds:
            hours = v / (s * 60.0 * c["pouch_line_efficiency"])
            grid.append({"cubes_per_year": v, "pouches_per_min_assumed": s, "line_hours": round(hours, 1),
                         "pct_of_4000_h": round(hours / 4000 * 100, 2), "pct_of_8760_h": round(hours / 8760 * 100, 2)})
    headroom_90 = {}
    for v in [200000, 1000000]:
        hrs = v / (speed * 60.0 * eff)
        headroom_90[str(v)] = {
            "line_hours_90": {k: round(x, 1) for k, x in pct(hrs).items()},
            "pct_of_4000_h_90": {k: round(x, 2) for k, x in pct(hrs / 4000 * 100).items()},
            "pct_of_8760_h_90": {k: round(x, 2) for k, x in pct(hrs / 8760 * 100).items()},
            "draws": "pouches a minute triangular 20 to 60 to 120 (ASSUMPTION); efficiency uniform 0.50 to 0.85 (ASSUMPTION)"}
    moq_years_90 = {str(v): {"years_to_fill_co_packer_minimum_90": {k: round(x, 2) for k, x in pct(moq / v).items()}}
                    for v in [200000, 1000000]}
    res["estimate_5_line_capacity"] = {
        "derivation_A_count_basis_top_down_proxy": {
            "group_nameplate_cans_m_proxy": round(nameplate_cans_m, 1),
            "group_can_output_at_59_46_pct_use_m_proxy": round(used_cans_m, 1),
            "unused_can_slots_m_proxy": round(unused_cans_m, 1),
            "cube_volume_as_pct_of_nameplate": {str(v): round(v / (nameplate_cans_m * 1e6) * 100, 4) for v in volumes},
            "cube_volume_as_pct_of_unused_slots": {str(v): round(v / (unused_cans_m * 1e6) * 100, 4) for v in volumes},
            "interval": "No interval: the nameplate is a proxy whose scope is unknown, so no bounds can be stated without inventing them. Point values only.",
            "read": "A count of can slots, not a line hour. It treats a cube as one can slot. Shown for scale only; it is not an independent "
                    "derivation of the line-time figure."},
        "derivation_B_line_hours_bottom_up": {
            "grid": grid,
            "available_hours": avail,
            "headroom_90": headroom_90,
            "read": "Line hours from assumed speeds and efficiency. No speed for any can or pouch line is sourced (open)."},
        "tbc_capacity_cans_m": c["tbc_capacity_cans_m"],
        "tbc_actual_cans_m": c["tbc_actual_cans_m"],
        "tbc_utilisation": round(util_tbc, 4),
        "tbc_singha_customer_note": "Thai Beverage Can's filing names Singha Beverage Co., Ltd. as one of five main domestic customers, with no product or plant named (P, BJC One Report 2025; record 69)",
        "bang_len_ml_undated_s": c["bangrenlen_ml"],
        "lemon_soda_top_down_share_of_nameplate_cans": round(cans_td_c / 1e6 / nameplate_cans_m, 4),
        "co_packer_moq_years_to_fill": {str(v): {"moq_500k_years": round(c["moq_low_units"] / v, 2),
                                                 "moq_1500k_years": round(c["moq_high_units"] / v, 2)} for v in volumes},
        "co_packer_moq_years_90_range_uniform_moq": moq_years_90,
        "dry_solids_kg_per_year": {str(v): {"khco3_kg": round(v * c["cube_serve_khco3_g"] / 1000, 1),
                                            "citric_kg": round(v * c["cube_serve_citric_g"] / 1000, 1)} for v in volumes},
        "read": "No pouch, sachet or dry-solids line is evidenced at any group company. Line time is small at the assumed speeds. "
                "The co-packer minimum run (500,000 to 1,500,000 per SKU and formula) binds before line time does."}

    # ---------------------------------------------------------- estimate 6: cannibalisation (intervals drawn; A and B are not independent)
    rows = []
    at_risk_90 = {}
    for v in [200000, 1000000]:
        for s in [0.25, 0.50]:
            displaced = v * s
            key = f"{v}_cubes_{int(s*100)}pct"
            at_risk_90[key] = {
                "cans_displaced": round(displaced),
                "gross_can_contribution_at_risk_thb_90": {k: round(x) for k, x in pct(displaced * contrib).items()},
                "net_change_zero_aluminium_cube_at_planning_15_thb_90": {k: round(x) for k, x in pct(displaced * (cube_chain15_contrib - contrib)).items()},
                "net_change_zero_aluminium_cube_at_listing_price_parity_thb_90": {k: round(x) for k, x in pct(displaced * (cube_parity_contrib - contrib)).items()}}
            rows.append({
                "cubes_per_year": v, "share_from_existing_can_buyers": s,
                "cans_displaced": round(displaced),
                "gross_can_contribution_at_risk_thb_upper_bound_central": round(displaced * contrib_pre_c),
                "net_change_zero_aluminium_cube_at_planning_15_thb_central": round(displaced * (cube_chain15_contrib_c - contrib_pre_c)),
                "net_change_zero_aluminium_cube_at_listing_price_parity_thb_central": round(displaced * (cube_parity_contrib_c - contrib_pre_c)),
                "displaced_as_pct_of_top_down_can_volume": round(displaced / cans_td_c * 100, 4),
                "displaced_as_pct_of_bottom_up_can_volume": round(displaced / cans_bu_c * 100, 4)})
    res["estimate_6_cannibalisation"] = {
        "can_contribution_pre_aluminium_central_thb_per_can": round(contrib_pre_c, 3),
        "cube_contribution_thb_per_cube": {
            "model_basis_ex_factory_9_00_before_excise": round(cube_model_contrib_c, 3),
            "chain_at_planning_price_15_after_excise": round(cube_chain15_contrib_c, 3),
            "parity_at_can_listing_price_after_excise": round(cube_parity_contrib_c, 3)},
        "gap_per_switched_unit_zero_aluminium_thb": {
            "cube_at_15_minus_can": round(cube_chain15_contrib_c - contrib_pre_c, 3),
            "cube_at_parity_minus_can": round(cube_parity_contrib_c - contrib_pre_c, 3)},
        "aluminium_price_above_which_a_switch_does_not_lower_contribution_usd_t": {
            "cube_at_15_central": round((contrib_pre_c - cube_chain15_contrib_c) * 1e6 / (sheet_c * fx), 0),
            "cube_at_15_90": {k: round(v, 0) for k, v in pct((contrib - cube_chain15_contrib) * 1e6 / (d["sheet_g_per_can"] * d["fx_thb_per_usd"])).items()},
            "cube_at_parity_central": round((contrib_pre_c - cube_parity_contrib_c) * 1e6 / (sheet_c * fx), 0),
            "cube_at_parity_90": {k: round(v, 0) for k, v in pct((contrib - cube_parity_contrib) * 1e6 / (d["sheet_g_per_can"] * d["fx_thb_per_usd"])).items()}},
        "rows": rows,
        "at_risk_intervals_90": at_risk_90,
        "derivations": "A: displaced cans times can contribution, as a share of top-down can volume. B: the same ratio on bottom-up can volume. "
                       "A and B are the same ratio on two denominators, so they are NOT independent derivations. The independent check is the "
                       "net-change calculation (cube contribution minus can contribution), which uses a separate cube cost and price. Stated limit: "
                       "no independent source for the share of cube buyers who are existing can buyers was found.",
        "read": "Gross at-risk figures are upper bounds because the can contribution excludes aluminium. The net change is the cube "
                "contribution minus the can contribution on each switched unit. The cube cost excludes binder and flavour, which are not priced, "
                "and the cube's planning price of THB 15 is an assumption. 1:1 switch is an assumption."}

    # ---------------------------------------------------------- estimate 7: pilot fixed cost (two bases; basis stated)
    fixed = c["pilot_fixed_cost_thb"]
    be_model = fixed / cube_model_contrib_c
    be_chain = fixed / cube_chain15_contrib_c
    be_parity = fixed / cube_parity_contrib_c
    res["estimate_7_pilot_fixed_cost_fit"] = {
        "fixed_cost_base_thb": fixed,
        "headline_steady_state_breakeven_cubes": round(be_chain),
        "headline_basis": "chain basis: planning price THB 15 through the same VAT, margin and excise chain, after excise, less THB 4.09",
        "headline_90": {k: round(v) for k, v in pct(fixed / cube_chain15_contrib).items() if k in ("p5", "p95")},
        "derivation_A_model_basis_ex_factory_9_00_BEFORE_EXCISE": {
            "contribution_per_cube_thb": round(cube_model_contrib_c, 3),
            "steady_state_breakeven_cubes": round(be_model),
            "status": "Before excise, so not on the same basis as the chain figure. Shown for reconciliation with submission 05 only; not in judge-facing ranges.",
            "coverage_at_200k_x": round(200000 * cube_model_contrib_c / fixed, 2),
            "coverage_at_50k_x": round(50000 * cube_model_contrib_c / fixed, 2)},
        "derivation_B_chain_basis_planning_price_15_after_excise": {
            "contribution_per_cube_thb": round(cube_chain15_contrib_c, 3),
            "steady_state_breakeven_cubes": round(be_chain),
            "steady_state_breakeven_cubes_90": {k: round(v) for k, v in pct(fixed / cube_chain15_contrib).items()},
            "coverage_at_200k_x": round(200000 * cube_chain15_contrib_c / fixed, 2),
            "coverage_at_50k_x": round(50000 * cube_chain15_contrib_c / fixed, 2)},
        "sensitivity_parity_cube_at_can_listing_price": {
            "contribution_per_cube_thb": round(cube_parity_contrib_c, 3),
            "steady_state_breakeven_cubes": round(be_parity),
            "coverage_at_200k_x": round(200000 * cube_parity_contrib_c / fixed, 2),
            "coverage_at_50k_x": round(50000 * cube_parity_contrib_c / fixed, 2)},
        "model_npv_breakeven_cubes_record_05": c["pilot_npv_breakeven_cubes_model"],
        "read": "Steady-state break-even ignores discounting and the year-0 cost, so it sits below the model's NPV break-even. "
                "Both bases use the same fixed cost. The headline is the chain basis, which is after excise. The cube price is a planning "
                "assumption. Pilot fit does not depend on the can volume."}

    # ---------------------------------------------------------- price cases (sensitivity table)
    price_cases = []
    cases = [
        ("single-can online list THB 17.00 (Lotus's, 68d S01)", PRICE_SINGLE),
        ("mean of four readings with the 7-Eleven 24-can at its undiscounted list THB 408 (THB 17.00 a can)", PRICE_408_MEAN),
        ("central: mean of four readings (7-Eleven 24-can at its promotional selling price THB 330)", PRICE_MODE),
        ("mean of three readings excluding the promotional 7-Eleven reading", PRICE_EX_PROMO_MEAN),
        ("Lotus's six-can, THB 85 for six (68d D13)", PRICE_SIX),
        ("lowest reading, Makro PRO 24-can, THB 325 for 24 (68d D06)", PRICE_LOW),
    ]
    for label, p in cases:
        inv_p, net_p = net_price(p, c["vat"], c["retail_margin"], c["distributor_margin"], c["excise_ad_valorem"])
        cp = net_p - nonal_thb_c
        price_cases.append({"case": label, "listing_price_thb_per_can": round(p, 4),
                            "top_down_cans_central": round(c["csd_market_2025_thb_m"] * 1e6 * c["lemon_soda_share_csd"] / p),
                            "net_after_excise_thb": round(net_p, 3),
                            "contribution_pre_aluminium_thb": round(cp, 3),
                            "gross_margin_pre_aluminium": round(cp / net_p, 4),
                            "aluminium_zero_contribution_usd_per_tonne": round(cp * 1e6 / (sheet_c * fx), 0),
                            "top_down_net_revenue_thb_m": round(c["csd_market_2025_thb_m"] * c["lemon_soda_share_csd"] * net_p / p, 1)})
    res["price_cases"] = price_cases

    # ---------------------------------------------------------- self-checks
    checks = {
        "central_price_is_mean_of_four_readings": abs(price_c - sum(MULTIPACK_PRICES.values()) / 4) < 1e-9,
        "d01_undiscounted_list_is_17_per_can": abs(PRICE_D01_LIST - 17.0) < 1e-9,
        "mean_with_d01_at_list_is_14_615": abs(PRICE_408_MEAN - 14.615) < 1e-9,
        "mean_of_three_excluding_promo_is_13_82": abs(PRICE_EX_PROMO_MEAN - 13.82) < 1e-9,
        "tbc_utilisation_matches_printed_59.46": abs(round(util_tbc, 4) - 0.5946) < 0.0002,
        "check_2021_volume_is_84.85m": abs(28e6 / CAN_L / 1e6 - 84.85) < 0.01,
        "net_per_can_below_listing_price": bool(net_c < price_c),
        "contribution_pre_aluminium_positive_central": bool(contrib_pre_c > 0),
        "interval_brackets_central_cans_td": bool(np.percentile(cans_td, 5) <= cans_td_c <= np.percentile(cans_td, 95)),
        "top_down_revenue_identity_central": bool(abs(rev_td_c - c["csd_market_2025_thb_m"] * c["lemon_soda_share_csd"] * chain_ratio_c) < 1e-6),
        "top_down_revenue_identity_draws": bool(np.allclose(rev_td, retail_val * net / price, rtol=1e-9)),
        "moq_cover_2_5_years_at_200k": abs(c["moq_low_units"] / 200000 - 2.5) < 1e-9,
        "dry_solids_200k_khco3_162_kg": round(200000 * 0.81 / 1000, 1) == 162.0,
        "dry_solids_200k_citric_420_kg": round(200000 * 2.10 / 1000, 1) == 420.0,
        "mc_draws_finite": bool(np.isfinite(net).all() and np.isfinite(cans_td).all() and np.isfinite(contrib).all()
                                and np.isfinite(speed).all() and np.isfinite(moq).all()),
        "cube_chain15_draw_equals_central_at_mode_zero_spread": bool(abs(cube_chain15_contrib_c - (net_price(15.0, c["vat"], c["retail_margin"],
                                                                                                c["distributor_margin"],
                                                                                                c["excise_ad_valorem"])[1] - cube_cost)) < 1e-12),
        "pilot_chain_breakeven_127k": abs(round(be_chain) - 126769) <= 2,
        "pilot_model_breakeven_102k": abs(round(be_model) - 101833) <= 2,
        "six_can_zero_alu_price_computed": price_cases[4]["aluminium_zero_contribution_usd_per_tonne"] > 0,
    }
    res["self_checks"] = checks
    res["self_checks_all_pass"] = all(checks.values())

    # ---------------------------------------------------------- slide 9: can cost (variable cost, excluding aluminium)
    grid9 = []
    for q in [5e8, 1e9, 1675757576.0]:
        row = {"cans_per_year": round(q)}
        for f in [0.0, 300.0, 600.0]:
            row["fixed_%dm_thb_per_can_excl_aluminium" % int(f)] = round(nonal_thb_c + f * 1e6 / q, 3)
        grid9.append(row)
    res["slide9_can_cost"] = {
        "variable_cost_excl_aluminium_thb_per_can_central": round(nonal_thb_c, 2),
        "variable_cost_excl_aluminium_thb_per_can_90": [round(float(np.percentile(nonal_thb, 5)), 2),
                                                       round(float(np.percentile(nonal_thb, 95)), 2)],
        "cost_per_can_grid_excl_aluminium": grid9,
        "aluminium_thb_per_can_per_usd_100_per_tonne": round(alu_per_100usd_t_c, 3),
        "aluminium_zero_contribution_usd_per_tonne_central": round(alu_breakeven_c, 0),
        "aluminium_zero_contribution_usd_per_tonne_90": [round(float(np.percentile(alu_breakeven, 5)), 0),
                                                        round(float(np.percentile(alu_breakeven, 95)), 0)],
        "zero_contribution_basis": "net revenue after VAT, margins and excise of THB 7.39 (a listing price of THB 13.80 a can)",
        "status": "Aluminium is not included. The LME route is not authorised (record 69). Each USD 100 a tonne adds the slope above."}

    # ---------------------------------------------------------- slide 4: Singha-side numbers (rounded as they appear in the slide text)
    res["slide4_numbers"] = {
        "cans_td_central_modal_m": round(cans_td_c / 1e6, 1),
        "cans_td_90_m": [round(float(np.percentile(cans_td, 5)) / 1e6, 1), round(float(np.percentile(cans_td, 95)) / 1e6, 1)],
        "cans_td_draw_median_m": round(float(np.percentile(cans_td, 50)) / 1e6, 1),
        "cans_td_at_408_mean_m": round(c["csd_market_2025_thb_m"] * c["lemon_soda_share_csd"] / PRICE_408_MEAN, 1),
        "cans_bu_central_m": round(cans_bu_c / 1e6, 1),
        "cans_bu_90_m": [round(float(np.percentile(cans_bu, 5)) / 1e6, 1), round(float(np.percentile(cans_bu, 95)) / 1e6, 1)],
        "net_rev_td_central_thb_m": round(rev_td_c),
        "net_rev_td_90_thb_m": [round(float(np.percentile(rev_td, 5))), round(float(np.percentile(rev_td, 95)))],
        "net_rev_bu_central_thb_m": round(rev_bu_c),
        "retail_value_td_central_thb_m": round(retail_val_c),
        "share_rev_td_central_pct": round(rev_td_c / c["sing_corp_revenue_2025_thb_m"] * 100, 1),
        "share_rev_td_90_pct": [round(float(np.percentile(share_rev_td, 5)) * 100, 1), round(float(np.percentile(share_rev_td, 95)) * 100, 1)],
        "share_rev_bu_central_pct": round(rev_bu_c / c["sing_corp_revenue_2025_thb_m"] * 100, 1),
        "share_np_td_central_pct": round(ctb_td_c / c["sing_corp_net_profit_2025_thb_m"] * 100, 1),
        "share_np_td_90_pct": [round(float(np.percentile(share_np_td, 5)) * 100, 1), round(float(np.percentile(share_np_td, 95)) * 100, 1)],
        "invoice_before_excise_central": round(inv_c, 2),
        "net_after_excise_central": round(net_c, 2),
        "variable_cost_excl_al_central": round(nonal_thb_c, 2),
        "variable_cost_excl_al_90": [round(float(np.percentile(nonal_thb, 5)), 2), round(float(np.percentile(nonal_thb, 95)), 2)],
        "contribution_pre_al_central": round(contrib_pre_c, 2),
        "variable_margin_pre_al_central_pct": round(gm_pre_c * 100, 1),
        "variable_margin_pre_al_90_pct": [round(float(np.percentile(contrib / net, 5)) * 100, 1), round(float(np.percentile(contrib / net, 95)) * 100, 1)],
        "alu_slope_thb_per_usd100": round(alu_per_100usd_t_c, 3),
        "alu_zero_usd_t_central": round(alu_breakeven_c),
        "headroom_200k_line_hours_central": round(200000 / (60.0 * 60.0 * c["pouch_line_efficiency"]), 1),
        "headroom_1m_line_hours_central": round(1000000 / (60.0 * 60.0 * c["pouch_line_efficiency"]), 1),
        "pilot_breakeven_chain_central": round(be_chain),
        "pilot_breakeven_chain_90": [round(float(np.percentile(fixed / cube_chain15_contrib, 5))), round(float(np.percentile(fixed / cube_chain15_contrib, 95)))],
        "pilot_breakeven_parity": round(be_parity),
    }

    res["aluminium_status_note"] = "LME reading not used: route not authorised; page HTTP 403 on 20 Oct 2026."
    res["web_search_note"] = ("Four open searches (Yuzu on sale; Thai distributor margin; can and pouch line speeds; CP ALL margin) "
                              "were attempted on 20 October 2026 and returned the budget-exhausted notice. None was run. Stated limits.")

    OUT_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"listing_price_central": round(price_c, 4),
                      "cans_td": round(cans_td_c), "cans_td_90": [round(float(np.percentile(cans_td, 5))), round(float(np.percentile(cans_td, 95)))],
                      "cans_td_draw_median": round(float(np.percentile(cans_td, 50))),
                      "cans_bu": round(cans_bu_c),
                      "net_per_can": round(net_c, 3), "invoice": round(inv_c, 3),
                      "nonal_thb": round(nonal_thb_c, 3), "contrib_pre_al": round(contrib_pre_c, 3),
                      "alu_per_100": round(alu_per_100usd_t_c, 4), "alu_zero_usd_t": round(alu_breakeven_c),
                      "pilot_chain_be": round(be_chain), "pilot_model_be": round(be_model),
                      "checks_pass": res["self_checks_all_pass"],
                      "failed_checks": [k for k, v in checks.items() if not v]}, indent=1))


if __name__ == "__main__":
    main()
