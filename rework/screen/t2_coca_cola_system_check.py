"""T2 Coca-Cola system check, 20 October 2026 (rework/68a_coca_cola_system.md, revision 2 of 20 October 2026).

Recomputes every DERIVED figure that the 68a record and its proposed slide text use. Each input is typed in
below with the saved raw file it was read from. Arithmetic only: no random numbers, no fitted values.
Writes t2_coca_cola_system_check_results.json next to this script.

This script supersedes the two-listing range in coca_cola_system_derived_results.json (fields
cube_vs_sprite_no_sugar_325_pack24_per_330, sprite_no_sugar_pack24_per_330_range_thb and
cube_vs_pack24_low_and_high_thb), which were computed before the Fresh Mart and CR7 ManU rows were added.

Revision 2 (after the independent verifier's report) adds: section 8, the ThaiNamthip shareholding after the
offering and under the put option, with each printed figure checked against the arithmetic; section 9, the printed
Coca-Cola Company gross margins checked against gross profit over revenue; section 10, the recorded attribution
of the Haad Thip carbonated share and the brand membership of the other carbonated line (text records with their
sources, no arithmetic). It also makes the Haad Thip FY2024 gross margin a computed value instead of a typed one.

Revision 3 (20 October 2026) adds section 11: text checks that the re-opened wording (Swire 2025 results page, Lazada
delivery tiles, Makro PRO availability message, Marketeer 79.3% sentence) is saved in the raw files, that the Thai
name and the saved extract headers are as recorded, that the printed digits occur in the saved Version 2 extract,
and that section 10 of the record has no internal note, no dash and no "planning price" wording.
"""
import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))


def per_can(pack_thb, cans):
    return pack_thb / cans


def per_330(pack_thb, cans, can_ml):
    return per_can(pack_thb, cans) * 330.0 / can_ml


def per_litre(pack_thb, cans, can_ml):
    return per_can(pack_thb, cans) / (can_ml / 1000.0)


def pct(x):
    return round(100.0 * x, 1)


out = {
    "task": "T2 Coca-Cola system check, 20 October 2026 (68a revision)",
    "method": "per can = pack / cans; per 330 mL = per can x 330 / can size; no rounding before comparison; "
              "ratios shown to 1 or 2 decimals after computation",
    "inputs_note": "Each input carries the raw file it was read from (rework/raw/diligence_2026-10-20/T2/ unless stated).",
}

# ---------------------------------------------------------------- 1. Shelf prices
sprite_24 = [
    {"label": "Sprite No Sugar 325 mL x 24, Coca-Cola Official Store (LazMall), via Priceza",
     "pack": 334.0, "cans": 24, "ml": 325, "src": "priceza_sprite_2026-10-20.md row 9"},
    {"label": "Sprite No Sugar 325 mL x 24, Lazada trending page (seller not stated)",
     "pack": 365.0, "cans": 24, "ml": 325, "src": "retail_prices_2026-10-20.md (Lazada block)"},
    {"label": "Sprite No Sugar 325 mL x 24, Fresh Mart, via Priceza",
     "pack": 414.0, "cans": 24, "ml": 325, "src": "priceza_sprite_2026-10-20.md row 18"},
    {"label": "Sprite No Sugar 325 mL x 24, CR7 ManU, via Priceza",
     "pack": 456.0, "cans": 24, "ml": 325, "src": "priceza_sprite_2026-10-20.md row 10"},
]
for row in sprite_24:
    row["per_can"] = round(per_can(row["pack"], row["cans"]), 2)
    row["per_330"] = round(per_330(row["pack"], row["cans"], row["ml"]), 2)
    row["per_litre"] = round(per_litre(row["pack"], row["cans"], row["ml"]), 1)

per330_values = [row["per_330"] for row in sprite_24]
sprite_24_summary = {
    "listings_used": len(per330_values),
    "min_per_330": min(per330_values),
    "max_per_330": max(per330_values),
    "median_per_330": round(statistics.median(per330_values), 2),
    "excluded_bundle": "LazMall 325 mL x 24 with Halls XS candy, THB 328, row 22 (bundle, not used)",
}

singles_and_others = [
    {"label": "Sprite (regular) 325 mL can, Lotus's Shop Online (sugar wording not stated on page)",
     "pack": 16.0, "cans": 1, "ml": 325, "src": "lotus_sprite_can_2026-10-20.md"},
    {"label": "Sprite No Sugar 325 mL can, Tops Online (UNVERIFIED lead, HTTP 403, not used in any range)",
     "pack": 16.0, "cans": 1, "ml": 325, "src": "retail_prices_2026-10-20.md (lead only)"},
    {"label": "Sprite Lemon Plus 325 mL can, planning reference 2022 (dated)",
     "pack": 15.0, "cans": 1, "ml": 325, "src": "sprite_fanta_schweppes_launch_releases.md item 2"},
    {"label": "Sprite No Sugar 325 mL can, first release 2019 (dated)",
     "pack": 14.0, "cans": 1, "ml": 325, "src": "sprite_fanta_schweppes_launch_releases.md item 1"},
    {"label": "Schweppes Lime Soda Zero Sugar 330 mL x 6, Makro PRO (unavailable in area selected)",
     "pack": 84.0, "cans": 6, "ml": 330, "src": "retail_prices_2026-10-20.md (Makro PRO block)"},
    {"label": "Fanta Pineapple 325 mL x 6, Lazada trending page",
     "pack": 85.0, "cans": 6, "ml": 325, "src": "retail_prices_2026-10-20.md (Lazada block)"},
    {"label": "Coke No Sugar 330 mL x 12, Makro PRO",
     "pack": 102.0, "cans": 12, "ml": 330, "src": "retail_prices_2026-10-20.md (Makro PRO block)"},
    {"label": "7UP NS Strawberry Lemon 325 mL x 6, Lazada (context, other brand)",
     "pack": 75.0, "cans": 6, "ml": 325, "src": "retail_prices_2026-10-20.md (Lazada block)"},
    {"label": "SINGHA LEMON SODA can 330 mL, Lotus's Shop Online (proposer's own product)",
     "pack": 17.0, "cans": 1, "ml": 330, "src": "lotus_singha_lemon_soda_can_2026-10-20.md"},
]
for row in singles_and_others:
    row["per_can"] = round(per_can(row["pack"], row["cans"]), 2)
    row["per_330"] = round(per_330(row["pack"], row["cans"], row["ml"]), 2)
    row["per_litre"] = round(per_litre(row["pack"], row["cans"], row["ml"]), 1)

# ---------------------------------------------------------------- 2. Cube comparison (planning price, ASSUMPTION)
CUBE_PRICE = 15.0  # ASSUMPTION: planning price per 330 mL, from the proposal and deck, not a sourced figure
comparisons = {}
for row in sprite_24:
    comparisons[row["label"]] = round(CUBE_PRICE - row["per_330"], 2)
comparisons["Schweppes Lime Soda Zero Sugar 330 mL x 6 (Makro PRO)"] = round(CUBE_PRICE - singles_and_others[4]["per_330"], 2)
comparisons["Sprite (regular) 325 mL can (Lotus's), per 330 mL"] = round(CUBE_PRICE - singles_and_others[0]["per_330"], 2)
comparisons["SINGHA LEMON SODA can 330 mL (Lotus's)"] = round(CUBE_PRICE - singles_and_others[8]["per_330"], 2)

out["shelf_prices"] = {
    "sprite_no_sugar_24_pack": sprite_24,
    "sprite_no_sugar_24_pack_summary": sprite_24_summary,
    "sprite_no_sugar_24_pack_median_check_16_48": sprite_24_summary["median_per_330"] == 16.48,
    "singles_and_others": singles_and_others,
    "cube_planning_price_thb_per_330_ASSUMPTION": CUBE_PRICE,
    "cube_minus_listing_per_330": comparisons,
}

# ---------------------------------------------------------------- 3. The Coca-Cola Company (group, USD million)
ko = {
    "FY2023": {"revenue": 45754, "gross_profit": 27234, "net_attrib": 10714},
    "FY2024": {"revenue": 47061, "gross_profit": 28737, "net_attrib": 10631},
    "FY2025": {"revenue": 47941, "gross_profit": 29544, "net_attrib": 13107},
}
out["coca_cola_company_group_usd_m"] = {
    y: {"gross_margin_pct": pct(v["gross_profit"] / v["revenue"]),
        "net_margin_pct": pct(v["net_attrib"] / v["revenue"])}
    for y, v in ko.items()
}

# ---------------------------------------------------------------- 4. ThaiNamthip Corporation PCL (THB million)
tncc = {
    "FY2022": {"total_rev": 35989.15, "sales_goods": 35632.60, "gross_profit": 13617.82, "net": 3083.24},
    "FY2023": {"total_rev": 39294.98, "sales_goods": 38876.25, "gross_profit": 15004.43, "net": 3374.41},
    "FY2024": {"total_rev": 41314.24, "sales_goods": 39828.47, "gross_profit": 15332.02, "net": 4379.08},
    "6M2024": {"total_rev": 21528.72, "sales_goods": 21291.92, "gross_profit": 8275.56, "net": 2069.93},
    "6M2025": {"total_rev": 18330.18, "sales_goods": 17863.60, "gross_profit": 6994.12, "net": 958.51},
}
out["thainamthip_tncc_thb_m"] = {
    k: {"gross_margin_on_sales_of_goods_pct": pct(v["gross_profit"] / v["sales_goods"]),
        "net_margin_on_total_revenue_pct": pct(v["net"] / v["total_rev"])}
    for k, v in tncc.items()
}
out["thainamthip_growth_pct"] = {
    "total_rev_FY2023_vs_FY2022": pct(tncc["FY2023"]["total_rev"] / tncc["FY2022"]["total_rev"] - 1),
    "total_rev_FY2024_vs_FY2023": pct(tncc["FY2024"]["total_rev"] / tncc["FY2023"]["total_rev"] - 1),
    "total_rev_6M2025_vs_6M2024": pct(tncc["6M2025"]["total_rev"] / tncc["6M2024"]["total_rev"] - 1),
    "net_profit_6M2025_vs_6M2024": pct(tncc["6M2025"]["net"] / tncc["6M2024"]["net"] - 1),
}
# Channel split FY2024 (sales of goods 39,828.47): filing V2 Thai text and V1 channel table
channels = {"modern_trade": 19917.5, "traditional_trade": 19136.8, "laos_and_export": 774.1}
out["thainamthip_channels_fy2024"] = {
    k: {"thb_m": v, "pct_of_sales_goods": pct(v / 39828.47)} for k, v in channels.items()
}
out["thainamthip_channels_fy2024"]["sum_check_vs_sales_goods"] = round(sum(channels.values()) - 39828.47, 2)
# Six months 2025 line revenue (P, filing V2): cola and other carbonated
out["thainamthip_6M2025_lines"] = {
    "cola_pct_change": pct(10872.74 / 12745.80 - 1),
    "other_carbonated_pct_change": pct(5080.19 / 6365.02 - 1),
    "volume_pct_change_181_vs_216_million_cases": pct(181.0 / 216.0 - 1),
}
cola_fy2024 = 24060.03
other_carb_fy2024 = 11609.18
carb_fy2024 = cola_fy2024 + other_carb_fy2024
out["thainamthip_carbonated_plausibility"] = {
    "carbonated_revenue_fy2024_thb_m": round(carb_fy2024, 2),
    "implied_market_at_51_4pct_thb_bn": round(carb_fy2024 / 0.514 / 1000.0, 1),
    "carbonated_as_pct_of_press_market_66_bn": pct(carb_fy2024 / 66000.0),
    "carbonated_as_pct_of_press_market_76_9_bn": pct(carb_fy2024 / 76900.0),
    "note": "A bracket only. It shows the 51.4 per cent share is consistent with a ThaiNamthip-only reading; it is not a share estimate.",
}
# Capacity utilisation on sales volume (400 million FY2024 in V2; 404 million in V1; capacity 564 million (2025 filing) or 450 million (2024 wording))
out["capacity_utilisation_fy2024"] = {
    "400m_on_564m_pct": pct(400.0 / 564.0),
    "404m_on_564m_pct": pct(404.0 / 564.0),
    "400m_on_450m_pct": pct(400.0 / 450.0),
    "404m_on_450m_pct": pct(404.0 / 450.0),
}

# ---------------------------------------------------------------- 5. Haad Thip Public Company Ltd (THB million)
HTC_GM_FY2025_PCT = 42.2   # P: Haad Thip investor relations page (42.20%), read 20 October 2026
HTC_GM_DROP_PTS = 0.5      # S: company release of 2 March 2026 as relayed by The Thai Press, "down 0.5 point"
out["haad_thip_thb_m"] = {
    "FY2023_net_margin_on_total_rev_pct": pct(598.56 / 7863.97),
    "FY2024_net_margin_on_total_rev_pct": pct(601.68 / 8189.09),
    # FY2025 gross margin 42.2% (company page, P) and "down 0.5 point" (release, S): FY2024 = 42.2 + 0.5
    "FY2024_gross_margin_derived_pct": round(HTC_GM_FY2025_PCT + HTC_GM_DROP_PTS, 1),
    "FY2025_net_margin_on_sales_pct": pct(568.3 / 8258.4),
    "FY2025_net_margin_company_page_pct": 6.90,
    "FY2025_revenue_growth_on_FY2024_total_rev_8189_09_pct": pct(8258.4 / 8189.09 - 1),
    "FY2025_revenue_growth_on_FY2024_total_rev_if_8368_pct": pct(8368.0 / 8189.09 - 1),
    "FY2024_sales_comparator_implied_by_release_1_6_pct": round(8258.4 / 1.016, 1),
    "FY2025_net_profit_change_release_pct": -5.6,
}

# ---------------------------------------------------------------- 6. Owner versus bottler gap (FY2024)
out["gross_margin_gap_owner_minus_tncc_fy2024_pts"] = round(
    out["coca_cola_company_group_usd_m"]["FY2024"]["gross_margin_pct"]
    - out["thainamthip_tncc_thb_m"]["FY2024"]["gross_margin_on_sales_of_goods_pct"], 1)

# ---------------------------------------------------------------- 8. ThaiNamthip shareholding (P, filing Version 2, PDF page 9)
# The filing prints three columns: at 30 June 2025 (before the offering), after the 612,451,687-share IPO,
# and after the IPO with the put option sold in full to SWB. Figures typed from the saved extract
# (tncc_sec_filing_v2_exec_summary_extract.md, "PDF page 9" block, and the offering table on the same page).
SHARES = {
    "total_before_offering": 5512065185,
    "total_after_offering": 6124516872,
    "ipo_new_shares": 612451687,
    "swb_before": 3064110570,
    "swb_after_ipo": 3064110570,
    "swb_after_put_option_ipo": 3340453330,
    "tntl_before": 1650642840,
    "tntl_after_ipo": 1650642840,
    "put_option_shares_sold_to_swb": 276342760,
}
PRINTED_PCT = {
    "swb_before": 55.59, "swb_after_ipo": 50.03, "swb_after_put_option_ipo": 54.54,
    "tntl_before": 29.95, "tntl_after_ipo": 26.95,
}
s = SHARES
def pct2(x):
    return round(100.0 * x, 2)


shareholding_checks = {
    "ipo_new_shares_plus_before_equals_after": s["total_before_offering"] + s["ipo_new_shares"] == s["total_after_offering"],
    "put_option_shares_added_to_swb_equals_put_case": s["swb_after_ipo"] + s["put_option_shares_sold_to_swb"] == s["swb_after_put_option_ipo"],
    "computed_pct": {
        "swb_before": pct2(s["swb_before"] / s["total_before_offering"]),
        "swb_after_ipo": pct2(s["swb_after_ipo"] / s["total_after_offering"]),
        "swb_after_put_option_ipo": pct2(s["swb_after_put_option_ipo"] / s["total_after_offering"]),
        "tntl_before": pct2(s["tntl_before"] / s["total_before_offering"]),
        "tntl_after_ipo": pct2(s["tntl_after_ipo"] / s["total_after_offering"]),
    },
}
shareholding_checks["printed_pct"] = PRINTED_PCT
shareholding_checks["computed_matches_printed"] = {
    k: abs(shareholding_checks["computed_pct"][k] - PRINTED_PCT[k]) < 0.005 for k in PRINTED_PCT
}
shareholding_checks["put_option_cap_usd_m_printed"] = 250
shareholding_checks["tier"] = ("P: all five percentages are printed in the filing (Version 2, page 9); the computed "
                               "values match them. The put option case is a filing assumption, and the filing says the "
                               "actual steps may change.")
out["thainamthip_shareholding_p"] = shareholding_checks

# ---------------------------------------------------------------- 9. Coca-Cola Company gross margins: printed versus computed
# The FY2025 earnings extract prints gross profit margin 61.6% (2025) and 61.1% (2024). FY2023 is not printed.
KO_PRINTED_GM = {"FY2024": 61.1, "FY2025": 61.6}
out["coca_cola_company_gm_printed_check"] = {
    y: {
        "printed_pct": KO_PRINTED_GM[y],
        "computed_pct": out["coca_cola_company_group_usd_m"][y]["gross_margin_pct"],
        "matches": abs(KO_PRINTED_GM[y] - out["coca_cola_company_group_usd_m"][y]["gross_margin_pct"]) < 0.05,
    }
    for y in KO_PRINTED_GM
}
out["coca_cola_company_gm_printed_check"]["FY2023"] = {
    "printed_pct": None,
    "computed_pct": out["coca_cola_company_group_usd_m"]["FY2023"]["gross_margin_pct"],
    "note": "not printed in the extract; DERIVED only",
}
out["coca_cola_company_gm_printed_check"]["tier"] = (
    "FY2024 and FY2025 gross margins are printed (P, Form 10-K FY2025 extract, section C, line 34 of ko_group_income_statement_fy2022_fy2025.md); "
    "FY2023 and all net margins are DERIVED from the printed revenue, gross profit and net income.")

# ---------------------------------------------------------------- 10. Text records with sources (no arithmetic)
out["haad_thip_southern_carbonated_78_2_attribution"] = {
    "value": "78.2% share of southern carbonated soft drinks, 2025",
    "thai_press_3_march_2026": "credits Nielsen (Thailand) for 23.2% (NARTD) and for 78.2% (carbonated); basis not stated",
    "marketeer_24_march_2026": "78.2% sentence has no source in the sentence; infographic source line reads Haad Thip company, March 2026; 23.2% described as by value",
    "status": "S, attribution conflicting; not described as the company's claim alone",
    "saved": "haadthip_results_press_2024_2026.md; haadthip_78_2_attribution_2026-10-20.md",
    "judge_text": "not used in judge-facing text (proposal 11 section 2.3 paragraph in rev 2 leaves it out)",
}
out["other_carbonated_line_brand_membership"] = {
    "filing_revenue_line": "2. other carbonated soft drinks (เครื่องดื่มอัดลมประเภทอื่นๆ), Version 2 PDF page 10 revenue table; 6M 2025 on PDF page 23",
    "filing_brand_split": "not given in the pages read",
    "authorised_brands_named_on_page_7": "Coca-Cola, Fanta, Sprite, Schweppes, Minute Maid, A&W (Thailand only), Fuze Tea and Namthip",
    "team_reading": "other carbonated line = Fanta, Sprite, Schweppes (non-alcoholic) and A&W; a reading by elimination, not a filing statement",
    "schweppes_mixed": "alcoholic ready-to-drink; the filing reports it in row 5 'other (1)' with footnote (1), not in the carbonated line",
}

# ---------------------------------------------------------------- 11. Re-opened wording and record checks (revision 3)
# Each check reads a saved file and tests that the quoted wording is present. These are text checks, not arithmetic.
RAW_T2 = os.path.normpath(os.path.join(HERE, "..", "raw", "diligence_2026-10-20", "T2"))
RECORD = os.path.normpath(os.path.join(HERE, "..", "68a_coca_cola_system.md"))


def read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


reopens = read_text(os.path.join(RAW_T2, "verifier_reopens_2026-10-20.md"))
retail = read_text(os.path.join(RAW_T2, "retail_prices_2026-10-20.md"))
v2 = read_text(os.path.join(RAW_T2, "tncc_sec_filing_v2_exec_summary_extract.md"))
v1 = read_text(os.path.join(RAW_T2, "tncc_sec_filing_v1_exec_summary_extract.md"))
record = read_text(RECORD)
judge_10 = record[record.index("## 10. Comparison tables"):record.index("## 11. Conflicts with current text")]
s11 = {
    "swire_tncc_subsidiary_30_sept_2024_on_reopened_page": "became a subsidiary on 30th September 2024" in reopens,
    "swire_laos_date_absent_on_reopened_page": "It gives no date for the Laos franchise" in reopens,
    "lazada_original_delivery_text_saved": "ส่งในกทม. ปริมณฑล,ลำพูน,เชียงใหม่และชลบุรี" in reopens and "ส่งในกทม. ปริมณฑล,ลำพูน,เชียงใหม่และชลบุรี" in retail,
    "lazada_no_sugar_delivery_text_saved": "จัดส่งเฉพาะกทม. ปริมณฑลและชลบุรี" in reopens and "จัดส่งเฉพาะกทม. ปริมณฑลและชลบุรี" in retail,
    "makro_unavailable_text_saved": "This item is unavailable in the area you selected" in reopens and "This item is unavailable in the area you selected" in retail,
    "marketeer_79_3_no_year_no_source_saved": "Year in the sentence: none" in reopens and "Source credit next to the figure: none" in reopens,
    "thai_name_spelled_with_long_vowel_in_v2_extract": "ไทยน้ำทิพย์" in v2 and "ไทยนำทิพย์" not in v2,
    "v2_header_states_verbatim_on_pages_tested_in_rev3": "Thai text is verbatim from the PDF text layer on the pages tested in revision 3" in v2,
    "v1_header_states_v1_not_retested": "Revision 3 did not re-test Version 1" in v1,
    "printed_digits_present_in_saved_v2_extract": {
        d: (d in v2) for d in ["51.4", "47.9", "66.0", "27.5", "15.6", "511,000", "564", "55.59", "50.03", "54.54", "29.95", "26.95", "181", "216", "5,080.19", "6,365.02"]
    },
    "record_section_10_has_no_internal_note_on_haad_thip_press_credit": "A press share for the independent southern bottler" not in judge_10,
    "record_section_10_has_no_em_or_en_dash_or_middle_dot": not any(ch in judge_10 for ch in ["—", "–", "·"]),
    "record_section_5_haad_thip_79_3_labelled_undated": "79.3% (undated in the article" in record,
    "record_section_10_has_no_planning_price_wording": "planning price" not in judge_10.lower(),
}
s11["all_text_checks_pass_except_digit_table"] = all(
    v for k, v in s11.items() if isinstance(v, bool))
s11["digit_table_all_present"] = all(s11["printed_digits_present_in_saved_v2_extract"].values())
out["reopen_and_record_text_checks"] = s11
out["reopen_and_record_text_checks"]["tier"] = (
    "Text checks against the saved extracts (tool extracts, not raw page text). They confirm that the quoted wording is "
    "saved and that the record carries no internal note or dash in section 10. They do not verify the PDF text layer.")

# ---------------------------------------------------------------- 7. Write
here_path = os.path.join(HERE, "t2_coca_cola_system_check_results.json")
with open(here_path, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)
print("wrote", here_path)
