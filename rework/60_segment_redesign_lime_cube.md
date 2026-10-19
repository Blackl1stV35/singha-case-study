# Segment redesign: Lime Cube (19 October 2026)

Status: a proposal draft. The redesign is in the labels, the 3D page and the scene. Gate G1 (the lion on a non-alcoholic pack) is open and blocks any proof, print or sale. Nothing is printed or submitted.

## 1. Brief

The package is tailored to the target segment and the preference clusters the team identified: **men, mainly 25 to 34, sport-minded, with Singha brand presence as the reason to buy**. The product is named **Lime Cube**, with no SINGHA word in the name. The lion is the only SINGHA reference on the pack. Units: one cube per pouch, single serve.

## 2. Design (merged from three cluster concepts, workflow wf_87c8ab5d-bf0)

- **Brand presence:** the authorised lion, in silver foil, is the front hero. It is the only SINGHA reference.
- **Men:** charcoal (#17191C) matte field, Georgia Bold capitals for the name, silver foil in place of gold, restrained paper-tone type, two foil elements only.
- **Sport:** one lime wedge (#A8CF3A) bleeding off the bottom right, plus an angled foil rule. Graphics only: no athletes, no league marks, no performance words.
- **Palette:** charcoal #17191C, lime #A8CF3A, silver foil #C4C9CE, paper #F1F0EB. The brighter lime #C5F03A was dropped as too loud for the men cluster.

## 3. Layout as built (70 by 90 mm, 15 px per mm)

Front: lion box 40 by 34 mm at x 15 to 55, y 12 to 46 mm. Name plate LIME CUBE, centred, baseline 55 mm. Foil rule from (6, 62) to (64, 58) mm. Instruction block left at 6 mm, measure to 55 mm, baselines from 66.5 mm. Lime wedge (70, 72), (70, 90), (44, 90) mm.

Back: name at 13 pt, ink hairline at 19.5 mm, preparation line at 23 mm, mandatory copy in one column at 2.27 mm (34 px), format line above the 80 mm seal zone.

## 4. Check findings and how each was handled

The compliance check returned `ok: false` with 11 findings.

| # | Finding | Handling |
|---|---|---|
| 1 | Front copy sits under the lion. The brief reads "no text under or beside the lion except the product name" | **Open decision for the user.** I read the rule as covering the SINGHA wordmark, which was removed. Copy below the lion stays. If the rule means all text, the front copy moves and the front is redone |
| 2 | Back lion has text beneath it | Applied: the back lion is removed. The design's own fallback |
| 3 | Back lion 10 mm wide, below the 25 mm minimum | Applied: removed (see 2) |
| 4 | **Gate G1, blocking:** the lion is an alcoholic-beverage brand emblem. Brand presence is the lead reason to buy on a non-alcoholic pack, which resembles surrogate advertising | **Open, not cleared.** Brand-owner and legal decision needed before any proof, print or sale. The 18 October 2026 authorisation covers the proposal only. This is the main decision for the user |
| 5 | The lime wedge reads as a fruit (a lime wedge) | Partly applied: the shape is an abstract triangle with no rind or segments. The name in the design files should change to "lime triangle" |
| 6 | The format line's descender reached the seal zone at 79.5 mm | Applied: baseline moved to 78.5 mm |
| 7 | Units per package stated as fact | Applied: one cube per pouch. The sales unit is inferred from "single-serve" and needs the user's confirmation |
| 8 | Leading did not match the stated 1.3 ratio | Applied: leading 3.0 mm on the preparation line; back copy at 1.15 times its size |
| 9 | The lion's wordmark lettering removal is unverified | Open: the lion asset (`assets/singha_lion.png`) was cut at the wordmark gap. A designer re-cut from the authorised file is needed before any proof |
| 10 | Leelawadee UI has no unconfirmed-font limit or Latin fallback | Stated limit: Georgia and Leelawadee UI are taken as installed on target machines; not checked there |
| 11 | The trademark limit is a naming concern in another form | Kept as a stated limit, separate from the dropped naming concern |

Mock-up scope: the design asked for a seven-layer laminate with three ink stations and a hot-foil stamp. The layer record is in `mockup/MATERIALS_pouch_stack.md`. The scene's rim colour is now the foil silver. The hot-foil stamp, the ink stations and the gusset are not drawn in the scene (stated limit).

## 5. Stated limits

- Gate G1 is open and blocks everything that follows.
- The lion's cut is scripted, not designer artwork.
- The mandatory copy is placeholder text. The Thai particulars, ingredients, sweetener name and manufacturer are not set.
- The back copy is at 2.27 mm. The token minimum is 2.2 mm.
- The drop line, "One compressed cube is dropped into 330 ml of water.", is the wording stated in the product brief. The approved wording is not confirmed.
- Sales unit: one pouch per sold unit is inferred, not confirmed.
- The name Lime Cube is descriptive and weakly protectable. It also overlaps the existing Singha lime sparkling product (`rework/54`). No register search.
- No physical proof, dieline, colour proof or foil swatch.

## 6. Decisions for the user

1. **G1:** keep the lion as hero on a non-alcoholic pack, subject to brand and legal clearance, or drop the lion and the brand-presence reason to buy.
2. **Below-the-lion rule:** does "no text under the lion" cover all front copy, or only the SINGHA wordmark?
3. **Sales unit:** confirm one pouch as the sold unit.

## 7. Resolution of G1 for the proposal (19 October 2026)

- The user confirmed the claim that the SINGHA lion may be used for the proposal. Recorded as the user's decision for the competition proposal.
- This is not a brand-owner or legal clearance. The print and sale conditions are unchanged: brand-owner and legal sign-off before any print or production use, and no beer, bar or beverage-brand cue on the pack.
- The judge folder is synced to the merged design: label_front.png, label_back.png, cube_3d.html and cube_hero.png (the 2K render with the cleaned lion).

## 8. G1 closed by the user (19 October 2026)

- The user placed the brand-owner and legal sign-off, and the alcohol-cue concern on the lion for a non-alcoholic product, with Singha's department. The team's records no longer carry that condition.
- The check in section 4 (item 4) raised this concern. It stays on record as the reason the question was asked. It is no longer a team gate.
- The team's own copy rules stay: no sugar-free, sodium-free, health or fizz wording.
