# NSO Health Behaviour of Population Survey 2021, Table 2 (statistics and CV), sweet-tasting packaged beverages eaten or drunk 5 or more days a week, by sex and age

- Source: the uploaded NSO report SD10_04_114 (222 PDF pages), PDF page 31, printed page 12, Table 2 ("Estimated statistic and percent coefficient of variation of the estimated total", our translation). Read in the saved text-layer extract `rework/raw/nso2021_SD10_04_114_extract.md` (pdfplumber, 19 October 2026), lines 258 to 290.
- Date read: 20 October 2026.
- Tier: P (National Statistical Office, 2021 fieldwork). Status: SOURCED from the saved extract. The printed page image was not re-checked in T15 (the PDF is not on this machine; only the text-layer extract is).
- Table scope (our translation of the Thai heading): population aged 6 and over who eat the high-fat food group, the semi-prepared food group and the sweet-tasting packaged-beverage group that carry a high risk of non-communicable disease (5 or more days a week), by region, sex and age group. The third value pair in each row is the sweet-tasting packaged-beverage group (Thai column heading, spacing damaged in the text layer: "การทานกลุ่มเครื่องดื่มบรรจุภัณฑ์ที่มีรสหวานมีความเสี่ยงสูง").
- Each row prints three pairs: estimate (percent) and CV (percent of the estimated total), for high-fat food, semi-prepared food and sweet-tasting packaged beverages.

## Rows as printed (sweet-tasting packaged beverages pair only)

| Row | Estimate, percent | CV, percent |
|---|---|---|
| Whole kingdom | 18.9 | 0.74 |
| Men | 23.3 | 0.92 |
| Women | 14.7 | 1.23 |
| Age 6-14 | 15.4 | 2.32 |
| Age 15-24 | 19.0 | 2.84 |
| Age 25-44 | 24.1 | 1.26 |
| Age 45-59 | 20.4 | 1.28 |
| Age 60 and over | 11.2 | 2.14 |

(Full printed row for men: "ชาย 16.5 1.26 1.6 4.18 23.3 0.92"; women: "หญิง 15.8 1.26 1.1 5.03 14.7 1.23".)

## Consistency check against Table 20 (same report, printed p. 41)

Table 20 prints the bottled non-alcoholic drink frequency by age. Adding "5-6 days a week" and "every day":

- Whole kingdom: 4.6 + 14.3 = 18.9 (matches the Table 2 value 18.9).
- Age 25-44: 5.8 + 18.2 = 24.0 (Table 2: 24.1; rounding).
- Age 45-59: 4.4 + 16.0 = 20.4 (matches 20.4).

So the Table 2 sweet-beverage column is the Table 20 "5 or more days a week" share, and the sex rows belong to the same measure. Table 20 itself has no sex split.

## Derived relative factors used in rework/screen/ambient_variation.py (DERIVED)

- Men's factor = 23.3 / 18.9 = 1.2328; women's factor = 14.7 / 18.9 = 0.7778 (all ages 6 and over, 5 or more days a week).
- Applied as a relative factor to the everyday band shares (18.2 for 25-44, 16.0 for 45-59). This assumes the same sex ratio at ages 25 to 59, at every-day frequency, and no sex-by-age interaction. The men's factor is drawn uniform 1.10 to 1.35 (range is an ASSUMPTION). The women's factor is set so that each band's both-sex share is unchanged.
- Cross-reference: rework/47 section 2 records, from a workflow journal that is not saved in the repo (UNVERIFIED), daily sugar-sweetened consumption of 20.6 percent for men and 12.5 percent for women aged 25 to 59, which is 1.245 and 0.755 of their mean of 16.55. It points the same way and sits inside the drawn range.

## Limits

- Definition differs from the base shares (5 or more days a week versus every day); the age range of the sex split is 6 and over.
- The CV printed is for the estimated total count, not for the percentage.
