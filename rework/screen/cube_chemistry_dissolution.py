"""Dissolution-time model for the 14 mm Singha Lemon Soda Cube (T8 part b). Model estimate, not a measurement.

Standard library only. Fixed seed. Run with: python -I cube_chemistry_dissolution.py
Writes cube_chemistry_dissolution_results.json next to this file.

Structure
- Stage A: disintegration of the cube into fragments (time t_A; ASSUMPTION, anchored to the opened Atchade et al.
  2025 effervescent tablet times (156 to 307 s for 0.45 to 0.52 g tablets in 200 mL at 25 C) and the Ph. Eur.
  5 minute pass criterion).
- Stage B: dissolution of the fragments by Noyes-Whitney mass transfer, shrinking sphere,
  dissolved mass balance with a bulk concentration that rises with time. The mass-transfer coefficient
  uses the Ranz-Marshall Sherwood correlation Sh = 2 + 0.6 Re^0.5 Sc^(1/3) (tier S, Wikipedia
  Sherwood page; Sc is above the printed validity range, which is flagged). The relative velocity
  U is the bubble-driven flow (unstirred) or a stirrer-driven flow (stirred). Both are ASSUMPTIONS.
- The acid-base reaction and CO2 release are treated as fast (tier S for the carbonic acid rate
  constants; the proton transfer step is assumed instantaneous, ASSUMPTION).
- Total time to full dissolution = t_A + t_B (a conservative sum: dissolution during disintegration is
  not credited).
- Saturation concentration Cs. The whole fragment is treated as one solid that dissolves at the saturation
  concentration of potassium bicarbonate (224 g/L, the least soluble reactant read; conservative). The
  citric acid solubility (59.2 percent w/w at 20 C, S) is NOT used in the central case. It enters only the
  composition-weighted variants and the tornado (added 2026-10-20), where Cs is
  varied by 0.7 and 1.5 and replaced by a mass-weighted value of the components.
- Flow at the fragment. The unstirred relative flow (0.1 to 2 mm/s) and the stirred flow (5 to 30 mm/s) are
  ASSUMPTIONS and are kept as the central parameter set. A derived bracket (flow_bracket_25C in the results)
  adds: the no-flow limit Sh = 2 (S, Sherwood page); solutal natural convection from an isolated sphere
  (Steinberger and Treybal correlation as printed in NPTEL lecture notes, S; Grashof number form from the
  Wikipedia Grashof page, S; density step from an additive-volume estimate, ASSUMPTION); a gas-driven slip
  velocity from the power of the rising gas (epsilon = g u_s, an energy balance) with the inertial-range
  eddy speed (epsilon d)^(1/3) (textbook scaling, not opened: ASSUMPTION); and the free-fall velocity of a
  fragment (Schiller-Naumann drag, formula not opened, checked against the benchmark value 1.0917 at Re 100
  on the MFiX tutorial page), which acts for seconds only. None of these replaces a measurement.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cube_chemistry_dissolution_results.json")

# ---------------- inputs ----------------
SIDE_MM = 14.0               # design, cube edge
MASS_G = 3.79                # design central mass (DERIVED from ASSUMPTION inputs, submission 09)
MASS_RANGE_G = (3.46, 4.24)  # submission 09 range (ASSUMPTION of the inputs)
VOL_L = 0.330                # serve volume (design)
REACTANTS_G = 2.94           # KHCO3 0.81 + citric 2.10 (design)
SOLUBLE_FRACTION = 1.0       # ASSUMPTION: binder, filler and flavour dissolve (not known, limit)
CS_KHCO3_G_L = 224.0         # S, Wikipedia potassium bicarbonate 22.4 g per 100 mL at 20 C (used at all T; ASSUMPTION)
# Citric acid saturation, 20 C: 59.2 percent w/w (S, Wikipedia citric acid) converted to g/L with the specific gravity of
# citric acid solutions (S, CORECHEM chart at 15 C: 58 percent 1.2627, 60 percent 1.2738; interpolated at 59.2 percent).
# The 15 C chart is applied at 20 C (the difference is below 0.5 percent, ASSUMPTION). DERIVED, tier S.
CITRIC_SOL_W_W = 0.592
CITRIC_SG_58, CITRIC_SG_60 = 1.2627, 1.2738
CITRIC_SG_592 = CITRIC_SG_58 + (59.2 - 58.0) / 2.0 * (CITRIC_SG_60 - CITRIC_SG_58)
CS_CITRIC_G_L = CITRIC_SOL_W_W * CITRIC_SG_592 * 1000.0       # about 751 g/L
SUCRALOSE_SOL_G_L = 283.0    # S, Wikipedia sucralose, 20 C (saved page wikipedia_physical_constants.md)
MASS_KHCO3_G, MASS_CITRIC_G, MASS_SUCRALOSE_G = 0.81, 2.10, 0.033
G_ACC = 9.80665              # m/s2, CONSTANT

# Water properties (S, Wikipedia water data page, read 2026-10-20)
WATER = {  # T C: (dynamic viscosity mPa s, density g/cm3)
    20.0: (1.0050, 0.9982071),
    25.0: (0.8937, 0.9970479),
    30.0: (0.8007, 0.9956502),
}
T_REF = 25.0

# Diffusivity inputs at 25 C
D_CO2_25 = 1.92e-9           # S, Wikipedia mass diffusivity (1.92e-5 cm2/s); reference only
LAMBDA_K_25 = 73.5           # S cm2/mol, Wikipedia molar conductivity (Laidler and Meiser; T not stated; 25 C ASSUMED)
F_FARADAY = 96485.33         # C/mol, CONSTANT
R_GAS = 8.314462618          # J/(mol K), CONSTANT
D_K_25 = R_GAS * 298.15 * (LAMBDA_K_25 * 1e-4) / (1.0 ** 2 * F_FARADAY ** 2)   # m2/s, DERIVED (Nernst-Hartley)
# HCO3- diffusivity at 25 C. Zeebe 2011 (Geochim. Cosmochim. Acta 75, 2483; P, molecular dynamics fit, Table 2):
# D = D0 [(T/Ti) - 1]^c with D0 = 7.0158e-9 m2/s, Ti = 204.0282 K, c = 2.3942 (273 to 373 K). Other values read:
# 1.09e-9 (Falkowski and Raven 2007 via BioNumbers, S), 1.15e-9 (Fridlyand et al. 1996 via BioNumbers, S),
# 1.19e-9 (conductivity-based infinite dilution estimate printed in Zeebe 2011, which he judges somewhat high).
ZEEBE_HCO3 = (7.0158e-9, 204.0282, 2.3942)


def zeebe_hco3(t_c):
    d0, ti, c = ZEEBE_HCO3
    return d0 * ((t_c + 273.15) / ti - 1.0) ** c


D_HCO3_CENTRAL = zeebe_hco3(25.0)            # about 1.10e-9 m2/s
D_HCO3_BRACKET = (1.0e-9, 1.2e-9)  # spread of the four values above (S and P); the central is the MD fit
D_CIT_BRACKET = (0.5e-9, 0.9e-9)   # ASSUMPTION: no sourced citric acid binary diffusivity at 25 C (Melia et al. 2019 data not printed)

# Disintegration time (ASSUMPTION). Anchors: Atchade et al. 2025 (opened; P): five formulations of 0.45 to 0.52 g
# tablets (11.1 mm diameter, 4.28 mm thick, about 20 percent citric acid plus sodium bicarbonate) disintegrated in
# 307, 156, 263, 209 and 261 s in 200 mL at 25 C (median 209 s); Ph. Eur. effervescent test pass at 5 min (edition 7.0
# mirror, S). The cube is 3.79 g, 14 mm thick (3.3 times the tablet thickness) and 78 percent reactants, so the
# range is set at 60 s (low), 210 s (the median of the five tablets) and 600 s (twice the compendial limit). Revised
# on 2026-10-20 from 60/150/300 after the Atchade paper was opened.
TA_LOW_CENTRAL_HIGH = (60.0, 210.0, 600.0)

# Fragment radius after disintegration (ASSUMPTION): fine granulate to coarse fragments
RF_MM = (0.2, 0.5, 2.0)

# Relative flow at the fragment (ASSUMPTION). Unstirred: bubble-driven only. Stirred: magnetic stirrer.
U_UNSTIRRED_MM_S = (2.0, 0.5, 0.1)   # low time, central, high time
U_STIRRED_MM_S = (30.0, 10.0, 5.0)

# Hydrodynamic and porosity ASSUMPTIONS
POROSITY = (0.10, 0.20, 0.30)        # ASSUMPTION; solid density = bulk / (1 - porosity)

# Ranz-Marshall validity (S): Sc below 250. Sc here is far above, so the correlation is extrapolated.
SC_VALID_MAX = 250.0


def water_props(t_c):
    mu_mpa, rho = WATER[t_c]
    return mu_mpa * 1e-3, rho * 1000.0   # Pa s, kg/m3


def d_salt(t_c, d_hco3):
    """Salt effective diffusivity (Nernst-type for a 1:1 electrolyte): 2 D+ D- / (D+ + D-)."""
    d_k = D_K_25
    d_eff_25 = 2.0 * d_k * d_hco3 / (d_k + d_hco3)
    return d_eff_25 * scale_T(t_c)


def scale_T(t_c):
    """Stokes-Einstein scaling of diffusivity with temperature and viscosity (S form)."""
    mu_t, _ = water_props(t_c)
    mu_25, _ = water_props(T_REF)
    T = t_c + 273.15
    T25 = T_REF + 273.15
    return (T / T25) * (mu_25 / mu_t)


def d_citric(t_c, d_cit_25):
    return d_cit_25 * scale_T(t_c)


def d_eff(t_c, d_hco3, d_cit25):
    """Harmonic (resistance) average of citric acid and salt diffusivities, mass-weighted (ASSUMPTION)."""
    w_c = 2.10 / REACTANTS_G
    w_k = 0.81 / REACTANTS_G
    dc = d_citric(t_c, d_cit25)
    dk = d_salt(t_c, d_hco3)
    return 1.0 / (w_c / dc + w_k / dk)


def sherwood(u_ms, d_m, nu, diff):
    """Ranz-Marshall for a sphere: Sh = 2 + 0.6 Re^0.5 Sc^(1/3). Re = U d / nu, Sc = nu / D."""
    re = u_ms * d_m / nu
    sc = nu / diff
    return 2.0 + 0.6 * math.sqrt(max(re, 0.0)) * sc ** (1.0 / 3.0), re, sc


def sherwood_nc(d_m, nu, diff, drho_rel):
    """Solutal natural convection from an isolated sphere in a quiescent liquid (Steinberger and Treybal 1960, as printed
    in NPTEL lecture notes, S): Sh = 2 + 0.569 (Gr Sc)^(1/4) for Gr Sc < 1e8, Sh = 2 + 0.0254 (Gr Sc)^(1/3) Sc^0.244 above.
    Gr = g (delta rho / rho) d^3 / nu^2 (mass-transfer Grashof number, Wikipedia Grashof page, S)."""
    gr = G_ACC * drho_rel * d_m ** 3 / nu ** 2
    sc = nu / diff
    grsc = gr * sc
    if grsc < 1e8:
        return 2.0 + 0.569 * grsc ** 0.25, grsc
    return 2.0 + 0.0254 * grsc ** (1.0 / 3.0) * sc ** 0.244, grsc


def drho_relative(rho_s_kg_m3, cs_g_l, rho_w_kg_m3):
    """Relative density step of a saturated solution of the cube material, additive-volume estimate (ASSUMPTION):
    delta rho = c (1 - rho_w / rho_solid); real salt solutions are somewhat denser (not used). cs_g_l in g/L equals kg/m3."""
    return cs_g_l * (1.0 - rho_w_kg_m3 / rho_s_kg_m3) / rho_w_kg_m3


def dissolve_fragments(r0_m, m_solid_kg, t_c, u_ms, rho_s, d_h, d_c, cs=CS_KHCO3_G_L, mode="RM"):
    """Shrinking-sphere dissolution of N identical fragments of radius r0. Returns time (s) to full dissolution.

    State x = r^2: dx/dt = -Sh D dC / rho_s, with dC = Cs - C(t) (kg/m3) and C(t) = dissolved mass / V.
    mode "RM": Sherwood from Ranz-Marshall at the local radius (Sh = 2 + 0.6 Re^0.5 Sc^(1/3), Re = U d / nu).
    mode "diff": no relative flow, Sh = 2 (the diffusion limit).
    mode "NC": solutal natural convection (Steinberger and Treybal), isolated sphere, Gr from the local diameter.
    Fixed step with an exact final step; the step is set from the initial rate and refined by a fixed count of 2000 steps.
    """
    mu, rho_w = water_props(t_c)
    nu = mu / rho_w
    diff = d_eff(t_c, d_h, d_c)
    v_liq = VOL_L * 1e-3                       # m3
    per_particle_vol = (4.0 / 3.0) * math.pi * r0_m ** 3
    n_part = m_solid_kg / (per_particle_vol * rho_s)
    drho_rel = drho_relative(rho_s, cs, rho_w)

    def sh_at(d_m):
        if mode == "diff":
            return 2.0
        if mode == "NC":
            return sherwood_nc(d_m, nu, diff, drho_rel)[0]
        return sherwood(u_ms, d_m, nu, diff)[0]

    x = r0_m * r0_m
    sh0 = sh_at(2.0 * r0_m)
    t_est = x * rho_s / (sh0 * diff * cs)
    dt = t_est / 2000.0
    t = 0.0
    steps = 0
    while steps < 40000:
        r = math.sqrt(x)
        sh = sh_at(2.0 * r)
        m_left = n_part * (4.0 / 3.0) * math.pi * rho_s * r ** 3
        c_bulk = (m_solid_kg - m_left) / v_liq
        dc = max(cs - c_bulk, 1e-9)
        rate = sh * diff * dc / rho_s           # m2/s
        if rate * dt >= x:
            t += x / rate
            return t
        x -= rate * dt
        t += dt
        steps += 1
    return t


def fragment_time(t_c, rf_mm, u_mm_s, porosity, d_hco3, d_cit25, cs=CS_KHCO3_G_L, mode="RM"):
    """Time (s) for the fragment population to dissolve (stage B)."""
    rho_b = MASS_G / ((SIDE_MM / 10.0) ** 3)     # g/cm3
    rho_s = rho_b / (1.0 - porosity) * 1000.0    # kg/m3
    m_solid_kg = MASS_G * SOLUBLE_FRACTION / 1000.0
    return dissolve_fragments(rf_mm * 1e-3, m_solid_kg, t_c, u_mm_s * 1e-3, rho_s, d_hco3, d_cit25, cs=cs, mode=mode)


def intact_cube_time(t_c, u_mm_s, porosity, d_hco3, d_cit25):
    """Time (s) if the intact cube dissolved as one shrinking sphere of the same volume (reference only)."""
    vol_cm3 = (SIDE_MM / 10.0) ** 3
    r_eq_m = ((3.0 * vol_cm3 / (4.0 * math.pi)) ** (1.0 / 3.0)) * 1e-2
    rho_b = MASS_G / vol_cm3
    rho_s = rho_b / (1.0 - porosity) * 1000.0
    m_solid_kg = MASS_G * SOLUBLE_FRACTION / 1000.0
    return dissolve_fragments(r_eq_m, m_solid_kg, t_c, u_mm_s * 1e-3, rho_s, d_hco3, d_cit25)


def cs_weighted_all():
    """Mass-weighted saturation concentration over all components of the cube (g/L). KHCO3 224, citric acid about 751,
    sucralose 283 (all S); binder, filler and flavour (0.85 g, unknown) taken at the KHCO3 value (ASSUMPTION, lower)."""
    other = MASS_G - (MASS_KHCO3_G + MASS_CITRIC_G + MASS_SUCRALOSE_G)
    return (MASS_KHCO3_G * CS_KHCO3_G_L + MASS_CITRIC_G * CS_CITRIC_G_L + MASS_SUCRALOSE_G * SUCRALOSE_SOL_G_L
            + other * CS_KHCO3_G_L) / MASS_G


def cs_weighted_reactants():
    """Mass-weighted over KHCO3, citric acid and sucralose only; the remainder takes the same weighted value (g/L)."""
    m = MASS_KHCO3_G + MASS_CITRIC_G + MASS_SUCRALOSE_G
    return (MASS_KHCO3_G * CS_KHCO3_G_L + MASS_CITRIC_G * CS_CITRIC_G_L + MASS_SUCRALOSE_G * SUCRALOSE_SOL_G_L) / m


def sweep(d_hco3_mid, d_cit_mid):
    """Central, low and high values per condition."""
    res = {}
    for t_c in (20.0, 25.0, 30.0):
        row = {}
        for regime, uvals in (("unstirred", U_UNSTIRRED_MM_S), ("stirred", U_STIRRED_MM_S)):
            # central fragment and disintegration
            t_b = fragment_time(t_c, RF_MM[1], uvals[1], POROSITY[1], d_hco3_mid, d_cit_mid)
            row[regime] = {
                "U_mm_s_central": uvals[1],
                "t_B_fragments_s": round(t_b, 1),
                "t_total_central_s": round(TA_LOW_CENTRAL_HIGH[1] + t_b, 1),
                "intact_cube_t_s_reference": round(intact_cube_time(t_c, uvals[1], POROSITY[1], d_hco3_mid, d_cit_mid), 1),
            }
        res[str(int(t_c))] = row
    return res


def tornado(t_c=25.0):
    """One-at-a-time swings for the unstirred and stirred central cases at 25 C."""
    base_hco3, base_cit = D_HCO3_CENTRAL, 0.7e-9
    rows = []

    def tot(rf=RF_MM[1], u=None, ta=TA_LOW_CENTRAL_HIGH[1], por=POROSITY[1], dh=base_hco3, dc=base_cit, regime="unstirred",
            cs=CS_KHCO3_G_L):
        if u is None:
            u = U_UNSTIRRED_MM_S[1] if regime == "unstirred" else U_STIRRED_MM_S[1]
        return ta + fragment_time(t_c, rf, u, por, dh, dc, cs=cs)

    for regime in ("unstirred", "stirred"):
        b = tot(regime=regime)
        cand = [
            ("fragment radius 0.2 to 2.0 mm", tot(rf=RF_MM[0], regime=regime), tot(rf=RF_MM[2], regime=regime)),
            ("flow velocity (regime range)",
             tot(u=(U_UNSTIRRED_MM_S[0] if regime == "unstirred" else U_STIRRED_MM_S[0]) * 1.0, regime=regime),
             tot(u=(U_UNSTIRRED_MM_S[2] if regime == "unstirred" else U_STIRRED_MM_S[2]) * 1.0, regime=regime)),
            ("disintegration time 60 to 600 s", tot(ta=TA_LOW_CENTRAL_HIGH[0], regime=regime), tot(ta=TA_LOW_CENTRAL_HIGH[2], regime=regime)),
            ("porosity 0.10 to 0.30", tot(por=POROSITY[0], regime=regime), tot(por=POROSITY[2], regime=regime)),
            ("citric D 0.5 to 0.9e-9", tot(dc=D_CIT_BRACKET[1], regime=regime), tot(dc=D_CIT_BRACKET[0], regime=regime)),
            ("HCO3- D 1.0 to 1.2e-9", tot(dh=D_HCO3_BRACKET[1], regime=regime), tot(dh=D_HCO3_BRACKET[0], regime=regime)),
            ("saturation concentration Cs x1.5 to x0.7 (KHCO3 224 g/L basis)", tot(cs=1.5 * CS_KHCO3_G_L, regime=regime),
             tot(cs=0.7 * CS_KHCO3_G_L, regime=regime)),
            ("Cs mass-weighted over all components, 517 g/L (against KHCO3 only, 224 g/L)", tot(cs=cs_weighted_all(), regime=regime),
             tot(regime=regime)),
            ("Cs mass-weighted over the reactants, 601 g/L (against KHCO3 only, 224 g/L)", tot(cs=cs_weighted_reactants(), regime=regime),
             tot(regime=regime)),
        ]
        for name, lo, hi in cand:
            rows.append({"regime": regime, "input": name, "t_low_s": round(min(lo, hi), 1), "t_high_s": round(max(lo, hi), 1),
                         "swing_s": round(abs(hi - lo), 1), "base_s": round(b, 1)})
    return rows


GLASS_D_M = 0.065            # ASSUMPTION (55 to 75 mm), same glass as the fizz model
CO2_MOL_PER_SERVE = MASS_KHCO3_G / 100.115


def settling_velocity(r_m, rho_p, t_c):
    """Terminal velocity (m/s) and Reynolds number of a sphere with Schiller-Naumann drag, by bisection.
    C_D = 24/Re (1 + 0.15 Re^0.687) (formula text not opened; the benchmark C_D = 1.0917 at Re = 100 on the MFiX
    tutorial page is reproduced to 0.003 percent, S, so the form is used and flagged)."""
    mu, rho_w = water_props(t_c)
    weight = (4.0 / 3.0) * math.pi * r_m ** 3 * (rho_p - rho_w) * G_ACC

    def resid(v):
        re = rho_w * v * 2.0 * r_m / mu
        cd = 24.0 / re * (1.0 + 0.15 * re ** 0.687)
        return 0.5 * rho_w * cd * math.pi * r_m ** 2 * v ** 2 - weight

    lo, hi = 1e-6, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if resid(mid) < 0:
            lo = mid
        else:
            hi = mid
    v = 0.5 * (lo + hi)
    return v, rho_w * v * 2.0 * r_m / mu


def gas_slip_velocity(d_m, t_gas_s, gas_fraction, t_c=25.0):
    """Order-of-magnitude slip velocity at a fragment of diameter d from the power of rising CO2 (DERIVED, textbook scaling).

    Gas flow: all CO2 (8.09 mmol) released as gas at t_c and 1 atm, a share gas_fraction of it bubbling out over t_gas.
    Superficial velocity u_s = Q / A_glass. Energy balance of gas rising through liquid depth H: power rho g Q H over
    mass rho A H gives epsilon = g u_s (W/kg). Eddy speed at scale d in the inertial range: (epsilon d)^(1/3)
    (Kolmogorov scaling, not opened: ASSUMPTION). Kolmogorov length (nu^3 / epsilon)^(1/4) (Wikipedia, S) checks d > eta."""
    mu, rho_w = water_props(t_c)
    nu = mu / rho_w
    v_gas_m3 = CO2_MOL_PER_SERVE * 8.314462618 * (t_c + 273.15) / 101325.0
    area = math.pi * (GLASS_D_M / 2.0) ** 2
    u_s = gas_fraction * v_gas_m3 / (area * t_gas_s)
    eps = G_ACC * u_s
    eta = (nu ** 3 / eps) ** 0.25
    return (eps * d_m) ** (1.0 / 3.0), u_s, eps, eta, v_gas_m3


def flow_bracket(t_c=25.0):
    """Stage B and total time (s) at the central fragment sizes for each flow basis (derived bracket and assumed values)."""
    d_h, d_c = D_HCO3_CENTRAL, 0.7e-9
    por = POROSITY[1]
    rho_b = MASS_G / ((SIDE_MM / 10.0) ** 3)
    rho_s = rho_b / (1.0 - por) * 1000.0
    mu, rho_w = water_props(t_c)
    nu = mu / rho_w
    diff = d_eff(t_c, d_h, d_c)
    out = {"temperature_C": t_c, "t_A_s": TA_LOW_CENTRAL_HIGH[1], "porosity": por, "Cs_g_L": CS_KHCO3_G_L,
           "drho_over_rho_additive_volume": round(drho_relative(rho_s, CS_KHCO3_G_L, rho_w), 4), "cases": {}, "settling": {}}
    glass_area = math.pi * (GLASS_D_M / 2.0) ** 2
    depth = VOL_L * 1e-3 / glass_area
    out["liquid_depth_m"] = round(depth, 4)
    for rf in RF_MM:
        d0 = 2.0 * rf * 1e-3
        rows = {}

        def add(name, u_mm_s, mode, extra=None):
            tb = fragment_time(t_c, rf, u_mm_s, por, d_h, d_c, mode=mode)
            if mode == "RM":
                sh0 = sherwood(u_mm_s * 1e-3, d0, nu, diff)[0]
            elif mode == "NC":
                sh0, grsc = sherwood_nc(d0, nu, diff, drho_relative(rho_s, CS_KHCO3_G_L, rho_w))
            else:
                sh0 = 2.0
            row = {"Sh_initial": round(sh0, 2), "t_B_s": round(tb, 1), "t_total_s": round(TA_LOW_CENTRAL_HIGH[1] + tb, 1)}
            if mode == "RM":
                row["U_mm_s"] = round(u_mm_s, 3)
            if mode == "NC":
                row["Gr_Sc_initial"] = float("%.3g" % grsc)
                row["Gr_Sc_below_1e8_validity_limit"] = bool(grsc < 1e8)
            if extra:
                row.update(extra)
            rows[name] = row

        add("no_flow_limit_Sh_2", 0.0, "diff")
        add("assumed_unstirred_0.1_mm_s", 0.1, "RM")
        add("assumed_unstirred_0.5_mm_s_central", 0.5, "RM")
        add("assumed_unstirred_2.0_mm_s", 2.0, "RM")
        add("solutal_natural_convection_isolated_sphere", 0.0, "NC")
        for t_gas, frac, tag in ((120.0, 1.0, "gas_driven_120s_all_gas"), (600.0, 0.5, "gas_driven_600s_half_gas")):
            u_slip, u_s, eps, eta, _ = gas_slip_velocity(d0, t_gas, frac, t_c)
            add(tag, u_slip * 1000.0, "RM", {"u_s_mm_s": round(u_s * 1000.0, 3), "epsilon_W_kg": float("%.3g" % eps),
                                              "kolmogorov_length_mm": round(eta * 1000.0, 3),
                                              "fragment_diameter_over_kolmogorov": round(d0 / eta, 1)})
        add("assumed_stirred_5_mm_s", 5.0, "RM")
        add("assumed_stirred_10_mm_s_central", 10.0, "RM")
        add("assumed_stirred_30_mm_s", 30.0, "RM")
        out["cases"]["r_%.1f_mm" % rf] = rows
        v_t, re_t = settling_velocity(rf * 1e-3, rho_s, t_c)
        out["settling"]["r_%.1f_mm" % rf] = {"terminal_velocity_mm_s": round(v_t * 1000.0, 1), "Re": round(re_t, 1),
                                              "fall_time_through_liquid_s": round(depth / v_t, 2)}
    out["note"] = ("Settling acts only until the fragments reach the bottom of the glass (seconds), so it is not a sustained flow. "
                   "Natural convection is for an isolated sphere in an unbounded quiescent liquid; a fragment bed on the bottom of a "
                   "glass with a dense solution pooling beneath it would be slower (not modelled). The gas-driven slip velocity is an "
                   "order of magnitude from scaling, not a correlation fitted to effervescent systems.")
    return out


def monte_carlo(n=3000, seed=20261020, fixed_t=None, cs=CS_KHCO3_G_L):
    rng = random.Random(seed)
    totals = {"stirred": [], "unstirred": []}
    for _ in range(n):
        t_c = rng.choice((20.0, 25.0, 30.0)) if fixed_t is None else fixed_t
        regime = "stirred" if rng.random() < 0.5 else "unstirred"
        ta = rng.uniform(TA_LOW_CENTRAL_HIGH[0], TA_LOW_CENTRAL_HIGH[2])
        rf = math.exp(rng.uniform(math.log(RF_MM[0]), math.log(RF_MM[2])))
        if regime == "stirred":
            u = math.exp(rng.uniform(math.log(U_STIRRED_MM_S[2]), math.log(U_STIRRED_MM_S[0])))
        else:
            u = math.exp(rng.uniform(math.log(U_UNSTIRRED_MM_S[2]), math.log(U_UNSTIRRED_MM_S[0])))
        por = rng.uniform(POROSITY[0], POROSITY[2])
        dc = rng.uniform(D_CIT_BRACKET[0], D_CIT_BRACKET[1])
        dh = rng.uniform(D_HCO3_BRACKET[0], D_HCO3_BRACKET[1])
        tb = fragment_time(t_c, rf, u, por, dh, dc, cs=cs)
        totals[regime].append(ta + tb)
    out = {"n_per_regime_approx": n // 2, "seed": seed, "Cs_g_L": round(cs, 1),
           "temperature_C": "pooled 20, 25, 30" if fixed_t is None else fixed_t,
           "draws": "uniform on the assumed ranges (log-uniform for fragment radius and flow); stirred and unstirred drawn 50/50; NOT a probability distribution of real cubes"}
    allv = []
    for k, v in totals.items():
        v.sort()
        allv.extend(v)
        out[k] = {"p5_s": round(v[int(0.05 * (len(v) - 1))], 1), "p50_s": round(v[int(0.5 * (len(v) - 1))], 1),
                  "p95_s": round(v[int(0.95 * (len(v) - 1))], 1)}
    allv.sort()
    out["all"] = {"p5_s": round(allv[int(0.05 * (len(allv) - 1))], 1),
                  "p50_s": round(allv[int(0.5 * (len(allv) - 1))], 1),
                  "p95_s": round(allv[int(0.95 * (len(allv) - 1))], 1)}
    return out


def main():
    d_hco3_mid = D_HCO3_CENTRAL
    d_cit_mid = 0.7e-9
    rho_b = MASS_G / ((SIDE_MM / 10.0) ** 3)
    out = {
        "task": "T8 part b, dissolution time model (model estimate, not a measurement)",
        "date": "2026-10-20",
        "inputs": {
            "cube_side_mm": {"value": SIDE_MM, "tier": "design"},
            "cube_mass_g": {"value": MASS_G, "tier": "design; DERIVED from ASSUMPTION inputs (submission 09)"},
            "cube_mass_range_g": {"value": list(MASS_RANGE_G), "tier": "submission 09 (ASSUMPTION range)"},
            "bulk_density_g_cm3": {"value": round(rho_b, 4), "tier": "DERIVED from mass and volume"},
            "porosity": {"value": list(POROSITY), "tier": "ASSUMPTION (low, central, high)"},
            "solid_density_g_cm3_central": {"value": round(rho_b / (1 - POROSITY[1]), 4), "tier": "DERIVED from bulk density and porosity"},
            "volume_L": {"value": VOL_L, "tier": "design"},
            "reactant_mass_g": {"value": REACTANTS_G, "tier": "design (KHCO3 0.81 and citric 2.10)"},
            "soluble_fraction": {"value": SOLUBLE_FRACTION, "tier": "ASSUMPTION (binder, filler and flavour dissolve; limit)"},
            "Cs_KHCO3_g_L_20C": {"value": CS_KHCO3_G_L, "tier": "S, Wikipedia potassium bicarbonate 22.4 g/100 mL; T dependence ASSUMPTION (none). Applied to the WHOLE cube mass (conservative: KHCO3 is the least soluble reactant read)"},
            "Cs_citric_g_L_20C": {"value": round(CS_CITRIC_G_L, 1), "tier": "DERIVED from S: 59.2 percent w/w (Wikipedia citric acid) times the solution specific gravity 1.2694 (CORECHEM chart at 15 C, interpolated between 58 and 60 percent); used only in the composition-weighted variants"},
            "Cs_mass_weighted_all_components_g_L": {"value": round(cs_weighted_all(), 1), "tier": "DERIVED (heuristic: mass-weighted over KHCO3 224, citric acid 751, sucralose 283; binder, filler and flavour at 224, ASSUMPTION)"},
            "Cs_mass_weighted_reactants_g_L": {"value": round(cs_weighted_reactants(), 1), "tier": "DERIVED (heuristic: mass-weighted over KHCO3, citric acid and sucralose only)"},
            "water_viscosity_density": {"value": {str(k): v for k, v in WATER.items()}, "tier": "S, Wikipedia water data page (read 2026-10-20)"},
            "D_CO2_25C_m2_s": {"value": D_CO2_25, "tier": "S, Wikipedia mass diffusivity (reference only)"},
            "K_conductivity_S_cm2_mol": {"value": LAMBDA_K_25, "tier": "S, Wikipedia molar conductivity citing Laidler and Meiser (T not stated)"},
            "D_K_25C_m2_s": {"value": round(D_K_25, 13), "tier": "DERIVED (Nernst-Hartley from the K+ conductivity, 25 C assumed)"},
            "D_HCO3_central_25C_m2_s": {"value": round(D_HCO3_CENTRAL, 13), "tier": "P, Zeebe 2011 molecular dynamics fit (Table 2); DERIVED from the fit"},
            "D_HCO3_bracket_m2_s": {"value": list(D_HCO3_BRACKET), "tier": "S and P: Falkowski and Raven 2007 1.09e-9 (S, BioNumbers); Zeebe 2011 1.10e-9 (P, MD); Fridlyand 1996 1.15e-9 (S, BioNumbers); conductivity estimate 1.19e-9 (S, printed in Zeebe 2011)"},
            "D_citric_bracket_m2_s_25C": {"value": list(D_CIT_BRACKET), "tier": "ASSUMPTION, UNVERIFIED: no opened source gives a value (search snippets give about 0.7e-9 and 0.68e-9 in water-butanol, not opened; Melia et al. record prints no value)"},
            "disintegration_time_s": {"value": list(TA_LOW_CENTRAL_HIGH), "tier": "ASSUMPTION, anchored to Atchade et al. 2025 (opened, P: 156 to 307 s for 0.5 g tablets) and Ph. Eur. effervescent test (5 min, S)"},
            "fragment_radius_mm": {"value": list(RF_MM), "tier": "ASSUMPTION"},
            "flow_unstirred_mm_s": {"value": list(U_UNSTIRRED_MM_S), "tier": "ASSUMPTION (bubble-driven; low time, central, high time)"},
            "flow_stirred_mm_s": {"value": list(U_STIRRED_MM_S), "tier": "ASSUMPTION (magnetic stirrer)"},
            "Sherwood_correlation": {"value": "Ranz-Marshall 2 + 0.6 Re^0.5 Sc^(1/3)", "tier": "S, Wikipedia Sherwood number (Sc validity below 250 exceeded: flagged)"},
        },
    }

    # Gas balance (DERIVED)
    n_co2 = 0.81 / 100.115                      # mol per serve
    v_gas_25 = n_co2 * 0.082057 * (25 + 273.15) / 1.0   # L at 1 atm, 25 C (all CO2 released)
    out["gas_balance"] = {
        "CO2_mol_per_serve": round(n_co2, 6),
        "gas_volume_if_all_released_mL_25C_1atm": round(v_gas_25 * 1000.0, 1),
        "note": "The dose of 0.55 volumes is below the 1 atm saturation at 20 to 30 C (about 0.86 to 0.66 volumes, DERIVED from the Sander constant), so the liquid can hold it at equilibrium. Near the dissolving fragments the local concentration is far higher and bubbles can form there; how much of the 198 mL leaves as bubbles during dissolution (so how much is dissolved at serve) is NOT known. It is the retention input of the fizz model (break-even 0.408).",
    }

    central = sweep(d_hco3_mid, d_cit_mid)
    out["central_by_temperature_s"] = central

    # Low, central, high (deterministic bounds from the regime and input ranges, 25 C)
    low = {"t_A": TA_LOW_CENTRAL_HIGH[0], "rf": RF_MM[0], "u_stir": U_STIRRED_MM_S[0], "u_un": U_UNSTIRRED_MM_S[0]}
    out["bounds_25C_s"] = {
        "low_stirred": round(TA_LOW_CENTRAL_HIGH[0] + fragment_time(25.0, RF_MM[0], U_STIRRED_MM_S[0], POROSITY[0], D_HCO3_BRACKET[1], D_CIT_BRACKET[1]), 1),
        "central_stirred": round(TA_LOW_CENTRAL_HIGH[1] + fragment_time(25.0, RF_MM[1], U_STIRRED_MM_S[1], POROSITY[1], d_hco3_mid, d_cit_mid), 1),
        "high_unstirred": round(TA_LOW_CENTRAL_HIGH[2] + fragment_time(25.0, RF_MM[2], U_UNSTIRRED_MM_S[2], POROSITY[2], D_HCO3_BRACKET[0], D_CIT_BRACKET[0]), 1),
        "central_unstirred": round(TA_LOW_CENTRAL_HIGH[1] + fragment_time(25.0, RF_MM[1], U_UNSTIRRED_MM_S[1], POROSITY[1], d_hco3_mid, d_cit_mid), 1),
    }

    out["tornado_25C"] = tornado(25.0)
    out["flow_bracket_25C"] = flow_bracket(25.0)
    # Central totals for the Cs variants (deterministic, 25 C)
    cs_var = {}
    for name, cs_v in (("Cs_224_KHCO3_only_central_basis", CS_KHCO3_G_L), ("Cs_x0.7", 0.7 * CS_KHCO3_G_L), ("Cs_x1.5", 1.5 * CS_KHCO3_G_L),
                       ("Cs_mass_weighted_all", cs_weighted_all()), ("Cs_mass_weighted_reactants", cs_weighted_reactants())):
        cs_var[name] = {
            "Cs_g_L": round(cs_v, 1),
            "stirred_total_s": round(TA_LOW_CENTRAL_HIGH[1] + fragment_time(25.0, RF_MM[1], U_STIRRED_MM_S[1], POROSITY[1], d_hco3_mid, d_cit_mid, cs=cs_v), 1),
            "unstirred_total_s": round(TA_LOW_CENTRAL_HIGH[1] + fragment_time(25.0, RF_MM[1], U_UNSTIRRED_MM_S[1], POROSITY[1], d_hco3_mid, d_cit_mid, cs=cs_v), 1),
        }
    out["Cs_variants_25C_central"] = cs_var
    out["monte_carlo"] = monte_carlo()
    out["monte_carlo_25C_only"] = monte_carlo(n=3000, seed=20261021, fixed_t=25.0)
    out["monte_carlo_25C_only_Cs_mass_weighted_all"] = monte_carlo(n=3000, seed=20261021, fixed_t=25.0, cs=cs_weighted_all())

    # Cross-checks
    mc = out["monte_carlo"]
    sc_range = {}
    for tc in (20.0, 25.0, 30.0):
        mu_, rho_ = water_props(tc)
        sc_range[str(int(tc))] = round((mu_ / rho_) / d_eff(tc, D_HCO3_CENTRAL, 0.7e-9), 0)
    out["cross_checks"] = {
        "Ph_Eur_effervescent_limit_s": 300,
        "Ph_Eur_note": "The 5 minute limit is for one tablet in 200 mL at 15 to 25 C (edition 7.0 mirror: Tablets monograph, not chapter 2.9.1). Pass means disintegration with no agglomerates; the cube test is not run.",
        "published_effervescent_times_s": {
            "Atchade_2025_F1_to_F5_opened_P": [307, 156, 263, 209, 261],
            "Atchade_2025_tablet": "0.45 to 0.52 g, 11.1 mm diameter, 4.28 mm thick, citric acid plus sodium bicarbonate about 20 percent of the mass, 1 tablet in 200 mL distilled water at 25 C, Ph. Eur. 10th ed. test",
            "cube_comparison": "cube is 7.3 to 8.4 times heavier, 3.3 times thicker and about 78 percent reactants: the tablet times are an order-of-magnitude anchor only",
            "Elagina_2022_furazolidone_100mL_under_s_abstract_only_S": 300},
        "central_25C_stirred_total_s": out["bounds_25C_s"]["central_stirred"],
        "central_25C_unstirred_total_s": out["bounds_25C_s"]["central_unstirred"],
        "intact_cube_25C_unstirred_reference_s": central["25"]["unstirred"]["intact_cube_t_s_reference"],
        "intact_cube_25C_stirred_reference_s": central["25"]["stirred"]["intact_cube_t_s_reference"],
        "Sc_range_20_to_30C_central_D_eff": sc_range,
        "Sherwood_validity_note": "Sc is far above the printed range (below 250); the correlation is extrapolated (limit).",
        "MC_p50_all_s": mc["all"]["p50_s"],
        "MC_p5_p95_all_s": [mc["all"]["p5_s"], mc["all"]["p95_s"]],
    }

    # Dominant uncertainty: largest swing in the unstirred and stirred tornado
    sw = sorted(out["tornado_25C"], key=lambda r: -r["swing_s"])
    out["dominant_uncertainty"] = {
        "largest_swing_row": sw[0],
        "top_three": sw[:3],
        "statement": "The fragment size after break-up has the largest one-at-a-time swing in both regimes; the disintegration time, the flow and the saturation concentration follow (see tornado_25C). The intact cube, with no break-up, is hours.",
    }
    out["limits"] = [
        "Model estimate. No dissolution was measured. The result depends on assumed fragment size, bubble and stirrer velocities, and disintegration time.",
        "The unstirred case rests on an assumed flow (0.1 to 2 mm/s). The derived bracket (flow_bracket_25C) runs from the no-flow limit (Sh = 2, slowest) to natural-convection and gas-driven estimates that approach the stirred case; none is a measurement, and a fragment bed on the glass bottom with dense solution pooling beneath it is not modelled.",
        "The whole cube mass is dissolved against the potassium bicarbonate solubility (224 g/L, S, conservative). Composition-weighted values (517 to 601 g/L, DERIVED heuristic) shorten the central times (see Cs_variants_25C_central); reaction in the boundary layer is not modelled.",
        "The citric acid binary diffusivity is not sourced (ASSUMPTION bracket, UNVERIFIED). The HCO3- value is a molecular dynamics fit (P) and three secondary values.",
        "Sherwood correlation is extrapolated to Sc of about 1000 (printed validity below 250).",
        "The disintegration range (60, 210 and 600 s) is an ASSUMPTION anchored to 0.5 g tablets, not to a 3.79 g cube.",
        "The Monte Carlo ranges are assumed uniform ranges, not measured distributions; the percentiles are not probabilities.",
        "The compendial end point (no agglomerates left) is earlier than full dissolution, and the total here sums disintegration and fragment dissolution without overlap (conservative).",
        "The gas-driven flow is not modelled from first principles; the flow range is an ASSUMPTION.",
        "Binder, filler and flavour are assumed fully soluble; insoluble residue would change the end point.",
        "Temperature effect on KHCO3 solubility is not sourced and is set to zero.",
    ]
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("central 25 C stirred total s:", out["bounds_25C_s"]["central_stirred"], "unstirred:", out["bounds_25C_s"]["central_unstirred"])
    print("bounds 25 C:", out["bounds_25C_s"])
    print("MC all p5/p50/p95:", mc["all"])
    print("MC 25 C only:", out["monte_carlo_25C_only"]["all"], out["monte_carlo_25C_only"]["stirred"], out["monte_carlo_25C_only"]["unstirred"])
    print("Sc:", sc_range, "D_HCO3 central:", D_HCO3_CENTRAL)
    print("tornado top:", sw[0])
    print("tornado rows 25 C:")
    for r in out["tornado_25C"]:
        print("  ", r["regime"], r["input"], r["t_low_s"], r["t_high_s"], r["swing_s"])
    print("Cs variants:", out["Cs_variants_25C_central"])
    print("MC 25 C, Cs weighted all:", out["monte_carlo_25C_only_Cs_mass_weighted_all"]["all"], out["monte_carlo_25C_only_Cs_mass_weighted_all"]["stirred"], out["monte_carlo_25C_only_Cs_mass_weighted_all"]["unstirred"])
    fb = out["flow_bracket_25C"]
    for rname, rows in fb["cases"].items():
        print("flow bracket", rname)
        for k, v in rows.items():
            print("   ", k, v)
    print("settling:", fb["settling"])
    print("wrote", os.path.basename(OUT))


if __name__ == "__main__":
    main()
