# Results file scope check and finer directional rerun

- Item: V5 revision. Date: 20 October 2026. This is a read of the repo's own results file plus a rerun of the repo model. Nothing was written to rework/screen.
- File read: rework/screen/ambient_variation_results.json (seed 20261020, 40,000 draws, modified 20 October 2026 06:43). Script read: rework/screen/ambient_variation.py, lines 605 to 770 for the run definitions.
- Method for the scope check: a script walked every run stored under each of the four lenses (model forms, leave-one-factor-out, months, season stress, structural sweeps, coverage-weight sweep, reverse-stress runs, directional scenarios, directional by month) and listed each run whose modal leader differs from the lens leader. Python -I, read-only.

## 1. Every run in the file whose leader differs from the lens leader

| Lens | Full-run leader (probability, file confidence) | Runs with a different leader | Temperature or not |
|---|---|---|---|
| Reach | men 45 to 59 (0.6808, none) | sex_gradient_off (leader first 0.4043), alcohol_cue_20 (0.4313), drinking_2021_cells (0.3254), bottled_habit_counted_once (0.4379); in all four the modal base is sweet-bottled drinkers 25 to 44 (SB25) | all four are structural, none is temperature |
| Per person, drinkers only | men 25 to 34 (0.9405, moderate) | directional scenarios only: April at delta 0.04 (men 25 to 34 first 0.2826) and 0.05 (0.128); by month at delta 0.05, April (0.128) and May (0.3051); the leader becomes men 35 to 44 | temperature only |
| Per person, all eight bases | men 25 to 34 (0.9405, moderate) | the same four runs, same figures | temperature only |
| Per member | men 25 to 34 (0.8156, none) | structural: sex_gradient_off (men 25 to 34 first 0.0674), alcohol_cue_20 (0.2069), bottled_habit_counted_once (0.1867), modal base SB25; temperature: April at delta 0.04 (0.2148) and 0.05 (0.1003), May at delta 0.05 (0.244), modal base men 35 to 44 | both |

- Runs that change no leader on any lens: the three other model forms, the 23 leave-one-factor-out runs, the 12 months, the season stress run (beta up to 0.15), the four coverage-weight runs, the structural sweeps not named for that lens in the table, and the four reverse-stress runs (beta up to 0.3, 0.45, 0.6 and 1.0 with independent draws).
- The file's flag leader_unchanged_in_every_run is true for the two per-person lenses and false for reach and per member. The flag covers the 55 counted runs (run_counts) and does not include the directional scenarios or the reverse-stress runs, so a per-person flag of true does not mean the directional scenarios leave the leader unchanged.
- The reach lens also lists one tornado input that flips its top base between the lowest and highest fifth: sweet-bottled share, 25 to 44 (2021). That is not a run and not a temperature input.
- Definition of the directional scenario (script lines 639 to 659): men 25 to 34 are fixed at a heat sensitivity of 0, men 35 to 44 and men 45 to 59 are both fixed at delta per degree Celsius, and the other six bases keep their independent draws from 0 to 0.05. The scenario is run for April (30.7 C) and for the twelve-month mixture, with deltas 0, 0.01, 0.02, 0.03, 0.04 and 0.05; month by month only for 0.03 and 0.05.
- In the twelve-month mixture no delta up to 0.05 changes any leader. At delta 0.03, no month changes any leader.

## 2. Finer rerun of the directional scenario (DERIVED, not in the results file)

- The file's grid steps by 0.01, so "0.04" is only the first grid point at which the leader differs. The rerun uses the repo functions (av.run, av.sum_all) with the file's own seed and settings and the same fixed sensitivities.
- Reproduction check: April at delta 0, 0.03, 0.04 and 0.05 reproduces the file's figures to four decimals (per person men 25 to 34 first: 0.9734, 0.5052, 0.2826, 0.128; per member: 0.6718, 0.3711, 0.2148, 0.1003; reach leader men 45 to 59 at 0.6131, 0.7511, 0.7865, 0.8151).
- April, probability that each base is first (per person, drinkers only and all eight bases give the same numbers for these two bases):

| Delta | Men 25 to 34 first | Men 35 to 44 first | Leader |
|---|---|---|---|
| 0 | 0.9734 | 0.0259 | men 25 to 34 |
| 0.030 | 0.5052 | 0.4894 | men 25 to 34 |
| 0.031 | 0.4808 | 0.5135 | men 35 to 44 |
| 0.035 | 0.3899 | 0.6036 | men 35 to 44 |
| 0.040 | 0.2826 | 0.7099 | men 35 to 44 |
| 0.050 | 0.1280 | 0.8629 | men 35 to 44 |

- Per member, April: men 25 to 34 / men 35 to 44 first is 0.3711 / 0.3545 at delta 0.030 (men 25 to 34 lead) and 0.3540 / 0.3747 at 0.031 (men 35 to 44 lead). So for both per-person and per-member lenses the April crossing lies between 0.030 and 0.031 per degree Celsius.
- Month by month at delta 0.04 and at 0.045: the leader changes to men 35 to 44 in April and May only. March and June are still men 25 to 34 (per person 0.7761 at 0.04, 0.7315 at 0.045); the remaining eight months are 0.92 or higher per person. The reach leader stays men 45 to 59 in every month.
- Raw output: directional_fine_rerun_output.json in this folder (37 runs; each entry holds the modal base and the probability that each base is first, for the four lenses).

### Script (kept outside the repo; it was run with python -B -I so no bytecode was written into rework/screen)

```python
import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, r"D:\Workspace\singha-case-study\rework\screen")
import ambient_variation as av
av.load_coverage()
A0 = av.potency(av.central(1), av.PRIMARY)
LENS = ["reach", "per_cell_drinkers", "per_cell_all", "per_member"]

def one(delta, tm):
    fx = {"beta_M25": 0.0, "beta_M35": delta, "beta_M45": delta}
    _, oo = av.run(av.PRIMARY, fixed=fx, month=tm)
    r = av.sum_all(oo, A0)
    return {l: (r[l]["modal_top"], r[l]["prob_rank_first"]) for l in LENS}

out = {}
for delta in (0.0, 0.03, 0.04, 0.05):
    out["apr_%g" % delta] = one(delta, 30.7)
for delta in (0.031, 0.032, 0.033, 0.034, 0.035, 0.036, 0.037, 0.038, 0.039):
    out["apr_%g" % delta] = one(delta, 30.7)
for delta in (0.04, 0.045):
    for name, tm in zip(av.TMD_NAMES, av.TMD):
        out["m_%g_%s" % (delta, name)] = one(delta, tm)
json.dump(out, open(sys.argv[1], "w"), indent=1)
```

## 3. What this does and does not change

- The sourced temperature values are common to all bases or unknown by base, so they do not create a difference between men 25 to 34 and older men. Nothing sourced reaches the delta of about 0.031 that the directional scenario needs, and that scenario also fixes men 25 to 34 at exactly zero heat response. The conclusion that a sourced temperature value changes no leader stands.
- The reach and per-member leaders are separately fragile to non-temperature inputs (table in section 1). That fragility is in the file already and is unrelated to temperature.
- The threshold in rework/78 section 7.6 ("about 0.04 per degree Celsius or more") is the first grid point. The April crossing in this rerun is about 0.031. This record does not edit rework/78; the parent decides.
