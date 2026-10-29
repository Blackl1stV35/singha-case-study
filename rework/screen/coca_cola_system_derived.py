"""T2 derived figures for rework/68a_coca_cola_system.md.
Inputs are copied from the saved raw pages in rework/raw/diligence_2026-10-20/T2/.
Pure arithmetic, no random numbers (no seed needed). Run: python -I coca_cola_system_derived.py
"""
import json, os

out = {}

# ---- Price per 330 mL and per litre (retail, THB) ----
# (label, price, units_in_pack, ml_per_unit)
prices = [
    ("Schweppes Lime Soda Zero Sugar 330 mL, 6 cans, Makro PRO 20 Oct 2026", 84.0, 6, 330),
    ("Coke No Sugar 330 mL x 12, Makro PRO 20 Oct 2026 (unit 8.50)", 102.0, 12, 330),
    ("Sprite Original 325 mL x 24, Lazada, read 20 Oct 2026", 365.0, 24, 325),
    ("Sprite No Sugar 325 mL x 24, Lazada, read 20 Oct 2026", 365.0, 24, 325),
    ("Fanta Orange 325 mL pack 5+1 (6 cans), Lazada, read 20 Oct 2026", 85.0, 6, 325),
    ("Fanta Pineapple 6 x 325 mL, Lazada, read 20 Oct 2026", 85.0, 6, 325),
    ("7UP NS Strawberry Lemon 6 x 325 mL, Lazada, read 20 Oct 2026 (context)", 75.0, 6, 325),
    ("Sprite Zero Sugar 325 mL can, Tops, 18 Oct 2026 browser read (lead)", 16.0, 1, 325),
    ("Sprite Lemon Plus 325 mL can, Thaiger 29 Aug 2022 (dated)", 15.0, 1, 325),
    ("Sprite sugar-free 325 mL can, release of 1 Apr 2019 (dated)", 14.0, 1, 325),
    ("Fanta Strawberry 1.5 L single, Lazada, read 20 Oct 2026", 32.0, 1, 1500),
    # Two rows taken from record 68d (rework/68d_lemon_soda_price_ladder.md, read 20 Oct 2026), not opened again here
    ("Sprite No Sugar 325 mL x 24, Coca-Cola Official Store on LazMall via Priceza, record 68d row Z2 (aggregator, retailer page not opened)", 334.0, 24, 325),
    ("Sprite single can 325 mL, Lotus's Shop Online, record 68d row L1", 16.0, 1, 325),
]
rows = []
for label, price, n, ml in prices:
    per_unit = price / n
    per_330 = per_unit * 330.0 / ml
    per_litre = per_unit * 1000.0 / ml
    rows.append({"item": label, "pack_price_thb": price, "units": n, "ml_per_unit": ml,
                 "price_per_unit_thb": round(per_unit, 2),
                 "price_per_330ml_thb": round(per_330, 2),
                 "price_per_litre_thb": round(per_litre, 1)})
out["price_per_330ml"] = rows

# ---- TNCC (ThaiNamthip Corporation PCL), THB million, from the SEC filing (V1 and V2) ----
tncc = {
    "FY2022": {"sales_of_goods": 35632.60, "total_revenue": 35989.15, "cost_of_sales": 22014.78, "gross_profit": 13617.82, "net_profit": 3083.24},
    "FY2023": {"sales_of_goods": 38876.25, "total_revenue": 39294.98, "cost_of_sales": 23871.82, "gross_profit": 15004.43, "net_profit": 3374.41},
    "FY2024": {"sales_of_goods": 39828.47, "total_revenue": 41314.24, "cost_of_sales": 24496.45, "gross_profit": 15332.02, "net_profit": 4379.08},
    "6M2024": {"sales_of_goods": 21291.92, "total_revenue": 21528.72, "cost_of_sales": 13016.37, "gross_profit": 8275.56, "net_profit": 2069.93},
    "6M2025": {"sales_of_goods": 17863.60, "total_revenue": 18330.18, "cost_of_sales": 10869.48, "gross_profit": 6994.12, "net_profit": 958.51},
}
t = {}
for k, v in tncc.items():
    t[k] = {
        "gross_margin_on_sales_of_goods_pct": round(100 * v["gross_profit"] / v["sales_of_goods"], 2),
        "net_margin_on_total_revenue_pct": round(100 * v["net_profit"] / v["total_revenue"], 2),
        "check_sales_minus_cost_equals_gross_profit": round(v["sales_of_goods"] - v["cost_of_sales"] - v["gross_profit"], 2),
    }
t["total_revenue_growth_pct"] = {
    "FY2023_vs_FY2022": round(100 * (tncc["FY2023"]["total_revenue"] / tncc["FY2022"]["total_revenue"] - 1), 1),
    "FY2024_vs_FY2023": round(100 * (tncc["FY2024"]["total_revenue"] / tncc["FY2023"]["total_revenue"] - 1), 1),
    "6M2025_vs_6M2024": round(100 * (tncc["6M2025"]["total_revenue"] / tncc["6M2024"]["total_revenue"] - 1), 1),
    "net_profit_6M2025_vs_6M2024": round(100 * (tncc["6M2025"]["net_profit"] / tncc["6M2024"]["net_profit"] - 1), 1),
}
# channel mix FY2024 (filing V1, MD&A): modern 19917.5, traditional 19136.8, LCCB and export 774.1; sales of goods 39828.47
ch = {"modern_trade": 19917.5, "traditional_trade": 19136.8, "laos_and_export": 774.1}
tot = sum(ch.values())
t["channel_mix_FY2024_pct_of_sales_of_goods"] = {k: round(100 * v / 39828.47, 1) for k, v in ch.items()}
t["channel_sum_check"] = round(tot, 1)
# capacity utilisation 2024 (unit cases): sold 404 (V1) or 400 (V2) against maximum capacity 564
t["capacity_utilisation_2024_pct"] = {"V1_404m": round(100 * 404 / 564, 1), "V2_400m": round(100 * 400 / 564, 1)}
# volume change 6M2025 vs 6M2024 (V2): 181 vs 216 million unit cases
t["volume_6M2025_vs_6M2024_pct"] = round(100 * (181 / 216 - 1), 1)
# revenue mix FY2024 (V1 table): cola 24060.03 / total revenue 41314.24
t["cola_share_of_total_revenue_FY2024_pct"] = round(100 * 24060.03 / 41314.24, 1)
# capacity utilisation on the older capacity figure (450 million unit cases a year, Swire release of 9 Feb 2024 and marketingoops 21 Sep 2024)
t["capacity_utilisation_2024_on_450m_pct"] = {"V1_404m": round(100 * 404 / 450, 1), "V2_400m": round(100 * 400 / 450, 1)}
# revenue mix, 6M2025 against 6M2024 (V2 PDF page 10 table and page 23 text), THB million
t["six_month_2025_vs_2024_pct"] = {
    "cola_10872.74_vs_12745.80": round(100 * (10872.74 / 12745.80 - 1), 1),
    "other_carbonated_5080.19_vs_6365.02": round(100 * (5080.19 / 6365.02 - 1), 1),
}
# plausibility bracket for the 51.4% share (Frost and Sullivan, as quoted in the filing; attributed by the filing to the company)
# ThaiNamthip carbonated revenue FY2024 = cola 24060.03 + other carbonated 11609.18 (THB million)
carb = 24060.03 + 11609.18
t["carbonated_revenue_FY2024_thb_m"] = round(carb, 2)
t["implied_market_if_51_4pct_thb_bn"] = round(carb / 0.514 / 1000, 1)
t["carbonated_revenue_as_pct_of_press_market_sizes"] = {
    "of_66_bn_thansettakij_2024": round(100 * carb / 66000, 1),
    "of_76_9_bn_marketeer_2026": round(100 * carb / 76900, 1),
}
out["tncc"] = t

# ---- Haad Thip (company statements) ----
htc = {
    "FY2023": {"total_revenue": 7863.97, "net_profit": 598.56},
    "FY2024": {"total_revenue": 8189.09, "net_profit": 601.68},
    "FY2025": {"sales_revenue": 8258.4, "net_profit": 568.3, "gross_margin_pct": 42.2},
}
h = {}
h["FY2023_net_margin_on_total_revenue_pct"] = round(100 * 598.56 / 7863.97, 2)
h["FY2024_net_margin_on_total_revenue_pct"] = round(100 * 601.68 / 8189.09, 2)
h["FY2025_net_margin_on_sales_pct"] = round(100 * 568.3 / 8258.4, 2)
h["FY2024_gross_margin_derived_pct"] = round(42.2 + 0.5, 1)  # FY2025 release: 42.2%, "down 0.5 point"
h["net_profit_FY2025_vs_FY2024_pct"] = round(100 * (568.3 / 601.68 - 1), 1)
h["revenue_FY2024_vs_FY2023_pct"] = round(100 * (8189.09 / 7863.97 - 1), 1)
# Basis check for FY2025 (verification fix). The company release says revenue from sales 8,258.4, up 1.6%.
# Thairath's FY2024 figure of 8,189.09 is total revenue. Marketeer prints 8,368 for 2025.
h["fy2025_8258_4_vs_fy2024_total_revenue_8189_09_pct"] = round(100 * (8258.4 / 8189.09 - 1), 1)
h["fy2025_8368_vs_fy2024_total_revenue_8189_09_pct"] = round(100 * (8368.0 / 8189.09 - 1), 1)
h["fy2024_comparator_implied_by_release_growth_1_6pct"] = round(8258.4 / 1.016, 1)
h["fy2025_net_margin_on_8368_pct"] = round(100 * 568.3 / 8368.0, 2)
h["difference_8368_minus_8258_4"] = round(8368.0 - 8258.4, 1)
out["haad_thip"] = h

# ---- The Coca-Cola Company group, USD million ----
ko = {
    "FY2023": {"revenue": 45754, "gross_profit": 27234, "net_income_attrib": 10714},
    "FY2024": {"revenue": 47061, "gross_profit": 28737, "net_income_attrib": 10631},
    "FY2025": {"revenue": 47941, "gross_profit": 29544, "net_income_attrib": 13107},
}
k = {}
for y, v in ko.items():
    k[y] = {"gross_margin_pct": round(100 * v["gross_profit"] / v["revenue"], 1),
            "net_margin_pct": round(100 * v["net_income_attrib"] / v["revenue"], 1)}
out["coca_cola_company_group"] = k

# ---- Pairs for the brand-owner versus bottler note ----
out["gross_margin_gap_pct_points_FY2024"] = round(100 * 28737 / 47061 - 100 * 15332.02 / 39828.47, 1)

# ---- Cube price parity (base-case cube price THB 15 from proposal 11 and the deck) ----
out["cube_base_case_price_thb"] = 15.0
# SUPERSEDED (20 October 2026, revision 3): the three fields below use two Sprite No Sugar 24-pack listings only.
# They are kept under SUPERSEDED_ names so that the earlier run can be reproduced. Cite
# rework/screen/t2_coca_cola_system_check_results.json instead (four listings, range THB 14.13 to 19.29).
out["SUPERSEDED_note"] = ("Fields prefixed SUPERSEDED_ use two Sprite No Sugar 24-pack listings (Lazada THB 365 and one "
    "other row). They are superseded by t2_coca_cola_system_check_results.json, which uses four listings. Do not cite them.")
out["SUPERSEDED_cube_vs_sprite_no_sugar_325_pack24_per_330"] = round(15.0 - rows[3]["price_per_330ml_thb"], 2)
# Parity is a range, not a point: two 24-pack listings and one single-can listing
no_sugar_pack24 = [rows[3]["price_per_330ml_thb"], rows[11]["price_per_330ml_thb"]]
single_can = rows[12]["price_per_330ml_thb"]
out["SUPERSEDED_sprite_no_sugar_pack24_per_330_range_thb"] = [min(no_sugar_pack24), max(no_sugar_pack24)]
out["SUPERSEDED_cube_vs_pack24_low_and_high_thb"] = [round(15.0 - min(no_sugar_pack24), 2), round(15.0 - max(no_sugar_pack24), 2)]
out["sprite_single_can_per_330_thb"] = single_can
out["cube_vs_single_can_thb"] = round(15.0 - single_can, 2)

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "coca_cola_system_derived_results.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("wrote coca_cola_system_derived_results.json")
