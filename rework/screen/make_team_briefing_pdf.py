"""Team-meeting briefing PDF: decisions, novelty, technical basis, Thai conditions, quantum runs and open items.

Reads the result JSON files and figures in rework/ and writes rework/21_team_briefing_novelty.pdf.
Every number in the PDF is read from those files or from the cited notes. Run:  python make_team_briefing_pdf.py
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

story.append(P("Team meeting briefing: decisions, novelty, technical basis and Thai conditions", H1))
story.append(P("Leaf-wrapped frozen coconut-pandan drink pop, Innovative Bev &amp; Bite entry. "
               "Prepared 18 October 2026. Virtual evidence only: no physical or consumer test has been run, and none is in scope.", SMALL))
story.append(Spacer(1, 6))

story.append(P("1. Decisions taken (18 October 2026)", H2))
story += bullets([
    "<b>Working design (confirmed by the user, 18 October):</b> the leaf-wrapped frozen coconut-pandan drink with a food-grade inner barrier, under Alternative Formats. Leaf-only (no barrier) is rejected on physical grounds: freeze damage and stomata would leak (rework/30, rework/31).",
    "<b>Inner barrier:</b> the inner film is plastic, so the product is not plastic-free. It is the working design, not a fallback.",
    "<b>Claim:</b> describe the product as <b>leaf-wrapped</b>. Do not say plastic-free. The outer wrap is leaf; the inner barrier is plastic.",
    "<b>Novelty claim:</b> a leaf-wrapped frozen drink eaten peel-and-sip as it thaws. No such drink was found in the extended search. One leaf-wrapped frozen ice-cream bar is a disclosed precedent (section 3).",
    "<b>Hot-season use conditions:</b> keep the pop in an insulated box with gel packs, keep it out of ice water, and eat it within about an hour when it is in full sun. These go in the product instructions. They do not go on the label until a Thai registration adviser confirms the classification.",
    "<b>Product classification for holding rules:</b> treat the product as a non-heat ready-to-eat beverage. Thai rules then require below 5 °C, or no more than 2 hours at room temperature, when sold from food premises.",
    "<b>After thaw (spoilage):</b> eat within 2 hours of leaving the freezer, and within about 1 hour in full sun. Do not refreeze. Keep the wrap dry and out of standing water. Spoilage needs about 6 to 12 h at 30 C (rework/28), so the Thai 2-hour limit is the operative one. Pathogens: one contaminating cell reaches the hazard in about 6 to 27 h at 30 C, but a serving that starts at the hazard level is unsafe at once. Production control (a validated kill step or pathogen-free raw material) is therefore required (rework/29).",
    "<b>Physical test (approved 18 October):</b> a dye-penetration test on leaf-only wraps (rework/33), with 300 wraps and a pre-registered pass rule. The leaf-only option is approved for testing; the working design stays the barrier until the result is in. The test has not yet been run.",
])

story.append(P("2. The product", H2))
story.append(P("A frozen coconut or pandan drink sealed in a banana or pandan leaf. The consumer peels the leaf open and sips the drink as it thaws. "
               "The newness is the consumption act, not an ingredient. Target: Thai buyers who value traditional packaging "
               "(hypothesis; the evidence is produce wrapping, not drinks). Assumed size: 38 mm core, 41 mm leaf wrap, 150 mm tall, 170 mL.", BODY))

story.append(P("3. Novelty: searched, one precedent found", H2))
story += bullets([
    "<b>Searched:</b> about 137 queries in four searches, covering 11 languages and the web, patents, the OTOP registry, and Thai retail and delivery sites. Matches were re-opened by a separate checker, and each absence claim was tested with new queries.",
    "<b>Found:</b> no leaf-wrapped frozen drink, slush or ice pop. No patent found claims a leaf-based wrap or container for a frozen drink. The only patent near the concept is a pending plant-fibre food wrap, which is not a leaf.",
    "<b>Closest precedent:</b> an old-style ice-cream bar wrapped in banana leaf, sold at Talat O-Ploi market in Suan Phueng, Ratchaburi. It rests on one 2023 user post, and a 2024 review of the same market's bars does not mention the leaf. Its frozen status and whether the leaf is peeled or kept on while eating are inferred, not confirmed.",
    "<b>Other leaf items:</b> a Chanthaburi menu item named \"banana-leaf-wrapped ice cream\" (name only); leaf containers for ice cream in Indonesia and India, which are containers, not wraps. Leaf cones such as clorot and cucurucho are not frozen.",
    "<b>Limits:</b> most Thai retail and delivery sites could not be read, and the OTOP registry has no public keyword search. Only Google Patents pages were readable (WIPO and the Thai DIP portal were not). The retail absence is weak evidence.",
    "<b>Verdict:</b> novel as a leaf-wrapped frozen <i>drink</i> on the evidence found. The Ratchaburi precedent is disclosed above. Full record: rework/25_novelty_search_extended.md.",
])

story.append(P("4. Technical basis (virtual screen, lab reference)", H2))
if sim:
    nom = sim["nominal_h10"]["N8"]
    mc = sim["monte_carlo"]
    story.append(table([
        ["Question", "Result", "Basis"],
        ["Surface starts to melt at 30 C", "%.2f h (about %d min)" % (nom["t_wet_s"] / 3600, round(nom["t_wet_s"] / 60)),
         "Transient radial heat model, h = 10 W/m2K"],
        ["50% thawed (sippable)", "%.2f h" % (nom["t50_s"] / 3600), "Same model; grid difference 0.44% at t100 (8 vs 16 nodes)"],
        ["Fully thawed", "%.2f h" % (nom["t100_s"] / 3600),
         "Lumped estimate was 2.47 h; conduction lags the core"],
        ["Exposed-edge leak within 2 h", "%d%% of 200 runs" % round(100 * mc["design_A_exposed_vessel_leak_probability"]),
         "Vessel-sized paths wick the wrap in 1.5 to 7 min"],
        ["Sealed-edge critical damaged-path radius", "%.2f um median (5 to 95%%: %.2f to %.2f um)" % (
            mc["design_B_critical_damaged_radius_m"]["median"] * 1e6,
            mc["design_B_critical_damaged_radius_m"]["p5"] * 1e6,
            mc["design_B_critical_damaged_radius_m"]["p95"] * 1e6),
         "Monte Carlo, 200 runs over 1 to 3 mPa s; freeze-damage size is unmeasured"],
        ["Intact cuticle", "does not leak", "Pores 0.3 to 2 nm, far below the threshold"],
        ["Continuous inner film", "no liquid path", "Not plastic-free"],
    ], [52 * mm, 58 * mm, 70 * mm]))
    story.append(P("Thaw and wicking model: rework/17. Leak screen: rework/16. Leaf optics for banana now sourced (section 9). Not measured: freeze damage and seam strength.", SMALL))

story.append(P("5. Thai conditions: thaw timing and holding rules", H2))
story.append(P("Bangkok Mar-May normals (TMD 48455, 1991-2020): mean maximum 34.6 C in March and 35.7 C in April, humidity 72 to 74 %, dew point 23.9 to 24.9 C (April 24.8 C), 6.3 to 7.6 h of sun per day. "
               "The model uses a diurnal mean of 31.5 C with 4.3 K amplitude, a half-sine sun peak of 800 W/m2, and a gel-pack melting point of about -1.3 C. "
               "Splash and open-water temperature is set to 29.3 C, the Bangkok canal annual mean, as the nearest sourced proxy. Every input and its confidence is in rework/22_thailand_inputs.md. Virtual screen, not measured.", BODY))
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
story += bullets([
    "<b>Thai holding rules (food premises):</b> non-heat ready-to-eat food, beverages included, must be kept below 5 C, or may stay at room temperature for no more than 2 hours (2566 notification, clause 6(4)). No Thai time-out-of-freezer rule was found.",
    "<b>Frozen storage:</b> the Thai −18 C rule covers fresh food in premises. No Thai rule was found for processed or packaged frozen products, or for transport. The design target is −18 C, following the proposed Codex draft (final text not retrieved).",
    "<b>Notification No. 463 on edible ice:</b> in force from 12 December 2025. It requires ice to meet the drinking-water standard, and it requires the label \"Ice for Consumption\" on packaged ice. It has no drink-specific wording.",
])

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
                   "The outside-water column assumes only the bottom edge is wet, and it uses the measured 76 degree leaf contact angle. "
                   "The drink-side value uses the lower-bound viscosity (1 mPa s), so it is the conservative end of the section 4 range. "
                   "The damaged-path size is unmeasured, so these are thresholds, not leak probabilities.", SMALL))
    story += bullets([
        "<b>Thaw window:</b> does not hold in full sun. Half the drink is sippable in about 0.6 h and the whole pop passes 5 C at about 1.5 h. In shade the two-hour window only just holds: the core passes 5 C at about 2.0 h.",
        "<b>Best hot-season option in the screen:</b> an insulated cooler with gel packs. The surface starts to melt at about 1.6 h, half the pop thaws at about 3.2 h, and the drink-side threshold rises to about 0.7 um.",
        "<b>Drink-side leak margin:</b> roughly holds. The threshold falls only from 0.180 um to 0.162 to 0.171 um, because the melt starts earlier.",
        "<b>Outside water:</b> not established. Dew on banana and plantain leaves lasted 14 plus or minus 2 hours a night on 16 of 18 nights at one humid-tropics site (Costa Rica), and the screen caps retained dew at 90 um per side (a model cap). Songkran splash and ice-water coolers wet the wrap as well. For all of these the top of the wrap is likely wet, so the screen gives no climb margin.",
        "<b>Contact angle, resolved by physics:</b> intact waxy cuticle (about 130 degrees for fresh leaf) gives no capillary climb. Damaged paths with exposed cell wall (76 degrees) do wick. The screen applies 76 degrees to the damaged paths only.",
        "<b>Verdict:</b> the leak claim does not hold for summer outdoor use by default. It holds only if the wrap stays dry above the melt line, the damaged paths are narrower than the values above, and the damaged paths are the only ones that wick, as the screen assumes (intact wax does not).",
    ])

story.append(P("7. Quantum runs", H2))
rows = [["Run", "Result", "Note"]]
if qpu1:
    rows.append(["One-qubit sampling, ibm_fez, 1000 shots", "%.3f +/- %.3f" % (qpu1["p_quantum_estimate"], qpu1["shot_standard_error"]),
                 "Classical value 0.715; 2.8 standard errors low; plausibly hardware noise"])
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
                 "Noiseless error falls roughly as 1/sqrt(N), 3.3-fold over a 16-fold budget. The noisy model is biased by +%.4f at 4000 shots, a small offset that does not match hardware (see figure 21)." % noisy["bias"]])
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
story.append(P("9. Product visuals and leaf optics", H2))
story.append(fig("26_pop_mockup_leaf_optics.png", 120))
story.append(Spacer(1, 6))
story.append(fig("08_pop_label_dieline.png", 150))
story.append(P("Mockup: CC0 leaf, ice and paper textures from ambientCG. The leaf is a generic leaf photo, not confirmed as banana or pandan. The earlier approved still is rework/23; the leaf-optics version is rework/26. "
               "Banana leaf optics are applied since 18 October: colour scaled to the sourced 10.5 % green reflectance (Gausman and Allen 1973, derived), translucency weight 0.12 from the sourced 12 % transmittance. The mapping is derived and not validated. "
               "Dimensions are assumptions. Label text is placeholder. Thai FDA label content needs a registration adviser.", SMALL))

story.append(P("10. Open items: status", H2))
story.append(table([
    ["Item", "Status", "Decision or limit"],
    ["Novelty: global, patents, OTOP, retail", "Closed (limited)", "Searched. One precedent disclosed. Retail, OTOP and WIPO limits stated in section 3."],
    ["Banana leaf optics", "Closed (resolved)", "Measured and derived values sourced; not applied to the locked render."],
    ["Pandan leaf optics and cuticle roughness", "Closed (physics assumption)", "Banana values used for pandan (plus or minus 20 %); roughness 0.3. The screens do not depend on them."],
    ["Splash and open-water temperature", "Closed (proxy)", "Bangkok canal annual mean, 29.3 C, used. No Songkran or tap value found."],
    ["Thai frozen storage rule for packaged products", "Closed (physics assumption)", "Target −18 C: most water is ice, so the thaw starts slow. Codex draft is the reference."],
    ["Thai time out of freezer", "Closed (physics assumption)", "The thaw screen governs the temperature history; the Thai 2-hour rule is the legal limit for sale."],
    ["Condensate on packaged frozen food", "Closed (physics assumption)", "Mass transfer gives about 15 g/m2/min uncapped; the 90 um cap is reached in about 6 to 22 min. The screen uses the dew-point film rule."],
    ["Leaf contact angle (76 vs 130 degrees)", "Closed (physics)", "Intact wax does not wick; damaged paths at 76 degrees do. The outside-water rows apply to damaged paths."],
    ["Product classification (beverage or ice cream)", "Working assumption", "Treated as a non-heat ready-to-eat beverage, pending a Thai registration adviser. If classed as ice cream, the −2.2 C storage rule applies instead."],
    ["Physical leak test: leaf-only wrap (rework/33)", "Confirmed by user, not yet run", "Dye-penetration on 300 wraps, controls included. Pass if zero leaks. The lab run is a separate physical step and needs its own go-ahead. A simulated run is in rework/34."],
    ["Stomatal state in the leaf-only test (rework/34)", "Adopted 18 Oct (rework/33, step 7a)", "The simulation shows the outcome depends on open or closed stomata, not only on breach fraction. The scoring rule is adopted for any run. The lab run is not scheduled in the desk plan."],
    ["Second track: isoflavone soy drink (rework/40)", "Closed as limit; not advanced", "Desk track complete. The food-or-supplement route, the dose, the safety and the cost stay unverified. No outside contact is in the plan. The leaf wrap (A) remains primary."],
    ["PET pouch compliance (rework/32)", "Confirmed by user", "Thai No. 435 limits verified. Overall migration margin about 76x; antimony needs antimony-free PET; fat content and a migration test (needs approval) are open."],
    ["Unknown parameters (drink, damage, stomata, process)", "Closed (physics)", "Resolved in rework/30: water activity 0.995, pH 6.3, lag from h0 = 2. Leaf-only seal not supported; inner barrier is the working design."],
    ["Percolation of damage (rework/31)", "Closed (physics)", "Connected airspace network adopted. Leaf-only seal survives only below about 1e-8 damaged cells; 50 percent leak near 3 to 5 x 1e-7."],
    ["Taste of inner barrier (rework/31)", "Closed (physics)", "PE and PP scalp aroma completely; PET takes up about 0.2 percent in 2 h. PET selected; EVOH the alternative."],
    ["Consumer effect of inner barrier (rework/31)", "Closed (decision)", "Positioned on leaf format and peel-and-sip; the plastic-free buyer hypothesis is withdrawn for the barrier version. Consumer test out of scope."],
    ["Spoilage after thaw (rotten condition)", "Closed (physics screen)", "Growth screen: sealed drink spoils in about 6 to 12 h at 30 C; contaminated, in about 3.5 to 7 h. The 2-hour rule governs. Rules in rework/28."],
    ["Pathogens and microbial load", "Closed (physics screen)", "From one cell per serving, hazard in about 6 to 27 h at 30 C. The start load decides the risk, so a kill step or pathogen-free raw material is required. Rules in rework/29."],
], [58 * mm, 40 * mm, 76 * mm]))

story.append(Spacer(1, 6))
story += bullets([
    "Widen the global search later, if the team wants a full patent claim review (CN106414847A is the one pending candidate to read).",
    "Confirm the claim wording and classification with a Thai registration adviser, including the rules on packaging and claim wording.",
])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(18 * mm, 10 * mm, "Team briefing, leaf-wrapped frozen pop. Virtual evidence only. Not for submission as is.")
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
                        title="Team meeting briefing: decisions, novelty and technical basis", author="Team working draft")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("wrote", os.path.abspath(OUT))
