# NHES VI hypertension at ages 40 to 59: re-read for verifier issue (T13 second pass, 20 October 2026)

Purpose: the verifier could not reproduce the 25.6 percent figure (ages 40 to 59, 2019 to 2020) in the stakeholder register of record 76. This file records every attempt made on 20 October 2026.

Article: Aekplakorn W et al., BMC Public Health 2024;24:3149, DOI 10.1186/s12889-024-20643-1. Thai National Health Examination Survey VI (NHES VI), adults aged 20 and over.

## Attempts, in order

1. https://pmc.ncbi.nlm.nih.gov/articles/PMC11562084 (WebFetch, read 20 October 2026). Returned a browser verification page (reCAPTCHA check). No figure. Not usable.
2. https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-024-20643-1 (WebFetch, read 20 October 2026). Returned a 301 redirect to https://link.springer.com/article/10.1186/s12889-024-20643-1. That page returned a 303 redirect to a publisher sign-in page (idp.springer.com). The sign-in flow was not followed, because it is an authentication step and not the article.
3. https://europepmc.org/article/PMC/PMC11562084 (WebFetch, read 20 October 2026). HTTP 403; body not retrieved.
4. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11562084/fullTextXML (WebFetch, read 20 October 2026). The full-text XML of the open-access article, served by Europe PMC, was returned as an extract. Result, quoted from the extract:
   - Table 2, row "40-59 Crude", 2019 to 2020 column: 25.6 (95% CI 22.6 to 28.7). The extract says the row is not split by sex, so it covers both sexes.
   - Table 2, age-standardised, men: 26.8 (24.0 to 29.6); women: 24.6 (22.9 to 26.4).
   - Abstract (as quoted in the extract): age-standardised hypertension prevalence 25.7 percent (24.6 percent females, 26.8 percent males).

## Result and tier

- Value: 25.6 percent crude prevalence at ages 40 to 59, both sexes, 2019 to 2020 (NHES VI, Table 2).
- Tier: P (extract). The figure was read through a WebFetch extract of the publisher-independent full-text XML (Europe PMC), not by reading the printed table in full. The extract is model-written, so the table row should be checked by eye against the published table before the figure is printed. The extract says the row is not split by sex; the saved T10 extract reads both sexes, which is consistent.
- Status: SOURCED for the record. It is not on any slide.
- Access block: the PMC HTML page and the publisher page were not readable (CAPTCHA, HTTP 403, sign-in redirect).

Saved trace: this file. The earlier saved extract is `rework/raw/diligence_2026-10-20/T10/thai_hypertension_diabetes_acei_arb.md` (section 1, line 8 or thereabouts), which reads 25.6 percent for 40 to 59, both sexes.
