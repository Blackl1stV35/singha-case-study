export const meta = {
  name: 'singha-deck-diligence-loop',
  description: 'Research or model each deck diligence task, verify it independently, revise and re-verify in a loop until nothing blocking is left (routine on Haiku 5.5; hard statistical and chemistry tasks on Sonnet)',
  whenToUse: 'Re-run the 20 October 2026 deck diligence prompt (rework/workflows/deck_diligence_prompt_2026-10-20.md). Pass args.only as a list of task ids (T1 to T16, T68) to rerun a subset; args.maxRounds sets the revision rounds (default 2); args.hardModel sets the reviewer for hard tasks (default sonnet). Check the weekly usage meter before a Sonnet pass.',
  phases: [
    { title: 'Stage 1 research', detail: 'web research and chemistry models, one agent per task' },
    { title: 'Stage 2 derive', detail: 'estimates of Singha internal information and the competitor synthesis' },
    { title: 'Stage 3 model', detail: 'value accrual, sequential Monte Carlo, ambient variation' },
    { title: 'Verify', detail: 'independent verifier per task, then revise and re-verify' },
    { title: 'Critic', detail: 'completeness check against the prompt' },
  ],
}

const MAX_ROUNDS = (args && args.maxRounds) || 2
const ONLY = (args && args.only) || null
// Model routing (rework/workflows/model_routing_2026-10-20.md). Authors and routine verifiers run on Haiku 5.5.
// Hard statistical and chemistry tasks verify and revise on Sonnet; the author stage stays on Haiku.
const MODEL = 'haiku'
const HARD_MODEL = (args && args.hardModel) || 'sonnet'
const HARD = ['T8', 'T9', 'T10', 'T11', 'T12', 'T14', 'T15']
const reviewModel = t => (HARD.includes(t.id) ? HARD_MODEL : MODEL)

const COMMON = `You are working on the SINGHA Ultimate Challenge 2026 entry: the Singha Lemon Soda Cube (shown as "Lemon Soda"): one dissolvable lemon cube dropped into 330 mL of water (potassium bicarbonate 0.81 g, citric acid 2.10 g, sucralose about 33 mg, binder and filler 0.80 g, lemon flavour 0.05 g; 14 mm cube; central dry mass 3.79 g). The proposer is Singha Corporation; Boon Rawd Brewery is the holding company. The repo is D:\\Workspace\\singha-case-study. Today is 20 October 2026. Read rework/SOURCING_POLICY.md and CLAUDE.md first (section 0 of CLAUDE.md supersedes the lime-cube lines). The judge-facing set is rework/submission/*.md, the team copies are rework/proposal/*.md, the deck content is rework/deck/deck_content.md, and the tier key is rework/submission/appendix_a_tier_key.md.

Rules that apply to every task:
1. Tools: load WebSearch and WebFetch first with ToolSearch (query "select:WebSearch,WebFetch"). Use WebSearch in standard mode and switch to extended mode when a standard result is thin, for niche Thai facts or for recent figures. Read Thai pages in Thai where needed.
2. Sourcing: primary first, secondary allowed and labelled. Tiers: P, S, SOURCED, UNVERIFIED, DERIVED, PROXY, ASSUMPTION, COMPANY CLAIM. Every figure carries a value, a tier, a source URL and the date read. Open a page before citing it: a search snippet is only a lead. Save the text or table behind every SOURCED figure to rework/raw/diligence_2026-10-20/<task id>/<slug>.md with the URL and the date read (a figure whose page is not saved is UNVERIFIED).
3. No fabrication: never invent a number and never invent a breakdown of a total. If a number cannot be traced, write UNVERIFIED and say what would settle it. Close an unverifiable item as a stated limit instead of leaving it open. Quote numbers only from a source or results file you have read.
4. Models: write the script and a results JSON (under rework/screen/), run it, and report only numbers it produced. Fixed seeds. The machine has little free memory (about 1 GB): keep each Python process under 300 MB, run one at a time, and do not launch a browser, Playwright or Blender.
5. Not allowed: form submission, account creation, entering personal data, outside contact of any kind, supplier or agency quote requests, downloading arbitrary files, publishing, git commit or push (the lead does that).
6. Write only your own output files named in the task. Do not edit rework/submission, rework/proposal or rework/deck files; put proposed text in your result. Create folders as needed.
7. Text written for the judges and the executives: plain complete sentences; no em dashes, no en dashes, no middle dots; no internal notes; never hand a decision to Singha Corporation. Where an earlier plan said Singha decides something, state the setting the team proposes, its basis and its tier. Items that cannot be closed from sources are stated limits.
8. Report honestly: say what is verified, what is a proxy and what could not be checked. If your result contradicts the current deck or submission text, list it under conflicts.`

const RESULT = {
  type: 'object',
  properties: {
    summary: { type: 'string' },
    files_written: { type: 'array', items: { type: 'string' } },
    figures: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          label: { type: 'string' },
          value: { type: 'string' },
          tier: { type: 'string' },
          source: { type: 'string' },
          source_date: { type: 'string' },
          saved_page: { type: 'string' },
          note: { type: 'string' },
        },
        required: ['label', 'value', 'tier', 'source'],
      },
    },
    slide_text: {
      type: 'array',
      items: {
        type: 'object',
        properties: { target: { type: 'string' }, text: { type: 'string' } },
        required: ['target', 'text'],
      },
    },
    limits: { type: 'array', items: { type: 'string' } },
    conflicts: { type: 'array', items: { type: 'string' } },
  },
  required: ['summary', 'files_written', 'figures', 'slide_text', 'limits'],
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
          where: { type: 'string' },
          problem: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['severity', 'where', 'problem', 'fix'],
      },
    },
  },
  required: ['verdict', 'checked', 'issues'],
}

const COMP = `For each entity cover: ownership and role (brand owner, bottler, distributor) and the group it belongs to; brands in lemon, lime, clear carbonated and sugar-free lines with launch dates; shelf price and pack and the price per 330 mL; channels; market share (volume or value, with the year and the source); financials for the last three fiscal years from filings (revenue, gross profit and gross margin, net profit and net margin; state the legal entity and whether the figure is the group or the Thai entity, and the fiscal year end; SET filings, 56-1 One Report, annual reports, DBD statements); the key advantages (distribution reach, brand, price, capacity, innovation, trade terms); recent moves 2023 to 2026 (launches, sugar-free ranges, packaging, price changes); and the threat or response to a dissolvable cube (what they could copy and what they cannot). Give a comparison table fit for rework/proposal/11 section 2.3 and for slide 8. Brand-owner and bottler margins are not comparable: say which is which.`

const TASKS = [
  {
    id: 'T1', stage: 1, title: 'Market sizes checked at source (carbonated soft drink and bottler)',
    out: 'rework/67_market_size_source_check.md',
    brief: `TASK T1 (slide 3, market size). The deck says: "Press figures for the Thai carbonated soft-drink market differ: over THB 66,000 million (2024 press, year not stated) and THB 76,900 million (2026 bottler data). Neither is checked at source, and no market is sized from them." Canned carbonated drinks are quoted as THB 13,172 million (Marketeer, 16 August 2022, year not stated). The user asked: check at source for both the carbonated soft-drink market and the bottler market.
Do: (1) Trace each figure to the page it came from: the Thansettakij article of 16 March 2024 and whatever it quotes; the source of THB 76,900 million (search rework/proposal, rework/submission and rework/raw for 76,900 and 66,000); the Marketeer article of 16 August 2022. Open and save each page. (2) Find primary or best-available sources for the Thai carbonated soft-drink market: value and volume, the level of the value (retail sales value or manufacturer revenue), the year and the definition (carbonated only, or all soft drinks). Candidates: Euromonitor, Statista, Mordor, IMARC or Fitch Solutions summaries, Nielsen, Kantar, the Office of Industrial Economics, trade associations, trade press. (3) Bottler market: the bottlers' own filings and releases. The Coca-Cola bottlers in Thailand (Thai Namthip, Coca-Cola Beverages (Thailand) and any other), the Pepsi bottler Serm Suk PCL and any other: read their revenue for the last three fiscal years (SET, 56-1 One Report, DBD statements). Sum what is reported and state what is missing. (4) Reconcile the figures into one defensible range with its definition and tier. If they cannot be reconciled, say which is best supported and why, and close the rest as stated limits. (5) Look for a lemon-lime or clear carbonated sub-segment size. (6) Return the final slide 3 sentence (figure, year, level, tier) and the Appendix C limit sentence.`,
  },
  {
    id: 'T2', stage: 1, title: 'Competitor due diligence: Coca-Cola system',
    out: 'rework/68a_coca_cola_system.md',
    brief: `TASK T2 (competitor due diligence, Coca-Cola system). Entities and brands: The Coca-Cola Company's Thai operations, Sprite, Sprite Lemon Plus, Sprite Zero, Schweppes (find out who owns and makes it in Thailand), Fanta; the bottlers Thai Namthip Ltd, Coca-Cola (Thailand) Ltd, Coca-Cola Beverages (Thailand) and any other the filings show. ${COMP}`,
  },
  {
    id: 'T3', stage: 1, title: 'Competitor due diligence: Pepsi system and Serm Suk',
    out: 'rework/68b_pepsi_sermsuk.md',
    brief: `TASK T3 (competitor due diligence, Pepsi system). Entities and brands: Pepsi-Cola (Thai) Trading, Serm Suk PCL (SET: SSC; check current ownership, listing status and its ThaiBev relationship), Pepsi, 7UP, 7UP No Sugar, Mirinda, and any lemon or lime variants. Also resolve what "S Cola 8.6%" in the market-share line of the deck refers to (the company that owns S Cola). ${COMP}`,
  },
  {
    id: 'T4', stage: 1, title: 'Competitor due diligence: Osotspa, ThaiBev, S-Cola, private label and other lemon sodas',
    out: 'rework/68c_osotspa_thaibev_private_label.md',
    brief: `TASK T4 (competitor due diligence, other makers). Entities: Osotspa PCL (est cola, SET: OSP), the non-alcoholic arm of Thai Beverage (Chang soda, Oishi, est through Serm Suk as the filings show), the owner of S-Cola, and private labels (Aro at Makro, Lotus's, Big C, Tops). Also determine which other firms sell lemon or lime flavoured sodas and soda waters in Thailand (local brands, craft sodas, imports) and which could respond to a lemon cube. ${COMP}`,
  },
  {
    id: 'T5', stage: 1, title: 'Retail price ladder for lemon and lime carbonated drinks',
    out: 'rework/68d_lemon_soda_price_ladder.md',
    brief: `TASK T5 (retail price ladder). Scan current dated retail listings (7-Eleven and CP All online, Lotus's, Big C, Makro, Tops, Foodland, Lazada and Shopee official stores, brand sites) for lemon, lime and clear carbonated soft drinks and soda waters in 325 to 345 mL cans: Sprite, Sprite Lemon Plus, Sprite Zero, 7UP, 7UP No Sugar, Schweppes lime and lemon soda, Singha Lemon Soda, Singha Soda, house brands, and any other found. For each: product, size, pack, price, price per 330 mL, retailer, date read, URL, sugar status. Save the pages. Give the ladder (minimum, median, maximum), where the THB 15 planning shelf price sits on it, and the price per serve for the cube against the can. If a retailer blocks automated reading, record that as a limit and use another retailer. This task is prices only: competitor financials belong to T2 to T4.`,
  },
  {
    id: 'T5b', stage: 1, title: 'Competitor due diligence: dissolvable and effervescent drink analogues',
    out: 'rework/68e_dissolvable_drink_analogues.md',
    brief: `TASK T5b (competitor due diligence, dissolvable analogues). Entities: overseas drink cubes and tablets that a Thai shopper or retailer could meet (Waterdrop or Microdrink, Coca-Cola Japan freeze-dried cubes, Ricola drink cubes, Nuun and other electrolyte tablets, Hydralyte, Thai-sold effervescent vitamin tablets such as Berocca and Redoxon, soda-making machines such as SodaStream and their flavour syrups as a different route to a home soda). For each: format, price per serve, claims, channel in Thailand (listed or not, dated evidence), company scale and margins where public (Waterdrop, SodaStream under PepsiCo, Nestle Health Science for Nuun; open the filings or reports), key advantage, and what a Thai entrant would meet (regulatory class, price anchor). State what a dissolvable cube must beat on price per serve against the canned lemon soda ladder in rework/68d if it exists. ${COMP}`,
  },
  {
    id: 'T6', stage: 1, title: 'Slide 4: verify every open point on the can',
    out: 'rework/69_can_leverage_verification.md',
    brief: `TASK T6 (slide 4, verify every open point on the can). Slide 4 says: launched August 2020 in a 330 mL can; flavours Yuzu 2021, Red 2022, Ume 2023, Pink 2024, Lemon Cream 2025; THB 16 for the lemon can at launch in 2020 and THB 16 and 17 for later flavours; channels 7-Eleven, supermarkets and the Singha Online Shop named in 2024 and 2025 press; sugar-free wording at launch is the company's claim; and "not yet verified: line capacity at the group's plants, the can's unit cost, its current shelf price and the retail reach". The user asked: proceed complete the verifications to all open points.
Do: (1) Open the Singha Lemon Soda product page now (the site named in rework/raw/browser_captures_2026-10-18.md and rework/raw/captures_2026-10-19) and the company's launch releases; save the text; verify each date, flavour, pack, price, sweetener wording and claim. (2) Current shelf price and pack: dated listings at 7-Eleven (CP All), Lotus's, Big C, Makro, Tops, Foodland, the Singha Online Shop, Shopee and Lazada official stores; the price per 330 mL for single cans and multipacks (share the pages with T5's ladder only through your own saved pages). (3) Retail reach and channels: which channels list the can, any count or share, the distributor structure (check Boon Rawd Trading or Singha Trading), modern against traditional trade. (4) Is the can still on sale in October 2026, in which flavours, and what the company says about its sales (revenue, growth, share) in releases, the annual report or investor material. (5) Production: where the can is made (own plant, co-packer, which plant), published capacities and lines at Boon Rawd's and Singha Corporation's plants (filings, sustainability reports, press), canning line speeds if published. (6) Singha Corporation group financials from primary sources: revenue and net profit 2023 to 2025 (check the THB 3,085 million for 2025 at the primary), the segment split, listing or IPO status as of October 2026. (7) Anything published on the can's unit cost or margin; the can-cost model rework/screen/can_cost_model.py and records rework/58 and rework/61 list the primary sources it still needs (LME settlement, Bank of Thailand rate, the sugar levy, a can-maker's annual report): close what can be sourced now. For every open point give: closed (source and tier) or closed as a stated limit (what would settle it). Deliver finished slide 4 text for all four cards and the note bar.`,
  },
  {
    id: 'T8', stage: 1, title: 'Slide 6: chemistry model of taste, dissolution time and the surface-only fizz bound',
    out: 'rework/71_cube_chemistry_model.md',
    brief: `TASK T8 (slide 6, chemistry model). The deck says: working pH 3.5; taste not tested; dissolution time not yet measured (an earlier unsupported "about 60 seconds" was removed); fizz above a 0.44 g/L threshold for up to about 96 minutes, a derived surface-only upper bound (rework/submission/09_feasibility_and_registration.md around line 15; rework/screen/cube_size_0_55.py and formulation_desk_model.py hold the earlier models). The user asked: proceed model based on the chemistry science to the taste, dissolution time and the surface-only upper bound.
Build three transparent models, each a Python script with a results JSON in rework/screen/ (file stem cube_chemistry_), every input tiered and sourced (open sources, save pages):
(a) Taste. From the recipe (potassium bicarbonate 0.81 g, citric acid 2.10 g, sucralose 33 mg in 330 mL) compute: the equilibrium pH by charge balance with citric acid pKa 3.13, 4.76 and 6.40 (and their temperature dependence at 5, 20 and 30 C), ionic strength, titratable acidity (g/L as citric acid and mmol H+ to pH 8.2), the potassium ion concentration, the sucralose sweetness equivalent (potency range from sources; sucrose-equivalent g per 100 mL), the sweetness to acid ratio, and compare with benchmark lemon-lime sodas (Sprite or 7UP nutrition and ingredient data: acid g/L, pH, Brix; open sources). Compare the potassium and acid levels with published taste thresholds (potassium chloride bitter and metallic detection threshold, citric acid sourness thresholds, sweetness equi-intensity). Output a chemistry-based predicted taste profile with risk flags (too sour, salty or bitter, thin sweetness, weak carbonation bite) and which input to adjust (acid level, sweetener amount or blend, flavour) with the arithmetic. Do not claim a taste result.
(b) Dissolution time. Model a 14 mm compressed cube of 3.79 g (density from mass and volume; porosity an assumption) dissolving and reacting in 330 mL of water at 20, 25 and 30 C, stirred and unstirred. Use Noyes-Whitney and shrinking-particle kinetics with literature solubilities and diffusion coefficients (citric acid, potassium bicarbonate), the acid-base reaction rate, and the stirring effect of CO2 bubble evolution on the mass-transfer coefficient. Cross-check against the Ph. Eur. 2.9.1 effervescent tablet limit (disintegration within 5 minutes in 200 mL of water at 15 to 25 C) and against published effervescent tablet dissolution times (open the sources). Give low, central and high times to full dissolution, name the dominant uncertainty, and call it a model estimate, not a measurement.
(c) Surface-only upper bound on fizz. Rebuild the fizz-duration bound: dissolved CO2 of 0.55 volume (convert to g/L; state the molar volume and temperature basis) in a 330 mL serve in an open glass, loss through the free surface only, with the 0.44 g/L threshold (an abstract-only sparkling-water figure, PROXY). Use Henry's law and a liquid-side mass-transfer coefficient range from the literature (still, stirred, nucleating glass). Show the surface-only time as the upper bound, then add bubble nucleation losses (champagne and beer literature, Liger-Belair and others) to give a lower bound and a central range. Re-derive the 96 minutes, reconcile it with the earlier script, and say whether 96 minutes stands.
Report which conclusions are robust to the inputs (a one-at-a-time tornado). Give finished slide 6 text (the durations of stages 2 and 3, or the reason none can be stated) and the proposal text.`,
  },
  {
    id: 'T9', stage: 1, title: 'Slide 7: revalidate every product specification from first principles',
    out: 'rework/72_spec_revalidation.md',
    brief: `TASK T9 (slide 7, revalidate all product specifications). Recompute every figure on slide 7 and its caveat from first principles in a fresh script (rework/screen/spec_revalidation.py with results JSON) BEFORE you read rework/screen/formulation_desk_model.py, cube_size_0_55.py, project_valuation.py or the calculations in the submission files; then compare. Figures: 0.55 volume of CO2 per 330 mL (state the molar volume and temperature basis; show the result at 0, 20 and 30 C); potassium bicarbonate 0.81 g; potassium 317 mg a serve and its share of a 3,500 mg reference (and of the EFSA and US National Academies adequate intakes; open the sources); citric acid 0.52 g stoichiometric and 2.10 g at pH 3.5 (charge-balance solution; show pH against citric acid mass); sucralose 33 mg and about 100 mg/kg (state the mass basis of the serve); binder and filler 0.80 g; lemon flavour 0.05 g; central dry mass 3.79 g and its range 3.46 to 4.24 g (what drives the range); the 14 mm cube, density and compaction plausibility (typical effervescent tablet density and hardness) and the cube volume from mass and density; packed 5.29 g with a 1.5 g pouch; net weight 3.8 g; the six-cube carton of 190 x 150 x 50 mm (pouch geometry and packing); the 20 ft container at 21,431 cartons and 128,586 cubes (internal dimensions from the ONE page, 92% packing); cost per cube THB 4.09 (reactants 0.12, pouch and print 2.80, processing 0.50, carton 0.67): re-price the reactants from current food-grade price sources where reachable (open them); contribution THB 4.91 at a planning price of THB 9.00 and the 60% ex-factory share. For each: matches, mismatches (with the right value), and the sensitivity to its assumption. Flag any specification that chemistry or regulation makes inconsistent (for example the sucralose level against sweetness, the pH against taste, or the 14 mm size at 3.79 g). Give corrected slide 7 table rows if anything changes.`,
  },
  {
    id: 'T10', stage: 1, title: 'Slide 7 caveat: potassium, potassium-retaining medicines and kidney disease',
    out: 'rework/73_potassium_medicines_kidney_cover.md',
    brief: `TASK T10 (slide 7 caveat). The deck says: potassium is 317 mg a serve, about 9% of a 3,500 mg reference; the desk model does not cover people on potassium-retaining medicines or with kidney disease; a medical view is required at Gate 2. The user asked: source to check the cover of potassium-retaining medicines or with kidney diseases. Read this as: find the guidance and the share of consumers it covers, so the 317 mg serve can be judged.
Do: (1) Drug classes that raise serum potassium (ACE inhibitors, ARBs, mineralocorticoid antagonists such as spironolactone and eplerenone, potassium-sparing diuretics such as amiloride and triamterene, trimethoprim, heparin, NSAIDs, calcineurin inhibitors, beta blockers, potassium supplements and salt substitutes) from primary sources (drug labels, the Thai National List of Essential Medicines, KDIGO, ESC or AHA guidance, NICE or UK Renal Association hyperkalaemia guidance, peer-reviewed papers). (2) Kidney disease: dietary potassium guidance by CKD stage (KDIGO 2024, KDOQI 2020, Thai Nephrology Society or a Thai CKD guideline) and what a 317 mg single drink means against typical restrictions and against Thai foods and drinks (coconut water, orange juice, banana, sports drinks; Thai Food Composition Database of INMU Mahidol or the Ministry of Public Health; USDA FoodData Central). (3) Coverage: the share of Thai adults with CKD (Thai SEEK, Ministry of Public Health, Thai Nephrology Society), CKD stages 3 to 5, treated hypertension (ACE inhibitor or ARB use), heart failure and diabetes, and an estimate of the combined share of men aged 25 to 59 and of all adults covered by the caution (DERIVED; state overlaps; do not double count). The lead segment is men 25 to 34, so give the age-specific share. (4) How comparable products warn: US FDA and EU rules for potassium-containing products and electrolyte drinks, any Thai FDA rule on potassium labelling or high-potassium claims, and the precaution wording on effervescent potassium products (for example potassium bicarbonate effervescent tablet labels; open them). (5) Judge the serve: is 317 mg a serve plausible for a general-population beverage? Compare the 99 mg per dose US limit for potassium in over-the-counter supplements and the potassium in a Thai coconut water serve. Recommend the label precaution wording (Thai and English) that Gate 2 would review, and the stated-limit text. Do not give medical advice; frame the work as a screening for a reviewer.`,
  },
  {
    id: 'T11', stage: 1, title: 'Appendix A: sodium check, binder and filler named',
    out: 'rework/74_sodium_check_and_label_rules.md',
    brief: `TASK T11 (Appendix A, sodium). The label rules say: no sodium carbonate; the binder and filler are not yet named or checked for sodium; sodium-free and low-sodium wording are barred. The user asked: check the sodium. The proposal must be finished by us, so name the binder and filler.
Do: (1) Choose and name the binder and filler (0.80 g in the 3.79 g cube) from sodium-free, sugar-free, tableting-grade options (for example mannitol, isomalt, erythritol, sorbitol, PEG 6000 as a soluble lubricant, leucine, low-sugar maltodextrin; reject insoluble options such as microcrystalline cellulose), justified by effervescent tablet formulation literature (open it), dissolution clarity, hygroscopicity and moisture reaction with the acid and bicarbonate pair, laxative or tolerance limits at the dose, price per kg (sourced, else ASSUMPTION), and Thai FDA permission (rework/raw/moph_468_annex_flavoured_drinks_extract_2026-10-19.md and Notification 468 category 14.1.4: is the substance listed for flavoured drinks, or is it a processing aid or carrier?). Check that the choice adds no sugar under the Thai sugar-drink excise definition (rework/raw/gazette_sugar_drink_excise_primary_2560_A095_111.md: how sugars and polyols are treated). Give a primary choice and one fallback. (2) Sodium per serve: for every component (potassium bicarbonate, citric acid, sucralose, lemon flavour and its carrier, the binder and filler, and any pouch film migration) give the specification limit or typical sodium (FCC, JECFA, supplier specification sheets; open them), compute mg per serve and mg per 100 mL as consumed (330 mL), and the total as a range. (3) Regulatory thresholds: the Thai rule for "sodium free" and "low sodium" claims (Ministry of Public Health notifications on nutrition labelling and claims; read the Thai text) and Codex CAC/GL 23 (sodium-free, very low and low thresholds); the Thai rule on declaring sodium on a beverage nutrition label; any Thai front-of-pack sodium scheme that applies. (4) Conclusion: is "no added sodium salt" a supportable composition fact? Is any claim possible? Keep barred claims barred unless the Thai rule allows a claim with a verified number (then give the number needed and the test). Write the finished Appendix A text: the "May say", "Barred" and "Held" lists, with the binder named, no "not yet named", and the sodium fact stated with its basis and tier.`,
  },
  {
    id: 'T13', stage: 1, title: 'Strategic business unit involvement and the stakeholder onion',
    out: 'rework/76_sbu_involvement_and_stakeholder_onion.md',
    brief: `TASK T13 (strategic business units and the stakeholder onion). The user asked to add strategic business unit involvement and a stakeholder onion to the proposal. The executives receive the proposal, so owners must be assigned by us and not handed over.
Do: (1) From primary sources (Singha Corporation and Boon Rawd websites, annual and sustainability reports, SEC filings, releases) establish the business units and functions as published: beer and alcoholic beverages, soda and drinking water, other non-alcoholic beverages, food and restaurants, Singha Park, international, distribution (Boon Rawd Trading or Singha Trading), R&D and quality, supply chain and plants, marketing and brand, finance, legal and regulatory, sustainability. Use only units you can source and label each (P or S). (2) SBU involvement: a matrix of unit by phase and gate (Gates 0 to 9 and Phases 0 to 6 in rework/submission/10_risk_and_implementation.md) giving each unit's role (responsible, accountable, consulted, informed), the deliverable it owns, the capability it already holds (sourced) and the gap, so that every gate has an owning unit (a role, not a person) and no decision is handed over: the matrix is the proposal's own operating model. (3) Stakeholder onion, from the core outward: the project core; Singha Corporation business units and functions; the group and its shareholders (Boon Rawd Brewery, the board); the value chain (suppliers of potassium bicarbonate, citric acid, sucralose, pouch film and cartons; co-packers; distributors; retailers such as 7-Eleven, Makro, Tops, Lotus's and online marketplaces); consumers and the lead segment; regulators and standards bodies (Thai FDA, the Excise Department, the Department of Intellectual Property, the Consumer Protection Board); the wider environment (competitors, medical reviewers, media and KOLs, community and sustainability bodies). For each stakeholder: interest, influence on the programme, expected stance, risk, how the proposal engages them, and the gate that depends on them. Give a table plus a layer list that a designer can draw as concentric rings. (4) Give the finished slide 13 exhibit text for both, to replace the old "decisions for Singha Corporation" exhibit.`,
  },
  {
    id: 'T16', stage: 1, title: 'Marketing campaign proposal with domestic KOLs: research and survey',
    out: 'rework/79_kol_campaign_research_and_survey.md',
    brief: `TASK T16 (marketing campaign proposal with domestic KOLs). The user asked to add research and survey for a marketing campaign proposal using domestic KOLs (Thai key opinion leaders and influencers). Reading: a desk survey of the Thai influencer market and a scan of domestic KOL candidates, then a finished campaign proposal. No outreach to any KOL or agency, no form and no fielded respondent survey (repo rule: outside contact needs the user's approval).
Do: (1) Market research from sources (2025 and 2026 first; open and save pages): Thai social media and platform use (DataReportal Digital 2026 Thailand or the latest, Meta, TikTok and LINE releases, the ETDA Thailand Internet User Behavior survey); the Thai influencer marketing market size and fee ranges by tier (nano, micro, mid, macro, mega; agency rate cards and trade press such as Brand Buffet, Marketeer and Positioning, Wisesight, Starngage or HypeAuditor summaries); engagement rates by tier and platform; Thai consumer trust in KOL recommendations and their effect on beverage and food purchase (Kantar, Nielsen, YouGov, Wisesight, ETDA); the shift to TikTok Shop and live commerce; benchmarks for cost per view, cost per click and cost per acquisition for Thai beverage campaigns, compared with the existing assumptions in rework/submission/10 (cost per click THB 11.5 PROXY, cost per thousand impressions THB 120 ASSUMPTION). (2) KOL landscape scan: a shortlist of at least 20 domestic KOLs across tiers and platforms who fit men aged 25 to 34 and the product (food and drink reviewers, lifestyle, fitness and health, comedy, gaming, home bar content), using only public profile pages and public aggregator figures (follower counts and engagement, with the date read and the source, labelled S); public figures only, no private information, and no claim that any is available or contacted. Score each for audience fit, brand safety (no alcohol-promotion conflict, no controversy found in a public check), and platform and format fit, and give the score rule. Check what Singha has publicly done with presenters and KOLs (Singha Lemon Soda, Singha Soda, 2020 to 2026). (3) Regulation and brand safety: the Thai Food Act B.E. 2522 advertising rules (section 40 and the Ministry of Public Health notifications on food advertising), the Consumer Protection Board and OCPB guidance on influencer and sponsored content disclosure, the Alcohol Control Act B.E. 2551 section 32 (the SINGHA name and alcohol cues), platform ad policies (Meta, TikTok, YouTube, LINE) for beverages, and what a KOL may and may not say about this product (reuse the label rules in rework/deck/deck_content.md Appendix A: no sugar-free, health, hydration or fizz claims until cleared). (4) Campaign proposal finished by us: the objective funnel (awareness, trial, repeat); the tiered KOL mix and the number of creators per tier; content formats (make-it-in-the-glass demonstration, blind taste test, home bar); the platform mix; phasing across the 13-week pilot (weeks; Route A and Route B in rework/submission/10); the one pilot budget by line with arithmetic and tier; the cost per first purchase and its break-even against the THB 3.51 contribution floor (use the pilot funnel and the cost-per-click assumption; flag if paid social does not recover its first-purchase cost); KPIs and the measurement design (unique codes, listing click-to-purchase, a brand-lift question set); the compliance checklist; the risk register (KOL controversy, platform policy, alcohol cue, undisclosed sponsorship) with mitigations; and the stop rule. (5) Survey instrument: 6 to 10 consumer questions on KOL influence (trust, platform, content preference, purchase effect) in English and Thai, ready to add to the concept survey (rework/proposal/12_concept_survey_plan.md); do not edit that file. Give finished text for one deck slide on the campaign, in plain sentences, and the proposal text. Also write rework/79a_kol_shortlist.md with the candidate table.`,
  },
  {
    id: 'T7', stage: 2, title: 'Slide 4: estimates of Singha internal information by derivation',
    out: 'rework/70_singha_internal_estimates.md',
    brief: `TASK T7 (slide 4, estimate Singha's internal information by derivation). The user asked: complete the verifications of all open points on the can, plus deriving estimated verifications of Singha's internal information. Singha does not publish these figures, so derive them from public anchors and say so at the top of the record: "Estimates derived from public data; not Singha figures". Use the verified records of the earlier tasks listed in the context (rework/67, 68a to 68e, 69) as anchors.
Estimate, each with a central value, a 90% interval, a tier (DERIVED, with the anchors tiered) and two independent derivations (top-down and bottom-up) compared: (1) the Singha Lemon Soda annual can volume and revenue; (2) its share of Singha Corporation revenue and net profit; (3) the can's variable cost (reuse and update rework/screen/can_cost_model.py with sourced inputs; the existing result is THB 4.94 a can at the mid input, range 3.73 to 6.14) and the ex-factory price (shelf price less the trade margin chain; trade margins from sources); (4) gross margin and contribution per can, compared with listed peers' gross margins from rework/68; (5) line capacity and utilisation: the group's plants and the canning or pouch line capacity that could carry the Cube (filings, plant lists, the 1,676 million cans group nameplate PROXY in the can-cost model), the headroom for 200,000 to 1,000,000 cubes a year expressed as hours of line time and as a percent of capacity, and what a co-packer would need; (6) cannibalisation exposure: the can's contribution at risk if 25 or 50% of cube buyers are existing can buyers; (7) the pilot's fixed-cost fit against the base THB 500,000. Write the estimate table, the method, the cross-check gaps and the limits. Put the can-cost numbers for slide 9 and the Singha-side text for slide 4 in your result. Script: rework/screen/singha_internal_estimates.py with results JSON.`,
  },
  {
    id: 'T68', stage: 2, title: 'Competitor due diligence: synthesis',
    out: 'rework/68_competitor_due_diligence.md',
    brief: `TASK T68 (competitor due diligence, synthesis). Read the verified competitor records rework/68a_coca_cola_system.md, 68b_pepsi_sermsuk.md, 68c_osotspa_thaibev_private_label.md, 68d_lemon_soda_price_ladder.md and 68e_dissolvable_drink_analogues.md and the market record rework/67_market_size_source_check.md (those that exist). Write rework/68_competitor_due_diligence.md: one comparison table (entity, role, lemon and lime lines, shelf price per 330 mL, share, gross margin and net margin with year and entity, key advantage, recent move, response to a cube), the margin comparability note, the strategic reading (where the cube competes, where it does not, the price position at THB 15), the answer to the brief's questions 3 (competitors: pricing, gross margin or net margin, key advantage) and 4 (what consumers like about the product), the finished slide 8 text (table, strip, note bar, source line) and slide 3 competitor lines, and the stated limits. Do not add a figure that is not in those records; spot-check at least ten figures against the saved pages in rework/raw/diligence_2026-10-20 and report any mismatch in the earlier records as a conflict.`,
  },
  {
    id: 'T12', stage: 3, title: 'Slide 10: model how value accrues',
    out: 'rework/75_value_accrual_model.md',
    brief: `TASK T12 (slide 10, how value accrues). The deck says: the base-case NPV is about 0.03% of one year's profit of Singha Corporation (about THB 3,085 million, MGR Online 23 May 2026, S); value accrues to Singha Corporation; how it passes to the shareholders of Boon Rawd Brewery is not modelled. The user asked: do the modeling on value accrues.
Do: (1) Establish the structure from primary sources (use rework/69 and rework/76 if present, then check yourself): Boon Rawd Brewery Co., Ltd. and Singha Corporation Co., Ltd. (ownership percentages, other shareholders, any listing or IPO filing as of October 2026, dividend policy and payout ratio, the corporate income tax rate, group net profit and revenue for 2023 to 2025). Use SEC filings, SET, Singha releases, DBD and annual reports; save pages. (2) Build rework/screen/value_accrual_model.py (with results JSON) that maps the project cash flows (the base from rework/screen/project_valuation.py: 200,000 cubes a year, THB 4.91 contribution, THB 500,000 fixed cost, five years, 10% discount rate, year 0 outlay of one year's fixed cost, year 1 at half volume) to: after-tax project cash flow (Thai corporate income tax 20%, check); cannibalisation netting against the Singha Lemon Soda can (the can's contribution from rework/70 if present, else rework/screen/can_cost_model_results.json; cannibalisation of 0, 25, 50 and 100 percent of cube buyers); incremental net profit by year; its share of Singha Corporation net profit each year and cumulatively; dividends to the parent and to the ultimate holders at the stated ownership and payout; the implied equity value uplift using sourced peer price-to-earnings multiples (ThaiBev, Osotspa, Carabao, Serm Suk or others; open sources) alongside the NPV method; return on invested capital against a cost of capital (the Bank of Thailand policy rate in rework/raw/bot_fx_primary_2026-10-15.md plus a stated premium, ASSUMPTION); and the scale at which the project would matter (the annual cubes needed for the incremental profit to reach 0.1%, 0.5% and 1% of group net profit). (3) State plainly how much value accrues, to whom and when, with the break points, and whether the project is a value driver or a learning option. Give finished slide 10 text and the shareholder-value section text for rework/submission/05.`,
  },
  {
    id: 'T14', stage: 3, title: 'Sequential Monte Carlo on valuation and projection; significance',
    out: 'rework/77_smc_valuation_significance.md',
    brief: `TASK T14 (sequential Monte Carlo on the valuation and the projection, and a significance conclusion). The user asked: use quantitative method testing on the valuation and projection to conduct the sequential Monte Carlo for corporate financial modeling, and conclude whether the inferring statistics and the outcome projected are significant or not.
Inputs: rework/screen/project_valuation.py and its results (base: 200,000 cubes a year, contribution THB 4.91, fixed cost THB 500,000, five years, 10%, year 1 at half volume, pre-tax); rework/submission/05 and 06; rework/screen/conversion_synthesis_test.py and conversion_test_power_sim.py (the survey inference); the can-cost model; and the verified earlier records rework/67 to 76 if present (use rework/70 for the volume prior and rework/75 for the tax and cannibalisation structure).
Build rework/screen/smc_valuation.py (numpy, scipy, matplotlib; at most 200,000 particles; under 300 MB; fixed seeds) with:
(A) Prior predictive Monte Carlo of the cash-flow model with a documented prior for every input (price, ex-factory share, each cost line, volume, repeat rate, fixed cost, discount rate, tax, cannibalisation), with correlations where justified (price and volume), each prior tied to a source or labelled ASSUMPTION; output the NPV distribution, P(NPV > 0), mean, median, 5th and 95th percentiles, IRR and payback distributions, with Monte Carlo standard errors.
(B) Sequential Monte Carlo (a bootstrap particle filter that resamples when the effective sample size falls below half, with Liu-West or particle-learning parameter updating) for the latent weekly demand state of the pilot (units per store per week; latent log-demand as a random walk with drift; Poisson or negative binomial observations), mapped to annual volume and NPV at each week of the 13-week pilot. No real data exist, so run it on simulated pilots drawn from three truths (below break-even, base, above) and report: how the posterior P(NPV > 0) evolves week by week; the weeks and stores needed to separate the truths with 80% power; the operating characteristics of the proposed stop and scale rules (3 units per store per week on two reads, repeat floor 15%, contribution THB 3.51): false-scale and false-stop rates; and the value of waiting for the full 13 weeks against stopping early. Recommend the number of stores for Route A at which the rule is statistically meaningful (the team sets it).
(C) Significance conclusions, stated separately and plainly: (i) Is the projected NPV significantly greater than zero under the stated input uncertainty? Fix the test in advance: reject H0 (NPV <= 0) if P(NPV > 0) >= 0.95, and also report the 90% credible interval against zero. (ii) Is the segment lead (men 25 to 34 over 35 to 44) statistically significant? Use the existing ratio and interval and a proper test at the sample the survey can afford. (iii) Are the pilot rule thresholds distinguishable from noise at the planned sample? Say plainly that (i) is conditional on assumed priors and is not a finding from market data, and name what would change the conclusion (the input whose narrowing moves P(NPV > 0) most: a variance-based or rank-correlation sensitivity).
Produce PNG charts in rework/charts/ (smc_npv_distribution.png with P(NPV>0) marked, smc_pilot_posterior_fan.png over pilot weeks, smc_operating_characteristics.png); open each PNG and confirm it is readable. Give a bulleted conclusion and finished slide 10 and slide 11 text.`,
  },
  {
    id: 'T15', stage: 3, title: 'Ambient variation: which existing Singha customer base is most potent',
    out: 'rework/78_ambient_variation_customer_potency.md',
    brief: `TASK T15 (ambient variation: which existing Singha customer base is most potent). The user asked: conduct the ambient variation to identify the more potent existing Singha customer base for the product, and validate before applying them. Reading: a perturbation analysis around the base case in which every segment input is varied across its plausible range, including the ambient seasonal temperature as one factor, to test whether the ranking of customer bases holds.
Inputs: rework/43_singha_consumer_base_semantic.md, 55_consumer_persona_and_acquisition.md, 46_segment_decision.md, 47_statistical_explanation.md, 49_conversion_test_synthesis.md; scripts rework/screen/persona_acquisition_model.py, conversion_synthesis_test.py, conversion_test_power_sim.py; the NSO 2021 extract rework/raw/nso2021_SD10_04_114_extract.md; and the verified earlier records (rework/69, 70, 73 and 79 if present).
Do: (1) Define the candidate existing Singha customer bases from sources, not invention: for example Singha beer drinkers by age and sex band (NSO 2021 drinking prevalence), Singha soda and drinking water buyers, buyers of the Singha Lemon Soda can (the evidence of their profile, or the stated limit that none exists), heavy modern-trade shoppers, and the sugar-reduction pool (Mintel 27%). (2) Define potency as a stated, decomposed quantity: reach (size of the base) times trial propensity (a conversion proxy: top-2-box intent, assumption-based) times repeat propensity times contribution per cube, less the exclusion share (potassium-caution coverage from rework/73 if present; alcohol-cue risk for beer drinkers). (3) Ambient variation: perturb every input within sourced or assumed ranges (uniform or triangular), including the seasonal ambient temperature (Thai Meteorological Department monthly means or another primary source; map to a soft-drink demand seasonality index only if a source supports it, otherwise a stated ASSUMPTION range) and the channel and price context; run at least 20,000 draws; for each base report the median potency, its interval, the probability of ranking first, and the rank stability (Kendall tau between perturbed and base rankings; a tornado of the inputs that flip the ranking). (4) Validate before applying: (a) a split check, re-estimating potency on two disjoint halves of the draws and on two alternative model forms (additive and multiplicative; odds scale and share scale); (b) a leave-one-factor-out run; (c) a placebo (shuffle the segment labels) to show the method does not produce a ranking from noise; (d) a comparison with the earlier segment finding in rework/46 and 47 (men 25 to 34 over 35 to 44, ratio 1.04, interval touching 1). State which findings validate and which do not. (5) Apply only what validates: state the lead segment and the confidence, and which existing customer base is the more potent, or that the ranking is not robust. Give finished slide 5 text. Script: rework/screen/ambient_variation.py with results JSON; chart rework/charts/ambient_potency.png (open it and confirm it is readable).`,
  },
]

const researchPrompt = (t, ctx) =>
  `${COMMON}\n\n${t.brief}\n\nYour output record is ${t.out}. Write it, then return the structured result. List in "figures" at most 25 figures, the ones used in your slide text. List every file you wrote in files_written.${ctx ? `\n\nContext from earlier stages (summaries only; read the records for detail):\n${ctx}` : ''}`

const verifyPrompt = (t, result) =>
  `${COMMON}\n\nYou are the independent verifier for ${t.id} (${t.title}). You did not write this work. Find defects. The task brief was:\n${t.brief}\n\nThe author's structured result (JSON):\n${JSON.stringify(result).slice(0, 24000)}\n\nDo all of this: (1) read the output record ${t.out} and every file in files_written; confirm they exist and are not empty; (2) re-open the source page for every headline figure (at least the ten most important; all of them if fewer) and confirm the figure, the date and the tier, and confirm the saved page under rework/raw/diligence_2026-10-20 matches; (3) rerun every script and compare its results JSON to the figures reported; recompute at least five numbers by hand; (4) look for claims stronger than their source, ranges quoted as points, a total split without a source, a tier upgraded from S to P, a snippet cited as a read page, and results that contradict rework/submission or rework/deck/deck_content.md without being listed as a conflict; (5) check that the work covers what the user asked in the brief, and that any slide text has no em dash, no en dash, no middle dot, no internal note and no decision handed to Singha Corporation. Default to fail when you cannot reproduce a figure. Severity: high = wrong figure, unreproducible result, missing deliverable or fabrication; medium = overstated claim, missing tier or page, gap against the brief; low = style. Return the verdict.`

const revisePrompt = (t, result, verdict) =>
  `${COMMON}\n\n${t.brief}\n\nAn independent verifier found problems in your earlier work. Your earlier structured result (JSON):\n${JSON.stringify(result).slice(0, 16000)}\n\nVerifier issues (fix every high and medium issue; fix low ones if cheap):\n${JSON.stringify(verdict.issues, null, 1).slice(0, 12000)}\n\nFix the files (record ${t.out}, scripts, saved pages), rerun the scripts, and return the full corrected structured result. If a verifier issue is wrong, say so in the record with the evidence and keep your figure.`

async function runTask(t, ctx, phaseName) {
  let result = await agent(researchPrompt(t, ctx), { label: `work:${t.id}`, phase: phaseName, schema: RESULT, model: MODEL })
  if (!result) return { id: t.id, title: t.title, failed: true }
  let verdict = null
  for (let round = 1; round <= MAX_ROUNDS + 1; round++) {
    verdict = await agent(verifyPrompt(t, result), { label: `verify:${t.id}#${round}`, phase: 'Verify', schema: VERDICT, model: reviewModel(t) })
    if (!verdict) break
    const blocking = (verdict.issues || []).filter(i => i.severity !== 'low')
    if (verdict.verdict === 'pass' && blocking.length === 0) return { id: t.id, title: t.title, rounds: round, verdict, result }
    if (round > MAX_ROUNDS) break
    const revised = await agent(revisePrompt(t, result, verdict), { label: `revise:${t.id}#${round}`, phase: 'Verify', schema: RESULT, model: reviewModel(t) })
    if (revised) result = revised
  }
  return { id: t.id, title: t.title, rounds: MAX_ROUNDS + 1, verdict, result }
}

const digest = list =>
  list
    .filter(r => r && r.result)
    .map(r => {
      const x = r.result
      const figs = (x.figures || []).slice(0, 14).map(f => `${f.label} = ${f.value} [${f.tier}]`).join('; ')
      return `### ${r.id} ${r.title}\nSummary: ${x.summary}\nFiles: ${(x.files_written || []).join(', ')}\nKey figures: ${figs}\nLimits: ${(x.limits || []).slice(0, 6).join(' | ')}`
    })
    .join('\n\n')
    .slice(0, 14000)

const compact = r =>
  r.failed
    ? { id: r.id, title: r.title, failed: true }
    : {
        id: r.id,
        title: r.title,
        rounds: r.rounds,
        verdict: r.verdict ? r.verdict.verdict : null,
        open_issues: ((r.verdict && r.verdict.issues) || []).filter(i => i.severity !== 'low'),
        low_issue_count: ((r.verdict && r.verdict.issues) || []).filter(i => i.severity === 'low').length,
        summary: r.result.summary,
        files: r.result.files_written,
        slide_text: r.result.slide_text,
        limits: r.result.limits,
        conflicts: r.result.conflicts || [],
        figures: (r.result.figures || []).slice(0, 20),
      }

const pick = stage => TASKS.filter(t => t.stage === stage && (!ONLY || ONLY.includes(t.id)))

const all = []

phase('Stage 1 research')
const s1 = (await parallel(pick(1).map(t => () => runTask(t, '', 'Stage 1 research')))).filter(Boolean)
all.push(...s1)
log(`Stage 1 done: ${s1.length} tasks`)

phase('Stage 2 derive')
const ctx2 = digest(all)
const s2 = (await parallel(pick(2).map(t => () => runTask(t, ctx2, 'Stage 2 derive')))).filter(Boolean)
all.push(...s2)
log(`Stage 2 done: ${s2.length} tasks`)

phase('Stage 3 model')
const ctx3 = digest(all)
const s3 = (await parallel(pick(3).map(t => () => runTask(t, ctx3, 'Stage 3 model')))).filter(Boolean)
all.push(...s3)
log(`Stage 3 done: ${s3.length} tasks`)

phase('Critic')
const critic = await agent(
  `${COMMON}\n\nYou are the completeness critic. The user's prompt was: slide 3 the gap: check at source for both carbonated soft-drink and bottler markets; do complete due diligence on the competitor; slide 4 leverage the can: complete the verifications to all open points plus deriving the estimated verifications to Singha's internal information; slide 6 the cube in use: model based on the chemistry science to the taste, dissolution time, surface-only upper bound; check and revalidate all product specs; source to check the cover of potassium-retaining medicines or with kidney diseases; slide 10 do the modeling on value accrues; Appendix A: check the sodium; add strategic business unit involvement and stakeholder onion; use quantitative method testing on the valuation and projection to conduct the sequential Monte Carlo for corporate financial modeling and conclude whether the inferring statistics and the outcome projected are significant or not; conduct the ambient variation to identify the more potent existing Singha customer base for the product (validate before applying); do research and survey for a marketing campaign proposal using domestic KOLs; remove all decision hand-over to Singha Corporation and move internal notes to chat (the work must be finished by the team).\n\nSummaries of what the loop produced:\n${digest(all)}\n\nRead the records named in the summaries. List: gaps against the prompt (what was not done or only half done), contradictions between records (same quantity, different values), figures that appear in a slide text but not in a verified record, and the five riskiest claims to re-check. Be specific with file and line.`,
  {
    label: 'critic',
    phase: 'Critic',
    model: MODEL,
    schema: {
      type: 'object',
      properties: {
        gaps: { type: 'array', items: { type: 'string' } },
        contradictions: { type: 'array', items: { type: 'string' } },
        unsupported_slide_figures: { type: 'array', items: { type: 'string' } },
        riskiest_claims: { type: 'array', items: { type: 'string' } },
      },
      required: ['gaps', 'contradictions', 'unsupported_slide_figures', 'riskiest_claims'],
    },
  },
)

return { results: all.map(compact), critic }
