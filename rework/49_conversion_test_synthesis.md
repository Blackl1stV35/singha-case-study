# Conversion test on a synthesis basis (18 October 2026)

Status: run. The basis changed from a recruited panel to synthesis at the user's instruction. There are no respondents, no panel, and no outside contact. The result is a model result under stated assumptions. It is not a consumer finding.

Script: [screen/conversion_synthesis_test.py](screen/conversion_synthesis_test.py). Results: [screen/conversion_synthesis_results.json](screen/conversion_synthesis_results.json). Inputs: [47 statistical explanation](47_statistical_explanation.md) and the rework/47 results file [screen/segment_stat_results.json](screen/segment_stat_results.json). The script checks its ratio against that file (median 1.041 against 1.04; consistent).

## 1. What changed

- The recruited test in [screen/conversion_test_design.md](screen/conversion_test_design.md) (sections 5 to 12) is **deferred, not deleted**. It runs only if the team approves an outside contact separately, with a named panel provider and budget (decision S4 in [45](45_working_candidate_rework.md)).
- The test that now counts compares modelled purchase intent for men aged 25 to 34 against men aged 35 to 44 (lead against comparison), with men aged 45 to 59 as a reference.
- Synthetic respondents (for example, language-model personas) are **not** used. Their answers would be our assumptions returned as data, not evidence.

## 2. Model

- Per-person potency: drinking share times the age-adjusted daily sugar-sweetened share. The sugar base cancels in every ratio.
- Synthesised intent in the lead cell: the comparison-cell baseline B times (potency ratio) to the power e. The elasticity e is an **assumption**, uniform from 0.5 to 1.0. An elasticity of 0 would mean no link, and then the test returns nothing.
- Comparison-cell baseline B: **no source exists**. A grid of 20, 30, 40 and 50 percent is used.
- **Scale.** The primary reading applies the ratio to the **odds** of the comparison cell, which is how an odds ratio should be used. The earlier version applied it to the share. Both are reported. The share version overstates the gap at higher baselines. The conclusion is the same on both.
- Uncertainty: the odds ratio per year is log-normal from the published interval (0.991 to 1.001); drinking shares carry plus or minus 3 points, because no 2024 interval is published; e is uniform.

## 3. Decision rules (fixed before the run)

- **Direction:** "lead supported" if P(difference > 0) is at least 0.90. "Lead not supported" if P(difference < 0) is at least 0.90. Otherwise "direction undetermined".
- **Size:** "5-point lead supported" if P(difference at least 5 points) is at least 0.90. Otherwise "5-point lead not supported". Five points is the design size from the recruited test.
- The probabilities are model probabilities under the stated assumptions. They are not sampling probabilities.

## 4. Results

Difference in intent, men 25 to 34 minus men 35 to 44, in percentage points. Primary (odds scale):

| Comparison-cell baseline | Median | 90% interval | P(> 0) | P(≥ 5) | Direction | Size |
|---|---|---|---|---|---|---|
| 20% | 0.47 | −0.02 to 1.06 | 0.94 | 0.000 | lead supported | 5-point lead not supported |
| 30% | 0.61 | −0.03 to 1.39 | 0.94 | 0.000 | lead supported | 5-point lead not supported |
| 40% | 0.70 | −0.04 to 1.58 | 0.94 | 0.000 | lead supported | 5-point lead not supported |
| 50% | 0.72 | −0.04 to 1.63 | 0.94 | 0.000 | lead supported | 5-point lead not supported |

For comparison, the share scale (the ratio applied to the share) gives medians of 0.59, 0.88, 1.18 and 1.47 points at the four baselines, with P(≥ 5) at most 0.003. The conclusion is the same.

Reference, men 25 to 34 minus men 45 to 59 (volume item, pended; not a decision input):

| Baseline | Median | 90% interval |
|---|---|---|
| 20% | 2.10 | 0.37 to 4.46 |
| 30% | 3.15 | 0.55 to 6.68 |
| 40% | 4.20 | 0.74 to 8.91 |
| 50% | 5.25 | 0.92 to 11.14 |

## 5. Reading

- **The model supports a direction but not a size.** Men 25 to 34 come out ahead in 94% of draws, but the median gap is under 1 point on the odds scale at every baseline tested (under 1.5 on the share scale). A 5-point lead is not supported at any baseline.
- **The 0.94 probability is a sampling-side statement.** It comes from the odds-ratio interval, which includes 1.0, and an elasticity with no source. The critic's check found a two-sided p of about 0.12 on the odds ratio itself. Read 0.94 as "directional under the stated inputs", not as confidence.
- **The direction rests on two assumptions.** The first is the age gradient, whose odds-ratio interval includes 1.0 ([47 section 2](47_statistical_explanation.md)). The second is the elasticity e, which has no source. The synthesis probability is only as good as those two inputs.
- **The lower bound touches zero at every baseline.** At 90% the gap is not separated from zero.
- **Consequence for the lead.** A gap of about 1 point needs roughly 22,000 respondents per cell for 80% power ([design section 8](screen/conversion_test_design.md)). A recruited test at the design size would not resolve it. So the synthesis basis cannot replace field evidence. It only records what the sourced inputs imply.
- **The lead against men 45 to 59 is larger on paper**, about 2 to 5 points. It is also the reference that depends most on the extrapolated age gradient, so it is not a stronger finding. Volume, the pended item, depends on population size, not on this gap ([46 section 3](46_segment_decision.md)).

## 6. What this basis can and cannot show

**Can show:** the size and direction the sourced drinking shares and age gradient imply, under stated assumptions, with sensitivity to the baseline and the elasticity.

**Cannot show:** actual conversion, purchase, repeat or intent. Whether any band responds to the cube. Whether the segment proxy carries over to this product. The proxy measures sugar-sweetened drinking, and the candidate contains no sugar, so the age ranking may not transfer to an intensively sweetened drink. This is untested. The baseline and the elasticity are unsourced. No conversion outcome exists in any source ([47 section 4](47_statistical_explanation.md)).

## 7. Gate verdict

| Gate | Resolution | Basis |
|---|---|---|
| Conversion test (synthesis basis) | stated_limit | Ran on the model. Direction supported under the stated assumptions (P about 0.94). Size not supported (a 5-point lead has probability 0 at every baseline). No consumer evidence, and the test cannot provide any |

## 8. Decision for the user

The user's decision to optimise conversion (lead: men 25 to 34) stands as recorded in [46](46_segment_decision.md). This synthesis tells the user one thing the record did not state plainly: the per-person gap is about 1 point. If the team wants to keep the conversion lead as the reason to target men 25 to 34, that choice rests on a small, assumption-driven gap. Options, for the user to choose:

1. Keep conversion as the lead, with the synthesis result stated as a limit in the submission.
2. Keep conversion as the lead, and approve an outside panel with a named provider and budget. That is the only route that could test the size.
3. Revisit the segment choice. The lead against men 45 to 59 is larger on paper, but it depends more on the same extrapolated age gradient.

I have not changed the decision.
