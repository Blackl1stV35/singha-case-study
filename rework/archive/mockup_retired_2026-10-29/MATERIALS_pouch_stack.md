# Pouch laminate stack, as modelled (19 October 2026)

Status: the stack is now in the mock-up model. Thicknesses and barrier choices are ASSUMPTION (typical structures for a dry, food-contact single-serve pouch). The only sourced value is the PET refractive index. No converter quote, no barrier test, no food-contact check and no recycling check has been done.

## 1. Layers, outside to inside

| Layer | Material | Typical thickness | Function | Model in the scene |
|---|---|---|---|---|
| 1. Outer carrier | PET film | about 12 µm (ASSUMPTION) | clarity, abrasion, print carrier | `PackFilm` surface; IOR 1.575 (PET, sourced); 3D page clearcoat 0.3 |
| 2. Print | reverse-printed inks | 1 to 3 µm (ASSUMPTION) | colour and artwork | front label texture with a luminance relief (`PackLabel` bump, strength 0.03), the ink build-up |
| 3. Adhesive | solventless polyurethane | about 3 µm (ASSUMPTION) | bonds PET to foil | not modelled separately |
| 4. Barrier | aluminium foil | 7 to 9 µm (ASSUMPTION) | oxygen and moisture barrier | metallic 0.35 under the print on `PackFilm`; silver on the rim |
| 5. Adhesive | solventless polyurethane | about 3 µm (ASSUMPTION) | bonds foil to sealant | not modelled separately |
| 6. Sealant | PE (LDPE or LLDPE) | 50 to 70 µm (ASSUMPTION) | heat seal, food contact | `PackLaminateEdge` rim: foil silver with a sealant tint |

Total laminate: about 0.08 to 0.10 mm (ASSUMPTION). At the hero-shot distance this is about one pixel, so the layers are not visible as separate stripes. The visible cues are the metallic sheen on the body and the silver rim.

## 2. Why these layers

- **Moisture is the main risk.** The cube is potassium bicarbonate and citric acid, which take up water. The foil is there for moisture. No water-vapour transmission rate has been sourced, so the required rate is open.
- **Oxygen and light** matter less for a dry sweetened cube, but the foil covers them too. Not tested.
- **Sealant** must be food-contact PE. Compliance is not checked here.

## 3. What changed in the model

- `build_cube_scene.py`: the pouch rim is a separate material (`PackLaminateEdge`, metallic 0.9, roughness 0.3, silver with a sealant tint). The body film gets metallic 0.35 for the foil beneath the print. The label gets a luminance relief for the ink build-up.
- `cube_3d.html`: the rim is a metallic silver material, and the film carries the same foil sheen.

## 4. Trade-offs and limits

- **Recycling.** A PET, foil and PE laminate is generally not recyclable in common Thai collection streams (ASSUMPTION; not checked). The old workspace document (`Singha (1).docx`, not in the repo) reports that environmentally friendly packaging was chosen by only 5.8% of consumers. It does not give its source table. `rework/41` does not contain this figure. A foil laminate works against that.
- **Converter quote.** No pouch converter quote exists, so the thicknesses, the adhesive system and the seal parameters are unpriced and unverified.
- **Physical test.** Nothing is made, sealed, dropped or stored. Moisture uptake and seal strength are untested.
- **Food contact.** The PE sealant, the foil and the inks need a food-contact check. Not done.
