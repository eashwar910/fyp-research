Repo: FYP candidate-discovery pipeline, branch `v3`. You are **Lane C, Phase 0**.
Read `RUNBOOK.md` §5 before starting. Build two tools, **Python stdlib only —
do NOT pip install anything; pyyaml is not available in this environment.**

## 1. `tools/check4.py`
Usage: `python3 tools/check4.py <role>:<id>` where role is `nov` or `dat`.
- `nov` → validate `.research/novelty/<id>.json` against `schemas/novelty_verdict.schema.json`
- `dat` → validate `.research/data/<id>.json` against `schemas/data_verification.schema.json`
- Resolve `$ref` into `schemas/_common.schema.json`.
- On pass print exactly `ok` and nothing else; else print numbered violations, exit 1.

Beyond plain schema checking, it MUST enforce:
- Every date matches `^\d{4}-\d{2}(-\d{2})?$`. **A bare year is invalid and must never be
  padded to a month.** This defect broke 2 stage-2 hunters and 6 stage-4 outputs.
- `queries`: min 3 items (nov), each with `q` and `useful`.
- maxLength: `reason` 600, `why` 300, `notes` 500, `nearest_neighbours_do_not` 400.
- Conditionals: `closing_item` required when `verdict=closed`; all four `type_b_fields` when
  `type_b`; `human_should_check` when `unclear`; `product_search` always present.

**Acceptance test — must pass before you go further.** These three must each print `ok`:
`nov:R4-S23`, `nov:R4-S01`, `dat:R4-S13`.
They are known-good outputs from the last run. If one fails, YOUR VALIDATOR IS WRONG — fix
the validator. Do not edit the data files.

## 2. `tools/gen_envelopes.py`
Derive the working id list exactly as `tools/whats_left.sh` does (the `not_verified` ids in
`.research/gate_screen.yml`, excluding `R4-S20`). For each id emit:

- `.research/dispatch/nov/<id>.md` — paste-ready prompt using the template in `RUNBOOK.md`
  §6.2.1 verbatim, filling `{{...}}` from `.research/candidates.jsonl` (`one_liner`,
  `delta_claim`, `region`, `bucket`, `seed_urls`) and `{{crowded_list_areas}}` from
  `.research/landscape/merged.json` → `crowded_list[].area`.
- `.research/dispatch/dat/<id>.json` — machine envelope matching the `input` block of
  `agents/data_verifier.json`, with the `C9_feasibility` and `C2_region.sensor_rules` blocks
  copied **verbatim** from `constraints.yml`.

Exceptions: `R4-S47` needs the `nov` file only (its data output already exists — do not emit a
`dat` envelope for it). `R4-S50` needs both. Pin the SHA-256 of every source file into each
envelope, as the previous run did.

## 3. Verify
Run `tools/whats_left.sh`. Expect **42 nov outstanding, 41 dat outstanding, 3 deep**. Confirm
your generated file counts match (42 nov prompts, 41 dat envelopes).

## 4. Shared-dependency pre-check (needs web access)
If you have no web access, stop after step 3 and say so. Otherwise do `RUNBOOK.md` §3.1,
**MOPAD first**: fetch each dataset family's landing page, quote licence / size / coverage /
date range verbatim (≤25 words each), and write `.research/data/_shared/<family>.json`.
A search snippet is not verification — you must fetch the page.

## Boundaries
Write only to `tools/`, `.research/dispatch/`, `.research/data/_shared/`,
`.research/ledger/lanec.jsonl`. **Never** edit `gate_screen.yml`, `RUN_LOG.md`,
`candidates.jsonl` or `ROSTER.md` — another agent owns those and concurrent edits corrupt the
run. Commit with `git add` on your own paths only.
