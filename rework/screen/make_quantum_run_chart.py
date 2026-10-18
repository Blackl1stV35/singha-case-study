"""Chart of the last IBM quantum run (one-qubit sampling check, rework/18).

Reads quantum_leak_probability_results.json and writes rework/19_quantum_last_run.png.
Run:  python make_quantum_run_chart.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT = os.path.join(HERE, "quantum_leak_probability_results.json")
OUT = os.path.join(HERE, "..", "19_quantum_last_run.png")

with open(RESULT, encoding="utf-8") as fh:
    run = json.load(fh)

shots = run["shots"]
counts = run["counts"]
n0, n1 = counts.get("0", 0), counts.get("1", 0)
p_c = run["p_classical"]
p_q = run["p_quantum_estimate"]
se = run["shot_standard_error"]
diff = run["difference"]
sig = run["difference_in_standard_errors"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1, 1.2]})

# Panel 1: measured counts on the IBM backend
bars = ax1.bar(["|0>", "|1>"], [n0, n1], color=["#85B7EB", "#EF9F27"], edgecolor="#333", width=0.5)
for bar, n in zip(bars, [n0, n1]):
    ax1.text(bar.get_x() + bar.get_width() / 2, n + 12, "%d (%.1f%%)" % (n, 100.0 * n / shots),
             ha="center", fontsize=10)
ax1.set_ylim(0, max(n0, n1) * 1.18)
ax1.set_ylabel("shots out of %d" % shots)
ax1.set_title("Measured outcomes on %s" % run["backend"])

# Panel 2: classical target vs quantum estimate
ax2.bar(["classical\n(Monte Carlo target)", "IBM hardware\n(%d shots)" % shots], [p_c, p_q],
        color=["#85B7EB", "#EF9F27"], edgecolor="#333", width=0.5)
ax2.errorbar([1], [p_q], yerr=[se], fmt="none", ecolor="#333", capsize=7, lw=1.4)
ax2.axhline(p_c, color="#185FA5", ls=":", lw=1)
ax2.set_ylim(0, 1)
ax2.set_ylabel("P(leak), design B at 0.3 um")
ax2.set_title("Quantum estimate vs classical value")
ax2.text(1, p_q + 0.09, "%.3f +/- %.3f (shot error)" % (p_q, se), ha="center", fontsize=9)
ax2.text(0.5, 0.06, "difference %.3f = %.1f shot errors low" % (diff, -sig), ha="center", fontsize=9,
         transform=ax2.transAxes)

fig.suptitle("Last IBM quantum run: job %s" % run["job_id"], fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(OUT, dpi=130)
print("wrote", os.path.abspath(OUT))
