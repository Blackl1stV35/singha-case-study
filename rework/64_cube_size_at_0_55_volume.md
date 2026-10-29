# Cube size and mass at the recommended dose (19 October 2026)

Status: DERIVED on ASSUMPTION inputs. Desk calculation only; nothing is weighed or sealed. Script: [screen/cube_size_0_55.py](screen/cube_size_0_55.py), results in [screen/cube_size_0_55_results.json](screen/cube_size_0_55_results.json).

This record sets the cube size for the recommended dose (0.55 volume, target pH 3.5, [52](52_pivot_and_retirement.md) D14 and D15). It supersedes the 15 mm and 5.3 g cube figures in [48](48_brand_style_matching.md) section 6.1. The mock-up source files still carry 15 mm; see section 6.

## 1. Result

| Item | Value | Status |
|---|---|---|
| Cube side | **13 mm** (recommended) | DERIVED; the choice is the team's |
| Cube volume | 2.20 cm3 (was 3.375 cm3 at 15 mm) | DERIVED |
| Mass, basis A (reactants only) | **2.94 g** | DERIVED |
| Mass, basis B (A plus carried binder and flavour) | 3.16 g | DERIVED; the 0.22 g is ASSUMPTION |
| Density at 13 mm | 1.34 g/cm3 (A); 1.44 g/cm3 (B) | DERIVED; both inside the assumed band 1.25 to 1.60 |
| Pack depth | 18 mm (13 mm plus 2.5 mm per face), was 20 mm | DERIVED from the rule in 48 section 6.1 |
| Front face | 70 x 90 mm, unchanged | ASSUMPTION (design choice) |
| Packed unit, with 1.5 g pouch | 4.44 g | ASSUMPTION for the pouch mass |

Basis A is the basis already in the proposal and the models: the proposal's pouch mass of 4.44 g is the reactants (2.94 g) plus a 1.5 g pouch ([proposal/06_kpi.md](proposal/06_kpi.md); [screen/handover_figures_results.json](screen/handover_figures_results.json)). Basis A is therefore the recommended basis for the mock-up. Basis B applies only if R&D finds that the cube needs a binder.

## 2. Recipe per 330 mL at 0.55 volume, pH 3.5

| Component | Amount | Status |
|---|---|---|
| CO2 | 8.1 mmol | DERIVED (0.55 x 0.330 L / 22.414 L per mol) |
| Potassium bicarbonate | 0.811 g | DERIVED (one mole per mole of CO2; 100.12 g per mol) |
| Citric acid, stoichiometric | 0.519 g | DERIVED (one third mole per mole of CO2) |
| Citric acid, free-acid excess | 1.581 g | DERIVED from the total below |
| Citric acid, total for pH 3.5 | 2.10 g | DERIVED from pKa values (S, UNVERIFIED in the handover) |
| Sucralose | 33 mg | DERIVED (S; 6 g sugar equivalent divided by 600) |
| Reactants | 2.944 g | DERIVED |
| Potassium | 316.6 mg per serve | DERIVED (9.1% of the Thai reference; [63](63_desk_model_stress_and_pack_economics.md)) |

Check: the same script at 1.75 volumes gives 4.23 g of reactants and 1.564 g/cm3 for 5.28 g at 15 mm. Both match [48](48_brand_style_matching.md) section 6.1, so the stoichiometry is consistent with the earlier design.

## 3. Why 13 mm

The density band (1.25 to 1.60 g/cm3) is an ASSUMPTION ([48](48_brand_style_matching.md) section 6.4). Density at four candidate sides:

| Side | Density, basis A | Density, basis B | Inside the band on both? |
|---|---|---|---|
| 12.5 mm | 1.51 | 1.62 (above) | No |
| **13.0 mm** | **1.34** | **1.44** | **Yes** |
| 13.5 mm | 1.20 (below) | 1.29 | No |
| 15.0 mm (old) | 0.87 (below) | 0.94 (below) | No |

13 mm is the only candidate inside the band on both mass bases. It also means the size does not depend on the binder question in section 5.

## 4. What changed from the 1.75-volume design

- Reactants: 4.23 g became 2.94 g, because the dose fell from 1.75 to 0.55 volume.
- Excess citric acid: the 1.75-volume design used 0.80 g. That was an assumption, not a pH calculation. At pH 3.5 the model gives 1.58 g.
- The 1.05 g aggregate (binder and filler 0.17 g, flavour 0.05 g, sweetener 0.03 g, excess acid 0.80 g) is replaced. Sweetener is now 33 mg from its own derivation. Excess acid comes from the pH calculation. Only binder, filler and flavour (0.22 g) are carried, for basis B, and they remain ASSUMPTION.
- Potassium: 1,007 mg per 330 mL became 317 mg per serve.

## 5. Open items and limits

1. **Binder need (R&D).** Whether 2.94 g of potassium bicarbonate and citric acid compresses into a cube without binder, or needs about 0.2 g of binder, is not sourced and has not been tested. The 13 mm size holds for both bases.
2. **Density band.** The 1.25 to 1.60 band is an ASSUMPTION. The team's decision, as [48](48_brand_style_matching.md) section 6.4 says.
3. **Mass range.** The old 4.9 to 5.8 g range is not re-derived. This record gives point values only.
4. **Pouch mass.** The 1.5 g pouch is an ASSUMPTION. No converter quote exists.
5. **Net weight on the label.** This is the cube's mass. Under basis A it is about 2.9 g; under basis B, about 3.2 g. Nothing is weighed, so the figure should be marked as derived until a weighed cube exists.
6. **Pack depth.** The 20 mm depth in the tokens file stays until the mock-up is updated.

## 6. Stale figures (not changed by this record)

The mock-up source and render still show the 1.75-volume cube. The grep on 19 October 2026 found these files:

- [48](48_brand_style_matching.md) sections 6.1, 6.4 and 10.2: 15 mm, 4.23 g, 5.28 g, 1.56 g/cm3.
- `mockup/style_tokens.json`: `cube_side`, the mass basis text, the label net weight "5.3 g", and the potassium placeholder at 1,007 mg (5 matches).
- `mockup/MATERIALS_cube.md`: 15 mm and the 4.23 g and 5.28 g figures (2 matches).
- `mockup/build_cube_scene.py` (2 matches) and `mockup/make_label.py` (1 match): the cube side and the label text.
- `mockup/cube_3d.html` and `judge/cube_3d.html` (1 match each). The judge copy's "at 1.75 volumes" wording came from the scrub in [52](52_pivot_and_retirement.md) section 4.
- Records [45](45_working_candidate_rework.md), [50](50_final_gate_resolution.md), [51](51_final_conclusion_and_recommendation.md), [52](52_pivot_and_retirement.md), [53](53_unit_cost_and_value_chain.md), [57](57_package_revision_tarlo.md) and [62](62_component1_food_science_check.md): 1.75-volume or 5.28 g figures. Not opened one by one in this pass.
- `screen/`: `final_gate_sim_results.json`, `financial_projection.py` and its results, `lime_cube_screen_results.json`, `unit_cost_value_chain.py`. Not opened in this pass.
- `strategy/09_trend_tracks_and_20pct_test.md` and `strategy/data/fin_tornado.csv` matched a pattern. They sit outside `rework/` and were not opened.

Not stale: the proposal folder and `judge/handover_rd_figures.md` contain none of the 15 mm, 5.3 g, 4.23 g, 5.28 g, 1,007 mg or 1.75-volume patterns. They carry 0.55 volume and the 4.44 g pouch mass.

## 7. Next step (not done)

Update the mock-up at 14 mm and basis B (section 8): the tokens file, `MATERIALS_cube.md`, the build script, the label text and the ingredient list. Then re-render (check free RAM first, per [CLAUDE.md](../CLAUDE.md) section 6), re-sync `judge/`, and run `verify_cube_mockup.py`. The judge sync and the ingredient list are product-facing, so they need the team's go-ahead first.

## 8. Basis B confirmed, and correction (19 October 2026)

The user confirmed basis B: the cube carries binder and flavour as well as the reactants and sucralose. This section supersedes sections 1, 3, 4 and 5, item 5, where they say otherwise.

**Correction to section 4.** The 0.17 g is the citric acid excess at 10% of 1.65 g from the 1.75-volume design ([48](48_brand_style_matching.md) section 6.1, row "Citric acid excess"). It is not binder. The binder and filler row is 0.80 g (range 0.5 to 1.2), and the lime flavour powder is 0.05 g (range 0.02 to 0.10). All three are ASSUMPTION, and [57](57_package_revision_tarlo.md) section 3 says the 1.05 g total is an aggregate, not a split. Section 4's "binder 0.17 g" and the 0.22 g used in basis B were wrong.

**Basis B, recomputed** ([screen/cube_size_0_55.py](screen/cube_size_0_55.py) for the reactants, the arithmetic here for the additions):

| Item | Value | Status |
|---|---|---|
| Reactants | 2.944 g | DERIVED |
| Binder and filler | 0.80 g (range 0.5 to 1.2) | ASSUMPTION |
| Lime flavour powder | 0.05 g (range 0.02 to 0.10) | ASSUMPTION |
| Cube mass, central | **3.79 g** (range 3.46 to 4.24 g) | DERIVED on ASSUMPTION inputs |
| Packed unit with 1.5 g pouch | **5.29 g** (was 4.44 g) | ASSUMPTION for the pouch |

**Cube side under basis B: 14 mm (recommended).** At 13 mm the central mass gives 1.73 g/cm3, above the assumed band of 1.60. At 14 mm it gives 1.38 g/cm3, inside the band. The band-consistent range for the central mass is 13.3 to 14.5 mm. Across the whole binder range no single side fits, because the low case needs about 13 mm and the high case about 15 mm. Pack depth at 14 mm is 19 mm, which still fits the 20 mm pouch depth.

**Net weight.** Withdrawn: the 2.9 g and 3.2 g figures in section 5, item 5, and the earlier recommendation of 2.9 g. [52](52_pivot_and_retirement.md) section 6, item 9, keeps the net weight as "[to be set]" until a cube is weighed. The 3.8 g central value is derived, not weighed.

**Package and container effects**
- Pouch: the packed unit rises from 4.44 g to 5.29 g. The pouch price is per piece in the model, so the pouch cost does not change.
- Carton: the count and mass do not change. Carton count is set by volume, and the empty carton is 0.10 kg whatever the cube weighs.
- 20 ft container: the count stays at 128,580 cubes, because volume limits the load, not weight. The mass rises from about 1.64 t to about 1.75 t (128,580 x 5.29 g, plus 10,715 cartons x 0.10 kg), against a 28.2 t payload.
- Cost: binder and flavour are not priced ([53](53_unit_cost_and_value_chain.md) row "Flavour and binder"). The reactant cost in the model excludes them, so the per-cube cost is understated by an unpriced amount.

**Not yet propagated to basis B.** These still show reactants only (basis A) and need a go-ahead, because the judge-facing ones state the composition:
- [judge/handover_rd_figures.md](judge/handover_rd_figures.md) line 7 (composition: potassium bicarbonate, citric acid and sucralose only).
- [proposal/06_kpi.md](proposal/06_kpi.md) (4.44 g pouch mass; reactants 2.94 g).
- `screen/handover_figures.py` and `screen/pack_economics.py` (reactants only in the pouch mass). `pack_economics.py` also still describes a 0.9-volume cube, and [63](63_desk_model_stress_and_pack_economics.md) section 7 is at 0.9 volume.
- The mock-up source, render and `judge/` (section 7 above).

## 9. Carton outside size, confirmed as an assumption (19 October 2026)

- **Portable pack: a 6-cube carton, 190 x 150 x 50 mm outside (width, depth, height). ASSUMPTION.** The user chose the portable pack for sport and recreation use on 19 October 2026. The size is the 6-pack entry in `screen/pack_economics.py` (lines 70 to 75). The 12-cube carton, 190 x 150 x 100 mm, stays as the larger option. No carton maker's quote, board specification or sourced standard supports either size.
- **Fit check (DERIVED, arithmetic only).** A flat pouch is 90 x 70 x 20 mm. Two across and two deep fill 180 x 140 mm of the 190 x 150 mm footprint, with 10 mm spare each way. Two layers make a 40 mm stack, inside the 50 mm height. Six pouches fit with room to spare. The model's packing factor (1.5 times the pouch volume) is an ASSUMPTION, and board thickness is not counted.
- **Cost and container, the 6-cube pack (DERIVED from `screen/handover_figures_results.json`, binder and flavour excluded).** Cost per cube THB 4.09, of which the carton share is THB 0.67 (the THB 4.00 carton price is an ASSUMPTION scaled from the 12-cube price). In a 20 ft container, 128,586 cubes in 21,431 cartons, a modelled mass of 2.82 t against a 28.2 t payload. The 12-cube pack gives THB 3.84 per cube and 1.75 t. The cube count per container barely changes, because the limit is volume. The cartons double.
- **Valuation not rebased.** `screen/project_valuation.py` still runs on the 0.9-volume pack model with a 12-cube base. Its outputs are not changed by this decision. Rebasing them is an open item.
- **Other reference, not used.** [Record 63](63_desk_model_stress_and_pack_economics.md) cites a 20 x 14 x 12 cm retail box at a retail asking price. Its contents are not stated there, so it is not used for the size.
- **Where the size is used.** The Blender render and the 3D page both draw the carton at 190 x 150 x 50 mm (width, depth, height), the 6-cube pack. The first test render had the width, depth and height in a different order; that was corrected to the model's order before the 12-cube version. The carton was resized to the 6-cube pack on 19 October 2026.
- **Status and closure.** Confirmed as the working assumption. It stays a stated limit until a carton maker confirms the outside size and the board thickness before any print. No contact has been made with a maker.
- **Carton material: resolved on 19 October 2026 as printed folding paperboard.** The carton is outer, secondary packaging. The food contact is the PET pouch ([rework/32](32_pet_compliance.md); D-P1). The render and the 3D page show an ink board with a lime band. No material price exists, so the THB 4.00 carton price stays an ASSUMPTION.
- **Held Thai rule.** [Record 41](41_upstream_packaging_survey_thai.md) (D-P4) holds paper and bagasse packaging. It says the costing assumes a TIS 2948 licence applies. I have not verified that the THB 4.00 carton price includes that licence cost. The Gazette has not been read. Reading it needs a download, which needs your OK. This stays a stated limit.
- **Not yet chosen:** board grade, coating and print process. These need a carton maker's quote. None has been requested, since that needs your approval.

## 11. Valuation rebased to the 0.55-volume design and the 6-cube pack (19 October 2026)

- [screen/project_valuation.py](screen/project_valuation.py) now reads the 0.55-volume design and the pack rows from [screen/handover_figures_results.json](screen/handover_figures_results.json). Its base pack is the 6-cube carton. The prices are unchanged. The earlier 0.9-volume, 12-cube run is in git history.
- Base unit economics: cost per cube THB 4.09 (6-cube), ex-factory THB 9.00 (ASSUMPTION), contribution THB 4.91 per cube, margin 54.6%. Binder and flavour are excluded, because they are not priced. The earlier 0.9-volume base was THB 3.90 cost and THB 5.10 contribution.
- Base case, 200,000 cubes per year, 10% rate, fixed cost THB 500,000 per year: NPV THB 0.88 million, payback 2.1 years. At THB 250,000 the NPV is THB 2.08 million. At THB 1,000,000 it is negative.
- Maximum fixed cost at base volume and 10%: THB 683,852 per year (was THB 710,315).
- Low volume (50,000 cubes) is negative at every fixed cost. High volume (1,000,000 cubes) is positive. These scenarios are DERIVED on ASSUMPTION volumes, not forecasts.
- The proposal drafts that quoted the 12-cube valuation are updated by a separate pass. Until then, their statements that say "not rebased" are out of date.

## 10. Judge 3D page resolved (19 October 2026)

- The water block and the drop-into-water sequence were removed from the judge 3D page. This follows the 18 October 2026 critic pass (rework/48 section 8.4), which removed the water column from the render. Sections 9.1 to 9.3 of rework/48 describe the earlier page and are superseded on this point.
- The carton is added behind the pouch, and the cube rests on the floor beside the pouch, as in the render. The page keeps orbit, auto-rotate and reset view. The drop button is gone.
- The page's lead, description, specs and accessible name now describe a pouch, a cube and a carton. The page shows no water.
- Reopening water needs the owner's written decision, as rework/48 section 10.3 already requires for glass and bubbles.
