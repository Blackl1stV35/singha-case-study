export const meta = {
  name: 'update-loop-sync',
  description: 'Bring the submission (judge) files and the proposal (team) files into line with the deck content and the confirmed update-loop state, then check each judge file for leaks and contradictions',
  whenToUse: 'Run after update-loop-revise. The deck (rework/deck/deck_content.md) is the source of truth. Judge copies go in rework/submission, team copies in rework/proposal.',
  phases: [
    { title: 'Sync', detail: 'one agent per file rewrites its statements to match the deck and the confirmed state' },
    { title: 'Review', detail: 'an independent reviewer checks each judge file against the deck and scans it for leaks' },
  ],
}

const FILES = [
  { path: 'rework/submission/01_problem_and_pain_point.md', copy: 'judge' },
  { path: 'rework/submission/02_situation_analysis.md', copy: 'judge' },
  { path: 'rework/submission/03_background_and_trends.md', copy: 'judge' },
  { path: 'rework/submission/04_strategy.md', copy: 'judge' },
  { path: 'rework/submission/05_finance_and_project_valuation.md', copy: 'judge' },
  { path: 'rework/submission/06_kpi.md', copy: 'judge' },
  { path: 'rework/submission/07_organization_audit_and_evaluation.md', copy: 'judge' },
  { path: 'rework/submission/08_success_and_fail_case_studies.md', copy: 'judge' },
  { path: 'rework/submission/09_feasibility_and_registration.md', copy: 'judge' },
  { path: 'rework/submission/10_risk_and_implementation.md', copy: 'judge' },
  { path: 'rework/submission/11_mvp_situation_and_product_proposal.md', copy: 'judge' },
  { path: 'rework/submission/12_concept_survey_plan.md', copy: 'judge' },
  { path: 'rework/submission/appendix_a_tier_key.md', copy: 'judge' },
  { path: 'rework/submission/executive_summary.md', copy: 'judge' },
  { path: 'rework/proposal/00_proposal_structure.md', copy: 'team' },
  { path: 'rework/proposal/01_problem_and_pain_point.md', copy: 'team' },
  { path: 'rework/proposal/02_situation_analysis.md', copy: 'team' },
  { path: 'rework/proposal/03_background_and_trends.md', copy: 'team' },
  { path: 'rework/proposal/04_strategy.md', copy: 'team' },
  { path: 'rework/proposal/05_finance_and_project_valuation.md', copy: 'team' },
  { path: 'rework/proposal/06_kpi.md', copy: 'team' },
  { path: 'rework/proposal/07_organization_audit_and_evaluation.md', copy: 'team' },
  { path: 'rework/proposal/08_success_and_fail_case_studies.md', copy: 'team' },
  { path: 'rework/proposal/09_feasibility_and_registration.md', copy: 'team' },
  { path: 'rework/proposal/10_risk_and_implementation.md', copy: 'team' },
  { path: 'rework/proposal/11_mvp_situation_and_product_proposal.md', copy: 'team' },
  { path: 'rework/proposal/12_concept_survey_plan.md', copy: 'team' },
  { path: 'rework/proposal/appendix_a_tier_key.md', copy: 'team' },
  { path: 'rework/proposal/team_appendix_executive_summary.md', copy: 'team' },
  { path: 'rework/proposal/team_appendix_handover_rd_figures.md', copy: 'team' },
]

const COMMON = `You are working in the repo D:\\Workspace\\singha-case-study for the SINGHA Ultimate Challenge 2026 entry (Singha Lemon Soda Cube, shown as "Lemon Soda"). Today is 20 October 2026.

Sources of truth, in this order:
1. rework/deck/deck_content.md (the slide content; read it in full first).
2. rework/workflows/update_loop_state_2026-10-20.md (the confirmed decisions, the creator budget, Route A and the team settings).
3. The verification records rework/83_verify_V1_yuzu_on_sale.md, rework/83_verify_V3_line_speeds.md, rework/83_verify_V5_temperature_demand.md, rework/83_verify_V6_notification_195.md, rework/83_verify_V7_paid_datasets_and_oie.md, rework/83_verify_V4_cpall_margin.md and rework/83_verify_V2_distributor_margin.md. Read only the parts your file needs.

Facts the deck now states (check your file against these):
- Market size: NielsenIQ values are THB 70,772 million (12 months to November 2024) and THB 66,000 million (12 months to January 2024), both press relays (S). 2025 values found run from about THB 67,000 million (no source named) to THB 76,900 million (Kasikorn Research Center relayed 8 September 2025; a Marketeer forecast of 9 May 2025). None names NielsenIQ. Remove the labels "2024 press" and "2026 bottler data". The canned figure THB 13,172 million (year not stated) is context only. The Singha share "THB 1,357 million" and "10.3 percent" are not computed.
- Brand shares: Coca-Cola 51 percent, Pepsi 30 percent, est 8.6 percent by volume (press, no year, no data owner). ThaiNamthip holds 51.4 percent of Thai carbonated soft drinks in 2024 (a Frost and Sullivan estimate quoted in its filing; basis not stated).
- Singha Lemon Soda can prices: single can THB 17.00 at Lotus's Shop Online (online, 20 October 2026, S); 24-can packs THB 13.54 to 13.75 a can (pack prices SOURCED, per-can DERIVED); band THB 13.54 to 17.00 across six retail rows, median 13.75. No store shelf price was read. "Price not verified" is replaced by these online prices.
- Yuzu: Yuzu is named in the range in the press (June 2021 launch; April 2025 mentions). Yuzu is listed online at Lotus's Shop Online at THB 17 on an aggregator page stamped 20 October 2026, and Yuzu packs appear at Makro PRO and Lazada. Whether a Yuzu can can be bought in October 2026 is not confirmed. Do not write "on sale now".
- Launch: August 2020 in a company release (S); two later articles say late 2020 (S). Lemon can launch price THB 16 (2020).
- Distributor margin: no sourced Thai figure. The closest sourced value is the National Statistical Office's 2023 wholesale value-added share for non-alcoholic beverages, 16.2 percent (P, PROXY; a value-added measure, not a margin). The 10 to 20 percent band is an ASSUMPTION.
- Retailer margin: the 21.6 percent retailer margin is a group all-category proxy. CP ALL's 2025 group gross margin is 22.7 percent (P, group figure); net margin 2.8 percent (P).
- Line speeds: pre-made pouch machines range from about 15 to 80 pouches a minute as maker maxima (dry-cycle; 60 is a mid-range maker figure). The planning point is 42 pouches a minute (60 a minute at 70 percent efficiency; both assumptions); about 79 hours for 200,000 cubes. 330 mL can lines range about 100 to 300 cans a minute from a maker table (dated), with installed lines at 200 (S) and about 483 to 550 (S, company claim).
- Notification 195 (Thai mineral-salt beverages): clause 4(1.3) sets potassium at no more than 195 mg per litre where present. The text is unchanged from the Gazette original through the Thai FDA compilation of about 29 March 2023 (P). No later amending notification was found by title on the Thai FDA list to 20 October 2026 (P, negative finding). A post-March-2023 amendment inside a general notification is not excluded. The 2011 and 2020 amendments did not change clauses 3, 4(1) or 7. Whether the cube is a mineral-salt beverage under clause 3 is the Gate 1 question. The cube holds about 960 mg of potassium per litre (about 4.9 times the ceiling). Do not write "in force and unchanged" as a closed fact.
- Sucralose: 55 mg a serve, about 167 mg per kg of drink, equal in sweetness to about 10 g of sugar per 100 mL (ASSUMPTION for sweetness). 33 mg is obsolete. Limit 300 mg/kg for flavoured drinks in category 14.1.4 (P, flavoured-drink rows only).
- Binder: 0.80 g mannitol, tableting grade (INS 421), fallback isomalt. Its price is an import-value proxy of THB 0.08 to 1.27 per cube. The lemon flavour (0.05 g) is not priced.
- Sodium: no sodium salt in the recipe; sodium from the recipe 0 to about 2 mg a serve; water adds 0 to about 7 mg at the WHO typical level, or about 33 to 68 mg with the reported Thai tap-water level; no sodium-free or low-sodium claim.
- Container (20 ft): 21,386 cartons and 128,316 cubes (volume estimate at 92 percent of ONE's internal volume); payload 28.33 t. "21,431" and "128,586" are obsolete.
- Potassium: about 317 mg a serve, 9 percent of the 3,500 mg Thai reference (P); about 960 mg per litre. Medical review at Gate 2.
- Chemistry (desk model, not tasted): pH about 3.4 to 3.5 (working 3.5); dissolution about 6 minutes stirred and 11 not stirred (central, assumed inputs), 3 to 22 and 5 to 74 minutes across ranges; fizz above 0.44 g/L by surface loss about 1.7 to 3.4 hours at 20 C, about 15 minutes with bubble loss (champagne proxy); below 41 percent dissolved, under the threshold.
- Value (after excise and tax, 200,000 cubes a year, THB 500,000 fixed cost, five years, 10 percent): NPV THB 0.17 million (base); chance of a positive NPV 0.26 across the stated ranges (0.40 before excise and tax; 0.58 on a simpler structure); expected NPV minus THB 0.88 million; 90 percent range minus 3.40 to plus 1.59 million. Break-even with no cannibalisation 184,325 cubes a year (148,076 before excise). Operating break-even 127,000 cubes (fixed cost divided by contribution after excise). Cannibalisation break-even about 7.5 percent of cube buyers; review level 7 percent. Contribution THB 3.94 a cube after excise; THB 4.91 before excise on the planning price of THB 9.00. The earlier 146,230 figure is a before-excise, before-tax break-even on the older basis and is labelled as such, or removed. The 1,676 million cans and the THB 4.94 can cost are withdrawn; the can's variable cost is about THB 3.3 before aluminium (2.6 to 3.9).
- Creator and pilot budget: nine confirmed creators (four mid-tier, five mega-tier) on commission-led offers, no flat fee committed. Committed THB 24,686 (creator kits 442, commission cap 4,000, Route A 18,000, contingency 10 percent). Conditional THB 60,000 for paid social (learning tranche 20,000, scale tranche 40,000). Ceiling THB 84,686. Flat fees for the nine creators (3,489,200 for one post each) are not recommended. "5,480" and "65,480" are obsolete. Cap THB 27.38 per first purchase at a 30 percent repeat (THB 24.22 at 15 percent). Route A: 20 stores, three sampling days a store, 20 samples a day, THB 15 a sample (committed THB 18,000; range 12,000 to 30,000).
- Pilot: Route A, 20 stores, read at weeks 8 and 13: scale if both are at or above 3 units per store per week, stop if both are below, otherwise hold. Route B, paid social, starts only at a 1.0 percent non-paid click-to-first-purchase rate (assumption). Scale needs repeat of 15 percent or more in both cohorts, contribution of at least THB 3.51 per cube before excise (THB 2.54 after excise), and a cannibalisation share under 7 percent.
- Ownership and settings: gate owners are roles (executive sponsor, regulatory affairs head, R&D lead, operations director, marketing lead, finance lead, sales and channel head, brand and legal function). The twelve decisions once handed to Singha Corporation are now the team's settings, with basis, owner role and timing (deck slide 13, exhibit 6C). The only ask is the executive sponsor's signature on the Gate 0 record. Do not write that Singha Corporation decides anything.

What to do with your file:
1. Read the deck and the state file. Read your file in full.
2. Rewrite every statement in your file that conflicts with the facts above, and every obsolete figure listed above. Add a statement where the deck adds one that your file's topic needs. Keep your file's structure, headings and tier labels, and keep statements that are still correct.
3. No em dashes, en dashes or middle dots. Plain complete sentences.
4. Keep tier labels accurate (P, S, SOURCED, UNVERIFIED, DERIVED, PROXY, ASSUMPTION, COMPANY CLAIM). Never upgrade S to P.
5. Do not hand any decision to Singha Corporation. Replace "Singha Corporation decides" or "for Singha Corporation to set" with the team's setting, its basis and the owner role.
6. Do not add internal notes, verifier or reviewer language, workflow or task names, file paths under rework/, or the words "team-only" in the judge copy.
7. The team copy (rework/proposal) may keep its own team-only blocks and its file paths. Update its numbers and statements in the same way.
8. Edit only your own file. Do not change any other file. Do not commit.
9. Return a short list of the statements you changed (old to new, one line each), and any conflict you could not resolve with the sources you have.`

const RESULT = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    changes: { type: 'array', items: { type: 'string' } },
    unresolved: { type: 'array', items: { type: 'string' } },
  },
  required: ['file', 'changes', 'unresolved'],
}

const VERDICT = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail'] },
    checked: { type: 'array', items: { type: 'string' } },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['high', 'medium', 'low'] },
          where: { type: 'string' },
          problem: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['severity', 'where', 'problem', 'fix'],
      },
    },
  },
  required: ['verdict', 'checked', 'issues'],
}

const syncPrompt = (f) => `${COMMON}\n\nYour file: ${f.path} (${f.copy === 'judge' ? 'JUDGE copy: no team-only content, no file paths, no internal language' : 'TEAM copy: keep its team-only blocks and paths'}).\n\nSync it now. Return the structured result.`

const reviewPrompt = (f, result) => `${COMMON}\n\nYou are the independent reviewer for the judge file ${f.path}. You did not write the change. Read the deck (rework/deck/deck_content.md), the state file, and the file as it now stands. The author's change list is:\n${JSON.stringify(result).slice(0, 8000)}\n\nDo this: (1) check each fact in the file that the deck also states; a figure that differs from the deck is a high issue unless the file says why; (2) check for any obsolete figure listed above (5,480; 65,480; 21,431; 128,586; 4.94 as a current figure; 33 mg sucralose as current; "price not verified" for the Singha can; "Singha Corporation decides" or any decision left to Singha; any "on sale now" for Yuzu; the 2024 press or 2026 bottler labels for the market value); (3) check for leaks: the words "rework/", "team-only", "verifier", "reviewer", "workflow", "loop", "Claude", "Sonnet", "Haiku", "task", "critic", any em dash, en dash or middle dot; (4) check that no S source is tiered P and no snippet is cited as a read page. Default to fail when a figure differs from the deck and the file gives no reason. Return the verdict and each issue.`

phase('Sync')
const synced = (await parallel(FILES.map(f => () =>
  agent(syncPrompt(f), { label: `sync:${f.path.split('/').pop()}`, phase: 'Sync', schema: RESULT, model: 'sonnet' })
    .then(r => ({ f, result: r }))
))).filter(Boolean)

phase('Review')
const reviewed = (await parallel(synced.filter(x => x.f.copy === 'judge').map(x => () => {
  if (!x.result) return Promise.resolve({ f: x.f, failed: true })
  return agent(reviewPrompt(x.f, x.result), { label: `review:${x.f.path.split('/').pop()}`, phase: 'Review', schema: VERDICT, model: 'sonnet' })
    .then(v => ({ f: x.f, result: x.result, verdict: v }))
}))).filter(Boolean)

return {
  synced: synced.map(x => ({ file: x.f.path, copy: x.f.copy, failed: !x.result, changes: x.result ? x.result.changes.length : 0, unresolved: x.result ? x.result.unresolved : [] })),
  reviewed: reviewed.map(x => ({ file: x.f.path, failed: !!x.failed, review: x.verdict ? x.verdict.verdict : null, issues: x.verdict ? x.verdict.issues : [] })),
}
