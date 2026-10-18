"""Spoilage screen for the thawed pop: microbial growth after thaw, and leaf wetting.

Physics basis: the square-root (Ratkowsky) growth model with generic mesophile parameters, applied to
the bulk temperature history from the thermal screen (mean of core and surface, no growth below 0 C while
frozen). Lag phase is ignored, which makes the result conservative. All growth parameters and the spoilage
threshold are assumptions, not measurements. The output is a screen, not a shelf-life claim.

Run:  python spoilage_screen.py   (writes spoilage_screen_results.json)
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
THAI = os.path.join(HERE, "thailand_stress_test_results.json")
SUMMER = os.path.join(HERE, "thai_summer_occasions_results.json")
OUT = os.path.join(HERE, "spoilage_screen_results.json")

MU30_CASES = {"conservative (doubling 21 min)": 2.0, "slower (doubling 42 min)": 1.0}  # per hour at 30 C
T_MIN, T_MAX, C_RAT = 0.0, 45.0, 0.2           # Ratkowsky cardinal temperatures (assumed)
SPOIL_LOG = 7.0                                # log10 CFU/mL at spoilage (assumed; visible spoilage about 1e7 to 1e8)
START = {"sealed, 1e2 CFU/mL": 2.0, "outside water wicked in, 1e4 CFU/mL": 4.0}   # log10 start loads (assumed)
SCENARIOS = ["S1", "S2", "S3", "S4", "S5", "S7", "SU1", "SU2", "SU3", "SU4", "SU5"]


def b_for(mu30):
    """Ratkowsky slope so that the growth rate at 30 C equals mu30 (per hour)."""
    return math.sqrt(mu30) / (30.0 * (1.0 - math.exp(C_RAT * (30.0 - T_MAX))))


def mu(temp_c, b):
    """Specific growth rate per hour at temperature temp_c (Ratkowsky square-root model)."""
    if temp_c <= T_MIN or temp_c >= T_MAX:
        return 0.0
    return (b * (temp_c - T_MIN) * (1.0 - math.exp(C_RAT * (temp_c - T_MAX)))) ** 2


def growth_curve(trace, b):
    """Cumulative ln growth (natural log units) and hours since freezer exit at each trace point."""
    t = trace["t_s"]
    ts = trace["T_surface_C"]
    tc = trace["T_core_C"]
    cum = [0.0]
    for i in range(1, len(t)):
        dt_h = (t[i] - t[i - 1]) / 3600.0
        temp = 0.5 * (ts[i] + tc[i])
        cum.append(cum[-1] + mu(temp, b) * dt_h)
    return [x / 3600.0 for x in t], cum


def hours_to_threshold(hours, cum, need_ln):
    """Interpolated hours at which cumulative growth reaches need_ln, or None if not reached."""
    for i in range(1, len(cum)):
        if cum[i] >= need_ln:
            span = cum[i] - cum[i - 1]
            frac = (need_ln - cum[i - 1]) / span if span > 0 else 0.0
            return hours[i - 1] + frac * (hours[i] - hours[i - 1])
    return None


def main():
    with open(THAI, encoding="utf-8") as fh:
        thai = json.load(fh)
    with open(SUMMER, encoding="utf-8") as fh:
        summer = json.load(fh)
    wet_h = {r["key"]: r["external_wet_h"] for r in summer["rows"]}

    results = {"assumptions": {"ratkowsky_Tmin_C": T_MIN, "ratkowsky_Tmax_C": T_MAX, "ratkowsky_c": C_RAT,
                               "spoil_log10_CFU_per_mL": SPOIL_LOG, "mu30_cases_per_h": MU30_CASES,
                               "start_log10_CFU_per_mL": START,
                               "temperature_proxy": "mean of core and surface temperature from the thermal screen",
                               "lag_phase": "ignored (conservative)"},
               "scenarios": {}}
    for key in SCENARIOS:
        tr = thai["traces"][key]
        label = thai["scenarios"][key]["label"]
        window_h = tr["t_s"][-1] / 3600.0
        per = {"label": label, "window_h": round(window_h, 2),
               "external_wet_h": wet_h.get(key), "growth": {}}
        for mu_name, mu30 in MU30_CASES.items():
            b = b_for(mu30)
            hours, cum = growth_curve(tr, b)
            row = {}
            for start_name, start_log in START.items():
                need_ln = (SPOIL_LOG - start_log) * math.log(10.0)
                t_hit = hours_to_threshold(hours, cum, need_ln)
                row[start_name] = {
                    "hours_to_spoilage": None if t_hit is None else round(t_hit, 2),
                    "log10_growth_at_window_end": round(cum[-1] / math.log(10.0), 2),
                }
            per["growth"][mu_name] = row
        results["scenarios"][key] = per
    # Constant-temperature table: hours after thaw to spoilage, independent of the thermal screen
    constant = {}
    for temp in (5.0, 10.0, 20.0, 25.0, 30.0, 35.0, 40.0):
        row = {}
        for mu_name, mu30 in MU30_CASES.items():
            b = b_for(mu30)
            for start_name, start_log in START.items():
                need_ln = (SPOIL_LOG - start_log) * math.log(10.0)
                row["%s | %s" % (mu_name, start_name)] = round(need_ln / mu(temp, b), 2) if mu(temp, b) > 0 else None
        constant["%.0f C" % temp] = row
    results["constant_temperature_hours_to_spoilage"] = constant
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    for temp, row in constant.items():
        print(temp, {k.split(" | ")[0][:12] + " " + k.split(" | ")[1][:8]: v for k, v in row.items()})

    print("scenario, window h, external wet h, then hours to spoilage (conservative mu30=2/h):")
    for key in SCENARIOS:
        s = results["scenarios"][key]
        g = s["growth"]["conservative (doubling 21 min)"]
        sealed = g["sealed, 1e2 CFU/mL"]["hours_to_spoilage"]
        wicked = g["outside water wicked in, 1e4 CFU/mL"]["hours_to_spoilage"]
        print("%-4s %-46s window %.1f h | wet %s h | sealed %s h | wicked-in %s h" % (
            key, s["label"][:46], s["window_h"], s["external_wet_h"], sealed, wicked))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
