# V1 evidence 07: Makro PRO control pages (non-Yuzu Singha lemon sodas, opened)

Item: V1 (revision of 20 October 2026)
Date read: 20 October 2026
Tier: S (retailer pages, opened and read). Status SOURCED (secondary, labelled). No page gave a date.

Purpose: to test whether the Makro delivery-area notice on the Yuzu pages (file 05) is specific to Yuzu. Seven other Singha lemon soda pages were opened in the same session with the same prompt.

Method: WebFetch asking for title, price, struck-through price, per-unit price and any delivery-area or availability notice, quoted exactly. Text as returned by the tool.

| Product (page title) | URL | Price read | Original price on page | Per unit | Delivery-area notice |
|---|---|---|---|---|---|
| SINGHA Lemon Soda 330 ml x 6 | https://www.makro.pro/en/p/893947-6814746706115 | ฿78 | "฿ 82.00", "-4%" | ฿13.67 | Absent. A "Delivery" heading with no area text. |
| SINGHA Lemon Soda 330 ml x 24 | https://www.makro.pro/en/p/428706-7350275997891 | ฿325 | "฿ 330.00", "-1%" | ฿13.54 | Absent. |
| SINGHA Red Lemon Soda 330 ml x 24 | https://www.makro.pro/en/p/895147-441558077299226 | ฿325 | "฿ 330.00", "-1%" | ฿13.54 | Absent. |
| SINGHA Pink Lemon Soda 330 ml x 24 | https://www.makro.pro/en/p/929157-623536453647288 | ฿325 | "฿ 330.00", "-1%" | ฿13.54 | Absent. |
| SINGHA Pink Lemon Soda 330 ml x 6 | https://www.makro.pro/en/p/928273-283493924351755 | ฿78 | "฿ 82.00", "-4%" | ฿13.67 | Absent. |
| SINGHA Ume lemon soda 330 ml x 6 | https://www.makro.pro/en/p/922924-374686462349285 | ฿78 | "฿ 82.00", "-4%" | ฿13.67 | Absent. |
| SINGHA Ume Lemon Soda 330 ml x 24 | https://www.makro.pro/en/p/922923-175605632107181 | ฿324 | none | ฿13.50 | Present, exact: "This item is unavailable in the area you selected" |

Other notes from the same reads:
- No page showed a discontinued marker or an out-of-stock notice. A search-tool summary said the structured data of the Lemon x24 page marks it "discontinued". The opened Lemon x24 page showed no discontinued marker in the extracted text, and the page was not checked for hidden structured data. That summary claim is a lead and is not used.
- The two Yuzu pages (file 05) and the Ume x24 page carry the notice. Six pages read here do not.
- The Makro "Soda" category page (https://www.makro.pro/en/c/beverages/soda) was opened. It showed "Showing products 1-20 of 186", listed three Singha products (Soda 325 ml x 24 at ฿190, Soda 325 ml x 6 at ฿52, Lemon Soda 330 ml x 6 at ฿82) and no Yuzu in the 20 shown. The content was truncated, so the other 166 products were not seen.

## Reading

- The delivery-area notice is not Yuzu-only. It also sits on the Ume 24-pack, a flavour that 7-Eleven ALL Online lists as a 24-can case (file 10). So the notice alone cannot be read as "delisted".
- Makro pages in the range that carry no notice show a discount from a list price (82 to 78, 330 to 325). The Yuzu 6-pack shows 84 with no discount, which differs from the 78 or 82 of the other 6-packs. The Yuzu prices may be stale list prices, but the pages do not say so.
- Whether Makro delivers a Yuzu pack to any area is not shown. The pages show only that the product pages exist, with a price, and that for the area the fetch tool had, delivery was marked unavailable.
