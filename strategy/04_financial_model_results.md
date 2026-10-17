# Step 4: financial model results (revised 2026-10-17)

Notebook: `04_financial_model.ipynb`. Outputs: `data/fin_*.csv`, figures `04_tornado.png` and `04_cumulative_cash.png`. Inputs and their status: `data/assumptions.json`. Korea values are converted to S$ at 1 S$ = 1,015 KRW. The model is pre-tax and has no working capital.

This revision replaces the earlier results. Three input changes drove it:

1. **BCRS deposit** is a pass-through charged at checkout, so it is not an importer cost. The producer fee of S$0.035 per can is added (validated).
2. **Realised price** is now the base case in both markets. Singapore uses the mid-point of the Thai export and Singapore mirror bracket (S$0.478 CIF per can). Korea uses the Thai unit value (KRW 528 CIF per can). The back-solved importer ceiling is now the bull case only.
3. **Korean freight and retail margin** are proxies (freight USD 1,900 per 20 ft from expired LCL quotes; retailer margin 25 percent from BGF and GS Retail gross margins).

## Unit economics per can (base, realised)

| | Singapore (S$, 330 ml) | Korea (KRW, 355 ml) |
|---|---|---|
| CIF price the exporter receives | 0.478 | 528 |
| Exporter cost (ex-works, freight, insurance) | 0.343 | 387 |
| Net contribution after 10% trade spend | 0.088 (18% of CIF) | 88 (17% of CIF) |
| CIF needed for 20% contribution | 0.489 | about 553 |
| Break-even volume at base fixed cost | 5.1m cans a year (1.25% of category) | 5.7m cans a year (0.86% of category) |

Both markets fall short of the 20 percent threshold at the base realised price. The gap is small: about 2 to 5 percent on the CIF price.

## Scenarios

| Market | Scenario | Price basis | Category growth | Share multiplier | NPV (S$m) | Payback | Peak funding (S$m) | Year-5 volume (m cans) |
|---|---|---|---|---|---|---|---|---|
| Singapore | base | realised | 0.0% | 1.0 | -1.00 | not within 5 years | 1.26 | 4.1 |
| Singapore | bull | ceiling | +1.8% | 1.8 | +7.67 | year 3 | 0.36 | 8.1 |
| Singapore | bear | realised low | -1.8% | 0.4 | -1.68 | not within 5 years | 2.31 | 1.5 |
| Korea | base | realised | +3.7% | 1.0 | -0.10 | not within 5 years | 0.99 | 7.1 |
| Korea | bull | ceiling | +6.0% | 1.8 | +34.47 | year 2 | 0.13 | 14.2 |
| Korea | bear | realised low | 0.0% | 0.4 | -1.77 | not within 5 years | 2.42 | 2.4 |

Terminal-value convention: a negative year-5 cash flow gets no terminal value, which treats the business as exiting rather than losing money indefinitely.

## KPI test (step 0 thresholds)

| KPI | Singapore base | Singapore bull | Korea base | Korea bull |
|---|---|---|---|---|
| K1 net contribution at least 20% of CIF | fail (18%) | pass (34%) | fail (17%) | pass (46%) |
| K2 break-even share at most 1.0% | fail (1.25%) | pass (0.51%) | pass (0.86%) | pass (0.18%) |
| K3 year-3 share at least break-even share | fail (0.60% vs 1.25%) | pass (1.08% vs 0.51%) | fail (0.60% vs 0.86%) | pass (1.08% vs 0.18%) |
| K7 NPV positive | fail (-S$1.00m) | pass (+S$7.67m) | fail (-S$0.10m) | pass (+S$34.5m) |
| K8 peak funding at most S$1.0m | fail (1.26) | pass (0.36) | pass (0.99) | pass (0.13) |
| K4 listing, K5 velocity, K6 regulatory | open | open | open | open |

The bear case has no break-even point in Singapore (net contribution is zero), so K2 is not meaningful there.

## What moves the answer (tornado, base case)

- **Singapore** (largest swing first): realised CIF price (S$0.38 to S$0.58 gives -S$1.7m to +S$1.1m), exworks cost (USD 0.15 to 0.30 per can), fixed cost (S$300k to S$600k a year), share ramp, trade spend, freight.
- **Korea** (largest swing first): realised CIF price (KRW 450 to 805 gives -S$1.6m to +S$12.1m), exworks cost, share ramp, freight (USD 1,200 to 2,200 per 20 ft), fixed cost (KRW 350m to 700m a year), trade spend.

The realised CIF price dominates in both markets. The levy and tariff matter less: the levy high case (KRW 18 per can) is a small reduction, and the tariff does not move the exporter's result under the realised basis (the importer absorbs it).

## What the revision means

- At category-average realised prices, neither market clears the economic thresholds in the base case. Both are close to break-even.
- Both markets become positive only if the product can realise a price about 2 to 5 percent above the Thai category unit value, or if fixed costs and exworks cost are lower than assumed.
- A group route (shared fixed cost, group factory) moves the fixed-cost and exworks lines. Those are sensitivities until the group shows actual costs.
- Korea's base is closer to break-even than Singapore's, but its bull case is much larger. The Korea bull case relies on the ceiling price and a 1.8 share multiplier, neither of which has evidence.

## Limits

- Pre-tax, no working capital, no depreciation, no hedging.
- Category volume bases are vendor-derived (Singapore 2021, Korea 2024).
- Freight, importer margin and listing fees are unverifiable or proxies.
- The realised price is a category average, not a Singha price.
- The company-stated Korea figures are not used and are unverifiable.
