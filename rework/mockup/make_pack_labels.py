"""Pack labels for the Tarlo single-serve pouch (front and back), 70 by 90 mm at 15 px per mm.

Front (ink field): the product name above the lion, a lime lion with a violet keyline as the hero,
one violet diagonal cut, and the drop instruction, serving line, sweetener disclosure, pouch format
and net weight below the cut. Back (paper ground): a violet lion head with the name, the mandatory
copy (including the preparation line) at the largest size that fits, and the net weight band.

Copy comes only from style_tokens.json. The net weight is read from copy_front (it matches
dimensions_mm.net_weight_g, which holds the derivation). Writes label_front.png and label_back.png
(1050 by 1350 px, RGB).
"""
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
TOKENS = HERE / "style_tokens.json"
LION = HERE / "assets" / "singha_lion.png"
W, H = 1050, 1350
M = 75  # 5 mm safe margin

DISPLAY = r"C:\Windows\Fonts\georgiab.ttf"
TEXT_REG = r"C:\Windows\Fonts\leelawad.ttf"
TEXT_BOLD = r"C:\Windows\Fonts\leelawdb.ttf"

UPSCALE = 3  # the lion is resampled 3x before recolouring, so edges and the keyline stay smooth

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
    """Accept a hex string or an (r, g, b) tuple."""
    return hexrgb(c) if isinstance(c, str) else tuple(c)


def tracked(draw, x, y, text, fnt, fill, track):
    """Draw letter by letter with extra tracking in px. Returns the x after the last letter."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="ls")
        x += fnt.getlength(ch) + track
    return x


def item_runs(item, body, head):
    """Split 'Label: text' into a bold label run and a regular text run; plain items stay regular."""
    label, sep, rest = item.partition(": ")
    if not sep:
        return [(item, body)]
    return [(label + ":", head), (" " + rest, body)]


def runs_wrap(runs, max_w):
    """Greedy word wrap over (text, font) runs. Returns lines of (word, font)."""
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


def lion_art(fill, line, target_h, crop=None, keyline=None, keyline_out_px=0):
    """Recolour the authorised lion: gold areas take the fill, dark contour lines take the line colour.

    crop limits the source to a box (the back head). keyline is a colour for a ring around the
    silhouette, keyline_out_px wide in output pixels. target_h is the lion height in output pixels.
    """
    src_img = Image.open(LION).convert("RGBA")
    if crop:
        src_img = src_img.crop(crop)
    src_img = src_img.resize((src_img.width * UPSCALE, src_img.height * UPSCALE), Image.LANCZOS)
    src = np.array(src_img).astype(np.float32)
    rgb, alpha = src[..., :3], src[..., 3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    solid = alpha > 127
    out = np.zeros(src.shape, dtype=np.uint8)
    out[solid & (lum >= 90)] = (*_rgb(fill), 255)
    out[solid & (lum < 90)] = (*_rgb(line), 255)
    out[..., 3] = alpha.astype(np.uint8)
    scale = target_h / float(src_img.height)
    lion_rgba = Image.fromarray(out, "RGBA")
    pad = int(round(keyline_out_px / scale)) if keyline and keyline_out_px else 0
    canvas = Image.new("RGBA", (lion_rgba.width + 2 * pad, lion_rgba.height + 2 * pad), (0, 0, 0, 0))
    if pad:
        mask = Image.new("L", canvas.size, 0)
        mask.paste(Image.fromarray(np.where(solid, 255, 0).astype(np.uint8), "L"), (pad, pad))
        grown = mask
        for _ in range(pad):  # stepwise 3x3 dilation keeps the ring smooth at a modest cost
            grown = grown.filter(ImageFilter.MaxFilter(3))
        ring = (np.array(grown) > 0) & (np.array(mask) == 0)
        key = np.zeros((canvas.height, canvas.width, 4), dtype=np.uint8)
        key[ring] = (*_rgb(keyline), 255)
        canvas = Image.fromarray(key, "RGBA")
    canvas.alpha_composite(lion_rgba, (pad, pad))
    new_size = (round(canvas.width * scale), round(canvas.height * scale))
    return canvas.resize(new_size, Image.LANCZOS)


def check_copy(tok):
    import make_label  # the forbidden-wording list lives there; importing it runs no build
    text = " ".join(tok["copy_front"] + tok["copy_back"])
    # "potassium bicarbonate" is the ingredient name, not a carbonation claim, so the word is set aside for the check.
    text = re.sub(r"bicarbonate", "", text, flags=re.I)
    hits = [p for p in make_label.FORBIDDEN if re.search(p, text, re.I)]
    if hits:
        raise SystemExit("forbidden wording in pack copy: %s" % hits)
    organiser = make_label.organiser_digest_hits(text)
    if organiser:
        raise SystemExit("organiser digest in pack copy: %s" % organiser)


def build_front(tok, C):
    cf = tok["copy_front"]
    name, descriptor = cf[0].split(" · ", 1)
    drop = next(x for x in cf if x.startswith("Drop one cube"))
    serving = next(x for x in cf if x.startswith("Serving:"))
    sweet = next(x for x in cf if x.startswith("Contains an intensive sweetener"))
    pouch = next(x for x in cf if x.startswith("Single-serve pouch"))
    net = next(x for x in cf if x.startswith("Net weight"))

    img = Image.new("RGB", (W, H), C["ink"])
    d = ImageDraw.Draw(img)

    # Name above the lion: the largest size that fits the live width.
    size = 260
    while size > 120 and font(DISPLAY, size).getlength(name.upper()) > W - 2 * M:
        size -= 4
    base = M + 0.70 * size
    d.text((M, base), name.upper(), font=font(DISPLAY, size), fill=C["paper"], anchor="ls")
    tracked(d, M, base + 72, descriptor.upper(), font(TEXT_BOLD, 46), C["lime"], 6)

    # Lion hero: lime with a violet keyline, bleeding slightly off the right trim.
    art = lion_art(C["lime"], C["ink"], 520, keyline=C["violet"], keyline_out_px=28)
    lion_top = 360
    img.paste(art, (W - art.width + 30, lion_top - 28), art)

    # One violet diagonal cut divides the hero from the instruction band.
    d.line([(0, 1000), (W, 915)], fill=C["violet"], width=22)

    # Instruction band, ink with paper text.
    body = font(TEXT_REG, 46)
    y = 1060
    for line in runs_wrap([(drop, body)], W - 2 * M):
        x = M
        for word, f in line:
            d.text((x, y), word, font=f, fill=C["paper"], anchor="ls")
            x += f.getlength(word) + f.getlength(" ")
        y += 56
    d.text((M, y + 10), serving, font=font(TEXT_REG, 34), fill=C["paper"], anchor="ls")
    d.text((M, y + 56), sweet, font=font(TEXT_REG, 30), fill=C["paper"], anchor="ls")
    d.text((M, 1262), pouch, font=font(TEXT_REG, 30), fill=C["paper"], anchor="ls")
    d.text((W - M, 1262), net, font=font(TEXT_BOLD, 46), fill=C["paper"], anchor="rs")
    return img


def build_back(tok, C):
    cb = tok["copy_back"]
    net = next(x for x in tok["copy_front"] if x.startswith("Net weight"))
    img = Image.new("RGB", (W, H), C["paper"])
    d = ImageDraw.Draw(img)

    # Header: violet lion head, then the name.
    head = lion_art(C["violet"], C["ink"], 150)  # the whole lion at header size; a head crop clipped the crest
    img.paste(head, (M, M), head)
    name = tok["copy_front"][0].split(" · ", 1)[0].upper()
    x = M + head.width + 80
    d.text((x, M + 75 + 26), name, font=font(DISPLAY, 80), fill=C["ink"], anchor="ls")
    d.rectangle([M, 256, W - M, 259], fill=C["ink"])

    # Mandatory copy: the largest size from 36 down to 28 px (2.4 to 1.9 mm) that fits the space.
    top, bottom = 290, 1190
    for sz in range(36, 27, -1):
        body, head_f = font(TEXT_REG, sz), font(TEXT_BOLD, sz)
        lh, gap = round(sz * 1.2), round(sz * 0.35)
        paras = [runs_wrap(item_runs(item, body, head_f), W - 2 * M) for item in cb]
        height = sum(len(p) * lh + gap for p in paras)
        if top + height <= bottom:
            break
    else:
        raise SystemExit("back copy does not fit the pack face at 28 px")
    y = top
    for para in paras:
        for line in para:
            x = M
            for word, f in line:
                d.text((x, y), word, font=f, fill=C["ink"], anchor="ls")
                x += f.getlength(word) + f.getlength(" ")
            y += lh
        y += gap

    # Net weight band, ink, paper text.
    d.rectangle([0, 1205, W, H], fill=C["ink"])
    d.text((W - M, 1270), net, font=font(TEXT_BOLD, 46), fill=C["paper"], anchor="rs")
    return img, sz


def main():
    tok = json.loads(TOKENS.read_text(encoding="utf-8"))
    C = {k: hexrgb(v) for k, v in tok["colour"].items()}
    check_copy(tok)
    front = build_front(tok, C)
    back, back_size = build_back(tok, C)
    front.save(HERE / "label_front.png", optimize=True)
    back.save(HERE / "label_back.png", optimize=True)
    print("labels written: %dx%d; back copy at %d px (%.2f mm)" % (W, H, back_size, back_size / 15.0))


if __name__ == "__main__":
    main()
