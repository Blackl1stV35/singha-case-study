# Filings read for T5b financials, 20 October 2026

Access route: WebFetch for SEC pages and Nestle releases (page converted to text; a small model extracted the table; each section holds that extract). For the two Nestle financial-statement PDFs the tool saved the file locally, and the text layer was extracted with pdftotext (the columns come out interleaved; the reading was proved by arithmetic below). Date read: 20 October 2026.

## 1. The Coca-Cola Company, Form 10-K for the year ended 31 December 2025
- URL: https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/R3.htm (Consolidated Statements of Income, XBRL page of the 10-K; main document ko-20251231.htm). Tier P. USD million, years ended 31 December.
- Net operating revenues: 47,941 (2025); 47,061 (2024); 45,754 (2023).
- Cost of goods sold: 18,397; 18,324; 18,520. Gross profit: 29,544; 28,737; 27,234.
- Operating income: 13,762; 9,992; 11,311. Consolidated net income: 13,137; 10,649; 10,703.
- Net income attributable to shareowners of The Coca-Cola Company: 13,107; 10,631; 10,714.

## 2. PepsiCo, Inc., Form 10-K for the year ended 27 December 2025
- URL: https://www.sec.gov/Archives/edgar/data/77476/000007747626000007/R3.htm (Consolidated Statement of Income). Tier P. USD million; fiscal years ended 27 December 2025, 28 December 2024 and 30 December 2023.
- Net revenue: 93,925; 91,854; 91,471. Cost of sales: 43,066; 41,744; 41,881. Gross profit: 50,859; 50,110; 49,590.
- SG&A: 37,368; 37,190; 36,677. Operating profit: 11,498; 12,887; 11,986. Net income: 8,295; 9,626; 9,155.
- Net income attributable to PepsiCo: 8,240; 9,578; 9,074.

## 3. Prestige Consumer Healthcare Inc., Form 10-K for the year ended 31 March 2026
- URL: https://www.sec.gov/Archives/edgar/data/1295947/000129594726000016/R3.htm (Consolidated Statements of Income and Comprehensive Income). Tier P. USD thousand; years ended 31 March 2026, 2025 and 2024.
- Total revenues: 1,088,705; 1,137,762; 1,125,357. Cost of sales: 493,127; 503,299; 500,909. Gross profit: 595,578; 634,463; 624,448.
- Operating income: 309,409; 336,775; 342,429. Net income: 190,301; 214,605; 209,339.

## 4. Nestle S.A., Consolidated Financial Statements of the Nestle Group 2025 and 2024
- URLs: https://www.nestle.com/sites/default/files/2026-02/financial-statements-2025-en.pdf (2025 and 2024 columns) and https://www.nestle.com/sites/default/files/2025-02/financial-statements-2024-en.pdf (2024 and 2023 columns). Tier P. CHF million, years ended 31 December. Consolidated income statement (page 80 of the 2025 statements; page 79 of the 2024 statements).
- Sales: 89,490 (2025); 91,354 (2024); 92,998 (2023).
- Cost of goods sold: 48,694; 48,670; 50,328. Other revenue: 395; 366; 353. Distribution expenses: 7,306; 7,567; 7,765. Marketing and administration expenses: 17,883; 18,112; 17,549. Research and development: 1,613; 1,667; 1,656. Other trading income: 135; 124; 132. Other trading expenses: 1,849; 1,195; 1,665. Trading operating profit: 12,675; 14,633; 14,520.
- Profit for the year attributable to shareholders of the parent (net profit): 9,033; 10,884; 11,209. As a percentage of sales (printed): 10.1%; 11.9%; 12.1%.
- Nestle does not print a gross profit line. Gross profit in the record is sales minus cost of goods sold (our arithmetic). The reading of the interleaved columns is proved by the arithmetic: sales + other revenue - cost of goods sold - distribution - marketing and administration - research and development + other trading income - other trading expenses equals the printed trading operating profit in all three years (script rework/screen/analogue_price_per_serve_68e.py, key nestle_arithmetic_check).

## 5. Nestle full-year releases
- 2025: https://www.nestle.com/media/pressreleases/allpressreleases/full-year-results-2025 , 19 February 2026, P: sales CHF 89,490 million (2025) and 91,354 million (2024); organic growth 3.5% and 2.2%; underlying trading operating profit margin 16.1% and 17.2%; net profit CHF 9,033 million and 10,884 million.
- 2024: https://www.nestle.com/media/pressreleases/allpressreleases/full-year-results-2024 , 13 February 2025, P: sales CHF 91,354 million (2024) and 92,998 million (2023); net profit CHF 10,884 million and 11,209 million.
- Nestle Health Science in these releases: see nuun_hydralyte_2026-10-20.md, section A2.
