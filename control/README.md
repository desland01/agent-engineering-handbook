# control/ — how this directory is organised

One file per purpose, named by what it is. The date lives on the file's first line and in
git, never in the file name. A new round of the same work **overwrites** the file; the
previous round is in git history. Nothing here is ever suffixed with a date, a letter or
"final". Handoffs and other read-once files are not kept here at all: they go to
`~/ephemera/` (`handbook-handoff.md`), where everything is deleted 48 hours after it was
last touched.

| File | What it is |
| --- | --- |
| `plan.md` | The plan of record for the design system and the handbook. Rewritten as it changes. |
| `tickets.md` | The executable ticket graph derived from the plan. |
| `patterns.md` | Composition patterns extracted from the reference sites; input to design work. |
| `skill-evals.md` | Whether the skills are used and working, from run records; updated when an eval runs. |
| `design-notes.md` | Design decisions and the delegation record, running. |
| `design-skill-standard.md` | The role-first standard every design skill follows (referenced from `ARCHITECT.md`). |
| `design-review-capsule.md` | The review capsule template (route, evidence, report format). |
| `reviews/<subject>.md` | One review record per reviewed subject: what was checked, by which route, findings, the maker's answers. A worker's raw output sits beside it as `<subject>.<role>.json`. |
| `proposals/<skill>.SKILL.md` + `.RESULT.md` | A proposed skill body and the authoring result that accompanies it, until published. |
| `runtime/<deliverable>/` | Deliverables for the Nautilus runtime (patch, tests, preparer, provenance), staged here until applied. |

Rules for adding to it:

1. Before creating a file, look for the file that already has this purpose and overwrite
   or extend it.
2. A review is named for its subject (`reviews/headings.md`), not for the round or the
   reviewer; a second review of the same subject replaces the first.
3. Worker workspaces under `~/.nautilus/.../workspaces/` are named `<route>-<subject>`
   (`astra-headings`, `glm-heading-reader`); the run's own record carries its timestamp.
4. Scratch, tiles and screenshots never land here; they go to the session scratchpad or
   the worker's `evidence/`.
