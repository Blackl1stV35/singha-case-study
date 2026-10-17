# Step 3: econometric results on the feasible series

Notebook: `03_econometric_model.ipynb`. Results: `data/econ_trend_results.csv`, `data/econ_share_results.csv`, `data/econ_forecast_annual_sgd_k.csv`. Figure: `03_econometric_fit.png`.

## Data check before estimation (a correction)

The first run of the Singapore parser overwrote the HS 6-digit totals with 8-digit breakdown rows for the flavoured subheading, so the flavoured-lane series and its shares were wrong. The fetch script now keeps total rows only (8-digit field empty). Rebuilt annual totals match the earlier gate-track figures: flavoured lane S$170.1m (2023), S$178.0m (2024), S$172.8m (2025); Thailand share of the lane 1.1% (2023) to 2.1% (2025); Malaysia about 73% of the lane. The HS 2202 total matches the track exactly (S$441.3m, S$440.9m, S$446.9m).

## Results

| Series | Estimate | 95% interval | Reading |
|---|---|---|---|
| Singapore HS 2202 imports, total | +0.9% a year | -0.8% to +2.5% | flat market with a slight upward trend; the interval includes zero |
| Singapore flavoured lane 2202.10 | +0.0% a year | -1.8% to +1.8% | flat; this is the segment proxy for the target |
| Thailand share of HS 2202 | +0.7 pp a year (mean 9.7%) | t = 5.0 | Thai share rising steadily |
| Thailand share of flavoured lane | +0.5 pp a year (mean 1.8%) | t = 8.7 | Thai share small but rising |
| Malaysia share of flavoured lane | -2.1 pp a year (mean 73.7%) | t = -7.9 | Malaysia dominant and losing share slowly |
| Structural shift from 2025 | +1.1% level shift | p = 0.58 | no evidence of a break |
| Forecast, HS 2202 total, 2027 | S$454m (80% interval S$408m to S$505m) | | trend model; 2026 is October to December only, 2029 is January to September only |
| Korea HS 2202, all origins (7 annual points) | +8.0% a year | +3.8% to +12.3% | descriptive only; too few points for a planning estimate |
| Korea HS 2202, from Thailand (7 annual points) | +8.7% a year | +1.9% to +16.0% | descriptive only; wide |

## What this means for the model

1. **The target segment is flat.** The flavoured lane, the closest proxy for zero-sugar sparkling in Singapore, shows no growth. A new entrant has to take share, not ride growth. Base-case category growth is therefore 0%, with a bull case of +1.8% and a bear case of -1.8%, the edges of the interval.
2. **Malaysia holds the lane.** Malaysia is 73% of flavoured imports and is losing about 2 points a year, which is slow. Price and positioning against Malaysian imports are the main commercial questions (risk R4).
3. **The Korea trend is not planning evidence.** Its growth interval runs from about 2% to 16% a year. It should not be used as a base growth figure, and the company's 28% claim does not sit inside this trend range once the 2025 provisional value is considered.
4. **Price response is still not estimated.** The model has no price series, so the elasticity stays a sensitivity range (step 1).

## Limits

- 45 monthly points on a flat series give a wide trend interval. The growth estimate is weak in the way the feasibility note predicted.
- The flavoured lane includes all flavoured waters, not only carbonated or zero-sugar drinks.
- The forecast is a trend model. Its prediction interval is a rough guide, and the annual sums ignore correlation between months.
