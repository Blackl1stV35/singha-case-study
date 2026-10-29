"""T5b (68e): price per serve and margin arithmetic for the dissolvable-drink analogues.

Reads nothing from the network. Every input below was read from a page saved in
rework/raw/diligence_2026-10-20/T5b/ (file named in the 'src' field) or from the canned-lemon
ladder results file. No random numbers.
Run: python rework/screen/analogue_price_per_serve_68e.py
Writes: rework/screen/analogue_price_per_serve_68e_results.json

Sixth version (20 October 2026, after the T68 verifier; record 68e to be corrected by the lead): the canned can ladder is read from
 rework/screen/t5_retail_price_ladder_results.json (68d second revision, sets A, B, D and K), not from
 lemon_soda_price_ladder_results.json. The single-can median is set D (4 rows); the multi-pack median is set B (16 retailer-page
 rows); the all-can median is set A (31 rows). The Singha Lemon Soda pack range uses set K rows D01, D06, D07, D12 and D13, with
 the 7-Eleven six-can D02 named as the outlier. The 18-row and 22-row medians of version 5 are withdrawn.

Fifth version (20 October 2026, after the third independent check; record version 5). Changes in this version:
 - Nuun tubes (US and Canadian listing) and the Thai Nuun rows: the 500 mL directions dose on the Canadian
   listing is the central dose, and the 473 mL nutrition basis is shown as the alternative (both ASSUMPTION-based);
 - the waterdrop US figures carry the UK product's 400 to 600 mL dose as an ASSUMPTION (the US page states none);
 - the Interpharma rows (L06 to L08) are UNVERIFIED for effervescent form: a sensitivity without them is printed;
 - multi-pack median sensitivities (without the two plain soda-water cans) and an overseas ratio summary;
 - sanity assertions for the quoted Thai medians and the multi-pack medians.

Third version (20 October 2026, after the second independent check):
 - medians and quartiles are computed on unrounded per-tablet and per-serve values and rounded at the end;
 - the Thai effervescent set carries a title-form flag (the listing title states the effervescent form) and
   a sensitivity on that subset; the two rows whose title carries an expiry year of 2027 are named and
   removed in a sensitivity (they are not expired on 20 October 2026);
 - the Singha Lemon Soda pack range names its five rows and the one 7-Eleven six-can outlier (THB 28.67);
 - the SodaStream floor is taken on the UK price and the UK yield ("up to 60 L", P); the Canadian price is
   shown only as a PROXY at the UK yield, because the Canadian page states no litre figure;
 - the Nestle trading-operating-profit arithmetic takes each input from the saved statements extract, and
   asserts that the computed figure equals the printed one;
 - the US Nuun tube is labelled as the Strawberry Lemonade tube on the US page read, with the 10-tablet count
   an ASSUMPTION from a Canadian Lemon + Lime listing.
"""
import json
import os
import statistics
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))


def r2(x):
    """Round half up to 2 decimals (so that an exact half such as 16.625 gives 16.63)."""
    return float(Decimal(repr(float(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------- FX
# BoT average counter rates for USD, as of 15 October 2026: mid of buying sight and selling transfer.
BOT_BUY_SIGHT = 33.3535
BOT_SELL_TRANSFER = 33.7455
THB_PER_USD = (BOT_BUY_SIGHT + BOT_SELL_TRANSFER) / 2.0  # 33.5495 (as in rework/raw/bot_fx_primary_2026-10-15.md)

# ECB euro reference rates, 19 October 2026 (units of currency per 1 EUR).
ECB = {"EUR": 1.0, "USD": 1.1225, "JPY": 177.63, "GBP": 0.84205, "CHF": 0.9261, "CAD": 1.5798}
THB_PER_EUR = THB_PER_USD * ECB["USD"]  # cross rate through USD
THB_PER = {ccy: THB_PER_EUR / rate for ccy, rate in ECB.items()}
THB_PER["THB"] = 1.0

CUBE_SHELF = 15.0     # THB per 330 mL serve (plan base shelf price, ASSUMPTION)
SERVE_ML = 330.0

# ---------------------------------------------------------------- overseas items, per cube or tablet as sold
# id, label, ccy, pack price, serves, dose in mL (list of the label's range), tax basis, src, note
ITEMS = [
    ("waterdrop_us_lemon_lime_12", "waterdrop Lemon Lime (Soft Drink Alternatives), 12 servings, US own store, regular price", "USD", 13.99, 12, [400, 500, 600], "US store price, sales tax not included", "waterdrop_2026-10-20.md", "US own store, regular price; the US page says 12 servings (one cube per serving is an ASSUMPTION); the 400 to 600 mL dose is the UK product's label transferred by ASSUMPTION, because the US page states no water volume"),
    ("waterdrop_uk_focus_lemon_lime_12_sale", "waterdrop FOCUS Lemon-Lime (a different product from the US Lemon Lime), 12 cubes, UK retailer, sale price", "GBP", 6.12, 12, [400, 500, 600], "UK retailer price incl 5% VAT as the page states", "waterdrop_2026-10-20.md", "retailer page, sale price, offer ends 21 Oct 2026"),
    ("waterdrop_uk_focus_lemon_lime_12_regular", "waterdrop FOCUS Lemon-Lime, 12 cubes, UK retailer, regular price", "GBP", 6.80, 12, [400, 500, 600], "UK retailer price incl 5% VAT as the page states", "waterdrop_2026-10-20.md", "retailer page, struck-through price"),
    ("ricola_discovery_48_sale", "Ricola x waterdrop Discovery Set, 48 cubes, EU own store, sale price", "EUR", 28.79, 48, [400, 500, 600], "EU store price incl VAT, excl shipping", "ricola_2026-10-20.md", "20% off"),
    ("ricola_discovery_48_regular", "Ricola x waterdrop Discovery Set, 48 cubes, EU own store, regular price", "EUR", 35.96, 48, [400, 500, 600], "EU store price incl VAT, excl shipping", "ricola_2026-10-20.md", "regular price"),
    ("coke_jp_15cube_ex_tax", "Coca-Cola Japan 1,2,CUBE tea, 15 cubes, JPY 600 excluding tax (2021 release)", "JPY", 600.0, 15, [200, 400], "excl consumption tax", "coca_cola_japan_2026-10-20.md", "release price; Amazon.co.jp only, 2021; tea cube 200 to 400 mL (coffee cube 130 mL not scaled)"),
    ("coke_jp_15cube_incl_10pct", "Coca-Cola Japan 1,2,CUBE tea, 15 cubes, with 10% tax (DERIVED)", "JPY", 660.0, 15, [200, 400], "incl 10% tax (our arithmetic)", "coca_cola_japan_2026-10-20.md", "tax-inclusive figure is our arithmetic"),
    ("nuun_us_tube_10", "Nuun Sport tube, US store (Strawberry Lemonade on the page read); 10 tablets is an ASSUMPTION", "USD", 7.49, 10, [500, 473], "US store price, sales tax not included", "nuun_nuunlife_2026-10-20.md", "US page gives no tablet count; the count of 10 is taken from a Canadian Lemon + Lime listing that states 'one tube makes 10 drinks' (nuun_hydralyte_2026-10-20.md, section A4); the dose is the Canadian listing's directions (500 mL, central) with the 473 mL nutrition basis (16 fl oz) as the alternative; per-tablet figure is ASSUMPTION-based"),
    ("nuun_ca_vitasave_10", "Nuun Sport Lemon + Lime tube, Canadian reseller (Vitasave), regular price", "CAD", 14.99, 10, [500, 473], "Canadian reseller price", "nuun_hydralyte_2026-10-20.md", "reseller price, sold out on read; dose as for the US tube (500 mL directions, 473 mL nutrition basis)"),
]

per_serve = []
per_330 = {}
for (iid, label, ccy, price, serves, doses, taxb, src, note) in ITEMS:
    local = price / serves
    thb = local * THB_PER[ccy]
    per_serve.append({
        "id": iid, "label": label, "currency": ccy, "pack_price": price, "serves": serves,
        "dose_ml_range_on_label": doses, "tax_basis": taxb,
        "price_per_serve_local": round(local, 4),
        "price_per_cube_as_sold_THB": round(thb, 2), "price_per_serve_THB": round(thb, 2),
        "src": src, "note": note,
    })
    # per 330 mL equivalent: price per cube x 330 / dose (assumes the taste scales with the dose: ASSUMPTION)
    eq = {str(d): r2(thb * SERVE_ML / d) for d in doses}
    lo, hi = min(eq.values()), max(eq.values())
    if 500 in doses:
        central = eq["500"]
        central_is = "500 mL"
    elif len(doses) == 1:
        central = eq[str(doses[0])]
        central_is = "%d mL" % doses[0]
    else:
        central = r2(thb * SERVE_ML / (sum(doses) / len(doses)))
        central_is = "midpoint of the label range"
    per_330[iid] = {
        "dose_ml_options": doses, "THB_per_330ml_by_dose_ml": eq,
        "THB_per_330ml_low": lo, "THB_per_330ml_high": hi, "THB_per_330ml_central": central,
        "central_is": central_is,
        "ratio_to_cube_as_sold": round(thb / CUBE_SHELF, 2),
        "ratio_to_cube_per_330ml_low": round(lo / CUBE_SHELF, 2),
        "ratio_to_cube_per_330ml_central": round(central / CUBE_SHELF, 2),
        "ratio_to_cube_per_330ml_high": round(hi / CUBE_SHELF, 2),
        "cube_minus_analogue_per_330ml_central_THB": r2(CUBE_SHELF - central),
        "cube_vs_low_dose_pct": round(100.0 * (CUBE_SHELF - lo) / lo, 1),
        "cube_vs_high_dose_pct": round(100.0 * (CUBE_SHELF - hi) / hi, 1),
    }
for x in per_serve:
    x["per_330ml_equivalent"] = per_330[x["id"]]

# ---------------------------------------------------------------- Thai effervescent tablets (Priceza, 20 Oct 2026)
# Inclusion rule as applied (68e section 3.3): a row is counted when the listing presents the product as an
# effervescent vitamin or mineral tablet, judged from the brand or the Priceza search page that returned it
# (Berocca, Redoxon, Demosana Vitamin C, HOF Effer, Interpharma and Airborne rows in the Priceza effervescent
# searches) or from the title; the title states the tablet count (a multi-tube pack counts all tubes); the
# price is not a placeholder; and the row has no expiry or out-of-stock note that makes it expired on
# 20 October 2026; listings of one shop chain at one price count once. TITLE_STATES_FORM marks the rows whose
# own title says effervescent (เม็ดฟู่, Effer, effervescent, แบบเม็ดฟู่ละลายน้ำ). EXPIRY_2027_IN_TITLE marks the
# two rows whose title says the product expires in 2027 (not expired on the day read; sensitivity only).
# Source pages: priceza_thai_effervescent_tablets_2026-10-20.md (S, 20 October 2026).
# group: "bayer" (Berocca, Redoxon vitamin tablets), "cdr" (Redoxon family CDR Calcium D), "lemon" (lemon or lime tablets),
#        "other" (orange or mixed Demosana)
THAI_ROWS = [
    # id, product, group, flavour, tablets, price THB, listed price, seller (channel)
    ("T01", "Berocca Immu D+ 15 tablets", "bayer", "not stated (orange line)", 15, 149.0, 209.0, "ALL ONLINE (7-Eleven online shop)"),
    ("T02", "Berocca Immu D+ 2 tablets, pack of 12 (24 tablets, our reading of the title)", "bayer", "not stated", 24, 399.0, 420.0, "ALL ONLINE (7-Eleven online shop)"),
    ("T03", "Berocca Immu D 3 x 15 tablets", "bayer", "orange line", 45, 559.0, None, "Bayer Consumer Health Official Store, LazMall (Lazada)"),
    ("T04", "Berocca Immu D+ 15 tablets", "bayer", "orange", 15, 217.0, None, "Shopee, MM pharmacy"),
    ("T05", "Berocca vitamin effervescent 15 tablets (title: expiry year 2027)", "bayer", "not stated", 15, 235.0, None, "Lazada, ช้อปปิ้งชิลล์"),
    ("T06", "Berocca effervescent 15 tablets (title: expiry year 2027)", "bayer", "orange", 15, 235.0, None, "Lazada, ยาเภสัช"),
    ("T07", "Berocca Immu D+ Z D Zinc (Redoxon formula) 15 tablets", "bayer", "orange", 15, 219.0, None, "Shopee, 24 OSOD"),
    ("T08", "Berocca Immu D+ 15 tablets", "bayer", "orange", 15, 649.0, None, "Shopee, healthy_trends_official_store"),
    ("T09", "Berocca 30 tablets", "bayer", "orange", 30, 1239.0, None, "Shopee, 76np3t0n_i"),
    ("T10", "Redoxon Zinc 15 tablets", "bayer", "not stated", 15, 228.0, None, "Lazada"),
    ("T11", "Redoxon Zinc 15 tablets", "bayer", "not stated", 15, 195.0, None, "PharmaShop4U (online pharmacy)"),
    ("T12", "Redoxon vitamin C 15 tablets", "bayer", "not stated", 15, 200.0, None, "Shopee, pattaruk_ja"),
    ("T13", "Redoxon Triple Action 10 tablets", "bayer", "not stated", 10, 221.0, None, "Shopee, fachristore7c.th"),
    ("T14", "Redoxon Triple Action Effervescent Orange 30 x 3 (90 tablets)", "bayer", "orange", 90, 1313.0, None, "Shopee, mve8llnwqv"),
    ("T15", "CDR Calcium D Redoxon 15 tablets", "cdr", "not stated", 15, 150.0, None, "Shopee, ห้องยาชุมชน"),
    ("T16", "CDR Calcium D Redoxon 15 tablets, pack of 2 (30 tablets, our reading)", "cdr", "orange", 30, 245.0, None, "Shopee"),
    ("T17", "CDR Calcium D Redoxon 2 tubes of 15 (30 tablets)", "cdr", "orange", 30, 330.0, 540.0, "Lazada"),
    ("T18", "CDR Calcium D Redoxon 2 tubes of 15 (30 tablets)", "cdr", "orange", 30, 394.0, 540.0, "Lazada"),
    ("T19", "CDR Calcium D Redoxon 3 tubes of 15 (45 tablets)", "cdr", "orange", 45, 474.0, 795.0, "Lazada"),
    ("T20", "CDR Calcium D Redoxon 4 tubes of 15 (60 tablets)", "cdr", "orange", 60, 565.0, 1000.0, "Lazada"),
    ("T21", "CDR Calcium D Redoxon 4 tubes of 15 (60 tablets)", "cdr", "orange", 60, 631.0, 1000.0, "Lazada"),
    ("L01", "Demosana Vitamin C Lemon 20 tablets", "lemon", "lemon", 20, 119.0, 180.0, "Lazada, Today is bestseller"),
    ("L02", "Demosana Vitamin C Lemon 20 tablets", "lemon", "lemon", 20, 130.0, None, "Shopee, santegoodhealth_officialshop"),
    ("L03", "Demosana Vitamin C Lemon Effer 20 tablets", "lemon", "lemon", 20, 132.16, 159.5, "Lazada, SAVEDRUG (LazMall)"),
    ("L04", "Demosana Vitamin C Lemon 20 tablets (11 branch listings of one pharmacy chain, counted once)", "lemon", "lemon", 20, 145.0, None, "Shopee, ร้านยากรุงเทพ (pharmacy chain)"),
    ("L05", "Demosana Vitamin C Lemon 20 tablets", "lemon", "lemon", 20, 149.0, None, "Shopee, ชีวดี"),
    ("L06", "Interpharma Magnesium Plus B Complex 20 tablets", "lemon", "lemon", 20, 140.0, None, "Lazada, Yadeemedical"),
    ("L07", "Interpharma Magnesium Plus B Complex 20 tablets (green)", "lemon", "lemon", 20, 190.0, 780.0, "Shopee, 365wecareshop"),
    ("L08", "Interpharma Magnesium B Complex 20 tablets", "lemon", "lemon", 20, 280.0, None, "TikTok Shop"),
    ("L09", "HOF Effer Zinc+ Vitamin C 20 tablets", "lemon", "lime lemon", 20, 150.0, None, "PharmaShop4U (online pharmacy)"),
    ("L10", "Airborne Vitamin C effervescent 10 tablets (US brand, import)", "lemon", "lemon", 10, 490.0, None, "Shopee, mememelonshop"),
    ("O01", "Demosana Vitamin C Orange 20 tablets", "other", "orange", 20, 129.0, None, "Lazada, ร้านยา DE BANGKOK 4"),
    ("O02", "Demosana Vitamin C mixed flavours 20 tablets (3 listings of one seller counted once)", "other", "mixed (orange, strawberry, yuzu, lemon)", 20, 117.0, None, "Lazada, PharmacarePlus"),
    ("O03", "Demosana Vitamin C mixed flavours 20 tablets", "other", "mixed (orange, strawberry, yuzu, lemon)", 20, 279.71, 337.0, "TikTok Shop"),
]
# Rows whose own listing title states the effervescent form (raw Priceza titles, 20 October 2026)
TITLE_STATES_FORM = {"T03", "T05", "T06", "T08", "T11", "T14", "T15", "T16", "T19", "L03", "L09", "L10"}
# Rows whose title says the product expires in 2027 (not expired on 20 October 2026)
EXPIRY_2027_IN_TITLE = {"T05", "T06"}

# Rows read and not counted, with the reason (so that the set is not hand-picked)
THAI_EXCLUDED = [
    ("Redoxon Zinc 15 tablets, THB 888 (Shopee, Banya Yooyen)", "price looks like a placeholder: THB 888 recurs on two single-tablet listings"),
    ("Redoxon Zinc, THB 99,999 (three Shopee sellers)", "placeholder price"),
    ("Redoxon Zinc 15 tablets, THB 155 (Shopee, FS.MEDICALS)", "the title says expiry 03/2025 (expired on 20 October 2026)"),
    ("Redoxon Zinc 15 tablets, THB 183 (Meyaadee online pharmacy)", "out of stock on read (page opened); would be THB 12.20 per tablet"),
    ("HOF Effer Zinc+ Vitamin C 20s, THB 447 and THB 1,776 (PharmaShop4U, two other SKUs)", "same title as the THB 150 row at 3 and 12 times the price: pack size UNVERIFIED"),
    ("Demosana Magnesium Lemon 20s (2 tubes) THB 249 (Lazada)", "tablet count ambiguous"),
    ("Demosana Vitamin C Lemon / Immune Refresh Lemon 82 g THB 149 (Tops Online); Demosana Vitamin C 20Tab THB 149 (Boots); Strawberry 20S THB 288 (Boots)", "channel evidence only: the Tops and Boots rows are in Priceza's recommended block and the Tops title gives no tablet count"),
    ("Berocca Performance 30 tablets (ALL ONLINE THB 199; LazMall THB 213; Shopee THB 250)", "swallowed tablet (title says เม็ดกลืน), not effervescent"),
    ("Berocca Boost 20 tablets THB 1,350 and BeroccaMind Citrus 20 tablets THB 1,228 (Lazada, YUI49)", "format not stated on the page"),
    ("Berocca Immu D Dietary Supplement THB 209 (LazMall); Berocca 12 ingredients orange THB 230; Berocca Australia import THB 750; Demosana Collagen C THB 299 and Zinc C THB 179; NUTRAKAL calcium THB 249; Redoxon / Berocca THB 187", "no tablet count stated"),
    ("Redoxon Kids Vitamin C 60 chewable THB 299 (Shopee)", "chewable, not effervescent"),
    ("Berocca and Elderberry sachets and drinks (THB 224 to THB 819)", "not a tablet"),
    ("Demosana TikTok Shop rows at THB 165.55 to THB 212.85 (about 80% off a THB 930 list)", "no tablet count; deep-discount listing"),
    ("Hall XS Singh Ume Lemon Soda 20 tablets THB 22 (BigC Shopping Online)", "a lozenge or confectionery tablet, not a drink"),
    ("Alka-Seltzer, bath salts, descalers, stain removers, candies", "not a vitamin drink tablet"),
]


def exact_price_per_tablet(row):
    return row["price_THB"] / row["tablets"]


thai_rows_out = []
for (tid, prod, grp, flav, n, price, listed, seller) in THAI_ROWS:
    thai_rows_out.append({
        "id": tid, "product": prod, "group": grp, "flavour": flav, "tablets": n, "price_THB": price,
        "listed_price_THB": listed, "seller": seller,
        "title_states_effervescent_form": tid in TITLE_STATES_FORM,
        "expiry_2027_in_title": tid in EXPIRY_2027_IN_TITLE,
        "price_per_tablet_THB": r2(price / n),
        "price_per_tablet_unrounded_THB": round(price / n, 6),
        "price_per_tablet_at_listed_price_THB": (r2(listed / n) if listed else None),
    })
_exact = {r["id"]: r["price_per_tablet_unrounded_THB"] for r in thai_rows_out}


def stats_from_exact(vals):
    """Quartiles and median on unrounded values (inclusive method); rounded to 2 dp at the end."""
    v = sorted(vals)
    if len(v) >= 2:
        q = statistics.quantiles(v, n=4, method="inclusive")
        q1, q3 = q[0], q[2]
    else:
        q1 = q3 = v[0]
    med = statistics.median(v)
    return {
        "n": len(v), "min": r2(v[0]), "q1": r2(q1), "median": r2(med), "q3": r2(q3), "max": r2(v[-1]),
        "median_unrounded_THB": round(med, 6),
        "rows_below_cube": sum(1 for x in v if x < CUBE_SHELF),
        "rows_above_cube": sum(1 for x in v if x > CUBE_SHELF),
        "cube_minus_median_THB": r2(CUBE_SHELF - med),
        "cube_over_median_ratio": round(CUBE_SHELF / med, 2),
    }


def ids_stats(ids):
    return stats_from_exact([_exact[i] for i in ids])


ALL_IDS = [r["id"] for r in thai_rows_out]
BAYER_IDS = [r["id"] for r in thai_rows_out if r["group"] == "bayer"]
CDR_IDS = [r["id"] for r in thai_rows_out if r["group"] == "cdr"]
LEMON_IDS = [r["id"] for r in thai_rows_out if r["group"] == "lemon"]
# The three Interpharma Magnesium rows (L06 to L08): no listing title shows an effervescent form (raw Priceza
# titles, 20 October 2026). They stay counted in the headline set and are UNVERIFIED for form; the set without
# them is the sensitivity.
INTERPHARMA_FORM_UNVERIFIED = {"L06", "L07", "L08"}
OTHER_IDS = [r["id"] for r in thai_rows_out if r["group"] == "other"]
TITLE_IDS = [r["id"] for r in thai_rows_out if r["title_states_effervescent_form"]]

thai_stats = {
    "all_counted_rows": ids_stats(ALL_IDS),
    "bayer_berocca_redoxon_vitamin_tablets": ids_stats(BAYER_IDS),
    "redoxon_cdr_calcium_tablets": ids_stats(CDR_IDS),
    "lemon_or_lime_tablets": ids_stats(LEMON_IDS),
    "orange_or_mixed_demosana": ids_stats(OTHER_IDS),
}
thai_stats["bayer_without_two_high_outliers_T08_T09"] = ids_stats([i for i in BAYER_IDS if i not in ("T08", "T09")])
thai_stats["bayer_without_two_high_outliers_T08_T09"]["note"] = "T08 (THB 43.27) and T09 (THB 41.30) are named outliers"
thai_stats["lemon_or_lime_without_airborne_import_L10"] = ids_stats([i for i in LEMON_IDS if i != "L10"])
thai_stats["lemon_or_lime_without_airborne_import_L10"]["note"] = "L10 (THB 49.00, a US brand import) is a named outlier"

thai_stats["lemon_or_lime_without_interpharma_form_unverified_L06_L07_L08"] = ids_stats([i for i in LEMON_IDS if i not in INTERPHARMA_FORM_UNVERIFIED])
thai_stats["lemon_or_lime_without_interpharma_form_unverified_L06_L07_L08"]["note"] = "seven rows whose brand or own title is taken as the effervescent form (L01 to L05, L09, L10); the three Interpharma rows (L06 to L08) are UNVERIFIED for form"
# The two rows whose title says expiry year 2027 (T05 and T06), removed as a sensitivity
thai_stats["bayer_without_2027_expiry_rows_T05_T06"] = ids_stats([i for i in BAYER_IDS if i not in EXPIRY_2027_IN_TITLE])
thai_stats["bayer_without_2027_expiry_rows_T05_T06"]["note"] = "T05 and T06 (THB 235 each, Lazada) carry 'expiry year 2027' in the title; not expired on 20 October 2026; removed here as a sensitivity only"
thai_stats["all_counted_without_2027_expiry_rows_T05_T06"] = ids_stats([i for i in ALL_IDS if i not in EXPIRY_2027_IN_TITLE])
# Title-form subsets: only rows whose own listing title states the effervescent form
thai_stats["title_states_form_all_counted"] = ids_stats(TITLE_IDS)
thai_stats["title_states_form_bayer"] = ids_stats([i for i in TITLE_IDS if i in BAYER_IDS])
thai_stats["title_states_form_lemon"] = ids_stats([i for i in TITLE_IDS if i in LEMON_IDS])
thai_stats["title_states_form_all_counted"]["note"] = "rows whose own title states the effervescent form; 22 of 34 counted rows do not state it in the title"
thai_stats["title_states_form_bayer"]["note"] = "Berocca and Redoxon rows whose own title states the effervescent form (T03, T05, T06, T08, T11, T14)"
thai_stats["title_states_form_bayer"]["median_is_above_or_below_cube"] = (
    "above" if thai_stats["title_states_form_bayer"]["median"] > CUBE_SHELF else "below")
lemon_ratio_vs_cube = {
    "cube_over_lemon_tablet_median": round(CUBE_SHELF / thai_stats["lemon_or_lime_tablets"]["median_unrounded_THB"], 2),
    "cube_over_lemon_tablet_min": round(CUBE_SHELF / thai_stats["lemon_or_lime_tablets"]["min"], 2),
    "cube_over_lemon_tablet_q3": round(CUBE_SHELF / thai_stats["lemon_or_lime_tablets"]["q3"], 2),
}

# Sensitivity: rows read and left out are put back to show what they would do to the medians
_bayer_vals = [_exact[i] for i in BAYER_IDS]
_lemon_vals = [_exact[i] for i in LEMON_IDS]
thai_sensitivity = {
    "bayer_with_the_THB_888_15_tablet_row_added": stats_from_exact(_bayer_vals + [888.0 / 15]),
    "lemon_with_the_HOF_THB_447_and_THB_1776_rows_added_at_20_tablets": stats_from_exact(_lemon_vals + [447.0 / 20, 1776.0 / 20]),
    "bayer_with_the_out_of_stock_Meyaadee_THB_183_row_added": stats_from_exact(_bayer_vals + [183.0 / 15]),
}
_bayer_listed = []
for r in thai_rows_out:
    if r["group"] == "bayer":
        if r["id"] in ("T01", "T02"):
            _bayer_listed.append(r["listed_price_THB"] / r["tablets"])
        else:
            _bayer_listed.append(_exact[r["id"]])
thai_sensitivity["bayer_listed_prices_instead_of_ALL_ONLINE_sale_prices"] = stats_from_exact(_bayer_listed)

# ---------------------------------------------------------------- Thai marketplace rows for Nuun and Hydralyte (Priceza, 20 Oct 2026)
NUUN_THAI = [
    ("N19", "Nuun Sport Hydration, 10 tablets, Lazada, iBody Thailand (price 195.50, listed 200; title carries a '75 OFF' phrase)", 195.50, 10, 473, "Lazada"),
    ("N_iherb_orange", "Nuun Sport Effervescent Electrolyte, Orange, 10 tablets, iHerb", 267.64, 10, 473, "iHerb (cross-border)"),
    ("N_iherb_grape", "Nuun Sport Effervescent Electrolyte, Grape, 10 tablets, iHerb", 267.34, 10, 473, "iHerb (cross-border)"),
    ("N_iherb_immune", "Nuun Daily Hydration Immune Support, Orange Citrus, 10 tablets, iHerb", 227.24, 10, None, "iHerb (cross-border)"),
    ("N16", "Nuun Hydration Immunity, 10 servings, Lazada, iLiveLife (listed 1,000)", 745.0, 10, None, "Lazada"),
]
nuun_thai_out = []
for (nid, label, price, n, ml, ch) in NUUN_THAI:
    row = {"id": nid, "label": label, "price_THB": price, "tablets": n, "channel": ch, "price_per_tablet_THB": r2(price / n)}
    if ml:
        row["THB_per_330ml_at_500ml_directions_dose"] = r2(price / n * SERVE_ML / 500.0)
        row["THB_per_330ml_at_473ml_nutrition_dose"] = r2(price / n * SERVE_ML / ml)
    nuun_thai_out.append(row)
_nuun_nocount = [295.0, 295.0, 295.0, 295.0, 295.0, 290.0, 299.0, 299.0, 349.0, 349.0, 350.0, 350.0, 350.0, 380.0, 420.0, 420.0, 420.0, 300.0, 300.0]
nuun_nocount = {
    "rows": len(_nuun_nocount), "price_min_THB": min(_nuun_nocount), "price_max_THB": max(_nuun_nocount),
    "pack_count": "not stated on any of these rows (UNVERIFIED)",
    "conditional_per_tablet_if_10_tablets_THB": [r2(min(_nuun_nocount) / 10), r2(max(_nuun_nocount) / 10)],
    "conditional_is": "ASSUMPTION: the tube holds 10 tablets as on the iBody, iHerb and Canadian reseller pages; not read on these rows",
}
HYDRALYTE_THAI = [
    ("H4", "Hydralyte Electrolyte Ice Blocks 16 pack, Strawberry Kiwi, Shopee", 850.0, 16, "per ice block"),
    ("H5", "Hydralyte Liver Support Blood Orange, 12 packets, iHerb", 586.34, 12, "per packet"),
    ("H6", "Hydralyte Lemon Squeeze, 6 packets, iHerb", 506.83, 6, "per packet"),
    ("H7", "Hydralyte Variety Pack, 30 packets, iHerb", 1187.58, 30, "per packet"),
    ("H8", "Hydralyte Verisol Collagen Strawberry Lemonade, 12 packets, iHerb", 471.47, 12, "per packet"),
]
hydralyte_thai_out = [{"id": a, "label": b, "price_THB": c, "units": d, "unit": e, "price_per_unit_THB": r2(c / d)} for (a, b, c, d, e) in HYDRALYTE_THAI]
hydralyte_thai_out.append({"id": "H1_to_H3", "label": "Hydralyte effervescent electrolyte tablets (three listings, one a lemon listing), Lazada, Ching tongom", "price_THB": 280.0,
                           "units": None, "unit": "tablet count not stated", "price_per_unit_THB": None})
hydralyte_us_value_pack = {"label": "Hydralyte Orange tablets Value 2-pack (2 tubes), US-facing brand site", "price_USD": 21.99,
                           "price_THB": r2(21.99 * THB_PER_USD), "tablet_count": "not stated (UNVERIFIED)", "price_per_tablet_THB": None}

# ---------------------------------------------------------------- SodaStream home route
# UK basis (P): price GBP 25.98 and "up to 60L" per cylinder on sodastream.co.uk/products/refill.
# Canadian price CAD 19.99 (sodastream.ca/products/refill, P) states no litre figure; applying the UK yield to it is a PROXY.
# The mix is "about 9 L" per 440 mL pack (sodastream.com starry page, P).
SYRUP_L = 9.0          # litres per 440 mL Starry Lemon Lime Zero Sugar mix, as stated on the page ("about 9 L")
SERVE_L = 0.330
syrup = {}
for tag, usd in (("regular", 7.99), ("sale", 5.99)):
    usd_serve = usd * SERVE_L / SYRUP_L
    syrup[tag] = {"usd_pack": usd, "usd_per_330ml": round(usd_serve, 4), "thb_per_330ml": round(usd_serve * THB_PER["USD"], 2)}
CO2_L = 60.0           # "up to 60L" per cylinder, UK page only (a maximum, so the UK cost per serve is a floor)
uk_local = 25.98 * SERVE_L / CO2_L
ca_local = 19.99 * SERVE_L / CO2_L
co2 = {
    "uk_exchange_25.98_GBP_at_stated_up_to_60L": {
        "status": "P (UK page: exchange price and 'up to 60L')", "local_per_330ml": round(uk_local, 4),
        "thb_per_330ml": round(uk_local * THB_PER["GBP"], 2)},
    "canada_exchange_19.99_CAD_at_UK_60L_yield": {
        "status": "PROXY (Canadian page states no litre figure; the UK yield is applied)", "local_per_330ml": round(ca_local, 4),
        "thb_per_330ml": round(ca_local * THB_PER["CAD"], 2)},
}
uk_co2 = co2["uk_exchange_25.98_GBP_at_stated_up_to_60L"]["thb_per_330ml"]
ca_co2 = co2["canada_exchange_19.99_CAD_at_UK_60L_yield"]["thb_per_330ml"]
sodastream = {
    "syrup": syrup, "co2": co2,
    "total_thb_per_330ml_low_UK_basis": round(syrup["sale"]["thb_per_330ml"] + uk_co2, 2),
    "total_thb_per_330ml_high_UK_basis": round(syrup["regular"]["thb_per_330ml"] + uk_co2, 2),
    "total_thb_per_330ml_low_if_Canadian_cylinder_taken_at_UK_yield_PROXY": round(syrup["sale"]["thb_per_330ml"] + ca_co2, 2),
    "note": ("machine purchase excluded; prices from the UK and Canadian brand pages and the US mix page. The UK-basis "
             "figures are a floor because the cylinder yield is 'up to' 60 L and the mix is 'about' 9 L. The "
             "Canadian low end is a PROXY at the UK yield."),
}

# ---------------------------------------------------------------- reference ladder (canned lemon soda), read from the 68d second-revision results file
# Version 6: the ladder is read from rework/screen/t5_retail_price_ladder_results.json, the file that record 68d (second revision)
# cites. The first-revision file lemon_soda_price_ladder_results.json (row IDs E, M and L) is no longer read. Its single-can set
# includes a lemon-mint flavour variant, and its 18-row and 22-row sets follow rules that 68d second revision does not use.
LADDER_PATH = os.path.join(HERE, "t5_retail_price_ladder_results.json")
with open(LADDER_PATH, encoding="utf-8") as _f:
    _L = json.load(_f)
_lad = _L["ladders"]
_sets = _L["sets"]
_rows = {r["id"]: r for r in _L["rows"]}
_mainA = _lad["A_main_all_usable_cans"]        # 31 rows: 16 retailer pages and 15 Priceza offers from named sellers
_directB = _lad["B_direct_retailer_pages"]     # 16 rows: retailer product pages only; every row is a multipack
_singlesD = _lad["D_single_cans"]              # 4 rows: S01, S02, S03, S05
_singhaK = _lad["K_singha_rows_in_main"]       # 8 rows: Singha Lemon Soda and Singha Sparkling Water Lime
ladder_summary = {
    "source_file": "rework/screen/t5_retail_price_ladder_results.json (68d second revision; sets A, B, D and K)",
    "main_set_A_per_330ml": _mainA,
    "retailer_pages_set_B_per_330ml": _directB,
    "single_cans_set_D_per_330ml": _singlesD,
    "singha_rows_set_K_per_330ml": _singhaK,
    "cube_shelf_price_THB": CUBE_SHELF, "cube_planning_ex_factory_THB": 9.0, "cube_cost_THB": 4.09,
}
SINGHA_SINGLE = _rows["S01"]["per_330ml_thb"]                       # 17.00 (Lotus's, single can)
SINGLE_MIN = _singlesD["min"]                                       # 16.2462 (THB 16 on a 325 mL can, scaled)
SINGLE_MEDIAN = _singlesD["median"]                                 # 16.6231 (median of unrounded per-330 mL values)
SINGLE_MAX = _singlesD["max"]                                       # 18.00
MULTI_MEDIAN = _directB["median"]                                   # 13.875 (set B, 16 retailer-page rows)
ALL_MEDIAN = _mainA["median"]                                       # 14.0462 (set A, 31 rows)
# Singha Lemon Soda pack rows (the Sparkling Water Lime rows D04 and D08 are not Lemon Soda); the 7-Eleven six-can outlier is named separately
SINGHA_PACK_IDS = ("D01", "D06", "D07", "D12", "D13")
SINGHA_OUTLIER_IDS = ("D02",)
singha_pack_rows = [{"id": i, "product": _rows[i]["product"], "retailer": _rows[i]["retailer"], "pack_count": _rows[i]["pack_count"],
                     "per_330ml_thb": _rows[i]["per_330ml_thb"]} for i in SINGHA_PACK_IDS + SINGHA_OUTLIER_IDS]
SINGHA_PACK_LOW = min(_rows[i]["per_330ml_thb"] for i in SINGHA_PACK_IDS)    # 13.54 (Makro PRO 24-can)
SINGHA_PACK_HIGH = max(_rows[i]["per_330ml_thb"] for i in SINGHA_PACK_IDS)   # 14.17 (Lotus's 6-can)
SINGHA_OUTLIER = _rows["D02"]["per_330ml_thb"]                                # 28.67 (7-Eleven ALL Online 6-can, THB 172)

# Multi-pack median sensitivities on set B (16 retailer-page rows)
_mp_ids = _sets["B_direct_retailer_pages"]
_mp_vals = [_rows[i]["per_330ml_thb"] for i in _mp_ids]
MULTI_ALL_16 = statistics.median(_mp_vals)
_plain_ids = set(_sets["N_plain_soda_water_rows_in_main"])                    # D11, D17
_sparkling_ids = {"D04", "D08"}                                               # Singha Sparkling Water Lime 24-can and 24-unit rows
_mp_no_plain = [_rows[i]["per_330ml_thb"] for i in _mp_ids if i not in _plain_ids]
_mp_lemon_lime_only = [_rows[i]["per_330ml_thb"] for i in _mp_ids if i not in _plain_ids | _sparkling_ids]
MULTI_NO_PLAIN_SODA = statistics.median(_mp_no_plain)
MULTI_LEMON_LIME_ONLY = statistics.median(_mp_lemon_lime_only)
assert len(_mp_vals) == 16 and abs(MULTI_ALL_16 - 13.875) < 1e-9, MULTI_ALL_16
assert len(_mp_no_plain) == 14 and len(_mp_lemon_lime_only) == 12
assert abs(SINGLE_MEDIAN - 16.6231) < 0.0001 and abs(MULTI_MEDIAN - 13.875) < 1e-9 and abs(ALL_MEDIAN - 14.0462) < 0.0001
multipack_sensitivity = {
    "set_B_16_retailer_page_rows_median": round(MULTI_ALL_16, 4),
    "set_B_without_2_plain_soda_water_cans_D11_D17_14_rows_median": round(MULTI_NO_PLAIN_SODA, 4),
    "set_B_lemon_and_lime_packs_only_without_plain_soda_water_or_sparkling_water_12_rows_median": round(MULTI_LEMON_LIME_ONLY, 4),
    "range_of_set_B_per_330ml": [min(_mp_vals), max(_mp_vals)],
}


def diff(a, ref):
    return {"abs_THB": round(a - ref, 2), "pct": round(100.0 * (a - ref) / ref, 1)}


by_id = {x["id"]: x["price_per_serve_THB"] for x in per_serve}
sodastream_low = round(syrup["sale"]["thb_per_330ml"] + uk_co2, 2)
comparisons = {
    "cube_shelf_vs_cheapest_single_can": diff(CUBE_SHELF, SINGLE_MIN),
    "cube_shelf_vs_singha_single_can": diff(CUBE_SHELF, SINGHA_SINGLE),
    "cube_shelf_vs_single_can_median": diff(CUBE_SHELF, SINGLE_MEDIAN),
    "cube_shelf_vs_most_expensive_single_can": diff(CUBE_SHELF, SINGLE_MAX),
    "cube_shelf_vs_singha_pack_low": diff(CUBE_SHELF, SINGHA_PACK_LOW),
    "cube_shelf_vs_singha_pack_high": diff(CUBE_SHELF, SINGHA_PACK_HIGH),
    "cube_shelf_vs_multipack_median": diff(CUBE_SHELF, MULTI_MEDIAN),
    "cube_shelf_vs_all_cans_median": diff(CUBE_SHELF, ALL_MEDIAN),
    "waterdrop_us_over_cube_shelf_ratio_as_sold": round(by_id["waterdrop_us_lemon_lime_12"] / CUBE_SHELF, 2),
    "waterdrop_uk_focus_sale_over_cube_shelf_ratio_as_sold": round(by_id["waterdrop_uk_focus_lemon_lime_12_sale"] / CUBE_SHELF, 2),
    "ricola_eu_sale_over_cube_shelf_ratio_as_sold": round(by_id["ricola_discovery_48_sale"] / CUBE_SHELF, 2),
    "nuun_us_over_cube_shelf_ratio_as_sold": round(by_id["nuun_us_tube_10"] / CUBE_SHELF, 2),
    "coke_jp_ex_tax_over_cube_shelf_ratio_as_sold": round(by_id["coke_jp_15cube_ex_tax"] / CUBE_SHELF, 2),
    "cube_shelf_vs_thai_lemon_tablet_median": diff(CUBE_SHELF, thai_stats["lemon_or_lime_tablets"]["median_unrounded_THB"]),
    "cube_shelf_vs_thai_bayer_vitamin_tablet_median": diff(CUBE_SHELF, thai_stats["bayer_berocca_redoxon_vitamin_tablets"]["median_unrounded_THB"]),
    "cube_shelf_vs_thai_bayer_median_without_2027_expiry_rows": diff(CUBE_SHELF, thai_stats["bayer_without_2027_expiry_rows_T05_T06"]["median_unrounded_THB"]),
    "cube_shelf_vs_thai_bayer_median_title_states_form_only": diff(CUBE_SHELF, thai_stats["title_states_form_bayer"]["median_unrounded_THB"]),
    "cube_shelf_vs_thai_all_counted_tablet_median": diff(CUBE_SHELF, thai_stats["all_counted_rows"]["median_unrounded_THB"]),
    "cube_shelf_vs_sodastream_UK_basis_low": diff(CUBE_SHELF, sodastream_low),
    "cube_shelf_vs_sodastream_UK_basis_high": diff(CUBE_SHELF, sodastream["total_thb_per_330ml_high_UK_basis"]),
}
cube_vs_analogue = {}
for x in per_serve:
    v = x["price_per_serve_THB"]
    cube_vs_analogue[x["id"]] = {"analogue_THB_per_cube_as_sold": v, "cube_minus_analogue_THB": round(CUBE_SHELF - v, 2),
                                 "cube_vs_analogue_pct": round(100.0 * (CUBE_SHELF - v) / v, 1),
                                 "analogue_over_cube_ratio": round(v / CUBE_SHELF, 2)}


overseas_ratio_as_sold = {x["id"]: round(x["price_per_serve_THB"] / CUBE_SHELF, 2) for x in per_serve}
overseas_ratio_as_sold["thai_lazada_nuun_10_tablets_THB_19.55"] = round(19.55 / CUBE_SHELF, 2)
_ratio_listed = [v for k, v in overseas_ratio_as_sold.items() if k not in ("coke_jp_15cube_ex_tax", "coke_jp_15cube_incl_10pct", "thai_lazada_nuun_10_tablets_THB_19.55")]
overseas_ratio_summary = {
    "listed_overseas_units_min": min(_ratio_listed), "listed_overseas_units_max": max(_ratio_listed),
    "exceptions": {"thai_lazada_nuun_10_tablets_THB_19.55": overseas_ratio_as_sold["thai_lazada_nuun_10_tablets_THB_19.55"],
                   "coke_jp_tea_2021_ex_tax": overseas_ratio_as_sold["coke_jp_15cube_ex_tax"]},
}
assert overseas_ratio_summary["listed_overseas_units_min"] >= 1.5 and overseas_ratio_summary["listed_overseas_units_max"] <= 2.61

# ---- sanity assertions for the Thai medians quoted in the record (68e section 3.3)
assert round(thai_stats["bayer_berocca_redoxon_vitamin_tablets"]["median_unrounded_THB"], 2) == 14.90
assert round(thai_stats["bayer_without_2027_expiry_rows_T05_T06"]["median_unrounded_THB"], 2) == 14.59
assert round(thai_stats["title_states_form_bayer"]["median_unrounded_THB"], 2) == 15.13
assert round(thai_stats["lemon_or_lime_tablets"]["median_unrounded_THB"], 2) == 7.35
assert round(thai_stats["lemon_or_lime_without_interpharma_form_unverified_L06_L07_L08"]["median_unrounded_THB"], 2) == 7.25
assert len(TITLE_IDS) == 12 and len(ALL_IDS) == 34

# ---------------------------------------------------------------- financials arithmetic (inputs read from saved pages)
def pct(a, b):
    return round(100.0 * a / b, 1)


FIN = {
    "Coca-Cola Company (group, FY to 31 Dec)": {
        "unit": "USD million", "years": {
            "FY2023": {"revenue": 45754, "gross_profit": 27234, "net_income_parent": 10714},
            "FY2024": {"revenue": 47061, "gross_profit": 28737, "net_income_parent": 10631},
            "FY2025": {"revenue": 47941, "gross_profit": 29544, "net_income_parent": 13107}}},
    "PepsiCo (group, FY to last Saturday of Dec)": {
        "unit": "USD million", "years": {
            "FY2023": {"revenue": 91471, "gross_profit": 49590, "net_income_parent": 9074},
            "FY2024": {"revenue": 91854, "gross_profit": 50110, "net_income_parent": 9578},
            "FY2025": {"revenue": 93925, "gross_profit": 50859, "net_income_parent": 8240}}},
    "Nestle S.A. (group, FY to 31 Dec); gross profit = sales minus cost of goods sold (DERIVED)": {
        "unit": "CHF million", "years": {
            "FY2023": {"revenue": 92998, "cogs": 50328, "net_income_parent": 11209},
            "FY2024": {"revenue": 91354, "cogs": 48670, "net_income_parent": 10884},
            "FY2025": {"revenue": 89490, "cogs": 48694, "net_income_parent": 9033}}},
    "Prestige Consumer Healthcare (group, FY to 31 March)": {
        "unit": "USD thousand", "years": {
            "FY2024 (to 31 Mar 2024)": {"revenue": 1125357, "gross_profit": 624448, "net_income_parent": 209339},
            "FY2025 (to 31 Mar 2025)": {"revenue": 1137762, "gross_profit": 634463, "net_income_parent": 214605},
            "FY2026 (to 31 Mar 2026)": {"revenue": 1088705, "gross_profit": 595578, "net_income_parent": 190301}}},
    "Bayer AG (group, FY to 31 Dec; secondary aggregator)": {
        "unit": "EUR million", "years": {
            "FY2023": {"revenue": 47637, "gross_profit": 27950, "net_income_parent": -2941},
            "FY2024": {"revenue": 46606, "gross_profit": 25775, "net_income_parent": -2552},
            "FY2025": {"revenue": 45575, "gross_profit": 27048, "net_income_parent": -3620}}},
    "waterdrop (Konzernabschluss as labelled by trend.at, 6 May 2026; EUR million; scope partial per the page; no gross profit published)": {
        "unit": "EUR million", "years": {
            "FY2023": {"revenue": 107.12, "net_income_parent": -33.74},
            "FY2024": {"revenue": 126.55, "net_income_parent": -26.62}}},
}
fin_out = {}
for ent, d in FIN.items():
    rows = {}
    for yr, v in d["years"].items():
        gp = v.get("gross_profit")
        if gp is None and "cogs" in v:
            gp = v["revenue"] - v["cogs"]
        row = {"revenue": v["revenue"], "net_income": v["net_income_parent"],
               "net_margin_pct": pct(v["net_income_parent"], v["revenue"])}
        if gp is not None:
            row["gross_profit"] = gp
            row["gross_margin_pct"] = pct(gp, v["revenue"])
        rows[yr] = row
    fin_out[ent] = {"unit": d["unit"], "years": rows}

# Nestle trading operating profit: each input is read from the saved statements extract
# (rework/raw/diligence_2026-10-20/T5b/financials_filings_2026-10-20.md, section 4, which quotes the PDFs
#  rework source: financial-statements-2025-en.pdf for FY2025 and FY2024, financial-statements-2024-en.pdf for FY2023).
NESTLE_INPUTS = {
    "FY2025": {"source": "2025 consolidated statements PDF (2025 column)", "sales": 89490, "other_revenue": 395, "cogs": 48694,
               "distribution": 7306, "marketing_admin": 17883, "rnd": 1613, "other_trading_income": 135,
               "other_trading_expenses": 1849, "reported_trading_operating_profit": 12675},
    "FY2024": {"source": "2025 consolidated statements PDF (2024 column)", "sales": 91354, "other_revenue": 366, "cogs": 48670,
               "distribution": 7567, "marketing_admin": 18112, "rnd": 1667, "other_trading_income": 124,
               "other_trading_expenses": 1195, "reported_trading_operating_profit": 14633},
    "FY2023": {"source": "2024 consolidated statements PDF (2023 column)", "sales": 92998, "other_revenue": 353, "cogs": 50328,
               "distribution": 7765, "marketing_admin": 17549, "rnd": 1656, "other_trading_income": 132,
               "other_trading_expenses": 1665, "reported_trading_operating_profit": 14520},
}
nestle_check = {}
for yr, v in NESTLE_INPUTS.items():
    computed = (v["sales"] + v["other_revenue"] - v["cogs"] - v["distribution"] - v["marketing_admin"] - v["rnd"]
                + v["other_trading_income"] - v["other_trading_expenses"])
    assert computed == v["reported_trading_operating_profit"], (yr, computed, v["reported_trading_operating_profit"])
    nestle_check[yr] = {"source": v["source"], "computed_trading_operating_profit": computed,
                        "printed_trading_operating_profit": v["reported_trading_operating_profit"],
                        "difference": computed - v["reported_trading_operating_profit"], "match": computed == v["reported_trading_operating_profit"]}

other = {
    "cube_contribution_margin_pct_of_ex_factory": pct(4.91, 9.00),
    "cube_contribution_note": "ex-factory THB 9.00 is an ASSUMPTION (60 percent of the THB 15 shelf price); contribution THB 4.91 = 9.00 - 4.09 is DERIVED from plan inputs",
    "cube_cost_share_of_ex_factory_pct": pct(4.09, 9.00),
    "waterdrop_per_330ml_at_500ml_dilution_factor": round(330 / 500, 2),
    "waterdrop_revenue_growth_2023_to_2024_pct": pct(126.55 - 107.12, 107.12),
    "yellow_wood_price_over_divested_business_2025_sales_USD": round(1000.0 / 1200.0, 2),
}

out = {
    "fx": {"THB_per_USD_BoT_mid_15Oct2026": round(THB_PER_USD, 4), "ECB_19Oct2026_per_EUR": ECB,
           "THB_per": {k: round(v, 4) for k, v in THB_PER.items()}},
    "cube_shelf_THB_per_330ml_ASSUMPTION": CUBE_SHELF,
    "per_serve": per_serve,
    "thai_effervescent_tablets": {
        "inclusion_rule_as_applied": ("form taken from the brand or the Priceza search page that returned the row, or from the title "
                                      "(title_states_effervescent_form flags the 12 rows whose own title states it); the title states the tablet count; "
                                      "price not a placeholder; no expiry or out-of-stock note that makes the row expired on 20 Oct 2026 (two rows say expiry year 2027 and are named in expiry_2027_in_title); "
                                      "one shop chain at one price counted once. Source pages: priceza_thai_effervescent_tablets_2026-10-20.md (S, 20 Oct 2026)"),
        "rows": thai_rows_out, "excluded_rows_read": [{"row": a, "reason": b} for (a, b) in THAI_EXCLUDED],
        "stats_per_tablet_THB": thai_stats, "cube_vs_lemon_tablets": lemon_ratio_vs_cube, "sensitivity": thai_sensitivity,
    },
    "nuun_thai_marketplace": {"rows_with_stated_count": nuun_thai_out, "rows_without_count": nuun_nocount},
    "hydralyte_thai_marketplace": hydralyte_thai_out, "hydralyte_us_value_pack": hydralyte_us_value_pack,
    "sodastream_proxy": sodastream,
    "canned_ladder_summary": ladder_summary,
    "singha_pack_per_330ml_low_high": [SINGHA_PACK_LOW, SINGHA_PACK_HIGH],
    "singha_pack_rows": singha_pack_rows,
    "singha_pack_outlier_E2_per_330ml": SINGHA_OUTLIER,
    "comparisons": comparisons, "cube_vs_analogue": cube_vs_analogue,
    "overseas_ratio_as_sold": overseas_ratio_as_sold, "overseas_ratio_summary": overseas_ratio_summary,
    "multipack_sensitivity": multipack_sensitivity,
    "financials": fin_out, "nestle_arithmetic_check": nestle_check, "other": other,
}
path = os.path.join(HERE, "analogue_price_per_serve_68e_results.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("wrote", path)
