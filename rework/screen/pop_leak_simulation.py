"""Coupled virtual simulation for the leaf-wrapped frozen pop: thaw, wetting and wicking.

Model chain (stage-gate screen, not a measurement):
  1. Transient radial heat conduction in the frozen core (finite volume, enthalpy method,
     convective surface to 30 C ambient), giving the surface wetting time t_wet and the
     thaw fractions.
  2. Capillary wicking (Washburn) into a path of radius r, starting when the edge is wet:
     leak if  t_wet + t_climb(r) <= window,  t_climb = 2*eta*H^2 / (gamma*r*cos(theta)).
  3. Monte Carlo over the uncertain inputs for three designs:
       A  leaf-only, cut edges in melt contact (exposed vessels, analogue radius)
       B  leaf-only, edges sealed; freeze-damaged surface paths of unknown radius r_d (scanned)
       C  continuous inner film (no pores; defects not modelled)

All inputs are assumptions or literature analogues; see rework/16_permeability_seam_estimate.md.
Run:  python pop_leak_simulation.py   (writes JSON and a plot next to this script)
"""
import json
import math
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# --- geometry and fixed properties --------------------------------------------
R = 0.019                 # core radius, m (assumed)
T_AMB = 30.0              # C, test ambient
T0 = -18.0                # C, freezer start
DT_MUSH = 1.0             # K, width of the freezing (mushy) zone
RHO = 1000.0              # kg/m^3 (near water)
CP_L = 3900.0             # J/(kg K), liquid
K_L = 0.6                 # W/(m K), liquid
GAMMA_NOM = 0.072         # N/m
WINDOW_S = 2 * 3600.0     # s, thaw window
WRAP_H = 0.100            # m, wrap height (assumed)


def make_props(p):
    """Derive mushy-zone enthalpy breakpoints for one parameter draw."""
    Ts = p["Tf"] - DT_MUSH / 2.0
    Tl = p["Tf"] + DT_MUSH / 2.0
    Hs_Ts = p["cp_s"] * (Ts - T0)          # enthalpy at solid edge of mushy zone
    return dict(Ts=Ts, Tl=Tl, Hs_Ts=Hs_Ts, L=p["L"], cp_s=p["cp_s"], cp_l=CP_L,
                k_s=p["k_s"], k_l=K_L, Tf=p["Tf"])


def T_of_H(H, q):
    """Temperature from enthalpy (vectorised)."""
    Hs_Ts, L, Ts, Tl = q["Hs_Ts"], q["L"], q["Ts"], q["Tl"]
    T = np.where(H <= Hs_Ts, T0 + H / q["cp_s"],
        np.where(H <= Hs_Ts + L, Ts + (H - Hs_Ts) * (Tl - Ts) / L,
                 Tl + (H - Hs_Ts - L) / q["cp_l"]))
    return T


def f_of_H(H, q):
    """Liquid fraction from enthalpy (vectorised)."""
    return np.clip((H - q["Hs_Ts"]) / q["L"], 0.0, 1.0)


def k_of_f(f, q):
    return q["k_s"] * (1.0 - f) + q["k_l"] * f


def thermal(p, N=8, t_max=3 * 3600.0, record_every=None):
    """Finite-volume radial conduction. Returns dict with t_wet, t50, t100 and optional traces."""
    q = make_props(p)
    dr = R / N
    r = np.arange(N + 1) * dr
    V = np.zeros(N + 1)
    V[0] = math.pi * (dr / 2.0) ** 2
    for i in range(1, N):
        V[i] = math.pi * dr * dr * 2 * i
    V[N] = math.pi * dr * dr * (N - 0.25)
    A_face = 2.0 * math.pi * (np.arange(N) + 0.5) * dr        # per unit length
    k_max = max(q["k_s"], q["k_l"])
    G_sum = np.zeros(N + 1)
    G_sum[:-1] += k_max * A_face / dr
    G_sum[1:] += k_max * A_face / dr
    G_sum[N] += p["h"] * 2.0 * math.pi * R
    dt = min(0.5 * RHO * V * q["cp_s"] / G_sum)

    H = np.zeros(N + 1)                       # start at T0 (frozen, H = 0)
    t = 0.0
    t_wet = None
    t50 = None
    t100 = None
    trace_t, trace_Ts, trace_f = [], [], []
    step = 0
    while t < t_max:
        T = T_of_H(H, q)
        f = f_of_H(H, q)
        k = k_of_f(f, q)
        kf = 0.5 * (k[:-1] + k[1:])
        G = kf * A_face / dr
        flux = G * (T[1:] - T[:-1])           # W/m per face, flow from node i+1 to i when positive
        Q = np.zeros(N + 1)
        Q[:-1] += flux
        Q[1:] -= flux
        Q[N] += p["h"] * 2.0 * math.pi * R * (T_AMB - T[N])
        H = H + dt * Q / (RHO * V)
        t += dt
        step += 1
        f = f_of_H(H, q)
        f_avg = float((f * V).sum() / V.sum())
        if t_wet is None and f[N] > 0.0:
            t_wet = t
        if t50 is None and f_avg >= 0.5:
            t50 = t
        if t100 is None and f_avg >= 0.999:
            t100 = t
            break
        if record_every and step % record_every == 0:
            trace_t.append(t)
            trace_Ts.append(float(T[N]))
            trace_f.append(f_avg)
    out = {"t_wet_s": t_wet, "t50_s": t50, "t100_s": t100, "dt_s": float(dt), "N": N}
    if record_every:
        out["trace"] = {"t_s": trace_t, "T_surface_C": trace_Ts, "f_avg": trace_f}
    return out


def t_climb(H_m, r, theta_deg, eta, gamma):
    c = math.cos(math.radians(theta_deg))
    if c <= 0 or r <= 0:
        return math.inf
    return 2.0 * eta * H_m * H_m / (gamma * r * c)


def sample_params(rng, n):
    draws = []
    for _ in range(n):
        draws.append(dict(
            h=float(rng.triangular(5.0, 10.0, 15.0)),
            k_s=float(rng.uniform(2.0, 2.4)),
            cp_s=float(rng.uniform(1900.0, 2100.0)),
            L=float(rng.uniform(280e3, 320e3)),
            Tf=float(rng.uniform(-1.5, -0.5)),
            eta=float(rng.uniform(1.0e-3, 3.0e-3)),
            theta=float(rng.uniform(60.0, 76.0)),
            gamma=float(rng.uniform(0.065, 0.072)),
            r_vessel=float(math.exp(rng.uniform(math.log(2.75e-6), math.log(12.5e-6)))),
        ))
    return draws


def main():
    t0 = time.time()
    results = {"assumptions": {"core_radius_m": R, "ambient_C": T_AMB, "start_C": T0,
                               "window_s": WINDOW_S, "wrap_height_m": WRAP_H}}

    # 1. Nominal thermal run, grid convergence, and comparison with the lumped screen
    nom = dict(h=10.0, k_s=2.2, cp_s=2000.0, L=300e3, Tf=-1.0, eta=1.0e-3, theta=76.08,
               gamma=GAMMA_NOM, r_vessel=5.5e-6)
    n8 = thermal(nom, N=8, record_every=600, t_max=6 * 3600.0)
    n16 = thermal(nom, N=16, t_max=6 * 3600.0)
    results["nominal_h10"] = {
        "N8": {k: n8[k] for k in ("t_wet_s", "t50_s", "t100_s", "dt_s")},
        "N16": {k: n16[k] for k in ("t_wet_s", "t50_s", "t100_s", "dt_s")},
        "lumped_screen_t100_h": 2.47,
        "grid_convergence_t100_diff_pct": None,
    }
    if n8["t100_s"] and n16["t100_s"]:
        results["nominal_h10"]["grid_convergence_t100_diff_pct"] = round(
            100.0 * (n8["t100_s"] - n16["t100_s"]) / n16["t100_s"], 2)
    def hrs(x):
        return "n/a" if x is None else "%.2f h" % (x / 3600.0)

    print("Nominal h=10: t_wet %s, t50 %s, t100 %s (N=8); t100 %s (N=16)" % (
        hrs(n8["t_wet_s"]), hrs(n8["t50_s"]), hrs(n8["t100_s"]), hrs(n16["t100_s"])))
    print("Lumped screen gave t100 2.47 h at h=10 (rework/15)")

    # 2. Monte Carlo over the uncertain inputs
    rng = np.random.default_rng(20261018)
    N_MC = 200
    draws = sample_params(rng, N_MC)
    t_wet, t50, t100, r_dstar, leakA, leakA_series = [], [], [], [], [], []
    for p in draws:
        th = thermal(p, N=8, t_max=WINDOW_S)
        tw = th["t_wet_s"] if th["t_wet_s"] is not None else math.inf
        t_wet.append(tw)
        t50.append(th["t50_s"] if th["t50_s"] is not None else math.inf)
        t100.append(th["t100_s"] if th["t100_s"] is not None else math.inf)
        # Design A: exposed vessel path wicking from the wetted edge
        tc = t_climb(WRAP_H, p["r_vessel"], p["theta"], p["eta"], p["gamma"])
        leakA.append(bool(tw + tc <= WINDOW_S))
        # Design B: critical damaged-path radius (wider leaks)
        remaining = WINDOW_S - tw
        if remaining <= 0 or math.isinf(tw):
            r_dstar.append(math.inf)
        else:
            c = math.cos(math.radians(p["theta"]))
            r_dstar.append(2.0 * p["eta"] * WRAP_H * WRAP_H / (p["gamma"] * c * remaining))

    tw_arr = np.array(t_wet)
    finite = np.isfinite(tw_arr)
    dstar = np.array(r_dstar)
    scan_r = [1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6, 1e-5]

    def pct(x, q):
        x = np.asarray(x)
        x = x[np.isfinite(x)]
        return None if x.size == 0 else float(np.percentile(x, q))

    results["monte_carlo"] = {
        "n": N_MC,
        "fraction_never_wets_within_3h": float(1.0 - finite.mean()),
        "t_wet_h": {"p5": pct(tw_arr / 3600, 5), "median": pct(tw_arr / 3600, 50), "p95": pct(tw_arr / 3600, 95)},
        "t50_h": {"median": pct(np.array(t50) / 3600, 50)},
        "t100_h": {"p5": pct(np.array(t100) / 3600, 5), "median": pct(np.array(t100) / 3600, 50),
                   "p95": pct(np.array(t100) / 3600, 95)},
        "design_A_exposed_vessel_leak_probability": float(np.mean(leakA)),
        "design_B_critical_damaged_radius_m": {"p5": pct(dstar, 5), "median": pct(dstar, 50), "p95": pct(dstar, 95)},
        "design_B_leak_probability_vs_damaged_radius": [
            {"r_d_m": r, "P_leak": float(np.mean(dstar <= r))} for r in scan_r],
        "design_C_film_leak_probability": 0.0,
    }
    print("MC n=%d: P(leak) design A = %.2f" % (N_MC, np.mean(leakA)))
    print("Design B critical damaged radius (median, 5-95%%): %s" % (
        results["monte_carlo"]["design_B_critical_damaged_radius_m"]))

    out_json = os.path.join(HERE, "pop_leak_simulation_results.json")
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print("Wrote", out_json, "in %.0f s" % (time.time() - t0))

    # 3. Plots: thaw trace (nominal) and design B leak curve
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(10, 4))
        tr = n8["trace"]
        ax[0].plot(np.array(tr["t_s"]) / 3600, tr["f_avg"], label="thawed fraction (volume average)")
        ax[0].plot(np.array(tr["t_s"]) / 3600, np.array(tr["T_surface_C"]) / 40 + 0.5, "--",
                   label="surface T scaled (-18 to 30 C)")
        ax[0].axvline(WINDOW_S / 3600, color="grey", ls=":", label="2 h window")
        ax[0].set_xlabel("time (h)")
        ax[0].set_title("Nominal thaw at 30 C, h = 10 W/m2K")
        ax[0].legend(fontsize=7)
        rs = [row["r_d_m"] for row in results["monte_carlo"]["design_B_leak_probability_vs_damaged_radius"]]
        ps = [row["P_leak"] for row in results["monte_carlo"]["design_B_leak_probability_vs_damaged_radius"]]
        ax[1].semilogx(np.array(rs) * 1e6, ps, "o-")
        ax[1].axvline(0.16, color="grey", ls=":", label="nominal threshold (0.16 um)")
        ax[1].set_xlabel("damaged-path radius (um)")
        ax[1].set_ylabel("P(leak), sealed edges")
        ax[1].set_title("Design B: leak probability vs damaged-path size")
        ax[1].legend(fontsize=7)
        fig.tight_layout()
        out_png = os.path.join(HERE, "pop_leak_simulation.png")
        fig.savefig(out_png, dpi=130)
        print("Wrote", out_png)
    except Exception as exc:  # noqa: BLE001
        print("Plot skipped:", exc)


if __name__ == "__main__":
    main()
