"""T6 fourth pass, revised 20 October 2026 after the second independent verifier round.

Arithmetic for slide 4 of the Singha Lemon Soda can. Every input is a figure printed on a page read on 20 October 2026
(WebFetch extracts, saved under rework/raw/diligence_2026-10-20/T6/) or on a saved primary file. Derived numbers are our
arithmetic and are marked DERIVED in the output. Nothing is estimated and nothing comes from a search snippet.
There is no random draw, so no seed is needed. Standard library only; memory use is far below 300 MB.

Run:  python t6_can_leverage_calc_2026-10-20.py
Writes t6_can_leverage_results_2026-10-20.json next to this script.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "t6_can_leverage_results_2026-10-20.json"
CAN_L = 0.33  # litres in one 330 mL can


def per_can(price, cans):
    """THB per can and THB per litre for a pack price."""
    pc = price / cans
    return round(pc, 4), round(pc / CAN_L, 2)


def printed_discount_floor(price, reference):
    """Whole-percent discount between a selling price and a struck-through price, rounded down."""
    return int(math.floor((1.0 - price / reference) * 100 + 1e-9))


res = {
    "note": ("DERIVED arithmetic on figures printed on pages read 20 October 2026 and on saved primary files. "
             "Tiers and status sit in rework/69_can_leverage_verification.md (fourth pass, revised)."),
    "read_date": "2026-10-20",
    "revision": "fourth pass, after the second independent verifier round (20 October 2026)",
}

# ---- 1. Pack listings read on 20 October 2026 (files 04 and 13; re-reads in file 18) ------------------------
# A pack price printed with "Each" is read as the pack price, the same convention on every Lotus's page
# (a single can is listed at THB 17.00 on the same retailer). The reading is stated on the slide.
pack_listings = [
    # retailer, product, pack price THB, cans, status, source
    ("Lotus's online", "Lemon six-can pack, non-member price (printed 'Each', read as the pack price)", 85.0, 6,
     "used (range high, non-member)", "file 13; lotuss.com/en/product/singha-lemon-soda-can-330ml-6-51109221"),
    ("Lotus's online", "Lemon six-can pack, Club Card member price", 81.0, 6,
     "used (range low, member price)", "file 13; same page"),
    ("Lotus's online", "Lemon 24-can pack (printed 330.00 'Each', read as the pack price)", 330.0, 24,
     "used", "file 04; shopping.lotuss.com/en/product/169912032"),
    ("Makro Pro", "Lemon six-can pack, read as 82 (the page also prints 78 beside 'buy 3 or more')", 82.0, 6,
     "NOT USED: the one-pack price is not labelled and the printed features point in different directions (file 18 item 17)",
     "files 04, 13 and 18 items 10 and 17; makro.pro/p/02emhsl-6814746706115"),
    ("Makro Pro", "Lemon 24-can pack (printed 325; per unit 13.54; 330 struck through, -1%)", 325.0, 24,
     "used (range low)", "file 13; makro.pro/p/mpnvmxs-7350275997891"),
    ("7-Eleven ALL Online", "Lemon 24-can case (printed 330; 408 struck through, -19%; validity to 20 October 2026)", 330.0, 24,
     "used (range high)", "file 13; allonline.7eleven.co.th/p/.../474313/"),
    ("7-Eleven ALL Online", "Lemon six-can pack (printed 172; 182 struck through, -5%; validity to 20 October 2026)", 172.0, 6,
     "excluded as an outlier; disclosed on the slide", "file 13 and file 18 item 7; allonline.7eleven.co.th/p/.../514221/"),
    ("Lotus's online", "Lemon single can", 17.0, 1,
     "used", "file 13; shopping.lotuss.com/en/product/singha-lemon-soda-zero-sugar-lemon-soda-330ml-50986847"),
]

rows = []
for retailer, product, price, cans, status, src in pack_listings:
    pc, pl = per_can(price, cans)
    rows.append({"retailer": retailer, "product": product, "pack_price_thb": price, "cans": cans,
                 "per_can_thb": pc, "per_litre_thb": pl, "status": status, "source": src})
res["listings_20oct2026"] = rows

# ---- 2. Other flavours on listings read 20 October 2026 (file 04 read the same day; file 18 re-reads) -------
# Prices as printed. Used only to close the flavour question; none of the Makro six-can prices is in any range.
flavour_listings = [
    ("Lemon Cream", "Lotus's single can (pack size not printed; 'Each')", 17.0, 1, "file 04; file 18 item 9"),
    ("Lemon Cream", "Makro Pro six-can pack (price as printed; not used in any range)", 79.0, 6, "file 04"),
    ("Lemon Cream", "7-Eleven ALL Online 24-can case", 330.0, 24, "file 04 search page"),
    ("Pink", "Lotus's single can", 17.0, 1, "file 04"),
    ("Pink", "Lotus's 24-can pack", 337.0, 24, "file 04"),
    ("Pink", "Makro Pro six-can pack (price as printed; not used in any range)", 82.0, 6, "file 04"),
    ("Pink", "Makro Pro 24-can pack", 325.0, 24, "file 04"),
    ("Pink", "7-Eleven ALL Online 24-can case", 330.0, 24, "file 04 search page"),
    ("Red", "Lotus's single can", 17.0, 1, "file 04"),
    ("Red", "Makro Pro six-can pack (price as printed; not used in any range)", 79.0, 6, "file 04"),
    ("Red", "Makro Pro 24-can pack", 325.0, 24, "file 04"),
    ("Red", "7-Eleven ALL Online 24-can case", 330.0, 24, "file 04 search page"),
    ("Red", "7-Eleven ALL Online six-can pack (THB 172, the same as the excluded Lemon six-pack; not used)", 172.0, 6,
     "file 04 search page"),
    ("Ume", "Makro Pro six-can pack (price as printed; not used in any range)", 82.0, 6, "file 04; file 18 item 10"),
    ("Ume", "7-Eleven ALL Online 24-can case", 330.0, 24, "file 04 search page"),
    ("Watermelon (limited edition)", "7-Eleven ALL Online 24-can case (342 struck through; validity 26/02/2026 to 20/10/2026)",
     330.0, 24, "file 18 item 8"),
]
fl_rows = []
for flavour, product, price, cans, src in flavour_listings:
    pc, pl = per_can(price, cans)
    fl_rows.append({"flavour": flavour, "listing": product, "price_thb": price, "cans": cans,
                    "per_can_thb": pc, "per_litre_thb": pl, "source": src})
res["flavour_listings_20oct2026"] = fl_rows
res["flavour_status_20oct2026"] = {
    "Lemon": "on sale: Lotus's, Makro Pro, 7-Eleven online; Lazada page read with no price (S, 20 October 2026)",
    "Pink": "on sale: Lotus's, Makro Pro, 7-Eleven online (S, 20 October 2026)",
    "Red": "on sale: Lotus's, Makro Pro, 7-Eleven online (S, 20 October 2026)",
    "Ume": "on sale: Makro Pro, 7-Eleven online (S, 20 October 2026)",
    "Lemon Cream": "on sale: Lotus's, Makro Pro, 7-Eleven online (S, 20 October 2026)",
    "Watermelon (limited edition)": "listed at 7-Eleven online; promotion validity printed to 20 October 2026, the read date (S)",
    "Yuzu": ("NOT FOUND in the reads: no listing in the nine Makro Pro lemon-soda results (file 04), none in the first 20 "
             "of 110 Makro Pro results for 'singha yuzu' (file 18 item 12), and the 7-Eleven search feature was unavailable "
             "(file 18 item 11). Not closed."),
    "Melon (limited edition, six months from April 2025)": "no listing read; reported as a six-month summer edition (S). Not closed; not expected on sale.",
}

# ---- 3. Makro six-can pack: the one-pack price is not settled --------------------------------------------
res["makro_unit_price_checks"] = {
    "lemon_24_printed_unit_13_54": {"computed_325_over_24": round(325.0 / 24, 2), "printed": 13.54,
                                     "matches": round(325.0 / 24, 2) == 13.54},
    "lemon_6_printed_unit_13_67_equals_82_over_6": {"computed_82_over_6": round(82.0 / 6, 2), "printed": 13.67,
                                                    "matches": round(82.0 / 6, 2) == 13.67},
    "lemon_6_78_over_6_if_78_is_one_pack": round(78.0 / 6, 2),
}
discount_pairs = [
    {"label": "7-Eleven 24-can case, 330 against struck 408", "printed_pct": 19,
     "computed_floor_pct": printed_discount_floor(330.0, 408.0)},
    {"label": "7-Eleven six-can pack, 172 against struck 182", "printed_pct": 5,
     "computed_floor_pct": printed_discount_floor(172.0, 182.0)},
    {"label": "Makro Pro 24-can case, 325 against struck 330", "printed_pct": 1,
     "computed_floor_pct": printed_discount_floor(325.0, 330.0)},
    {"label": "Makro Pro lemon six-can pack, 78 against 82", "printed_pct": 4,
     "computed_floor_pct": printed_discount_floor(78.0, 82.0)},
    {"label": "Makro Pro lemon six-can pack, 82 against 82 (if 82 were the selling price)", "printed_pct": 4,
     "computed_floor_pct": printed_discount_floor(82.0, 82.0)},
]
res["makro_discount_label_check"] = {
    "pairs": discount_pairs,
    "reading": ("The printed percentages match the whole-percent discount rounded down on the first three pairs and on the "
                "78 against 82 pair. The printed -4% fits 78 against 82 and no other pair. The printed per-unit 13.67 fits 82 "
                "over 6, and the Makro 24-can per-unit price fits the selling price, so the two printed features point in "
                "different directions. The page does not label the one-pack price. The Makro six-can figure is not used in any "
                "range. This is an inference from the page layout (DERIVED), not a printed fact."),
}

# ---- 4. Slide ranges per can (online listings; not store shelf prices) ----------------------------------
six_member = per_can(81.0, 6)[0]        # Lotus's Club Card member price, 6 cans
six_nonmember = per_can(85.0, 6)[0]     # Lotus's non-member price, 6 cans
six_makro_if_82 = per_can(82.0, 6)[0]   # Makro Pro, if 82 is the one-pack price (not used)
six_makro_if_78 = per_can(78.0, 6)[0]   # Makro Pro, if 78 is the one-pack price (not used)
case_makro = per_can(325.0, 24)[0]      # Makro Pro 24-can case
case_lotus = per_can(330.0, 24)[0]      # Lotus's 24-can pack
case_711 = per_can(330.0, 24)[0]        # 7-Eleven online 24-can case
res["slide_ranges_per_can_thb"] = {
    "lemon_six_pack_member_lotuss": round(six_member, 2),
    "lemon_six_pack_nonmember_lotuss": round(six_nonmember, 2),
    "lemon_six_pack_range_lotuss_only": [round(six_member, 2), round(six_nonmember, 2)],
    "lemon_six_pack_makro_if_82_one_pack_not_used": round(six_makro_if_82, 2),
    "lemon_six_pack_makro_if_78_one_pack_not_used": round(six_makro_if_78, 2),
    "lemon_six_pack_makro_status": "not used in any range; the one-pack price is not settled (see makro_discount_label_check)",
    "lemon_case_24_range": [round(case_makro, 2), round(case_711, 2)],
    "lemon_case_24_lotuss": round(case_lotus, 2),
    "single_can_lotuss_online": 17.00,
    "single_can_per_litre_thb": per_can(17.0, 1)[1],
    "excluded_six_pack_172_per_can": round(per_can(172.0, 6)[0], 2),
    "note": ("Online listings read 20 October 2026. Not store shelf prices. The six-can range uses Lotus's only (THB 81 member "
             "and THB 85 non-member). The 24-can range uses Makro Pro (THB 325) and Lotus's and 7-Eleven online (THB 330). "
             "The 7-Eleven six-can pack at THB 172 is excluded and disclosed on the slide. Lotus's 'Each' is read as the pack price."),
}

res["seven_eleven_validity_windows_printed"] = {
    "case_24": "11/08/2020 - 20/10/2026",
    "six_pack": "09/06/2021 - 20/10/2026",
    "watermelon_case_24": "26/02/2026 - 20/10/2026",
    "note": ("All windows end on the read date. The pages do not say what the window covers. The case window's start date "
             "(11 August 2020) is a listing or promotion date, not a launch date, and is not used as one."),
}

# ---- 5. Launch dating (press; read 20 October 2026 and saved) ----------------------------------------------
res["launch_dating_reports"] = [
    {"date": "19 Aug 2020", "source": "Brand Buffet, tagged PR (file 12; same article as brandbuffet.in.th/?p=153039)",
     "statement": "can sold at 330 mL, 16 baht, 7-Eleven nationwide; the product 'launched' with no date printed"},
    {"date": "20 Aug 2020", "source": "Marketeer, archives/183206 (opened 20 Oct 2026)",
     "statement": "330 mL can at 16 baht from 7-Eleven nationwide; no launch date printed"},
    {"date": "22 Sep 2020 (22 ก.ย. 2563)", "source": "Positioning, strategic-move/76404 (file 12)",
     "statement": "channel plan in the future tense; first-period sales five times the planned target"},
    {"date": "4 Jun 2021", "source": "MGR Online, 9640000054177 (file 18 item 1)",
     "statement": "entered the market in late 2563 (late 2020 in the Buddhist calendar)"},
    {"date": "3 Sep 2023", "source": "Marketeer, archives/321216 (file 18 item 2)",
     "statement": "first launch in late 2563 (late 2020)"},
    {"date": "11 Aug 2020 (validity start)", "source": "7-Eleven ALL Online case page (file 13)",
     "statement": "validity window start only; not a launch date"},
]
res["launch_month_status"] = ("Not settled. The August 2020 PR article reports the can on sale without a date. Two later articles "
                              "date the first launch to late 2020. The slide reports both.")

# ---- 6. Price history per can (list prices read in the press; DERIVED per litre) --------------------------
history = [
    ("2020 (PR article 19 Aug 2020)", "Lemon", 16.0, "Brand Buffet, 19 Aug 2020, tagged PR"),
    ("2021 (reported 8 Jun 2021)", "Yuzu", 16.0, "Brand Inside, 8 Jun 2021"),
    ("2022 (reported 15 Aug 2022)", "Red", 16.0, "Thansettakij, 15 Aug 2022; Marketingoops, 15 Aug 2022"),
    ("2023 (reported 3 Sep 2023)", "Ume", 17.0, "Marketeer, 3 Sep 2023; Brand Inside, 4 Sep 2023"),
    ("2024 (reported 25 Jun 2024)", "Pink", 17.0, "Marketeer, 25 Jun 2024"),
    ("2026 (Lotus's online, 20 Oct 2026)", "Lemon single", 17.0, "Lotus's online, read 20 Oct 2026"),
]
res["price_history_per_can_thb"] = [
    {"date": d, "flavour": f, "price_thb": p, "per_litre_thb": round(p / CAN_L, 2), "source": s}
    for d, f, p, s in history
]
res["price_rise_2022_to_2023_pct"] = round((17.0 / 16.0 - 1) * 100, 2)

# ---- 7. Volume arithmetic (Thansettakij 15 Aug 2022; Marketeer 16 Aug 2022, two articles) ------------------
vol_2021_l = 28.0e6          # litres, printed for 2564 (2021)
vol_target_2022_l = 45.0e6   # litres, printed target for 2565 (2022), "over 45 million"
sales_value_printed_thb_m = 1357.0  # printed "about 1,357 million baht", no year in Thansettakij
revenue_2021_marketeer_thb_m = 1357.0   # Marketeer 275740 (16 Aug 2022): "revenue was only 1,357 million baht" in the previous year
revenue_2022_target_marketeer_thb_m = 2200.0  # Marketeer 275740: "generating 2,200 million baht in revenue this year"
cans_2021 = vol_2021_l / CAN_L
cans_target = vol_target_2022_l / CAN_L
diff_pct = (cans_2021 * 16.0 / 1e6 - sales_value_printed_thb_m) / sales_value_printed_thb_m * 100
res["volume_arithmetic"] = {
    "cans_2021_million": round(cans_2021 / 1e6, 2),
    "cans_2022_target_million": round(cans_target / 1e6, 2),
    "target_over_2021_pct_increase": round((vol_target_2022_l / vol_2021_l - 1) * 100, 2),
    "value_check_84_85m_cans_at_16_thb_million": round(cans_2021 * 16.0 / 1e6, 2),
    "value_check_difference_pct_vs_printed_1357": round(diff_pct, 2),
    "press_2021_sales_value_thb_m_thansettakij": sales_value_printed_thb_m,
    "press_2021_revenue_thb_m_marketeer_275740": revenue_2021_marketeer_thb_m,
    "press_2022_revenue_target_thb_m_marketeer_275740": revenue_2022_target_marketeer_thb_m,
    "implied_revenue_per_can_at_2022_target_thb": round(revenue_2022_target_marketeer_thb_m * 1e6 / cans_target, 2),
    "reading": ("The printed 1,357 million equals the 2021 volume (84.85 million cans, 28 million litres) at THB 16 a can to within "
                "0.04 per cent. Thansettakij prints no year and no basis. Marketeer (16 Aug 2022) calls the figure the previous "
                "year's revenue. Neither article names a source for the 1,357 million figure; its basis is not confirmed."),
}
res["press_attribution_2022"] = {
    "thansettakij_15_aug_2022": ("the 28 and 45 million litre figures and the 1,357 million figure are in the article's own wording; "
                                 "no named source or company statement is attached (checked 20 Oct 2026)"),
    "marketeer_16_aug_2022_275740": ("the same figures, with 2021 revenue of 1,357 million and a 2022 target of 2,200 million; "
                                     "the 2022 target of 45 million litres and 2,200 million baht is attributed to Singha's expectations in general terms; the 2021 figures carry no named source (checked 20 Oct 2026)"),
    "marketeer_16_aug_2022_275504": ("the same 28, 45, 1,357 and 13,172 million figures in one sentence (checked 20 Oct 2026)"),
}

wm_cans = 2.0e6   # Watermelon limited edition, "limited to 2 million cans" (Brand Buffet, 16 Mar 2026, PR-tagged)
res["limited_edition"] = {"watermelon_cans_million": 2.0,
                          "watermelon_litres_million": round(wm_cans * CAN_L / 1e6, 2)}
res["limited_edition_dates"] = {
    "melon": {
        "marketeer_408963": ("2 April 2025 (printed 02/04/2025): sold as a limited edition only during the summer season, "
                             "for six months; the start month is not stated"),
        "brand_buffet_2025_04": "4 April 2025: on sale through this summer for six months; 7-Eleven nationwide and Singha Online Shop",
        "slide_wording": "Melon, a six-month summer edition reported in April 2025 (S)",
    },
    "watermelon": {
        "brand_buffet_2026_03": ("16 March 2026, PR-tagged: two million cans, two label designs, 7-Eleven all branches and "
                                 "Singha Online"),
        "bloody_nanno_name": ("the article body uses 'Bloody Nanno' as the product name for the watermelon flavour (file 18 item 16); "
                              "the slide uses 'Watermelon limited edition'"),
        "7_eleven_case_validity": "26/02/2026 to 20/10/2026 (printed); the promotion ends on the read date",
    },
}

# ---- 8. Canned market and share claims (Positioning 4 Jul 2022 at two URLs; press 2023) -------------------
csd_2021_thb_m = 62725.0     # printed 2021 CSD market (Positioning 4 Jul 2022)
canned_share = 0.21          # printed 21% of the CSD market is canned packaging
canned_value_printed = 13172.0
res["canned_market_year_check"] = {
    "csd_2021_times_21pct_million": round(csd_2021_thb_m * canned_share, 2),
    "difference_to_printed_13172_million": round(csd_2021_thb_m * canned_share - canned_value_printed, 2),
    "reading": ("Read as the 2021 canned figure by arithmetic (DERIVED); Positioning 4 Jul 2022 prints '2564' for the CSD market "
                "and no year beside 13,172 million."),
}
res["share_claims_company"] = {
    "q4_2020_share_pct": 4,
    "source": "MGR Online, 4 Jun 2021 (company claim; 4% of canned carbonated drinks in the last quarter of 2020)",
    "canned_format_share_pct_sep2023": 52,
    "source2": ("Marketeer, 3 Sep 2023 (press; 'Singha Lemon Soda holds 52% in the canned format'). The same paragraph gives the "
                "sugar-free carbonated soft drink market at about THB 6,930 million and growth above 25%. No period is printed, "
                "and the base of the 52% is not stated."),
    "sugar_free_csd_market_thb_m_marketeer_2023": 6930,
    "sugar_free_csd_market_thb_m_brandinside_headline_2023": 7000,
    "note": "Not used on slide 4 as a verified market share. The 52% is shown as a company claim as reported by press.",
}
pos_12 = 0.12 * canned_value_printed
res["share_12pct_mismatch_positioning_4jul2022"] = {
    "urls": ["https://positioningmag.com/strategic-move/88360", "https://positioningmag.com/1391149"],
    "twelve_pct_of_13172_million": round(pos_12, 1),
    "printed_value_million": 1450,
    "printed_value_as_share_of_13172_pct": round(1450 / canned_value_printed * 100, 2),
    "printed_value_as_share_of_csd_2021_pct": round(1450 / csd_2021_thb_m * 100, 2),
    "printed_2_4_pct_of_csd_2021_million": round(0.024 * csd_2021_thb_m, 1),
    "reading": ("The article does not say which market the 12% refers to. The printed 12% and 1,450 million fit neither the canned "
                "base (12% of 13,172 is about 1,581 million) nor the total CSD base. 1,450 is 2.31% of 62,725; the article's "
                "own 2.4% share of total CSD would be about 1,505 million. Conflict, not used on slide 4."),
}

# ---- 9. Can maker, BJC 56-1 One Report 2025 (saved in T6/08, printed figures) ----------------------------
tbc_cap = {"2023": 3440, "2024": 3780, "2025": 3880}
tbc_act = {"2023": 2027, "2024": 2214, "2025": 2307}
tbc_usage_printed = {"2023": 58.92, "2024": 58.57, "2025": 59.46}
vn_act = {"2023": 1910, "2024": 1764, "2025": 1959}
seg_sales_2025 = 11852.0       # THB million, aluminium can business, printed
tbc_rev_2025 = 11909.031       # THB million, total revenue 2025, printed
tbc_profit_2025 = 1356.513
tbc_rev_2024 = 12374.731
tbc_profit_2024 = 1551.215
cans_both_2025 = tbc_act["2025"] + vn_act["2025"]
res["can_maker_bjc_2025"] = {
    "capacity_2025_million_cans": tbc_cap["2025"],
    "actual_2025_million_cans": tbc_act["2025"],
    "usage_2025_computed_pct": round(tbc_act["2025"] / tbc_cap["2025"] * 100, 2),
    "usage_2025_printed_pct": tbc_usage_printed["2025"],
    "spare_2025_million_cans": tbc_cap["2025"] - tbc_act["2025"],
    "spare_2025_pct": round((tbc_cap["2025"] - tbc_act["2025"]) / tbc_cap["2025"] * 100, 2),
    "capacity_growth_2023_to_2025_pct": round((tbc_cap["2025"] / tbc_cap["2023"] - 1) * 100, 2),
    "vietnam_actual_2025_million_cans": vn_act["2025"],
    "thai_plus_vietnam_actual_2025_million_cans": cans_both_2025,
    "target_2022_cans_as_pct_of_capacity_2025": round(cans_target / 1e6 / tbc_cap["2025"] * 100, 2),
    "target_2022_cans_as_pct_of_output_2025": round(cans_target / 1e6 / tbc_act["2025"] * 100, 2),
    "revenue_per_can_blended_upper_thb": round(seg_sales_2025 / cans_both_2025, 2),
    "revenue_per_can_upper_bracket_thai_cans_only_thb": round(tbc_rev_2025 / tbc_act["2025"], 2),
    "scope_caution": ("Capacity and output are for all can sizes and all customers. They are not the capacity "
                      "of the 330 mL can or of any Boon Rawd plant."),
}
res["can_maker_margins_2025_2024"] = {
    "net_margin_2025_pct": round(tbc_profit_2025 / tbc_rev_2025 * 100, 2),
    "net_margin_2024_pct": round(tbc_profit_2024 / tbc_rev_2024 * 100, 2),
    "note": "The can maker's margins, not Singha's.",
}

# ---- 10. Singha Corporation group, press figures (file 14, file 18 item 13; S, no filing named) ------------
sc = {
    "2021": {"revenue_m": 4226.6397, "net_profit_m": 3590.7008,
             "source": "Thaiger, 18 Apr 2025 (S; year printed; cites the company site, no filing named)"},
    "2024": {"revenue_m": 3950.0, "net_profit_m": 3135.0,
             "source": "MGR Online, 23 May 2026 (S; revenue year printed; net profit year inferred by position)"},
    "2025": {"revenue_m": 3892.0, "net_profit_m": 3085.0,
             "source": "MGR Online, 23 May 2026 (S; revenue year printed; net profit year inferred by position)"},
}
res["singha_corporation_press"] = {}
for y, v in sc.items():
    res["singha_corporation_press"][y] = {
        "revenue_m": v["revenue_m"], "net_profit_m": v["net_profit_m"], "source": v["source"],
        "net_margin_pct": round(v["net_profit_m"] / v["revenue_m"] * 100, 2),
        "margin_basis": "not stated in the press",
    }
res["singha_corporation_changes_2025_vs_2024"] = {
    "revenue_pct": round((3892.0 / 3950.0 - 1) * 100, 2),
    "net_profit_pct": round((3085.0 / 3135.0 - 1) * 100, 2),
    "note": "Derived from press figures; not checked against a filing.",
}
res["boon_rawd_2022_press"] = {"revenue_m": 11711, "net_profit_m": 5793,
                               "source": "Thaiger, 18 Apr 2025 (S; Boon Rawd, not Singha Corporation)"}
res["tracxn_band"] = {
    "text": "$100M - $500M as on Dec 31, 2023 (annual revenue band)",
    "opened_20_oct_2026": "yes, by WebFetch (the page shows an 'Internal Server Error' banner; the content was readable)",
    "reported_or_estimated": "not stated on the page",
    "used_as_figure": False,
}

# ---- 11. Metal cost per can at the saved LME and Bank of Thailand inputs (NOT REPRODUCED; NOT USED) ---------
lme_bid, lme_offer = 3013.0, 3014.0          # USD per tonne, LME cash, saved file; data valid 16 Oct 2026
fx_buy, fx_sell = 33.3535, 33.7455           # THB per USD, saved BOT copy, as of 15 Oct 2026
sheet_g_low, sheet_g_high = 14.4, 18.5       # grams of sheet per can (ASSUMPTION)
metal_low = sheet_g_low / 1000 * (lme_bid / 1000) * fx_buy
metal_high = sheet_g_high / 1000 * (lme_offer / 1000) * fx_sell
res["metal_cost_per_can_thb"] = {
    "status": ("NOT REPRODUCED on 20 October 2026 and NOT USED anywhere. The LME page returned HTTP 403 today. The saved LME file "
               "says it was read in the user's Chrome on 19 October 2026 (raw line 4). CLAUDE.md section 4 allows Claude in "
               "Chrome only on a named request, and none is recorded. The route is not authorised; the lead must confirm it."),
    "reproduced_20_oct_2026": False,
    "route_authorised": False,
    "used_on_slide": False,
    "lme_cash_usd_per_kg_low": round(lme_bid / 1000, 4),
    "lme_cash_usd_per_kg_high": round(lme_offer / 1000, 4),
    "thb_per_kg_low": round(lme_bid / 1000 * fx_buy, 2),
    "thb_per_kg_high": round(lme_offer / 1000 * fx_sell, 2),
    "metal_low_thb_per_can": round(metal_low, 3),
    "metal_high_thb_per_can": round(metal_high, 3),
    "inputs_note": ("Sheet mass is an ASSUMPTION (14.4 to 18.5 g). Excludes the regional premium, scrap credit and lids. "
                    "The Bank of Thailand rate is a saved copy whose route is not recorded and which was not re-verified on 20 October 2026."),
}
res["lme_status"] = {
    "live_20_oct_2026": "https://www.lme.com/en/metals/non-ferrous/lme-aluminium returned HTTP 403 (re-tested 20 October 2026)",
    "saved_file": "raw/lme_trading_summary_primary_2026-10-19.md; line 4: 'Read in the user's Chrome, 19 October 2026.'",
    "route_status": "not authorised: no named request in the record (CLAUDE.md section 4); the lead must confirm",
    "settlement_price": "not obtained. The brief asked for the settlement price; the saved file holds the official cash bid and offer only",
    "used_on_slide": False,
    "limit": "LME input is a stated limit; it is not used in any judge-facing text",
}
res["bot_rates_status"] = {
    "saved_copy": ("raw/bot_fx_primary_2026-10-15.md (read 19 October 2026): average buying (sight) 33.3535, buying (bill) 33.4246, "
                   "selling (transfer) 33.7455 baht per USD, as of 15 October 2026"),
    "route_recorded_in_saved_file": False,
    "live_page_20_oct_2026": ("https://www.bot.or.th/en/statistics/exchange-rate.html printed no rate table and no as-of date; "
                              "it links to thaifxrates.net, which is not a primary source"),
    "tier": "P as a saved copy; NOT re-verified on 20 October 2026",
    "used_on_slide": False,
}

# ---- 12. Excise (Royal Gazette schedule, saved copy; P) -------------------------------------------------
res["excise_02_02_1oct2566"] = {
    "ad_valorem_pct": 14,
    "per_litre_thb_by_sugar_per_100ml": {"up_to_6g": 0, "over_6_to_8g": 1, "over_8_to_10g": 3, "over_10g": 5},
    "lemon_soda_tier": "up_to_6g (zero sugar, sweetened and flavoured, so 02.02)",
    "per_litre_thb_for_lemon_soda": 0,
    "per_can_from_per_litre_part_thb": 0.0,
    "ad_valorem_base": "not read; the 14% cannot be turned into baht per can",
    "gazette_pdf_20_oct_2026": "HTTP 403 Forbidden (re-tested 20 October 2026); the saved copy was read from page images",
    "note": "Later amendments not searched. Figures read from page images; a second reader should check the Thai numerals. Not on slide 4.",
}

# ---- 13. Retail reach (P) and Big C tier -------------------------------------------------------------------
bigc = {"supercenter": 140, "extra": 13, "market": 36, "foodplace": 17, "mini": 1490}
res["retail_reach_p"] = {
    "seven_eleven_stores_end_2025": 15945,
    "seven_eleven_scope_read": ("CP ALL prints 'the total number of stores' at the end of 2025. The scope is not stated in the source. "
                                "Read as its 7-Eleven network in Thailand by inference: the same document gives 700 new stores in "
                                "Thailand and 138 international stores separately."),
    "seven_eleven_international_stores_2025": 138,
    "big_c_components_tier": "P (BJC One Report 2025, printed component counts)",
    "big_c_large_formats_thailand_31dec2025": sum(v for k, v in bigc.items() if k != "mini"),
    "big_c_all_formats_thailand_31dec2025": sum(bigc.values()),
    "big_c_total_tier": "DERIVED (sum of the printed components; the source text says 'sum by us')",
    "big_c_note": "Not a count of outlets that carry the can. Big C product pages returned HTTP 403.",
}

# ---- 14. Plants (S, undated) and the 2020 plan (S) ----------------------------------------------------------
res["plant_capacity_s_undated"] = {
    "singha_beverage_bang_len_million_litres_per_year": 925,
    "text": "The Thai history page says the plant 'currently has a capacity of 925 million litres a year'.",
    "source": ("plant.boonrawd.co.th/th/history, read 20 Oct 2026; undated; footer 2016; the plant brews Leo beer; the page does not "
               "say which products the figure covers and does not mention cans"),
}
res["new_line_plan_2020"] = {
    "statement": ("Positioning, 22 September 2020: the company was still considering a new line at the existing plant or on a "
                  "new site; at least THB 1,000 million; the plan was to be finalised by the end of 2021 (end 2564). "
                  "Tentative wording."),
    "status": "PLAN (S). No source read shows the line was built or where it is.",
}
res["flavour_names_company_page"] = {
    "thai_page": "Lemon, Yuzu, Ume, Red and Pink (the Thai page prints the Pink name)",
    "english_page": ("the fifth card is headed 'Pink LEMON SODA' but its 330 ML title reads 'Red Lemon Soda'; "
                     "the Thai page is cited for Pink"),
}

# ---- 15. Slide numbers and where each comes from -------------------------------------------------------
res["slide_numbers_and_source_keys"] = {
    "THB 13.5 a can, Club Card member six-pack": "slide_ranges_per_can_thb.lemon_six_pack_member_lotuss",
    "THB 14.2 a can, non-member six-pack": "slide_ranges_per_can_thb.lemon_six_pack_nonmember_lotuss",
    "THB 13.5 to 13.8 a can, 24-can packs": "slide_ranges_per_can_thb.lemon_case_24_range",
    "THB 17.00 single can, about THB 51.5 a litre": "slide_ranges_per_can_thb.single_can_lotuss_online; single_can_per_litre_thb",
    "THB 172 six-can pack excluded (about THB 28.67 a can)": "slide_ranges_per_can_thb.excluded_six_pack_172_per_can",
    "28 million litres in 2021; about 84.85 million cans": "volume_arithmetic",
    "45 million litres target for 2022": "volume_arithmetic.cans_2022_target_million (litres from the press)",
    "THB 1,357 million, 2021 sales value or revenue (press)": "volume_arithmetic.value_check_difference_pct_vs_printed_1357",
    "THB 2,200 million, 2022 revenue target (press)": "volume_arithmetic.press_2022_revenue_target_thb_m_marketeer_275740",
    "THB 13,172 million canned market, 21% of THB 62,725 million": "canned_market_year_check",
    "15,945 stores, CP ALL, end 2025 (P)": "retail_reach_p.seven_eleven_stores_end_2025",
    "3,880 million cans capacity; 59.46% used (P, all sizes)": "can_maker_bjc_2025",
    "925 million litres, Singha Beverage plant (S, undated)": "plant_capacity_s_undated",
    "52% canned share, press (COMPANY CLAIM as reported)": "share_claims_company.canned_format_share_pct_sep2023",
    "THB 6,930 million sugar-free CSD market, press 2023": "share_claims_company.sugar_free_csd_market_thb_m_marketeer_2023",
    "4% last quarter of 2020 (company claim)": "share_claims_company.q4_2020_share_pct",
}

# ---- 16. Self-checks ------------------------------------------------------------------------------------
checks = {
    "six_pack_range_lotuss_low_round": round(six_member, 2) == 13.5,
    "six_pack_range_lotuss_high_round": round(six_nonmember, 2) == 14.17,
    "makro_78_reading_would_fall_below_lotuss_member_floor": six_makro_if_78 < six_member,
    "case_24_range_low_round": round(case_makro, 2) == 13.54,
    "case_24_range_high_round": round(case_711, 2) == 13.75,
    "volume_2021_cans_million_round": round(cans_2021 / 1e6, 1) == 84.8,
    "volume_value_check_within_0_1_pct": abs(diff_pct) < 0.1,
    "press_2021_revenue_1357_equals_printed_sales_value": revenue_2021_marketeer_thb_m == sales_value_printed_thb_m,
    "tbc_usage_matches_printed_2025": round(tbc_act["2025"] / tbc_cap["2025"] * 100, 2) == 59.46,
    "canned_year_check_within_1_million": abs(csd_2021_thb_m * canned_share - canned_value_printed) < 1.0,
    "share_12pct_mismatch_detected": abs(pos_12 - 1450) > 100,
    "makro_unit_24_matches": res["makro_unit_price_checks"]["lemon_24_printed_unit_13_54"]["matches"],
    "makro_unit_6_82_over_6_matches": res["makro_unit_price_checks"]["lemon_6_printed_unit_13_67_equals_82_over_6"]["matches"],
    "makro_discount_floor_matches_first_four_pairs": all(p["printed_pct"] == p["computed_floor_pct"] for p in discount_pairs[:4]),
    "makro_discount_82_against_82_does_not_match": discount_pairs[4]["printed_pct"] != discount_pairs[4]["computed_floor_pct"],
    "big_c_total_is_sum_of_printed_components": sum(bigc.values()) == 1696,
    "singha_net_margin_2024_2025_about_79_printed_ratio": (
        abs(3135.0 / 3950.0 * 100 - 79) < 0.5 and abs(3085.0 / 3892.0 * 100 - 79) < 0.5),
    "metal_cost_flagged_not_reproduced_and_not_used": (
        res["metal_cost_per_can_thb"]["reproduced_20_oct_2026"] is False
        and res["metal_cost_per_can_thb"]["used_on_slide"] is False),
    "volume_2022_target_implied_revenue_per_can_near_16": 16.0 < res["volume_arithmetic"]["implied_revenue_per_can_at_2022_target_thb"] < 16.5,
}
res["self_checks"] = checks
res["self_checks_all_pass"] = all(checks.values())

OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print("written", OUT)
print("self checks all pass:", res["self_checks_all_pass"])
print("failed checks:", [k for k, v in checks.items() if not v])
print("slide ranges:", res["slide_ranges_per_can_thb"]["lemon_six_pack_range_lotuss_only"],
      res["slide_ranges_per_can_thb"]["lemon_case_24_range"])
print("metal per can (THB, NOT USED):", res["metal_cost_per_can_thb"]["metal_low_thb_per_can"],
      res["metal_cost_per_can_thb"]["metal_high_thb_per_can"])
