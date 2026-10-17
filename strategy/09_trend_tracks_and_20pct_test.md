# Trend-driven target tracks and the 20 percent test (2026-10-17)

The C3 route (premium glass, on-premise) is conditional and not validated. The workflow screened four new trend-driven tracks in Singapore and Korea, using the same evidence rules, and a judge scored them.

## Track verdicts

| Track | Judge | Theme fit | Main reason |
|---|---|---|---|
| **A: fibre and gut-health sparkling with no health claim (Singapore lead, Korea later)** | **conditional, recommended** | Strong on themes 1 and 3 | Most launched trend in the set: three Korean fibre sparklers in 2026 and Refresh in Singapore from 22 September 2026. Price evidence is mostly claim-bearing. The fibre threshold is unread |
| D: sparkling botanical tea (jasmine, butterfly pea, roselle, Thai tea), sugar-free | conditional, runner-up | Strong on narrative, moderate on evidence | Singapore regulation is good: the SFA record of views covers butterfly pea, roselle and jasmine. Demand is not measured. Premium floral sparkling competes (Perrier at S$2.06 to 2.56) |
| B: Thai-flavour sparkling | not presentable | Weak | A flavour choice, not a trend. Singha's own citrus lines are the nearest comparators |
| C: electrolyte sparkling | not presentable | Moderate | Hydration wording is not allowed in Singapore. 100PLUS Zero and H-Two-O already sell |

## Recommended track A: product definition (working)

- A zero-sugar sparkling soda in a 330 ml can, Singapore first.
- **Flavour:** apple-ginger, a non-citrus lane. The ginger needs an SFA listing check.
- **Sweetener:** a non-nutritive blend, with sugar under 0.5 g per 100 ml. This grades at most Nutri-Grade B, and the mark is optional for A and B. A sugar-sweetened control is needed in any taste test.
- **Fibre:** soluble fibre from acacia or resistant maltodextrin (the launched SKUs use these). Malt-derived fibre is dropped (`08_malt_fibre_status.md`).
- **Dose:** at or above the confirmed source-of-fibre threshold, with the claim printed (about 5.3 g per 355 ml if the 1.5 g per 100 ml proxy holds); or below it, with no fibre wording on pack.
- **Wording:** "sugar free", the nutrition panel with the fibre figure, and the sweetener declaration. No health, gut, prebiotic, digestive, hydration or "replenish" wording in either market.
- **Price band:** S$2.00 to 2.50 shelf per can plus the S$0.10 BCRS deposit, anchored on the no-claim Perrier flavoured sparkling (S$2.06 to 2.56 per 330 ml). Korea: KRW 1,650 to 2,000 per can, if Korea stays in the comparison.

## The 20 percent test: three readings

The brief's definition is not in the files available to the team. The judge's workaround and our model use different readings, so all three are shown. **The exact wording of the brief's 20 percent test is needed.**

1. **Exporter contribution test (K1 in the model).** Net contribution per can (CIF less exporter cost and 10 percent trade spend) is at least 20 percent of CIF. Result: Singapore needs CIF of at least S$0.489, Korea at least KRW 553 (`strategy/data/price_basis_thresholds.csv`). The customs averages (S$0.478, KRW 528) fall just short.
2. **Channel markup test (judge's gate 1).** After GST or VAT and a 30 percent retailer margin, the price must leave at least 20 percent over the CIF value. Result: shelf of about S$0.93 per 330 ml in Singapore (S$0.87 to 1.01 across the retailer range), or about S$1.17 if a 20 percent importer margin is added. Korea: about KRW 1,040 per 355 ml (10 percent VAT assumed).
3. **Fixed-cost absorption test (judge's gate 2, also our absorption reading).** A 20 percent operating margin after standalone fixed cost, at a stated volume. At 5 million cans, the required CIF is S$0.62 (Singapore) and KRW 696 (Korea). At 10 million cans, it falls to S$0.55 and KRW 624. Track A's volume needs: about 0.56 to 0.82 million cans a year in Singapore at S$2.00 to 2.50 shelf.

The looser reading (price at least 1.25 times CIF) clears every track and does not discriminate, so it is not used.

## Price-basis assumption

The S$0.478 and KRW 528 values are customs averages (Comtrade, CIF convention) across Thai flavoured-water imports. They are what importers pay on average. They are not a premium brand's price, and a premium product probably costs more to land, which lowers every margin. The sweep in `strategy/data/price_basis_sweep.csv` covers the full range.

## Volume is the binding constraint

No scan found any category volume that supports the volumes the 20 percent tests need. Track A needs about 0.56 to 0.82 million cans a year in Singapore. The price evidence for Track A is mostly claim-bearing, so a no-claim product may not earn that price.

## Tests before 22 October (kill criteria)

1. Read the HPB Guide Appendix I for the source-of-fibre and high-fibre thresholds per 100 ml. This decides any fibre wording and the minimum dose.
2. Check whether Refresh's "feeds beneficial bacteria" wording is on the HPB approved lists. If not, the design carries no gut wording.
3. Singapore shelf audit at 7-Eleven, FairPrice, Cold Storage and RedMart: Refresh's price, Olipop, Poppi, Simply Pop and Pepsi Prebiotic Cola presence, current Perrier flavoured prices.
4. Distributor margin: one quote or published range from a Singapore distributor. Rerun the channel test at a 20 percent importer margin (S$1.17 threshold).
5. Blind taste test with thresholds set in advance: sugar-free apple-ginger with fibre, without fibre, and a sugar-sweetened control, against Perrier flavoured and Refresh. Run only if about 40 target-age Singapore adults can be reached.
6. Nutri-Grade calculation on the final recipe.
7. Legal check on the ginger rhizome (SFA botanicals list) and the sweetener caps (steviol glycosides and sucralose).

## What this cannot show

- Realised prices or sell-through for any fibre or botanical sparkling in Singapore or Korea. Refresh has been on sale only since 22 September 2026.
- Whether Singapore absorbs the volumes in the tests.
- Whether a no-claim fibre soda keeps the premium that claim-bearing launches earn.
- Singapore and Korean fibre thresholds, and Korean functional approval for fibre.
- Competitor response from Coca-Cola (Simply Pop) or PepsiCo (Pepsi Prebiotic Cola) if either enters Singapore.
