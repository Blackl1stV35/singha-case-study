"""Charts for the thaw, leak and quantum-check results already in rework/screen.

Reads the JSON outputs of pop_leak_simulation.py and quantum_leak_probability.py and writes one PNG.
Run:  python make_results_charts.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, "pop_leak_simulation_results.json")
QPU = os.path.join(HERE, "quantum_leak_probability_results.json")
OUT = os.path.join(HERE, "..", "19_results_charts.png")
WINDOW_H = 2.0

with open(SIM, encoding="utf-8") as fh:
    sim = json.load(fh)
with open(QPU, encoding="utf-8") as fh:
    qpu = json.load(fh)

nom = sim["nominal_h10"]
t_wet = nom["N8"]["t_wet_s"] / 3600.0
t50 = nom["N8"]["t50_s"] / 3600.0
t100 = nom["N8"]["t100_s"] / 3600.0
mc = sim["monte_carlo"]
scan = mc["design_B_leak_probability_vs_damaged_radius"]
r_um = [row["r_d_m"] * 1e6 for row in scan]
p_leak = [row["P_leak"] for row in scan]
r_star_med_um = mc["design_B_critical_damaged_radius_m"]["median"] * 1e6

fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))

# Panel 1: thaw timeline at 30 C
ax = axes[0]
ax.barh([0], [t100], color="#c7e3f5", edgecolor="#185FA5", height=0.5, label="frozen to full thaw")
ax.barh([0], [t50], color="#85B7EB", edgecolor="#185FA5", height=0.5, label="to 50% (sippable)")
ax.axvline(WINDOW_H, color="#993C1D", ls="--", label="2 h test window")
ax.scatter([t_wet], [0], color="#27500A", zorder=3, s=60, label="surface starts to melt")
ax.annotate("%.2f h" % t_wet, (t_wet, 0), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=9)
ax.annotate("50%%: %.2f h" % t50, (t50, 0), textcoords="offset points", xytext=(0, -22), ha="center", fontsize=9)
ax.annotate("100%%: %.2f h" % t100, (t100, 0), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=9)
ax.set_yticks([])
ax.set_xlabel("time at 30 C (h)")
ax.set_xlim(0, 3.8)
ax.set_title("Nominal thaw (h = 10 W/m2K, 8-node grid)")
ax.legend(fontsize=7, loc="lower right")

# Panel 2: leak probability for the sealed-edge design vs damaged-path radius
ax = axes[1]
ax.semilogx(r_um, p_leak, "o-", color="#185FA5", label="sealed edges, damaged paths (design B)")
ax.axhline(1.0, color="#993C1D", ls=":", label="exposed edges (design A): 100% of runs leak")
ax.axvline(r_star_med_um, color="#27500A", ls="--", label="median critical radius %.2f um" % r_star_med_um)
ax.axvspan(0.001, 0.0016, color="#c7e3f5", alpha=0.6, label="intact cuticle pores (0.3 to 2 nm)")
ax.set_xlabel("damaged-path radius (um)")
ax.set_ylabel("P(leak within 2 h)")
ax.set_xlim(0.001, 15)
ax.set_ylim(-0.05, 1.08)
ax.set_title("Leak probability (200 Monte Carlo runs)")
ax.legend(fontsize=7, loc="lower right")

# Panel 3: quantum sampling check vs classical value
ax = axes[2]
p_c = qpu["p_classical"]
p_q = qpu["p_quantum_estimate"]
se = qpu["shot_standard_error"]
ax.bar(["classical\n(Monte Carlo)", "IBM ibm_fez\n(1000 shots)"], [p_c, p_q], color=["#85B7EB", "#EF9F27"],
       edgecolor="#333", width=0.5)
ax.errorbar([1], [p_q], yerr=[se], fmt="none", ecolor="#333", capsize=6)
ax.axhline(p_c, color="#185FA5", ls=":", lw=1)
ax.set_ylim(0, 1)
ax.set_ylabel("P(leak), design B at 0.3 um")
ax.set_title("Quantum sampling check: %.3f vs %.3f" % (p_q, p_c))
ax.text(1, p_q + 0.07, "difference %.3f (%.1f shot errors)" % (p_q - p_c, qpu["difference_in_standard_errors"] * -1),
        ha="center", fontsize=8)

fig.suptitle("Leaf-wrapped frozen pop: thaw, leak and quantum-check results (virtual screen, not measurements)",
             fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(OUT, dpi=130)
print("wrote", os.path.abspath(OUT))
