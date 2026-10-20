# TMD climate normals, Bangkok Metropolis, re-read from the source PDF

- Item: V5 revision. Date read: 20 October 2026.
- Why: the first V5 record said the Bangkok monthly means were "carried from" the T15 note and "read again", but the first pass read only that note. This pass re-read the source.
- Source: Thai Meteorological Department, "Climatological Data of Thailand for 30 Year Period (1991-2020)". URL https://ubonmet.tmd.go.th/files/MetInfo/climate_normal.pdf (WebFetch returned the binary, which the tool saved to the session folder; it was copied to its own scratch folder and its text layer read locally with PyMuPDF, python -I). The PDF has 96 pages.
- Page: PDF page 57, headed "CLIMATOLOGICAL DATA FOR THE PERIOD 1991-2020", station BANGKOK METROPOLIS, index station 48455, elevation 3 m, 13 43 N, 100 33 E. The column header on the page reads JAN to DEC and ANNUAL.

## Temperature (Celsius), as printed

| Row | JAN | FEB | MAR | APR | MAY | JUN | JUL | AUG | SEP | OCT | NOV | DEC | ANNUAL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mean | 27.4 | 28.6 | 29.7 | 30.7 | 30.3 | 29.7 | 29.2 | 29.0 | 28.6 | 28.4 | 28.4 | 27.3 | 28.9 |
| Mean max. | 32.7 | 33.7 | 34.7 | 35.7 | 35.1 | 34.1 | 33.5 | 33.3 | 33.2 | 33.0 | 33.1 | 32.3 | 33.7 |
| Mean min. | 23.4 | 24.8 | 26.4 | 27.2 | 26.9 | 26.4 | 26.1 | 25.9 | 25.4 | 25.2 | 24.7 | 23.2 | 25.5 |

- The mean row matches the values used by rework/screen/ambient_variation.py (TMD list) and the T15 note, value for value.
- Tier P (Thai Meteorological Department climate normals, page read). Status SOURCED. Station: Bangkok Metropolis only; it is not a national mean.
