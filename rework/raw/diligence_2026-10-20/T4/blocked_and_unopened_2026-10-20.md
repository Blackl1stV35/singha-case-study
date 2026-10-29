# T4: pages that were blocked, empty or not opened, and what was not attempted (log written in the verifier round, 20 October 2026)

This file records what T4 could not read, so that nothing below is cited as sourced. The first T4 run kept no log; the entries below come from the first run's notes in record 68c section 11 and from the second-round attempts, and each says which. Where an entry comes only from the first run's notes, the response was not re-tested in the second round unless stated.

## Web search

- The shared web search budget for the run was used up. In the second round WebSearch returned "web search budget is used up" and no further discovery search could be made. WebFetch still worked. Discovery of local and craft lemon or lime brands therefore rests on aggregator pages opened by URL.

## Department of Business Development (DBD) statements: attempted or not

| Entity | What was tried | Result |
|---|---|---|
| Thai Drinks Co., Ltd. (marketer of est) | Second round: https://data.creden.co/search?key=ไทยดริ้งค์ (Creden, an aggregator of DBD data) | Empty results shell ("no data available"); the page loads its results by script, so no registration number or statement figure could be read |
| Thai Drinks Co., Ltd. | Second round: https://www.dataforthai.com/company/search?q=ไทยดริ้งค์ | HTTP 403 |
| Thai Drinks Co., Ltd. | The DBD data warehouse pattern https://datawarehouse.dbd.go.th/company/profile/5/<registration number> needs the registration number, which no page read gives | Not attempted (no number). The same pattern with another company's number returned HTTP 404 in task T3 (rework/raw/diligence_2026-10-20/T3/blocked_and_unopened_2026-10-20.md) |
| International Beverage Holdings Limited (Interbev) and Super Brands Company Pte. Ltd. | Not attempted. Both are named as non-Thai entities in the sources read (a Pte. Ltd. is a Singapore form; Interbev's place of registration was not read). A DBD statement would not apply | Not attempted |
| Oishi Group PCL | Not attempted in the second round. The company was delisted after the 2023 tender offer, and the first run found no public filing after delisting | Limit |
| Sermsuk PCL | DBD not needed: the SET MD&A filings were read (T3). T3 also opened the Creden page for the Pepsi bottler: revenue, profit and asset cells blank without login (T3 file spbt_ownership_and_jv_press_2017_2018.md section 7) | MD&A used instead (tier P) |

Plain statement for the record: DBD statements were attempted for Thai Drinks only, through two aggregators, and could not be opened. No DBD statement was read for any entity in this record.

## Company and retailer pages (first-run notes, with the second-round re-test result beside each)

| Page | Result recorded by the first run | Second round, 20 October 2026 | What it would have given |
|---|---|---|---|
| Lotus's online product search (https://www.lotuss.com/th/search/โซดา) | Returned an empty page shell | Re-tested: page title "ผลการค้นหา | Lotus's online" only, no product list | private-label drink list |
| Big C online search (https://www.bigc.co.th/search?q=โซดา) | HTTP 403 | Re-tested: HTTP 403 | private-label drink list |
| Tops online search (https://www.tops.co.th/th/search/โซดา) | HTTP 403 | Re-tested: HTTP 403 | private-label drink list |
| Makro search | Returned no product list | Re-tested with the guessed URL https://www.makro.pro/th/search?q=aro โซดา: HTTP 404, so this URL is not the Makro search route; the first run's search page had no products | aro drink list |
| BJC (Berli Jucker) company site | Bot check; not bypassed | Guessed investor URL https://investor.bjc.co.th/en/financial-highlights: HTTP 404; not re-tested further | filings of the Big C owner |
| Central Retail investor site | Not tried in the first run | Guessed URL https://investor.centralretail.com/en/financial-highlights: connection refused | filings of the Tops owner |
| CP Axtra financial highlights (https://www.cpaxtra.com/en/investor-relations/results-and-reporting/financial-highlights) | The document hub redirects the statements download to a third-party file host; the redirect was not followed | Opened: store and area statistics by year (stores 2,690 in 2023, 2,728 in 2024, 2,758 in 2025) are in the text; the sales, gross margin and net profit charts have no numbers in the text, and the page states no "consolidated" wording and no fiscal year end | filings of the Makro and Lotus's owner |
| Osotspa 56-1 One Report page | Viewer page with no text layer | fiscal year end statement, segment revenue |
| ThaiBev annual report 2024 (SGX PDF) | Over the tool's 10 MB limit | full segment detail (the SGX year-end announcements were read instead) |
| Osotspa financial highlights page | Opened (second round); no "consolidated" wording and no fiscal year end statement on the page | see osotspa_financial_highlights.md |

## Search snippets used only as leads (not opened, so UNVERIFIED)

- 7-Eleven online est Cola 6-can price THB 110 on the same day as the THB 138 read (snippet, not opened).

## Not attempted by design

- No form, account, registration or outside contact; no supplier or agency quote; no download of archives (the SEC statement downloads are zip files). Rule 5 of the task.
