# Step 0: KPI thresholds and risk register

Status: proposed, rough. Inputs are in `data/assumptions.json`. Numbers marked "hand check" are my arithmetic on the base inputs; the financial model (step 4) recomputes them.

## Unit economics per 330 ml can (Singapore base, SGD)

| Step | Value | Basis |
|---|---|---|
| Shelf price incl. GST | 1.45 | FairPrice listing (dated, one read) |
| Ex-GST retail price | 1.33 | 1.45 / 1.09 |
| Importer buy price (after 30% retail margin) | 0.93 | assumption |
| Importer cost (after 25% importer margin) | 0.70 | assumption |
| CIF price ceiling (less handling 0.08 and BCRS deposit 0.10) | 0.52 | assumption and dated deposit |
| Exporter cost (ex-works USD 0.20, freight, insurance) | 0.34 | assumption |
| Gross contribution before trade spend | 0.18 | hand check |
| Net contribution after 10% trade spend | 0.12 (24% of CIF) | hand check |

## Unit economics per 355 ml can (Korea base, KRW, 0% tariff placeholder)

| Step | Value | Basis |
|---|---|---|
| Shelf price incl. VAT | 2,000 | GS25 list (dated) |
| CIF price ceiling | 805 | assumption; tariff unresolved |
| Exporter cost | 364 | assumption |
| Net contribution after 10% trade spend | 360 (45% of CIF) | hand check |

Break-even volume (fixed cost / net contribution per can) is about 3.6m cans a year in Singapore (about 0.9% of the category) and about 1.4m cans a year in Korea (about 0.24% of the category). Both category bases are rough, and the Korea figure is vendor-derived.

## KPI thresholds (go / no-go)

| ID | KPI | Threshold | Base case result (hand check) | Status |
|---|---|---|---|---|
| K1 | Net contribution per can as a share of CIF price | at least 20% | SG 24%, KR 45% (0% tariff), KR about 31% at 30% tariff | proposed |
| K2 | Break-even volume as a share of category volume | at most 1.0% | SG about 0.9% (tight), KR about 0.24% | proposed |
| K3 | Year-3 volume share against break-even | Year-3 share at least break-even share | SG base Year-3 share 0.6% (fails, needs about 0.9%); KR base 0.6% (passes) | proposed |
| K4 | Listing | at least 2 national gatekeepers listed within 6 months | not yet tested | proposed |
| K5 | Pilot velocity | at least 3 cans per store per week in listed stores | not yet tested; benchmark is an assumption | proposed, rough |
| K6 | Regulatory (binary) | sweetener and botanical ingredients permitted; registration route confirmed; labelling grade known | open (resolution runs) | must pass before commitment |
| K7 | Payback and NPV | NPV at 12% positive over 5 years, or payback within 4 years | model step 4 | proposed |
| K8 | Peak funding | at most S$1.0m equivalent | model step 4 | user to confirm |

K1 and K2 are the economic gates, K6 is the legal gate, and K4 to K5 are the demand gates. K3 links the volume ramp to the break-even test, so it is the most sensitive test.

## Risk register

Scores: likelihood (L) and impact (I) on 1 to 5. Score is L times I. Owner is to be assigned.

| ID | Risk | L | I | Score | Mitigation | Trigger (KPI) | Model input |
|---|---|---|---|---|---|---|---|
| R1 | Gatekeepers refuse listing | 4 | 5 | 20 | importer-led entry; pilot through independent retailers first | K4 | retailer margin, share ramp |
| R2 | Sweetener or botanical ingredient not permitted | 2 | 5 | 10 | resolve in G6 before reformulation; use a permitted sweetener | K6 (binary) | exit, not a parameter |
| R3 | Sparkling or zero-sugar demand below assumption | 3 | 4 | 12 | bear case; pilot velocity test before scale | K5, K3 | share ramp multiplier |
| R4 | Price pressure from Malaysian flavoured imports (73% of the Singapore flavoured lane) | 4 | 3 | 12 | price band; differentiate on botanical citrus | K1 | shelf price |
| R5 | Korea tariff higher than placeholder | 3 | 4 | 12 | resolve G2 tariff; price to tariff | K1 at 30% tariff | tariff rate |
| R6 | Freight rate volatility | 3 | 2 | 6 | contract rates for 6 months | K1 | freight per container |
| R7 | FX move (THB, SGD, KRW) | 3 | 3 | 9 | price in SGD or KRW; hedge larger orders | K1 | exchange rates |
| R8 | BCRS deposit cost falls on the importer | 3 | 2 | 6 | resolve mechanics in G6; price pass-through | K1 | BCRS deposit |
| R9 | Trademark conflict or non-registration | 2 | 4 | 8 | IPOS and KIPRIS record check before filing | K6 | none, gate |
| R10 | Upstream supply or co-packer capacity | 3 | 3 | 9 | partner or contract, not acquisition | K1 | ex-works cost |
| R11 | Group or brand consent constraint | 2 | 3 | 6 | confirm group governance; TCFF stays do-not-acquire | none | none |
| R12 | Sugar policy tightens and changes labelling or claims | 2 | 2 | 4 | Nutri-Grade on final recipe | K6 | none |
| R13 | Company-stated Korea figures do not hold | 4 | 3 | 12 | verify before commitment; the Korea case rests on them | K3 | Korea share ramp |

R13 is specific to this study. The company's Korea market and growth claims did not reproduce in the gate run, so the Korea volume ramp is only as good as its verification.

## Owner and review

Owners and review dates are not set. They are needed before any commitment, and they are a decision for you.
