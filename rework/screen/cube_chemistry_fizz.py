"""Fizz duration bounds for the Singha Lemon Soda Cube (T8 part c).

Surface loss by Henry's law and a liquid-side mass-transfer coefficient, then a nucleation check.
Standard library only. Run with: python -I cube_chemistry_fizz.py
Writes cube_chemistry_fizz_results.json next to this file.

Model
- Dissolved CO2 at serve: C0 = dose (volumes) x 44.01 / 22.414 g/L (molar basis, central). The density
  basis 1.977 g/L per volume is the basis that gives the earlier 96 minutes (sensitivity).
- Henry constant H(T) = 0.033 mol/(L bar) at 298.15 K with d ln H / d(1/T) = 2400 K (Sander 2023
  compilation, tier S, read through a fetch summary; 2300 K from Burkholder 2019 as the sensitivity).
  Partial pressure p = C / H.
- Surface-only loss in a well-mixed bulk: dC/dt = -(A/V) kL (C - Ceq). Time to threshold
  t = (V/(kL A)) ln((C0 - Ceq)/(Cthr - Ceq)); Ceq = H p_CO2(air).
- kL from (a) lake coefficients k600 (Cole and Caraco 1998; Cole et al. 2010; Xiao et al. 2014; tier S, abstracts)
  converted to CO2 at T with Sc^(-1/2) (ASSUMPTION of the convention); the lowest coefficient in the sources
  read is 0.65 cm/h (Xiao et al. 2014, a pond with floating chambers); it is NOT a bound; (b) penetration theory
  kL = 2 sqrt(D / (pi t_r)), with renewal time t_r (textbook method; t_r is an ASSUMPTION for a glass).
- Retention. Every time assumes a share (retention) of the 0.55 volume dose is still dissolved at serve. The
  tornado runs it from 0.4 to 1.0 (break-even 0.408). A coupled estimate gives the retention left at the end of
  dissolution from SURFACE loss only (an upper bound on retention: bubble losses at the cube and on the glass
  are not included).
- D(T) by Stokes-Einstein scaling from 1.92e-9 m2/s at 25 C (tier S).
- Nucleation check: (N1) pure-CO2 bubble criterion C_crit = H (P_amb + 2 sigma / r);
  (N2) air-equilibrated liquid, C_crit = H 2 sigma / r. Site radius 1 to 10 micrometre (ASSUMPTION;
  modelling range from Liger-Belair and Cilindre 2021). Champagne first-order constant 1.0e-3 per
  second, DERIVED from the 7.4 to 3 g/L in 15 min figure in Liger-Belair et al. 2012 (tier S, PROXY).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cube_chemistry_fizz_results.json")

MOLAR_VOL = 22.414           # L/mol at 0 C and 1 atm, CONSTANT
MW_CO2 = 44.01               # g/mol, CONSTANT
DENSITY_STP_G_L = 1.977      # g/L of CO2 at 0 C and 1 atm, CONSTANT (basis of the earlier 96 minutes)
P_AMB = 1.013                # bar, CONSTANT
P_CO2_AIR = 420e-6           # bar, ASSUMPTION (420 ppm)
THRESH_G_L = 0.44            # PROXY, tier S (abstract only): Puleo et al. 2021, mineral water detection threshold
THRESH_LOW, THRESH_HIGH = 0.33, 0.55   # ASSUMPTION: +/-25 percent (no sourced spread)
DOSE_VOL = 0.55              # design
RETENTION = 1.0              # ASSUMPTION: share of the dose still dissolved at serve (not measured)
VOL_L = 0.330                # design serve
GLASS_D_M = 0.065            # ASSUMPTION (range 55 to 75 mm)

H0_MOL_L_BAR = 0.033         # S, Sander 2023 compilation read through a fetch summary (3.3e-4 mol/(m3 Pa) at 298.15 K)
DLNH_K = 2400.0              # S, Sander 2011 and 2006, Weiss 1974 as listed in the compilation (Burkholder 2019: 2300)
T_REF = 298.15

# Water viscosity (mPa s) and density (g/cm3), S, Wikipedia water data page (re-read 2026-10-20; the 5 C row is printed:
# 1.5188 mPa s and 0.99996 g/cm3; an earlier version interpolated 1.531 for 5 C, +0.8 percent).
MU = {0.0: 1.7921, 5.0: 1.5188, 10.0: 1.3077, 15.0: 1.1404, 20.0: 1.0050,
      25.0: 0.8937, 30.0: 0.8007, 35.0: 0.7225}
RHO = {5.0: 0.99996, 20.0: 0.9982071, 25.0: 0.9970479, 30.0: 0.9956502}
D_CO2_25 = 1.92e-9           # m2/s, S, Wikipedia mass diffusivity (1.92e-5 cm2/s)
# Zeebe 2011 (Geochim. Cosmochim. Acta 75, 2483, Table 2; P, molecular dynamics fit): D = D0 [(T/Ti) - 1]^c
ZEEBE_CO2 = (14.6836e-9, 217.2056, 1.9970)
D_CO2_ZEEBE_25 = ZEEBE_CO2[0] * (298.15 / ZEEBE_CO2[1] - 1.0) ** ZEEBE_CO2[2]   # about 2.04e-9, sensitivity only
SIGMA_WATER = {20.0: 0.07274, 25.0: 0.07198}     # N/m, S, Wikipedia water data page
SIGMA_BEV = 0.047            # N/m, beverage central (champagne 47, lager 43 mN/m; S, Liger-Belair and Cilindre 2021)
SITE_R_UM = (1.0, 10.0)      # ASSUMPTION
K600_CM_H = {"lake_low": 1.5, "lake_central": 2.65, "lake_high": 3.1}   # S, Cole and Caraco 1998; Cole et al. 2010
K600_LOWEST_READ_CM_H = 0.65  # S (abstract), Xiao et al. 2014, Tellus B 66, 23795: CO2 k600 at one pond site in autumn, floating chambers (3.2 text gives 0.72)
CHAMP_K_APP = math.log(7.4 / 3.0) / 900.0   # 1/s, DERIVED from the PROXY figure


def mu_at(t_c):
    if t_c in MU:
        return MU[t_c]
    keys = sorted(MU)
    for lo, hi in zip(keys, keys[1:]):
        if lo <= t_c <= hi:
            f = (t_c - lo) / (hi - lo)
            return math.exp((1 - f) * math.log(MU[lo]) + f * math.log(MU[hi]))
    raise ValueError("temperature outside the table")


def rho_at(t_c):
    return RHO.get(t_c, 0.9980)


def diff_co2(t_c):
    """Stokes-Einstein scaling of D from 25 C (tier S form)."""
    T = t_c + 273.15
    return D_CO2_25 * (T / 298.15) * (MU[25.0] / mu_at(t_c))


def sc_co2(t_c):
    nu = mu_at(t_c) * 1e-3 / (rho_at(t_c) * 1000.0)
    return nu / diff_co2(t_c)


def henry(t_c, dlnh=DLNH_K, h0=H0_MOL_L_BAR):
    """Henry constant in mol/(L bar)."""
    T = t_c + 273.15
    return h0 * math.exp(dlnh * (1.0 / T - 1.0 / T_REF))


def henry_g(t_c, dlnh=DLNH_K):
    return henry(t_c, dlnh) * MW_CO2


def kl_penetration(t_c, t_r_s):
    return 2.0 * math.sqrt(diff_co2(t_c) / (math.pi * t_r_s))


def kl_lake(t_c, k600_cm_h):
    """k600 (cm/h) converted to CO2 at t_c with Sc^(-1/2) (ASSUMPTION of the convention), in m/s."""
    k600 = k600_cm_h / 100.0 / 3600.0
    return k600 * (sc_co2(t_c) / 600.0) ** -0.5


def a_over_v(glass_d=GLASS_D_M):
    return (math.pi * (glass_d / 2.0) ** 2) / (VOL_L * 1e-3)   # 1/m


def c0_g_L(dose=DOSE_VOL, basis="molar", retention=RETENTION):
    if basis == "molar":
        return dose * retention / MOLAR_VOL * MW_CO2
    return dose * retention * DENSITY_STP_G_L


def ceq_g_L(t_c, dlnh=DLNH_K):
    return henry_g(t_c, dlnh) * P_CO2_AIR


def t_surface_min(t_c, kl_m_s, c0, thr=THRESH_G_L, glass_d=GLASS_D_M, dlnh=DLNH_K):
    if c0 <= thr:
        return 0.0
    tau = 1.0 / (kl_m_s * a_over_v(glass_d))          # s
    ceq = ceq_g_L(t_c, dlnh)
    return tau * math.log((c0 - ceq) / (thr - ceq)) / 60.0


def nucleation(t_c, c0, sigma=SIGMA_BEV):
    H = henry_g(t_c)                                   # g/(L bar)
    out = {
        "H_g_L_bar": round(H, 4),
        "C0_g_L": round(c0, 4),
        "p_CO2_bar_at_C0": round(c0 / H, 4),
        "N1_flat_limit_g_L": round(H * P_AMB, 4),
        "N1_Ccrit_10um_g_L": round(H * (P_AMB + 2 * sigma / 10e-6 / 1e5), 4),
        "N1_Ccrit_1um_g_L": round(H * (P_AMB + 2 * sigma / 1e-6 / 1e5), 4),
        "N1_nucleates_at_C0": bool(c0 > H * P_AMB),
    }
    p = c0 / H
    rc_um = 2 * sigma / (p * 1e5) * 1e6
    out["N2_r_c_um_at_C0"] = round(rc_um, 3)
    out["N2_active_sites_in_1_to_10_um"] = bool(rc_um <= SITE_R_UM[1])
    out["N2_floor_10um_site_g_L"] = round(H * 2 * sigma / 10e-6 / 1e5, 4)
    out["N2_floor_1um_site_g_L"] = round(H * 2 * sigma / 1e-6 / 1e5, 4)
    return out


def main():
    res = {
        "task": "T8 part c, surface-only fizz bound and nucleation check (rebuilds the 96 minutes)",
        "date": "2026-10-20",
        "inputs": {
            "dose_volumes": {"value": DOSE_VOL, "tier": "design (ASSUMPTION of the deck)"},
            "retention_at_serve": {"value": RETENTION, "tier": "ASSUMPTION (not measured)"},
            "C0_molar_basis_g_L": {"value": round(c0_g_L(), 4), "tier": "CONSTANT (22.414 L/mol; 44.01 g/mol)"},
            "C0_density_basis_g_L": {"value": round(c0_g_L(basis="density"), 4), "tier": "CONSTANT (1.977 g/L per volume; basis of the earlier 96 minutes)"},
            "threshold_g_L": {"value": THRESH_G_L, "tier": "PROXY, tier S (Puleo et al. 2021, abstract only, mineral water detection threshold); 0.33 to 0.55 ASSUMPTION"},
            "H_CO2_298K_mol_L_bar": {"value": H0_MOL_L_BAR, "tier": "S, Sander 2023 compilation read through a fetch summary (3.3e-4 mol/(m3 Pa))"},
            "dlnH_dinvT_K": {"value": DLNH_K, "tier": "S (2400 K: Sander 2011, 2006, Weiss 1974, as listed in the compilation); Burkholder 2019 2300 K as sensitivity"},
            "D_CO2_25C_m2_s": {"value": D_CO2_25, "tier": "S, Wikipedia mass diffusivity (1.92e-5 cm2/s)"},
            "water_viscosity_mPa_s": {"value": {str(k): round(v, 4) for k, v in MU.items()}, "tier": "S, Wikipedia water data page (re-read 2026-10-20, the 5 C row is printed)"},
            "k600_lake_cm_h": {"value": K600_CM_H, "tier": "S, Cole and Caraco 1998 (2.65); Cole et al. 2010 (1.5 to 3.1)"},
            "k600_lowest_in_sources_read_cm_h": {"value": K600_LOWEST_READ_CM_H, "tier": "S, Xiao et al. 2014 abstract (one pond site in autumn, floating chambers; text of section 3.2 gives 0.72); the lowest in the sources read, not a bound"},
            "glass_diameter_mm": {"value": GLASS_D_M * 1000, "tier": "ASSUMPTION (55 to 75 mm)"},
            "A_over_V_per_m": {"value": round(a_over_v(), 3), "tier": "DERIVED from the 65 mm glass and 330 mL"},
            "sigma_beverage_N_m": {"value": SIGMA_BEV, "tier": "S (Liger-Belair and Cilindre 2021: lager 43, champagne 47 mN/m); PROXY"},
            "sigma_water_N_m": {"value": SIGMA_WATER, "tier": "S, Wikipedia water data page (the re-read prints 72.75 and 71.97 mN/m at 20 and 25 C; the 0.01 difference is immaterial and used only in a nucleation check)"},
            "site_radius_um": {"value": list(SITE_R_UM), "tier": "ASSUMPTION (S modelling range)"},
            "champagne_k_app_per_s": {"value": round(CHAMP_K_APP, 6), "tier": "DERIVED from the PROXY figure (7.4 to 3 g/L in 15 min)"},
            "P_CO2_air_bar": {"value": P_CO2_AIR, "tier": "ASSUMPTION (420 ppm)"},
        },
    }

    # 1. Henry check and saturation at 1 atm
    sat = {}
    for t_c in (5.0, 20.0, 25.0, 30.0, 35.0):
        h = henry(t_c)
        sat[str(int(t_c))] = {
            "H_mol_L_bar": round(h, 5),
            "saturation_1atm_volumes_from_Sander": round(h * P_AMB * MOLAR_VOL, 3),
            "dose_p_CO2_bar": round(c0_g_L() / henry_g(t_c), 3),
            "dose_as_fraction_of_1atm_saturation": round(DOSE_VOL / (h * P_AMB * MOLAR_VOL), 3),
            "D_CO2_m2_s": diff_co2(t_c),
            "Sc": round(sc_co2(t_c), 1),
        }
    sat["note"] = ("Lange-based table in the earlier model gives 0.878 volumes at 20 C and 0.655 at 30 C (S); "
                   "the Sander-based values here agree to about 2 percent.")
    res["henry_and_saturation"] = sat

    # 2. Reconciliation of the 96 minutes
    c_den = c0_g_L(basis="density")
    kl_10 = kl_penetration(25.0, 10.0)
    tau_min = 1.0 / (kl_10 * a_over_v()) / 60.0
    res["reconciliation_96_min"] = {
        "earlier_basis_25C_10s": {
            "C0_g_L_density_basis": round(c_den, 4),
            "D_m2_s": D_CO2_25,
            "renewal_s": 10.0,
            "kL_m_s": kl_10,
            "kL_cm_h": round(kl_10 * 100 * 3600, 2),
            "tau_min": round(tau_min, 2),
            "t_min": round(tau_min * math.log((c_den - ceq_g_L(25.0)) / (THRESH_G_L - ceq_g_L(25.0))), 2),
            "statement": "Reproduces the earlier 96 minutes: tau %.1f min x ln(%.4f / 0.44) = %.1f min (25 C, density basis, 10 s renewal, 65 mm glass)." % (
                tau_min, c_den, tau_min * math.log((c_den - ceq_g_L(25.0)) / (THRESH_G_L - ceq_g_L(25.0)))),
        },
        "same_10s_renewal_20C_molar_basis": {
            "kL_cm_h": round(kl_penetration(20.0, 10.0) * 100 * 3600, 2),
            "t_min": round(t_surface_min(20.0, kl_penetration(20.0, 10.0), c0_g_L()), 2),
        },
        "calm_lake_central_20C_molar_basis": {
            "kL_cm_h": round(kl_lake(20.0, K600_CM_H["lake_central"]) * 100 * 3600, 3),
            "t_min": round(t_surface_min(20.0, kl_lake(20.0, K600_CM_H["lake_central"]), c0_g_L()), 1),
        },
    }

    # 3. Surface-only times by regime and temperature (molar basis, 65 mm glass)
    regimes = {
        "lake_lowest_read_0.65cm_h": lambda t: kl_lake(t, K600_LOWEST_READ_CM_H),
        "lake_low_1.5cm_h": lambda t: kl_lake(t, K600_CM_H["lake_low"]),
        "lake_central_2.65cm_h": lambda t: kl_lake(t, K600_CM_H["lake_central"]),
        "lake_high_3.1cm_h": lambda t: kl_lake(t, K600_CM_H["lake_high"]),
        "penetration_600s_quiescent": lambda t: kl_penetration(t, 600.0),
        "penetration_30s": lambda t: kl_penetration(t, 30.0),
        "penetration_10s_earlier_basis": lambda t: kl_penetration(t, 10.0),
        "penetration_3s_fast": lambda t: kl_penetration(t, 3.0),
    }
    times = {}
    for name, fn in regimes.items():
        row = {}
        for t_c in (5.0, 20.0, 30.0):
            kl = fn(t_c)
            row[str(int(t_c))] = {
                "kL_cm_h": round(kl * 100 * 3600, 3),
                "t_surface_min": round(t_surface_min(t_c, kl, c0_g_L()), 1),
            }
        times[name] = row
    res["surface_only_times_molar_basis"] = times

    still_hi_20 = times["lake_high_3.1cm_h"]["20"]["t_surface_min"]
    still_lo_20 = times["lake_low_1.5cm_h"]["20"]["t_surface_min"]
    lowest_read_20 = times["lake_lowest_read_0.65cm_h"]["20"]["t_surface_min"]
    quiescent_20 = times["penetration_600s_quiescent"]["20"]["t_surface_min"]
    stirred_20 = times["penetration_10s_earlier_basis"]["20"]["t_surface_min"]
    central_lake_20 = times["lake_central_2.65cm_h"]["20"]["t_surface_min"]
    res["bounds_20C_surface_only_min"] = {
        "still_lake_range_min": [still_hi_20, still_lo_20],
        "central_still_lake_min": central_lake_20,
        "quiescent_penetration_600s_renewal_min_theory_only": quiescent_20,
        "lake_low_1.5_cm_h_min": still_lo_20,
        "lowest_coefficient_in_sources_read_0.65cm_h_min": lowest_read_20,
        "stirred_10s_renewal_min": stirred_20,
        "statement": ("Surface-only time at 20 C for the lake coefficients of Cole and Caraco 1998 and Cole et al. 2010 (k600 1.5 to 3.1 cm/h) is %.0f to %.0f minutes; "
                      "the lowest coefficient in the sources read (0.65 cm/h, Xiao et al. 2014, one pond site) gives %.0f minutes and a perfectly quiescent surface "
                      "(600 s renewal, theory only) %.0f minutes. The 96 minute value needs a 10 s surface renewal (5.3 cm/h at 20 C), a stirred surface, and is not an upper bound. "
                      "No sourced upper bound exists. All times assume the full 0.55 volume dose is still dissolved at serve (retention 1.0, not measured)."
                      % (still_hi_20, still_lo_20, lowest_read_20, quiescent_20)),
    }

    # 4. Nucleation check
    nuc = {}
    for t_c in (5.0, 20.0, 30.0):
        nuc[str(int(t_c))] = nucleation(t_c, c0_g_L())
    nuc["sigma_water_20C_check"] = nucleation(20.0, c0_g_L(), sigma=SIGMA_WATER[20.0])
    res["nucleation_check"] = nuc

    # Validation of the pure-CO2 critical radius rule (N1) against the beer and champagne figures
    def crit_r_um(h_g, c_g, sigma):
        dp = c_g / h_g - P_AMB
        return round(2 * sigma / (dp * 1e5) * 1e6, 3) if dp > 0 else None
    beer_calc = crit_r_um(2.4, 5.2, 0.043)
    beer_calc_sander = crit_r_um(henry_g(6.0), 5.2, 0.043)
    champ_calc = crit_r_um(henry_g(10.0), 8.0, 0.047)
    res["validation_N1_critical_radius"] = {
        "beer_6C_5.2gL_paper_H_2.4_um": beer_calc,
        "beer_6C_5.2gL_Sander_H_um": beer_calc_sander,
        "champagne_10C_8gL_Sander_H_um": champ_calc,
        "paper_values_um": {"beer_6C": 0.7, "champagne_10C": 0.3},
        "deviation_percent": {
            "beer_paper_H": round(100.0 * (beer_calc - 0.7) / 0.7, 1),
            "beer_Sander_H": round(100.0 * (beer_calc_sander - 0.7) / 0.7, 1),
            "champagne_Sander_H": round(100.0 * (champ_calc - 0.3) / 0.3, 1),
        },
        "source": "Liger-Belair and Cilindre 2021 (ACS Omega) abstract (S, saved in T8 raw folder)",
        "statement": ("The pure-CO2 rule gives %.3f against 0.7 micrometre for beer (%+.0f percent, the paper's Henry constant) and %.3f against 0.3 for champagne "
                      "(%+.0f percent, Sander constant; the champagne constant used in the paper was not read). The published radii are quoted to one figure, "
                      "so agreement is to about 20 percent at best. It is used as the literature's criterion, not as a validated predictor."
                      % (beer_calc, 100.0 * (beer_calc - 0.7) / 0.7, champ_calc, 100.0 * (champ_calc - 0.3) / 0.3)),
    }
    lb_min = math.log(c0_g_L() / THRESH_G_L) / CHAMP_K_APP / 60.0
    res["nucleation_bound"] = {
        "champagne_proxy_k_app_per_s": round(CHAMP_K_APP, 6),
        "floor_min_champagne_proxy": round(lb_min, 1),
        "status": "PROXY floor only: the constant was measured for a supersaturated champagne flute at about 4.5 bar; a floor at 0.6 bar driving force is not sourced",
        "central_not_stated": "Active-site density and bubble rate at 1.08 g/L are not sourced",
    }

    # 5. One-at-a-time tornado at 20 C
    def run(kl_fn, glass=GLASS_D_M, dose=DOSE_VOL, ret=RETENTION, thr=THRESH_G_L, t_c=20.0, dlnh=DLNH_K, basis="molar"):
        c0 = c0_g_L(dose=dose, basis=basis, retention=ret)
        return t_surface_min(t_c, kl_fn(t_c), c0, thr=thr, glass_d=glass, dlnh=dlnh)

    lake_c = lambda t: kl_lake(t, K600_CM_H["lake_central"])
    lake_lo = lambda t: kl_lake(t, K600_CM_H["lake_low"])
    lake_hi = lambda t: kl_lake(t, K600_CM_H["lake_high"])
    lake_lowest = lambda t: kl_lake(t, K600_LOWEST_READ_CM_H)
    stir_c = lambda t: kl_penetration(t, 10.0)
    stir_fast = lambda t: kl_penetration(t, 3.0)
    stir_slow = lambda t: kl_penetration(t, 30.0)

    def rows_for(base_fn):
        global D_CO2_25
        rows = []
        cases = [
            ("kL source range", dict(kl_fn=None)),
            ("kL lowest coefficient in the sources read (0.65 cm/h; lake base only)", dict(kl_fn=None)),
            ("glass diameter 55 to 75 mm", dict(glass=(0.055, 0.075))),
            ("retention at serve 0.4 to 1.0 (break-even 0.408)", dict(ret=(0.4, 1.0))),
            ("threshold 0.33 to 0.55 g/L", dict(thr=(THRESH_HIGH, THRESH_LOW))),
            ("H temperature term 2300 to 2400 K", dict(dlnh=(2300.0, 2400.0))),
            ("temperature 5 to 30 C", dict(t_c=(5.0, 30.0))),
            ("dose basis density 1.0874 vs molar 1.0800 g/L", dict(basis=("density", "molar"))),
            ("D(CO2) 25 C: 1.92e-9 (S) to 2.04e-9 (Zeebe MD fit, P)", dict(dco2=(D_CO2_25, D_CO2_ZEEBE_25))),
        ]
        for name, spec in cases:
            if name == "kL source range":
                if base_fn is stir_c:
                    lo_v = run(stir_slow)
                    hi_v = run(stir_fast)
                else:
                    lo_v = run(lake_hi)
                    hi_v = run(lake_lo)
            elif name.startswith("kL lowest"):
                if base_fn is stir_c:
                    continue
                lo_v = run(base_fn)
                hi_v = run(lake_lowest)
            elif name.startswith("glass"):
                lo_v = run(base_fn, glass=0.075)
                hi_v = run(base_fn, glass=0.055)
            elif name.startswith("retention"):
                lo_v = run(base_fn, ret=0.4)
                hi_v = run(base_fn, ret=1.0)
            elif name.startswith("threshold"):
                lo_v = run(base_fn, thr=THRESH_HIGH)
                hi_v = run(base_fn, thr=THRESH_LOW)
            elif name.startswith("H temperature"):
                lo_v = run(base_fn, dlnh=2300.0)
                hi_v = run(base_fn, dlnh=2400.0)
            elif name.startswith("temperature"):
                lo_v = run(base_fn, t_c=30.0)
                hi_v = run(base_fn, t_c=5.0)
            elif name.startswith("D(CO2)"):
                keep_d = D_CO2_25
                try:
                    v_a = run(base_fn)
                    D_CO2_25 = D_CO2_ZEEBE_25
                    v_b = run(base_fn)
                finally:
                    D_CO2_25 = keep_d
                lo_v, hi_v = v_b, v_a
            else:
                lo_v = run(base_fn, basis="molar")
                hi_v = run(base_fn, basis="density")
            rows.append({"input": name, "low_min": round(min(lo_v, hi_v), 1), "high_min": round(max(lo_v, hi_v), 1),
                         "swing_min": round(abs(hi_v - lo_v), 1)})
        return rows

    base_lake = run(lake_c)
    base_stir = run(stir_c)
    res["tornado_still_lake_central_20C"] = {"base_min": round(base_lake, 1), "rows": rows_for(lake_c)}
    res["tornado_stirred_10s_20C"] = {"base_min": round(base_stir, 1), "rows": rows_for(stir_c)}

    # 6. Retention at serve: table, break-even and the retention left after dissolution by surface loss only
    breakeven = THRESH_G_L / c0_g_L()
    ret_rows = {}
    for ret in (1.0, 0.8, 0.6, 0.5, 0.45, 0.41, 0.4):
        ret_rows[str(ret)] = {
            "C0_g_L": round(c0_g_L(retention=ret), 4),
            "still_lake_central_min": round(run(lake_c, ret=ret), 1),
            "stirred_10s_min": round(run(stir_c, ret=ret), 1),
            "lowest_coefficient_read_0.65_min": round(run(lake_lowest, ret=ret), 1),
        }

    def ret_for_time(target_min, kl_fn):
        lo, hi = 0.3, 1.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if run(kl_fn, ret=mid) < target_min:
                lo = mid
            else:
                hi = mid
        return round(0.5 * (lo + hi), 3)

    res["retention_at_serve"] = {
        "break_even_retention": round(breakeven, 4),
        "break_even_note": "Below this share of the 0.55 volume dose still dissolved at serve, the drink is already below 0.44 g/L (time zero).",
        "times_20C_by_retention_min": ret_rows,
        "retention_needed_for_still_lake_central_time_of_150_min": ret_for_time(150.0, lake_c),
        "retention_needed_for_stirred_10s_time_of_60_min": ret_for_time(60.0, stir_c),
    }

    def tau_s(kl_fn):
        return 1.0 / (kl_fn(20.0) * a_over_v())

    with open(os.path.join(HERE, "cube_chemistry_dissolution_results.json"), encoding="utf-8") as fh_d:
        dres = json.load(fh_d)
    t_d_cases = {
        "stirred central (25 C)": dres["bounds_25C_s"]["central_stirred"],
        "unstirred central (25 C)": dres["bounds_25C_s"]["central_unstirred"],
        "stirred 95th percentile of assumed ranges (25 C)": dres["monte_carlo_25C_only"]["stirred"]["p95_s"],
        "unstirred 95th percentile of assumed ranges (25 C)": dres["monte_carlo_25C_only"]["unstirred"]["p95_s"],
    }
    regs = {"stirred_10s_renewal": stir_c, "calm_lake_central": lake_c, "lowest_coefficient_read_0.65": lake_lowest}
    coupled = {}
    for dname, t_d in t_d_cases.items():
        row = {"t_dissolve_s": t_d}
        for rname, fn in regs.items():
            tau = tau_s(fn)
            r_start = math.exp(-t_d / tau)
            r_unif = (tau / t_d) * (1.0 - math.exp(-t_d / tau))
            row[rname] = {
                "tau_min": round(tau / 60.0, 1),
                "retention_gas_all_formed_at_start": round(r_start, 3),
                "retention_gas_formed_uniformly": round(r_unif, 3),
                "time_after_dissolution_ends_min_worst": round(run(fn, ret=r_start), 1),
                "time_after_dissolution_ends_min_uniform": round(run(fn, ret=r_unif), 1),
            }
        coupled[dname] = row
    res["retention_after_dissolution_surface_loss_only"] = {
        "basis": ("CO2 formed during the stage 2 dissolution time and lost through the free surface only at the first-order rate 1/tau (20 C, "
                  "65 mm glass); two bracketing generation profiles (all formed at the start, or uniformly over the dissolution time). "
                  "Ceq (about 0.001 g/L) is neglected. This is an UPPER bound on retention: bubble formation at the cube, in the "
                  "plume and on the glass is not included and is not bounded by any source read."),
        "dissolution_times_from": "cube_chemistry_dissolution_results.json (25 C; the fizz model is at 20 C, a stated mismatch of a few percent)",
        "cases": coupled,
    }

    res["robustness"] = {
        "still_lake_min_min": round(still_hi_20, 1),
        "still_lake_max_min": round(still_lo_20, 1),
        "ninety_six_min_is_below_still_lake_range": bool(still_hi_20 > 96.0),
        "still_lake_time_above_150_min_needs_retention_at_least": res["retention_at_serve"]["retention_needed_for_still_lake_central_time_of_150_min"],
        "still_lake_central_time_at_retention_0.8_min": ret_rows["0.8"]["still_lake_central_min"],
        "still_lake_central_time_at_retention_0.5_min": ret_rows["0.5"]["still_lake_central_min"],
        "still_lake_central_time_at_retention_0.45_min": ret_rows["0.45"]["still_lake_central_min"],
        "break_even_retention": round(breakeven, 4),
        "pure_CO2_nucleation_at_0.55_volumes_any_T_5_to_30C": any(nuc[k]["N1_nucleates_at_C0"] for k in ("5", "20", "30")),
        "air_equilibrated_sites_active_at_C0_20C": nuc["20"]["N2_active_sites_in_1_to_10_um"],
        "air_equilibrated_10um_floor_below_threshold_20C": bool(nuc["20"]["N2_floor_10um_site_g_L"] < THRESH_G_L),
        "statement": ("The surface-only still-glass time stays above 150 minutes at 20 C only while the retention at serve is at or above about %.2f; "
                      "retention 0.8 gives %.0f minutes, 0.5 gives %.0f, 0.45 gives %.0f and below %.2f the drink is under the threshold at serve. "
                      "Retention is the dominant unmeasured input."
                      % (res["retention_at_serve"]["retention_needed_for_still_lake_central_time_of_150_min"],
                         ret_rows["0.8"]["still_lake_central_min"], ret_rows["0.5"]["still_lake_central_min"],
                         ret_rows["0.45"]["still_lake_central_min"], breakeven)),
    }
    res["stage3_summary_20C"] = {
        "surface_only_stirred_10s_min": stirred_20,
        "surface_only_calm_lake_central_min": central_lake_20,
        "surface_only_range_h": [round(stirred_20 / 60.0, 1), round(central_lake_20 / 60.0, 1)],
        "proxy_floor_with_bubble_loss_min": res["nucleation_bound"]["floor_min_champagne_proxy"],
        "break_even_retention": round(breakeven, 3),
        "basis": ("Surface-only range runs from an ASSUMED 10 s surface renewal (stirred glass) to a lake coefficient (calm lake central, "
                  "Cole and Caraco 1998), neither measured in a drinking glass. The floor is a champagne PROXY. Full dose dissolved at serve is assumed."),
    }
    res["limits"] = [
        "No fizz measurement. The 0.44 g/L threshold is a mineral-water detection threshold (PROXY); a sugared, acidic drink may differ.",
        "Surface coefficients are lake values (S). No source gives a free-surface coefficient for a drinking glass.",
        "Nucleation depends on whether the liquid carries dissolved air (N2) or only CO2 (N1). Neither the air content nor the active-site density is sourced.",
        "The champagne constant is a PROXY from a supersaturated flute (about 4.5 bar); it is a floor only.",
        "Retention at serve is not measured. The times in the surface tables assume the full 0.55 volume dose is dissolved at serve; the tornado runs retention from 0.4 to 1.0 (break-even 0.408, below which there is no time above the threshold at all).",
        "The retention left after dissolution from surface loss alone is high (see retention_after_dissolution_surface_loss_only) but it is an upper bound: bubble formation at the cube and on the glass is not bounded by any source read.",
        "The lowest coefficient in the sources read (0.65 cm/h, one pond site, floating chambers, abstract) is not a bound; other sources were not searched exhaustively.",
        "The surface-loss model assumes a well-mixed bulk; a quiescent column loses CO2 more slowly at first, so a still glass can exceed the lake-based times (no sourced upper bound).",
        "C0 is 1.080 g/L for exactly 0.55 volumes (22.414 L/mol) and 1.079 g/L from 0.81 g of potassium bicarbonate (0.5495 volumes); the difference is rounding.",
    ]

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)

    print("96 check t_min:", res["reconciliation_96_min"]["earlier_basis_25C_10s"]["t_min"], "tau:", res["reconciliation_96_min"]["earlier_basis_25C_10s"]["tau_min"])
    print("20 C surface-only min (still hi/lo):", still_hi_20, still_lo_20, "quiescent:", quiescent_20, "stirred 10 s:", times["penetration_10s_earlier_basis"]["20"]["t_surface_min"])
    print("nucleation 20 C:", {k: nuc["20"][k] for k in ("N1_flat_limit_g_L", "N1_nucleates_at_C0", "N2_r_c_um_at_C0", "N2_floor_10um_site_g_L")})
    print("champagne floor min:", res["nucleation_bound"]["floor_min_champagne_proxy"])
    print("tornado still base:", res["tornado_still_lake_central_20C"]["base_min"], "stirred base:", res["tornado_stirred_10s_20C"]["base_min"])
    print("robustness:", res["robustness"])
    print("retention table:", res["retention_at_serve"])
    print("coupled:", json.dumps(res["retention_after_dissolution_surface_loss_only"]["cases"], indent=None)[:2400])
    print("stage3:", res["stage3_summary_20C"])
    for k in ("tornado_still_lake_central_20C", "tornado_stirred_10s_20C"):
        print(k, res[k]["base_min"])
        for r in res[k]["rows"]:
            print("   ", r)
    print("wrote", os.path.basename(OUT))


if __name__ == "__main__":
    main()
