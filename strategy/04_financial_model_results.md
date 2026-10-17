# Step 4: financial model results (rough inputs)

Notebook: `04_financial_model.ipynb`. Outputs: `data/fin_*.csv`, figures `04_tornado.png` and `04_cumulative_cash.png`. Inputs: `data/assumptions.json`. Every input is rough, as accepted by the user on 2026-10-17, and its status is recorded there. Korea values are converted to S$ at the model rate (1 S$ = 1,015 KRW).

## Unit economics per can

| | Singapore (S$ per 330 ml) | Korea (KRW per 355 ml) |
|---|---|---|
| Shelf price incl. tax | 1.45 | 2,000 |
| CIF price the exporter can charge | 0.52 | 805 (0% tariff placeholder) |
| Exporter cost (ex-works, freight, insurance) | 0.34 | 364 |
| Net contribution after 10% trade spend | 0.12 (24% of CIF) | 360 (45% of CIF) |
| Break-even volume at base fixed cost | 3.6m cans a year (0.9% of category) | 1.4m cans a year (0.2% of category) |

## Scenarios

| Market | Scenario | Category growth | Share multiplier | NPV (S$m) | Payback | Peak funding (S$m) | Year-5 volume (m cans) |
|---|---|---|---|---|---|---|---|
| Singapore | base | 0.0% | 1.0 | -0.40 | not within 5 years | 0.90 | 4.1 |
| Singapore | bull | +1.8% | 1.8 | +3.08 | year 5 | 0.58 | 8.1 |
| Singapore | bear | -1.8% | 0.4 | -1.32 | not within 5 years | 1.76 | 1.5 |
| Korea | base | +3.7% | 1.0 | +13.2 | year 3 | 0.35 | 7.1 |
| Korea | bull | +6.0% | 1.8 | +30.7 | year 2 | 0.17 | 14.2 |
| Korea | bear | 0.0% | 0.4 | +1.5 | not within 5 years | 0.73 | 2.4 |

## Where the value comes from

- **Singapore:** the five-year cash flow is negative in the base case (about -S$0.65m present value). The small positive NPV comes only from the terminal value. The market is flat, Malaysia holds 73% of the flavoured lane, and the fixed cost is large relative to the margin.
- **Korea:** about 79% of the base NPV is terminal value, so the Korea answer depends on the cash flow still holding in year 5 and beyond. Read the Korea NPV as "positive if the ramp is reached and sustained", not as a five-year return.

## KPI test (step 0 thresholds)

| KPI | Singapore base | Singapore bull | Singapore bear | Korea base | Korea bull | Korea bear |
|---|---|---|---|---|---|---|
| K1 net contribution at least 20% of CIF | pass (24%) | pass | pass | pass (45%) | pass | pass |
| K2 break-even share at most 1.0% | pass (0.88%) | pass (0.83%) | pass (0.93%) | pass (0.21%) | pass (0.20%) | pass (0.24%) |
| K3 year-3 share at least break-even share | **fail** (0.60% vs 0.88%) | pass (1.08% vs 0.83%) | **fail** (0.24% vs 0.93%) | pass (0.60% vs 0.21%) | pass | pass (0.24% vs 0.24%, marginal) |
| K7 NPV positive | **fail** | pass | **fail** | pass | pass | pass |
| K8 peak funding at most S$1.0m | pass (0.90) | pass | **fail** (1.76) | pass | pass | pass |
| K4 listing, K5 pilot velocity, K6 regulatory | open | open | open | open | open | open |

Read across: Korea passes every testable KPI in all three scenarios, and Singapore passes only in the bull case. The bull result for Singapore needs the category to grow and the share to nearly double. K4 to K6 are untested in all cases, so no scenario clears the full set.

## What moves the answer (tornado, base case)

- **Singapore** (NPV swing largest first): exworks cost (0.15 to 0.30 USD per can: from +1.6m to -1.8m), shelf price (1.20 to 1.60: from -1.6m to +1.5m), BCRS deposit treatment (0 to 0.10 per can: from +2.2m to -0.4m), share ramp (0.5x to 1.5x), fixed cost, retailer margin.
- **Korea** (NPV swing largest first): share ramp (0.5x to 1.5x: from 4.4m to 22.0m), shelf price (1,600 to 2,200 KRW: from 4.8m to 17.4m), ex-works cost, retailer margin, category volume (400m to 700m cans: from 7.5m to 16.5m), tariff (0% to 30%: from 13.2m to 5.0m). Korea stays positive at the 30% tariff.

## What would change the verdicts

1. **Singapore BCRS deposit.** If the deposit is passed to consumers rather than borne by the importer, Singapore's base NPV turns to about +S$2.2m. This is a G6 item in the Singapore resolution run.
2. **Korea tariff.** The base uses 0%. The Korea resolution run reports the Thailand-Korea FTA and MFN rates. Korea stays NPV-positive up to a 30% tariff in this model.
3. **Korea volume.** The base assumes about 1% of carbonated volume by year 5. No source supports that share. It is a planning assumption that a pilot must test (KPI K5).
4. **Retail price in Korea.** The 2,000 KRW reference is a convenience store list price. Supermarket prices may be lower, which the tornado covers from 1,600 KRW.

## Limits

- Pre-tax, with no working capital, no depreciation, no tax, and no currency hedging.
- Category volume bases are vendor-derived (Singapore from a 2021 figure, Korea from a 2024 teaser).
- The terminal value is a simple perpetuity on year-5 cash at 1% growth and a 12% discount rate, all rough.
- The Korea share ramp is the same shape as Singapore's. It has not been fitted to any Korean evidence.
