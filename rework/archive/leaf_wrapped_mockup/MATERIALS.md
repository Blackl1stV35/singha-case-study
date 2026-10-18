# Mockup materials: sources and assumptions (18 October 2026)

Used by `build_pop_scene.py`. Scene dimensions are assumptions (see the script docstring). Materials are real where a public source was found, and assumptions are marked **ASSUMPTION**.

## 1. Values used in the scene

| Object | Blender input | Value used | Source | Kind |
|---|---|---|---|---|
| Frozen core | Base Color | sRGB (0.7937, 0.7860, 0.7376) | Coconut milk Hunter L 80.6 and b 6.4, converted to sRGB (D65). Sourced: homogenised sample L 80.59 at 30 °C; b range 4.2 to 8.6 (midpoint used). **a = −1.5 is an ASSUMPTION** (a slight green tint for pandan). | literature (secondary) + assumption |
| Frozen core | IOR | 1.311 | Ice Ih at 550 nm, Warren and Brandt (2008), J. Geophys. Res. 113, D14220, doi:10.1029/2007JD009744. File https://atmos.uw.edu/ice_optical_constants/IOP_2008_ASCIItable.dat, row 5.500E-01 µm, mre 1.3110. Verified by re-reading the file. | measured-derived compilation |
| Frozen core | Roughness, Normal | Ice002 CC0 maps (1K) | ambientCG Ice002, https://ambientcg.com/view?id=Ice002. Normal strength 0.3. | texture (CC0) |
| Frozen core | Transmission Weight 0.35, Subsurface Weight 0.10, Subsurface Radius (0.4, 0.7, 1.0) | — | **ASSUMPTION**: no sourced transmission or scattering value for frozen coconut drinks | assumption |
| Leaf wrap | Base Color, Roughness, Normal | Interior crop of the Leaf001 CC0 maps (512 px, from the 2K maps at box 260,860 to 772,1372) | ambientCG Leaf001, https://ambientcg.com/view?id=Leaf001. The full photo has a black background, so only the veined leaf interior is used. Normal uses the OpenGL map (NormalGL), strength 0.6. The photo is a **generic leaf**, not confirmed as banana or pandan. | texture (CC0) |
| Leaf wrap | Subsurface Weight 0.25, Radius (0.2, 0.4, 0.1), Scale 0.004 | — | **ASSUMPTION**: no measured Musa or pandan transmittance was found. Thickness context: Musa lamina 147 to 172 µm (Widiyawati 2019, abstract, https://eprints.ums.ac.id/74234, qualitative anatomy). | assumption |
| Label band | Base Color | placeholder dieline artwork (unchanged) | rework/08 and mockup/label_artwork.png | — |
| Label band | Roughness, Normal | Paper002 CC0 maps (1K, centre-cropped to square) | ambientCG Paper002, https://ambientcg.com/view?id=Paper002 (brown cartonage, kraft-like). Normal strength 0.2. | texture (CC0) |

## 2. Values sourced but not used in the render

- Plain-paper Ra 1.8 µm (Example C-1), patent US6130185A, https://patents.google.com/patent/US6130185A/en. A patent measurement, not peer-reviewed. Ra is not a Principled BSDF input, and no sourced mapping from Ra to roughness was found, so the paper roughness comes from the texture instead.
- Web Ra 3.2 to 7.0 µm, patent US5922457A, https://patents.google.com/patent/US5922457A/en. Same caveat.
- Coconut-milk refractive index 1.3412 to 1.3446, Tetra Pak Coconut Handbook Table 8.2, https://coconuthandbook.tetrapak.com/chapter/chemistry-coconut-milk-and-cream (secondary; wavelength and temperature not stated). Not used, since the frozen core is scattering ice rather than liquid.
- Chlorophyll a absorbance peak 664 nm, buffer S (pure pigment, not pandan extract). Context for the green tint only.

## 3. Gaps (not sourced)

- Measured leaf reflectance and transmittance for banana (Musa) and pandan. Leads found but not verified: Macias-Echeverri et al. 2022 (Agronomia Colombiana, fetch refused), Springer s41348-023-00830-9 (login redirect), and the Mediamatic PDF (scanned image, unreadable by the fetch tool).
- Leaf cuticle roughness: Bousquet et al. 2005 (ScienceDirect returned HTTP 403).
- Coconut milk a* value and CIELAB colour from a measured source.
- Frozen-drink scattering and transmission values.

## 4. Textures: licence, size and files

All three packs are CC0 1.0 (ambientCG states that all assets are CC0; attribution not required). Downloaded 18 October 2026 from ambientCG `get?file=` links, 2K JPG zips (sizes as received):

| Pack | Zip | Received size | Maps used (1K, in `textures/`) |
|---|---|---|---|
| Leaf001 | Leaf001_2K-JPG.zip | 15.6 MB | Leaf001_Color_interior512.jpg, Leaf001_NormalGL_interior512.jpg, Leaf001_Roughness_interior512.jpg (interior crops of the 2K maps) |
| Ice002 | Ice002_2K-JPG.zip | 19.3 MB | Ice002_NormalGL_1K.jpg, Ice002_Roughness_1K.jpg |
| Paper002 | Paper002_2K-JPG.zip | 19.6 MB | Paper002_NormalGL_1K.jpg, Paper002_Roughness_1K.jpg (centre-cropped from 1588 × 2048) |

The 2K maps were resized to 1024 × 1024 with Lanczos resampling. The archives, their `.blend` and `.usdc` contents, and the unused maps were not kept. The `.blend` files inside the archives were not opened.

## 5. Scope

- The pop materials changed. Dimensions, lights and backdrop are unchanged.
- The still camera now starts from the video's first key (0.75 m, 300°, z 0.13, 85 mm). The earlier still camera sat at about 0.57 m and cropped the pack; the 1080p still now frames the whole pop.
- The 4K marketing video (rework/13) was rendered with the earlier placeholder materials and has not been re-rendered.

## 6. Leaf optics (applied 18 October)

Resolved 18 October 2026 (see `rework/22_thailand_inputs.md`, section 6). Banana single-leaf values from Gausman and Allen (1973), Tables III to V, derived with the single-layer Kubelka–Munk form: diffuse reflectance 10.5 % and transmittance 12.0 % at 550 nm; reflectance 6.0 % and transmittance 0.69 % at 650 nm. Fresh leaf thickness 0.241 mm (measured).

Applied on 18 October at your request (still `rework/26_pop_mockup_leaf_optics.png`): the leaf colour texture is scaled so its green reflectance matches the sourced 10.5 % (linear factor 0.52, file `Leaf001_Color_optics512.jpg`); subsurface weight is 0.12 from the 12 % transmittance; the red subsurface radius is scaled by 0.69 / 12 and the blue radius is set equal to green. The mapping is derived and not validated against a measurement. The earlier approved still is `rework/23_pop_mockup_real_materials.png`.

## 7. Physics assumptions in the render (18 October 2026)

Set from physical reasoning where no measurement exists (see `rework/22_thailand_inputs.md`, section 7):
- Pandan optics: same as banana, plus or minus 20 %. The pandan leaf is not modelled separately; the wrap uses the banana-based values.
- Cuticle specular roughness: Principled roughness from the leaf texture's roughness map, which is consistent with a waxy cuticle near 0.3.
- Leaf refractive index: 1.47 (not a render input; recorded for the optics note).

The render is for appearance only. Thresholds in the screens are not computed from the render.
