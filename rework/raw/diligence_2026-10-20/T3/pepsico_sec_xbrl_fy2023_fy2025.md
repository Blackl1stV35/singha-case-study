# PepsiCo, Inc.: revenue, gross profit and net income, FY2023 to FY2025, SEC XBRL (T3)

- Issuer: PepsiCo, Inc., consolidated (global group, not the Thai entity). SEC CIK 0000077476. Fiscal year ends on the last Saturday of December. Unit: US dollars.
- Source type: SEC XBRL company-concept data derived from the 10-K filings. Tier P (regulator database of the company's own filings).
- URLs read:
  - https://data.sec.gov/api/xbrl/companyconcept/CIK0000077476/us-gaap/Revenues.json
  - https://data.sec.gov/api/xbrl/companyconcept/CIK0000077476/us-gaap/GrossProfit.json
  - https://data.sec.gov/api/xbrl/companyconcept/CIK0000077476/us-gaap/NetIncomeLoss.json
- Date read: 20 October 2026. Access route: WebFetch; a small model listed the annual 10-K values from the JSON. This file holds that listing, not the raw JSON.
- The 10-K for FY2025 is the one the proposal already cites: https://www.sec.gov/Archives/edgar/data/77476/000007747626000007/pep-20251227.htm

## Revenues (10-K, annual)

| Fiscal year | Period start | Period end | Value (USD) | Accession | Filed |
|---|---|---|---|---|---|
| FY2025 | 2024-12-29 | 2025-12-27 | 93,925,000,000 | 0000077476-26-000007 | 2026-02-03 |
| FY2024 | 2023-12-31 | 2024-12-28 | 91,854,000,000 | 0000077476-25-000007 | 2025-02-04 |
| FY2023 | 2023-01-01 | 2023-12-30 | 91,471,000,000 | 0000077476-24-000008 | 2024-02-09 |

## GrossProfit (10-K, annual)

| Fiscal year | Period end | Value (USD) | Accession | Filed |
|---|---|---|---|---|
| 2025 | 2025-12-27 | 50,859,000,000 | 0000077476-26-000007 | 2026-02-03 |
| 2024 | 2024-12-28 | 50,110,000,000 | 0000077476-25-000007 | 2025-02-04 |
| 2023 | 2023-12-30 | 49,590,000,000 | 0000077476-24-000008 | 2024-02-09 |

## NetIncomeLoss (10-K, annual; the tag PepsiCo uses for net income attributable to PepsiCo)

| Fiscal year | Period start | Period end | Value (USD) | Accession | Filed |
|---|---|---|---|---|---|
| FY2025 | 2024-12-29 | 2025-12-27 | 8,240,000,000 | 0000077476-26-000007 | 2026-02-03 |
| FY2024 | 2023-12-31 | 2024-12-28 | 9,578,000,000 | 0000077476-25-000007 | 2025-02-04 |
| FY2023 | 2023-01-01 | 2023-12-30 | 9,074,000,000 | 0000077476-24-000008 | 2024-02-09 |

## Notes

- The tool noted that FY2024 and FY2025 are 52-week-style periods of 363 days and FY2023 is 364 days; all are full fiscal years.
- That NetIncomeLoss is the attributable-to-PepsiCo figure is our reading of the tag name; the 10-K statement itself was not opened in this task.
- The proposal already carries FY2025 margins of about 54.1% and about 8.8%; the script rework/screen/t3_pepsi_sermsuk_margins.py reproduces them (54.15% and 8.77%).
