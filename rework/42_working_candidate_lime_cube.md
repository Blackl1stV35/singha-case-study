# Working candidate: Lime Soda Cube (18 October 2026)

> **Superseded 18 October 2026** by the sodium-free potassium-bicarbonate cube ([rework/45](45_working_candidate_rework.md)). Kept as the record of the frozen pour-over route.

Status: research complete on five tracks (novelty, base product, food science and physics, Thai regulation, alternative-format fit), with verification checks and a completeness critic. The screen is reproducible: [screen/lime_cube_screen.py](screen/lime_cube_screen.py), results in [screen/lime_cube_screen_results.json](screen/lime_cube_screen_results.json). Raw track output is in the workflow journal (wf_020c4cb1-0a2) and is not copied into the repo.

Scope: Thailand domestic only. Public information only. No outside party is contacted. The consumer-base map (gate E) is a separate workflow and is still running.

**Verdict: not validated as briefed.** The candidate fails the brief's "never existed before" test on the evidence found, and the fizz cannot be claimed for a frozen cube. The one version that survives the physics is a narrower pour-over product, which does not cover the Ingredients and Nutrition axis.

## 1. What the candidate is

- **Base product (public, dated):** Singha Sparkling Water Lime Flavour, a 330 ml can, sugar-free, 0% calorie profile, announced in March 2026 at 15 baht at 7-Eleven. Public name differs from the team brief's "Singha Lime Soda", which was not found as a Singha product.
- **Working format:** a frozen cube of the same liquid (about 25 g), poured over carbonated water. This is the route the physics and format tracks model.
- **Route not yet fixed.** The novelty track read "resolvable" as a dissolvable cube (effervescent or freeze-dried). The physics and format tracks read it as a frozen cube. This document uses the frozen pour-over route. The other two readings have no regulatory or cost work.

## 2. Gate verdicts

| Gate | Question | Result | Status |
|---|---|---|---|
| A | Novelty as briefed ("never existed before") | Frozen lime and citrus cubes are sold abroad (Frecco, UK, 2006; Zhero, Italy, undated, unverified). Dissolvable drink cubes exist (1,2,CUBE, Japan, 2021; Waterdrop, EU). Frozen carbonated soda is established abroad. No Thai packaged cube was found, but Thai retailer pages were unreadable | **Fails as briefed.** Narrower Thai-shelf claim is provisional only |
| B | Carbonation kept in the cube | The base case retains 0% of the can's CO₂ on freezing (2.27 g per 330 ml at 3.5 volumes, 4 °C). Sensitivity runs keep at most 1%. No sourced value for CO₂ in ice at 1 atm exists. CO₂ survives only in a pour-over, and the drink ends about 1.7 volumes above saturation, so it degasses in an open glass | **Fails for a fizz claim in the cube.** A pour-over version can be tested |
| C | Thai classification and labelling | Edible ice under Notification 463 (2568), or a sealed beverage under 356 or 469, is not settled. If it is ice, the label must read "Ice for Consumption" and drink-style statements are barred (cl. 6(2) and 7, as reported by the regulation track). Sugar-free wording requires under 0.5 g per reference serving | **Limit.** A Thai adviser must decide |
| D | Alternative Formats and the three-axis fit | The cube adds form only. Ingredients and Nutrition is not met by a sugar-free lime soda. Thai drinkers already use ice in drinks, so the form is not a new consumption act | **Weak; not presentable yet** |
| E | Consumer base | Semantic map of public Singha consumers is running. No cube-specific evidence exists | **Pending** |
| F | Cost | No cost for the tray, freezing, the −18 °C chain, margin or price against the 15 baht can | **Limit.** No figure exists |
| G | Timeline | Registration closes 22 October 2026 at 23:59. About four days remain | **Tight.** A 24-hour freeze, two physical tests and the adviser question do not fit |

## 3. Key numbers (screen, all assumption-dependent)

- CO₂ in a 330 ml can at 3.5 volumes and 4 °C: 2.27 g. In a 25 g cube: 0.172 g (about 87.5 mL at STP), if fully retained.
- Ice-to-liquid partition ratio k_ice of 10⁻⁴, 10⁻³ and 10⁻² retains 0.01%, 0.1% and 1% of the can's CO₂. k_ice is an assumption; no sourced value exists.
- Pour-over with two cubes in 280 ml of carbonated water at 4 °C retains about 85% of the can's CO₂ right after mixing, then degasses.
- Melt time of a 25 g cube in 250 ml of soda at 25 °C: 4.8 to 15.8 minutes at h = 300 W/(m²·K). The h range of 100 to 900 gives 5 to 47 minutes. h is the most sensitive input and must be measured.
- Dilution after full melt: 9.1% by mass. Flavour strength with two cubes is about 15% of the can's concentration, if the cube carries the drink's solutes. If the cube is pure ice, flavour is lower still.

## 4. Critic findings that bind the decision

- **Route, mapping and identity are undefined.** No track states how many cubes equal one can, whether the cube is a concentrate, or what a serving is. The name, the lime-or-lemon aroma and the "no sweetness" wording conflict across sources.
- **CO₂ level is not stated** on any Singha launch page. The 3.5 volumes used in the screen is a generic soft-drink range, not the product's level.
- **Sweetener, ingredients, pH and Thai registration number** are not read. The can label was not read. Reading it needs a purchase, which is outside the no-contact plan unless you approve it.
- **Sources are thin.** Most claims about the product trace to three March 2026 reprints of one company release. Retailer shelf checks failed (Lazada and Shopee empty, Makro 404, Tops 403).
- **Contradictions to correct:** the sugar-free rule in the C3 note (0.5 g per 100 ml) is wrong; the Notification 463 "Thai original not reached" item is stale, since the Thai text was read on the same FDA page; the Frecco "2013" product was not read.
- **Fallback not lower-risk:** the Freeze-Fizz Can fallback fails the same novelty test, because frozen carbonated soda already exists abroad.
- **No go/no-go threshold** is stated for fizz after thaw, flavour or consumer response.

## 5. Decisions taken (per recommendation; reviewable)

| # | Decision | Reason | Reopen if |
|---|---|---|---|
| L1 | Do not enter the Lime Soda Cube as a "never existed before" product | Gate A fails on the abroad precedents | A Thai and patent search finds no precedent, which the no-contact plan cannot close |
| L2 | If kept, the route is a frozen pour-over cube, not a dissolvable or sealed frozen can | Only this route has physics and regulatory work; the others have none | The team picks another route, which then needs its own tests |
| L3 | No carbonation or "fizz" claim is made for the cube | Gate B fails for the cube | A physical test measures CO₂ retained in the cube |
| L4 | Use the public name "Singha Sparkling Water Lime Flavour" in all material | "Singha Lime Soda" is not a found product name | The team confirms a different product |
| L5 | No "0% calorie" or "no sweetness" wording until the label is read | Sources disagree; a sweetener is present in the lemon line | The label is read |
| L6 | Regulation gate C is closed as a limit. The conservative design is to label as edible ice, with no drink-style statements | An adviser is needed, and no adviser contact is in the plan | An adviser answers |
| L7 | Gate F (cost) and gate E (consumer test) are closed as limits for this entry | No quote is in the no-contact plan, and recruiting a panel would be outside contact | The team authorises outside steps |
| L8 | Do not change the entry recommendation in rework/06 yet | The team's confirmed choice is still pending from you | You confirm the choice |

## 6. Work plan (no outside contact)

1. **Read the can label** (needs your approval to buy one can). Settles identity, sweetener, CO₂ volume if stated, lemon or lime aroma and the Thai registration number. Closed as a limit if not approved.
2. **Define the serving** (desk). Decide whether the cube is a concentrate, and how many cubes equal one 330 ml can. The screen's two-cube, 280 ml case is the starting point.
3. **Physical bench test** (needs your approval; in-house only). Freeze three lots at −18 °C for 24 hours. Measure CO₂ released by sealed melting, open-glass CO₂ over time for the pour-over, and melt time with a thermocouple to calibrate h. Pass rule to be set before the run.
4. **Regulatory classification** (closed as a limit). Note in the pack plan that edible-ice labelling applies until an adviser says otherwise.
5. **Consumer evidence** (desk only). Use the semantic consumer-base map when it reports. A panel of outside respondents is a contact step and is closed as a limit.
6. **Go or no-go before 22 October 2026.** The default is "not validated" unless the bench test shows retained CO₂ in the pour-over and the label supports the serving.

## 7. Limits

- Model outputs, not measurements. Every CO₂ and melt figure depends on assumed k_ice, pocket retention and h.
- The base product is known from launch releases only. No shelf, label or current-listing check was possible for Lazada, Shopee, Makro or Tops.
- Patent search used Google Patents only. Espacenet (Thailand filter) and the Thailand DIP database were not searched.
- The 7-Eleven Thailand frozen range was not checked directly. The freezer-price evidence comes from a single blog.
- Cost, distribution and cold-chain economics are none.
