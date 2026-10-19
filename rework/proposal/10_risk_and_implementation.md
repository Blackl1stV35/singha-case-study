# Risk register and implementation plan

Dated 19 October 2026. Desk model only: no bench test, sensory test or regulatory opinion yet. Letters in brackets point to Sources.

## Risk register

| Risk | Cause | Effect | Likelihood (ASSUMPTION) | Mitigation | Owner (role) |
|---|---|---|---|---|---|
| Retention and fizz | Dose of 0.55 volume (ASSUMPTION) is below CO2 solubility of 0.592 volume at 35 C [A, S, SOURCED], so the desk model keeps it dissolved at every serve from 5 to 35 C (DERIVED). | Desk model: time above the threshold is at most about 96 minutes, counting surface loss only (DERIVED). Published perception threshold of 0.44 g/L, from an abstract only [I, S, SOURCED], is a PROXY for a soft drink. | High | Persistence bench test by serve temperature. R&D sets the gate. No fizz claim. | R&D lead |
| Taste at the acid level | Total citric acid is 2.10 g per 330 mL (DERIVED), about four times the stoichiometric 0.52 g (DERIVED), to reach working pH 3.5 (ASSUMPTION). Citric acid pKa values [B, S, UNVERIFIED for this repository]. | Sourness above acceptance. Taste untested. | Medium | Panel test across a pH band. | Sensory lead |
| Sweetness | Sucralose 33 mg per 330 mL, about 100 mg/kg (DERIVED), set by a sweetness target that is an ASSUMPTION. Sucralose is 600 to 650 times sweeter than sucrose [F, S, SOURCED]. | Too sweet, too weak, or an aftertaste. | Medium | Panel test at two or three levels. A separate Singha lemon soda, which is not the lime product, names sucralose [J, S, SOURCED]. | R&D lead |
| Classification and labelling | Class is open: beverage, edible ice or electrolyte drink. Category 14.1.4 (flavoured drinks) allows sucralose at 300 mg/kg under condition 127, which applies the limit to the drink as ready to drink [D, P, SOURCED]. Condition TH3 applies to electrolyte drinks only, and they must be used with sugar [D, P, SOURCED]. Sub-category rule: the major-category permission extends to its sub-categories, but a sub-category permission stays within its own sub-category [E, P, SOURCED]. | A wrong class changes the sweetener condition, the sugar rule, the label and the excise base. | Medium | Written regulatory opinion before any print run. Label limited to composition. | Regulatory lead, via organiser |
| Potassium question | Potassium bicarbonate gives 317 mg potassium per serve, 9.1 percent of the Thai reference of 3,500 mg per day (DERIVED; reference [C, S, SOURCED]; primary text not opened). | Suitability for people on potassium-restricted diets is not assessed here. | Medium | Medical adviser's opinion. No potassium-benefit claim. | Medical adviser; regulatory lead |
| Moisture in the pack | Bicarbonate and citric acid react in the presence of water. Moisture that enters before opening can release CO2 inside the sealed pouch. No water-vapour rate is sourced and no humidity test has run. | Pouch swells, or the dose is lost before sale. | Medium | Film and seal specification, then a warm, humid storage test. | Packaging lead |
| Pouch and print cost | Pouch THB 1.30 (ASSUMPTION). It is near the midpoint of a non-Thai listing of USD 0.03 to 0.05 per piece (S, UNVERIFIED; no link or saved copy), converted at 33.55 baht per dollar, the midpoint of the Bank of Thailand's buying and selling rates on 15 October 2026 [O, P, SOURCED]. The range, THB 0.67 to 2.70, uses USD 0.02 to 0.08 from unverified supplier snippets, and the top is rounded up to 2.70 (ASSUMPTION). Print THB 1.50 and processing THB 0.50 are ASSUMPTIONS. No Thai quote was requested. | Pouch, print and processing are about 96.5 percent of the THB 3.42 per-pouch cost before carton (DERIVED; reactants are the other THB 0.12). The 12-cube cost includes a carton share of THB 0.42 per cube (THB 5 per 12-cube carton, from a retail box listing used as a PROXY). The 12-cube cost is THB 3.84 per cube (DERIVED). | High | Thai quotes through the organiser's process, requested only once the organiser approves outreach. | Procurement lead; finance lead |
| Excise base | Depends on product class. The Royal Gazette sugar-drink excise schedule, item 02.02, which lists rates for four periods [P, SOURCED], is not applied in the price model. The 14% ad valorem rate applies if the value base applies; the base was not read. | Unbudgeted tax or a price error. | Medium | Tax adviser's view after classification. Price model excludes excise until then. | Finance lead; tax adviser |
| Brand sign-off | The lion emblem was confirmed for this proposal. Brand-owner and legal sign-off sit with Singha's department and are not held here; the alcohol-cue question is unchecked. | No emblem on pack without sign-off. An alcohol cue could block the product. | Medium | No pack artwork is released before sign-off. | Organiser's brand department |
| Competitor overlap on flavour | The company's Singha Sparkling Water Lime Flavour is also lime: a 330 ml can at 15 baht, launched March 2026 [M, P, SOURCED; news reprint N, S, SOURCED]. Lime Cube overlaps it on flavour. The company describes its can as sugar-free with 0% calories (a company claim, not checked here). | Cannibalisation: the can takes buyers who want a lime drink, and the cube loses sales it would otherwise make. Confusion: shoppers read the cube as a lime drink in another form, or pick the can by mistake. | Medium | Keep the points of difference plain. Lime Cube differs in consumption form (a dissolvable cube that makes the drink in the glass, one cube per pouch) and in pack (a pouch of one cube, against a 330 ml ready-to-drink can). Lime Cube uses no sugar-free wording. Test shopper understanding of the difference before any pilot. | Commercial lead |

## Implementation plan (after the competition)

No step starts before the competition ends. Each gate is a question, and R&D or the panel sets the value.

1. **Formulation bench test (R&D).** Measure dissolved CO2 and persistence at 5, 20 and 35 C serves, at 0.55 volume in 330 mL. Gate question: what retention will R&D accept, compared with the published threshold [I], which is a PROXY for a soft drink? Feeds the dose, the fill, and whether any fizz wording is possible.
2. **Sensory test (panel).** Compare pH values, with 3.5 included, and sucralose levels. Gate question: which pH band and sweetness level does the panel accept? Feeds the acid load and sweetener level, and replaces the sweetness assumption.
3. **Pack and film specification.** Moisture barrier and seal for the pouch, then storage testing. Gate question: how much gas build-up in a sealed pouch is acceptable, and which film meets it? Feeds the pouch choice, the largest cost input.
4. **Regulatory opinion.** Written view from a Thai regulatory adviser on product class, condition TH3, label wording and the excise base, plus a medical adviser's view on potassium. Gate: written opinion and a proposed class put to the organiser. Feeds the sweetener condition, label and excise base.
5. **Cost quotes through the organiser's process.** Thai prices for pouch, print, potassium bicarbonate and citric acid, requested only once the organiser approves outreach. No Thai quote has been requested. Gate: quotes replace the placeholders. Feeds cost per cube and carton size.
6. **Pilot batch.** Small batch only after steps 1 to 4 pass. Gate: all four met, class settled, emblem signed off. Feeds the pilot channel and volume, which the organiser decides.

## Decisions owned by the organiser

None of these has been decided. The project does not decide them and has not contacted anyone about them.

- Sign-off on the lion emblem and the alcohol-cue question, held by the brand and legal department.
- Product classification: beverage, edible ice or electrolyte drink.
- Sold unit: one cube per pouch (inferred, not confirmed with the organiser) and carton size of 6, 12 or 24 cubes. An overseas analogue [K] makes 400 to 600 ml per cube (P, SOURCED), against the 330 ml serve here (ASSUMPTION).
- The pilot channel.

## Limits

- Desk model only: no bench test, no sensory test, no measured fizz decay.
- Taste is untested. pH 3.5 is a working anchor. The 0.55-volume gate is not set; R&D must define it.
- The sucralose limit comes from an annex extract [D], read for the flavoured-drink rows only; the full annex was not read. The potassium reference rests on secondary copies [C]; the primary text was not opened.
- Pouch and print costs are assumptions. The pouch range comes from a non-Thai listing that is UNVERIFIED. No Thai quote was requested.
- The figure of about 128,580 cubes per 20 ft container (DERIVED, [G]) assumes 12-cube cartons, volume as the limit, and packing allowances that are ASSUMPTIONS. It is not a load plan.
- Overseas analogues [H, K] are cited only because no domestic evidence for dissolvable cubes is among the sources used here.
- The company's sugar-free and 0% calorie description of its can is the company's own claim and was not checked. No shelf, price or sales test against the can has run.
- Bangkok climate figures are UNVERIFIED and are not used. Other sources were unreadable or blocked (a container PDF and three retailer listings). No figure relies on them.
- Claims are barred: no sugar-free, zero-sugar, sodium-free, health, electrolyte, hydration, potassium-benefit or validated-fizz claim. The composition may be stated as fact: potassium bicarbonate, citric acid and sucralose, with no sodium carbonate.

## Tier key

P: a government or regulator text read in full, a company's own filing or release, official statistics, a peer-reviewed article read in full, or a primary database. S: any other source, including press, trade portals, consultancy pages, company web pages that are not filings, handbooks reproduced online, and search snippets. SOURCED: the page text was read, and the public URL is given. UNVERIFIED: not read, blocked, unreadable, or only a snippet was read. DERIVED: our arithmetic, with the inputs and their tiers shown. PROXY: a stand-in for what is not measured. ASSUMPTION: a value chosen for the model, not sourced.

## Sources

All sources were read on 19 October 2026 unless a date is shown.

A. CO2 solubility at 35 C, attributed as printed to Dean JA, Lange's Handbook of Chemistry, 15th edition (1999), pp. 5.4 to 5.5, Table 5.1. https://bionumbers.hms.harvard.edu/bionumber.aspx?id=106208 S, SOURCED.

B. Citric acid pKa values, from a reproduced CRC handbook table. The handbook edition is not stated, and the values were read from rendered images of a saved copy. https://diverdi.colostate.edu/all_courses/CRC%20reference%20data/dissociation%20constants%20of%20organic%20acids%20and%20bases.pdf S, UNVERIFIED for this repository.

C. Thai potassium reference of 3,500 mg a day, from secondary copies: a third-party copy of MoPH Notification 182 (B.E. 2541), and a consultancy page that gives the current value under Notification No. 445. https://www.lovefitt.com/system/wp-content/uploads/2017/05/4-4-2ThaiRDI.pdf and https://www.siamdevelopment.com/thai-fda-rdi-nutrition-standards-in-thailand/ S, SOURCED. The primary texts were not opened.

D. Thai food-additive annex, flavoured-drink category 14.1.4, MoPH Notification 468 (B.E. 2568). https://food.fda.moph.go.th/media.php?id=840096266338836480&name=P468.pdf P, SOURCED for the flavoured-drink rows only. The full annex was not read.

E. Thai FDA clarification of Notification 468 (B.E. 2568), pages 1 to 3 of 36; translation ours. https://food.fda.moph.go.th/media.php?id=849894195891150848&name=468_FoodAdditives.pdf P, SOURCED.

F. JECFA monograph on sucralose sweetness. http://www.inchem.org/documents/jecfa/jecmono/v28je14.htm S, SOURCED.

G. 20 ft dry container dimensions and cubic capacity, from two product pages. https://www.one-line.com/en/dry-containers and https://seacubecontainers.com/product_specs/20-foot-dry/ S, SOURCED.

H. Overseas analogue: freeze-dried tea and coffee cubes, about 15 per pouch, article dated 17 June 2021. https://www.beveragedaily.com/Article/2021/06/17/Drop-it-then-its-hot-Coca-Cola-Japan-creates-freeze-dried-tea-and-coffee-cubes-to-reduce-packaging-waste S, SOURCED.

I. Abstract only (Food Research International, 2021): sparkling-water sensitivity threshold of 0.44 g/L CO2 (BET), n = 100. The full text was not read. A PROXY for a soft drink. https://research.wur.nl/en/publications/is-it-still-water-relationships-between-sparkling-sensitivity-and/ S, SOURCED.

J. Singha Lemon Soda product page, a separate product from the lime drink. It names sucralose. https://www.singhacorporation.com/singhalemonsoda/th/ S, SOURCED.

K. Overseas analogue: Ricola Drink Cubes press release, dated 5 June 2025. https://www.ricola.com/en/about/press-releases/ricola-brings-a-new-product-to-the-market/ P, SOURCED.

L. Desk model results, the proposal's own arithmetic, with no external source. Arithmetic only; DERIVED.

M. Company release for Singha Sparkling Water Lime Flavour, 330 ml can, priced at 15 baht; dated 13 March 2026. The sugar-free and 0% calorie wording is the company's own claim. https://www.nationthailand.com/pr-news/40063747 P, SOURCED.

N. News article reprinting the launch: Lime Flavour, 330 ml can, 15 baht; posted 17 March 2026. https://www.kaohooninternational.com/?p=579263 S, SOURCED.

O. Bank of Thailand, US dollar buying and selling rates, 15 October 2026. The midpoint of 33.55 baht per dollar is DERIVED from the two rates. https://www.bot.or.th/en/statistics/exchange-rate.html P, SOURCED.

P. Royal Gazette, B.E. 2560 (2017), sugar-drink excise schedule, item 02.02. https://www.ratchakitcha.soc.go.th/DATA/PDF/2560/A/095/111.PDF P, SOURCED.

## Team-only traceability (delete before submission)

Capture and file references removed from the body during the scrub of 19 October 2026. This section is the only place they appear. The body contained no record numbers (for example "record 52" or "D14"), no repository paths and no team names.

Capture files behind each source letter (letters as at 19 October 2026, risk-register pass):

- A: capture 73, 73_bionumbers-co2-solubility.md
- B: capture 75, 75_crc-citric-acid-pka.md
- C: captures 67 and 78, 67_thai_rdi_potassium_secondary.md and 78_thai-fda-potassium-rdi.md
- D: capture 82, 82_moph-468-annex-flavoured-drinks-extract.md; extract at rework/raw/moph_468_annex_flavoured_drinks_extract_2026-10-19.md
- E: capture 66, 66_thai_fda_468_subcat_rule.md
- F: capture 63, 63_jecfa-tgs-sweetness.md
- G: captures 57 and 58, 57_one-dry-containers.md and 58_seacube-20ft-dry.md
- H: capture 21, 21_beveragedaily-coke-japan-cubes.md
- I: capture 77, 77_wur-sparkling-threshold-abstract.md
- J: capture 48, 48_singha-lemon-soda-th.md
- K: capture 46, 46_ricola-drink-cubes-release.md
- L: handover_figures_results.json (desk model arithmetic, no public URL)
- M: capture 86, 86_singha-sparkling-lime-press-release-nation.md
- N: capture 87, 87_singha-sparkling-lime-article-kaohoon.md
- O: capture index 83; saved record rework/raw/bot_fx_primary_2026-10-15.md (capture 22 showed no table)
- P: capture index 84; saved copy of the Royal Gazette notice rework/raw/gazette_sugar_drink_excise_primary_2560_A095_111.md (capture 45 was blocked)
- Removed from the body in this pass: EFSA 2016 adult potassium, capture 69. No longer cited, because the Thai potassium reference is tiered S.

Changes in this pass (19 October 2026, risk register):

- Added the competitor risk row for the company's lime sparkling water, with a mitigation by consumption form and pack (captures 86 and 87).
- Company release tiered P, news reprint S, per the 19 October rules. The tier key now says that company releases count as P.
- Lemon soda kept only as a separate product (capture 48). No lemon statement about Lime Cube remains.
- Thai potassium reference tiered S, primary text not opened. EFSA citation removed.
- Citric acid pKa tiered S, UNVERIFIED for this repository.
- Condition 127 now follows the annex wording (applies the limit to the drink as ready to drink). The annex is the source; the other proposal files that still carry the older wording need the same change.
- Pouch range rebased to the non-Thai listing (UNVERIFIED), converted at the Bank of Thailand midpoint (capture index 83). No Thai quote requested.
- Excise row changed from UNVERIFIED to P, SOURCED (gazette, saved copy of the Royal Gazette notice).
- Container dimensions tiered S (ONE and SeaCube), not P.
- Sucralose and potassium arithmetic checked against the handover results: the printed 317 mg gives 9.1 percent of 3,500 mg, the figure now used in the body.
- Source letters renumbered A to P; the EFSA letter is gone.

Changes in this pass (19 October 2026, final check and binding rules):

- Potassium printed as 9.1 percent (317 mg of 3,500 mg). Tier key checked against the canonical paragraph; no change needed.
- Pouch listing aligned to USD 0.03 to 0.05 (non-Thai, UNVERIFIED). The 0.67 to 2.70 band comes from USD 0.02 to 0.08 snippets and is an ASSUMPTION. Cost share rounded to 96.5 percent.
- Carton share written as the single agreed sentence; the other carton-share sentence removed.
- Excise row: the 14% rate applies if the value base applies; the base was not read. The four-period reading was checked against the saved copy of the Royal Gazette notice.
- Brand sign-off row uses the agreed sentence.
- Scope sentence removed from the limits.
- Solubility citation (Source A) matched to the BioNumbers capture. Proposal file 03 and the screen code still cite the 10th edition with a Wikipedia URL; they need the same citation.

Wording changed in the body, earlier scrub (letters as at that pass):

- Tier key, SOURCED: "captured and read; name the capture file" became "read; the public URL is listed under Sources." The label is unchanged.
- Tier key, UNVERIFIED: "not captured" became "page text not read." The label is unchanged.
- Sources intro: "All captures were read" became "All sources were read".
- Limits: "not in the capture index" (source E) was removed from the body. "captures" became "sources" in two bullets.
- The tier key sits after Limits, not at the top as the scrub brief described. It was not moved.
