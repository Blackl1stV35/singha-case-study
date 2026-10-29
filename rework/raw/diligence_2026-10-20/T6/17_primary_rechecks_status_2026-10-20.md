# Primary inputs for the can-cost model: status of re-reads on 20 October 2026

Task T6, fourth pass (after the second verifier round). This file records which primary inputs were re-tested today and which are used only from saved copies. No browser was used. Re-tests were WebFetch calls; the results are in file 18 items 18, 30 and 31.

| Input | Source (primary) | Re-test on 20 October 2026 | Value in the saved copy | Saved copy | Tier and status |
|---|---|---|---|---|---|
| LME aluminium cash | https://www.lme.com/en/metals/non-ferrous/lme-aluminium (trading summary) | HTTP 403 Forbidden (file 18 item 30) | Cash bid 3,013.00 and offer 3,014.00 USD per tonne, "Data valid for 16 Oct 2026" | `raw/lme_trading_summary_primary_2026-10-19.md`; line 4 says "Read in the user's Chrome, 19 October 2026" | NOT USED. Route not authorised (CLAUDE.md section 4; no named request recorded). Stated limit. The settlement price was not obtained. |
| Bank of Thailand USD rate | https://www.bot.or.th/en/statistics/exchange-rate.html | Page read; no rate table and no as-of date; links to thaifxrates.net, which is not a primary (file 18 item 18) | Average buying (sight) 33.3535, buying (bill) 33.4246, selling (transfer) 33.7455 baht per USD, as of 15 October 2026 | `raw/bot_fx_primary_2026-10-15.md` (read 19 October 2026); the saved file records no access route | P as a saved copy; NOT re-verified on 20 October 2026. Not used on slide 4. |
| Royal Gazette excise schedule | https://www.ratchakitcha.soc.go.th/DATA/PDF/2560/A/095/111.PDF | HTTP 403 Forbidden (file 18 item 31) | Item 02.02: 14% ad valorem; per litre 0 baht for up to 6 g sugar per 100 mL in every period | `raw/gazette_sugar_drink_excise_primary_2560_A095_111.md` (copy saved from a viewer tab; read from page images) | P for the saved schedule; NOT re-read on 20 October 2026. The ad valorem base was not read. Not on slide 4. |
| TBC can maker, BJC 56-1 One Report 2025 | https://bjc.listedcompany.com/misc/one-report/20260403-bjc-one-report2025-en.pdf (and the CP AXTRA copy) | Saved text in `T6/08` (read 20 October 2026) | Capacity 3,880; output 2,307; usage 59.46% (2025), million cans; total revenue THB 11,909.0 million (2025) | `T6/08_bjc_one_report_2025_tbc_capacity_customers_bigc.md` | P, SOURCED |

## Notes

- The LME and Bank of Thailand readings are the latest saved readings and are dated. Neither is used on slide 4.
- The LME trading summary returned HTTP 403 to WebFetch on 20 October 2026. It was not worked around, and no browser route was used.
- The Bank of Thailand page gives no rate table in today's extract. The 19 October read is a saved copy; its route is not recorded in the saved file.
- The Gazette schedule's later amendments, and the ad valorem base, remain stated limits.
