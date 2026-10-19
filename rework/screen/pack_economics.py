"""Pack economics for the 0.9-volume cube: cost per cube, units per carton, units per container (desk).

Uses the formulation from formulation_desk_model.py for the reactant masses. Prices are inputs with a
status: SOURCED (read on a page), DERIVED (our arithmetic on a sourced figure), LISTED (asking price),
or ASSUMPTION (placeholder until a Thai input is read). Desk only; no quote requested.
Standard library only. Run with: python -I pack_economics.py
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import formulation_desk_model as fdm  # noqa: E402  (same folder; -I does not add it to sys.path)

OUT = HERE / "pack_economics_results.json"

# Exchange rate: midpoint of the Bank of Thailand average buying (sight) and selling (transfer) rates,
# 15 October 2026 (SOURCED, primary; raw/bot_fx_primary_2026-10-15.md). DERIVED midpoint.
FX_THB_PER_USD = (33.3535 + 33.7455) / 2.0

PRICES = {
    # THB per kg. US listing USD 242 for 22.68 kg (rework/53), converted at FX. LISTED (non-Thai); Thai price pending.
    # THB per kg. PROXY: UN Comtrade, Thailand imports, HS 2836.40 (potassium carbonates; the US national
    # line 2836.40.20.00 is bicarbonate, so the series may mix the two), 2024 unit value USD 1.136/kg. High is
    # a US small-pack listing (rework/53). Thai official statistics were not read.
    "khco3_thb_per_kg": {"base": 38.1, "low": 33.6, "high": 358.0,
                         "status": "PROXY: UN Comtrade HS 2836.40 import unit value 2024 (USD 1.136/kg); the line may mix carbonate and bicarbonate; high is a US small-pack listing (DERIVED)"},
    # THB per kg. PROXY: UN Comtrade, Thailand imports, HS 2918.14 (citric acid), 2025 unit value USD 0.936/kg
    # (weight estimated by UN); 2024 USD 0.894. High is a US small-pack listing (rework/53).
    "citric_thb_per_kg": {"base": 31.4, "low": 30.0, "high": 128.5,
                          "status": "PROXY: UN Comtrade HS 2918.14 import unit value 2025 (USD 0.936/kg, estimated weight); high is a US small-pack listing (DERIVED)"},
    # THB per kg. Lazada TH asking price THB 655 per kg (rework/53). High is UN Comtrade HS 2932.14 unit value
    # 2025 (USD 23.82/kg, a 6-digit proxy that may include other products).
    "sucralose_thb_per_kg": {"base": 655.0, "low": 400.0, "high": 799.0,
                             "status": "LISTED (Lazada TH asking price); high is UN Comtrade HS 2932.14 unit value 2025 (proxy); low is ASSUMPTION"},
    # THB per pouch. Base: USD 0.03 to 0.05 per piece, MOQ 1,000, non-Thai listing (rework/53), DERIVED.
    # Low and high: USD 0.02 and 0.08 per piece from unverified supplier snippets (Global Sources, not opened).
    # No Thai or Asian converter price per 1,000 was found; this input is still open.
    "pouch_thb": {"base": 1.30, "low": 0.67, "high": 2.70,
                  "status": "DERIVED from a non-Thai listing (USD 0.03 to 0.05 per piece, MOQ 1,000); low and high are unverified supplier snippets; no Thai converter price found"},
    # THB per pouch. Print placeholder carried from rework/53. ASSUMPTION.
    "print_thb": {"base": 1.50, "low": 0.80, "high": 2.50, "status": "ASSUMPTION (placeholder)"},
    # THB per cube. Compaction, sealing, packing labour and energy. ASSUMPTION; no sourced figure.
    "processing_thb": {"base": 0.50, "low": 0.25, "high": 1.00, "status": "ASSUMPTION (no sourced figure)"},
    # THB per carton, by pack size. 12-pack base and high: HomePro retail asking THB 5 (10 or more) and THB 7
    # (single) for a 20 x 14 x 12 cm box (S, retail, not a bulk price). 6 and 24 are scaled ASSUMPTIONS; low is ASSUMPTION.
    "carton_thb": {6: {"base": 4.0, "low": 3.0, "high": 7.0},
                   12: {"base": 5.0, "low": 3.0, "high": 7.0},
                   24: {"base": 9.0, "low": 6.0, "high": 14.0}},
    # Price per cube at shelf, THB. Shelf reference: 330 mL can at THB 15 to 17 (rework/04, rework/53). ASSUMPTION for the cube.
    "shelf_thb_per_cube": {"low": 10.0, "base": 15.0, "high": 20.0, "status": "ASSUMPTION (cube not priced)"},
    # Share of shelf price kept by the producer at ex-factory (after retailer and distributor). ASSUMPTION.
    "ex_factory_share": {"base": 0.60, "low": 0.50, "high": 0.70, "status": "ASSUMPTION (no sourced margin)"},
}

# Carton outer volume per pouch: pouch flat footprint 90 mm by 70 mm by 20 mm contents, times a packing factor.
POUCH_VOL_M3 = 0.090 * 0.070 * 0.020
CARTON_PACK_FACTOR = 1.5               # carton wall and void space. ASSUMPTION.

# Shipping containers. Internal dimensions: SeaCube spec (S, 5,898 x 2,352 x 2,393 mm; Maersk and ONE agree
# within 2 mm). Payload: Maersk 20 ft 28,200 kg (P, gross 30,480 kg less tare 2,280 kg); ONE 40 ft 26,840 kg
# (P, gross 30,480 kg less tare 3,640 kg; the 40 ft gross rating is disputed across sources).
CONTAINERS = {
    "20ft": {"length_m": 5.898, "width_m": 2.352, "height_m": 2.393, "payload_kg": 28200.0},
    "40ft": {"length_m": 12.032, "width_m": 2.352, "height_m": 2.393, "payload_kg": 26840.0},
}
# Carton outer volumes. ASSUMPTION dimensions: 6-pack 190 x 150 x 50 mm, 12-pack 190 x 150 x 100 mm (3 layers of
# 4 pouches), 24-pack 380 x 150 x 100 mm. Single pouch uses pouch volume times the packing factor.
CARTON_DIMS_M3 = {1: POUCH_VOL_M3 * CARTON_PACK_FACTOR,
                  6: 0.190 * 0.150 * 0.050,
                  12: 0.190 * 0.150 * 0.100,
                  24: 0.380 * 0.150 * 0.100}
# Share of internal volume usable for cartons. 0.92 is calibrated to the sourced grid count of 10,764 twelve-pack
# cartons per 20 ft (S-derived; theoretical 11,647 at 100%). Stacking strength is not checked.
PACKING_EFFICIENCY = 0.92
CARTON_MASS_KG = 0.10                  # empty carton, mass. ASSUMPTION.
POUCH_MASS_G = 1.5                     # laminate pouch with seal and print, mass. ASSUMPTION (laminate ~96 g/m2, 0.0126 m2 two sides plus seal).


def reactant_grams(target_ph):
    """Reactant masses per 330 mL at 0.9 volume, from the desk model at 25 C serve (no ice)."""
    m = fdm.serve_model(serve_c=25.0, target_ph=target_ph)
    return {
        "khco3_g": m["khco3_g"],
        "citric_total_g": m["citric_total_for_target_g"],
        "citric_free_g": m["citric_free_for_target_g"],
        "potassium_mg": m["potassium_mg_per_serve"],
    }


def sucralose_mg():
    return fdm.sucralose_mg_per_serve(330.0)


def cost_per_cube(target_ph=3.5, pouch=None, carton_pack=None, khco3_mult=1.0, citric_mult=1.0):
    r = reactant_grams(target_ph)
    khco3_kg = r["khco3_g"] / 1000.0
    citric_kg = r["citric_total_g"] / 1000.0
    sucr_kg = sucralose_mg() / 1e6
    p = PRICES
    reactants = (khco3_kg * p["khco3_thb_per_kg"]["base"] * khco3_mult
                 + citric_kg * p["citric_thb_per_kg"]["base"] * citric_mult
                 + sucr_kg * p["sucralose_thb_per_kg"]["base"])
    pouch_cost = p["pouch_thb"]["base"] if pouch is None else pouch
    per_pouch = reactants + pouch_cost + p["print_thb"]["base"] + p["processing_thb"]["base"]
    return {"target_ph": target_ph, "reactants_thb": round(reactants, 3), "pouch_thb": round(pouch_cost, 3),
            "print_thb": p["print_thb"]["base"], "processing_thb": p["processing_thb"]["base"],
            "per_pouch_before_carton_thb": round(per_pouch, 3), "reactant_grams": r}


def pack_row(n, target_ph=3.5, pouch=None, shelf=None, carton_mult=1.0):
    base = cost_per_cube(target_ph, pouch=pouch)
    carton_cost = PRICES["carton_thb"][n]["base"] * carton_mult if n in PRICES["carton_thb"] else 0.0
    per_cube = base["per_pouch_before_carton_thb"] + carton_cost / n
    carton_vol = CARTON_DIMS_M3[n]
    shelf_price = PRICES["shelf_thb_per_cube"]["base"] if shelf is None else shelf
    ex_factory = shelf_price * PRICES["ex_factory_share"]["base"]
    cont = {}
    for name, c in CONTAINERS.items():
        vol = c["length_m"] * c["width_m"] * c["height_m"]
        cartons_vol = math.floor(vol * PACKING_EFFICIENCY / carton_vol)
        pouches_vol = cartons_vol * n
        carton_mass_kg = CARTON_MASS_KG if n > 1 else 0.0      # a single pouch has no outer carton
        mass_kg = pouches_vol * (base["reactant_grams"]["khco3_g"] + base["reactant_grams"]["citric_total_g"]
                                 + sucralose_mg() / 1000.0 + POUCH_MASS_G) / 1000.0 + cartons_vol * carton_mass_kg
        limited_by = "volume" if mass_kg <= c["payload_kg"] else "payload"
        pouches = pouches_vol if limited_by == "volume" else math.floor(c["payload_kg"] / (mass_kg / pouches_vol))
        cogs = pouches * per_cube
        revenue_ex = pouches * ex_factory
        cont[name] = {
            "cartons": cartons_vol if limited_by == "volume" else math.floor(pouches / n),
            "pouches": pouches,
            "limited_by": limited_by,
            "container_mass_kg": round(mass_kg, 1),
            "cogs_thb": round(cogs, 0),
            "revenue_ex_factory_thb": round(revenue_ex, 0),
            "gross_margin_thb": round(revenue_ex - cogs, 0),
            "gross_margin_pct": round(100 * (revenue_ex - cogs) / revenue_ex, 1),
        }
    return {"pack_size": n, "cost_per_cube_thb": round(per_cube, 2), "carton_thb": carton_cost,
            "carton_volume_m3": round(carton_vol, 6), "shelf_thb_per_cube": shelf_price,
            "ex_factory_thb_per_cube": round(ex_factory, 2), "containers": cont}


def sensitivities():
    out = {}
    base_pack = pack_row(12, target_ph=3.5)
    out["base_pack12_cost_per_cube_thb"] = base_pack["cost_per_cube_thb"]
    out["by_target_ph_cost_per_cube_thb_pack12"] = {
        str(ph): pack_row(12, target_ph=ph)["cost_per_cube_thb"] for ph in (3.0, 3.5, 4.0, 4.5)}
    out["by_pouch_price_thb_pack12"] = {
        str(pp): pack_row(12, pouch=pp)["cost_per_cube_thb"] for pp in (1.00, 1.30, 1.67, 3.00)}
    out["by_carton_multiplier_pack12"] = {
        str(m): pack_row(12, carton_mult=m)["cost_per_cube_thb"] for m in (0.6, 1.0, 1.5)}
    return out


def main():
    packs = [pack_row(n) for n in (1, 6, 12, 24)]
    # A single pouch sold alone has no carton; cost is per pouch.
    packs[0]["carton_thb"] = 0.0
    packs[0]["cost_per_cube_thb"] = cost_per_cube(3.5)["per_pouch_before_carton_thb"]
    result = {
        "design": "0.9 volume of CO2 per 330 mL, one cube per pouch; reactant masses from formulation_desk_model.py",
        "fx_thb_per_usd": round(FX_THB_PER_USD, 4),
        "prices": PRICES,
        "containers": CONTAINERS,
        "packing_efficiency": PACKING_EFFICIENCY,
        "pack_rows_target_ph_3_5": packs,
        "cost_breakdown_target_ph_3_5": cost_per_cube(3.5),
        "cost_breakdown_target_ph_3_0": cost_per_cube(3.0),
        "sensitivities": sensitivities(),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", OUT.name)


if __name__ == "__main__":
    main()
