# Primary-source attempts for the can cost model (19 October 2026)

Purpose: close the largest gaps in `rework/61` by reading primary sources, as `SOURCING_POLICY.md` requires. Each attempt is recorded, including the ones that failed. Nothing here is a verified value unless its row says so.

| Input | Primary source tried | Result | Tier now | Value used |
|---|---|---|---|---|
| LME aluminium cash settlement | lme.com aluminium page (fetched) | HTTP 403 Forbidden. No price read | none (blocked) | not used; `rework/61` still uses a news-report cash bid (secondary) |
| USD/THB reference rate | Bank of Thailand exchange-rate page (fetched) | Page shows no USD rate and no date; it links to a third-party site (thaifxrates.net) | none (no primary rate read) | not used; `rework/61` still uses the XE mid-market rate (secondary) |
| Thai excise tax on sugar-sweetened drinks | Excise Department landing page (fetched) | Landing page only; no rate table | none (not read) | not used |
| Thai excise tax on sugar-sweetened drinks | search for the Excise Department rate schedule (secondary results only) | News reports give a stepped schedule by grams of sugar per 100 ml. The reports conflict on the current schedule, and one news report is dated 2019 to 2021 | S (news), unverified | not used in the model; the excise line stays excluded |
| Thai Beverage Can capacity | tbcan.com (domain does not resolve) | DNS error | none | not used |
| Thai Beverage Can capacity | search for its annual report (secondary results only) | Only a 2012 report, cited in news, gives capacity: about 1.8 billion cans a year, rising to 2.2 billion. No current figure found | S (news, 2012), dated | not used in the model; the Crown line figure stays unverified |

## Next primary sources to try

- **Berli Jucker (BJC) 56-1 One Report, 2025.** BJC holds Thai Beverage Can and is listed on SET, so its filing should state TBC's capacity and volume. Not yet fetched.
- **Excise Department notifications (กรมสรรพสามิต).** The Royal Gazette notice for the sugar-drink rate, with its date. Not yet found.
- **LME settlement.** Retry through a source other than the blocked page, and record the access route. Not yet found.
- **Bank of Thailand reference rate.** The BOT statistics table, if it can be reached from a different route. Not yet found.

## Effect on the model

No input in `rework/61` changes on the strength of this pass. The gaps stay as stated limits. The sugar-tax excise line and the can-capacity figure are still missing.

## Outcomes after the Claude in Chrome pass (19 October 2026)

- **LME (primary): read.** Official cash bid 3013.00, offer 3014.00 US$/t, data valid 16 Oct 2026. Saved to `lme_trading_summary_primary_2026-10-19.md`.
- **Bank of Thailand (primary): read.** USD buying sight 33.3535, selling transfer 33.7455, as of 15 Oct 2026. Saved to `bot_fx_primary_2026-10-15.md`.
- **BJC 56-1 One Report 2025 (primary): read.** TBC has 4 can lines, plus a hybrid line added in 2025; the 2022 expansion is stated as about 10% of current capacity. Saved to `bjc_one_report_2025_tbc_excerpt.md`.
- **Royal Gazette, sugar-drink tax (primary): blocked.** The ratchakitcha PDF is behind a bot-verification page. Not bypassed. The user opened a separate tab to resolve it. Not read yet.
