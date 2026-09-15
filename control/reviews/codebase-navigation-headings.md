# You navigate unfamiliar code without guessing: heading-reader review

Date: 2026-09-13. Subject: `lessons/codebase-navigation.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| The behavior gives search a target | Start from the observed behavior to define search terms | Same | MATCH | — | no change needed |
| Search builds a working map | Iterative search produces a rough map of relevant code | Same | MATCH | — | no change needed |
| Focused context exposes the route | Narrowing context reveals the execution route | Same | MATCH | — | no change needed |
| Planning separates evidence from action | Plan distinguishes confirmed evidence from intended change | Same | MATCH | — | no change needed |
| Limits keep the map honest | Record what was not explored so the map doesn't overclaim | Same | MATCH | — | no change needed |
| Failed refreshes preserve useful evidence | Unclear (flagged); guessed "keep earlier evidence when a re-run fails" | If a map's build/relationship inputs fail, the new map cannot be trusted; report the gap, restore inputs, and keep the previous useful map until the refreshed one completes | PARTIAL | Keep the old map when refresh fails | applied: Keep the old map when refresh fails |
| A checked route earns the edit | Edit only after the route is verified | Same | MATCH | — | no change needed |
| The sources show exploration comes first | Sources back exploration before modification | Same, with qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes. No template-label sentences. Front-facing paths: body link to `missing-tools.md` (markdown source path in a rendered page). No hashes or tool internals.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
