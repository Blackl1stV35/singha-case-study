"""Pack labels for Lime Cube, 70 by 90 mm at 15 px per mm (1050 by 1350 px).

Revised to the merged segment design (workflow wf_87c8ab5d-bf0, 19 October 2026). Layout positions are in
millimetres from the design, converted at MM px per mm. Copy comes only from style_tokens.json.

Front (charcoal field): the authorised lion in silver foil as the hero, the LIME CUBE name plate under it,
a foil rule, the instruction block, and one lime wedge at bottom right. Back (paper): the name, a foil-free
ink hairline, the preparation line, and the mandatory copy at the largest size that fits. The back lion is
dropped in this revision: at 10 mm it breaks the 25 mm minimum reproduction width in the design.

Gate G1 (the lion on a non-alcoholic pack) is NOT cleared. These labels are a proposal draft only.
Writes label_front.png and label_back.png.
"""
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
TOKENS = HERE / "style_tokens.json"
LION = HERE / "assets" / "singha_lion_clean.png"  # background and specks removed
W, H = 1050, 1350
MM = 15                    # px per millimetre
PT = 25.4 / 72 * MM        # px per point, about 5.29
M = 6 * MM                 # 6 mm text margin, 90 px

DISPLAY = r"C:\Windows\Fonts\georgiab.ttf"
TEXT_REG = r"C:\Windows\Fonts\leelawad.ttf"
TEXT_BOLD = r"C:\Windows\Fonts\leelawdb.ttf"

UPSCALE = 3  # the lion is resampled 3x before recolouring, so edges stay smooth

_cache = {}


def font(path, size):
    key = (path, int(round(size)))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, int(round(size)))
    return _cache[key]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb(c):
    return hexrgb(c) if isinstance(c, str) else tuple(c)


def tracked_width(text, fnt, track):
    return sum(fnt.getlength(ch) + track for ch in text) - track


def tracked(draw, x, y, text, fnt, fill, track):
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="ls")
        x += fnt.getlength(ch) + track
    return x


def item_runs(item, body, head):
    label, sep, rest = item.partition(": ")
    if not sep:
        return [(item, body)]
    return [(label + ":", head), (" " + rest, body)]


def runs_wrap(runs, max_w):
    words = [(w, f) for text, f in runs for w in text.split(" ") if w]
    lines, cur, cur_w = [], [], 0.0
    for w, f in words:
        if cur and cur_w + f.getlength(" ") + f.getlength(w) > max_w:
            lines.append(cur)
            cur, cur_w = [], 0.0
        cur_w += (f.getlength(" ") if cur else 0) + f.getlength(w)
        cur.append((w, f))
    if cur:
        lines.append(cur)
    return lines


def draw_line(d, x, y, line, fill):
    for word, f in line:
        d.text((x, y), word, font=f, fill=fill, anchor="ls")
        x += f.getlength(word) + f.getlength(" ")


def lion_art(fill, line, target_h, crop=None):
    """Recolour the authorised lion: gold areas take the fill, dark contour lines take the line colour."""
    src_img = Image.open(LION).convert("RGBA")
    if crop:
        src_img = src_img.crop(crop)
    src_img = src_img.resize((src_img.width * UPSCALE, src_img.height * UPSCALE), Image.LANCZOS)
    src = np.array(src_img).astype(np.float32)
    rgb, alpha = src[..., :3], src[..., 3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    # Gold artwork is saturated; outlines and grey edge blends are not. Keying on saturation keeps the grey
    # halo out of the silver fill, so it drops into the background instead.
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    solid = alpha > 127
    gold = solid & (sat >= 0.30) & (lum >= 60)
    out = np.zeros(src.shape, dtype=np.uint8)
    out[gold] = (*_rgb(fill), 255)
    out[solid & ~gold] = (*_rgb(line), 255)
    out[..., 3] = alpha.astype(np.uint8)
    scale = target_h / float(src_img.height)
    art = Image.fromarray(out, "RGBA")
    return art.resize((round(art.width * scale), round(art.height * scale)), Image.LANCZOS)


def check_copy(tok):
    import make_label  # the forbidden-wording list lives there; importing it runs no build
    text = " ".join(tok["copy_front"] + tok.get("copy_back_top", []) + tok["copy_back"])
    # "potassium bicarbonate" is the ingredient name, not a carbonation claim, so the word is set aside.
    text = re.sub(r"bicarbonate", "", text, flags=re.I)
    hits = [p for p in make_label.FORBIDDEN if re.search(p, text, re.I)]
    if hits:
        raise SystemExit("forbidden wording in pack copy: %s" % hits)
    organiser = make_label.organiser_digest_hits(text)
    if organiser:
        raise SystemExit("organiser digest in pack copy: %s" % organiser)


def build_front(tok, C):
    cf = tok["copy_front"]
    name, drop, serving, sweet, fmt = cf[0], cf[1], cf[2], cf[3], cf[4]
    img = Image.new("RGB", (W, H), C["ink"])
    d = ImageDraw.Draw(img)

    # Lion hero: silver foil, box 40 by 34 mm, centred at x 35 mm, top at y 12 mm.
    art = lion_art(C["foil"], C["ink"], 34 * MM)
    img.paste(art, (round(35 * MM - art.width / 2), 12 * MM), art)

    # Name plate: Georgia Bold capitals, tracking 0.12 em, centred at x 35 mm, baseline y 55 mm.
    nf = font(DISPLAY, 16 * PT)
    track = 0.12 * 16 * PT
    tracked(d, round(35 * MM - tracked_width(name.upper(), nf, track) / 2), 55 * MM,
            name.upper(), nf, C["paper"], track)

    # Foil rule, 0.3 mm, from (6, 62) to (64, 58) mm.
    d.line([(6 * MM, 62 * MM), (64 * MM, 58 * MM)], fill=C["foil"], width=5)

    # Instruction block, left at 6 mm, measure to 55 mm.
    measure = (55 - 6) * MM
    y = 66.5 * MM
    for line in runs_wrap([(drop, font(TEXT_BOLD, 7 * PT))], measure):
        draw_line(d, M, round(y), line, C["paper"])
        y += 3.3 * MM
    d.text((M, 73 * MM), serving, font=font(TEXT_REG, 7 * PT), fill=C["paper"], anchor="ls")
    d.text((M, 76 * MM), sweet, font=font(TEXT_REG, 6.5 * PT), fill=C["paper"], anchor="ls")
    # Format and net weight: the design's baseline is 79.5 mm; moved to 78.5 mm so the descender clears 80 mm.
    d.text((M, 78.5 * MM), fmt, font=font(TEXT_BOLD, 6.5 * PT), fill=C["paper"], anchor="ls")

    # Lime wedge, bleeding off the right and bottom edges, no text.
    d.polygon([(70 * MM, 72 * MM), (70 * MM, 90 * MM), (44 * MM, 90 * MM)], fill=C["lime"])
    return img


def build_back(tok, C):
    img = Image.new("RGB", (W, H), C["paper"])
    d = ImageDraw.Draw(img)

    # Header: the name at 13 pt, left at 6 mm, baseline 16 mm. No back lion (see the module note).
    d.text((M, 16 * MM), tok["copy_front"][0].upper(),
           font=font(DISPLAY, 13 * PT), fill=C["ink"], anchor="ls")
    d.rectangle([M, 19.5 * MM - 2, W - M, 19.5 * MM + 1], fill=C["ink"])

    # Preparation line, 6.8 pt, two lines at most.
    prep_runs = item_runs(tok["copy_back_top"][0], font(TEXT_REG, 6.8 * PT), font(TEXT_BOLD, 6.8 * PT))
    y = 23 * MM
    for line in runs_wrap(prep_runs, W - 2 * M):
        draw_line(d, M, round(y), line, C["ink"])
        y += 3.0 * MM
    top = round(y + 0.6 * MM)

    # Mandatory copy: the largest size from 34 down to 26 px that fits above the format line.
    bottom = 1140
    for sz in range(34, 25, -1):
        body, head = font(TEXT_REG, sz), font(TEXT_BOLD, sz)
        lh, gap = round(sz * 1.15), round(sz * 0.3)
        paras = [runs_wrap(item_runs(item, body, head), W - 2 * M) for item in tok["copy_back"]]
        height = sum(len(p) * lh + gap for p in paras)
        if top + height <= bottom:
            break
    else:
        raise SystemExit("back copy does not fit above the format line at 26 px")
    y = top
    for para in paras:
        for line in para:
            draw_line(d, M, y, line, C["ink"])
            y += lh
        y += gap

    # Format line, bold, above the bottom seal zone (80 mm = 1200 px).
    d.text((M, 1177), tok["copy_front"][4], font=font(TEXT_BOLD, 6.5 * PT), fill=C["ink"], anchor="ls")
    return img, sz


def main():
    tok = json.loads(TOKENS.read_text(encoding="utf-8"))
    C = {k: _rgb(v) for k, v in tok["colour"].items()}
    check_copy(tok)
    front = build_front(tok, C)
    back, back_size = build_back(tok, C)
    front.save(HERE / "label_front.png", optimize=True)
    back.save(HERE / "label_back.png", optimize=True)
    print("labels written: %dx%d; back copy at %d px (%.2f mm)" % (W, H, back_size, back_size / MM))


if __name__ == "__main__":
    main()
