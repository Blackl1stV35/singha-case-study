# T5 recheck: blocked pages, unreadable retailers and search leads (20 October 2026)

Access route: WebFetch and WebSearch only. No browser, login, cart, form or account was used. Nothing was bypassed. A search snippet is a lead, not evidence; a snippet is used only where the page was then opened, as stated.

## 1. Blocked pages (HTTP 403 Forbidden, 20 October 2026)
| Retailer | URL tried | Result | Consequence |
|---|---|---|---|
| Tops Online | https://www.tops.co.th/en/sprite-soft-drink-zero-sugar-lemon-lime-flavour-325ml-8851959132395 (Sprite Zero 325 mL, product page named in the submission) | HTTP 403 | Not read. Tops is covered only through a Priceza row (S). |
| Tops Online | https://www.tops.co.th/en/schweppes-soda-water-330cc-8851959132647 (Schweppes soda water 330 mL) | HTTP 403 | Not read. No Tops figure is used except the Priceza row. |
| Big C Online | https://www.bigc.co.th/search?q=sprite | HTTP 403 | No Big C figure. Big C is a stated limit. |
| Foodland | https://www.foodland.co.th (earlier pass, r25) | HTTP 403 | No Foodland figure. Foodland is a stated limit. Search in this pass found no Thai Foodland listing (below). |

## 2. Pages read but without the target listing
- Lazada trending page (Sparkling Flavoured Drinks): read; see t5_recheck_lazada_priceza_2026-10-20.md, section 1.
- 7-Eleven ALL Online search for "sprite": read; 30 of 273 cards; only the Schweppes Lime Soda Zero 6-pack matches; see t5_recheck_7eleven_allonline_2026-10-20.md, section 7.
- Makro PRO search for "sprite": HTTP 404.
- Lotus's Shop Online search for "sprite": shell page (title only), no listings.
- Priceza 7UP listing and Schweppes listing: read; see t5_recheck_lazada_priceza_2026-10-20.md, sections 4 and 5.

## 3. Search leads (not opened unless stated; used only as leads)
- "Sprite Zero 325 ml can price Big C Lotus's 7-Eleven 2026" (WebSearch, standard): no Thai retail listing for a 325 mL Sprite Zero can. Results were in other markets.
- "7UP No Sugar 325 ml can price Thailand 2026 official store" (WebSearch, standard): no Thai official-store listing. Results were in other markets, plus a used collectible seller in Phuket (not current stock).
- "สไปรท์ เลมอนพลัส 325 มล ราคา" (WebSearch, standard, Thai): no 2026 Sprite Lemon Plus shelf price. The Lazada trending page (opened) and the Thaiger and Thaipr pages (opened) came back. A snippet showed the Lazada Sprite 24-pack at THB 354 (was 384); the opened page shows THB 365.
- "เซเว่นอัพ ไม่มีน้ำตาล 325 มล กระป๋อง ราคา 7-Eleven ALL Online" (WebSearch, standard, Thai): no 7-Eleven ALL Online 7UP listing found. Results were other markets and older Thai news.
- "Shopee Thailand Sprite 325ml 24 cans Coca-Cola Official Store price" (WebSearch, standard): no Shopee Thailand listing found. The closest result was the Lazada trending page (opened).
- "Foodland Thailand Sprite 325 ml can price" (WebSearch, standard): no Foodland Thailand listing found.
- "น้ำอัดลมกลิ่นมะนาว กระป๋อง 330 มล ตราโลตัส หรือ ตรามากรแพ็คโปร ราคา" (WebSearch, standard, Thai, house brands): no Lotus's or Makro house-brand lemon or lime soda found. The results were Schweppes (brand) and the Lazada trending page.
- "Singha Lemon Soda 330 ml can price Thailand 7-Eleven single can" (WebSearch, standard): no current 7-Eleven single-can price. Leads: Thai articles in 2022 mention a 16 baht launch price for a Singha red lemon soda (undated in the snippet; not opened in this pass; the marketeer article of 16 August 2022 is already in the record as a source).
- Kaohoon International search result on Singha Sparkling Water: opened; see t5_recheck_brands_press_2026-10-20.md, section 5.

## 4. Coverage limits closed in this pass
- Big C, Tops and Foodland: blocked (403) or not readable. Stated limit. No figure from these three is in the ladder except Tops rows reached only through the Priceza aggregator (S).
- Shopee Thailand and the Lazada official stores: the Lazada and Priceza pages were read; a Shopee-specific page was not reached.
- House brands at Lotus's and Makro: no listing found in search or on the Lotus's and Makro pages read. Stated limit.
- Single-can 7-Eleven shelf price for the Singha Lemon Soda and for Sprite: not found online. Stated limit.

## Correction note (20 October 2026, second pass)
Section 1 lists the Tops Sprite Zero and Schweppes soda water product pages as HTTP 403 on 20 October 2026. That is still the result for those pages (re-tried in t5_recheck3_live_checks_2026-10-20.md, section 1). The built-in browser read the same two Tops pages on 18 October 2026 and printed prices marked Out Of Stock (rework/raw/browser_captures_2026-10-18.md; copied in t5_recheck3_live_checks_2026-10-20.md, section 3).
