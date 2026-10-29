# The Coca-Cola Company, group income statement FY2022 to FY2025, and Thailand and Schweppes statements

Task T2, read 20 October 2026. Route: WebFetch of SEC pages (model-written extract of tables). Tier P (SEC filings). Entity: The Coca-Cola Company, group, USD million, fiscal year ends 31 December.

## A. FY2025 and FY2024 (8-K exhibit 99.1, earnings release dated 10 February 2026)

- URL: https://www.sec.gov/Archives/edgar/data/21344/000162828026006642/a2025q4earningsreleaseex-9.htm

| USD million | 2025 | 2024 |
|---|---|---|
| Net operating revenues | 47,941 | 47,061 |
| Cost of goods sold | 18,397 | 18,324 |
| Gross profit | 29,544 | 28,737 |
| Operating income | 13,762 | 9,992 |
| Net income attributable to shareowners of The Coca-Cola Company | 13,107 | 10,631 |
| Net income (consolidated) | 13,137 | 10,649 |

## B. FY2023 and FY2022 (8-K exhibit 99.1, earnings release of February 2024)

- URL: https://www.sec.gov/Archives/edgar/data/21344/000002134424000004/a2023q4earningsreleaseex-9.htm

| USD million | 2023 | 2022 |
|---|---|---|
| Net operating revenues | 45,754 | 43,004 |
| Cost of goods sold | 18,520 | 18,000 |
| Gross profit | 27,234 | 25,004 |
| Operating income | 11,311 | 10,909 |
| Net income attributable to shareowners | 10,714 | 9,542 |
| Net income (consolidated) | 10,703 | 9,571 |

## C. Form 10-K for FY2025 (filed 2026), statements read in the MD&A and Item 1 extracts

- URL: https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm
- "Net operating revenues were $47,941 million in 2025, compared to $47,061 million in 2024." Gross profit margin 61.6% in 2025 and 61.1% in 2024.
- Asia Pacific segment: operating income USD 2,042 million (2025) against USD 2,156 million (2024); share of group net revenue 11.1% (2025) and 10.9% (2024); "unit case volume was even" in 2025 (worldwide concentrate sales volume +1%).
- Thailand: the 2024 other income discussion records "a gain of $506 million related to the sale of our ownership interest in an equity method investee in Thailand".
- Item 1 footnote: Schweppes "is owned by the Company in certain countries other than the United States". Item 1 lists Swire Coca-Cola Limited as a bottler with operations in Cambodia, Laos, Thailand and Vietnam among others.
- Not read: the full Item 8 statements (the fetch tool truncated the page); the two earnings releases above are used for the income statement.

## D. Derived ratios (computed in rework/screen/coca_cola_system_derived.py; see coca_cola_system_derived_results.json)

- Gross margin: FY2023 59.5%, FY2024 61.1%, FY2025 61.6%.
- Net margin (attributable net income over net operating revenues): FY2023 23.4%, FY2024 22.6%, FY2025 27.3%.
