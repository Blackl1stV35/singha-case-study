export const meta = {
  name: 'update-loop-resolve',
  description: 'Resolve the open items on all 30 submission and proposal files against the updated deck, then re-check the judge files',
  whenToUse: 'Run after update-loop-sync. Reads rework/workflows/update_loop_resolve_2026-10-20.md for the findings. Edits judge files only.',
  phases: [
    { title: 'Fix', detail: 'one agent per judge file fixes its high and medium findings' },
    { title: 'Review', detail: 'a fresh reviewer re-checks each fixed file' },
  ],
}

const FILES = [
  'rework/submission/01_problem_and_pain_point.md',
  'rework/submission/02_situation_analysis.md',
  'rework/submission/03_background_and_trends.md',
  'rework/submission/04_strategy.md',
  'rework/submission/05_finance_and_project_valuation.md',
  'rework/submission/06_kpi.md',
  'rework/submission/07_organization_audit_and_evaluation.md',
  'rework/submission/08_success_and_fail_case_studies.md',
  'rework/submission/09_feasibility_and_registration.md',
  'rework/submission/10_risk_and_implementation.md',
  'rework/submission/11_mvp_situation_and_product_proposal.md',
  'rework/submission/12_concept_survey_plan.md',
  'rework/submission/appendix_a_tier_key.md',
  'rework/submission/executive_summary.md',
  'rework/proposal/00_proposal_structure.md',
  'rework/proposal/01_problem_and_pain_point.md',
  'rework/proposal/02_situation_analysis.md',
  'rework/proposal/03_background_and_trends.md',
  'rework/proposal/04_strategy.md',
  'rework/proposal/05_finance_and_project_valuation.md',
  'rework/proposal/06_kpi.md',
  'rework/proposal/07_organization_audit_and_evaluation.md',
  'rework/proposal/08_success_and_fail_case_studies.md',
  'rework/proposal/09_feasibility_and_registration.md',
  'rework/proposal/10_risk_and_implementation.md',
  'rework/proposal/11_mvp_situation_and_product_proposal.md',
  'rework/proposal/12_concept_survey_plan.md',
  'rework/proposal/appendix_a_tier_key.md',
  'rework/proposal/team_appendix_executive_summary.md',
  'rework/proposal/team_appendix_handover_rd_figures.md',
]

const COMMON = `You are working in the repo D:\\Workspace\\singha-case-study for the SINGHA Ultimate Challenge 2026 entry (Singha Lemon Soda Cube, shown as "Lemon Soda"). Today is 20 October 2026.

Sources of truth: rework/deck/deck_content.md (the slide content, which is the source of truth), rework/workflows/update_loop_state_2026-10-20.md (the confirmed decisions), and the verification records under rework/83_verify_*.md.

Rules for every file:
- No em dashes, en dashes or middle dots. Plain complete sentences.
- No team-only text, no file paths under rework/, no reviewer or workflow language, no internal notes.
- No decision handed to Singha Corporation: state the team's setting, its basis and the owner role instead.
- Keep tier labels accurate. Never upgrade S to P. Never give a snippet a read-page tier.
- Edit only the one file you are given. Do not edit the deck or any other file.`

const FIX_RESULT = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    fixed: { type: 'array', items: { type: 'string' } },
    not_fixed: { type: 'array', items: { type: 'string' } },
  },
  required: ['file', 'fixed', 'not_fixed'],
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
          problem: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['severity', 'problem', 'fix'],
      },
    },
  },
  required: ['verdict', 'checked', 'issues'],
}

const fixPrompt = (path) => `${COMMON}

Your file: ${path}

Read rework/workflows/update_loop_resolve_2026-10-20.md and find the section for this file (its heading names the file). Apply the standard resolutions R1 to R9 wherever they occur in your file, and fix every finding marked high or medium in that section, in this file only. For low findings, fix only the ones that take one edit. Where a finding depends on a deck-level decision (for example the basis of the cube mass or the tier of a company page), keep the deck's figure, state the basis in the file as a stated limit, and list it under not_fixed with the reason. Read the deck section that each fix uses before you edit. Return the list of what you fixed and what you did not, with the reason.`

const checkPrompt = (path, result) => `${COMMON}

You are the independent reviewer for ${path}. You did not write the fixes. Read the file as it now stands, the deck, and the findings section for this file in rework/workflows/update_loop_resolve_2026-10-20.md. The fixing agent reported:
${JSON.stringify(result).slice(0, 6000)}

Do this: (1) check that each high and medium finding in the section is closed, or is listed under not_fixed with a reason that holds; (2) check each figure the file states against the deck, and flag any difference the file does not explain; (3) scan the file for leaks: "rework/", "team-only", "verifier", "reviewer", "workflow", "loop", "Claude", "Sonnet", "Haiku", em dashes, en dashes, middle dots; (4) check no S source is tiered P and no snippet is cited as a read page. Default to fail when a high or medium finding is open with no reason. Return the verdict and each issue.`

phase('Fix')
const fixed = (await parallel(FILES.map(path => () =>
  agent(fixPrompt(path), { label: `fix:${path.split('/').pop()}`, phase: 'Fix', schema: FIX_RESULT, model: 'sonnet' })
    .then(r => ({ path, result: r }))
))).filter(Boolean)

phase('Review')
const checked = (await parallel(fixed.filter(x => x.path.includes('/submission/')).map(x => () => {
  if (!x.result) return Promise.resolve({ path: x.path, failed: true })
  return agent(checkPrompt(x.path, x.result), { label: `check:${x.path.split('/').pop()}`, phase: 'Review', schema: VERDICT, model: 'sonnet' })
    .then(v => ({ path: x.path, result: x.result, verdict: v }))
}))).filter(Boolean)

return checked.map(c => ({
  file: c.path,
  failed: !!c.failed,
  fixed: c.result ? c.result.fixed.length : 0,
  not_fixed: c.result ? c.result.not_fixed : [],
  review: c.verdict ? c.verdict.verdict : null,
  issues: c.verdict ? c.verdict.issues : [],
}))
