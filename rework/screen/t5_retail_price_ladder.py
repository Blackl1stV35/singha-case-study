"""T5 retail price ladder: lemon, lime and clear carbonated cans and soda waters, 325 to 345 mL.

Check step (runs first, for every row, before any figure is computed):
  1. the row's anchor (a URL, a Priceza listing number, or a product name as printed) must occur in its
     saved raw file under rework/raw/diligence_2026-10-20/T5/;
  2. within WINDOW characters after (or BEFORE characters before) an occurrence of the anchor, the printed pack
     price must appear with its currency mark (baht sign or THB);
  3. where the page prints a per-unit price, that figure must appear in the same window, and it must agree
     with pack price / pack count to within half a satang.
This is a presence check on the saved extract, not a parse of the page. A failed check stops the script.
A failure can also mean that the extract dropped a label, so the failure is reported and nothing is computed.
The matched text for every row is written to the results file for inspection.

Compute step (after every row passes):
  Per can = pack price / pack count.
  Per 330 mL = per can x 330 / can mL (325 mL cans are scaled by 330/325).
  Per litre = per can / can litres.
  Statistics: Python statistics module, inclusive quartiles. No random numbers are used, so there is no seed.

Output: rework/screen/t5_retail_price_ladder_results.json. Run with: python -I t5_retail_price_ladder.py
"""
import json
import os
import re
import statistics
from decimal import Decimal, ROUND_HALF_UP

ROOT = r"D:\Workspace\singha-case-study"
RAW_DIR = os.path.join(ROOT, "rework", "raw", "diligence_2026-10-20", "T5")
OUT = os.path.join(ROOT, "rework", "screen", "t5_retail_price_ladder_results.json")

CUBE_SHELF_PRICE_THB = 15.0   # ASSUMPTION in the submission model (base 15; range 10 to 20)
SERVE_ML = 330.0
WINDOW = 900                  # characters after an anchor occurrence that must hold the printed price
BEFORE = 200                  # characters before an anchor that may hold the printed price (table rows put price first)
DATE = "2026-10-20"

R7 = "t5_recheck_7eleven_allonline_2026-10-20.md"
RM = "t5_recheck_makro_pro_2026-10-20.md"
RL = "t5_recheck_lotuss_2026-10-20.md"
RZ = "t5_recheck_lazada_priceza_2026-10-20.md"
RZ2 = "t5_recheck2_priceza_7up_listing_2026-10-20.md"
RB = "t5_recheck_brands_press_2026-10-20.md"
RX = "t5_recheck3_live_checks_2026-10-20.md"   # live re-reads of 20 October 2026 and the 18 October Tops capture copy

# Group: main = set A (the main ladder); single = single-can set; sens = sensitivity only;
# excluded = bottles, kept for reference and in no can ladder.


def R(**kw):
    d = dict(unit=None, price_pattern=None, anchor=None, note="", exclude_reason="", stock="", sens=[], date=DATE)
    d.update(kw)
    d["pack_price_thb"] = float(d["price"])
    if d["anchor"] is None:
        d["anchor"] = d["url"]
    return d


ROWS = [
    # ---- Direct: retailer product pages (7-Eleven ALL Online, Makro PRO, Lotus's Shop Online) ----
    R(id="D01", group="main", channel="direct", retailer="7-Eleven ALL Online", brand="Singha",
      product="Singha Lemon Soda 330 mL, case of 24 cans", flavour="lemon", size_ml=330, pack_count=24,
      price="330", container="can", container_status="stated",
      sugar="sugar-free (maker page: 0% sugar; retailer page: no sugar claim)", tier="S",
      url="https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-ยกลัง-24-กระป๋อง/474313/", raw=R7,
      stock="in stock (page label)", note="second price 408 read as the earlier price (-19%)"),
    R(id="D02", group="main", channel="direct", retailer="7-Eleven ALL Online", brand="Singha",
      product="Singha Lemon Soda 330 mL, pack of 6 cans", flavour="lemon", size_ml=330, pack_count=6,
      price="172", container="can", container_status="stated", sugar="sugar-free (maker page)", tier="S",
      url="https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-แพ็ก-6-กระป๋อง/514221/", raw=R7,
      stock="in stock (page label)",
      note="per can 28.67 is about twice the same retailer's 24-can price per can (13.75); page gives no cause; outlier test"),
    R(id="D03", group="main", channel="direct", retailer="7-Eleven ALL Online", brand="Schweppes",
      product="Schweppes Lime Soda Zero 330 mL, pack of 6 cans", flavour="lime", size_ml=330, pack_count=6,
      price="170", container="can", container_status="stated",
      sugar="sugar-free (page: สูตรไม่มีน้ำตาล, sugar-free formula)", tier="S",
      url="https://www.allonline.7eleven.co.th/p/ชเวปส์มะนาวโซดาซีโร่-330มล-แพ็ก-6-กระป๋อง/354988/", raw=R7,
      stock="in stock (page label)",
      note="second price 190 (-11%); per can 28.33, outlier test; price validity ends 20 Oct 2026"),
    R(id="D04", group="main", channel="direct", retailer="7-Eleven ALL Online", brand="Singha",
      product="Singha Sparkling Water Lime 330 mL, case of 24 cans", flavour="lime", size_ml=330, pack_count=24,
      price="302", container="can", container_status="stated",
      sugar="not stated on retailer page (0% calorie claim only); company claim relayed by press: sugar-free (S)",
      tier="S",
      url="https://www.allonline.7eleven.co.th/p/สิงห์สปาร์คกลิ้งไลม์-330-มล-ยกลัง-24-กระป๋อง/327253/", raw=R7,
      stock="in stock (page label)", note="second price 304 (-1%); launch price THB 15 per Kaohoon, 17 March 2026 (S)"),
    R(id="D05", group="main", channel="direct", retailer="Makro PRO", brand="Sprite",
      product="Sprite Soft Drink Lemon Lime 325 mL, pack of 24 (SKU 179712)", flavour="lemon-lime", size_ml=325,
      pack_count=24, price="311", unit="12.96", container="can", container_status="inferred",
      sugar="not stated (the name does not say regular or no sugar; the page does not say)", tier="S",
      url="https://www.makro.pro/en/p/179712-7078659719363", raw=RM,
      note="list 321 (-3%); container not stated; 325 mL is the Sprite can size per the Coca-Cola Thailand page"),
    R(id="D06", group="main", channel="direct", retailer="Makro PRO", brand="Singha",
      product="SINGHA Lemon Soda 330 mL, 24 cans", flavour="lemon", size_ml=330, pack_count=24,
      price="325", unit="13.54", container="can", container_status="stated",
      sugar="sugar-free (maker page); retailer page: no sugar claim", tier="S",
      url="https://www.makro.pro/en/p/428706-7350275997891", raw=RM,
      note="page shows 325 and 330.00 (-1%); per-unit 13.54; container stated in the page text (24 cans, each 330 ml)"),
    R(id="D07", group="main", channel="direct", retailer="Makro PRO", brand="Singha",
      product="SINGHA Lemon Soda 330 mL, pack of 6", flavour="lemon", size_ml=330, pack_count=6,
      price="82", unit="13.67", container="can", container_status="inferred", sugar="sugar-free (maker page)",
      tier="S", url="https://www.makro.pro/en/p/893947-6814746706115", raw=RM,
      note="82 is the single-pack price (per unit 13.67 = 82/6); Buy 3+ units tier 78 not used; container inferred from product line"),
    R(id="D08", group="main", channel="direct", retailer="Makro PRO", brand="Singha",
      product="SINGHA Sparkling Water Lime 330 mL, 24 units", flavour="lime", size_ml=330, pack_count=24,
      price="312", unit="13.00", container="can", container_status="inferred", sugar="not stated on page", tier="S",
      url="https://www.makro.pro/en/p/699716183874140", raw=RM,
      note="list 319 (-2%); per unit 13.00 = 312/24; three Loading placeholders on the page"),
    R(id="D09", group="sens", channel="direct", retailer="Makro PRO", brand="Sprite",
      product="Sprite Chill Soft Drink Lemon Mint 325 mL, pack of 6", flavour="lemon-mint (flavour variant)",
      size_ml=325, pack_count=6, price="78", unit="13.00", container="can", container_status="inferred",
      sugar="not stated on page", tier="S", url="https://www.makro.pro/en/p/630907-363090727914101", raw=RM,
      sens=["I"],
      exclude_reason="flavour variant: lemon-mint adds a mint flavour, outside plain lemon or lime (rule of set A)",
      note="78 matches per unit 13.00 x 6; list 81 (-3%) not labelled; container inferred; three Loading placeholders"),
    R(id="D10", group="main", channel="direct", retailer="Makro PRO", brand="Schweppes",
      product="Schweppes Soft Drink Lime Soda 330 mL, pack of 6 (regular)", flavour="lime", size_ml=330,
      pack_count=6, price="84", unit="14.00", container="can", container_status="inferred",
      sugar="regular: no zero or no-sugar wording; nutrition panel shows 16 g carbohydrate (basis not stated)",
      tier="S", url="https://www.makro.pro/en/p/vwmvjuh-6814746476739", raw=RM,
      note="Buy 2+ units tier 83 not used; container inferred"),
    R(id="D11", group="main", channel="direct", retailer="Makro PRO", brand="Schweppes",
      product="Schweppes Soda Water 330 mL, 24 units", flavour="plain soda water", size_ml=330, pack_count=24,
      price="341", unit="14.21", container="can", container_status="inferred",
      sugar="plain soda water; no sugar statement on page", tier="S",
      url="https://www.makro.pro/en/p/119581-7416114282691", raw=RM,
      note="soda water, not lemon or lime; Buy 2+ units tier 336 not used"),
    R(id="D12", group="main", channel="direct", retailer="Lotus's Shop Online", brand="Singha",
      product="SINGHA LEMON SODA CAN 330ML. PACK 24", flavour="lemon", size_ml=330, pack_count=24,
      price="330", container="can", container_status="stated",
      sugar="sugar-free (maker page); retailer page: no sugar claim", tier="S",
      url="https://www.lotuss.com/en/product/169912032", raw=RL,
      note="unit label '/Each'; 330 read as the pack price (DERIVED; per-can reading implausible)"),
    R(id="D13", group="main", channel="direct", retailer="Lotus's Shop Online", brand="Singha",
      product="SINGHA LEMON SODA CAN 330ML.X6", flavour="lemon", size_ml=330, pack_count=6, price="85",
      container="can", container_status="stated", sugar="sugar-free (maker page)", tier="S",
      url="https://www.lotuss.com/en/product/singha-lemon-soda-can-330ml-6-51109221", raw=RL,
      note="unit label '/Each'; 85 read as the six-pack price (DERIVED); club price 81 not used"),
    R(id="D14", group="main", channel="direct", retailer="Lotus's Shop Online", brand="Sprite",
      product="SPRITE CAN 325 ML. PACK 24 (clubpack)", flavour="lemon-lime", size_ml=325, pack_count=24,
      price="332", container="can", container_status="stated", sugar="not stated on page (the name does not say regular or no sugar)", tier="S",
      url="https://www.lotuss.com/en/product/sprite-soft-drink-original-325ml-x-24pcs-clubpack-150033088", raw=RL,
      note="unit label '/Each' read as pack price (DERIVED); club price 315 not used"),
    R(id="D15", group="main", channel="direct", retailer="Lotus's Shop Online", brand="Sprite",
      product="SPRITE 325 ML.X6", flavour="lemon-lime", size_ml=325, pack_count=6, price="85",
      container="can", container_status="inferred", sugar="not stated on page", tier="S",
      url="https://www.lotuss.com/en/product/sprite-lemonlime-flavour-soft-drink-325ml-x-6pcs-6808557", raw=RL,
      note="'/Each' read as pack price (DERIVED); promotion Buy 2 for 156 not used; container not stated"),
    R(id="D16", group="main", channel="direct", retailer="Lotus's Shop Online", brand="7UP",
      product="7 UP ZERO SUGAR LEMON SODA 325 ML. PACK6", flavour="lemon-lime", size_ml=325, pack_count=6,
      price="75", container="can", container_status="inferred", sugar="zero sugar (name only)", tier="S",
      url="https://www.lotuss.com/en/product/171266560", raw=RL,
      note="second price 80 not labelled; '/Each' read as pack price (DERIVED)"),
    R(id="D17", group="main", channel="direct", retailer="Lotus's Shop Online", brand="Schweppes",
      product="SCHWEPPES SODA WATER 330ML.X6", flavour="plain soda water", size_ml=330, pack_count=6, price="88",
      container="can", container_status="inferred", sugar="plain soda water; no sugar statement", tier="S",
      url="https://www.lotuss.com/en/product/schweppes-sparkling-soda-water-330ml-x-6-cans-75162024", raw=RL,
      note="'/Each' read as pack price (DERIVED); container not stated"),

    # ---- Lazada trending page: seller not shown on the page (group F, sensitivity) ----
    R(id="D18", group="sens", channel="marketplace_unnamed", retailer="Lazada (trending page; seller not shown)",
      brand="Sprite", product="Sprite Soft Drink Original 325 mL, pack of 24 cans", flavour="lemon-lime",
      size_ml=325, pack_count=24, price="365", container="can", container_status="stated",
      sugar="regular by name (no sugar wording)", tier="S",
      url="https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705", raw=RZ,
      anchor="Sprite Soft Drink Original 325ml Pack 24", sens=["F"],
      exclude_reason="seller not shown on the page; set A admits only official or named sellers",
      stock="not shown", note="was 384 (-5%); seller not shown in the later read; a snippet (not opened) showed 354"),
    R(id="D19", group="sens", channel="marketplace_unnamed", retailer="Lazada (trending page; seller not shown)",
      brand="Sprite", product="Sprite Soft Drink No Sugar 325 mL, pack of 24 cans", flavour="lemon-lime",
      size_ml=325, pack_count=24, price="365", container="can", container_status="stated",
      sugar="no sugar (name)", tier="S",
      url="https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705", raw=RZ,
      anchor="Sprite Soft Drink No Sugar 325ml Pack 24", sens=["F"],
      exclude_reason="seller not shown on the page; set A admits only official or named sellers",
      stock="not shown", note="was 384 (-5%); seller not shown in the later read"),

    # ---- Priceza aggregator offers (tier S; merchant prices that Priceza does not guarantee) ----
    R(id="A01", group="main", channel="aggregator", retailer="Coca-Cola Official Store, LazMall (via Priceza)",
      brand="Sprite", product="Sprite Lemon Plus Zero Sugar 325 mL, pack of 24 cans", flavour="lemon-lime (lemon variant)",
      size_ml=325, pack_count=24, price="332", container="can", container_status="stated",
      sugar="sugar-free (name: สูตรไม่มีน้ำตาล)", tier="S",
      url="https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813", raw=RZ,
      anchor="16105459253", stock="not shown",
      note="the only 2026 retail price for Sprite Lemon Plus found; listing 16105459253"),
    R(id="A02", group="main", channel="aggregator", retailer="Tops Online (via Priceza)", brand="Sprite",
      product="Sprite 325 mL, pack of 24", flavour="lemon-lime", size_ml=325, pack_count=24, price="332",
      container="can", container_status="inferred", sugar="regular (no sugar wording)", tier="S",
      url="https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813", raw=RZ,
      anchor="8851959232361", stock="not shown",
      note="Tops Online page itself returned HTTP 403; price read from Priceza only"),
    R(id="A03", group="main", channel="aggregator", retailer="Coca-Cola Official Store, LazMall (via Priceza)",
      brand="Sprite", product="Sprite No Sugar 325 mL, pack of 24 cans", flavour="lemon-lime", size_ml=325,
      pack_count=24, price="334", container="can", container_status="stated", sugar="no sugar (name)", tier="S",
      url="https://www.priceza.com/b/groceries/น้ำอัดลม/sprite", raw=RZ, anchor="3988892697", stock="not shown",
      note="was 384"),
    R(id="A04", group="main", channel="aggregator", retailer="Coca-Cola Official Store, LazMall (via Priceza)",
      brand="Sprite", product="Sprite Soft Drink Original 325 mL, pack of 6 cans", flavour="lemon-lime", size_ml=325,
      pack_count=6, price="96", container="can", container_status="stated", sugar="regular (name)", tier="S",
      url="https://www.priceza.com/b/groceries/น้ำอัดลม/sprite", raw=RZ, anchor="3988850987", stock="not shown",
      note="no higher figure shown"),
    R(id="A05", group="main", channel="aggregator", retailer="Suntory PepsiCo, LazMall (via Priceza)",
      brand="7UP", product="7UP No Sugar lemon soda 325 mL, pack of 24 cans", flavour="lemon-lime", size_ml=325,
      pack_count=24, price="293", container="can", container_status="stated", sugar="no sugar (name)", tier="S",
      url="https://www.priceza.com/s/ราคา/เซเว่นอัพ", raw=RZ2, anchor="21448428679", stock="not shown",
      note="was 384 (inferred by the extract); Suntory PepsiCo in LazMall (brand owner's seller account; no official-store label in the extract)"),
    R(id="A06", group="main", channel="aggregator", retailer="Suntory PepsiCo, LazMall (via Priceza)",
      brand="7UP", product="7UP No Sugar lemon soda 325 mL, pack of 12 cans", flavour="lemon-lime", size_ml=325,
      pack_count=12, price="161", container="can", container_status="stated", sugar="no sugar (name)", tier="S",
      url="https://www.priceza.com/s/ราคา/เซเว่นอัพ", raw=RZ2, anchor="21448460740", stock="not shown",
      note="was 192 (inferred); official-store label shown on this listing"),
    R(id="A07", group="main", channel="aggregator", retailer="Suntory PepsiCo, LazMall (via Priceza)",
      brand="7UP", product="7UP No Sugar lemon soda 325 mL, pack of 6 cans", flavour="lemon-lime", size_ml=325,
      pack_count=6, price="96", container="can", container_status="stated", sugar="no sugar (name)", tier="S",
      url="https://www.priceza.com/s/ราคา/เซเว่นอัพ", raw=RZ2, anchor="21448401884", stock="not shown",
      note="no was-price shown"),
    R(id="A08", group="main", channel="aggregator", retailer="Coca-Cola Official Store, LazMall (via Priceza)",
      brand="Schweppes", product="Schweppes lime soda no sugar 330 mL, pack of 12 cans", flavour="lime", size_ml=330,
      pack_count=12, price="196", container="can", container_status="stated", sugar="no sugar (name)", tier="S",
      url="https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", raw=RZ, anchor="10615542238", stock="not shown",
      note="no higher figure"),
    R(id="A09", group="main", channel="aggregator", retailer="Coca-Cola Official Store, LazMall (via Priceza)",
      brand="Schweppes", product="Schweppes lime soda 330 mL, pack of 12 cans (regular)", flavour="lime", size_ml=330,
      pack_count=12, price="196", container="can", container_status="stated", sugar="regular (no sugar wording)",
      tier="S", url="https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", raw=RZ, anchor="10247417739",
      stock="not shown", note="no higher figure"),
    R(id="A10", group="main", channel="aggregator", retailer="Coca-Cola Official Store, LazMall (via Priceza)",
      brand="Schweppes", product="Schweppes lime soda no sugar 330 mL, pack of 24 cans", flavour="lime", size_ml=330,
      pack_count=24, price="351", container="can", container_status="stated", sugar="no sugar (name)", tier="S",
      url="https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", raw=RZ, anchor="10615452638", stock="not shown",
      note="was 404; delivery limited to Bangkok, Nonthaburi and Chonburi"),
    R(id="A11", group="main", channel="aggregator", retailer="Lotus's Shop Online (via Priceza)",
      brand="Schweppes", product="Schweppes lime soda no sugar 330 mL, pack of 12", flavour="lime", size_ml=330,
      pack_count=12, price="167", container="can", container_status="inferred", sugar="no sugar (name)", tier="S",
      url="https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", raw=RZ, anchor="165851607", stock="not shown",
      note="no higher figure"),
    R(id="A12", group="main", channel="aggregator", retailer="Lotus's Shop Online (via Priceza)",
      brand="Schweppes", product="Schweppes lime soda 330CC, pack of 12 (regular)", flavour="lime", size_ml=330,
      pack_count=12, price="167", container="can", container_status="inferred", sugar="regular (no sugar wording)",
      tier="S", url="https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", raw=RZ, anchor="165851599", stock="not shown",
      note="no higher figure"),
    R(id="A13", group="main", channel="aggregator", retailer="Lotus's Shop Online (via Priceza)",
      brand="Schweppes", product="Schweppes lime soda 330 mL, six-pack (regular)", flavour="lime", size_ml=330,
      pack_count=6, price="85", container="can", container_status="inferred", sugar="regular (no sugar wording)",
      tier="S", url="https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", raw=RZ, anchor="15514234", stock="not shown",
      note="no higher figure"),
    R(id="A14", group="main", channel="aggregator", retailer="Lotus's Shop Online (via Priceza)",
      brand="Schweppes", product="Schweppes lime soda no sugar 330 mL, six-pack (330มลX6กป)", flavour="lime",
      size_ml=330, pack_count=6, price="85", container="can", container_status="stated", sugar="no sugar (name)",
      tier="S", url="https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา", raw=RZ, anchor="51616830", stock="not shown",
      note="กป in the name is the abbreviation for กระป๋อง (can)"),
    R(id="A15", group="main", channel="aggregator", retailer="Makro PRO (via Priceza, second listing)",
      brand="Sprite", product="Sprite can 325 mL, pack of 24 (second Makro listing)", flavour="lemon-lime",
      size_ml=325, pack_count=24, price="315", container="can", container_status="stated",
      sugar="not stated (name: กระป๋อง 325 มล. x 24)", tier="S",
      url="https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813", raw=RZ,
      anchor="7416114544835", stock="not shown",
      note="second Makro listing; read on the Priceza product page (same listing number); kept in set A"),

    # ---- Single cans (one unit per listing) ----
    R(id="S01", group="single", channel="direct", retailer="Lotus's Shop Online", brand="Singha",
      product="SINGHA LEMON SODA CAN 330ML. (single can)", flavour="lemon", size_ml=330, pack_count=1, price="17",
      container="can", container_status="stated", sugar="sugar-free (maker page)", tier="S",
      url="https://www.lotuss.com/en/product/singha-lemon-soda-zero-sugar-lemon-soda-330ml-50986847", raw=RL,
      stock="no stock wording on page", note="'/Each' single unit"),
    R(id="S02", group="single", channel="direct", retailer="Lotus's Shop Online", brand="Sprite",
      product="Sprite can 325 mL (single can)", flavour="lemon-lime", size_ml=325, pack_count=1, price="16",
      container="can", container_status="stated", sugar="not stated (regular)", tier="S",
      url="https://shopping.lotuss.com/th/product/sprite-lemonlime-flavour-soft-drink-325ml-238945", raw=RL,
      stock="no stock wording on page", note="name: สไปรท์ กระป๋อง 325 มล."),
    R(id="S03", group="single", channel="direct", retailer="Lotus's Shop Online", brand="Schweppes",
      product="Schweppes Manao Soda 330CC (single can)", flavour="lime", size_ml=330, pack_count=1, price="18",
      container="can", container_status="inferred", sugar="not stated", tier="S",
      url="https://shopping.lotuss.com/en/product/schweppes-soft-drink-lime-soda-330ml-single-6709516", raw=RL,
      stock="no stock wording on page",
      note="Priceza lists 17 for the same product code (S); the page read (18) is used; container not stated on the page"),
    R(id="S04", group="sens", channel="direct", retailer="Lotus's Shop Online", brand="Sprite",
      product="Sprite Chill Lemon Mint 325 mL (single)", flavour="lemon-mint (flavour variant)", size_ml=325,
      pack_count=1, price="17", container="can", container_status="inferred", sugar="not stated", tier="S",
      url="https://www.lotuss.com/en/product/75714334", raw=RL, sens=["I", "D2"],
      exclude_reason="flavour variant: lemon-mint; container not stated on the page",
      stock="no stock wording on page", note="kept in sensitivity D2 (single cans plus this row)"),
    R(id="S05", group="single", channel="aggregator", retailer="Lotus's Shop Online (via Priceza)", brand="7UP",
      product="7UP No Sugar lemon soda 325 mL (single)", flavour="lemon-lime", size_ml=325, pack_count=1, price="16",
      container="can", container_status="inferred", sugar="no sugar (name)", tier="S",
      url="https://www.priceza.com/s/ราคา/เซเว่นอัพ", raw=RZ, anchor="75553150", stock="not shown",
      note="Priceza row; container not stated in the row; the name says 325 mL"),

    # ---- Excluded or sensitivity rows ----
    R(id="X01", group="sens", channel="direct", retailer="Makro PRO", brand="Sprite",
      product="Sprite Soft Drink Lemon Lime 330 mL, pack of 12 (SKU 830198)", flavour="lemon-lime", size_ml=330,
      pack_count=12, price="137", unit="11.42", container="not stated", container_status="not stated",
      sugar="not stated", tier="S", url="https://www.makro.pro/en/p/830198-7078660866243", raw=RM, sens=["H"],
      exclude_reason=("container not stated on the Makro page (re-read 20 October 2026); the can test of the rule fails. "
                      "The page prints 135 under 'Buy 3+ units' (a buy-more tier, not used); 137 is the pack price because "
                      "137 divided by 12 gives the printed per-unit 11.42. The bottle reading rests on the sizes in the image "
                      "file names and alt text of the Coca-Cola Thailand Sprite products page (readable on 20 October 2026, "
                      "t5_recheck3); the ladder minimum depends on this classification"),
      note="330 mL is not a size shown for a Sprite can on the Coca-Cola Thailand page"),
    R(id="X02", group="sens", channel="direct", retailer="7-Eleven ALL Online", brand="Nestle",
      product="Nestle Pure Life Soda Plus Lemon Lime 330 mL, tray of 24 cans", flavour="lemon-lime", size_ml=330,
      pack_count=24, price="377", container="can", container_status="stated", sugar="no sugar claim on page",
      tier="S", url="https://www.allonline.7eleven.co.th/p/เนสท์เล่-เพียวไลฟ์-โซดาพลัส-เลมอนไลม์-330-มลถาด-24-กระป๋อง/327940/",
      raw=R7, sens=["J"], exclude_reason="out of stock on the page", stock="sorry, out of stock (page label)"),
    R(id="X03", group="sens", channel="direct", retailer="Makro PRO", brand="Schweppes",
      product="Schweppes Soft Drink Lime Soda Zero Sugar 330 mL, six cans", flavour="lime", size_ml=330,
      pack_count=6, price="84", container="can", container_status="stated", sugar="zero sugar (name)", tier="S",
      url="https://www.makro.pro/en/p/899900-7499701616835", raw=RM, sens=["J"],
      exclude_reason="unavailable in the area selected", stock="unavailable in the area selected"),
    R(id="X04", group="sens", channel="marketplace_unnamed", retailer="Lazada (trending page; seller not shown)",
      brand="7UP", product="7UP strawberry-lemon 325 mL, six cans (NS not confirmed on the opened page)", flavour="strawberry-lemon (flavour variant)",
      size_ml=325, pack_count=6, price="75", container="can", container_status="stated", sugar="NS not confirmed on the opened page",
      tier="S", url="https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705", raw=RZ,
      anchor="7Up Ns Strawberry Lemon 6*325Ml", sens=["I"], stock="not shown",
      exclude_reason="flavour variant (strawberry-lemon) and seller not shown"),
    R(id="X05", group="excluded", channel="direct", retailer="Lotus's Shop Online", brand="Singha",
      product="SINGHA SODA 325 mL x 6", flavour="plain soda water", size_ml=325, pack_count=6, price="48",
      container="bottle", container_status="inferred from the 7-Eleven and Makro bottle listings",
      sugar="not stated", tier="S", url="https://www.lotuss.com/en/product/singha-soda-325-ml-6-24183741", raw=RL,
      exclude_reason="bottle product; outside the can ladder; '/Each' read as pack price (DERIVED)"),
    R(id="X06", group="excluded", channel="direct", retailer="7-Eleven ALL Online", brand="Singha",
      product="Singha Soda 325 mL, pack of 24 bottles", flavour="plain soda water", size_ml=325, pack_count=24,
      price="195", container="bottle", container_status="stated", sugar="none stated", tier="S",
      url="https://www.allonline.7eleven.co.th/p/โซดาสิงห์-325-มล-แพ็ก-24-ขวด/452565/", raw=R7,
      exclude_reason="bottle product (แพ็ก 24 ขวด); outside the can ladder"),
    R(id="X07", group="excluded", channel="direct", retailer="Makro PRO", brand="Singha",
      product="SINGHA Soda 325 mL x 24 bottles", flavour="plain soda water", size_ml=325, pack_count=24, price="190",
      unit="7.92", container="bottle", container_status="stated", sugar="none stated", tier="S",
      url="https://www.makro.pro/en/p/160629-6761215066307", raw=RM,
      exclude_reason="bottle product ('24 bottles, each filled with 325 ml'); outside the can ladder"),
]

# Dated reference figures (not in any ladder). Each has its own price pattern.
REFERENCE = [
    R(id="R01", group="reference", channel="reference", retailer="Thaiger (news, 29 August 2022)", brand="Sprite",
      product="Sprite Lemon Plus 325 mL, 2022 price as stated (unit not stated; read as one can)", flavour="lemon-lime",
      size_ml=325, pack_count=1, price="15", container="can", container_status="inferred", sugar="sugar-free (2022 article)",
      tier="S", url="https://thethaiger.com/th/news/641196/", raw=RB,
      price_pattern=r"ราคา\s*15\s*บาท", note="dated 2022; not a current price", date="2022-08-29"),
    R(id="R02", group="reference", channel="reference", retailer="Kaohoon International (17 March 2026)",
      brand="Singha", product="Singha Sparkling Water Lime 330 mL can, launch price", flavour="lime",
      size_ml=330, pack_count=1, price="15", container="can", container_status="stated",
      sugar="company claim relayed by press: sugar-free (S)", tier="S",
      url="https://www.kaohooninternational.com/?p=579263", raw=RB,
      price_pattern=r"priced at 15 Baht", date="2026-03-17",
      note="trade press quoting the Chief Marketing Officer of Boon Rawd Trading Co., Ltd.; no release named or dated in the article; the 13 March 2026 company release was not opened"),
    R(id="X08", group="reference", channel="reference", retailer="Tops Online (built-in browser capture, 18 October 2026)",
      brand="Sprite", product="Sprite Soft Drink Zero Sugar Lemon Lime Flavour 325 ml, SKU 8851959132395 (out of stock on the page)",
      flavour="lemon-lime", size_ml=325, pack_count=1, price="16", container="can", container_status="stated",
      sugar="zero sugar (name)", tier="S", url="https://www.tops.co.th/en/sprite-soft-drink-zero-sugar-lemon-lime-flavour-325ml-8851959132395",
      raw=RX, anchor="8851959132395", price_pattern=r"16 / can", date="2026-10-18",
      stock="Out Of Stock (printed on the page, 18 October 2026)",
      note="excluded lead: out of stock; read in the built-in browser on 18 October 2026, not 20 October; the 20 October product page returned HTTP 403"),
    R(id="X09", group="reference", channel="reference", retailer="Tops Online (built-in browser capture, 18 October 2026)",
      brand="Schweppes", product="Schweppes Soda Water 330 cc, SKU 8851959132647 (out of stock on the page)",
      flavour="plain soda water", size_ml=330, pack_count=1, price="17", container="can", container_status="stated",
      sugar="plain soda water; no sugar statement", tier="S", url="https://www.tops.co.th/en/schweppes-soda-water-330cc-8851959132647",
      raw=RX, anchor="8851959132647", price_pattern=r"17 / can", date="2026-10-18",
      stock="Out Of Stock (printed on the page, 18 October 2026)",
      note="excluded lead: out of stock; plain soda water, not lemon or lime; read 18 October 2026"),
]

# Alternative reading of the 7-Eleven six-pack (sensitivity only): the printed pair is 172 and 182. Set P uses 182.
ALT = [
    R(id="D02alt", group="sens", channel="direct", retailer="7-Eleven ALL Online", brand="Singha",
      product="Singha Lemon Soda 330 mL, pack of 6 cans (alternative reading: 182 as the selling price)", flavour="lemon",
      size_ml=330, pack_count=6, price="182", container="can", container_status="stated", sugar="sugar-free (maker page)",
      tier="S", url="https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-แพ็ก-6-กระป๋อง/514221/", raw=R7,
      sens=["P"], exclude_reason="alternative reading only; 182 is the earlier price on the savings line (save 10), so it is not the selling price",
      stock="in stock (page label)", note="sensitivity only: the printed pair is 172 and 182; the savings line reads 182 minus 172"),
]


def price_regex(num):
    """Printed pack price: baht sign or THB, then the number (optionally .00), not followed by another digit."""
    if "." in num:
        body = re.escape(num) + r"(?![\d])"
    else:
        body = re.escape(num) + r"(?:\.00)?(?![\d])"
    return r"(?:฿|THB)\s*" + body


def unit_regex(num):
    return r"(?<![\d.])" + re.escape(num) + r"(?![\d])"


def load_raw():
    texts = {}
    for r in ROWS + REFERENCE + ALT:
        name = r["raw"]
        if name in texts:
            continue
        path = os.path.join(RAW_DIR, name)
        if not os.path.isfile(path):
            raise SystemExit("MISSING RAW FILE: " + name)
        with open(path, "r", encoding="utf-8") as fh:
            texts[name] = fh.read()
    return texts


def check_row(r, text):
    pat = r["price_pattern"] or price_regex(r["price"])
    occ = [m.start() for m in re.finditer(re.escape(r["anchor"]), text)]
    out = dict(id=r["id"], raw_file=r["raw"], anchor_found=bool(occ), price_matched=None, unit_matched=None)
    for idx in occ:
        seg = text[max(0, idx - BEFORE): idx + WINDOW]
        m = re.search(pat, seg)
        if not m:
            continue
        out["price_matched"] = m.group(0)
        if r["unit"]:
            mu = re.search(unit_regex(r["unit"]), seg)
            out["unit_matched"] = mu.group(0) if mu else None
            if not mu:
                continue
        return out
    return out


def check_rows(rows, texts):
    """Every row gets its own passed flag and its matched text. A failing row stops the run before any output is written."""
    table = []
    failures = []
    for r in rows:
        res = check_row(r, texts[r["raw"]])
        ok = res["anchor_found"] and res["price_matched"] is not None and (not r["unit"] or res["unit_matched"] is not None)
        if r["unit"]:
            res["unit_arithmetic_ok"] = abs(round(r["pack_price_thb"] / r["pack_count"], 4) - float(r["unit"])) <= 0.005
            ok = ok and res["unit_arithmetic_ok"]
        else:
            res["unit_arithmetic_ok"] = None
        res["passed"] = bool(ok)
        table.append(res)
        if not ok:
            failures.append(r["id"] + " in " + r["raw"])
    if failures:
        raise SystemExit("CHECK FAILED for rows: " + "; ".join(failures))
    return table


def per_can(r):
    return r["pack_price_thb"] / r["pack_count"]


def per_330(r):
    return per_can(r) * SERVE_ML / r["size_ml"]


def per_litre(r):
    return per_can(r) / (r["size_ml"] / 1000.0)


def stats(vals):
    vals = sorted(vals)
    n = len(vals)
    q = statistics.quantiles(vals, n=4, method="inclusive")
    return dict(n=n, min=round(vals[0], 4), q1=round(q[0], 4), median=round(statistics.median(vals), 4),
                q3=round(q[2], 4), max=round(vals[-1], 4), mean=round(sum(vals) / n, 4))


def d2(x):
    """Two decimals, rounded half up (display only)."""
    return str(Decimal(repr(round(x, 6))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def rowline(r):
    return dict(id=r["id"], group=r["group"], retailer=r["retailer"], brand=r["brand"], product=r["product"],
                size_ml=r["size_ml"], pack_count=r["pack_count"], pack_price_thb=r["pack_price_thb"],
                per_can_thb=round(per_can(r), 4), per_330ml_thb=round(per_330(r), 4),
                per_litre_thb=round(per_litre(r), 2), container=r["container"],
                container_status=r["container_status"], sugar=r["sugar"], tier=r["tier"], channel=r["channel"],
                url=r["url"], raw_file=r["raw"], date_read=DATE, stock=r["stock"], note=r["note"],
                exclude_reason=r["exclude_reason"], sens_groups=r["sens"], display_per_330_thb=d2(per_330(r)))


def main():
    texts = load_raw()
    check_table = check_rows(ROWS + REFERENCE + ALT, texts)
    checks_passed = all(c["passed"] for c in check_table)

    R_ = {r["id"]: r for r in ROWS}
    A = [r for r in ROWS if r["group"] == "main"]
    S = [r for r in ROWS if r["group"] == "single"]
    B = [r for r in A if r["channel"] == "direct"]
    C = [r for r in A if r["channel"] == "aggregator"]
    sets = {
        "A_main_all_usable_cans": A,
        "B_direct_retailer_pages": B,
        "C_aggregator_priceza_rows": C,
        "D_single_cans": S,
        "D2_single_cans_plus_S04_flavour_variant": S + [R_["S04"]],
        "E_main_without_7eleven_six_packs": [r for r in A if r["id"] not in ("D02", "D03")],
        "F_main_plus_lazada_unnamed_seller_rows": A + [R_["D18"], R_["D19"]],
        "G_main_stated_container_only": [r for r in A if r["container_status"] == "stated"],
        "H_main_plus_X01_container_not_stated": A + [R_["X01"]],
        "I_main_plus_flavour_variants_D09_X04": A + [R_["D09"], R_["X04"]],
        "J_main_plus_out_of_stock_or_unavailable_X02_X03": A + [R_["X02"], R_["X03"]],
        "K_singha_rows_in_main": [r for r in A if r["brand"] == "Singha"],
        "L_schweppes_rows_in_main": [r for r in A if r["brand"] == "Schweppes"],
        "M_sprite_and_7up_rows_in_main": [r for r in A if r["brand"] in ("Sprite", "7UP")],
        "N_plain_soda_water_rows_in_main": [r for r in A if r["flavour"] == "plain soda water"],
        "P_main_with_D02_at_182_alternative_reading": [r for r in A if r["id"] != "D02"] + [ALT[0]],
    }
    ladders = {k: stats([per_330(r) for r in v]) for k, v in sets.items()}
    ladders["O_main_per_litre"] = stats([per_litre(r) for r in A])

    cube = CUBE_SHELF_PRICE_THB
    a_vals = [per_330(r) for r in A]
    s_vals = [per_330(r) for r in S]
    below = [r["id"] for r in A if per_330(r) < cube]
    above = [r["id"] for r in A if per_330(r) > cube]
    a_med = statistics.median(a_vals)
    b_med = statistics.median([per_330(r) for r in B])
    s_med = statistics.median(s_vals)
    s_min = min(s_vals)
    position = dict(
        cube_price_thb=cube,
        main_rows_n=len(A),
        main_rows_below_cube=len(below),
        main_rows_above_cube=len(above),
        share_of_main_rows_below_cube_pct=round(100.0 * len(below) / len(A), 1),
        below_cube_ids=below,
        above_cube_ids=above,
        gap_to_main_median_thb=round(cube - a_med, 4),
        gap_to_main_median_pct=round(100.0 * (cube / a_med - 1), 1),
        gap_to_direct_median_thb=round(cube - b_med, 4),
        gap_to_single_can_min_thb=round(cube - s_min, 4),
        gap_to_single_can_median_thb=round(cube - s_med, 4),
    )

    singha_single = R_["S01"]
    cmp_rows = [
        ("Singha Lemon Soda single can (Lotus's online)", per_330(singha_single), "S01"),
        ("Singha Lemon Soda 24-can case, per can (7-Eleven ALL Online)", per_330(R_["D01"]), "D01"),
        ("Singha Lemon Soda 24-can case, per can (Lotus's online)", per_330(R_["D12"]), "D12"),
        ("Singha Lemon Soda 24-can case, per can (Makro PRO online)", per_330(R_["D06"]), "D06"),
        ("Singha Lemon Soda 6-can pack, per can (Makro PRO online)", per_330(R_["D07"]), "D07"),
        ("Singha Lemon Soda 6-can pack, per can (Lotus's online)", per_330(R_["D13"]), "D13"),
        ("Singha Sparkling Water Lime 24-can case, per can (7-Eleven ALL Online)", per_330(R_["D04"]), "D04"),
        ("Singha Sparkling Water Lime 24 units, per can (Makro PRO online)", per_330(R_["D08"]), "D08"),
        ("Median of the four single-can listings (S01, S02, S03, S05)", s_med, "D_single_median"),
        ("Cheapest single-can listing (S02 and S05)", s_min, "D_single_min"),
        ("Singha Sparkling Water Lime launch price (Kaohoon, 17 March 2026, S)", 15.0 * SERVE_ML / 330.0, "R02"),
        ("Sprite Lemon Plus 2022 price (Thaiger, 29 August 2022, S, dated)", 15.0 * SERVE_ML / 325.0, "R01"),
    ]
    cube_vs_can = [dict(comparison=c, row_id=i, can_per_330_thb=round(v, 4), cube_per_serve_thb=cube,
                        cube_minus_can_thb=round(cube - v, 4), cube_vs_can_pct=round(100.0 * (cube / v - 1), 1))
                   for c, v, i in cmp_rows]

    cube_block = dict(cube_per_serve_thb=cube, serve_ml=SERVE_ML,
                      cube_per_litre_thb=round(cube / (SERVE_ML / 1000.0), 2),
                      note="One cube makes one 330 mL serve. The THB 15 price is an ASSUMPTION in the submission model.")

    display = dict(
        A_min=d2(ladders["A_main_all_usable_cans"]["min"]), A_q1=d2(ladders["A_main_all_usable_cans"]["q1"]),
        A_median=d2(ladders["A_main_all_usable_cans"]["median"]), A_q3=d2(ladders["A_main_all_usable_cans"]["q3"]),
        A_max=d2(ladders["A_main_all_usable_cans"]["max"]),
        B_median=d2(ladders["B_direct_retailer_pages"]["median"]),
        D_min=d2(ladders["D_single_cans"]["min"]), D_median=d2(ladders["D_single_cans"]["median"]),
        D_max=d2(ladders["D_single_cans"]["max"]),
        gap_main_median=d2(position["gap_to_main_median_thb"]),
        gap_direct_median=d2(position["gap_to_direct_median_thb"]),
        gap_single_min=d2(position["gap_to_single_can_min_thb"]),
        gap_single_median=d2(position["gap_to_single_can_median_thb"]),
        H_min=d2(ladders["H_main_plus_X01_container_not_stated"]["min"]),
        F_median=d2(ladders["F_main_plus_lazada_unnamed_seller_rows"]["median"]),
        I_median=d2(ladders["I_main_plus_flavour_variants_D09_X04"]["median"]),
        cube_per_litre=d2(cube_block["cube_per_litre_thb"]),
    )

    out = dict(
        task="T5 retail price ladder (lemon, lime and clear carbonated cans and soda waters, 325 to 345 mL), revised 20 October 2026",
        date_read=DATE,
        method=("Each row is checked first: its anchor (URL, listing number or product name) must occur in its saved raw "
                "file, and the printed pack price (baht sign or THB) must appear within %d characters after it or %d "
                "characters before it; where a "
                "per-unit price is printed it must appear too and agree with pack price / pack count. This is a presence "
                "check on the saved extracts, not a parse. Then per can = pack price / pack count; per 330 mL = per can x "
                "330 / can mL; per litre = per can / can litres. Set A (main) admits can rows from a retailer page, or a "
                "Priceza offer whose seller is an official store or a named seller, and excludes bundles, out-of-stock, "
                "unavailable, bottles, out-of-range sizes, unnamed sellers and non-lemon, non-lime flavours. No random "
                "numbers; no seed. A row that fails stops the run before any output is written, so a results file "
                "with all_rows_pass true means every row passed on that run.") % (WINDOW, BEFORE),
        checks=dict(rows_checked=len(check_table), rows_passed=sum(1 for c in check_table if c["passed"]),
                    all_rows_pass=checks_passed,
                    unit_consistency_checked=sum(1 for r in ROWS if r["unit"]),
                    window_characters=WINDOW, raw_folder="rework/raw/diligence_2026-10-20/T5/"),
        check_table=check_table,
        rows=[rowline(r) for r in ROWS],
        reference_dated_not_in_ladder=[dict(id=r["id"], product=r["product"], price_thb=float(r["price"]),
                                            url=r["url"], raw_file=r["raw"], tier="S", date=r["date"], stock=r["stock"],
                                            per_330ml_thb=round(per_330(r), 4)) for r in REFERENCE],
        ladders=ladders,
        position_of_cube_price=position,
        cube=cube_block,
        cube_vs_can_per_serve=cube_vs_can,
        sets={k: [r["id"] for r in v] for k, v in sets.items()},
        counts=dict(main_rows=len(A), direct_rows=len(B), aggregator_rows=len(C), single_rows=len(S),
                    sensitivity_rows=sum(1 for r in ROWS if r["group"] == "sens"),
                    excluded_rows=sum(1 for r in ROWS if r["group"] == "excluded")),
        display=display,
    )

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    print("checks_passed", checks_passed, "rows", len(check_table), "passed", sum(1 for c in check_table if c["passed"]))
    print("counts", out["counts"])
    for k, v in ladders.items():
        print(k, v)
    print("position", position)
    for c in cube_vs_can:
        print(c["row_id"], c["can_per_330_thb"], c["cube_minus_can_thb"], c["cube_vs_can_pct"])
    print("display", display)
    print("written", OUT)


if __name__ == "__main__":
    main()
