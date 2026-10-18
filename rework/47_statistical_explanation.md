# Statistical explanation of the conversion lead (18 October 2026)

> Correction, 19 October 2026: the everyday-drinker rates for 25 to 44 and 45 to 59 (17.9% and 15.8% above) count Unknown answers in the denominator; the printed rates are 18.2% and 16.0%. The 68.6% and 46.9% cells come from NSO Social Indicators 2025 Table 4.6.2, not from the 2021 report, and the pooled 15.8% sugar-sweetened share is not a printed 2021 figure. Read [55](55_consumer_persona_and_acquisition.md) before quoting any figure from this record.

Status: plan steps run where sources allowed. Inputs gathered, local analysis run, and limits recorded. **The conversion lead is weakly identified.** The volume lead (men 45–59) is well identified by size but is pended by decision.

Scripts and outputs: [rework/screen/stat_explanation.py](screen/stat_explanation.py) (results in [rework/screen/segment_stat_results.json](screen/segment_stat_results.json)), chart [rework/charts/conversion_statistics.png](charts/conversion_statistics.png). Inputs gathered in the workflow journal (wr0grmzon), not copied into the repo.

## 1. What the analysis shows

Per-person potency for a sex-specific band is drinking share × daily sugar-sweetened share (age-adjusted). Two ratios were tested under the stated uncertainty:

| Ratio | Probability ahead | Median ratio | 90% interval | What drives it |
|---|---|---|---|---|
| A: men 25–34 vs men 35–44 | 0.94 | 1.04 | 1.00 to 1.09 | Age gradient only (drinking cell is shared) |
| B: men 25–34 vs men 45–59 | 0.98 | 1.15 | 1.03 to 1.28 | Age gradient about 65%, drinking cells about 35% |

Sensitivity of B (total-order indices, log scale): the odds ratio per year of age 0.72, drinking 25–34 0.14, drinking 45–59 0.15, sugar base 0.00.

**Reading:** B looks positive, but most of it comes from one input, the age gradient, which is estimated from one pooled survey and whose 95% interval includes 1.0 (0.991 to 1.001). A is small and fragile. The conversion ranking is therefore an estimate, not a demonstrated fact.

## 2. What the inputs add and where they stop

**Sex-specific sugar share (new, important).** In the 2021 survey (25–59), daily sugar-sweetened consumers are 20.6% of men and 12.5% of women. The men's adjusted odds ratio against women is 1.44. The earlier model pooled the sexes at 15.8%. This changes the level of per-person potency for men but not the within-men ratios above, because the sugar base cancels.

**Age gradient, restated.** The per-year odds ratio for daily consumption is 0.996 (CI 0.991 to 1.001). Over ten years the derived odds ratio is 0.96 (CI 0.91 to 1.01), which includes 1. The weekly-plus odds ratio is 0.78 per decade. Intake falls about 1 mL per day per year. The age effect is small and its interval includes no effect.

**Drinking by sex and band (2024).** Men 25–44 at 68.6% and men 45–59 at 65.4% are the only sex-specific band cells available. Men 25–34 and 35–44 are not published separately. Women are 25.2% (25–44) and 19.9% (45–59). No 2024 standard errors, confidence intervals or design effects are published.

**Series break (blocks any trend claim).** Men's current drinking reads 56.6% (2015), 47.5% (2017) and 55.7% (2024). The 2017 release defines past-year drinking; the 2024 definition is inferred. Until the definition is confirmed, the 2017–2024 change cannot be read as a trend.

**Conflicting headline (unresolved).** The NSO infographic gives 35.2% (20.9 million) for 2024; a news report gives 31.7% (15.3 million). The sex rates in the news report do not reproduce its total. The 35.2% figure is used here, flagged as unresolved.

**Size (well identified).** Men 45–59 are about 6.65 million (DOPA Nov 2568), against about 4.76 million for men 25–34. Size alone gives men 45–59 about 1.4 times the pool. This is the volume lead, which is pended.

## 3. Plan steps: status

| Step | Status | Result or limit |
|---|---|---|
| 1. Global sensitivity (Sobol) | Done | Odds ratio per year dominates B; sugar base cancels |
| 2. Design-based uncertainty | Blocked | 2024 sample counts by band, standard errors and design effects are not published; the survey-detail PDF returned 404 |
| 3. Beverage-spend cross-check | Blocked | The 2024 Household Socio-Economic Survey publishes beverage spend by household size and region, but not by age of household head; head-age bands do not match the target bands |
| 4. Trend check | Blocked | The series break in men's drinking (definition change) prevents a trend claim |
| 5. Alternative definitions | Partial | The 2017 heavy-episodic data have 25–30 and 31–45 bands; no 2024 equivalent |
| 6. Regional split | Blocked | Bangkok 25–59 by age is not published; the DOPA table omits ages 26–59 |
| 7. Consumer panel | Gated | Recruiting a panel is outside contact and needs your approval |

## 4. Limits closed as stated limits

- No sex-by-band sugar-sweetened beverage tables exist in any accessible source. The 2021 survey publishes sex-specific totals and per-year age odds ratios only. The full 2021 report (over 10 MB) was not read.
- No conversion outcome exists in any source: no trial, purchase, repeat or response data. Conversion is undefined in the data, so the segment comparison has no outcome variable.
- No sugar-free or artificially sweetened drink data by sex and age, other than a restricted urban sample of ASB use by 20–49 and 50–64 (Loyfah et al. 2025).
- The men 25–34 vs 35–44 order rests on the age gradient alone. The claim that men 25–34 convert better than men 35–44 or 45–59 is an open assumption, not a finding.

## 5. Decision and what it needs

The user's decision to optimise conversion stands (see [rework/46](46_segment_decision.md)). The statistical support for it is thinner than the earlier record suggested: it rests on the age gradient, and the size lead is the stronger finding. The decision should be read as a choice made on a weak estimate, not on a demonstrated conversion advantage.

Two downloads would close the most important gaps. Both need your permission, per the download rule:
1. **The NSO 2021 Health Behaviour of Population Survey full report** (file SD10_04_114_1.pdf, from catalogapi.nso.go.th; size over 10 MB). It is the most likely source of age-band and sex-specific sweet-drink tables.
2. **The DDC open-data CSV for population by age group, province and sex** (opendata.ddc.moph.go.th, file untitled.csv; size unknown). It may give a Bangkok 25–59 split. Its age labels and sex codes are unverified, so it needs checking before use.

## 6. Update: approved downloads (18 October)

- **NSO 2021 Health Behaviour full report:** the download was blocked by the NSO web application firewall. The server returned a block page (3.5 KB, not the report). The block was not bypassed, so the limit stands. The route that remains is for you to download the file in your own browser and point me to the saved copy.
- **DDC population CSV (mid-year series, province × age group × sex):** downloaded (301 KB, 2,618 rows). It reproduces the national total (65.9 million) and the registered Bangkok total (about 5.4 million, once under-15 and 70+ are added). It is a mid-year series, not a registration count, so it is a cross-check, not a replacement for DOPA.

Size cross-check, men aged 25–34, 35–44 and 45–59 (millions):

| Basis | 25–34 | 35–44 | 45–59 |
|---|---|---|---|
| Thailand, DOPA Nov 2568 (registration) | 4.76 | 4.75 | 6.65 |
| Thailand, DDC mid-year | 4.71 | 4.65 | 7.13 |
| Bangkok, DDC mid-year | 0.37 | 0.37 | 0.56 |

The size lead of men 45–59 holds nationally and in Bangkok (about 1.5 times either younger band). In Bangkok, men 25–34 and 35–44 are the same size, so a Bangkok conversion test would compare equal-sized cells.

The CSV has no drinking or sugar data. The conversion ranking and its uncertainty are therefore unchanged.

## 7. Update: the uploaded NSO 2021 report (read in full where needed)

The user uploaded the 222-page NSO Health Behaviour of Population Survey 2021 (SD10_04_114_1). It is a 2021 survey, not 2024. Its age groups are 6–14, 15–19, 20–24, **25–44 (combined)**, 45–59 and 60+. It does not separate 25–34 from 35–44, so the conversion comparison of men 25–34 against men 35–44 cannot be sourced from it.

**Sourced 2021 figures used here:**

| Measure | Value | Source |
|---|---|---|
| Drank alcohol in past 12 months, 25–44 | 36.5% | Summary Table 2 (p. VI) |
| Drank alcohol in past 12 months, 45–59 | 32.4% | Summary Table 2 |
| Drank alcohol in past 12 months, men / women | 46.4% / 10.8% | Summary Table 2 |
| Non-alcoholic beverages drunk every day, 25–44 | 17.9% | Table 50 (counts; computed as everyday ÷ total) |
| Non-alcoholic beverages drunk every day, 45–59 | 15.8% | Table 50 |
| Non-alcoholic beverages drunk every day, men / women | 17.5% / 10.9% | Table 50 |

Table 50 covers all non-alcoholic beverages, not only sugar-sweetened ones, so it is a broad proxy for sweet-drink frequency. The report contains no sex-by-age cross-tab for drinking or beverage frequency.

**Per-person proxy, 25–44 against 45–59 (2021, both sexes):** drinking × everyday non-alcoholic share gives 0.065 against 0.051, a ratio of **1.28**. That agrees in direction with the earlier model's ratio of 1.15 for men 25–34 against men 45–59. The comparison is not sex-specific and not band-specific, so it is a cross-check, not a replacement.

**What this changes:**
- The 25–34 vs 35–44 comparison (ratio A) has no source in any survey we hold. It stays a model assumption. The claim that men 25–34 convert better than men 35–44 is still unsupported.
- The 25–44 vs 45–59 direction is now supported by a 2021 survey, not only by the 2024 model inputs.

The recruited consumer panel stays deferred. The conversion test runs on a synthesis basis, with no respondents, and its result is in [49](49_conversion_test_synthesis.md).
