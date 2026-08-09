# FYP — AI for agriculture from satellite/drone imagery

Finding and validating a final-year-project topic. Not building it yet.

## The goal

A **roster** of strong candidate topics — not one pick. Every candidate that
passes the gate stays on the roster, ranked.

## Non-negotiables (full spec in `constraints.yml` — read it before judging any candidate)

1. Imagery-native — satellite or drone as the primary signal. **EU and India
   only. Singapore candidates are exempt** and may be any genuinely novel AI
   solution for the Singapore agricultural landscape.
2. Region: EU / India / Singapore. Want some candidates from each. **No quota,
   no target numbers** — never balance or pad, never reject a strong candidate
   because its region is already represented.
3. No dashboards, no chatbots, no generic agri-AI.
4. Genuinely novel: unexplored direction, or a measurable technical improvement
   over a named prior solution. **Same method in a new region is an auto-fail.**
5. Scope floor: must clear 3 of 5 FYP-vs-side-project criteria.
6. Feasible: 8 months part-time, MacBook without CUDA, RM200, free hosted compute.

Excluded: aquaculture, indoor farming, vertical farming.

## Hard facts that constrain candidates

- **Singapore**: agricultural land is <1% of the country (<10 km²). Average
  vegetable farm ~2 ha — Sentinel-2 at 10 m cannot resolve it. This is why the
  imagery requirement is lifted here. If a Singapore candidate *is* imagery-
  based it needs drone / sub-metre from an **existing** source (self-collected
  flights are out of scope); otherwise imagery is simply not required. Live
  local hooks: Lim Chu Kang 390 ha master plan and its plot re-parcelling, the
  farm-biodiversity buffer against Sungei Buloh and Kranji Marshes, and 90%
  food-import dependence.
- **NICFI** (Planet, 4.77 m, via Earth Engine) covers tropical Asia, not the EU,
  and is licence-bound to reducing tropical forest loss. India/SEA candidates
  using it must frame around forest-edge agriculture or deforestation-free
  commodities.
- **No CUDA.** Anything needing sustained local GPU training is infeasible.
  Google Earth Engine, Copernicus Data Space, Planetary Computer, and Kaggle's
  free GPU hours are the compute budget.
- **Cloud cover**: SEA and much of India are cloud-obscured most of the year.
  Optical-imagery methods that dominate EU/US literature quietly fail there.
  SAR (Sentinel-1) is often the honest answer. This asymmetry is a real source
  of novelty, not a workaround.

## Working style

- Owner is a strong AI engineer using AI-assisted coding. **Implementation
  difficulty is not a limiting factor** — never down-scope a candidate because
  it looks like a lot of code.
- Reading is the scarce resource, not coding. Prefer candidates whose novelty
  can be verified from a small number of papers.
- Prefer systems / dataset / benchmark contributions over novel architectures.
  Dev-heavy and publishable at the same time.

## Pipeline

Artifacts live in `.research/`. Each stage reads the previous stage's file, not
the previous conversation.

| Stage | Skill | Output |
|---|---|---|
| 0 | Deep Research (`/research`, trim outline to ~5, then `/research-deep`) | landscape |
| 1 | `research-hub` + CLI | corpus in vault |
| 2 | `literature-triage-matrix` | screen ~200 → ~50 |
| 3 | `paper-summarize` | per-paper notes |
| 4 | `gap-to-topic` | candidate one-liners |
| 5 | **`fyp-constraint-gate` (SCREEN)** | kill weak candidates BEFORE elaboration |
| 6 | targeted search per survivor | novelty kill-attempt |
| 7 | `gap-to-topic` (full) + **`fyp-constraint-gate` (FULL)** | ranked roster |
| 8 | `research-design-helper` | design brief for the chosen one |

**Stage 5 exists because of the v1 failure**: 17 of 20 candidates were
elaborated and then discarded. Never elaborate a candidate that hasn't been
screened.

## Accounts

Two Claude Code profiles share this repo. `cc-p` runs bulk stages (1–3),
`cc-w` runs judgment stages (4–8). Handoff is via files in `.research/`.

## Prior run

`research-archive-v1/` is the previous Deep Research run. Do not delete or
overwrite it. Its rejected candidates are useful negative examples — when
generating new candidates, check them against v1 to avoid regenerating ideas
already dismissed.
