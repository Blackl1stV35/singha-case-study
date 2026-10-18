#!/usr/bin/env python3
"""Lime Soda Cube screen: CO2 partition on freezing, pour-over retention,
cube melt time, and drink dilution.

Working candidate: a sweetened lime soda (no sugar-free claim) reformatted from a
330 ml can into a frozen cube (Alternative Formats axis). Thailand domestic only.

Standard library only. Reproduce with:
    python lime_cube_screen.py
Writes lime_cube_screen_results.json beside this file and prints a summary.

Status tags used in the output:
    sourced  value read from a public URL listed in SOURCES
    derived  computed here from sourced and/or assumed inputs
    assumed  chosen for this screen; basis stated; not measured
No cost or price is computed. No team, group or internal data is used.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "lime_cube_screen_results.json")

# --------------------------------------------------------------- sources
SOURCES = {
    "lange_bunsen_table": {
        "url": "https://en.wikipedia.org/wiki/Carbon_dioxide_(data_page)",
        "content": "CO2 solubility in water at 101.3 kPa: Bunsen-type volumes and g CO2 per 100 mL water; "
                   "table cited to Lange's Handbook of Chemistry, 10th ed., p. 1100. Rows used: 0, 4, 5, 25 C.",
        "status": "sourced (read via WebFetch 2026-10-18; secondary page citing Lange)",
    },
    "sander_henry_compilation": {
        "url": "https://henrys-law.org/henry/casrn/124-38-9",
        "content": "Henry's law constant Hscp for CO2 at 298.15 K = 3.3e-4 mol/(m3 Pa); "
                   "d ln(Hscp)/d(1/T) = 2400 K (Sander 2006 and 2011; Wilhelm 1977 also 2400 K). "
                   "Table is flattened; value and slope pairing checked by order only.",
        "status": "sourced (read via WebFetch 2026-10-18; verify live table before publication)",
    },
    "fao_water_ice": {
        "url": "https://www.fao.org/4/T0713E/T0713E0c.htm",
        "content": "Latent heat of melting 80 kcal/kg; specific heat of water 1.0 kcal/(kg C); "
                   "ice 0.49 kcal/(kg C) at 0 C (unit inferred, no unit printed); ice density 0.92 kg/L at 0 C.",
        "status": "sourced (read via WebFetch 2026-10-18)",
    },
    "ifas_carbonation": {
        "url": "https://ask.ifas.ufl.edu/publication/FS379",
        "content": "Most soft drinks such as tonic water carbonated to 3-3.5 volumes of CO2; "
                   "colas 3.5-4 vol (Table 1); minimum detectable ~0.6 vol; absolute maximum recommended 8 vol.",
        "status": "sourced (read via WebFetch 2026-10-18)",
    },
    "singha_sparkling_lime_price": {
        "url": "https://www.kaohooninternational.com/?p=579263",
        "content": "Singha Sparkling Water Lime Flavour: 330 ml can, sugar-free and 0% calorie, "
                   "15 baht, all 7-Eleven branches nationwide. Article dated 17/03/2026. "
                   "Public shelf price for the can, not for a cube.",
        "status": "sourced (read via WebFetch 2026-10-18; trade press reprint of company announcement)",
    },
    "dspe_htc": {
        "url": "https://www.dspe.nl/knowledge/thermomechanics/chapter-1-basics/1-2-heat-transfer/convection/",
        "content": "Typical h: forced convection water laminar 500-1000 W/(m2 K), turbulent 2000-10000 W/(m2 K); "
                   "natural convection water not listed.",
        "status": "sourced (read via WebFetch 2026-10-18)",
    },
    "waterloo_htc_snippet": {
        "url": "https://www.mhtlab.uwaterloo.ca/courses/ece309_mechatronics/lectures/pdffiles/chapter6.pdf",
        "content": "Natural convection water 60-900 W/(m2 K) (search snippet only; PDF text not readable by WebFetch).",
        "status": "unverified (search snippet only)",
    },
}

# --------------------------------------------------------------- constants
R_GAS = 8.314462618                 # J/(mol K), exact SI value
P_STD_PA = 101325.0                 # Pa, 1 atm
T_STD_K = 273.15                    # K, 0 C
T298 = 298.15                       # K
M_CO2 = 44.01                       # g/mol
VM_STP_L = R_GAS * T_STD_K / P_STD_PA * 1000.0   # L/mol, ideal gas at 0 C and 1 atm (derived, ~22.414)
KH_CONV = 1000.0 / P_STD_PA         # mol/(m3 Pa) per (mol/L per atm), i.e. 1 M/atm = 0.0098692 mol/(m3 Pa)

C_WATER = 4.184                     # J/(g K)   FAO: 1.0 kcal/(kg C)           [sourced]
C_ICE = 2.05                        # J/(g K)   FAO: 0.49 kcal/(kg C) at 0 C   [sourced, unit inferred]
L_FUS = 334.7                       # J/g       FAO: 80 kcal/kg                [sourced, converted]
RHO_ICE = 0.92                      # g/cm3     FAO: 0.92 kg/L at 0 C          [sourced]

# Lange table (via SOURCES["lange_bunsen_table"]): T C -> (Bunsen volumes, g CO2 per 100 mL water)
LANGE_BUNSEN = {
    0: (1.713, 0.3346),
    4: (1.473, 0.2871),
    5: (1.424, 0.2774),
    25: (0.759, 0.1449),
}
HSCP_298 = 3.3e-4                   # mol/(m3 Pa)  [sourced, Sander compilation]
DLNH_DINVT = 2400.0                 # K            [sourced, Sander compilation]

# Case assumptions (all tagged 'assumed' in the output)
CAN_VOL_ML = 330.0
CAN_VOLS = 3.5                      # volumes CO2 per volume liquid, within 3-3.5 (most soft drinks) to 3.5-4 (colas) [sourced]
CAN_TEMP_C = 4.0
CUBE_G = 25.0                       # g per cube (assumed working cube size)
CUBE_T0_C = -18.0                   # C, freezer start (assumed)
SODA_G_MELT_CASE = 250.0            # g, soda in melt case (given by team computed task)
SODA_T0_C = 25.0                    # C (given by team computed task)
SODA_DENSITY_G_ML = 1.0             # assumed
H_BASE = 300.0                      # W/(m2 K) assumed; range 100-900 covers natural convection
H_SWEEP = (100.0, 300.0, 900.0)
DT_S = 0.01                         # s, explicit Euler step


# --------------------------------------------------------------- Henry / solubility
def mol_per_L_lange(t_c):
    """CO2 concentration in water at 1 atm CO2 (Lange), mol per litre of water."""
    _, g100 = LANGE_BUNSEN[t_c]
    return g100 * 10.0 / M_CO2


def hscp_van_hoff(t_c):
    """Compilation Hscp (mol/(m3 Pa)) at t_c, van 't Hoff with slope 2400 K."""
    t_k = t_c + T_STD_K
    return HSCP_298 * math.exp(DLNH_DINVT * (1.0 / t_k - 1.0 / T298))


def mol_per_L_compilation(t_c):
    return hscp_van_hoff(t_c) / KH_CONV


def bunsen_at(t_c):
    """Bunsen volumes at t_c, linear between tabulated Lange points (clamped at ends)."""
    pts = sorted((t, v[0]) for t, v in LANGE_BUNSEN.items())
    if t_c <= pts[0][0]:
        return pts[0][1]
    if t_c >= pts[-1][0]:
        return pts[-1][1]
    for (t1, v1), (t2, v2) in zip(pts, pts[1:]):
        if t1 <= t_c <= t2:
            return v1 + (v2 - v1) * (t_c - t1) / (t2 - t1)
    raise ValueError("unreachable")


def section_henry():
    rows = []
    for t in (0, 4, 25):
        vol, g100 = LANGE_BUNSEN[t]
        m_l = mol_per_L_lange(t)
        m_c = mol_per_L_compilation(t)
        rows.append({
            "t_C": t,
            "bunsen_volumes_per_volume": vol,
            "g_CO2_per_100mL_water_lange": g100,
            "g_CO2_per_L_at_1atm_lange": round(g100 * 10.0, 4),
            "M_per_atm_lange": round(m_l, 5),
            "Hscp_mol_per_m3_Pa_lange": round(m_l * KH_CONV, 7),
            "Hscp_mol_per_m3_Pa_compilation_vanthoff": round(hscp_van_hoff(t), 7),
            "M_per_atm_compilation_vanthoff": round(m_c, 5),
            "compilation_over_lange_ratio": round(m_c / m_l, 4),
            "status": "lange values sourced; compilation values derived from sourced Hscp and slope",
        })
    slope_lange = math.log(mol_per_L_lange(0) / mol_per_L_lange(25)) / (1.0 / 273.15 - 1.0 / 298.15)
    return {
        "rows": rows,
        "implied_dlnH_d_invT_from_lange_0_to_25C_K": round(slope_lange, 0),
        "reading": "Lange 0 C and 4 C values are used as primary. The compilation van 't Hoff with 2400 K "
                   "is about 6-8 percent lower at 0 and 4 C. The Lange-implied slope between 0 and 25 C is "
                   "about 2700 K, so the constant-slope form is an approximation.",
    }


# --------------------------------------------------------------- CO2 in the can
def section_can():
    v_stp_L = CAN_VOLS * CAN_VOL_ML / 1000.0
    mol = v_stp_L / VM_STP_L
    mass_g = mol * M_CO2
    p_lange = CAN_VOLS / bunsen_at(CAN_TEMP_C)
    p_comp = (CAN_VOLS / VM_STP_L) / mol_per_L_compilation(CAN_TEMP_C)
    return {
        "can_volume_ml": CAN_VOL_ML,
        "carbonation_volumes": CAN_VOLS,
        "temperature_C": CAN_TEMP_C,
        "co2_volume_STP_L": round(v_stp_L, 4),
        "co2_mol": round(mol, 5),
        "co2_mass_g": round(mass_g, 4),
        "co2_mass_per_25g_of_same_liquid_g": round(mass_g * CUBE_G / CAN_VOL_ML, 5),
        "headspace_CO2_partial_pressure_atm_abs_lange_linear": round(p_lange, 3),
        "headspace_CO2_partial_pressure_atm_abs_compilation": round(p_comp, 3),
        "headspace_CO2_partial_pressure_kPa_abs_lange_linear": round(p_lange * 101.325, 1),
        "saturation_CO2_at_1atm_g_per_L_lange_4C": round(LANGE_BUNSEN[4][1] * 10.0, 4),
        "status": "volumes sourced (IFAS); Lange values sourced; mass and pressure derived (ideal gas, linear Henry)",
    }


# --------------------------------------------------------------- freezing partition
def section_freeze(co2_mass_g):
    scenarios = [
        dict(id="base_premise", k_ice=0.0, f_pocket=0.0, pocket_retention=0.0,
             status="team premise: CO2 leaves the ice and is not recovered; no retained pockets"),
        dict(id="k_ice_1e-4", k_ice=1e-4, f_pocket=0.0, pocket_retention=0.0,
             status="assumed illustrative ice-to-liquid CO2 ratio; no sourced value found"),
        dict(id="k_ice_1e-3", k_ice=1e-3, f_pocket=0.0, pocket_retention=0.0,
             status="assumed illustrative ice-to-liquid CO2 ratio; no sourced value found"),
        dict(id="k_ice_1e-2", k_ice=1e-2, f_pocket=0.0, pocket_retention=0.0,
             status="assumed illustrative ice-to-liquid CO2 ratio; no sourced value found"),
        dict(id="pockets_2pct_half_retained", k_ice=0.0, f_pocket=0.02, pocket_retention=0.5,
             status="assumed unfrozen pocket fraction and retention; not measured"),
        dict(id="pockets_5pct_fully_retained", k_ice=0.0, f_pocket=0.05, pocket_retention=1.0,
             status="assumed upper bound for pocket retention; not measured"),
    ]
    out = []
    for s in scenarios:
        f_ice = 1.0 - s["f_pocket"]
        retained = min(1.0, s["k_ice"] * f_ice + s["f_pocket"] * s["pocket_retention"])
        lost = 1.0 - retained
        out.append({
            "id": s["id"],
            "k_ice_CO2_ice_to_liquid_ratio": s["k_ice"],
            "unfrozen_pocket_mass_fraction": s["f_pocket"],
            "pocket_CO2_retention_fraction": s["pocket_retention"],
            "retained_fraction": round(retained, 6),
            "lost_fraction": round(lost, 6),
            "co2_lost_g_per_330ml_batch": round(lost * co2_mass_g, 4),
            "co2_retained_g_per_25g_cube": round(retained * co2_mass_g * CUBE_G / CAN_VOL_ML, 6),
            "status": s["status"],
        })
    return {
        "model": "retained = k_ice * ice_mass_fraction + pocket_mass_fraction * pocket_retention; "
                 "concentration-ratio form, first order, no Scheil correction",
        "scenarios": out,
    }


# --------------------------------------------------------------- pour-over
def section_pour_over(counts=(1, 2, 3, 4), water_T=4.0, cube_T=CUBE_T0_C):
    co2_can_L = CAN_VOLS * CAN_VOL_ML / 1000.0
    rows = []
    for n in counts:
        cube_total = n * CUBE_G
        v_w = CAN_VOL_ML - cube_total                       # ml carbonated water, cube melt counted in total
        co2_L = CAN_VOLS * v_w / 1000.0
        retained_immediate = co2_L / co2_can_L
        mass_g = co2_L / VM_STP_L * M_CO2
        q_cool = v_w * SODA_DENSITY_G_ML * C_WATER * (water_T - 0.0)
        q_warm = cube_total * C_ICE * (0.0 - cube_T)
        q_left = q_cool - q_warm
        melt_need = cube_total * L_FUS
        if q_left >= melt_need:
            melted = cube_total
            t_f = (q_left - melt_need) / ((v_w * SODA_DENSITY_G_ML + cube_total) * C_WATER)
            residual_ice = 0.0
        elif q_left > 0.0:
            melted = q_left / L_FUS
            residual_ice = cube_total - melted
            t_f = 0.0
        else:
            raise ValueError("cube does not warm to 0 C in this pour-over case")
        liquid_g = v_w * SODA_DENSITY_G_ML + melted
        vols_after = co2_L * 1000.0 / liquid_g
        sat = bunsen_at(t_f)
        rows.append({
            "cubes": n,
            "cube_mass_g_total": cube_total,
            "carbonated_water_ml": v_w,
            "water_temperature_C": water_T,
            "co2_mass_g_from_water": round(mass_g, 4),
            "retained_fraction_of_can_co2_immediately_after_mix": round(retained_immediate, 4),
            "final_temperature_C_adiabatic": round(t_f, 2),
            "cube_mass_melted_g": round(melted, 2),
            "residual_ice_g": round(residual_ice, 2),
            "drink_liquid_g_after_melt": round(liquid_g, 2),
            "drink_CO2_volumes_after_melt": round(vols_after, 3),
            "saturation_CO2_volumes_at_final_T_1atm_linear_interp": round(sat, 3),
            "excess_over_1atm_saturation_volumes": round(vols_after - sat, 3),
            "flavour_solute_factor_vs_can_if_cube_carries_soda_solutes": round(n * CUBE_G / CAN_VOL_ML, 4),
            "co2_factor_vs_can_immediate": round(retained_immediate, 4),
            "status": "water and cube inputs assumed; CO2 from sourced volumes; energy balance derived; "
                      "cube CO2 taken as zero (team premise)",
        })
    return rows


# --------------------------------------------------------------- melt model
def melt_time(h, area_shrinks=True, t_liq0=SODA_T0_C, t_cube0=CUBE_T0_C,
              m_soda=SODA_G_MELT_CASE, m_cube=CUBE_G, dt=DT_S, t_max=3600.0):
    """Lumped model: liquid at one temperature, cube at one surface temperature.
    Liquid energy is tracked relative to 0 C; melt water enters at 0 C and carries zero
    relative enthalpy, so dE_L/dt = -Q and T_L = E_L / (m_L * c_w)."""
    side_cm = (m_cube / RHO_ICE) ** (1.0 / 3.0)
    a0 = 6.0 * side_cm ** 2 * 1e-4            # m2, cube surface area at start
    m_ice = m_cube
    m_melt = 0.0
    t_c = t_cube0
    e_l = m_soda * C_WATER * t_liq0           # J relative to 0 C
    t = 0.0
    t90 = None
    while m_ice > 1e-6 and t < t_max:
        m_l = m_soda + m_melt
        t_l = e_l / (m_l * C_WATER)
        area = a0 * (m_ice / m_cube) ** (2.0 / 3.0) if area_shrinks else a0
        q = h * area * (t_l - t_c) * dt       # J into cube during this step
        if t_c < 0.0:
            need = m_ice * C_ICE * (0.0 - t_c)
            if q < need:
                t_c += q / (m_ice * C_ICE)
                e_l -= q
            else:
                leftover = q - need
                t_c = 0.0
                dm = min(m_ice, leftover / L_FUS)
                m_ice -= dm
                m_melt += dm
                e_l -= q
                e_l += leftover - dm * L_FUS  # unabsorbed energy returns to liquid
        else:
            dm = min(m_ice, q / L_FUS)
            m_ice -= dm
            m_melt += dm
            e_l -= dm * L_FUS
        t += dt
        if t90 is None and m_ice <= 0.1 * m_cube:
            t90 = t
    m_l = m_soda + m_melt
    t_l = e_l / (m_l * C_WATER)
    t_f_analytic = (m_soda * C_WATER * t_liq0 - m_cube * C_ICE * (0.0 - t_cube0) - m_cube * L_FUS) / \
                   ((m_soda + m_cube) * C_WATER)
    return {
        "h_W_per_m2K": h,
        "area_shrinks_with_melt": area_shrinks,
        "cube_start_C": t_cube0,
        "melt_time_s": round(t, 2),
        "melt_time_min": round(t / 60.0, 2),
        "time_to_90pct_melt_s": round(t90, 2) if t90 is not None else None,
        "time_to_90pct_melt_min": round(t90 / 60.0, 2) if t90 is not None else None,
        "cube_surface_area_start_cm2": round(a0 * 1e4, 2),
        "final_liquid_temperature_C_ode": round(t_l, 3),
        "final_temperature_C_energy_balance": round(t_f_analytic, 3),
        "closure_difference_C": round(t_l - t_f_analytic, 4),
        "final_liquid_mass_g": round(m_l, 2),
        "status": "h assumed (range 100-900 W/(m2 K) bracketed by natural-convection water snippet and "
                  "dspe laminar-forced range); geometry, densities and heat capacities sourced or assumed",
    }


def section_melt():
    rows = [melt_time(h, area_shrinks=True) for h in H_SWEEP]
    rows.append(melt_time(H_BASE, area_shrinks=False))
    rows.append(melt_time(H_BASE, area_shrinks=True, t_cube0=0.0))
    return {
        "base_h_W_per_m2K": H_BASE,
        "geometry": "cube, full immersion assumed, side from 25 g at 0.92 g/cm3",
        "rows": rows,
    }


# --------------------------------------------------------------- dilution
def section_dilution():
    total = SODA_G_MELT_CASE + CUBE_G
    return {
        "soda_g": SODA_G_MELT_CASE,
        "cube_g": CUBE_G,
        "final_mass_g_after_full_melt": total,
        "water_dilution_percent": round(100.0 * CUBE_G / total, 2),
        "solute_factor_if_cube_carries_soda_solutes_uniformly": 1.0,
        "solute_factor_if_cube_is_pure_ice": round(SODA_G_MELT_CASE / total, 4),
        "cubes_per_330ml_of_liquid_at_25g": round(CAN_VOL_ML / CUBE_G, 2),
        "status": "derived from mass balance; which solute case applies is a freezing-mode question for the physical test",
    }


# --------------------------------------------------------------- assumption register
def assumption_register():
    return [
        {"id": "A1", "text": "Soda density 1.0 g/mL", "status": "assumed"},
        {"id": "A2", "text": "Soda specific heat equal to water (4.184 J/g K)", "status": "assumed"},
        {"id": "A3", "text": "Ideal-gas molar volume at 0 C, 1 atm (22.414 L/mol); CO2 molar mass 44.01 g/mol", "status": "derived"},
        {"id": "A4", "text": "Henry's law linear from 1 atm to the pressure needed for 3.5 volumes at 4 C", "status": "assumed"},
        {"id": "A5", "text": "CO2 partition ratio k_ice = 0 in base case (team premise; no sourced ice solubility number found)", "status": "assumed"},
        {"id": "A6", "text": "Unfrozen pocket fraction and pocket CO2 retention: 0 in base case; sensitivity values not sourced", "status": "assumed"},
        {"id": "A7", "text": "Cube size 25 g; 0.92 g/cm3 ice; cube geometry", "status": "assumed"},
        {"id": "A8", "text": "Cube start -18 C (freezer); sensitivity case 0 C", "status": "assumed"},
        {"id": "A9", "text": "Heat transfer coefficient h = 300 W/(m2 K) base; sweep 100 and 900", "status": "assumed"},
        {"id": "A10", "text": "Cube surface area scales as (mass)^(2/3) during melt; constant-area variant also reported", "status": "assumed"},
        {"id": "A11", "text": "Lumped liquid, adiabatic container, full immersion, no ambient heat gain", "status": "assumed"},
        {"id": "A12", "text": "Pour-over water at 4 C and 3.5 vol; total serving 330 ml; melt water counted in total volume", "status": "assumed"},
        {"id": "A13", "text": "Cube CO2 content zero for pour-over (team premise: CO2 lost on freezing)", "status": "assumed"},
        {"id": "A14", "text": "CO2 is not modelled during the melt step; degassing during mixing is not modelled", "status": "assumed"},
        {"id": "A15", "text": "Saturation at intermediate temperatures by linear interpolation between Lange points", "status": "assumed"},
        {"id": "A16", "text": "Melt step runs in a 250 ml soda at 25 C with a 25 g cube (team computed task)", "status": "given"},
        {"id": "A17", "text": "Heat of fusion 334.7 J/g; ice 2.05 J/g K; water 4.184 J/g K", "status": "sourced (FAO)"},
    ]


# --------------------------------------------------------------- main
def main():
    henry = section_henry()
    can = section_can()
    freeze = section_freeze(can["co2_mass_g"])
    pour = section_pour_over()
    melt = section_melt()
    dil = section_dilution()

    result = {
        "meta": {
            "screen": "lime_cube_screen.py",
            "scope": "Thailand domestic only; Singapore and Korea excluded",
            "product": "Sweetened lime soda, 330 ml can reformatted to a frozen cube (working name Lime Soda Cube)",
            "double_blind_note": "Public information only. No team or group data is used. Repo notes were treated as leads.",
            "cost_rule": "No cost computed. Only public price in the record: Singha Sparkling Water Lime, 15 baht, 330 ml can, "
                         "7-Eleven, dated 17/03/2026 (a can, not a cube). Cube cost: none.",
            "constants": {
                "R_GAS_J_per_mol_K": R_GAS,
                "P_std_Pa": P_STD_PA,
                "T_std_K": T_STD_K,
                "M_CO2_g_per_mol": M_CO2,
                "Vm_STP_L_per_mol": round(VM_STP_L, 4),
                "C_water_J_per_gK": C_WATER,
                "C_ice_J_per_gK": C_ICE,
                "L_fus_J_per_g": L_FUS,
                "rho_ice_g_per_cm3": RHO_ICE,
            },
        },
        "sources": SOURCES,
        "A_henry_and_solubility": henry,
        "B_can_co2": can,
        "C_freeze_partition": freeze,
        "D_pour_over": pour,
        "E_melt_time": melt,
        "F_dilution": dil,
        "assumptions": assumption_register(),
        "open_items": [
            "Ice-phase CO2 segregation coefficient at atmospheric pressure: no sourced number found (k_ice = 0 is a premise).",
            "Natural-convection h for a cube in still soda: only a search snippet (Waterloo 60-900) is available.",
            "Solubility in ice: Dye-3 ice-core work says earlier lab CO2-in-ice values were too high; the new value is not given in the read text.",
            "Pour-over at 4 C does not fully melt 2 cubes; the drink ends at 0 C with residual ice in the base case.",
            "CO2 at pour-over and open-glass equilibrium with air (about 0.04 percent CO2) is not sourced in this run.",
        ],
    }

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)

    # human-readable summary
    print("Lime Soda Cube screen")
    print("Henry / solubility (Lange primary):")
    for r in henry["rows"]:
        print("  %2d C  Bunsen %.3f  %.4f g/L  Hscp(lange) %.3e  Hscp(vH) %.3e  ratio comp/lange %.3f" % (
            r["t_C"], r["bunsen_volumes_per_volume"], r["g_CO2_per_L_at_1atm_lange"],
            r["Hscp_mol_per_m3_Pa_lange"], r["Hscp_mol_per_m3_Pa_compilation_vanthoff"],
            r["compilation_over_lange_ratio"]))
    print("  implied slope 0-25 C (Lange): %s K" % henry["implied_dlnH_d_invT_from_lange_0_to_25C_K"])
    print("Can (330 ml, 3.5 vol, 4 C): CO2 %.4f L STP = %.4f mol = %.3f g; headspace %.3f atm (Lange linear) / %.3f atm (vH)" % (
        can["co2_volume_STP_L"], can["co2_mol"], can["co2_mass_g"],
        can["headspace_CO2_partial_pressure_atm_abs_lange_linear"],
        can["headspace_CO2_partial_pressure_atm_abs_compilation"]))
    print("Freeze partition:")
    for s in freeze["scenarios"]:
        print("  %-30s retained %.6f  lost %.6f  lost g %.4f" % (
            s["id"], s["retained_fraction"], s["lost_fraction"], s["co2_lost_g_per_330ml_batch"]))
    print("Pour-over (water 4 C, 3.5 vol):")
    for p in pour:
        print("  %d cube(s): water %d ml, CO2 retained (immediate) %.4f, T_final %.2f C, melted %.2f g, residual ice %.2f g, drink %.3f vol, sat %.3f vol" % (
            p["cubes"], p["carbonated_water_ml"], p["retained_fraction_of_can_co2_immediately_after_mix"],
            p["final_temperature_C_adiabatic"], p["cube_mass_melted_g"], p["residual_ice_g"],
            p["drink_CO2_volumes_after_melt"], p["saturation_CO2_volumes_at_final_T_1atm_linear_interp"]))
    print("Melt time, 25 g cube in 250 ml soda at 25 C:")
    for m in melt["rows"]:
        print("  h=%g shrink=%s cube0=%g C: full %.1f s (%.2f min), 90%% %.1f s (%.2f min), T_final ode %.3f vs energy %.3f" % (
            m["h_W_per_m2K"], m["area_shrinks_with_melt"], m["cube_start_C"], m["melt_time_s"],
            m["melt_time_min"], m["time_to_90pct_melt_s"], m["time_to_90pct_melt_min"],
            m["final_liquid_temperature_C_ode"], m["final_temperature_C_energy_balance"]))
    print("Dilution: water %.2f %%, solute factor (pure-ice cube) %.4f, (uniform cube) %.1f" % (
        dil["water_dilution_percent"], dil["solute_factor_if_cube_is_pure_ice"],
        dil["solute_factor_if_cube_carries_soda_solutes_uniformly"]))
    print("Wrote %s" % OUT_PATH)


if __name__ == "__main__":
    main()
