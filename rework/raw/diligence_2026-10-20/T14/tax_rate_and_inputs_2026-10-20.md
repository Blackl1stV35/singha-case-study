# T14 inputs that carry a source: tax rate and the record 75 basis (read 20 October 2026; tier corrected in the third pass)

## 1. Thai corporate income tax rate (Revenue Department)

- URL: https://www.rd.go.th/english/6044.html
- Page title: Corporate Income Tax, The Revenue Department (English Site)
- Date printed on the page: "Last updated: 23.11.2020"
- Date read in T14: 20 October 2026 (WebFetch, read again in the third pass the same day). The tool returns a model-written answer, so the text below is an extract with the short phrases as returned, not the page in full. Also read twice in T12; the T12 extract is saved at rework/raw/diligence_2026-10-20/T12/revenue_dept_corporate_income_tax_and_dividend_rule_2026-10-20.md.
- Tier: S (primary-origin page, read through a page summary). Appendix A reserves P for text read in full, so this is not P. This matches record 75 (sections 7 and 8, conflict 19) and the T12 note. The earlier label "P (extract)" in the first revision of this note was a tier upgrade and is withdrawn.
- Phrase as returned (third-pass read): "The corporate income tax rate in Thailand is 20 % on net profit (accounting periods 2015)".
- Loss rule as returned (third-pass read): "Net losses carried forward from the last five accounting periods"; the returned summary was that losses can be carried forward for five accounting periods. The same read said the rates vary by taxpayer type.
- Use in T14: the rate is fixed at 20 percent (a statutory rate, no prior). What is uncertain is the structure (same-year loss offset against other group profit and a depreciation shield in record 75; no relief in variant C; a five-year carry-forward in variant D_cf). All three are modelled and reported.

## 2. Record 75 basis (read from the repo, not from the web)

- File: rework/screen/value_accrual_model_results.json (written by rework/screen/value_accrual_model.py, record 75).
- After-excise contribution THB 3.9444 per cube (key contribution_bases.after_excise_thb); before-excise contribution THB 4.91; can net-to-listing chain ratio 0.535628 (key contribution_bases.chain_ratio_can_net_to_listing); can contribution before aluminium THB 4.127 (record 70 section 2.11, can_cost_model_results.json). The can contribution is on the after-excise basis.
- After-tax NPV at 200,000 cubes, THB 500,000 fixed cost, 10 percent, year 1 at half volume, no cannibalisation: THB 165,023.77 (key base_case.after_excise.0.0.npv_after_tax_at_base_rate_thb). T14 reproduces this value from its own cash-flow code and the script asserts the match.
- Tier: DERIVED (S inputs); the chain ratio is a secondary-sourced derivation in record 70.

## 3. Store context for the store-equivalent count (read from the repo, not from the web)

- File: rework/submission/04 (line 37): "About 15,945 7-Eleven stores at end-2025, read as Thailand-only by inference" (tier P, SOURCED there, source 13). Not re-opened in T14; the figure is quoted as context only.
- Arithmetic (DERIVED): 1,282 store-equivalents is 8.0 percent of 15,945 (1,282 / 15,945 = 0.0804). The 1,282 itself is back-solved so that 3 units a store a week equal 200,000 cubes a year (52 x 1,282 x 3 = 199,992); it is an ASSUMPTION, and the 8 percent is context, not a derivation.
