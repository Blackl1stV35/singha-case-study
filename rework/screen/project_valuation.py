"""Product-level project valuation for the Lemon Soda (desk model, team-only).

Standard library only. Deterministic: no random draws and no clock.
Run with:  python -I project_valuation.py
Reads:     pack_economics_results.json (prices) and handover_figures_results.json (0.55-volume design
           and pack rows) in this folder. Rebased 19 October 2026 from the 0.9-volume design.
Writes:    project_valuation_results.json (this folder).

Every input is listed in INPUTS with a tier (P, S or none) and a status
(SOURCED, DERIVED, PROXY, ASSUMPTION or UNVERIFIED). A figure whose source page is
not saved in the record store is UNVERIFIED, whatever its kind.

Model (pre-tax, product level, domestic Thailand):
  cash flow in year t (t = 1..5) = c * V * ramp_t - F
  c   = contribution per cube (ex-factory price minus cost per cube, THB)
  V   = steady-state cubes per year (scenario, ASSUMPTION)
  F   = annual fixed cash cost (grid, ASSUMPTION; not sourced)
  setup outlay in year 0 = F (convention, ASSUMPTION)
  no terminal value
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PACK_PATH = os.path.join(HERE, "pack_economics_results.json")
HANDOVER_PATH = os.path.join(HERE, "handover_figures_results.json")
OUT_PATH = os.path.join(HERE, "project_valuation_results.json")

# Scenario and method choices (all ASSUMPTION).
VOLUMES = {"low": 50000, "base": 200000, "high": 1000000}   # cubes per year, steady state
RAMP = [0.5, 1.0, 1.0, 1.0, 1.0]                              # year 1 at half volume
RATES = [0.08, 0.10, 0.12]                                    # discount rate range
BASE_RATE = 0.10
FIXED_GRID = [250000, 500000, 1000000, 2000000]               # THB per year, not sourced
BASE_VOLUME_KEY = "base"
BASE_PACK = 6   # recommended portable pack, 19 October 2026 (user)
CPA_BASE = 1150.0   # THB per first purchase, paid social base case (acquisition record; UNVERIFIED inputs)
ACQ_CUBES = (12, 50, 225)

# Chemistry constants for the cross-check only (standard atomic weights, IUPAC; tier P).
K_ATOMIC = 39.0983
KHCO3_MOLAR = 100.1191
EXCISE_RATE_02_02 = 0.14   # Royal Gazette 2560 schedule, item 02.02, ad valorem (base not read)


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


PACK = load(PACK_PATH)
HAND = load(HANDOVER_PATH)
PRICES = PACK["prices"]


def inp(key, label, value, unit, tier, kind, status, source):
    return {
        "key": key,
        "label": label,
        "value": value,
        "unit": unit,
        "tier": tier,
        "kind": kind,
        "status": status,
        "source": source,
    }


DESIGN = HAND["design"]
RECIPE = HAND["per_330ml_recipe"]
KHCO3_G = RECIPE["potassium_bicarbonate_g"]                   # 0.811 g at 0.55 volume
CITRIC_G_PH35 = RECIPE["citric_acid_total_for_pH_target_g"]   # 2.10 g at pH 3.5
CITRIC_G_PH30 = HAND["citric_by_target_ph_g_per_330ml"]["3.0"]["total"]   # 3.701 g at pH 3.0
SUCRALOSE_MG = RECIPE["sucralose_mg"]                         # 33.0 mg
DOSE_VOL = DESIGN["co2_volumes_per_330ml"]                    # 0.55 volume (decision D14)
POTASSIUM_MG_HAND = RECIPE["potassium_mg"]                    # 316.6 mg per serve

INPUTS = [
    inp("khco3_price", "Potassium bicarbonate price", PRICES["khco3_thb_per_kg"]["base"], "THB/kg",
        "P", "PROXY", "UNVERIFIED",
        "UN Comtrade HS 2836.40 import unit value 2024 (carbonate line, may mix bicarbonate); page not saved; no Thai price found"),
    inp("citric_price", "Citric acid price", PRICES["citric_thb_per_kg"]["base"], "THB/kg",
        "P", "PROXY", "UNVERIFIED",
        "UN Comtrade HS 2918.14 import unit value 2025 (estimated weight); page not saved; no Thai price found"),
    inp("sucralose_price", "Sucralose price", PRICES["sucralose_thb_per_kg"]["base"], "THB/kg",
        "S", "LISTED", "UNVERIFIED",
        "Retailer asking price, Thai online marketplace; page not saved; cost effect is about 0.02 THB per cube"),
    inp("pouch", "Pouch, 90 x 70 mm laminate", PRICES["pouch_thb"]["base"], "THB/piece",
        "S", "DERIVED", "UNVERIFIED",
        "Non-Thai listing USD 0.03 to 0.05 per piece, MOQ 1,000, converted; listing page not saved; no Thai converter price"),
    inp("print", "Print", PRICES["print_thb"]["base"], "THB/cube", "none", "ASSUMPTION",
        "ASSUMPTION", "Placeholder; no sourced price"),
    inp("processing", "Compaction, sealing and packing labour", PRICES["processing_thb"]["base"], "THB/cube",
        "none", "ASSUMPTION", "ASSUMPTION", "No sourced figure"),
    inp("carton_12", "Carton, 12 cubes", PRICES["carton_thb"]["12"]["base"], "THB/carton",
        "S", "LISTED", "UNVERIFIED",
        "Retail asking price for a 20 x 14 x 12 cm box, Thai home-improvement retailer; page not saved"),
    inp("carton_6", "Carton, 6 cubes", PRICES["carton_thb"]["6"]["base"], "THB/carton",
        "none", "ASSUMPTION", "ASSUMPTION", "Scaled from the 12-cube price"),
    inp("carton_24", "Carton, 24 cubes", PRICES["carton_thb"]["24"]["base"], "THB/carton",
        "none", "ASSUMPTION", "ASSUMPTION", "Scaled from the 12-cube price"),
    inp("binder_flavour", "Binder, filler and lemon flavour per cube", "not priced", "text", "none",
        "ASSUMPTION", "ASSUMPTION",
        "Masses assumed in rework/48 section 6.1 (binder 0.80 g, flavour 0.05 g); no price, so the cost per cube excludes them"),
    inp("shelf", "Shelf price per cube", PRICES["shelf_thb_per_cube"]["base"], "THB/cube",
        "S", "ASSUMPTION", "ASSUMPTION",
        "The cube is not priced. Reference: 330 ml zero-sugar cans at 16 to 17 THB, Thai online retailer, captured 18 October 2026 (SOURCED, secondary)"),
    inp("ex_share", "Ex-factory share of shelf price", PRICES["ex_factory_share"]["base"], "fraction",
        "none", "ASSUMPTION", "ASSUMPTION",
        "No sourced margin. Cross-check: mid-case value-chain factor 0.595 from assumed margins"),
    inp("excise_rate", "Excise, item 02.02, ad valorem", EXCISE_RATE_02_02, "fraction",
        "P", "SOURCED", "SOURCED",
        "Royal Gazette 2560 (2017) excise schedule, read from page images; a sweetened, flavoured drink falls in 02.02; latest period in the notice 1 October 2566 onwards"),
    inp("excise_base", "Excise value base", "ex-factory (assumed for sensitivity only)", "text",
        "P", "ASSUMPTION", "UNVERIFIED",
        "The notice does not state the value base and it was not read; the baht amount is UNVERIFIED"),
    inp("excise_tier_per_l", "Excise per-litre tier, up to 6 g sugar per 100 ml", 0.0, "THB/litre",
        "P", "SOURCED", "SOURCED", "Same schedule; a sugar-free sweetened drink falls in tier (a) at 0 THB per litre"),
    inp("khco3_g", "Potassium bicarbonate per cube", KHCO3_G, "g", "none", "DERIVED", "DERIVED",
        "Stoichiometry at 0.55 volume of CO2 per 330 ml (handover figures)"),
    inp("citric_g_ph35", "Total citric acid per cube at pH 3.5", CITRIC_G_PH35, "g", "none", "DERIVED",
        "DERIVED", "Charge balance, citric pKa 3.13, 4.76, 6.40 (tier P, CRC); handover figures at 0.55 volume"),
    inp("citric_g_ph30", "Total citric acid per cube at pH 3.0", CITRIC_G_PH30, "g", "none", "DERIVED",
        "DERIVED", "Handover figures, pH 3.0 sensitivity at 0.55 volume"),
    inp("sucralose_mg", "Sucralose per cube", SUCRALOSE_MG, "mg", "none", "DERIVED", "DERIVED",
        "Handover figures at 0.55 volume (sweetness 600 times sucrose; JECFA monograph, tier P)"),
    inp("dose_vol", "CO2 dose per 330 ml", DOSE_VOL, "volumes", "none", "DECIDED",
        "DECIDED", "User decision, 19 October 2026 (rework/52 D14); recommended over the 0.9-volume design"),
    inp("target_ph", "Target pH", 3.5, "pH", "none", "ASSUMPTION", "ASSUMPTION", "Working assumption"),
    inp("vol_low", "Volume scenario, low", VOLUMES["low"], "cubes per year", "none", "ASSUMPTION",
        "ASSUMPTION", "Scenario; no volume basis in the record"),
    inp("vol_base", "Volume scenario, base", VOLUMES["base"], "cubes per year", "none", "ASSUMPTION",
        "ASSUMPTION", "Scenario; no volume basis in the record"),
    inp("vol_high", "Volume scenario, high", VOLUMES["high"], "cubes per year", "none", "ASSUMPTION",
        "ASSUMPTION", "Scenario; no volume basis in the record"),
    inp("ramp", "Year 1 volume as share of steady state", RAMP[0], "fraction", "none", "ASSUMPTION",
        "ASSUMPTION", "Launch ramp; years 2 to 5 at full volume"),
    inp("horizon", "Horizon", len(RAMP), "years", "none", "ASSUMPTION", "ASSUMPTION",
        "Five-year horizon; no terminal value"),
    inp("rates", "Discount rate range", "8% to 12%", "per year", "none", "ASSUMPTION", "ASSUMPTION",
        "Range set for this model; base 10%"),
    inp("fixed_grid", "Annual fixed cash cost grid", "250,000 to 2,000,000", "THB per year", "none",
        "ASSUMPTION", "ASSUMPTION", "Grid, not a sourced figure; tooling, registration, trademark, pouch minimums and marketing are inside it"),
    inp("setup", "Year 0 setup outlay", "equal to one year of fixed cost", "text", "none", "ASSUMPTION",
        "ASSUMPTION", "Convention so the grid covers the one-off cost; no sourced setup figure"),
    inp("cpa", "Paid-social cost per first purchase (base)", CPA_BASE, "THB", "S", "DERIVED", "UNVERIFIED",
        "Acquisition record base case from PROXY and ASSUMPTION inputs; ad-cost pages not saved"),
]

INPUT_INDEX = {item["key"]: item for item in INPUTS}


def value(key):
    return INPUT_INDEX[key]["value"]


# ---- Unit economics -------------------------------------------------------

HCOST = HAND["cost_and_containers"]
HAND_PACKS = HCOST["packs"]
REACTANTS_35 = HCOST["reactants_thb_per_cube"]
BREAKDOWN_35 = {"per_pouch_before_carton_thb": HCOST["per_pouch_before_carton_thb"], "reactants_thb": REACTANTS_35}
COST_JSON = {1: HCOST["per_pouch_before_carton_thb"]}   # single pouch, no carton
COST_JSON.update({size: HAND_PACKS[str(size)]["cost_per_cube_thb"] for size in (6, 12, 24)})
CARTON_JSON = {1: 0.0}
CARTON_JSON.update({size: PRICES["carton_thb"][str(size)]["base"] for size in (6, 12, 24)})


def reactants_for(citric_g):
    return (KHCO3_G * value("khco3_price") / 1000.0
            + citric_g * value("citric_price") / 1000.0
            + SUCRALOSE_MG * value("sucralose_price") / 1e6)


# Cross-check 1: reactant cost recomputed from masses and prices (0.55 volume, pH 3.5 and pH 3.0).
REACT_RECOMP = reactants_for(CITRIC_G_PH35)
assert abs(REACT_RECOMP - REACTANTS_35) < 0.005, (REACT_RECOMP, REACTANTS_35)
REACTANTS_30 = reactants_for(CITRIC_G_PH30)

# Cross-check 2: cost per cube by pack size recomputed from components.
PACK_CHECK = {}
for size in (1, 6, 12, 24):
    recomputed = (
        REACTANTS_35
        + value("pouch")
        + value("print")
        + value("processing")
        + CARTON_JSON[size] / size
    )
    PACK_CHECK[str(size)] = {
        "json_cost": COST_JSON[size],
        "recomputed": round(recomputed, 4),
        "diff": round(recomputed - COST_JSON[size], 4),
    }
    assert abs(recomputed - COST_JSON[size]) < 0.01, (size, recomputed, COST_JSON[size])

# Cross-check 3: potassium per serve from the bicarbonate mass.
K_MG_RECOMP = KHCO3_G * K_ATOMIC / KHCO3_MOLAR * 1000.0
assert abs(K_MG_RECOMP - POTASSIUM_MG_HAND) < 0.5

SHELF = value("shelf")
SHARE = value("ex_share")
EX = SHELF * SHARE
assert abs(EX - PACK["prices"]["shelf_thb_per_cube"]["base"] * PACK["prices"]["ex_factory_share"]["base"]) < 1e-9
assert abs(EX - HAND_PACKS["6"]["ex_factory_thb_per_cube"]) < 1e-9

C_BY_PACK = {str(size): round(EX - COST_JSON[size], 4) for size in (1, 6, 12, 24)}
COST_BASE = COST_JSON[BASE_PACK]
C_BASE = EX - COST_BASE                 # 9.00 - 3.90 = 5.10 THB per cube
MARGIN_BASE = C_BASE / EX


# ---- Cash flows and valuation ---------------------------------------------

def annuity(rate):
    disc = [(1.0 + rate) ** -t for t in range(1, len(RAMP) + 1)]
    a_sum = sum(disc)
    r_sum = sum(ramp * d for ramp, d in zip(RAMP, disc))
    return a_sum, r_sum, disc


def flows(c, v, f):
    return [c * v * ramp - f for ramp in RAMP]


def npv(c, v, f, rate):
    _, _, disc = annuity(rate)
    return -f + sum(cf * d for cf, d in zip(flows(c, v, f), disc))


def payback_years(c, v, f):
    """Undiscounted payback from the year 0 outlay (= f). None if not within the horizon."""
    cum = -f
    for t, cf in enumerate(flows(c, v, f), start=1):
        prev = cum
        cum = prev + cf
        if cum >= 0:
            return round((t - 1) + (-prev) / cf, 2)
    return None


def breakeven_volume(c, f, rate):
    a_sum, r_sum, _ = annuity(rate)
    return f * (1.0 + a_sum) / (c * r_sum)


def max_fixed(c, v, rate):
    a_sum, r_sum, _ = annuity(rate)
    return c * v * r_sum / (1.0 + a_sum)


# Cross-check 4: the closed forms give NPV zero at their roots.
for rate in RATES:
    v_star = breakeven_volume(C_BASE, 500000, rate)
    assert abs(npv(C_BASE, v_star, 500000, rate)) < 1e-4
    f_star = max_fixed(C_BASE, VOLUMES["base"], rate)
    assert abs(npv(C_BASE, VOLUMES["base"], f_star, rate)) < 1e-4

scenario_results = []
for key in ("low", "base", "high"):
    v = VOLUMES[key]
    for f in FIXED_GRID:
        entry = {
            "scenario": key,
            "cubes_per_year": v,
            "fixed_cost_thb_per_year": f,
            "setup_outlay_thb": f,
            "contribution_per_cube_thb": round(C_BASE, 4),
            "npv_thb": {str(rate): round(npv(C_BASE, v, f, rate)) for rate in RATES},
            "payback_years_base_rate": payback_years(C_BASE, v, f),
            "steady_state_cash_flow_thb": round(C_BASE * v - f),
        }
        scenario_results.append(entry)

max_fixed_by_scenario = {
    key: {str(rate): round(max_fixed(C_BASE, VOLUMES[key], rate)) for rate in RATES}
    for key in ("low", "base", "high")
}

breakeven_by_fixed = []
for f in FIXED_GRID:
    breakeven_by_fixed.append({
        "fixed_cost_thb_per_year": f,
        "simple_cubes_per_year_no_ramp_no_setup": round(f / C_BASE),
        "npv_zero_cubes_per_year": {str(rate): round(breakeven_volume(C_BASE, f, rate)) for rate in RATES},
    })


# ---- Sensitivities (one at a time, deltas to the base cost per cube) --------

def sens_row(label, c_new, note):
    f_star = max_fixed(c_new, VOLUMES[BASE_VOLUME_KEY], BASE_RATE)
    return {
        "change": label,
        "contribution_per_cube_thb": round(c_new, 4),
        "delta_vs_base_thb": round(c_new - C_BASE, 4),
        "max_fixed_cost_thb_per_year_base_volume_10pct": round(f_star),
        "note": note,
    }


pouch_b = value("pouch")
print_b = value("print")
proc_b = value("processing")
carton_b = CARTON_JSON[BASE_PACK]
dose_scale = value("dose_vol")

# Carton listing range is per 12 cubes (3 to 7 THB); scaled to a 6-cube carton by half (ASSUMPTION).
CARTON_LOW_6 = 3.0 * 6 / 12
CARTON_HIGH_6 = 7.0 * 6 / 12

SENS = [
    sens_row("Base: 6-cube carton, pH 3.5, 0.55 volume, shelf 15 THB, ex-factory 60%", C_BASE,
             "Model base (decision 19 October 2026)"),
    sens_row("Shelf price 10 THB (ex-factory 6.00)", 10 * SHARE - COST_BASE, "ASSUMPTION range"),
    sens_row("Shelf price 20 THB (ex-factory 12.00)", 20 * SHARE - COST_BASE, "ASSUMPTION range"),
    sens_row("Ex-factory share 50%", SHELF * 0.5 - COST_BASE, "ASSUMPTION range"),
    sens_row("Ex-factory share 70%", SHELF * 0.7 - COST_BASE, "ASSUMPTION range"),
    sens_row("Pouch 0.67 THB (low)", EX - (COST_BASE + (0.67 - pouch_b)), "DERIVED listing range, UNVERIFIED"),
    sens_row("Pouch 2.70 THB (high)", EX - (COST_BASE + (2.70 - pouch_b)), "DERIVED listing range, UNVERIFIED"),
    sens_row("Print 0.80 THB (low)", EX - (COST_BASE + (0.8 - print_b)), "ASSUMPTION range"),
    sens_row("Print 2.50 THB (high)", EX - (COST_BASE + (2.5 - print_b)), "ASSUMPTION range"),
    sens_row("Processing 0.25 THB (low)", EX - (COST_BASE + (0.25 - proc_b)), "ASSUMPTION range"),
    sens_row("Processing 1.00 THB (high)", EX - (COST_BASE + (1.0 - proc_b)), "ASSUMPTION range"),
    sens_row("Carton 1.50 THB per 6 (low, scaled from 3 THB per 12)",
             EX - (COST_BASE + (CARTON_LOW_6 - carton_b) / BASE_PACK), "UNVERIFIED listing range, scaled"),
    sens_row("Carton 3.50 THB per 6 (high, scaled from 7 THB per 12)",
             EX - (COST_BASE + (CARTON_HIGH_6 - carton_b) / BASE_PACK), "UNVERIFIED listing range, scaled"),
    sens_row("All four packaging inputs at low",
             EX - (COST_BASE + (0.67 - pouch_b) + (0.8 - print_b) + (0.25 - proc_b)
                   + (CARTON_LOW_6 - carton_b) / BASE_PACK),
             "Combined bound, not a probability"),
    sens_row("All four packaging inputs at high",
             EX - (COST_BASE + (2.70 - pouch_b) + (2.5 - print_b) + (1.0 - proc_b)
                   + (CARTON_HIGH_6 - carton_b) / BASE_PACK),
             "Combined bound, not a probability"),
    sens_row("Target pH 3.0 (reactants {:.3f} THB)".format(REACTANTS_30),
             EX - (COST_BASE + (REACTANTS_30 - REACTANTS_35)), "Handover figures, 0.55 volume"),
    sens_row("Dose 0.9 volume (earlier design; reactants scaled linearly)",
             EX - (COST_BASE + (REACTANTS_35 * (0.9 / DOSE_VOL - 1.0))),
             "DERIVED approximation; the 0.9-volume design is superseded"),
    sens_row("Excise 14% of an assumed ex-factory base (1.26 THB per cube)",
             C_BASE - EXCISE_RATE_02_02 * EX, "Base not read; classification open"),
    sens_row("Pack: single pouch, no carton", EX - COST_JSON[1], "Flatters: carries no carton"),
    sens_row("Pack: 12-cube carton (larger option)", EX - COST_JSON[12], "Model comparison"),
    sens_row("Pack: 24-cube carton", EX - COST_JSON[24], "Model comparison"),
]

# ---- Acquisition cross-check (not in the cash flows) ------------------------

acquisition = {
    "cpa_thb_per_first_purchase": CPA_BASE,
    "cubes_to_recover_cpa_at_base_contribution": round(CPA_BASE / C_BASE, 1),
    "acquisition_cost_per_cube_by_cubes_bought": [
        {"cubes_per_first_purchase": n, "cost_per_cube_thb": round(CPA_BASE / n, 2)} for n in ACQ_CUBES
    ],
}

# ---- Summary and output --------------------------------------------------

summary = {
    "base_case": {
        "pack": BASE_PACK,
        "cost_per_cube_thb": COST_BASE,
        "ex_factory_per_cube_thb": EX,
        "contribution_per_cube_thb": round(C_BASE, 4),
        "contribution_margin": round(MARGIN_BASE, 4),
        "volume": VOLUMES[BASE_VOLUME_KEY],
        "rate": BASE_RATE,
        "npv_at_fixed_250000_thb": round(npv(C_BASE, VOLUMES["base"], 250000, BASE_RATE)),
        "npv_at_fixed_500000_thb": round(npv(C_BASE, VOLUMES["base"], 500000, BASE_RATE)),
        "npv_at_fixed_1000000_thb": round(npv(C_BASE, VOLUMES["base"], 1000000, BASE_RATE)),
        "max_fixed_cost_thb_per_year_at_10pct": round(max_fixed(C_BASE, VOLUMES["base"], BASE_RATE)),
    },
}

RESULT = {
    "model": "Lemon Soda product-level project valuation, desk model, pre-tax, domestic Thailand",
    "scope_note": "Model output for the proposal. Not a valuation opinion. Not the group sum-of-parts.",
    "method": {
        "cash_flow_year_t": "c * V * ramp_t - F, t = 1..5",
        "setup_outlay_year_0": "F (convention)",
        "terminal_value": "none",
        "payback": "undiscounted, from year 0 outlay, linear within year",
        "break_even_volume": "V* = F * (1 + A) / (c * R), NPV zero, A = sum of discount factors, R = ramp-weighted sum",
        "max_fixed_cost": "F* = c * V * R / (1 + A)",
    },
    "inputs": INPUTS,
    "checks": {
        "reactants_recomputed_thb": round(REACT_RECOMP, 4),
        "reactants_json_thb": REACTANTS_35,
        "pack_cost_check": PACK_CHECK,
        "potassium_mg_recomputed": round(K_MG_RECOMP, 2),
        "potassium_mg_json": POTASSIUM_MG_HAND,
        "all_asserts_passed": True,
    },
    "unit_economics": {
        "shelf_thb": SHELF,
        "ex_factory_share": SHARE,
        "ex_factory_thb_per_cube": EX,
        "cost_per_cube_by_pack_thb": {str(k): v for k, v in COST_JSON.items()},
        "contribution_per_cube_by_pack_thb": C_BY_PACK,
        "base_pack": BASE_PACK,
        "base_cost_thb": COST_BASE,
        "base_contribution_thb": round(C_BASE, 4),
        "base_contribution_margin": round(MARGIN_BASE, 4),
        "cost_ph30_base_pack_thb": round(COST_BASE + (REACTANTS_30 - REACTANTS_35), 4),
        "pouch_plus_print_plus_processing_share_of_cost": round(
            (pouch_b + print_b + proc_b) / BREAKDOWN_35["per_pouch_before_carton_thb"], 4),
    },
    "volume_scenarios_cubes_per_year": VOLUMES,
    "scenario_results": scenario_results,
    "max_fixed_cost_by_scenario_thb_per_year": max_fixed_by_scenario,
    "break_even_by_fixed_cost": breakeven_by_fixed,
    "sensitivities": SENS,
    "acquisition_cross_check": acquisition,
    "summary": summary,
}


def main():
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(RESULT, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("contribution per cube (base):", round(C_BASE, 4))
    print("written:", OUT_PATH)


if __name__ == "__main__":
    main()
