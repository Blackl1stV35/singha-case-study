# 68d. Retail price ladder: lemon, lime and clear carbonated cans and soda waters in Thailand (task T5)

Date read: 20 October 2026. This is the second revision. It replaces the first revision in full and applies the findings of a second independent verifier. Section 16 lists each finding and the change made. Section 15 lists the first revision. The main ladder keeps every figure from the first revision. The changes are to tiers, dates, wording, the access log and the excluded leads.

Scope: lemon, lime and clear carbonated soft drinks and soda waters in 325 to 345 mL cans, read against the THB 15 planning price of the Singha Lemon Soda Cube (one cube makes one 330 mL serve). This record covers prices only. Competitor financials belong to T2 to T4.

Status: every price here is an online listing read on 20 October 2026, except the two Tops out-of-stock leads, which were read in a built-in browser on 18 October 2026 and are excluded from every ladder. No store shelf price was read. Tiers: retailer product pages, Priceza offer rows and browser-read pages are S (SOURCED: read and opened). Company and brand pages were read as WebFetch extracts, not in full, so they are S (extract). The tier key gives P only for a page read in full. DERIVED means our arithmetic from the inputs shown. ASSUMPTION marks the THB 15 planning price, which has no source.

Saved pages: rework/raw/diligence_2026-10-20/T5/. This pass: t5_recheck_*_2026-10-20.md, t5_recheck2_*_2026-10-20.md and t5_recheck3_live_checks_2026-10-20.md (the second verifier's live re-reads, and a copy of the 18 October Tops capture). Earlier pass: r01 to r34 and older captures. Script: rework/screen/t5_retail_price_ladder.py (run with python -I). Results: rework/screen/t5_retail_price_ladder_results.json.

The script checks every row against its saved file before it computes anything. The row's anchor (a URL, a Priceza listing number, a SKU, or a product name as printed) must occur in the file. The printed pack price, with its baht sign or THB (or, for the two Tops rows, the printed "16 / can" or "17 / can"), must appear within 900 characters after the anchor or 200 characters before it. Where the page prints a per-unit price, that figure must also appear and must agree with pack price divided by pack count. This is a presence check on the saved extracts. It is not a parse of the pages. Each of the 51 rows has its own passed flag and its matched text in the results file (the 48 rows of the first revision, plus two Tops reference rows and one alternative reading of a 7-Eleven row). A failing row stops the run before any output is written. In the run that produced these results, all 51 rows passed.

## 1. Result in brief

- Main ladder (set A): 31 usable can listings. Per 330 mL they run from THB 12.40 to THB 28.67, with a median of THB 14.05 (quartiles THB 13.64 and THB 14.50; mean THB 15.04). Per litre the median is THB 42.56. Tier S, SOURCED. Per-can and per-330 mL figures are DERIVED.
- Direct ladder (retailer product pages only): 16 listings, median THB 13.88 (exactly 13.875), range THB 12.58 to THB 28.67.
- Aggregator ladder (Priceza offer rows from official or named sellers): 15 listings, median THB 14.13, range THB 12.40 to THB 16.33.
- Single cans (one unit per listing): 4 listings, THB 16.25 to THB 18.00 per 330 mL, median THB 16.62. The two cheapest single cans read THB 16 each: the Sprite 325 mL can at Lotus's online, and a 7UP No Sugar 325 mL can in a Priceza row. The Singha Lemon Soda single can reads THB 17 at Lotus's online. No Sprite No Sugar single can was read on any opened retailer page. The 18 October Tops capture printed a Sprite Zero Sugar 325 mL can at THB 16, marked out of stock; it is an excluded lead (X08).
- The THB 15 planning price sits above the main median. 25 of the 31 main listings are below THB 15 and 6 are above. It is THB 0.95 (6.8 percent) above the main median, and THB 1.25 below the cheapest single can read.
- Per serve, the cube at THB 15 is THB 2.00 (11.8 percent) below the Singha Lemon Soda single can at Lotus's online (THB 17). It is THB 1.25 (9.1 percent) above the same can bought in a 24-can case (THB 330 for 24 cans, tier S, SOURCED, so THB 13.75 per can, DERIVED, at 7-Eleven ALL Online and at Lotus's online).
- The lowest main listing (THB 12.40) is a 7UP No Sugar 24-can offer read through Priceza. If the Makro PRO 330 mL Sprite 12-pack (THB 11.42 per can; container not stated on the page) were counted as a can, the minimum would be THB 11.42. Section 4.3 explains why it is not counted. The main median is THB 14.05 either way.
- Singha rows: 8 listings, with a median of THB 13.71 per 330 mL. The Singha Lemon Soda 24-can case reads THB 13.54 to THB 13.75 per can (DERIVED from pack prices of THB 325 at Makro PRO and THB 330 at 7-Eleven and Lotus's). The Singha Sparkling Water Lime 24-can case reads THB 12.58 (7-Eleven ALL Online) and THB 13.00 (Makro PRO). The Singha Sparkling Water Lime launch price was THB 15 for a 330 mL can (S, Kaohoon International, posted 17 March 2026).
- Sugar: the Singha Lemon Soda is sugar-free on the maker's own page (S, extract; sucralose and acesulfame potassium). Sprite Lemon Plus is described as sugar-free in its launch release (S, extract) and in the Priceza row name. The 7UP No Sugar rows are sugar-free by name. Most Sprite and Schweppes rows state no sugar.
- Sprite Lemon Plus has no current retail price on a retailer page. The one 2026 price found is a Priceza row at THB 332 for 24 cans (THB 14.05 per 330 mL, DERIVED, tier S). The THB 15 figure is from a 2022 article and is dated.
- Not read: Big C Online and Foodland (HTTP 403 on every page tried), Shopee Thailand (a traffic-verification page; no listing reached), CP Fresh Mart (a redirect to a third-party host, not followed), and Lazada official-store product pages (not opened; section 11). Tops Online returned HTTP 403 on every product page read on 20 October 2026, including the two pages re-tried on the second pass. A built-in browser capture on 18 October 2026 printed two Tops single cans, both out of stock: the Sprite Zero Sugar 325 mL at THB 16 and the Schweppes Soda Water 330 cc at THB 17. They are excluded leads (rows X08 and X09). Tops appears in the main ladder only through one Priceza row (S).
- Maker pages: the Coca-Cola Thailand Sprite products page was readable on the second pass on 20 October 2026. It gives the sizes from image file names only, and the record uses it for sugar status and container context, not for prices.

## 2. Method and set rules

- Per can = pack price divided by pack count. Per 330 mL = per can x 330 / can mL, so 325 mL cans are scaled by 330/325. Per litre = per can / can litres. Pack prices are S (read on the page). Per can, per 330 mL and per litre figures are DERIVED from them.
- Pack price = the headline price for one unit of the pack. Buy-more tiers, club or member prices, promotion prices, and struck-through or list prices are not used. Where a page shows two prices, the one that matches the page's per-unit figure or the pack count is read, and the reading is noted row by row. For the 7-Eleven pages the lower price is read as the selling price where the savings line equals the difference between the two prices and the badge is a discount (section 4.1, row D02).
- Lotus's pack pages carry only a "/Each" label. The extract does not say whether it means per can or per pack. A per-can reading gives implausible totals (THB 330 for one can, THB 510 for six cans), so the pack price is read (DERIVED).
- Set A (main ladder) admits can rows from a retailer product page, and Priceza offers whose seller is an official store or a named seller. A named seller is a retailer (Lotus's, Makro, 7-Eleven) or the brand owner's own LazMall account (Coca-Cola Official Store, and Suntory PepsiCo's LazMall account for row A05, which carries no official-store label).
- Set A excludes: bundles (candy, crackers, free gift), three-pack totals, out-of-stock and unavailable rows, bottles, sizes outside 325 to 345 mL, rows whose seller is not shown or not verified, flavour variants that add a flavour other than lemon or lime, and duplicate rows.
- Flavour rule: plain lemon-lime, lemon, lime and plain soda water count as plain. Mint and strawberry variants are excluded. The brief names Sprite Lemon Plus, so it is kept in set A as a lemon variant. No other flavour is named in the sources read for it.
- Container rule: a row counts as a can when its name, its size, or the same product's other listings say can. Rows whose container is inferred this way stay in set A and are tested in set G (stated container only). A row that fails the rule is not in set A.
- Statistics: Python statistics module, inclusive quartiles. No random numbers are used, so there is no seed. The statistics describe one day's listings. They are not a sample of prices, and the rows are not independent: the 8 Singha rows come from one brand.

## 3. Coverage and access

| Retailer or source | Read | Result | Used for |
|---|---|---|---|
| 7-Eleven ALL Online | Product pages and one search page, 20 October 2026 | Four usable can rows; one out-of-stock row; one bottle row; the search shows 30 of 273 cards, one matching. Each product page carries a notice that a function is unavailable because of a technical problem. The search was flagged unreliable | D01 to D04 (set A); D02alt (set P, sensitivity); X02 (set J); X06 (excluded) |
| Makro PRO | Product pages, 20 October 2026; search page (HTTP 404) | Product pages read; several show Loading placeholders | D05 to D08 and D10 to D11 (set A); D09 (set I); X01 (set H); X03 (set J); X07 (excluded) |
| Lotus's Shop Online | Product pages, 20 October 2026; search page (shell) | Product pages read | D12 to D17 (set A); S01, S02, S03 (singles); S04 (set D2); X05 (excluded) |
| Lazada trending page (seller not shown) | Two passes on 20 October 2026 (the second with a seller prompt) | Sprite 24-can rows at THB 365; seller not shown on either read | D18, D19 (set F); X04 (set I) |
| Lazada official-store pages | Search, tag and product pages on 20 October returned shells without prices or sellers. On 18 October the Lazada route stopped at a reCAPTCHA robot check (not solved) | No Lazada official-store product page was opened. Priceza LazMall rows are aggregator merchant prices | Limit (section 11) |
| Shopee Thailand | Two product pages and a search page, 18 October 2026 (browser). Web search, 20 October 2026 | A traffic-verification page (not bypassed). No listing reached | Not read (limit) |
| CP Fresh Mart (CP All) | Search page, 20 October 2026 | HTTP 302 to a third-party host; the redirect was not followed | Not read (limit). Two Priceza Fresh Mart rows have a seller that is not verified and are not used |
| Priceza (aggregator) | Sprite, 7UP and Schweppes listing pages; the Sprite product page | Offer rows from official or named sellers | A01 to A15 (set A); S05 (single); 7UP listing numbers re-read (raw t5_recheck2_priceza_7up_listing_2026-10-20.md) |
| Coca-Cola Thailand Sprite products page | First pass, 20 October 2026 (readable). Two later attempts on 20 October returned HTTP 403. A later re-read on 20 October was readable (raw t5_recheck3_live_checks_2026-10-20.md, section 4) | Four Sprite products (can and plastic bottle, regular and no-sugar formula); sizes from image file names only; no prices | Sugar status and can size (S, extract); basis of X01 (see 4.3) |
| Coca-Cola Thailand Sprite brand page (alternate address) | One attempt returned HTTP 403 (blocked file, row 15). A later read on 20 October gave an extract | Lists no products; no volumes | Context only (S, extract) |
| Coca-Cola Thailand Schweppes brand page | Read on the later pass | Seven Schweppes products; lime soda described as in a can (alt text); no volume shown | Container context for Schweppes rows (S, extract) |
| Coca-Cola (Thailand) press release on Schweppes zero-sugar fruit sodas (thaipr, 28 June 2022) | Read on the later pass | Pineapple Mojito Soda (325 mL cans) and Citrus Raspberry Soda (no size); fruit flavours | Not used (outside scope) |
| Singha Corporation, Singha Lemon Soda page (English and Thai) | Read as an extract, 20 October 2026 | Flavours, 330 mL, sugar-free and sweetener statements; no price | Sugar status (S, extract) |
| Sprite Lemon Plus release (thaipr, 8 September 2022) and Thaiger article (29 August 2022) | Read | Sugar-free; no can size; 2022 price THB 15 | Dated reference only (S) |
| Kaohoon International, Singha Sparkling Water Lime article (posted 17 March 2026) | Read | THB 15 for a 330 ml can, quoted from the Chief Marketing Officer of Boon Rawd Trading Co., Ltd. No company release named or dated | Reference (S) |
| Tops Online | Product pages on 20 October 2026: HTTP 403, including the Sprite Zero 325 mL and Schweppes soda water pages (first pass and re-tried on the second pass). Search and 7UP pages: HTTP 403. Built-in browser capture on 18 October 2026 | 18 October capture: Sprite Zero Sugar 325 mL at 16 per can and Schweppes Soda Water 330 cc at 17 per can, both printed Out Of Stock | A02 from Priceza only (set A). X08 and X09 are excluded leads (4.3) |
| Big C Online | Search page and five product pages, 20 October 2026 | HTTP 403 on all | Not read (limit) |
| Foodland | Home page; web search | HTTP 403; no Thai listing found | Not read (limit) |
| Suntory PepsiCo company site (suntorypepsico.co.th) | Read attempt | HTTP 403 | Not read; the address comes from a job-listing site and is a lead only |
| Singha Online Shop | Search | No page found | No maker-shop price |
| Schweppes Thailand official site; 7UP Thailand official site | Web searches (standard) | Not found | Stated limit |

## 4. Ladder rows

Each row gives the product, size, pack, price, per-330 mL price, retailer, date read, URL, sugar status and tier. "Inferred" means the container is not stated on the page; the container rule (section 2) applies. Pack prices are S. Per can and per 330 mL are DERIVED.

### 4.1 Main ladder (set A, 31 rows)

| ID | Product | Retailer or channel | Size (mL) | Pack | Pack price (THB) | Per can (THB) | Per 330 mL (THB) | Container | Sugar status | Tier | Date read | URL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01 | Singha Lemon Soda 330 mL, case of 24 cans | 7-Eleven ALL Online | 330 | 24 | 330.00 | 13.75 | 13.75 | can (stated) | sugar-free (maker page: 0% sugar; retailer page: no sugar claim) | S | 2026-10-20 | https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-ยกลัง-24-กระป๋อง/474313/ |
| D02 | Singha Lemon Soda 330 mL, pack of 6 cans | 7-Eleven ALL Online | 330 | 6 | 172.00 | 28.67 | 28.67 | can (stated) | sugar-free (maker page) | S | 2026-10-20 | https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-แพ็ก-6-กระป๋อง/514221/ |
| D03 | Schweppes Lime Soda Zero 330 mL, pack of 6 cans | 7-Eleven ALL Online | 330 | 6 | 170.00 | 28.33 | 28.33 | can (stated) | sugar-free (page: สูตรไม่มีน้ำตาล, sugar-free formula) | S | 2026-10-20 | https://www.allonline.7eleven.co.th/p/ชเวปส์มะนาวโซดาซีโร่-330มล-แพ็ก-6-กระป๋อง/354988/ |
| D04 | Singha Sparkling Water Lime 330 mL, case of 24 cans | 7-Eleven ALL Online | 330 | 24 | 302.00 | 12.58 | 12.58 | can (stated) | not stated on retailer page (0% calorie claim only); company claim relayed by press: sugar-free | S | 2026-10-20 | https://www.allonline.7eleven.co.th/p/สิงห์สปาร์คกลิ้งไลม์-330-มล-ยกลัง-24-กระป๋อง/327253/ |
| D05 | Sprite Soft Drink Lemon Lime 325 mL, pack of 24 (SKU 179712) | Makro PRO | 325 | 24 | 311.00 | 12.96 | 13.16 | can (inferred) | not stated (the name does not say regular or no sugar; the page does not say) | S | 2026-10-20 | https://www.makro.pro/en/p/179712-7078659719363 |
| D06 | SINGHA Lemon Soda 330 mL, 24 cans | Makro PRO | 330 | 24 | 325.00 | 13.54 | 13.54 | can (stated) | sugar-free (maker page); retailer page: no sugar claim | S | 2026-10-20 | https://www.makro.pro/en/p/428706-7350275997891 |
| D07 | SINGHA Lemon Soda 330 mL, pack of 6 | Makro PRO | 330 | 6 | 82.00 | 13.67 | 13.67 | can (inferred) | sugar-free (maker page) | S | 2026-10-20 | https://www.makro.pro/en/p/893947-6814746706115 |
| D08 | SINGHA Sparkling Water Lime 330 mL, 24 units | Makro PRO | 330 | 24 | 312.00 | 13.00 | 13.00 | can (inferred) | not stated on page | S | 2026-10-20 | https://www.makro.pro/en/p/699716183874140 |
| D10 | Schweppes Soft Drink Lime Soda 330 mL, pack of 6 (regular) | Makro PRO | 330 | 6 | 84.00 | 14.00 | 14.00 | can (inferred) | regular: no zero or no-sugar wording; nutrition panel shows 16 g carbohydrate (sugar not stated) | S | 2026-10-20 | https://www.makro.pro/en/p/vwmvjuh-6814746476739 |
| D11 | Schweppes Soda Water 330 mL, 24 units | Makro PRO | 330 | 24 | 341.00 | 14.21 | 14.21 | can (inferred) | plain soda water; no sugar statement on page | S | 2026-10-20 | https://www.makro.pro/en/p/119581-7416114282691 |
| D12 | SINGHA LEMON SODA CAN 330ML. PACK 24 | Lotus's Shop Online | 330 | 24 | 330.00 | 13.75 | 13.75 | can (stated) | sugar-free (maker page); retailer page: no sugar claim | S | 2026-10-20 | https://www.lotuss.com/en/product/169912032 |
| D13 | SINGHA LEMON SODA CAN 330ML.X6 | Lotus's Shop Online | 330 | 6 | 85.00 | 14.17 | 14.17 | can (stated) | sugar-free (maker page) | S | 2026-10-20 | https://www.lotuss.com/en/product/singha-lemon-soda-can-330ml-6-51109221 |
| D14 | SPRITE CAN 325 ML. PACK 24 (clubpack) | Lotus's Shop Online | 325 | 24 | 332.00 | 13.83 | 14.05 | can (stated) | not stated on page (the name does not say regular or no sugar) | S | 2026-10-20 | https://www.lotuss.com/en/product/sprite-soft-drink-original-325ml-x-24pcs-clubpack-150033088 |
| D15 | SPRITE 325 ML.X6 | Lotus's Shop Online | 325 | 6 | 85.00 | 14.17 | 14.38 | can (inferred) | not stated | S | 2026-10-20 | https://www.lotuss.com/en/product/sprite-lemonlime-flavour-soft-drink-325ml-x-6pcs-6808557 |
| D16 | 7 UP ZERO SUGAR LEMON SODA 325 ML. PACK6 | Lotus's Shop Online | 325 | 6 | 75.00 | 12.50 | 12.69 | can (inferred) | zero sugar (name only) | S | 2026-10-20 | https://www.lotuss.com/en/product/171266560 |
| D17 | SCHWEPPES SODA WATER 330ML.X6 | Lotus's Shop Online | 330 | 6 | 88.00 | 14.67 | 14.67 | can (inferred) | plain soda water; no sugar statement | S | 2026-10-20 | https://www.lotuss.com/en/product/schweppes-sparkling-soda-water-330ml-x-6-cans-75162024 |
| A01 | Sprite Lemon Plus Zero Sugar 325 mL, pack of 24 cans | Coca-Cola Official Store, LazMall (via Priceza) | 325 | 24 | 332.00 | 13.83 | 14.05 | can (stated) | sugar-free (name: สูตรไม่มีน้ำตาล) | S | 2026-10-20 | https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813 |
| A02 | Sprite 325 mL, pack of 24 | Tops Online (via Priceza) | 325 | 24 | 332.00 | 13.83 | 14.05 | can (inferred) | regular (no sugar wording) | S | 2026-10-20 | https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813 |
| A03 | Sprite No Sugar 325 mL, pack of 24 cans | Coca-Cola Official Store, LazMall (via Priceza) | 325 | 24 | 334.00 | 13.92 | 14.13 | can (stated) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/b/groceries/น้ำอัดลม/sprite |
| A04 | Sprite Soft Drink Original 325 mL, pack of 6 cans | Coca-Cola Official Store, LazMall (via Priceza) | 325 | 6 | 96.00 | 16.00 | 16.25 | can (stated) | regular (name) | S | 2026-10-20 | https://www.priceza.com/b/groceries/น้ำอัดลม/sprite |
| A05 | 7UP No Sugar lemon soda 325 mL, pack of 24 cans | Suntory PepsiCo LazMall account (via Priceza; no official-store label on the listing) | 325 | 24 | 293.00 | 12.21 | 12.40 | can (stated) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/เซเว่นอัพ |
| A06 | 7UP No Sugar lemon soda 325 mL, pack of 12 cans | Suntory PepsiCo, LazMall (via Priceza; official-store label shown) | 325 | 12 | 161.00 | 13.42 | 13.62 | can (stated) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/เซเว่นอัพ |
| A07 | 7UP No Sugar lemon soda 325 mL, pack of 6 cans | Suntory PepsiCo, LazMall (via Priceza) | 325 | 6 | 96.00 | 16.00 | 16.25 | can (stated) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/เซเว่นอัพ |
| A08 | Schweppes lime soda no sugar 330 mL, pack of 12 cans | Coca-Cola Official Store, LazMall (via Priceza) | 330 | 12 | 196.00 | 16.33 | 16.33 | can (stated) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา |
| A09 | Schweppes lime soda 330 mL, pack of 12 cans (regular) | Coca-Cola Official Store, LazMall (via Priceza) | 330 | 12 | 196.00 | 16.33 | 16.33 | can (stated) | regular (no sugar wording) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา |
| A10 | Schweppes lime soda no sugar 330 mL, pack of 24 cans | Coca-Cola Official Store, LazMall (via Priceza) | 330 | 24 | 351.00 | 14.63 | 14.63 | can (stated) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา |
| A11 | Schweppes lime soda no sugar 330 mL, pack of 12 | Lotus's Shop Online (via Priceza) | 330 | 12 | 167.00 | 13.92 | 13.92 | can (inferred) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา |
| A12 | Schweppes lime soda 330CC, pack of 12 (regular) | Lotus's Shop Online (via Priceza) | 330 | 12 | 167.00 | 13.92 | 13.92 | can (inferred) | regular (no sugar wording) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา |
| A13 | Schweppes lime soda 330 mL, six-pack (regular) | Lotus's Shop Online (via Priceza) | 330 | 6 | 85.00 | 14.17 | 14.17 | can (inferred) | regular (no sugar wording) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา |
| A14 | Schweppes lime soda no sugar 330 mL, six-pack (330มลX6กป) | Lotus's Shop Online (via Priceza) | 330 | 6 | 85.00 | 14.17 | 14.17 | can (stated) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา |
| A15 | Sprite can 325 mL, pack of 24 (second Makro listing) | Makro PRO (via Priceza) | 325 | 24 | 315.00 | 13.13 | 13.33 | can (stated) | not stated (name: กระป๋อง 325 มล. x 24) | S | 2026-10-20 | https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813 |

A15 is read on the Priceza product page, where the same listing number is printed with its price. The earlier raw note that called it "not used" is corrected in the raw file by an appended note.

Row note, D02 (7-Eleven six-pack). The page prints two prices: a selling price of THB 172 and a second price of THB 182, with a badge of -5% and a savings line of THB 10. The savings line equals 182 minus 172, and the same pattern holds on the two other 7-Eleven pages read (D01: 330 selling, 408 earlier, saving 78; D03: 170 selling, 190 earlier, saving 20). The record therefore reads THB 172 as the selling price. The page gives no cause for the gap to the 24-can case. If THB 182 were the selling price, D02 would be THB 30.33 per 330 mL. That alternative is set P (section 5), a sensitivity only, and the main ladder keeps the reading above.

### 4.2 Single cans (4 rows)

| ID | Product | Retailer or channel | Size (mL) | Price (THB) | Per 330 mL (THB) | Container | Sugar status | Tier | Date read | URL |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 | SINGHA LEMON SODA CAN 330ML. (single can) | Lotus's Shop Online | 330 | 17.00 | 17.00 | can (stated) | sugar-free (maker page) | S | 2026-10-20 | https://www.lotuss.com/en/product/singha-lemon-soda-zero-sugar-lemon-soda-330ml-50986847 |
| S02 | Sprite can 325 mL (single can) | Lotus's Shop Online | 325 | 16.00 | 16.25 | can (stated) | not stated (regular) | S | 2026-10-20 | https://shopping.lotuss.com/th/product/sprite-lemonlime-flavour-soft-drink-325ml-238945 |
| S03 | Schweppes Manao Soda 330CC (single can) | Lotus's Shop Online | 330 | 18.00 | 18.00 | can (inferred) | not stated | S | 2026-10-20 | https://shopping.lotuss.com/en/product/schweppes-soft-drink-lime-soda-330ml-single-6709516 |
| S05 | 7UP No Sugar lemon soda 325 mL (single) | Lotus's Shop Online (via Priceza) | 325 | 16.00 | 16.25 | can (inferred) | no sugar (name) | S | 2026-10-20 | https://www.priceza.com/s/ราคา/เซเว่นอัพ |

Row notes. S03 has an inferred container: its page prints neither a can nor a bottle (re-read on 20 October 2026, confirmed). S05 has an inferred container: its Priceza row gives 325 mL but no container word. The single-can median depends on both rows (section 11). The single-can minimum (THB 16.25) also comes from S02, which has a stated container.

### 4.3 Sensitivity and excluded rows

| ID | Product | Retailer or channel | Pack price (THB) | Per can (THB) | Per 330 mL (THB) | Set | Why | Tier | URL |
|---|---|---|---|---|---|---|---|---|---|
| D09 | Sprite Chill Lemon Mint 325 mL, pack of 6 | Makro PRO | 78.00 for 6 | 13.00 | 13.20 | I | flavour variant: lemon-mint adds a mint flavour | S | https://www.makro.pro/en/p/630907-363090727914101 |
| D18 | Sprite Soft Drink Original 325 mL, pack of 24 cans | Lazada trending page (seller not shown) | 365.00 for 24 | 15.21 | 15.44 | F | seller not shown on either read | S | https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705 |
| D19 | Sprite Soft Drink No Sugar 325 mL, pack of 24 cans | Lazada trending page (seller not shown) | 365.00 for 24 | 15.21 | 15.44 | F | seller not shown on either read | S | https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705 |
| S04 | Sprite Chill Lemon Mint 325 mL (single) | Lotus's Shop Online | 17.00 for 1 | 17.00 | 17.26 | D2 | flavour variant (lemon-mint); container not stated on the page | S | https://www.lotuss.com/en/product/75714334 |
| X01 | Sprite Soft Drink Lemon Lime 330 mL, pack of 12 (SKU 830198) | Makro PRO | 137.00 for 12 | 11.42 | 11.42 | H | container not stated on the page (re-read 20 October 2026: no container word); the can test of the rule fails. The page prints 135 under "Buy 3+ units" (a buy-more tier, not used). 137 is the pack price, because 137 divided by 12 gives the printed per-unit 11.42 and 135 would give 11.25 | S | https://www.makro.pro/en/p/830198-7078660866243 |
| X02 | Nestle Pure Life Soda Plus Lemon Lime 330 mL, tray of 24 cans | 7-Eleven ALL Online | 377.00 for 24 | 15.71 | 15.71 | J | out of stock on the page | S | https://www.allonline.7eleven.co.th/p/เนสท์เล่-เพียวไลฟ์-โซดาพลัส-เลมอนไลม์-330-มลถาด-24-กระป๋อง/327940/ |
| X03 | Schweppes Soft Drink Lime Soda Zero Sugar 330 mL, six cans | Makro PRO | 84.00 for 6 | 14.00 | 14.00 | J | unavailable in the area selected | S | https://www.makro.pro/en/p/899900-7499701616835 |
| X04 | 7UP strawberry-lemon 325 mL, six cans (NS not confirmed on the opened page) | Lazada trending page (seller not shown) | 75.00 for 6 | 12.50 | 12.69 | I | flavour variant (strawberry-lemon); seller not shown; NS not confirmed on the opened page | S | https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705 |
| X08 | Sprite Soft Drink Zero Sugar Lemon Lime Flavour 325 ml, SKU 8851959132395 | Tops Online (built-in browser capture, 18 October 2026) | 16.00 for 1 | 16.00 | 16.25 | excluded | out of stock on the page (Out Of Stock, printed 18 October 2026); read 18 October, not 20 October | S | https://www.tops.co.th/en/sprite-soft-drink-zero-sugar-lemon-lime-flavour-325ml-8851959132395 |
| X09 | Schweppes Soda Water 330 cc, SKU 8851959132647 | Tops Online (built-in browser capture, 18 October 2026) | 17.00 for 1 | 17.00 | 17.00 | excluded | out of stock on the page (Out Of Stock, printed 18 October 2026); plain soda water, not lemon or lime | S | https://www.tops.co.th/en/schweppes-soda-water-330cc-8851959132647 |
| D02alt | Singha Lemon Soda 330 mL, pack of 6 cans (alternative reading: 182 as the selling price) | 7-Eleven ALL Online | 182.00 for 6 | 30.33 | 30.33 | P | sensitivity only; the savings line reads 182 minus 172, so 182 is the earlier price on the page | S | https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-แพ็ก-6-กระป๋อง/514221/ |

Notes on the excluded rows:
- D09 and S04 are lemon-mint flavour variants. The flavour rule excludes them from set A and from the single-can set. Set D2 adds S04 to the single cans, and set I adds D09.
- D18 and D19 are Sprite 24-can listings on the Lazada trending page. The seller is not shown on either read, and the set A rule admits only official or named sellers. Set F adds them back to show the effect (median unchanged at THB 14.05).
- X01 is the Makro PRO 330 mL Sprite 12-pack. The Makro page states no container. The container rule therefore fails for this row: its name does not say can, and 330 mL is not a size the maker's own page shows for a Sprite can. The page also prints THB 135 under "Buy 3+ units" (a buy-more tier, not used), and the -1% badge sits beside both 135 and 137 (live re-read, t5_recheck3_live_checks_2026-10-20.md, section 2). The bottle basis rests on the Coca-Cola Thailand Sprite products page. That page was attempted twice on 20 October and returned HTTP 403, and a later read on the same day was readable. It lists a 325 mL can and a 330 mL plastic bottle, but the sizes come from image file names and alt text only, not from visible text. The minimum of the ladder depends on this classification. If X01 is counted, the minimum is THB 11.42 and the median stays at THB 14.05 (set H).
- X02 and X03 are out of stock or unavailable in the area selected. They are kept in set J only to show the effect on the spread.
- X04 is a strawberry-lemon flavour; it is in set I only to show the effect. The Lazada trending page does not spell out "No Sugar" for this row, so NS is not confirmed on the opened page.
- X08 and X09 are two single cans on a Tops page, read in the built-in browser on 18 October 2026. Both are printed Out Of Stock. They are excluded from every ladder. X08 is the Sprite Zero Sugar 325 mL that the submission lists at THB 16 (section 9, item 2). It is the only Sprite No Sugar single-can price in the record, and it is out of stock.
- D02alt (set P) is the alternative reading of the 7-Eleven six-pack. It is a sensitivity only.

### 4.4 Bottles (reference only, not in any can ladder)

| ID | Product | Retailer or channel | Pack price (THB) | Per bottle, 330 mL equivalent (THB) | Container | Tier | URL |
|---|---|---|---|---|---|---|---|
| X05 | SINGHA SODA 325 mL x 6 | Lotus's Shop Online | 48.00 for 6 | 8.12 | bottle (inferred from the 7-Eleven and Makro bottle listings) | S | https://www.lotuss.com/en/product/singha-soda-325-ml-6-24183741 |
| X06 | Singha Soda 325 mL, pack of 24 bottles | 7-Eleven ALL Online | 195.00 for 24 | 8.25 | bottle (stated) | S | https://www.allonline.7eleven.co.th/p/โซดาสิงห์-325-มล-แพ็ก-24-ขวด/452565/ |
| X07 | SINGHA Soda 325 mL x 24 bottles | Makro PRO | 190.00 for 24 | 8.04 | bottle (stated) | S | https://www.makro.pro/en/p/160629-6761215066307 |

### 4.5 Dated and launch figures (not in any ladder)

| Figure | Price (THB) | Per 330 mL (THB, DERIVED) | Date | Tier | URL |
|---|---|---|---|---|---|
| Sprite Lemon Plus 325 mL, 2022 price as stated (unit not stated; read as one can) | 15.00 | 15.23 | 2022-08-29 | S | https://thethaiger.com/th/news/641196/ |
| Singha Sparkling Water Lime 330 mL can, launch price | 15.00 | 15.00 | 2026-03-17 | S | https://www.kaohooninternational.com/?p=579263 |

## 5. Ladder statistics

Per 330 mL, THB, from the results file. n is the number of rows. Q1 and Q3 are inclusive quartiles.

| Ladder | n | Min | Q1 | Median | Q3 | Max | Mean |
|---|---|---|---|---|---|---|---|
| A. Main ladder: all usable can listings (set A) | 31 | 12.40 | 13.64 | 14.05 | 14.50 | 28.67 | 15.04 |
| B. Direct: retailer product pages only | 16 | 12.58 | 13.45 | 13.88 | 14.25 | 28.67 | 15.54 |
| C. Aggregator: Priceza offer rows | 15 | 12.40 | 13.92 | 14.13 | 15.44 | 16.33 | 14.50 |
| D. Single cans (S01, S02, S03, S05) | 4 | 16.25 | 16.25 | 16.62 | 17.25 | 18.00 | 16.87 |
| D2. Single cans plus S04 (flavour variant) | 5 | 16.25 | 16.25 | 17.00 | 17.26 | 18.00 | 16.95 |
| E. Main without the two 7-Eleven six-packs | 29 | 12.40 | 13.62 | 14.05 | 14.21 | 16.33 | 14.11 |
| F. Main plus the two Lazada rows (seller not shown) | 33 | 12.40 | 13.67 | 14.05 | 14.67 | 28.67 | 15.06 |
| G. Main, stated container only | 19 | 12.40 | 13.69 | 14.13 | 16.25 | 28.67 | 15.81 |
| H. Main plus X01 (Makro PRO 330 mL Sprite 12-pack) | 32 | 11.42 | 13.60 | 14.05 | 14.44 | 28.67 | 14.92 |
| I. Main plus D09 and X04 (flavour variants) | 33 | 12.40 | 13.54 | 14.05 | 14.38 | 28.67 | 14.91 |
| J. Main plus X02 and X03 (out of stock or unavailable) | 33 | 12.40 | 13.67 | 14.05 | 14.63 | 28.67 | 15.03 |
| K. Singha rows in main | 8 | 12.58 | 13.41 | 13.71 | 13.85 | 28.67 | 15.39 |
| L. Schweppes rows in main | 11 | 13.92 | 14.08 | 14.21 | 15.50 | 28.33 | 15.88 |
| M. Sprite and 7UP rows in main | 12 | 12.40 | 13.28 | 14.05 | 14.19 | 16.25 | 14.03 |
| N. Plain soda water rows in main (two rows; weak) | 2 | 14.21 | 14.32 | 14.44 | 14.55 | 14.67 | 14.44 |
| P. Main with the 7-Eleven six-pack at THB 182 (alternative reading, sensitivity only) | 31 | 12.40 | 13.64 | 14.05 | 14.50 | 30.33 | 15.09 |
| O. Main ladder per litre (THB per litre, not per 330 mL) | 31 | 37.56 | 41.35 | 42.56 | 43.95 | 86.87 | 45.57 |

Set definitions: A is the main ladder. B is the retailer product pages. C is the Priceza offer rows. D is the single-can set. D2 adds S04. E removes the two 7-Eleven six-packs, which read about twice the same retailer's 24-can price per can. F adds the two Lazada rows whose seller is not shown. G keeps rows whose container is stated on the page or by name. H adds X01. I adds D09 and X04. J adds X02 and X03. K, L and M are the Singha, Schweppes, and Sprite and 7UP rows. N is the two plain soda water rows. P is set A with the 7-Eleven six-pack read at THB 182 (D02alt). O is set A per litre.

Range note. The top of the main range is D02 at THB 28.67, read as the selling price (section 4.1). Under the alternative reading (set P) the top would be THB 30.33. The median and the quartiles are unchanged under set P. The six-pack is about twice the same retailer's 24-can price per can on either reading (2.1 times as listed, 2.2 times under the alternative). It is kept as listed in the main ladder.

## 6. Where the THB 15 planning price sits

- Against the main ladder, THB 15 is below 25 of the 31 listings (80.6 percent) and above 6 (19.4 percent). The six rows above THB 15 are the two 7-Eleven six-packs (Singha Lemon Soda at THB 28.67 and Schweppes lime zero at THB 28.33 per 330 mL), two Priceza six-packs at THB 16.25 (Sprite at Coca-Cola's official store; 7UP at the Suntory PepsiCo store on LazMall), and two Schweppes twelve-packs at THB 16.33 (Coca-Cola's official store).
- Against the direct ladder, THB 15 is THB 1.13 above the median of the 16 retailer-page rows (THB 13.875).
- Against the single cans, THB 15 is below all four. It is THB 1.25 below the cheapest (THB 16.25 per 330 mL) and THB 1.62 below the median (THB 16.62). The single-can median depends on S03 and S05, whose containers are inferred (section 11).
- The main median stays at THB 14.05 in sets E, F, H, I, J and P. The position does not depend on the excluded rows.
- The position is a listing position, not a sales result. The team has no sales, shelf or consumer test at THB 15, and the ladder does not show what a shopper would pay for a dissolvable cube.

## 7. Price per serve: the cube against the can

One cube is one 330 mL serve. At the ASSUMPTION price of THB 15 per cube, the cube costs THB 45.45 per litre (DERIVED). Each can price in the table is DERIVED from a pack price that is read on the page (S).

| Comparison | Row | Can price per 330 mL (THB) | Cube per serve (THB, ASSUMPTION price) | Cube minus can (THB) | Cube against the can (percent) |
|---|---|---|---|---|---|
| Singha Lemon Soda single can (Lotus's online) | S01 | 17.00 | 15.00 | -2.00 | -11.8 |
| Singha Lemon Soda 24-can case, per can (7-Eleven ALL Online) | D01 | 13.75 | 15.00 | +1.25 | +9.1 |
| Singha Lemon Soda 24-can case, per can (Lotus's online) | D12 | 13.75 | 15.00 | +1.25 | +9.1 |
| Singha Lemon Soda 24-can case, per can (Makro PRO online) | D06 | 13.54 | 15.00 | +1.46 | +10.8 |
| Singha Lemon Soda 6-can pack, per can (Makro PRO online) | D07 | 13.67 | 15.00 | +1.33 | +9.8 |
| Singha Lemon Soda 6-can pack, per can (Lotus's online) | D13 | 14.17 | 15.00 | +0.83 | +5.9 |
| Singha Sparkling Water Lime 24-can case, per can (7-Eleven ALL Online) | D04 | 12.58 | 15.00 | +2.42 | +19.2 |
| Singha Sparkling Water Lime 24 units, per can (Makro PRO online) | D08 | 13.00 | 15.00 | +2.00 | +15.4 |
| Median of the four single cans (S01, S02, S03, S05) | D | 16.62 | 15.00 | -1.62 | -9.8 |
| Cheapest single can (S02 and S05) | D | 16.25 | 15.00 | -1.25 | -7.7 |
| Singha Sparkling Water Lime launch price (Kaohoon, 17 March 2026, S) | R02 | 15.00 | 15.00 | 0.00 | 0.0 |
| Sprite Lemon Plus 2022 price (Thaiger, 29 August 2022, S, dated) | R01 | 15.23 | 15.00 | -0.23 | -1.5 |

Reading the table. Against the single Singha Lemon Soda can at Lotus's online, the cube is cheaper. The -2.00 figure uses S01, which is not affected by the flavour rule. Against the same can bought in a 24-can case, the cube is about THB 1.25 dearer per serve, and the gap is smaller against the six-can pack at Lotus's. The Singha Sparkling Water Lime is cheaper per can than the cube at both retailers that list it in 24-can cases. The comparison is an online listing per serve against an ASSUMPTION planning price. No store shelf price was read. The cube's cost and ex-factory figures are not part of this record.

## 8. Sugar status

- Singha Lemon Soda (330 mL can): sugar-free and zero calorie on the maker's own page (S, extract; the page was read as an extract, not in full). The page names sucralose and acesulfame potassium, and states that Thailand's FDA approves them. The retailer pages (7-Eleven, Makro, Lotus's) state no sugar claim.
- Singha Sparkling Water Lime (330 mL can): the 7-Eleven page states 0% calorie only. The company's launch statement, as relayed by Kaohoon International (S), says sugar-free. The Makro page states no sugar. Sugar status is therefore a company claim relayed by trade press, not confirmed on a retail page.
- Sprite Lemon Plus: described as sugar-free and calorie-free in the company's launch release of 8 September 2022 (S, extract) and in the Priceza row name (S). The release gives no can size.
- Sprite No Sugar (the Sprite Zero equivalent in Thailand): the Coca-Cola Thailand Sprite products page (readable on 20 October 2026) lists a 325 mL can labelled no-sugar formula (S, extract). Priceza row A03 (Coca-Cola Official Store, 24 cans, THB 334) carries No Sugar in its name. The Lazada row D19 (THB 365) also carries No Sugar in its name, but it is outside set A.
- 7UP No Sugar: sugar-free by name on the Lotus's and Suntory PepsiCo (Priceza) rows.
- Schweppes lime zero and no-sugar variants: sugar-free by name or page (7-Eleven: sugar-free formula; Priceza rows: no-sugar names; the Coca-Cola Thailand Schweppes page lists a no-sugar lime formula, S, extract).
- Regular Sprite, Schweppes lime soda (regular) and Schweppes soda water: no sugar statement on the page. The Makro Schweppes lime soda (regular) row shows a nutrition line with 16 g total carbohydrate (basis not stated). Carbohydrate is shown; sugar is not stated on the page, so the sugar status of that row is not confirmed.
- 7UP NS strawberry-lemon (Lazada, X04): NS is not confirmed on the opened page.

## 9. Conflicts

Each conflict is between this record and a current deck or submission line, or between two sources. File and line numbers are as found on 20 October 2026.

1. Submission 02, situation table (rework/submission/02_situation_analysis.md, line 25): the row "Schweppes Lime Soda Zero Sugar, 6 x 330 ml (Makro online)" at 14 per can, tier "S, SOURCED (S3)". The Makro page (SKU 899900) reads "This item is unavailable in the area you selected". The row should read unavailable in that area. The same brand reads THB 170 for six at 7-Eleven ALL Online (THB 28.33 per can, DERIVED), kept in set A as listed.

2. Submission 02, line 28: "Sprite Zero Sugar, 325 ml (Tops), 16, S, UNVERIFIED (S5)". The 18 October 2026 built-in browser capture of the Tops page (rework/raw/browser_captures_2026-10-18.md, Tops item 1; copied in rework/raw/diligence_2026-10-20/T5/t5_recheck3_live_checks_2026-10-20.md, section 3) prints "16 / can" and "Out Of Stock". That is the only reading of the price. The 20 October product page returned HTTP 403 (re-tried on the second pass). Priceza lists Tops only for the 24-can Sprite at THB 332. The figure is an excluded lead (row X08), not a ladder price. The line should carry the date and the status: "Sprite Zero Sugar, 325 ml (Tops): 16 per can, printed on a Tops page read on 18 October 2026, marked out of stock (tier S)." The UNVERIFIED tag should be removed, because the price is read and dated, though out of stock.

3. Deck content line 121 ("price: can price not verified"), submission 06 (rework/submission/06_kpi.md, line 46, "the Singha Lemon Soda can's price is not verified") and submission 11 (rework/submission/11_mvp_situation_and_product_proposal.md, line 52, the row "Current shelf price | Not verified"): the current Singha can price is recorded as not verified. This pass reads THB 17 for one Singha Lemon Soda can at Lotus's online and pack prices of THB 330 (7-Eleven, Lotus's) and THB 325 (Makro PRO) for 24 cans, which are THB 13.75 and THB 13.54 per can (DERIVED). The text should say that an online listing was read and that no store shelf price was read.

4. Submission 06, line 46: "Cans at 16 and 17 baht (S, UNVERIFIED; Source 3) are leads only". The Lotus's pages read THB 16 (Sprite 325 mL can) and THB 17 (Singha Lemon Soda can) on 20 October 2026 (tier S, SOURCED). They are no longer leads.

5. Submission 04 (rework/submission/04_strategy.md), line 35, the shelf-price line: "The base price is not tied to a verified competitor price". The 20 October listings now benchmark the THB 15 price: THB 0.95 above the median of 31 main listings and THB 1.25 below the cheapest single can read. The THB 15 base remains an ASSUMPTION.

6. Submission 05, line 35 ("ASSUMPTION: not benchmarked; the Singha Lemon Soda can's price is not verified") and submission 06, line 46 ("Shelf 15 baht per cube (ASSUMPTION; range 10 to 20), not benchmarked"): the same point as item 5. The label should read "ASSUMPTION, benchmarked against online listings read on 20 October 2026 (S, DERIVED)".

7. Deck content line 124: "Schweppes zero-sugar 330 mL variants (releases of 3 July 2023 and 24 June 2024; price not found)". Prices are now found for the lime zero variant: THB 170 for six at 7-Eleven ALL Online; THB 196 for twelve and THB 351 for twenty-four at the Coca-Cola Official Store (Priceza); THB 167 for twelve at Lotus's (Priceza). The 2023 and 2024 variants named in the deck are not found in any retail read in this pass.

8. Deck content line 124 and submission 11 line 92: "Sprite 24-pack about THB 15.2 a can (Lazada listing, undated)" and "365 for 24 (about 15.2 each); a second snippet says 354". The Lazada trending page was opened on 20 October 2026 and shows THB 365 for the Sprite and the Sprite No Sugar 24-can packs, with no seller shown on either read. Those rows are outside the main ladder (set F). The THB 354 figure is a search snippet that was not opened, and it is not used.

9. Submission 11, line 93, the row "7UP NS Strawberry Lemon": "75 for 6 (about 12.5 each)", with "NS" read as no sugar, not confirmed. The opened Lazada page reads "7Up Ns Strawberry Lemon6*325Ml" and does not spell out NS. The row is a strawberry-lemon flavour and is outside set A. It stays not confirmed on an opened page.

10. Submission 11, line 125: "Per serve, the can costs THB 16 to 17 (S, 2020 to 2023)". This is a dated figure. It should keep its date beside the 2026 figures.

11. Launch date and release of the Singha Sparkling Water Lime. The submission cites the Boon Rawd Trading release of 13 March 2026 (submission 04, line 73, and submission 03, line 66; tier P). The trade report opened in this pass (Kaohoon International, posted 17 March 2026, tier S) gives the same THB 15 for a 330 ml can. The article quotes the Chief Marketing Officer of Boon Rawd Trading Co., Ltd. It does not mention a company announcement or a release, and it gives no date for any release. The 13 March release was not opened, so the 13 March and 17 March dates are not reconciled. The release is published by Boon Rawd Trading Co., which submission 01 (line 54) says is a different company from the proposer.

12. Lotus's Schweppes lime single can: Priceza shows THB 17 for product code 6709516, and the Lotus's product page read on 20 October shows THB 18. The page (THB 18) is used. The Priceza figure is recorded here and not used.

13. Sprite No Sugar 24-can price: the Priceza row from the Coca-Cola Official Store shows THB 334 (was 384); the Lazada trending page (seller not shown) shows THB 365 (was 384). Both are in the record as separate rows; the Lazada row is outside set A.

14. 7-Eleven ALL Online six-packs against 24-can cases: the Singha six-pack reads THB 172 (THB 28.67 per can) against THB 330 for the 24-can case (THB 13.75 per can), and the Schweppes lime zero six-pack reads THB 170 (THB 28.33 per can). The page gives no cause. Both are kept as listed and tested in set E. The alternative reading of the Singha six-pack (182) is set P (section 4.1, row D02).

15. Tier of retailer pages: the earlier pass tagged the retailer product pages (r01 to r34) as P. A retailer's listing that is read and opened is S under the tier key. This record uses S, and the earlier raw files carry a correction note.

16. Another team record: rework/68b_pepsi_sermsuk.md (line 296 and line 328, as read on 20 October 2026) treats the Lotus's six-pack at THB 75 as "7UP Zero Sugar Strawberry Lemon" and proposes it as the replacement for the "7UP NS Strawberry Lemon" row. The Lotus's page read today (product 171266560) is named "7 UP ZERO SUGAR LEMON SODA 325 ML. PACK6", with no strawberry in the name. The Lazada strawberry-lemon row (THB 75, was THB 85) is a different listing. It stays a sensitivity row here (X04), and the Lotus's lemon row should not replace it.

17. Submission 01, line 11 ("Its price is not verified.") and line 21 ("The Singha Lemon Soda can's price is not verified, so no per-can comparison is drawn from it."). Submission 02, line 26 ("price UNVERIFIED (S7)"), line 35 ("Its price is not verified.") and line 49 ("The Singha Lemon Soda can's price is not verified, so the rungs are not compared with it."). The 20 October reads contradict all of these: THB 17 for a single can at Lotus's online (tier S, SOURCED), and pack prices of THB 330 and THB 325 for 24 cans, which are THB 13.75 and THB 13.54 per can (DERIVED). Replacement wording is in section 12.

18. Tier of the Singha company product page: deck content lines 120 and 126 and submission 02 (S7) tag it S. The tier key gives P only for a company product page read in full. The 20 October reads were WebFetch extracts (English and Thai), so S (extract) stands for this record. The first-pass raw file carried the label P; it is corrected to S (extract) in rework/raw/diligence_2026-10-20/T5/singha_lemon_soda_brand_page_P.md, which keeps the first-pass file name. Deck text needs no change beyond the extract note in section 12. Team records that still tag the page P are listed in section 14.

19. The bottle basis of the 330 mL Sprite 12-pack (sensitivity X01) rests on the Coca-Cola Thailand Sprite products page. That page was readable on 20 October 2026 on a later read, and its sizes come from image file names and alt text only. No submission or deck file cites this row, so no judge-facing text changes. The ladder minimum depends on the classification (section 4.3).

20. Not in the earlier list. Submission 11, line 199: "No volume after 2021 and no current shelf price (the latest verified price is THB 17 for Ume in 2023)." The 20 October reads contradict the statement that no current shelf price exists in the online sense. They show 330 mL on the 2026 pages of the Singha Lemon Soda and THB 17 for a single can at Lotus's. No store shelf price was read. The 2023 Ume figure is not checked in this record.

21. Not in the earlier list. Deck content line 54: "The current lemon can price is not verified." The 20 October reads give THB 17 for a single lemon can at Lotus's and THB 13.54 to THB 13.75 per can in 24-can cases (per-can figures DERIVED from pack prices). No store shelf price was read.

22. Not in the earlier list. Deck content line 57, the note bar: "Not yet verified: line capacity at the group's plants, the can's unit cost, its current shelf price and the retail reach." The current online price was read on 20 October 2026. The shelf price is still not read.

23. Not in the earlier list. Submission 11, line 208: "Competitor prices are undated listings or 2022 figures. No current price has been verified for any competitor." The 20 October reads give online prices for competitor cans: a Sprite single can at THB 16 and a Schweppes lime single can at THB 18 at Lotus's, and 24-can Sprite packs at THB 332 at Lotus's and THB 311 at Makro PRO (tier S, SOURCED; per-can figures DERIVED). No store shelf price was read.

24. Not in the earlier list. Submission 11, line 235: "Not verified: line capacity at the group's plants, the can's unit cost and its current shelf price." The current online price was read on 20 October 2026. The shelf price is still not read.

25. Not in the earlier list. Submission 11, line 52, the row "Current shelf price | Not verified | UNVERIFIED | none found | section 4": this is item 3 above. Replacement wording is in section 12.

26. Not in the earlier list. Team records outside this task still tag the Singha brand page P: rework/68c_osotspa_thaibev_private_label.md (lines 399 and 405, rows Z4 and Z10) and rework/raw/diligence_2026-10-20/T4/68c_round4_singha_schweppes_lime_rows_2026-10-20.md (line 104). The lead should retag them S (extract). No deck, submission or proposal file cites the page.

## 10. Access log: what could not be read

- Big C Online: HTTP 403 on the search page and on five product pages (blocked file, row 1). Not read.
- Tops Online: 20 October 2026: HTTP 403 on the Sprite Zero 325 mL and the Schweppes soda water 330 mL product pages (first pass; the same two pages again on the second pass), and HTTP 403 on the Tops search page and the 7UP page (blocked file, row 8). 18 October 2026: a built-in browser capture of the same two pages printed prices marked Out Of Stock (rework/raw/browser_captures_2026-10-18.md, copied in t5_recheck3_live_checks_2026-10-20.md, section 3). Those are excluded leads (X08, X09). The Heineken 0.0 and Chamm herbal items in the same capture are outside this record. The blocked file also names a Coca-Cola No Sugar single can at 16 in the 18 October capture; the capture does not contain that item, so it is not used (correction note in the blocked file).
- Foodland: HTTP 403 on the home page. A web search found no Foodland Thailand listing for a Sprite can.
- Shopee Thailand: 18 October 2026: two product pages and a search page. The product pages redirected to a traffic-verification page, which was not bypassed; the search page was empty. No listing was reached.
- CP Fresh Mart: the search page (20 October 2026) redirected (HTTP 302) to a third-party host. The redirect was not followed.
- Lazada: the trending page was read on two passes (no seller name shown on either). The Lazada search, tag and product pages on 20 October returned shells without prices or sellers. On 18 October the Lazada route stopped at a reCAPTCHA robot check, which was not solved. No Lazada official-store product page was opened.
- Makro PRO search for Sprite: HTTP 404.
- Lotus's Shop Online search for Sprite: a shell page, no listings.
- 7-Eleven ALL Online search for Sprite: 30 of 273 cards read; only the Schweppes lime zero six-pack matched. The search is flagged unreliable in the blocked file (row 17), because the page carries a notice that a function is unavailable because of a technical problem.
- Coca-Cola Thailand Sprite products page: HTTP 403 on two attempts on 20 October (t5_recheck2_brand_sites_2026-10-20.md, section 1). A later read on 20 October was readable (t5_recheck3_live_checks_2026-10-20.md, section 4). The first-pass extract is also saved.
- Coca-Cola Thailand Sprite brand page: HTTP 403 on one attempt (blocked file, row 15). A later read gave an extract that lists no products and no volumes.
- Suntory PepsiCo company site: HTTP 403.
- Lazada trending page: read on two passes; no seller name shown on either.
- Priceza: the Sprite product page lists ten more offers that were not expanded. The 7UP listing shows 293 products, and about 24 offers were read.
- No browser, login, cart or form was used on 20 October 2026. The 18 October capture used the built-in browser to read pages only; no login, cart, form or verification step was completed. Nothing was bypassed.

## 11. Limits (closed as stated limits)

- Store shelf prices: none read. All prices are online listings, read on 20 October 2026, except the two Tops out-of-stock leads, which were read on 18 October 2026 and are excluded from every ladder. Several 7-Eleven listings carry validity dates that end today (20 October 2026), so those prices may change.
- Single-can prices: 7-Eleven prices for the Singha Lemon Soda and for Sprite were not found online. The 7-Eleven search that would show them is flagged unreliable, so the absence of 7-Eleven single-can prices is not proof. The four-row single-can set rests on three Lotus's pages and one Priceza row.
- Single-can containers: two of the four single-can rows have inferred containers. S03 (the Lotus's Manao single) prints neither a can nor a bottle. S05 (a Priceza row) gives 325 mL with no container word. The single-can median (THB 16.62) depends on both rows. The single-can minimum (THB 16.25) also comes from S02, which has a stated container.
- Singha Lemon Soda: no price at Big C, Tops (out of stock on 18 October), Foodland or Shopee was read.
- Sprite No Sugar single can: no single-can price was found on any opened retailer page. The only Sprite Zero Sugar single-can price in the record is the out-of-stock Tops capture of 18 October 2026 (THB 16, excluded). The 20 October reads found none.
- House brands: no lemon or lime house-brand soda was found at Lotus's or Makro, in the pages or in search. Stated limit.
- Schweppes and 7UP brand sites: the Schweppes Thailand official site and the 7UP Thailand official site were not found by search. The Suntory PepsiCo company site returned HTTP 403. Stated limit.
- The Schweppes lemon variant, and the 2023 and 2024 Schweppes variants named in the deck, were not found in any retail read.
- Sprite Lemon Plus: the only 2026 price is a Priceza row (tier S). The 2022 launch price of THB 15 is dated.
- Container: not stated on several Makro and Lotus's pages. Treated by the container rule in section 2; sets G and H show the effect.
- Makro 330 mL Sprite 12-pack (X01): the page states no container. The bottle reading rests on the sizes in image file names and alt text of the Coca-Cola Thailand Sprite products page, which the page does not print in visible text. Set H shows the effect: minimum THB 11.42, median unchanged. The 135 tier is a buy-more price and is not used.
- Lazada official-store pages: not opened directly. The Lazada search, tag and product pages on 20 October were shells, and the Lazada route stopped at a reCAPTCHA on 18 October. The Priceza LazMall rows (A01 to A15) are the aggregator's merchant prices, not the Lazada page prices.
- Shopee Thailand: a traffic-verification page on 18 October; no listing reached.
- CP Fresh Mart: the search page redirected to a third-party host; no figure from the site.
- Lotus's "/Each" label: read as the pack price (DERIVED). The extract does not confirm it.
- 7-Eleven six-pack gap (section 9, item 14): not explained by any source read. Kept as listed; set E removes both rows. The alternative reading of the 182 price is set P.
- Lazada seller: not shown on either read. Set F shows the effect (median unchanged at THB 14.05).
- Extract reading: all retailer and company figures come from WebFetch text extracts, which are small-model paraphrases, not verbatim copies or browser views. The script's check is a presence check on those extracts, not a parse. An extract can drop a strikethrough or a label. Two second-pass live reads (the Makro 135 label and the Kaohoon attribution) were checked against the extract again and are recorded in t5_recheck3_live_checks_2026-10-20.md.
- Kaohoon date gap: the article is dated 17 March 2026 and names no release date. The 13 March 2026 release cited by the submission was not opened, so the two dates are not reconciled.
- Was-price figures on the Priceza 7UP rows are inferred by the extract from the higher price, since no strikethrough is shown. They are not used in any ladder.
- Priceza prices are merchant prices that Priceza does not guarantee.
- The record does not test purchase intent, shelf presence or any consumer response at THB 15.

## 12. Proposed text for the deck and the submission (for the lead to place)

Nothing below has been edited into the deck or the submission. Each figure carries its tier and date. The text has no dashes, and it names no internal file.

Price check (proposed for the deck price-ladder slide and submission 04). On 20 October 2026 the team read 31 usable can listings of lemon, lime and clear carbonated drinks in 325 to 345 mL cans. The listings come from the 7-Eleven ALL Online, Makro PRO and Lotus's Shop Online product pages, and from Priceza offers by official or named sellers. They are online listings, not store shelf prices (tier S, SOURCED). Per 330 mL the listings run from THB 12.40 to THB 28.67, with a median of THB 14.05 (DERIVED from the listed prices). The top of the range is a six-can pack at 7-Eleven, about twice that retailer's 24-can price per can, and it is kept as listed. Single cans read from THB 16.25 to THB 18.00 per 330 mL. The Singha Lemon Soda single can read THB 17 at Lotus's online.

Position of the planning price (proposed for the deck and submission 04, line 35). The THB 15 planning price is an ASSUMPTION in the financial model. It sits THB 0.95 above the median of these listings and THB 1.25 below the cheapest single can read (THB 16.25 per 330 mL; online listings, tier S, DERIVED).

Per serve (proposed for the deck). Per serve, the cube at the THB 15 planning price (ASSUMPTION) is THB 2.00 below the Singha Lemon Soda single can read online at THB 17 (tier S, read 20 October 2026). It is THB 1.25 above the same can bought as a 24-can case at THB 13.75 per can (pack price THB 330 for 24 cans, tier S, SOURCED; per can DERIVED).

Limits (proposed for the deck and submission). Big C, Tops (out of stock on the one page read on 18 October) and Foodland could not be read (HTTP 403), and Shopee was not reached. Lazada official-store product pages were not opened. The prices are online listings, not store shelf prices. No store price for the single Singha Lemon Soda can was found.

Replacement sentences for the files named in section 9:

- Submission 01, line 11 ("Its price is not verified."): "Online listings read on 20 October 2026 give THB 17 for one can at Lotus's (tier S, SOURCED). Pack prices of THB 330 for 24 cans at 7-Eleven and Lotus's, and THB 325 for 24 cans at Makro PRO, give THB 13.75 and THB 13.54 per can (pack prices tier S, SOURCED; per-can figures DERIVED). No store shelf price was read."
- Submission 01, line 21 ("The Singha Lemon Soda can's price is not verified, so no per-can comparison is drawn from it."): "Online listings read on 20 October 2026 give the Singha Lemon Soda can at THB 17 as a single can at Lotus's (tier S, SOURCED), and at THB 13.54 to THB 13.75 per can in 24-can cases (pack prices tier S, SOURCED; per-can figures DERIVED)."
- Submission 02, line 26 (the Singha can row, "price UNVERIFIED (S7)"): "price read 20 October 2026: THB 17 single can at Lotus's online (tier S, SOURCED); 24-can cases at THB 330 and THB 325 give THB 13.75 and THB 13.54 per can (pack prices tier S, SOURCED; per-can figures DERIVED)."
- Submission 02, line 35 ("Its price is not verified."): "Its online price was read on 20 October 2026 (tier S, SOURCED; see the price check)."
- Submission 02, line 49 ("The Singha Lemon Soda can's price is not verified, so the rungs are not compared with it."): "The Singha Lemon Soda can's online price was read on 20 October 2026 (THB 17 single can at Lotus's, tier S, SOURCED; 24-can cases at THB 13.54 to THB 13.75 per can, with pack prices tier S, SOURCED and per-can figures DERIVED), so the rungs can be compared with it."
- Submission 02, line 28 (Tops Sprite Zero, "16, S, UNVERIFIED (S5)"): "Sprite Zero Sugar, 325 ml (Tops): 16 per can, printed on a Tops page read on 18 October 2026, marked out of stock (tier S)."
- Deck content line 54 ("The current lemon can price is not verified."): "Online listings read on 20 October 2026 give THB 17 for a single lemon can at Lotus's and THB 13.54 to THB 13.75 per can in 24-can cases (pack prices tier S, SOURCED; per-can figures DERIVED). No store shelf price was read."
- Deck content line 57 (note bar): "Not yet verified: line capacity at the group's plants, the can's unit cost and the retail reach. The current online price was read on 20 October 2026 (THB 17 single can at Lotus's); no store shelf price was read."
- Deck content line 120 and line 126 (company product page tagged S): keep S and add "read as an extract on 20 October 2026".
- Deck content line 121 ("price: can price not verified ..."): "price: online listings read 20 October 2026: THB 17 single can (Lotus's, tier S, SOURCED); 24-can cases at THB 330 and THB 325 (tier S, SOURCED), which give THB 13.75 and THB 13.54 per can (DERIVED). No store shelf price was read. The Lemon Soda THB 15 planning price is an ASSUMPTION."
- Deck content line 124, Sprite 24-pack: "Sprite 325 mL, 24 cans: THB 365 on a Lazada listing page (seller not shown; outside the main ladder), read 20 October 2026; tier S. That is THB 15.44 per 330 mL (DERIVED)."
- Deck content line 124, Schweppes zero-sugar variants: "Schweppes lime zero: THB 170 for six at 7-Eleven (online); THB 196 for twelve and THB 351 for twenty-four at the Coca-Cola Official Store; THB 167 for twelve at Lotus's (online, Priceza, tier S, read 20 October 2026). The 2023 and 2024 variants: price not found."
- Deck content line 124, Sprite Lemon Plus: "Sprite Lemon Plus, 325 mL, THB 15 (2022, dated); THB 332 for 24 cans in 2026 (online, Priceza, tier S)."
- Submission 11, line 52 (the row "Current shelf price"): "Current shelf price | Online listings read 20 October 2026: THB 17 single can at Lotus's (tier S, SOURCED); 24-can cases at THB 13.54 to THB 13.75 per can (pack prices tier S, SOURCED; per-can figures DERIVED). No store shelf price read | S, SOURCED | section 4".
- Submission 11, line 199: "The volume after 2021 is 330 mL on the 2026 retailer pages (tier S, SOURCED). Online listings read on 20 October 2026 give THB 17 for a single Singha Lemon Soda can at Lotus's and THB 13.54 to THB 13.75 per can in 24-can cases (pack prices tier S, SOURCED; per-can figures DERIVED). No store shelf price was read."
- Submission 11, line 208: "Online prices were read on 20 October 2026 for competitor cans (tier S, SOURCED; per-can figures DERIVED): a Sprite single can at THB 16 and a Schweppes lime single can at THB 18 at Lotus's, and 24-can Sprite packs at THB 332 at Lotus's and THB 311 at Makro PRO. No store shelf price was read."
- Submission 11, line 235: "Not verified: line capacity at the group's plants and the can's unit cost. The current online price was read on 20 October 2026 (THB 17 single can at Lotus's); no store shelf price was read."
- Submission 04, line 35 (shelf-price line): "The THB 15 base shelf price remains an ASSUMPTION. It is benchmarked against online listings read on 20 October 2026: THB 0.95 above the median of 31 listings and THB 1.25 below the cheapest single can read (tier S, DERIVED)."
- Submission 06, line 46 ("Cans at 16 and 17 baht (S, UNVERIFIED; Source 3) are leads only."): "Single cans read THB 16 (Sprite 325 mL) and THB 17 (Singha Lemon Soda) on Lotus's online on 20 October 2026 (tier S, SOURCED). These are online listings; no store shelf price was read."
- Submission 05 line 35 and submission 06 line 46 (label of the THB 15 price): "ASSUMPTION, benchmarked against online listings read on 20 October 2026 (S, DERIVED)."

Suggested one-line outlier note for the slide range: "The THB 28.67 top of the range is a six-can pack at 7-Eleven, about twice that retailer's 24-can price per can."

## 13. Sources

Retailer and aggregator pages (tier S unless marked). Each was opened on 20 October 2026, except the Tops rows, which were read in a built-in browser on 18 October 2026. The raw file holds the extract text.

| Page (URL) | Retailer or source | Tier | Date read | Raw file |
|---|---|---|---|---|
| https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-ยกลัง-24-กระป๋อง/474313/ | 7-Eleven ALL Online | S | 2026-10-20 | t5_recheck_7eleven_allonline_2026-10-20.md |
| https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-แพ็ก-6-กระป๋อง/514221/ | 7-Eleven ALL Online | S | 2026-10-20 | t5_recheck_7eleven_allonline_2026-10-20.md |
| https://www.allonline.7eleven.co.th/p/ชเวปส์มะนาวโซดาซีโร่-330มล-แพ็ก-6-กระป๋อง/354988/ | 7-Eleven ALL Online | S | 2026-10-20 | t5_recheck_7eleven_allonline_2026-10-20.md |
| https://www.allonline.7eleven.co.th/p/สิงห์สปาร์คกลิ้งไลม์-330-มล-ยกลัง-24-กระป๋อง/327253/ | 7-Eleven ALL Online | S | 2026-10-20 | t5_recheck_7eleven_allonline_2026-10-20.md |
| https://www.allonline.7eleven.co.th/p/เนสท์เล่-เพียวไลฟ์-โซดาพลัส-เลมอนไลม์-330-มลถาด-24-กระป๋อง/327940/ | 7-Eleven ALL Online | S | 2026-10-20 | t5_recheck_7eleven_allonline_2026-10-20.md |
| https://www.allonline.7eleven.co.th/p/โซดาสิงห์-325-มล-แพ็ก-24-ขวด/452565/ | 7-Eleven ALL Online | S | 2026-10-20 | t5_recheck_7eleven_allonline_2026-10-20.md |
| https://www.makro.pro/en/p/179712-7078659719363 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/428706-7350275997891 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/893947-6814746706115 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/699716183874140 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/630907-363090727914101 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/vwmvjuh-6814746476739 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/119581-7416114282691 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/830198-7078660866243 | Makro PRO | S | 2026-10-20 (re-reads: t5_recheck2_makro_830198_2026-10-20.md; t5_recheck3_live_checks_2026-10-20.md, section 2) | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/899900-7499701616835 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.makro.pro/en/p/160629-6761215066307 | Makro PRO | S | 2026-10-20 | t5_recheck_makro_pro_2026-10-20.md |
| https://www.lotuss.com/en/product/169912032 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lotuss.com/en/product/singha-lemon-soda-can-330ml-6-51109221 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lotuss.com/en/product/sprite-soft-drink-original-325ml-x-24pcs-clubpack-150033088 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lotuss.com/en/product/sprite-lemonlime-flavour-soft-drink-325ml-x-6pcs-6808557 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lotuss.com/en/product/171266560 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lotuss.com/en/product/schweppes-sparkling-soda-water-330ml-x-6-cans-75162024 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lotuss.com/en/product/singha-lemon-soda-zero-sugar-lemon-soda-330ml-50986847 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://shopping.lotuss.com/th/product/sprite-lemonlime-flavour-soft-drink-325ml-238945 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://shopping.lotuss.com/en/product/schweppes-soft-drink-lime-soda-330ml-single-6709516 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lotuss.com/en/product/75714334 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lotuss.com/en/product/singha-soda-325-ml-6-24183741 | Lotus's Shop Online | S | 2026-10-20 | t5_recheck_lotuss_2026-10-20.md |
| https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705 | Lazada trending page (seller not shown) | S | 2026-10-20 (first pass and seller check) | t5_recheck_lazada_priceza_2026-10-20.md; t5_recheck2_lazada_seller_2026-10-20.md |
| https://www.priceza.com/p/สไปรท์-เครื่องดื่มอัดลมกระป๋อง-325-มล-sprite-soft-drink-325ml-12341813 | Priceza product page (several sellers) | S | 2026-10-20 | t5_recheck_lazada_priceza_2026-10-20.md |
| https://www.priceza.com/b/groceries/น้ำอัดลม/sprite | Priceza listing (several sellers) | S | 2026-10-20 | t5_recheck_lazada_priceza_2026-10-20.md |
| https://www.priceza.com/s/ราคา/เซเว่นอัพ | Priceza listing (several sellers); listing numbers | S | 2026-10-20 | t5_recheck_lazada_priceza_2026-10-20.md; t5_recheck2_priceza_7up_listing_2026-10-20.md |
| https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา | Priceza listing (several sellers) | S | 2026-10-20 | t5_recheck_lazada_priceza_2026-10-20.md |
| https://www.tops.co.th/en/sprite-soft-drink-zero-sugar-lemon-lime-flavour-325ml-8851959132395 and https://www.tops.co.th/en/schweppes-soda-water-330cc-8851959132647 | Tops Online, built-in browser capture (out of stock) | S | 2026-10-18 | rework/raw/browser_captures_2026-10-18.md; copied in t5_recheck3_live_checks_2026-10-20.md, section 3 |

Maker, brand and press pages (tier as marked; each read as a WebFetch extract, so not in full):

- Coca-Cola Thailand, Sprite products page: https://www.coca-cola.com/th/th/brands/sprite/products. S (extract), 20 October 2026. The first pass and a later read on 20 October were readable (t5_recheck_brands_press_2026-10-20.md, section 1; t5_recheck3_live_checks_2026-10-20.md, section 4). Two other attempts on 20 October returned HTTP 403 (t5_recheck2_brand_sites_2026-10-20.md, section 1).
- Coca-Cola Thailand, Sprite brand page: https://www.coca-cola.com/th/th/brands/sprite. S (extract), 20 October 2026, no product list (t5_recheck2_brand_sites_2026-10-20.md, section 2).
- Coca-Cola Thailand, Schweppes brand page: https://www.coca-cola.com/th/th/brands/schweppes. S (extract), 20 October 2026 (t5_recheck2_brand_sites_2026-10-20.md, section 3).
- Coca-Cola (Thailand) press release on Schweppes zero-sugar fruit sodas: https://www.thaipr.net/?p=3207267. S (company release relayed by a PR agency; extract), dated 28 June 2022, read 20 October 2026 (t5_recheck2_brand_sites_2026-10-20.md, section 4).
- Sprite Lemon Plus launch release: https://www.thaipr.net/?p=3236730. S (company release relayed by a PR agency; extract), dated 8 September 2022, read 20 October 2026 (t5_recheck_brands_press_2026-10-20.md, section 2).
- Thaiger, Sprite Lemon Plus article: https://thethaiger.com/th/news/641196/. S, dated 29 August 2022, read 20 October 2026 (t5_recheck_brands_press_2026-10-20.md, section 3).
- Singha Corporation, Singha Lemon Soda page (English and Thai): https://singhacorporation.com/singhalemonsoda/en/ and https://singhacorporation.com/singhalemonsoda/th/. S (maker's product page read as an extract, not in full), footer 2020, read 20 October 2026 (singha_lemon_soda_brand_page_P.md, which carries the S tier, and t5_recheck_brands_press_2026-10-20.md, section 4).
- Kaohoon International, Singha Sparkling Water Lime article: https://www.kaohooninternational.com/?p=579263. S (trade press quoting the Chief Marketing Officer of Boon Rawd Trading Co., Ltd.; read as an extract), posted 17 March 2026, read 20 October 2026 (t5_recheck_brands_press_2026-10-20.md, section 5; re-read in t5_recheck3_live_checks_2026-10-20.md, section 5).
- Suntory PepsiCo company site: https://www.suntorypepsico.co.th. HTTP 403 on 20 October 2026; not read.

## 14. Files written for this task

- rework/68d_lemon_soda_price_ladder.md (this record, second revision).
- rework/screen/t5_retail_price_ladder.py (the script; checks every row against its saved file, records a passed flag per row, then computes the ladders). Run with python -I.
- rework/screen/t5_retail_price_ladder_results.json (the results file that this record uses; all 51 rows passed on the run that produced it).
- New raw file, in rework/raw/diligence_2026-10-20/T5/: t5_recheck3_live_checks_2026-10-20.md (second-pass live re-reads: Tops 403 today, Makro 830198 label, Coca-Cola Sprite products page readable, Kaohoon attribution; and a copy of the 18 October Tops capture). Earlier new raw files from the first revision: t5_recheck2_priceza_7up_listing_2026-10-20.md; t5_recheck2_makro_830198_2026-10-20.md; t5_recheck2_brand_sites_2026-10-20.md; t5_recheck2_lazada_seller_2026-10-20.md.
- Earlier raw files in the same folder, changed only by appended correction notes or tier labels. Page text is unchanged. t5_recheck_makro_pro_2026-10-20.md (earlier note on the 830198 row); t5_recheck_lazada_priceza_2026-10-20.md (the A15 note; the P label on line 62; a correction note for line 50, which labelled the A05 seller as an official store); t5_recheck_brands_press_2026-10-20.md (tier labels, and correction notes for the Coca-Cola Sprite products page and the Kaohoon article); t5_recheck2_makro_830198_2026-10-20.md (correction note: 135 is the Buy 3+ units tier); t5_recheck2_brand_sites_2026-10-20.md (correction note: the Sprite products page was readable on the later read); t5_recheck_7eleven_allonline_2026-10-20.md (reading note on the 172 and 182 pair, and the 7-Eleven notice); t5_recheck_blocked_and_search_2026-10-20.md (correction note on the Tops 403 and capture); blocked_or_empty_2026-10-20.md (correction note: the Coca-Cola No Sugar 16 item is not in the 18 October capture); singha_lemon_soda_brand_page_P.md (tier changed from P to S (extract), with a correction note; the file name keeps the first-pass label).
- Earlier raw files r01 to r34 and the older captures are not edited.
- rework/README.md is not edited. The T5 brief limits this task's output to the files named, so the index entry is proposed here instead: "68d | Retail price ladder: lemon, lime and clear cans, 325 to 345 mL (T5), revised 20 October 2026 | rework/68d_lemon_soda_price_ladder.md | results: rework/screen/t5_retail_price_ladder_results.json".
- Team records outside this task that still tag the Singha brand page P, for the lead to retag: rework/68c_osotspa_thaibev_private_label.md (rows Z4 and Z10, lines 399 and 405) and rework/raw/diligence_2026-10-20/T4/68c_round4_singha_schweppes_lime_rows_2026-10-20.md (line 104). Not edited here.

## 15. Revision log, first revision (the first verifier's findings and the change made)

| Finding | Change made |
|---|---|
| Set A included two Lazada rows whose seller is not shown (D18, D19). | Moved to set F (sensitivity). The main ladder is now 31 rows, not 34. Below THB 15: 25 of 31 (80.6 percent), not 26 of 34 (76.5 percent). The main median stays at THB 14.05. |
| The flavour rule was not applied to Sprite Chill Lemon Mint (D09 and S04). | Both excluded (sets I and D2). The single-can median is now THB 16.62 (was THB 17.00). The cube's gap to the single-can median is THB 1.62 below (was THB 2.00). The -2.00 gap to the Singha single can (S01) is unchanged. |
| Conflicts not listed: submission 01 (lines 11 and 21), submission 02 (lines 26, 35 and 49), and the company page's tier. | Added as section 9 items 17 and 18, with replacement wording in section 12. The company page tier stays S (extract). |
| Section 7 said "shelf price against shelf price"; the slide text tagged THB 15 without ASSUMPTION and gave THB 17 without "online". | Section 7 now says online listing against an ASSUMPTION planning price. Section 12 tags THB 15 as ASSUMPTION and calls the reads online. |
| The script checked identifiers only; A05 to A07 used a generic brand word; the checks field was hard-coded. | The script checks each row's anchor and printed price (and per-unit price, where printed) in its saved file, and checks the per-unit arithmetic. A05 to A07 use their listing numbers, now in a new raw file (t5_recheck2_priceza_7up_listing_2026-10-20.md). The checks field is computed. |
| The X01 bottle basis (Coca-Cola page) could not be reproduced. | Basis stated as alt text and image file names. The Makro page itself states no container. The container rule is applied. The minimum is shown both ways (THB 11.42 with X01, THB 12.40 without). |
| Brand sites not tried (Schweppes, 7UP). | Tried: Coca-Cola Thailand Sprite (products and brand pages), Coca-Cola Thailand Schweppes, the Coca-Cola Schweppes release (2022), the Suntory PepsiCo company site (HTTP 403), and searches for Schweppes Thailand and 7UP Thailand official sites (not found). Section 3 and section 11 record the outcome. |
| Maker and brand pages tagged P, but read as extracts. | Retagged S (extract), with a note that P applies only when a page is read in full. |
| Leftover P labels in the script comments and a raw note. | Script comments corrected. The raw label on line 62 of t5_recheck_lazada_priceza_2026-10-20.md corrected by an appended note. |
| The A15 raw note said "not used", but the record used the row. | Raw note corrected by an appended note. A15 is in set A, with the price printed on the Priceza product page. |
| Section 12 said "retailer listings" for all 34 rows; the outlier caveat was missing from the slide text. | Section 12 says "retailer and aggregator listings", and a one-line outlier note is proposed for the slide. |
| Sugar wording "points to a sugared product" was stronger than the page supports. | Section 8 now says carbohydrate is shown and sugar is not stated on the page. |
| README index not updated. | Not edited (the T5 brief limits output to the files named). A proposed index line is in section 14. |

## 16. Revision log, second revision (the second verifier's findings and the change made)

| Finding | Change made |
|---|---|
| Medium. The 18 October Tops capture (Sprite Zero Sugar 325 mL at 16; Schweppes soda water 330 cc at 17, both out of stock) was not recorded. The Tops access log did not match the blocked-read file. | Both are recorded as excluded leads X08 and X09 (section 4.3), dated 18 October 2026, tier S, out of stock. Sections 1, 3, 9 (item 2), 10, 11 and 12 are corrected. The Tops access log lists every Tops URL tried and its result. The blocked file's claim of a Coca-Cola No Sugar single can at 16 in that capture is not in the capture file and is not used (correction note in the blocked file). Live re-read today: the Tops Sprite Zero page still returns HTTP 403. |
| Medium. Five judge-facing or deck statements that the 20 October reads contradict were missing from section 9. | Added as section 9 items 20 to 25 (deck content lines 54 and 57; submission 11 lines 199, 208, 235 and 52), with replacement wording in section 12. |
| Medium. The proposed text gave "13.54 to 13.75 per can (tier S, SOURCED)". Per can is DERIVED. | Every proposed sentence in section 12 now tags the pack prices S, SOURCED and the per-can figures DERIVED. Section 9 items 3, 17 and 20 to 23 use the same tags. |
| Medium. The 7-Eleven six-pack page prints 172 and 182 with no label on the selling price. The row had no note, and the alternative maximum was not stated. | Row note on D02 added (section 4.1): the savings line equals 182 minus 172 and the -5% badge points to 172, the pattern also seen on two other 7-Eleven pages. Set P (182 as the selling price) is computed by the script. Maximum under the alternative: THB 30.33 per 330 mL. Median and quartile Q1 unchanged; Q3 unchanged at 14.50. Section 5 range note and section 4.3 (D02alt) updated. |
| Medium. The Kaohoon article was described as trade press relaying the company announcement. The live article quotes the Chief Marketing Officer of Boon Rawd Trading Co., Ltd., mentions no announcement or release, and gives no release date. | The description is corrected in sections 3, 9 (item 11), 13 and 14, the raw file (correction note), the script note for R02, and t5_recheck3_live_checks_2026-10-20.md, section 5. The 13 March versus 17 March gap is kept as unresolved. The officer's name is not reproduced in the record. |
| Medium. Lazada official-store pages were not opened, and the Lazada and Shopee routes were blocked. The access log did not say so. | Coverage table (section 3) and access log (section 10) say so. Section 11 has a limit: Lazada official-store pages not opened; Priceza LazMall rows are merchant prices; the Lazada route stopped at a reCAPTCHA on 18 October; Shopee gave a traffic-verification page. CP Fresh Mart is added as a row. |
| Medium. The brand page file carried tier P (the first-pass label on the header and the Thai section). | Both labels in singha_lemon_soda_brand_page_P.md are changed to S (extract), with a correction note. The verifier cited line 4; the tier label is on line 6, and a second label is on line 21. Both are corrected. Team records 68c (lines 399 and 405) and the T4 raw file (line 104) still tag the page P. They are outside this task and are listed for the lead in section 9 item 26 and section 14. No deck, submission or proposal file cites the page. |
| Low. The A05 first-pass raw line labelled the 7UP No Sugar 24-can row as an official store. | A correction note is appended to t5_recheck_lazada_priceza_2026-10-20.md. Row A05 in section 2 and section 4.1 keeps the brand owner's LazMall account wording, with no official-store label. |
| Low. checks_passed was a gate, not an independent result. | The script now records a passed flag and the matched text for every row, counts the rows that passed, and stops with no output if any row fails. The results file reports rows_checked (51), rows_passed (51) and all_rows_pass. |
| Low. D05 and D14 were described as "regular by name", and X04 as "no sugar (name)". The names do not say either. | D05 and D14 now read "not stated (the name does not say regular or no sugar; the page does not say)". X04 reads "NS not confirmed on the opened page" in the record and the script; the "no sugar (name)" entry is removed from the script and the results JSON. |
| Low. The Makro 830198 page prints 135 under "Buy 3+ units", which the record did not mention. The later raw file described the 135 as beside the 137 with a -1% label. | The X01 row (section 4.3) notes the 135 buy-more tier. The live re-read (t5_recheck3, section 2) confirms the label. The later raw file has a correction note. The 137 pack price is kept because 137 divided by 12 gives the printed per-unit 11.42. |
| Low. The Coca-Cola Thailand Sprite products page was recorded as HTTP 403 on later attempts, so the X01 bottle basis "could not be re-checked". | The page was readable on a later read on 20 October 2026. Section 3, section 4.3 (X01 note), section 10, section 11 and section 13 record the successful read. The basis still rests on image file names and alt text, and set H is kept. |
| Low. The 7-Eleven pages carry a notice that a function is unavailable, and the search was flagged unreliable. | Caveat added to section 3, section 10 and section 11: the absence of 7-Eleven single-can Sprite or Singha prices is not proof. |
| Low. S03 (container inferred; the page prints neither can nor bottle) and S05 (a Priceza row without a container word) are inferred. The single-can median depends on both. | Section 4.2 row notes and section 11 limit added: the single-can median depends on S03 and S05, and the minimum also comes from S02. Section 6 notes the same. |
