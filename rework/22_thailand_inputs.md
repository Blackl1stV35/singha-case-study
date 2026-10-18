# Thailand stress-test inputs and sources (18 October 2026)

Virtual screen inputs for the frozen leaf-wrapped pop. Each value is either sourced (URL given, confidence stated) or marked **assumption**. Used by `rework/screen/thailand_stress_test.py` and `rework/screen/thai_summer_occasions.py`.

Confidence: **medium** = station or standard source read directly; **low** = secondary, reanalysis or single-source value; **assumption** = no public source found.

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

## 3. Frozen storage reference

| Parameter | Value used | Source | Confidence |
|---|---|---|---|
| Frozen storage and transport, at or below | −18 °C (start and reefer case) | Codex CAC/RCP 8-1976, FAO text, http://www.fao.org/4/Y0681E/y0681e07.htm (labelled a proposed draft; confirm final text); ASEAN-Japan cold-chain guidelines, https://www.mlit.go.jp/common/001444815.pdf | high (international, not Thai law) |
| Thai regulatory frozen-food temperature | **not found** (only a draft durian rule, not applicable) | Thansettakij, https://www.thansettakij.com/economy/668297 | — |
| Cold-holding line used for the "core above 5 °C" check | 5 °C | **assumption**, to be confirmed against Thai FDA or Ministry of Public Health guidance | assumption |

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
| Songkran splash water temperature | 26 °C; splash fraction 20 %; water film h = 300 W/m²K | **assumption**: no sourced water temperature found. The only source read (Radical Storage travel blog, 2026, https://radicalstorage.com/travel/songkran-2026/) advises room-temperature water and warns against ice water, with no Celsius value. | assumption |
| Ice-water bath | 0 to 3 °C over 4 h; water convection h = 300 W/m²K (range 100–500) | Ice-water coolers stay near 0 °C for many hours: frozen 5 kg bottles 5.2 h below 0 °C (minimum −11.7 °C); time to 6 °C with ice-water 38.6 to 63.7 h by cooler type. Indoor, 17.6 °C average, so not tropical. PLoS One 2020, https://pmc.ncbi.nlm.nih.gov/articles/PMC7164660/. The 0 to 3 °C warm-up over 4 h is still an assumption. Convection h is an assumption. | partly sourced |
| Bangkok April normal mean maximum | 35.7 °C (festival peak in SU1, SU5); Songkran forecasts 30 to 37 °C (Naewna, 12 Apr 2025) and 35 to 40 °C (Thansettakij, 10 Apr 2025), both forecasts | Wikipedia Bangkok climate table, https://en.wikipedia.org/wiki/Bangkok (secondary; TMD origin not confirmed) and section 1 | medium |
| Chiang Mai and Khon Kaen April normal maximum | 36.7 °C and 36.2 °C (not used in the model; context for northern and northeastern festivals) | Wikipedia climate tables, https://en.wikipedia.org/wiki/Chiang_Mai, https://en.wikipedia.org/wiki/Khon_Kaen (WMO and Royal Irrigation Department cited, not TMD) | low |
| Thai heat-index warning tiers (TMD and Department of Health) | Observation 27 to 32.9 °C; watch 33 to 41.9 °C; danger 42 to 51.9 °C; extreme 52 °C and above (heat index, not air temperature) | Nation Thailand, quoted in the summer research; Thai index formula not confirmed. Context only. | low |
| Sun-exposure uplift to heat index | up to +15 °F (about +8 °C) under full sun, for shady light-wind index values | US National Weather Service, https://www.weather.gov/safety/heat-index (not a Thai source; context only) | medium (official US) |
| Saturation vapour pressure over ice at −18 °C | 124.9 Pa (used in the condensation estimate) | Computed from the Goff–Gratch and Murphy–Koop ice formulas (Vömel, https://cires1.colorado.edu/~voemel/vp.html); the FAO table only reaches −14.9 °C (0.166 kPa, https://www.fao.org/4/y7223e/y7223e0i.htm) | medium (derived) |
| Water viscosity and surface tension (external liquid) | 1.79 mPa·s / 0.0756 N/m at 0 °C, down to 0.80 mPa·s / 0.0712 N/m at 30 °C | standard water property tables (IAPWS values as I recall them; not fetched in this session, verify before citing) | medium (unverified fetch) |
| Drink viscosity and surface tension (internal liquid, screen) | 1.0 mPa·s (range 1–3) / 0.072 N/m | rework/16 (assumption from coconut-drink range) | assumption |
| Leaf contact angle, adaxial | 76.08° (measured); 60° wettable bound | rework/16 (measured) | medium |

## 6. Not sourced (declared gaps)

- Thai measured cargo temperature in delivery vans and motorbike boxes in service.
- Thai or tropical hold-time data for frozen food in insulated boxes with gel packs.
- Thai regulatory frozen-food storage and the cold-holding limit for ready-to-drink products.
- Songkran splash-water temperature (no public source read gave a Celsius value) and street-stall exposure duration.
- Condensation rate on frozen packs in humid air: no measured source found. The deposition estimate uses psychrometric values only.
