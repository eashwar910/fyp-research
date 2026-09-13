# Runbook — driving run 4 from Claude Code

Principle: the repo docs carry the detail, so each prompt only says **which
stage, which files to read, what to write, when to stop**. Never paste
constraints or agent prompts into chat; point at the files. One stage per
session; `/clear` between stages. Files are the state, not the conversation.

Subagent note: Claude Code runs subagents via the Task/Agent tool and picks up
project subagents from `.claude/agents/*.md`. Step 0b generates those from
`agents/*.json` so every dispatch inherits the right model, tools and prompt
without re-pasting.

---

## 0a — Setup (terminal)

```
tar xzf fyp-research-repo.tar.gz && cd fyp-research-repo
git init -q && git add -A && git commit -qm "run4: scaffold"
claude
```

## 0b — Generate project subagents (one-time)

```
Read agents/README.md and each agents/*.json. For each, create
.claude/agents/<role>.md with frontmatter name=<role>, model=sonnet,
tools per the json, and body = the json "system" string followed by
"Return only JSON valid against <output_schema>". Do not change wording.
List the files created, then stop.
```

Commit. `/clear`.

## 0c — Archive (you, not Claude)

T1 and T2 are already resolved in `constraints.yml` v2 (standout bucket;
Malaysia in C2). Drop run 1 & 2 rejects into `research-archive/`. Commit.

---

## Stage 0 — Preflight

```
Act as orchestrator per CLAUDE.md. Run Stage 0 of ORCHESTRATOR.md only.
Refuse if any constraints.yml todo is unresolved or a bucket is placeholder.
Write .research/RUN_LOG.md and .research/archive_index.json. Report counts. Stop.
```

`/clear`

## Stage 1 — Landscape

```
Stage 1 per ORCHESTRATOR.md. Dispatch the landscape_scout subagent 3x in
parallel (india, singapore_malaysia, eu), input per agents/landscape_scout.json.
Validate each against schemas/landscape_report.schema.json; re-dispatch once
on failure. Write landscape/<market>.json, merged.json, SUMMARY.md. Update
RUN_LOG. Report: crowded count, forcing-function count, any re-dispatch. Stop.
```

If you have a deep-research skill installed, append:
`Tell each scout to use the <skill-name> skill for its searches.`

`/clear`

## Stage 2 — Gap hunt

```
Stage 2 per ORCHESTRATOR.md. Dispatch gap_hunter per the buckets.yml matrix,
all in parallel, inputs per agents/gap_hunter.json (pass files verbatim, never
summarised). Validate against schemas/candidate_oneliner.schema.json. Merge,
assign R4- ids, dedupe, write .research/candidates.jsonl. Update RUN_LOG incl.
data_class distribution. Report: lines per hunter, after dedupe, any hunter
under 15 lines. Stop.
```

`/clear`

## Stage 3 — SCREEN (no subagents)

```
Stage 3 per ORCHESTRATOR.md. Run .claude/skills/fyp-constraint-gate SCREEN mode
on .research/candidates.jsonl using archive_index.json. Write gate_screen.yml.
If kill rate < 50% redo it stricter. Update RUN_LOG. Report: assessed/passed,
kills by gate, borderline ids. Stop.
```

`/clear`

## Stage 4 — Verify (the new stage)

```
Stage 4 per ORCHESTRATOR.md. For every screen_pass in gate_screen.yml dispatch
novelty_adversary AND data_verifier in parallel, inputs per their agents/*.json.
Neither sees the other's output. Validate against their schemas. Write
novelty/<id>.json and data/<id>.json. Apply the routing table (closed→FAIL C7,
blocked→FAIL C9, unclear→one deep re-dispatch). Spot-check 10% of URLs.
Update gate_screen.yml verify blocks and RUN_LOG. Report the verdict counts
and the routed-out ids with one line each. Stop.
```

If context gets heavy mid-stage: `/compact keep RUN_LOG state and the list of ids still pending; drop everything else.`

`/clear`

## Stage 5 — Elaborate

```
Stage 5 per ORCHESTRATOR.md. For each candidate that cleared Stage 4, dispatch
elaborator (no tools) with inputs per agents/elaborator.json. Validate against
schemas/elaborated_candidate.schema.json. If a result is {needs:[...]}, route
back to the named verifier once, then re-dispatch. Write elaborated/<id>.json.
Update RUN_LOG. Report ids elaborated and any needs. Stop.
```

`/clear`

## Stage 6 — FULL gate (no subagents)

```
Stage 6 per ORCHESTRATOR.md. Run fyp-constraint-gate FULL on elaborated/*.json.
C7 comes from novelty/<id>.json, C9 from data/<id>.json — do not re-judge.
Every CONDITIONAL gets a written reframe. Write gate_verdicts.yml with
region_mix. Update RUN_LOG. Report PASS/COND/FAIL counts only. Stop.
```

`/clear`

## Stage 7 — Roster + archive

```
Stage 7 per ORCHESTRATOR.md. Write .research/ROSTER.md (all PASS+CONDITIONAL,
ranked by the key in the playbook, one paragraph + pitch + 3 URLs each). Copy
.research/ to research-archive/run4/. Finish RUN_LOG incl. total tool calls.
Give me: counts, region mix, the 2-3 most interesting CONDITIONALs with
reframes. No single winner. Stop.
```

Commit `research-archive/run4/`.

---

## Resume / re-run one candidate

```
Resume from stage 4 for R4-S07 only: delete novelty/R4-S07.json, re-dispatch
novelty_adversary with depth=deep, then continue that id through stages 5-6.
Leave every other candidate untouched. Report the new verdict. Stop.
```

## One-shot (not recommended; use only after a clean staged run)

```
Run the full pipeline per ORCHESTRATOR.md, stages 0-7, /compact-ing between
stages and keeping only RUN_LOG state. Stop and ask me at any refusal
condition. Final report per Stage 7 only.
```

---

## Why the prompts are short

Each prompt is ~60 tokens because ORCHESTRATOR.md, the agent JSONs and the
schemas are the real instructions and Claude Code reads them from disk. Restating
them in chat costs tokens twice and drifts from the file. If you find yourself
adding a rule to a prompt, add it to the doc instead and re-run the stage.

## Cost guardrails

- Stages 1–2 and 4 are the spend; expect ~600–800 subagent tool calls total.
- To halve cost: cut the Stage 2 matrix to one region per bucket, never cut Stage 4.
- Sonnet for all subagents is set in `.claude/agents/*.md`; do not raise it. The
  orchestrator session is where a stronger model pays off (Stages 3, 6, 7).
