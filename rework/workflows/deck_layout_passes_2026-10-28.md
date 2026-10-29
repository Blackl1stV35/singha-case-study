# Deck layout passes (28 October 2026)

Scope: layout edits only (position, resize, format, line geometry) on the staged Canva copy `DAHZRLUtEGk`. No wording changed except the page-badge digits. The original deck and the baseline copies were not edited. Saved workflow: `.claude/workflows/singha-deck-layout-then-loop.js` (args: `layout_tasks`, `allowed_ops`, `audit_groups`, `skip_loop`, `loop_args`).

## Result after the fix loop (round 5)

8 of 9 judges advance (mean 6.6); 10 open objections, all medium. Every page is under its word cap (5,021 words; page 16 is 134 of 140). The advance rule (at least 7 of 9 and no verified high objection) is met. Log: `deck_fix_loop_log_2026-10-28-r5.md`.

## Layout fixes landed

- Page 12: notes moved off the waterfall axis labels and the navigation bar; leader line re-seated on the Contribution bar.
- Page 14: trading-week ticks (wk 1, 4, 8) placed inside the Week 30 to 43 bar in order; Week 43 connector joined; band label spacing.
- Page 15: Phase 4 ends and Phase 5 starts at week 43, Phase 5 ends at week 48 (matches pages 4, 14, 16: 13 trading weeks, Week 43 to 48); Phase 0 bar and Week 0 label moved onto the axis scale; axis numbers aligned to ticks.
- Page 16: the signature ask is its own bold 26 px block; the other two paragraphs keep the original size.
- Page 22: the 7% scale-limit line, the 25% mean tick and the prior line moved onto the axis scale.
- Pages 4, 5, 7, 8, 9, 10, 11, 12: spacing, nav-label alignment, badge position, red-box and callout fixes, white-on-gold text recoloured for contrast.
- Page badges run 1 to 12 on pages 4 to 15.

## Chart fixes done in Canva through Claude in Chrome (29 October 2026)

- The parentheses on chart labels came from a literal "(" prefix and ")" suffix in the chart data table's column format. Cleared on page 18 (line chart), page 20 (tornado), page 21 (A/B/D bars and variance bars). The page 21 bottom chart keeps its brackets on purpose (the slide says cubes a year in brackets).
- Page 20 tornado: the 12% discount-rate case was stored as -0.12; the correct NPV is +0.12 (recomputed from the stated cash-flow convention: 8% gives 0.21, 10% gives 0.17, 12% gives 0.12; matches pages 18 and 19). Corrected to 0.12. The "Base 0.17" line was drawn at the zero axis; moved to the 0.17 position (bars are absolute NPVs from zero).
- Extra copies `DAHZSFXJYeE` and `DAHZRKYhszs` moved to Canva trash (restorable for 30 days) on the user's confirmation. The staged copy `DAHZRLUtEGk` is the final deck for submission.

## Final deck moved to the original link (29 October 2026, user instruction)

- `DAHX_hKTpDE` now holds the final deck: renamed "Singha Lemon Soda Cube – Final", 19 pages, no hidden pages (the hidden pages 1, 2, 4 and 6 of the original were removed; the 19 visible pages of the working copy were inserted and the original 23 pages deleted). Badges renumbered 1 to 11 on pages 2 to 12.
- Page 18 (Model Results): the red Pilot Floor line crossed bar A's data label. The chart's data labels were turned off and the cubes-a-year figures were added to the "x units" text boxes beside each bar (for example "2.55 units (170,300)"), each placed just right of its bar end.
- Safety copies: `DAHZUgx5WUs` (the original before the replace) and the working copy `DAHZRLUtEGk`. Delete when the user has checked the final deck.

## Not fixable through the connector (stated limits)

- Page 18 table: first-column labels are clipped ("tax" is cut off); the connector cannot widen the columns.
- Page 5: the can's flavour list (Watermelon, no Yuzu) differs from pages 2, 4, 6 and 10 (Yuzu); no source to settle it.
- Page 5: an empty decorative beige band bleeds off the left edge (deleting it was out of the layout rules).
- Canva file title is still the template name; page 2 (Brand Portfolio) sits before the cover.

## Final read-only verification

Six read-only checkers found no high-severity defect on pages 2 to 16 and no disagreeing week or key figure in the slide text and notes. High items on pages 15, 18, 20 and 21 were the chart format and data points above and the page 15 week-0 origin (fixed afterwards). Medium and low cosmetic items remain (small type on pages 5, 12, 15; a few 2 to 5 px box overlaps with no glyph collision).
