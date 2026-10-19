# Coupled thaw and wicking simulation: classical results

> **Retired 18 October 2026.** This record belongs to candidate A (the leaf-wrapped frozen drink) or to a retired step of the desk work. See [README](README.md). Kept for the record.

Date: 18 October 2026. Script: [screen/pop_leak_simulation.py](screen/pop_leak_simulation.py). Raw output: [screen/pop_leak_simulation_results.json](screen/pop_leak_simulation_results.json). Plot: [screen/pop_leak_simulation.png](screen/pop_leak_simulation.png).

Status: virtual screen only. Inputs are assumptions or analogue values (see [16](16_permeability_seam_estimate.md)). Nothing here is a measurement.

## Thaw at 30 °C (nominal, h = 10 W/m²K)

| Quantity | Value | Note |
|---|---|---|
| Surface begins to melt (t_wet) | 0.22 h (about 13 min) | Edge wetting time, the start of the wicking window |
| 50% thawed | 1.53 h | Sippable slush |
| 100% thawed | 3.26 h (8-node grid), 3.28 h (16-node grid) | Grid converged to 0.6% |

The earlier lumped screen gave a full thaw at 2.47 h. Conduction makes the core lag, so the full thaw is later, at 3.3 h. The planned two-hour window is therefore a slush window, not a full thaw.

## Leak screen (Monte Carlo, 200 runs, 2 h window)

| Design | Result |
|---|---|
| A: leaf-only, cut edges in melt contact | Leaks in 100% of runs. The exposed vessel path wicks the 100 mm wrap within minutes of wetting |
| B: leaf-only, edges sealed, freeze-damaged surface paths | Critical damaged-path radius 0.24 µm (5–95%: 0.14 to 0.45 µm). Any damaged path wider than this leaks within the window |
| C: continuous inner film | No pores, so no liquid path in this model. Film defects and seams are not modelled |

Intact cuticle pores (0.3 to 2 nm) sit far below the threshold, so an intact surface holds. Design B turns on the freeze-damage size, which nothing has measured.

## Reading against the decisions in 16 and 15

- Design A fails in every run. Any leaf-only design needs its cut edges out of the melt pool.
- Design B's threshold (0.14 to 0.45 µm) is wider than the 0.16 µm estimate in 16, because the wetting time adds about 13 minutes. It does not change the decisions: the plastic-free claim stays dropped, and the film arm is the closed fallback.
- The open question is the size of freeze-damage paths. The model shows exactly how wide one would need to be to leak.
