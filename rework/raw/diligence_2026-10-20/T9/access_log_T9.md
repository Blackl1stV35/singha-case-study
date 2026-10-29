# Access log for T9: attempts that failed or were not used (second pass, corrected 20 October 2026)
Date read for all entries: 2026-10-20.

- EFSA full potassium opinion (efsa.europa.eu/en/efsajournal/pub/4592; doi 10.2903/j.efsa.2016.4592; Wiley): HTTP 403. The press release was used instead.
- NASEM summary page nap.nationalacademies.org/25353: redirect. The table was found on read/25353/chapter/8.
- PubChem citric acid and potassium bicarbonate pages: reCAPTCHA interstitial, no data. Wikipedia was used instead (tier S).
- Thai potassium reference value (MOPH Notification 445, Annex 3 row 32, 3,500 mg): not found by the T9 search. Confirmed from the saved English-translation page read by task T10 (raw/diligence_2026-10-20/T10/thai_notification_445_potassium.md), tier P.
- EU Regulation 1333/2008 Annex II sucralose maximum in flavoured water-based drinks: not reached. Old UK national instruments show 300 mg/l (2002 and 2005, both predating the EU regulation). Not relied on. UNVERIFIED.
- ONE dry container dimensions: resolved. https://www.one-line.com/en/dry-containers was read on 2026-10-20 (tier P): 5,898 x 2,350 x 2,390 mm, payload 28,330 kg (see one_dry_20ft_read_2026-10-20.md). The earlier search had found only special-cargo brochures. DSV's generic box is a cross-check only.
- Univar citric acid product page (food grade bags, list price): HTTP 403. The $96 per 50 lb snippet was not opened. UNVERIFIED.
- OnBuy potassium bicarbonate listing: HTTP 403. UNVERIFIED.
- Thai food-grade prices for KHCO3 and citric acid (baht): none found in Thai-language or Thai-market search. UNVERIFIED.
- Sucralose bulk prices: listings only (2.68 USD/kg lapsed trader quote; 22 to 28 USD/kg marketplace listing). Not usable as SOURCED. Used only to bound a cost line.
- Effervescent tablet density 1.250 g/cm3 (Engineering Proceedings 2023, vitamin C effervescent tablets): DOAJ, sciforum and MDPI all returned HTTP 403. Snippet only. UNVERIFIED. (Other benchmarks that WERE read are in effervescent_tablet_benchmarks.md: Pharmaceutics 2025 reopened on the second pass.)
- RSC Advances 2019 effervescent porosity (PMC9072709): the saved extraction was read earlier on 2026-10-20; on the second pass the PMC page returned a browser verification page, so the 13.67 percent figure is not reconfirmed and is quoted from the saved extraction with that flag. A WebFetch call on the same page also returned a tool error once.
- Effervescent hardness 10 to 47 N and porosity 15 to 45 percent: from a US patent snippet (non-effervescent rapidly disintegrating tablets). The Google Patents page returned 404. UNVERIFIED as a proxy.
- Bank of Thailand: the average counter rates for USD as of 15 October 2026 (https://www.bot.or.th/en/statistics/exchange-rate.html) WERE read (saved in raw/bot_fx_primary_2026-10-15.md; mid 33.5495). The BOT official reference-rate series was not separately reached. The earlier line of this log that said the BOT rate was not found and that FX was UNVERIFIED (tracker snippet of about 33.3 on 16 Sep) is withdrawn.
- Sweetness comparator: official lemon-lime soft drink pages (Coca-Cola India page HTTP 403) were seen only as snippets and are not used. The sweet and sour comparison now rests on two pages that were opened (Ingredion formula, S; Foods 2020, P), saved in taste_and_acid_benchmarks.md.
- Sprite Thailand label: not found.
- Thai Notification 195 B.E. 2543 (mineral-salt beverages): the Thai FDA compilation copy https://exfood.fda.moph.go.th/law/data/complilation/Compi_195.pdf was fetched on the second pass; the PDF text layer is unusable (TIS-620 mis-decoding), so page 1 was rendered to an image and read visually. Saved in thai_notification_195_mineral_salt_beverage.md (tier P, our translation, a compilation copy and not the Gazette text).
- FRED DEXTHUS and DEXCHUS: opened again on the second pass; latest observation 9 Oct 2026 in both. Used.
- Guidechem citric acid page: opened again on the second pass (rows listed in guidechem_rows_read_2026-10-20.md).
- Elchemy citric acid guide: opened again on the second pass (anhydrous premium sentence added).

## Third pass (20 October 2026, after the second verification)
- Thai Notification 468 Annex (P468.pdf, 16,616,446 bytes): the fetch tool refuses it (maxContentLength 10485760 exceeded). The local copy saved on 19 October 2026 (D:\Downloads\moph_468_annex\P468.pdf, SHA-256 5BEB26FC...FF7C, identical to the recorded hash) was read as page images: sucralose row (PDF page 678), citric acid (197), potassium hydrogen carbonate (534), condition 127 (789), condition TH3 (836). Saved in `thai_notification_468_rows_reconfirmed_2026-10-20.md`. The earlier "not reopened" entries above and in `blocked_or_unread_sources.md` are withdrawn.
- Explanatory announcement of Notification 468 (36 pages): fetch returns a binary with no usable text layer; the saved PDF was read as page images for pages 2 to 20. Saved in `thai_notification_468_explanatory_announcement_quantum_satis.md`. Pages 21 to 36 not read.
- Hardness: Jungbunzlauer PDF (page images), Ansar 2009 and Taymouri 2019 (abstract pages), Roquette page: read. PMC4219208 (amoxicillin) via PMC returned a browser verification page; via Europe PMC XML it returned text with no hardness unit. PMC3846033 (potassium citrate effervescent tablets) via Europe PMC XML: HTTP 500 twice; via europepmc fulltextRepo: HTTP 403; not read. RSC Pharmaceutics 2025 review (pubs.rsc.org): HTTP 403.
- Bank of Thailand USD page: reopened; it returned only navigation menus and links, with no rate table, so the 15 October 2026 average counter rate cannot be reconfirmed from the live page. The saved page `raw/bot_fx_primary_2026-10-15.md` remains the record; the USD rate is used only in the Elchemy citric acid cross-check.
- Guidechem sucralose page: reopened; static listing (identical prices in every column, zero change; update date 10 Oct against daily headers 14 to 16 Oct); see `guidechem_rows_read_2026-10-20.md`.
