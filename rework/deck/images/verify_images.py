"""Measure the rendered deck PNGs against the rules in rework/deck/image_placeholders.md.

    python verify_images.py PNG_DIR [--json out.json]

Per file it reports size, RGBA mode, transparency at the border, how many separate pieces there are,
their framing, colour, and edge fringing, and marks each rule PASS or FAIL. It measures; it does not judge
realism or forbidden content (glass, water, text and so on), which are checked by eye on the composites.
"""
import sys
import json
import glob
import os
import colorsys

import numpy as np
from PIL import Image
from scipy import ndimage

FLAVOUR = ["#F7D23A", "#E9DC7B", "#C8453B", "#8E5A7C", "#E9A3B4"]
SIZES = {  # accepted (W, H) per id: 4K first, 2K second
    "P1": [(3072, 3840), (1638, 2048)],
    "P2": [(3840, 2880), (2048, 1536)],
    "P3": [(3840, 2880), (2048, 1536)],
    "P4": [(3840, 2880), (2048, 1536)],
    "P5": [(3840, 2880), (2048, 1536)],
    "P6": [(3840, 960), (2048, 512)],
}


def hex_hsv(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(r, g, b)


def hue_diff(a, b):
    d = abs(a - b) % 1.0
    return min(d, 1.0 - d) * 360.0


def analyse(path):
    name = os.path.basename(path)
    pid = name[:2]
    noshadow = "_noshadow" in name
    img = Image.open(path)
    res = {"file": name, "mode": img.mode, "size": img.size, "checks": {}}
    ck = res["checks"]
    ck["mode_RGBA"] = img.mode == "RGBA"
    ck["size_ok"] = tuple(img.size) in SIZES[pid]
    arr = np.array(img.convert("RGBA"))
    a = arr[..., 3]
    rgb = arr[..., :3].astype(np.float32)
    H, W = a.shape
    res["resolution_class"] = "4K" if max(W, H) >= 3072 else ("2K" if max(W, H) >= 2000 else "other")

    band = 24
    border = np.concatenate([a[:band].ravel(), a[-band:].ravel(), a[:, :band].ravel(), a[:, -band:].ravel()])
    res["border_alpha_max"] = int(border.max())
    ck["border_transparent"] = int(border.max()) == 0

    opaque = a >= 235
    lab, n = ndimage.label(opaque)
    areas = ndimage.sum(opaque, lab, range(1, n + 1)) if n else []
    min_area = 0.00004 * W * H
    idx = [i + 1 for i, ar in enumerate(areas) if ar >= min_area]
    objs = ndimage.find_objects(lab)
    pieces = []
    for i in idx:
        sl = objs[i - 1]
        m = lab == i
        er = ndimage.binary_erosion(m, iterations=max(2, W // 400))
        sel = er if er.sum() > 50 else m
        med = np.median(rgb[sel], axis=0)
        hsv = colorsys.rgb_to_hsv(*(med / 255.0))
        # brightest-quartile pixels approximate the lit face colour
        lum = rgb[sel].mean(axis=1)
        top = rgb[sel][lum >= np.percentile(lum, 70)].mean(axis=0)
        pieces.append({
            "x0": sl[1].start, "x1": sl[1].stop, "y0": sl[0].start, "y1": sl[0].stop,
            "area": float(areas[i - 1]), "median_rgb": [int(v) for v in med],
            "hsv": [round(v, 3) for v in hsv], "lit_rgb": [int(v) for v in top],
        })
    pieces.sort(key=lambda p: (p["x0"] + p["x1"]) / 2)
    res["pieces"] = len(pieces)
    if pieces:
        x0 = min(p["x0"] for p in pieces); x1 = max(p["x1"] for p in pieces)
        y0 = min(p["y0"] for p in pieces); y1 = max(p["y1"] for p in pieces)
        res["union"] = {"w": round((x1 - x0) / W, 3), "h": round((y1 - y0) / H, 3),
                        "cx": round((x0 + x1) / 2 / W, 3), "cy_from_bottom": round(1 - (y0 + y1) / 2 / H, 3)}
    soft = (a >= 8) & (a < 235)
    res["soft_alpha_pct"] = round(100 * float(soft.mean()), 2)
    res["soft_alpha_max_outside_cubes"] = int(a[~ndimage.binary_dilation(opaque, iterations=6)].max()) if (~ndimage.binary_dilation(opaque, iterations=6)).any() else 0

    # edge fringing: colour of anti-aliased rim pixels against the colour of the body next to them
    ring = (a >= 60) & (a <= 215) & ndimage.binary_dilation(opaque, iterations=3) & ~opaque
    if ring.sum() > 200 and pieces:
        body = ndimage.binary_erosion(opaque, iterations=max(3, W // 300))
        res["fringe_rgb_distance"] = round(float(np.linalg.norm(rgb[ring].mean(axis=0) - rgb[body].mean(axis=0))), 1)
    else:
        res["fringe_rgb_distance"] = None

    u = res.get("union", {})
    if pid == "P1":
        ck["one_cube"] = res["pieces"] == 1
        ck["cube_height_30pct"] = abs(u.get("h", 0) - 0.30) <= 0.05
        ck["cube_lower_centre"] = abs(u.get("cx", 0) - 0.5) <= 0.06 and 0.18 <= u.get("cy_from_bottom", 0) <= 0.42
    elif pid == "P2":
        ck["one_cube"] = res["pieces"] == 1
        ck["cube_height_46pct"] = abs(u.get("h", 0) - 0.46) <= 0.05
        ck["centred"] = abs(u.get("cx", 0) - 0.5) <= 0.06 and abs(u.get("cy_from_bottom", 0) - 0.5) <= 0.10
    elif pid == "P3":
        ck["one_cube"] = res["pieces"] == 1
        ck["cube_height_40pct"] = abs(u.get("h", 0) - 0.40) <= 0.05
        ck["centred"] = abs(u.get("cx", 0) - 0.5) <= 0.06 and abs(u.get("cy_from_bottom", 0) - 0.5) <= 0.10
    elif pid == "P4":
        ck["ten_pieces"] = res["pieces"] == 10
        ck["group_inside_frame"] = u.get("w", 1) <= 0.85 and u.get("h", 1) <= 0.75
        if pieces:
            sizes = [max(p["x1"] - p["x0"], p["y1"] - p["y0"]) / W for p in pieces]
            res["piece_max_dim_pct_of_width"] = [round(100 * s, 1) for s in sizes]
    elif pid == "P5":
        ck["three_pieces"] = res["pieces"] == 3
        ck["mostly_empty"] = u.get("w", 1) <= 0.45 and u.get("h", 1) <= 0.35
    elif pid == "P6":
        ck["five_cubes"] = res["pieces"] == 5
        if res["pieces"] == 5:
            cxs = [(p["x0"] + p["x1"]) / 2 for p in pieces]
            gaps = np.diff(cxs)
            res["spacing_cv_pct"] = round(100 * float(gaps.std() / gaps.mean()), 1)
            hs = [p["y1"] - p["y0"] for p in pieces]
            res["height_cv_pct"] = round(100 * float(np.std(hs) / np.mean(hs)), 1)
            ck["evenly_spaced"] = res["spacing_cv_pct"] <= 6.0
            ck["equal_heights"] = res["height_cv_pct"] <= 5.0
            ck["width_86pct"] = abs(u.get("w", 0) - 0.86) <= 0.06
            ok = []
            for p, hx in zip(pieces, FLAVOUR):
                eh, es, ev = hex_hsv(hx)
                h, s, v = p["hsv"]
                ok.append(hue_diff(h, eh) <= 16.0 and abs(s - es) <= 0.25)
            res["flavour_colour_match"] = ok
            ck["flavour_colours_in_order"] = all(ok)
    if pid in ("P1", "P2", "P3", "P4", "P5") and pieces:
        eh, es, ev = hex_hsv("#F7D23A")
        ok = [hue_diff(p["hsv"][0], eh) <= 14.0 and abs(p["hsv"][1] - es) <= 0.25 for p in pieces]
        ck["lemon_colour"] = all(ok)

    if noshadow:
        ck["no_shadow_in_alpha"] = res["soft_alpha_pct"] <= 1.0 + 100 * float(np.mean(ndimage.binary_dilation(opaque, iterations=3) & ~opaque))
        ck["no_shadow_far_from_cubes"] = res["soft_alpha_max_outside_cubes"] == 0
    else:
        ck["has_soft_shadow"] = res["soft_alpha_pct"] > 0.3
        ck["shadow_soft_not_dark"] = res["soft_alpha_max_outside_cubes"] <= 150
    if res["fringe_rgb_distance"] is not None:
        ck["no_edge_fringe"] = res["fringe_rgb_distance"] <= 60.0
    res["pass"] = all(ck.values())
    return res


def main():
    d = sys.argv[1]
    out = None
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
    results = [analyse(p) for p in sorted(glob.glob(os.path.join(d, "P*.png")))]
    for r in results:
        bad = [k for k, v in r["checks"].items() if not v]
        print("%-44s %-4s %s %s pieces=%d union=%s fringe=%s soft=%s%%  %s" % (
            r["file"], r["resolution_class"], "PASS" if r["pass"] else "FAIL", r["size"], r["pieces"],
            r.get("union"), r["fringe_rgb_distance"], r["soft_alpha_pct"], ("FAILED: " + ",".join(bad)) if bad else ""))
    if out:
        with open(out, "w") as f:
            json.dump(results, f, indent=1, default=str)
    print("TOTAL %d files, %d pass" % (len(results), sum(r["pass"] for r in results)))


if __name__ == "__main__":
    main()
