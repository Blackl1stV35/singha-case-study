# Lime Cube: R&D handover of figures

19 October 2026. Desk figures only. No bench, sensory or consumer test has been run.

## What is handed over

The Lime Cube is a dissolvable drink cube. One cube is dissolved in one 330 mL serve to make a carbonated lime drink. One cube per pouch is inferred and not confirmed with the organiser. The composition is potassium bicarbonate, citric acid and sucralose. No sodium carbonate is used.

The recommended dose is 0.55 volume of carbon dioxide per 330 mL. The working pH anchor is 3.5, and taste at that pH is untested. Packs are cartons of 6, 12 or 24 cubes. Product classification (beverage, edible ice or electrolyte drink) is open.

Only the composition is stated as fact. No health, hydration, electrolyte, potassium-benefit, sugar, sodium or fizz-performance claim is made. International expansion is out of scope. No domestic cube-format listing was found, so overseas cube products are cited below as labelled analogues (PROXY): freeze-dried tea and coffee cubes in pouches in Japan (2021), and cube brands abroad (2018 and 2024).

## The figures per 330 mL at the recommended dose

- Carbon dioxide: 0.55 volume, about 8.1 mmol (DERIVED: 0.55 times 0.330 L, at standard molar volume).
- Potassium bicarbonate: 0.81 g (DERIVED: one mole of bicarbonate per mole of carbon dioxide).
- Citric acid: 0.52 g to neutralise the bicarbonate (DERIVED: 8.1 mmol divided by three acid protons). The total for pH 3.5 is 2.10 g, about 6.4 g per litre (DERIVED from citric and carbonic acid pKa values, S, SOURCED).
- Potassium: about 317 mg (DERIVED: 8.1 mmol at 39.1 mg per mmol). This is 9.0% of the Thai reference of 3,500 mg per day (S, SOURCED). Two secondary pages give that reference but cite different notification numbers, and the primary was not opened. The EFSA adult adequate intake is also 3,500 mg per day (P, SOURCED).
- Sucralose: 33 mg, about 100 mg per kg (DERIVED: a sweetness target of 6 g sugar per 100 mL, an ASSUMPTION, divided by 600, the low end of the reproduced 600 to 650 times sucrose range, S, SOURCED).
- Sucralose ceiling: 300 mg per kg in category 14.1.4, under condition 127, which applies to the drink as consumed (P, UNVERIFIED: the annex extract is not in the capture index). Condition TH3 applies only to electrolyte drinks. Potassium bicarbonate and citric acid are quantum satis in the same category (P, UNVERIFIED for the same reason). A Singha lemon soda company page already names sucralose (S, SOURCED).

## Serve temperature and carbon dioxide retention

Solubility is 0.592 volume at 35 C, the lowest value across the 5 to 35 C serve range (S, SOURCED; at one atmosphere). So 0.55 volume is within solubility at every modelled serve. Pack pressure is not modelled.

The desk model starts each serve at 0.55 volume and decays it exponentially (form DERIVED from the file's outputs) with an upper-bound time constant of 106 minutes. At 25 C it keeps about 0.50 volume after 10 minutes (DERIVED). The fizz threshold of 0.44 g per litre, about 0.22 volume (DERIVED), comes from a mineral-water study read as an abstract (PROXY, S, SOURCED). Time above it is about 96 minutes at every serve from 5 to 35 C (DERIVED). This is a surface-only upper bound, because the model assumes no bubble formation.

Ice lowers the starting level. With 30 g of ice the serve is about 21 C at 0.50 volume. With 60 g it is about 13 C at 0.47 volume (DERIVED).

## Cost per cube and per container

Cost per pouch before carton is THB 3.42 (DERIVED from four inputs): reactants THB 0.12, pouch THB 1.30, print THB 1.50 and processing THB 0.50. All four are ASSUMPTIONS. The pouch figure has a range of 0.67 to 2.70, and a non-Thai listing stands in for a Thai price (PROXY).

At 0.55 volume and pH 3.5, cost per cube is THB 4.09 in a 6-cube carton, THB 3.84 in a 12-cube carton and THB 3.79 in a 24-cube carton (DERIVED). The gap to THB 3.42 is THB 0.37 to 0.67 per cube. The handover file does not split that gap, and no carton price is sourced. The model's ex-factory figure of THB 9.00 per cube is a placeholder, not a proposed price (ASSUMPTION).

A 20-foot container holds about 128,580 cubes in 12-cube cartons (10,715 cartons). Volume, not weight, is the limit (DERIVED from container specification pages, S, SOURCED). This implies about 0.26 litres of container volume per cube, a packing assumption the handover file does not state. The modelled load is about 1.6 tonnes against a payload of 28.2 tonnes.

## What R&D must define

1. What retention at 25 C, after how many minutes, should the gate for 0.55 volume be? So far the desk model keeps about 0.50 volume after 10 minutes. This is a model value to test, not a gate.
2. What pH and acid level should the drink reach? So far 3.5 is a working anchor, and citric acid is about 6.4 g per litre. No lemon-lime acid level has been sourced as a number. Three retailer listings that might show one were blocked when checked.
3. What sweetness do panellists accept at 33 mg of sucralose per serve? So far the figure rests on an assumed sugar equivalence. No sensory test has run.
4. Should the pack say chilled, iced or ambient, and what serve rule should it give? So far the model covers 5 to 35 C and two ice cases. No serve rule or pack wording exists.
5. What fizz duration is acceptable, and how will it be measured? So far the threshold is a mineral-water proxy, and the 96-minute figure is an upper bound. No bench measurement exists.
6. What potassium declaration and medical wording are permissible, and who reviews the risk? So far a serve gives about 317 mg of potassium. No medical review has been done. Kidney function and potassium-sparing drugs are the risks to review first.
7. Is the product a beverage, an edible ice or an electrolyte drink, and which limits follow? So far classification is open. A Thai FDA clarification says a 14.1.4 permission extends to its sub-categories, while a sub-category permission stays there (P, SOURCED). The sub-category rows were not read. The excise item 02.02, at 14% ad valorem with per-litre rates by sugar content, comes from a desk record. Its value base is unread, and a second reader must check the Thai numerals before public use (UNVERIFIED).
8. What pouch barrier and shelf life can be supported? So far no water-vapour transmission rate has been sourced. Bangkok relative humidity of 73% (annual mean) and 79% (September) is UNVERIFIED, because the official climate table could not be read. No shelf-life test exists.
9. What are the Thai prices for pouches, print and cartons? So far every price is an assumption. No quote was requested, and R&D should obtain them through its own process.

## What is not yet known

- The model is desk-only. No bench, sensory or consumer test exists, and no consumer evidence supports the cube format or the taste.
- The time constant does not vary with serve temperature in the model, so the flat result from 5 to 35 C is a model limit, not a finding.
- Pack pressure, headspace and storage temperature are not modelled.
- Captured 25 C solubility values differ by convention (0.759 and 0.839 volume; S and P, SOURCED), so the gate must state its basis.
- The sucralose ceiling and the quantum satis rows are not yet in the capture index.

## Tier key

P: a government or regulator text read in full, a company's own filing, official statistics, a peer-reviewed article read in full, or a primary database. S: any other source, including press, trade portals, consultancy pages, company web pages that are not filings, handbooks reproduced online, and search snippets. SOURCED: the page text was captured and read; name the capture file. UNVERIFIED: not captured, blocked, unreadable, or only a snippet read. DERIVED: our arithmetic, inputs and tiers shown. PROXY: a stand-in for what is not measured. ASSUMPTION: a value chosen for the model, not sourced.

## Sources

Capture ids refer to the proposal capture index. Dates are source or read dates.

- Capture 4 (S, SOURCED), 04_co2-solubility-table-wikipedia.md. Solubility table, 0 to 35 C, read 19 Oct 2026. https://en.wikipedia.org/wiki/Carbon_dioxide_(data_page)
- Capture 15 (P, SOURCED), 15_nist-co2-ostwald-solubility.md. Ostwald coefficient, 25 C 0.839, 1991 evaluation. https://srdata.nist.gov/solubility/sol_detail.aspx?sysID=62_1
- Capture 72 (S, SOURCED), 72_bionumbers_co2_solubility_25c.md. 25 C value 0.759, basis inferred. https://bionumbers.hms.harvard.edu/bionumber.aspx?id=106207
- Capture 73 (S, SOURCED), 73_bionumbers-co2-solubility.md. 35 C value 0.592 at 1 atm. https://bionumbers.hms.harvard.edu/bionumber.aspx?id=106208
- Capture 75 (S, SOURCED), 75_crc-citric-acid-pka.md. Citric acid pKa 3.13, 4.76, 6.40 at 25 C. https://diverdi.colostate.edu/all_courses/CRC%20reference%20data/dissociation%20constants%20of%20organic%20acids%20and%20bases.pdf
- Capture 76 (S, SOURCED), 76_crc-carbonic-acid-pkw.md. Carbonic acid pKa 6.35 and 10.33 at 25 C. https://diverdi.colostate.edu/all_courses/CRC%20reference%20data/dissociation%20constants%20of%20inorganic%20acids%20and%20bases.pdf
- Capture 77 (S, SOURCED), 77_wur-sparkling-threshold-abstract.md. Abstract only, 2021; threshold 0.44 g per litre. https://research.wur.nl/en/publications/is-it-still-water-relationships-between-sparkling-sensitivity-and/
- Capture 63 (S, SOURCED), 63_jecfa-tgs-sweetness.md. Sucralose 600 to 650 times sucrose, reproduced monograph. http://www.inchem.org/documents/jecfa/jecmono/v28je14.htm
- Capture 66 (P, SOURCED), 66_thai_fda_468_subcat_rule.md. Thai FDA clarification of notification 468, sub-category rule, in force 12 December B.E. 2568. https://food.fda.moph.go.th/media.php?id=849894195891150848&name=468_FoodAdditives.pdf
- Annex extract (P, UNVERIFIED for the capture index; no capture id). Category 14.1 rows for sucralose, potassium bicarbonate and citric acid, read 19 Oct 2026. File moph_468_annex_flavoured_drinks_extract_2026-10-19.md. https://food.fda.moph.go.th/media.php?id=840096266338836480&name=P468.pdf
- Capture 80 (P, UNVERIFIED), 80_moph-p468-url-check.md. Annex PDF exceeded the 10 MB read limit; no content read. Same URL as the extract.
- Capture 67 (S, SOURCED), 67_thai_rdi_potassium_secondary.md. Thai reference 3,500 mg per day; cites notification 182 (B.E. 2541). https://www.lovefitt.com/system/wp-content/uploads/2017/05/4-4-2ThaiRDI.pdf
- Capture 78 (S, SOURCED), 78_thai-fda-potassium-rdi.md. Thai reference 3,500 mg per day; cites Announcement No. 445. https://www.siamdevelopment.com/thai-fda-rdi-nutrition-standards-in-thailand/
- Capture 69 (P, SOURCED), 69_efsa_2016_potassium_ai.md. EFSA adult adequate intake 3,500 mg per day, 25 Oct 2016. https://www.efsa.europa.eu/en/press/news/161025
- Capture 48 (S, SOURCED), 48_singha-lemon-soda-th.md. Singha Lemon Soda, sucralose named. https://www.singhacorporation.com/singhalemonsoda/th/
- Capture 21 (S, SOURCED; PROXY), 21_beveragedaily-coke-japan-cubes.md. Freeze-dried cubes in pouches, Japan, 17 Jun 2021. https://www.beveragedaily.com/Article/2021/06/17/Drop-it-then-its-hot-Coca-Cola-Japan-creates-freeze-dried-tea-and-coffee-cubes-to-reduce-packaging-waste
- Capture 28 (S, SOURCED; PROXY), 28_santo-cubes-foodnavigator-2018.md. Coffee cube format, 11 Oct 2018. https://www.foodnavigator.com/Article/2018/10/11/Santo-Cubes-aims-to-update-instant-coffee-set-with-launch-of-coffee-cubes
- Capture 29 (S, SOURCED; PROXY), 29_waterdrop-foodnavigator-2024.md. Drink cube brand, 3 Oct 2024. https://www.foodnavigator.com/Article/2024/10/03/Beverage-cubes-Innovations-from-entrepreneurs-waterdrop-and-more/
- Captures 57, 58 and 59 (index tier P; S here, as company web pages that are not filings), 57_one-dry-containers.md, 58_seacube-20ft-dry.md, 59_seacube-40ft-dry.md. Internal dimensions, payload and cubic capacity, read 19 Oct 2026. https://www.one-line.com/en/dry-containers ; https://seacubecontainers.com/product_specs/20-foot-dry/ ; https://seacubecontainers.com/product_specs/40-foot-standard-dry/
- Capture 45 (P, UNVERIFIED), 45_gazette-sugar-drink-excise-403.md. Gazette PDF blocked (HTTP 403). https://www.ratchakitcha.soc.go.th/DATA/PDF/2560/A/095/111.PDF
- Capture 17 (P, UNVERIFIED), 17_tmd-bangkok-climate-normals-pdf.md. Climate PDF unreadable; humidity not captured. https://ubonmet.tmd.go.th/files/MetInfo/climate_normal.pdf
- Captures 51, 52 and 53 (S, UNVERIFIED, blocked; not used): 51_tops-chamm-roselle-herbal-drink.md, 52_tops-schweppes-soda-water.md, 53_tops-sprite-zero-sugar-lemon-lime.md.
- Capture 56 (P, UNVERIFIED, unreadable; not used): 56_maersk-dry-container-spec-pdf.md. Captures 57 to 59 were used instead.
