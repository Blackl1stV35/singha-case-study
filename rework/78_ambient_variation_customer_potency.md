# T15: ambient variation of the potency of existing Singha customer bases (20 October 2026, revision 3 after the second verification)

Status: run and checked against the criteria below. The per-person lead is a proposal that passes four of the six checks it was given and does not pass the other two; it is not a validated result (section 7.1 defines how the words "validated", "proposed" and "moderate" are used). Team-only record. Synthesis under stated assumptions: no respondents, no outside contact, no purchase or sales data. Nothing was committed or pushed, and no judge-facing file was edited.

Files: [screen/ambient_variation.py](screen/ambient_variation.py) (script), [screen/ambient_variation_results.json](screen/ambient_variation_results.json) (every number below comes from this file unless a source is named), [screen/ambient_variation_run.log](screen/ambient_variation_run.log) (run log), chart [charts/ambient_potency.png](charts/ambient_potency.png). Raw sources: [raw/diligence_2026-10-20/T15/](raw/diligence_2026-10-20/T15/). Run: 40,000 draws (two halves of 20,000), seed 20261020, 200 placebo permutations, about 36 seconds, peak working set 191 MB.

## 0. Answer in brief

Potency is a decomposed quantity: reach (size of the base) times trial propensity (top-2-box intent proxy, an ASSUMPTION link) times repeat propensity times contribution per cube, less the exclusion share (potassium-caution coverage, plus an alcohol-cue exclusion for drinker bases). The result depends on the denominator, so three lenses are reported and each states its own.

| Lens (denominator) | Result | Confidence and status |
|---|---|---|
| Reach: total potency of the base | No robust winner. Men aged 45 to 59 who drink alcohol rank first in 68.1 percent of draws; sweet-bottled drinkers aged 25 to 44 in 18.5 percent; men aged 25 to 34 in 13.0 percent. | None (not robust). The leader changes to sweet-bottled drinkers 25 to 44 in four structural sweeps: no sex gradient, alcohol cue at 20 percent, the 2021 drinking column, and the bottled-base habit counted once (section 7.8). |
| Per person in the age-sex cell (denominator: the cell population; the conversion lens of rework/46 and 47; like-for-like among the six drinker cells) | **Men aged 25 to 34 who drink alcohol** rank first among the drinker cells in 94.1 percent of draws (men 35 to 44: 5.8; men 45 to 59: 0.1). | **Moderate.** The leader is the same in all 55 re-runs and splits. The 0.90 bar is met in the full run, both halves, four model forms and 23 leave-one-factor-out runs, and missed in four runs: April (0.871), December (0.895), the season stress run (0.834) and the run where men 35 to 44 have the same coverage as men 25 to 34 (0.882). Not validated: two of the seven criteria fail (c5, c7). |
| Per member of the base (denominator: population times penetration; comparable across base types) | Men aged 25 to 34 first in 81.6 percent of draws; sweet-bottled drinkers 25 to 44 in 13.4 percent. | None (not robust). The leader changes to sweet-bottled drinkers 25 to 44 in three sweeps (no sex gradient, alcohol cue 20 percent, bottled habit counted once). |

Margin of men 25 to 34 over men 35 to 44, per person in the cell, on two measures (both intervals touch 1):

- Age gradient alone (the per-year age odds ratio and the assumed intent elasticity; the part that rests on a source): ratio 1.0295 (90 percent interval 0.9985 to 1.0677; probability above 1 is 0.9412), about 0.9 points at a 30 percent baseline. This reproduces rework/47 ratio A (1.0409; 0.9979 to 1.0855; 0.9411). The odds ratio itself is carried and UNVERIFIED (section 2).
- Full model: ratio 1.057 (0.997 to 1.123; probability above 1 is 0.9415), about 1.7 points at a 30 percent baseline. The extra margin is the potassium-caution exclusion (ratio 1.022 on its own), which is a team model with PROXY inputs, and the assumed temperature noise.
- Trial propensity including the assumed temperature sensitivity: 1.030 (0.984 to 1.082; 0.869). This is not a sourced figure: the 0.869 is lower than 0.941 because the assumed temperature sensitivities add noise.

The 94 percent in this record is a different quantity from the 94 percent in submission/01, 02 and 06 and in rework/49. Those state that men 25 to 34 beat men 35 to 44 in 94 percent of draws on the age gradient alone (a pairwise probability, 0.941). This record's 94 percent is the first-place probability among six drinker cells in the full model (0.9405). The two coincide by chance of rounding and must not be read as one result (section 9).

**Applied:** men aged 25 to 34 who drink alcohol as the proposed lead for conversion, within the drinker cells, at moderate confidence and with a thin margin over men aged 35 to 44. This is a proposal that the pilot tests, not a validated result. **Not applied:** any reach winner, and any claim that men aged 25 to 34 are more potent than sweet-bottled drinkers on a per-member basis. The volume item (men 45 to 59) stays pended, as decided in rework/46. The sugar-reduction pool ranks first on reach among all nine bases (99.5 percent) but is a market pool (Mintel, S), not a Singha customer base; it is reported separately.

Ambient temperature: with independent per-base sensitivities inside the assumed range (0 to 0.05 per degree Celsius), no leader changes in any month, and none changes even at 20 times that range (up to 1.00). It does lower the per-person leader's first-place probability: 0.871 in April, 0.973 in August, 0.941 over all months, 0.973 with temperature fixed at its mean. That result is a property of the independent draws: no base is more heat-sensitive than another. When men 35 to 59 are given a higher sensitivity than men 25 to 34 by a fixed amount, the per-person leader in April changes to men 35 to 44 at a difference of 0.04 per degree Celsius or more (0.03 leaves men 25 to 34 first at 0.505), and the twelve-month leader never changes (section 7.6). No source gives the size or direction of any heat effect on demand: a source was not searched for successfully (section 8, item 8).

## 1. What this revision changed

Revision 3 answers the second verification (11 issues). Each row gives the finding on checking and the action.

| Verifier issue | Finding on checking | Action |
|---|---|---|
| Medium: slide 5 quotes a margin of about 6 percent that includes the team-model coverage gradient; the set says 0.6 to 1.2 points; the 94 percent is a different basis from submission/01 and 06; "no edit needed" for ratio A | Correct. About 3 percent (0.9 points) is the age-gradient margin; about 6 percent (1.7 points) adds the coverage gradient and temperature noise. | Both measures are quoted in section 0, section 6 and the slide text; section 9 lists submission/01 line 30, 02 line 56, 06 line 37 and 10 line 95 and states that the two 94 percent figures differ in basis. |
| Medium: the per-person lens fails c5 and c7, yet the lead was applied; "moderate" undefined; "in every month" could be read as 94 percent every month | Correct. The results JSON had lead_applied null for this lens. | The JSON now has lead_validated (null unless all seven criteria hold), lead_proposed and a confidence field set by a stated rule (section 7.1). The record says the lead is a proposal. The slide says "first in 94 percent of outcomes (87 to 97 percent by month)". |
| Medium: the reach figure of 68 percent rests on a convention that is not tested (bottled bases count the sweet-drink habit twice); on a slide it is false precision | Correct. I reproduced the check in the script: with the habit ratio set to 1 for the bottled bases the reach leader becomes sweet-bottled 25 to 44 (0.544, men 45 to 59 0.438) and the per-member leader becomes sweet-bottled 25 to 44 (0.801); the per-person lens is unchanged (0.9405). | Added as sweep `bottled_habit_counted_once` (section 7.8 and limit 12). The slide drops the 68 percent and says no group leads clearly by total reach. |
| Medium: DOPA populations, the odds ratio and internet use are tiered P with no saved page | Correct under the repo rule (a figure whose page is not saved is UNVERIFIED). submission/12 labels the same counts UNVERIFIED. | Relabelled UNVERIFIED (carried) in section 2, in the carried-inputs page and in the figures list. P is kept only for pages saved in T15. |
| Medium: the 1.030 "intent only" ratio is not the sourced gradient alone | Correct. It is the trial-propensity ratio and includes the assumed temperature sensitivity. The age gradient alone gives 1.0295 (0.9985 to 1.0677; 0.9412), which reproduces rework/47 ratio A (1.0409; 0.9979 to 1.0855; 0.9411). | The script now outputs `age_gradient_only_ratio_men25_34_over_35_44` and the 1.030 figure is relabelled "trial propensity including assumed temperature sensitivity" (section 6). |
| Medium: the population range of plus or minus 0.96 percent is narrower than the repo's own alternatives; the age-60 correction of rework/73 and the DDC 7 percent gap are not mentioned | Correct. rework/73 section 5.2 estimates that age 60 is counted in both the 45 to 59 and 60 and over bands (the band is 14,904,550 as held and 13,910,913 after the estimated duplicate is removed, minus 6.7 percent); DDC mid-year men 45 to 59 is 7.13 million against DOPA 6.65 million (plus 7.2 percent). | Two sweeps added: `population_range_wide` (the repo's own alternatives) and `population_pm7_all_bands` (the verifier's check). Reach leader unchanged at 0.678 and 0.648; per person unchanged. Both noted in limits 6 and 13. The primary range is kept so that the headline numbers stay comparable with revision 2. |
| Medium: no temperature-to-demand search was ever executed and logged; "temperature never changes the leader" cannot fail by design | Correct on both counts. Three more search attempts in this revision were refused by the turn's search budget, which is a tool limit and not the usage routing the user dropped. | Search record rewritten as "not searched successfully", with all five logged attempts (T15/temperature_demand_source_search_record.md). The claim is restricted to independent draws within the assumed range. New reverse-stress runs (sensitivity up to 1.00) and directional scenarios (older men more heat-sensitive by 0.01 to 0.05) show what would change the leader (section 7.6). |
| Low: THB 15.00 is the base shelf price, not the planning price | Correct (deck lines 134 and 136: the planning price is THB 9.00 ex-factory, 60 percent of THB 15). | Relabelled in section 2. |
| Low: the count of 49 re-runs includes the primary form and omits the weight sweep | Correct. | The script computes the count: 3 other model forms, 23 leave-one-out, 12 months, 1 stress, 10 structural sweeps, 4 coverage-weight runs and 2 halves, 55 in all; the primary form is the full run and is not counted. |
| Low: conflicts omitted (submission/11 line 121; the 68.6 label in submission/04 and 01; Mintel wording in deck line 42 and submission/11 line 40) | Correct. | Added to section 9. |
| Low: dependence on the rework/73 band cells, which are being verified | Correct. The results file (last modified 20 October 2026 03:44) is read at run time and its modification time is written to the results JSON. | Re-run T15 if the T10 verification changes those band cells (about 40 seconds). Stated in section 8, limit 3. |

Revision 2 (the earlier verification) had replaced the symmetric placebo by a full-model permutation placebo, added the three lenses with stated denominators, the sourced sex gradient (NSO 2021 Table 2), the rework/73 band cells in place of an interpolation, a real tornado with a flip rule and the 0.90 bar for every run. Those changes stand.

## 2. Sources read or carried (tiers and status)

Read date 20 October 2026 unless stated. Under the repo rule a figure whose page is not saved is UNVERIFIED; carried inputs are therefore tiered UNVERIFIED here and show the originating tier in brackets.

| Input | Value used | Source | Tier, status |
|---|---|---|---|
| Bangkok monthly mean temperature, 1991 to 2020 (station 48455) | Jan 27.4, Feb 28.6, Mar 29.7, Apr 30.7, May 30.3, Jun 29.7, Jul 29.2, Aug 29.0, Sep 28.6, Oct 28.4, Nov 28.4, Dec 27.3; annual 28.9 Celsius | TMD, Climatological Data of Thailand 1991 to 2020, PDF p. 57 (https://ubonmet.tmd.go.th/files/MetInfo/climate_normal.pdf; saved: [T15/tmd_bangkok_monthly_mean_1991_2020.md](raw/diligence_2026-10-20/T15/tmd_bangkok_monthly_mean_1991_2020.md)) | P, SOURCED (values). The mapping to demand: ASSUMPTION (no source searched for successfully; see the search record) |
| Mintel share willing to switch to salt or sugar substitutes | 27 percent (range 20 to 35, ASSUMPTION) | Mintel press release, 16 February 2026 (https://www.mintel.com/press-centre/thai-consumers-take-a-more-balanced-and-practical-approach-to-reducing-sugar/; saved: [T15/mintel_press_2026-02-16_sugar_reduction.md](raw/diligence_2026-10-20/T15/mintel_press_2026-02-16_sugar_reduction.md)) | S, SOURCED for the figure only (secondary). Sample size, base and fieldwork dates are not on the page |
| Current drinking, men 25 to 44 / 45 to 59; women 25 to 44 / 45 to 59 | 68.6 / 65.4; 25.2 / 19.9 percent (both sexes 46.9 and 41.9) | NSO Social Indicators 2025, Table 4.6.2 (https://www.nso.go.th/public/e-book/Indicators-Social/Social-Indicators-2025/284/; saved: [T15/nso_si2025_table_4_6_2_drinking_2024.md](raw/diligence_2026-10-20/T15/nso_si2025_table_4_6_2_drinking_2024.md)) | P, SOURCED with limits. The title lists five Thai survey years (six in English) but only three values are printed per row; the assignment of the third value to 2024 is inferred; page image not checked. The 2021 column (58.1, 54.6, 15.2, 12.2) is used in a sweep |
| Everyday sweet bottled non-alcoholic drinks, 2021, 25 to 44 / 45 to 59 (both sexes) | 18.2 / 16.0 percent | NSO Health Behaviour of Population Survey 2021, Table 20, printed p. 41 (uploaded report SD10_04_114; extract [raw/nso2021_SD10_04_114_extract.md](raw/nso2021_SD10_04_114_extract.md); saved rows [T15/nso2021_table20_22_printed_rows.md](raw/diligence_2026-10-20/T15/nso2021_table20_22_printed_rows.md)) | P, SOURCED. The Table 20 title does not say "sweet"; the section narrative and Table 2 do (noted in the saved page). No sex split in Table 20 |
| Sex gradient of sweet-drink habit | men 23.3, women 14.7, all 18.9 percent (5 or more days a week, ages 6 and over); men's factor 1.233, range 1.10 to 1.35 | NSO 2021 Table 2, printed p. 12 (saved: [T15/nso2021_table2_sweet_beverage_5plus_days_by_sex.md](raw/diligence_2026-10-20/T15/nso2021_table2_sweet_beverage_5plus_days_by_sex.md)) | P, SOURCED for the three percentages (checked against Table 20). Applying them as a factor on the everyday band shares is DERIVED; the range is an ASSUMPTION |
| Potassium-caution coverage, narrow group, percent of the group (low / mode / high) | men 25 to 34: 0.14 / 1.07 / 5.52; men 35 to 44: 1.12 / 3.08 / 9.26; men 45 to 59: 4.26 / 8.28 / 20.54; both sexes 25 to 34: 0.20 / 1.15 / 4.45; 35 to 44: 1.12 / 3.09 / 6.94; 45 to 59: 4.26 / 7.58 / 20.23; adults 25 to 59: 2.19 / 4.45 / 11.88 | `screen/t10_potassium_cover_results.json` (rework/73 results, read at run time, file last modified 20 October 2026 03:44; saved: [T15/potassium_coverage_band_cells_rework73.md](raw/diligence_2026-10-20/T15/potassium_coverage_band_cells_rework73.md)) | DERIVED (team model with PROXY inputs). Not a survey cell. Women use the both-sex band cells (PROXY) |
| Age odds ratio per year, daily sweet-drink consumption (2021) | 0.996 (0.991 to 1.001) | rework/47 section 2 (carried; submission/01 line 30 says "table not located") | UNVERIFIED (carried; originating tier P). Not in the saved extract. It drives the whole age-gradient margin |
| DOPA population, men 25 to 34 / 35 to 44 / 45 to 59 (November B.E. 2568) | 4.76 / 4.75 / 6.65 million; both sexes 9.384, 9.407, 14.905 million; women derived as both sexes minus men | rework/47 section 6; rework/screen/segment_potency_mc.py (carried) | UNVERIFIED (carried; originating tier P). Range plus or minus 0.96 percent in the primary run. DOPA bands are ages 26 to 35, 36 to 45 and 46 to 60. Alternatives for the sweep: DDC mid-year men 4.71 / 4.65 / 7.13 million (UNVERIFIED in submission/12), and the rework/73 age-60 correction (13,910,913 for the 45 to 59 band; DERIVED, ASSUMPTION) |
| Internet use by band; online channel share | 96.1 to 99.2 percent; 0.1 to 0.5 | rework/screen/segment_potency_mc.py (carried) | UNVERIFIED (carried; originating tier P) for internet use; ASSUMPTION for the channel share |
| Contribution per cube | range THB 3.6 to 6.8; centre THB 4.91 | rework/55 section 5 (range); deck/deck_content.md (centre) | Team range and desk value, carried (DERIVED) |
| Repeat rate; top-2-box baseline and intent elasticity | 15 to 40 percent (mode 30); 20 to 50 percent and 0.5 to 1.0 | rework/55; rework/49 | ASSUMPTION |
| Base shelf price; listing-parity shelf price | THB 15.00 (assumption); THB 13.80 | deck/submission 11 (the planning price in the deck is THB 9.00 ex-factory, 60 percent of THB 15); rework/70 (mean of four listings, from 68d) | ASSUMPTION (team decision); S, DERIVED mean. Used only in the price factor, common to all bases |

Bases that cannot be measured (stated limits, not ranked):

- **Singha soda and drinking water buyers:** no Singha sales, share or panel data exists in the public record (rework/43 section 4). Proxied by sweet bottled non-alcoholic drinkers, all brands (NSO 2021).
- **Singha beer drinkers:** proxied by all current drinkers of alcohol by sex and age band. No Singha beer share is sourced.
- **Buyers of the Singha Lemon Soda can:** none exist as a profile; the evidence of their profile is that no buyer profile is published (rework/43, rework/69). Not ranked.
- **Heavy modern-trade shoppers:** no Thai channel share was found (rework/55 section 7). Not ranked.

## 3. Candidate bases and the potency decomposition

Each base is a set of people. Singha's own share of any base is unobserved.

Reach (persons) = population x penetration x channel factor. Potency (THB million, model scale) = Reach x T x R x C x (1 - X), with T trial propensity, R repeat rate, C contribution per cube and X the exclusion share. Penetration is current drinking (drinker bases), everyday sweet-bottled share (bottled bases) or the Mintel share (pool).

Trial propensity T = B x rho^e (power link), where B is the top-2-box baseline of the comparison cell (men 35 to 44) and rho is the base's sweet-drink habit over that cell. The linear link replaces rho^e with 1 + e x (rho - 1). The odds scale applies the same ratio to the odds of B. Both links are ASSUMPTIONS (rework/49). The habit of each cell is the printed 2021 band share, adjusted by the age odds ratio (25 to 34 uses OR^(29.5 - 34.5), 35 to 44 uses OR^(39.5 - 34.5), 45 to 59 the printed value) and by the sex gradient (men multiplied by 1.233; women by a factor that keeps the band's both-sex share unchanged). No sex-by-age interaction is modelled.

Convention for the bottled bases (not a sourced choice): a bottled base counts the sweet-drink habit twice, once as penetration (the share who drink sweet bottled drinks every day) and once as the habit ratio in trial propensity (about 0.83 against men 35 to 44). The sweep `bottled_habit_counted_once` sets that ratio to 1 and shows that the reach and per-member leaders depend on it (section 7.8). The per-person lens over the drinker cells does not use it.

Exclusion X: for drinker bases the potassium-caution coverage combined with an alcohol-cue exclusion (ASSUMPTION 0 to 20 percent, mode 5; no source; the team does not check the cue, rework/50 gate G1); for bottled buyers and the pool, potassium coverage only.

Lenses (all from the same draws):

- **Reach:** potency as defined, ranked over the eight existing bases.
- **Per person in the age-sex cell:** reach divided by the population of the cell. This is the conversion lens of rework/46 and 47. It is like-for-like among the six drinker cells, so the formal ranking is over those six; a version over all eight is shown to expose the denominator problem (penetration is inside the quantity and differs by base type).
- **Per member of the base:** reach divided by population times penetration, comparable across base types.

| Base | Definition | Penetration (source) | Exclusion (source tier) |
|---|---|---|---|
| M25 | Men 25 to 34, current drinkers | 68.6 percent (NSO 2024) | potassium 1.07 percent mode (rework/73 cell); alcohol cue |
| M35 | Men 35 to 44, current drinkers (comparison cell) | 68.6 percent (NSO 2024; shared 25 to 44 cell) | potassium 3.08 percent mode (rework/73 cell); alcohol cue |
| M45 | Men 45 to 59, current drinkers | 65.4 percent (NSO 2024) | potassium 8.28 percent mode (rework/73 cell); alcohol cue |
| W25, W35, W45 | Women 25 to 34, 35 to 44, 45 to 59, current drinkers | 25.2, 25.2, 19.9 percent (NSO 2024) | both-sex band cells (PROXY); alcohol cue |
| SB25 | Sweet-bottled drinkers, both sexes 25 to 44, every day (soda and water proxy) | 18.2 percent (NSO 2021 Table 20) | both-sex cells 25 to 34 and 35 to 44 (PROXY); no alcohol cue |
| SB45 | Sweet-bottled drinkers, both sexes 45 to 59, every day | 16.0 percent (NSO 2021) | both-sex cell 45 to 59 (PROXY) |
| POOL | Sugar-reduction pool (market, not a Singha base) | 27 percent (Mintel, S; range 20 to 35 ASSUMPTION) of adults 25 to 59 | adults 25 to 59 (PROXY); habit mapping k log-uniform 0.5 to 2 (ASSUMPTION) |

Common factors (repeat, contribution, price level and elasticity, B, e in the base case) scale every base alike and cannot change the order by themselves.

## 4. Ambient variation design

- **Draws:** 40,000 (two halves of 20,000), one seed (20261020) and one draw order, so each run differs only where a factor is changed.
- **Input ranges:** every factor in section 3 is drawn from its stated range: population gap uniform plus or minus 0.96 percent per band (carried, UNVERIFIED); drinking shares plus or minus 3 points (ASSUMPTION); sweet shares plus or minus 2 points (ASSUMPTION); odds ratio log-normal from the carried interval; men's sex factor uniform 1.10 to 1.35; each potassium cell an independent triangular (low, mode, high); alcohol cue triangular 0, 5, 20 percent; pool share triangular 20, 27, 35 percent; habit mapping log-uniform 0.5 to 2; B uniform 20 to 50 percent; e uniform 0.5 to 1.0; R triangular 15, 30, 40 percent; C uniform THB 3.6 to 6.8; channel share uniform 10 to 50 percent; shelf price THB 13.80 or 15.00 with elasticity uniform minus 1.5 to minus 0.5.
- **Ambient temperature:** the month is drawn uniformly from the twelve TMD monthly means (27.3 to 30.7 Celsius). Each base has its own season sensitivity beta, uniform 0 to 0.05 per degree Celsius (ASSUMPTION; base case 0.025), applied as exp(beta x (month mean minus 28.9)) to trial propensity. Beta is drawn separately for each base: a common temperature effect on every base could not change any ranking. At the stress setting (beta up to 0.15) the seasonal effect reaches roughly plus 30 percent in April and minus 20 percent in January. Two further designs go beyond the assumed range: reverse-stress runs with beta up to 0.30, 0.45, 0.60 and 1.00, and directional scenarios in which men 35 to 44 and 45 to 59 have a fixed sensitivity higher than men 25 to 34 by 0.01 to 0.05 per degree Celsius (section 7.6).
- **Base case:** every factor at its mode. Leave-one-factor-out runs fix one input group (23 groups) at its sample mean and redraw the rest, so the change isolates that group's spread.
- **Rank stability:** Kendall tau between each draw's ranking and the base-case ranking, and a tornado: for each input group, the first-place probability of the lens leader in the highest fifth of the input minus the lowest fifth.

## 5. Results by lens (40,000 draws)

Reach lens, THB million model scale (median; 5th to 95th percentile; first-place probability). Base case: men 45 to 59 1.785, men 25 to 34 1.626, men 35 to 44 1.540, sweet-bottled 25 to 44 1.492, sweet-bottled 45 to 59 0.887, women 45 to 59 0.497, women 25 to 34 0.404, women 35 to 44 0.387.

| Base | Median | 5th to 95th | P(first) |
|---|---|---|---|
| Men 45 to 59 drinkers | 1.655 | 0.838 to 3.004 | 0.681 |
| Men 25 to 34 drinkers | 1.537 | 0.787 to 2.743 | 0.130 |
| Sweet-bottled 25 to 44 | 1.476 | 0.754 to 2.662 | 0.185 |
| Men 35 to 44 drinkers | 1.451 | 0.744 to 2.589 | 0.004 |
| Sweet-bottled 45 to 59 | 0.851 | 0.420 to 1.594 | 0.000 |
| Women 45 to 59 | 0.461 | 0.225 to 0.881 | 0.000 |
| Women 25 to 34 | 0.385 | 0.191 to 0.727 | 0.000 |
| Women 35 to 44 | 0.370 | 0.183 to 0.696 | 0.000 |

Rank stability, reach lens: mean Kendall tau against the base-case order 0.871; the full ranking is identical to the base case in 28.9 percent of draws. Men 45 to 59 are in the top two in 84.2 percent of draws, men 25 to 34 in 70.4 percent and sweet-bottled drinkers 25 to 44 in 39.2 percent, so the order of the leaders is weakly identified. These reach figures depend on the conventions in section 3 (bottled habit counted twice) and on the population range (limit 13).

Per person in the age-sex cell, drinker cells (model scale, THB million per person in the cell): men 25 to 34 0.323 (0.165 to 0.577), men 35 to 44 0.305 (0.157 to 0.546), men 45 to 59 0.249 (0.126 to 0.452), women 25 to 34 0.083, women 35 to 44 0.079, women 45 to 59 0.056. First-place probability: men 25 to 34 0.9405, men 35 to 44 0.0583, men 45 to 59 0.0012; top two: men 25 to 34 in 99.98 percent of draws and men 35 to 44 in 98.7 percent. Kendall tau 0.981 (identical ranking in 87.3 percent of draws). Over all eight existing bases with the same denominator, sweet-bottled drinkers 25 to 44 (0.079) and 45 to 59 (0.057) fall far below the men's cells, which is mostly the denominator: the cell includes everyone, and only 18.2 and 16.0 percent of them are sweet-bottled drinkers.

Per member of the base (model scale): men 25 to 34 0.471 (0.241 to 0.840), men 35 to 44 0.445, sweet-bottled 25 to 44 0.433 (0.223 to 0.770), men 45 to 59 0.380, sweet-bottled 45 to 59 0.358, women 25 to 34 0.331, women 35 to 44 0.315, women 45 to 59 0.281. First-place probability: men 25 to 34 0.816, sweet-bottled 25 to 44 0.134, men 35 to 44 0.046. Kendall tau 0.860.

Pool (market, reach lens): first among all nine bases in 99.45 percent of draws, about 2.2 times the median of the best existing base. Reported, not used as an answer.

## 6. Ratio checks against rework/46 and rework/47

| Ratio | Median | 5th to 95th | P(above 1) | Touches 1? |
|---|---|---|---|---|
| Men 25 to 34 over 35 to 44, per person in the cell (full model) | 1.057 | 0.997 to 1.123 | 0.9415 | Yes |
| Same, age gradient alone (odds ratio and elasticity only; rests on a source, carried and UNVERIFIED) | 1.0295 | 0.9985 to 1.0677 | 0.9412 | Yes |
| Same, trial propensity including the assumed temperature sensitivity (not a sourced figure) | 1.030 | 0.984 to 1.082 | 0.869 | Yes |
| Same, exclusion only (potassium coverage; the alcohol cue is shared; team model) | 1.022 | 0.989 to 1.064 | 0.859 | Yes |
| Men 45 to 59 over 25 to 34, reach | 1.080 | 0.913 to 1.257 | 0.779 | Yes |
| Men 25 to 34 over 45 to 59, per person in the cell | 1.294 | 1.112 to 1.530 | 0.999 | No |
| rework/47 ratio A, men 25 to 34 over 35 to 44 | 1.0409 | 0.9979 to 1.0855 | 0.9411 | Yes |
| rework/47 ratio B, men 25 to 34 over 45 to 59 | 1.147 | 1.026 to 1.284 | 0.979 | No |

The age-gradient-alone interval runs from 0.9985 to 1.0677 and touches 1 narrowly (its lower end is 0.15 percent below 1). The pairwise bar (probability above 1 of at least 0.90 and a 5th percentile above 1) is passed by neither the age-gradient-only ratio nor the full-model ratio (results JSON, decision.pair_men25_34_over_35_44_*).

What validates and what does not:

- **Validates:** the direction and size of men 25 to 34 over men 35 to 44. The age-gradient ratio (1.0295) reproduces rework/47 ratio A (1.0409) with the same probability above 1 (0.941), as it should, since it uses the same two sourced inputs and the same assumed elasticity range. The full-model ratio (1.057) adds the team-model coverage gradient. All intervals touch 1. Direction is supported (probability above 1 of 0.94 on both measures); separation at 90 percent is not. This agrees with the deck's statement that the interval includes zero.
- **Validates in direction, not in size:** men 25 to 34 over men 45 to 59. T15 gives 1.294 against 1.147 in rework/47. The components (medians, jointly drawn): drinking share 1.049 (rework/47: 1.049, from log 0.0478), channel 1.005, trial propensity 1.114 (rework/47 age gradient 1.094, from log 0.0902), exclusion 1.093. The excess comes from the potassium-caution exclusion (1.093), which rework/46 and 47 did not model, and from a steeper age gradient in the printed 2021 band shares (18.2 and 16.0) than in the adjusted odds ratio extrapolation. The alcohol cue is common to both drinker cells and cancels.
- **Does not validate:** any claim that the per-person lead is sourced. The margin over men 35 to 44 rests on the sweet-drink age gradient (an odds ratio that is carried and UNVERIFIED, with an interval that includes 1) and on a team-model coverage gradient (1.12 / 3.08 / 9.26 against 0.14 / 1.07 / 5.52). Remove the coverage gradient and the first-place probability is 0.882 (section 7.8).

## 7. Validation

### 7.1 Criteria and the words used (fixed before the run, except where stated)

- c1: first-place probability of the leader at least 0.90 in the full run.
- c2: same leader in both halves, each at least 0.90.
- c3: same leader in all four model forms, each at least 0.90.
- c4: same leader and at least 0.90 in every leave-one-factor-out run (23 groups).
- c5: same leader and at least 0.90 in each of the twelve months and in the season stress run (beta up to 0.15).
- c6: permutation placebo: the mean first-place probability of the leader's label, over 200 permutations of the sourced inputs across labels, is at most 1.5 times chance.
- c7: structural sweeps: same leader and at least 0.90 in each of ten sweeps (interpolation weight uniform 0 to 1 for men 35 to 44 coverage; men 35 to 44 coverage equal to men 25 to 34; fully correlated coverage; no sex gradient; alcohol cue 0; alcohol cue 20 percent; 2021 drinking cells; and, added in revision 3, bottled habit counted once, population range widened to the repo's alternatives, population plus or minus 7 percent for every band). c7 started with seven sweeps in revision 2 and gained three in revision 3; c1 to c6 were fixed before the first run.

Words used (the grading was written after the first verification; the seven criteria were not changed):

- **Validated:** all seven criteria hold. No lens is validated.
- **Proposed, moderate confidence:** the leader is the same in every re-run and split and c1 holds, so the full run is at least 0.90, but the 0.90 bar is missed in at least one re-run. Moderate describes the ranking among the drinker cells under the stated assumptions, not customers.
- **None (not robust):** the leader changes in any re-run, or c1 fails.

The results JSON carries these as lead_validated (null for every lens), lead_proposed (men 25 to 34 for the per-person lens, null for reach and per member) and confidence (moderate, none, none). The JSON also holds the per-person lens ranked over all eight bases (`per_cell_all`); it is shown only to expose the denominator problem, and its leader and grading equal the drinker-cell lens because the two bottled bases fall far below the men's cells. It is not an additional result.

| Check | Reach | Per person in the cell (drinker cells; same for all eight bases) | Per member |
|---|---|---|---|
| Leader (full run) and P | men 45 to 59, 0.681 | men 25 to 34, 0.941 | men 25 to 34, 0.816 |
| c1 | Fail | Pass | Fail |
| c2 halves | Fail: leader men 45 to 59 in both (0.678, 0.684) but below 0.90 | Pass: 0.939 and 0.942 | Fail: 0.813 and 0.818 |
| c3 forms (share-power, odds-power, share-linear, odds-linear) | Fail: leader men 45 to 59 in all four (0.681, 0.746, 0.684, 0.747), below 0.90 | Pass: 0.941, 0.944, 0.941, 0.944 | Fail: leader men 25 to 34 in all four (0.816, 0.638, 0.810, 0.629) |
| c4 leave-one-out | Fail: leader unchanged in all 23, P 0.681 to 0.743 | Pass: leader unchanged, P 0.941 to 0.973 | Fail: leader unchanged, P 0.816 to 0.885 |
| c5 months and stress | Fail: leader unchanged; months 0.668 to 0.687, stress 0.643 | Fail: leader unchanged; months 0.871 to 0.973 (April 0.871, December 0.895 below 0.90), stress 0.834 | Fail: leader unchanged; months 0.747 to 0.847, stress 0.709 |
| c6 permutation placebo (mean permuted P; threshold) | Pass: 0.090; 0.188 | Pass: 0.177; 0.250 | Pass: 0.094; 0.188 |
| c7 sweeps | Fail: leader changes to sweet-bottled 25 to 44 in four sweeps | Fail: leader unchanged in all ten; P below 0.90 in one (0.882) | Fail: leader changes to sweet-bottled 25 to 44 in three sweeps |
| **Status** | **None (not robust)** | **Leader unchanged in all 55 re-runs and splits; the 0.90 bar is met in c1 to c4 and c6, missed in c5 and c7 (four runs). Proposed, moderate confidence; not validated** | **None (not robust)** |

Run counts (computed by the script, results JSON run_counts): 3 other model forms (the primary form is the full run and is not counted), 23 leave-one-out, 12 months, 1 season stress, 10 structural sweeps, 4 coverage-weight sweep runs and 2 halves, 55 in all. The four temperature reverse-stress runs and the directional scenarios are outside the assumed range and are not counted.

### 7.2 Split check

Two disjoint halves (draws 1 to 20,000 and 20,001 to 40,000). All three lenses have the same leader in both halves, and the median orders of the two halves agree exactly (Kendall 1.0 between them). Reach: 0.678 and 0.684 for men 45 to 59. Per person in the cell: 0.939 and 0.942 for men 25 to 34. Per member: 0.813 and 0.818.

### 7.3 Model forms

Four forms: multiplicative (power) or additive (linear) intent link, on the share or the odds scale (the first is the primary). Reach: men 45 to 59 lead in all four. Per person in the cell: men 25 to 34 in all four. Per member: men 25 to 34 in all four, but on the odds scale their first-place probability falls to 0.638 and 0.629 and sweet-bottled drinkers 25 to 44 rise to 0.327 and 0.338.

### 7.4 Leave-one-factor-out (each input group fixed at its sample mean)

Per person in the cell: no group changes the leader. The first-place probability rises when a group's spread is removed (none fell below the full-run value of 0.941): fixing the age odds ratio gives 0.966, potassium coverage for men 35 to 44 gives 0.960, for men 25 to 34 gives 0.953, ambient temperature (month and sensitivities) gives 0.973. Reach: no group changes the leader; the largest changes are sweet-bottled share 25 to 44 (+0.062), sweet-bottled share 45 to 59 (+0.029), alcohol cue (+0.015), men 45 to 59 coverage (+0.014) and the sex gradient (+0.014). Per member: the alcohol cue is the largest (+0.070, to 0.885).

### 7.5 Tornado (highest fifth minus lowest fifth of each input; first-place probability of the lens leader, in points)

Flip rule: the top base differs between the lowest and highest fifth and the swing is at least 2 points.

- **Reach** (leader men 45 to 59): sweet-bottled share 25 to 44 minus 64.7 (the only input that flips the top base: in the highest fifth sweet-bottled drinkers 25 to 44 lead); sweet-bottled share 45 to 59 plus 47.6; coverage men 45 to 59 minus 34.1; drinking share men 45 to 59 plus 21.4; alcohol cue minus 19.1; men's sex factor plus 15.3; intent elasticity minus 12.3; drinking share men 25 to 44 minus 11.3. All others under 5 points.
- **Per person in the cell** (leader men 25 to 34): age odds ratio minus 16.5; coverage men 35 to 44 plus 13.3; coverage men 25 to 34 minus 11.8; intent elasticity plus 2.2; all others under 2 points. No input flips the top base. Ambient temperature swings it by minus 1.6 points between its highest and lowest fifth.
- **Per member** (leader men 25 to 34): alcohol cue minus 41.1; men's sex factor plus 28.6; intent elasticity plus 20.1; age odds ratio minus 19.7; coverage men 25 to 34 minus 17.2; coverage men 35 to 44 plus 10.5. No quintile flips the top base, but three structural sweeps do (section 7.8).

### 7.6 Ambient temperature

**Within the assumed range, independent draws.** Reach: the leader (men 45 to 59) is the same in all twelve months, probability 0.668 (April) to 0.687 (February, September). Per person in the cell: men 25 to 34 first in every month; probability by month: January 0.902, February 0.971, March 0.949, April 0.871, May 0.906, June 0.949, July 0.970, August 0.973, September 0.971, October 0.966, November 0.966, December 0.895. The probability is lowest at the temperature extremes (April 30.7, December 27.3, January 27.4) because the assumed per-base sensitivities then differ most in effect. Per member: 0.747 (April) to 0.847 (August). Season stress (beta up to 0.15): reach 0.643, per person in the cell 0.834, per member 0.709; the leader is unchanged on all lenses.

**Reverse stress, independent draws with the range widened (beta up to 0.30, 0.45, 0.60, 1.00 per degree Celsius, which is 6 to 20 times the assumed maximum).** The leader is unchanged on every lens at every setting; the per-person leader's first-place probability falls to 0.737, 0.672, 0.628 and 0.570. This shows that independent sensitivities cannot change the modal leader however large they are: they add noise with no direction. It is a property of the design, not a finding about customers.

**Directional scenarios (an ASSUMPTION; no source gives a direction).** Men 25 to 34 are given a sensitivity of 0 and men 35 to 44 and men 45 to 59 a higher fixed sensitivity by delta per degree Celsius; the other bases keep their independent draws. Per person in the cell, drinker cells:

| Delta (per degree Celsius) | April: leader and P(men 25 to 34 first) | Twelve-month mixture: leader and P(men 25 to 34 first) |
|---|---|---|
| 0 | men 25 to 34, 0.973 | men 25 to 34, 0.973 |
| 0.01 | men 25 to 34, 0.896 | men 25 to 34, 0.964 |
| 0.02 | men 25 to 34, 0.732 | men 25 to 34, 0.937 |
| 0.03 | men 25 to 34, 0.505 | men 25 to 34, 0.896 |
| 0.04 | **men 35 to 44**, 0.283 | men 25 to 34, 0.849 |
| 0.05 | **men 35 to 44**, 0.128 | men 25 to 34, 0.804 |

By month at delta 0.05 the leader is men 35 to 44 in April (0.128) and May (0.305), and men 25 to 34 in the other months (March and June 0.686, January and December 1.000). At delta 0.03 men 25 to 34 lead in every month (April 0.505, May 0.661). The reach and per-member leaders do not change in these scenarios except that the per-member leader also moves to men 35 to 44 in April at 0.04 and above; the reach leader stays men 45 to 59.

So the statement that temperature does not change a leader is conditional. It holds for independent sensitivities at any size and for a twelve-month mixture. It fails for the hottest months if men 35 to 44 respond to heat more strongly than men 25 to 34 by about 0.04 per degree Celsius or more, a difference inside the assumed 0 to 0.05 range. The reverse direction (younger men more heat-sensitive) can only strengthen the lead. Settling the direction needs a source (section 8, item 8).

### 7.7 Placebo (full-model permutation)

The sourced inputs (population, penetration, sweet-drink habit, potassium coverage) were shuffled across the eight existing base labels, each input independently, 200 times; shared factors, the alcohol cue, the season sensitivities and the channel factor stayed with their labels; all lenses were recomputed.

- What it shows: the leader's result depends on its actual inputs. The mean first-place probability of the real leader's label falls to 0.090 on reach (chance 0.125), 0.177 per person in the cell (chance 0.167) and 0.094 per member. The permuted median order is unrelated to the real one (mean Kendall tau 0.017, 0.003 and 0.040). The observed probability exceeded the permuted value in 92.5 percent (reach), 91.0 percent (per person in the cell) and 97.5 percent (per member) of permutations. This is a check that no label-specific code structure creates the leader; it cannot fail by symmetry in the other direction.
- What it does not show: that a first-place probability of 0.90 is hard to reach. Under random assignment of these inputs some base reached 0.90 in 77.0 percent of permutations on reach, 68.5 percent per person in the cell and 24.0 percent per member. The probability measures how large the gaps between bases are against the input spread. It is a dominance measure under the stated ranges, not statistical evidence about customers.
- A second check gives every label the same sourced inputs (those of men 35 to 44), leaving only label structure. Among the drinker cells, men 25 to 34 and women 25 to 34 lead in 26.5 and 26.1 percent of draws against 16.7 percent chance, men 35 to 44 and women 35 to 44 in 16.0 percent, men 45 to 59 and women 45 to 59 in 7.8 and 7.7 percent. The only label-specific sourced input left is internet use by band (99.05, 98.45, 97.15 percent, carried and UNVERIFIED), which gives the younger bands a small edge in the channel factor (men 25 to 34 over men 45 to 59: 1.005). Across all eight bases, the two bottled bases win (65.4 and 32.0 percent) because they carry no alcohol cue.

### 7.8 Structural sweeps (c7): the assumptions the lead depends on

| Sweep | Reach: leader and P | Per person in the cell: leader and P | Per member: leader and P |
|---|---|---|---|
| Men 35 to 44 coverage by interpolation, weight uniform 0 to 1 | men 45 to 59, 0.682 | men 25 to 34, 0.975 | men 25 to 34, 0.841 |
| Men 35 to 44 coverage equal to men 25 to 34 (no coverage gradient) | men 45 to 59, 0.679 | men 25 to 34, **0.882** | men 25 to 34, 0.769 |
| All coverage cells move together | men 45 to 59, 0.690 | men 25 to 34, 0.969 | men 25 to 34, 0.842 |
| No sex gradient (the earlier model) | **sweet-bottled 25 to 44, 0.583** (men 45 to 59 0.404) | men 25 to 34, 0.941 | **sweet-bottled 25 to 44, 0.849** (men 25 to 34 0.067) |
| Alcohol cue 0 | men 45 to 59, 0.767 | men 25 to 34, 0.941 | men 25 to 34, 0.939 |
| Alcohol cue 20 percent | **sweet-bottled 25 to 44, 0.544** (men 45 to 59 0.431) | men 25 to 34, 0.941 | **sweet-bottled 25 to 44, 0.779** (men 25 to 34 0.207) |
| 2021 drinking cells (year-matched to the sweet-drink data) | **sweet-bottled 25 to 44, 0.649** (men 45 to 59 0.325) | men 25 to 34, 0.941 | men 25 to 34, 0.816 |
| Bottled habit counted once (habit ratio of the bottled bases set to 1) | **sweet-bottled 25 to 44, 0.544** (men 45 to 59 0.438) | men 25 to 34, 0.941 | **sweet-bottled 25 to 44, 0.801** (men 25 to 34 0.187) |
| Population range widened to the repo's alternatives (plus or minus 2.2 percent for ages 25 to 44; minus 6.7 to plus 7.2 percent for 45 to 59) | men 45 to 59, 0.678 | men 25 to 34, 0.941 | men 25 to 34, 0.816 |
| Population plus or minus 7 percent for every band | men 45 to 59, 0.648 | men 25 to 34, 0.941 | men 25 to 34, 0.816 |

Fixed interpolation weights for men 35 to 44 coverage (weight on the men 25 to 34 cell; per person in the cell, probability that men 25 to 34 lead): 0.0 gives 0.996, 0.25 gives 0.993, 0.5 gives 0.987, 0.75 gives 0.964, 1.0 (no gradient) gives 0.882. The rework/73 band cell sits at an implied weight of about 0.72. The per-person lead needs a coverage gradient of at least a modest size to stay above 0.90 in the full model; the gradient is a team-model result with PROXY inputs.

The sex gradient, the alcohol cue, the year of the drinking data and the convention for the bottled habit decide the reach and per-member rankings against sweet-bottled drinkers. None of them changes the per-person ranking among drinker cells, because they are common to the drinker cells (or, for the bottled convention, do not enter them). The population sweeps leave the per-person lens exactly unchanged, because the cell population divides out.

## 8. Stated limits

1. No Singha sales, share, panel or buyer data exists in the public record. Every base is a market-pool proxy, and Singha's share of each is unobserved.
2. No source gives trial intent for any base. The top-2-box baseline (20 to 50 percent) and the intent elasticity (0.5 to 1.0) are ASSUMPTIONS. They are common to all bases and cannot by themselves change a ranking, but they set the size of the gaps; the elasticity moves the per-person leader's probability by about 2 points and the per-member leader's by about 20.
3. Potassium-caution coverage is the rework/73 team model (DERIVED, with PROXY inputs: a hospital sample for the ACE inhibitor and ARB share, an assumed young-adult treated share). It is not a survey cell, and women, bottled buyers and the pool use the both-sex band cells (PROXY). The cells share assumptions in truth; the primary run draws them independently (conservative for rankings) and a sweep draws them together. The coverage gradient between men 25 to 34 and men 35 to 44 decides whether the per-person lead stays above 0.90 (0.882 without it). The cells are read from the T10 results file at run time (file last modified 20 October 2026 03:44, recorded in the results JSON); T15 must be re-run if the verification of rework/73 changes the band cells.
4. The alcohol-cue exclusion (0 to 20 percent) has no source. The team does not check the cue (gate G1). It cancels among drinker cells but decides the ranking between drinker and bottled bases (swing of 41 points on the per-member lens).
5. The 2024 drinking cells come from a garbled text layer. The title lists five survey years (six in English) and only three values are printed per row, so the assignment of the third value to 2024 is inferred, and the printed page image was not checked. A series break is recorded in rework/47: the 2017 release defines past-year drinking and the 2024 definition is inferred (men's current drinking 56.6 in 2015, 47.5 in 2017, 55.7 in 2024), so the 2021 to 2024 jump for men 25 to 44 (58.1 to 68.6) may include a definition change. The year-matched sweep with the 2021 drinking column changes the reach leader to sweet-bottled drinkers 25 to 44.
6. Drinking shares are 2024 values and sweet-drink shares are 2021 values; the model combines them without a common year. The 2021 sweet-drink odds ratio, the DOPA counts and the internet shares are carried and UNVERIFIED (pages not saved). DOPA age bands are ages 26 to 35, 36 to 45 and 46 to 60.
7. The sweet-drink sex gradient is from ages 6 and over at 5 or more days a week, applied to everyday shares at ages 25 to 59 without a sex-by-age interaction (NSO 2021 has no sex-by-band table). Its range (1.10 to 1.35) is an ASSUMPTION; the rework/47 figures (20.6 and 12.5 percent) are UNVERIFIED and are used only as a cross-reference.
8. Temperature. The TMD values are 1991 to 2020 normals, not 2026 observations. A temperature-to-demand source was not searched for successfully: five search attempts (two in revision 2, three in revision 3) were refused by the turn's web search budget, and the first run's searches were not logged, so no search result was read (`T15/temperature_demand_source_search_record.md`). "Not found" would be wrong here: it is "not searched". The sensitivity (0 to 0.05 per degree Celsius per base, stress 0.15) is an ASSUMPTION. The statement that temperature does not change a leader holds for independent sensitivities and for the twelve-month mixture only; section 7.6 shows that a systematic difference of 0.04 per degree Celsius or more between men 35 to 44 and men 25 to 34 changes the April per-person leader. What would settle it: a Thai monthly beverage sales or production series matched to the TMD means, or a published weather-sales elasticity for carbonated drinks in a tropical market, read in full. The search can be run in a new turn with a fresh search budget.
9. The Mintel 27 percent has no stated sample, base or fieldwork date (S, SOURCED for the figure only; secondary).
10. The sweet-drink series is a PROXY for sugar-sweetened drinking. The cube uses an intense sweetener (rework/49 section 6), so the age transfer is untested. The Table 20 title does not say "sweet"; the narrative and Table 2 do.
11. The first-place probabilities are model probabilities under stated ranges. They are not sampling probabilities or purchase probabilities, and random assignment of the same inputs gives a first-place probability of at least 0.90 in 24 to 77 percent of permutations (section 7.7). Nothing here is a consumer finding.
12. Convention: the bottled bases carry the sweet-drink habit twice (as penetration and as the habit ratio). This is a modelling choice with no source. With the habit counted once, the reach and per-member leaders change to sweet-bottled drinkers 25 to 44 (section 7.8). The reach figures, including 68 percent for men 45 to 59, are therefore not quoted on the slide.
13. Population. The primary range (plus or minus 0.96 percent, carried) is narrower than the repo's own alternatives: DDC mid-year men 45 to 59 is 7.13 million against 6.65 million (plus 7.2 percent; UNVERIFIED in submission/12), and rework/73 section 5.2 estimates that age 60 is counted in both the 45 to 59 and 60 and over bands (the held 45 to 59 band, ages 46 to 60, is 14,904,550 and would be 13,910,913 without the duplicate; an equal-thirds ASSUMPTION). Women's population is derived as both sexes minus men and inherits any mismatch between the two series. Two sweeps use the wider ranges; the reach leader stays men 45 to 59 (0.678 and 0.648) and the per-person lens does not change.

## 9. Conflicts with current text (for the lead)

- **Ratio B, men 25 to 34 over men 45 to 59.** submission/04_strategy.md line 14 and submission/12_concept_survey_plan.md line 134 (and the proposal copies) quote 1.15 (90 percent interval 1.03 to 1.28); rework/46 line 35 says men 45 to 59 are about 12 percent below per person. T15's per-person ratio is 1.29 (1.11 to 1.53), so men 45 to 59 are about 23 percent below. Cause by component (medians): drinking share 1.049 and channel 1.005 agree with rework/47; trial propensity 1.114 against the rework/47 age gradient 1.094 (a steeper gradient in the printed 2021 band shares than in the odds-ratio extrapolation); exclusion 1.093, which rework/46 and 47 did not model. The text should say which model it quotes.
- **Ratio A and the margin wording.** submission/12 quotes median 1.04, interval 1.00 to 1.09, probability 0.94. On the age gradient alone T15 gives 1.0295 (0.9985 to 1.0677; 0.9412), which agrees. The full model gives 1.057 (0.997 to 1.123; 0.9415), about 6 percent, because it adds the team-model potassium-caution coverage gradient and assumed temperature noise. submission/01 line 30, submission/10 line 95 and the deck (slide 5) state the gap as 0.6 to 1.2 points at a 30 percent baseline; the age-gradient margin (0.9 points) sits inside that range, the full-model margin (1.7 points) does not. The slide text quotes both measures. Judge-facing lines that quote only the 0.6 to 1.2 points are not wrong but are incomplete next to the new slide.
- **The two 94 percent figures.** submission/01 line 30, submission/02 line 56, submission/06 line 37 and submission/10 (and the proposal copies) say men 25 to 34 lead in about 94 percent of draws. That figure is rework/49 and rework/47: the probability that men 25 to 34 beat men 35 to 44 on the age gradient alone (0.941), pairwise. The T15 figure is the first-place probability among six drinker cells in the full model (0.9405). They are different quantities with nearly the same value. Wherever both appear the basis must be named.
- **Slide 5.** The text in section 11 replaces the current slide 5 of rework/deck/deck_content.md (lines 61 to 73). The Kantar, Innova, Mintel sweetness and category-band bullets and the Lemon Soda no-buyer-profile limit are kept (not re-verified in T15); the lead-segment bullet is rewritten, and two bullets are added.
- **Lead segment and the confirmed band.** submission/11 line 121 recommends keeping the confirmed band (men 27 to 44, Bangkok sample) as the lead and treating men 25 to 34 as a labelled test. The new slide title and submission/10 ("proposed lead segment") name men 25 to 34 as the proposed lead, to be tested. The two readings differ in what is called the lead; the lead should align them.
- **UNVERIFIED labels.** submission/04 line 13 and submission/01 label the 68.6 and 65.4 drinking shares "P, UNVERIFIED" and submission/12 says the NSO 2024 table could not be read reliably. T15 read the rows twice (68.6, 65.4, 25.2, 19.9); the year assignment is inferred (three values for five or six listed years). Status: SOURCED with limits. The 2021 daily bottled-drink shares labelled UNVERIFIED in submission/01 can be upgraded to SOURCED (P) for the two cells read (Table 20: 18.2 for 25 to 44; 16.0 for 45 to 59). In the other direction, the DOPA counts, the odds ratio and internet use that T15 first tiered P are UNVERIFIED (not re-read).
- **Sex split.** The statement that no sex split exists is no longer true for the 5-or-more-days-a-week measure: NSO 2021 Table 2 gives men 23.3 and women 14.7 percent (saved page). The sex-by-band cross-tabulation still does not exist.
- **Mintel wording.** deck/deck_content.md line 42, submission/11 line 40 and rework/proposal/11 say "open to sugar or salt alternatives"; the Mintel page says "willing to switch to salt or sugar substitutes". The new slide 5 uses the Mintel wording. The figure (27 percent) is the same; the set should use one wording.
- **rework/47 section 2.** It records 20.6 and 12.5 percent from a journal (UNVERIFIED); a sourced equivalent now exists (section 2).
- **Reach reading.** rework/46 treats men 45 to 59 as the pended volume segment. T15 shows men 45 to 59 are the most likely reach leader but not robustly: the order against sweet-bottled drinkers 25 to 44 changes with the sex gradient, the alcohol cue, the drinking year and the bottled-habit convention. No judge-facing text claims a reach winner, and the new slide drops the 68 percent.

## 10. Decision and what is applied

1. **Reach (total):** no existing base is named as more potent. Men aged 45 to 59 are the most likely leader under the primary conventions and are consistent with the pended volume segment, but the result is not robust and no figure is quoted on the slide.
2. **Per person in the age-sex cell (conversion):** men aged 25 to 34 who drink alcohol are the proposed lead among the drinker cells, first in 94 percent of draws (87 to 97 percent by month) and the leader in every one of 55 re-runs and splits. The margin over men aged 35 to 44 is about 3 percent on the age gradient alone and about 6 percent in the full model; both intervals include no difference. The first-place probability falls below 0.90 in two months, the season stress run and the no-coverage-gradient sweep. Confidence: moderate, as defined in section 7.1. The lead is a proposal that the pilot tests, not a validated result.
3. **Per member:** men aged 25 to 34 lead in 82 percent of draws but not robustly; sweet-bottled drinkers aged 25 to 44 lead if the sex gradient is removed, the alcohol cue is at the top of its range or the bottled habit is counted once. No per-member claim is made.
4. **Ambient temperature:** no change in any leader within the assumed independent sensitivity range or in the twelve-month mixture; the per-person leader's probability ranges from 0.87 to 0.97 across months. A systematic heat-sensitivity difference of 0.04 per degree Celsius or more between men 35 to 44 and men 25 to 34 would change the April leader; no source gives the direction or size.
5. **Pool and unobserved bases:** the pool ranks first on reach but is a market pool. Lemon Soda can buyers and heavy modern-trade shoppers are not ranked.
6. **Volume (men 45 to 59):** stays pended, as decided in rework/46.

## 11. Slide 5 text (finished; judge-facing; replaces the current slide 5 of the deck content)

Title: Consumers want less sugar without losing taste; men aged 25 to 34 are the proposed lead, to be tested.

On the slide:

- Out of home, often: 90% of urban consumers drink carbonated drinks out of home, more than 22 purchases a year, about THB 19 per trip (Kantar, April 2024, S).
- Taste matters: about two in five consumers name taste as a decision factor for soft drinks (Innova, October 2025, S). Consumers expect taste to match zero sugar (Mintel, February 2026; Coca-Cola Thailand, June 2021; both S).
- Sweetness: 40% prefer full sweetness, 36% less sweet, 24% are undecided; 27% say they are willing to switch to salt or sugar substitutes (Mintel, February 2026, S).
- We compared the customer groups a Singha product would reach, varying every input across its range in 40,000 simulated outcomes, including Bangkok's monthly average temperature (27 to 31 degrees Celsius). No Singha buyer data exists, so every group is a market proxy.
- Compared per person within each age and sex group, men aged 25 to 34 who drink alcohol rank first among the six drinker groups in 94% of simulated outcomes (87% to 97% by month). Their margin over men aged 35 to 44 is about 3% on purchase intent (about 0.9 points at a 30% baseline) and about 6% after the potassium-caution exclusion; both ranges include no difference. The confirmed category band is men aged 27 to 44 (Bangkok sample, n = 400, S).
- By total reach no group leads clearly, and the order depends on how the groups are defined. Men aged 45 to 59 are a later volume segment, pended.
- Limit: no published buyer profile exists for Singha Lemon Soda. The comparison is a model result under stated assumptions, not a consumer finding.

Exhibit: three tiles: 90% | more than 22 purchases a year | about THB 19 per trip (unchanged).

Source line: Kantar, 9 April 2024; Mintel, 16 February 2026; Innova, 31 October 2025; Coca-Cola Thailand, June 2021; Bangkok study, 31 August 2025 (all S). National Statistical Office, Health Behaviour of Population Survey 2021 and Social Indicators 2025 (P). Thai Meteorological Department, climate normals 1991 to 2020 (P). Customer comparison: team model (derived); its population counts and age gradient are carried from earlier team work and not re-read at source (UNVERIFIED).

Speaker note: Present the lead segment as the first thing the pilot tests. Say that the margin over men aged 35 to 44 is small and its range includes no difference, that total reach has no clear leader, and that these are model results under stated assumptions. The model's effect of heat on demand is an assumption; it does not change who leads unless men aged 35 to 44 are assumed to respond to heat more strongly than men aged 25 to 34 by a wide margin.

## 12. Verification

- The script ran to completion (exit 0), 40,000 draws, fixed seeds, 191 MB peak (psutil). The run log is in `screen/ambient_variation_run.log`. The revision 2 results file was kept for comparison in the session scratch folder; the first-place probabilities of the full run, halves, forms, leave-one-out, months, stress and the seven earlier sweeps are identical to revision 2 (same seed and draw order).
- The verifier's checks were reproduced in the script: bottled habit counted once gives reach sweet-bottled 25 to 44 0.544 and men 45 to 59 0.438, per member sweet-bottled 25 to 44 0.801, per person 0.9405; the age gradient alone gives 1.0295 (0.9985 to 1.0677; 0.9412); the plus or minus 7 percent population sweep gives reach 0.648 (the verifier reported 0.647).
- Base-case arithmetic checked by hand for three bases against the script in revision 2: men 25 to 34 per person in the cell 0.3416 (0.686 x 0.99715 x 0.3608 x 0.30 x 4.91 x 0.93966, reach 1.626), men 45 to 59 reach 1.784 (script 1.785), sweet-bottled 25 to 44 reach 1.490 (script 1.492).
- Consistency check: with every male temperature sensitivity set to 0 (directional delta 0) the per-person leader's probability is 0.9734, equal to the leave-one-out run with temperature fixed at its mean (0.9734).
- Chart opened and read back after the changes: all six panels are legible at full size (A reach interval, B first-place share by lens, C by month with the two directional scenarios, D and E tornados, F validation matrix). Panel C's legend was moved above the lines after the first read showed it covering the April dip.
- Not checked: the printed NSO 2024 and 2021 page images (text-layer extracts only); the DOPA counts, odds ratio and internet shares (carried, UNVERIFIED); the Mintel sample; the TMD table in the original PDF beyond the page read; any temperature-to-demand source (not searched for successfully, section 8, item 8); the effect of the T10 verification on the band cells (re-run needed if they change).
- No file in rework/submission, rework/proposal or rework/deck was edited; rework/README.md was not updated (the lead adds the row).
