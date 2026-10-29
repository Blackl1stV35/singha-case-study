# Sources attempted and not read, or read only as a lead (T10, 20 October 2026, revised after the second verification)

A source listed here is not used as evidence for any figure in the T10 record. Each unread item is a stated limit in section 11 of `rework/73_potassium_medicines_kidney_cover.md`.

## Not read (stated limits)

| Source | Attempt on 20 October 2026 | Result |
|---|---|---|
| NIH Office of Dietary Supplements, Potassium Health Professional fact sheet, https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/ | WebFetch, two attempts | HTTP 403 both times. |
| NIH ODS Potassium Consumer fact sheet, https://ods.od.nih.gov/factsheets/Potassium-Consumer/ | WebFetch, an earlier run and this run | HTTP 403 both times. The 99 mg question is answered from the CRN page instead (S). |
| NICE Clinical Knowledge Summaries, hyperkalaemia, https://cks.nice.org.uk/topics/hyperkalaemia/ | WebFetch | HTTP 403. |
| NLEM, Thai National List of Essential Medicines (2565 or later) | Search | No official document found in results. Not checked. |
| Thai FDA drug database for potassium effervescent products | Earlier run | Form search only. Not checked. |
| Thai Food Composition Database (INMU, Mahidol), https://inmu.mahidol.ac.th/thaifcd/ | Earlier run | Search form only. A form submission is not permitted. No value read. |
| Search for a Thai coconut water potassium value (Thai language) | Search | Results were a health-blog table (not a government table) and a news item. No usable potassium value. |
| KDOQI 2020 primary (Ikizler et al., AJKD 2020) | Earlier run | HTTP 403 on the journal site. A secondary review (Frontiers in Medicine 2021) was read instead. |
| ESC 2021 heart failure guideline (MRA and potassium) and AHA/ACC | Earlier run | ESC page truncated before the relevant sections; AHA/ACC HTTP 403. Not read. |
| Thai CKD guideline 2022 (pre-dialysis care) | Earlier run | Listed on the Nephrology Society site, not opened. |
| Thai Gazette text of Notification 445 | Not searched | English translation published by the Thai FDA was read instead. |
| Population split of DOPA counts at ages 60 to 69 and 70 and over | Not searched | Stated limit. |
| EUR-Lex text of Regulation (EU) 1169/2011 | Earlier run | No text returned. UK-retained legislation copy used (S). |

## Closed in the second verification (now read)

| Source | Result |
|---|---|
| UK Kidney Association, Management of Hyperkalaemia in Adults, October 2023 (PDF, 171 pages) | Read; extract in `ukka_hyperkalaemia_guideline_2023_extract.md` (P). The earlier note that the text was not found was wrong: the first search had returned only secondary material. |
| USDA FoodData Central | Read through the official API (api.nal.usda.gov, DEMO_KEY): `usda_fdc_api_potassium_2026-10-20.md` (P). |
| eCFR current text of 21 CFR 201.306 | Read through the eCFR versioner API: `ecfr_21cfr201_306_current_2026-10-20.md` (P). The eCFR "current" page URL itself still redirects to a block page; the API address works. |
| Council for Responsible Nutrition page on the 99 mg line | Read: `crn_99mg_otc_drugs_2026-10-20.md` (S). |

## Search leads, not sources (see `us_99mg_secondary_leads_2026-10-20.md`)
Search results for the 99 mg claim returned supplement and blog pages, which are leads only. Their snippets were not opened and they are not cited for any figure.

## Fourth pass (20 October 2026, after the third verification)

| Source | Attempt | Result |
|---|---|---|
| KDOQI 2020 primary, https://www.ajkd.org/article/S0272-6386(20)30857-1/fulltext | WebFetch | HTTP 403 again. Not opened. The claim that KDOQI sets no daily figure rests on two secondary reviews (Molina 2021; Lambert 2022) and is stated that way. |
| Lambert et al., Commentary on the 2020 KDOQI nutrition guideline, Nephrology 2022, https://pmc.ncbi.nlm.nih.gov/articles/PMC9303594 | WebFetch | Read (S). It says potassium intake should be individualised and the guideline is far less prescriptive than earlier ones; it gives no potassium milligram figure. Saved in `kdigo_2024_potassium_extract.md`. |
| USDA FoodData Central API with the public DEMO_KEY | curl, header check | HTTP 429, Retry-After 13,044 seconds (10 requests allowed; used up by the earlier read). The FoodData Central site's data endpoint `https://fdc.nal.usda.gov/portal-data/external/<fdcId>` was used instead and returned the full JSON (HTTP 200) for the five IDs. Saved in `usda_fdc_api_potassium_2026-10-20.md`. |
| DailyMed label texts | DailyMed web service, SPL XML for eight set IDs | Read (P). Verbatim paragraphs saved in `us_drug_labels_hyperkalaemia.md`. |
| Notification 467 B.E. 2568 English translation, https://food.fda.moph.go.th/media.php?id=841484892608012288&name=P467_EN.pdf | WebFetch (the page was a compressed PDF stream; the tool saved the file) and pdftotext | Read in full (P, English translation). Saved in `thai_notification_467_2568_extract.md`. Thai Gazette text not opened. |
| Notification 445 Annex 4 Table 2, solid column | Re-read of the saved text layer | Read (page 65). Added to `thai_notification_445_potassium.md`. |
| Bangkok Biz News coconut water article | WebFetch, two reads | Re-read for the reasons given for each warning. Saved in `thai_dmsc_coconut_water_news_2026-10-20.md`. |
| DOPA population counts by single year of age or five-year band 56 to 60 | Not searched | The 56 to 60 band is not in the repo; the age 60 duplicate is estimated by an equal-thirds assumption. Stated limit. |
