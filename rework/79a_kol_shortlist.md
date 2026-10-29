# 79a. Domestic creator shortlist (desk scan, 20 October 2026; revised after the verifier review)

Team-only record. Companion to [79_kol_campaign_research_and_survey.md](79_kol_campaign_research_and_survey.md).

Status: desk scan of public pages only. No creator, agency or manager has been contacted, and nothing here says that any creator is available, interested or willing. Public figures only; no private information. The repo is public on GitHub. This file names real public creators. The lead decides before any push whether it stays in the public copy, is moved out, or is pseudonymised (79 section 11).

Tier S for every follower and engagement figure (aggregator pages read on 20 October 2026; vidIQ pages show "last updated 17 October 2026" and the CreatorDB pages were refreshed in late September and early October 2026). Scores are provisional and are produced by [screen/kol_shortlist_scores.py](screen/kol_shortlist_scores.py), results in [screen/kol_shortlist_scores_results.json](screen/kol_shortlist_scores_results.json), which also holds the band sensitivity runs and the recomputed TikTok statistics. Page readings are saved in [raw/diligence_2026-10-20/T16/09_kol_public_pages_vidiq_hypeauditor_tia.md](raw/diligence_2026-10-20/T16/09_kol_public_pages_vidiq_hypeauditor_tia.md) and [raw/.../T16/21_awards_creatordb_vidiq_candidate_reads.md](raw/diligence_2026-10-20/T16/21_awards_creatordb_vidiq_candidate_reads.md).

## 1. Score rule

Each candidate gets three scores of 0 to 3 and a total of 0 to 9. A point is given only for evidence that was read on a public page; anything not read scores 0.

| Score | Point | Rule |
|---|---|---|
| Audience fit (0 to 3) | up to 2 | Genre read from the channel's titles and category: 2 if on target (food or drink review, gaming, football or other sport, fitness); 1 if adjacent (food-led travel, humour or vlog, film or game explainers, talk shows); 0 if off target |
| | 1 | The content is adult-directed. 0 where the page evidence points to children (for example a Toys category or Lego school-trip themes) |
| Brand safety (0 to 3) | 1 | No alcohol cue in the titles and topics read |
| | 1 | Not centred on weight loss, body shaping or medical advice (the Thai FDA criteria bar these claims; a creator whose own content rests on them is a claim-drift risk) |
| | 1 | Not child-directed (the product carries the SINGHA name; see 79 section 4) |
| Format and platform fit (0 to 3) | 1 | The format already shows eating, tasting or a hands-on product demonstration. This point is required for a Priority candidate (needed for the dissolution demonstration and the blind taste test; glass-based formats start only after the Gate 7 ruling on glassware) |
| | 1 | A video posted on or after 17 September 2026 (read within a month of the scan) |
| | 1 | The lower-bound YouTube fee for the creator's tier is at or below THB 40,000 (Influencer Marketing Hub, global PROXY, converted at 33.5410 baht per dollar, the Bank of Thailand reference rate for 15 October 2026, P). The THB 40,000 cut-off is an ASSUMPTION, set at the size of the Route B scale tranche; it is not a sourced threshold |

Bands:
- Priority candidate: a total of 8 or 9 with the fee point and the demonstration point. A candidate is not approached until a full public record check and a check of any current alcohol-brand contract are documented.
- Reference (above the pilot fee scale): a total of 8 or 9 without the fee point.
- Reserve: a total of 8 or 9 with the fee point but no demonstration point, or a total of 6 or 7.
- Not recommended on the evidence read: a total of 5 or less.

Tier bands by followers or subscribers: nano 1,000 to 10,000; micro 10,000 to 100,000; mid 100,000 to 500,000; macro 500,000 to 1,000,000; mega above 1,000,000. The nano, micro and mega edges come from the sources (Influencer Marketing Hub, 6 October 2026; Marketing Oops, 18 May 2026). The Influencer Marketing Hub page defines macro as 100,000 to 1,000,000 followers and gives no follower range for mid (its rate table has a mid row). The split of the 100,000 to 1,000,000 band at 500,000 is therefore an ASSUMPTION.

Band sensitivity (screen/kol_shortlist_scores_results.json, section "sensitivity"; the bands depend on two ASSUMPTIONS, the 500,000 split and the THB 40,000 cut-off):

| Setting | Priority candidates | Reference | Reserve, no demonstration point | Reserve | Not recommended |
|---|---|---|---|---|---|
| Baseline (the rule above) | 1 (row 1) | 4 | 2 (rows 4 and 6) | 13 | 2 |
| Previous rule, without the demonstration point | 3 (rows 1, 4 and 6) | 4 | 0 | 13 | 2 |
| Influencer Marketing Hub macro band (100,000 to 1,000,000 as macro, no mid) | 0 | 5 | 0 | 15 | 2 |
| Fee cut-off at THB 33,000 | 0 | 5 | 0 | 15 | 2 |
| Both of the last two | 0 | 5 | 0 | 15 | 2 |

Reading: the Priority candidate is not robust to either ASSUMPTION. It is a candidate under the baseline only.

Brand safety status: provisional for every row. The three brand-safety points rest on the titles or topics read on the aggregator pages, and for most rows on the genre label alone; the Priority candidate rests on one title only. No full title sweep was run.

Controversy check (a gate, not a scoring point): one WebSearch per creator was run for five creators (rows 1, 2, 3, 4 and 6 of section 2, on 20 October 2026). None surfaced a controversy relevant to the creator in the results read, and the leads were not opened. One query is not a sweep. For every other creator the check is "not run". Before any approach, each creator needs a full public record check (Thai and English news, the creator's own posts, listed brand partners) and a check that the creator has no current alcohol-brand contract.

What the rule cannot do (stated limits):
- No creator-level audience age or gender could be read (profile pages are behind a login or return HTTP 403). The fit score is a genre and adult-directed proxy for men aged 25 to 34, not a measure of that audience. At platform level the male share of the adult ad audience is 44.8 percent on TikTok, 48.5 percent on YouTube, 48.8 percent on Facebook and 41.5 percent on Instagram (DataReportal, tier S). The LINE figure of 54 percent male is a share of its monthly active users, not of an ad audience (DataReportal). Among the platforms listed, Instagram has the lowest male share (41.5 percent) and TikTok is 44.8 percent, so this measure does not show TikTok as the platform that skews most female.
- The safety score covers only what the titles and topics on the pages show. For every row the safety score is provisional. For the newest row (Nott Hungry) only one title was read.
- The Instagram and Facebook lists reachable were not usable (the Instagram "Thailand" list is mostly Korean and international celebrities). Creators are scored on YouTube pages; TikTok and Instagram accounts are listed unscored (section 3).
- No micro-tier creator (10,000 to 100,000 followers) could be read on a public page in this run. The pilot's micro creators are therefore chosen by criteria, not from this list (79 section 5).

## 2. Scored candidates (22 YouTube channels read on vidIQ or HypeAuditor, or CreatorDB)

Latest-video ER is vidIQ's engagement rate for the creator's latest video only (one video; not an average). Awards are Tellscore's Thailand Influencer Awards and show genre only, not safety. "Fit", "Safety" and "Format" are the three scores of section 1, each out of 3.

| # | Creator and handle | Tier | Followers or subscribers | Latest-video ER | Genre read from the page | Fit /3 | Safety /3 | Format /3 | Total /9 | Band (baseline) | Controversy check |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Nott Hungry, honest reviews (@imknothungry) | mid | 361K | 2.5% | Food: snack and food reviews; latest title read | 3 | 3 | 3 | 9 | Priority candidate (pending checks; one title read) | one search, nothing relevant surfaced |
| 2 | BANKII (@bankii) | mega | 10.6M | 3.0% | Food: street food, big meals; Japan Expo Best Food 2026 | 3 | 3 | 2 | 8 | Reference: above the pilot fee scale | one search, nothing surfaced |
| 3 | Cinmhef (@cinmhef) | mega | 1.46M | 4.8% | Food: street-food vlogs (TikTok 3.5M followers also); Best Foodie 2026 (1st) | 3 | 3 | 2 | 8 | Reference: above the pilot fee scale | one search, nothing surfaced |
| 4 | FZK Frozenkiss (@fzkfrozenkiss) | mid | 483K | 4.4% | Esports (RoV) and travel vlogs; Best Gaming 2026 (1st) | 3 | 3 | 2 | 8 | Reserve (fee fit; no demonstration format) | one search, nothing surfaced |
| 5 | PEACH EAT LAEK (@peacheatlaek) | mega | 9.12M | 0.9% | Food: eating | 3 | 3 | 2 | 8 | Reference: above the pilot fee scale | not run |
| 6 | Reflex Channel (@reflexchannel) | mid | 139K | 1.2% | Formula 1 and MotoGP stories; Best Sports 2024 (3rd) | 3 | 3 | 2 | 8 | Reserve (fee fit; no demonstration format) | one search, nothing surfaced |
| 7 | หม่อมถนัดแดก, Tanaddak (@tanaddak) | mega | 4.96M | 2.5% | Food: restaurant and dish tasting | 3 | 3 | 2 | 8 | Reference: above the pilot fee scale | not run |
| 8 | Be Fit With Jess (@befitwithjess) | mid | 174K | 3.0% | Home body-shaping workouts, expert interviews; Best Health & Mind 2025 (3rd) | 3 | 2 | 2 | 7 | Reserve | not run |
| 9 | Jack Papho (@jackpapho532) | mega | 9.03M | 1.2% | Travel with food, music, challenges | 2 | 3 | 2 | 7 | Reserve | not run |
| 10 | Jdumofficial (@jdumofficial3) | mid | 440K | 1.8% | Football talk, talk shows; Best Sports 2025 (2nd) | 2 | 3 | 2 | 7 | Reserve | not run |
| 11 | CGGG (@cggg01234) | mega | 7.99M | 4.0% | Mobile-game matches | 3 | 3 | 1 | 7 | Reserve | not run |
| 12 | FOOTBOT (@footbot) | mega | 5.54M | 0.7% | Football skill challenges | 3 | 3 | 1 | 7 | Reserve | not run |
| 13 | HEARTROCKER (@heartrock) | mega | 9.68M | 1.2% | Gaming: horror and multiplayer live streams | 3 | 3 | 1 | 7 | Reserve | not run |
| 14 | JIMSURIYA V.2 (@jimsuriyav2) | mega | 3.25M | 2.7% | Food: unusual food hunts, eating shows; Best Foodie 2025 (1st) | 3 | 3 | 1 | 7 | Reserve | not run |
| 15 | SkizzTV (@skizztv59) | mega | 6.38M | 2.5% | Gaming, snack reviews, news summaries | 3 | 3 | 1 | 7 | Reserve | not run |
| 16 | กาย หงิด, Guy Ngid (@guyngid) | mega | 6.6M | 1.7% | Gaming comedy, card-game shop | 3 | 3 | 1 | 7 | Reserve | not run |
| 17 | Ananped (@ananped) | mega | 8.5M | 2.1% | Vlogs, food challenges, horror series, pranks | 2 | 3 | 1 | 6 | Reserve | not run |
| 18 | NutApiwich (@nutapiwich) | macro | 542K | 1.2% | Food-focused travel vlogs; Best Foodie 2024 (3rd) | 2 | 3 | 1 | 6 | Reserve | not run |
| 19 | The Moof (@themoof) | mega | 1.31M | 0.8% | Film and game story explainers; Best Gaming 2026 (3rd) | 2 | 3 | 1 | 6 | Reserve | not run |
| 20 | fitwithplant (@fitwithplant312) | nano | 6,830 | 1.0% | HIIT fat-burn and toning routines; Best Sports 2024 (2nd) | 3 | 2 | 1 | 6 | Reserve | not run |
| 21 | PojzPlaza (@ppz321) | mega | 9.64M | 3.2% | Gaming (HypeAuditor lists Toys) | 2 | 2 | 1 | 5 | Not recommended on the evidence read | not run |
| 22 | OAUJUN HI-END (@oaujunhiend) | mega | 10.9M | 1.5% | Long challenge, prank and Lego adventure videos (young audience likely) | 1 | 2 | 0 | 3 | Not recommended on the evidence read | not run |

Brief coverage and the Priority candidate. The brief asked for at least 20 domestic KOLs across tiers and platforms. Twenty-two are scored, which meets the count, but all 22 are YouTube channels, one is nano, none is micro, and no TikTok or Instagram account is scored. The platform and micro-tier parts of the brief are not met (stated limit). The one Priority candidate (row 1) is a mid-tier YouTube channel. Option B of the campaign plan funds nano and micro creators only, so it is not funded under option B; it is a candidate for the optional mid-tier video in option A, which is cut first. Option B's creators are to be found by the criteria in section 1, after approval. The candidate is pending the controversy and public record checks. Under the sensitivity settings in section 1 it is not a Priority candidate at all.

Notes on rows 1 and 2: the subscriber count for BANKII is 10.6M on vidIQ; Heepsy's July 2026 Bangkok ranking shows about 10.3M followers (a different platform read; both shown; search snippet, not opened). Row 1 is CreatorDB's Thai food creator; its TikTok account has about 856K followers and its Instagram about 119K (CreatorDB, refreshed 2 October 2026), so on TikTok it would sit in the macro band.

Band counts (baseline, from the results file): Priority candidate 1 (row 1), Reserve with the fee point but no demonstration point 2 (rows 4 and 6), Reference above the pilot fee scale 4, Reserve 13, Not recommended 2. Tier counts: mega 15, mid 5, macro 1, nano 1, micro 0.

Coverage against the requested genres:
- Food and drink reviewers: eight scored (rows 1, 2, 3, 5, 7, 14, 17 and 18, the last two as food-led vlogs and challenges). Most are mega channels. None is a home-bar creator.
- Gaming: seven scored (rows 4, 11, 13, 15, 16, 19 and 21).
- Sport and fitness: five scored (rows 6, 8, 10, 12 and 20).
- Comedy and humour: two scored (rows 17 and 22), both set low on fit.
- Lifestyle: no channel was classified as lifestyle on the pages read; the vlog and travel-with-food channels (rows 9, 17, 18) are the nearest.
- Home bar: none found in the public lists or searches reachable. Home-bar content in this pilot must be non-alcoholic (79 section 4). The creator is to be found by the criteria, not from this list.
- Micro tier (10,000 to 100,000): none scored. Stated limit (section 1).

## 3. Named or tracked candidates not scored (follower tier not read)

These names came from award results pages or CreatorDB. They are not scored because no title, date or follower count could be read on a public page. The tier column is UNVERIFIED. They are listed so that the team can check them by criteria when the pilot is approved. No one listed here has been contacted.

| Name or handle | Platform | Evidence of genre | Follower evidence | Why not scored |
|---|---|---|---|---|
| jamyjamess | YouTube (assumed) | Best Foodie 2025 (2nd) | none read | vidIQ handle page returned the popular-channels list |
| paratt_ | YouTube (assumed) | Best Foodie 2025 (3rd) | none read | as above |
| pangboyz | YouTube (assumed) | Best Gaming 2026 (2nd) | none read | as above |
| GUFUNNAROCK | YouTube | Best Gaming 2025 (1st); gaming | 371K, a third-party estimate page (Net Worth Spot, updated 1 October 2026) | no title or date read; vidIQ page not reached |
| JAI RAW ใจร้าว, ffewelry | YouTube (assumed) | Best Gaming 2025 (2nd, 3rd) | none read | not read |
| Life Dot | YouTube (assumed) | Best Health & Mind 2025 (2nd) | none read | health genre; would need the claim screen first |
| juepak_, mosjookqs | YouTube (assumed) | Best Entertainment 2025 (2nd, 3rd) | none read | not read |
| Foodie.Munchies | Instagram | Food and cooking, Thailand (CreatorDB) | Instagram 1,128,907; engagement 1.0 percent (refreshed 4 October 2026) | mega on Instagram; no titles read |
| J100.Kg | not shown | Food and cooking, Thailand (CreatorDB) | engagement 5.8 percent (refreshed 2 October 2026) | follower count not shown in the extract |

TikTok accounts from the HypeAuditor top 50 for Thailand (unscored). TikTok and Instagram profile pages are not readable here, so these accounts cannot be scored (no titles, no dates). Figures are the per-post averages shown by HypeAuditor (page dated 2026, no day). They are listed so that the team can review the profiles by hand when outreach is approved.

| Handle | Name shown | Followers | Avg views per post | Evidence of genre |
|---|---|---|---|---|
| cardncyn | Carddd | 12.4M | 2M | Best Affiliate Influencer 2024 (1st) |
| win.william_official | Win William | 31.7M | 2.5M | Best Affiliate Influencer 2024 (3rd) |
| iamsungstarwin | Sungstarwin | 8.1M | 1.3M | Best Creatorpreneur 2025 (1st) |
| psiscott | ทราย สมุทร | 1.6M | 787.8K | Japan Expo, Green and Sustainable 2025 |
| domkao | ดมข้าว [Domkao] | 2M | 2.7M | genre not verified |
| spriteder_spd | SPD No.1 | 11M | 2.3M | YouTube category DIY & Life Hacks and Toys (child-leaning) |

Cinmhef (row 3 above) is also on this list at 3.5M followers, 1.1M average views, 150K average likes, 127 average comments and 19.6K average shares per post.

Reading across the 47 accounts of 100,000 followers or more in the 50-row HypeAuditor TikTok table (raw 09 section 2). These statistics are recomputed by screen/kol_shortlist_scores.py from the saved table; they replace the earlier source in screen/kol_campaign_model.py, which is not needed for them. Median per-post views are 0.46 times followers (range 0.08 to 5.1); median likes, comments and shares together are 10.5 percent of followers and 18.0 percent of views. The list is ranked by the aggregator and favours very high averages, so these are upper bounds for a typical creator. For the YouTube channels above, the latest video had a median of 2.6 percent of subscribers in views for the 15 channels of 1 million or more. For the 100,000 to 1 million band the median is 11.5 percent over five channels (Nott Hungry excluded; range 0.2 to 22.5 percent), and 9.2 percent over six channels with Nott Hungry (6.9 percent). Several readings were taken within a day of upload, so they understate the final ratio; the two lowest readings in the five-channel set (FZK 0.2 percent and Be Fit With Jess 0.8 percent) are early readings. Row 1 (Nott Hungry) had 24.81K views on 361K subscribers in its latest video, about 6.9 percent (DERIVED).

## 4. Set aside after reading

| Channel | Reason |
|---|---|
| One Food and Drinks channel (name withheld from this copy) | A Thai encyclopaedia entry read on 20 October 2026 for one public-record check raised a brand-safety question about the sale of unregistered goods. The question has not been checked against a primary source and is not used in any score. The channel is not scored here. The detail and name are withheld pending a primary-source check and the lead's decision on the public copy. |
| Doctor Tany (@drtany, 1.16M) | Medical and health content; the Thai FDA criteria bar recommendation or praise of a food's benefits by medical or public health personnel (article 4(6)); the page also lists the country as United States. |
| Dek Jew Chill Out (@dekjewchillout, 5.51M) | Children's drama skits. |
| KRK Channel (@xkrkx, 6.73M) | Minecraft series, children's audience likely. |
| ZENSE MORE (@zensetv, 8.39M) | Variety and talk-show channel; no food or drink fit read. |
| Genierock (@genierock2, 17.3M) | Music-label channel. |

## 5. What Singha has publicly done with presenters and creators

Press read on 20 October 2026 (tier S; saved in [raw/diligence_2026-10-20/T16/08_singha_presenters_and_kol_press.md](raw/diligence_2026-10-20/T16/08_singha_presenters_and_kol_press.md)).

- Singha Lemon Soda, 2020 to 2026: none of the launch releases read (August 2020, June 2021, August 2022, September 2023, June 2024, April 2025, August 2026 Korea) names a presenter, ambassador, celebrity, influencer or KOL. The people named are the company's chief marketing officer and a director of the non-alcohol brand marketing group. Two 2026 items are collaborations: the limited "Bloody Nanno" watermelon flavour of 16 March 2026 with the series "Girl from Nowhere: The Reset" (a fan street-tasting activation; no presenter named), and the Halls XS candy of 9 April 2026.
- The 2020 launch article used sugar-free, zero-calorie, vitamin C, health and "Healthier Choice" wording (raw 23). The cube cannot use any of these words (deck Appendix A). A creator who repeats the 2020 wording would breach the rule.
- Singha Soda (plain soda): a song with five named artists on 14 April 2020; a fashion-brand collaboration and colour-changing labels in December 2021.
- Limit: Singha's own social posts, paid creator posts and any affiliate programme could not be read. A search for a 2026 Lemon Soda creator or idol campaign found nothing dated 2026 (search lead only). The press shows no creator use but does not prove there was none.

## Sources

All pages read 20 October 2026 through WebFetch (model-written extracts) or WebSearch (leads, opened where a figure is used); tier S unless stated.
1. vidIQ channel pages, https://vidiq.com/youtube-stats/channel/@HANDLE/ for each handle in section 2 (page "last updated 17 October 2026"; @imknothungry page "last updated 17 October 2026"); list page https://vidiq.com/youtube-stats/top/country/th/ (top 100, updated 19 October 2026).
2. HypeAuditor, https://hypeauditor.com/top-youtube-all-thailand/ (as of October 2026) and https://hypeauditor.com/top-tiktok-thailand/ (2026). The 50-row TikTok table is saved in raw 09 section 2.
3. Thailand Influencer Awards (Tellscore): https://www.thailandinfluencerawards.com/awards/2025 and https://www.thailandinfluencerawards.com/awards/2026?tab=Winners ; 2024 results via Brand Buffet, 18 October 2024, https://www.brandbuffet.in.th/2024/10/thailand-influencer-awards-2024/ .
4. Thai encyclopaedia read for one creator's public-record check (section 4); the detail is withheld from this copy.
5. Influencer Marketing Hub, https://influencermarketinghub.com/influencer-rates/ (last updated 6 October 2026) for tier bands and the benchmark fee.
6. DataReportal, https://datareportal.com/reports/digital-2026-thailand (published 8 November 2025) for platform gender shares.
7. Singha press pages listed in raw file 08 and the 2020 launch article in raw file 23.
8. CreatorDB creator-stats pages (Thailand food creators), https://creatordb.app/creatorstats/imknothungry/ , https://creatordb.app/creatorstats/foodiemunchies/ , https://creatordb.app/creatorstats/j100kg/ (read 20 October 2026; refreshed September and October 2026; raw 21).
9. Net Worth Spot, https://networthspot.com/gufunnarock/net-worth/ (third-party estimate, updated 1 October 2026; raw 21).
10. Controversy searches, one WebSearch per creator for five creators (20 October 2026; raw 21, section E, and the Nott Hungry line added in this revision). Leads, not opened.
11. Bank of Thailand reference rate of 33.5410 baht per dollar for 15 October 2026 (P; Report 123, saved in rework/raw/diligence_2026-10-20/T1/bot_fx_report123_2026-10-20.md).
