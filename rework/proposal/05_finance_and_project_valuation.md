# Finance and project valuation: Lime Cube (19 October 2026)

This is a model output for one product, the Lime Cube, sold in domestic Thailand. It is not investment advice.

## Tier key

P: a government or regulator text read in full, a company's own filing, official statistics, a peer-reviewed article read in full, or a primary database. S: any other source, including press, trade portals, consultancy pages, company web pages that are not filings, handbooks reproduced online, and search snippets. SOURCED: the page text is saved in rework/raw and was read; this is the repository rule. UNVERIFIED: the page was not saved, or only a snippet or summary was read; a figure stays UNVERIFIED until its page is saved. DERIVED: our arithmetic, with the inputs and their tiers shown. PROXY: a stand-in for what is not measured. ASSUMPTION: a value chosen for the model, not sourced.

## Scope: the project, not the group

- One product in domestic Thailand; no group financials, volumes or cost bases are used.
- The central claim is a new consumption form, a dissolvable lime cube. It is unpriced; no price response is measured.
- Sucralose is recommended, not yet chosen; its Thai permission, also needed for potassium bicarbonate, is open and blocks sale.
- The design dose is 0.9 volume of CO2 per 330 mL, under review; the alternative is 0.55 volume. Each has its own gate:
  - 0.9 volume: at least 0.6 volume dissolved at 10 minutes, at serves of 30 °C or below (ASSUMPTION for the gate value).
  - 0.55 volume: gate not set; to be defined by R&D.
  - CO2 solubility is 0.655 volume at 30 °C and 0.592 at 35 °C (S, UNVERIFIED; handbook table, Lange-attributed), both below the 0.9 dose.
- Method: pre-tax, five-year horizon, no terminal value, discount rate 8% to 12% (ASSUMPTION; base 10%).

## Unit economics: 0.9 volume per 330 mL (under review)

Per cube, 12-cube carton, target pH 3.5. The 0.55 column shows cost totals only.

| Line (THB per cube) | 0.9 volume | 0.55 volume | Tier and status |
|---|---|---|---|
| Potassium bicarbonate, 1.33 g | 0.05 | not split | P, PROXY; UNVERIFIED |
| Citric acid, 3.42 g at pH 3.5 | 0.11 | not split | P, PROXY; UNVERIFIED |
| Sucralose, 33 mg | 0.02 | not split | S; UNVERIFIED |
| Pouch, 90 x 70 mm | 1.30 | not split | S, PROXY; UNVERIFIED; chosen base (ASSUMPTION) |
| Print | 1.50 | not split | ASSUMPTION (placeholder) |
| Processing | 0.50 | not split | ASSUMPTION |
| Carton, 5 THB per 12 cubes | 0.42 | not split | S; UNVERIFIED |
| Cost per cube | 3.90 | 3.83 to 3.87 | DERIVED |
| Shelf price | 15.00 | 15.00 | ASSUMPTION; Tops cans at 16 and 17 THB, both out of stock (S, SOURCED; source 2) |
| Ex-factory, 60% of shelf | 9.00 | 9.00 | ASSUMPTION; cross-check 59.5% |
| Contribution | 5.10 (56.7%) | 5.13 to 5.17 | DERIVED |

Cost per cube is 3.90 THB, the sum of the rows above; contribution is 9.00 less 3.90 (DERIVED). The 0.55 cost is 0.03 to 0.07 THB lower (DERIVED; the range depends on whether the citric excess, set by pH, scales with dose).

Reactants total 0.18 THB. A 15 THB serve of 330 ml (about 45 THB per litre, DERIVED) sits inside the 26 to 86 THB mass-market band for zero-sugar and plain sparkling drinks (S, UNVERIFIED; source 3).

Contribution by pack: 5.52 single pouch (no carton; this flatters), 4.85 six, 5.10 twelve, 5.15 twenty-four. The six- and 24-cube results rest on ASSUMPTION carton prices of about 4 THB and 9 THB. One cube per pouch is inferred, not confirmed with the organiser.

About 128,600 cubes fit in a 20 ft container for 6-, 12- or 24-cube cartons (DERIVED: 33.2 m3 internal volume (S, SeaCube specification), 92% packing (ASSUMPTION), 0.00285 m3 per 12-cube carton).

## Volume scenarios

No volume basis exists; the acquisition inputs give costs, not sales. Scenarios (ASSUMPTION) are 50,000 (low), 200,000 (base) and 1,000,000 (high) cubes per year, with year 1 at 50%.

## Project cash flows and valuation

Year t cash flow is 5.10 times volume times the ramp, minus fixed cost F; year 0 outlay equals F (ASSUMPTION convention). NPV at 10% is DERIVED from the contribution and ASSUMPTION volume, ramp, cost and discount inputs. Payback is undiscounted. At 8% and 12%, NPVs lie within about 10%.

| Scenario (cubes per year) | F = 250,000 | F = 500,000 | F = 1,000,000 | F = 2,000,000 | Max F (NPV at or above 0) |
|---|---|---|---|---|---|
| Low (50,000) | -347,000; beyond 5 yr | -1,545,000; beyond 5 yr | -3,940,000; beyond 5 yr | -8,731,000; beyond 5 yr | 178,000 |
| Base (200,000) | +2,205,000; 0.96 yr | +1,008,000; 1.94 yr | -1,388,000; beyond 5 yr | -6,179,000; beyond 5 yr | 710,000 |
| High (1,000,000) | +15,817,000; 0.11 yr | +14,619,000; 0.24 yr | +12,224,000; 0.65 yr | +7,433,000; 1.47 yr | 3,552,000 |

## Break-even

Cubes per year at which NPV is zero (DERIVED from the same inputs).

| Annual fixed cost (THB) | NPV zero at 8% | NPV zero at 10% | NPV zero at 12% |
|---|---|---|---|
| 250,000 | 69,337 | 70,391 | 71,469 |
| 500,000 | 138,673 | 140,783 | 142,938 |
| 1,000,000 | 277,346 | 281,565 | 285,876 |
| 2,000,000 | 554,693 | 563,131 | 571,753 |

## Sensitivities

One change at a time; maximum fixed cost for NPV at or above zero at base volume and 10% (DERIVED: 0.6964 x contribution x volume).

| Change | Contribution (THB) | Max F (THB per year) | Status |
|---|---|---|---|
| Base | 5.10 | 710,000 | DERIVED |
| Shelf 10 / 20 THB | 2.10 / 8.10 | 292,000 / 1,128,000 | ASSUMPTION |
| Ex-factory share 50% / 70% | 3.60 / 6.60 | 501,000 / 919,000 | ASSUMPTION |
| Pouch 0.67 / 2.70 THB (range) | 5.73 / 3.70 | 798,000 / 515,000 | UNVERIFIED |
| Pouch 3.00 THB (stress case only) | 3.40 | 474,000 | DERIVED |
| Print 0.80 / 2.50 THB | 5.80 / 4.10 | 808,000 / 571,000 | ASSUMPTION |
| Processing 0.25 / 1.00 THB | 5.35 / 4.60 | 745,000 / 641,000 | ASSUMPTION |
| Dose 0.55, cost only (range of savings) | 5.13 to 5.17 | 714,000 to 720,000 | DERIVED; gate not set |
| Excise 14% on assumed ex-factory base | 3.84 | 535,000 | Rate SOURCED; base UNVERIFIED |

Outside the cash flows, customer acquisition at 1,150 THB per first purchase (DERIVED: 11.5 THB paid-social click cost, PROXY, at a 1.0% click-to-purchase rate, ASSUMPTION; UNVERIFIED) needs about 225 cubes per customer at 5.10 THB each, so paid social alone does not pay back.

## Limits

- The 1.30 THB pouch base is a chosen value (ASSUMPTION), near the midpoint of USD 0.03 to 0.05 per piece from a non-Thai listing (THB 1.01 to 1.68 at the Bank of Thailand mid-rate of 33.55 THB per USD; DERIVED). The 0.67 to 2.70 THB range rests on unverified supplier snippets; 3.00 THB is a stress case only. No Thai pouch or print quote exists.
- Fixed costs, tooling, registration, trademark, pouch minimums and marketing are unsourced; the grid covers them.
- Excise: the 14% rate is sourced (P, SOURCED); its value base was not read, later amendments were not searched, and its application to a dissolvable cube is unconfirmed.
- VAT, freight, cold chain and income tax are excluded; no depreciation, working capital or terminal value is modelled.
- Inputs without a URL stay UNVERIFIED: the carton price, sucralose listing, non-Thai pouch listing, UN Comtrade values (no query URL), and print and processing placeholders. Input prices are bulk import unit values and listings, not Thai trade prices.
- One cube per pouch is unconfirmed with the organiser. No supplier quote has been obtained and no outside contact has been made. Break-even figures assume the sweetener permission is granted.

## Sources

1. Royal Gazette 2560 (2017), excise schedule, item 02.02 (P; SOURCED): https://www.ratchakitcha.soc.go.th/DATA/PDF/2560/A/095/111.PDF
2. Tops Online single-can listings, 18 October 2026 (S; SOURCED; both out of stock at capture): https://www.tops.co.th/en/sprite-soft-drink-zero-sugar-lemon-lime-flavour-325ml-8851959132395 (16 THB); https://www.tops.co.th/en/schweppes-soda-water-330cc-8851959132647 (17 THB)
3. Retailer listing audit, 18 October 2026 (S; UNVERIFIED; not every row saved).
4. UN Comtrade import unit values, HS 2836.40, 2918.14 and 2932.14 (P; PROXY; UNVERIFIED; no query URL given).
5. Retail asking prices for the carton and sucralose, and a non-Thai pouch listing (S; UNVERIFIED; no URL given).
6. Facebook ad costs, Thailand 2025, Phoenix Media (S; PROXY; UNVERIFIED): https://www.phoenixmedia.co.th/the-costs-of-facebook-google-and-line-ads-in-thailand-for-2025/
7. Bank of Thailand, average USD buying and selling rates, 15 October 2026 (P; SOURCED; midpoint 33.55 THB per USD): https://www.bot.or.th/en/statistics/exchange-rate.html

## Team-only traceability (delete before submission)

- Design and masses: rework/63 section 1 item 4 (citric 3.42 g at pH 3.5 and 5.97 g at pH 3.0; free excess set by target pH) and section 2 (bicarbonate 1.33 g; stoichiometric citric 0.85 g). The 0.9-volume basis is decision D10, now under review. A superseded earlier design mass is not used.
- Dose: rework/63 section 1 items 1, 2 and 6, and section 9. Solubility: rework/63 section 1 items 1 and 2; rework/06 pre-launch gates. The decision record calls the table sourced, but no saved page or URL was found in the record, so it is UNVERIFIED here.
- Gates: 0.6 volume threshold in rework/06 (dose and effervescence row). The 0.55 gate is "gate not set; to be defined by R&D" (no value in the record). Gate G6 (sweetener and potassium bicarbonate permission, sale-blocking): rework/63 section 8. Sucralose recommended, not chosen: rework/52 D13.
- Pouch: range USD 0.02 to 0.08 and THB 0.67 to 2.70 from rework/63 (pouch row, section 7.1); chosen base 1.30 THB (decision (d), 19 October 2026); stress case 3.00 THB from rework/63 section 7.4.
- Unit costs: rework/63 section 7.1 (inputs and ranges), 7.2 (cost per cube 3.90; pack costs 3.48, 4.15, 3.90 and 3.85), 7.3 (container counts 128,586, 128,580 and 128,568 cubes; carton sizes for 6 and 24 are ASSUMPTION), 7.4 (pH 3.0).
- Exchange rate: screen/pack_economics.py (FX_THB_PER_USD, midpoint of 33.3535 and 33.7455); raw/bot_fx_primary_2026-10-15.md.
- Shelf cans: raw/browser_captures_2026-10-18.md items 1 and 2; rework/04 browser table. The 26 to 86 band is in rework/04 (mass-market row) and raw/wiawiyd7e_price_audit.json.
- Excise: raw/gazette_sugar_drink_excise_primary_2560_A095_111.md.
- Valuation: screen/project_valuation.py (0.55 sensitivity near line 319, reactants scaled linearly) and screen/project_valuation_results.json. Base NPVs, break-even and maximum F were re-derived and agree within rounding. Also in the results file and not in the body: the simple break-even column (F / 5.10: 49,020; 98,039; 196,078; 392,157), the single-pouch (5.52, 769,000) and 24-cube carton (5.15, 717,000) rows, the target pH 3.0 row (5.02, 699,000), the carton 3 / 7 THB row (5.27 / 4.93; 734,000 / 687,000), the 699,000 to 721,000 range at 8% to 12%, and the combined pouch, print, carton and processing bounds (6.85 / 2.03; 954,000 / 283,000).
- Customer acquisition: rework/55 (cost per click 11.5 THB, PROXY; landing-page rate 1.0%, ASSUMPTION; 1,150 THB per first purchase); value-chain record rework/53 (59.5% cross-check).
- Container: rework/63 section 7.3 (internal dimensions and counts; 92% packing at line 142); carton volume 0.00285 m3 from rework/screen/pack_economics_results.json.
- Body edits in the 19 October 2026 fix pass: gate G1 and G6 labels, the team-only status line, the corporate and international scope sentence, the export-study KPI reference, the registration and submission line, and the consumer synthesis label were removed. The volume table, the simple break-even column, and the single-pouch, 24-cube, pH 3.0, carton 3 / 7 and combined-bound rows, and the read-across line, were moved to this appendix to meet the word limit.
- Not settled: (1) the top of the pouch range: USD 0.08 at 33.55 gives 2.68 THB, not 2.70; decision (d) keeps 2.70 until the rate used is confirmed. (2) A saved page or URL for the solubility table. (3) URLs for the carton, sucralose and pouch listings. (4) A query URL for the Comtrade values. (5) The Tier key text names rework/raw and the repository rule, which the body rule bars; kept verbatim per the key instruction.
