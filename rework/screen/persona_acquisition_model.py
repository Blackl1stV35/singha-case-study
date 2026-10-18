"""Persona and acquisition-cost model for the sodium-free lime cube (desk study, no respondents).

Every number below carries one label:
  SOURCED     printed page of the NSO Health Behaviour 2021 report (uploaded file SD10_04_114_1.pdf;
              printed arabic page + 19 = PDF page), or a URL read in this study with WebFetch,
              or a repo record named in the comment
  PROXY       a figure that stands in for what the product needs; the gap is stated
  ASSUMPTION  no source; a range is given
  DERIVED     arithmetic on the labelled inputs

Outputs: rework/screen/persona_acquisition_results.json and
         rework/charts/cost_per_acquired_customer_scenarios.png
Run: python persona_acquisition_model.py
"""
import json
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_JSON = os.path.join(HERE, "persona_acquisition_results.json")
OUT_PNG = os.path.join(REPO, "rework", "charts", "cost_per_acquired_customer_scenarios.png")

SEED = 20261019
N = 20000

# Chart colours: dataviz reference palette, categorical slot 1 (blue), light surface and ink tokens.
BLUE = "#2a78d6"
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#d9d8d3"
BAND = "#e6e5e0"

# ---------------------------------------------------------------------------
# A. NSO Health Behaviour 2021, printed figures (SOURCED)
# ---------------------------------------------------------------------------
# Table 2, printed p. VI (PDF 7): drank in past 12 months, % of age group.
T2_PAST12 = {"all": 28.0, "25-44": 36.5, "45-59": 32.4, "60+": 15.0, "men": 46.4, "women": 10.8,
             "15-19": 9.0, "20-24": 31.6}

# Table 6, printed p. 25 (PDF 44): counts of persons aged 15+, past 12 months.
T6 = {"all_total": 57021842, "all_past12": 15966498,
      "25-44_total": 19343114, "25-44_past12": 7066102,
      "45-59_total": 15484363, "45-59_past12": 5019512,
      "men_total": 27495370, "men_past12": 12768859,
      "women_total": 29526472, "women_past12": 3197639}

# Table 50, annex printed p. 140 (PDF 159): counts of persons aged 6+ by frequency of bottled
# non-alcoholic beverage consumption, read from the report's text layer (reversed-digit cells)
# and matched to the rotated page image. Keys: no consumption, 1-3 days/month, 1-2 days/week,
# 3-4 days/week, 5-6 days/week, everyday, unknown (excluded from printed rates), total.
T50 = {
    "all":   dict(total=63878199, unknown=816645, no=24992944, m1_3=4665584, w1_2=11872066,
                  w3_4=9629333, w5_6=2910493, everyday=8991132),
    "6-14":  dict(total=6856357, unknown=79931, no=2420987, m1_3=365054, w1_2=1609237,
                  w3_4=1340385, w5_6=356533, everyday=684230),
    "15-24": dict(total=9163628, unknown=159268, no=2560625, m1_3=618916, w1_2=2137898,
                  w3_4=1972372, w5_6=503570, everyday=1210979),
    "25-44": dict(total=19343114, unknown=340994, no=5856735, m1_3=1306885, w1_2=3941303,
                  w3_4=3324297, w5_6=1106829, everyday=3466072),
    "45-59": dict(total=15484363, unknown=178620, no=6256241, m1_3=1322738, w1_2=2583023,
                  w3_4=2022996, w5_6=669720, everyday=2451026),
    "60+":   dict(total=13030737, unknown=57833, no=7898356, m1_3=1051991, w1_2=1600605,
                  w3_4=969284, w5_6=273841, everyday=1178826),
    "men":   dict(total=31001044, unknown=419615, no=10385305, m1_3=2123226, w1_2=5791169,
                  w3_4=5150361, w5_6=1717796, everyday=5413571),
    "women": dict(total=32877155, unknown=397030, no=14607639, m1_3=2542358, w1_2=6080897,
                  w3_4=4478972, w5_6=1192697, everyday=3577561),
}

# Table 20, printed p. 41 (PDF 60): bottled non-alcoholic beverages, printed %, unknown excluded.
T20 = {
    "all":   dict(no=39.6, m1_3=7.4, w1_2=18.8, w3_4=15.3, w5_6=4.6, everyday=14.3),
    "6-14":  dict(no=35.7, m1_3=5.4, w1_2=23.7, w3_4=19.8, w5_6=5.3, everyday=10.1),
    "15-24": dict(no=28.5, m1_3=6.9, w1_2=23.7, w3_4=21.9, w5_6=5.6, everyday=13.4),
    "25-44": dict(no=30.9, m1_3=6.9, w1_2=20.7, w3_4=17.5, w5_6=5.8, everyday=18.2),
    "45-59": dict(no=40.9, m1_3=8.6, w1_2=16.9, w3_4=13.2, w5_6=4.4, everyday=16.0),
    "60+":   dict(no=60.9, m1_3=8.1, w1_2=12.3, w3_4=7.5, w5_6=2.1, everyday=9.1),
}

# Table 22, printed p. 42 (PDF 61): drinks with sugar substitutes (intensive sweetener), printed %.
T22 = {
    "all":   dict(no=95.9, m1_3=1.3, w1_2=1.2, w3_4=0.6, w5_6=0.2, everyday=0.8),
    "6-14":  dict(no=97.9, m1_3=0.5, w1_2=0.9, w3_4=0.3, w5_6=0.1, everyday=0.3),
    "15-24": dict(no=96.6, m1_3=1.1, w1_2=1.3, w3_4=0.5, w5_6=0.2, everyday=0.3),
    "25-44": dict(no=95.3, m1_3=1.7, w1_2=1.5, w3_4=0.7, w5_6=0.2, everyday=0.6),
    "45-59": dict(no=95.7, m1_3=1.3, w1_2=1.2, w3_4=0.6, w5_6=0.2, everyday=1.0),
    "60+":   dict(no=95.4, m1_3=1.3, w1_2=1.1, w3_4=0.7, w5_6=0.3, everyday=1.2),
}

# ---------------------------------------------------------------------------
# B. NSO Social Indicators 2025, Table 4.6.2, % of persons 15+ currently drinking.
#    SOURCED from https://www.nso.go.th/public/e-book/Indicators-Social/Social-Indicators-2025/284/
#    read with WebFetch. The text layer is garbled; values were reconstructed by row and column
#    and checked against the 2021 column (36.5, 9.0, 31.6, 32.4, 46.4, 10.8 all match the printed
#    2021 report). The printed page image has not been read; this is a stated limit.
# ---------------------------------------------------------------------------
SI = {
    "2024": {"all": 35.2, "men": 55.7, "women": 16.7, "men_25-44": 68.6, "men_45-59": 65.4,
             "women_25-44": 25.2, "women_45-59": 19.9, "both_25-44": 46.9, "both_45-59": 41.9,
             "both_60+": 18.3},
    "2021": {"all": 28.0, "men": 46.4, "women": 10.8, "men_25-44": 58.1, "men_45-59": 54.6,
             "women_25-44": 15.2, "women_45-59": 12.2, "both_25-44": 36.5, "both_45-59": 32.4},
}

# Population, men aged 25-44 (DOPA Nov 2568, from rework/47; not re-read here).
DOPA_MEN_25_34_M = 4.76
DOPA_MEN_35_44_M = 4.75

# ---------------------------------------------------------------------------
# C. Ad-cost and reach inputs
# ---------------------------------------------------------------------------
# Phoenix Media, "The Costs of Facebook, Google and LINE Ads in Thailand for 2025"
# https://www.phoenixmedia.co.th/the-costs-of-facebook-google-and-line-ads-in-thailand-for-2025/
# (WebFetch). Agency's own client campaigns, mostly lead-gen and conversion; no sample or method.
PHOENIX_CPM_FB_2025 = 120.0   # THB per 1,000 impressions, Facebook 2025. PROXY (Thai market, agency)
PHOENIX_CPM_FB_2024 = 110.0   # THB per 1,000 impressions, Facebook 2024. SOURCED (same page)
PHOENIX_CPC_FBIG_2025 = 11.5  # THB per click, Facebook and Instagram combined, 2025. PROXY
PHOENIX_CONV_FBIG_2025 = 0.0008  # conversion rate 0.08% (base not defined on the page). PROXY, low end

# ECDB, Thai beverages e-commerce, 2025 (WebFetch of
# https://ecdb.com/resources/sample-data/market/th/beverages). No sample or method given; the page
# pattern repeats across categories, so it is low confidence. Conversion rate not shown (locked).
ECDB_ADD_TO_CART_PCT = (11.5, 12.0)      # session add-to-cart rate. PROXY, low confidence
ECDB_CART_ABANDON_PCT = (70.5, 71.0)     # cart abandonment rate. PROXY, low confidence

# Affect Group, Meta Ads audience for Thailand, 18+ (WebFetch of
# https://affectgroup.com/blog/thailand-meta-ads-audience-by-age-and-gender-2026/, dated 7 April 2026).
# Counts of accounts (potential reach), not unique persons. Data via Meta Marketing API.
META_AUDIENCE_M = {"18+": 52.1, "men": 24.9, "women": 27.2, "25-34": 18.3, "35-44": 11.1}

# CP All, year-end 2025 snapshot (WebFetch of
# https://lssmedia.setlink.set.or.th/2025/YE/CPALL-YE68-ListedCompanySnapshot-EN.html). SOURCED.
CPALL_STORES_2025 = 15945
CPALL_OPENED_2025 = 700

# Contribution per serving at mid margins, from rework/53 (ASSUMPTION margins 30% and 15%).
NET_TO_BRAND_THB = 8.93       # retail THB 15 x 0.595
COST_LOW_THB = 2.12           # unit cost, low case (rework/53)
COST_HIGH_THB = 5.32          # unit cost, high case (rework/53)
CONTRIB_LOW_COST = NET_TO_BRAND_THB - COST_LOW_THB    # 6.81
CONTRIB_HIGH_COST = NET_TO_BRAND_THB - COST_HIGH_THB  # 3.61

# ---------------------------------------------------------------------------
# D. Funnel inputs (per 1,000 impressions)
# ---------------------------------------------------------------------------
CPM_BASE = PHOENIX_CPM_FB_2025
CPM_LO, CPM_HI = 80.0, 180.0                     # ASSUMPTION band around the PROXY (about -33%, +50%)
CTR_BASE = CPM_BASE / (1000.0 * PHOENIX_CPC_FBIG_2025)   # DERIVED: CTR = CPM / (1000 x CPC) = 1.04%
CTR_LO, CTR_HI = 0.007, 0.012                    # ASSUMPTION band
LPR_LOW = PHOENIX_CONV_FBIG_2025                 # PROXY: agency conversion 0.08% (low end)
LPR_BASE = 0.010                                 # ASSUMPTION: click to first purchase
LPR_HIGH = (sum(ECDB_ADD_TO_CART_PCT) / 2 / 100.0) * (1 - (sum(ECDB_CART_ABANDON_PCT) / 2 / 100.0))
# DERIVED: add-to-cart x (1 - abandonment) = 0.1175 x 0.2925 = 3.44% (PROXY, high end)
REP_LO, REP_BASE, REP_HI = 0.15, 0.30, 0.40      # ASSUMPTION: share of first buyers who buy again
FREQ = 2.0                                       # ASSUMPTION: impressions per unique person (reach only)
RETAIL_SAMPLE_COST = {"low": 10.0, "base": 15.0, "high": 25.0}      # ASSUMPTION, THB per sample
RETAIL_SAMPLE_TO_TRIAL = {"low": 0.20, "base": 0.10, "high": 0.05}  # ASSUMPTION


def cpa_trial(cpm, ctr, lpr):
    """Cost per acquired (first-purchase) customer, THB. CPA = (CPM / 1000) / (CTR x LPR)."""
    return (cpm / 1000.0) / (ctr * lpr)


def pct(a, b):
    return 100.0 * a / b


def share_everyday(group, exclude_unknown=True):
    d = T50[group]
    denom = d["total"] - (d["unknown"] if exclude_unknown else 0)
    return 100.0 * d["everyday"] / denom


def weekly_plus(table, group):
    d = table[group]
    return d["w1_2"] + d["w3_4"] + d["w5_6"] + d["everyday"]


# ---------------------------------------------------------------------------
# 1. Verification of rework/47 and of the 46.9% and 68.6% values
# ---------------------------------------------------------------------------
verification = []


def check(item, record, printed_or_source, recomputed, status, note):
    verification.append({"item": item, "record_value": record, "printed_or_source": printed_or_source,
                         "recomputed": round(recomputed, 2) if isinstance(recomputed, float) else recomputed,
                         "status": status, "note": note})


check("Drank past 12 months, 25-44 (both sexes), 2021", 36.5, T2_PAST12["25-44"],
      pct(T6["25-44_past12"], T6["25-44_total"]), "holds",
      "Table 2 p. VI (PDF 7) and Table 6 p. 25 (PDF 44) agree.")
check("Drank past 12 months, 45-59 (both sexes), 2021", 32.4, T2_PAST12["45-59"],
      pct(T6["45-59_past12"], T6["45-59_total"]), "holds", "Table 2 and Table 6 agree.")
check("Drank past 12 months, men, 2021", 46.4, T2_PAST12["men"],
      pct(T6["men_past12"], T6["men_total"]), "holds", "Table 2 and Table 6 agree.")
check("Drank past 12 months, women, 2021", 10.8, T2_PAST12["women"],
      pct(T6["women_past12"], T6["women_total"]), "holds", "Table 2 and Table 6 agree.")
check("Bottled non-alcoholic drunk every day, 25-44", 17.9, T20["25-44"]["everyday"],
      share_everyday("25-44", exclude_unknown=False), "holds as a count ratio; printed rate differs",
      "17.9 = everyday / all persons 6+ in the group, including Unknown. The printed rate (Table 20) "
      "is 18.2 = everyday / persons with a known answer. The record should use 18.2.")
check("Bottled non-alcoholic drunk every day, 45-59", 15.8, T20["45-59"]["everyday"],
      share_everyday("45-59", exclude_unknown=False), "holds as a count ratio; printed rate differs",
      "Same denominator issue: printed 16.0; count with Unknown 15.8.")
check("Bottled non-alcoholic drunk every day, men", 17.5, "no printed rate (Table 50 counts only)",
      share_everyday("men", exclude_unknown=False), "holds as a count ratio",
      "Known-answer denominator gives 17.7. No printed sex-specific rate exists.")
check("Bottled non-alcoholic drunk every day, women", 10.9, "no printed rate (Table 50 counts only)",
      share_everyday("women", exclude_unknown=False), "holds as a count ratio",
      "Known-answer denominator gives 11.0.")
ratio_record = (36.5 * 17.9) / (32.4 * 15.8)
ratio_printed = (36.5 * 18.2) / (32.4 * 16.0)
check("Per-person ratio, 25-44 over 45-59 (drinking x everyday)", 1.28, "derived from printed rates",
      ratio_printed, "holds",
      f"Record inputs give {ratio_record:.3f}; printed inputs give {ratio_printed:.3f}. Direction and size unchanged.")
check("Men 25-44 drinking 68.6 (2024)", 68.6, "NSO Social Indicators 2025, Table 4.6.2 (WebFetch)",
      SI["2024"]["men_25-44"], "holds, men only; not in the 2021 report",
      "The 2021 report has no sex-by-age cell (Tables 2 and 6 cross only one dimension). The 2024 cell "
      "is from NSO Social Indicators 2025; printed page not yet read.")
check("Both sexes 25-44 drinking 46.9 (2024)", 46.9, "NSO Social Indicators 2025, Table 4.6.2 (WebFetch)",
      (SI["2024"]["men_25-44"] + SI["2024"]["women_25-44"]) / 2.0, "holds, both sexes; not in the 2021 report",
      "Equal-weight average of men 68.6 and women 25.2 gives 46.9, so the two values are consistent. "
      "The implied male weight is 0.50.")
w_2021 = (SI["2021"]["both_25-44"] - SI["2021"]["women_25-44"]) / (SI["2021"]["men_25-44"] - SI["2021"]["women_25-44"])
check("2021 cross-check: men 25-44 58.1 and women 15.2 average to 36.5", 36.5, "NSO Social Indicators 2025, 2021 column",
      (SI["2021"]["men_25-44"] + SI["2021"]["women_25-44"]) / 2.0, "consistent",
      f"Equal-weight average 36.65 against printed 36.5. Implied male weight {w_2021:.3f}. "
      "The 2021 column matches the printed 2021 report on every row checked.")

# Share of everyday bottled-drink consumers by age and sex (SOURCED counts, Table 50).
everyday_total = T50["all"]["everyday"]
share_25_44_everyday = 100.0 * T50["25-44"]["everyday"] / everyday_total
share_25_44_pop = 100.0 * T50["25-44"]["total"] / T50["all"]["total"]
share_men_everyday = 100.0 * T50["men"]["everyday"] / (T50["men"]["everyday"] + T50["women"]["everyday"])
share_men_pop = 100.0 * T50["men"]["total"] / (T50["men"]["total"] + T50["women"]["total"])

# ---------------------------------------------------------------------------
# 2. Persona cells (SOURCED, 2021 survey, as far as the measures allow)
# ---------------------------------------------------------------------------
persona_cells = {
    "sweet_bottled_everyday_pct": {g: T20[g]["everyday"] for g in T20},
    "sweet_bottled_weekly_plus_pct": {g: round(weekly_plus(T20, g), 1) for g in T20},
    "sugar_substitute_everyday_pct": {g: T22[g]["everyday"] for g in T22},
    "sugar_substitute_weekly_plus_pct": {g: round(weekly_plus(T22, g), 1) for g in T22},
    "share_25_44_of_everyday_bottled_drinkers_pct": round(share_25_44_everyday, 1),
    "share_25_44_of_population_6plus_pct": round(share_25_44_pop, 1),
    "share_men_of_everyday_bottled_drinkers_pct": round(share_men_everyday, 1),
    "share_men_of_population_6plus_pct": round(share_men_pop, 1),
    "prevalence_ratio_sugar_substitute_to_sweet_weekly_plus_25_44": round(
        weekly_plus(T22, "25-44") / weekly_plus(T20, "25-44"), 3),
    "note": "Prevalence ratios, not conditional probabilities. Sugar substitute and sweet bottled "
            "drinks are measured in the same survey but not cross-tabulated with each other.",
}

# Target pool for men 25-44 (DERIVED from repo and public figures; ASSUMPTION where marked).
men_25_44_pop_m = DOPA_MEN_25_34_M + DOPA_MEN_35_44_M
men_25_44_drinkers_m = men_25_44_pop_m * SI["2024"]["men_25-44"] / 100.0
men_share_meta = META_AUDIENCE_M["men"] / META_AUDIENCE_M["18+"]           # ASSUMPTION: sex split constant by age
men_25_44_meta_m = men_share_meta * (META_AUDIENCE_M["25-34"] + META_AUDIENCE_M["35-44"])
pool = {
    "men_25_44_population_million": round(men_25_44_pop_m, 2),
    "men_25_44_current_drinkers_million_2024": round(men_25_44_drinkers_m, 2),
    "men_25_44_meta_potential_reach_million": round(men_25_44_meta_m, 2),
    "basis": "Population: rework/47 (DOPA Nov 2568). Drinkers: 2024 cell 68.6 (NSO SI 2025). Meta: "
             "Affect Group counts with an ASSUMPTION that the male share is constant across ages.",
}

# ---------------------------------------------------------------------------
# 3. Funnel and cost per acquired customer
# ---------------------------------------------------------------------------
def scenario(name, cpm, ctr, lpr, rep, label):
    cpc = cpm / (1000.0 * ctr)
    cpa = cpc / lpr
    return {"name": name, "cpm_thb": cpm, "ctr": round(ctr, 6), "cpc_thb": round(cpc, 2),
            "lpr": round(lpr, 6), "cpa_trial_thb": round(cpa, 1), "repeat_rate": rep,
            "cpa_repeat_thb": round(cpa / rep, 1),
            "servings_to_recover_at_high_cost": round(cpa / CONTRIB_HIGH_COST, 1),
            "servings_to_recover_at_low_cost": round(cpa / CONTRIB_LOW_COST, 1),
            "label": label}


scenarios = [
    scenario("S1 agency-implied conversion", CPM_BASE, CTR_BASE, LPR_LOW, REP_BASE,
             "Paid social; LPR 0.08% is the Phoenix conversion (base undefined). PROXY"),
    scenario("S2 base case", CPM_BASE, CTR_BASE, LPR_BASE, REP_BASE,
             "Paid social; LPR 1.0% is ASSUMPTION. CPM and CTR are PROXY and DERIVED"),
    scenario("S3 beverage-cart benchmark", CPM_BASE, CTR_BASE, LPR_HIGH, REP_BASE,
             "Paid social; LPR 3.4% from ECDB cart funnel. PROXY, low confidence"),
]

retail_cases = {}
for k in ("low", "base", "high"):
    cpa_r = RETAIL_SAMPLE_COST[k] / RETAIL_SAMPLE_TO_TRIAL[k]
    retail_cases[k] = {"sample_cost_thb": RETAIL_SAMPLE_COST[k],
                       "sample_to_trial": RETAIL_SAMPLE_TO_TRIAL[k],
                       "cpa_trial_thb": round(cpa_r, 1),
                       "cpa_repeat_thb": round(cpa_r / REP_BASE, 1)}
retail_floor = {
    "stores_7eleven_2025": CPALL_STORES_2025,
    "cases": retail_cases,
    "label": "Floor only. Excludes listing fees, trade spend, distribution and shelf costs, which are "
             "not sourced. Sample cost and sample-to-trial rate are ASSUMPTION.",
}

# Break-even: the conversion needed for a paid click (CPC) to be recovered within k servings.
breakeven = {
    "cpc_thb": PHOENIX_CPC_FBIG_2025,
    "contribution_high_cost_thb": round(CONTRIB_HIGH_COST, 2),
    "lpr_needed_for_1_serving_payback": round(PHOENIX_CPC_FBIG_2025 / CONTRIB_HIGH_COST, 3),
    "lpr_needed_for_4_servings_payback": round(PHOENIX_CPC_FBIG_2025 / (4 * CONTRIB_HIGH_COST), 3),
    "reading": "A paid click costs more than one serving's contribution. Recovering the cost of one "
               "first purchase needs a click-to-purchase rate of about 320% (impossible). Recovering it "
               "over four servings still needs about 80%.",
}

# ---------------------------------------------------------------------------
# 4. Monte Carlo over all funnel inputs (independent triangular draws)
# ---------------------------------------------------------------------------
rng = np.random.default_rng(SEED)
cpm_d = rng.triangular(CPM_LO, CPM_BASE, CPM_HI, N)
ctr_d = rng.triangular(CTR_LO, CTR_BASE, CTR_HI, N)
lpr_d = rng.triangular(LPR_LOW, LPR_BASE, LPR_HIGH, N)
rep_d = rng.triangular(REP_LO, REP_BASE, REP_HI, N)
cpa_d = cpa_trial(cpm_d, ctr_d, lpr_d)
cpa_rep_d = cpa_d / rep_d


def quant(x):
    return {f"p{p}": round(float(np.percentile(x, p)), 1) for p in (5, 50, 95)}


monte_carlo = {
    "seed": SEED, "draws": N, "distribution": "triangular (low, mode, high) for CPM, CTR, LPR, repeat; independent",
    "cpa_trial_thb": quant(cpa_d),
    "cpa_repeat_thb": quant(cpa_rep_d),
    "share_of_draws_cpa_below_one_serving_high_cost": round(float(np.mean(cpa_d < CONTRIB_HIGH_COST)), 4),
    "share_of_draws_cpa_below_one_serving_low_cost": round(float(np.mean(cpa_d < CONTRIB_LOW_COST)), 4),
    "share_of_draws_cpa_below_1000_thb": round(float(np.mean(cpa_d < 1000)), 3),
}
mc_inputs = {
    "cpm_thb": quant(cpm_d), "ctr_pct": {f"p{p}": round(float(np.percentile(ctr_d, p)) * 100, 3) for p in (5, 50, 95)},
    "lpr_pct": {f"p{p}": round(float(np.percentile(lpr_d, p)) * 100, 3) for p in (5, 50, 95)},
    "repeat_pct": {f"p{p}": round(float(np.percentile(rep_d, p)) * 100, 1) for p in (5, 50, 95)},
}

# ---------------------------------------------------------------------------
# 5. Levers: one at a time across the stated ranges, others at base
# ---------------------------------------------------------------------------
base = {"cpm": CPM_BASE, "ctr": CTR_BASE, "lpr": LPR_BASE, "rep": REP_BASE}
base_cpa = cpa_trial(base["cpm"], base["ctr"], base["lpr"])
lever_defs = [
    ("Click-to-first-purchase rate (offer, price, product page, marketplace listing)", "lpr", LPR_LOW, LPR_HIGH,
     "ECDB cart funnel and Phoenix conversion bound the range. PROXY"),
    ("Cost per mille (placement, audience, bidding)", "cpm", CPM_LO, CPM_HI, "ASSUMPTION band around PROXY"),
    ("Click-through rate (creative, hook, targeting)", "ctr", CTR_LO, CTR_HI, "ASSUMPTION band around DERIVED"),
]
tornado_trial = []
for label, key, lo, hi, src in lever_defs:
    vals = {}
    for tag, v in (("low", lo), ("high", hi)):
        p = dict(base)
        p[key] = v
        vals[tag] = cpa_trial(p["cpm"], p["ctr"], p["lpr"])
    swing = abs(vals["high"] - vals["low"])
    tornado_trial.append({"lever": label, "input": key, "range": [lo, hi], "cpa_at_low_input": round(vals["low"], 1),
                          "cpa_at_high_input": round(vals["high"], 1), "swing_thb": round(swing, 1),
                          "source": src})
tornado_trial.sort(key=lambda r: -r["swing_thb"])
tornado_repeat = {
    "lever": "Repeat rate (retention, pack size, subscription)",
    "range": [REP_LO, REP_HI],
    "cpa_repeat_at_low": round(base_cpa / REP_LO, 1),
    "cpa_repeat_at_high": round(base_cpa / REP_HI, 1),
    "swing_thb": round(base_cpa / REP_LO - base_cpa / REP_HI, 1),
    "note": "Changes cost per repeat customer only. Does not change cost per first purchase.",
}

# ---------------------------------------------------------------------------
# 6. Write results JSON
# ---------------------------------------------------------------------------
results = {
    "question": "Cost per acquired customer for the targeted group, Thailand, desk proxy basis",
    "formula": "CPA_trial = (CPM / 1000) / (CTR x LPR) = CPC / LPR; CPA_repeat = CPA_trial / repeat rate",
    "labels": {"SOURCED": "printed page or URL read in this study", "PROXY": "stands in for what is needed",
               "ASSUMPTION": "no source; range given", "DERIVED": "arithmetic on the labelled inputs"},
    "inputs": {
        "CPM_thb_per_1000": {"base": CPM_BASE, "range": [CPM_LO, CPM_HI], "label": "PROXY (Phoenix 2025, FB); range ASSUMPTION"},
        "CPC_thb": {"base": PHOENIX_CPC_FBIG_2025, "label": "PROXY (Phoenix 2025, FB and IG combined)"},
        "CTR": {"base": round(CTR_BASE, 5), "range": [CTR_LO, CTR_HI], "label": "DERIVED (CPM / (1000 x CPC)); range ASSUMPTION"},
        "LPR": {"low": LPR_LOW, "base": LPR_BASE, "high": round(LPR_HIGH, 5),
                "label": "low PROXY (Phoenix 0.08%); base ASSUMPTION; high PROXY (ECDB, low confidence, derived)"},
        "repeat_rate": {"range": [REP_LO, REP_BASE, REP_HI], "label": "ASSUMPTION"},
        "frequency": {"value": FREQ, "label": "ASSUMPTION (reach only; not in CPA)"},
        "contribution_per_serving_thb": {"high_cost": round(CONTRIB_HIGH_COST, 2), "low_cost": round(CONTRIB_LOW_COST, 2),
                                         "label": "DERIVED from rework/53 (margins ASSUMPTION)"},
        "meta_audience_million": {**META_AUDIENCE_M, "label": "PROXY (Affect Group, potential reach in accounts)"},
        "7eleven_stores_2025": {"value": CPALL_STORES_2025, "label": "SOURCED (CP All, YE2025)"},
    },
    "verification_rework47": verification,
    "persona_cells": persona_cells,
    "pool_men_25_44": pool,
    "scenarios": scenarios,
    "retail_floor": retail_floor,
    "breakeven": breakeven,
    "monte_carlo": monte_carlo,
    "monte_carlo_inputs": mc_inputs,
    "tornado_trial": tornado_trial,
    "tornado_repeat": tornado_repeat,
    "limits": [
        "No respondents, no outside contact. Desk proxy only.",
        "Ad benchmarks are one Thai agency's client data with no stated method; the Meta audience counts are third-party with no stated date for the estimate.",
        "The 2021 survey measures bottled non-alcoholic drinks (sweet group, per the report's text), drinks with sugar substitutes, and alcohol. It does not measure sugar-sweetened drinking as such, and it has no sodium or sparkling-water question.",
        "2024 sex-by-age drinking cells come from a garbled text layer; printed-page image check still needed.",
        "No Thai FMCG channel share was found (Kantar page gave no percentages), so the retail route is a floor only.",
        "Persona fit (the match between the cube and the target) is folded into the click-to-purchase rate; it is not measured.",
    ],
}
os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
with open(OUT_JSON, "w", encoding="utf-8") as fh:
    json.dump(results, fh, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# 7. Chart: cost per acquired customer by scenario (log scale)
# ---------------------------------------------------------------------------
s1, s2, s3 = scenarios[0]["cpa_trial_thb"], scenarios[1]["cpa_trial_thb"], scenarios[2]["cpa_trial_thb"]
mc_med = monte_carlo["cpa_trial_thb"]["p50"]
mc_lo, mc_hi = monte_carlo["cpa_trial_thb"]["p5"], monte_carlo["cpa_trial_thb"]["p95"]
r_lo = retail_cases["low"]["cpa_trial_thb"]
r_base = retail_cases["base"]["cpa_trial_thb"]
r_hi = retail_cases["high"]["cpa_trial_thb"]

fig, ax = plt.subplots(figsize=(9.6, 4.9), dpi=160)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.axvspan(CONTRIB_HIGH_COST, CONTRIB_LOW_COST, color=BAND, zorder=0)
ax.text(np.sqrt(CONTRIB_HIGH_COST * CONTRIB_LOW_COST), 4.62, "one serving's contribution\nTHB 3.6 to 6.8",
        ha="center", va="bottom", fontsize=8, color=INK2)

rows = [
    (4, "Paid social, agency conversion (0.08%)", s1, None, None, f"THB {s1:,.0f}"),
    (3, "Paid social, base case (1.0% to purchase)", s2, None, None, f"THB {s2:,.0f}"),
    (2, "Paid social, beverage-cart benchmark (3.4%)", s3, None, None, f"THB {s3:,.0f}"),
    (1, "Paid social, all inputs (Monte Carlo)", mc_med, mc_lo, mc_hi,
     f"THB {mc_med:,.0f} median\n(P5 {mc_lo:,.0f} to P95 {mc_hi:,.0f})"),
    (0, "7-Eleven sampling floor (no trade costs)", r_base, r_lo, r_hi,
     f"THB {r_base:,.0f} (range {r_lo:,.0f} to {r_hi:,.0f})"),
]
for y, label, val, lo, hi, text in rows:
    if lo is not None:
        ax.hlines(y, lo, hi, color=BLUE, lw=2.2, alpha=0.55, zorder=2)
        ax.plot([lo, hi], [y, y], "|", color=BLUE, ms=11, zorder=2)
    ax.plot(val, y, "o", color=BLUE, ms=8, zorder=3)
    anchor = hi if hi is not None else val
    ax.annotate(text, (anchor, y), xytext=(10, 0), textcoords="offset points",
                va="center", fontsize=9, color=INK)

ax.set_xscale("log")
ax.set_xlim(2, 40000)
ax.set_ylim(-0.6, 5.1)
ax.set_yticks([r[0] for r in rows])
ax.set_yticklabels([r[1] for r in rows], fontsize=9, color=INK)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.set_xticks([10, 100, 1000, 10000])
ax.tick_params(axis="x", labelsize=9, colors=INK2)
ax.set_xlabel("Cost per acquired (first-purchase) customer, THB, log scale", fontsize=9, color=INK2)
ax.grid(axis="x", color=GRID, lw=0.7, zorder=1)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(axis="y", length=0)
fig.suptitle("Cost per acquired customer by scenario (desk proxy, no respondents)",
             x=0.02, ha="left", fontsize=12, color=INK, y=0.985)
fig.text(0.02, 0.02,
         "Paid social: Phoenix Media 2025 CPM THB 120 and CPC THB 11.5 (PROXY); click-to-purchase, repeat "
         "and CPM band are ASSUMPTION.\nSource detail and gaps: rework/55_consumer_persona_and_acquisition.md",
         fontsize=7.5, color=INK2, ha="left", va="bottom")
fig.subplots_adjust(left=0.31, right=0.97, top=0.86, bottom=0.2)
os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
fig.savefig(OUT_PNG, dpi=160, facecolor=SURFACE, metadata={"Software": None})
plt.close(fig)

# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------
print("wrote", OUT_JSON)
print("wrote", OUT_PNG)
print(f"CTR base {CTR_BASE*100:.3f}%  LPR high {LPR_HIGH*100:.2f}%  CPC {PHOENIX_CPC_FBIG_2025}")
for s in scenarios:
    print(f"{s['name']:<32} CPA trial {s['cpa_trial_thb']:>10,.1f}  per repeat {s['cpa_repeat_thb']:>10,.1f}")
print("retail floor (low/base/high):", retail_cases["low"]["cpa_trial_thb"],
      retail_cases["base"]["cpa_trial_thb"], retail_cases["high"]["cpa_trial_thb"])
print("Monte Carlo CPA trial P5/P50/P95:", monte_carlo["cpa_trial_thb"])
print("Share of draws below one serving (high cost):", monte_carlo["share_of_draws_cpa_below_one_serving_high_cost"])
print("Pool men 25-44:", pool)
print("Persona cells 25-44 everyday sweet:", T20["25-44"]["everyday"], " sugar-sub everyday:", T22["25-44"]["everyday"])
print("Share 25-44 of everyday bottled drinkers %:", round(share_25_44_everyday, 1),
      " men share of everyday %:", round(share_men_everyday, 1))
for v in verification:
    print(f"{v['item'][:60]:<60} record {v['record_value']}  recomputed {v['recomputed']}  {v['status']}")
