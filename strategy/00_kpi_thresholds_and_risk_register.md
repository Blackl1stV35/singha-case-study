# Step 0: KPI thresholds and risk register (revised 2026-10-17)

Status: proposed, rough. Inputs are in `data/assumptions.json`, each with its status. Results are from `04_financial_model_results.md`. This revision replaces the earlier version, which used superseded inputs (a Singapore shelf price of S$1.45 from an unreproduced listing, and an importer-borne BCRS deposit).

## Unit economics (base, realised basis)

| Step | Singapore (S$ per 330 ml) | Korea (KRW per 355 ml) |
|---|---|---|
| Shelf price incl. tax | 1.50 (observed comparables S$0.82 to S$1.71) | 2,000 list (promotions lower it) |
| CIF price received by the exporter | 0.48 (realised bracket) | 528 (realised Thai unit value) |
| Exporter cost (ex-works, freight, insurance) | 0.34 | 387 |
| Net contribution after 10% trade spend | 0.09 (18% of CIF) | 88 (17% of CIF) |
| Back-solved importer ceiling (bull only) | 0.61 | 873 |

The BCRS S$0.10 deposit is a pass-through at checkout. The S$0.035 producer fee is an importer cost, and it sits inside the ceiling, not the realised price.

## KPI thresholds (go / no-go)

| ID | KPI | Threshold | Base result | Status |
|---|---|---|---|---|
| K1 | Net contribution as a share of CIF | at least 20% | SG 18% (fail), KR 17% (fail) | proposed |
| K2 | Break-even volume as a share of category volume | at most 1.0% | SG 1.25% (fail), KR 0.86% (pass) | proposed |
| K3 | Year-3 share at least break-even share | Y3 share at least break-even | SG 0.60% vs 1.25% (fail), KR 0.60% vs 0.86% (fail) | proposed |
| K4 | Listing: at least 2 national gatekeepers within 6 months | not tested; Korea listing is an extension of group presence, but the per-can fee is unverifiable | open | proposed |
| K5 | Pilot velocity: at least 3 cans per store per week | not tested; benchmark is an assumption | open | proposed, rough |
| K6 | Regulatory (binary): sweetener and botanical permitted; registration route; label grade; trademark and name clear | open. Singapore: botanical novel-food review (9 to 12 months), BCRS deposit mark from 1 October 2026, importer of record and IPOS ownership unverified. Korea: sweetener usage limits unverified, importer of record unverified, 소비기한 label, overseas plant registration | must pass before commitment |
| K7 | NPV at 12% positive over 5 years | SG -S$1.0m (fail), KR -S$0.1m (fail) | proposed |
| K8 | Peak funding at most S$1.0m equivalent | SG S$1.26m (fail), KR S$0.99m (pass) | user to confirm |

K1 is the economic gate. The base cases miss it by 2 to 3 percentage points, so the realised price decides the verdict in both markets. K6 is a legal gate that is still open in both markets.

## Risk register

Scores: likelihood (L) and impact (I) on 1 to 5. Score is L times I. Owners are not assigned.

| ID | Risk | L | I | Score | Mitigation | Trigger (KPI) | Model input |
|---|---|---|---|---|---|---|---|
| R1 | Realised price below the category unit value | 4 | 5 | 20 | price positioning; premium evidence before launch | K1 | realised CIF |
| R2 | Sweetener or botanical not permitted or needs review | 3 | 5 | 15 | check each named botanical; choose a permitted sweetener; novel-food review in Singapore | K6 | exit or delay |
| R3 | Gatekeepers refuse listing; Korea listing fee unverifiable | 4 | 5 | 20 | pilot through independent retailers; use existing group accounts in Korea | K4 | fixed cost, trade spend |
| R4 | Zero-sugar demand below assumption | 3 | 4 | 12 | bear case; pilot velocity before scale | K5, K3 | share ramp |
| R5 | Price pressure from Malaysian imports (73% of the Singapore flavoured lane) and crowded zero shelves | 4 | 3 | 12 | differentiate on botanical and sweetener choice | K1 | shelf price |
| R6 | Korean sugar levy on sugar-substitute drinks (draft up to 50 won per litre) | 2 | 3 | 6 | levy high case in the model; sweetener choice | K1 | levy |
| R7 | Korean importer of record unidentified | 3 | 4 | 12 | label read and 식품안전나라 record before commitment | K6 | none, gate |
| R8 | BCRS deposit mark required from 1 October 2026; producer role must be assigned | 3 | 4 | 12 | assign importer as producer; mark stock before shipment | K6 | producer fee |
| R9 | Freight rate volatility; no current container quote | 3 | 2 | 6 | forwarder quotes for two lanes | K1 | freight |
| R10 | FX move (THB, SGD, KRW) | 3 | 3 | 9 | price in SGD or KRW | K1 | exchange rates |
| R11 | Co-packer capacity or can-line capability in the group factories | 3 | 3 | 9 | verify can-line capability at group factories | K1 | exworks cost |
| R12 | Singapore IPOS ownership of SINGHA classes 32 and 30 unverifiable | 2 | 4 | 8 | direct IPOS search | K6 | none, gate |
| R13 | Company-stated Korea figures do not hold | 4 | 3 | 12 | not used; unverifiable; group sell-out data unavailable to the study | K3 | none (excluded) |
| R14 | Trade-data gap between Thai export and Singapore mirror values | 3 | 3 | 9 | bracket and sensitivity | K1 | realised CIF |
| R15 | Group perspective: intra-group shelf and portfolio overlap with Singha zero SKUs | 3 | 2 | 6 | noted; excluded from competitor set per the user | none | none |

## Owners and review

Owners and review dates are not set. They are needed before any commitment. This is a decision for the user.
