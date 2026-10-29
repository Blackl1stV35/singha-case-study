# Retail price rows used in the T3 record, with the pages they come from (T3)

These rows were read and saved by other tasks of the same run (T4 for est, T5 for 7UP, Sprite, Singha and Schweppes, and an earlier capture for Pepsi). T3 did not re-open the retailer pages (the web search budget was used up, and the pages are already saved with URL, date and extract). Each row below was copied from the saved page named in its last column. Tier S (retailer online listings and one price aggregator). Prices are single snapshots dated by the read date, and the listings carry no date of their own.

Unit price per 330 mL in the T3 record is computed by rework/screen/t3_pepsi_sermsuk_margins.py (results in rework/screen/t3_pepsi_sermsuk_margins_results.json).

| Item | Pack | Price (THB) | Retailer and row | Read | Saved page |
|---|---|---|---|---|---|
| 7UP Zero Sugar Lemon Soda | 6 x 325 mL (PACK6; the page does not use the word can) | 75 (listed 80, struck; "-6%" badge; page prints "฿75.00/Each") | Lotus's, row L5, https://www.lotuss.com/en/product/171266560 | 20 Oct 2026 | T5/lotuss_2026-10-20.md |
| 7UP Zero Sugar Strawberry Lemon | 6 x 325 mL (printed as PACK 6) | 75 (listed 80, struck) | Lotus's, row L6, https://shopping.lotuss.com/en/product/171356661 | 20 Oct 2026 | T5/lotuss_2026-10-20.md |
| 7UP no-sugar lemon soda, 325 mL | single can | 16 | Lotus's Shop Online row on Priceza page P3 (https://www.priceza.com/s/ราคา/เซเว่นอัพ); the Lotus's pre-production host shows the same 16 and is not used | 20 Oct 2026 | T5/priceza_aggregator_2026-10-20.md |
| 7UP lemon soda no sugar, official Suntory PepsiCo store on LazMall | 6 / 12 / 24 cans of 325 mL | 96 / 161 (was 192) / 293 (was 384) | Priceza page P3 | 20 Oct 2026 | T5/priceza_aggregator_2026-10-20.md |
| Sprite 325 mL | 6 cans | 85 | Lotus's, row L2 | 20 Oct 2026 | T5/lotuss_2026-10-20.md |
| Singha Lemon Soda 330 mL | single can / 6 cans / 24 cans | 17 / 85 / 330 | Lotus's, rows L7, L8, L9 | 20 Oct 2026 | T5/lotuss_2026-10-20.md |
| Singha Lemon Soda 330 mL | 6 cans | 172 (was 182) | 7-Eleven ALL Online, page A2 | 20 Oct 2026 | T5/7eleven_allonline_2026-10-20.md |
| Pepsi 325 mL | 6 cans | 167 (was 176, "5% off") | 7-Eleven ALL Online, https://www.allonline.7eleven.co.th/p/เป๊ปซี่-325-มล-แพ็ก-6-กระป๋อง/421682/ | 19 Oct 2026 | captures_2026-10-19/19_7eleven-pepsi-6pack.md |
| est cola 325 mL | 6 cans | 79 ("13.17 per unit") | Makro PRO (a cash-and-carry listing, not a consumer shelf price), https://www.makro.pro/th/p/916060-7606383608003 (listing says it cannot be delivered to the selected area) | 20 Oct 2026 | T4/est_retail_listings_makro_7eleven_2026-10-20.md |
| est cola 325 mL | 6 cans | 138 (was 176; a snippet the same day showed 110) | 7-Eleven ALL Online, https://www.allonline.7eleven.co.th/s/est/est-cola-2/ | 20 Oct 2026 | T4/est_retail_listings_makro_7eleven_2026-10-20.md |
| est Sugar Free (flavour not stated on the Priceza row; a separate 1 L listing is a sugar-free cola), 325 mL | 6 cans | 99 | "Sermsuk Click" seller on Lazada, via Priceza est brand page | 20 Oct 2026 | T4/est_priceza_listing_2026-10-20.md |
| est Kamikaze Lime | 24 x 325 mL cans / 12 x 360 mL bottles / 12 x 1 L bottles | 408 / 144 / 264 | third-party Lazada seller, via Priceza est brand page | 20 Oct 2026 | T4/est_priceza_listing_2026-10-20.md |

## Reading notes

- The 7-Eleven ALL Online prices run about twice those of Lotus's for the same pack: Singha Lemon Soda 6 cans is 172 at 7-Eleven online and 85 at Lotus's (ratio 2.02 in the results file). The Pepsi row is therefore not comparable with the 7UP and est rows from Lotus's and Makro. No Pepsi row from Lotus's, Makro or another cash-and-carry or hypermarket page was found, so a like-for-like Pepsi shelf price is UNVERIFIED.
- The 7UP pages show "ZERO SUGAR" in the product name at Lotus's. The proposal's earlier row "7UP NS Strawberry Lemon" (Lazada listing, THB 75 for 6) reads "NS" as no sugar without confirmation; row L6 above is the same flavour and pack at the same THB 75 and names it "ZERO SUGAR".
- The T5 note on Lotus's says the Pepsi-related promotion "Buy SUNTORY PEPSICO products worth 199 baht get 30 coins" appears on the 7UP pages.

## Second-pass notes (20 October 2026)

- The 7UP single-can price of 16 is a Lotus's Shop Online row shown by Priceza (page P3); the Lotus's page for the single can was not opened and the pre-production host is not used. The six-pack rows at 75 (flavours lemon soda and strawberry lemon) are opened Lotus's pages L5 and L6. A pineapple-peach 7UP row (single 16, six-pack 75) is on the same Priceza row only (page not opened).
- The Makro PRO est row is a cash-and-carry listing and says it cannot be delivered to the selected area; it is cited as a trade listing, not a consumer shelf price.
- Lotus's Singha Lemon Soda single can 17, six-pack 85 and the Sprite six-pack 85 are Lotus's pages (T5, rows L7, L8, L2).
