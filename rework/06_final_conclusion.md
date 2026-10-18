# Innovative Bev & Bite: team conclusion (18 October 2026)

Status: team conclusion. All evidence is virtual: no physical, taste or consumer test is in scope. Submission-facing text is held separately and is pended (see rework/27).

## Decisions

- **Primary concept:** a leaf-wrapped frozen coconut-pandan drink with a food-grade inner barrier, under Alternative Formats. The inner barrier is the working design, confirmed by the user on 18 October (rework/30, rework/31). The barrier is PET. The consumer peels the leaf and sips as it thaws.
- **Claim:** "leaf-wrapped". Not "plastic-free".
- **Novelty claim:** a leaf-wrapped frozen drink. No such drink was found in the extended search. A leaf-wrapped frozen ice-cream bar in Ratchaburi is a disclosed precedent: one 2023 user post shows it; its sale and frozen status are unconfirmed (rework/25).
- **Leaf-only (no barrier):** rejected on physical grounds. Freeze damage gives about one leaking path per wrap at a damaged fraction of about 10^-7, and open stomata wick the wrap in minutes (rework/30).
- **Hot-season use:** keep in an insulated box with gel packs, keep out of ice water, and eat within about an hour in full sun. These go in the product instructions. They go on the label only after a Thai registration check.
- **Holding rule:** the product is treated as a non-heat ready-to-eat beverage (working assumption, pending registration check). Thai food-premises rules then require below 5 °C, or no more than 2 hours at room temperature.
- **After thaw:** eat within 2 hours of leaving the freezer, and within about an hour in full sun. Do not refreeze. Keep the wrap dry and out of standing water. Spoilage screen: rework/28.
- **Ranking:** A (above) is primary. B (midlife isoflavone soy drink) is second-ranked and conditional on a regulator's written confirmation. C (the reframed non-alcoholic Thai-herb drink) is dropped, because its viability and unit cost are both open.

## Virtual evidence

| Question | Result | Basis |
|---|---|---|
| Novelty | no leaf-wrapped frozen drink found; one unconfirmed leaf-wrapped ice-cream bar | extended search: about 137 queries, 11 languages, patents (Google Patents only), OTOP, Thai retail (partly blocked) |
| Thaw, lab (30 °C still air) | surface melts at 13 min; half thawed at 1.5 h; fully thawed at 3.3 h | radial thermal model (rework/17) |
| Thaw, street stall in sun | half thawed at about 38 min (0.63 h); whole pop above 5 °C at about 1.5 h | Thai screen, sourced Bangkok inputs (rework/22) |
| Thaw, street stall in shade | half thawed at about 50 min (0.84 h); above 5 °C at about 2.0 h | same |
| Thaw, insulated cooler with gel packs (festival) | surface melts at about 1.6 h; half thawed at about 3.2 h | summer screen (rework/24) |
| Leak, drink side (sealed edges) | damaged-path threshold, Monte Carlo over 1 to 3 mPa s: median 0.24 µm, 5 to 95 % range 0.14 to 0.45 µm. Lower-viscosity case in the summer screen: 0.16 to 0.17 µm. Exposed edges leak in all runs. Damage size is unmeasured | leak screen (rework/16, rework/17) and summer screen |
| Leak, outside water | only damaged paths wick: intact wax (about 130 degrees) does not, damaged exposed cell wall (76 degrees) does. Dew film reaches its 90 µm cap in about 6 to 22 min in Bangkok humidity. No margin where the film reaches the top of the wrap | physics assumptions (rework/22, section 7) and summer screen |
| Quantum runs | method check only. Hardware noise dominates the deeper circuits, so no precision gain is claimed | rework/18, rework/20, rework/21 |
| Thai holding and ice rules | non-heat ready-to-eat beverages: below 5 °C, or 2 hours at room temperature in food premises. No Thai rule for processed frozen products. Ice notification 463 in force, no drink wording | Thai gazette and FDA texts (rework/22, section 3) |

## Physics assumptions set in place of the open gaps (rework/22, section 7)

- **Pandan leaf optics:** the same as banana, plus or minus 20 %.
- **Leaf cuticle roughness:** 0.3 (range 0.2 to 0.4), from the waxy cuticle's micro-scale structure.
- **Outside-water wetting:** capillary climb needs cos theta above zero. Intact wax does not wick, and the damaged paths do.
- **Splash and open-water temperature:** 29.3 °C, within the range that open water reaches under daytime air with evaporative cooling.
- **Frozen storage target:** −18 °C, because most of the water is ice at that temperature.
- **Time out of freezer:** governed by the thaw screen, with the Thai 2-hour rule as the legal limit for sale.

## Limits that remain

- No physical leak, taste or consumer test is in scope. Every leak and taste figure is virtual.
- The damaged-path size is not measured. The screens report thresholds, not probabilities.
- The leaf in the render is a generic photo, not confirmed as banana or pandan.
- Whether the product is legally a beverage or an ice cream is a registration question. The screen uses the stricter beverage rule.
- Spoilage (about 6 to 12 h at 30 C for a sealed drink) and pathogens (about 6 to 27 h from one contaminating cell at 30 C) are screened with generic parameters (rework/28, rework/29). The start load decides the risk, so a validated kill step or pathogen-free raw material is a production requirement.
