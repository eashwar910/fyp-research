# Run 3 — landscape scan (Sep 2026)

Purpose: ground the candidate list in what companies in the target job markets are
actually shipping and hiring for. Not a literature review; a "what would a hiring
manager at X want to see in a fresher's FYP" scan.

## 1. Who is hiring, and for what

| Company | Region | What they build | What a fresher FYP should signal |
|---|---|---|---|
| SatSure | IN (Bengaluru) | Satellite analytics for agri-lending & crop insurance (PMFBY), infra monitoring. Clients: banks, insurers, govts. Part of the IN-SPACe private EO constellation consortium. | Fluency in GEE + Sentinel; a *decision* output (a claim, a loan) not a map. Their own guidance: NDVI/crop-condition project on public data is the best portfolio piece. |
| Pixxel | IN | Hyperspectral constellation (Fireflies, 5 m, 135+ bands) + Aurora analysis studio. Hiring geospatial ML (crop classification, change detection). | Multi-band / hyperspectral handling, change detection, anything that shows you can extract value from more bands than RGB. |
| Cropin | IN | Farm-management + earth-observation platform; high technical bar. | Model + agronomic understanding together. |
| Satyukt, Fasal, GalaxEye, Dhruva | IN | Remote-sensing SaaS; hires "currently pursuing / recently completed" — fresher-friendly. | GEE, Python, ML on satellite time series. |
| Aonic (ex-Poladrone), Aerodyne, Meraque, Braintree | MY | Drone *services*: spraying, mapping, plantation (oil palm) ops. Profitable, hardware-heavy. | Drone data pipelines that work on raw flight output; anything that makes repeat-flight data comparable. |
| Garuda Robotics, H3 Dynamics | SG | Drone fleet platform + inspection analytics; agriculture is one vertical among many. | Same as above; plus systems/pipeline engineering. |
| Space Intelligence, Nimbo, Coffee Canopy Partnership (Airbus + JDE Peet's/Sucden/Touton) | EU-facing | EUDR compliance maps: distinguishing shade-grown tree crops from forest, 2020 baseline, plot-level verification. | This is the single hottest EO-for-ag problem in 2026 (deadline 30 Dec 2026). |
| Bayer FieldView, EOSDA, Farmonaut, Pro Ladang (MY) | global/MY | Commercial NDVI monitoring dashboards. | Do NOT compete here — this is the C3 auto-fail zone. |

## 2. Trends that matter for candidate generation

1. **Geospatial foundation models are now infrastructure.** AlphaEarth Foundations (64-d, 10 m, annual 2017–2025, free on GEE), Prithvi-EO-2.0, Clay. The labeled-data economics changed: 500–5,000 labels now do what 50,000 did. Google is running an academic program for on-demand *Custom Satellite Embeddings* (higher cadence) — applications close 15 Oct 2026. An FYP that uses AEF as a feature backbone is cheap on compute (all server-side GEE) and looks current.
2. **EUDR is the forcing function.** Large operators must comply from 30 Dec 2026. Open problems named by industry itself: shade-grown coffee/cocoa misclassified as forest (false positives), smallholder plot geolocation (points for <4 ha, polygons for >4 ha), and telling *renovation* from *conversion*. India is a coffee, rubber and (via Kerala/Karnataka) cocoa exporter to the EU.
3. **Field boundaries went global.** FTW released a 10 m global map (1.6 B polygons/yr, 2024 & 2025) — but their own docs say the confidence layer is *conservative in smallholder systems*. Boundaries are the substrate for everything else (EUDR, insurance, MRV).
4. **Drones in India are now policy, not pilots.** Namo Drone Didi (15,000 women SHGs), Kisan Drone subsidies 40–75 %. Spray drones are everywhere; *imagery* drones and the analytics behind them are the gap. Only a handful of open Indian UAV datasets exist; IMPaCT-UAV-MsRGB (Vijayawada paddy, 414 GB, 1 cm GSD, all growth stages, raw frames + GPS metadata, CC-BY 4.0) is the standout.
5. **"Pilot theatre is ending."** Buyers ask: does it save labour, reduce inputs, work offline, fit existing workflows, and can the payback be explained in one sentence. This is the C6 pitch test in the market's own words.
6. **Singapore has no visible farmland** but SFA is investing in early-warning: a new risk-monitoring / supply-visibility dashboard (with PSA BDP, logistics-based) and the Lim Chu Kang master plan (re-parcelling, shared facilities, circularity). The visible gap is *field-level* early warning over Singapore's source basket (Cameron Highlands, Johor, etc.) — which is a satellite problem over Malaysia, not Singapore.

## 3. Things that are crowded (do not enter without a sharp technical delta)

Stubble-burning detection in Punjab (PRSC, CEEW, S1+S2 already done); EU grassland mowing / CAP checks-by-monitoring (JRC, dozens of papers); UAV↔Sentinel-2 fusion (reviewed to death); crop-type mapping; NDVI dashboards; generic weed / disease detection on public datasets; drone SfM canopy height as biomass proxy.

## 4. Bucket note

Your message defines buckets 1 (satellite) and 2 (drone) but bucket 3 says "refer below" and nothing follows — the "B" section never arrived. I treated bucket 3 as the Singapore C1-exempt lane already defined in constraints.yml (non-imagery, novel AI for the SG agri-food landscape). If bucket 3 was meant to be something else, say so and I'll re-run that lane.

Also: constraints.yml C2 lists EU / India / Singapore only. Malaysia is in your job-target list but not in C2, so I did not generate Malaysia-native candidates. Several India candidates (EUDR shade-crop, drone radiometric harmonisation) transfer directly to Malaysian oil-palm / cocoa contexts if you add MY to C2.
