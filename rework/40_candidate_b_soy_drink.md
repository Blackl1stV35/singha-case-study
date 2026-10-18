# Finalist B: midlife isoflavone soy drink, desk track result (18 October 2026)

Status: desk research complete on four tracks (regulatory, dose, consumer, supply and price). Each track had adversarial checks on its verified claims, then a completeness critic. Raw output: [raw/waexezeqk_finalist_b_desk_track.json](raw/waexezeqk_finalist_b_desk_track.json). No physical, consumer or registration step has run. Nothing was submitted or contacted.

**Verdict: not advanced, not killed.** B stays second-ranked and conditional. Its regulatory route is open, not passed. Its dose recommendation from the first pass is withdrawn (section 3).

## 1. What holds on public text

- **Thai soy milk already carries isoflavones.** Eight products from four brands, two flavours each, held 25.5 to 63.5 mg per 250 ml (Chiang Mai, 2018). Verified from the abstract; the full PDF was not read.
- **The operative food standard is Notification 198 (B.E. 2543).** It requires UHT at 133 °C for at least 1 second, aseptic packing, soy protein at least 2 %, and soy fat at least 1 %. Verified from the Thai text. The consolidated text is unverified.
- **No Thai FDA isoflavone intake limit or guidance was found.**
- **EFSA 2015 (press release only):** no indication of harm at supplement-level doses over up to about a year. No tolerable upper intake level. No data for women in the transition to menopause, or with a cancer history. The full opinion returned HTTP 403.
- **No menopause-positioned soy drink was found** on the pages read. The kill test is not met on that evidence, but the evidence is weak (section 6).
- **No Thai isoflavone-extract supplier was verified.** The only suppliers found are foreign: Total Ingredients (40 % HPLC, India origin, certificate of analysis behind a login) and Parchem (quote only, no specification).
- **No Thai co-packer was identified** for a 250 ml carton UHT soy line. Lactasoy and Tofusan run UHT lines, but neither was asked. General Beverage co-packs PET bottles (lead from 2014).

## 2. Corrections to the working file

These corrections come from the adversarial checks. Each needs an edit in rework/01 or rework/02 before the entry is used.

| Claim in file | Check result | Action |
|---|---|---|
| "Plain Thai soy milk carries little isoflavone" (rework/01, section B; ideation JSON) | Contradicted by the 2018 Chiang Mai data (25.5 to 63.5 mg per 250 ml) | Replace with the 2018 range |
| Food route "pass" (rework/02, check B1) | Refuted as written. No source covers a 250 ml UHT drink as a conventional food form, and cl. 2 lists liquids among supplement forms. The food-or-supplement question is open | Change to "pass on form; open on purpose" |
| Serial-number basis, Notification 293 cl. 12 (check B1) | Contradicted: cl. 12 is repealed by Notification 411 cl. 2 | Cite 411, or FDA slide 7 |
| Mahidol value of 9.65 (per 100 g) | Unit not verified; table undated (2010 metadata) | Do not use as a present-tense fact |
| "Midlife reason tied to a Mintel June 2026 report" | The public Mintel page names no menopause, hot flush, soy or isoflavone | Source it or drop it |
| "Prefers a daily food to capsules" | No source. Kasetsart 2011 measured beverage (57.7 %) and supplementary food (25.3 %) preferences, with a denominator of 352, not 402 | Reword, or cite the survey as stated |
| Sirisivanart 2025, OR 12.57 | Crude odds ratio. The adjusted OR is 6.69 (95 % CI 0.68 to 66.15, p = 0.104), not significant | Quote the adjusted figure, or drop it |
| Maejo 2025, 3.15 baht per 300 ml, "nearest WTP study" | Document identity unresolved; sample is low-income parents in Narathiwat with a cow's milk comparator | Do not use as WTP evidence |
| Sriprasert 2017, 65 % hot flushes or night sweats | Cited URL is a wrong page; volume and pages unconfirmed | Unverified. Do not use |
| Koebnick 2005 | Cited through a test-host mirror; European population | Cite the DOI |
| Lactasoy "first UHT soymilk manufacturer in Thailand" | A brand-guideline source credits the 1981 launch to another brand | Unresolved. Do not use in competitor framing |
| Total Ingredients minimum order | Live page 25 kg; second listing 50 kg | Confirm before use |
| Notification 293 cl. 3(1) (plant and animal products as "other substances") | Verdict contested: refuted on a stale-compilation ground, which was not applied to cl. 2 | Cite cl. 3(2) for extracts |

## 3. Dose and labelling

**Screen.** `rework/screen/soy_isoflavone_dose_screen.py`, results in `soy_isoflavone_dose_screen_results.json`. The base soy is assumed uniform over 25.5 to 63.5 mg. The extract tolerance is ±10 % (an assumption, not sourced). The window is ±15 % with a 90 % target. No label between 40 and 100 mg keeps 90 % of servings in the window. The best is about 73 %.

**The first-pass recommendation does not hold.** It proposed "at least 50 mg total isoflavones per 250 ml, with about 30 mg standardised extract". Under the only identified extract specification (40 % isoflavones), 30 mg of extract supplies about 12 mg of isoflavone. The worst-case total is about 36 mg, below the 50 mg floor. The screen treats "added extract" as isoflavone mass, which the available product does not supply. The recommendation is withdrawn until the extract's units and tolerance are fixed.

**Safety gate.** The target group includes women in the transition to menopause and women with a cancer history. EFSA reports no data for either. An Intertek snippet on endometrial hyperplasia (6 of 154 women at 150 mg per day for five years) was noted but not assessed. No dose should be set before a medical or regulatory safety review.

**Stability.** No data on isoflavone loss through UHT processing or over shelf life. The labelled dose cannot yet be shown to hold to expiry.

## 4. Regulatory route and claims

**Food or supplement: open.** The form test points to food, but FDA's own 2026 slides say the boundary turns on the purpose stated to consumers. Any menopause, hot-flush or sleep message, or a declared isoflavone dose, moves the product toward the claim rules.

**Claims.** No annex of Notification 447 lists a soy, isoflavone, menopause, hot-flush or sleep claim. This was checked on the English unofficial translation only. Any other-function or risk-reduction claim needs:

- an FDA-designated assessment, then FDA permission (cl. 5);
- human intervention evidence in the target group (cl. 2(3));
- no implication of relief or treatment of disease (cl. 6(2));
- the required disclaimer (cl. 6(3)).

Hot flushes and sleep disturbance are symptoms. They fit poorly under "normal body function", and the text does not settle whether they count as "disease" for cl. 6(2).

**Other open points:**

- A declared isoflavone dose with no health words may itself be a health claim under the broad definition in cl. 1.
- Is standardised extract a new food? Under FDA slides 9 and 10, a new food needs a label and an FDA approval letter before a serial number.
- Any benefit wording needs an advertising approval (FDA slide 6; the Food Act s.41 text was not read).
- Would an isoflavone-fortified drink still count as soy milk under Notification 198 cl. 3, and is the extract a permitted addition?

## 5. Consumer evidence and test design

**Demand: weak to moderate, and not yet shown for purchase.**

- Thai symptom data come from clinic and small-city samples: 52 % insomnia in a 102-woman Bangkok clinic sample; hot flushes among the three most common complaints in an 870-woman, nine-clinic cohort.
- No Thai community prevalence estimate for women aged 40 to 59 was found.
- The only Thai survey on soy or isoflavone products in this group (Kasetsart 2011, n = 402) measures stated interest (87.6 %), not purchase or price.
- No Thai study measures willingness to pay for a functional or isoflavone soy drink.

**The 30-woman blind test (rework/01, section B) cannot show:** demand size, prevalence in the target group, price or willingness to pay, reason to buy, repeat use, or dose safety. At n = 30, a 15/30 result has a 95 % interval of 33 to 67 %, and 0/30 has an upper bound of 11 %. Two spec changes are needed before the test runs: a screen for hot flushes, night sweats or disturbed sleep, and a price-ladder question. It also must not run before the dose-safety gate.

## 6. Supply, production and price

- **No verified shelf price** for a plain 250 ml UHT soy drink. Lazada trending pages show Lactasoy unsweetened at 300 ml and Tofusan at 180 ml. Two DNA and Beanwell snippets conflict (324 vs 228.75 baht; 504 vs 363.75 baht). None is usable as a price anchor.
- **Extract:** no Thai supplier, login-gated certificate of analysis, and a one-sided specification ("not less than 40 %"). A two-sided specification with lot data is needed.
- **Co-packer:** none identified for a 250 ml carton line with isoflavone dosing. Lactasoy, Tofusan and General Beverage are candidates to ask. None has been contacted.
- **Kill-test coverage:** the store audit is incomplete. Makro, Tops, 7-Eleven, Boots and Villa Market were not reached. Shopee redirected to a verification page, which was not bypassed. The Lazada method note says catalogue search returns "no results" even for control terms, so the absence is weakly supported.

## 7. Kill-test status

The kill test in rework/02 section B is: a desk check of Thai FDA rules shows the pack can carry only nutrient content and no menopause-linked benefit.

- **Public text:** not met, but not cleared. The regulatory track says "provisionally triggered for planning". The supply track says "not killed".
- **Reconciled reading:** record the test as open and plan as if triggered. No annex lists a menopause benefit, and the only route needs FDA permission after an assessment.

## 8. Go or no-go criteria (proposed, for team agreement)

Advance B only if all of these hold:

1. FDA's written classification: food or supplement, asked with and without a dose message and with and without a symptom message.
2. FDA's written reading of cl. 6(2): whether hot flushes or sleep disturbance count as "disease", and whether a cl. 5 permission is obtainable within the timetable.
3. A two-sided certificate of analysis for an isoflavone extract from a supplier that will sell to a Thai registrant, plus lot-tested base soy isoflavones.
4. A safety review covering women aged 40 to 59, including transition-stage women and women with a cancer history. A dose is set only after it.
5. Confirmation that a fortified drink stays compliant with Notification 198.
6. A co-packer with a 250 ml UHT carton line that will run isoflavone dosing, with a written quote.
7. A redesigned demand test (symptom screen and price question), run after gate 4.

**Kill B if** FDA reads the symptom wording as disease relief with no cl. 5 route obtainable, **or** no two-sided extract specification with lot control is available at a viable cost.

## 9. Limits

- Desk and web reads only. No contact, submission, registration or physical test.
- Primary texts not read: the full EFSA 2015 opinion (HTTP 403), the consolidated Notification 198, Notifications 405, 411 and 448, Notification 450, the Food Act s.41, and the Thai text of Notification 447's annexes.
- Absence claims are weakly supported. Catalogue search is unreliable, and several Thai retailers were not reached.
- The dose screen is a model with unsourced assumptions. Its output is not evidence about the product.

## 10. Close-out (18 October)

Per the user's instruction, no step in the candidate B plan contacts an outside party. Each earlier step is either done on desk evidence or closed as a limit (section 9 lists the limits). Decisions are in section 11.

| Earlier step | Status | Result or limit |
|---|---|---|
| 1.1 Written question set to FDA or an adviser | Closed as limit | No reply without contact. Treated as provisionally triggered for planning |
| 1.2 Unread Thai texts | Desk attempt; closed as limit where unreadable | Unreadable texts are listed in section 9 |
| 2.1 Extract specification and CoA | Closed as limit | Only a one-sided 40 % specification, from a login-gated listing |
| 2.2 Base-soy lab assay | Closed as limit | No lab work in the plan |
| 2.3 Dose screen re-run | Done with existing inputs | No dose label is feasible on current inputs. The 73 % figure is a model output only |
| 2.4 Safety review | Closed as limit | No dose is set |
| 2.5 Composition against 447 cl. 4 | Closed as limit | Composition not public |
| 3.1 Pilot UHT retention | Closed as limit | No pilot |
| 3.2 Shelf-life study | Closed as limit | No study |
| 3.3 Packaging compatibility | Closed as limit | No co-packer |
| 3.4 Co-packer quote | Closed as limit | No contact |
| 3.5 Unit economics | Closed as limit | Not costed |
| 4.1 Demand-test specification | Done on paper | Revised specification, decision D5 |
| 4.2 Full texts of Thai demand studies | Desk attempt; closed as limit | Mahidol and MDPI texts not readable (HTTP 403) |
| 4.3 Dated shelf-price captures | Closed as limit | Lazada and Shopee read earlier. Makro and Tops not reached |
| 4.4 Consumer test | Closed as limit | Not run |
| 5.1 Go or no-go | Decided | Not advanced (D1) |

## 11. Decisions taken (18 October, by Claude per recommendation; reviewable)

**Validation status.** B has no food-science or engineering verdict. Every verdict on B is a desk verdict on regulation, dose, supply or consumer evidence. The food-science and engineering screens in the repo (rework/15 to 17, 22, 28 to 32) model product A, the leaf wrap, and do not transfer to a soy drink. The Singha verdict notes in memory cover the botanical-citrus and flavour-house questions for the export track, not B. So B is not validated by the food-science or engineering verdicts.

| # | Decision | Reason | Reopen if |
|---|---|---|---|
| D1 | Candidate B is not advanced. Its desk track is closed with limits. Candidate A stays primary | The midlife claim route cannot be cleared on public text. The food route, dose and cost stay unverified | The team later authorises outside contact |
| D2 | B carries no health, symptom or isoflavone-dose wording | Notification 447 cl. 1 and cl. 6(2) risks. Dose safety unsettled | An FDA reply, which is not in the plan |
| D3 | Gates A, B and C are closed as limits. Planning treats the kill test as triggered | No outside reply, no measured base soy, no safety review | As D2 |
| D4 | If B is reopened, the retention threshold is 80 % of isoflavone through UHT and shelf life. The shelf-life target is set with the trial. Both are proposals, not sourced | Gate D needs a number before any trial | Team decision at reopening |
| D5 | Demand-test redesign: a symptom screen for hot flushes, night sweats or disturbed sleep, plus a price question. Not run | The current specification cannot show demand or price | Reopening, after gates A to C |
| D6 | The stomatal scoring rule in rework/33 step 7a is adopted with its proposed numbers: 15 stomata per wrap, 9 of 10 scorer agreement, 270 of 300 wraps closed. The physical run is not scheduled in this plan | It closes the gap found in rework/34 | A team lab slot and a rule trial on the pilot |
| D7 | Recommended competition entry is A, the leaf-wrapped frozen drink with an inner barrier. B is not entered. The team submits. Claude has submitted nothing | A has the most complete evidence (rework/06) | The team decides otherwise before the 22 October 2026 deadline |
| D8 | Judge-facing material carries no team identity. Source names are fine | The competition is double-blind (memory note) | Not applicable |

**Gates (for the record, all closed as limits under section 10).** A: regulatory reply. B: dose feasibility. C: safety review. D: retention and shelf life. E: co-packer quote. F: price and demand.

**Not sourced:** durations and costs for any step. The plan contains no contact with outside parties, so no quotes are expected. Section 10 records the close-out of each step.

**Section 2 corrections.** Applied to rework/01 and rework/02 on 18 October: the Mintel link, the "daily food" preference and the "little isoflavone" statement are corrected there, and the food-route check is restated as "pass on form; open on purpose". The remaining section 2 items (Sriprasert, Maejo, Lactasoy and others) are recorded here only.
