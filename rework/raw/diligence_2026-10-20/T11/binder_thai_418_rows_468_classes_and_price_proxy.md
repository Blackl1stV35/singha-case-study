# Binder and filler: Thai additive rows (Notification 418, Annex 1, category 14.1.4), 468 functional classes, and a price proxy (saved excerpt)

Date read: 2026-10-20 for all items.

## A. Notification No. 418 (B.E. 2563), Annex 1 (บัญชีหมายเลข ๑), read from rendered pages of the Thai PDF

- Source: https://exfood.fda.moph.go.th/law/data/announ_moph/P418.pdf (657 PDF pages, 3.9 MB; the text layer is partly readable, so rows were checked on rendered images). Tier P. Status: SOURCED for the rows named.
- The Thai FDA list of food-additive notifications (https://food.fda.moph.go.th/food-law/category/additives, read 20 October 2026) marks Annexes I and II of No. 418 as cancelled; Notification 468 (B.E. 2568) is listed as effective from 12 December 2568 (2025). The rows below are therefore the predecessor annex. The 468 rows were read on 20 October 2026 and are saved in thai_notification_468_binder_rows_14_1_4.md (they agree: quantum satis for mannitol, maltodextrin and erythritol; mannitol, isomalt and erythritol also carry TH3, electrolyte drinks only).

| Additive (INS) | Category 14.1.4 (flavoured drinks) | Maximum level | Condition | Year | Printed page (PDF page) | Functions in the header |
|---|---|---|---|---|---|---|
| Mannitol (421) | yes | quantum satis (ปริมาณที่เหมาะสม) | none | 2559 | 329 (330) | Header (printed 326, PDF 327): anticaking agent, bulking agent, humectant, stabilizer, sweetener, thickener (สารป้องกันการจับเป็นก้อน, สารเพิ่มปริมาณ, สารทำให้เกิดความชุ่มชื้น, สารทำให้คงตัว, สารให้ความหวาน, สารให้ความข้นเหนียว) |
| Erythritol (968) | yes | quantum satis | none | 2559 | 199 (200) | Header (printed 198, PDF 199): flavour enhancer, humectant, sweetener (สารเพิ่มรสชาติ, สารทำให้เกิดความชุ่มชื้น, สารให้ความหวาน) |
| Maltodextrin | yes | quantum satis | none | 2559 | 326 (327) | no function line read on the image |

Notes: Notification 418 Annex 1 rows for category 14.2 and 15 and 16 are also quantum satis for mannitol and erythritol (rendered page checks). The Thai FDA list of No. 418 says annexes I and II are cancelled; the 468 rows were read afterwards (see the pointer above).

## B. Notification No. 468 (B.E. 2568) Thai FDA clarification, functional classes (text layer, read in this run)

- Source: https://food.fda.moph.go.th/media.php?id=849894195891150848&name=468_FoodAdditives.pdf (788 KB, 36 pages, Thai with English class names in the text layer). Tier P. Status: SOURCED for the class names.
- Bulking agent: "bulking agent, filler" (line 227 of the text layer; the class is defined as adding volume without a significant effect on energy value).
- Stabilizer: "... stabilizer synergist, binder, Tablet binder" (lines 349 to 355).
- Thickener: "thickener, bodying agent, binder, texturizing agent, thickener synergist" (line 365).
- Carrier: "carrier, carrier solvent, nutrient carrier, diluent for other food additives, encapsulating agent" (lines 236 to 237), with "lubricant, granulation aid, glidant" (line 252).
- Sweetener: "sweetener, intense sweetener, bulk sweetener" (line 357).

## C. UN Comtrade, HS 290543 (mannitol), Thailand imports 2025, World, one row re-read in this run

- Request: https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=764&period=2025&cmdCode=290543&flowCode=M&partnerCode=0 (WebFetch). Date read: 2026-10-20. Tier P (UN Comtrade database; the fetch returned the JSON fields as an extraction).
- Fields returned: primaryValue 2095441.421 (CIF, USD), netWgt 476781.0 (kg), qtyUnitCode 8 (kilograms), cmdCode 290543, period 2025. One row.
- Unit value (DERIVED): 2,095,441.421 / 476,781 = USD 4.3947 per kg.
- Limits: a bulk import average, not a supplier price for a tableting grade; the premium is ASSUMPTION (1 to 3 times, as the team's comtrade record uses). Exchange rate: 33.5495 THB per USD (mid of buying sight and selling transfer, Bank of Thailand, 15 October 2026, repo file rework/raw/bot_fx_primary_2026-10-15.md, P).
- Derived THB per kg: about 147 (at 1 times) and up to about 442 (at 3 times). Per cube at 0.80 g: about THB 0.12 to 0.35.

## D. Effervescent literature read by the team's T11 literature record (not re-read in this run; full text reported by that record)

- Rosch M et al. (2021) Pharmaceuticals 14(12):1327, DOI 10.3390/ph14121327, PMC8707073: four saccharide fillers in a magnesium plus citric acid effervescent tablet (roller compaction). Mannitol gave the fastest disintegration (72 s, against maltose 238 s, dextrates 257 s, lactose 300 s). Mannitol tablets had the lowest crushing resistance (112.0 N at 40 kN) and the lowest tensile strength (0.865 N/mm); only dextrates tablets passed friability (0.72 percent). Mannitol granule mix showed no mass change up to 70 percent RH in dynamic vapour sorption; large uptake from 80 percent RH.
- Fontenele M et al. (2025) MATEC Web of Conferences (conference abstract, Roquette authors): mannitol solubility 0.25 kg per kg of water at 25 C.
- Ubeda A et al. (2009) Pharmacoepidemiol Drug Saf 18(5):417-9 (abstract): effervescent paracetamol at 3 g per day carried 74 mmol per day of sodium, mainly from bicarbonate and carbonate.
- Wikipedia entry on mannitol (S, read 20 October 2026): very low hygroscopicity, no water pick-up until about 98 percent RH; an osmotic laxative at oral doses above 20 g.

## Correction (20 October 2026)

- Section D above (the T11 literature items) is superseded by binder_evidence_rosch_isomalt_mannitol_solubility.md, where Rosch et al. 2021 was re-opened in full text, the 0.25 kg per kg mannitol solubility was dropped (conference abstract not opened; replaced by a PubChem value, S), and the Wikipedia statement is not used for any figure.
