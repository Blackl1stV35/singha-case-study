# Definition of "volumes of CO2" (read 20 October 2026)

1. University of Florida IFAS Extension FS379, "A Guide to Carbonating Beverages at Small Scale" (Song, Wendrick, Sims, MacIntosh; (c) 2024 University of Florida; no publication date shown).
   URL: https://ask.ifas.ufl.edu/publication/FS379 . Tier S (university extension guide).
   Quoted: "volumes of CO2 (STP) per volume of liquid (vol/vol)"; "The exact conversion is 1 vol/vol = 1.96 g/L"; Table 2 reports "Vol/Vol at 0 C [32 F]". The guide never spells out STP.
   Check (ours): 44.01 g/mol / 22.414 L/mol = 1.963 g/L, so 1.96 g/L is the 0 C, 1 atm basis. On a 15.56 C basis the factor would be 1.858 g/L.
2. US Patent 4,636,337 (published 13 January 1987), https://patents.google.com/patent/US4636337 . Tier S (patent description, not a standard).
   Quoted: volume "is defined as the amount of gas in milliliters that a given volume of water will absorb at atmospheric pressure (760 mm. of mercury) and 60 F. (15.5 C.)".
Conclusion: two conventions are in use (0 C and 60 F). The 1.96 g/L conversion used in a current university guide is the 0 C convention. A source that is a standards body definition was not found (limit).

## Second verification pass (20 October 2026): the 60 F basis computed
- On the 60 F (15.56 C) convention of US 4,636,337 the molar volume at 1 atm is 23.690 L/mol and the same 8.098 mmol dose reads 0.581 volume per 330 mL (`spec_revalidation_results.json`, results.co2_volume.by_temperature.60F_15p56C). The slide basis stays 0 C and 1 atm (0.550). Both conventions are stated in `rework/72_spec_revalidation.md` section 2.
