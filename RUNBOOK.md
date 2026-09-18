# RUNBOOK — Run 4, Stage 4 completion across three agents

**Written:** 2026-09-18 · **Branch:** `v3` · **Applies to:** finishing stage 4, then stages 5–7.

This runbook splits the remaining work across three accounts (Claude Code, Claude.ai web
chat, Codex) so that **no session limit can cost you more than the single dispatch that was
in flight.** Read §2 before running anything — the durability and concurrency rules are what
make the split safe.

---

## 1. Ground truth (verified 2026-09-18, not copied from RUN_LOG)

Stage 4 halted at 34% on 2026-09-13 (search cap, then API spend limit). **Both limits have
since reset** — verified this session by a live WebSearch and a live Sonnet subagent
dispatch, both clean, no 429.

### 1.1 Current verdict state — `gate_screen.yml` is authoritative

| route | n | ids |
|---|---|---|
| `proceed` | 2 | R4-S22, R4-S23 |
| `proceed_conditional` | 6 | R4-S01, R4-S13, R4-S15, R4-S26, R4-S35, R4-S42 |
| `conditional` (novelty unclear) | 3 | R4-S25, R4-S28, R4-S30 |
| `fail` | 9 | R4-S02, R4-S18, R4-S24, R4-S32, R4-S38, R4-S40, R4-S44, R4-S51, R4-S52 |
| `not_verified` | 43 | see §3 |
| **total** | **63** | |

### 1.2 Four corrections to `RUN_LOG.md` — apply these, do not trust the log here

1. **The log's "Cleared to stage 5" list is wrong.** It says `proceed: R4-S23, R4-S42`.
   The gate file says **R4-S22 and R4-S23** are `proceed`; **R4-S42** is `proceed_conditional`.
2. **R4-S47 and R4-S50 are NOT cleared.** The log lists them as `proceed_conditional (partial)`.
   Both are `not_verified` in the gate file and are part of the 43. R4-S47 has a data file
   only; R4-S50 has neither.
3. **R4-S20 is a free kill — do not spend two dispatches on it.** Its novelty verdict is
   already `closed` with a live evidence file (`.research/novelty/R4-S20.json`). A `closed`
   novelty verdict is a C7 hard fail regardless of data access, so the `dat:R4-S20` re-run
   the log asks for is wasted work. Route it to `fail` / `C7_novelty` at fold-in.
   (Its `note:` field — "Not dispatched. No novelty or data evidence exists" — is stale and
   contradicts its own `novelty_verdict: closed`. Fix the note at fold-in.)
4. **The 126 pre-built envelopes, `check4.py` and `DISPATCH_RULES.md` are gone.** They lived
   in the previous session's scratchpad, which is session-scoped and has been cleared. None
   are in the repo. Phase 0 rebuilds them. Resume step 5 of the old log is void.

### 1.3 Files that exist

- `.research/novelty/*.json` — 21 ids (includes R4-S20; excludes R4-S47, R4-S50)
- `.research/data/*.json` — 21 ids (includes R4-S47; excludes R4-S20, R4-S50)
- Both files: 20 ids. These 20 are the only fully-verified candidates.

---

## 2. Three principles

### 2.1 Durability — state lives in the repo, resume is derived from the filesystem

Every unit of work is **one file, written the moment it completes**. Never a scratchpad
(that is exactly how the envelopes died), never a single aggregate file that can be left
half-written (that is how the stage-2 merge was lost at `status: running`).

Resume is therefore **stateless**: diff the expected id list against the files on disk.
Nothing needs to remember anything. A limit hit costs you the in-flight dispatch only.

### 2.2 Concurrency — conflicts are prevented by construction, not by merge skill

- Each lane owns a **disjoint set of candidate ids** and writes only its own new files.
- **Workers never touch shared files.** `gate_screen.yml`, `RUN_LOG.md`, `candidates.jsonl`
  and `ROSTER.md` have exactly one writer: Lane A, during the sequential fold-in.
- Per-lane append-only ledgers (`.research/ledger/lane{a,b,c}.jsonl`) so no two agents ever
  append to the same file.
- All three lanes work on branch `v3` and `git add` **only their own paths**. Because the
  file sets are disjoint there is nothing to conflict on. If you hit `.git/index.lock`,
  wait two seconds and retry — that is lock contention, not a merge problem.

### 2.3 Prefix-value — rank first, so stopping anywhere is still a good outcome

The work is ordered by expected survival (§3). Any prefix of the ranked list is a usable
deliverable. This is what makes "I ran out of usage" a cost in *quantity*, never in *quality*.

---

## 3. Ranking and tiers — the 43 `not_verified`

Stage 7's ranking key needs verifier output the 43 don't have yet, so these are ranked by a
**pre-verification priority = P(data accessible) × clarity of technical delta.** The RUN_LOG
states plainly that data access "will be the main stage-4 killer", so accessibility dominates.

**R4-S20** — excluded, free C7 kill (§1.2.3). Leaves **42** to work.

### Tier A — open, named, fetch-verifiable data (21). Work these first.

| # | id | region | data | note |
|---|---|---|---|---|
| 1 | R4-S93 | eu | BD_ORTHO + PDOK + basemap.at | restates run3:D10; cross-resolution benchmark, strong C8 reusable artifact |
| 2 | R4-S101 | eu | WeedsGalore + PhenoBench | restates run3:D03; cross-dataset failure map |
| 3 | R4-S75 | india | IMPaCT-UAV | restates run3:D01; radiometric repeatability |
| 4 | R4-S74 | india | IMPaCT-UAV | restates run3:D04; per-plant detection w/ uncertainty |
| 5 | R4-S103 | eu | GrapeSLAM raw frames | restates run3:D04; row-level geolocation uncertainty |
| 6 | R4-S47 | malaysia | Sentinel-1/2 | **needs novelty only** — data already `conditional`. Cheapest win on the board |
| 7 | R4-S76 | india | IMPaCT-UAV | orthomosaic seam / misalignment mask |
| 8 | R4-S79 | india | IMPaCT-UAV | RGB↔multispectral band misalignment |
| 9 | R4-S90 | eu | FLAIR-HUB + LPIS | structure-vs-declared-label contradiction |
| 10 | R4-S95 | eu | PNOA 25 cm | terrace-wall break / erosion risk |
| 11 | R4-S113 | malaysia | revised MOPAD labels | label errors that flip a subsidy verdict |
| 12 | R4-S110 | malaysia | MOPAD + Roboflow | domain-shift rejection for client orthomosaics |
| 13 | R4-S115 | malaysia | MOPAD | geolocation uncertainty ellipses |
| 14 | R4-S108 | malaysia | MOPAD | block-level vacant-point confidence |
| 15 | R4-S104 | eu | AgriAdapt salad weed | spray-ready / review / unsafe triage |
| 16 | R4-S50 | malaysia | Sentinel-1/2 + AlphaEarth | EUDR commodity-identity uncertainty |
| 17 | R4-S58 | malaysia | NICFI + AlphaEarth | **C9 NICFI purpose-bound licence check applies** |
| 18 | R4-S65 | sg_basket | WorldCereal + S1 | shortfall simultaneity vs substitutability |
| 19 | R4-S67 | sg_basket | Sentinel-1 | restates run3:S21; flood timing → price |
| 20 | R4-S60 | sg_basket | Sentinel-1/2 | consignment origin plausibility |
| 21 | R4-S64 | sg_basket | Landsat + S2 | irrigation persistence → import price |

### Tier B — standout bucket (11). Open-ish, non-imagery.

R4-S141, R4-S152 (OpenET API) · R4-S151 (GEOGLAM/NASA Harvest) · R4-S150 (PlantVillage) ·
R4-S137 (FAO eLocust) · R4-S142 (FAO FLAPP) · R4-S144 (APEDA HortiNet) · R4-S136 (ultrasonic
plant audio) · R4-S145, R4-S146 (saffron: smartphone spectral / Foldscope) · R4-S153 (camera
trap + acoustic deterrent)

> Expect a heavy second cull here at stage 6. SCREEN applied only two of C11's five
> requirements; `not_already_a_product`, `surprise` and `headline_claim` are evaluated in FULL
> and depend on the adversary's `product_search`. **The `product_search` block is therefore
> mandatory and load-bearing for every Tier B candidate** — the gate cannot pass one without it.

### Tier C — access asserted or gated (10). **Data-first — do not spend an adversary yet.**

R4-S83 (request-access HSI pearl millet) · R4-S118 (request-access iRadar hyperspectral) ·
R4-S124, R4-S131 (BCA TR78 thermal inspection archives) · R4-S127 (raw frames off the
aircraft from named firms) · R4-S132 (**known C2 problem** — commissioning periodic flights
is functionally self-collection, which `sensor_rules.singapore.extra_check` puts out of
scope) · R4-S133 (PUB Kranji BVLOS feed) · R4-S134 (competing vendors' proprietary pipelines)
· R4-S147, R4-S148 (commercial robot camera streams: See & Spray / LaserWeeder / Blue River)

**Rule for Tier C: run `data_verifier` ONLY. Dispatch the novelty adversary only if data comes
back `open` or `conditional`.** The RUN_LOG predicted these die on C9; a `blocked` data verdict
kills the candidate outright and the expensive search-heavy adversary is never spent. This
alone saves up to 10 adversary dispatches.

### 3.1 Shared-dependency pre-check — run ONCE, before per-candidate work

Several candidates stand or fall together on one dataset. Verify each family **once**, not
4× redundantly, and record it at `.research/data/_shared/<family>.json`:

| family | candidates at stake | if blocked |
|---|---|---|
| MOPAD | S108, S110, S113, S115, S118 | 5 candidates die together |
| IMPaCT-UAV | S74, S75, S76, S79 | 4 die together |
| national orthophotos (BD_ORTHO / PDOK / basemap.at / PNOA) | S90, S93, S95 | 3 die together |
| OpenET API | S141, S152 | 2 die together |
| BCA TR78 thermal archive | S124, S131 | 2 die together (both Tier C) |
| WeedsGalore + PhenoBench | S101 | 1 |

The RUN_LOG already flags that 13 of 17 drone-Malaysia lines depend on MOPAD. **Verify MOPAD
first.** If it is blocked you delete five candidates for the cost of one fetch.

---

## 4. Lane assignment

| Lane | Account | Owns | Writes | Why there |
|---|---|---|---|---|
| **A** | Claude Code (pro #1) | Orchestration, gate stages, stage-5 elaboration, fold-in | `.research/elaborated/*`, shared files, `ledger/lanea.jsonl` | Gate stages are non-delegable (CLAUDE.md). Elaboration costs **zero searches** |
| **B** | Claude.ai web chat (pro #2) | `novelty_adversary` — Tier A then Tier B, in rank order | `.research/novelty/*.json`, `ledger/laneb.jsonl` | Search-heavy (15/dispatch) on a **separate meter**; no budget-exhaustion degradation |
| **C** | Codex Plus | Phase-0 scaffolding, then **all** `data_verifier` | `.research/data/*.json`, `.research/dispatch/*`, `ledger/lanec.jsonl` | Deterministic code work needs no search; verification is fetch-led. Precedent: Codex drove part of stage 2 |

**Disjointness holds:** Lane B only ever creates `novelty/<id>.json`; Lane C only ever creates
`data/<id>.json`; Lane A only ever touches shared files and `elaborated/`. No two lanes can
write the same path.

### 4.1 Why elaboration goes first in Lane A

The 8 already-cleared candidates (§1.1) have passed SCREEN **and** both verifiers, so
elaborating them is contract-legal under CLAUDE.md. The elaborator has **no search tools**, so
this consumes nothing from any meter. **This is your guaranteed output for today** — finished,
readable candidate write-ups that exist regardless of whether any verification completes.

> Caveat carried from the RUN_LOG: `.claude/agents/elaborator.md` declares `tools: []` to
> express "no search". Whether the harness reads `[]` as "none" or falls back to inherit-all is
> unverified. Lane A must confirm the elaborator ran no searches (check its transcript) — if it
> inherited tools, the stage-5 no-search rule is unenforced and the run is still valid but the
> budget accounting changes.

---

## 5. Phase 0 — setup (sequential, blocking, ~20 min)

Everything downstream needs these. Do them in order; do not start Phase 1 until step 4 passes.

**5.1 — Lane A: create the skeleton.**
```bash
mkdir -p .research/dispatch/nov .research/dispatch/dat .research/data/_shared \
         .research/elaborated .research/ledger
git add -A && git commit -m "stage4 resume: lane skeleton"
```

**5.2 — Lane C (Codex): rebuild the validator.** Recreate the lost `check4.py` at
`tools/check4.py`. Contract: `python3 tools/check4.py <role>:<id>` where role ∈ {nov,dat},
validates `.research/{novelty,data}/<id>.json` against `schemas/novelty_verdict.schema.json`
or `schemas/data_verification.schema.json`, resolving `$ref` into `schemas/_common.schema.json`.
Prints exactly `ok` on success, else a numbered list of violations. Must enforce, explicitly:
- `queries` `minItems: 3` (nov) and every item having `q` + `useful`
- every date matching `^\d{4}-\d{2}(-\d{2})?$` — **a bare year is invalid and must never be
  padded to a month.** This one defect broke two stage-2 hunters and six stage-4 outputs.
- `maxLength` on `reason` (600), `why` (300), `notes` (500), `nearest_neighbours_do_not` (400)
- conditional requirements: `closing_item` when `verdict=closed`; `type_b_fields` (all four
  keys) when `verdict=type_b`; `human_should_check` when `verdict=unclear`; `product_search`
  always present
It needs no network and no LLM. Pure stdlib JSON + a hand-rolled subset validator is fine.

**5.3 — Lane C (Codex): rebuild the envelope generator** at `tools/gen_envelopes.py`, writing
one file per candidate per role from `candidates.jsonl` + `gate_screen.yml` + `agents/*.json`
+ `constraints.yml`. Output: `.research/dispatch/nov/<id>.md` (paste-ready, §6.2 format) and
`.research/dispatch/dat/<id>.json` (machine envelope). Pin the SHA-256 of every source file
into each envelope, as the previous run did.

**5.4 — Lane A: verify before fan-out.** Run `check4.py` against three existing known-good
outputs (`nov:R4-S23`, `nov:R4-S01`, `dat:R4-S13`). All three must print `ok`. If the
validator rejects a file that was accepted last run, the validator is wrong — fix it before
dispatching anything, or you will re-run 80 dispatches against a broken gate.

**5.5 — Lane C: shared-dependency pre-check (§3.1).** MOPAD first. Commit each result.

```bash
git add tools/ .research/dispatch .research/data/_shared && git commit -m "stage4: tooling + shared source precheck"
```

---

## 6. Phase 1 — parallel execution

All three lanes now run at the same time. They cannot collide (§2.2).

### 6.1 Lane A — Claude Code (me)

In priority order:

1. **Elaborate the 8 cleared candidates** (stage 5) → `.research/elaborated/<id>.md`.
   Zero search. This is today's guaranteed deliverable.
2. **Fold in results as they land.** Poll `.research/{novelty,data}/` every so often, validate
   new files with `check4.py`, and update `gate_screen.yml`. Lane A is the *only* writer here.
3. **Deep re-dispatch the 3 `unclear` adversaries** — R4-S25 (peatland rewetting), R4-S28
   (hedgerow survival), R4-S30 (vineyard event dating) — with `input.depth: "deep"`, using my
   own subagents. These are high-value and benefit from harness-observed query logs.
4. **Spot-check** ~10% of new URLs, plus the two that failed last run
   (`pmfby.gov.in/pdf/Revised_Operational_Guidelines.pdf`, `zenodo.org/records/4473715`).
5. Keep `RUN_LOG.md` current after each fold.

**Budget discipline:** Lane A should hold its 200 searches in reserve for items 3–4. Do not
run per-candidate verification here — that is what Lanes B and C are for.

### 6.2 Lane B — Claude.ai web chat (pro #2)

**Order:** Tier A #1 → #21, then Tier B. Stop whenever you like; the ranking makes any prefix
a good result. **Skip Tier C entirely** until Lane C clears their data (§3).

**Three rules that make or break this lane:**

1. **One fresh conversation per candidate. Never batch.** A verdict's quality is a direct
   function of search depth (~11.7 queries was the healthy average). Batch five candidates and
   the model shortcuts, and a shallow adversary produces a **false `type_a`** — an assertion
   that no prior art exists. That is the single worst failure mode in this pipeline. Last run's
   integrity held *precisely* because exhausted agents returned honest `unclear` instead.
2. **Never run a novelty and a data prompt in the same thread.** The contract requires that
   neither verifier sees the other's output.
3. **Save the reply as a file, do not paste it back into Claude Code.** Copy the JSON block to
   `.research/novelty/<id>.json`. This keeps the result durable and costs no session context.
   Validation happens in bulk later.

**Per-candidate loop:**
```
open a NEW chat on claude.ai
  → paste the contents of .research/dispatch/nov/<id>.md
  → wait for the JSON
  → save it verbatim to .research/novelty/<id>.json
  → append one line to .research/ledger/laneb.jsonl:
      {"id":"<id>","role":"nov","lane":"b","status":"written","ts":"<ISO8601>"}
  → every 5 candidates:  git add .research/novelty .research/ledger && git commit -m "lane B: nov <ids>"
```

If the reply is truncated or wrapped in prose, reply in that same chat with:
`Return only the JSON object, complete, no prose.` If it still fails, mark the ledger line
`status:"invalid"` and move on — Lane A re-dispatches once at fold-in, per CLAUDE.md.

#### 6.2.1 The Lane B prompt (what `gen_envelopes.py` emits per candidate)

Everything between the rules is one paste. `{{...}}` are filled from `candidates.jsonl`.

---
You are the **novelty adversary**. Your ONLY goal is to find the paper, dataset, or product
that makes this candidate unnecessary. You are rewarded for closing candidates with evidence
and penalised for vague "seems novel" verdicts. Return one JSON object matching the schema
below and nothing else.

**Procedure — run at least the first five steps, and log every query you run:**
1. **Exact framing**: search the candidate's own words.
2. **Output-space**: search what the candidate OUTPUTS, ignoring inputs and region.
3. **Method-space**: search the delta_claim's technique with the domain removed. The same
   method in another domain does NOT close it, but must be listed for an honest type_b.
4. **Region-swap**: search with the region removed. If the same thing exists elsewhere and the
   delta is only geographic, the verdict is `closed` under C7 hard_rejection.
5. **Product**: search "<problem> software / platform / startup". A shipping product closes as
   hard as a paper. ALWAYS fill `product_search`.
6. **Recency**: rerun your two best queries with 2026 and 2025 appended.

**Verdict definitions (constraints C7):**
- `closed` — a tier-A item has the same problem AND the same output space, or the delta is
  geographic only. One is enough. Name it in `closing_item`.
- `type_a` — you ran ≥5 queries across steps 1, 2, 4, 5; found no item with the same problem
  framing; and can name ≥3 nearest neighbours each with a one-line "differs because".
- `type_b` — ALL of: a named prior solution (url); a measurable axis on which the delta_claim
  should beat it; the specific technical choice the gain is attributed to; and whether the
  prior is deployed in the target region.
- `unclear` — literature genuinely ambiguous. State in `human_should_check` the exact question
  a human must answer.

**Rules:**
- **Do not judge from memory.** If you recall a paper but cannot find its URL by searching,
  mention it in `notes` and do NOT put it in `prior_art`.
- Every `prior_art` item needs: url, date, title, tier (A/B/C), `closes` (bool), and one
  sentence on why.
- **Dates must be `YYYY-MM` or `YYYY-MM-DD`. A bare year is invalid. Never pad a bare year to
  a month — if you cannot establish a real month, omit the item.**
- Be blunt in `reason`. A closed candidate saves the owner weeks.
- Do not propose reframes — that is the orchestrator's job. You may note in
  `nearest_neighbours_do_not` what the closest prior art does NOT do.
- `reason` ≤600 chars; `why` ≤300; `notes` ≤500; `nearest_neighbours_do_not` ≤400.

**C7 verbatim (source of truth):**
```
C7_novelty:
  rule: Must be genuinely novel. Classify as TYPE_A or TYPE_B or FAIL.
  type_a_unexplored:
    requires: no prior work attempts this problem framing
    evidence_required: adversarial search found no closing paper
  type_b_significant_improvement:
    requires_all:
      - a named prior solution exists and is beaten on a MEASURABLE axis
      - the improvement is attributable to a specific technical choice
      - the solution is unavailable in the target region
    hard_rejection: >
      "Same method, new region" is an AUTO-FAIL even if the region is
      genuinely underserved. Regional transfer alone is NOT novelty.
      There must be a technical delta, not just a geographic one.
```

**The candidate:**
- id: `{{id}}`
- one_liner: {{one_liner}}
- delta_claim: {{delta_claim}}
- region: {{region}}
- bucket: {{bucket}}
- seed_urls: {{seed_urls}}
- today: 2026-09-18
- depth: normal

**Crowded areas already identified in this run's landscape (provisional):**
{{crowded_list_areas}}

**Return exactly one JSON object with this shape and nothing else:**
```json
{
  "id": "string (required)",
  "verdict": "closed | type_a | type_b | unclear (required)",
  "reason": "string, max 600 chars (required)",
  "queries": [{"q": "string", "useful": true, "note": "optional"}],
  "prior_art": [{"url":"", "date":"YYYY-MM-DD", "title":"", "tier":"A|B|C",
                 "closes": false, "why":"max 300 chars",
                 "relation":"same_problem|same_output_space|same_method_other_domain|same_thing_other_region|product"}],
  "closing_item": null,
  "type_b_fields": null,
  "human_should_check": null,
  "nearest_neighbours_do_not": "max 400 chars",
  "budget_exhausted": false,
  "notes": "max 500 chars",
  "product_search": {
    "queries_run": ["string"],
    "shipping_products_found": [{"url":"", "date":"YYYY-MM", "title":"", "tier":"A|B|C", "note":""}]
  }
}
```
`queries` needs at least 3 entries and must record **every** search you ran, including the
useless ones. `closing_item` is required when verdict is `closed`; `type_b_fields` (all four
keys) when `type_b`; `human_should_check` when `unclear`. `product_search` is always required.

Return only the JSON.

---

> **Provenance note.** Because this runs outside the harness, `queries[]` is self-reported
> rather than observed. This repo already carries that scar: `standout__global` was recovered
> from a transcript, so its query log does not exist and the contract's "record every query"
> clause is permanently unverifiable for it. Lane A mitigates at fold-in by rejecting
> implausible pairings — a `type_a` backed by three queries is not a `type_a`. See §9.4.

### 6.3 Lane C — Codex Plus

Codex works directly in the repo on branch `v3`. Give it this brief:

> **Brief for Codex.** You are Lane C of a three-agent run. Read `RUNBOOK.md` §2, §3, §5, §6.3
> and `docs/02_subagent_contract.md` first.
>
> **Phase 0 (blocking, do first):** build `tools/check4.py` and `tools/gen_envelopes.py` to the
> contracts in §5.2 and §5.3. Then run the shared-dependency pre-check in §3.1, MOPAD first,
> writing `.research/data/_shared/<family>.json`.
>
> **Phase 1:** act as `data_verifier` for every id in §3 (Tiers A, B and C — all of them),
> following `agents/data_verifier.json` exactly. Tier C first, because a `blocked` verdict
> there kills a candidate outright and saves Lane B an expensive dispatch.
>
> **Hard rules:**
> - **A search snippet is not verification. FETCH the landing page.** If a landing page cannot
>   be fetched, that source is `unverified`, NOT `open`. The single worst failure of the last
>   run was a verifier claiming `fetched_ok: true` for a URL that never appeared in `fetched[]`.
> - Quote licence, size, coverage and date range **verbatim, ≤25 words each**. Never paraphrase
>   a licence.
> - Record every query in `queries[]` and every fetched URL in `fetched[]`.
> - Dates are `YYYY-MM` or `YYYY-MM-DD`. **A bare year is invalid; never pad it to a month.**
> - Judge compute against C9: 8 months part-time, MacBook with no CUDA, no sustained GPU, free
>   hosted compute only (GEE / Copernicus / Planetary Computer / Kaggle / Colab free tier),
>   budget MYR 200.
> - **NICFI** (R4-S58 especially): quote the purpose clause and state inside / outside /
>   borderline. Generic yield or boundary work on NICFI is **outside** and a licence fail.
> - **Singapore candidates**: the source must be drone / aerial / sub-metre AND its terms must
>   permit analytical use. OneMap and SLA basemap tiles are display-licensed unless you find
>   text saying otherwise — in that case `access_mode: unverified`.
> - Do **not** assess novelty or impact. Data only.
> - After each candidate: run `python3 tools/check4.py dat:<id>` and do not move on until it
>   prints `ok`. Append to `.research/ledger/lanec.jsonl`. Commit every 5 candidates,
>   `git add .research/data .research/ledger tools` only.
>
> Write only to `.research/data/`, `.research/dispatch/`, `.research/ledger/lanec.jsonl` and
> `tools/`. **Never** edit `gate_screen.yml`, `RUN_LOG.md`, `candidates.jsonl` or `ROSTER.md` —
> Lane A owns those and concurrent edits will corrupt the run.

---

## 7. Phase 2 — fold-in (sequential, Lane A only)

Run this whenever lanes pause, and once at the end. It is idempotent.

1. **Validate everything new**: `for f in .research/novelty/*.json; do python3 tools/check4.py nov:$(basename $f .json); done` (and the same for `dat:`). Invalid → re-dispatch once with
   the validator error appended; still invalid → log it and drop, per CLAUDE.md.
2. **Plausibility screen** (§9.4) — reject `type_a` verdicts with thin query logs.
3. **Route each candidate** into `gate_screen.yml`:
   - novelty `closed` → `fail` / `C7_novelty` (data verdict is irrelevant — apply to R4-S20 now)
   - data `blocked` → `fail` / `C9_feasibility`
   - both good → `proceed` or `proceed_conditional`
   - novelty `unclear` → `conditional`, with the human question recorded
4. **Run the constraint gate in FULL mode** (stage 6) on everything that now has both verdicts.
   This is mine and is not delegated. Expect the heavy standout cull here (C11
   `not_already_a_product`, `surprise`, `headline_claim`).
5. **Elaborate** newly-cleared candidates (stage 5) — still zero search.
6. **Write `.research/ROSTER.md`** — every PASS and CONDITIONAL, ranked by the stage-7 key
   (C7 confidence: type_a evidenced > type_b evidenced > unclear; then C8 scope count; then C4
   publishability; then C6 pitch; ties → nearer forcing-function date). **Never a single pick.**
   If lanes did not finish, write it anyway and mark it `PARTIAL — n of 63 verified`.
7. Update `RUN_LOG.md`; copy `.research/` → `research-archive/run4/`.

---

## 8. Resume procedure — after any limit, crash, or day boundary

No session state is needed. Run this and it tells you exactly what is left:

```bash
#!/usr/bin/env bash
# tools/whats_left.sh
cd "$(git rev-parse --show-toplevel)"
NV=$(awk '/^verify:/,/^verify_summary:/' .research/gate_screen.yml \
     | grep -B1 'route: not_verified' | grep -o 'R4-S[0-9]*')
echo "== novelty outstanding =="
for id in $NV; do
  [ "$id" = "R4-S20" ] && continue                      # free C7 kill, no dispatch
  [ -f ".research/novelty/$id.json" ] || echo "  nov:$id"
done
echo "== data outstanding =="
for id in $NV; do
  [ "$id" = "R4-S20" ] && continue
  [ -f ".research/data/$id.json" ] || echo "  dat:$id"
done
echo "== deep re-dispatch (unclear) =="
for id in R4-S25 R4-S28 R4-S30; do
  grep -q "\"depth\": *\"deep\"" ".research/novelty/$id.json" 2>/dev/null || echo "  nov:$id (deep)"
done
```

Then pick up at the top of the Tier A order (§3) for whatever is missing. **Ledgers are an
audit trail, not state** — if a ledger and the filesystem disagree, the filesystem wins.

---

## 9. Known defects to avoid (each of these has already bitten this project)

**9.1 Bare-year dates.** Broke two stage-2 hunters and six stage-4 outputs. The schema pattern
is `^\d{4}-\d{2}(-\d{2})?$`. A bare year is invalid and **must not be padded** to a month —
drop the item or resolve the real date from the page. Two stage-4 product entries were dropped
last run for exactly this reason, which was the correct call.

**9.2 Asserted access.** A verifier claiming `fetched_ok: true` for a URL absent from
`fetched[]` is a substantive contract violation, not a formatting slip. `dat:R4-S20` was
rejected for it. A search snippet is never verification.

**9.3 The evidence asymmetry — preserve it.** A `closed` verdict is a POSITIVE finding (a named
URL); a short search does not weaken it, and all such closures stand. A `type_a` verdict asserts
the ABSENCE of prior art and is only as strong as the search behind it. Never let a
budget-starved run produce a `type_a`. Last run this held — no `type_a` came from an exhausted
agent — and that property must survive this run too.

**9.4 Self-reported query logs (new risk this run).** Lane B runs outside the harness, so its
`queries[]` cannot be observed. At fold-in, reject as `unclear` any `type_a` whose log shows
fewer than the 5 required queries across steps 1, 2, 4, 5, or whose queries are trivial
restatements of each other. State the rejection in the ledger.

**9.5 Do not manufacture kills to hit a number.** Stage 3 produced 63 survivors against a
12–25 exit band because stage 2 over-delivered (155 vs a planned 40–80). Narrowing by
inventing failures is the same error class as region-balancing, which the skill forbids.
Region mix is an **observation, never a target.**

**9.6 Provisional landscape.** Stage 1 exited `ready_for_stage_2: false` with the India scout
dropped. Every candidate carries
`landscape_context: provisional_stage1_owner_authorized_stage2`. Crowded-area claims are
PROVISIONAL and must not be treated as established prior art — that is the adversary's job.

---

## 10. Dispatch accounting

| block | dispatches |
|---|---|
| 40 candidates × 2 roles | 80 |
| R4-S47 (novelty only — data exists) | 1 |
| R4-S50 (both) | 2 |
| R4-S20 | **0** — free C7 kill |
| deep re-dispatch of the 3 `unclear` | 3 |
| **total** | **86** |

**Tier C data-first saves up to 10** of the search-heavy adversary dispatches if their data
comes back `blocked`, which the RUN_LOG predicts for most of them.

**Split:** Lane C ≈ 41 data dispatches · Lane B ≈ 32 novelty dispatches (21 Tier A + 11 Tier B,
plus up to 10 more if Tier C survives) · Lane A = 3 deep + elaboration + fold-in.

**Realistic target for one day:** Lane B is bounded by your copy-paste patience, not by any
meter. 12–15 conversations is a good day and covers most of Tier A. Because the list is ranked,
that is a genuinely good outcome, not a partial failure.

---

## 11. Quick start

1. Lane A: `mkdir` skeleton, commit (§5.1).
2. Lane C (Codex): build `check4.py` + `gen_envelopes.py`, then MOPAD pre-check (§5.2–5.5).
3. Lane A: validate the tooling against three known-good files (§5.4). **Gate — do not proceed
   until this passes.**
4. Fan out: Lane C starts Tier C data; Lane B starts Tier A novelty at #1; Lane A elaborates
   the 8 cleared.
5. Fold in whenever convenient (§7). Stop whenever you like — §8 resumes cleanly.
