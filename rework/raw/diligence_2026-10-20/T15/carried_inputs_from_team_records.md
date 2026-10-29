# Inputs carried from team records (page not saved in T15)

Date recorded: 20 October 2026 (revision 3). These values are taken from the repo records named below. The underlying source pages are not saved in the T15 folder and were not re-opened in T15. Under the repo rule (CLAUDE.md section 3: a figure whose page is not saved is UNVERIFIED) every carried figure that stands for a published statistic is therefore tiered UNVERIFIED here, whatever tier the originating record gave it. The originating tier is shown in the last column for traceability only.

| Input | Value used | Record and location | T15 tier and status | Originating tier |
|---|---|---|---|---|
| Population, men 25 to 34 | 4.76 million | rework/47 section 6 (DOPA, November B.E. 2568, registration basis) | UNVERIFIED (carried; page not saved) | P (DOPA) |
| Population, men 35 to 44 | 4.75 million | rework/47 section 6 | UNVERIFIED (carried; page not saved) | P (DOPA) |
| Population, men 45 to 59 | 6.65 million | rework/47 section 6 | UNVERIFIED (carried; page not saved) | P (DOPA) |
| Population, both sexes 25 to 34, 35 to 44, 45 to 59 | 9,384,203; 9,407,482; 14,904,550 | rework/screen/segment_potency_mc.py (DOPA, November 2568); DOPA bands start at age 26, so the bands are ages 26 to 35, 36 to 45 and 46 to 60 | UNVERIFIED (carried; page not saved). Women are derived as both sexes minus men, so they inherit any band mismatch between the two series | P (DOPA) |
| Population range, primary run | plus or minus 0.96 percent per band | rework/screen/segment_potency_mc.py | UNVERIFIED (carried) | P range |
| Population alternative 1: DDC mid-year men counts | 4.71, 4.65 and 7.13 million for men 25 to 34, 35 to 44 and 45 to 59 (differences from DOPA: minus 1.1, minus 2.1 and plus 7.2 percent) | rework/47 section 6 table; submission/12 line 35 (labelled UNVERIFIED there: "not re-read") | UNVERIFIED (carried); used only to set the range of the sweep `population_range_wide` | UNVERIFIED |
| Population alternative 2: age 60 counted twice | the held 45 to 59 band (ages 46 to 60) is 14,904,550 and is 13,910,913 after the estimated duplicate of 993,637 is removed (minus 6.7 percent) | rework/73 section 5.2 and limit 14 (equal-thirds estimate, an ASSUMPTION; the 56 to 60 band count is not in the repo) | DERIVED, ASSUMPTION; used only to set the range of the sweep `population_range_wide` | DERIVED |
| Odds ratio per year of age, daily sweet-drink consumption | 0.996 (0.991 to 1.001) | rework/47 section 2 (NSO 2021 report); submission/01 line 30 labels the same table "not located, UNVERIFIED" | UNVERIFIED (carried; not found in the saved extract `raw/nso2021_SD10_04_114_extract.md`). It drives the whole age-gradient margin of men 25 to 34 over men 35 to 44 | P (NSO) |
| Internet use by band (NSO ICT 2569 Q2) | 25 to 34: 99.0 to 99.2; 35 to 44: 98.2 to 98.7; 45 to 59: 96.1 to 98.2 percent | rework/screen/segment_potency_mc.py | UNVERIFIED (carried; page not saved); used only in the channel factor (common to all bases to within about 1 percent) | P (NSO) |
| Channel online share | 0.1 to 0.5 | rework/screen/segment_potency_mc.py | ASSUMPTION, carried | ASSUMPTION |
| Contribution per cube or serving | THB 3.6 to 6.8 at mid margins (range); centre THB 4.91 | range: rework/55 section 5, citing rework/53; centre: deck/deck_content.md and submission/05 (six-cube carton, DERIVED) | Team range and team desk value, carried. The centre is a common factor and cannot change a ranking | DERIVED |
| Repeat rate, first purchase to repeat | 30 percent (15 to 40) | rework/55 section 5 | ASSUMPTION, carried | ASSUMPTION |
| Top-2-box baseline grid and intent elasticity | 20 to 50 percent; elasticity 0.5 to 1.0 | rework/49 section 2 | ASSUMPTION, carried | ASSUMPTION |
| Base shelf price (a model input) | THB 15.00 | deck/deck_content.md and submission/11 (the shelf price used in the concept test; the planning price in the deck is THB 9.00 ex-factory, 60 percent of THB 15) | ASSUMPTION (team decision), carried. Used only in the price factor, which is common to all bases | ASSUMPTION |
| Listing-parity shelf price | THB 13.80 | rework/70 (mean of four online listings read 20 October 2026, from rework/68d) | S (online listings), DERIVED mean, carried | S |
| Age-sex ratio inputs for the earlier finding | ratio A median 1.0409 (0.9979 to 1.0855, P 0.941); ratio B median 1.1474 (1.0260 to 1.2837, P 0.979) | rework/screen/segment_stat_results.json | DERIVED (ASSUMPTION-based), carried | DERIVED |
| Singha sales, share or panel by customer base | none in the public record | rework/43 section 4 | Limit (stated) | |
| Lemon Soda can buyers | no buyer profile; product not on sale | rework/43; rework/69 | Limit (stated) | |
| Heavy modern-trade shoppers (Thai share by channel) | none found | rework/55 section 7 | Limit (stated) | |

The potassium-caution coverage cells are no longer carried by memory: they are read from `rework/screen/t10_potassium_cover_results.json` at run time (file last modified 20 October 2026 03:44, recorded in the results JSON) and listed in `potassium_coverage_band_cells_rework73.md`. If the verification of rework/73 changes those band cells, T15 must be re-run (`python rework/screen/ambient_variation.py`, about 40 seconds). The sweet-drink sex split is read from the saved NSO extract and listed in `nso2021_table2_sweet_beverage_5plus_days_by_sex.md`.

What would settle the carried items: the DOPA table for November B.E. 2568 by single year or five-year band and sex (to re-read the six population cells and to settle the age-60 overlap); the NSO 2021 report table that carries the age gradient of daily sweet-drink consumption (to re-read the odds ratio); the NSO ICT 2569 table (internet use by age band).
