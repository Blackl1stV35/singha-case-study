"""Thai summer occasions: does the thaw and leak picture still hold?

Runs the summer-occasion scenarios (SU1-SU5) and the two street baselines (S1, S2) through the
thermal model in thailand_stress_test.py, then applies the Washburn screen twice:
  internal  the drink wicks out of a damaged path once the surface has melted (drink properties,
            conservative lower bound: viscosity 1 mPa s, surface tension 0.072 N/m)
  external  water on the outside of the wrap wicks into a damaged path while the surface stays wet
            (water properties at the occasion's temperature; wet time from the scenario)

Output is a threshold r*: the smallest damaged-path radius that wicks the 100 mm wrap within the time
available (paths at or above r* leak). A higher r* means more margin. The threshold assumes only the
bottom edge is wet and the liquid must climb the full height. If a film or pool reaches the top of the
wrap, there is no climb and the threshold does not protect; those rows are flagged top_wetted.
The damaged-path size is not measured, so this is not a leak probability.
Run:  python thai_summer_occasions.py   (writes thai_summer_occasions_results.json and rework/24_thai_summer_occasions.png)
"""
import json
import math
import os
import time

import numpy as np

import thailand_stress_test as s

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "thai_summer_occasions_results.json")
OUT_PNG = os.path.join(HERE, "..", "24_thai_summer_occasions.png")
H_WRAP = 0.100                              # m, wrap height: climb to the top of the wrap
WINDOW_S = 2 * 3600.0                       # s, consumption window counted from the freezer
COS_MEAS = math.cos(math.radians(76.08))    # adaxial contact angle, measured (rework/16)
COS_WETTABLE = math.cos(math.radians(60.0)) # more wettable envelope (assumption)
T_DEW = 24.8                                # C, Bangkok Mar-May mean dew point (TMD 48455, 1991-2020)
P_NOM = dict(h=10.0, k_s=2.2, cp_s=2000.0, L=300e3, Tf=-1.0)
ETA_DRINK, GAMMA_DRINK = 1.0e-3, 0.072      # Pa s, N/m: lower-bound viscosity, upper-bound surface tension
CASES = ["S1", "S2", "SU1", "SU2", "SU3", "SU4", "SU5"]

# Standard water properties (viscosity Pa s; surface tension against air N/m)
WATER_T = [0.0, 10.0, 20.0, 25.0, 30.0, 40.0]
WATER_ETA = [1.787e-3, 1.307e-3, 1.002e-3, 0.890e-3, 0.797e-3, 0.653e-3]
WATER_GAMMA = [0.0756, 0.0742, 0.0728, 0.0720, 0.0712, 0.0696]


def water_props(t_c):
    return float(np.interp(t_c, WATER_T, WATER_ETA)), float(np.interp(t_c, WATER_T, WATER_GAMMA))


def r_star_um(eta, gamma, cos_t, t_s):
    """Largest path radius (micrometres) that wicks the full wrap height within t_s seconds (Washburn)."""
    if t_s is None or t_s <= 0:
        return None
    return 2.0 * eta * H_WRAP ** 2 / (gamma * cos_t * t_s) * 1e6


def first_time_above(trace, level):
    for t, temp in zip(trace["t_s"], trace["T_surface_C"]):
        if temp > level:
            return t
    return None


def external_case(key, out, t_max):
    """(mode, wet seconds, water eta, water gamma, description) for the external wetting path."""
    if key in ("S1", "S2", "SU1", "SU5"):
        t_dry = first_time_above(out["trace"], T_DEW)
        t_ext = t_max if t_dry is None else t_dry
        eta, gamma = water_props(10.0)            # condensate film, central 10 C (envelope 0 to 25 C below)
        return "condensate", t_ext, eta, gamma, "film from humid air until the surface passes the dew point"
    if key == "SU2":
        eta, gamma = water_props(s.NOMINAL_X["T_water"])
        return "splash", t_max, eta, gamma, "splash water at T_water for the whole stall period"
    if key == "SU3":
        eta, gamma = water_props(0.5 * s.NOMINAL_X["bath_T1"])
        return "ice_water", t_max, eta, gamma, "wrap immersed in ice-water, bath 0 to bath_T1 C (mean used)"
    return "none", 0.0, None, None, "closed insulated box: pop not exposed to outside water"


def top_wetted_likely(mode):
    """True when the external water is expected to reach the top of the wrap (no climb margin)."""
    return mode in ("condensate", "splash", "ice_water")


def main():
    t0 = time.time()
    # Baseline: lab reference (30 C still air), used for the internal threshold comparison
    base = s.thermal_env(P_NOM, s.build_env("S0", s.NOMINAL_X), 3 * 3600.0, N=8)
    base_remaining = WINDOW_S - base["t_wet"]
    r_int_base = r_star_um(ETA_DRINK, GAMMA_DRINK, COS_MEAS, base_remaining)
    print("Baseline lab: t_wet %.2f h, internal threshold %.3f um" % (base["t_wet"] / 3600, r_int_base))

    rows, traces = [], {}
    for key, label, t_max_h in s.SCENARIOS:
        if key not in CASES:
            continue
        t_max = t_max_h * 3600.0
        out = s.thermal_env(P_NOM, s.build_env(key, s.NOMINAL_X), t_max, N=8, record_dt=300.0)
        traces[key] = out["trace"]
        mode, t_ext, eta_w, gamma_w, desc = external_case(key, out, t_max)
        t_wet = out["t_wet"]
        remaining = (WINDOW_S - t_wet) if t_wet is not None else None
        row = {
            "key": key, "label": label, "t_max_h": t_max_h,
            "t_wet_h": None if t_wet is None else t_wet / 3600.0,
            "t50_h": None if out["t50"] is None else out["t50"] / 3600.0,
            "t_core5_h": None if out["t_core5"] is None else out["t_core5"] / 3600.0,
            "max_T_surface_C": out["max_T_surface_C"],
            "internal_threshold_um": r_star_um(ETA_DRINK, GAMMA_DRINK, COS_MEAS, remaining),
            "external_mode": mode, "external_description": desc,
            "external_wet_h": t_ext / 3600.0,
            "top_wetted_likely": top_wetted_likely(mode),
        }
        if mode != "none" and t_ext > 0:
            row["external_threshold_um"] = r_star_um(eta_w, gamma_w, COS_MEAS, t_ext)
            row["external_threshold_wettable_um"] = r_star_um(eta_w, gamma_w, COS_WETTABLE, t_ext)
            row["water_eta_mPa_s"] = eta_w * 1e3
            row["water_gamma_N_m"] = gamma_w
        else:
            row["external_threshold_um"] = None
            row["external_threshold_wettable_um"] = None
        rows.append(row)
        print("%-4s %-46s wet %s  t50 %s  core5 %s  int r* %s um  ext %s  ext r* %s um" % (
            key, label,
            "n/a" if row["t_wet_h"] is None else "%.2f h" % row["t_wet_h"],
            "n/a" if row["t50_h"] is None else "%.2f h" % row["t50_h"],
            "n/a" if row["t_core5_h"] is None else "%.2f h" % row["t_core5_h"],
            "n/a" if row["internal_threshold_um"] is None else "%.3f" % row["internal_threshold_um"],
            mode,
            "n/a" if row["external_threshold_um"] is None else "%.3f" % row["external_threshold_um"]), flush=True)

    payload = {
        "inputs": {"H_wrap_m": H_WRAP, "window_s": WINDOW_S, "contact_angle_measured_deg": 76.08,
                   "contact_angle_wettable_deg": 60.0, "dew_point_C": T_DEW,
                   "drink_eta_Pa_s": ETA_DRINK, "drink_gamma_N_m": GAMMA_DRINK,
                   "water_table": {"T_C": WATER_T, "eta_Pa_s": WATER_ETA, "gamma_N_m": WATER_GAMMA},
                   "nominal_x": s.NOMINAL_X, "note": "Screen only. Damaged-path radius unmeasured."},
        "baseline_lab": {"t_wet_h": base["t_wet"] / 3600.0, "internal_threshold_um": r_int_base},
        "rows": rows,
        "traces": traces,
        "runtime_s": round(time.time() - t0, 1),
    }
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=float)
    print("wrote", os.path.abspath(OUT_JSON), "in %.0f s" % (time.time() - t0))
    make_chart(rows, traces, r_int_base)


def make_chart(rows, traces, r_int_base):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.4))
    ax = axes[0]
    for key in CASES:
        tr = traces.get(key)
        if tr is None:
            continue
        ax.plot(np.array(tr["t_s"]) / 3600.0, tr["T_surface_C"], lw=1.4, label=key)
    ax.axhline(0.0, color="grey", lw=0.8, ls=":")
    ax.axhline(T_DEW, color="#EF9F27", lw=0.9, ls="--", label="dew point 24.8 C")
    ax.set_xlabel("elapsed time from start (h)")
    ax.set_ylabel("surface temperature (C)")
    ax.set_title("Surface temperature, Thai summer occasions (nominal, screen)")
    ax.legend(fontsize=7, loc="upper left")

    ax = axes[1]
    y = np.arange(len(rows))
    for i, r in enumerate(rows):
        if r["external_threshold_um"] is not None:
            lo = r["external_threshold_wettable_um"]
            hi = r["external_threshold_um"]
            ax.plot([lo, hi], [i, i], color="#185FA5", lw=6, alpha=0.35, solid_capstyle="butt")
            marker = "x" if r["top_wetted_likely"] else "o"
            ax.plot(hi, i, marker, color="#185FA5", ms=8,
                    label="outside water, bottom-edge climb (x = top likely wet: no margin)" if i == 0 else None)
        if r["internal_threshold_um"] is not None:
            ax.plot(r["internal_threshold_um"], i, "s", color="#993C1D",
                    label="drink (internal) threshold" if i == 0 else None)
    ax.axvline(r_int_base, color="grey", ls=":", label="baseline lab, drink threshold")
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(["%s %s" % (r["key"], r["label"]) for r in rows], fontsize=7)
    ax.set_xlabel("smallest damaged-path radius that leaks in time (micrometres, log)")
    ax.set_title("Smallest leaking path (um): higher = more margin")
    ax.legend(fontsize=6.5, loc="upper center", bbox_to_anchor=(0.45, -0.16), ncol=1, frameon=False)
    fig.suptitle("Thai summer occasions: thaw and wicking screen (virtual, damaged-path size unmeasured)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT_PNG, dpi=130)
    print("wrote", os.path.abspath(OUT_PNG))


if __name__ == "__main__":
    main()
