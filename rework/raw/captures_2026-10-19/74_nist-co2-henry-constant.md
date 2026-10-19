# Capture 74: NIST WebBook, carbon dioxide (CAS 124-38-9), Henry's law solubility data

- URL: https://webbook.nist.gov/cgi/cbook.cgi?ID=C124389&Units=SI&Mask=10#Solubility
- Date read: 19 October 2026
- Access route: WebFetch (model-extracted text of the page, not a verbatim copy)
- Tier: P. NIST is a government reference database. The rows themselves carry no citations (see below).
- Status: SOURCED. The Henry's law table was visible.

## Extracted facts

- Solvent: water. Column header as shown: "Henry's Law constant (water solution)".
- Reference temperature for k(H) degrees: 298.15 K.
- Units: k(H) degrees in mol/(kg bar). Temperature constant is labelled d(ln kH)/d(1/T), unit K.
- Temperature dependence as printed: kH(T) = k(H) degrees x exp[ d(ln kH)/d(1/T) x (1/T - 1/298.15 K) ].
- Rows: 17 in total. Values as printed:

| Row | k(H) degrees, mol/(kg bar) | d(ln kH)/d(1/T), K | Method code | Note on page |
|---|---|---|---|---|
| 1 | 0.035 | 2400 | L | none |
| 2 | 0.034 | 2600 | Q | only data 273-303 K used; fit poor above 303 K; citation missing |
| 3 | 0.045 | blank | Q | several references not assigned to species; citation missing |
| 4 | 0.035 | 2300 | L | none |
| 5 | 0.034 | 2400 | C | none |
| 6 | 0.034 | 2400 | C | none |
| 7 | 0.034 | 2400 | C | none |
| 8 | 0.031 | 2400 | T | none |
| 9 | 0.034 | 2400 | Q | several references not assigned to species; citation missing |
| 10 | 0.034 | blank | N/A | none |
| 11 | 0.034 | blank | C | none |
| 12 | 0.032 | 2400 | X | none |
| 13 | 0.035 | 2400 | L | none |
| 14 | 0.034 | 2400 | L | none |
| 15 | 0.034 | 2400 | X | value from an unpublished compilation by W. Asman |
| 16 | 0.034 | 2700 | X | value from an unpublished compilation by W. Asman |
| 17 | 0.034 | 2400 | N/A | none |

- References: the Reference column reads N/A for every row. The References section says "No reference data available." The data compilation is credited to Rolf Sander. Rows 2, 3 and 9 carry the page comment "missing citation." Authors, year and journal are not given for any row.
- Method codes L, Q, C, T and X link to a legend. The legend text was not in the extracted content, so the codes are not defined here.
- Row used for water at 298 K: the page marks no row as the typical value. The k(H) degrees column is defined at 298.15 K, but no single row is designated. This capture does not select one.

## Could not read

- The method-code legend (linked, not extracted).
- Any citation for the rows.
- Per-row temperatures, except the 273-303 K range for row 2.
- The "Mask=10" anchor label. The extraction did not show a label for the Solubility section, although the table content was visible.

## Limits

- WebFetch returns a model-generated extraction. The table above was transcribed from that extraction. Check it against the live page before a record cites any row.
