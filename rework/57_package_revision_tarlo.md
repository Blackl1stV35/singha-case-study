# Package revision: Tarlo, modern direction, lion recoloured, net weight derived (19 October 2026)

> Audit, 19 October 2026: the corrections at the end of this record supersede the figures they name.

Status: revision applied to the label artwork, the 3D page and the 2K front render. The lion treatment, the brand-cue question and the trademark check are open gates before any print or production use. Nothing is printed, registered or submitted.

## 1. What the user asked

- Make the package more modern, with a bold, cinematic "avenger" feel.
- Allow the lion emblem to be touched (recoloured, re-cut).
- Remove the text below the lion (the SINGHA wordmark).
- Name the product.
- Derive and state the net weight at the end.

## 2. Decisions

> Update, 19 October 2026: the user picked **Singha Lime Cube** as the product name. This overrides T1 below. Open: whether SINGHA appears as text on the pack, since the wordmark was removed from the lion at the user's request (section 7).

| # | Decision | Basis | Status |
|---|---|---|---|
| T1 | **Product name: Tarlo** (descriptor "lime drink cube"). Runner-up: Cubi | Workflow wg0nz9dbo, name phase: a judge scored nine candidates on legibility at 70 mm, Thai-English readability, distinctiveness and trademark risk. Tarlo scored 17 of 20 (trademark scored so 5 is the lowest risk). Cubi scored 14 and describes the cube, so it is weakly distinctive and carries a Cuba association | Working name. One web search only. No register search. Stated limit (section 5) |
| T2 | Palette: ink #0B0C0A, lime #C5F03A, violet #6A3CFF, paper #F2F0E6 | Workflow direction phase, merged. Ink stays dominant so the pack does not borrow the organiser's lime can field | Design choice, not a brand colour |
| T3 | Type: Georgia Bold caps for the name; Leelawadee UI for copy | Workflow direction. Both are installed on target machines and not checked there | Free fallbacks: Gelasio Bold; Noto Sans Thai |
| T4 | **Lion recoloured, not redrawn.** Gold areas take lime on the front and violet on the back head; the dark contour takes ink. A violet keyline rings the front lion. The SINGHA wordmark and the text below the lion are cut away (`assets/singha_lion.png`) | User request; the lion is cut at the wordmark gap, row 292 of the supplied emblem file | Recolour by script, not a designer's artwork. Open gate G2 |
| T5 | **TARLO sits above the lion, not below it.** The workflow put the name under the lion across the diagonal. That conflicts with the request to remove text below the lion, so the name moves up | Check finding 4 | Applied. Confirm with the user |
| T6 | Violet appears only in the lion keyline, the diagonal cut and the back lion head | Workflow direction, "avoid" list | Applied |
| T7 | Front keeps the sweetener disclosure "Contains an intensive sweetener." | Earlier record (rework/50 and rework/52). The workflow direction left it off | Applied |
| T8 | Back keeps the potassium presence line "Potassium: present. Amount per serving: [to be set]". The workflow direction asked for no amount to be printed | Decision F4 in rework/50 (declared as a plain fact, no claim). The conflict is flagged to the user | Kept as F4. Open for the user |
| T9 | The three numbered directions are folded into one "Preparation:" copy line so the mandatory copy fits at a legal size | Space on a 70 x 90 mm back | Applied |

## 3. Net weight, derived

One cube per pouch.

- Reactants, derived from stoichiometry at the 1.75-volume design dose (rework/50, gate G3; rework/screen/final_gate_sim.py): 2.58 g potassium bicarbonate plus 1.65 g citric acid = **4.23 g**.
- Binder, filler, flavour, sweetener and excess citric acid, all ASSUMPTION: **1.05 g** in total.
- Design mass: 4.23 + 1.05 = **5.28 g**, rounded to **5.3 g net weight**.

Printed as "Net weight: 5.3 g" on the front band, the back band and the 3D page. Recorded in `style_tokens.json` under `dimensions_mm.net_weight_g`.

Limits: the 4.23 g is derived. The 1.05 g is an assumed aggregate, not a split, because no binder, filler or sweetener mass is sourced. Nothing has been weighed. The 5.8 g high end of the earlier mass range implies a density above the assumed band, so the printed figure must be confirmed on weighed production cubes before print.

The check agent proposed a split of the 1.05 g (0.17, 0.03, 0.05 and 0.80 g). Those figures do not appear in any record and were not used.

## 4. Check findings and how each was resolved

The compliance check returned ok = false with ten findings.

| # | Finding | Resolution |
|---|---|---|
| 1 | The ingredient list omitted the binder and filler, and the order was wrong | Applied. The ingredients run in descending order: potassium bicarbonate, citric acid, binder and filler [to be set], intensive sweetener [name to be set], flavour. The names are placeholders and must be confirmed before print |
| 2 | The SINGHA lion is the emblem of an alcoholic beverage brand, and on a non-alcoholic pack it can be read as a beer or alcohol cue | **Open, hard gate G1.** Brand-owner and legal sign-off before any print or production use. The authorisation of 18 October 2026 covers the proposal only |
| 3 | The word "first" in the rationale | Not pack copy. Avoided in the record |
| 4 | TARLO under the lion conflicts with the removal of text below the lion | Applied (T5). TARLO sits above the lion |
| 5 | LIME DRINK CUBE sat on the trim edge, outside the 5 mm safe margin | Applied. Inset to the 75 px (5 mm) margin |
| 6 | The drop line and net weight may not fit on one row | Applied. The drop line wraps to two lines and the net weight sits on the right, both inside the margin |
| 7 | The diagonal cut bounds were inconsistent | Applied. The cut runs from the left edge at y 1000 px to the right edge at y 915 px. TARLO sits clear of it |
| 8 | Sodium-free basis: sweetener and binder unnamed | Partly open. The pack copy makes no sodium claim (F1). Name the sweetener and binder and confirm they contain no sodium before the proposal describes the product that way. **Open, gate G3** |
| 9 | No zones for the Thai panel, regulatory block, barcode or manufacturer | Partly applied. The back has the Thai-language particulars line and the mandatory copy. The barcode and a dedicated regulatory block are not drawn. **Stated limit for the packaging team** |
| 10 | Marvel or Avengers look-alike risk | Mane and shapes come only from the authorised lion file. Nothing is added (no star, shield or crest). **Open, gate G4:** a side-by-side look-alike check before print |
| 11 | Grain contradicted "flat colour only" | Applied. No grain is drawn. Flat colour only |

## 5. Gates and limits

- **G1 Lion on a non-alcoholic pack.** Hard gate. Brand-owner and legal sign-off before print or production. No beer, bar or beverage-brand cue may be added. The authorisation covers the proposal only.
- **G2 Lion treatment.** The recolour is a script output, not designer artwork. A designer should re-cut it from the authorised file before print.
- **G3 Sodium and ingredients.** Name the sweetener and binder, and confirm no sodium is present, before any sodium-free description.
- **G4 Look-alike.** Side-by-side check against Avengers and Marvel key art and logos before print.
- **Trademark.** Tarlo had one web search and no register search (USPTO, WIPO Global Brand, Thai DIP, IPOS, class 32 and 33). Nearest name: Tarax. "Tar" may carry a tobacco cue in English. The authorisation of the SINGHA name and lion for the proposal is not a licence. Not cleared.
- **Fonts.** Georgia and Leelawadee UI are taken as installed on target machines and are not checked there.
- **Layout.** The layout was checked on the rendered PNG at 1050 by 1350 px. It has no proof, dieline or colour check.
- **Back copy size.** The mandatory copy is set at 2.3 mm, above the 2.2 mm particulars minimum in the tokens.
- **Barcode, regulatory block and Thai panel.** Not drawn. For the packaging team.
- **No physical test.** Nothing is printed or weighed.

## 6. Files

- `mockup/make_pack_labels.py` (new layout), `mockup/style_tokens.json` (copy, palette, net weight), `mockup/assets/singha_lion.png` (lion without the wordmark).
- `mockup/label_front.png`, `mockup/label_back.png` (1050 by 1350 px).
- `mockup/cube_3d.html` (labels embedded as images), `mockup/cube_front_2k.png` (2K front render).
- `screen/verify_cube_mockup.py` (checks the label images load; 24 of 24 pass).
- `judge/`: label_front.png, label_back.png, cube_3d.html, cube_hero.png (the 2K render). Team-only records stay out of judge/.

## 7. Name pick and the SINGHA question (19 October 2026)

- **Picked:** Singha Lime Cube, by the user.
- **Why Tarlo was first:** the judge scored Tarlo 17 of 20 and Cubi 14. Cubi describes the cube's form, so it is weakly protectable. Cubi also surfaced a Cuba Libre Cola record (abandoned 2002). Tarlo is coined, with no drink or Thai meaning.
- **Costs of Singha Lime Cube:** "Lime Cube" is descriptive, so the product part of the name is weakly protectable on its own. It overlaps the existing Singha Sparkling Water Lime Flavour recorded in rework/54 (from rework/42), which could confuse shoppers. "Singha + descriptor" follows the pattern in the old workspace document (for example "Singha Lemon Soda").
- **Open decision:** a product name on the pack carries the word SINGHA as text. That conflicts with the earlier request to remove the wordmark. Options: (a) SINGHA as a small top line above the name, with no text under the lion; (b) the name without SINGHA, with the lion as the only SINGHA reference; (c) keep SINGHA only in the legal name. The pack artwork is not changed until this is decided.
- **Not done:** no register search for Singha Lime Cube. Authorisation of 18 October 2026 covers the proposal only.

## 8. Decisions confirmed (19 October 2026)

- **Name: Lime Cube.** The SINGHA word is not in the product name, so the SINGHA naming question is dropped. The lion is the only SINGHA reference on the pack. Descriptive name, so it is weakly protectable; it still needs a register search. It also sits close to the existing Singha lime sparkling product in rework/54.
- **Units per package: one cube per pouch.** The proposal sells single-serve pouches, each made up to 330 ml. No multipack is in the proposal. A carton of several pouches would be a later decision with its own pricing.
- **Segment brief:** men, mainly 25 to 34, sport-minded, with Singha brand presence as a reason to buy. The package redesign follows this brief. The lead segment rests on the synthesis test, which the desk study in rework/55 qualified: sugar-substitute drinkers skew 45 and over.
- **Laminate:** PET outer, printed ink, aluminium barrier foil, PE sealant, as set out in mockup/MATERIALS_pouch_stack.md. The thicknesses are assumptions.

## Audit corrections (19 October 2026)

- The compliance check returned ok = false with **eleven** findings (rows 1 to 11 in section 4), not ten.
- **Safe margin:** the generator's constant M is 6 mm (90 px), not 75 px (5 mm). Row 5 of section 4 is corrected accordingly.
- **The 5.8 g high end** is cited to rework/48 section 6.4. That passage was not traced in the audit. Unverified.
- **The scores** (Tarlo 17 of 20, Cubi 14) come from a workflow output that is not saved in the repo. Unverified until saved to rework/raw/.
- **The 80 cm2 format limit** (Notification 445 Annex 1) is not traced to its text. Unverified.
