# FDA potassium daily value, potassium declaration and "good source" and "high" claim lines (T10)

Date read: 20 October 2026. Tier S (Legal Information Institute, Cornell Law School, copies of the Code of Federal Regulations; the official eCFR was not reached). The text is the regulation, so the content is primary law read through a copy.
- 21 CFR 101.9: https://www.law.cornell.edu/cfr/text/21/101.9
- 21 CFR 101.54: https://www.law.cornell.edu/cfr/text/21/101.54
- Currency: the 101.9 copy shows no "current through" date. The 101.54 copy lists its most recent amendment as 66 FR 17358 (Mar. 30, 2001).

## 21 CFR 101.9(c)(8)(iv) (read through the Cornell page; fetched as a model summary of the page text)
- Potassium is in the RDI table of 101.9(c)(8)(iv). For adults and children 4 years and older the table gives 4,700 mg (row "Milligrams (mg)").
- 101.9(c)(8)(ii): the vitamin and mineral declaration "shall include vitamin D, calcium, iron, and potassium in that order".
- 101.9(c)(8)(iii): potassium may be omitted if present below 2 percent of the RDI and the label carries the "not a significant source" statement.

## 21 CFR 101.54 (quoted from the page through the fetch)
- 101.54(c)(1) "good source", "contains" or "provides": the food "contains 10 to 19 percent of the RDI or the DRV per reference amount customarily consumed".
- 101.54(b)(1) "high", "rich in" or "excellent source of": the food "contains 20 percent or more of the RDI or the DRV per reference amount customarily consumed".

## Arithmetic used (DERIVED, in `rework/screen/t10_potassium_cover_results.json`, block `us_fda_dv_and_claims`)
- Cube serve 316.6 mg is 6.7 percent of 4,700 mg.
- The good source line is 470 mg per reference amount; 316.6 mg is below it on a per 330 mL basis.
- The U.S. reference amount customarily consumed for this product was not read (limit). The per 330 mL basis is shown for orientation only.
