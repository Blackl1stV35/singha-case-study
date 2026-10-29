export const meta = {
  name: 'singha-deck-apply-corrected-list',
  description: 'Apply the corrected manual-revision list to the final Canva deck DAHX_hKTpDE in place; skips flagged items; commits each page group when its edits applied and nothing overflows',
  phases: [
    { title: 'Apply', detail: 'sequential per page group on Haiku: edit existing boxes from the corrected list, read back, commit if clean' },
  ],
}

const A = args
const DECK = 'DAHX_hKTpDE'
const LIST = A.list_file
const READ = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__read-design'
const EDIT = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__edit-design'
const GROUPS = [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13], [14, 15, 16, 17, 18, 19]]
// Every agent in this workflow runs on Haiku 5.5 (set 29 October 2026).
const hagent = (prompt, opts = {}) => agent(prompt, { model: 'haiku', ...opts })

const SKIP = `Do NOT apply these items; leave the original text as it is:
- p2 "Scale Route A" to "Scale One Route".
- p10 box beginning "74% chance of a negative NPV".
- p11 subtitle "Weeks from the opening record".
- p11 timeline label "8 Weeks of".
- p12 top line "Ten ladders, 1 measurement each, and a stop rule at ever ladder."
- p14 "Market and Consumer" body replacement.
- p14 "Stated limits" paragraph replacement.
- p14 "Also read 20 Oct 2026" paragraph replacement.
- p18 "Underlying assumptions are:" paragraph replacement.
- p8 "Reliability Level of Info Source" header item (the header already reads that).`

const CORRECTIONS = `Apply these corrections on top of the file:
- p9 cost label: use "6-cube carton", not "6-cube Pack".
- p18 "Lead basis" paragraph: replace with exactly this text: "Lead basis: the chance of a positive NPV is 0.26, below the pre-set bar of 0.95 (assumed); the segment lead and the simulated pilots also fall short of it."
- p4 launch sentence: delete "(S)" only.
- p8 Status column item: change only the Reliability cell words. Potassium bicarbonate, Citric acid, Cube, Net weight, Container 20 ft: "calculated from the stated inputs". Sucralose, Binder and filler, Lemon flavour, Packed unit, Carton: "assumed". Sucralose limit: "secondary source".
- Cover (page 1): delete the text element "Desk-stage proposal, October 2026". Keep "SINGHA name and lion used for this proposal only, not a licence."
- Presenter notes: set to empty text on pages 2 and 5 only. Do not change notes on any other page.`

const RULES = `RULES
- Work only on the Canva design ${DECK}. Never open or edit any other design.
- Read the corrected list in ${LIST} with the Read tool. Apply the items under the page headings for your pages, minus the SKIP list, plus the CORRECTIONS.
- Change text only inside existing text elements (find_and_replace_text or replace_text on the element's locator_id). The one allowed deletion is the cover element named in CORRECTIONS. Do not add any element, shape, line or image, and do not move, resize or restyle anything.
- Copy each find string exactly from design_content. If a find string is not found, skip that edit and report it.
- Keep every other word of the deck as it is.

${SKIP}

${CORRECTIONS}`

const APPLY_SCHEMA = {
  type: 'object',
  properties: {
    committed: { type: 'boolean' },
    applied: { type: 'integer' },
    failed: { type: 'array', items: { type: 'string' } },
    remaining_codes: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['committed', 'applied', 'failed', 'remaining_codes', 'summary'],
}

phase('Apply')
const results = []
for (let i = 0; i < GROUPS.length; i++) {
  const pages = GROUPS[i].join(', ')
  const r = await hagent(
    `${RULES}

APPLY GROUP ${i + 1}: pages ${pages} of ${DECK}.
Steps:
1. ToolSearch query "select:${READ},${EDIT}".
2. Read ${LIST} and collect the items for pages ${pages}.
3. Open ONE transaction: read-design design_id ${DECK}, open_transaction true, filter {"fields": ["design_content", "thumbnails"], "page_indices": [${pages}], "thumbnail_pages": [${pages}]}. Note each page's id and each element's locator_id from design_content.
4. Apply the items with edit-design, finalize keep_open, page_index = the item's page. Use find_and_replace_text or replace_text. For notes use replace_speaker_notes with the page id.
5. Read back the group's pages in the same transaction (design_content and thumbnails). If a text overflows its box or overlaps another element, shorten only the text you just changed. At most two fix calls.
6. finalize commit if there is no overflow and no overlap; otherwise finalize cancel. Return committed, applied (edits that succeeded), failed (items that did not apply, with the reason), remaining_codes (any code or bracketed status tag still in slide text on these pages, with its page), and a one-line summary.`,
    { label: 'apply:g' + (i + 1), phase: 'Apply', schema: APPLY_SCHEMA })
  results.push({ group: i + 1, result: r })
  log('group ' + (i + 1) + ': ' + (r ? (r.committed ? 'committed' : 'not committed') + ', ' + r.applied + ' edits' : 'no result'))
}

return { results }
