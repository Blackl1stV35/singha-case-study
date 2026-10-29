"""Retail price ladder for lemon, lime and clear carbonated soft drinks and soda waters
in 325 to 345 mL cans (Thailand), read 20 October 2026. Task T5.

Inputs are the listing rows saved under rework/raw/diligence_2026-10-20/T5/. Every row carries
its source file. No random numbers are used, so there is no seed. The script writes
rework/screen/lemon_soda_price_ladder_results.json and prints a short summary.
Memory use is a few MB.
"""
import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "lemon_soda_price_ladder_results.json")
DATE = "2026-10-20"
SERVE_ML = 330
CUBE_SHELF_THB = 15.0          # planning shelf price per cube (ASSUMPTION in the proposal)
CUBE_CARTON_COUNT = 6          # recommended carton in the proposal

R7 = "7eleven_allonline_2026-10-20.md"
MK = "makro_pro_2026-10-20.md"
LT = "lotuss_2026-10-20.md"
PZ = "priceza_aggregator_2026-10-20.md"
SG = "singha_lemon_soda_brand_page_P.md"

SG_FREE = "sugar-free (maker page: zero sugar, zero calories; sucralose and acesulfame potassium)"

# id, retailer, channel (direct page opened | aggregator row), product, group, container,
# can_ml, pack_count, pack_price, sugar_status, url, raw_file, note, flags
ROWS = [
    # ---- 7-Eleven ALL Online (direct) ----
    ("E1", "7-Eleven ALL Online", "direct", "Singha Lemon Soda", "lemon_lime", "can", 330, 24, 330, SG_FREE,
     "https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-ยกลัง-24-กระป๋อง/474313/", R7, "struck-through 408", {"stock_label": True}),
    ("E2", "7-Eleven ALL Online", "direct", "Singha Lemon Soda", "lemon_lime", "can", 330, 6, 172, SG_FREE,
     "https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-แพ็ก-6-กระป๋อง/514221/", R7, "struck-through 182", {"stock_label": True}),
    ("E3", "7-Eleven ALL Online", "direct", "Schweppes Lime Soda Zero", "lemon_lime", "can", 330, 6, 170, "sugar-free (page: สูตรไม่มีน้ำตาล)",
     "https://www.allonline.7eleven.co.th/p/ชเวปส์มะนาวโซดาซีโร่-330มล-แพ็ก-6-กระป๋อง/354988/", R7, "struck-through 190; promotion ends 20 Oct 2026", {"stock_label": True}),
    ("E4", "7-Eleven ALL Online", "direct", "Nestle Pure Life Soda Plus Lemon Lime", "lemon_lime", "can", 330, 24, 377, "not stated",
     "https://www.allonline.7eleven.co.th/p/เนสท์เล่-เพียวไลฟ์-โซดาพลัส-เลมอนไลม์-330-มลถาด-24-กระป๋อง/327940/", R7, "search row; label: sorry, out of stock", {"unavailable": True}),
    ("E5", "7-Eleven ALL Online", "direct", "Singha Sparkling Water Lime", "lemon_lime", "can", 330, 24, 302,
     "not confirmed by this read (page: 0% calories; no sugar line)",
     "https://www.allonline.7eleven.co.th/p/สิงห์สปาร์คกลิ้งไลม์-330-มล-ยกลัง-24-กระป๋อง/327253/", R7, "304 shown beside the price; -1%; in stock label", {"stock_label": True}),
    # ---- Makro PRO (direct) ----
    ("M1", "Makro PRO", "direct", "Sprite Lemon Lime", "lemon_lime", "can", 325, 24, 311, "regular variant; sugar not stated on page",
     "https://www.makro.pro/en/p/179712-7078659719363", MK, "list 321", {}),
    ("M2", "Makro PRO", "direct", "Sprite Lemon Lime", "lemon_lime", "can", 330, 12, 137, "regular variant; sugar not stated on page",
     "https://www.makro.pro/en/p/830198-7078660866243", MK, "Buy 3+ units tier 135", {}),
    ("M3", "Makro PRO", "direct", "Sprite Chill Lemon Mint", "lemon_lime", "can", 325, 6, 78, "not stated on page",
     "https://www.makro.pro/en/p/630907-363090727914101", MK, "list 81", {}),
    ("M4", "Makro PRO", "direct", "Singha Lemon Soda", "lemon_lime", "can", 330, 6, 82, SG_FREE,
     "https://www.makro.pro/en/p/893947-6814746706115", MK, "Buy 3+ units tier 78", {}),
    ("M5", "Makro PRO", "direct", "Singha Lemon Soda", "lemon_lime", "can", 330, 24, 325, SG_FREE,
     "https://www.makro.pro/en/p/428706-7350275997891", MK, "list 330", {}),
    ("M7", "Makro PRO", "direct", "Schweppes Soda Water", "soda_water", "can", 330, 24, 341, "plain soda water; no sugar claim on page",
     "https://www.makro.pro/en/p/119581-7416114282691", MK, "Buy 2+ units tier 336", {}),
    ("M8", "Makro PRO", "direct", "Schweppes Lime Soda", "lemon_lime", "can", 330, 6, 84, "regular; page nutrition panel shows carbohydrates 16 g (basis not stated)",
     "https://www.makro.pro/en/p/vwmvjuh-6814746476739", MK, "Buy 2+ units tier 83", {}),
    ("M9", "Makro PRO", "direct", "Schweppes Lime Soda Zero Sugar", "lemon_lime", "can", 330, 6, 84, "sugar-free (name)",
     "https://www.makro.pro/en/p/899900-7499701616835", MK, "page: unavailable in the area selected", {"unavailable": True}),
    ("M10", "Makro PRO", "direct", "Singha Sparkling Water Lime", "lemon_lime", "can", 330, 24, 312,
     "not confirmed by this read (no sugar text on page extract)",
     "https://www.makro.pro/en/p/699716183874140", MK, "list 319; -2%", {}),
    # ---- Lotus's Shop Online (direct) ----
    ("L1", "Lotus's Shop Online", "direct", "Sprite (single can)", "lemon_lime", "can", 325, 1, 16, "regular variant; sugar not stated on page",
     "https://shopping.lotuss.com/th/product/sprite-lemonlime-flavour-soft-drink-325ml-238945", LT, "", {}),
    ("L2", "Lotus's Shop Online", "direct", "Sprite", "lemon_lime", "can", 325, 6, 85, "regular variant; sugar not stated on page",
     "https://www.lotuss.com/en/product/sprite-lemonlime-flavour-soft-drink-325ml-x-6pcs-6808557", LT, "promotion: buy 2 for 156", {}),
    ("L3", "Lotus's Shop Online", "direct", "Sprite", "lemon_lime", "can", 325, 24, 332, "regular variant; sugar not stated on page",
     "https://www.lotuss.com/en/product/sprite-soft-drink-original-325ml-x-24pcs-clubpack-150033088", LT, "member price 315", {}),
    ("L4", "Lotus's Shop Online", "direct", "Sprite Chill Lemon Mint (single can)", "lemon_lime", "can", 325, 1, 17, "not stated on page",
     "https://www.lotuss.com/en/product/75714334", LT, "", {}),
    ("L5", "Lotus's Shop Online", "direct", "7UP Zero Sugar Lemon Soda", "lemon_lime", "can", 325, 6, 75, "sugar-free (name: ZERO SUGAR)",
     "https://www.lotuss.com/en/product/171266560", LT, "list 80", {}),
    ("L7", "Lotus's Shop Online", "direct", "Singha Lemon Soda (single can)", "lemon_lime", "can", 330, 1, 17, SG_FREE,
     "https://www.lotuss.com/en/product/singha-lemon-soda-zero-sugar-lemon-soda-330ml-50986847", LT, "", {}),
    ("L8", "Lotus's Shop Online", "direct", "Singha Lemon Soda", "lemon_lime", "can", 330, 6, 85, SG_FREE,
     "https://www.lotuss.com/en/product/singha-lemon-soda-can-330ml-6-51109221", LT, "member price 81", {}),
    ("L9", "Lotus's Shop Online", "direct", "Singha Lemon Soda", "lemon_lime", "can", 330, 24, 330, SG_FREE,
     "https://www.lotuss.com/en/product/169912032", LT, "", {}),
    ("L10", "Lotus's Shop Online", "direct", "Schweppes Manao (Lime) Soda (single can)", "lemon_lime", "can", 330, 1, 18, "regular lime soda; sugar not stated on page",
     "https://shopping.lotuss.com/en/product/schweppes-soft-drink-lime-soda-330ml-single-6709516", LT, "", {}),
    ("L11", "Lotus's Shop Online", "direct", "Schweppes Soda Water", "soda_water", "can", 330, 6, 88, "plain soda water; no sugar claim on page",
     "https://www.lotuss.com/en/product/schweppes-sparkling-soda-water-330ml-x-6-cans-75162024", LT, "", {}),
    # ---- Aggregator layer (Priceza reading Tops Online and Lazada official stores; retailer page not opened) ----
    ("Z1", "Tops Online (via Priceza)", "aggregator", "Sprite", "lemon_lime", "can", 325, 24, 332, "regular variant; sugar not stated",
     "https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813", PZ, "S aggregator row; Tops blocks direct reading", {}),
    ("Z2", "Coca-Cola Official Store, LazMall (via Priceza)", "aggregator", "Sprite No Sugar", "lemon_lime", "can", 325, 24, 334, "sugar-free (name: สูตรไม่มีน้ำตาล)",
     "https://www.priceza.com/b/groceries/น้ำอัดลม/sprite", PZ, "was 384", {}),
    ("Z4", "Coca-Cola Official Store, LazMall (via Priceza)", "aggregator", "Sprite Original", "lemon_lime", "can", 325, 6, 96, "regular variant; sugar not stated",
     "https://www.priceza.com/b/groceries/น้ำอัดลม/sprite", PZ, "", {}),
    ("Z5", "Suntory PepsiCo official store, LazMall (via Priceza)", "aggregator", "7UP Lemon Soda No Sugar", "lemon_lime", "can", 325, 24, 293, "sugar-free (name: ไม่มีน้ำตาล)",
     "https://www.priceza.com/s/ราคา/เซเว่นอัพ", PZ, "was 384", {}),
    ("Z6", "Suntory PepsiCo official store, LazMall (via Priceza)", "aggregator", "7UP Lemon Soda No Sugar", "lemon_lime", "can", 325, 12, 161, "sugar-free (name: ไม่มีน้ำตาล)",
     "https://www.priceza.com/s/ราคา/เซเว่นอัพ", PZ, "was 192", {}),
    ("Z7", "Suntory PepsiCo official store, LazMall (via Priceza)", "aggregator", "7UP Lemon Soda No Sugar", "lemon_lime", "can", 325, 6, 96, "sugar-free (name: ไม่มีน้ำตาล)",
     "https://www.priceza.com/s/ราคา/เซเว่นอัพ", PZ, "", {}),
    ("Z8", "Coca-Cola Official Store, LazMall (via Priceza)", "aggregator", "Schweppes Lime Soda Zero", "lemon_lime", "can", 330, 24, 351, "sugar-free (name: สูตรไม่มีน้ำตาล)",
     "https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", PZ, "404 inferred as was-price; delivery limited to Bangkok metro and Chonburi", {}),
    ("Z9", "Coca-Cola Official Store, LazMall (via Priceza)", "aggregator", "Schweppes Lime Soda Zero", "lemon_lime", "can", 330, 12, 196, "sugar-free (name: สูตรไม่มีน้ำตาล)",
     "https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", PZ, "", {}),
    ("Z10", "Lotus's Shop Online (via Priceza)", "aggregator", "7UP Zero Sugar Lemon Soda (single can)", "lemon_lime", "can", 325, 1, 16, "sugar-free (name: ไม่มีน้ำตาล)",
     "https://www.priceza.com/s/ราคา/เซเว่นอัพ", PZ, "single-can price; the pre-production Lotus's page shows the same 16 and is not used as source", {}),
]

# Soda water in bottles (shown for completeness; not part of the can ladder)
BOTTLE_ROWS = [
    ("B1", "7-Eleven ALL Online", "Singha Soda (soda water)", 325, 24, 195,
     "https://www.allonline.7eleven.co.th/p/โซดาสิงห์-325-มล-แพ็ก-24-ขวด/452565/", R7, "bottle; the 6-bottle listing at 157 is shown as an outlier"),
    ("B2", "7-Eleven ALL Online", "Singha Soda small bottle (soda water)", 325, 6, 157,
     "https://www.allonline.7eleven.co.th/p/สิงห์-โซดาขวดเล็ก-325-มล-แพ็ก-6-ขวด/452376/", R7, "outlier against B1, B3 and B4; reason not on page"),
    ("B3", "Makro PRO", "Singha Soda (soda water)", 325, 24, 190,
     "https://www.makro.pro/en/p/160629-6761215066307", MK, "bottle"),
    ("B4", "Lotus's Shop Online", "Singha Soda (soda water)", 325, 6, 48,
     "https://www.lotuss.com/en/product/singha-soda-325-ml-6-24183741", LT, "packaging type not stated on the page"),
]


def derive(r):
    (rid, retailer, channel, product, group, container, can_ml, n, price, sugar, url, raw, note, flags) = r
    per_can = price / n
    return {
        "id": rid, "retailer": retailer, "channel": channel, "product": product, "group": group,
        "container": container, "can_ml": can_ml, "pack_count": n, "pack_price_thb": price,
        "per_can_thb": round(per_can, 2),
        "per_330ml_thb": round(per_can * SERVE_ML / can_ml, 2),
        "per_litre_thb": round(per_can / (can_ml / 1000.0), 1),
        "sugar_status": sugar, "date_read": DATE, "url": url, "raw_file": raw, "note": note,
        "unavailable": bool(flags.get("unavailable", False)),
        "stock_wording": ("in stock (page label)" if flags.get("stock_label")
                          else "flagged unavailable on page" if flags.get("unavailable")
                          else "none on page"),
        "single_can": n == 1,
    }


def stats(vals):
    vals = sorted(vals)
    if not vals:
        return None
    return {"n": len(vals), "min": round(vals[0], 2), "median": round(statistics.median(vals), 2),
            "max": round(vals[-1], 2)}


def ladder(rows, key):
    return stats([r[key] for r in rows])


def position(rows, key, x):
    vals = [r[key] for r in rows]
    n = len(vals)
    return {
        "x": x, "n": n,
        "rows_below": sum(v < x for v in vals),
        "rows_equal": sum(abs(v - x) < 0.005 for v in vals),
        "rows_above": sum(v > x for v in vals),
        "share_at_or_below": round(sum(v <= x + 1e-9 for v in vals) / n, 3),
    }


def main():
    rows = [derive(r) for r in ROWS]
    usable = [r for r in rows if not r["unavailable"] and r["container"] == "can"]
    direct = [r for r in usable if r["channel"] == "direct"]
    lemon_lime = [r for r in usable if r["group"] == "lemon_lime"]
    direct_ll = [r for r in direct if r["group"] == "lemon_lime"]

    def sub(rs, **kw):
        out = rs
        if "single" in kw:
            out = [r for r in out if r["single_can"] == kw["single"]]
        if "brand" in kw:
            out = [r for r in out if kw["brand"] in r["product"]]
        if "sugarfree" in kw:
            out = [r for r in out if r["sugar_status"].startswith("sugar-free") == kw["sugarfree"]]
        return out

    sets = {
        "direct_all_cans": direct,
        "direct_lemon_lime_cans": direct_ll,
        "direct_plus_aggregator_lemon_lime_cans": lemon_lime,
        "direct_single_cans": sub(direct, single=True),
        "direct_multipack_cans": sub(direct, single=False),
        "all_single_cans_incl_aggregator": sub(usable, single=True),
        "all_multipack_cans_incl_aggregator": sub(usable, single=False),
        "singha_lemon_soda_direct": sub(direct, brand="Singha Lemon"),
        "singha_lemon_soda_direct_single": sub(sub(direct, brand="Singha Lemon"), single=True),
        "singha_lemon_soda_direct_multipack": sub(sub(direct, brand="Singha Lemon"), single=False),
        "sugar_free_lemon_lime_direct": sub(direct_ll, sugarfree=True),
        "other_lemon_lime_direct_not_confirmed_sugar_free": sub(direct_ll, sugarfree=False),
        "soda_water_cans_direct": [r for r in direct if r["group"] == "soda_water"],
        # Singha rows (Lemon Soda in several packs and shops, and Sparkling Water Lime) are not independent of each other
        "singha_brand_direct": [r for r in direct if r["product"].startswith("Singha")],
        "singha_sparkling_water_lime_direct": [r for r in direct if "Sparkling" in r["product"]],
        "direct_cans_not_singha_brand": [r for r in direct if not r["product"].startswith("Singha")],
        "direct_cans_not_singha_brand_excluding_7eleven_6can": [
            r for r in direct if not r["product"].startswith("Singha")
            and not (r["retailer"].startswith("7-Eleven") and r["pack_count"] == 6)],
        # the two 7-Eleven 6-can rows read about twice the other retailers' 6-can rows
        "sensitivity_direct_cans_excluding_7eleven_6can_rows": [
            r for r in direct if not (r["retailer"].startswith("7-Eleven") and r["pack_count"] == 6)],
        "retailer_7eleven_direct": [r for r in direct if r["retailer"].startswith("7-Eleven")],
        "retailer_makro_direct": [r for r in direct if r["retailer"].startswith("Makro")],
        "retailer_lotuss_direct": [r for r in direct if r["retailer"].startswith("Lotus")],
    }
    ladders = {}
    for name, rs in sets.items():
        ladders[name] = {
            "per_can_thb": ladder(rs, "per_can_thb"),
            "per_330ml_thb": ladder(rs, "per_330ml_thb"),
            "per_litre_thb": ladder(rs, "per_litre_thb"),
            "row_ids": [r["id"] for r in rs],
        }

    # Sensitivity: add the two rows flagged unavailable
    flagged = [r for r in rows if r["unavailable"]]
    sens_all = [r for r in rows if r["container"] == "can" and r["channel"] == "direct"]
    ladders["sensitivity_direct_cans_including_unavailable_rows"] = {
        "per_can_thb": ladder(sens_all, "per_can_thb"),
        "per_330ml_thb": ladder(sens_all, "per_330ml_thb"),
        "per_litre_thb": ladder(sens_all, "per_litre_thb"),
        "row_ids": [r["id"] for r in sens_all],
    }

    # Sensitivity: Makro M2 (Sprite 330 mL x 12, the ladder minimum) at THB 135, the page's "Buy 3+ units" figure,
    # in case the 135 on the page is the one-pack price instead of the tier price (two page reads disagree).
    m2_alt = []
    for r in direct:
        if r["id"] == "M2":
            r = dict(r)
            r["pack_price_thb"] = 135
            r["per_can_thb"] = round(135 / r["pack_count"], 2)
            r["per_330ml_thb"] = round(135 / r["pack_count"] * SERVE_ML / r["can_ml"], 2)
            r["per_litre_thb"] = round(135 / r["pack_count"] / (r["can_ml"] / 1000.0), 1)
        m2_alt.append(r)
    ladders["sensitivity_direct_cans_with_makro_M2_at_135"] = {
        "per_can_thb": ladder(m2_alt, "per_can_thb"),
        "per_330ml_thb": ladder(m2_alt, "per_330ml_thb"),
        "per_litre_thb": ladder(m2_alt, "per_litre_thb"),
        "row_ids": [r["id"] for r in m2_alt],
    }

    # Row composition and stock wording (rows are not independent; stock wording is on 7-Eleven pages only)
    composition = {
        "direct_rows": len(direct),
        "singha_lemon_soda_rows": len(sets["singha_lemon_soda_direct"]),
        "singha_sparkling_water_lime_rows": len(sets["singha_sparkling_water_lime_direct"]),
        "singha_brand_rows": len(sets["singha_brand_direct"]),
        "not_singha_brand_rows": len(sets["direct_cans_not_singha_brand"]),
        "rows_with_in_stock_label_on_page": [r["id"] for r in direct if r["stock_wording"].startswith("in stock")],
        "rows_with_no_stock_wording_on_page": [r["id"] for r in direct if r["stock_wording"] == "none on page"],
        "rows_flagged_unavailable_and_excluded": [r["id"] for r in rows if r["unavailable"]],
    }

    # Where THB 15 sits
    pos = {}
    for name in ["direct_all_cans", "direct_lemon_lime_cans", "direct_single_cans",
                 "direct_multipack_cans", "direct_plus_aggregator_lemon_lime_cans",
                 "all_single_cans_incl_aggregator", "all_multipack_cans_incl_aggregator",
                 "singha_lemon_soda_direct", "sensitivity_direct_cans_excluding_7eleven_6can_rows",
                 "retailer_7eleven_direct", "retailer_makro_direct", "retailer_lotuss_direct",
                 "direct_cans_not_singha_brand",
                 "direct_cans_not_singha_brand_excluding_7eleven_6can",
                 "singha_brand_direct", "singha_sparkling_water_lime_direct"]:
        pos[name] = position(sets[name], "per_330ml_thb", CUBE_SHELF_THB)

    # Per serve: cube against can
    def cmp(label, can_val):
        return {"label": label, "can_per_330ml_thb": round(can_val, 2),
                "cube_minus_can_thb": round(CUBE_SHELF_THB - can_val, 2),
                "cube_vs_can_pct": round((CUBE_SHELF_THB / can_val - 1) * 100, 1)}

    comp = []
    sl_single = sets["singha_lemon_soda_direct_single"]
    for r in sl_single:
        comp.append(cmp("Singha Lemon Soda single can, " + r["retailer"], r["per_330ml_thb"]))
    for r in sets["singha_lemon_soda_direct_multipack"]:
        comp.append(cmp("Singha Lemon Soda %d-can pack, %s" % (r["pack_count"], r["retailer"]), r["per_330ml_thb"]))
    for r in sets["singha_sparkling_water_lime_direct"]:
        comp.append(cmp("Singha Sparkling Water Lime %d-can pack, %s" % (r["pack_count"], r["retailer"]), r["per_330ml_thb"]))
    comp.append(cmp("Direct lemon-lime cans, median of single cans",
                    ladders["direct_single_cans"]["per_330ml_thb"]["median"]))
    comp.append(cmp("Direct cans, median of multipacks",
                    ladders["direct_multipack_cans"]["per_330ml_thb"]["median"]))
    comp.append(cmp("Direct cans, median of all rows",
                    ladders["direct_all_cans"]["per_330ml_thb"]["median"]))

    carton = {
        "cube_carton_count": CUBE_CARTON_COUNT,
        "cube_carton_price_thb": CUBE_SHELF_THB * CUBE_CARTON_COUNT,
        "six_can_packs_singha_lemon_soda": [
            {"retailer": r["retailer"], "pack_price_thb": r["pack_price_thb"],
             "carton_minus_pack_thb": CUBE_SHELF_THB * CUBE_CARTON_COUNT - r["pack_price_thb"]}
            for r in sets["singha_lemon_soda_direct_multipack"] if r["pack_count"] == 6],
    }

    bottles = []
    for (bid, ret, prod, ml, n, price, url, raw, note) in BOTTLE_ROWS:
        pc = price / n
        bottles.append({"id": bid, "retailer": ret, "product": prod, "bottle_ml": ml, "pack_count": n,
                        "pack_price_thb": price, "per_bottle_thb": round(pc, 2),
                        "per_330ml_thb": round(pc * 330 / ml, 2), "per_litre_thb": round(pc / (ml / 1000), 1),
                        "date_read": DATE, "url": url, "raw_file": raw, "note": note})

    cube = {"cube_shelf_thb_per_serve": CUBE_SHELF_THB, "serve_ml": SERVE_ML,
            "cube_per_litre_thb": round(CUBE_SHELF_THB / (SERVE_ML / 1000.0), 1)}

    result = {
        "task": "T5 retail price ladder", "date_read": DATE,
        "method": "per can = pack price / pack count; per 330 mL = per can x 330 / can mL (325 mL cans scaled by 330/325); "
                  "per litre = per can / can litres; unavailable or out-of-stock rows excluded from the ladder and shown in a sensitivity set; "
                  "bottle rows excluded from the can ladder; no random numbers, no seed.",
        "cube": cube,
        "rows": rows,
        "excluded_unavailable_rows": [r["id"] for r in flagged],
        "row_composition": composition,
        "ladders": ladders,
        "position_of_cube_price_15": pos,
        "cube_vs_can_per_serve": comp,
        "carton_vs_six_can_pack": carton,
        "bottle_rows_soda_water": bottles,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    # short console summary
    print("rows:", len(rows), "usable cans:", len(usable), "direct:", len(direct))
    for k in ["direct_all_cans", "direct_lemon_lime_cans", "direct_single_cans", "direct_multipack_cans",
              "direct_plus_aggregator_lemon_lime_cans", "singha_lemon_soda_direct",
              "sensitivity_direct_cans_excluding_7eleven_6can_rows", "retailer_7eleven_direct",
              "retailer_makro_direct", "retailer_lotuss_direct", "soda_water_cans_direct",
              "sugar_free_lemon_lime_direct", "other_lemon_lime_direct_not_confirmed_sugar_free",
              "sensitivity_direct_cans_including_unavailable_rows",
              "sensitivity_direct_cans_with_makro_M2_at_135",
              "singha_brand_direct", "singha_sparkling_water_lime_direct",
              "direct_cans_not_singha_brand",
              "direct_cans_not_singha_brand_excluding_7eleven_6can"]:
        L = ladders[k]
        print(k, L["per_can_thb"], L["per_330ml_thb"], L["per_litre_thb"])
    print(json.dumps(composition))
    print(json.dumps(pos["direct_all_cans"]))
    print(json.dumps(pos["direct_cans_not_singha_brand"]))
    print(json.dumps(pos["direct_single_cans"]))
    print(json.dumps(pos["direct_multipack_cans"]))
    for c in comp:
        print(c)


if __name__ == "__main__":
    main()
