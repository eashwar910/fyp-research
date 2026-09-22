# Stage 1 landscape — incomplete

2026-09-13 · Run 4 · **Do not proceed to Stage 2.**

Three landscape scouts ran in parallel on `gpt-5.5`; each received one retry. EU and Singapore/Malaysia now pass the report schema. India failed its retry and was dropped. Neither remaining report fully clears the evidence contract.

| Result | Count |
|---|---:|
| Provisional crowded areas after deduplication | 9 |
| Provisional dated forcing functions after union | 10 |
| Schema-valid reports | 2 / 3 |
| Fully cleared reports | 0 / 3 |
| Re-dispatches | 3 |

The provisional [merged report](merged.json) retains company and source context from [EU](eu.json) and [Singapore/Malaysia](singapore_malaysia.json). [India](india.json) is a failure record; both raw attempts are under `attempts/`. The ten forcing functions include EU EUDR/CAP and monitoring releases, Malaysian palm replanting, Singapore land-use and submission changes, cadastral data, and the historical NICFI programme transition. These are retained scout claims, not independently verified findings.

The overlap between satellite crop-health alerts and prescription mapping was merged across markets. EUDR was unioned once, retaining Malaysian and EU context. India contributes no accepted data. The crowded list remains below the required ten, and several entries do not substantiate two distinct shipping products.

Evidence defects remain material: EU company dates exceed the recency limit or were inherited from other pages; Singapore/Malaysia retains undated page claims, a tier-C second product, and one-product evidence labelled as two-product crowding. Current NICFI/Tropical Forest Observatory access needs checking. Job evidence is sparse or lacks verified publication dates. Suggested technical deltas are unverified; no candidate has been screened or elaborated.

All three retries are exhausted. India’s final invalid date is `companies[3].evidence[1].date = "2026"`; the schema requires `YYYY-MM` or `YYYY-MM-DD`. No month was invented to force acceptance. A third/deep dispatch was not run because the one-retry failure limit has been reached; Stage 1 has not met its exit conditions.

Search use: **168 queries** (140 initial against 75; 28 retry against 30). Singapore/Malaysia exceeded its retry cap, 12 against 10. Exact fetch totals are unavailable; the audit distinguishes trace counts from scout self-reports. Three orchestrator product-URL spot-checks resolved successfully. See [validation audit](VALIDATION.json) and [run log](../RUN_LOG.md).
