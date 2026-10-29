# 68c cross-reference rows: sugar-free lemon-lime cans, Singha Lemon Soda listings and Schweppes lime soda (round 3)

- Date read: 20 October 2026. Tier: S (retailer and aggregator listings; not shelf prices and not a company price list).
- Purpose: saved text behind the figures in record 68c, sections 0, 4.3, 10 and 14. The rows were first read in the T2 and T5 tasks; each row below names the saved page it was typed from, so the figures can be traced without re-reading those tasks.
- Per 330 mL figures are DERIVED by `rework/screen/t4_competitor_margins.py` (price divided by the pack count, multiplied by 330 and divided by the unit size in mL). Results: `rework/screen/t4_competitor_margins_results.json`, key `lemon_lime_and_singha_cross_reference_2026`.

## Rows

| Id | Product and seller (as printed or as the page names it) | Pack | Shown price, THB | Per pack unit, THB | Per 330 mL, THB | URL (read 20 October 2026) | Saved page |
|---|---|---|---|---|---|---|---|
| SF01 | Sprite Soft Drink No Sugar 325 ml Pack 24, Coca-Cola Official Store (LazMall), Priceza row 9 | 325 mL x 24 | 334 (struck 384) | 13.92 | 14.13 | https://www.priceza.com/b/groceries/น้ำอัดลม/sprite | T2/priceza_sprite_2026-10-20.md |
| SF02 | Sprite Soft Drink No Sugar 325 ml Pack 24, Lazada listing (seller not stated; trending page) | 325 mL x 24 | 365 (struck 384) | 15.21 | 15.44 | https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705 | T2/retail_prices_2026-10-20.md |
| SF03 | Sprite No Sugar 325 mL x 24, Fresh Mart, Priceza row 18 | 325 mL x 24 | 414 (struck 828) | 17.25 | 17.52 | https://www.priceza.com/b/groceries/น้ำอัดลม/sprite | T2/priceza_sprite_2026-10-20.md |
| SF04 | Sprite No Sugar 325 mL x 24, CR7 ManU, Priceza row 10 | 325 mL x 24 | 456 | 19.00 | 19.29 | https://www.priceza.com/b/groceries/น้ำอัดลม/sprite | T2/priceza_sprite_2026-10-20.md |
| SF05 | 7UP No Sugar lemon soda 325 mL x 24, Suntory PepsiCo official store, LazMall, Priceza row 17 | 325 mL x 24 | 293 (struck 384) | 12.21 | 12.40 | https://www.priceza.com/s/ราคา/เซเว่นอัพ | T5/r23_priceza_7up_listing.md |
| SF06 | 7UP No Sugar lemon soda 325 mL x 12, same store, Priceza row 20 | 325 mL x 12 | 161 (struck 192) | 13.42 | 13.62 | https://www.priceza.com/s/ราคา/เซเว่นอัพ | T5/r23_priceza_7up_listing.md |
| SF07 | 7UP Zero Sugar Lemon Soda 325 mL, pack of 6, Lotus's Shop Online (list 80; "ZERO SUGAR" in the product name) | 325 mL x 6 | 75 | 12.50 | 12.69 | https://www.lotuss.com/en/product/171266560 | T5/r09_lotuss_7up_zero_325_6can.md |
| SF08 | 7UP No Sugar lemon soda 325 mL x 6, same LazMall store, Priceza row 21 | 325 mL x 6 | 96 | 16.00 | 16.25 | https://www.priceza.com/s/ราคา/เซเว่นอัพ | T5/r23_priceza_7up_listing.md |
| SG01 | SINGHA LEMON SODA CAN 330ML, Lotus's Shop Online (proposer's product; retailer price; "/Each") | 330 mL x 1 | 17.00 | 17.00 | 17.00 | https://shopping.lotuss.com/en/product/singha-lemon-soda-zero-sugar-lemon-soda-330ml-50986847 | T2/lotus_singha_lemon_soda_can_2026-10-20.md; T5/r10_lotuss_singha_lemon_single_can.md |
| SG02 | SINGHA LEMON SODA CAN 330ML.X6, Lotus's Shop Online (list 85; member price 81 with Club Card) | 330 mL x 6 | 85.00 | 14.17 | 14.17 | https://www.lotuss.com/en/product/singha-lemon-soda-can-330ml-6-51109221 | T5/r06_lotuss_singha_lemon_6can.md |
| SG03 | SINGHA LEMON SODA CAN 330ML. PACK 24, Lotus's Shop Online ("/Each" label; the pack reading is DERIVED, not a page statement) | 330 mL x 24 | 330.00 | 13.75 | 13.75 | https://www.lotuss.com/en/product/169912032 | T5/r05_lotuss_singha_lemon_24can.md |
| SW01 | Schweppes lime soda no sugar 330 mL x 12, Coca-Cola Official Store (LazMall), Priceza row 15 | 330 mL x 12 | 196 | 16.33 | 16.33 | https://www.priceza.com/s/ราคา/ชเวปส์มะนาวโซดา | T5/r24_priceza_schweppes_listing.md |
| SW02 | SCHWEPPES Soft Drink Lime Soda Zero Sugar 330 ml x 6, Makro PRO. The page says "This item is unavailable in the area you selected"; excluded from every range | 330 mL x 6 | 84 | 14.00 | 14.00 | https://www.makro.pro/en/p/899900-7499701616835 | T5/r33_makro_schweppes_lime_zero_unavailable.md |
| SL01 | Sprite Lemon Plus 325 mL single can, price stated in a 2022 review (dated; not a 2026 price; excluded from every 2026 band) | 325 mL x 1 | 15 | 15.00 | 15.23 | https://thethaiger.com/th/news/641196/ (29 August 2022) | T5/r27_thaiger_sprite_lemon_plus_2022.md |

## Bands (per 330 mL, script output)

- Sprite No Sugar, 24-pack, four 2026 listings (SF01 to SF04): 14.13 to 19.29, median 16.48.
- 7UP No Sugar lemon soda, four 2026 listings (SF05 to SF08): 12.40 to 16.25, median 13.15 (the script rounds the midpoint of 12.69 and 13.62 to 13.15).
- All eight sugar-free lemon-lime cans above (SF01 to SF08): 12.40 to 19.29, median 14.79.
- Singha Lemon Soda, three Lotus's rows (SG01 to SG03): 13.75 to 17.00, median 14.17.

## Notes

- The Singha pack readings and the Schweppes Lime Soda Zero Sugar Makro row are as the pages show. The Makro page says the item is unavailable in the area selected, so it is excluded from the bands.
- No date is printed on the Lotus's Singha or 7UP pages; the read date is 20 October 2026 for each.
- Record 68a (Coca-Cola system) and record 68b (Pepsi system) hold the same rows with their own discussion; this file is the saved text behind record 68c.
