# Item V6: search and access log (20 October 2026)

Rules applied: rework/SOURCING_POLICY.md. A search result is a lead until the page is opened. Every claim below that was not opened is marked "snippet, not opened".

## 1. Secondary pages opened (tier S)

- ChemLinked, "MOPH Notification Re: Electrolyte beverage (No. 195 & 332)", https://food.chemlinked.com/database/view/1843, opened 20 October 2026. Fields as extracted: release date 2011-03-03, implementation date 2011-04-08, status "In force", scope "applicable to electrolyte beverage", and the note that it incorporates the standard of No. 195 and No. 332 (No. 2). The page lists no amendments after 2011. Its metadata dates (2020 and 2026) are page dates, not regulation dates. The 3 March 2011 date is the signing date printed in the Gazette text of the "(No. 2)" notification and 8 April 2011 is its effective date on the Thai FDA list, so the entry agrees with the primary texts. Tier S; used only as a cross-check.
- ECOLEX record, https://www.ecolex.org/details/legislation/notification-of-the-ministry-of-public-health-no-195-be-2543-2000-re-electrolyte-drinks-lex-faoc160178/, opened. Title and abstract only; "Status", "Amended by" and "Repealed by" are printed as not stated, and its "date of text" (1987 or 2001) conflicts with the B.E. 2543 title, so it carries no weight on status.
- ChemLinked entries 7634 and 6683, which a search summary had described as electrolyte drink entries, were opened and are not: they are Nos. 473 and 465 (beverages in sealed containers). The search summary was wrong on that point and was not used.

## 2. Pages that could not be opened

- Royal Gazette site, https://www.ratchakitcha.soc.go.th/DATA/PDF/2552/E/041/19.PDF and https://www.ratchakitcha.soc.go.th/DATA/PDF/2563/E/237_1/9.PDF (with and without "www"): HTTP 403 to the fetch tool. The Gazette texts used instead are the copies hosted by the Thai FDA (P195, the No. 2 file, P413, P415, P416, P417), each of which prints the Gazette volume, part, page and date.
- FAOLEX record pages (https://leap.unep.org/en/countries/th/national-legislation/notification-ministry-public-health-no-195-be-2543-2000-re and https://www.fao.org/faolex/results/details/en/c/LEX-FAOC160178/): HTTP 403. A search summary said the FAOLEX record shows "Repealed: No"; that is a snippet, not opened, and is not used. The FAOLEX PDF of the English translation (tha160178.pdf) did open.
- Built-in browser pane, https://food.fda.moph.go.th/...: refused by the pane ("navigation ... was denied or failed"), so the FDA pages were read through the fetch tool only.
- https://food.fda.moph.go.th/media.php?id=857797030200877056&name=GuidelinesLaw465.pdf (FDA implementation guide for No. 465): over the fetch tool's 10 MB limit. https://food.fda.moph.go.th/media.php?id=840096265747439616&name=P468_EN.pdf (English Annex of No. 468): same limit.
- https://exfood.fda.moph.go.th/law/data/announ_fda/6_No54 Statement yeast - mold.pdf: fetched, text layer undecodable, not read in the first pass; read as page images in the revision of 20 October 2026 (see section 5 and fda_statement_yeast_mold_B_E_2554.md). https://food.fda.moph.go.th/media.php?id=509711629370400768&name=416_QualitySetting.pdf: fetched, text layer undecodable, not read.
- https://food.fda.moph.go.th/media.php?id=509705379920355328&name=62_Beverage2.pdf: rendered and read; it is an FDA announcement on caffeine labelling of beverages and has no bearing on classification.
- https://exfood.fda.moph.go.th/law/data/announ_moph/CANCEL/Cancel_admin2.pdf: fetched, undecodable, not read; it was a search hit and nothing suggests it relates to No. 195.

## 3. Searches run and what they returned

Standard mode unless stated. No search surfaced a source that is better than the Thai FDA pages above.

| Query theme | Result |
|---|---|
| Thai title of No. 195 with "amended, repealed" | FDA compilation, FAOLEX and news pages; no repeal found (leads; the FDA pages were then opened) |
| English translation of No. 195 | FAOLEX English PDF (opened) |
| No. 413, 415 and 417 B.E. 2563, Thai and Thai-numeral titles; Gazette-domain search | FDA category pages and Gazette hits; the FDA copies of 413, 415, 416 and 417 were opened |
| No. 2 B.E. 2554, "128 part 41 ง" | ChemLinked entry and FDA statement (opened or fetched, see sections 1 and 2) |
| Draft "mineral-salt beverage (No. 3)" or hearing; WTO SPS and TBT; extended mode for 2025 and 2026 revisions | None found. The 2025 draft that did surface revises beverages in sealed containers (No. 356), not electrolyte drinks; its final form No. 465 was read (n356_n465_sealed_container_beverages.md). Trade-press summaries of the 2025 and 2026 FDA notification packages were not used as sources |
| FDA or Thai practice on how a drink is classed as a mineral-salt beverage versus a sports or flavoured drink | Consumer and pharmacy pages only (not usable as evidence of the FDA's practice). No FDA guidance, Q&A or ruling on the "main ingredient" test was found |

## 4. Statements taken from search summaries and not relied on (snippet, not opened)

- That Notification 195 was repealed or amended by anything other than the five footnoted changes: no source supports it; the FDA list says the opposite.
- That a 2009 Gazette notice (Volume 126, Special Part 41 ง, 19 March 2552) repealed the pathogen text of 4(5)(ค): the Gazette page returned HTTP 403 and the claim is a snippet, not opened. It does not touch clause 4(1) or clause 7 on the claim itself.

## 5. Revision pass of 20 October 2026 (after the review of this item)

Same rules. Everything below was opened on 20 October 2026.

Opened and read:
- FDA list pages 1 to 15, 16 and 29 (https://food.fda.moph.go.th/food-law/category/announcement-of-the-ministry-of-public-health-1/?page=N): every row title, status and date saved in fda_list_pages_1_to_15_titles_2026-10-20.md and fda_list_status_n195_n332.md. Same result as the first pass.
- https://food.fda.moph.go.th/food-law/f2-elt-drink: opened again; lists No. 195 and the "(No. 2)" notification only; the printed date is a page date (see fda_list_status_n195_n332.md, section 3a).
- https://food.fda.moph.go.th/food-law/f2-beverage-sc: opened; lists Nos. 356, 402, 465 and 473 (see n356_amendments_465_473_thai_and_402_english_2026-10-20.md).
- No. 473 Thai text, https://food.fda.moph.go.th/media.php?id=943702414677123072&name=P473.pdf: 3 pages, text layer does not decode, read as page images. Read in full.
- No. 465 Thai text, https://food.fda.moph.go.th/media.php?id=841484111456641024&name=P465.pdf: 1 page, read as a page image.
- No. 402 English translation, https://food.fda.moph.go.th/media.php?id=509422712972779520&name=No.402.pdf: text extracted and read.
- The FDA clarification 6_No54 Statement yeast - mold.pdf: 3 pages read as images (fda_statement_yeast_mold_B_E_2554.md).
- The FDA English translation of No. 195, https://faolex.fao.org/docs/pdf/tha160178.pdf: fetched again, hash matches the first pass, text extracted; the sentences for clauses 1, 4(2) to 4(9), 8 and 9 added to n195_fda_unofficial_english_translation.md.
- The locally kept copies of P195.PDF (5 pages) and Compi_195.pdf (3 pages) from the first pass: hashes match the saved pages; page images re-read to add the Thai sentences for clauses 1, 4(2) to 4(6), 8 and 9 to n195_gazette_original_B_E_2544.md and n195_compilation_footnotes_B_E_2566.md.

Could not be opened:
- Royal Gazette home page https://ratchakitcha.soc.go.th/: HTTP 403 to the fetch tool again. The Gazette index therefore still cannot be searched from here; that is the route named in the record's limits.

Searches run (standard mode; results are leads only):
- Thai query for an amendment or repeal of No. 195 with 2568 and 2569: returned the FDA compilation, the FDA clarification, ChemLinked entries 1843, 6683 and 7634 and a consumer page; nothing newer than the first pass. The search summary's remarks were not used.
- English query for a 2026 amendment, repeal or replacement of No. 195: returned ChemLinked 1843, a FAOLEX mirror and trade-press items on 2025 drafts for beverages, water and ice; nothing naming No. 195. The FAOLEX mirror page was not opened and its "Repealed: No" remark in the search summary is a snippet, not opened, and is not used.

Not done and why: reading the Gazette text of every general notification issued after March 2023 (for example Nos. 450, 456, 468, 472) to look for an in-body amendment of clause 3, 4(1) or 7 of No. 195. It was judged out of proportion for a status check, and the record states it as a limit with its route (the Gazette index or the Gate 1 opinion).
