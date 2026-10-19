# Consumer persona and cost per acquired customer (19 October 2026)

> Audit, 19 October 2026: the corrections at the end of this record supersede the figures they name.

Team-only record. Desk study: public proxies, no respondents, no outside contact, nothing committed or pushed.

Files: [screen/persona_acquisition_model.py](screen/persona_acquisition_model.py), results [screen/persona_acquisition_results.json](screen/persona_acquisition_results.json), chart [charts/cost_per_acquired_customer_scenarios.png](charts/cost_per_acquired_customer_scenarios.png).

Labels: **SOURCED** (printed page of the NSO 2021 report, or a URL read in this study), **PROXY** (stands in for what the product needs; the gap is stated), **ASSUMPTION** (no source; a range is given), **DERIVED** (arithmetic on labelled inputs).

## 1. The question

Which Thai consumers should the sodium-free lime cube target, using Singha's consumer base as the proxy audience, what does it cost to acquire them, and which levers move that cost most. The conversion lead stays as recorded in [rework/46](46_segment_decision.md) (men, with 25 to 34 as the lead cell). The published cells are 25 to 44, so the lead is tested at that band.

## 2. Source check: rework/47 and the 46.9% and 68.6% values

I checked the NSO 2021 figures against the uploaded report (SD10_04_114_1.pdf), reading the printed pages as images. The extract in [raw/nso2021_SD10_04_114_extract.md](raw/nso2021_SD10_04_114_extract.md) was used as a guide only. Printed page + 19 = PDF page.

| Figure in rework/47 | Record | Printed value (page) | Verdict |
|---|---|---|---|
| Drank in past 12 months, 25 to 44 | 36.5 | 36.5 (Table 2, p. VI; counts in Table 6, p. 25) | Holds |
| Drank in past 12 months, 45 to 59 | 32.4 | 32.4 (same) | Holds |
| Drank in past 12 months, men / women | 46.4 / 10.8 | 46.4 / 10.8 (same) | Holds |
| Drink bottled non-alcoholic every day, 25 to 44 | 17.9 | 18.2 printed (Table 20, p. 41). 17.9 is the count over all persons, including Unknown (Table 50, p. 140) | Holds as a count, but the printed rate is 18.2. Use 18.2 |
| Same, 45 to 59 | 15.8 | 16.0 printed; 15.8 with Unknown in the denominator | Same correction |
| Same, men / women | 17.5 / 10.9 | No printed sex rate; counts give 17.5 / 10.9 with Unknown, 17.7 / 11.0 without | Holds as counts |
| Per-person ratio 25 to 44 over 45 to 59 | 1.28 | 1.28 from printed rates | Holds |
| "Table 50 covers all non-alcoholic beverages" | Scope as stated | Table 50 exists, but the report's text (pp. 36 and 41) and Chart 27 call the group sweet bottled drinks | Scope is ambiguous. Treat it as sweet bottled drinks, as the report's text does |
| "No sex-by-age cross-tab for drinking" | None | True for the 2021 report. NSO Social Indicators 2025 publishes one for 2017, 2021 and 2024 | Holds for the 2021 report only |

**Which holds: 68.6% and 46.9%, for different populations.** NSO Social Indicators 2025, Table 4.6.2, gives men 25 to 44 at 68.6% and women 25 to 44 at 25.2%, with both sexes at 46.9%. The equal-weight average of 68.6 and 25.2 is 46.9, so the three numbers agree. The 68.6% is the men-only value and is the right input for the men lead in [rework/46](46_segment_decision.md) and [rework/49](49_conversion_test_synthesis.md). The 46.9% is the both-sexes value and is right for the all-sex index in `segment_potency_mc.py`, but it cannot rank men's cells. Neither figure appears in the 2021 printed report, which has no sex-by-age cell. The 2021 column of the NSO table matches the printed 2021 report on every row I checked (36.5, 9.0, 31.6, 32.4, 46.4, 10.8), and its 2021 men and women 25 to 44 (58.1 and 15.2) average to 36.65 against the printed 36.5.

- SOURCED, NSO Social Indicators 2025, Table 4.6.2 (https://www.nso.go.th/public/e-book/Indicators-Social/Social-Indicators-2025/284/). Read with WebFetch from a garbled text layer; the printed page image has not been checked. Limit.
- Extract gaps: the extract omits PDF pages 44 (Table 6) and 159 (Table 50). I read both from the uploaded PDF. They should be added to the extract.
- The summary text on printed p. VI does not match its own Table 2 for ages 15 to 19 and 60 and over. This study uses the table values.

## 3. Personas

**Persona A (the lead, men 25 to 44).** The basis is the sweet bottled-drink habit and the alcohol occasion, not sugar-free demand.
- SOURCED: 25 to 44 is 38.5% of everyday bottled-drink consumers aged 6 and over, against 30.3% of the population (Table 50 counts). It is the largest adult group for everyday use: 18.2% against 16.0% for 45 to 59 and 13.4% for 15 to 24 (Table 20, p. 41).
- SOURCED: men are 60.2% of everyday bottled-drink consumers against 48.5% of the population (Table 50 counts). The age-by-sex cell for this habit is not published, so the men 25 to 44 rate is an ASSUMPTION.
- SOURCED (WebFetch): men 25 to 44 currently drink at 68.6% (2024), against 65.4% for men 45 to 59. This is an occasion proxy, not a sugar measure.
- Fit: the hot-season and mixing occasions in [rework/43](43_singha_consumer_base_semantic.md). Neither has been verified and neither carries an age tag, so the fit is an ASSUMPTION.
- Reach: about 14.1 million men aged 25 to 44 on Meta. This is PROXY, from an audience count that gives the male share by total only, so the male share is an ASSUMPTION held constant by age.

**Persona B (a finding that challenges the lead, not promoted).** Adults who already drink sugar-substitute drinks are older, not younger. Everyday use is 1.0% for 45 to 59 and 1.2% for 60 and over, against 0.6% for 25 to 44 (SOURCED, Table 22, p. 42). Weekly-plus use is 3.0% for 25 to 44 and 45 to 59 and 3.3% for 60 and over. So the age ranking seen for sweet bottled drinks does not carry over to intensively sweetened drinks. This is the transfer gap that [rework/49](49_conversion_test_synthesis.md) flagged, now measured. The men 45 to 59 volume item stays pended as the user decided ([rework/46](46_segment_decision.md)).

## 4. What the 2021 survey measures, and the transfer gap

The 2021 survey measures alcohol (past-12-month drinking and frequency), bottled non-alcoholic drinks by frequency, drinks with sugar substitutes by frequency, brewed drinks and food. It does not measure sugar-sweetened drinking as an amount or a share of sugar intake. It has no question on sodium, sparkling water, lime flavour or mixing. The sweet-drink series is therefore a PROXY for sugar-sweetened drinking. The sugar-substitute series is a PROXY for intensively sweetened drinks. Neither is the sugar-free lime cube.
- The report's "high-risk" group means five or more days a week: 18.9% of people aged 6 and over for sweet bottled drinks (Chart 27, p. 36) and 1.0% for drinks with sugar substitutes (Table 22). Neither is a sugar-sweetened volume.
- The sugar-substitute habit is small: 0.8% use it every day and 2.8% weekly-plus, against 14.3% and 53.0% for sweet bottled drinks (SOURCED, Table 20 and Table 22). The cube has to create a habit, not follow an existing one.
- The sweet-drink age ranking does not transfer: it peaks at 25 to 44 for sweet bottled drinks but at 60 and over and 45 to 59 for sugar-substitute drinks.
- The sex split exists only for the sweet bottled-drink series. The sugar-substitute series has no sex split.
- The alcohol measure is an occasion proxy only. It is not a measure of alcohol-alternative demand.
- The 2021 survey predates the product. The 2024 cells sit in a series with a definition change ([rework/47](47_statistical_explanation.md)).

## 5. Funnel and cost per acquired customer

Main route: paid social (Facebook and Instagram), per 1,000 impressions. Formula: **CPA (first purchase) = (CPM / 1,000) / (CTR × LPR) = CPC / LPR**, where LPR is the click-to-first-purchase rate. **CPA (repeat customer) = CPA / repeat rate.**

| Step | Rate used (range) | Label and basis |
|---|---|---|
| Cost per 1,000 impressions (CPM) | THB 120 (80 to 180) | PROXY: Phoenix Media 2025, Facebook average, THB 120 (https://www.phoenixmedia.co.th/the-costs-of-facebook-google-and-line-ads-in-thailand-for-2025/, read with WebFetch). The agency's own clients; no sample or method. The band is an ASSUMPTION |
| Cost per click (CPC) | THB 11.5 | PROXY: same page, Facebook and Instagram combined, 2025 |
| Impression to click (CTR) | 1.04% (0.7 to 1.2%) | DERIVED: CPM / (1,000 × CPC). The band is an ASSUMPTION |
| Impression to unique person (reach) | 50% (frequency 2) | ASSUMPTION. Reach only; not in the CPA |
| Click to first purchase (LPR) | 1.0% (0.08% to 3.4%) | Base: ASSUMPTION. Low: PROXY, Phoenix's conversion of 0.08%, base not defined. High: PROXY, ECDB Thai beverages 2025, add-to-cart 11.5 to 12.0% × (1 − cart abandonment 70.5 to 71.0%) = 3.4%, low confidence (https://ecdb.com/resources/sample-data/market/th/beverages, read with WebFetch; no sample or method; the page repeats across categories) |
| First purchase to repeat | 30% (15 to 40%) | ASSUMPTION |
| Retail route: cost per sample | THB 15 (10 to 25) | ASSUMPTION |
| Retail route: sample to trial | 10% (5 to 20%) | ASSUMPTION |
| 7-Eleven network | 15,945 stores, end 2025 (700 opened in 2025) | SOURCED: CP All year-end 2025 snapshot (https://lssmedia.setlink.set.or.th/2025/YE/CPALL-YE68-ListedCompanySnapshot-EN.html, read with WebFetch) |

**Results (THB per acquired customer):**
- Base (LPR 1.0%): **1,150** per first purchase; 3,833 per repeat customer.
- Agency-implied conversion (LPR 0.08%): 14,375; 47,917 per repeat customer.
- Beverage-cart benchmark (LPR 3.4%): 335; 1,115 per repeat customer.
- Monte Carlo, all four inputs drawn from their ranges (20,000 draws, independent): median **915**, P5 423, P95 2,848 per first purchase. The median is below the base because the LPR distribution is skewed upward. Repeat-adjusted median 3,285 (P5 1,423, P95 10,689).
- Retail sampling floor: 150 per trial (50 to 500). It excludes listing fees, trade spend, distribution and shelf costs, none of which is sourced. It is not comparable with the paid-social figures.

**The range to report** is about THB 335 to 14,400 per first purchase across the three paid-social cases, with a central estimate of THB 900 to 1,150.

**Payback.** A paid click (THB 11.5) costs more than one serving's contribution (THB 3.6 to 6.8 at mid margins, [rework/53](53_unit_cost_and_value_chain.md)). Recovering one first purchase within a single serving needs a click-to-purchase rate of about 320%, which is impossible. Recovering it over four servings still needs about 80%. At the base, payback takes 170 to 320 servings. In no Monte Carlo draw does the cost per first purchase fall below one serving's contribution, and 56% of draws fall below THB 1,000. On these inputs, paid social alone does not acquire single-serve buyers at a profit.

## 6. Levers, ranked by cost effect

Each lever is varied across its stated range with the others at base. The effect on cost per first purchase is proportional: a 50% gain in any one of LPR, CTR or CPM cuts the cost by a third.

| Rank | Lever | Range tested | Cost per first purchase | Swing | Label |
|---|---|---|---|---|---|
| 1 | Click-to-purchase rate: offer, price, product page, marketplace listing, persona fit | 0.08% to 3.4% | THB 14,375 to 335 | 14,040 | PROXY bounds; ASSUMPTION base |
| 2 | Cost per mille: placement, audience, bidding | THB 80 to 180 | THB 767 to 1,725 | 958 | ASSUMPTION band |
| 3 | Click-through rate: creative, hook, targeting | 0.7% to 1.2% | THB 1,714 to 1,000 | 714 | ASSUMPTION band |
| Separate | Repeat rate: retention, pack size, subscription | 15% to 40% | Cost per repeat customer THB 7,667 to 2,875 | 4,792 | ASSUMPTION. Moves the repeat cost only |
| Off-platform | Retail sampling instead of paid media | Floor only | THB 50 to 500 per trial | Not comparable | ASSUMPTION; trade costs unsourced |

Persona fit enters through the LPR, so the first lever is also the one the persona choice moves. The highest-value next step is to test the click-to-purchase rate (price, trial offer, listing) before buying media. The consumer synthesis in [rework/49](49_conversion_test_synthesis.md) is not a consumer finding and cannot test it.

## 7. Limits

- No respondents and no outside contact. The personas are desk hypotheses. The team's consumer-base work ([rework/43](43_singha_consumer_base_semantic.md)) found no age tags and no verified segment.
- Ad costs come from one Thai agency's client data, with no method stated. The Meta audience is a third-party count with no stated estimate date and counts accounts, not people ([Affect Group, 7 April 2026](https://affectgroup.com/blog/thailand-meta-ads-audience-by-age-and-gender-2026/), read with WebFetch).
- The ECDB funnel is low confidence: its conversion rate is locked, and the figures repeat across category pages. The high LPR (3.4%) is therefore weak.
- The 2024 sex-by-age cells come from a garbled text layer. The printed-page image check (NSO SI 2025, p. 284) is still needed.
- The 2021 survey measures sweet bottled drinks, sugar-substitute drinks and alcohol, not sugar-sweetened drinking as such (section 4).
- No Thai FMCG channel share was found. The Kantar page gave no percentages, so the retail route is a floor only.
- Contribution per serving depends on ASSUMPTION margins ([rework/53](53_unit_cost_and_value_chain.md)).
- The Monte Carlo treats the four inputs as independent. Persona fit is not measured separately.
- Snippets used only as context, not as data: Sphere Agency and Mack Media CPM ranges; TikTok global CPM and CPC benchmarks; Euromonitor (paywalled); DataReportal (no ad split by age and sex).

## Audit corrections (19 October 2026)

- **NSO cells:** 68.6% (men 25 to 44), 46.9% (both sexes 25 to 44), 25.2% (women 25 to 44), 65.4% (men 45 to 59), and the 2021 cross-check (58.1 and 15.2 averaging to 36.5). These come from a WebFetch of NSO Social Indicators 2025, Table 4.6.2, read from a garbled text layer. The printed page is not saved and not checked. Unverified.
- **Everyday-drinker counts** (17.9, 15.8, 38.5, 30.3, 60.2): these reproduce from the Table 50 counts in the script. The printed page is not saved, so they stay unverified.
- **Ad costs and benchmarks** (CPM THB 120, CPC THB 11.5, the ECDB conversion benchmark), the 15,945 7-Eleven stores (CP All snapshot), and the 14.1 million Meta reach: cited to pages that are not saved. Read them as 'cited, page not saved'.
- **The 700 stores opened in 2025:** no file holds this figure. Remove it or source it.
