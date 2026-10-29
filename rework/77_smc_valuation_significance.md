# 77. Sequential Monte Carlo on the valuation and the pilot, and significance (task T14), third pass

Date: 20 October 2026. Team-only record. Desk model on stated priors. Not a finding from market data.

Script: [screen/smc_valuation.py](screen/smc_valuation.py). Results: [screen/smc_valuation_results.json](screen/smc_valuation_results.json). Charts: [charts/smc_npv_distribution.png](charts/smc_npv_distribution.png), [charts/smc_pilot_posterior_fan.png](charts/smc_pilot_posterior_fan.png), [charts/smc_operating_characteristics.png](charts/smc_operating_characteristics.png), [charts/smc_expected_npv_by_demand.png](charts/smc_expected_npv_by_demand.png). Saved source note: [raw/diligence_2026-10-20/T14/tax_rate_and_inputs_2026-10-20.md](raw/diligence_2026-10-20/T14/tax_rate_and_inputs_2026-10-20.md). Run: one process, seed 20261020, about 470 seconds, 200,000 prior draws, 200,000 particles in the fan, 2,000 particles per simulated pilot elsewhere (300 evolution pilots per truth at 20 stores and at 40 stores), 40,000 truths for the value comparison (10,000 in the main run and 30,000 in an independent run), peak working set 271 MB (measured with psutil, under the 300 MB limit). Every number below is read from the results file.

This pass answers the second independent verifier review (section 10 lists every issue and what was done; the first review's table is kept as history). It was written and run on Sonnet 5.5, which meets the routing rule in CLAUDE.md for T14 (Sonnet or higher to verify and revise). The single final Opus check of T14 named in rework/workflows/model_routing_2026-10-20.md is not part of this pass.

## Status and checks

- Reconciliation, record 05: the deterministic NPV at THB 4.91 a cube is THB 880,796 (record 05: 880,796) and the break-even is 146,230 cubes a year (record 05: 146,230). The script asserts both.
- Reconciliation, record 75: the script rebuilds the after-excise contribution as 15 times the can chain ratio (7.393 / 13.8025) less 4.09, which is THB 3.9444, and the after-tax NPV at 200,000 cubes, THB 500,000 fixed cost and 10 percent is THB 165,023.77 (record 75: 165,023.77). The after-tax break-even is 184,324.7 cubes (record 75: 184,324.7). The script asserts both.
- Replication of the verifier's figures (fixed true demand, every other input from its prior): variant B at 2.2 units a store-week, expected NPV minus THB 0.99 million and P(NPV above 0) 0.27 (verifier: minus 0.98 and 0.28); B at 3.0 units, minus 0.39 and 0.43 (verifier: minus 0.38 and 0.43); A at 2.2 units, minus 0.36 and 0.42 (verifier: minus 0.36 and 0.43). The expected-NPV break-even is 2.55 units on A and 3.53 on B (verifier: about 2.5 and 3.5). The verifier's finding is therefore confirmed and the 2.2-unit proposal of the first pass is withdrawn.
- Corporate income tax: 20 percent, tier S (primary-origin page, Revenue Department page 6044, last updated 23 November 2020, read through a page summary on 20 October 2026; saved note above, also saved in T12). Appendix A reserves P for text read in full, so the second pass's "P (extract)" was a tier upgrade and is withdrawn. Record 75 and the T12 note use S. The first pass called the rate UNVERIFIED because it did not find the T12 page; that stays corrected.
- Calibration (unchanged from the first pass because the seeds are the same): the realised national demand lies inside the 90 percent posterior band at week 13 in 88, 93 and 89 percent of 300 pilots (truths 1.5, 3.0, 4.5) with 2,000 particles, and in 97, 90 and 90 percent of 100 pilots with 10,000 particles. The largest difference in P(demand at or above 3) between 200,000 and 2,000 particles on the same pilot is 0.005, 0.026 and 0.013.
- Reproduction. The third-pass script reproduces every number of the second-pass results file exactly (no differing numeric value over all shared keys), because the new computations use their own random streams. The 200,000-particle week-by-week mapping agrees with the Rao-Blackwellised mapping to within 0.002 to 0.005.
- All four charts were opened and checked for legibility after the final run.
- Not verified: any Thai source for the cost lines, fixed cost, shelf price, cannibalisation share or the store-equivalent count behind the unit conversion; any pilot data (none exist).
- No outside contact, no form, no download, no supplier quote. No new figure was sourced beyond the tax rate, so the only file added to rework/raw/diligence_2026-10-20/T14 is the tax and basis note.

What changed in this (third) pass: the tax rate is re-tiered S; the value of waiting is reported under three scoring conventions on 40,000 truths, with and without a five-week delay discount (the sign depends on the convention and the size is within about THB 5,000); the week-by-week evolution of P(NPV above 0) is now averaged over 300 simulated pilots per truth (with the 10th to 90th percentile) beside the single pilot; the separation powers carry Monte Carlo standard errors and the store-count wording is at halving resolution; the break-evens are stated as a range with their conditions; the missing team settings (click-to-purchase threshold, pilot spend limit) replace the dropped hand-offs; the slide 10 and slide 11 text is cut from about 700 and 600 words to about 370 and 400 (the current slides carry 240 and 300) and corrected on cannibalisation. Earlier passes: the break-even became the expected-NPV break-even; the record 75 lead basis was added; the store-equivalent count was re-tiered ASSUMPTION; IRR and payback got Monte Carlo standard errors; joint narrowing was added.

## 0. Answer in brief

- Basis. Records 05 and 75 use different contribution bases and no basis has been chosen, so three are reported side by side. A is the record 05 structure. B is the full stated prior on the record 05 basis (before excise, pre-tax); it is the headline fixed in advance. D is the lead basis of record 75 (after excise, 20 percent tax, same-year loss offset, depreciation shield, cannibalisation). Every conclusion below holds on all three.
- Test (i), is the projected NPV significantly above zero? No. P(NPV above 0) is 0.58 on A, 0.40 on B and 0.26 on D (Monte Carlo standard error 0.001 each), against the 0.95 fixed in advance. The 90 percent intervals are minus 2.72 to plus 4.14 million (A), minus 3.64 to plus 3.03 million (B) and minus 3.40 to plus 1.59 million (D); all include zero. This is conditional on the assumed priors and is not a finding from market data.
- The base values are point values, not expected values. THB 0.88 million (before excise, pre-tax) and THB 0.17 million (lead basis, after tax) are the NPV with every input at its median. The expected NPV under the stated uncertainty is plus 0.49 million on A, minus 0.41 million on B and minus 0.88 million on D; the medians are plus 0.36, minus 0.46 and minus 0.87 million.
- What would change the conclusion. Fixed cost and shelf price. First-order variance index: fixed cost 0.31 on B and 0.36 on D; shelf price 0.22 and 0.23. In decision terms (expected value of perfect information on one input) shelf price and fixed cost are each worth about THB 0.23 million on B, and fixed cost THB 0.03 million on D. Even the most favourable tenth of one input gives at most 0.73 (B, fixed cost) and 0.58 (D, fixed cost). A joint restriction reaches 0.96: on B, fixed cost at or below THB 500,000, shelf price at or above THB 16.7 and steady volume at or above 196,000 cubes (6.0 percent of the prior); on D, fixed cost at or below THB 416,000, shelf price at or above THB 16.7, cannibalisation share at or below 0.23 and volume at or above 196,000 cubes (1.9 percent of the prior). These are what would have to be learned, not forecasts.
- Break-even demand, corrected, and its range. The 2.19 units of the first pass is the point-value break-even at input medians, before excise and before tax, and it assumes 1,282 store-equivalents. Under the stated uncertainty the demand at which the expected NPV is zero is 2.55 units a store-week (170,300 cubes a year) on A, 3.53 units (235,300 cubes) on B and 5.03 units (335,200 cubes) on D. These are a range with two stated conditions, not points. Price and volume independent (used here) against the assumed link between a higher price and lower volume kept: 2.40, 4.09 and 8.76 units (160,100, 272,500 and 583,900 cubes). The store-equivalent count is an ASSUMPTION (the count implied by 3 units and 200,000 cubes; 8.0 percent of about 15,945 7-Eleven stores as context): at 2,000 the three figures become 1.6, 2.3 and 3.2 units, and at 1,000 they become 3.3, 4.5 and 6.4. The 3-unit line of the plan sits above the A figure and below the B and D figures. The 2.2-unit proposal of the first pass is withdrawn: at 2.2 units the expected NPV is negative on every basis (A minus 0.36, B minus 0.99, D minus 1.19 million).
- Test (ii), is the segment lead (men 25 to 34 over 35 to 44) significant? No. P(ratio above 1) is 0.941, below the 0.95 rule, and the 90 percent interval is 0.998 to 1.085. At 1,377 completes per cell the power is 6 to 11 percent for leads of 0.6 to 1.2 points (two-sided). The minimum detectable difference is 4.99 points.
- How P(NPV above 0) evolves over the pilot, averaged over 300 simulated 20-store pilots per truth. Almost all of the movement comes in the first four weeks. Variant B, mean (10th to 90th percentile) at week 13: 0.13 (0.08 to 0.18) at a true 1.5 units, 0.42 (0.34 to 0.49) at 3.0 and 0.61 (0.56 to 0.66) at 4.5; the prior is 0.40. Variant D: 0.06, 0.28 and 0.46; variant A: 0.22, 0.60 and 0.79. The three truths are separated by the posterior probability, but no simulated pilot reaches 0.95 on any basis at any truth (0 of 300 in every cell), because fixed cost, price and the cost lines are not learned from demand counts. The pilot therefore does not change the answer to test (i); it moves the probability within a band of about 0.06 to 0.8.
- Test (iii), are the pilot rule thresholds distinguishable from noise at the planned sample? Partly. At 20 stores the two-read 3-unit rule stops 91 percent of pilots at a true 2.5 units and scales 86 percent at 3.5 units; at the line itself it scales 35 percent, stops 39 percent and holds 27 percent. A halving of demand (1.5 against 3.0) is told apart with power about 0.9 at 20 stores (0.88, Monte Carlo SE 0.02; 0.81 at 15 stores; 0.78 at 20 stores if store-to-store variation is high). A rise of half again (3.0 against 4.5) is not separated at any store count tested (0.78 at 40). The 15 percent repeat floor is a band: a true 15 percent passes in 28 percent of cohort pairs.
- Store count for Route A: 20 stores, for halving resolution. At week 13 the decision-pair power is 0.75 at 10 stores, 0.81 at 15, 0.88 at 20 and 0.93 at 30 (Monte Carlo SE 0.014 to 0.025). Fifteen meets the 0.80 criterion by less than one standard error and is not distinguishable from 10 stores at 300 pilots a cell (z 1.7); 20 stores is distinguishable from both (z 2.4 against 15, 4.1 against 10). Use 30 stores if store-to-store variation is high (0.88 at log-sd 0.5). No tested count separates 3.0 from 4.5 with 80 percent power, so the count is not a resolution of the 3-unit line itself.
- Value of the pilot and of waiting, like for like. The demand read is worth THB 0.19 million (A, against scaling without a pilot), THB 0.25 million (B) and THB 0.03 million (D) in expectation, and the Bayes rule at week 8 already captures 87 to 95 percent of the value of knowing demand exactly. Waiting from week 8 to week 13 is worth between minus THB 3,500 and plus THB 4,900 on every basis, and the sign depends on how the NPV is scored: against the start-of-pilot level (the second pass) it is minus THB 3,541 (A, standard error 372), minus 3,281 (B, 351) and minus 1,184 (D, 193); against the level at each rule's own decision week it is plus 4,909 (798), plus 3,283 (537) and plus 790 (228); against the common week-13 level it is plus 2,020 (345), plus 2,043 (325) and plus 603 (169), on 40,000 truths. After the discount for acting five weeks later (a factor 0.9909, about THB 9,100 per THB 1 million of NPV) the week-13 rule is worth between minus 5,700 and plus 900. The data cannot say whether waiting helps; it is below 4 percent of the value of the demand read in every case. The first pass's "THB 15,200 worth of waiting" compared a two-read rule with a one-read rule; it measured the stricter line, not the extra weeks. The 3-unit rules add value on A and B and lose value on D (minus THB 0.15 to minus 0.19 million), because the D break-even is 5 units.

## 1. Inputs and priors

Every input has a prior. Tiers follow the repo key (submission/appendix_a_tier_key.md). "Achieved" is the 5th, median and 95th percentile of the 200,000 draws.

| Input | Prior | Achieved (5th, median, 95th) | Tier and status | Source or basis |
|---|---|---|---|---|
| Shelf price (THB per cube) | Uniform 10 to 20 | 10.5, 15.0, 19.5 | ASSUMPTION | submission/06_kpi.md range; record 05 base 15 |
| Ex-factory share | Uniform 0.50 to 0.70 | 0.51, 0.60, 0.69 | ASSUMPTION | submission/06_kpi.md range; record 05 base 0.60 |
| After-excise scaling of the ex-factory share (variants A2, B2, D) | Multiply the share by 0.535628 / 0.60 | 0.89 times | DERIVED, PROXY | Can net-to-listing chain ratio 7.393 / 13.8025 (can_cost_model_results.json, S) used for the cube as in record 75; excise classification and base not verified |
| First-purchase cubes a year | Log-normal, median 140,000, log-sd 0.38; Gaussian copula with shelf price, rho minus 0.30 | 74,900, 140,100, 262,000 | ASSUMPTION (median and rho); PROXY (spread) | Median is 200,000 times (1 minus 0.30). Spread from record 70 bottom-up can volume (a can measure, not a cube measure). The sign and size of the correlation are assumptions |
| Repeat rate | Triangular, 0.15, mode 0.30, 0.40 | 0.19, 0.29, 0.36 | ASSUMPTION | submission/06_kpi.md bounds 15 to 40 percent, target 30 percent. No mass below the 15 percent floor |
| Repeat rate, wide variant (B_wide, D_wide) | Beta, mean 0.283, sd 0.10 | 0.13, 0.28, 0.46; P(below 0.15) = 0.079 | ASSUMPTION | Same mean as the triangular prior; lets the repeat fall below the stop floor |
| Cubes a year (steady state) | First-purchase cubes divided by (1 minus repeat) | 103,600, 195,900, 370,600 (mean 211,300) | DERIVED | The median is 196,000, not the 200,000 base scenario, because the repeat prior has mean 0.283 |
| Year-1 share of steady volume | Uniform 0.30 to 0.70 | 0.32, 0.50, 0.68 | ASSUMPTION | Record 05 uses 0.5 |
| Potassium bicarbonate price (THB per kg) | Log-normal, median 38.1, log-sd 0.25 | 25, 38, 58 | PROXY, UNVERIFIED | Record 05 (UN Comtrade unit value, page not saved). Spread is an assumption |
| Citric acid price (THB per kg) | Log-normal, median 31.4, log-sd 0.25 | 21, 31, 47 | PROXY, UNVERIFIED | Record 05 (UN Comtrade, page not saved) |
| Sucralose price (THB per kg) | Log-normal, median 655, log-sd 0.25 | 435, 656, 988 | UNVERIFIED | Record 05 (retailer asking price, page not saved). Cost effect about THB 0.02 a cube |
| Citric acid mass per cube (g) | Uniform 2.10 to 3.70 (variants B, B2, D); 2.10 in A, A2 | 2.18, 2.90, 3.62 | DERIVED endpoints; ASSUMPTION on the pH range | Record 05 handover figures at pH 3.5 and pH 3.0 |
| Potassium bicarbonate and sucralose mass | 0.811 g and 33 mg, fixed | | DERIVED | Record 05 |
| Pouch (THB) | Log-normal, median 1.30, log-sd 0.42 | 0.65, 1.30, 2.60 | DERIVED on an UNVERIFIED listing | Record 05 range 0.67 to 2.70 |
| Print (THB) | Log-normal, median 1.50, log-sd 0.35 | 0.84, 1.50, 2.66 | ASSUMPTION | Record 05 range 0.80 to 2.50 |
| Processing (THB) | Log-normal, median 0.50, log-sd 0.42 | 0.25, 0.50, 1.00 | ASSUMPTION | Record 05 range 0.25 to 1.00 |
| Carton per 6 cubes (THB) | Log-normal, median 4.00, log-sd 0.33 | 2.32, 4.00, 6.88 | ASSUMPTION | Record 05 base |
| Binder and flavour (THB per cube) | Uniform 0 to 0.30 (zero in A, A2) | 0.02, 0.15, 0.29 | ASSUMPTION | Not priced in records 05 and 06; the 0.30 bound is a placeholder |
| Cannibalisation share (buyers who were can buyers; zero in A, A2) | Beta, mean 0.25, 5th to 95th near 0.05 to 0.50 (a = 2.26, b = 6.77) | 0.06, 0.23, 0.50 | ASSUMPTION | Record 70 uses 25 and 50 percent. P(share at or above 0.50) = 0.053; P(share at or above the record 75 break-even of 0.075) = 0.924 |
| Can contribution before aluminium (THB per can) | Triangular, 3.38, mode 4.13, 5.68 | 3.67, 4.35, 5.26 | DERIVED | Record 70 section 2.11; aluminium is not netted, so the lost contribution is an upper bound |
| Annual fixed cash cost (THB) | Log-normal, median 500,000, log-sd 0.42 (mean 546,800) | 250,100, 501,000, 998,100 | ASSUMPTION | Record 05 grid 250,000 to 2,000,000 |
| Discount rate | Uniform 0.08 to 0.12 | 0.08, 0.10, 0.12 | ASSUMPTION | Record 05; record 75 builds it as the policy rate (1.00 percent, S: Bank of Thailand press release read through a page summary) plus a premium of 9 points (7 to 11, ASSUMPTION) |
| Corporate income tax rate | 0.20, fixed in C, D, D_cf and D_wide; zero in the pre-tax variants | | S (primary-origin page, read through a page summary; not P) | Revenue Department page 6044, last updated 23 November 2020. A statutory rate has no prior. The uncertain part is the structure, so three are modelled: C no relief; D same-year loss offset with a five-year straight-line depreciation shield of the year-0 outlay (record 75); D_cf stand-alone entity with loss carry-forward (the page lists losses carried forward from the last five periods) |
| Store-equivalents behind 200,000 cubes (N_EFF) | 1,282 (sensitivity 1,000 and 2,000) | | ASSUMPTION | The store-equivalent count implied by 3 units a store-week and 200,000 cubes a year (52 x 1,282 x 3 = 199,992); it is back-solved, not found. Nothing in the repo ties 200,000 cubes to a store count or to the 3-unit target; the first pass called it DERIVED, which was wrong. Context only: 1,282 is 8.0 percent of the about 15,945 7-Eleven stores of submission/04 line 37 (P, SOURCED there; read as Thailand-only by inference); that share is arithmetic, not a derivation. The pilot's own store count is not sourced (record 79) |
| Pilot: store-to-store log-sd of weekly demand | 0.30 (base); 0.15 and 0.50 in sensitivity | | ASSUMPTION | No source. The pilot offset has sd 0.30 divided by the square root of the store count |
| Pilot: weekly drift noise | 0.02 (base); 0.005 in sensitivity | | ASSUMPTION | No source |
| Pilot: NB size per store-week | 5 | | ASSUMPTION | No source |
| Pilot: read weeks | 8 and 13 | | ASSUMPTION | Submission 10 says two consecutive reads without dates; the repeat reads are at 8 and 12 weeks. The two reads come from one cumulative posterior, so they are correlated (phi 0.35 at 2.5 units, 0.47 at 3.0, 0.68 at 3.5) |

Survey inputs (section 5) are taken from records 47 and 49 (sampling error on the odds ratio only; no respondents).

## 2. Method

### 2.1 Prior predictive Monte Carlo (part A)

Cash flow in year t (t = 1 to 5): (c minus k times cc) times V times ramp_t, minus F, with tax as stated below. Here c is shelf price times ex-factory share (scaled for excise in A2, B2, D) minus cost per cube; k is the cannibalisation share; cc is the can contribution; V is cubes a year; F is fixed cost. Year 0 is minus F. No terminal value. The same structure as record 05.

Variants, all from the same 200,000 draws:
- A: record 05 structure (binder and flavour 0, citric acid fixed at 2.10 g, no cannibalisation), before excise, pre-tax. A therefore fixes three inputs that B gives priors to: binder and flavour, citric acid mass and cannibalisation.
- B: full stated prior, before excise, pre-tax. This is the pre-registered headline.
- C: B with 20 percent tax on positive annual operating profit (no loss relief, no shield).
- A2 and B2: A and B on the after-excise basis, pre-tax.
- D: record 75 lead basis. After excise; tax is 20 percent of operating profit less one fifth of F depreciation, and a loss earns the same credit in the year.
- D_cf: D with a stand-alone entity, depreciation deducted and losses carried forward.
- B_wide and D_wide: B and D with the wide repeat prior.
- B_rho0: B without the price and volume correlation.

Basis mixing. The before-excise variants with cannibalisation (B, C, B_wide, B_rho0) subtract the after-excise can contribution (THB 4.13) from a before-excise cube contribution. Record 75 (section 11) flags this as flattering when the cannibalisation share is high. The consistent versions are B2 and D, where cube and can are both after excise; P(NPV above 0) is lower on them (0.267 and 0.262). Variants A and A2 have no cannibalisation term, so the mixing does not arise in them (A2 differs from A only in the after-excise share, 0.445 against 0.580). The pre-registered headline B is therefore the more favourable reading, and it still fails the test.

IRR is solved by bisection (minus 90 to 1,000 percent) and does not exist where the flows do not change sign. Payback is undiscounted, linear within the year. Monte Carlo standard errors: probabilities from the binomial formula; means from the sample standard error; medians, percentiles, IRR and payback statistics from 20 batch means.

### 2.2 Sequential Monte Carlo for the pilot (part B)

Latent state: the pilot-level log demand, a random walk with a learned drift (weekly noise 0.02). The national demand is the pilot-level value minus a store offset with prior sd 0.30 divided by the square root of the store count, drawn from its exact conditional given the initial level. Observations: weekly unit sales across S stores as a negative binomial with size 5 times S and mean S times the pilot-level demand. Filter: bootstrap particle filter with systematic resampling when the effective sample size falls below half the particles; the drift is updated with a Liu-West kernel (discount 0.98). Static inputs that do not enter the counts are redrawn from their priors after each resampling, which is exact. NPV is linear in volume for the pre-tax and record 75 structures (NPV = alpha times V minus beta), so each particle's NPV is exact and the script checks the linear form against the cash-flow code for 200,000 draws.

The true demand levels are 1.5, 3.0 and 4.5 units a store a week for the fan, and 1.0 to 6.0 in steps of 0.5 for the operating characteristics. The truth is the start-of-pilot level; the realised level drifts by about 7 percent over 13 weeks at the base noise.

Week-by-week evolution over many pilots (third pass). For each truth (1.5, 3.0 and 4.5 units a store a week) 300 simulated pilots of 20 stores are filtered with 2,000 particles each (and 300 of 40 stores, for the pair check in section 4.4). NPV is linear in volume (NPV = alpha times V minus beta), so P(NPV above 0 given the data) is the weight-averaged exact conditional P(NPV above 0 given V) taken from the 200,000 prior draws (static inputs independent of demand), and the posterior expected NPV is the mean alpha times the posterior mean volume minus the mean beta. This mapping uses no random numbers; on the three 200,000-particle pilots of section 4.2 it agrees with the particle mapping to within 0.003 to 0.005. The runs use their own random streams, so every earlier number is reproduced exactly (the script's output and the second-pass results file agree on every shared number).

Pilot world. When the pilot reads demand, the other inputs keep their priors and are independent of the demand read. The prior predictive keeps the price and volume correlation. The effect is stated as a sensitivity (section 4.1): the independent mapping lifts the expected NPV by THB 0.10 to 0.14 million against the joint prior, and with the correlation kept the break-even demand is higher (B 4.09 units, D 8.76 units, A 2.40 units).

### 2.3 Pre-registered tests (fixed before the run; written in the script header)

- (i) H0: NPV at or below 0. Reject if P(NPV above 0) is at least 0.95 under variant B, the headline. The 90 percent credible interval (5th to 95th percentile) is reported against zero. The same rule is applied to every other variant and reported.
- (ii) Segment lead: significant only if P(ratio above 1) is at least 0.95 and the 90 percent interval excludes 1. Power at the affordable cell size (1,377 completes per cell, records 47 and 49) is reported.
- (iii) Pilot rule. A read says "at or above 3" if P(demand at or above 3 | data) is at least 0.5. Scale if both reads (weeks 8 and 13) say "at or above", stop if both say below, otherwise hold. Truths are separated if P(demand above the midpoint | data) is at least 0.9 for the higher truth or at most 0.1 for the lower; the target is 80 percent power.
- Recommended store count: the smallest count at which, at week 13, the separation power is at least 0.80 for the decision pairs (1.5 against 3.0, and 1.5 against 4.5), the false-scale rate at 1.5 is at most 0.10 and the false-stop rate at 4.5 is at most 0.10. The pair 3.0 against 4.5 is reported and is not a decision pair in this criterion. The criterion therefore fixes a count for halving resolution only; under an all-pairs criterion no tested count qualifies (section 4.4).
- Added in this pass, with the same standing: the expected-NPV break-even demand and the value of the pilot (section 4.1 and 4.6) are descriptive and carry no pass or fail rule.

## 3. Results A: prior predictive NPV (200,000 draws per variant)

| Variant | P(NPV above 0) | MC SE | Mean (THB m) | Median (THB m) | 5th (THB m) | 95th (THB m) | Rule (i): reject H0 if P at least 0.95 |
|---|---|---|---|---|---|---|---|
| A, record 05 structure (before excise, pre-tax) | 0.580 | 0.0011 | +0.49 | +0.36 | -2.72 | +4.14 | not met |
| B, full stated prior (before excise, pre-tax; pre-registered headline) | 0.399 | 0.0011 | -0.41 | -0.46 | -3.64 | +3.03 | not met |
| C, B with 20 percent tax, no loss relief | 0.370 | 0.0011 | -0.58 | -0.51 | -3.64 | +2.34 | not met |
| A2, A on the after-excise basis, pre-tax | 0.445 | 0.0011 | -0.17 | -0.23 | -3.21 | +3.07 | not met |
| B2, B on the after-excise basis, pre-tax | 0.267 | 0.0010 | -1.07 | -1.06 | -4.20 | +2.02 | not met |
| D, record 75 lead basis (after excise, after tax) | 0.262 | 0.0010 | -0.88 | -0.87 | -3.40 | +1.59 | not met |
| D_cf, D with a stand-alone entity and loss carry-forward | 0.261 | 0.0010 | -1.14 | -1.06 | -4.20 | +1.59 | not met |
| B_wide, B with repeat prior reaching below 15 percent | 0.403 | 0.0011 | -0.37 | -0.45 | -3.65 | +3.22 | not met |
| D_wide, D with the same repeat prior | 0.267 | 0.0010 | -0.86 | -0.86 | -3.40 | +1.70 | not met |
| B_rho0, B without the price and volume correlation | 0.411 | 0.0011 | -0.27 | -0.44 | -3.62 | +3.64 | not met |

Monte Carlo standard errors are at most THB 5,100 on the means, THB 7,000 on the medians, THB 11,100 on the 5th percentiles and THB 15,800 on the 95th percentiles. All 90 percent intervals include zero.

IRR and payback (undiscounted), with Monte Carlo standard errors in brackets:

| Variant | IRR defined (share, SE) | IRR median (SE) | IRR 5th to 95th | Paid back within 5 years (share, SE) | Payback median if paid (SE), years | Payback 5th to 95th if paid |
|---|---|---|---|---|---|---|
| A | 0.751 (0.0010) | 57.8 percent (0.24) | -33 to 252 percent | 0.618 (0.0011) | 1.63 (0.003) | 0.50 to 4.11 |
| B | 0.563 (0.0011) | 42.9 percent (0.25) | -39 to 216 percent | 0.434 (0.0011) | 1.80 (0.004) | 0.59 to 4.29 |
| D | 0.436 (0.0011) | 22.9 percent (0.20) | -45 to 151 percent | 0.296 (0.0010) | 2.12 (0.007) | 0.87 to 4.47 |

The results file also holds the standard errors of the IRR and payback 5th and 95th percentiles.

- Reading the variants. Moving from the before-excise to the after-excise basis costs 13 to 14 points of probability (A 0.58 to 0.45; B 0.40 to 0.27). Tax then changes little (B2 0.267, D 0.262, D_cf 0.261) because most of the probability mass sits in the loss-making draws, where relief is either credited (D) or ignored (D_cf, same median as B2). A repeat prior that reaches below the floor changes P(NPV above 0) by 0.004 to 0.005 (B_wide 0.403, D_wide 0.267): the repeat floor is not what limits the NPV. Removing the price and volume correlation raises B to 0.411.
- Why the prior median is lower than the point values. The record 05 point uses the medians of the cost lines. The median of their sum is higher (cost per cube median THB 4.46 on B against THB 4.09 at the record point), and the fixed cost has a mean above its median (THB 546,800). Contribution before cannibalisation has median THB 4.53 on A, 4.36 on B and 3.41 on D (after excise).
- Contribution floor of THB 3.51 (record 06 stop rule, before excise): prior probability of being below it is 0.36 on B and 0.33 on A. On the after-excise basis the same cost rise gives a floor of THB 2.54 (record 75 section 5.8) and the probability of being below it is 0.34 on D.

### 3.1 Sensitivity (variance-based first-order indices, rank correlations, and the value of learning one input)

Variant B (pre-registered headline):

| Input | First-order variance index | Spearman with NPV | P(NPV above 0) lowest to highest tenth | P(NPV above 0) if pinned near median | EVPPI (THB) |
|---|---|---|---|---|---|
| Fixed cost (THB a year) | 0.305 | -0.53 | 0.73 to 0.07 | 0.401 | 228,812 |
| Shelf price (THB) | 0.224 | +0.49 | 0.08 to 0.66 | 0.417 | 231,449 |
| Ex-factory share | 0.084 | +0.29 | 0.21 to 0.58 | 0.404 | 94,209 |
| First-purchase cubes a year | 0.054 | +0.21 | 0.19 to 0.55 | 0.413 | 59,748 |
| Pouch (THB) | 0.046 | -0.20 | 0.51 to 0.23 | 0.416 | 17,466 |
| Cannibalisation share | 0.042 | -0.20 | 0.52 to 0.24 | 0.408 | 22,674 |
| Print (THB) | 0.038 | -0.19 | 0.51 to 0.24 | 0.409 | 13,779 |
| Carton per 6 cubes (THB) | 0.007 | -0.08 | 0.45 to 0.33 | 0.403 | 0 |

Variant D (record 75 lead basis):

| Input | First-order variance index | Spearman with NPV | P(NPV above 0) lowest to highest tenth | P(NPV above 0) if pinned near median | EVPPI (THB) |
|---|---|---|---|---|---|
| Fixed cost (THB a year) | 0.359 | -0.57 | 0.58 to 0.03 | 0.242 | 32,302 |
| Shelf price (THB) | 0.227 | +0.49 | 0.03 to 0.51 | 0.253 | 8,552 |
| Ex-factory share | 0.077 | +0.28 | 0.11 to 0.43 | 0.258 | 0 |
| Pouch (THB) | 0.052 | -0.21 | 0.37 to 0.12 | 0.273 | 0 |
| Cannibalisation share | 0.048 | -0.21 | 0.38 to 0.13 | 0.266 | 0 |
| Print (THB) | 0.043 | -0.20 | 0.36 to 0.13 | 0.270 | 0 |
| First-purchase cubes a year | 0.019 | +0.12 | 0.10 to 0.39 | 0.270 | 0 |
| Carton per 6 cubes (THB) | 0.008 | -0.08 | 0.31 to 0.20 | 0.263 | 0 |

EVPPI is the expected value of perfect information on one input (25 bins; it is biased upward by up to about THB 10,000 for inputs with no effect, and the zeros are inputs whose best decision never changes). On D no single input is worth more than THB 32,000 because the prior says do not scale and learning one input rarely reverses that.

Reading: fixed cost and shelf price carry most of the variance on both bases. Narrowing either to its middle half leaves P(NPV above 0) unchanged (0.40 on B), because the centre of the distribution does not move. What moves the probability is learning the tails. No single input, narrowed to its most favourable tenth, reaches 0.95. Shelf price and cubes are negatively correlated by construction (rho minus 0.30), so their indices are approximate; the first-order sum on B is about 0.8, so interactions carry about a fifth of the variance.

### 3.2 Joint narrowing (largest prior region in which P(NPV above 0) reaches 0.95)

The scan covers 390 regions defined by an upper quantile of fixed cost, a lower quantile of shelf price, an upper quantile of cannibalisation share and a lower quantile of steady volume, each with at least 200 draws. The regions are chosen after the fact, so the probabilities are optimistic; they show what would have to be learned.

| Basis | Fixed cost and shelf price in their favourable tertiles (prior mass; P) | Largest region reaching 0.95 (prior mass; P) |
|---|---|---|
| A | 0.109; 0.965 | Fixed cost at or below THB 416,000, shelf price at or above THB 15 (prior mass 0.165; P 0.950) |
| B | 0.109; 0.887 | Fixed cost at or below THB 500,000, shelf price at or above THB 16.7, volume at or above 196,000 cubes (0.060; 0.962) |
| D | 0.109; 0.751 | Fixed cost at or below THB 416,000, shelf price at or above THB 16.7, cannibalisation at or below 0.23, volume at or above 196,000 cubes (0.019; 0.962) |

Adding a cannibalisation share in its lowest third to the favourable fixed cost and price tertiles gives 0.937 on B and 0.841 on D (prior mass 0.036). On D, the lead basis, the 0.95 threshold is reached only in a region that holds about 2 percent of the prior.

## 4. Results B: sequential Monte Carlo for the pilot

### 4.1 Fixed true demand: expected NPV and P(NPV above 0), and the break-even demand

The first pass used the point-value break-even (2.19 units). That value is the NPV at input medians, before excise and before tax, so it is not the demand at which the expected NPV is zero. The table fixes the true steady demand (cubes a year = 52 times 1,282 times demand) and draws every other input from its prior.

| True demand (units a store-week) | Cubes a year | Point value, before excise, pre-tax (THB m) | Point value, lead basis (THB m) | A: expected NPV (THB m), P(NPV above 0) | B: expected NPV, P | D: expected NPV, P |
|---|---|---|---|---|---|---|
| 2.0 | 133,328 | -0.21 | -0.54 | -0.57, 0.37 | -1.14, 0.23 | -1.28, 0.13 |
| 2.2 | 146,661 | n/a | n/a | -0.36, 0.42 | -0.99, 0.27 | -1.19, 0.16 |
| 2.5 | 166,660 | +0.33 | -0.19 | -0.06, 0.50 | -0.76, 0.34 | -1.07, 0.21 |
| 3.0 | 199,992 | +0.88 | +0.16 | +0.46, 0.61 | -0.39, 0.43 | -0.86, 0.28 |
| 3.5 | 233,324 | +1.43 | +0.52 | +0.97, 0.69 | -0.02, 0.50 | -0.65, 0.35 |
| 4.0 | 266,656 | +1.97 | +0.87 | +1.48, 0.75 | +0.35, 0.56 | -0.43, 0.41 |
| 4.5 | 299,988 | +2.52 | +1.22 | +2.00, 0.79 | +0.72, 0.61 | -0.22, 0.46 |
| 5.0 | 333,320 | +3.06 | +1.57 | +2.51, 0.82 | +1.09, 0.65 | -0.01, 0.50 |
| 6.0 | 399,984 | +4.16 | +2.27 | +3.53, 0.87 | +1.83, 0.71 | +0.41, 0.56 |

Monte Carlo standard errors: THB 2,200 to 7,200 on the expected NPV, at most 0.0011 on the probability. The results file also holds the 5th and 95th percentiles.

- Expected-NPV break-even demand: A 2.55 units (170,300 cubes a year), B 3.53 units (235,300 cubes), D 5.03 units (335,200 cubes). The demand at which the median NPV is zero is close (A 165,900 cubes, B 233,500, D 335,500). The after-excise pre-tax variants give A2 3.23 units and B2 4.97 units. The point-value break-even on the lead basis is 184,325 cubes (2.76 units, after tax, no cannibalisation; record 75).
- Dependence on the store-equivalent count N_EFF (ASSUMPTION). The break-even in cubes a year does not depend on it; the break-even in units does. At 1,000 store-equivalents: A 3.28, B 4.52, D 6.45 units. At 1,282: 2.55, 3.53, 5.03. At 2,000: 1.64, 2.26, 3.22. The 3-unit line equals the expected-NPV break-even at 1,092 store-equivalents on A, 1,508 on B and 2,149 on D.
- Price and volume correlation kept (rho minus 0.30). The expected-NPV break-even is then 2.40 units (160,100 cubes a year) on A, 4.09 (272,500) on B and 8.76 (583,900) on D. The independent mapping used in the pilot analysis (and in the 2.55, 3.53 and 5.03 above) is the lower-demand case for B and D. The break-evens are therefore a range with two stated conditions: price and volume independent or correlated, and 1,000 to 2,000 store-equivalents (D 3.2 to 6.4 units under independence, and higher with the correlation kept). Neither condition is sourced.
- Shelf price pinned between THB 14.5 and 15.5 (10 percent of the prior): the break-even demand is 2.56 (A), 3.54 (B) and 5.05 (D) units, and P(NPV above 0) at 6.0 units is 0.949 (A; just below the 0.95 line, standard error 0.0015 on 20,116 draws), 0.804 (B) and 0.61 (D). Knowing the price near THB 15 does not change the conclusion except on the simplest structure at 6 units, where it sits on the line.
- Perfect knowledge of volume does not make NPV certain: at 6 units a store-week P(NPV above 0) is 0.87 (A), 0.71 (B) and 0.56 (D). The pilot cannot settle the economics on its own.
- Oracle rules (scale if and only if the steady volume is known to be above a line; 200,000 joint prior draws, correlation kept; THB per draw, standard error in brackets). On B: scale always minus 406,200 (4,600); line at 3 units plus 5,500 (3,700); line at the point-value break-even 2.19 minus 171,500 (4,300); line at the B break-even plus 53,900 (3,200). On A: scale always plus 491,200 (4,800); line at 3 units plus 570,800 (3,900); line at 2.19 plus 612,500 (4,400). On D: never scale 0; line at 3 units minus 332,700 (2,900); line at the D break-even minus 40,000 (1,500), which is negative because the kept correlation moves the true break-even above 5 units (8.76 units). These agree with the verifier's check (the 3-unit line on B pays about zero and the 2.19 line loses about THB 0.17 million).

### 4.2 Posterior by week: the average of 300 simulated 20-store pilots per truth, and one representative pilot

The requested evolution is the average path with its spread across pilots, not one pilot. Each cell below is the mean over 300 simulated pilots (2,000 particles each; Monte Carlo standard error of the mean at most 0.005). The prior predictive P(NPV above 0) is 0.580 (A), 0.399 (B) and 0.262 (D). The chart smc_pilot_posterior_fan.png shows the same paths with the 10th to 90th percentile bands beside the single pilot.

P(NPV above 0 given the pilot data), mean at weeks 1 / 4 / 8 / 13, and the 10th to 90th percentile across pilots at week 13:

| True demand (units a store-week) | Variant | Weeks 1 / 4 / 8 / 13 (mean) | Week 13: 10th to 90th percentile | Pilots with P at or above 0.95 at week 13 |
|---|---|---|---|---|
| 1.5 | A | 0.30 / 0.24 / 0.23 / 0.22 | 0.14 to 0.30 | 0 of 300 |
| 1.5 | B | 0.19 / 0.14 / 0.13 / 0.13 | 0.08 to 0.18 | 0 of 300 |
| 1.5 | D | 0.10 / 0.07 / 0.07 / 0.06 | 0.03 to 0.10 | 0 of 300 |
| 3.0 | A | 0.59 / 0.60 / 0.60 / 0.60 | 0.51 to 0.67 | 0 of 300 |
| 3.0 | B | 0.42 / 0.42 / 0.42 / 0.42 | 0.34 to 0.49 | 0 of 300 |
| 3.0 | D | 0.28 / 0.28 / 0.28 / 0.28 | 0.21 to 0.34 | 0 of 300 |
| 4.5 | A | 0.76 / 0.78 / 0.78 / 0.79 | 0.74 to 0.83 | 0 of 300 |
| 4.5 | B | 0.57 / 0.60 / 0.60 / 0.61 | 0.56 to 0.66 | 0 of 300 |
| 4.5 | D | 0.43 / 0.45 / 0.45 / 0.46 | 0.41 to 0.51 | 0 of 300 |

Posterior expected NPV at week 13 (THB million), mean and 10th to 90th percentile across pilots:

| True demand | A | B | D |
|---|---|---|---|
| 1.5 | -1.05 (-1.31 to -0.80) | -1.49 (-1.67 to -1.30) | -1.48 (-1.58 to -1.37) |
| 3.0 | +0.46 (-0.02 to +0.89) | -0.39 (-0.74 to -0.08) | -0.86 (-1.05 to -0.68) |
| 4.5 | +2.06 (+1.52 to +2.69) | +0.77 (+0.38 to +1.22) | -0.20 (-0.42 to +0.06) |

P(demand at or above 3), mean and 10th to 90th percentile across pilots, weeks 1 / 4 / 8 / 13: true 1.5, 0.01 / 0.00 / 0.00 / 0.00; true 3.0, 0.48 (0.14 to 0.86) / 0.48 (0.13 to 0.87) / 0.49 (0.10 to 0.90) / 0.49 (0.05 to 0.89); true 4.5, 0.95 / 1.00 / 1.00 / 1.00. The mean 90 percent band for demand (log width, true 3.0) is 0.53 at week 1, 0.42 at week 4, 0.38 at week 8 and 0.34 at week 13; it stops narrowing at about week 6 (0.35), because the pilot-level offset (sd 0.30 over the square root of the store count) is not identified by the counts and the weekly random walk keeps adding noise.

Reading:
- Almost all of the movement happens in the first four weeks. At a true 3.0 the mean P(NPV above 0) is the same at week 1 and week 13 on every basis (B 0.42, D 0.28, A 0.60) because the posterior mean demand is unbiased; the information shows in the spread across pilots, which narrows from 0.34 to 0.50 at week 1 to 0.37 to 0.48 at week 4 on B and does not narrow after that. At a true 1.5 the mean falls from the prior 0.40 (B) to 0.19 at week 1, 0.14 at week 4 and 0.13 at week 13.
- The pilot separates the truths through this probability: on B the week-13 bands (0.08 to 0.18, 0.34 to 0.49, 0.56 to 0.66) do not overlap.
- No simulated pilot reaches 0.95 on any basis at any truth. Even at a true 4.5 units the 90th percentile is 0.66 on B and 0.51 on D (0.83 on A), because fixed cost, price, the cost lines and cannibalisation are not learned from demand counts. The pilot therefore cannot make the NPV significantly positive on its own; it moves the probability within about 0.06 to 0.8.

One representative pilot per truth (as in the earlier passes; 200,000 particles). The single-pilot weeks move by up to about 0.1 around the averages above, which is the noise the 300-pilot average removes:

| Truth (units a store-week) | P(NPV above 0), variant B, weeks 1 / 4 / 8 / 13 | Variant D | Variant A | P(demand at or above 3), weeks 1 / 4 / 8 / 13 | Posterior demand at week 13: median (5th to 95th) | Realised national demand at week 13 |
|---|---|---|---|---|---|---|
| 1.5 | 0.29 / 0.21 / 0.17 / 0.18 | 0.17 / 0.12 / 0.09 / 0.09 | 0.44 / 0.34 / 0.29 / 0.30 | 0.04 / 0.00 / 0.00 / 0.00 | 1.77 (1.47 to 2.13) | 1.47 |
| 3.0 | 0.37 / 0.43 / 0.39 / 0.39 | 0.23 / 0.29 / 0.25 / 0.26 | 0.54 / 0.61 / 0.57 / 0.57 | 0.23 / 0.56 / 0.25 / 0.25 | 2.80 (2.36 to 3.32) | 3.00 |
| 4.5 | 0.53 / 0.53 / 0.57 / 0.59 | 0.38 / 0.38 / 0.42 / 0.44 | 0.71 / 0.72 / 0.76 / 0.78 | 0.92 / 0.99 / 1.00 / 1.00 | 4.33 (3.67 to 5.10) | 4.99 |

The week-13 values of the single pilots lie inside the 10th to 90th percentile bands above, except that the pilot at a true 1.5 sits at the 90th percentile (its posterior median demand is 1.77 against an average of 1.53). The 200,000-particle mapping and the exact conditional mapping used for the 300-pilot average agree to within 0.005 on these pilots.

### 4.3 Operating characteristics of the rule as written (two reads at weeks 8 and 13, line at 3 units; 300 pilots per cell, Monte Carlo SE up to 0.03)

Each cell is P(scale) / P(stop); the remainder is hold.

| Stores | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 5.0 |
|---|---|---|---|---|---|---|
| 5 | 0.01 / 0.97 | 0.09 / 0.76 | 0.35 / 0.38 | 0.69 / 0.12 | 0.91 / 0.04 | 0.99 / 0.00 |
| 10 | 0.00 / 1.00 | 0.05 / 0.81 | 0.37 / 0.37 | 0.78 / 0.08 | 0.96 / 0.01 | 1.00 / 0.00 |
| 15 | 0.00 / 1.00 | 0.03 / 0.89 | 0.31 / 0.37 | 0.81 / 0.07 | 0.97 / 0.01 | 1.00 / 0.00 |
| 20 | 0.00 / 1.00 | 0.02 / 0.91 | 0.35 / 0.39 | 0.86 / 0.08 | 1.00 / 0.00 | 1.00 / 0.00 |
| 30 | 0.00 / 1.00 | 0.01 / 0.94 | 0.32 / 0.40 | 0.91 / 0.03 | 1.00 / 0.00 | 1.00 / 0.00 |
| 40 | 0.00 / 1.00 | 0.01 / 0.94 | 0.34 / 0.38 | 0.90 / 0.02 | 1.00 / 0.00 | 1.00 / 0.00 |

The rule's own outcome at 20 stores, set against what each true demand is worth (the false-scale and false-stop rates follow from reading across):

| True demand | P(scale) | P(stop) | P(hold) | A: expected NPV (THB m), P(NPV above 0) | B | D |
|---|---|---|---|---|---|---|
| 2.0 | 0.00 | 1.00 | 0.00 | -0.57, 0.37 | -1.14, 0.23 | -1.28, 0.13 |
| 2.5 | 0.02 | 0.91 | 0.07 | -0.06, 0.50 | -0.76, 0.34 | -1.07, 0.21 |
| 3.0 | 0.35 | 0.39 | 0.27 | +0.46, 0.61 | -0.39, 0.43 | -0.86, 0.28 |
| 3.5 | 0.86 | 0.08 | 0.06 | +0.97, 0.69 | -0.02, 0.50 | -0.65, 0.35 |
| 4.0 | 1.00 | 0.00 | 0.00 | +1.48, 0.75 | +0.35, 0.56 | -0.43, 0.41 |
| 4.5 | 1.00 | 0.00 | 0.00 | +2.00, 0.79 | +0.72, 0.61 | -0.22, 0.46 |
| 5.0 | 1.00 | 0.00 | 0.00 | +2.51, 0.82 | +1.09, 0.65 | -0.01, 0.50 |
| 6.0 | 1.00 | 0.00 | 0.00 | +3.53, 0.87 | +1.83, 0.71 | +0.41, 0.56 |

- The rule is a demand screen with its midpoint near 3.15 units. At 20 stores P(scale) is 0.10 at 2.62 units, 0.50 at 3.15 and 0.90 at 3.65; the zone narrows slowly with more stores (at 40 stores 2.63, 3.14, 3.52) because store offset and weekly drift set a floor.
- False scale (scaling when the expected NPV is negative). On A the rule scales only above the break-even in practice (0.02 at 2.5 units). On B the false-scale rate is 0.35 at 3.0 units (expected NPV minus THB 0.39 million) and 0.86 at 3.5 (about zero). On D the false-scale rate is 0.35 at 3.0, 0.86 at 3.5 and 1.00 at 4.0 and 4.5, where the expected NPV is minus THB 0.86 to minus 0.22 million. A rule that waits for the D break-even instead would scale 0.50 at 5.0 units.
- False stop (stopping when the expected NPV is positive). On A the rule stops 0.39 of pilots at a true 3.0 units, where the expected NPV is plus THB 0.46 million. On B and D, with true demand above the break-even, the stop rate is 0.00 to 0.08.
- A one-read rule at the same line scales 0.49 (week 8) and 0.47 (week 13) at 3.0 units and 0.91 and 0.88 at 3.5; the second read moves the effective line from 3.0 to about 3.15.
- The two reads are correlated (phi 0.35, 0.47 and 0.68 at 2.5, 3.0 and 3.5 units), so the AND rule is less strict than two independent reads would be.
- Bayes rule (scale if the posterior mean demand is at or above the break-even of the basis; 20 stores, week 13): P(scale) at 2.5, 3.0 and 3.5 units is 0.41, 0.91 and 0.98 for A; 0.00, 0.11 and 0.54 for B; 0.00, 0.00 and 0.00 for D (0.50 at 5.0 units).

### 4.4 Separation of truths (power at week 13, 300 pilots per cell, Monte Carlo SE 0.01 to 0.03; midpoint rule 0.9 and 0.1)

| Stores | 1.5 against 3.0 | 3.0 against 4.5 (not a decision pair) | 1.5 against 4.5 |
|---|---|---|---|
| 5 | 0.61 | 0.35 | 0.82 |
| 10 | 0.75 | 0.49 | 0.95 |
| 15 | 0.81 | 0.64 | 0.99 |
| 20 | 0.88 | 0.69 | 0.99 |
| 30 | 0.93 | 0.72 | 1.00 |
| 40 | 0.96 | 0.78 | 1.00 |

- Weeks. The grid tests weeks 4, 6, 8, 10, 12 and 13. For the decision pairs the power is 0.82 at 15 stores and 0.90 at 20 stores by week 4 and changes by at most 0.04 between week 4 and week 13 at 15 to 40 stores (SE 0.02), so the weeks after about 4 add little. The evolution run reads every week (300 pilots per truth, scored on the start label): for 1.5 against 3.0 the power at weeks 1 to 5 is 0.51, 0.83, 0.88, 0.93 and 0.95 at 20 stores, so 80 percent power is reached at week 2 (0.83) at 20 stores, and at week 1 (0.83) at 40 stores. Ten stores never reach 0.80 (best 0.797 at week 10 on the weaker pair; 0.75 at week 13). For 3.0 against 4.5 the power reaches 0.84 at 40 stores by week 4 (0.88 at week 5 in the evolution run) and then falls to 0.78 by week 13 (0.80 in the evolution run).
- Scoring convention check. The pairs were also scored against the realised national level at the read week instead of the start-of-pilot label (a pilot is confidently right if P(demand above the midpoint) is at least 0.9 when its level at that week is above the midpoint, at most 0.1 when below). The power changes by at most 0.003 at 20 and 40 stores. The fall after week 5 for 3.0 against 4.5 is therefore not a labelling effect: the level itself drifts (standard deviation of the log level 0.073 by week 13 at the assumed weekly noise of 0.02), which moves some pilots toward the midpoint 3.75, and it depends on the assumed drift (with weekly noise 0.005 the week-13 power for this pair at 40 stores is 0.89). The weeks-needed result for the decision pairs does not depend on the scoring convention.
- Pairs that straddle each basis's expected-NPV break-even, one unit apart (power at week 13): A 2.0 against 3.0, 0.35 / 0.48 / 0.57 / 0.63 / 0.72 / 0.80 at 5 / 10 / 15 / 20 / 30 / 40 stores; B 3.0 against 4.0, 0.22 / 0.34 / 0.39 / 0.50 / 0.55 / 0.63; D 4.5 against 5.5, 0.15 / 0.29 / 0.34 / 0.35 / 0.51 / 0.52. Only the lowest break-even (A) is resolved to within one unit, and only at 40 stores. The pilot is a screen of demand, not an instrument for the economic break-even.
- Sensitivity to the drift (weekly noise 0.005), power at week 13 for 1.5 against 3.0 and 3.0 against 4.5: 10 stores 0.84 and 0.45; 20 stores 0.94 and 0.76; 30 stores 0.98 and 0.79; 40 stores 1.00 and 0.89.
- Sensitivity to store-to-store variation, power at week 13 for 1.5 against 3.0 with store log-sd 0.15 and 0.50: 10 stores 0.85 and 0.66; 15 stores 0.95 and 0.74; 20 stores 0.94 and 0.78; 30 stores 0.96 and 0.88; 40 stores 0.99 and 0.89.
- Recommended count, at halving resolution only. The decision-pair criterion is first met at 15 stores (power 0.81, SE 0.02; false scale at 1.5 equal to 0.00 and false stop at 4.5 equal to 0.00), by less than one standard error. Fifteen stores cannot be told from 10 stores (0.75; difference 0.06, z 1.7). Twenty stores is above both (0.88; z 2.4 against 15 and 4.1 against 10), and 30 stores is above 20 (0.93; z 2.3). Proposed count for Route A: 20 stores (0.88 in the base case, 0.94 with low drift, 0.78 with store log-sd 0.50); 30 stores if store-to-store variation is high (0.88). Under an all-pairs criterion no tested count qualifies, because 3.0 against 4.5 stays below 0.80 up to 40 stores, so the count resolves a halving of demand and not the 3-unit line itself. The headline power depends on the three unsourced noise parameters (store sd, drift, negative binomial size); the range for 1.5 against 3.0 at 20 stores is 0.78 to 0.94.

### 4.5 Repeat-floor rule (two cohorts of n first buyers; flat Beta(1, 1) posterior; a cohort passes if P(repeat at or above 15 percent) is at least 0.5)

| Cohort size | True repeat 10 percent: scale / stop | 15 percent: scale / stop | 20 percent: scale / stop | 30 percent: scale / stop |
|---|---|---|---|---|
| 100 | 0.005 / 0.86 | 0.29 / 0.21 | 0.84 / 0.007 | 1.00 / 0.00 |
| 200 | 0.0002 / 0.97 | 0.28 / 0.22 | 0.945 / 0.0007 | 1.00 / 0.00 |
| 400 | 0.000 / 1.00 | 0.27 / 0.23 | 0.99 / 0.0001 | 1.00 / 0.00 |

Reading: a true repeat of 15 percent, exactly at the floor, is indistinguishable from noise at any cohort size tested (scale about 0.28, stop about 0.22, hold about 0.50). Repeat of 10 or 20 percent is separated at 200 buyers per cohort. The floor should be read as a band, 10 to 20 percent, not as a line.

### 4.6 Value of the pilot and of waiting, like for like (20 stores; 10,000 truths drawn from the prior; pilot world)

Payoff is the expected NPV of the decision: a rule that scales earns the expected NPV at the true demand (the other inputs integrated out exactly, so the only noise is in the truth and the pilot), and a rule that does not scale earns zero. "No pilot" scales if the prior expected NPV is positive (A) and does not scale otherwise (B, D). The Bayes rule scales if the posterior mean demand is at or above the basis's expected-NPV break-even. Standard errors in brackets.

| Rule | A: value (THB thousand) | B | D |
|---|---|---|---|
| No pilot | 640 (13) | 0 (0) | 0 (0) |
| One read at week 8, line 3 | 784 (11) | 218 (6) | -182 (4) |
| One read at week 13, line 3 | 782 (11) | 213 (6) | -187 (4) |
| Two reads (weeks 8 and 13), line 3 | 766 (11) | 231 (6) | -152 (4) |
| Bayes rule at week 8 (own basis) | 825 (11) | 251 (6) | 31 (2) |
| Bayes rule at week 13 (own basis) | 822 (11) | 249 (6) | 31 (2) |
| Perfect knowledge of demand | 839 (11) | 264 (6) | 36 (2) |

Paired differences, with standard errors (THB):

| Comparison | A | B | D |
|---|---|---|---|
| Bayes rule, week 13 minus week 8, scored on the start-of-pilot level (the second-pass convention; see the next table for the others) | -2,767 (804) | -2,156 (690) | -913 (395) |
| One read at week 13 minus one read at week 8 (same line) | -2,161 (1,570) | -4,821 (1,275) | -5,589 (2,392) |
| Two reads minus one read at week 13 (stringency, not waiting) | -16,329 (1,038) | +17,341 (974) | +35,369 (1,748) |
| Bayes rule at week 8 minus no pilot (value of the demand read) | +185,343 (3,647) | +250,954 (5,894) | +31,426 (1,718) |
| Two reads (proposed) minus no pilot | +125,863 (4,395) | +230,710 (6,072) | -151,777 (3,555) |

- The first pass reported plus THB 15,193 (standard error 4,710) as the value of waiting. That was two reads at week 13 minus one read at week 8, so it measured a stricter line. With the first-pass estimator (a realised NPV draw per truth) and 10,000 truths, two reads minus one read at week 8 is plus 13,828 (3,708) on B, plus 30,442 (3,186) on D and minus 17,527 (3,740) on A, which reproduces the effect; one read at week 13 minus one read at week 8 is minus 3,367 (5,190) on B. The weekly break-even cost of THB 3,039 inherited the confusion and is withdrawn.
- The value of the demand read is THB 0.19 million (A; Bayes week 8 minus no pilot is 185,000, against a perfect-knowledge gain of 199,000), THB 0.25 million (B; 251,000 against 264,000) and THB 0.03 million (D; 31,000 against 36,000). The Bayes rule at week 8 captures 93, 95 and 87 percent of those gains. The values are robust to the store-equivalent count: the week 8 read is worth 194,700 (A), 261,100 (B) and 36,200 (D) at N_EFF 1,000, and 183,800, 266,700 and 38,700 at 2,000 (3,000 truths each).
- Value of waiting, under three scoring conventions. The second pass scored every rule on the start-of-pilot level (the truth), although the filter tracks the level at the read week; waiting is then penalised by construction, because drift between the start and the read week is noise that a longer wait accumulates. The verifier's rescoring on the level at the decision week flips the sign. Three conventions are reported on 40,000 truths (10,000 in the main run and 30,000 in an independent run with its own random stream; paired differences, Bayes rule at week 13 minus week 8, THB, standard error in brackets):

| Convention | A | B | D |
|---|---|---|---|
| Start-of-pilot level (second pass) | -3,541 (372) | -3,281 (351) | -1,184 (193) |
| Level at each rule's own decision week | +4,909 (798) | +3,283 (537) | +790 (228) |
| Common week-13 level (pure information comparison) | +2,020 (345) | +2,043 (325) | +603 (169) |
| Level at the decision week, week-13 rule after the five-week delay discount | -2,772 (793) | +878 (534) | +461 (227) |
| Common week-13 level, after the delay discount | -5,661 (349) | -362 (325) | +274 (169) |

  The two samples agree in sign and size (10,000 truths: decision-time level plus 6,948 (1,608) on A, plus 4,896 (1,072) on B, plus 859 (457) on D; the verifier's own run on 10,000 truths gave plus 2,932 (1,597), plus 1,762 (1,105) and plus 1,027 (467), within about two standard errors on A and B and the same on D). The delay discount is the factor 0.9909 at the prior mean rate (acting five weeks later), about THB 9,100 per THB 1 million of NPV; it is applied to the week-13 rule only.
- Reading the three conventions. The estimate runs from minus THB 5,700 to plus THB 4,900 and its sign depends on how the NPV is scored, so the model cannot say whether waiting from week 8 to week 13 helps or hurts. In every cell it is at most 3.8 percent of the value of the demand read (A 2.6, B 1.3, D 3.8 percent) and at most THB 5,700. The second pass's claim that waiting loses value is dropped; the conclusion that waiting adds nothing material stands. Week 8 captures the information about demand; week 13 serves the repeat and cannibalisation reads and confirmation.
- The 3-unit rules add value on A (plus THB 0.13 to 0.14 million against scaling without a pilot) and on B (plus 0.21 to 0.23 million), because they scale mostly where the expected NPV is positive, and they lose value on D (minus THB 0.15 to 0.19 million), because on D the expected NPV stays negative until about 5 units while the rules scale from about 3. The result depends on where the line sits against the break-even of the basis, so it depends on the store-equivalent count: at 2,000 store-equivalents the 3-unit line is 312,000 cubes a year, above the A and B break-evens (1.64 and 2.26 units), and the one-read rules then lose THB 0.26 million on A against scaling without a pilot (395,000 against 657,000, because they stop projects worth scaling) while earning 198,000 on B and 36,000 on D.
- Pilot running costs are not set; the value is gross of them, and pilot spend is a stated limit (section 6). What the pilot learns about cannibalisation, price and cost lines is not valued here (the pilot informs demand only in this model). Under the stated ranges the cannibalisation share explains about 5 percent of the variance of the NPV on the lead basis (first-order index 0.048; fixed cost 0.36 and shelf price 0.23) and its value of perfect information is nil in section 3.1, so this model does not show that the cannibalisation read is where the pilot's value lies. At the base inputs any share above about 7.5 percent turns the NPV negative (record 75), which is a point-value statement. The cannibalisation read is simply not priced here.

## 5. Significance conclusions (part C)

### (i) Is the projected NPV significantly greater than zero under the stated input uncertainty?

No. Under the test fixed in advance:
- Variant B (pre-registered headline): P(NPV above 0) = 0.399 (SE 0.001), below 0.95. The 90 percent interval is minus THB 3.64 million to plus THB 3.03 million, which includes zero.
- Variant A (record 05 structure): 0.580; interval minus 2.72 to plus 4.14 million.
- Variant D (record 75 lead basis, after excise and after tax): 0.262; interval minus 3.40 to plus 1.59 million.
- The other variants (C 0.370, A2 0.445, B2 0.267, D_cf 0.261, B_wide 0.403, D_wide 0.267, B_rho0 0.411) all fail the rule and all include zero in the 90 percent interval.

Conditions. All conclusions depend on the stated priors, which are ASSUMPTION or PROXY values. They are not findings from market data. The 0.95 threshold is a standard set in advance, not derived from data. The base-case values in the deck (THB 0.88 million; THB 0.17 million on the lead basis) are point values at input medians, not expected values.

What would change the conclusion. Learning fixed cost or shelf price in their tails (section 3.1) and a joint restriction (section 3.2). The input whose narrowing moves P(NPV above 0) most is fixed cost on both B and D by the variance index (0.31 and 0.36); by the value of information, shelf price and fixed cost tie on B (about THB 0.23 million each) and fixed cost leads on D. The pilot cannot supply either: it informs volume, and even a volume known to be 6 units a store-week leaves P(NPV above 0) at 0.71 on B and 0.56 on D. In the simulated pilots no pilot reaches 0.95 on any basis at any of the three truths (0 of 300 in every cell, section 4.2): the pilot separates demand levels and cannot make the NPV significant.

### (ii) Is the segment lead (men 25 to 34 over men 35 to 44) statistically significant?

No.
- Existing ratio (record 47, sampling error on the odds ratio only): median 1.041; 90 percent interval 0.998 to 1.085; P(ratio above 1) = 0.941. The lower bound touches 1 and the probability is below 0.95.
- Synthesis (record 49, 30 percent baseline, odds scale): median lead 0.61 points; P(lead above 0) = 0.941; P(lead of 5 points or more) = 0.00.
- Proper test at the affordable sample (1,377 completes per cell, two-proportion test, alpha 0.05, 30 percent baseline): power 0.064, 0.081 and 0.105 for leads of 0.6, 0.9 and 1.2 points (two-sided); 0.096, 0.129 and 0.168 one-sided. Minimum detectable difference at 80 percent power: 4.99 points.
- Sample for 80 percent power: 23,149 per cell for a 1.2-point lead; 33,274 for 1.0 point; 22,040 for 1.23 points (close to the 22,166 in record 49 and submission 12, which was computed at about 1.23 points); 41,042 for 0.9; 92,088 for 0.6.

The lead is directional under the stated inputs and not established. The survey cannot establish it at 1,377 per cell.

### (iii) Are the pilot rule thresholds distinguishable from noise at the planned sample?

Partly.
- The 3-unit two-read rule separates demand levels one unit apart around the line at 15 to 20 stores: at 20 stores a true 2.5 units is stopped in 91 percent of pilots and a true 3.5 is scaled in 86 percent. At the line, the outcome is close to a three-way split (scale 0.35, stop 0.39, hold 0.27), which is what a threshold does.
- Halving demand (1.5 against 3.0) is told apart with power 0.81 at 15 stores and 0.88 at 20 stores by week 13 (Monte Carlo SE 0.02; about 0.8 and 0.9); week 4 is enough, and the week-by-week run reaches 0.83 at week 2 at 20 stores. The power depends on assumed store and weekly variation: 0.78 to 0.94 at 20 stores. Fifteen stores cannot be told from 10 (0.75) at 300 pilots a cell; 20 can.
- The rule does not separate 3.0 from 4.5 at any store count tested, and it cannot place demand relative to the economic break-even to within one unit except on the lowest break-even at 40 stores.
- Distinguishable from noise is not the same as correct economically. The 3-unit line is below the expected-NPV break-even on B (3.5 units) and D (5.0 units) and above it on A (2.6 units). The line is a necessary condition for scale, not a profit test.
- The 15 percent repeat floor is not distinguishable from noise at 100 to 400 buyers per cohort; repeat of 10 or 20 percent is distinguishable at 200 buyers per cohort.
- The THB 3.51 contribution floor is breached in 36 percent of prior draws on B (34 percent against the THB 2.54 after-excise floor on D). It is an economics test the pilot does not inform.

## 6. Proposed settings and the store count

These are the settings the team proposes, with basis and tier. The team confirms them before the slides change.

- Store count for Route A: 20 stores, at halving resolution. Basis: the decision-pair criterion is met at 15 stores (power 0.81, SE 0.02), which is not distinguishable from 10 stores (0.75; z 1.7), and with margin at 20 (0.88; z 2.4 against 15); use 30 stores if store-to-store variation is high (0.88 at log-sd 0.5). The count separates a halving of demand from the 3-unit target; it does not resolve demand near the 3-unit line itself (3.0 against 4.5 stays below 0.80 up to 40 stores). Tier: DERIVED on ASSUMPTION noise inputs.
- Scale line: keep 3 units a store a week on two reads, as in the plan, and treat it as the demand target and a necessary condition. The first pass proposed moving it to 2.2; that is withdrawn (section 4.1). Basis: 3 units a store-week is 200,000 cubes a year at 1,282 store-equivalents, the base scenario of record 05; 1,282 is the count implied by those two numbers (ASSUMPTION; 8.0 percent of about 15,945 7-Eleven stores as context). The line sits above the expected-NPV break-even on the record 05 structure (2.55 units) and below it on the full prior (3.53) and the lead basis (5.03), with price and volume independent; with the link kept the break-evens are 2.40, 4.09 and 8.76, and at 1,000 to 2,000 store-equivalents the lead-basis figure is 6.4 to 3.2. Tier: ASSUMPTION (the store-equivalent count). Scale is then a joint decision: demand at the line, repeat at or above 15 percent on both cohorts, contribution at or above THB 3.51 a cube (THB 2.54 after excise), and a cannibalisation share below the break-even share for the adopted basis (7.5 percent at 200,000 cubes on the lead basis, record 75). The team proposes that the measured decision compares the observed demand and cannibalisation share with the break-even demand and break-even share of the adopted basis. Tier: DERIVED on ASSUMPTION inputs.
- Repeat floor: read as a band, 10 to 20 percent, not a line at 15 percent. At 200 first buyers per cohort a true 20 percent passes in 95 percent of cohort pairs and a true 10 percent in fewer than 1 in 1,000.
- Reads: the demand read at week 8 captures the information about demand; week 13 serves the repeat and cannibalisation reads and confirmation. The model puts the value of waiting from week 8 to week 13 between minus THB 5,700 and plus THB 4,900 depending on the scoring convention (section 4.6), which is not distinguishable from zero in practice. Tier: DERIVED (section 4.6); the read weeks are an ASSUMPTION.
- Click-to-purchase threshold (replaces the hand-off to Singha Corporation): the team proposes that Route B paid media starts only when the non-paid click-to-first-purchase read reaches 1.0 percent. Basis: the desk base in submission/10 line 109 (1.0 percent click-to-first-purchase). Tier: ASSUMPTION. At THB 11.5 a click (S, PROXY, one agency's 2025 figure) a 1.0 percent rate is about THB 1,150 a first purchase and about 234 cubes to recover at THB 4.91 (submission/10, DERIVED), so Route B does not recover its first-purchase cost in one serve even at the threshold; the threshold is a start gate for a learning read, not a profit test.
- Pilot spend (replaces "one budget still to be set"): a stated limit. No pilot cost is sourced (cost per sample THB 15 and a sample-to-trial rate of 10 percent are ASSUMPTIONS in submission/10), so the spend is not sized from sources. The model's value of the demand read is THB 0.03 million (lead basis) to THB 0.25 million (full prior, before excise), gross of costs (section 4.6); a spend above that is justified only by what the pilot measures beyond demand (repeat, contribution, cannibalisation share), which the model does not price. Tier: DERIVED on ASSUMPTION inputs; pilot costs UNVERIFIED.
- Drift and store variation are the limits on the 3.0 against 4.5 pair. Sizing the pilot for that pair would need more than 40 stores and a lower drift, neither of which is sourced.

## 7. Finished slide 10 and slide 11 text (judge-facing; proposed, not placed)

These replace the slide 10 and slide 11 text in rework/deck/deck_content.md when the lead approves them, and they replace the slide 10 text proposed in record 75 section 7. They are on the record 75 lead basis (after excise, after tax) and keep every item of the current slides; the before-excise figures appear once, labelled. Each slide is cut to the headline figures: about 370 words on slide 10 and about 400 on slide 11 (same count, excluding speaker notes, as the current 240 and 300; the second pass's text was about three times the current length). The increase over the current slides is the uncertainty result and the stated limits that replace the hand-offs; the detail sits in the speaker note and in the appendix text after the slides. Ranges use "to". No dashes or middle dots.

### Slide 10. Valuation and shareholder value

- **Title:** At the base inputs the cube adds THB 0.17 million after tax, but across the stated input ranges the chance of a positive NPV is about one in four.
- **Exhibit left:** NPV after tax in THB million against annual cubes, at THB 500,000 fixed cost and THB 3.94 a cube after excise: 50,000 cubes, minus 1.41; 184,325, 0 (break-even); 200,000, 0.17 (base case); 500,000, 3.32; 1,000,000, 8.59. The before-excise, pre-tax values are in the appendix.
- **Exhibit middle (stated uncertainty):** the chance of a positive NPV over 200,000 draws of every input is 0.26 after excise and tax (0.40 before; 0.58 on a simpler structure). The test set in advance needs 0.95; none reaches it, and every 90 percent range includes zero. The expected NPV after excise and tax is minus THB 0.88 million.
- **Exhibit right (value drivers):**
  1. Contribution: THB 3.94 a cube after excise (THB 4.91 before).
  2. Cannibalisation: the NPV turns negative above about 7.5 percent of cube buyers who would otherwise buy a can.
  3. Volume: break-even 184,325 cubes a year; base 200,000; expected NPV zero at about 335,000 across the ranges.
  4. Fixed cost and shelf price carry most of the spread; the NPV stays positive up to THB 0.54 million a year of fixed cost.
  5. Option: the pilot reads demand after 13 weeks and can stop (worth THB 0.03 million to THB 0.25 million in the model); pilot spend is not sized from sources (a stated limit).
- **Scale note:** Singha Corporation's 2025 net profit was about THB 3,085 million (MGR Online, 23 May 2026, S); the base-case NPV is about 0.005 percent of it, so the case rests on volume, cannibalisation and fixed cost. The pass-through to Boon Rawd Brewery rests on a holding that was not found (appendix).
- **Source line:** Desk model: five years, 10% discount rate, no terminal value; 20% tax (Revenue Department page, updated 23 November 2020), setup cost depreciated over five years; year 0 carries one year of fixed cost and year 1 sells half the base volume (assumptions). 200,000 Monte Carlo draws, fixed seed, conditional on the stated ranges; not market data. Payback about 3.3 years after tax and excise.
- **Speaker note:** Say that the base case is small and positive when every input sits at its middle value, and that the chance of a positive NPV does not reach the 0.95 set before the analysis was run, on any basis. At the base inputs a cannibalisation share above about 7.5 percent turns the value negative; across the stated range the chance that the share is above 7.5 percent is 0.92. Across the stated ranges, though, fixed cost and shelf price explain most of the spread (about 36 and 23 percent of the variance after excise and tax), and the pilot measures neither. The pilot's value therefore rests on the demand read, which the model prices at THB 0.03 to 0.25 million, and on the cannibalisation and repeat reads, which the model does not price. The expected-NPV break-even of about 335,000 cubes assumes price and volume are independent (about 584,000 if a higher price is assumed to lower volume) and about 1,282 stores behind 200,000 cubes. Say that the ranges are assumptions and not market data.

### Slide 11. Pilot

- **Title:** A 20-store pilot can tell a halving of demand from the 3-unit target, but demand alone does not settle the economics.
- **On the slide (three columns):**
  - **Concept pre-test, M3 to M5:** recruited online panel of men aged 25 to 59 who drank alcohol in the past year; one brand-blind concept signed off by M3; top-2-box purchase intent by age cell at one test price (THB 15, assumption); rule fixed in advance; it reads direction and a 5-point size rule, and it cannot confirm the modelled 1.2-point lead; no media, no sale.
  - **Pilot, two routes, M7 to M10 (13 weeks):** click-to-purchase read on non-paid traffic in the first four weeks; Route A in-store trial in 20 stores, read at weeks 8 and 13: scale if both are at or above 3 units per store per week, stop if both are below, otherwise hold; Route B paid social to one listing only if the click-to-first-purchase read reaches 1.0% (assumption), and at base inputs it does not recover its first-purchase cost in one serve (derived); repeat read at 8 and 12 weeks.
  - **Measured decision, M10 to M11:** scale one route, repeat once in the same stores, or stop; scale needs repeat of 15% or more on both cohorts, contribution of THB 3.51 or more per cube (THB 2.54 after excise) and a cannibalisation share below its break-even; national listing is read at about M13.
- **What 20 stores can show:** a true 2.5 units is stopped in about 90% of simulated pilots and a true 3.5 is scaled in about 85%; a halving of demand is told apart with about 90% power. Three units is a target and a necessary condition, not a profit test.
- **Survey box:** a screening test at 1,377 completes per cell for a 5-point lead at a 30% baseline. The modelled lead is about 1.23 points, which would need about 22,000 per cell. At 1,377 per cell the test confirms the direction of the lead in 12.7% of simulated runs and rules out a 5-point lead in 56.4%. Fieldwork waits for Gate 1; panel provider and cost are not sized from sources (a stated limit).
- **Source line:** Simulated pilots under stated assumptions, not pilot data (store-to-store variation 0.30, weekly drift 0.02). Cost per click THB 11.5 (proxy, one agency); cost per thousand impressions THB 120 (assumption).
- **Speaker note:** Say that the survey is a screen and that no market is sized from it; the existing survey model gives a probability of 0.94 that men aged 25 to 34 lead, below the 0.95 set in advance, and the 12.7 percent averages over the uncertainty in the lead. Say that the pilot is the test of demand and that it does not measure fixed cost, price or margin, which come from quotes and the market. Three units a store a week is 200,000 cubes a year at an assumed 1,282 stores (the count implied by those two numbers, about 8 percent of the roughly 15,945 7-Eleven stores; an assumption). It is a target and a necessary condition. The demand at which the expected NPV is zero, with price and volume independent, is about 2.6 units on the simpler structure, 3.5 on the full ranges before excise and 5.0 after excise and tax; with a higher price assumed to lower volume it is 2.4, 4.1 and 8.8, and at 1,000 to 2,000 stores it is 6.4 to 3.2 units after excise and tax. Scale also needs repeat, contribution and a low cannibalisation share. The 90 percent power for a halving depends on assumed store and weekly variation (about 80 percent if store-to-store variation is high). The demand read has almost all of its value by week 8: the model puts the value of waiting to week 13 within a few thousand baht of zero, with a sign that depends on how it is scored, so week 13 serves the repeat and cannibalisation reads. Valued on demand alone the pilot is worth THB 0.03 million (after excise and tax) to THB 0.25 million (before) in expectation.

### Appendix text for slides 10 and 11 (detail moved off the slides; proposed for Appendix B or C)

Slide 10 detail. Before excise and before tax, at THB 4.91 a cube (NPV in THB million): 50,000 cubes, minus 1.58; 146,230, 0 (break-even); 200,000, 0.88; 500,000, 5.80; 1,000,000, 13.99. Cannibalisation: across the stated range the chance that the share is above 7.5 percent is 0.92 (the break-even share is 30.9 percent before excise). Fixed cost: the NPV stays positive up to THB 0.68 million a year before excise and tax. The chance of a positive NPV is 0.58 in the lowest-cost tenth of fixed-cost outcomes and 0.03 in the highest (after excise and tax); for shelf price, 0.03 in the lowest tenth and 0.51 in the highest. The 90 percent range of the NPV after excise and tax is minus THB 3.4 million to plus THB 1.6 million. Pass-through: if Boon Rawd Brewery held all of Singha Corporation and it paid out all profit, Boon Rawd Brewery would receive about THB 151,000 a year in years 2 to 5 (year 1 is a loss year with no dividend), and each 10 percent stake in Boon Rawd Brewery would receive about THB 15,000 a year before holder tax; neither the holding nor the payout was found in the sources read. Payback is about 2.1 years before excise and tax (3.3 after). The base-case NPV is about 0.03 percent of one year's profit before excise and tax (0.005 percent after). Discount rate: the policy rate of 1.00 percent plus a 9-point premium (an assumption). Incremental profit reaches 0.1 percent of Singha Corporation's 2025 profit only at about 1.1 million cubes a year with no cannibalisation (0.9 million before excise).

Valuation under the stated uncertainty (200,000 draws of every input; mean, 5th to 95th percentile and the chance of a positive NPV; Monte Carlo SE of the chance 0.001):

| Basis | Chance of a positive NPV | Mean (THB million) | 90 percent range (THB million) | Expected NPV is zero at (units a store a week; cubes a year) |
|---|---|---|---|---|
| Simpler structure, before excise, pre-tax | 0.58 | +0.49 | -2.72 to +4.14 | 2.6; 170,000 (2.4; 160,000 with the price and volume link) |
| Full ranges, before excise, pre-tax | 0.40 | -0.41 | -3.64 to +3.03 | 3.5; 235,000 (4.1; 272,000) |
| Full ranges, after excise and tax | 0.26 | -0.88 | -3.40 to +1.59 | 5.0; 335,000 (8.8; 584,000) |

The units a store a week assume 1,282 store-equivalents (at 2,000 the three figures are 1.6, 2.3 and 3.2 for price and volume independent; at 1,000, 3.3, 4.5 and 6.4). The second row subtracts the after-excise can contribution from a before-excise cube contribution, which flatters the cannibalised case; the third is consistent (both after excise), and the first has no cannibalisation term.

Pilot rule at 20 stores (300 simulated pilots per cell; both reads at weeks 8 and 13 at or above 3 units to scale, both below to stop):

| True demand (units a store a week) | Scale | Stop | Hold |
|---|---|---|---|
| 2.0 | 0.00 | 1.00 | 0.00 |
| 2.5 | 0.02 | 0.91 | 0.07 |
| 3.0 | 0.35 | 0.39 | 0.27 |
| 3.5 | 0.86 | 0.08 | 0.06 |
| 4.0 | 1.00 | 0.00 | 0.00 |

Repeat floor of 15 percent (two cohorts of 200 first buyers): a true repeat of 10 percent passes in fewer than 1 in 1,000 cohort pairs, 15 percent in 28 percent and 20 percent in 95 percent, so the floor is a band of about 10 to 20 percent.

Items of the current slides that the replacement text changes or drops (for the lead):
- Slide 10: the title; the payback of 2.1 years (now 3.3 after tax and excise in the source line; the before-excise 2.1 is in the appendix text); the THB 0.68 million fixed-cost ceiling (now THB 0.54 million after excise and tax; 0.68 is in the appendix text); the 0.03 percent scale note (now 0.005 percent after excise and tax; 0.03 percent before excise and tax is in the appendix text); the sentence that value accrues to Singha Corporation with no pass-through (replaced by the record 75 pass-through text); and "one budget still to be set (decision 9)", replaced by a stated limit on pilot spend (section 6).
- Slide 11: the title; "Route B ... only after Singha Corporation sets the cost threshold" (now "only if the click-to-first-purchase read reaches 1.0 percent (assumption)", section 6); "about 22,166 per cell" at "about 1.2 points" (now about 1.23 points and about 22,000 per cell); "Fieldwork waits for Gate 1 and for approval of the panel provider and budget" (now "Fieldwork waits for Gate 1", with the provider and cost as a stated limit). The click-to-purchase read, the repeat reads at 8 and 12 weeks, the national listing at M13, the 5-point size rule and the 12.7 and 56.4 percent figures are kept. The measured decision gains the THB 2.54 after-excise floor and the cannibalisation share.

## 8. Conflicts with the current deck and submission

1. Two different slide 10 replacements. Record 75 section 7 and record 77 (first pass) propose different slide 10 texts on different contribution bases (after excise and tax against before excise and tax). The lead must choose one basis. The 0.88, 0.58 and 0.40 figures belong to the before-excise basis; the 0.17 and 0.26 figures belong to the lead basis. Section 7 is written on the lead basis and merges the two.
2. Slide 10 and executive summary (deck_content.md line 29), submission 05 (lines 81 to 83, 95), submission 11 (lines 224 to 230): the base NPV of THB 0.88 million is the value at input medians, before excise and before tax. The expected NPV under the stated uncertainty is plus 0.49 million (A), minus 0.41 million (B) and minus 0.88 million (D). The deck's "desk case adds value only above 146,230 cubes a year" is a point-value statement; on the lead basis the point-value break-even is 184,325 cubes and the expected-NPV break-even is about 335,000 cubes.
3. Slide 11, submission 10 (lines 110 and 133) and submission 06 (line 43): the 3-unit line stays, but it is a demand target and a necessary condition. The expected-NPV break-even demand is 2.55, 3.53 and 5.03 units on A, B and D at an assumed 1,282 store-equivalents. The first pass's proposal to move the line to 2.2 is withdrawn.
4. Submission 06 line 49 sets the cannibalisation review at 50 percent. Record 75 puts the NPV break-even at 7.5 percent of cube buyers at 200,000 cubes on the lead basis, and the prior probability that the share exceeds 7.5 percent is 0.92 (exceeds 50 percent: 0.053). The review line is far above the share at which the NPV turns negative.
5. Record 49 says "a gap of about 1 point needs roughly 22,000 respondents per cell". By the same formula, 22,000 corresponds to about 1.23 points, and 1.0 point needs about 33,000. The wording should read "about 1.2 points needs about 22,000". The same figures appear in submission 10 (lines 13 and 162), submission 12 (lines 133 to 149) and deck slide 11.
6. Slide 11 survey box, record 49, submission 10 and submission 12 say the test at 1,377 per cell confirms the direction of the lead in 12.7 percent of simulated runs. This run gives 10.5 percent for a fixed 1.2-point lead (two-sided) and 16.8 percent (one-sided); the 12.7 percent averages over the uncertainty in the lead, so the two are not like for like. The slide should say which it quotes (section 7 does).
7. Submission 06 and submission 10 describe the repeat floor of 15 percent as a line. It is a band (section 4.5).
8. Velocity reads. Submission 10 says "two consecutive reads"; the model reads at weeks 8 and 13 (an ASSUMPTION), and the repeat reads are at 8 and 12 weeks. Consecutive weekly reads would be almost the same read; the plan should date the reads.
9. Record 75 section 6 says the pilot measures the cannibalisation share (submission 06: exit question). The model here lets the pilot inform demand only, so the pilot's modelled value is a lower bound on the lead basis. Record 75 and record 77 should be read together.
10. Slide 10 treats the value of waiting as an option. The like-for-like value of waiting from week 8 to week 13 is within minus THB 5,700 and plus THB 4,900 with a sign that depends on the scoring convention (section 4.6), and the demand read is worth THB 0.03 to 0.25 million. The first pass's "THB 15,200 and THB 3,000 a week" is withdrawn.
11. Record 56 (lines 88 and 195) tags the 20 percent tax as secondary. Record 75 (section 9, conflict 11, and conflict 19) reads the Revenue Department page through a page summary and tiers it S, naming the primary page, so record 56's S stands; this record and the T12 note use the same S. The second pass's "P (extract)" is withdrawn: Appendix A has no such tier and reserves P for text read in full.
12. The contribution basis. Submission 04 line 38, submission 06 lines 47 to 59 and submission 10 lines 116 to 176 carry THB 4.91 and THB 3.51 on the before-excise basis. Whether they move with the valuation is the lead's call; if the valuation moves and they do not, the proposal carries two contribution bases (record 75 conflict 7).
13. Store-equivalents. Nothing in the repo ties 200,000 cubes to a store count or to the 3-unit target. The 1,282 is the store-equivalent count implied by 3 units a store-week and 200,000 cubes a year (back-solved; ASSUMPTION). As context only, it is 8.0 percent of the about 15,945 7-Eleven stores of submission/04 line 37 (P, SOURCED there; read as Thailand-only by inference). The units a store-week in section 4 depend on it, and the pilot's store count is unsourced (record 79).
14. Hand-offs to Singha Corporation. Slide 11 as currently written asks Singha Corporation to set the Route B cost threshold and to approve the panel provider and budget, slide 10 carries "one budget still to be set (decision 9)", and submission/10 (lines 109 and 114, and the Budget paragraph) says the same. Section 6 replaces each with a team setting: paid media starts only when the non-paid click-to-first-purchase read reaches 1.0 percent (desk base of submission/10 line 109; ASSUMPTION), and the pilot spend is a stated limit that is not sized from sources. The lead decides whether the submission files follow.
15. Length of the slide text. The current slide 10 is about 240 words and slide 11 about 300 words on the slide (excluding speaker notes). The second pass's replacements were about three times as long. Section 7 now gives about 370 and 400 words, with the remainder in the speaker note and the appendix text; the lead may cut the exhibit middle or the survey box further if the slides must stay at the current length.

## 9. Limits and what is not verified

- All priors are ASSUMPTION or PROXY values taken from records 05, 06, 70 and 75 or set by this analysis; there is no market data. The conclusions are conditional on these priors.
- The store-equivalent count (1,282) is an ASSUMPTION, the count implied by 3 units a store-week and 200,000 cubes a year (8.0 percent of the about 15,945 7-Eleven stores of submission/04 line 37, as context only). Every figure in units a store-week is conditional on it; figures in cubes a year are not. The sensitivity at 1,000 and 2,000 is in section 4.1 and 4.6.
- The volume spread comes from a can measure (record 70), not a cube measure. The median volume is the record 05 scenario, not sourced.
- The 20 percent tax rate is tier S (primary-origin page, Revenue Department page 6044, read through a page summary, not in full). The tax structure is an assumption; the same-year loss offset of record 75 assumes losses can be used against other group profit, which was not checked against the Revenue Department's rules for group relief. D_cf shows the stand-alone alternative; the probability does not move (0.262 against 0.261).
- Basis mixing. Variants B, C, B_wide and B_rho0 subtract the after-excise can contribution (THB 4.13) from a before-excise cube contribution, which flatters the cannibalised cases (record 75, section 11). The consistent cannibalisation versions are B2 and D (0.267 and 0.262). Variants A and A2 have no cannibalisation term, so the mixing does not arise in them. The headline B is the more favourable reading and still fails the test. Variant A also fixes citric acid at 2.10 g, binder and flavour at zero and cannibalisation at zero.
- The after-excise basis is the proxy of record 75 (the can's net-to-listing ratio applied to the cube). The excise classification and base of the cube are not verified.
- The can contribution before aluminium is an upper bound on lost contribution, so cannibalisation is conservative; no aluminium price is sourced. The binder and flavour prior (uniform 0 to 0.30 THB) is a placeholder for an unpriced line.
- Price and volume correlation (rho minus 0.30) is an assumed sign and size. The pilot analysis treats price and demand as independent; with the correlation kept the break-even demand is higher (section 4.1).
- The pilot model has one national level, a store offset with prior sd 0.30 over the square root of the store count, a weekly drift of 0.02 and a negative binomial with size 5 per store-week; none is sourced. Store heterogeneity beyond the offset is not modelled, so the posterior is probably somewhat optimistic; the store log-sd 0.50 and low-drift runs are the check. Calibration is nominal (0.88 to 0.93 at 2,000 particles; 0.90 to 0.97 at 10,000 with 100 pilots).
- Operating-characteristic probabilities use 300 pilots per cell (Monte Carlo SE up to 0.03 near 0.5). Powers in the sensitivity runs use 200 pilots per cell.
- The value of the pilot uses the prior distribution of truths and the expected NPV at each truth. It ignores pilot running costs, which are not set, and it values demand only. The sign of the value of waiting from week 8 to week 13 depends on the scoring convention (start-of-pilot level, level at the decision week, common week-13 level; section 4.6); the size is at most THB 4,900 (3.8 percent of the value of the demand read) and the five-week delay discount (factor 0.9909) is of the same order, so the model cannot say whether waiting helps.
- The repeat rule uses a flat Beta(1, 1) posterior and cohort counts only. The contribution rule uses the prior probability, because the pilot does not inform contribution.
- The joint-narrowing regions are chosen after the fact among 390 candidates; the probabilities are optimistic and describe what would have to be learned.
- Survey: no respondents. The lead is tested on the model's ratio and on the power of a two-proportion test at the affordable size.
- The week-by-week averages (section 4.2) map demand to NPV through the exact conditional P(NPV above 0 given volume) with the static inputs independent of demand (pilot world), use 2,000 particles for each of 300 pilots per truth, and score the truths on the start-of-pilot level. Separation powers carry a Monte Carlo SE of 0.01 to 0.03; differences of about 0.05 between neighbouring store counts or weeks are within about two standard errors.
- The click-to-first-purchase threshold of 1.0 percent is an ASSUMPTION (the desk base of submission/10 line 109), and pilot spend and panel cost are not sized from sources: both are stated limits.
- Not checked: any Thai source for the cost lines

## 10. Responses to the verifiers' reviews (20 October 2026)

### 10.1 Second review (this pass)

| Issue | Handling |
|---|---|
| Medium: the 20 percent tax rate is tiered "P (extract)"; Appendix A reserves P for text read in full; record 75 and T12 tier it S; conflict 11 misstates record 75 | Accepted. Re-tiered S (primary-origin page read through a page summary) in the status section, section 1, conflicts, limits, the saved note and the results file. The page was read again on 20 October 2026 (same sentence: 20 percent on net profit; page last updated 23 November 2020). Conflict 11 now says record 75 uses S. |
| Medium: the value of waiting is penalised by construction (truth is the start-of-pilot level, the rule tracks the level at the read week); the separation power falling after week 6 comes from the same convention | Accepted for the value of waiting. Three conventions on 40,000 truths (10,000 plus an independent 30,000): start-of-pilot level minus THB 3,541 (A), minus 3,281 (B), minus 1,184 (D); decision-time level plus 4,909, plus 3,283, plus 790; common week-13 level plus 2,020, plus 2,043, plus 603; after the five-week delay discount minus 5,661 to plus 878. The verifier's decision-time figures (plus 2,932, 1,762, 1,027 on 10,000 truths) are within about two standard errors of the 10,000-truth figures here (plus 6,948, 4,896, 859). The claim that waiting loses value is dropped; the sign depends on the convention and the size is under 4 percent of the value of the demand read. Qualified for the separation power: re-scoring each pair against the level at the read week changes the power by at most 0.003 (20 and 40 stores), so the convention does not drive it. For the halving pair the power changes by at most 0.04 from week 4 to week 13 (SE 0.02); the fall for 3.0 against 4.5 at 30 to 40 stores (minus 0.03 and minus 0.06) is the drift of the level itself and shrinks with a lower assumed drift (0.89 at weekly noise 0.005). Section 4.4. |
| Medium: slide 10 title and note overstate the cannibalisation share (index 0.048, EVPPI nil on D; the pilot gives no value for learning it; 7.5 percent is a point value) | Accepted. Title and speaker note rewritten as the verifier proposed; section 4.6 states that the model does not price the cannibalisation read and does not show that the pilot's value lies there. |
| Medium: the break-even quoted as a point and on the wrong basis (335,000 cubes, 2.6, 3.5, 5.0 units are with price and volume independent; correlated 2.40, 4.09, 8.76; depends on 1,282) | Accepted. Section 4.1, slide 10 (speaker note and driver) and slide 11 (speaker note) give the range and its two conditions, with the correlated figures (584,000 cubes on D) and the 1,000 to 2,000 store-equivalent range. |
| Medium: the week-by-week P(NPV above 0) is shown for one pilot per truth, which is noise | Accepted. Section 4.2 and the chart now average 300 simulated 20-store pilots per truth (mean and 10th to 90th percentile), with the single pilot beside them. No pilot reaches 0.95 on any basis at any truth; the information arrives in the first four weeks. The mapping through the exact conditional P(NPV above 0 given volume) agrees with the 200,000-particle mapping to within 0.005. |
| Medium: the hand-offs to Singha Corporation were dropped, not replaced with a team setting | Accepted. Section 6 proposes a click-to-first-purchase threshold of 1.0 percent (ASSUMPTION; desk base of submission/10 line 109) and states pilot spend and panel cost as limits that are not sized from sources. Slides 10 and 11 carry both. |
| Low: store-count criterion is at halving resolution; 15 and 20 cannot be told from 10 at 300 pilots; powers to two decimals | Accepted and partly qualified. The recommendation is stated at halving resolution; powers carry SE; the z values are 1.7 (15 against 10), 4.1 (20 against 10), 2.4 (20 against 15) and 2.3 (30 against 20), so 15 cannot be told from 10 but 20 can. Prose powers are rounded (about 0.8 and 0.9). |
| Low: slide 11 survey box pairs 1.2 points with 22,166 per cell | Accepted. Now "about 1.23 points ... about 22,000 per cell". |
| Low: the N_EFF sensitivity sentence quotes week 13 values as the week 8 read | Accepted. Section 4.6 quotes the week 8 values (194,700, 261,100, 36,200 at 1,000; 183,800, 266,700, 38,700 at 2,000). |
| Low: variant A is not described as fixing citric acid; the basis mixing in B, C, B_wide and B_rho0 is not in the limits | Accepted. Section 2.1, section 7 and the limits name both. The mixing arises where a cannibalisation term subtracts the after-excise can contribution (B, C, B_wide, B_rho0); A and A2 have no such term. The consistent versions are B2 (0.267) and D (0.262). |
| Low: 1,282 is back-solved and the slide does not say so; the 8 percent of 15,945 stores is a useful anchor | Accepted. Slide 11 note, section 1, conflict 13 and the limits say it is the count implied by 3 units and 200,000 cubes (ASSUMPTION) and give the 8.0 percent context from submission/04 line 37. |
| Low: A at 6.0 units with price pinned is 0.9495, written 0.95; slides about three times the current length | Accepted. Written 0.949 (just below 0.95; SE 0.0015). Slide 10 is cut from about 700 to about 370 words and slide 11 from about 600 to about 400; the current slides are 240 and 300; the remainder is in the speaker notes and the appendix text. |

### 10.2 First review (second pass; kept as history)


| Issue | Handling |
|---|---|
| High: the 2.2-unit scale-line proposal is contradicted by the model; 2.19 is a point-value break-even | Accepted and replicated (status section). The proposal and conflict 3 of the first pass are withdrawn. The expected-NPV break-even demand is reported for each basis (A 2.55, B 3.53, D 5.03 units), the 3-unit line is judged against expected NPV and P(NPV above 0) by true demand (sections 4.1 and 4.3), and slide 11 is reverted to the 3-unit line with its basis and the break-evens |
| High: the value of waiting compared a two-read rule with a one-read rule; every payoff has SE about 23,000 | Accepted. Section 4.6 compares like for like with a lower-variance estimator (SE 400 to 2,400 on paired differences) and 10,000 truths. The like-for-like value of waiting was reported as nil (the third pass shows its sign depends on the scoring convention and its size is a few thousand THB); the first pass's figure reproduces as a stringency effect (plus 13,828 on B with SE 3,708). The slide 11 claim and the THB 3,039 weekly cost are removed. Whether the pilot is worth anything is now stated by basis: THB 0.03 to 0.25 million for the demand read |
| Medium: rework/75 exists; 20 percent tax is P (extract); 75 and 77 propose different slide 10 texts; 77 never models excise; variant C differs from 75 | Accepted. The tax was tiered P (extract) with the T12 page and a fresh read (re-tiered S in the third pass, section 10.1); "rework/75 absent" and first-pass conflict 10 are deleted; variants A2, B2 and D model the after-excise basis and the 75 tax structure, and D reproduces record 75's THB 165,023.77 exactly; the two slide 10 texts are listed as a conflict (conflict 1) and merged in section 7. The verifier's after-excise proxy figures are replicated (A2 0.445 against 0.45; B2 0.267 against 0.27) |
| Medium: N_EFF is an ASSUMPTION, not DERIVED | Accepted. Re-tiered ASSUMPTION; the break-even in units is conditional on it; the sensitivity at 1,000 and 2,000 gives the break-evens (verifier: about 2.8 and 1.4 at the old point value) and the value of the pilot |
| Medium: slide 10 and 11 are not drop-in; the pilot is said to test price realisation; title mixes a point value with a probability; threshold wording differs | Accepted. Every item the replacement changes or drops is listed after section 7. The pilot is said to read demand and repeat (and, for the lead, the cannibalisation read); price realisation is not claimed. The slide 10 title now says the probability refers to the NPV under the stated range, not the base case. One wording: "set before the analysis was run" |
| Medium: the 91 percent headline depends on unsourced noise parameters | Accepted. The power is now 88 percent (the demand grid was widened to 6 units, which changes the random stream; the first pass's 91 percent is within about 1.5 standard errors of it at 300 pilots a cell), and the slide states the assumption and the 78 percent figure at high store-to-store variation; the range 0.78 to 0.94 is in the record |
| Medium: IRR and payback have no standard errors; tax has no prior; the repeat prior has no mass below 15 percent; no joint narrowing | Accepted. Standard errors are added to the IRR and payback statistics (section 3). The tax rate is a statutory rate and is fixed (the structure is varied: C, D, D_cf). B_wide and D_wide give the repeat prior mass below 15 percent (0.079). Joint narrowing is computed (section 3.2) |
| Low: read weeks unlabelled; reads correlated; contribution rule only a prior probability; "record 06" ambiguous; README; submission 12 | Accepted. Read weeks labelled ASSUMPTION; phi reported; contribution rule stated as prior probability only; the priors cite submission/06_kpi.md by path; submission 12 added to conflict 5; the README index is left to the lead |

One verifier statement is qualified rather than rejected: the verifier's perfect-information payoffs (minus THB 2,708 for the 3-unit line, minus 183,410 for the 2.19 line) were estimated on 5,000 truths with a standard error of about 24,000; on 200,000 draws the values are plus 5,500 (3,700) and minus 171,500 (4,300), which agree within the verifier's error and carry the same conclusion.

## 11. Files and reproduction

- Script: rework/screen/smc_valuation.py. Run: `python -I smc_valuation.py` from rework/screen (about 470 seconds, peak working set 271 MB; `SMC_QUICK=1` runs a small smoke test that writes to a scratch folder). Reads project_valuation_results.json, value_accrual_model_results.json, can_cost_model_results.json, segment_stat_results.json and conversion_synthesis_results.json.
- Results: rework/screen/smc_valuation_results.json (every number in this record).
- Charts: rework/charts/smc_npv_distribution.png; rework/charts/smc_pilot_posterior_fan.png; rework/charts/smc_operating_characteristics.png; rework/charts/smc_expected_npv_by_demand.png. All four were opened after the final run and checked for legibility (the fan chart now has three rows: one pilot per truth, the 300-pilot average with its 10th to 90th percentile band for variants A, B and D, and the single-pilot and P(demand at or above 3) panels).
- Raw: rework/raw/diligence_2026-10-20/T14/tax_rate_and_inputs_2026-10-20.md.
- The judge-facing files (rework/submission, rework/proposal, rework/deck) were not edited. Section 7 is proposed text only. rework/README.md does not index records 75 and 77; the index is the lead's file.
