# Exchange rates used, and pages that could not be read (T5b), 20 October 2026

## 1. Exchange rates
- Bank of Thailand, average counter rates for USD as of 15 October 2026: buying sight 33.3535; selling transfer 33.7455; mid 33.5495 (our arithmetic). Source file already in the repo: rework/raw/bot_fx_primary_2026-10-15.md (https://www.bot.or.th/en/statistics/exchange-rate.html, tier P). The Bank of Thailand page did not return a rate table to WebFetch today ("The page ... contains only navigation menus"), so the file of 19 October 2026 is the source.
- European Central Bank euro reference rates, reference date 19 October 2026 (units per 1 EUR): USD 1.1225; JPY 177.63; GBP 0.84205; CHF 0.9261; AUD 1.6068; SGD 1.4357; CAD 1.5798; CNY 7.4991. URL: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html . Tier P (central bank).
- Cross rates to the baht are our arithmetic: THB per EUR = 33.5495 x 1.1225 = 37.6593; THB per other currency = THB per EUR divided by the ECB rate. The two dates differ by four days; the cross rates are therefore indicative (PROXY for a same-day rate).

## 2. Pages that returned an error or no usable text (not used for any figure)
- HTTP 403: brutkasten.com (waterdrop revenue target article); goxip.co.th (waterdrop in Thailand); coop.ch and swissfood.store (Ricola cubes price); waterdrop.com.au; desertcart.co.th (Nuun); th.iherb.com; shoprite.com; berocca.co.th (product and where to buy); watsons.co.th; bayer.com (all pages tried); hydralyte.com.au; coca-cola.com/jp (release page).
- HTTP 401: nestlehealthscience.com press release (Nuun acquisition).
- HTTP 404 or timeout: waterdrop.com Lemon Lime product page (404); sodastream.com CO2 pages (404); tga.gov.au ARTG entry (timeout); Amazon.co.jp 1,2,CUBE page (HTTP 500).
- Unreadable PDF text layer: Thai FDA Notification 293 compilation and announcement 029mso179.pdf (font encoding without a Unicode map).

## 3. Search budget
- The session web-search allowance ended during this task (the tool returned: "this turn's web search budget is used up (limit: 200 WebSearch calls per turn, shared by every agent in it)"). Items that needed a further search are recorded as stated limits in rework/68e_dissolvable_drink_analogues.md. No search engine was reached by another route.
