"""T68 fix pass checks (20 October 2026).

Purpose: check the figures that the T68 fix pass states or relies on against
(a) the saved pages in rework/raw/diligence_2026-10-20 and (b) the results
files in rework/screen. Each check prints a PASS or FAIL line and is written
to rework/screen/t68_fix_checks_results.json. Nothing is fetched from the web.

Run: python -I rework/screen/t68_fix_checks.py   (from the repo root)
Memory: small; one process; standard library only.
"""

import json
import statistics
from pathlib import Path

ROOT = Path("D:/Workspace/singha-case-study")
RAW = ROOT / "rework" / "raw" / "diligence_2026-10-20"
SCREEN = ROOT / "rework" / "screen"
OUT = SCREEN / "t68_fix_checks_results.json"

saved_checks = []    # saved-page string checks
derived_checks = []  # arithmetic and results-file checks


def read_raw(rel):
    return (RAW / rel).read_text(encoding="utf-8", errors="replace")


def read_any(rel_list):
    """Return the joined text of the listed raw or screen files (missing files are skipped)."""
    parts = []
    for rel in rel_list:
        for base in (RAW, ROOT / "rework"):
            p = base / rel
            if p.exists():
                parts.append(p.read_text(encoding="utf-8", errors="replace"))
                break
    return "\n".join(parts)


def saved_check(cid, files, needle, claim):
    text = read_any(files)
    found = needle in text
    saved_checks.append({
        "id": cid,
        "files": files,
        "needle": needle,
        "claim": claim,
        "found": found,
    })
    print(("PASS" if found else "FAIL"), cid, claim)


def derived_check(cid, value, expected, claim, tol=1e-9):
    ok = abs(value - expected) <= tol
    derived_checks.append({
        "id": cid,
        "value": round(value, 6),
        "expected": expected,
        "claim": claim,
        "pass": ok,
    })
    print(("PASS" if ok else "FAIL"), cid, round(value, 6), "expected", expected, claim)


# ---------------------------------------------------------------------------
# A. Saved-page string checks (figures named in the T68 fix pass)
# ---------------------------------------------------------------------------
saved_check("S01", ["T4/osotspa_financial_highlights.md"], "25,561",
            "Osotspa revenue from sales 2025, 25,561 million baht")
saved_check("S02", ["T4/osotspa_financial_highlights.md"], "3,667",
            "Osotspa profit attributable to owners of the parent 2025, 3,667 million baht")
saved_check("S03", ["T4/thaibev_fy2025_yearend_sgx_extract.md"], "23,694",
            "ThaiBev non-alcoholic gross profit FY2025, 23,694 million baht")
saved_check("S04", ["T4/thaibev_fy2025_yearend_sgx_extract.md"], "64,774",
            "ThaiBev non-alcoholic sales FY2025, 64,774 million baht")
saved_check("S05", ["T4/thaibev_fy2025_yearend_sgx_extract.md"], "5,141",
            "ThaiBev non-alcoholic net profit FY2025, 5,141 million baht (before owners' share)")
saved_check("S06", ["T4/thaibev_fy2025_yearend_sgx_extract.md"], "2,414",
            "ThaiBev non-alcoholic attributable profit FY2025, 2,414 million baht")
saved_check("S07", ["T2/haadthip_ir_pages_2026-10-20.md"], "4,505",
            "Haad Thip total revenue, column 30 June 2026, 4,505 million baht")
saved_check("S08", ["T2/haadthip_ir_pages_2026-10-20.md"], "| 41.90 |",
            "Haad Thip gross margin %, column 30 June 2026, 41.90")
saved_check("S09", ["T2/haadthip_ir_pages_2026-10-20.md"], "| 6.70 |",
            "Haad Thip net margin %, column 30 June 2026, 6.70")
saved_check("S10", ["T3/pepsi_system_moves_and_launches_2012_2026.md"], "กว่า 2,000 ล้านบาท",
            "Suntory PepsiCo: investment over THB 2,000 million for two new Saraburi lines (Thai text)")
saved_check("S11", ["T3/pepsi_system_moves_and_launches_2012_2026.md"], "10 July 2569",
            "Suntory PepsiCo release dated 10 July 2569 (2026)")
saved_check("S12", ["T3/csd_market_share_press_2020_2025.md"], "2025 plan",
            "Pepsi THB 1,000 million 2025 plan (press, Saraburi)")
saved_check("S13", ["T3/csd_market_share_press_2020_2025.md"], "Saraburi carbonated capacity up 50%",
            "Pepsi Saraburi carbonated capacity up 50% (press, 2025)")
saved_check("S14", ["T5/t5_recheck_lazada_priceza_2026-10-20.md"], "16105459253",
            "Sprite Lemon Plus Zero Sugar 24-can listing number 16105459253 (2026 row)")
saved_check("S15", ["T5/t5_recheck_lazada_priceza_2026-10-20.md"], "Coca-Cola Official Store",
            "Sprite Lemon Plus row seller shown as Coca-Cola Official Store (LazMall, via Priceza)")
saved_check("S16", ["T6/04_retail_listings_2026-10-20.md"], "เรดเลมอนโซดา 330 มล. x 6 | 79",
            "Singha Red Lemon Soda six-pack at Makro PRO, THB 79")
saved_check("S17", ["T6/04_retail_listings_2026-10-20.md"], "เลมอน ครีมโซดา 330 มล. x 6 | 79",
            "Singha Lemon Cream Soda six-pack at Makro PRO, THB 79")
saved_check("S18", ["T4/est_cola_thansettakij_2024-03-16_share_and_moves.md"], "อยู่ที่ 26%",
            "est penetration 26 percent before the 2023 rebrand (Thansettakij, 16 March 2024)")
saved_check("S19", ["T4/est_cola_thansettakij_2024-03-16_share_and_moves.md"], "rising to 28%",
            "est penetration rising to 28 percent (no year printed for the 28 percent)")
saved_check("S20", ["T3/csd_market_share_press_2020_2025.md"], "Gen Z is 36%",
            "Gen Z is 36 percent of est customers (Thairath, 15 April 2024)")
saved_check("S21", ["T1/bot_fx_report123_2026-10-20.md"], "33.5410",
            "Bank of Thailand USD reference rate 15 October 2026, 33.5410")
saved_check("S22", ["T3/sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md"], "394,057",
            "Suntory Beverage and Food APAC external revenue FY2025, 394,057 million yen")
saved_check("S23", ["T2/priceza_sprite_2026-10-20.md"], "456",
            "Sprite No Sugar 24-can, CR7 ManU, 456 baht (Priceza row)")
saved_check("S24", ["T5/lotuss_2026-10-20.md"], "332",
            "Sprite 325 mL 24-can at Lotus's, 332 baht (regular, no sugar wording)")
saved_check("S25", ["T5/makro_pro_2026-10-20.md"], "311",
            "Sprite 325 mL 24-can at Makro PRO, 311 baht")
saved_check("S26", ["T2/lotus_singha_lemon_soda_can_2026-10-20.md"], "17.00",
            "Singha Lemon Soda single can at Lotus's, 17.00 baht")
saved_check("S27", ["T1/mitihoon_622207_2026-03-03_hadthip_results.md"], "8,258.4",
            "Haad Thip revenue from sales 2025, 8,258.4 million baht (Mitihoon reprint)")
saved_check("S28", ["T4/68c_cpaxtra_newsroom_own_brand_2025-06-06.md"], "18.5%",
            "Makro own brand products about 18.5 percent of Makro sales (CP Axtra newsroom, 6 June 2025)")
saved_check("S29", ["T5/r27_thaiger_sprite_lemon_plus_2022.md"], "29 ส.ค. 2565",
            "Sprite Lemon Plus 2022 price article dated 29 August 2022")
saved_check("S30", ["T2/tncc_sec_filing_v2_exec_summary_extract.md", "T1/tncc_sec_v2_exec_summary_pages.md"],
            "511,000",
            "ThaiNamthip about 511,000 outlets at 30 June 2025")
saved_check("S31", ["T3/csd_market_share_press_2020_2025.md"], "8.6%",
            "est 8.6 percent volume share (Thansettakij, 16 March 2024)")
saved_check("S32", ["T1/mitihoon_622207_2026-03-03_hadthip_results.md", "T1/haadthip_release_2026-03-25_storythailand.md"],
            "5.6%",
            "Haad Thip FY2025 net profit change of minus 5.6 percent (string '5.6%' present; context read by hand)")

# ---------------------------------------------------------------------------
# B. Results-file checks (script 68e and t5 ladder)
# ---------------------------------------------------------------------------
t5 = json.loads((SCREEN / "t5_retail_price_ladder_results.json").read_text(encoding="utf-8"))
rows = {r["id"]: r for r in t5["rows"]}


def per330(rid):
    return rows[rid]["per_330ml_thb"]


def half_up(x, places):
    """Round half away from zero (the rule the record states), not Python's round-half-even."""
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-places)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))


derived_check("D01", t5["checks"]["rows_passed"], 51, "t5 ladder: 51 of 51 saved-page rows pass (rerun 20 October 2026)")
derived_check("D02", statistics.median([per330(i) for i in t5["sets"]["A_main_all_usable_cans"]]),
              14.0462, "set A main ladder median, 31 can listings (rounded 14.05)", tol=5e-5)
derived_check("D03", statistics.median([per330(i) for i in t5["sets"]["B_direct_retailer_pages"]]),
              13.875, "set B retailer-page multipacks median, 16 rows (rounded 13.88)", tol=1e-9)
derived_check("D04", statistics.median([per330(i) for i in t5["sets"]["D_single_cans"]]),
              16.6231, "set D single-can median, unrounded (rounded 16.62)", tol=5e-5)
derived_check("D05", min(per330(i) for i in t5["sets"]["D_single_cans"]),
              16.2462, "set D single-can minimum (7UP No Sugar and Sprite single at 16.00 per 325 mL)", tol=5e-5)
derived_check("D07", statistics.median([per330(i) for i in t5["sets"]["K_singha_rows_in_main"]]),
              13.7083, "set K Singha rows median recomputed from row values", tol=5e-5)

# Sugar-free 24-can rows from named sellers (68d rule used in the record)
named_sf_24 = ["A05", "D06", "D01", "D12", "A03", "A10"]  # A01 (Sprite Lemon Plus, seller open, C7) excluded
for rid in named_sf_24:
    assert rows[rid]["pack_count"] == 24, rid
derived_check("D08", round(min(per330(i) for i in named_sf_24), 2), 12.40,
              "named-seller sugar-free 24-can range (A01 excluded), minimum (A05 7UP No Sugar)", tol=1e-9)
derived_check("D09", half_up(max(per330(i) for i in named_sf_24), 2), 14.63,
              "named-seller sugar-free 24-can range, maximum (A10 Schweppes lime no sugar; half-up rounding of 14.625)", tol=1e-9)
derived_check("D10", half_up(min(per330(i) for i in named_sf_24 + ["A01"]), 2), 12.40,
              "range if A01 were included: minimum unchanged", tol=1e-9)
derived_check("D11", half_up(max(per330(i) for i in named_sf_24 + ["A01"]), 2), 14.63,
              "range if A01 were included: maximum unchanged (A01 at 14.05 lies inside the range)", tol=1e-9)

# Sugar-free singles
derived_check("D12", per330("S01"), 17.0, "Singha Lemon Soda single can, sugar-free (Lotus's), THB per 330 mL")
derived_check("D13", round(per330("S05"), 4), 16.2462, "7UP No Sugar single can, 325 mL at 16.00, per 330 mL (sugar-free by name)", tol=1e-4)
derived_check("D14", round(per330("S02"), 4), 16.2462, "Sprite single can (regular), 325 mL at 16.00, per 330 mL", tol=1e-4)

# Cube comparisons at THB 15 (planning price ASSUMPTION)
cube = 15.0
main_med = statistics.median([per330(i) for i in t5["sets"]["A_main_all_usable_cans"]])
direct_med = statistics.median([per330(i) for i in t5["sets"]["B_direct_retailer_pages"]])
single_med = statistics.median([per330(i) for i in t5["sets"]["D_single_cans"]])
derived_check("G01", round(cube - main_med, 2), 0.95, "cube minus main median (above by 0.95)", tol=1e-9)
derived_check("G02", round((cube - main_med) / main_med * 100, 1), 6.8, "cube above main median, percent", tol=1e-9)
derived_check("G03", round(cube - direct_med, 3), 1.125, "cube minus retailer-page multipack median (1.125; half-up 1.13)", tol=1e-9)
derived_check("G04", round((cube - direct_med) / direct_med * 100, 1), 8.1, "cube above set B median, percent", tol=1e-9)
derived_check("G05", round(cube - single_med, 4), -1.6231, "cube minus single-can median (below by 1.62)", tol=1e-4)
derived_check("G06", round((cube - single_med) / single_med * 100, 1), -9.8, "cube below single-can median, percent", tol=1e-9)
derived_check("G07", round(cube - per330("S05"), 4), -1.2462, "cube minus 7UP No Sugar single (below by 1.25)", tol=1e-4)
derived_check("G08", round((cube - per330("S05")) / per330("S05") * 100, 1), -7.7, "cube below 7UP No Sugar single, percent", tol=1e-9)
derived_check("G09", round(cube - per330("S01"), 2), -2.0, "cube minus Singha single (below by 2.00)", tol=1e-9)
derived_check("G10", round((cube - per330("S01")) / per330("S01") * 100, 1), -11.8, "cube below Singha single, percent", tol=1e-9)
derived_check("G11", round(cube - per330("A03"), 4), 0.8692, "cube minus Sprite No Sugar 24-can (above by 0.87)", tol=1e-4)

# ---------------------------------------------------------------------------
# C. Margin arithmetic used in the record
# ---------------------------------------------------------------------------
derived_check("M01", 3667 / 25561 * 100, 14.3, "Osotspa attributable margin 2025, 3,667 over 25,561 (one decimal 14.3)", tol=0.05)
derived_check("M02", 23694 / 64774 * 100, 36.58, "ThaiBev non-alcoholic gross margin FY2025 (36.58)", tol=0.005)
derived_check("M03", 5141 / 64774 * 100, 7.94, "ThaiBev non-alcoholic net margin before owners' share (7.94)", tol=0.005)
derived_check("M04", 2414 / 64774 * 100, 3.73, "ThaiBev attributable margin (3.73)", tol=0.005)
derived_check("M05", 568.3 / 8258.4 * 100, 6.88, "Haad Thip net margin, base revenue from sales (6.88, not the printed 6.90)", tol=0.005)
derived_check("M06", 79 / 6, 13.1667, "Singha Red and Lemon Cream six-pack at THB 79 per 330 mL (13.17)", tol=1e-4)
derived_check("M07", 82 / 6, 13.6667, "Singha Lemon six-pack at Makro PRO THB 82 per 330 mL (13.67)", tol=1e-4)

summary = {
    "saved_page_checks": len(saved_checks),
    "saved_page_found": sum(1 for c in saved_checks if c["found"]),
    "saved_page_not_found": [c["id"] for c in saved_checks if not c["found"]],
    "derived_checks": len(derived_checks),
    "derived_pass": sum(1 for c in derived_checks if c["pass"]),
    "derived_fail": [c["id"] for c in derived_checks if not c["pass"]],
}

OUT.write_text(json.dumps({
    "task": "T68 fix pass checks",
    "date_read": "2026-10-20",
    "method": "String presence in saved raw pages (UTF-8), and arithmetic on the t5 ladder results file and the figures in the record. No web access.",
    "saved_page_checks": saved_checks,
    "derived_checks": derived_checks,
    "summary": summary,
}, ensure_ascii=False, indent=2), encoding="utf-8")

print("SUMMARY", json.dumps(summary, ensure_ascii=False))
