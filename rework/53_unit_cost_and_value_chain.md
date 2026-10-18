# Unit cost and value chain: the lime cube against the 330 ml can (18 October 2026)

Status: desk arithmetic from public prices read on 18 October 2026. No quote was requested, no supplier was contacted, and nothing was downloaded or logged into. Every margin is an ASSUMPTION, because no public Thai distributor or retailer margin was found. Fixed costs are excluded.

Calculation: [screen/unit_cost_value_chain.py](screen/unit_cost_value_chain.py), results in [screen/unit_cost_value_chain_results.json](screen/unit_cost_value_chain_results.json).

## 1. Answer

**On variable cost, the cube clears the can's price. Whether it justifies the value chain is not yet shown.**

- A cube serving costs about **฿2.1 to ฿5.3** in ingredients, sweetener and pouch, against a **฿15 to ฿17** can. That is 14% to 35% of the can's shelf price.
- The break-even retail price is about **฿3 to ฿10 per serving**, depending on cost case and margins. That sits below the can.
- The cube's cost is driven by the pouch and print, not the chemistry. The pouch is ฿1.00 to ฿1.67 on a non-Thai listing, and the print is an unpriced placeholder.
- Three things are missing before a value-chain verdict: Thai input prices, the retailer and distributor margins, and fixed costs (tooling, registration, trademark, pouch minimums). Consumer value is also unevidenced (see [49](49_conversion_test_synthesis.md)).

## 2. Cube cost per serving (THB)

| Line | Low | High | Basis |
|---|---|---|---|
| Potassium bicarbonate, 2.58 g | 0.92 | 1.84 | US listing, USD 242 for 22.68 kg, converted at 33.46 THB/USD. High is 2x (ASSUMPTION) |
| Citric acid, 1.65 g | 0.19 | 0.23 | US listings, THB 115 to 142/kg (DERIVED) |
| Sweetener (sucralose), 0.01 to 0.10 g | 0.01 | 0.07 | Lazada TH listing THB 655/kg (LISTED). Dose is ASSUMPTION |
| Pouch, 70 x 90 mm PET/PE | 1.00 | 1.67 | USD 0.03 to 0.05 per piece, MOQ 1,000. Non-Thai listing, spec unconfirmed (DERIVED) |
| Print | 0.00 | 1.50 | ASSUMPTION placeholder. No public price found |
| Flavour and binder | not priced | not priced | About 0.9 g of the 5.2 g design mass (ASSUMPTION) |
| **Total per serving** | **2.12** | **5.32** | Excludes fixed cost, freight, duty, VAT |

Potassium bicarbonate and citric acid have no Thai baht price in the search results. The US prices are the basis.

## 3. Can, 330 ml

| Item | Value | Basis |
|---|---|---|
| Launch retail, 7-Eleven | THB 15 | LISTED (launch, March 2026) |
| Zero-sugar single cans, Tops | THB 16 to 17 | LISTED (online, 18 October 2026) |
| Zero-sugar multipacks | THB 8.5 to 21 per can | LISTED (online) |
| Aluminium metal only | about THB 1.0 | DERIVED (9.6 g at USD 3,102/t, LME 7 October 2026). Excludes can making, lacquer, liquid, CO₂, filling and freight |
| Converted can cost in Thailand | not found | Limit. Needs a can-maker quote, which is outside contact |

## 4. Value chain: what the brand keeps

Net to brand per serving = retail price × (1 − retailer margin) × (1 − distributor margin). The margins are ASSUMPTION, at 25% to 35% for the retailer and 10% to 20% for the distributor.

Mid case (retailer 30%, distributor 15%, factor 0.595):

| Cube retail price per serving | Net to brand | Contribution, low cost (2.12) | Contribution, high cost (5.32) |
|---|---|---|---|
| THB 10 | 5.95 | 3.83 | 0.63 |
| THB 15 | 8.93 | 6.81 | 3.61 |
| THB 20 | 11.90 | 9.78 | 6.58 |

Break-even retail price (mid margins): about **THB 3.6** at the low cost and **THB 8.9** at the high cost. Across the full margin range the break-even is THB 3.1 to THB 10.2.

## 5. Why the cube's cost case is real, and where it is weak

**Real:**
- The can's weight is about 340 g gross for 330 ml. The cube's design mass is 5.2 g, so the cube is roughly 60 times lighter per serving (DERIVED). Freight, shelf space and cold chain favour the dry cube. The cube needs no cold chain.
- The chemistry is cheap. The reactants and sweetener together are about THB 1 to 2 per serving.

**Weak:**
- The cost is mostly pouch and print, and both are unsourced in Thailand. A Thai pouch maker's 1,000-unit price at 70 x 90 mm is the missing input.
- Potassium bicarbonate is a commodity. Its price is not a moat.
- The cube's cost advantage is only a gain if the brand keeps it. Retailers and distributors take a share at the shelf, and the assumed margins are not sourced.
- Fixed costs are excluded. Tooling, registration, trademark, pouch minimums and marketing could exceed the per-serving contribution at low volume.
- Consumer value is unevidenced. The conversion synthesis in [49](49_conversion_test_synthesis.md) gives about a 1-point per-person gap, under assumed inputs. No consumer test has been run.

## 6. Judgement

- **Upstream unit cost: justified on variable cost.** At any retail price of THB 10 or more, the cube covers its variable cost under the assumed margins, and at THB 15 it covers it by a wide margin.
- **Value chain: not yet justified.** The margins are unsourced, the fixed costs are not modelled, and the consumer value has not been shown. A cube at THB 10 is thin at high cost. A cube at THB 15 leaves room, but whether a consumer will pay THB 15 for a dissolvable cube is unknown.
- **What would change the verdict:** a Thai pouch and print price; the Thai potassium bicarbonate and citric acid prices; one dated retailer or distributor margin (SET filing or channel table); a fixed-cost estimate; and a consumer price test.

## 7. Limits

- No public Thai distributor or retailer margin was found.
- No converted Thai can cost (beyond the metal) was found.
- The cube's input prices are US listings, not Thai prices.
- The pouch price is non-Thai and the spec is unconfirmed.
- Flavour, binder, freight, duty, VAT and fixed costs are excluded.
- The weight of the can and the cube is derived, not sourced.
