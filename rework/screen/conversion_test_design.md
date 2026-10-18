# Conversion test design: sweetened lime fizz cube (18 October 2026)

**Basis changed on 18 October 2026: the conversion test now runs on a synthesis basis, with no respondents and no outside contact. See [49 conversion test on a synthesis basis](../49_conversion_test_synthesis.md). This recruited design is deferred. It runs only if the team approves an outside contact separately.**

Status: design, power, expected cell sizes, outcome simulation and decision rules are complete. **Execution is not done, and this track cannot recruit or run the test.** Recruitment is an outside contact. The team must run it, or a panel provider must, after the team approves this design. No panel provider was contacted, no quote was requested, and nothing was submitted or registered.

Scripts and outputs: [conversion_test_power_sim.py](conversion_test_power_sim.py), results in [conversion_test_power_sim_results.json](conversion_test_power_sim_results.json). Inputs: [47 statistical explanation](../47_statistical_explanation.md), [46 segment decision](../46_segment_decision.md), [45 working candidate](../45_working_candidate_rework.md), and the simulated ratio summaries in [segment_stat_results.json](segment_stat_results.json).

## 1. Rules applied

- **No sugar-free claim of any kind.** The product is sweetened with an intensive sweetener. That fact is disclosed in the ingredient list, not claimed.
- **No lab test and no medical test.** This is a concept-only test. Nobody consumes the product, so no safety screen or medical question is needed here. The drop of the lab and medical tests does not change this design.
- **No health, nutrition or sodium claim in the stimulus.** The sodium-free claim is gate G1 in [45](../45_working_candidate_rework.md). Rule S2 there closes G1 by physics simulation with stated limits, and any public claim waits for the Thai-text check. This test does not use the claim.
- **Public information only.** No outside contact, no quote or data request, no submission or registration, no bypass of bot checks.

## 2. What the test is for

- **The conversion lead (rework/46):** men aged 25 to 34 convert better per person reached than men aged 35 to 44.
- **Ratio A (25–34 over 35–44):** median 1.04, 90% interval 1.00 to 1.09, probability above 1 of 0.94 ([47 section 1](../47_statistical_explanation.md)). It comes from the age gradient alone. The drinking cell is shared, and the per-year odds ratio interval (0.991 to 1.001) includes 1.0. The ratio is a model assumption, not a finding.
- **Ratio B (25–34 over 45–59):** median 1.15, 90% interval 1.03 to 1.28. Reference only.
- **The outcome is a proxy.** No conversion outcome exists in any source ([47 section 4](../47_statistical_explanation.md)). The test measures purchase intent per person exposed. Ratio A at a 30% baseline is about 1.2 percentage points, which is far below the 5-point design size. Section 10 shows what this means.

## 3. Cells

| Cell | Population | Role |
|---|---|---|
| A | Men aged 25 to 34 | Lead cell |
| B | Men aged 35 to 44 | Comparison cell (closest per-person cell) |
| C | Men aged 45 to 59 | Reference only. Informs the pended volume item. Not a decision input |

Universe: men resident in Thailand, aged 25 to 59, who drank alcohol in the past 12 months and meet the occasion screen (section 5). National online panel. Bangkok is an optional stratum. The DDC counts make the Bangkok 25–34 and 35–44 cells equal in size (section 9).

## 4. Stimulus

Plain product description and a concept image. Neither carries a health, nutrition, sugar or sodium claim. Brand-blind.

Draft text. Square brackets are team inputs, not set in this design:

> [Working name] is a lime-flavoured drink cube. Drop one cube into a glass of water. The cube dissolves and releases carbon dioxide into the water. Pack: [N] cubes. Price: [PRICE] THB per pack.
>
> Ingredients: potassium bicarbonate, citric acid, lime flavour, [intensive sweetener, name to be fixed by the team].

Rules for the stimulus:

- Describe the mechanism only. Do not state a fizz volume or level. Gate G2 (fizz) is closed by physics simulation with stated limits ([45](../45_working_candidate_rework.md), rule S2). A simulation is a model, not a measurement, so no fizz level goes into the stimulus.
- Do not use: "sugar-free", "no sugar", "zero", "sodium", "sodium-free", "low", "healthy", "natural", "for hydration", or any leaf or botanical health wording.
- Do not use the public Singha product name ([42](../42_working_candidate_lime_cube.md), [45 section 2](../45_working_candidate_rework.md)).
- Concept image: one cube dropped into a glass with a lime wedge. No health text, no sugar or sodium text, no brand. No image for this candidate exists in the repo. The team produces it, and a claim check runs before use.

## 5. Screening rules

Terminate, quota or record, in this order:

| Code | Question or check | Rule |
|---|---|---|
| S1 | Sex | Male only. Terminate if not |
| S2 | Exact age | 25 to 59. Assign cell A (25–34), B (35–44) or C (45–59). Terminate outside 25–59 |
| S3 | "In the past 12 months, have you drunk any alcoholic drink?" | Yes continues. No terminates |
| S4 | "In the past 3 months, have you done any of these? Select all." (a) had a drink on a hot day, (b) drank alcohol at home, (c) mixed an alcoholic drink with a soft drink or soda, (d) none of these | Terminate if only (d). Record each item. The same rule applies to both cells |
| S5 | Works in beverage, alcohol, food retail, advertising or market research | Terminate if yes |
| S6 | Took part in a beverage concept or taste test in the past 6 months | Terminate if yes |
| S7 | Consent to the study notice | Terminate if no. Notice wording to be checked by the team's adviser under Thailand's PDPA (not verified here) |
| S8 | Attention check (Q7) | Exclude from analysis if failed |

Quotas: each cell fills to its own target and then closes. Over-quota respondents terminate. Cell C runs only if the team decides to fund it.

Quality rules (proposed; the team and the panel provider confirm them):

- Exclude speeders below one third of the median completion time.
- Exclude duplicate or fraud-flagged panel IDs.
- Record the stimulus dwell time and exclude below the minimum the team sets.

## 6. Questionnaire items

Exact wording. Options are shown in order.

**Exposure**
- Q1. Show the stimulus (text and image) once. Minimum dwell time: team sets it. Proposed 10 seconds.

**Primary measure**
- Q2. "If you saw this product in a shop, how likely would you be to buy it?" 1 Definitely would not; 2 Probably would not; 3 Might or might not; 4 Probably would; 5 Definitely would. **Top-2-box = codes 4 and 5.**

**Secondary measures**
- Q3. "This product costs [PRICE] THB for a pack of [N] cubes. Would you buy it at this price?" Yes / No. The price is a team input, not set here.
- Q4. "When would you use this product? Select all that apply." (a) On a hot day, outdoors or at work; (b) At home, on its own; (c) Mixed with beer, spirits or another drink; (d) At a party or gathering; (e) Other (specify); (f) I would not use it. Occasion measures: (a) hot season, (b) drinking at home, (c) mixing.
- Q5. "In your own words, what kind of product is this?" Open text, coded for product type. Flag any mention of health, diet or sugar as a comprehension finding.
- Q6. "The ingredient list says this product is sweetened with [SWEETENER]. How does this affect your interest?" Much more interested / A little more / No change / A little less / Much less.

**Attention**
- Q7. "To show you are paying attention, select 'Probably would not'."

**Profile (not screened on)**
- P1. Exact age (from S2).
- P2. Province, for the optional Bangkok stratum.
- P3. "In the past 7 days, how often did you drink a sweetened soft drink?" Never / 1 to 2 times / 3 to 6 times / once a day / more than once a day.

## 7. Analysis plan and decision rules

Fix these rules before fieldwork.

- **Primary contrast:** top-2-box share in cell A minus cell B. Two-sided alpha 0.05. Report the 95% confidence interval (Newcombe–Wilson).
- **Direction statement:** "lead supported" if the lower bound is above 0. "Lead reversed" if the upper bound is below 0. Otherwise "direction undetermined".
- **Size statement:** "5-point lead supported" if the lower bound is at or above 5 percentage points. "5-point lead not supported" if the upper bound is below 5 percentage points. Otherwise "size undetermined".
- Report both statements together. A result can support the direction and still rule out a 5-point lead.
- **Secondary:** Yes rate at the stated price by cell (same test). Occasion incidence by cell (Q4), to check whether occasion mix explains any age gap. Disclosure reaction (Q6). Comprehension (Q5).
- **Cell C:** descriptive only, compared with A and B. Not a decision input.

## 8. Power analysis

Two independent cells, two-sided alpha 0.05, power 0.80. Formula, with no continuity correction and no design effect:

n per cell = [z(alpha/2) × sqrt(2 p̄ q̄) + z(beta) × sqrt(p1 q1 + p2 q2)]² / (p1 − p2)²

The baseline top-2-box for men 35–44 is not in any source. The grid below covers 20, 30, 40 and 50 percent. Cell A is p1 = p2 + difference.

| Baseline (cell B) | 5 points | 10 points | 15 points |
|---|---|---|---|
| 20% | 1,094 | 294 | 138 |
| 30% | **1,377** | 356 | 163 |
| 40% | 1,534 | 388 | 173 |
| 50% | 1,565 | 388 | 170 |

One-sided alpha 0.05 would reduce these numbers. Neither a continuity correction nor a panel design effect is applied. Both would increase them.

**The modelled lead is far smaller than 5 points.** Ratio A at a 30% baseline is 1.23 points, which needs 22,166 per cell for 80% power. Averaged over the uncertainty in ratio A, power at that size is about 66%. Ratio B at 30% is 4.4 points, which needs about 1,751 per cell.

## 9. Expected cell sizes

Counts are men, from [47 section 6](../47_statistical_explanation.md). The DDC counts are summed from the downloaded DDC CSV, which sits in the session scratchpad, not in the repo. For men 25 to 44 they agree with the rounded values in 47 within about 2%. For men 45 to 59 they do not match: 7.13 million against 6.65 million, a gap of about 7%. That cell feeds the pended volume item.

| Band | Men, DOPA Nov 2568 (registration) | Men, DDC mid-year | Current drinkers, DOPA | Current drinkers, DDC | Bangkok men, DDC | Bangkok current drinkers |
|---|---|---|---|---|---|---|
| 25–34 | 4,760,000 | 4,705,326 | 3,265,360 (68.6%) | 3,227,854 | 370,367 | 254,072 |
| 35–44 | 4,750,000 | 4,649,860 | 3,258,500 (68.6%) | 3,189,804 | 370,960 | 254,479 |
| 45–59 | 6,650,000 | 7,126,743 | 4,349,100 (65.4%) | 4,660,890 | 563,815 | 368,735 |

- **2024 counts:** DOPA Nov 2568 is the Thai year 2568, which is calendar 2025. It is the nearest registration count to the 2024 drinking survey. The DDC file carries no year label, so its year cannot be confirmed from the file.
- **2021 counts:** none. No 2021 population count by band exists in [47](../47_statistical_explanation.md) or the repo. The 2021 row is a stated limit, not an estimate.
- **Drinking share:** 68.6% is the published men 25–44 cell. Men 25–34 and 35–44 are not published separately, so both use it. The 2024 definition of current drinking is inferred, not confirmed ([47 section 2](../47_statistical_explanation.md)).
- **Screening load:** the pool is far larger than the sample. At the 5-point design (1,377 completes per cell), about 2,008 screened men per cell are needed if the occasion screen passes everyone who drinks. At an illustrative occasion pass rate of 0.5, about 4,015. The occasion pass rate is not in any source. A pilot measures it (section 12).
- **Bangkok:** cells 25–34 and 35–44 are equal in size. A Bangkok stratum would need its own sample size, not derived here.

## 10. Simulation of the test outcome

Method, from the script: two cells of size n. Each person is top-2-box with probability p (cell B) or p × R (cell A). R is drawn from ratio A or ratio B, fitted as log-normal to the median and 90% interval in 47. A pooled two-proportion z-test is run in each of 20,000 draws. Outcomes are the share of draws that confirm the lead, reverse it, or leave it inconclusive. Also reported is the share where the 95% upper bound sits below 5 points.

**Ratio A (25–34 over 35–44), at the 5-point sample size**

| Baseline (cell B) | n per cell | Confirms lead (25–34 significantly higher) | Reverses lead | Inconclusive | Rules out a 5-point lead |
|---|---|---|---|---|---|
| 20% | 1,094 | 7.7% | 0.8% | 91.5% | 67.5% |
| 30% | 1,377 | 12.7% | 0.8% | 86.5% | 56.4% |
| 40% | 1,534 | 18.6% | 0.6% | 80.8% | 47.8% |
| 50% | 1,565 | 25.9% | 0.6% | 73.5% | 40.5% |

**Other checks at a 30% baseline**

- **Null (no lead, ratio = 1):** confirms in 2.5% of draws and reverses in 2.7%. Rules out a 5-point lead in 82%. The test behaves as a two-sided 5% test.
- **Ratio A at the 10-point size (356 per cell):** confirms 6.0%, rules out a 5-point lead in 20.3%.
- **Ratio A at the 15-point size (163 per cell):** confirms 4.5%, rules out a 5-point lead in 11.6%.
- **Ratio A at its own 80%-power size (22,166 per cell):** confirms about 66%, averaged over the uncertainty.
- **Ratio B at the 5-point size (1,377 per cell):** confirms 63%, reverses 0.3%, rules out a 5-point lead in 15.5%. Ratio B's size also rests on the extrapolated age gradient, so a confirm would show no more than the model already assumes.
- **Power check:** a fixed 5-point lead at 1,377 per cell gives 0.80, which validates the power formula.

**Reading**

- If the conversion lead is ratio A, this test confirms it in about 8% to 13% of runs at a 20% to 30% baseline, and about 26% at 50%. It almost never reverses it.
- The test does reject a 5-point-or-larger lead in more than half the runs at a 30% baseline. That is the rejection the design can deliver.
- A result that shows no difference is not evidence against the lead. Under ratio A it is the most likely outcome.

## 11. What this test can and cannot show

**Can show**
- The purchase-intent gap between cells, with 95% intervals about ±3.4 points at a 30% baseline and ±3.7 points at 50%, for 1,377 per cell.
- Whether a 5-point-or-larger lead exists in stated intent for this concept.
- Stated willingness at one price, and occasion mix by cell.

**Cannot show**
- Actual conversion, repeat purchase, or sales. Intent is not behaviour.
- The price response curve. One stated price is tested.
- Taste or fit. The test is concept-only.
- Whether intent tracks per-person potency. This link is assumed, not evidenced.
- Any sodium, sugar, health or nutrition effect. No such claim is in the stimulus.
- Bangkok versus upcountry differences, unless a stratum is funded.

## 12. Recruitment plan (deferred; not the current basis)

The team carries out every step below. This track sends nothing. Under [45 rule S4](../45_working_candidate_rework.md), recruitment needs a separate explicit yes from the user that names the provider and the budget. That yes has not been given.

1. The team approves this design and the decision rules in section 7, before any fieldwork.
2. The team fixes the stimulus inputs: sweetener name, pack size, price points, concept image, and a claim check of the image and text.
3. The team confirms with its adviser the consent notice (PDPA) and the 2024 current-drinking definition.
4. The team asks panel providers for quotes. The quote must give incidence, cost per complete, quota feasibility, quality controls and data protection. This track does not contact any provider.
5. A pilot, sized by the team, measures the screen-in rate and the occasion pass rate. It then resets the screened-persons count in section 9.
6. Fieldwork runs with the quotas in section 5. Each cell closes at its target.
7. Analysis follows section 7. Results are reported with the section 10 simulation as context.

Cost: not estimated. No quote exists.

## 13. Gate verdicts

| Gate | Resolution | Basis |
|---|---|---|
| Conversion test design (design, power, cell sizes, simulation, decision rules) | resolved | Sections 3 to 10 and the script and JSON above. Execution is outside this track |
| Conversion lead settled by the test (men 25–34 over men 35–44) | stated_limit | At the 5-point size the test confirms ratio A in about 13% of runs at a 30% baseline. The baseline is unknown. No conversion outcome exists. Ratio A rests on the age gradient alone, whose odds-ratio interval includes 1.0 |

## 14. Open items and inconsistencies

**Open items (team steps)**
- Sweetener name, price points, pack size, and concept image.
- Pilot to measure the screen-in and occasion pass rates.
- Panel quote, consent notice and drinking definition confirmed by the team's adviser.
- Decision on whether to fund cell C and a Bangkok stratum.

**Stated limits**
- No baseline top-2-box in any source (grid used).
- No 2021 population count by band.
- Men 25–34 and 35–44 drinking not published separately.
- The intent-to-potency link is assumed.
- The 2024 drinking definition is inferred.

**Inconsistencies found in the repo (not edited in this track)**
- [45](../45_working_candidate_rework.md) was corrected while this track ran (file time 18:50). Its section 2 and section 3 now make no sugar-free claim, and its S1 rule closes the sugar-free route. No change is needed there.
- [45](../45_working_candidate_rework.md) section 6 still lists G1 and G2 as "Open. Bench lab test needed" and "Open. Bench test". Its rule S2 closes both by physics simulation. The gate table should be updated to match S2.
- The screen scripts below still carry "sugar-free" in product labels. They are internal, not consumer copy, but the rule says "of any kind", so the team should correct them before any label reaches the panel.
- [effervescent_cube_screen.py](effervescent_cube_screen.py) line 5 and line 612 say "sugar-free". Line 648 (A11) says "contains no sugar and no sodium other than the carbonate", which is a claim-like assumption.
- [lime_cube_screen.py](lime_cube_screen.py) lines 5 and 404 say "sugar-free lime soda". The line 55 quote is the existing public Singha label, which is a different product and is not this candidate's claim.
- [segment_potency_mc.py](segment_potency_mc.py) line 222 chart title says "sugar-free dissolvable lime drink".
- [segment_potency_mc.py](segment_potency_mc.py) lines 57 to 58 use both-sex drinking shares (46.9% and 41.9%). [46](../46_segment_decision.md) and [47](../47_statistical_explanation.md) use men-specific shares (68.6% and 65.4%). This affects the volume index, not ratio A.
- The DOPA Nov 2568 label is calendar 2025, not 2024. The DDC year is not labelled.
