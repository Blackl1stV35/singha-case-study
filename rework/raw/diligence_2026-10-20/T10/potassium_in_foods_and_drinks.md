# Potassium in comparison foods and drinks, saved extracts (T10)

Date read: 20 October 2026. The Thai Food Composition Database (Institute of Nutrition, Mahidol University, https://inmu.mahidol.ac.th/thaifcd/) is a search form on a site with sign-in links; the pages opened showed the search form only (food group Q is non-alcoholic beverages, E fruits), and a form submission is not allowed in this task. No Thai FCD value was read.

## USDA values (now primary)
Items 1 to 3 of the earlier version of this file were secondary copies of USDA entries taken from Wikipedia tables. They are replaced by the USDA FoodData Central values read through the official API on 20 October 2026 (tier P): see `usda_fdc_api_potassium_2026-10-20.md`.
- Coconut water, FDC 170174: 250 mg per 100 g (cup of 240 g). Earlier Wikipedia value agreed.
- Orange juice, FDC 169098: 200 mg per 100 g; one cup is 248 g, so 496 mg per cup. The earlier note "496 mg per 250 mL" was the cup value with a wrong volume; USDA's basis is mass.
- Banana: FDC 173944 (SR Legacy, "Bananas, raw") 358 mg per 100 g; FDC 1105314 (Foundation, "Bananas, ripe and slightly ripe, raw") 326 mg per 100 g. The earlier note attached 358 mg to 1105314 in error.
- Lemon-lime soda, FDC 173206 (Sprite, SR Legacy): 1.00 mg per 100 g; 12 fl oz is 369 g.

## Other items (unchanged)
4. Sports drink powder, maker label. Gatorade Thirst Quencher single-serve packet (orange), maker page https://www.gatorade.com/powders/gatorade-thirst-quencher/orange-single-serve-sticks-00052000047011 : "70mg of potassium per serving" and 230 mg sodium; one packet makes 15 to 20 oz (the FAQ says mix with 16.9 fl oz, 500 mL, of water). Tier P for the maker's label of that product; Thai bottled sports drinks were not read. Pocari Sweat Thailand page (https://www.pocarisweat.co.th/): names potassium among electrolytes but gives no amounts, so nothing is used.
5. WHO reduced-osmolarity oral rehydration salts: potassium 20 mmol/L (acceptable range 15 to 25), potassium chloride 1.5 g/L. Wikipedia "Oral rehydration therapy", citing WHO/UNICEF "Oral rehydration salts: production of the new ORS" (WHO/FCH/CAH/06.1, 2006). Page: https://en.wikipedia.org/wiki/Oral_rehydration_therapy . Tier S (the WHO document itself was not opened).
6. Sports drink sodium, for context only: Wikipedia "Sports drink" cites Rosner 2019 for sodium 20 to 30 mEq/L; no potassium figure on the page.

## Not read (stated limit)
Any Thai bottled sports drink or Thai coconut water label; any Thai Food Composition Database value; the potassium content of soft drinks other than the one USDA entry above.

## Arithmetic used (see screen/t10_potassium_cover_results.json)
- Cube serve: 316.6 mg potassium in 330 mL = 0.959 mg/mL = 24.5 mmol/L (using atomic mass 39.098).
- Densities for the 330 mL comparisons come from USDA's own portion weights (coconut water 1.0144, orange juice 1.0482, lemon-lime soda 1.0398 g/mL; US customary cup and fluid ounce taken as 236.588 mL and 29.5735 mL, our assumption about USDA's units). At 1.0 g/mL the values are 825, 660 and 3.3 mg per 330 mL.
