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
`control/reviews/design-qa.md`, `control/reviews/diagrams.md`.

## As a ticket acceptance target

`acceptance.qualityReceipt` is written by the host only after `REVIEW.md` reads *ship* or
every *fix first* item has an *applied* row in `ANSWER.md` and the re-render passes
`build/check-report.cjs`. The receipt's `reason` names both files.


## Review the lesson as a reader

Phase 2 addition, 2026-09-13. This section supplies reviewer instructions for later
authorized lesson and skill-README work. It does not launch a review or authorize the
historical dispatch template above. Use the current task’s admitted route and record
one subject’s findings in `control/reviews/<subject>.md` under the current directory rules.

Inputs: the approved lesson title and ownership from `control/plan.md`, the delivered
source and rendered article, `control/lesson-standard.md`, the applicable primary-source
citations, and the actual `--lessons` output. A structural pass establishes only its
measured properties. Apply these instructions equally to skill reader READMEs and their
rendered pages, not to the package’s agent-facing instruction interface.

1. State the useful distinction the opening teaches. Compare it with the approved
   lesson’s one change. Reject an opening that asks the learning question, repeats an
   instruction, or promises material the article does not teach. Require two or three
   complete thesis sentences, not fragments that happen to satisfy the counter.
2. Inspect rendered evidence at a narrow phone and desktop size, recording the actual
   dimensions. Confirm the complete title and opening fit together in the first viewport
   without clipping or overflow. The character budget alone does not prove this.
3. With section bodies withheld, write the claim each heading leads you to expect.
   Then compare those expectations with the corresponding bodies. Reject headings whose
   words are grammatical but ambiguous, topical rather than conclusive, or inconsistent
   with the section. A vocabulary hit may be a noun: establish that a plain verb actually
   functions as a verb. Apply the clause requirement at every authored heading level.
4. Trace the teaching dependency between adjacent sections. State what the earlier section
   establishes that the later section uses. Reject outline filler, repeated advice, padding,
   or an unexplained jump. Check that each section contains at least three complete
   evidence-led sentences, including the explanation of the sources. Lists of labels,
   code punctuation, abbreviations and fragment counting cannot substitute for prose.
5. Inspect every factual claim about a named person’s practice. Follow its nearby primary
   citation to the specific timestamp or anchor, and compare the claim with the material.
   Record reachability separately from evidential support. Preserve quoted-through
   attribution, sponsorship, opinion versus measurement, repository authorship limits,
   proposal versus merged state, historical versus current runs, and unresolved findings.
   No citation means remove or qualify the claim. Do not manufacture an anchor or result.
6. Confirm the final sources heading states what the sources show. Check that each listed
   source contributes evidence, that inline citations name the right entry, and that no
   unrelated navigation or source padding conceals missing support. Local reference
   resolution and URL syntax do not prove an external resource exists or supports a claim.
7. Read the final paragraph as an instruction to the reader. Require exactly one concrete
   next action in one complete sentence. Reject a recap, multiple actions joined into one
   sentence, a question or a list of choices. Do not give the action an h2 that would
   contradict the section-length rule.
8. Inspect visible copy for instruction field names, file paths, hashes, code spans,
   format names and tool internals. State the reader-facing meaning instead. Evidence
   addresses and invisible markup identifiers may retain technical detail. A check for
   one banned phrase is not a complete instruction-copy or technical-leak check.
9. For skills, compare the actual README with the rendered reader article. Confirm the
   same thesis → dependent sequence → primary evidence → next-action shape, including
   when the skill helps, required inputs, result and verification. A rendered SKILL.md
   or a passing HTML fixture does not prove README delivery or source/render agreement.

For each finding, record the page and location, expected claim or behavior, observed
material, violated standard and necessary correction. Reconcile each as applied with
changed evidence, or overruled with a reason. Record unavailable sources or rendered
evidence as unresolved rather than passing. Preserve the plan’s three groups and ten
lesson titles. Do not add research quotas, extra model routes or another approval gate.
