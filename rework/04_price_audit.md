# Desk price audit: non-alcoholic sparkling and herbal drinks, and beer (Thailand)

Date: 18 October 2026. Workflow wiawiyd7e, one agent per channel. Raw result with every row, URL, quote and capture date: [raw/wiawiyd7e_price_audit.json](raw/wiawiyd7e_price_audit.json).

Status: desk data only. Prices are online listings, not shelf prices. No physical or consumer test has run.

## Bottom line for finalist C

- **The 50 to 70 THB test point for a 250 ml can is not supported by any mass-market price.** It equals 200 to 280 THB per litre. The only prices at that level are imported flavoured sparkling water (Perrier, 198 THB per litre for a 30-can pack and 248 for a 10-can pack) and one marketplace seller's non-alcoholic beer at about 200. Every mass-market non-alcoholic sparkling drink read is below 90 THB per litre, and Thai herbal drinks run from 26 to 133.
- **Beer is cheaper per litre than the test point.** The 320 ml beer cans read at 96 to 139 THB per litre, so a 250 ml beer-equivalent is about 24 to 35 THB.
- **Proposed price ladder (for team agreement):** 15, 25 and 35 THB per 250 ml can. That is 60, 100 and 140 THB per litre. 60 sits within the zero-sugar and herbal band. 100 matches the cheaper beers. 140 is near non-alcoholic beer at Makro.
- **Viability is the open question.** No unit cost exists for this can. The 15 THB point may sit below cost. A cost quote is needed before the team commits to the test.

## Channels and what each produced

| Channel | Rows read | Status |
|---|---|---|
| 7-Eleven, ALL Online (allonline.7eleven.co.th) | 13 | Online listing prices, not shelf. Several promotions end 18 October 2026. No beer: the on-site search returned a technical-problem notice |
| Makro (makro.pro) | 26 | Online listing prices. Four beer rows are visible but restricted to licensed business buyers. Several rows are marked unavailable in the selected area |
| Tops (tops.co.th) | 0 from the fetch tool; 4 from the browser | All 14 pages returned HTTP 403 to the fetch tool. Four pages read in the built-in browser on 18 October 2026, all marked out of stock at capture |
| Lazada (product pages only) | 3 from the fetch tool; 5 more from the browser | About 15 product pages returned HTTP 404 to the fetch tool, and several showed no price text. In the browser, a reCAPTCHA appeared on one page; after the user cleared it, five more product prices were read on 18 October 2026 |
| Shopee (product pages and search) | 0 from the fetch tool; 3 from the browser | Fetch returned empty content. In the browser the first pass hit a traffic verification page; after the user cleared it, three listings were read on 18 October 2026 |

## Prices, per litre (pack price divided by total volume)

### Zero-sugar and plain sparkling (no-sugar or soda water)

| Product | Channel | Pack | THB (pack) | THB per can | THB per litre | Availability note |
|---|---|---|---|---|---|---|
| Sprite No Sugar 330 ml | Makro | 12 x 330 | 66 | 5.50 | 16.7 | Marked unavailable in area |
| Coke No Sugar No Calories 330 ml | Makro | 12 x 330 | 102 | 8.50 | 25.8 | |
| Schweppes Manao Soda Zero 330 ml | Makro | 6 x 330 | 81 | 13.50 | 40.9 | |
| Coke Zero Sugar 0% 325 ml | Makro | 6 x 325 | 81 | 13.50 | 41.5 | Marked unavailable in area |
| Coke Zero Vanilla 325 ml | Makro | 6 x 325 | 78 | 13.00 | 40.0 | Marked unavailable in area |
| Schweppes Soda Water 330 ml | Makro | 24 x 330 | 336 | 14.00 | 42.4 | Headline price used; page per-unit figure differs |
| Schweppes Lime Soda Zero 330 ml | Makro | 6 x 330 | 84 | 14.00 | 42.4 | Marked unavailable in area |
| San Pellegrino Zero 330 ml | Makro | 3 x 330 | 76 | 25.33 | 76.8 | Marked unavailable in area |
| Schweppes lemon soda zero 330 ml | 7-Eleven | 6 x 330 | 170 | 28.33 | 85.9 | Promotion ends 18 October 2026 |
| Pepsi sugar-free 325 ml | 7-Eleven | 6 x 325 | 167 | 27.83 | 85.6 | Promotion ends 18 October 2026 |
| Perrier sparkling mineral water 330 ml | Makro | 4 x 330 | 254 | 63.50 | 192.4 | Plain sparkling water, premium |

Sugar status of Singha soda (7-Eleven, 24 x 325 ml at 195 THB, 25.0 per litre), Nestle soda plus lemon honey and the Fanta and Big Cola lines was not established, so they are left out of this group.

### Thai herbal non-alcoholic drinks

| Product | Channel | Pack | THB (pack) | THB per can | THB per litre | Availability note |
|---|---|---|---|---|---|---|
| YENYEN Chrysanthemum and Honey 315 ml | Makro | 24 x 315 | 195 | 8.13 | 25.8 | |
| YENYEN Herbal Drink Jub Liang 315 ml | Makro | 24 x 315 | 195 | 8.13 | 25.8 | |
| YENYEN Gekhuay 315 ml | Makro | 6 x 315 | 52 | 8.67 | 27.5 | |
| YENYEN Cool Herb Tea 400 ml | Makro | 6 x 400 | 70 | 11.67 | 29.2 | Headline price used |
| IF Chinese Herbal Drink 350 ml | Makro | 6 x 350 | 75 | 12.50 | 35.7 | Marked unavailable in area |
| Payanak Promt 150 ml | 7-Eleven | 6 x 150 | 80 | 13.33 | 88.9 | Listed under energy drinks on 7-Eleven |
| Phraya Nak herbal drink 150 ml | 7-Eleven | 48 x 150 | 660 | 13.75 | 91.7 | |

### Non-alcoholic beer (0.0)

| Product | Channel | Pack | THB (pack) | THB per can | THB per litre | Availability note |
|---|---|---|---|---|---|---|
| Heineken 0.0 330 ml | Makro | 24 x 330 | 970 | 40.42 | 122.5 | |
| Heineken 0.0 330 ml | Makro | 6 x 330 | 255 | 42.50 | 128.8 | |
| hite ZERO 350 ml | Makro | 6 x 350 | 354 | 59.00 | 168.6 | Marked unavailable in area |
| Heineken 0.0 330 ml | Lazada (seller) | 6 x 330 | 395 | 65.83 | 199.5 | Seller price; original price 450 |

### Beer, 320 ml cans (Makro)

These four rows are visible, but Makro restricts them to business buyers with a verified alcohol licence. They show what the market charges, not what an ordinary shopper pays.

| Product | Pack | THB (pack) | THB per can | THB per litre |
|---|---|---|---|---|
| Chang Classic 320 ml | 28 x 320 | 860 | 30.71 | 96.0 |
| Chang Classic 320 ml | 24 x 320 | 760 | 31.67 | 99.0 |
| Leo 320 ml | 24 x 320 | 762 | 31.75 | 99.2 |
| Leo 320 ml | 6 x 320 | 193 | 32.17 | 100.5 |
| Singha 320 ml | 24 x 320 | 819 | 34.12 | 106.6 |
| Singha 320 ml | 6 x 320 | 214 | 35.67 | 111.5 |
| Heineken Sleek 320 ml | 6 x 320 | 266 | 44.33 | 138.5 |

No Lazada or Shopee beer rows were read. No 7-Eleven beer was read.

## Comparison with the C test point

| Reference | THB per litre | Equivalent for a 250 ml can |
|---|---|---|
| C's old test point, 50 to 70 THB per 250 ml | 200 to 280 | 50 to 70 THB |
| Zero-sugar and plain sparkling, Makro | 17 to 42 | 4 to 11 THB |
| Zero-sugar and plain sparkling, mass market (Makro, 7-Eleven, Tops, Shopee, Lazada) | 26 to 86 | 7 to 22 THB |
| Imported flavoured sparkling water, Perrier (Lazada) | 198 to 248 | 50 to 62 THB |
| Thai herbal drinks | 26 to 92 | 7 to 23 THB |
| Non-alcoholic beer, Makro | 123 to 129 | 31 to 32 THB |
| Beer, 320 ml cans, Makro | 96 to 139 | 24 to 35 THB |

## Proposed price ladder for the test (for team agreement)

- **15 THB per 250 ml can (60 THB per litre):** inside the herbal and zero-sugar band, at the lower end of the 7-Eleven zero-sugar prices.
- **25 THB per 250 ml can (100 THB per litre):** matches the cheaper beers per litre.
- **35 THB per 250 ml can (140 THB per litre):** near non-alcoholic beer at Makro and above the cheaper beers.

These are test points, not a recommended shelf price. They say nothing about cost.

## Browser rework (authorised by the user, 18 October 2026)

The user authorised the built-in browser for this step. Captures are in [raw/browser_captures_2026-10-18.md](raw/browser_captures_2026-10-18.md). Nothing was logged into, added to a cart, or submitted.

| Product | Channel | Pack | THB (printed) | THB per can | THB per litre | Status at capture |
|---|---|---|---|---|---|---|
| Sprite Zero Sugar 325 ml, single can | Tops | 1 x 325 | 16 | 16.0 | 49.2 | Out of stock |
| Schweppes Soda Water 330 ml, single can | Tops | 1 x 330 | 17 | 17.0 | 51.5 | Out of stock |
| Heineken 0.0 330 ml, pack of 6 | Tops | 6 x 330 | 267 | 44.5 | 134.8 | Out of stock; "available for business clients only" |
| Chamm Roselle Herbal Drink 300 ml, single bottle | Tops | 1 x 300 | 40 | 40.0 | 133.3 | Out of stock; listed as 100% juice, sugar not stated |
| Coca-Cola No Sugar 325 ml, single can | Tops | 1 x 325 | 16 | 16.0 | 49.2 | No out-of-stock label; add-to-cart shown; branch-dependent |
| Perrier Strawberry 250 ml, single can | Tops | 1 x 250 | 42 | 42.0 | 168.0 | Out of stock |
| San Pellegrino Sparkling Natural Water 330 ml, single can | Tops | 1 x 330 | 50 | 50.0 | 151.5 | No out-of-stock label; "Buy 3 Pay 2" promotion running to 27 October 2026 |
| Heineken 0.0 330 ml, pack of 24 | Tops | 24 x 330 | 1,008 | 42.0 | 127.3 | Out of stock; business clients only |
| Singha Beer 320 ml, single can | Tops | 1 x 320 | 37 | 37.0 | 115.6 | Out of stock; business clients only |
| Chang Beer 320 ml, single can | Tops | 1 x 320 | 33 | 33.0 | 103.1 | Out of stock; business clients only |
| Leo Beer 320 ml, single can | Tops | 1 x 320 | 35 | 35.0 | 109.4 | Out of stock; business clients only |
| Heineken Lager 320 ml, pack of 6 | Tops | 6 x 320 | 266 | 44.3 | 138.5 | Out of stock; business clients only |
| Asahi 330 ml, pack of 6 | Tops | 6 x 330 | 273 | 45.5 | 137.9 | Out of stock; business clients only |

What this adds:
- **Single-can prices at Tops for zero-sugar and plain sparkling are 16 to 17 THB,** about 49 to 52 THB per litre. That is the nearest thing to a shelf price in the audit. Converted to a 250 ml can, it is about 12 to 13 THB, just below the lowest proposed test point of 15 THB. Treat it as one anchor: the Sprite Zero and Schweppes cans were out of stock, and the Coca-Cola No Sugar can was not marked out of stock.
- **The roselle drink at 40 THB per 300 ml (133 THB per litre)** is the highest-priced Thai botanical drink found. It is still below the 200 THB per litre test point, and its sugar status is unknown.
- **Shopee and Lazada were blocked, then read.** Shopee redirected to a traffic verification page and Lazada showed a reCAPTCHA. The user cleared both checks, and the reads below were made after that.

## Shopee and Lazada reads after the checks were cleared (18 October 2026)

Captures are in [raw/browser_captures_2026-10-18.md](raw/browser_captures_2026-10-18.md). Lazada prices were read from the page's price elements, and the Schweppes and Coca-Cola prices were also confirmed on screenshot. Variant selection was used only to read other variants' prices. Nothing was added to a cart.

| Product | Channel and seller | Pack | THB (printed) | THB per can | THB per litre | Notes |
|---|---|---|---|---|---|---|
| Coca-Cola 325 ml, 6-pack (not zero, pack image says less sugar) | Shopee, product listing | 6 x 325 | 79 | 13.2 | 40.5 | "Unserviceable Area" for shipping to the browser's location; sugar status unclear |
| Coke Zero 325 ml, 24-can | Shopee, product listing | 24 x 325 | 409 | 17.0 | 52.4 | Seller marked "currently on vacation"; free shipping 20 to 24 October; 40 sold |
| Coke Zero Sugar 325 ml, 24-pack | Shopee, search card (Samut Prakan seller) | 24 x 325 | 365 (struck 384, -5%) | 15.2 | 46.8 | Read from the search results card, not the product page; 5,000+ sold |
| Schweppes Soda Water 330 ml, 6-pack | Lazada, Premium High Quality | 6 x 330 | 126 | 21.0 | 63.6 | Confirmed on screenshot |
| Coca-Cola Zero 325 ml, 6-pack (Zero variant selected) | Lazada, Coca-Cola | 6 x 325 | 119 | 19.8 | 61.0 | Original variant on the same page also reads 119; confirmed on screenshot for Original |
| Heineken 0.0 330 ml, 24-can | Lazada | 24 x 330 | 1,369 (struck 2,740, -50%) | 57.0 | 172.8 | Read from page elements, not screenshot |
| Maison Perrier flavoured sparkling 250 ml, 10-can (Lemon) | Lazada | 10 x 250 | 620 | 62.0 | 248.0 | Read from page elements; screenshot showed this variant selected |
| Maison Perrier flavoured sparkling 250 ml, 30-can (Lemon) | Lazada | 30 x 250 | 1,488 (struck 1,860, -20%) | 49.6 | 198.4 | Read from page elements after selecting the 30-can variant |

What this adds:
- **Zero-sugar cola is 26 to 61 THB per litre across the channels read.** Makro's 12-can pack is 26, Shopee is 47 to 52, Tops single cans are 49, and the Lazada 6-pack is 61.
- **Imported flavoured sparkling water is the only thing that reaches 200 THB per litre.** The 30-can Perrier pack is 198 THB per litre. The 10-can pack is 248. So the 50 to 70 THB test point for a 250 ml can matches imported flavoured sparkling water, not the mass-market drinks that price-led switchers would compare against.
- **Shopee's Coca-Cola 6-pack at 79 THB** (40.5 THB per litre) is one of three Shopee listings read. It cannot be shipped to the browser's location, so it may not be buyable by the target.

## Caveats

- **Online listings, not shelf prices.** Per-can shelf prices were not captured. Several 7-Eleven promotions end 18 October 2026, so prices may change.
- **Tops and Shopee rows come from the browser.** The fetch tool was blocked on Tops and returned empty pages on Shopee. Browser reads were made in the built-in browser, not on the user's own tabs, and the Shopee listings came from search cards and product pages.
- **Restricted and unavailable rows.** Makro beer is for licensed business buyers only. Several Makro rows are marked unavailable in the buyer's area.
- **Sugar status.** Not established for Singha soda, Nestle soda plus lemon honey, Fanta and Big Cola, so they are not used as zero-sugar comparators.
- **Lazada.** One marketplace seller price for a 0.0 beer, not a retailer price.
- **Caching.** WebFetch caches for 15 minutes, so some self-checks may have returned a cached copy.
- **Not covered:** unit cost, retailer margin, listing fees, and any premium that price-led switchers would pay.

## Gaps to close before the test

- A unit-cost quote for a 250 ml can from a co-packer (decides whether the 15 THB point is viable).
- Dated shelf-price captures at 7-Eleven and Makro stores, in person, for single cans.
- Single-can shelf prices at 7-Eleven and Makro stores, since the audit only reached online listings.
- Whether the 79 THB Shopee Coca-Cola 6-pack can be shipped to the target, and whether the Shopee Coke Zero 24-pack seller is active.
