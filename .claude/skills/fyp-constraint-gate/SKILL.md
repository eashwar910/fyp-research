---
name: fyp-constraint-gate
description: >
  Filters candidate final-year-project topics against the owner's hard
  constraints in constraints.yml and emits a pass/conditional/fail verdict with
  a reason for each. Use this WHENEVER project ideas, research gaps, thesis
  topics, or candidate directions are being generated, discussed, compared,
  shortlisted, or elaborated — including when the user just says "here are some
  ideas", pastes a gaps.yml, or asks "is this a good project?". Run it in
  SCREEN mode on raw one-line candidates BEFORE any elaboration happens, and in
  FULL mode on survivors afterwards. Do not elaborate, research, or write up any
  candidate that has not been through this gate first.
---

# FYP Constraint Gate

Kills weak candidates cheaply, before anyone spends tokens elaborating them.

**Why this exists**: in a prior run, 20 candidates were fully elaborated and 17
were then discarded. The constraints existed but were applied too late. This
skill moves them to the front.

## First: read the constraints

Always read `constraints.yml` from the project root before judging anything.
Never judge from memory or from this file's summary — `constraints.yml` is the
source of truth and it changes.

If `constraints.yml` is missing, stop and say so. Do not improvise constraints.

## Two modes

### SCREEN — cheap, on one-liners

Input: a list of candidate one-liners (typically 20–40, from `gap-to-topic` or
a brainstorm). Each is a sentence or two. No elaboration yet.

Check ONLY the four cheapest hard gates, in this order, stopping at first fail:

1. **C3 auto-fail patterns** — pattern-match against the banned list. Fastest kill.
2. **C1 imagery-native** — is imagery the primary signal, or decoration?
   **Skip this check entirely for Singapore candidates** — they are exempt.
3. **Excluded domains** — aquaculture always. Indoor and vertical farming only
   for EU and India; both are permitted for Singapore.
4. **C7 regional-transfer sniff test** — does the novelty reduce to "existing
   method, new place"? If the one-liner's only distinguishing feature is the
   region, fail it here.

Do NOT attempt scope floor, feasibility, or licence checks in SCREEN mode —
they need detail the one-liner doesn't have. Mark them `unassessed`.

Output: the list, each marked `screen_pass` / `screen_fail` + one-line reason.
Expect to kill 60–75%. If fewer than half fail, you are being too generous —
re-read the C3 auto-fail patterns and try again.

### FULL — on survivors only

Input: elaborated candidates (a paragraph or more each, with a named data
source and a named prior-art comparison).

Evaluate every hard gate: C1, C2 (incl. sensor rules), C3, C7, C8 scope floor,
C9 feasibility (incl. NICFI licence check), C10 impact. Then score the soft
criteria C4, C5, C6.

## Verdicts

- **PASS** — every hard gate clears. Goes on the roster.
- **CONDITIONAL** — one hard gate fails, but a specific, stated reframe would
  fix it. You must write the reframe. "Could be adjusted" is not a reframe.
- **FAIL** — a hard gate fails with no reframe available.

## Rules that are easy to get wrong

**Mark, never delete.** Every candidate stays in the output with its verdict and
reason, including fails. A gap that fails on data access is often two degrees
from one that passes, and that is only visible if it is still on the page.

**There is no region quota.** Report the region mix as an observation only.
Never invent, pad, promote, or demote a candidate to balance regions, and never
fail a strong candidate because its region already has several. Uneven output is
the correct output.

**Implementation difficulty is not a fail reason.** The owner is a strong AI
engineer using AI-assisted coding. Fail on *compute* (no CUDA, no sustained GPU
training) and on *data access* — never on "this is a lot of code to write".

**Regional transfer is an auto-fail, not a soft mark.** "Method X has not been
applied to Indian smallholders" is not novelty under C7. There must be a
technical delta. If the only delta is geography, fail it — even if the region
is genuinely underserved and the impact would be real.

**Do not judge novelty from memory.** If C7 cannot be assessed without knowing
the prior art, mark it `needs_novelty_check` and route to the stage-6
adversarial search. Never guess that something is novel.

**Check against v1.** `research-archive-v1/` holds previously rejected
candidates. If a new candidate restates one of them, say so and cite it.

## Output format

Write to `.research/gate_verdicts.yml`:

```yaml
mode: screen | full
assessed: <n>
passed: <n>
candidates:
  - id: C07
    one_liner: "..."
    verdict: pass | conditional | fail
    region: eu | india | singapore
    failed_gate: C7_novelty        # omit if pass
    reason: "Delta is geographic only — SAR flood mapping already published for the Mekong."
    reframe: "..."                 # required if conditional
    scope_floor_met: 3             # full mode only
    novelty_type: type_a | type_b | needs_novelty_check
    data_source: "Sentinel-1 GRD via Copernicus"
    pitch: "..."                   # full mode only
region_mix:          # observation only — not a target
  eu: 4
  india: 3
  singapore: 1
notes: "..."
```

## After running

Report only: how many assessed, how many passed, the region mix as a plain
observation, and the two or three most interesting CONDITIONALs with their
reframes. Do not narrate every fail — the file has them.
