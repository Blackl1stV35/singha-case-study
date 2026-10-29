"""Section 2 ("The case", slides 3 to 5) visualization proposal, drawn with matplotlib (CPU only).

    python build_section2_viz.py OUT_DIR

Writes three 1920 x 1080 slide mocks (slide3_gap.png, slide4_leverage_the_can.png,
slide5_consumers.png), a three-up overview sheet, and section2_viz_data.json with every plotted number,
its source and its tier. Figures come from rework/deck/deck_content.md (slides 3 to 5) and, for the two
margin intervals on slide 5, from the team model results rework/screen/ambient_variation_results.json
(read from the file at build time, not typed in). Nothing is invented: a value with no stated range is drawn
without a range.

Design tokens follow the Canva deck: paper #F6F4EE, ink #15171A, grey #6B6F76, rules #D9D6CC, one accent
(lemon #F2C94C) per slide, white cards with a 1 px ink outline and radius 12, flat fills, no shadows.
The text avoids em dashes, en dashes and middle dots (checked at the end of the build).
"""
import sys
import os
import json
from decimal import Decimal, ROUND_HALF_UP

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

W, H = 1920, 1080
PAPER, INK, GREY, RULE, LEMON, WHITE = "#F6F4EE", "#15171A", "#6B6F76", "#D9D6CC", "#F2C94C", "#FFFFFF"
SERIF, SANS = "Georgia", "Segoe UI"
NAV = ["Opening", "The case", "The product", "The economics", "The plan", "Appendix"]
MODEL_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "screen",
                          "ambient_variation_results.json")
ALL_TEXT = []  # every string drawn, for the character check


def tw(s, size, family=SANS, weight="normal"):
    fp = FontProperties(family=family, weight=weight)
    return TextPath((0, 0), s, size=size, prop=fp).get_extents().width


class Slide:
    def __init__(self):
        self.fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        self.fig.patch.set_facecolor(PAPER)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, W)
        self.ax.set_ylim(H, 0)
        self.ax.axis("off")

    # primitives -------------------------------------------------------------------------------
    def rect(self, x, y, w, h, fc=None, ec=None, lw=1.0, r=0, z=1, ls="-", alpha=1.0):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=%s" % r,
                           fc=fc or "none", ec=ec or "none", lw=lw * 0.72, linestyle=ls, zorder=z, alpha=alpha)
        self.ax.add_patch(p)

    def card(self, x, y, w, h, fc=WHITE, z=1):
        self.rect(x, y, w, h, fc=fc, ec=INK, lw=1.0, r=12, z=z)

    def line(self, x0, y0, x1, y1, color=INK, lw=1.0, z=3, cap="butt", ls="-"):
        self.ax.plot([x0, x1], [y0, y1], color=color, lw=lw * 0.72, zorder=z, solid_capstyle=cap, linestyle=ls)

    def dot(self, x, y, d, fc=INK, ring=WHITE, z=6):
        self.ax.scatter([x], [y], s=(d * 0.72) ** 2, c=fc, edgecolors=ring, linewidths=2 * 0.72, zorder=z)

    def text(self, x, y, s, size, weight="normal", color=INK, family=SANS, ha="left", z=5):
        """x, y = left (or centre / right) and top of the line box; size in px."""
        ALL_TEXT.append(s)
        self.ax.text(x, y + size * 0.86, s, fontsize=size * 0.72, fontweight=weight, color=color,
                     family=family, ha=ha, va="baseline", zorder=z)

    def wrap(self, s, size, width, weight="normal", family=SANS):
        lines, cur = [], ""
        for word in s.split(" "):
            trial = (cur + " " + word).strip()
            if tw(trial, size, family, weight) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, size, width, weight="normal", color=INK, family=SANS, lh=1.32, ha="left"):
        yy = y
        for ln in self.wrap(s, size, width, weight, family):
            self.text(x, yy, ln, size, weight, color, family, ha)
            yy += size * lh
        return yy

    def pill(self, x, y, s, size=16, fc=INK, fg=WHITE, pad=14, h=None, weight="bold"):
        h = h or size + 16
        w = tw(s, size, SANS, weight) + 2 * pad
        self.rect(x, y, w, h, fc=fc, ec=INK if fc == WHITE else None, lw=1.0, r=8, z=4)
        self.text(x + w / 2, y + (h - size) / 2 - 1, s, size, weight, fg, ha="center", z=6)
        return w

    def can_icon(self, cx, top, w=140, h=250):
        """Flat can: body, rim ellipse and base ellipse (not a phone)."""
        from matplotlib.patches import Ellipse
        e = 34
        self.ax.add_patch(Ellipse((cx, top + h - e / 2), w, e, fc=WHITE, ec=INK, lw=3 * 0.72, zorder=3))
        self.rect(cx - w / 2, top + e / 2, w, h - e, fc=WHITE, z=4)
        self.line(cx - w / 2, top + e / 2, cx - w / 2, top + h - e / 2, INK, 3, z=5)
        self.line(cx + w / 2, top + e / 2, cx + w / 2, top + h - e / 2, INK, 3, z=5)
        self.ax.add_patch(Ellipse((cx, top + e / 2), w, e, fc=RULE, ec=INK, lw=3 * 0.72, zorder=6))
        self.rect(cx - 16, top + e / 2 - 7, 32, 12, fc=WHITE, ec=INK, lw=2, r=6, z=7)  # pull tab

    def chip(self, x, y, s, size=20, fc=WHITE, pad=14, h=40, weight="normal"):
        w = tw(s, size, SANS, weight) + 2 * pad
        self.rect(x, y, w, h, fc=fc, ec=INK, lw=1.0, r=8, z=4)
        self.text(x + w / 2, y + (h - size) / 2 - 1, s, size, weight, INK, ha="center", z=6)
        return w

    def title(self, s):
        lines = self.wrap(s, 54, 1720, "bold", SERIF)
        if len(lines) == 2:  # balance the two lines so the second one is not an orphan
            words = s.split(" ")
            best = None
            for k in range(1, len(words)):
                a, b = " ".join(words[:k]), " ".join(words[k:])
                m = max(tw(a, 54, SERIF, "bold"), tw(b, 54, SERIF, "bold"))
                if best is None or m < best[0]:
                    best = (m, a, b)
            if best[0] <= 1720:
                lines = [best[1], best[2]]
        y = 66
        for ln in lines:
            self.text(100, y, ln, 54, "bold", INK, SERIF)
            y += 62
        return y

    def nav(self, current):
        for i, label in enumerate(NAV):
            cx = 560 + 160 * i
            on = label == current
            self.text(cx, 1022, label, 20, "bold" if on else "normal", INK if on else GREY, ha="center")

    def save(self, path):
        self.fig.savefig(path, dpi=100, facecolor=PAPER)
        plt.close(self.fig)


# helpers ---------------------------------------------------------------------------------------
def r1(x):
    """One decimal, half away from zero, as a string with an explicit sign for margins."""
    return Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def margin_pct(ratio):
    return (Decimal(str(ratio)) - 1) * 100


def range_axis(s, x0, x1, y, lo, hi, vmin, vmax, ticks, tick_fmt, bar_h=12, color=INK, label_size=16):
    """Hairline axis with tick labels and a thick range bar from lo to hi (data units vmin..vmax)."""
    def X(v):
        return x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    s.line(x0, y, x1, y, RULE, 2, z=2)
    for t in ticks:
        s.line(X(t), y - 5, X(t), y + 5, RULE, 2, z=2)
        s.text(X(t), y + 10, tick_fmt(t), label_size, "normal", GREY, ha="center")
    s.rect(X(lo), y - bar_h / 2, X(hi) - X(lo), bar_h, fc=color, r=bar_h / 2, z=4)
    return X


# slide 3 -----------------------------------------------------------------------------------------
def slide3(path, data):
    s = Slide()
    s.title("Cans are the lemon drink on the shelf. No dissolvable cube was found.")

    # left: three stat lines, each with a small visual
    lx, lw_ = 100, 700
    y0 = 225
    ch = 190
    gap = 18
    # stat 1: two bars (share of respondents)
    s.card(lx, y0, lw_, ch)
    for i, (v, txt) in enumerate([(44, "strictly try to reduce sugar"), (27, "are open to sugar or salt alternatives")]):
        yy = y0 + 22 + i * 68
        s.text(lx + 30, yy, "%d%%" % v, 54, "bold", INK)
        s.text(lx + 190, yy + 2, txt, 24, "normal", INK)
        s.rect(lx + 190, yy + 38, 470, 10, fc=RULE, r=5, z=2)
        s.rect(lx + 190, yy + 38, 470 * v / 100, 10, fc=INK, r=5, z=3)
    s.text(lx + 30, y0 + ch - 34, "Mintel, February 2026, S", 18, "normal", GREY)
    data["slide3"]["stat1"] = {"strictly_try_to_reduce_sugar_pct": 44, "open_to_sugar_or_salt_alternatives_pct": 27,
                               "source": "Mintel, February 2026", "tier": "S"}

    # stat 2: price range on a THB axis
    y1 = y0 + ch + gap
    s.card(lx, y1, lw_, ch)
    s.text(lx + 30, y1 + 20, "THB 12.40 to 14.63", 46, "bold", INK)
    s.para(lx + 30, y1 + 78, "per 330 ml: sugar-free lemon and lime 24-can packs at named sellers (S, 20 October 2026)",
           20, 640, "normal", GREY)
    range_axis(s, lx + 70, lx + 630, y1 + 142, 12.40, 14.63, 10, 16, [10, 12, 14, 16], lambda t: "THB %d" % t)
    data["slide3"]["stat2"] = {"price_per_330ml_thb": [12.40, 14.63], "what": "sugar-free lemon and lime 24-can packs",
                               "where": "named sellers", "date": "20 October 2026", "tier": "S", "axis_thb": [10, 16]}

    # stat 3: where cubes are found
    y2 = y1 + ch + gap
    s.card(lx, y2, lw_, ch)
    s.dot(lx + 46, y2 + 46, 24, INK, WHITE)
    s.text(lx + 76, y2 + 28, "Drink cubes sell overseas (waterdrop; Ricola)", 26, "bold", INK)
    s.dot(lx + 46, y2 + 118, 24, LEMON, INK)
    s.para(lx + 76, y2 + 90, "None was found on sale in Thailand in listings read on 20 October 2026", 26, 600, "bold", INK, lh=1.25)
    data["slide3"]["stat3"] = {"overseas": "found (waterdrop; Ricola)",
                               "thailand": "none found in listings read on 20 October 2026"}

    # right: two-column exhibit
    ex, ew, gx = 840, 478, 24
    ey, eh = y0, 3 * ch + 2 * gap
    s.card(ex, ey, ew, eh, WHITE)
    s.card(ex + ew + gx, ey, ew, eh, LEMON)
    s.text(ex + 30, ey + 26, "Today: a 330 ml can", 30, "bold", INK)
    s.para(ex + ew + gx + 30, ey + 26, "Proposed: one cube in 330 ml of water", 30, ew - 60, "bold", INK, lh=1.2)
    # can icon (flat)
    cx = ex + ew / 2
    s.can_icon(cx, ey + 150)
    s.text(cx, ey + 262, "330 ml", 28, "bold", INK, ha="center", z=8)
    # ghost cube icon (dashed = not found)
    cx2 = ex + ew + gx + ew / 2
    sz = 120
    k = 0.866
    top = [(cx2, ey + 170), (cx2 + k * sz, ey + 170 + sz / 2), (cx2, ey + 170 + sz), (cx2 - k * sz, ey + 170 + sz / 2)]
    left = [(cx2 - k * sz, ey + 170 + sz / 2), (cx2, ey + 170 + sz), (cx2, ey + 170 + 2 * sz), (cx2 - k * sz, ey + 170 + 1.5 * sz)]
    right = [(cx2, ey + 170 + sz), (cx2 + k * sz, ey + 170 + sz / 2), (cx2 + k * sz, ey + 170 + 1.5 * sz), (cx2, ey + 170 + 2 * sz)]
    for poly in (top, left, right):
        s.ax.add_patch(Polygon(poly, closed=True, fc="none", ec=INK, lw=3 * 0.72, ls=(0, (5, 4)), zorder=4, joinstyle="round"))
    # pills and captions
    pw = s.pill(ex + 30, ey + 452, "ON THE SHELF IN THAILAND", 17)
    s.para(ex + 30, ey + 500, "Lemon and lime cans, sugar-free, at named sellers.", 24, ew - 60, "normal", GREY)
    s.pill(ex + ew + gx + 30, ey + 452, "NOT FOUND ON SALE IN THAILAND", 17)
    s.para(ex + ew + gx + 30, ey + 500, "No dissolvable cube was found.", 24, ew - 60, "normal", INK)

    # out-of-scope bar
    by = 874
    s.card(100, by, 1720, 122)
    s.pill(130, by + 18, "OUT OF SCOPE", 18)
    s.para(130, by + 62, "Market size. Press values disagree (NielsenIQ THB 70,772 million to November 2024; THB 66,000 million to January 2024; "
           "2025 values THB 67,000 million to THB 76,900 million). No level is stated, and no market is sized from them.",
           20, 1660, "normal", INK, lh=1.3)
    s.nav("The case")
    s.save(path)


# slide 4 -----------------------------------------------------------------------------------------
def slide4(path, data):
    s = Slide()
    s.title("The Singha lemon can gives the cube a flavour family and routes to test.")
    cw, gap = 413, 22
    xs = [100 + i * (cw + gap) for i in range(4)]
    cy, chh = 218, 372
    for x in xs:
        s.card(x, cy, cw, chh)

    # card 1: brand
    x = xs[0] + 26
    s.text(x, cy + 20, "Brand", 28, "bold", INK)
    yy = s.para(x, cy + 64, "Launched August 2020 (press; later articles say late 2020).", 21, cw - 52)
    s.text(x, yy + 14, "Later flavours", 18, "normal", GREY)
    cxx, cyy = x, yy + 44
    for label in ["Yuzu", "Red", "Ume", "Pink", "Lemon Cream"]:
        w = tw(label, 20) + 28
        if cxx + w > xs[0] + cw - 26:
            cxx, cyy = x, cyy + 48
        cxx += s.chip(cxx, cyy, label) + 10
    cyy += 62
    wl = s.chip(x, cyy, "Lemon can", fc=WHITE, weight="bold")
    s.text(x + wl + 12, cyy + 8, "the taste reference", 20, "normal", INK)
    data["slide4"]["brand"] = {"launched": "August 2020 (press; later articles say late 2020)",
                               "later_flavours": ["Yuzu", "Red", "Ume", "Pink", "Lemon Cream"]}

    # card 2: pack and price (THB per can)
    x = xs[1] + 26
    s.text(x, cy + 20, "Pack and price", 28, "bold", INK)
    s.text(x, cy + 62, "330 ml can; prices in THB a can", 21, "normal", GREY)
    ax0, ax1, ay = x + 6, xs[1] + cw - 34, cy + 190
    X = range_axis(s, ax0, ax1, ay, 13.54, 13.75, 12, 18, [12, 14, 16, 18], lambda t: "%d" % t, bar_h=14)
    s.dot(X(16.0), ay, 18, INK, WHITE)
    s.dot(X(17.0), ay, 18, INK, WHITE)
    s.text(ax0 - 6, ay - 54, "24-can packs 13.54 to 13.75", 17, "bold", INK)
    s.text(X(16.0), ay + 40, "Launch 16", 17, "bold", INK, ha="center")
    s.text(X(17.0) + 22, ay - 54, "Single 17.00", 17, "bold", INK, ha="center")
    s.para(x, ay + 78, "THB 16 at launch. Online on 20 October 2026: a single lemon can at THB 17.00 (Lotus's); 24-can packs at THB 13.54 to 13.75 a can.",
           18, cw - 52, "normal", INK, lh=1.28)
    data["slide4"]["pack_and_price_thb_per_can"] = {"launch": 16.0, "single_can_lotus_20_oct_2026": 17.00,
                                                    "pack_24_per_can_20_oct_2026": [13.54, 13.75], "axis_thb": [12, 18]}

    # card 3: channels
    x = xs[2] + 26
    s.text(x, cy + 20, "Channels", 28, "bold", INK)
    cxx, cyy = x, cy + 70
    for label in ["7-Eleven", "Lotus's", "Makro", "Singha Online Shop"]:
        w = tw(label, 22) + 28
        if cxx + w > xs[2] + cw - 26:
            cxx, cyy = x, cyy + 54
        cxx += s.chip(cxx, cyy, label, size=22, h=44) + 10
    s.para(x, cyy + 80, "The lemon can was listed online on 20 October 2026.", 21, cw - 52, "normal", INK)
    data["slide4"]["channels"] = ["7-Eleven", "Lotus's", "Makro", "Singha Online Shop"]

    # card 4: proof
    x = xs[3] + 26
    s.text(x, cy + 20, "Proof", 28, "bold", INK)
    yy = cy + 66
    s.para(x, yy, "The maker's page says 0% sugar.", 21, cw - 52)
    s.pill(x, yy + 36, "COMPANY CLAIM", 15, fc=WHITE, fg=INK, pad=10, h=30)
    s.text(x, yy + 82, "Blind taste test against the can.", 21, "normal", INK)
    s.rect(x - 12, yy + 124, cw - 28, 118, fc=LEMON, r=8, z=2)  # the one accent: the review point
    s.para(x, yy + 136, "Review point: if 7% or more of cube buyers would otherwise have bought a can, the value model is rerun.",
           21, cw - 56, "normal", INK)

    # derived estimates band
    s.text(100, 614, "DERIVED FROM PUBLIC DATA; NOT SINGHA FIGURES", 18, "bold", GREY)
    gy, gh = 646, 238
    g = [
        dict(label="Cans a year", value="about 119 million", pt=119, lo=83, hi=137, vmax=150, ends=("83", "137"), zero="0", top="150 million"),
        dict(label="A year, to the producer", value="about THB 880 million", pt=None, lo=None, hi=None, vmax=None, ends=None, zero=None, top=None),
        dict(label="Can variable cost, before aluminium", value="about THB 3.3", pt=3.3, lo=2.6, hi=3.9, vmax=5, ends=("2.6", "3.9"), zero="0", top="THB 5"),
        dict(label="Line-hours for 200,000 cubes", value="about 79", pt=79, lo=45, hi=152, vmax=160, ends=("45", "152"), zero="0", top="160 hours"),
    ]
    vsize = min(38, min(int((cw - 52) / tw(d["value"], 1, SANS, "bold")) for d in g))  # one size that fits every value
    data["slide4"]["derived_estimates_not_singha_figures"] = []
    for x, d in zip(xs, g):
        s.card(x, gy, cw, gh)
        s.text(x + 26, gy + 20, d["label"], 20, "bold", GREY)
        s.text(x + 26, gy + 58, d["value"], vsize, "bold", INK)
        a0, a1, ay = x + 34, x + cw - 34, gy + 176
        if d["pt"] is None:
            s.text(x + 26, gy + 128, "Range not stated", 20, "normal", GREY)
            data["slide4"]["derived_estimates_not_singha_figures"].append({"label": d["label"], "point": "about THB 880 million a year to the producer", "range": None})
            continue
        def X(v, a0=a0, a1=a1, vmax=d["vmax"]):
            return a0 + v / vmax * (a1 - a0)
        s.line(a0, ay, a1, ay, RULE, 2, z=2)
        s.text(a0, ay + 12, d["zero"], 16, "normal", GREY, ha="center")
        s.text(a1, ay + 12, d["top"], 16, "normal", GREY, ha="right")
        s.line(X(d["lo"]), ay, X(d["hi"]), ay, INK, 3, z=4, cap="round")
        for v in (d["lo"], d["hi"]):
            s.line(X(v), ay - 9, X(v), ay + 9, INK, 3, z=4)
        s.dot(X(d["pt"]), ay, 18, INK, WHITE)
        s.text(X(d["lo"]), ay - 40, d["ends"][0], 17, "normal", GREY, ha="center")
        s.text(X(d["hi"]), ay - 40, d["ends"][1], 17, "normal", GREY, ha="center")
        data["slide4"]["derived_estimates_not_singha_figures"].append({"label": d["label"], "point": d["pt"], "range": [d["lo"], d["hi"]], "axis_max": d["vmax"]})

    # out of scope bar
    by = 902
    s.card(100, by, 1720, 100)
    s.pill(130, by + 14, "OUT OF SCOPE", 18)
    s.para(300, by + 21, "The filling plant; the can's unit cost; line capacity at the group's plants; the number of outlets that carry the can; store shelf prices; retail reach.",
           20, 1480, "normal", INK, lh=1.25)
    s.text(130, by + 66, "Brand use: the lion and SINGHA need written sign-off from the brand owner before any pack print.", 19, "normal", GREY)
    s.nav("The case")
    s.save(path)


# slide 5 -----------------------------------------------------------------------------------------
def slide5(path, data, model):
    s = Slide()
    s.title("Consumers want less sugar without losing taste. Men aged 25 to 34 are the lead to test.")

    # three stat tiles
    tw_, tg = 560, 20
    tiles = [("90%", "of urban consumers drink carbonated drinks out of home"), ("more than 22", "purchases a year"), ("about THB 19", "per trip")]
    ty, th_ = 228, 165
    for i, (big, small) in enumerate(tiles):
        x = 100 + i * (tw_ + tg)
        s.card(x, ty, tw_, th_)
        s.text(x + 26, ty + 16, big, 58, "bold", INK)
        s.para(x + 26, ty + 88, small, 22, tw_ - 52, "normal", GREY)
    s.text(1820, ty + th_ + 10, "Kantar, April 2024, S", 18, "normal", GREY, ha="right")
    data["slide5"]["tiles"] = {"urban_consumers_drink_carbonated_out_of_home_pct": 90, "purchases_a_year": "more than 22",
                               "spend_per_trip_thb": "about 19", "source": "Kantar, April 2024", "tier": "S"}

    # left card: three lines
    ly, lh_ = 438, 560
    s.card(100, ly, 760, lh_)
    x = 130
    s.text(x, ly + 18, "Taste", 28, "bold", INK)
    s.para(x, ly + 58, "About two in five name taste as a decision factor (Innova, October 2025, S).", 21, 700)
    s.text(x, ly + 132, "Preference for sweetness (Mintel, February 2026, S)", 19, "normal", GREY)
    bx, bw, by = x, 700, ly + 162
    segs = [(40, "full sweetness", INK, WHITE), (36, "less sweet", GREY, WHITE), (24, "undecided", RULE, INK)]
    cx0 = bx
    for v, lab, fc, fg in segs:
        w = bw * v / 100 - 2
        s.rect(cx0, by, w, 44, fc=fc, r=4, z=3)
        s.text(cx0 + w / 2, by + 9, "%d%%" % v, 22, "bold", fg, ha="center", z=6)
        s.text(cx0 + w / 2, by + 52, lab, 18, "normal", GREY, ha="center")
        cx0 += bw * v / 100
    data["slide5"]["sweetness_preference_pct"] = {"full sweetness": 40, "less sweet": 36, "undecided": 24, "source": "Mintel, February 2026", "tier": "S"}
    s.line(x, ly + 250, 830, ly + 250, RULE, 2, z=2)
    s.text(x, ly + 266, "Lead", 28, "bold", INK)
    s.para(x, ly + 306, "In the model, men aged 25 to 34 who drink alcohol rank first among six drinker groups in 94% of simulated outcomes. "
           "The confirmed category band is men aged 27 to 44 (Bangkok sample, n = 400, S).", 21, 700)
    s.line(x, ly + 420, 830, ly + 420, RULE, 2, z=2)
    s.pill(x, ly + 438, "OUT OF SCOPE", 17)
    s.para(x, ly + 478, "A buyer profile for Singha Lemon Soda. Men aged 45 to 59 are a later volume segment, pended.", 20, 700, "normal", INK)

    # right card: margin with 90% range crossing zero
    rx, rw = 880, 940
    s.card(rx, ly, rw, lh_)
    s.text(rx + 30, ly + 18, "Margin of men aged 25 to 34 over men aged 35 to 44", 28, "bold", INK)
    s.text(rx + 30, ly + 58, "Purchase intent, model result (DERIVED), 90% range", 20, "normal", GREY)
    ax0, ax1 = rx + 300, rx + rw - 50   # left gutter of 270 px holds the row labels
    vmin, vmax = -3.6, 14.0
    X = lambda v: ax0 + (v - vmin) / (vmax - vmin) * (ax1 - ax0)
    top, bot = ly + 120, ly + 440
    s.rect(X(0), top, X(vmax) - X(0), bot - top, fc=LEMON, r=0, z=1, alpha=0.30)   # the one accent: men 25 to 34 ahead
    s.rect(X(vmin), top, X(0) - X(vmin), bot - top, fc=RULE, r=0, z=1, alpha=0.45)
    for t in (0, 5, 10):
        s.line(X(t), top, X(t), bot, RULE if t else INK, 2 if t else 2.5, z=2)
        s.text(X(t), bot + 8, "%d%%" % t, 18, "normal", GREY, ha="center")
    s.text(X(0) + 12, top + 8, "Men 25 to 34 ahead", 18, "bold", INK)
    s.text(X(0) - 10, top + 8, "Men 35 to 44", 16, "bold", GREY, ha="right")
    s.text(X(0) - 10, top + 28, "ahead", 16, "bold", GREY, ha="right")
    s.text(X(0), bot + 32, "0 = no difference", 18, "normal", GREY, ha="center")

    cmp = model["comparison_with_rework_46_47"]
    rows = [
        ("Age gradient alone", cmp["age_gradient_only_ratio_men25_34_over_35_44"]),
        ("Full model: with potassium exclusion and assumed temperature noise", cmp["per_cell_ratio_men25_34_over_35_44"]),
    ]
    data["slide5"]["margin_over_men_35_44_pct"] = []
    for i, (lab, d) in enumerate(rows):
        yc = top + 110 + i * 120
        lo, md, hi = (margin_pct(d["p05"]), margin_pct(d["median"]), margin_pct(d["p95"]))
        s.para(rx + 30, yc - 22 - (13 if i else 0), lab, 21, 250, "bold", INK, lh=1.25)
        s.line(X(float(lo)), yc, X(float(hi)), yc, INK, 3, z=5, cap="round")
        for v in (lo, hi):
            s.line(X(float(v)), yc - 10, X(float(v)), yc + 10, INK, 3, z=5)
        s.dot(X(float(md)), yc, 22, INK, WHITE)
        sign = lambda v: ("plus " if v >= 0 else "minus ") + str(abs(r1(v)))
        s.text(X(float(md)), yc - 42, "+%s%%" % r1(md), 24, "bold", INK, ha="center")
        s.text(X(float(lo)) - 4, yc + 16, sign(lo), 17, "normal", GREY, ha="right")
        s.text(X(float(hi)), yc + 16, sign(hi), 17, "normal", GREY, ha="center")
        data["slide5"]["margin_over_men_35_44_pct"].append({
            "row": lab, "ratio_median": d["median"], "ratio_p05": d["p05"], "ratio_p95": d["p95"],
            "margin_pct_median": float(md), "margin_pct_p05": float(lo), "margin_pct_p95": float(hi),
            "shown": {"median": "+%s" % r1(md), "p05": sign(lo), "p95": sign(hi)}, "interval_touches_1": d["interval_touches_1"],
            "source": "rework/screen/ambient_variation_results.json, comparison_with_rework_46_47", "tier": "DERIVED (ASSUMPTION and PROXY inputs)"})
    s.para(rx + 30, ly + lh_ - 64, "Both ranges include no difference. A model result under stated assumptions, not a consumer finding; the pilot tests it.",
           19, rw - 60, "normal", GREY, lh=1.3)
    data["slide5"]["rank_first_probability"] = {"men_25_34_among_six_drinker_groups": model["lenses"]["per_cell_drinkers"]["full_run"]["prob_rank_first"]["M25"],
                                                "shown": "94%"}
    s.nav("The case")
    s.save(path)


# overview ------------------------------------------------------------------------------------------
def overview(out_dir):
    from PIL import Image, ImageDraw, ImageFont
    names = [("slide3_gap.png", "Slide 3. The gap"), ("slide4_leverage_the_can.png", "Slide 4. Leverage the can"),
             ("slide5_consumers.png", "Slide 5. Consumers and the drinking way")]
    tw_, th_ = 1200, 675
    pad, cap = 40, 56
    sheet = Image.new("RGB", (tw_ + 2 * pad, pad + len(names) * (th_ + cap + pad) - 0), "#E9E6DC")
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 30)
    y = pad
    for fn, cap_txt in names:
        im = Image.open(os.path.join(out_dir, fn)).convert("RGB").resize((tw_, th_), Image.LANCZOS)
        d.text((pad, y), cap_txt, fill="#15171A", font=font)
        sheet.paste(im, (pad, y + cap))
        y += cap + th_ + pad
    sheet.save(os.path.join(out_dir, "section2_overview.png"), optimize=True)


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    with open(MODEL_JSON, encoding="utf-8") as f:
        model = json.load(f)
    data = {"slide3": {}, "slide4": {}, "slide5": {},
            "note": "Slides 3 to 5 figures are from rework/deck/deck_content.md; the slide 5 margin ranges are read from the team model results."}
    slide3(os.path.join(out, "slide3_gap.png"), data)
    slide4(os.path.join(out, "slide4_leverage_the_can.png"), data)
    slide5(os.path.join(out, "slide5_consumers.png"), data, model)
    overview(out)
    bad = [t for t in ALL_TEXT if any(c in t for c in "\u2014\u2013\u00b7")]
    data["drawn_text"] = ALL_TEXT
    data["forbidden_characters_found"] = bad
    with open(os.path.join(out, "section2_viz_data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print("built", out, "strings", len(ALL_TEXT), "forbidden", bad)


if __name__ == "__main__":
    main()
