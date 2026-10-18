"""Thailand stress test for the frozen leaf-wrapped pop: street, sun, parked car, insulated box, truck, freezer outage.

Extends the radial enthalpy model in pop_leak_simulation.py with:
  - a time-varying external temperature (diurnal cycle, cabin warm-up, reefer door-open event),
  - absorbed solar flux on the wrap (absorptance x geometry factor x global irradiance),
  - an insulated box with a gel-pack buffer: a lumped box-air node held at the gel melting
    temperature while latent heat remains (no refreezing),
  - an end-cap correction (1 + R/H) on the surface heat-transfer area, switched off for validation.

Screen, not a measurement. Results are virtual and depend on the inputs in INPUTS_NOTE below.
Run:  python thailand_stress_test.py   (writes thailand_stress_test_results.json and rework/22_thailand_stress_test.png)
"""
import json
import math
import os
import time

import numpy as np

from pop_leak_simulation import R, T0, RHO, make_props, T_of_H, f_of_H, k_of_f, sample_params, thermal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "thailand_stress_test_results.json")
OUT_PNG = os.path.join(HERE, "..", "22_thailand_stress_test.png")
H_CORE = 0.15                 # m, core height; 170 mL at R = 19 mm
CAP = 1.0 + R / H_CORE        # lateral-equivalent area of the two end caps
FOOD_LINE_C = 5.0             # C, cold-holding line used as the thawed-drink check (verify against Thai guidance)
INPUTS_NOTE = "Inputs: see rework/22_thailand_inputs.md for sources; [asm] marks assumptions."
N_MC = 30


# --- environment builders -----------------------------------------------------------------
def diurnal(clock0_h, t_mean, amp, t_peak_h=15.0):
    """External air temperature (C) for elapsed time t (s) from a clock start (h of day)."""
    def f(t):
        hour = clock0_h + t / 3600.0
        return t_mean + amp * math.cos(2.0 * math.pi * (hour - t_peak_h) / 24.0)
    return f


def sun(clock0_h, g_peak):
    """Global irradiance on a horizontal plane (W/m2): clear-sky half sine from 06:00 to 18:00."""
    def g(t):
        hour = (clock0_h + t / 3600.0) % 24.0
        if hour < 6.0 or hour > 18.0:
            return 0.0
        return g_peak * math.sin(math.pi * (hour - 6.0) / 12.0)
    return g


def cabin(base, d_t, tau_s):
    """Parked-car cabin air: ambient plus a first-order rise towards d_t above ambient."""
    return lambda t: base(t) + d_t * (1.0 - math.exp(-t / tau_s))


def reefer(t_open_s, t_close_s, t_hot, t_cold):
    """Truck cargo air: cold, with a door-open excursion to t_hot."""
    return lambda t: t_hot if t_open_s <= t < t_close_s else t_cold


def build_env(key, x):
    """Environment dict for scenario key with environment parameters x (see NOMINAL_X)."""
    def box():
        return {"UA": x["UA_box"], "m_air": 0.03, "m_gel": x["m_gel_total"], "c_gel": 2000.0,
                "L_gel": x["L_gel"], "T_plat": x["T_plat"]}

    if key == "S0":   # lab reference, must reproduce thermal() in pop_leak_simulation.py
        return {"T_ext": lambda t: 30.0, "h_conv": 10.0, "h_rad": 0.0, "cap": False}
    if key == "S1":   # street stall in shade, hot-season day, from 09:00
        return {"T_ext": diurnal(9.0, x["t_mean"], x["amp"]), "h_conv": x["h_shade"], "h_rad": x["h_rad"]}
    if key == "S2":   # street stall in full sun, same day
        return {"T_ext": diurnal(9.0, x["t_mean"], x["amp"]), "G": sun(9.0, x["G_peak"]),
                "alpha": x["alpha"], "f_geom": x["f_geom"], "h_conv": x["h_shade"], "h_rad": x["h_rad"]}
    if key == "S3":   # parked car, closed, from 11:00 for 2 h, cabin air warms by d_t
        return {"T_ext": cabin(diurnal(11.0, x["cabin_mean"], 5.0), x["dT_cabin"], 1800.0),
                "h_conv": 8.0, "h_rad": x["h_rad"]}
    if key == "S4":   # insulated box with gel packs, motorbike delivery from 13:00
        return {"T_ext": diurnal(13.0, x["t_mean"], x["amp"]), "h_conv": x["h_box"], "h_rad": 0.0, "box": box()}
    if key == "S5":   # extreme 40 C day, full sun, bare pop, from 09:00
        return {"T_ext": diurnal(9.0, 34.0, 6.0), "G": sun(9.0, 950.0), "alpha": x["alpha"],
                "f_geom": x["f_geom"], "h_conv": x["h_wind"], "h_rad": x["h_rad"]}
    if key == "S6":   # reefer at -18 C, 30 min door open at 30 C, from 1 h to 1.5 h
        return {"T_ext": reefer(3600.0, 5400.0, 30.0, -18.0), "h_conv": 15.0, "h_rad": 0.0}
    if key == "S7":   # home freezer outage, 28 C kitchen, still indoor air
        return {"T_ext": lambda t: 28.0, "h_conv": 10.0, "h_rad": 0.0}
    # Thai summer occasions (sources in rework/22_thailand_inputs.md)
    if key == "SU1":  # festival stall in sun, hot-season afternoon, from 11:00 for 3 h, low urban wind
        return {"T_ext": diurnal(11.0, x["fest_mean"], x["fest_amp"]), "G": sun(11.0, x["G_fest"]),
                "alpha": x["alpha"], "f_geom": x["f_geom"], "h_conv": x["h_calm"], "h_rad": x["h_rad"]}
    if key == "SU2":  # Songkran street stall: surface splashed with water a fraction of the time (time-averaged)
        f = x["splash_frac"]
        h_air = x["h_calm"] + x["h_rad"]
        h_eff = f * x["h_water"] + (1.0 - f) * h_air
        T_eff = (f * x["h_water"] * x["T_water"] + (1.0 - f) * h_air * x["fest_peak"]) / h_eff
        return {"T_ext": lambda t: T_eff, "h_conv": h_eff, "h_rad": 0.0}
    if key == "SU3":  # ice-water cooler at a picnic: bath starts at 0 C and warms to bath_T1 over 4 h
        return {"T_ext": lambda t: x["bath_T1"] * min(t / (4 * 3600.0), 1.0), "h_conv": x["h_water"], "h_rad": 0.0}
    if key == "SU4":  # insulated cooler with gel packs at a festival, diurnal ambient, 4 h
        return {"T_ext": diurnal(11.0, x["fest_mean"], x["fest_amp"]), "h_conv": x["h_box"], "h_rad": 0.0, "box": box()}
    if key == "SU5":  # parked car at a festival lot, 3 h, cabin rises by cabin_dT_fest above ambient
        return {"T_ext": cabin(diurnal(12.0, x["fest_mean"], x["fest_amp"]), x["cabin_dT_fest"], 1800.0),
                "h_conv": 8.0, "h_rad": x["h_rad"]}
    raise KeyError(key)


SCENARIOS = [
    ("S0", "Lab reference, 30 C still air", 3.0),
    ("S1", "Street stall, shade, hot-season day", 6.0),
    ("S2", "Street stall, full sun, hot-season day", 6.0),
    ("S3", "Parked car, closed, 2 h", 2.0),
    ("S4", "Insulated box + gel packs, motorbike, 3 h", 3.0),
    ("S5", "Extreme 40 C day, full sun, bare pop", 6.0),
    ("S6", "Reefer at -18 C, 30 min door open", 4.0),
    ("S7", "Home freezer outage, 28 C kitchen", 6.0),
    ("SU1", "Festival stall in sun, hot afternoon, 3 h", 3.0),
    ("SU2", "Songkran street stall, splash-wetted, 2 h", 2.0),
    ("SU3", "Ice-water cooler at a picnic, 4 h", 4.0),
    ("SU4", "Insulated cooler with gel packs at a festival, 4 h", 4.0),
    ("SU5", "Parked car at a festival lot, 3 h", 3.0),
]
MC_SCENARIOS = ["S1", "S2", "S3", "S4", "S5"]

# Sourced values (rework/22_thailand_inputs.md). Bangkok Mar-May, TMD 48455, 1991-2020 normals:
#   daily mean max 35.7 C, daily mean min 27.2 C (April) -> diurnal mean 31.5 C, amplitude 4.3 K
#   clear-sky daily irradiation 5.6-6.1 kWh/m2/day (NASA POWER) -> half-sine peak about 800 W/m2
#   urban wind 1.1-1.4 m/s -> h_shade about 10.7 W/m2K (McAdams 5.7 + 3.8 u); open 3.1 m/s -> h_wind 17.5
#   gel pack melting point about -1.3 C; latent heat 200-330 J/g; EPS 0.027-0.040 W/mK, 3 cm walls
NOMINAL_X = dict(t_mean=31.5, amp=4.3, G_peak=800.0, alpha=0.75, f_geom=0.40, h_shade=10.7, h_wind=17.5,
                 h_rad=5.0, dT_cabin=20.0, cabin_mean=31.5, UA_box=1.0, m_gel_total=0.6, L_gel=270e3,
                 T_plat=-1.3, h_box=8.0,
                 # Thai summer occasions: afternoon peak 35.7 C; diurnal mean/amplitude as above
                 fest_mean=31.5, fest_amp=4.3, fest_peak=35.7, G_fest=800.0, h_calm=10.7, splash_frac=0.2,
                 h_water=300.0, T_water=26.0, bath_T1=3.0, cabin_dT_fest=23.0)


def sample_x(rng):
    return dict(t_mean=rng.uniform(30.8, 32.2), amp=rng.uniform(3.8, 4.8), G_peak=rng.uniform(740.0, 860.0),
                alpha=rng.uniform(0.6, 0.85), f_geom=rng.uniform(0.32, 0.5), h_shade=rng.uniform(8.0, 14.0),
                h_wind=rng.uniform(15.0, 20.0), h_rad=rng.uniform(4.0, 6.0), dT_cabin=rng.uniform(15.0, 25.0),
                cabin_mean=rng.uniform(30.5, 32.5), UA_box=rng.uniform(0.8, 1.2),
                m_gel_total=rng.uniform(0.4, 1.0), L_gel=rng.uniform(200e3, 330e3),
                T_plat=rng.uniform(-2.0, 0.0), h_box=rng.uniform(6.0, 10.0))


# --- thermal core with a time-varying environment ----------------------------------------
def _box_step(T_box, E_in, C_box, E_latent, T_plat):
    """Advance the box-air node by energy E_in (J). Gel holds the box at T_plat while latent heat remains."""
    if E_latent > 0.0 and T_box >= T_plat and E_in > 0.0:
        absorbed = min(E_in, E_latent)
        E_latent -= absorbed
        E_in -= absorbed
        return T_plat + E_in / C_box, E_latent
    T_box = T_box + E_in / C_box
    if E_latent > 0.0 and T_box > T_plat:
        excess = (T_box - T_plat) * C_box
        absorbed = min(excess, E_latent)
        E_latent -= absorbed
        return T_plat + (excess - absorbed) / C_box, E_latent
    return T_box, E_latent


def thermal_env(p, env, t_max, N=8, record_dt=None):
    """Finite-volume radial conduction, enthalpy method, time-varying environment.

    Returns event times (s) for surface wetting, 50% and 100% thaw, and core above FOOD_LINE_C,
    maxima, and an optional trace every record_dt seconds.
    """
    q = make_props(p)
    dr = R / N
    V = np.zeros(N + 1)
    V[0] = math.pi * (dr / 2.0) ** 2
    for i in range(1, N):
        V[i] = math.pi * dr * dr * 2 * i
    V[N] = math.pi * dr * dr * (N - 0.25)
    A_face = 2.0 * math.pi * (np.arange(N) + 0.5) * dr
    cap = CAP if env.get("cap", True) else 1.0
    h_tot = env["h_conv"] + env.get("h_rad", 0.0)
    A_pl = 2.0 * math.pi * R * cap                       # surface area per unit length, m2/m
    k_max = max(q["k_s"], q["k_l"])
    G_sum = np.zeros(N + 1)
    G_sum[:-1] += k_max * A_face / dr
    G_sum[1:] += k_max * A_face / dr
    G_sum[N] += h_tot * A_pl
    dt = min(0.5 * RHO * V * q["cp_s"] / G_sum)

    box = env.get("box")
    T_box = T0
    C_box = E_latent = 0.0
    if box:
        C_box = box["m_air"] * 1005.0 + box["m_gel"] * box["c_gel"]
        E_latent = box["m_gel"] * box["L_gel"]

    H = np.zeros(N + 1)                                  # frozen at T0
    t = 0.0
    next_rec = 0.0
    ev = {"t_wet": None, "t50": None, "t100": None, "t_core5": None, "gel_out": None}
    if box and E_latent <= 0.0:
        ev["gel_out"] = 0.0
    mx = {"T_surface": -1e9, "T_core": -1e9, "T_box_min": 1e9, "T_box_max": -1e9}
    trace = {"t_s": [], "T_surface_C": [], "T_core_C": [], "f_avg": [], "T_box_C": []}
    while t < t_max:
        T = T_of_H(H, q)
        f = f_of_H(H, q)
        k = k_of_f(f, q)
        kf = 0.5 * (k[:-1] + k[1:])
        G = kf * A_face / dr
        flux = G * (T[1:] - T[:-1])
        Q = np.zeros(N + 1)
        Q[:-1] += flux
        Q[1:] -= flux
        T_ext = env["T_ext"](t)
        if box is None:
            q_in = h_tot * A_pl * (T_ext - T[N])
            if env.get("G") is not None:
                q_in += env["alpha"] * env["f_geom"] * env["G"](t) * A_pl
        else:
            q_in = h_tot * A_pl * (T_box - T[N])
        Q[N] += q_in
        H = H + dt * Q / (RHO * V)
        if box is not None:
            E_in = dt * (box["UA"] * (T_ext - T_box) - q_in * H_CORE)
            T_box, E_latent = _box_step(T_box, E_in, C_box, E_latent, box["T_plat"])
            if ev["gel_out"] is None and E_latent <= 0.0:
                ev["gel_out"] = t
            mx["T_box_min"] = min(mx["T_box_min"], T_box)
            mx["T_box_max"] = max(mx["T_box_max"], T_box)
        t += dt
        T = T_of_H(H, q)                                  # event checks use the state after this step
        f = f_of_H(H, q)
        f_avg = float((f * V).sum() / V.sum())
        if ev["t_wet"] is None and f[N] > 0.0:
            ev["t_wet"] = t
        if ev["t50"] is None and f_avg >= 0.5:
            ev["t50"] = t
        if ev["t100"] is None and f_avg >= 0.999:
            ev["t100"] = t
        if ev["t_core5"] is None and T[0] > FOOD_LINE_C:
            ev["t_core5"] = t
        mx["T_surface"] = max(mx["T_surface"], float(T[N]))
        mx["T_core"] = max(mx["T_core"], float(T[0]))
        if record_dt and t >= next_rec:
            trace["t_s"].append(t)
            trace["T_surface_C"].append(float(T[N]))
            trace["T_core_C"].append(float(T[0]))
            trace["f_avg"].append(f_avg)
            trace["T_box_C"].append(float(T_box) if box else None)
            next_rec += record_dt
    out = dict(ev, dt_s=float(dt), N=N, max_T_surface_C=mx["T_surface"], max_T_core_C=mx["T_core"],
               trace=trace)
    if box:
        out["box_T_min_C"] = mx["T_box_min"]
        out["box_T_max_C"] = mx["T_box_max"]
    return out


# --- validation and grid check -------------------------------------------------------------
def validate():
    nom = dict(h=10.0, k_s=2.2, cp_s=2000.0, L=300e3, Tf=-1.0, eta=1e-3, theta=76.08, gamma=0.072, r_vessel=5.5e-6)
    ref = thermal(nom, N=8, t_max=3 * 3600.0)
    new = thermal_env(nom, build_env("S0", NOMINAL_X), 3 * 3600.0, N=8)
    diffs = {}
    for k in ("t_wet", "t50", "t100"):
        a, b = ref[k + "_s"], new[k]
        diffs[k] = None if (a is None or b is None) else float(b - a)
    # Both runs null (not thawed within the window) counts as agreement; otherwise allow one solver step.
    diffs_ok = all((a is None and b is None) or (d is not None and abs(d) <= ref["dt_s"] + 1e-6)
                   for d, a, b in ((diffs[k], ref[k + "_s"], new[k]) for k in diffs))
    return {"reference_thermal_h": {k: (None if ref[k] is None else ref[k] / 3600.0) for k in
                                    ("t_wet_s", "t50_s", "t100_s")},
            "thermal_env_h": {k: (None if new[k] is None else new[k] / 3600.0) for k in
                              ("t_wet", "t50", "t100")},
            "difference_s": diffs, "dt_s": ref["dt_s"], "agrees_within_2_steps": bool(diffs_ok)}


def grid_check(p):
    """Same scenario on N=8 and N=16 to confirm the stress-test outputs are grid-converged."""
    env = build_env("S2", NOMINAL_X)
    a = thermal_env(p, env, 6 * 3600.0, N=8)
    b = thermal_env(p, env, 6 * 3600.0, N=16)
    rel = {}
    for k in ("t_wet", "t50", "t_core5"):
        if a[k] and b[k]:
            rel[k] = round(100.0 * (a[k] - b[k]) / b[k], 2)
    return {"scenario": "S2", "N8_vs_N16_percent_difference": rel}


# --- main --------------------------------------------------------------------------------
def hours(x):
    return None if x is None else x / 3600.0


def summarise(key, out):
    keep = {k: hours(out[k]) for k in ("t_wet", "t50", "t100", "t_core5", "gel_out")}
    keep.update({k: out[k] for k in ("max_T_surface_C", "max_T_core_C")})
    if "box_T_min_C" in out:
        keep.update({"box_T_min_C": out["box_T_min_C"], "box_T_max_C": out["box_T_max_C"]})
    keep["dt_s"] = out["dt_s"]
    return keep


def make_chart(scen, mc):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))
    ax = axes[0]
    plotted = [key for key, _, _ in SCENARIOS if key != "S0"]
    cmap = plt.get_cmap("tab20")
    for i, key in enumerate(plotted):
        tr = scen[key]["trace"]
        label = [lab for k, lab, _ in SCENARIOS if k == key][0]
        ax.plot(np.array(tr["t_s"]) / 3600.0, tr["T_surface_C"], lw=1.4, color=cmap(i % 20),
                label="%s %s" % (key, label))
    tr4 = scen["S4"]["trace"]
    ax.plot(np.array(tr4["t_s"]) / 3600.0, tr4["T_box_C"], "k--", lw=1, label="S4 box air")
    ax.axhline(0.0, color="grey", lw=0.8, ls=":")
    ax.axhline(FOOD_LINE_C, color="grey", lw=0.8, ls="-.")
    ax.set_xlabel("elapsed time from start (h)")
    ax.set_ylabel("surface temperature (C)")
    ax.set_title("Surface temperature under Thai exposure scenarios (nominal)")
    ax.legend(fontsize=7, loc="upper left")

    ax = axes[1]
    labels = [key + " " + label for key, label, _ in SCENARIOS if key != "S0"]
    keys = [key for key, _, _ in SCENARIOS if key != "S0"]
    y = np.arange(len(keys))
    for offset, metric, color, name in ((0.15, "t_wet", "#185FA5", "surface starts to melt"),
                                        (-0.15, "t_core5", "#EF9F27", "core above 5 C")):
        for i, key in enumerate(keys):
            v = scen[key].get(metric)                    # already in hours (see summarise)
            if v is not None:
                ax.plot(v, i + offset, "o", color=color, label=name if i == 0 else None)
            else:
                ax.text(0.05, i + offset, "not reached", fontsize=7, color=color, va="center")
            if key in mc and mc[key].get(metric) is not None:
                lo, hi = mc[key][metric]["p5"], mc[key][metric]["p95"]
                if lo is not None and hi is not None:
                    ax.plot([lo, hi], [i + offset, i + offset], color=color, lw=2, alpha=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("time (h); thick bars = 5 to 95 percent of Monte Carlo draws")
    ax.set_title("When the pop starts to melt and when the core passes 5 C")
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.45, -0.14), ncol=2, frameon=False)
    fig.suptitle("Thailand stress test, frozen leaf-wrapped pop (virtual screen, not measured)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT_PNG, dpi=130)
    print("wrote", os.path.abspath(OUT_PNG))


def main():
    t0 = time.time()
    p_nom = dict(h=10.0, k_s=2.2, cp_s=2000.0, L=300e3, Tf=-1.0)
    val = validate()
    print("validation:", json.dumps(val, indent=1))
    grid = grid_check(p_nom)
    print("grid check:", grid)

    scen = {}
    for key, label, t_max_h in SCENARIOS:
        out = thermal_env(p_nom, build_env(key, NOMINAL_X), t_max_h * 3600.0, N=8, record_dt=300.0)
        scen[key] = dict(summarise(key, out), label=label, t_max_h=t_max_h, trace=out["trace"])
        print("%s %-44s wet %s  t50 %s  core5 %s  Tmax surf %.1f" % (
            key, label, "n/a" if scen[key]["t_wet"] is None else "%.2f h" % scen[key]["t_wet"],
            "n/a" if scen[key]["t50"] is None else "%.2f h" % scen[key]["t50"],
            "n/a" if scen[key]["t_core5"] is None else "%.2f h" % scen[key]["t_core5"],
            scen[key]["max_T_surface_C"]), flush=True)

    rng = np.random.default_rng(20261018)
    mc = {}
    for key in MC_SCENARIOS:
        t_max = [t for k, _, t in SCENARIOS if k == key][0] * 3600.0
        rows = {"t_wet": [], "t50": [], "t_core5": []}
        for _ in range(N_MC):
            x = sample_x(rng)
            p = sample_params(rng, 1)[0]
            out = thermal_env(p, build_env(key, x), t_max, N=8)
            for m in rows:
                rows[m].append(math.inf if out[m] is None else out[m] / 3600.0)
        mc[key] = {}
        for m, vals in rows.items():
            arr = np.array(vals)
            fin = arr[np.isfinite(arr)]
            mc[key][m] = None if fin.size == 0 else {
                "p5": float(np.percentile(fin, 5)), "median": float(np.percentile(fin, 50)),
                "p95": float(np.percentile(fin, 95)), "not_reached_fraction": float(1.0 - fin.size / arr.size)}
        print("MC %s done: wet %s" % (key, mc[key]["t_wet"]), flush=True)

    payload = {
        "inputs": {"core_radius_m": R, "core_height_m": H_CORE, "end_cap_factor": CAP,
                   "food_line_C": FOOD_LINE_C, "start_C": T0, "nominal_x": NOMINAL_X, "N_MC": N_MC,
                   "note": INPUTS_NOTE},
        "validation": val, "grid_check": grid,
        "scenarios": {k: {kk: vv for kk, vv in v.items() if kk != "trace"} for k, v in scen.items()},
        "monte_carlo": mc,
        "traces": {k: v["trace"] for k, v in scen.items()},
        "runtime_s": round(time.time() - t0, 1),
    }
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=float)
    print("wrote", os.path.abspath(OUT_JSON), "in %.0f s" % (time.time() - t0))
    make_chart(scen, mc)


if __name__ == "__main__":
    main()
