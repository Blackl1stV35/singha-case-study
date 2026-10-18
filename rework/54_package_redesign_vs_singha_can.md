# Package redesign, with regard to the Singha lime soda can (18 October 2026)

Status: redesign applied to the front label and the 3D page, and the hero re-rendered. This is a design decision for the team, not a legal clearance. A trade-dress and trademark check is still open (section 6).

Correction, 18 October 2026 (from the user). The restriction taken from the Singha can is its lion emblem only. The package uses no lion emblem. The 330 ml serving reference is not cleared and remains under review, and it is not a settled rule. Rules R-P2 to R-P5 and R-P7 are design preferences, not clearance findings. The trademark and trade dress search is not complete: a WIPO Global Brand Database search for PLUNK returned 51 results across several offices, and the Thai mark register was not reached in that pass.

## 1. What we looked at

Google image search for "singha lime soda", read through the built-in browser on 18 October 2026. Thumbnails only: nothing was downloaded, and no page beyond the results was opened.

- The first results were **SINGHA LEMON SODA** (green variant) and **SINGHA RED LEMON SODA** (red variant), both listed by Singha Corporation. No lime-variant can was in the first results.
- The lime sparkling product is **Singha Sparkling Water Lime Flavour**, a 330 ml can at THB 15 from the March 2026 launch ([rework/42](42_working_candidate_lime_cube.md)). Its can design was not seen, so section 3 rests on the lemon soda can.
- Can features seen: a slim can; a full lime-green field (green variant); the lion emblem in white; the SINGHA wordmark across the top; a "LEMON SODA" name band; fruit slices bottom right; a small circular "C" badge on the lower left; small Thai product text. The red variant uses the same layout in red.

## 2. What "respecting the can" means here

We read the instruction as: design the package with regard to the can. That means three things.

1. **Stay clear of its trade dress.** Do not copy its emblem, wordmark, colour field, or layout.
2. **Keep the like-for-like reference.** Same 330 ml serving reference, so shoppers can compare the two at the shelf.
3. **Be distinct at a glance.** A different format (a pouch, not a cylinder) and a different dominant colour.

## 3. Rules adopted

| # | Rule | Reason |
|---|---|---|
| R-P1 | No lion emblem, no Garuda, no SINGHA wordmark or lettering in any form | Organiser marks, on the no-use list in [rework/48](48_brand_style_matching.md) |
| R-P2 | No full lime-green field. Lime is an accent only: a thin rule and the cube's own face. The dominant colour is deep ink | The can's lime field is its main shelf identity |
| R-P3 | No fruit-slice composition. The cube drawing is the hero | Fruit slices are part of the can's layout |
| R-P4 | No "C" or other nutrition badge | Badges can imply a claim we cannot make ([rework/50](50_final_gate_resolution.md)) |
| R-P5 | No "soda", "lemon", or the organiser's product name. The working name stays "Plunk Lime Cube" | The can's name family; the working name is not cleared |
| R-P6 | Keep the 330 ml serving reference | Like-for-like comparison at the shelf |
| R-P7 | The pack is a flat single-serve pouch, not a cylinder | Format clearly different from a can |

## 4. Palette: before and after

| Element | Before (18 Oct, earlier) | After (this redesign) |
|---|---|---|
| Name band | Full-width lime `#9ED83A` | Deep ink `#12241B`, with off-white name |
| Accent | None | 10 px lime rule under the name band |
| Cube panel | Lime-pale `#E3F3BE` | Off-white-deep `#E6E0CB` |
| Cube face | Lime `#9ED83A` | Lime `#9ED83A` (kept, as the one lime element) |
| Bottom band | Ink | Ink (unchanged) |

## 5. What changed in the repo

- `rework/mockup/make_label.py`: name band to ink with the off-white name, a lime rule, and the cube panel to off-white-deep. Front and back. The label was regenerated.
- `rework/mockup/cube_3d.html`: the same changes in the canvas label, and the name-line colour.
- `rework/mockup/cube_hero.png`: re-rendered with the new front (128 samples, Blender 5.2, about 6 minutes).
- `rework/judge/`: copies updated. The browser check passes 26 of 26 on the recoloured page. The judge PNGs carry no text metadata.

## 6. Limits and open items

- **Trade dress and trademark are not cleared.** Only thumbnails were seen, and no registry search was done. A formal trade-dress and trademark search is needed before any public use, and it is outside this desk scope.
- **The lime can itself was not seen.** The redesign follows the lemon soda can. If the lime can differs, rules R-P1 to R-P3 still hold, but the palette should be checked against it.
- **Pack form still reads as a box** in the render, because the 20 mm depth and the seal-ridge profile are assumptions ([MATERIALS_cube.md](mockup/MATERIALS_cube.md)).
- **The palette is a design choice.** It has not been tested with shoppers.

## Closed as a stated limit (18 October 2026)

The trademark search is closed as a stated limit, as the user instructed when the WIPO search could not be completed. The WIPO Global Brand Database search for PLUNK returned 51 results across several offices, with no Thailand filter applied, because the designation-country and Nice class filters returned errors. The Thai DIP public page reached in that pass lists goods and services, not marks, so the Thai mark register was not searched. No registry result clears or blocks the name Plunk Lime Cube. This is a limit on the search, not a finding of freedom to operate.

## Authorization (18 October 2026, from the user)

SINGHA name and lion emblem: authorized by the user for the product proposal (18 October 2026). The user dropped the trademark rights concern. This is the user's statement, not a licence document. The lion-only restriction in the correction above and rule R-P1 are superseded for the proposal. The package artwork is not yet changed: the choice among options A, B and C is still open, and the lion is not yet on any front. The 330 ml reference and the physics stress test remain open.
