# Image placeholders and prompts (deck build, 20 October 2026)

The Canva deck leaves six empty frames. Another model generates each image from the prompt below; the file is then dropped into the frame with the same label.

Rules that apply to every image (anti-slop filter and the glassware hold, Gate 7):
- No glass, water, bubbles, fizz, lemon fruit, bottle, can, alcohol cue, text, logo or watermark.
- Background: seamless warm paper tone, hex #F6F4EE, so the image sits flat on the slide with no visible frame.
- Subject: a pressed lemon-yellow tablet cube, 14 mm, soft rounded edges, satin matte finish, fine granular pressed-powder texture, faint sheen on the top edges. Colour about #F7D23A.
- Light: soft three-point studio light, soft contact shadow, no hard glare, no glow, no gradient background.
- Output: PNG, at least 2400 px on the long side.

| Label | Slide | Frame size (px at 1920 x 1080) | Aspect ratio |
|---|---|---|---|
| P1 | 1 Cover | 864 x 1080 | 4:5 portrait |
| P2 | 2 Executive summary | 620 x 465 | 4:3 |
| P3 | 6 The cube in use, phase 1 | 604 x 453 | 4:3 |
| P4 | 6 The cube in use, phase 2 | 604 x 453 | 4:3 |
| P5 | 6 The cube in use, phase 3 | 604 x 453 | 4:3 |
| P6 | 12 Extension options | 1600 x 400 | 4:1 strip |

## Prompts

**P1 (cover).** Studio product photograph, portrait 4:5. One compressed lemon-yellow tablet cube, 14 mm, softly rounded edges, satin matte finish with a fine granular pressed-powder texture and a faint sheen on the top edges. Placed on a matte warm-paper surface (#F6F4EE), slightly elevated three-quarter view, the cube in the lower-centre of the frame with generous empty space above. Soft three-point studio light, soft contact shadow. Seamless background in the same paper tone. No glass, no water, no bubbles, no fruit, no packaging, no text, no logo.

**P2 (executive summary).** Studio product photograph, landscape 4:3. One lemon-yellow pressed tablet cube, 14 mm, rounded edges, satin matte, fine granular texture. Centred, three-quarter view from slightly above, soft contact shadow, seamless paper-tone background (#F6F4EE). Soft even studio light. No glass, no water, no bubbles, no fruit, no packaging, no text, no logo.

**P3 (phase 1, the cube).** Same camera, light and background as P2. One whole cube, front-three-quarter view, centred, the cube filling about 40% of the frame height.

**P4 (phase 2, dropped into water; no water drawn).** Same camera, light and background as P2. Ten small lemon-yellow pressed fragments, broken from one cube, scattered loosely on a flat matte surface, each with rounded edges and the same satin granular finish; the pieces vary in size from about a quarter to a half of the original cube's side; soft contact shadows. No glass, no water, no bubbles.

**P5 (phase 3, ready to drink; no liquid drawn).** Same camera, light and background as P2. Three very small lemon-yellow pressed fragments resting on a flat matte surface, rounded edges, satin granular finish, most of the frame left empty. Soft contact shadows. No glass, no water, no bubbles.

**P6 (extension options).** Studio product photograph, ultra-wide 4:1 strip. A row of five identical pressed tablet cubes, 14 mm, evenly spaced on a matte paper-tone surface, same satin granular finish, same soft three-point light. Left to right: lemon yellow (#F7D23A), yuzu pale yellow-green (#E9DC7B), red (#C8453B), ume soft plum (#8E5A7C), pink (#E9A3B4). Seamless background #F6F4EE. No glass, no water, no bubbles, no fruit, no packaging, no text, no logo.

## Notes
- P1 to P5 should come out of one generation session so the cube, light and surface match across slides 1, 2 and 6.
- The earlier local renders (Blender, 20 October 2026) are in `rework/mockup/deck_mock/renders/` and can serve as a style reference for the generator. They are not used in the Canva deck.
