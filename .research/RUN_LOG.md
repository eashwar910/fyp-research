# RUN_LOG — run 4

Copy to `.research/RUN_LOG.md` at stage 0. Fill each block when the stage
exits. Keep it terse; this is for resuming and auditing, not narrative.

## Stage 0 — preflight
- date: 2026-09-13
- constraints.yml version / sha: v2 / sha256:abeba9167470f791
- buckets.yml sha: v5 / sha256:8c40cdde1db2f293
- agents/ tree sha (per agents/README.md): 10816a528944ab84 (repo HEAD 8ab21b9)
- archive runs indexed: [run3] → 41 prior candidates
- open TODOs at start: none (T1 bucket-3 definition, T2 Malaysia in C2 — both `resolved: true`)
- bucket status check: bucket_1 satellite / bucket_2 drone_and_aerial / bucket_3 standout (`status: active`) — no `status: placeholder`
- archive index written: `.research/archive_index.json`
  - by stage reached: full 14 / screen-only 27
  - by final verdict: pass 4, conditional 8, fail 2, screen_fail 27
  - by failed gate: C7_novelty 25, C3_not_generic 8, C9_feasibility 3, C8_scope_floor 1
  - by region: india 21, eu 15, singapore 5 (no malaysia, no standout — both new in run 4)
- dispatches this stage: 0 (stage 0 is orchestrator-only, per ORCHESTRATOR.md)

## Stage 1 — landscape
- date / status: 2026-09-13 / INCOMPLETE; `ready_for_stage_2: false`
- dispatches: 3 initial, parallel (india, singapore_malaysia, eu), plus 3 retries; model `gpt-5.5` (available identifier for owner routing “GPT 5.5 sol”)
- input: exact landscape_scout system, depth normal, verbatim constraints v2, today 2026-09-13; Malaysia equal weight in combined market
- validation: Draft 2020-12 + local shared references + URI format checks, before semantic acceptance; raw response text extracted mechanically from this run’s scout transcripts
- initial schema results: India valid; EU 1 date error; Singapore/Malaysia 29 date errors
- retry schema results: EU valid (6 companies / 5 crowded / 5 forcing); Singapore/Malaysia valid (5 / 5 / 6); India invalid (year-only date), dropped
- evidence acceptance: 0 fully cleared reports; EU/SG-MY retained provisionally with explicit issues, excluded from Stage 2 readiness
- searches used / budget: 140 initial / 75; retries 28 / 30 (India 8/10, EU 8/10, SG-MY 12/10); cumulative 168 queries
- crowded entries (merged): 9 PROVISIONAL (10 raw claims → 9 after crop-health dedupe); <10 exit threshold, several crowding claims unsubstantiated
- forcing functions (merged, dated): 10 PROVISIONAL (11 raw → 10 after EUDR union)
- re-dispatches and why: 3. EU schema/date and evidence defects; SG-MY schema/date and unsupported shipping/crowding; India evidence-contract defects despite initial schema pass. Each received one retry with errors appended.
- second failure handling: India dropped after invalid retry; failure record at landscape/india.json. No third/deep retry after failure allowance exhausted. Stage exit conditions unmet.
- spot-checks: 3 product URLs (BASF, SatSure, Bayer/Polybee), all resolved; no 404 re-dispatch
- output: landscape/{india,singapore_malaysia,eu}.json, merged.json, SUMMARY.md, VALIDATION.json, attempts/*.json
- evidence limits: borrowed/crawl dates, stale EU company evidence, undated hiring, insufficient distinct shipping products, current tropical-mosaic access unverified; detailed in VALIDATION.json
- stopped after Stage 1; no candidates, gates, verifiers, elaboration or roster run

## Stage 2 — gap hunt
- date / status: 2026-09-13 / COMPLETE
- authorization: owner explicitly requested Stage 2 after Stage 1 incomplete report; proceeding with verbatim provisional landscape, retaining all evidence limitations
- dispatch matrix: satellite × india/eu/malaysia/singapore_source_basket; drone_and_aerial × india/eu/malaysia/singapore; standout × global (9 jobs)
- model / concurrency: hunters 1-8 dispatched by the Codex session on gpt-5.5; drone_and_aerial__singapore attempt 2 dispatched by Claude Code on Sonnet (per CLAUDE.md model routing). Runtime permitted 3 active subagents against 9 requested, so jobs launched as slots opened.
- input provenance: hunters/dispatch_manifest.json records source/envelope SHA-256. All 7 source files re-hashed at resume and matched the recorded SHA-256 exactly, so the Singapore re-dispatch used a byte-identical envelope apart from region, depth, avoid and the appended attempt-1 validator errors.

### HANDOFF — Codex to Claude Code (mid-stage, 2026-09-13)
- trigger: the Codex session hit its account usage limit mid-merge. `merge_audit.json` was left at `status: "running"`; `candidates.jsonl` held a partial 107-row merge over 6 hunters only.
- work completed by Claude Code on resume: (1) repaired `standout__global.json`; (2) dispatched and validated `drone_and_aerial__singapore` attempt 2; (3) re-merged across all 9 hunters and regenerated `candidates.jsonl` wholesale.
- **`standout__global` was recovered from a Codex session transcript, NOT a live dispatch.** The array is byte-identical to what the hunter returned (verified against `attempts/standout__global.1.json`). Consequence: its `queries[]` log does not exist and cannot be reconstructed, so the "record every query" clause of the subagent contract is unverifiable for this one hunter. Its 21 lines are otherwise schema-valid and contract-complete (bucket, region and all three `standout_fields` present on every line).
- **`standout__global` seed_url dates were resolved by the orchestrator, not the hunter.** Attempt 1 failed schema on 5 bare-year dates. The orchestrator fetched each source and replaced only the `date` field; the diff is exactly 10 lines (5 pairs). Full basis per URL in `validation.json` → `standout__global` → attempt 2 → `date_resolutions`. Two are worth knowing: the CGIAR/Tumaini date was substantively wrong (2019 was the underlying journal paper; the page itself is 2021-01-24), and cropmonitor.org/about-us carries no visible page date at all, so its 2024-03-14 comes from the site's own sitemap.xml `lastmod` — a weaker basis than the other four.
- **`drone_and_aerial__singapore` was not an empty cell.** The resume brief described it as having no output and no transcript; in fact attempt 1 existed (8 lines, schema-valid, contract-invalid on `queries[]` string-vs-object, under the 15 floor) and `dispatch_manifest.json` showed a deep retry already launched and lost. It was therefore re-dispatched as attempt 2, not attempt 1. The genuinely missing output was `drone_and_aerial__malaysia`, whose attempt 2 (17 lines) landed after the Codex merge ran and so was absent from the 107-row merge.

### Results
- one-liners returned per hunter: satellite india 19 / eu 25 / malaysia 16 / singapore_source_basket 21; drone india 16 / eu 18 / malaysia 17 / singapore 16; standout global 21
- received total: 169
- after dedupe: 155 (14 removed across 11 semantic merge groups)
- hunters under the 15-line floor: NONE (lowest is 16, met by four hunters)
- ids: reassigned wholesale R4-S01 … R4-S155 in matrix order. The previous merge's ids are VOID — any R4-S reference written before this merge points at a different candidate.
- dedupe rule: within-bucket only. Buckets are distinct gate lanes (standout skips C1/C2 and adds hard C11), so a cross-bucket merge would subject a line to gates it is exempt from and discard its `standout_fields`. 3 cross-bucket near-duplicates recorded as metadata instead of merged.
- new merge groups this pass: 5 (1 cross-hunter radiometric-drift group spanning drone india/eu/singapore; 3 within drone malaysia; 1 within standout). The 6 Codex-era satellite groups were carried over unchanged.
- integrity check: all 169 source records appear exactly once across the 155 rows; id sequence contiguous; every row `screen_status: unassessed`.
- bucket distribution: satellite 73 / drone_and_aerial 62 / standout 20
- region distribution (observation only, no quota): eu 41, india 35, malaysia 29, global 20, singapore 15, singapore_source_basket 15
- archive restatements flagged: 31 of 155 carry a `restates` pointer into run3
- data_class distribution: in `hunters/merge_audit.json`; families are non-exclusive. Top families: uav_or_aerial 56, sentinel_2_optical 52, sentinel_1_sar 45, derived_maps_or_registries 29, foundation_model_embeddings 20.
- queries logged: 179 across 7 hunters. Two gaps, both from the Codex session and both unrecoverable: `standout__global` (no log at all) and `drone_and_aerial__malaysia` (count 11 attested in validation.json, body never written to query_logs.json).
- budget: Singapore re-dispatch logged 31 search queries against `max_searches: 30` — 1 over, a soft failure per the subagent contract; output accepted.
- stage 2 exit check: playbook wants 40-80 unique one-liners; actual 155. The re-dispatch trigger is "fewer than 40" only, so the exit condition is met. Volume carries into SCREEN, where a 60-75% kill is expected.

### Carried into Stage 3 (not acted on — Stage 2 stop boundary)
- Landscape input remains PROVISIONAL: stage 1 exited `ready_for_stage_2: false` with the India scout dropped. Every candidate row carries `landscape_context: provisional_stage1_owner_authorized_stage2`.
- Several `drone_and_aerial__singapore` lines name an imagery source whose ACCESS is asserted rather than shown (Malaysian partner drone archives; BCA TR78 thermal inspection archives; the PUB Kranji BVLOS feed; "under written data-sharing terms"). C2 `sensor_rules.singapore.extra_check` requires a named EXISTING, ACCESSIBLE source, and naming a firm is not the same as having an archive. The hunter self-flagged four of these `hunter_confidence: low`. This is a SCREEN/stage-4 call, not a merge call, but it is the likeliest concentrated kill zone in that hunter.
- `drone_and_aerial__malaysia` returned all 17 lines with `crowded_area_entered: true`, and 13 of 17 depend on one dataset family (MOPAD). The iRadar hyperspectral set is request-access, not open.
- stop boundary: Stage 2 complete. No SCREEN, no verifiers, no elaboration run.

## Stage 3 — SCREEN
- date / status: 2026-09-13 / COMPLETE
- run by: orchestrator, no dispatch (CLAUDE.md: gate stages are not delegated)
- input: `.research/candidates.jsonl` (155) + `.research/archive_index.json` (41 run3 candidates)
- output: `.research/gate_screen.yml` — all 155 retained with a verdict and reason (mark, never delete)
- assessed / passed / kill rate: 155 / 63 / **59.4%**
- kills by gate: C7 67 / C3 19 / C1 4 / excl 0 / C11 2
- **two passes were run.** Pass 1 killed only 25.2%, below the skill's "if fewer than half fail you are being too generous" threshold and below the owner's 50% floor. Pass 2 re-read C3 and tightened on two grounds that are in constraints.yml rather than invented:
  - C3 is a RULE ("must not be a generic agri-AI artifact"), not only the `auto_fail_patterns` list. Applied to candidates whose analytic content is a GIS overlay, a business wrapper around crop classification, or a ranking layer with no new measurement.
  - C7 `hard_rejection` covers "no technical delta", not only literal geographic transfer. Applied to (a) the typing template — relabelling an established detection into decision classes for a new regulation/user — and (b) duplicate moves within this run, where a second candidate reproduces another's contribution with only the sensor, commodity or audience changed.
- kills by hunter: sat india 14/19, sat eu 11/24, sat malaysia 9/15, sat SG-basket 11/15, drone india 11/16, drone eu 11/17, drone malaysia 9/14, drone SG 9/15, standout 7/20
- region mix of survivors (observation only, never balanced): eu 19, global 13, malaysia 11, india 10, singapore 6, singapore_source_basket 4
- bucket mix of survivors: satellite 28, drone_and_aerial 22, standout 13

### Archive check (run3)
- 31 of 155 carried a `restates` pointer. Rule applied: inherit the archived verdict unless the `delta_claim` explicitly addresses that candidate's `failed_gate`.
- inherited a kill where the delta did NOT address the archived gate: R4-S87 (restates run3:D02, C9 — no accessible post-spray imagery; the delta re-framed novelty, not data access), R4-S91 (run3:D09), R4-S102 (run3:D11), R4-S140 (run3:S07), R4-S125 (run3:S21 with only a sensor change).
- survived BECAUSE the delta addressed the archived gate: R4-S02 (run3:S20), R4-S13 (run3:S02), R4-S15 (run3:S07 — names the monthly on-demand embedding product the archived candidate lacked), R4-S22 (run3:S09 — supplies the typing its reason demanded), R4-S28/R4-S93 (run3:D10), R4-S30 (run3:D09), R4-S35 (run3:S05), R4-S74/R4-S103 (run3:D04), R4-S101 (run3:D03).
- R4-S37 was killed on C7 for restating run3:S01 — the owner's own archived PASS — with only the region and user changed (India smallholders -> EU importers). Regional transfer of a prior pass is still regional transfer.

### Known limits of this screen
- **Exit band missed.** ORCHESTRATOR.md stage 3 expects a `screen_pass` list of 12-25; this produced 63. The cause is upstream: stage 2 exited with 155 candidates against a planned 40-80. Even the skill's expected 60-75% kill on 155 lands at 39-62 survivors, so the 12-25 band was unreachable without inventing kills. Not narrowed further, because manufacturing fails to hit a number is the same error class as region-balancing, which the skill forbids.
- **Stage 4 budget is blown.** ORCHESTRATOR.md budgets stage 4 at <=25 survivors x (adversary <=15 searches + verifier <=10 fetches). 63 survivors is ~2.5x that. The owner must decide before stage 4: raise the budget, or rank the 63 and verify a top slice. Do not start stage 4 on the assumption that 63 is affordable.
- **standout is under-killed at 59.4% (only 7/20) and this is correct.** SCREEN applies just two of C11's five requirements (layperson sentence, visible demo moment). The other three — `not_already_a_product`, `surprise`, `headline_claim` — need the adversary's product search and are evaluated in FULL. Expect a heavy second cull of this bucket at stage 6.
- **C7 verdicts here are sniff-test only.** Every survivor is `novelty_type: needs_novelty_check`. No novelty was judged from memory; the C7 kills recorded above are for absent technical delta or duplicate moves, not for prior art found by search.
- **Data access was not assessed and will be the main stage-4 killer.** Several survivors name a source whose access is asserted: R4-S124/R4-S131 (BCA TR78 thermal inspection archives), R4-S133 (PUB Kranji BVLOS feed), R4-S134 (competing vendors' proprietary pipelines), R4-S147/R4-S148 (commercial robot camera streams), R4-S015 (Custom Satellite Embeddings academic programme, deadline 15 Oct 2026), R4-S083/R4-S118 (request-access UAV/hyperspectral datasets).
- **R4-S132 carries a known C2 problem that SCREEN cannot fail it on.** It proposes tasking a drone firm to fly periodic missions; C2 `sensor_rules.singapore.extra_check` puts self-collected flights out of scope, and commissioning flights is functionally that. C2 is not a SCREEN gate, so it passed here and must be settled at stage 4.
- stop boundary: Stage 3. No verifiers dispatched, no elaboration.

## Stage 4 — verify
- date / status: 2026-09-13 / **PARTIAL — HALTED BY PLATFORM LIMITS, NOT BY DESIGN**
- authorization: owner instructed full coverage ("for every screen_pass") after being told the 63 survivors exceed the <=25 stage-4 budget. Proceeded on that reaffirmation.
- planned: 63 survivors x 2 roles = 126 dispatches (novelty_adversary + data_verifier, neither seeing the other's output), model sonnet per CLAUDE.md routing.
- **completed: 43 of 126 dispatches (34%). 20 of 63 candidates have BOTH files; 43 have neither.**
- outputs written: `.research/novelty/*.json` 21, `.research/data/*.json` 21 (only schema-valid, contract-clean files were written)

### Why it stopped
1. **WebSearch session cap.** A hard session-wide limit of 200 web searches was consumed mid-run. Degradation was measurable: the first 7 adversaries averaged 11.7 queries with 0 budget_exhausted; the next 7 averaged 8.3 with 6 exhausted. Later agents reported "200/200" before running a single query and fell back to CrossRef/Semantic Scholar APIs and direct WebFetch.
2. **API monthly spend limit.** Dispatches then began failing outright with HTTP 429 ("monthly spend limit", session resets 15:00 Asia/Kuala_Lumpur). `nov:R4-S47` and `nov:R4-S50` died this way. No further subagent can be launched.

### Evidence integrity under exhaustion — the asymmetry that matters
- A `closed` verdict is a POSITIVE finding: the adversary produced a named URL. A short search does not weaken it. All 6 closures stand.
- A `type_a` verdict asserts the ABSENCE of prior art and is only as strong as the search behind it. **Checked explicitly: no type_a verdict came from an exhausted run.** Agents that ran out returned `closed` or an honest `unclear` and did not fabricate prior_art. That is the correct behaviour and preserves the F4 fix.
- Every affected candidate carries `search_budget_exhausted` and an `evidence_caveat` in `gate_screen.yml`.

### Results over the 20 fully-verified candidates
- novelty: closed 6 / type_a 5 / type_b 6 / unclear 4 (42 not run)
- data: open 4 / conditional 12 / blocked 5 (42 not run)
- routing: fail 9 / proceed_conditional 6 / conditional 3 / proceed 2 / not_verified 43

### Routed out (9)
| id | gate | why |
|---|---|---|
| R4-S18 | C7 | Closed by TraceX EUDR due-diligence for Indian coffee exporters |
| R4-S20 | C7 | Closed by the Area Monitoring geotagged-photo application (deployed EU, Slovenia/England) |
| R4-S24 | C7 | Closed by Agreena — live EU cover-crop additionality, 4.5M ha, 17 countries, incl. leakage |
| R4-S32 | C7 | Closed by ESA EO-INSURE (Agricolus): same event-vs-pre-existing damage separation, same region |
| R4-S38 | C7 | Closed by Whisp (FAO/Google/WRI): already does commodity-plausibility + post-2020 timing screening |
| R4-S44 | C7 | Closed by Whisp: point-or-polygon ingestion with a "More info needed" tier = the claimed triage delta |
| R4-S02 | C9 | CCE plot-to-insurance-unit geolocation exists only behind PMFBY/DGCES OTP login; no public route |
| R4-S40 | C9 | No parcel-level enrolment register for cover-crop/tillage programmes; no treatment group exists |
| R4-S51 | C9 | No public TSPKS/MPOB smallholder geometry, and FTW has not shipped Malaysia at all |
| R4-S52 | C9 | Coherence needs SLC pairs (absent from GEE/PC, GRD-only); myGAP parcel geolocations not published |

(R4-S52 and R4-S51 both also carry `budget_exhausted` on the data side — their negative findings are "could not confirm", not "confirmed absent", and should be re-run.)

### CONDITIONAL on novelty (3) — unclear after budget exhaustion, deep re-dispatch never possible
- R4-S25 peatland rewetting — human check: does the 2025 RSASE "Modelling water table depth at rewetted peatlands with S1/S2" already cover the 3-way rewetting/flood/cultivation triage?
- R4-S28 hedgerow survival — human check: does France's Dispositif National de Suivi des Bocages already classify hedgerow survival state?
- R4-S30 vineyard event dating — human check: does the CCDC / BFAST / LandTrendr disturbance-dating family already cover this? That is the method-space question the adversary could not run.

### Cleared to stage 5 (2 proceed, 6 proceed_conditional)
proceed: R4-S23, R4-S42. proceed_conditional: R4-S01, R4-S13, R4-S15, R4-S22, R4-S26, R4-S35, R4-S47(partial), R4-S50(partial) — see per-id `verify:` blocks.

### Validation and repairs
- A systematic defect appeared in the first outputs: bare-year dates inside `product_search` (the same bug that broke two stage-2 hunters) plus `maxLength` overflows. Fixed mid-run by adding a MANDATORY self-validation step — each agent runs `check4.py <role>:<id>` and cannot reply until it prints `ok`. Later dispatches came back clean.
- Orchestrator repairs to 6 files, all recorded in `hunters/../repair_log.json` (12 entries): 2 dates re-resolved by fetching the page (eos.com `article:modified_time` / JSON-LD `dateModified`), 2 product entries DROPPED because no date could be established (business.esa.int/projects/cropsnap, land.copernicus.eu HRL croplands) — a bare year is invalid and padding to a month is forbidden; 5 maxLength truncations; 5 null optional keys removed.
- **2 outputs rejected and NOT written**: `dat/R4-S20` claimed `fetched_ok: true` on a JRC CbM page whose URL never appeared in `fetched[]` — a substantive contract violation (assumed access, exactly F4), not a formatting slip; `nov/R4-S47` overflowed `reason` and could not be re-run before the spend limit hit.
- URL spot-check: 14 of a 142-URL pool (10%). 12 resolve. 2 unresolved on two attempts — `pmfby.gov.in/pdf/Revised_Operational_Guidelines.pdf` (independently reported unreachable by two agents) and `zenodo.org/records/4473715`. Both flagged for `reverify`; the re-dispatch the failure table calls for was not possible.

### Budget
- The <=25-survivor stage-4 budget was knowingly exceeded (63 survivors). The run consumed the entire 200-search session allowance and then the API spend limit, at 34% of planned dispatches — empirical confirmation that full coverage of 63 survivors is not affordable in one session.

### To resume (what the next session must do)
1. 83 dispatches for 43 candidates never started. Ids are every `route: not_verified` in `gate_screen.yml`.
2. Re-run `dat:R4-S20` (contract violation) and `nov:R4-S47` (invalid output).
3. Deep re-dispatch the 3 `unclear` adversaries (R4-S25, R4-S28, R4-S30) with `input.depth: "deep"`.
4. Re-verify the 2 unresolved URLs via `input.reverify`.
5. Envelopes for all 126 dispatches are already built and pinned to verified source SHAs at `<scratchpad>/env/{nov,dat}/<id>.json`; `DISPATCH_RULES.md` and `check4.py` make each relaunch a one-line prompt.
- stop boundary: Stage 4. No elaboration run.

### Stage 4 RESUME — session of 2026-09-18 / 2026-09-22 (no dispatches yet)

- **Limits reset.** Verified live on 2026-09-18, not assumed: one orchestrator WebSearch and one
  Sonnet subagent dispatch both clean, no 429. The 200-search cap was session-scoped; the
  monthly spend limit rolled over.
- **The resume plan in the section above was partly void.** The 126 pre-built envelopes,
  `check4.py` and `DISPATCH_RULES.md` lived in the previous session's scratchpad, which is
  session-scoped and had been cleared. None were in the repo. All were rebuilt.
- **Four corrections to this log, from `gate_screen.yml` (authoritative):**
  1. "Cleared to stage 5" above is wrong. `proceed` = **R4-S22, R4-S23**; R4-S42 is
     `proceed_conditional`.
  2. **R4-S47 and R4-S50 are NOT cleared** — both are `not_verified`. R4-S47 has a data file
     only; R4-S50 has neither.
  3. **R4-S20 needs no further dispatch.** Its novelty verdict is `closed` with 8 logged queries
     and a named closing URL (JRC Area Monitoring traffic-light system). That is a C7 hard fail
     regardless of data, so the `dat:R4-S20` re-run requested above is wasted work. Its `note:`
     field ("Not dispatched. No novelty or data evidence exists") is stale and contradicts its
     own `novelty_verdict` — fix at fold-in.
  4. Route counts are: proceed 2, proceed_conditional 6, conditional 3, fail 9, not_verified 43.

#### Constraints changed — v2 → v3 (2026-09-22, owner-requested)
- C9 gained `max_local_storage_gb: 512` (owner can attach an external SSD). A dataset up to
  512 GB must NOT be failed on size alone; above it, the candidate must name a separately
  downloadable subset that fits. Scoped to STORAGE only — the compute rule is unchanged.
- sha256 `abeba9167470f791` → `4521dc01d7545044`. Stage 0's pinned hash is superseded.
- Checked before editing: **no completed data verdict was size-blocked**, so nothing needed
  re-verification. The TB figures in R4-S13 and R4-S35 are total-archive sizes with a workable
  subset already identified.
- All 41 data envelopes embed C9 verbatim and pin the constraints SHA, so they were regenerated.
  Verified: 0 still pinning the old SHA, 41 on the new, 0 missing the 512 rule.
- **Unresolved interaction:** `budget_myr: 200` is unchanged and a 512 GB SSD plausibly consumes
  most of it. If the SSD is not separate from the project budget, a verifier could fail a
  candidate on budget having just passed it on storage. Owner to decide.

#### Tooling rebuilt (commit 63fccea)
- `tools/check4.py`, `tools/gen_envelopes.py`, 42 novelty prompts, 41 data envelopes,
  6 shared-source prechecks, `tools/whats_left.sh`.
- Validator was **negative-tested**, not just acceptance-tested: given a deliberately broken
  file it correctly caught a bare-year date, a short query log, a missing `closing_item`,
  a missing `product_search`, and a `maxLength` overflow. (Minor: it reports the `reason`
  overflow twice.)
- Orchestrator spot-check: arXiv 2601.01084 fetched and every quoted figure matched exactly
  (42,430 images / 415 GB / Vijayawada / 3 Jan 2026).

#### Shared-source pre-check results
- **open**: national orthophotos (S90, S93, S95) · WeedsGalore + PhenoBench (S101)
- **conditional**: MOPAD (S108/110/113/115/118 — exists with labels but **no licence text on any
  landing page**) · IMPaCT-UAV (S74/75/76/79 — IEEE DataPort terms still unfetched; 415 GB now
  inside the v3 ceiling) · OpenET API (S141, S152)
- **blocked**: BCA TR78 thermal archive → **S124 and S131 are dead on C9.** No public archive
  exists, only inspection rules and forms. Saves 4 dispatches. *Not yet folded into
  `gate_screen.yml`.*

#### Plan changed — three accounts to one (2026-09-22)
- The second Claude account and the Codex subscription are gone. Phase 0 survives them.
- 82 dispatches remain (40 nov + 39 dat + 3 deep) against an empirical ~200 searches per
  session. Full coverage of 63 is **not reachable**; the deliverable is a verified, ranked
  **top-20 slice** with the remainder honestly left `not_verified`.
- Ordering changed to **data-first globally**: a `blocked` data verdict is a complete verdict,
  so it converts a scarce budget into finished verdicts fastest.
- Insurance rule: every session ends by regenerating `ROSTER.md`, marked `PARTIAL — n of 63`.
- Full plan: `RUNBOOK.md` (repo root).

#### Repo hazard found
- `.gitignore` line 2 is `.research/*`, so **a plain `git add` of any `.research/` path silently
  commits nothing**. Every such add needs `-f`. As of now the entire run-4 state —
  `gate_screen.yml`, `candidates.jsonl`, this log, and all 42 verifier outputs — is untracked,
  working-tree only. Session limits do not threaten it, but `git clean -fdx` would erase it.
  Recommended narrowing is in `RUNBOOK.md` §9.8; owner's call.

- **Dispatches run this session: 0.** No stage-4 verification, no elaboration, no gate.


## Stage 5 — elaborate
- dispatches:
- `needs:` returned (id → what → routed to):

## Stage 6 — FULL
- PASS / CONDITIONAL / FAIL:
- region mix (observation):
- scope-floor distribution:

## Stage 7 — roster
- roster length:
- top-3 by ranking key:
- archived to: research-archive/run4/

## Budget
- total tool calls (searches + fetches): 168 individual search queries in 42 batched search calls; at least 10 scout open actions visible in transcripts plus 3 orchestrator spot-check URL opens. Exact fetch-target total not available; retry self-reports are in landscape/VALIDATION.json.
- over/under ceiling and where: Stage 1 initial query allowance exceeded by 65 (140/75); SG-MY retry exceeded by 2 (12/10). No evidence of approaching the pipeline-wide 1000-call ceiling; exact fetch total remains unavailable.

## Open questions for the owner
- Archive coverage: `research-archive/` contains run3 only. `constraints.yml
  prior_run_failures` references runs 1–3, and run3's own header says
  "research-archive-v1/ was NOT available in this session, so the 'check against
  v1' rule could not be applied". The run-4 archive check therefore covers run3
  only. If run1/run2 verdict files exist elsewhere, drop them in
  `research-archive/` and stage 0 should be re-run before stage 2.
- run3 C7 verdicts were recorded without the v1 archive check (per that file's
  own header) and 25 of 41 kills were C7. Inheriting a run3 C7 kill at stage 3
  inherits that weakness; the archive check should defer to the stage-4
  adversary where a run-4 delta_claim addresses the run3 `failed_gate`.
- `.claude/agents/elaborator.md` carries `tools: []` to express the contract's
  "elaborator has no search tools". Whether Claude Code parses `[]` as "none"
  rather than falling back to inherit-all is unverified; if it inherits, the
  stage-5 no-search rule is unenforced at the harness level.
- Repo state: the run4_changes extraction left HEAD at `8ab21b9 "ToDo Changes"`,
  a commit not present at session start, and the working tree clean. Nothing in
  stage 0 depends on this, but the owner should confirm that commit is theirs.
