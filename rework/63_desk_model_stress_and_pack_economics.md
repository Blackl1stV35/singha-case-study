# Desk model, Thai stress test and pack economics for the lime cube (19 October 2026)

Status: a desk model only. No bench test, no quote, no outside contact. Scripts: [screen/formulation_desk_model.py](screen/formulation_desk_model.py) (results in [screen/formulation_desk_model_results.json](screen/formulation_desk_model_results.json)) and [screen/pack_economics.py](screen/pack_economics.py) (results in [screen/pack_economics_results.json](screen/pack_economics_results.json)). Both use the standard library only and run with `python -I`. Every figure is a model output or a sourced input with its tier. Page text behind SOURCED figures is not yet saved to `rework/raw/`, so under the repo rule those figures stay UNVERIFIED until saved.

Design under test: 0.9 volume of CO₂ per 330 mL, one cube per pouch, potassium bicarbonate with citric acid (stoichiometric plus a free-acid excess set by target pH), an intensive sweetener (sucralose recommended, [rework/52](52_pivot_and_retirement.md) D13).

## 1. Corrections to records 62 and 45 (from the verification run)

The verification run (an independent re-read of the Gazette, a chemistry recheck, a food-science critic, and refutations of the critic's high- and medium-severity objections) upheld the following. They correct [rework/62](62_component1_food_science_check.md) sections 2.2 and 2.3.

1. **The 0.76-volume figure is not an open-glass value.** It is the solubility of pure CO₂ at 1 atm over water (Lange-attributed table, tier S). In an open glass the equilibrium is set by room air: about 0.0003 volumes at 25 °C and 0.0006 at 4 °C (at 420 ppm, ASSUMPTION).
2. **0.9 volume is above the ceiling, not at it.** It is 18.5% above the 25 °C value (0.759) and 2.5% above the 20 °C value (0.878). It holds fully in a sealed 1-atm pure-CO₂ pack only at or below about 19 °C. At 25 °C it would need about 1.19 atm of CO₂.
3. **The fizz is a kinetic question.** Equilibrium arithmetic gives the endpoint, not the rate. Section 2 gives a surface-only upper bound on persistence. Nucleation and stirring are not included, so the real time is shorter. The "faint" wording has no sensory source (section 10).
4. **The free-acid excess is 3 to 6 times the stoichiometric citric acid**, not "roughly double". At a target pH of 3.0, total citric acid is 5.97 g per 330 mL (free 5.12 g). At pH 3.5 it is 3.42 g (free 2.57 g). The stoichiometric product, with no free acid, is near pH 6.0 in the model, not "above pH 4".
5. **Potassium reference.** The 15% figure in [rework/62](62_component1_food_science_check.md) rested on a circular 3,456 mg reference. The Thai RDI for potassium is 3,500 mg per day: MOPH Notification 182 (B.E. 2541) is read from a third-party copy (tier S; the primary text was not opened), and the current No. 445 value of 3,500 mg comes from a consultancy page (tier S). The Royal Gazette text of No. 445 was not read. At 518 mg per 330 mL the figure is **14.8%** of the Thai RDI.
6. **The user's 19 October 2026 confirmation of 0.9 volume** was given on the reasoning in items 1 and 2. Both are withdrawn by this record. The dose is under review; see section 9.

## 2. Model results at 25 °C serve (no ice, 330 mL)

| Quantity | Value | Basis |
|---|---|---|
| CO₂ generated, 0.9 volume | 13.25 mmol | DERIVED from V × 0.330 L / 22.414 L/mol |
| Potassium bicarbonate | 1.33 g | DERIVED (stoichiometric) |
| Potassium per serve | 518 mg | DERIVED (K 39.10) |
| Potassium, % of Thai RDI 3,500 mg | 14.8% | S (third-party copy of Notification 182; No. 445 value S) |
| Citric acid, stoichiometric | 0.85 g | DERIVED |
| Dissolved at serve (25 °C) | 0.759 volumes; 15.7% of the dose leaves at once | Model; Lange anchor (S) |
| Mass-transfer time constant | 106 min (surface only, renewal 10 s) | Model; upper bound |
| Time above the sensory threshold | about 130 min (surface only) | Model; threshold is mineral water (P), a proxy |

The sensory threshold is the BET value of 0.44 g/L, about 0.22 volumes, for sparkling sensation in mineral water (Puleo et al. 2021; tier S, abstract only, full text not read). No soft-drink threshold was found.

## 3. Serve temperature and Thai conditions

Solubility of CO₂ at 1 atm, volumes at STP per volume of water. The Lange-attributed table gives 30 and 35 °C (tier S). NIST Ostwald coefficients converted to STP give 0.676 and 0.600 (tier P), a ±3% cross-check.

| Serve water | 5 °C | 10 °C | 15 °C | 20 °C | 25 °C | 30 °C | 35 °C |
|---|---|---|---|---|---|---|---|
| Solubility (volumes) | 1.424 | 1.194 | 1.021 | 0.878 | 0.759 | 0.655 | 0.592 |
| Dissolved from a 0.9-volume dose | 0.90 | 0.90 | 0.90 | 0.878 | 0.759 | 0.655 | 0.592 |

Thai climate (TMD 30-year normals, 1991 to 2020, Bangkok station 48455; tier P): the April mean daily maximum is 35.7 °C, the May mean is 35.1 °C, and the annual mean is 33.7 °C. The annual mean relative humidity is 73%, ranging from 66% (December) to 79% (September). Thai regulation sets no numeric storage temperature for ambient packaged food (MoPH Notifications 367, 450, 469 and 473 read; "normal temperature" only). The 35 °C storage and hot-serve case is therefore anchored to the April mean maximum, not to a Thai storage rule.

Serve scenarios (330 mL prepared, unless ice is added):

| Scenario | Serve temperature (°C) | Prepared volume (mL) | Dissolved at serve (volumes) | Fraction leaving at once | Time above threshold, upper bound (min) |
|---|---|---|---|---|---|
| Chilled water, no ice | 5.0 | 330 | 0.900 | 0% | 148 |
| Room water, no ice | 25.0 | 330 | 0.759 | 16% | 130 |
| Ambient water, no ice | 30.0 | 330 | 0.655 | 27% | 115 |
| Hot day, no ice | 35.0 | 330 | 0.592 | 34% | 104 |
| Ambient 30 °C with 30 g ice | 20.9 | 360 | 0.825 | 0% | 152 |
| Ambient 30 °C with 60 g ice | 13.1 | 390 | 0.762 | 0% | 154 |

Ice melts into the drink, so the prepared volume rises and the volumes fall. Ice keeps the 0.9 dose dissolved in a Thai serve by cooling the drink into the range where the solubility holds. The melt heat balance uses the latent heat of fusion (333.55 J/g) and the specific heat of water (4.1787 J/(g·K)), both tier S (Wikipedia data pages). The model assumes the cube dissolves after the ice has melted. The effervescent reaction is endothermic, so the real temperature drop is larger; that heat is not modelled (limit).

## 4. Stress test: Monte Carlo over serve temperature, mass transfer, water alkalinity and target pH

10,000 draws (seed 20261019): serve temperature uniform 5 to 35 °C; surface renewal time log-uniform 1 to 30 s; water alkalinity uniform 0 to 150 mg/L as CaCO₃; target pH uniform 2.8 to 3.5.

| Output | 5th percentile | Median | 95th percentile |
|---|---|---|---|
| Dissolved CO₂ at serve (volumes) | 0.610 | 0.882 | 0.900 |
| Fraction leaving at once | 0% | 2% | 32% |
| Mass-transfer time constant (min) | 36 | 79 | 169 |
| Time above threshold (min, upper bound) | 46 | 101 | 222 |
| Total citric acid (g per 330 mL) | 3.66 | 5.06 | 7.96 |
| Free citric acid (g per 330 mL) | 2.81 | 4.21 | 7.11 |

Reading of the stress test:
- The chemistry is robust to alkalinity. Alkalinity raises the citric need by only 0.43 g over the full 0 to 150 mg/L range. The Thai evidence is narrower (section 8), so the effect is smaller still.
- Fizz duration is most sensitive to the mass-transfer assumption. A renewal time of 1 s gives a time constant of 34 min; 30 s gives 184 min. The model is an upper bound because it has no bubble nucleation.
- A 0.9-volume dose exceeds the solubility at every serve temperature above about 19 °C, so the dose is the decisive design variable for Thai conditions.

## 5. Acid balance and the taste trade-off

Total citric acid per 330 mL needed for a target pH, from the charge balance (citric pKa 3.13, 4.76, 6.40; carbonic pKa 6.35, 10.33; CRC, tier P, with an edition caveat):

| Target pH | Total citric (g per 330 mL) | Per litre (g/L) | Free excess (g per 330 mL) |
|---|---|---|---|
| 2.8 | 8.15 | 24.7 | 7.30 |
| 3.0 | 5.97 | 18.1 | 5.12 |
| 3.2 | 4.60 | 13.9 | 3.75 |
| 3.5 | 3.42 | 10.4 | 2.57 |
| 4.0 | 2.47 | 7.5 | 1.62 |
| 4.5 | 1.90 | 5.8 | 1.05 |

Sourced comparison (tier P): commercial lemon-lime carbonated drinks sit at about pH 2.5 to 3.3 (Sprite 2.71 ± 0.04; a UAE market survey gives 2.32 to 4.99 for carbonated drinks, mean 3.01). A lemon-lime patent gives a typical pH of 3.2 to 3.8 and citric acid of 0.18 to 0.24%. That converts to about 1.8 to 2.4 g/L (DERIVED; the patent's percentage basis is not confirmed). A lime-flavoured sparkling water in the UAE market reads pH 4.48.

Consequence: the cube needs about 3 to 12 times the acid of a typical lemon-lime soda at any pH from 3.0 to 4.5. The potassium citrate buffer sets this, not the free acid alone. Target pH 3.5 is a reasonable taste anchor (10.4 g/L total, about 5 times typical). A sensory test decides it. That is a limit for R&D, not a desk-resolvable question.

Water alkalinity sensitivity (at pH 3.0): 0 mg/L gives 5.97 g; 50 mg/L gives 6.11 g; 100 mg/L gives 6.25 g; 150 mg/L gives 6.40 g.

## 6. Storage gas in a sealed pouch (35 °C, 20 mL headspace, ASSUMPTION)

If part of the bicarbonate reacts with moisture before opening, CO₂ builds in the pouch. Ideal-gas estimate at 35 °C:

| Fraction reacted in pack | Gas (mL) | Headspace pressure rise |
|---|---|---|
| 0.1% | 0.34 | +1.7% |
| 0.5% | 1.68 | +8.4% |
| 1% | 3.35 | +17% |
| 5% | 16.8 | +84% |

A 1% reaction in storage gives a visible pressure rise in a 20 mL headspace. The pack specification must keep reaction below about 0.5%. No water-vapour transmission rate is sourced (limit; [rework/mockup/MATERIALS_pouch_stack.md](mockup/MATERIALS_pouch_stack.md)).

Humidity: no deliquescence humidity was found for potassium bicarbonate. For citric acid, a 77% RH value is given for the monohydrate (tier S, UNVERIFIED; the anhydrous value was not found). Bangkok's mean relative humidity is 78 to 79% in September and October. If a 77% threshold applies to the anhydrous acid used, the pack would sit above it in the rainy season. This is a limit until the anhydrous value is sourced.

## 7. Pack economics: units per pack and per container

### 7.1 Inputs (THB; status in [screen/pack_economics.py](screen/pack_economics.py))

| Input | Base | Range | Status |
|---|---|---|---|
| Potassium bicarbonate | 38.1 THB/kg | 33.6 to 358 | PROXY: UN Comtrade HS 2836.40 (potassium carbonates, 2024 unit value USD 1.136/kg); the line may mix carbonate and bicarbonate. High is a US small-pack listing (DERIVED) |
| Citric acid | 31.4 THB/kg | 30.0 to 128.5 | PROXY: UN Comtrade HS 2918.14 (2025 unit value USD 0.936/kg; weight estimated by UN). High is a US small-pack listing (DERIVED) |
| Sucralose | 655 THB/kg | 400 to 799 | LISTED (Lazada TH asking price); high is UN Comtrade HS 2932.14 (USD 23.8/kg, a proxy that may include other products) |
| Pouch, 90 × 70 mm laminate | 1.30 THB | 0.67 to 2.70 | DERIVED from a non-Thai listing (USD 0.03 to 0.05 per piece, MOQ 1,000). Low and high are USD 0.02 and 0.08 from unverified supplier snippets. No Thai converter price found |
| Print | 1.50 THB | 0.80 to 2.50 | ASSUMPTION (placeholder) |
| Compaction, sealing and packing labour | 0.50 THB | 0.25 to 1.00 | ASSUMPTION (no sourced figure) |
| Carton, 6 / 12 / 24 cubes | 4 / 5 / 9 THB | 3 to 14 | 12-cube base and high: HomePro retail asking THB 5 (10 or more) and THB 7 (single) for a 20 × 14 × 12 cm box (S, retail). 6 and 24 scaled, ASSUMPTION |
| Shelf price for a cube | 15 THB | 10 to 20 | ASSUMPTION (the cube is not priced; a 330 mL can sells at THB 15 to 17) |
| Ex-factory share of shelf | 60% | 50 to 70% | ASSUMPTION (no sourced margin) |

Sourcing note: the Thai Ministry of Commerce and Thai Customs trade statistics were not read directly. The UN Comtrade figures are a compiled view of Thai-reported data (tier P, with estimated weights). They are bulk import averages, so they are a floor for a small producer, not a quote. No Thai price for potassium bicarbonate, citric acid or a pouch was found.

### 7.2 Cost per cube (pH 3.5 base)

Reactants 0.18 THB, pouch 1.30, print 1.50, processing 0.50, giving 3.48 THB before carton. Packaging (pouch, print, processing) is 95% of this cost. The reactants are 5%.

| Pack size | Cubes per carton | Cost per cube (THB) | Ex-factory revenue per cube (THB) | Gross margin, base |
|---|---|---|---|---|
| Single pouch (no carton) | 1 | 3.48 | 9.00 | 61.3% |
| Six-cube carton | 6 | 4.15 | 9.00 | 53.9% |
| Twelve-cube carton | 12 | 3.90 | 9.00 | 56.7% |
| Twenty-four-cube carton | 24 | 3.85 | 9.00 | 57.2% |

The single-pouch margin is flattered because it carries no carton. The fair comparison is a retail carton for each pack size.

### 7.3 Units per container (volume-limited in every case)

Container internal dimensions: 20 ft 5,898 × 2,352 × 2,393 mm and 40 ft 12,032 × 2,352 × 2,393 mm (SeaCube spec, tier S; Maersk and ONE agree within 2 mm). Payload: 20 ft 28,200 kg (Maersk, tier P: 30,480 kg gross less 2,280 kg tare); 40 ft 26,840 kg (ONE, tier P: 30,480 kg gross less 3,640 kg tare). The 40 ft gross rating is disputed across sources. The packing efficiency of 92% is calibrated to a sourced grid count of 10,764 twelve-pack cartons per 20 ft (S-derived). Carton dimensions for 6, 12 and 24 packs are ASSUMPTION. The 12-pack carton, 190 × 150 × 100 mm, fits 12 pouches as three layers of four.

| Container | Pack | Cartons | Cubes | Container mass (kg) | Cost of goods (THB) | Ex-factory revenue (THB) | Gross margin before freight and overhead (THB) |
|---|---|---|---|---|---|---|---|
| 20 ft | Single | 161,588 | 161,588 | 1,015 | 562,326 | 1,454,292 | 891,966 (61.3%) |
| 20 ft | 6 | 21,431 | 128,586 | 2,951 | 533,203 | 1,157,274 | 624,071 (53.9%) |
| 20 ft | 12 | 10,715 | 128,580 | 1,879 | 501,033 | 1,157,220 | 656,187 (56.7%) |
| 20 ft | 24 | 5,357 | 128,568 | 1,343 | 495,630 | 1,157,112 | 661,482 (57.2%) |
| 40 ft | 12 | 21,860 | 262,320 | 3,833 | 1,022,174 | 2,360,880 | 1,338,706 (56.7%) |

Volume is the limit in every case. The 20 ft container holds about 128,600 cubes, or about 10,700 cartons of 12. Weight stays well inside the payload.

### 7.4 Sensitivity (cost per cube, 12-cube carton, THB)

- Target pH 3.0, 3.5, 4.0, 4.5: 3.98, 3.90, 3.87, 3.85. The acid choice moves cost by about 0.1 THB, so taste, not cost, drives it.
- Pouch price THB 1.00, 1.30, 1.67, 3.00: 3.60, 3.90, 4.27, 5.60. The pouch is the largest lever.
- Carton cost at 0.6×, 1.0× and 1.5×: 3.73, 3.90, 4.11.

## 8. Thai inputs, sourced and still open

Sourced (tier shown):
- Bangkok climate: TMD normals 1991 to 2020 (P). April mean maximum 35.7 °C; annual mean relative humidity 73%, 66 to 79%.
- Storage: no numeric Thai storage temperature for ambient packaged food in MoPH Notifications 367, 450, 469, 473 or 420 (P). The 35 °C case is anchored to the climate, not a rule.
- Tap-water alkalinity: the PWA water quality standard lists no alkalinity or bicarbonate (P). PWA consumer confidence reports for 2568 (Taku Pa) give total hardness of 5 to 84 mg/L as CaCO₃ and 14 to 80 mg/L at the second station (P). Alkalinity is not measured. The 0 to 150 mg/L sensitivity is wider than the evidence, which bounds alkalinity at or below hardness, about 84 mg/L. At that bound the citric need rises by about 0.2 g.
- Bottled drinking water: MoPH Notification 61 (B.E. 2524) sets a hardness limit of 100 mg/L (P). Notification 462 (B.E. 2568) is the current rule, in force 12 December 2025 (S).
- Sucralose sweetness: 600 to 650 times sucrose (JECFA monograph, P); 600 used. Codex GSFA maximum for carbonated drinks (14.1.4.1) is 600 mg/kg (P; archived FAO table; the current GSFA was not reached). The cube's 33 mg per 330 mL is about 100 mg/kg, inside that archived level.
- Thai food-additive rules: MoPH Notification 468 (B.E. 2568) took effect on 12 December 2568 (P). The Thai FDA clarification says a level permitted for 14.1.4 applies to its sub-categories (P).

Open:
- **Thai permission for the additives (gate G6, sale-blocking).** The FDA-hosted No. 468 annex list has no 14.1.4 row for potassium bicarbonate, citric acid, acesulfame potassium, sucralose or steviol glycosides. The gazetted annex is over the 10 MB reader limit and was not read. This is a limit, not a prohibition. Reading it needs a download with the user's permission.
- Thai potassium bicarbonate, citric acid and pouch prices (no Thai figure found); the print cost (placeholder).
- Deliquescence humidity of potassium bicarbonate and of anhydrous citric acid (not found).
- Current GSFA (2024) sucralose level for carbonated drinks (not reached).

## 9. What this changes for the handover

1. **The dose needs a decision.** At 25 °C the 0.9-volume design loses about 16% at once and holds fully only up to about 19 °C. At Thai ambient (30 to 35 °C) it loses 27 to 34%. Options for R&D:
   - Keep 0.9 volume and specify a chilled or iced serve. Ice at 30 g gives 21 °C, and 60 g gives 13 °C, which keeps 0.76 to 0.83 volume.
   - Lower the dose to 0.55 volume, which holds at every Thai serve in the model, including 35 °C (0.592). A 0.6-volume dose leaks about 1% at 35 °C. Potassium at 0.55 volume is about 317 mg per serve, or 9.0% of the Thai RDI.
2. **The acid load is several times a typical lime soda.** The pH target is a taste decision (section 5).
3. **Sweetener permission is open** (section 8). It blocks sale.
4. **Pack choice.** A 12-cube carton is the balance point in this model: 3.90 THB per cube and about 128,600 cubes per 20 ft container. The pouch price is the lever that matters, and the Thai pouch price is still missing.

## 10. Limits (not resolved on a desk)

- Fizz duration in a glass is kinetic. The model is a surface-only upper bound. Nucleation, stirring and the reaction time are not modelled, and no measured decay curve exists.
- Sensory thresholds come from mineral water (tier P) and a sports drink (tier S). No soft-drink threshold was found.
- Storage stability and the pouch moisture barrier need a humidity test, which is outside the no-lab-test scope. The anhydrous citric acid deliquescence humidity is not sourced.
- The potassium medical question (kidney disease, potassium-sparing drugs) is not answered by any desk figure.
- Claim thresholds: the potassium share of a reference value could trigger a nutrient claim under other rules. Thai claim rules were not checked. No claim wording is used (S1, F1, D4).
- Prices are inputs with the status shown. Bulk proxies are not quotes. No quote was requested.
