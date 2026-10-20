# V2. Distributor margin on a 330 mL can or carbonated soft drink, Thailand, 2024 to 2026

Record date: 20 October 2026. Item V2 of rework/workflows/update_loop_state_2026-10-20.md, worked under rework/SOURCING_POLICY.md. Saved text for every figure is in rework/raw/update_2026-10-20/V2/.

Scope: read-only research. No outside contact, no quote request, no form, no account, no file download, no commit or push. The deck, submission and proposal files were not edited.

## 1. Answer

Closed as a limit. No distributor margin on carbonated soft drinks or on a 330 mL can for 2024 to 2026 was found in any source read.

The best proxy is the National Statistical Office (NSO) value added share of income for wholesale of non-alcoholic beverages in the 2023 reference year: 16.2% (tier P, status PROXY). It measures value added for a class of goods that includes water, juice and carbonated drinks. It is not a margin on a soft drink, it is not a 2024 to 2026 figure, and the NSO definition behind it is not yet confirmed.

The 10% to 20% distributor band on slide 4 remains an ASSUMPTION. The proxy lies inside the band, but the band's lower bound sits below it.

## 2. Figures and tiers

| Figure | Value | Period | Source (URL or page) | Tier | Status |
|---|---|---|---|---|---|
| Wholesale of non-alcoholic beverages (NSO class 46322), value added as % of income | 16.2% (THB 5,219.3 million on THB 32,282.8 million) | 2023 | NSO Business Trade and Services Survey Report 2024, Table 3, printed page 89. https://www.nso.go.th/public/e-book/Census_Survey/The_2024_Business_Services_Survey/124-125 | P | PROXY (value added, class level, not carbonated-soft-drink specific) |
| Wholesale of food, beverages and tobacco (463) | 16.7% | 2023 | Same report, printed page 88 (flipbook /122-123) | P | PROXY |
| Wholesale of alcoholic beverages (46321) | 6.6% | 2023 | Printed page 89 | P | PROXY (context) |
| Wholesale of beverages and tobacco (4632) | 8.4% | 2023 | Printed page 89 | P | PROXY (context) |
| Convenience stores and minimarts (47113), value added as % of income | 32.2% | 2023 | Printed page 91. /128-129 | P | PROXY for the retailer band |
| Supermarkets (47111) | 18.0% | 2023 | Printed page 91 | P | PROXY |
| Discount stores, supercentres, hypermarkets (47112) | 23.7% | 2023 | Printed page 91 | P | PROXY |
| Grocery stores (47114) | 21.8% | 2023 | Printed page 91 | P | PROXY |
| Specialised beverage retail (4722) | 18.1% | 2023 | Printed page 91 | P | PROXY |
| Specialised non-alcoholic beverage retail (47222) | 39.0% on a base of THB 5.1 billion | 2023 | Printed page 91 | P | PROXY, small base |
| CP Axtra gross margin (group, all categories) | 16.45% FY2024; 16.08% FY2025 | 2024, 2025 | https://stockanalysis.com/quote/bkk/CPAXT/financials/income-statement/ (read 20 October 2026) | S (aggregator) | Group, not beverage-specific |
| SiS Distribution gross margin (IT distributor, other category) | 7.65% FY2024; 8.02% FY2025 | 2024, 2025 | https://stockanalysis.com/quote/bkk/SIS/financials/income-statement/ | S (aggregator) | Cross-category indicator only |
| Saha Pathanapibul gross margin (consumer products) | 17.84% FY2024 | 2024 | https://stockanalysis.com/quote/bkk/SPC/financials/income-statement/ | S (aggregator) | Includes any manufacturing, not a pure distributor |
| Haad Thip gross margin (Coca-Cola bottler and distributor, southern Thailand) | 53.08% FY2024 (aggregator); 42.1% Q1 2025 (press quoting the company) | 2024; Q1 2025 | https://stockanalysis.com/quote/bkk/HTC/financials/income-statement/; https://www.mitihoon.com/2025/05/21/545832/ | S | Bottler margin, not a distributor margin; revenue conflict unresolved |
| Sahapat outlets served | 72,570, of which 65,650 traditional trade | Undated | https://www.sahapat.co.th/th/distribution/distribution-network.html | COMPANY CLAIM | Context only |

Saved text: rework/raw/update_2026-10-20/V2/nso_wholesale_table3_2023.md, nso_retail_table3_2023.md, nso_definitions_checked_2026-10-20.md and company_and_press_checks_2026-10-20.md.

## 3. Why the NSO figure is a proxy and not the margin

The NSO table gives income, intermediate consumption and value added. Value added is income minus intermediate consumption (the NSO formula, as stated on an NSO open data page). A distributor's gross margin is income minus the purchase cost of the goods it sells.

Value added is therefore a floor on the gross margin only if intermediate consumption includes goods bought for resale. The wholesale ratio of 83% to 84% of income suggests that it does, because a services-only cost base could not be that large. The NSO definition was not found in any page read, so this is an ASSUMPTION until the methodology is checked. If the definition is confirmed, the distributor's gross margin on non-alcoholic beverages in 2023 was at least 16.2% of income. If it is not confirmed, the 16.2% says little about the margin.

Value added is also what remains for labour, depreciation and profit after non-labour intermediate costs. That is a further reason the figure is a PROXY and not a margin.

## 4. Effect on the slide 4 distributor band (10% to 20%)

- The band stays an ASSUMPTION. No source gives a distributor margin for a carbonated soft drink or a 330 mL can.
- The NSO class figure of 16.2% lies inside the band, close to its midpoint of 15%. The 10% lower bound lies below the proxy.
- If the team wants a sourced anchor, the 16.2% can be cited as a PROXY from NSO 2023 data, with the caveats in sections 3 and 6. The band can stay as a stated range. This is a team decision. Nothing was changed.

## 5. Retailer band check (25% to 35%)

Where the band appears in the repo:
- rework/53_unit_cost_and_value_chain.md, section 4: "25% to 35% for the retailer" (ASSUMPTION).
- rework/screen/unit_cost_value_chain.py: retailer margin r between 25% and 35%.
- rework/screen/financial_projection.py: retailer margin 30% (mid) and 35% (high), ASSUMPTION.
- rework/proposal/10_risk_and_implementation.md and rework/submission/10_risk_and_implementation.md: risk row "Listing and channel", "Retailer margin of 25 to 35 percent ... ASSUMPTIONS".

Slide 4 text in rework/deck/deck_content.md states the distributor band (10 to 20 percent, unsourced) and does not state the retailer band. The user should confirm which slide carries the 25% to 35% figure. Nothing was changed.

The invoice chain in rework/screen/value_accrual_model.py uses a retailer margin of 21.6% and a distributor margin of 15%. rework/70_singha_internal_estimates.md names 21.6% as the median of three retail gross margins. The 21.6% is a different number from the 25% to 35% band.

Test against the sources read:
- NSO convenience stores, 32.2%: inside the 25% to 35% band.
- NSO supermarkets 18.0%, grocery stores 21.8%, hypermarkets and discount stores 23.7%, specialised beverage retail 18.1%: below the band.
- CP Axtra group gross margin, 16.1% to 16.5%: below the band. The group includes wholesale cash and carry.

Verdict: the 25% to 35% band is not sourced for beverages. It is consistent with the NSO convenience store figure only. The model's 21.6% lies between the NSO class values and the band. The reconciliation belongs to V4 (CP ALL margin). The band stays an ASSUMPTION.

## 6. Limits and routes that would settle them

1. No beverage-specific distributor margin was found in any source read. Thai and English searches covered trade press, Thai distributors listed on SET, Boon Rawd Trading, Haad Thip, ThaiNamthip, Osotspa, ThaiBev and marketing-margin journals.
2. Boon Rawd Trading (the Singha sales arm, per a 2016 release seen only as a snippet) is not listed, and no statements were read. Route: a DBD DataWarehouse+ lookup by the company's 13-digit registration number, once that number is found. This is a registry lookup, not contact.
3. Haad Thip Form 56-1 for FY2024 is filed (SEC portal, received 14 August 2025). The download is a ZIP file, which was not downloaded because it needs your permission. Route: the revenue and cost-of-sales notes and any trade discount lines. The aggregator revenue (THB 6,648 million for 2024) conflicts with a Thai snippet (THB 8,129 million, not opened). Settled by the 56-1 notes.
4. NSO definition of intermediate consumption: not found on flipbook pages 73 to 78 (printed pages 47 to 52) or on the NSO open data pages read. Route: the definitions section or glossary of the same NSO report (later flipbook pages), or the survey's methodology appendix.
5. The NSO values were read from the text of flipbook pages, not from the printed image. Each row passed the income minus intermediate equals value added check, and subclasses add to their parents. Route: check printed pages 88, 89 and 91 before any figure enters a deck or submission.
6. Year coverage: the only NSO round read has reference year 2023. The survey runs every two years. No 2024 to 2026 value was found.
7. Class mix: non-alcoholic beverage wholesale includes water, juice, milk drinks, energy drinks and carbonated drinks. The NSO table does not split carbonated soft drinks.
8. Coverage: the wholesale class counts establishments classified as wholesalers. A bottler that sells direct to shops is classed as a manufacturer, so direct-store-delivery margins are outside the class.
9. Excise and sugar tax: if the sugar tax is included in income and in purchases, the value added share is diluted. The table does not show the effect.
10. Income is the establishment's operating income. It is used as the proxy for the selling price.
11. Haad Thip and Thai press figures conflict (aggregator revenue against a snippet). Haad Thip is a bottler, so its gross margin is not used.
12. The K Research non-alcoholic beverage report (November 2024) has a value chain diagram with counts of wholesalers and retailers but no margin. The K Research update of May 2025 and the LH Bank outlook of March 2026 were fetched but not read, and are not cited.

## 7. Work done

About 25 web searches in Thai and English and about 35 page or PDF fetches, including the NSO flipbook pages listed in the saved text. Pages opened and cited are listed in the saved-text files with their URLs and the date read (20 October 2026). Snippets that were not opened are listed as leads only.

## 8. Items for the team to decide (no edits made)

- Keep the 10% to 20% band labelled ASSUMPTION on any judge-facing slide.
- If the team wants a sourced anchor, use the NSO 2023 non-alcoholic beverage wholesale value added share (16.2%, PROXY, tier P), with the definition caveat in section 3 and the one-year limit in section 6.
- Confirm which slide carries the 25% to 35% retailer band (section 5).
- Reconcile the 21.6% retailer margin in the model with the NSO convenience store share (32.2%) and the CP Axtra group margin (16.1% to 16.5%), through V4.
