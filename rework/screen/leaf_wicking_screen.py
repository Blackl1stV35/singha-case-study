"""Virtual leak screen for a leaf wrap: capillary (Washburn) wicking of melt water.

Question: can liquid travel from the melt pool to the outside of the wrap within the
2-hour thaw window through a path of radius r?  Washburn:  h(t)^2 = gamma*r*cos(theta)*t / (2*eta)

Inputs are literature-derived (see rework/16_permeability_seam_estimate.md) and labelled.
Wrap height and thaw window are design assumptions. Output is a screen, not a measurement.
Run:  python leaf_wicking_screen.py
"""
import json
import math

GAMMA = 0.072          # N/m, surface tension of water (sugared drink slightly lower; sensitivity below)
ETA = 1.0e-3           # Pa s, dynamic viscosity of water near 20 C (sugared drink higher; sensitivity below)
G = 9.81               # m/s^2
RHO = 1000.0           # kg/m^3
WRAP_H = 0.100         # m, leaf wrap height (assumed; leaf is about 100 mm tall)
T_WINDOW = 2 * 3600.0  # s, thaw window the product must survive

THETA_ADAXIAL = 76.08  # deg, apparent static contact angle, upper leaf surface (Jiang et al. 2022, measured)
THETA_ABAXIAL = 94.32  # deg, apparent static contact angle, lower leaf surface (Jiang et al. 2022, measured)


def washburn_height(r, theta_deg, t, eta=ETA, gamma=GAMMA):
    """Height reached by melt water in a tube of radius r after time t (m). Returns 0 if cos(theta) <= 0."""
    c = math.cos(math.radians(theta_deg))
    if c <= 0:
        return 0.0
    return math.sqrt(gamma * r * c * t / (2.0 * eta))


def washburn_time_to(height, r, theta_deg, eta=ETA, gamma=GAMMA):
    """Time (s) for the melt water to reach a given height in a tube of radius r. None if it cannot wet."""
    c = math.cos(math.radians(theta_deg))
    if c <= 0:
        return None
    return 2.0 * eta * height * height / (gamma * r * c)


def jurin_height(r, theta_deg, gamma=GAMMA):
    """Equilibrium capillary rise (m). Upper bound on how high a tube can hold liquid."""
    c = math.cos(math.radians(theta_deg))
    if c <= 0:
        return 0.0
    return 2.0 * gamma * c / (RHO * G * r)


def critical_radius(height, t, theta_deg, eta=ETA, gamma=GAMMA):
    """Smallest pore radius that wicks `height` within time `t`. Anything wider is a leak path."""
    c = math.cos(math.radians(theta_deg))
    if c <= 0:
        return None
    return 2.0 * eta * height * height / (gamma * c * t)


def fmt_len(m):
    if m is None:
        return "no wetting"
    if m < 1e-6:
        return f"{m*1e9:.1f} nm"
    if m < 1e-3:
        return f"{m*1e6:.2f} um"
    return f"{m*1e3:.1f} mm"


if __name__ == "__main__":
    out = {}

    r_crit = critical_radius(WRAP_H, T_WINDOW, THETA_ADAXIAL)
    print(f"Critical pore radius to wick the {WRAP_H*1e3:.0f} mm wrap in {T_WINDOW/3600:.0f} h "
          f"(adaxial angle {THETA_ADAXIAL:.1f} deg): {fmt_len(r_crit)}")
    out["critical_radius_m"] = r_crit

    paths = [
        ("intact cuticle pore, low (ivy-type, analogue)", 0.3e-9, THETA_ADAXIAL, "analogue, cuticle"),
        ("intact cuticle pore, high (coffee-type, analogue)", 2.0e-9, THETA_ADAXIAL, "analogue, cuticle"),
        ("exposed vessel, narrow (sycamore-type, analogue)", 2.75e-6, THETA_ADAXIAL, "analogue, vessel"),
        ("exposed vessel, wide (petiole-type, analogue)", 12.5e-6, THETA_ADAXIAL, "analogue, vessel"),
        ("intact cuticle, abaxial surface (measured angle)", 2.0e-9, THETA_ABAXIAL, "measured angle"),
    ]
    print("\nPath                                                  Height at 2 h   Time to 100 mm   Leak path?")
    rows = []
    for label, r, theta, basis in paths:
        h = washburn_height(r, theta, T_WINDOW)
        t_wrap = washburn_time_to(WRAP_H, r, theta)
        leak = h >= WRAP_H
        print(f"{label:<54}{fmt_len(h):>13}   {('%.1f min' % (t_wrap/60)) if t_wrap else 'no wetting':>14}   {'YES' if leak else 'no'}")
        rows.append({"path": label, "radius_m": r, "theta_deg": theta, "basis": basis,
                     "height_2h_m": h, "time_to_wrap_s": t_wrap, "leak_path": leak})
    out["paths"] = rows

    print("\nSensitivity of the critical radius to viscosity and contact angle:")
    sens = []
    for eta in (1.0e-3, 2.0e-3, 3.0e-3):
        for theta in (60.0, THETA_ADAXIAL):
            rc = critical_radius(WRAP_H, T_WINDOW, theta, eta=eta)
            print(f"  eta {eta*1e3:.0f} mPa s, theta {theta:5.1f} deg -> r_crit {fmt_len(rc)}")
            sens.append({"eta_Pa_s": eta, "theta_deg": theta, "r_crit_m": rc})
    out["sensitivity"] = sens

    with open("leaf_wicking_screen_results.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("\nWrote leaf_wicking_screen_results.json")
