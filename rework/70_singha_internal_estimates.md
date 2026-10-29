Estimates derived from public data; not Singha figures.

# 70. Singha Lemon Soda: estimates of Singha's internal figures (task T7, slide 4)

**Estimates derived from public data; not Singha figures.** Singha Corporation does not publish the can volume, the can price structure, the can cost, the plant capacity or the cube plan. Every number below is a derived estimate with its anchors tiered. None of them is a Singha figure, and none should be presented as one.

Date of work: 20 October 2026. Revised the same day after the second independent check (section 0). Script: `rework/screen/singha_internal_estimates.py`. Results: `rework/screen/singha_internal_estimates_results.json` (all self-checks pass; seed 20261020; 200,000 draws). Shared can-cost script: `rework/screen/can_cost_model.py` (results `rework/screen/can_cost_model_results.json`; chart `rework/screen/can_cost_non_aluminium.png`). The 90 per cent ranges are the 5th and 95th percentiles of the fixed-seed draws over the stated input bounds. Central values use the modal value of each triangular input and the midpoint of each uniform input. They are not calibrated statistical intervals (section 2.3).

---

## 0. What changed after the second independent check, and what is still open

The verifier's 21 items are each addressed below. No verifier point was rejected. Where a point could not be closed from sources, it is a stated limit (section 5), not an open item.

| Verifier item | Action this turn |
|---|---|
| 1. The 7-Eleven 24-can reading (THB 330) is a promotion | Verified: the live page prints 330 against a struck-through 408, a minus 19 per cent badge, a saving of 78 and a promotion valid to 20 October 2026 (`T7/7eleven_d01_promotion_check_2026-10-20.md`). The four readings are relabelled as online listing prices. The promotion is disclosed. Sensitivities added: undiscounted 408 (mean THB 14.615; top-down cans 112.6 million) and the mean without the promotional reading (THB 13.82; 119.0 million). The central stays at the mean of four (THB 13.80). The word "realised" is removed from the slide text. The conflict with record 68d section 2 is listed in section 6. |
| 2. Pilot break-even mixes before-excise and after-excise bases | Headline is the chain basis (after excise): about 127,000 cubes (90 per cent range 114,000 to 159,000). The before-excise model basis (101,833) is kept for reconciliation only and is not in judge-facing text. |
| 3. Slide 9 source line cites records 58 and 61; two slide 9 texts | Source line rewritten in public terms (section 7.2). One slide 9 text only, with "carbon dioxide". |
| 4. Conflict list incomplete; deck line reference wrong | Conflict rows added (section 6). The THB 4.94 appears in deck lines 133 and 135 only, not 136. The minimum-run statement in submission/11 is at lines 135 and 269 (line 193 names the co-packers without a minimum). |
| 5. Share anchor measurement year | The article says the share was held "two years after launch". The launch is dated August 2020 (record 69), so the measurement is 2021 or 2022: unresolved. The slide text says so. The central applies to the 2025 market either way. |
| 6. No 90 per cent interval for the headroom and the at-risk values | Drawn in the script: line hours (speed and efficiency assumptions) and at-risk values (can and cube contribution draws). The count-basis capacity percentage has no interval because the nameplate scope is unknown (stated in the table). |
| 7. Two derivations are not independent for 3a, 5a and 6a | Stated in the table (section 1) and as limits (section 5). No independent second source was found for the non-aluminium cost or the cannibalisation share. |
| 8. Four open points not closed; distributor margin in slide text | The four searches were attempted again this turn and returned the notice that this turn's web search budget is used up (none ran). They are now stated limits with the follow-up route (section 3.3). The distributor margin is marked in the slide text as an unsourced assumption. |
| 9. Excise label | The 14 per cent is P as saved, read from page images. A second-reader check of the Thai numerals and a search for later amendments are outstanding; both are stated (section 5). |
| 10. Arnifo tier and pilot conflict | The page lists pilot batch steps and also states "No small trial, pilot or pre-commercial sales production". Tier aligned to COMPANY CLAIM in the save and the record (`T7/arnifo_oem_moq_recheck_2026-10-20.md`). |
| 11. "The true figure may be lower" | Removed from slide 4. |
| 12. Draw median not beside the central | Slide 4 states the median (111 million) beside the modal central (119 million). |
| 13. Six-can row missing from the script; 7,840 slip | Added to the script. The zero-contribution price for the six-can case is USD 7,834 a tonne. |
| 14. Zero-contribution method wording | Corrected: net revenue after VAT, margins and excise, less all non-aluminium variable cost, divided by sheet mass times FX. |
| 15. The 1,357 million figure and the 2021 label | The saved text (T6/09) prints no year for 1,357 million. It equals 28 million litres at THB 16 a can to within 0.04 per cent, so it may be derived, not a sales figure. The gap to 1,450 million is 6.9 per cent. Neither is used as a sourced 2021 value. |
| 16. The 68e anchor is a category median | Stated: the multipack median of THB 13.75 is a category median over 18 multipack rows of lemon, lime and clear soda packs (record 68e section 1, citing the 68d second pass). The record does not show whether Singha packs are among the 18, so the anchor is not an independent Singha price and is not counted as a second source for the price. |
| 17. CP ALL capture says no publication date | The live page prints "Published on 24/03/2026" (WebFetch, 20 October 2026; `T7/cpall_ye68_publication_date_check_2026-10-20.md`). Thailand scope remains an inference. The capture file itself is outside this task's outputs; the lead should correct its date line. |
| 18. Stale chart | `can_cost_model.py --chart` was run. The new chart is `rework/screen/can_cost_non_aluminium.png`. The stale `rework/charts/can_cost_per_unit.png` still exists and must be replaced or removed by the lead. |
| 19. CO2 versus carbonation | Slide 9 uses "carbon dioxide" only. |
| 20. The 7-Eleven "about 7 cans a store a day" check mixes years | Dropped from slide text. Kept in section 2.2 as an indicative check only, with the note that no 2021 store count is sourced. |
| 21. Zero-contribution point stated at the listing price | Slide 9 now says the point is at net revenue of THB 7.39 (a listing price of THB 13.80). |

**Other changes.** The aluminium price is still not used (LME route not authorised; the LME page returned HTTP 403 on 20 October 2026). The earlier THB 4.94 can cost is superseded (section 6). The non-aluminium cost is THB 3.27 (2.62 to 3.92). No browser was launched, no form was submitted, no account was created, no outside contact was made, no supplier quote was requested, and no arbitrary file was downloaded. Nothing was committed or pushed. No file in `rework/submission/`, `rework/proposal/` or `rework/deck/` was edited.

---

## 1. Estimate table

Central values first. Where the central is a modal value and the draw median differs, both are shown.

| # | Estimate | Central value | 90% range | Tier and status | Derivation A | Derivation B | Gap and note |
|---|---|---|---|---|---|---|---|
| 1a | Lemon Soda cans a year | **119 million** (modal central; the draw median is 111 million, because the price input is skewed) | Top-down 83 to 137 million; bottom-up 26 to 91 million | DERIVED. Market S (press, mixed windows, section 2.5); share S (Positioning, 4 July 2022, measurement 2021 or 2022, unresolved) with an ASSUMPTION band; price S (online listings, 20 October 2026) | Top-down: market THB 70,000 million times share 2.35 per cent, divided by listing price THB 13.80 | Bottom-up: 15,945 stores (P) times 0.8 stocking share times 6 cans a store a day times 365, divided by a 0.55 7-Eleven channel share (three ASSUMPTIONS): **51 million** (26 to 91 million) | The two methods are independent in their inputs. The bottom-up is 43 per cent of the top-down. Price sensitivities: THB 17.00 gives 96.8 million; undiscounted 408 gives 112.6 million; mean without the promotion gives 119.0 million; Lotus's six-can gives 116.1 million; THB 13.54 gives 121.5 million. |
| 1b | Net revenue to the producer after VAT, margins and excise (THB million a year) | **881** (646 to 1,061) | as shown | DERIVED from 1a and 3b | Top-down cans times net THB 7.39 | Bottom-up cans times THB 7.39: **376** (201 to 710) | Top-down net revenue equals retail value times the chain ratio, so it does not depend on the listing price chosen (section 2.1). Bottom-up is a cross-check only. |
| 1c | Retail value of Lemon Soda a year (THB million) | **1,645** | 1,243 to 1,992 | DERIVED. Retail basis assumed | Market times share | Not derived | The market value basis (retail or manufacturer) is not stated by any source. A manufacturer basis would lower it. |
| 2a | Share of Singha Corporation 2025 revenue (THB 3,892 million, press) | **22.6%** | 16.6 to 27.3% | DERIVED. Revenue S (MGR Online, 23 May 2026, no source named) | Top-down net revenue divided by 3,892 | Bottom-up: **9.6%** (5.2 to 18.2%) | Conditional: holds only if Singha Corporation books the can. Booking entity not known. The two derivations share the can volume of 1a, so they are not independent of it. |
| 2b | Share of Singha Corporation 2025 net profit (THB 3,085 million, press) | **15.9%** | 11.2 to 21.2% | DERIVED. Net profit S (same article, no source named) | Top-down contribution before aluminium (THB 492 million) divided by 3,085 | Bottom-up: **6.8%** (3.6 to 13.8%) | Contribution is before aluminium, labour, overhead, depreciation and tax. Not like for like with net profit. |
| 3a | Variable cost per can excluding aluminium (THB a can) | **3.27** | 2.62 to 3.92 (bounding cases 2.28 to 4.26) | DERIVED from component inputs (S, PROXY, ASSUMPTION; section 2.7) | Component build from records 58 and 61 with the aluminium line removed | **Not an independent second derivation.** Peer full-cost check (section 2.7): THB 4.27 to 5.23 a can, leaving THB 1.01 to 1.96 for aluminium and fixed cost. It is a basis check. | Stated limit: no independent second source for the non-aluminium cost was found (section 5). |
| 3b | Price chain: listing price, invoice and net to producer (THB a can) | Listing price **13.80**; invoice before excise **8.60** (8.02 to 10.17); net after excise **7.39** (6.90 to 8.75) | as shown | DERIVED. VAT P; excise P as saved (read from page images); retailer margin S (group proxy, median of three); distributor margin **UNSOURCED ASSUMPTION** (10 to 20 per cent; open) | Listing price divided by 1.07, times (1 minus 21.6%), times (1 minus 15%), times (1 minus 14%) | Team model: 60 per cent of a THB 15 shelf (THB 9.00) through the same chain at THB 15 gives THB 9.34 invoice before excise | Invoice is 62 per cent of the listing price. The 60 per cent in the submission is within two points. |
| 3c | Aluminium cost (not a number) | Slope **THB 0.055 a can per USD 100 a tonne** (0.049 to 0.061). Zero contribution at **USD 7,477 a tonne** (6,008 to 10,603) | n/a | Stated limit. Sheet mass ASSUMPTION; the aluminium price is not sourced | n/a | n/a | No aluminium price is used. Single-can case (THB 17.00): USD 10,581 a tonne. |
| 4 | Variable gross margin before aluminium | **55.8%** (47.4 to 67.3%) | as shown | DERIVED | A (bottom-up): (net less variable cost) divided by net: 4.13 divided by 7.39 | B (top-down, peer-implied): at the peer median of 40.1%, the full cost per can on the same net price is THB 4.43, leaving THB 1.16 (0.53 to 2.26) for aluminium and fixed cost | Different bases (variable against full cost). Peer margins are for brand owners, bottlers and retailers. Peer bottler mean 36.7%. The gap is a basis difference, not an efficiency finding. |
| 5a | Group can capacity and headroom | 1,676 million cans at 100% of nameplate; 996 million at Thai Beverage Can's 59.46% use; 679 million unused | Count basis: no interval (nameplate scope unknown; a bound would be invented). Line hours: see below | PROXY (group nameplate 1,000 million litres; scope unclear; canned share 55.3%, Vietnamese peer) | A (count basis): cube volume as a share of unused can slots. 200,000 cubes is 0.03% of unused slots; 1,000,000 is 0.15%. Shown for scale only | B (line hours): 200,000 cubes need **79 hours** at 60 pouches a minute and 70% efficiency (2.0% of 4,000 hours; 0.9% of 8,760). 90% range **45 to 152 hours** (1.1 to 3.8% of 4,000). 1,000,000 cubes need **397 hours** (9.9%; 90% range 227 to 760 hours, 5.7 to 19.0%). At 20 a minute, 1,190 hours (29.8%) | A treats a cube as one can slot, so A and B are not independent. No pouch, sachet or dry-solids line is evidenced at any group company. The co-packer minimum binds before line time (5b). |
| 5b | Co-packer minimum run | 500,000 to 1,500,000 units per SKU and formula, phased within 12 months (co-packer's own terms) | Bounds only: the range is the claim | COMPANY CLAIM (co-packer's own page; read by WebFetch as an extract, section 3.1) | At 200,000 cubes a year: 2.5 years (500,000) to 7.5 years (1,500,000) of volume to fill the minimum; midpoint 5 years | At 1,000,000 cubes a year: 0.5 to 1.5 years | The page also lists a pilot batch step and states no pilot or pre-commercial sales production (conflict noted). Dry solids at 200,000 cubes: 162 kg potassium bicarbonate and 420 kg citric acid a year (team specification). |
| 6a | Can contribution at risk if 25 or 50% of cube buyers are existing can buyers, at 200,000 cubes a year | **THB 206,000** (25%) and **THB 413,000** (50%): upper bounds, before aluminium (90% ranges 169,000 to 284,000 and 339,000 to 567,000) | as shown | DERIVED | Displaced cans times can contribution, as a share of top-down can volume: 0.04% and 0.08% | The same ratio on bottom-up can volume: 0.10% and 0.20%. **Not an independent derivation** (same ratio, two denominators) | Net change after the cube's own contribution, at zero aluminium, central: planning price THB 15 (cube THB 3.94): **minus THB 9,000** (25%) and **minus THB 18,000** (50%); 90% ranges minus 86,000 to plus 11,000 and minus 171,000 to plus 21,000. At the can's listing price (cube THB 3.30): minus 41,000 and minus 82,000 (90% ranges minus 74,000 to minus 9,000 and minus 147,000 to minus 17,000). At 1,000,000 cubes: section 2.11. |
| 6b | Aluminium price above which a can-to-cube switch does not lower contribution | **USD 331 a tonne** at the planning price (draw range minus 388 to 3,139; a negative value means the cube earns more even at zero aluminium); **USD 1,493 a tonne** at parity with the can's listing price (316 to 2,720) | as shown | DERIVED | Can contribution before aluminium less cube contribution, divided by sheet mass times FX | n/a | A switch lowers contribution per unit only if aluminium costs less than these prices. The aluminium price is not sourced. |
| 7 | Pilot fixed-cost break-even at THB 500,000 a year (cubes a year, steady state) | **127,000** (chain basis, planning price THB 15 after excise; 90% range 114,000 to 159,000) | as shown | DERIVED. Fixed cost ASSUMPTION (submission 05) | A (model basis, ex-factory THB 9.00 less THB 4.09, **before excise**): 101,833. Reconciliation only, not in judge-facing text | B (chain basis, after excise): 126,769 (headline) | Sensitivity, cube at the can's listing price (cube contribution THB 3.30): 151,388. Model NPV break-even in record 05: 146,230. Coverage of THB 500,000 at 200,000 cubes: 1.58 times (B); at 50,000 cubes: 0.39 times (B). Both bases use the same fixed cost; the basis difference is excise only. |

---

## 2. Method

### 2.1 Price basis (the explicit choice)

- **Central listing price: THB 13.80 a can**, the unweighted mean of four online listing prices for the Singha Lemon Soda multipacks, read on 20 October 2026 (record 68d, S):
  - D06, Makro PRO, 24-can case, THB 325 for 24: THB 13.54.
  - D01, 7-Eleven ALL Online, 24-can case, THB 330 for 24: THB 13.75. **This is a promotional selling price.** The page prints 408 struck through, a minus 19 per cent badge, a saving of THB 78, and a promotion valid to 20 October 2026 (`rework/raw/diligence_2026-10-20/T7/7eleven_d01_promotion_check_2026-10-20.md`, read 20 October 2026, S).
  - D12, Lotus's Shop Online, 24-can case, THB 330 for 24: THB 13.75.
  - D13, Lotus's Shop Online, six-can pack, THB 85 for six: THB 14.17.
  - Record 68e gives the same level as a category median (section 1 of 68e): THB 13.75 per 330 mL over 18 multipack rows of lemon, lime and clear soda packs. The record does not show whether Singha packs are among the 18. It is a category anchor, not an independent Singha price.
- **Top of range: THB 17.00,** the single-can online list price at Lotus's (68d S01). It is an online list price for a single can, not a store shelf price, and it is run as its own case.
- **Promotion sensitivities.** (i) The undiscounted 408 list reading for the 24-can case is THB 17.00 a can; with that reading, the mean of four is THB 14.615 and the top-down volume is 112.6 million. (ii) Without the promotional reading, the mean of the other three is THB 13.82 and the top-down volume is 119.0 million. The central is therefore not sensitive to whether the promotion is counted (about 0.2 per cent).
- **Excluded:** the 7-Eleven six-pack at THB 172 (THB 28.67 a can; 68d D02), which record 68d reads as about twice the 24-can price per can; and the Makro PRO six-pack at THB 82 (THB 13.67 a can, 68d D07), whose one-pack reading is not settled (section 3.1). Neither is in any range.
- **Why the mean of the four readings:** the mix of pack sizes that shoppers buy is not sourced. The readings are the sourced prices for the product itself. A weighted average would need a pack mix, which is not available (stated limit).
- **Effect.** The top-down volume depends on this price. Top-down net revenue does not, because the top-down cans equal retail value divided by price, and the net price per can is the same chain applied to that price. The price cases (central values):

| Case | Listing price (THB a can) | Top-down cans a year | Net after excise (THB) | Contribution before aluminium (THB) | Variable margin before aluminium | Aluminium price at zero contribution (USD a tonne) | Top-down net revenue (THB million) |
|---|---|---|---|---|---|---|---|
| Single-can online list, Lotus's (68d S01) | 17.00 | 96.8 million | 9.11 | 5.84 | 64.1% | 10,581 | 881 |
| Mean of four with the 7-Eleven 24-can at its undiscounted THB 408 | 14.615 | 112.6 million | 7.83 | 4.56 | 58.3% | 8,266 | 881 |
| **Central: mean of four readings (promotion included, disclosed)** | **13.80** | **119.2 million** | **7.39** | **4.13** | **55.8%** | **7,477** | **881** |
| Mean of three readings without the promotional reading | 13.82 | 119.0 million | 7.40 | 4.14 | 55.9% | 7,494 | 881 |
| Lotus's six-can (68d D13) | 14.17 | 116.1 million | 7.59 | 4.32 | 57.0% | 7,834 | 881 |
| Lowest reading, Makro PRO 24-can (68d D06) | 13.54 | 121.5 million | 7.25 | 3.99 | 55.0% | 7,223 | 881 |

### 2.2 Cans and revenue (estimates 1a to 1c)

- Top-down: cans = carbonated soft-drink market (THB million, press values; section 2.5) times 1,000,000 times Lemon Soda share, divided by the listing price per can (section 2.1). Central: 70,000 times 2.35 per cent divided by 13.80, giving 119.2 million.
- Bottom-up: cans = 15,945 stores (CP ALL, end 2025, P; Thailand by inference, section 3.1) times share of stores that stock the can (0.5, 0.8, 1.0; ASSUMPTION) times cans a stocking store a day (2, 6, 12; ASSUMPTION) times 365, divided by the 7-Eleven share of can volume (0.40, 0.55, 0.70; ASSUMPTION). Central: 50.8 million.
- Indicative check only, not an input: the 2021 press volume of 28 million litres (84.85 million cans at 0.33 litre) would be about 7 cans a store a day if 7-Eleven carried half of it. No 2021 store count is sourced, so this is not a rate and is not used.
- Revenue: cans times the net price per can (section 2.3).
- Retail value: market times share (retail basis assumed; section 4).

### 2.3 Input bounds, and what the ranges mean

- The 90 per cent ranges are the 5th and 95th percentiles of the draws. Each draw takes every input from its stated bounds. They are ranges from the stated bounds, not calibrated statistical intervals.
- Bounds that are **assumptions** (no source): 7-Eleven stocking share (0.5 to 1.0); cans a store a day (2 to 12); 7-Eleven channel share (0.40 to 0.70); distributor margin (10 to 20 per cent); sheet mass per can (14.4 to 18.5 g); filling (USD 0.001 to 0.004); seaming (USD 0.0001 to 0.0005); the liquid line (USD 0.027 to 0.040, built on a sugar proxy); line speed (20 to 120 pouches a minute, mode 60) and efficiency (0.50 to 0.85, mode 0.70); the planning shelf price of the cube (THB 15); the cube's fixed cost (THB 500,000); the 1:1 switch in cannibalisation.
- Bounds that are **proxies**: non-metal conversion (US 2024, USD 0.04 to 0.08); CO2 (USD 0.0003 to 0.0018); retailer margin (group all-category gross margins, 16.1, 21.6 and 31.7 per cent; the mode is their median, the Big C figure); canned share (55.3 per cent, a Vietnamese peer).
- Central values are modal (triangular) or midpoint (uniform). The draw median for top-down cans is 111 million against a modal central of 119 million, because the price input is skewed toward the single-can end. Both are reported; the slide states both.
- The co-packer minimum is drawn uniformly across the company's stated range (500,000 to 1,500,000) only for the years-to-fill figure. The range itself is the claim.

### 2.4 Share anchor (Positioning, 4 July 2022)

- Printed: Singha Lemon Soda "2.4% of the total carbonated soft-drink market"; "THB 1,450 million"; "12%" (of the can segment, no year printed). The article's sentence says the share was held "two years after launch" (หลังจากเปิดตัวได้ 2 ปี). The carbonated soft-drink market is THB 62,725 million (2021); the canned segment is THB 13,172 million (21 per cent, 2021 inferred).
- **Year of the share: unresolved between 2021 and 2022.** The launch is dated August 2020 (record 69). Two years after launch is about 2022. The article's market value is the 2021 value. No printed text settles the year, so both are stated.
- Arithmetic: 1,450 divided by 62,725 is 2.31 per cent; 1,450 divided by 13,172 is 11.0 per cent; 12 per cent of 13,172 is 1,581. The printed 2.4 per cent and 12 per cent do not reconcile with the printed 1,450. The 12 per cent is not used.
- The central share is 2.35 per cent, the midpoint of the printed 2.4 and the computed 2.31. The band 1.5 to 3.0 per cent is an assumption of change between the measurement and 2025.
- Saved text: `rework/raw/diligence_2026-10-20/T7/positioning_2022_07_04_csd_share.md`. Earlier citation to the 2020 Positioning article (T1) was wrong and is withdrawn.

### 2.5 Market value (the five 2025 press values, relabelled)

The five values are a mix of windows and statuses, not one 2025 series:

- 67,000 million baht: Bangkokbiznews, 13 October 2025. Labelled 2025; window not stated; no source named.
- 68,000 million baht: a named ThaiBev executive, reported 13 October 2025. Labelled 2024 by its source; may be a 2025 level.
- 70,000 million baht: Marketeer compilation, 17 April 2026, "NielsenIQ and brand forecasts". Labelled 2025.
- 70,772 million baht: NielsenIQ, 12 months to November 2024, as printed by Thansettakij (14 January 2025). A 2024 window.
- 76,900 million baht: KResearch, a 2025 estimate or forecast, via Thansettakij (8 September 2025). A forecast.

The central is the median (70,000). It is **not a 2025 actual**: it mixes 2024 and 2025 values and one forecast. The 2025 direction is disputed (record 67). The triangle is 67,000, 70,000, 76,900. Market basis (retail or manufacturer) is not stated by any source.

### 2.6 Price chain (estimate 3b)

- Listing price (shelf, incl. VAT) divided by 1.07. VAT 7 per cent: Revenue Department, rd.go.th/59.html, read 20 October 2026 (P; extended to 30 September 2027; `rework/raw/diligence_2026-10-20/T9/rd_vat_7_percent_2026.md`).
- Retailer margin: the retailer's gross margin on all categories, FY2025: CP Axtra 16.1 per cent, BJC (Big C) 21.6 per cent, CRC 31.7 per cent (stockanalysis aggregator, S; `rework/raw/diligence_2026-10-20/T4/retail_groups_financials_stockanalysis_2026-10-20.md`). The mode is the median of the three, which is the Big C value. It is a PROXY. No beverage-specific retail margin and no 7-Eleven operator margin were read (stated limit, section 5).
- Distributor margin: 10 to 20 per cent, central 15 per cent. **UNSOURCED ASSUMPTION** (the team's band in records 53, 76 and submission 10). No Thai beverage distributor margin was read; the search could not be run this turn (section 3.3).
- Excise: 14 per cent ad valorem on item 02.02 (Royal Gazette B.E. 2560, P as saved, record 69 section 6). The saved text was read from page images; a second reader should check the Thai numerals before public use; later amendments were not searched; and the ad valorem base was not read (the Gazette PDF returned HTTP 403 on 20 October 2026). Applied to the ex-VAT invoice as an assumption. Net to the producer = invoice times 0.86.

### 2.7 Variable cost (estimate 3a) and the peer check

- Components, reused from records 58 and 61 with the aluminium line removed: non-metal conversion (USD 0.04 to 0.08, PROXY, US 2024); filling consumables (USD 0.001 to 0.004, ASSUMPTION); seaming (USD 0.0001 to 0.0005, ASSUMPTION); CO2 (USD 0.0003 to 0.0018, PROXY); liquid (USD 0.027 to 0.040, sugar proxy, ASSUMPTION). FX THB 33.3535 to 33.7455 per USD (Bank of Thailand, 15 October 2026, saved copy, P as saved; not re-verified today, section 3.1). Central: USD 0.0974 times FX midpoint 33.55, which is THB 3.27.
- Aluminium: sheet mass 14.4 to 18.5 g (ASSUMPTION). Cost per can = sheet grams times USD a tonne divided by 1,000,000, times FX. Slope THB 0.0552 a can per USD 100 a tonne.
- **Zero-contribution price** = (net revenue after VAT, margins and excise, less all non-aluminium variable cost of THB 3.27) divided by (sheet mass times FX). Central USD 7,477 a tonne. No aluminium price is used.
- Peer check (a basis check, not a second derivation): each bottler's full cost per can = (1 minus its gross margin) times the net price. ThaiNamthip (38.5 per cent) gives THB 4.55; Haad Thip (42.2 per cent) gives THB 4.27; Sermsuk (29.25 per cent) gives THB 5.23. Subtracting the variable cost leaves THB 1.01 to 1.96 for aluminium and fixed production cost. These are full-cost figures for peers, so the room is a basis comparison and not a threshold.

### 2.8 Can-cost model (rework/screen/can_cost_model.py, updated and rerun)

- The non-aluminium inputs are read from the shared INPUTS table in `singha_internal_estimates.py`, so there is one set of inputs in the repo.
- The LME input is removed. Aluminium appears only as a slope and a break-even price.
- Utilisation: Thai Beverage Can's printed utilisation for 2024 and 2025 (58.57 and 59.46 per cent; P, third party). It is not the Boon Rawd group figure.
- Results (`rework/screen/can_cost_model_results.json`): non-aluminium variable cost THB 3.27 at the midpoint convention; bounding cases THB 2.28 (all inputs at low bounds) and THB 4.26 (all at high bounds). The bounding cases are wider than the 90 per cent range (2.62 to 3.92).
- Chart: `rework/screen/can_cost_non_aluminium.png`, produced by `python can_cost_model.py --chart` on 20 October 2026. It shows the central variable cost with the bounding band. The stale LME-based chart `rework/charts/can_cost_per_unit.png` is superseded (section 6).
- The earlier mid-input result of THB 4.94 (3.73 to 6.14) used the LME reading and is superseded (section 6).

### 2.9 Margins against peers (estimate 4)

- Peer gross margins are the saved values: The Coca-Cola Company 61.6 per cent (FY2025; record 68a section 6.1); PepsiCo 54.15 per cent (FY2025, derived; record 68b section 7.2); ThaiNamthip 38.5 per cent (FY2024, on sales of goods; record 68a 6.2); Haad Thip 42.2 per cent (FY2025; record 68a 6.3); Sermsuk 29.25 per cent (FY2024, derived from its filing; record 68b 7.1); ThaiBev non-alcoholic segment 36.58 per cent (FY2025, derived; record 68c 5.3); Osotspa 40.1 per cent (FY2025; company page; year end S; record 68c 5.1). Median 40.1 per cent; Thai bottler mean 36.7 per cent.
- Two derivations (section 1, row 4) are on different bases and are not independent: A is the variable margin of the can at the central listing price; B is the full-cost margin implied by the peers on the same price.

### 2.10 Plants, capacity and co-packer (estimate 5)

**Plants and the filling site.** The Boon Rawd company pages name eight manufacturing companies (plant.boonrawd.co.th/en/about, read 20 October 2026; S; undated content). For each, the company pages print the following, and no capacity or can line for any of them:

1. Pathumthani Brewery: beer, soda and drinking water (Thai history page).
2. Chiang Mai Beverage: soda and bottled drinking water.
3. Khon Kaen Brewery: Leo beer; registered capital THB 1,300 million.
4. Wangnoi Beverage: drinking water and soda. Lines 1 and 2 make drinking water (500 mL) and glass-bottle soda (400 mL), and "soda 325 mL (one-way)", whose container is not stated. The new site has PET water at up to 72,000 bottles an hour per line. No can line is named.
5. Boonrawd Asia Beverage: PET bottled drinking water.
6. Surat Thani Beverage: products not stated.
7. Singha Beverage (Bang Len, Nakhon Pathom): Leo beer; "currently has a capacity of 925 million litres a year" (undated; no mention of cans).
8. Mahasarakham Beverage: water and soda.

Thai Beverage Can's filing (P; BJC One Report 2025) names Singha Beverage Co., Ltd. as one of five main domestic customers, with no product or plant named. No source names the plant that fills the 330 mL can or a co-packer for it.

**Capacity.** Group can capacity is a PROXY: 1,000 million litres times 55.3 per cent canned share divided by 0.33 litre = 1,676 million cans at 100 per cent, which is 996 million at Thai Beverage Can's 59.46 per cent use (third party, not the group). The scope of the 1,000 million litres is unclear.

**Derivations.** A (count basis): cube volumes as a share of unused can slots (not a line-time figure). B (line hours): hours at assumed speeds of 20, 60 and 120 pouches a minute and 70 per cent efficiency, with a draw over speed (triangular, mode 60) and efficiency (uniform 0.50 to 0.85). Available hours: 4,000 (two shifts, 250 days, ASSUMPTION) and 8,760 (ASSUMPTION). No line speed is sourced (open; section 3.3).

**Co-packer.** The minimum run is 500,000 to 1,500,000 units per SKU and formula, phased within 12 months, with no pilot run in the company's stated position (Arnifo, COMPANY CLAIM; the same page lists a pilot batch step, which is a conflict; section 3.1). A co-packer would need: a dry-solids or sachet line; a formula and pack specification that the team has not yet fixed; a minimum run of 500,000 or more units for each SKU; and certification. No quote was requested (outside contact is not used in this project).

### 2.11 Cannibalisation (estimate 6)

- Can contribution before aluminium: THB 4.13 a can (central). Cube contribution per cube, on three bases: (i) model basis, ex-factory THB 9.00 (60 per cent of THB 15) less THB 4.09 cost, **before excise**: THB 4.91 (reconciliation only); (ii) chain basis, planning price THB 15 through the same chain, after excise, less THB 4.09: THB 3.94 (headline); (iii) parity, the cube at the can's listing price of THB 13.80 through the same chain, after excise, less THB 4.09: THB 3.30.
- Gross contribution at risk = displaced cans times can contribution before aluminium (an upper bound, because aluminium is excluded from the can). Intervals are drawn from the can and cube contribution draws.
- Net change per switched unit at zero aluminium = cube contribution minus can contribution. The planning-price gap is minus THB 0.18 a unit; the parity gap is minus THB 0.82 a unit.
- Aluminium price above which a switch does not lower contribution per unit = (can contribution before aluminium less cube contribution) divided by (sheet mass times FX): USD 331 a tonne (planning price) and USD 1,493 a tonne (parity).
- The cube cost excludes binder and flavour, which are not priced, so the cube contribution is an upper bound by those two items.

Table of cases (THB, per year; central, with 90 per cent ranges from the draws):

| Cubes a year | Share from existing can buyers | Cans displaced | Gross can contribution at risk (upper bound; 90% range) | Net change at zero aluminium, cube at planning price THB 15 (90% range) | Net change at zero aluminium, cube at listing-price parity THB 13.80 (90% range) |
|---|---|---|---|---|---|
| 200,000 | 25% | 50,000 | 206,000 (169,000 to 284,000) | minus 9,000 (minus 86,000 to plus 11,000) | minus 41,000 (minus 74,000 to minus 9,000) |
| 200,000 | 50% | 100,000 | 413,000 (339,000 to 567,000) | minus 18,000 (minus 171,000 to plus 21,000) | minus 82,000 (minus 147,000 to minus 17,000) |
| 1,000,000 | 25% | 250,000 | 1,032,000 (847,000 to 1,418,000) | minus 46,000 (minus 428,000 to plus 53,000) | minus 206,000 (minus 369,000 to minus 44,000) |
| 1,000,000 | 50% | 500,000 | 2,063,000 (1,695,000 to 2,837,000) | minus 91,000 (minus 857,000 to plus 107,000) | minus 412,000 (minus 737,000 to minus 87,000) |

The displaced cans as a share of top-down can volume are 0.04% (200,000 cubes, 25%) and 0.42% (1,000,000 cubes, 50%). As a share of bottom-up can volume: 0.10% to 0.98%. A positive net change in a draw means the cube contributes more than the can at zero aluminium in that draw.

### 2.12 Pilot fixed-cost fit (estimate 7)

- Steady-state break-even = fixed cost divided by contribution per cube (undiscounted, one year). It ignores discounting and the year-0 cost, so it is lower than the model's NPV break-even (146,230 cubes; record 05).
- Headline (chain basis, after excise): 126,769 cubes a year (90% range 113,802 to 159,419), rounded to 127,000 (114,000 to 159,000) in the judge-facing text.
- Reconciliation only: the model basis (ex-factory THB 9.00 before excise, contribution THB 4.91) gives 101,833. It is not on the same basis (before excise) and is not in any judge-facing range.
- Sensitivity (parity at the listing price, THB 3.30 per cube): 151,388.
- Coverage of THB 500,000 a year on the chain basis: 1.58 times at 200,000 cubes; 0.39 times at 50,000 cubes. The fit depends on the planning price, which is an assumption, and on the unpriced binder and flavour. The pilot fit does not depend on the can volume.

---

## 3. Open points on the can: closure

Each row says what was checked and the result. "Closed" means the figure has a source, a tier, a status and a date read. "Stated limit" means it cannot be closed from sources in this project; the follow-up route is given.

### 3.1 Re-checks and reads made in this turn (WebFetch of named URLs, 20 October 2026)

| Point | Check | Result | Status |
|---|---|---|---|
| 7-Eleven 24-can promotion (D01) | https://www.allonline.7eleven.co.th/p/สิงห์-เลมอนโซดา-330-มล-ยกลัง-24-กระป๋อง/474313/. Saved: `T7/7eleven_d01_promotion_check_2026-10-20.md` | Prints 330 (current), 408 (struck through), minus 19 per cent, saves 78, promotion valid to 20/10/2026. | Closed (S). Disclosed; sensitivities run. |
| Makro PRO one-pack price (product 02emhsl, six-can Lemon) | https://www.makro.pro/p/02emhsl-6814746706115. Saved: `T7/makro_02emhsl_one_pack_recheck_2026-10-20.md` | Prints 13.67 per unit, "buy 3 or more" at 78, and minus 4 per cent against a reference of 82. No label says which price is the one-pack price. | Stated limit: not settled. Excluded from every range. Follow-up: a dated product page that labels the one-pack price. |
| Arnifo minimum run and pilot wording (co-packer) | https://www.arnifo.com/oem-beverage/. Saved: `T7/arnifo_oem_moq_recheck_2026-10-20.md` (both reads) | MOQ 500,000 to 1,500,000 per SKU and formula, phased within 12 months. The process steps list pilot batches; the same page states "No small trial, pilot or pre-commercial sales production". No line speed printed. | COMPANY CLAIM. The conflict is stated. Read route: WebFetch returned an extract, not full page text. |
| CP ALL 15,945 stores (year-end 2025) | https://lssmedia.setlink.set.or.th/2025/YE/CPALL-YE68-ListedCompanySnapshot-EN.html. Saved: `T7/cpall_ye68_publication_date_check_2026-10-20.md` | Prints "Published on 24/03/2026"; store count "by the end of 2025"; 700 new stores "in Thailand"; 138 international stores reported separately. Thailand-only is not stated. | Closed as P for the count. Scope inferred (stated). The earlier capture's "no publication date" line is wrong; the lead should correct the capture. |
| Bank of Thailand rate | https://www.bot.or.th/en/statistics/exchange-rate.html. Saved copy: `T7/bot_and_lme_and_gazette_rechecks_2026-10-20.md` | No rate table and no date on the page. | Not re-verified today. The 15 October saved copy stays P as saved. Stated limit. |
| LME aluminium (re-check) | https://www.lme.com/en/metals/non-ferrous/lme-aluminium. Same saved file | HTTP 403. | Stated limit. Not used. |
| Royal Gazette item 02.02 (ad valorem base) | https://www.ratchakitcha.soc.go.th/DATA/PDF/2560/A/095/111.PDF. Same saved file | HTTP 403. | Stated limit. The 14 per cent rate stays P as saved, read from page images. |
| VAT 7 per cent | Revenue Department, rd.go.th/59.html; `T9/rd_vat_7_percent_2026.md` | Reduced rate of 7 per cent extended to 30 September 2027. | Closed (P). |
| Positioning, 4 July 2022 (share anchor) | https://positioningmag.com/strategic-move/88360. Saved: `T7/positioning_2022_07_04_csd_share.md` | Figure sentences: 12 per cent or 1,450 million "two years after launch"; 2.4 per cent of total CSD; CSD 62,725 million (2021); canned 21 per cent or 13,172 million. | Closed as a secondary source (S). The reconciliation gap and the unresolved measurement year (2021 or 2022) are stated. |

### 3.2 Points from record 69 and the open list

| # | Point | Status and basis |
|---|---|---|
| 1 | Launch month (August 2020 against late 2020) | Stated limit. Two sources conflict. No dated company statement found (record 69 row 1). |
| 2 | Flavours and first press years | Closed as first press reports (record 69 row 2). Months not printed. |
| 3 | Prices THB 16 and THB 17 | Closed (record 69 row 3). |
| 4 | Sugar-free wording | Closed as a company claim (record 69 row 4). No laboratory result. |
| 5 | Current price | Online listing prices, read 20 October 2026 (record 68d): Lotus's single can THB 17.00 (S01); 24-can cases THB 13.54 to 13.75 per can (one of them a promotion, section 3.1); Lotus's six-can THB 14.17 (S). Store shelf price: stated limit (none read). |
| 6 | Channels | Closed (record 69 row 6). |
| 7 | Retail reach | CP ALL 15,945 stores (P; published 24 March 2026; Thailand scope inferred). Can outlet count: stated limit. Lotus's, Makro and Big C store counts: stated limit (Big C pages returned HTTP 403). |
| 8 | Distributor structure and trade split | Stated limit. The 2020 plan (7-Eleven first, then modern and traditional trade) is a plan, not a completed step. |
| 9 | On sale in October 2026: Yuzu | Stated limit (follow-up search needed; section 3.3). Record 69 reads did not find it on sale. |
| 9 | On sale: Melon | Six-month summer edition reported April 2025. Not expected on sale. Stated limit. |
| 10 | Sales statements after 2022 | Stated limit. The 2021 volume of 28 million litres is press with no named source. The 2021 value of THB 1,357 million has no year printed in the saved text and equals volume times THB 16; the Positioning value of THB 1,450 million differs by 6.9 per cent. Neither is an audited sales figure. |
| 11 | Plant that fills the can or a co-packer | Stated limit. No source names it. |
| 12 | Plant capacities | Bang Len 925 million litres (S, undated, beer plant); Thai Beverage Can 3,880 million cans (P, third party). Stated limit for a can line at a Boon Rawd site. |
| 13 | Canning line speed; pouch or sachet line speed | Stated limit (follow-up search needed; section 3.3). No can line speed is published for any Boon Rawd site. The only printed speed is a PET water line at 72,000 bottles an hour (S). Pouch speeds in this record are ASSUMPTIONS. |
| 14 | Group revenue and net profit 2021 to 2025 | 2021 from Thaiger (S). 2024 and 2025 from MGR Online (S): the article prints the year 2568 in the same sentence for revenue and net profit; no source named. 2022 and 2023: stated limit. DBD statements behind a login: stated limit. |
| 15 | Segment split | Stated limit. |
| 16 | Listing status | Not listed on the evidence read (record 69 row 16). |
| 17 | Can cost and margin inputs | Aluminium price: stated limit (section 3.1). BOT and Gazette: section 3.1. Sheet mass: ASSUMPTION. Regional premium, scrap credit and lids: stated limit. |
| 18 | Distributor margin | Stated limit (follow-up search needed; section 3.3). The 10 to 20 per cent band is an UNSOURCED ASSUMPTION and is marked as such in slide 4. |
| 19 | 7-Eleven operator margin (CP ALL gross margin for beverages or all categories) | Stated limit (follow-up search needed; section 3.3). Only group proxies (section 2.6) are used. CP ALL's annual report (P) is the first source to read. |
| 20 | Yuzu, distributor margin, line speeds, and the CP ALL margin | Four WebSearch calls were attempted on 20 October 2026 and each returned the notice that this turn's web search budget is used up. None ran. Stated limits with the follow-up route in section 3.3. |
| 21 | Company launch releases | Stated limit. The company news page returned empty content. |

### 3.3 Status of the four open searches (follow-up route)

- **Yuzu on sale (October 2026):** not searched; budget used up. Follow-up: one standard search for the Singha Yuzu listing; open any retailer page found before citing it. Until then, a stated limit.
- **Thai distributor margin (beverage):** not searched; budget used up. Follow-up: a dated distributor margin from a filing or channel table. Until then, the 10 to 20 per cent band is an UNSOURCED ASSUMPTION and is labelled so on slide 4.
- **Canning line speed and pouch or sachet line speed:** not searched; budget used up. Follow-up: an equipment maker's published speed for a can line and for a dry-solids or sachet line. Until then, the 20 to 120 pouch speed range is an ASSUMPTION.
- **7-Eleven operator margin (CP ALL):** not searched; budget used up. Follow-up: CP ALL's annual report (P) gross margin for beverages or all categories. Until then, the group proxy (median of three, 21.6 per cent) is used and labelled a PROXY.

The follow-up is a further search turn; this record does not claim those figures.

---

## 4. Cross-check gaps

1. **Volume.** The top-down (119 million, modal central; 83 to 137 million) and the bottom-up (51 million; 26 to 91 million) differ by a factor of about 2.3. The 90 per cent ranges overlap from 83 to 91 million. The bottom-up rests on three assumptions (stocking share, cans a store a day, channel share), none sourced. The top-down rests on a 2022 share with an unresolved measurement year, a market basis that is not stated, and a mixed-window market value. The top-down is the reported central because it uses sourced anchors; the bottom-up is the lower check and gives no directional evidence on its own.
2. **Price.** Top-down cans move from 96.8 million at THB 17.00 to 121.5 million at THB 13.54. The promotional reading moves the top-down by about 7 per cent (112.6 million undiscounted). Top-down revenue does not move (section 2.1).
3. **Market basis.** Retail or manufacturer value is not stated for any of the five values. A manufacturer basis would lower the top-down cans and the retail value.
4. **2021 press values.** The volume (28 million litres) and the value (THB 1,357 million, no year printed in the saved text) are press figures. The value equals the volume times THB 16 to within 0.04 per cent, so it may be derived rather than a sales figure. Positioning's THB 1,450 million differs by 6.9 per cent.
5. **Share.** 1,450 million is 2.31 per cent of 62,725 million; the article prints 2.4 per cent. The 12 per cent in the same article does not reconcile.
6. **Liquid cost.** Built on a sugar proxy. The Lemon Soda uses a sugar-free sweetener system, not sugar. No sweetener cost is sourced. The liquid line is small (about THB 0.9 to 1.3 a can at the FX range).
7. **Group nameplate.** 1,000 million litres (proxy) against the Bang Len plant's 925 million litres (S, undated). The group figure may be site-scope.
8. **Singha Corporation.** Revenue and net profit are press figures with no named source. Net profit is 79 per cent of revenue, which suggests a holding-level or dividend basis. The can's share of either figure is conditional on the booking entity.
9. **Excise.** Applied to the invoice in the chain. The submission (05) excludes excise from its can cost (line 128). The figures in this record are net of excise, so the two are not comparable without a note.
10. **Trade margin.** The retailer margin is a group all-category gross margin and the distributor margin is an unsourced assumption. Together they give 62 per cent of the listing price for the invoice. The submission's 60 per cent of shelf is within two points.
11. **Peer margins.** They include fixed production cost and are on sales of goods. The can's 56 per cent is variable only. The gap is a basis difference, not an efficiency finding.
12. **Co-packer.** The submission cites a minimum of 500,000. The page prints 500,000 to 1,500,000 per SKU and formula. The lower bound is confirmed; the upper bound is new. The page's own pilot wording conflicts with its no-pilot statement.
13. **Cube and can gap.** At the planning price of THB 15 the cube contribution is THB 0.18 below the can's before aluminium. At the can's listing price it is THB 0.82 below. Both depend on the cube's unpriced binder and flavour, which would lower the cube contribution further.
14. **Retailer margin for 7-Eleven.** The group proxy is used (median of three group values). The 7-Eleven operator margin is a stated limit (section 3.3).
15. **Independence.** Estimates 3a, 5a and 6a have no independent second derivation from sources; the gaps are stated in section 1 and section 5.

---

## 5. Limits (what would settle each)

| Limit | What would settle it |
|---|---|
| Aluminium price (LME) | An authorised route for an LME settlement or a dated aluminium price. The LME page returned HTTP 403 on 20 October 2026. Not used. |
| Bank of Thailand rate, re-verified | A dated BOT rate table that renders. Today's page prints no table. |
| Excise ad valorem base, second-reader check and amendments | The Royal Gazette PDF (HTTP 403 today), a second reader of the Thai numerals of the saved text, and a search for later amendments. The 14 per cent is P as saved, read from page images. |
| Distributor margin (open) | A dated Thai beverage distributor margin from a filing or a channel table. Follow-up search (section 3.3). Labelled an UNSOURCED ASSUMPTION in slide text. |
| Retailer margin for 7-Eleven (open) | The CP ALL annual report (P) gross margin, or a dated channel table. Follow-up search (section 3.3). |
| Sheet mass per can | A can maker's published spec for a 330 mL can. |
| Line speed: can and pouch or sachet (open) | An equipment maker's published speed for a dry-solids or sachet line, and for a can line. Follow-up search (section 3.3). |
| Co-packer line capacity, fee and pilot wording | A quote or a company statement. Outside contact is not used in this project. |
| Yuzu on sale (open); Melon | A listing that renders on a retailer page. Follow-up search (section 3.3) for Yuzu. |
| Makro six-can one-pack price | A dated product page that labels the one-pack price. |
| Promotion status and price ladder | A dated, non-promotional 24-can listing at each retailer. Record 68d section 2 and the 7-Eleven rule need reconciling (section 6). |
| Outlets carrying the can; modern against traditional trade split | A distributor count, or an outlet panel. |
| Booking entity of the can; Singha Corporation revenue and profit for 2022, 2023 and the 2025 primary check | DBD statements for the registration (behind a login), or a filing. |
| Plant that fills the can | A company statement or a factory licence entry. |
| Sweetener cost in the liquid line | A supplier price for the sweeteners, dated. |
| Market value basis (retail or manufacturer) | The NielsenIQ or Kantar method note, or a dated press value that states the basis. |
| Current share of Lemon Soda; measurement year of the 2.4 per cent share | A dated share figure for 2024 to 2026, or the measurement year printed in a primary source. |
| Independent second derivation for the non-aluminium cost (3a), the cannibalisation share (6a), and the line-time versus count-basis capacity (5a) | A source for a second cost build (for example a can maker's published cost or price), a survey of cube buyers' prior can use, and a published line speed. None found. |
| Cannibalisation share (what share of cube buyers are existing can buyers) | A consumer test of the cube (the pilot), since no source covers it. |
| Capacity interval for the group nameplate | The scope of the 1,000 million litres (site or group) from a company statement. The count-basis percentage has no interval until then. |
| Co-packer MOQ "per SKU" or "per product" wording on the FAQ | The company's written terms (outside contact not used). |

---

## 6. Conflicts with the current deck and submission text (for the lead; not judge-facing)

Nothing in `rework/deck/`, `rework/submission/` or `rework/proposal/` was edited (rule 6). The conflicts below are for the lead to apply. Line numbers were confirmed on 20 October 2026.

1. **THB 4.94 can cost (3.73 to 6.14), superseded.** It appears in: `deck/deck_content.md` slide 9 (lines 133 and 135 only; line 136 does not carry it); `submission/05` (lines 116, 122 and 126); `submission/11` (lines 78, 136 and 194); `proposal/05` (lines 116, 122 and 126); `proposal/11` (lines 78, 136 and 194); `rework/61` (line 107). The figure includes sheet metal at the 19 October saved LME reading, which is not authorised. Replace with THB 3.27 (2.62 to 3.92) excluding aluminium, the aluminium slope of THB 0.055 a can per USD 100 a tonne, and the break-even of about USD 7,500 a tonne. `rework/screen/can_cost_model_results.json` has been overwritten with the updated results; the 4.94 is kept there as a superseded note.
2. **Chart.** `rework/charts/can_cost_per_unit.png` (19 October 2026) was drawn from the LME-based model. It is stale. The replacement is `rework/screen/can_cost_non_aluminium.png` (from `can_cost_model.py --chart`, run on 20 October 2026). The lead should replace the stale chart or remove it from any slide that uses it.
3. **Co-packer minimum.** `submission/11` lines 135 and 269, and `proposal/11` lines 135 and 269, print a minimum of 500,000 units per SKU. Line 193 names the co-packers without a minimum and is not a conflict. Replace with "500,000 to 1,500,000 units per SKU and formula, phased within 12 months" (co-packer's own terms, read 20 October 2026). The 2.5 years at 200,000 cubes stays correct at the lower bound; 7.5 years at the upper bound should be added.
4. **Excise.** `submission/05` line 128 excludes "excise on sugar-sweetened drinks" from the can cost. `submission/10` line 177 states "the price model excludes excise". `submission/10` line 22 gives the excise bands (four sugar bands with 14 per cent ad valorem) and says the base is not read. The new figures are net of the 14 per cent excise, applied on an assumed base. The three statements should give the same basis: either the net-of-excise figure is used, or the basis is stated. The 14 per cent is P as saved, read from page images, with a second-reader check and amendments outstanding.
5. **Shelf price and dates.** `submission/02` line 19 says "Prices are online retailer listings read on 18 and 19 October 2026, not shelf prices." The Singha Lemon Soda listings used here were read on 20 October 2026. The date should be corrected; the "not shelf prices" wording is correct and should be kept.
6. **THB 17 described as a shelf price.** Any deck or submission line that calls the THB 17 a shelf price should say "online list price at Lotus's, single can".
7. **Market value window.** Any text that presents "THB 70,000 million" or "2025" for the market should cite the mixed windows in section 2.5 (record 67). The 76,900 is a forecast.
8. **Share anchor year.** Any text that dates the 2.4 per cent share to 2022 should say the share is from a 4 July 2022 article, whose market value is for 2021, and that the measurement year is 2021 or 2022. The 12 per cent in the same article is not reconciled and should not be quoted.
9. **Cannibalisation statement.** Any text that says "a cube earns about THB 1.9 less per unit than a can before aluminium" (from the earlier draft) is withdrawn. The gap is THB 0.18 at the planning price and THB 0.82 at the can's listing price, both before aluminium and with binder and flavour unpriced.
10. **Singha Corporation share.** None of the submission text gives a share. If the slide 4 text in section 7.1 is used, it must carry the "not Singha figures" note and the booking-entity limit.
11. **Record 69 section 8 Card 2** says "THB 13.5 a can at the member price" and "THB 14.2 for non-members". Those are Lotus's six-can figures. Unchanged.
12. **Thai Beverage Can source line.** The earlier slide 9 source line cited the TBC filing for the cost model. It is removed; TBC is cited only for the capacity and utilisation figures.
13. **Promotion and the record 68d rule.** Record 68d section 2 says promotion prices are not used, but its 7-Eleven rule reads the lower price as the selling price where the saving equals the difference and the badge is a discount; that rule was applied to D01 and D02. Record 68d and this record must be reconciled by the lead. This record keeps the promotional reading in the central and discloses it (section 2.1).
14. **Deck slide 4 note bar.** `deck/deck_content.md` line 57 says line capacity and the can's unit cost are "not yet verified". The estimates in section 7.1 now give both as derived estimates (not Singha figures). The note bar should be revised to match.
15. **Deck slide 9 title and exhibit.** `deck/deck_content.md` lines 133 and 135 print THB 4.94 and the legend "floor THB 4.94". Replace with the section 7.2 figures.
16. **Records 61 and 69 1,357 million figure.** Record 69 labels THB 1,357 million (press, 2021) as a 2021 value. The saved text prints no year and the value equals the press volume times THB 16. Record 69 should carry that qualification.
17. **CP ALL capture.** `rework/raw/captures_2026-10-19/07_cpall-7eleven-stores-ye2025.md` says no publication date is printed. The live page prints "Published on 24/03/2026" (read 20 October 2026). The capture's date line should be corrected; that file is outside this task's outputs and was not edited.

---

## 7. Proposed text (plain sentences; no dashes; no internal notes; nothing handed to Singha Corporation)

### 7.1 Slide 4, Singha side

**Estimates derived from public data; not Singha figures.**

Singha does not publish the Lemon Soda volume, price structure, cost, plant capacity or cube plan. The figures below are estimates built from public sources. Each range is the middle 90 per cent of a calculation over stated input bounds, several of which are assumptions. The ranges are not statistical confidence intervals.

- Volume: about 119 million Lemon Soda cans a year on a top-down estimate (90 per cent range 83 to 137 million). The median of the calculation is 111 million, because the price input is skewed. The estimate divides a carbonated soft-drink market of about THB 70,000 million by a listing price of about THB 13.80 a can, and applies a share of about 2.35 per cent from a 2022 trade press article. That article measures the share in 2021 or 2022, and its market value is for 2021. The market value mixes press values for 2024 and 2025, one of them a forecast, so the central is not a 2025 actual. The listing price is the average of four online prices, one of which is a promotional price at one retailer; at its undiscounted price the top-down estimate would be about 113 million. A bottom-up store count gives about 51 million (26 to 91 million); that count depends on three assumed inputs.
- Revenue: about THB 880 million a year to the producer (650 to 1,060 million), after VAT, retail and distributor margins and a 14 per cent excise on an assumed base. The distributor margin is an unsourced assumption of 10 to 20 per cent. The retail value is about THB 1,650 million. The company that books these sales is not known. If Singha Corporation booked them, the can would be about 23 per cent of its 2025 revenue as reported in the press (17 to 27 per cent). The press report names no source.
- Price chain: a listing price of about THB 13.80 a can, the average of four online prices, leaves about THB 8.60 a can before excise and about THB 7.39 after it. The single can lists online at Lotus's at THB 17 (an online list price, read 20 October 2026; not a store shelf price). Variable cost excluding aluminium is about THB 3.3 a can (2.6 to 3.9). Aluminium is not included: each USD 100 a tonne adds about THB 0.06 a can. Before aluminium, the can's contribution would reach zero at an aluminium price of about USD 7,500 a tonne.
- Margin: the variable margin before aluminium is about 56 per cent (47 to 67 per cent). Thai bottlers' gross margins, derived from their filings, are 29 to 42 per cent. Those margins include fixed production cost, so the two are not comparable.
- Capacity: no pouch, sachet or dry-solids line is evidenced at any group company. At 60 pouches a minute with 70 per cent efficiency, both assumptions, 200,000 cubes a year need about 79 hours of line time (about 2 per cent of a 4,000-hour year), and 1,000,000 cubes need about 397 hours (about 10 per cent). The 90 per cent range for 200,000 cubes is 45 to 152 hours. A co-packer's minimum run is 500,000 to 1,500,000 units per product and formula, so the minimum run, not line time, is the binding constraint. At 200,000 cubes a year, filling the minimum takes 2.5 to 7.5 years.
- Cannibalisation: if 25 or 50 per cent of cube buyers were can buyers, the can contribution given up would be at most about THB 206,000 or 413,000 a year at 200,000 cubes, before aluminium (90 per cent ranges of 169,000 to 284,000 and 339,000 to 567,000). After the cube's own contribution, the central net change is a loss of about THB 9,000 or 18,000 a year at the planning price of THB 15 a cube, and about THB 41,000 or 82,000 if the cube sold at the can's listing price of THB 13.80. Within the stated ranges the net change can be positive. The comparison turns on the aluminium price, which is not confirmed from a source. The cube cost excludes binder and flavour, which are not yet priced.
- Pilot fixed cost: THB 500,000 a year is covered about 1.6 times at 200,000 cubes and about 0.4 times at 50,000 cubes, at the planning price after excise. Steady-state break-even is about 127,000 cubes a year (90 per cent range 114,000 to 159,000). If the cube sold at the can's listing price, break-even would be about 151,000 cubes a year. The pilot would test listings, repeat purchase and the rate at which can buyers switch before any scale-up.

Source line: retailer listings for Singha Lemon Soda on Lotus's, 7-Eleven ALL Online and Makro PRO, read 20 October 2026; carbonated soft-drink market values in Thai press, 2024 to 2025; Positioning, 4 July 2022; press report on Singha Corporation 2025 results (MGR Online, 23 May 2026); CP ALL store count at the end of 2025 (published 24 March 2026); Revenue Department VAT notice (2026); Royal Gazette excise notice (B.E. 2560); Bank of Thailand rate of 15 October 2026; peer filings and reports (The Coca-Cola Company, PepsiCo, ThaiNamthip, Haad Thip, Sermsuk, Thai Beverage, Osotspa); co-packer web page, read 20 October 2026. Estimates; not Singha figures.

### 7.2 Slide 9, can cost

Variable cost of a 330 mL can, excluding aluminium, is about THB 3.3 (90 per cent range THB 2.6 to 3.9). It is built from public inputs, several of which are proxies or assumptions. Aluminium is not included: each USD 100 a tonne adds about THB 0.06 a can. At a listing price of about THB 13.80 a can, which gives net revenue of THB 7.39 after VAT, margins and excise, contribution before aluminium reaches zero at an aluminium price of about USD 7,500 a tonne.

Cost per can with fixed cost, excluding aluminium (THB a can):

| Cans a year | No fixed cost | THB 300 million fixed | THB 600 million fixed |
|---|---|---|---|
| 500 million | 3.27 | 3.87 | 4.47 |
| 1,000 million | 3.27 | 3.57 | 3.87 |
| 1,676 million (group nameplate, a proxy at 100 per cent use) | 3.27 | 3.45 | 3.62 |

Source line: desk model from public inputs: a US 2024 non-metal can conversion cost (a proxy for a Thai line); filling and seaming consumables and carbon dioxide from public trade and vendor sources (assumptions and proxies); a liquid line built on a sugar proxy (an assumption, since the sweetener cost is not sourced); and the Bank of Thailand rate of 15 October 2026. Sheet mass and the fixed-cost scenarios are assumptions. The 1,676 million cans figure is a proxy for group capacity. Not Singha figures.

---

## 8. Sources

Anchors used (saved files already in the repo):

- Market and share: `rework/67_market_size_source_check.md`; `rework/raw/diligence_2026-10-20/T1/` (press extracts); `rework/raw/diligence_2026-10-20/T6/09_verbatim_key_passages_second_read.md` section C (2022 Positioning passages); the T7 save `positioning_2022_07_04_csd_share.md` (WebFetch, 20 October 2026).
- Price: Lotus's, 7-Eleven ALL Online and Makro PRO listings, read 20 October 2026, as recorded in `rework/68d_lemon_soda_price_ladder.md` (rows D01, D06, D12, D13, S01, D02, D07), with the saved reads `rework/raw/diligence_2026-10-20/T6/13_retail_listings_read_2026-10-20.md` and `T6/04_retail_listings_2026-10-20.md`. The 7-Eleven promotion check: `T7/7eleven_d01_promotion_check_2026-10-20.md`. Record 68e section 1 (category multipack median THB 13.75).
- Retailer margins (S, aggregator): `rework/raw/diligence_2026-10-20/T4/retail_groups_financials_stockanalysis_2026-10-20.md`.
- VAT (P): `rework/raw/diligence_2026-10-20/T9/rd_vat_7_percent_2026.md`.
- Excise (P as saved, read from page images): `rework/raw/gazette_sugar_drink_excise_primary_2560_A095_111.md`.
- Thai Beverage Can (P): `rework/raw/diligence_2026-10-20/T6/08_bjc_one_report_2025_tbc_capacity_customers_bigc.md`.
- Singha Corporation press (S): `rework/raw/diligence_2026-10-20/T6/07_group_financials.md`, `T6/09_verbatim_key_passages_second_read.md`.
- Boon Rawd plants (S, company pages): `rework/raw/diligence_2026-10-20/T6/15_production_plants_and_reach_read_2026-10-20.md`.
- Peer gross margins: record 68a (`T2/`), record 68b (`T3/`), record 68c (`T4/`).
- CP ALL stores (P): `rework/raw/captures_2026-10-19/07_cpall-7eleven-stores-ye2025.md` (summary; date corrected by the T7 check below).
- Cube specification and model inputs (team, records 64, 72, submission 05): not external sources.

Reads and rechecks made in this turn (WebFetch of named URLs, 20 October 2026; no browser):

- 7-Eleven ALL Online, D01 (promotion): `rework/raw/diligence_2026-10-20/T7/7eleven_d01_promotion_check_2026-10-20.md`.
- CP ALL YE68 snapshot (publication date and scope): `rework/raw/diligence_2026-10-20/T7/cpall_ye68_publication_date_check_2026-10-20.md`.
- Makro PRO product 02emhsl: `rework/raw/diligence_2026-10-20/T7/makro_02emhsl_one_pack_recheck_2026-10-20.md`.
- Arnifo OEM page (both reads, with the pilot wording): `rework/raw/diligence_2026-10-20/T7/arnifo_oem_moq_recheck_2026-10-20.md`.
- BOT, LME and Royal Gazette (blocked or no table): `rework/raw/diligence_2026-10-20/T7/bot_and_lme_and_gazette_rechecks_2026-10-20.md`.
- Positioning, 4 July 2022: `rework/raw/diligence_2026-10-20/T7/positioning_2022_07_04_csd_share.md`.

---

## 9. Files

Written or revised in this task:

- `rework/70_singha_internal_estimates.md` (this record).
- `rework/screen/singha_internal_estimates.py` (script; seed 20261020; 200,000 draws; listing-price basis with promotion sensitivities; draws for headroom, co-packer years and at-risk values).
- `rework/screen/singha_internal_estimates_results.json` (results; self-checks pass; includes `slide4_numbers`, `price_cases` and `slide9_can_cost`).
- `rework/screen/can_cost_model.py` (updated: listing-price labels; chart beside the central variable cost).
- `rework/screen/can_cost_model_results.json` (rerun; the 4.94 is kept as a superseded note).
- `rework/screen/can_cost_non_aluminium.png` (new chart, from `can_cost_model.py --chart`).
- `rework/raw/diligence_2026-10-20/T7/7eleven_d01_promotion_check_2026-10-20.md` (new).
- `rework/raw/diligence_2026-10-20/T7/cpall_ye68_publication_date_check_2026-10-20.md` (new).
- `rework/raw/diligence_2026-10-20/T7/arnifo_oem_moq_recheck_2026-10-20.md` (tier aligned; pilot conflict added).
- `rework/raw/diligence_2026-10-20/T7/positioning_2022_07_04_csd_share.md` (measurement year stated as unresolved).
- `rework/raw/diligence_2026-10-20/T7/makro_02emhsl_one_pack_recheck_2026-10-20.md`, `bot_and_lme_and_gazette_rechecks_2026-10-20.md` (unchanged).

Not edited: `rework/submission/`, `rework/proposal/`, `rework/deck/`, `rework/README.md` (index, for the lead), `rework/charts/` (stale chart noted in section 6), `rework/raw/captures_2026-10-19/` (CP ALL date line noted in section 6). Nothing committed or pushed.
