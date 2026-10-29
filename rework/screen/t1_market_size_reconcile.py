"""T1 slide 3 market-size check: arithmetic on figures read from saved pages.

Every input below is a number printed in a page saved under
rework/raw/diligence_2026-10-20/T1/ (file named in the comment), or in a page
read by another task and saved under rework/raw/diligence_2026-10-20/T2/ or T3/
(named where used). Nothing here is estimated. All outputs are DERIVED (our
arithmetic) and are written to rework/screen/t1_market_size_reconcile_results.json.
No random numbers, so no seed is needed.

Revision of 20 October 2026 (third pass, after the second independent check and
the verifier's points on the third pass):
- Attribution fixes. The 67,000 value and the 8 percent fall are from Bangkokbiznews
  (13 October 2025), with no source named. The ThaiBev executive named in
  Thansettakij (13 October 2025) is the source only of 68,000 (labelled 2024) and the
  4 percent fall. The 70,772 value is NielsenIQ as printed by Thansettakij (14 January 2025).
  The 17,391 colour-soda figure has no data house or period in Thansettakij; the
  NielsenIQ window belongs to Bangkokbiznews's 17,300.
- The "volume down 6 percent" wording is not used. The sentence is ambiguous.
- The Thai Drinks size clause is removed (no source). Thai Drinks is a stated limit.
- Bank of Thailand report 123 (read 20 October 2026, P): 15 October 2026 buying sight
  33.3535, buying transfer 33.4246 (not "bill"), selling 33.7455, reference rate
  33.5410. The StrategyHelix conversion uses the reference rate. The team midpoint
  (33.5495) is kept as a DERIVED check only.
- Non-alcoholic totals in press and bank notes are listed with their definitions.
  MarketPlus's 31 percent of 198,000 to 200,000 gives 61,380 to 62,000, not the 66,000
  it prints for carbonated drinks.
- KResearch's 2.0 percent is also printed as the growth of the whole non-alcoholic
  business in the same note, so the mapping of 2.0 to carbonated is weaker. Both
  mappings are computed. Thansettakij also prints about 2 percent for the 226,000 total.
- Hadthip infographic sales for 2021 to 2025 are tabulated (basis: infographic sales).
- Sermsuk FY2023 carbonated line: source is the Thai SEC Form 250-2 dated 8 October
  2024 (revenue structure table, PDF pages 11 and 63 to 64), not the 15 November 2023 letter.
- The Positioningmag 2019 growth ("almost 12 percent") does not match its own figures (10.0 percent).
- The ThaiNamthip unit-case figures (216 to 181 million) are for all licensed beverages,
  not carbonated drinks only.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "t1_market_size_reconcile_results.json")

r = {}

# ---- Inputs (THB million unless stated) ------------------------------------
# ThaiNamthip (TNCC) Version 1 page 9 (tncc_sec_draft_prospectus_exec_summary.md):
# 2022 to 2024 revenue by product group.
# Version 2 page 10 (read in T2/tncc_sec_filing_v2_exec_summary_extract.md) prints
# the 2024 values 24,060.03 and 11,609.18. Version 2 page 24 prints them to one
# decimal (24,060.0 and 11,609.2) (tncc_sec_v2_exec_summary_pages.md).
tncc = {
    2022: {"coca_cola": 21241.94, "other_csd": 10415.37, "water": 2739.62, "total": 35989.15},
    2023: {"coca_cola": 23270.67, "other_csd": 11660.40, "water": 2740.57, "total": 39294.98},
    2024: {"coca_cola": 24060.03, "other_csd": 11609.18, "water": 2794.49, "total": 41314.24},
}
tncc_share_csd_2024 = 0.514  # Version 1 page 6 and Version 2 page 7: Frost & Sullivan statistic quoted in the filing, basis not stated
# Version 2 pages 8, 19, 23: first-half figures. The unit cases are for ALL LICENSED
# BEVERAGES (tncc_sec_v2_exec_summary_pages.md, line 12), not carbonated drinks only.
tncc_h1 = {
    2024: {"coca_cola": 12745.8, "other_csd": 6365.0, "total_revenue": 21528.72, "sales_of_goods": 21291.92, "unit_cases_all_licensed_m": 216.0},
    2025: {"coca_cola": 10872.7, "other_csd": 5080.2, "total_revenue": 18330.18, "sales_of_goods": 17863.60, "unit_cases_all_licensed_m": 181.0},
}

# Hadthip (HTC). 8,258.4 for 2025 sales ("รายได้จากการขาย"): Mitihoon, 3 March 2026, S
# (mitihoon_622207_2026-03-03_hadthip_results.md). 8.25 billion, +1.6 percent: The Story
# Thailand reprint dated 25 March 2026, S (haadthip_release_2026-03-25_storythailand.md).
# The release date (2 March 2026) is from T2/haadthip_ir_pages_2026-10-20.md (not opened by T1).
htc_sales_2025_release = 8258.4
htc_growth_2025 = 0.016
# Marketeer, 24 March 2026, S (marketeer_460572_2026-03-24_hadthip.md): company infographic table
# ("ยอดขาย" = sales, units not printed) and CEO statement (8,368 "revenue from total sales").
htc_total_2025_infographic = 8368.0
htc_sales_infographic = {2021: 6544, 2022: 7092, 2023: 7863, 2024: 8189, 2025: 8368}
htc_carbonated_brand_mix = 0.68 + 0.20 + 0.06   # Coke, Fanta and Sprite share of revenue (2025 infographic); an ASSUMPTION when applied to 2024
htc_south_market = 10000.0                      # "about 10,000" as printed in the infographic
htc_south_share = 0.782                         # 78.2 percent, a company claim (release and infographic)

# Serm Suk (SSC, est maker). SET letters (P) and Thai SEC Form 250-2 (P for PDF pages
# 11 and 63 to 64). Fiscal years end 30 September.
ssc_total_mda = {2022: 10905.0, 2023: 12371.0, 2024: 13153.0}
ssc_total_table = {2021: 9618.49, 2022: 10904.85, 2023: 12371.03}          # Form 250-2 (8 October 2024), PDF page 11
ssc_csd = {2021: 3708.03, 2022: 3972.69, 2023: 4550.15}                    # carbonated soft drinks line, Form 250-2
ssc_9m_fy2024 = {"csd": 3964.26, "total": 9926.54}                         # 1 October 2023 to 30 June 2024

# NielsenIQ values as printed by press (nielseniq_press_series_2023_2026.md), S.
niq = {"to_aug_2023_press_no_source": 62000.0, "to_jan_2024": 66000.0, "to_nov_2024": 70772.0}
niq_growth = {"to_jan_2024": 0.12, "to_nov_2024": 0.09}
coke_share_press = 0.51
pepsi_share_press = 0.30
est_share_volume_press = 0.086   # Thansettakij 16 March 2024 (volume share); MarketPlus 8 May 2024 gives 8.6 percent as a volume share, attributed to Kantar
# Big Cola (AJ Thai). Thansettakij, 1 March 2025 (thansettakij_620945_2025-03-01_bigcola.md), S.
# The article prints "ยอดขายรวม" (total sales): 3,600 for the year before, target 4,500.
# It does not say the figure is carbonated only. Used as a PROXY for Big Cola's carbonated sales.
big_cola_2024_total_sales_proxy = 3600.0
big_cola_target_2025 = 4500.0
# Thansettakij, 3 April 2025 (thansettakij_624003_2025-04-03_pepsi_bigcola.md), S.
aj_dark_cola_share_624003 = 0.85     # Big Cola section: dark cola about 85 percent of the carbonated market
aj_value_624003 = 60000.0            # Big Cola section: "about 6 หมื่นล้านบาท" (about 60,000 million), no year, no source
aj_intro_value_624003 = 66000.0      # article intro: "6.6 หมื่นล้านบาท", no year, no source
shares_624003 = {"coke": 51.0, "pepsi_suntory": 39.0, "s_thai_drinks": 8.9, "big_cola": 5.0}
dark_cola_72_623088 = 72.0           # Thansettakij 26 March 2025, a forecast in the journalist's narration (not used)
# GotoManager, 29 October 2023 (gotomanager_5234_2023-10-29_est_pepsi_history.md), S.
gotomanager_value_2023 = 62000.0     # "มูลค่ารวมกว่า 62,000 ล้านบาท", no source named; black 75 percent, colour 25 percent

# ThaiBev executive, named in Thansettakij 641276 (13 October 2025; saved as
# thansettakij_641276_2025-10-13_thaibev_68000_17391.md). S.
exec_68000_label_2024 = 68000.0      # "ตลาดน้ำอัดลมรวมมีมูลค่า 68,000 ล้านบาท (ปี 2567)"
exec_decline_2025 = 0.04             # "ตลาดรวมติดลบถึง 4%" (this year)
# Bangkokbiznews 1202914 (13 October 2025; saved as bangkokbiznews_1202914_2025-10-13_67000_colour_soda.md). S.
# No source is named in the article for the 67,000 value or the 8 percent fall.
bkk_2025_67000 = 67000.0             # "ปี 2568 ตลาดน้ำอัดลมมีมูลค่า 6.7 หมื่นล้านบาท", window not stated
bkk_decline_jan_aug_2025 = 0.08      # "ติดลบ 8%" for January to August 2025
bkk_nab_2025_over = 260000.0         # "เครื่องดื่มไม่มีแอลกอฮอล์มูลค่ากว่า 2.6 แสนล้านบาท" (non-alcoholic over 260,000), no source named
# Colour soda: Bangkokbiznews gives 17,300 with NielsenIQ and the window September 2024 to August 2025.
colour_niq_bkk_sep2024_aug2025 = 17300.0
# Thansettakij 641276 gives 17,391 in the paragraph after the executive's statement, with no data house or period.
colour_unattributed_thansettakij = 17391.0

# MarketPlus, 8 May 2024 (marketplus_25050_2024-05-08_66000_nab.md), S.
marketplus_nab_low, marketplus_nab_high = 198000.0, 200000.0   # "ประมาณ 1.98 - 2 แสนล้านบาท", year not stated in that sentence
marketplus_csd_share_nab = 0.31                                # "ประมาณ 31%"
marketplus_csd_printed = 66000.0                               # NielsenIQ, February 2023 to January 2024

# KResearch note of 30 May 2025 (kresearch_76900_chain.md; excerpt in kresearch_note_2025-05-30_excerpt.md), S.
kres_csd, kres_water, kres_nab = 76900.0, 48100.0, 226000.0    # 76,900 and 48,100 are not printed in the note text (chart Figure 3)
# "ยอดขายน้ำอัดลมและน้ำดื่มบรรจุขวด คาดว่าจะขยายตัว 2.0% และ 2.6%": the two figures are unlabelled.
# Carbonated is listed first, so the mapping 2.0 percent = carbonated is an inference from list order.
kres_growth_pair_printed = (0.020, 0.026)
# The same note (excerpt lines 11 and 14): the whole non-alcoholic business grows 2.0 percent in 2025
# (about 226,000 million, slowing from 4.5 percent). Thansettakij (8 September 2025) also prints 2 percent for the 226,000 total.
kres_nab_growth_2025 = 0.020

# Krungsri Research, 15 June 2026 (krungsri_beverage_outlook_2026-06-15.md), S.
nab_litres_2025 = 10764.5           # million litres, domestic non-alcoholic sales
csd_volume_share = 0.250            # carbonated and soda share of that volume
krungsri_printed_litres = 2700.0    # "2.7 billion liters"
krungsri_nab_value_usd_m_2025 = 10555.5  # "valued at USD 10,555.5 million" (non-alcoholic, 2025)
krungsri_thb_per_usd_2025 = 32.88        # Krungsri footnote 2: Bank of Thailand average rate for 2025

# Bank of Thailand, report FM_FX_001_S3 (reportID 123), read 20 October 2026 (bot_fx_report123_2026-10-20.md), P.
bot_buy_sight_15oct = 33.3535        # printed BUYING SIGHT, 15 OCT 2026
bot_buy_transfer_15oct = 33.4246     # printed BUYING TRANSFER, 15 OCT 2026 (the earlier raw file called this "bill")
bot_sell_15oct = 33.7455             # printed SELLING, 15 OCT 2026
bot_reference_15oct = 33.5410        # printed REFERENCE RATE: US DOLLAR (USD), 15 OCT 2026
bot_mid_in_team_files = 33.5495      # the earlier team midpoint (DERIVED, not a published rate)
usd_bn_2026, usd_bn_2031 = 3.4, 4.1  # StrategyHelix summary page (S, not used as a market value)

# Canned carbonated (Marketeer 16 August 2022, marketeer_275504_2022-08-16_singha_red_lemon.md), S.
canned_market_2022_press = 13172.0
singha_sales_2022_press = 1357.0     # year not stated in the article
csd_2022 = 57000.0
can_share_2022 = 0.10               # ThaiBev pack mix, measure not stated

colour_clear_share_2024 = 0.18      # Marketeer 2024 value shares, colour or clear line (zero sugar 15 percent is a separate line)
pos2020 = {"market_2019": 56000.0, "market_2018": 50900.0, "black": 0.71, "colour": 0.23, "clear": 0.06}
pos2020_growth_printed_text = 0.12  # "almost 12 percent", as printed in the article text

# ---- 1. TNCC carbonated lines ----------------------------------------------
r["tncc_carbonated_lines"] = {
    y: round(v["coca_cola"] + v["other_csd"], 2) for y, v in tncc.items()
}
r["tncc_carbonated_share_of_total_revenue_2024"] = round(
    r["tncc_carbonated_lines"][2024] / tncc[2024]["total"], 4)

h1_24 = tncc_h1[2024]["coca_cola"] + tncc_h1[2024]["other_csd"]
h1_25 = tncc_h1[2025]["coca_cola"] + tncc_h1[2025]["other_csd"]
r["tncc_first_half"] = {
    "carbonated_lines_h1_2024": round(h1_24, 1),
    "carbonated_lines_h1_2025": round(h1_25, 1),
    "carbonated_lines_change_pct": round(h1_25 / h1_24 - 1, 4),
    "coca_cola_line_change_pct": round(tncc_h1[2025]["coca_cola"] / tncc_h1[2024]["coca_cola"] - 1, 4),
    "other_csd_line_change_pct": round(tncc_h1[2025]["other_csd"] / tncc_h1[2024]["other_csd"] - 1, 4),
    "total_revenue_change_pct": round(tncc_h1[2025]["total_revenue"] / tncc_h1[2024]["total_revenue"] - 1, 4),
    "unit_cases_all_licensed_beverages_change_pct": round(
        tncc_h1[2025]["unit_cases_all_licensed_m"] / tncc_h1[2024]["unit_cases_all_licensed_m"] - 1, 4),
    "unit_cases_note": "All licensed beverages (ALL licensed beverages, not carbonated only), 216 to 181 million unit cases, from the Version 2 text (tncc_sec_v2_exec_summary_pages.md, line 12). Not a carbonated unit-case figure.",
    "note": "First half to 30 June, Version 2 of the draft prospectus (pages 8, 19, 23). Full-year 2025 was not read. Do not double a half year: the first half holds the hot season.",
}

# ---- 2. Hadthip ------------------------------------------------------------
htc_2024_implied = htc_sales_2025_release / (1 + htc_growth_2025)
htc_csd_2024_derived = htc_2024_implied * htc_carbonated_brand_mix
r["htc"] = {
    "sales_2025_release_mitihoon": htc_sales_2025_release,
    "sales_2024_implied_from_release_growth_DERIVED": round(htc_2024_implied, 1),
    "infographic_sales_2021_to_2025": htc_sales_infographic,
    "infographic_growth_2025_over_2024_pct": round(htc_total_2025_infographic / htc_sales_infographic[2024] - 1, 4),
    "infographic_growth_2024_over_2023_pct": round(htc_sales_infographic[2024] / htc_sales_infographic[2023] - 1, 4),
    "infographic_minus_release_2025": round(htc_total_2025_infographic - htc_sales_2025_release, 1),
    "infographic_minus_release_2025_pct": round(
        (htc_total_2025_infographic - htc_sales_2025_release) / htc_sales_2025_release, 4),
    "infographic_minus_implied_2024": round(htc_sales_infographic[2024] - htc_2024_implied, 1),
    "three_year_table_basis": "2023 and 2024 are infographic sales (ยอดขาย). 2025 is both the release revenue from sales (8,258.4, Mitihoon, S) and the infographic sales (8,368, CEO statement, S). The basis gap of 109.6 is not explained by the pages read.",
    "carbonated_brand_mix_2025_assumed_for_2024": round(htc_carbonated_brand_mix, 2),
    "carbonated_sales_2025_at_brand_mix": round(htc_sales_2025_release * htc_carbonated_brand_mix, 1),
    "carbonated_sales_2024_at_2025_brand_mix_ASSUMPTION": round(htc_csd_2024_derived, 1),
    "south_market_times_share": round(htc_south_market * htc_south_share, 1),
    "ratio_htc_carbonated_2025_to_south_market_times_share": round(
        htc_sales_2025_release * htc_carbonated_brand_mix / (htc_south_market * htc_south_share), 4),
    "note": "The 2024 base is derived from the 2025 growth rate, and the carbonated part applies the 2025 brand mix to it. Both steps are assumptions for 2024.",
}

# ---- 3. Sermsuk (est) -------------------------------------------------------
r["sermsuk"] = {
    "source_of_carbonated_line": "Thai SEC Form 250-2 (opinion on a tender offer), dated 8 October 2024, revenue structure table, PDF pages 11 and 63 to 64 (P for those pages). The 15 November 2023 letter gives no carbonated split.",
    "mda_total_matches_form_250_2_table_fy2022_fy2023": {
        "fy2022": [ssc_total_mda[2022], round(ssc_total_table[2022], 2)],
        "fy2023": [ssc_total_mda[2023], round(ssc_total_table[2023], 2)],
    },
    "carbonated_share_of_total": {
        y: round(ssc_csd[y] / ssc_total_table[y], 4) for y in ssc_csd
    },
    "carbonated_growth_fy2023_over_fy2022": round(ssc_csd[2023] / ssc_csd[2022] - 1, 4),
    "carbonated_9m_fy2024_share_of_total": round(ssc_9m_fy2024["csd"] / ssc_9m_fy2024["total"], 4),
    "total_fy2024_mda": ssc_total_mda[2024],
    "note": "Fiscal years end 30 September. The carbonated line is Sermsuk's own revenue (it makes est under a manufacturing contract for the trademark owner), not est retail sales. The FY2024 carbonated line is not printed; the nine-month figure runs to 30 June 2024. The table gives no brand split.",
}

# ---- 4. Sum of bottler lines (derived; mixed periods; NOT a floor) ----------
coke_system_2024 = r["tncc_carbonated_lines"][2024] + htc_csd_2024_derived
sum_ex_sermsuk = coke_system_2024 + big_cola_2024_total_sales_proxy
sum_with_sermsuk = sum_ex_sermsuk + ssc_csd[2023]
niq_nov = niq["to_nov_2024"]
r["bottler_sum"] = {
    "coca_cola_system_carbonated_2024_tncc_reported_plus_htc_derived": round(coke_system_2024, 1),
    "of_which_htc_part_is_assumption": round(htc_csd_2024_derived, 1),
    "plus_big_cola_total_sales_proxy_2024": round(sum_ex_sermsuk, 1),
    "plus_sermsuk_carbonated_fy2023_reported": round(sum_with_sermsuk, 1),
    "sum_with_sermsuk_over_niq_to_nov_2024": round(sum_with_sermsuk / niq_nov, 4),
    "periods": "TNCC calendar 2024 (P as filed); Hadthip 2024 derived from the 2025 release growth rate and the 2025 brand mix (ASSUMPTION); Big Cola 2024 total sales (S, a proxy); Sermsuk fiscal year to 30 September 2023 (P). Mixed periods.",
    "missing": ["Suntory PepsiCo Beverage (Thailand) (Pepsi, Mirinda, 7UP): statements not found",
                "Thai Drinks Co., Ltd. (marketer of est): revenue not found",
                "Coca-Cola (Thailand) Limited (brand owner, does not bottle): no revenue readable from the registry aggregator (T2)",
                "TNCC full-year 2025 and Hadthip statements under the SEC (not opened)",
                "other small brands and imports"],
    "status": "A sum of derived and reported lines on mixed years, with one assumed component and Pepsi missing. It is not a lower bound and does not size the market.",
}
pepsi_illustration = pepsi_share_press * niq_nov
r["sum_plus_pepsi_press_share_illustration"] = {
    "pepsi_30pct_of_niq_to_nov_2024": round(pepsi_illustration, 1),
    "sum_with_sermsuk_plus_that": round(sum_with_sermsuk + pepsi_illustration, 1),
    "ratio_to_niq_to_nov_2024": round((sum_with_sermsuk + pepsi_illustration) / niq_nov, 4),
    "note": "Illustration only. Pepsi's 30 percent has no stated measure (value or volume) and Pepsi's own revenue was not found. The bottler lines are at manufacturer level on mixed periods, and the level of the NielsenIQ value is not stated. The result shows that the sum plus Pepsi at its press share is near the NielsenIQ value; the bottler data therefore do not contradict it.",
}
r["bottler_sum_2024"] = {  # kept for continuity with the earlier record
    "coca_cola_system_carbonated_tncc_plus_htc": round(coke_system_2024, 1),
    "plus_big_cola_sales": round(sum_ex_sermsuk, 1),
    "coke_system_over_niq_to_nov_2024": round(coke_system_2024 / niq_nov, 4),
    "coke_system_over_niq_to_jan_2024": round(coke_system_2024 / niq["to_jan_2024"], 4),
    "coke_share_in_press": coke_share_press,
    "coke_share_times_niq_to_nov_2024": round(coke_share_press * niq_nov, 1),
    "sum_ex_sermsuk_over_niq_to_nov_2024": round(sum_ex_sermsuk / niq_nov, 4),
}
r["press_shares_applied_to_niq_to_nov_2024"] = {
    "coca_cola_51pct": round(coke_share_press * niq_nov, 1),
    "pepsi_30pct": round(pepsi_share_press * niq_nov, 1),
    "est_8_6pct_volume": round(est_share_volume_press * niq_nov, 1),
    "big_cola_3600_over_niq": round(big_cola_2024_total_sales_proxy / niq_nov, 4),
    "note": "Press shares carry no stated measure (only est 8.6 percent is labelled volume), so these are illustrations, not value estimates.",
}

# ---- 5. What the 51 percent share would imply -------------------------------
r["share_implied_market_2024"] = {
    "tncc_carbonated_over_niq_to_nov_2024": round(r["tncc_carbonated_lines"][2024] / niq_nov, 4),
    "tncc_carbonated_over_51_4pct": round(r["tncc_carbonated_lines"][2024] / tncc_share_csd_2024, 1),
    "tncc_implied_vs_niq_to_nov_2024_pct": round(
        r["tncc_carbonated_lines"][2024] / tncc_share_csd_2024 / niq_nov - 1, 4),
    "coke_system_over_niq_to_nov_2024": round(coke_system_2024 / niq_nov, 4),
    "coke_system_over_51pct": round(coke_system_2024 / coke_share_press, 1),
    "coke_system_over_51_4pct": round(coke_system_2024 / tncc_share_csd_2024, 1),
    "note": "Conditional: the filing does not say whether 51.4 percent is by value, or whether it is TNCC alone or the Coca-Cola brand family nationally. TNCC alone is consistent with NielsenIQ. The whole Coca-Cola system implies a producer-level market above the range if 51 percent is a value share.",
}

# ---- 6. NielsenIQ window consistency (explicit, not a proof of one series) --
r["niq_window_consistency"] = {
    "implied_12m_to_nov_2023_from_9pct": round(niq_nov / (1 + niq_growth["to_nov_2024"]), 1),
    "implied_12m_to_jan_2023_from_12pct": round(niq["to_jan_2024"] / (1 + niq_growth["to_jan_2024"]), 1),
    "change_12m_to_nov_2023_to_12m_to_jan_2024_pct": round(
        niq["to_jan_2024"] / (niq_nov / (1 + niq_growth["to_nov_2024"])) - 1, 4),
    "change_to_jan_2024_to_to_nov_2024_pct": round(niq_nov / niq["to_jan_2024"] - 1, 4),
    "change_to_aug_2023_to_to_nov_2024_pct": round(niq_nov / niq["to_aug_2023_press_no_source"] - 1, 4),
    "reading": "The two NielsenIQ-attributed values (66,000 and 70,772) and their stated growth rates are consistent with a rising run, but that is not proof of one series. The 62,000 value names no source and is not counted as NielsenIQ. The 66,000 window (February 2023 to January 2024) is mostly 2023 and the 70,772 window (December 2023 to November 2024) is mostly 2024; they are ten months apart.",
}

# ---- 7. The 2025 press statements: attribution-correct checks ---------------
r["press_2025_checks"] = {
    "bkk_2025_67000_over_niq_to_nov_2024_pct": round(bkk_2025_67000 / niq_nov - 1, 4),
    "niq_to_nov_2024_times_0_96": round(niq_nov * (1 - exec_decline_2025), 1),
    "niq_to_nov_2024_times_0_92": round(niq_nov * (1 - bkk_decline_jan_aug_2025), 1),
    "exec_68000_label_2024_times_0_96": round(exec_68000_label_2024 * (1 - exec_decline_2025), 1),
    "marketeer_2025_70000_over_its_2024_66000_calendar_labels_pct": round(70000.0 / 66000.0 - 1, 4),
    "reading": "70,772 less 4 percent is about 67,900, close to the 68,000 that the ThaiBev executive labels 2024 and to the 67,000 that Bangkokbiznews gives for 2025 with no source. 68,000 may be a 2025 level or a 12 month window to August 2025; the pages do not say. Kept as a possible reading and a stated limit, not as a second 2024 value. The Marketeer +6.1 percent uses its own calendar labels, which are not like for like with the NielsenIQ windows.",
}

# ---- 8. KResearch fit and growth check (two mappings of the unlabelled pair) -
kres_base_map_a = kres_csd / (1 + kres_growth_pair_printed[0])   # 2.0 percent = carbonated (list order, inferred)
kres_base_map_b = kres_csd / (1 + kres_growth_pair_printed[1])   # 2.6 percent = carbonated (alternative)
r["kresearch_check"] = {
    "csd_plus_water_over_nab": round((kres_csd + kres_water) / kres_nab, 4),
    "printed_text": "more than 55 percent",
    "csd_over_nab": round(kres_csd / kres_nab, 4),
    "csd_76900_over_niq_to_nov_2024": round(kres_csd / niq_nov, 4),
    "mapping": "The note prints '2.0% and 2.6%' for carbonated and bottled water without labels. The mapping in list order (carbonated first) is an inference. The same note gives 2.0 percent for the whole non-alcoholic business in 2025 (excerpt lines 11 and 14), so the 2.0 may be the total's growth. Thansettakij (8 September 2025) also prints about 2 percent for the 226,000 total.",
    "nab_total_growth_2025_printed_in_note": kres_nab_growth_2025,
    "map_a_carbonated_2_0pct_base_2024": round(kres_base_map_a, 1),
    "map_a_base_over_niq_to_nov_2024": round(kres_base_map_a / niq_nov - 1, 4),
    "map_b_carbonated_2_6pct_base_2024": round(kres_base_map_b, 1),
    "map_b_base_over_niq_to_nov_2024": round(kres_base_map_b / niq_nov - 1, 4),
    "reading": "Under either mapping the implied 2024 carbonated base is 5.9 to 6.5 percent above the NielsenIQ value to November 2024. So the 76,900 is on a higher level than NielsenIQ, or the forecast growth is not the one applied to it. The 76,900 sits in a chart (Figure 3) that was not read as text, so this is not settled. The conclusion holds whichever of the two printed figures is the carbonated growth.",
}

# ---- 9. Volume, implied price and the Krungsri value gap --------------------
litres = nab_litres_2025 * csd_volume_share
r["krungsri_volume"] = {
    "carbonated_and_soda_million_litres_2025": round(litres, 1),
    "matches_printed_2_7_billion_within_pct": round(abs(litres - krungsri_printed_litres) / krungsri_printed_litres, 4),
    "thb_per_litre_at_66000": round(66000.0 / litres, 2),
    "thb_per_litre_at_70772": round(70772.0 / litres, 2),
    "thb_per_litre_at_76900": round(76900.0 / litres, 2),
    "note": "Volume is carbonated and soda for 2025 (Krungsri, citing Euromonitor). The page does not define the category, which may be wider than carbonated soft drinks. The values are for 2024 or 2025 windows. Team check, not a figure printed on the page. Plausibility check only.",
}
nab_value_thb = krungsri_nab_value_usd_m_2025 * krungsri_thb_per_usd_2025
r["krungsri_value_2025"] = {
    "nab_value_usd_million": krungsri_nab_value_usd_m_2025,
    "thb_per_usd_krungsri": krungsri_thb_per_usd_2025,
    "nab_value_thb_million_derived": round(nab_value_thb, 1),
    "over_kresearch_nab_226000_pct": round(nab_value_thb / kres_nab - 1, 4),
    "note": "Krungsri (15 June 2026) gives domestic non-alcoholic sales of USD 10,555.5 million for 2025, converted at THB 32.88 per USD (its footnote 2). That is about THB 347,000 million, 53.6 percent above the KResearch total of THB 226,000 million for 2025. The two bank totals differ in definition, source or level. The pages read do not explain the gap. The gap bears on whether the 76,900 is at the NielsenIQ level.",
}

# ---- 9b. Non-alcoholic totals in press and bank notes (not like for like) ---
r["nab_totals_2024_2025"] = {
    "marketplus_2024_article_low": marketplus_nab_low,
    "marketplus_2024_article_high": marketplus_nab_high,
    "marketplus_year_not_stated_in_sentence": True,
    "marketplus_csd_share_printed": marketplus_csd_share_nab,
    "marketplus_implied_csd_low": round(marketplus_csd_share_nab * marketplus_nab_low, 0),
    "marketplus_implied_csd_high": round(marketplus_csd_share_nab * marketplus_nab_high, 0),
    "marketplus_printed_csd_value": marketplus_csd_printed,
    "marketplus_internal_gap_low": round(marketplus_csd_printed - marketplus_csd_share_nab * marketplus_nab_high, 0),
    "marketplus_internal_gap_high": round(marketplus_csd_printed - marketplus_csd_share_nab * marketplus_nab_low, 0),
    "kresearch_2025_nab": kres_nab,
    "kresearch_2025_nab_growth_printed": kres_nab_growth_2025,
    "bangkokbiznews_2025_nab_over": bkk_nab_2025_over,
    "krungsri_2025_nab_thb_derived": round(nab_value_thb, 1),
    "reading": "Four non-alcoholic totals with four definitions or levels: 198,000 to 200,000 (MarketPlus, 8 May 2024, year not stated in the sentence), 226,000 (KResearch, 2025), over 260,000 (Bangkokbiznews, 13 October 2025, no source named) and about 347,000 (Krungsri, 2025, USD converted). None is explained in the pages read. MarketPlus's own 31 percent gives 61,380 to 62,000 for carbonated drinks, not the 66,000 it prints.",
}

# ---- 10. Bank of Thailand rates and the StrategyHelix conversion -------------
bot_mid_derived = (bot_buy_sight_15oct + bot_sell_15oct) / 2
r["bot_check"] = {
    "source": "Bank of Thailand report FM_FX_001_S3 (reportID 123), read 20 October 2026 (P). Date column: 15 OCT 2026.",
    "reference_rate_usd_printed": bot_reference_15oct,
    "buying_sight_usd_printed": bot_buy_sight_15oct,
    "buying_transfer_usd_printed": bot_buy_transfer_15oct,
    "selling_usd_printed": bot_sell_15oct,
    "midpoint_buying_sight_and_selling_derived": round(bot_mid_derived, 4),
    "midpoint_minus_printed_reference_rate": round(bot_mid_derived - bot_reference_15oct, 4),
    "note": "The 33.4246 row is printed as BUYING TRANSFER (the earlier raw file of 19 October 2026 labelled it 'bill'). The printed reference rate is used for the conversion. The midpoint is DERIVED and is not a published rate.",
}
r["strategyhelix_thb_million"] = {
    "2026_at_bot_reference_rate_DERIVED": round(usd_bn_2026 * 1000 * bot_reference_15oct, 0),
    "2031_at_bot_reference_rate_DERIVED": round(usd_bn_2031 * 1000 * bot_reference_15oct, 0),
    "2026_at_team_midpoint_check_DERIVED": round(usd_bn_2026 * 1000 * bot_mid_in_team_files, 0),
    "ratio_2026_at_reference_to_niq_to_nov_2024": round(usd_bn_2026 * 1000 * bot_reference_15oct / niq_nov, 3),
    "note": "Converted at the BOT reference rate for 15 October 2026. Reproduced on 20 October 2026 from the BOT table. The source does not state the level or the sources of the market size, so the figure is not used as a market value.",
}

# ---- 11. Canned carbonated figure ------------------------------------------
r["canned_13172"] = {
    "singha_over_canned_market": round(singha_sales_2022_press / canned_market_2022_press, 4),
    "canned_over_csd_2022_57000": round(canned_market_2022_press / csd_2022, 4),
    "can_share_10pct_of_57000": round(can_share_2022 * csd_2022, 0),
    "canned_over_that": round(canned_market_2022_press / (can_share_2022 * csd_2022), 2),
    "note": "The 13,172 figure has no year, no source and no level (Marketeer, 16 August 2022). The year of the 1,357 million Singha sales value is also not stated. The 10.3 percent Singha share divides two undated numbers and is not a market share.",
}

# ---- 12. Colour (non-cola) and clear sub-segments --------------------------
r["colour_clear_segment"] = {
    "bkk_colour_nielseniq_sep2024_aug2025": colour_niq_bkk_sep2024_aug2025,
    "thansettakij_colour_unattributed_no_period": colour_unattributed_thansettakij,
    "bkk_17300_over_bkk_2025_67000_mixed_window": round(colour_niq_bkk_sep2024_aug2025 / bkk_2025_67000, 4),
    "bkk_17300_note": "Mixed window: the 67,000 value has no window (Bangkokbiznews). Not a share of a common period. Not used for sizing.",
    "marketeer_regular_colour_or_clear_18pct_of_66000": round(colour_clear_share_2024 * 66000.0, 0),
    "marketeer_note": "The 18 percent line excludes zero-sugar variants (15 percent, separate line), so it is a floor for the non-cola segment, not its size.",
    "positioningmag_2019_clear_6pct_of_56000": round(pos2020["clear"] * pos2020["market_2019"], 0),
    "positioningmag_2019_colour_plus_clear_share": round(pos2020["colour"] + pos2020["clear"], 2),
    "positioningmag_2019_growth_printed_text": "almost 12 percent (from about 50,900 million)",
    "positioningmag_2019_growth_from_its_printed_figures": round(pos2020["market_2019"] / pos2020["market_2018"] - 1, 4),
    "positioningmag_growth_note": "The article's text says almost 12 percent; its own printed figures give 10.0 percent. The article is internally inconsistent on growth. Neither growth figure is used.",
    "lemon_lime_only": "not found",
}

# ---- 13. Press values of the market: the spread of statements, not one range --
press_statements = [
    {"value": gotomanager_value_2023, "label": "all carbonated, 2023 article, no source named (GotoManager)", "tier": "S"},
    {"value": niq["to_aug_2023_press_no_source"], "label": "all carbonated, growth window to August 2023, no source named (Thairath)", "tier": "S"},
    {"value": aj_value_624003, "label": "AJ Thai Big Cola section, 3 April 2025, no year, no source", "tier": "S"},
    {"value": niq["to_jan_2024"], "label": "NielsenIQ as printed by MarketPlus and Thansettakij, 12 months to January 2024", "tier": "S"},
    {"value": aj_intro_value_624003, "label": "Thansettakij intro 3 April 2025, no year, no source", "tier": "S"},
    {"value": niq["to_nov_2024"], "label": "NielsenIQ as printed by Thansettakij, 12 months to November 2024", "tier": "S"},
    {"value": bkk_2025_67000, "label": "Bangkokbiznews 2025, window not stated, no source named", "tier": "S"},
    {"value": exec_68000_label_2024, "label": "ThaiBev executive (named), Thansettakij 13 October 2025, labelled 2024", "tier": "S"},
    {"value": 70000.0, "label": "Marketeer compilation 2025 (NielsenIQ and brand forecasts)", "tier": "S"},
    {"value": kres_csd, "label": "Kasikorn Research Center estimate or forecast 2025 (as relayed by Thansettakij)", "tier": "S"},
]
vals = [p["value"] for p in press_statements]
r["press_value_spread_all_statements"] = {
    "min": min(vals),
    "max": max(vals),
    "statements": sorted(press_statements, key=lambda p: p["value"]),
    "note": "The spread of statements, not a range. The endpoints have different windows and one is a forecast.",
}

# ---- 14. Dark-cola shares (not used to size a segment) ----------------------
r["dark_cola_shares_check"] = {
    "shares_624003_printed": shares_624003,
    "sum_of_printed_shares_pct": round(sum(shares_624003.values()), 1),
    "note": "The shares do not add to 100 percent (they add to 103.9), so they are not shares of one total. AJ Thai's 85 percent dark cola and Pepsi's 72 percent forecast (26 March 2025) disagree; neither is used.",
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(r, f, ensure_ascii=False, indent=2, sort_keys=True)
print(json.dumps(r, ensure_ascii=True, indent=2, sort_keys=True))
