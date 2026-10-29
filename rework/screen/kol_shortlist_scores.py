"""Domestic creator shortlist scoring (T16, 20 October 2026; revised after the independent verifier's review).

Applies the score rule in rework/79a_kol_shortlist.md to flags that were read from public pages saved in
rework/raw/diligence_2026-10-20/T16/09_kol_public_pages_vidiq_hypeauditor_tia.md and in T16 raw 21. No page is fetched here.
Writes rework/screen/kol_shortlist_scores_results.json. A point is given only for evidence that was read;
anything not read scores 0.

Also reads the 50-row TikTok table in raw 09 (section 2) and recomputes the per-post statistics for the 100,000-plus
accounts (the earlier figures came from screen/kol_campaign_model.py; this script replaces that source for the record).

Band sensitivity: the Priority band depends on two ASSUMPTIONS (the 500,000 mid and macro split, and the THB 40,000
fee cut-off). The script re-runs the scoring under alternative settings and writes the band counts for each.

Run:  python rework/screen/kol_shortlist_scores.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "kol_shortlist_scores_results.json")
RAW09 = os.path.join(HERE, "..", "raw", "diligence_2026-10-20", "T16", "09_kol_public_pages_vidiq_hypeauditor_tia.md")

# Baht per US dollar: Bank of Thailand reference rate for 15 October 2026 (P, Report 123 read 20 October 2026;
# rework/raw/diligence_2026-10-20/T1/bot_fx_report123_2026-10-20.md). Replaces the 33.55 team midpoint.
FX = 33.5410

# YouTube lower-bound fee in USD by tier (Influencer Marketing Hub rate table, 6 October 2026; raw 05). PROXY.
FEE_LOW_USD_YT = {"nano": 20, "micro": 200, "mid": 1000, "macro": 10000, "mega": 20000}

# Baseline settings. mid_band True: the team's own split (mid 100K to 500K, macro 500K to 1M), ASSUMPTION.
# mid_band False: the Influencer Marketing Hub follower definition (macro 100K to 1M; no mid band), S.
# cutoff: the pilot fee cut-off in THB, ASSUMPTION (set at the size of the Route B scale tranche, record 79 section 5.8).
SCENARIOS = {
    "baseline": {"mid_band": True, "cutoff": 40000, "demo_rule": True},
    "previous_rule_no_demo_point": {"mid_band": True, "cutoff": 40000, "demo_rule": False},
    "imh_macro_band_100k_to_1m": {"mid_band": False, "cutoff": 40000, "demo_rule": True},
    "fee_cutoff_33000": {"mid_band": True, "cutoff": 33000, "demo_rule": True},
    "imh_band_and_cutoff_33000": {"mid_band": False, "cutoff": 33000, "demo_rule": True},
}


def tier(n, mid_band=True):
    if n >= 1_000_000:
        return "mega"
    if mid_band:
        if n >= 500_000:
            return "macro"
        if n >= 100_000:
            return "mid"
    else:
        if n >= 100_000:
            return "macro"
    if n >= 10_000:
        return "micro"
    return "nano"


def fee_low_thb(t):
    return FEE_LOW_USD_YT[t] * FX


# Fields: name, handle, subs, hypeauditor category (or None), latest-video ER %, latest video date read (or None), genre label,
# fit_genre (2 on-target, 1 adjacent, 0 off), adult (1 adult-directed per evidence, else 0), alcohol_cue_in_titles_read (bool),
# centred_on_weight_or_medical (bool), consumption_or_demo_format (bool), award note
C = [
    ("BANKII", "@bankii", 10.6e6, "Food & Drinks; DIY & Life Hacks", 3.0, "2026-10-18", "Food: street food, big meals", 2, 1, False, False, True, "Japan Expo Best Food 2026"),
    ("PEACH EAT LAEK", "@peacheatlaek", 9.12e6, "Food & Drinks; Travel", 0.9, "2026-10-17", "Food: eating", 2, 1, False, False, True, ""),
    ("Jack Papho", "@jackpapho532", 9.03e6, "Travel; Food & Drinks", 1.2, "2026-10-14", "Travel with food, music, challenges", 1, 1, False, False, True, ""),
    ("หม่อมถนัดแดก (Tanaddak)", "@tanaddak", 4.96e6, "Food & Drinks; Show", 2.5, "2026-10-18", "Food: restaurant and dish tasting", 2, 1, False, False, True, ""),
    ("JIMSURIYA V.2", "@jimsuriyav2", 3.25e6, None, 2.7, None, "Food: unusual food hunts, eating shows", 2, 1, False, False, True, "Best Foodie 2025 (1st)"),
    ("Cinmhef", "@cinmhef", 1.46e6, None, 4.8, "2026-10-16", "Food: street-food vlogs (TikTok 3.5M followers also)", 2, 1, False, False, True, "Best Foodie 2026 (1st)"),
    ("NutApiwich", "@nutapiwich", 542e3, None, 1.2, None, "Food-focused travel vlogs", 1, 1, False, False, True, "Best Foodie 2024 (3rd)"),
    ("PojzPlaza", "@ppz321", 9.64e6, "Video games; Toys", 3.2, "2026-10-17", "Gaming (HypeAuditor lists Toys)", 2, 0, False, False, False, ""),
    ("HEARTROCKER", "@heartrock", 9.68e6, "Video games; DIY & Life Hacks", 1.2, "2026-10-18", "Gaming: horror and multiplayer live streams", 2, 1, False, False, False, ""),
    ("กาย หงิด (Guy Ngid)", "@guyngid", 6.6e6, "Video games; Humor", 1.7, "2026-10-18", "Gaming comedy, card-game shop", 2, 1, False, False, False, ""),
    ("SkizzTV", "@skizztv59", 6.38e6, "Video games; Humor", 2.5, None, "Gaming, snack reviews, news summaries", 2, 1, False, False, True, ""),
    ("CGGG", "@cggg01234", 7.99e6, "Video games; Sports", 4.0, "2026-09-25", "Mobile-game matches", 2, 1, False, False, False, ""),
    ("The Moof", "@themoof", 1.31e6, None, 0.8, "2026-10-18", "Film and game story explainers", 1, 1, False, False, False, "Best Gaming 2026 (3rd)"),
    ("FZK Frozenkiss", "@fzkfrozenkiss", 483e3, None, 4.4, "2026-10-16", "Esports (RoV) and travel vlogs", 2, 1, False, False, False, "Best Gaming 2026 (1st)"),
    ("FOOTBOT", "@footbot", 5.54e6, None, 0.7, "2026-10-18", "Football skill challenges", 2, 1, False, False, False, ""),
    ("Jdumofficial", "@jdumofficial3", 440e3, None, 1.8, "2026-10-18", "Football talk, talk shows", 1, 1, False, False, False, "Best Sports 2025 (2nd)"),
    ("Reflex Channel", "@reflexchannel", 139e3, None, 1.2, "2026-10-16", "Formula 1 and MotoGP stories", 2, 1, False, False, False, "Best Sports 2024 (3rd)"),
    ("Be Fit With Jess", "@befitwithjess", 174e3, None, 3.0, "2026-10-16", "Home body-shaping workouts, expert interviews", 2, 1, False, True, False, "Best Health & Mind 2025 (3rd)"),
    ("fitwithplant", "@fitwithplant312", 6830, None, 1.0, "2026-06-27", "HIIT fat-burn and toning routines", 2, 1, False, True, False, "Best Sports 2024 (2nd)"),
    ("Ananped", "@ananped", 8.5e6, "Daily vlogs; Humor", 2.1, None, "Vlogs, food challenges, horror series, pranks", 1, 1, False, False, True, ""),
    ("OAUJUN HI-END", "@oaujunhiend", 10.9e6, "Humor", 1.5, None, "Long challenge, prank and Lego adventure videos (young audience likely)", 1, 0, False, False, False, ""),
    # Added 20 October 2026 (rework/raw/.../T16/21): vidIQ page read; one latest title read (snack review, translated); subscribers 361K.
    ("Nott Hungry (honest reviews)", "@imknothungry", 361e3, None, 2.5, "2026-10-18", "Food: snack and food reviews ('honest review' channel)", 2, 1, False, False, True, "CreatorDB: Thailand, Food and Cooking; TikTok 855.7K, Instagram 119K"),
]

# Controversy check (20 October 2026): one WebSearch per creator, results read as leads, not opened. Not a scoring point;
# it is a gate: a Priority candidate still needs a full public record check before any approach (see the rule text).
CONTROVERSY = {
    "FZK Frozenkiss": "one search, no controversy surfaced (results unrelated; leads not opened)",
    "Cinmhef": "one search, no controversy surfaced (results unrelated; leads not opened)",
    "BANKII": "one search, no controversy surfaced in 2026 results; Heepsy July 2026 lists about 10.3M followers (snippet, not opened)",
    "Reflex Channel": "one search, no controversy surfaced (results MotoGP news; leads not opened)",
    "Nott Hungry (honest reviews)": "one search (20 October 2026), nothing relevant surfaced (results unrelated to this handle; leads not opened)",
}

# The scan date for "recent": the vidIQ pages were updated 17 Oct 2026; a latest video dated on or after 17 Sep 2026 counts as recent.
RECENT_FROM = "2026-09-17"


def score_rows(scn):
    rows = []
    for (name, handle, subs, cat, er, last, genre, fit_genre, adult, alcohol, weightmed, demo, award) in C:
        t = tier(subs, scn["mid_band"])
        fee_low = fee_low_thb(t)
        size_ok = 1 if fee_low <= scn["cutoff"] else 0
        fit = fit_genre + (1 if adult else 0)
        s1 = 0 if alcohol else 1  # no alcohol cue in the titles or topics read; provisional for every row
        s2 = 0 if weightmed else 1
        s3 = 1 if adult else 0
        safety = s1 + s2 + s3
        f1 = 1 if demo else 0
        f2 = 1 if (last is not None and last >= RECENT_FROM) else 0
        fmt = f1 + f2 + size_ok
        total = fit + safety + fmt
        if total >= 8 and size_ok and (f1 or not scn["demo_rule"]):
            band = "Priority candidate (pending controversy and public record checks)"
        elif total >= 8 and not size_ok:
            band = "Reference: above the pilot fee scale"
        elif total >= 8:
            band = "Reserve: fits the fee scale but has no eating or demonstration format"
        elif total >= 6:
            band = "Reserve"
        else:
            band = "Not recommended on the evidence read"
        rows.append({"name": name, "handle": handle, "platform": "YouTube", "followers_or_subs": subs, "tier": t,
                     "fee_low_thb_youtube": round(fee_low, 2), "size_fits_pilot_fee_scale": bool(size_ok),
                     "category_hypeauditor": cat, "latest_video_er_pct": er, "latest_video_date": last, "genre_read": genre,
                     "award_note": award, "audience_fit": fit, "brand_safety": safety, "format_fit": fmt, "total": total,
                     "controversy_check": CONTROVERSY.get(name, "not run (required before any approach)"),
                     "points": {"genre": fit_genre, "adult_directed": 1 if adult else 0, "no_alcohol_cue_in_titles": s1,
                                "not_weight_or_medical": s2, "not_child_directed": s3, "consumption_or_demo_format": f1,
                                "recent_post": f2, "size_fits_pilot": size_ok},
                     "brand_safety_status": "provisional: alcohol-cue and child-direction points rest on the titles or topics read (for some rows one title only); controversy check " + ("run (one search, nothing relevant surfaced; leads not opened)" if name in CONTROVERSY else "not run"),
                     "band": band})
    rows.sort(key=lambda r: (-r["total"], -r["format_fit"], r["name"]))
    return rows


def band_members(rows):
    bands = {}
    for r in rows:
        bands.setdefault(r["band"], []).append(r["name"])
    return bands


def parse_num(s):
    s = s.strip().replace(",", "")
    mult = 1.0
    if s.endswith("M"):
        mult, s = 1e6, s[:-1]
    elif s.endswith("K"):
        mult, s = 1e3, s[:-1]
    return float(s) * mult


def read_tiktok_table(path):
    """Reads the 50-row TikTok table in raw 09 section 2 (HypeAuditor top 50, per-post averages)."""
    out = []
    inside = False
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("## 2. TikTok creators"):
                inside = True
                continue
            if inside and line.startswith("## 3."):
                break
            if not inside or not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 7 or cells[0] in ("Handle",) or cells[0].startswith("---"):
                continue
            out.append({"handle": cells[0], "name": cells[1], "followers": parse_num(cells[2]),
                         "views": parse_num(cells[3]), "likes": parse_num(cells[4]),
                         "comments": parse_num(cells[5]), "shares": parse_num(cells[6])})
    return out


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def tiktok_stats():
    tt = read_tiktok_table(RAW09)
    big = [r for r in tt if r["followers"] >= 100_000]
    vf = [r["views"] / r["followers"] for r in big]
    eng_f = [(r["likes"] + r["comments"] + r["shares"]) / r["followers"] for r in big]
    eng_v = [(r["likes"] + r["comments"] + r["shares"]) / r["views"] for r in big]
    return {
        "source": "raw 09 section 2 (HypeAuditor top 50 TikTok, per-post averages; ranked by the aggregator)",
        "rows_parsed": len(tt),
        "accounts_100k_plus": len(big),
        "views_to_followers_median": round(median(vf), 3),
        "views_to_followers_min": round(min(vf), 3),
        "views_to_followers_max": round(max(vf), 2),
        "likes_comments_shares_pct_of_followers_median": round(100 * median(eng_f), 1),
        "likes_comments_shares_pct_of_views_median": round(100 * median(eng_v), 1),
        "caution": "Ranked by the aggregator, which favours very high per-post averages; upper bounds for a typical creator of the same size.",
    }


rows_base = score_rows(SCENARIOS["baseline"])
bands_base = band_members(rows_base)
tiers = {}
for r in rows_base:
    tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1

sensitivity = {}
for key, scn in SCENARIOS.items():
    rr = score_rows(scn)
    bm = band_members(rr)
    sensitivity[key] = {
        "settings": scn,
        "band_counts": {k: len(v) for k, v in bm.items()},
        "priority_candidates": [r["name"] for r in rr if r["band"].startswith("Priority")],
    }

unscored = [
    {"handle": "cardncyn", "name_shown": "Carddd", "platform": "TikTok", "followers": 12.4e6, "avg_views": 2.0e6, "evidence": "Best Affiliate 2024 (1st)"},
    {"handle": "win.william_official", "name_shown": "Win William", "platform": "TikTok", "followers": 31.7e6, "avg_views": 2.5e6, "evidence": "Best Affiliate 2024 (3rd)"},
    {"handle": "iamsungstarwin", "name_shown": "Sungstarwin", "platform": "TikTok", "followers": 8.1e6, "avg_views": 1.3e6, "evidence": "Best Creatorpreneur 2025 (1st)"},
    {"handle": "psiscott", "name_shown": "ทราย สมุทร", "platform": "TikTok", "followers": 1.6e6, "avg_views": 787.8e3, "evidence": "Japan Expo, Green and Sustainable 2025"},
    {"handle": "domkao", "name_shown": "ดมข้าว [Domkao]", "platform": "TikTok", "followers": 2.0e6, "avg_views": 2.7e6, "evidence": "genre not verified"},
    {"handle": "spriteder_spd", "name_shown": "SPD No.1", "platform": "TikTok", "followers": 11e6, "avg_views": 2.3e6, "evidence": "YouTube category DIY & Life Hacks, Toys (child-leaning)"},
    # Named on award pages (genre evidence only); follower tier NOT read (vidIQ handle pages returned the popular-channels list).
    {"handle": "jamyjamess", "name_shown": "jamyjamess", "platform": "YouTube (assumed)", "followers": None, "avg_views": None, "evidence": "Best Foodie 2025 (2nd); tier not read"},
    {"handle": "paratt_", "name_shown": "paratt_", "platform": "YouTube (assumed)", "followers": None, "avg_views": None, "evidence": "Best Foodie 2025 (3rd); tier not read"},
    {"handle": "pangboyz", "name_shown": "pangboyz", "platform": "YouTube (assumed)", "followers": None, "avg_views": None, "evidence": "Best Gaming 2026 (2nd); tier not read"},
    {"handle": "GUFUNNAROCK", "name_shown": "GUFUNNAROCK", "platform": "YouTube", "followers": 371e3, "avg_views": None, "evidence": "Best Gaming 2025 (1st); 371K is a third-party estimate (Net Worth Spot, 1 October 2026); no title read"},
    {"handle": "Foodie.Munchies", "name_shown": "Foodie.Munchies", "platform": "Instagram", "followers": 1128907, "avg_views": None, "evidence": "CreatorDB: Thailand, Food and Cooking, Instagram 1,128,907, engagement rate 1.0 percent (refreshed 4 October 2026); no titles read"},
    {"handle": "J100.Kg", "name_shown": "J100.Kg", "platform": "not shown", "followers": None, "avg_views": None, "evidence": "CreatorDB: Thailand, Food and Cooking, engagement rate 5.8 percent (refreshed 2 October 2026); follower count not shown in the extract"},
]

res = {
    "rule": {
        "audience_fit_0_3": "genre 2 on-target (food or drink, gaming, sports, fitness), 1 adjacent, 0 off; plus 1 if adult-directed per the page evidence",
        "brand_safety_0_3": "1 no alcohol cue in the titles read; 1 not centred on weight loss, body shaping or medical advice; 1 not child-directed",
        "format_fit_0_3": "1 format already shows eating, tasting or a hands-on demonstration; 1 latest video on or after 17 Sep 2026; 1 lower-bound YouTube fee for its tier at or below the pilot fee cut-off (THB 40,000, ASSUMPTION)",
        "bands": "Priority candidate: total 8 or 9, with the fee point and the demonstration point. Reference: total 8 or 9 without the fee point (above the pilot fee scale). Reserve: total 8 or 9 with the fee point but no demonstration point, or total 6 or 7. Not recommended: 5 or less.",
        "gates": "A Priority candidate is not approached until (a) a full public record check (Thai and English news, the creator's own posts, listed brand partners) and (b) a check of any current alcohol-brand contract are documented. The controversy search in the record is one search per creator and is a lead check only.",
        "assumptions": "The 500,000 mid and macro split and the THB 40,000 fee cut-off are ASSUMPTIONS. Under the Influencer Marketing Hub follower definition (macro 100,000 to 1,000,000; no mid band, S) or at a THB 33,000 cut-off, no row is a Priority candidate (see sensitivity).",
        "brand_safety": "provisional for every row; the controversy search was run for five rows only (one search each; leads not opened)",
        "fx": "THB per USD %s (Bank of Thailand reference rate, 15 October 2026, P)" % FX,
        "limits": "No creator-level audience age or gender was readable; no TikTok or micro-tier profile sweep was run; points are given only for what was read.",
    },
    "rows": rows_base,
    "band_counts": {k: len(v) for k, v in bands_base.items()},
    "band_members": bands_base,
    "tier_counts": tiers,
    "sensitivity": sensitivity,
    "tiktok_top50_statistics": tiktok_stats(),
    "tiktok_unscored": unscored,
    "brief_coverage": {
        "scored_rows": len(rows_base),
        "platform_counts": {"YouTube": sum(1 for r in rows_base if r["platform"] == "YouTube"), "TikTok": 0, "Instagram": 0},
        "tier_counts": tiers,
        "priority_candidate_tiers": sorted({r["tier"] for r in rows_base if r["band"].startswith("Priority")}),
        "statement": "Count met: 22 scored against a brief of at least 20. Platform coverage not met: every scored row is a YouTube channel; TikTok and Instagram accounts are listed unscored. Micro tier: none scored. Campaign option B funds nano and micro creators only, so no scored row is funded under option B; the Priority candidate is a candidate for the optional mid-tier video in option A, which is cut first, and only under the baseline settings.",
    },
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("wrote", OUT)
for r in rows_base:
    print("%2d | %-30s | %-6s | fit %d safety %d format %d | %s" % (r["total"], r["name"], r["tier"], r["audience_fit"], r["brand_safety"], r["format_fit"], r["band"]))
print("baseline", res["band_counts"], tiers)
for k, v in sensitivity.items():
    print("sensitivity", k, v["band_counts"], v["priority_candidates"])
print("tiktok", res["tiktok_top50_statistics"])
