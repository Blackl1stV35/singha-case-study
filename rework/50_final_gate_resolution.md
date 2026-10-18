# Final gate resolution: sodium-free lime fizz cube (18 October 2026)

Status: the gate pass is complete on desk and simulation. No outside contact was made. Nothing was submitted, registered or purchased. Several gates close only as **stated limits**, because the answer needs an outside step the team has not approved. The entry is not validated.

Sources: the final-gate workflow (wkwu938zw, nine agents, completed 19:10). Physics: [screen/final_gate_sim.py](screen/final_gate_sim.py) and [screen/final_gate_sim_results.json](screen/final_gate_sim_results.json). Regulation and patent tracks: desk reads recorded in the workflow output (no script). Conversion test: superseded by [49](49_conversion_test_synthesis.md). Candidate: [45](45_working_candidate_rework.md).

Rules applied: no sugar-free claim of any kind (S1); no lab test and no medical test (S2, S3); unverifiable items closed as stated limits; public information only.

## 1. Gate table

| Gate | Resolution | What closes it | What stays open |
|---|---|---|---|
| **G1 sodium-free** | **Resolved by scope (claim not used); stated limit on the claim** | Physics: sodium is 1.65 mg per 330 ml with base water at 5 mg/L or less. It fails at 20 mg/L (6.6 mg) and passes up to about 15 mg/L. Regulation: the claim threshold is under 5 mg per reference serving (Notification 445, Annex 4 Table 1, read from the Thai text). Decision F1 below | The Table 1 condition "prohibited if the food already meets the condition by nature" may bar the claim for a cube that is sodium-free by reformulation. Needs a Thai classification opinion (outside contact) |
| **G2 fizz** | **Stated limit** (design dose conditional) | Simulation with stated pass rules: release of at least 5 ml at 2 minutes, and dissolved CO₂ of at least 0.6 volumes at 10 minutes. Base case passes from **1.75 volumes** (4 °C binds; 1.5 volumes passes at 25 °C only) | The degassing coefficient has no source; the 2×10⁻⁵ m/s base is a calibration value. At the low end (5×10⁻⁶ m/s), no dose up to 2.0 volumes passes. Dissolution time (60 s assumed) and storage CO₂ loss are not modelled. Only a measured or sourced coefficient closes this |
| **G3 potassium** | **Resolved by design for the dose; medical question stated as a limit** | Lowest passing dose, 1.75 volumes: about **1,007 mg potassium per 330 ml** (610 mg per 200 ml). Potassium declared as a fact; no potassium claim (Notification 445, cl. 3, requires a declaration only when a claim is made) | The medical safety question is **not** resolved. For people with reduced potassium excretion, or on potassium-retaining medicines, 1,007 mg per drink is a large dose. This needs a medical reviewer and label wording approval (outside contact). It is the most serious open item. The RDI denominator (3,500 mg) is not reconfirmed; it is about 50% at 2,000 mg |
| **G4 regulatory route** | **Resolved with design change** | Beverage route (FDA category 14, under Notifications 445 and 450). All health-purpose wording removed, including hydration, electrolyte and potassium-benefit language. The repo default (supplement because tablet form is listed) is contradicted: the FDA guideline sorts by purpose, not form | Whether a compressed cube is a "non-conventional form" under Notification 293 cl. 2, and so category 13 or 14, needs a regulator query (outside contact) |
| **G5 patent** | **Resolved with design change; Thai territory is a stated limit** | US 5,254,355 A **expired on 2012-05-29** (this corrects the earlier note in [45](45_working_candidate_rework.md)). EP 4,516,115 A2 is pending, and its published claims need lactobionic acid (claim 7 also needs calcium carbonate). Five specification constraints are recorded in section 3 below | The EPO and Espacenet registers returned HTTP 403. The Thai DIP register returned no content. The live US and Spanish claims found are avoided by constraint, not cleared. The sweep was not a classification search |
| **G6 food additives** (new; added by the critic) | **Open** | Read-only step, possible without contact: the Thai food-additive notification for the intensive sweetener in a beverage, and for potassium bicarbonate as the acid-carbonate source | Not read. This blocks sale whatever G1 to G5 say. Stevia, sucralose and acesulfame K show no warning in the annexes read, but their beverage permission is unverified. Acesulfame K also adds potassium |
| **Conversion test** | **Stated limit** (synthesis basis) | [49](49_conversion_test_synthesis.md): direction supported under stated inputs; a 5-point lead not supported at any baseline | No respondents. The recruited design is deferred and needs an approval naming a provider and budget (S4) |

## 2. Decisions taken under the standing authority (reviewable)

| # | Decision | Reason | Reverse if |
|---|---|---|---|
| F1 | **No sodium-free wording on the product** until a Thai classification opinion answers the "by nature" condition. The formulation (potassium bicarbonate, no sodium carbonate) is stated on the ingredient list as a fact | The claim may be barred. An unclaimed fact cannot fail the claim rule | A Thai opinion permits the claim |
| F2 | Beverage route; no health-purpose wording anywhere | Follows G4 | An FDA classification puts the product in category 13 |
| F3 | Dose: **1.75 volumes**, conditional on the 5 ml release rule and the 2×10⁻⁵ m/s calibration | The lowest dose that passes the base case | A sourced coefficient or a measured fizz test moves the dose |
| F4 | Potassium declared as a fact; no potassium claim; medical question kept as a stated limit | Dropped medical test (S3); the sim cannot answer safety | A medical reviewer signs the label wording |
| F5 | Patent constraints written into the formulation: no lactobionic acid, calcium carbonate or vacuum pre-treatment; no inorganic potassium acid or potassium phosphate; no sodium bicarbonate or sodium-bearing formula; carbohydrate at or below 50 mmol/L per drink | Avoids the live claims found | A Thai register read clears a constraint |

**The cost of F1.** The Ingredients and Nutrition pillar in [45](45_working_candidate_rework.md) rested on a sodium-free claim. Without the claim, the pillar rests on a formulation fact. That is a weaker case for judges, and I have not hidden it. It is the main reason to decide the "by nature" question before the entry closes.

## 3. Specification constraints (from the patent track)

1. No lactobionic acid, no calcium carbonate, no partial-vacuum pre-treatment of the carbonate.
2. No inorganic potassium-containing acid (for example potassium phosphate or potassium bisulfate).
3. No monopotassium or dipotassium phosphate fortifier.
4. No sodium bicarbonate, PEG or sodium-bearing formula.
5. Total carbohydrate at or below 50 mmol/L per diluted drink. Whether sugar alcohols count is unread, so the stricter reading is used.

Binder note: the expired US 5,254,355 used mannitol as sole binder. Potassium citrate forms in situ from the bicarbonate and citric acid. Whether potassium citrate alone meets a fortifier claim is not checked.

## 4. Issues the critic raised that change the record

- **Sugar-free strings in internal screen files** (effervescent_cube_screen.py, lime_cube_screen.py, segment_potency_mc.py, and their results files). These are internal, but S1 says "of any kind". They are corrected in the screen files listed in [45](45_working_candidate_rework.md).
- **Population counts.** The DDC and DOPA counts for men 25 to 44 agree within about 2%. For men 45 to 59 they differ by about 7% (7.13 million against 6.65 million). The earlier statement that they "match" was wrong for that cell. It feeds the pended volume item.
- **Segment transfer.** The segment logic (rework/46) measures sugar-sweetened drinking. The candidate has no sugar. Whether the age ranking carries over to an intensively sweetened product is untested.
- **Two potassium doses in the repo.** The earlier screen gives 864 mg (1.5 volumes) as the design figure. The gate design is 1.75 volumes and about 1,007 mg. The gate design governs.
- **Potassium declaration conflict.** The physics track called the declaration mandatory; the regulation track, reading the primary text, says it is required only when a claim is made. The regulation reading governs. The declaration is kept as a voluntary fact (F4).
- **Sweetener descriptor.** Notification 450 requires a functional name for a sugar-replacing sweetener. That needs a ruling that it is a disclosure, not a sugar claim, before any label copy is drafted.

## 5. Entry position

- **Validated:** no. G2 and G6 are open, and G1's claim is barred until a Thai opinion.
- **Closable before 22 October 23:59 with no outside contact:** G6 (read-only food-additive check), the Thai patent register if a reader is found, and the internal sugar-free cleanup.
- **Needs an outside step, which the team has not approved:** the Thai classification opinion (G1), a regulator query (G4), a medical reviewer (G3), a supplier water specification (G1), and a Thai patent attorney (G5). None of these can close in four days without outside contact.

The entry decision is the user's. A concept-only entry, with this record presented as stated limits, is possible. An entry that claims the sodium-free and fizz properties as validated is not supported by this record.
