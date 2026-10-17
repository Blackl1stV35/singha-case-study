"""Economics for Track A (fibre soda, 330 ml can) and Track D (sparkling botanical tea, 330 ml can).

Route: in-house (group factories) versus partner (co-packer). The exworks cost differs by route.
Price basis: CIF ceiling (what an importer can pay at the shelf price, after its margin, handling and the
BCRS producer fee) and the customs-average CIF (S$0.478 per 330 ml can; KRW 528 per 355 ml can).

Tests:
  K1 (unit margin): net contribution per can (CIF less exporter cost and 10 percent trade spend) is at
     least 20 percent of CIF.
  Gate 2 (operating margin): net contribution less fixed cost per can is at least 20 percent of CIF at the
     stated volume. Volume needed = fixed / (net - 0.20 CIF).

Inputs: strategy/data/assumptions.json for the shared logistics, duty, margins and fixed cost. Track-specific
exworks costs and price points are assumptions (labelled). Run from the strategy folder:
  python code/track_economics.py
Outputs: data/track_economics.csv
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
A = json.loads((HERE / "data" / "assumptions.json").read_text(encoding="utf-8"))
TRADE = 0.10
CAT_SG = A["singapore"]["category_volume_cans"]["value"]
CAT_KR = A["korea"]["category_volume_cans"]["value"]

# Track-specific exworks cost (USD per can), assumptions. Partner adds a co-packer margin.
EXW = {
    ("A", "in_house"): 0.22,
    ("A", "partner"): 0.25,
    ("D", "in_house"): 0.28,
    ("D", "partner"): 0.32,
}
# In-house shares the group's fixed cost (assumption: 300k vs 450k standalone); partner keeps standalone.
FIXED_SG = {"in_house": 300_000, "partner": 450_000}
FIXED_KR = {"in_house": 400_000_000, "partner": 500_000_000}

PRICE_SG = {"A": [2.00, 2.25, 2.50], "D": [2.50, 3.00, 3.50]}
PRICE_KR = {"A": [1650, 1800, 2000], "D": [2500, 2750, 3000]}


def sg_ceiling(shelf):
    p = A["singapore"]
    ex_gst = shelf / (1 + p["gst_rate"]["value"])
    buy = ex_gst * (1 - p["retailer_margin"]["value"])
    imp = buy * (1 - p["importer_margin"]["value"])
    return imp - p["importer_handling_sgd_per_can"]["value"] - p["bcrs_producer_fee_sgd_per_can"]["value"]


def sg_cost(track, route):
    p = A["singapore"]
    freight = p["freight_20ft_usd"]["value"] / (p["cartons_per_20ft"]["value"] * p["cans_per_carton"]["value"]) * p["usd_sgd"]["value"]
    return EXW[(track, route)] * p["usd_sgd"]["value"] + freight + p["insurance_sgd_per_can"]["value"]


def kr_ceiling(shelf):
    p = A["korea"]
    ex_vat = shelf / (1 + p["vat_rate"]["value"])
    buy = ex_vat * (1 - p["retailer_margin"]["value"])
    imp = buy * (1 - p["importer_margin"]["value"])
    return (imp - p["importer_handling_krw_per_can"]["value"]) / (1 + p["tariff_rate"]["value"])


def kr_cost(track, route):
    p = A["korea"]
    freight = p["freight_20ft_usd"]["value"] / (p["cartons_per_20ft"]["value"] * 24) * p["usd_krw"]["value"]
    return EXW[(track, route)] * p["usd_krw"]["value"] + freight + p["insurance_krw_per_can"]["value"]


def row(market, track, route, shelf, cif, basis, cost, fixed, cat):
    net = cif * (1 - TRADE) - cost
    k1 = net / cif
    gap = net - 0.20 * cif
    vol = fixed / gap if gap > 0 else None
    return {
        "market": market, "track": track, "route": route, "shelf_price": shelf, "cif_basis": basis,
        "cif_per_can": round(cif, 4), "exporter_cost_per_can": round(cost, 4),
        "net_per_can": round(net, 4), "k1_net_pct_cif": round(k1, 4), "k1_pass": k1 >= 0.20,
        "fixed_cost": fixed, "volume_for_20pct_operating_margin": round(vol) if vol else "not reachable",
        "volume_share_of_category": round(vol / cat, 5) if vol else "not reachable",
    }


def main():
    out = []
    for track in ["A", "D"]:
        for route in ["in_house", "partner"]:
            for shelf in PRICE_SG[track]:
                cost = sg_cost(track, route)
                ceil = sg_ceiling(shelf)
                out.append(row("singapore", track, route, shelf, ceil, "ceiling", cost, FIXED_SG[route], CAT_SG))
                out.append(row("singapore", track, route, shelf, A["singapore"]["cif_realised_sgd_per_can"]["value"], "customs_avg", cost, FIXED_SG[route], CAT_SG))
            for shelf in PRICE_KR[track]:
                cost = kr_cost(track, route)
                ceil = kr_ceiling(shelf)
                out.append(row("korea", track, route, shelf, ceil, "ceiling", cost, FIXED_KR[route], CAT_KR))
                out.append(row("korea", track, route, shelf, A["korea"]["cif_realised_krw_per_can"]["value"], "customs_avg", cost, FIXED_KR[route], CAT_KR))
    path = HERE / "data" / "track_economics.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(r["market"], r["track"], r["route"], r["shelf_price"], r["cif_basis"], "CIF", r["cif_per_can"], "net%", r["k1_net_pct_cif"], "K1", r["k1_pass"], "vol", r["volume_for_20pct_operating_margin"])
    print("wrote", path)


if __name__ == "__main__":
    main()
