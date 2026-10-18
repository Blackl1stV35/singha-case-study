# Resolved parameters and the working design (18 October 2026)

The screens had unknown parameters: drink composition, lag, damage size and density, stomata, and the process. This note resolves each one from physical reasoning, states its basis and sensitivity, and records the consequence for the design. Values are physics-based assumptions, not measurements. Code: `rework/screen/resolve_parameters.py`, results `rework/screen/resolved_parameters_results.json`.

## Resolved values

| Parameter | Resolved value | Physical basis | Sensitivity |
|---|---|---|---|
| Water activity, drink | 0.995 | ideal (Raoult) water activity of a 8 % sugar solution | not a limiting factor; growth is near optimal |
| pH, drink | 6.3 | coconut milk is near neutral | near the optimum for most spoilage and pathogenic organisms |
| Lag parameter h0 (cold-stressed cells) | 2.0, so lag = h0 / mu, about 1 h at mu = 2 per h | Baranyi model, typical 1 to 3 for stressed cells | ignoring lag (done in the screens) is conservative |
| Drink viscosity (for wicking) | 1.0 mPa·s, the lower bound | coconut milk with fat and sugar may be higher | at 3 mPa·s the climb times are three times longer and the threshold radius three times larger, so the lower bound is conservative |
| Damaged-path radius | log-uniform 0.1 to 1 um | freeze rupture of plant cell walls gives gaps of the order of the cell-wall thickness | single-path leak probability 0.62 over 0.1 to 1 um; 0.36 over 0.1 to 0.3 um; 0.86 over 0.3 to 1 um |
| Cells per wrap | 1.7 x 10^7 | wrap area 0.0155 m² divided by a 30 um mesophyll cell | order of magnitude |
| Freeze-damaged cell fraction | not measurable here; the screen brackets 10^-6 to 10^-2 | freezing damages a finite fraction of cells | the sealed design is decided by this value (see below) |
| Stomatal pores | open pores of 5 to 15 um radius wick the wrap in 77 to 231 s | Washburn climb of the full wrap height | open or closed state after death is unknown; open pores defeat the seal |
| Contact angle, outside water | intact wax: no climb; exposed cell wall: 76 degrees | capillary climb needs cos theta above zero | as in rework/22, section 7 |
| Spoilage start load after production | 10^-2 CFU/mL target after a 5-log kill step on a 10^3 CFU/mL base | a kill step sets the start load; time-based rules cannot offset a high start load | depends on the raw base, which is not yet specified |

## What the damage fraction does

With the resolved damage radius, a single damaged path leaks with probability 0.62. The expected number of leaking paths per wrap is:

| Freeze-damaged fraction | Damaged cells per wrap | Expected leaking paths per wrap |
|---|---|---|
| 10^-6 | 17 | about 11 |
| 10^-4 | 1,700 | about 1,100 |
| 10^-2 | 170,000 | about 107,000 |

One leaking path per wrap needs a damaged fraction of about 10^-7. Connection along the 100 mm wrap height, estimated from the spacing of leaking paths being shorter than the wrap height, needs about 1.5 x 10^-7. Freeze damage in plant tissue is many orders of magnitude above this. So a leaf-only seal cannot be assumed to hold physically.

## Decision

1. **Working design: a leaf wrap with a food-grade inner barrier (the fallback film).** The leaf stays as the outer wrap, and the inner barrier removes the damaged-path problem. This is decided on the physics above, under the delegation of decisions to me on 18 October. It is reversible if a barrier-free seal is later shown to hold.
2. **Claim: "leaf-wrapped".** Not plastic-free. The inner barrier is plastic, so this claim must say so if pressed.
3. **Leaf-only is recorded as rejected on physical grounds**, not on a test result.
4. **Stomata.** The inner barrier also seals open stomata, which would otherwise wick the wrap in minutes.
5. **Production.** A 5-log kill step on the drink base, as set in rework/29, is still required.

## Limits

- The freeze-damaged fraction is unmeasured. The decision rests on the physical bound of about 10^-7, which is far below any plausible freeze damage. An edible or barrier-free option would need its own physical case.
- The percolation estimate is a spacing argument, not a full network model.
- The stomatal state and the damage radius are assumed, and the resolved values are conservative in the direction that favours the barrier.
- The consumer and taste effects of the inner barrier are not assessed.
