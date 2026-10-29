# Goldberg, Kishore, Lennen 2002: citrate ionization, selected values (Table 7.22)

- URL: https://srd.nist.gov/jpcrdreprint/1.1416902.pdf (NIST-hosted reprint)
- Citation: R. N. Goldberg, N. Kishore, R. M. Lennen, "Thermodynamic Quantities for the Ionization Reactions of Buffers", J. Phys. Chem. Ref. Data 31(2), 231-370 (2002), doi 10.1063/1.1416902
- Date read: 20 October 2026. Route: WebFetch saved the PDF; the text layer was extracted with pypdf and the Table 7.22 (Citrate) lines read directly.
- Tier: P (peer-reviewed critical evaluation, NIST reprint, table read in the text layer).
- Status: SOURCED.

## Selected values at 298.15 K and zero ionic strength (as printed)

| Step | pK | DrG (kJ/mol) | DrH (kJ/mol) | DrCp (J/K/mol) |
|---|---|---|---|---|
| (1) H3L -> H2L- + H+ | 3.128 | 17.855 | 4.07 | -131 |
| (2) H2L- -> HL2- + H+ | 4.761 | 27.176 | 2.23 | -178 |
| (3) HL2- -> L3- + H+ | 6.396 | 36.509 | -3.38 | -254 |

## Literature pK1 versus temperature, Bates and Pinching 1949 (49BAT/PIN row of the review, I = 0)

278.15 K 3.200; 283.15 K 3.176; 288.15 K 3.160; 293.15 K 3.142; 298.15 K 3.128; 303.15 K 3.116; 308.15 K 3.109; 313.15 K 3.099; 318.15 K 3.097; 323.15 K 3.095.

## Limits
- Values are for zero ionic strength; the beverage has an ionic strength of about 0.03 mol/L (computed in cube_chemistry_taste.py), so the model applies an extended Debye-Huckel (Davies) correction.
- Table text was read from a PDF text layer with ligature and sign-glyph noise ("21" for minus); signs were checked against the pK1 versus T rows above (pK1 falls as T rises, consistent with a positive DrH).
