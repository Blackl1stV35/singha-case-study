"""KOL campaign pilot model (T16, 20 October 2026).

Reads no files. Every input is written below with its tier and source note. Writes
rework/screen/kol_campaign_model_results.json. Fixed seed. Light memory (numpy, 20,000 draws).

Tiers: S secondary source read; P primary; PROXY stand-in; ASSUMPTION chosen for the model; DERIVED arithmetic.
Run:  python rework/screen/kol_campaign_model.py
"""
import json
import math
import os

import numpy as np

SEED = 20261020
N_DRAWS = 20000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kol_campaign_model_results.json")

# ---------------------------------------------------------------- inputs
FX = 33.55  # THB per USD, Bank of Thailand midpoint 15 October 2026 (P; DERIVED midpoint), rework/raw/bot_fx_primary_2026-10-15.md

# Influencer Marketing Hub rate cheat sheet, read 20 Oct 2026 (S, global PROXY), USD per sponsored deliverable
FEE_USD = {
    "tiktok": {"nano": (50, 200), "micro": (200, 800), "mid": (800, 800), "macro": (800, 5000), "mega": (5000, 50000)},
    "youtube": {"nano": (20, 200), "micro": (200, 1000), "mid": (1000, 10000), "macro": (10000, 20000), "mega": (20000, 50000)},
}
# TikTok "mid" is not listed by the source; the shared boundary of the micro upper and macro lower bound (USD 800) is used (ASSUMPTION).

# Existing pilot inputs (rework/submission/06 and 10; rework/55)
CPC_META = 11.5          # THB per click, Phoenix Media 2025 (S, PROXY)
CPM_META = 120.0         # THB per 1,000 impressions, Phoenix Media 2025 (S, PROXY)
CPM_BAND = (80.0, 180.0)  # ASSUMPTION band used in rework/55
CPV_META = 4.00          # THB per video view, Phoenix Media 2025 (S, PROXY)
LPR_BASE = 0.010         # click to first purchase (ASSUMPTION; rework/10)
LPR_LOW = 0.0008         # Phoenix conversion 0.08 percent (S, PROXY)
LPR_HIGH = 0.03437       # ECDB add-to-cart derived (PROXY, low confidence; rework/55)
CONTRIB_BASE = 4.91      # THB per cube, six-cube pack (DERIVED; rework/10)
CONTRIB_FLOOR = 3.51     # THB per cube floor (DERIVED; rework/10)
COST_PER_CUBE = 4.09     # THB, six-cube pack (DERIVED; rework/10), excludes binder, filler, flavour
SHELF_PER_CUBE = 15.0
CUBES_PER_CARTON = 6
SAMPLE_COST = 15.0       # THB per in-store sample (ASSUMPTION; rework/10)
SAMPLE_TO_TRIAL = 0.10   # (ASSUMPTION; rework/10)

# Campaign design (proposal; ASSUMPTION unless noted). fee_point "none" means product kit plus commission on sale, no flat fee.
MIX = [
    {"tier": "nano", "platform": "tiktok", "creators": 16, "posts_each": 2, "fee_point": "none"},
    {"tier": "micro", "platform": "tiktok", "creators": 4, "posts_each": 2, "fee_point": "low"},
    {"tier": "mid", "platform": "youtube", "creators": 1, "posts_each": 1, "fee_point": "low"},
]
COMMISSION_RATE = 0.10    # of shelf price of a six-cube carton, paid on sale (ASSUMPTION; no source)
KIT_CUBES = 12            # per creator (two cartons) (ASSUMPTION)
GIVEAWAY_CUBES = 600      # (ASSUMPTION)
AMPLIFY_SPEND = 60000.0   # conditional paid amplification, Route B (ASSUMPTION)
ROUTE_A_SAMPLES = 3000    # (ASSUMPTION)
CONTINGENCY = 0.10        # (ASSUMPTION)
COMMISSION_RESERVE = 10000.0  # cap set aside for pay-on-sale commissions (ASSUMPTION)

# Views per post (ASSUMPTION), median with 5th and 95th percentile; the mid-tier YouTube value is anchored on the vidIQ latest-video ratios below
VIEWS = {
    "nano": (1000, 300, 4000),
    "micro": (8000, 2500, 25000),
    "mid": (44000, 8000, 110000),
}
CTR_VIEW_TO_CLICK = (0.010, 0.003, 0.025)  # median, P5, P95 (ASSUMPTION; Meta CPM over CPC gives 1.04 percent per impression, DERIVED)

COMM = COMMISSION_RATE * SHELF_PER_CUBE * CUBES_PER_CARTON
res = {"meta": {"seed": SEED, "draws": N_DRAWS, "fx_thb_per_usd": FX}}
# Benchmark fee table converted to baht (arithmetic only): low and high per sponsored deliverable
res["fee_table_thb"] = {plat: {tier_: [lo * FX, hi * FX] for tier_, (lo, hi) in tiers_.items()} for plat, tiers_ in FEE_USD.items()}


def fee_thb(platform, tier, point):
    if point == "none":
        return 0.0
    lo, hi = FEE_USD[platform][tier]
    usd = {"low": lo, "mid": (lo + hi) / 2.0, "high": hi}[point]
    return usd * FX


# ---------------------------------------------------------------- budget lines
lines = []
fees_total = {}
for m in MIX:
    f = fee_thb(m["platform"], m["tier"], m["fee_point"])
    posts = m["creators"] * m["posts_each"]
    fees_total[m["tier"]] = {"creators": m["creators"], "posts": posts, "fee_per_post_thb": f,
                             "amount_thb": posts * f,
                             "benchmark_usd_range": FEE_USD[m["platform"]][m["tier"]]}
    if m["fee_point"] == "none":
        lines.append({"line": "Creator fees, %s %s" % (m["tier"], m["platform"]),
                      "arithmetic": "no flat fee: product kit plus commission on sale (see the kit and commission lines)",
                      "thb": 0.0, "tier_label": "ASSUMPTION (offer structure)"})
    else:
        lines.append({"line": "Creator fees, %s %s" % (m["tier"], m["platform"]),
                      "arithmetic": "%d posts x THB %.1f (USD %d x 33.55)" % (posts, f, FEE_USD[m["platform"]][m["tier"]][0]),
                      "thb": posts * f, "tier_label": "PROXY (global benchmark, lower bound, converted at 33.55)"})
fees_sum = sum(x["amount_thb"] for x in fees_total.values())
n_creators = sum(m["creators"] for m in MIX)
seed_cubes = n_creators * KIT_CUBES + GIVEAWAY_CUBES
seeding = seed_cubes * COST_PER_CUBE
lines.append({"line": "Product kits and giveaways",
              "arithmetic": "(%d creators x %d cubes + %d giveaway cubes) x THB %.2f" % (n_creators, KIT_CUBES, GIVEAWAY_CUBES, COST_PER_CUBE),
              "thb": seeding, "tier_label": "DERIVED (cost per cube excludes binder, filler, flavour)"})
lines.append({"line": "Pay-on-sale commission reserve",
              "arithmetic": "cap; %.0f percent of the THB %.0f carton price, THB %.0f per sale" % (COMMISSION_RATE * 100, SHELF_PER_CUBE * CUBES_PER_CARTON, COMM),
              "thb": COMMISSION_RESERVE, "tier_label": "ASSUMPTION"})
lines.append({"line": "Paid amplification of creator posts (Route B), conditional",
              "arithmetic": "THB %.0f (about %.0f clicks at THB %.1f)" % (AMPLIFY_SPEND, AMPLIFY_SPEND / CPC_META, CPC_META),
              "thb": AMPLIFY_SPEND, "tier_label": "ASSUMPTION spend; cost per click PROXY"})
route_a = ROUTE_A_SAMPLES * SAMPLE_COST
lines.append({"line": "Route A in-store samples", "arithmetic": "%d samples x THB %.0f" % (ROUTE_A_SAMPLES, SAMPLE_COST),
              "thb": route_a, "tier_label": "ASSUMPTION"})
subtotal = sum(l["thb"] for l in lines)
contingency = subtotal * CONTINGENCY
lines.append({"line": "Contingency", "arithmetic": "%.0f percent of subtotal THB %.0f" % (CONTINGENCY * 100, subtotal),
              "thb": contingency, "tier_label": "ASSUMPTION"})
total = subtotal + contingency
res["budget_lines"] = lines
sens_fee = {}
for point in ("low", "mid", "high"):
    s = 0.0
    for m in MIX:
        if m["fee_point"] == "none":
            continue
        s += m["creators"] * m["posts_each"] * fee_thb(m["platform"], m["tier"], point)
    sens_fee[point] = s
res["budget"] = {
    "subtotal_thb": subtotal, "contingency_thb": contingency, "total_thb": total,
    "flat_fee_total_thb": fees_sum, "flat_fee_share_of_total": fees_sum / total,
    "share_of_500k_fixed_cost_base": total / 500000.0,
    "share_of_250k_fixed_cost_grid_low": total / 250000.0,
    "creators_total": n_creators, "posts_total": sum(x["posts"] for x in fees_total.values()),
    "by_tier": fees_total,
    "conditional_amplification_thb": AMPLIFY_SPEND,
    "total_without_amplification_thb": (subtotal - AMPLIFY_SPEND) * (1 + CONTINGENCY),
    "flat_fee_total_by_benchmark_point_thb": sens_fee,
    "total_if_fees_at_benchmark_mid_thb": (subtotal - fees_sum + sens_fee["mid"]) * (1 + CONTINGENCY),
    "total_if_fees_at_benchmark_high_thb": (subtotal - fees_sum + sens_fee["high"]) * (1 + CONTINGENCY),
    "one_tiktok_mega_post_lowest_fee_share_of_total": fee_thb("tiktok", "mega", "low") / total,
    "one_youtube_macro_video_lowest_fee_share_of_total": fee_thb("youtube", "macro", "low") / total,
}

# ---------------------------------------------------------------- contribution and break-even
carton_contrib_base = CONTRIB_BASE * CUBES_PER_CARTON
carton_contrib_floor = CONTRIB_FLOOR * CUBES_PER_CARTON
paid_cpa = CPC_META / LPR_BASE
res["unit"] = {
    "carton_contribution_base_thb": carton_contrib_base,
    "carton_contribution_floor_thb": carton_contrib_floor,
    "carton_shelf_price_thb": SHELF_PER_CUBE * CUBES_PER_CARTON,
    "commission_per_sale_thb": COMM,
    "kit_cost_per_creator_thb": KIT_CUBES * COST_PER_CUBE,
}
pb = {
    "cpa_base_thb": paid_cpa,
    "cubes_per_buyer_to_recover_at_4_91": paid_cpa / CONTRIB_BASE,
    "cubes_per_buyer_to_recover_at_3_51": paid_cpa / CONTRIB_FLOOR,
    "first_carton_share_of_cpa_base": carton_contrib_base / paid_cpa,
    "first_carton_share_of_cpa_floor": carton_contrib_floor / paid_cpa,
    "cpa_at_cpm_80_thb": (CPM_BAND[0] / CPM_META * CPC_META) / LPR_BASE,
    "cpa_at_cpm_180_thb": (CPM_BAND[1] / CPM_META * CPC_META) / LPR_BASE,
    "cpa_at_phoenix_conversion_0_08_pct_thb": CPC_META / LPR_LOW,
    "cpa_at_ecdb_proxy_3_44_pct_thb": CPC_META / LPR_HIGH,
    "clicks_from_amplification_budget": AMPLIFY_SPEND / CPC_META,
    "first_purchases_from_amplification_budget_base": AMPLIFY_SPEND / CPC_META * LPR_BASE,
    "stop_ceiling_cpa_thb": paid_cpa * 1.5,
    "lpr_needed_for_carton_to_cover_click_base": CPC_META / carton_contrib_base,
    "lpr_needed_for_carton_to_cover_click_floor": CPC_META / carton_contrib_floor,
}
for rep, label in ((0.30, "target_30"), (0.15, "floor_15")):
    cubes = CUBES_PER_CARTON * (1 + rep)
    pb["value_per_buyer_in_pilot_%s" % label] = {"cubes_per_buyer": cubes, "contribution_base_thb": cubes * CONTRIB_BASE,
                                                  "contribution_floor_thb": cubes * CONTRIB_FLOOR}
# other conversion cases from the existing record (rework/55): cubes per buyer to recover
pb["cubes_per_buyer_at_ecdb_proxy_lpr"] = {"at_4_91": (CPC_META / LPR_HIGH) / CONTRIB_BASE, "at_3_51": (CPC_META / LPR_HIGH) / CONTRIB_FLOOR}
pb["cubes_per_buyer_at_phoenix_0_08_lpr"] = {"at_4_91": (CPC_META / LPR_LOW) / CONTRIB_BASE, "at_3_51": (CPC_META / LPR_LOW) / CONTRIB_FLOOR}
res["paid_social_route_b"] = pb
# effect on the valuation if the pilot budget were added on top of the THB 500,000 year-0 fixed cost (deck slide 10: NPV THB 0.88 million at 200,000 cubes)
NPV_BASE_MILLION = 0.88
res["valuation_check"] = {"npv_base_million_deck_slide_10": NPV_BASE_MILLION,
                          "year0_pilot_budget_million": total / 1e6,
                          "npv_if_pilot_added_on_top_million_undiscounted_year0": NPV_BASE_MILLION - total / 1e6,
                          "note": "Year 0 carries fixed cost undiscounted in the existing model; the pilot is read as drawn from that line, and this shows the effect if it were added instead."}

# ---------------------------------------------------------------- base funnel by tier (creator layer)
funnel = {}
tot_views = tot_clicks = tot_purch = tot_cost = tot_fees = 0.0
for m in MIX:
    t = m["tier"]
    posts = m["creators"] * m["posts_each"]
    views = posts * VIEWS[t][0]
    clicks = views * CTR_VIEW_TO_CLICK[0]
    purch = clicks * LPR_BASE
    fee_each = fee_thb(m["platform"], t, m["fee_point"])
    fees = posts * fee_each
    kit_cost = m["creators"] * KIT_CUBES * COST_PER_CUBE
    commission = purch * COMM
    cost_all = fees + kit_cost + commission
    cpv = (fees + kit_cost) / views
    funnel[t] = {"posts": posts, "views_base": views, "clicks": clicks, "first_purchases": purch,
                 "flat_fees_thb": fees, "kit_cost_thb": kit_cost, "commission_thb": commission,
                 "all_in_cost_thb": cost_all, "cost_per_1000_views_before_commission_thb": cpv * 1000.0,
                 "cost_per_view_before_commission_thb": cpv,
                 "cpa_all_in_thb": cost_all / purch,
                 "cubes_per_buyer_to_recover_at_4_91": cost_all / purch / CONTRIB_BASE,
                 "cubes_per_buyer_to_recover_at_3_51": cost_all / purch / CONTRIB_FLOOR}
    if fee_each > 0:
        funnel[t]["views_per_post_needed_to_match_paid_social_cpa"] = (fee_each + kit_cost / posts) / (paid_cpa * CTR_VIEW_TO_CLICK[0] * LPR_BASE)
        funnel[t]["max_all_in_cost_per_post_to_match_paid_social_thb"] = VIEWS[t][0] * CTR_VIEW_TO_CLICK[0] * LPR_BASE * paid_cpa
    tot_views += views; tot_clicks += clicks; tot_purch += purch; tot_cost += cost_all; tot_fees += fees
total_posts = sum(m["creators"] * m["posts_each"] for m in MIX)
funnel["all_creator_posts"] = {
    "posts": total_posts, "views_base": tot_views, "clicks": tot_clicks, "first_purchases": tot_purch,
    "flat_fees_thb": tot_fees, "all_in_cost_thb": tot_cost, "cpa_all_in_thb": tot_cost / tot_purch,
    "cubes_per_buyer_to_recover_at_4_91": tot_cost / tot_purch / CONTRIB_BASE,
    "cubes_per_buyer_to_recover_at_3_51": tot_cost / tot_purch / CONTRIB_FLOOR,
    "views_needed_for_100_first_buyers_at_base_ctr_and_lpr": 100.0 / (CTR_VIEW_TO_CLICK[0] * LPR_BASE),
    "views_per_post_needed_for_100_buyers": 100.0 / (CTR_VIEW_TO_CLICK[0] * LPR_BASE) / total_posts,
}
res["creator_funnel_base"] = funnel
res["comparison_cost_per_view"] = {
    "meta_cost_per_video_view_thb": CPV_META, "meta_cost_per_impression_thb": CPM_META / 1000.0,
    "note": "A Meta video view and a creator post's view are different measures; shown side by side only."}

# ---------------------------------------------------------------- pay-on-sale arithmetic (per creator)
kit = KIT_CUBES * COST_PER_CUBE
flat_two_nano_posts = 2 * fee_thb("tiktok", "nano", "low")
res["pay_on_sale"] = {
    "commission_per_first_carton_thb": COMM,
    "kit_cost_per_creator_thb": kit,
    "net_per_first_carton_base_thb": carton_contrib_base - COMM,
    "net_per_first_carton_floor_thb": carton_contrib_floor - COMM,
    "sales_per_creator_to_cover_kit_base": kit / (carton_contrib_base - COMM),
    "sales_per_creator_to_cover_kit_floor": kit / (carton_contrib_floor - COMM),
    "if_nano_were_paid_the_benchmark_low_flat_fee_for_two_posts": {
        "flat_fee_thb": flat_two_nano_posts,
        "sales_per_creator_to_cover_kit_and_fee_base": (kit + flat_two_nano_posts) / (carton_contrib_base - COMM),
        "sales_per_creator_to_cover_kit_and_fee_floor": (kit + flat_two_nano_posts) / (carton_contrib_floor - COMM)},
    "caveat": "Commission is on the shelf price; contribution is on the ex-factory basis (conservative). Marketplace or platform fees are not sourced and are not deducted.",
}

# ---------------------------------------------------------------- Monte Carlo
rng = np.random.default_rng(SEED)


def lognorm_from_q(med, p5, p95, size):
    mu = math.log(med)
    sig = (math.log(p95) - math.log(p5)) / (2 * 1.6449)
    return rng.lognormal(mu, sig, size)


def summ(a):
    a = np.asarray(a)
    return {"median": float(np.median(a)), "p5": float(np.percentile(a, 5)), "p95": float(np.percentile(a, 95)), "mean": float(np.mean(a))}


ctr = lognorm_from_q(*CTR_VIEW_TO_CLICK, N_DRAWS)
lpr = rng.triangular(LPR_LOW, LPR_BASE, LPR_HIGH, N_DRAWS)
cpm = rng.uniform(CPM_BAND[0], CPM_BAND[1], N_DRAWS)
mc = {"note": "Creator layer cost includes flat fees, product kits and commission on sale. Views per post, view-to-click and click-to-purchase are drawn independently."}
cost_tier, purch_tier = {}, {}
for m in MIX:
    t = m["tier"]
    posts = m["creators"] * m["posts_each"]
    v = lognorm_from_q(*VIEWS[t], N_DRAWS) * posts
    purch_tier[t] = v * ctr * lpr
    fixed = posts * fee_thb(m["platform"], t, m["fee_point"]) + m["creators"] * KIT_CUBES * COST_PER_CUBE
    cost_tier[t] = fixed + purch_tier[t] * COMM
all_p = sum(purch_tier.values())
all_c = sum(cost_tier.values())
cpa_all = all_c / np.maximum(all_p, 1e-9)
mc["creator_layer_first_purchases"] = summ(all_p)
mc["creator_layer_cpa_all_in_thb"] = summ(cpa_all)
for t in purch_tier:
    mc["cpa_all_in_thb_%s" % t] = summ(cost_tier[t] / np.maximum(purch_tier[t], 1e-9))
paid_cpa_draw = (cpm / CPM_META * CPC_META) / lpr
mc["paid_social_cpa_thb"] = summ(paid_cpa_draw)
mc["share_draws_creator_cpa_at_or_below_1150"] = float(np.mean(cpa_all <= paid_cpa))
mc["share_draws_creator_cpa_at_or_below_1725"] = float(np.mean(cpa_all <= paid_cpa * 1.5))
mc["share_draws_creator_cpa_at_or_below_first_carton_contribution_floor"] = float(np.mean(cpa_all <= carton_contrib_floor))
mc["share_draws_paid_social_cpa_at_or_below_1150"] = float(np.mean(paid_cpa_draw <= paid_cpa))
mc["share_draws_paid_social_cpa_at_or_below_1725"] = float(np.mean(paid_cpa_draw <= paid_cpa * 1.5))
mc["share_draws_paid_social_cpa_at_or_below_first_carton_contribution_floor"] = float(np.mean(paid_cpa_draw <= carton_contrib_floor))
mc["paid_social_cpa_min_thb"] = float(np.min(paid_cpa_draw))
amp_clicks = AMPLIFY_SPEND / (cpm / CPM_META * CPC_META)
amp_p = amp_clicks * lpr
mc["amplification_first_purchases"] = summ(amp_p)
tot_p = all_p + amp_p
tot_c = all_c + AMPLIFY_SPEND
mc["creator_plus_amplification_first_purchases"] = summ(tot_p)
mc["creator_plus_amplification_cpa_thb"] = summ(tot_c / np.maximum(tot_p, 1e-9))
mc["share_draws_100_or_more_first_purchases_creator_plus_amplification"] = float(np.mean(tot_p >= 100))
res["monte_carlo"] = mc


def n_for_halfwidth(p, h, z=1.96):
    return z * z * p * (1 - p) / (h * h)


res["repeat_read_sample"] = {
    "n_for_30pct_halfwidth_9pts": n_for_halfwidth(0.30, 0.09),
    "n_for_30pct_halfwidth_10pts": n_for_halfwidth(0.30, 0.10),
    "n_for_15pct_halfwidth_9pts": n_for_halfwidth(0.15, 0.09),
    "halfwidth_pts_at_25_buyers_p30": 100 * 1.96 * math.sqrt(0.30 * 0.70 / 25),
    "halfwidth_pts_at_50_buyers_p30": 100 * 1.96 * math.sqrt(0.30 * 0.70 / 50),
    "base_first_purchases_creator_layer": tot_purch,
    "base_first_purchases_amplification": AMPLIFY_SPEND / CPC_META * LPR_BASE,
    "route_a_trials_from_samples": ROUTE_A_SAMPLES * SAMPLE_TO_TRIAL,
    "route_a_cost_per_trial_thb": SAMPLE_COST / SAMPLE_TO_TRIAL,
}

# ---------------------------------------------------------------- ratios from public pages (DERIVED from saved readings)
# vidIQ latest-video views / subscribers, read 20 Oct 2026 (S); several are early-window counts, so they understate the final ratio
yt = {
    "BANKII": (10.6e6, 200.54e3), "PEACH EAT LAEK": (9.12e6, 239.81e3), "Jack Papho": (9.03e6, 1.96e6),
    "Tanaddak": (4.96e6, 14.11e3), "JIMSURIYA V.2": (3.25e6, 644.42e3), "Cinmhef": (1.46e6, 253.99e3),
    "NutApiwich": (542e3, 62.13e3), "PojzPlaza": (9.64e6, 78.79e3), "HEARTROCKER": (9.68e6, 172.18e3),
    "Guy Ngid": (6.6e6, 717.74e3), "SkizzTV": (6.38e6, 180.61e3), "CGGG": (7.99e6, 12.37e3), "The Moof": (1.31e6, 27.5e3),
    "FZK Frozenkiss": (483e3, 861), "FOOTBOT": (5.54e6, 30.91e3), "Jdumofficial": (440e3, 98.87e3),
    "Reflex Channel": (139e3, 19.52e3), "Be Fit With Jess": (174e3, 1.33e3), "Ananped": (8.5e6, 928.34e3), "OAUJUN": (10.9e6, 302.51e3),
}


def q(a):
    a = sorted(a)
    return {"n": len(a), "min": a[0], "median": float(np.median(a)), "max": a[-1]}


res["youtube_latest_video_view_ratio"] = {
    "mega_1m_plus": q([v / s for k, (s, v) in yt.items() if s >= 1e6]),
    "mid_macro_100k_to_1m": q([v / s for k, (s, v) in yt.items() if 1e5 <= s < 1e6]),
    "note": "Latest-video views over subscribers, one video each, read within about a day or two of upload; not a typical-post average."}

# TikTok top-50 per-post averages (S; ranked by the aggregator; favours very high averages, so an upper bound).
# Columns: followers, avg views, avg likes, avg comments, avg shares. Rows 21, 48 and 49 of the saved table (accounts under 10,000 followers) are left out.
tt = [(4.1e6, 3e6, 882e3, 5.5e3, 106.5e3), (1.7e6, 2.2e6, 866.7e3, 4.8e3, 46.1e3), (10.8e6, 2.8e6, 453.2e3, 2.1e3, 29e3), (955.1e3, 2.6e6, 407.8e3, 1.4e3, 31.8e3),
      (483.2e3, 2.3e6, 293.6e3, 1.4e3, 43.7e3), (1.5e6, 1.6e6, 333.6e3, 264, 47.1e3), (1.4e6, 1.5e6, 322.2e3, 298, 36.2e3), (2.4e6, 984.1e3, 400.2e3, 4e3, 32.7e3),
      (1.4e6, 1.3e6, 379.2e3, 1.5e3, 24.3e3), (2.5e6, 3.6e6, 248.6e3, 3.9e3, 9e3), (2e6, 2.7e6, 181e3, 612, 22.3e3), (31.7e6, 2.5e6, 211.7e3, 2.8e3, 11.9e3),
      (3.3e6, 1.1e6, 338.9e3, 4.1e3, 15.2e3), (4.3e6, 1.4e6, 284.6e3, 3.7e3, 14e3), (3.5e6, 1.5e6, 235e3, 826, 19.1e3), (2.6e6, 1.1e6, 124.9e3, 530, 51.4e3),
      (4e6, 2e6, 198.7e3, 1.5e3, 15.5e3), (2.1e6, 777e3, 310.7e3, 3.3e3, 23.5e3), (3.8e6, 1.3e6, 331e3, 3.4e3, 9.2e3), (2.1e6, 1.8e6, 117.7e3, 804, 23.3e3),
      (274.5e3, 1.4e6, 170e3, 557, 17.3e3), (2.4e6, 975.7e3, 136.9e3, 457, 30.4e3), (253e3, 934e3, 137.7e3, 419, 31.2e3), (1.8e6, 2.9e6, 157.5e3, 3.7e3, 5.2e3),
      (4.8e6, 707.1e3, 217e3, 1e3, 22.7e3), (3.5e6, 1.1e6, 150e3, 127, 19.6e3), (1.7e6, 685.1e3, 295.3e3, 2.3e3, 12.8e3), (1.5e6, 1.2e6, 152.1e3, 425, 14.9e3),
      (1e6, 558e3, 183.1e3, 820, 23.6e3), (1.6e6, 787.8e3, 186.9e3, 1.6e3, 14.7e3), (11e6, 2.3e6, 140.3e3, 595, 6.8e3), (1.1e6, 594.1e3, 236.4e3, 1.3e3, 15.5e3),
      (2.1e6, 657.1e3, 197.1e3, 1e3, 16.7e3), (12.4e6, 2e6, 168.4e3, 316, 6.3e3), (2.5e6, 749.6e3, 296.2e3, 1.3e3, 8.4e3), (615.2e3, 807.6e3, 118.6e3, 135, 22e3),
      (5.5e6, 1.6e6, 157.1e3, 347, 8.3e3), (1.9e6, 527.6e3, 246.2e3, 2.7e3, 13e3), (1.2e6, 549.3e3, 190e3, 1.6e3, 17e3), (3.5e6, 670.1e3, 273.9e3, 3.1e3, 7.4e3),
      (1.5e6, 938.5e3, 124.4e3, 247, 16e3), (2.9e6, 1.8e6, 137.7e3, 224, 6.5e3), (2.7e6, 643e3, 179.5e3, 3e3, 11.3e3), (1.2e6, 620.5e3, 229.3e3, 1.2e3, 9.6e3),
      (8.1e6, 1.3e6, 161.4e3, 249, 6.5e3), (705.1e3, 554.7e3, 61.3e3, 225, 38.5e3), (9.2e6, 1.6e6, 113.3e3, 374, 6.3e3)]
res["tiktok_top50_ratios"] = {
    "n": len(tt),
    "views_over_followers": q([r[1] / r[0] for r in tt]),
    "engagement_over_followers_likes_comments_shares": q([(r[2] + r[3] + r[4]) / r[0] for r in tt]),
    "engagement_over_views_likes_comments_shares": q([(r[2] + r[3] + r[4]) / r[1] for r in tt]),
    "note": "Per-post averages over followers or views for the accounts of 100,000 followers or more in a list ranked by the aggregator; an upper bound for a typical creator."}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("wrote", OUT)
print("total budget", round(total), "flat fees", round(fees_sum), "base creator CPA", round(tot_cost / tot_purch))
