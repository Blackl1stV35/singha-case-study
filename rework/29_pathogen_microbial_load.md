# Pathogens and microbial load for the thawed pop (18 October 2026)

> **Retired 18 October 2026.** This record belongs to candidate A (the leaf-wrapped frozen drink) or to a retired step of the desk work. See [README](README.md). Kept for the record.

Question: after thaw, can pathogens grow to a hazard in one serving, and does the microbial start load matter more than the time after thaw?

Short answer: the start load decides the risk. From one contaminating cell per serving, the hazard is reached after about 6 to 27 hours at 30 °C, so the 2-hour limit leaves a wide margin. But a serving that starts at or above the hazard level is hazardous at once, whatever the time. Production control is therefore the binding requirement, and the time rules are secondary.

## Method

- **Serving:** one 170 mL serving, starting from one contaminating cell (assumed low-level contamination).
- **Growth:** the Ratkowsky square-root model with a separate minimum and maximum temperature for each pathogen, applied to the bulk temperature (mean of core and surface) from the thermal screen. No growth while frozen. The lag phase is ignored, which is conservative.
- **Hazard:** a per-serving level for each organism. For toxin-formers it is the level that produces toxin, which is about 10^5 CFU/g in the literature; for infectious organisms it is a low infective dose. All levels are assumptions.
- **Code:** `rework/screen/pathogen_screen.py`, results `rework/screen/pathogen_screen_results.json`.

| Organism | Min / max temperature (C) | Relative growth at 30 C (per h) | Hazard per serving | Basis |
|---|---|---|---|---|
| *Salmonella* | 5.2 / 46 | 0.8 | 10^3 | low infective dose |
| *E. coli* O157:H7 | 7 / 45 | 0.8 | 10^2 | very low infective dose |
| *Listeria monocytogenes* | −1.5 / 45 | 0.4 | 10^2 | grows in the cold; susceptible groups |
| *Staphylococcus aureus* (enterotoxin) | 7 / 45 | 0.6 | 10^7 | toxin level about 10^5 CFU/g |
| *Bacillus cereus* (emetic toxin) | 4 / 48 | 1.0 | 10^7 | toxin level about 10^5 CFU/g |

## Results

**Hours from one cell per serving to the hazard, at constant temperature:**

| Organism | 30 C | 35 C |
|---|---|---|
| *E. coli* O157:H7 | 5.8 h | 4.7 h |
| *Salmonella* | 8.6 h | 7.0 h |
| *Listeria monocytogenes* | 11.5 h | 10.4 h |
| *B. cereus* (emetic toxin) | 16.1 h | 12.5 h |
| *S. aureus* (enterotoxin) | 26.9 h | 21.9 h |

**Two-hour check:** from one cell, 2 h at 30 °C gives 2 to 7 cells per serving, far below every hazard level.

**Start-load sensitivity at 30 °C** (hours to hazard; 0 means the hazard is already present):

| Start load per serving | *Salmonella* | *E. coli* | *Listeria* | *B. cereus* | *S. aureus* |
|---|---|---|---|---|---|
| 1 cell | 8.6 h | 5.8 h | 11.5 h | 16.1 h | 26.9 h |
| 10 cells | 5.8 h | 2.9 h | 5.8 h | 13.8 h | 23.0 h |
| 100 cells | 2.9 h | 0 h | 0 h | 11.5 h | 19.2 h |
| 1,000 cells | 0 h | 0 h | 0 h | 9.2 h | 15.4 h |
| 100,000 cells | 0 h | 0 h | 0 h | 4.6 h | 7.7 h |

**Thai scenarios:** from one cell per serving, no hazard is reached within the scenario windows (at most 6 h), for any organism. The thermal traces warm the bulk too slowly.

**Spoilage organisms, for comparison:** from 10^2 CFU/mL to visible spoilage (10^7) takes 5.8 h at 30 °C. From 10^4 it takes 3.5 h.

## Decisions

1. **Production control is required.** A validated kill step on the drink base (pasteurisation or an equivalent step), or a hygienic process with pathogen-free raw material. Freezing does not kill *Listeria* or *Salmonella*. The start load must be controlled before freezing.
2. **Keep the Thai 2-hour and 5 °C rules.** At one cell per serving they leave a wide margin, and they are the operative time limit for food-premises sale.
3. **Keep outside water out of the wrap.** Leaf surfaces and outside water can carry pathogens. Wicking through a damaged path therefore brings a route to contamination as well as spoilage (rework/28).
4. **Release testing is a production control, not a product test.** Any real launch needs batch testing for the organisms above. It is outside this virtual screen, and it is not a physical leak or taste test.

## Limits

- The growth and cardinal parameters are generic and assumed, and no matrix or product-specific data exist.
- The lag phase is ignored, and the single-cell start is an assumption about contamination.
- Toxin formation is modelled only as a level threshold, not as toxin kinetics.
- The real process, the drink's pH and water activity, and any preservatives are unknown.
- The screen gives time scales and start-load thresholds. It does not certify safety.
