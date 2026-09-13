# agents/

One JSON file per subagent role. Each file is the complete dispatch spec:
`system` (the prompt), `input` (what the orchestrator fills in), `tools`,
`budget`, and `output_schema` (validated before the orchestrator reads it).

| File | Stage | Fan-out (run 4) | Tools | Returns |
|---|---|---|---|---|
| landscape_scout.json | 1 | 3 (india, singapore_malaysia, eu) | search, fetch | landscape_report |
| gap_hunter.json | 2 | 7 (bucket × region) | search, fetch | candidate_oneliner[] |
| novelty_adversary.json | 4a | 1 per screen_pass | search, fetch | novelty_verdict |
| data_verifier.json | 4b | 1 per screen_pass | search, fetch | data_verification |
| elaborator.json | 5 | 1 per cleared survivor | none | elaborated_candidate |

The gate (stages 3 and 6) is NOT an agent. The orchestrator runs
`.claude/skills/fyp-constraint-gate/SKILL.md` itself. Delegating judgement to
the same tier that generated the ideas is how run 3 ended up with
`needs_novelty_check` everywhere.

## Dispatching from Claude Code

The orchestrator uses the Task tool (subagent) with:
- `model`: the `model` field in the JSON (`sonnet`)
- prompt: the `system` string, followed by a line `INPUT:` and the filled
  `input` object as JSON
- it then validates the returned text against `output_schema` (treat any
  non-JSON or schema failure as a re-dispatch per ORCHESTRATOR.md failure table)

Inputs marked `<verbatim ...>` are pasted in full. Inputs marked `<.research/...>`
are the file contents. Never summarise inputs before passing them.

## Editing a prompt

- Keep `system` self-contained; a subagent does not see this repo's other docs.
  The contract in `docs/02_subagent_contract.md` is restated inside each prompt
  for that reason.
- If you add a field to an output, add it to the schema first, then the prompt.
- Bump nothing; the run log records the sha of `agents/` at stage 0.
