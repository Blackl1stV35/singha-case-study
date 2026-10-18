"""Simulated run of the dye-penetration protocol (rework/33). This is a SIMULATION, not a physical test.

It runs the protocol on virtual wraps using the screen's breach model (rework/31):
  - N_cells per wrap, each damaged with probability f; a damaged cell is a qualifying breach with p_qual
  - a qualifying breach sits on the inner epidermis or the outer epidermis (0.25 each, from leaf anatomy)
  - a wrap leaks if an inner qualifying breach connects to an outer one (closed stomata), or to an open stomatum
  - the dye spot on the outer surface is seen with probability p_detect (assumed)
Controls (protocol section "Controls") are run in the same simulation: positive controls (punctured wraps) must
all show a spot; negative controls (PET film inside) must show none. The pass rule is k = 0 of N.

The result says what the protocol would most likely show for each true breach fraction. It is not a result
for any real wrap. Run:  python lab_sim_dye_protocol.py   (writes lab_sim_dye_protocol_results.json)
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "lab_sim_dye_protocol_results.json")

N_CELLS = 1.72e7        # cells per wrap (rework/30)
P_QUAL = 0.62           # probability that a damaged cell is a qualifying breach (rework/30)
EPI = 0.25              # fraction of breaches on each epidermis (rework/31)
P_DETECT = 0.95         # probability a leaking wrap shows a visible spot (assumed)
N_WRAPS = 300
N_POS = 10              # positive controls (punctured wraps)
N_NEG = 10              # negative controls (PET inside)
FRACTIONS = [1e-9, 1e-8, 1e-7, 3e-7, 1e-6]
RUNS = 2000             # simulated protocol runs per condition


def poisson(lam, rng):
    """Poisson sample (Knuth), for the small and moderate means used here."""
    if lam <= 0:
        return 0
    if lam > 50:
        return max(0, int(round(rng.gauss(lam, math.sqrt(lam)))))
    L = math.exp(-lam)
    k, p = 0, 1.0
    while True:
        k += 1
        p *= rng.random()
        if p <= L:
            return k - 1


def wrap_leaks(f, stomata_open, rng):
    lam = N_CELLS * f * P_QUAL
    n_in = poisson(EPI * lam, rng)
    if stomata_open:
        return n_in > 0                         # outer surface connected through open stomata
    n_out = poisson(EPI * lam, rng)
    return n_in > 0 and n_out > 0


def run_protocol(f, stomata_open, rng):
    """One simulated protocol run: returns (k observed, pass, controls valid)."""
    leaks = sum(1 for _ in range(N_WRAPS) if wrap_leaks(f, stomata_open, rng))
    k = sum(1 for _ in range(leaks) if rng.random() < P_DETECT)
    pos_ok = all(rng.random() < 1.0 for _ in range(N_POS))  # punctures always produce a spot in this simulation
    neg_ok = True                                            # PET inside: no inner breach, no spot
    controls_valid = pos_ok and neg_ok
    return k, (k == 0) and controls_valid, controls_valid


def main():
    rng = random.Random(20261018)
    results = {"simulation": True,
               "statement": "Simulated run of rework/33 with the screen's breach model. Not a physical measurement.",
               "protocol": {"wraps": N_WRAPS, "positive_controls": N_POS, "negative_controls": N_NEG,
                            "pass_rule": "k = 0 of 300 with controls valid", "p_detect": P_DETECT,
                            "runs_per_condition": RUNS},
               "conditions": {}}
    for stomata_open in (False, True):
        key = "stomata open" if stomata_open else "stomata closed"
        results["conditions"][key] = {}
        for f in FRACTIONS:
            passes, ks = 0, []
            for _ in range(RUNS):
                k, ok, _ = run_protocol(f, stomata_open, rng)
                ks.append(k)
                passes += int(ok)
            ks.sort()
            results["conditions"][key]["f=%.0e" % f] = {
                "pass_probability": round(passes / RUNS, 4),
                "median_k": ks[len(ks) // 2],
                "p95_k": ks[int(0.95 * len(ks))],
                "mean_k": round(sum(ks) / len(ks), 2),
            }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    print("SIMULATED dye-penetration run (rework/33), 300 wraps, pass if k = 0")
    for key, rows in results["conditions"].items():
        print(key)
        for f, r in rows.items():
            print("  %-10s pass probability %5.1f %%  median k %3d  95th percentile k %3d" % (
                f, 100 * r["pass_probability"], r["median_k"], r["p95_k"]))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
