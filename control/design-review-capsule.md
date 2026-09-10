# The design-review capsule — the gate as a dispatchable unit (C1, C2)

This is the template used four times on 2026-09-10 (astra QA, diagram review r1–r3), written
down so a ticket can bind it. Two files per review: the reviewer's `REVIEW.md` and, beside
it, the maker's `ANSWER.md`. Both are copied into `control/` as `review-<subject>-<date>.md`.

## Capsule (version 4)

```json
{"version": 4, "id": "<plan>-<ticket>-review", "releaseDigest": "<current at dispatch>",
 "workspaceRoot": "<current>/var/workspaces/<plan>/<ticket>-review",
 "allowWrite": ["<workspaceRoot>"], "allowRead": [], "inputs": {},
 "requiredCharts": ["nautilus-core:precise"],
 "tools": ["Read", "Write", "Bash", "Glob", "Grep", "Skill"],
 "modelRoute": "gpt-6-astra", "provider": "local-proxy",
 "limits": {"maxSeconds": null, "maxRequests": null},
 "declaredOutputs": ["<workspaceRoot>/REVIEW.md"], "expiresAt": null}
```

Route: `gpt-6-astra` for composition, copy and diagram reviews (proven); `glm-5.3-flash`
as the parallel second reviewer on composition when cheap. Never the route that made the
work. Bind workspace and digest in the same step as the launch. On a release whose Chart
delivery fails at zero requests, do not dispatch; wait for `current` to move.

## Workspace contents the parent supplies

- `evidence/` — PNG tiles, **≤2000px on both axes**, named `<page>-<width>[-<part>].png`;
  full pages tiled, element captures at reading size (studies at 640px wide, 2× DPR).
- `VOCABULARY.md` — the design language scale; plus `DESIGN.md` when the review is of
  the handbook.
- `PLAN.md` — the maker's pre-flight `<design_plan>` when one exists.
- `TASK.md` — the review task: intent withheld until a first impression is written; per
  item: page@width, what is wrong in one sentence, the evidence (file and place, or a
  value from the built HTML/CSS with line), the rule broken (quoted), a concrete proposed
  fix; then a verdict line — ship / fix first with the blocking item. "Do not pad."

## The maker's answer (`ANSWER.md`, beside the review)

One row per finding: **applied** (with the revision) or **overruled** (with the reason).
No finding closes by silence. The answer names the render or measurement that shows the
fix. When a proposal is wrong — as astra's rail-label fix was, restyling mono labels to
sans — the diagnosis is taken and the fix is not; the row says so. Example:
`control/design-qa-20260910.md`, `control/review-diagrams-20260910.md`.

## As a ticket acceptance target

`acceptance.qualityReceipt` is written by the host only after `REVIEW.md` reads *ship* or
every *fix first* item has an *applied* row in `ANSWER.md` and the re-render passes
`build/check-report.cjs`. The receipt's `reason` names both files.
