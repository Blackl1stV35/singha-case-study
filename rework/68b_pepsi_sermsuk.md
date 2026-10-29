# 68b: The Pepsi system and Sermsuk (est): competitor due diligence (task T3)

Date: 20 October 2026. Re-run of T3 with the listing status verified from primary documents. A third pass on the same day closed the independent verifier's high and medium issues and the low issues. Section 16 lists the changes in each pass; section 17 maps the third-pass verifier issues to their closure, and section 18 maps the fourth-pass issues (13 items: six medium and seven low). This record supports proposal 11 section 2.3 and slide 8. It is a team record. The proposed text for the proposal and the slides is in section 11 and is written for the judges and the executives; everything else is for the team.

Method and limits of the run:

- Saved pages: `rework/raw/diligence_2026-10-20/T3/`. New in the re-run: `rerun_set_delisting_notice_sermsuk_2026-10-20.md` (SET notice), `thaibev_sgx_27nov2024_and_agm_2025_minutes_2026-10-20.md` (ThaiBev announcement of 27 November 2024 and the Sermsuk 2025 AGM minutes, read as page images), `rerun_search_leads_and_blocked_2026-10-20.md` (blocked pages and search snippets that were not used as figures). New in the third pass: `sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md` (Suntory Beverage & Food annual securities reports for FY2023, FY2024 and FY2025 from EDINET, Asia Pacific segment and Thai commentary) and `mini_me_2025-03-30_opened_2026-10-20.md` (the Mini Me article, opened on 20 October 2026). Earlier files in the same folder are cited by name.
- Numbers come from two scripts and their results files: `rework/screen/t3_pepsi_sermsuk_margins.py` (results `t3_pepsi_sermsuk_margins_results.json`: margins, prices per 330 mL, share sums, mass ratio, Asia Pacific series) and `rework/screen/t3_rerun_listing_checks.py` (results `t3_rerun_listing_checks_results.json`: tender holdings, tender value, Sermsuk arithmetic, the 64.67% holding check, Asia Pacific margin checks). No random numbers.
- Tiers follow `rework/SOURCING_POLICY.md` and `rework/submission/appendix_a_tier_key.md`. P is primary (filing, exchange notice, issuer announcement, company minutes, annual securities report). S is secondary (trade press, aggregators, retailer pages). A WebFetch read is an extract made by a small model; where the saved file is the text of a page image, or a text layer extracted locally from a saved PDF, it says so.
- Blocked in this run: Suntory's investor pages and the company's quarterly supplemental releases (HTTP 403, including the 2023 and 2024 fourth-quarter supplementals, the 2024 and 2025 fourth-quarter releases and the 2017 joint venture release); the Department of Business Development statements for the Pepsi bottler (aggregators login-only or 403; DBD data warehouse 404). The Suntory annual securities reports on EDINET were readable and are used.

## 1. Findings in brief

1. **"S Cola 8.6%" is est (Thai: เอส), a ThaiBev group brand.** The trademark belongs to the ThaiBev group: Sermsuk's own filing says its subsidiary Great Brands Limited sold the est brand and trademark to Super Brands Company Pte. Ltd. in 2014, and that the manufacturing contract is with ThaiBev, "who owns the trademark" (Sermsuk Form 250-2, pages 8 and 64, P). The 2014 press names International Beverage Holdings Limited as the buyer for THB 1.56 billion (S); the two buyer names are not linked by any page read. Sermsuk Public Company Limited makes it. Thai Drinks Co., Ltd. is named by the press as the marketer (S). The 8.6% is a volume share printed by Thansettakij on 16 March 2024 with no year and no data owner (S). The latest est figure is 10.6%, stated in Thansettakij's article of 13 October 2025 with no named source, and the basis is not stated (S).
2. **There are two systems, not one.** Pepsi, 7UP and Mirinda are made and sold in Thailand by Suntory PepsiCo Beverage (Thailand) Co., Ltd. (SPBT), a joint venture in which Suntory Beverage & Food held 51.0% at 31 December 2022 (P, securities report page 116) and in the FY2023 to FY2025 annual reports (P, subsidiaries table). PepsiCo's Thai company, Pepsi-Cola (Thai) Trading Co., Ltd., is reported to hold the other 49% (S, 2017 press). The venture started on 5 March 2018 (S). Before that, PepsiCo ran its own Thai company from 2 November 2012 after Sermsuk's Pepsi contract ended on 1 November 2012 (S). Sermsuk is therefore a rival of the Pepsi system, not part of it.
3. **Sermsuk is no longer listed.** ThaiBev's subsidiary So Water Company Limited acquired 34.52% of Sermsuk's shares (91,786,404 shares) in a tender offer for delisting, run from 19 September to 22 November 2024 at THB 63 a share, and then held 99.19% (263,741,208 shares) (P, ThaiBev announcement to SGX of 27 November 2024, read as a page image). The SET notice of 11 December 2024 (P) states that the SET approved the delisting of SSC's common stocks from 20 December 2024, with 19 December 2024 as the last trading day. Sermsuk's 2025 AGM minutes of 30 January 2025 record that "the Company has been delisted from the SET" (P, page 23). No later document was read. The listing status in October 2026 is therefore the January 2025 position, with no sign of a relisting (stated limit).
4. **Financials found.** Sermsuk (consolidated, year end 30 September, three years from SET filings): gross margin 28.26%, 28.30% and 29.25%; net margin 0.12%, 2.00% and 3.07% for FY2022, FY2023 and FY2024 (P, DERIVED). The FY2024 figures are confirmed by the 2025 AGM minutes (revenue THB 13,153 million, page 14, P). PepsiCo, Inc., the global brand owner and franchisor that holds 49% of the Thai bottler through its Thai company: gross margin 54.21%, 54.55%, 54.15% and net margin 9.92%, 10.43%, 8.77% for FY2023 to FY2025 (P, DERIVED). ThaiBev's non-alcoholic segment (a group segment): gross margin 33.77% (FY2023, derived), 36.00% (FY2024) and 36.58% (FY2025) (P, DERIVED). As a PROXY for the Pepsi bottler, Suntory Beverage & Food's Asia Pacific segment, which consolidates SPBT, reported segment profit of JPY 43.1 billion on revenue of JPY 371.4 billion in 2023 (11.60%), JPY 45.4 billion on JPY 402.0 billion in 2024 (11.29%) and JPY 42.5 billion on JPY 394.1 billion in 2025 (10.79%) (P, annual securities reports; PROXY; a segment profit ratio, not a gross or net margin; the segment also covers Vietnam, Indonesia, Oceania and health foods). **Not found:** revenue and profit of SPBT and of Pepsi-Cola (Thai) Trading (section 7.4).
5. **Price.** A 7UP Zero Sugar Lemon Soda six-pack costs THB 75 at Lotus's (THB 12.69 per 330 mL), and a single 7UP lemon soda no-sugar pack at THB 16 on the Lotus's Shop Online row shown by Priceza (THB 16.25 per 330 mL), 20 October 2026 (S). The 7UP lemon listings run from THB 12.40 to THB 16.25 per 330 mL. est cola costs THB 79 for six at Makro PRO, a cash-and-carry listing, THB 13.37 per 330 mL (S). No like-for-like Pepsi shelf price from a hypermarket was found.
6. **Cube.** The can systems can copy the lemon flavour and a price promotion quickly, and a zero-sugar lemon-lime can already exists (7UP Zero Sugar Lemon Soda). What they cannot copy quickly is the form: the packed Lemon Soda unit is about 1.6% of the mass of the 330 mL it makes (5.29 g against 330 g). That figure is 3.79 g of dry mass, which already includes the 0.80 g binder and filler, plus an assumed 1.5 g pouch; nothing was weighed, so the 1.6% is DERIVED from an ASSUMPTION. This is team analysis (ASSUMPTION), not a sourced statement about either company's plans.
7. **Conflicts with current text** are listed in section 12.

## 2. Entity map: ownership and role

| Entity | Group | Role | Ownership and status | Tier |
|---|---|---|---|---|
| PepsiCo, Inc. | PepsiCo (NYSE: PEP) | Brand owner and franchisor of Pepsi, Mirinda and 7UP in Thailand; retains marketing and innovation for them in the joint venture | Listed parent. Thai trademark holder not confirmed by a registry; a 2003 trade press item names Pepsi-Cola (Thai) Trading as the owner of the Pepsi, Mirinda and 7-Up trademarks in Thailand | S (The Nation, 2 Nov 2017); trademark holder UNVERIFIED |
| Pepsi-Cola (Thai) Trading Co., Ltd. | PepsiCo | PepsiCo's Thai company. Ran Pepsi's own production and distribution from 2 Nov 2012 after the Sermsuk contract ended; sold 51% of International Refreshment (Thailand) Co., Ltd. to Suntory Beverage & Food Asia in 2017 and is reported to keep 49% | PepsiCo subsidiary. Registry number and statements not found | S (MGR Online 25 Oct 2012; M&A Online and Prachachat, 2017) |
| Suntory PepsiCo Beverage (Thailand) Co., Ltd. (SPBT), formerly International Refreshment (Thailand) Co., Ltd. | Joint venture of Suntory Beverage & Food and PepsiCo's Thai company; consolidated subsidiary of Suntory Beverage & Food | Bottler and distributor of Pepsi, 7UP, Mirinda, Gatorade, Lipton and Aquafina, and of Suntory-linked brands | Suntory 51.0% at 31 Dec 2022 (P, FY2022 report page 116) and shown at 51.0% in the subsidiaries tables of the FY2023, FY2024 and FY2025 reports (P, saved in `sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md`); 49% PepsiCo side per the 2017 announcement (S). Registered 18 Nov 2003, registration number 0105546139004 (S, Creden registry page, a DBD aggregator). Started in March 2018 (5 Mar per Brand Inside and Bangkok Biznews, S). Plants at Rayong and Saraburi | 51.0%: P; 49%, 2018 start and plants: S |
| Sermsuk Public Company Limited (formerly SET: SSC) | ThaiBev | Maker and distributor of est under a manufacturing contract with the ThaiBev trademark owner; maker of Crystal drinking water, Ranger, Power Plus, V-Boost, 100Plus and others; distributor of Oishi, Chang mineral water and Rock Mountain soda water. Bottled and distributed Pepsi until 1 Nov 2012 (S) | Established 1952 (P, ThaiBev announcement of 3 July 2024). Its own history lists "1975: being a listed company" and "1994: became a listed company" (P, Form 250-2 history; not reconciled). So Water 99.19% on 27 Nov 2024 (P). Delisted from the SET, effective 20 Dec 2024 (P, SET notice; P, AGM minutes 30 Jan 2025). Fiscal year end 30 September | P |
| So Water Company Limited | ThaiBev (indirect, wholly owned subsidiary per the ThaiBev announcement) | Holding company for ThaiBev's beverage business; holds 99.19% of Sermsuk (after the tender offer), 99.84% of S.P.M. Foods & Beverages and 4.95% of Thai Drinks Co., Ltd. Holding of Sermsuk was 64.67% at the 6 December 2023 and 17 July 2024 record dates | Named in the Form 250-2 (pages 42 and 94) and in the ThaiBev announcements | P |
| est (เอส, "S Cola") | ThaiBev group | Brand. Trademark: sold by Great Brands Limited to Super Brands Company Pte. Ltd. in 2014 (P), and held in the ThaiBev group ("ThaiBev, who owns the trademark", P). Buyer named in 2014 press: International Beverage Holdings Limited (S). Maker: Sermsuk. Marketer: Thai Drinks Co., Ltd. (S) | Launched 2012 (P for the year, Form 250-2 page 8; S for the day) | P (Form 250-2 pages 8, 42, 64); S (press) |
| Thai Drinks Co., Ltd. (also written Thai Drink Co., Ltd. in some press) | Press calls it a ThaiBev group company (Bangkok Biznews, about October 2023, S); Gotomanager (29 October 2023, S) places it in the ThaiBev chain as marketer | Marketer of est (press, S). Business: manufacture and distribution of beverages and beverage concentrate (Form 250-2, page 42, P) | So Water holds 4.95% (P, Form 250-2 page 42). Gotomanager (29 October 2023, S) says in its owner chain (team translation of the saved extract) that "Thai Beverage Logistics later became the major shareholder, within the ThaiBev group"; the sentence does not say which company it describes, so it is recorded as a lead only and not as evidence of control. The controlling holder was not found, so "group company" is a press claim | P for the 4.95% stake; S for the role and for the group label |

Reading: the est trademark sale in 2014 is recorded in the Sermsuk filing (Super Brands) and the press (International Beverage Holdings); both are described as ThaiBev group entities, and no page read links them to each other. This record gives both names as printed.

## 3. What "S Cola 8.6%" refers to, the share reports, and the market value

### 3.1 The deck line

The deck line is: "Brand shares 2023 to 2024: Coca-Cola group 51%, Pepsi 30%, S Cola 8.6% (volume)". It comes from Thansettakij, 16 March 2024 (S). The article says Coca-Cola holds 51% (Coke, Fanta and Sprite); "Pepsi is number two with 30%"; S Cola "keeps a volume market share of 8.6%" and is third. The three figures sit in one opening paragraph with no year and no data owner. Only the 8.6% is described as a volume share. The Thansettakij list of 3 April 2025 names the company behind "S" as Thai Drinks Co., Ltd. and the Pepsi company as Suntory PepsiCo Beverage (Thailand) Co., Ltd., which supports reading S Cola as est.

### 3.2 Share reports as printed

Script results `share_reports_as_printed` (all S unless stated). "Sum" is shown only for rows that print three or more shares.

| Date | Source | est | Coke | Pepsi | Other | Sum | Base as printed |
|---|---|---|---|---|---|---|---|
| 13 Mar 2023 | Thansettakij 558785 (read by T4) | 8% | | | | | not stated |
| 21 Mar 2023 | Positioning 1424257 (T1 row 1) | 8% | 51% | 37% | Big Cola 3%, others 1% | 100.0 | ThaiBev table "partly Nielsen"; year and measure not stated |
| 17 Oct 2023 | Brand Buffet (T4) | 9.1% (was 7.1%) | | | | | not stated |
| 29 Oct 2023 | Gotomanager 5234 | 9.1% (was 7%) | 54% | 30% | | 93.1 | est volume share for August 2023; others not stated |
| 15 Mar 2024 | Marketeer 345506 (T4) | 8.9% | | | | | est volume |
| 16 Mar 2024 | Thansettakij 590894 | 8.6% | 51% | 30% | | 89.6 | est volume; year not stated |
| 15 Apr 2024 | Thairath 2778345 | 9% | 51% | 30% | | 90.0 | not stated |
| 12 Mar 2025 | Marketeer 406131 (read by T4) | 8.9% (reference March 2024) | | | Big Cola 6% | | not stated |
| 26 Mar 2025 | Thansettakij 623088 | | 51% | 39.1% | | | "of the dark cola market"; year not stated |
| 3 Apr 2025 | Thansettakij 624003 | 8.9% | 51% | 39% | Big Cola 5% | 103.9 | "Thai carbonated soft drink market" as printed; no year, no data owner |
| 17 Apr 2025 | Brand Buffet 2025/04 (suntory-pepsico-beverage-strategy-2025) | | 51% | 39.1% | | | "of the dark cola segment"; year not stated |
| 30 Mar 2025 | Mini Me Insights (opened 20 October 2026; citing Prachachat for the investment figures only) | | | 39.1% | | | "current market share"; basis not stated; 2025 target 40% |
| 13 Oct 2025 | Thansettakij 641276 (read by T4) | 10.6% (was 7% before the rebrand); 24.6% of colour soda, number 2 there | | | | | est total soda share; basis not stated |

Reading (script `share_summary`):

- est is between 8.0% and 10.6% in the ten reports from March 2023 to October 2025. The 8.6% of the deck is inside that band and is not the latest figure: the latest, in Thansettakij's article of 13 October 2025 with no named source, is 10.6%, with the basis not stated. The Marketeer story of 15 March 2024 prints 8.9% as a volume share for the same period for which Thansettakij prints 8.6%; neither article reconciles them.
- Pepsi takes four values: 30% (Gotomanager October 2023, Thansettakij March 2024, Thairath April 2024), 37% (the March 2023 ThaiBev table, the only row that sums to 100), and 39% to 39.1% (March and April 2025; the Mini Me article of 30 March 2025, opened on 20 October 2026, gives 39.1% with no basis; two of the three 2025 reports say "dark cola"). The bases differ and are not stated, so a single like-for-like Pepsi share is not available; the range is 30% to 39.1%.
- The rows that print three or more shares sum to 89.6% to 103.9%. Only the March 2023 ThaiBev table sums to 100; the 3 April 2025 list sums above 100, so its figures come from different bases.
- The Mini Me article repeats the 39.1% and gives a 2025 target of 40%. It attributes only the investment figures and the CEO remarks to Prachachat; no source is given for the share. No 2025 NielsenIQ or Kantar share table was found (stated limit).
- Earlier references: 2019 brand shares (Nielsen as printed) Coke 35.7%, Pepsi 25.4%, Fanta 15.6%; est estimated at 10.3% (Positioning, 26 Mar 2020, S); about 10% in 2016 (Brand Buffet, 10 Mar 2016, S).

### 3.3 Market value statements

Script `market_value_statements_as_printed` (all S). Record 67 (`67_market_size_source_check.md`) traced the windows; the rows are in `rework/raw/diligence_2026-10-20/T1/nielseniq_press_series_2023_2026.md` and block 10 of `csd_market_share_press_2020_2025.md`.

| Value (THB million) | Where printed | Window or year | Tier |
|---|---|---|---|
| over 62,000 | Gotomanager 29 Oct 2023; Brand Buffet 17 Oct 2023; Thairath 10 Oct 2023 | not stated (Thairath: growth period September 2022 to August 2023) | S |
| 66,000 | Marketeer 15 Mar 2024 and MarketPlus 8 May 2024 attribute the value to NielsenIQ for February 2023 to January 2024 (growth 12%). Thansettakij 16 Mar 2024 prints the same window and the +12% as NielsenIQ growth rates, but gives no source for the value. Repeated in Thansettakij 26 Mar and 3 Apr 2025 and Brand Buffet 17 Apr 2025 | NielsenIQ, February 2023 to January 2024, +12% (as attributed by Marketeer and MarketPlus) | S |
| 70,772 | Thansettakij 14 Jan 2025 | NielsenIQ via ThaiBev, 12 months to November 2024, +9% | S |
| 68,000 (about 67,000 in Bangkokbiznews) | Thansettakij and Bangkokbiznews 13 Oct 2025 | the pages label 2024 and 2025; may be a 2025 level. In Thansettakij the 68,000 figure is credited to a ThaiBev senior director (re-read 20 October 2026) | S |
| 76,900 | Kasikorn Research Center via Thansettakij 8 Sep 2025 and Marketeer 9 May 2025 | 2025 estimate or forecast | S |

Reading:

- The values run from THB 62,000 million to THB 76,900 million for 2023 to 2025. Outlets label the same value with years that differ by one, so this record does not call 66,000 either "2023" or "2024".
- The best-supported single value is THB 70,772 million for the 12 months to November 2024 (NielsenIQ, S). No source states whether any value is at retail or manufacturer level (stated limit).

### 3.4 The colour-soda segment, where lemon-lime sits

The press splits the market into cola (น้ำดำ, "dark") and colour soda (น้ำสี, the non-cola segment that holds lemon-lime; the label is the segment name and not the colour of the liquid).

- Thansettakij, 13 October 2025 (S, no named source in the article; re-read 20 October 2026): colour soda THB 17,391 million, printed as "30% of the total market"; 17,391 is 25.57% of 68,000 and 24.57% of 70,772, so the printed 30% does not fit (the inconsistency is inside the source). The 30% is therefore not used.
- Bangkokbiznews, 13 October 2025 (S): colour soda THB 17,300 million for September 2024 to August 2025 per NielsenIQ.
- est holds 24.6% of colour soda and is number 2 in it; its colour range reached 13 flavours with est Glow Edition (4 new flavours).
- No size for lemon-lime alone was found (stated limit).

## 4. Brands in the lemon, lime, clear carbonated and sugar-free lines, with dates

| Brand and line | System | What it is | Launch or change date | Evidence | Tier |
|---|---|---|---|---|---|
| 7UP | Pepsi | Clear lemon-lime carbonated soft drink | Produced at PepsiCo's new Thai plant and sold through all channels from 2 Nov 2012 under Pepsi-Cola (Thai) Trading; earlier Thai history not found. 2019 growth 5%; the press says Pepsi is reviving 7-Up (March 2020) | MGR Online 25 Oct 2012; Positioning 26 Mar 2020 | S |
| 7UP Low Sugar | Pepsi | Low-sugar version | About 2018: listed among reduced-sugar products after the March 2018 start (page undated, read as about September 2018) | Bangkok Biznews 812103 | S |
| 7UP Free | Pepsi | Sugar-free lemon-lime, no colour, no caffeine | Reported 23 Feb 2020 as launching in Thailand; Positioning 26 Mar 2020 calls it a new product to test the market worldwide; Thai date not stated | Mini Me Insights, 23 Feb 2020; Positioning | S |
| 7UP Free + Fibre | Pepsi | Sugar-free with added fibre; 325 mL can, 440 mL PET | Reported 8 Aug 2021 | Mini Me Insights | S |
| 7UP, now "100% no sugar" | Pepsi | Reformulation | Reported 17 Apr 2025 | Brand Buffet | S (company statement relayed) |
| 7UP Zero Sugar Lemon Soda and Strawberry Lemon | Pepsi | 325 mL packs; the Lotus's page reads "7 UP ZERO SUGAR LEMON SODA 325 ML. PACK6" (six-pack; the page does not use the word "can"); "ZERO SUGAR" is in the product name | Listed 20 Oct 2026 on opened Lotus's pages; launch dates not found | Lotus's (T5), re-read 20 Oct 2026 | S |
| 7UP Zero Sugar Pineapple Peach | Pepsi | 325 mL cans | Listed 20 Oct 2026 on a Priceza row (page not opened); launch date not found | Priceza (T5) | S |
| Mirinda | Pepsi | No lemon or lime variant found. Flavours named: Mirinda Mix-It (two fruit flavours in one bottle) and green cream. Full flavour list not established | Mix-It about 2018 (Bangkok Biznews 812103); green cream announced 26 Mar 2020 for around mid-2020 with a new global look (a plan, not a confirmed date) | Bangkok Biznews 812103; Positioning 26 Mar 2020 | S |
| Pepsi (cola) | Pepsi | Pepsi Max Test (sugar-free) listed about 2018 (Bangkok Biznews); sugar-free Pepsi grew 19% (Thansettakij 27 Mar 2023) and 16.1% on average (26 Mar 2025); plum flavour 2025; Pepsi Treats Strawberry 'N' Cream (zero sugar), May 2026; Chocolate Dubai, July 2026. No lemon or lime Pepsi found | As listed | Bangkok Biznews; Thansettakij 27 Mar 2023 and 26 Mar 2025; company news 7 May 2026; Workpoint 10 Jul 2026 | S; the May 2026 launch is P as a company statement |
| est cola | ThaiBev | Cola | 2012 (launch day 2 Nov 2012) | Form 250-2 page 8 (year); Gotomanager (day) | P (year); S (day) |
| est Sugar Free | ThaiBev | Sugar-free est; the 325 mL six-pack listing does not state the flavour | In the range at the March 2023 relaunch | Thansettakij 13 Mar 2023 (read by T4); Lazada via Priceza (T4) | S |
| est Lemon Lime | ThaiBev | Lemon-lime soft drink, one of eight est flavours; the press counts it in the colour-soda (น้ำสี) segment | Named "est Clear" until 2015, "est Play" lemon-lime from 2015, "Play" dropped in March 2023; in Sermsuk's Oct 2024 flavour list. The saved page does not say whether the liquid is colourless | Brand Buffet 10 Mar 2016 (T4); Form 250-2 page 9 | P for the 2024 flavour list; S for the history |
| est Kamikaze Lime | ThaiBev | Lime flavour on sale | Listed 20 Oct 2026 | Lazada via Priceza (T4) | S |
| est Glow Edition | ThaiBev | 4 new flavours; colour range 13 flavours | 13 Oct 2025 | Thansettakij 641276 (T4) | S |
| Rock Mountain soda water | ThaiBev (Sermsuk) | Clear soda water, 325 mL bottles | Launched 2016 | Form 250-2 pages 8 and 10; 7-Eleven online (T5) | P and S |
| Chang Soda | ThaiBev | Clear soda water | Chang Soda and Chang Water: 122.8 million litres in FY2024 (+8.2%, FY2024 announcement). Water and Soda: 127.6 million litres in FY2025 (down 4.0%, FY2025 announcement). The two series have different scopes and are not comparable; no growth rate is taken across them | ThaiBev SGX year-end announcements (read by T4) | P |

Lemon and lime reading: the Pepsi system's clear lemon-lime line is 7UP, now zero sugar; no Pepsi or Mirinda lemon variant was found. The ThaiBev system has est Lemon Lime (a lemon-lime soft drink in the colour-soda segment) and est Kamikaze Lime as fruit sodas, and Rock Mountain and Chang Soda as clear soda water. No lemon soda in 330 mL was found in the pages read; this is not a full market survey. A 2026 7UP Extra Fizz zero-sugar line appeared only in a search snippet (the company page returned HTTP 403); it is listed in the limits and not used.

## 5. Shelf price, pack and price per 330 mL

Retail rows were read on 19 and 20 October 2026 and saved by other tasks (`retail_price_inputs_from_T4_T5.md` lists each row and its source page). Price per 330 mL is the listed pack price divided by the units, scaled by 330 over the unit size (script results `price_per_330ml_thb`). All S.

| Product | Pack | Price (THB) | Per unit (THB) | Per 330 mL (THB) | Retailer |
|---|---|---|---|---|---|
| 7UP Zero Sugar Lemon Soda | 6 x 325 mL (PACK6) | 75 | 12.50 | 12.69 | Lotus's (page opened; prints "฿75.00/Each" with the PACK6 name, read as the six-pack price) |
| 7UP no-sugar lemon soda | 1 x 325 mL (single) | 16 | 16.00 | 16.25 | Lotus's Shop Online row shown by Priceza (the Lotus's single-pack page was not opened) |
| 7UP lemon soda no sugar (official Suntory PepsiCo store) | 6 x 325 mL | 96 | 16.00 | 16.25 | LazMall via Priceza |
| same | 24 x 325 mL | 293 | 12.21 | 12.40 | LazMall via Priceza |
| est cola | 6 x 325 mL | 79 | 13.17 | 13.37 | Makro PRO, a cash-and-carry listing that says it cannot be delivered to the selected area |
| est cola | 6 x 325 mL | 138 | 23.00 | 23.35 | 7-Eleven online |
| est Sugar Free (flavour not stated) | 6 x 325 mL | 99 | 16.50 | 16.75 | Lazada seller "Sermsuk Click" via Priceza |
| Pepsi | 6 x 325 mL | 167 | 27.83 | 28.26 | 7-Eleven online |
| Sprite (reference) | 6 x 325 mL | 85 | 14.17 | 14.38 | Lotus's |
| Singha Lemon Soda can (reference only; see section 12, conflict 14) | 6 x 330 mL | 85 | 14.17 | 14.17 | Lotus's (rows L8, T5) |
| Singha Lemon Soda can (reference only; see section 12, conflict 14) | 1 x 330 mL | 17 | 17.00 | 17.00 | Lotus's (row L7, T5) |
| Singha Lemon Soda can (reference only) | 6 x 330 mL | 172 | 28.67 | 28.67 | 7-Eleven ALL Online (page A2, T5) |

Reading:

- The 7UP zero-sugar lemon listings span THB 12.40 to THB 16.25 per 330 mL. The judge-facing range uses only the 7UP rows and the Sprite six-pack: the six-packs are THB 12.69 (7UP at Lotus's) and 14.38 (Sprite at Lotus's), and the single pack THB 16.25 (7UP, via Priceza). The Singha Lemon Soda rows are reference rows only, because the deck and submission say the Singha can price is not verified (section 12, conflict 14). The Lemon Soda planning shelf price of THB 15 is an assumption; it sits between the 7UP six-pack and single-pack levels (script `price_position_of_lemon_soda_assumption`). The official 7UP store on LazMall prices its six-pack at the single-pack level (16.25) and its 24-pack at 12.40, so the multipack level is not uniform. The record does not claim price parity.
- 7-Eleven online prices run about twice those of Lotus's for the same pack (Singha Lemon Soda six-pack THB 172 against THB 85, ratio 2.02). The 7-Eleven Pepsi and est rows are not comparable with the Lotus's rows. The est Makro PRO row is a cash-and-carry listing. No Pepsi row from Lotus's, Makro or another hypermarket page was found, so a like-for-like Pepsi price and a consumer-level est price are UNVERIFIED and are left out of the proposed slide comparison except as labelled rows.
- Sermsuk's average selling price for carbonated drinks is THB 18.42 a litre (the adviser's assumption table in Form 250-2, page 63, P), which is THB 6.08 per 330 mL (DERIVED). It is an average net price across all est packs, shown only as the order of magnitude of what a bottler receives. It is not a shelf price.
- Trade terms, by who they concern:
  - Pepsi system: a Lotus's promotion on the 7UP pages, "Buy SUNTORY PEPSICO products worth 199 baht get 30 coins" (a retailer scheme naming Suntory PepsiCo products; S, 20 Oct 2026). SPBT said in March 2023 it would hold prices in 2023 and treat a rise as a last resort (S, Thansettakij 27 Mar 2023).
  - est: no promotion funded by est or Sermsuk was found. In 2013 an est 12-bottle case cost THB 125 upcountry against Coke at THB 130 (S, dated).
  - Market-wide (no brand named): store checks by the Thansettakij reporter in April 2025 found shelf price cuts averaging THB 5 to 10 a bottle (S).
- No list-price change by Pepsi, 7UP, Mirinda or est between 2023 and 2026 was found (limit, section 13).

## 6. Channels and distribution

Pepsi system (SPBT):

- At launch in 2018: 25 distribution partners, 68 delivery points and over 470,000 retail outlets (Bangkok Biznews 812103, undated, read as about September 2018, S; dated, not a current count). In 2012 the build used DHL and local distributors through 50 distribution centres (MGR Online, S).
- March 2023: the company said it was widening its partner base across modern trade, traditional trade and restaurant networks, and that e-commerce sales doubled (Thansettakij 560215, 27 March 2023, chief executive Achit Joshi; S). An official store on LazMall lists 7UP in 6, 12 and 24 can packs (Priceza, S).
- Packs seen: 7UP in 325 mL cans and 440 mL PET (2021 launch article); Pepsi 550 mL (the recycled-PET bottle, 2023 release), 325 mL cans, 330 mL bottles in a 24-pack and 1.95 L at 7-Eleven online (T5 page).

est (ThaiBev system):

- Traditional trade and restaurants: over 100,000 grocery shops nationwide plus restaurants (Bangkok Biznews about October 2023, S). est held 12% of the restaurant channel and ranked first there (Thansettakij 13 Mar 2023, read by T4, S). From October 2025 each est colour flavour is sold in one main channel, for example 7-Eleven, Lotus's, Makro or Big C (Thansettakij 641276, S).
- Sermsuk uses direct and indirect channels from small shops to wholesale stores and restaurants, and uses the ThaiBev group's logistics network (ThaiBev announcement 3 Jul 2024; COMPANY CLAIM).
- est sales by pack: PET 64%, glass 18%, cans 2% to 3%; by region Bangkok 37%, Central 28%, Northeast 19%, North 10%, South 5% (Thansettakij 16 Mar 2024, S). Marketeer 15 Mar 2024 prints PET 70%, glass 18%, can 12%, so the two pack mixes disagree.
- 2013 reference: over 200,000 outlets and 50 distribution centres (Bangkok Biznews 2013, read by T4, S; dated).

## 7. Financials

### 7.1 Sermsuk Public Company Limited and its subsidiaries (consolidated; fiscal year end 30 September; THB million)

| Year | Sales and services | Cost of sales | Gross profit | Gross margin (as filed) | Gross margin (computed) | Net profit | Net margin | Tier |
|---|---|---|---|---|---|---|---|---|
| FY2022 (to 30 Sep 2022) | 10,905 | 7,824 | 3,081 | 28.26% | 28.26% from unrounded Form 250-2 lines; 28.25% from whole-million MD&A figures | 13 | 0.12% | P (SET MD&A, 16 Nov 2022; Form 250-2); margins DERIVED |
| FY2023 (to 30 Sep 2023) | 12,371 | 8,870 | 3,501 | 28.30% | 28.30% (both ways) | 248 | 2.00% | P (SET MD&A, 15 Nov 2023); DERIVED |
| FY2024 (to 30 Sep 2024) | 13,153 | 9,306 | 3,847 | not in the MD&A for the full year (nine months to 30 Jun 2024: 29.47%) | 29.25% | 404 | 3.07% | P (SET MD&A, 15 Nov 2024; 2025 AGM minutes page 14, which confirm revenue, cost of sales, distribution and net profit); DERIVED |

- FY2024 details confirmed at the 2025 AGM (minutes of 30 January 2025, page 14, P): cost of distribution THB 3,033 million (23.06% of sales, +5%), administrative expenses THB 736 million (+7%), net profit THB 404 million, up THB 156 million or 63% (so FY2023 is THB 248 million, which reconciles with the MD&A; script `sermsuk_fy24_checks`). The AGM approved these financial statements on 30 January 2025.
- Sales growth: 13.44% in FY2023 and 6.32% in FY2024 (DERIVED). The MD&A says est and Crystal drove FY2023 and FY2024.
- Gross margin check: the Form 250-2 (company opinion, page 16) states gross margins of 30.93% (FY2021), 28.26% (FY2022), 28.30% (FY2023) and 29.47% (nine months to 30 Jun 2024). The unrounded lines reproduce 28.26% and 28.30%; the whole-million MD&A inputs give 28.25% for FY2022, a 0.01 point rounding difference. This record uses the filed 28.26%.
- FY2022 net profit was THB 13 million after THB 67 million of tax on deferred tax assets. The normalised figures in the MD&A (THB 169 million in FY2022, THB 283 million in FY2023) are not used.
- Mix, FY2023: carbonated soft drinks THB 4,550.15 million (36.78% of sales) and non-carbonated drinks THB 7,820.88 million (63.22%) (Form 250-2 page 11, P). Carbonated drinks, mostly est, are about 37% of Sermsuk's sales.
- Net profit is the MD&A's "net profit of the Company"; the split to owners of the parent was not read.
- FY2025 (year to 30 September 2025) was not found: no Sermsuk filing after the FY2024 statements appears in the SEC index read, and the company is delisted (limit, section 13).

### 7.2 PepsiCo, Inc. (group, global consolidated; fiscal year ends the last Saturday of December; USD million)

| Year | Revenue | Gross profit | Gross margin | Net income to PepsiCo | Net margin | Tier |
|---|---|---|---|---|---|---|
| FY2023 (to 30 Dec 2023) | 91,471 | 49,590 | 54.21% | 9,074 | 9.92% | P (SEC XBRL, 10-K filed 9 Feb 2024); DERIVED |
| FY2024 (to 28 Dec 2024) | 91,854 | 50,110 | 54.55% | 9,578 | 10.43% | P (10-K filed 4 Feb 2025); DERIVED |
| FY2025 (to 27 Dec 2025) | 93,925 | 50,859 | 54.15% | 8,240 | 8.77% | P (10-K filed 3 Feb 2026); DERIVED |

The proposal already carries the FY2025 row (about 54.1% and about 8.8%). This is the global group and franchisor, not the Thai bottler and not the Thai entity. PepsiCo's Thai company holds the 49% side of SPBT, which Suntory Beverage & Food consolidates as a 51.0% subsidiary (securities report page 116 for FY2022 and the subsidiaries tables of FY2023 to FY2025, P; how PepsiCo accounts for its 49% was not read).

### 7.3 ThaiBev non-alcoholic beverages segment (group segment of Thai Beverage PCL; fiscal year end 30 September; THB million)

| Year | Sales | Gross profit | Gross margin | Profit for the year | Margin | Attributable to owners | Tier |
|---|---|---|---|---|---|---|---|
| FY2023 | 63,143 | 21,323 | 33.77% | 5,430 | 8.60% | 1,196 | P, DERIVED from the changes stated in the FY2024 announcement |
| FY2024 | 65,802 | 23,688 | 36.00% | 5,934 | 9.02% | 1,455 | P (SGX year-end announcement, read by T4) |
| FY2024 comparative in the FY2025 announcement | not restated here | | | | | 1,146 | P (FY2025 SGX year-end announcement, by-business table; see the note below the table) |
| FY2025 | 64,774 | 23,694 | 36.58% | 5,141 | 7.94% | 2,414 | P (SGX year-end announcement, read by T4) |

This segment contains Sermsuk, F&N, Oishi and dairies, so it is not a Thai-only or soda-only figure. In FY2024 its carbonated soft drink volume rose 48.2 million litres, or 19.2% (P, ThaiBev FY2024 announcement read by T4).

Non-Alcohol attributable profit, two bases (P; script `fourth_pass_thaibev_fy24_non_alcohol_basis`): the FY2024 announcement gives 1,455 million baht for FY2024, up 259 million or 21.7% on 1,196 million for FY2023. The FY2025 announcement gives 1,146 million for the FY2024 comparative in its by-business table, and its Others row moves from 2,191 million to 2,500 million. Both splits sum to the same total of 27,215 million, so 309 million baht moved between the two rows. The FY2025 extract does not label this a restatement. The FY2025 figure of 2,414 million is up 110.6% as printed, which is measured from 1,146 (65.9% from 1,455). The FY2024 announcement's table prints a movement of 251 on the Beer-row numbers, which does not reconcile to the narrative 259; the record uses the narrative.

### 7.4 SPBT and Pepsi-Cola (Thai) Trading: entity figures not obtained; one PROXY with three years

- **SPBT (Pepsi bottler, Thailand).** Statements are filed with the Department of Business Development. The Creden registry page (S, DBD aggregator, saved in `spbt_ownership_and_jv_press_2017_2018.md`, block 7) lists statements as filed for 2021 to 2025 but shows no revenue, profit or assets without a login. The DBD data warehouse returned HTTP 404 and a second aggregator HTTP 403. A juristic-number search in this run returned press and market pages only. No revenue, gross profit or net profit of SPBT is reported here (UNVERIFIED; the DBD statements for FY2023 to FY2025 would settle it).
- **Pepsi-Cola (Thai) Trading Co., Ltd.** Business+ (8 Jan 2024, S) prints total revenue THB 11,226 million and net profit THB 2,487 million for 2022 and gross margins of 37.18% and 43.46% for the same year. The article is internally inconsistent (revenue less costs of THB 8,547 million gives THB 2,679 million, and the margin text does not follow from the totals). It is a lead only and is not used. UNVERIFIED.
- **PROXY for the Pepsi bottler: Suntory Beverage & Food Limited, Asia Pacific business segment, FY2023 to FY2025 (annual securities reports on EDINET, P).** Saved text: `sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md`. Figures in JPY million (external segment revenue; segment profit as printed in each report's segment table):

| Year (report) | Segment revenue | Segment profit | Segment profit ratio | MD&A growth as printed (segment profit; currency-neutral) |
|---|---|---|---|---|
| FY2022 restated on the new basis (in the FY2023 report) | 352,615 | 57,731 | 16.37% | the base for the FY2023 change |
| FY2022 as first reported (in the FY2022 report; Africa included; 359.4 and 56.4 billion yen) | 359,400 (rounded to 100 million yen) | 56,400 (rounded) | 15.69% | +42.0% (currency-neutral +28.6%) |
| FY2023 (S100T62P, filed 28 March 2024) | 371,435 | 43,075 | 11.60% | -25.4% (currency-neutral -27.7%) |
| FY2024 (S100VHVQ, filed 27 March 2025) | 402,049 | 45,404 | 11.29% | +5.4% (currency-neutral +1.0%) |
| FY2025 (S100XSOA, filed 23 March 2026) | 394,057 | 42,516 | 10.79% | -6.4% (currency-neutral -6.2%) |

- Scope and definition checks (P): the FY2023 report moved the Africa business from Asia Pacific to Europe and restated FY2022. On the restated basis FY2022 segment profit was 57,731 million yen, so the FY2023 fall is 25.4%, which matches the MD&A. The FY2022 proxy (15.69%) is on the old basis and is shown for reference only. The earlier conflict with a snippet of 43.1 billion for FY2023 is resolved: the snippet's figure is the FY2023 annual report's figure.
- The segment label was checked on the FY2022 report's text layer (PDF page 31: アジアパシフィック事業). The 28.6% in that passage is the currency-neutral growth in segment profit (為替中立28.6％増), not the reported growth of 42.0%. The PDF page image did not render the heading legibly, so the text layer is the source for the label.
- Thailand commentary, from the MD&A of each report (P): FY2023, PEPSI including low-sugar products and TEA+ performed well and volume grew as inflation fell and tourism recovered; FY2024, PEPSI and TEA+ performed well and revenue rose; FY2025, the beverage business's volume fell in Vietnam and Thailand, and in Thailand the main carbonated category market fell because of unseasonable weather. These are segment statements, not SPBT's own accounts.
- Scope: the segment covers Vietnam, Thailand, Indonesia, Oceania and health foods. It is not a Thailand-only figure, and segment profit is not a gross or net margin.
- The correction report for the FY2023 annual report (訂正報告書, filed 14 March 2025, listed in the FY2024 report) was not read. The FY2023 comparatives in the FY2024 report (371,435 and 43,075) match the original FY2023 report, so the correction does not change the Asia Pacific figures used here (stated limit on the correction's content).
- Scale indicators for SPBT (S, as printed, not reconciled): capacity of 600 million litres a year and 800 bottles a minute (Thansettakij 27 Mar 2023); average capacity of 1,300 million litres a year (Thansettakij 26 Mar 2025); plant output of up to 800 million litres a year after two new lines (Workpoint release 10 Jul 2026). SPBT growth averaged 8.2% a year over seven years (company statement, S).

### 7.5 Brand-owner margins and bottler margins are not comparable

- **PepsiCo, Inc.** is the brand owner and franchisor, and it also owns bottlers elsewhere. Its 54% gross margin includes concentrate, brand and franchise income and the snack business. It is the franchisor's group figure; it is not a bottler margin and not a figure for the Thai bottler.
- **SPBT (Suntory PepsiCo Beverage (Thailand))** is the bottler and distributor for the Pepsi brands in Thailand. Its margin is the margin of a bottler that pays for concentrate or brand rights. It is not available in the sources used. The Asia Pacific segment profit ratio in 7.4 is a PROXY for the segment, not this margin.
- **Pepsi-Cola (Thai) Trading Co., Ltd.** is PepsiCo's Thai company. Whether its statements are those of a brand holder, a shareholder in the joint venture, or both was not established.
- **Sermsuk** is a bottler and contract manufacturer. The est trademark sits with the ThaiBev group, and Thai Drinks Co., Ltd. is named as its marketer (press). In 2014 the press said Sermsuk would earn fees that rise with volume and stop funding the brand (S, dated); today's filings show a sales and services line, so how est revenue and brand costs are split between Sermsuk and the ThaiBev group was not established. Sermsuk also sells its own Crystal water and distributes other brands. Its 28% to 29% gross margin is a bottler and distributor margin on a mixed range.
- **ThaiBev non-alcoholic segment** is a group segment that mixes bottling, brand ownership and dairy; its 36% to 37% gross margin is not a Sermsuk or Pepsi figure.
- The proposal's margin table shows Haad Thip (the Coca-Cola bottler in the south, gross margin 42.2%, FY2025, S). Rows for brand owners, franchise bottlers and mixed bottlers should be read as separate groups, not as a ranking.

## 8. Key advantages

| Dimension | Pepsi system (SPBT) | est and Sermsuk (ThaiBev) | Evidence and tier |
|---|---|---|---|
| Distribution reach | 25 distribution partners, 68 delivery points, over 470,000 retail outlets at launch in 2018 | Over 100,000 grocery shops and restaurants; first in the restaurant channel with 12%; uses the ThaiBev logistics network | Bangkok Biznews about September 2018 (S, dated); Bangkok Biznews about Oct 2023 (S); Thansettakij 13 Mar 2023 (S); ThaiBev 3 Jul 2024 (COMPANY CLAIM) |
| Brand | Pepsi is about 75% of SPBT's total sales (Brand Buffet, 17 April 2025, S, as printed); share 30% to 39.1% depending on base; 7UP and Mirinda as second brands | est is the Thai cola, aimed at Gen Z (15 to 24); Gen Z is 36% of its customers; penetration 26% (2023) to 28% (2024); share 10.6% in Oct 2025 (basis not stated) | Brand Buffet 17 Apr 2025 (S); Thansettakij 16 Mar 2024 and 13 Oct 2025; Thairath 15 Apr 2024 (S) |
| Price | Zero-sugar 7UP at THB 12.40 to 16.25 per 330 mL; loyalty coins on a retailer page | est cola THB 13.37 per 330 mL on a Makro PRO cash-and-carry listing; est Sugar Free six-pack THB 99 | Section 5 (S) |
| Capacity | THB 1,000 million in 2025 for Saraburi (+50% carbonated capacity); over THB 2,000 million in 2026 for two lines and output of up to 800 million litres a year | Sermsuk plants (Pathum Thani, Surat Thani, Chonburi among those listed) and carbonated volume about 275.6 million litres for October 2023 to September 2024 (adviser estimate) | Brand Buffet 17 Apr 2025; Workpoint 10 Jul 2026 (S); Form 250-2 pages 8 and 63 (P) |
| Innovation | About 8 new products in Q1 2025; Pepsi Treats (2026); plum flavour (2025); 7UP reformulated to no sugar; rPET 550 mL from 2023 | est recipe and look relaunched March 2023 with eight flavours; est Glow Edition took the colour range to 13 flavours (Oct 2025); sugar-free est; music marketing | Thansettakij 26 Mar 2025 (S); Workpoint 10 Jul 2026 (S); Thansettakij 13 Oct 2025 (S); Form 250-2 pages 8 and 9 (P) |
| Trade terms | Held prices in 2023 (statement); a retailer coins offer on Suntory PepsiCo products; no Pepsi-specific price cut found | Case price below Coke in 2013 (dated); est sales growth above the carbonated category in FY2023 and FY2024 (company statement in the MD&A); no est promotion funding found | Thansettakij 27 Mar 2023 (S); Lotus's page (S); Bangkok Biznews 2013 (S, dated); Sermsuk MD&As (P, COMPANY CLAIM). Store-check price cuts of THB 5 to 10 a bottle in April 2025 are market-wide and name no brand (S) |

## 9. Recent moves, 2023 to 2026

| Date | System | Move | Source and tier |
|---|---|---|---|
| 13 Mar 2023 | est | Recipe and look relaunched; "PLAY" dropped from the name; sampling and presenters; rebrand over THB 150 million | Thansettakij 13 Mar 2023 (T4); Gotomanager 29 Oct 2023 (S) |
| 27 Mar 2023 | Pepsi | Prices held for 2023; THB 1,000 million investment; sugar tax phase 3 noted; rPET adds 20% to 30% to packaging cost | Thansettakij 27 Mar 2023 (S) |
| 2023 | Pepsi | First 100% recycled PET bottle in Thailand, Pepsi 550 mL, now over 10 SKUs | Company release via Workpoint, 10 Jul 2026 (S) |
| 2023 | Pepsi (Thailand, inside the Asia Pacific segment) | PEPSI, including low-sugar products, and TEA+ grew volume as inflation eased and tourism recovered; segment profit fell 25.4% on the restated basis, mainly because health-food revenue fell and a prior-year gain on the sale of an Oceania fresh-coffee business did not recur | Suntory Beverage & Food FY2023 annual securities report (P, EDINET S100T62P) |
| Oct 2022 to Sep 2023 | est | Sales growth faster than the carbonated category; rebrand "Born to be Awesome" | Sermsuk MD&A 15 Nov 2023 (P; COMPANY CLAIM on the comparison) |
| 15 Apr 2024 | Pepsi and est | Pepsi new logo and "Thirsty For More"; est THB 200 million "Awaken Awesome Senses" | Thairath (S) |
| 2024 | Pepsi (Thailand, inside the Asia Pacific segment) | PEPSI and TEA+ performed well and revenue rose; segment revenue JPY 402.0 billion (+8.2%) | Suntory Beverage & Food FY2024 annual securities report (P, EDINET S100VHVQ) |
| 3 Jul 2024 | ThaiBev | Tender offer announced to delist Sermsuk at THB 63 a share, through So Water | ThaiBev announcement to SGX, 3 Jul 2024 (P) |
| 19 Sep to 22 Nov 2024 | ThaiBev | Tender offer period (45 business days); So Water acquired 91,786,404 shares (34.52%), holding 263,741,208 shares (99.19%) at 27 Nov 2024 | ThaiBev announcement to SGX, 27 Nov 2024 (P, page image read 20 Oct 2026) |
| 11 Dec 2024 | ThaiBev | SET notice: delisting of SSC approved from 20 Dec 2024; last trading day 19 Dec 2024 | SET notice (P, read 20 Oct 2026) |
| 30 Jan 2025 | Sermsuk | 2025 AGM: FY2024 statements approved; minutes record the company "has been delisted from the SET" | Sermsuk AGM minutes (P, pages 2, 14, 15, 23) |
| Oct 2023 to Sep 2024 | ThaiBev | Carbonated soft drink volume in the non-alcoholic segment up 19.2% | ThaiBev FY2024 announcement (P, read by T4) |
| 1 Feb 2025 | Pepsi | Tanuj Chadha becomes chief executive of SPBT | Marketeer 3 Feb 2025 (S); Mini Me 30 Mar 2025 (S, opened) |
| Jan to Mar 2025 | est | Restaurant campaign at 1,000 restaurants; Big Cola (a challenger at 5% to 6%) is pushing again | Marketeer 12 Mar 2025 (T4, S) |
| Mar to Apr 2025 | Pepsi | THB 1,000 million, Saraburi carbonated capacity up 50%; about 8 new products in Q1; 7UP reformulated to no sugar; plum Pepsi; sugar tax phase 4 from 1 Apr 2025, reported at THB 0.3 to THB 5 a litre (S, press only; not checked against a primary notice; section 12, conflict 19) | Thansettakij 26 Mar 2025; Brand Buffet 17 Apr 2025; Mini Me 30 Mar 2025 (S) |
| 2025 | Pepsi (Thailand, inside the Asia Pacific segment) | Beverage volume and revenue fell in Thailand as the main carbonated category shrank in unseasonable weather; segment revenue JPY 394.1 billion (-2.0%) | Suntory Beverage & Food FY2025 annual securities report (P, EDINET S100XSOA) |
| 13 Oct 2025 | est | est Glow Edition: 4 new flavours, colour range 13 flavours; share 10.6% (basis not stated); campaigns with presenters and music festivals | Thansettakij 641276 (T4, S) |
| 27 Feb to 7 May 2026 | Pepsi | Pepsi Treats Strawberry 'N' Cream, zero sugar | Company news 7 May 2026 (P as a company statement) |
| 10 Jul 2026 | Pepsi | Over THB 2,000 million for two Saraburi lines; Pepsi Treats Chocolate Dubai; premium cafe range planned for Q4 2026 | Workpoint, company release (S) |

## 10. Threat and response to a dissolvable cube

Everything in this section is team analysis (ASSUMPTION). No page read says what either system plans to do about a dissolvable product. The facts it rests on are tiered in the sections above.

What the Pepsi system or ThaiBev could copy at once or within one season:

1. **The flavour and the price.** A zero-sugar lemon-lime can already exists (7UP Zero Sugar Lemon Soda, 325 mL six-pack, THB 75 at Lotus's, and a single 7UP lemon soda pack at THB 16 on the Lotus's Shop Online row shown by Priceza), and est has Lemon Lime and Sugar Free lines. A lemon flavour is not a lasting difference for Lemon Soda. The 7UP cans already carry a zero-sugar claim, and Lemon Soda does not make one (section 12, conflict 15).
2. **Price.** The 7UP lemon listings range from THB 12.40 to THB 16.25 per 330 mL, and Lemon Soda's planning shelf price of THB 15 is an assumption between the 7UP six-pack and single-pack levels. Price promotions are common in the category (store checks in April 2025 found cuts averaging THB 5 to 10 a bottle, no brand named) and a Lotus's coins offer names Suntory PepsiCo products; no est promotion funding was found. Either system could answer with a promotion (ASSUMPTION), so a THB 15 price is not a lasting point of difference.
3. **Speed.** SPBT launched about 8 products in the first quarter of 2025 and runs limited flavours (Pepsi Treats, plum, Chocolate Dubai); est added 4 flavours in October 2025. A copy of a flavour takes weeks.
4. **Sugar-tax answer.** Press reports a phase 4 of the sugar tax from 1 April 2025 (S, not checked against a primary notice). Both systems already sell zero-sugar lines (7UP, est Sugar Free); this record does not show that the tax caused them.

What they cannot copy quickly:

1. **The form.** The packed Lemon Soda unit is 5.29 g: the dry cube of 3.79 g, which already includes the 0.80 g binder and filler, plus an assumed 1.5 g pouch. Against the 330 g of liquid the drink contains, the dry cube is 1.15% and the packed unit 1.60% (script `mass_packed_unit_vs_liquid`). Tier: DERIVED from an ASSUMPTION input (the pouch); nothing was weighed. Over the 3.46 to 4.24 g allowance range for the cube, the packed unit is 1.50% to 1.74%. The can or bottle is not counted, so the real ratio is lower still. Their capital is in filling and carbonating lines for liquid (THB 1,000 million in 2025 and over THB 2,000 million in 2026). A dry effervescent cube needs a different plant, pack and handling, and a different regulatory path. No source shows either system planning one.
2. **Their cost structure is built on filled packs.** In FY2024 Sermsuk's cost of sales was 70.75% of sales and its distribution costs were THB 3,033 million, or 23.06% of THB 13,153 million of sales (P, FY2024 MD&A and AGM minutes; script `mass_packed_unit_vs_liquid` and `sermsuk_cost_shares_fy2024`). Moving liquid is a large part of the can business. This is context, not a measure of what a cube would save.
3. **Occasion.** Their strength is route to market for cans and bottles at over 470,000 outlets (Pepsi, dated 2018) and over 100,000 grocery shops (est). The cube is a single-serve dry unit; no source shows either system serving that occasion.

Direct rivals of the Singha brand in the ThaiBev system: est competes in cola and, through est Lemon Lime and est Kamikaze Lime, in fruit sodas; Chang Soda and Rock Mountain compete in clear soda water, the nearest ThaiBev products to Singha's soda range.

Positioning that follows from the analysis (proposed text in section 11): Lemon Soda should be presented as a form and convenience product that shares its lemon flavour with cans already on the shelf, with its price position set between the six-pack and single-pack levels (an assumption), and with no sugar-free or health claim, consistent with the submission. It should not be presented as a better flavour or a lower price.

## 11. Comparison table and proposed text

### 11.1 Table for proposal 11 section 2.3 (rows to add to the "Soda competitors" table)

| Product | Pack | Price (THB) | Sugar wording | Tier and date |
|---|---|---|---|---|
| 7UP Zero Sugar Lemon Soda (Suntory PepsiCo Beverage (Thailand)) | 325 mL, six-pack | 75 for 6 (12.5 each; 12.69 per 330 mL) | "Zero Sugar" in the retailer's product name | S, Lotus's, 20 October 2026 |
| 7UP no-sugar lemon soda (same maker) | 325 mL, single pack | 16 (16.25 per 330 mL) | no sugar in the Thai product name | S, Lotus's Shop Online row shown by Priceza, 20 October 2026 |
| 7UP Zero Sugar Strawberry Lemon | 325 mL, six-pack | 75 for 6 (about 12.5 each) | "Zero Sugar" in the retailer's product name | S, Lotus's, 20 October 2026 |
| est cola (ThaiBev group; made by Sermsuk) | 325 mL, six-pack | 79 for 6 (13.17 each; 13.37 per 330 mL) | est Sugar Free is also sold | S, Makro PRO cash-and-carry listing, 20 October 2026 |
| est Sugar Free (ThaiBev group; made by Sermsuk) | 325 mL, six-pack | 99 for 6 (16.75 per 330 mL) | sugar-free by name; flavour not stated in the listing | S, Lazada seller via Priceza, 20 October 2026 |
| est Lemon Lime (ThaiBev group; made by Sermsuk) | not found | not found | one of eight est flavours | P, Sermsuk filing, 8 October 2024 |

### 11.2 Proposed paragraphs for proposal 11 section 2.3 (replace the "Market structure" line)

Market structure (S, Thansettakij, 16 March 2024): the press reports Coca-Cola at 51%, Pepsi at 30% and est at 8.6%. Only the est figure is stated as a volume share, and the article gives no year or data owner. est is the cola that the press also writes as S Cola. Its trademark sits in the ThaiBev group (Sermsuk Public Company Limited's filing of 8 October 2024, P). Sermsuk makes it under a manufacturing contract, and Thai Drinks Co., Ltd. is named by the press as its marketer (S). Other reports give est between 8.0% and 10.6% from March 2023 to October 2025 (the latest, 10.6%, is stated in Thansettakij's article of 13 October 2025 with no named source, and its basis is not stated), and they give Pepsi 30%, 37% or 39% depending on the report and the base. The shares are therefore indicative and do not add to one total. The press values the Thai carbonated soft-drink market at THB 66,000 million for the 12 months to January 2024 and THB 70,772 million for the 12 months to November 2024 (NielsenIQ, S). Other press and bank figures for 2023 to 2025 run from THB 62,000 million to THB 76,900 million; no source states whether the value is at retail or manufacturer level. est also competes in the colour-soda segment (lemon-lime and fruit flavours). Thansettakij (13 October 2025, S) reports that segment at THB 17,391 million, with no named source in the article. The same article prints the segment as 30% of the market, which does not match its own total.

Two competing systems: Pepsi, 7UP and Mirinda are made and sold in Thailand by Suntory PepsiCo Beverage (Thailand) Co., Ltd., a joint venture that began in March 2018 (S). Suntory Beverage & Food held 51.0% at 31 December 2022 and still shows 51.0% in its 2025 annual report (P), and PepsiCo's Thai company holds 49% (S, 2017 press). Sermsuk bottled and distributed Pepsi until its contract ended on 1 November 2012 (S) and now makes est for the ThaiBev group. Sermsuk's shares were delisted from the Stock Exchange of Thailand with effect from 20 December 2024, after ThaiBev's subsidiary So Water Company Limited acquired 34.52% of the shares in the tender offer and then held 99.19% (P). Suntory Beverage & Food's 2025 annual securities report says that in Thailand the main carbonated category market fell in 2025 because of unseasonable weather (P).

### 11.3 Proposed rows and sentences for the margin table in section 2.2

| Entity (year) | Gross margin | Net margin | Tier and note |
|---|---|---|---|
| Sermsuk (est maker; consolidated; year to 30 September 2024) | 29.2% | 3.1% | P, DERIVED, SET filing of 15 November 2024; confirmed in the 2025 AGM minutes |
| Suntory Beverage & Food, Asia Pacific segment (PROXY for the Pepsi bottler; year to 31 December 2025) | Not disclosed | Not disclosed; segment profit ratio 10.8% (2024: 11.3%) | P (annual securities report FY2025), PROXY; segment profit divided by segment revenue |

Sentences to add under the table: Margins in the table are not comparable across rows. PepsiCo is a brand owner and franchisor and its figure is the global group; Sermsuk and Haad Thip are bottlers; ThaiBev's non-alcoholic figure is a group segment. Revenue and profit of Suntory PepsiCo Beverage (Thailand), the Pepsi bottler in Thailand, are filed with the Department of Business Development and are not available in the public sources used for this proposal, so no Pepsi bottler margin is shown. As a PROXY, the Asia Pacific segment of Suntory Beverage & Food, which consolidates that bottler together with businesses in Vietnam, Indonesia, Oceania and health foods, reported segment profit of JPY 42.5 billion on revenue of JPY 394.1 billion in 2025 (10.8%) and JPY 45.4 billion on JPY 402.0 billion in 2024 (11.3%). These are segment profit ratios, not gross or net margins (P, company annual securities reports).

### 11.4 Proposed slide 8 text

- **Competitor strip:** Sprite Lemon Plus, 325 mL, THB 15 (Thaiger, 29 August 2022; dated); 7UP Zero Sugar Lemon Soda, 325 mL six-pack, THB 75 for six, THB 12.69 per 330 mL (Lotus's, 20 October 2026), and THB 16 for a single 325 mL pack (Lotus's Shop Online row shown by Priceza, 20 October 2026); est cola, THB 79 for six, THB 13.37 per 330 mL (Makro PRO cash-and-carry listing, 20 October 2026); est Lemon Lime and est Sugar Free from the ThaiBev group; Schweppes zero-sugar 330 mL variants (releases of 3 July 2023 and 24 June 2024; price not found). Press brand shares: Coca-Cola 51%, Pepsi 30%, est (written S Cola) 8.6% by volume; the source gives no year, and Thansettakij's article of 13 October 2025 gives est 10.6% (basis not stated).
- **Note bar:** The lemon soda is the closest substitute. It shares its lemon flavour with cans already on the shelf and differs in form and pack. Its planning shelf price of THB 15 per 330 mL is an assumption. It sits between the 7UP zero-sugar six-pack price (THB 12.69 per 330 mL) and the 7UP single-pack price (THB 16.25 per 330 mL), both from listings read on 20 October 2026. The packed unit is about 1.6% of the mass of the 330 mL it makes: the 3.79 g dry mass and an assumed 1.5 g pouch, against 330 g of liquid; nothing was weighed.
- **Source line addition:** Lotus's and Priceza, 20 October 2026 (S); Makro PRO, 20 October 2026 (S); Thaiger, 29 August 2022 (S); Thansettakij, 13 October 2025 (S); Sermsuk Form 250-2, 8 October 2024 (P); ThaiBev announcement, 27 November 2024 (P); SET notice, 11 December 2024 (P); Suntory Beverage & Food annual securities reports, FY2023 to FY2025 (P, EDINET).
- **Speaker note addition:** Say that S Cola in the press is est, a ThaiBev group brand, and that its maker, Sermsuk, bottled Pepsi until 2012 and was delisted from the Stock Exchange of Thailand on 20 December 2024 after ThaiBev's tender offer. Say that no head-to-head taste or price claim is confirmed, and that the Thai Pepsi bottler's own revenue and profit are not available in the public sources used; the Asia Pacific segment of its parent is shown as a proxy.

## 12. Conflicts with the current deck and submission text, and with record 67

1. **Deck slide 8 and proposal 11 section 2.3: "Pepsi 30%, S Cola 8.6% (volume)", "2023 to 2024".** The source gives no year and no data owner, and only the 8.6% is described as a volume share. Later reports give est 10.6% (13 October 2025), Pepsi 39.1% of the dark cola segment (2025), and a March 2023 ThaiBev table gives Pepsi 37%. Suggested wording: section 11.2.
2. **Market value lines.** (a) "Carbonated market value over THB 66,000 million (2024, year not stated)" in `submission/11` line 97 labels the figure as 2024; record 67 traces 66,000 to NielsenIQ for the 12 months to January 2024. (b) "THB 76,900 million (2026 bottler data)" in `submission/11` line 97, `submission/03` line 30 and the deck is a Kasikorn Research Center estimate for 2025, not bottler data and not 2026 (record 67). Section 11.2 removes the "2026 bottler data" wording and keeps the figure as the top of a labelled range. The range here (THB 62,000 million to THB 76,900 million) is wider than record 67's THB 66,000 million to THB 76,900 million because the October 2023 pages print over THB 62,000 million (S, not reconciled).
3. **The brand name.** The line says "S Cola". The brand's own name is est (Thai เอส). The deck should say "est (S Cola)" at first use and name the ThaiBev group as the trademark owner. Nothing in the deck says who owns S Cola.
4. **Proposal 11 section 2.3, row "7UP NS Strawberry Lemon ... 'NS' read as no sugar, not confirmed".** Lotus's names the same flavour and pack (six cans for THB 75) "ZERO SUGAR", read on 20 October 2026. The row can cite that page and drop the "not confirmed" wording (11.1).
5. **Slide 8 title claims lemon is the shared flavour; the competitor strip does not mention the Pepsi system's 7UP at all.** The strip should add the 7UP row (section 11.1).
6. **The proposal's margin table lists PepsiCo FY2025 only.** The three-year series is in section 7.2. No contradiction in the FY2025 figures; the row is the global franchisor group (11.3). The Asia Pacific proxy row is added in 11.3.
7. **Entity wording.** The proposal does not name Sermsuk, ThaiBev's role in est, or Suntory PepsiCo Beverage (Thailand). Sections 2 and 11.2 supply them.
8. **Slide 8 note bar (deck_content.md line 125).** The current note bar reads: "The lemon soda is the closest substitute. Cannibalisation is reviewed at Phase 5 if 50% or more of buyers say they switched." The replacement in 11.4 keeps the first sentence and drops the second, which refers to an internal phase of the plan and is not a claim for the judges. The lead may restore it if the team wants it in the judge text. An earlier draft of this record quoted a phrase ("not in price") that is not in the deck or the submission; the replacement states the price as an assumption instead.
9. **Sermsuk's listing status.** If any deck or proposal text calls Sermsuk "SET-listed" or cites it as SSC on the SET, it must be corrected to "delisted from the SET on 20 December 2024". The current text was not read for this wording; the lead must check it.
10. **Thai Drinks.** The earlier draft of this record called Thai Drinks Co., Ltd. a ThaiBev group company with no source. The evidence is now stated in full: the press calls it a ThaiBev group company (Bangkok Biznews, about October 2023, S), Gotomanager (29 October 2023, S) places it in the ThaiBev chain as marketer, and the one primary fact is that So Water, a ThaiBev subsidiary, holds 4.95% of it (P, Form 250-2 page 42). The controlling holder was not found, so "group company" stays a press claim. The judge text in 11.2 names Thai Drinks only as the press's marketer.
11. **Suntory Asia Pacific segment, FY2022 against FY2023 (resolved).** The FY2022 report's segment profit of JPY 56.4 billion (P) is on the old basis, which included Africa. The FY2023 report restated FY2022 to JPY 57.7 billion when Africa moved to Europe (P). The FY2023 fall of 25.4% on that basis matches the MD&A. The FY2023 figure of JPY 43.1 billion in an earlier snippet is confirmed by the FY2023 report. No definition question remains for FY2023 to FY2025.
12. **Sermsuk's listing history.** Its own filing gives both 1975 ("being a listed company in Thailand") and 1994 ("became a listed company"). Neither date is in the deck or the proposal; if either is used, the conflict must be stated.
13. **est launch year and the marketer's name (new, S against P).** Bangkok Biznews (about October 2023, S) gives the brand's launch as 2011 and writes the marketer as "Thai Drink Co., Ltd.". Form 250-2 page 8 (P) gives 2012 as the launch year, and MGR Online (25 October 2012, S) and Gotomanager (S) give 2012 with the launch day 2 November 2012. The record uses 2012 (P for the year). The marketer appears as "Thai Drinks Co., Ltd." in the filing and in the Thansettakij list of 3 April 2025 (S). The two spellings refer to the same company as far as the sources show.
14. **Singha Lemon Soda can price (new, deck and submission against S retailer rows).** The deck says the current lemon can price is not verified (deck_content.md line 54: "The current lemon can price is not verified"; line 121: "can price not verified"), and the submission says the same (`submission/01_problem_and_pain_point.md` line 11; `submission/02_situation_analysis.md` lines 26 and 35; `submission/05_finance_and_project_valuation.md` line 35, "not benchmarked"). Lotus's rows read on 20 October 2026 (T5, `lotuss_2026-10-20.md`, rows L7 and L8; S) show the Singha Lemon Soda 330 mL single can at THB 17 and the six-pack at THB 85 (THB 14.17 per 330 mL). A 7-Eleven ALL Online six-pack reads THB 172 (page A2; S). These are retailer listings, not Singha's price list. The judge text in this record does not use them. Options for the lead: (a) cite the Lotus's rows as a dated retailer listing and change the "not verified" wording to "listed at THB 17 a single can and THB 85 for six at Lotus's, 20 October 2026 (S)"; or (b) keep "not verified" and leave them out. Recommendation: (a), with the retailer named. The choice is the team's; no decision is passed to Singha Corporation.
15. **Sugar-free wording (new).** The deck says Lemon Soda "carries no sugar-free or health claim" (deck_content.md line 122), and the submission says "Lemon Soda carries no sugar-free status" (`submission/04_strategy.md` line 59). An earlier draft of sections 8 and 11.4 said Lemon Soda shares a sugar-free claim with zero-sugar cans. That is wrong and has been removed from this record's proposed text; the position stated here is no sugar-free claim. Deck_content.md line 56 mentions "sugar-free wording at launch" as the company's own claim (S) for the existing can. That refers to the company's can and not to Lemon Soda; the lead should check that the judge text does not blur the two. The lead should confirm the position.
16. **Slide 8 removals and replacements (new; for the change list).** (a) The deck competitor strip's row "Sprite 24-pack about THB 15.2 a can (Lazada listing, undated)" (deck_content.md line 124) is removed, because it has no date and the dated Lotus's Sprite six-pack (THB 85) is in section 5. (b) The second sentence of the note bar (Phase 5 cannibalisation, deck_content.md line 125) is removed (conflict 8). (c) The note bar's "shares its flavour and its sugar-free claim" wording is not used (conflict 15). (d) The note bar's reference to a price of "THB 12.69 to 14.38" and "THB 16.25 to 17.00" is replaced by the 7UP-only rows in 11.4. (e) "325 mL can" for 7UP Zero Sugar Lemon Soda is replaced by "325 mL six-pack" (the Lotus's page reads PACK6 and does not use the word can).
17. **Unit ratio basis (new, wording only).** The earlier wording "derived from an assumed pouch and an assumed binder" is wrong: the binder is inside the 3.79 g dry mass. The 5.29 g is 3.79 g plus the assumed 1.5 g pouch. The note bar and section 10 now say so.
18. **Sprite 24-pack row (new; submission/11 line 92, and the same row in the proposal copy).** The submission row reads "Sprite Original and No Sugar | 325 mL cans, 24-pack | 365 for 24 (about 15.2 each); a second snippet says 354 | names only | S, Lazada listing, undated". The Lazada trending page was opened on 20 October 2026 (saved in `rework/raw/diligence_2026-10-20/T5/t5_recheck_lazada_priceza_2026-10-20.md`). Both the Sprite Original and the Sprite No Sugar 24-can rows read THB 365 (struck THB 384). The rows carry no date stamp and no seller is shown; the page footer reads 20 October 2026. The THB 354 figure is a search snippet that was not opened and is not used. Replacement row for the proposal: "Sprite Original and Sprite No Sugar | 325 mL cans, 24-pack | 365 for 24 (about 15.2 each) | sugar wording taken from the product name | S, Lazada page read 20 October 2026; no listing date or seller shown".
19. **Sugar-tax phase 4 (new; section 9 and submission/10 line 22).** Submission/10 line 22 gives four sugar bands of 0, 1, 3 and 5 baht per litre with 14% ad valorem, from the saved Royal Gazette schedule (P, `rework/raw/gazette_sugar_drink_excise_primary_2560_A095_111.md`, section 2). The schedule's row for 1 October 2566 onward has the same nonzero rates (1, 3 and 5 baht) and no 0.3 baht rate. The press phase 4 range of THB 0.3 to THB 5 a litre (Brand Buffet, 17 April 2025, S) is therefore not a schedule of any period in the notice read. The press phase 3 ladder (0.3, 1, 3 and 5 baht, given in the press for 1 April 2023 to 31 March 2025) matches the notice's row for 1 October 2564 to 30 September 2566, not the press dates. Judge text does not use the phase dates or the phase 4 range. The lead should keep submission/10 line 22 as it stands, which already says later periods are not verified, and should not cite a phase 4 range. Script `fourth_pass_sugar_tax_ladder_check` (fourth pass); stated limit 18.

## 13. Stated limits

1. **SPBT revenue, gross profit and net profit (three years):** not available in the public sources used. The statements are filed with the Department of Business Development, but the aggregators show no values without a login, the DBD data warehouse returned HTTP 404 and a second aggregator HTTP 403. The DBD statements for FY2023 to FY2025 would settle it. The Suntory annual reports, which consolidate SPBT, are used only as the proxy in item 2.
2. **The Asia Pacific segment is a proxy, not the Pepsi bottler.** The segment's revenue and segment profit are read from the annual securities reports for FY2023, FY2024 and FY2025 (P). The segment covers Vietnam, Thailand, Indonesia, Oceania and health foods, and no Thailand-only profit is disclosed. Its profit ratio is a segment ratio, not a margin. The correction report for the FY2023 annual report (14 March 2025) was not read; the FY2024 report's FY2023 figures match the original.
3. **Pepsi-Cola (Thai) Trading Co., Ltd. statements and the ownership of the 49% side of SPBT:** not found. The Business+ figures for 2022 are internally inconsistent and are not used.
4. **Sermsuk after January 2025:** the SET effective date (20 December 2024) and the delisting are verified. The last primary statement read is the 2025 AGM minutes of 30 January 2025, which say the company "has been delisted from the SET". No filing after that date was found, and the FY2025 statements (year to 30 September 2025) were not found. A later relisting was not seen but not searched for in depth.
5. **Which entity holds the Pepsi, 7UP and Mirinda trademarks in Thailand:** not confirmed by a registry or a primary page. A 2003 trade press item names Pepsi-Cola (Thai) Trading; it is UNVERIFIED.
6. **Controlling holder of Thai Drinks Co., Ltd.:** not found; So Water holds 4.95% (P). The press's "ThaiBev group company" label (S) is not confirmed by a primary document on control. Gotomanager (29 October 2023, S) names "Thai Beverage Logistics" in its owner chain as a later major shareholder "within the ThaiBev group" (team translation); the sentence does not say which company it describes, so it is a lead only.
7. **A like-for-like Pepsi shelf price and a consumer-level est price:** not found. The only Pepsi row (7-Eleven online, THB 167 for six cans) comes from a channel that prices about twice Lotus's for the same pack, and the est row at Makro PRO is a cash-and-carry listing. No Mirinda shelf price was found. The Lotus's 7UP page prints "฿75.00/Each" with the PACK6 name; the record reads THB 75 as the six-pack price, which is consistent with the THB 16 single pack on the Priceza row. The Lotus's single-pack page itself was not opened.
8. **Launch dates of 7UP in Thailand before 2012, the 7UP flavours on sale in 2026, est Lemon Lime in its present form, and the full Mirinda flavour list:** not found. A 7UP Extra Fizz zero-sugar line appeared only in a search snippet, and the company page returned HTTP 403; it is UNVERIFIED and is not used.
9. **Price changes 2023 to 2026:** no list-price change by Pepsi, 7UP, Mirinda or est was found; only statements that prices were held (SPBT, March 2023) and discounts in store checks that name no brand.
10. **Market shares:** no data owner or year is printed for any of the Coke, Pepsi and est shares used. The Pepsi shares (30%, 37%, 39%, 39.1%) and the est shares (8.0% to 10.6%) have different or unstated bases and are not additive. No 2025 NielsenIQ or Kantar share table was found. A current like-for-like share table needs the Nielsen or Kantar release itself.
11. **Market value level and year labels:** no source states whether a value is at retail or manufacturer level, and outlets label the same value with years that differ by one (section 3.3).
12. **Outlet counts:** the 470,000 outlets for the Pepsi system date from the 2018 launch and the 100,000 shops for est from about October 2023. No current count was found for either.
13. **Capacity figures for SPBT** (600, 1,300 and up to 800 million litres) come from three articles and do not reconcile; they are shown as printed.
14. **est revenue and profit:** not disclosed; est sits inside Sermsuk's and ThaiBev's totals. The nearest disclosed proxy is Sermsuk's carbonated drink revenue (THB 4,550 million, 36.78% of FY2023 sales, P), which also covers 100Plus and Sarsi.
15. **ThaiBev annual report 2024:** over the tool's file size limit; the SGX year-end announcements (read by T4) were used for the segment figures instead.
16. **Thai SEC filing index:** the index shows no Sermsuk filing after 15 November 2024 in the pages read.
17. **Singha Lemon Soda price:** the deck and the submission say the price is not verified; the Lotus's rows (S) are not used in the judge text (conflict 14).
18. **Sugar-tax phase 4 (from 1 April 2025):** press only (Brand Buffet, 17 April 2025, S). No primary notice for that period was read. The saved Royal Gazette schedule for item 02.02 has its last row from 1 October 2566, and later amendments were not searched. A standard web search returned press leads on phase 4; they were not opened and are not used.

## 14. Figure register (the figures used in the slide text)

| Label | Value | Tier | Source | Date read | Saved page |
|---|---|---|---|---|---|
| est identity and trademark owner | est (เอส), ThaiBev group brand; trademark sold by Great Brands to Super Brands Company Pte. Ltd. in 2014; "ThaiBev, who owns the trademark" | P (filing); S (press, buyer named as International Beverage Holdings Limited) | Sermsuk Form 250-2, 8 Oct 2024, pages 8, 42 and 64 | 20 Oct 2026 | T3/sermsuk_form250_2_opinion_2024-10-08_extracts.md |
| Marketer of est and its ownership | Thai Drinks Co., Ltd. (press: Thansettakij 624003, 3 Apr 2025, S; Bangkok Biznews about Oct 2023, S, "ThaiBev group company"); So Water holds 4.95% (P, page 42); controlling holder not found | P for the 4.95% stake; S for the role and the group label | Thansettakij 624003; Bangkok Biznews 1093142; Form 250-2 page 42 | 20 Oct 2026 | T3/csd_market_share_press_2020_2025.md blocks 4 and 5; T3/sermsuk_form250_2_opinion_2024-10-08_extracts.md |
| est volume share (the deck's S Cola 8.6%) | 8.6% (year not stated) | S | Thansettakij 590894, 16 Mar 2024 | 20 Oct 2026 | T3/csd_market_share_press_2020_2025.md |
| est latest share | 10.6% (up from 7% before the rebrand; basis not stated); 24.6% of colour soda, number 2 | S | Thansettakij 641276, 13 Oct 2025 | 20 Oct 2026 | T4/est_thansettakij_2025-10-13_share_and_glow.md |
| est share band | 8.0% to 10.6% in ten reports, March 2023 to October 2025 | S | script `share_summary` | 20 Oct 2026 | rework/screen/t3_pepsi_sermsuk_margins_results.json |
| Coca-Cola share | 51% | S | Thansettakij 590894, 16 Mar 2024 | 20 Oct 2026 | T3/csd_market_share_press_2020_2025.md |
| Pepsi share | 30% (2023 to 2024 reports); 37% (ThaiBev table, Mar 2023); 39% to 39.1% (2025; Mini Me 30 Mar 2025 opened, basis not stated) | S | Thansettakij 590894, 623088 and 624003; Positioning 1424257; Mini Me 30 Mar 2025 | 20 Oct 2026 | T3/csd_market_share_press_2020_2025.md; T3/mini_me_2025-03-30_opened_2026-10-20.md |
| Pepsi share of SPBT sales | about 75% | S | Brand Buffet, 17 Apr 2025, block 7 | 20 Oct 2026 | T3/csd_market_share_press_2020_2025.md block 7 |
| Thai carbonated market value | THB 66,000 million (NielsenIQ, Feb 2023 to Jan 2024); THB 70,772 million (NielsenIQ, 12 months to Nov 2024); other reports THB 62,000 million to THB 76,900 million | S | Marketeer 15 Mar 2024 and MarketPlus 8 May 2024 (NielsenIQ attribution of the 66,000 value and window); Thansettakij 16 Mar 2024 (value unsourced); Thansettakij 14 Jan 2025 (70,772); Gotomanager 29 Oct 2023; KResearch via Thansettakij 8 Sep 2025 | 20 Oct 2026 | T1/nielseniq_press_series_2023_2026.md; T3/csd_market_share_press_2020_2025.md block 10; record 67 |
| Colour-soda segment | THB 17,391 million (printed as 30% of the market, which does not fit the total; 25.57% of 68,000); THB 17,300 million for Sep 2024 to Aug 2025 (NielsenIQ) | S | Thansettakij 641276 and Bangkokbiznews, 13 Oct 2025 | 20 Oct 2026 | T4/est_thansettakij_2025-10-13_share_and_glow.md; T1/nielseniq_press_series_2023_2026.md |
| Sermsuk tender offer | 19 Sep to 22 Nov 2024 (45 business days); THB 63 a share; So Water acquired 91,786,404 shares (34.52%) and held 263,741,208 shares (99.19%) at 27 Nov 2024. Maximum offer: 93,945,680 shares at THB 63, a total of THB 5,918,577,840 (Form 250-2 page 10) | P | ThaiBev announcement to SGX, 27 Nov 2024 (page image); ThaiBev announcement of 3 Jul 2024 (share count, line 27 of the saved file); Form 250-2 page 10 | 20 Oct 2026 | T3/thaibev_sgx_27nov2024_and_agm_2025_minutes_2026-10-20.md section A |
| So Water holding before the tender | 64.67% (171,954,804 shares) at the record date of 6 Dec 2023 (3 Jul 2024 announcement) and at 17 Jul 2024 (15 Nov 2024 notice); both P | P | ThaiBev announcements of 3 Jul 2024 (lines 48 to 49 of the saved file) and 15 Nov 2024 (lines 155 to 156) | 20 Oct 2026 | T3/thaibev_sgx_announcements_sermsuk_2024.md; script `so_water_holding_before_tender_check` |
| Sermsuk delisting | Delisting from 20 Dec 2024; last trading day 19 Dec 2024; voluntary delisting under s.171(4) of the Securities and Exchange Act | P | SET notice, published 11 Dec 2024 | 20 Oct 2026 | T3/rerun_set_delisting_notice_sermsuk_2026-10-20.md |
| Sermsuk status after delisting | "has been delisted from the SET" (2025 AGM, 30 Jan 2025, page 23); 265,900,484 issued shares; 99.1885% attending | P | Sermsuk AGM minutes, 30 Jan 2025, pages 2 and 23 | 20 Oct 2026 | T3/thaibev_sgx_27nov2024_and_agm_2025_minutes_2026-10-20.md section B |
| SPBT ownership | Suntory 51.0% on 31 Dec 2022 and in the FY2023 to FY2025 subsidiaries tables; PepsiCo side 49% per 2017 press; started March 2018 | P for 51.0%; S for 49% and start | Suntory Beverage & Food annual securities reports FY2022 (page 116), FY2023 (S100T62P), FY2024 (S100VHVQ), FY2025 (S100XSOA); The Nation, 2 Nov 2017 | 20 Oct 2026 | T3/sbf_securities_report_fy2022_edinet_extract.md; T3/sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md; T3/spbt_ownership_and_jv_press_2017_2018.md |
| SPBT registry | Registered 18 Nov 2003; registration number 0105546139004; statements listed as filed 2021 to 2025, values not shown | S (aggregator of DBD data) | Creden registry page | 20 Oct 2026 | T3/spbt_ownership_and_jv_press_2017_2018.md block 7 |
| Pepsi contract with Sermsuk | ended 1 Nov 2012 | S | MGR Online, 25 Oct 2012 | 20 Oct 2026 | T3/pepsi_system_moves_and_launches_2012_2026.md |
| Sermsuk FY2024 | sales THB 13,153 million; cost of sales 9,306; gross profit 3,847 (29.25%); distribution 3,033; net profit 404 (3.07%) | P, DERIVED | SET MD&A 15 Nov 2024; 2025 AGM minutes page 14 | 20 Oct 2026 | T3/sermsuk_mda_fy2022_fy2023_fy2024_set_filings.md; T3/thaibev_sgx_27nov2024_and_agm_2025_minutes_2026-10-20.md section B |
| Sermsuk FY2023 | sales 12,371; gross margin 28.30%; net profit 248 (2.00%) | P, DERIVED | SET MD&A 15 Nov 2023 | 20 Oct 2026 | T3/sermsuk_mda_fy2022_fy2023_fy2024_set_filings.md |
| Sermsuk FY2022 | sales 10,905; gross margin 28.26% (filed; 28.25% from whole-million inputs); net profit 13 (0.12%) | P, DERIVED | SET MD&A 16 Nov 2022; Form 250-2 page 16 | 20 Oct 2026 | T3/sermsuk_mda_fy2022_fy2023_fy2024_set_filings.md; T3/sermsuk_form250_2_opinion_2024-10-08_extracts.md |
| Sermsuk carbonated share of sales | THB 4,550.15 million, 36.78% (FY2023) | P | Form 250-2 page 11 | 20 Oct 2026 | T3/sermsuk_form250_2_opinion_2024-10-08_extracts.md |
| Sermsuk average carbonated price | THB 18.42 a litre; THB 6.08 per 330 mL | P, DERIVED | Form 250-2 page 63 | 20 Oct 2026 | same |
| ThaiBev Non-Alcohol attributable profit | FY2023 1,196; FY2024 1,455 (FY2024 announcement, up 259 or 21.7%); FY2024 comparative 1,146 in the FY2025 announcement (309 moved to Others; total 27,215 unchanged); FY2025 2,414 (up 110.6% as printed, on 1,146) | P, DERIVED | ThaiBev SGX year-end announcements FY2024 and FY2025 (read by T4) | 20 Oct 2026 | T4/thaibev_fy2024_yearend_sgx_extract.md; T4/thaibev_fy2025_yearend_sgx_extract.md; script fourth_pass_thaibev_fy24_non_alcohol_basis |
| PepsiCo FY2025 | revenue USD 93,925 million; gross margin 54.15%; net margin 8.77% (global franchisor group) | P, DERIVED | SEC XBRL, 10-K filed 3 Feb 2026 | 20 Oct 2026 | T3/pepsico_sec_xbrl_fy2023_fy2025.md |
| PepsiCo FY2023 and FY2024 | gross margin 54.21% and 54.55%; net margin 9.92% and 10.43% | P, DERIVED | SEC XBRL | 20 Oct 2026 | same |
| ThaiBev non-alcoholic segment | gross margin 36.00% (FY2024), 36.58% (FY2025) | P, DERIVED | SGX year-end announcements | 20 Oct 2026 | T4/thaibev_fy2024_yearend_sgx_extract.md; T4/thaibev_fy2025_yearend_sgx_extract.md |
| Asia Pacific segment, FY2023 (PROXY for the Pepsi bottler) | segment revenue JPY 371,435 million; segment profit JPY 43,075 million; 11.60% | PROXY (P filing; DERIVED ratio); segment, not Thailand-only; not a gross or net margin | Suntory Beverage & Food annual securities report FY2023 (S100T62P), segment table and MD&A | 20 Oct 2026 | T3/sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md |
| Asia Pacific segment, FY2024 (PROXY) | segment revenue JPY 402,049 million; segment profit JPY 45,404 million; 11.29% | PROXY (P filing; DERIVED ratio) | Annual securities report FY2024 (S100VHVQ) | 20 Oct 2026 | same |
| Asia Pacific segment, FY2025 (PROXY) | segment revenue JPY 394,057 million; segment profit JPY 42,516 million; 10.79% | PROXY (P filing; DERIVED ratio) | Annual securities report FY2025 (S100XSOA) | 20 Oct 2026 | same |
| Asia Pacific segment, FY2022 (as first reported, PROXY) | revenue JPY 359.4 billion; segment profit JPY 56.4 billion; 15.69% (old basis, Africa included) | PROXY (P filing, DERIVED) | Suntory Beverage & Food securities report FY2022, PDF page 31 (text layer) | 20 Oct 2026 | T3/sbf_securities_report_fy2022_edinet_extract.md |
| Asia Pacific segment, FY2022 restated (PROXY) | segment revenue JPY 352,615 million; segment profit JPY 57,731 million; 16.37% | PROXY (P filing, DERIVED) | Annual securities report FY2023, prior-year column | 20 Oct 2026 | T3/sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md |
| 7UP Zero Sugar Lemon Soda price | THB 75 for six x 325 mL (PACK6) (12.69 per 330 mL) at Lotus's; THB 16 single pack (16.25 per 330 mL) on the Lotus's Shop Online row via Priceza | S, DERIVED | Lotus's (re-read 20 Oct 2026); Priceza, 20 Oct 2026 | 20 Oct 2026 | T3/retail_price_inputs_from_T4_T5.md |
| 7UP zero-sugar lemon range per 330 mL | THB 12.40 to THB 16.25 | S, DERIVED | Lotus's and the Suntory PepsiCo official store on LazMall (via Priceza), 20 Oct 2026 | 20 Oct 2026 | same |
| est cola price | THB 79 for 6 x 325 mL (13.37 per 330 mL), Makro PRO cash-and-carry listing | S, DERIVED | Makro PRO, 20 Oct 2026 | 20 Oct 2026 | same |
| Lemon Soda price position | THB 15 (assumption) between the 7UP six-pack price (THB 12.69) and the 7UP single-pack price (THB 16.25); Sprite six-pack THB 14.38 also shown | ASSUMPTION against S, DERIVED rows | script `price_position_of_lemon_soda_assumption` | 20 Oct 2026 | rework/screen/t3_pepsi_sermsuk_margins_results.json |
| Singha Lemon Soda Lotus's rows (reference only) | single 330 mL THB 17 (17.00 per 330 mL); six-pack THB 85 (14.17 per 330 mL); 7-Eleven six-pack THB 172 | S; not used in the judge text (conflict 14) | Lotus's rows L7 and L8; 7-Eleven ALL Online page A2 (T5) | 20 Oct 2026 | T3/retail_price_inputs_from_T4_T5.md |
| Packed unit against liquid | 5.29 g against 330 g, 1.60%; 1.50% to 1.74% over the cube allowance range; dry 3.79 g (includes the 0.80 g binder) is 1.15% | DERIVED from an ASSUMPTION input (pouch 1.5 g); nothing weighed | deck unit mass and dry mass; record 72; water at 1 g per mL | 20 Oct 2026 | rework/screen/t3_pepsi_sermsuk_margins_results.json |
| Mini Me, 30 March 2025 (opened) | current share 39.1% (basis not stated); 2025 target 40%; THB 1 billion investment; Saraburi capacity +50% | S | Mini Me Insights article (opened 20 Oct 2026; investment figures attributed to Prachachat) | 20 Oct 2026 | T3/mini_me_2025-03-30_opened_2026-10-20.md |
| Royal Gazette item 02.02 schedule | From 1 Oct 2566: 0, 1, 3 and 5 baht a litre by sugar band (14% ad valorem in each row; value base not read) | P (page images; Thai numerals read from the images) | Royal Gazette 2560 A/095/111 (https://www.ratchakitcha.soc.go.th/DATA/PDF/2560/A/095/111.PDF), read 19 Oct 2026 | 19 Oct 2026 | rework/raw/gazette_sugar_drink_excise_primary_2560_A095_111.md; script fourth_pass_sugar_tax_ladder_check |
| Sugar-tax phase 4 (press) | From 1 Apr 2025, reported at 0.3 to 5 baht a litre; no primary notice for that period read | S (press only); not checked against a notice | Brand Buffet 17 Apr 2025 (block 7) | 20 Oct 2026 | T3/csd_market_share_press_2020_2025.md block 7 |
| SPBT investment 2025 | THB 1,000 million; Saraburi carbonated capacity +50% | S | Brand Buffet 17 Apr 2025; Mini Me 30 Mar 2025 | 20 Oct 2026 | T3/csd_market_share_press_2020_2025.md |
| SPBT investment 2026 | over THB 2,000 million for two lines; up to 800 million litres a year | S (company release relayed) | Workpoint, 10 Jul 2026 | 20 Oct 2026 | T3/rereads_after_verifier_2026-10-20.md |
| SPBT outlets | over 470,000; 25 partners; 68 delivery points (about September 2018) | S, dated | Bangkok Biznews 812103 | 20 Oct 2026 | T3/spbt_ownership_and_jv_press_2017_2018.md; T3/rereads_after_verifier_2026-10-20.md |
| est outlets | over 100,000 grocery shops (about Oct 2023) | S | Bangkok Biznews 1093142 | 20 Oct 2026 | T3/csd_market_share_press_2020_2025.md |
| SPBT revenue and profit | not obtained | UNVERIFIED | DBD statements (not readable) | 20 Oct 2026 | T3/blocked_and_unopened_2026-10-20.md; T3/rerun_search_leads_and_blocked_2026-10-20.md |

## 15. Sources

Primary (P):

- SET notice, "SET announces the delisting of SSC's common stocks from SET", published 11 December 2024 (https://www.set.or.th/en/market/news-and-alert/newsdetails?id=92823700&symbol=SET), read 20 October 2026.
- ThaiBev announcement to SGX, "Progress on the Delisting Tender Offer for All Remaining Shares of Sermsuk Public Company Limited", 27 November 2024 (attachment https://links.sgx.com/FileOpen/Sermsuk_Delisting.ashx?App=Announcement&FileID=826567; announcement page https://links.sgx.com/1.0.0/corporate-announcements/G1KIRCJBY36GZ9FS), read as a page image 20 October 2026.
- Sermsuk Public Company Limited, Minutes of the 2025 Annual General Meeting of Shareholders, held 30 January 2025 (English unofficial translation, https://www.sermsukplc.com/ssc_cms/storage/shareholder_news/pdf/251216114512/2025.01.30_SSC_Minutes_AGM_2025_EN_(v4)_Final.pdf), pages 2, 14, 15 and 23 read as page images, 20 October 2026.
- ThaiBev announcements to SGX: 3 July 2024 (https://links.sgx.com/1.0.0/corporate-announcements/XJ4SAIDZVZLD9AVA/808724_Tender_Offer_SSC_Shares.pdf; record date 6 December 2023 and 64.67%), 15 November 2024 (https://links.sgx.com/1.0.0/corporate-announcements/8Y820EFUN5FKTBSU/825548_SSC_FS_FY2024.pdf; record date 17 July 2024 and 64.67%).
- Sermsuk MD&A for FY2022, FY2023 and FY2024 (https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202211/22137968.pdf, .../202311/0009NWS151120231852450901E.pdf, .../202411/0009NWS151120241815250070E.pdf).
- Sermsuk Form 250-2 with the independent adviser's opinion, 8 October 2024 (http://capital.sec.or.th/webapp/corp_fin/datafile/TO/0009000333250-22024-10-08e01.pdf), pages 2, 8, 9, 10, 11, 15, 16, 42, 63, 64 and 94 extracted.
- Thai SEC filing index for SSC (https://market.sec.or.th/public/idisc/en/FinancialReport/ALL-0000000694/20240101-20261020?symbol=SSC).
- SET and TFEX notice, 4 July 2024 (https://www.tfex.co.th/en/market-data/news-and-notice/trading-notice/newsdetails?id=89857500&symbol=SSC).
- Suntory Beverage & Food annual securities report, FY2022 (https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100QGLN.pdf), PDF pages 4, 31, 34 and 116.
- Suntory Beverage & Food annual securities report, FY2023, 第15期, filed 28 March 2024 (https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100T62P.pdf), segment note, MD&A and subsidiaries table; read 20 October 2026 (text layer, saved in `sbf_apac_segment_fy2023_fy2025_edinet_2026-10-20.md`).
- Suntory Beverage & Food annual securities report, FY2024, 第16期, filed 27 March 2025 (https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100VHVQ.pdf); same saved file.
- Suntory Beverage & Food annual securities report, FY2025, 第17期, filed 23 March 2026 (https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XSOA.pdf); same saved file.
- PepsiCo SEC XBRL (https://data.sec.gov/api/xbrl/companyconcept/CIK0000077476/us-gaap/Revenues.json, GrossProfit.json, NetIncomeLoss.json).
- ThaiBev SGX year-end announcements FY2024 and FY2025, and the NDR presentation of January 2025 (read and saved by T4; see `rework/raw/diligence_2026-10-20/T4/`).
- Royal Gazette 2560 (2017), Ministerial Regulation excise schedule, item 02.02, file 095/111 (https://www.ratchakitcha.soc.go.th/DATA/PDF/2560/A/095/111.PDF), read as page images 19 October 2026; saved as `rework/raw/gazette_sugar_drink_excise_primary_2560_A095_111.md`.
- Suntory PepsiCo company news, 7 May 2026 (https://suntorypepsico.co.th/en/news/detail/brand/c0FzVw), as a company statement.

Secondary (S), saved in `rework/raw/diligence_2026-10-20/T3/` unless stated:

- Thansettakij: 590894 (16 Mar 2024), 623088 (26 Mar 2025), 624003 (3 Apr 2025), 560215 (27 Mar 2023), 641276 (13 Oct 2025, saved by T4); Thairath 2778345 (15 Apr 2024); Gotomanager 5234 (29 Oct 2023); Bangkok Biznews 1093142 (about Oct 2023) and 812103 (about September 2018); Bangkokbiznews 1202914 (13 Oct 2025, T1 row 11); Brand Buffet (4 Nov 2014; 10 Mar 2016, T4; 17 Oct 2023, T4; 27 Aug 2024; 17 Apr 2025, https://www.brandbuffet.in.th/2025/04/suntory-pepsico-beverage-strategy-2025/); Positioning (26 Mar 2020; 21 Mar 2023, T1 row 1); Mini Me Insights (23 Feb 2020; 8 Aug 2021; 30 Mar 2025, opened 20 October 2026: `mini_me_2025-03-30_opened_2026-10-20.md`); The Nation (2 Nov 2017); Prachachat (2017, JV seller and 49% side, snippet read); M&A Online (2 Nov 2017); Brand Inside (4 Sep 2018, ownership, start date and plants only); MGR Online (25 Oct 2012); Business+ (8 Jan 2024); Marketeer (3 Feb 2025; 15 Mar 2024, T4; 12 Mar 2025, T4); MarketPlus (8 May 2024, T1); Workpoint Today (10 Jul 2026); Asia Food and Beverages (Aug 2024; Apr 2025); TipRanks (27 Nov 2024); Wikipedia, Est Cola; Creden registry page (https://data.creden.co/company/general/0105546139004).
- Retail listings read by other tasks and re-read on 20 October 2026: Lotus's product page 171266560 (re-read for the pack wording), Lotus's, Priceza, Makro PRO, 7-Eleven ALL Online (T4, T5 and capture 19; see `retail_price_inputs_from_T4_T5.md`).
- Thaiger, review of Sprite Lemon Plus, 29 August 2022 (https://thethaiger.com/th/news/641196/), read 20 October 2026; saved as `rework/raw/diligence_2026-10-20/T5/thaiger_sprite_lemon_plus_2022.md`.
- Thansettakij 641276 (13 October 2025), re-read 20 October 2026 with WebFetch for the attribution of the 10.6%, 17,391 and 68,000 figures (a small-model extract; saved as `rework/raw/diligence_2026-10-20/T3/pass4_rereads_2026-10-20.md`). The 10.6% and the 17,391 carry no attribution in the article; the 68,000 is credited to a ThaiBev senior director.
- Suntory Beverage & Food quarterly supplemental and tanshin releases for 2023 to 2025: the company's own pages returned HTTP 403, and the search snippets were not used as figures (the annual securities reports above supersede them; see `rerun_search_leads_and_blocked_2026-10-20.md`).

## 16. Changes in the re-run (20 October 2026)

Pass 1 (the first re-run of the day):

| Item (before this re-run) | What the re-run found | Change made |
|---|---|---|
| Sermsuk delisting: effective date "not confirmed"; a snippet gave 19 December 2024 (limit 3) | SET notice of 11 Dec 2024 (P): delisting from 20 Dec 2024, last trading day 19 Dec 2024. 2025 AGM minutes (P, p.23): "has been delisted from the SET" | Date stated as verified; limit 3 narrowed to the period after 30 January 2025 |
| Tender offer: 99.19% stated from a ThaiBev notice (P), period and shares not stated | SGX announcement of 27 Nov 2024 read as a page image (P): tender period 19 Sep to 22 Nov 2024; 91,786,404 shares (34.52%) acquired; 263,741,208 shares (99.19%) held | Added to sections 1, 2, 9 and 14; the script `t3_rerun_listing_checks.py` derives the value (THB 5,782.5 million accepted; THB 5,918.6 million at the maximum offer, consistent with Brand Buffet's THB 5,918 million) |
| Thai Drinks described as a "ThaiBev group company" | The filing shows So Water holds 4.95% of Thai Drinks (P, page 42). Controlling holder not found | Corrected in sections 1, 2 and 11.2 and conflict 10 in section 12 (pass 3 adds the press claim with its source) |
| est trademark owner stated as the ThaiBev group with the 2014 buyer named in two ways | Form 250-2 page 8 (sale to Super Brands Company Pte. Ltd.) and page 64 ("ThaiBev, who owns the trademark") confirmed in the saved text | Section 2 cites both pages and names both buyers as printed; the link between them is not stated |
| Sermsuk FY2024 figures from the SET MD&A only | 2025 AGM minutes page 14 (P) confirm revenue 13,153, cost of sales 9,306, distribution 3,033, admin 736 and net profit 404 (up THB 156 million); FY2023 net 248 reconciles | Added to section 7.1 and the figure register |
| Sermsuk founding and listing dates ("listed 1975") | 1952 founding (P, ThaiBev 3 Jul 2024); Form 250-2 history gives 1975 "being a listed company" and 1994 "became a listed company" | Founding date added; the two listing dates are stated as an unreconciled conflict (section 12, conflict 12) |
| SPBT registry number and 2003 registration | Creden registry page (S, aggregator of DBD data) gives registration 0105546139004 and 18 Nov 2003. Juristic-number search in this run returned no statement | Kept with tier S and the aggregator named; no financial figure taken from it |
| Suntory Asia Pacific FY2023 to FY2025 (limit) | Suntory's releases blocked (HTTP 403); snippets conflicted | Superseded in pass 3 (see below) |
| Pepsi trademark holder: "a search summary said Pepsi-Cola (Thai) Trading" | A 2003 trade press item says the same (S, dated). No registry or primary page | Kept as UNVERIFIED (limit 5) |
| Mini Me 2025 share target and Pepsi 39.1% | Snippet only in pass 1 | Superseded in pass 3: opened 20 October 2026 |
| The earlier limit "no 2025 share" | Searched again (Euromonitor and Mini Me snippets); no 2025 NielsenIQ or Kantar table found | Limit 10 restated with the search result |
| Judge-facing text (11.2) | Updated for the delisting and for the trademark and marketer wording | Sections 11.2 and 11.4 (speaker note) carry the verified dates |

Pass 2 (the independent verifier's issues, closed in pass 3 on the same day; section 17 maps each issue):

| Item | Change made in pass 3 |
|---|---|
| Sugar-free wording in sections 8 and 11.4 | Removed. Section 8 and the note bar state no sugar-free claim. Conflict 15 added. |
| Singha Lemon Soda prices in the note bar and section 5 | Removed from the judge-facing note bar; the price range uses the 7UP and Sprite rows only. Section 5 rows are labelled reference only. Conflict 14 added. |
| Quoted note bar in section 12 item 8 | Corrected to the deck's actual sentence; removal of the Phase 5 sentence listed (conflict 8 and conflict 16). |
| Asia Pacific margin labelled "P, DERIVED" in 11.3 | Relabelled PROXY; described as a segment profit ratio. Figures now from the FY2023 to FY2025 reports. |
| 75% attribution to Thansettakij 26 March 2025 | Corrected to Brand Buffet, 17 April 2025 (S), which the saved block 7 shows. |
| Thai Drinks ThaiBev link "not supported" | Replaced with the press claim (Bangkok Biznews, Gotomanager; S) and the primary 4.95% stake (P). Both S conflicts (launch year 2011 against 2012; "Thai Drink" against "Thai Drinks") listed as conflict 13. |
| Mini Me labelled as a snippet | Opened on 20 October 2026 with WebFetch; saved as `mini_me_2025-03-30_opened_2026-10-20.md`; leads file line 26 corrected. |
| Suntory page 31 segment heading and the 28.6 figure | The FY2022 report's text layer reads アジアパシフィック事業; 28.6% is the currency-neutral growth in segment profit. Explained in 7.4. |
| Suntory FY2023 to FY2025 not tried on EDINET | Tried. The FY2023, FY2024 and FY2025 annual securities reports were read (P) and saved. The FY2023 snippet (43.1) is confirmed. |
| 325 mL can for 7UP Zero Sugar Lemon Soda | Replaced with "325 mL, six-pack" after re-reading the Lotus's page (PACK6; no "can" on the page). |
| Colour-soda 17,391 million attributed to a ThaiBev statement | Attributed to Thansettakij quoting a ThaiBev non-alcoholic executive; the printed 30% is not used (section 11.2). Superseded in pass 4: the article gives no attribution for this figure (section 18, item 2). |
| Packed-unit basis "assumed pouch and assumed binder" | Corrected: the binder is inside the 3.79 g dry mass; the assumption is the 1.5 g pouch (sections 1, 10, 11.4; script). |
| Sprite 24-pack deck row dropped without a note | Removal listed (section 12, conflict 16). |
| 64.67% with two dates (6 Dec 2023 and 17 Jul 2024) | Both dates stated with their sources; the script `so_water_holding_before_tender_check` checks the percentage at the first date. |

Pass 3 also adds the Asia Pacific FY2023 to FY2025 series and its Thailand commentary to section 9, and the 11.3 table row for the proxy.

## 17. Verifier issues and how each was closed (pass 3, 20 October 2026)

All 14 issues (1 high, 8 medium, 5 low) were checked against the saved files and the deck and submission text. None was wrong; each is closed as follows.

| # | Severity | Issue | Closure | Where |
|---|---|---|---|---|
| 1 | high | Sugar-free claim shared with zero-sugar cans (sections 8 and 11.4) | Removed; conflict added. Deck line 122 and submission 04 line 59 confirmed. | 8, 11.4, 12 (15) |
| 2 | medium | Singha prices in the note bar and section 5 against "not verified" | Removed from the judge text; conflict added with the cited rows and the options for the lead. | 5, 11.4, 12 (14) |
| 3 | medium | Quoted note bar "not in price" wrong; Phase 5 sentence dropped without a list | Quote corrected; removal listed. | 12 (8, 16) |
| 4 | medium | Asia Pacific margin labelled P, DERIVED in 11.3 | Relabelled PROXY; segment profit ratio. | 1, 7.4, 11.3, 14 |
| 5 | medium | 75% attributed to Thansettakij 26 March 2025 | Attribution corrected to Brand Buffet 17 April 2025 (block 7). | 8 |
| 6 | medium | Thai Drinks ThaiBev link "not supported"; Bangkok Biznews conflicts unlisted | Press claim stated with its source; So Water 4.95% kept as the primary fact; both S conflicts listed. | 1, 2, 12 (10, 13) |
| 7 | medium | Mini Me labelled snippet; two saved files disagree | Opened today and saved; leads file corrected. | 3.2, 9, 14, 15, 16; leads file line 26 |
| 8 | medium | Suntory page 31 heading not legible; 28.6 unexplained | Confirmed in the text layer (アジアパシフィック事業); 28.6 is the currency-neutral growth rate. | 7.4 |
| 9 | medium | FY2023 and FY2024 EDINET reports not tried; three-year bottler proxy missing | FY2023, FY2024 and FY2025 annual securities reports read (P) and saved; the three-year series is in 7.4. SPBT's own statements remain a limit. | 7.4, 13 (2) |
| 10 | low | 325 mL can for 7UP Zero Sugar Lemon Soda | Corrected to six-pack after re-reading the Lotus's page. | 4, 11.1 |
| 11 | low | 17,391 million called a ThaiBev statement; 30% inconsistency omitted | Attributed to the quoted executive; the 30% is not used. Superseded in pass 4 (section 18, item 2): no attribution in the article. | 11.2 |
| 12 | low | Note bar packed-unit basis (binder) | Corrected. | 11.4, 1, 10 |
| 13 | low | Sprite 24-pack deck row dropped without a listed removal | Listed. | 12 (16) |
| 14 | low | 64.67% with two dates | Both dates stated with their notices; the check script added. | 14, 15 |

## 18. Verifier issues of the fourth pass (20 October 2026) and how each was closed

The fourth list has 13 items: six medium and seven low. The third-pass summary counted 14 items; the list received now has 13. Each item was checked against the saved files. Two points were checked again on the live pages on 20 October 2026: the speaker attribution of the Thansettakij figures (WebFetch, extract saved in `rework/raw/diligence_2026-10-20/T3/pass4_rereads_2026-10-20.md`) and the sugar-tax phase 4 leads (search only, not opened). Where a verifier item was only partly right, the closure says so.

| # | Severity | Issue | Closure | Where |
|---|---|---|---|---|
| 1 | medium | "Acquired 99.19%" overstated the tender offer | Corrected to: acquired 34.52% of the shares in the tender offer, then held 99.19% (ThaiBev announcement of 27 November 2024, P: 91,786,404 and 263,741,208 shares). The same change is made in section 1 finding 3 and judge text 11.2. | 1, 11.2, 14 |
| 2 | medium | 10.6% and THB 17,391 million attributed to a ThaiBev executive | Confirmed by re-read on 20 October 2026. Neither figure carries an attribution sentence in the article; only the THB 68,000 million total is credited to a named ThaiBev senior director. The attribution is removed for the 10.6% and the 17,391 throughout the record and in judge text 11.2 and 11.4. The T4 extract's speaker line describes the article's company statements, not these figures. | 1, 3.2, 3.3, 3.4, 11.2, 11.4 |
| 3 | medium | FY2024 Non-Alcohol attributable profit (1,455) shown beside FY2025 2,414 with no note | Both bases are now shown. The FY2024 announcement gives 1,455 (up 259, or 21.7%, on 1,196). The FY2025 announcement gives 1,146 for the FY2024 comparative and moves Others from 2,191 to 2,500. The 309 million baht moves between the two rows; both splits sum to 27,215 (script). The 110.6% growth printed for FY2025 is measured from 1,146 (65.9% from 1,455). The FY2025 extract does not label the move a restatement. The FY2024 table's movement figure of 251 does not reconcile to the narrative 259, so the narrative is used. | 7.3, 14 |
| 4 | medium | "No system sells a lemon soda like the Singha Lemon Soda can at 330 mL" (absence claim) | Reworded to: no lemon soda in 330 mL was found in the pages read; this is not a full market survey. The Schweppes zero-sugar 330 mL releases and the Makro Schweppes lime listing are in the Coca-Cola system material (T2), which is not classified here. | 4 |
| 5 | medium | Sprite Lemon Plus had no saved T3 page; submission/11 line 92 row not in the conflicts | The Thaiger review (29 August 2022) is saved in the T5 folder and is now in the slide 8 competitor strip and source line. Submission/11 line 92 is conflict 18, with replacement row wording. The Lazada rows read on 20 October 2026 show THB 365 for both Sprite 24-can rows, with no date stamp and no seller. | 11.4, 12 (16, 18) |
| 6 | medium | Phase 4 sugar-tax rates (THB 0.3 to 5 a litre) rest on press only; no reconciliation with submission/10 line 22 | Phase 4 is tiered S (press only, not checked against a notice) in sections 9 and 10 and in the figure register. Conflict 19 records the mismatch. The saved Royal Gazette schedule (P) gives 0, 1, 3 and 5 baht from 1 October 2566, which matches submission/10 line 22. The press phase 3 ladder matches the 1 October 2564 row, not the press dates (script `fourth_pass_sugar_tax_ladder_check`). Stated limit 18. | 9, 10, 12 (19), 13 (18), 14 |
| 7 | low | Internal notes in judge text: the "(replaces the 7UP NS Strawberry Lemon row)" parenthetical and "so that percentage is not used" | Both removed. Judge text 11.2 keeps the source caveat only. | 11.1, 11.2 |
| 8 | low | Thai Drinks: the Gotomanager owner-chain sentence was not quoted | Quoted in section 2 (team translation of the saved extract) and in limit 6 as an ambiguous lead. Control of Thai Drinks is still not established. | 2, 13 (6) |
| 9 | low | Chang rows mix two product scopes | The scopes are stated and the two series are not comparable; no growth rate is taken across them. Script `fourth_pass_chang_scope_check`: the FY2025 scope implies an FY2024 base of 132.9 million litres, against 122.8 million litres printed for the FY2024 scope. | 4 |
| 10 | low | "A joint venture that began in March 2018" had no tier | Tagged (S), as the verifier asked. | 11.2 |
| 11 | low | Raw retail file: pack column "6 x 325 mL cans" | The 7UP Zero Sugar Lemon Soda row now reads PACK6, with the note that the page does not use the word can; the listed price of 80 (struck) and the "฿75.00/Each" unit label are recorded. The strawberry row reads "printed as PACK 6". | `T3/retail_price_inputs_from_T4_T5.md` |
| 12 | low | Script comment cites a "SET/TFEX notice" for 93,945,680 shares | The comment now cites the 3 July 2024 ThaiBev announcement (line 27 of the saved file) and Form 250-2 page 10. A check was added: 63 times 93,945,680 equals 5,918,577,840, the Form 250-2 page 10 total. | script `t3_rerun_listing_checks.py`; 14 |
| 13 | low | The 66,000 window was attributed to Thansettakij 16 March 2024 | Partly right. Thansettakij prints the window and the +12% as NielsenIQ growth rates, but gives no source for the 66,000 value. The NielsenIQ attribution of the value and the window is in Marketeer (15 March 2024) and MarketPlus (8 May 2024). Section 3.3 and the figure register are corrected. | 3.3, 14 |

### Changes in pass 4

- Record `68b_pepsi_sermsuk.md`: the items above, and conflicts 18 and 19 and limit 18 added.
- Scripts: `t3_rerun_listing_checks.py` (source comment; maximum-value check against the Form 250-2 total) and `t3_pepsi_sermsuk_margins.py` (fourth-pass block: ThaiBev Non-Alcohol split, Chang scope, sugar-tax ladder against the Gazette). Both rerun on 20 October 2026, one at a time; both results JSON files regenerated.
- Raw: `T3/retail_price_inputs_from_T4_T5.md` (pack wording for two 7UP rows, CRLF kept); `T3/pass4_rereads_2026-10-20.md` (new).
- Not changed: submission, proposal and deck files, as rule 6 requires. Conflicts 14, 16, 18 and 19 list the changes the lead has to make there.

### Still not verified after pass 4

- SPBT's own revenue, gross profit and net profit: the Department of Business Development statements were not readable (stated limit 1).
- Pepsi-Cola (Thai) Trading's statements, and the ownership of its 49% side of the joint venture (stated limit 3).
- Sermsuk after the 30 January 2025 AGM minutes, including any FY2025 statements (stated limit 4).
- The content of the FY2023 correction report of 14 March 2025 (stated limit 2).
- Sugar-tax phase 4: no phase 4 notice was read, and later amendments to item 02.02 were not searched (stated limit 18).
- The measure (retail or manufacturer; volume or value) of the 66,000 and 70,772 value figures and of the 8.6%, 10.6% and 30% to 39.1% share figures (stated limits 10 and 11).
- The date and seller of the Sprite 24-pack rows on Lazada (conflict 18).
- Whether ThaiBev controls Thai Drinks Co., Ltd. (stated limit 6).

