// Saved fix loop (28 October 2026): revise a STAGED copy of the Canva deck against the nine-role panel's
// verified objections, re-judge, verify, and repeat until the panel advances the case or max_rounds is reached.
//
// Run: Workflow({scriptPath: '.claude/workflows/singha-deck-fix-loop.js', args: {...}})
// args (all absolute paths use forward slashes):
//   staging_id    required  Canva design id of the working copy. The ONLY design this loop may edit.
//   protected_ids optional  Canva design ids that must never be opened for editing (original, baselines).
//   scratch_dir   required  folder (trailing slash) for text dumps of the staged copy.
//   panel_file    optional  JSON from a previous panel run: keys "judge:<role>" and "verify:<role>".
//   page_map_note optional  text mapping the page numbers used in the objections to the working copy's pages.
//   repo          optional  records folder, default D:/Workspace/singha-case-study/rework/
//   max_rounds    optional  default 2
//   date          optional  ISO date for the log file name and text (scripts cannot read the clock)
//
// Boundary (CLAUDE.md section 10): an undergraduate student desk proposal. No overclaiming. Stated limits
// instead of invented fixes. No outside contact. No personas or marketing-plan pages (aborted 28 Oct 2026).

export const meta = {
  name: 'singha-deck-fix-loop',
  description: 'Revise a staged Canva copy of the deck against panel objections, re-judge with the nine-role panel, verify, loop until advance or max rounds',
  phases: [
    { title: 'Setup', detail: 'dump the staged copy, canonical numbers, load open objections' },
    { title: 'Spec', detail: 'four editors write exact edits per page group' },
    { title: 'Apply', detail: 'edits applied to the staged copy only, read back, committed' },
    { title: 'Check', detail: 're-dump and check edits landed, layout holds' },
    { title: 'Judge', detail: 'nine judges re-audit against the boundary' },
    { title: 'Verify', detail: 'a skeptic per judge tries to refute open objections' },
    { title: 'Record', detail: 'write the loop log into the repo' },
  ],
}

const A = args || {}
// Every agent in this workflow runs on Haiku 5.5 (set 29 October 2026).
const hagent = (prompt, opts = {}) => agent(prompt, { model: 'haiku', ...opts })
if (!A.staging_id || !A.scratch_dir) throw new Error('args.staging_id and args.scratch_dir are required')
const STAGING = A.staging_id
const PROTECTED = A.protected_ids || []
const DIR = A.scratch_dir
const REPO = A.repo || 'D:/Workspace/singha-case-study/rework/'
const MAX_ROUNDS = A.max_rounds || 2
const DATE = A.date || 'undated'
const PAGE_NOTE = A.page_map_note || ''
const CANVA_READ = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__read-design'
const CANVA_EDIT = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__edit-design'

const BOUNDARY_BASE = `BOUNDARY (user instruction, 28 Oct 2026; repo CLAUDE.md section 10). The entry is an UNDERGRADUATE STUDENT TEAM's desk-stage proposal. Work inside that boundary and never overclaim.
ALLOWED: public sources already in the repo records; the team's own arithmetic shown or traceable; stated assumptions and limits; test designs written as plans and labelled ASSUMPTION; saying what a result does NOT prove.
NOT ALLOWED: invented quotes, licences, regulatory opinions, lab results, supplier terms, prices, plant names or makers; any outside contact; any figure not traceable to deck_content.md or the records (write UNVERIFIED or drop it); an invented split of a total; handing a decision to Singha in judge-facing text (the team closes decisions or states a limit); sugar, health, function, hydration, electrolyte or fizz claims; team or member names; personas or marketing-plan pages (aborted).
PREFER a stated limit (OUT OF SCOPE, tier words as in Appendix C) to an invented fix. Keep slide text short and plain, one message per slide, no new boxes unless an edit says so.`
const BOUNDARY = BOUNDARY_BASE + (A.extra_rules ? ' ' + A.extra_rules : '')

// ------------------------------------------------------------------ schemas
const DUMP_SCHEMA = {
  type: 'object',
  properties: {
    page_count: { type: 'integer' },
    dump_path: { type: 'string' },
    pages_without_text: { type: 'array', items: { type: 'integer' } },
    page_titles: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['page_count', 'dump_path', 'page_titles'],
}
const OBJ_ITEM = {
  type: 'object',
  properties: {
    role: { type: 'string' }, id: { type: 'string' }, severity: { type: 'string' }, page: { type: 'string' },
    objection: { type: 'string' }, fix: { type: 'string' }, status: { type: 'string' }, corrected: { type: 'string' },
  },
  required: ['role', 'id', 'severity', 'page', 'objection', 'fix', 'status'],
}
const LOAD_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: OBJ_ITEM } }, required: ['items'] }
const NUMBERS_SCHEMA = {
  type: 'object',
  properties: { numbers: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, value: { type: 'string' }, source: { type: 'string' } }, required: ['name', 'value', 'source'] } } },
  required: ['numbers'],
}
const SPEC_SCHEMA = {
  type: 'object',
  properties: {
    edits: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          page: { type: 'integer' }, target: { type: 'string' }, replacement: { type: 'string' },
          kind: { type: 'string', enum: ['correct', 'rewrite', 'stated_limit', 'remove_text', 'add_box', 'move_to_notes'] },
          objection_ids: { type: 'array', items: { type: 'string' } }, reason: { type: 'string' }, boundary_note: { type: 'string' },
        },
        required: ['page', 'target', 'replacement', 'kind', 'objection_ids', 'reason'],
      },
    },
    declined: { type: 'array', items: { type: 'object', properties: { objection_ids: { type: 'array', items: { type: 'string' } }, reason: { type: 'string' } }, required: ['objection_ids', 'reason'] } },
  },
  required: ['edits', 'declined'],
}
const APPLY_SCHEMA = {
  type: 'object',
  properties: {
    applied: { type: 'array', items: { type: 'object', properties: { page: { type: 'integer' }, target: { type: 'string' }, status: { type: 'string', enum: ['applied', 'skipped', 'failed'] }, note: { type: 'string' } }, required: ['page', 'target', 'status'] } },
    committed: { type: 'boolean' },
    notes: { type: 'string' },
  },
  required: ['applied', 'committed'],
}
const CHECK_SCHEMA = {
  type: 'object',
  properties: {
    missing: { type: 'array', items: { type: 'object', properties: { page: { type: 'integer' }, target: { type: 'string' }, note: { type: 'string' } }, required: ['page', 'target'] } },
    layout_issues: { type: 'array', items: { type: 'object', properties: { page: { type: 'integer' }, issue: { type: 'string' }, suggested_fix: { type: 'string' } }, required: ['page', 'issue'] } },
    over_budget: { type: 'array', items: { type: 'object', properties: { page: { type: 'integer' }, words: { type: 'integer' }, cap: { type: 'integer' } }, required: ['page', 'words', 'cap'] } },
    ok: { type: 'boolean' },
  },
  required: ['missing', 'layout_issues', 'ok'],
}
const JUDGE_SCHEMA = {
  type: 'object',
  properties: {
    role: { type: 'string' },
    verdict: { type: 'string', enum: ['advance_to_pilot', 'revise_then_advance', 'hold', 'reject'] },
    verdict_reason: { type: 'string' },
    scores: { type: 'array', items: { type: 'object', properties: { criterion: { type: 'string' }, score: { type: 'integer' }, why: { type: 'string' } }, required: ['criterion', 'score', 'why'] } },
    prior: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, status: { type: 'string', enum: ['fixed', 'partly_fixed', 'not_fixed', 'stated_limit_accepted', 'out_of_boundary'] }, note: { type: 'string' } }, required: ['id', 'status', 'note'] } },
    new_objections: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['high', 'medium', 'low'] }, page: { type: 'string' }, objection: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'page', 'objection', 'evidence', 'fix'] } },
    would_change_my_vote: { type: 'string' },
  },
  required: ['role', 'verdict', 'verdict_reason', 'scores', 'prior', 'new_objections', 'would_change_my_vote'],
}
const VERIFY_SCHEMA = {
  type: 'object',
  properties: { checks: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, status: { type: 'string', enum: ['confirmed', 'partly', 'refuted', 'unverifiable'] }, evidence: { type: 'string' }, corrected_objection: { type: 'string' } }, required: ['id', 'status', 'evidence'] } } },
  required: ['checks'],
}

// ------------------------------------------------------------------ panel
const JUDGES = [
  { key: 'executive-strategy', title: 'Chief Executive / Chief Strategy Officer', rubric: ['strategic fit with Singha core (beer, soda, water) and portfolio logic', 'size of the prize and what passing the pilot would and would not earn', 'risk to the SINGHA brand and to the can business', 'clarity and weight of the ask', 'credibility of the team and the plan to deliver', 'innovation versus what Singha could copy'], focus: 'You decide whether this deserves management attention. Is the proof programme honest about its small size?' },
  { key: 'finance', title: 'Chief Financial Officer / Corporate Finance', rubric: ['soundness of the valuation method and the numbers behind it', 'honesty about uncertainty (the 0.26 chance of a positive NPV against the 0.95 test)', 'treatment of excise, tax, fixed cost, depreciation and cannibalisation', 'capital at risk and stage-gate economics', 'consistency of figures across pages', 'whether decision rules agree with the value model'], focus: 'Re-derive what you can and look for numbers that disagree between pages.' },
  { key: 'marketing-brand', title: 'Chief Marketing Officer / Brand Director', rubric: ['consumer insight and segment logic', 'positioning against the Singha lemon can and the white-space claim', 'cannibalisation reasoning and how the pilot measures it', 'creator and paid-social plan, brand safety and claims discipline', 'price point and pack architecture', 'whether the pilot can prove demand'], focus: 'You own the SINGHA brand. Check name, promise and claims discipline.' },
  { key: 'rnd-product', title: 'Head of R&D / Product Development', rubric: ['technical feasibility of a dissolvable, carbonating cube', 'realism of the formulation and dose', 'taste and sensory plan against the can', 'stability and pack-reaction plan', 'whether gates have a measurable pass or fail', 'honesty about modelled versus measured'], focus: 'Check the chemistry and the gate wording. A gate needs a measurable pass or fail, written as a plan.' },
  { key: 'regulatory-quality', title: 'Head of Regulatory Affairs / Quality and Food Safety', rubric: ['correct reading of Thai food law for this product class (potassium notification)', 'label, claim and advertising discipline', 'medical and consumer-safety framing', 'food safety and quality gate', 'excise classification risk', 'whether regulatory risk is stated honestly as a limit'], focus: 'You can stop a launch. Look for claim drift and any regulatory assumption stated as fact.' },
  { key: 'operations-supply', title: 'Head of Operations / Supply Chain / Procurement (with sustainability)', rubric: ['stated route to make the cube and honesty about not naming a maker', 'cost build with tier labels on each bar', 'what the budget includes and excludes', 'packaging, heat exposure and pouch waste', 'quality at scale', 'supply risk'], focus: 'A student team cannot name a maker or hold quotes; judge whether the deck states that honestly and sets a gate for it.' },
  { key: 'sales-channel', title: 'Head of Sales / Modern Trade and Channel', rubric: ['route to market and what the pilot assumes', 'pilot design: 20 stores, the 3-unit target, reads at weeks 8 and 13', 'definition of terms (unit, hold) and decision rules', 'price ladder and what is shown', 'online and creator-code mechanics', 'realism of volume per store'], focus: 'Judge whether the pilot rules are unambiguous and the sales plan is stated honestly.' },
  { key: 'legal-brand-protection', title: 'General Counsel / Brand Protection and Intellectual Property', rubric: ['use of the SINGHA name and lion on a non-alcoholic product', 'name clearance and trademark ownership stated as limits', 'advertising and influencer disclosure discipline', 'claims liability and consumer-safety exposure', 'creator terms as stated', 'survey and data-handling exposure'], focus: 'The deck must state the mark owner and alcohol-cue limits plainly. A stated limit is acceptable; a hidden one is not.' },
  { key: 'stage-presentation', title: 'Competition judge for presentation quality and internal consistency', rubric: ['story clarity and one message per slide', 'visual design and density', 'fit to 15 minutes and the order of the story, ending on the ask', 'internal consistency of numbers, labels and page references', 'honest handling of limits without sounding unsure', 'readiness for questions'], focus: 'Also view the pages: open a read-design transaction on the staged copy for thumbnails (filter.fields ["thumbnails"], thumbnail_pages in batches of five) and cancel it afterwards without committing. List every inconsistency between pages.' },
]

// ------------------------------------------------------------------ helpers
function readDeck(file, label) {
  return hagent(`You are a read-only copier of a Canva design into a text file. Design id: ${STAGING} (the staged working copy).
First load the Canva tool with ToolSearch (query: "select:${CANVA_READ}"). Call read-design with filter.fields ["design_metadata"] for the page count. Then for EACH page, one page per call, call read-design with filter.fields ["design_content","presenter_notes"], filter.page_indices [N], and NO transaction. Do not edit, copy, comment on, export or create anything.
Write the file ${DIR}${file} with the Write tool: a header (design id, page count, last-modified time) then for every page "## Page N" followed by the page text VERBATIM as returned (keep numbers, typos and order), then "Presenter notes:" with the notes or "none"; "(no text layer)" when a page has no text. Write the file once at the end so no page is lost.
Return page_count, dump_path (${DIR}${file}), pages_without_text, page_titles (first heading per page, 'none' if none) and notes (anything odd).`,
    { label, phase: 'Setup', schema: DUMP_SCHEMA })
}

function priorFor(items, role) { return items.filter(i => i.role === role) }

const state = { items: [], rounds: [], dump: null, numbers: [] }

// ------------------------------------------------------------------ setup
phase('Setup')
const [dump0, nums, loaded] = await parallel([
  () => readDeck('staged_r0_dump.md', 'dump:r0'),
  () => hagent(`Build the canonical numbers sheet for a deck. Read ${REPO}deck/deck_content.md in full and, where a figure needs its source, ${REPO}75_value_accrual_model.md, ${REPO}77_smc_valuation_significance.md and ${REPO}70_singha_internal_estimates.md (grep first, keep tool output small).
Return every headline figure that appears on more than one slide with its exact canonical value and a source (file and line or section): contribution per cube after and before excise; NPV after excise and tax and before excise; probabilities of a positive NPV on bases A, B and D; pilot committed budget, conditional paid social, ceiling; break-even cubes with and without cannibalisation; cannibalisation break-even share and the review level; units per store per week floor and the zero-expected-NPV units on bases A, B and D; Singha Corporation 2025 net profit and the 0.005% scale note; cube mass, packed mass, potassium per serve and per litre and the Notification 195 ceiling; fixed cost and the fixed-cost ceiling at which NPV stays positive; Gate numbers and stop rules. Use only what the files say; if two files disagree, give both and say which the deck_content file uses.`,
    { label: 'numbers', phase: 'Setup', schema: NUMBERS_SCHEMA }),
  () => A.items_file
    ? hagent(`Read the JSON file ${A.items_file}; it holds an object with an items array. Return exactly those items, unchanged.`, { label: 'load-items', phase: 'Setup', schema: LOAD_SCHEMA })
    : A.panel_file
    ? hagent(`Read the JSON file ${A.panel_file}. Keys "judge:<role>" hold a judge result (verdict, objections with id, severity, page, objection, evidence, fix); keys "verify:<role>" hold a skeptic's checks (id, status confirmed|partly|refuted|unverifiable, evidence, corrected_objection). For every judge, take each objection with severity high or medium, join it to the verifier check with the same id (status "not_verified" if none), DROP those whose status is refuted, and return the rest as items {role (the key suffix), id, severity, page, objection, fix, status, corrected (the verifier's corrected_objection or '')}. Keep the text of objection and fix complete but do not add anything. Note: ids repeat across roles (O1, O2...), so keep role with every item.`,
      { label: 'load-objections', phase: 'Setup', schema: LOAD_SCHEMA })
    : Promise.resolve({ items: [] }),
])
if (!dump0) throw new Error('could not dump the staged copy')
state.dump = dump0
state.numbers = (nums && nums.numbers) || []
state.items = (loaded && loaded.items) || []
log(`staged copy ${STAGING}: ${dump0.page_count} pages; ${state.numbers.length} canonical numbers; ${state.items.length} open objections loaded`)

// ------------------------------------------------------------------ rounds
let advanced = false
for (let round = 1; round <= MAX_ROUNDS; round++) {
  log(`ROUND ${round}: ${state.items.length} open objections`)
  const pc = state.dump.page_count
  const q = Math.ceil(pc / 4)
  const groups = [0, 1, 2, 3].map(g => ({ from: g * q + 1, to: Math.min(pc, (g + 1) * q) })).filter(g => g.from <= pc)

  // ---- Spec
  phase('Spec')
  const specs = (await parallel(groups.map(g => () =>
    hagent(`You are an editor revising slide text on pages ${g.from} to ${g.to} (inclusive) of the staged deck, using the dump ${state.dump.dump_path} (verbatim text, "## Page N" sections; the dump's page numbers are the working copy's). ${PAGE_NOTE ? 'PAGE NUMBERS IN OBJECTIONS: ' + PAGE_NOTE : ''}
${BOUNDARY}
Read the dump in full (all pages, so you see cross-page numbers), then write exact edits ONLY for pages ${g.from} to ${g.to}. For each edit give: page; target (an exact substring that exists in that page's text, at most 140 characters, copied from the dump; for kind add_box use a short description of the free area instead); replacement (the new wording); kind; objection_ids (as role:id, for example finance:O1); reason; boundary_note.
Use the canonical numbers below and no others; where a page shows a different figure, correct it to the canonical one. Where an objection asks for something outside the boundary (outside contact, quotes, a named maker, a written opinion), do NOT invent it: either write a short stated limit (kind stated_limit, for example "Maker: not named (OUT OF SCOPE); Gate 6 names the plant") or list the objection in declined with the reason.
Kind move_to_notes: target is text to DELETE from the slide (exact substring) and replacement is the wording to APPEND to that page's presenter notes (short, traceable); use it to cut slide density without losing the defence.
Keep each replacement within about 115% of the target's length unless the box is clearly larger; prefer deleting words to adding. At most two add_box edits per page. Open the backup records in ${REPO} only to check a fact (grep first). Do not edit any file.
CANONICAL NUMBERS: ${JSON.stringify(state.numbers)}
OPEN OBJECTIONS (JSON; fix texts are suggestions from the judges and may exceed the boundary): ${JSON.stringify(state.items)}`,
      { label: `spec:p${g.from}-${g.to}`, phase: 'Spec', schema: SPEC_SCHEMA })))).filter(Boolean)
  const edits = specs.flatMap(s => s.edits)
  const declined = specs.flatMap(s => s.declined)
  log(`round ${round}: ${edits.length} edits specified, ${declined.length} declined`)

  // ---- Apply (sequential; one transaction at a time on the staged copy)
  phase('Apply')
  const applied = []
  for (const g of groups) {
    const mine = edits.filter(e => e.page >= g.from && e.page <= g.to)
    if (!mine.length) continue
    const r = await hagent(`You apply text edits to ONE Canva design: ${STAGING} (the staged working copy). The user has authorised committing to ${STAGING} only. NEVER open a transaction on, edit or commit any other design, in particular not: ${PROTECTED.join(', ') || 'none listed'}.
Protocol:
1. Load tools with ToolSearch (query "select:${CANVA_READ},${CANVA_EDIT}").
2. Open ONE transaction: read-design design_id ${STAGING}, open_transaction true, filter.fields ["design_content","page_metadata","presenter_notes"], filter.page_indices [pages ${g.from} to ${g.to}]. Note transaction_id and each element's locator id and text. Later reads of other pages use the same transaction_id.
3. For each edit below find the element whose text contains the target. Use find_and_replace_text (locator_id, exact find_text, replace_text) to change just that wording. Use replace_text for a whole element only if you restate the whole new text with unchanged parts verbatim. Text layers can merge elements: edit only the substring. If the target is not found, mark skipped; do not guess another element. For kind move_to_notes: delete the target from the slide with find_and_replace_text (replace_text empty), read the page's existing presenter notes, then set the notes to the existing notes plus a new line plus the replacement with replace_speaker_notes (page_id from page_metadata; at most 5000 characters). Do not add boxes unless the edit's kind is add_box (then add_text in a free area, width set, small plain text matching nearby text size, no overlap).
4. Keep text within its box: after applying, read the pages back through the transaction (design_content and thumbnails) and confirm each edit; shorten any replacement that overflows or collides, and re-check.
5. Commit with edit-design finalize "commit" (no operations in that call) only after the read-back confirms the edits and no overflow. If it does not, finalize "cancel" and return the failures.
6. Return one entry per edit (applied, skipped or failed, with a short note) and whether you committed.
EDITS (JSON): ${JSON.stringify(mine)}`,
      { label: `apply:p${g.from}-${g.to}`, phase: 'Apply', schema: APPLY_SCHEMA })
    if (r) applied.push(...r.applied)
  }
  const nApplied = applied.filter(a => a.status === 'applied').length
  log(`round ${round}: ${nApplied} of ${edits.length} edits applied`)

  // ---- Check
  phase('Check')
  state.dump = (await readDeck(`staged_r${round}_dump.md`, `dump:r${round}`)) || state.dump
  const check = await hagent(`Check a staged Canva deck (${STAGING}) after edits. Read the new dump ${state.dump.dump_path}. Intended edits (JSON, with status from the apply step): ${JSON.stringify(edits.map(e => ({ page: e.page, target: e.target, replacement: e.replacement, kind: e.kind, status: (applied.find(a => a.page === e.page && a.target === e.target) || {}).status })))}.
1. Text check: for each intended edit, does the replacement text now appear on that page (and the old target not)? List any missing.
2. Layout check: open a read-design transaction on ${STAGING} (open_transaction true, filter.fields ["thumbnails"], thumbnail_pages = the pages that were edited, in batches of five; load the tool with ToolSearch "select:${CANVA_READ}") and LOOK at each thumbnail for text that overflows its box, collides with other text or is cut off. Then CANCEL the transaction with edit-design finalize "cancel" (load "select:${CANVA_EDIT}"); never commit. Note the saved-design thumbnails may be a stale cache; use the transaction view.
3. Density check (only if word caps are given: ${JSON.stringify(A.word_caps || null)}): run Bash with python over the new dump to count words per page, excluding each page's 'Presenter notes:' line and what follows it inside that page section. Main pages are 2 to word_caps.main_to and use main_max; pages 1 and 3 and the closing page word_caps.closing_page use cover_max; appendix pages use appendix_max. Report pages over their cap in over_budget (page, words, cap).
Return missing, layout_issues (page, issue, suggested_fix), over_budget and ok (true only if nothing is missing, no layout issue and nothing is over budget).`,
    { label: `check:r${round}`, phase: 'Check', schema: CHECK_SCHEMA })
  if (check && !check.ok && (check.missing.length || check.layout_issues.length || (check.over_budget || []).length)) {
    const fixes = [...check.missing.map(m => ({ page: m.page, kind: 'redo', target: m.target, note: m.note })), ...check.layout_issues.map(l => ({ page: l.page, kind: 'layout', issue: l.issue, suggested_fix: l.suggested_fix })), ...(check.over_budget || []).map(o => ({ page: o.page, kind: 'trim', words: o.words, cap: o.cap }))]
    await hagent(`Fix-up on the staged Canva design ${STAGING} only (committing to it is authorised; never touch ${PROTECTED.join(', ') || 'any other design'}). Load tools with ToolSearch (query "select:${CANVA_READ},${CANVA_EDIT}"). Open one transaction (read-design open_transaction true on the pages involved), repair each item (redo = reapply the missing edit from the spec if its target can now be found, shortening it; layout = shorten the text or resize the text box width so it fits; trim = cut the page to its word cap by deleting repeated wording or by move_to_notes: delete from the slide and append to the presenter notes), read back with thumbnails, then commit only if clean, else cancel. Stay inside the boundary: ${BOUNDARY}
Items (JSON): ${JSON.stringify(fixes)}
Intended edits for reference (JSON): ${JSON.stringify(edits.filter(e => fixes.some(f => f.page === e.page)))}`,
      { label: `fixup:r${round}`, phase: 'Check', schema: APPLY_SCHEMA })
    state.dump = (await readDeck(`staged_r${round}b_dump.md`, `dump:r${round}b`)) || state.dump
  }

  // ---- Judge and Verify
  phase('Judge')
  const results = await pipeline(
    JUDGES,
    j => hagent(`You are the ${j.title} on a Singha judging panel, re-auditing a revised competition deck.
The case: an undergraduate student team's entry in the SINGHA Ultimate Challenge 2026: Singha Lemon Soda Cube, one dissolvable lemon cube in 330 ml of water, a gated proof programme (pilot ceiling THB 84,686), presented in 15 minutes to Singha executives.
${BOUNDARY}
CALIBRATION: judge this as an undergraduate desk-stage proposal. Penalise overclaiming, inconsistency, unclear rules and hidden limits. Do NOT penalise the absence of work that needs outside contact or professional resources (quotes, written opinions, a named maker, lab results) when the deck states the limit honestly and sets a gate for it; mark such prior objections stated_limit_accepted (if the limit is now stated) or out_of_boundary (if you agree it cannot be asked of students).
READ the revised deck: ${state.dump.dump_path} (verbatim, "## Page N" sections, ${state.dump.page_count} pages). Backup records are in ${REPO}; open them only to test a doubt. Verify any outside fact with WebSearch or WebFetch (at most four lookups) or label it UNVERIFIED. Presenter notes are backup for questions: slide text is what the audience sees, and an answer found only in the notes counts as question-ready, not as on-slide disclosure. Read-only; edit nothing.
YOUR PRIOR OBJECTIONS (JSON; page numbers refer to the earlier numbering${PAGE_NOTE ? ': ' + PAGE_NOTE : ''}): ${JSON.stringify(priorFor(state.items, j.key))}
TASKS: (1) For each prior objection id return prior status fixed, partly_fixed, not_fixed, stated_limit_accepted or out_of_boundary with a one-line note quoting the page text that settles it. (2) Raise at most 4 NEW objections that are real, within the boundary and not already listed, with page, evidence and a boundary-safe fix. (3) Re-score your rubric 1 to 10 (7 = fund the pilot with conditions; 9 = outstanding): ${j.rubric.map((r, i) => (i + 1) + '. ' + r).join(' ')}. (4) Verdict: advance_to_pilot only if you would put your name to the deck as an undergraduate entry.
Lens: ${j.focus}`,
      { label: `judge:${j.key}:r${round}`, phase: 'Judge', schema: JUDGE_SCHEMA }),
    (res, j) => {
      const open = [
        ...(res.prior || []).filter(p => p.status === 'not_fixed' || p.status === 'partly_fixed').map(p => {
          const o = priorFor(state.items, j.key).find(i => i.id === p.id) || {}
          return { id: p.id, severity: o.severity || 'medium', page: o.page || '', objection: (o.corrected || o.objection || '') + ' [judge note: ' + p.note + ']' }
        }),
        ...(res.new_objections || []).filter(n => n.severity !== 'low'),
      ]
      if (!open.length) return { checks: [], _open: [], _judge: res }
      return hagent(`You are a skeptical verifier. A Singha department judge (${j.title}) re-audited a revised student deck and says these objections remain or are new. Try to REFUTE each against the actual deck text in ${state.dump.dump_path} (verbatim) before it is reported: an objection the deck already answers, or one that asks for work beyond an undergraduate desk proposal, must not survive. Backup records are in ${REPO} (grep first); you may use WebSearch (at most three lookups). Read-only.
${BOUNDARY}
Return per objection: confirmed (the deck really has this defect and it can be fixed within the boundary), partly (true but overstated or partly answered; give the corrected objection), refuted (answered in the deck or outside the boundary; quote), unverifiable.
OBJECTIONS (JSON): ${JSON.stringify(open)}`,
        { label: `verify:${j.key}:r${round}`, phase: 'Verify', schema: VERIFY_SCHEMA }).then(v => ({ ...(v || { checks: [] }), _open: open, _judge: res }))
    },
  )

  // ---- Decide
  const scoreRows = []
  const nextItems = []
  results.forEach((r, i) => {
    const j = JUDGES[i]
    const checks = (r && r.checks) || []
    const openList = (r && r._open) || []
    const jd = (r && r._judge) || {}
    const sc = (jd.scores || []).map(s => s.score)
    scoreRows.push({ role: j.key, verdict: jd.verdict || 'none', mean: sc.length ? Math.round(sc.reduce((a, b) => a + b, 0) / sc.length * 10) / 10 : null })
    openList.forEach(o => {
      const c = checks.find(x => x.id === o.id)
      const status = c ? c.status : 'not_verified'
      if (status === 'refuted') return
      nextItems.push({ role: j.key, id: o.id, severity: o.severity, page: o.page, objection: o.objection, fix: '', status, corrected: (c && c.corrected_objection) || '' })
    })
    scoreRows[scoreRows.length - 1].open_after_verify = openList.filter(o => { const c = checks.find(x => x.id === o.id); return !c || c.status !== 'refuted' }).length
  })
  const advanceCount = scoreRows.filter(s => s.verdict === 'advance_to_pilot').length
  const means = scoreRows.map(s => s.mean).filter(m => m !== null)
  const meanAll = means.length ? Math.round(means.reduce((a, b) => a + b, 0) / means.length * 10) / 10 : null
  state.rounds.push({ round, edits: edits.length, applied: nApplied, declined: declined.length, advance_votes: advanceCount, mean_score: meanAll, open_after_verify: nextItems.length, per_judge: scoreRows })
  log(`round ${round}: ${advanceCount} of ${JUDGES.length} judges advance; mean ${meanAll}; ${nextItems.length} objections still open after verification`)
  state.items = nextItems
  // Advance rule: at least 7 of 9 judges say advance_to_pilot and no verified high-severity objection is left.
  const highOpen = nextItems.filter(i => i.severity === 'high' && i.status !== 'unverifiable').length
  if (advanceCount >= 7 && highOpen === 0) { advanced = true; break }
}

// ------------------------------------------------------------------ record
phase('Record')
await hagent(`Write the loop log ${REPO}workflows/deck_fix_loop_log_${DATE}.md with the Write tool. No team or member names, no Canva edit links. Content: a title; the date ${DATE}; that the loop edited only a staged Canva copy and left the original and the baselines untouched; the boundary rule in two lines; per round: edits specified, applied, declined, objections still open after verification; the final status (${advanced ? 'ADVANCED: at least 7 of 9 judges advance and no verified high objection remains' : 'NOT ADVANCED: the advance rule (7 of 9 judges and no verified high objection) was not met'}); and the list of objections still open (role, id, severity, page, objection) from this JSON: ${JSON.stringify(state.items)}. Round summary JSON: ${JSON.stringify(state.rounds)}. Keep it under 60 lines and plain.`,
  { label: 'record-log', phase: 'Record' })

return { staging_id: STAGING, advanced, rounds: state.rounds, open_items: state.items, final_dump: state.dump && state.dump.dump_path }
