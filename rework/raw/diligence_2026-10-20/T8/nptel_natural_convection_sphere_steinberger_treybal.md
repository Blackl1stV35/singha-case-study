# NPTEL lecture notes, Mass Transfer Operation, Module 3 Lecture 3: single-sphere correlations (secondary)

- URL read: https://archive.nptel.ac.in/content/storage2/courses/103103035/module3/lec3.pdf (80 KB PDF; text extracted locally with pdftotext; the web fetch summariser could not decode it)
- Date read: 2026-10-20
- Tier: S (university lecture notes, a textbook-level secondary reporting Steinberger and Treybal 1960 and Froessling 1939). The notes are in "Joint initiative of IITs and IISc, funded by MHRD", authored "Kaushik" per the PDF metadata, created 2012. Status: SOURCED, secondary. The original papers were not opened.

## Printed correlations (section 3.4.1, equation numbers as in the notes)
- (3.35) Natural convection, single sphere: Sh_nc = 2.0 + 0.569 (Gr_D Sc)^(1/4), in the range Gr_D Sc < 1e8.
- (3.36) Sh_nc = 2.0 + 0.0254 (Gr_D Sc)^(1/3) Sc^0.244, for Gr_D Sc > 1e8.
- (3.34) Sh = Sh_nc + 0.347 (Re Sc^0.5)^0.62, for 1 < Re < 3e4 and 0.6 < Sc < 3200 (combined natural and forced convection; not used in the model).
- (3.37 to 3.39) forced convection: Sh = 2.0 + m Re^n Sc^(1/3); the notes print Froessling and Evnochides and Thodos as Sh = 2.0 + 0.552 Re^(1/7)... for Re 2 to 12000 and Sc 0.6 to 2.7; the exponent on Re as extracted (1/7) looks like a garbled 1/2 and is not used.
- The Grashof number definition in the extracted text is garbled (the symbols are lost); the definition used in the model is the mass-transfer Grashof number from the Wikipedia Grashof page (see wikipedia_grashof_mass_transfer_form.md): Gr = g beta* (delta c) L^3 / nu^2 with beta* = -(1/rho)(d rho / d c).

## Use in rework/71
- Solutal natural convection from an isolated dissolving sphere in a quiescent liquid, Sh_nc = 2 + 0.569 (Gr Sc)^(1/4), with Gr = g (delta rho / rho) d^3 / nu^2, delta rho from an additive-volume estimate (ASSUMPTION). The central fragment of 1 mm diameter gives Gr Sc about 1.3e6, inside the printed range (below 1e8). The Schmidt number of the model (about 1,100 to 1,400) is inside the 0.6 to 3200 range printed for (3.34) only.
- The correlation is for an isolated sphere in an unbounded liquid. A bed of fragments on the bottom of a glass, with dense solution pooling beneath it, is not covered.

## Limits
- Secondary lecture notes; garbled Grashof definition; original papers not opened.
