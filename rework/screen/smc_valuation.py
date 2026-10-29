"""Task T14: sequential Monte Carlo on the Lemon Soda valuation and the 13-week pilot (third pass).

Team-only desk model. numpy, scipy, matplotlib (psutil optional, for the memory log). Fixed seed.
    python -I smc_valuation.py            full run (about 8 minutes, one process)
    SMC_QUICK=1 python -I smc_valuation.py  smoke test with small sizes; writes to a scratch folder

Third-pass additions (they use their own random streams, so every second-pass number is reproduced):
    * pilot_evolution: P(NPV > 0), the expected NPV, P(demand >= 3) and the width of the 90 percent demand band by
      pilot week, averaged over R_EVO simulated 20-store pilots per truth (mean and 10th to 90th percentile).
      NPV is linear in volume, so P(NPV > 0 | data) is mapped from each filter's particles through the exact
      conditional P(NPV > 0 | volume) of the prior (Rao-Blackwellised).
    * value of waiting under three scoring conventions (start-of-pilot level, level at the decision week, common
      week-13 level), because the sign of a difference of a few thousand THB depends on the convention.
    * Monte Carlo standard errors on the separation powers; delay discount factor for a five-week wait.

Reads (numbers are read from these files, not retyped):
    project_valuation_results.json     record 05 (base NPV, break-even volume)
    value_accrual_model_results.json   record 75 (after-excise contribution 3.9444, chain ratio 0.535628,
                                       after-tax NPV 165,023.77 used as the reconciliation target)
    segment_stat_results.json          record 47 (ratio A median and 90% interval)
    conversion_synthesis_results.json  record 49 (synthesis direction probability)
Writes:
    smc_valuation_results.json         every number quoted in rework/77
    rework/charts/smc_npv_distribution.png, smc_pilot_posterior_fan.png, smc_operating_characteristics.png,
    smc_expected_npv_by_demand.png

Parts
  A  Prior predictive Monte Carlo of the project cash flows, with a prior for every input. Variants:
       A   record 05 structure (before excise, pre-tax, binder 0, citric 2.10 g, no cannibalisation)
       B   full stated prior (before excise, pre-tax)                                  [pre-registered headline]
       C   B with 20 percent tax, no loss relief and no depreciation shield
       A2  A on the after-excise basis;  B2  B on the after-excise basis
       D   record 75 lead basis: after excise, 20 percent tax, same-year loss offset, 5-year straight-line
           depreciation shield (the structure of rework/75), full stated prior
       D_cf  D with a stand-alone entity and a five-year loss carry-forward (Revenue Department page 6044)
       B_wide, D_wide  B and D with a repeat prior that has mass below the 15 percent stop floor
       B_rho0  B without the price and volume correlation
  B  Bootstrap particle filter for the latent weekly demand of the pilot. Resampling when ESS < N/2.
     Liu-West kernel (discount 0.98) updates the weekly drift. Fixed-demand tables, expected-NPV break-even
     demand, operating characteristics, separation power and the value of the pilot (like for like).
  C  Significance tests, fixed before the run and written here:
     (i)   H0: NPV <= 0. Reject H0 if P(NPV > 0) >= 0.95 under variant B (pre-registered headline). The same
           rule is applied to every other variant and reported. The 90% credible interval is reported.
     (ii)  Segment lead (men 25-34 over men 35-44): significant only if P(ratio > 1) >= 0.95 and the 90%
           interval excludes 1. Power is reported at the affordable survey cell size (1,377).
     (iii) Pilot rule: a read says "at or above 3" if P(demand >= 3 | data) >= 0.5. Scale if the reads at
           weeks 8 and 13 both say "at or above"; stop if both say below; otherwise hold (the read weeks are
           an ASSUMPTION). A truth pair is separated if P(demand > midpoint | data) >= 0.9 or <= 0.1, with
           80% power as the target.

Model probabilities are conditional on the stated priors and are not findings from market data.
"""

import gc
import json
import math
import os
import time

import numpy as np
from scipy import stats
from scipy.optimize import brentq

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

try:
    import psutil
except Exception:  # pragma: no cover
    psutil = None

QUICK = os.environ.get("SMC_QUICK") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
if QUICK:
    SCRATCH = os.environ.get("SMC_SCRATCH", os.path.join(HERE, "_quick"))
    os.makedirs(SCRATCH, exist_ok=True)
    CHART_DIR = SCRATCH
    OUT_JSON = os.path.join(SCRATCH, "smc_valuation_results_quick.json")
else:
    CHART_DIR = os.path.join(REPO, "rework", "charts")
    OUT_JSON = os.path.join(HERE, "smc_valuation_results.json")
PV_JSON = os.path.join(HERE, "project_valuation_results.json")
VA_JSON = os.path.join(HERE, "value_accrual_model_results.json")
CAN_JSON = os.path.join(HERE, "can_cost_model_results.json")
SEG_JSON = os.path.join(HERE, "segment_stat_results.json")
SYN_JSON = os.path.join(HERE, "conversion_synthesis_results.json")

SEED = 20261020
if QUICK:
    N_PRIOR, N_FAN, N_PF = 20_000, 20_000, 1_000
    R_OC, R_SIG, R_CAL, R_CAL_BIG, N_PF_BIG = 20, 10, 10, 5, 3_000
    N_VOI, N_VOI_SENS, R_REP = 400, 200, 2_000
    N_VOI_BIG = 600
    R_EVO = 20
else:
    N_PRIOR = 200_000        # prior predictive draws
    N_FAN = 200_000          # particles for the representative pilot fan (at most 200,000)
    N_PF = 2_000             # particles per pilot in the operating-characteristic runs
    R_OC = 300               # pilots per (store count, true demand) cell
    R_SIG = 200              # pilots per cell in the store-heterogeneity and drift sensitivities
    R_CAL = 300              # pilots per truth in the calibration check (2,000 particles)
    R_CAL_BIG = 100          # pilots per truth in the calibration check with more particles
    N_PF_BIG = 10_000        # particles in that check
    N_VOI = 10_000           # truths in the value-of-the-pilot experiment
    N_VOI_BIG = 30_000       # truths in the larger run that compares the scoring conventions
    N_VOI_SENS = 3_000       # truths in the store-equivalent sensitivity of that experiment
    R_REP = 20_000           # draws in the repeat-rule experiment
    R_EVO = 300              # simulated pilots per truth in the week-by-week evolution of P(NPV > 0)
SIGMA_ETA_ALT = 0.005    # weekly drift noise in the drift sensitivity (ASSUMPTION)
S_LIST = (5, 10, 15, 20, 30, 40)
LAM_GRID = (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0)
TRUTHS = (1.5, 3.0, 4.5)  # low, base, high
S_FAN = 20
S_VOI = 20
T = 13
WEEK_IDX = {w: w - 1 for w in range(1, 14)}
READS = (8, 13)          # read weeks: ASSUMPTION (the plan says two consecutive reads, without dates)
RULE_THR = 3.0           # units per store per week
RULE_P = 0.5             # a read says "at or above" if P(demand >= 3 | data) >= 0.5
POST_HI, POST_LO = 0.90, 0.10
POWER_TARGET = 0.80
ALPHA_H0 = 0.95
FALSE_MAX = 0.10
SEP_WEEKS = (4, 6, 8, 10, 12, 13)

KAPPA = 5.0               # NB size per store per week (ASSUMPTION)
LOG_K = math.log(KAPPA)
SIGMA_ETA = 0.02          # weekly log-demand drift noise (ASSUMPTION)
MU_SD = 0.02              # prior sd of the weekly drift (ASSUMPTION)
DELTA_LW = 0.98           # Liu-West discount
A_LW = (3.0 * DELTA_LW - 1.0) / (2.0 * DELTA_LW)
H_LW = math.sqrt(1.0 - A_LW * A_LW)
STORE_SD = 0.30           # store-to-store log-sd of weekly demand (ASSUMPTION)
N_EFF = 1282              # store-equivalents: ASSUMPTION chosen so that 3 units per store-week = 200,000 cubes
N_EFF_SENS = (1000, 1282, 2000)
WEEKS_PER_YEAR = 52
RHO = -0.30               # shelf price and first-purchase volume copula correlation (ASSUMPTION)
TAX = 0.20                # Thai corporate income tax rate: S (primary-origin page read through a page summary), Revenue Department page 6044
QS3 = (0.05, 0.50, 0.95)
Z90 = 1.6448536269514722

# ---- Record inputs (THB unless stated) -------------------------------------
K_G = 0.811               # potassium bicarbonate per cube, g (DERIVED, record 05)
S_MG = 33.0               # sucralose per cube, mg (DERIVED, record 05)
P_K_MED, P_C_MED, P_S_MED = 38.1, 31.4, 655.0   # THB per kg (PROXY, UNVERIFIED; record 05)
POUCH_MED, PRINT_MED, PROC_MED, CARTON6_MED = 1.30, 1.50, 0.50, 4.00
N_FIRST_MED = 200_000.0 * (1.0 - 0.30)  # first purchases a year so that the base gives 200,000 cubes (DERIVED)
N_SD = 0.38               # log-sd of first-purchase cubes (PROXY: record 70 bottom-up 90% range)
REP_MEAN, REP_LO, REP_HI = 0.30, 0.15, 0.40   # submission/06_kpi.md repeat target, floor and bounds
REP_WIDE_MEAN, REP_WIDE_SD = (REP_LO + REP_MEAN + REP_HI) / 3.0, 0.10  # wide repeat prior (ASSUMPTION)
K_MEAN, K_LO, K_HI = 0.25, 0.05, 0.50         # cannibalisation share (ASSUMPTION; record 70 cases)
CCAN_LO, CCAN_MODE, CCAN_HI = 3.38, 4.13, 5.68  # record 70 section 2.11, THB per can, aluminium excluded
F_MED, F_SD = 500_000.0, 0.42                  # annual fixed cost (ASSUMPTION; record 05 grid 250,000 to 2,000,000)
RD_LO, RD_HI = 0.08, 0.12                      # discount rate (ASSUMPTION; record 05)
RAMP_LO, RAMP_HI = 0.30, 0.70                  # year-1 share of steady volume (ASSUMPTION; record 05 uses 0.5)
C_G_LO, C_G_HI = 2.10, 3.70                    # citric acid per cube, g (DERIVED: pH 3.5 and pH 3.0)
BINDER_HI = 0.30                               # binder and flavour per cube, THB (ASSUMPTION; unpriced)
CITRIC_RECORD = 2.10
SHARE_BASE = 0.60                              # record 05 ex-factory share of the shelf price
# after-excise chain ratio (record 75): read from the results file in main(), 0.535628
CHAIN_RATIO = 0.535628


def beta_from_mean_90(mean, lo, hi):
    """Beta parameters with the given mean and 5th and 95th percentiles near lo and hi."""
    sd = (hi - lo) / (2.0 * Z90)
    v = sd * sd
    s = mean * (1.0 - mean) / v - 1.0
    return mean * s, (1.0 - mean) * s


def beta_from_mean_sd(mean, sd):
    s = mean * (1.0 - mean) / (sd * sd) - 1.0
    return mean * s, (1.0 - mean) * s


A_K, B_K = beta_from_mean_90(K_MEAN, K_LO, K_HI)
A_REPW, B_REPW = beta_from_mean_sd(REP_WIDE_MEAN, REP_WIDE_SD)


def breakeven_lambda():
    """Point-value demand per store per week at which NPV is zero, record 05 base (c 4.91, F 500,000, 10 percent).
    DERIVED at input medians, before excise and before tax; depends on N_EFF (ASSUMPTION)."""
    rd, c, F = 0.10, 4.91, 500_000.0
    disc = (1.0 + rd) ** -np.arange(1, 6)
    A = disc.sum()
    R = 0.5 * disc[0] + disc[1:].sum()
    v_star = F * (1.0 + A) / (c * R)
    return v_star / (WEEKS_PER_YEAR * N_EFF), v_star


LAM_BE, V_STAR = breakeven_lambda()

# Posterior thresholds carried by the filter. BASE_THR holds the midpoints used for separation and the
# rule line (3.0); the named thresholds are added in main() once the expected-NPV break-evens are known.
BASE_THR = [round(float(x), 2) for x in np.arange(1.25, 5.76, 0.25)]
TI_G = {x: i for i, x in enumerate(BASE_THR)}
THRS = np.array(BASE_THR, dtype=float)   # extended in main()
TI_N = {}                                  # name -> index of a named threshold
PAIRS = {"1.5_vs_3.0": (1.5, 3.0), "3.0_vs_4.5": (3.0, 4.5), "1.5_vs_4.5": (1.5, 4.5)}
LIN_VARIANTS = {          # name -> (record structure, after excise, tax mode)
    "A": (True, False, "none"),
    "B": (False, False, "none"),
    "A2": (True, True, "none"),
    "B2": (False, True, "none"),
    "D": (False, True, "relief_shield"),
}
FAN_VARS = ("A", "B", "D")


def prior_draws(n, rng):
    """Raw prior draws. Gaussian copula links the shelf price and the first-purchase volume.
    The first 18 inputs are drawn in the same order as the first pass, so variants A, B, C reproduce it."""
    zP = rng.standard_normal(n)
    zN = RHO * zP + math.sqrt(1.0 - RHO * RHO) * rng.standard_normal(n)
    raw = {}
    raw["shelf_price"] = 10.0 + 10.0 * stats.norm.cdf(zP)
    raw["first_purchase_cubes"] = np.exp(math.log(N_FIRST_MED) + N_SD * zN)
    raw["ex_factory_share"] = rng.uniform(0.50, 0.70, n)
    raw["repeat_rate"] = rng.triangular(REP_LO, REP_MEAN, REP_HI, n)
    raw["year1_ramp"] = rng.uniform(RAMP_LO, RAMP_HI, n)
    raw["khco3_price"] = P_K_MED * np.exp(0.25 * rng.standard_normal(n))
    raw["citric_price"] = P_C_MED * np.exp(0.25 * rng.standard_normal(n))
    raw["sucralose_price"] = P_S_MED * np.exp(0.25 * rng.standard_normal(n))
    raw["citric_mass"] = rng.uniform(C_G_LO, C_G_HI, n)
    raw["pouch"] = POUCH_MED * np.exp(0.42 * rng.standard_normal(n))
    raw["print"] = PRINT_MED * np.exp(0.35 * rng.standard_normal(n))
    raw["processing"] = PROC_MED * np.exp(0.42 * rng.standard_normal(n))
    raw["carton_per_6"] = CARTON6_MED * np.exp(0.33 * rng.standard_normal(n))
    raw["binder_flavour"] = rng.uniform(0.0, BINDER_HI, n)
    raw["cannibal_share"] = rng.beta(A_K, B_K, n)
    raw["can_contribution"] = rng.triangular(CCAN_LO, CCAN_MODE, CCAN_HI, n)
    raw["fixed_cost"] = F_MED * np.exp(F_SD * rng.standard_normal(n))
    raw["discount_rate"] = rng.uniform(RD_LO, RD_HI, n)
    # added in the second pass (drawn after the first 18, so the first pass is reproduced)
    raw["repeat_wide"] = rng.beta(A_REPW, B_REPW, n)
    raw["first_purchase_rho0"] = np.exp(math.log(N_FIRST_MED) + N_SD * rng.standard_normal(n))
    return raw


def derive(raw, record_structure, after_excise=False, wide_repeat=False, rho0=False):
    """Contribution, volume and the cash-flow inputs. record_structure=True is the record 05 structure."""
    n = len(raw["shelf_price"])
    if record_structure:
        binder = np.zeros(n)
        mc = np.full(n, CITRIC_RECORD)
        k = np.zeros(n)
    else:
        binder = raw["binder_flavour"]
        mc = raw["citric_mass"]
        k = raw["cannibal_share"]
    reactants = K_G * raw["khco3_price"] / 1000.0 + mc * raw["citric_price"] / 1000.0 + S_MG * raw["sucralose_price"] / 1e6
    cost = reactants + raw["pouch"] + raw["print"] + raw["processing"] + raw["carton_per_6"] / 6.0 + binder
    share = raw["ex_factory_share"] * ((CHAIN_RATIO / SHARE_BASE) if after_excise else 1.0)
    c = share * raw["shelf_price"] - cost
    rep = raw["repeat_wide"] if wide_repeat else raw["repeat_rate"]
    first = raw["first_purchase_rho0"] if rho0 else raw["first_purchase_cubes"]
    V = first / (1.0 - rep)
    return {"c": c, "cost": cost, "reactants": reactants, "k": k, "cc": raw["can_contribution"],
            "V": V, "F": raw["fixed_cost"], "rd": raw["discount_rate"], "ramp1": raw["year1_ramp"]}


def cash_flows(c, k, cc, V, F, ramp1, mode="none"):
    """Years 1 to 5. Net contribution per cube is c minus k times the can contribution lost.
    mode: none (pre-tax); no_relief (20 percent on positive annual operating profit); relief_shield (record 75:
    tax on operating profit less straight-line depreciation of the year-0 outlay, losses credited in the year);
    carry_forward (stand-alone entity: depreciation deducted, losses carried forward up to five years)."""
    net = c - k * cc
    n = len(V)
    cf = np.empty((n, 5))
    dep = F / 5.0
    nol = np.zeros(n)
    for t in range(5):
        ramp = ramp1 if t == 0 else 1.0
        ebitda = net * V * ramp - F
        if mode == "none":
            cf[:, t] = ebitda
        elif mode == "no_relief":
            cf[:, t] = ebitda - TAX * np.maximum(ebitda, 0.0)
        elif mode == "relief_shield":
            cf[:, t] = ebitda - TAX * (ebitda - dep)
        elif mode == "carry_forward":
            taxable = ebitda - dep
            use = np.where(taxable > 0, np.minimum(nol, taxable), 0.0)
            nol = nol - use + np.maximum(-taxable, 0.0)
            cf[:, t] = ebitda - TAX * np.maximum(taxable - use, 0.0)
        else:
            raise ValueError(mode)
    return cf


def npv_of(cf, F, rd):
    disc = (1.0 + rd)[:, None] ** -np.arange(1, 6)[None, :]
    return -F + np.sum(cf * disc, axis=1)


def alpha_beta(d, mode):
    """NPV is linear in volume for the pre-tax and relief_shield structures: NPV = alpha * V - beta."""
    disc = (1.0 + d["rd"])[:, None] ** -np.arange(1, 6)[None, :]
    A = disc.sum(axis=1)
    R = d["ramp1"] * disc[:, 0] + disc[:, 1:].sum(axis=1)
    net = d["c"] - d["k"] * d["cc"]
    F = d["F"]
    if mode == "none":
        return net * R, F * (1.0 + A)
    if mode == "relief_shield":
        return (1.0 - TAX) * net * R, F * (1.0 + A * (1.2 * (1.0 - TAX) - 0.2))
    raise ValueError(mode)


def irr_vec(F, cf):
    n = len(F)

    def f(r):
        disc = (1.0 + r)[:, None] ** -np.arange(1, 6)[None, :]
        return -F + np.sum(cf * disc, axis=1)

    lo = np.full(n, -0.9)
    hi = np.full(n, 10.0)
    flo = f(lo)
    fhi = f(hi)
    ok = np.sign(flo) != np.sign(fhi)
    a = lo.copy()
    b = hi.copy()
    fa = flo.copy()
    for _ in range(60):
        m = 0.5 * (a + b)
        fm = f(m)
        same = np.sign(fm) == np.sign(fa)
        a = np.where(same, m, a)
        fa = np.where(same, fm, fa)
        b = np.where(same, b, m)
    return np.where(ok, 0.5 * (a + b), np.nan)


def payback_vec(F, cf):
    n = len(F)
    cum = -F.copy()
    pb = np.full(n, np.nan)
    for t in range(5):
        prev = cum.copy()
        cum = prev + cf[:, t]
        hit = np.isnan(pb) & (cum >= 0) & (prev < 0)
        pb[hit] = t + (-prev[hit]) / cf[hit, t]
    return pb


def batch_se(x, stat, nb=20):
    chunks = np.array_split(x, nb)
    vals = []
    for ch in chunks:
        ch = ch[~np.isnan(ch)]
        if len(ch) > 1:
            vals.append(stat(ch))
    if len(vals) < 2:
        return None
    return float(np.std(vals, ddof=1) / math.sqrt(len(vals)))


def summarise_npv(npv, irr, pb):
    n = len(npv)
    p = float(np.mean(npv > 0))
    out = {
        "n_draws": n,
        "P_NPV_gt_0": p,
        "MC_SE_P": math.sqrt(p * (1 - p) / n),
        "mean_THB": float(npv.mean()),
        "MC_SE_mean_THB": float(npv.std(ddof=1) / math.sqrt(n)),
        "median_THB": float(np.median(npv)),
        "MC_SE_median_THB": batch_se(npv, np.median),
        "p05_THB": float(np.percentile(npv, 5)),
        "MC_SE_p05_THB": batch_se(npv, lambda z: np.percentile(z, 5)),
        "p95_THB": float(np.percentile(npv, 95)),
        "MC_SE_p95_THB": batch_se(npv, lambda z: np.percentile(z, 95)),
        "sd_THB": float(npv.std(ddof=1)),
    }
    ok = ~np.isnan(irr)
    sh = float(ok.mean())
    out["IRR"] = {
        "share_defined": sh,
        "MC_SE_share_defined": math.sqrt(sh * (1 - sh) / n),
        "median": float(np.median(irr[ok])) if ok.any() else None,
        "MC_SE_median": batch_se(irr, np.median) if ok.any() else None,
        "p05": float(np.percentile(irr[ok], 5)) if ok.any() else None,
        "MC_SE_p05": batch_se(irr, lambda z: np.percentile(z, 5)) if ok.any() else None,
        "p95": float(np.percentile(irr[ok], 95)) if ok.any() else None,
        "MC_SE_p95": batch_se(irr, lambda z: np.percentile(z, 95)) if ok.any() else None,
        "share_above_discount_rate_10pct_among_defined": float(np.mean(irr[ok] > 0.10)) if ok.any() else None,
    }
    paid = ~np.isnan(pb)
    sp = float(paid.mean())
    p2 = float(np.mean(paid & (pb <= 2.0)))
    out["payback_years"] = {
        "share_within_5_years": sp,
        "MC_SE_share_within_5_years": math.sqrt(sp * (1 - sp) / n),
        "P_within_2_years_all_draws": p2,
        "MC_SE_P_within_2_years_all_draws": math.sqrt(p2 * (1 - p2) / n),
        "median_if_paid": float(np.median(pb[paid])) if paid.any() else None,
        "MC_SE_median_if_paid": batch_se(pb, np.median) if paid.any() else None,
        "p05_if_paid": float(np.percentile(pb[paid], 5)) if paid.any() else None,
        "MC_SE_p05_if_paid": batch_se(pb, lambda z: np.percentile(z, 5)) if paid.any() else None,
        "p95_if_paid": float(np.percentile(pb[paid], 95)) if paid.any() else None,
        "MC_SE_p95_if_paid": batch_se(pb, lambda z: np.percentile(z, 95)) if paid.any() else None,
    }
    return out


def first_order_index(x, y, nb=50):
    edges = np.quantile(x, np.linspace(0.0, 1.0, nb + 1))
    idx = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, nb - 1)
    counts = np.bincount(idx, minlength=nb).astype(float)
    sums = np.bincount(idx, weights=y, minlength=nb)
    means = sums / np.maximum(counts, 1.0)
    wts = counts / len(x)
    m = y.mean()
    return float(np.sum(wts * (means - m) ** 2) / y.var())


SENS_NAMES = {
    "shelf_price": "Shelf price (THB)",
    "ex_factory_share": "Ex-factory share",
    "first_purchase_cubes": "First-purchase cubes a year",
    "repeat_rate": "Repeat rate",
    "year1_ramp": "Year-1 ramp",
    "fixed_cost": "Fixed cost (THB a year)",
    "discount_rate": "Discount rate",
    "pouch": "Pouch (THB)",
    "print": "Print (THB)",
    "processing": "Processing (THB)",
    "carton_per_6": "Carton per 6 cubes (THB)",
    "binder_flavour": "Binder and flavour (THB)",
    "citric_mass": "Citric acid mass (g)",
    "khco3_price": "Bicarbonate price",
    "citric_price": "Citric acid price",
    "sucralose_price": "Sucralose price",
    "cannibal_share": "Cannibalisation share",
    "can_contribution": "Can contribution (THB)",
}


def sensitivity(raw, y):
    sens = []
    base_p = float(np.mean(y > 0))
    for key, label in SENS_NAMES.items():
        x = raw[key]
        edges = np.quantile(x, np.linspace(0, 1, 11))
        idx = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, 9)
        p_bins = [float(np.mean(y[idx == j] > 0)) for j in range(10)]
        q25, q75 = np.percentile(x, [25, 75])
        mask = (x >= q25) & (x <= q75)
        p_iqr = float(np.mean(y[mask] > 0))
        p_mid = 0.5 * (p_bins[4] + p_bins[5])
        nbe = 25
        ed2 = np.quantile(x, np.linspace(0, 1, nbe + 1))
        ix2 = np.clip(np.searchsorted(ed2, x, side="right") - 1, 0, nbe - 1)
        cn2 = np.bincount(ix2, minlength=nbe).astype(float)
        m2 = np.bincount(ix2, weights=y, minlength=nbe) / np.maximum(cn2, 1.0)
        evppi = float(np.sum(cn2 / len(x) * np.maximum(m2, 0.0)) - max(float(y.mean()), 0.0))
        sens.append({
            "EVPPI_THB": round(evppi, 0),
            "input": label,
            "key": key,
            "variance_based_first_order_index": round(first_order_index(x, y), 4),
            "spearman_rank_correlation_with_NPV": round(float(stats.spearmanr(x, y).correlation), 4),
            "P_NPV_gt_0_by_prior_decile": [round(v, 4) for v in p_bins],
            "P_NPV_gt_0_by_decile_range": round(max(p_bins) - min(p_bins), 4),
            "P_NPV_gt_0_if_pinned_near_median": round(p_mid, 4),
            "P_NPV_gt_0_if_narrowed_to_IQR": round(p_iqr, 4),
            "change_in_P_if_narrowed_to_IQR": round(p_iqr - base_p, 4),
        })
    sens.sort(key=lambda d: -d["variance_based_first_order_index"])
    return sens


def joint_narrowing(npv, raw, V, has_k):
    """Scan joint restrictions on fixed cost (upper quantile), shelf price (lower quantile), cannibalisation
    (upper quantile) and steady volume (lower quantile). Report the best conditional probability for several
    prior-mass floors, the named tertile scenario, and the smallest-mass region that reaches 0.95."""
    F = raw["fixed_cost"]
    pr = raw["shelf_price"]
    k = raw["cannibal_share"]
    qF = {u: np.quantile(F, u) for u in (0.10, 0.20, 0.33, 0.50, 1.0)}
    qP = {u: np.quantile(pr, u) for u in (0.0, 0.50, 0.67, 0.80, 0.90)}
    qK = {u: np.quantile(k, u) for u in ((0.20, 0.33, 0.50, 1.0) if has_k else (1.0,))}
    qV = {u: np.quantile(V, u) for u in (0.0, 0.33, 0.50, 0.67)}
    rows = []
    n = len(npv)
    pos = npv > 0
    for uF, tF in qF.items():
        mF = F <= tF
        for uP, tP in qP.items():
            mFP = mF & (pr >= tP)
            for uK, tK in qK.items():
                mFPK = mFP & (k <= tK)
                for uV, tV in qV.items():
                    m = mFPK & (V >= tV)
                    cnt = int(m.sum())
                    if cnt < 200:
                        continue
                    rows.append({"fixed_cost_upper_q": uF, "price_lower_q": uP, "cannibal_upper_q": uK,
                                 "volume_lower_q": uV, "prior_mass": cnt / n, "P_NPV_gt_0": float(pos[m].mean())})
    best_by_mass = {}
    for floor in (0.20, 0.10, 0.05, 0.02, 0.01):
        cand = [r for r in rows if r["prior_mass"] >= floor]
        best_by_mass[str(floor)] = max(cand, key=lambda r: r["P_NPV_gt_0"]) if cand else None
    reach = [r for r in rows if r["P_NPV_gt_0"] >= ALPHA_H0]
    smallest = max(reach, key=lambda r: r["prior_mass"]) if reach else None  # largest mass that still reaches 0.95
    tert = (F <= np.quantile(F, 0.33)) & (pr >= np.quantile(pr, 0.67))
    tert2 = tert & (k <= np.quantile(k, 0.33)) if has_k else tert
    return {
        "tertile_F_low_and_price_high": {"prior_mass": float(tert.mean()), "P_NPV_gt_0": float(pos[tert].mean())},
        "tertile_F_low_price_high_and_cannibal_low": {"prior_mass": float(tert2.mean()),
                                                       "P_NPV_gt_0": float(pos[tert2].mean())},
        "best_region_by_minimum_prior_mass": best_by_mass,
        "largest_region_reaching_0_95": smallest,
        "n_regions_scanned": len(rows),
        "n_regions_reaching_0_95": len(reach),
    }


def wq(v, w, qs):
    o = np.argsort(v)
    cw = np.cumsum(w[o])
    cw = cw / cw[-1]
    vs = v[o]
    return np.array([vs[min(np.searchsorted(cw, q), len(vs) - 1)] for q in qs])


def systematic(w, rng):
    n = len(w)
    u = (rng.random() + np.arange(n)) / n
    c = np.cumsum(w)
    c[-1] = 1.0
    return np.searchsorted(c, u)


def obs_loglik(Y, S, x):
    """Log-likelihood up to a constant of the aggregated count Y over S stores, NB with size S*kappa."""
    lk = np.logaddexp(LOG_K, x)
    return S * KAPPA * (LOG_K - lk) + Y * (x - lk)


def simulate_pilot(lam_nat, S, sig_store, rng):
    """Truth: national demand at the start lam_nat, pilot-store offset e ~ N(0, sig_store^2 / S), and a
    weekly random walk with noise SIGMA_ETA (realised national path returned for calibration)."""
    e = (sig_store / math.sqrt(S)) * rng.standard_normal()
    x = math.log(lam_nat) + e
    Y = np.zeros(T)
    path = np.zeros(T)
    for t in range(T):
        x = x + SIGMA_ETA * rng.standard_normal()
        lam_pilot = math.exp(x)
        Y[t] = rng.negative_binomial(S * KAPPA, KAPPA / (KAPPA + lam_pilot))
        path[t] = math.exp(x - e)
    return Y, path


def make_rb(ab, names=FAN_VARS, n_grid=90):
    """Exact conditional P(NPV > 0 | annual cubes V) for each linear variant, from the prior draws (pilot world:
    the static inputs are independent of the demand read). Returned as (log V grid, probability, mean alpha,
    mean beta), so that E[NPV | V] = mean alpha * V - mean beta."""
    Vg = np.exp(np.linspace(math.log(10_000.0), math.log(1_500_000.0), n_grid))
    rb = {}
    for nm in names:
        al, be = ab[nm]
        p = np.array([float(np.mean(al * v - be > 0)) for v in Vg])
        p = np.maximum.accumulate(p)    # P(NPV > 0 | V) is non-decreasing in V; removes grid noise
        rb[nm] = (np.log(Vg), p, float(al.mean()), float(be.mean()))
    return rb


def run_filter(Y, S, N, rng, m_ell, s_ell, sig_store, static_fn=None, want_q=False, thrs=None, rb=None):
    """Bootstrap particle filter with resampling at ESS < N/2 and Liu-West drift updating.

    State: x_t (pilot-level log demand), x0 (its initial value), e (pilot offset given x0, exact conditional),
    mu (weekly drift). The national demand is exp(x_t - e). Static inputs (static_fn, returning a dict of
    (alpha, beta) pairs with NPV = alpha * V - beta) are redrawn from their prior after each resampling, which
    is exact because they do not enter the counts. Returns P(demand > threshold | data) for every threshold
    and the posterior mean demand by week. With rb (see make_rb) it also returns P(NPV > 0 | data) and the
    posterior expected NPV by week, mapped through the exact conditional P(NPV > 0 | V); this uses no random
    numbers, so adding it changes no other result.
    """
    th = THRS if thrs is None else np.asarray(thrs, dtype=float)
    sig_e = sig_store / math.sqrt(S)
    tot = s_ell * s_ell + sig_e * sig_e
    x0 = m_ell + math.sqrt(tot) * rng.standard_normal(N)
    a = sig_e * sig_e * (x0 - m_ell) / tot
    b = s_ell * s_ell * sig_e * sig_e / tot
    e = a + math.sqrt(b) * rng.standard_normal(N)
    x = x0.copy()
    mu = MU_SD * rng.standard_normal(N)
    logw = np.zeros(N)
    st = static_fn(N, rng) if static_fn is not None else None
    p_out = np.zeros((T, len(th)))
    mean_lam = np.zeros(T)
    lam_q = np.zeros((T, 3)) if (want_q or static_fn is not None) else None
    npv_q = {k: np.zeros((T, 3)) for k in st} if st is not None else None
    p_npv = {k: np.zeros(T) for k in st} if st is not None else None
    resamples = 0
    p_rb = {k: np.zeros(T) for k in rb} if rb is not None else None
    e_npv = {k: np.zeros(T) for k in rb} if rb is not None else None
    for t in range(T):
        x = x + mu + SIGMA_ETA * rng.standard_normal(N)
        logw = logw + obs_loglik(Y[t], S, x)
        w = np.exp(logw - logw.max())
        w = w / w.sum()
        lam = np.exp(x - e)
        mean_lam[t] = float(np.sum(w * lam))
        order = np.argsort(lam)
        cw = np.cumsum(w[order])
        pos = np.searchsorted(lam[order], th, side="right")
        p_out[t] = 1.0 - np.where(pos > 0, cw[np.maximum(pos - 1, 0)], 0.0)
        if lam_q is not None:
            lam_q[t] = wq(lam, w, QS3)
        if rb is not None:
            lv = np.log(WEEKS_PER_YEAR * N_EFF * lam)
            for kname, (lg, pg, am, bm) in rb.items():
                p_rb[kname][t] = float(np.sum(w * np.interp(lv, lg, pg)))
                e_npv[kname][t] = am * WEEKS_PER_YEAR * N_EFF * mean_lam[t] - bm
        if st is not None:
            V = WEEKS_PER_YEAR * N_EFF * lam
            for kname, (al, be) in st.items():
                npv = al * V - be
                p_npv[kname][t] = w[npv > 0].sum()
                npv_q[kname][t] = wq(npv, w, QS3)
        ess = 1.0 / np.sum(w * w)
        if ess < N / 2.0:
            idx = systematic(w, rng)
            resamples += 1
            x = x[idx]
            x0 = x0[idx]
            e = e[idx]
            mu = mu[idx]
            mm = mu.mean()
            vv = mu.var()
            mu = A_LW * mu + (1.0 - A_LW) * mm + H_LW * math.sqrt(vv) * rng.standard_normal(N)
            if static_fn is not None:
                st = static_fn(N, rng)
            logw = np.zeros(N)
        else:
            logw = np.log(np.maximum(w, 1e-300))
    return {"p": p_out, "mean_lam": mean_lam, "lam_q": lam_q, "npv_q": npv_q, "p_npv": p_npv,
            "resamples": resamples, "p_rb": p_rb, "e_npv": e_npv}


def static_ab(n, rng, names=FAN_VARS):
    raw = prior_draws(n, rng)
    out = {}
    for nm in names:
        rec, ex, mode = LIN_VARIANTS[nm]
        out[nm] = alpha_beta(derive(raw, rec, ex), mode)
    return out


def oc_grid(sig_store, R, rng, lam_list, s_list, m_ell, s_ell):
    res = {}
    for S in s_list:
        for lam in lam_list:
            P = np.zeros((R, T, len(THRS)))
            M = np.zeros((R, T))
            for r in range(R):
                Y, _ = simulate_pilot(lam, S, sig_store, rng)
                o = run_filter(Y, S, N_PF, rng, m_ell, s_ell, sig_store)
                P[r] = o["p"]
                M[r] = o["mean_lam"]
            res[(S, lam)] = (P, M)
    return res


def pair_power(res, S, lo_t, hi_t, weeks=SEP_WEEKS):
    j = TI_G[round((lo_t + hi_t) / 2.0, 2)]
    P_lo = res[(S, lo_t)][0]
    P_hi = res[(S, hi_t)][0]
    out = []
    for w in weeks:
        t = WEEK_IDX[w]
        below = np.mean(P_lo[:, t, j] <= POST_LO)
        above = np.mean(P_hi[:, t, j] >= POST_HI)
        out.append(float(min(below, above)))
    return out


def pair_power_se(res, S, lo_t, hi_t, week=13):
    """Binomial Monte Carlo standard error of the separation power (the binding side) at one week."""
    j = TI_G[round((lo_t + hi_t) / 2.0, 2)]
    t = WEEK_IDX[week]
    P_lo = res[(S, lo_t)][0]
    P_hi = res[(S, hi_t)][0]
    p = float(min(np.mean(P_lo[:, t, j] <= POST_LO), np.mean(P_hi[:, t, j] >= POST_HI)))
    return math.sqrt(max(p * (1.0 - p), 1e-12) / len(P_lo))


def summarise_paths(M):
    """Mean, standard error of the mean and 10th, 50th, 90th percentile across pilots, for each week."""
    M = np.asarray(M, dtype=float)
    return {"mean": M.mean(axis=0).tolist(),
            "se_mean": (M.std(axis=0, ddof=1) / math.sqrt(M.shape[0])).tolist(),
            "p10": np.percentile(M, 10, axis=0).tolist(),
            "p50": np.percentile(M, 50, axis=0).tolist(),
            "p90": np.percentile(M, 90, axis=0).tolist()}


def pilot_evolution(rng, rb, S, R, truths, sep_pairs=((1.5, 3.0), (3.0, 4.5))):
    """Week-by-week posterior of R simulated S-store pilots per truth (N_PF particles each): P(NPV > 0) and the
    posterior expected NPV for variants A, B and D, P(demand >= 3), the posterior mean demand and the log width of
    the 90 percent demand band. The truth is the start-of-pilot level, as elsewhere.

    It also scores the separation of each pair of truths two ways: against the start-of-pilot label (as in the
    operating characteristics) and against the realised national level at the read week (a pilot is confidently
    right if P(demand > midpoint | data) is at least 0.9 when its level at that week is above the midpoint, and
    at most 0.1 when below). The difference is the effect of the scoring convention."""
    mids = sorted({round((lo + hi) / 2.0, 2) for lo, hi in sep_pairs})
    thr = [RULE_THR] + mids
    out = {}
    keep = {}
    for lam in truths:
        Pn = {nm: np.zeros((R, T)) for nm in rb}
        En = {nm: np.zeros((R, T)) for nm in rb}
        P3 = np.zeros((R, T))
        Ml = np.zeros((R, T))
        Wd = np.zeros((R, T))
        Pm = {m: np.zeros((R, T)) for m in mids}
        Lv = np.zeros((R, T))
        for r in range(R):
            Y, path = simulate_pilot(lam, S, STORE_SD, rng)
            o = run_filter(Y, S, N_PF, rng, M_ELL, S_ELL, STORE_SD, want_q=True, thrs=thr, rb=rb)
            for nm in rb:
                Pn[nm][r] = o["p_rb"][nm]
                En[nm][r] = o["e_npv"][nm]
            P3[r] = o["p"][:, 0]
            for j, m in enumerate(mids):
                Pm[m][r] = o["p"][:, 1 + j]
            Ml[r] = o["mean_lam"]
            Wd[r] = np.log(o["lam_q"][:, 2] / o["lam_q"][:, 0])
            Lv[r] = path
        keep[lam] = (Pm, Lv)
        cell = {"pilots": R, "stores": S,
                "P_demand_ge_3": summarise_paths(P3),
                "posterior_mean_demand": summarise_paths(Ml),
                "log_width_90pct_demand_band": summarise_paths(Wd),
                "realised_level_sd_of_log_over_pilots_by_week": np.std(np.log(Lv), axis=0, ddof=1).tolist()}
        for nm in rb:
            cell[nm] = {"P_NPV_gt_0": summarise_paths(Pn[nm]),
                        "expected_NPV_THB": summarise_paths(En[nm]),
                        "share_of_pilots_P_NPV_gt_0_ge_0_95_by_week": (Pn[nm] >= ALPHA_H0).mean(axis=0).tolist(),
                        "share_of_pilots_P_NPV_gt_0_ge_0_50_by_week": (Pn[nm] >= 0.5).mean(axis=0).tolist(),
                        "share_of_pilots_P_NPV_gt_0_le_0_05_by_week": (Pn[nm] <= 0.05).mean(axis=0).tolist()}
        out[str(lam)] = cell
    sep = {}
    for lo, hi in sep_pairs:
        m = round((lo + hi) / 2.0, 2)
        sides = {}
        for lam, hi_side in ((lo, False), (hi, True)):
            Pm, Lv = keep[lam]
            conf_start = (Pm[m] >= POST_HI) if hi_side else (Pm[m] <= POST_LO)
            conf_level = np.where(Lv > m, Pm[m] >= POST_HI, Pm[m] <= POST_LO)
            sides[lam] = (conf_start.mean(axis=0), conf_level.mean(axis=0))
        sep[f"{lo}_vs_{hi}"] = {
            "midpoint": m,
            "power_scored_on_start_label_by_week": np.minimum(sides[lo][0], sides[hi][0]).tolist(),
            "power_scored_on_level_at_read_week_by_week": np.minimum(sides[lo][1], sides[hi][1]).tolist(),
            "MC_SE_approx": math.sqrt(0.8 * 0.2 / R)}
    out["separation_by_scoring_convention"] = sep
    return out


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (int, np.integer)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        v = float(o)
        return None if (math.isnan(v) or math.isinf(v)) else v
    return o


M_ELL = 0.0   # national log-demand prior mean, set in main() from the prior draws
S_ELL = 1.0   # national log-demand prior sd, set in main()


def interp_crossing(xs, ys, level):
    """x at which the (cumulative-max) curve first reaches level, linear interpolation; None if never."""
    ys = np.maximum.accumulate(np.asarray(ys, dtype=float))
    xs = np.asarray(xs, dtype=float)
    if ys[-1] < level or ys[0] > level:
        return None
    return float(np.interp(level, ys, xs))


def conditional_gline(V, alpha, beta, nb=40):
    """E[NPV | V] under the joint prior (price and volume correlation kept): binned conditional means of alpha and
    beta, interpolated. Returns a function of V."""
    edges = np.quantile(V, np.linspace(0.0, 1.0, nb + 1))
    idx = np.clip(np.searchsorted(edges, V, side="right") - 1, 0, nb - 1)
    cnt = np.bincount(idx, minlength=nb).astype(float)
    vb = np.bincount(idx, weights=V, minlength=nb) / cnt
    ab = np.bincount(idx, weights=alpha, minlength=nb) / cnt
    bb = np.bincount(idx, weights=beta, minlength=nb) / cnt

    def g(v):
        v = np.asarray(v, dtype=float)
        return np.interp(v, vb, ab) * v - np.interp(v, vb, bb)

    return g


def voi_experiment(n_eff, n_truth, rng, V_pop, ab_means, vstar, ab_pop, S, with_plain=True, delay_factor=1.0):
    """Value of the pilot, like for like, in the pilot world (price and volume independent given V).

    Truths: V_i drawn from the marginal prior of steady volume; lam_i = V_i / (52 n_eff). A pilot of S stores is
    simulated and filtered (N_PF particles). Rules: R1_8 and R1_13 (one read, P(demand >= 3) >= 0.5), R2 (both
    reads), and the Bayes rules B8_v and B13_v (scale iff the posterior mean demand is at or above the expected-NPV
    break-even demand of variant v). Payoffs: decision times E[NPV | V_i] (exact, Rao-Blackwellised over the static
    inputs) and, for reference, decision times a realised NPV draw (the first-pass estimator)."""
    lam_pop = V_pop / (WEEKS_PER_YEAR * n_eff)
    m_ell = float(np.mean(np.log(lam_pop)))
    s_ell = float(np.std(np.log(lam_pop)))
    idx = rng.integers(0, len(V_pop), n_truth)
    Vi = V_pop[idx]
    lam_i = Vi / (WEEKS_PER_YEAR * n_eff)
    stat = static_ab(n_truth, rng) if with_plain else None
    names = list(ab_means.keys())
    thr = {v: vstar[v] / (WEEKS_PER_YEAR * n_eff) for v in names}
    d = {"R1_8": np.zeros(n_truth, bool), "R1_13": np.zeros(n_truth, bool)}
    for v in names:
        d["B8_" + v] = np.zeros(n_truth, bool)
        d["B13_" + v] = np.zeros(n_truth, bool)
    t3 = np.array([RULE_THR])
    lam8 = np.zeros(n_truth)       # realised national level at week 8 and week 13 (for the alternative scorings)
    lam13 = np.zeros(n_truth)
    for i in range(n_truth):
        Y, path_i = simulate_pilot(float(lam_i[i]), S, STORE_SD, rng)
        lam8[i] = path_i[WEEK_IDX[8]]
        lam13[i] = path_i[WEEK_IDX[13]]
        o = run_filter(Y, S, N_PF, rng, m_ell, s_ell, STORE_SD, thrs=t3)
        d["R1_8"][i] = o["p"][WEEK_IDX[8], 0] >= RULE_P
        d["R1_13"][i] = o["p"][WEEK_IDX[13], 0] >= RULE_P
        for v in names:
            d["B8_" + v][i] = o["mean_lam"][WEEK_IDX[8]] >= thr[v]
            d["B13_" + v][i] = o["mean_lam"][WEEK_IDX[13]] >= thr[v]
    d["R2"] = d["R1_8"] & d["R1_13"]
    out = {"stores": S, "truths": n_truth, "N_EFF": n_eff, "break_even_demand_units_by_variant": thr,
           "share_scale": {k: float(v.mean()) for k, v in d.items()}}
    for v in names:
        a_v, b_v = ab_means[v]
        g_i = a_v * Vi - b_v
        g_pop = a_v * V_pop - b_v
        e_prior = float(g_pop.mean())
        no_pilot_scale = e_prior > 0
        nopilot = g_i if no_pilot_scale else np.zeros(n_truth)
        pay = {"no_pilot": nopilot}
        for k, dec in d.items():
            pay[k] = dec * g_i
        pay["perfect_information_on_demand"] = np.maximum(g_i, 0.0)
        vv = {"E_NPV_prior_THB": e_prior, "no_pilot_decision": "scale" if no_pilot_scale else "do not scale",
              "EVPI_on_demand_THB_population": float(np.maximum(g_pop, 0.0).mean()),
              "value_THB": {}, "paired_diff_THB": {}}
        for k, p in pay.items():
            vv["value_THB"][k] = {"mean": float(p.mean()), "se": float(p.std(ddof=1) / math.sqrt(n_truth))}
        for k in ("R1_8", "R1_13", "R2", "B8_" + v, "B13_" + v):
            df = pay[k] - pay["no_pilot"]
            vv["paired_diff_THB"][k + "_minus_no_pilot"] = {"mean": float(df.mean()),
                                                           "se": float(df.std(ddof=1) / math.sqrt(n_truth))}
        for k1, k0 in (("R1_13", "R1_8"), ("R2", "R1_13"), ("R2", "R1_8"), ("B13_" + v, "B8_" + v)):
            df = pay[k1] - pay[k0]
            vv["paired_diff_THB"][k1 + "_minus_" + k0] = {"mean": float(df.mean()),
                                                         "se": float(df.std(ddof=1) / math.sqrt(n_truth))}
        # Alternative scoring conventions. The default above scores every rule on the start-of-pilot level (the
        # truth), although the filter tracks the level at the read week. T scores a rule on the national level at
        # its own decision week (no pilot: the start level). C scores every rule on the common week-13 level.
        g8 = a_v * (WEEKS_PER_YEAR * n_eff * lam8) - b_v
        g13 = a_v * (WEEKS_PER_YEAR * n_eff * lam13) - b_v
        gdec = {"R1_8": g8, "B8_" + v: g8, "R1_13": g13, "R2": g13, "B13_" + v: g13}
        payT = {k: d[k] * g for k, g in gdec.items()}
        payT["no_pilot"] = nopilot
        payC = {k: d[k] * g13 for k in gdec}
        payC["no_pilot"] = g13 if no_pilot_scale else np.zeros(n_truth)
        payC["perfect_information_on_demand"] = np.maximum(g13, 0.0)
        for pp in (payT, payC):          # acting five weeks later costs the delay discount (prior mean rate)
            pp["B13_" + v + "_delayed"] = pp["B13_" + v] * delay_factor
        for label, pp in (("decision_time_level", payT), ("common_week13_level", payC)):
            blk = {"value_THB": {k: {"mean": float(p.mean()), "se": float(p.std(ddof=1) / math.sqrt(n_truth))}
                                 for k, p in pp.items()},
                   "paired_diff_THB": {}}
            for k1, k0 in (("B13_" + v, "B8_" + v), ("B13_" + v + "_delayed", "B8_" + v), ("R1_13", "R1_8"),
                           ("R2", "R1_13"), ("R2", "R1_8"),
                           ("B8_" + v, "no_pilot"), ("B13_" + v, "no_pilot"), ("R2", "no_pilot")):
                df = pp[k1] - pp[k0]
                blk["paired_diff_THB"][k1 + "_minus_" + k0] = {"mean": float(df.mean()),
                                                              "se": float(df.std(ddof=1) / math.sqrt(n_truth))}
            vv[label] = blk
        if with_plain and v in stat:
            al, be = stat[v]
            npv_i = al * Vi - be
            plain = {k: dec * npv_i for k, dec in d.items()}
            vv["first_pass_estimator_realised_NPV_payoff_THB"] = {
                k: {"mean": float(p.mean()), "se": float(p.std(ddof=1) / math.sqrt(n_truth))} for k, p in plain.items()}
            df = plain["R2"] - plain["R1_8"]
            vv["first_pass_estimator_R2_minus_R1_8_THB"] = {"mean": float(df.mean()),
                                                            "se": float(df.std(ddof=1) / math.sqrt(n_truth))}
            df = plain["R1_13"] - plain["R1_8"]
            vv["first_pass_estimator_R1_13_minus_R1_8_THB"] = {"mean": float(df.mean()),
                                                               "se": float(df.std(ddof=1) / math.sqrt(n_truth))}
        out[v] = vv
    return out


def main():
    global M_ELL, S_ELL, SIGMA_ETA, THRS, TI_N, CHAIN_RATIO
    t0 = time.time()
    rng = np.random.default_rng(SEED)

    va = json.load(open(VA_JSON, encoding="utf-8"))
    can = json.load(open(CAN_JSON, encoding="utf-8"))
    CHAIN_RATIO = float(can["aluminium"]["net_after_excise_thb_per_can"]) / float(can["aluminium"]["listing_price_basis_thb_per_can"])
    assert abs(CHAIN_RATIO - float(va["contribution_bases"]["chain_ratio_can_net_to_listing"])) < 1e-6
    c_after_75 = 15.0 * CHAIN_RATIO - 4.09          # planning price 15 times the can chain ratio, less cube cost 4.09
    assert abs(c_after_75 - float(va["contribution_bases"]["after_excise_thb"])) < 1e-4
    npv_75_target = float(va["base_case"]["after_excise"]["0.0"]["npv_after_tax_at_base_rate_thb"])

    # ------------------------------------------------------------------ A. prior predictive
    raw = prior_draws(N_PRIOR, rng)
    spec = {
        "A_record05_structure": dict(rec=True, ex=False, mode="none"),
        "B_headline_full_prior": dict(rec=False, ex=False, mode="none"),
        "C_tax_no_relief_before_excise": dict(rec=False, ex=False, mode="no_relief"),
        "A2_record05_structure_after_excise": dict(rec=True, ex=True, mode="none"),
        "B2_full_prior_after_excise_pretax": dict(rec=False, ex=True, mode="none"),
        "D_record75_lead_basis": dict(rec=False, ex=True, mode="relief_shield"),
        "D_cf_standalone_carry_forward": dict(rec=False, ex=True, mode="carry_forward"),
        "B_wide_repeat_prior": dict(rec=False, ex=False, mode="none", wide=True),
        "D_wide_repeat_prior": dict(rec=False, ex=True, mode="relief_shield", wide=True),
        "B_no_price_volume_correlation": dict(rec=False, ex=False, mode="none", rho0=True),
    }
    npvs = {}
    derived = {}
    summ = {}
    for nm, sp in spec.items():
        d = derive(raw, sp["rec"], sp["ex"], sp.get("wide", False), sp.get("rho0", False))
        cf = cash_flows(d["c"], d["k"], d["cc"], d["V"], d["F"], d["ramp1"], sp["mode"])
        npv = npv_of(cf, d["F"], d["rd"])
        irr = irr_vec(d["F"], cf)
        pb = payback_vec(d["F"], cf)
        summ[nm] = summarise_npv(npv, irr, pb)
        summ[nm]["definition"] = sp
        npvs[nm] = npv
        if nm in ("A_record05_structure", "B_headline_full_prior", "D_record75_lead_basis"):
            derived[nm] = d
        del cf, irr, pb
        gc.collect()
        print(f"[{time.time()-t0:.1f}s] prior variant {nm}: P(NPV>0) = {summ[nm]['P_NPV_gt_0']:.3f}")
    npvA = npvs["A_record05_structure"]
    npvB = npvs["B_headline_full_prior"]
    npvD = npvs["D_record75_lead_basis"]
    dA = derived["A_record05_structure"]
    dB = derived["B_headline_full_prior"]
    dD = derived["D_record75_lead_basis"]

    # alpha and beta of the linear variants (NPV = alpha * V - beta), checked against the cash-flow code
    ab = {}
    for nm, (rec, ex, mode) in LIN_VARIANTS.items():
        d = derive(raw, rec, ex)
        al, be = alpha_beta(d, mode)
        ab[nm] = (al, be)
        chk = npv_of(cash_flows(d["c"], d["k"], d["cc"], d["V"], d["F"], d["ramp1"], mode), d["F"], d["rd"])
        assert np.allclose(al * d["V"] - be, chk, rtol=1e-9, atol=1e-3), nm
    name_map = {"A": "A_record05_structure", "B": "B_headline_full_prior", "A2": "A2_record05_structure_after_excise",
                "B2": "B2_full_prior_after_excise_pretax", "D": "D_record75_lead_basis"}
    for nm, full in name_map.items():
        assert np.allclose(ab[nm][0] * (derive(raw, *LIN_VARIANTS[nm][:2])["V"]) - ab[nm][1], npvs[full], atol=1e-3)

    # Deterministic reconciliation with record 05 and record 75
    pv = json.load(open(PV_JSON, encoding="utf-8"))
    one = lambda x: np.array([float(x)])  # noqa: E731
    recon_npv = float(npv_of(cash_flows(one(4.91), one(0), one(0), one(200_000.0), one(500_000.0), one(0.5), "none"),
                             one(500_000.0), one(0.10))[0])
    recon_D = float(npv_of(cash_flows(one(c_after_75), one(0), one(0), one(200_000.0), one(500_000.0), one(0.5),
                                      "relief_shield"), one(500_000.0), one(0.10))[0])
    record_npv = pv["summary"]["base_case"]["npv_at_fixed_500000_thb"]
    record_be = pv["break_even_by_fixed_cost"][1]["npv_zero_cubes_per_year"]["0.1"]
    assert abs(recon_npv - record_npv) < 1.0, (recon_npv, record_npv)
    assert abs(recon_D - npv_75_target) < 1.0, (recon_D, npv_75_target)

    # Point-value (input-median) NPV by demand: record 05 basis and record 75 lead basis
    def det_npv(c, lam, mode):
        return float(npv_of(cash_flows(one(c), one(0), one(0), one(WEEKS_PER_YEAR * N_EFF * lam), one(500_000.0),
                                       one(0.5), mode), one(500_000.0), one(0.10))[0])

    point_npv = {"before_excise_pretax_c_4_91": {str(l): det_npv(4.91, l, "none") for l in LAM_GRID},
                 "after_excise_aftertax_c_3_9444": {str(l): det_npv(c_after_75, l, "relief_shield") for l in LAM_GRID}}
    v_point_D = brentq(lambda v: float(npv_of(cash_flows(one(c_after_75), one(0), one(0), one(v), one(500_000.0),
                                                         one(0.5), "relief_shield"), one(500_000.0), one(0.10))[0]),
                       1e4, 2e6)

    # Prior quantiles of the inputs (achieved, from the draws)
    prior_check = {}
    for key in list(SENS_NAMES.keys()) + ["repeat_wide"]:
        x = raw[key]
        prior_check[key] = {"p05": float(np.percentile(x, 5)), "median": float(np.median(x)),
                            "p95": float(np.percentile(x, 95)), "mean": float(x.mean())}
    prior_check["repeat_wide"]["P_below_0_15"] = float(np.mean(raw["repeat_wide"] < 0.15))
    prior_check["repeat_triangular"] = {"P_below_0_15": 0.0, "mean": float(raw["repeat_rate"].mean())}
    for nm, d in (("variant_B", dB), ("variant_A", dA), ("variant_D", dD)):
        prior_check["cost_per_cube_" + nm] = {"p05": float(np.percentile(d["cost"], 5)),
                                              "median": float(np.median(d["cost"])),
                                              "p95": float(np.percentile(d["cost"], 95))}
        prior_check["contribution_" + nm] = {"p05": float(np.percentile(d["c"], 5)),
                                             "median": float(np.median(d["c"])),
                                             "p95": float(np.percentile(d["c"], 95))}
    prior_check["steady_cubes_per_year"] = {"p05": float(np.percentile(dB["V"], 5)),
                                            "median": float(np.median(dB["V"])),
                                            "p95": float(np.percentile(dB["V"], 95)), "mean": float(dB["V"].mean())}
    prior_check["spearman_shelf_vs_first_purchase"] = float(
        stats.spearmanr(raw["shelf_price"], raw["first_purchase_cubes"]).correlation)
    prior_check["beta_cannibal_params"] = [A_K, B_K]
    prior_check["beta_wide_repeat_params"] = [A_REPW, B_REPW]

    # Sensitivity of the NPV: variant B (pre-registered headline) and variant D (lead basis)
    sens_B = sensitivity(raw, npvB)
    sens_D = sensitivity(raw, npvD)
    joint = {"B": joint_narrowing(npvB, raw, dB["V"], True), "D": joint_narrowing(npvD, raw, dD["V"], True),
             "A": joint_narrowing(npvA, raw, dA["V"], False)}
    print(f"[{time.time()-t0:.1f}s] sensitivity and joint narrowing done")
    p_cannib_review = float(np.mean(raw["cannibal_share"] >= 0.5))
    p_cannib_review_analytic = float(stats.beta.sf(0.5, A_K, B_K))
    k75 = float(va["break_points"]["after_excise"]["npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct"]["raw"])
    p_cannib_ge_k75 = float(np.mean(raw["cannibal_share"] >= k75))
    p_contrib_below = float(np.mean(dB["c"] < 3.51))
    p_contrib_below_A = float(np.mean(dA["c"] < 3.51))
    # The 3.51 floor is before excise (record 75 section 5.8 gives 2.54 after excise); also report on the after-excise basis
    p_contrib_below_D = float(np.mean(dD["c"] < 2.54))
    npv_lin = {"A": npvA, "B": npvB, "D": npvD}
    band = (raw["shelf_price"] >= 14.5) & (raw["shelf_price"] <= 15.5)     # shelf price pinned near the planning price
    ab_band = {nm: (ab[nm][0][band], ab[nm][1][band]) for nm in ("A", "B", "D")}
    band_share = float(band.mean())
    V_pop = dB["V"].copy()
    lam_nat_prior = V_pop / (WEEKS_PER_YEAR * N_EFF)
    # discount factor for launching five weeks later (not priced in the value of waiting; reported for scale)
    delay_factor_5wk = float(np.mean((1.0 + raw["discount_rate"]) ** (-5.0 / WEEKS_PER_YEAR)))
    del raw, derived, dA, dB, dD, npvs
    gc.collect()

    # ------------------------------------------------------------------ B0. fixed-demand analysis
    ab_means = {nm: (float(ab[nm][0].mean()), float(ab[nm][1].mean())) for nm in LIN_VARIANTS}
    vstar = {nm: ab_means[nm][1] / ab_means[nm][0] for nm in LIN_VARIANTS}   # cubes a year, expected-NPV zero
    dstar = {nm: vstar[nm] / (WEEKS_PER_YEAR * N_EFF) for nm in LIN_VARIANTS}
    # median-NPV (P = 0.5) break-even volume by variant
    v_med = {}
    for nm in ("A", "B", "D"):
        al, be = ab[nm]
        v_med[nm] = float(brentq(lambda v: np.mean(al * v - be > 0) - 0.5, 20_000.0, 2_000_000.0))
    neff_table = {nm: {str(n): vstar[nm] / (WEEKS_PER_YEAR * n) for n in N_EFF_SENS} for nm in LIN_VARIANTS}
    neff_cross = {nm: vstar[nm] / (WEEKS_PER_YEAR * RULE_THR) for nm in LIN_VARIANTS}   # N_EFF at which d* = 3
    # copula-retained conditional expectation (sensitivity)
    g_corr = {nm: conditional_gline(V_pop, ab[nm][0], ab[nm][1]) for nm in ("A", "B", "D")}
    vstar_corr = {}
    for nm in ("A", "B", "D"):
        try:
            vstar_corr[nm] = float(brentq(lambda v: float(g_corr[nm](v)), 60_000.0, 900_000.0))
        except ValueError:
            vstar_corr[nm] = None
    demand_list = sorted(set(list(LAM_GRID) + [round(LAM_BE, 4), 2.2]))
    fixed_demand = {}
    for nm in ("A", "B", "D", "A2", "B2"):
        al, be = ab[nm]
        fixed_demand[nm] = {}
        for lam in demand_list:
            V = WEEKS_PER_YEAR * N_EFF * lam
            y = al * V - be
            p = float(np.mean(y > 0))
            fixed_demand[nm][str(lam)] = {"cubes_a_year": V, "E_NPV_THB": float(y.mean()),
                                          "MC_SE_E_NPV_THB": float(y.std(ddof=1) / math.sqrt(len(y))),
                                          "P_NPV_gt_0": p, "MC_SE_P": math.sqrt(p * (1 - p) / len(y)),
                                          "p05_THB": float(np.percentile(y, 5)), "p95_THB": float(np.percentile(y, 95))}
    price_pinned = {}
    for nm in ("A", "B", "D"):
        al_b, be_b = ab_band[nm]
        price_pinned[nm] = {}
        for lam in (3.0, 4.5, 6.0):
            y = al_b * (WEEKS_PER_YEAR * N_EFF * lam) - be_b
            price_pinned[nm][str(lam)] = {"E_NPV_THB": float(y.mean()), "P_NPV_gt_0": float(np.mean(y > 0)), "n_draws": int(len(y))}
        vb = ab_means_band = float(be_b.mean() / al_b.mean())
        price_pinned[nm]["expected_NPV_break_even_demand_units"] = vb / (WEEKS_PER_YEAR * N_EFF)
    # oracle rules (perfect knowledge of V, scale iff V above the line), joint prior draws (copula kept)
    Vj = V_pop
    lines = {"3_units_line": WEEKS_PER_YEAR * N_EFF * RULE_THR, "point_value_break_even_record05": V_STAR,
             "expected_NPV_break_even_A": vstar["A"], "expected_NPV_break_even_B": vstar["B"],
             "expected_NPV_break_even_D": vstar["D"]}
    oracle = {}
    for nm in ("A", "B", "D"):
        y = npv_lin[nm]
        oracle[nm] = {"scale_always": {"mean": float(y.mean()), "se": float(y.std(ddof=1) / math.sqrt(len(y)))}}
        for ln, vl in lines.items():
            pay = np.where(Vj >= vl, y, 0.0)
            oracle[nm][ln] = {"line_cubes": vl, "mean": float(pay.mean()),
                              "se": float(pay.std(ddof=1) / math.sqrt(len(pay))), "share_scaled": float((Vj >= vl).mean())}
    print(f"[{time.time()-t0:.1f}s] fixed-demand tables done; expected-NPV break-even demand A {dstar['A']:.2f}, "
          f"B {dstar['B']:.2f}, D {dstar['D']:.2f}")

    # ------------------------------------------------------------------ B. pilot model setup
    M_ELL = float(np.mean(np.log(lam_nat_prior)))
    S_ELL = float(np.std(np.log(lam_nat_prior)))
    lam_prior_q = np.percentile(lam_nat_prior, [5, 50, 95])
    named = {"point_BE": LAM_BE, "dstar_A": dstar["A"], "dstar_B": dstar["B"], "dstar_D": dstar["D"]}
    THRS = np.array(BASE_THR + list(named.values()), dtype=float)
    TI_N = {k: len(BASE_THR) + i for i, k in enumerate(named)}
    TI3 = TI_G[3.0]
    print(f"[{time.time()-t0:.1f}s] pilot setup. lam prior median {np.median(lam_nat_prior):.3f}, "
          f"log-sd {S_ELL:.3f}, point BE lambda {LAM_BE:.3f}")

    # Exact conditional P(NPV > 0 | volume) for the week-by-week mapping (no random numbers)
    rb = make_rb(ab)

    # Fan: representative pilot per truth, N_FAN particles, S_FAN stores
    fan = {}
    fan_rng = np.random.default_rng(SEED + 11)
    for lam in TRUTHS:
        Y, path = simulate_pilot(lam, S_FAN, STORE_SD, fan_rng)
        big = run_filter(Y, S_FAN, N_FAN, fan_rng, M_ELL, S_ELL, STORE_SD, static_fn=static_ab, want_q=True, rb=rb)
        small = run_filter(Y, S_FAN, N_PF, fan_rng, M_ELL, S_ELL, STORE_SD, want_q=True)
        diff = float(np.max(np.abs(big["p"][:, TI3] - small["p"][:, TI3])))
        rb_diff = {nm: float(np.max(np.abs(big["p_rb"][nm] - big["p_npv"][nm]))) for nm in FAN_VARS}
        fan[str(lam)] = {"Y": Y.tolist(), "path": path.tolist(), "big": big, "small": small,
                         "particle_check_max_abs_diff_P_ge_3": diff,
                         "rb_vs_particle_mapping_max_abs_diff_P_NPV_gt_0": rb_diff}
        print(f"[{time.time()-t0:.1f}s] fan truth {lam}: week-13 P(NPV>0) B {big['p_npv']['B'][-1]:.3f}, "
              f"D {big['p_npv']['D'][-1]:.3f}; particle check {diff:.4f}; resamples {big['resamples']}; "
              f"RB check {max(rb_diff.values()):.4f}")

    # Week-by-week P(NPV > 0) over many simulated pilots per truth (own random stream)
    evo_rng = np.random.default_rng(SEED + 71)
    evolution = pilot_evolution(evo_rng, rb, S_FAN, R_EVO, TRUTHS)
    evolution_40 = pilot_evolution(np.random.default_rng(SEED + 79), rb, 40, R_EVO, TRUTHS)
    print(f"[{time.time()-t0:.1f}s] pilot evolution done ({R_EVO} pilots per truth)")

    # Calibration: realised national demand at week 13 inside the 90% posterior band (S_FAN)
    cal, cal_n = {}, {}
    cal_rng = np.random.default_rng(SEED + 23)
    for lam in TRUTHS:
        inside = 0
        for _ in range(R_CAL):
            Y, path = simulate_pilot(lam, S_FAN, STORE_SD, cal_rng)
            out_f = run_filter(Y, S_FAN, N_PF, cal_rng, M_ELL, S_ELL, STORE_SD, want_q=True, thrs=[3.0])
            lo, hi = out_f["lam_q"][-1, 0], out_f["lam_q"][-1, 2]
            inside += int(lo <= path[-1] <= hi)
        cal[str(lam)] = inside / R_CAL
        inside = 0
        for _ in range(R_CAL_BIG):
            Y, path = simulate_pilot(lam, S_FAN, STORE_SD, cal_rng)
            out_f = run_filter(Y, S_FAN, N_PF_BIG, cal_rng, M_ELL, S_ELL, STORE_SD, want_q=True, thrs=[3.0])
            lo, hi = out_f["lam_q"][-1, 0], out_f["lam_q"][-1, 2]
            inside += int(lo <= path[-1] <= hi)
        cal_n[str(lam)] = inside / R_CAL_BIG
    print(f"[{time.time()-t0:.1f}s] calibration coverage at week 13: {cal}; big {cal_n}")
    gc.collect()

    # ------------------------------------------------------------------ C. operating characteristics
    oc_rng = np.random.default_rng(SEED + 31)
    res = oc_grid(STORE_SD, R_OC, oc_rng, LAM_GRID, S_LIST, M_ELL, S_ELL)
    print(f"[{time.time()-t0:.1f}s] operating-characteristic grid done")

    iA, iB, iD, iBE = TI_N["dstar_A"], TI_N["dstar_B"], TI_N["dstar_D"], TI_N["point_BE"]
    t8, t13 = WEEK_IDX[8], WEEK_IDX[13]
    oc_table = {}
    zones = {}
    pairs_table = {}
    for S in S_LIST:
        oc_table[str(S)] = {}
        for lam in LAM_GRID:
            P, M = res[(S, lam)]
            d8 = P[:, t8, TI3] >= RULE_P
            d13 = P[:, t13, TI3] >= RULE_P
            scale2 = d8 & d13
            stop2 = (~d8) & (~d13)
            cell = {
                "P_scale_two_reads": float(scale2.mean()),
                "P_stop_two_reads": float(stop2.mean()),
                "P_hold_two_reads": float(1.0 - scale2.mean() - stop2.mean()),
                "P_scale_one_read_week8": float(d8.mean()),
                "P_scale_one_read_week13": float(d13.mean()),
                "MC_SE_P_scale_two_reads": math.sqrt(max(scale2.mean() * (1 - scale2.mean()), 1e-12) / R_OC),
            }
            for nm, ix in (("A", iA), ("B", iB), ("D", iD), ("point_BE", iBE)):
                a8 = P[:, t8, ix] >= RULE_P
                a13 = P[:, t13, ix] >= RULE_P
                cell["P_scale_two_reads_line_" + nm] = float((a8 & a13).mean())
                cell["P_stop_two_reads_line_" + nm] = float(((~a8) & (~a13)).mean())
            for nm in ("A", "B", "D"):
                cell["P_scale_bayes_week13_" + nm] = float(np.mean(M[:, t13] >= dstar[nm]))
                cell["P_scale_bayes_week8_" + nm] = float(np.mean(M[:, t8] >= dstar[nm]))
            if lam in (2.5, 3.0, 3.5):
                a, b2 = d8.astype(float), d13.astype(float)
                cell["phi_corr_read8_read13"] = float(np.corrcoef(a, b2)[0, 1]) if a.std() > 0 and b2.std() > 0 else None
            oc_table[str(S)][str(lam)] = cell
        ps = [oc_table[str(S)][str(l)]["P_scale_two_reads"] for l in LAM_GRID]
        zones[str(S)] = {"demand_at_P_scale_0.10": interp_crossing(LAM_GRID, ps, 0.10),
                         "demand_at_P_scale_0.50": interp_crossing(LAM_GRID, ps, 0.50),
                         "demand_at_P_scale_0.90": interp_crossing(LAM_GRID, ps, 0.90)}
        pairs_table[str(S)] = {k: pair_power(res, S, lo, hi) for k, (lo, hi) in PAIRS.items()}

    # Power at week 13 for pairs of truths 0.5, 1.0 and 1.5 units apart (midpoint rule), all store counts
    pair_grid = {}
    for S in S_LIST:
        pair_grid[str(S)] = {}
        for gap in (0.5, 1.0, 1.5):
            for lo in LAM_GRID:
                hi = round(lo + gap, 2)
                if hi in LAM_GRID:
                    pair_grid[str(S)][f"{lo}_vs_{hi}"] = pair_power(res, S, lo, hi, weeks=(13,))[0]
    # pairs that straddle each variant's expected-NPV break-even demand, 1 unit apart
    straddle = {"A_2.0_vs_3.0": (2.0, 3.0), "B_3.0_vs_4.0": (3.0, 4.0), "D_4.5_vs_5.5": (4.5, 5.5)}
    straddle_power = {str(S): {k: pair_power(res, S, lo, hi, weeks=(13,))[0] for k, (lo, hi) in straddle.items()}
                      for S in S_LIST}

    # Sensitivities: store-to-store variation (0.15 and 0.50) and weekly drift noise (0.005); truths only
    def sens_run(sig, drift, seed):
        global SIGMA_ETA
        base = SIGMA_ETA
        SIGMA_ETA = drift
        rr = np.random.default_rng(seed)
        resS = oc_grid(sig, R_SIG, rr, TRUTHS, S_LIST, M_ELL, S_ELL)
        SIGMA_ETA = base
        out_s = {}
        for S in S_LIST:
            out_s[str(S)] = {k: pair_power(resS, S, lo, hi, weeks=(13,))[0] for k, (lo, hi) in PAIRS.items()}
            P15 = resS[(S, 1.5)][0]
            P45 = resS[(S, 4.5)][0]
            d8 = P15[:, t8, TI3] >= RULE_P
            d13 = P15[:, t13, TI3] >= RULE_P
            out_s[str(S)]["P_scale_at_1_5_two_reads"] = float((d8 & d13).mean())
            d8b = P45[:, t8, TI3] >= RULE_P
            d13b = P45[:, t13, TI3] >= RULE_P
            out_s[str(S)]["P_stop_at_4_5_two_reads"] = float(((~d8b) & (~d13b)).mean())
        return out_s

    sig_sens = {}
    for sig in (0.15, 0.50):
        sig_sens[str(sig)] = sens_run(sig, SIGMA_ETA, SEED + int(sig * 1000))
        print(f"[{time.time()-t0:.1f}s] sensitivity sigma_store={sig} done")
    drift_out = sens_run(STORE_SD, SIGMA_ETA_ALT, SEED + 67)
    print(f"[{time.time()-t0:.1f}s] drift sensitivity done")

    # Recommended store count (criteria fixed here): decision pairs 1.5 vs 3.0 and 1.5 vs 4.5 at week 13
    # with power >= 0.80, false-scale at 1.5 <= 0.10 and false-stop at 4.5 <= 0.10 (two-read rule at 3 units).
    rec_S, rec_dr_S, rec_rows = None, None, []
    for S in S_LIST:
        pw = min(pairs_table[str(S)][k][-1] for k in PAIRS)
        pw_dr = min(pairs_table[str(S)]["1.5_vs_3.0"][-1], pairs_table[str(S)]["1.5_vs_4.5"][-1])
        fs = oc_table[str(S)]["1.5"]["P_scale_two_reads"]
        fst = oc_table[str(S)]["4.5"]["P_stop_two_reads"]
        ok = (pw >= POWER_TARGET) and (fs <= FALSE_MAX) and (fst <= FALSE_MAX)
        ok_dr = (pw_dr >= POWER_TARGET) and (fs <= FALSE_MAX) and (fst <= FALSE_MAX)
        se_dr = max(pair_power_se(res, S, 1.5, 3.0), pair_power_se(res, S, 1.5, 4.5))
        rec_rows.append({"stores": S, "min_pair_power_week13_all_pairs": round(pw, 4),
                         "min_pair_power_week13_decision_pairs": round(pw_dr, 4),
                         "MC_SE_min_pair_power_week13_decision_pairs_binding_pair": round(
                             pair_power_se(res, S, 1.5, 3.0) if pairs_table[str(S)]["1.5_vs_3.0"][-1]
                             <= pairs_table[str(S)]["1.5_vs_4.5"][-1] else pair_power_se(res, S, 1.5, 4.5), 4),
                         "MC_SE_max_over_decision_pairs": round(se_dr, 4),
                         "false_scale_at_1_5": round(fs, 4), "false_stop_at_4_5": round(fst, 4),
                         "meets_all_pairs_criteria": bool(ok), "meets_decision_pairs_criteria": bool(ok_dr)})
        if ok and rec_S is None:
            rec_S = S
        if ok_dr and rec_dr_S is None:
            rec_dr_S = S

    # Are the powers at neighbouring store counts distinguishable at R_OC pilots per cell? (independent cells)
    rr = {r["stores"]: (r["min_pair_power_week13_decision_pairs"],
                        r["MC_SE_min_pair_power_week13_decision_pairs_binding_pair"]) for r in rec_rows}
    power_diff_z = {}
    for sa, sb in ((15, 10), (20, 10), (20, 15), (30, 20), (40, 20)):
        d_ = rr[sa][0] - rr[sb][0]
        s_ = math.sqrt(rr[sa][1] ** 2 + rr[sb][1] ** 2)
        power_diff_z[f"{sa}_minus_{sb}"] = {"difference": round(d_, 4), "se": round(s_, 4),
                                           "z": round(d_ / s_, 2) if s_ > 0 else None}

    weeks_needed = {}
    for S in S_LIST:
        wk = None
        for i, w in enumerate(SEP_WEEKS):
            if min(pairs_table[str(S)]["1.5_vs_3.0"][i], pairs_table[str(S)]["1.5_vs_4.5"][i]) >= POWER_TARGET:
                wk = w
                break
        weeks_needed[str(S)] = wk

    # Repeat-rule operating characteristics (cohorts of n first buyers, Beta(1,1) posterior)
    rep_rng = np.random.default_rng(SEED + 41)
    rep_table = {}
    for n in (100, 200, 400):
        rep_table[str(n)] = {}
        for r_true in (0.10, 0.15, 0.20, 0.30):
            k1 = rep_rng.binomial(n, r_true, R_REP)
            k2 = rep_rng.binomial(n, r_true, R_REP)
            p1 = stats.beta.sf(0.15, 1 + k1, 1 + n - k1)
            p2 = stats.beta.sf(0.15, 1 + k2, 1 + n - k2)
            pass1 = p1 >= RULE_P
            pass2 = p2 >= RULE_P
            rep_table[str(n)][str(r_true)] = {
                "P_scale_both_cohorts_pass": float(np.mean(pass1 & pass2)),
                "P_stop_both_cohorts_fail": float(np.mean((~pass1) & (~pass2))),
            }

    print(f"[{time.time()-t0:.1f}s] repeat rule and floors done")

    # ------------------------------------------------------------------ value of the pilot (like for like)
    voi_rng = np.random.default_rng(SEED + 53)
    abm = {v: ab_means[v] for v in ("A", "B", "D")}
    vs = {v: vstar[v] for v in ("A", "B", "D")}
    voi = voi_experiment(N_EFF, N_VOI, voi_rng, V_pop, abm, vs, ab, S_VOI, delay_factor=delay_factor_5wk)
    print(f"[{time.time()-t0:.1f}s] value of the pilot done")
    # Larger independent sample for the scoring-convention comparison (own stream; same experiment, more truths)
    voi_big = voi_experiment(N_EFF, N_VOI_BIG, np.random.default_rng(SEED + 83), V_pop, abm, vs, ab, S_VOI,
                             with_plain=False, delay_factor=delay_factor_5wk)
    print(f"[{time.time()-t0:.1f}s] value of the pilot, large sample for the conventions, done")
    voi_sens = {}
    for n_eff in (1000, 2000):
        r2 = np.random.default_rng(SEED + 59 + n_eff)
        voi_sens[str(n_eff)] = voi_experiment(n_eff, N_VOI_SENS, r2, V_pop, abm, vs, ab, S_VOI, with_plain=False)
        print(f"[{time.time()-t0:.1f}s] value of the pilot at N_EFF {n_eff} done")

    # ------------------------------------------------------------------ D. segment and survey inference
    seg = json.load(open(SEG_JSON, encoding="utf-8"))
    syn = json.load(open(SYN_JSON, encoding="utf-8"))
    n_cell = 1377
    p0 = 0.30
    za2 = stats.norm.ppf(0.975)
    za1 = stats.norm.ppf(0.95)
    zb = stats.norm.ppf(POWER_TARGET)

    def power_two_prop(delta, two_sided=True):
        p1 = p0 + delta / 100.0
        se = math.sqrt(p0 * (1 - p0) / n_cell + p1 * (1 - p1) / n_cell)
        dd = delta / 100.0 / se
        if two_sided:
            return float(stats.norm.cdf(dd - za2) + stats.norm.cdf(-dd - za2))
        return float(stats.norm.cdf(dd - za1))

    def n_for(delta):
        p1 = p0 + delta / 100.0
        pbar = (p0 + p1) / 2.0
        num = (za2 * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p0 * (1 - p0) + p1 * (1 - p1))) ** 2
        return num / ((delta / 100.0) ** 2)

    def mdd_two_sided():
        f = lambda dd: power_two_prop(dd) - POWER_TARGET  # noqa: E731
        return float(brentq(f, 0.01, 20.0)) * 1.0

    seg_out = {
        "ratio_A_25_34_over_35_44": {
            "median": seg["ratio_A_median"], "p05": seg["ratio_A_p05"], "p95": seg["ratio_A_p95"],
            "P_ratio_gt_1": seg["P_ratio_A_25_34_over_35_44_gt_1"],
            "source": "rework/screen/segment_stat_results.json (record 47; sampling error only on the odds ratio)",
        },
        "synthesis_difference_pts_30pct_baseline": {
            "share_scale_median": syn["results_by_baseline"]["30"]["share_scale"]["diff_25_34_minus_35_44_pts"]["median"],
            "odds_scale_median": syn["results_by_baseline"]["30"]["odds_scale"]["diff_25_34_minus_35_44_pts"]["median"],
            "P_diff_gt_0_odds_scale": syn["results_by_baseline"]["30"]["odds_scale"]["P_diff_gt_0"],
            "P_diff_ge_5": syn["results_by_baseline"]["30"]["share_scale"]["P_diff_ge_5"],
            "source": "rework/screen/conversion_synthesis_results.json (record 49)",
        },
        "affordable_cell_size": n_cell,
        "baseline_top2_box": p0,
        "power_two_sided_alpha05": {str(x): round(power_two_prop(x), 4) for x in (0.6, 0.9, 1.2)},
        "power_one_sided_alpha05": {str(x): round(power_two_prop(x, False), 4) for x in (0.6, 0.9, 1.2)},
        "minimum_detectable_difference_pts_two_sided_80pct": round(mdd_two_sided(), 3),
        "n_per_cell_for_80pct_at_1_2_pts": round(n_for(1.2), 0),
        "n_per_cell_for_80pct_at_1_0_pts": round(n_for(1.0), 0),
        "n_per_cell_for_80pct_at_1_23_pts_record_22166_check": round(n_for(1.23), 0),
        "n_per_cell_for_80pct_at_0_9_pts": round(n_for(0.9), 0),
        "n_per_cell_for_80pct_at_0_6_pts": round(n_for(0.6), 0),
        "pre_registered_rule": "Significant only if P(ratio > 1) >= 0.95 and the 90% interval excludes 1.",
    }
    seg_out["verdict_significant"] = bool(seg["P_ratio_A_25_34_over_35_44_gt_1"] >= ALPHA_H0 and seg["ratio_A_p05"] > 1.0)

    # ------------------------------------------------------------------ verdicts
    def verdict(nm):
        s = summ[nm]
        return {"P_NPV_gt_0": s["P_NPV_gt_0"], "MC_SE_P": s["MC_SE_P"], "threshold": ALPHA_H0,
                "reject_H0": bool(s["P_NPV_gt_0"] >= ALPHA_H0),
                "credible_90pct_interval_THB": [s["p05_THB"], s["p95_THB"]],
                "interval_excludes_zero": bool(s["p05_THB"] > 0 or s["p95_THB"] < 0)}

    verdict_i = {"pre_registered_headline_B": verdict("B_headline_full_prior"),
                 "all_variants": {nm: verdict(nm) for nm in summ}}

    # Value of waiting (Bayes rule, week 13 minus week 8) under the three scoring conventions. Two independent
    # samples of truths (N_VOI and N_VOI_BIG) are pooled; delayed rows also apply the five-week delay discount.
    def pick(src, v, conv, key):
        if conv == "start_of_pilot_level":
            return src[v]["paired_diff_THB"].get(key)
        return src[v][conv]["paired_diff_THB"].get(key)

    def pool(x1, n1, x2, n2):
        return {"mean": (n1 * x1["mean"] + n2 * x2["mean"]) / (n1 + n2),
                "se": math.sqrt((n1 * x1["se"]) ** 2 + (n2 * x2["se"]) ** 2) / (n1 + n2)}

    wait_tab, wait_tab_samples = {}, {"main_10000_truths": {}, "independent_large_sample": {}}
    for conv in ("start_of_pilot_level", "decision_time_level", "common_week13_level"):
        wait_tab[conv] = {}
        for sname, src in (("main_10000_truths", voi), ("independent_large_sample", voi_big)):
            wait_tab_samples[sname][conv] = {v: pick(src, v, conv, "B13_%s_minus_B8_%s" % (v, v)) for v in ("A", "B", "D")}
        for v in ("A", "B", "D"):
            wait_tab[conv][v] = pool(wait_tab_samples["main_10000_truths"][conv][v], N_VOI,
                                     wait_tab_samples["independent_large_sample"][conv][v], N_VOI_BIG)
    wait_delayed = {}
    for conv in ("decision_time_level", "common_week13_level"):
        wait_delayed[conv] = {}
        for v in ("A", "B", "D"):
            k = "B13_%s_delayed_minus_B8_%s" % (v, v)
            wait_delayed[conv][v] = pool(pick(voi, v, conv, k), N_VOI, pick(voi_big, v, conv, k), N_VOI_BIG)
    wait_max = max(abs(x["mean"]) for c in wait_tab.values() for x in c.values())
    wait_sig = {c: {v: bool(abs(x["mean"]) > 1.96 * x["se"]) for v, x in d_.items()} for c, d_ in wait_tab.items()}
    wait_delayed_sig = {c: {v: bool(abs(x["mean"]) > 1.96 * x["se"]) for v, x in d_.items()}
                        for c, d_ in wait_delayed.items()}
    read_value = {v: voi[v]["paired_diff_THB"]["B8_%s_minus_no_pilot" % v]["mean"] for v in ("A", "B", "D")}
    wait_rel = {v: max(abs(wait_tab[c][v]["mean"]) for c in wait_tab) / read_value[v] for v in ("A", "B", "D")}
    signs = {v: sorted({("plus" if wait_tab[c][v]["mean"] > 0 else "minus") for c in wait_tab}) for v in ("A", "B", "D")}
    limit_wait = (
        "Value of waiting (Bayes rule, week 13 minus week 8), pooled over "
        f"{N_VOI + N_VOI_BIG:,} simulated truths: the sign depends on the scoring convention "
        "(start-of-pilot level, level at the decision week, common week-13 level). The largest absolute value over the "
        f"three bases and three conventions is THB {wait_max:,.0f}; as a share of the value of the demand read it is at most "
        f"{100 * wait_rel['A']:.1f} percent (A), {100 * wait_rel['B']:.1f} percent (B) and {100 * wait_rel['D']:.1f} percent (D). "
        "Acting five weeks later also costs the discount factor "
        f"{delay_factor_5wk:.4f} at the prior mean rate (about THB {1e6 * (1.0 - delay_factor_5wk):,.0f} per THB 1 million of NPV); "
        "the delayed rows apply it to the week-13 rule.")
    halv = {S: pairs_table[str(S)]["1.5_vs_3.0"][-1] - pairs_table[str(S)]["1.5_vs_3.0"][0] for S in (15, 20, 30, 40)}
    half_pair = {S: pairs_table[str(S)]["3.0_vs_4.5"][-1] - pairs_table[str(S)]["3.0_vs_4.5"][0] for S in (30, 40)}
    conv_diff = max(abs(a - b) for ev in (evolution, evolution_40)
                    for pr in ev["separation_by_scoring_convention"].values()
                    for a, b in zip(pr["power_scored_on_start_label_by_week"],
                                    pr["power_scored_on_level_at_read_week_by_week"]))
    realised_sd13 = float(np.mean([evolution[str(t)]["realised_level_sd_of_log_over_pilots_by_week"][-1] for t in TRUTHS]))
    limit_sep = (
        "Separation power is scored against the start-of-pilot label. For the halving pair (1.5 against 3.0) the power "
        f"changes by at most {max(abs(v) for v in halv.values()):.2f} between week 4 and week 13 at 15 to 40 stores "
        f"(Monte Carlo SE about 0.02), so weeks after about 4 add little. For 3.0 against 4.5 the change is "
        f"{half_pair[30]:+.2f} at 30 stores and {half_pair[40]:+.2f} at 40 stores. Re-scoring each pair against the level "
        f"at the read week instead of the start label changes the power by at most {conv_diff:.2f} (separation_by_scoring_convention), "
        "so the fall is not a labelling effect: the level itself drifts (sd of the log level "
        f"{realised_sd13:.3f} by week 13), which moves some pilots toward the midpoint. It depends on the assumed weekly "
        f"drift of {SIGMA_ETA} (ASSUMPTION); at {SIGMA_ETA_ALT} the week-13 power for 3.0 against 4.5 at 40 stores is "
        f"{drift_out['40']['3.0_vs_4.5']:.2f}.")
    max_z_stores = max(abs(v_["z"]) for v_ in power_diff_z.values() if v_["z"] is not None)
    limit_stores = (
        "Store count: the recommendation is at halving resolution (1.5 against 3.0 units). Powers are estimated from "
        f"{R_OC} pilots per cell (binomial SE about 0.02 near 0.8). The largest absolute z between neighbouring store "
        f"counts in the comparisons made (15 against 10, 20 against 10, 20 against 15, 30 against 20, 40 against 20) is "
        f"{max_z_stores:.1f}; counts whose powers differ by less than about 0.05 are not statistically distinguishable.")

    peak_mb = None
    if psutil is not None:
        try:
            mi = psutil.Process().memory_info()
            peak_mb = float(getattr(mi, "peak_wset", mi.rss) / 1e6)
        except Exception:
            peak_mb = None

    out = {
        "task": "T14 sequential Monte Carlo on the valuation and the pilot; significance (third pass)",
        "seed": SEED,
        "quick_mode": QUICK,
        "particles": {"prior_draws": N_PRIOR, "fan": N_FAN, "operating_characteristics": N_PF},
        "peak_working_set_MB": peak_mb,
        "pilot_model": {
            "weeks": T, "reads": list(READS), "reads_tier": "ASSUMPTION (the plan says two consecutive reads without dates)",
            "store_count_fan": S_FAN, "NB_size_kappa_per_store_week": KAPPA,
            "weekly_drift_noise_sigma_eta": SIGMA_ETA, "drift_prior_sd": MU_SD,
            "liu_west_delta": DELTA_LW, "liu_west_a": A_LW, "liu_west_h": H_LW,
            "store_heterogeneity_sigma_store": STORE_SD,
            "store_offset_sd_at_S": {str(S): STORE_SD / math.sqrt(S) for S in S_LIST},
            "N_EFF_stores": N_EFF, "N_EFF_tier": "ASSUMPTION: chosen so that 3 units a store-week equal 200,000 cubes a year; nothing in the repo ties the two",
            "national_log_demand_prior": {"mean": M_ELL, "sd": S_ELL},
            "lambda_prior_p05_p50_p95": [float(v) for v in lam_prior_q],
            "point_value_break_even_lambda_record05": LAM_BE, "point_value_break_even_cubes_a_year_record05": V_STAR,
            "rule": {"threshold": RULE_THR, "read_p": RULE_P, "reads_weeks": list(READS)},
            "thresholds_carried": [float(x) for x in THRS], "named_threshold_index": TI_N,
        },
        "pre_registered_tests": {
            "i": "Reject H0 (NPV <= 0) if P(NPV > 0) >= 0.95 under variant B. 90% credible interval against zero. Same rule reported for every other variant.",
            "ii": "Segment lead significant only if P(ratio > 1) >= 0.95 and 90% interval excludes 1.",
            "iii": "Separation: decide above if P(demand > midpoint) >= 0.9, below if <= 0.1; power target 0.80. "
                   "Rule reads at weeks 8 and 13 with posterior threshold 0.5. Recommended store count criteria: "
                   "week-13 power >= 0.80 for the decision pairs (1.5 vs 3.0, 1.5 vs 4.5), false-scale at 1.5 <= 0.10, false-stop at 4.5 <= 0.10.",
        },
        "reconciliation": {
            "record05_deterministic_npv_at_c_4_91_THB": round(recon_npv, 1),
            "record05_npv_at_fixed_500000_THB": record_npv,
            "record05_break_even_cubes_a_year_at_500k_10pct": record_be,
            "python_break_even_cubes_check": round(V_STAR, 1),
            "record75_after_excise_contribution_exact": c_after_75,
            "record75_chain_ratio": CHAIN_RATIO,
            "record75_after_tax_npv_target_THB": npv_75_target,
            "this_script_after_tax_npv_at_c_3_9444_THB": round(recon_D, 2),
            "record75_after_tax_break_even_cubes_0pct_cannibalisation": float(va["break_points"]["after_excise"]["npv_zero_cubes_per_year_after_tax_by_share"]["0.0"]["cubes_per_year"]),
            "this_script_after_tax_break_even_cubes": round(v_point_D, 1),
        },
        "prior_check_from_draws": prior_check,
        "prior_summaries": summ,
        "variant_definitions": {
            "A_record05_structure": "All inputs with priors, except binder and flavour at 0, citric acid at 2.10 g, no cannibalisation; before excise, pre-tax",
            "B_headline_full_prior": "All inputs with priors, incl. binder and flavour, citric acid 2.10 to 3.70 g, cannibalisation; before excise, pre-tax (pre-registered headline)",
            "C_tax_no_relief_before_excise": "B with 20 percent tax on positive annual operating profit, no loss relief, no depreciation shield",
            "A2_record05_structure_after_excise": "A with the ex-factory share scaled by 0.535628 / 0.60 (can net-to-listing chain ratio, record 75), pre-tax",
            "B2_full_prior_after_excise_pretax": "B on the after-excise basis, pre-tax",
            "D_record75_lead_basis": "B on the after-excise basis with 20 percent tax, losses credited in the year, year-0 outlay (one year of fixed cost) depreciated straight line over 5 years (record 75 structure)",
            "D_cf_standalone_carry_forward": "D with a stand-alone entity: depreciation deducted, losses carried forward (5 years)",
            "B_wide_repeat_prior": "B with repeat ~ Beta(mean 0.283, sd 0.10), allowing repeat below the 15 percent stop floor",
            "D_wide_repeat_prior": "D with the same wide repeat prior",
            "B_no_price_volume_correlation": "B with rho = 0 between shelf price and first-purchase volume",
        },
        "sensitivity_B_headline_NPV": sens_B,
        "sensitivity_D_lead_basis_NPV": sens_D,
        "joint_narrowing": joint,
        "fixed_demand": {
            "N_EFF": N_EFF,
            "note": "NPV at a fixed true steady demand with every other input drawn from its prior (price and volume independent). Cubes a year = 52 * N_EFF * demand. N_EFF is an ASSUMPTION.",
            "by_variant": fixed_demand,
            "expected_NPV_break_even_cubes_a_year": vstar,
            "expected_NPV_break_even_demand_units": dstar,
            "median_NPV_zero_cubes_a_year": v_med,
            "expected_NPV_break_even_demand_by_N_EFF": neff_table,
            "N_EFF_at_which_3_unit_line_equals_expected_NPV_break_even": neff_cross,
            "copula_retained_expected_NPV_break_even_cubes_a_year": vstar_corr,
            "copula_retained_expected_NPV_break_even_demand_units": {k: (v / (WEEKS_PER_YEAR * N_EFF) if v else None) for k, v in vstar_corr.items()},
            "point_value_NPV_at_input_medians_by_demand": point_npv,
            "point_value_break_even_cubes_after_excise_aftertax": v_point_D,
            "shelf_price_pinned_14_5_to_15_5": {"share_of_prior": band_share, "by_variant": price_pinned},
            "oracle_rule_payoffs_THB_joint_prior": oracle,
        },
        "significance": {"i_NPV": verdict_i, "ii_segment_lead": seg_out},
        "pilot": {
            "fan": {k: {
                "week_lambda_q05_q50_q95": v["big"]["lam_q"].tolist(),
                "week_P_NPV_gt_0": {nm: v["big"]["p_npv"][nm].tolist() for nm in FAN_VARS},
                "week_NPV_q05_q50_q95_THB": {nm: v["big"]["npv_q"][nm].tolist() for nm in FAN_VARS},
                "week_P_demand_ge_3": v["big"]["p"][:, TI3].tolist(),
                "week_P_demand_ge_dstar": {nm: v["big"]["p"][:, TI_N["dstar_" + nm]].tolist() for nm in FAN_VARS},
                "week_posterior_mean_demand": v["big"]["mean_lam"].tolist(),
                "particle_check_max_abs_diff_P_ge_3": v["particle_check_max_abs_diff_P_ge_3"],
                "week_P_NPV_gt_0_rao_blackwellised": {nm: v["big"]["p_rb"][nm].tolist() for nm in FAN_VARS},
                "week_expected_NPV_THB": {nm: v["big"]["e_npv"][nm].tolist() for nm in FAN_VARS},
                "rb_vs_particle_mapping_max_abs_diff_P_NPV_gt_0": v["rb_vs_particle_mapping_max_abs_diff_P_NPV_gt_0"],
                "realised_national_path_weeks_1_to_13": v["path"],
                "Y_counts": v["Y"],
                "resamples_at_N_FAN": v["big"]["resamples"],
            } for k, v in fan.items()},
            "calibration_coverage_90pct_week13_2000_particles": cal,
            "calibration_coverage_90pct_week13_10000_particles": cal_n,
            "evolution_over_many_pilots": {
                "note": "R pilots of 20 stores per truth, 2,000 particles each, own random stream (seed + 71). "
                        "P(NPV > 0 | data) is the weight-averaged exact conditional P(NPV > 0 | volume) of the prior "
                        "(static inputs independent of demand). Mean, SE of the mean and 10th, 50th, 90th percentile "
                        "across pilots, weeks 1 to 13. The truth is the start-of-pilot level.",
                "pilots_per_truth": R_EVO,
                "by_truth": evolution,
                "at_40_stores_by_truth": evolution_40,
            },
        },
        "operating_characteristics": {
            "rule_two_reads_weeks_8_and_13": oc_table,
            "scale_probability_zones_two_read_rule": zones,
            "separation_power_by_store_count_and_week": {S: {k: [round(x, 4) for x in pairs_table[S][k]] for k in PAIRS} for S in pairs_table},
            "separation_power_week13_pairs_by_gap": pair_grid,
            "separation_power_week13_pairs_straddling_expected_NPV_break_even": straddle_power,
            "separation_weeks": list(SEP_WEEKS),
            "weeks_needed_for_80pct_decision_pairs": weeks_needed,
            "recommendation_grid": rec_rows,
            "recommended_store_count_all_pairs_criteria": rec_S,
            "recommended_store_count_decision_pairs_criteria": rec_dr_S,
            "recommendation_power_difference_between_store_counts": power_diff_z,
            "value_of_waiting_week13_minus_week8_by_convention": {
                "paired_diff_THB_Bayes_rule_pooled": wait_tab, "abs_diff_exceeds_1_96_se": wait_sig,
                "paired_diff_THB_Bayes_rule_by_sample": wait_tab_samples,
                "pooled_truths": N_VOI + N_VOI_BIG,
                "paired_diff_THB_week13_rule_after_five_week_delay_discount_pooled": wait_delayed,
                "delayed_abs_diff_exceeds_1_96_se": wait_delayed_sig,
                "largest_abs_diff_THB": wait_max, "largest_abs_share_of_demand_read_value": wait_rel,
                "signs_over_conventions": signs,
                "demand_read_value_start_level_THB": read_value,
                "conventions": "start_of_pilot_level: every rule scored on the start level (second pass). "
                               "decision_time_level: a rule scored on the national level at its own decision week. "
                               "common_week13_level: every rule scored on the week-13 level."},
            "recommendation_note": "The criterion applies to the decision pairs (1.5 against 3.0 and 1.5 against 4.5), "
                                   "a halving of demand. The pair around the rule line (3.0 against 4.5) does not reach 80 "
                                   "percent power at any tested store count, so no tested count meets an all-pairs criterion. "
                                   "Powers are estimated from R_OC pilots per cell (binomial SE about 0.02 near 0.8).",
            "delay_discount_factor_5_weeks_prior_mean": delay_factor_5wk,
            "delay_discount_loss_THB_per_million_of_NPV": 1e6 * (1.0 - delay_factor_5wk),
            "drift_sensitivity_week13_sigma_eta_0_005": drift_out,
            "store_heterogeneity_sensitivity_week13": sig_sens,
            "repeat_rule_cohorts": rep_table,
            "P_contribution_below_3_51_prior_variant_B": p_contrib_below,
            "P_contribution_below_3_51_prior_variant_A": p_contrib_below_A,
            "P_contribution_below_2_54_prior_variant_D_after_excise": p_contrib_below_D,
            "P_cannibalisation_share_at_or_above_50pct_prior": p_cannib_review,
            "P_cannibalisation_share_at_or_above_50pct_analytic_beta": p_cannib_review_analytic,
            "P_cannibalisation_share_at_or_above_record75_break_even_7_5pct_prior": p_cannib_ge_k75,
            "record75_break_even_cannibalised_share_at_base_volume": k75,
            "value_of_the_pilot_like_for_like": voi,
            "value_of_the_pilot_N_EFF_sensitivity": voi_sens,
            "value_of_the_pilot_large_sample_for_conventions": voi_big,
        },
        "limits": [
            "Priors are ASSUMPTIONS or PROXY values from records 05, 06 and 70. No market data.",
            "The 20 percent tax rate is tier S (primary-origin page, Revenue Department page 6044, last updated 23 November 2020, read 20 October 2026 through a page summary, so not P). The structure (loss relief, depreciation shield, carry-forward) is an ASSUMPTION; three structures are reported.",
            "N_EFF (store-equivalents behind 200,000 cubes) is an ASSUMPTION; every break-even in units a store-week is conditional on it. It is back-solved so that 3 units a store-week equal 200,000 cubes; as context it is 8.0 percent of the about 15,945 7-Eleven stores of submission/04 (read as Thailand-only by inference), which is not a derivation.",
            "Basis mixing: variants B, C, B_wide and B_rho0 subtract the after-excise can contribution (THB 4.13) from a before-excise cube contribution, which flatters the cannibalised cases (record 75, section 11). The consistent cannibalisation versions are B2 and D (both after excise); P(NPV above 0) is lower there (B2 0.267, D 0.262). Variants A and A2 have no cannibalisation term, so the mixing does not arise in them. The pre-registered headline B is therefore the more favourable reading and still fails the test.",
            "Variant A fixes citric acid at 2.10 g, binder and flavour at zero and cannibalisation at zero; the other variants give those three inputs priors.",
            limit_wait,
            limit_sep,
            limit_stores,
            "Demand model: one common national level plus a store offset with sd sigma_store/sqrt(S). Store heterogeneity beyond that is not modelled.",
            "The pilot informs demand only in this model. It does not inform fixed cost, price realisation, cost lines or the cannibalisation share, so the value of the pilot here is a lower bound for any learning on those.",
            "In the pilot world the static inputs are independent of demand; the prior predictive keeps the price and volume correlation. The copula-retained break-even is reported.",
            "Repeat rule uses Beta(1,1) in the operating characteristics; contribution rule uses the prior probability only.",
            "Read weeks 8 and 13 are an ASSUMPTION; the two reads come from one cumulative posterior and are correlated (phi reported).",
        ],
        "runtime_seconds": round(time.time() - t0, 1),
    }

    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(jsonable(out), fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"[{time.time()-t0:.1f}s] wrote {OUT_JSON}")

    os.makedirs(CHART_DIR, exist_ok=True)
    ctx = {"npvA": npvA, "npvB": npvB, "npvD": npvD, "fan": fan, "oc_table": oc_table, "pairs_table": pairs_table,
           "dstar": dstar, "ab": ab, "fixed_demand": fixed_demand, "voi": voi, "zones": zones, "vstar": vstar,
           "evolution": evolution}
    make_charts(ctx)
    print(f"[{time.time()-t0:.1f}s] charts written; peak working set {peak_mb} MB")


# ---------------------------------------------------------------------- charts
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"   # variants A, B, D (reference palette slots 1 to 3)
CV, CM, CG = "#6250d6", "#e87ba4", "#008300"   # slots 7, 5, 6: pairs of truths
TRUTH_COL = {"1.5": "#9ab3d5", "3.0": "#4f78b4", "4.5": "#16335f"}   # ordered by demand: light to dark
VAR_COL = {"A": C1, "B": C2, "D": C3}


def _style(ax):
    ax.grid(color=GRID, lw=0.7)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#9a9994")
    ax.tick_params(colors=INK2, labelsize=9)
    ax.xaxis.label.set_color(INK2)
    ax.yaxis.label.set_color(INK2)


def make_charts(ctx):
    plt.rcParams.update({"font.size": 10, "text.color": INK, "axes.titlesize": 10.5})
    npvA, npvB, npvD = ctx["npvA"], ctx["npvB"], ctx["npvD"]
    dstar, ab = ctx["dstar"], ctx["ab"]
    fan, oc_table, pairs_table = ctx["fan"], ctx["oc_table"], ctx["pairs_table"]
    labs = {"A": "A: simpler structure (before excise, pre-tax)", "B": "B: full prior (headline)",
            "D": "D: after excise and tax"}

    # ---- 1. NPV distribution with P(NPV > 0) marked
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6), dpi=130)
    allv = np.concatenate([npvA, npvB, npvD]) / 1e6
    lo, hi = np.percentile(allv, [1, 99])
    bins = np.linspace(lo, hi, 90)
    series = (("A", npvA), ("B", npvB), ("D", npvD))
    ax = axes[0]
    for nm, v in series:
        ax.hist(v / 1e6, bins=bins, weights=np.full(len(v), 1.0 / len(v)), histtype="step", lw=1.8, color=VAR_COL[nm])
    ax.axvspan(lo, 0, color="#f4c7c3", alpha=0.25, zorder=0)
    ax.axvline(0, color=INK, lw=1.4)
    ax.set_xlim(lo, hi)
    ax.set_xlabel("Project NPV, THB million (five years, 10 percent unless varied)")
    ax.set_ylabel("Share of prior draws per bin")
    ax.set_title("Prior predictive NPV (200,000 draws per variant, seed 20261020)")
    _style(ax)
    ax = axes[1]
    xs = np.linspace(lo, hi, 400)
    for nm, v in series:
        srt = np.sort(v / 1e6)
        cdf = np.searchsorted(srt, xs, side="right") / len(srt)
        ax.plot(xs, cdf, color=VAR_COL[nm], lw=2.0)
        p0 = float(np.mean(v <= 0))
        ax.plot([0], [p0], marker="o", color=VAR_COL[nm], ms=7, mec="white", mew=1.2)
        ax.annotate(f"{nm}: P(NPV > 0) = {1 - p0:.2f}", xy=(0, p0), xytext=(0.12 * hi, p0 - 0.035),
                    fontsize=9, color=INK, va="center")
    ax.axhline(1 - ALPHA_H0, color=INK2, ls="--", lw=1.1)
    ax.text(lo + 0.42 * (hi - lo), 1 - ALPHA_H0 + 0.012, "H0 is rejected only if a curve is below 0.05 at zero",
            fontsize=8.5, color=INK2, va="bottom")
    ax.axvline(0, color=INK, lw=1.4)
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel("Project NPV, THB million")
    ax.set_ylabel("P(NPV at or below x)")
    ax.set_title("Cumulative distribution (height at zero = 1 minus P(NPV > 0))")
    _style(ax)
    handles = [plt.Line2D([0], [0], color=VAR_COL[nm], lw=2.2) for nm in ("A", "B", "D")]
    fig.legend(handles, [f"{labs[nm]}, P(NPV > 0) = {float(np.mean(v > 0)):.2f}" for nm, v in series],
               loc="lower center", ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 0.045))
    fig.suptitle("Is the projected NPV above zero? No: P(NPV > 0) is far below the 0.95 set in advance", fontsize=12)
    fig.tight_layout(rect=[0, 0.11, 1, 0.95])
    fig.text(0.5, 0.012, "Axis shows the 1st to 99th percentile of the three draws. Conditional on the stated priors; "
             "not a finding from market data.", ha="center", fontsize=8.5, color=INK2)
    fig.savefig(os.path.join(CHART_DIR, "smc_npv_distribution.png"))
    plt.close(fig)

    # ---- 2. Pilot posterior fan: one representative pilot per truth, and the average over many pilots
    evo = ctx["evolution"]
    fig, axes = plt.subplots(3, 3, figsize=(16, 13.2), dpi=130)
    weeks = np.arange(1, T + 1)
    for ax, lam in zip(axes[0], TRUTHS):
        v = fan[str(lam)]["big"]["lam_q"]
        ax.fill_between(weeks, v[:, 0], v[:, 2], color="#8da2c0", alpha=0.35, lw=0,
                        label="posterior 5th to 95th percentile")
        ax.plot(weeks, v[:, 1], color="#33415c", lw=2, label="posterior median")
        ax.plot(weeks, fan[str(lam)]["path"], color=INK, lw=1.0, marker=".", label="realised national level")
        ax.axhline(RULE_THR, color=INK2, ls=":", lw=1.3)
        ax.text(13.15, RULE_THR, "line 3", fontsize=8.5, color=INK2, va="center")
        for nm in ("A", "B", "D"):
            ax.axhline(dstar[nm], color=VAR_COL[nm], ls="--", lw=1.1)
            ax.text(13.15, dstar[nm], f"{nm} {dstar[nm]:.1f}", fontsize=8.5, color=VAR_COL[nm], va="center")
        ax.set_title(f"One pilot: true starting demand {lam} (20 stores)")
        ax.set_xlabel("Pilot week")
        ax.set_ylabel("Units per store per week")
        ax.set_xticks([1, 4, 8, 13])
        ax.set_xlim(1, 13)
        ax.set_ylim(0, max(6.5, float(v[:, 2].max()) + 0.5))
        _style(ax)
    axes[0, 0].legend(fontsize=8, loc="upper left", frameon=False, bbox_to_anchor=(0.0, 0.8))
    vlab = {"A": "variant A (simpler structure)", "B": "variant B (full prior, headline)",
            "D": "variant D (after excise and tax)"}
    for ax, nm in zip(axes[1], ("A", "B", "D")):
        for lam in TRUTHS:
            c = evo[str(lam)][nm]["P_NPV_gt_0"]
            col = TRUTH_COL[str(lam)]
            ax.fill_between(weeks, c["p10"], c["p90"], color=col, alpha=0.22, lw=0)
            ax.plot(weeks, c["mean"], color=col, lw=2.3, label=f"true demand {lam}")
        ax.axhline(ALPHA_H0, color=INK2, ls=":", lw=1.2)
        ax.text(1.2, ALPHA_H0 + 0.015, "0.95 threshold", fontsize=8.5, color=INK2)
        ax.set_ylim(0, 1.05)
        ax.set_xlim(1, 13)
        ax.set_xticks([1, 4, 8, 13])
        ax.set_xlabel("Pilot week")
        ax.set_ylabel("Posterior P(NPV > 0)")
        ax.set_title(f"Mean and 10th to 90th percentile, {R_EVO} pilots, {vlab[nm]}", fontsize=9.5)
        ax.legend(fontsize=8.5, loc="upper center", frameon=False, ncol=3, bbox_to_anchor=(0.5, 0.915))
        _style(ax)
    for ax, nm, ttl in ((axes[2, 0], "B", "One pilot: P(NPV > 0), variant B"),
                        (axes[2, 1], "D", "One pilot: P(NPV > 0), variant D")):
        for lam in TRUTHS:
            ax.plot(weeks, fan[str(lam)]["big"]["p_npv"][nm], color=TRUTH_COL[str(lam)], lw=2.0, marker="o", ms=3.2,
                    label=f"true demand {lam}")
        ax.axhline(ALPHA_H0, color=INK2, ls=":", lw=1.2)
        ax.text(1.2, ALPHA_H0 + 0.015, "0.95 threshold", fontsize=8.5, color=INK2)
        ax.set_ylim(0, 1.05)
        ax.set_xlim(1, 13)
        ax.set_xticks([1, 4, 8, 13])
        ax.set_xlabel("Pilot week")
        ax.set_ylabel("Posterior probability")
        ax.set_title(ttl)
        ax.legend(fontsize=8.5, loc="upper left", frameon=False, bbox_to_anchor=(0.0, 0.88))
        _style(ax)
    ax = axes[2, 2]
    for lam in TRUTHS:
        c = evo[str(lam)]["P_demand_ge_3"]
        col = TRUTH_COL[str(lam)]
        ax.fill_between(weeks, c["p10"], c["p90"], color=col, alpha=0.22, lw=0)
        ax.plot(weeks, c["mean"], color=col, lw=2.3, label=f"true demand {lam}")
    ax.axhline(RULE_P, color=INK2, ls=":", lw=1.2)
    ax.text(13, RULE_P + 0.015, "0.5: read says at or above 3", fontsize=8.5, color=INK2, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_xlim(1, 13)
    ax.set_xticks([1, 4, 8, 13])
    ax.set_xlabel("Pilot week")
    ax.set_ylabel("Posterior probability")
    ax.set_title(f"Mean and 10th to 90th percentile, {R_EVO} pilots: P(demand at or above 3)", fontsize=9.5)
    ax.legend(fontsize=8.5, loc="center right", frameon=False, bbox_to_anchor=(1.0, 0.72))
    _style(ax)
    fig.suptitle("Sequential Monte Carlo for simulated 20-store pilots: one pilot per truth (200,000 particles) and the "
                 f"average of {R_EVO} pilots per truth (2,000 particles); conditional on priors", fontsize=12)
    fig.tight_layout(rect=[0, 0.03, 1, 0.965])
    fig.text(0.5, 0.01, "Top row dashed lines: expected-NPV break-even demand for variants A, B and D; dotted: the 3-unit "
             "rule line. Middle row: bands are the 10th to 90th percentile across simulated pilots.",
             ha="center", fontsize=8.5, color=INK2)
    fig.savefig(os.path.join(CHART_DIR, "smc_pilot_posterior_fan.png"))
    plt.close(fig)

    # ---- 3. Operating characteristics
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.6), dpi=130)
    cols_s = {5: "#b9b8b2", 10: "#8a8983", 20: "#55544f", 40: INK}
    for ax, key, ttl in ((axes[0, 0], "P_scale_two_reads", "P(scale): both reads at weeks 8 and 13 at or above 3"),
                         (axes[0, 1], "P_stop_two_reads", "P(stop): both reads below 3")):
        for S in (5, 10, 20, 40):
            ys = [oc_table[str(S)][str(l)][key] for l in LAM_GRID]
            ax.plot(list(LAM_GRID), ys, marker="o", ms=4, lw=1.8, color=cols_s[S], label=f"{S} stores")
        ax.axvline(RULE_THR, color=INK2, ls=":", lw=1.4)
        for nm in ("A", "B", "D"):
            ax.axvline(dstar[nm], color=VAR_COL[nm], ls="--", lw=1.2)
            ax.text(dstar[nm] + 0.04, 1.045, f"{nm} {dstar[nm]:.1f}", fontsize=8.5, color=VAR_COL[nm])
        ax.set_xlabel("True demand, units per store per week")
        ax.set_ylabel("Probability")
        ax.set_ylim(-0.02, 1.1)
        ax.set_title(ttl)
        ax.legend(fontsize=8.5, loc="center left" if key == "P_scale_two_reads" else "center right", frameon=False)
        _style(ax)
    ax = axes[1, 0]
    xs = list(S_LIST)
    for key, lab, col in (("1.5_vs_3.0", "1.5 vs 3.0", CV), ("3.0_vs_4.5", "3.0 vs 4.5", CM),
                          ("1.5_vs_4.5", "1.5 vs 4.5", CG)):
        ys = [pairs_table[str(S)][key][-1] for S in xs]
        ax.plot(xs, ys, marker="s", ms=5, lw=1.9, color=col, label=f"truths {lab}")
    ax.axhline(POWER_TARGET, color=INK2, ls="--", lw=1.2)
    ax.text(24.0, POWER_TARGET - 0.045, "80% power", fontsize=8.5, color=INK2)
    ax.set_xlabel("Stores in the pilot")
    ax.set_ylabel("Power to separate the two truths at week 13")
    ax.set_ylim(0, 1.04)
    ax.set_title("Separation power at week 13 (midpoint rule, 0.9 and 0.1)")
    ax.legend(fontsize=8.5, loc="lower right", frameon=False)
    _style(ax)
    ax = axes[1, 1]
    voi = ctx["voi"]
    rules = [("no_pilot", "No pilot"), ("R1_8", "One read\nweek 8"), ("R1_13", "One read\nweek 13"),
             ("R2", "Two reads\n(proposed)"), ("B13", "Bayes rule\nweek 13")]
    width = 0.26
    for j, nm in enumerate(("A", "B", "D")):
        vals, ses = [], []
        for k, _ in rules:
            kk = k if k != "B13" else "B13_" + nm
            vals.append(voi[nm]["value_THB"][kk]["mean"] / 1000.0)
            ses.append(voi[nm]["value_THB"][kk]["se"] / 1000.0)
        xpos = np.arange(len(rules)) + (j - 1) * width
        ax.bar(xpos, vals, width=width * 0.9, color=VAR_COL[nm], label=f"variant {nm}")
        ax.errorbar(xpos, vals, yerr=1.96 * np.array(ses), fmt="none", ecolor=INK, elinewidth=1.0, capsize=2)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xticks(np.arange(len(rules)))
    ax.set_xticklabels([r[1] for r in rules], fontsize=8.5)
    ax.set_ylabel("Expected NPV captured, THB thousand")
    ax.set_title("Value of the pilot by decision rule (20 stores; bars show 95% intervals)")
    ax.legend(fontsize=8.5, loc="lower left", frameon=False)
    _style(ax)
    fig.suptitle("Operating characteristics of the scale and stop rule (simulated pilots; "
                 f"{R_OC} per cell; value panel {N_VOI:,} truths)", fontsize=12)
    fig.tight_layout(rect=[0, 0.03, 1, 0.96])
    fig.text(0.5, 0.01, "Top row: dashed lines are the expected-NPV break-even demand for variants A (blue), B (orange) "
             "and D (aqua); dotted is the 3-unit rule line.", ha="center", fontsize=8.5, color=INK2)
    fig.savefig(os.path.join(CHART_DIR, "smc_operating_characteristics.png"))
    plt.close(fig)

    # ---- 4. Expected NPV by true demand
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.8), dpi=130)
    dgrid = np.linspace(0.5, 6.0, 56)
    ax = axes[0]
    Vg = WEEKS_PER_YEAR * N_EFF * dgrid
    for nm in ("A", "B", "D"):
        al, be = ab[nm]
        mean_y = (al.mean() * Vg - be.mean()) / 1e6
        ax.plot(dgrid, mean_y, color=VAR_COL[nm], lw=2.2, label=f"{labs[nm]}; zero at {dstar[nm]:.2f}")
        if nm == "B":
            qs = np.array([np.percentile(al * v - be, [25, 75]) for v in Vg]) / 1e6
            ax.fill_between(dgrid, qs[:, 0], qs[:, 1], color=VAR_COL[nm], alpha=0.14, lw=0)
    ax.axhline(0, color=INK, lw=1.0)
    ax.axvline(RULE_THR, color=INK2, ls=":", lw=1.3)
    ax.text(RULE_THR + 0.05, -4.2, "rule line 3", fontsize=8.5, color=INK2)
    ax.axvline(LAM_BE, color=INK2, ls="--", lw=1.0)
    ax.text(LAM_BE - 0.05, -4.5, f"point-value\nbreak-even {LAM_BE:.2f}\n(medians, before excise)",
            fontsize=8, color=INK2, ha="right", va="bottom")
    ax.set_xlim(0.5, 6.0)
    ax.set_ylim(-4.6, 5.0)
    ax.set_xlabel("True steady demand, units per store per week (1,282 store-equivalents, ASSUMPTION)")
    ax.set_ylabel("NPV, THB million")
    ax.set_title("Expected NPV by true demand; shaded band is the 25th to 75th percentile for B")
    ax.legend(fontsize=8.3, loc="upper left", frameon=True, facecolor="white", edgecolor="none", framealpha=0.85)
    _style(ax)
    ax = axes[1]
    for nm in ("A", "B", "D"):
        al, be = ab[nm]
        pp = [float(np.mean(al * v - be > 0)) for v in Vg]
        ax.plot(dgrid, pp, color=VAR_COL[nm], lw=2.2, label=labs[nm])
    ax.axhline(ALPHA_H0, color=INK2, ls="--", lw=1.1)
    ax.text(0.55, ALPHA_H0 + 0.015, "0.95 threshold", fontsize=8.5, color=INK2)
    ax.axhline(0.5, color=INK2, ls=":", lw=1.0)
    ax.axvline(RULE_THR, color=INK2, ls=":", lw=1.3)
    ax.text(RULE_THR + 0.05, 0.88, "rule line 3", fontsize=8.5, color=INK2)
    ax.set_xlim(0.5, 6.0)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("True steady demand, units per store per week")
    ax.set_ylabel("P(NPV > 0), other inputs from their priors")
    ax.set_title("Even a known demand of 6 units does not make NPV certain")
    ax.legend(fontsize=8.5, loc="lower right", frameon=False)
    _style(ax)
    fig.suptitle("Expected NPV and P(NPV > 0) at a fixed true demand (the point value at medians is not the "
                 "expected value)", fontsize=12)
    fig.tight_layout(rect=[0, 0.02, 1, 0.95])
    fig.savefig(os.path.join(CHART_DIR, "smc_expected_npv_by_demand.png"))
    plt.close(fig)


if __name__ == "__main__":
    main()
