# RUNBOOK — Run 4, Stage 4 completion

**Written:** 2026-09-18 · **Branch:** `v3` · **Applies to:** finishing stage 4, then stages 5–7.
**Constraints:** v3 (`sha256:4521dc01d7545044`) — C9 gained `max_local_storage_gb: 512`.
**Revised 2026-09-22 (rev 2):** one Pro subscription, **four sessions**, full coverage retained.
Parallel lanes are gone; the schedule replaced them, not the deliverable. See §4.
All 41 data envelopes were regenerated against v3; any envelope pinning `abeba9167470f791` is stale.

This runbook finishes stage 4 on a **single Claude Pro subscription across four sessions** —
three in Claude Code and one in claude.ai web chat, which carries its own independent session
budget (§4.2). **The deliverable is the same one the three-account plan promised: all 63
candidates resolved, every survivor carrying both verdicts, in one ranked roster.** Coverage is
not traded away; only the calendar is. Read §2 and §4 before running anything — the durability
rule and the data-first ordering are what make a scarce budget produce finished verdicts
instead of half-finished ones.

**Operator's step-by-step companion: `MANUAL.md`.** This file is the design; the manual is the
keystrokes — which prompt to run, in which surface, in what order.

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

### 2.2 Sequencing — one operator, strict order

Every dispatch runs one at a time, under one operator, in one of four sessions (§4.2). There is
no concurrency to manage and no merge risk, because there is only ever one writer — **you**, and
you write every file regardless of which surface produced the verdict. What replaces the old
lane discipline is **ordering**: cheap kills before expensive confirmations (§4.3), so that a
session cut short has still produced finished verdicts rather than half-finished ones.

Commits still need `git add -f` for any `.research/` path (§9.7).

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

### 3.2 Pre-check results (Lane C, 2026-09-18, commit 63fccea)

| family | verdict | consequence |
|---|---|---|
| national orthophotos | **open** | S90, S93, S95 clear to verify |
| WeedsGalore + PhenoBench | **open** | S101 clears |
| MOPAD | **conditional** | Exists with labels, but **no licence text on any landing page** (Google Drive / Baidu links). 5 candidates held conditional; per-candidate verifiers must find a licence in the downloaded package |
| IMPaCT-UAV | **conditional** | Real (arXiv 2601.01084, spot-checked by orchestrator: 42,430 images / 415 GB / Vijayawada / 3 Jan 2026). IEEE DataPort access terms still unfetched |
| OpenET API | **conditional** | S141, S152 |
| BCA TR78 thermal archive | **blocked** | **S124 and S131 route to `fail` / C9.** No public archive exists — only inspection rules and forms. Saves 4 dispatches (2 dat + 2 nov) |

**IMPaCT-UAV size is no longer a blocker.** At 415 GB it sits under the new C9
`max_local_storage_gb: 512` ceiling (constraints v3), so S74, S75, S76 and S79 must **not** be
failed on size. Per-candidate verifiers still have to confirm IEEE DataPort access terms, and
should note that S75 needs only multispectral *metadata* (light) while S76 needs raw frames
plus orthomosaics (heaviest of the four).

---

## 4. Operating model — one subscription, four sessions

**Changed 2026-09-22 (rev 2).** The second Claude account and the Codex subscription are gone.
Phase 0 survives them — `check4.py`, `gen_envelopes.py`, all 83 envelopes and the six shared
prechecks are committed and do not care who produced them. What was lost is *parallel capacity*.

Parallel capacity buys **elapsed time**, not verdict quality. A novelty adversary running on
account 2 on Tuesday and the same adversary running in session 3 on Thursday produce the same
verdict from the same prompt against the same schema. So the correct response to losing two
accounts is to **re-schedule the work, not to shrink it**.

> **The deliverable is unchanged: all 63 candidates resolved, both verdicts on every survivor,
> one ranked roster.** An earlier draft of this section cut the target to a "verified top-20
> slice". That cut is withdrawn — §4.1 shows it was based on an estimate that double-counted
> the search budget.

### 4.1 The arithmetic, redone honestly

The binding resource is **searches**, not dispatches, and only one of the four roles is
search-hungry.

| role | dispatches | searches each | search total |
|---|---|---|---|
| novelty adversary | ~34 (40 less data kills) | ~11.7 observed (cap 15) | ~400 |
| deep re-dispatch (`unclear`) | 3 | 15 (cap) | ~45 |
| data verifier | 39 | ~4–6, fetch-led (cap 10) | ~175 |
| elaborator (stage 5) | 8 now, more as they clear | **0 — no search tools** | 0 |
| fold-in, FULL gate, roster | — | **0 — all yours** | 0 |
| | | **total** | **~620** |

Against a **200-search cap per session** that is **~3.1 sessions of search**, which four
sessions carry with ~180 searches of margin.

The superseded estimate said "~800+ searches ≈ 4+ sessions, therefore full coverage is
unreachable". It reached that by charging all 82 remaining dispatches at adversary rates. Three
corrections:

1. **The web chat session is an independent session.** claude.ai and Claude Code do not share a
   per-session cap. Web chat is therefore not a desperate fallback — it is one of the four
   planned sessions (§4.2), and it is the right home for novelty work because the novelty
   prompts are already generated and paste-ready in `.research/dispatch/nov/`.
2. **Data verification is fetch-led, and fetches did not stop when searches hit 200/200.** That
   was observed last run. Data work therefore keeps producing finished verdicts inside a session
   whose search budget is already spent — it is close to free on the binding resource.
3. **Every data kill deletes its own adversary dispatch.** Data-first (§4.3) means a `blocked`
   verdict removes ~11.7 searches of adversary work that is now never spent. The RUN_LOG
   predicts Tier C dies on C9; that is up to 10 adversary dispatches the budget never pays for.

**Margin, stated plainly.** At the caps rather than the observed rates (15/nov, 10/dat) the
total is ~1,000 searches ≈ 5 sessions. If the run tracks the cap rather than the average, §4.4
tells you what to do, and the answer is never "produce a thinner verdict".

### 4.2 What counts as a session

| # | surface | budget | carries |
|---|---|---|---|
| 1 | Claude Code | 200 searches | all 39 data verifications + free output |
| 2 | Claude Code | 200 searches | novelty, Tier A order |
| 3 | **claude.ai web chat** | independent session | novelty overflow, paste-driven (§6.3) |
| 4 | Claude Code | 200 searches | remaining novelty, 3 deep, FULL gate, roster |

Session boundaries are **budget boundaries, not calendar ones**. Two sessions can happen on one
day; one session can span two days. If a session still has capacity, carry on into the next
block; if it dies early, §8 resumes cleanly with no state to reconstruct.

Session 3 is a real session doing real work, not a contingency. It exists because novelty is the
only search-bound role and web chat is search budget that Claude Code's cap cannot touch.

### 4.3 Data-first, globally — the ordering that pays for the coverage

The old plan ran data-first only for Tier C. It now applies to **everything**, for one reason:
**a `blocked` data verdict is a complete verdict.** It kills the candidate on C9 outright, with
no novelty work needed. Data is also the cheaper role on the binding resource and the RUN_LOG
names it "the main stage-4 killer".

Running all 39 data verifications first (session 1) therefore does two things at once: it
finishes every candidate that dies on access, and it tells sessions 2–4 exactly which novelty
dispatches are still worth paying for. This is what converts a ~620-search budget into full
coverage rather than a slice.

### 4.4 The quality floor — non-negotiable, and what makes coverage safe to promise

Full coverage is only an honest target if it is never met by thinning individual verdicts. These
rules bind harder than the schedule:

1. **Never let a budget-starved agent emit `type_a`** (§9.3). A `type_a` asserts the absence of
   prior art and is only as strong as the search behind it. If a session's search budget runs
   out mid-dispatch, the verdict is **not** salvaged — bank the session (§7) and re-dispatch
   that candidate whole in the next one.
2. **A short session costs quantity, never quality.** If the run is tracking the cap rather than
   the observed rate, the correct response is a **fifth session**, not a shallower adversary.
   Coverage may slip in time; it may not slip in standard.
3. **Web-chat verdicts face the extra screen** (§9.4) before they are trusted: self-reported
   query logs, so any `type_a` with fewer than the 5 required queries across steps 1, 2, 4, 5 —
   or with queries that are trivial restatements of each other — is downgraded to `unclear`.
4. **One fresh conversation per candidate in web chat. Never batch** (§6.3). Batching is what
   produces a false `type_a`, the worst failure mode in this pipeline.
5. **Nothing is elaborated that has not passed SCREEN and both verifiers**, per CLAUDE.md. The
   schedule change does not touch the gate.

### 4.5 The insurance rule

**Every session ends by regenerating `.research/ROSTER.md` from whatever is verified at that
moment**, marked `PARTIAL — n of 63`. If sessions 3 and 4 never happen, you still hold a ranked
roster. The deliverable is never allowed to exist only in a future session.

---

## 5. Phase 0 — setup — ✅ **COMPLETE** (commit 63fccea, 2026-09-18)

> Done and verified: `tools/check4.py`, `tools/gen_envelopes.py`, 42 novelty prompts, 41 data
> envelopes, 6 shared prechecks. The §5.4 gate passed (validator confirmed to reject bad input,
> not merely to print `ok`). Envelopes were regenerated on 2026-09-22 against constraints v3.
> **Nothing here needs redoing.** The "Lane A / Lane C" labels below are a historical record of
> who did what, kept for the audit trail.

> **Housekeeping — envelope provenance.** `gen_envelopes.py` pins the SHA-256 of `RUNBOOK.md`
> into every envelope, so editing this file makes that one hash stale. It is provenance only —
> `check4.py` does not verify it and no dispatch is invalidated. To clear the drift, re-run
> `python3 tools/gen_envelopes.py` (idempotent; rewrites all 42 novelty prompts and 41 data
> envelopes from the same candidate data). Do it before session 1 or not at all — **not**
> mid-run, or half the envelopes will pin one hash and half another.

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
git add -f tools/ .research/dispatch .research/data/_shared && git commit -m "stage4: tooling + shared source precheck"
```

---

## 6. The four sessions

Session boundaries are budget boundaries, not calendar ones. If a session still has capacity,
carry on into the next block; if it dies early, §8 resumes cleanly. Step-by-step keystrokes for
each of these live in `MANUAL.md`.

**The shape:** session 1 buys information cheaply (every data verdict, every free kill), so that
sessions 2–4 spend the expensive adversary only on candidates that are still alive.

### Session 1 — Claude Code — free output, then every data verdict

1. **Elaborate the 8 cleared candidates** (stage 5) → `.research/elaborated/<id>.md`.
   **Zero searches.** R4-S22, R4-S23 (`proceed`) and R4-S01, R4-S13, R4-S15, R4-S26, R4-S35,
   R4-S42 (`proceed_conditional`). This is the output that exists no matter what follows.
2. **Apply the free kills** — no dispatch needed:
   - R4-S20 → `fail` / C7 (novelty already `closed` with evidence, §1.2.3)
   - R4-S124, R4-S131 → `fail` / C9 (BCA TR78 archive `blocked`, §3.2)
3. **Data-verify all 39 remaining candidates**, in Tier A (§3) → Tier C → Tier B order, using
   `.research/dispatch/dat/<id>.json`. Tier C is ordered early on purpose: it is where the kills
   are expected, and each kill deletes an adversary dispatch from sessions 2–4.
4. **Paste the family precheck into the envelope for any candidate in a pre-checked family**
   (§6.5). This is the single largest search saving available and it costs nothing.
5. **If the 200-search cap hits, keep going on data anyway.** Fetches are not capped (§4.1);
   a data verifier working from an injected landing-page URL needs few searches or none.
6. Fold in (§7), write the partial roster, commit.

**Exit condition:** all 39 data verdicts on disk. Every `blocked` is now a finished candidate,
and the novelty list for sessions 2–4 is exactly the set that survived.

### Session 2 — Claude Code — the expensive adversary, ranked order

1. **Novelty adversary on every surviving candidate, in Tier A §3 order**, skipping any whose
   data came back `blocked`. Expect ~17 dispatches to consume the 200-search budget.
2. **Stop at the cap. Do not compress the last dispatch to fit** (§4.4.1). Bank and carry the
   remainder into session 3.
3. Fold in, refresh the roster, commit.

### Session 3 — claude.ai web chat — novelty overflow, paste-driven

This is a planned session, not a fallback (§4.2). The prompts are already generated.

1. **Work the novelty backlog** left by session 2, continuing down the Tier A → B order.
2. **One fresh conversation per candidate** — paste the whole of `.research/dispatch/nov/<id>.md`
   and nothing else. **Never batch** (§6.3).
3. **Save each reply straight to `.research/novelty/<id>.json`.** Do not paste results back into
   Claude Code; that burns context for nothing. Validation happens in bulk in session 4.
4. Commit the saved files (`git add -f`) when you stop.

**Everything produced here is provisional until it passes the §9.4 plausibility screen in
session 4.** That screen is what keeps a self-reported query log from buying a cheap `type_a`.

### Session 4 — Claude Code — close out

1. **Validate the whole web-chat batch**: `check4.py` over everything session 3 wrote, then the
   §9.4 plausibility screen. Downgrade thin `type_a` verdicts to `unclear`; re-dispatch in-harness
   if budget allows.
2. **Novelty on whatever is still outstanding** — run `tools/whats_left.sh` (§8) rather than
   trusting any list in this file.
3. **Deep re-dispatch the 3 `unclear` adversaries** — R4-S25, R4-S28, R4-S30 — with
   `input.depth: "deep"`.
4. **Tier B `product_search` check.** The `product_search` block is load-bearing for C11 there
   (§3); a Tier B candidate whose adversary skipped it cannot pass the gate and must be
   re-dispatched, not waved through.
5. **Run the constraint gate in FULL mode** (stage 6) on everything with both verdicts. Mine,
   not delegated.
6. **Final `ROSTER.md`**, `RUN_LOG.md` update, archive to `research-archive/run4/`.

> **If session 4 ends with work outstanding, open session 5.** Per §4.4.2 the schedule flexes;
> the standard does not.

### 6.1 Per-dispatch loop (all sessions)

```
for each id, in the order above:
  dispatch the role via subagent (model: sonnet, per CLAUDE.md)
  → write .research/{novelty,data}/<id>.json
  → python3 tools/check4.py {nov,dat}:<id>     # must print ok
  → invalid? re-dispatch ONCE with the validator error appended; still invalid → log and drop
  → append to .research/ledger/
  every 5:  git add -f .research tools && git commit -m "session N: <ids>"
```

### 6.2 If the search cap hits mid-session

Claude Code's 200-search cap is per session. What you do depends on the role in flight:

1. **Data verifier in flight → keep going.** Fetches are not capped (§4.1). A data verifier
   working from an injected landing-page URL (§6.5) may need no further searches at all. This is
   why session 1 is the data session.
2. **Novelty adversary in flight → stop and bank.** Fold in, write the partial roster, commit.
   Resume in the next session via §8. **Do not let the adversary finish on a starved budget**
   (§4.4.1) — a `type_a` produced that way is exactly the failure this pipeline cannot absorb.
3. **Carry the remainder to the web chat session** (session 3). Different surface, independent
   session budget, prompts already paste-ready in `.research/dispatch/nov/`. Note that this is
   the same Pro subscription, so subscription-level limits still apply even though the
   per-session search cap does not.

### 6.3 Rules for the web chat session (session 3)

1. **One fresh conversation per candidate. Never batch.** Verdict quality tracks search depth.
   Batch five and the model shortcuts, producing a **false `type_a`** — an assertion that no
   prior art exists. That is the worst failure mode in this pipeline.
2. **Never put a novelty and a data prompt in the same thread** — the contract requires that
   neither verifier sees the other's output.
3. **Save the reply straight to `.research/novelty/<id>.json`.** Do not paste it back into
   Claude Code; that burns context for nothing. Validation happens in bulk with `check4.py`.
4. Verdicts produced this way have self-reported query logs — see the provenance note in §6.4
   and the plausibility screen in §9.4.

### 6.4 What each generated novelty prompt contains

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
> clause is permanently unverifiable for it. The fold-in step mitigates this by rejecting
> implausible pairings — a `type_a` backed by three queries is not a `type_a`. See §9.4.

### 6.5 Injecting the family precheck — the cheapest search saving available

Six dataset families were already resolved once, in §3.2, and the results sit in
`.research/data/_shared/<family>.json` with **fetched landing-page URLs**. The generated data
envelopes do **not** carry those results, so a verifier dispatched bare will re-discover the
MOPAD landing page from scratch — spending searches on a question answered on 2026-09-18.

**Before dispatching `dat:<id>` for any candidate in a pre-checked family, append the family's
precheck JSON to the envelope's input**, with this instruction:

```
Shared pre-check already performed for this family — do NOT re-discover the landing page.
Start from the fetched URLs below. Your remaining job is the candidate-specific part:
the licence text inside the downloaded package, the size/subset question against C9,
and the ground-truth path.
<contents of .research/data/_shared/<family>.json>
```

| family | candidates | precheck file |
|---|---|---|
| MOPAD | S108, S110, S113, S115, S118 | `mopad.json` |
| IMPaCT-UAV | S74, S75, S76, S79 | `impact_uav.json` |
| national orthophotos | S90, S93, S95 | `national_orthophotos.json` |
| OpenET API | S141, S152 | `openet_api.json` |
| WeedsGalore + PhenoBench | S101 | `weedsgalore_phenobench.json` |
| BCA TR78 thermal | S124, S131 | `bca_tr78_thermal_archive.json` — **blocked, do not dispatch** |

That is **15 of the 39 data dispatches** starting from a fetched URL instead of a cold search.

**This does not weaken the verdict.** The precheck was itself a fetched-page verification, and
every unresolved question it left is named in its `required_followup` — which the per-candidate
verifier still has to answer. §9.2 still applies in full: `fetched_ok: true` for a URL absent
from `fetched[]` is a contract violation, injected precheck or not.

---

## 7. Fold-in — run at the end of EVERY session

Idempotent. This is also what produces the insurance roster (§4.5), so never skip it because a
session felt short.

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

No session state is needed. `tools/whats_left.sh` derives the remaining work from the filesystem:

```bash
bash tools/whats_left.sh
```

It prints four blocks — novelty outstanding, data outstanding, deep re-dispatches, and the free
kills to confirm routed. **On a clean start it reconciles exactly to the §10 accounting:
40 novelty + 3 deep + 39 data = 82.** If it does not, trust the script and fix the accounting,
not the other way round.

What it already knows, so you do not have to remember it:

- **The three free kills are excluded** — R4-S20 (C7, novelty already `closed`) and R4-S124 /
  R4-S131 (C9, BCA TR78 `blocked`). It excludes them explicitly rather than waiting for fold-in
  to route them, so the list is correct before session 1 has run as well as after.
- **R4-S47 is excluded from the data list** — it has no data envelope by design; its data
  verdict is already `conditional`. It needs novelty only.

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

**9.4 Self-reported query logs.** The web chat session (§6.3, session 3) runs outside the
harness, so its `queries[]` cannot be observed. At fold-in, reject as `unclear` any `type_a` whose log shows
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

**9.7 `.research/` is gitignored — a plain `git add` silently does nothing.** `.gitignore`
line 2 is `.research/*` (by design: "current-run working files are ephemeral; archives are
committed"). Consequence: **every `git add` of a `.research/` path must use `-f`**, or the
commit succeeds while committing nothing and you believe work is saved when it is not.

As of 2026-09-18 the entire run-4 state — `gate_screen.yml`, `candidates.jsonl`,
`RUN_LOG.md`, and all 42 existing verifier outputs — is **untracked, working-tree only**.
Session limits do not threaten it (files persist on disk), but a stray `git clean -fdx`
would erase the whole run. See §9.8 for the recommended fix.

**9.8 Recommended `.gitignore` change (owner's call).** Narrow the ignore so durable outputs
are tracked while genuinely ephemeral files stay out:

```gitignore
.research/*
!.research/README.md
!.research/novelty/
!.research/data/
!.research/dispatch/
!.research/ledger/
!.research/gate_screen.yml
!.research/candidates.jsonl
!.research/RUN_LOG.md
```

The directory itself must be un-ignored before git will descend into it — negating only the
files does not work. With this in place, `-f` is no longer needed for those paths.

---

## 10. Dispatch accounting (revised 2026-09-22, rev 2)

| block | dispatches |
|---|---|
| novelty, 42 generated | 42 |
| less R4-S124, R4-S131 (BCA TR78 blocked) | −2 |
| data, 41 generated | 41 |
| less R4-S124, R4-S131 | −2 |
| deep re-dispatch of the 3 `unclear` | +3 |
| **remaining total** | **82** |
| R4-S20 | 0 — free C7 kill |

**All 82 are in scope.** The top-20 slice is withdrawn (§4).

### 10.1 Expected search draw per session

| session | surface | work | searches |
|---|---|---|---|
| 1 | Claude Code | 8 elaborations (0) + 3 free kills (0) + **39 data** | ~175 |
| 2 | Claude Code | novelty ×~17, Tier A order | ~200 (cap-bound) |
| 3 | web chat | novelty ×~14, paste-driven | independent budget |
| 4 | Claude Code | novelty remainder + 3 deep + re-dispatches + FULL gate | ~150 |
| | | **total** | **~620 + web chat** |

Novelty is charged at the observed 11.7 searches, not the 15 cap. At the cap the total is
~1,000 and the run needs a fifth session — see §4.4.2. **Add the session; do not thin the
verdict.**

### 10.2 What full coverage means here

63 candidates: 20 already carry both verdicts (§1.3) · 3 are free kills (R4-S20, R4-S124,
R4-S131) · 9 already `fail` · the remaining 31 get both verdicts across sessions 1–4, plus the
3 `unclear` deepened. Nothing is left `not_verified` by design — only by a session that ran out,
and §4.5 makes that state visible in the roster rather than silent.

**Free work, no searches:** 8 elaborations in session 1, plus one per candidate that clears at
any later fold-in (§7.5) — up to the 15-dispatch stage-5 ceiling — plus 3 free kills and every
fold-in, gate and roster pass.

---

## 11. Quick start (session 1)

> Keystroke-level instructions, including the exact prompts and which surface to run them in,
> are in **`MANUAL.md`**. This is the summary.

1. *(Optional, once)* `python3 tools/gen_envelopes.py` to clear the RUNBOOK hash drift (§5).
2. Elaborate the 8 cleared candidates — zero searches, guaranteed output.
3. Apply the 3 free kills (R4-S20, R4-S124, R4-S131).
4. Data-verify all 39 from `.research/dispatch/dat/`, Tier A → Tier C → Tier B, injecting the
   family precheck where §6.5 has one.
5. Keep going on data after the search cap — fetches are not capped.
6. Fold in (§7) → partial `ROSTER.md` → `git add -f` → commit.

Phase 0 (§5) is **complete** — tooling, envelopes and prechecks are committed at 63fccea.
Nothing there needs redoing.
