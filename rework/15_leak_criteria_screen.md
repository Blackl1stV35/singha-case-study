# Leak test: criteria set from physics, then a screen (stage-gate)

Status: criteria set before any sample is made. The thaw screen is run. The leak itself is not screened and stays a physical test (pended, as instructed).

## Stage-gate approach

1. **Set criteria first.** Thresholds are fixed before any run, so the test can't be read to suit the result.
2. **Screen with physics.** A cheap model can kill or redesign a concept before samples are made. A failed screen is a kill. A passed screen is not evidence.
3. **Physical tests decide.** Only concepts that pass the screen go to samples.

## What the physics can and cannot screen

| Question | Can physics screen it? | Why |
|---|---|---|
| How long to a sippable slush or full thaw at 30 °C | Yes, as a bounded estimate | Heat balance on a frozen core. Needs the heat-transfer coefficient, which is measured, not assumed |
| Does the leaf leak during thaw | No | Depends on leaf permeability, seam quality and wicking. None measured |
| Does freezing expansion split the wrap | Not applicable | The pop is frozen first and wrapped after, so no expansion occurs inside the wrap |

## Screen (lumped heat balance, assumed properties)

Script: [screen/leak_thaw_screen.py](screen/leak_thaw_screen.py). Results: [screen/leak_thaw_screen_results.json](screen/leak_thaw_screen_results.json).

Assumptions (replace with measurements): core 19 mm radius, 150 mm long, 170 mL, 0.17 kg. Frozen start at −18 °C, freezing onset at −1 °C, latent heat 300 kJ/kg, ambient 30 °C.

| Surface coefficient h (W/m²K) | 50% thawed | 100% thawed |
|---|---|---|
| 5 | 2.7 h | 4.9 h |
| 10 | 1.3 h | 2.5 h |
| 15 | 0.9 h | 1.7 h |

Mass sensitivity at h = 10: 0.14 kg gives 1.1 h to 50% and 2.0 h to 100%. 0.20 kg gives 1.6 h and 2.9 h.

**Reading:**
- A fully liquid pop at 30 °C takes 1.7 to 4.9 h. The planned two-hour window falls inside that range, so a fixed two-hour window can't by itself be a pass or fail. The test needs the real h.
- A sippable slush (50% thawed) takes about 0.9 to 2.7 h. That fits the "sip as it thaws" idea, but the window depends on h.
- The leak itself is not in this screen. No physics here can say whether the leaf leaks.

## Criteria (proposed, to be agreed before the test)

| ID | Criterion | Type | Pass | Fail → action |
|---|---|---|---|---|
| C1 | Core temperature traced by thermocouple during the thaw | Physical | Trace logged, and h estimated from it | No trace → repeat with the thermocouple |
| C2 | Sippable slush (50% thawed) within the window the team sets | Physical, from C1 | Reached inside the window | Window too short or long → change the product window, not the leaf |
| C3 | Leaf-only arm: no visible liquid outside the wrap through full thaw | Physical | Zero leaks | Leaks → go to the film arm |
| C4 | Film arm: no leaks through full thaw | Physical | Zero leaks | Leaks → redesign the seal |
| C5 | Decision: plastic-free claim | Decision | Keep the claim only if C3 passes | If C3 fails and C4 passes, drop the plastic-free claim (film is plastic) |

## Virtual close (18 October 2026, after the physical test was removed)

The physical test will not happen. C2 to C5 are closed virtually in [16_permeability_seam_estimate.md](16_permeability_seam_estimate.md):

- **C3 (leaf-only):** closed as a decision. The leaf-only design is not proven, because cut edges in contact with melt water wick the wrap in minutes (D2 and D3).
- **C4 (film arm):** closed as a decision. A continuous film passes the liquid screen (D4).
- **C5 (plastic-free claim):** closed as dropped (D5). The product is described as leaf-wrapped.
- **C1 and C2 (thaw trace and window):** the thaw screen shows a fully liquid pop at 30 °C takes 1.7 to 4.9 h, so the window needs the measured heat-transfer coefficient. Closed as a limit: the window is set from the screen, not from a trace.
- **Remaining limits (not closed virtually):** freeze-damage permeability (L1) and seam strength (L2). These are disclosed in the proposal.

## Gates

- **Gate 0 (done today):** desk checks, criteria set, thaw screen. No kill on thaw timing. Leakage not screened.
- **Gate 1 (closed virtually, 18 October):** C1 to C5 closed as above. No physical test will be run.
- **Gate 2 (pended):** consumer test of the slush and the leaf wrap.

## Limits

- The model is lumped. It ignores heat conduction inside the core, and it takes the properties as assumed.
- Blender is not used as evidence in any gate.
- A pass at Gate 0 is not a pass of the product. A fail at Gate 0 would be a kill. The screen didn't kill anything.
