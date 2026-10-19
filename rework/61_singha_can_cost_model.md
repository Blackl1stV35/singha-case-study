# Singha 330 ml can: cost per unit and production scenarios (desk model, 19 October 2026)

> Audit, 19 October 2026: the corrections at the end of this record supersede the figures they name.

Status: a desk estimate. No Singha or Boon Rawd can cost was found, and no quote was requested (per the user). The model runs on public figures, mostly secondary, and labelled assumptions. Treat it as a range for a 330 ml can at a Thai-style plant, not as Singha's cost. Script: `screen/can_cost_model.py`. Results: `screen/can_cost_model_results.json`. Chart: `charts/can_cost_per_unit.png`.

Sourcing follows `SOURCING_POLICY.md`. Every input is tiered: **P** primary, **S** secondary. Most inputs are S; no primary (LME settlement, Bank of Thailand rate, Excise Department, a company filing) was read.

## 1. Answer

- **Variable cost per 330 ml can: THB 3.7 to 6.1 (middle THB 4.9)**, covering sheet metal, non-metal conversion (labour, energy, coating and printing in one proxy), filling consumables, seaming, CO2 and the sugar-and-flavour liquid.
- **Fixed cost adds THB 0.1 to 0.6 per can** in the scenarios, depending on volume and fixed cost. No fixed-cost figure is sourced.
- **Desk total: about THB 4 to 6.5 per can,** before the items listed in section 5 (premium, excise, end and tab, packaging, freight). Those would move it up.
- **Metal is 30 to 39% of variable cost.** The metal estimate is THB 1.44 to 1.86 per can, not the THB 1.00 in `rework/53`; see section 6.
- **Cans per year:** about 1.0 billion at 58 to 63% of a 1,000 million litre nameplate with a 55% canned share, and about 1.7 billion at full nameplate. The volume comes from proxies and the group nameplate scope is unclear.

## 2. Inputs

| Input | Value | Tier | Status | Source |
|---|---|---|---|---|
| FX, THB per USD | 33.32 to 33.44 | S | SOURCED | XE mid-market, 18 Oct 2026 (low is a 16 Sep reading). Bank of Thailand not read |
| LME aluminium cash | USD 2,998.5 to 3,008.5 per t | S | SOURCED | News report of the LME cash bid (alcircle, 16 Oct 2026); high is a Trading Economics CFD. lme.com not read |
| Sheet aluminium per can | 14.4 to 18.5 g | S/P | ASSUMPTION | Derived: can mass 13 to 15 g (supplier page, S) divided by (1 minus scrap 10 to 19%, a patent statement and an unparsed LCA, P but unverified) |
| Non-metal conversion | USD 0.04 to 0.08 per can | S | PROXY | US 2024 consultancy blog, arithmetic corrected by the checker; a US figure, not Thai |
| Filling consumables | USD 0.001 to 0.004 | S | ASSUMPTION | Asian can-factory project profile (S) |
| Seaming | USD 0.0001 to 0.0005 | S | ASSUMPTION | Seamer vendor page (S) |
| CO2 for carbonation | USD 0.0003 to 0.0018 | S | PROXY | IMARC news on CO2 prices (S); the high excludes a 50% purge loss, which would give 0.0027 |
| Sugar, flavour and liquid | USD 0.027 to 0.040 per can | S | ASSUMPTION | Built on a Thai sugar price proxy (21 to 29 THB per kg, S); the basis is mixed |
| Group nameplate | 1,000 million litres per year | S | PROXY | Wikipedia and a 2012 news report; scope (group or site) not stated |
| Canned share | 55.3% | S | PROXY | A Vietnamese peer brewer (S) |
| Utilisation | 58.4 to 63.3% | S | PROXY | Prachachat news on Thai capacity (S) |
| Fixed cost | THB 0, 300, 600 million per year | — | ASSUMPTION | Scenarios only; not sourced |

## 3. Results

Variable cost per can, from the sourced inputs:

| Item | Low (USD) | High (USD) |
|---|---|---|
| Sheet metal (LME, no premium) | 0.0432 | 0.0557 |
| Non-metal conversion | 0.0400 | 0.0800 |
| Filling consumables | 0.0010 | 0.0040 |
| Seaming | 0.0001 | 0.0005 |
| CO2 | 0.0003 | 0.0018 |
| Sugar, flavour and liquid | 0.0270 | 0.0400 |
| **Total** | **0.1116** | **0.1829** |
| **Total in THB** | **3.72** | **6.09** |

Cost per can at middle variable cost (THB 4.90) by volume and fixed cost:

| Cans per year | Fixed 0 | Fixed THB 300 m | Fixed THB 600 m |
|---|---|---|---|
| 0.5 billion | 4.90 | 5.50 | 6.10 |
| 1.0 billion | 4.90 | 5.20 | 5.50 |
| 1.68 billion (nameplate) | 4.90 | 5.08 | 5.26 |

Premium sensitivity (mid inputs, THB per can at zero, USD 100 and USD 200 per tonne): 1.65, 1.70, 1.76. Each USD 100 per tonne adds about THB 0.055 per can.

## 4. Production scenarios

- Nameplate 1,000 million litres × 55.3% canned share = 553 million litres of cans, or **1.68 billion cans** at 100% utilisation.
- At 58.4 to 63.3% utilisation: **0.98 to 1.06 billion cans per year.**
- Nameplate per can line: 500 to 1,200 million cans (a proxy from a Crown plant, which the checker says is installed capacity, not a line figure). That implies **one to two lines** at 1 billion cans. The line count is not reconciled with the group volume; see section 5.

## 5. Not in the model (and why)

- **Regional aluminium premium and sheet rolling.** No input. The premium scenarios above show the effect.
- **Scrap credit.** Scrap generated is 1.4 to 3.5 g per can, but no scrap price. Not netted, so the cost is overstated by the credit.
- **End and tab conversion, lacquer-curing gas, secondary packaging** (carton, shrink, pallet). No input.
- **Excise on sugar-sweetened drinks** (item 02.02). The primary rates are now read (`raw/gazette_sugar_drink_excise_primary_2560_A095_111.md`): 14% ad valorem in every tier, plus 0, 1, 3 or 5 baht per litre by sugar per 100 ml from 1 October 2566. Per 330 ml that is 0, 0.33, 0.99 or 1.65 baht. Not in the model yet: the ad valorem base is not read, so the 14% has no baht figure. A sugar-free lime drink is in the 0-baht tier, but still under 02.02 at 14% ad valorem. Later amendments are not checked.
- **Freight, distribution, marketing, overheads, depreciation, line capex.** Only a company-level D&A ratio was found, and the Heineken Malaysia report it cites was unreadable.
- **Lacquer and ink, labour, electricity.** Sub-components of the conversion proxy. Adding them would double-count (the checker flagged this).

## 6. Corrections to earlier records

- **`rework/53`:** the metal figure was 9.6 g per can, giving THB 1.00. The sourced can mass gives 14.4 to 18.5 g of sheet, which at the LME price gives **THB 1.44 to 1.86 of metal per can**. The 9.6 g figure is not supported.
- **`rework/58`:** the metal share and the plant-model yield (18 to 21 g of can per can, from IMARC) are now reflected in the sheet-input range. The model uses the derived 14.4 to 18.5 g, labelled ASSUMPTION.

## 7. Policy check

- Almost every input is **secondary**. The primary items used are a patent (the scrap statement, used only inside an assumption) and a company press release on plant capacity (not used in the cost).
- Primary sources that would close the largest gaps: the LME cash settlement on lme.com; the Bank of Thailand reference rate; the Excise Department's sugar levy rates and the law; Boon Rawd or Singha filings with the DBD (group volume, cost of sales, lines); and a Thai can-maker's annual report (Thai Beverage Can publishes one; capacity and volume are the missing figures).
- The Aluminum Association LCA (primary) gives the scrap and remelt figures, but its PDF was not parsed, so those figures are unverified.

## 8. Limits

- Desk only. No quote, no plant data, no Singha data.
- Mostly US and regional proxies, not Thai.
- The group nameplate and utilisation may refer to different scopes.
- The model is not a cost-to-serve for the lime product; it covers the can only.

## Audit corrections (19 October 2026)

- **Desk total:** the variable cost is THB 3.7 to 6.1 per can. With the fixed-cost adder, the total is THB 3.9 to 7.3. The earlier 'about THB 4 to 6.5' is withdrawn.
- **Fixed-cost adder:** THB 0.2 to 1.2 per can, by volume and fixed cost (0.18 at full nameplate with THB 300 million; up to 1.2 at 0.5 billion cans with THB 600 million). Not 0.1 to 0.6.
- **FX:** the 33.32 low is a 16 September reading. The 18 October XE rate is 33.44. Use 33.44 as the one FX input across rework/53, 56 and 61, and reconcile the 33.46 in the older script.
- **IMARC:** the sheet-input range (14.4 to 18.5 g) is driven by the 13 to 15 g can mass. IMARC's 18.0 g is a sensitivity, not the basis of the range.
- **Nameplate citation:** the record says 2012 news and the script says 2018. Use one year when the source is saved.
- **Not saved in the repo (unverified until the page text is saved to rework/raw/):** the LME prices (alcircle and Trading Economics), the XE rate, the sugar price (21 to 29 THB per kg), the non-metal conversion (sciencefix), the peer canned share (55.3%), utilisation (58.4 to 63.3%), the Crown line capacity, and the scrap figure (1.4 to 3.5 g).

## Primary update (19 October 2026)

The model now uses primary values where they were read:
- **LME cash:** US$3,013.00 to 3,014.00 per tonne, the official cash bid and offer, data valid 16 October 2026 (`raw/lme_trading_summary_primary_2026-10-19.md`). This replaces the news-report band (2,998.50 to 3,008.50).
- **USD/THB:** 33.3535 to 33.7455, the Bank of Thailand average buying (sight) and selling (transfer) rates as of 15 October 2026 (`raw/bot_fx_primary_2026-10-15.md`). This replaces the XE band.

Result: variable cost is THB 3.73 to 6.14 per can, middle THB 4.94 (before, THB 3.72 to 6.09). Sheet metal is USD 0.0434 to 0.0558 per can.

Still not primary: the excise ad valorem base (the Gazette rates are primary now; see section 5), the non-metal conversion (a US proxy), the sugar liquid (an assumption), the scrap and the premium. The regional aluminium premium and scrap credit remain missing.

Can capacity, now from the primary filing: BJC's 56-1 One Report 2025 says TBC has 4 can production lines and added a fifth (hybrid) line in 2025. The 2022 expansion of 400 million cans a year is stated as about 10% of current capacity, which derives to roughly 4,000 million cans a year (approximate; `raw/bjc_one_report_2025_tbc_excerpt.md`). The line count and the 2022 timing are not reconciled. This is not used in the cost per can, which does not depend on the can plant's capacity.
