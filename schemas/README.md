# schemas/

JSON Schema (draft 2020-12) for every subagent output. The orchestrator
validates each result against its schema BEFORE reading it. Invalid → one
re-dispatch with the validator message appended; still invalid → drop and log.

| Schema | Produced by | Consumed by |
|---|---|---|
| _common.schema.json | — | all (shared $defs: url_evidence, region, bucket, query_log) |
| landscape_report.schema.json | landscape_scout | orchestrator merge → gap_hunter, elaborator |
| candidate_oneliner.schema.json | gap_hunter | SCREEN gate |
| novelty_verdict.schema.json | novelty_adversary | FULL gate, elaborator |
| data_verification.schema.json | data_verifier | FULL gate, elaborator |
| elaborated_candidate.schema.json | elaborator | FULL gate |
| gate_verdicts.schema.json | orchestrator (gate) | roster; next run's archive index |

Design choices worth knowing:
- `url_evidence` requires a `date`. Undated claims fail validation on purpose.
- `query_log` is required on every searching role. A verdict with no queries is invalid — this is the mechanical enforcement of "never judge novelty from memory".
- `novelty_verdict.type_b_fields` has all four C7 type_b requirements as required properties. You cannot claim type_b without naming the prior, the metric, the attribution, and regional availability.
- `data_verification.sources[].fetched_ok` is required. `open` with `fetched_ok=false` is contradictory and the orchestrator treats it as `unverified`.
- `elaborated_candidate` is a `oneOf`: either a full elaboration or `{needs: [...]}`. No half-elaborations.
- `gate_verdicts` mirrors the skill's YAML format; it is written as YAML on disk and validated as JSON.

Validation is not automated in this docs-only repo. The orchestrator is
expected to validate by reading the schema and checking the object; if a
validator tool is later added, point it at these files unchanged.
