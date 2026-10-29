// Saved wrapper (28 October 2026): a layout pass on the STAGED Canva copy, then the saved fix loop.
// The fix loop (singha-deck-fix-loop.js) can only edit text; the panel keeps reporting render problems
// (overlaps, tick placement, duplicate badges, weak hierarchy) as "needs the Canva editor". This wrapper fixes
// those with position, resize and format edits first, then runs the loop on the text objections.
//
// Run: Workflow({scriptPath: '.claude/workflows/singha-deck-layout-then-loop.js', args: {
//   staging_id, protected_ids, scratch_dir, layout_tasks: [{page, label, brief}], loop_args: {...fix-loop args...} }})
//
// Boundary (CLAUDE.md section 10): no new content, no new claims. Layout edits move, resize or restyle only;
// every word on a slide stays unless a brief says otherwise.

export const meta = {
  name: 'singha-deck-layout-then-loop',
  description: 'Fix render problems on the staged Canva copy (position, resize, format), audit every page visually, then run the saved fix loop on the text objections',
  phases: [
    { title: 'Layout', detail: 'one agent per render problem, sequential on the staged copy, committed to it only' },
    { title: 'Audit', detail: 'fresh thumbnails of every page; fix leftover overlaps and clipping' },
    { title: 'Loop', detail: 'saved fix loop on the text objections' },
  ],
}

const A = args || {}
// Every agent in this workflow runs on Haiku 5.5 (set 29 October 2026).
const hagent = (prompt, opts = {}) => agent(prompt, { model: 'haiku', ...opts })
if (!A.staging_id || (!A.loop_args && !A.skip_loop)) throw new Error('args.staging_id and args.loop_args (or args.skip_loop) are required')
// Optional: args.allowed_ops overrides the edit list (for example to allow update_line_properties for line elements),
// args.audit_groups overrides the audited page groups, args.skip_loop true ends after the audit.
const OPS = A.allowed_ops || 'position_element, resize_element, format_text, layer_element, recolor_element or update_text_anchoring'
const STAGING = A.staging_id
const PROTECTED = A.protected_ids || []
const CANVA_READ = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__read-design'
const CANVA_EDIT = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__edit-design'

const LAYOUT_SCHEMA = {
  type: 'object',
  properties: {
    committed: { type: 'boolean' },
    changes: { type: 'array', items: { type: 'object', properties: { page: { type: 'integer' }, what: { type: 'string' } }, required: ['page', 'what'] } },
    residual: { type: 'array', items: { type: 'object', properties: { page: { type: 'integer' }, issue: { type: 'string' } }, required: ['page', 'issue'] } },
    words_changed: { type: 'boolean' },
  },
  required: ['committed', 'changes', 'residual', 'words_changed'],
}

const RULES = `Design ${STAGING} is the staged working copy and the ONLY design you may edit or commit to (the user has authorised committing to it). NEVER open a transaction on, edit or commit any of: ${PROTECTED.join(', ') || 'none listed'}.
Method:
1. Load tools with ToolSearch (query "select:${CANVA_READ},${CANVA_EDIT}").
2. Open ONE transaction with read-design: design_id ${STAGING}, open_transaction true, filter.fields ["design_content","page_metadata","thumbnails"], the page_indices and thumbnail_pages you need. Saved-design thumbnails without a transaction are a stale cache; only thumbnails from the transaction are fresh. Note every element's locator id, text, position and size.
3. Edit with ${OPS} only. Do NOT change any wording, number, rule or stated limit. Do NOT delete an element. Do not add content (a task may say explicitly that a split of existing text into two elements is allowed; then the words of the pieces joined must equal the original words exactly). Text elements: give only a width to resize_element (height is automatic). Keep a 16 px margin from the page edge and keep the bottom navigation bar (the strip with Introduction, Market and Competition, and so on) clear.
4. After each batch of edits read the pages back through the same transaction with fresh thumbnails. Look at the picture: overlapping text, text over a chart label or the nav bar, clipped or overflowing text, uneven spacing, a tick or label that does not sit where its meaning says. Iterate up to four times.
5. Commit with edit-design finalize "commit" (no operations in that call) only when the picture is clean for the task. If you cannot get it clean, finalize "cancel" and report what blocks it.
6. Return what you changed per page, what is still wrong, and whether any wording changed (it must be false).`

const tasks = A.layout_tasks || []
const results = []
phase('Layout')
for (const t of tasks) {
  const r = await hagent(`${RULES}

TASK (page ${t.page}): ${t.brief}`, { label: `layout:${t.label || 'p' + t.page}`, phase: 'Layout', schema: LAYOUT_SCHEMA })
  results.push({ task: t.label || 'p' + t.page, result: r })
  log(`layout ${t.label || 'p' + t.page}: ${r ? (r.committed ? 'committed' : 'not committed') : 'no result'}${r && r.residual.length ? ', ' + r.residual.length + ' residual' : ''}`)
}

phase('Audit')
const GROUPS = A.audit_groups || [[2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22]]
const audits = []
for (const g of GROUPS) {
  const r = await hagent(`${RULES}

TASK (pages ${g.join(', ')}): visual audit of these pages from fresh thumbnails in one transaction. For each page report overlapping or clipped text, text on top of a chart or the navigation bar, and a text box that overflows its panel. Fix only clear defects with position, resize or format edits, never touching wording. Another agent has just fixed these known problems, so do not undo them: page 12 text blocks over the waterfall axis labels, page 14 trading-week tick placement, the page badges, the page 16 ask hierarchy. Commit only if you made a change and the picture is clean; otherwise cancel. Return residual defects you could not fix.`,
    { label: `audit:p${g[0]}-${g[g.length - 1]}`, phase: 'Audit', schema: LAYOUT_SCHEMA })
  audits.push({ pages: g, result: r })
  log(`audit pages ${g[0]}-${g[g.length - 1]}: ${r ? r.changes.length + ' changes, ' + r.residual.length + ' residual' : 'no result'}`)
}

let loop = null
if (A.skip_loop) {
  log('loop skipped (args.skip_loop)')
} else {
  phase('Loop')
  loop = await workflow({ scriptPath: 'D:/Workspace/singha-case-study/.claude/workflows/singha-deck-fix-loop.js' }, A.loop_args)
}

return { layout: results, audit: audits, loop }
