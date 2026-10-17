"""Price-basis and 20 percent test model for the can concepts (Singapore and Korea).

Two readings of the 20 percent test:
  U (unit margin): net contribution per can / CIF price >= 20 percent.
  A (fixed-cost absorption at volume V): (net contribution per can - fixed cost / V) / CIF >= 20 percent.

Price basis: the category CIF value is a customs average (Comtrade HS 220210, CIF convention for imports),
the importer's purchase price across all Thai brands in that heading. A premium product's CIF is a
separate question; the sweep below covers the full range.

Inputs come from strategy/data/assumptions.json (status recorded there). Run from the strategy folder:
  python code/price_basis_model.py
Outputs: data/price_basis_sweep.csv and data/price_basis_thresholds.csv.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
A = json.loads((HERE / "data" / "assumptions.json").read_text(encoding="utf-8"))
TRADE = 0.10  # trade spend share of CIF (assumption, range 5 to 20 percent)
TARGET = 0.20  # 20 percent test


def exporter_cost_sg():
    p = A["singapore"]
    freight = p["freight_20ft_usd"]["value"] / (p["cartons_per_20ft"]["value"] * p["cans_per_carton"]["value"]) * p["usd_sgd"]["value"]
    return p["exworks_usd_per_can"]["value"] * p["usd_sgd"]["value"] + freight + p["insurance_sgd_per_can"]["value"]


def exporter_cost_kr():
    p = A["korea"]
    freight = p["freight_20ft_usd"]["value"] / (p["cartons_per_20ft"]["value"] * 24) * p["usd_krw"]["value"]
    return p["exworks_usd_per_can"]["value"] * p["usd_krw"]["value"] + freight + p["insurance_krw_per_can"]["value"]


MARKETS = {
    "singapore": {"cost": exporter_cost_sg(), "fixed": A["singapore"]["fixed_cost_sgd_per_year"]["value"],
                  "cat_cans": A["singapore"]["category_volume_cans"]["value"], "unit": "S$", "cif_grid": [round(0.30 + 0.02 * i, 2) for i in range(21)],
                  "customs_mid": A["singapore"]["cif_realised_sgd_per_can"]["value"],
                  "customs_low": A["singapore"]["cif_realised_sgd_per_can"]["low"], "customs_high": A["singapore"]["cif_realised_sgd_per_can"]["high"]},
    "korea": {"cost": exporter_cost_kr(), "fixed": A["korea"]["fixed_cost_krw_per_year"]["value"],
              "cat_cans": A["korea"]["category_volume_cans"]["value"], "unit": "KRW", "cif_grid": [int(400 + 25 * i) for i in range(21)],
              "customs_mid": A["korea"]["cif_realised_krw_per_can"]["value"],
              "customs_low": A["korea"]["cif_realised_krw_per_can"]["low"], "customs_high": A["korea"]["cif_realised_krw_per_can"]["high"]},
}


def net_per_can(cif, cost):
    return cif * (1 - TRADE) - cost


def test_unit(cif, cost):
    return net_per_can(cif, cost) / cif >= TARGET


def test_absorption(cif, cost, fixed, volume):
    return (net_per_can(cif, cost) - fixed / volume) / cif >= TARGET


def required_cif_unit(cost):
    # CIF such that (cif * (1 - TRADE) - cost) / cif = TARGET  =>  cif = cost / (1 - TRADE - TARGET)
    return cost / (1 - TRADE - TARGET)


def required_cif_absorption(cost, fixed, volume):
    return (cost + fixed / volume) / (1 - TRADE - TARGET)


def main():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    sweep_rows = []
    for mkt, m in MARKETS.items():
        for cif in m["cif_grid"]:
            n = net_per_can(cif, m["cost"])
            row = {"market": mkt, "cif_per_can": cif, "net_per_can": round(n, 4), "net_pct_cif": round(n / cif, 4),
                   "unit_test_pass": test_unit(cif, m["cost"])}
            for v in (1_000_000, 3_000_000, 5_000_000, 10_000_000):
                row[f"absorption_pass_{v // 1_000_000}m_cans"] = test_absorption(cif, m["cost"], m["fixed"], v)
            sweep_rows.append(row)
    with (out / "price_basis_sweep.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(sweep_rows[0].keys()))
        w.writeheader()
        w.writerows(sweep_rows)

    thr_rows = []
    for mkt, m in MARKETS.items():
        row = {"market": mkt, "unit": m["unit"], "exporter_cost": round(m["cost"], 4),
               "required_cif_unit_reading": round(required_cif_unit(m["cost"]), 4),
               "customs_mid": m["customs_mid"], "customs_low": m["customs_low"], "customs_high": m["customs_high"]}
        for v in (1_000_000, 3_000_000, 5_000_000, 10_000_000):
            row[f"required_cif_absorption_{v // 1_000_000}m_cans"] = round(required_cif_absorption(m["cost"], m["fixed"], v), 4)
        row["customs_mid_passes_unit"] = test_unit(m["customs_mid"], m["cost"])
        row["customs_mid_passes_absorption_5m"] = test_absorption(m["customs_mid"], m["cost"], m["fixed"], 5_000_000)
        thr_rows.append(row)
    with (out / "price_basis_thresholds.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(thr_rows[0].keys()))
        w.writeheader()
        w.writerows(thr_rows)

    for r in thr_rows:
        print(json.dumps(r, ensure_ascii=False))
    print("wrote", out / "price_basis_sweep.csv", "and", out / "price_basis_thresholds.csv")


if __name__ == "__main__":
    main()
