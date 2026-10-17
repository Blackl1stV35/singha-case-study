"""Fetch SingStat T010001 monthly merchandise imports for HS 2202 and save raw responses.

Source: SingStat Table Builder, T010001 (Merchandise Trade Value by Commodity and Market, Monthly).
Units: thousand Singapore dollars (as published).
Run from the strategy folder: python code/fetch_singstat_hs2202.py
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
RAW = HERE / "raw" / "singstat"
OUT = HERE / "data" / "singstat_hs2202_monthly_imports_2023_2026.csv"
BASE = "https://tablebuilder.singstat.gov.sg/api/table/tabledata/T010001"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
PERIODS = [f"{y} {m}" for y in range(2023, 2027) for m in MONTHS]
PERIODS = PERIODS[: PERIODS.index("2026 Sep") + 1]
MARKETS = {"WORLD": "world", "THAILAND": "thailand", "MALAYSIA": "malaysia"}


def fetch(period):
    tf = urllib.parse.quote(period)
    url = f"{BASE}?timeFilter={tf}&limit=5000&search=AERATED"
    last_err = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as err:  # retry on any transient error
            last_err = err
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"failed {period}: {last_err}")


def value_of(raw):
    try:
        return float(str(raw).replace(",", ""))
    except ValueError:
        return None


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    table = {}
    for period in PERIODS:
        name = period.replace(" ", "_")
        path = RAW / f"T010001_{name}.json"
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
        else:
            payload = fetch(period)
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            time.sleep(1)
        row_map = {}
        for r in payload["Data"]["rows"]:
            if r["tradeType"] != "IMPORTS" or r["market"] not in MARKETS:
                continue
            tag = MARKETS[r["market"]]
            hs4 = r["hs4Products"][:4]
            hs6 = r["hs6Products"][:6]
            hs8 = r["hs8Products"][:8]
            # Keep only the total row for each heading. 8-digit breakdown rows share the
            # 6-digit label and would otherwise overwrite the total.
            if hs8 != "":
                continue
            if hs4 == "2202" and hs6 == "":
                row_map[f"{tag}_2202"] = value_of(r["value"])
            elif hs6 == "220210":
                row_map[f"{tag}_220210"] = value_of(r["value"])
            elif hs6 == "220299":
                row_map[f"{tag}_220299"] = value_of(r["value"])
        table[period] = row_map

    cols = [
        "world_2202", "world_220210", "world_220299",
        "thailand_2202", "thailand_220210", "thailand_220299",
        "malaysia_2202", "malaysia_220210", "malaysia_220299",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["period", "year", "month"] + cols + ["unit"])
        for period in PERIODS:
            y, m = period.split(" ")
            vals = [table[period].get(c) for c in cols]
            w.writerow([period, y, m] + vals + ["thousand SGD"])
    print("wrote", OUT, "rows:", len(PERIODS))


if __name__ == "__main__":
    main()
