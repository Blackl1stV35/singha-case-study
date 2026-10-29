"""T6 slide 4 arithmetic: price per can and per litre, brand volume, can-maker cross-check, reach counts, group ratios.

Every input below is copied from a saved page in rework/raw/diligence_2026-10-20/T6/ (the file is named on each line).
Nothing is estimated. There is no random draw, so no seed is needed. Run: python t6_can_leverage_calc.py
Writes t6_can_leverage_results.json next to this script. Memory use is a few MB.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "t6_can_leverage_results.json"
MODEL = HERE / "can_cost_model_results.json"

CAN_L = 0.33  # litres in one 330 mL can


def per(price, cans):
    """Return (THB per can, THB per litre) for a pack price."""
    pc = price / cans
    return round(pc, 2), round(pc / CAN_L, 2)


res = {"note": "DERIVED arithmetic on figures saved in rework/raw/diligence_2026-10-20/T6/. Tiers sit in rework/69."}

# ---- 1. Price per can and per litre (file 04_retail_listings_2026-10-20.md, read 20 Oct 2026) -------
# Each row: (retailer, flavour, pack, price in THB, cans, flag). flag is "" for a normal one-pack price,
# "member" for the Lotus's Club Card member price, "list" for a struck-through list price,
# "anomaly" for a listing that is out of line with every other price read (not used in any range),
# "qty_tier" for a bulk price at Makro Pro (not used in any range).
listings = [
    ("Lotus's", "Lemon", "single", 17.00, 1, ""),
    ("Lotus's", "Red", "single", 17.00, 1, ""),
    ("Lotus's", "Pink", "single", 17.00, 1, ""),
    ("Lotus's", "Lemon Cream", "single", 17.00, 1, ""),
    ("Lotus's", "Lemon", "pack6", 85.00, 6, ""),
    ("Lotus's", "Lemon", "pack6", 81.00, 6, "member"),
    ("Lotus's", "Lemon", "case24", 330.00, 24, ""),
    ("Lotus's", "Pink", "case24", 337.00, 24, ""),
    ("Makro Pro", "Lemon", "pack6", 82.00, 6, ""),
    ("Makro Pro", "Lemon", "pack6", 78.00, 6, "qty_tier"),
    ("Makro Pro", "Red", "pack6", 79.00, 6, ""),
    ("Makro Pro", "Lemon Cream", "pack6", 79.00, 6, ""),
    ("Makro Pro", "Pink", "pack6", 82.00, 6, ""),
    ("Makro Pro", "Ume", "pack6", 82.00, 6, ""),
    ("Makro Pro", "Lemon", "case24", 325.00, 24, ""),
    ("Makro Pro", "Pink", "case24", 325.00, 24, ""),
    ("Makro Pro", "Red", "case24", 325.00, 24, ""),
    ("7-Eleven ALL Online", "Lemon", "case24", 330.00, 24, ""),
    ("7-Eleven ALL Online", "Lemon", "case24", 408.00, 24, "list"),
    ("7-Eleven ALL Online", "Watermelon", "case24", 330.00, 24, ""),
    ("7-Eleven ALL Online", "Watermelon", "case24", 342.00, 24, "list"),
    ("7-Eleven ALL Online", "Pink", "case24", 330.00, 24, ""),
    ("7-Eleven ALL Online", "Ume", "case24", 330.00, 24, ""),
    ("7-Eleven ALL Online", "Red", "case24", 330.00, 24, ""),
    ("7-Eleven ALL Online", "Lemon Cream", "case24", 330.00, 24, ""),
    ("7-Eleven ALL Online", "Lemon", "pack6", 172.00, 6, "anomaly"),
    ("7-Eleven ALL Online", "Lemon", "pack6", 182.00, 6, "anomaly"),
    ("7-Eleven ALL Online", "Red", "pack6", 172.00, 6, "anomaly"),
]
rows = []
for retailer, flavour, pack, price, cans, flag in listings:
    pc, pl = per(price, cans)
    rows.append({"retailer": retailer, "flavour": flavour, "pack": pack, "flag": flag,
                 "pack_price_thb": price, "cans": cans, "thb_per_can": pc, "thb_per_litre": pl})
res["price_per_can_and_litre"] = rows


def sel(**kw):
    """Rows matching every key=value in kw (flag compared exactly)."""
    return [r for r in rows if all(r[k] == v for k, v in kw.items())]


def rng(rs):
    v = [r["thb_per_can"] for r in rs]
    return {"min": min(v), "max": max(v), "n": len(v)}


def one_dec(x):
    return round(x + 1e-9, 1)


# Lemon-only ranges quoted on the slide. Used rows: flag "" (one-pack list price) or "member" (Club Card member price).
lemon_pack6_all = [r for r in sel(flavour="Lemon", pack="pack6") if r["flag"] in ("", "member")]
lemon_pack6_nonmember = sel(flavour="Lemon", pack="pack6", flag="")
lemon_case24 = sel(flavour="Lemon", pack="case24", flag="")
other_multi = [r for r in rows if r["flavour"] not in ("Lemon",) and r["pack"] in ("pack6", "case24") and r["flag"] == ""]
all_multi_used = [r for r in rows if r["pack"] in ("pack6", "case24") and r["flag"] in ("", "member")]
anomaly_rows = [r for r in rows if r["flag"] == "anomaly" and r["flavour"] == "Lemon" and r["pack"] == "pack6" and r["pack_price_thb"] == 172.0]
list_row = sel(retailer="7-Eleven ALL Online", flavour="Lemon", pack="case24", flag="list")[0]
tier_row = sel(retailer="Makro Pro", flavour="Lemon", pack="pack6", flag="qty_tier")[0]
res["price_ranges"] = {
    "single_can_lemon_lotus_thb": 17.0,
    "lemon_6pack_thb_per_can_member_to_nonmember": rng(lemon_pack6_all),
    "lemon_6pack_thb_per_can_nonmember_only": rng(lemon_pack6_nonmember),
    "lemon_24case_thb_per_can": rng(lemon_case24),
    "other_flavours_multipack_and_case_thb_per_can": rng(other_multi),
    "all_flavours_multipack_and_case_used_rows_thb_per_can": rng(all_multi_used),
    "lemon_case_list_price_thb_per_can_7eleven_online": list_row["thb_per_can"],
    "lemon_case_7eleven_online_discount_pct": round((list_row["pack_price_thb"] - 330.0) / list_row["pack_price_thb"] * 100, 1),
    "lotus_member_discount_on_6pack_pct": round((85.0 - 81.0) / 85.0 * 100, 1),
    "makro_qty_tier_6pack_thb_per_can_not_used": tier_row["thb_per_can"],
    "seven_eleven_lemon_6pack_anomaly_thb_per_can_not_used": anomaly_rows[0]["thb_per_can"],
    "slide_strings_one_decimal": {
        "lemon_6pack_min": one_dec(rng(lemon_pack6_all)["min"]),
        "lemon_6pack_max": one_dec(rng(lemon_pack6_all)["max"]),
        "lemon_case_min": one_dec(rng(lemon_case24)["min"]),
        "lemon_case_max": one_dec(rng(lemon_case24)["max"]),
        "other_flavours_min": one_dec(rng(other_multi)["min"]),
        "seven_eleven_lemon_6pack_anomaly": one_dec(anomaly_rows[0]["thb_per_can"]),
        "single_can_per_litre": round(17.0 / CAN_L, 1),
    },
    "reading": ("Lemon only: 6-packs THB 13.50 (Lotus's Club Card member price) to 14.17 (Lotus's non-member); "
                "24-can cases THB 13.54 to 13.75 (Makro Pro, Lotus's and 7-Eleven online). Other flavours read as low as "
                "THB 13.17 (Makro Pro Red and Lemon Cream 6-packs). The 7-Eleven online Lemon 6-pack (THB 28.67 a can) and "
                "the Makro Pro quantity price are not in these ranges."),
}
res["price_history"] = {
    "launch_price_thb_2020": 16, "red_aug_2022_thb": 16, "ume_sep_2023_thb": 17, "pink_jun_2024_thb": 17,
    "current_single_can_thb_20_oct_2026": 17,
    "rise_16_to_17_pct": round((17 - 16) / 16 * 100, 2),
    "per_litre_at_16": round(16 / CAN_L, 2), "per_litre_at_17": round(17 / CAN_L, 2),
}

# ---- 2. Brand volume (file 03_company_sales_statements.md) ----------------------------------------
l2021, l2022t = 28e6, 45e6
cans2021, cans2022t = l2021 / CAN_L, l2022t / CAN_L
retail_2021 = l2021 * (16 / CAN_L) / 1e6
can_segment_2021 = 13172.0  # THB million, press, 2021 canned carbonated drinks
res["brand_volume"] = {
    "litres_2021_million": 28, "litres_2022_target_million": 45,
    "cans_2021_million": round(cans2021 / 1e6, 1), "cans_2022_target_million": round(cans2022t / 1e6, 1),
    "target_growth_pct": round((45 / 28 - 1) * 100, 1),
    "retail_value_2021_at_thb16_million": round(retail_2021, 1),
    "press_sales_value_million_year_unclear": 1357,
    "difference_pct": round((1357 - retail_2021) / retail_2021 * 100, 2),
    "limited_edition_2_million_cans_in_million_litres": round(2e6 * CAN_L / 1e6, 2),
}
res["canned_segment_year_inference"] = {
    "csd_market_2021_thb_million_dated_in_source": 62725,
    "canned_share_pct_in_source": 21,
    "21pct_of_62725_thb_million": round(0.21 * 62725, 2),
    "canned_value_in_source_thb_million_year_not_stated": 13172,
    "difference_thb_million": round(0.21 * 62725 - 13172, 2),
    "reading": ("The source dates 62,725 to 2021 and gives 13,172 without a year. 21% of 62,725 is 13,172.25, so the year of 13,172 "
                "is INFERRED as 2021 by this arithmetic (Positioning, 4 July 2022, file 09 section C). It is not a printed date."),
}
res["share_arithmetic"] = {
    "1357_over_13172_pct": round(1357 / can_segment_2021 * 100, 1),
    "1450_over_13172_pct": round(1450 / can_segment_2021 * 100, 1),
    "12pct_of_13172_million": round(0.12 * can_segment_2021, 0),
    "1450_over_62725_total_csd_pct": round(1450 / 62725 * 100, 2),
}

# ---- 3. Can maker, BJC 56-1 One Report 2025 (file 08) ----------------------------------------------
tbc_cap = {"2023": 3440, "2024": 3780, "2025": 3880}
tbc_act = {"2023": 2027, "2024": 2214, "2025": 2307}
vn_act = {"2023": 1910, "2024": 1764, "2025": 1959}
seg_sales_2025 = 11852.0       # THB million, Aluminum Can business, PDF p.129
tbc_rev = {"2025": 11909.031, "2024": 12374.731}   # THB million, notes, consolidated incl. Vietnam
tbc_profit = {"2025": 1356.513, "2024": 1551.215}
cans_both_2025 = tbc_act["2025"] + vn_act["2025"]
rev_per_can_blended = seg_sales_2025 / cans_both_2025
rev_per_can_tbc_total = tbc_rev["2025"] / cans_both_2025
rev_per_can_upper = tbc_rev["2025"] / tbc_act["2025"]
res["can_maker_bjc_2025"] = {
    "tbc_capacity_million_cans": tbc_cap, "tbc_actual_million_cans": tbc_act,
    "tbc_usage_pct_computed": {y: round(tbc_act[y] / tbc_cap[y] * 100, 2) for y in tbc_cap},
    "tbc_capacity_growth_2023_to_2025_pct": round((tbc_cap["2025"] / tbc_cap["2023"] - 1) * 100, 1),
    "tbc_spare_capacity_2025_million_cans": tbc_cap["2025"] - tbc_act["2025"],
    "tbc_spare_capacity_2025_pct_of_capacity": round((tbc_cap["2025"] - tbc_act["2025"]) / tbc_cap["2025"] * 100, 2),
    "tbc_actual_growth_2025_vs_2024_pct": round((tbc_act["2025"] / tbc_act["2024"] - 1) * 100, 1),
    "tbc_ball_vn_actual_million_cans": vn_act,
    "thai_plus_vn_cans_2025_million": cans_both_2025,
    "segment_sales_2025_thb_million": seg_sales_2025,
    "tbc_total_revenue_thb_million": tbc_rev, "tbc_profit_thb_million": tbc_profit,
    "tbc_net_margin_pct": {y: round(tbc_profit[y] / tbc_rev[y] * 100, 2) for y in tbc_rev},
    "tbc_revenue_change_2025_pct": round((tbc_rev["2025"] / tbc_rev["2024"] - 1) * 100, 2),
    "revenue_per_can_produced_thb_blended_segment_sales": round(rev_per_can_blended, 3),
    "revenue_per_can_produced_thb_blended_tbc_revenue": round(rev_per_can_tbc_total, 3),
    "revenue_per_can_produced_thb_upper_bracket_all_revenue_over_thai_cans_only": round(rev_per_can_upper, 3),
    "packaging_supply_chain_gross_margin_pct_printed": 22.8, "packaging_supply_chain_ebit_margin_pct_printed": 17.6,
    "caveat": "Revenue per can includes lids and all can sizes and the Vietnamese plant. It is a bracket, not a price list.",
}
brand_vs_can_maker = {
    "brand_2021_cans_pct_of_tbc_2025_actual": round(cans2021 / 1e6 / tbc_act["2025"] * 100, 2),
    "brand_2022_target_cans_pct_of_tbc_2025_actual": round(cans2022t / 1e6 / tbc_act["2025"] * 100, 2),
    "brand_2022_target_cans_pct_of_tbc_2025_capacity": round(cans2022t / 1e6 / tbc_cap["2025"] * 100, 2),
}
res["brand_vs_can_maker"] = brand_vs_can_maker

# ---- 4. Cross-check against the can-cost model (rework/screen/can_cost_model_results.json) ----------
m = json.loads(MODEL.read_text(encoding="utf-8"))
lo, hi = m["variable_cost_per_can"]["low"]["items_usd"], m["variable_cost_per_can"]["high"]["items_usd"]
fx_lo, fx_hi = m["inputs"]["fx_thb_per_usd"]
body_lo = (lo["sheet_metal"] + lo["conversion_nonmetal"]) * fx_lo
body_hi = (hi["sheet_metal"] + hi["conversion_nonmetal"]) * fx_hi
res["model_cross_check"] = {
    "model_sheet_metal_plus_nonmetal_conversion_thb_low": round(body_lo, 2),
    "model_sheet_metal_plus_nonmetal_conversion_thb_high": round(body_hi, 2),
    "model_variable_cost_per_filled_can_thb_low": m["variable_cost_per_can"]["low"]["thb"],
    "model_variable_cost_per_filled_can_thb_high": m["variable_cost_per_can"]["high"]["thb"],
    "model_cans_per_year_group_proxy_low": m["cans_per_year"]["at_util_low"],
    "model_cans_per_year_group_proxy_high": m["cans_per_year"]["at_util_high"],
    "bjc_blended_revenue_per_can_thb": round(rev_per_can_blended, 2),
    "reading": "The blended revenue per can, lids included, is at the model's low end for the can body alone; the model's high end is not supported by the filing.",
    "brand_2022_target_cans_pct_of_model_group_cans_low_to_high": [
        round(cans2022t / m["cans_per_year"]["at_util_high"] * 100, 1),
        round(cans2022t / m["cans_per_year"]["at_util_low"] * 100, 1)],
}

# ---- 5. Reach counts (files 05 and 08; the 7-Eleven count is capture 07) ----------------------------
bigc = {"supercenter": 140, "extra": 13, "market": 36, "foodplace": 17, "mini": 1490}
res["retail_reach_counts"] = {
    "seven_eleven_stores_end_2025": 15945,
    "big_c_big_format_thailand": bigc["supercenter"] + bigc["extra"] + bigc["market"] + bigc["foodplace"],
    "big_c_mini_thailand": bigc["mini"],
    "big_c_all_formats_thailand": sum(bigc.values()),
    "siri_pro_retail_shops_2021_press": 70000, "siri_pro_traditional_wholesale_2021_press": 3600,
}

# ---- 6. Group financials (file 07, press, tier S) ---------------------------------------------------
sc = {2021: (4226.639742, 3590.700760), 2024: (3950.0, 3135.0), 2025: (3892.0, 3085.0)}
res["singha_corporation_ratios"] = {
    str(y): {"revenue_thb_million": r, "net_profit_thb_million": p, "net_profit_pct_of_revenue": round(p / r * 100, 1)}
    for y, (r, p) in sc.items()}
res["singha_corporation_changes"] = {
    "revenue_2025_vs_2024_pct": round((sc[2025][0] / sc[2024][0] - 1) * 100, 1),
    "net_profit_2025_vs_2024_pct": round((sc[2025][1] / sc[2024][1] - 1) * 100, 1),
    "revenue_2025_vs_2021_pct": round((sc[2025][0] / sc[2021][0] - 1) * 100, 1),
    "net_profit_2025_vs_2021_pct": round((sc[2025][1] / sc[2021][1] - 1) * 100, 1),
}
res["boon_rawd_brewery_2022_net_profit_pct_of_revenue"] = round(5793 / 11711 * 100, 1)

# ---- 7. Second pass, 20 October 2026 (reads saved in raw/diligence_2026-10-20/T6/10_second_pass_reads_2026-10-20.md) ----
# Counts and dates are as printed on the pages read. Only the derived items are arithmetic.
res["dates_read_as_printed"] = {
    "lemon_launch_brand_buffet_pr": "19 Aug 2020 (330 mL, THB 16, 7-Eleven nationwide, sugar-free and 0 calories)",
    "yuzu_brand_inside": "8 Jun 2021 (330 mL, THB 16, sugar-free formula and no calories)",
    "red_thansettakij": "15 Aug 2022 (330 mL, THB 16, 45 million litres target for 2022)",
    "ume_marketeer_and_brand_inside": "3 Sep 2023 and 4 Sep 2023 (330 mL, THB 17, 52% share of canned, no period)",
    "pink_marketeer": "25 Jun 2024 (330 mL, THB 17, No. 1 in canned sugar-free carbonated drinks, no figure)",
    "watermelon_bloody_nanno_brand_buffet_pr": "16 Mar 2026 (2 million cans, two label designs, 7-Eleven and Singha Online)",
    "melon_brand_buffet": "4 Apr 2025 (limited edition, sold for 6 months that summer, no can count)",
    "lemon_cream_mitihoon": "10 Nov 2025 (330 mL, price not printed, more than 6 flavours before it)",
}
res["channels_as_printed"] = {
    "ume_2023": ["Singha Online Shop", "7-Eleven nationwide"],
    "pink_2024": ["7-Eleven", "Lotus's", "Makro", "leading stores nationwide", "Singha Online Shop"],
    "lemon_cream_2025": ["7-Eleven", "department stores", "supermarkets nationwide"],
    "watermelon_2026": ["7-Eleven all branches", "Singha Online"],
    "company_product_page_th_en": ["7-Eleven", "department stores", "Singha Online", "Shopee", "Lazada"],
}
res["yuzu_still_listed_check_2026_10_20"] = {
    "seven_eleven_search_header_count": 373,
    "seven_eleven_search_cards_shown": 30,
    "seven_eleven_yuzu_beverage_listed": 0,
    "makro_pro_search_header_count": 110,
    "makro_pro_search_rows_shown": 20,
    "makro_pro_yuzu_beverage_listed": 0,
    "lotuss_search_page_rendered_results": False,
    "reading": "No Yuzu beverage on the first pages read. Yuzu is not confirmed on sale; the pages show a partial read only.",
}
res["single_can_check_2026_10_20"] = {
    "lotuss_single_can_thb": 17.0,
    "lotuss_single_can_thb_per_litre": round(17.0 / CAN_L, 2),
    "lotuss_page_manufacturer_field": "none printed",
    "seven_eleven_24_case_manufacturer_field": "none printed; shelf life 1 year; promotion valid 11/08/2020 to 20/10/2026",
}
res["sales_statements_as_published_no_arithmetic"] = {
    "ume_2023_forecast_sales_growth_pct": 30,
    "ume_2023_forecast_timeframe": "none stated",
    "ume_2023_canned_share_pct": 52,
    "ume_2023_canned_share_period": "none stated",
    "ume_2023_sugar_free_carbonated_market_thb_million": 6930,
    "ume_2023_sugar_free_carbonated_market_growth_pct_stated": "more than 25",
    "pink_2024_sales_or_share_figure": "none printed; No. 1 claim only",
    "lemon_cream_2025_sales_figure": "none printed",
    "red_2022_sales_target_million_litres": 45,
}
res["healthier_choice_register_2026_10_20"] = {
    "register_entry_for_lemon_soda_found": False,
    "programme_front_page_read": True,
    "reading": "Search and front page read; no entry for the product found. Stated limit.",
}

OUT.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
print("wrote", OUT)
