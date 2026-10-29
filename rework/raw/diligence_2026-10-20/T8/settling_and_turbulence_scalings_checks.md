# Checks behind the settling and gas-driven flow estimates (dissolution model flow bracket)

- Date read: 2026-10-20. Tier: S for the pages opened; the formulas marked "not opened" are textbook forms used with a stated tier of ASSUMPTION.

## Stokes terminal velocity (opened)
- https://en.wikipedia.org/wiki/Terminal_velocity (WebFetch summary): printed V_t = g d^2 / (18 mu) (rho_s - rho), for creeping flow (Re much less than 1), with C_d = 24/Re. No Schiller-Naumann form is printed.

## Schiller-Naumann drag (formula text not opened)
- Citation only (opened): the OpenFOAM source header https://cpp.openfoam.org/v7/SchillerNaumannDragForce_8H_source.html names "Naumann, Z., and Schiller, L. (1935), A drag coefficient correlation, Z Ver Deutsch Ing 77, 318-323"; the formula sits in a source file that was not shown.
- Benchmark (opened): the MFiX tutorial https://mfix.netl.doe.gov/doc/mfix-exa/guide/latest/tutorials/fluid/steady-flow-around-sphere.html states "the Schiller-Naumann correlation (C_d = 1.0917 at Re=100)". The textbook form C_D = 24/Re (1 + 0.15 Re^0.687) gives 1.09173 at Re 100 (checked by arithmetic: 24/100 x (1 + 0.15 x 100^0.687) = 0.24 x 4.549), a match to 0.003 percent. The formula is therefore used for the free-fall velocity, flagged as formula text not opened. A search snippet (not an opened page) gave the validity as Re below 800 to 1000; the fragments of 0.2 to 2 mm radius have Re about 16 to 1,400, so the 2 mm value (Re about 1,400) is beyond that range and its velocity of 313 mm/s is an extrapolation; it is used only to show that free fall lasts under a second.

## Kolmogorov length (opened) and inertial-range velocity (not opened)
- https://en.wikipedia.org/wiki/Kolmogorov_microscales (WebFetch): eta = (nu^3 / epsilon)^(1/4), epsilon the average rate of dissipation of turbulence kinetic energy per unit mass, nu the kinematic viscosity; the Kolmogorov velocity scale (nu epsilon)^(1/4). The inertial-range scaling u(l) of about (epsilon l)^(1/3) is NOT on that page and the Kolmogorov 1941 page returned HTTP 404; the scaling is textbook and is used as an order of magnitude only (ASSUMPTION).
- Power of rising gas: epsilon = g u_s is an energy balance (power rho g Q H over the mass rho A H of the liquid), not a sourced correlation. The Wikipedia Bubble column reactor page prints only the gas holdup definition, no dissipation or circulation velocity correlation.

## Use in rework/71
- Free-fall velocities of the model's fragments (DERIVED): about 36, 95 and 313 mm/s for 0.2, 0.5 and 2 mm radius, a fall of 0.3 to 2.8 s through the 99 mm depth of the glass: a transient, not a sustained flow.
- Gas-driven slip velocity (DERIVED, order of magnitude): about 6 to 17 mm/s at the central fragment, with 0.05 to 0.5 mm/s of superficial gas velocity.
