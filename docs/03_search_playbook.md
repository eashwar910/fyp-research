# Search playbook

For landscape scouts, gap hunters, and the novelty adversary. The data verifier
mostly fetches, not searches, but §4 applies to it.

## 1. Query construction

- 2–6 words. Start broad, then narrow. Never repeat a near-identical query.
- Include the year only for time-sensitive things (deadlines, releases, job posts).
- One concept per query. "EUDR coffee shade satellite India" is four concepts;
  run "EUDR shade coffee misclassification", then "coffee agroforestry India
  satellite mapping", then "Coorg coffee canopy change detection".
- For papers: use the phrasing a title would use, not a question.
  ✗ "is there work on detecting mowing from SAR coherence"
  ✓ "mowing detection Sentinel-1 coherence"
- For datasets: name + "dataset" + one distinguishing word; then fetch the
  landing page, never rely on the snippet.
- For companies: "<company> product" then "<company> careers" / "<company>
  jobs" then "<company> 2026" for news.
- For regulations: the regulation's short name + "deadline" / "guidance" /
  "delegated act" + year.

## 2. Source tiers

| Tier | Examples | Use for |
|---|---|---|
| A — primary | arXiv/journal page, dataset landing page (Zenodo, IEEE DataPort, source.coop, HF), EUR-Lex, gov.sg / gov.in / europa.eu, company product or careers page | any factual claim |
| B — curated secondary | Tracxn, Glassdoor job listings, JRC technical reports, ESA/NASA/ISRO pages, Papers-with-Code | company/hiring facts, pointers to tier A |
| C — commentary | Medium, vendor blogs, news aggregators, LinkedIn posts | trend colour only, `supporting` field only |
| X — do not use | content farms, SEO listicles without dates, AI-generated summaries of papers | never |

If the only evidence for a claim is tier C, mark `confidence: low` and move on.

## 3. Gap-hunting heuristics (stage 2)

Where gaps actually came from in run 3, in order of yield:

1. **A regulation or subsidy with a date and a verification need.** (EUDR,
   vine grubbing scheme, CRM incentives, GAEC 8.) Query: `<scheme> verification
   satellite` / `<scheme> monitoring remote sensing`. If nothing comes back,
   that's a gap.
2. **A dataset or product's own stated weakness.** (FTW confidence "conservative
   in smallholder systems"; AEF "annual only"; IMPaCT "raw frames, no
   analytics".) Read the limitations section / README. Query: `<product> limitations`.
3. **A company complaint quoted in press.** (JDE Peet's on shade-coffee
   misclassification; SFA on early-warning lead time.) Query: `<company> challenge
   satellite 2026`.
4. **A pipeline step everyone does the slow way.** (Orthomosaicking before
   detection; panel-based radiometric calibration.) Query: `<step> alternative` /
   `without <step>`.
5. **Two mature fields that haven't met.** (Foundation-model embeddings ×
   insurance loss; open aerial orthophotos × CAP conditionality.) Query each
   half, then the intersection.

Low-yield in run 3 (don't spend budget): "novel architecture for X", "X in
region Y", "X using deep learning".

## 4. Adversarial novelty search (stage 4a)

Goal: find the paper or product that makes the candidate unnecessary. You are
trying to close it. Minimum 3 queries, typically 6–10.

Procedure:
1. **Exact framing.** Query the candidate's own words. If the first page of
   results contains a paper with the same problem AND same output space →
   likely `closed`. Fetch it; confirm; record.
2. **Output-space search.** Query the *output* the candidate produces
   ("event typing canopy loss", "residue fate classification", "boundary
   confidence calibration"). Different inputs, same output = prior art.
3. **Method-space search.** Query the *technical delta* alone, without the
   domain ("multi-view consensus detection uav", "self-supervised radiometric
   normalization"). Same method in a different domain does NOT close, but must
   be listed so the type_b comparison is honest.
4. **Region-swap search.** Query the candidate with the region removed. If the
   same thing exists elsewhere and the delta_claim is only geographic →
   `closed` under C7 hard_rejection.
5. **Product search.** Query `<problem> software` / `<problem> platform` /
   `<problem> startup`. A shipping commercial product closes a candidate as
   hard as a paper does (constraints: vertical-farming warning generalises).
6. **Recency sweep.** Add `2026` and `2025` to the two best queries. arXiv
   moves fast; run 3 found a June-2026 paper that closed a drone BRDF idea.

Verdict rules:
- `closed`: a tier-A item does the same problem with the same output space,
  OR the delta is geographic only. Cite it. One is enough.
- `type_a`: ≥ 5 queries, no item with the same problem framing; nearest
  neighbours listed with why they differ.
- `type_b`: a named prior solution exists; the candidate's delta_claim names a
  measurable axis on which it should beat it; the improvement is attributable
  to a specific technical choice; the prior solution is not deployed in the
  target region. All four required or it's `unclear`.
- `unclear`: you ran out of budget or the literature is ambiguous. Say what a
  human should check.

## 5. Data verification (stage 4b)

For every source the candidate names or implies:
1. Search `<dataset name> dataset` → open the landing page (tier A) → fetch it.
2. Quote: licence, size, format, coverage, date range, access mode.
3. Ground truth: does the dataset ship labels? If not, name the label source
   the candidate would use (LPIS, Coffee Board registry, scheme plot list,
   visual interpretation protocol) and fetch THAT page too.
4. NICFI: if used, quote the NICFI purpose clause and state in one sentence
   whether the candidate's framing is inside it.
5. Compute path: which free platform hosts it (GEE catalog id, Planetary
   Computer collection, Kaggle dataset) or is it a download (state GB).
6. Singapore imagery: if the candidate images SG farmland, confirm the source
   is drone/aerial/sub-metre AND its terms allow analytical use. OneMap /
   SLA basemap tiles are display-licensed unless you find text saying otherwise.

If a landing page cannot be fetched, the source is `unverified`, not `open`.
