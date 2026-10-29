# ThaiNamthip Corporation PCL (TNCC): SEC filing, Part 1 Executive Summary, Version 2 (includes the six months to 30 June 2025)

- URL: https://market.sec.or.th/public/ipos/IPOSGetFile.aspx?TransID=691644&TransFileSeq=299 (Thai; 29 pages; PDF creation date in the file metadata 2 October 2025). This is the later version of the filing whose Version 1 is saved in `tncc_sec_draft_prospectus_exec_summary.md`.
- Date read: 20 October 2026. Route: the PDF was fetched again at source (WebFetch stored the binary file, 2.3 MB), and the text layer was extracted locally with PyMuPDF. The text layer of Version 2 keeps the Thai characters. Another task (T2) saved extracts of the same pages in `rework/raw/diligence_2026-10-20/T2/tncc_sec_filing_v2_exec_summary_extract.md`; the numbers agree.
- Pages read in this check: 7, 8, 18, 19, 22, 23, 24 and 26 (Part 1 page numbers equal PDF page numbers). All 29 pages were searched by keyword for any value of the Thai carbonated soft-drink market in baht: none is printed. The only market values are the Frost and Sullivan NARTD forecast (CAGR 7.4 percent to THB 337.6 billion by 2029) and the shares below. The filing was not read in full.
- Tier: P as filed, for the pages read (company filing at the Thai SEC). The 51.4 percent is a Frost & Sullivan statistic quoted in the filing, so it carries a third-party basis that the filing does not describe.
- The final prospectus (the Securities and Exchange Commission approved the filing on 23 July 2026 according to Marketeer, 25 July 2026, https://marketeeronline.co/archives/478955) was not opened: the filing index page (https://market.sec.or.th/public/ipos/IPOSViewDetail.aspx?TransID=691644) redirected to a document-storage address that was not followed, and no later file address is known. Full-year 2025 revenue for TNCC was therefore not read. The Marketeer article of 25 July 2026 prints revenue only up to 2024 (THB 41,314 million) and net profit THB 4,379 million (read through a page summary, not as saved text).

## Page 7: share and volume (Thai as printed, team translation)

- "จากข้อมูลของบริษัท ฟรอส์ท แอนด์ ซัลลิวัน (ไทยแลนด์) จำกัด ... เมื่อพิจารณาจากยอดขายในประเทศไทยสำหรับปีสิ้นสุดวันที่ 31 ธันวาคม 2567 ... บริษัทฯ ครองอันดับที่ 1 ในผลิตภัณฑ์ประเภทเครื่องดื่มอัดลม โดยมีส่วนแบ่งตลาดคิดเป็นร้อยละ 51.4" (From Frost & Sullivan data, considering sales in Thailand for the year ended 31 December 2024, the company ranks first in carbonated soft drinks with a market share of 51.4 percent.) Coca-Cola brand 47.9 percent of cola; Fanta and Sprite 66.0 percent of other flavoured carbonated drinks. The same figures appear in Version 1.
- "จำหน่ายเครื่องดื่มที่ได้รับอนุญาตให้จัดจำหน่าย ... รวม 400 ล้านยูนิตเคส 216 ล้านยูนิตเคส และ 181 ล้านยูนิตเคส ตามลำดับ" for the year 2024, the six months to 30 June 2024 and the six months to 30 June 2025 (all licensed beverages in the licensed area, in million unit cases). Version 1 printed 404 million for 2024; Version 2 prints 400.
- Frost & Sullivan expects the Thai NARTD market to grow at a CAGR of 7.4 percent from 2024 to 2029 to THB 337.6 billion (value of the whole NARTD market, not carbonated drinks).
- The text does not say whether 51.4 percent is by value or by volume, or whether it is TNCC alone or the Coca-Cola family across Thailand.

## Page 8: total revenue (as printed)

Total revenue (รายได้รวม) for 2022, 2023, 2024, six months to 30 June 2024 and 30 June 2025: THB 35,989.2, 39,295.0, 41,314.2, 21,528.7 and 18,330.2 million. Net profit margin 8.6, 8.6, 10.6, 9.6 and 5.2 percent.

## Page 19: results table (THB million, as printed)

| Line | 2022 | 2023 | 2024 | 6M 2024 | 6M 2025 |
|---|---|---|---|---|---|
| Revenue from sales of goods | 35,632.60 | 38,876.25 | 39,828.47 | 21,291.92 | 17,863.60 |
| Total revenue | 35,989.15 | 39,294.98 | 41,314.24 | 21,528.72 | 18,330.18 |
| Net profit | 3,083.24 | 3,374.41 | 4,379.08 | 2,069.93 | 958.51 |

## Page 22 to 23: first half of 2025 (Thai as printed, team translation)

- Page 22: revenue from sales of goods in the six months to 30 June 2025 was THB 17,863.6 million, down THB 3,428.3 million or 16.1 percent from THB 21,291.9 million; main causes stated: lower demand from the weather and the Thai economy, lower consumer spending and fewer tourists (company statement).
- Page 23: Coca-Cola brand revenue THB 10,872.7 million, down THB 1,873.1 million or 14.7 percent from THB 12,745.8 million; brand volume down 17 million unit cases or 16.1 percent; revenue per unit case up 1.4 percent. Other carbonated soft drinks revenue THB 5,080.2 million, down THB 1,284.8 million or 20.2 percent from THB 6,365.0 million; volume down 11 million unit cases or 22.0 percent. Drinking water (Namthip) THB 1,288.7 million, down 10.2 percent.
- Page 23 also says the retail price of large-pack carbonated drinks was raised in mid-2024.

## Page 24: full year 2024 and 2023 by product group (as printed)

Coca-Cola brand THB 24,060.0 million in 2024, up THB 789.4 million or 3.4 percent from THB 23,270.7 million; other carbonated soft drinks THB 11,609.2 million, down THB 51.2 million or 0.4 percent from THB 11,660.4 million. These agree with the Version 1 page 9 table.

## Derived (script: rework/screen/t1_market_size_reconcile.py, key `tncc_first_half`)

- Carbonated lines (Coca-Cola plus other carbonated soft drinks): 6M 2024 THB 19,110.8 million; 6M 2025 THB 15,952.9 million; change -16.5 percent (DERIVED). Total revenue change -14.9 percent. Unit cases 216 to 181 million, -16.2 percent.
- Full-year 2025 was not read. A half year is not doubled, because the first half holds the hot season.
