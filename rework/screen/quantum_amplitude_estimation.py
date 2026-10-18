"""Quantum amplitude estimation (maximum likelihood) of the design B leak probability, three ways.

The probability is p = P_TARGET (rework/17, design B at a 0.3 um damaged-path radius).
State: A|0> = Ry(2 theta)|0> with sin^2(theta) = p. Grover operator Q = A Z A^dagger Z.
Circuit k applies A, then Q^k, then measures: P(|1>) = sin^2((2k+1) theta).

Runs, same circuits each time:
  exact     noiseless Aer simulation
  noisy     Aer simulation with the noise model of a fake IBM backend (fake_fez if present)
  hardware  IBM Quantum backend (least busy operational, open plan, token saved on this machine)

Estimator: maximum likelihood over theta from the counts at each Grover power, with the
Fisher-information error. Reference: Bernoulli Monte Carlo with the same oracle budget.

Writes quantum_amplitude_estimation_results.json and rework/20_quantum_amplitude_estimation.png.
Run:  python quantum_amplitude_estimation.py
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "quantum_amplitude_estimation_results.json")
OUT_PNG = os.path.join(HERE, "..", "20_quantum_amplitude_estimation.png")
P_TARGET = 0.715
GROVER_POWERS = [0, 1, 2, 3]
SHOTS = 1000


def theta_of(p):
    return math.asin(math.sqrt(p))


def build_circuit(theta, k):
    from qiskit import QuantumCircuit

    qc = QuantumCircuit(1, 1, name="qae_k%d" % k)
    qc.ry(2 * theta, 0)               # A
    for _ in range(k):                # Q = A Z A^dagger Z, applied k times
        qc.z(0)
        qc.ry(-2 * theta, 0)          # A^dagger
        qc.z(0)
        qc.ry(2 * theta, 0)           # A
    qc.measure(0, 0)
    return qc


def check_grover_structure(theta):
    """Numerical check that Q^k A|0> has P(|1>) = sin^2((2k+1) theta)."""
    def ry(phi):
        return np.array([[math.cos(phi / 2), -math.sin(phi / 2)],
                         [math.sin(phi / 2), math.cos(phi / 2)]])

    A = ry(2 * theta)
    Z = np.diag([1.0, -1.0])
    Q = A @ Z @ A.T @ Z
    v = A @ np.array([1.0, 0.0])
    for k in GROVER_POWERS:
        w = np.linalg.matrix_power(Q, k) @ v
        expected = math.sin((2 * k + 1) * theta) ** 2
        if not math.isclose(w[1] ** 2, expected, abs_tol=1e-9):
            raise SystemExit("Grover structure check failed at k=%d" % k)
    return True


def mlae(ones, shots):
    """Maximum-likelihood amplitude estimate and its Fisher-information standard error."""
    grid = np.linspace(1e-7, math.pi / 2 - 1e-7, 400001)
    loglik = np.zeros_like(grid)
    for k, h in zip(GROVER_POWERS, ones):
        P = np.clip(np.sin((2 * k + 1) * grid) ** 2, 1e-12, 1 - 1e-12)
        loglik += h * np.log(P) + (shots - h) * np.log(1 - P)
    th = float(grid[int(np.argmax(loglik))])
    fisher = 0.0
    for k in GROVER_POWERS:
        m = 2 * k + 1
        P = math.sin(m * th) ** 2
        dP = m * math.sin(2 * m * th)
        fisher += shots * dP * dP / max(P * (1 - P), 1e-12)
    sigma_theta = 1.0 / math.sqrt(fisher)
    return math.sin(th) ** 2, abs(math.sin(2 * th)) * sigma_theta


def run_exact(theta):
    from qiskit_aer import AerSimulator

    sim = AerSimulator()
    circs = [build_circuit(theta, k) for k in GROVER_POWERS]
    res = sim.run(circs, shots=SHOTS).result()
    return [res.get_counts(i) for i in range(len(circs))], {"backend": "AerSimulator (noiseless)"}


def run_noisy(theta):
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2

    provider = FakeProviderForBackendV2()
    names = [b.name for b in provider.backends()]
    fake_name = "fake_fez" if "fake_fez" in names else ("fake_brisbane" if "fake_brisbane" in names else names[0])
    fake = next(b for b in provider.backends() if b.name == fake_name)
    sim = AerSimulator.from_backend(fake)
    pm = generate_preset_pass_manager(optimization_level=1, backend=sim)
    circs = [pm.run(build_circuit(theta, k)) for k in GROVER_POWERS]
    res = sim.run(circs, shots=SHOTS).result()
    return [res.get_counts(i) for i in range(len(circs))], {"backend": "AerSimulator with %s noise model" % fake_name}


def run_hardware(theta):
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=1)
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    circs = [pm.run(build_circuit(theta, k)) for k in GROVER_POWERS]
    sampler = SamplerV2(mode=backend)
    job = sampler.run([(c,) for c in circs], shots=SHOTS)
    result = job.result()
    counts = [result[i].data.c.get_counts() for i in range(len(circs))]
    return counts, {"backend": backend.name, "job_id": job.job_id()}


def summarise(name, counts, extra):
    ones = [c.get("1", 0) for c in counts]
    p_hat, sigma = mlae(ones, SHOTS)
    return {
        "mode": name, **extra,
        "counts_by_k": counts,
        "ones_by_k": ones,
        "p_hat": p_hat,
        "sigma_qae": sigma,
        "bias_vs_target": p_hat - P_TARGET,
        "bias_in_sigma": (p_hat - P_TARGET) / sigma,
    }


def make_chart(results):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    theta = theta_of(P_TARGET)
    colors = {"exact": "#185FA5", "noisy": "#EF9F27", "hardware": "#993C1D"}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))

    # Panel 1: outcome probability per Grover power
    ax = axes[0]
    kk = np.linspace(0, max(GROVER_POWERS), 200)
    ax.plot(kk, np.sin((2 * kk + 1) * theta) ** 2, color="#333", lw=1, label="ideal sin^2((2k+1) theta)")
    for name in ("exact", "noisy", "hardware"):
        m = results["modes"].get(name, {})
        if "ones_by_k" not in m:
            continue
        y = [h / SHOTS for h in m["ones_by_k"]]
        err = [math.sqrt(max(v * (1 - v), 1e-9) / SHOTS) for v in y]
        ax.errorbar(GROVER_POWERS, y, yerr=err, fmt="o", color=colors[name], capsize=3, label=name)
    ax.set_xlabel("Grover power k (oracle calls 2k+1)")
    ax.set_ylabel("P(|1>)")
    ax.set_title("Outcome probability per circuit")
    ax.legend(fontsize=8)

    # Panel 2: estimates vs the classical value, at the same oracle budget
    ax = axes[1]
    budget = results["oracle_calls_total"]
    labels = ["classical MC\n(same budget)"]
    vals = [P_TARGET]
    errs = [results["classical_sigma_at_budget"]]
    cols = ["#85B7EB"]
    for name in ("exact", "noisy", "hardware"):
        m = results["modes"].get(name, {})
        if "p_hat" not in m:
            continue
        labels.append("QAE\n%s" % name)
        vals.append(m["p_hat"])
        errs.append(m["sigma_qae"])
        cols.append(colors[name])
    ax.errorbar(range(len(vals)), vals, yerr=errs, fmt="none", ecolor="#333", capsize=6)
    for i, (v, c) in enumerate(zip(vals, cols)):
        ax.scatter([i], [v], s=80, color=c, zorder=3)
    ax.axhline(P_TARGET, ls=":", color="#185FA5")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("P(leak), design B at 0.3 um")
    ax.set_title("Estimates at %d oracle calls" % budget)

    # Panel 3: error vs oracle budget
    ax = axes[2]
    m_sum = sum(2 * k + 1 for k in GROVER_POWERS)
    m2_sum = sum((2 * k + 1) ** 2 for k in GROVER_POWERS)
    N = np.logspace(3, 5, 100)
    ax.loglog(N, np.sqrt(P_TARGET * (1 - P_TARGET) / N), color="#85B7EB", label="classical MC, ~1/sqrt(N)")
    shots_per_k = N / m_sum
    sigma_q = abs(math.sin(2 * theta)) / np.sqrt(4 * shots_per_k * m2_sum)
    ax.loglog(N, sigma_q, color="#185FA5", label="amplitude estimation, ~1/N (ideal)")
    ax.axvline(budget, ls=":", color="#333", label="this run's budget")
    ax.set_xlabel("oracle calls N")
    ax.set_ylabel("standard error of P")
    ax.set_title("Error scaling with the oracle budget")
    ax.legend(fontsize=8)

    fig.suptitle("Amplitude estimation of the leak probability (virtual screen, real and simulated runs)",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT_PNG, dpi=130)
    print("wrote", os.path.abspath(OUT_PNG))


def main():
    theta = theta_of(P_TARGET)
    check_grover_structure(theta)
    budget = SHOTS * sum(2 * k + 1 for k in GROVER_POWERS)
    # QAE_MODES selects which runs to (re)execute; other modes keep their earlier results.
    # This avoids spending IBM runtime again when only a local run needs fixing.
    selected = os.environ.get("QAE_MODES", "exact,noisy,hardware").split(",")
    previous = {}
    if os.path.exists(OUT_JSON):
        with open(OUT_JSON, encoding="utf-8") as fh:
            previous = json.load(fh).get("modes", {})
    results = {
        "P_TARGET": P_TARGET,
        "shots": SHOTS,
        "grover_powers": GROVER_POWERS,
        "oracle_calls_total": budget,
        "classical_sigma_at_budget": math.sqrt(P_TARGET * (1 - P_TARGET) / budget),
        "modes": dict(previous),
    }
    for name, fn in (("exact", run_exact), ("noisy", run_noisy), ("hardware", run_hardware)):
        if name not in selected:
            continue
        try:
            counts, extra = fn(theta)
            results["modes"][name] = summarise(name, counts, extra)
            m = results["modes"][name]
            print("%s: p_hat %.4f +/- %.4f (bias %.1f sigma)" % (name, m["p_hat"], m["sigma_qae"], m["bias_in_sigma"]))
        except Exception as exc:  # noqa: BLE001
            results["modes"][name] = {"mode": name, "error": "%s: %s" % (type(exc).__name__, str(exc)[:200])}
            print("%s failed: %s" % (name, type(exc).__name__))
        with open(OUT_JSON, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2, default=str)
    print("wrote", OUT_JSON)
    make_chart(results)


if __name__ == "__main__":
    main()
