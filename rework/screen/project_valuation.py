"""Product-level project valuation for the Lime Cube (desk model, team-only).

Standard library only. Deterministic: no random draws and no clock.
Run with:  python -I project_valuation.py
Reads:     pack_economics_results.json and formulation_desk_model_results.json (this folder).
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
FORM_PATH = os.path.join(HERE, "formulation_desk_model_results.json")
OUT_PATH = os.path.join(HERE, "project_valuation_results.json")

# Scenario and method choices (all ASSUMPTION).
VOLUMES = {"low": 50000, "base": 200000, "high": 1000000}   # cubes per year, steady state
RAMP = [0.5, 1.0, 1.0, 1.0, 1.0]                              # year 1 at half volume
RATES = [0.08, 0.10, 0.12]                                    # discount rate range
BASE_RATE = 0.10
FIXED_GRID = [250000, 500000, 1000000, 2000000]               # THB per year, not sourced
BASE_VOLUME_KEY = "base"
BASE_PACK = 12
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
FORM = load(FORM_PATH)
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


KHCO3_G = FORM["design_at_25c"]["khco3_g"]                    # 1.327 g at 0.9 volume
CITRIC_G_PH35 = FORM["sensitivity_target_ph"]["3.5"]["citric_total_g"]   # 3.42 g at pH 3.5
CITRIC_G_PH30 = FORM["sensitivity_target_ph"]["3.0"]["citric_total_g"]   # 5.965 g at pH 3.0
SUCRALOSE_MG = FORM["sucralose_mg_per_330ml"]                 # 33.0 mg

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
        "Stoichiometry at 0.9 volume of CO2 per 330 ml (formulation desk model)"),
    inp("citric_g_ph35", "Total citric acid per cube at pH 3.5", CITRIC_G_PH35, "g", "none", "DERIVED",
        "DERIVED", "Charge balance, citric pKa 3.13, 4.76, 6.40 (tier P, CRC); formulation desk model"),
    inp("citric_g_ph30", "Total citric acid per cube at pH 3.0", CITRIC_G_PH30, "g", "none", "DERIVED",
        "DERIVED", "Formulation desk model, sensitivity"),
    inp("sucralose_mg", "Sucralose per cube", SUCRALOSE_MG, "mg", "none", "DERIVED", "DERIVED",
        "Formulation desk model (sweetness 600 times sucrose; JECFA monograph, tier P)"),
    inp("dose_vol", "CO2 dose per 330 ml", FORM["design_dose_vol"], "volumes", "none", "ASSUMPTION",
        "ASSUMPTION", "Team decision of 19 October 2026; under review because its basis was withdrawn"),
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

PACK_ROWS = {row["pack_size"]: row for row in PACK["pack_rows_target_ph_3_5"]}
COST_JSON = {size: PACK_ROWS[size]["cost_per_cube_thb"] for size in (1, 6, 12, 24)}
CARTON_JSON = {size: PACK_ROWS[size]["carton_thb"] for size in (1, 6, 12, 24)}
BREAKDOWN_35 = PACK["cost_breakdown_target_ph_3_5"]
BREAKDOWN_30 = PACK["cost_breakdown_target_ph_3_0"]
REACTANTS_35 = BREAKDOWN_35["reactants_thb"]
REACTANTS_30 = BREAKDOWN_30["reactants_thb"]

# Cross-check 1: reactant cost recomputed from masses and prices.
REACT_RECOMP = (
    KHCO3_G * value("khco3_price") / 1000.0
    + CITRIC_G_PH35 * value("citric_price") / 1000.0
    + SUCRALOSE_MG * value("sucralose_price") / 1e6
)
assert abs(REACT_RECOMP - REACTANTS_35) < 0.005, (REACT_RECOMP, REACTANTS_35)

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
assert abs(K_MG_RECOMP - FORM["design_at_25c"]["potassium_mg_per_serve"]) < 0.5

SHELF = value("shelf")
SHARE = value("ex_share")
EX = SHELF * SHARE
assert abs(EX - PACK["prices"]["shelf_thb_per_cube"]["base"] * PACK["prices"]["ex_factory_share"]["base"]) < 1e-9
assert abs(EX - PACK["pack_rows_target_ph_3_5"][2]["ex_factory_thb_per_cube"]) < 1e-9

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

SENS = [
    sens_row("Base: 12-cube carton, pH 3.5, 0.9 volume, shelf 15 THB, ex-factory 60%", C_BASE,
             "Model base"),
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
    sens_row("Carton 3 THB per 12 (low)", EX - (COST_BASE + (3.0 - carton_b) / BASE_PACK), "UNVERIFIED listing range"),
    sens_row("Carton 7 THB per 12 (high)", EX - (COST_BASE + (7.0 - carton_b) / BASE_PACK), "UNVERIFIED listing range"),
    sens_row("All four packaging inputs at low", EX - (COST_BASE + (0.67 - pouch_b) + (0.8 - print_b)
                                                       + (0.25 - proc_b) + (3.0 - carton_b) / BASE_PACK),
             "Combined bound, not a probability"),
    sens_row("All four packaging inputs at high", EX - (COST_BASE + (2.70 - pouch_b) + (2.5 - print_b)
                                                        + (1.0 - proc_b) + (7.0 - carton_b) / BASE_PACK),
             "Combined bound, not a probability"),
    sens_row("Target pH 3.0 (reactants 0.259 THB)", EX - (COST_BASE + (REACTANTS_30 - REACTANTS_35)),
             "Formulation model"),
    sens_row("Dose 0.55 volume (reactants scaled linearly)",
             EX - (COST_BASE + (REACTANTS_35 * 0.55 / dose_scale - REACTANTS_35)),
             "DERIVED approximation; assumes free-acid excess scales with dose"),
    sens_row("Excise 14% of an assumed ex-factory base (1.26 THB per cube)",
             C_BASE - EXCISE_RATE_02_02 * EX, "Base not read; classification open"),
    sens_row("Pack: single pouch, no carton", EX - COST_JSON[1], "Flatters: carries no carton"),
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
    "model": "Lime Cube product-level project valuation, desk model, pre-tax, domestic Thailand",
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
        "potassium_mg_json": FORM["design_at_25c"]["potassium_mg_per_serve"],
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
