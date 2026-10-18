# Thailand stress-test inputs and sources (updated 18 October 2026)

Virtual screen inputs for the frozen leaf-wrapped pop. Each value is either sourced (URL or citation given, confidence stated) or marked **assumption**. Used by `rework/screen/thailand_stress_test.py` and `rework/screen/thai_summer_occasions.py`.

Confidence: **high** = official text read in full; **medium** = station, standard or measured source read directly; **low** = secondary, reanalysis, single-source or model-derived value; **assumption** = no public source found.

## 1. Ambient air (Bangkok and central plains)

| Parameter | Value used | Source | Confidence |
|---|---|---|---|
| Mar–May daily mean maximum, Bangkok (TMD 48455, 1991–2020) | 35.7 °C afternoon peak; April 35.6–35.7 | TMD climate normals, https://ubonmet.tmd.go.th/files/MetInfo/climate_normal.pdf; TMD outlook Feb–Apr 2026, https://tmd.go.th/media/climate/3-months/newsfma_2026_english.pdf | medium |
| Mar–May daily mean minimum, Bangkok | 26.0–27.2 °C (April 27.2 / 26.9) | same TMD sources | medium |
| Diurnal mean and amplitude used in the model | mean 31.5 °C, amplitude 4.3 K, peak 15:00 (from max and min above) | derived from the two rows above | medium |
| Mar–May absolute monthly maximum, Bangkok | 40.0–40.1 °C (3-hourly synoptic readings) | TMD climate normals | medium |
| Central plains, Nakhon Sawan (TMD 48400) mean maximum | 36.4–38.1 °C; extremes 41.8–43.7 °C | TMD climate normals | medium (not used in the model; sensitivity only) |
| Mean relative humidity, Bangkok | 72–74 % (daily-maximum RH 86–88 %) | TMD climate normals | medium |
| Mean dew point, Bangkok, April | 24.8 °C (Mar–May 23.9–24.9) | TMD climate normals | medium |
| Sunshine | 6.3–7.6 h per day | TMD climate normals | medium |
| Clear-sky daily irradiation, Bangkok (grid cell 13.75 N, 100.5 E) | 5.6–6.1 kWh/m²/day; half-sine peak 800 W/m² used | NASA POWER, https://power.larc.nasa.gov (point query, 1991–2020) | low (reanalysis, not station-validated) |
| Urban wind, Bangkok station, 10 m | 1.1–1.4 m/s; street convective h = 10.7 W/m²K (McAdams 5.7 + 3.8u) | TMD climate normals | medium |
| Open-terrain wind, Don Mueang, 10 m | 3.1 m/s; convective h = 17.5 W/m²K | TMD climate normals | medium |

## 2. Parked car and vehicles

| Parameter | Value used | Source | Confidence |
|---|---|---|---|
| Parked car cabin, Bangkok, highest recorded (east-facing, all day) | 59 °C; model adds +20 K (S3) and +23 K (SU5) above ambient | KMUTT 2024, https://kirim.kmutt.ac.th/converis/portal/detail/Publication/1475727610?lang=en_GB (conference abstract, full text not accessed) | low |
| Refrigerated truck cargo in service, Thailand | **not sourced**; only a reported pre-cool to −15 to −18 °C (one operator) | GCCA Thailand cold-chain assessment, https://www.gcca.org/wp-content/uploads/2024/02/220819-Thailand-Cold-Chain-Assessment-Report-v9-MJ.pdf | low (capability claim) |
| Bangkok truck time window | 10-wheel trucks 10:00–15:00 in the city | one interview-based report (not used in the model) | low |

## 3. Frozen and chilled storage: Thai rules (resolved 18 October 2026)

| Parameter | Value used | Source | Confidence |
|---|---|---|---|
| Frozen storage, **fresh food** in food premises (Thai rule) | at or below −18 °C | DOH notice (B.E. 2561), definition clause 3 and attachment table, https://laws.anamai.moph.go.th/en/doh-annuance/204278 | high (fresh food only) |
| Frozen storage and transport, **processed or packaged** frozen products (Thai rule) | **not found**. No Thai notification sets a storage or transport temperature for processed frozen food, and none for transport | searched Thai FDA and MOPH notifications; GMP notification No. 193 (B.E. 2543) gives only a general prevention duty | gap |
| Frozen storage and transport (international reference) | −18 °C or colder through the cold chain | Codex CAC/RCP 8-1976, proposed draft revision on FAO site, http://www.fao.org/4/Y0681E/y0681e07.htm (final adopted text not retrieved; the −12 °C figure is unverified and excluded) | medium (international, not Thai law) |
| **Cold-holding limit, non-heat ready-to-eat food including beverages** (food premises) | below 5 °C, or up to 2 hours at room temperature as an alternative | Notification on ready-to-eat food (2566), Royal Gazette vol. 140 special 147 ง, 22 June 2566, p.13 clause 6(4); the 5 °C clause also appears in the 2565 notice | high (for food premises sale) |
| Time out of refrigeration (non-heat RTE food, beverages included) | 2 hours at room temperature during preparation or sale | same clause 6(4), as an either/or alternative to below 5 °C | high (food premises only) |
| Time out of freezer | **not found**; no Thai rule addresses it | searched the same notices | gap |
| Storage of ice cream until sale | not higher than −2.2 °C | P354 notice, clause 4(3), https://exfood.fda.moph.go.th/law/data/announ_moph/P354.pdf. Applies only if the product is legally classed as ice cream | high (if classed as ice cream) |
| **Notification No. 463 (B.E. 2568) on edible ice** | In force; takes effect the day after Royal Gazette publication (gazette dated 11 Dec 2568, effective 12 Dec 2568) | Thai FDA law page https://food.fda.moph.go.th/food-law/announ-moph-463; English text https://food.fda.moph.go.th/media.php?id=861494046714109952&name=P463_EN.pdf (clauses 1 to 8 read in full); status also on food.chemlinked.com (secondary). Gazette and FDA page disagree by one day on the issue date; the gazette wins. | high |
| Notification 463: water used for ice | must meet the sealed drinking-water notification's quality standard by reference (clause 4); no municipal or other source named | same English text | high |
| Notification 463: drinks | **no drink or beverage wording**. Whether a drink vendor who adds ice falls under it is a legal interpretation | same English text | gap (legal) |
| Notification 463: labelling and transition | non-transport packaged ice must read "Ice for Consumption" (clause 7); existing sellers have up to one year, about 12 Dec 2026 (clause 8) | same English text | high |

## 4. Gel packs and insulated box

| Parameter | Value used | Source | Confidence |
|---|---|---|---|
| Gel-pack melting point | −1.3 °C (range −2 to 0 °C) | Manufacturer SDS, https://www.thermosafe.com/wp-content/uploads/2021/03/SDS_Final_Gel_Packs.pdf (0 °C, 99 % water); phase-change point −1.3 °C from Feng 2026 model, https://pmc.ncbi.nlm.nih.gov/articles/PMC13125594/ | medium |
| Gel-pack latent heat | 270 J/g (range 200–330 J/g; water upper bound 334 J/g) | Feng 2026 model input (estimated, not a food datasheet); water fusion 334 J/g standard constant | low |
| Pack mass | 0.6 kg total nominal (range 0.4–1.0 kg) | **assumption** (two packs of 200–500 g) | assumption |
| EPS wall conductivity | 0.027–0.040 W/m·K; box UA = 1.0 W/K (range 0.8–1.2) for 3 cm walls, about 0.9 m² | Feng 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC13125594/ (0.027, validated model); manufacturer EPS 0.038 (https://eps.co.uk/applications/thermal_properties_of_eps.html) | medium |
| Box inside convection | 8 W/m²K (range 6–10) | **assumption** | assumption |
| Vendor gel-pack hold times (30 h at 25 °C; 24–72 h) | **not used** | Cooled Solutions, https://cooledsolutions.com/collections/ice-packs (vendor claims, method undisclosed) | excluded |
| Vaccine-carrier retention (13.7–18.6 h at 43 °C) | **not used** as a frozen-food value (chilled 2–8 °C payload) | Marhoon et al., Int. J. Heat and Technology 44(2), 2026, https://doi.org/10.18280/ijht.440216 | excluded |

## 5. Summer occasions (Songkran, festivals, ice-water coolers, humidity)

| Parameter | Value used | Source | Confidence |
|---|---|---|---|
| Festival afternoon peak air temperature | 35.7 °C | section 1 | medium |
| **Splash and open-water temperature** | **29.3 °C** (changed from an assumed 26 °C) | Bangkok canal annual mean, 2024: 29.28 °C; five-year range 28.6 to 29.3 °C (2020 to 2024). Bangkok environmental report 2567, sections 4.1.1 and 4.2.1 (PDF p.28 and p.32). Chao Phraya River annual mean 2024: 30.8 °C (same report, p.28). These are annual means of river and canal water, not April, Songkran or tap-water values. No measured tap or Songkran splash temperature was found. | medium (proxy) |
| Splash fraction and water film | 20 % of time; water film h = 300 W/m²K | **assumption** (no sourced value) | assumption |
| Ice-water bath | 0 to 3 °C over 4 h; water convection h = 300 W/m²K (range 100–500) | Ice-water coolers stay near 0 °C for many hours: frozen 5 kg bottles 5.2 h below 0 °C (minimum −11.7 °C); time to 6 °C with ice-water 38.6 to 63.7 h by cooler type. Indoor, 17.6 °C average, so not tropical. PLoS One 2020, https://pmc.ncbi.nlm.nih.gov/articles/PMC7164660/. The 0 to 3 °C warm-up over 4 h and the convection h are assumptions. | partly sourced |
| Bangkok April normal mean maximum | 35.7 °C (festival peak in SU1, SU5); Songkran forecasts 30 to 37 °C (Naewna, 12 Apr 2025) and 35 to 40 °C (Thansettakij, 10 Apr 2025), both forecasts | Wikipedia Bangkok climate table, https://en.wikipedia.org/wiki/Bangkok (secondary; TMD origin not confirmed) and section 1 | medium |
| Chiang Mai and Khon Kaen April normal maximum | 36.7 °C and 36.2 °C (not used in the model) | Wikipedia climate tables (WMO and Royal Irrigation Department cited, not TMD) | low |
| Thai heat-index warning tiers (TMD and Department of Health) | Observation 27 to 32.9 °C; watch 33 to 41.9 °C; danger 42 to 51.9 °C; extreme 52 °C and above (heat index, not air temperature) | Nation Thailand, quoted in the summer research; Thai index formula not confirmed. Context only. | low |
| Sun-exposure uplift to heat index | up to +15 °F (about +8 °C) under full sun, for shady light-wind index values | US National Weather Service, https://www.weather.gov/safety/heat-index (not a Thai source; context only) | medium (official US) |
| Saturation vapour pressure over ice at −18 °C | 124.9 Pa | Computed from the Goff–Gratch and Murphy–Koop ice formulas (Vömel, https://cires1.colorado.edu/~voemel/vp.html); the FAO table only reaches −14.9 °C (0.166 kPa, https://www.fao.org/4/y7223e/y7223e0i.htm) | medium (derived) |
| **Frost deposition on a cold surface** | measured mean rate 1.7 to 4.1 g/m²/min over 120 min, at −5 to −15 °C plates, 50 to 80 % RH, 16 °C air, 0.7 m/s. Example: 458 g/m² at 120 min, 80 % RH, −10 °C plate | Hermes et al. (2009) test data as tabulated in Kandula (NASA), Table 1 p.31, https://ntrs.nasa.gov/api/citations/20110009969/downloads/20110009969.pdf. Thickness and density come from separate test sets, so the mass values are estimates. Bare aluminium plate, not a food package. | medium (measured, different surface) |
| **Correction to the earlier condensation estimate** | The earlier psychrometric estimate (about 0.27 g/m²/s, or 16 g/m²/min, at 35 °C and 72 % RH) is 4 to 10 times the measured frost rates above. Treat it as an upper bound only; it was not used in the screen. | derived from the frost data above | — |
| **Dew on banana and plantain leaves** | dew 14 ± 2 h per night on 16 of 18 nights (Costa Rica, humid tropics); maximum dew retained 90 µm per side of a leaf (model cap) | Lhomme and Jimenez (1992), IRD, https://horizon.documentation.ird.fr/exl-doc/pleins_textes/pleins_textes_6/b_fdi_35-36/41391.pdf, p.269 to 270 | medium |
| Water vapour and dew point at 30 °C, 80 % RH | dew point 26.2 °C (Magnus, checked against the WFLO worked example) | GCC Association, Condensation Control, https://www.gcca.org/legacy-system/CondensationControl_0_0.pdf (worked example p.4 to 5) | medium |
| Water viscosity and surface tension (external liquid) | 1.79 mPa·s / 0.0756 N/m at 0 °C, down to 0.80 mPa·s / 0.0712 N/m at 30 °C | standard water property tables (IAPWS values as I recall them; not fetched in this session, verify before citing) | medium (unverified fetch) |
| Drink viscosity and surface tension (internal liquid, screen) | 1.0 mPa·s (range 1–3) / 0.072 N/m | rework/16 (assumption from coconut-drink range) | assumption |
| **Leaf contact angle, adaxial (outside-water wetting)** | **Conflict:** 76.08 ± 2.01° (Materials 2022, https://pmc.ncbi.nlm.nih.gov/articles/PMC8839732/) vs about 130° for fresh banana leaf (BioResources 2019, Hassan et al., https://bioresources.cnr.ncsu.edu/wp-content/uploads/2019/09/BioRes_14_4_8331_Hassan_GMA_Wettability_Effect_Surface_Morphologies_Musa_Leaves_15317-3.pdf). The screen keeps 76° as the conservative value. At 130° there is no capillary climb (cos θ < 0), so the outside-water thresholds would not apply. | measured, conflicting |

## 6. Leaf optics (banana, resolved 18 October 2026)

Source: Gausman and Allen (1973), Optical Parameters of Leaves of 30 Plant Species, Plant Physiology 52:57–62, Tables II to V, https://www.mediamatic.net/image/2016/12/14/plntphys00231_0064_copy.pdf (scanned PDF, values read visually and checked by a second reader). Banana is *Musa paradisiaca*.

| Parameter | Value | Basis | Confidence |
|---|---|---|---|
| Infinite-layer reflectance, adaxial, 550 nm | 10.7 % | measured (Table III) | medium |
| Infinite-layer reflectance, adaxial, 650 nm | 6.0 % | measured (Table III) | medium |
| Single-leaf diffuse reflectance, 550 nm | 10.5 % | derived from measured k and s with the single-layer Kubelka–Munk form; reproduces the measured infinite-layer value | estimated |
| Single-leaf diffuse transmittance, 550 nm | 12.0 % | derived, same model; the paper does not publish single-leaf r and t | estimated |
| Single-leaf diffuse reflectance, 650 nm | 6.0 % | derived | estimated |
| Single-leaf diffuse transmittance, 650 nm | 0.69 % | derived; most sensitive to k, so wide uncertainty | estimated |
| Absorption coefficient k, 550 / 650 nm | 1.701 / 4.413 | measured (Table IV) | medium |
| Scattering coefficient s, 550 / 650 nm | 0.456 / 0.602 | measured (Table V) | medium |
| Fresh leaf thickness | 0.241 mm (field-grown) | measured (Table II); the 29-species range is 0.14 to 0.98 mm | medium |
| Reflectance cross-check | about 9 % near 550 nm, about 5 % from 350 to 700 nm | Diaz Herrera (2024) thesis, section 6.1.1 (local copy in the data-gap folder) | low (single thesis) |

**Not resolved:** pandan leaf optics (no measured reflectance or transmittance found; the only pandan source is a cuticle-thickness class, Rahayu et al. 2012, not optics); the leaf cuticle specular roughness (ScienceDirect source refused access); a measured leaf refractive index.

**Mockup note:** the single-leaf transmittance (12 % at 550 nm) is sourced data that could replace the subsurface assumption. The mockup is locked, so these values are recorded in `rework/mockup/MATERIALS.md` and not applied to the render.

## 7. Not sourced (declared gaps)

- Measured tap-water temperature and Songkran splash-water temperature (only annual river and canal means were found).
- Thai frozen-storage and transport rules for processed or packaged frozen products, and any Thai time-out-of-freezer rule.
- Thai or tropical hold-time data for frozen food in insulated boxes with gel packs.
- Measured condensate or frost on frozen packaged food moved into warm, humid air (only bare-plate frost data exist).
- Leaf contact-angle behaviour at high humidity and during dew (the 76° and 130° sources conflict; no measurement in between).
- Pandan leaf optics and cuticle specular roughness.
- Whether a frozen drink pop is legally classed as ready-to-eat (2-hour rule) or as ice cream (−2.2 °C rule). This is a classification question for a Thai registration adviser.
