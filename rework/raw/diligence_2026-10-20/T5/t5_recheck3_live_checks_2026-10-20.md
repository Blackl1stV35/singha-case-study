# T5 recheck 3: live re-reads for the second verifier (read 20 October 2026)

Access route: WebFetch, 20 October 2026. Each text is a small-model extract quoting labels as shown. It is not a verbatim copy. Tier as stated per item. No login, cart or form was used.

## 1. Tops Online: Sprite Zero Sugar 325 mL product page (SKU 8851959132395)
- URL: https://www.tops.co.th/en/sprite-soft-drink-zero-sugar-lemon-lime-flavour-325ml-8851959132395
- Result on 20 October 2026: HTTP 403 Forbidden. Not read. The 18 October built-in browser capture of this page is in section 3 below.

## 2. Makro PRO 330 mL Sprite 12-pack (SKU 830198)
- URL: https://www.makro.pro/en/p/830198-7078660866243
- Result on 20 October 2026: read. Extract:
  - "฿ 11.42 per unit" (per-unit price).
  - "฿ 135" under the label "Buy 3+ units". This is the only bulk-tier label on the page.
  - "฿ 137.00" with no label, shown next to the discount badge. The page does not say it is the original price.
  - "-1%" badge beside the 135 and 137 figures.
  - The "Delivery" label has no price attached.
  - No container word (can or bottle). The page uses "unit(s)" and "330 ml" in the title.
- Reading: 135 is the buy-more tier and is not the pack price. 137 is the pack price, because 137 divided by 12 gives the printed per-unit 11.42, and 135 divided by 12 would give 11.25. The container is still not stated on the page.
- Tier: S (retailer listing page read as an extract).

## 3. Tops Online: built-in browser capture of 18 October 2026
- Copied from rework/raw/browser_captures_2026-10-18.md (Tops items 1 and 2). Captured 18 October 2026 with the built-in browser (get_page_text and one screenshot). Prices are as printed at capture time. The 20 October product pages returned HTTP 403 (section 1 above and t5_recheck_blocked_and_search_2026-10-20.md, section 1).
- Sprite Soft Drink Zero Sugar Lemon Lime Flavour 325 ml, SKU 8851959132395. URL: https://www.tops.co.th/en/sprite-soft-drink-zero-sugar-lemon-lime-flavour-325ml-8851959132395. Printed: "16 / can" and "Out Of Stock". Branch-dependent pricing noted on the page.
- Schweppes Soda Water 330 cc, SKU 8851959132647. URL: https://www.tops.co.th/en/schweppes-soda-water-330cc-8851959132647. Printed: "17 / can" and "Out Of Stock".
- Tier: S (page opened in a browser). Both are out of stock, so both are excluded leads and sit in no ladder.

## 4. Coca-Cola Thailand: Sprite products page
- URL: https://www.coca-cola.com/th/th/brands/sprite/products
- Result on 20 October 2026 (this pass): readable. The page lists four Sprite products. No size appears in the visible text or in the alt text. The sizes come only from image file names.
  1. Heading "สไปรท์"; alt text "สไปรท์ในกระป๋อง" (Sprite in a can); 325 ml (image file name).
  2. Heading "สไปรท์"; alt text "สไปรท์ในขวดพลาสติก" (Sprite in a plastic bottle); 330 ml (image file name).
  3. Heading "สไปรท์ สูตรไม่มีน้ำตาล"; alt text "สไปรท์ซีโร่ชูการ์ในกระป๋อง" (Sprite Zero Sugar in a can); 325 ml (image file name).
  4. Heading "สไปรท์ สูตรไม่มีน้ำตาล"; alt text "สไปรท์ซีโร่ชูการ์ในขวดพลาสติก" (Sprite Zero Sugar in a plastic bottle); 330 ml (image file name).
- No-sugar wording: heading "สไปรท์ สูตรไม่มีน้ำตาล" and description "แต่ปราศจากน้ำตาล" (free of sugar).
- No price on the page.
- Tier: S (brand owner's page read as an extract, not in full).
- The later attempts on 20 October that returned HTTP 403 (t5_recheck2_brand_sites_2026-10-20.md, section 1) are superseded by this readable read. The first-pass extract (t5_recheck_brands_press_2026-10-20.md, section 1) gives the same four items.

## 5. Kaohoon International: Singha Sparkling Water Lime article
- URL: https://www.kaohooninternational.com/?p=579263
- Result on 20 October 2026: read. Posted "17/03/2026".
- The 330 ml can "priced at 15 Baht" is attributed to the Chief Marketing Officer of Boon Rawd Trading Co., Ltd. (the officer's name is printed in the article and is omitted here; it is not needed for the ladder).
- The article does not mention a company announcement or a press release. It gives no date for any release. It says the product is "now available" at all 7-Eleven branches nationwide.
- Tier: S (trade press quoting a named officer; read as an extract). The 13 March 2026 release cited in the submission was not opened.
