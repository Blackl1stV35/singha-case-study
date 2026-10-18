"""Portrait pack labels for the single-serve pouch (front and back), 70 by 90 mm at about 380 dpi.

Front: the SINGHA lion emblem is the hero on the deep ink field, the product name and descriptor sit
below it, one flat lime cube sits in the spare space beside the instruction, and the bottom band
carries the sweetener disclosure, the pack format and the net weight. Back: the mandatory copy in
reading order. Copy comes only from style_tokens.json, so the pack and the record cannot drift apart.

Writes label_front.png and label_back.png (1050 by 1350 px, RGB, no text chunks).
"""
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
TOKENS = HERE / "style_tokens.json"
EMBLEM = HERE / "assets" / "singha_emblem.png"
W, H = 1050, 1350
MARGIN = 84
LIVE_W = W - 2 * MARGIN

DISPLAY_BOLD = r"C:\Windows\Fonts\georgiab.ttf"
TEXT_REG = r"C:\Windows\Fonts\leelawad.ttf"
TEXT_BOLD = r"C:\Windows\Fonts\leelawdb.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def wrap(text, f, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if f.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(text, path, start, min_size, max_w):
    size = start
    while size > min_size and font(path, size).getlength(text) > max_w:
        size -= 2
    return size


def draw_cube(d, cx, cy, s, C):
    """One flat cube in oblique projection: top off-white, front lime, side lime-deep, ink outline."""
    e = s
    ox, oy = round(0.42 * e), round(-0.30 * e)
    fx, fy = cx - (e + ox) / 2, cy + e / 2
    f_tl, f_tr = (fx, fy - e), (fx + e, fy - e)
    f_br, f_bl = (fx + e, fy), (fx, fy)
    b_tl, b_tr = (fx + ox, fy - e + oy), (fx + e + ox, fy - e + oy)
    b_br, b_bl = (fx + e + ox, fy + oy), (fx + ox, fy + oy)
    faces = [([f_tl, f_tr, b_tr, b_tl], C["off-white"]),
             ([f_tl, f_tr, f_br, f_bl], C["lime"]),
             ([f_tr, f_br, b_br, b_tr], C["lime-deep"])]
    for poly, fill in faces:
        d.polygon(poly, fill=fill, outline=C["ink"], width=5)


def build_front(tok, C):
    cf = tok["copy_front"]
    name_line = cf[0]
    trade, descriptor = name_line.split(" · ", 1)
    drop = next(x for x in cf if x.startswith("Drop one cube"))
    serving = next(x for x in cf if x.startswith("Serving:"))
    sweet = next(x for x in cf if x.startswith("Contains an intensive sweetener"))
    pouch = next(x for x in cf if x.startswith("Single-serve pouch"))
    net = next(x for x in cf if x.startswith("Net weight"))

    img = Image.new("RGB", (W, H), C["off-white"])
    d = ImageDraw.Draw(img)

    # Hero: ink field with the lion emblem centred.
    band = 700
    d.rectangle([0, 0, W, band], fill=C["ink"])
    emblem = Image.open(EMBLEM).convert("RGBA")
    # The cut-out leaves a light fringe on the lion's edge; one erosion pass removes it on the ink field.
    emblem.putalpha(emblem.getchannel("A").filter(ImageFilter.MinFilter(3)))
    ew = 640
    eh = round(emblem.height * ew / emblem.width)
    em = emblem.resize((ew, eh), Image.LANCZOS)
    img.paste(em, ((W - ew) // 2, (band - eh) // 2), em)
    d.rectangle([0, band, W, band + 10], fill=C["lime"])

    # Name and descriptor.
    size = fit_size(trade, DISPLAY_BOLD, 96, 60, LIVE_W)
    d.text((MARGIN, 838), trade, font=font(DISPLAY_BOLD, size), fill=C["ink"], anchor="ls")
    d.text((MARGIN, 896), descriptor, font=font(TEXT_BOLD, 44), fill=C["ink-soft"], anchor="ls")

    # Instruction and serving, with the flat cube in the spare space on the right.
    body = font(TEXT_REG, 44)
    y = 980
    for line in wrap(drop, body, 640):
        d.text((MARGIN, y), line, font=body, fill=C["ink"], anchor="ls")
        y += 56
    d.text((MARGIN, y + 16), serving, font=font(TEXT_REG, 34), fill=C["ink"], anchor="ls")
    draw_cube(d, 862, 1000, 150, C)

    # Bottom ink band: sweetener disclosure, pack format and net weight.
    d.rectangle([0, 1190, W, H], fill=C["ink"])
    sweet_head, sweet_tail = sweet.split(": ", 1) if ": " in sweet else (sweet, "")
    d.text((MARGIN, 1236), sweet_head + ":", font=font(TEXT_BOLD, 36), fill=C["off-white"], anchor="ls")
    d.text((MARGIN, 1282), sweet_tail, font=font(TEXT_REG, 36), fill=C["off-white"], anchor="ls")
    d.text((MARGIN, 1326), pouch, font=font(TEXT_REG, 30), fill=C["off-white"], anchor="ls")
    nf = font(TEXT_REG, 30)
    d.text((W - MARGIN, 1326), net, font=nf, fill=C["off-white"], anchor="rs")
    return img


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


def build_back(tok, C):
    cb = tok["copy_back"]
    img = Image.new("RGB", (W, H), C["off-white"])
    d = ImageDraw.Draw(img)
    name_line = tok["copy_front"][0]
    trade = name_line.split(" · ", 1)[0]
    size = fit_size(trade, DISPLAY_BOLD, 64, 44, LIVE_W)
    d.text((MARGIN, 120), trade, font=font(DISPLAY_BOLD, size), fill=C["ink"], anchor="ls")
    d.rectangle([MARGIN, 150, W - MARGIN, 153], fill=C["lime"])

    top, bottom = 218, H - 60
    for size in range(36, 27, -1):  # largest size that fits the face; 33 px is 2.2 mm (token minimum)
        body, head = font(TEXT_REG, size), font(TEXT_BOLD, size)
        lh, gap = round(size * 1.32), round(size * 0.55)
        paras = [runs_wrap(item_runs(item, body, head), LIVE_W) for item in cb]
        height = sum(len(p) * lh + gap for p in paras)
        if top + height <= bottom:
            break
    else:
        raise SystemExit("back copy does not fit the pack face at 28 px")
    y = top
    for para in paras:
        for line in para:
            x = MARGIN
            for word, f in line:
                d.text((x, y), word, font=f, fill=C["ink"], anchor="ls")
                x += f.getlength(word) + f.getlength(" ")
            y += lh
        y += gap
    return img, size


def check_copy(tok):
    import make_label  # the forbidden-wording list lives there; importing it runs no build
    text = " ".join(tok["copy_front"] + tok["copy_back"])
    hits = [p for p in make_label.FORBIDDEN if re.search(p, text, re.I)]
    if hits:
        raise SystemExit("forbidden wording in pack copy: %s" % hits)
    organiser = make_label.organiser_digest_hits(text)
    if organiser:
        raise SystemExit("organiser digest in pack copy: %s" % organiser)


def main():
    tok = json.loads(TOKENS.read_text(encoding="utf-8"))
    C = {k: hexrgb(v) for k, v in tok["colour"].items()}
    check_copy(tok)
    front = build_front(tok, C)
    back, back_size = build_back(tok, C)
    front.save(HERE / "label_front.png", optimize=True)
    back.save(HERE / "label_back.png", optimize=True)
    print("portrait labels written: %dx%d; back copy at %d px (%.2f mm)" % (W, H, back_size, back_size / 15.0))


if __name__ == "__main__":
    main()
