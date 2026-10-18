# Dye-penetration protocol: leaf-only wrap leak test (approved 18 October 2026)

Status: **approved** by the user on 18 October 2026, together with the leaf-only option for testing. Not yet run. The working design stays the leaf wrap with a food-grade PET inner barrier until this test reports.

## Question

Does a leaf-only wrap, with no inner barrier, leak a drink on thaw? The screen predicts a wrap-level leak probability of about 0.07 % at a damaged-cell fraction of 10⁻⁸, about 5 % at 10⁻⁷, and about 87 % at 10⁻⁶ for closed stomata (rework/31). The test measures the wrap-level leak probability directly.

## Design: one primary endpoint, pre-registered

- **Endpoint:** the number of wraps, out of N, that show any dye on the outer surface after thaw (k of N). A wrap "leaks" if at least one spot is seen.
- **Sample size:** N = 300 wraps. With zero leaks, the 95 % upper bound on the leak probability is about 1.0 % (1 − 0.05^(1/300)). A true leak probability of 5 % would give about 15 leaking wraps, so the test has the power to tell the screen's cases apart.
- **Pre-registered pass rule:** pass if k = 0 with N = 300 and all controls valid. Otherwise investigate. A single leak is not automatically a fail, but it needs an explanation that the controls support.
- **Provisional target:** no more than 1 % of wraps leaking. This is my proposal, to be confirmed by the team.

## Materials

- **Leaves:** fresh banana leaves (*Musa*), about 30 leaves for 300 wraps. Record the species and the cultivar if known. Harvest, store and handle all leaves in the same way, and test within 24 hours of harvest.
- **Wrap geometry:** 129 mm circumference × 100 mm high, matching the pop's wrap. Lateral area 129 cm² per wrap, so 300 wraps give 38,700 cm² of outer surface.
- **Core mimic:** an 8 % sucrose solution with 0.1 % brilliant blue FCF (E133, a food colour). The solution is frozen in a 38 mm diameter cylinder mould at −18 °C. Use a mould that matches the core radius.
- **Equipment:** a freezer at −18 °C (±1 °C), an incubator or room held at 30 °C (±1 °C), a flatbed scanner at 1200 dpi in colour, a loupe or stereo microscope, clear nail varnish for stomata imprints, and a clock.

## Procedure

1. **Assemble.** Wrap the leaf around the frozen core, leaf inner surface against the core, and secure with a food-safe clip or elastic. Record the wrap ID, leaf batch and position on the leaf.
2. **Freeze.** Hold at −18 °C for 24 h. The leaf freezes with the core, as in the real product.
3. **Thaw and contact.** Move each wrap to the 30 °C holding area, standing vertically on a clean white tray. Hold for 2 hours, which matches the thawed contact in the screen. Log the start and end times.
4. **Remove and dry.** Gently blot the outer surface without wiping across the leaf. Do not touch the outer surface with the tray or with any liquid.
5. **Scan.** Scan the full outer surface at 1200 dpi in colour, with a scale bar. Store the image with the wrap ID.
6. **Score.** Count spots of blue dye on the outer surface. A spot is at least 0.2 mm across and clearly blue. The scorer is blind to the group. Confirm each spot with the loupe.
7. **Stomata covariate.** Take a clear nail-varnish imprint of the outer surface of each wrap, and count stomata in three fields. Record the stomata per mm².

## Controls (must pass before the 300 results count)

- **Positive control (10 wraps):** three micro-punctures per wrap through both surfaces, made with a 0.1 mm pin. Expect spots in all 10 wraps. If any positive control shows no spot, the detection method has failed, and the 300 results do not count.
- **Negative control (10 wraps):** the same procedure with a food-grade PET film placed inside between the leaf and the core. Expect no spots in any of the 10 wraps. Any spot here points to contamination of the outer surface, not a leak.
- **Condensate control:** keep the tray dry and the room below dew point of the outer surface, and record any drips. A drip on the outer surface is not counted as a leak unless it links to a spot.

## Covariates to record

- Stomata per mm² (imprint).
- Leaf batch and position.
- Thaw temperature and contact time.
- Freeze profile (log of the freezer, if available).

## Interpretation

- **Pass (k = 0 among closed-state wraps, at least 270 of 300 closed, controls valid):** for closed-state wraps, the leaf-only leak probability is below about 1.1 % at 95 % confidence (1 − 0.05^(1/270)). The leaf-only option moves forward as a candidate, and the team decides whether to keep the barrier or switch. Step 7a sets the closed-state rule.
- **Fail (k ≥ 1 among closed-state wraps, controls valid):** the leaf-only option is rejected for this product. The working design stays the barrier.
- **Inconclusive (fewer than 270 of 300 closed):** the run does not answer the leaf-only question. Report the open-state results as a stomatal-state finding.
- **Pattern check:** compare k with the screen's prediction. If k is far above the screen's value at the measured stomata density, that points to a mechanism the screen does not include.
- **Confirmation step:** on a pass, repeat with 30 wraps of the actual coconut-pandan drink in place of the sucrose core, because the drink's viscosity may differ.

## What is needed to run it

- Thirty fresh banana leaves, and the person who will run the lab work.
- A freezer at −18 °C and an incubator at 30 °C.
- A flatbed scanner, E133 food colour, 8 % sucrose, a 38 mm mould, and PET film for the negative control.
- Around one week for the batches, with about 50 wraps per day.

## Amendment: stomatal-state check (adopted 18 October, per recommendation; reviewable)

Source: the simulation in rework/34 shows that the stomatal state changes the outcome more than breach fraction does. The rule below is adopted as the working protocol for any future run. The physical run is not scheduled in the desk plan. The team can reopen the rule after a pilot, if the agreement check in step 5 fails.

**Order.** Steps 5 and 6 (scan and dye count) come first. Step 7 (imprint) follows on the same wrap, after the dye count. The stomatal scorer is blind to the group and to the dye result.

**Step 7a: scoring rule (final).**

1. **Fields.** Score three fixed fields per imprint. Every field has the same area and the same magnification on a stereo microscope. The field area is set in a pilot on 5 fresh leaves so that a field holds about 5 stomata on average. The pilot is done before any wrap is made.
2. **Open or closed, per stoma.** A stoma is open if the pore shows a visible gap between its two guard cells at the fixed magnification. Otherwise it is closed.
3. **Open or closed, per wrap (presence rule).** A wrap is open-state if at least one stoma in its three fields is called open. A wrap is closed-state if no stoma is called open and at least 15 stomata are counted across the three fields. The 15 is proposed and may be changed in the pilot.
4. **Not scorable.** A wrap with fewer than 15 stomata counted, or an unreadable imprint, is re-imprinted once. If it is still not scorable, it is reported as not scorable and left out of both groups. The count is stated.
5. **Agreement check before the run.** Two scorers call the state on the same 10 pilot imprints, independently. They must agree on at least 9 of 10 wraps. Any open call that the two scorers dispute goes to a third scorer. If agreement fails, the rule is changed and re-tested before any wrap is scored.
6. **Baseline.** Take imprints from 10 fresh, unfrozen leaves from the same batch and score them with the same rule. Report the baseline open fraction. This shows whether freezing and thawing change the state. It has no pass or fail.
7. **Direction of error.** The presence rule calls more wraps open than a majority rule would. This is deliberate. One open stoma is enough for the outer surface to connect, as modelled in rework/34, so the rule errs toward the barrier.

**Reporting and interpretation (replaces the earlier text).**

- Report k of N among closed-state wraps, k of N among open-state wraps, and the count of not-scorable wraps.
- The leaf-only pass needs k = 0 among closed-state wraps, controls valid, and at least 270 of the 300 wraps scored closed (90 %, proposed). With fewer closed wraps, the run is inconclusive for leaf-only.
- An open-state wrap that leaks is a stomatal-state finding, not a breach result. An open-state wrap that does not leak is reported and does not count toward the pass.
- Production implication: a leaf-only product needs closed stomata after freeze and thaw. The test can show whether that happens. The product cannot control it directly, so a leaf-only design carries a stomatal-state risk that the barrier design does not.

## Limits

- The core is a sucrose solution, not the coconut-pandan drink, so the first run tests the leaf and not the drink.
- A wrap test does not separate the outer-surface route from the inner one. It measures the event that matters for the product.
- Dye detection depends on the threshold. The positive control sets the detection floor.
