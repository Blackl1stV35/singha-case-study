# 75. Value accrual to shareholders (task T12, slide 10 and submission 05), revision 2

Date: 20 October 2026 (revised twice after the independent verifier's reviews the same day). Read with rework/SOURCING_POLICY.md and rework/submission/appendix_a_tier_key.md. Team-only record. The judge-facing text is in section 7 (slide 10) and section 8 (submission 05); no judge-facing file was edited.

Model: rework/screen/value_accrual_model.py. Results: rework/screen/value_accrual_model_results.json. Both were rewritten and run in this revision (exit 0, 12 boolean checks and the inline assertions). The script asserts that the pre-tax NPV on the before-excise contribution reproduces project_valuation_results.json (880,796 THB, all 12 grid cells at three rates, the four break-even volumes, the base fixed-cost ceiling of 683,852 and the pre-tax sensitivity table), that the cash identity and the scale formula round-trip, that every break point is an exact zero of the NPV, that the cost of capital equals the policy rate plus the premium, that the same-year tax variant equals the base flow, and that the can's price chain reproduces its THB 7.393 net and the cube's THB 3.94.

Tier vocabulary: Appendix A reserves P for text read in full. The Bank of Thailand and Revenue Department pages were read through WebFetch page summaries, not in full, so they are tiered S in this revision (they were "P (extract)" before; see section 11, issue 6). Other tiers as in Appendix A. Figures in sections 7 and 8 are copied from the results file.

## 1. Answer in brief

- How much value accrues. At 200,000 cubes a year, THB 500,000 fixed cost, a 10 percent discount rate, five years, no terminal value, 20 percent Thai corporate income tax and no cannibalisation, the after-tax NPV is THB 0.17 million on the after-excise contribution of THB 3.94 a cube (the lead basis, on the same footing as the can). On the before-excise contribution of THB 4.91 a cube it is THB 0.68 million after tax and THB 0.88 million before tax (the figure now in the deck). Cumulative net profit over five years is about THB 0.44 million (after excise).
- The sign of that value is not robust. With no cannibalisation the NPV is zero at a contribution of about THB 3.64 a cube, THB 0.31 (7.8 percent) below THB 3.94. The unpriced binder and flavour, the assumed pouch, print and processing costs and the excise base each move the contribution by that much or more. The excise sensitivity already in submission 05 (THB 3.65) sits THB 0.015 above that edge.
- To whom. The profit is earned by the group company that sells the cube. The model books it in Singha Corporation as a stated assumption (the entity is a stated limit; group profit after 20 percent tax is the same wherever it is booked). If Boon Rawd Brewery holds all of Singha Corporation and Singha Corporation pays out all of the profit (both assumptions; neither was found), Boon Rawd Brewery receives about THB 151,000 a year in years 2 to 5 (THB 604,000 in all), and about THB 136,000 a year under the half exclusion. Each 10 percent stake in Boon Rawd Brewery would receive about THB 15,000 a year before holder tax (THB 13,600 after a 10 percent withholding rate for Thai individuals). Stakes were not found.
- When. Year 0 is the outlay of THB 500,000. Year 1 runs at half volume and loses about THB 164,000 after tax (no dividend). Years 2 to 5 earn about THB 151,000 a year. The outlay and the year-1 loss are recovered in the fourth year (undiscounted payback 3.25 years; discounted 3.95 years).
- Size. The steady-state incremental profit is about 0.005 percent of Singha Corporation's 2025 net profit of THB 3,085 million (S). The after-tax NPV is also about 0.005 percent of it (0.02 percent before excise; the deck's 0.03 percent is the before-excise, before-tax figure). These are single-company figures; consolidated group profit was not found, and Boon Rawd Brewery's 2022 net profit was 1.9 times Singha Corporation's 2025 figure, so every share against a wider base would be smaller.
- Break points (200,000 cubes, THB 500,000, 10 percent, after tax). The NPV is zero when 7.5 percent of cube buyers would otherwise buy a can. The 7.5 percent is approximate, because two unpriced items push it in opposite directions: the can contribution is taken before aluminium, so the loss per displaced can is overstated and the true figure is higher; and the cube's binder and flavour are not priced, so the cube's contribution is overstated and the true figure is lower. Neither is sized, so the net direction is not known. Before excise it is about 30 percent (30.9 percent if only the can bears excise; 30.3 percent if neither does). With no cannibalisation the NPV is zero at 184,325 cubes a year (148,076 before excise; 146,230 before tax and before excise, the deck figure), and the fixed-cost ceiling is THB 542,521 a year (THB 675,329 before excise; THB 683,852 before tax and before excise, the deck figure).
- Return. Steady-state return on the THB 500,000 setup is 30.2 percent a year after excise (61.1 percent before excise), against a cost of capital of 10 percent (8 to 12 percent): the Bank of Thailand policy rate of 1.00 percent plus a premium of 9 points (7 to 11) that is an assumption. The return falls to 10 percent at 15.3 percent cannibalisation, later than the NPV break-even because the NPV also carries the year-1 loss.
- Peer multiples (median trailing P/E 13.66 of four listed drinks companies, S, range 10.87 to 24.10) applied to the steady-state profit would imply about THB 2.1 million (1.6 to 3.6 million). That treats a five-year stream as permanent, so the NPV is the measure.
- Scale. Incremental profit equals 0.1 percent of Singha Corporation's 2025 net profit at about 1.13 million cubes a year with no cannibalisation (0.91 million before excise), 0.5 percent at about 5.04 million (4.05 million) and 1 percent at about 9.93 million (7.98 million). At 100 percent cannibalisation the after-excise project never reaches any of them.
- Pilot review level. The plan's current trigger (review at 50 percent or more of buyers saying they switched) sits far above the break-even. Section 5.12 gives the replacement: a review level of 7 percent of buyers saying they would otherwise have bought a can, with the mapping from a stated switch share to displaced cans.
- Verdict. At the base volume the cube is a learning option, not a value driver. Its value is small, can be zero or negative, and is positive only while few cube buyers would otherwise buy a can; the pilot measures that share and the volume, and can stop.

## 2. Structure from sources

Web search was not available in this revision (the turn's search budget is shared and was used up), so added sources were reached by direct page reads. All pages are saved under rework/raw/diligence_2026-10-20/T12/. Every WebFetch read returns a page summary, not the verbatim page.

| Entity or item | Fact read | Tier | Source, date read |
|---|---|---|---|
| Singha Corporation Co., Ltd. | Private limited company (บริษัทจำกัด); juristic number 0105544082625; registered 27 August 2001; registered capital THB 4,863 million; TSIC 64202 (holding company) | S | Creden company data page, read 20 Oct 2026 (aggregator; extract). creden_singha_corporation_0105544082625_2026-10-20.md; TSIC from T6/07 |
| Singha Corporation | "an important subsidiary of Boon Rawd Brewery"; Boon Rawd became the holding company after the 2000 reorganisation; reports to the Boon Rawd board; oversees management of Boon Rawd's subsidiaries. Page footer is 2014. | COMPANY CLAIM | Singha Corporation English About page, read twice 20 Oct 2026. singha_corporation_about_us_2026-10-20.md; ownership_second_read_2026-10-20.md |
| Singha Corporation | Thai Wikipedia describes it as founded in 2544 BE (2001) as the holding company that looks after all businesses in the Boon Rawd group. This differs from the About page's "subsidiary" wording | S | https://th.wikipedia.org/wiki/บุญรอดบริวเวอรี่, read 20 Oct 2026. ownership_second_read_2026-10-20.md |
| Singha Corporation | Percentage held by Boon Rawd Brewery: not found in any source read. Creden shows shareholder names and percentages behind a login. Boon Rawd's own "Our group" page lists 8 factories and 11 subsidiaries and does not list Singha Corporation. Wikipedia (English) lists Singha Corporation as a Boon Rawd subsidiary with no percentage. The Thaiger article calls it a subsidiary and gives no percentage | UNVERIFIED (stated limit) | ownership_sources_read_2026-10-20.md; ownership_second_read_2026-10-20.md |
| Singha Corporation | Neither company is listed on the Stock Exchange of Thailand: both carry the legal form "Co., Ltd." and only a public company can list (DERIVED). Two extended searches earlier on 20 Oct 2026 found no report of an IPO plan; the absence of news is not proof | DERIVED; S | Creden; T6/07 (listing section); record 69 row 16 |
| Singha Corporation | Revenue 2024 about THB 3,950 million, 2025 about THB 3,892 million; net profit 2024 about THB 3,135 million, 2025 about THB 3,085 million (year labels printed in the article); no source named in the article | S | MGR Online, 23 May 2026. mgronline_9690000048712_2026-05-23_extract.md |
| Singha Corporation | Revenue 2021 THB 4,226,639,742; net profit 2021 THB 3,590,700,760 | S | Thaiger, 18 Apr 2025 (T6/07). thaiger_1389992_group_financials_2026-10-20.md |
| Singha Corporation | 2022 and 2023: not found. Statements for 2564 to 2568 BE are listed by Creden as filed (amounts behind a login) | UNVERIFIED | Creden; T6/07 |
| Singha Corporation | Income: beverage licence fees, management fees and dividends from group companies (explains the 79 to 85 percent profit-to-revenue ratio) | S | MGR Online, same article |
| Singha Corporation | Dividend policy and payout ratio: none found. Creden gives "company value" (shareholders' equity) of THB 19,547,932,120 with no year, 401.97 percent of registered capital, which suggests earnings retained in the past | UNVERIFIED | Creden; unlisted, so no Form 56-1 or SEC filing (record 69) |
| Boon Rawd Brewery Co., Ltd. | Privately owned; founded 1933; managed by the 3rd and 4th generations of the founder's descendants; "over 50 affiliated companies" (the Singha Corporation page says it manages "more than 150"; the two company pages differ in scope) | COMPANY CLAIM | Boon Rawd About page (copyright 2020), read 20 Oct 2026. boonrawd_profile_2026-10-20.md |
| Boon Rawd Brewery | Private limited company, registration 0105476000061, TSIC 64202; equity THB 34,757,848,936 (no year); shareholder proportions behind a login; statements 2564 to 2568 BE listed with amounts empty; the aggregator's registered-capital figure (THB 600,000) looks like a unit error and is not used | S | Creden, read twice (T6/07 and 20 Oct 2026). ownership_second_read_2026-10-20.md |
| Boon Rawd Brewery | Revenue and net profit 2018 to 2022 (net profit 2022 THB 5,793 million; revenue THB 11,711 million); 2023 to 2025 not found | S | Thaiger, 18 Apr 2025. thaiger_1389992_group_financials_2026-10-20.md |
| Boon Rawd Brewery | Shareholders and stakes; dividend policy: not found in any source read. The Thaiger article credits the Bhirombhakdi family and says that in 2018 the Boon Rawd group and the family together held 68.5 percent of the BG group; it gives no breakdown for Boon Rawd | UNVERIFIED (stated limit) | ownership_sources_read_2026-10-20.md |
| Other group companies | Singha Estate, S Hotels and Resorts and BG Container Glass are SET-listed and are different companies from the beverage business | S | efinancethai, 12 Mar 2026, via T13/04. Not used for the beverage value |
| Thai corporate income tax | 20 percent on net profit | S (primary-origin page, read through a page summary) | Revenue Department page 6044, last updated 23 Nov 2020, read twice 20 Oct 2026. revenue_dept_corporate_income_tax_and_dividend_rule_2026-10-20.md. Forvis Mazars (20 Jan 2021, S) agrees |
| Dividends between Thai companies | Half excluded; full exclusion if the recipient is SET-listed or holds at least 25 percent of the distributing company's capital, with a 3-month holding rule before and after, and the proviso that the distributing company holds no interest in the recipient. The page's withholding table lists dividends at 10 percent and states no exemption for Thai-to-Thai dividends | S (same) | Same page |
| Dividends to individuals | 10 percent withheld at source where a Thai individual takes the separate-taxation option; otherwise included in assessable income with a 3/7 tax credit | S (same) | Revenue Department page 6045, last updated 21 Mar 2024, read 20 Oct 2026. Same saved file |
| Bank of Thailand policy rate | 1.00 percent, maintained unanimously at MPC Decision 4/2026, 26 August 2026 (press release 31/2026). Latest decision before 20 October 2026; the next meeting is listed for 28 October 2026 | S (primary-origin page, read through a page summary; second fetch asking for the verbatim text returned a summary with the same decision) | https://www.bot.or.th/en/news-and-media/news/mpc/news-20260826-KsecaE98.html. bot_policy_rate_press_release_31_2026_2026-10-20.md. Cross-check Trading Economics (S), also 1 percent. rework/raw/bot_fx_primary_2026-10-15.md holds USD counter rates only, no policy rate |
| Peer trailing P/E | Thai Beverage (SGX Y92) 10.87; Ichitan (SET ICHI) 13.65; Osotspa (SET OSP) 13.67; Carabao (SET CBG) 24.10; median 13.66. Forward 9.76, 13.21, 13.09, 16.55 | S | stockanalysis.com, prices as of 19 Oct 2026, read 20 Oct 2026. peer_pe_stockanalysis_2026-10-20.md. Serm Suk page returned 404; not read |

## 3. Inputs and tiers

| Input | Value | Tier and status | Basis |
|---|---|---|---|
| Cubes a year, steady state | 50,000 / 200,000 / 1,000,000 | ASSUMPTION | project_valuation.py scenario set |
| Year 1 share of volume | 50 percent | ASSUMPTION | project_valuation.py |
| Years | 5, no terminal value | ASSUMPTION | project_valuation.py |
| Fixed cash cost a year | THB 500,000 (grid 250,000, 1,000,000, 2,000,000) | ASSUMPTION | not sourced |
| Setup outlay (year 0) | equal to one year's fixed cost; depreciated straight line over 5 years | ASSUMPTION | convention |
| Cost of capital | 10 percent base (8 and 12 shown), kept from project_valuation.py; built as policy rate 1.00 percent plus a premium of 9 points (7 and 11) | policy rate S; premium ASSUMPTION; the 10 percent predates the build and the premium is back-solved to it | BOT press release 31/2026. The sourced rate supplies 1 of the 10 points |
| Cube contribution, after excise (lead) | THB 3.94 per cube (planning price 15 times the can's net-to-listing ratio 7.393 / 13.8025, less cube cost 4.09) | DERIVED on PROXY and ASSUMPTION inputs | can_cost_model_results.json; project_valuation_results.json; record 70 section 2.11. Inputs: listing prices (S), VAT (P), retailer margin (PROXY), distributor margin 10 to 20 percent (ASSUMPTION, unsourced), excise rate (P as saved; base not read), cube pouch and print costs (ASSUMPTION). Excludes binder and flavour |
| Cube contribution, before excise (deck basis) | THB 4.91 per cube (ex-factory 9.00 less cost 4.09) | DERIVED | project_valuation_results.json; the basis of the current deck and submission figures |
| Cube contribution, both products before excise on the can's chain (team record) | THB 5.25 per cube (invoice 9.34 less 4.09) | DERIVED on PROXY and ASSUMPTION inputs | used only to test the deck basis (section 5.1) |
| Can contribution before aluminium, after excise | THB 4.127 per can (upper bound on the loss; aluminium cost avoided not netted; no aluminium price used) | DERIVED on PROXY and ASSUMPTION inputs | can_cost_model_results.json; record 70. Inputs as for the cube plus non-aluminium cost (PROXY, US 2024 conversion cost, and ASSUMPTION bounds) |
| Can contribution before aluminium, before excise (team record) | THB 5.33 per can (invoice 8.60 less 3.266) | DERIVED on PROXY and ASSUMPTION inputs | test of the deck basis only |
| Cannibalisation | 0, 25, 50 and 100 percent of cube buyers; one can displaced per cube bought by a switcher | ASSUMPTION | task scenario set; displacement factor 0.5 and 1.5 shown as an illustrative range |
| Corporate income tax | 20 percent | S | Revenue Department page 6044 |
| Tax in a loss year | Same-year credit (base); carry-forward and no-relief variants shown | ASSUMPTION | Thai companies file separately; the carry-forward rule was not read |
| Singha Corporation net profit 2025 | THB 3,085 million, held flat | S | MGR Online. Single-company figure |
| Boon Rawd Brewery net profit 2022 | THB 5,793 million (larger denominator; different year) | S, PROXY | Thaiger. Single-company figure |
| Entity that books the profit | Singha Corporation | ASSUMPTION (stated limit) | the profit is earned by the group company that sells the cube |
| Boon Rawd share of Singha Corporation | 100 percent (upper bound) | UNVERIFIED | not found in any source read |
| Payout by Singha Corporation | 100 percent of positive incremental profit (high case); 50 percent alternative | ASSUMPTION | no policy found |
| Parent tax on the dividend | 0 percent under full exclusion, conditional on a holding of at least 25 percent, the 3-month rule and the cross-holding proviso, all unverified; 10 percent effective under half exclusion | S rule; CONDITIONAL | Revenue Department page 6044 |
| Boon Rawd payout to its holders | 100 percent | ASSUMPTION | no policy found |
| Holder-level tax | 10 percent, illustrative, for Thai individuals on separate taxation; holder type unknown | S rate; ASSUMPTION on holders | Revenue Department page 6045 |
| Peer P/E | median 13.66; range 10.87 to 24.10 (trailing, four companies) | S | stockanalysis |

## 4. Method

- Cash flow after tax: year 0 is minus the setup outlay. For years 1 to 5, incremental profit before tax is cube contribution times cubes, minus can contribution lost (share times one can per cube times cubes), minus fixed cost, minus depreciation of the setup outlay. Tax is 20 percent of that profit. In the base a loss year gives a same-year credit, as if the cube and the can were booked in one taxpayer. Thai companies file separately, so a credit works only against the booking company's own taxable profit; two variants bound the effect (section 5.9). After-tax cash flow is net profit plus depreciation.
- The pre-tax NPV without depreciation, on the before-excise contribution, reproduces the project_valuation.py base (880,796 THB). The after-tax NPV includes the depreciation tax shield.
- Share of Singha Corporation net profit: incremental net profit divided by THB 3,085 million, held flat. The cumulative share is the sum of years 1 to 5 divided by five years of the same figure. As a proxy, the steady-state profit is also divided by Boon Rawd's 2022 net profit.
- Dividends: payout times positive incremental net profit, received by Boon Rawd at the stated ownership, less the parent tax; passed to holders at the stated share. Holder amounts are per 10 percent stake because the stakes were not found.
- Equity value uplift: (a) NPV at the base rate; (b) peer min, median and max trailing P/E times the steady-state (year 2) incremental net profit.
- ROIC: steady-state (year 2) incremental net profit divided by the setup outlay of THB 500,000, compared with the cost of capital (policy rate plus premium). An upper bound: working capital and launch spending beyond the fixed cost are not modelled.
- Scale: the steady-state cube volume at which incremental net profit equals 0.1, 0.5 or 1 percent of the reference net profit. Closed form, checked by round trip.
- Break points: NPV is linear in volume, in fixed cost, in the cannibalised share and in the contribution per cube, so the zero points are exact.
- Bias: the can contribution is before aluminium, so the loss per displaced can is an upper bound, which lowers every cannibalisation break point. The cube contribution excludes binder and flavour (not priced), so it is an upper bound too, which raises every break point. The two are not sized and they offset in an unknown proportion, so the break points are stated as approximate and not as conservative.
- Three contribution bases are run. After excise (lead): cube and can both after excise. Before excise (deck basis): the cube at 4.91; at a cannibalised share above 0 it is netted against the can's after-excise contribution, which is the scenario in which the cube is outside the excise and the can is inside it (the cube's excise classification is not determined). Before excise on the can's chain (team record): both products on the can's invoice before excise (cube 5.25, can 5.33), used to test the deck basis.

## 5. Results

### 5.1 Base case, 200,000 cubes a year, THB 500,000 fixed cost, 10 percent (after tax unless marked)

After-excise contribution, THB 3.94 a cube (lead; can contribution THB 4.127, same basis):

| Cannibalised share | NPV after tax (THB) | NPV before tax (THB) | Steady-state incremental net profit (THB a year) | Steady share of 2025 Singha net profit | Cumulative share, years 1 to 5 | NPV as share of 2025 Singha net profit |
|---|---|---|---|---|---|---|
| 0 percent | 165,024 | 236,510 | 151,106 | 0.0049 percent | 0.0029 percent | 0.0053 percent |
| 25 percent | -385,723 | -451,923 | -13,974 | -0.0005 percent | -0.0020 percent | -0.0125 percent |
| 50 percent | -936,470 | -1,140,357 | -179,054 | -0.0058 percent | -0.0068 percent | -0.0304 percent |
| 100 percent | -2,037,963 | -2,517,224 | -509,214 | -0.0165 percent | -0.0164 percent | -0.0661 percent |

Before-excise contribution, THB 4.91 a cube (deck basis). At 0 percent the can does not enter and the row is a plain before-excise run. At 25, 50 and 100 percent it is the scenario in which the cube is outside the excise and the can is inside it:

| Cannibalised share | NPV after tax (THB) | NPV before tax (THB) | Steady-state incremental net profit (THB a year) | Steady share of 2025 Singha net profit | Cumulative share, years 1 to 5 | NPV as share of 2025 Singha net profit |
|---|---|---|---|---|---|---|
| 0 percent | 680,452 | 880,796 | 305,600 | 0.0099 percent | 0.0074 percent | 0.0221 percent |
| 25 percent | 129,705 | 192,362 | 140,520 | 0.0046 percent | 0.0025 percent | 0.0042 percent |
| 50 percent | -421,041 | -496,071 | -24,560 | -0.0008 percent | -0.0023 percent | -0.0136 percent |
| 100 percent | -1,522,535 | -1,872,938 | -354,720 | -0.0115 percent | -0.0119 percent | -0.0494 percent |

Both products before excise on the can's invoice chain (cube THB 5.25, can THB 5.33; team record, tests the deck basis):

| Cannibalised share | NPV after tax (THB) | NPV before tax (THB) | Difference from the deck-basis row, after tax (THB) |
|---|---|---|---|
| 0 percent | 863,041 | 1,109,032 | deck basis lower by 182,589 (the chain's invoice is 9.34, not 9.00) |
| 25 percent | 151,721 | 219,882 | deck basis lower by 22,016 |
| 50 percent | -559,598 | -669,268 | deck basis less negative by 138,557 |
| 100 percent | -1,982,238 | -2,447,567 | deck basis less negative by 459,703 |

Reading. The break-even share is 30.9 percent on the deck basis and 30.3 percent with both products before excise. At 25 percent the deck basis is a close read (THB 0.02 million lower); at 50 and 100 percent it flatters the NPV by THB 0.14 and 0.46 million. Judge-facing text therefore keeps only the 0 percent before-excise NPV (0.68 million, 0.88 million before tax) and the break-even stated as about 30 percent on either reading; it does not quote the before-excise NPV at 25, 50 or 100 percent.

NPV at 8 and 12 percent (after tax, 0 percent cannibalisation): after excise 210,416 and 123,438; before excise 755,739 and 611,383.

### 5.2 Who receives value and when (0 percent cannibalisation, after excise, 100 percent payout, 100 percent holding)

| Year | After-tax cash flow (THB) | Cumulative (THB) | Incremental net profit (THB) | Dividend declared and received by Boon Rawd (THB) | Per 10 percent stake in Boon Rawd, before holder tax (THB) |
|---|---|---|---|---|---|
| 0 | -500,000 | -500,000 | nil | nil | nil |
| 1 | -64,447 | -564,447 | -164,447 (same-year tax credit of THB 41,112 assumed) | nil | nil |
| 2 | 251,106 | -313,341 | 151,106 | 151,106 | 15,111 |
| 3 | 251,106 | -62,234 | 151,106 | 151,106 | 15,111 |
| 4 | 251,106 | 188,872 | 151,106 | 151,106 | 15,111 |
| 5 | 251,106 | 439,978 | 151,106 | 151,106 | 15,111 |

- Total dividend to Boon Rawd, years 2 to 5: THB 604,425 (THB 543,983 under half exclusion, 10 percent effective parent tax, THB 135,996 a year). Cumulative net profit years 1 to 5: THB 439,978. Undiscounted payback 3.25 years; discounted at 10 percent, 3.95 years.
- After the 10 percent holder withholding rate (illustrative), each 10 percent stake receives THB 13,600 a year.
- At 50 percent payout the dividend is half of these amounts. In the 25, 50 and 100 percent cannibalisation cases the steady-state profit is negative, so no dividend arises.
- Before-excise sensitivity: dividend THB 305,600 a year (total THB 1,222,400; half exclusion THB 275,040 a year); per 10 percent stake THB 30,560 before holder tax, THB 27,504 after the 10 percent rate; payback 2.2 years undiscounted, 2.5 discounted.

### 5.3 Equity value uplift (0 percent cannibalisation)

| Method | After excise | Before excise |
|---|---|---|
| NPV at 10 percent, after tax | 165,024 THB | 680,452 THB |
| Peer P/E median 13.66 times on steady-state profit | 2,064,111 THB | 4,174,496 THB |
| Peer P/E min 10.87 times (Thai Beverage) | 1,642,525 THB | 3,321,872 THB |
| Peer P/E max 24.10 times (Carabao) | 3,641,661 THB | 7,364,960 THB |

The P/E rows assume a stream with no end. The project runs five years with no terminal value, so the NPV is the measure in use. Peer multiples are of listed companies, not of Singha Corporation, and are trailing figures from an aggregator.

### 5.4 Return on invested capital against the cost of capital

- Steady-state return on the THB 500,000 setup outlay, 0 percent cannibalisation: 30.2 percent a year after excise (61.1 percent before excise). Average over years 1 to 5, which includes the year-1 loss: 17.6 percent after excise (45.4 percent before). Upper bounds.
- Cost of capital: 8, 10 and 12 percent (the policy rate of 1.00 percent plus 7, 9 and 11 points, the premium an ASSUMPTION). At the 10 percent base, the steady-state spread is plus 20.2 points after excise (plus 51.1 before excise).
- Cannibalised share at which the steady-state return equals the cost of capital: after excise 16.8, 15.3 and 13.8 percent at 8, 10 and 12 percent; before excise 40.2, 38.7 and 37.2 percent. The NPV break-even (7.5 percent after excise; about 30 percent before) is earlier on both bases, so the NPV is the stricter test of the sign of value.

### 5.5 Break points

| Break point | After excise | Before excise (deck basis) |
|---|---|---|
| Cannibalised share at which NPV is zero, after tax (200,000 cubes, THB 500,000, 10 percent) | 7.5 percent | 30.9 percent (cube outside excise, can inside); 30.3 percent with both before excise |
| Same, before tax | 8.6 percent | 32.0 percent |
| Same, after tax, at 8 and 12 percent | 9.0 and 5.9 percent | 32.4 and 29.3 percent |
| Same, after tax, at 50,000 and 1,000,000 cubes a year | none (negative even at 0 percent) and 78.0 percent | none, and above 100 percent (the NPV stays positive even at 100 percent cannibalisation); 84.9 percent with both before excise |
| Contribution per cube at which NPV is zero, after tax, 0 percent cannibalisation | THB 3.64 (THB 0.31 or 7.8 percent below 3.94) | the same value, THB 3.64 (a property of the cash flow); pre-tax THB 3.59 |
| Cannibalised share at which the contribution per cube sold equals the can's | 95.6 percent | 119 percent (never reached) |
| Cubes a year at which NPV is zero, after tax, 0 percent cannibalisation | 184,325 | 148,076 |
| Same, 25, 50, 100 percent | 249,618; 386,542; no positive volume | 187,469; 255,420; 928,548 |
| Same, before tax, 0 percent | 182,028 | 146,230 (the deck figure) |
| Fixed-cost ceiling at 200,000 cubes, after tax, 0 percent cannibalisation | THB 542,521 a year | THB 675,329 a year |
| Same, 25, 50, 100 percent | 400,612; 258,704; none | 533,421; 391,512; 107,695 |
| Same, before tax, 0 percent | THB 549,368 | THB 683,852 (the deck figure) |

All cannibalisation break points carry two offsetting biases (aluminium not netted from the can; binder and flavour not priced in the cube), so they are approximate. The break-even share also depends strongly on volume: it is 7.5 percent at 200,000 cubes a year, 78.0 percent at 1,000,000 and below zero at 50,000, so the review level in section 5.12 is re-read with the pilot's measured volume.

### 5.6 Scale: cubes a year for steady-state incremental net profit to reach a share of the reference net profit

Reference: Singha Corporation 2025 net profit, THB 3,085 million (S, a single-company figure).

| Share | 0 percent (after excise) | 25 percent | 50 percent | 100 percent | 0 percent (before excise) | 25 percent | 50 percent | 100 percent |
|---|---|---|---|---|---|---|---|---|
| 0.1 percent | 1,129,762 | 1,529,957 | 2,369,194 | none | 907,587 | 1,149,036 | 1,565,519 | 5,691,252 |
| 0.5 percent | 5,040,356 | 6,825,796 | 10,569,994 | none | 4,049,134 | 5,126,346 | 6,984,455 | 25,391,124 |
| 1 percent | 9,928,598 | 13,445,595 | 20,820,994 | none | 7,976,069 | 10,097,982 | 13,758,124 | 50,015,964 |

Proxy against Boon Rawd's 2022 net profit of THB 5,793 million (S, a different year, 1.9 times the Singha Corporation figure): 0.1 percent needs 1,987,938 cubes a year after excise (1,596,996 before excise), 0.5 percent needs 9,331,234 (7,496,181) and 1 percent needs 18,510,354 (14,870,163), with no cannibalisation. Steady-state profit is 0.0026 percent of that profit after excise (0.0053 percent before).

The base volume of 200,000 cubes gives about 0.005 percent of Singha Corporation's 2025 net profit at steady state after excise, a twentieth of the 0.1 percent threshold. The 1,000,000 cube scenario is just below 0.1 percent after excise (the model needs 1,129,762) and above it before excise (907,587).

### 5.7 Replacement grid for the deck's Appendix B and submission 05 (after tax, 10 percent, 0 percent cannibalisation)

NPV in THB million after tax, after-excise contribution (THB 3.94). Pre-tax and before-excise versions are in the results file under replacement_grid_for_deck_appendix_b_and_submission_05.

| Cubes a year | Fixed THB 250k | THB 500k | THB 1.0m | THB 2.0m | Maximum fixed cost for NPV = 0 |
|---|---|---|---|---|---|
| 50,000 | minus 0.44 | minus 1.41 | minus 3.35 | minus 7.24 | 0.14 |
| 200,000 (base) | 1.14 | 0.17 | minus 1.78 | minus 5.66 | 0.54 |
| 1,000,000 | 9.56 | 8.59 | 6.65 | 2.77 | 2.71 |

Cubes a year for NPV = 0, after tax, after excise: 92,162 at THB 250k; 184,325 at THB 500k; 368,649 at THB 1.0m; 737,299 at THB 2.0m. At THB 500,000 fixed cost the NPV in THB million is minus 1.41 at 50,000 cubes, 0.17 at 200,000, 3.32 at 500,000 and 8.59 at 1,000,000.

On the before-excise contribution after tax: base volume 1.65, 0.68, minus 1.26, minus 5.14; low minus 0.32, minus 1.29, minus 3.23, minus 7.11; high 12.13, 11.16, 9.22, 5.34; maximum fixed cost 0.17, 0.68, 3.38 (million).

### 5.8 Figures elsewhere that depend on the contribution basis

- Cubes needed to recover the paid-click cost of THB 1,150 for a first purchase: 234.2 at THB 4.91; 291.6 at THB 3.94.
- Stop-rule floor: the deck sets a contribution floor of THB 3.51 a cube (THB 4.91 less THB 1.40 for a THB 2.70 pouch). The same THB 1.40 rise on the after-excise basis leaves THB 2.54.

### 5.9 Tax treatment of a loss year (new in revision 2)

The year-1 loss before tax is THB 205,559 (after excise, no cannibalisation); the base takes a same-year credit of THB 41,112. NPV after tax at 200,000 cubes, 10 percent, after excise:

| Treatment | NPV (THB) | Change from base (THB) |
|---|---|---|
| Same-year credit (base) | 165,024 | none |
| Carried forward against the year-2 and year-3 profit (ASSUMPTION; the rule was not read) | 161,376 | minus 3,648 |
| Never used (no relief) | 127,649 | minus 37,374 |

In the cannibalised cases there is never a profit to set the loss against, so carry-forward and no relief coincide: the NPV falls by THB 66,200 at 25 percent, THB 203,887 at 50 percent and THB 479,260 at 100 percent against the base. The sign of the headline NPV does not change under either variant. Thai companies file separately; the base credit therefore works only if the cube loss falls in a company with other taxable profit (or the cube and the can are booked in one taxpayer), which is an ASSUMPTION.

### 5.10 Reconciliation of the 3.65 and 3.94 contributions (new in revision 2)

Submission 05 line 103 gives an excise sensitivity of THB 3.65 (the THB 4.91 before-excise contribution less THB 1.26, which is 14 percent of the assumed THB 9.00 ex-factory price; maximum fixed cost 508,000 pre-tax). The lead contribution of THB 3.94 takes the same 14 percent excise off the invoice that the can's chain gives for the same THB 15 shelf price: VAT 7 percent (P), retailer margin 21.6 percent (PROXY) and distributor margin 15 percent (ASSUMPTION) leave an invoice of THB 9.34 (62.3 percent of the shelf price), excise is THB 1.31, and the contribution is 9.34 minus 1.31 minus 4.09 = THB 3.94 (pre-tax maximum fixed cost 549,000). The gap of THB 0.29 is the difference between the two invoices (THB 0.34) after excise. Both rest on the same unverified excise base. Choice made: THB 3.94 is the lead; the 3.65 row is replaced by the chain row (section 8, replacement for line 103) and the reconciliation sentence goes into the excise limit (line 134).

### 5.11 Sensitivity table of submission 05 (lines 93 to 108) re-run on the lead basis (new in revision 2)

After tax, 200,000 cubes a year, 10 percent, 0 percent cannibalisation. Cost rows shift the lead contribution by the same THB amount as the pre-tax table; the shelf-price rows re-price through the can's chain. The ex-factory share rows (50 and 70 percent) and the excise row are replaced by the chain itself (invoice 62.3 percent of shelf, excise 14 percent of the invoice) and are not re-run. Maximum fixed cost is rounded to the nearest THB 1,000.

| Change | Contribution after excise (THB) | Maximum fixed cost, after tax (THB a year) | Status |
|---|---|---|---|
| Base case (6-cube carton, pH 3.5, 0.55 volume, shelf 15 THB, the can's price chain) | 3.94 | 543,000 | DERIVED on PROXY and ASSUMPTION inputs |
| Shelf 10 / 20 THB | 1.27 / 6.62 | 174,000 / 911,000 | ASSUMPTION |
| Pouch 0.67 / 2.70 THB (range) | 4.57 / 2.54 | 629,000 / 350,000 | UNVERIFIED |
| Print 0.80 / 2.50 THB | 4.64 / 2.94 | 639,000 / 405,000 | ASSUMPTION |
| Processing 0.25 / 1.00 THB | 4.19 / 3.44 | 577,000 / 474,000 | ASSUMPTION |
| Carton 1.50 / 3.50 THB per 6 | 4.36 / 4.03 | 600,000 / 554,000 | UNVERIFIED listing range, scaled |
| Target pH 3.0 (citric acid 3.70 g per cube) | 3.89 | 536,000 | DERIVED; pKa values S, UNVERIFIED |
| Pack: single pouch, no carton (flatters) | 4.61 | 635,000 | DERIVED |
| Pack: 12-cube carton (larger option) | 4.19 | 577,000 | DERIVED; carton PROXY |
| Pack: 24-cube carton | 4.24 | 584,000 | DERIVED; carton ASSUMPTION |
| All four packaging inputs at low | 5.94 | 817,000 | DERIVED; inputs UNVERIFIED or ASSUMPTION |
| All four packaging inputs at high | 1.13 | 155,000 | DERIVED; inputs UNVERIFIED or ASSUMPTION |

The pouch-high, print-high, processing-high and all-high rows fall below THB 500,000, so the NPV at the base fixed cost is negative in each. The lead case sits close to the edge.

### 5.12 Pilot review level for the cannibalisation question (new in revision 2)

- The current plan reviews cannibalisation at Phase 5 when 50 percent or more of buyers say they switched (ASSUMPTION; no source). At 50 percent the lead-basis NPV is already minus THB 0.94 million at 200,000 cubes a year, and the volume at which it returns to zero is about 386,500 cubes a year. The trigger sits far above the break-even of about 7.5 percent.
- Mapping from a stated switch share to displaced cans: displaced cans per cube = stated switch share times the cans lost per cube bought by a stated switcher (the displacement factor). The model sets the factor to 1 (ASSUMPTION): one cube is one 330 mL serve, the size of one can. If a switcher loses only half a can per cube, the stated share at which the NPV is zero is 15.0 percent; at one and a half cans it is 5.0 percent. A stated switch is a self-report: a buyer who says they switched may still buy cans, and a buyer who does not say so may still switch. The pilot's store sales, where available, set the factor.
- Proposed setting: review when 7 percent or more of cube buyers say they would otherwise have bought a can. The basis is the break-even of 7.5 percent at 200,000 cubes a year rounded down to a whole percent (DERIVED on ASSUMPTION inputs; NPV at 7 percent is +THB 11,000). The review reruns the model with the measured share, volume and contribution, because the break-even moves with all three; the Phase 6 scale gate becomes "the rerun NPV is positive" in place of "the cannibalisation review is passed or explained".
- The review is a value review, not a stop by itself. The plan stops short of scale when the rerun NPV is negative.

## 6. Value driver or learning option

- At the base volume the cube adds about 0.005 percent of one year's Singha Corporation profit on the lead basis (0.02 percent before excise, after tax; 0.03 percent before excise and before tax). It turns negative once more than about 7.5 percent of cube buyers would otherwise buy a can (approximate, with two offsetting unpriced items), and it is zero if the contribution is THB 0.31 lower.
- Incremental profit reaches 0.1 percent of Singha Corporation's 2025 profit only at about 1.1 million cubes a year with no cannibalisation (0.9 million before excise), about five times the base volume. The base case does not reach that scale on any source read.
- The pilot measures the stated switch share and the volume. Those two numbers decide the sign of the value, with the contribution. Until they are measured, the cube is a learning option.

## 7. Slide 10 text (finished; for the deck; not edited in this task)

Title: The cube adds little or no value, and only while it takes few sales from the Lemon Soda can.

Exhibit left: A bar chart of the after-tax NPV in THB million at 200,000 cubes a year, a fixed cost of THB 500,000 a year, a 10 percent discount rate and five years, against the share of cube buyers who would otherwise buy a can. At 0 percent the NPV is 0.17. At 25 percent it is minus 0.39. At 50 percent it is minus 0.94. At 100 percent it is minus 2.04. One marker on the 0 percent bar shows the NPV before excise, which uses a contribution of THB 4.91 a cube: 0.68.

Exhibit right, value drivers:
1. Contribution. The contribution is THB 3.94 a cube after excise, on the same basis as the can's THB 4.13 before aluminium. With no cannibalisation the NPV is zero at a contribution of about THB 3.64 a cube, only THB 0.31 (8 percent) lower, so the sign of the headline value is not robust. Before excise the contribution is THB 4.91 a cube.
2. Cannibalisation. The NPV is zero when about 7.5 percent of cube buyers would otherwise buy a can. The figure is approximate: the aluminium cost the can would have carried is not netted, which would raise it, and the cube's binder and flavour are not yet priced, which would lower it. If the cube were outside the excise, the figure would be about 31 percent while the can stays inside it, and about 30 percent if neither bore excise.
3. Volume. With no cannibalisation the NPV is zero at 184,325 cubes a year, and the base is 200,000. Before excise the figure is 148,076.
4. Fixed cost. With no cannibalisation the NPV stays positive up to THB 0.54 million a year at 200,000 cubes, and the model uses THB 0.5 million. Before excise the ceiling is THB 0.68 million.
5. Option. The pilot reads after 13 weeks of trading and can stop then. It asks buyers whether they would otherwise have bought a can. The review level is 7 percent, just under the break-even of 7.5 percent, and the model is rerun with the measured share, volume and contribution before any scale.

Exhibit right, how value reaches shareholders:
1. The profit is earned by the group company that sells the cube. The model books it in Singha Corporation, and the booking entity is a stated limit.
2. If Boon Rawd Brewery holds all of Singha Corporation and Singha Corporation pays out all of the profit, Boon Rawd Brewery receives about THB 151,000 a year in years 2 to 5, before any dividend tax, and about THB 136,000 a year if only half of the dividend is excluded from its taxable income. Year 1 is a loss year and pays no dividend. Neither the holding nor the payout was found in the sources read.
3. The shareholders of Boon Rawd Brewery then receive their share. Their stakes were not found in the sources read, so each 10 percent stake would receive about THB 15,000 a year before holder tax.
4. Incremental profit equal to 0.1 percent of Singha Corporation's 2025 net profit needs about 1.1 million cubes a year with no cannibalisation.

Scale note: Singha Corporation's 2025 net profit was about THB 3,085 million (MGR Online, 23 May 2026, S). It is a single-company figure. Consolidated group profit was not found, and Boon Rawd Brewery's 2022 net profit of THB 5,793 million (Thaiger, 18 April 2025, S) was 1.9 times it, so against a wider base the shares below would be smaller. The base-case after-tax NPV is about 0.005 percent of one year's profit, and the steady-state incremental profit is also about 0.005 percent of it. Before excise and before tax, the base-case NPV of THB 0.88 million is about 0.03 percent. Incremental profit reaches 0.1, 0.5 and 1 percent of that profit at about 1.1 million, 5.0 million and 9.9 million cubes a year with no cannibalisation (0.9, 4.0 and 8.0 million before excise).

Source line: Desk model on assumption inputs: five years, no terminal value, year 0 carries one year of fixed cost and year 1 sells half the base volume. Thai corporate income tax at 20 percent (Revenue Department, page last updated 23 November 2020, S), with the setup cost depreciated over five years; a loss year is taken as a same-year credit, and if the loss were only carried forward the NPV would be THB 0.16 million (assumption). The discount rate is 10 percent (assumption, kept from the earlier model); the Bank of Thailand policy rate of 1.00 percent (decision of 26 August 2026, S) is the base of that rate, and the premium of 9 points is an assumption. At 8 and 12 percent the NPV is 0.21 and 0.12 million. The contribution of THB 3.94 and the can contribution of THB 4.13 are DERIVED on PROXY and ASSUMPTION inputs. The can's is before aluminium, an upper bound on the loss, and the cube's binder and flavour are not yet priced, an upper bound on its contribution. A median trailing price-to-earnings ratio of 13.7 times (range 10.9 to 24.1; stockanalysis, 19 October 2026, S) would imply about THB 2.1 million (1.6 to 3.6 million) on the steady-state profit if it were permanent, so the NPV is used.

Takeaway: At the base volume the cube is a learning option, not a value driver. The value is small on every basis, can be zero or negative, and depends on how many cube buyers would otherwise buy a can. The pilot measures that share and the volume before any scale is considered.

Speaker note: Say that the value is small on every basis and that its sign is not robust: a THB 0.31 lower contribution makes it zero. It turns negative once more than about 7.5 percent of cube buyers would otherwise buy a can, and that figure moves with two costs not yet priced, the can's aluminium and the cube's binder and flavour, in opposite directions. Then say that the pilot measures that share, reviews at 7 percent, and can stop.

## 8. Shareholder value section for rework/submission/05 (finished text for the lead to place; not edited)

Note for the lead (not for the judges). This text replaces lines 79, 81, 83 and 87 of submission 05 (the opening paragraph, the base-case NPV paragraph, the fixed-cost paragraph and the "Value accrues to Singha Corporation" paragraph). Line 85, the pilot paragraph, stays, subject to conflict 10 (its last sentence hands a budget decision over). Line 103 of the sensitivity table is replaced as shown below the section. The same lines exist in rework/proposal/05_finance_and_project_valuation.md. The judge-facing text starts at the next paragraph and ends before "Replacement for line 103".

Shareholder value. The proposer is Singha Corporation Co., Ltd., a private limited company (registration 0105544082625, registered 27 August 2001, registered capital THB 4,863 million; Creden company data page, S, read 20 October 2026). Its own About page (footer 2014) describes it as an important subsidiary of Boon Rawd Brewery Co., Ltd., which became the holding company in a reorganisation in 2000 (COMPANY CLAIM). Thai Wikipedia (S) describes Singha Corporation as the holding company for the Boon Rawd group's businesses, and Boon Rawd Brewery's own Our group page does not list it, so the sources differ on how Singha Corporation sits in the group. Boon Rawd Brewery is also a private limited company (Creden, S). Neither company is listed on the Stock Exchange of Thailand: only a public company can list (DERIVED), and searches on 20 October 2026 found no report of an IPO plan, although the absence of news is not proof. The percentage of Singha Corporation held by Boon Rawd Brewery, the shareholders of Boon Rawd Brewery and any dividend policy were not found in the sources read.

Press reports (MGR Online, 23 May 2026, S, not checked against a filing) give Singha Corporation's total revenue as about THB 3,950 million for 2024 and THB 3,892 million for 2025, and its net profit as about THB 3,135 million and THB 3,085 million. The article attributes the high share of profit in revenue to beverage licence fees, management fees and dividends. A 2021 net profit of THB 3,590.7 million is reported by Thaiger (18 April 2025, S). No figure for 2023 was found. For Boon Rawd Brewery the latest figure found is a 2022 net profit of THB 5,793 million (Thaiger, S), and none was found for 2023 to 2025. Statements for 2564 to 2568 BE are listed by Creden as filed with the Department of Business Development, and the amounts were not reached. These are single-company figures, not consolidated group profit, which was not found; Boon Rawd Brewery's 2022 net profit was 1.9 times Singha Corporation's 2025 net profit, so shares of a wider profit base would be smaller. The scale test below uses Singha Corporation's 2025 net profit. No group cash flow is modelled; the profit figures serve only as a scale denominator.

The model applies Thai corporate income tax at 20 percent (Revenue Department, page last updated 23 November 2020; S, read through a page summary) and depreciates the setup outlay over five years. A loss year is taken as a same-year tax credit, which works only against taxable profit of the booking company or of a taxpayer that books the can as well (ASSUMPTION). If the year-1 loss were carried forward instead, the NPV would be THB 0.16 million, and if it were never used, THB 0.13 million (DERIVED). At 200,000 cubes a year, a fixed cost of THB 500,000 a year, five years and no terminal value, the discount rate is 10 percent (ASSUMPTION, kept from the earlier model). The Bank of Thailand policy rate of 1.00 percent, set on 26 August 2026 (S, read through a page summary), is the base of that rate, and the premium of 9 points is an assumption. The after-tax NPV is THB 0.17 million (DERIVED), using a contribution of THB 3.94 a cube after excise (the planning price of THB 15 less the same VAT, margins and excise as the can, less the cube cost of THB 4.09; DERIVED on PROXY and ASSUMPTION inputs), which is on the same basis as the can. On the before-excise contribution of THB 4.91 a cube used in the valuation tables above, the NPV is THB 0.88 million before tax and THB 0.68 million after tax. The incremental net profit is about THB 151,000 a year from year 2, after a loss of about THB 164,000 in year 1. That is about 0.005 percent of Singha Corporation's 2025 net profit (0.01 percent before excise). The cumulative net profit over the five years is about THB 0.44 million, and the setup outlay and the year-1 loss are recovered in the fourth year. With no cannibalisation the NPV is zero at a contribution of about THB 3.64 a cube, THB 0.31 (8 percent) below THB 3.94, so the sign of the headline value is not robust.

The value depends on how many cube buyers would otherwise buy a can of Singha Lemon Soda. Each such buyer costs the can's contribution of THB 4.13 before aluminium (DERIVED on PROXY and ASSUMPTION inputs; an upper bound, because the aluminium cost the can would have carried is not netted). At 25 percent the after-tax NPV is minus THB 0.39 million, at 50 percent minus THB 0.94 million and at 100 percent minus THB 2.04 million. The NPV is zero at about 7.5 percent. That figure is approximate: the aluminium cost the can would have carried is not netted, which would raise it, and the cube's binder and flavour are not priced, which would lower it. If the cube were outside the excise while the can stays inside it, the NPV would be zero at 30.9 percent, and if neither bore excise, at 30.3 percent. With no cannibalisation, the after-tax NPV is zero at 184,325 cubes a year (148,076 before excise), and the fixed-cost ceiling at 200,000 cubes is THB 0.54 million a year (THB 0.68 million before excise).

The pilot asks buyers whether they would otherwise have bought a can. A stated switcher is counted as losing one can for each cube bought (ASSUMPTION), so the stated share equals the model's cannibalised share; if a switcher loses half a can per cube the stated share at which the NPV is zero is 15.0 percent, and at one and a half cans it is 5.0 percent. The review level is 7 percent, just under the break-even of 7.5 percent (DERIVED on ASSUMPTION inputs). The review reruns this model with the measured share, volume and contribution, because the break-even moves with all three, and scale is considered only if the rerun NPV is positive.

Value reaches shareholders through a dividend chain. The profit is earned by the group company that sells the cube. The model books it in Singha Corporation as a stated assumption, and the booking entity is a stated limit; the group's profit after 20 percent tax is the same wherever it is booked. If Boon Rawd Brewery holds all of Singha Corporation (an upper bound, ASSUMPTION) and Singha Corporation pays out all of the profit (ASSUMPTION), Boon Rawd Brewery receives about THB 151,000 a year in years 2 to 5, about THB 604,000 in all. A dividend received from another Thai company is half excluded from taxable income, or fully excluded where the recipient holds at least 25 percent of the distributing company's capital, holds the shares for three months before and after the dividend, and the distributing company holds no interest in the recipient (Revenue Department; S, read through a page summary). Those conditions were not verified, so the half-exclusion case gives about THB 136,000 a year. If Boon Rawd Brewery passes the whole dividend to its shareholders (ASSUMPTION), each 10 percent stake would receive about THB 15,000 a year before holder tax, or about THB 13,600 after a 10 percent withholding rate for Thai individuals (Revenue Department; S; the type of holder was not found).

A peer multiple gives a second view. The trailing price-to-earnings ratios of four listed drinks companies are 10.87 (Thai Beverage), 13.65 (Ichitan), 13.67 (Osotspa) and 24.10 (Carabao), with a median of 13.66 (stockanalysis, 19 October 2026, S). Applied to the steady-state profit of THB 151,000, they imply an equity value of about THB 2.1 million (1.6 to 3.6 million). That treats the profit as permanent, whereas the project is modelled for five years with no terminal value, so the NPV of THB 0.17 million is the measure used.

The steady-state return on the setup outlay of THB 500,000 is about 30 percent a year after excise (61 percent before excise), against a cost of capital of 10 percent (8 to 12 percent). It is an upper bound, because working capital and launch spending beyond the fixed cost are not modelled. The return falls to the cost of capital when about 15 percent of buyers would otherwise buy a can. The NPV turns negative earlier, at 7.5 percent, because it also carries the year-1 loss.

Scale. Incremental profit reaches 0.1 percent of Singha Corporation's 2025 net profit at about 1.1 million cubes a year with no cannibalisation, 0.5 percent at about 5.0 million, and 1 percent at about 9.9 million. On the before-excise contribution the volumes are about 0.9, 4.0 and 8.0 million. With 25 percent cannibalisation the 0.1 percent volume is about 1.5 million cubes after excise, and with 50 percent it is about 2.4 million; at 100 percent it is never reached.

The project is therefore a learning option at the proposed scale, not a value driver. Its value is small, can be zero or negative, is positive only when few cube buyers would otherwise buy a can, and can be measured by the pilot, which reads after 13 weeks of trading and can stop. The figures are a desk estimate, not a forecast of profit, dividends or share price.

Limits. Not found in the sources read: the percentage of Singha Corporation held by Boon Rawd Brewery; the shareholders of Boon Rawd Brewery; any dividend policy or payout ratio; Singha Corporation's net profit for 2023; Boon Rawd Brewery's net profit for 2023 to 2025; consolidated group profit; and a Serm Suk multiple. Not determined: the entity that books the project profit (the model books it in Singha Corporation); the excise classification and base of the cube (the after-excise contribution uses the can's chain, which takes 14 percent off an invoice of THB 9.34 at the THB 15 shelf price; taking it off the assumed THB 9.00 ex-factory price would give a contribution of THB 3.65); and the withholding treatment of dividends between Thai companies (the Revenue Department table shows 10 percent, and the credit and exemption were not read). The premium over the policy rate and the tax treatment of a loss year are assumptions. The profit figures are press reports, not filings. The Bank of Thailand and Revenue Department pages were read through page summaries, not in full.

Notes for the lead (not for the judges). Replacement for line 103 of the sensitivity table (and removal of the two ex-factory share rows at line 97, which the can's chain replaces), as a table row:

Excise 14% of the invoice in the can's chain (invoice THB 9.34 at the THB 15 shelf price, excise THB 1.31 a cube; this is the base contribution of THB 3.94) | 3.94 | 549,000 pre-tax; 543,000 after tax | Rate P as saved (Source 1); base not read, ASSUMPTION

If the sensitivity table stays pre-tax and before excise as it stands, line 103 keeps its THB 3.65 and the excise sentence in the Limits paragraph above covers the difference. The full after-tax re-run of lines 93 to 108 is in section 5.11.

Sources to add to the Sources list of submission 05 (judge-facing; numbering continues from 13):
14. Revenue Department, Corporate Income Tax page (20 percent; dividend exclusion), last updated 23 November 2020, read 20 October 2026, through a page summary. S. https://www.rd.go.th/english/6044.html
15. Revenue Department, Individuals page (dividend tax credit; 10 percent separate taxation), last updated 21 March 2024, read 20 October 2026, through a page summary. S. https://www.rd.go.th/english/6045.html
16. Bank of Thailand, press release 31/2026, MPC Decision 4/2026, 26 August 2026, read 20 October 2026, through a page summary. S. https://www.bot.or.th/en/news-and-media/news/mpc/news-20260826-KsecaE98.html
17. Thaiger, 18 April 2025, Singha Corporation and Boon Rawd Brewery financial statements. S. https://thethaiger.com/th/news/1389992/
18. Creden company data pages for Singha Corporation (0105544082625) and Boon Rawd Brewery (0105476000061), read 20 October 2026. S. https://data.creden.co/company/general/0105544082625 ; https://data.creden.co/company/general/0105476000061
19. Singha Corporation, About us (footer 2014). COMPANY CLAIM. https://www.singhacorporation.com/en/about-us
20. Thai Wikipedia, Boon Rawd Brewery, read 20 October 2026. S. https://th.wikipedia.org/wiki/บุญรอดบริวเวอรี่
21. Peer trailing price-to-earnings ratios (Thai Beverage, Ichitan, Osotspa, Carabao), prices as of 19 October 2026, read 20 October 2026. S. https://stockanalysis.com/quote/sgx/Y92/statistics/ ; https://stockanalysis.com/quote/bkk/ICHI/statistics/ ; https://stockanalysis.com/quote/bkk/OSP/statistics/ ; https://stockanalysis.com/quote/bkk/CBG/statistics/

Replacement text for the cannibalisation review (judge-facing settings, for the files named in conflict 17):
- Plan wording: "Cannibalisation is reviewed at Phase 5 if 7% or more of buyers say they would otherwise have bought a Singha Lemon Soda can."
- KPI table row (submission 06 line 49): "Cannibalisation of the Singha Lemon Soda can | Share of cube buyers who say they would otherwise have bought a Singha Lemon Soda can (pilot exit question; store sales set the cans lost per cube). Review at 7% or more (DERIVED from the value model's break-even of 7.5% at 200,000 cubes a year, a contribution of THB 3.94 and a fixed cost of THB 500,000; ASSUMPTION inputs). The review reruns the value model with the measured share, volume and contribution."
- Risk table row (submission 10 line 136): "Cannibalisation | 7% or more of cube buyers say they would otherwise have bought a Singha Lemon Soda can | DERIVED on ASSUMPTION inputs | Value review: the value model is rerun with the measured share, volume and contribution"
- Scale gate (submission 10 line 116): replace "the cannibalisation review is passed or explained" with "the value model rerun with the measured switch share, volume and contribution gives a positive NPV".

## 9. Conflicts with the current deck and submission

1. Slide 10 as a whole (deck_content.md lines 142 to 151). The title, exhibits, drivers, scale note, source line and speaker note are replaced by section 7. The basis moves from before excise and before tax (NPV 0.88 million, break-even 146,230, ceiling 0.68 million, 0.03 percent) to after excise and after tax (0.17 million, 184,325, 0.54 million, 0.005 percent). Section 7 keeps the volume and fixed-cost drivers and the option line, which slide 11 and Appendix B depend on, and shows the before-excise figures once as a labelled sensitivity. The pre-tax before-excise figures stay in the results file.
2. Executive summary (deck_content.md line 29): "THB 4.91 contribution per cube; NPV THB 0.88 million at 200,000 cubes a year and THB 500,000 fixed cost". Replacement: "THB 3.94 contribution per cube after excise; after-tax NPV THB 0.17 million at 200,000 cubes a year and THB 500,000 fixed cost (desk model, assumptions)", or keep 4.91 and 0.88 with the words "before excise and before tax".
3. Slide 9 (deck_content.md lines 133 and 134): the title and exhibit state a contribution of THB 4.91 (before excise) and the superseded can variable cost of THB 4.94 (record 70 section 6 item 15 already asks for the replacement). Slide 10 now uses the can contribution of THB 4.13 from record 70, so slides 9 and 10 disagree on can economics until slide 9 is replaced, and slide 9 needs a one-line link: THB 4.91 before excise, THB 3.94 after excise.
4. Appendix B (deck_content.md lines 194 to 202): the NPV grid, maximum fixed cost and break-even volumes are before tax and before excise. The after-tax, after-excise replacement is in section 5.7; the before-tax versions are in the results file.
5. Submission 05: line 11 ("No group data is used") and line 79 ("no group data is used"): the scale test now uses Singha Corporation's reported profit as a denominator; replace with "No group cash flow is modelled; reported profit serves only as a scale denominator" (section 8 says this). Line 18 ("Method: pre-tax") and line 135 ("VAT, freight, cold chain, income tax, depreciation ... are excluded"): the lead valuation now carries 20 percent income tax and depreciation of the setup outlay; line 135 becomes "VAT enters only through the can's price chain; freight, cold chain, working capital and terminal value are excluded". Line 37 (contribution table), line 56 (cash-flow definition), lines 60 to 83 (valuation grid, break-even table, shareholder value paragraphs), line 83 (fixed-cost ceiling), lines 91 to 108 (sensitivities, see conflict 18), line 110 (234 cubes per customer; 291.6 at THB 3.94), line 140 ("it does not model how value passes to the shareholders of Boon Rawd Brewery", replaced by section 8, which models a stated chain under assumptions) and line 87 ("Value accrues to Singha Corporation. How it passes to the shareholders of Boon Rawd Brewery is not modelled", replaced by section 8). The same lines exist in rework/proposal/05_finance_and_project_valuation.md.
6. Submission 11 lines 78, 192, 224, 228 to 230 (contribution THB 4.91; NPV 0.88 million; break-even 146,230; 500,000 cubes 5.80 million; 1,000,000 cubes 13.99 million; ceiling 0.68 million) and the same lines in rework/proposal/11_mvp_situation_and_product_proposal.md. At THB 500,000 fixed cost the after-tax after-excise NPV is minus 1.41, 0.17, 3.32 and 8.59 million at 50,000, 200,000, 500,000 and 1,000,000 cubes.
7. Other uses of the THB 4.91 contribution and the THB 3.51 floor: submission 04 line 38, submission 06 lines 47, 50 and 59, submission 10 line 176, and the stop rules on deck slides 11 and 13. They are before excise. After excise the same cost rise leaves a floor of THB 2.54 and the paid-click recovery is 291.6 cubes instead of 234. Whether these move with the valuation is for the lead; if the valuation moves and they do not, the proposal carries two contribution bases.
8. Break-even wording. The deck and submission 05 state a break-even of 146,230 cubes; it is before tax and before excise. The same inputs give 148,076 after tax and 184,325 after tax and after excise. Record 70 section 2.12 gives a different measure (a steady-state, undiscounted break-even of 126,769 cubes, fixed cost divided by contribution); it is not the NPV break-even and must keep its label if quoted.
9. "Value accrues to Singha Corporation" (deck slide 10 scale note; submission 05 line 87). The profit is earned by the group company that sells the cube; section 7 and section 8 replace the sentence with the assumption and the limit.
10. The pilot paragraph in submission 05 (line 85) and slide 10 driver 4 end with "one budget still to be set (decision 9)", and line 85 says "Singha Corporation can stop it then". That hands a decision to Singha Corporation; record 76 section 3.6 converts such decisions into settings. Section 7 drops the clause; submission 05 still carries it.
11. Corporate tax tier. Record 56 (lines 88 and 195) tags the 20 percent tax as secondary because the Revenue Department was not reached. The page is now read through a page summary and tiered S in this record, so record 56's S stands; the primary page is named.
12. Year labels. Record 69 limit 15 and record 70 say the 2024 and 2025 net profit years were assigned by position. The MGR article prints 2567 BE and 2568 BE beside the figures. The press figures remain S and unchecked against a filing.
13. Policy rate. The task text says the Bank of Thailand policy rate is in rework/raw/bot_fx_primary_2026-10-15.md. That file holds USD counter rates only. The rate is read from the central bank's press release (1.00 percent, 26 August 2026), tiered S because the page was read through a summary.
14. Company pages differ. Singha Corporation's page says it is a subsidiary of Boon Rawd and manages "more than 150" companies. Boon Rawd's "Our group" page lists 8 factories and 11 subsidiaries without Singha Corporation, its profile says "over 50 affiliated companies", and Thai Wikipedia calls Singha Corporation the holding company for the group's businesses. The structure is therefore stated as a company claim with no percentage. Appendix A's entity convention ("Boon Rawd Brewery is the holding company") follows the About page and is not confirmed by the other two sources.
15. Stale comment in project_valuation.py (around line 210): it reads "9.00 - 3.90 = 5.10"; the results file holds cost 4.09 and contribution 4.91. The computed values are correct; only the comment is stale. Not edited.
16. Index. rework/README.md needs record 75 added (the index is the lead's file).
17. Cannibalisation review trigger (new). The plan reviews cannibalisation "if 50% or more of buyers say they switched": deck_content.md line 56 (proof bullet) and line 125 (note bar), submission 06 line 49 (KPI row, "Review at 50% or more (ASSUMPTION; no source)"), submission 10 lines 112 (both routes, repeat and listing targets), 116 (scale gate: "the cannibalisation review is passed or explained") and 136 (risk row, "Positioning review. Not a stop"), and submission 11 line 120 ("the plan's review threshold is 50% of buyers saying they switched"); the proposal copies carry the same lines. The model shows the NPV is zero at about 7.5 percent and is minus THB 0.94 million at 50 percent, so the trigger sits above the break-even, and the pilot KPI is a self-reported switch share, not the model's one can displaced per cube. Slide 10's earlier claim that the pilot "settles the sign of the value" was not supported by that KPI. Replacement text for every location is at the end of section 8, with the review level (7 percent, DERIVED on ASSUMPTION inputs) and the mapping from stated share to displaced cans (section 5.12).
18. Submission 05 sensitivity table, lines 93 to 108 (new). The table is pre-tax on the THB 4.91 base: lines 95 (base), 96 (shelf 10 / 20), 97 (ex-factory share 50 / 70 percent), 98 (pouch), 99 (print), 100 (processing), 101 (carton), 102 (target pH 3.0), 103 (excise 3.65 | 508,000), 104 (single pouch), 105 (12-cube carton), 106 (24-cube carton), 107 and 108 (all four packaging inputs). Line 103 carries a second after-excise contribution (3.65) next to the lead 3.94. Reconciliation is in section 5.10 (the gap is the invoice: 9.00 against 9.34). Choice: THB 3.94 is the lead; line 103 is replaced by the chain row, the two ex-factory share rows are removed because the chain fixes the invoice at 62.3 percent of the shelf price, and the after-tax re-run of the remaining rows is in section 5.11. If the lead keeps the table pre-tax and before excise, line 103 stays and the reconciliation sentence in the Limits paragraph covers it. Lines 134 (excise limit) and 138 are touched only by that sentence.
19. Tier label for extracts (new). Appendix A defines P as "read in full". The earlier "P (extract)" label for the Bank of Thailand policy rate (1.00 percent), the Revenue Department 20 percent rate, the dividend rules and the 10 percent holder rate is replaced by S in sections 7 and 8, with the origin named. Record 76 and other records still use "P (extract)" or "P, extract"; either they move to S too or Appendix A gains a line for the hybrid. This record uses S.
20. Tiers of the cube and can contributions (new). Wherever 3.94 and 4.13 (4.127) appear, the tier is "DERIVED on PROXY and ASSUMPTION inputs", as record 70 has it; "S" applies only to the listing prices and the retailer margins as a PROXY.

## 10. Limits (closed as stated limits, not open items)

- Boon Rawd's percentage in Singha Corporation: not found in the sources read; 100 percent is assumed as an upper bound. Creden holds shareholder names and percentages behind a login. The percentage determines the parent's tax treatment (full exclusion needs at least 25 percent) and the size of the dividend to Boon Rawd.
- Shareholders of Boon Rawd and their stakes: not found in the sources read. Per-stake amounts only. Whether holders are Thai individuals, and which tax option they take, is not known; the 10 percent holder rate is illustrative.
- Dividend policy and payout of Singha Corporation and Boon Rawd: none found. 50 and 100 percent used for Singha Corporation; 100 percent assumed for the pass-through to holders. Creden's equity of THB 19.5 billion against registered capital of THB 4.86 billion suggests past retention, so 100 percent payout is a high case.
- Corporate dividend withholding: the Revenue Department table lists dividends at 10 percent; whether it applies to Thai-to-Thai dividends that qualify for the exclusion, and how any credit works, was not read. Not modelled.
- Booking entity: the profit is earned by the group company that sells the cube. The model books it in Singha Corporation. Creden gives Singha Corporation the holding-company code TSIC 64202 and Thai Wikipedia calls it the group holding company, so a selling subsidiary is possible. Group profit after tax does not depend on the entity; the entity share and the dividend path do.
- Group net profit: Singha Corporation 2024 and 2025 are press figures (S); 2023 was not found. Boon Rawd Brewery's latest found figure is 2022 (S, Thaiger); 2023 to 2025 were not found. Both companies' statements for 2564 to 2568 BE are listed as filed with DBD, and the amounts are behind a login. Consolidated group profit was not found. The scale test uses Singha Corporation's 2025 net profit, a holding-type figure fed by licence fees, management fees and dividends; Boon Rawd's 2022 net profit (1.9 times larger) is shown as a proxy denominator. Every share is therefore an upper bound on the share of a wider group profit.
- Press figures for 2024 and 2025 are not checked against a filing.
- Policy rate: 1.00 percent from the central bank's press release (S, read through a page summary). The premium of 7, 9 and 11 points is an ASSUMPTION, so the cost of capital of 8, 10 and 12 percent is an assumption on top of a sourced base; the 10 percent was kept from the earlier model.
- Peer P/E: aggregator (S); trailing multiples of four listed drinks companies, not of Singha Corporation. Serm Suk page returned 404; not read.
- Excise on the cube: classification (item 02.02, 14 percent ad valorem) and the excise base are not verified. The after-excise basis is derived from the can's chain ratio.
- Can contribution: before aluminium; an upper bound on the loss, which lowers the cannibalisation break points. The LME route is not authorised and no aluminium price is used.
- Cube contribution: binder and flavour are not priced, so the contribution is an upper bound by those two items, which raises the cannibalisation break points. The net effect of the two biases is not known. The NPV is zero at THB 3.64 a cube, THB 0.31 below the lead, so the sign of the headline NPV is not robust.
- Depreciation, the year-0 setup convention, the same-year tax credit and the carry-forward variant are ASSUMPTIONS; the carry-forward rule was not read.
- Displacement factor: one can lost per cube bought by a stated switcher is an ASSUMPTION; the pilot's store sales, where available, set it.
- Invested capital is the setup outlay only. ROIC is an upper bound.
- Page reads: every web page in this record was read through a WebFetch page summary, not in full. A request for the verbatim text of the Bank of Thailand statement returned a summary.
- Web search: the turn's search budget is shared by all agents and was used up, so the ownership, shareholder and 2023 profit items could not be searched again. Follow-up route, if wanted: the DBD filing (shareholder list and statements for 2564 to 2568 BE), or a Form 56-1 of a listed group company that prints the group structure.

## 11. Responses to the verifier's reviews (20 October 2026)

### Round 1 (earlier in the day)

| Issue | Handling |
|---|---|
| Booking entity stated and denied; "not yet confirmed" an open item | Accepted. The profit is earned by the group company that sells the cube, the model books it in Singha Corporation as a stated assumption, and the entity is a stated limit |
| "Not published" for ownership and shareholders | Accepted. Reworded to "not found in the sources read"; limit kept |
| Creden called a "registry record" | Accepted. Now "Creden company data page, S" |
| Speaker note said value "turns negative once the cube takes sales from the can"; break-evens not flagged conservative | Accepted in part. The note now says the value turns negative at about 7.5 percent and names the aluminium point. The word "conservative" is not used: the cube's binder and flavour are also unpriced (record 70 section 2.11), which pushes the break-even the other way |
| Two contribution bases, none chosen | Accepted. The after-excise contribution (THB 3.94) leads; THB 4.91 appears as the labelled sensitivity |
| Cost of capital not built as policy rate plus premium | Accepted and closed from the central bank's press release (1.00 percent) plus a premium (ASSUMPTION) |
| Conflicts list incomplete; slide 10 drops drivers | Accepted. Section 9 lists every location found; slide 10 keeps the volume, fixed-cost and option drivers |
| P tier for a model-written extract; omitted proviso; full-exclusion value tagged P | Accepted. Proviso added; full-exclusion value is CONDITIONAL (tier moves again in round 2, below) |
| Group-financials limit overstated | Accepted. Reworded; Boon Rawd 2022 added as a proxy denominator |
| Scale volumes on one basis only | Accepted. Both bases in sections 5.6, 7 and 8 |
| Dividend chain stated as fact | Accepted. Items are conditional; assumptions and limits listed |
| Carabao flag false alarm; add Ichitan | Accepted and checked. Ichitan added; median of four 13.66 |
| Exhibit text in fragments; slide 9 against slide 10 | Accepted. Written as sentences; conflict 3 |

### Round 2 (this revision)

| Issue | Severity | Handling |
|---|---|---|
| Before-excise cannibalisation figures mix bases (4.91 cube against the 4.127 after-excise can) and are presented as a plain "before excise" sensitivity; a consistent basis would be less flattering | Medium | Accepted in part. The mixing is real: the deck-basis rows are the scenario in which only the can bears excise. Tested with a consistent run (both products before excise on the can's chain: cube 5.25, can 5.33): the break-even share is 30.3 percent against 30.9 percent, and the NPV at 25 percent is THB 0.152 million against 0.130 million, so the deck basis is a close read at 25 percent and not flattering there. At 50 and 100 percent it is less negative by THB 0.14 and 0.46 million, so there it does flatter. Fix: judge-facing text keeps only the 0 percent before-excise NPV (0.68 million) and states the before-excise break-even as about 30 percent with both readings named; the before-excise figures at 25, 50 and 100 percent (0.13, minus 0.42, minus 1.52) are removed |
| The 50 percent cannibalisation review trigger sits above the break-even; the pilot KPI is a self-reported share; slide 10 overstated what the pilot settles; not in the conflicts list | Medium | Accepted. Conflict 17 added with every line; replacement text and a 7 percent review level (DERIVED) at the end of section 8; the stated-share mapping and the displacement factor are in section 5.12; slide 10 driver 5 now states the review level and the rerun |
| Submission 05 lines 96 to 108 not listed; line 103 carries a second after-excise contribution (3.65) | Medium | Accepted. Conflict 18 lists lines 95 to 108; section 5.10 reconciles 3.65 and 3.94 (invoice 9.00 against 9.34, both with 14 percent excise off the invoice); THB 3.94 chosen; replacement for line 103 and an after-tax re-run of the table (section 5.11) |
| Tier of 4.127 and 3.94 given as S although inputs are ASSUMPTION or PROXY | Medium | Accepted. Relabelled "DERIVED on PROXY and ASSUMPTION inputs" in the script, the results file, the record and the judge-facing text. Conflict 20 |
| Slide source line pairs a range of multiples with one value | Medium | Accepted. Now "A median trailing price-to-earnings ratio of 13.7 times (range 10.9 to 24.1) would imply about THB 2.1 million (1.6 to 3.6 million)" |
| "P (extract)" is not a tier in Appendix A | Low | Accepted. Relabelled S in sections 7 and 8 and in the saved pages. A fetch asking the tool for the full Bank of Thailand text returned a summary, so P could not be earned; conflict 19 notes the repo-wide choice |
| 10 percent discount rate reads as anchored on the policy rate | Low | Accepted. Now "10 percent (assumption, kept from the earlier model); the policy rate of 1.00 percent is the base of that rate and the premium is an assumption" |
| "Its own pages"; "filed with DBD"; Boon Rawd's group page does not list Singha Corporation | Low | Accepted. "Its own About page (footer 2014)"; Boon Rawd's Our group page and Thai Wikipedia added; "listed by Creden as filed" |
| Section 8 header does not say which lines go; slide item 2 omits the half-exclusion case | Low | Accepted. Placement note names lines 79, 81, 83 and 87 and keeps 85; slide item 2 adds "before any dividend tax" and the THB 136,000 half-exclusion figure |
| Year-1 tax credit "offsets other group profit" is not a legal mechanism | Low | Accepted. Reworded; carry-forward (NPV 0.161 million) and no relief (0.128 million) computed in section 5.9 |
| Denominators are single-company figures, not consolidated group profit | Low | Accepted. Sentence added to the limits and to the scale note; Boon Rawd 2022 is 1.9 times Singha Corporation 2025 (computed) |
| Contribution break-even not given; sign of the headline NPV not robust | Low | Accepted. NPV is zero at THB 3.64 a cube (THB 0.31, 7.8 percent below 3.94); on the slide and in section 8; title toned to "little or no value" |

No issue was rejected. One was accepted in part (the first row), with the evidence shown. The word "conservative" is still not used (round 1).

## 12. Files

- rework/75_value_accrual_model.md (this record).
- rework/screen/value_accrual_model.py (model, standard library; run in this revision; all checks pass).
- rework/screen/value_accrual_model_results.json (results; written by the script).
- rework/raw/diligence_2026-10-20/T12/singha_corporation_about_us_2026-10-20.md
- rework/raw/diligence_2026-10-20/T12/boonrawd_profile_2026-10-20.md
- rework/raw/diligence_2026-10-20/T12/creden_singha_corporation_0105544082625_2026-10-20.md
- rework/raw/diligence_2026-10-20/T12/mgronline_9690000048712_2026-05-23_extract.md
- rework/raw/diligence_2026-10-20/T12/revenue_dept_corporate_income_tax_and_dividend_rule_2026-10-20.md (tier relabelled S)
- rework/raw/diligence_2026-10-20/T12/peer_pe_stockanalysis_2026-10-20.md
- rework/raw/diligence_2026-10-20/T12/bot_policy_rate_pages_2026-10-20.md
- rework/raw/diligence_2026-10-20/T12/bot_policy_rate_press_release_31_2026_2026-10-20.md (tier relabelled S; second fetch noted)
- rework/raw/diligence_2026-10-20/T12/tradingeconomics_thailand_interest_rate_2026-10-20.md
- rework/raw/diligence_2026-10-20/T12/ownership_sources_read_2026-10-20.md
- rework/raw/diligence_2026-10-20/T12/ownership_second_read_2026-10-20.md (new: Thai Wikipedia, Creden Boon Rawd, About page re-read)
- rework/raw/diligence_2026-10-20/T12/thaiger_1389992_group_financials_2026-10-20.md

Searches: the turn's web search budget is shared by every agent and was used up, so no search ran in this revision; three direct page reads were added. No outside contact, form, download or publication was made.
