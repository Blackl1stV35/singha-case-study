# PET inner pouch: food-contact compliance and migration (18 October 2026)

Status: limits verified from the Thai notification text; migration estimated by physics (`rework/screen/pet_migration.py`, results `pet_migration_results.json`). Not a compliance certificate. A migration test on the actual pouch and drink is still needed, and it is a physical test that needs your approval.

## 1. Limits that apply (verified)

Thai MoPH Notification No. 435 (B.E. 2565) on plastic food packaging, in force from 18 June 2022 (Clause 14). Source: FDA translation and Thai text, `food.fda.moph.go.th`.

| Item | Limit | Where in the notification | Status |
|---|---|---|---|
| Overall migration, PET | 10 mg/dm² of food-contact surface | Annex 1, Table 1, item 6 | verified |
| Antimony | 0.04 mg/kg | Annex 1, Table 2, item 11 (applies to all plastics) | verified |
| Acetaldehyde | 6 mg/kg | Annex 1, Table 4, section 4.7, item 1 | verified |
| Ethylene glycol | 30 mg/kg | Table 4, section 4.7, item 12 | verified |
| Diethylene glycol | 30 mg/kg | Table 4, section 4.7, item 5 | verified |
| Terephthalic acid | 7.5 mg/kg | Table 4, section 4.7, item 24 (basis corrected by erratum, 27 Oct 2022) | verified |
| 2-aminobenzamide | 0.05 mg/kg | Table 3.2, item 4 | verified; PET applicability unclear in the Thai layout |
| PET oligomers | **no limit** | none in Thai Table 2, Table 4 or Tables 3.1 and 3.2 | verified absence; overall migration governs |

The EU Regulation (EU) No 10/2011 gives the same values for the group restrictions, and the EU limits also give simulant and test rules. The EU rules were used as a cross-check, not as the governing source for Thailand.

## 2. Migration estimate (physics)

Sink-condition diffusion from a 25 µm PET film into a 170 mL serving (0.02 m² pouch), over the 2 h thawed contact. Frozen storage gives a slowdown of about 1000 times, so it adds almost nothing.

| Substance | Migration over 2 h | Limit | Margin |
|---|---|---|---|
| PET oligomers, overall migration (assumed residual 1 % w/w) | 0.13 mg/dm² | 10 mg/dm² | about 76× |
| Acetaldehyde (assumed residual 10 mg/kg) | 0.05 mg/kg food | 6 mg/kg | about 122× |
| Ethylene glycol (assumed residual 1000 mg/kg) | 1.6 mg/kg food | 30 mg/kg | about 19× |
| Antimony, if all residual leaches | 1.2 mg/kg food | 0.04 mg/kg | fails |

**Correction.** An earlier draft gave the overall migration as 1.32 mg/dm². That was a units error (13.2 mg/m² is 0.132 mg/dm²). The margin is about 76×, not 7.6×.

**Antimony is the constraint.** Its catalyst residue is 300 mg/kg in the worst assumed case, which puts 0.21 mg of antimony in each pouch. To stay below 0.04 mg/kg in the food, less than about 3.3 % of that antimony may leach in two hours. Antimony leaches by surface processes, so this is a real risk, not a diffusion calculation. **Decision: specify antimony-free PET** (titanium- or germanium-catalysed), which removes the question.

## 3. Fat content (open, with a bound)

The EU rules apply a fat-food correction above 20 % fat and use an olive-oil simulant for fatty foods. Canned coconut milk is fat-rich, so a coconut-based drink could exceed 20 %. Migration into fat is higher for lipophilic substances. The overall-migration margin of about 76× therefore holds only if migration into the drink rises by less than about 76 times. For a fatty drink this is an open check, and the fat content must be measured. The drink's fat content is not yet specified.

## 4. What the Thai notification does not give

- **No test conditions, simulants or uncertainty rules.** The EU rules supply these, and their 2-hour and frozen-storage conditions were used only as a reading, not as a regulatory mapping.
- **No declaration of compliance clause.** The EU requires a written declaration by the business operator. The Thai text read has documentation duties (Clause 7) but no equivalent declaration.
- **Transition.** Packaging made to the former standards may be used for up to three years from entry into force (Clauses 12 and 13), which does not affect a new pouch.

## 5. Checks still open

- **Notification 92 (B.E. 2528)** on general food containers: its English text is image-only and could not be read. It may overlap with Notification 435.
- **Thai errata (21 July 2025):** the Thai text was garbled; the English translation was used.
- **A secondary source** says PET specific limits apply from 19 June 2025. This was not verified and conflicts with the 2022 date.
- **A draft revision** to Notification 435 (16 September 2026, comments due later) is reported by a secondary source. It must be checked before launch, since limits may change.
- **Thai industrial standards** TIS 655 and TIS 2493 are reported from a 2022 news article only.
- **EU simulant rows** (Annex III, Table 3) need confirmation against the Official Journal before any test design uses them.

## 6. Decisions

1. **Pouch material: PET, food-contact grade for water and beverage contact, antimony-free catalyst.**
2. **Compliance route: supplier documentation for the PET grade, the Thai Clause 7 dossier, and a migration test on the finished pouch and drink.** The test is a physical lab test and needs your approval before it runs. I have not run it.
3. **Fat content measured before the test design is fixed.** If the drink is above 20 % fat, the test uses a fatty simulant.
4. **No claim of compliance** until the migration test has run and the revision check is done.

## 7. Limits

- The migration numbers are physics estimates with assumed residuals and a sink condition. They are not measurements.
- The Thai notification is verified; the open checks in section 5 may change the limits or the procedure.
- This note is not legal advice. A Thai registration adviser must confirm the route.
