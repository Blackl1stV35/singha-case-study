"""T3 re-run checks for the Sermsuk listing status and the est and Sermsuk arithmetic (20 October 2026).

Inputs are typed from primary sources saved in rework/raw/diligence_2026-10-20/T3/:
- ThaiBev SGX announcement, 27 November 2024 (thaibev_sgx_27nov2024_and_agm_2025_minutes_2026-10-20.md, section A)
- Sermsuk 2025 AGM minutes, 30 January 2025, pages 2 and 14 (same file, section B)
- Sermsuk Form 250-2 and the SET MD&A figures (saved T3 files, read earlier)
- Brand Buffet 27 August 2024 maximum tender value of THB 5,918 million (secondary, cross-check only)

No random numbers. Output: t3_rerun_listing_checks_results.json next to this script.

Fourth pass (20 October 2026): the source of the maximum tender share count is now the 3 July 2024 ThaiBev
announcement and Form 250-2 page 10 (P), not a notice that is not saved. A check that the maximum value equals the
Form 250-2 total (THB 5,918,577,840) was added.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

ISSUED_SHARES = 265_900_484          # AGM minutes 30 Jan 2025, page 2 (P)
ATTENDING_SHARES_AGM = 263_742_657   # AGM minutes 30 Jan 2025, page 2 (P)
TENDER_ACCEPTED = 91_786_404         # ThaiBev SGX announcement 27 Nov 2024 (P)
HOLDING_AFTER_TENDER = 263_741_208   # ThaiBev SGX announcement 27 Nov 2024 (P)
TENDER_MAX_SHARES = 93_945_680       # 3 Jul 2024 ThaiBev announcement for the remaining shares (P; printed in raw/diligence_2026-10-20/T3/thaibev_sgx_announcements_sermsuk_2024.md, line 27); Form 250-2 page 10 gives the total below (P)
FORM250_MAX_TOTAL_THB = 5_918_577_840  # Form 250-2 page 10 (P): maximum offer total in baht (saved in sermsuk_form250_2_opinion_2024-10-08_extracts.md, lines 143 and 179)
OFFER_PRICE_THB = 63                 # 3 Jul 2024 offer price (P)
BRAND_BUFFET_MAX_VALUE_MN = 5_918    # Brand Buffet 27 Aug 2024 (S, cross-check)

# Sermsuk FY2024 year to 30 Sep 2024 (AGM minutes page 14 for revenue, cost, distribution, net; SET MD&A for gross profit)
REV_FY24 = 13_153
COGS_FY24 = 9_306
GP_FY24 = 3_847
DIST_FY24 = 3_033
NET_FY24 = 404
NET_FY23 = 248                       # Sermsuk MD&A FY2023 (P), and 404 - 156 = 248 from page 14
NET_CHANGE_FY24 = 156                # AGM minutes page 14 (P)

# Suntory Beverage & Food, Asia Pacific segment, FY2022 (P, securities report PDF page 31)
SBF_APAC_REV_FY22_BN = 359.4
SBF_APAC_PROFIT_FY22_BN = 56.4
# Snippet only (NOT opened, not used as a figure): FY2023 segment profit JPY 43.1 billion
SNIPPET_SBF_APAC_PROFIT_FY23_BN = 43.1

results = {}

results["sermsuk_shares"] = {
    "issued_shares": ISSUED_SHARES,
    "accepted_tender_pct_of_issued": round(100 * TENDER_ACCEPTED / ISSUED_SHARES, 2),
    "holding_after_tender_pct_of_issued": round(100 * HOLDING_AFTER_TENDER / ISSUED_SHARES, 2),
    "agm_attending_pct_of_issued": round(100 * ATTENDING_SHARES_AGM / ISSUED_SHARES, 4),
    "max_tender_pct_of_issued": round(100 * TENDER_MAX_SHARES / ISSUED_SHARES, 2),
    "holding_after_tender_as_printed_pct": 99.19,
    "check_holding_rounds_to_printed": round(100 * HOLDING_AFTER_TENDER / ISSUED_SHARES, 2) == 99.19,
}

cost_accepted_thb = OFFER_PRICE_THB * TENDER_ACCEPTED
cost_max_thb = OFFER_PRICE_THB * TENDER_MAX_SHARES
results["tender_value_thb"] = {
    "accepted_value_thb": cost_accepted_thb,
    "accepted_value_thb_million": round(cost_accepted_thb / 1_000_000, 1),
    "max_value_thb_million": round(cost_max_thb / 1_000_000, 1),
    "check_max_truncates_to_brand_buffet_5918": int(cost_max_thb / 1_000_000) == BRAND_BUFFET_MAX_VALUE_MN,
    "note": "DERIVED: price times shares. Brand Buffet's 5,918 million equals the derived 5,918.6 million truncated to whole millions (cross-check only, S).",
    "max_value_thb_exact": cost_max_thb,
    "form250_page10_total_thb": FORM250_MAX_TOTAL_THB,
    "max_value_equals_form250_total": cost_max_thb == FORM250_MAX_TOTAL_THB,
}

# So Water's holding before the tender offer. The 3 July 2024 ThaiBev announcement gives the record date 6 December 2023;
# the 15 November 2024 ThaiBev notice gives the record date 17 July 2024. Both state 64.67 per cent (P, saved in
# raw/diligence_2026-10-20/T3/thaibev_sgx_announcements_sermsuk_2024.md).
SO_WATER_SHARES_RECORD_6DEC2023 = 171_954_804
results["so_water_holding_before_tender_check"] = {
    "record_date_6_dec_2023_pct_of_issued": round(100 * SO_WATER_SHARES_RECORD_6DEC2023 / ISSUED_SHARES, 2),
    "record_date_6_dec_2023_as_printed_pct": 64.67,
    "record_date_17_jul_2024_as_printed_pct": 64.67,
    "note": "Same percentage at two record dates (6 Dec 2023 in the 3 Jul 2024 announcement; 17 Jul 2024 in the 15 Nov 2024 notice). The date basis is stated in the record.",
}

gm_fy24 = 100 * GP_FY24 / REV_FY24
results["sermsuk_fy24_checks"] = {
    "gross_profit_check_rev_minus_cogs": REV_FY24 - COGS_FY24,
    "gross_profit_check_matches_printed": (REV_FY24 - COGS_FY24) == GP_FY24,
    "gross_margin_pct": round(gm_fy24, 2),
    "net_margin_pct": round(100 * NET_FY24 / REV_FY24, 2),
    "distribution_share_of_sales_pct": round(100 * DIST_FY24 / REV_FY24, 2),
    "net_fy23_from_fy24_minus_change": NET_FY24 - NET_CHANGE_FY24,
    "net_fy23_matches_mda": (NET_FY24 - NET_CHANGE_FY24) == NET_FY23,
    "net_change_pct_yoy": round(100 * NET_CHANGE_FY24 / NET_FY23, 1),
}

# Third pass (20 October 2026): the Suntory Asia Pacific FY2023 figure is now read from the FY2023 annual securities
# report on EDINET (P), so the snippet is no longer used. The FY2023 report moved Africa from Asia Pacific to Europe and
# restated FY2022 to 57,731 million yen of segment profit on 352,615 million yen of external revenue.
SBF_APAC_FY22_RESTATED_REV_MN = 352_615
SBF_APAC_FY22_RESTATED_PROFIT_MN = 57_731
SBF_APAC_FY23_REV_MN = 371_435
SBF_APAC_FY23_PROFIT_MN = 43_075
SBF_APAC_FY24_REV_MN = 402_049
SBF_APAC_FY24_PROFIT_MN = 45_404
SBF_APAC_FY25_REV_MN = 394_057
SBF_APAC_FY25_PROFIT_MN = 42_516
results["sbf_apac_definition_check_p"] = {
    "fy22_original_margin_pct": round(100 * SBF_APAC_PROFIT_FY22_BN / SBF_APAC_REV_FY22_BN, 2),
    "fy22_restated_margin_pct": round(100 * SBF_APAC_FY22_RESTATED_PROFIT_MN / SBF_APAC_FY22_RESTATED_REV_MN, 2),
    "fy23_margin_pct": round(100 * SBF_APAC_FY23_PROFIT_MN / SBF_APAC_FY23_REV_MN, 2),
    "fy24_margin_pct": round(100 * SBF_APAC_FY24_PROFIT_MN / SBF_APAC_FY24_REV_MN, 2),
    "fy25_margin_pct": round(100 * SBF_APAC_FY25_PROFIT_MN / SBF_APAC_FY25_REV_MN, 2),
    "fy23_vs_fy22_restated_profit_change_pct": round(
        100 * (SBF_APAC_FY23_PROFIT_MN / SBF_APAC_FY22_RESTATED_PROFIT_MN - 1), 1),
    "fy23_vs_fy22_restated_profit_change_as_printed_pct": -25.4,
    "fy23_snippet_43_1_matches_p_fy23_profit": round(SNIPPET_SBF_APAC_PROFIT_FY23_BN, 1) == round(SBF_APAC_FY23_PROFIT_MN / 1000, 1),
    "fy25_profit_snippet_45_0_superseded": "The earlier snippet said JPY 45.0 billion; the annual report says JPY 42.5 billion (42,516 million).",
    "note": "PROXY for the Pepsi bottler: Asia Pacific segment (Vietnam, Thailand, Indonesia, Oceania, health foods). "
            "Segment profit ratio, not a gross or net margin. The FY2022 original basis includes Africa.",
}

out = HERE / "t3_rerun_listing_checks_results.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(results, ensure_ascii=False, indent=2))
print("written:", out)
