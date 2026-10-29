export const meta = {
  name: 'singha-deck-remove-additions',
  description: 'Remove loop-added text, internal notes and codes from the final Canva deck; rewrite only existing text boxes; list leftovers for manual revision',
  phases: [
    { title: 'Extract', detail: 'verbatim text of the untouched original deck into baseline files' },
    { title: 'Plan', detail: 'one planner per page group lists each addition and its explicit replacement' },
    { title: 'Apply', detail: 'sequential per group: edit existing boxes, read back, commit only if clean' },
  ],
}

const A = args
// Every agent in this workflow runs on Haiku 5.5 (set 29 October 2026).
const hagent = (prompt, opts = {}) => agent(prompt, { model: 'haiku', ...opts })
const DECK = 'DAHX_hKTpDE'
const ORIG = 'DAHZUgx5WUs'
const DIR = A.scratch_dir
const READ = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__read-design'
const EDIT = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__edit-design'
const ORIG_GROUPS = [[1, 2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15, 16], [17, 18, 19, 20, 21, 22, 23]]
const DECK_GROUPS = [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13], [14, 15, 16, 17, 18, 19]]
const BASELINE = [1, 2, 3].map(n => DIR + 'baseline_part' + n + '.md')

const EXTRACT_SCHEMA = {
  type: 'object',
  properties: { file: { type: 'string' }, pages: { type: 'integer' } },
  required: ['file', 'pages'],
}

const PLAN_SCHEMA = {
  type: 'object',
  properties: {
    edits: { type: 'array', items: { type: 'object', properties: {
      page: { type: 'integer' },
      locator_id: { type: 'string' },
      op: { type: 'string', enum: ['find_replace', 'replace_text', 'delete'] },
      find: { type: 'string' },
      replace: { type: 'string' },
      reason: { type: 'string' },
    }, required: ['page', 'locator_id', 'op', 'reason'] } },
    notes: { type: 'array', items: { type: 'object', properties: {
      page: { type: 'integer' },
      text: { type: 'string' },
      reason: { type: 'string' },
    }, required: ['page', 'text', 'reason'] } },
    manual: { type: 'array', items: { type: 'object', properties: {
      page: { type: 'integer' },
      text: { type: 'string' },
      proposed_location: { type: 'string' },
      reason: { type: 'string' },
    }, required: ['page', 'text', 'proposed_location', 'reason'] } },
    summary: { type: 'string' },
  },
  required: ['edits', 'notes', 'manual', 'summary'],
}

const APPLY_SCHEMA = {
  type: 'object',
  properties: {
    committed: { type: 'boolean' },
    applied: { type: 'integer' },
    failed: { type: 'array', items: { type: 'string' } },
    leftover: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['committed', 'applied', 'failed', 'leftover', 'summary'],
}

const RULES = `RULES
Scope
- Work only on the Canva design ${DECK} (the final deck). Never open, edit or commit any other design. The original ${ORIG} is read only.
- The baseline is the original deck text in the baseline files. Any text in the final deck that the original does not contain is an addition.

What may change
- Change text only inside an existing text element of ${DECK}, with find_and_replace_text or replace_text on its locator_id. Delete an element only when its whole content is an addition and it holds no limit, stop rule, canonical number or ask.
- Never add a text element, shape, line or image. Never move, resize or restyle anything.
- Never delete a stop rule, a canonical number, the ask or a credited stated limit. If an addition holds one of these and no existing box on that page can take it, leave it on the slide, do not add a box, and list it under manual with its page, exact text and proposed location (the existing box and where in it).
- The cover text stays as in the original: the team names, degrees, universities and "Presented By Singha Ultra Smooth Team".

Wording
- Remove additions. Where a reworded sentence carries a code or an internal note, restore the original wording, or rewrite it as an explicit statement.
- Remove codes: gate numbers (for example "Gate 5", "G3"), finding IDs (for example "N13", "OPS-N1", "F4", "P15"), references to slide or page numbers, and bracketed status tags. Put each status in words: (DERIVED) becomes "calculated from the stated inputs"; (PROXY) becomes "a proxy, not a Singha figure"; (ASSUMPTION) becomes "assumed"; (UNVERIFIED) becomes "not verified"; OUT OF SCOPE becomes "not covered in this proposal"; a source tag becomes the source's name and date in words. Never upgrade a status.
- Remove internal notes: working derivations, phrases such as "team-set", "the records", "record inputs", "shown on the X page", "rule on the X page", "judges", "round", and any sentence addressed to the team.
- Use explicit statements: plain declarative sentences that state the fact, with no codes and no bracketed tags. Use only numbers and facts already on the deck or in the original. Invent nothing.
- A page may not get longer in words.
- Presenter notes: replace them with plain notes that restate only facts from the page, or set empty text when the page needs none. No codes or internal notes.

Commit rule
- Commit only when the read-back shows no added element, no code or internal note left, no text overflowing its box, no overlap, and nothing over the navigation bar. Otherwise cancel and report.`

phase('Extract')
const parts = await parallel(ORIG_GROUPS.map((g, i) => () => hagent(
  `Read the original deck ${ORIG}. Read only: do not edit or commit anything. Load tools with ToolSearch (query "select:${READ}"). Call read-design with design_id ${ORIG} and filter {"fields": ["design_content"], "page_indices": [${g.join(', ')}]}, with no transaction. Write every page to the file ${BASELINE[i]} in this layout, text verbatim (keep every line break and character; do not paraphrase or shorten):

# Original deck text, part ${i + 1}

## Page <number>
Title: <first line of the page>
<each text element on its own line, in reading order>
Presenter notes: <notes verbatim, or none>

Write the file with the Write tool (in pieces with Edit if it is long). Return the file path and the number of pages written.`,
  { label: 'baseline:' + (i + 1), phase: 'Extract', schema: EXTRACT_SCHEMA })))

phase('Plan')
const plans = await parallel(DECK_GROUPS.map((g, i) => () => hagent(
  `${RULES}

PLAN GROUP ${i + 1}: pages ${g.join(', ')} of the final deck ${DECK}. Read only.
1. ToolSearch query "select:${READ}".
2. read-design design_id ${DECK}, filter {"fields": ["design_content"], "page_indices": [${g.join(', ')}]}, no transaction. Every element comes with its locator_id, text and formatting; the presenter notes come too.
3. Read the baseline files ${BASELINE.join(' and ')} (the original deck text). Match each final page to its original page by title and content. Final page 1 is the original cover.
4. For each page compare element by element with the original. Classify each text as: kept (same as original); reworded (keep only if the new wording is an explicit statement with no code or internal note, otherwise restore the original wording); added (not in the original: delete it, or, if it carries a limit, stop rule, canonical number or ask, rewrite it in explicit words into an existing box on the same page, or list it under manual); or carries a code or internal note (rewrite the sentence in explicit words).
5. Output the edits. Copy each locator_id exactly from design_content. op find_replace: find = an exact substring copied from that element, replace = the new text. op replace_text: text = the whole new text of that element (use only when the whole element changes). op delete: only for a pure addition with no limit, stop rule, canonical number or ask. Output notes: the full replacement presenter notes for each page that has internal notes (plain and explicit; empty text if none is needed). Output manual items for anything a rule forbids you to do in place. Do not edit or commit anything.`,
  { label: 'plan:g' + (i + 1), phase: 'Plan', schema: PLAN_SCHEMA })))

phase('Apply')
const applied = []
for (let i = 0; i < DECK_GROUPS.length; i++) {
  const p = plans[i]
  if (!p) { applied.push({ group: i + 1, skipped: 'plan failed' }); continue }
  const pages = DECK_GROUPS[i].join(', ')
  const r = await hagent(
    `${RULES}

APPLY GROUP ${i + 1}: pages ${pages} of ${DECK}. Edit only this group.
Edits, in order: ${JSON.stringify(p.edits)}
Presenter notes to set (page number and text): ${JSON.stringify(p.notes)}

Steps:
1. ToolSearch query "select:${READ},${EDIT}".
2. Open ONE transaction: read-design design_id ${DECK}, open_transaction true, filter {"fields": ["design_content", "thumbnails"], "page_indices": [${pages}], "thumbnail_pages": [${pages}]}. Note each page's id from design_content.
3. For each edit call edit-design with that transaction_id, finalize keep_open and page_index = the edit's page. op find_replace uses find_and_replace_text (find_text, replace_text); op replace_text uses replace_text; op delete uses delete_element. Set notes with replace_speaker_notes, using the page id (not the index). An edit whose element is not found is skipped and listed in failed.
4. Read back the group's pages in the same transaction (design_content and thumbnails). Check every page against the commit rule. If a text overflows its box, shorten only that element's text. Make at most two fix calls.
5. finalize commit only if clean; otherwise finalize cancel. Return committed, applied (the count of edits that succeeded), failed (the edits that did not apply), leftover (any code, internal note, overflow or overlap still present, with its page), and a one-line summary.`,
    { label: 'apply:g' + (i + 1), phase: 'Apply', schema: APPLY_SCHEMA })
  applied.push({ group: i + 1, result: r })
  log('group ' + (i + 1) + ': ' + (r ? (r.committed ? 'committed' : 'not committed') + ', ' + r.applied + ' edits' : 'no result'))
}

const manual = plans.filter(Boolean).flatMap(p => p.manual || [])
return { baseline: parts, applied, manual }
