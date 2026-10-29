export const meta = {
  name: 'singha-deck-explicit-names-8-13',
  description: 'On pages 8 to 13 of the final Canva deck DAHX_hKTpDE, replace gate codes with explicit check names in slide text and presenter notes, and fix the awkward wording left by earlier swaps, in place, on Haiku',
  phases: [
    { title: 'Fix', detail: 'sequential per page group: explicit check names and grammar fixes in existing boxes and notes, read back, commit if clean' },
  ],
}

const A = args
const DECK = 'DAHX_hKTpDE'
const READ = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__read-design'
const EDIT = 'mcp__b86701ca-dbd2-4b59-8bab-16fd965f353d__edit-design'
// Page 13 (implementation plan) is held back until the layout and word-cap decision is made.
const GROUPS = [[8, 9, 10], [11, 12]]
// Every agent in this workflow runs on Haiku 5.5 (set 29 October 2026).
const hagent = (prompt, opts = {}) => agent(prompt, { model: 'haiku', ...opts })

const RULES = `RULES
- Work only on the Canva design ${DECK}. Never open or edit any other design.
- Change text only inside existing text elements (find_and_replace_text or replace_text on the element's locator_id), and presenter notes only with replace_speaker_notes (page id from design_content). Do not add, delete, move, resize or restyle any element.
- Copy each find string exactly from design_content. Keep every other word as it is.
- Never invent a number, a source or a claim. Never upgrade a status.

Gate codes become check names (a small word increase is allowed for these)
- Gate 0, G0: sponsor sign-off
- Gate 1, G1: class and sweetener check
- Gate 2, G2: potassium check
- Gate 3, G3: dissolved CO2 check
- Gate 4, G4: taste test
- Gate 5, G5: pack and quote check
- Gate 6, G6: route and food-safety check
- Gate 7, G7: brand check
- Gate 8, G8: pilot design check
- Gate 9, G9: pack release check
- "Gates 2, 7" becomes "the potassium and brand checks"; "G1-G3, G5-G7" becomes "the class, sweetener, dissolved CO2, pack and quote, route and brand checks".
- Where a gate code is the subject of a sentence, rewrite the sentence with the check name so it reads naturally ("No sale until G1, G2, G7, G9 pass" becomes "No sale until the class and sweetener, potassium, brand and pack release checks pass"). Keep the meaning and the claims exactly.

Other codes
- COMPANY CLAIM becomes company claim.
- An unbracketed source class ", S" becomes ", secondary source".
- A typo "untasted" in the notes becomes "untested".
- Any remaining (DERIVED), (PROXY), (ASSUMPTION), (UNVERIFIED), OUT OF SCOPE, SECONDARY SOURCE or bracketed (S) or (P) becomes calculated, proxy, assumed, unverified, not covered, secondary source, secondary or primary. Use the explicit wording from the same sentence.

Awkward wording from earlier swaps
- "a dose cut cannot cure the class and sweetener check", wherever it appears on these pages (slide text or notes), becomes "a smaller dose cannot fix a class and sweetener failure".
- "is an assumed" or "is one assumed" becomes "is assumed" or "is one assumption", whichever reads correctly.
- "the target is an assumed" becomes "the target is assumed".
- Any other "an assumed", "a assumed" or "a calculated" becomes plain "assumed" or "calculated" where the sentence reads better that way.
- Sentence-initial "Proxy", "Assumed" or "Not covered" keeps its capital letter only if it starts the sentence.

Limits
- Each page keeps its slide text within its word cap: main pages 300 words, closing page 140. If an edit takes a page over its cap, shorten the same sentence without dropping any claim.
- Presenter notes must stay under 5,000 characters.`

const FIX_SCHEMA = {
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

phase('Fix')
const results = []
for (let i = 0; i < GROUPS.length; i++) {
  const pages = GROUPS[i].join(', ')
  const r = await hagent(
    `${RULES}

FIX GROUP ${i + 1}: pages ${pages} of ${DECK}.
Steps:
1. ToolSearch query "select:${READ},${EDIT}".
2. Open ONE transaction: read-design design_id ${DECK}, open_transaction true, filter {"fields": ["design_content", "thumbnails"], "page_indices": [${pages}], "thumbnail_pages": [${pages}]}. Note each element's locator_id and each page's id.
3. Find every gate code, tier code, awkward phrase and typo listed above, in the slide text and presenter notes of these pages. Apply the explicit wording, one edit per element, edit-design with finalize keep_open and page_index = the page. Notes go through replace_speaker_notes with the page id.
4. Read back the group's pages in the same transaction. Check for codes left, overflow and overlap. Shorten only the text you just changed if something overflows or overlaps. At most two fix calls.
5. finalize commit if the slide text has no codes, nothing overflows or overlaps, and every page is within its word cap; otherwise finalize cancel. Return committed, applied, failed (what did not apply and why), remaining_codes (slide text still carrying a code, with its page), notes_status (for each page, whether the notes changed and whether they are under 5,000 characters), and a one-line summary.`,
    { label: 'fix:g' + (i + 1), phase: 'Fix', schema: FIX_SCHEMA })
  results.push({ group: i + 1, result: r })
  log('fix group ' + (i + 1) + ': ' + (r ? (r.committed ? 'committed' : 'not committed') + ', ' + r.applied + ' edits' : 'no result'))
}

return { results }
