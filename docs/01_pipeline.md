# Pipeline stage contracts

Each stage lists: who runs it, inputs, outputs (file + schema), exit criterion,
and what the next stage may assume. If a stage's exit criterion is not met, the
orchestrator does not proceed; it re-dispatches or stops and asks.

Files live under `.research/` for the current run and are copied verbatim to
`research-archive/run<N>/` at the end.

| # | Stage | Runs on | Inputs | Outputs | Exit criterion |
|---|---|---|---|---|---|
| 0 | Preflight | orchestrator | constraints.yml, buckets.yml, research-archive/* | `RUN_LOG.md`, `archive_index.json` | no open TODO; no placeholder bucket |
| 1 | Landscape | 3 × landscape_scout (Sonnet) | market id, depth | `landscape/<market>.json`, `landscape/merged.json`, `landscape/SUMMARY.md` | ≥ 10 crowded entries; ≥ 5 dated forcing functions; every company has ≥ 1 URL ≤ 12 months old |
| 2 | Gap hunt | 7 × gap_hunter (Sonnet) | bucket block, constraints, merged landscape, archive index | `candidates.jsonl` | 40–80 unique one-liners; every line has region + data_class + delta_claim |
| 3 | SCREEN | orchestrator (skill) | candidates.jsonl, archive index | `gate_screen.yml` | 60–75 % killed; every kill has a gate + one-line reason |
| 4a | Novelty | 1 × novelty_adversary per survivor (Sonnet) | one-liner, delta_claim, seed_urls, crowded list | `novelty/<id>.json` | verdict ∈ {closed, type_a, type_b, unclear}; ≥ 3 queries logged; every prior-art item has URL+date |
| 4b | Data | 1 × data_verifier per survivor (Sonnet) | one-liner, data_class, region | `data/<id>.json` | every needed source has fetched URL + licence quote + access mode + ground-truth path |
| 5 | Elaborate | 1 × elaborator per cleared survivor (Sonnet, no tools) | one-liner + 4a + 4b + constraints + landscape slice | `elaborated/<id>.json` | all required fields; `what_would_kill_this` non-empty |
| 6 | FULL | orchestrator (skill) | elaborated/*, 4a, 4b | `gate_verdicts.yml` | every candidate has verdict; every CONDITIONAL has a written reframe |
| 7 | Roster | orchestrator | gate_verdicts.yml | `ROSTER.md`, archive copy | every PASS/CONDITIONAL present and ranked; owner report ≤ 300 words |

## Data flow rules

- **Downstream stages consume only upstream JSON**, never upstream prose. If the
  orchestrator wants to pass a landscape insight to a hunter, it passes the JSON
  entry, not its own paraphrase.
- **Ids are assigned once**, at stage 2 merge, as `R<run>-<bucket-letter><nn>`
  (e.g. `R4-S07`, `R4-D03`, `R4-G02`). All later files are keyed by this id.
- **Stage 4a and 4b run in parallel** and neither sees the other's output. This is
  deliberate: a data verifier that knows the novelty verdict starts rationalising.
- **Stage 5 has no tools.** If the elaborator needs something, it returns
  `needs: [...]` and the orchestrator routes back to 4a/4b. Elaboration is
  synthesis, not research.
- **The gate never re-derives C7 or C9.** It reads `novelty/<id>.json` and
  `data/<id>.json`. If those are missing, the candidate is `unassessed`, not
  `pass`.

## Parallelism

Stages 1, 2, 4, 5 are embarrassingly parallel. The orchestrator should dispatch
all subagents of a stage at once and wait. Sequential dispatch wastes wall-clock
and, worse, tempts the orchestrator to start judging partial results.

## Re-entry

A run can be resumed from any stage if the prior stage's files validate.
`RUN_LOG.md` records which stage is complete. To re-run only stage 4 for one
candidate (e.g. after the owner supplies a dataset link), delete
`novelty/<id>.json` and/or `data/<id>.json` and say `resume from stage 4`.

## Directory map (per run)

```
.research/
  RUN_LOG.md
  archive_index.json
  landscape/{india,singapore_malaysia,eu}.json
  landscape/merged.json
  landscape/SUMMARY.md
  candidates.jsonl
  gate_screen.yml
  novelty/<id>.json
  data/<id>.json
  elaborated/<id>.json
  gate_verdicts.yml
  ROSTER.md
```
