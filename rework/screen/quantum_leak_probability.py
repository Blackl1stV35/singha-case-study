"""Quantum check of one Monte Carlo probability on IBM hardware (pipeline test, not an advantage claim).

The classical simulation (rework/17) gives P(leak) = 0.715 for a damaged-path radius of 0.3 um
(design B, sealed edges). Here a single qubit is rotated so that measuring |1> has that probability,
then sampled on an IBM backend. The estimate is compared with the classical value, and the
difference is reported together with the hardware noise and the shot error.

Runs with the IBM token saved on this machine (QiskitRuntimeService). The token is never printed.
Closes its runtime session when done.
Run:  python quantum_leak_probability.py
"""
import json
import math
import os

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "pop_leak_simulation_results.json")
SHOTS = 1000
TARGET_RADIUS = 3e-7   # m, the 0.3 um row of the design B scan


def classical_target():
    with open(RESULTS, encoding="utf-8") as fh:
        rows = json.load(fh)["monte_carlo"]["design_B_leak_probability_vs_damaged_radius"]
    for row in rows:
        if abs(row["r_d_m"] - TARGET_RADIUS) < 1e-12:
            return row["P_leak"]
    raise SystemExit("target radius not found in the classical scan")


def main():
    p = classical_target()
    theta = 2.0 * math.asin(math.sqrt(p))
    qc = QuantumCircuit(1, 1, name="leak_probability")
    qc.ry(theta, 0)
    qc.measure(0, 0)

    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=1)
    print("backend:", backend.name, "pending jobs:", backend.status().pending_jobs)

    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa = pm.run(qc)

    counts = None
    job_id = None
    mode_used = "session"
    try:
        with Session(service=service, backend=backend) as session:
            sampler = SamplerV2(mode=session)
            job = sampler.run([(isa,)], shots=SHOTS)
            job_id = job.job_id()
            result = job.result()
    except Exception as exc:  # noqa: BLE001
        print("session mode unavailable, falling back to backend mode:", type(exc).__name__)
        mode_used = "backend"
        sampler = SamplerV2(mode=backend)
        job = sampler.run([(isa,)], shots=SHOTS)
        job_id = job.job_id()
        result = job.result()

    counts = result[0].data.c.get_counts()
    ones = counts.get("1", 0)
    p_hat = ones / SHOTS
    stderr = math.sqrt(p_hat * (1 - p_hat) / SHOTS) if 0 < p_hat < 1 else math.sqrt(p * (1 - p) / SHOTS)
    summary = {
        "backend": backend.name,
        "mode": mode_used,
        "job_id": job_id,
        "shots": SHOTS,
        "counts": counts,
        "p_classical": p,
        "p_quantum_estimate": p_hat,
        "shot_standard_error": stderr,
        "difference": p_hat - p,
        "difference_in_standard_errors": (p_hat - p) / stderr if stderr > 0 else None,
    }
    out = os.path.join(HERE, "quantum_leak_probability_results.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    print("backend %s | job %s | counts %s" % (backend.name, job_id, counts))
    print("classical p = %.3f, quantum estimate = %.3f +/- %.3f (shot error)" % (p, p_hat, stderr))
    print("wrote", out)


if __name__ == "__main__":
    main()
