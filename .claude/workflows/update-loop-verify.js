export const meta = {
  name: 'update-loop-verify',
  description: 'Run the seven remaining verification items of the 20 October 2026 update loop, each checked by an independent reviewer (Haiku for routine lookups, Sonnet for the regulatory and statistical items)',
  whenToUse: 'Run after rework/workflows/update_loop_state_2026-10-20.md. Each item writes its own record under rework/ and saved pages under rework/raw/update_2026-10-20/.',
  phases: [
    { title: 'Research', detail: 'one agent per verification item, web search and page reads' },
    { title: 'Verify', detail: 'independent reviewer per item, default to fail when a figure cannot be reproduced' },
  ],
}

const COMMON = `You are working in the repo D:\\Workspace\\singha-case-study for the SINGHA Ultimate Challenge 2026 entry (Singha Lemon Soda Cube, shown as "Lemon Soda"). Today is 20 October 2026. Read rework/SOURCING_POLICY.md and rework/workflows/update_loop_state_2026-10-20.md first.

Rules:
1. Load the tools first with ToolSearch (query "select:WebSearch,WebFetch"). Use WebSearch in standard mode; use extended mode only when a standard result is thin. Open every page before you cite it: a search snippet is a lead, not evidence.
2. Save the text or table behind every figure you use to rework/raw/update_2026-10-20/<item id>/<slug>.md with the URL, the date read, and the exact sentence. A figure without a saved page is UNVERIFIED.
3. Tiers: P (regulator text, company filing or release read in full, official statistics, primary database); S (any other page read and opened); SOURCED; UNVERIFIED; DERIVED; PROXY; ASSUMPTION; COMPANY CLAIM. Never upgrade S to P.
4. No fabrication. If a number cannot be found, say so and write it as a stated limit with the route that would settle it.
5. Not allowed: outside contact, supplier or agency quote requests, form submission, account creation, downloading arbitrary files, git commits or pushes.
6. Write only your own record file (named below). Do not edit rework/deck, rework/submission or rework/proposal.
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
    record_file: { type: 'string' },
  },
  required: ['question', 'answer', 'verdict', 'figures', 'limits', 'record_file'],
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

const ITEMS = [
  {
    id: 'V1', model: 'haiku', slug: 'yuzu_on_sale',
    record: 'rework/83_verify_V1_yuzu_on_sale.md',
    brief: `ITEM V1. Question: is Singha Yuzu soda (the Yuzu flavour of the Singha Lemon Soda range, 330 mL can) on sale in Thailand in October 2026? Search Thai and English sources: the Singha product pages, the Singha Online Shop, 7-Eleven ALL Online, Lotus's Shop Online, Makro PRO, Big C, Tops, Shopee and Lazada official stores. Report each dated listing (price, pack, date read, URL). If none is found, close it as a limit and name the route that would settle it (a store visit by the team, which is not allowed here without approval).`,
  },
  {
    id: 'V2', model: 'haiku', slug: 'distributor_margin',
    record: 'rework/83_verify_V2_distributor_margin.md',
    brief: `ITEM V2. Question: what is the margin that a Thai beverage distributor or wholesaler keeps on a 330 mL can or a carbonated soft drink, as a percentage of the selling price, in 2024 to 2026? Search Thai trade press and industry reports, company filings of Thai distributors (for example Boon Rawd Trading if it files, Thai FMCG distributors listed on SET), and Thai wholesale statistics. Also check the retailer margin used on slide 4 (25% to 35%) against the same sources. The current 10% to 20% distributor band is an unsourced assumption. Report the sourced figure or close as a limit with the best proxy named and tiered.`,
  },
  {
    id: 'V3', model: 'haiku', slug: 'line_speeds',
    record: 'rework/83_verify_V3_line_speeds.md',
    brief: `ITEM V3. Question: what are the published speeds of (a) a 330 mL aluminium can filling and seaming line and (b) a pouch or sachet filling and sealing line for dry or powder products, in units per minute? Use equipment-maker specifications (for example Krones, Sidel, KHS, Tetra Pak, Hosokawa Pillow pack, Pack Expo listings) and published line data. Give the range and the source for each line type. The current pouch speed of 60 pouches a minute with 70% efficiency and the 20 to 120 pouches a minute range are assumptions; say whether the sources support them.`,
  },
  {
    id: 'V4', model: 'haiku', slug: 'cpall_margin',
    record: 'rework/83_verify_V4_cpall_margin.md',
    brief: `ITEM V4. Question: what is the gross margin and the net margin of CP ALL Public Company Limited (7-Eleven operator in Thailand) for 2024 and 2025, and of its convenience store business if reported separately? Use the CP ALL annual report or Form 56-1 One Report, the SET filings, or the investor relations pages. Open and save the page. Give the year, the entity (group or CP ALL alone) and the basis. The current slide uses a group all-category proxy of 21.6% median; say whether a sourced figure replaces it.`,
  },
  {
    id: 'V5', model: 'sonnet', slug: 'temperature_demand',
    record: 'rework/83_verify_V5_temperature_demand.md',
    brief: `ITEM V5. Question: is there a sourced relationship between ambient temperature and soft-drink or carbonated-drink sales, usable as the seasonal temperature input of the ambient variation model (rework/screen/ambient_variation.py, sensitivity 0 to 0.05 per degree Celsius per base, currently an ASSUMPTION)? Search for (a) Thai monthly beverage sales or production series matched to Thai Meteorological Department monthly temperatures; (b) published elasticities of soft-drink demand to temperature in tropical or Asian markets (peer-reviewed papers, central bank or statistics releases). Report the coefficient with its population, period, method and tier. If nothing usable is found, say so and state what would settle it. Also report whether the finding changes the ranking of customer bases in rework/screen/ambient_variation_results.json: read that file and state the effect of any sourced value on the leader.`,
  },
  {
    id: 'V6', model: 'sonnet', slug: 'notification_195',
    record: 'rework/83_verify_V6_notification_195.md',
    brief: `ITEM V6. Question: is Thai Ministry of Public Health Notification No. 195 B.E. 2543 (mineral-salt beverages) still in force as to clause 4(1) (the composition limits including potassium at most 195 mg per litre where present) and clause 7 (the label statements), after its amendments? The page footnotes in the saved copy refer to amendments by Notification 2 (B.E. 2554, Royal Gazette 128 part 41 d, 7 April 2011) and to Notification 417 (B.E. 2563) and 413 (B.E. 2563). Search for the Thai FDA list of amended notifications, the Royal Gazette texts, and the English translations. The saved copy is in rework/raw/update_2026-10-20/V6/ if you save it there; the original PDF was read from page images. Establish which provisions were repealed or amended, and whether clause 4(1) applies to a flavoured drink that is not sold as a mineral-salt beverage (the classification test in the notification's definition). Report the status of the potassium limit in plain words, with the provision number and the tier. Do not give legal advice; state what the Gate 1 opinion must settle.`,
  },
  {
    id: 'V7', model: 'haiku', slug: 'paid_datasets',
    record: 'rework/83_verify_V7_paid_datasets_and_oie.md',
    brief: `ITEM V7. Question: can the paid market datasets and the Office of Industrial Economics (OIE) tables behind the carbonated soft-drink market value be read, for 2024 and 2025? Targets: the NielsenIQ and Euromonitor summaries for Thailand carbonated soft drinks (value, level and window); the OIE statistics on beverage production or sales value (Thai, oie.go.th) for 2024 and 2025; the Krungsri Research note of 2026 that cites OIE for a monthly domestic sales-value series. Report whether each target was opened, the figure and its level (retail or manufacturer) and window if found, and the tier. Where a paid dataset is not reachable, say so and do not infer its value.`,
  },
]

const research = (it) => `${COMMON}\n\n${it.brief}\n\nWrite your record to ${it.record} (create the folder if needed) and return the structured result.`

const review = (it, result) => `${COMMON}\n\nYou are the independent reviewer for ${it.id}. You did not write this. The question was: ${it.brief.split('\n')[0]}\n\nThe author's result (JSON):\n${JSON.stringify(result).slice(0, 14000)}\n\nDo this: (1) open the record ${it.record} and confirm it exists and matches the result; (2) re-open at least two of the source URLs and confirm the figure, date and tier; (3) confirm each saved page under rework/raw/update_2026-10-20/${it.id}/ exists and contains the quoted sentence; (4) check that no snippet is cited as a read page and no S source is tiered P; (5) check that a stated limit is not presented as a closed fact. Default to fail when a figure cannot be reproduced. Severity: high = wrong or unsourced figure, missing record; medium = tier or date error, missing saved page; low = style.`

phase('Research')
const researched = (await parallel(ITEMS.map(it => () =>
  agent(research(it), { label: `research:${it.id}`, phase: 'Research', schema: RESULT, model: it.model })
    .then(r => ({ item: it, result: r }))
))).filter(Boolean)

phase('Verify')
const verified = (await parallel(researched.map(x => () => {
  if (!x.result) return Promise.resolve({ id: x.item.id, failed: true })
  return agent(review(x.item, x.result), { label: `verify:${x.item.id}`, phase: 'Verify', schema: VERDICT, model: 'sonnet' })
    .then(v => ({ id: x.item.id, slug: x.item.slug, result: x.result, verdict: v }))
}))).filter(Boolean)

log(`researched ${researched.filter(x => x.result).length} of ${ITEMS.length}`)

return verified.map(v => ({
  id: v.id,
  slug: v.slug,
  failed: !!v.failed,
  answer: v.result ? v.result.answer : null,
  verdict: v.result ? v.result.verdict : null,
  figures: v.result ? v.result.figures : [],
  limits: v.result ? v.result.limits : [],
  record_file: v.result ? v.result.record_file : null,
  review: v.verdict ? v.verdict.verdict : null,
  review_issues: v.verdict ? v.verdict.issues : [],
}))
