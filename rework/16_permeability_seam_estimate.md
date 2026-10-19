# Leaf permeability and seam quality: virtual estimate and decisions

> **Retired 18 October 2026.** This record belongs to candidate A (the leaf-wrapped frozen drink) or to a retired step of the desk work. See [README](README.md). Kept for the record.

Status: virtual only. No physical test was run, and none will be run. Each decision below is closed on the evidence stated, with its uncertainty. Limits that virtual evidence cannot close are listed at the end as limits, not as pending work.

## 1. Sourced inputs (research workflow wuilchzkv, 18 October 2026)

| Quantity | Value | Basis | Source | Use here |
|---|---|---|---|---|
| Water contact angle, upper (adaxial) surface, banana | 76.1° (apparent) | measured, medium confidence | Jiang et al. 2022, Materials 15(3):917 | Wicking angle, liquid spreads on the upper surface |
| Water contact angle, lower (abaxial) surface, banana | 94.3° | measured, medium confidence | Same | cos < 0, so no spontaneous wicking from the lower surface |
| Dried leaf thickness (klaras, *Musa brachycarpa*) | 0.213 mm | measured, low confidence (abstract) | UGM thesis 2014 | Thickness, dried only |
| Water vapour flux, dried leaf | 0.465–0.5 mg/cm²·h | measured, medium confidence (two theses) | UGM 2014 | Vapour only, not liquid leakage |
| Water vapour transmission, derived | 112–120 g/m²·day | estimated arithmetic | From the flux above | Not a standard WVTR |
| Cuticle aqueous pore radius | 0.3–2 nm | estimated, analogue (ivy, coffee, citrus) | Tredenick et al. 2017 and cited work | Intact cuticle path |
| Vessel hydraulic diameter, midrib tip | 5.5–6.5 µm | measured, **analogue** (sycamore maple) | Lechthaler et al. 2019 | Exposed-vessel path, order of magnitude only |
| Freeze-thaw electrolyte leakage, leaf | up to 90% at −16.5 °C | measured, analogue (Arabidopsis, leaf tissue) | Nezami et al. 2010 | Membrane damage at −18 °C freezing |
| Seam or fold leak data for any leaf wrap | none found | gap | Research workflow | Not closable virtually |
| Whole-leaf WVTR, porosity, tensile strength | none found for banana or pandan | gap | Research workflow | Not closable virtually |

Not used as evidence: lime, plastic bag, fibre, coated paper, and laminate values. They are analogues of other materials and do not describe the leaf.

## 2. Virtual leak screen (Washburn wicking)

Script: [screen/leaf_wicking_screen.py](screen/leaf_wicking_screen.py). Results: [screen/leaf_wicking_screen_results.json](screen/leaf_wicking_screen_results.json).

Model: Washburn capillary rise, h² = γ r cos θ t / (2η). Assumptions: γ = 0.072 N/m, η = 1 mPa·s, wrap height 100 mm, thaw window 2 h. Straight-tube model, so real tortuous paths are slower. Treat the result as a bound.

**Critical pore radius** (the smallest radius that wicks the 100 mm wrap within 2 h): **160 nm** at the measured upper-surface angle. Across the sensitivity range (η 1 to 3 mPa·s, θ 60° to 76°) it spans **77 to 481 nm**.

| Path | Radius (analogue) | Height at 2 h | Time to 100 mm | Leak path? |
|---|---|---|---|---|
| Intact cuticle, low | 0.3 nm | 4 mm | not reached within a day | no |
| Intact cuticle, high | 2 nm | 11 mm | about 160 h | no |
| Exposed vessel, narrow | 2.75 µm | 414 mm | 7 min | **yes** |
| Exposed vessel, wide | 12.5 µm | 883 mm | 1.5 min | **yes** |
| Intact lower surface | 2 nm | none (cos θ < 0) | none | no |

**Reading:** an intact cuticle is about 100 times narrower than the threshold, so the surface holds. A cut or torn edge that exposes vessels, once in contact with melt water, wicks the whole wrap within minutes. The vessel radii are sycamore analogues, but the order of magnitude sits far above the threshold, so the conclusion holds across any plausible banana vessel size.

## 3. Decisions closed virtually

| ID | Decision | Closed by | Confidence | Consequence |
|---|---|---|---|---|
| D1 | An intact leaf surface does not leak liquid within the window | Screen: cuticle pores 0.3 to 2 nm against a 77 to 481 nm threshold | Medium (analogue pore sizes, straight-tube bound) | Intact surface is acceptable |
| D2 | A cut or torn edge in contact with melt water is a leak path | Screen: exposed vessels wick the wrap in 1.5 to 7 min | Medium (analogue vessel size) | Edges must stay out of the melt pool, or be sealed |
| D3 | The leaf-only design cannot be shown to avoid D2 | No seam or edge-sealing data exists | Medium | The leaf-only arm is not proven |
| D4 | A continuous non-porous film blocks the wicking path | Screen: a film has no pores | High (physics) | The film arm passes the liquid screen |
| D5 | The "plastic-free" claim is **dropped** for now | D3 plus D4: the only design that passes is not plastic-free | Medium | The product is described as **leaf-wrapped**, not plastic-free. Reopen only if seal data appear |

## 4. Limits that virtual evidence cannot close

These are disclosed in the proposal. They are not treated as pending tests.

- **Freeze-damage permeability (L1):** freezing at −18 °C damages leaf membranes (electrolyte leakage up to 90% in leaf tissue). Whether it opens paths wider than the 160 nm threshold is unknown. This is the largest remaining risk to the leaf-only design, and the screen cannot size it.
- **Seam and fold strength (L2):** no data exists for any leaf seam, fold or overlap. The screen treats the seam as a leak path only if it exposes an edge.
- **Fresh leaf thickness and porosity (L3):** only the dried thickness (0.213 mm) and analogue vessel sizes are known. These affect vapour and wicking only at the margin, but they are not measured for banana or pandan.
- **Vapour transmission (L4):** only a derived, unstandardised figure exists. Vapour loss is not a leak, so this does not change D1 to D5.

## 5. What this means for the concept

- **Claim:** "leaf-wrapped frozen pop". Not "plastic-free".
- **Design rule:** keep cut edges out of the melt pool. If that can't be guaranteed, use the film arm and drop the leaf-only claim.
- **Disclosure:** state L1 (freeze damage) and L2 (seam strength) in the proposal as known, unquantified risks.
- **Confidence:** the screen supports a reasoned decision, not a measured guarantee. It was built from analogue pore sizes and a straight-tube model.
