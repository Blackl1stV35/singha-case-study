"""Unit cost and value-chain sensitivity for the lime cube versus the 330 ml can (desk, 18 October 2026).

All prices are read on 18 October 2026 from public pages or derived from them. No quote was requested
and nothing was contacted. Every margin is an ASSUMPTION because no public Thai distributor or retailer
margin was found. The output is the arithmetic, not a finding about the market.

Cube per serving (one cube in 330 ml; reactant masses from rework/screen/effervescent_cube_screen and
rework/mockup/style_tokens.json: KHCO3 2.58 g, citric acid 1.65 g at 1.75 volumes):
  KHCO3 price  : USD 242 for 22.68 kg (US listing, search result) -> THB 357/kg (low); x2 for high (ASSUMPTION)
  citric acid  : THB 115/kg (low) and THB 142/kg (high), US listings converted (DERIVED)
  pouch        : USD 0.03 to 0.05 per piece, MOQ 1,000 (non-Thai listing, spec unconfirmed; DERIVED)
  print        : 0 (low) and THB 1.50 (high) per pouch (ASSUMPTION placeholder, no public price)
  sweetener    : sucralose THB 655/kg (Lazada TH listing, LISTED); dose 0.01 to 0.10 g (ASSUMPTION)
  unpriced     : flavour and binder (about 0.9 g of the 5.2 g design mass; ASSUMPTION, not priced)

Can side:
  retail       : THB 15 per 330 ml (launch, 7-Eleven, LISTED); zero-sugar single cans THB 16 to 17 (Tops, LISTED)
  metal only   : 9.6 g x USD 3,102/t = about USD 0.030, about THB 1.0 (DERIVED; excludes can making)

Value chain (ASSUMPTION throughout; no Thai margin was found):
  retailer margin r   : 25% and 35%
  distributor margin d: 10% and 20%
  net to brand per serving = P x (1 - r) x (1 - d)
  break-even retail P  = cost / ((1 - r) x (1 - d))
Fixed costs (tooling, registration, marketing, freight, duty, VAT) are excluded and must be added before any
conclusion about profit.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "unit_cost_value_chain_results.json")

FX = 33.4573  # THB per USD, XE mid-market, read 2026-10-18 13:24 UTC (cube-side research)

# Reactant masses per serving (grams), from the 1.75-volume design in the mockup spec
KHCO3_G = 2.58
CITRIC_G = 1.65
SUCRALOSE_G = {"low": 0.01, "high": 0.10}  # ASSUMPTION

KHCO3_LOW_THB_PER_G = 242.0 / 22.68 * FX / 1000.0  # USD 242 for 22.68 kg, US listing
KHCO3_THB_PER_G = {"low": KHCO3_LOW_THB_PER_G, "high": 2 * KHCO3_LOW_THB_PER_G}  # high = 2x (ASSUMPTION)
CITRIC_THB_PER_G = {"low": 115.0 / 1000.0, "high": 142.0 / 1000.0}
SUCRALOSE_THB_PER_G = 655.0 / 1000.0
POUCH_THB = {"low": 0.030 * FX, "high": 0.050 * FX}
PRINT_THB = {"low": 0.0, "high": 1.50}  # ASSUMPTION
CAN_RETAIL_THB = {"launch_330ml": 15.0, "zero_single_low": 16.0, "zero_single_high": 17.0}
CAN_METAL_THB = 9.6 / 1000.0 * 3102.0 / 1000.0 * FX  # USD 3,102/t, 9.6 g can

RETAILER = {"low": 0.25, "high": 0.35}      # ASSUMPTION
DISTRIBUTOR = {"low": 0.10, "high": 0.20}   # ASSUMPTION
RETAIL_PRICES = [10.0, 15.0, 20.0]          # THB per serving, a price grid for the cube (ASSUMPTION)


def cube_cost(case):
    ingredients = KHCO3_G * KHCO3_THB_PER_G[case] + CITRIC_G * CITRIC_THB_PER_G[case]
    sweetener = SUCRALOSE_G[case] * SUCRALOSE_THB_PER_G
    pack = POUCH_THB[case] + PRINT_THB[case]
    return {"ingredients": ingredients, "sweetener": sweetener, "pouch_and_print": pack,
            "total": ingredients + sweetener + pack}


def main():
    low = cube_cost("low")
    high = cube_cost("high")

    cost_grid = []
    for case_name, cost in (("low", low["total"]), ("high", high["total"])):
        for r_name, r in (("retailer_low", RETAILER["low"]), ("retailer_high", RETAILER["high"])):
            for d_name, d in (("distributor_low", DISTRIBUTOR["low"]), ("distributor_high", DISTRIBUTOR["high"])):
                factor = (1 - r) * (1 - d)
                cost_grid.append({
                    "cost_case": case_name,
                    "cost_thb": round(cost, 3),
                    "margins": f"{r_name}, {d_name}",
                    "retailer_margin": r,
                    "distributor_margin": d,
                    "break_even_retail_thb": round(cost / factor, 2),
                    "net_to_brand_at_retail_thb": {str(p): round(p * factor, 2) for p in RETAIL_PRICES},
                    "contribution_at_retail_thb": {str(p): round(p * factor - cost, 2) for p in RETAIL_PRICES},
                })

    result = {
        "basis": "desk arithmetic, 18 October 2026; all margins ASSUMPTION; fixed costs excluded",
        "fx_thb_per_usd": FX,
        "cube_cost_per_serving_thb": {"low": low, "high": high},
        "can": {"retail_thb": CAN_RETAIL_THB, "metal_only_thb": round(CAN_METAL_THB, 3)},
        "cost_to_retail_ratio_vs_can_15": {"low": round(low["total"] / 15.0, 3), "high": round(high["total"] / 15.0, 3)},
        "value_chain_grid": cost_grid,
        "weight_g": {"cube_design_mass_per_serving": 5.2, "can_330ml_gross_derived": 340.0},
        "limits": [
            "No public Thai distributor or retailer margin was found.",
            "No converted can cost (beyond the metal) was found in Thailand.",
            "Potassium bicarbonate and citric acid prices are US listings, not Thai prices.",
            "The pouch price is a non-Thai listing at unconfirmed spec.",
            "Flavour and binder are not priced. Fixed costs and freight are excluded.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    print("cube cost per serving (THB):")
    print("  low  ", {k: round(v, 3) for k, v in low.items()})
    print("  high ", {k: round(v, 3) for k, v in high.items()})
    print("can metal only (THB):", round(CAN_METAL_THB, 3))
    print("cube cost as share of THB 15 can:", result["cost_to_retail_ratio_vs_can_15"])
    print("break-even retail price range (THB per serving):",
          min(g["break_even_retail_thb"] for g in cost_grid),
          "to", max(g["break_even_retail_thb"] for g in cost_grid))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
