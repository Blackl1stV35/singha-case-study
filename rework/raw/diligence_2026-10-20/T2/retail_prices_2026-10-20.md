# Retail prices for Coca-Cola system carbonated products, read 20 October 2026

Task T2. Route: WebFetch (model-written extracts of retailer product pages; not raw page text). Tier S (retailer listings; none carries a page date; branch and area pricing may differ). Per 330 mL figures are derived in rework/screen/coca_cola_system_derived.py.

## Makro PRO (cash and carry, business channel)

- https://www.makro.pro/en/p/899900-7499701616835 : "SCHWEPPES Soft Drink Lime Soda Zero Sugar 330 ml 6 cans". Unit price THB 14.00; pack THB 84 (shown as separate elements); message "This item is unavailable in the area you selected". Same figures as capture 38 of 19 October 2026.
- https://www.makro.pro/en/p/7078661193923 : "COKE Soft Drink No Sugar No Calories 330 ml x 12". Unit price THB 8.50; pack THB 102. On 19 October 2026 (capture 34) the unit price read THB 8.67 and the page showed 102 and 104. The two readings differ by one day, so the price is not fixed to a date.

## Lazada Thailand trending page (consumer channel; undated)

- https://www.lazada.co.th/trending/Sparkling-Flavoured-Drinks-Best-Price/1584270705
- Sprite Soft Drink Original 325 ml Pack 24: THB 365.00 (struck price THB 384.00, -5%). Seller not shown. Delivery-area tile text (Thai, re-opened 20 October 2026, verifier_reopens_2026-10-20.md section 2): "ส่งในกทม. ปริมณฑล,ลำพูน,เชียงใหม่และชลบุรี", that is delivery to Bangkok and its metro area, Lamphun, Chiang Mai and Chon Buri (our translation).
- Sprite Soft Drink No Sugar 325 ml Pack 24: THB 365.00 (struck price THB 384.00, -5%). Seller not shown. Delivery-area tile text (Thai, re-opened 20 October 2026, verifier_reopens_2026-10-20.md section 2): "จัดส่งเฉพาะกทม. ปริมณฑลและชลบุรี", that is delivery only to Bangkok and its metro area and Chon Buri (our translation). This listing is one of the four in the Sprite No Sugar range, but it is delivery-restricted.
- Fanta Soft Drink Orange 325 ML Pack 5+1: THB 85.00.
- Fanta Pineapple 6*325 ml: THB 85.00.
- Fanta Soft Drink Strawberry (Red) 1.5 L single: THB 32.00.
- 7Up NS Strawberry Lemon 6*325 ml: THB 75.00 (struck THB 85.00).
- No Schweppes item on the page. A previous note of a second Sprite figure of THB 354 (in proposal 11) is not on the page as read today.

## Earlier readings kept as leads (not re-read)

- Tops Online, Sprite Zero Sugar Lemon Lime 325 ml: "16 / can" in the in-app browser read of 18 October 2026 (rework/raw/browser_captures_2026-10-18.md); the page returned HTTP 403 to WebFetch on 19 October 2026 (capture 53). Branch-dependent price. Tier S, lead only.
- Sprite sugar-free 325 mL can THB 14 (1 April 2019 release); Sprite Lemon Plus 325 mL can THB 15 (29 August 2022 review). Dated figures, not current.

## Not verified

- A current price for Sprite Lemon Plus, and any 7-Eleven or Lotus's shelf price for Sprite, Fanta or Schweppes. No 7-Eleven or Lotus's product page address was known, and the session's web search allowance ran out before one was found.

## Cross-reference added 20 October 2026 (verification fix)

- Record rework/68d_lemon_soda_price_ladder.md (read 20 October 2026) holds two rows used in the T2 record, both read from retailer or aggregator pages in that task and not opened again here: Sprite No Sugar 325 mL x 24 at THB 334 (Coca-Cola Official Store on LazMall, via Priceza; row Z2; the retailer page was not opened) and a single Sprite 325 mL can at THB 16 (Lotus's Shop Online, row L1). The Lazada THB 365 for the same 24-pack read above therefore differs by seller; no single price is the market price.
- "Fanta Soft Drink Orange 325 ML Pack 5+1" at THB 85: the page does not state the can count; the T2 record reads it as 6 cans (5 plus 1 free), which is an assumption about the pack wording.
