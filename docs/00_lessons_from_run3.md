# Lessons from run 3

Run 3 was executed by a single model in one session on 2026-09-10. Inputs:
constraints.yml v1, the owner's brief. Outputs: `research-archive/run3/`.
Numbers: 15 searches, 41 one-liners screened, 14 survived, 4 PASS / 8 CONDITIONAL / 2 FAIL.

## What worked — keep

1. **Screen before elaborate.** 66 % killed at the one-liner stage for ~zero cost. F1 is fixed.
2. **Forcing functions produce the best candidates.** The two strongest passes (EUDR
   event-typing, Singapore source-basket early warning) came from reading regulation
   and policy news, not papers. Run 4 makes forcing functions a first-class output of
   the landscape stage.
3. **Company-first research.** Starting from "what would SatSure / Aonic / Space
   Intelligence want to see" produced hireable topics; starting from paper gaps
   produced side projects. Keep the landscape stage first.
4. **Open drone data with raw frames + metadata** (IMPaCT-UAV) unlocked pipeline-level
   drone candidates that don't collapse into "fine-tune a detector". Hunters should
   be told to prefer raw-frame datasets.
5. **Mark, never delete.** The FAIL entries (D02 spray verification, D13 SG aerial)
   are two degrees from passes; keeping them on the page is what makes that visible.

## What broke — fix

1. **Novelty was judged by the same model that generated the idea.** 8 of 14
   survivors carry `needs_novelty_check`. The adversarial search was done partially,
   late, and by the orchestrator. → Stage 4a: a separate adversary whose only goal
   is to kill the candidate, run BEFORE elaboration, with a mandatory query log.
2. **Data access was assumed.** IMPaCT's 414 GB, NICFI's licence, OneMap's tile
   terms, BD ORTHO's refresh cadence were all reasoned about from snippets, not
   fetched. D13 failed on data only at FULL stage, after elaboration. → Stage 4b:
   a verifier that fetches landing pages and quotes licence text.
3. **Orchestrator context was consumed by search results.** By stage 6 the model
   was holding ~40 search-result documents it no longer needed. → Subagents return
   JSON only; orchestrator never holds raw pages.
4. **Hunters invented restrictions.** The owner's explicit complaint: asked for
   "satellite", models narrowed to optical NDVI. In run 3 the first sketch of the
   candidate list was still optical-heavy until SAR/NICFI/AEF/aerial were forced in.
   → `buckets.yml` `global_hunter_rules[0]` says it in writing, and the hunter
   schema requires `data_class` per line so drift is visible in the output.
5. **Bucket 3 was undefined and Malaysia was ambiguous.** The run proceeded on an
   assumption. → `constraints.yml` `todo:` block; orchestrator refuses to start
   while open.
6. **research-archive-v1 was unavailable.** The skill's "check against v1" rule
   was silently skipped. → Stage 0 builds an archive index from every prior run
   in-repo; v1 and v2 outputs should be dropped into `research-archive/` before
   run 4 (see that folder's README).
7. **Region mix drifted toward India** because the two richest sources (EUDR,
   IMPaCT) are Indian. That is correct per C2, but EU candidates were all aerial +
   LPIS and all crowded. Not a bug, but the EU hunter should be told explicitly that
   the novelty bar is highest there and to look at hyperspectral (EnMAP/PRISMA) and
   AEF Custom Embeddings, which run 3 under-explored.

## Things run 3 did that run 4 must NOT repeat

- Writing the elaborated candidate before the novelty verdict existed.
- Quoting a dataset's size/licence from a search snippet.
- Letting the same model author the pitch and judge the pitch in one pass.
- Skipping the archive check "because the folder wasn't there".

## Cost note

Run 3 was ~15 searches. Run 4's ceiling is ~900 tool calls across subagents. That
is the price of having every C7 and C9 verdict evidenced instead of guessed. If
budget matters, cut the hunter fan-out (fewer regions per bucket), not the
verifiers.
