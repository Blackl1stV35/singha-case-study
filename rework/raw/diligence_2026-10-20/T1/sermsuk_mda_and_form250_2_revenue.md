# Sermsuk PCL (SSC): revenue from its SET filings (Management Discussion and Analysis, FY2022 to FY2024) and the revenue structure table in its Form 250-2

Date read: 20 October 2026. Fiscal year ends 30 September. Unit: THB million. Consolidated (Sermsuk Public Company Limited and its subsidiaries). The documents are the English translations that Sermsuk filed.

Route: each PDF was fetched again at source on 20 October 2026 (WebFetch stored the binary file), and the text layer was extracted locally with PyMuPDF. The text below is as printed. The same documents were also saved by task T3 (`rework/raw/diligence_2026-10-20/T3/sermsuk_mda_fy2022_fy2023_fy2024_set_filings.md` and `sermsuk_form250_2_opinion_2024-10-08_extracts.md`); the numbers agree.

Tier: P (company filings with the Stock Exchange of Thailand and the Thai SEC). The three Management Discussion and Analysis letters (3 pages each) were read in full. The Form 250-2 document has 114 pages and was not read in full: pages 11 and 63 to 64 were read for this check, so the revenue structure table is P for those pages only.

## Management Discussion and Analysis letters (revenue paragraph, as printed)

| Fiscal year | Filed | URL | Printed sentence |
|---|---|---|---|
| FY2022 (to 30 Sep 2022) | 16 Nov 2022 | https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202211/22137968.pdf | "Revenue from sales and services of the Company was Baht 10,905 million, increased by Baht 1,287 million or 13.4% from the same period of last year" |
| FY2023 (to 30 Sep 2023) | 15 Nov 2023 | https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202311/0009NWS151120231852450901E.pdf | "Revenue from sales and services of the Company was Baht 12,371 million, increased by Baht 1,466 million or 13.4% from the same period of last year." It adds that est sales "grow higher than overall growth of carbonated beverage market and gained market share" (company statement). |
| FY2024 (to 30 Sep 2024) | 15 Nov 2024 | https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202411/0009NWS151120241815250070E.pdf | "Revenue from sales and services of the Company was Baht 13,153 million, increased by Baht 782 million or 6.3% from the same period of last year." It adds that est sales grew "higher than overall growth of carbonated beverage market in this year" (company statement). |

The totals include est and Crystal drinking water and the distributed brands. The letters give no carbonated split.

## Form 250-2 (opinion on the tender offer, 8 October 2024), section 1.4 "Revenue Structure", PDF page 11 (repeated in the adviser's section on PDF page 64)

- URL: https://capital.sec.or.th/webapp/corp_fin/datafile/TO/0009000333250-22024-10-08e01.pdf (the http address returned "Request Rejected"; the https address returned the PDF, 114 pages, 2.5 MB). English translation prepared by Sermsuk; the Thai version prevails.

Table as printed (THB million; years ended 30 September; "9-month" is 1 October 2023 to 30 June 2024):

| Item | FY2021 | % | FY2022 | % | FY2023 | % | 9M to 30 Jun 2024 | % |
|---|---|---|---|---|---|---|---|---|
| Revenue from carbonated soft drinks | 3,708.03 | 38.55 | 3,972.69 | 36.43 | 4,550.15 | 36.78 | 3,964.26 | 39.94 |
| Revenue from non-carbonated drinks | 5,910.46 | 61.45 | 6,932.16 | 63.57 | 7,820.88 | 63.22 | 5,962.28 | 60.06 |
| Total revenue | 9,618.49 | 100.00 | 10,904.85 | 100.00 | 12,371.03 | 100.00 | 9,926.54 | 100.00 |

- The totals agree with the Management Discussion and Analysis letters (10,905 and 12,371).
- The FY2024 carbonated line is not printed in the pages read (only the 9 month figure is).
- PDF page 64 (adviser's assumptions): other income includes "Profit from free beverage sales, as part of the manufacturing contract provided to ThaiBev, who owns the trademark". So the carbonated revenue is Sermsuk's own revenue from making and selling under a contract for the trademark owner, not est brand sales at the trademark owner's selling price.

## Reading (team)

- Sermsuk's carbonated soft drink revenue is a P figure for one company's own line: THB 4,550.15 million in the year to 30 September 2023. The table does not give a brand split, so the est share of this line is not stated.
- GotoManager (29 October 2023, S, `gotomanager_5234_2023-10-29_est_pepsi_history.md`) says PepsiCo ended the Serm Suk contract in 2012 and that Pepsi-Cola (Thai) Trading produced and distributed Pepsi in Thailand from 1 November 2012; it names no current Pepsi holder. Serm Suk is a ThaiBev group company now. Pepsi's Thai statements (Suntory PepsiCo Beverage (Thailand) Co., Ltd.) were not found by T1 or T3.
- Arithmetic on these lines is in `rework/screen/t1_market_size_reconcile.py` (results file `t1_market_size_reconcile_results.json`, key `sermsuk`).
