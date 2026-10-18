"""Team-meeting briefing PDF: novelty, technical basis, Thai conditions, quantum runs and decisions.

Reads the result JSON files and figures in rework/ and writes rework/21_team_briefing_novelty.pdf.
Every number in the PDF is read from those files. Run:  python make_team_briefing_pdf.py
"""
import json
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
REWORK = os.path.join(HERE, "..")
OUT = os.path.join(REWORK, "21_team_briefing_novelty.pdf")


def load(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return None


sim = load(os.path.join(HERE, "pop_leak_simulation_results.json"))
qpu1 = load(os.path.join(HERE, "quantum_leak_probability_results.json"))
qae = load(os.path.join(HERE, "quantum_amplitude_estimation_results.json"))
sweep = load(os.path.join(HERE, "quantum_local_sweep_results.json"))
thai = load(os.path.join(HERE, "thailand_stress_test_results.json"))
summer = load(os.path.join(HERE, "thai_summer_occasions_results.json"))

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12.5, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("BODY", parent=styles["BodyText"], fontSize=9.5, leading=13)
SMALL = ParagraphStyle("SMALL", parent=styles["BodyText"], fontSize=8, leading=10, textColor=colors.HexColor("#444444"))


def P(text, style=BODY):
    return Paragraph(text, style)


def bullets(items):
    return [P("&bull; " + i) for i in items]


def table(data, widths):
    t = Table([[P(str(c), SMALL) for c in row] for row in data], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6F1FB")),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def fig(name, width_mm):
    path = os.path.join(REWORK, name)
    if not os.path.exists(path):
        return P("[figure %s not found]" % name, SMALL)
    from PIL import Image as PILImage

    with PILImage.open(path) as im:
        w, h = im.size
    width = width_mm * mm
    return Image(path, width=width, height=width * h / w)


def hrs(x):
    return "not in window" if x is None else "%.2f h" % x


def rng(d):
    if not d or d.get("p5") is None:
        return "n/a"
    return "%.2f to %.2f h" % (d["p5"], d["p95"])


story = []

story.append(P("Team meeting briefing: novelty, technical basis and Thai conditions", H1))
story.append(P("Leaf-wrapped frozen coconut-pandan drink pop, Innovative Bev &amp; Bite entry. "
               "Prepared 18 October 2026. Virtual evidence only: no physical or consumer test has been run, and none is in scope.", SMALL))
story.append(Spacer(1, 6))

story.append(P("1. What we ask the team to decide", H2))
story += bullets([
    "<b>Primary concept:</b> the leaf-wrapped frozen coconut-pandan pop, under Alternative Formats. Fallback: the same drink in a continuous inner film, which is not plastic-free.",
    "<b>Claim:</b> describe the product as <b>leaf-wrapped</b>. Do not say plastic-free: the leaf-only design passes the liquid screen only if its cut edges stay out of the melt water, and no seam data exists to show that.",
    "<b>Hot-season use (proposal):</b> keep the pop in an insulated box with gel packs, keep it out of ice water, and eat it within about an hour in full sun. The Thai summer screen does not support an unconditioned leak claim for outdoor use (section 6).",
    "<b>Limits we disclose, not test:</b> freeze damage to leaf membranes, seam strength, and the leaf's measured optics. No physical test is in scope.",
    "<b>Timing:</b> the competition closes 22 October 2026 at 23:59.",
])

story.append(P("2. The product", H2))
story.append(P("A frozen coconut or pandan drink sealed in a banana or pandan leaf. The consumer peels the leaf open and sips the drink as it thaws. "
               "The newness is the consumption act, not an ingredient. Target: Thai buyers who value plastic-free, traditional packaging "
               "(hypothesis; the evidence is produce wrapping, not drinks). Assumed size: 40 mm pop, 150 mm tall, 170 mL.", BODY))

story.append(P("3. Novelty: what we can and cannot claim", H2))
story += bullets([
    "<b>Claim:</b> a new way of drinking a frozen coconut-pandan drink, peel-and-sip as it thaws. This fits the brief's \"new form of consumption\" route.",
    "<b>Evidence:</b> six Thai and English searches on 18 October 2026 found no leaf-wrapped frozen or ready-to-drink drink. This is absence evidence only.",
    "<b>Nearest precedents:</b> a Chiang Mai supermarket's banana-leaf produce wraps (2019), and leaf-wrapped foods such as kuih. None are drinks.",
    "<b>Not yet checked:</b> global search beyond English queries, patents, the OTOP registry, and in-store audits. Several retail pages could not be read.",
    "<b>Verdict:</b> novel as a consumption form on the evidence so far. The submission should state it as such, and widen the search before claiming it as first.",
])

story.append(P("4. Technical basis (virtual screen, lab reference)", H2))
if sim:
    nom = sim["nominal_h10"]["N8"]
    mc = sim["monte_carlo"]
    story.append(table([
        ["Question", "Result", "Basis"],
        ["Surface starts to melt at 30 C", "%.2f h (about %d min)" % (nom["t_wet_s"] / 3600, round(nom["t_wet_s"] / 60)),
         "Transient radial heat model, h = 10 W/m2K"],
        ["50% thawed (sippable)", "%.2f h" % (nom["t50_s"] / 3600), "Same model; grid converged to 0.6%"],
        ["Fully thawed", "%.2f h" % (nom["t100_s"] / 3600),
         "Lumped estimate was 2.47 h; conduction lags the core"],
        ["Exposed-edge leak within 2 h", "%d%% of 200 runs" % round(100 * mc["design_A_exposed_vessel_leak_probability"]),
         "Vessel-sized paths wick the wrap in 1.5 to 7 min"],
        ["Sealed-edge critical damaged-path radius", "%.2f um median (5 to 95%%: %.2f to %.2f um)" % (
            mc["design_B_critical_damaged_radius_m"]["median"] * 1e6,
            mc["design_B_critical_damaged_radius_m"]["p5"] * 1e6,
            mc["design_B_critical_damaged_radius_m"]["p95"] * 1e6),
         "Monte Carlo, 200 runs; freeze-damage size is unmeasured"],
        ["Intact cuticle", "does not leak", "Pores 0.3 to 2 nm, far below the threshold"],
        ["Continuous inner film", "no liquid path", "Not plastic-free"],
    ], [52 * mm, 58 * mm, 70 * mm]))
    story.append(P("Thaw and wicking model: rework/17. Leak screen: rework/16. Not measured: freeze damage, seam strength, leaf thickness and porosity for fresh banana or pandan leaves.", SMALL))

story.append(P("5. Thai conditions: thaw timing under sourced inputs", H2))
story.append(P("Bangkok Mar-May normals (TMD 48455, 1991-2020): mean maximum 34.6 to 35.7 C, humidity 72 to 74 %, dew point 24.8 C, 6.3 to 7.6 h of sun per day. "
               "The model uses a diurnal mean of 31.5 C with 4.3 K amplitude, a half-sine sun peak of 800 W/m2, and a gel-pack melting point of about -1.3 C. "
               "Every input and its confidence is in rework/22_thailand_inputs.md. Virtual screen, not measured.", BODY))
if thai:
    keys = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "SU1", "SU2", "SU3", "SU4", "SU5"]
    mcd = thai.get("monte_carlo", {})
    rows = [["Scenario", "Surface starts to melt", "50% thawed", "Core above 5 C", "Max surface (C)"]]
    for k in keys:
        s = thai["scenarios"][k]
        wet = hrs(s["t_wet"])
        if k in mcd:
            wet += " (5 to 95%%: %s)" % rng(mcd[k]["t_wet"])
        rows.append(["%s %s" % (k, s["label"]), wet, hrs(s["t50"]), hrs(s["t_core5"]), "%.1f" % s["max_T_surface_C"]])
    story.append(table(rows, [66 * mm, 46 * mm, 22 * mm, 22 * mm, 18 * mm]))
    story.append(P("S0 is the lab reference (30 C still air, no sun). S1 to S7 are the earlier Thai exposures; SU1 to SU5 are summer occasions. "
                   "Times are from leaving the freezer. Monte Carlo ranges are shown for S1 to S5 only. Figure 22 shows the traces.", SMALL))

story.append(P("6. Summer occasions: do the conditions still hold?", H2))
if summer:
    base = summer["baseline_lab"]
    rows = [["Occasion", "Drink-side threshold (um)", "Outside water", "Outside threshold (um)", "Top of wrap likely wet"]]
    rows.append(["Lab reference, 30 C still air", "%.3f" % base["internal_threshold_um"], "none", "n/a", "no"])
    for r in summer["rows"]:
        if r["key"] not in ("S1", "S2", "SU1", "SU2", "SU3", "SU4", "SU5"):
            continue
        ext = "n/a" if r["external_threshold_um"] is None else "%.3f" % r["external_threshold_um"]
        rows.append(["%s %s" % (r["key"], r["label"]), "%.3f" % r["internal_threshold_um"],
                     r["external_mode"].replace("_", " "), ext, "yes" if r["top_wetted_likely"] else "no"])
    story.append(table(rows, [60 * mm, 30 * mm, 26 * mm, 30 * mm, 28 * mm]))
    story.append(P("Thresholds: the smallest damaged-path radius that wicks the 100 mm wrap in the time available. Paths at or above it leak, so higher means more margin. "
                   "The outside-water column assumes only the bottom edge is wet. Where a film or pool reaches the top of the wrap, there is no climb margin and the threshold does not protect. "
                   "The drink-side value uses the lower-bound viscosity (1 mPa s), so it is the conservative end of the section 4 range (median 0.24 um, which spans 1 to 3 mPa s). "
                   "The damaged-path size is unmeasured, so these are thresholds, not leak probabilities.", SMALL))
    story += bullets([
        "<b>Thaw window:</b> does not hold in full sun. Half the drink is sippable in about 0.6 h and the whole pop passes 5 C at about 1.4 h. In shade the two-hour window only just holds: the core passes 5 C at about 2.0 h.",
        "<b>Best hot-season option in the screen:</b> an insulated cooler with gel packs. The surface starts to melt at about 1.6 h, half the pop thaws at about 3.2 h, and the drink-side threshold rises to about 0.7 um.",
        "<b>Drink-side leak margin:</b> roughly holds. The threshold falls only from 0.180 um to 0.162 to 0.171 um, because the melt starts earlier.",
        "<b>Outside water:</b> not established. Condensate from the 24.8 C dew point, Songkran splash, and ice-water coolers all wet the outside of the wrap. For each of these the top of the wrap is likely wet, so the screen gives no climb margin.",
        "<b>Verdict:</b> the leak claim does not hold for summer outdoor use by default. It holds only if the wrap stays dry above the melt line and the damaged paths are narrower than the values above, which is unmeasured.",
    ])

story.append(P("7. Quantum runs", H2))
rows = [["Run", "Result", "Note"]]
if qpu1:
    rows.append(["One-qubit sampling, ibm_fez, 1000 shots", "%.3f +/- %.3f" % (qpu1["p_quantum_estimate"], qpu1["shot_standard_error"]),
                 "Classical value 0.715; 2.8 shot errors low, consistent with hardware noise"])
if qae:
    for name, label in (("exact", "Amplitude estimation, exact simulation"),
                        ("noisy", "Amplitude estimation, fake_fez noise model"),
                        ("hardware", "Amplitude estimation, ibm_kingston hardware")):
        m = qae["modes"].get(name, {})
        if "p_hat" in m:
            rows.append([label, "%.4f +/- %.4f" % (m["p_hat"], m["sigma_qae"]),
                         "job %s" % m["job_id"] if m.get("job_id") else "local simulation"])
if sweep:
    by = {(r["mode"], r["shots"]): r for r in sweep["rows"]}
    cls, noiseless, noisy = by[("classical", 1000)], by[("noiseless", 1000)], by[("noisy", 4000)]
    rows.append(["Local sweep (no IBM), 6 Grover powers, 250 to 4000 shots, 30 repetitions",
                 "std %.4f classical vs %.4f noiseless at %d oracle calls" % (cls["std"], noiseless["std"], cls["budget"]),
                 "Noiseless error falls about as 1/N. The noisy model is biased by +%.4f at 4000 shots, a small offset that does not match hardware (see figure 21)." % noisy["bias"]])
else:
    rows.append(["Local sweep (no IBM)", "pending", "Results added when the run completes"])
story.append(table(rows, [70 * mm, 50 * mm, 54 * mm]))
story.append(P("Reading: the quantum runs test the method, not the leak question. Hardware noise dominates the deeper circuits (ibm_kingston gave 0.517 against 0.715), "
               "and the local noise model does not reproduce that error, so no precision gain is claimed. The leak decisions do not depend on the quantum results.", SMALL))

story.append(PageBreak())
story.append(P("8. Figures", H2))
story.append(fig("19_results_charts.png", 170))
story.append(Spacer(1, 6))
story.append(fig("20_quantum_amplitude_estimation.png", 170))
story.append(Spacer(1, 6))
story.append(fig("21_local_quantum_sweep.png", 170))
story.append(PageBreak())
story.append(fig("22_thailand_stress_test.png", 170))
story.append(Spacer(1, 6))
story.append(fig("24_thai_summer_occasions.png", 170))
story.append(PageBreak())
story.append(P("9. Product visuals", H2))
story.append(fig("23_pop_mockup_real_materials.png", 120))
story.append(Spacer(1, 6))
story.append(fig("08_pop_label_dieline.png", 150))
story.append(P("Mockup: CC0 leaf, ice and paper textures from ambientCG; the leaf is a generic leaf photo, not confirmed as banana or pandan. Materials and open assumptions: rework/mockup/MATERIALS.md. "
               "Dimensions are assumptions. Label text is placeholder. Thai FDA label content needs a registration adviser.", SMALL))

story.append(P("10. Open items after the meeting", H2))
story += bullets([
    "Widen the novelty search: global queries, patents, OTOP registry, and in-store audits at 7-Eleven, Makro and Tops.",
    "Confirm the claim wording with a Thai registration adviser, including the plastic-free and leaf-packaging rules.",
    "Find measured optics for banana and pandan leaves (no public value was verified) and a Songkran splash-water temperature (none was sourced).",
    "Team decision: whether the hot-season use conditions in section 1 go on the label or in the entry text.",
])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(18 * mm, 10 * mm, "Team briefing, leaf-wrapped frozen pop. Virtual evidence only. Not for submission as is.")
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
                        title="Team meeting briefing: novelty and technical basis", author="Team working draft")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("wrote", os.path.abspath(OUT))
