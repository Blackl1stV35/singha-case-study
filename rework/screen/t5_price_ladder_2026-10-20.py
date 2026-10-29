"""T5 retail price ladder: lemon, lime and clear carbonated soft drinks and soda waters in 325 to 345 mL cans
sold in Thailand, read 2026-10-20.

Each price row names the raw file saved under rework/raw/diligence_2026-10-20/T5/ that holds the page or
listing text it came from. Prices are the values in those saved extracts (WebFetch summaries of retailer
pages, and Priceza listing pages, which are aggregators). Derived values use exact decimal arithmetic.

Per 330 mL serve = pack price / pack count x 330 / can mL (325 mL cans are scaled to the 330 mL serve).
The cube shelf price of THB 15 per serve is an ASSUMPTION carried from the deck base case, not a market price.

No random numbers are used, so there is no seed. Memory use is a few MB.
Writes rework/screen/t5_price_ladder_2026-10-20_results.json and prints a short summary.
"""
import json
import os
import statistics
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "t5_price_ladder_2026-10-20_results.json")
DATE = "2026-10-20"
SERVE_ML = Decimal(330)
CUBE_SHELF = Decimal("15")  # planning shelf price per cube serve (ASSUMPTION; deck base case)

CAN_STATED = "can (stated on page or listing)"
CAN_READ = "can (not stated; read as can)"
BOTTLE = "bottle"
UNKNOWN = "container not stated"

LL = "lemon_lime_or_lime"
SW = "plain_soda_water"

S_NO = "no sugar claim on page"


def q2(d):
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def R(rid, retailer, channel, product, group, container, can_ml, pack, price, sugar, stock, use, raw, url, note):
    return dict(id=rid, retailer=retailer, channel=channel, product=product, group=group,
                container=container, can_ml=can_ml, pack_count=pack, pack_price_thb=price,
                sugar_status=sugar, stock_wording=stock, use=use, raw_file=raw, url=url, note=note,
                tier="S", date_read=DATE)


def X(rid, retailer, product, price, reason):
    """Listing rows that are not in any ladder; kept for the record."""
    return dict(id=rid, retailer=retailer, product=product, price_thb=price, reason=reason, date_read=DATE)


MAIN_DIRECT_OTHER = []

ROWS = [
    # ---------------- direct retailer pages (7-Eleven ALL Online, CP All) ----------------
    R("D01", "7-Eleven ALL Online", "direct", "Singha Lemon Soda", LL, CAN_STATED, 330, 24, 330,
      "sugar-free (maker page: 0% sugar)", "in stock (page label)", "main",
      "r01_7eleven_singha_lemon_24can.md",
      "https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-ยกลัง-24-กระป๋อง/474313/",
      "Original 408 shown beside 330 (-19%); price validity wording ends 20/10/2026"),
    R("D02", "7-Eleven ALL Online", "direct", "Singha Lemon Soda (6 pack)", LL, CAN_STATED, 330, 6, 172,
      "sugar-free (maker page: 0% sugar)", "in stock (page label)", "anomaly",
      "r02_7eleven_singha_lemon_6can.md",
      "https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-แพ็ก-6-กระป๋อง/514221/",
      "Per can 28.67, about twice the same retailer's 24 pack per can (13.75) and the Makro and Lotus's 6 pack per can; page gives no per can figure; kept in sensitivity"),
    R("D03", "7-Eleven ALL Online", "direct", "Schweppes Lime Soda Zero (6 pack)", LL, CAN_STATED, 330, 6, 170,
      "sugar-free (page: สูตรไม่มีน้ำตาล)", "in stock (page label)", "anomaly",
      "r13_7eleven_schweppes_lime_zero_6can.md",
      "https://www.allonline.7eleven.co.th/p/ชเวปส์มะนาวโซดาซีโร่-330มล-แพ็ก-6-กระป๋อง/354988/",
      "Per can 28.33, about twice the same retailer's 24 pack per can; original 190 struck through; validity ends 20/10/2026; kept in sensitivity"),
    R("D04", "7-Eleven ALL Online", "direct", "Nestle Pure Life Soda Plus Lemon Lime (24 pack)", LL, CAN_STATED, 330, 24, 377,
      "no sugar claim on page (ไม่มีน้ำตาล)", "out of stock (page: ขออภัยสินค้าหมด)", "unavailable",
      "r32_7eleven_nestle_pure_life_soda_lemon_lime_out_of_stock.md",
      "https://www.allonline.7eleven.co.th/p/เนสท์เล่-เพียวไลฟ์-โซดาพลัส-เลมอนไลม์-330-มลถาด-24-กระป๋อง/327940/",
      "Out of stock on the page; excluded from main; kept in sensitivity"),
    R("D05", "7-Eleven ALL Online", "direct", "Singha Sparkling Water Lime (24 pack)", LL, CAN_STATED, 330, 24, 302,
      "not confirmed (page gives 0% calories only)", "in stock (page label)", "main",
      "r14_7eleven_singha_sparkling_lime_24can.md",
      "https://www.allonline.7eleven.co.th/p/สิงห์สปาร์คกลิ้งไลม์-330-มล-ยกลัง-24-กระป๋อง/327253/",
      "Price validity wording 02/03/2026 to 20/10/2026; original 304 beside it"),
    # ---------------- direct retailer pages (Makro PRO, CP All-independent) ----------------
    R("D06", "Makro PRO", "direct", "Sprite Lemon Lime (24 pack)", LL, CAN_READ, 325, 24, 311,
      "regular (sugar not stated)", "none on page", "main",
      "r15_makro_sprite_325_24can.md",
      "https://www.makro.pro/en/p/179712-7078659719363",
      "List price 321 (-3%)"),
    R("D07", "Makro PRO", "direct", "Sprite Lemon Lime (12 pack, 330 mL)", LL, UNKNOWN, 330, 12, 137,
      "regular (sugar not stated)", "none on page", "excluded",
      "r16_makro_sprite_330_12can.md",
      "https://www.makro.pro/en/p/830198-7078660866243",
      "Container not stated; 330 mL Sprite 12 packs are sold as bottles on the Priceza listing (r22, row 13), so the can reading is not confirmed; tier price 135 for 3 or more units"),
    R("D08", "Makro PRO", "direct", "Sprite Chill Lemon Mint (6 pack)", LL, CAN_READ, 325, 6, 78,
      "regular (sugar not stated)", "none on page", "main",
      "r17_makro_sprite_chill_lemon_mint_6can.md",
      "https://www.makro.pro/en/p/630907-363090727914101",
      "List price 81 (-3%); container for this product not confirmed on a readable page"),
    R("D09", "Makro PRO", "direct", "Singha Lemon Soda (6 pack)", LL, CAN_READ, 330, 6, 82,
      "sugar-free (maker page: 0% sugar)", "none on page", "main",
      "r04_makro_singha_lemon_6can.md",
      "https://www.makro.pro/en/p/893947-6814746706115",
      "Buy 3 or more units tier price 78 (used in member-or-tier sensitivity)"),
    R("D10", "Makro PRO", "direct", "Singha Lemon Soda (24 pack)", LL, CAN_READ, 330, 24, 325,
      "sugar-free (maker page: 0% sugar)", "none on page", "main",
      "r03_makro_singha_lemon_24can.md",
      "https://www.makro.pro/en/p/428706-7350275997891",
      "Shown beside 330 (-1%)"),
    R("D11", "Makro PRO", "direct", "Schweppes Soda Water (24 pack)", SW, CAN_READ, 330, 24, 341,
      "plain soda water (" + S_NO + ")", "none on page", "main",
      "r19_makro_schweppes_soda_water_24can.md",
      "https://www.makro.pro/en/p/119581-7416114282691",
      "Tier price 336 for 2 or more units"),
    R("D12", "Makro PRO", "direct", "Schweppes Lime Soda (6 pack)", LL, CAN_READ, 330, 6, 84,
      "regular (sugar not stated; nutrition panel carbohydrates 16 g, basis not stated)", "none on page", "main",
      "r18_makro_schweppes_lime_soda_6can.md",
      "https://www.makro.pro/en/p/vwmvjuh-6814746476739",
      "Tier price 83 for 2 or more units"),
    R("D13", "Makro PRO", "direct", "Schweppes Lime Soda Zero Sugar (6 pack)", LL, CAN_READ, 330, 6, 84,
      "sugar-free (name: Zero Sugar)", "unavailable in the area selected", "unavailable",
      "r33_makro_schweppes_lime_zero_unavailable.md",
      "https://www.makro.pro/en/p/899900-7499701616835",
      "Unavailable in the selected area; kept in sensitivity"),
    R("D14", "Makro PRO", "direct", "Singha Sparkling Water Lime (24 pack)", LL, CAN_READ, 330, 24, 312,
      "not confirmed (no sugar text on the extract)", "none on page", "main",
      "r20_makro_singha_sparkling_lime_24can.md",
      "https://www.makro.pro/en/p/699716183874140",
      "List price 319 (-2%)"),
    # ---------------- direct retailer pages (Lotus's Shop Online) ----------------
    R("D15", "Lotus's Shop Online", "direct", "Sprite (single can, 325 mL)", LL, CAN_STATED, 325, 1, 16,
      "regular (sugar not stated)", "none on page", "main",
      "r08_lotuss_sprite_325_single_can.md",
      "https://shopping.lotuss.com/th/product/sprite-lemonlime-flavour-soft-drink-325ml-238945",
      "Single can, price per Each"),
    R("D16", "Lotus's Shop Online", "direct", "Sprite (6 pack, 325 mL)", LL, CAN_READ, 325, 6, 85,
      "regular (sugar not stated)", "none on page", "main",
      "r07_lotuss_sprite_325_6can.md",
      "https://www.lotuss.com/en/product/sprite-lemonlime-flavour-soft-drink-325ml-x-6pcs-6808557",
      "Buy 2 for 156; the same retailer's single 325 mL Sprite listing says can (กระป๋อง); price read as pack price"),
    R("D17", "Lotus's Shop Online", "direct", "Sprite (24 can pack, 325 mL)", LL, CAN_STATED, 325, 24, 332,
      "regular (sugar not stated)", "none on page", "main",
      "r21_lotuss_sprite_325_24can.md",
      "https://www.lotuss.com/en/product/sprite-soft-drink-original-325ml-x-24pcs-clubpack-150033088",
      "Member price 315 (used in member-or-tier sensitivity); price read as pack price"),
    R("D18", "Lotus's Shop Online", "direct", "Sprite Chill Lemon Mint (single, 325 mL)", LL, CAN_READ, 325, 1, 17,
      "not stated", "none on page", "main",
      "r34_lotuss_sprite_chill_lemon_mint_single.md",
      "https://www.lotuss.com/en/product/75714334",
      "Single unit; container not stated on the page"),
    R("D19", "Lotus's Shop Online", "direct", "7UP Zero Sugar Lemon Soda (6 pack, 325 mL)", LL, CAN_READ, 325, 6, 75,
      "sugar-free (name: ZERO SUGAR)", "none on page", "main",
      "r09_lotuss_7up_zero_325_6can.md",
      "https://www.lotuss.com/en/product/171266560",
      "List price 80 (-6%); container not stated on the page"),
    R("D20", "Lotus's Shop Online", "direct", "Singha Lemon Soda (single can)", LL, CAN_STATED, 330, 1, 17,
      "sugar-free (maker page: 0% sugar)", "none on page", "main",
      "r10_lotuss_singha_lemon_single_can.md",
      "https://www.lotuss.com/en/product/singha-lemon-soda-zero-sugar-lemon-soda-330ml-50986847",
      "Single can; a second read of the same page on this pass gave the same 17.00"),
    R("D21", "Lotus's Shop Online", "direct", "Singha Lemon Soda (6 pack)", LL, CAN_STATED, 330, 6, 85,
      "sugar-free (maker page: 0% sugar)", "none on page", "main",
      "r06_lotuss_singha_lemon_6can.md",
      "https://www.lotuss.com/en/product/singha-lemon-soda-can-330ml-6-51109221",
      "Member price 81 (used in member-or-tier sensitivity); price read as pack price"),
    R("D22", "Lotus's Shop Online", "direct", "Singha Lemon Soda (24 can pack)", LL, CAN_STATED, 330, 24, 330,
      "sugar-free (maker page: 0% sugar)", "none on page", "main",
      "r05_lotuss_singha_lemon_24can.md",
      "https://www.lotuss.com/en/product/169912032",
      "Shown as 330.00 per Each; read as pack price (a per can reading would be implausible)"),
    R("D23", "Lotus's Shop Online", "direct", "Schweppes Manao lime soda (single can, 330 cc)", LL, CAN_READ, 330, 1, 18,
      "regular (sugar not stated)", "none on page", "main",
      "r11_lotuss_schweppes_manao_lime_single.md",
      "https://shopping.lotuss.com/en/product/schweppes-soft-drink-lime-soda-330ml-single-6709516",
      "Priceza row for the same code shows 17 (conflict; the page read is used)"),
    R("D24", "Lotus's Shop Online", "direct", "Schweppes Soda Water (6 pack, 330 mL)", SW, CAN_READ, 330, 6, 88,
      "plain soda water (" + S_NO + ")", "none on page", "main",
      "r12_lotuss_schweppes_soda_water_6can.md",
      "https://www.lotuss.com/en/product/schweppes-sparkling-soda-water-330ml-x-6-cans-75162024",
      "Shown as 88.00 per Each; read as pack price"),
    # ---------------- aggregator rows (Priceza listings; merchant prices, S) ----------------
    R("A01", "Tops Online (via Priceza)", "aggregator", "Sprite (24 pack, 325 mL)", LL, CAN_STATED, 325, 24, 332,
      "regular (sugar not stated)", "not stated on listing", "main",
      "r26_priceza_sprite_product_tops_lazmall_makro.md",
      "https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813",
      "Tops listing 8851959232361; Tops itself returned HTTP 403 on this pass"),
    R("A02", "Coca-Cola Official Store, LazMall (via Priceza)", "aggregator", "Sprite No Sugar (24 can pack, 325 mL)", LL, CAN_STATED, 325, 24, 334,
      "sugar-free (name: สูตรไม่มีน้ำตาล)", "not stated on listing", "main",
      "r22_priceza_sprite_listing.md",
      "https://www.priceza.com/b/groceries/น้ำอัดลม/sprite",
      "Was 384 on the listing"),
    R("A03", "Coca-Cola Official Store, LazMall (via Priceza)", "aggregator", "Sprite (6 can pack, 325 mL)", LL, CAN_STATED, 325, 6, 96,
      "regular (sugar not stated)", "not stated on listing", "main",
      "r22_priceza_sprite_listing.md",
      "https://www.priceza.com/b/groceries/น้ำอัดลม/sprite",
      "Listing row 11"),
    R("A04", "Suntory PepsiCo official store, LazMall (via Priceza)", "aggregator", "7UP No Sugar lemon soda (24 can pack, 325 mL)", LL, CAN_STATED, 325, 24, 293,
      "sugar-free (name: ไม่มีน้ำตาล)", "not stated on listing", "main",
      "r23_priceza_7up_listing.md",
      "https://www.priceza.com/s/ราคา/เซเว่นอัพ",
      "Was 384 on the listing"),
    R("A05", "Suntory PepsiCo official store, LazMall (via Priceza)", "aggregator", "7UP No Sugar lemon soda (12 can pack, 325 mL)", LL, CAN_STATED, 325, 12, 161,
      "sugar-free (name: ไม่มีน้ำตาล)", "not stated on listing", "main",
      "r23_priceza_7up_listing.md",
      "https://www.priceza.com/s/ราคา/เซเว่นอัพ",
      "Was 192 on the listing"),
    R("A06", "Suntory PepsiCo official store, LazMall (via Priceza)", "aggregator", "7UP No Sugar lemon soda (6 can pack, 325 mL)", LL, CAN_STATED, 325, 6, 96,
      "sugar-free (name: ไม่มีน้ำตาล)", "not stated on listing", "main",
      "r23_priceza_7up_listing.md",
      "https://www.priceza.com/s/ราคา/เซเว่นอัพ",
      "Listing row 21"),
    R("A07", "Coca-Cola Official Store, LazMall (via Priceza)", "aggregator", "Schweppes Lime Soda Zero (24 can pack, 330 mL)", LL, CAN_STATED, 330, 24, 351,
      "sugar-free (name: สูตรไม่มีน้ำตาล)", "not stated on listing", "main",
      "r24_priceza_schweppes_listing.md",
      "https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา",
      "Was 404; delivery limited to Bangkok metro, Nonthaburi and Chonburi"),
    R("A08", "Coca-Cola Official Store, LazMall (via Priceza)", "aggregator", "Schweppes Lime Soda Zero (12 can pack, 330 mL)", LL, CAN_STATED, 330, 12, 196,
      "sugar-free (name: สูตรไม่มีน้ำตาล)", "not stated on listing", "main",
      "r24_priceza_schweppes_listing.md",
      "https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา",
      "Listing row 15"),
    R("A09", "LazMall, Lazada Mall seller (via Priceza)", "aggregator", "Sprite Lemon Plus Zero Sugar (24 can pack, 325 mL)", LL, CAN_STATED, 325, 24, 332,
      "sugar-free (name: สูตรไม่มีน้ำตาล; 2022 Thaiger article: sugar-free)", "not stated on listing", "main",
      "r26_priceza_sprite_product_tops_lazmall_makro.md",
      "https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813",
      "Listing 16105459253; seller is a Lazada Mall seller, not named as the brand's own store; 2022 Thaiger article gives THB 15 (r27)"),
    R("A11", "Lotus's Shop Online (via Priceza)", "aggregator", "7UP No Sugar lemon soda (single can, 325 mL)", LL, CAN_READ, 325, 1, 16,
      "sugar-free (name: ไม่มีน้ำตาล)", "not stated on listing", "main",
      "r23_priceza_7up_listing.md",
      "https://www.priceza.com/s/ราคา/เซเว่นอัพ",
      "Listing row 4; container not stated"),
    R("A12", "Lotus's Shop Online (via Priceza)", "aggregator", "Schweppes Lime Soda Zero (12 pack, 330 mL)", LL, CAN_READ, 330, 12, 167,
      "sugar-free (name: สูตรไม่มีน้ำตาล)", "not stated on listing", "main",
      "r24_priceza_schweppes_listing.md",
      "https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา",
      "Listing row 5; container not stated"),
    R("A13", "Lotus's Shop Online (via Priceza)", "aggregator", "Schweppes Lime Soda (6 pack, 330 mL)", LL, CAN_READ, 330, 6, 85,
      "regular (sugar not stated)", "not stated on listing", "main",
      "r24_priceza_schweppes_listing.md",
      "https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา",
      "Listing row 6; container not stated"),
    R("A14", "Lotus's Shop Online (via Priceza)", "aggregator", "Schweppes Lime Soda no sugar (6 pack, 330 mL)", LL, CAN_READ, 330, 6, 85,
      "sugar-free (name: สูตรไม่มีน้ำตาล)", "not stated on listing", "main",
      "r24_priceza_schweppes_listing.md",
      "https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา",
      "Listing row 7; container not stated"),
    # ---------------- bottles (outside the can ladder; kept for the soda water table) ----------------
    R("B01", "7-Eleven ALL Online", "direct", "Singha Soda (24 bottles, 325 mL)", SW, BOTTLE, 325, 24, 195,
      "plain soda water (no sugar claim on page)", "in stock (page label)", "bottle",
      "r28_7eleven_singha_soda_24bottle.md",
      "https://www.allonline.7eleven.co.th/p/โซดาสิงห์-325-มล-แพ็ก-24-ขวด/452565/",
      "Bottles; price validity ends 20/10/2026"),
    R("B02", "Makro PRO", "direct", "Singha Soda (24 bottles, 325 mL)", SW, BOTTLE, 325, 24, 190,
      "plain soda water (no sugar claim on page)", "none on page", "bottle",
      "r30_makro_singha_soda_24bottle.md",
      "https://www.makro.pro/en/p/160629-6761215066307",
      "Bottles, 24 x 325 mL"),
    R("B03", "Lotus's Shop Online", "direct", "Singha Soda (6 pack, 325 mL)", SW, UNKNOWN, 325, 6, 48,
      "plain soda water (no sugar claim on page)", "none on page", "excluded",
      "r29_lotuss_singha_soda_6bottle.md",
      "https://www.lotuss.com/en/product/singha-soda-325-ml-6-24183741",
      "Container not stated on the page; the same product is bottled at 7-Eleven and Makro; price shown 48.00 per Each with 52.00 also shown"),
]

EXCLUDED_LISTING_ROWS = [
    X("X01", "Lotus's Shop Online (via Priceza)", "Schweppes lime soda 330 mL single (330CC)", 17,
      "Conflict: the Lotus's product page read on this pass shows 18.00 for the same code; page read used"),
    X("X02", "Coca-Cola Official Store, LazMall (via Priceza)", "Sprite 325 mL x 24 with Halls XS candy", 328,
      "Bundle with candy; not a plain can price"),
    X("X03", "Coca-Cola Official Store, LazMall (via Priceza)", "Sprite No Sugar 325 mL x 24 with Halls XS candy", 328,
      "Bundle with candy; was 413"),
    X("X04", "Coca-Cola Official Store, LazMall (via Priceza)", "Sprite 325 mL x 6 with a free gift", 85,
      "Bundle with a free gift (was 96); not used as a plain can price"),
    X("X05", "Coca-Cola Official Store, LazMall (via Priceza)", "Sprite 325 mL x 24 with Ritz crackers", 438,
      "Bundle with crackers"),
    X("X06", "US Mart (via Priceza)", "Sprite lemon-lime 325 mL x 6 cans", 125,
      "Seller not an official store; price about half the official listing (was 250)"),
    X("X07", "CR7 ManU (via Priceza)", "Sprite no sugar lemon-lime 325 mL x 6 cans", 120,
      "Seller not an official store"),
    X("X08", "CR7 ManU (via Priceza)", "Sprite lemon-lime no sugar 325 mL x 24 cans", 456,
      "Seller not an official store"),
    X("X09", "Fresh Mart (via Priceza)", "Sprite No Sugar 325 mL x 24 cans", 414,
      "Seller named as Fresh Mart; not verified as CP Fresh Mart; was 828"),
    X("X10", "Fresh Mart (via Priceza)", "Sprite lemon-lime 325 mL x 24 cans", 442,
      "Seller named as Fresh Mart; not verified as CP Fresh Mart; was 884"),
    X("X11", "Makro PRO (via Priceza)", "Sprite 325 mL x 24 cans (second Makro SKU)", 315,
      "Second Makro listing; not opened on its own page"),
    X("X12", "Suntory PepsiCo, LazMall (via Priceza)", "7UP No Sugar 325 mL, three packs of 24", 869,
      "Three-pack total (title says x3); not a single pack price"),
    X("X13", "MV Siam (via Priceza)", "7UP Free Fiber 325 mL x 6 cans", 211,
      "Fibre variant; seller not official"),
    X("X14", "Seller not named (via Priceza)", "7UP Special Set with fibre 325 mL x 6 cans", 218,
      "Bundle; seller not named"),
    X("X15", "Lotus's Shop Online (via Priceza)", "7UP No Sugar pineapple-peach 325 mL single", 16,
      "Flavour outside lemon, lime or clear"),
    X("X16", "Lotus's Shop Online (via Priceza)", "7UP No Sugar pineapple-peach 325 mL x 6", 75,
      "Flavour outside lemon, lime or clear"),
    X("X17", "Lotus's Shop Online (via Priceza)", "7UP strawberry-lemon 325 mL single", 16,
      "Flavour outside lemon, lime or clear"),
    X("X18", "Lotus's Shop Online (via Priceza)", "7UP strawberry-lemon 325 mL x 6", 75,
      "Flavour outside lemon, lime or clear"),
    X("X19", "Various Lazada and Shopee sellers (via Priceza)", "7UP No Sugar 345 mL (single, x 12 bottles, x 12)", 142,
      "345 mL is in range, but the containers are bottles (ขวด) or not stated; sellers not official; excluded"),
    X("X20", "Various Lazada sellers (via Priceza)", "Schweppes lime soda 330 mL singles (4 listings)", 18,
      "Non-official sellers; singles at 18.62 to 38; not used"),
    X("X21", "Polomane Co. Ltd (via Priceza)", "Schweppes lime soda 330 mL x 6", 142,
      "Seller not an official store"),
    X("X22", "CR7 Academy (via Priceza)", "Schweppes lime soda no sugar 330 mL x 12", 252,
      "Seller not an official store; per can 21"),
    X("X23", "Coca-Cola Official Store, LazMall (via Priceza)", "Schweppes lime soda 330 mL x 12 (no sugar wording in name)", 196,
      "Sugar status unclear: no sugar wording in the name; same price as the zero 12 pack (A08); not used"),
    X("X24", "Various sellers (via Priceza)", "Schweppes Sparkling Manao Soda 330 mL (grouped, 11 offers)", 82,
      "Range of 82 to 325 across 11 offers; not one price"),
    X("X25", "Coolzashop.Selection (via Priceza)", "Schweppes soda with blueberry or raspberry flavour, single cans", 16,
      "Flavours outside lemon, lime or clear"),
    X("X26", "Various (via Priceza)", "Sprite 250 mL, 450 mL and 500 mL bottles", 214,
      "Out of size range and bottles"),
    X("X27", "Shopee seller (via Priceza)", "7UP No Sugar 440 mL", 14,
      "Out of size range"),
    X("X28", "Soda Inter (via Priceza)", "7Up Zero Sugar 355 mL (imported) and 7UP tropical 355 mL", 75,
      "355 mL is outside 325 to 345 mL"),
    X("X29", "Various (via Priceza)", "7UP Slim Can 245 mL x 6", 250,
      "Out of size range"),
]


def derive(r):
    pp = Decimal(r["pack_price_thb"])
    n = Decimal(r["pack_count"])
    cm = Decimal(r["can_ml"])
    per_can = pp / n
    per330 = per_can * SERVE_ML / cm
    d = dict(r)
    d["per_can_thb"] = float(q2(per_can))
    d["per_330ml_thb"] = float(q2(per330))
    d["per_litre_thb"] = float(q2(per_can / (cm / Decimal(1000))))
    d["_p330"] = q2(per330)
    return d


def with_price(r, price):
    s = dict(r)
    s["pack_price_thb"] = price
    return derive(s)


def ladder(rs):
    vals = sorted(r["_p330"] for r in rs)
    med = q2(statistics.median(vals))
    return {"n": len(vals), "min": float(vals[0]), "median": float(med), "max": float(vals[-1]),
            "row_ids": [r["id"] for r in rs]}


def position(rs, x=CUBE_SHELF):
    vals = [r["_p330"] for r in rs]
    n = len(vals)
    below = sum(1 for v in vals if v < x)
    eq = sum(1 for v in vals if v == x)
    above = sum(1 for v in vals if v > x)
    return {"x_thb": float(x), "n": n, "below": below, "equal": eq, "above": above,
            "share_at_or_below": round((below + eq) / n, 3)}


def cmp(label, can_val):
    cv = Decimal(str(can_val))
    diff = CUBE_SHELF - cv
    pct = (CUBE_SHELF / cv - 1) * 100
    return {"label": label, "can_per_330ml_thb": float(q2(cv)),
            "cube_minus_can_thb": float(q2(diff)),
            "cube_vs_can_pct": float(pct.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))}


def main():
    rows = [derive(r) for r in ROWS]
    by_id = {r["id"]: r for r in rows}
    main_rows = [r for r in rows if r["use"] == "main"]
    anomaly = [r for r in rows if r["use"] == "anomaly"]
    unavailable = [r for r in rows if r["use"] == "unavailable"]

    MT = {"D09": 78, "D21": 81, "D17": 315, "D12": 83}
    main_mt = [with_price(r, MT[r["id"]]) if r["id"] in MT else r for r in main_rows]

    sets = {
        "main_all": main_rows,
        "main_direct": [r for r in main_rows if r["channel"] == "direct"],
        "main_aggregator": [r for r in main_rows if r["channel"] == "aggregator"],
        "main_lemon_lime_or_lime_only": [r for r in main_rows if r["group"] == LL],
        "main_plain_soda_water": [r for r in main_rows if r["group"] == SW],
        "main_singles": [r for r in main_rows if r["pack_count"] == 1],
        "main_multipacks": [r for r in main_rows if r["pack_count"] > 1],
        "main_24_can_packs": [r for r in main_rows if r["pack_count"] == 24],
        "main_singha_lemon_soda": [r for r in main_rows if r["product"].startswith("Singha Lemon Soda")],
        "main_singha_lemon_soda_multipacks": [r for r in main_rows if r["product"].startswith("Singha Lemon Soda") and r["pack_count"] > 1],
        "main_sugar_free": [r for r in main_rows if r["sugar_status"].startswith("sugar-free")],
        "main_container_stated_only": [r for r in main_rows if r["container"] == CAN_STATED],
        "main_member_or_tier_prices": main_mt,
        "sens_main_plus_7eleven_6pack_anomalies": main_rows + anomaly,
        "sens_main_plus_unavailable_rows": main_rows + unavailable,
    }
    ladders = {k: ladder(v) for k, v in sets.items()}

    pos = {k: position(v) for k, v in sets.items()}

    sing_multi = ladders["main_singha_lemon_soda_multipacks"]["median"]
    cube_vs = [
        cmp("Singha Lemon Soda, median of multipacks (main)", sing_multi),
        cmp("Singha Lemon Soda, single can (Lotus's)", by_id["D20"]["_p330"]),
        cmp("Singha Lemon Soda 24 can pack (7-Eleven)", by_id["D01"]["_p330"]),
        cmp("Singha Sparkling Water Lime 24 can pack (7-Eleven)", by_id["D05"]["_p330"]),
        cmp("Main ladder median (all 32 rows)", ladders["main_all"]["median"]),
        cmp("Main 24 can pack median", ladders["main_24_can_packs"]["median"]),
        cmp("Main singles median", ladders["main_singles"]["median"]),
    ]

    conflicts = [
        "Deck competitor strip (rework/deck/deck_content.md, the line that reads Sprite 24 pack about THB 15.2 a can, Lazada listing, undated): the dated 20 October 2026 reads give 13.83 to 14.13 a can for the 325 mL Sprite and Sprite No Sugar 24 packs (Lotus's 332, Tops 332, Coca-Cola Official Store 334). The deck figure is older and undated; it should be replaced.",
        "Deck competitor strip: Schweppes zero sugar 330 mL variants are described as 'price not found'. This pass finds Schweppes Lime Soda Zero at THB 170 for 6 cans at 7-Eleven (page read), THB 351 for 24 cans and THB 196 for 12 cans at the Coca-Cola Official Store on LazMall (Priceza listings).",
        "Deck competitor strip: Sprite Lemon Plus THB 15 (2022) is confirmed by the Thaiger article of 29 August 2022 (r27). A 2026 Sprite Lemon Plus Zero Sugar 24 can listing on LazMall reads THB 332 (14.05 per 330 mL serve, Priceza, S).",
        "Lotus's Schweppes lime soda 330 mL single: Lotus's product page reads THB 18.00 (r11); the Priceza row for the same product code reads THB 17. The page read is used.",
        "Makro Sprite 330 mL 12 pack: the Makro page gives THB 137 and THB 135 (tier); the page does not state the container, and Priceza shows 330 mL Sprite 12 packs as bottles. The row is excluded.",
        "7-Eleven 6 can rows (Singha Lemon Soda THB 172; Schweppes Lime Soda Zero THB 170) read about twice the per can price of the same retailer's 24 can packs and of the 6 can packs at Makro and Lotus's. The pages give no explanation. They are excluded from the main ladder and shown in a sensitivity set.",
    ]

    limits = [
        "Big C (bigc.co.th), Tops Online (tops.co.th) and Foodland (foodland.co.th) returned HTTP 403 on this pass. No direct figure from these three retailers is used. Tops appears only through a Priceza listing and product page (S).",
        "CP Fresh Mart: not read on this pass. The Fresh Mart rows on Priceza are not verified as CP Fresh Mart and are excluded (X09, X10).",
        "7-Eleven ALL Online's own search page reports 'function unavailable' (technical problem), so 7UP and Sprite cannot be listed there directly. The 7-Eleven rows used are product pages found through Priceza and earlier reads.",
        "Shopee and Lazada search pages were not read directly on this pass; Lazada Mall and Coca-Cola, Suntory PepsiCo and Singha stores are used only through Priceza listings (S).",
        "Retailer pages were read through WebFetch summaries (a small model extracts the page text). The extracts are not verbatim copies, and some pages showed 'Loading' blocks. Per unit and 'Each' labels on Lotus's pages are ambiguous; the pack reading is DERIVED and is stated in each raw file.",
        "Price validity: the 7-Eleven pages print validity dates ending 20 October 2026 (the day of this read). The prices may change after this date.",
        "House brands: no 2026 Thai shelf price for a house-brand lemon or lime soda can was found by search or on the retailer pages read.",
        "Sprite Chill container: the Coca-Cola media-centre page returned HTTP 403, so the can size of Sprite Chill Lemon Mint (D08, D18) is not confirmed on a readable page; read as a can.",
        "Sprite Lemon Plus 2026 price: found only on a Priceza listing for a LazMall seller (A09, S). No 2026 retailer's own page for Sprite Lemon Plus was read.",
        "Sugar status: for Singha Lemon Soda it rests on the maker's page (P, read through an extract, copyright footer 2020). For other rows the sugar status is what the page name or claim says; 'not stated' means the page does not say.",
        "Competitor financials are outside this task (T2 to T4).",
    ]

    result = {
        "task": "T5 retail price ladder: lemon, lime and clear carbonated soft drinks and soda waters, 325 to 345 mL cans, Thailand",
        "date_read": DATE,
        "method": ("Per can = pack price / pack count. Per 330 mL serve = per can x 330 / can mL (325 mL cans scaled to 330 mL). "
                   "Main ladder: direct retailer pages and Priceza listing rows for cans in lemon, lime or plain soda water flavours, "
                   "from named retailers or brand official stores, with no bundles, no out-of-stock or unavailable rows, "
                   "and no 7-Eleven 6 can anomalies. Sensitivity sets add the anomalies, add the unavailable rows, restrict to "
                   "rows whose container is stated, and apply member or tier prices. Rounding is ROUND_HALF_UP to 0.01. "
                   "No random numbers; no seed."),
        "cube": {"shelf_price_thb_per_330ml_serve": float(CUBE_SHELF),
                 "tier": "ASSUMPTION (planning shelf price in the deck base case; not a retail price)",
                 "per_litre_thb": float(q2(CUBE_SHELF / (SERVE_ML / Decimal(1000))))},
        "rows": [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows],
        "excluded_listing_rows": EXCLUDED_LISTING_ROWS,
        "sets": {k: {"ladder_per_330ml_thb": ladders[k], "position_of_thb15": pos[k]} for k in sets},
        "cube_vs_can_per_serve": cube_vs,
        "conflicts": conflicts,
        "limits": limits,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print("rows:", len(rows), "main:", len(main_rows), "anomaly:", len(anomaly), "unavailable:", len(unavailable))
    for k in sets:
        L = ladders[k]
        P = pos[k]
        print("%-40s n=%2d min=%.2f median=%.2f max=%.2f | THB15 at-or-below %d/%d (%.3f)" % (
            k, L["n"], L["min"], L["median"], L["max"], P["below"] + P["equal"], P["n"], P["share_at_or_below"]))
    for c in cube_vs:
        print(c)


if __name__ == "__main__":
    main()
