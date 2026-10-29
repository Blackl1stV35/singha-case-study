"""T15 (revision 3): ambient variation of the potency of existing Singha customer bases.

Revision 3 (after the second verification): two sweeps added to the structural set (bottled-base habit counted once;
population range widened to the repo's own alternatives), a temperature break-even run, an age-gradient-only ratio
(the figure that rests on a source) separate from the trial-propensity ratio that carries the assumed temperature
sensitivity, a stated confidence rule, a split between the lead that is validated and the lead that is proposed,
and run counts computed here instead of typed in the record.

Synthesis under stated assumptions: no respondents, no purchase data, no outside contact.

Potency of base b, per draw (THB million, model scale):

    Reach_b = Pop_b x g_b x chan_b x T_b x R x C x (1 - X_b)

  Pop_b   population of the age-sex cell (DOPA Nov 2568; women derived as both sexes minus men)
  g_b     penetration: current drinking (NSO 2024) for drinker bases, everyday sweet bottled drinks
          (NSO 2021 Table 20) for bottled buyers, the Mintel share for the pool
  chan_b  channel factor (1 - r) + r x internet use (NSO ICT 2569 Q2, carried)
  T_b     trial propensity (top-2-box intent proxy, ASSUMPTION link): B x rho_b^e x season x price,
          rho_b = sweet-drink habit of base b over the comparison cell (men 35 to 44); the habit carries an
          age gradient (OR per year, NSO 2021) and a sex gradient (men 23.3 vs women 14.7 percent, NSO 2021
          Table 2, 5 or more days a week)
  R, C    repeat propensity and contribution per cube (common to every base)
  X_b     exclusion: potassium-caution coverage (rework/73 band cells, team model) combined, for drinker
          bases, with an alcohol-cue exclusion (ASSUMPTION, no source)

Three lenses, all from the same draws, each with its denominator stated:
  reach        total potency of the base
  per_cell     reach divided by the population of the age-sex cell (the conversion lens of rework/46 and 47;
               like-for-like among drinker cells only, so it is ranked over the drinker bases)
  per_member   reach divided by the members of the base (population x penetration); comparable across base types

Four model forms (power or linear intent link, on the share or the odds scale), 23 input groups for
leave-one-factor-out, 12 TMD monthly means, a season stress run, a set of structural-assumption sweeps, and a
full-model permutation placebo that shuffles the sourced inputs across base labels.

Writes rework/screen/ambient_variation_results.json and rework/charts/ambient_potency.png.
Run: python ambient_variation.py      (about 35 seconds; peak working set about 180 MB, measured with psutil)
"""
import json
import math
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_JSON = os.path.join(HERE, "ambient_variation_results.json")
OUT_PNG = os.path.join(REPO, "rework", "charts", "ambient_potency.png")
POTASSIUM_JSON = os.path.join(HERE, "t10_potassium_cover_results.json")

SEED = 20261020
N = 40000                       # total draws (at least 20,000); halves of 20,000 for the split check
HALF = N // 2
N_PERM = 200                    # permutations in the placebo
TOP_P_THRESHOLD = 0.90          # decision bar, fixed before the run
PLACEBO_CHANCE_MULT = 1.5       # c6: mean permuted first-place probability at most 1.5 x chance
TORNADO_MIN_SWING = 0.02        # a quintile flip counts only if the swing is at least this (about 2.5 standard errors)

BASES = ["M25", "M35", "M45", "W25", "W35", "W45", "SB25", "SB45", "POOL"]
DRINKERS = ["M25", "M35", "M45", "W25", "W35", "W45"]
EXISTING = [b for b in BASES if b != "POOL"]
SHORT = {
    "M25": "Men 25-34 drinkers",
    "M35": "Men 35-44 drinkers",
    "M45": "Men 45-59 drinkers",
    "W25": "Women 25-34 drinkers",
    "W35": "Women 35-44 drinkers",
    "W45": "Women 45-59 drinkers",
    "SB25": "Sweet-bottled drinkers 25-44",
    "SB45": "Sweet-bottled drinkers 45-59",
    "POOL": "Sugar-reduction pool (market)",
}

# Lens configurations: name -> (matrix key, candidate bases, one-line definition with the denominator)
LENSES = {
    "reach": ("reach", EXISTING,
              "Total potency of the base (population x penetration x channel x trial x repeat x contribution x (1 - exclusion)); ranked over the eight existing bases."),
    "per_cell_drinkers": ("per_cell", DRINKERS,
                          "Potency per person in the age-sex cell (denominator: the cell population); the conversion lens of rework/46 and 47; ranked over the six drinker cells, which are like-for-like."),
    "per_cell_all": ("per_cell", EXISTING,
                     "Same denominator (cell population) ranked over all eight existing bases; shown to expose the denominator problem, because penetration is inside the quantity and differs by base type."),
    "per_member": ("per_member", EXISTING,
                   "Potency per member of the base (denominator: population x penetration); comparable across base types."),
}
LENS_ORDER = list(LENSES)

# Population, DOPA November 2568. Both sexes: rework/screen/segment_potency_mc.py; men: rework/47 section 6.
POP_BOTH = {"25": 9.384203, "35": 9.407482, "45": 14.904550}
POP_MEN = {"25": 4.76, "35": 4.75, "45": 6.65}
POP_WOMEN = {k: POP_BOTH[k] - POP_MEN[k] for k in POP_BOTH}
PI = {k: POP_MEN[k] / POP_BOTH[k] for k in POP_BOTH}     # men's share of the band
DOPA_GAP = 0.0096               # carried range, plus or minus 0.96 percent (rework/screen/segment_potency_mc.py; UNVERIFIED)
# Wider population ranges from the repo's own alternatives, used in the sweep "population_range_wide" only:
#  - bands 25 to 34 and 35 to 44: DDC mid-year men counts differ from DOPA by -1.1 and -2.1 percent (rework/47 section 6,
#    submission/12 line 35: "agree within about 2%"); range plus or minus 2.2 percent
#  - band 45 to 59: DDC mid-year men 7.13 million against DOPA 6.65 million is +7.2 percent (submission/12 line 35), and the
#    rework/73 section 5.2 correction for age 60 counted twice (13,910,913 against 14,904,550) is -6.7 percent
POP_WIDE_YOUNG = 0.022
POP45_LOW = 13910913 / 14904550 - 1.0
POP45_HIGH = 7.13 / 6.65 - 1.0

# NSO 2024 drinking (Social Indicators 2025, Table 4.6.2; third value of each printed row) and NSO 2021 everyday
# sweet bottled drinks (Table 20, printed p. 41). Drinking 2021 cells (second value) are used in a sweep.
PUB = {"d_m2544": 68.6, "d_m4559": 65.4, "d_w2544": 25.2, "d_w4559": 19.9, "s2544": 18.2, "s4559": 16.0}
PUB_2021_DRINK = {"d_m2544": 58.1, "d_m4559": 54.6, "d_w2544": 15.2, "d_w4559": 12.2}
HALF_D = 3.0                    # ASSUMPTION: no 2024 interval published (rework/55)
HALF_S = 2.0                    # ASSUMPTION: sampling and series difference

# Sex gradient of the sweet-drink habit: NSO 2021 Table 2 (printed p. 12), sweet bottled drinks 5 or more days a week,
# ages 6 and over: men 23.3, women 14.7, all 18.9 percent. Men's factor = 23.3 / 18.9. Range is an ASSUMPTION.
SEX_MEN, SEX_WOMEN, SEX_ALL = 23.3, 14.7, 18.9
SEX_CENT = SEX_MEN / SEX_ALL
SEX_RANGE = (1.10, 1.35)

# NSO 2021 age odds ratio per year for daily consumption (rework/47 section 2, carried).
OR_MID, OR_LO, OR_HI = 0.996, 0.991, 1.001
MID = {"25": 29.5, "35": 39.5, "ref": 34.5}   # band mid-ages; 34.5 is the mid of the 25 to 44 cell (ASSUMPTION)

# Potassium-caution coverage, narrow group, fraction of the group: low, mode, high. Read at run time from
# rework/screen/t10_potassium_cover_results.json (rework/73 team model; band cells coverage.by_band).
XA = (0.0, 0.05, 0.20)                    # alcohol-cue exclusion, drinker bases: ASSUMPTION, no source

G_POOL = (0.20, 0.27, 0.35)               # Mintel 27 percent (S), range ASSUMPTION (sample not stated)
K_POOL = (0.5, 2.0)                       # pool habit mapping, log-uniform, ASSUMPTION

B_RANGE, B_CENT = (0.20, 0.50), 0.35      # top-2-box baseline of the comparison cell, ASSUMPTION (rework/49)
E_RANGE, E_CENT = (0.5, 1.0), 0.75        # intent-to-potency elasticity, ASSUMPTION (rework/49)
R_TRI = (0.15, 0.30, 0.40)                # repeat propensity, ASSUMPTION (rework/55)
C_RANGE, C_CENT = (3.6, 6.8), 4.91        # contribution per cube: range rework/55; centre = deck desk value (6-cube carton)

# TMD Bangkok (station 48455) monthly mean temperature, 1991 to 2020 (raw saved in rework/raw/diligence_2026-10-20/T15).
TMD = [27.4, 28.6, 29.7, 30.7, 30.3, 29.7, 29.2, 29.0, 28.6, 28.4, 28.4, 27.3]
TMD_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
TMD_ANNUAL = 28.9
BETA_RANGE, BETA_CENT = (0.0, 0.05), 0.025  # season sensitivity per degree C, drawn independently per base: ASSUMPTION
BETA_STRESS = 0.15                          # stress run only
DIRECTIONAL_DELTAS = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]   # older male cells more heat-sensitive than men 25 to 34, per degree C
BETA_BREAKEVEN = [0.30, 0.45, 0.60, 1.00]   # reverse stress: how large must the per-base sensitivity be to change a leader

R_CH_RANGE, R_CH_CENT = (0.1, 0.5), 0.3     # online channel share, ASSUMPTION (rework/screen/segment_potency_mc.py)
ICT = {"25_34": (99.0, 99.2, 99.05), "35_44": (98.2, 98.7, 98.45), "45_59": (96.1, 98.2, 97.15)}

PRICES = (13.80, 15.00)                     # listing parity (rework/70, from 68d) and planned price (deck, submission 11)
PRICE_PLAN = 15.00
EPS_RANGE, EPS_CENT = (-1.5, -0.5), -1.0    # price elasticity of trial, ASSUMPTION

FORMS = ["mult_share", "mult_odds", "add_share", "add_odds"]
PRIMARY = "mult_share"

XP_KEYS = ["m25", "m35", "m45", "a25", "a35", "a45", "pool"]
XP = {}                                      # filled by load_coverage()
COVERAGE_SOURCE = {}


def load_coverage():
    """Read the rework/73 band cells (percent, low / mode / high) from its results file."""
    with open(POTASSIUM_JSON, encoding="utf-8") as fh:
        r = json.load(fh)
    bb = r["coverage"]["by_band"]
    ag = r["coverage"]["aggregates"]
    cells = {
        "m25": bb["men_25-34"]["narrow_ckd35_or_acei_arb_pct_low_mid_high"],
        "m35": bb["men_35-44"]["narrow_ckd35_or_acei_arb_pct_low_mid_high"],
        "m45": bb["men_45-59"]["narrow_ckd35_or_acei_arb_pct_low_mid_high"],
        "a25": bb["all_25-34"]["narrow_ckd35_or_acei_arb_pct_low_mid_high"],
        "a35": bb["all_35-44"]["narrow_ckd35_or_acei_arb_pct_low_mid_high"],
        "a45": bb["all_45-59"]["narrow_ckd35_or_acei_arb_pct_low_mid_high"],
        "pool": ag["adults_25_59"]["narrow_pct_low_mid_high"],
    }
    for k, v in cells.items():
        XP[k] = tuple(x / 100.0 for x in v)
        COVERAGE_SOURCE[k] = {"low_mode_high_percent": v}
    COVERAGE_SOURCE["_file"] = "rework/screen/t10_potassium_cover_results.json (coverage.by_band, coverage.aggregates)"


GROUPS = [
    # (label, keys fixed at their sample mean in the leave-one-out run, representative key for the quintile split)
    ("Population (DOPA gap, by age band)", ["gap25", "gap35", "gap45"], "gap25"),
    ("Drinking share, men 25 to 44 (2024)", ["d_m2544"], "d_m2544"),
    ("Drinking share, men 45 to 59 (2024)", ["d_m4559"], "d_m4559"),
    ("Drinking share, women (2024)", ["d_w2544", "d_w4559"], "d_w2544"),
    ("Sweet-bottled share, 25 to 44 (2021)", ["s2544"], "s2544"),
    ("Sweet-bottled share, 45 to 59 (2021)", ["s4559"], "s4559"),
    ("Age odds ratio per year (2021)", ["OR"], "OR"),
    ("Men's sweet-drink factor (sex gradient)", ["sexm"], "sexm"),
    ("Potassium coverage, men 25 to 34", ["xp_m25"], "xp_m25"),
    ("Potassium coverage, men 35 to 44", ["xp_m35"], "xp_m35"),
    ("Potassium coverage, men 45 to 59", ["xp_m45"], "xp_m45"),
    ("Potassium coverage, women and bottled buyers (both-sex bands)", ["xp_a25", "xp_a35", "xp_a45"], "xp_a25"),
    ("Potassium coverage, pool (adults 25 to 59)", ["xp_pool"], "xp_pool"),
    ("Alcohol-cue exclusion (drinker bases)", ["xa"], "xa"),
    ("Sugar-reduction pool share (Mintel 27 percent)", ["g_pool"], "g_pool"),
    ("Pool habit mapping k", ["k_pool"], "k_pool"),
    ("Top-2-box baseline B", ["B"], "B"),
    ("Intent elasticity e", ["e"], "e"),
    ("Repeat rate R", ["R"], "R"),
    ("Contribution per cube C", ["C"], "C"),
    ("Ambient temperature (TMD month and seasonal sensitivity)", ["Tm"] + ["beta_" + b for b in BASES], "Tm"),
    ("Channel online share and internet use", ["r", "ict_25_34", "ict_35_44", "ict_45_59"], "r"),
    ("Price level and price elasticity", ["p", "eps"], "eps"),
]


def draw(n, rng, beta_max=BETA_RANGE[1]):
    d = {}
    for k in ("25", "35", "45"):
        d["gap" + k] = rng.uniform(-DOPA_GAP, DOPA_GAP, n)
    for key in ("d_m2544", "d_m4559", "d_w2544", "d_w4559"):
        d[key] = rng.uniform(PUB[key] - HALF_D, PUB[key] + HALF_D, n)
    d["s2544"] = rng.uniform(PUB["s2544"] - HALF_S, PUB["s2544"] + HALF_S, n)
    d["s4559"] = rng.uniform(PUB["s4559"] - HALF_S, PUB["s4559"] + HALF_S, n)
    sd_log = (math.log(OR_HI) - math.log(OR_LO)) / (2 * 1.96)
    d["OR"] = np.exp(rng.normal(math.log(OR_MID), sd_log, n))
    d["sexm"] = rng.uniform(*SEX_RANGE, n)
    for k in XP_KEYS:
        d["xp_" + k] = rng.triangular(*XP[k], n)
    d["xa"] = rng.triangular(*XA, n)
    d["g_pool"] = rng.triangular(*G_POOL, n)
    d["k_pool"] = np.exp(rng.uniform(math.log(K_POOL[0]), math.log(K_POOL[1]), n))
    d["B"] = rng.uniform(*B_RANGE, n)
    d["e"] = rng.uniform(*E_RANGE, n)
    d["R"] = rng.triangular(*R_TRI, n)
    d["C"] = rng.uniform(*C_RANGE, n)
    d["Tm"] = rng.choice(np.array(TMD), n)
    for b in BASES:
        d["beta_" + b] = rng.uniform(BETA_RANGE[0], beta_max, n)
    d["r"] = rng.uniform(*R_CH_RANGE, n)
    for k, (lo, hi, _) in ICT.items():
        d["ict_" + k] = rng.uniform(lo, hi, n)
    d["p"] = rng.choice(np.array(PRICES), n)
    d["eps"] = rng.uniform(*EPS_RANGE, n)
    return d


def central(n):
    """Base case: every factor at its mode (most likely value)."""
    full = lambda v: np.full(n, float(v))
    d = {"gap25": full(0), "gap35": full(0), "gap45": full(0)}
    for key in ("d_m2544", "d_m4559", "d_w2544", "d_w4559", "s2544", "s4559"):
        d[key] = full(PUB[key])
    d["OR"] = full(OR_MID)
    d["sexm"] = full(SEX_CENT)
    for k in XP_KEYS:
        d["xp_" + k] = full(XP[k][1])
    d["xa"] = full(XA[1])
    d["g_pool"] = full(G_POOL[1])
    d["k_pool"] = full(1.0)
    d["B"] = full(B_CENT)
    d["e"] = full(E_CENT)
    d["R"] = full(R_TRI[1])
    d["C"] = full(C_CENT)
    d["Tm"] = full(TMD_ANNUAL)
    for b in BASES:
        d["beta_" + b] = full(BETA_CENT)
    d["r"] = full(R_CH_CENT)
    for k, (_, _, c) in ICT.items():
        d["ict_" + k] = full(c)
    d["p"] = full(PRICE_PLAN)
    d["eps"] = full(EPS_CENT)
    return d


def fixed_values(d_full, keys):
    """Sample means of the full run (expected values); price is held at the planned price."""
    return {k: (PRICE_PLAN if k == "p" else float(np.mean(d_full[k]))) for k in keys}


def tri_inv(u, a, c, b):
    fc = (c - a) / (b - a)
    return np.where(u < fc, a + np.sqrt(u * (b - a) * (c - a)), b - np.sqrt((1 - u) * (b - a) * (b - c)))


# ----------------------------------------------------------------------------------------------------------------
# Model
# ----------------------------------------------------------------------------------------------------------------
def base_inputs(d):
    """Per-base source inputs (arrays over draws). These are the sourced inputs that the placebo permutes."""
    m = d["sexm"]
    w = {k: (1 - PI[k] * m) / (1 - PI[k]) for k in PI}      # women's factor keeps the band's both-sex share
    OR = d["OR"]
    s25 = d["s2544"] * OR ** (MID["25"] - MID["ref"])
    s35 = d["s2544"] * OR ** (MID["35"] - MID["ref"])
    s45 = d["s4559"]
    s = {"M25": s25 * m, "M35": s35 * m, "M45": s45 * m,
         "W25": s25 * w["25"], "W35": s35 * w["35"], "W45": s45 * w["45"],
         "SB25": d["s2544"], "SB45": d["s4559"], "POOL": s35 * d["k_pool"]}
    ref = s["M35"]
    rho = {b: s[b] / ref for b in BASES}
    if "bottled_rho_one" in d:
        # sweep: the sweet-drink habit of the bottled bases enters once (as penetration), not also as the habit ratio
        rho["SB25"] = np.ones_like(rho["SB25"])
        rho["SB45"] = np.ones_like(rho["SB45"])

    g1, g2, g3 = 1 + d["gap25"], 1 + d["gap35"], 1 + d["gap45"]
    pop = {
        "M25": POP_MEN["25"] * g1, "M35": POP_MEN["35"] * g2, "M45": POP_MEN["45"] * g3,
        "W25": POP_WOMEN["25"] * g1, "W35": POP_WOMEN["35"] * g2, "W45": POP_WOMEN["45"] * g3,
        "SB25": POP_BOTH["25"] * g1 + POP_BOTH["35"] * g2,
        "SB45": POP_BOTH["45"] * g3,
        "POOL": POP_BOTH["25"] * g1 + POP_BOTH["35"] * g2 + POP_BOTH["45"] * g3,
    }
    pen = {
        "M25": d["d_m2544"] / 100, "M35": d["d_m2544"] / 100, "M45": d["d_m4559"] / 100,
        "W25": d["d_w2544"] / 100, "W35": d["d_w2544"] / 100, "W45": d["d_w4559"] / 100,
        "SB25": d["s2544"] / 100, "SB45": d["s4559"] / 100, "POOL": d["g_pool"],
    }
    wa, wb = POP_BOTH["25"], POP_BOTH["35"]
    x2544 = (wa * d["xp_a25"] + wb * d["xp_a35"]) / (wa + wb)
    xpot = {"M25": d["xp_m25"], "M35": d["xp_m35"], "M45": d["xp_m45"],
            "W25": d["xp_a25"], "W35": d["xp_a35"], "W45": d["xp_a45"],
            "SB25": x2544, "SB45": d["xp_a45"], "POOL": d["xp_pool"]}
    i25, i35, i45 = d["ict_25_34"], d["ict_35_44"], d["ict_45_59"]
    wc = POP_BOTH["45"]
    ict = {"M25": i25, "M35": i35, "M45": i45, "W25": i25, "W35": i35, "W45": i45,
           "SB25": (i25 + i35) / 2, "SB45": i45,
           "POOL": (wa * i25 + wb * i35 + wc * i45) / (wa + wb + wc)}
    return {"pop": pop, "pen": pen, "rho": rho, "xpot": xpot, "ict": ict}


MAT_KEYS = ("reach", "per_cell", "per_member", "T", "X", "chan", "pen", "pop")


def assemble(d, inp, form, perm=None):
    n = d["B"].shape[0]
    shape = (n, len(BASES))
    mats = {k: np.zeros(shape) for k in MAT_KEYS}
    B, e, R, C, r = d["B"], d["e"], d["R"], d["C"], d["r"]
    pf = (d["p"] / PRICE_PLAN) ** d["eps"]
    base_odds = B / (1 - B)
    for j, b in enumerate(BASES):
        def src(key):
            sb = perm[key].get(b, b) if (perm and key in perm) else b
            return inp[key][sb]
        popb, penb, rhob, xpb, ictb = src("pop"), src("pen"), src("rho"), src("xpot"), src("ict")
        X = (1 - (1 - xpb) * (1 - d["xa"])) if b in DRINKERS else xpb
        chan = (1 - r) + r * ictb / 100
        mult = np.exp(d["beta_" + b] * (d["Tm"] - TMD_ANNUAL)) * pf
        if form == "mult_share":
            Tb = np.clip(B * rhob ** e * mult, 0.0, 1.0)
        elif form == "mult_odds":
            o = base_odds * rhob ** e * mult
            Tb = o / (1 + o)
        elif form == "add_share":
            Tb = np.clip(B * (1 + e * (rhob - 1)) * mult, 0.0, 1.0)
        elif form == "add_odds":
            o = base_odds * (1 + e * (rhob - 1)) * mult
            Tb = o / (1 + o)
        else:
            raise ValueError(form)
        member = chan * Tb * R * C * (1 - X)          # potency per member of the base
        per_cell = penb * member                       # potency per person in the age-sex cell
        mats["reach"][:, j] = popb * per_cell
        mats["per_cell"][:, j] = per_cell
        mats["per_member"][:, j] = member
        mats["T"][:, j] = Tb
        mats["X"][:, j] = X
        mats["chan"][:, j] = chan
        mats["pen"][:, j] = penb
        mats["pop"][:, j] = popb
    return mats


def potency(d, form, perm=None):
    return assemble(d, base_inputs(d), form, perm)


def run(form=PRIMARY, fixed=None, month=None, beta_max=BETA_RANGE[1], variant=None):
    rng = np.random.default_rng(SEED)
    d = draw(N, rng, beta_max=beta_max)
    if fixed:
        for k, v in fixed.items():
            d[k] = np.full(N, float(v))
    if month is not None:
        d["Tm"] = np.full(N, float(month))
    if variant:
        apply_variant(d, variant)
    return d, potency(d, form)


VARIANTS = {
    "m35_interp_0_1": "Men 35-44 coverage = weight x (men 25-34 cell) + (1 - weight) x (men 45-59 cell), weight uniform 0 to 1 (the earlier interpolation, widened)",
    "m35_equals_m25": "Men 35-44 coverage set equal to the men 25-34 draw (no coverage gradient between the two age bands)",
    "common_coverage": "All coverage cells move together on one latent position (fully correlated scenario draws)",
    "sex_gradient_off": "Sweet-drink habit the same for men and women (the earlier model)",
    "alcohol_cue_zero": "Alcohol-cue exclusion set to 0",
    "alcohol_cue_20": "Alcohol-cue exclusion set to 20 percent (top of its range)",
    "drinking_2021_cells": "Drinking shares from the 2021 column of NSO Table 4.6.2 (year-matched to the sweet-drink data)",
    "bottled_habit_counted_once": "Bottled bases: the sweet-drink habit ratio is set to 1, so the habit enters once (as penetration) and not also as the trial-propensity ratio",
    "population_pm7_all_bands": "Population range plus or minus 7 percent for every band (a stress beyond the repo's own alternatives)",
    "population_range_wide": "Population ranges widened to the repo's own alternatives: plus or minus 2.2 percent for ages 25 to 34 and 35 to 44; minus 6.7 to plus 7.2 percent for ages 45 to 59 (age-60 correction of rework/73 and the DDC mid-year gap)",
}
WEIGHT_SWEEP = [0.0, 0.25, 0.5, 0.75]


def apply_variant(d, variant):
    n = d["B"].shape[0]
    if variant == "m35_interp_0_1":
        u = np.random.default_rng(SEED + 101).uniform(0, 1, n)
        d["xp_m35"] = u * d["xp_m25"] + (1 - u) * d["xp_m45"]
    elif variant.startswith("m35_weight_"):
        wgt = float(variant.split("_")[-1])
        d["xp_m35"] = wgt * d["xp_m25"] + (1 - wgt) * d["xp_m45"]
    elif variant == "m35_equals_m25":
        d["xp_m35"] = d["xp_m25"].copy()
    elif variant == "common_coverage":
        u = np.random.default_rng(SEED + 102).uniform(0, 1, n)
        for k in XP_KEYS:
            d["xp_" + k] = tri_inv(u, *XP[k])
    elif variant == "sex_gradient_off":
        d["sexm"] = np.ones(n)
    elif variant == "alcohol_cue_zero":
        d["xa"] = np.zeros(n)
    elif variant == "alcohol_cue_20":
        d["xa"] = np.full(n, 0.20)
    elif variant == "drinking_2021_cells":
        for key, v in PUB_2021_DRINK.items():
            d[key] = d[key] + (v - PUB[key])
    elif variant == "bottled_habit_counted_once":
        d["bottled_rho_one"] = np.ones(n)
    elif variant == "population_pm7_all_bands":
        r = np.random.default_rng(SEED + 104)
        for k in ("gap25", "gap35", "gap45"):
            d[k] = r.uniform(-0.07, 0.07, n)
    elif variant == "population_range_wide":
        r = np.random.default_rng(SEED + 103)
        d["gap25"] = r.uniform(-POP_WIDE_YOUNG, POP_WIDE_YOUNG, n)
        d["gap35"] = r.uniform(-POP_WIDE_YOUNG, POP_WIDE_YOUNG, n)
        d["gap45"] = r.uniform(POP45_LOW, POP45_HIGH, n)
    else:
        raise ValueError(variant)


# ----------------------------------------------------------------------------------------------------------------
# Summaries
# ----------------------------------------------------------------------------------------------------------------
def kendall_pairs(sub, p0):
    m = sub.shape[1]
    pairs = [(i, j) for i in range(m) for j in range(i + 1, m)]
    acc = np.zeros(sub.shape[0])
    for i, j in pairs:
        acc += np.sign(sub[:, i] - sub[:, j]) * np.sign(p0[i] - p0[j])
    return acc / len(pairs)


def summarise(A, names, A0, light=False):
    order = np.argsort(-A, axis=1)
    top, second = order[:, 0], order[:, 1]
    p1 = {names[j]: float(np.mean(top == j)) for j in range(len(names))}
    modal = max(p1, key=p1.get)
    out = {"prob_rank_first": {k: round(v, 4) for k, v in p1.items()}, "modal_top": modal}
    if light:
        return out
    p2 = {names[j]: float(np.mean((top == j) | (second == j))) for j in range(len(names))}
    tau = kendall_pairs(A, A0)
    out.update({
        "median": {names[j]: float(np.median(A[:, j])) for j in range(len(names))},
        "p05": {names[j]: float(np.percentile(A[:, j], 5)) for j in range(len(names))},
        "p95": {names[j]: float(np.percentile(A[:, j], 95)) for j in range(len(names))},
        "prob_top_two": {k: round(v, 4) for k, v in p2.items()},
        "base_case_order": [names[k] for k in np.argsort(-A0)],
        "kendall_tau_vs_base_mean": round(float(tau.mean()), 4),
        "kendall_tau_vs_base_median": round(float(np.median(tau)), 4),
        "share_draws_identical_ranking_to_base": round(float(np.mean(tau == 1.0)), 4),
    })
    return out


def kendall_between(order_a, order_b):
    pos_b = {k: i for i, k in enumerate(order_b)}
    pairs = [(i, j) for i in range(len(order_a)) for j in range(i + 1, len(order_a))]
    agree = sum(1 if pos_b[order_a[i]] < pos_b[order_a[j]] else -1 for i, j in pairs)
    return agree / len(pairs)


def lens_cols(lens):
    key, names, _ = LENSES[lens]
    return key, names, [BASES.index(b) for b in names]


def sum_all(out, A0_mats, light=True):
    res = {}
    for lens in LENS_ORDER:
        key, names, idx = lens_cols(lens)
        res[lens] = summarise(out[key][:, idx], names, A0_mats[key][0][idx], light=light)
    return res


def quintile_split(d, A, names, rep_key, star):
    x = d[rep_key]
    q20, q80 = np.quantile(x, 0.2), np.quantile(x, 0.8)
    low, high = x <= q20, x >= q80
    top = np.argmax(A, axis=1)
    star_j = names.index(star)

    def modal(mask):
        counts = np.bincount(top[mask], minlength=len(names))
        return names[int(np.argmax(counts))], float(np.mean(top[mask] == star_j))

    m_low, p_low = modal(low)
    m_high, p_high = modal(high)
    swing = p_high - p_low
    return {
        "low_quintile_cut": round(float(q20), 4), "high_quintile_cut": round(float(q80), 4),
        "modal_top_low": m_low, "modal_top_high": m_high,
        "prob_star_first_low": round(p_low, 4), "prob_star_first_high": round(p_high, 4),
        "swing_high_minus_low": round(swing, 4),
        "modal_top_differs": m_low != m_high,
        "flips_ranking": bool(m_low != m_high and abs(swing) >= TORNADO_MIN_SWING),
    }


def permutation_placebo(d, form, full_summaries, n_perm=N_PERM):
    """Full-model placebo: shuffle the sourced inputs (population, penetration, sweet-drink habit, potassium
    coverage) across the eight existing base labels, independently for each input, keep every shared factor and the
    label-specific structure (alcohol cue, season sensitivity, channel), recompute all lenses."""
    rng = np.random.default_rng(SEED + 11)
    inp = base_inputs(d)
    stars = {lens: full_summaries[lens]["modal_top"] for lens in LENS_ORDER}
    real_order = {lens: sorted(LENSES[lens][1], key=lambda b: -full_summaries[lens]["median"][b]) for lens in LENS_ORDER}
    rec = {lens: {"p_star": [], "max_p": [], "tau": []} for lens in LENS_ORDER}
    for _ in range(n_perm):
        perm = {key: {b: EXISTING[i] for b, i in zip(EXISTING, rng.permutation(len(EXISTING)))}
                for key in ("pop", "pen", "rho", "xpot")}
        mats = assemble(d, inp, form, perm)
        for lens in LENS_ORDER:
            key, names, idx = lens_cols(lens)
            A = mats[key][:, idx]
            top = np.argmax(A, axis=1)
            p = np.bincount(top, minlength=len(names)) / A.shape[0]
            rec[lens]["p_star"].append(float(p[names.index(stars[lens])]))
            rec[lens]["max_p"].append(float(p.max()))
            med = np.median(A, axis=0)
            order = [names[k] for k in np.argsort(-med)]
            rec[lens]["tau"].append(kendall_between(order, real_order[lens]))
    out = {}
    for lens in LENS_ORDER:
        names = LENSES[lens][1]
        ps, mx, tau = (np.array(rec[lens][k]) for k in ("p_star", "max_p", "tau"))
        obs = full_summaries[lens]["prob_rank_first"][stars[lens]]
        out[lens] = {
            "label_tested": stars[lens],
            "n_permutations": n_perm,
            "observed_prob_first": round(obs, 4),
            "chance_level": round(1.0 / len(names), 4),
            "perm_mean_prob_label_first": round(float(ps.mean()), 4),
            "perm_p95_prob_label_first": round(float(np.percentile(ps, 95)), 4),
            "perm_share_label_first_prob_ge_observed": round(float(np.mean(ps >= obs)), 4),
            "perm_median_of_max_prob_any_label": round(float(np.median(mx)), 4),
            "perm_share_some_label_prob_ge_0_90": round(float(np.mean(mx >= TOP_P_THRESHOLD)), 4),
            "perm_mean_kendall_tau_vs_real_median_order": round(float(tau.mean()), 4),
            "threshold_mean_prob": round(PLACEBO_CHANCE_MULT / len(names), 4),
        }
    return out


def identical_inputs_check(d, form, n_runs=1):
    """Specificity check (cannot fail by symmetry among the drinker cells): every label receives the same sourced
    inputs (those of men 35-44); only label-specific structure remains."""
    inp = base_inputs(d)
    perm = {key: {b: "M35" for b in EXISTING} for key in ("pop", "pen", "rho", "xpot")}
    mats = assemble(d, inp, form, perm)
    res = {}
    for lens in LENS_ORDER:
        key, names, idx = lens_cols(lens)
        top = np.argmax(mats[key][:, idx], axis=1)
        p = np.bincount(top, minlength=len(names)) / top.shape[0]
        res[lens] = {names[j]: round(float(p[j]), 4) for j in range(len(names))}
    return res


def ratio_stats(a, b):
    x = a / b
    p05, p95 = float(np.percentile(x, 5)), float(np.percentile(x, 95))
    return {"median": round(float(np.median(x)), 4), "p05": round(p05, 4), "p95": round(p95, 4),
            "prob_gt_1": round(float(np.mean(x > 1)), 4), "interval_touches_1": bool(p05 <= 1 <= p95)}


# ----------------------------------------------------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------------------------------------------------
def collect():
    d_full, out_full = run(PRIMARY)
    A0 = {f: potency(central(1), f) for f in FORMS}

    full_sum = {}
    for lens in LENS_ORDER:
        key, names, idx = lens_cols(lens)
        full_sum[lens] = summarise(out_full[key][:, idx], names, A0[PRIMARY][key][0][idx], light=False)

    store = {"forms": {}, "loo": [], "months": [], "stress": None, "variants": {}, "weights": {}}
    store["forms"][PRIMARY] = sum_all(out_full, A0[PRIMARY])
    for f in FORMS:
        if f == PRIMARY:
            continue
        _, oo = run(f)
        store["forms"][f] = sum_all(oo, A0[f])
        del oo

    for label, keys, rep in GROUPS:
        fixed = fixed_values(d_full, keys)
        _, oo = run(PRIMARY, fixed=fixed)
        store["loo"].append({"label": label, "keys": keys, "fixed": {k: round(v, 4) for k, v in fixed.items()},
                             "res": sum_all(oo, A0[PRIMARY])})
        del oo

    for name, val in zip(TMD_NAMES, TMD):
        _, oo = run(PRIMARY, month=val)
        store["months"].append({"month": name, "tm": val, "res": sum_all(oo, A0[PRIMARY])})
        del oo

    _, oo = run(PRIMARY, beta_max=BETA_STRESS)
    store["stress"] = {"res": sum_all(oo, A0[PRIMARY]),
                       "full": {lens: summarise(oo[lens_cols(lens)[0]][:, lens_cols(lens)[2]], lens_cols(lens)[1],
                                                A0[PRIMARY][lens_cols(lens)[0]][0][lens_cols(lens)[2]], light=False)
                                for lens in LENS_ORDER}}
    del oo

    for v in VARIANTS:
        _, oo = run(PRIMARY, variant=v)
        store["variants"][v] = sum_all(oo, A0[PRIMARY])
        del oo
    for wgt in WEIGHT_SWEEP:
        _, oo = run(PRIMARY, variant="m35_weight_%g" % wgt)
        store["weights"]["%g" % wgt] = sum_all(oo, A0[PRIMARY])
        del oo

    # reverse stress on temperature: how large must the differential per-base sensitivity be to change a leader
    store["breakeven"] = {}
    for bm in BETA_BREAKEVEN:
        _, oo = run(PRIMARY, beta_max=bm)
        store["breakeven"]["%g" % bm] = sum_all(oo, A0[PRIMARY])
        del oo

    # directional temperature scenarios: the per-base sensitivities in the main run are independent draws, so no base is
    # systematically more heat-sensitive than another. Here the older male cells (35 to 44 and 45 to 59) are given a
    # higher fixed sensitivity than men 25 to 34 by delta per degree C, in April (30.7 C, the hottest month) and over
    # the twelve-month mixture. The sensitivity is an ASSUMPTION; no source gives its direction.
    store["directional"] = {}
    for delta in DIRECTIONAL_DELTAS:
        fx = {"beta_M25": 0.0, "beta_M35": delta, "beta_M45": delta}
        _, oa = run(PRIMARY, fixed=fx, month=TMD[3])
        _, ob = run(PRIMARY, fixed=fx)
        store["directional"]["%g" % delta] = {"april": sum_all(oa, A0[PRIMARY]), "all_months": sum_all(ob, A0[PRIMARY])}
        del oa, ob
    # the same two strongest directional scenarios, month by month (chart panel C)
    store["directional_months"] = {}
    for delta in (0.03, 0.05):
        fx = {"beta_M25": 0.0, "beta_M35": delta, "beta_M45": delta}
        rows = []
        for name, val in zip(TMD_NAMES, TMD):
            _, oo = run(PRIMARY, fixed=fx, month=val)
            rows.append({"month": name, "tm": val, "res": sum_all(oo, A0[PRIMARY])})
            del oo
        store["directional_months"]["%g" % delta] = rows

    return d_full, out_full, A0, full_sum, store


def build_lens_validation(lens, d_full, out_full, A0, full_sum, store, placebo):
    key, names, idx = lens_cols(lens)
    A_full = out_full[key][:, idx]
    s_full = full_sum[lens]
    star = s_full["modal_top"]
    star_j = names.index(star)
    A0p = A0[PRIMARY][key][0][idx]

    def p_star(res):
        return res[lens]["prob_rank_first"][star]

    def same(res):
        return res[lens]["modal_top"] == star

    # split check
    h1 = summarise(A_full[:HALF], names, A0p)
    h2 = summarise(A_full[HALF:], names, A0p)
    med1 = sorted(names, key=lambda b: -h1["median"][b])
    med2 = sorted(names, key=lambda b: -h2["median"][b])
    split = {
        "half_1_modal_top": h1["modal_top"], "half_2_modal_top": h2["modal_top"],
        "half_1_prob_first": h1["prob_rank_first"], "half_2_prob_first": h2["prob_rank_first"],
        "half_1_prob_first_of_full_leader": h1["prob_rank_first"][star],
        "half_2_prob_first_of_full_leader": h2["prob_rank_first"][star],
        "half_1_median_order": med1, "half_2_median_order": med2,
        "kendall_between_half_median_orders": round(kendall_between(med1, med2), 4),
    }

    forms = {f: {"modal_top": store["forms"][f][lens]["modal_top"],
                 "prob_first_of_full_leader": p_star(store["forms"][f]),
                 "prob_rank_first": store["forms"][f][lens]["prob_rank_first"]} for f in FORMS}

    loo = []
    for row in store["loo"]:
        res = row["res"]
        loo.append({
            "factor_group_fixed_at_mean": row["label"], "keys": row["keys"], "fixed_values": row["fixed"],
            "modal_top": res[lens]["modal_top"],
            "prob_first_of_full_leader": p_star(res),
            "change_in_prob_vs_full": round(p_star(res) - s_full["prob_rank_first"][star], 4),
            "changes_leader": not same(res),
            "below_bar": p_star(res) < TOP_P_THRESHOLD,
        })

    tornado = []
    for label, keys, rep in GROUPS:
        tornado.append({"factor_group": label, "representative_key": rep, "keys_in_group": keys,
                        **quintile_split(d_full, A_full, names, rep, star)})
    tornado_sorted = sorted(tornado, key=lambda r: -abs(r["swing_high_minus_low"]))

    months = [{"month": m["month"], "tm_celsius": m["tm"], "modal_top": m["res"][lens]["modal_top"],
               "prob_first_of_full_leader": p_star(m["res"]), "prob_rank_first": m["res"][lens]["prob_rank_first"]}
              for m in store["months"]]
    stress = store["stress"]["full"][lens]
    stress_out = {"modal_top": stress["modal_top"], "prob_first_of_full_leader": stress["prob_rank_first"][star],
                  "prob_rank_first": stress["prob_rank_first"],
                  "kendall_tau_vs_base_mean": stress["kendall_tau_vs_base_mean"]}

    variants = {v: {"description": VARIANTS[v], "modal_top": store["variants"][v][lens]["modal_top"],
                    "prob_first_of_full_leader": p_star(store["variants"][v]),
                    "prob_rank_first": store["variants"][v][lens]["prob_rank_first"]} for v in VARIANTS}
    weights = {w: {"modal_top": r[lens]["modal_top"], "prob_first_of_full_leader": p_star(r)}
               for w, r in store["weights"].items()}

    breakeven = {bm: {"modal_top": r[lens]["modal_top"], "prob_first_of_full_leader": p_star(r),
                      "prob_rank_first": r[lens]["prob_rank_first"]} for bm, r in store["breakeven"].items()}

    directional = {dl: {"april_modal_top": r["april"][lens]["modal_top"],
                        "april_prob_first_of_full_leader": p_star(r["april"]),
                        "april_prob_rank_first": r["april"][lens]["prob_rank_first"],
                        "all_months_modal_top": r["all_months"][lens]["modal_top"],
                        "all_months_prob_first_of_full_leader": p_star(r["all_months"]),
                        "all_months_prob_rank_first": r["all_months"][lens]["prob_rank_first"]}
                   for dl, r in store["directional"].items()}

    directional_months = {dl: [{"month": m["month"], "tm_celsius": m["tm"], "modal_top": m["res"][lens]["modal_top"],
                                "prob_first_of_full_leader": p_star(m["res"])} for m in rows]
                          for dl, rows in store["directional_months"].items()}

    plc = placebo[lens]

    # every re-run: the 3 other model forms (the primary form is the full run), 23 leave-one-out, 12 months, the season
    # stress run, the structural sweeps, and the 4 coverage-weight sweep runs; plus the 2 halves (disjoint draws)
    rerun_sets = ([store["forms"][f] for f in FORMS if f != PRIMARY] + [r["res"] for r in store["loo"]] +
                  [m["res"] for m in store["months"]] + [store["stress"]["res"]] +
                  [store["variants"][v] for v in VARIANTS] + list(store["weights"].values()))
    all_runs = rerun_sets + [store["forms"][PRIMARY]]
    leader_same_everywhere = all(same(r) for r in all_runs) and h1["modal_top"] == star and h2["modal_top"] == star
    p_all = [p_star(r) for r in all_runs] + [h1["prob_rank_first"][star], h2["prob_rank_first"][star]]
    min_p = min(p_all)
    run_counts = {
        "other_model_forms": len(FORMS) - 1, "leave_one_factor_out": len(store["loo"]), "months": len(store["months"]),
        "season_stress": 1, "structural_sweeps": len(VARIANTS), "coverage_weight_sweep_runs": len(store["weights"]),
        "halves": 2,
    }
    run_counts["total_reruns_and_splits"] = sum(run_counts.values())
    run_counts["note"] = ("The primary model form is the full run itself and is not counted. The temperature break-even runs "
                          "(%d) are reverse-stress runs outside the assumed range and are not counted." % len(store["breakeven"]))

    crit = {
        "c1_prob_first_at_least_0_90_full_run": s_full["prob_rank_first"][star] >= TOP_P_THRESHOLD,
        "c2_halves_same_leader_and_each_at_least_0_90": (
            h1["modal_top"] == star and h2["modal_top"] == star
            and h1["prob_rank_first"][star] >= TOP_P_THRESHOLD and h2["prob_rank_first"][star] >= TOP_P_THRESHOLD),
        "c3_four_forms_same_leader_and_each_at_least_0_90": all(
            same(store["forms"][f]) and p_star(store["forms"][f]) >= TOP_P_THRESHOLD for f in FORMS),
        "c4_leave_one_out_same_leader_and_each_at_least_0_90": all(
            (not r["changes_leader"]) and (not r["below_bar"]) for r in loo),
        "c5_months_and_stress_same_leader_and_each_at_least_0_90": (
            all(same(m["res"]) and p_star(m["res"]) >= TOP_P_THRESHOLD for m in store["months"])
            and same(store["stress"]["res"]) and p_star(store["stress"]["res"]) >= TOP_P_THRESHOLD),
        "c6_permutation_placebo_mean_prob_at_most_1_5_times_chance": (
            plc["perm_mean_prob_label_first"] <= plc["threshold_mean_prob"]),
        "c7_structural_sweeps_same_leader_and_each_at_least_0_90": all(
            same(store["variants"][v]) and p_star(store["variants"][v]) >= TOP_P_THRESHOLD for v in VARIANTS),
    }
    failing = [k for k, v in crit.items() if not v]
    # Confidence rule. It was written after the first verification, not before the run: the seven criteria above were
    # fixed before the run; this grading of a partial pass was added afterwards and is stated as such in the record.
    #   high      all seven criteria hold
    #   moderate  the leader is the same in every re-run and split and c1 holds (the 0.90 bar is missed in some runs)
    #   none      the leader changes in any re-run, or c1 fails (the lens is not robust)
    if not failing:
        status = "validated: all seven criteria hold"
        confidence = "high"
    elif leader_same_everywhere and crit["c1_prob_first_at_least_0_90_full_run"]:
        status = "leader unchanged in every run; probability bar of 0.90 not met in: " + ", ".join(failing)
        confidence = "moderate"
    else:
        status = "not robust (leader changes or the full run is below the bar); failing: " + ", ".join(failing)
        confidence = "none"
    below_bar_runs = []
    for row in loo:
        if row["below_bar"]:
            below_bar_runs.append("leave-one-out: " + row["factor_group_fixed_at_mean"])
    for m in months:
        if m["prob_first_of_full_leader"] < TOP_P_THRESHOLD:
            below_bar_runs.append("month: " + m["month"])
    if stress_out["prob_first_of_full_leader"] < TOP_P_THRESHOLD:
        below_bar_runs.append("season stress run")
    for v, row in variants.items():
        if row["prob_first_of_full_leader"] < TOP_P_THRESHOLD:
            below_bar_runs.append("sweep: " + v)
    for f, row in forms.items():
        if row["prob_first_of_full_leader"] < TOP_P_THRESHOLD:
            below_bar_runs.append("model form: " + f)
    for hn, hp in (("half 1", h1["prob_rank_first"][star]), ("half 2", h2["prob_rank_first"][star])):
        if hp < TOP_P_THRESHOLD:
            below_bar_runs.append(hn)
    for w, row in weights.items():
        if row["prob_first_of_full_leader"] < TOP_P_THRESHOLD:
            below_bar_runs.append("coverage weight sweep: weight " + w)

    return {
        "lens": lens,
        "definition": LENSES[lens][2],
        "candidate_bases": names,
        "base_case": {k: round(float(A0p[j]), 4) for j, k in enumerate(names)},
        "full_run": s_full,
        "modal_top": star,
        "prob_modal_top_first": round(s_full["prob_rank_first"][star], 4),
        "model_forms": forms,
        "split_check": split,
        "leave_one_factor_out": loo,
        "quintile_tornado_sorted_by_swing": tornado_sorted,
        "tornado_flip_rule": "modal top differs between the lowest and highest fifth of the input AND |swing| >= %.2f" % TORNADO_MIN_SWING,
        "inputs_that_flip_ranking": [r["factor_group"] for r in tornado_sorted if r["flips_ranking"]],
        "ambient_by_month": months,
        "beta_stress_0_15": stress_out,
        "structural_sweeps": variants,
        "m35_coverage_weight_sweep": weights,
        "placebo_permutation": plc,
        "temperature_breakeven_reverse_stress": breakeven,
        "temperature_directional_scenarios": directional,
        "temperature_directional_by_month": directional_months,
        "leader_unchanged_in_every_run": bool(leader_same_everywhere),
        "lowest_prob_of_leader_first_across_runs": round(float(min_p), 4),
        "runs_below_bar_of_0_90": below_bar_runs,
        "run_counts": run_counts,
        "criteria": crit,
        "status": status,
        "confidence": confidence,
        "confidence_rule": "high: all seven criteria hold; moderate: the leader is the same in every re-run and split and c1 holds, the 0.90 bar being missed in some runs; none: the leader changes in any re-run or c1 fails. Written after the first verification (the criteria themselves were fixed before the run).",
        # lead_validated is set only when every criterion holds; lead_proposed is the leader of a lens that is not
        # contradicted by any re-run. A proposal is not a validated result.
        "lead_validated": star if not failing else None,
        "lead_proposed": star if confidence in ("high", "moderate") else None,
    }


def main():
    load_coverage()
    d_full, out_full, A0, full_sum, store = collect()
    placebo = permutation_placebo(d_full, PRIMARY, full_sum)
    identical = identical_inputs_check(d_full, PRIMARY)

    lens_res = {lens: build_lens_validation(lens, d_full, out_full, A0, full_sum, store, placebo) for lens in LENS_ORDER}
    for lens in LENS_ORDER:
        lens_res[lens]["placebo_identical_sourced_inputs_prob_first"] = identical[lens]

    j = {b: BASES.index(b) for b in BASES}
    T, Xm, chan, pen = out_full["T"], out_full["X"], out_full["chan"], out_full["pen"]
    pc = out_full["per_cell"]
    # Age-gradient-only ratio: the part that rests on a source (the per-year age odds ratio, carried and UNVERIFIED, and the
    # assumed elasticity). Men 25 to 34 and men 35 to 44 share the sex factor, price and base share, so the trial-propensity
    # ratio without the temperature sensitivity is (OR ** (MID25 - MID35)) ** e.
    age_only = (d_full["OR"] ** (MID["25"] - MID["35"])) ** d_full["e"]
    comparison = {
        "per_cell_ratio_men25_34_over_35_44": ratio_stats(pc[:, j["M25"]], pc[:, j["M35"]]),
        "age_gradient_only_ratio_men25_34_over_35_44": {
            **ratio_stats(age_only, np.ones_like(age_only)),
            "note": "(OR ** (29.5 - 39.5)) ** e from the same draws: the age odds ratio and the intent elasticity only. Reproduces rework/47 ratio A.",
        },
        "trial_propensity_ratio_men25_34_over_35_44_with_assumed_temperature_sensitivity": ratio_stats(T[:, j["M25"]], T[:, j["M35"]]),
        "exclusion_only_ratio_men25_34_over_35_44": ratio_stats(1 - Xm[:, j["M25"]], 1 - Xm[:, j["M35"]]),
        "reach_ratio_men45_59_over_25_34": ratio_stats(out_full["reach"][:, j["M45"]], out_full["reach"][:, j["M25"]]),
        "per_cell_ratio_men25_34_over_45_59": ratio_stats(pc[:, j["M25"]], pc[:, j["M45"]]),
        "per_cell_ratio_men25_34_over_45_59_components": {
            "drinking_share_ratio": ratio_stats(pen[:, j["M25"]], pen[:, j["M45"]]),
            "channel_ratio": ratio_stats(chan[:, j["M25"]], chan[:, j["M45"]]),
            "trial_propensity_ratio": ratio_stats(T[:, j["M25"]], T[:, j["M45"]]),
            "exclusion_ratio": ratio_stats(1 - Xm[:, j["M25"]], 1 - Xm[:, j["M45"]]),
            "note": "The product of the four component medians approximates the total ratio; components are drawn jointly so medians do not multiply exactly.",
        },
        "rework47_reference": {
            "ratio_A_men25_34_over_35_44": {"median": 1.0409, "p05": 0.9979, "p95": 1.0855, "prob_gt_1": 0.9411},
            "ratio_B_men25_34_over_45_59": {"median": 1.1474, "p05": 1.0260, "p95": 1.2837, "prob_gt_1": 0.9787,
                                           "log_decomposition": {"drinking_cells": 0.0478, "age_gradient": 0.0902}},
            "source": "rework/screen/segment_stat_results.json (ratio_A_*, ratio_B_*, log_ratio_B_decomposition_central)",
        },
    }
    # pair tests
    pair_age = comparison["age_gradient_only_ratio_men25_34_over_35_44"]
    pair_full = comparison["per_cell_ratio_men25_34_over_35_44"]
    decision_pairs = {
        "pair_men25_34_over_35_44_age_gradient_only_passes_bar": bool(pair_age["prob_gt_1"] >= TOP_P_THRESHOLD and pair_age["p05"] > 1.0),
        "pair_men25_34_over_35_44_full_model_passes_bar": bool(pair_full["prob_gt_1"] >= TOP_P_THRESHOLD and pair_full["p05"] > 1.0),
        "pair_bar_definition": "probability of a ratio above 1 at least 0.90 and the 5th percentile above 1",
    }
    # pool among all nine bases (reach)
    idx_all = list(range(len(BASES)))
    A0_reach = A0[PRIMARY]["reach"][0]
    reach_all = summarise(out_full["reach"][:, idx_all], BASES, A0_reach)

    result = {
        "task": "T15 ambient variation: potency of existing Singha customer bases (revision 3)",
        "seed": SEED, "draws_total": N, "draws_per_half": HALF, "permutations": N_PERM,
        "bases": {b: SHORT[b] for b in BASES},
        "existing_bases": EXISTING,
        "lens_definitions": {k: v[2] for k, v in LENSES.items()},
        "lenses": lens_res,
        "comparison_with_rework_46_47": comparison,
        "decision": {
            "statuses": {lens: lens_res[lens]["status"] for lens in LENS_ORDER},
            "leaders": {lens: lens_res[lens]["modal_top"] for lens in LENS_ORDER},
            "leader_prob_first": {lens: lens_res[lens]["prob_modal_top_first"] for lens in LENS_ORDER},
            "lowest_prob_of_leader_first_across_runs": {lens: lens_res[lens]["lowest_prob_of_leader_first_across_runs"] for lens in LENS_ORDER},
            "leader_unchanged_in_every_run": {lens: lens_res[lens]["leader_unchanged_in_every_run"] for lens in LENS_ORDER},
            "confidence": {lens: lens_res[lens]["confidence"] for lens in LENS_ORDER},
            "lead_validated": {lens: lens_res[lens]["lead_validated"] for lens in LENS_ORDER},
            "lead_proposed": {lens: lens_res[lens]["lead_proposed"] for lens in LENS_ORDER},
            "runs_below_bar_of_0_90": {lens: lens_res[lens]["runs_below_bar_of_0_90"] for lens in LENS_ORDER},
            "reach_lens_all_nine_bases_including_pool_prob_first": reach_all["prob_rank_first"],
            **decision_pairs,
        },
        "inputs": {
            "coverage_cells_read_from": COVERAGE_SOURCE,
            "sex_gradient": {"men_pct": SEX_MEN, "women_pct": SEX_WOMEN, "all_pct": SEX_ALL, "men_factor_centre": round(SEX_CENT, 4),
                             "range": SEX_RANGE, "source": "NSO 2021 Table 2 (printed p. 12), 5 or more days a week, ages 6 and over; range is an ASSUMPTION"},
            "contribution_centre_thb": C_CENT,
            "base_shelf_price_thb_assumption": PRICE_PLAN,
            "listing_parity_shelf_price_thb": PRICES[0],
            "t10_results_file_modified": __import__("datetime").datetime.fromtimestamp(os.path.getmtime(POTASSIUM_JSON)).isoformat(timespec="seconds"),
            "population_ranges": {
                "primary": "plus or minus %.2f percent per band (carried, UNVERIFIED)" % (100 * DOPA_GAP),
                "wide_sweep": "plus or minus %.1f percent for ages 25 to 34 and 35 to 44; %.1f to +%.1f percent for ages 45 to 59" % (
                    100 * POP_WIDE_YOUNG, 100 * POP45_LOW, 100 * POP45_HIGH),
            },
        },
        "assumptions": [
            "Intent link T = B x rho^e (power) or B x (1 + e(rho - 1)) (linear); rho = sweet-drink habit over the comparison cell (men 35 to 44). B and e are ASSUMPTIONS (rework/49).",
            "Sweet-drink habit differs by sex by the NSO 2021 Table 2 ratio (men 23.3, women 14.7, all 18.9 percent; 5 or more days a week, ages 6 and over) applied to the everyday band shares; the range 1.10 to 1.35 for the men's factor is an ASSUMPTION; no sex-by-age interaction is modelled.",
            "Potassium-caution coverage uses the rework/73 band cells for men (25-34, 35-44, 45-59) and both sexes (25-34, 35-44, 45-59, and adults 25-59 for the pool), narrow group, drawn as independent triangular variables; the cells are a team model (DERIVED, PROXY inputs), not survey cells. Women's bases use the both-sex band cells (PROXY).",
            "Alcohol-cue exclusion for drinker bases is an ASSUMPTION range 0 to 20 percent, mode 5 (no source; the team does not check the cue, rework/50 gate G1).",
            "Pool habit mapping k is log-uniform 0.5 to 2 (ASSUMPTION).",
            "Repeat, contribution, price and channel inputs are common across bases (or nearly so); they scale every base and cannot by themselves change the ranking.",
            "Temperature sensitivity beta is an ASSUMPTION range 0 to 0.05 per degree C, drawn independently for each base (a differential sensitivity; a common sensitivity cannot change a ranking); stress 0.15. A temperature-to-demand source was not searched for in this revision: every search attempt was refused by the turn's web search budget (T15/temperature_demand_source_search_record.md). The statement that temperature does not change a leader holds within the assumed range only; the reverse-stress runs show how large the differential sensitivity must be to change it.",
            "Bottled bases carry the sweet-drink habit twice in the primary model (as penetration, and as the habit ratio in trial propensity). This is a convention, not a sourced choice; the sweep bottled_habit_counted_once sets the ratio to 1.",
            "Population counts (DOPA), the age odds ratio and internet use are carried from earlier records and are UNVERIFIED (pages not saved). The primary population range (plus or minus 0.96 percent) is narrower than the repo's own alternatives; the sweep population_range_wide uses them.",
            "Drinking shares are 2024 values (inferred column); sweet-drink shares are 2021 values. The year-matched sweep uses the 2021 drinking column.",
            "No Singha sales, share or panel data exists in the public record. Every base is a market-pool proxy.",
        ],
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    make_chart(result, out_full)

    print("wrote", OUT_JSON)
    print("wrote", OUT_PNG)
    for lens in LENS_ORDER:
        r = lens_res[lens]
        print("LENS", lens, "| leader", r["modal_top"], "P", r["prob_modal_top_first"], "|", r["status"])
        print("  first-prob:", r["full_run"]["prob_rank_first"])
        print("  median order:", sorted(r["candidate_bases"], key=lambda b: -r["full_run"]["median"][b]))
        print("  kendall mean vs base:", r["full_run"]["kendall_tau_vs_base_mean"],
              "identical ranking share:", r["full_run"]["share_draws_identical_ranking_to_base"])
        print("  halves:", r["split_check"]["half_1_modal_top"], r["split_check"]["half_2_modal_top"],
              r["split_check"]["half_1_prob_first_of_full_leader"], r["split_check"]["half_2_prob_first_of_full_leader"])
        print("  forms:", {f: (v["modal_top"], v["prob_first_of_full_leader"]) for f, v in r["model_forms"].items()})
        print("  LOO min P:", min(x["prob_first_of_full_leader"] for x in r["leave_one_factor_out"]),
              "changes leader:", [x["factor_group_fixed_at_mean"] for x in r["leave_one_factor_out"] if x["changes_leader"]])
        print("  months P range:", min(m["prob_first_of_full_leader"] for m in r["ambient_by_month"]),
              max(m["prob_first_of_full_leader"] for m in r["ambient_by_month"]),
              "leaders:", sorted({m["modal_top"] for m in r["ambient_by_month"]}))
        print("  stress:", r["beta_stress_0_15"]["modal_top"], r["beta_stress_0_15"]["prob_first_of_full_leader"])
        print("  sweeps:", {v: (x["modal_top"], x["prob_first_of_full_leader"]) for v, x in r["structural_sweeps"].items()})
        print("  breakeven (beta_max -> leader, P):", {b: (x["modal_top"], x["prob_first_of_full_leader"]) for b, x in r["temperature_breakeven_reverse_stress"].items()})
        print("  directional (delta -> April leader, P; all-months leader, P):", {dl: (x["april_modal_top"], x["april_prob_first_of_full_leader"], x["all_months_modal_top"], x["all_months_prob_first_of_full_leader"]) for dl, x in r["temperature_directional_scenarios"].items()})
        print("  confidence:", r["confidence"], "| lead_validated:", r["lead_validated"], "| lead_proposed:", r["lead_proposed"])
        print("  runs below 0.90:", r["runs_below_bar_of_0_90"])
        print("  run counts:", r["run_counts"])
        print("  weights:", r["m35_coverage_weight_sweep"])
        print("  placebo:", r["placebo_permutation"])
        print("  identical inputs:", r["placebo_identical_sourced_inputs_prob_first"])
        print("  flips:", r["inputs_that_flip_ranking"])
        print("  criteria:", r["criteria"])
    print("ratios:")
    for k, v in comparison.items():
        print(" ", k, v)
    print("decision:", result["decision"])
    try:
        import psutil
        mi = psutil.Process().memory_info()
        print("peak working set (MB):", round(getattr(mi, "peak_wset", mi.rss) / 1e6, 1))
    except Exception:
        print("peak working set: psutil not available")


# ----------------------------------------------------------------------------------------------------------------
# Chart
# ----------------------------------------------------------------------------------------------------------------
def make_chart(result, out_full):
    lens_res = result["lenses"]
    BLUE, ORANGE, RED, GREY, GREEN = "#185FA5", "#D97B1A", "#B5462E", "#8C8C8C", "#2E7D4F"
    fig, axes = plt.subplots(2, 3, figsize=(24, 14), gridspec_kw={"width_ratios": [1.1, 1.0, 1.1]}, constrained_layout=True)

    # A. reach-lens potency with 90 percent interval, all nine bases
    ax = axes[0, 0]
    reach = out_full["reach"]
    med = {b: float(np.median(reach[:, BASES.index(b)])) for b in BASES}
    p05 = {b: float(np.percentile(reach[:, BASES.index(b)], 5)) for b in BASES}
    p95 = {b: float(np.percentile(reach[:, BASES.index(b)], 95)) for b in BASES}
    scale = max(med[b] for b in EXISTING)
    order = sorted(BASES, key=lambda b: -med[b])
    ys = np.arange(len(order))[::-1]
    for y, b in zip(ys, order):
        m, lo, hi = 100 * med[b] / scale, 100 * p05[b] / scale, 100 * p95[b] / scale
        col = GREY if b == "POOL" else BLUE
        ax.errorbar([m], [y], xerr=[[m - lo], [hi - m]], fmt="o", color=col, ecolor=col, capsize=4, markersize=7)
        ax.text(hi + 3, y, f"{m:.0f}", va="center", fontsize=10)
    ax.set_yticks(ys)
    ax.set_yticklabels([SHORT[b] for b in order], fontsize=10)
    ax.set_xlabel("Reach potency, median and 90 percent interval\n(best existing base median = 100)", fontsize=10)
    ax.set_title("A. Reach potency by customer base (grey = market pool)", fontsize=12, loc="left")
    ax.grid(axis="x", alpha=0.3)
    ax.set_xlim(0, 100 * max(p95[b] for b in BASES) / scale + 30)
    ax.tick_params(axis="x", labelsize=10)

    # B. heat table: probability of ranking first, by base and lens
    ax = axes[0, 1]
    mat = np.full((len(EXISTING), len(LENS_ORDER)), np.nan)
    for c, lens in enumerate(LENS_ORDER):
        for b, p in lens_res[lens]["full_run"]["prob_rank_first"].items():
            mat[EXISTING.index(b), c] = 100 * p
    ax.imshow(np.nan_to_num(mat, nan=0), cmap="Blues", vmin=0, vmax=100, aspect="auto")
    for r in range(mat.shape[0]):
        for c in range(mat.shape[1]):
            if np.isnan(mat[r, c]):
                ax.text(c, r, "n/a", ha="center", va="center", fontsize=10, color="#555")
            else:
                ax.text(c, r, f"{mat[r, c]:.0f}%", ha="center", va="center", fontsize=11,
                        color="white" if mat[r, c] > 55 else "black", fontweight="bold" if mat[r, c] >= 20 else "normal")
    ax.set_xticks(range(len(LENS_ORDER)))
    ax.set_xticklabels(["Reach\n(total)", "Per person\nin cell\n(drinker cells)", "Per person\nin cell\n(all bases)", "Per member\nof base"], fontsize=10)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(EXISTING)))
    ax.set_yticklabels([SHORT[b] for b in EXISTING], fontsize=10)
    ax.set_title("B. Share of draws ranked first, by lens (percent)", fontsize=12, loc="left", pad=48)

    # C. months
    ax = axes[0, 2]
    colors = {"reach": BLUE, "per_cell_drinkers": ORANGE, "per_cell_all": GREY, "per_member": GREEN}
    marks = {"reach": "o", "per_cell_drinkers": "s", "per_cell_all": "^", "per_member": "D"}
    labels = {"reach": "Reach", "per_cell_drinkers": "Per person in cell",
              "per_cell_all": "Per person in cell (all bases)", "per_member": "Per member of base"}
    xs = np.arange(12)
    for lens in ("reach", "per_cell_drinkers", "per_member"):
        ys_ = [100 * m["prob_first_of_full_leader"] for m in lens_res[lens]["ambient_by_month"]]
        extra = ""
        ax.plot(xs, ys_, marker=marks[lens], color=colors[lens], lw=1.8, ms=6,
                label=f"{labels[lens]}: {SHORT[lens_res[lens]['modal_top']].replace(' drinkers', '')}")
    for dl, sty in (("0.03", ":"), ("0.05", "-.")):
        rows = lens_res["per_cell_drinkers"]["temperature_directional_by_month"][dl]
        ax.plot(xs, [100 * m["prob_first_of_full_leader"] for m in rows], ls=sty, color=ORANGE, lw=1.4,
                label=f"Per person, men 35-59 more heat-sensitive by {float(dl):.2f} per C (assumed)")
    ax.axhline(90, color="black", lw=1, ls="--")
    ax.text(11.2, 91, "bar 90%", ha="right", fontsize=9)
    ax.set_xticks(xs)
    ax.set_xticklabels([f"{m}\n{t}" for m, t in zip(TMD_NAMES, TMD)], fontsize=9)
    ax.set_ylim(0, 150)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylabel("Probability the full-run leader ranks first (percent)", fontsize=10)
    ax.set_xlabel("Month and Bangkok mean temperature, degrees C (TMD 1991 to 2020)", fontsize=10)
    ax.set_title("C. Ambient temperature: leader's first-place probability by month", fontsize=12, loc="left")
    ax.legend(fontsize=8.5, loc="upper center", frameon=True)
    ax.grid(alpha=0.3)
    ax.tick_params(axis="y", labelsize=10)

    # D and E. tornados
    def tornado(ax, lens, title):
        r = lens_res[lens]
        rows = r["quintile_tornado_sorted_by_swing"][:10]
        yc = np.arange(len(rows))[::-1]
        sw = [100 * x["swing_high_minus_low"] for x in rows]
        cols = [RED if x["flips_ranking"] else "#7FA9D1" for x in rows]
        ax.barh(yc, sw, color=cols)
        ax.axvline(0, color="black", lw=0.8)
        ax.set_yticks(yc)
        ax.set_yticklabels([x["factor_group"] for x in rows], fontsize=9)
        for y, s_ in zip(yc, sw):
            ax.text(s_ + (1.0 if s_ >= 0 else -1.0), y, f"{s_:+.1f}", va="center", ha="left" if s_ >= 0 else "right", fontsize=9)
        lim = max(abs(min(sw)), abs(max(sw)), 5) * 1.35
        ax.set_xlim(-lim, lim)
        ax.set_xlabel(f"Change in probability that {SHORT[r['modal_top']]} ranks first (points),\nhighest fifth of the input minus lowest fifth", fontsize=9.5)
        ax.set_title(title, fontsize=12, loc="left")
        ax.grid(axis="x", alpha=0.3)
        ax.tick_params(axis="x", labelsize=10)

    tornado(axes[1, 0], "reach", "D. Tornado, reach lens (red = the top base changes)")
    tornado(axes[1, 1], "per_cell_drinkers", "E. Tornado, per person in cell, drinker cells")

    # F. check matrix
    ax = axes[1, 2]
    crits = ["c1", "c2", "c3", "c4", "c5", "c6", "c7"]
    cm = np.zeros((len(LENS_ORDER), len(crits)))
    for r_, lens in enumerate(LENS_ORDER):
        for c_, k in enumerate(lens_res[lens]["criteria"]):
            cm[r_, c_] = 1.0 if lens_res[lens]["criteria"][k] else 0.0
    from matplotlib.colors import ListedColormap
    ax.imshow(cm, cmap=ListedColormap(["#E9B8AC", "#B8DAC4"]), vmin=0, vmax=1, aspect="auto")
    for r_ in range(cm.shape[0]):
        for c_ in range(cm.shape[1]):
            ax.text(c_, r_, "pass" if cm[r_, c_] else "FAIL", ha="center", va="center", fontsize=11, fontweight="bold",
                    color=GREEN if cm[r_, c_] else RED)
    ax.set_xticks(range(len(crits)))
    ax.set_xticklabels(["c1\nfull", "c2\nhalves", "c3\nforms", "c4\nleave-\none-out", "c5\nmonths\nstress", "c6\nplacebo", "c7\nsweeps"], fontsize=9)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(LENS_ORDER)))
    ax.set_yticklabels(["Reach", "Per person in cell\n(drinker cells)", "Per person in cell\n(all bases)", "Per member\nof base"], fontsize=10)
    ax.set_title("F. Validation checks by lens (bar: leader first in at least 90 percent)", fontsize=12, loc="left", pad=48)

    fig.text(0.5, -0.012, f"Potency of existing Singha customer bases under ambient and input variation ({N:,} draws, seed {SEED}). "
             "Market-pool proxies, not Singha sales. Per-person lens: denominator is the age-sex cell; per-member lens: denominator is population x penetration.",
             ha="center", va="top", fontsize=12)
    os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
    fig.savefig(OUT_PNG, dpi=130, bbox_inches="tight")


if __name__ == "__main__":
    main()
