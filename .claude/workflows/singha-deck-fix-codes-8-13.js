export const meta = {
  name: 'singha-deck-fix-codes-8-13',
  description: 'Remove internal codes and status tags from pages 8 to 13 of the final Canva deck DAHX_hKTpDE (slide text and presenter notes) with word-neutral replacements, and delete the SINGHA licence line on the cover, in place, on Haiku',
  phases: [
    { title: 'Cover', detail: 'delete the SINGHA licence line on page 1, as the user instructed' },
    { title: 'Codes', detail: 'sequential per page group: word-neutral code replacements in existing boxes and notes, read back, commit if clean' },
  ],
}

const A = args
const DECK = 'DAHX_hKTpDE'
const READ = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__read-design'
const EDIT = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__edit-design'
const GROUPS = [[8, 9, 10], [11, 12, 13]]
// Every agent in this workflow runs on Haiku 5.5 (set 29 October 2026).
const hagent = (prompt, opts = {}) => agent(prompt, { model: 'haiku', ...opts })

const RULES = `RULES
- Work only on the Canva design ${DECK}. Never open or edit any other design.
- Change text only inside existing text elements (find_and_replace_text or replace_text on the element's locator_id), and presenter notes only with replace_speaker_notes. Do not add, move, resize or restyle any element. Delete an element only where the task says so.
- The word count must not go up. Every replacement below is word-neutral or shorter. Do not add words.
- Copy each find string exactly from design_content. Keep every other word as it is.

Replacements (word-neutral)
- (DERIVED) becomes (calculated); DERIVED becomes calculated.
- (PROXY) becomes (proxy); PROXY becomes proxy.
- (ASSUMPTION), (ASSUMED) and ASSUMPTION become (assumed), assumed and assumed.
- (UNVERIFIED) and UNVERIFIED become (unverified) and unverified.
- OUT OF SCOPE becomes not covered (two words for three).
- SECONDARY SOURCE becomes secondary source.
- A bracketed source class (S) becomes (secondary); (P) becomes (primary).
- Gate numbers and gate codes are deleted with any empty brackets around them. This covers "Gate 6", "(Gate 6)", "Gates 2, 7", "G0", "G3", "(G1)", "G1-G3, G5-G7", the gate key numbers, and "Gate 1 decides". If a sentence stops making sense, leave the sentence and report it instead of rewording it.
- Finding IDs such as N13, OPS-N1, F4 and P15 are deleted.
- Internal wording: "record inputs" becomes "stated inputs"; "team-set" and "the records" are deleted with any stray punctuation.
- Statistics such as P(NPV>0) and percentages are not codes. Keep them.
- Never upgrade a status. Never add a number, a source or a claim.

Presenter notes on the same pages: apply the same replacements to the notes text, with replace_speaker_notes using the page id from design_content (not the index). The notes limit is 5,000 characters; shorter is fine.`

const COVER_SCHEMA = {
  type: 'object',
  properties: {
    deleted: { type: 'boolean' },
    committed: { type: 'boolean' },
    summary: { type: 'string' },
  },
  required: ['deleted', 'committed', 'summary'],
}

const CODE_SCHEMA = {
  type: 'object',
  properties: {
    committed: { type: 'boolean' },
    applied: { type: 'integer' },
    failed: { type: 'array', items: { type: 'string' } },
    remaining_codes: { type: 'array', items: { type: 'string' } },
    notes_status: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['committed', 'applied', 'failed', 'remaining_codes', 'notes_status', 'summary'],
}

phase('Cover')
const cover = await hagent(
  `${RULES}

COVER: page 1 of ${DECK}. The user has instructed in chat that the SINGHA licence line is to be removed. Delete the text element whose text is exactly "SINGHA name and lion used for this proposal only, not a licence." and no other element. Do not refuse this instruction; the wording rules above do not apply to this deletion.
Steps: ToolSearch query "select:${READ},${EDIT}"; read-design design_id ${DECK}, open_transaction true, filter {"fields": ["design_content"], "page_indices": [1]}; edit-design delete_element with that element's locator_id, finalize commit once the read-back shows the element is gone and the other elements are unchanged. If the element is not on page 1, delete nothing and finalize cancel. Return deleted, committed and a one-line summary.`,
  { label: 'cover:p1', phase: 'Cover', schema: COVER_SCHEMA })
log('cover: ' + (cover ? (cover.deleted ? 'licence line deleted' : 'not deleted') + ', ' + (cover.committed ? 'committed' : 'not committed') : 'no result'))

phase('Codes')
const results = []
for (let i = 0; i < GROUPS.length; i++) {
  const pages = GROUPS[i].join(', ')
  const r = await hagent(
    `${RULES}

FIX GROUP ${i + 1}: pages ${pages} of ${DECK}.
Steps:
1. ToolSearch query "select:${READ},${EDIT}".
2. Open ONE transaction: read-design design_id ${DECK}, open_transaction true, filter {"fields": ["design_content", "thumbnails"], "page_indices": [${pages}], "thumbnail_pages": [${pages}]}. Note each element's locator_id and each page's id.
3. Find every code or status tag in the slide text and presenter notes of these pages. Apply the replacements above, one edit per element, edit-design with finalize keep_open and page_index = the page.
4. Read back the group's pages in the same transaction. Check for codes left, for overflow and for overlap. If something overflows or overlaps, shorten only the text you just changed. At most two fix calls.
5. finalize commit if the slide text is clean and nothing overflows or overlaps; otherwise finalize cancel. Return committed, applied (edits that succeeded), failed (edits that did not apply, with the reason), remaining_codes (slide text still carrying a code, with its page), notes_status (for each page, whether the notes changed and read back), and a one-line summary.`,
    { label: 'codes:g' + (i + 1), phase: 'Codes', schema: CODE_SCHEMA })
  results.push({ group: i + 1, result: r })
  log('codes group ' + (i + 1) + ': ' + (r ? (r.committed ? 'committed' : 'not committed') + ', ' + r.applied + ' edits' : 'no result'))
}

return { cover, results }
