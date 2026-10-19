"""Desk model of the sodium-free lime cube (component 1, rework/62). Desk only: no bench test.

Covers: CO2 solubility at the serve temperature, retention at serve, first-order degassing
(mass transfer only, so an upper bound on how long the fizz lasts), the citric acid balance to a
target pH by charge balance, potassium per serve, a sucralose dose by sweetness equivalence, gas
from a storage reaction in a sealed pouch, ice dilution and melt, and a Monte Carlo stress test.
Standard library only. Run with: python -I formulation_desk_model.py
"""
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "formulation_desk_model_results.json"

# ---- constants: value and status. Page text behind SOURCED values is in rework/raw/ ----
MOLAR_VOLUME_STP_L = 22.414            # L/mol, 0 C and 1 atm. CONSTANT.
R_L_ATM = 0.082057                     # L atm/(mol K). CONSTANT.
K_MW = 39.098                          # CONSTANT.
KHCO3_MW = 100.115                     # CONSTANT.
CITRIC_MW = 192.124                    # CONSTANT.
DOSE_BASIS_L = 0.330                   # the dose is defined per 330 mL. CONSTANT of the design.

# CO2 solubility, volumes at STP per volume of water, 1 atm pure CO2.
# Anchors: Lange-attributed table via the Wikipedia data page and BioNumbers (S). 30 and 35 C from the same table (S).
# NIST Ostwald coefficients converted to STP give 0.676 at 30 C and 0.600 at 35 C (P), a cross-check.
ALPHA_ANCHOR = {0: 1.713, 4: 1.473, 5: 1.424, 10: 1.194, 20: 0.878, 25: 0.759, 30: 0.655, 35: 0.592}
ALPHA_BAND_ABOVE_25 = 0.03             # Lange (S) against NIST (P) converted to STP, 30 and 35 C. DERIVED band.
ALPHA_BAND_BELOW_25 = 0.02             # interpolation error between Lange anchors. ASSUMPTION.

CO2_AIR_ATM = 420e-6                   # CO2 partial pressure in room air. ASSUMPTION (record uses 432 ppm monthly peak).

# Citric acid and carbonic acid, 25 C. CRC Handbook Section 8 via a course copy (P, edition caveat).
CIT_PKA = (3.13, 4.76, 6.40)
CARB_PKA = (6.35, 10.33)               # apparent constants; the CRC entry is labelled H2CO3 (P, ambiguity).
PKW = 13.995                           # CRC (P).

# Mass transfer. D: CO2 diffusivity in water at 25 C, 1.92e-9 m2/s (Cussler textbook value via Wikipedia, S;
# other sources read 1.88 to 1.95e-9 m2/s, and the high-pressure TRC value is 2.2e-9 at 14 MPa, not used).
DIFF_CO2_M2S = 1.92e-9
GLASS_DIAM_M = 0.065                   # serving glass, cross-section. ASSUMPTION.

# Sensory threshold, sparkling sensation, mineral water: BET 0.44 g/L (Puleo et al. 2021, P)
# divided by 1.977 g/L per volume of CO2 at STP (DERIVED). Applied to a soft drink as a proxy: LIMIT.
THRESH_VOL = 0.44 / 1.977

# Ice and water heat balance. Wikipedia data pages (S): latent heat of fusion 333.55 J/g; Cp of liquid water 4.1787 J/(g K).
ICE_LATENT_J_G = 333.55
CP_WATER_J_GK = 4.1787

# Sweetener. Sucralose sweetness relative to sucrose: 600 to 650 (JECFA monograph, P); 600 used (lower end).
SUCRALOSE_RS = 600.0
SWEET_ANCHOR_SUGAR_G_PER_100ML = 6.0  # the Thai 02.02 tier boundary, used as a sweetness anchor. ASSUMPTION (sensory not tested).

# Storage and pack. Storage temperature and headspace: ASSUMPTION until Thai climate source is read.
STORE_C = 35.0
HEADSPACE_ML = 20.0


def alpha(t_c):
    """Volumes of CO2 (STP) per volume of water at 1 atm pure CO2, at t_c degrees Celsius (0 to 35 C)."""
    T = t_c + 273.15
    xs = sorted(ALPHA_ANCHOR)
    for lo, hi in zip(xs, xs[1:]):
        if lo <= t_c <= hi:
            x0, x1 = 1 / (lo + 273.15), 1 / (hi + 273.15)
            y0, y1 = math.log(ALPHA_ANCHOR[lo]), math.log(ALPHA_ANCHOR[hi])
            return math.exp(y0 + (y1 - y0) * (1 / T - x0) / (x1 - x0))
    raise ValueError("temperature outside the 0 to 35 C anchor range")


def alpha_band(t_c):
    if t_c > 25:
        return ALPHA_BAND_ABOVE_25
    return ALPHA_BAND_BELOW_25


def ceq_vol(t_c):
    """Open-air equilibrium dissolved CO2, volumes. The endpoint of degassing in an open glass."""
    return alpha(t_c) * CO2_AIR_ATM


def _h(ph):
    return 10 ** -ph


def _citrate_z(h):
    k1, k2, k3 = (10 ** -p for p in CIT_PKA)
    d = h ** 3 + k1 * h ** 2 + k1 * k2 * h + k1 * k2 * k3
    return (k1 * h ** 2 + 2 * k1 * k2 * h + 3 * k1 * k2 * k3) / d


def _carbonate_charge(h, c_tot):
    c1, c2 = (10 ** -p for p in CARB_PKA)
    g = h * h + c1 * h + c1 * c2
    return c_tot * (c1 * h + 2 * c1 * c2) / g


def charge_residual(ph, k_m, a_m, cT_m, cit_m):
    """Charge balance: K+ + alkalinity cation + H+ = OH- + carbonate charge + citrate charge (molar)."""
    h = _h(ph)
    kw = 10 ** -PKW
    return k_m + a_m + h - kw / h - _carbonate_charge(h, cT_m) - cit_m * _citrate_z(h)


def solve_ph(k_m, a_m, cT_m, cit_m):
    lo, hi = 0.0, 14.0
    f_lo = charge_residual(lo, k_m, a_m, cT_m, cit_m)
    f_hi = charge_residual(hi, k_m, a_m, cT_m, cit_m)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f_mid = charge_residual(mid, k_m, a_m, cT_m, cit_m)
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return 0.5 * (lo + hi)


def citrate_for_ph(ph_target, k_m, a_m, cT_m):
    """Citrate (molar, all forms) that gives ph_target, solved from the charge balance (analytic)."""
    h = _h(ph_target)
    kw = 10 ** -PKW
    num = k_m + a_m + h - kw / h - _carbonate_charge(h, cT_m)
    return num / _citrate_z(h)


def serve_model(dose_vol=0.9, prepared_L=DOSE_BASIS_L, serve_c=25.0, ice_g=0.0,
                t_r_s=10.0, alk_mg_caco3_L=0.0, target_ph=3.0):
    """One serve. dose_vol is CO2 volumes per 330 mL of the design; prepared_L is the drink volume
    before ice; serve_c is the water temperature before ice; ice_g is the ice added to the glass."""
    m_w = prepared_L * 1000.0
    if ice_g > 0:
        t_f = (m_w * CP_WATER_J_GK * serve_c - ice_g * ICE_LATENT_J_G) / ((m_w + ice_g) * CP_WATER_J_GK)
    else:
        t_f = serve_c
    v_total = prepared_L + ice_g / 1000.0                       # melt water adds 1 mL per gram of ice
    n_co2_mmol = dose_vol * DOSE_BASIS_L / MOLAR_VOLUME_STP_L * 1000.0
    vol_eff = dose_vol * DOSE_BASIS_L / v_total                 # nominal volumes after dilution
    c0 = min(vol_eff, alpha(t_f))                               # dissolved at serve; the excess leaves as gas
    escaped = 1.0 - c0 / vol_eff
    cT_mmol = c0 * v_total / MOLAR_VOLUME_STP_L * 1000.0        # dissolved carbonate, mmol
    k_m = n_co2_mmol / (v_total * 1000.0)
    cT_m = cT_mmol / (v_total * 1000.0)
    a_m = (alk_mg_caco3_L / 50.0) * v_total / (v_total * 1000.0) # mg/L as CaCO3 to meq/L (= mmol/L) to molar
    c_needed_m = citrate_for_ph(target_ph, k_m, a_m, cT_m)
    c_needed_mmol = c_needed_m * v_total * 1000.0
    stoich_mmol = n_co2_mmol / 3.0
    kl = 2.0 * math.sqrt(DIFF_CO2_M2S / (math.pi * t_r_s))     # penetration theory, m/s
    a_surf = math.pi * (GLASS_DIAM_M / 2.0) ** 2                # m2
    tau_s = (v_total * 1e-3) / (kl * a_surf)                    # mass-transfer time constant, s
    ceq = ceq_vol(t_f)
    if c0 > THRESH_VOL:
        t_thr_s = tau_s * math.log((c0 - ceq) / (THRESH_VOL - ceq))
    else:
        t_thr_s = 0.0
    ph_check = solve_ph(k_m, a_m, cT_m, c_needed_m)
    return {
        "serve_c": round(t_f, 2),
        "v_total_L": round(v_total, 4),
        "alpha_at_serve": round(alpha(t_f), 4),
        "dissolved_vol_at_serve": round(c0, 4),
        "escaped_fraction": round(escaped, 4),
        "kl_m_s": kl,
        "tau_min": round(tau_s / 60.0, 1),
        "t_above_threshold_min": round(t_thr_s / 60.0, 1),
        "ceq_vol": ceq,
        "potassium_mg_per_serve": round(n_co2_mmol * K_MW, 1),
        "khco3_g": round(n_co2_mmol / 1000.0 * KHCO3_MW, 3),
        "citric_stoich_g": round(stoich_mmol / 1000.0 * CITRIC_MW, 3),
        "citric_total_for_target_g": round(c_needed_mmol / 1000.0 * CITRIC_MW, 3),
        "citric_free_for_target_g": round((c_needed_mmol - stoich_mmol) / 1000.0 * CITRIC_MW, 3),
        "target_ph": target_ph,
        "ph_at_design_acid": None if ph_check is None else round(ph_check, 2),
    }


def dose_temperature_table():
    doses = [0.5, 0.6, 0.7, 0.76, 0.8, 0.9, 1.0]
    temps = [5, 10, 15, 20, 25, 30, 35]
    rows = []
    for d in doses:
        rows.append({"dose_vol": d, "dissolved_by_temp_c": {str(t): round(min(d, alpha(t)), 3) for t in temps}})
    return {"temps_c": temps, "alpha_by_temp_c": {str(t): round(alpha(t), 3) for t in temps},
            "alpha_band_pct_by_temp_c": {str(t): round(100 * alpha_band(t), 1) for t in temps},
            "rows": rows}


def ice_and_serve_scenarios():
    cases = [
        ("chilled water 5 C, no ice", dict(serve_c=5.0)),
        ("room water 25 C, no ice", dict(serve_c=25.0)),
        ("ambient water 30 C, no ice", dict(serve_c=30.0)),
        ("hot day 35 C, no ice", dict(serve_c=35.0)),
        ("ambient 30 C with 30 g ice", dict(serve_c=30.0, ice_g=30.0)),
        ("ambient 30 C with 60 g ice", dict(serve_c=30.0, ice_g=60.0)),
    ]
    out = {}
    for name, kw in cases:
        out[name] = serve_model(**kw)
    return out


def sensitivity_on_mass_transfer():
    out = {}
    for tr in (1.0, 5.0, 10.0, 30.0):
        m = serve_model(serve_c=25.0, t_r_s=tr)
        out[str(tr)] = {"kl_m_s": m["kl_m_s"], "tau_min": m["tau_min"], "t_above_threshold_min": m["t_above_threshold_min"]}
    return out


def sensitivity_on_target_ph():
    out = {}
    for ph in (2.8, 3.0, 3.2, 3.5, 4.0, 4.5):
        m = serve_model(serve_c=25.0, target_ph=ph)
        out[str(ph)] = {"citric_total_g": m["citric_total_for_target_g"], "citric_free_g": m["citric_free_for_target_g"]}
    return out


def alkalinity_sensitivity():
    out = {}
    for alk in (0, 50, 100, 150):
        m = serve_model(serve_c=25.0, alk_mg_caco3_L=alk)
        out[str(alk)] = {"citric_total_g": m["citric_total_for_target_g"], "citric_free_g": m["citric_free_for_target_g"]}
    return out


def storage_gas():
    n_mmol = serve_model()["potassium_mg_per_serve"] / K_MW     # mmol CO2 generated at 0.9 volume
    rows = {}
    for f in (0.001, 0.005, 0.01, 0.05):
        v_pre_ml = f * n_mmol / 1000.0 * R_L_ATM * (STORE_C + 273.15) * 1000.0
        rows[str(f)] = {"gas_ml": round(v_pre_ml, 2), "pressure_rise_pct_in_headspace": round(100 * v_pre_ml / HEADSPACE_ML, 1)}
    return {"store_c": STORE_C, "headspace_ml": HEADSPACE_ML, "rows": rows}


def sucralose_mg_per_serve(prepared_ml=330.0):
    sugar_g = SWEET_ANCHOR_SUGAR_G_PER_100ML * prepared_ml / 100.0
    return round(sugar_g * 1000.0 / SUCRALOSE_RS, 1)


def potassium_bases(k_mg):
    # Thai RDI 3,500 mg/day: MOPH Notification 182 (B.E. 2541) read as primary; the current No. 445 value
    # is 3,500 mg per a consultancy page (S), the Royal Gazette text was not read. WHO 3,510 mg (P, news release).
    # EU NRV 2,000 mg is not a Thai reference; shown for comparison only.
    return {
        "thai_rdi_3500_mg": round(100 * k_mg / 3500.0, 1),
        "who_adult_minimum_3510_mg": round(100 * k_mg / 3510.0, 1),
        "eu_nrv_2000_mg_not_thai": round(100 * k_mg / 2000.0, 1),
    }


def monte_carlo(n=10000, seed=20261019):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        t = rng.uniform(5.0, 35.0)
        tr = math.exp(rng.uniform(math.log(1.0), math.log(30.0)))
        alk = rng.uniform(0.0, 150.0)
        ph = rng.uniform(2.8, 3.5)
        m = serve_model(serve_c=t, t_r_s=tr, alk_mg_caco3_L=alk, target_ph=ph)
        rows.append({"c0": m["dissolved_vol_at_serve"], "esc": m["escaped_fraction"], "tau": m["tau_min"],
                     "thr": m["t_above_threshold_min"], "citric_total": m["citric_total_for_target_g"],
                     "citric_free": m["citric_free_for_target_g"]})

    def pct(key):
        xs = sorted(r[key] for r in rows)
        return {p: round(xs[int(q * (len(xs) - 1))], 3) for p, q in (("p5", 0.05), ("p50", 0.5), ("p95", 0.95))}

    return {"n": n, "seed": seed,
            "inputs": {"serve_c": "U(5,35)", "t_r_s": "logU(1,30)", "alk_mg_caco3_L": "U(0,150)", "target_ph": "U(2.8,3.5)"},
            "dissolved_vol_at_serve": pct("c0"), "escaped_fraction": pct("esc"),
            "tau_min": pct("tau"), "t_above_threshold_min": pct("thr"),
            "citric_total_g": pct("citric_total"), "citric_free_g": pct("citric_free")}


def main():
    design = serve_model(serve_c=25.0)
    result = {
        "design_dose_vol": 0.9,
        "dose_basis_ml": 330,
        "constants": {
            "alpha_anchor_c": ALPHA_ANCHOR, "co2_air_atm": CO2_AIR_ATM, "cit_pka": CIT_PKA,
            "carb_pka": CARB_PKA, "pkw": PKW, "diff_co2_m2_s": DIFF_CO2_M2S, "glass_diam_m": GLASS_DIAM_M,
            "thresh_vol": round(THRESH_VOL, 4), "ice_latent_j_g": ICE_LATENT_J_G, "cp_water_j_gk": CP_WATER_J_GK,
            "sucralose_rs": SUCRALOSE_RS, "sweet_anchor_g_per_100ml": SWEET_ANCHOR_SUGAR_G_PER_100ML,
            "store_c": STORE_C, "headspace_ml": HEADSPACE_ML,
        },
        "design_at_25c": design,
        "potassium_bases_pct": potassium_bases(design["potassium_mg_per_serve"]),
        "dose_by_temperature": dose_temperature_table(),
        "serve_scenarios": ice_and_serve_scenarios(),
        "sensitivity_mass_transfer_tr_s": sensitivity_on_mass_transfer(),
        "sensitivity_target_ph": sensitivity_on_target_ph(),
        "alkalinity_sensitivity": alkalinity_sensitivity(),
        "storage_gas": storage_gas(),
        "sucralose_mg_per_330ml": sucralose_mg_per_serve(),
        "monte_carlo": monte_carlo(),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", OUT.name)


if __name__ == "__main__":
    main()
