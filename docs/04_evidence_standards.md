# Evidence standards

What a verdict must contain to be accepted by the orchestrator. If a field
below is missing, the verdict is `unassessed`, never `pass`.

## C7 — novelty

| Verdict | Required evidence |
|---|---|
| closed | One tier-A item (URL, date, title) + one sentence stating the matching problem AND matching output space, or the geographic-only delta. |
| type_a | ≥ 5 logged queries covering §4 steps 1, 2, 4, 5 of the search playbook; ≥ 3 nearest-neighbour items each with a one-line "differs because". |
| type_b | Named prior solution (URL); measurable axis (metric + why it's the right metric); the specific technical choice the gain is attributed to; evidence the prior is not deployed in the target region (or an honest "unknown"). |
| unclear | The logged queries + the specific question a human should resolve. |

"I'm not aware of prior work" is not evidence. A query log is.

## C9 — data feasibility

Per data source:
- `url` of the landing page, fetched (not a search snippet).
- `licence_quote` ≤ 25 words verbatim; `licence_class ∈ {open, non_commercial, academic_program, registration, paid, unknown}`.
- `access_mode ∈ {gee_catalog, planetary_computer, direct_download, api, application_required, unverified}` and, for downloads, `size_gb`.
- `covers_target_region: true/false/partial` with the coverage statement quoted.
- `ground_truth ∈ {shipped, external_named, must_construct, none}`; if `external_named`, the label source's URL; if `must_construct`, a ≤ 40-word protocol (who labels what from what).
- `nicfi_purpose_check` (only if NICFI): `inside | outside | borderline` + the framing sentence.
- `compute_path`: one of the free tiers in constraints C9 plus a one-line reason it suffices (server-side, tabular, small CNN, etc.).

Aggregate verdict: `open` (all sources open/academic and ground truth exists or is constructible) / `conditional` (one source needs an application or partner, name it) / `blocked` (no access or no ground-truth path).

## C10 — impact

- `user`: a role at a named type of organisation ("EUDR compliance lead at an Indian coffee exporter", "Punjab Dept of Agriculture CRM cell"). "Farmers" alone is too broad; "researchers" is invalid.
- `decision_changed`: the binary or scalar decision the output moves ("hold shipment vs release", "pay incentive vs withhold", "diversify sourcing this week vs not").
- `evidence`: one URL showing that user actually faces that decision (regulation text, scheme guidelines, press quote).

## C8 — scope floor

Elaborator must fill all five criteria as `true/false` with one line each. The gate counts them; ≥ 3 passes. The gate may downgrade a `true` if the line is vacuous ("it has two components: a model and a script").

## C3 — not generic

Screen-stage pattern match against `constraints.yml auto_fail_patterns`. Evidence is the matched pattern id. No search needed.

## C1 — imagery-native

Screen-stage judgement with one sentence: what is the primary signal and what would be lost if imagery were removed. If the answer is "a nice map", fail.

## Landscape claims

- Company "actively building X": product page or press release ≤ 12 months.
- Company "hiring for X": job post URL ≤ 6 months, or a careers page snapshot.
- Forcing function: primary text (regulation, scheme guideline, dataset release note) with the date that matters.
- Crowded area: ≥ 5 papers in 24 months (list 5 URLs) or ≥ 2 shipping products (list 2 URLs).

## Dates

Every URL carries a `date` (YYYY-MM or YYYY-MM-DD). Undated tier-C sources are dropped. The orchestrator spot-checks 10 % of URLs per stage; a 404 triggers re-verification of that verdict.
