#!/usr/bin/env python3
"""Generate Lane B/C dispatch envelopes for remaining stage-4 candidates."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-18"
SKIP_ID = "R4-S20"
NO_DAT_IDS = {"R4-S47"}

SOURCE_FILES = [
    "RUNBOOK.md",
    "constraints.yml",
    "agents/data_verifier.json",
    "agents/novelty_adversary.json",
    "schemas/data_verification.schema.json",
    "schemas/novelty_verdict.schema.json",
    "schemas/_common.schema.json",
    ".research/candidates.jsonl",
    ".research/gate_screen.yml",
    ".research/landscape/merged.json",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_hashes() -> dict[str, str]:
    return {name: sha256(ROOT / name) for name in SOURCE_FILES}


def not_verified_ids() -> list[str]:
    """Replicate tools/whats_left.sh: ids in verify block with route:not_verified."""
    text = (ROOT / ".research/gate_screen.yml").read_text(encoding="utf-8")
    m = re.search(r"^verify:\n(?P<body>.*?)(?=^verify_summary:)", text, re.M | re.S)
    if not m:
        raise SystemExit("could not find verify block")
    ids: list[str] = []
    current: str | None = None
    for line in m.group("body").splitlines():
        id_match = re.match(r"^  (R4-S\d+):\s*$", line)
        if id_match:
            current = id_match.group(1)
            continue
        if current and re.match(r"^    route:\s+not_verified\s*$", line):
            if current != SKIP_ID:
                ids.append(current)
            current = None
    return ids


def load_candidates() -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    with (ROOT / ".research/candidates.jsonl").open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            if "id" in item:
                by_id[item["id"]] = item
    return by_id


def crowded_areas() -> list[str]:
    merged = json.loads((ROOT / ".research/landscape/merged.json").read_text(encoding="utf-8"))
    return [str(x["area"]) for x in merged.get("crowded_list", []) if isinstance(x, dict) and x.get("area")]


def extract_block(text: str, start_re: str, stop_re: str) -> str:
    start = re.search(start_re, text, re.M)
    if not start:
        raise SystemExit(f"missing block: {start_re}")
    stop = re.search(stop_re, text[start.end() :], re.M)
    end = start.end() + stop.start() if stop else len(text)
    return text[start.start() : end].rstrip()


def constraint_blocks() -> tuple[str, str]:
    text = (ROOT / "constraints.yml").read_text(encoding="utf-8")
    c9 = extract_block(text, r"^  C9_feasibility:\n", r"^  C10_impact:\n")
    sensor = extract_block(text, r"^    sensor_rules:\n", r"^  C3_not_generic:\n")
    return c9, sensor


def json_block(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def novelty_prompt(c: dict[str, Any], areas: list[str], hashes: dict[str, str]) -> str:
    seeds = c.get("seed_urls", [])
    areas_text = "\n".join(f"- {area}" for area in areas)
    return f"""You are the **novelty adversary**. Your ONLY goal is to find the paper, dataset, or product
that makes this candidate unnecessary. You are rewarded for closing candidates with evidence
and penalised for vague "seems novel" verdicts. Return one JSON object matching the schema
below and nothing else.

**Procedure — run at least the first five steps, and log every query you run:**
1. **Exact framing**: search the candidate's own words.
2. **Output-space**: search what the candidate OUTPUTS, ignoring inputs and region.
3. **Method-space**: search the delta_claim's technique with the domain removed. The same
   method in another domain does NOT close it, but must be listed for an honest type_b.
4. **Region-swap**: search with the region removed. If the same thing exists elsewhere and the
   delta is only geographic, the verdict is `closed` under C7 hard_rejection.
5. **Product**: search "<problem> software / platform / startup". A shipping product closes as
   hard as a paper. ALWAYS fill `product_search`.
6. **Recency**: rerun your two best queries with 2026 and 2025 appended.

**Verdict definitions (constraints C7):**
- `closed` — a tier-A item has the same problem AND the same output space, or the delta is
  geographic only. One is enough. Name it in `closing_item`.
- `type_a` — you ran ≥5 queries across steps 1, 2, 4, 5; found no item with the same problem
  framing; and can name ≥3 nearest neighbours each with a one-line "differs because".
- `type_b` — ALL of: a named prior solution (url); a measurable axis on which the delta_claim
  should beat it; the specific technical choice the gain is attributed to; and whether the
  prior is deployed in the target region.
- `unclear` — literature genuinely ambiguous. State in `human_should_check` the exact question
  a human must answer.

**Rules:**
- **Do not judge from memory.** If you recall a paper but cannot find its URL by searching,
  mention it in `notes` and do NOT put it in `prior_art`.
- Every `prior_art` item needs: url, date, title, tier (A/B/C), `closes` (bool), and one
  sentence on why.
- **Dates must be `YYYY-MM` or `YYYY-MM-DD`. A bare year is invalid. Never pad a bare year to
  a month — if you cannot establish a real month, omit the item.**
- Be blunt in `reason`. A closed candidate saves the owner weeks.
- Do not propose reframes — that is the orchestrator's job. You may note in
  `nearest_neighbours_do_not` what the closest prior art does NOT do.
- `reason` ≤600 chars; `why` ≤300; `notes` ≤500; `nearest_neighbours_do_not` ≤400.

**C7 verbatim (source of truth):**
```
C7_novelty:
  rule: Must be genuinely novel. Classify as TYPE_A or TYPE_B or FAIL.
  type_a_unexplored:
    requires: no prior work attempts this problem framing
    evidence_required: adversarial search found no closing paper
  type_b_significant_improvement:
    requires_all:
      - a named prior solution exists and is beaten on a MEASURABLE axis
      - the improvement is attributable to a specific technical choice
      - the solution is unavailable in the target region
    hard_rejection: >
      "Same method, new region" is an AUTO-FAIL even if the region is
      genuinely underserved. Regional transfer alone is NOT novelty.
      There must be a technical delta, not just a geographic one.
```

**The candidate:**
- id: `{c["id"]}`
- one_liner: {c.get("one_liner")}
- delta_claim: {c.get("delta_claim")}
- region: {c.get("region")}
- bucket: {c.get("bucket")}
- seed_urls: {json.dumps(seeds, ensure_ascii=False)}
- today: {TODAY}
- depth: normal

**Crowded areas already identified in this run's landscape (provisional):**
{areas_text}

**Return exactly one JSON object with this shape and nothing else:**
```json
{{
  "id": "string (required)",
  "verdict": "closed | type_a | type_b | unclear (required)",
  "reason": "string, max 600 chars (required)",
  "queries": [{{"q": "string", "useful": true, "note": "optional"}}],
  "prior_art": [{{"url":"", "date":"YYYY-MM-DD", "title":"", "tier":"A|B|C",
                 "closes": false, "why":"max 300 chars",
                 "relation":"same_problem|same_output_space|same_method_other_domain|same_thing_other_region|product"}}],
  "closing_item": null,
  "type_b_fields": null,
  "human_should_check": null,
  "nearest_neighbours_do_not": "max 400 chars",
  "budget_exhausted": false,
  "notes": "max 500 chars",
  "product_search": {{
    "queries_run": ["string"],
    "shipping_products_found": [{{"url":"", "date":"YYYY-MM", "title":"", "tier":"A|B|C", "note":""}}]
  }}
}}
```
`queries` needs at least 3 entries and must record **every** search you ran, including the
useless ones. `closing_item` is required when verdict is `closed`; `type_b_fields` (all four
keys) when `type_b`; `human_should_check` when `unclear`. `product_search` is always required.

Return only the JSON.

---
source_sha256:
{json_block(hashes)}
"""


def data_envelope(c: dict[str, Any], c9: str, sensor: str, hashes: dict[str, str]) -> dict[str, Any]:
    return {
        "role": "data_verifier",
        "source_sha256": hashes,
        "input": {
            "id": c["id"],
            "one_liner": c.get("one_liner"),
            "data_class": c.get("data_class"),
            "region": c.get("region"),
            "constraints_C9": c9,
            "constraints_C2_sensor_rules": sensor,
            "reverify": [],
            "today": TODAY,
        },
    }


def main() -> int:
    ids = not_verified_ids()
    candidates = load_candidates()
    missing = [cid for cid in ids if cid not in candidates]
    if missing:
        raise SystemExit(f"missing candidates: {', '.join(missing)}")

    areas = crowded_areas()
    c9, sensor = constraint_blocks()
    hashes = source_hashes()

    nov_dir = ROOT / ".research/dispatch/nov"
    dat_dir = ROOT / ".research/dispatch/dat"
    nov_dir.mkdir(parents=True, exist_ok=True)
    dat_dir.mkdir(parents=True, exist_ok=True)

    nov_count = dat_count = 0
    for cid in ids:
        c = candidates[cid]
        (nov_dir / f"{cid}.md").write_text(novelty_prompt(c, areas, hashes), encoding="utf-8")
        nov_count += 1
        if cid not in NO_DAT_IDS:
            env = data_envelope(c, c9, sensor, hashes)
            (dat_dir / f"{cid}.json").write_text(json.dumps(env, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            dat_count += 1

    print(f"wrote {nov_count} novelty prompts")
    print(f"wrote {dat_count} data envelopes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
