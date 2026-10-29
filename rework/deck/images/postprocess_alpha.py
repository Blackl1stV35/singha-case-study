"""Clean the alpha channel of a rendered PNG, in place.

The shadow-catcher floor picks up a very faint sky-light shade (alpha 1 to 8 of 255) far from the
cubes. It is invisible on its own but can show as a faint box once the PNG sits on the slide. Alpha at
or below KNEE goes to 0 and the rest is rescaled so that 255 stays 255. The cube (alpha 255) and the
contact shadow (alpha well above the knee) are not changed in any way that shows; RGB is not touched.

    python postprocess_alpha.py file1.png [file2.png ...]
"""
import sys

import numpy as np
from PIL import Image

KNEE = 7


def clean(path):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    a = arr[..., 3].astype(np.float32)
    out = np.clip((a - KNEE) * 255.0 / (255.0 - KNEE), 0, 255)
    arr[..., 3] = np.rint(out).astype(np.uint8)
    Image.fromarray(arr, "RGBA").save(path, optimize=True)
    return float((a == 0).mean()), float((arr[..., 3] == 0).mean())


if __name__ == "__main__":
    for p in sys.argv[1:]:
        before, after = clean(p)
        print("%s transparent %.1f%% -> %.1f%%" % (p, 100 * before, 100 * after))
