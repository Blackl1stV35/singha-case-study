# Materials for the lime cube hero shot

Scene: `cube_hero.png`, built by `build_cube_scene.py` in Blender 5.2, Cycles on CPU, 1600 x 1200, 128 samples, denoise on. The scene uses only Blender primitives and procedural node materials. No texture file, downloaded asset or network source is used. No glass, water or bubble is drawn (48 section 3.3, decision D7, rule S2).

Basis codes:
- **ASSUMPTION**: a design or rendering choice with no measured or published source. Colours and sizes read from `style_tokens.json` are ASSUMPTION (design choice). No brand colour is verified.
- **DERIVED**: arithmetic on ASSUMPTION inputs, for example the cube side from the design dose in 48 section 6.1.
- **SOURCED**: none. No value in this scene is sourced. The stoichiometry in 48 section 6.1 is sourced, and it sets only the derived cube side.

## Materials

| Material | Where it is used | Settings | Basis |
|---|---|---|---|
| PackFilm | Pouch body (sides, back, and the front outside the label) | Base colour: off-white `#F6F3E8`. Roughness 0.25. IOR 1.575 (PET). Default specular. | Colour: ASSUMPTION (design choice, off-white token). IOR: SOURCED. PET refractive index about 1.575 at 589 nm, from the Wikipedia list of refractive indices and the KLA refractive-index database (read 18 Oct 2026). The value is an isotropic average, and PET film is birefringent, so this is a stated simplification. Roughness 0.25 (satin print): ASSUMPTION, no measured source. |
| PackSeal | Heat-seal ridges along the top and bottom | Base colour: off-white-deep `#E6E0CB`. Roughness 0.30. IOR 1.575 (same PET film). | Colour: ASSUMPTION (design choice). IOR: as PackFilm. Roughness and ridge size: ASSUMPTION. |
| PackLabel | Front artwork, 65 x 32.5 mm, centred on the front face | Image texture from `label_front.png` (2400 x 1200, from the label step), used as base colour. Roughness 0.35. | Artwork: the label step, built from the tokens file (ASSUMPTION, design choice). Placement, size and finish: ASSUMPTION. |
| CubeLime | The compressed cube, resting on the floor beside the pouch | Base colour: lime `#9ED83A`. Roughness 0.75 (matte compressed powder). Subsurface weight 0.10, radius 3 / 2 / 1.5 mm. Noise bump (scale 600, strength 0.25). | Colour: ASSUMPTION (design choice). Roughness, subsurface and bump: ASSUMPTION (no measured finish for a compressed cube). |
| Cyclorama | Matte floor and curved backdrop | Base colour: background `#DCE5D1`. Roughness 0.95. Specular IOR level 0.2. | Colour: ASSUMPTION (design choice). Matte finish and curve radius 120 mm: ASSUMPTION. |
| World (fill only) | Soft ambient fill | Background colour `#DCE5D1` at strength 0.25. | ASSUMPTION. |

Removed in this revision (critic blocker, 48 section 8.4): TumblerGlass, LimeWater and Bubble. The earlier render drew a tumbler with pale lime water by default; both, and the bubble option, are removed from the script and from this table.

## Geometry used by the materials

| Item | Value | Basis |
|---|---|---|
| Pack width x height | 70 x 90 mm | ASSUMPTION (design choice). `dimensions_mm` in the tokens file (`pack_w`, `pack_h`) |
| Pack depth | 20 mm | ASSUMPTION (the tokens file marks it ASSUMPTION) |
| Pack edge bevel | 2.5 mm | ASSUMPTION |
| Heat-seal ridges | 4 mm tall at top and bottom, full depth, 1.2 mm bevel | ASSUMPTION |
| Front label | 65 x 32.5 mm, 2:1 aspect kept | ASSUMPTION (layout). The artwork is landscape and the front is portrait, so it is contained, not stretched. |
| Cube side | 15 mm | DERIVED. Design dose 1.75 volumes: 4.23 g of reactants, design mass 5.28 g, density 1.56 g/cm3 at 15 mm. The density band (1.25 to 1.60) is ASSUMPTION; the high end of the mass range is above it (48 section 6.4). |
| Cube bevel and rotation | 1.5 mm bevel; rotated 18 degrees about Z only, so the base sits flat on the floor; centre 7.5 mm above the floor, 26 mm right of the pouch centre line | ASSUMPTION (staging) |

## Render settings with a basis

| Setting | Value | Basis |
|---|---|---|
| Engine and device | Cycles, CPU | Task requirement |
| Samples | 128 (not reduced) | Task requirement. The final render took 248 s of script time (252 s wall), recorded in `rework/screen/cube_hero_render_log_2026-10-18.txt` |
| Denoise | OpenImageDenoise, on | Task requirement. The setting raised no error in the log. Its visual effect was not measured separately. |
| View transform | Standard, exposure -1.2 stops | ASSUMPTION. Set by measuring the backdrop against the background token. |
| Caustics | Off | ASSUMPTION (noise control) |
| Light bounces | 32 | ASSUMPTION (set during testing) |
| Lights | Three soft square area lights: key 12 W, fill 4 W, rim 8 W | ASSUMPTION (tuned by eye) |
| Camera | 85 mm lens, 36 mm sensor, 4:3, looking down about 14 degrees, aimed at the pouch and cube together | ASSUMPTION (composition) |
| PNG metadata | All text chunks removed. The remaining chunks are IHDR, sRGB, gAMA, pHYs, IDAT and IEND. | Task requirement. Checked on the output file. |

## Measured checks on the output

Read from `cube_hero.png` with PIL on 18 October 2026, as patch medians:
- Backdrop, top-left patch (40 to 80 px): `#E1EFD2`. Target `#DCE5D1`. Lighter and slightly greener.
- Backdrop, mid-right patch: `#D5E1C7`. Falloff from the key light.
- Cube, front-face patch (1075 to 1100 px, 925 to 950 px): `#9DD846`. Target lime `#9ED83A`. Close.

## Limits

- No material here is validated against a real pouch or cube. Every surface finish and every tint is a rendering choice.
- The pack reads more like a rigid box than a flat single-serve pouch. The heat-seal ridges make it look like a lid. The depth of 20 mm is ASSUMPTION.
- The label is shown at 65 mm wide and 2:1, so it covers only the centre of the front face. The copy layout in 48 section 5.5 was built for a portrait front, and the artwork does not follow that layout.
- The cube's density at the high end of the mass range (5.80 g) is above the ASSUMPTION band at 15 mm. The render does not depend on mass. The owner must choose between a side of about 15.4 mm or more and a narrower mass range (48 section 6.4, L6).
- No glass is drawn. If the owner wants a glass, rule 5 must be reopened in writing before judging (48 section 10.3).


## Revision, 18 October 2026 (real-material values)

The pouch film and the cube now use the values above. The pack geometry is unchanged: 70 x 90 mm front, 20 mm depth, and seal ridges 4 mm tall. The render still reads as a rigid box. The depth and the ridge profile are ASSUMPTION and need a decision on the pouch form before the shape can read as a flat pouch.