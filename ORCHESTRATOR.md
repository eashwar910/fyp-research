# ORCHESTRATOR.md — run 4 playbook

You are the judge and router. Subagents are the eyes. This document is the
sequence; `docs/01_pipeline.md` has the per-stage contracts; `agents/*.json`
has the exact prompts you dispatch.

Naming: a **dispatch** is one subagent invocation = one `agents/*.json` prompt
+ one `input` object. Every dispatch returns one JSON object validated against
the schema named in the prompt file. You never accept prose from a subagent.

Context discipline: you hold only (a) constraints.yml, (b) buckets.yml,
(c) the JSON results, (d) the run log. You do not hold fetched web pages.
If you find yourself reading a paper, you are doing a subagent's job.

---

## Stage 0 — Preflight (you, no dispatch)

1. Read `constraints.yml`. If `todo:` has any item without `resolved: true`, STOP.
   Print the open items and ask the owner. Do not proceed on assumptions.
2. Read `buckets.yml`. If any bucket has `status: placeholder`, STOP the same way.
3. Read every `research-archive/*/gate_verdicts.yml` and build the **archive index**:
   `{id, one_liner, verdict, failed_gate, reason}` for every prior candidate.
   You will hand this index to hunters (as "do not restate") and to the gate.
4. Create `.research/RUN_LOG.md` from `docs/05_run_log_template.md`. Record run id,
   date, constraints version, bucket definitions hash.

Exit: RUN_LOG stage 0 block filled; archive index written to `.research/archive_index.json`.

---

## Stage 1 — Landscape (3 dispatches, parallel)

Prompt: `agents/landscape_scout.json`
Dispatch once per job market with `input.market ∈ {india, singapore_malaysia, eu}`.
(`singapore_malaysia` now also feeds the Malaysia region in stage 2; tell that
scout to give Malaysian companies and MPOB/EUDR-palm forcing functions equal
weight to Singapore ones.)

What you want back (schema `schemas/landscape_report.schema.json`):
- companies actively shipping, with product one-liners and evidence URLs dated ≤ 12 months
- what they are hiring for (job-post URLs, not vibes)
- what a fresher FYP would signal to each
- **forcing functions**: regulations, subsidies, deadlines, dataset releases with dates
- **crowded list**: problem areas with ≥ 5 recent papers or ≥ 2 commercial products

Merge: concatenate crowded lists (dedupe), union forcing functions. Write
`.research/landscape/merged.json` and a 1-page human summary
`.research/landscape/SUMMARY.md`.

Exit: three valid reports; merged crowded list has ≥ 10 entries (if fewer, the
scouts were lazy — re-dispatch with `input.depth: "deep"`).

---

## Stage 2 — Gap hunt (N dispatches, parallel)

Prompts: `agents/gap_hunter.json`
Dispatch matrix: for each bucket in `buckets.yml` × each region listed in that
bucket. Run 4: bucket_1 × {india, eu, malaysia, singapore_source_basket},
bucket_2 × {india, eu, malaysia, singapore}, bucket_3 (standout) × {global}
= 9 dispatches. The standout hunter gets a higher target count and must fill
`standout_fields` on every line.

Each hunter receives: its bucket block, constraints.yml, `landscape/merged.json`,
and the archive index. Nothing else.

What you want back (schema `schemas/candidate_oneliner.schema.json`, array):
20–30 one-liners each, every one with `region`, `data_class`, `bucket`,
`delta_claim` (one clause: what is new), `forcing_function` (or null),
`crowded_area_entered` (bool) and `seed_urls` (1–3 URLs that made the hunter
think this is a gap).

Merge: assign run-scoped ids (`R4-S01`…), dedupe by semantic similarity — if two
hunters produced the same idea, keep one, note both sources. Write
`.research/candidates.jsonl`.

Exit: 40–80 unique one-liners. Fewer than 40 → re-dispatch the thinnest
hunters with `input.avoid` = the ids already produced.

---

## Stage 3 — SCREEN gate (you, no dispatch)

Run `.claude/skills/fyp-constraint-gate/SKILL.md` in SCREEN mode on
`candidates.jsonl`. Four gates only, in order: C3 patterns → C1 imagery-native
(skip for SG and for `standout`; for `standout` run C11's two cheap checks —
layperson sentence and demo moment — in its place) → exclusions → C7
regional-transfer sniff. Read `constraints.yml bucket_exemptions` first. Also apply the archive
check: if a one-liner restates an archived candidate, mark `restates: <id>` and
inherit that candidate's verdict unless the `delta_claim` explicitly addresses
the archived `failed_gate`.

Write `.research/gate_screen.yml`. Expect 60–75 % kill. If < 50 % killed,
re-read the C3 list and do it again; you are being generous.

Exit: `screen_pass` list of 12–25 candidates.

---

## Stage 4 — Verify (2 dispatches per survivor, parallel)

This stage is new in run 4 and is the fix for F4. Every `screen_pass` gets BOTH:

**4a. Novelty adversary** — `agents/novelty_adversary.json`
Input: the one-liner, its `delta_claim`, its `seed_urls`, the crowded list.
The adversary's job is to KILL the candidate: find the closing paper or product.
Returns `schemas/novelty_verdict.schema.json`: `verdict ∈ {closed, type_a, type_b, unclear}`,
≥ 3 documented queries, every prior-art item with URL + date + one-line
"why this does/doesn't close it", and for type_b the **named prior solution**
and **measurable axis**.

**4b. Data verifier** — `agents/data_verifier.json`
Input: the one-liner, its `data_class`, region.
Fetches the actual landing page of every dataset/imagery source the candidate
needs. Returns `schemas/data_verification.schema.json`: per source → URL,
licence text (verbatim ≤ 25 words), access mode (open / registration / academic
program / paid), size, coverage of target region, **ground-truth existence**
(where labels come from, or "must be constructed" + how), NICFI purpose check
if NICFI is used, compute path (GEE / Planetary Computer / Kaggle / Colab).

Routing after 4:
- novelty `closed` → verdict FAIL C7, stop. Record the closing URL.
- data `blocked` (no access, no ground truth path) → FAIL C9, stop.
- novelty `unclear` after a second adversary pass with `input.depth: "deep"` →
  treat as CONDITIONAL with reframe "run a human literature check on X".
- both clear → proceed to stage 5.

Write `.research/novelty/<id>.json`, `.research/data/<id>.json`, and update
`.research/gate_screen.yml` with a `verify:` block per candidate.

Exit: every survivor has both files; routing decisions logged.

---

## Stage 5 — Elaborate (1 dispatch per cleared survivor, parallel)

Prompt: `agents/elaborator.json`
Input: the one-liner, novelty verdict, data verification, constraints.yml,
the relevant landscape entries (companies + forcing functions for that region).

Returns `schemas/elaborated_candidate.schema.json`: components (≥ 2), research
question, non-obvious failure mode, reusable artifact, named user + decision
changed, compute plan on free tiers, 8-month part-time phase plan, C6 pitch,
and — mandatory — `what_would_kill_this` (the elaborator's own best attack).

The elaborator may NOT run new searches. It works only from the verified
inputs. If it needs a fact it doesn't have, it returns `needs: [...]` and you
dispatch the data verifier or adversary again.

Write `.research/elaborated/<id>.json`.

---

## Stage 6 — FULL gate (you, no dispatch)

Run the gate in FULL mode on every elaborated candidate. All hard gates, then
soft scores. `standout` candidates skip C1/C2 and must clear C11 with the
adversary's `product_search` as evidence for `not_already_a_product`. Verdicts PASS / CONDITIONAL / FAIL with reframes written out in
full (the skill forbids "could be adjusted"). Use the novelty verdict for C7 —
do not re-judge from memory. Use the data verification for C9 — do not
re-judge from memory.

Write `.research/gate_verdicts.yml` in the skill's format, plus `region_mix`
as an observation.

---

## Stage 7 — Roster + archive (you)

1. Write `.research/ROSTER.md`: every PASS and CONDITIONAL ranked. Ranking key,
   in order: C7 confidence (type_a evidenced > type_b evidenced > unclear),
   C8 scope count, C4 publishability, C6 pitch. Ties → the one whose forcing
   function has the nearer date.
2. For each roster entry, one paragraph a human can read + the pitch + the
   three URLs that matter most.
3. Report to the owner ONLY: counts, region mix, the 2–3 most interesting
   CONDITIONALs with reframes. Do not narrate fails.
4. Copy `.research/` → `research-archive/run4/`. The next run's stage 0 will
   index it.

---

## Failure handling

| Situation | Action |
|---|---|
| Subagent returns invalid JSON | Re-dispatch once with the validator error appended to input. Second failure → drop, log. |
| Subagent returns prose | Same as invalid JSON. |
| Subagent cites a URL that 404s on spot-check | Re-dispatch that verdict with `input.reverify: [url]`. |
| Hunter output < 15 lines | Re-dispatch with `input.depth: "deep"` and the crowded list emphasised. |
| Two hunters disagree on whether an area is crowded | Adversary decides in stage 4. Do not resolve it yourself. |
| Owner asks for a single winner | Decline; point to ROSTER.md and F3. |
| Context pressure | Drop fetched content, never drop JSON results. Summaries of JSON are allowed only in RUN_LOG. |

## Budgets (run 4 defaults)

- Stage 1: 3 dispatches × ≤ 25 searches
- Stage 2: 9 dispatches × ≤ 30 searches (standout hunter may use 40)
- Stage 4: ≤ 25 survivors × (adversary ≤ 15 searches + verifier ≤ 10 fetches)
- Stage 5: ≤ 15 dispatches × 0 searches
- Total ceiling ≈ 1000 tool calls. If exceeded, the run log must say where.
