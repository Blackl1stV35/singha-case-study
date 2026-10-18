"""Stage-gate physics screen for the leaf-wrapped frozen pop: thaw timing only.

What this screens: how long the frozen core takes to thaw at 30 C ambient, under a
lumped heat balance. It does NOT screen leakage. Leakage depends on leaf permeability,
seam quality and wicking, which are not measured; those stay physical tests.

All inputs are assumptions, labelled below. Replace with measured values when available.
Run:  python leak_thaw_screen.py
"""
import json
import math

# --- geometry (assumed; see rework/08_pop_label_dieline.svg notes) -------------
R = 0.019          # core radius, m
L = 0.150          # core length, m
A = 2 * math.pi * R * L + 2 * math.pi * R * R   # lateral + both ends, m^2
V = math.pi * R * R * L                         # core volume, m^3

# --- material (assumed for a sugared coconut-pandan drink, close to water) -----
RHO = 1000.0       # kg/m^3
C_ICE = 2.0        # kJ/(kg K), frozen specific heat
LF = 300.0         # kJ/kg, latent heat (assumed; sugar lowers the freezing point)
T_FREEZE = -1.0    # C, onset of thaw for a sugared drink (assumed)
T_START = -18.0    # C, freezer temperature (assumed)
T_AMBIENT = 30.0   # C, the test condition

DT = 10.0          # s, time step
T_MAX = 8 * 3600.0


def thaw_times(h, mass):
    """Explicit Euler on the lumped balance. Returns seconds to 50% and 100% thawed."""
    hA = h * A
    T, f, t = T_START, 0.0, 0.0
    t_half = t_full = None
    while f < 1.0 and t < T_MAX:
        if T < T_FREEZE:
            power = hA * (T_AMBIENT - T)                     # W, sensible heating
            T += power * DT / (mass * C_ICE * 1000.0)        # K
            if T > T_FREEZE:
                T = T_FREEZE
        else:
            power = hA * (T_AMBIENT - T_FREEZE)              # W, latent phase at T_freeze
            f += power * DT / (mass * LF * 1000.0)
            if f >= 0.5 and t_half is None:
                t_half = t
        t += DT
    if f >= 1.0:
        t_full = t
    return t_half, t_full


def hours(seconds):
    return None if seconds is None else round(seconds / 3600.0, 2)


if __name__ == "__main__":
    mass0 = RHO * V
    print(f"Core volume {V*1e6:.0f} mL, mass {mass0:.3f} kg, surface area {A*1e4:.1f} cm^2")

    results = {"geometry": {"radius_m": R, "length_m": L, "area_m2": A, "volume_m3": V},
               "assumptions": {"rho": RHO, "c_ice_kJ": C_ICE, "Lf_kJ": LF,
                               "T_freeze_C": T_FREEZE, "T_start_C": T_START,
                               "T_ambient_C": T_AMBIENT}}

    print("\nSweep 1: surface heat-transfer coefficient h (mass fixed)")
    print(f"{'h (W/m2K)':>10} {'50% thawed (h)':>16} {'100% thawed (h)':>17}")
    sweep_h = []
    for h in (5.0, 10.0, 15.0):
        t50, t100 = thaw_times(h, mass0)
        sweep_h.append({"h": h, "t50_h": hours(t50), "t100_h": hours(t100)})
        print(f"{h:>10.1f} {hours(t50):>16} {hours(t100):>17}")
    results["sweep_h"] = sweep_h

    print("\nSweep 2: core mass (h fixed at 10 W/m2K)")
    print(f"{'mass (kg)':>10} {'50% thawed (h)':>16} {'100% thawed (h)':>17}")
    sweep_m = []
    for mass in (0.14, mass0, 0.20):
        t50, t100 = thaw_times(10.0, mass)
        sweep_m.append({"mass_kg": round(mass, 3), "t50_h": hours(t50), "t100_h": hours(t100)})
        print(f"{mass:>10.3f} {hours(t50):>16} {hours(t100):>17}")
    results["sweep_mass"] = sweep_m

    with open("leak_thaw_screen_results.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print("\nWrote leak_thaw_screen_results.json")
