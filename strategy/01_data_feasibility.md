# Step 1: data-feasibility check for the econometric model

## What data exist

| Series | Market | Frequency and span | Source and status | Usable for |
|---|---|---|---|---|
| HS 2202 imports, world | Singapore | monthly, Jan 2023 to Sep 2026 (45 months) | SingStat T010001, validated (updated 16 Oct 2026); saved in `raw/singstat/` | time series: trend, seasonality |
| HS 2202.10 flavoured lane, world | Singapore | monthly, same span | SingStat, validated | segment proxy for the target |
| HS 2202 and 2202.10 imports from Thailand and Malaysia | Singapore | monthly, same span | SingStat, validated | share trends |
| HS 2202 imports, all origins | Korea | annual, 2019 to 2025 (7 points) | UN Comtrade preview, validated but provisional for 2025 | trend only |
| HS 2202 imports from Thailand | Korea | annual, 2019 to 2025 (7 points) | UN Comtrade preview, validated | trend only |
| Sparkling and carbonated sales volume | Singapore | annual, 2021 only (vendor) | MarketLine, vendor | category volume anchor |
| Sparkling and carbonated sales volume | Korea | 2024 only (vendor) | MarketLine, vendor | category volume anchor |
| Shelf prices | Singapore | one listing (FairPrice, 17 Oct 2026) plus comparators in the gate track | dated, thin | price level only |
| Shelf prices | Korea | one reference (GS25 list) | dated, thin | price level only |
| Brand or product sales series | both | none validated | company claims only | not usable |
| Consumer panel or price-response data | both | none validated for sparkling | regional elasticities only (transferability low) | prior only |

## Feasibility verdicts

1. **Singapore time-series model: feasible.** 45 monthly points, validated, with seasonality. It can estimate the trend growth of the HS 2202 total and of the flavoured lane, its volatility, and the Thai and Malaysian share trends. It cannot estimate price response, because there is no monthly price series.
2. **Korea trend model: descriptive only.** Seven annual points are too few for a credible trend interval, and the 2025 figure is provisional. The output will show the direction and a wide range, not an estimate to plan on.
3. **Price elasticity from data: not feasible.** There is no price series for sparkling or zero-sugar products in either market. The only elasticity evidence is regional and non-transferable (about -0.9 to -1.4 in the gate track). It is used as a prior range in the financial model's sensitivity, not as an estimate.
4. **Sugar-reduction demand shift: feasible as a parameter.** The Singapore Nutri-Grade study (Shin et al., AJPH 2026, validated abstract) reports sugar purchases down 18% and unhealthy beverage purchases down 44%. It supports a demand shift toward reduced-sugar drinks, but it does not size sparkling demand. It enters as a scenario multiplier, not a fitted coefficient.
5. **Korea company claims: not usable as data.** The 29.1m-litre market and 28% growth did not reproduce, and the Singha sales claims have no source in the gate run. They are excluded from the model's inputs and kept as a scenario.

## Decision for step 3

- Estimate a Singapore monthly model for the HS 2202 total and the 2202.10 flavoured lane, with a log-linear trend, month dummies and Newey-West standard errors. Use the estimated trend growth as the category growth input in step 4.
- Report the Korea trend as descriptive, with its wide interval, and use the flat-to-modest trend as a bear-case growth input.
- Do not fit a price-response model. Carry price response as a sensitivity range.

## Risks to the feasibility of the model itself

- 45 monthly points cover a flat period (S$441m to S$447m a year). A trend estimated from a flat series has a wide interval, so the growth input is weak, and the model should say so.
- The 2202.10 lane is a segment proxy. It includes all flavoured waters, not only carbonated or zero-sugar drinks, and Malaysia holds about 73% of it.
- A structural break in 2025 would not be separable from the trend with this span.
