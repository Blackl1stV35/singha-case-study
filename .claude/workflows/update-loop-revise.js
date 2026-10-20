export const meta = {
  name: 'update-loop-revise',
  description: 'Revise the five update-loop verification items whose independent review found medium or high issues (V1, V3, V5, V6, V7), then check each revision against its own findings',
  whenToUse: 'Run after update-loop-verify. Reads rework/workflows/update_loop_review_2026-10-20.md for the findings and rework/workflows/update-loop-verify.js for each question.',
  phases: [
    { title: 'Revise', detail: 'one agent per item fixes the record and re-checks its pages' },
    { title: 'Verify', detail: 'a fresh reviewer checks each revised record against its own findings' },
  ],
}

const REVIEW_FILE = 'rework/workflows/update_loop_review_2026-10-20.md'
const QUESTION_FILE = '.claude/workflows/update-loop-verify.js'

const COMMON = `You are working in the repo D:\\Workspace\\singha-case-study for the SINGHA Ultimate Challenge 2026 entry (Singha Lemon Soda Cube, shown as "Lemon Soda"). Today is 20 October 2026.

Read first: rework/SOURCING_POLICY.md and rework/workflows/update_loop_state_2026-10-20.md.

Rules:
1. Load the tools with ToolSearch (query "select:WebSearch,WebFetch"). Open every page before you cite it. A search snippet is a lead, not evidence.
2. Save the text behind every figure to rework/raw/update_2026-10-20/<item id>/<slug>.md with the URL, the date read, and the exact sentence. A figure without a saved page is UNVERIFIED.
3. Tiers: P (regulator text, company filing or release read in full, official statistics, primary database); S (any other page read and opened); SOURCED; UNVERIFIED; DERIVED; PROXY; ASSUMPTION; COMPANY CLAIM. Never upgrade S to P.
4. No fabrication. If something cannot be found, write it as a stated limit with the route that would settle it.
5. Not allowed: outside contact, supplier or agency quotes, form submission, account creation, downloading arbitrary files, git commits or pushes. Opening public product pages and public documents is allowed.
6. Edit only your own record file and your own raw folder. Do not edit rework/deck, rework/submission or rework/proposal.
7. Plain complete sentences. No em dashes, en dashes or middle dots.`

const RESULT = {
  type: 'object',
  properties: {
    question: { type: 'string' },
    answer: { type: 'string' },
    verdict: { type: 'string', enum: ['closed', 'closed_as_limit', 'partly_closed'] },
    figures: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          label: { type: 'string' },
          value: { type: 'string' },
          tier: { type: 'string' },
          source_url: { type: 'string' },
          date_read: { type: 'string' },
          saved_page: { type: 'string' },
        },
        required: ['label', 'value', 'tier', 'source_url'],
      },
    },
    limits: { type: 'array', items: { type: 'string' } },
    issues_closed: { type: 'array', items: { type: 'string' } },
    issues_not_closed: { type: 'array', items: { type: 'string' } },
    record_file: { type: 'string' },
  },
  required: ['question', 'answer', 'verdict', 'figures', 'limits', 'issues_closed', 'issues_not_closed', 'record_file'],
}

const VERDICT = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail'] },
    checked: { type: 'array', items: { type: 'string' } },
    residual: {
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
  required: ['verdict', 'checked', 'residual'],
}

const ITEMS = [
  {
    id: 'V1', slug: 'yuzu_on_sale', record: 'rework/83_verify_V1_yuzu_on_sale.md',
    task: `ITEM V1 revision. The earlier record closed Yuzu as a limit. The reviewer found Singha Yuzu product pages on Makro PRO that the author missed: "SINGHA Yuzu Lemon Soda 330 ml x 6" at THB 84 (https://www.makro.pro/en/p/898530-7325020881091, also /en/p/cfar5hht-7325020881091) and "สิงห์ ยูสุเลมอน โซดา 330 มล. x 24" at THB 324 (https://www.makro.pro/th/p/431132-7497422667971), both with a delivery-area notice; Gourmet Market Thailand "Singha Yuzu Lemon Soda 330ML. Pack 5+1" at THB 85 (undated listing). The reviewer also notes that Makro PRO's "Singha Online" collection (https://www.makro.pro/en/c/collections/Singha%20Online) lists 15 products without Yuzu. Re-run the retailer step: domain-restricted WebSearch for makro.pro, tops.co.th, bigc.co.th, allonline.7eleven.co.th, lotuss.com and lazada.co.th; open each Yuzu product page and save it. Record each dated listing with its price, pack, date read and URL, and quote any delivery-area wording exactly. Make the answer say what is shown: Yuzu product pages exist online, and October 2026 purchasability is not confirmed. Use the review file for every point.`,
  },
  {
    id: 'V3', slug: 'line_speeds', record: 'rework/83_verify_V3_line_speeds.md',
    task: `ITEM V3 revision. Fix every medium issue in the review file. In particular: (1) open the Viking Masek 8SU-180 page (https://vikingmasek.com/packaging-machines/premade-pouch/duplex/8su-180), save it, and add its dry-cycle maximum of 80 a minute to the pre-made range; restate the pre-made range as about 15 to 80 pouches a minute, with 60 a mid-range maker figure and not a ceiling; (2) tier the Krones brochure copy on making.com as S (third-party copy of a maker document), or give the reason for treating it differently from PER-FIL, and add the brochure's own footnote that its values are examples from measurements at customer facilities; (3) correct the search counts in limits 5 and 6 to the counts in the search log; (4) state the 330 mL can range as about 100 to 300 cans a minute from the maker table, with installed lines at 200 (CFT, S) and 483 to 550 (Sidel-supplied, S, company claim), and show 600 only as a label-conflicted row.`,
  },
  {
    id: 'V5', slug: 'temperature_demand', record: 'rework/83_verify_V5_temperature_demand.md',
    task: `ITEM V5 revision. Fix every medium issue in the review file. In particular: (1) correct the scope statement about rework/screen/ambient_variation_results.json: read the file and state exactly which configurations flip a per-person or per-member leader and at what heat sensitivity; (2) the Japan soft-drink direction rests on a Consensus abstract record (Kato 2021); either open the paper or the publisher abstract and save it, or say plainly that the finding rests on an abstract record and is not read in full, and tier it accordingly. Keep the closed-as-limit verdict unless a sourced coefficient is found.`,
  },
  {
    id: 'V6', slug: 'notification_195', record: 'rework/83_verify_V6_notification_195.md',
    task: `ITEM V6 revision. Fix every medium and low issue in the review file. In particular: (1) reword the status so that it is split honestly: the text is unchanged from the Gazette original through the FDA compilation of 29 March 2023 (P); no later amending or repealing notification was found by title on the FDA list to 20 October 2026 (P, negative finding from page extraction); a post-March-2023 amendment inside a general notification is not excluded (stated limit, to be settled by the Gazette index or at Gate 1). Keep "in force" as stated, since the FDA list supports it. (2) Save the Thai sentences for clauses 1, 4(2) to 4(5)(d), 8 and 9 to the Gazette file, or point those rows to the FDA English translation file, which contains them. (3) Give the correct source URL for the scan of Nos. 333 to 473 (the list pages 1 to 15). (4) In the answer and the figure labels, say that No. 356 is as amended by Nos. 465 and 473, with No. 473 known only from a secondary summary and its Thai text not opened.`,
  },
  {
    id: 'V7', slug: 'paid_datasets', record: 'rework/83_verify_V7_paid_datasets_and_oie.md',
    task: `ITEM V7 revision. Fix every medium issue in the review file. In particular: (1) the OIE home page returns HTTP 400, but https://www.oie.go.th/view/1/statistics/TH-TH loads and links a per-product Excel and CSV (sales value, production, stock and capacity, January 2021 to August 2026). Correct every statement that says the OIE tables were not located. Do not download the file (downloads need the user's permission); add both URLs as the route that would raise the OIE rows to tier P, and keep the OIE limit as a limit. (2) Open and save three 2025 sources: Thansettakij 638312 (8 September 2025, credits Kasikorn Research Center about THB 76,900 million for 2568), Marketeer archives/415150 (9 May 2025, a 2025 forecast of THB 76,900 million), and Thansettakij 623088 (26 March 2025, over THB 66,000 million, no year or source). Record each sentence and date; add them as S rows with the credited source. Replace "the only 2025 total" with the full list of 2025 totals found (67,000 with no source; 76,900 Kasikorn; 76,900 forecast; none names NielsenIQ), and record the spread. Keep all of them unused as values.`,
  },
]

const reviseWith = (it) => `${COMMON}\n\n${it.task}\n\nThe original question and the research brief for ${it.id} are in ${QUESTION_FILE} (look for the ITEM ${it.id} entry). Every reviewer finding for ${it.id} is in ${REVIEW_FILE} (the section headed ${it.id}). Fix every high and medium finding in the record ${it.record}, rerun or reopen whatever is needed, and return the structured result. List the findings you closed and any you did not close, with the reason.`

const checkWith = (it, result) => `${COMMON}\n\nYou are the independent reviewer for the revised ${it.id} (${it.slug}). You did not write the revision. Read the record ${it.record}, the reviewer findings for ${it.id} in ${REVIEW_FILE}, and the author's result (JSON):\n${JSON.stringify(result).slice(0, 12000)}\n\nDo this: (1) confirm each finding in the review file is closed in the record, or is reported as not closed with a reason that holds; (2) re-open at least two of the source URLs the revision relies on and confirm the figure, date and tier; (3) confirm the saved pages exist under rework/raw/update_2026-10-20/${it.id}/; (4) check that no snippet is cited as a read page, no S source is tiered P, and no stated limit is presented as a closed fact. Default to fail when a finding is not closed. Return the verdict and any residual issues.`

phase('Revise')
const revised = (await parallel(ITEMS.map(it => () =>
  agent(reviseWith(it), { label: `revise:${it.id}`, phase: 'Revise', schema: RESULT, model: 'sonnet' })
    .then(r => ({ item: it, result: r }))
))).filter(Boolean)

phase('Verify')
const checked = (await parallel(revised.map(x => () => {
  if (!x.result) return Promise.resolve({ item: x.item, failed: true })
  return agent(checkWith(x.item, x.result), { label: `check:${x.item.id}`, phase: 'Verify', schema: VERDICT, model: 'sonnet' })
    .then(v => ({ item: x.item, result: x.result, verdict: v }))
}))).filter(Boolean)

return checked.map(c => ({
  id: c.item.id,
  slug: c.item.slug,
  failed: !!c.failed,
  answer: c.result ? c.result.answer : null,
  verdict: c.result ? c.result.verdict : null,
  figures: c.result ? c.result.figures : [],
  limits: c.result ? c.result.limits : [],
  issues_closed: c.result ? c.result.issues_closed : [],
  issues_not_closed: c.result ? c.result.issues_not_closed : [],
  record_file: c.result ? c.result.record_file : null,
  review: c.verdict ? c.verdict.verdict : null,
  residual: c.verdict ? c.verdict.residual : [],
}))
