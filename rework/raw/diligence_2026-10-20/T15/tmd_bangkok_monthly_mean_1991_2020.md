# TMD climatological data, Bangkok Metropolis (station 48455), 1991 to 2020

- Source: Thai Meteorological Department, "Climatological Data of Thailand for 30 Year Period (1991-2020)", Meteorological Data report No. 551.586-13-2023.
- URL fetched: https://ubonmet.tmd.go.th/files/MetInfo/climate_normal.pdf (WebFetch, 20 October 2026; the binary PDF was saved to the session scratch folder and read as images and as text with PyMuPDF; the copy is not in the repo).
- Date read: 20 October 2026.
- Tier: P (Thai Meteorological Department, climate normals).
- Page: PDF page 57 of 96 (station table, "CLIMATOLOGICAL DATA FOR THE PERIOD 1991-2020", station BANGKOK METROPOLIS, index station 48455).

## Extracted rows (Temperature, Celsius, as printed; the text layer lists 12 monthly values then the annual value)

| Row | JAN | FEB | MAR | APR | MAY | JUN | JUL | AUG | SEP | OCT | NOV | DEC | ANNUAL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mean | 27.4 | 28.6 | 29.7 | 30.7 | 30.3 | 29.7 | 29.2 | 29.0 | 28.6 | 28.4 | 28.4 | 27.3 | 28.9 |
| Mean max. | 32.7 | 33.7 | 34.7 | 35.7 | 35.1 | 34.1 | 33.5 | 33.3 | 33.2 | 33.0 | 33.1 | 32.3 | 33.7 |
| Mean min. | 23.4 | 24.8 | 26.4 | 27.2 | 26.9 | 26.4 | 26.1 | 25.9 | 25.4 | 25.2 | 24.7 | 23.2 | 25.5 |

Column assignment follows the printed order (JAN to DEC, then ANNUAL). The April mean max of 35.7 agrees with the value already in rework/22 (TMD 48455, 1991 to 2020).

## Use in this study

The monthly means (27.3 to 30.7 C; annual 28.9 C) drive the ambient-temperature factor in rework/screen/ambient_variation.py. The mapping from temperature to soft-drink or beer demand is not in this source, so the sensitivity to temperature is an ASSUMPTION range (see rework/78).
