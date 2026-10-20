export const meta = {
  name: 'update-loop-fix2',
  description: 'Second pass: fix the open medium findings on the judge files that still failed re-review, then re-check them',
  whenToUse: 'Run after update-loop-sync. Reads rework/workflows/update_loop_fix2_review_2026-10-20.md for the findings. Edits judge files only.',
  phases: [
    { title: 'Fix', detail: 'one agent per judge file fixes its high and medium findings' },
    { title: 'Review', detail: 'a fresh reviewer re-checks each fixed file' },
  ],
}

const FILES = [
  'rework/submission/01_problem_and_pain_point.md',
  'rework/submission/02_situation_analysis.md',
  'rework/submission/05_finance_and_project_valuation.md',
  'rework/submission/07_organization_audit_and_evaluation.md',
  'rework/submission/09_feasibility_and_registration.md',
  'rework/submission/10_risk_and_implementation.md',
  'rework/submission/appendix_a_tier_key.md',
]

const COMMON = `You are working in the repo D:\\Workspace\\singha-case-study for the SINGHA Ultimate Challenge 2026 entry (Singha Lemon Soda Cube, shown as "Lemon Soda"). Today is 20 October 2026.

Sources of truth: rework/deck/deck_content.md (the slide content, which is the source of truth), rework/workflows/update_loop_state_2026-10-20.md (the confirmed decisions), and the verification records under rework/83_verify_*.md.

Rules for the judge copy (rework/submission):
- No em dashes, en dashes or middle dots. Plain complete sentences.
- No team-only text, no file paths under rework/, no reviewer or workflow language, no internal notes.
- No decision handed to Singha Corporation: state the team's setting, its basis and the owner role instead.
- Keep tier labels accurate. Never upgrade S to P. Never give a snippet a read-page tier.
- Edit only the one judge file you are given. Do not edit the deck, the team copy, or any other file.`

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

Read rework/workflows/update_loop_fix2_review_2026-10-20.md and find the section for this file (its heading names the file). Fix every finding marked high or medium in that section, in the judge file only. For low findings, fix only the ones that take one edit. Where a finding depends on a deck-level decision (for example the basis of the cube mass or the tier of a company page), keep the deck's figure, state the basis in the file as a stated limit, and list it under not_fixed with the reason. Read the deck section that each fix uses before you edit. Return the list of what you fixed and what you did not, with the reason.`

const checkPrompt = (path, result) => `${COMMON}

You are the independent reviewer for ${path}. You did not write the fixes. Read the file as it now stands, the deck, and the findings section for this file in rework/workflows/update_loop_fix2_review_2026-10-20.md. The fixing agent reported:
${JSON.stringify(result).slice(0, 6000)}

Do this: (1) check that each high and medium finding in the section is closed, or is listed under not_fixed with a reason that holds; (2) check each figure the file states against the deck, and flag any difference the file does not explain; (3) scan the file for leaks: "rework/", "team-only", "verifier", "reviewer", "workflow", "loop", "Claude", "Sonnet", "Haiku", em dashes, en dashes, middle dots; (4) check no S source is tiered P and no snippet is cited as a read page. Default to fail when a high or medium finding is open with no reason. Return the verdict and each issue.`

phase('Fix')
const fixed = (await parallel(FILES.map(path => () =>
  agent(fixPrompt(path), { label: `fix:${path.split('/').pop()}`, phase: 'Fix', schema: FIX_RESULT, model: 'sonnet' })
    .then(r => ({ path, result: r }))
))).filter(Boolean)

phase('Review')
const checked = (await parallel(fixed.map(x => () => {
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
