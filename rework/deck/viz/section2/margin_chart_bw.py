"""Margin chart for slide 5, black and white, Times New Roman 24 pt.

    python margin_chart_bw.py OUT_DIR

Reads the two margin rows from rework/screen/ambient_variation_results.json (median, p05, p95 of the
per-cell ratio), converts to percent as (ratio - 1) x 100, and rounds half away from zero to one decimal.

Layout is searched, not hand-tuned: each candidate spacing is drawn, every text box is measured against
the other text boxes, the lines and the dot markers, and the first candidate with zero overlaps is saved.
The defect list of every rejected candidate is printed, so the loop shows what it found.
"""
import sys
import os
import json
import itertools
from decimal import Decimal, ROUND_HALF_UP

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "..", "..", "..", "screen", "ambient_variation_results.json")
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 24
XMIN, XMAX = -4, 14


def pct(ratio):
    return (Decimal(str(ratio)) - 1) * 100


def r1(x):
    return Decimal(x).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def load_rows():
    m = json.load(open(MODEL, encoding="utf-8"))["comparison_with_rework_46_47"]
    return [
        ("Age gradient alone", m["age_gradient_only_ratio_men25_34_over_35_44"]),
        ("Full model, with potassium exclusion and temperature noise", m["per_cell_ratio_men25_34_over_35_44"]),
    ]


def draw(rows, val_dy, rng_dy, row_gap, out=None):
    """Draw one layout. Returns the list of overlap defects found (empty list = clean)."""
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.40, 0.14, 0.56, 0.80])
    ax.set_facecolor("white")
    ax.set_xlim(XMIN, XMAX)
    top, axis_y, foot_y = 3 * row_gap + 1.2, -1.0, -2.2
    ax.set_ylim(foot_y - 0.4, top)
    # zero line starts at the axis, so the 0% tick label and the footnote stay clear of it
    ax.plot([0, 0], [axis_y, top - 0.6], color="black", lw=2.5, zorder=1)
    ax.plot([XMIN, XMAX], [axis_y, axis_y], color="black", lw=1.5, zorder=1)
    for t in (0, 5, 10):
        ax.plot([t, t], [axis_y, axis_y - 0.12], color="black", lw=1.5, zorder=1)
        ax.text(t, axis_y - 0.18, "%d%%" % t, ha="center", va="top", color="black")
    ax.text(-0.4, top - 0.2, "Men 35 to 44 ahead", ha="right", va="center", color="black")
    ax.text(0.4, top - 0.2, "Men 25 to 34 ahead", ha="left", va="center", color="black")
    ys = [2 * row_gap, 0.0]
    for (label, d), y in zip(rows, ys):
        lo_d, md_d, hi_d = pct(d["p05"]), pct(d["median"]), pct(d["p95"])
        lo, md, hi = float(lo_d), float(md_d), float(hi_d)
        # row label sits in the gutter left of the plot, so it never crosses the zero line
        ax.text(-0.03, y, label, transform=ax.get_yaxis_transform(), ha="right", va="center", color="black")
        ax.plot([lo, hi], [y, y], color="black", lw=4, solid_capstyle="butt", zorder=3)
        for v in (lo, hi):
            ax.plot([v, v], [y - 0.12, y + 0.12], color="black", lw=4, zorder=3)
        ax.scatter([md], [y], s=600, color="black", edgecolors="white", linewidths=3, zorder=4)
        ax.text(md, y + val_dy, "+%s%%" % r1(md_d), ha="center", va="bottom", color="black")
        # low end sits left of its tick so the label never crosses the zero line
        ax.text(lo - 0.15, y + rng_dy, ("minus " if lo_d < 0 else "plus ") + str(abs(r1(lo_d))), ha="right", va="top", color="black")
        ax.text(hi + 0.15, y + rng_dy, ("minus " if hi_d < 0 else "plus ") + str(abs(r1(hi_d))), ha="left", va="top", color="black")
    ax.text(XMIN + 0.1, foot_y, "Both ranges include zero. Model result under stated assumptions; 90% range.",
            ha="left", va="top", color="black")
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    items = []
    for t in ax.texts:
        if t.get_text():
            items.append(("text: " + t.get_text().replace("\n", " ")[:40], t.get_window_extent(rend)))
    for ln in ax.lines:
        items.append(("line at y=%.2f" % ln.get_ydata()[0] if len(set(ln.get_ydata())) == 1 else "vertical line", ln.get_window_extent(rend)))
    # each dot measured at its true size: 600 pt^2 marker plus a 3 pt white ring
    from matplotlib.transforms import Bbox
    radius_px = (600 ** 0.5 / 2 + 3) * 100 / 72
    for col in ax.collections:
        for (x, y) in col.get_offsets():
            cx, cy = ax.transData.transform((x, y))
            items.append(("dot", Bbox([[cx - radius_px, cy - radius_px], [cx + radius_px, cy + radius_px]])))
    defects = []
    pad = 3
    for i, j in itertools.combinations(range(len(items)), 2):
        a_name, a = items[i]
        b_name, b = items[j]
        if a_name.startswith("line") and b_name.startswith("line"):
            continue
        if a_name.startswith("line") or b_name.startswith("line") or a_name.startswith("text") or b_name.startswith("text"):
            if a_name.startswith("text") or b_name.startswith("text"):
                if a.padded(pad).overlaps(b):
                    defects.append("%s  <->  %s" % (a_name, b_name))
    if out and not defects:
        fig.savefig(out, facecolor="white", bbox_inches="tight", pad_inches=0.4)
    plt.close(fig)
    return defects


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    rows = load_rows()
    path = os.path.join(out_dir, "slide5_margin_chart_bw.png")
    attempts = 0
    first_defects = None
    for row_gap, val_dy, rng_dy in itertools.product([1.4, 1.7, 2.0, 2.3], [0.5, 0.6, 0.7], [-0.22, -0.38]):
        attempts += 1
        defects = draw(rows, val_dy, rng_dy, row_gap, out=None)
        if first_defects is None:
            first_defects = defects
        if not defects:
            draw(rows, val_dy, rng_dy, row_gap, out=path)
            print("clean layout after %d attempts: row_gap=%s val_dy=%s rng_dy=%s" % (
                attempts, row_gap, val_dy, rng_dy))
            print("saved", path)
            if first_defects:
                print("defects found on the first attempt (fixed by the loop):")
                for d in first_defects:
                    print("  -", d)
            return
    print("no clean layout in %d attempts; first attempt defects:" % attempts)
    for d in first_defects or []:
        print("  -", d)
    sys.exit(1)


if __name__ == "__main__":
    main()
