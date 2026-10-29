# UN Comtrade: Thailand imports 2025 of polyols and dextrins, unit values (read 20 October 2026)

- Base URL pattern: https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=764&period=2025&cmdCode=<HS code>&flowCode=M
- Date read: 20 October 2026. Access route: WebFetch (HTTP 429 on parallel calls; each repeated alone and succeeded). The tool returned a model-written extraction of the JSON rows, not the verbatim page.
- Tier: P (UN Comtrade trade statistics). Reporter 764 is the ISO numeric code for Thailand (as in the repo's earlier captures 61 and 62). The preview does not name the currency or the quantity unit; Comtrade reports CIF values in US dollars and qtyUnitCode 8 is kilograms. That convention was not confirmed on the page.
- Status: SOURCED for the rows. The unit values are PROXY for the price of the food grades (see below).

## Rows (World, partnerCode 0, and China, partnerCode 156)

| HS code (heading) | Partner | CIF value | Net weight (kg) | Estimated weight? | Unit value, per kg (DERIVED) |
|---|---|---|---|---|---|
| 290543 mannitol | World | 2,095,441.421 | 476,781 | no | 4.395 |
| 290543 mannitol | China | 1,299,035.829 | 427,232 | no | 3.041 |
| 290543 mannitol | France (251) | 297,949.194 | 24,375 | no | 12.22 |
| 290543 mannitol | Germany (276) | 233,269.068 | 4,929 | no | 47.33 |
| 290543 mannitol | Japan (392) | 257,495.476 | 19,951 | no | 12.91 |
| 290549 other polyhydric alcohols (basket that includes erythritol and xylitol) | World | 6,535,824.369 | 3,692,852.63 | yes | 1.770 |
| 290549 | China | 6,044,834.743 | 3,494,160.295 | yes | 1.730 |
| 290544 D-glucitol (sorbitol, includes syrups) | World | 18,870,735.432 | 27,317,175.591 | yes | 0.691 |
| 290544 | China | 14,155,150.981 | 20,186,799 | no | 0.701 |
| 350510 dextrins and modified starches (includes maltodextrin) | World | 30,370,017.275 | not given | | not computable |
| 350510 | China | 6,763,776.52 | 6,676,632.063 | yes | 1.013 |

Unit value = CIF value divided by net weight (our arithmetic).

## Limits

- The unit values are import averages across grades. Directly compressible spray-dried mannitol and polyol grades made for tablets are not separated from bulk powder; the premium is unknown (ASSUMPTION used in the model: 1 to 3 times the bulk unit value).
- HS 290549 is a basket; its unit value is not a price for erythritol. Isomalt has no row here (not searched; its HS code was not established).
- Exchange rate used for baht: 33.55 THB per USD, Bank of Thailand average counter rate midpoint, 15 October 2026 (raw/bot_fx_primary_2026-10-15.md, P).
