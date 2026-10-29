# Physical constants read from Wikipedia pages (secondary, S)

- Date read: 20 October 2026 for every row. Route: WebFetch (model-summarised; numbers as printed on the pages). Tier: S (encyclopedia; handbook values reproduced, handbooks not opened). Status: SOURCED, secondary.

## Citric acid, https://en.wikipedia.org/wiki/Citric_acid (first 100,000 of 119,196 characters read)
- Density 1.665 g/cm3 (anhydrous). Molar mass 192.123 g/mol (anhydrous), 210.14 (monohydrate).
- Solubility in water, percent w/w: 10 C 54; 20 C 59.2; 30 C 64.3; 40 C 68.6; 50 C 70.9; 60 C 73.5. (Used only in the composition-weighted Cs variants of the dissolution model, converted to about 751 g/L at 20 C with the specific gravity page.)
- pKa1 3.13, pKa2 4.76, pKa3 6.39 and also printed 6.40.

## Potassium bicarbonate, https://en.wikipedia.org/wiki/Potassium_bicarbonate
- Density 2.17 g/cm3. Solubility 22.4 g/100 mL at 20 C. Molar mass 100.115 g/mol. Decomposes between 100 and 120 C. pKa 6.351 (carbonic acid) and 10.329 (bicarbonate).
- A possible handbook conflict (a different solubility per 100 g of water at 20 C) was recalled and NOT opened; it is not used and not resolved. The dissolution model applies this 22.4 g/100 mL (224 g/L) to the WHOLE cube mass (conservative, as KHCO3 is the least soluble reactant read). The tornado in cube_chemistry_dissolution.py varies it by x0.7 and x1.5 and tests two composition-weighted values (517 and 601 g/L, from the citric acid solubility below and the specific gravity page corechem_citric_acid_solution_specific_gravity.md). An earlier version of this page said that the model already varied the solubility; it did not, and that sentence was wrong (corrected 2026-10-20 after the verifier review).

## Carbonic acid, https://en.wikipedia.org/wiki/Carbonic_acid (no citation printed for the rates)
- Uncatalysed hydration CO2 + H2O to H2CO3 at 25 C: 0.039 per second. Dehydration H2CO3 to CO2 + H2O at 25 C: 23 per second. [H2CO3]/[CO2] about 1.7e-3 in pure water at 25 C.

## Sucralose, https://en.wikipedia.org/wiki/Sucralose
- Density 1.69 g/cm3. Solubility in water 283 g/L at 20 C. Molar mass 397.63 g/mol. "About 600 times sweeter than sucrose".

## Water (data page), https://en.wikipedia.org/wiki/Water_(data_page)
- Dynamic viscosity (mPa s) and density (g/cm3): 0 C 1.7921, 0.9998395; 5 C 1.5188, 0.99996 (re-read, see wikipedia_water_data_page_reread_5C.md); 10 C 1.3077, 0.9997026; 15 C 1.1404, 0.9991026; 20 C 1.0050, 0.9982071; 25 C 0.8937, 0.9970479; 30 C 0.8007, 0.9956502; 35 C 0.7225, 0.99403.
- Surface tension 72.74 mN/m at 20 C and 71.98 mN/m at 25 C.

## Mass diffusivity, https://en.wikipedia.org/wiki/Mass_diffusivity
- Diffusion in water at 25 C, 1e-5 cm2/s: carbon dioxide 1.92; oxygen 2.10; nitrogen 1.88; methanol 0.84; ethanol 0.84; acetone 1.16. No ions, sugars or citric acid on the page.
- Temperature scaling printed: D(T1)/D(T2) = (T1/T2) (mu(T2)/mu(T1)) (Stokes-Einstein form).

## Sherwood number, https://en.wikipedia.org/wiki/Sherwood_number
- Ranz-Marshall for spheres: Sh = 2.0 + 0.6 Re^(1/2) Sc^(1/3), 0 <= Re < 200 and 0 <= Sc < 250 (as printed). Froessling: Sh = 2 + 0.552 Re^(1/2) Sc^(1/3). Sh = h L / D. The page gives no natural-convection or stirred-tank correlation.

## Davies equation, https://en.wikipedia.org/wiki/Davies_equation
- -log f = 0.5 z1 z2 ( sqrt(I) / (1 + sqrt(I)) - 0.30 I ), stated for 25 C; no temperature dependence printed; about 2 % deviation for 1:1 electrolytes at 0.1 M.

## Limits
- The Sc validity range on the Ranz-Marshall row (below 250) is exceeded for citric acid (Sc about 1,500); the model uses the correlation as an extrapolation and says so.
- Natural_convection page (Wikipedia): only a gas-type vertical-plate correlation (Nu = 0.478 Gr^0.25, Pr about 0.7) was printed, which is not valid for a liquid with Sc of 1,000 or more. The solutal natural-convection estimate for a sphere uses the Steinberger and Treybal correlation from the NPTEL lecture notes instead (nptel_natural_convection_sphere_steinberger_treybal.md) and the mass-transfer Grashof form from the Wikipedia Grashof page (wikipedia_grashof_mass_transfer_form.md).
