# Risk register and implementation plan

Dated 19 October 2026. Rebuilt the same day from Singha Corporation's go decision, and corrected after an adversarial recheck. Desk model only: no bench, sensory, shelf, storage or consumer test has run, and no regulator, medical adviser or supplier has been asked. Letters in brackets point to Sources. "Gate" numbers refer to the implementation plan below.

## Risk register

| Risk | Cause | Effect | Likelihood (ASSUMPTION) | Mitigation | Owner (role) |
|---|---|---|---|---|---|
| Dissolved CO2 at the dose | The dose is 0.55 volume of CO2 per 330 mL (ASSUMPTION). Dissolved CO2 cannot exceed the dose, so the earlier rule of at least 0.6 volume dissolved after 10 minutes cannot be met at this dose (DERIVED). Solubility at 35 C is 0.592 volume [A, S, SOURCED]. | No fizz claim is supported at the chosen dose. The desk model keeps the full dose dissolved from 5 to 35 C and gives a surface-only upper bound of about 96 minutes above the threshold [I, S, abstract only, PROXY]. | High | R&D restates the pass rule and fixes the measurement method before any test (Gate 3). No fizz claim until a measured result exists. | R&D lead |
| Taste at the acid level | Citric acid is 2.10 g per 330 mL to reach working pH 3.5 (DERIVED; pH is an ASSUMPTION), about four times the 0.52 g stoichiometric amount (DERIVED). Citric acid pKa values come from a reproduced handbook table [B, S, UNVERIFIED for this proposal]. | Sourness above acceptance. Taste is untested. | Medium | Blind sensory test at pH 3.5 and either side, against the Singha Lemon Soda can as reference (Gate 4). Panel and pass rule fixed before the run. | Sensory lead (R&D) |
| Sweetness | Sucralose 33 mg per 330 mL, about 100 mg/kg (DERIVED), set by a sweetness target that is an ASSUMPTION. Sucralose is 600 to 650 times sweeter than sucrose [F, S, SOURCED]. | Too sweet, too weak, or an aftertaste. | Medium | Two or three sweetener levels inside the blind test (Gate 4). | R&D lead |
| Lead segment basis | The desk model for the lead segment rests on drinking of sugar-sweetened drinks [R, P, UNVERIFIED]. The cube contains no sugar. | The lead may not hold for a sweetener-only product. | High | The lead stays a proposal decision. The concept pre-test tests the cube itself, not a sugar-sweetened drink (Phase 2). | Marketing lead |
| Survey cannot confirm the lead | The modelled lead is about 1.2 points, and a lead of that size would need about 22,166 completes per cell. At 1,377 per cell, the test confirms the direction of the lead in 12.7 percent of simulated runs and rules out a 5-point lead in 56.4 percent of them (DERIVED from the design simulation). | The size of the lead cannot be confirmed, and a market sized on the survey would rest on an unconfirmed figure. | High | State the screening limit in advance; do not size the market from it. | Marketing lead, with executive sponsor |
| Classification and labelling | The class is open: beverage, edible ice or electrolyte drink. The flavoured-drink rows of the Thai food-additive annex allow sucralose at 300 mg/kg under condition 127 [D, P, SOURCED for the rows read]. The wording of condition 127 differs between sources. Condition TH3 covers electrolyte drinks only. | A wrong class changes the sweetener condition, the sugar rule, the label and the excise base. Sale is blocked until the class is settled. | Medium | Written Thai regulatory opinion on class, condition 127 and label before any print run (Gate 1). Label limited to composition until then. | Regulatory affairs |
| Potassium permission and serve | Potassium bicarbonate gives about 317 mg potassium per serve (DERIVED), about 9 percent of a Thai reference of 3,500 mg a day [C, S, SOURCED; primary text not opened]. Potassium bicarbonate and citric acid appear as quantum satis in the flavoured-drink rows read [D, P, SOURCED; edition check open]. Whether that covers the bicarbonate used as the acid carbonate is not settled. | A reviewer may reject the serve or require warning wording. People on potassium-retaining medicines or with kidney disease are not covered by any desk figure. Sale is blocked until the permission is confirmed. | Medium | Permission confirmed in writing, and a medical adviser's view on the serve, warning wording and at-risk groups (Gate 2). No potassium-benefit claim. | Regulatory affairs, with a medical adviser |
| Test cubes and samples | No bench cubes exist yet. Gates 3, 4 and 5 need test cubes, and the storage test needs samples. | The gates cannot run on time. | High | A bench batch of cubes at 0.55 volume is made by M2, in a laboratory or at a co-packer (Decision 4). | R&D lead |
| Moisture in the pack | Bicarbonate and citric acid react in the presence of water. No water-vapour rate is sourced and no humidity test has run. | The pouch swells, or the dose is lost before sale. | Medium | Film and seal specification, then a warm, humid storage test with stated duration and temperature (Gate 5). | Packaging R&D |
| Binder and dry-solids route | The binder is not yet named and is not priced. No dry-solids, compaction or pouch-sealing capability is evidenced at any group company. | No route to make the cube at scale, and its cost is not known. | High | Name the route: own line, co-packer or pilot run (Gate 6). Answer whether the reactants hold without a binder. | Operations director |
| Food-safety certificate | Food-safety standards are claimed. No certificate is verified for any site (UNVERIFIED). | No pilot batch can be released. | Medium | Verify a certificate on a public register for the named site and legal entity (Gate 6). | Quality assurance |
| Patent and freedom to operate | A European publication (EP 4,516,115 A2) and a US patent (US 5,254,355 A) were found, and neither has been checked for legal status [P, SOURCED; status unchecked]. | A freedom-to-operate problem could stop a launch. | Medium | Freedom-to-operate view by a patent attorney before any pilot batch (Gate 7). | Brand and legal |
| Pouch and print cost | The pouch is THB 1.30 (ASSUMPTION). A non-Thai listing of USD 0.03 to 0.05 (S, PROXY, UNVERIFIED; no link saved) gives THB 1.01 to 1.68 at 33.55 baht per dollar [O, P, SOURCED]. The THB 0.67 to 2.70 band is an ASSUMPTION built on USD 0.02 to 0.08 snippets. The listing has a minimum order of 1,000 pieces. Print THB 1.50 and processing THB 0.50 are ASSUMPTIONS. The THB 4 six-cube carton is scaled from a twelve-cube listing (ASSUMPTION); pro rata it would be THB 2.50 (DERIVED). | Pouch, print and processing are about 96.5 percent of the cost before carton (DERIVED). The six-cube cost is THB 4.09 per cube and the twelve-cube cost THB 3.84 (DERIVED). Both exclude binder, filler and lemon flavour, which are not priced. | High | Thai quotes requested only after Singha Corporation approves outreach (Gate 5). Quotes are tested against the THB 3.51 floor on the six-cube pack. | Procurement lead; finance lead |
| Excise base | Item 02.02 of the sugar-drink excise schedule, in the saved notice, sets four sugar bands (0, 1, 3 and 5 baht per litre) with 14 percent ad valorem in each row [P, SOURCED]. Later periods exist and are not verified. The value base has not been read. | Unbudgeted tax or a price error. | Medium | Tax adviser's view once the class is settled (Gate 1). The price model excludes excise until then. | Finance lead; tax adviser |
| Brand and legal sign-off | The lion and the SINGHA name are authorised for this proposal only, which is not a licence. Brand-owner and legal sign-off sit with the SINGHA mark holder's brand department and are not held. The alcohol-cue question is unchecked. | No emblem, name or campaign use without written sign-off. An alcohol cue could block the product or the campaign. | Medium | No artwork, creative, stimulus, sampling material or paid media is released before written sign-off (Gate 7). | SINGHA mark holder's brand and legal department |
| Name clearance | "Lemon Soda" has no register search. The one web search so far does not reach the Thai register. The name is the same as the printed flavour name "Lemon Soda" on the company's Singha Lemon Soda product page (tier S). | A name conflict forces a rename after print or launch. | Medium | Register search including the Thai register. A neutral placeholder name is used in test and sampling copy until cleared (Gate 7). | Brand and legal |
| Competitor overlap on flavour | The Singha Lemon Soda can is the comparison product: a 330 ml can, listed on the company product page (tier S); retail sale not dated [J, S, SOURCED]. Its price is not verified. Lemon Soda overlaps it on flavour. The can's own claims are not checked here, and Lemon Soda makes no sugar or calorie claim. | Cannibalisation of the can, and shopper confusion between a cube and a can. | Medium | Points of difference kept plain: a dissolvable cube made in the glass, one cube per pouch, against a ready-to-drink can. A shopper comparison with the can runs in the pre-test once a checked visual of the can exists. Cannibalisation is reviewed when 50 percent or more of buyers say they switched (Phase 5). | Marketing lead |
| Paid-media return | The desk model finds that paid social alone does not recover its first-purchase cost in one serve (DERIVED on PROXY and ASSUMPTION inputs). | Media spend without a return, and the pilot budget is spent before the read. | High | No paid media until the click-to-purchase read reaches the threshold Singha Corporation sets (Decision 10; Gate 8). | Marketing lead; finance lead |
| Budget not reconciled | Marketing and pilot costs sit outside the unit economics and the valuation base at THB 500,000 a year fixed cost. | A plan the fixed-cost base cannot carry. | Medium | Singha Corporation sets one campaign and pilot budget, in one currency unit, inside the fixed-cost grid (Gate 8). | Finance lead |
| Listing and channel | No channel is chosen. Listing gatekeepers and fees are not named. Retailer margin of 25 to 35 percent and distributor margin of 10 to 20 percent are ASSUMPTIONS. | Pilot routes fail to list, or margins erode the 60 percent ex-factory share. | High | Pilot channel decided at Gate 8, and margins quoted before the budget is set. | Sales and channel management |
| Pack release data | Net weight is left unprinted until a cube is weighed. The central dry cube is 3.79 g and the packed unit 5.29 g with a 1.5 g pouch (DERIVED on ASSUMPTION inputs). The shelf-life line needs stored samples. | A label printed with unmeasured figures. | Medium | Net weight printed only from weighed cubes, and shelf life only from the Gate 5 storage result (Gate 9). | Packaging R&D |

## Implementation plan

The plan starts at M0, Singha Corporation's go decision on this proposal. The evidence does not date M0, so every duration is an ASSUMPTION for Singha Corporation to set. No step, quote, test, sign-off or outside contact has happened. Each needs Singha Corporation's written approval first. The plan follows the strategy in section 04 (the lead segment is men aged 25 to 34, with men aged 45 to 59 a later volume segment, and the proposition is form, not flavour) and the gates, KPIs and kill criteria in section 06.

### Starting point

| Area | Status | What the evidence shows |
|---|---|---|
| Comparison product | Partly evidenced | The Singha Lemon Soda can is listed on the company product page (tier S); retail sale not dated [J, S, SOURCED]. Its price is not verified, and the can itself has not been seen. |
| Carbonation and can filling | Evidenced for cans; unknown for the cube | The Singha Lemon Soda can is listed on the company product page (tier S); retail sale not dated. Group carbonation capacity and the can's filler are not shown. |
| Dry powder, compaction and pouch sealing | Unknown | No line, capacity or site is shown at any group company. |
| Food safety | Claimed | Standards are claimed. No certificate is verified for any site. |
| Product class and sweetener | Partly evidenced | Sucralose is permitted at 300 mg/kg in the flavoured-drink rows read [D, P, SOURCED]. The class is open, and sale is blocked. |
| Consumer and channel | Unknown | No shelf, price, sales or consumer test of Lemon Soda has run. |
| Brand and legal | Assumed | The lion and SINGHA are authorised for this proposal only. Sign-off sits with the SINGHA mark holder's brand department and is not held here. |
| Budget | Unknown | No campaign or pilot budget exists. The valuation rests on assumed volumes. |

### Phases

| Phase | Timing (ASSUMPTION) | Opens when | Exits when |
|---|---|---|---|
| 0. Mobilise | M0 to M1 | Go decision | Owners and gate dates named; route for outside contact agreed |
| 1. Readiness gates | M1 to M5 | Phase 0 exits | Gates 1 to 7 passed |
| 2. Concept pre-test | M3 to M5 | Panel approved, and the stimulus signed off under Gate 7 by M3 | Pre-test read against the decision rule fixed in advance; no media and no sale |
| 3. Pilot readiness | M5 to M7 | Gates 1 to 7 passed | Gates 8 and 9 passed; stock placed in pilot routes |
| 4. Marketing pilot | M7 to M10 (13 weeks of trading) | Gates 8 and 9 passed, and the Phase 2 read is in | 13 weeks elapsed; 90-day sell-through read taken |
| 5. Measured decision | M10 to M11 | Pilot ends, plus two weeks | One of: scale one route, repeat once in the same stores, or stop |
| 6. Scale | From M13 for national listing | Measured decision says scale, and the six-month listing count is read (about M13) | One route at a time, against the stop and scale table |

A gate that fails inside its window blocks the step it controls. The dose or the acid is reworked once within the window, the change is written down, and the gate runs again. A second failure stops that format.

Sale is blocked until Gates 1, 2, 7 and 9 pass. A pilot batch also needs Gates 3 to 6 and 8.

### Gates

| Gate | Must show | Pass test | Owner (role) | Status now |
|---|---|---|---|---|
| 0. Go and owners (M0 to M1) | Written go decision; executive sponsor; one owner per gate with a date; route for outside contact | Owners and dates named within four weeks of M0 (ASSUMPTION) | Executive sponsor | Not held |
| 1. Class and sweetener (M1 to M3) | Written Thai regulatory opinion on class; condition 127 wording; annex edition checked against the B.E. 2568 clarification [E]; all sub-category rows of the sucralose permission; sodium check on binder, filler and flavour | Class settled in writing; no applicable row sets a limit below the design level of about 100 mg/kg (DERIVED) | Regulatory affairs | Class open; flavoured-drink rows read; edition check open |
| 2. Potassium permission and serve (M1 to M4) | Permission for potassium bicarbonate as the acid carbonate confirmed in writing; medical adviser's view on about 317 mg potassium per serve, on people on potassium-retaining medicines or with kidney disease, and on warning wording | Permission confirmed; the adviser does not reject the serve; the adviser sets any warning. The threshold is open until the adviser reports | Regulatory affairs, with a medical adviser | Permission not yet confirmed; no adviser sought |
| 3. Dissolved CO2 (M2 to M5) | Bench cubes at 0.55 volume made by M2; a restated pass rule; measurement at 5, 20 and 35 C with a named runner and method; pass sheet fixed before the run | Result read against the restated rule. The rule's number is set by R&D before the run and is open until then. One rework allowed inside the window | R&D lead | No measured value; desk model only |
| 4. Taste (M2 to M4) | Blind sensory test at pH 3.5 and either side, with two or three sweetness levels and the Singha Lemon Soda can as reference; panel size, provider, control and pass rule fixed in advance; panel approved by Singha Corporation | At least 55 percent blind preference at pH 3.5 (ASSUMPTION) | R&D, with consumer insight | Untested |
| 5. Pack, storage and quotes (M2 to M5) | Film and seal specification (antimony-free PET carried forward; sealant and any barrier layer still to be specified); storage test at 35 C for 8 weeks (ASSUMPTION), started by M2; Thai quotes requested only after approval | In-pack reaction at most 0.5 percent of the bicarbonate at 35 C (ASSUMPTION), with seals intact; contribution at least THB 3.51 per cube on six cubes after quotes (DERIVED floor) | Packaging R&D, with procurement; finance | No specification, test or quote. The pouch price of THB 1.30 is an assumption |
| 6. Route and food safety (M2 to M5) | A named plant or co-packer for dry solids and pouch sealing; a site certificate verified on a public register for that site and legal entity; certificates of analysis for each ingredient; an answer on whether the reactants hold without a binder | One route named, with a verified certificate for that site | Operations director, with quality assurance | No dry-solids or sealing capability evidenced; certificates claimed, none verified |
| 7. Brand, name and copy (M1 to M5) | Written brand and legal sign-off for the lion and SINGHA beyond this proposal; rulings on alcohol cues, glassware, bubbles and lemon imagery; stimulus sign-off by M3; register search for Lemon Soda including the Thai register; freedom-to-operate view by a patent attorney; Thai legal review of advertising and sample labelling | Written sign-off before any artwork, creative, stimulus, sampling material or paid media. Stimulus sign-off by M3 opens Phase 2 | SINGHA mark holder's brand and legal department | Name search not run; sign-off not held |
| 8. Pilot design and budget (M4 to M6) | Pilot routes, store count and location, duration and volume; listing fee and margins; one budget in one currency unit inside the fixed-cost grid; cost-per-first-purchase threshold; click-to-purchase threshold and traffic source; cohort, sell-through and cannibalisation rules; the pouch minimum order set against pilot volume | Each parameter written and approved by Singha Corporation. The figures themselves are Singha Corporation's decisions (Decisions 8 to 11) and stay open until then | Sales and channel management, with marketing; finance | Channel not chosen; no budget; margins are assumptions |
| 9. Pack release (M5 to M7) | Net weight from weighed cubes; shelf-life line only from the Gate 5 storage result; Thai particulars completed (sweetener name, ingredients, manufacturer); every printed figure tiered, dated and sourced | Printed figures come from weighed and tested samples, with written sign-off on the pack. If the storage result is not complete, no shelf life is printed | Packaging R&D, with regulatory affairs | Placeholders remain for shelf life, ingredients and manufacturer. The net weight is a 3.8 g specification, verified by weighing before print, and the sweetener is sucralose (working choice) |

### Workstreams

Owners are roles. Each workstream starts when Gate 0 names its owner.

| Workstream | Owner (role) | First 90 days | Depends on |
|---|---|---|---|
| Formulation and R&D | R&D lead, with sensory lead | Make bench cubes at 0.55 volume by M2 (Decision 4 sets where). Restate the dissolved-CO2 pass rule and fix the method (Gate 3). Name the binder, filler and flavour and check each for sodium. Fix the blind taste design (Gate 4). | Decisions 1, 4 |
| Regulatory and brand | Regulatory affairs head, with brand and legal | Class opinion, condition 127 wording and annex edition check (Gate 1). Potassium permission and medical view (Gate 2). Stimulus sign-off by M3, freedom-to-operate view and register search (Gate 7). Rulings on the lion, SINGHA, alcohol cues, glassware, bubbles and lemon imagery. | Decisions 2, 3, 7 |
| Packaging and sourcing | Packaging R&D lead, with procurement | Film and seal specification, and the storage test started by M2 (Gate 5). Quote request prepared, and sent only on approval. | Decisions 3, 6 |
| Manufacturing route | Operations director, with quality assurance | Map dry-solids and sealing capability across group sites and co-packers. Verify certificates for the named site (Gate 6). | Decision 5 |
| Marketing and channel | Marketing lead, with sales and channel management | Brief creative within the message rules. Build the stimulus with no glassware, lemon wedge or alcohol cue until the Gate 7 rulings. Set the pre-test fieldwork plan (Phase 2). Compare pilot routes A and B. Name the traffic source for the click-to-purchase read (Gate 8). | Gate 7; Decisions 3, 8, 10, 11 |
| Finance and governance | Finance lead, with executive sponsor and tax adviser | Owners and dates for each gate (Gate 0). One budget inside the fixed-cost grid (Gate 8; Decision 9). Replace assumed volumes with Singha Corporation's data. Excise base once the class is settled (Gate 1). | Decisions 1, 9 |
| Source and claim control | Marketing lead, with legal | Tier, date and saved-source check on every printed or pitched figure. Save page text for the PROXY inputs. Strike or label any figure that cannot be traced to its original within 48 hours. | Before any print, sampling or copy goes out |

## Marketing campaign

**Segment.** Men aged 25 to 34 are the proposed lead segment. That is a proposal decision, not a consumer finding. The desk model puts the gap between men aged 25 to 34 and men aged 35 to 44 at a median of about 0.6 to 1.2 points at a 30 percent baseline, depending on the model scale (0.6 on the odds scale and 0.9 on the share scale in the age-band model; 1.2 in the survey power simulation). On the odds scale its 90 percent interval at a 30 percent baseline runs from minus 0.03 to 1.39 points, so it includes zero (DERIVED from a desk model with unsourced inputs). The model rests on drinking of sugar-sweetened drinks, and the cube contains no sugar, so transfer to a sweetener-only product is untested. The drinking shares for men aged 25 to 44 and 45 to 59 are 68.6 and 65.4 percent [R, P, UNVERIFIED]. Use of sugar-substitute drinks is 0.6 percent at ages 25 to 44 and 1.0 percent at ages 45 to 59 [S, P, UNVERIFIED; the survey's column definition is to be checked before any figure is printed]. The survey does not split ages 25 to 34 from 35 to 44; that split is modelled. Men aged 45 to 59 are a later volume segment and are pended.

**Concept pre-test (Phase 2; no media, no sale).** A recruited online concept test, run only after Singha Corporation approves a provider and budget (Decision 3). Screen: men resident in Thailand aged 25 to 59 who drank alcohol in the past 12 months and had a drinking occasion in the past three months. Exclude people working in beverage, alcohol, food retail, advertising and research, and anyone in a beverage concept test in the past six months. Cells: ages 25 to 34 and 35 to 44, with 45 to 59 as reference. Stimulus: one brand-blind concept, text and image, showing the mechanism only, and signed off under Gate 7 by M3. The earlier concept image is withdrawn; no glassware or wedge appears in the track 1 concept until the Gate 7 rulings. Primary measure: top-two-box purchase intent by cell. Secondary: one price of 15 baht, against the Singha Lemon Soda can (price not verified); occasion incidence; open-text comprehension, with health, diet and sugar mentions flagged; reaction to the sweetener disclosure; attention check.

Decision rule, fixed before the run. The lead is supported if the lower bound of the 95 percent interval on men aged 25 to 34 minus men aged 35 to 44 is above zero. It is reversed if the upper bound is below zero. Otherwise it is undetermined. The pre-test reads direction and size under the interval rule set out in Appendix C, and the five-point rule is applied as stated there. About 1,377 respondents per cell give 80 percent power to detect a five-point gap against zero (DERIVED). Under the five-point rule, the lower bound must reach five points, which at that sample needs an observed gap of about 8 points (DERIVED from the design's interval).

**Message rules (all phases).** Allowed: "Drop one cube into 330 ml of water and stir"; "Serving: one cube made up to 330 ml"; "Single-serve pouch"; "Contains an intensive sweetener: sucralose (working choice; the Gate 1 regulatory opinion is to confirm it)". The working name is used only after Gate 7 clears it; until then a neutral placeholder is used. Potassium may appear as a composition fact; any amount or warning waits for Gate 2.

Barred with no clearance route: sugar-free, zero-sugar and no-added-sugar wording; sodium-free and low-sodium wording; health, function, electrolyte, hydration and potassium-benefit wording; calorie wording; certification and award wording, since none is verified.

Held until the Gate 7 rulings or a Thai legal review: novelty words; fizz, sparkling, bubbles and CO2-release wording, until a measured test exists; lemon fruit imagery and "made with real lemon"; glassware and bottle shape; alcohol cues; the company's taglines and campaign artwork; the lion or SINGHA without written sign-off; recyclable or plastic-free claims. No novelty claim is made until a Thailand-only shelf and novelty audit is complete. All copy is checked against these lists before any media, sampling or listing text goes out.

**Pilot (Phase 4; 13 weeks of trading; ASSUMPTION).** Two routes run in the same window against one budget set at Gate 8.

- *Step 1, click-to-purchase read (first four weeks).* A product page or listing with a trial offer and a price. No paid media is bought until the read reaches the click-to-first-purchase rate Singha Corporation sets (desk base 1.0 percent, ASSUMPTION). Traffic comes from non-paid sources Singha Corporation names (Decision 11): its existing channels, in-store or a listing.
- *Route A, in-store trial in pilot stores.* At least 3 units per store per week (ASSUMPTION; section 06 benchmark). Cost per sample THB 15 (range 10 to 25; ASSUMPTION), sample-to-trial rate 10 percent (range 5 to 20; ASSUMPTION). A cost per trial of about THB 150 is a floor that excludes listing fees, trade spend, distribution and shelf costs, none of which is sourced.
- *Route B, paid social to one online listing (Facebook and Instagram).* Cost per click THB 11.5 [Q, S, SOURCED, PROXY; one agency's 2025 figure]. Cost per thousand impressions THB 120 is an ASSUMPTION with no saved source. Click-to-first-purchase 1.0 percent (ASSUMPTION). A desk simulation gives a median cost per first purchase of about THB 915 (DERIVED on PROXY and ASSUMPTION inputs); at base inputs it is about THB 1,150. At THB 4.91 contribution per cube on the six-cube pack, recovery takes about 234 cubes per buyer (DERIVED), so paid social alone does not pay back in one serve. Route B starts only after Singha Corporation sets the threshold (Decision 10).
- *Both routes.* Repeat target 30 percent, floor 15 percent (ASSUMPTION; bounds 15 to 40 percent), read on two cohorts at 8 and 12 weeks. Sell-through of at least 60 percent of placed stock within 90 days (ASSUMPTION; no source). Listing with at least two national retail gatekeepers within six months of pilot start, which falls about M13 (ASSUMPTION). Cannibalisation review when 50 percent or more of buyers say they switched from the Singha Lemon Soda can (ASSUMPTION).

**Measured decision (Phase 5).** Both routes are read against this section and the stop and scale table, using the repeat and sell-through reads taken so far and the listings in progress. The outcome is one of three: scale one route; repeat once in the same stores with the same cohorts; or stop.

**Scale (Phase 6).** One route at a time, and only when repeat holds at 15 percent or more on both cohorts, contribution holds at THB 3.51 or more per cube on the six-cube pack, and the cannibalisation review is passed or explained. National scale also needs the six-month listing count (two gatekeepers) and sell-through on track at about M13. Volume is set from measured sell-through, not from the base volume of 200,000 cubes a year (ASSUMPTION). On the six-cube cost the shelf price at which contribution is zero is about THB 6.82 (DERIVED: THB 4.09 divided by the 60 percent ex-factory share). Break-even at a fixed cost of THB 250,000 a year is about 73,000 cubes a year, and at THB 500,000 about 146,000 cubes a year (DERIVED at a 10 percent rate). At 50,000 cubes a year, the case is negative at every fixed cost in the grid (DERIVED).

**Budget.** Marketing and pilot costs are outside the unit economics and the valuation base until Gate 8 sets one budget, in one currency unit, inside the fixed-cost grid (Decision 9).

## Stop and scale decisions

Thresholds are ASSUMPTIONS unless the tier column says otherwise. Rows marked "proposed addition" are not yet in section 06; this plan adds them, and they need the same sign-off as the rest of section 06.

| Trigger | Threshold | Tier | Action |
|---|---|---|---|
| Sweetener | Neither sucralose nor steviol glycosides permitted for the class | P for the flavoured-drink rows read | No sale. Steviol glycosides are the named fallback to check (their 115 mg/kg row is not yet read [D, P, UNVERIFIED for this row]) |
| Dose and fizz | Restated pass rule not met at 0.55 volume, with the method fixed before the run | ASSUMPTION | One rework of dose or acid inside the window, written down. A second failure stops the format (proposed addition: section 06 currently stops at the first failure) |
| Taste | Blind preference below 55 percent at pH 3.5 | ASSUMPTION | One acid and pH reset, then stop |
| Pack | In-pack reaction above 0.5 percent of the bicarbonate at 35 C | ASSUMPTION | No launch until the barrier or seal changes |
| Potassium | A reviewer rejects the serve of about 317 mg | DERIVED from a secondary reference; no threshold set | No sale |
| Food safety | No verified certificate for the named site (proposed addition) | UNVERIFIED | No pilot batch |
| Economics | Contribution below THB 3.51 per cube on six cubes, or repeat below 15 percent on two cohort reads | DERIVED; ASSUMPTION | Stop scale-up. Re-specify the pack or carton before any further pilot batch |
| Velocity | Below 3 units per store per week on two consecutive reads (proposed addition as a stop) | ASSUMPTION (benchmark in section 06) | Stop expanding that route; review |
| Sell-through | Below 60 percent of placed stock within 90 days | ASSUMPTION; no source | Review listings and store mix. Not a stop |
| Segment | The pre-test lower bound is not above zero and the upper bound is below zero (proposed addition) | Rule fixed before the run | Singha Corporation's sponsor decides the lead segment. No lead-segment media until then |
| Cannibalisation | 50 percent or more of buyers switched from the Singha Lemon Soda can | ASSUMPTION | Positioning review. Not a stop |
| Paid social | No cost-per-first-purchase threshold set before media (proposed addition) | Proposal | Route B does not start |
| Claims and brand | Barred wording used, or the lion or SINGHA used without written sign-off (proposed addition) | Message rules | Copy, artwork or media stopped until cleared |
| Source | Any printed or pitched figure without a tier, date and saved source (proposed addition) | Source rule | Struck, or labelled UNVERIFIED, before print |

## Decisions owned by Singha Corporation

Each decision has a proposed owner role and the point by which it is needed. Dates are relative to M0.

1. **Go decision and owners.** Approve this plan as the basis for a go decision at M0. Name the executive sponsor, one owner per gate with a date, and the entity that signs each gate decision (Singha Corporation, or the SINGHA mark holder for brand gates). Owner: executive sponsor, at M0. Unblocks Phase 0.
2. **Product class.** Choose beverage, edible ice or electrolyte drink, and commission the written Thai regulatory opinion. Owner: regulatory affairs head, by M1. Unblocks the sale, the label, the sweetener condition and the excise base.
3. **Outside contact.** Approve each contact separately, with a named provider and budget: regulatory opinion, medical adviser, tax adviser, laboratory, Thai quotes, taste panel, concept panel, patent attorney, co-packers and store visits. Owner: executive sponsor, by M1. Unblocks Gates 1, 2, 4, 5, 6 and 7, and Phase 2.
4. **Bench cubes and dissolved-CO2 method.** Decide where the bench cubes are made (a laboratory or a co-packer), whether the dissolved-CO2 test is measured or only simulated, who fixes the restated pass rule, and whether the 0.55-volume dose stays after one rework. Owner: R&D lead proposes; executive sponsor decides; by M1. Unblocks Gates 3, 4 and 5.
5. **Dry-solids route.** Choose an own line, a co-packer or a pilot run, and name the filler and the legal entity for the site. Owner: operations director, by M2. Unblocks Gate 6 and the pilot batch.
6. **Sold unit and carton.** Confirm one cube per pouch, which is inferred and not yet confirmed. Choose a six-cube (recommended), twelve-cube or twenty-four-cube carton. Owner: marketing lead, with finance, by M2. Unblocks artwork, quotes and the price model.
7. **Brand and legal rulings.** Rule on the lion and SINGHA beyond this proposal, on alcohol cues, glassware, bubbles and lemon imagery, and on whether the name proceeds after a register search. Owner: SINGHA mark holder's brand and legal department, by M2. Unblocks artwork, the stimulus and all media.
8. **Pilot routes.** Choose the routes, store count and location, duration and volume. Owner: sales and channel head, by M4. Unblocks Gate 8.
9. **One budget.** Set one campaign and pilot budget, in one currency unit, inside the fixed-cost envelope. Owner: finance lead, by M4. Unblocks media and listing spend.
10. **Paid-social threshold.** Set the cost-per-first-purchase threshold, cohort windows, sell-through rule and cannibalisation response before any paid media is bought. Owner: marketing lead proposes; finance lead decides; by M4. Unblocks Route B.
11. **Traffic for the click-to-purchase read.** Name the source: existing channels, in-store, or a listing. Owner: marketing lead, by M4. Unblocks pilot step 1.
12. **Segment reading.** State, before fieldwork, which direction of result keeps men aged 25 to 34 as the lead: above zero, below zero, or undetermined under the rule. Owner: executive sponsor, before fieldwork (about M3). Unblocks the pilot segment.

## Validation plan: concept survey on Singha Corporation

The survey is a brand-blind concept test of the lemon cube, run for Singha Corporation as proposer. Track 1 (brand-blind) can run first. Track 2 (brand-named) waits for Gate 7. Men are split into three cells: aged 25 to 34 (the lead), aged 35 to 44 (comparison) and aged 45 to 59 (descriptive only). The primary outcome is top-two-box purchase intent, a proxy for purchase.

At 1,377 completes per cell, the test screens for a 5-point lead at a 30 percent baseline. The modelled lead is about 1.2 points, which would need about 22,166 completes per cell. At 1,377 per cell, the test confirms the direction of the lead in 12.7 percent of simulated runs and rules out a 5-point lead in 56.4 percent of them (DERIVED from the design simulation). The recommended decision rule is the 95 percent interval rule, for Singha Corporation to approve.

Preconditions before fieldwork: Gate 1 passed; Singha Corporation's approval of the panel provider and budget (Decision 3); stimulus inputs set and signed off under Gate 7; and the consent notice checked under the Thai Personal Data Protection Act (PDPA). No outside contact, quote or fieldwork has happened. The full design is in Appendix C.

## Limits

- No calendar date is in the evidence, so M0 is not dated. Every duration and threshold marked ASSUMPTION is a proposal for Singha Corporation to accept or change.
- The lead segment rests on drinking of sugar-sweetened drinks. Transfer to a sweetener-only product is untested. The split between ages 25 to 34 and 35 to 44 is modelled, and the drinking and sugar-substitute figures are UNVERIFIED because the printed pages were not checked.
- The pre-test reads direction and size under the interval rule in Appendix C. It cannot confirm the size of the lead at the sample it can afford.
- No dry-powder, compaction or pouch-sealing capability is evidenced at any group company. Singha Corporation's own cost, supply, capacity, line and innovation-budget data were not available to the team. The number of group manufacturing companies differs by source (eight or nine), and no plant is named for the cube.
- No bench cubes exist yet. Taste, dissolved CO2, storage and sweetness are untested, and no measured value exists. The earlier fizz rule cannot be met at 0.55 volume, and its restatement is not yet set.
- Sale is blocked until Gates 1, 2, 7 and 9 pass. The class is not settled. The potassium bicarbonate permission is not confirmed, and sucralose sub-category rows other than the flavoured-drink rows have not been read. Condition 127 wording differs between sources ("as ready to drink" in the annex text, "as consumed" in earlier wording); the regulatory opinion settles it.
- The 3,500 mg Thai potassium reference rests on secondary copies, and the primary text has not been opened. The 317 mg per serve (about 9 percent) depends on it. People on potassium-retaining medicines or with kidney disease are not covered by any desk figure.
- The pouch price of THB 1.30 is an ASSUMPTION. The THB 0.67 to 2.70 range is an ASSUMPTION built on snippets, and the non-Thai listing it draws on is UNVERIFIED. The THB 3.51 floor is derived from the assumed THB 2.70 upper price. No Thai quote has been requested, and no pouch maker has been identified.
- Binder, filler and lemon flavour are neither priced nor checked for sodium, and the binder is not named. Contribution of THB 4.91 per cube on six cubes (DERIVED) excludes them.
- Excise: the 14 percent ad valorem rate applies if the value base applies. The base has not been read, and the price model excludes excise.
- The lion and SINGHA name are authorised for this proposal only. That is not a licence, and brand-owner and legal sign-off is not held. Lemon Soda has no register search, and no freedom-to-operate view exists for the patent publications found.
- The Singha Lemon Soda can's own claims, including its sugar and calorie wording on the product page, are not checked here. The can has not been seen, and its ingredient list and nutrition panel are not in the evidence.
- No consumer, shopper, price or channel test of Lemon Soda has run.
- The paid-social inputs are PROXY values or ASSUMPTIONS. No marketing result exists.
- No campaign creative, media plan, flight dates, Thai advertising rules, platform ad policy, food-labelling rules for samples or marketplace rules have been reviewed. Gate 7 covers the review.
- No pilot budget, campaign budget or sampling quote exists. Marketing costs are outside the valuation base until Gate 8.
- No Thai retailer or distributor margin has been found, and listing fees are not sourced.
- No outside contact, quote, sign-off, test or registration has taken place.

## Tiers

Tiers are defined once, in Appendix A.

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

J. Singha Lemon Soda company product page (tier S): a 330 ml can; sucralose and acesulfame potassium named as sweeteners; listed on the company product page; retail sale not dated. Price not verified. https://www.singhacorporation.com/singhalemonsoda/th/ S, SOURCED.

K. Overseas analogue: Ricola Drink Cubes press release, dated 5 June 2025. https://www.ricola.com/en/about/press-releases/ricola-brings-a-new-product-to-the-market/ P, SOURCED.

L. Desk model results, the proposal's own arithmetic, with no external source. Arithmetic only; DERIVED.

O. Bank of Thailand, US dollar buying and selling rates, 15 October 2026. The midpoint of 33.55 baht per dollar is DERIVED from the two rates. https://www.bot.or.th/en/statistics/exchange-rate.html P, SOURCED.

P. Royal Gazette, B.E. 2560 (2017), sugar-drink excise schedule, item 02.02. https://www.ratchakitcha.soc.go.th/DATA/PDF/2560/A/095/111.PDF P, SOURCED.
Q. Phoenix Media, Thai advertising costs for 2025 (Facebook cost per click, THB 11.5; one agency's figure), 3 February 2026. https://www.phoenixmedia.co.th/the-costs-of-facebook-google-and-line-ads-in-thailand-for-2025/ S, SOURCED; PROXY.
R. National Statistical Office, Social Indicators 2025, Table 4.6.2 (drinking shares for men by age, 2024): https://www.nso.go.th/public/e-book/Indicators-Social/Social-Indicators-2025/284/ P, UNVERIFIED; the printed page has not been checked.
S. National Statistical Office, Health Behaviour Survey 2021, tables 20 and 22 (use of sugar-substitute drinks by age); no URL saved. P, UNVERIFIED; the survey column definition is to be checked.

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
- J: capture 48, an extract (a WebFetch summary, not raw page text; no raw save exists), 48_singha-lemon-soda-th.md
- K: capture 46, 46_ricola-drink-cubes-release.md
- L: handover_figures_results.json (desk model arithmetic, no public URL)
- M and N (no longer cited in the body, because the Singha Sparkling Water Lime Flavour is a different product from the comparison can): capture 86, 86_singha-sparkling-lime-press-release-nation.md; capture 87, 87_singha-sparkling-lime-article-kaohoon.md
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

Changes in this pass (19 October 2026, implementation rebuild):

- The competition-calendar plan ("no step starts before the competition ends") is replaced by a plan that starts at Singha's go decision (M0). It has Gates 0 to 9, phases, workstreams, a marketing campaign, a stop and scale table, and twelve decisions for Singha.
- Method: five evidence readers (readiness; strategy, KPIs and gates; marketing; the old strategy-folder discussion; judge-facing constraints), two planner drafts from different lenses, one synthesis, and one adversarial check that returned 31 findings. Every high and medium finding was applied to the text above, or is stated as a limit.
- The old workspace discussion is taken as the strategy folder (strategy/), read item by item. Kept: capability labels; bench and blind taste tests with the 55 percent rule; certificate and register checks; co-packer enquiries, restated for dry solids and sealing; pilot velocity and listing thresholds; distributor margin; claim limits; the source rule; decision owners; a named fallback. Dropped as competition-only: the 21 and 22 October dates, the 20 October primary choice, the 19 October and 5-day bench window, the mentor and plant-tour dependency, the brief's 20 percent test, and the export, Singapore, Korea and China items. A search of the whole workspace found no other "Singha" document, so no file named "Singha (1).docx" was used.
- The proposing strategic plan is taken as section 04 (strategy) and section 06 (KPIs and kill criteria), read in full.
- Conflicts the user must settle, all stated in the text above:
  1. The fizz rule. The earlier pass rule (0.6 volume dissolved at 10 minutes) cannot be met at a 0.55-volume dose, because dissolved CO2 cannot exceed the dose (record 52, O1). Section 06 still states the rule. Gate 3 restates it.
  2. The bench test. The record that drops the laboratory test (record 45, S2, 18 October) conflicts with this plan's measured test. Decision 4 settles it.
  3. The lead segment. The strategy's working-adult sample (ages 25 to 40, record 14 and record 12) conflicts with the record's men aged 25 to 34 lead (records 46 and 60). This plan uses the record's lead.
  4. The budget. The THB 500,000 a year fixed-cost base (valuation) does not reconcile with a campaign and fixed line of THB 15 to 20 million a year in the older projection (rework/screen/financial_projection.py, line 153). Decision 9 sets one figure.
  5. The package file (record 57) still carries the 1.75-volume design: reactants of 4.23 g, a design mass of 5.28 g, and "Net weight: 5.3 g" printed on the front band, back band and the 3D page. Record 64 withdraws these figures. Check the judge folder's label and 3D page before the stage.
  6. The sold unit (one cube per pouch) is an inference, shown as Decision 6.
- Figures corrected in this pass: the pilot recovery uses the six-cube contribution of THB 4.91 (about 234 cubes), not the twelve-cube basis (177 to 223 cubes); the pre-test sample sizes are the design's own (1,377 per cell at 5 points; 22,166 at 1.23 points; about 33,500 for one point, DERIVED from the design's power formula); the pre-test uses one team price, as the design specifies, not a three-price ladder; the excise row reads the saved notice (four sugar bands; 14 percent in each row); the carton share of THB 0.67 is marked as an ASSUMPTION, since the listing it was scaled from does not reproduce it; the break-even shelf price on the six-cube cost is about THB 6.82.
- Sources: the Facebook cost-per-click figure is S, PROXY (source Q). The drinking and sugar-substitute survey figures are P, UNVERIFIED because the printed page was not checked (source R). The cost per thousand impressions of THB 120 has no saved source and is UNVERIFIED. The 7-Eleven store count is not used, because the saved page is not held.
- Not yet done: the judge-facing files named in the change list (executive summary, handover and proposal files 01 to 09) are updated only where they state the plan, timing or gates. Repository references and internal labels inside judge-facing body text in files 01, 02, 03, 04, 05, 07 and 09 are a separate clean-up and are listed for the next pass.

Changes in this pass (19 October 2026, recheck fixes):

- Sale-blocking gates are now the same in the plan and the Limits: sale is blocked until Gates 1, 2, 7 and 9 pass; a pilot batch also needs Gates 3 to 6 and 8.
- The storage test starts by M2 with an assumed eight-week duration, so its reaction result is in by M5. Gate 9 takes the shelf-life line from that result.
- The five-point rule is removed as a decision criterion. The pre-test decides direction only, and 80 percent power applies to the zero test only.
- The lead's basis (sugar-sweetened drinking) is stated in the segment paragraph, the risk register and the Limits.
- A bench-cube step is added before M2, and Gates 3, 4 and 5 depend on it.
- The potassium permission is restated: the flavoured-drink rows read list potassium bicarbonate and citric acid as quantum satis, and whether that covers the bicarbonate as acid carbonate is open (Gate 2).
- Phase 2 opens on a stimulus sign-off under Gate 7 by M3. Phase 6 national scale waits for the six-month listing count, about M13.
- The four proposed additions (segment, paid social, claims and brand, source) are marked in the stop table. Section 06 still needs them added to its kill list.
- The pouch band of THB 0.67 to 2.70 is attributed to USD 0.02 to 0.08 snippets as an ASSUMPTION, and the THB 3.51 floor to the assumed THB 2.70 upper price. The USD 0.03 to 0.05 listing gives THB 1.01 to 1.68.
- Segment shares: the drinking shares cite Social Indicators 2025, Table 4.6.2 (source R, with URL). The sugar-substitute figures cite Health Behaviour Survey 2021 (source S, no URL). "Everyday" is removed.
- Potassium is printed as about 9 percent of the reference (317 mg). The 96.5 percent share is restated against the cost before carton.
- Decision 1 is due at M0; Gate 0 allows four weeks after M0.
- Open for the team: section 06 needs the four proposed additions; the executive summary and the deck's footnote on potassium were updated separately; the at-risk groups for potassium are added to the Limits and Gate 2.

Changes in this pass (19 October 2026, Lemon Soda rename):
- The product is Lemon Soda, with lemon flavour. Lime Cube and lime flavour are replaced in the body. The earlier stimulus sentence keeps its lime wedge, because it describes the withdrawn stimulus.
- The comparison product is the Singha Lemon Soda can (capture 48, an extract, tier S). The sparkling lime water facts are removed from the body; its sources M and N are no longer cited.
- Sale status: "listed on the company product page (extract, tier S); retail sale not dated" replaces the earlier on-sale wording. No raw save is claimed.
- Sweetener: sucralose is the working choice. The message rule says the Gate 1 regulatory opinion is to confirm it, because no opinion is held. The earlier wording said the opinion confirms it.
- Net weight: 3.8 g specification, verified by weighing before print (Gate 9).
- The name row records that "Lemon Soda" is the same as a printed flavour name on the company's Singha Lemon Soda product page, a name-clearance point for Gate 7.

Group F, 19 October 2026: bare Singha made Singha Corporation or the SINGHA mark holder, Decisions heading renamed, validation plan and survey risk row added, Tier key replaced by the Appendix A pointer; Appendix C file was not yet present when this pass ran.
