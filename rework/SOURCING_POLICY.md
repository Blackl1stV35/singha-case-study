# Sourcing policy (19 October 2026)

Applies to every figure, fact and claim in the repo. Team-only records and judge-facing files both follow it. Set by the user on 19 October 2026: secondary sources are allowed, and primary sources come first.

## 1. Priority

**Primary (use first):**
- Laws, regulator notifications and gazettes (Thai Royal Gazette, Thai FDA and Ministry of Public Health notifications, and the Thai text rather than a translation where one exists).
- Statistical office releases and their tables (NSO Thailand and the like), with the table and page number.
- Company filings and reports: annual reports, Form 56-1 and similar, DBD filings, SET and SEC filings, company press releases.
- Exchange and index prices with the date (LME, exchange rates from the central bank).
- Patents and patent office records, with the number and the claims read.
- Peer-reviewed papers, and standards bodies' texts.
- The maker's own product label, spec sheet or quote published on the maker's site.

**Secondary (allowed when no primary is reachable, always labelled):**
- Trade press and industry news reports, including ones that quote a primary.
- Market research summaries and paid-report excerpts.
- Financial aggregators (stockanalysis, marketscreener, infobel and similar).
- Encyclopaedias and textbook summaries.

**Not usable as a source:**
- A search-result snippet that has not been opened. It is a lead, not evidence.
- An unlabelled listing, a forum post, a blog without an author or date.
- AI-generated summaries, and marketing copy used as evidence of performance.
- Anything with no date or no author that cannot be traced.

## 2. Rules

1. **Prefer primary.** If a primary exists and is reachable, cite it. Use a secondary only when the primary cannot be reached, and say so.
2. **Name what you used.** Give the document, the page or table, and the URL. For a secondary, also name the primary it reports, when it does.
3. **Tier every figure.** Each figure carries: value, unit, as-of date, source, tier (P or S), and status (SOURCED, PROXY or ASSUMPTION).
   - SOURCED: a primary or a labelled secondary.
   - PROXY: a figure from another market, company or year, with the thing it stands in for named.
   - ASSUMPTION: no source; marked as a design or modelling choice.
4. **Never upgrade a secondary.** A secondary is not SOURCED without the word "secondary" in its note.
5. **Conflicts.** Record every value and the spread. Use the primary. If only secondaries disagree, show the range and say so.
6. **Dates.** State the as-of date. Older figures are marked dated, not current.
7. **Translations.** A Thai text quoted in English is our translation unless the source gives an English version. Say which.
8. **Snippets.** Open the page before relying on it. A snippet's claim is noted as "snippet, not opened".
9. **No outside contact for quotes** unless the user approves it. Quote requests are dropped by default.
10. **Competition material.** Read-only. Nothing is submitted or registered. Forms are viewed and not filled in.

## 3. Where it applies now

- Can cost and production model: `58_singha_can_cost_research.md`, and the model that follows.
- Financial projection: `56_financial_projection.md`.
- Consumer persona and acquisition cost: `55_consumer_persona_and_acquisition.md`.
- Unit cost and value chain: `53_unit_cost_and_value_chain.md`.
- Packaging survey and PET: `41_upstream_packaging_survey_thai.md`, `32_pet_compliance.md`.
- Gates and regulation: `50_final_gate_resolution.md`, and the Notification texts it cites.
