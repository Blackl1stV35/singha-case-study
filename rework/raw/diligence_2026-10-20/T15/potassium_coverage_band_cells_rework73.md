# Potassium-caution coverage, band cells read from the rework/73 results file

- Source: `rework/screen/t10_potassium_cover_results.json`, the results file of the rework/73 coverage script (team model). Keys read: `coverage.by_band.<band>.narrow_ckd35_or_acei_arb_pct_low_mid_high` and `coverage.aggregates.adults_25_59.narrow_pct_low_mid_high`.
- Date read: 20 October 2026 (read directly from the file in this revision; the first T15 run used only the men 25-34, men 45-59 and adults 25-59 cells and interpolated men 35-44).
- Tier: team model. DERIVED from published Thai kidney and hypertension surveys with named PROXY inputs (rework/73 sections 5.2 and 5.3). Not a survey cell. The low and high values are model bounds (every input at its low value with full overlap; every input at its high value with no overlap), not a statistical interval; the mode is a midpoint of assumed bounds.
- Narrow group: kidney disease stage 3 to 5, or treatment for high blood pressure with an ACE inhibitor or an ARB. Percent of the group.

| Cell | Low | Mode (mid) | High | Used for |
|---|---|---|---|---|
| Men 25-34 | 0.14 | 1.07 | 5.52 | M25 |
| Men 35-44 | 1.12 | 3.08 | 9.26 | M35 |
| Men 45-59 | 4.26 | 8.28 | 20.54 | M45 |
| Both sexes 25-34 | 0.20 | 1.15 | 4.45 | W25 (PROXY for women); half of SB25 |
| Both sexes 35-44 | 1.12 | 3.09 | 6.94 | W35 (PROXY for women); half of SB25 |
| Both sexes 45-59 | 4.26 | 7.58 | 20.23 | W45 (PROXY for women); SB45 |
| Adults 25-59 | 2.19 | 4.45 | 11.88 | pool |

Notes:

- The DOPA bands in rework/73 start at age 26 ('25-34' is ages 26 to 35), a small mismatch with the NSO bands.
- In rework/73 the three coverage cells for each age band share assumptions (treated share of young adults, ACE inhibitor and ARB share, the 1.5 factor for young men's blood pressure), so the cells move together in truth. T15 draws them independently in the primary run (conservative for rankings) and runs a fully correlated draw as a sweep.
- Women's coverage is not published; the both-sex band cell stands in (PROXY).
