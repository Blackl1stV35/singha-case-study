# OIE access log (Office of Industrial Economics, Thailand; 20 October 2026; corrected in the V7 revision)

Item: V7.

Correction note (20 October 2026, revision). The first version of this log said the OIE statistics table pages were "not located" and that the OIE statistics portal was not opened. That was wrong as a statement of reachability. The home page returns HTTP 400, but sub-pages of oie.go.th load with WebFetch. The statistics page https://www.oie.go.th/view/1/statistics/TH-TH loads and links a per-product Excel file and a CSV file. See oie_statistics_page_2026-10-20.md. The files were not downloaded.

## 1. OIE home page: returns HTTP 400

- WebFetch https://www.oie.go.th: "The server returned HTTP 400 Bad Request." The response body was not retrieved.
- WebFetch http://www.oie.go.th/: HTTP 400 Bad Request.
- WebFetch https://www.oie.go.th/: HTTP 400 Bad Request.
- Built-in browser navigation to https://oie.go.th: "navigation to https://oie.go.th was denied or failed".
- Result: the home page did not load. This is a fact about the home page only.

## 2. OIE sub-pages: load with WebFetch

- https://www.oie.go.th/view/1/statistics/TH-TH: loaded on 20 October 2026. Title "สถิติอุตสาหกรรม" (Industrial Statistics). Links the Excel and CSV of per-product statistics, January 2021 to August 2026 (see oie_statistics_page_2026-10-20.md).
- https://www.oie.go.th/view/1/mpi/TH-TH: loaded on 20 October 2026. The Industrial Index page, which links to the statistics page above.
- https://www.oie.go.th/view/1/statistics/EN-US: loaded but returned only "Not have page." (no English content).
- The Excel and CSV files linked from the statistics page were not downloaded. A download needs the user's permission.

## 3. OIE publications: reached through search results and WebFetch

WebSearch with the domain filter oie.go.th returned OIE PDFs. These were opened with WebFetch. WebFetch saved each PDF as a binary copy. The text was then extracted with pdftotext from the saved copy, and the beverage passages were read from that text.

- Report on the Industrial Economics Status in October 2025: https://www.oie.go.th/assets/portals/1/files/monthly_report/en_briefOctober2025.pdf (see oie_brief_october_2025.md)
- Report on the Industrial Economics Status in 2025 and Outlook for 2026: https://www.oie.go.th/assets/portals/1/files/monthly_report/anualreport2025_outlookfor2026.pdf (see oie_annual_2025_outlook_2026.md)
- Report on the Industrial Economics Status 2024 and Outlook for 2025: https://www.oie.go.th/assets/portals/1/files/monthly_report/anualreport2024_outlookfor2025.pdf (see oie_annual_2024_outlook_2025.md)

Listed in search results, not opened: Q1/2025, Q2/2025, Q3/2025 and Q4/2024 quarterly reports, and the May, July and December monthly briefs (OIE PDF listings).

## 4. Thai-language search

A Thai-language search (สำนักงานเศรษฐกิจอุตสาหกรรม, มูลค่า การผลิต, เครื่องดื่ม, น้ำอัดลม, 2568) returned no OIE value page. It returned bank and press pages that cite OIE. The Thai search result did not name an OIE statistics page. The statistics page was not found by search. It was opened in the revision from its URL, which the reviewer gave, and the Industrial Index page (the mpi page) was confirmed to link to it.

## 5. What the OIE PDFs contain on this item

The OIE reports read give beverage production indices and volume statements. None of the three reports read gives a baht sales value for carbonated soft drinks. The sales-value series is used in a bank note that cites OIE (see lhbank_beverage_outlook_2026_03_26.md). The statistics page says its Excel and CSV files hold per-product sales value. That was not checked inside the files, which were not opened.
