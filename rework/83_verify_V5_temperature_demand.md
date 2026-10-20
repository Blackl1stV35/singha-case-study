# V5: Is there a sourced temperature-to-demand value for the ambient variation model?

- Record: rework/83_verify_V5_temperature_demand.md
- Item: V5 of the update loop. Source: rework/workflows/update_loop_state_2026-10-20.md, section 5, item 5 ("Thai temperature-to-demand source for the ambient model (T15)").
- Date of work: 20 October 2026. Revised the same day after the review in rework/workflows/update_loop_review_2026-10-20.md (section V5). The revision log is section 11.
- Verdict: closed as a stated limit. No Thai or tropical coefficient exists in anything that could be opened. Temperate-market values exist and are kept as PROXY brackets. The ranking question is closed with a computed answer: a sourced temperature value does not change any leader. That answer is about temperature only; the reach and per-member leaders are separately fragile to non-temperature inputs in the same file (section 6).
- Rules followed: rework/SOURCING_POLICY.md (19 October 2026) and CLAUDE.md section 3. No outside contact, no quote request, no form, no account, no commit or push. No spreadsheet, CSV or archive was downloaded. No deck, submission, proposal, script or results file was edited. Raw notes are in rework/raw/update_2026-10-20/V5/.
- Reading note: the fetch tool returns a condensed extract of a page, not the verbatim page. Short fragments in quotation marks below are as the extract returned them. PDFs were fetched through the tool, which stores the binary in the session folder; their text layers were then read locally with PyMuPDF (python -I, each file in its own scratch folder). The OpenAlex and Crossref bibliographic records for Kato (2021) were read as JSON. Nothing from the web was run as code.

## 1. Answer

Question: is there a sourced relationship between ambient temperature and soft-drink or carbonated-drink sales, usable as the seasonal temperature input of rework/screen/ambient_variation.py (sensitivity 0 to 0.05 per degree Celsius per base, currently an ASSUMPTION)?

- (a) Thai monthly series matched to Thai Meteorological Department (TMD) temperatures: not found in a usable form. The Office of Industrial Economics (OIE) publishes a monthly beverage Manufacturing Production Index (MPI), but its level series was not read (the i-Index portal did not respond; the Bangkok Bank industry reports that reprint it timed out twice). In the revision the OIE statistics page was found to load and to link Excel and CSV files with per-product monthly sales volume and value from January 2021; they were not downloaded because that needs the user's permission (limit 1). The OIE quarterly and monthly reports that could be opened give year-on-year changes only, and the TMD monthly pages give a national temperature departure for only four of the six months checked. No Thai coefficient can be computed.
- (b) Published elasticities in tropical or Asian markets: none with a magnitude. Asian sources give a direction or a threshold but no per-degree figure for soft drinks. The Japan direction (soft drinks, mean temperature positive in every time zone) rests on the abstract of Kato (2021), read as an abstract record in OpenAlex and confirmed as a real paper in Crossref; the ACM publisher page returned HTTP 403 and the paper was not read in full. It is tier S at abstract level, gives no magnitude, and no number is taken from it. The South Korea threshold (convenience stores: carbonated drinks sell well above about 24 degrees Celsius) is a press report, tier S.
- What does exist, all from temperate markets and all PROXY: weekly demand for a basket of six liquid refreshment beverages (the list and the country are not in the abstract that was read; the US is probable) up about 2.1 percent per degree in heat waves and down about 0.4 percent per degree in cold waves (peer-reviewed abstract); US household added sugar from sweetened beverages up 0.73 grams per degree between 12 and 30 degrees Celsius, about 1 percent per degree on the paper's own 70 gram baseline (derived); UK trade-press claims of 1.6 percent (IRI, 2019), 1.8 percent (Talysis, reported 1 June 2026) and 2 to 5 percent (Nielsen, 2014) per degree. Expressed as the model's beta (the natural log of one plus the fractional change), they span 0.004 to 0.049 per degree Celsius and all sit inside the assumed 0 to 0.05.
- Two sourced cautions point to the lower half of the range or below. The US household study finds the response plateaus or declines above 30 degrees Celsius and is "minimal" in the hot-humid climate zone (differences not statistically significant); Bangkok monthly means run from 27.3 to 30.7 degrees Celsius. A US conference abstract finds no temperature effect on diet drinks, and the cube is sweetened with sucralose. The evidence on that second point is thin and conflicts with a Swedish student thesis (section 5).
- Thai evidence is direction only: Marketeer (2020), Mintel (2023), Krungsri Research (2024 and 2026) and a Cabinet briefing document of 9 July 2024 (tier S: it is hosted on infocenter.oic.go.th, has no letterhead, and its issuer, the Ministry of Industry, is inferred from its text) all say hot weather lifts demand for non-alcoholic drinks. None gives a coefficient, and Krungsri says it does not separate weather from other drivers. The OIE attributes the 2025 falls in carbonated soft drinks to new products and production halts, not to weather.
- Effect on the ranking: none from a sourced temperature value. A common sensitivity on every base cancels from the ranking; the model's own notes say so and a re-run confirmed it (section 6). The leaders stay: men 45 to 59 on reach (probability 0.6808 in the results file), men 25 to 34 per person in the cell (0.9405) and per member (0.8156). Scope, read from the results file (section 6, table 6A):
  - The only temperature configuration in the results file that flips a per-person or per-member leader is the directional scenario, in which men 25 to 34 are fixed at a heat sensitivity of 0 and men 35 to 44 and men 45 to 59 are fixed at delta per degree Celsius. In the file it flips the leader to men 35 to 44 in April at delta 0.04 and 0.05, and in May at 0.05, on both per-person lenses and on the per-member lens. A finer rerun puts the April crossing at about 0.031 (the file's grid steps by 0.01, so 0.04 is only its first grid point). At delta 0.03 no month flips in the file's month-by-month run, April does not flip at any smaller delta, and the twelve-month mixture does not flip at any delta up to 0.05.
  - For the per-person lenses this is the only kind of run in the whole file that changes the leader. For the per-member lens, three non-temperature structural sweeps also flip the leader to sweet-bottled drinkers 25 to 44 (sex gradient off, alcohol cue 20 percent, bottled habit counted once). For the reach lens, four structural sweeps flip the leader to the same base (the three just named and the 2021 drinking cells), and no temperature configuration flips it. The reach and per-member leaders are therefore separately fragile to non-temperature inputs, and the file marks both with confidence "none". That fragility is not caused by temperature, so the conclusion that a sourced temperature value changes no leader is unaffected.
  - No source gives any age or sex difference in temperature response, and no source puts a base at exactly zero response, so the directional condition remains an unsourced ASSUMPTION.

## 2. Figures

Each row carries value, unit, population and period, method, tier and status. Tier S means a page was opened and read; it is never upgraded. The saved pages are in rework/raw/update_2026-10-20/V5/.

| # | Measure | Value | Unit | Population, period | Method | Tier | Status | Saved page |
|---|---|---|---|---|---|---|---|---|
| F1 | Weekly demand response to a heat wave, six liquid refreshment beverages (the abstract does not list them; a snippet not opened says carbonated soft drinks are among them) | +2.1 | percent per degree Celsius | Country and period not in the abstract; snippet not opened says 52 US markets, 10 years | Two-step econometric model, long-term trend plus short-term heat and cold waves | S | PROXY | keles_2018_ijpe_beverage_weather.md |
| F2 | Same, cold wave | -0.4 | percent per degree Celsius | same | same | S | PROXY | same |
| F3 | Same, long-term warming trend | +0.21 (63 million gallons) | percent per year | same | same | S | PROXY | same |
| F4 | Added sugar from sweetened beverages | 0.73 | grams per degree Celsius per capita-day (adult male equivalents) | US households, Nielsen Homescan retail purchases, 2004 to 2019, n = 6,908,936, slope stated for 12 to 30 C | Household fixed-effects regression, 2 C bins | S | PROXY | he_2025_nature_climate_change_added_sugar.md |
| F5 | Total added sugar | 0.70 | same | same | same | S | PROXY | same |
| F6 | F5 over the paper's quoted US baseline of over 70 grams a day | about 1.0 | percent per degree Celsius of total added sugar | arithmetic 0.70 / 70, scale only, mixes definitions | none | DERIVED from S | PROXY | same |
| F7 | Response above 30 C and in hot-humid zone | plateau or decline above 30 C; 0.8 percent of observations above 30 C; "minimal response" in the Hot-Humid zone, differences not statistically significant; Asian group "nonsignificant" | text | same | same | S | PROXY | same |
| F8 | Sugary drinks, one extra day above 35 C | +0.3 | percent of monthly per capita volume | US NielsenIQ Consumer Panel 2011 to 2019, 94,738 households | Poisson pseudo-maximum-likelihood panel, 5 degree bins | S (conference abstract) | PROXY | roche_de_preux_2024_sugary_drinks_conference.md |
| F9 | Diet drinks (non-sugar sweeteners) | no effect | text | same | same | S (conference abstract) | PROXY | same |
| F10 | Soft drink sales, IRI (reported 6 May 2019) | +1.6 | percent per degree Celsius | not stated (UK trade title) | not stated | S | PROXY | uk_trade_press_per_degree.md |
| F11 | Soft drink sales, Nielsen, above 14 C (reported 1 June 2014) | +2 to +5 | percent per degree Celsius | not stated (Scottish trade title, 2014) | not stated | S | PROXY | same |
| F12 | Carbonated drinks sell well above | 24 | degrees Celsius | South Korea convenience stores, Seven Eleven and GS25, June 2020 | press report, threshold only | S | PROXY | asia_and_other_evidence_reviewed.md |
| F13 | Thailand national mean temperature departure, April, May, June 2024 | +2.6, +1.3, +0.8 | degrees Celsius above normal | Thailand, TMD monthly summaries | official summary | P | SOURCED | thai_official_cabinet_oie_tmd.md |
| F14 | OIE beverage MPI, Q2 2024 | +7.5 | percent year on year | Thailand, rice whisky, beer, soft drinks, fruit flavoured drinks; no weather reason given | official index | P | SOURCED (fact only) | same |
| F15 | OIE carbonated soft drinks and soda water, Q1 2025 | -10.0 | percent year on year | Thailand; reason given: more product variety | official index | P | SOURCED (fact only) | same |
| F16 | Same, Q2 2025 | -17.8 | percent year on year | Thailand; reason given: new products | official index | P | SOURCED (fact only) | same |
| F17 | Same, May 2025 | -25.6 | percent year on year | Thailand; non-alcoholic beverages -13.6 percent | official index | P | SOURCED (fact only) | same |
| F18 | Bangkok monthly mean temperature 1991 to 2020 | 27.3 (Dec) to 30.7 (Apr); annual 28.9 | degrees Celsius | TMD station 48455 (Bangkok Metropolis), not a national mean | climate normals | P | SOURCED (source PDF page 57 re-read on 20 October 2026 in the revision; first pass read only the T15 note) | tmd_bangkok_normals_reread_page57.md |
| F19 | Seasonal multiplier on all bases at beta 0.0208 (F1 as a log) | April x1.038, October x0.990, December x0.967; hottest over coolest month x1.073 | ratio to the annual mean | model arithmetic, section 3 | exp(beta x (monthly mean - 28.9)) | DERIVED | PROXY | this record |
| F20 | Leader probabilities under any common sourced beta | reach M45 0.6858; per person M25 0.9734; per member M25 0.8478 | probability | 40,000 draws, seed 20261020 | re-run of the repo model, section 6 | DERIVED | DERIVED | this record |
| F21 | Smallest differential (men 35 to 44 and 45 to 59 above men 25 to 34, who are fixed at 0) at which the April per-person and per-member leader changes | about 0.031 (between 0.030 and 0.031); the results file's 0.01 grid first shows the change at 0.04 | per degree Celsius | rerun on a finer grid of the file's directional scenario, April 30.7 C | repo model, section 6 | DERIVED | ASSUMPTION (no source for any age or sex difference) | results_file_scope_and_directional_rerun.md |
| F22 | Soft drink sales, Talysis as reported by Asian Trader (1 June 2026) | +1.8 | percent per degree Celsius above the seasonal average | UK convenience sector, a recent hot spell, period not stated | not described | S | PROXY | uk_trade_press_per_degree.md |
| F23 | Japan, soft drinks, effect of mean temperature on purchase amount (Kato 2021) | positive in every time zone; no magnitude | text | Japan, five channels; period not in the abstract | fixed effects model, per the abstract | S (abstract level; paper not read in full; ACM page HTTP 403) | PROXY (direction only) | kato_2021_icebi_japan_soft_drinks_abstract.md |
| F24 | US alcohol retail sales, warmest regions (Hirche, Haensch and Lockshin 2021) | liquor and white wine do not respond to temperature in the warmest regions | text | 651 US counties, 2013 to 2015, weekly | seasonal ARIMA with regressors, per the abstract | S (publisher abstract page; full text not read) | PROXY (alcohol; a hint only) | hirche_haensch_lockshin_2021_ijwbr_alcohol_temperature.md |
| F25 | Cabinet briefing of 9 July 2567 (2024), Q1/2567 | non-alcoholic drinks rose in almost every item except instant coffee, attributed to very hot weather; no percentage | text | Thailand, first quarter 2024 | issuer's attribution, not an estimate | S (issuer inferred from content; no letterhead; hosted on infocenter.oic.go.th) | SOURCED as a statement only (direction) | thai_official_cabinet_oie_tmd.md |

Source URLs for the rows above (each page was opened on 20 October 2026; a row that shares a document with another row is listed once per row where the review asked for it):

- F1 to F3: https://ideas.repec.org/a/eee/proeco/v195y2018icp186-197.html (abstract only).
- F4 to F7: https://www.nature.com/articles/s41558-025-02398-8 (read through a condensed extract).
- F8, F9: https://events.gwdg.de/event/626/contributions/1962/ (conference programme entry).
- F10: https://forecourttrader.co.uk/soft-drinks/sales-pour-in/643387.article.
- F11: https://www.scottishgrocer.co.uk/2014/06/how-hot-days-generate-sales/.
- F12: https://www.asiae.co.kr/en/article/2020061711103640733.
- F13: https://www.tmd.go.th/en/climate/summarymonthly/042024, .../052024 and .../062024.
- F14: https://www.oie.go.th/assets/portals/1/files/quarterly_industrial/Q2_2024andOutlookQ3_2024_en.pdf.
- F15: https://www.oie.go.th/assets/portals/1/files/quarterly_industrial/Q1_2025_EN.pdf.
- F16: https://www.oie.go.th/assets/portals/1/files/quarterly_industrial/Q2_2025_EN.pdf.
- F17: https://www.oie.go.th/assets/portals/1/files/monthly_report/en_briefMay2025.pdf.
- F18: https://ubonmet.tmd.go.th/files/MetInfo/climate_normal.pdf, PDF page 57.
- F19 to F21: this record and rework/screen/ambient_variation_results.json; no web page.
- F22: https://www.asiantrader.biz/hot-conditions-convenience-sales-rise.
- F23: https://api.openalex.org/works/doi:10.1145/3497701.3497702 (abstract) and the Crossref record for DOI 10.1145/3497701.3497702; publisher page https://dl.acm.org/doi/10.1145/3497701.3497702 returned HTTP 403.
- F24: https://www.emerald.com/insight/content/doi/10.1108/IJWBR-07-2020-0035/full/html.
- F25: https://infocenter.oic.go.th/upload/cms/1745051594_8866.pdf.

Thai qualitative statements without a number (not in the table): see thai_press_bank_research_qualitative.md and the Cabinet briefing in thai_official_cabinet_oie_tmd.md.

## 3. The sourced values in the model's unit

The model multiplies trial propensity on each base by exp(beta x (monthly mean - 28.9)). A fractional change p per degree maps to beta = ln(1 + p).

| Source value | beta | April (30.7) over annual mean | December (27.3) over annual mean | April over December |
|---|---|---|---|---|
| Cold wave, 0.4 percent (F2) | 0.0040 | 1.0072 | 0.9936 | 1.0137 |
| About 1.0 percent, total added sugar (F6, scale only) | 0.0100 | 1.0181 | 0.9842 | 1.0344 |
| IRI, 1.6 percent (F10) | 0.0159 | 1.0290 | 0.9749 | 1.0555 |
| Talysis, 1.8 percent (F22) | 0.0178 | 1.0326 | 0.9719 | 1.0625 |
| Heat wave, 2.1 percent (F1) | 0.0208 | 1.0381 | 0.9673 | 1.0732 |
| Nielsen low end, 2 percent (F11) | 0.0198 | 1.0363 | 0.9688 | 1.0696 |
| Model centre, assumed | 0.0250 | 1.0460 | 0.9608 | 1.0887 |
| Nielsen high end, 5 percent (F11) | 0.0488 | 1.0918 | 0.9249 | 1.1804 |
| Top of assumed range | 0.0500 | 1.0942 | 0.9231 | 1.1853 |

- The Bangkok monthly means span 3.4 degrees Celsius, so even the top sourced value swings the seasonal level by under 20 percent between the coolest and hottest months, and the central sourced values (1.6 to 2.1 percent, including the 1.8 percent claim) by 5.6 to 7.3 percent.
- Pilot timing: October and November (28.4 C) sit 1.0 percent below the annual level at beta 0.0208, and December 3.3 percent below. These are PROXY-based and apply to every base alike.
- The model centre 0.025 is above the middle of the sourced values (0.016 to 0.021) and below only the Nielsen high end (0.049). It is inside the sourced span. Because a common beta does not move any ranking (section 6), this does not need to change for the ranking; it only sets the size of the seasonal swing in absolute potency.
- Unit caution: the model applies beta to a trial-propensity proxy (a top-2-box intent measure, ASSUMPTION link), while every source above measures sales, volume or grams purchased. Treating a sales response as a trial response is itself an assumption.

## 4. What the Thai evidence supports

- Direction: hot weather lifts demand for non-alcoholic drinks in Thailand. Marketeer (14 April 2020) calls summer the golden time of the soft drink market. Mintel (27 December 2023) reports a record 45.5 degrees Celsius in summer 2023 and carbonated drinks as the top non-alcoholic choice (70 percent). Krungsri (7 November 2024) says non-alcoholic domestic volume rose 7.0 percent in 2023 and 3.5 percent in the first nine months of 2024 on hotter than normal weather partly caused by El Nino, without separating the weather effect. A Cabinet briefing document of 9 July 2024 (tier S, F25: issuer inferred from content, no letterhead, hosted on infocenter.oic.go.th) says non-alcoholic drinks, mineral water and bottled water rose in the first quarter of 2024 in almost every item except instant coffee because of very hot weather. It is used for direction only; no figure depends on it. It would move to tier P only if a copy from the Cabinet Secretariat or the Ministry of Industry were opened.
- A natural experiment exists but cannot be identified from open pages. April 2024 was 2.6 degrees Celsius above normal, May 1.3 and June 0.8 (F13), and the OIE beverage MPI rose 7.5 percent in the second quarter of 2024 (F14). The 2023 comparison temperatures were not read, so no year-on-year temperature change is available, and the beverage MPI mixes beer, whisky and soft drinks. In 2025, with smaller departures (June 2025 was 0.1 above normal; the April and May 2025 pages state none), carbonated soft drinks fell 10.0 percent (Q1) and 17.8 percent (Q2), and the OIE attributes this to new products and production halts. A naive ratio of these changes would give a slope far above any US or UK value and would reflect price competition, product launches and tourism, not weather. No ratio is computed or used.
- Not a coefficient: the Krungsri forecast that carbonated production grows 2.1 to 3.1 percent a year "partly" because of rising temperatures is a growth forecast, not an elasticity.

## 5. Conflicts and how each is handled

| Item | Values found | Handling |
|---|---|---|
| Size of the response per degree | 0.4 (cold wave), about 1.0 (derived, added sugar), 1.6 (IRI), 1.8 (Talysis, 2026), 2.1 (heat wave), 2 to 5 (Nielsen, above 14 C), "as much as 5" (unattributed standfirst) | Spread 0.4 to 5 percent per degree, all temperate and mostly trade press. The figures that come from a peer-reviewed abstract or paper (F1, F2, and F6 derived from F5) are 0.4 to 2.1 percent. Nothing is chosen as the centre; the assumed 0 to 0.05 range is kept as the bracket. |
| Response at high temperature | US positive 12 to 30 C but plateau or decline above 30 C and minimal in the hot-humid zone (F7); Korea threshold of 24 C for carbonated drinks (F12); alcohol study (Hirche, Haensch and Lockshin 2021, publisher abstract page opened, full text not read, tier S, F24): liquor and white wine show no response in the warmest regions | Direction consistent: the response flattens when it is already warm. All twelve Bangkok monthly means are above 24 C, and ten of twelve are 28.4 C or higher. This argues for the lower half of the range in Thailand. It is PROXY reasoning, not a Thai measurement. |
| Sugar versus no sugar | US abstract: no effect on diet drinks (F9); Swedish student thesis: no clear difference between sugar-sweetened and non-sugar models | Unresolved. The cube is zero-sugar, which would lower the effect if the US abstract holds. Both sources are weak (a conference abstract and a bachelor thesis). Not used to set a value. |
| Weather versus other causes in Thai output | Cabinet briefing document (tier S, F25): heat raised demand (Q1 2024); OIE 2025: new products and halts, no weather | Both recorded. They are different years and different issuers, and neither is an estimate. |
| Journal of record for F1 | Search snippet attributed the paper to another journal; the opened IDEAS page shows International Journal of Production Economics 195, 186 to 197 | The opened page governs. |

## 6. Effect on the ambient model and on the ranking

What the results file (rework/screen/ambient_variation_results.json, seed 20261020, 40,000 draws) says, read in this item:

- Leaders under the primary form: reach, men 45 to 59 (probability 0.6808, confidence "none"); per person in the cell, men 25 to 34 (0.9405, "moderate"); per member, men 25 to 34 (0.8156, "none"). The per-person lens appears twice (drinkers only and all eight bases) with identical figures.
- Temperature is already a minor input in the file: fixing the ambient factor at its mean raises the leader probability to 0.6858 (reach), 0.9734 (per person) and 0.8478 (per member); its quintile swing is 0.4 points on reach, 1.6 on per person and 1.3 on per member. The file's own note says a common sensitivity cannot change a ranking.
- Directional scenarios in the file: men 25 to 34 are fixed at a heat sensitivity of 0, men 35 to 44 and men 45 to 59 are both fixed at delta per degree Celsius, and the other six bases keep their independent draws from 0 to 0.05. They are run for April (30.7 C) and for the twelve-month mixture at delta 0, 0.01, 0.02, 0.03, 0.04 and 0.05, and month by month at 0.03 and 0.05. Details and the full list of runs are in table 6A.

### 6A. Which runs in the results file change a leader (read from the file in the revision of 20 October 2026)

A script walked every stored run under each lens and listed each run whose modal leader differs from the lens leader (raw note results_file_scope_and_directional_rerun.md). The probability shown is the full-run leader's chance of being first in that run.

| Lens | Full-run leader (probability, file confidence) | Runs in the file with a different leader | Kind |
|---|---|---|---|
| Reach | men 45 to 59 (0.6808, none) | Four structural sweeps, all to sweet-bottled drinkers 25 to 44 (SB25): sex gradient off (0.4043), alcohol cue 20 percent (0.4313), 2021 drinking cells (0.3254), bottled habit counted once (0.4379) | non-temperature only; no temperature run changes it |
| Per person, drinkers only | men 25 to 34 (0.9405, moderate) | Directional scenario only: April at delta 0.04 (0.2826) and 0.05 (0.128); May at 0.05 (0.3051); the leader becomes men 35 to 44 | temperature only |
| Per person, all eight bases | men 25 to 34 (0.9405, moderate) | The same four runs with the same figures | temperature only |
| Per member | men 25 to 34 (0.8156, none) | Structural: sex gradient off (0.0674), alcohol cue 20 percent (0.2069), bottled habit counted once (0.1867), to SB25. Temperature: April at delta 0.04 (0.2148) and 0.05 (0.1003), May at 0.05 (0.244), to men 35 to 44 | both |

- Runs that change no leader on any lens: the three other model forms, the 23 leave-one-factor-out runs, the 12 months, the season stress run (beta up to 0.15), the four coverage-weight runs, the other structural sweeps, and the four reverse-stress runs (independent betas up to 0.3, 0.45, 0.6 and 1.0).
- The file's flag leader_unchanged_in_every_run is true for both per-person lenses and false for reach and per member. It counts the 55 runs listed in run_counts and leaves out the directional scenarios and the reverse-stress runs, so a true flag on a per-person lens does not mean the directional scenarios leave the leader in place.
- The reach lens also lists one tornado input that flips its top base between the lowest and highest fifth (sweet-bottled share, 25 to 44, 2021). It is not a run and not a temperature input.
- In the twelve-month mixture no delta up to 0.05 changes any leader. At delta 0.03 no month changes any leader. The reach leader stays men 45 to 59 at every delta (April probability 0.6131 at delta 0, rising to 0.8151 at 0.05).

### 6B. Finer rerun of the directional scenario (DERIVED, not in the results file)

The file's grid steps by 0.01, so 0.04 is only its first grid point at which a leader differs. A rerun of the repo functions with the file's seed and settings (script and raw output in the raw folder; the rerun reproduces the file's April figures at delta 0, 0.03, 0.04 and 0.05 to four decimals) gives, for April:

| Delta | Per person: men 25 to 34 first / men 35 to 44 first | Per member: men 25 to 34 first / men 35 to 44 first | Leader |
|---|---|---|---|
| 0.030 | 0.5052 / 0.4894 | 0.3711 / 0.3545 | men 25 to 34 |
| 0.031 | 0.4808 / 0.5135 | 0.3540 / 0.3747 | men 35 to 44 |
| 0.040 | 0.2826 / 0.7099 | 0.2148 / 0.5506 | men 35 to 44 |
| 0.050 | 0.1280 / 0.8629 | 0.1003 / 0.7115 | men 35 to 44 |

- The April crossing is between 0.030 and 0.031 per degree Celsius on both the per-person and the per-member lens.
- Month by month at delta 0.04 and 0.045 the leader changes to men 35 to 44 in April and May only; March and June stay with men 25 to 34 (per person 0.7761 and 0.7315), and the reach leader stays men 45 to 59 in every month.
- This is a property of the scenario as built, which fixes men 25 to 34 at exactly zero heat response while older men respond. A differential of about 0.031 sits inside the assumed 0 to 0.05 range, so the range cannot rule it out, and no source supports it.

What a sourced value does, from a re-run of the repo functions in a scratch folder (script in section 6.1; nothing written to the repo):

| Case | Reach leader (probability) | Per person leader (probability) | Per member leader (probability) |
|---|---|---|---|
| Results file, full run, independent betas 0 to 0.05 | men 45 to 59 (0.6808) | men 25 to 34 (0.9405) | men 25 to 34 (0.8156) |
| Re-run: one common beta on every base, values 0, 0.004, 0.010, 0.016, 0.0208 and 0.05, in April, December and at the annual mean | men 45 to 59 (0.6858) | men 25 to 34 (0.9734) | men 25 to 34 (0.8478) |
| Re-run: 0.0208 on the two bottled-sweet bases only, April then December | men 45 to 59 (0.6281 then 0.7243) | men 25 to 34 (0.9734 both) | men 25 to 34 (0.7161 then 0.9180) |
| Re-run: 0.0208 on the six drinker cells only, April then December | men 45 to 59 (0.7281 then 0.6349) | men 25 to 34 (0.9734 both) | men 25 to 34 (0.9244 then 0.7334) |

- The common-beta rows are identical to the file's own "ambient temperature fixed at its mean" leave-one-out rows (0.6858, 0.9734, 0.8478), which is a consistency check on the re-run. Across all twelve months at beta 0.0208 the leaders and probabilities do not move at all.
- The two single-group rows are scenarios built from the only sourced direction (sugary drinks respond, diet drinks do not). They are not a sourced split by base, since no source splits temperature response by the customer bases used here. They show that even a large one-sided response leaves every leader in place and moves only the probabilities.
- Conclusion for the ranking: no sourced temperature value changes the leader on any lens, because every sourced value is common to all bases or unknown by base, and a common value cancels. The only temperature configuration in the results file that flips a per-person or per-member leader is the directional scenario of table 6A, which needs men 35 to 44 and 45 to 59 to be more heat-sensitive than men 25 to 34 by about 0.031 per degree Celsius or more in the hottest months (the file's own grid shows 0.04), with men 25 to 34 at zero. The sources opened give no age result (the US household study uses age as a control only), no sex difference (effects "consistent across male and female heads") and no urban-versus-rural or income difference that maps to the bases. That condition therefore stays an ASSUMPTION.
- Scope of that conclusion: it is about temperature only. The reach and per-member leaders are fragile to non-temperature inputs in the same file (table 6A), and the file marks both with confidence "none". That fragility does not depend on temperature, so it does not alter the conclusion above.
- The file's statement that temperature does not change a leader stays true within the independent and common cases and stays conditional on the unsourced direction.

### 6.1 Reproduction (scratch script, not in the repo)

The script imports the repo module without running its main function, so the results file and figure are not rewritten. It was run with python -I on 20 October 2026 and took about 7 seconds. The bytecode cache that the import created in rework/screen was removed afterwards, and the modification times of the script and results file were unchanged (20 October 2026 06:43). In the revision the script was run again with python -B -I (no cache written) and the table above reproduced to four decimals: reach 0.6858 under any common beta, 0.6281 then 0.7243 for the bottled bases only and 0.7281 then 0.6349 for the six drinker cells only; per person 0.9734 throughout; per member 0.8478, then 0.7161 and 0.9180, then 0.9244 and 0.7334. The script for the finer directional rerun (section 6B) is in the raw note results_file_scope_and_directional_rerun.md.

```python
import sys, json, math
sys.path.insert(0, r"D:\Workspace\singha-case-study\rework\screen")
import ambient_variation as av
av.load_coverage()
A0 = av.potency(av.central(1), av.PRIMARY)

def leaders(out):
    res = {}
    for lens in av.LENS_ORDER:
        key, names, idx = av.lens_cols(lens)
        s = av.summarise(out[key][:, idx], names, A0[key][0][idx], light=True)
        res[lens] = (s["modal_top"], s["prob_rank_first"][s["modal_top"]])
    return res

def run_case(fixed_beta, months):
    rows = {}
    for name, tm in months:
        _, out = av.run(av.PRIMARY, fixed=dict(fixed_beta), month=tm)
        rows[name] = leaders(out)
    return rows

M = [("Apr", 30.7), ("Dec", 27.3), ("annual", av.TMD_ANNUAL)]
for b in [0.0, 0.004, 0.010, 0.016, math.log(1.021), 0.05]:
    print("common", b, run_case({"beta_" + k: b for k in av.BASES}, M))
b = math.log(1.021)
print("bottled only", run_case({"beta_" + k: (b if k in ("SB25", "SB45") else 0.0) for k in av.BASES}, M))
print("drinkers only", run_case({"beta_" + k: (0.0 if k in ("SB25", "SB45") else b) for k in av.BASES}, M))
```

## 7. What this means for the model and for text that quotes it

- Keep the label of the season sensitivity as an ASSUMPTION, range 0 to 0.05 per degree Celsius. Add that the range is bracketed by PROXY values from temperate markets (0.004 to 0.049) and that no Thai or tropical value was found in the public record opened on 20 October 2026. This record does not edit rework/screen/ambient_variation.py, rework/78 or any other file; the parent decides.
- Do not describe any value as a Thai sensitivity. A line that is safe to use if a stated limit is wanted: "The temperature sensitivity of demand is an assumption bracketed by temperate-market studies (about 0.4 to 5 percent per degree Celsius); no Thai figure was found in the public record."
- If a line says that hotter weather raises soft drink demand in Japan, say that it rests on a paper abstract (Kato 2021, direction only, paper not read in full). The Thai direction rests on press, a market-research release, bank research and a Cabinet briefing document of tier S; none gives a coefficient.
- The finding that no leader changes with temperature can be kept, with its scope stated: no sourced temperature value changes a leader. The only temperature configuration in the results file that flips a per-person or per-member leader is the directional scenario (men 35 to 44 and 45 to 59 more heat-sensitive than men 25 to 34 by about 0.031 per degree Celsius or more in April and May, with men 25 to 34 at zero), which rests on an age or sex difference that no source supports. The reach and per-member leaders are separately fragile to non-temperature inputs (file confidence "none"). rework/78 section 7.6 gives the directional threshold as about 0.04; that is the file's first grid point, and the April crossing in the finer rerun is about 0.031. This record does not edit rework/78.
- The pilot-timing statement (October to December sits 1.0 to 3.3 percent below the annual level at beta 0.0208) is PROXY-based and applies to all bases alike. It should be worded as an illustration, not a forecast.

## 8. Limits, and what would settle each

1. No Thai or tropical coefficient. The route is now verified at page level but not taken. The OIE industrial statistics page (https://www.oie.go.th/view/1/statistics/TH-TH) links an Excel file and a CSV file (Industry_Statistics_TSIC.xlsx and .csv) with per-product production volume, sales volume and sales value from January 2021 to August 2026, and the OIE industrial index page (https://www.oie.go.th/view/1/mpi/TH-TH) links monthly production and shipment index files for 75 industry groups. The files were not downloaded, because downloading a file needs the user's permission, so it is unknown whether they list carbonated soft drinks and in which unit. With that permission the settling work is: take the monthly carbonated soft drink and soda water series, match it to TMD monthly national mean temperature departures (one summary page per month at tmd.go.th/en/climate/summarymonthly), and regress with month-of-year and year effects. About 68 months is short, and 2021 to 2026 includes the product launches and production halts that the OIE itself cites for 2025. Even then, production or factory sales are not retail sales, and the page does not say whether a soft drink product is listed. The i-Index portal (i.index.oie.go.th) did not respond in the first pass.
2. Thai sales by month (a NielsenIQ or Kantar retail audit, a Statista monthly series, or a bottler's monthly volumes) are paid or private. The Statista page for monthly Thai carbonated drink sales value (June 2024 to June 2026) shows only masked values behind a Premium marker. Buying or requesting any of them needs the user's approval (outside contact and cost). Not attempted.
3. Age and sex differences in temperature response, which decide whether the directional flip condition (about 0.031 per degree Celsius in April, section 6B) is reachable, need purchase data by age and sex cell (a consumer panel). No open source was found. Not attempted.
4. Keles et al. (2018): only the abstract was read. The country, period and data source are unconfirmed in the abstract; full text was behind HTTP 403. The Mirasgedis et al. paper (Business Strategy and the Environment) could not be opened beyond a search-service abstract with no number.
5. He et al. (2025): read through a condensed extract; an Author Correction dated 10 June 2026 was not read; the paper gives grams, not percent of sweetened-beverage purchases, so the percent figure (F6) is for total added sugar only and is a scale check.
6. Roche and de Preux (2024) is a conference abstract; no journal version was found; its per-day effect cannot be turned into a per-degree slope.
7. UK figures (F10, F11, F22) are trade-press claims with no method; the country is stated only on the 2026 page. They carry the lowest weight. The Talysis figure (F22) comes from a single recent hot spell and the page does not name the source in the sentence.
8. Kato (2021), the only source for the Japan direction, was read at abstract level: the ACM publisher page returned HTTP 403, the abstract was read in the OpenAlex record and the paper's existence was confirmed in Crossref, and the paper was not read in full. Hirche, Haensch and Lockshin (2021) was read at the Emerald abstract page only. Both are tier S and neither supplies a number.
9. The Bangkok Post 2023 article quoting a Thai Drinks executive on El Nino heat (paywall, HTTP 402) and the Bloomberg article of 2 February 2026 (HTTP 403) were seen only as search snippets and are not relied on.
10. TMD departures for April and May 2025, and all 2023 months, were not available on the pages read, so no matched year-on-year temperature change was built.
11. Sugar versus zero-sugar response is unresolved (section 5); the cube uses sucralose.
12. The mapping from a sales response to the model's trial-propensity proxy is an assumption (section 3).
13. The only Thai monthly beverage regression found (Suwanvijit, Choonpradub and McNeil 2009, and the 2011 doctoral thesis of the first author) models one company's sparkling beverage revenue in 14 southern provinces for 2000 to 2006 and reports seasonal effects but no temperature variable. If the full text of the journal PDF or of the thesis chapters can be obtained (the repository page shows only five of the 11 thesis files), a Thai seasonal profile for the south may be recoverable. It would mix temperature with rain, the tourist season and Ramadan, and it is about 20 years old. It is a lead, not a coefficient.
14. The Cabinet briefing document is tier S until a copy from the Cabinet Secretariat or the Ministry of Industry is opened. It supports direction only and no figure depends on it.
15. The finer directional rerun (section 6B) describes the results file's own scenario design. It is DERIVED, it is not in the results file, and it does not say what real customers do.

## 9. Search and reading log

- First pass: about 37 web searches (32 standard, 5 extended where standard results were thin) and 3 Consensus searches. Themes: temperature elasticity of soft drink sales (English), the same for carbonated drinks, sugar-sweetened beverage purchases and heat, Thai-language queries on temperature and drink sales, Thai production index and OIE reports, Form 56-1 seasonality, Excise Department data, Asian markets (Japan, Korea, Taiwan, China, Vietnam, India), El Nino and Southeast Asian beverage results.
- First pass: about 45 pages were fetched. Pages that gave usable text are listed in the raw notes. Pages that failed (HTTP 402, 403, 502, timeouts, empty redirects) are listed in asia_and_other_evidence_reviewed.md, section C.
- Revision of 20 October 2026: 6 standard web searches (Kato 2021 by title; Suwanvijit, Choonpradub and McNeil; Hirche, Haensch and Lockshin; Kato by venue; Statista Thai carbonated monthly series; the UK 1.8 percent claim) and 16 fetches. Of the fetches, 3 returned HTTP 403 (ACM page, two kamcity.com pages) and 1 was a redirect to the ACM page. Pages that gave usable text: Crossref and OpenAlex records for Kato 2021, Emerald abstract page for Hirche et al., CCSE abstract page and two PSU repository pages for Suwanvijit, the PSU thesis Abstracts.pdf (read locally), Asian Trader (Talysis 1.8 percent), the Statista page (masked), the TMD climate normals PDF (page 57, read locally), and the two OIE pages. One further direct read of the OpenAlex JSON record was made to rebuild the Kato abstract exactly.
- New leads added to the log by the review: Suwanvijit, Choonpradub and McNeil (2009) and the 2011 thesis (section 8, item 13); the Statista Thai monthly carbonated drink sales value series (premium, masked; section 8, item 2); and the UK trade claim of about 1.8 percent per degree (F22).
- Reading files in the repo: SOURCING_POLICY.md, CLAUDE.md, workflows/update_loop_state_2026-10-20.md, workflows/update_loop_review_2026-10-20.md (section V5), .claude/workflows/update-loop-verify.js (the V5 brief), screen/ambient_variation.py (lines 1 to 814 in the first pass; lines 366 to 500 and 605 to 770 again in the revision), screen/ambient_variation_results.json (reach lens in full and other lenses by script in the first pass; all four lenses walked by script in the revision), rework/78 section 7 (lines 195 to 239), raw/diligence_2026-10-20/T15 search record and TMD note, and rework/83_verify_V4_cpall_margin.md for layout.

## 10. Checks done

- Every figure in section 2 traces to a raw note in rework/raw/update_2026-10-20/V5/ or to the results file; F18 now traces to the source PDF page re-read in the revision.
- The re-run reproduces the results file's fixed-temperature leave-one-out figures to four decimals (0.6858, 0.9734, 0.8478), and in the revision it reproduced every figure of the section 6 table and the file's April directional figures (delta 0, 0.03, 0.04, 0.05) to four decimals.
- The scope statement in sections 1, 6 and 7 was checked against a script that walked every run in the results file (table 6A); the per-lens lists of flipping runs match the file.
- The Bangkok monthly means (F18) were checked against PDF page 57 of the TMD normals: all 12 monthly values and the annual value agree with the values the model uses.
- The rerun was made with python -B -I, no bytecode cache exists in rework/screen, and the modification times of ambient_variation.py and ambient_variation_results.json are unchanged (20 October 2026 06:43).
- No em dash, en dash or middle dot was used in this record or the raw notes (checked by search at the end of the revision).
- Not checked: the Thai text of the Cabinet briefing against a second copy (one copy only, issuer inferred from content); the Author Correction to He et al.; the Kato paper beyond its abstract; any page that returned an error.

## 11. Revision log (20 October 2026, after the review of the same day)

| Review finding | Severity | What was done | Result |
|---|---|---|---|
| Scope overstatement about the results file (answer and section 1 said the only configuration that flips a per-person or per-member leader is the 0.04 older-men condition) | medium | Read the file and walked every run. Reworded to "the only temperature configuration"; added table 6A with the structural sweeps that flip the reach and per-member leaders (confidence "none"); added that the file's per-person flag excludes the directional scenarios; reran the directional scenario on a finer grid (April crossing about 0.031, the file's grid shows 0.04). | Closed. Conclusion that a sourced temperature value changes no leader is unchanged. |
| Japan direction rests on a Consensus abstract record (Kato 2021); Haensch alcohol abstract used in section 5 not opened | medium | Opened what could be opened. Kato: Crossref record and OpenAlex abstract read; ACM page HTTP 403; paper not read in full. Labelled "abstract level, direction only, paper not read in full" in the answer, F23, section 7 and limit 8. Haensch: corrected to Hirche, Haensch and Lockshin (2021); Emerald abstract page opened; labelled S, full text not read, F24. | Closed as stated limits at tier S (abstract level). The paper full text was not reached. |
| Cabinet briefing tiered P though the issuer is inferred | low | Retiered S in the record, F25 and the raw note; used for direction only. | Closed. |
| One source URL for the three OIE carbonated rows | low | Rows F15, F16 and F17 each carry their own URL in the source URL list; the structured result splits them into three. | Closed. |
| Leads missing from the search log (Suwanvijit and co-authors, Statista Thai monthly series, UK 1.8 percent) | low | Opened all three. Added to section 9, limit 2 (Statista) and limit 13 (Suwanvijit as the only Thai monthly beverage regression found, no temperature variable); added the 1.8 percent claim as F22. | Closed. |
| Bangkok monthly mean row described as re-read when only the T15 note was read | low | Re-read PDF page 57 of the TMD climate normals and saved tmd_bangkok_normals_reread_page57.md; F18 wording corrected. | Closed. |

- Verdict unchanged: closed as a stated limit. No sourced coefficient was found. The OIE statistics files that might settle it were not downloaded, and the route is in limit 1.
