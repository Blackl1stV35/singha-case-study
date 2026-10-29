# Wikipedia, Grashof number: the mass-transfer form

- URL read: https://en.wikipedia.org/wiki/Grashof_number
- Date read: 2026-10-20 (WebFetch, model-summarised)
- Tier: S (encyclopedia). Status: SOURCED, secondary.

## Printed
- Mass-transfer Grashof number: Gr_c = g beta* (C_a,s - C_a,a) L^3 / nu^2, with beta* = -(1/rho) (d rho / d C_a) at constant T and p (the form as returned by the fetch summary; L is a characteristic length, here the sphere diameter).
- The page prints no natural-convection correlation for a sphere (for Sherwood or Nusselt numbers), so the Sherwood correlation comes from the NPTEL notes (nptel_natural_convection_sphere_steinberger_treybal.md).
- Heat-transfer ranges printed are for vertical plates only (laminar roughly 1e3 < Gr_L < 1e6; transition around 1e8 to 1e9) and are not used.

## Use in rework/71
- beta* delta c = delta rho / rho, so Gr = g (delta rho / rho) d^3 / nu^2. The density step delta rho is estimated as c (1 - rho_w / rho_solid) with c = the saturation concentration (additive volumes, ASSUMPTION), about 9.5 percent of the water density; real salt solutions are somewhat denser. No measured density of a dissolved cube solution was found.
