# Storyboard: cube drop into 330 ml of water (draft, 19 October 2026)

Status: superseded on 19 October 2026. The water block and the drop sequence were removed (rework/48 section 8.4, which removed the water column from the render; the judge 3D page follows it). Frames 1 to 6 below no longer apply. A clip needs a new storyboard before anything is rendered. The record is kept as it was.
Earlier status: draft for review. Nothing is rendered yet. Timings are the page's own constants (`cube_3d.html`, `SCENE`). The dissolve is illustrative: a real dissolve time is an ASSUMPTION (60 s), not a measurement. The label shown is the current artwork, which still reads TARLO. It will change to Lime Cube after the segment redesign lands.

Rules applied to every frame: no bubbles, fizz, droplets or splash (rule S2). No glassware, no bar or night-out cues. The water is a plain translucent lime block, with no container and no rim.

## Frames

| # | Time (s) | Action | Camera | What must read |
|---|---|---|---|---|
| 1 | 0.0 to 1.0 | Hover. The cube bobs about 1.2 mm above the water top and turns slowly. | Three-quarter view, slow orbit. The pouch stands at left, the water block at right. | The pouch front and the label. |
| 2 | 1.0 to 1.9 | Fall. The cube drops from hover to 7.5 mm above the water top, accelerating (quadratic ease), spinning at 4 rad/s. | Slow push-in toward the water. | The cube in motion. No splash. |
| 3 | 1.9 to 2.9 | Sink. The cube goes 12 mm below the water top and shrinks from 100% to 92%. | Follows the cube down. | The cube seen through the translucent water. |
| 4 | 2.9 to 4.9 | Dissolve. The cube shrinks from 92% to 10% and fades from 100% to 0% opacity, with an ease-out. | Holds on the water block. | The water tinted lime. Caption: "Cube dropped into the water. Illustrative only." |
| 5 | 4.9 to 7.0 | Hold. The cube is hidden. Final card: the pouch front, the net weight and the caption. | Holds, then fades out. | The pack front and the net weight. |
| 6 | (page only) | Reset. The cube grows back from 10% to 100% in 0.8 s and returns to hover. | None in the clip. | Used only on the interactive page. |

## Production notes

- **Clip length:** about 7 seconds at 24 frames a second, about 170 frames.
- **Render cost:** the 2K front at 64 samples took about 5 minutes a frame, so a full 2K clip would take many hours. A preview at 960 by 540 px and 32 samples needs a timing test before a length is promised.
- **Memory:** the free memory check comes first, as in the earlier renders.
- **Cheaper option:** record the interactive page in real time with a screen recorder. Its timings are already set in code.
- **Open choices:** Blender frame sequence or the page recording; which resolution; and whether the clip shows the caption.
