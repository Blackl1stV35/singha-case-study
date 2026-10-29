"""T4 competitor due diligence: margins, per-330 mL price conversions, est price bands by format,
and the lemon-lime, lime and Singha cross-reference rows (rounds 3 and 4).

Every input below was typed on 20 October 2026 from a saved page. The file named beside each block or row is the saved
page under rework/raw/diligence_2026-10-20/ (T4 for the T4 pages; T2, T5 for the cross-referenced listings).
No randomness; standard library only. Output: t4_competitor_margins_results.json
Run: python -I rework/screen/t4_competitor_margins.py
"""
import json
import os
import statistics
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))


def pct(a, b):
    return round(100.0 * a / b, 3)


def r2_half_up(x):
    # Round-half-up to two decimals (Python's round() uses binary floats: 14.625 would print 14.62)
    return float(Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def band(values):
    return {"rows": len(values), "min": min(values), "max": max(values), "median": round(statistics.median(values), 2)}


# Osotspa PCL, group figures (the company page does not print "consolidated"), fiscal year to 31 December
# (calendar year per the 6M'26 column and an aggregator, tier S), THB million
# source file: T4/osotspa_financial_highlights.md (company page, P)
osp = {
    "2023": {"sales": 26062, "gp": 9003, "profit_year": 2423, "attrib": 2402},
    "2024": {"sales": 27069, "gp": 10103, "profit_year": 1758, "attrib": 1638},
    "2025": {"sales": 25561, "gp": 10262, "profit_year": 3854, "attrib": 3667},
}
osp_out = {}
for y, d in osp.items():
    osp_out[y] = {
        "gross_margin_pct": pct(d["gp"], d["sales"]),
        "net_margin_profit_for_year_pct": pct(d["profit_year"], d["sales"]),
        "net_margin_attributable_pct": pct(d["attrib"], d["sales"]),
    }

# Thai Beverage PCL, consolidated, fiscal year to 30 September, THB million
# source files: T4/thaibev_fy2024_yearend_sgx_extract.md (FY2023 restated, FY2024),
#               T4/thaibev_fy2025_yearend_sgx_extract.md (FY2025, FY2024 as restated there)
group = {
    "FY2023": {"sales": 332931, "gp": 98687, "profit_year": 35063, "attrib": 27434},
    "FY2024": {"sales": 340289, "gp": 103208, "profit_year": 35270, "attrib": 27215},
    "FY2025": {"sales": 333286, "gp": 103508, "profit_year": 31153, "attrib": 25361},
}
nab = {
    "FY2023": {"sales": 63143, "gp": 21323, "ebitda": 10180, "profit_year": 5430, "attrib": 1196},
    "FY2024": {"sales": 65802, "gp": 23688, "ebitda": 11553, "profit_year": 5934, "attrib": 1455,
               "attrib_restated_in_fy2025_filing": 1146},
    "FY2025": {"sales": 64774, "gp": 23694, "ebitda": 11308, "profit_year": 5141, "attrib": 2414},
}
# FY2025 sales by segment, printed in the narrative of the saved FY2025 extract (spirits 118,604 at its line 187; beer
# 123,222 at line 202; non-alcoholic 64,774 at line 218; food 21,899 at line 232; others 4,999 at line 245) and the
# elimination of (212) in the revenue row of the segment table (line 101). Sum check below.
fy2025_segment_sales = {"spirits": 118604, "beer": 123222, "non_alcoholic": 64774, "food": 21899, "others": 4999,
                        "eliminations": -212}
# FY2025 segment gross profit as printed in the table of the saved extract (line 103 and the narrative, lines 190 and 206)
fy2025_segment_gp = {"spirits": 40139, "beer": 29791, "non_alcoholic": 23694, "food": 8597, "others": 1311,
                     "eliminations": -24}
group_out, nab_out = {}, {}
for y, d in group.items():
    group_out[y] = {
        "gross_margin_pct": pct(d["gp"], d["sales"]),
        "net_margin_profit_for_year_pct": pct(d["profit_year"], d["sales"]),
        "net_margin_attributable_pct": pct(d["attrib"], d["sales"]),
    }
for y, d in nab.items():
    nab_out[y] = {
        "gross_margin_pct": pct(d["gp"], d["sales"]),
        "ebitda_margin_pct": pct(d["ebitda"], d["sales"]),
        "net_margin_profit_for_year_pct": pct(d["profit_year"], d["sales"]),
        "net_margin_attributable_pct": pct(d["attrib"], d["sales"]),
        "share_of_group_sales_pct": pct(d["sales"], group[y]["sales"]),
    }
nab_out["FY2024"]["net_margin_attributable_restated_pct"] = pct(1146, 65802)
fy2025_checks = {
    "segment_sales_sum": sum(fy2025_segment_sales.values()),
    "group_sales_printed": group["FY2025"]["sales"],
    "segment_sales_sum_equals_group": sum(fy2025_segment_sales.values()) == group["FY2025"]["sales"],
    "segment_gross_profit_sum": sum(fy2025_segment_gp.values()),
    "group_gross_profit_printed": group["FY2025"]["gp"],
    "segment_gross_profit_sum_equals_group": sum(fy2025_segment_gp.values()) == group["FY2025"]["gp"],
    "non_alcoholic_gross_margin_pct": pct(fy2025_segment_gp["non_alcoholic"], fy2025_segment_sales["non_alcoholic"]),
}

# Retail groups (aggregator, S), fiscal year to 31 December, THB million
# source file: T4/retail_groups_financials_stockanalysis_2026-10-20.md
retail = {
    "CP Axtra PCL": {"2023": (486472, 78198, 8640), "2024": (508745, 83675, 10569), "2025": (517802, 83265, 9356)},
    "Berli Jucker PCL": {"2023": (157020, 32392, 4795), "2024": (160068, 34304, 4001), "2025": (156272, 33700, 4011)},
    "Central Retail Corporation PCL": {"2023": (248391, 82837, 8016), "2024": (243971, 77160, 8136), "2025": (246075, 77905, 7411)},
}
retail_out = {}
for name, yrs in retail.items():
    retail_out[name] = {
        y: {"gross_margin_pct": pct(gp, s), "net_margin_pct": pct(ni, s)} for y, (s, gp, ni) in yrs.items()
    }

# Sermsuk PCL, consolidated, fiscal year to 30 September, THB million (revenue from sales and services, cost of sales and
# services, net profit). Source file: T4/sermsuk_filings_extract_via_T3.md (company MD&A to the SET, P).
ssc = {
    "FY2022": (10905, 7824, 13),
    "FY2023": (12371, 8870, 248),
    "FY2024": (13153, 9306, 404),
}
ssc_out = {}
for y, (rev, cost, ni) in ssc.items():
    ssc_out[y] = {
        "gross_profit": rev - cost,
        "gross_margin_pct": pct(rev - cost, rev),
        "net_margin_pct": pct(ni, rev),
    }

# Prices per 330 mL (price / pack count / can size * 330). Source files named in the label.
# Lemon-lime and Singha rows are in xref_rows below (cross-reference block), not here.
prices = [
    ("est Cola 325 mL, 6 pack THB 79, Makro (T4/est_retail_listings_makro_7eleven_2026-10-20.md; not deliverable to the area selected)", 79, 6, 325),
    ("est Cola 325 mL, 6 pack THB 138, 7-Eleven online (T4/est_retail_listings_makro_7eleven_2026-10-20.md)", 138, 6, 325),
    ("est Sugar Free 325 mL, 6 pack THB 99, Sermsuk Click on Lazada (T4/est_priceza_listing_2026-10-20.md)", 99, 6, 325),
    ("est Kamikaze Lime 325 mL, 24 pack THB 408, Lazada reseller (T4/est_priceza_listing_2026-10-20.md)", 408, 24, 325),
    ("M-150 Sparkling Pink Lemonade 245 mL, single THB 20, Lotus's Shop Online (T4/lemon_lime_soda_listings_priceza_2026-10-20.md)", 20, 1, 245),
    ("M-150 Sparkling Pink Lemonade 245 mL, 6 pack THB 105, Lotus's Shop Online (T4/lemon_lime_soda_listings_priceza_2026-10-20.md)", 105, 6, 245),
    ("Chang Soda 325 mL, 24 pack THB 180, Makro PRO (T4/lemon_lime_soda_listings_priceza_2026-10-20.md)", 180, 24, 325),
    ("Rock Mountain Soda 325 mL, single THB 10, Lotus's Shop Online (T4/lemon_lime_soda_listings_priceza_2026-10-20.md)", 10, 1, 325),
    ("Fanta Red Lime Soda 500 mL, single THB 19, Lotus's Shop Online (T4/lemon_lime_soda_listings_priceza_2026-10-20.md)", 19, 1, 500),
    ("Nestle Pure Life Soda Plus Lemon Lime 330 mL, 24 tray THB 377, 7-Eleven online, out of stock (T5/r32_7eleven_nestle_pure_life_soda_lemon_lime_out_of_stock.md; read by T5)", 377, 24, 330),
    ("Castown craft soda lemonade 265 mL, single bottle THB 59, Lazada (T4/castown_craft_soda_priceza_2026-10-20.md)", 59, 1, 265),
    ("San Pellegrino Limonata 330 mL, 4 pack THB 255, Lazada (T4/lemon_lime_soda_listings_priceza_2026-10-20.md)", 255, 4, 330),
    ("Limca lemon 250 mL, single THB 45, Lazada India Mart seller (T4/lemon_lime_soda_listings_priceza_2026-10-20.md)", 45, 1, 250),
    ("Wanglaoji green lime soda drink 330 mL, 12 pack THB 280, Shopee (T4/lemon_lime_soda_listings_priceza_2026-10-20.md; origin not established)", 280, 12, 330),
    ("เซียโล่ honey lime soda 600 mL, 12 pack THB 159, ALL ONLINE (T4/lemon_lime_soda_listings_priceza_2026-10-20.md; brand name as printed in Thai, owner not established)", 159, 12, 600),
]
# Round 4: Singha Soda (plain soda) is sold in 325 mL bottles, not cans (T5 rows r28, r29, r30; 7-Eleven, Lotus's, Makro PRO)
prices += [
    ("Singha Soda 325 mL bottle, 24 pack THB 195, 7-Eleven ALL Online (T5/r28_7eleven_singha_soda_24bottle.md; retailer page, tier S)", 195, 24, 325),
    ("Singha Soda 325 mL bottle, 24 pack THB 190, Makro PRO (T5/r30_makro_singha_soda_24bottle.md)", 190, 24, 325),
    ("Singha Soda 325 mL bottle, 6 pack THB 48, Lotus's Shop Online (T5/r29_lotuss_singha_soda_6bottle.md; container read from the size and the other retailers)", 48, 6, 325),
]
price_out = []
for label, total, n, ml in prices:
    per_can = total / n
    price_out.append({
        "item": label,
        "thb_per_pack_unit": r2_half_up(per_can),
        "thb_per_330ml": r2_half_up(per_can * 330.0 / ml),
        "thb_per_litre": round(per_can * 1000.0 / ml, 1),
    })

# ---------------------------------------------------------------------------------------------------------------
# Cross-reference rows (round 3): sugar-free lemon-lime cans of the Coca-Cola and Pepsi systems (records 68a and 68b),
# the proposer's Singha Lemon Soda listings at Lotus's, the Schweppes lime soda listings, and a dated 2022 price.
# Each row is typed from the saved page named in its last field (the T2 and T5 raw folders hold the pages).
# Fields: id, description, shown price THB, pack count, unit mL, group, saved source
# Groups: sugar_free_sprite and sugar_free_7up feed the 2026 lemon-lime bands; singha_lemon_soda feeds the Singha band;
# the other groups are shown but are not in any band.
# ---------------------------------------------------------------------------------------------------------------
xref_rows = [
    ("SF01", "Sprite No Sugar 325 mL x24, Coca-Cola Official Store (LazMall), Priceza row 9",
     334, 24, 325, "sugar_free_sprite", "T2/priceza_sprite_2026-10-20.md (row 9; struck price 384)"),
    ("SF02", "Sprite No Sugar 325 mL x24 (Sprite Soft Drink No Sugar 325 ml Pack 24), Lazada listing, seller not stated",
     365, 24, 325, "sugar_free_sprite", "T2/retail_prices_2026-10-20.md (Lazada rows; struck price 384)"),
    ("SF03", "Sprite No Sugar 325 mL x24, Fresh Mart, Priceza row 18",
     414, 24, 325, "sugar_free_sprite", "T2/priceza_sprite_2026-10-20.md (row 18; struck price 828)"),
    ("SF04", "Sprite No Sugar 325 mL x24, CR7 ManU, Priceza row 10",
     456, 24, 325, "sugar_free_sprite", "T2/priceza_sprite_2026-10-20.md (row 10)"),
    ("SF05", "7UP No Sugar lemon soda 325 mL x24, Suntory PepsiCo official store, LazMall, Priceza row 17",
     293, 24, 325, "sugar_free_7up", "T5/r23_priceza_7up_listing.md (row 17; struck price 384)"),
    ("SF06", "7UP No Sugar lemon soda 325 mL x12, Suntory PepsiCo official store, LazMall, Priceza row 20",
     161, 12, 325, "sugar_free_7up", "T5/r23_priceza_7up_listing.md (row 20; struck price 192)"),
    ("SF07", "7UP Zero Sugar Lemon Soda 325 mL x6, Lotus's Shop Online (list price 80)",
     75, 6, 325, "sugar_free_7up", "T5/r09_lotuss_7up_zero_325_6can.md"),
    ("SF08", "7UP No Sugar lemon soda 325 mL x6, Suntory PepsiCo official store, LazMall, Priceza row 21",
     96, 6, 325, "sugar_free_7up", "T5/r23_priceza_7up_listing.md (row 21)"),
    ("SG01", "Singha Lemon Soda 330 mL single can, Lotus's Shop Online (proposer's product; retailer price)",
     17, 1, 330, "singha_lemon_soda", "T2/lotus_singha_lemon_soda_can_2026-10-20.md; T5/r10_lotuss_singha_lemon_single_can.md"),
    ("SG02", "Singha Lemon Soda 330 mL x6, Lotus's Shop Online (list price 85; member price 81)",
     85, 6, 330, "singha_lemon_soda", "T5/r06_lotuss_singha_lemon_6can.md"),
    ("SG03", "Singha Lemon Soda 330 mL x24, Lotus's Shop Online (pack reading DERIVED from a per-each label)",
     330, 24, 330, "singha_lemon_soda", "T5/r05_lotuss_singha_lemon_24can.md"),
    ("SW01", "Schweppes Lime Soda no sugar 330 mL x12, Coca-Cola Official Store, LazMall, Priceza row 15",
     196, 12, 330, "schweppes_lime_sugar_free", "T5/priceza_aggregator_2026-10-20.md (P4, product 10615542238); T5/r24_priceza_schweppes_listing.md (row 15)"),
    ("SW02", "Schweppes Lime Soda Zero Sugar 330 mL x6, Makro PRO (unavailable in the area selected; excluded)",
     84, 6, 330, "excluded_unavailable", "T5/r33_makro_schweppes_lime_zero_unavailable.md"),
    ("SL01", "Sprite Lemon Plus 325 mL single can, 2022 price (dated; excluded from 2026 bands)",
     15, 1, 325, "excluded_dated_2022", "T5/r27_thaiger_sprite_lemon_plus_2022.md"),
]
# Round 4 rows: Schweppes lime (sugar-free and regular), further Singha Lemon Soda retail rows (Makro PRO, 7-Eleven,
# Lotus's), the Singha lemon range variants on the same search pages (T6 file), Singha Sparkling Water Lime and the
# Lazada third-party rows (excluded from bands). Each row is typed from the saved file named in its last field.
xref_rows_r4 = [
    ("SW01R", "Schweppes Lime Soda 330 mL x12, regular (no sugar wording in the name), Coca-Cola Official Store, LazMall (product 10247417739)",
     196, 12, 330, "schweppes_lime_regular", "T5/priceza_aggregator_2026-10-20.md (P4)"),
    ("SW03", "Schweppes Lime Soda no sugar 330 mL x24, Coca-Cola Official Store, LazMall (product 10615452638; delivery limited to Bangkok metro, Nonthaburi and Chonburi)",
     351, 24, 330, "schweppes_lime_sugar_free", "T5/priceza_aggregator_2026-10-20.md (P4); T5/r24_priceza_schweppes_listing.md (row 21)"),
    ("SW04", "Schweppes Lime Soda no sugar 330 mL x12, Lotus's Shop Online (Priceza row; the Lotus's page for this pack was not opened)",
     167, 12, 330, "schweppes_lime_sugar_free", "T5/priceza_aggregator_2026-10-20.md (P4); T5/r24_priceza_schweppes_listing.md (row 5)"),
    ("SW05", "Schweppes Lime Soda no sugar 330 mL x6, Lotus's Shop Online (Priceza row, product 51616830; page not opened)",
     85, 6, 330, "schweppes_lime_sugar_free", "T5/priceza_aggregator_2026-10-20.md (P4); T5/r24_priceza_schweppes_listing.md (row 7)"),
    ("SW06", "Schweppes Lime Soda 330 mL x6, regular, Lotus's Shop Online (Priceza row, product 15514234; page not opened)",
     85, 6, 330, "schweppes_lime_regular", "T5/priceza_aggregator_2026-10-20.md (P4); T5/r24_priceza_schweppes_listing.md (row 6)"),
    ("SW07", "Schweppes Soft Drink Lime Soda 330 mL x6, regular, Makro PRO (page read; no unavailability notice on this page)",
     84, 6, 330, "schweppes_lime_regular", "T5/t5_recheck_makro_pro_2026-10-20.md (section 5)"),
    ("SW08", "Schweppes Lime Soda Zero Sugar 330 mL x6, 7-Eleven ALL Online (page shows 170, struck 190; 28.33 a can, unreconciled outlier)",
     170, 6, 330, "excluded_outlier", "T5/r13_7eleven_schweppes_lime_zero_6can.md; T5/t5_recheck_7eleven_allonline_2026-10-20.md (section 3)"),
    ("SW09", "Schweppes Manao Soda 330CC single can, Lotus's Shop Online page (name carries no sugar-free wording; Priceza shows 17 for the same code and the page governs)",
     18, 1, 330, "schweppes_lime_regular", "T5/r11_lotuss_schweppes_manao_lime_single.md; T5/r24_priceza_schweppes_listing.md (row 4)"),
    ("SG04", "Singha Lemon Soda 330 mL x6, Makro PRO (single-pack price 82; the buy-3-or-more figure of 78 is not used)",
     82, 6, 330, "singha_lemon_retail", "T5/r04_makro_singha_lemon_6can.md; T5/t5_recheck_makro_pro_2026-10-20.md (section 2)"),
    ("SG05", "Singha Lemon Soda 330 mL x24, Makro PRO (325; 330 shown as the earlier price)",
     325, 24, 330, "singha_lemon_retail", "T5/r03_makro_singha_lemon_24can.md; T5/t5_recheck_makro_pro_2026-10-20.md (section 1)"),
    ("SG06", "Singha Lemon Soda 330 mL x24, 7-Eleven ALL Online (330; 408 shown as the earlier price)",
     330, 24, 330, "singha_lemon_retail", "T5/r01_7eleven_singha_lemon_24can.md; T5/t5_recheck_7eleven_allonline_2026-10-20.md (section 1)"),
    ("SG07", "Singha Lemon Soda 330 mL x6, 7-Eleven ALL Online (172; 182 shown as the earlier price; 28.67 a can, unreconciled outlier)",
     172, 6, 330, "singha_lemon_outlier", "T5/r02_7eleven_singha_lemon_6can.md; T5/t5_recheck_7eleven_allonline_2026-10-20.md (section 2)"),
    ("SG08", "Singha Lemon Soda 330 mL x6, Lotus's Shop Online as printed by Priceza (83; the Lotus's page read gives 85 and governs)",
     83, 6, 330, "excluded_conflict", "T5/priceza_aggregator_2026-10-20.md (P5)"),
    ("SG09", "Singha Lemon Soda 330 mL x6, Lazada third-party seller (114; not a retailer of record)",
     114, 6, 330, "excluded_third_party", "T5/priceza_aggregator_2026-10-20.md (P5)"),
    ("SG10", "Singha Lemon Soda 330 mL x6, Lazada third-party seller (126; not a retailer of record)",
     126, 6, 330, "excluded_third_party", "T5/priceza_aggregator_2026-10-20.md (P5)"),
    ("SG11", "Singha Lemon Soda 330 mL x24, Lazada third-party seller (369; not a retailer of record)",
     369, 24, 330, "excluded_third_party", "T5/priceza_aggregator_2026-10-20.md (P5)"),
    ("SG12", "Singha Lemon Soda 330 mL single, Lazada third-party seller (16; not a retailer of record)",
     16, 1, 330, "excluded_third_party", "T5/priceza_aggregator_2026-10-20.md (P5)"),
    ("SG13", "Singha Lemon Soda 330 mL single, Lazada third-party seller (17; not a retailer of record)",
     17, 1, 330, "excluded_third_party", "T5/priceza_aggregator_2026-10-20.md (P5)"),
    ("VR01", "Singha Red Lemon Soda 330 mL x6, Makro PRO (79)", 79, 6, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Makro PRO table)"),
    ("VR02", "Singha Lemon Cream Soda 330 mL x6, Makro PRO (79)", 79, 6, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Makro PRO table)"),
    ("VR03", "Singha Pink Lemon Soda 330 mL x6, Makro PRO (82)", 82, 6, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Makro PRO table)"),
    ("VR04", "Singha Ume Lemon Soda 330 mL x6, Makro PRO (82)", 82, 6, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Makro PRO table)"),
    ("VR05", "Singha Pink Lemon Soda 330 mL x24, Makro PRO (325)", 325, 24, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Makro PRO table)"),
    ("VR06", "Singha Red Lemon Soda 330 mL x24, Makro PRO (325)", 325, 24, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Makro PRO table)"),
    ("VR07", "Singha Pink Lemon Soda 330 mL x24, Lotus's Shop Online (337)", 337, 24, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Lotus's table)"),
    ("VR08", "Singha Pink Lemon Soda 330 mL x24, 7-Eleven ALL Online (330)", 330, 24, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (7-Eleven table)"),
    ("VR09", "Singha Ume Lemon Soda 330 mL x24, 7-Eleven ALL Online (330)", 330, 24, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (7-Eleven table)"),
    ("VR10", "Singha Red Lemon Soda 330 mL x24, 7-Eleven ALL Online (330)", 330, 24, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (7-Eleven table)"),
    ("VR11", "Singha Watermelon Lemon Soda 330 mL x24, 7-Eleven ALL Online (330; 342 shown as the earlier price)", 330, 24, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (7-Eleven table)"),
    ("VR12", "Singha Lemon Cream Soda 330 mL x24, 7-Eleven ALL Online (330; 400 shown as the earlier price)", 330, 24, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (7-Eleven table)"),
    ("VR13", "Singha Red Lemon Soda (Thai name says no sugar) 330 mL single, Lotus's Shop Online (17)", 17, 1, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Lotus's table)"),
    ("VR14", "Singha Pink Lemon Soda 330 mL single, Lotus's Shop Online (17)", 17, 1, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Lotus's table)"),
    ("VR15", "Singha Lemon Cream Soda 330 mL single, Lotus's Shop Online (17)", 17, 1, 330, "singha_variant", "T6/04_retail_listings_2026-10-20.md (Lotus's table)"),
    ("VR16", "Singha Red Lemon Soda 330 mL x6, 7-Eleven ALL Online (172; the same anomaly as the lemon six-pack, not used)", 172, 6, 330, "singha_variant_outlier", "T6/04_retail_listings_2026-10-20.md (7-Eleven table)"),
    ("LW01", "Singha Sparkling Water Lime 330 mL x24, 7-Eleven ALL Online (302; 304 shown as the earlier price)", 302, 24, 330, "singha_lime_water", "T5/r14_7eleven_singha_sparkling_lime_24can.md; T5/t5_recheck_7eleven_allonline_2026-10-20.md (section 4)"),
    ("LW02", "Singha Sparkling Water Lime 330 mL x24, Makro PRO (312; 319 shown as the list price)", 312, 24, 330, "singha_lime_water", "T5/r20_makro_singha_sparkling_lime_24can.md; T5/t5_recheck_makro_pro_2026-10-20.md (section 8)"),
    ("LW03", "Singha Sparkling Water Lime 330 mL can, launch price of March 2026 (a launch price, not a shelf price)", 15, 1, 330, "singha_lime_launch", "T5/t5_recheck_brands_press_2026-10-20.md (section 5)"),
]
xref_rows += xref_rows_r4
xref_out = []
xref_groups = {}
for rid, desc, shown, n, ml, grp, src in xref_rows:
    per_unit = shown / n
    p330 = r2_half_up(per_unit * 330.0 / ml)
    xref_out.append({
        "id": rid, "item": desc, "group": grp, "source": src, "shown_price_thb": shown, "pack_count": n,
        "unit_ml": ml, "thb_per_pack_unit": r2_half_up(per_unit), "thb_per_330ml": p330,
    })
    xref_groups.setdefault(grp, []).append(p330)
def _vals(*names):
    return [v for n in names for v in xref_groups.get(n, [])]


# Round 4 bands. Retail rows of record: Lotus's, Makro PRO and 7-Eleven (the Lazada third-party rows, the Priceza
# row at 83 and the 7-Eleven six-pack outlier are kept out of the bands and shown in the table).
xref_bands = {
    "sugar_free_sprite_no_sugar_24_pack_2026": band(_vals("sugar_free_sprite")),
    "sugar_free_7up_lemon_2026": band(_vals("sugar_free_7up")),
    "sugar_free_lemon_lime_cans_2026_all_listings": band(_vals("sugar_free_sprite", "sugar_free_7up")),
    "singha_lemon_soda_retail_of_record_2026": band(_vals("singha_lemon_soda", "singha_lemon_retail")),
    "singha_lemon_soda_retail_incl_7eleven_six_pack_outlier_2026": band(
        _vals("singha_lemon_soda", "singha_lemon_retail", "singha_lemon_outlier")),
    "singha_lemon_soda_same_range_variants_2026": band(_vals("singha_variant")),
    "schweppes_lime_sugar_free_2026": band(_vals("schweppes_lime_sugar_free")),
    "schweppes_lime_regular_2026": band(_vals("schweppes_lime_regular")),
    "singha_sparkling_water_lime_2026": band(_vals("singha_lime_water")),
    "sugar_free_lemon_and_lime_cans_2026_all_listings": band(
        _vals("sugar_free_sprite", "sugar_free_7up", "singha_lemon_soda", "singha_lemon_retail", "schweppes_lime_sugar_free")),
}

# ---------------------------------------------------------------------------------------------------------------
# est prices by pack format. Every row is typed from a page saved in rework/raw/diligence_2026-10-20/T4/ :
#   PZ = est_priceza_listing_2026-10-20.md  (Priceza est page, 24 of 100 items; Lazada, LazMall, Shopee, ALL ONLINE)
#   RT = est_retail_listings_makro_7eleven_2026-10-20.md  (Makro and 7-Eleven online)
#   LT = est_retail_listings_makro_7eleven_2026-10-20.md, Lotus's section (single units)
# Fields: id, description, shown price, pack count, unit mL, format, listed price (None if no discount shown), seller, source
# format "can" = 325 mL can pack; "bottle" = bottle multipack (PET or glass is not stated on any listing); "single" = one unit
# ---------------------------------------------------------------------------------------------------------------
est_rows = [
    ("E01", "est Cola 325 mL x6, Makro (listing says it cannot be delivered to the selected area)", 79, 6, 325, "can", None, "Makro", "RT"),
    ("E02", "est Cola 325 mL x6, 7-Eleven online", 138, 6, 325, "can", 176, "7-Eleven online", "RT"),
    ("E03", "est Sugar Free 325 mL x6, Sermsuk Click (LazMall)", 99, 6, 325, "can", None, "Sermsuk Click", "PZ"),
    ("E04", "est Strawberry red 325 mL x6, Sermsuk Click (LazMall)", 99, 6, 325, "can", None, "Sermsuk Click", "PZ"),
    ("E05", "est Kamikaze Lime 325 mL x24, CR7 ManU (Lazada reseller)", 408, 24, 325, "can", None, "CR7 ManU", "PZ"),
    ("E06", "est Cola 515 mL x24, 7-Eleven online", 309, 24, 515, "bottle", 345, "7-Eleven online", "RT"),
    ("E07", "est Cola 1 L x12, 7-Eleven online", 235, 12, 1000, "bottle", 239, "7-Eleven online", "RT"),
    ("E08", "est Cola 1.6 L x6, 7-Eleven online", 148, 6, 1600, "bottle", 159, "7-Eleven online", "RT"),
    ("E09", "est Kamikaze Lime 1 L x12, CR7 ManU", 264, 12, 1000, "bottle", None, "CR7 ManU", "PZ"),
    ("E10", "est Kamikaze Lime 360 mL x12, CR7 ManU", 144, 12, 360, "bottle", None, "CR7 ManU", "PZ"),
    ("E11", "est Play Kamikaze 360 mL x12, CR7 ManU (sale price)", 96, 12, 360, "bottle", 132, "CR7 ManU", "PZ"),
    ("E12", "est Sugar Free cola 1 L x12, third-party Lazada seller", 293, 12, 1000, "bottle", None, "Lazada seller", "PZ"),
    ("E13", "est Cocomansi (coconut and calamansi) 1.6 L x12, Sermsuk Click (LazMall, sale price)", 328, 12, 1600, "bottle", 348, "Sermsuk Click", "PZ"),
    ("E14", "est Electric Green (apple kiwi) 1.6 L x12, Sermsuk Click (LazMall)", 382, 12, 1600, "bottle", None, "Sermsuk Click", "PZ"),
    ("E15", "est Cream Soda Green 490 mL x12, Sermsuk Click (LazMall)", 215, 12, 490, "bottle", None, "Sermsuk Click", "PZ"),
    ("E16", "est Cola Cool Hand 250 mL x24, Sermsuk Click (LazMall)", 325, 24, 250, "bottle", None, "Sermsuk Click", "PZ"),
    ("E17", "est Salty Lychee 1 L x12, ALL ONLINE (sale price)", 204, 12, 1000, "bottle", 239, "ALL ONLINE", "PZ"),
    ("E18", "est Play Lychee plus vitamin B 1 L x12, CR7 ManU", 240, 12, 1000, "bottle", None, "CR7 ManU", "PZ"),
    ("E19", "est Play Grapeberry 1 L x12, Fresh Mart (50 percent off)", 295, 12, 1000, "bottle", 590, "Fresh Mart", "PZ"),
    ("E20", "est Play Kamikaze 1 L x12, US Mart (50 percent off)", 341, 12, 1000, "bottle", 682, "US Mart", "PZ"),
    ("E21", "est Cola 1.6 L x6, Fresh Mart (50 percent off)", 203, 6, 1600, "bottle", 406, "Fresh Mart", "PZ"),
    ("E22", "est Cola 360 mL x12, WHOLESALER SHOP (50 percent off)", 169, 12, 360, "bottle", 338, "WHOLESALER SHOP", "PZ"),
    ("E23", "est Play Orange 360 mL x12, Malee Supermart (50 percent off)", 159, 12, 360, "bottle", 318, "Malee Supermart", "PZ"),
    ("E24", "est Cola 250 mL x24, Fresh Mart (50 percent off)", 294, 24, 250, "bottle", 588, "Fresh Mart", "PZ"),
    ("E25", "est Cola 250 mL x24, Malee Supermart (50 percent off)", 307, 24, 250, "bottle", 614, "Malee Supermart", "PZ"),
    ("E26", "est Cream Soda 325 mL single, Lotus's Shop Online (sale price, container not stated)", 13, 1, 325, "single", 15, "Lotus's Shop Online", "LT"),
    ("E27", "est Cream Soda 1 L single, GROCER LOCK", 21, 1, 1000, "single", None, "GROCER LOCK", "PZ"),
    ("E28", "est Cream Soda 1.6 L single, Lotus's Shop Online", 29, 1, 1600, "single", None, "Lotus's Shop Online", "LT"),
]
# Not used (price per option not shown on the listing): Top UP Now 360 mL rows "1 bottle or 4 bottles" (THB 14.35 sale; THB 59).


def size_class(fmt, ml):
    if fmt == "can":
        return "can pack (325 mL)"
    if fmt == "single":
        return "single unit"
    if ml >= 1000:
        return "bottle multipack, 1 L and above"
    if ml >= 360:
        return "bottle multipack, 360 to 515 mL"
    return "bottle multipack, 250 mL"


est_out = []
for rid, desc, price, n, ml, fmt, listed, seller, src in est_rows:
    per_unit = price / n
    off = None if listed is None else round(100.0 * (listed - price) / listed, 1)
    est_out.append({
        "id": rid, "item": desc, "format": fmt, "size_class": size_class(fmt, ml), "source_code": src, "seller": seller,
        "shown_price_thb": price, "listed_price_thb": listed, "discount_pct": off,
        "thb_per_pack_unit": round(per_unit, 2),
        "thb_per_330ml": round(per_unit * 330.0 / ml, 2),
        "thb_per_litre": round(per_unit * 1000.0 / ml, 1),
        "promotion_50pct_or_more": (off is not None and off >= 50.0),
    })


est_bands = {}
for cls in ["can pack (325 mL)", "bottle multipack, 1 L and above", "bottle multipack, 360 to 515 mL",
            "bottle multipack, 250 mL", "single unit"]:
    rows = [r for r in est_out if r["size_class"] == cls]
    est_bands[cls] = {"all_rows": band([r["thb_per_330ml"] for r in rows])}
    no_promo = [r for r in rows if not r["promotion_50pct_or_more"]]
    if no_promo and len(no_promo) != len(rows):
        est_bands[cls]["excluding_50pct_promotions"] = band([r["thb_per_330ml"] for r in no_promo])
all_bottle_packs = [r for r in est_out if r["format"] == "bottle"]
est_bands["all bottle multipacks (every size)"] = {
    "all_rows": band([r["thb_per_330ml"] for r in all_bottle_packs]),
    "excluding_50pct_promotions": band([r["thb_per_330ml"] for r in all_bottle_packs if not r["promotion_50pct_or_more"]]),
}
# Round 3: the can listings without E01 (Makro, not deliverable to the area selected when read)
deliverable_cans = [r for r in est_out if r["format"] == "can" and r["id"] != "E01"]
est_bands["can pack (325 mL), excluding E01 (Makro, not deliverable to the area selected)"] = {
    "all_rows": band([r["thb_per_330ml"] for r in deliverable_cans])}
# Round 3: bottle multipacks of 360 mL and above (the 1 L class and the 360 to 515 mL class together)
big_bottles = [r for r in est_out if r["format"] == "bottle" and r["size_class"] in
               ("bottle multipack, 1 L and above", "bottle multipack, 360 to 515 mL")]
est_bands["bottle multipacks, 360 mL and above (round 3 combined)"] = {
    "all_rows": band([r["thb_per_330ml"] for r in big_bottles]),
    "excluding_50pct_promotions": band([r["thb_per_330ml"] for r in big_bottles if not r["promotion_50pct_or_more"]]),
}
cube_price_assumption = 15.0  # deck slide 8 base case (ASSUMPTION), THB per serve
est_vs_cube = {
    "cube_price_thb_assumption": cube_price_assumption,
    "can_rows_at_or_below_cube_price": sum(1 for r in est_out if r["format"] == "can" and r["thb_per_330ml"] <= cube_price_assumption),
    "can_rows_total": sum(1 for r in est_out if r["format"] == "can"),
    "can_rows_deliverable_at_or_below_cube_price": sum(1 for r in deliverable_cans if r["thb_per_330ml"] <= cube_price_assumption),
    "can_rows_deliverable_total": len(deliverable_cans),
    "bottle_multipack_rows_below_cube_price": sum(1 for r in all_bottle_packs if r["thb_per_330ml"] < cube_price_assumption),
    "bottle_multipack_rows_total": len(all_bottle_packs),
    "bottle_multipack_rows_below_half_cube_price": sum(1 for r in all_bottle_packs if r["thb_per_330ml"] < cube_price_assumption / 2.0),
    "bottle_250ml_rows_above_cube_price": sum(1 for r in est_out if r["size_class"] == "bottle multipack, 250 mL" and r["thb_per_330ml"] > cube_price_assumption),
    "bottle_250ml_rows_total": sum(1 for r in est_out if r["size_class"] == "bottle multipack, 250 mL"),
    "promotion_rows_50pct_or_more": sum(1 for r in est_out if r["promotion_50pct_or_more"]),
    "est_rows_total": len(est_out),
}

# Coloured soda share check (Thansettakij 13 October 2025; saved: est_thansettakij_2025-10-13_share_and_glow.md)
coloured = {
    "coloured_soda_value_thb_million": 17391,
    "total_soda_value_2024_thb_million": 68000,
    "computed_share_pct": pct(17391, 68000),
    "share_printed_by_source_pct": 30,
    "value_if_30pct_of_68000_thb_million": round(0.30 * 68000, 0),
    "gotomanager_2023_printed_coloured_share_pct": 25,
    "note": "The article's 30 percent does not reconcile with its own two figures (25.6 percent computed); Gotomanager (29 October 2023) prints 25 percent.",
}

# Sermsuk carbonated drink revenue (Form 250-2 PDF page 11, tier P; saved: sermsuk_filings_extract_via_T3.md section D3)
ssc_csd = {
    "FY2021": (3708.03, 9618.49), "FY2022": (3972.69, 10904.85), "FY2023": (4550.15, 12371.03), "9M2024": (3964.26, 9926.54),
}
ssc_csd_out = {k: {"carbonated_revenue_thb_million": a, "total_revenue_thb_million": b, "carbonated_share_pct": pct(a, b)}
               for k, (a, b) in ssc_csd.items()}
ssc_csd_out["FY2023_vs_FY2022_growth_pct"] = pct(4550.15 - 3972.69, 3972.69)
# Form 250-2 PDF page 63 (assumption table of the independent financial adviser; not audited; saved section D6)
ssc_vol_m_litres_fy2024 = 275.60
ssc_price_thb_per_litre = 18.42
thai_csd_consumption_m_litres = 2100.0   # Marketeer 15 March 2024, year before March 2024 (S; est_market_2023_2025_brandbuffet_marketeer_thansettakij.md)
ssc_proxy = {
    "carbonated_volume_FY2024_million_litres_IFA_base": ssc_vol_m_litres_fy2024,
    "carbonated_average_selling_price_thb_per_litre_IFA_assumption": ssc_price_thb_per_litre,
    "price_per_330ml_thb": round(ssc_price_thb_per_litre * 0.33, 2),
    "volume_over_thai_csd_consumption_pct_upper_bound_proxy": pct(ssc_vol_m_litres_fy2024, thai_csd_consumption_m_litres),
    "caveats": "The carbonated line covers est, 100 Plus and Sarsi, so it is an upper bound for est alone; the volume is the adviser's FY2024 base including a July to September 2024 estimate; the 2,100 million litres is Marketeer's figure for a different 12 months; this is not a share figure.",
}

# Osotspa top-10 shareholders as of 28 August 2026 (osotspa_major_shareholders_2026-08-28.md): six Osathanugrah holders
osp_family = [24.07, 3.14, 3.10, 2.84, 2.52, 2.51]

osp_sales_change_2025_vs_2024_pct = pct(osp["2025"]["sales"] - osp["2024"]["sales"], osp["2024"]["sales"])

# Round 4: the Singha Lemon Soda retail rows of record against the THB 15 cube price (ASSUMPTION)
singha_retail_vals = _vals("singha_lemon_soda", "singha_lemon_retail")
singha_vs_cube = {
    "cube_price_thb_assumption": cube_price_assumption,
    "singha_lemon_retail_rows": len(singha_retail_vals),
    "singha_lemon_retail_rows_at_or_below_cube_price": sum(1 for v in singha_retail_vals if v <= cube_price_assumption),
    "singha_lemon_retail_rows_above_cube_price": sum(1 for v in singha_retail_vals if v > cube_price_assumption),
    "makro_can_row_E01_per_330ml_at_or_below_cube_price": est_out[0]["thb_per_330ml"] <= cube_price_assumption,
    "est_can_deliverable_min_per_330ml": min(r["thb_per_330ml"] for r in deliverable_cans),
}

results = {
    "osotspa_sales_change_2025_vs_2024_pct": osp_sales_change_2025_vs_2024_pct,
    "osotspa_osathanugrah_holders_in_top10_pct": round(sum(osp_family), 2),
    "inputs_note": "All inputs typed from saved pages in rework/raw/diligence_2026-10-20/T4 (read 20 October 2026), and for the cross-referenced rows from the T2 and T5 folders named per row.",
    "osotspa_margins_on_revenue_from_sales": osp_out,
    "thaibev_group_margins": group_out,
    "thaibev_non_alcoholic_segment_margins": nab_out,
    "thaibev_fy2025_segment_checks": fy2025_checks,
    "sermsuk_consolidated_margins": ssc_out,
    "retail_group_margins_aggregator_S": retail_out,
    "prices_per_330ml": price_out,
    "lemon_lime_and_singha_cross_reference_2026": {"rows": xref_out, "bands_per_330ml": xref_bands},
    "est_price_rows_by_format": est_out,
    "est_price_bands_per_330ml": est_bands,
    "est_vs_cube_price": est_vs_cube,
    "singha_lemon_vs_cube_price": singha_vs_cube,
    "coloured_soda_share_check": coloured,
    "sermsuk_carbonated_revenue_p": ssc_csd_out,
    "sermsuk_carbonated_volume_price_proxy": ssc_proxy,
}
with open(os.path.join(HERE, "t4_competitor_margins_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(json.dumps({k: results[k] for k in ["lemon_lime_and_singha_cross_reference_2026", "est_price_bands_per_330ml",
                                          "est_vs_cube_price", "thaibev_fy2025_segment_checks"]},
                 indent=1, ensure_ascii=False))
