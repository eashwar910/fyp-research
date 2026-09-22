# MANUAL — how to actually run stage 4

**Companion to `RUNBOOK.md`.** The runbook is the design and the justification; this is the
keystrokes. Where they disagree, the runbook wins — but tell me, because it means one of them
is stale.

**Written:** 2026-09-22 · **Branch:** `v3` · **Plan:** one Pro subscription, four sessions,
full coverage of all 63 candidates.

---

## 0. How to read this

Every step is tagged with the surface it runs in:

| tag | means |
|---|---|
| 🖥️ **CC** | Claude Code, in this repo. You type the prompt; the orchestrator dispatches Sonnet subagents. |
| 🌐 **WEB** | claude.ai web chat, in a browser. You paste a prompt by hand and save the reply by hand. |
| ⌨️ **SHELL** | A command you run yourself in the terminal. |

Blocks marked **PASTE THIS** are literal — copy them whole, including the numbered lines. They
are written for the orchestrator, not for you, so they will read oddly in places. That is fine.

**The one rule that matters more than the schedule:** if a session runs out of search budget
mid-dispatch, you stop and bank. You never let an adversary finish on an empty budget. A
`type_a` verdict produced that way asserts "no prior art exists" on the strength of three
searches, and that is the one failure this pipeline cannot recover from. See §7.

---

## 1. Before session 1 — one-time preflight

### ⌨️ SHELL 1.1 — confirm the gate is clear

```bash
cd ~/Documents/Projects/FYP
git branch --show-current                  # expect: v3
awk '/^todo:/,/^[a-z_]+:$/' constraints.yml # expect: "todo:" and nothing under it
```

If anything is listed under `todo:`, **stop.** CLAUDE.md says resolve it with the owner first.

### ⌨️ SHELL 1.2 — clear the envelope hash drift

`gen_envelopes.py` pins the SHA-256 of `RUNBOOK.md` into all 83 envelopes. The runbook was just
rewritten, so that hash is stale. It is provenance only — nothing validates it — but clear it
now so every envelope in the run pins the same thing.

```bash
python3 tools/gen_envelopes.py     # expect: wrote 42 novelty prompts / wrote 41 data envelopes
```

**Do this before session 1 or not at all.** Never mid-run, or half your envelopes pin one hash
and half another, and the audit trail stops meaning anything.

### ⌨️ SHELL 1.3 — decide the `.gitignore` question (recommended)

Right now all of `.research/` is ignored, so every commit needs `git add -f`, and a stray
`git clean -fdx` would delete the entire run. Runbook §9.8 has the fix. If you apply it, you can
drop the `-f` everywhere below. If you don't, **every `git add` of a `.research/` path in this
manual must keep its `-f`.**

### ⌨️ SHELL 1.4 — snapshot before you start

```bash
git add -f .research tools RUNBOOK.md MANUAL.md
git commit -m "stage4: rev-2 runbook + operator manual, pre-session-1 snapshot"
```

---

## 2. 🖥️ Session 1 — Claude Code — free output, then every data verdict

**Goal:** 8 elaborations, 3 free kills, and all 39 data verdicts on disk.
**Budget:** ~175 searches of the 200 cap.
**Why first:** every `blocked` data verdict is a *finished* candidate, and it deletes a ~12-search
adversary dispatch from a later session. This session is what pays for full coverage.

### 2.1 — launch

```bash
cd ~/Documents/Projects/FYP && claude
```

### 2.2 — 🖥️ CC — orient the orchestrator

> **PASTE THIS**
>
> Session 1 of the four-session stage-4 plan. Read `RUNBOOK.md` §4 and §6 (Session 1) before
> doing anything, then confirm back to me in five lines: the session goal, the search budget,
> the dispatch order, what you will do when the search cap hits, and what you are forbidden
> from doing this session. Do not dispatch anything yet.

Check the answer says: **data only, no novelty this session**, and **keep going on data after
the cap because fetches are not capped**. If it says anything about a top-20 slice, it is reading
a stale copy — tell it §4 was revised and the slice is withdrawn.

### 2.3 — 🖥️ CC — the free output (zero searches)

> **PASTE THIS**
>
> Step 1 — elaborate the 8 already-cleared candidates (stage 5). Zero searches; the elaborator
> has no search tools.
>
> `proceed`: R4-S22, R4-S23
> `proceed_conditional`: R4-S01, R4-S13, R4-S15, R4-S26, R4-S35, R4-S42
>
> For each: dispatch the elaborator (model: sonnet, `agents/elaborator.json`) with that
> candidate's `.research/novelty/<id>.json` and `.research/data/<id>.json` as input. Write the
> result to `.research/elaborated/<id>.md`. Do not upgrade either verdict. If the elaborator
> returns `needs=[...]`, record it and move on — do not go fetch it.
>
> Then commit: `git add -f .research && git commit -m "session1: 8 elaborations"`

### 2.4 — 🖥️ CC — the three free kills (zero searches, zero dispatches)

> **PASTE THIS**
>
> Step 2 — apply the three free kills directly in `.research/gate_screen.yml`. No dispatches.
>
> - **R4-S20** → `fail` / `C7_novelty`. Its novelty verdict is already `closed` with evidence in
>   `.research/novelty/R4-S20.json`. Also fix its stale `note:` field, which claims no evidence
>   exists and contradicts its own verdict.
> - **R4-S124** → `fail` / `C9_feasibility`. BCA TR78 archive `blocked` (`.research/data/_shared/bca_tr78_thermal_archive.json`).
> - **R4-S131** → `fail` / `C9_feasibility`. Same precheck, same reason.
>
> Commit.

### 2.5 — 🖥️ CC — the data sweep (the main event)

> **PASTE THIS**
>
> Step 3 — data verification sweep. All 39 remaining candidates, this session.
>
> Order (Tier A, then Tier C, then Tier B — Tier C early on purpose, that is where the kills are):
>
> A: R4-S93 R4-S101 R4-S75 R4-S74 R4-S103 R4-S76 R4-S79 R4-S90 R4-S95 R4-S113 R4-S110
>    R4-S115 R4-S108 R4-S104 R4-S50 R4-S58 R4-S65 R4-S67 R4-S60 R4-S64
> C: R4-S83 R4-S118 R4-S127 R4-S132 R4-S133 R4-S134 R4-S147 R4-S148
> B: R4-S141 R4-S152 R4-S151 R4-S150 R4-S137 R4-S142 R4-S144 R4-S136 R4-S145 R4-S146 R4-S153
>
> For each id:
> 1. Dispatch `data_verifier` (model: sonnet) using `.research/dispatch/dat/<id>.json` as input.
> 2. **If the candidate is in a pre-checked family (RUNBOOK §6.5), append that family's
>    `.research/data/_shared/<family>.json` to the envelope, with the "do NOT re-discover the
>    landing page" preamble from §6.5.** This applies to 15 of the 39 and is the main search saving.
> 3. Write the result to `.research/data/<id>.json`.
> 4. Run `python3 tools/check4.py dat:<id>` — it must print exactly `ok`.
> 5. Invalid → re-dispatch ONCE with the validator error appended. Still invalid → log it in
>    `.research/ledger/` and drop, per CLAUDE.md.
> 6. Every 5 ids: `git add -f .research tools && git commit -m "session1 data: <ids>"`
>
> Hard rules for this session:
> - **No novelty dispatches at all.** Not even for a candidate that looks obviously novel.
> - **R4-S47 has no data envelope and needs none** — its data verdict is already `conditional`.
>   It needs novelty only, in session 2.
> - `fetched_ok: true` for a URL that is not in `fetched[]` is a contract violation, not a
>   formatting slip. Reject it and re-dispatch.
> - Dates are `YYYY-MM` or `YYYY-MM-DD`. A bare year is invalid and **must not be padded**.
> - **When the 200-search cap hits, keep going.** Fetches are not capped, and family-precheck
>   candidates need few searches or none. Only stop if fetches start failing too.
>
> Report after every 5: ids done, verdicts, and searches remaining if you can see it.

### 2.6 — 🖥️ CC — fold in and bank

> **PASTE THIS**
>
> Step 4 — fold-in, per RUNBOOK §7. Validate everything new, route each candidate in
> `gate_screen.yml` (data `blocked` → `fail`/`C9_feasibility`), then write
> `.research/ROSTER.md` marked `PARTIAL — n of 63 verified`, ranked by the stage-7 key. Every
> PASS and CONDITIONAL, never a single pick.
>
> Then tell me exactly two things:
> 1. How many candidates died on data, and which — that is the novelty list that just got shorter.
> 2. The exact remaining novelty backlog, from `tools/whats_left.sh`, in Tier A order.
>
> Commit with `git add -f`.

**Write down that novelty backlog.** Sessions 2 and 3 work from it.

---

## 3. 🖥️ Session 2 — Claude Code — the expensive adversary

**Goal:** ~17 novelty verdicts, in ranked order.
**Budget:** the full 200-search cap. This is the search-bound session.

### 3.1 — 🖥️ CC — dispatch

> **PASTE THIS**
>
> Session 2 of four. Novelty adversary only. Read `RUNBOOK.md` §6 (Session 2) and §9.3 first.
>
> 1. Run `bash tools/whats_left.sh` and work the novelty list it prints, in Tier A order
>    (RUNBOOK §3), **skipping any candidate whose data verdict came back `blocked`** — those are
>    already finished and the adversary must never be spent on them.
> 2. For each id: dispatch `novelty_adversary` (model: sonnet) using the generated prompt at
>    `.research/dispatch/nov/<id>.md`. Write the result to `.research/novelty/<id>.json`.
> 3. `python3 tools/check4.py nov:<id>` must print `ok`. Invalid → re-dispatch once with the
>    error appended; still invalid → log and drop.
> 4. Every 5: `git add -f .research && git commit -m "session2 nov: <ids>"`
>
> **Stop conditions — these bind harder than finishing the list:**
> - When the search budget will not cover a *whole* adversary dispatch (~12–15 searches), **stop.**
>   Do not start one you cannot finish. Do not compress one to fit.
> - Any verdict that comes back with `budget_exhausted: true` is **not accepted**. Re-dispatch it
>   whole next session.
> - A `type_a` requires ≥5 queries across steps 1, 2, 4, 5 and ≥3 named nearest neighbours. Fewer
>   than that is `unclear`, not `type_a`.
> - `product_search` is mandatory on every verdict and load-bearing for Tier B. A Tier B verdict
>   without it cannot pass the gate — reject and re-dispatch.
>
> End with the §7 fold-in and a refreshed PARTIAL roster, then tell me the exact list of ids
> still needing novelty. I am taking that list to web chat.

### 3.2 — ⌨️ SHELL — export the backlog for session 3

```bash
bash tools/whats_left.sh | sed -n '/novelty outstanding/,/data outstanding/p'
```

Keep that list next to you for the next session.

---

## 4. 🌐 Session 3 — claude.ai web chat — novelty overflow

**This is a planned session, not a rescue.** Web chat carries its own session budget that Claude
Code's 200-search cap cannot touch. It is the right home for novelty because the prompts are
already fully generated — you are not writing anything, just ferrying.

**It is also the session where quality is easiest to lose.** Everything here has a self-reported
query log that nobody observed. §4.4 exists because of that.

### 4.1 — the loop, per candidate

Do this **once per id**, from the top of your backlog list.

**⌨️ SHELL — copy the prompt:**

```bash
cat .research/dispatch/nov/R4-S93.md | pbcopy      # substitute the id
```

**🌐 WEB — run it:**

1. Open claude.ai and start a **brand new conversation**. Not a new message in an old one.
2. Paste. Send. Add nothing — no "please be thorough", no context, no follow-up. The prompt is
   the contract; anything you add is an uncontrolled variable.
3. Wait for the full JSON.

**⌨️ SHELL — save the reply:**

Copy the JSON out of the browser, then:

```bash
pbpaste > .research/novelty/R4-S93.json
python3 tools/check4.py nov:R4-S93                 # must print exactly: ok
```

If the model wrapped it in a markdown fence, strip it first:

```bash
pbpaste | sed '/^```/d' > .research/novelty/R4-S93.json
```

If `check4.py` reports violations, **paste the violations back into that same conversation** and
ask for a corrected JSON object. That is the one follow-up message that is allowed.

**⌨️ SHELL — commit every few:**

```bash
git add -f .research/novelty && git commit -m "session3 web: <ids>"
```

### 4.2 — the four rules you personally enforce here

1. **One fresh conversation per candidate. Never batch.** Batch five and the model shortcuts and
   hands you a false `type_a` — an assertion that no prior art exists. Worst failure mode in the
   pipeline, and it is invisible downstream.
2. **Never put a novelty and a data prompt in the same thread.** The contract requires that
   neither verifier sees the other's output.
3. **Do not paste results back into Claude Code.** Save to disk. Claude Code reads them in bulk
   in session 4. Pasting burns context for nothing.
4. **Do not help the model.** If it asks a clarifying question, say "follow the prompt as
   written". If it says it cannot search, stop and note the id — that candidate goes back to
   Claude Code, because a non-searching adversary is worthless.

### 4.3 — when to stop

Stop when the backlog is empty, or when web chat starts rate-limiting you. Either way, commit
what you have and note where you stopped. Session 4 recomputes the remainder from disk anyway —
there is no state to hand over.

---

## 5. 🖥️ Session 4 — Claude Code — validate, finish, close out

**Goal:** everything validated, every gap closed, FULL gate run, final roster.

### 5.1 — 🖥️ CC — screen the web-chat batch first

> **PASTE THIS**
>
> Session 4 of four. Before any new dispatch, audit what session 3 produced in web chat. Read
> `RUNBOOK.md` §9.4 and §4.4 first.
>
> 1. Run `check4.py nov:<id>` over every novelty file written since session 2 ended. List failures.
> 2. Then run the **plausibility screen** on every one that passed, because these query logs are
>    self-reported and unobserved:
>    - `type_a` with fewer than 5 queries across steps 1, 2, 4, 5 → **downgrade to `unclear`**
>    - `type_a` whose queries are trivial restatements of each other → **downgrade to `unclear`**
>    - any verdict missing `product_search` → reject
>    - any `prior_art` entry with a bare year, or a URL you cannot resolve → drop the entry and
>      say so
> 3. Give me a table: id, verdict as returned, verdict after screening, and why it changed.
> 4. Re-dispatch in-harness any candidate you downgraded, if budget allows — an observed verdict
>    beats a screened one.
>
> Note the asymmetry from §9.3 and apply it: a `closed` verdict is a positive finding backed by a
> named URL, so a short query log does **not** weaken it. Only `type_a` is vulnerable to a thin
> search. Do not downgrade closures.

### 5.2 — 🖥️ CC — close the remaining gaps

> **PASTE THIS**
>
> 1. Run `bash tools/whats_left.sh`. **Trust it over any list in the runbook or the manual** —
>    the filesystem is the state.
> 2. Dispatch novelty for anything still outstanding, Tier A order, same rules as session 2.
> 3. Deep re-dispatch the three `unclear` adversaries — R4-S25, R4-S28, R4-S30 — with
>    `input.depth: "deep"` in the envelope.
> 4. Check every Tier B candidate has a populated `product_search`. C11's
>    `not_already_a_product`, `surprise` and `headline_claim` are evaluated at the FULL gate and
>    depend on it. Missing → re-dispatch, do not wave through.
> 5. Commit every 5 with `git add -f`.

### 5.3 — 🖥️ CC — the FULL gate (yours, not delegated)

> **PASTE THIS**
>
> Run the `fyp-constraint-gate` skill in **FULL mode** on every candidate that now has both
> verdicts. This is stage 6 and per CLAUDE.md it is yours — do not delegate it to a subagent.
>
> Expect a heavy cull in the standout bucket. Report the verdict table before you write anything.

### 5.4 — 🖥️ CC — final deliverable

> **PASTE THIS**
>
> Final fold-in, per RUNBOOK §7:
> 1. Elaborate every newly-cleared candidate (stage 5, zero searches).
> 2. Write the final `.research/ROSTER.md`: **every PASS and CONDITIONAL, ranked**, with reframes.
>    Never a single pick. Rank by the stage-7 key: C7 confidence (type_a evidenced > type_b
>    evidenced > unclear), then C8 scope count, then C4 publishability, then C6 pitch, ties broken
>    by nearer forcing-function date.
> 3. If anything is still unverified, mark it `PARTIAL — n of 63` and list exactly what is missing
>    and why. Do not quietly drop it.
> 4. Update `.research/RUN_LOG.md`, then copy `.research/` → `research-archive/run4/`.
> 5. Commit everything with `git add -f`.
>
> Then tell me, in plain terms: how many candidates are on the roster, how many died and on which
> constraint, and what you would flag as the weakest verdict in the top five.

---

## 6. If something goes wrong

| symptom | do this |
|---|---|
| Session died mid-dispatch | Nothing is lost but the in-flight dispatch. Run `bash tools/whats_left.sh` and carry on. There is no state to restore. |
| A commit "succeeded" but committed nothing | You forgot `-f`. `.research/` is gitignored (§9.7). Re-run with `git add -f`. |
| `check4.py` rejects a file that was fine last run | The validator is wrong, not the file (§5.4). Fix the validator before dispatching anything else. |
| A ledger and the filesystem disagree | **The filesystem wins.** Ledgers are an audit trail, not state. |
| An agent returns `budget_exhausted: true` | Do not accept the verdict. Re-dispatch it whole next session. |
| Web chat refuses to search | That id goes back to Claude Code. A non-searching adversary produces nothing usable. |
| Search cap hit and work remains | Bank it. Open the next session. **Never** compress a dispatch to fit (§4.4.2). |
| Four sessions end with work outstanding | Open a fifth. The schedule flexes; the standard does not. |

---

## 7. The five things only you can enforce

The orchestrator will follow the runbook. These are the ones that need a human, because they are
all cases where the cheap path looks like the finished path.

1. **A starved `type_a` is worse than no verdict.** It asserts an absence. If budget ran thin,
   re-dispatch — do not accept and move on.
2. **Never batch in web chat.** One conversation, one candidate. This is the single highest-risk
   step in the whole run and it costs nothing but patience.
3. **`fetched_ok: true` must be backed by an entry in `fetched[]`.** A search snippet is not
   verification. This already got one verdict rejected last run.
4. **Bare years are invalid and must never be padded to a month.** This one defect broke two
   stage-2 hunters and six stage-4 outputs. Dropping the item is the correct call.
5. **Do not manufacture kills to hit a number, and do not balance regions.** 63 survivors against
   a 12–25 exit band is an observation, not a problem to fix. Region mix is never a target.

---

## 8. Quick reference

```bash
# where am I
bash tools/whats_left.sh

# validate one result
python3 tools/check4.py nov:R4-S93
python3 tools/check4.py dat:R4-S93

# validate everything
for f in .research/novelty/*.json; do python3 tools/check4.py nov:$(basename $f .json); done
for f in .research/data/*.json;    do python3 tools/check4.py dat:$(basename $f .json); done

# web chat ferry (macOS)
cat .research/dispatch/nov/<id>.md | pbcopy
pbpaste | sed '/^```/d' > .research/novelty/<id>.json

# commit (the -f is mandatory while .research/ is ignored)
git add -f .research tools && git commit -m "..."
```

| | session 1 | session 2 | session 3 | session 4 |
|---|---|---|---|---|
| surface | 🖥️ CC | 🖥️ CC | 🌐 WEB | 🖥️ CC |
| role | data ×39 | novelty ×~17 | novelty ×~14 | novelty rest + 3 deep |
| plus | 8 elaborations, 3 free kills | — | — | FULL gate, final roster |
| searches | ~175 | ~200 | independent | ~150 |
