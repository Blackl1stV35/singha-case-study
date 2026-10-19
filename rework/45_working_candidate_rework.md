# Working candidate, reworked: sodium-free lime fizz cube (18 October 2026)

> **Dose superseded 19 October 2026:** the design dose is 0.9 volume of CO₂ per 330 ml, confirmed by the user (see [rework/62](62_component1_food_science_check.md) and [rework/52](52_pivot_and_retirement.md) D10). The 1.5 and 1.75 volume figures in this record, including G2, G3 and F3, are superseded.
>
> **Primary candidate, confirmed 18 October 2026** (see [rework/52](52_pivot_and_retirement.md)). The salt is potassium bicarbonate. The earlier text that said carbonate is corrected below.

Status: the dissolvable construction failed its first pass on the brief's own tests. Under the authority recorded on 18 October 2026, I reworked the construction. On the same day the user set three rules: no sugar-free claim (S1); the lab test and the medical test are dropped (S2, S3); and each gate that needed them is resolved by a physics simulation, a desk reading of public texts, or a stated limit. The reworked candidate is below. It is not validated by any bench or clinical test. Section 6 gives the resolution of each gate.

Sources: the dissolvable-cube research workflow (wd2699uxn), the effervescent screen [screen/effervescent_cube_screen.py](screen/effervescent_cube_screen.py) with results in [screen/effervescent_cube_screen_results.json](screen/effervescent_cube_screen_results.json), and the earlier frozen-cube assessment in [rework/42](42_working_candidate_lime_cube.md). Public information only. No outside contact.

## 1. What failed on the first construction

| Test | Result | Source of the result |
|---|---|---|
| Plain dissolvable lime cube as an innovation | Fails the brief's "beyond a plain dissolvable cube" requirement. Dissolvable sugar-free lemon-lime cubes already exist abroad (Waterdrop, 20 markets) | Workflow angle 1; FoodNavigator, 3 October 2024 |
| Sodium bicarbonate as the carbonate | Gives 508 mg Na per 330 mL at 1.5 volumes with full retention, and 1,015 mg at half retention. Thai "low sodium" is under 140 mg per reference serving, so the drink fails it by a factor of about 3.6 | Screen, dose table; Thai Notification 445, Table 1 |
| Fizz claim | Not measurable from the table. The first pass used an open-glass ceiling that the check refuted (the 432 ppm figure is a May 2026 monthly peak, not an annual value). A fizz claim waits for a bench measurement | Chemistry verdict; verifier refutation |
| Regulatory route | Form does not decide it: the FDA guideline sorts by purpose, so the repo default of "supplement because of tablet form" is contradicted. Resolved as a beverage route with no health wording (G4 in [rework/50](50_final_gate_resolution.md)); the FDA classification query is a stated limit | Regulation track, 18 October 2026 |

## 2. The reworked construction

**Sodium-free lime fizz cube.** A compressed lime cube made with potassium bicarbonate and citric acid, sweetened with an intensive sweetener and labelled as such. Dropped into water, it releases CO₂ and flavours the drink. It carries no sodium carbonate. It makes no sugar-free claim (S1), and no sodium-free claim until a Thai opinion settles the "by nature" condition (F1).

- **Why potassium bicarbonate:** the carbonate delivers 0 mg sodium. At 1.5 volumes with full retention it delivers about 864 mg potassium per 330 mL (about 25% of the Thai reference intake). At 2.0 volumes it delivers about 1,151 mg (33%).
- **Cube mass (derived):** about 3.6 g of reactants per 330 mL at 1.5 volumes (KHCO₃ 2.21 g plus citric acid 1.42 g, stoichiometric). About 4.8 g at 2.0 volumes.
- **Sweetener:** an intensive sweetener, with no sodium. The sweetener is disclosed on the label. No sugar-free claim is made (S1), so the Thai sugar-free threshold is not used for this product.
- **Flavour:** natural lime. The public Singha lime product name is "Singha Sparkling Water Lime Flavour" (not "Lime Soda"), so the reworked product must not reuse the Singha name.

## 3. Pillar fit

| Pillar | How the reworked candidate meets it | Evidence strength |
|---|---|---|
| Ingredients and Nutrition | A sodium-free effervescent drink cube (potassium bicarbonate, no sodium carbonate). This is a new combination of raw materials and a labelled sodium-free outcome | Moderate. The Thai sodium-free threshold (under 5 mg per serving) was read from an English translation of Notification 445. The literature register could not confirm it from the Thai text (Attachment 4 was not read), so it stays unverified until the Thai text is checked. Patent check in gate G5; potassium load in gate G3 (simulated, not clinical) |
| Alternative Formats | A dissolvable fizz cube that makes the drink on the spot, with no can | Moderate. Dissolvable cubes exist abroad, so this is a format change, not a new format |
| New Trend-Driven Target | Low-sodium drinking and a hot-season refreshment occasion. No sugar-free claim | Weak to moderate. Thai evidence is strongest for sugar, with sodium as a secondary strand (consumer track). The sugar angle is not claimed, so it cannot carry this pillar alone |

## 4. Angles, after review

| Angle | Verdict | Reason |
|---|---|---|
| 1. Plain dissolvable reference | Hold, as the bench control only | Not beyond a plain dissolvable cube |
| 2. Fizz-on-demand coated cube | Merge into the delayed-release angle | Shares the barrier mechanism with angle 6 |
| 3. Cap with a CO₂ cartridge | Hold | Hardware route. Roam SodaTop is a prior product. Cartridge rules not verified |
| 4. Low-sodium cube with potassium or calcium carbonate | **Adopted as the reworked base** (potassium route) | Calcium route fails solubility (calcium citrate precipitates at about 0.13 volumes). Potassium route passes the sodium arithmetic |
| 5. Electrolyte hydration cube | Candidate for a later variant, not for the first construction | Electrolyte standard (Notifications 195 and 332) and ORS medical-wording risk, unverified |
| 6. Layered timed-fizz cube | Merge into the delayed-release angle | Same mechanism as 2 |
| 7. Botanical or fibre cube | Hold | Novel-food route: about 135 business days of sequential review (derived) |
| 8. Sachet or single-serve tablet | Hold, as the channel format | Convenience is the only evidenced hook |

## 5. Patent and freedom-to-operate gate (closed as a limit where unverified)

- **US 5,254,355 A** (beverage tablet with potassium hydrogen carbonate and an intensive sweetener; claim 5 names citric acid) was filed 29 May 1992 and granted 19 October 1993. **It expired on 29 May 2012.** This is from Google Patents legal status; the USPTO was not read.
- **EP 4,516,115 A2** (Biofar, sodium-free effervescent tablet) is pending with no granted claim. Its published claims need lactobionic acid (claim 7 also needs calcium carbonate), which the candidate does not contain. The claims were read from a machine translation of the German text, and the EPO register returned HTTP 403. The filing date given earlier (2015) is the parent's; the divisional is a 2024 filing. The five specification constraints in [rework/50](50_final_gate_resolution.md) section 3 apply.

## 6. Gates and tests

| Gate | Test | Pass rule (to be fixed before the run) | Status |
|---|---|---|---|
Status as of 18 October 2026, after the final-gate pass. Full record: [rework/50](50_final_gate_resolution.md). Physics results are simulated, not measured, and the lab and medical tests are dropped (S2, S3).

| Gate | Test | Pass rule | Status |
|---|---|---|---|
| G1 | Sodium-free claim | Sodium under 5 mg per 200 mL and per 330 mL (Thai Table 1). Simulated: 1.65 mg per 330 mL at base water 5 mg/L | Resolved by scope: no sodium-free wording (F1). The claim itself is a stated limit, pending a Thai opinion on the "by nature" condition |
| G2 | Fizz | Release of at least 5 ml at 2 min; dissolved CO₂ of at least 0.6 volumes at 10 min | Stated limit. Design dose 1.75 volumes, conditional on an unsourced degassing coefficient |
| G3 | Potassium | Declared as a fact; no potassium claim | Resolved by design at 1.75 volumes (about 1,007 mg per 330 ml). The medical question is a stated limit and needs a reviewer |
| G4 | Regulatory route | Beverage route under Notifications 445 and 450; no health wording | Resolved with design change. FDA classification is a stated limit |
| G5 | Patent | The five constraints in rework/50, section 3 | Resolved with design change. The Thai register is a stated limit |
| G6 | Food additives (added by the critic) | Sweetener and potassium bicarbonate permitted in a beverage | Open. A read-only check is possible without contact |

## 7. Decisions taken under the authority (reviewable)

| # | Decision | Reason |
|---|---|---|
| R1 | Rework the construction to a sodium-free potassium-bicarbonate lime fizz cube | Sodium bicarbonate fails the sodium pillar. Potassium bicarbonate passes the sodium arithmetic. Corrected 18 October: the earlier text said carbonate. Carbonate would double the potassium per serving, so it is rejected |
| R2 | Drop the plain dissolvable reference as an innovation | It fails the "beyond dissolvable" requirement |
| R3 | Merge the fizz-on-demand and timed-fizz angles into one delayed-release angle, held for phase 2 | They share the barrier mechanism and the same open tests |
| R4 | Electrolyte and botanical variants held, not built | Regulatory load (electrolyte standard, novel food) is higher than the first construction can carry |
| R5 | Novelty concern dropped, as instructed | Dissolvable cubes exist abroad. Innovation is carried by the sodium-free route |
| R6 | Registration treated as a regulatory design step, not a blocker | As instructed |
| R7 | Public name not reused | Public product is "Singha Sparkling Water Lime Flavour"; the reworked product gets its own name |
| S1 | No sugar-free claim on the product, in any wording (user, 18 October 2026) | The product is sweetened with an intensive sweetener, and that is disclosed. The sugar-free route is closed |
| S2 | Lab test dropped. Gates that needed bench data (G1 sodium, G2 fizz) are resolved by a physics simulation with stated limits (user, 18 October 2026) | A simulation of stoichiometry and degassing stands in for the bench measurement. It is a model, not a measurement. Any public claim waits for the Thai-text check |
| S3 | Medical test dropped. The potassium gate (G3) is resolved by a potassium-load simulation and a design choice, not by a medical review. The clinical question is a stated limit (user, 18 October 2026) | The simulation checks potassium per serving against reference intake. It cannot establish clinical safety, for example for people with kidney disease or on potassium-sparing drugs. That question stays open and is not claimed as answered |
| S4 | The conversion test runs on a synthesis basis, with no respondents (user, 18 October 2026; [rework/49](49_conversion_test_synthesis.md)). A recruited panel is deferred and waits for an explicit yes that names the provider and the budget | Recruitment sends messages to people on the team's behalf and needs its own approval |
| F1–F5 | Gate decisions from the final-gate pass: no sodium-free wording until a Thai opinion; beverage route; dose 1.75 volumes (conditional); potassium as a fact with the medical question as a limit; patent constraints in the formulation | Recorded in [rework/50](50_final_gate_resolution.md) section 2 |

## 8. Corrections to earlier notes

- **Sugar-free rule (repo note C3):** the note says the rule is 0.5 g per 100 mL and that this is wrong. Thai Table 2 does give 0.5 g per 100 mL for liquids. The per-serving rule in Table 1 is the binding one for a 330 mL can.
- **Open-glass CO₂ ceiling:** the earlier "0.76 volumes at 25 °C" cap is a pure-CO₂ value at 1 atm. Dissolved CO₂ depends on partial pressure, so open-glass fizz must be measured, not read from a table.
- **Lange values:** the Wikipedia table is a 1967 compilation. A check against the NIST evaluation found differences of up to about 2% at 5 °C. Cite NIST for final figures.

## 9. Limits closed

- The sweetener, the water sodium and the citric acid excess are assumed, not measured.
- Thai Notification 445 was read in its English translation; the Thai text is authoritative and was not read.
- The electrolyte standard (Notifications 195 and 332) and the ORS category were not read.
- Current Thai sugar-tax thresholds were not verified.
- The potassium medical-safety question is not sourced; it is a limit that needs a medical reviewer.
- Gate limits and the open items for each gate are in [rework/50](50_final_gate_resolution.md). The entry is not validated.
