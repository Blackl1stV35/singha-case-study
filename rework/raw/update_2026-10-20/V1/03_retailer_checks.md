# V1 evidence 03: Retailer and marketplace checks

Item: V1
Date read: 20 October 2026
Method: WebFetch on each store's own URL. Each result is recorded as the tool returned it. No store search returned a listing for the Singha Yuzu can.

| Store | URL tried | Result | Yuzu listing captured |
|---|---|---|---|
| 7-Eleven ALL Online (search) | https://www.allonline.7eleven.co.th/search?text=ยูซุ%20เลมอน%20โซดา | Empty search shell. The page says there are no search results. A notice, in the fetch tool's English translation (ours to check), says that due to a technical problem this function "cannot be used yet". Query shown blank. Banner alt text (as extracted): "Special Coupon (24 Sep - 23 Oct 26)" | No |
| 7-Eleven ALL Online (home) | https://www.allonline.7eleven.co.th/ | Home page with a beverage category "เครื่องดื่มและผงชงดื่ม" and a soft drink tile "น้ำดื่ม น้ำอัดลม". The text was cut at about 100,000 characters. In the visible part, no Singha, Yuzu, ยูซุ or Lemon Soda product. Visible lemon items were unrelated brands. | No (part of page not read) |
| Lotus's Shop Online (search) | https://www.lotuss.com/th-th/search/ยูซุ%20เลมอนโซดา | Shell page. Title "ผลการค้นหา | Lotus's online". No product list. | No |
| Makro PRO (search, guessed path) | https://www.makro.pro/search?q=สิงห์ ยูซุ เลมอนโซดา | HTTP 404. The path was a guess. | No |
| Makro PRO (home) | https://www.makro.pro/ | Title "สั่งซื้อออนไลน์ สินค้าหลากหลาย ราคาพิเศษจากแม็คโคร | Makro PRO". Visible text cut off before any product list. No Singha or Yuzu name visible. | No (not read in full) |
| Big C | https://www.bigc.co.th/search?q=singha%20yuzu | HTTP 403 | No |
| Tops | https://www.tops.co.th/en/search?q=singha%20yuzu | HTTP 403 | No |
| Lazada Thailand (search) | https://www.lazada.co.th/catalog/?q=singha+yuzu+lemon+soda | Shell page. The page title (as extracted) is "ช้อป Singha Yuzu Lemon Soda ออนไลน์ในราคาที่ดีกว่า | Lazada Thailand". No listing text captured. Footer "© Lazada 2026". | No. The title is a lead only, not evidence of a listing. |
| Shopee Thailand (search) | https://shopee.co.th/search?keyword=singha%20yuzu%20lemon%20soda | Empty shell (two separator lines, no text) | No |
| Dan Murphy's (Australia) | https://www.danmurphys.com.au/product/DM_ER_2000005099_8850999018508/singha-singha-yuzu-lemon-soda-sparkling-water-330ml | HTTP 403 when opened. Only the search snippet was seen. The snippet says "Zero Sugar. Zero Calories. Zero Alcohol" and "Thailand" as country of origin. Not a Thai retailer, so not used for the Thai question. | Not a Thai listing |

## Correction added 20 October 2026 (revision after review)

This file records only the first pass, which opened store search pages and home pages. Those pages are shells and do not show product listings. The first pass never located retailer product pages, and its conclusion that no Thai store page gave a Yuzu listing was wrong. Product pages found by domain-restricted search are recorded in files 05 to 13: Makro PRO (05, 06, 07), Gourmet Market (08), Lazada (09), 7-Eleven (10), Lotus's (11), Tops and Big C (12), Singha Online (13), and the search log (14). The "Reading" below is the first-pass reading and is superseded by the record, rework/83_verify_V1_yuzu_on_sale.md.

## Reading (first pass, superseded)

- No Thai store page returned a dated listing for Singha Yuzu Lemon Soda in October 2026. (Superseded: Makro PRO product pages show Yuzu with a price, read 20 October 2026, undated.)
- Five retail routes failed for tool reasons (403, shell pages, a broken store search, a guessed path that returned 404). This is a limit of the fetch tool, not evidence that the can is absent.
- The team's own earlier pass (rework/raw/diligence_2026-10-20/T6/04_retail_listings_2026-10-20.md) also records no Yuzu listing among nine retailer pages. That is a team record, not a source for this item.
