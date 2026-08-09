# RESEARCH BRIEF — FYP Ideation 2026

**Every subagent spawned in any later phase MUST read this file in full before doing
anything else. Do not paraphrase, compress, or summarise the constraints block below.
Evaluate every candidate idea against every constraint, explicitly, by ID.**

---

--- BEGIN CONSTRAINTS BLOCK ---

# FYP Constraints — Eashwar Siddha, BSc CS with AI, Univ. of Nottingham Malaysia

## HARD (non-negotiable — an idea failing ANY of these is disqualified, no exceptions)

H1. NOVELTY. The project must either solve an unsolved problem or be a materially
    better version of an existing solution. "Materially better" means a defensible
    delta: new method, new data regime, new deployment constraint, or a measurable
    improvement over a named published baseline. Re-implementing a known pipeline on
    a new region is NOT novelty. "Applied X to Y country" is NOT novelty unless the
    region introduces a genuine technical problem (e.g. persistent cloud cover,
    sub-pixel field sizes, absent labels).

H2. NOT GENERIC. Automatically REJECT any idea whose core is:
    - a chatbot / LLM advisory assistant / RAG-over-agri-documents
    - a dashboard, monitoring portal, or "farm management system"
    - leaf-photo disease classification (PlantVillage-style)
    - a plain NDVI / vegetation-index time-series viewer
    - tabular yield prediction from weather + soil CSVs
    - re-running an existing crop-type-classification benchmark
    - a mobile app whose only ML is calling someone else's model API
    If the one-sentence summary could describe 50 other FYPs, it fails H2.

H3. IMAGERY. Satellite imagery OR drone/UAV imagery must be the primary input, not a
    garnish. Sensor fusion is fine and encouraged (SAR + optical, drone + satellite).
    State sensor, resolution, revisit, and licence for every idea.

H4. GEOGRAPHY + USER. The end user must be farmers (or the agronomists/co-ops directly
    serving them) in Southeast Asia — Singapore preferred — or the EU. Name the actual
    user segment. "Farmers globally" fails this.

H5. COMPUTE + BUDGET. Must be fully executable by one student on a MacBook Pro M4 Pro
    (24GB unified memory, Apple Silicon, PyTorch MPS backend, NO CUDA) with a total
    cash budget of RM 200 (~USD 45). This means:
    - all imagery must be free-tier or open licence
    - training must fit in <= 24 GB unified memory
    - a full training run must complete in <= 12 hours on MPS, OR on free Colab /
      Kaggle T4 quotas
    - reject anything needing commercial VHR imagery (Planet, Maxar, Airbus) unless a
      genuinely free research/education tier is verified with a working access route
    - reject anything requiring the student to fly their own drone unless a free public
      drone dataset can substitute
    Flag total dataset size in GB — anything over ~200GB is a practical fail.

H6. PITCH. The elevator pitch must land with an FYP judging panel of CS academics in
    60 seconds. Strong pitches have: a named user, a quantified pain, a hard technical
    core the panel can see is non-trivial, and something demoable live on a laptop.

## SOFT (nice-to-have, use as tiebreakers)

S1. Should be publishable — realistically a workshop paper (CVPR EarthVision, ECCV
    CVPPA, IGARSS, ICLR ML4RS, AGU) or a mid-tier journal (Remote Sensing MDPI,
    Computers and Electronics in Agriculture).
S2. BUILD-HEAVY, NOT READ-HEAVY. I like building things. Target roughly 70% engineering
    (working system, real pipeline, demoable artifact) and 30% research. An idea that is
    mostly literature synthesis or theory is a poor fit even if novel.

## STEERING NOTES — confront these head-on, do not dodge them

N1. SINGAPORE RESOLUTION PROBLEM. Singapore has ~1% of land in agriculture, ~250 farms,
    mostly vertical/indoor/rooftop, under the "30 by 30" policy. Sentinel-2 at 10m
    cannot resolve these plots. So for Singapore, satellite-primary land-farming ideas
    are likely dead on arrival. Viable Singapore routes to evaluate explicitly:
      (a) drone/UAV imagery over small plots and rooftop farms
      (b) satellite over COASTAL AQUACULTURE — Johor Strait fish farms, algal bloom
          and water-quality early warning (Sentinel-2/3 water bands); this is farming,
          it is satellite-appropriate, and it is not generic
      (c) treat Singapore as the deployment/demo site but Malaysia/Indonesia/Thailand
          as the data source, and justify why
    If none survive, say so plainly and recommend EU instead. Do not force it.

N2. EU IS DATA-RICH. The EU has free Sentinel-1/2 plus free parcel-level ground truth
    (LPIS, EuroCrops, PASTIS, BreizhCrops, AI4Boundaries) and live regulatory drivers
    (CAP monitoring, EUDR deforestation compliance, eco-scheme verification). Weigh
    this honestly against the SEA options.

N3. SEED SOURCES to VERIFY (do not trust this list — check each is live, free, and
    accessible from Malaysia, and record the access route):
    Copernicus Data Space Ecosystem, Microsoft Planetary Computer STAC, AWS Earth
    Search STAC, Google Earth Engine (free non-commercial), NASA HLS, ESA WorldCover,
    Dynamic World, EuroCrops, PASTIS / PASTIS-R, BreizhCrops, AI4Boundaries,
    Agriculture-Vision, WeedMap, Sugar Beets 2016, Sen1Floods11, Sentinel-1 GRD.
    Then go find sources this list is missing.

--- END CONSTRAINTS BLOCK ---

---

## Operating rules for subagents

1. Read this entire file before your first tool call.
2. Read `research/TOOL_ROUTING.md` before your first tool call. It tells you which MCP
   server to use for your task type, and which tools are known-broken.
3. Judge every candidate idea against H1–H6 by ID. State pass/fail per constraint. A
   single HARD failure disqualifies the idea — say so and stop working on it.
4. Use S1–S2 only to rank ideas that already pass all HARD constraints.
5. Confront N1–N3 directly. Do not quietly avoid the Singapore resolution problem.
6. Never assert a dataset is free, live, or accessible without recording the concrete
   access route you verified (URL, API, auth requirement, approximate size in GB).
7. Report negative results. "This route is dead and here is why" is a valid, valued
   deliverable.
