# Simulated run of the dye-penetration protocol (18 October 2026)

> **Retired 18 October 2026.** This record belongs to candidate A (the leaf-wrapped frozen drink) or to a retired step of the desk work. See [README](README.md). Kept for the record.

**This is a simulation, not a physical test.** No leaves were cut, frozen, dyed or scanned. The run applies the protocol in rework/33 to virtual wraps, using the breach model in rework/31. It shows what the protocol would most likely report for each true breach fraction. It is not a result for any real wrap. Code: `rework/screen/lab_sim_dye_protocol.py`, results `lab_sim_dye_protocol_results.json`.

## Setup

- 300 wraps per run, 2,000 simulated runs per condition.
- A wrap leaks if a qualifying breach sits on the inner epidermis and another on the outer epidermis (closed stomata), or if an inner breach meets an open stomatum (open stomata).
- A leaking wrap shows a visible dye spot with probability 0.95 (assumed).
- Pass rule: zero spots in 300 wraps, with controls valid.
- Controls are assumed to pass in the simulation: the positive controls (punctured wraps) always show a spot, and the negative controls (PET inside) never do. A physical run has to check these.

## Result

Pass probability for the leaf-only wrap, out of 2,000 simulated runs:

| True breach fraction | Stomata closed | Stomata open |
|---|---|---|
| 10⁻⁹ | 99.8 % | 45.9 % |
| 10⁻⁸ | 82.8 % | 0.1 % |
| 10⁻⁷ | 0 % (median 16 spots) | 0 % (median 67 spots) |
| 3 × 10⁻⁷ | 0 % | 0 % |
| 10⁻⁶ | 0 % | 0 % |

Median spots (k) at 10⁻⁸: 0 with closed stomata, 7 with open stomata. The closed-stomata numbers match the screen's leak probability (about 0.07 % per wrap at 10⁻⁸, rework/31), and the open-stomata numbers match its open-stomata case.

## What it shows

1. **The protocol separates the cases it is meant to separate.** Closed stomata with breach fraction 10⁻⁸ or below pass most of the time. Breach fraction 10⁻⁷ fails every time.
2. **Stomatal state decides the outcome.** With open stomata, even 10⁻⁸ fails almost always. The protocol as written only records stomata density, so it cannot tell a pass from a fail caused by open stomata.
3. **Protocol gap found.** Before a physical run, add a stomatal-state check: for example, an assessment of whether the stomata are closed in the frozen-thawed wraps (see Limits). Without it, a failed run can't be traced to breaches or to stomata.

## Limits

- This is a model. The breach fraction, the connection rule and the stomatal state are assumptions from rework/30 and rework/31.
- The controls are assumed to pass. The physical run has to demonstrate the detection limit.
- The stomatal state after freezing is not measured here, and the protocol does not yet measure it.

## Next step, if you approve

Run the physical protocol (rework/33) with the stomatal-state check added. The lab work is physical and needs your approval, leaves, a freezer, an incubator and a scanner. I can't run it here.
