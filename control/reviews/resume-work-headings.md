# You resume work without repeating completed steps: heading-reader review

Date: 2026-09-13. Subject: `lessons/resume-work.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Durable records preserve finished decisions | Persist completed decisions so a later run skips them | Same | MATCH | — | no change needed |
| Recipes identify intended work | A recorded recipe identifies intended work and remaining steps | Same; recipe identity is separate from result identity | MATCH | — | no change needed |
| Content identity proves reusable results | Content identity (hash/identity of output) proves a prior result is reusable | Same; unproven identity means redo the work | MATCH | — | no change needed |
| Completeness decides whether reuse is safe | Reuse only complete results; partial results are redone | Same; measurable completeness property stored beside the result | MATCH | — | no change needed |
| Stable names reveal the restart point | Stable names make the stop point visible | Same | MATCH | — | no change needed |
| Fixed snapshots prevent moving reuse decisions | Unclear (flagged); guessed "pin inputs so the reuse decision can't shift" | Build every reuse decision from one fixed snapshot of the last accepted state; if a batch reuse route is refused, fall back only to already authorized individual actions and never widen permissions | PARTIAL | Decide reuse from one fixed snapshot | applied: Decide reuse from one fixed snapshot |
| Checkpoints limit repeated work | Checkpoints bound how much work is redone | Same | MATCH | — | no change needed |
| Summary repair stays separate from completed work | Unclear (flagged) | When completed work survives but its summary is missing or rejected, retry only the summary in isolation and verify no side effects repeated | MATCH (flag resolved) | — | open |
| The sources show durable recovery works | Sources evidence durable recovery | Same, with qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes. No template-label sentences. No front-facing paths, hashes, or tool internals.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
