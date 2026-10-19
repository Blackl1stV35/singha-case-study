# Component 1 (Ingredients and Nutrition): food-science check of the lime cube (19 October 2026)

Status: a desk check of the chemistry and arithmetic of the cube recorded in [rework/45](45_working_candidate_rework.md). No bench test: the lab test is dropped (S2), so every figure is a model output and every check below is a stated limit. The check finds that the cube can be recorrected in three places. None of the changes creates a sodium-free, fizz, health or sugar-free claim.

**Recorrection confirmed by the user (19 October 2026):** (1) the dose is set by what the drink holds, 0.9 volume of CO₂ per 330 ml, not 1.75 volumes; (2) the free-acid excess is set by titration to a target pH, not left at the stoichiometric 1:3 ratio; (3) any potassium-bearing sweetener has its potassium counted. Sweetener: sucralose (no potassium), recommended and confirmed by the user on 19 October 2026. The Thai permission check is pending, with steviol glycosides as the fallback. The next step is a desk test to resolve the limits in section 5. Its figures are to be handed to the company's internal R&D department.

## 1. The recorded construction

- Potassium bicarbonate and citric acid, stoichiometric, dosed at 1.5 and 1.75 volumes of CO₂ per 330 ml.
- 1,007 mg potassium per 330 ml at 1.75 volumes (rework/45, G3).
- Intensive sweetener, not yet named. Natural lime flavour.

## 2. Checks

### 2.1 Stoichiometry (checked; the record's numbers hold)

Reaction: 3 KHCO₃ + C₆H₈O₇ → K₃C₆H₅O₇ + 3 CO₂ + 3 H₂O.

- 1.5 volumes: 0.02208 mol CO₂ per 330 ml; KHCO₃ 2.21 g; citric acid 1.41 g; potassium 864 mg.
- 1.75 volumes: 0.02576 mol CO₂; potassium 1,007 mg.

### 2.2 Recorrection 1: the dose is set by what the glass can hold, not by what the reaction releases

The 1.75-volume figure is the CO₂ released by the reaction. It is not the CO₂ the drink keeps. In an open glass at 1 atmosphere, the solubility is about 0.76 volumes at 25 °C (rework/45 §8). Colder water holds more: the handbook value at 0 °C is about 1.7 volumes, and the values at 4 to 5 °C are higher than the 25 °C value. Those are not sourced in this repo and must be cited (NIST) before use.

So a 1.75-volume dose cannot stay dissolved at room temperature. The excess leaves as bubbles in the first minutes, and the rework/45 fizz figure has no basis.

Recorrected dose: **0.9 volume** of CO₂ per 330 ml. This sits at the room-temperature ceiling and below the cold ceiling, so it holds in a cold drink and reaches near saturation at room temperature.

- CO₂: 0.0132 mol; KHCO₃ 1.33 g; citric acid (stoichiometric) 0.85 g; potassium **518 mg** per 330 ml.
- Potassium is about 15% of the reference intake that rework/45 uses (about 3,460 mg, derived from its "25%" statement, not sourced here). That is half the 1,007 mg in the record.
- Trade-off: at 0.9 volume the effervescence is faint, not a can-like fizz. The fizz is weaker and stays a limit. No fizz claim is made.

### 2.3 Recorrection 2: the stoichiometric acid makes a salt, not a lime drink

If citric acid is exactly matched to bicarbonate (1 mol per 3 mol), every acid group is used up. What is left is potassium citrate, a basic-to-neutral salt, plus dissolved CO₂. A hand estimate of the carbonate–citrate balance puts the drink above pH 4. That is flat and soapy, not tart.

So the excess acid is not a detail. It sets the taste. rework/45 says "citric acid excess assumed" without a figure. The recipe needs a free-acid excess, chosen to a target pH for a lime soda. The target pH is an ASSUMPTION (about pH 3) and needs a source. A rough buffer estimate puts the excess at about the same mass as the stoichiometric citric acid, so the citric acid mass could roughly double. This is unmeasured.

Potassium does not change with the excess acid. Only the citric acid mass and the acid load change.

### 2.4 Recorrection 3: the sweetener can add potassium

Acesulfame-K is 19.4% potassium by weight (39.10 / 201.24). rework/45 counts only the bicarbonate. If acesulfame-K is the sweetener, its potassium is added on top. For example, 100 mg of acesulfame-K adds about 19 mg potassium.

Choose a sweetener without potassium (sucralose, or a steviol glycoside), or count the sweetener's potassium in the declaration. The permitted-additive check is gate G6, still open.

### 2.5 Moisture and storage (added check)

Potassium bicarbonate and citric acid react in the presence of water. A moisture barrier matters for a dry cube. rework/mockup/MATERIALS_pouch_stack.md lists an aluminium foil layer (ASSUMPTION, 7 to 9 µm). No water-vapour transmission rate is sourced, and no humidity test was run. Storage stability stays open. No shelf-life claim is made.

### 2.6 Nutrition declaration (what the label would show)

Per 330 ml, after the recorrection:

- Sugar: 0 g from the recipe (no sugar is added).
- Sodium: 0 from the carbonate. The water basis is unsourced (rework/52 open item 4).
- Potassium: 518 mg at 0.9 volume (was 1,007 mg at 1.75 volumes).
- Energy: not calculated.

These are declarations. Claim wording stays barred (S1, F1, D4).

## 3. What the component can and cannot carry

- **Can:** the sweetener named; potassium declared as a fact; the nutrition panel.
- **Cannot:** sodium-free, sugar-free, fizz, health or low-potassium wording.

Whether a declared potassium figure needs a medical reading (potassium-sparing drugs, kidney disease) is still open. The desk check does not settle it.

## 4. Effect on the record

- rework/45 dose: 1.75 volumes becomes 0.9 volume (recorrected). Potassium 1,007 mg becomes 518 mg per 330 ml.
- Acid: the stoichiometric citric acid is a minimum, not the recipe. The excess must be set to a target pH.
- Sweetener: pick one with no potassium, or count it.
- Pillar fit (Ingredients and Nutrition): the sodium-free route stays. The recorrected dose lowers the potassium exposure. The fit is still moderate, because the fizz is weaker and the taste rests on an unmeasured acid excess.

## 5. Limits

- All figures are desk models. The lab and medical tests are dropped (S2, S3). If the user reinstates a bench step, the first test is titration to the target pH and a dissolved-CO₂ measurement at the 0.9-volume dose.
- Solubility values come from the handbook and are not yet cited (NIST, per rework/45 §8).
- The reference intake (about 3,460 mg) is derived from rework/45, not sourced here.
- The sweetener is not chosen. Its permission (G6) is open.
- Energy is not calculated.
