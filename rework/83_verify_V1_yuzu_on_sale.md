# V1 verification: is Singha Yuzu soda on sale in Thailand in October 2026?

Date of check: 20 October 2026 (first version), revised 20 October 2026 after review
Item: V1, from rework/workflows/update_loop_state_2026-10-20.md, section 5, item 1
Product: Singha Yuzu Lemon Soda (the Yuzu flavour of the Singha Lemon Soda range, 330 mL can)
Evidence folder: rework/raw/update_2026-10-20/V1/ (files 01 to 14)
Governing rules: rework/SOURCING_POLICY.md and CLAUDE.md
Review file: rework/workflows/update_loop_review_2026-10-20.md, section V1

Revision note. The first version closed Yuzu as a limit and said no Thai store page gave a Yuzu listing. The reviewer found that wrong: the first pass opened only store search pages and home pages, which are shells, and never located product pages. This version re-runs the retailer step with searches limited to makro.pro, tops.co.th, bigc.co.th, allonline.7eleven.co.th, lotuss.com and lazada.co.th, and opens each Yuzu product page it can. Section 8 lists every reviewer finding and how it was handled.

## 1. Answer

Singha Yuzu Lemon Soda product pages exist online. Whether the can can be bought in Thailand in October 2026 is not confirmed.

What is shown, from pages opened and read on 20 October 2026:

- Makro PRO has two Yuzu products with a price on the page: a 6-pack at THB 84 (THB 14.00 a unit) and a 24-pack at THB 324 (THB 13.50 a unit). Both pages carry a delivery-area notice and no date. Gourmet Market Thailand has a "Pack 5+1" page at THB 85.00 with no stock statement, and the listing carries no date. Lazada has a 24-can Yuzu page with no price, seller or stock. Singha Online has a Yuzu tray page whose body does not load. Singha's own brand page shows a Yuzu card, undated.
- Against this, the evidence leans toward limited or no current availability, without proving it. Makro PRO's own "Singha Online" collection lists 15 products and none is Yuzu. The 7-Eleven ALL Online Singha shop pages list Lemon, Red, Pink, Ume, Watermelon, Lemon Cream and Sparkling Lime and no Yuzu, and the Yuzu product URL that the search index holds for 7-Eleven returns HTTP 404. Lotus's pages and searches show no Singha Yuzu. Tops and Big C hold Yuzu product pages, which could not be opened; the search tool's summaries of them say out of stock (Tops) and "Available soon" (Big C). Those summaries are leads only.
- No opened page shows an explicit out-of-stock label for Yuzu, and no opened page shows a date on which the can could be bought. The Makro notice is an area notice, and it also sits on a Singha Ume 24-pack page that other shops show with a price (section 3b).

Verdict: partly closed. The question whether Yuzu product pages exist online is answered. The question whether the can is purchasable in October 2026 is closed as a stated limit. The fact "on sale in Thailand in October 2026" stays UNVERIFIED. The route that would settle it is in section 6.

## 2. Routes tried

Route A, run in the first pass (store search pages and home pages). These returned shells and told nothing about product pages:

- Singha brand pages: singhacorporation.com/singhalemonsoda/en/ and /th/ (opened, Yuzu card present, undated; file 01). singha.com (age-gate for Singha Beer, no Lemon Soda list).
- Singha Online Shop root and the short link bit.ly/3PVAfiI (header and footer only; file 02).
- 7-Eleven ALL Online search page and home page, Lotus's search page, Makro PRO home page (cut off in the fetch) and a guessed Makro search path (HTTP 404), Big C and Tops search pages (HTTP 403), Shopee and Lazada search pages (empty shells or a title only). File 03 records these and now carries a correction note.
- Dan Murphy's (Australia) returned HTTP 403 and is not a Thai retailer, so it is not used.

Route B, run in this revision (the product-page route). WebSearch limited to one retail domain at a time, then WebFetch on each Yuzu product page the search listed, and on control pages:

- makro.pro: search found the Yuzu x6 page (two URLs) and the Yuzu x24 page. All three opened (file 05). The "Singha Online" collection page opened (file 06). Seven non-Yuzu Singha lemon soda pages opened as controls (file 07).
- gourmetmarketthailand.com: the page given by the reviewer opened (file 08).
- lazada.co.th: the 24-can Yuzu page and the tag page opened with no price; one older Yuzu product URL returned HTTP 404 (file 09).
- allonline.7eleven.co.th: three Singha shop pages opened, no Yuzu in them; the Yuzu product URL in the search index returned HTTP 404 in three URL forms (file 10).
- lotuss.com: the soda category page and a Singha Lemon Soda product page opened, no Yuzu; three searches found no Yuzu page (file 11).
- tops.co.th and bigc.co.th: search listed Yuzu product pages. All seven URLs tried returned HTTP 403 to the fetch tool. One Tops page and one Big C page were also tried in the built-in browser pane as ordinary page views, and the tool refused both navigations. They were not retried (file 12).
- singhaonline.com: a search limited to Singha domains found the shop's Yuzu tray page and a control Ume page; both opened (file 13).
- The search log, with the queries and result titles, is file 14.

The team's earlier pass (rework/raw/diligence_2026-10-20/T6/04_retail_listings_2026-10-20.md) recorded no Yuzu among nine retailer pages. It is a team record and not a source here. This revision found Yuzu product pages that pass did not.

## 3. Listings found

### 3a. Yuzu listings opened on 20 October 2026 (tier S, SOURCED as secondary, none carries a listing date)

| Retailer | Product as titled | Pack | Price read (THB) | Per unit | Date read | Date on listing | Notice quoted exactly | URL | File |
|---|---|---|---|---|---|---|---|---|---|
| Makro PRO | SINGHA Yuzu Lemon Soda 330 ml x 6 | 6 cans of 330 mL | 84 | 14.00 (page) | 20 Oct 2026 | none | "This item is unavailable in the area you selected" | https://www.makro.pro/en/p/898530-7325020881091 | 05 |
| Makro PRO (second URL, same product, code 898530) | SINGHA Yuzu Lemon Soda 330 ml x 6 | 6 cans | 84 | 14.00 (page) | 20 Oct 2026 | none | "This item is unavailable in the area you selected" | https://www.makro.pro/en/p/cfar5hht-7325020881091 | 05 |
| Makro PRO | สิงห์ ยูสุเลมอน โซดา 330 มล. x 24 | 24 cans | 324 | 13.50 (page) | 20 Oct 2026 | none | "สินค้านี้ ไม่สามารถจัดส่งได้ในพื้นที่ที่คุณเลือก" | https://www.makro.pro/th/p/431132-7497422667971 | 05 |
| Gourmet Market Thailand | Singha Yuzu Lemon Soda 330ML. Pack 5+1 | 6 cans (5+1) | 85.00 per pack ("/Each") | 14.17 (DERIVED, 85 divided by 6) | 20 Oct 2026 | none for the listing; "Last update 21 Aug 2025, 22:22" belongs to the store panel | "Delivery covered Bangkok / Vicinity and Other Provinces in Thailand"; no stock statement | https://gourmetmarketthailand.com/en/singha_yuzu_lemon_soda_330ml_pack_51_8850999018522 | 08 |
| Lazada Thailand | SINGHA YUZU LEMON SODA สิงห์เลมอนโซดา รสส้มยูสุ 330 มล. x 24 กระป๋อง | 24 cans | no price shown | not shown | 20 Oct 2026 | none | no delivery-area text; no seller; no stock | https://h5.lazada.co.th/products/singha-yuzu-lemon-soda-330-x-24-i5851059542.html | 09 |
| Singha Online Shop | สิงห์เลมอนโซดา รสส้มยูซุ 1 ถาด | tray | no price shown | not shown | 20 Oct 2026 | none | stock line "ไม่พบสินค้า" (our translation: "Product not found"), the same string as on the Ume page | https://singhaonline.com/product/singha-yuzu-lemon-soda-can-10046830100 | 13 |

Translation of the Makro Thai notice is ours: "This product cannot be delivered to the area you selected."

Conflict noted under SOURCING_POLICY rule 5. The search tool's summary of the Makro 6-pack said THB 80 (down from THB 82, THB 13.67 a unit). The opened page reads THB 84 and THB 14.00. The summary was not opened as a page, so the opened page governs. Makro also prices one product differently on different pages (Lemon 6-pack: THB 82 on the collection page and THB 78 on its product page), so the Makro Yuzu prices are page prices at the time of reading and not firm prices.

### 3b. Evidence that points to limited or no current availability (opened pages)

| Observation | Source and file | Tier |
|---|---|---|
| Makro PRO's "Singha Online" collection shows "Showing products 1-15 of 15" and none of the 15 names contains Yuzu. It lists Lemon x6 and x24, Red x6 and x24, Ume x6, Singha water and soda, and PURRA. | https://www.makro.pro/en/c/collections/Singha%20Online, file 06 | S |
| The same collection omits the Ume 24-pack and the Pink packs, whose product pages exist and are priced. So absence from the collection means "not in this collection" and does not by itself mean "not sold". | files 06 and 07 | S |
| The Makro delivery-area notice sits on 3 of the 9 Singha lemon soda product pages read: Yuzu x6, Yuzu x24 and Ume x24. It is absent on Lemon x6, Lemon x24, Red x24, Pink x24, Pink x6 and Ume x6. So the notice is not Yuzu-only. | file 07 | S, count DERIVED |
| 7-Eleven ALL Online Singha shop pages (5 products in the Lemon Soda group, 15 in beverages, about 150 tiles at the root) list no Yuzu. | https://www.allonline.7eleven.co.th/s/singha/singha-lemon-soda/ and two sibling pages, file 10 | S |
| The 7-Eleven Yuzu product URL (ID 512969) held by the search index returned HTTP 404 in three URL forms. | file 10d | S (observation of the result) |
| Lotus's: the soda category page and a Singha Lemon Soda page show no Yuzu, and three searches found no Singha Yuzu page. | file 11 | S |
| Lazada: the 24-can Yuzu page shows no price, seller or stock. | file 09 | S |

### 3c. Leads not opened (snippet, not opened, SOURCING_POLICY rule 8; status UNVERIFIED)

| Retailer | What the search tool's summary said | Why not opened | File |
|---|---|---|---|
| Tops | Yuzu 6-pack, 85 THB, "Out Of Stock"; Yuzu single can, 17 THB, out of stock | HTTP 403 to the fetch tool; browser pane refused | 12 |
| Big C | Yuzu single can ฿11 (down 35% from ฿17) with "Available soon"; 6-pack ฿42 (down 50% from ฿85); 24-pack ฿325, coming soon | HTTP 403; browser pane refused | 12 |
| 7-Eleven ALL Online | Yuzu 24-can case ฿330 against ฿408 (-19%), "ขออภัยสินค้าหมด" (our translation: "Sorry, out of stock") | HTTP 404 | 10d |
| Lazada | several listings out of stock; one shipping notice limits delivery to Bangkok, surroundings and some northern provinces | summary of a search, no page behind it | 09d |

These are leads that agree with each other. None is a figure in this record.

### 3d. Dated Thai press and other mentions (carried forward from the first version; none is an October 2026 listing)

| Date read in source | Source | Pack | Price (baht) | Channel named | Yuzu named as current? | URL |
|---|---|---|---|---|---|---|
| 4 June 2021 (04 มิ.ย. 64) | Thansettakij | not stated | not stated | not named | launch | https://www.thansettakij.com/business/482657 |
| 8 June 2021 (read from "08/06/2021", format not stated) | Brand Inside | 330 mL can | 16 | 7-Eleven nationwide, Singha Online Shop | launch | https://brandinside.asia/?p=111815 |
| 15 August 2022 | Thansettakij | 330 mL can (Red) | 16 (for Red, not Yuzu) | 7-Eleven first, then modern and traditional trade | 2 flavours named, Yuzu one of them | https://www.thansettakij.com/business/marketing/536655 |
| 25 June 2024 | Marketeer Online | 330 mL can (line) | 17 (line, not per flavour) | 7-Eleven, Lotus's, Makro, leading stores, Singha Online Shop | yes (5 flavours) | https://marketeeronline.co/archives/360326 |
| 2 April 2025 (read from "02/04/2025", order not stated) | Marketeer Online (Melon) | not stated | not stated | 7-Eleven nationwide, Singha Online Shop | yes (earlier flavour list) | https://marketeeronline.co/archives/408963 |
| 4 April 2025 | Brand Buffet (Melon) | not stated | not stated | Melon only: 7-Eleven, Singha Online Shop | yes (current range list) | https://www.brandbuffet.in.th/2025/04/singha-melon-lemon-soda/ |
| 10 to 11 November 2025 | Mitihoon, Marketing Oops, Brand Inside (Lemon Cream) | 330 mL can (Lemon Cream only) | not stated | 7-Eleven, department stores, supermarkets | no (Yuzu not named) | https://www.mitihoon.com/2025/11/10/592824/ |
| 9 April 2026 | Brand Buffet (Halls XS candy) | box, not a can | 29 (box of candy) | 7-Eleven and leading stores | no (Yuzu not named) | https://www.brandbuffet.in.th/2026/04/singha-lemon-soda-x-hall-xs/ |
| 18 August 2026 | Kaohoon International (Korea) | 355 mL can (Korea) | not Thai | South Korea | Korea only | https://www.kaohooninternational.com/markets/588867 |

Note on the 2024 price: the 17 baht sentence in the 25 June 2024 article states the can price for the line. It does not state a price per flavour.

Note on the 2022 price: the 16 baht sentence in the 15 August 2022 article refers to Singha Red Lemon Soda. A search summary that tied 16 baht to Yuzu was wrong on this point.

## 4. Figures and tiers

Tiers follow the rules of this run: P is regulator text, a company filing or release read in full, official statistics or a primary database; S is any other page read and opened. No figure in this record is tier P.

- F1. Singha Yuzu Lemon Soda is listed as a flavour card on the maker's brand page, 330 ML, "no sugar. No calories, high in vitamin C". Tier S, status COMPANY CLAIM, undated. SOURCING_POLICY section 1 would class the maker's product page as primary, but this page is undated marketing copy, so it is held at S for this run. It supports "Singha lists Yuzu on its brand page" and does not support "on sale now". Source: https://singhacorporation.com/singhalemonsoda/en/ and /th/. Date read 20 October 2026. Saved: 01_singha_brand_page_lemon_soda.md.
- F2. Yuzu launch, June 2021, 330 mL can at 16 baht, sold at 7-Eleven nationwide and Singha Online Shop. Tier S, SOURCED (secondary, labelled), dated 8 June 2021 as read from the page. Source: https://brandinside.asia/?p=111815. Saved: 04_thai_press_dated_mentions.md, section 4a.
- F3. Singha Lemon Soda line, 330 mL can, 17 baht, sold at 7-Eleven, Lotus's, Makro and leading stores including Singha Online Shop. Tier S, SOURCED (secondary), dated 25 June 2024. This is not an October 2026 price. Source: https://marketeeronline.co/archives/360326. Saved: 04, section 4c.
- F4. Yuzu named as part of the current Singha Lemon Soda range, April 2025. Tier S, SOURCED (secondary), dated 4 April 2025 and 2 April 2025. Sources: https://www.brandbuffet.in.th/2025/04/singha-melon-lemon-soda/ and https://marketeeronline.co/archives/408963. Saved: 04, sections 4d and 4e.
- F5. Yuzu sold in South Korea in August 2026 (three flavours: Lemon, Yuzu, Lime Lemon). Tier S, SOURCED (secondary), dated 18 August 2026. Korea only. It is not evidence for Thailand. Source: https://www.kaohooninternational.com/markets/588867. Saved: 04, section 4h.
- F6. Singha Yuzu Lemon Soda on sale in Thailand in October 2026. UNVERIFIED. Product pages exist (F9 to F11, F15, F16) but none shows that the can can be bought in October 2026 (section 5).
- F7. Red Lemon Soda launch price, 16 baht, 330 mL can, August 2022. Tier S, dated. Not Yuzu. Source: https://www.thansettakij.com/business/marketing/536655. Saved: 04, section 4b.
- F8. Yuzu launch date, 4 June 2021 (sugar-free formula named in the article). Tier S, dated. Source: https://www.thansettakij.com/business/482657. Saved: 04, section 4a.
- F9. Makro PRO, SINGHA Yuzu Lemon Soda 330 ml x 6: THB 84, THB 14.00 a unit, delivery-area notice "This item is unavailable in the area you selected", no date. Tier S, SOURCED (secondary). Date read 20 October 2026. Source: https://www.makro.pro/en/p/898530-7325020881091 (also https://www.makro.pro/en/p/cfar5hht-7325020881091). Saved: 05_makro_pro_yuzu_product_pages.md.
- F10. Makro PRO, สิงห์ ยูสุเลมอน โซดา 330 มล. x 24: THB 324, THB 13.50 a unit, notice "สินค้านี้ ไม่สามารถจัดส่งได้ในพื้นที่ที่คุณเลือก", no date. Tier S, SOURCED (secondary). Date read 20 October 2026. Source: https://www.makro.pro/th/p/431132-7497422667971. Saved: 05.
- F11. Gourmet Market Thailand, Singha Yuzu Lemon Soda 330ML. Pack 5+1: THB 85.00, listing undated, no stock statement. The "Last update 21 Aug 2025, 22:22" text is in the store panel and is not the listing date. Tier S, SOURCED (secondary). Date read 20 October 2026. Source: https://gourmetmarketthailand.com/en/singha_yuzu_lemon_soda_330ml_pack_51_8850999018522. Saved: 08_gourmet_market_yuzu_listing.md.
- F12. Makro PRO "Singha Online" collection: 15 products, none Yuzu. Tier S, SOURCED (secondary). Date read 20 October 2026. Source: https://www.makro.pro/en/c/collections/Singha%20Online. Saved: 06_makro_pro_singha_online_collection.md.
- F13. Makro delivery-area notice on 3 of 9 Singha lemon soda product pages (Yuzu x6, Yuzu x24, Ume x24); absent on the other 6. Tier S, count DERIVED. Saved: 07_makro_pro_control_pages.md.
- F14. 7-Eleven ALL Online Singha shop pages list no Yuzu (5, 15 and about 150 tiles); the indexed Yuzu product URL returns HTTP 404. Tier S. Date read 20 October 2026. Source: https://www.allonline.7eleven.co.th/s/singha/singha-lemon-soda/ and siblings. Saved: 10_seven_eleven_singha_pages.md.
- F15. Lazada Thailand 24-can Yuzu page exists, with no price, seller, stock or date. Tier S. Date read 20 October 2026. Source: https://h5.lazada.co.th/products/singha-yuzu-lemon-soda-330-x-24-i5851059542.html. Saved: 09_lazada_yuzu_pages.md.
- F16. Singha Online Shop Yuzu tray page exists; its body does not load; "ไม่พบสินค้า" also appears on the Ume page, so it is not read as a stock signal. Tier S. Date read 20 October 2026. Source: https://singhaonline.com/product/singha-yuzu-lemon-soda-can-10046830100. Saved: 13_singha_online_product_pages.md.
- F17. Tops and Big C Yuzu stock wording ("Out Of Stock", "Available soon") and prices (THB 85, 17, 11, 42, 325). Search-tool summaries only, snippet, not opened, UNVERIFIED. Saved: 12_tops_bigc_unopened_leads.md.
- F18. Lotus's Shop Online: no Singha Yuzu page found; two pages opened show none. Tier S, absence in a partial search. Saved: 11_lotuss_pages.md.

Figures not used: the Dan Murphy's (Australia) listing claims (zero sugar, zero calorie, 30.7 mg vitamin C, country of origin Thailand); the page returned HTTP 403, so the claims are search-snippet leads only. The Kantar "Brand Footprint 2025 Thailand" snippet about a 2024 Yuzu launch: the opened page did not mention Singha, so it is not used. The Makro search summary prices (THB 80, THB 13.67) that conflict with the opened page. The Makro "discontinued" claim for Lemon x24 (not seen on the opened page).

## 5. Limits (stated, not open items)

1. October 2026 purchasability of the Yuzu can is not confirmed. The pages that exist show prices with no validity date, and no opened page shows a purchase being possible. The status "on sale in Thailand in October 2026" is UNVERIFIED.
2. The Tops and Big C Yuzu product pages could not be opened (HTTP 403 for all seven URLs, and the built-in browser pane refused both navigations tried). Their stock wording is snippet only (section 3c).
3. The 7-Eleven ALL Online Yuzu product page that the search index lists returned HTTP 404 in three URL forms. Its content is snippet only. A 404 can mean the product page was removed or that the tool was blocked, and the pages do not say which.
4. The Makro delivery-area notice names "the area you selected". The fetch tool selects no area, so the area is not shown. The notice also sits on a Singha Ume 24-pack page, so it is not a Yuzu-only signal. No Makro page carries a validity date, and Makro prices for one product differ between pages, so the Makro Yuzu prices are page prices at the time of reading.
5. The Lazada Yuzu pages and the Singha Online Yuzu page give no price, seller or stock in the extracted text. This is a limit of the fetch tool on script-loaded pages and is not a finding about stock.
6. The Gourmet Market listing has no date. The 21 August 2025 timestamp belongs to the store panel and is not used as the listing date.
7. The Singha brand page carries no date. Its footer reads 2020, most likely template text.
8. The newest dated Thai item that names Yuzu as current is 4 April 2025. The November 2025 and April 2026 Thai items name other flavours or none. Absence in those items is not proof that Yuzu is off sale.
9. Two Thai press dates are numeric and their order is not shown on the page (08/06/2021 and 02/04/2025). They are read as dd/mm. The order is a stated risk.
10. The fetch tool returns an extracted answer to the prompt, not a byte copy of the page. The saved files hold the extracted text and the quoted strings as the tool returned them. A raw page capture was not saved, and I did not check any quote against the raw page.
11. The Thai sentences are quoted as extracted. Translations are ours and are labelled in the evidence files.
12. Search-tool summaries disagreed with opened pages in three places (file 14). The opened pages govern, and the summaries are not used as figures.
13. A 2026 Yuzu shelf price is not found. The only Yuzu prices read are page prices of THB 84, 324 and 85 (undated, not confirmed purchasable) and the older press prices of 16 baht (2021 launch) and a line price of 17 baht (June 2024).
14. Shopee Thailand was not re-searched in this revision because it was not in the list of domains for the retailer step. The first pass found an empty shell there.

## 6. Route that would settle it

Run in this session (no contact, no account, no form): the product-page route. Domain-restricted search found Yuzu product pages at Makro PRO, Gourmet Market, Lazada and Singha Online, and the opened pages gave the prices and notices in section 3a. It showed that Yuzu product pages exist and that purchasability is not confirmed. It did not show a shelf price, an in-stock status, or what the Makro notice refers to.

What this route could not open, and what still needs a person in Thailand using an ordinary browser on a dated day, saving the page text and the URL:

- The Tops and Big C Yuzu product pages (section 12a of file 12), and the 7-Eleven Yuzu product page (ID 512969), which returned HTTP 403 or 404 here.
- The two Makro Yuzu pages with a Thai delivery area chosen in the page (for example a Bangkok postcode), to see whether the notice changes. This is a page setting, not an account.
- The shelf: the pack, the shelf price, the date and a photo with the store name, at 7-Eleven, Lotus's, Makro and Big C in Bangkok. This is the only route that shows in-stock status on the shelf.
- Outside contact with Boon Rawd Trading or Singha Corporation to confirm the range. This needs the user's approval first and is not run here.

Until one of these is done, any judge-facing sentence that says the Yuzu can is on sale now is not supported by the sources in this record. A sentence that says Singha lists Yuzu on its brand page is supported only as a COMPANY CLAIM with no date. A sentence that says Yuzu product pages exist at online retailers is supported as of 20 October 2026, with the delivery-area notice and the absence from several current ranges stated beside it.

## 7. What changes in the repo

Nothing has been changed in rework/deck, rework/submission or rework/proposal. This record and the evidence folder (rework/raw/update_2026-10-20/V1/, files 01 to 14) are the only changed files. In the evidence folder, files 01, 02 and 03 carry correction notes and files 05 to 14 are new.

## 8. Review findings and how each was handled

| Finding | Severity | Handled | Where |
|---|---|---|---|
| The record says no Thai store page gave a Yuzu listing and blames tool limits; product pages were never located. Domain-restricted searches find Makro PRO (THB 84 and THB 324, with delivery-area notices) and Gourmet Market (THB 85, undated listing). | high | Closed. Retailer step re-run with domain-restricted searches on all six named domains. Each Yuzu page that opens is saved and recorded with price, pack, date read, URL and the notice quoted exactly. Gourmet Market marked as undated for the listing. Answer rewritten to say Yuzu product pages exist and October 2026 purchasability is not confirmed. | sections 1, 2, 3a; files 05, 08, 14 |
| Evidence pointing to unavailability is missing: the Makro "Singha Online" collection lists 15 products without Yuzu; Tops, 7-Eleven and Big C snippets say out of stock or available soon; the Lazada page opens with no price. | medium | Closed. The Makro collection is recorded as an opened page (tier S). Tops, Big C and 7-Eleven items are recorded as snippet, not opened, with the attempts to open them. The Lazada page is recorded as opened with no price, seller or stock. Status kept UNVERIFIED and the answer says the evidence leans toward limited or no current availability. Added two things the reviewer did not list: the 7-Eleven shop pages that list no Yuzu, and the Makro control pages that show the delivery-area notice is not Yuzu-only. | sections 1, 3b, 3c, 5; files 06, 07, 09, 10, 12 |
| Section 6 and the result say only a team store visit or browser capture would settle it; a no-contact route (product pages found by domain-restricted search) was available and unused; the Makro check was called "cut off". | medium | Closed. Section 2 now lists the product-page route and what it showed. Section 6 says it was run and keeps the store visit and dated browser capture only for shelf price, in-stock status and the pages that returned 403 or 404. Limit 1 and the old "cut off" wording are replaced. | sections 2, 5, 6 |
| F1 is tiered P though the brand page is undated marketing copy. | low | Closed. F1 relabelled "S, COMPANY CLAIM, undated", with the note that it supports "Singha lists Yuzu" and not "on sale now". File 01 carries the same change. | section 4; file 01 |

Reviewer statements checked and found correct: Makro PRO "SINGHA Yuzu Lemon Soda 330 ml x 6" at THB 84 and THB 14.00 a unit on both URLs; "สิงห์ ยูสุเลมอน โซดา 330 มล. x 24" at THB 324 and THB 13.50 a unit; both carry the delivery-area notice and no validity date; Gourmet Market at THB 85.00 with "Last update 21 Aug 2025" in the store panel; the Makro "Singha Online" collection lists 15 products with no Yuzu (Lemon x6 and x24, Red x6 and x24, Ume x6, Singha water and soda, PURRA); the Lazada 24-can page opens with no price, seller or stock. The reviewer also said the Tops, 7-Eleven and Big C pages returned 403 or 404 and could not be opened. That held here too (Tops and Big C 403, the 7-Eleven Yuzu page 404), and a further attempt through the built-in browser pane was refused for both Tops and Big C.

## Revision 20 October 2026 (aggregator counter-lead)

A reviewer found a counter-lead the first pass missed. The Priceza search page for "สิงห์เลมอนโซดา" (https://www.priceza.com/s/ราคา/สิงห์เลมอนโซดา, opened 20 October 2026; saved as rework/raw/update_2026-10-20/V1/15_priceza_singha_lemon_soda_search.md, tier S) carries the row "สิงห์ ยูซุ เลมอนโซดา กระป๋อง 330มล. SINGHA (51614348)" at Lotus's Shop Online for THB 17, on a page stamped 20 October 2026. The same page shows Yuzu rows at marketplace sellers (Lazada, ALL ONLINE, Makro PRO and Tops Online).

Effect on the answer: Yuzu is listed for sale online by at least one retailer on the date the page was read (aggregator row, S). The page shows no stock status, so the status of October 2026 purchasability stays UNVERIFIED. A listing on an aggregator is not proof that the can can be bought, because a row can stay after a product is withdrawn.
