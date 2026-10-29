# CORECHEM, Citric Acid Solution Properties: specific gravity of citric acid solutions

- URL read: https://corecheminc.com/citric-acid-solution-properties/
- Date read: 2026-10-20 (WebFetch, model-summarised; table rows as returned)
- Tier: S (a chemical supplier's reference page; no author or date on the page). Status: SOURCED, secondary, used only to convert a solubility in percent w/w to g/L.

## Extracted rows (specific gravity at 15 C, as printed)
- 40 percent w/w 1.1709; 48 percent 1.2103; 50 percent 1.2204; 52 percent 1.2307; 54 percent 1.2410; 56 percent 1.2514; 58 percent 1.2627; 60 percent 1.2738. The table runs from 2 to 60 percent.
- The density column on the page is in lb/ft3 with no stated temperature and looks inconsistent with the specific gravity column; it is not used.
- The page does not state a saturation concentration.

## Use in rework/71
- Citric acid solubility at 20 C is 59.2 percent w/w (Wikipedia citric acid, saved in wikipedia_physical_constants.md). Specific gravity interpolated between 58 and 60 percent at 59.2 percent: 1.2694. Concentration of the saturated solution: 0.592 x 1.2694 x 1000 = about 751 g/L (DERIVED; the 15 C chart is applied at 20 C, a difference below 0.5 percent, ASSUMPTION). Used only in the composition-weighted saturation concentration variants of the dissolution model.
