"""Price-per-330-mL check for the Coca-Cola system carbonated lines (task T2).

Arithmetic only, no random numbers. Every input is a listing read on 20 October 2026
and saved or quoted in rework/raw/diligence_2026-10-20/T2/ (see the 'source' field).
Per-can price = pack price / can count; per 330 mL = per-can price x 330 / can size.
Run: python coca_cola_system_prices_check.py (writes coca_cola_system_prices_check_results.json here).
"""
import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))

# (label, pack price THB, cans or bottles in pack, can size mL, bundled with another product, source)
LISTINGS = [
    ("Sprite No Sugar 325 mL x 24, Coca-Cola Official Store (LazMall), via Priceza", 334.0, 24, 325, False,
     "Priceza Sprite category page, row 9, read 20 Oct 2026 (raw/T2/priceza_sprite_2026-10-20.md)"),
    ("Sprite No Sugar 325 mL x 24, Lazada listing (seller not stated on page)", 365.0, 24, 325, False,
     "Lazada trending page, read 20 Oct 2026 (raw/T2/retail_prices_2026-10-20.md)"),
    ("Sprite No Sugar 325 mL x 24, Fresh Mart, via Priceza", 414.0, 24, 325, False,
     "Priceza Sprite category page, row 18, read 20 Oct 2026 (raw/T2/priceza_sprite_2026-10-20.md)"),
    ("Sprite No Sugar 325 mL x 24, CR7 ManU, via Priceza", 456.0, 24, 325, False,
     "Priceza Sprite category page, row 10, read 20 Oct 2026 (raw/T2/priceza_sprite_2026-10-20.md)"),
    ("Sprite No Sugar 325 mL x 24, Coca-Cola Official Store, bundled with Halls XS candy", 328.0, 24, 325, True,
     "Priceza Sprite category page, row 22; bundle, excluded from the range"),
    ("Sprite 325 mL single can, Lotus's Shop Online (regular Sprite)", 16.0, 1, 325, False,
     "Lotus's product page, read 20 Oct 2026 (raw/T2/lotus_sprite_can_2026-10-20.md)"),
    ("Schweppes Lime Soda Zero Sugar 330 mL x 6, Makro PRO", 84.0, 6, 330, False,
     "Makro PRO page, read 20 Oct 2026 (raw/T2/retail_prices_2026-10-20.md; captures_2026-10-19/38)"),
    ("Fanta Pineapple 325 mL x 6, Lazada (stated as 6*325 ml)", 85.0, 6, 325, False,
     "Lazada trending page, read 20 Oct 2026 (raw/T2/retail_prices_2026-10-20.md)"),
    ("Coke No Sugar 330 mL x 12, Makro PRO (THB 8.50 unit read on 20 Oct 2026)", 102.0, 12, 330, False,
     "Makro PRO page, read 20 Oct 2026 (raw/T2/retail_prices_2026-10-20.md)"),
]

# Cube planning base case (an ASSUMPTION in the plan, not a sourced price)
CUBE_BASE_THB = 15.0


def per_330(pack_price, count, size_ml):
    per_can = pack_price / count
    return per_can, per_can * 330.0 / size_ml


def main():
    rows = []
    for label, price, count, size, bundled, source in LISTINGS:
        per_can, p330 = per_330(price, count, size)
        rows.append({
            "label": label,
            "pack_price_thb": price,
            "cans_in_pack": count,
            "can_size_ml": size,
            "bundled": bundled,
            "per_can_thb": round(per_can, 2),
            "per_330ml_thb": round(p330, 2),
            "per_litre_thb": round(price / count / size * 1000.0, 1),
            "source": source,
        })

    sprite_ns_24 = [r for r in rows if r["label"].startswith("Sprite No Sugar 325 mL x 24") and not r["bundled"]]
    vals = [r["per_330ml_thb"] for r in sprite_ns_24]
    single = [r for r in rows if r["label"].startswith("Sprite 325 mL single can")][0]
    summary = {
        "sprite_no_sugar_24pack_per_330ml_min": min(vals),
        "sprite_no_sugar_24pack_per_330ml_max": max(vals),
        "sprite_no_sugar_24pack_per_330ml_median": round(statistics.median(vals), 2),
        "sprite_no_sugar_24pack_listings_used": len(vals),
        "sprite_single_can_per_330ml": single["per_330ml_thb"],
        "cube_base_case_thb_per_330ml": CUBE_BASE_THB,
        "cube_minus_24pack_min": round(CUBE_BASE_THB - min(vals), 2),
        "cube_minus_24pack_max": round(CUBE_BASE_THB - max(vals), 2),
        "cube_minus_single_can": round(CUBE_BASE_THB - single["per_330ml_thb"], 2),
        "cube_is_below_listings_count": sum(1 for v in vals if v > CUBE_BASE_THB),
    }
    out = {
        "task": "T2 Coca-Cola system price check, 20 October 2026",
        "method": "per can = pack price / cans; per 330 mL = per can x 330 / can size; no rounding before comparison",
        "rows": rows,
        "summary": summary,
    }
    with open(os.path.join(HERE, "coca_cola_system_prices_check_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("wrote coca_cola_system_prices_check_results.json")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
