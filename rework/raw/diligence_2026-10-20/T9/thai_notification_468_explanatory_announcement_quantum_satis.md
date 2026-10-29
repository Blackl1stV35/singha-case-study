# Explanatory announcement of Thai Notification 468 B.E. 2568: quantum satis and the sum-of-ratios rule (read 20 October 2026)

Tier P (Thai regulator text, Thai language). English wording is our translation; no English version exists on the page.

## Source and how read

- Document: "ประกาศสำนักงานคณะกรรมการอาหารและยา เรื่อง คำชี้แจงประกาศกระทรวงสาธารณสุข (ฉบับที่ ๔๖๘) พ.ศ. ๒๕๖๘" (Announcement of the Office of the Food and Drug Board, explanatory statement of MoPH Notification No. 468 B.E. 2568). 36 pages, 788.1 KB. Signed by the Secretary-General of the Food and Drug Board, "ประกาศ ณ วันที่ ๖ มกราคม พ.ศ. ๒๕๖๙" (announced 6 January B.E. 2569 = 6 January 2026), page 5.
- URL: https://food.fda.moph.go.th/media.php?id=849894195891150848&name=468_FoodAdditives.pdf . The text layer is not usable (the fetch tool could not decode it), so the PDF was saved by the fetch tool to the session tool-results folder (outside the repository) and pages 2 to 5, 6 to 8 and 9 to 20 were rendered to images and read visually on 20 October 2026.
- This is the explanatory announcement, not the Annex. The Annex rows are in `thai_notification_468_rows_reconfirmed_2026-10-20.md`.

## Page 2: clause 3 and clause 4 (our translation)

- Clause 3: food additives must be used according to the additive name, food category or type, technological function and maximum permitted amount set in List 1, with the further explanation in List 2 attached to Notification 468. Where a condition permits use in a main category such as 14.1.4, the additive is also permitted in its sub-categories 14.1.4.1, 14.1.4.2 and 14.1.4.3; where a condition permits a sub-category, use is only in that sub-category.
- Quantum satis (page 2, the sentence on a maximum set as "ปริมาณที่เหมาะสม"): "quantum satis" means the lowest amount of the additive that gives the desired technological effect in manufacturing under good manufacturing practice (GMP). An additive with a quantum satis condition does not mean it may be added without limit. The operator must study the use of that additive in its own product to find the lowest amount that gives the desired technological effect (the example given is a preservative studied at different amounts for shelf life), and the study must be under GMP.
- Clause 4: where two or more additives with a numeric maximum, in the same functional group, are used together, the sum of the ratios (amount used over the maximum permitted amount) of each additive must not exceed one. The clause applies where no specific additional condition applies under List 2.

## Page 4: the five lists

List 1 (explanation of functional groups), List 2 (calculation of the sum of ratios for numeric-maximum additives in the same functional group or colour group), List 3 (calculation according to the additional conditions), List 4 (how to calculate additive amount in the ready-to-consume state), List 5 (guidance on carry-over). Clause 5 (page 4): an additive use that differs from Notification 468 needs the approval of the Food and Drug Board's office after a safety assessment.

## Pages 6 to 8: List 1 functional groups (names as printed, with the Thai group name in the first column)

The groups include acidity regulator (acid, acidifier, buffer, pH adjusting agent), carbonating agent (an additive added to produce carbon dioxide), raising agent, sweetener (sweetener, intense sweetener, bulk sweetener), bulking agent and filler, stabilizer (including binder and tablet binder), and carrier (including tablet disintegrant, granulation aid and glidant). So a binder or filler that is itself a food additive belongs to a functional group and needs its own row in the Annex; the cube's binder is not yet named.

## Page 9: List 2, section 1

The explanation states that additives whose maximum is "quantum satis" are not brought into the sum-of-ratios rule even if they are in the same functional group; the rule concerns only numeric maxima. The formula is: 1 is at least the sum of Conc A over ML A, Conc B over ML B, and so on.

## Page 5: dates and transition

- Clause 8 (page 5): Notification 468 takes effect the day after publication in the Royal Gazette (12 December B.E. 2568 = 12 December 2025).
- Clause 7 (page 5): a manufacturer or importer whose products used additives differently from Notification 468 before the effective date has until 12 December B.E. 2570 (12 December 2027) to comply, for products placed before the effective date. A new product is not covered by this relief.

## What this means for the cube (DERIVED)

- Potassium bicarbonate and citric acid are quantum satis in category 14.1.4. That does not leave the dose open: the amount has to be the lowest that gives the technological effect. For citric acid the effect is the working pH 3.5 (a team design target, ASSUMPTION), and the 2.10 g is 4.05 times the stoichiometric amount, so the target pH is the justification the operator would have to document. A higher pH needs less acid (see `rework/screen/spec_revalidation_results.json`, key quantum_satis_citric_acid_basis).
- The sum-of-ratios rule concerns numeric maxima only. In the cube only sucralose has one (ratio 0.333 on 100 mg/kg against 300 mg/kg), so the sum is 0.333.
- Not read: the remaining pages 21 to 36 of this announcement (Lists 3 to 5), and Condition TH3 is not defined in this announcement (it is defined in the Annex, page 835).
