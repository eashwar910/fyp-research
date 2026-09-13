# fyp-research — FYP candidate discovery, run 4

A docs-only repo that specifies how to run one full cycle of "find genuinely novel,
feasible FYP topics in AI-for-agriculture from satellite/drone imagery" using a
single orchestrator model and a fleet of Sonnet subagents that do the actual
searching, reading and verifying.

There is no code here on purpose. Everything the orchestrator needs is a doc, a
JSON prompt, or a JSON schema. The orchestrator reads `ORCHESTRATOR.md` and drives.

## Why subagents

Run 3 was done by one model doing everything: ~15 web searches, 41 one-liners,
gate, elaboration. It worked, but 8 of the 14 survivors left the pipeline marked
`needs_novelty_check`, and dataset access was assumed rather than fetched. The
orchestrator's context was spent on searching instead of judging. Run 4 splits
the work: the orchestrator only *judges and routes*; Sonnet subagents *search,
fetch, and return structured JSON*.

## The pipeline in one screen

```
 constraints.yml + buckets.yml
          │
   ┌──────▼──────┐
   │ 0 preflight │  orchestrator: refuse to start if constraints.todo is non-empty
   └──────┬──────┘
   ┌──────▼──────┐
   │ 1 landscape │  landscape_scout ×3 (one per job market: IN / SG+MY / EU)
   └──────┬──────┘  → .research/landscape/*.json
   ┌──────▼──────┐
   │ 2 gap hunt  │  gap_hunter ×9 (bucket × region; standout ×1 global), fed the landscape + crowded list
   └──────┬──────┘  → .research/candidates.jsonl   (40–80 one-liners)
   ┌──────▼──────┐
   │ 3 SCREEN    │  orchestrator runs fyp-constraint-gate SCREEN. Expect 60–75 % killed.
   └──────┬──────┘  → .research/gate_screen.yml
   ┌──────▼──────┐
   │ 4 verify    │  per survivor, IN PARALLEL: novelty_adversary + data_verifier
   └──────┬──────┘  → .research/novelty/*.json  .research/data/*.json
   ┌──────▼──────┐
   │ 5 elaborate │  elaborator, only for survivors that cleared step 4
   └──────┬──────┘  → .research/elaborated/*.json
   ┌──────▼──────┐
   │ 6 FULL gate │  orchestrator runs fyp-constraint-gate FULL
   └──────┬──────┘  → .research/gate_verdicts.yml
   ┌──────▼──────┐
   │ 7 roster    │  ranked PASS + CONDITIONAL; archive the run
   └─────────────┘  → .research/ROSTER.md ; research-archive/run4/
```

The two arrows that did not exist in run 3 are step 4's parallel verifiers. They
are the whole point of run 4.

## Layout

```
README.md                    this file
CLAUDE.md                    entry point for Claude Code (points at ORCHESTRATOR.md)
ORCHESTRATOR.md              the orchestrator's playbook, stage by stage, with dispatch order
constraints.yml              source of truth (hard/soft gates, exclusions, TODOs)
buckets.yml                  the three search buckets and what each hunter is told
docs/
  00_lessons_from_run3.md    what worked, what broke, what run 4 changes
  01_pipeline.md             stage contracts: inputs, outputs, exit criteria
  02_subagent_contract.md    rules every subagent obeys
  03_search_playbook.md      query construction, source tiers, adversarial search
  04_evidence_standards.md   what counts as proof for novelty / data / user
  05_run_log_template.md     what the orchestrator writes as it goes
  06_runbook_claude_code.md  the exact per-stage prompts to type into Claude Code
agents/                      one JSON prompt per subagent role (system prompt + I/O + budget)
schemas/                     JSON schemas every subagent output is validated against
.research/                   per-run working files (gitignored except README)
research-archive/            prior runs; the gate checks new candidates against these
.claude/skills/              the fyp-constraint-gate skill (unchanged from run 3)
```

## Starting a run

1. `constraints.yml` v2: T1 and T2 are resolved (standout bucket; Malaysia in C2). Re-open a TODO if you change either.
2. Check `buckets.yml` — bucket 3 is the `standout` lane (no region/sensor constraint, hard C11).
3. Open the repo in Claude Code and say: `run the fyp pipeline per ORCHESTRATOR.md`.
4. Read `.research/ROSTER.md` when it finishes. Do not ask it for a single winner.

## Non-negotiables

- Subagents never elaborate. One-liners in, one-liners out, until step 5.
- Nobody judges novelty from memory. A novelty verdict without ≥3 documented searches and URLs is invalid.
- Nobody assumes a dataset exists. A data verdict without a fetched landing page + licence text is invalid.
- No hunter adds restrictions that are not in `constraints.yml` (run 3 complaint: models kept inventing extra satellite rules).
- Region mix is reported, never engineered.
