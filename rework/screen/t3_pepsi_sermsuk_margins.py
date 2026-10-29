"""T3 (Pepsi system and Sermsuk): margins, per-330 mL prices, share reports and mass ratio from filed or listed inputs.

Inputs are copied from the saved pages under rework/raw/diligence_2026-10-20/T3/ (and, for retail
prices and two share rows, T4 and T5 and T1). Nothing here is random. Run:  python t3_pepsi_sermsuk_margins.py
Output: t3_pepsi_sermsuk_margins_results.json (same folder).

Second pass (20 October 2026), after the independent check:
- Sermsuk FY2022 and FY2023 gross margin is also computed from the unrounded Form 250-2 lines (filed 28.26% and 28.30%).
- The share table now holds every report read (8 earlier rows plus the March 2023 ThaiBev table, the Marketeer and
  Brand Buffet rows, and the 13 October 2025 est row).
- Suntory Beverage & Food Asia Pacific FY2022 segment is added as a PROXY for the Pepsi bottler (not Thailand-only).
- Lemon Soda price position is computed against Lotus's six-pack and single-can levels.
- The packed-unit mass ratio carries its input tiers (ASSUMPTION inputs) and the allowance range.

Third pass (20 October 2026), after the verifier's issues:
- Suntory Beverage & Food Asia Pacific segment is now a P series for FY2022 (as first reported and restated), FY2023,
  FY2024 and FY2025, from the annual securities reports on EDINET (saved in
  raw/diligence_2026-10-20/T3/sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md). Still a PROXY for the Pepsi bottler.
- The Lemon Soda price position for the judge text uses only 7UP and Sprite rows. The Singha Lemon Soda rows stay in the
  price table as reference rows only, because the deck says the Singha can price is not verified (record section 12).
- The packed-unit mass uses the deck's 3.79 g dry mass, which already includes the 0.80 g binder, plus the assumed 1.5 g pouch.
- The Mini Me article of 30 March 2025 was opened on 20 October 2026 and is added to the share rows (basis not stated).

Fourth pass (20 October 2026), after the verifier's second list:
- ThaiBev Non-Alcohol attributable profit for FY2024 is printed as 1,455 in the FY2024 announcement and as 1,146 in the
  FY2025 announcement (comparative), with Others moved from 2,191 to 2,500. Both splits sum to 27,215 (check below).
- Chang Soda and Chang Water (FY2024) and Water and Soda (FY2025) are different scopes; the implied base is shown only to
  show that the two series do not join.
- The sugar-tax ladder printed by the press is compared with the saved Royal Gazette schedule for item 02.02
  (raw/gazette_sugar_drink_excise_primary_2560_A095_111.md, section 2). No phase 4 notice was read.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def pct(a, b, nd=2):
    return round(100.0 * a / b, nd)


# 1. Sermsuk PCL and subsidiaries, consolidated, THB million, fiscal year ends 30 September.
#    Source: MD&A filed with the SET for each year (saved in T3/sermsuk_mda_fy2022_fy2023_fy2024_set_filings.md).
#    The MD&A prints whole million baht, so margins from these inputs carry a rounding of about 0.01 point.
sermsuk_in = {
    "FY2022": {"year_end": "2022-09-30", "sales": 10905, "cost_of_sales": 7824, "net_profit": 13},
    "FY2023": {"year_end": "2023-09-30", "sales": 12371, "cost_of_sales": 8870, "net_profit": 248},
    "FY2024": {"year_end": "2024-09-30", "sales": 13153, "cost_of_sales": 9306, "net_profit": 404},
}
# Unrounded lines from Sermsuk Form 250-2 (8 Oct 2024), PDF pages 15 and 16 (saved in
# T3/sermsuk_form250_2_opinion_2024-10-08_extracts.md). The filing prints 12,371.04 in its income statement
# table and 12,371.03 in its text for FY2023 sales; the text figure is used here.
form250_2_lines = {
    "FY2022": {"sales": 10904.85, "cost_of_sales": 7823.54, "filed_gross_margin_pct": 28.26},
    "FY2023": {"sales": 12371.03, "cost_of_sales": 8869.46, "filed_gross_margin_pct": 28.30},
}
sermsuk = {}
for fy, d in sermsuk_in.items():
    gp = d["sales"] - d["cost_of_sales"]
    row = {
        **d,
        "gross_profit": gp,
        "gross_margin_pct": pct(gp, d["sales"]),
        "gross_margin_pct_4dp": pct(gp, d["sales"], 4),
        "net_margin_pct": pct(d["net_profit"], d["sales"]),
        "net_margin_pct_4dp": pct(d["net_profit"], d["sales"], 4),
    }
    if fy in form250_2_lines:
        f = form250_2_lines[fy]
        gp_u = f["sales"] - f["cost_of_sales"]
        row["gross_profit_unrounded_form250_2"] = round(gp_u, 2)
        row["gross_margin_pct_from_unrounded_form250_2"] = pct(gp_u, f["sales"])
        row["gross_margin_pct_as_filed_form250_2"] = f["filed_gross_margin_pct"]
        row["filed_minus_mdna_computed_point"] = round(f["filed_gross_margin_pct"] - row["gross_margin_pct"], 2)
    sermsuk[fy] = row
# growth in sales, FY2023 and FY2024
sermsuk["FY2023"]["sales_growth_pct"] = round(100.0 * (12371 / 10905 - 1), 2)
sermsuk["FY2024"]["sales_growth_pct"] = round(100.0 * (13153 / 12371 - 1), 2)

# Sermsuk FY2024 cost lines as shares of sales (MD&A of 15 Nov 2024: distribution costs 3,033; administrative 736)
sermsuk_cost_shares_fy2024 = {
    "sales": 13153,
    "cost_of_sales_pct": pct(9306, 13153),
    "distribution_costs": 3033,
    "distribution_costs_pct": pct(3033, 13153),
    "administrative_expenses": 736,
    "administrative_expenses_pct": pct(736, 13153),
}

# Sermsuk revenue structure (THB million), Form 250-2 of 8 Oct 2024, section 1.4
ssc_struct = {
    "FY2023_carbonated": 4550.15,
    "FY2023_total": 12371.03,
    "FY2023_carbonated_share_pct": pct(4550.15, 12371.03),
}

# Gross margin stated in Form 250-2 (check of the derivation above)
ssc_stated_gm = {"FY2021": 30.93, "FY2022": 28.26, "FY2023": 28.30, "9M_2024": 29.47}

# 2. PepsiCo, Inc., consolidated (global), USD million, fiscal year ends last Saturday of December.
#    Source: SEC XBRL company concepts, 10-K, accessions 0000077476-24-000008, -25-000007, -26-000007.
pepsico_in = {
    "FY2023": {"year_end": "2023-12-30", "revenue": 91471, "gross_profit": 49590, "net_income_to_pepsico": 9074},
    "FY2024": {"year_end": "2024-12-28", "revenue": 91854, "gross_profit": 50110, "net_income_to_pepsico": 9578},
    "FY2025": {"year_end": "2025-12-27", "revenue": 93925, "gross_profit": 50859, "net_income_to_pepsico": 8240},
}
pepsico = {}
for fy, d in pepsico_in.items():
    pepsico[fy] = {
        **d,
        "gross_margin_pct": pct(d["gross_profit"], d["revenue"]),
        "net_margin_pct": pct(d["net_income_to_pepsico"], d["revenue"]),
    }

# 3. ThaiBev non-alcoholic beverages segment (group segment; includes Sermsuk, F&N, Oishi, dairy), THB million,
#    fiscal year ends 30 September. FY2024 and FY2025 from the SGX year-end announcements (saved by T4);
#    FY2023 is DERIVED from the changes stated in the FY2024 announcement.
nab = {
    "FY2024": {"sales": 65802, "gross_profit": 23688, "profit_for_year": 5934, "attributable": 1455},
    "FY2025": {"sales": 64774, "gross_profit": 23694, "profit_for_year": 5141, "attributable": 2414},
}
nab["FY2023_derived"] = {
    "sales": 65802 - 2659,
    "gross_profit": 23688 - 2365,
    "profit_for_year": 5934 - 504,
    "attributable": 1455 - 259,
}
for fy, d in nab.items():
    d["gross_margin_pct"] = pct(d["gross_profit"], d["sales"])
    d["profit_for_year_margin_pct"] = pct(d["profit_for_year"], d["sales"])
    d["attributable_margin_pct"] = pct(d["attributable"], d["sales"])

# 3b. PROXY for the Pepsi bottler: Suntory Beverage & Food Limited, Asia Pacific segment, FY2022
#     (1 Jan to 31 Dec 2022; securities report filed 27 Mar 2023, PDF page 31, saved in
#     T3/sbf_securities_report_fy2022_edinet_extract.md). JPY billion as printed (3,594 and 564 hundred-million yen).
#     The segment covers Thailand, Vietnam, Indonesia, Oceania and health foods, so it is not a Thailand-only
#     figure and the segment profit is not a gross or net margin. Suntory Beverage & Food consolidates
#     Suntory PepsiCo Beverage (Thailand) at 51.0% (PDF page 116).
sbf_ap_fy2022 = {
    "revenue_jpy_billion": 359.4,
    "revenue_growth_pct_as_printed": 21.4,
    "segment_profit_jpy_billion": 56.4,
    "segment_profit_growth_pct_as_printed": 42.0,
}
sbf_ap_fy2022["segment_profit_margin_pct"] = pct(56.4, 359.4)
sbf_ap_fy2022["prior_year_revenue_jpy_billion_derived"] = round(359.4 / 1.214, 1)
sbf_ap_fy2022["prior_year_segment_profit_jpy_billion_derived"] = round(56.4 / 1.42, 1)
sbf_ap_fy2022["prior_year_segment_profit_margin_pct_derived"] = pct(
    sbf_ap_fy2022["prior_year_segment_profit_jpy_billion_derived"],
    sbf_ap_fy2022["prior_year_revenue_jpy_billion_derived"])
sbf_ap_fy2022["tier"] = "PROXY (P filing; Asia Pacific segment, not Thailand-only; segment profit, not gross or net margin)"
sbf_ap_fy2022["basis_note"] = ("As first reported in the FY2022 report, Africa was inside Asia Pacific. "
                               "The FY2023 report moved Africa to Europe and restated FY2022 (see the series below).")

# Asia Pacific segment series, JPY million, from the annual securities reports (P), external segment revenue
# and segment profit as printed in each report's segment table. Ratio = segment profit / external segment revenue.
# Columns in these tables: Japan, Asia Pacific, Europe, Americas. Currency-neutral growth is as printed in the MD&A.
sbf_ap_series = {
    "FY2022_restated_new_basis": {
        "source": "FY2023 annual securities report (S100T62P), prior-year column of the segment table",
        "revenue_jpy_m": 352615, "segment_profit_jpy_m": 57731},
    "FY2023": {
        "source": "FY2023 annual securities report (S100T62P), segment table, year 2023",
        "revenue_jpy_m": 371435, "segment_profit_jpy_m": 43075,
        "revenue_growth_pct_as_printed": 5.3, "revenue_growth_cc_pct_as_printed": 0.0,
        "segment_profit_growth_pct_as_printed": -25.4, "segment_profit_growth_cc_pct_as_printed": -27.7},
    "FY2024": {
        "source": "FY2024 annual securities report (S100VHVQ), segment table, year 2024",
        "revenue_jpy_m": 402049, "segment_profit_jpy_m": 45404,
        "revenue_growth_pct_as_printed": 8.2, "revenue_growth_cc_pct_as_printed": 3.1,
        "segment_profit_growth_pct_as_printed": 5.4, "segment_profit_growth_cc_pct_as_printed": 1.0},
    "FY2025": {
        "source": "FY2025 annual securities report (S100XSOA), segment table, year 2025",
        "revenue_jpy_m": 394057, "segment_profit_jpy_m": 42516,
        "revenue_growth_pct_as_printed": -2.0, "revenue_growth_cc_pct_as_printed": -1.6,
        "segment_profit_growth_pct_as_printed": -6.4, "segment_profit_growth_cc_pct_as_printed": -6.2},
}
for _k, _v in sbf_ap_series.items():
    _v["segment_profit_margin_pct"] = pct(_v["segment_profit_jpy_m"], _v["revenue_jpy_m"])
    _v["tier"] = "PROXY (P filing; segment profit ratio; Asia Pacific, not Thailand-only; not a gross or net margin)"
# Check: FY2022 restated to FY2023 change, against the printed -25.4%
sbf_ap_fy23_vs_fy22_restated_pct = round(100.0 * (43075 / 57731 - 1), 1)
# Constant-currency check for the FY2022 original figure: the FY2022 report prints 28.6% currency-neutral segment profit growth
sbf_ap_fy22_original_cc_profit_growth_pct_as_printed = 28.6

# 4. Price per 330 mL (THB). Listed pack price divided by units, then scaled by 330 / pack size.
#    Retail listings read 19 and 20 October 2026 (tier S); see the T3 price table in the record.
def per330(price, units, ml):
    per_unit = price / units
    return {"price": price, "units": units, "unit_ml": ml,
            "per_unit": round(per_unit, 2), "per_330ml": round(per_unit * 330.0 / ml, 2)}


prices = {
    "7UP Zero Sugar Lemon Soda 325 mL x6, Lotus's (L5)": per330(75, 6, 325),
    "7UP no-sugar lemon soda 325 mL single can, Lotus's Shop Online row on Priceza (P3)": per330(16, 1, 325),
    "7UP lemon soda no sugar 325 mL x6, Suntory PepsiCo official store, LazMall via Priceza (P3)": per330(96, 6, 325),
    "7UP lemon soda no sugar 325 mL x24, Suntory PepsiCo official store, LazMall via Priceza (P3)": per330(293, 24, 325),
    "est cola 325 mL x6, Makro PRO cash-and-carry listing (T4)": per330(79, 6, 325),
    "est cola 325 mL x6, 7-Eleven online (T4)": per330(138, 6, 325),
    "est Sugar Free (flavour not stated) 325 mL x6, Lazada seller Sermsuk Click via Priceza (T4)": per330(99, 6, 325),
    "Pepsi 325 mL x6, 7-Eleven online (capture 19)": per330(167, 6, 325),
    "Sprite 325 mL x6, Lotus's (L2)": per330(85, 6, 325),
    "Singha Lemon Soda 330 mL x6, Lotus's (L8)": per330(85, 6, 330),
    "Singha Lemon Soda 330 mL single, Lotus's (L7)": per330(17, 1, 330),
    "Singha Lemon Soda 330 mL x6, 7-Eleven online (A2)": per330(172, 6, 330),
}

# Sermsuk average selling price of carbonated drinks, THB per litre (Form 250-2 assumption table), per 330 mL
ssc_asp = {"carbonated_thb_per_litre": 18.42, "per_330ml": round(18.42 * 0.330, 2),
           "est_volume_Oct2023_Sep2024_million_litres_IFA": 275.60}

# Lemon Soda planning shelf price from the deck (assumption): THB 15 per 330 mL
cube_shelf = 15.0
p7 = lambda k: prices[k]["per_330ml"]
# Judge-text rows: 7UP and Sprite (six-pack) and 7UP (single can) only. The Singha Lemon Soda rows are not used
# for the price position, because the deck and submission say the Singha can price is not verified (record section 12).
lotus_six_pack = {
    "7UP Zero Sugar Lemon Soda": p7("7UP Zero Sugar Lemon Soda 325 mL x6, Lotus's (L5)"),
    "Sprite": p7("Sprite 325 mL x6, Lotus's (L2)"),
}
single_can = {
    "7UP no-sugar lemon soda (Lotus's Shop Online row on Priceza)": p7(
        "7UP no-sugar lemon soda 325 mL single can, Lotus's Shop Online row on Priceza (P3)"),
}
singha_reference_rows = {
    "note": "Reference only. Lotus's Singha Lemon Soda rows (S). The deck and submission say the Singha can price is not "
            "verified, so these rows are not used in the judge text. Record section 12 lists the conflict.",
    "six_pack_per330_lotus": p7("Singha Lemon Soda 330 mL x6, Lotus's (L8)"),
    "single_can_per330_lotus": p7("Singha Lemon Soda 330 mL single, Lotus's (L7)"),
    "six_pack_per330_7eleven_online": p7("Singha Lemon Soda 330 mL x6, 7-Eleven online (A2)"),
}
price_position = {
    "lotus_six_pack_per330": lotus_six_pack,
    "lotus_six_pack_range": [min(lotus_six_pack.values()), max(lotus_six_pack.values())],
    "single_can_per330": single_can,
    "single_can_range": [min(single_can.values()), max(single_can.values())],
    "cube_shelf_price_per330_assumption": cube_shelf,
    "cube_between_six_pack_max_and_single_can_min": bool(
        max(lotus_six_pack.values()) < cube_shelf < min(single_can.values())),
    "singha_reference_rows": singha_reference_rows,
    "note": "The 7UP official store on LazMall prices its own six-pack at the single-can level (16.25 per 330 mL) "
            "and its 24-pack at 12.40, so the multipack level is not uniform across retailers. Judge-text ranges "
            "use only the 7UP rows and the Sprite six-pack.",
}
ranges = {
    "7UP_zero_sugar_lemon_per330_min_max": [
        round(min(v["per_330ml"] for k, v in prices.items() if k.startswith("7UP")), 2),
        round(max(v["per_330ml"] for k, v in prices.items() if k.startswith("7UP")), 2),
    ],
    "cube_shelf_price_per330_assumption": cube_shelf,
}

# Seven-Eleven online price level against Lotus's for the same Singha pack (flag for reading the Pepsi row)
ratio_7e_to_lotus_singha_6pack = round(172 / 85, 2)

# Mass of the packed Lemon Soda unit against the liquid it makes. Deck inputs: dry cube 3.79 g central
# (allowance range 3.46 to 4.24 g, record 72). The 3.79 g dry mass already includes the 0.80 g binder and filler
# (0.81 + 2.10 + 0.033 + 0.80 + 0.05 = 3.79 g on the formulation). The pouch of 1.5 g is an ASSUMPTION and nothing
# was weighed. 330 mL of water is taken as 330 g at 1 g per mL; the weight of a can or bottle is not counted.
pouch_g = 1.5
dry_mass_formulation_sum_g = round(0.81 + 2.10 + 0.033 + 0.80 + 0.05, 3)
mass = {
    "tier": "DERIVED from an ASSUMPTION input (pouch 1.5 g). The dry mass 3.79 g is the deck's central figure and includes the binder; nothing was weighed",
    "packed_unit_g": 5.29,
    "dry_cube_g": 3.79,
    "dry_mass_formulation_sum_g_check": dry_mass_formulation_sum_g,
    "binder_inside_dry_mass_g": 0.80,
    "pouch_g_assumption": pouch_g,
    "liquid_330ml_g": 330.0,
    "packed_unit_pct_of_liquid": round(100.0 * 5.29 / 330.0, 2),
    "dry_cube_pct_of_liquid": round(100.0 * 3.79 / 330.0, 2),
    "liquid_to_packed_unit_ratio": round(330.0 / 5.29, 1),
    "dry_cube_allowance_range_g": [3.46, 4.24],
    "packed_unit_pct_of_liquid_over_allowance_range": [
        round(100.0 * (3.46 + pouch_g) / 330.0, 2), round(100.0 * (4.24 + pouch_g) / 330.0, 2)],
    "dry_cube_pct_of_liquid_over_allowance_range": [
        round(100.0 * 3.46 / 330.0, 2), round(100.0 * 4.24 / 330.0, 2)],
}

# Share reports as printed, volume unless stated. "basis" is what the page says; "not stated" means the page
# gives no base. Rows 1 to 8 are the earlier eight; the rest were added in the second pass.
share_reports = [
    {"date": "2023-03-13", "est_pct": 8.0, "basis": "not stated", "source": "Thansettakij 558785 (via T4)"},
    {"date": "2023-03-21", "est_pct": 8.0, "coke_pct": 51, "pepsi_pct": 37, "big_cola_pct": 3, "others_pct": 1,
     "basis": "ThaiBev table, partly Nielsen; year and measure not stated in the saved extract",
     "source": "Positioning 1424257 (T1 file nielseniq_press_series_2023_2026.md, row 1; page not re-opened in T3)"},
    {"date": "2023-10-17", "est_pct": 9.1, "basis": "not stated; up from 7.1% before the rebrand",
     "source": "Brand Buffet (T4 file est_market_2023_2025_brandbuffet_marketeer_thansettakij.md)"},
    {"date": "2023-10-29", "est_pct": 9.1, "coke_pct": 54, "pepsi_pct": 30,
     "basis": "est volume share for August 2023, was 7%; Coke and Pepsi bases not stated",
     "source": "Gotomanager 5234"},
    {"date": "2024-03-15", "est_pct": 8.9, "basis": "volume (as printed by Marketeer)",
     "source": "Marketeer 345506 (T4 file est_market_2023_2025_brandbuffet_marketeer_thansettakij.md)"},
    {"date": "2024-03-16", "est_pct": 8.6, "coke_pct": 51, "pepsi_pct": 30,
     "basis": "est stated as volume; Coke and Pepsi measure and year not stated", "source": "Thansettakij 590894"},
    {"date": "2024-04-15", "est_pct": 9.0, "coke_pct": 51, "pepsi_pct": 30, "basis": "not stated",
     "source": "Thairath 2778345"},
    {"date": "2025-03-12", "est_pct": 8.9, "basis": "reference March 2024", "source": "Marketeer 406131 (via T4)"},
    {"date": "2025-03-26", "coke_pct": 51, "pepsi_pct": 39.1, "basis": "of the dark cola market; year not stated",
     "source": "Thansettakij 623088"},
    {"date": "2025-04-03", "est_pct": 8.9, "coke_pct": 51, "pepsi_pct": 39, "big_cola_pct": 5,
     "basis": "of the Thai carbonated soft drink market as printed; year and data owner not stated",
     "source": "Thansettakij 624003"},
    {"date": "2025-04-17", "coke_pct": 51, "pepsi_pct": 39.1, "basis": "of the dark cola segment; year not stated",
     "source": "Brand Buffet suntory-pepsico-beverage-strategy-2025"},
    {"date": "2025-03-30", "pepsi_pct": 39.1, "basis": "not stated; the article gives no basis for the 39.1 per cent "
     "(opened 20 October 2026; the investment and CEO remarks are attributed to Prachachat, not the share)",
     "source": "Mini Me Insights, 30 March 2025 (opened; raw/diligence_2026-10-20/T3/mini_me_2025-03-30_opened_2026-10-20.md)"},
    {"date": "2025-10-13", "est_pct": 10.6, "est_colour_soda_pct": 24.6,
     "basis": "est total soda share, up from 7% before the rebrand; basis not stated; est number 2 in colour soda",
     "source": "Thansettakij 641276 (T4 file est_thansettakij_2025-10-13_share_and_glow.md)"},
]
for r in share_reports:
    parts = [r.get("est_pct", 0), r.get("coke_pct", 0), r.get("pepsi_pct", 0), r.get("big_cola_pct", 0),
             r.get("others_pct", 0)]
    # a sum is shown only when at least three shares are printed in the same row; a row with one or two shares
    # (for example Coke and Pepsi of the dark cola segment) is not a partition, so no sum is formed
    r["sum_of_printed_shares"] = round(sum(parts), 1) if sum(1 for p in parts if p) >= 3 else None
est_values = [r["est_pct"] for r in share_reports if "est_pct" in r]
share_summary = {
    "est_min_pct": min(est_values),
    "est_max_pct": max(est_values),
    "est_reports": len(est_values),
    "latest_est_report": "2025-10-13, 10.6 (basis not stated)",
    "pepsi_values_pct": sorted({r["pepsi_pct"] for r in share_reports if "pepsi_pct" in r}),
    "rows_summing_to_100": [r["date"] for r in share_reports if r["sum_of_printed_shares"] == 100.0],
    "rows_summing_over_100": [r["date"] for r in share_reports
                              if r["sum_of_printed_shares"] is not None and r["sum_of_printed_shares"] > 100.0],
    "rows_with_a_sum": [r["date"] for r in share_reports if r["sum_of_printed_shares"] is not None],
}

# Market value statements (THB million), as printed, with the window where record 67 traced one.
market_values = [
    {"value": 62000, "where": "Gotomanager 29 Oct 2023; Brand Buffet 17 Oct 2023; Thairath 10 Oct 2023",
     "window": "not stated (Thairath: growth period Sep 2022 to Aug 2023)", "tier": "S"},
    {"value": 66000, "where": "Thansettakij 16 Mar 2024; Marketeer 15 Mar 2024; MarketPlus 8 May 2024",
     "window": "NielsenIQ, Feb 2023 to Jan 2024, +12%", "tier": "S"},
    {"value": 70772, "where": "Thansettakij 14 Jan 2025", "window": "NielsenIQ via ThaiBev, 12 months to Nov 2024, +9%",
     "tier": "S"},
    {"value": 68000, "where": "Thansettakij 13 Oct 2025", "window": "labelled 2024; may be a 2025 level (record 67)",
     "tier": "S"},
    {"value": 76900, "where": "Kasikorn Research Center via Thansettakij 8 Sep 2025", "window": "2025 estimate or forecast",
     "tier": "S"},
]
mv = [m["value"] for m in market_values]
market_value_summary = {"min": min(mv), "max": max(mv),
                        "colour_soda_17391_pct_of_68000": pct(17391, 68000),
                        "colour_soda_17391_pct_of_70772": pct(17391, 70772),
                        "printed_share_of_total_pct_for_colour_soda": 30}

# ---- Fourth pass (20 October 2026) ----
# (a) ThaiBev Non-Alcohol attributable profit, FY2024. P: FY2024 announcement (performance table, by-business row,
#     and the Non-Alcohol commentary "Baht 1,455 million, an increase of Baht 259 million, or 21.7%") and FY2025
#     announcement (by-business table, FY2024 comparative column). THB million.
TB_FY24_SPLIT_FY24_ANNOUNCEMENT = {"spirits": 20770, "beer": 2735, "non_alcohol": 1455, "food": 64, "others": 2191}
TB_FY24_SPLIT_FY25_COMPARATIVE = {"spirits": 20770, "beer": 2735, "non_alcohol": 1146, "food": 64, "others": 2500}
TB_FY24_ATTRIBUTABLE_TOTAL = 27215
TB_FY23_NON_ALCOHOL_COMPARATIVE = 1196          # FY2024 announcement comparative (P)
TB_FY25_NON_ALCOHOL_ATTRIBUTABLE = 2414         # FY2025 announcement (P)
TB_FY25_NON_ALCOHOL_GROWTH_PRINTED_PCT = 110.6  # FY2025 announcement, as printed (P)
thaibev_fy24_nonalcohol_basis = {
    "sum_fy24_announcement_split": sum(TB_FY24_SPLIT_FY24_ANNOUNCEMENT.values()),
    "sum_fy25_comparative_split": sum(TB_FY24_SPLIT_FY25_COMPARATIVE.values()),
    "both_splits_sum_to_27215": (sum(TB_FY24_SPLIT_FY24_ANNOUNCEMENT.values()) == TB_FY24_ATTRIBUTABLE_TOTAL
                                 and sum(TB_FY24_SPLIT_FY25_COMPARATIVE.values()) == TB_FY24_ATTRIBUTABLE_TOTAL),
    "non_alcohol_reallocated_thb_million": TB_FY24_SPLIT_FY24_ANNOUNCEMENT["non_alcohol"]
                                           - TB_FY24_SPLIT_FY25_COMPARATIVE["non_alcohol"],
    "others_reallocated_thb_million": TB_FY24_SPLIT_FY25_COMPARATIVE["others"]
                                      - TB_FY24_SPLIT_FY24_ANNOUNCEMENT["others"],
    "fy24_vs_fy23_growth_pct_announcement_basis": round(
        100 * (TB_FY24_SPLIT_FY24_ANNOUNCEMENT["non_alcohol"] / TB_FY23_NON_ALCOHOL_COMPARATIVE - 1), 1),
    "fy25_growth_pct_on_1146_base": round(
        100 * (TB_FY25_NON_ALCOHOL_ATTRIBUTABLE / TB_FY24_SPLIT_FY25_COMPARATIVE["non_alcohol"] - 1), 1),
    "fy25_growth_pct_on_1455_base": round(
        100 * (TB_FY25_NON_ALCOHOL_ATTRIBUTABLE / TB_FY24_SPLIT_FY24_ANNOUNCEMENT["non_alcohol"] - 1), 1),
    "fy25_growth_as_printed_pct": TB_FY25_NON_ALCOHOL_GROWTH_PRINTED_PCT,
    "printed_growth_matches_1146_base": round(
        100 * (TB_FY25_NON_ALCOHOL_ATTRIBUTABLE / TB_FY24_SPLIT_FY25_COMPARATIVE["non_alcohol"] - 1), 1)
        == TB_FY25_NON_ALCOHOL_GROWTH_PRINTED_PCT,
    "note": "The FY2025 comparative restates the FY2024 split: 309 million baht moves from Non-Alcohol to Others with the "
            "total unchanged. The FY2025 extract does not label it a restatement. The FY2024 announcement's by-business "
            "table prints a movement of 251 for Beer-row numbers, which does not reconcile to the narrative 259; the record "
            "uses the narrative (1,455 against 1,196).",
}

# (b) Chang scope check. P: FY2024 announcement (Chang Soda and Chang Water, 122.8 million litres, +8.2%) and FY2025
#     announcement (Water & Soda, 127.6 million litres, -4.0%). Different product scopes.
CHANG_FY24_SODA_WATER_MLITRES = 122.8
CHANG_FY25_WATER_SODA_MLITRES = 127.6
CHANG_FY25_CHANGE_PCT = -4.0
chang_scope_check = {
    "fy25_implied_base_on_fy25_scope_mlitres": round(CHANG_FY25_WATER_SODA_MLITRES / (1 + CHANG_FY25_CHANGE_PCT / 100), 1),
    "fy24_printed_scope_mlitres": CHANG_FY24_SODA_WATER_MLITRES,
    "implied_base_equals_fy24_printed": round(CHANG_FY25_WATER_SODA_MLITRES / (1 + CHANG_FY25_CHANGE_PCT / 100), 1)
                                        == CHANG_FY24_SODA_WATER_MLITRES,
    "series_comparable": False,
    "note": "The FY2025 line is 'Water & Soda'; the FY2024 line is 'Chang Soda and Chang Water'. The implied base of "
            "about 132.9 million litres does not equal the FY2024 printed 122.8, so the two rows are not one series and no "
            "growth rate is taken from them.",
}

# (c) Sugar-tax ladder check. P: saved Royal Gazette schedule for item 02.02 (raw/gazette_sugar_drink_excise_primary_2560_A095_111.md,
#     section 2; baht per litre; read from page images). S: press ladder (phase 3, Thansettakij 27 March 2023 as saved in
#     raw/diligence_2026-10-20/T3/pepsi_system_moves_and_launches_2012_2026.md line 24; phase 4, Brand Buffet 17 April 2025
#     as saved in csd_market_share_press_2020_2025.md, block 7).
GAZETTE_02_02_BANDS = {  # rates for the bands over 6-8 g, 8-10 g, 10-14 g (or 10 g), 14-18 g (or 14 g) as printed
    "16 Sep 2560 to 30 Sep 2562": [0.10, 0.30, 0.50, 1],
    "1 Oct 2562 to 30 Sep 2564": [0.10, 0.30, 1, 3, 5],
    "1 Oct 2564 to 30 Sep 2566": [0.30, 1, 3, 5],
    "1 Oct 2566 onwards": [1, 3, 5],
}
PRESS_PHASE3_LADDER_BAHT = [0.3, 1, 3, 5]    # press, phase 3 (1 Apr 2023 to 31 Mar 2025) as printed (S)
PRESS_PHASE4_LOW_BAHT = 0.3                  # press, phase 4 (from 1 Apr 2025), as printed (S); not checked against a notice
PRESS_PHASE4_HIGH_BAHT = 5
sugar_tax_ladder_check = {
    "press_phase3_ladder_equals_gazette_1oct2564_row": PRESS_PHASE3_LADDER_BAHT == GAZETTE_02_02_BANDS["1 Oct 2564 to 30 Sep 2566"],
    "press_phase3_period_1apr2023_to_31mar2025_is_a_gazette_period": "1 Apr 2023 to 31 Mar 2025" in GAZETTE_02_02_BANDS,
    "gazette_row_in_force_from_1oct2566_nonzero_rates": GAZETTE_02_02_BANDS["1 Oct 2566 onwards"],
    "press_phase4_low_0_3_appears_in_gazette_1oct2566_row": PRESS_PHASE4_LOW_BAHT in GAZETTE_02_02_BANDS["1 Oct 2566 onwards"],
    "press_phase4_high_5_appears_in_gazette_1oct2566_row": PRESS_PHASE4_HIGH_BAHT in GAZETTE_02_02_BANDS["1 Oct 2566 onwards"],
    "phase4_notice_read": False,
    "note": "The press phase 3 ladder matches the Gazette row for 1 Oct 2564 to 30 Sep 2566, not the period the press gives. "
            "The Gazette row in force from 1 Oct 2566 has no 0.3 rate, so the press phase 4 range (0.3 to 5) is not a schedule "
            "of that notice. Later amendments were not searched. Phase 4 is tier S (press only) and is a stated limit.",
}

out = {
    "script": "rework/screen/t3_pepsi_sermsuk_margins.py",
    "seed": "none (no random numbers)",
    "sermsuk_consolidated_thb_million_fye_30_sep": sermsuk,
    "sermsuk_cost_shares_fy2024": sermsuk_cost_shares_fy2024,
    "sermsuk_revenue_structure_thb_million": ssc_struct,
    "sermsuk_stated_gross_margin_pct_form250_2": ssc_stated_gm,
    "sermsuk_average_selling_price_carbonated": ssc_asp,
    "pepsico_inc_consolidated_usd_million_fye_last_sat_dec": pepsico,
    "thaibev_non_alcoholic_segment_thb_million_fye_30_sep": nab,
    "suntory_beverage_food_asia_pacific_segment_fy2022_proxy": sbf_ap_fy2022,
    "suntory_beverage_food_asia_pacific_segment_series_fy2022_restated_to_fy2025": sbf_ap_series,
    "sbf_apac_fy23_vs_fy22_restated_change_pct": sbf_ap_fy23_vs_fy22_restated_pct,
    "sbf_apac_fy22_original_currency_neutral_profit_growth_pct_as_printed": sbf_ap_fy22_original_cc_profit_growth_pct_as_printed,
    "price_per_330ml_thb": prices,
    "price_position_of_lemon_soda_assumption": price_position,
    "ranges": ranges,
    "ratio_7eleven_online_to_lotus_singha_6pack": ratio_7e_to_lotus_singha_6pack,
    "mass_packed_unit_vs_liquid": mass,
    "share_reports_as_printed": share_reports,
    "share_summary": share_summary,
    "market_value_statements_as_printed": market_values,
    "market_value_summary": market_value_summary,
    "fourth_pass_thaibev_fy24_non_alcohol_basis": thaibev_fy24_nonalcohol_basis,
    "fourth_pass_chang_scope_check": chang_scope_check,
    "fourth_pass_sugar_tax_ladder_check": sugar_tax_ladder_check,
}
with open(os.path.join(HERE, "t3_pepsi_sermsuk_margins_results.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("wrote t3_pepsi_sermsuk_margins_results.json")
