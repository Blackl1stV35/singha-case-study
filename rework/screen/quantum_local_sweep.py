"""Local quantum simulation sweep for the design B leak probability. No IBM runtime is used.

Amplitude estimation (maximum likelihood) with Grover powers k = 0..5 (oracle calls 2k+1),
shot counts 250 to 4000 per circuit, 30 repetitions each, on two local simulators:
  noiseless   AerSimulator
  noisy       AerSimulator with the noise model of a fake IBM backend (fake_fez if present)
Reference: classical Bernoulli Monte Carlo at the same oracle budget.

Writes quantum_local_sweep_results.json and rework/21_local_quantum_sweep.png.
Run:  python quantum_local_sweep.py
"""
import json
import math
import os

import numpy as np

from quantum_amplitude_estimation import build_circuit, theta_of  # circuit builder only, no IBM calls

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "quantum_local_sweep_results.json")
OUT_PNG = os.path.join(HERE, "..", "21_local_quantum_sweep.png")
P_TARGET = 0.715
K_LIST = [0, 1, 2, 3, 4, 5]
SHOT_LIST = [250, 500, 1000, 2000, 4000]
REPS = 30
ORACLE_UNITS = sum(2 * k + 1 for k in K_LIST)  # 36 A-applications per shot across all circuits


def mlae_general(ones, shots, powers):
    """Maximum-likelihood amplitude estimate and its Fisher-information standard error."""
    grid = np.linspace(1e-7, math.pi / 2 - 1e-7, 200001)
    loglik = np.zeros_like(grid)
    for k, h in zip(powers, ones):
        P = np.clip(np.sin((2 * k + 1) * grid) ** 2, 1e-12, 1 - 1e-12)
        loglik += h * np.log(P) + (shots - h) * np.log(1 - P)
    th = float(grid[int(np.argmax(loglik))])
    fisher = 0.0
    for k in powers:
        m = 2 * k + 1
        P = math.sin(m * th) ** 2
        dP = m * math.sin(2 * m * th)
        fisher += shots * dP * dP / max(P * (1 - P), 1e-12)
    return math.sin(th) ** 2, abs(math.sin(2 * th)) / math.sqrt(fisher)


def run_counts(sim, circuits, shots, seed):
    res = sim.run(circuits, shots=shots, seed_simulator=seed).result()
    return [res.get_counts(i) for i in range(len(circuits))]


def make_chart(payload):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = payload["rows"]
    theta = theta_of(P_TARGET)
    colors = {"classical": "#85B7EB", "noiseless": "#185FA5", "noisy": "#EF9F27"}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))

    # Panel 1: standard error vs oracle budget
    ax = axes[0]
    budgets = np.array(sorted({r["budget"] for r in rows}))
    cls = [r for r in rows if r["mode"] == "classical"]
    ax.loglog(budgets, np.sqrt(P_TARGET * (1 - P_TARGET) / budgets), color=colors["classical"], lw=1,
              label="classical, theory ~1/sqrt(N)")
    ax.loglog([r["budget"] for r in cls], [r["std"] for r in cls], "o", color=colors["classical"],
              label="classical, measured")
    for mode in ("noiseless", "noisy"):
        mr = [r for r in rows if r["mode"] == mode]
        ax.loglog([r["budget"] for r in mr], [r["std"] for r in mr], "o", color=colors[mode],
                  label="QAE %s, measured" % mode)
        ax.loglog([r["budget"] for r in mr], [r["theory_sigma_mean"] for r in mr], "--", color=colors[mode],
                  lw=1, label="QAE %s, Fisher theory" % mode)
    ax.set_xlabel("oracle calls N")
    ax.set_ylabel("standard error of P")
    ax.set_title("Error vs oracle budget (%d repetitions)" % payload["REPS"])
    ax.legend(fontsize=7)

    # Panel 2: outcome probability per Grover power at the largest shot count
    ax = axes[1]
    kk = np.linspace(0, max(K_LIST), 300)
    ax.plot(kk, np.sin((2 * kk + 1) * theta) ** 2, color="#333", lw=1, label="ideal sin^2((2k+1) theta)")
    for mode in ("noiseless", "noisy"):
        g = payload["grid"].get(mode)
        if not g:
            continue
        y = [h / payload["grid_shots"] for h in g["ones_by_k"]]
        err = [math.sqrt(max(v * (1 - v), 1e-9) / payload["grid_shots"]) for v in y]
        ax.errorbar(K_LIST, y, yerr=err, fmt="o", color=colors[mode], capsize=3, label=mode)
    ax.set_xlabel("Grover power k (oracle calls 2k+1)")
    ax.set_ylabel("P(|1>)")
    ax.set_title("Outcome probability at %d shots" % payload["grid_shots"])
    ax.legend(fontsize=8)

    # Panel 3: bias of the estimate vs budget
    ax = axes[2]
    for mode in ("noiseless", "noisy"):
        mr = [r for r in rows if r["mode"] == mode]
        ax.errorbar([r["budget"] for r in mr], [r["bias"] for r in mr],
                    yerr=[r["std"] / math.sqrt(payload["REPS"]) for r in mr], fmt="o-", color=colors[mode],
                    capsize=3, label=mode)
    ax.axhline(0, color="#333", lw=1, ls=":")
    ax.set_xscale("log")
    ax.set_xlabel("oracle calls N")
    ax.set_ylabel("mean estimate minus target 0.715")
    ax.set_title("Bias vs budget (bars: std. error of mean)")
    ax.legend(fontsize=8)

    fig.suptitle("Local quantum simulation sweep, design B leak probability (no IBM hardware used)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT_PNG, dpi=130)
    print("wrote", os.path.abspath(OUT_PNG))


def main():
    from qiskit_aer import AerSimulator
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2

    theta = theta_of(P_TARGET)
    circuits = [build_circuit(theta, k) for k in K_LIST]

    ideal = AerSimulator()
    provider = FakeProviderForBackendV2()
    names = [b.name for b in provider.backends()]
    fake_name = "fake_fez" if "fake_fez" in names else ("fake_brisbane" if "fake_brisbane" in names else names[0])
    fake = next(b for b in provider.backends() if b.name == fake_name)
    noisy_sim = AerSimulator.from_backend(fake)
    pm = generate_preset_pass_manager(optimization_level=1, backend=noisy_sim)
    noisy_circuits = [pm.run(c) for c in circuits]
    modes = {"noiseless": (ideal, circuits), "noisy": (noisy_sim, noisy_circuits)}

    rows = []
    grid = {}
    grid_shots = SHOT_LIST[-1]
    rng = np.random.default_rng(20261018)
    for shots in SHOT_LIST:
        budget = shots * ORACLE_UNITS
        cls = rng.binomial(budget, P_TARGET, size=REPS) / budget
        rows.append({"mode": "classical", "shots": shots, "budget": budget,
                     "mean": float(cls.mean()), "std": float(cls.std(ddof=1)),
                     "bias": float(cls.mean() - P_TARGET),
                     "theory_sigma_mean": math.sqrt(P_TARGET * (1 - P_TARGET) / budget)})
        for name, (sim, circs) in modes.items():
            ests, sigmas = [], []
            for r in range(REPS):
                counts = run_counts(sim, circs, shots, seed=1000 * shots + r)
                ones = [c.get("1", 0) for c in counts]
                p_hat, s_theory = mlae_general(ones, shots, K_LIST)
                ests.append(p_hat)
                sigmas.append(s_theory)
                if shots == grid_shots and r == 0:
                    grid[name] = {"counts_by_k": counts, "ones_by_k": ones}
            ests = np.array(ests)
            rows.append({"mode": name, "shots": shots, "budget": budget,
                         "mean": float(ests.mean()), "std": float(ests.std(ddof=1)),
                         "bias": float(ests.mean() - P_TARGET),
                         "theory_sigma_mean": float(np.mean(sigmas))})
            print("%-9s shots %5d  budget %6d  mean %.4f  std %.5f  bias %+.4f" % (
                name, shots, budget, ests.mean(), ests.std(ddof=1), ests.mean() - P_TARGET))

    payload = {"P_TARGET": P_TARGET, "K_LIST": K_LIST, "SHOT_LIST": SHOT_LIST, "REPS": REPS,
               "oracle_units_per_shot": ORACLE_UNITS, "fake_backend": fake_name,
               "rows": rows, "grid_shots": grid_shots, "grid": grid}
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)
    print("wrote", os.path.abspath(OUT_JSON))
    make_chart(payload)


if __name__ == "__main__":
    main()
