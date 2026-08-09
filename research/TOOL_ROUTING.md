# TOOL ROUTING — FYP Ideation 2026

Verified by live probe on 2026-08-04. Every tool listed below was enumerated from its
real MCP schema; liveness/auth claims come from actual calls, not assumption.

**Read `research/RESEARCH_BRIEF.md` first. Always.**

---

## 0. Server roles

| Server | Job | Auth | State |
|---|---|---|---|
| `arxiv` | Preprint discovery, bleeding-edge method sweeps, 2024–2026 recency, full-text/LaTeX deep reads | None (anonymous arXiv API) | Local paper store — **empty** (0 papers) |
| `papers` | Peer-reviewed literature, venue + impact signals, systematic-review breadth across 21 backends | None configured; several backends dead without keys | Stateless |
| `zotero` | MY library. Check-before-fetch, then write shortlist back | `ZOTERO_API_KEY` set, cloud user `21185707` (`eashwarsid`), **read+write** | Library — **empty** (0 items, 0 collections, 0 groups) |

### Three findings that change the plan

1. **`papers` has no citation-graph tool.** All 42 of its tools are search / download /
   read. Forward and backward citation chasing — assigned to `papers` in the original
   brief — must be routed to **`zotero_scholar`** (OpenAlex, DOI-keyed, and it flags
   `inLibrary` so gaps are visible). `papers` keeps peer-reviewed discovery, venue
   signals, and OA full-text retrieval.
2. **`arxiv__citation_graph` is rate-limited right now.** Two consecutive calls both
   returned HTTP 429 from Semantic Scholar (no API key configured). Treat it as a
   fallback only, never the primary citation route.
3. **The Zotero library is empty.** "Check what I already have before fetching" is
   currently a no-op that will always return zero. Still run the check every time — it
   stops becoming a no-op the moment the first write lands — but do not read an empty
   result as "this topic is unexplored."

---

## 1. `arxiv` — preprint discovery (14 tools, all live)

| Tool | What it does |
|---|---|
| `search_papers` | arXiv search. Supports `ti:` / `au:` / `abs:` field prefixes, quoted phrases, `AND`/`OR`/`ANDNOT`, `categories[]`, `date_from`/`date_to`, `sort_by` relevance\|date, `max_results` ≤ 50. **The recency workhorse.** |
| `get_abstract` | Abstract + metadata for one ID, no download. Relevance triage before spending tokens. |
| `download_paper` | Fetches full text (HTML first, PDF fallback), stores locally, paginated via `start`/`max_chars`. Required before `read_paper` / `semantic_search`. |
| `read_paper` | Reads an already-downloaded paper as markdown, paginated. Errors if not downloaded. |
| `list_papers` | Lists locally downloaded IDs. Currently returns 0. |
| `semantic_search` | Vector similarity **over local downloads only**. Useless until papers are downloaded. Needs `[pro]` extras. |
| `reindex` | Rebuilds the local semantic index. |
| `list_paper_latex_sections` | Section outline from LaTeX source. |
| `get_paper_latex_section` | One section of LaTeX source, ≤ 50k chars. **Best way to read just Method or Experiments.** |
| `get_paper_latex` | Bounded raw LaTeX source. |
| `citation_graph` | Citations + references via Semantic Scholar. **Currently 429-throttled.** |
| `export_citations` | BibTeX from authoritative arXiv metadata, ≤ 50 IDs, deterministic keys. Never model-generated. |
| `watch_topic` | Saves a standing query as a persistent alert. |
| `check_alerts` | Returns only papers new since last check, per watch. |

**Rate limits / auth:** no key required, no key detected. arXiv's public API expects
polite pacing (~1 request / 3s); avoid large parallel bursts. `citation_graph` inherits
Semantic Scholar's unauthenticated quota and is currently exhausted.

**Useful categories:** `cs.CV`, `cs.LG`, `cs.AI`, `eess.IV`, `eess.SP`, `stat.ML`.

---

## 2. `papers` — peer-reviewed literature (42 tools across 21 backends)

Shape: for most backends there is a `search_X`, a `download_X`, and a `read_X`.
Plus three cross-cutting tools: `search_papers` (aggregator, dedupes across sources),
`download_with_fallback` (source → OA repos → Unpaywall → optional Sci-Hub), and
`get_crossref_paper_by_doi`.

### Backend status — probed live

| Backend | Search tool | Status | Use for |
|---|---|---|---|
| OpenAlex | `search_openalex` | ✅ live | **Primary peer-reviewed search.** Returns citation counts + DOI. |
| Semantic Scholar | `search_semantic` | ⚠️ works standalone, returned 0 inside the aggregator — throttled | Abstracts, citation counts, `year` filter (`2019`, `2016-2020`, `2010-`, `-2015`) |
| Crossref | `search_crossref` | ✅ live | DOI resolution, publisher/venue metadata, `filter` (e.g. `from-pub-date:2024`), `sort`, up to 1000 results |
| dblp | `search_dblp` | ✅ live | **Venue signal for CS.** Returns venue string + year (e.g. `IEEE Trans. Geosci. Remote Sens.`) |
| DOAJ | `search_doaj` | ✅ live | Open-access journals — strong for MDPI *Remote Sensing* (S1 target) |
| Europe PMC | `search_europepmc` | ✅ live | Life-science-adjacent agronomy |
| PMC | `search_pmc` | ✅ live | OA full text, biology-leaning |
| PubMed | `search_pubmed` | assumed live (same NCBI backend as PMC) | Rarely relevant here |
| OpenAIRE | `search_openaire` | ✅ live, but noisy — returned a GitHub repo as a "paper" | EU-funded project outputs. Low signal; use narrowly. |
| CORE | `search_core` | ✅ live, but low precision on short queries | Repository aggregation |
| arXiv (via papers) | `search_arxiv` | ✅ live | Redundant — prefer the `arxiv` server, which has better query syntax |
| **Google Scholar** | `search_google_scholar` | ❌ **DEAD** — empty on two different queries (scrape-blocked) | — |
| **BASE** | `search_base` | ❌ **DEAD** — returns empty | — |
| **CiteSeerX** | `search_citeseerx` | ❌ **DEAD** — returns empty | — |
| **SSRN** | `search_ssrn` | ❌ **DEAD** — returns empty (metadata-only connector anyway) | — |
| **Zenodo** | `search_zenodo` | ❌ **BROKEN** — `'str' object has no attribute 'isoformat'` | Use the Zenodo website directly for datasets |
| **HAL** | `search_hal` | ❌ **BROKEN** — same `isoformat` crash | Would have been useful for French agri-RS (PASTIS/BreizhCrops); use OpenAlex instead |
| **Unpaywall** | `search_unpaywall` | ⚠️ DOI-lookup only, not keyword search; returned empty on a live DOI | Prefer `download_with_fallback`, which uses it internally |
| bioRxiv | `search_biorxiv` | category-filtered, last 30 days only — **not a keyword search** | Rarely relevant |
| medRxiv | `search_medrxiv` | same limitation | Not relevant |
| IACR | `search_iacr` | crypto only | Not relevant |

**Retrieval tools:** `download_with_fallback` (best default — takes `source`,
`paper_id`, optional `doi`/`title`), `download_semantic` (accepts `DOI:`, `ARXIV:`,
`PMID:`, `URL:` prefixes), `read_semantic_paper` (extracts text). `download_crossref`,
`download_openalex`, `read_crossref_paper`, `read_openalex_paper` are **stubs** — they
only return "not supported" messages. `download_scihub` / `use_scihub:true` exists;
**leave it off** — default to legitimate OA routes.

**Rate limits / auth:** no API keys configured. OpenAlex and Crossref reward a mailto
in the UA but work without. CORE and Semantic Scholar throttle unauthenticated traffic —
Semantic Scholar is visibly throttled today. Keep `max_results_per_source` small and
avoid firing all 21 sources at once.

---

## 3. `zotero` — my library (26 tools; cloud write access confirmed)

| Tool | Role |
|---|---|
| `zotero_whoami` | Identity + scopes. Call first in any session. |
| `zotero_search_items` | **Check-before-fetch.** `q`, `qmode` (`titleCreatorYear` default \| `everything` = notes + PDF text), `tag` and `itemType` boolean filters (`\|\|`, `&&`, leading `-`), `collectionKey`, `since`, paging, `response_format: detailed` (needed before any write — gives `version`). Returns `totalResults`. |
| `zotero_semantic_search` | Meaning-based search (BM25 + vectors, RRF). **Requires `zotero_index` build first — index is currently empty (0 docs).** |
| `zotero_index` | `build` / `refresh` / `status`. Status now: 0 documents, 0 vectors, embedder `local`. |
| `zotero_get_item` | Full record by key; `include_children`, `include: bib\|citation\|csljson`. Returns the `version` needed for updates. |
| `zotero_get_fulltext` | PDF passages with page locators; `query` for relevant passages, `page_range`, `precise_pages`. **Use this to cite a claim with a page.** |
| `zotero_fulltext` | Low-level get/set/since on an attachment's indexed text. Not a search. |
| `zotero_list_collections` | Read-only collection list. Currently `[]`. |
| `zotero_manage_collections` | `list` / `create` / `rename` / `reparent` / `delete` / `add_items` / `remove_items`. **Creates FYP-Ideation-2026.** |
| `zotero_create_items` | Batch create/update. Auto-chunks at 50. Validates against the schema — one bad item blocks the whole batch. Include `key` + `version` to update. |
| `zotero_update_item` | PATCH one item. Handles 412 retry. `dry_run:true` previews the diff. Arrays (tags, collections) are **replaced wholesale, not merged**. |
| `zotero_schema` | Valid fields + creator types per item type. **Call before constructing items.** |
| `zotero_manage_tags` | `list` / `add` / `remove`. Tags are case-sensitive. |
| `zotero_list_tags` | Read-only tags with usage counts. |
| `zotero_tag_audit` | Audit library against a controlled vocabulary with required tiers. |
| `zotero_scholar` | **The citation-graph tool.** OpenAlex (Crossref fallback), DOI-keyed. `lookup` / `references` (backward) / `citations` (forward, most-cited first) / `related`. Flags `inLibrary` per result. ✅ verified live. |
| `zotero_import` | Resolve DOI / ISBN / arXiv id / URL to metadata, optionally `save_to_library`. **Needs a translation server** (`ZOTEUS_TRANSLATION_SERVER_URL`) — not configured, so expect setup instructions instead of results. Treat as unavailable. |
| `zotero_export` | `bibtex`, `biblatex`, `ris`, `csljson`, `csv`, … `better-biblatex` needs desktop Zotero + BBT — **`localApi:false`, so it will degrade to stock biblatex.** |
| `zotero_bibliography` / `zotero_format_bibliography` / `zotero_styles` | Formatted output; resolve style ids ("APA 7th" → `apa`) before formatting. |
| `zotero_attachment` | `upload` / `download` / `info`. Uses file-storage quota. |
| `zotero_sync` | Version-based delta since a library version. |
| `zotero_saved_searches` | Stores definitions; **the cloud API does not execute them.** Re-run as `zotero_search_items`. |
| `zotero_groups` | Group libraries. Currently `[]`. |
| `zotero_trash_items` | Reversible delete. **Use this, not the next one.** |
| `zotero_delete_items` | Permanent purge. Requires `ZOTEUS_ALLOW_DELETE=true` **and** `confirm:true`. Do not use. |
| `search_tools` | Tool catalog discovery. |

**Auth:** `ZOTERO_API_KEY` present in `.mcp.json`, user library `21185707`, write enabled
on user + group libraries. `localApi:false` — no desktop Zotero running, so all reads and
writes go through the cloud Web API.

**Rate limits:** Zotero's Web API rate-limits and returns `Backoff`/`Retry-After`. The
server's own instructions say to **call Zotero tools sequentially, never in large
parallel batches** — long or parallel calls time out. Honour that.

---

## 4. Routing table by task type

| # | Task | Call FIRST | Fallback | Never |
|---|---|---|---|---|
| 1 | **Do I already have this?** (every task starts here) | `zotero_search_items` `q=<title/author>`, `qmode=everything` | `zotero_semantic_search` — only after `zotero_index action:build` | Assume empty ⇒ unexplored. The library *is* empty right now. |
| 2 | **Bleeding-edge method sweep, 2024–2026** | `arxiv__search_papers` + `categories:["cs.CV","cs.LG"]` + `date_from:"2024-01-01"`, `sort_by:"date"` | `papers__search_semantic` with `year:"2024-"` | `search_google_scholar` (dead) |
| 3 | **Peer-reviewed coverage / systematic-review breadth** | `papers__search_openalex` | `papers__search_papers` `sources:"openalex,crossref,dblp,doaj"` (small `max_results_per_source`) | `sources:"all"` — fires 6 dead backends and burns quota |
| 4 | **Backward citation chase (what does it cite?)** | `zotero_scholar` `action:"references"` + DOI | `arxiv__citation_graph` (429 today) | Assuming `papers` can do this — it cannot |
| 5 | **Forward citation chase (who cites it?)** | `zotero_scholar` `action:"citations"` + DOI | `papers__search_openalex` on the title, read `citations` | — |
| 6 | **Find the neighbourhood of a key paper** | `zotero_scholar` `action:"related"` | `arxiv__semantic_search` — only after downloading papers locally | `arxiv__semantic_search` on an empty local store |
| 7 | **Venue + impact signal** | `papers__search_dblp` (venue string) | `papers__search_openalex` (citation count) + `papers__search_doaj` (OA journal) | Any claim of impact factor — no tool provides one |
| 8 | **Read a paper's Method / Experiments only** | `arxiv__list_paper_latex_sections` → `arxiv__get_paper_latex_section` | `arxiv__download_paper` → `arxiv__read_paper` (paginate with `start`/`max_chars`) | Dumping a whole PDF into context |
| 9 | **Get the PDF of a non-arXiv paper** | `papers__download_with_fallback` (`source`, `paper_id`, `doi`) | `papers__download_semantic` with `DOI:<doi>` | `download_scihub` / `use_scihub:true`; `download_crossref` and `download_openalex` (stubs) |
| 10 | **Verify a dataset is real, free, and reachable** | `WebFetch` / `WebSearch` on the actual portal (N3 list) | `papers__search_openalex` for the dataset paper → its access section | `papers__search_zenodo` (crashes) — use the Zenodo site |
| 11 | **Recency standing alert on a shortlisted topic** | `arxiv__watch_topic` → later `arxiv__check_alerts` | Re-run `arxiv__search_papers` with `date_from` | — |
| 12 | **Save a shortlisted paper to my library** | `zotero_schema item_type:"journalArticle"` → `zotero_create_items` with `collections:[<FYP key>]` + `tags` | `zotero_create_items` then `zotero_manage_collections action:"add_items"` | `zotero_import` (no translation server configured) |
| 13 | **Build the shortlist collection** | `zotero_manage_collections action:"create", name:"FYP-Ideation-2026"` — **once**, reuse the returned key | `zotero_list_collections` to recover the key if lost | Creating it twice — Zotero allows duplicate names |
| 14 | **Bibliography for the write-up** | `arxiv__export_citations` for arXiv IDs (authoritative metadata) | `zotero_export format:"bibtex"` scoped by `collection_key` | `better-biblatex` (no desktop Zotero — silently degrades) |
| 15 | **Tag hygiene check before hand-off** | `zotero_list_tags` | `zotero_tag_audit` with an inline vocabulary | — |

---

## 5. Write-back protocol — `FYP-Ideation-2026`

1. ~~`zotero_manage_collections action:"create", name:"FYP-Ideation-2026"`~~ **DONE 2026-08-04.**
   The collection key is **`MAW3C3DU`**. Do not create it again — reuse this key.
2. Before every fetch, run task #1. Do not re-add an item that already exists.
3. `zotero_schema item_type:"journalArticle"` (and `preprint` / `conferencePaper`) before
   constructing anything. Do not hand-write field names.
4. `zotero_create_items` in batches ≤ 50, each item carrying
   `collections:["<FYP key>"]` and its tags inline — cheaper than a second tagging pass,
   and it avoids the wholesale-array-replacement trap in `zotero_update_item`.
5. Tags are **case-sensitive**. Controlled vocabulary, one from each tier:

   - **Source:** `src:arxiv` · `src:peer-reviewed` · `src:dataset` · `src:portal`
   - **Theme:** `theme:sar` · `theme:optical` · `theme:fusion` · `theme:uav` ·
     `theme:aquaculture` · `theme:parcel-boundary` · `theme:cloud-gaps` ·
     `theme:label-scarcity` · `theme:smallholder`
   - **Region:** `geo:sea` · `geo:singapore` · `geo:malaysia` · `geo:eu`
   - **Verdict:** `verdict:baseline` · `verdict:competitor` · `verdict:enabler` ·
     `verdict:dataset` · `verdict:rejected`
   - **Constraint flag** (only when relevant): `flag:H1-novelty` · `flag:H3-imagery` ·
     `flag:H5-compute` — mark *why* a paper matters to a constraint.

6. Never call `zotero_delete_items`. If something must go, `zotero_trash_items`.
7. Sequential Zotero calls only. No parallel batches.

---

## 6. Known-broken, in one place

| Tool | Failure | Do instead |
|---|---|---|
| `papers__search_google_scholar` | Empty on all queries — scrape-blocked | OpenAlex + Crossref + dblp |
| `papers__search_base` | Empty | OpenAlex |
| `papers__search_citeseerx` | Empty | OpenAlex |
| `papers__search_ssrn` | Empty | — (not relevant to this FYP) |
| `papers__search_zenodo` | `'str' object has no attribute 'isoformat'` | Zenodo website via WebFetch |
| `papers__search_hal` | Same crash | OpenAlex (covers French agri-RS) |
| `papers__search_unpaywall` | DOI-only, returned empty on a live DOI | `download_with_fallback` |
| `papers__download_crossref` / `download_openalex` / `read_crossref_paper` / `read_openalex_paper` | Stubs returning "not supported" | `download_with_fallback` |
| `arxiv__citation_graph` | HTTP 429 (Semantic Scholar, no key) — twice | `zotero_scholar` |
| `arxiv__semantic_search` | Local store empty (0 papers) | Download papers first, or use `arxiv__search_papers` |
| `zotero_semantic_search` | Index empty (0 docs) | `zotero_index action:"build"` first, or `zotero_search_items` |
| `zotero_import` | No translation server configured | `zotero_create_items` with metadata from `papers`/`arxiv` |
| `zotero_export format:"better-biblatex"` | No desktop Zotero (`localApi:false`) | `format:"biblatex"` |
| `zotero_saved_searches` | Cloud API stores but does not execute | Re-run as `zotero_search_items` |
