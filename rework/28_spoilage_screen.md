# Spoilage screen: the rotten condition on the package (18 October 2026)

Question: after the pop thaws, does the drink or the leaf wrap rot before it is eaten, and what time limit follows?

Short answer: the drink does not spoil within the time it takes to reach the Thai 2-hour limit. Spoilage needs about 4 to 12 hours of warm holding. The two-hour rule therefore stays the operative limit. Contamination from outside water shortens the time to spoilage by about 40 %. The leaf does not rot within a single event, but a wrapped pop stored wet after an event would.

## Method

- **Growth model:** the square-root (Ratkowsky) model with generic mesophile parameters, fitted so that the growth rate at 30 °C equals 2 per hour (doubling about 21 min, fast case) or 1 per hour (doubling about 42 min, slow case). Cardinal temperatures are 0 °C and 45 °C, with c = 0.2 per °C. These are physics-based assumptions for a nutrient-rich coconut drink, not measurements.
- **Temperature history:** the bulk temperature is the mean of the core and surface temperatures from the thermal screen. No growth while frozen.
- **Spoilage threshold:** 10^7 CFU/mL (assumed; visible spoilage is about 10^7 to 10^8).
- **Start loads:** 10^2 CFU/mL for a sealed drink, 10^4 CFU/mL if outside water has wicked in (assumed).
- **Lag phase:** ignored. This is conservative, because it makes spoilage earlier.
- **Code:** `rework/screen/spoilage_screen.py`, results `rework/screen/spoilage_screen_results.json`.

## Results

**Constant temperature, hours after thaw to spoilage** (fast case, sealed start; slow case in brackets):

| Holding temperature | Sealed (10^2) | Contaminated (10^4) |
|---|---|---|
| 5 °C | 187 h (375 h) | 112 h (225 h) |
| 10 °C | 47 h (94 h) | 28 h (56 h) |
| 20 °C | 12 h (24 h) | 7.1 h (14 h) |
| 25 °C | 7.8 h (16 h) | 4.7 h (9.3 h) |
| 30 °C | 5.8 h (12 h) | 3.5 h (6.9 h) |
| 35 °C | 5.1 h (10 h) | 3.1 h (6.1 h) |
| 40 °C | 7.3 h (15 h) | 4.4 h (8.8 h) |

The rate peaks near 35 °C and falls at 40 °C, which the cardinal model predicts.

**Thai scenarios** (the bulk temperature history from the thermal screen, fast case):

| Scenario | Window | Sealed drink reaches spoilage | Contaminated drink reaches spoilage |
|---|---|---|---|
| Street stall, shade (S1) | 6 h | not within 6 h | 5.5 h |
| Street stall, full sun (S2) | 6 h | not within 6 h | not within 6 h |
| Festival stall in sun (SU1) | 3 h | not within 3 h | not within 3 h |
| Songkran splash, 2 h (SU2) | 2 h | not within 2 h | not within 2 h |
| Ice-water cooler, 4 h (SU3) | 4 h | not within 4 h | not within 4 h |
| Insulated cooler with gel packs, 4 h (SU4) | 4 h | not within 4 h | not within 4 h |
| Parked car, 3 h (SU5) | 3 h | not within 3 h | not within 3 h |

Within each event window, the sealed drink does not spoil. The contaminated drink spoils only in shade over 5.5 h, and only if outside water has wicked in.

## Leaf rot

- The screens keep the outside of the wrap wet for at most about 4 h (ice-water cooler), and for 1.6 to 2.5 h in the sun and shade cases.
- Leaf surface decay and mould need sustained wetness over days, not hours. So within an event the wrap does not rot.
- A wrapped pop kept wet in a closed box after an event would rot. The rule is to dry the wrap and eat the same day.

## Decisions

1. **Time limit after thaw.** The drink is eaten within 2 hours of leaving the freezer, and within about 1 hour in full sun. This is the Thai 2-hour limit in practice, and the screen shows it is well inside the spoilage time.
2. **Do not refreeze.** A refrozen and thawed drink adds a second growth period and damages quality. This is a rule, not a screen result.
3. **Keep the wrap dry and out of standing water.** Outside water that wicks into a damaged path raises the start load by about 100 times and cuts the time to spoilage by about 40 %. This ties the spoilage screen to the wicking screen.
4. **Do not store the wrapped pop in a closed, wet box after an event.** Dry it and eat it the same day.

## Limits

- **Pathogens are not modelled.** The screen covers spoilage organisms only. Pathogen growth after temperature abuse, including toxin-forming bacteria, needs a separate assessment. The Thai 2-hour and 5 °C rules are the operative safeguard for that.
- **Start loads are assumed.** A measured microbial load for the actual drink would change the result. No measurement is in scope.
- **Lag phase is ignored.** This makes the screen conservative for spoilage.
- **Generic growth parameters.** The actual drink's pH, water activity and preservative system (none assumed) would shift the rates.
