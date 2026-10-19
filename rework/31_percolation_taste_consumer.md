# Percolation, taste and consumer effects of the inner barrier (18 October 2026)

> **Retired 18 October 2026.** This record belongs to candidate A (the leaf-wrapped frozen drink) or to a retired step of the desk work. See [README](README.md). Kept for the record.

Status: the working design (leaf wrap with a food-grade inner barrier) is **confirmed by the user on 18 October 2026**. This note closes the three open questions it left: the percolation estimate, the taste effect, and the consumer effect. Code: `rework/screen/percolation_taste_resolution.py`, results `rework/screen/percolation_taste_results.json`.

## 1. Percolation: resolved

**Two physical regimes bound the leak.**

- **Local, cell-scale connection.** Damaged cells connect only when they lie within a connection distance d_c. For continuum percolation of discs, the critical areal density is about 4.51 / (π d_c²). This gives a damaged-cell fraction of 0.21 for d_c = 0.1 mm, 0.008 for d_c = 0.5 mm, and no solution for d_c = 0.03 mm (one cell). This bound is optimistic.
- **Connected airspace network.** Leaf mesophyll intercellular air spaces form one connected network, which is why gas exchange works through the leaf. A breach that opens to the network connects to the rest of the leaf. This is the physically appropriate regime for a leaf.

**Adopted model.** A leak needs a qualifying breach on both epidermal surfaces that connect through the airspace network. The inner surface is always wetted by the melt. The outer surface connects through breaches or through open stomata. The epidermis is 2 of about 8 cell layers across the 0.24 mm leaf, so each surface holds about 25 % of the breaches.

| Damaged-cell fraction | Expected qualifying breaches per wrap | Leak probability, stomata closed | Leak probability, stomata open |
|---|---|---|---|
| 10⁻⁹ | 0.011 | 0 % | 0.3 % |
| 10⁻⁸ | 0.11 | 0.07 % | 2.6 % |
| 10⁻⁷ | 1.1 | 5 % | 23 % |
| 10⁻⁶ | 11 | 87 % | 93 % |
| 10⁻⁵ and above | 107 and above | 100 % | 100 % |

**Fifty-percent leak point:** about 4.6 × 10⁻⁷ with stomata closed, and 2.6 × 10⁻⁷ with stomata open (about 3,100 open stomata per wrap, if they are open).

**Result.** The leaf-only seal survives only if freeze damage is below about 10⁻⁸ of cells. That is far below plausible freeze damage. The local bound (up to 0.2) is rejected because it ignores the connected airspace network. The inner barrier removes the problem, because the melt never reaches the leaf's inner surface.

## 2. Taste: resolved

The uptake of aroma into the inner film is approximately F = K (A/V) √(D t / π), with contact time t = 2 h and a pouch area of 0.02 m² per 170 mL. Assumed values are K and D set by polymer class, with a tenfold sensitivity on D.

| Inner barrier | Aroma uptake in 2 h | Tenfold D | Decision |
|---|---|---|---|
| Polyethylene (PE) | over 100 % (the model predicts complete depletion of the aroma; strong scalping) | over 100 % | avoid |
| Polypropylene (PP) | over 100 % (complete depletion) | over 100 % | avoid |
| **PET** | **0.18 %** | 0.56 % | **select** |
| EVOH | 0.03 % | 0.09 % | alternative, if oxygen barrier is needed |

**Result.** PE and PP would strip terpene-like aromas from a pandan-coconut drink. PET takes up well under 1 % of the aroma, so no taste loss is expected from scalping. PET is also a dense, low-migration polymer for small molecules, so migration into the drink is physically low. Food-contact compliance for PET must be confirmed for the supplier's grade. That is a regulatory check, not a physical question.

## 3. Consumer effect: resolved by a positioning decision

Physics cannot measure consumer perception, so this question is resolved by a decision, not a calculation.

- **Decision:** the proposition is leaf-wrapped frozen coconut-pandan drink, with the leaf as the visible, traditional element. The inner barrier is not advertised as plastic-free.
- **Target:** the plastic-free buyer hypothesis in the briefing is withdrawn for the barrier version. The audience is Thai buyers who value the leaf format and the peel-and-sip act. Whether they accept an inner PET pouch is not known, and the consumer test is out of scope.
- **Claim:** "leaf-wrapped". The claim does not say plastic-free, and the inner PET pouch is disclosed if asked.

## Limits that remain

- The breach fraction is unmeasured. The percolation result is a threshold, not a probability for a specific wrap.
- The K and D values are physics-based assumptions by polymer class. A tenfold change in D changes the uptake by about threefold.
- Food-contact compliance for PET and any migration limits are regulatory checks outside this screen.
- Consumer acceptance of the inner pouch is not measured.
