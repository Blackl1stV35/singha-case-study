> **SUPERSEDED (20 October 2026, second verification pass).** Use `guidechem_rows_read_2026-10-20.md`, which lists the rows actually used by `rework/screen/spec_revalidation.py` and the selection rule. This older note used a different row selection (for citric acid, rows labelled anhydrous; the headline now uses the 15 rows labelled food grade). The figures in this older note are not inputs to any number in the record.

# Food-grade ingredient price indications, China ex-works (rows read 20 October 2026, re-read and saved row by row after verification)

Source: GuideTrends price pages (Guidechem), https://www.guidechem.com/price/en/<CAS>.html . Tier S (a price aggregator: asking or ex-works indications, not a transaction record, not Thai landed cost). All prices CNY per tonne unless a row says CNY/kg. Read 20 October 2026 through WebFetch (a model-made extraction of the page tables; cell values are as the extraction printed them, and the pages do not always map a value to one day). The rows below are the ones that feed `rework/screen/spec_revalidation.py` (block I); nothing outside this file is used as a price.

Selection rule. Use only rows whose printed label matches the ingredient and form. A row whose label does not say food grade (or anhydrous) is kept apart as a labelled sensitivity and is not mixed into low, central and high.

## Potassium bicarbonate, CAS 298-14-6 (page "Updated: 2026-10-18")

Daily table (16 to 18 October 2026) and monthly table (Aug, Sep, Oct 2026), rows as printed:

| Label as printed | Food grade stated? | 16 Oct 2026 | Oct 2026 (month) |
|---|---|---|---|
| Zhejiang Dayang Food Grade, 99% Content (East China) | yes | 7,900 | 7,900 to 8,000 |
| Locally Made Food Grade, 99% Content (Other) | yes | (weekly 9,800) | 9,800 |
| Shanxi 99% Content (North China) | not stated | 5,500 | 5,500 to 5,950 |
| Shanxi Wentong Industrial Grade Content: 99% | no (industrial) | 5,600 | 5,600 |
| Shanxi Wencheng Chemical Co., Ltd. 99% Content | not stated | (5,400, weeks 40 to 41) | 5,400 |

Inputs used: low 7,900 and central 7,900 (Zhejiang Dayang, the named producer row), high 9,800 (Locally Made Food Grade). Sensitivity, grade not stated: 5,500 (Shanxi 99%). The earlier saved note quoted 5,500 as the "low" of a food-grade range; that row carries no food-grade label and is now a sensitivity only.

## Citric acid, CAS 77-92-9 (page "Updated: 2026-10-19")

Monthly table, October 2026 column, rows labelled anhydrous (form as printed in the label):

| Label as printed | Form | Oct 2026 |
|---|---|---|
| Shandong Yingxuan Anhydrous, 99.5% | anhydrous | 5,200 to 6,200 |
| Shijian Chemical Anhydrous Citric Acid, Food Grade | anhydrous, food grade | 7,000 |
| Locally Made Anhydrous, 99.5% | anhydrous | 6,000 |
| Locally Made anhydrous citric acid | anhydrous | 5,000 to 6,600 |

Rows with no form stated, for comparison: Shandong Food Grade 99%, 25 kg, 6,500 (Aug, Sep and Oct 2026, steady); Shandong 99.5 to 100.5%, 6,200; Locally Made Food Grade, 6,500. Monohydrate rows: Shijian Chemical Citric Acid Monohydrate, Food Grade, 6,300; Shandong Citric Acid Monohydrate 99.8%, 3,900 to 6,650.

Inputs used: low 5,000 (lowest end of the anhydrous-labelled rows), central 5,900 (median of the four row midpoints 5,700, 7,000, 6,000 and 5,800), high 7,000 (Shijian, the only row labelled both anhydrous and food grade). Sensitivity, form not stated: 6,500. The earlier saved note used 6,500 as the central price of "anhydrous" citric acid; that row has no anhydrous label.

## Sucralose, CAS 56038-13-2 (page "Updated: 2026-10-10")

| Label as printed | Purity | Daily (14 to 16 Oct), weekly (weeks 40 to 42) and monthly (Aug to Oct 2026) |
|---|---|---|
| Sucralose (Jiangsu Xin Su 99%), East China | 99% | 105,000 in every period |
| Sucralose (Senfida 98%), Other | 98% | 360,000 in every period |

Page headline: current 105,000, 3-month average 105,000, one-year level "Low". Inputs used: low and central 105,000, high 360,000.

## Maltodextrin, CAS 9050-36-6 (page "Updated: 2026-06-03"; older than the other pages, so a dated figure)

Weekly table, weeks 21 to 23 of 2026, rows as printed (monthly April to June 2026 shows the same series):

| Label as printed | Food grade stated? | Weeks 21 / 22 / 23 |
|---|---|---|
| Shandong Xiwang Food Grade, content 99% | yes | - / 3,500 / - (May 3,500 to 3,600) |
| Henan Food-Grade | yes | 4,300 / 4,300 / 4,300 |
| Locally Made 99% | not stated | 3,500 each week |
| Locally Made 99.9% | not stated | - / 3,600 / - |
| Locally Made DE value 10-15, content 99% | not stated | 2,850 each week |
| Locally Made DE value 10-15 | not stated | 4,500 each week |
| Shandong Xiwang 25 kg bag, 99.9% | not stated | 3,100 to 3,300 / 3,100 to 3,300 / 3,100 |
| Shandong Xiwang Solid | not stated | 4,000 to 4,300 / 4,300 / 4,300 |
| Hubei Industrial Grade | no (industrial) | 2,500 |

Inputs used: low 3,500, high 4,300, central 3,900 (the midpoint of the two food-grade-labelled rows; an ASSUMPTION, not a printed value). Sensitivity, grade not stated: 2,850 (Locally Made DE 10-15, 99%). The binder is not named in the design, so maltodextrin and mannitol are stand-ins (PROXY) for its price.

## Mannitol, CAS 69-65-8 (page "Updated: 2026-10-15")

One row, "Hubei July, August, and September 99% Content": 28 CNY/kg (28,000 CNY/t) in the daily (13 to 15 October), weekly (weeks 40 to 42) and monthly (Aug to Oct 2026) tables. Packaging and supplier are not stated.

## Not reached

- Lemon flavour: no price source reachable. The shared web search allowance for this run was used up before a flavour listing could be searched; flavour stays an ASSUMPTION range (THB 300, 800 and 1,500 per kg) and is flagged as a limit.
- Thai domestic or landed prices (distributor price lists, import unit values): not reached in this run for the same reason. Landed cost, duty and handling are not in the re-price (limit).
