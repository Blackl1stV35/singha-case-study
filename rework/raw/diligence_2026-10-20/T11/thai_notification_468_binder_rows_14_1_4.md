# Thai Notification No. 468 (B.E. 2568), Annex 1: binder and filler candidates in category 14.1.4 (saved reading)

- Document: Ministry of Public Health Notification No. 468 (B.E. 2568), food additives, Annex 1 (บัญชีหมายเลข ๑, maximum levels by food category) and Annex 2 part 2 (บัญชีหมายเลข ๒ ส่วนที่ ๒, condition codes). Thai original.
- URL: https://food.fda.moph.go.th/media.php?id=840096266338836480&name=P468.pdf (839 PDF pages, 16,616,446 bytes, SHA-256 5BEB26FC87AE26A0E7FD0023549FCA0658BEB1FEEA8728F1A1803673FD8BFF7C, from the earlier extract rework/raw/moph_468_annex_flavoured_drinks_extract_2026-10-19.md).
- Local copy (outside the repo): D:\Downloads\moph_468_annex\P468.pdf, saved on 19 October 2026 by the earlier extract. It was opened read-only on 20 October 2026.
- Date read: 2026-10-20. Tier: P (regulator text, Thai). Status: SOURCED.
- Method: pages were rendered to images with PyMuPDF (90 dpi) and read by the reader. The PDF text layer is in a legacy encoding and does not decode, so every row below was transcribed from the page image. Printed page number = PDF page number minus 1. The Thai words in brackets are copied from the images; the English words are our translation (the notification gives English names only for the additive and the INS number).
- Column order in the annex: food category code, food category, maximum level (mg/kg), condition, year adopted (B.E.).

## 1. Rows read for category 14.1.4 (เครื่องดื่มแต่งกลิ่นรส, flavoured drinks)

| Additive (INS) | Maximum level | Condition | Year (B.E.) | Row on printed page (PDF page) | Header with functions on printed page (PDF page) |
|---|---|---|---|---|---|
| Mannitol (แมนนิทอล), INS 421 | quantum satis (ปริมาณที่เหมาะสม) | TH3 | 2566 | 417 (418) | 414 (415) |
| Isomalt (ไอโซมอลต์), INS 953, other name hydrogenated isomaltulose | quantum satis | TH3 | 2566 | 328 (329) | 326 (327) |
| Erythritol (อีริทริทอล), INS 968 | quantum satis | TH3 | 2566 | 254 (255) | 252 (253) |
| Maltodextrin (มอลโตเดกซ์ทริน), no INS number | quantum satis | none | 2559 | 413 (414) | 411 (412) |

## 2. Function lines in the headers (หน้าที่), our translation

- Mannitol: anticaking agent (สารป้องกันการจับเป็นก้อน), bulking agent (สารเพิ่มปริมาณ), humectant (สารทำให้เกิดความชุ่มชื้น), stabilizer (สารทำให้คงตัว), sweetener (สารให้ความหวาน), thickener (สารให้ความข้นเหนียว), and solvent or carrier (สารช่วยทำละลายหรือช่วยพา).
- Isomalt: anticaking agent, bulking agent, flavour enhancer (สารเพิ่มรสชาติ), glazing agent (สารเคลือบผิว), stabilizer, sweetener, thickener.
- Maltodextrin: solvent or carrier, emulsifier (อิมัลซิไฟเออร์), stabilizer, thickener, bulking agent.
- Erythritol: flavour enhancer, humectant, sweetener. No bulking agent, stabilizer or thickener class.
- The Thai FDA clarification of 468 (saved in binder_thai_418_rows_468_classes_and_price_proxy.md) defines bulking agent to include "filler" and stabilizer to include "binder" and "tablet binder". The three first additives therefore sit in classes that cover a tableting binder and filler. Erythritol does not.
- Neighbouring rows for mannitol: the same quantum satis level (no condition) for 14.2.1, 14.2.2, 14.2.4 to 14.2.7, 15.0 and 16.0 on printed page 417.

## 2a. Polyethylene glycol (checked because the brief names PEG 6000 as a soluble lubricant option)

- Polyethylene glycol (พอลิเอทิลีนไกลคอล), INS 1521, other names PEG and Macrogol. Row in category 14.1.4: maximum level 500 mg/kg, condition 127 (the level is calculated for the product as ready to drink), year 2561. Printed page 493 (PDF page 494). Header functions (our translation): antifoaming agent, solvent or carrier, emulsifier, glazing agent, thickener.
- Arithmetic (DERIVED, rework/screen/t11_sodium_results.json): drink mass about 0.334 kg, so the level allows at most about 167 mg of PEG per cube; 0.80 g would be about 2,400 mg/kg, 4.8 times the level. PEG can therefore be at most a small lubricant addition, not the binder and filler.

## 3. Condition TH3 (Annex 2, part 2, printed page 835, PDF page 836)

Thai: "สำหรับผลิตภัณฑ์เครื่องดื่มเกลือแร่ ต้องใช้ร่วมกับน้ำตาลตามชนิดและปริมาณที่กำหนดไว้ตามประกาศกระทรวงสาธารณสุขว่าด้วยเครื่องดื่มเกลือแร่"

Our translation: for electrolyte (mineral) drink products, the additive must be used together with sugar of the type and amount set in the Ministry of Public Health notification on electrolyte drinks.

Reading (DERIVED): TH3 applies only if the product is classed as an electrolyte drink. The submission does not claim that class (the class opinion is the Gate 1 question). The same code is already read for sucralose in the 19 October extract.

## 4. What this settles

- Mannitol, isomalt and maltodextrin are listed additives for flavoured drinks at quantum satis, not only processing aids or carriers. The mannitol header also lists a solvent or carrier function.
- This closes the 468 limit left open in the first version of record 74. The predecessor Notification 418 rows (saved in binder_thai_418_rows_468_classes_and_price_proxy.md) gave the same level, 2559, and are now corroboration only.
- Not read: other food categories, and the English edition (P468_EN.pdf).
