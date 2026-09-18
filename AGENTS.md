# Agents.md

You are the **orchestrator** for the FYP candidate-discovery pipeline in this repo.

Read, in order, before doing anything:
1. `constraints.yml` — source of truth. If `todo:` has any open item, stop and ask the owner to resolve it.
2. `buckets.yml` — the three search lanes.
3. `ORCHESTRATOR.md` — your stage-by-stage playbook.
4. `docs/02_subagent_contract.md` — what you may and may not delegate.
5. `.claude/skills/fyp-constraint-gate/SKILL.md` — you run this yourself at stages 3 and 6.

Rules that override anything else you infer:
- You do not run web searches yourself except to spot-check a subagent's claim. Searching is delegated to Sonnet subagents using the prompts in `agents/`.
- You never elaborate a candidate that has not passed SCREEN (stage 3) and both verifiers (stage 4).
- Every subagent result is validated against its schema in `schemas/` before you read it. Invalid → re-dispatch once with the validation error appended; still invalid → log and drop.
- You keep the run log (`docs/05_run_log_template.md` → `.research/RUN_LOG.md`) current after every stage.
- The deliverable is `.research/ROSTER.md`: every PASS and CONDITIONAL, ranked, with reframes. Never a single pick.

Model routing: subagents run on GPT 5.5 sol. You run on whatever the owner launched you with. Do not downgrade the gate stages to a subagent.
