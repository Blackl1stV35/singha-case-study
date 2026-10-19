# Quantum check of one Monte Carlo probability (IBM hardware)

> **Retired 18 October 2026.** This record belongs to candidate A (the leaf-wrapped frozen drink) or to a retired step of the desk work. See [README](README.md). Kept for the record.

Date: 18 October 2026. Script: [screen/quantum_leak_probability.py](screen/quantum_leak_probability.py). Raw result: [screen/quantum_leak_probability_results.json](screen/quantum_leak_probability_results.json).

Status: pipeline test on hardware. It is not evidence for the leak question and it is not a quantum advantage claim.

## What was run

- Target: the classical design B leak probability at a 0.3 µm damaged-path radius, from [17](17_classical_simulation_results.md): P = 0.715.
- Circuit: one qubit, rotated so that measuring |1> has probability P, then measured. This is quantum sampling of a single Bernoulli probability.
- Backend: ibm_fez (least busy, 1 job pending at submission), open instance, 1000 shots.
- Job: dba33kfi0auc7391et3g, status DONE. No jobs left running on the account after the run.

## Result

| Quantity | Value |
|---|---|
| Counts | 0: 327, 1: 673 |
| Classical P | 0.715 |
| Quantum estimate | 0.673 ± 0.015 (shot error) |
| Difference | −0.042, which is −2.8 standard errors |

## Reading

- The shot error alone is 0.015. The gap of 0.042 is larger than that, so something other than sampling noise is pulling the reading down.
- The likely cause is hardware error: readout errors that flip |1> to |0>, plus gate error from the rotation. Both push the reading toward 0. I did not measure these errors, so this is an interpretation, not a result.
- The quantum estimate is less precise than the 200-run classical Monte Carlo for this single number. Quantum hardware did not improve precision here.

## What this does and does not show

- It shows the pipeline works end to end: token saved locally, a job submitted to IBM, results read back, and no jobs left running.
- It does not change the leak decisions in [16](16_permeability_seam_estimate.md) or [17](17_classical_simulation_results.md). The plastic-free claim stays dropped, and the film arm stays the closed fallback.
- A fair comparison would need more shots, readout-error mitigation, and a noise-free simulator run of the same circuit as a reference. Those are not in this check.

## Account

- The runtime session was not used: the session path raised a TypeError, and the script fell back to backend mode. No session was left open.
- Usage on the open plan: one 1000-shot job on a single qubit.
