"""T16 domestic KOL campaign plan: pilot budget, funnel, break-even and stop-rule model (20 October 2026).

Writes rework/screen/t16_kol_campaign_plan_results.json. Fixed seed. Pure Python (standard library only).
Every input carries its tier in the INPUTS table. Tiers follow rework/submission/appendix_a_tier_key.md:
P, S (with SOURCED), PROXY (stand-in for a measured value), ASSUMPTION (design or modelling choice),
DERIVED (arithmetic on the inputs shown), COMPANY CLAIM.

Run:  python rework/screen/t16_kol_campaign_plan.py
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "t16_kol_campaign_plan_results.json")
SEED = 20261020
DRAWS = 20000
FX = 33.5410  # baht per US dollar: Bank of Thailand REFERENCE RATE for 15 October 2026 (P; Report 123, read 20 October 2026; rework/raw/diligence_2026-10-20/T1/bot_fx_report123_2026-10-20.md). Replaces the team midpoint of 33.55 (which is DERIVED and not a published rate)

# ---------------------------------------------------------------- inputs (value, tier, source)
INPUTS = {
    "cubes_per_carton": (6, "ASSUMPTION", "team six-cube carton (a pack design choice), rework/proposal/05 and 10"),
    "exfactory_per_cube_thb": (9.00, "ASSUMPTION", "shelf 15.00 x 60 percent ex-factory share, rework/proposal/05 row Shelf price"),
    "cost_pouch_thb": (1.30, "ASSUMPTION", "pouch per cube, rework/proposal/06 cost build"),
    "cost_print_thb": (1.50, "ASSUMPTION", "print per cube, rework/proposal/06 cost build"),
    "cost_processing_thb": (0.50, "ASSUMPTION", "processing per cube, rework/proposal/06 cost build"),
    "cost_reactants_thb": (0.118, "DERIVED", "reactants per cube, rework/proposal/06 line 105 (the earlier note omitted this line)"),
    "cost_carton_share_6pack_thb": (0.67, "ASSUMPTION", "carton share per cube for the 6-cube carton (THB 4 per carton scaled from the 12-cube price), rework/proposal/05 cost table"),
    "cost_per_cube_6pack_thb": (4.09, "DERIVED", "sum of the five cost rows above, rounded (1.30 + 1.50 + 0.50 + 0.118 + 0.67 = 4.088), rework/proposal/05 and 06. Binder (0.80 g) and lemon flavour (0.05 g) are NOT priced anywhere in the repo cost build, so this cost is an incomplete build and the contribution is an upper bound"),
    "contrib_floor_per_cube_thb": (3.51, "DERIVED", "repo floor from the pouch high case, rework/proposal/10 and 06"),
    "shelf_per_cube_thb": (15.00, "ASSUMPTION", "rework/proposal/05 row Shelf price"),
    "commission_per_carton_thb": (8.00, "ASSUMPTION", "team setting below the ceiling of THB 8.40 per carton (base contribution 3.58 per cube after commission). The earlier planning value, 10 percent of the THB 90 carton (THB 9.00), gives 3.41 per cube at base and fails the 3.51 test"),
    "cpc_phoenix_thb": (11.5, "PROXY", "Phoenix Media 2025, Facebook and Instagram, cross-industry; rework/raw/diligence_2026-10-20/T16/14"),
    "cpm_phoenix_thb": (120, "PROXY", "Phoenix Media 2025, Facebook and Instagram; rework/raw/.../T16/14"),
    "cpc_global_usd": (0.82, "PROXY", "Vaizle 2025 average, 5,200 Meta accounts; rework/raw/.../T16/19"),
    "lpr_low": (0.0008, "PROXY", "Phoenix 2025 conversion rate 0.08 percent (lead-generation mix); rework/raw/.../T16/14"),
    "lpr_base": (0.01, "ASSUMPTION", "click-to-first-purchase base, rework/proposal/10 Step 1"),
    "lpr_high": (0.0202, "PROXY", "Triple Whale food and beverage conversion 2.02 percent, 2025, via Influee; rework/raw/.../T16/19"),
    "ctr_creator": (0.01, "ASSUMPTION", "view to link click on creator posts; cross-check Phoenix-implied 1.04 percent (DERIVED)"),
    "repeat_base": (0.30, "ASSUMPTION", "repeat target, rework/proposal/10 both routes"),
    "repeat_floor": (0.15, "ASSUMPTION", "repeat floor, rework/proposal/10"),
    "repeat_extra_cartons": (1, "ASSUMPTION", "a repeat buyer buys one more carton inside 13 weeks"),
    "micro_fee_usd": (200, "PROXY", "Influencer Marketing Hub, TikTok micro lower bound, 6 October 2026; rework/raw/.../T16/05"),
    "mid_fee_usd": (1000, "PROXY", "Influencer Marketing Hub, YouTube mid lower bound; rework/raw/.../T16/05"),
    "kit_cubes": (12, "ASSUMPTION", "two cartons per creator"),
    "commission_cap_cartons": (500, "ASSUMPTION", "planning cap on creator-coded cartons"),
    "contingency_share": (0.10, "ASSUMPTION", "planning contingency on committed lines"),
    "route_b_learning_thb": (20000, "ASSUMPTION", "paid learning tranche, released after the week 4 read"),
    "route_b_scale_thb": (40000, "ASSUMPTION", "paid scale tranche, released only if cost per first purchase meets the cap at week 8"),
}
V = {k: v[0] for k, v in INPUTS.items()}
_COST_SUM = round(V["cost_pouch_thb"] + V["cost_print_thb"] + V["cost_processing_thb"] + V["cost_reactants_thb"]
                  + V["cost_carton_share_6pack_thb"], 3)  # 4.088
assert abs(_COST_SUM - V["cost_per_cube_6pack_thb"]) < 0.005, _COST_SUM

CUBES = V["cubes_per_carton"]
CONTRIB_BASE_CUBE = round(V["exfactory_per_cube_thb"] - V["cost_per_cube_6pack_thb"], 2)  # 4.91
CONTRIB_FLOOR_CUBE = V["contrib_floor_per_cube_thb"]  # 3.51
CARTON_CONTRIB_BASE = CUBES * CONTRIB_BASE_CUBE  # 29.46
CARTON_CONTRIB_FLOOR = CUBES * CONTRIB_FLOOR_CUBE  # 21.06
COMMISSION = V["commission_per_carton_thb"]
CONTRIB_BASE_AFTER_COMMISSION_CUBE = round(CONTRIB_BASE_CUBE - COMMISSION / CUBES, 2)  # 3.58
KIT_COST = V["kit_cubes"] * V["cost_per_cube_6pack_thb"]  # 49.08 per creator (6-cube cost basis, conservative)
CPC = V["cpc_phoenix_thb"]
CPC_GLOBAL = round(V["cpc_global_usd"] * FX, 2)  # about 27.5
CTR = V["ctr_creator"]
LPR = {"low": V["lpr_low"], "base": V["lpr_base"], "high": V["lpr_high"]}
REPEAT = {"floor": V["repeat_floor"], "base": V["repeat_base"]}
MICRO_FEE = round(V["micro_fee_usd"] * FX, 2)  # 6,710
MID_FEE = round(V["mid_fee_usd"] * FX, 2)  # 33,550

# Creator mix (pilot). Views per post are ASSUMPTIONS; the low and high values are the sensitivity range.
TIERS = [
    {"tier": "nano", "followers": "1K to 10K", "creators": 16, "posts_each": 2, "views_base": 1000, "views_low": 500,
     "views_high": 2500, "flat_fee_per_post": 0.0, "fee_tier": "no flat fee (kit and commission only); ASSUMPTION offer structure"},
    {"tier": "micro", "followers": "10K to 100K", "creators": 4, "posts_each": 2, "views_base": 4000, "views_low": 2000,
     "views_high": 12000, "flat_fee_per_post": MICRO_FEE, "fee_tier": "PROXY: USD 200 x 33.55"},
    {"tier": "mid", "followers": "100K to 500K", "creators": 1, "posts_each": 1, "views_base": 25000, "views_low": 10000,
     "views_high": 60000, "flat_fee_per_post": MID_FEE, "fee_tier": "PROXY: USD 1,000 x 33.55 (optional line, cut first)"},
]


def creator_program(views_mult=1.0, lpr=None, repeat=None, include_mid=True, include_fees=True, views_key="views_base"):
    """Creator program over the 13-week pilot. Returns spend, buyers, cartons and net result (baht)."""
    lpr = LPR["base"] if lpr is None else lpr
    repeat = REPEAT["base"] if repeat is None else repeat
    posts = views = creators = 0
    fees = kits = 0.0
    per_tier = {}
    for t in TIERS:
        if t["tier"] == "mid" and not include_mid:
            continue
        n, p = t["creators"], t["posts_each"]
        tv = n * p * t[views_key] * views_mult
        posts += n * p
        views += tv
        creators += n
        tfee = (n * p * t["flat_fee_per_post"]) if include_fees else 0.0
        fees += tfee
        kits += n * KIT_COST
        per_tier[t["tier"]] = {"creators": n, "posts": n * p, "views": round(tv, 1), "flat_fees_thb": round(tfee, 2)}
    clicks = views * CTR
    buyers = clicks * lpr
    cartons_per_buyer = 1 + repeat * V["repeat_extra_cartons"]
    cartons = buyers * cartons_per_buyer
    net_contrib = cartons * (CARTON_CONTRIB_BASE - COMMISSION)  # commission netted from contribution
    commission_cost = cartons * COMMISSION
    fixed = fees + kits
    result = net_contrib - fixed
    spend = fixed + commission_cost
    cpf = spend / buyers if buyers > 0 else None
    return {
        "creators": creators, "posts": posts, "views": round(views, 1), "clicks": round(clicks, 2),
        "first_purchases_buyers": round(buyers, 3), "cartons_per_buyer": round(cartons_per_buyer, 3),
        "cartons": round(cartons, 3), "flat_fees_thb": round(fees, 2), "kits_thb": round(kits, 2),
        "commission_thb": round(commission_cost, 2), "spend_thb": round(spend, 2),
        "contribution_net_of_commission_thb": round(net_contrib, 2),
        "net_result_thb": round(result, 2), "cost_per_first_purchase_thb": round(cpf, 2) if cpf else None,
        "per_tier": per_tier,
    }


def creator_breakeven(lpr=None, repeat=None, include_mid=True, include_fees=True):
    """Views needed so that the fixed creator spend (fees and kits) is recovered from net contribution in 13 weeks."""
    lpr = LPR["base"] if lpr is None else lpr
    repeat = REPEAT["base"] if repeat is None else repeat
    base = creator_program(lpr=lpr, repeat=repeat, include_mid=include_mid, include_fees=include_fees)
    fixed = base["flat_fees_thb"] + base["kits_thb"]
    per_buyer_net = (1 + repeat * V["repeat_extra_cartons"]) * (CARTON_CONTRIB_BASE - COMMISSION)
    buyers_needed = fixed / per_buyer_net
    views_needed = buyers_needed / (CTR * lpr)
    return {"fixed_spend_thb": round(fixed, 2), "net_per_buyer_thb": round(per_buyer_net, 2),
            "buyers_needed": round(buyers_needed, 1), "views_needed": round(views_needed, 0),
            "views_planned": base["views"],
            "purchases_per_1000_views_needed_at_planned_views": round(1000 * buyers_needed / base["views"], 2),
            "purchases_per_1000_views_planned": round(1000 * base["first_purchases_buyers"] / base["views"], 3)}


def paid_route(spend, cpc, lpr, repeat, contrib=CARTON_CONTRIB_FLOOR):
    clicks = spend / cpc
    buyers = clicks * lpr
    cartons = buyers * (1 + repeat * V["repeat_extra_cartons"])
    cpf = spend / buyers if buyers > 0 else None
    return {"clicks": round(clicks, 1), "buyers": round(buyers, 3), "cartons": round(cartons, 3),
            "cost_per_first_purchase_thb": round(cpf, 2) if cpf else None,
            "gross_contribution_thb": round(cartons * contrib, 2), "net_thb": round(cartons * contrib - spend, 2)}


def cap(repeat, contrib=CARTON_CONTRIB_FLOOR):
    """Team's proposed cap on cost per first purchase for Route B: floor contribution per carton times cartons per buyer."""
    return round(contrib * (1 + repeat * V["repeat_extra_cartons"]), 2)


# ---------------------------------------------------------------- budget (one pilot budget)
def budget():
    mid_on = TIERS[2]["flat_fee_per_post"] * TIERS[2]["creators"] * TIERS[2]["posts_each"]
    micro_fees = TIERS[1]["flat_fee_per_post"] * TIERS[1]["creators"] * TIERS[1]["posts_each"]
    lines = [
        {"line": "Micro creator flat fees", "arithmetic": "4 creators x 2 posts x THB %s" % MICRO_FEE,
         "thb": round(micro_fees, 2), "tier": "PROXY"},
        {"line": "Mid creator flat fee (optional, cut first)", "arithmetic": "1 creator x 1 video x THB %s" % MID_FEE,
         "thb": round(mid_on, 2), "tier": "PROXY"},
        {"line": "Creator kits, nano", "arithmetic": "16 creators x 12 cubes x THB 4.09 = 16 x %.2f" % KIT_COST,
         "thb": round(16 * KIT_COST, 2), "tier": "DERIVED on ASSUMPTION cost inputs"},
        {"line": "Creator kits, micro and mid", "arithmetic": "5 creators x %.2f" % KIT_COST,
         "thb": round(5 * KIT_COST, 2), "tier": "DERIVED on ASSUMPTION cost inputs"},
        {"line": "Commission cap on creator-coded cartons", "arithmetic": "%d cartons x THB %.2f" % (
            V["commission_cap_cartons"], COMMISSION), "thb": round(V["commission_cap_cartons"] * COMMISSION, 2),
         "tier": "ASSUMPTION (cap; rate set by the 3.51 test)"},
        {"line": "Measurement: unique codes and listing analytics", "arithmetic": "internal tools; no quote obtained",
         "thb": 0.0, "tier": "ASSUMPTION; not costed"},
    ]
    subtotal = round(sum(x["thb"] for x in lines), 2)
    contingency = round(subtotal * V["contingency_share"], 2)
    committed = round(subtotal + contingency, 2)
    conditional = [
        {"line": "Route B learning tranche (paid social, one listing)", "arithmetic": "released after the week 4 read",
         "thb": V["route_b_learning_thb"], "tier": "ASSUMPTION"},
        {"line": "Route B scale tranche (paid social)", "arithmetic": "released only if the week 8 cost per first purchase is at or below the cap",
         "thb": V["route_b_scale_thb"], "tier": "ASSUMPTION"},
    ]
    # Tranche release rule (week 8): cost per first purchase at or below the cap at the measured repeat, and contribution
    # per cube after commission at least 3.51. The scaling rule (week 12) is in res["scale_rule"] in main().
    cond_total = sum(x["thb"] for x in conditional)
    ceiling = round(committed + cond_total, 2)
    no_mid_committed = round((subtotal - mid_on) * (1 + V["contingency_share"]), 2)
    # Option B (team's recommended default): commission-led; 16 nano and 4 micro on kit plus commission; no flat fees; no mid video.
    kits_b = round(20 * KIT_COST, 2)
    comm_b = round(V["commission_cap_cartons"] * COMMISSION, 2)
    sub_b = round(kits_b + comm_b, 2)
    cont_b = round(sub_b * V["contingency_share"], 2)
    committed_b = round(sub_b + cont_b, 2)
    option_b = {"name": "B, commission-led (recommended default)",
                "lines": [
                    {"line": "Creator kits, nano and micro", "arithmetic": "20 creators x 12 cubes x THB 4.09 = 20 x %.2f" % KIT_COST,
                     "thb": kits_b, "tier": "DERIVED on ASSUMPTION cost inputs"},
                    {"line": "Commission cap on creator-coded cartons", "arithmetic": "%d cartons x THB %.2f" % (
                        V["commission_cap_cartons"], COMMISSION), "thb": comm_b, "tier": "ASSUMPTION (cap; rate set by the 3.51 test)"},
                    {"line": "Measurement: unique codes and listing analytics", "arithmetic": "internal tools; no quote obtained",
                     "thb": 0.0, "tier": "ASSUMPTION; not costed"}],
                "subtotal_committed_thb": sub_b, "contingency_thb": cont_b, "committed_total_thb": committed_b,
                "conditional_total_thb": cond_total, "ceiling_total_thb": round(committed_b + cond_total, 2)}
    option_a = {"name": "A, with flat fees for micro and mid posts", "subtotal_committed_thb": subtotal,
                "contingency_thb": contingency, "committed_total_thb": committed,
                "conditional_total_thb": cond_total, "ceiling_total_thb": ceiling}
    return {"option_A": option_a, "option_B": option_b, "lines": lines, "subtotal_committed_thb": subtotal, "contingency_thb": contingency,
            "committed_total_thb": committed, "conditional_lines": conditional,
            "conditional_total_thb": cond_total, "ceiling_total_thb": ceiling,
            "committed_without_mid_thb": no_mid_committed,
            "creators_total": sum(t["creators"] for t in TIERS), "posts_total": sum(t["creators"] * t["posts_each"] for t in TIERS)}


def monte_carlo():
    rng = random.Random(SEED)
    net_pos = 0
    net_pos_nofee = 0
    cpf_list = []
    paid_ok = 0
    paid_cpf = []
    for _ in range(DRAWS):
        vm = math.exp(rng.gauss(0.0, 0.5))  # views multiplier, median 1 (ASSUMPTION spread)
        lpr = rng.triangular(0.0008, 0.0202, 0.01)  # ASSUMPTION distribution between PROXY bounds, mode at base
        ctr_draw = rng.triangular(0.005, 0.02, 0.01)  # ASSUMPTION
        rep = rng.triangular(0.15, 0.40, 0.30)  # ASSUMPTION
        global CTR
        saved = CTR
        CTR = ctr_draw
        r = creator_program(views_mult=vm, lpr=lpr, repeat=rep)
        r_nofee = creator_program(views_mult=vm, lpr=lpr, repeat=rep, include_fees=False, include_mid=False)
        CTR = saved
        if r["net_result_thb"] >= 0:
            net_pos += 1
        if r_nofee["net_result_thb"] >= 0:
            net_pos_nofee += 1
        if r["cost_per_first_purchase_thb"]:
            cpf_list.append(r["cost_per_first_purchase_thb"])
        # paid: CPC and LPR draws; cap uses the repeat draw at week 8 (ASSUMPTION)
        cpc_draw = rng.triangular(CPC, CPC_GLOBAL, CPC)
        lpr_p = rng.triangular(0.0008, 0.0202, 0.01)
        cpf_paid = cpc_draw / lpr_p
        paid_cpf.append(cpf_paid)
        if cpf_paid <= cap(rep):
            paid_ok += 1
    cpf_list.sort()
    paid_cpf.sort()
    med = lambda xs: xs[len(xs) // 2]
    return {"draws": DRAWS, "seed": SEED,
            "prob_creator_net_result_at_or_above_zero": round(net_pos / DRAWS, 4),
            "creator_cpf_median_thb": round(med(cpf_list), 2) if cpf_list else None,
            "creator_cpf_p10_thb": round(cpf_list[int(0.10 * len(cpf_list))], 2) if cpf_list else None,
            "creator_cpf_p90_thb": round(cpf_list[int(0.90 * len(cpf_list))], 2) if cpf_list else None,
            "prob_creator_net_result_at_or_above_zero_option_B_commission_led": round(net_pos_nofee / DRAWS, 4),
            "prob_paid_cpf_at_or_below_cap": round(paid_ok / DRAWS, 4),
            "paid_cpf_floor_thb": round(CPC / V["lpr_high"], 2),
            "cap_max_thb": cap(0.40),
            "paid_cpf_median_thb": round(med(paid_cpf), 2),
            "paid_cpf_p10_thb": round(paid_cpf[int(0.10 * DRAWS)], 2),
            "paid_cpf_p90_thb": round(paid_cpf[int(0.90 * DRAWS)], 2),
            "note": "ASSUMPTION distributions: views multiplier lognormal (sigma 0.5), CTR triangular 0.5 to 2 percent, LPR triangular between the PROXY bounds (0.08 to 2.02 percent) with mode at the 1.0 percent base, repeat triangular 15 to 40 percent (mode 30). Paid cost per click triangular between the Phoenix PROXY (THB 11.5, mode) and the global PROXY (THB 27.51). These are model readings, not forecasts. The paid cap result of 0.0 is structural, not a finding: the lowest paid cost per first purchase in any draw is paid_cpf_floor_thb (THB 11.5 divided by 2.02 percent), and the highest cap in any draw is cap_max_thb (at a 40 percent repeat), so no draw can meet the cap."}


def main():
    res = {"meta": {"date": "2026-10-20", "seed": SEED, "fx_thb_per_usd": FX,
                    "note": "All numbers are produced by this script. Inputs carry their tier in INPUTS."},
           "inputs": {k: {"value": v[0], "tier": v[1], "source": v[2]} for k, v in INPUTS.items()}}

    res["unit_economics"] = {
        "contrib_base_per_cube_thb": CONTRIB_BASE_CUBE,
        "contrib_floor_per_cube_thb": CONTRIB_FLOOR_CUBE,
        "carton_contrib_base_thb": round(CARTON_CONTRIB_BASE, 2),
        "carton_contrib_floor_thb": round(CARTON_CONTRIB_FLOOR, 2),
        "commission_per_carton_thb": COMMISSION,
        "contrib_base_after_commission_per_cube_thb": CONTRIB_BASE_AFTER_COMMISSION_CUBE,
        "max_commission_per_carton_keeping_3_51_at_base_thb": round((CONTRIB_BASE_CUBE - CONTRIB_FLOOR_CUBE) * CUBES, 2),
        "headroom_to_floor_before_commission_per_cube_thb": round(CONTRIB_BASE_CUBE - CONTRIB_FLOOR_CUBE, 2),
        "headroom_to_floor_after_commission_per_cube_thb": round(CONTRIB_BASE_AFTER_COMMISSION_CUBE - CONTRIB_FLOOR_CUBE, 2),
        "unpriced_inputs": "binder and filler 0.80 g and lemon flavour 0.05 g are not priced in the repo cost build (proposal/05, proposal/06); contribution figures are upper bounds; any unpriced cost above the after-commission headroom per cube fails the 3.51 test",
        "kit_cost_per_creator_thb": round(KIT_COST, 2),
        "cpc_phoenix_thb": CPC, "cpc_global_thb": CPC_GLOBAL, "cpm_phoenix_thb": V["cpm_phoenix_thb"],
        "phoenix_implied_ctr_pct": round(100 * V["cpm_phoenix_thb"] / (CPC * 1000), 3),
        "micro_fee_thb": MICRO_FEE, "mid_fee_thb": MID_FEE,
    }

    # Paid route (Route B): cost per first purchase and break-even
    cost_grid = []
    for cpc_label, cpc in (("phoenix", CPC), ("global", CPC_GLOBAL)):
        for lpr_label in ("low", "base", "high"):
            cpf = cpc / LPR[lpr_label]
            cost_grid.append({"cpc": cpc_label, "cpc_thb": cpc, "lpr": lpr_label, "lpr_value": LPR[lpr_label],
                              "cost_per_first_purchase_thb": round(cpf, 2),
                              "cartons_to_recover_base_1carton": round(cpf / CARTON_CONTRIB_BASE, 2),
                              "cartons_to_recover_floor_1carton": round(cpf / CARTON_CONTRIB_FLOOR, 2),
                              "cubes_to_recover_at_4_91": round(cpf / CONTRIB_BASE_CUBE, 1)})
    res["paid_route_grid"] = cost_grid
    res["paid_cap"] = {
        "cap_repeat_floor_thb": cap(REPEAT["floor"]),
        "cap_repeat_base_thb": cap(REPEAT["base"]),
        "lpr_needed_at_phoenix_cpc_for_cap_base_repeat_pct": round(100 * CPC / cap(REPEAT["base"]), 2),
        "lpr_needed_at_phoenix_cpc_for_one_carton_floor_pct": round(100 * CPC / CARTON_CONTRIB_FLOOR, 2),
        "lpr_needed_at_phoenix_cpc_for_one_carton_base_pct": round(100 * CPC / CARTON_CONTRIB_BASE, 2),
    }
    learn = paid_route(V["route_b_learning_thb"], CPC, LPR["base"], REPEAT["base"])
    scale = paid_route(V["route_b_scale_thb"], CPC, LPR["base"], REPEAT["base"])
    res["paid_route_at_base"] = {"learning_tranche": learn, "scale_tranche_if_released": scale,
                                 "full_60000_route_b": paid_route(60000, CPC, LPR["base"], REPEAT["base"]),
                                 "flag": "paid social does not recover its first-purchase cost at base inputs"}

    # Budget
    res["budget"] = budget()
    res["budget"]["scope"] = ("Creator programme and Route B paid-social budget only. Route A in-store sampling is NOT costed: "
                              "the store count and samples per store are not set in proposal/10 (UNVERIFIED), so no Route A total "
                              "and no two-route total is stated. Brand-lift panel and Thai legal review are not costed either.")
    res["route_a_not_costed"] = {"per_sample_thb": 15, "range_thb": [10, 25], "tier": "ASSUMPTION (proposal/10 Route A)",
                                 "stores": "UNVERIFIED: not set in proposal/10", "formula": "stores x samples per store x THB 15",
                                 "total_thb": None}
    res["scale_rule"] = {
        "tranche_release_week_8": "Release the THB 40,000 scale tranche at week 8 only if the measured cost per first purchase on cohort 1 is at or below the cap at the measured repeat, and the measured contribution per cube after commission is at least THB 3.51.",
        "scaling_week_12": "Scale a route beyond the released tranche only if repeat is at least 15 percent in both cohorts and the measured contribution per cube after commission is at least THB 3.51.",
        "cap_thb": {"repeat_30pct": cap(REPEAT["base"]), "repeat_15pct": cap(REPEAT["floor"]), "repeat_40pct_max_draw": cap(0.40)},
        "tiers": "cap DERIVED on the repo floor (THB 3.51 per cube, 6 cubes per carton); the repeat rates are ASSUMPTIONS; the week 8 and week 12 gates are ASSUMPTIONS",
    }

    # Creator program: base, sensitivity and break-even
    res["creator_program_base_full"] = creator_program()
    res["creator_program_base_no_mid"] = creator_program(include_mid=False)
    res["creator_program_commission_only_no_fees"] = creator_program(include_fees=False)
    res["creator_program_commission_led_B"] = creator_program(include_fees=False, include_mid=False)
    sens = []
    for vm_label, vm in (("views_low", "low"), ("views_base", "base"), ("views_high", "high")):
        for lpr_label in ("low", "base", "high"):
            key = "views_base" if vm == "base" else ("views_low" if vm == "low" else "views_high")
            r_full = creator_program(lpr=LPR[lpr_label], views_key=key)
            sens.append({"views": vm_label, "lpr": lpr_label, "lpr_value": LPR[lpr_label],
                         "views_total": r_full["views"], "buyers": r_full["first_purchases_buyers"],
                         "spend_thb": r_full["spend_thb"], "net_result_thb": r_full["net_result_thb"],
                         "cost_per_first_purchase_thb": r_full["cost_per_first_purchase_thb"]})
    res["creator_sensitivity"] = sens
    res["creator_breakeven_base"] = creator_breakeven()
    res["creator_breakeven_high_lpr"] = creator_breakeven(lpr=LPR["high"])
    res["creator_breakeven_repeat_floor"] = creator_breakeven(repeat=REPEAT["floor"])
    res["creator_breakeven_option_B"] = creator_breakeven(include_mid=False, include_fees=False)

    res["monte_carlo"] = monte_carlo()

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print("wrote", OUT)
    b = res["budget"]
    print("budget A", b["option_A"]["committed_total_thb"], b["option_A"]["ceiling_total_thb"], "B", b["option_B"]["committed_total_thb"], b["option_B"]["ceiling_total_thb"])
    print("creator base", {k: res["creator_program_base_full"][k] for k in ("views", "first_purchases_buyers", "spend_thb", "net_result_thb", "cost_per_first_purchase_thb")})
    print("paid cpf base", cost_grid[1]["cost_per_first_purchase_thb"], "cap base", res["paid_cap"]["cap_repeat_base_thb"], "cap floor repeat", res["paid_cap"]["cap_repeat_floor_thb"])
    print("creator breakeven", res["creator_breakeven_base"])
    print("mc", {k: v for k, v in res["monte_carlo"].items() if k not in ("note",)})


if __name__ == "__main__":
    main()
