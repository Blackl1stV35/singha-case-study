"""Build the Lime Cube brochure (HTML) from the results files, then print it to PDF with headless Chrome.

Judge-facing: no team name, university, author, email, local path or repo reference in the output.
Every number is read from the results files in rework/screen/ or from the renders in rework/mockup/.
Run:  python -I build_brochure.py
"""
import html
import json
import os
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SCREEN = REPO / "screen"
MOCK = REPO / "mockup"
IMG = HERE / "images"
OUT_HTML = HERE / "lime_cube_brochure.html"
OUT_PDF = HERE / "lime_cube_brochure.pdf"
CHROME = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


VAL = load(SCREEN / "project_valuation_results.json")
HAND = load(SCREEN / "handover_figures_results.json")
RECIPE = HAND["per_330ml_recipe"]
COST = HAND["cost_and_containers"]
PACK6 = COST["packs"]["6"]
PACK12 = COST["packs"]["12"]
UE = VAL["unit_economics"]
BASE = VAL["summary"]["base_case"]


def npv(scenario, fixed, rate="0.1"):
    for r in VAL["scenario_results"]:
        if r["scenario"] == scenario and r["fixed_cost_thb_per_year"] == fixed:
            return r["npv_thb"][rate], r["payback_years_base_rate"]
    raise KeyError((scenario, fixed))


def th(v):
    """Thai baht, whole number, with a thousands separator and a sign."""
    return ("-" if v < 0 else "") + "THB {:,}".format(abs(round(v)))


def mn(v):
    return ("-" if v < 0 else "") + "THB {:.2f} million".format(abs(v) / 1e6)


# ---- figures (all read, none typed) -------------------------------------
cost6 = PACK6["cost_per_cube_thb"]
cost12 = PACK12["cost_per_cube_thb"]
ex = UE["ex_factory_thb_per_cube"]
contrib6 = UE["base_contribution_thb"]
margin6 = UE["base_contribution_margin"]
contrib12 = VAL["unit_economics"]["contribution_per_cube_by_pack_thb"]["12"]
carton6_share = round(4.0 / 6, 2)   # THB 4.00 per 6-cube carton (ASSUMPTION) / 6
carton12_share = round(5.0 / 12, 2)  # THB 5 per 12-cube carton (PROXY) / 12
reactants = COST["reactants_thb_per_cube"]
pouch = COST["pouch_thb"]
print_ = COST["print_thb"]
proc = COST["processing_thb"]
npv250, _ = npv("base", 250000)
npv500, payback500 = npv("base", 500000)
npv1000, _ = npv("base", 1000000)
npv_low500, _ = npv("low", 500000)
npv_high500, _ = npv("high", 500000)
maxfixed = BASE["max_fixed_cost_thb_per_year_at_10pct"]
c_by = VAL["unit_economics"]["contribution_per_cube_by_pack_thb"]
c_12 = c_by["12"]
pouch_high = [r for r in VAL["sensitivities"] if r["change"].startswith("Pouch 2.70")][0]

cont20 = PACK6["containers"]["20ft"]
cont20_12 = PACK12["containers"]["20ft"]
cont40 = PACK6["containers"]["40ft"]

# ---- copy the images into the brochure folder ---------------------------
IMG.mkdir(exist_ok=True)
from PIL import Image  # noqa: E402  (Pillow is in the environment; only used to shrink the render)

hero = Image.open(MOCK / "cube_front_2k.png").convert("RGB")
hero.thumbnail((1600, 1600))
hero.save(IMG / "hero.jpg", quality=88)
for name in ("label_front", "label_back"):
    im = Image.open(MOCK / (name + ".png")).convert("RGB")
    im.thumbnail((700, 900))
    im.save(IMG / (name + ".jpg"), quality=90)

E = html.escape

CSS = """
@page { size: A4; margin: 14mm 14mm 14mm 14mm; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", Arial, Helvetica, sans-serif; color: #17191C; font-size: 10pt; line-height: 1.42; margin: 0; }
.page { page-break-after: always; min-height: 265mm; position: relative; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 30pt; margin: 0 0 2mm 0; letter-spacing: 0.02em; }
h2 { font-size: 15pt; margin: 0 0 3mm 0; color: #17191C; border-bottom: 2px solid #A8CF3A; padding-bottom: 1mm; }
h3 { font-size: 11pt; margin: 4mm 0 1.5mm 0; }
p { margin: 0 0 2.5mm 0; }
.lead { font-size: 13pt; color: #3A3F36; margin-bottom: 4mm; }
.tag { display: inline-block; background: #A8CF3A; color: #17191C; font-weight: 700; font-size: 8.5pt; padding: 0.6mm 2mm; border-radius: 1mm; margin-right: 1.5mm; }
.note { font-size: 8.5pt; color: #3A3F36; background: #F1F0EB; border-left: 3px solid #A8CF3A; padding: 2mm 3mm; margin: 3mm 0; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 4mm 0; font-size: 9pt; }
th, td { border-bottom: 1px solid #D9D9D2; padding: 1.4mm 2mm; vertical-align: top; text-align: left; }
th { background: #17191C; color: #F1F0EB; font-weight: 600; }
td.num, th.num { text-align: right; white-space: nowrap; }
tr.total td { font-weight: 700; border-top: 1.5px solid #17191C; }
.status { font-size: 7.5pt; color: #3A3F36; }
.cols { display: table; width: 100%; table-layout: fixed; }
.col { display: table-cell; vertical-align: top; padding-right: 6mm; }
.col:last-child { padding-right: 0; }
.kpi { display: table; width: 100%; table-layout: fixed; margin: 3mm 0; }
.kpi div { display: table-cell; border: 1px solid #D9D9D2; padding: 2.5mm; text-align: center; }
.kpi b { display: block; font-size: 15pt; color: #17191C; }
.kpi span { font-size: 8pt; color: #3A3F36; }
.hero { width: 100%; height: auto; border-radius: 2mm; }
.labels img { width: 46%; height: auto; margin-right: 3%; border-radius: 1.5mm; }
ul { margin: 1mm 0 3mm 4.5mm; padding: 0; }
li { margin-bottom: 1.2mm; }
.foot { position: absolute; bottom: 0; left: 0; right: 0; font-size: 7.5pt; color: #3A3F36; border-top: 1px solid #D9D9D2; padding-top: 1.5mm; }
"""


def foot(text):
    return '<div class="foot">' + E(text) + "</div>"


pages = []

# ---- page 1: cover ----------------------------------------------------------
pages.append(f"""
<section class="page">
  <img class="hero" src="images/hero.jpg" alt="Lime Cube pouch, carton and cube">
  <h1>Lime Cube</h1>
  <p class="lead">A dissolvable drink cube. One cube, dissolved in one 330 mL serve, makes a carbonated lime drink.</p>
  <div class="kpi">
    <div><b>0.55 volume</b><span>CO₂ per 330 mL serve</span></div>
    <div><b>{cost6:.2f} THB</b><span>cost per cube, 6-cube carton</span></div>
    <div><b>{contrib6:.2f} THB</b><span>contribution per cube (desk)</span></div>
    <div><b>{PACK6["containers"]["20ft"]["cubes"]:,}</b><span>cubes per 20 ft container</span></div>
  </div>
  <div class="note"><b>Desk-stage proposal.</b> Every figure is derived on stated assumptions or taken from a source with its tier. Nothing has been measured, weighed, tasted or tested with consumers. Net weight is <i>[to be set]</i> until a cube is weighed.</div>
  {foot("Lime Cube · proposal brochure · 19 October 2026 · figures as stated in the sections that follow")}
</section>""")

# ---- page 2: what it is, how it is used, what it does not claim -------------
pages.append(f"""
<section class="page">
  <h2>What it is and how it is used</h2>
  <div class="cols">
    <div class="col" style="width:55%">
      <p>Lime Cube is a single-serve, dissolvable drink cube for domestic Thailand. The cube is pressed from potassium bicarbonate, citric acid, an intensive sweetener and a lime flavour. When it dissolves in water, the acid and the bicarbonate release carbon dioxide. The drink is carbonated, and the form is new: the consumer makes the drink in the glass.</p>
      <h3>Use</h3>
      <ul>
        <li>Open the pouch and drop one cube into 330 mL of water.</li>
        <li>Stir until dissolved. Drink.</li>
      </ul>
      <p class="status">The label copy is set in the artwork. One cube per pouch is inferred, not yet confirmed.</p>
      <h3>Position</h3>
      <p>The company already sells a lime sparkling water: Singha Sparkling Water, Lime Flavour, in a 330 mL can at 15 baht (company release, 13 March 2026, P; news reprint, S). The two overlap on flavour. They differ in form and pack: Lime Cube dissolves in the glass, from a pouch; the company product is ready to drink from a can.</p>
    </div>
    <div class="col" style="width:45%">
      <div class="labels"><img src="images/label_front.jpg" alt="Front label"><img src="images/label_back.jpg" alt="Back label"></div>
      <p class="status">Front and back artwork. Thai particulars, manufacturer, sweetener name, binder name and net weight are placeholders.</p>
    </div>
  </div>
  <h2 style="margin-top:6mm">What it does not claim</h2>
  <div class="note">
    <p>The proposal makes no sugar-free, sodium-free, low-potassium, health, hydration, electrolyte, calorie or fizz-performance claim. Those wordings are held back until a Thai text check, a shelf test, a sensory test and a medical review are done. The competitor describes its can as sugar-free with 0% calories; that is its own claim and is not checked here.</p>
  </div>
  {foot("Sources: company release (P, 13 March 2026) and news reprint (S, 17 March 2026).")}
</section>""")

# ---- page 3: technical details ------------------------------------------------
pages.append(f"""
<section class="page">
  <h2>Technical details: one serve, 330 mL</h2>
  <table>
    <tr><th>Component</th><th class="num">Amount per serve</th><th>Basis and status</th></tr>
    <tr><td>Carbon dioxide</td><td class="num">0.55 volume, {RECIPE["co2_mmol"]} mmol</td><td>0.55 times 0.330 L at standard molar volume. Recommended dose (decision, 19 October 2026). DERIVED.</td></tr>
    <tr><td>Potassium bicarbonate</td><td class="num">{RECIPE["potassium_bicarbonate_g"]:.3f} g</td><td>One mole per mole of CO₂. DERIVED.</td></tr>
    <tr><td>Citric acid, neutralising part</td><td class="num">{RECIPE["citric_acid_stoichiometric_g"]:.3f} g</td><td>One third mole per mole of CO₂. DERIVED.</td></tr>
    <tr><td>Citric acid, total for pH 3.5</td><td class="num">{RECIPE["citric_acid_total_for_pH_target_g"]:.2f} g</td><td>Working anchor pH 3.5, untested by taste. Acid constants: secondary source, UNVERIFIED in the handover. DERIVED.</td></tr>
    <tr><td>Sucralose</td><td class="num">{RECIPE["sucralose_mg"]:.0f} mg</td><td>{RECIPE["sucralose_mg_per_kg"]:.0f} mg/kg. Permitted at 300 mg/kg in category 14.1.4, condition 127, for the drink as consumed (primary, flavoured-drink rows). Classification open. DERIVED.</td></tr>
    <tr><td>Binder and filler</td><td class="num">{RECIPE["binder_filler_g"]:.2f} g (0.5 to 1.2)</td><td>ASSUMPTION. Not yet named. Sodium content not checked, so no sodium claim is made.</td></tr>
    <tr><td>Natural lime flavour powder</td><td class="num">{RECIPE["flavour_g"]:.2f} g (0.02 to 0.10)</td><td>ASSUMPTION.</td></tr>
    <tr><td>Potassium</td><td class="num">{RECIPE["potassium_mg"]:.0f} mg</td><td>about {RECIPE["potassium_pct_of_thai_rdi"]:.0f}% of a Thai reference of 3,500 mg (secondary copies; primary not opened). DERIVED. The label amount line stays <i>[to be set]</i> pending the decision on the potassium line.</td></tr>
    <tr class="total"><td>Reactants (before binder and flavour)</td><td class="num">{RECIPE["reactants_g"]:.3f} g</td><td>DERIVED.</td></tr>
  </table>

  <h3>The cube</h3>
  <table>
    <tr><th>Item</th><th class="num">Value</th><th>Basis and status</th></tr>
    <tr><td>Side</td><td class="num">14 mm</td><td>Design side, chosen so the density sits inside the assumed band. DERIVED on ASSUMPTION inputs.</td></tr>
    <tr><td>Mass, central (range)</td><td class="num">{RECIPE["cube_mass_g"]:.2f} g (3.46 to 4.24)</td><td>Reactants plus binder and flavour. Not weighed. DERIVED on ASSUMPTIONS.</td></tr>
    <tr><td>Density at 14 mm</td><td class="num">1.38 g/cm³</td><td>Inside the assumed band of 1.25 to 1.60 g/cm³. ASSUMPTION band.</td></tr>
    <tr><td>Packed unit</td><td class="num">{COST["pouch_mass_g"]:.2f} g</td><td>Cube plus a 1.5 g pouch. ASSUMPTION for the pouch.</td></tr>
    <tr><td>Net weight on the label</td><td class="num">[to be set]</td><td>Not printed until a cube is weighed.</td></tr>
  </table>

  <h3>Carbon dioxide in the serve (desk model)</h3>
  <p>Solubility of CO₂ at 35 °C is 0.592 volume, the lowest across the 5 to 35 °C serve range, so 0.55 volume is within solubility at every modelled serve (secondary, Lange-attributed, SOURCED). At 25 °C the model keeps about 0.50 volume after 10 minutes. Above a mineral-water threshold of about 0.22 volume (a proxy for a soft drink, abstract only) the upper bound is about 96 minutes. The model assumes no bubble formation. Ice lowers the start level: 30 g of ice gives about 21 °C at 0.50 volume. These are model results, not measurements; the retention gate is for R&D to define.</p>
  {foot("Stoichiometry, potassium and cube arithmetic from the 0.55-volume design.")}
</section>""")

# ---- page 4: pack, container, economics, desk valuation ---------------------
val_rows = []
for label, fixed in (("THB 250,000 a year", 250000), ("THB 500,000 a year", 500000), ("THB 1,000,000 a year", 1000000)):
    v = {"250000": npv250, "500000": npv500, "1000000": npv1000}[str(fixed)]
    val_rows.append(f"<tr><td>{label}</td><td class=\"num\">{mn(v)}</td></tr>")
pages.append(f"""
<section class="page">
  <h2>Pack, container and unit economics</h2>
  <div class="cols">
    <div class="col" style="width:50%">
      <h3>Pouch</h3>
      <p>Single-serve flat pouch, 70 × 90 mm front, 20 mm deep. Printed laminate of food-contact PET with an antimony-free catalyst, and a foil barrier layer in the render. The sealant and barrier specification are not yet sourced. ASSUMPTION for size.</p>
      <h3>Carton</h3>
      <p>Six pouches (six cubes) in a printed folding paperboard carton, 190 × 150 × 50 mm outside. The board is not a food-contact surface, since the pouch is the food contact. The size is an ASSUMPTION; the board grade, print and price need a carton maker's quote, which has not been requested. The larger 12-cube carton is the alternative.</p>
      <h3>Container</h3>
      <p>A 20 ft container holds about {cont20["cubes"]:,} cubes in {cont20["cartons"]:,} six-cube cartons. Volume, not weight, is the limit. The modelled load is {cont20["container_mass_kg"]/1000:.2f} tonnes against a 28.2 tonne payload. The 12-cube carton gives {cont20_12["cubes"]:,} cubes in {cont20_12["cartons"]:,} cartons, a load of {cont20_12["container_mass_kg"]/1000:.2f} tonnes.</p>
    </div>
    <div class="col" style="width:50%">
      <h3>Cost and contribution per cube (6-cube carton)</h3>
      <table>
        <tr><th>Line</th><th class="num">THB</th></tr>
        <tr><td>Reactants</td><td class="num">{reactants:.2f}</td></tr>
        <tr><td>Pouch (ASSUMPTION; non-Thai listing as proxy)</td><td class="num">{pouch:.2f}</td></tr>
        <tr><td>Print (ASSUMPTION)</td><td class="num">{print_:.2f}</td></tr>
        <tr><td>Processing (ASSUMPTION)</td><td class="num">{proc:.2f}</td></tr>
        <tr><td>Carton share, THB 4.00 per 6 (ASSUMPTION)</td><td class="num">{carton6_share:.2f}</td></tr>
        <tr class="total"><td>Cost per cube</td><td class="num">{cost6:.2f}</td></tr>
        <tr><td>Ex-factory planning value (ASSUMPTION: 60% of a THB 15 shelf price)</td><td class="num">{ex:.2f}</td></tr>
        <tr class="total"><td>Contribution per cube ({margin6*100:.1f}% margin)</td><td class="num">{contrib6:.2f}</td></tr>
      </table>
      <p class="status">Binder and flavour are not priced, so these figures exclude them. The 12-cube carton gives THB {cost12:.2f} per cube and contribution THB {contrib12:.2f}; the 12-cube carton share rests on a retail listing (PROXY).</p>
    </div>
  </div>
  <h3>Desk valuation (product level, pre-tax, domestic)</h3>
  <p>Base case: 200,000 cubes a year at steady state, a launch year at half volume, five years, no terminal value, 10% discount rate. Volumes and fixed costs are assumptions, not forecasts.</p>
  <table>
    <tr><th>Annual fixed cost</th><th class="num">NPV at 10%, base volume</th></tr>
    {''.join(val_rows)}
  </table>
  <p>At THB 500,000 a year the undiscounted payback is about {payback500:.1f} years. The break-even fixed cost at base volume is about THB {maxfixed:,} a year. At 50,000 cubes a year the NPV is {mn(npv_low500)} at THB 500,000 fixed cost; at 1,000,000 cubes a year it is {mn(npv_high500)}. Figures are DERIVED on ASSUMPTION volumes and costs.</p>
  {foot("Product-level desk valuation, rebased to the 0.55-volume design and the 6-cube pack on 19 October 2026.")}
</section>""")

# ---- page 5: status, open questions, what R&D must define ----------------------
pages.append(f"""
<section class="page">
  <h2>Decided, not yet known, and what comes next</h2>
  <div class="cols">
    <div class="col" style="width:50%">
      <h3>Decided for this proposal</h3>
      <ul>
        <li>Dose: 0.55 volume of CO₂ per 330 mL (recommended; gate for R&D to define).</li>
        <li>Working pH anchor 3.5 (taste untested).</li>
        <li>Composition: potassium bicarbonate, citric acid, sucralose, a binder and filler, natural lime flavour. No sodium carbonate.</li>
        <li>Pack: six-cube carton for portable use, with the twelve-cube carton as the larger option.</li>
        <li>Carton material: printed folding paperboard. Board grade and price open.</li>
        <li>No health, sugar-free, sodium-free or fizz-performance claim.</li>
      </ul>
      <h3>Not yet known</h3>
      <ul>
        <li>Taste, sweetness acceptance and consumer demand: no sensory or consumer test has been run.</li>
        <li>Binder: not yet named, and its sodium content is not checked. Binder and flavour amounts are assumptions until weighed.</li>
        <li>Pouch barrier and shelf life: no water-vapour rate, shelf test or Thai quote.</li>
        <li>Sweetener classification, which sets the limits. Excise rules apply; the value base was not read.</li>
        <li>Medical review of the potassium declaration.</li>
      </ul>
    </div>
    <div class="col" style="width:50%">
      <h3>What R&amp;D is asked to define</h3>
      <ol style="margin:1mm 0 3mm 4.5mm; padding:0">
        <li style="margin-bottom:1.2mm">The retention gate for 0.55 volume: CO₂ left at 25 °C after how many minutes.</li>
        <li style="margin-bottom:1.2mm">The pH and acid level, with 3.5 as the working anchor.</li>
        <li style="margin-bottom:1.2mm">Sweetness accepted at 33 mg sucralose per serve.</li>
        <li style="margin-bottom:1.2mm">Chilled, iced or ambient, and the serve rule and pack wording.</li>
        <li style="margin-bottom:1.2mm">An acceptable fizz duration and how it is measured.</li>
        <li style="margin-bottom:1.2mm">The potassium declaration and medical wording, and who reviews the risk.</li>
        <li style="margin-bottom:1.2mm">The classification, which sets the limits.</li>
        <li style="margin-bottom:1.2mm">Pouch barrier, shelf life, and Thai prices for the pouch, print and carton.</li>
      </ol>
      <h3>Stated limits</h3>
      <p class="status">The registry trademark search is partial. Brand-owner and legal sign-off on the lion emblem sit with the brand owner's department. The Thai patent register is unsearched. Novelty and freedom to operate are not assessed. Overseas cube products are analogues only (proxy).</p>
    </div>
  </div>
  {foot("Tier key: P = primary (regulator text read in full, a company release, or official statistics). S = secondary (press, trade portals, consultancy pages, search snippets). SOURCED = page read. DERIVED = arithmetic on stated inputs. ASSUMPTION = chosen for the model, not sourced. PROXY = a stand-in for what is not measured.")}
</section>""")

doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lime Cube brochure</title>
<style>{CSS}</style>
</head>
<body>
{''.join(pages)}
</body>
</html>
"""
OUT_HTML.write_text(doc, encoding="utf-8")
print("wrote", OUT_HTML)

# ---- print to PDF with headless Chrome ---------------------------------------
if OUT_PDF.exists():
    OUT_PDF.unlink()
cmd = [
    str(CHROME), "--headless", "--disable-gpu", "--no-pdf-header-footer",
    "--print-to-pdf=" + str(OUT_PDF), OUT_HTML.as_uri(),
]
subprocess.run(cmd, check=True, timeout=180)
print("wrote", OUT_PDF, OUT_PDF.stat().st_size, "bytes")
