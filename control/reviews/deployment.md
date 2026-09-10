# The handbook is live on its domain

September 10, 2026. The resumed handoff was executed through the existing Vercel project.

Production deployment `dpl_4kf8ErLZ2ffFt3rZAfDMHW2WgBrN` reached `READY`, then
`agent-engineering-handbook.dev` was attached to `agent-engineering-handbook`.
The public root returned HTTP 200. Local Stagehand renders at 1440×1100 and 390×850
confirmed the expected title, no horizontal overflow, and empty console/page error arrays.
Both screenshots were opened and inspected. Read-once captures are in
`~/ephemera/handbook-live/` and expire under the ephemera policy.

Before deployment, the existing suite passed: 54 HTML pages and 72 rendered checks.
The cloud build exposed an archive-only layout-check defect: the fallback inventory included
Vercel metadata and installed Python dependencies when Git was absent. The correction omits
generated directories while retaining unknown source files for rejection. A regression fixture
first reproduced the defect, then verified that generated files are ignored and unknown and
dated source files still fail. `build/check.test.py` retains that behavioral check.

An initial upload mistakenly excluded the evidence screenshots. The exclusion was removed;
the successful deployment includes those source assets and passes the cloud build's link and
hash checks. Local agent installations, environment files, scratch files and control records
are excluded from deployment. Agent installations remain on disk and are ignored by Git.

The subsequent composition release is commit `15d5cad`, pushed to `origin/main` after the
mechanical push checks passed (the optional model leg was skipped). Production deployment
`dpl_3pQDnkWp5cxXv93UxKviATKvnpyc` reached READY and was aliased to the same domain.
The live home HTML, CSS, JavaScript and problem graphic all returned HTTP 200 and matched
the reviewed local build byte-for-byte. Live Stagehand captures of the report section at
1440×1100 and 390×850 were opened: no overflow, console errors or page errors. Evidence is
in `~/ephemera/handbook-live-composition/`. Composition, graphic and native scroll motion are
now live; reader-heading work remains blocked on the requested Astra route.
