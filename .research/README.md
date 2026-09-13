# .research/ — working directory for the CURRENT run

Everything here is written by the orchestrator only (subagents return JSON to
the orchestrator; they never write files). Layout and stage ownership are in
`docs/01_pipeline.md`.

At the end of a run the orchestrator copies this whole directory to
`research-archive/run<N>/`. Then this directory is cleared for the next run.

Git: contents are ignored except this README (see .gitignore). Archive copies
are committed.

To resume a run: `RUN_LOG.md` says which stage completed last. Delete the
file(s) you want regenerated and tell the orchestrator `resume from stage N`.
