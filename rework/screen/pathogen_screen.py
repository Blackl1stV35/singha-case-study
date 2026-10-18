"""Pathogen and microbial-load screen for the thawed pop.

Physics basis: the Ratkowsky square-root growth model, applied per pathogen with its own cardinal
temperatures, to the bulk temperature history from the thermal screen. Per-serving framing: one 170 mL
serving, starting from one contaminating cell (assumed low-level contamination). Growth is ignored
while frozen. The lag phase is ignored, which is conservative.

All parameters are assumptions: generic cardinal temperatures, relative growth rates, and hazard
thresholds per serving. They are not measurements, and they are not a risk assessment. The output is a
time scale for the 2-hour rule and for the start-load question, not a safety certification.

Run:  python pathogen_screen.py   (writes pathogen_screen_results.json)
"""
import json
import math
import os

import spoilage_screen as sp

HERE = os.path.dirname(os.path.abspath(__file__))
THAI = os.path.join(HERE, "thailand_stress_test_results.json")
OUT = os.path.join(HERE, "pathogen_screen_results.json")

SERVING_G = 170.0          # g or mL per serving (assumed, the pop's drink volume)
C_RAT = 0.2                # Ratkowsky c (assumed, shared)

# name: cardinal temperatures (C), relative growth rate at 30 C (per h, assumed), hazard threshold
# (log10 cells per serving at which the hazard is taken to apply; assumed), and the basis of the threshold.
PATHOGENS = {
    "Salmonella": dict(tmin=5.2, tmax=46.0, mu30=0.8, hazard_log=3.0,
                       basis="low infectious dose; 10^3 per serving taken as the hazard level"),
    "E. coli O157:H7": dict(tmin=7.0, tmax=45.0, mu30=0.8, hazard_log=2.0,
                            basis="very low infectious dose; 10^2 per serving"),
    "Listeria monocytogenes": dict(tmin=-1.5, tmax=45.0, mu30=0.4, hazard_log=2.0,
                                   basis="grows in the cold; 10^2 per serving for susceptible people"),
    "Staphylococcus aureus (enterotoxin)": dict(tmin=7.0, tmax=45.0, mu30=0.6, hazard_log=7.0,
                                                basis="toxin needs about 10^5 CFU/g; 10^7 per serving"),
    "Bacillus cereus (emetic toxin)": dict(tmin=4.0, tmax=48.0, mu30=1.0, hazard_log=7.0,
                                           basis="emetic toxin needs about 10^5 CFU/g; 10^7 per serving"),
}
START_CELLS = 1.0          # cells per serving at the start (single contaminating cell, assumed)


def b_generic(mu30, tmin, tmax):
    return math.sqrt(mu30) / ((30.0 - tmin) * (1.0 - math.exp(C_RAT * (30.0 - tmax))))


def mu_generic(temp_c, b, tmin, tmax):
    if temp_c <= tmin or temp_c >= tmax:
        return 0.0
    return (b * (temp_c - tmin) * (1.0 - math.exp(C_RAT * (temp_c - tmax)))) ** 2


def growth_curve_generic(trace, b, tmin, tmax):
    t = trace["t_s"]
    ts = trace["T_surface_C"]
    tc = trace["T_core_C"]
    hours = [x / 3600.0 for x in t]
    cum = [0.0]
    for i in range(1, len(t)):
        dt_h = (t[i] - t[i - 1]) / 3600.0
        cum.append(cum[-1] + mu_generic(0.5 * (ts[i] + tc[i]), b, tmin, tmax) * dt_h)
    return hours, cum


def first_hour_hazard(hours, cum, need_ln):
    for i in range(1, len(cum)):
        if cum[i] >= need_ln:
            span = cum[i] - cum[i - 1]
            frac = (need_ln - cum[i - 1]) / span if span > 0 else 0.0
            return hours[i - 1] + frac * (hours[i] - hours[i - 1])
    return None


def main():
    with open(THAI, encoding="utf-8") as fh:
        thai = json.load(fh)
    results = {"assumptions": {"serving_g": SERVING_G, "ratkowsky_c": C_RAT, "start_cells_per_serving": START_CELLS,
                               "temperature_proxy": "mean of core and surface, thermal screen",
                               "lag_phase": "ignored (conservative)", "frozen": "no growth"},
               "pathogens": {}, "scenarios": {}, "constant_temperature_hours_to_hazard": {},
               "start_load_sensitivity_hours_at_30C": {}, "two_hour_check": {}, "spoilage_start_load_hours_at_30C": {}}

    for name, p in PATHOGENS.items():
        b = b_generic(p["mu30"], p["tmin"], p["tmax"])
        need_ln = (p["hazard_log"] - math.log10(START_CELLS)) * math.log(10.0)
        results["pathogens"][name] = dict(p, b=round(b, 5), need_ln=round(need_ln, 3))

        # constant temperature table: hours from start (one cell per serving) to hazard
        ct = {}
        for temp in (5.0, 10.0, 20.0, 25.0, 30.0, 35.0, 40.0):
            m = mu_generic(temp, b, p["tmin"], p["tmax"])
            ct["%.0f C" % temp] = round(need_ln / m, 2) if m > 0 else None
        results["constant_temperature_hours_to_hazard"][name] = ct

        # two-hour check at 30 C: cells per serving after 2 h from one cell
        m30 = mu_generic(30.0, b, p["tmin"], p["tmax"])
        results["two_hour_check"][name] = {
            "cells_per_serving_after_2h_at_30C": round(START_CELLS * math.exp(m30 * 2.0), 2),
            "hazard_cells_per_serving": 10 ** p["hazard_log"],
        }

        # start-load sensitivity at 30 C: hours to the hazard for different start loads
        sens = {}
        for log_start in (0.0, 1.0, 2.0, 3.0, 5.0):
            n0 = 10 ** log_start
            if n0 >= 10 ** p["hazard_log"]:
                sens["10^%.0f cells per serving" % log_start] = 0.0   # hazard already present
            elif m30 > 0:
                sens["10^%.0f cells per serving" % log_start] = round(
                    (p["hazard_log"] - log_start) * math.log(10.0) / m30, 2)
        results["start_load_sensitivity_hours_at_30C"][name] = sens

        # scenarios: hours from freezer exit to hazard, from the thermal traces
        for key in ("S1", "S2", "S3", "S4", "S5", "S7", "SU1", "SU2", "SU3", "SU4", "SU5"):
            hours, cum = growth_curve_generic(thai["traces"][key], b, p["tmin"], p["tmax"])
            t_hit = first_hour_hazard(hours, cum, need_ln)
            results["scenarios"].setdefault(key, {"label": thai["scenarios"][key]["label"],
                                                  "window_h": round(hours[-1], 2)})
            results["scenarios"][key][name] = None if t_hit is None else round(t_hit, 2)

    # spoilage start-load sensitivity at 30 C (microbial load question, spoilage organisms)
    mu_spoil = 2.0
    b_s = sp.b_for(mu_spoil)
    for log_start in (1.0, 2.0, 3.0, 4.0, 5.0):
        need = (sp.SPOIL_LOG - log_start) * math.log(10.0)
        m = sp.mu(30.0, b_s)
        results["spoilage_start_load_hours_at_30C"]["10^%.0f CFU/mL" % log_start] = round(need / m, 2)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    print("Pathogen hours from one cell per serving, constant temperature (30 C and 35 C):")
    for name in PATHOGENS:
        ct = results["constant_temperature_hours_to_hazard"][name]
        print("  %-38s 30 C: %s h   35 C: %s h" % (name, ct["30 C"], ct["35 C"]))
    print("Two-hour check (cells per serving after 2 h at 30 C from one cell):")
    for name, v in results["two_hour_check"].items():
        print("  %-38s %s (hazard %s)" % (name, v["cells_per_serving_after_2h_at_30C"], v["hazard_cells_per_serving"]))
    print("Thai scenarios, hours to hazard, one cell per serving:")
    for key in ("S1", "S2", "SU1", "SU2", "SU3", "SU4", "SU5"):
        s = results["scenarios"][key]
        vals = ", ".join("%s %s" % (n.split(" ")[0], s[n]) for n in PATHOGENS)
        print("  %-4s window %.1f h | %s" % (key, s["window_h"], vals))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
