# research-archive/ — prior runs

One folder per run. The gate's "check against v1" rule reads every
`*/gate_verdicts.yml` here at stage 0 and builds `.research/archive_index.json`
(`{id, one_liner, verdict, failed_gate, reason, run}`). Hunters receive that
index as "do not restate"; the SCREEN gate inherits a prior verdict when a new
one-liner restates an archived one without addressing its failed gate.

## Present

- `run3/` — 2026-09-10, single-model run. 41 screened, 14 survived, 4 PASS /
  8 CONDITIONAL / 2 FAIL. `landscape.md` is the company/trend scan that fed it.
  See `docs/00_lessons_from_run3.md`.

## Missing — add before run 4

- `run1/` and `run2/` (the Claude Code deep-research runs the owner rejected).
  Drop their candidate lists here in ANY format; the orchestrator will convert
  them to the gate_verdicts format at stage 0 (verdict=fail, reason="rejected by
  owner in run N" unless a reason is recorded). Without them, the archive check
  cannot stop run 4 from re-proposing what the owner already disliked.

## Ids

Run-scoped: `R<run>-<letter><nn>`. Run 3 used `S01/D01/G01` without a prefix;
the stage-0 indexer prefixes them as `R3-S01` etc. Do not rename files.
