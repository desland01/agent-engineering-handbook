# You remove obstacles for the next contributor: heading-reader review

Date: 2026-09-13. Subject: `lessons/better-environments.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Newcomers reveal hidden work | Newcomers expose undocumented work others stopped noticing | Same | MATCH | — | no change needed |
| One obstacle should guide the repair | Pick the single highest-cost obstacle to fix | Record one blocked obstacle, diagnose its cause, and route it to the matching lesson; prefer obstacles that affect several contributors | PARTIAL | Record the obstacle, then route it | applied: Record the obstacle, then route it |
| Shared repairs should reach everyone | Fixes must land in the shared environment so everyone inherits them | Same | MATCH | — | no change needed |
| Stable paths prevent repeated interruptions | Keeping paths stable/reproducible avoids repeated blocks | Tolerable workarounds become recurring barriers for unattended agents; repair the failing shared step instead of adding retries or parallel work | PARTIAL | Repair the failing step before adding retries | applied with a vocabulary-safe verb: Fix the failing step before adding retries |
| Comparable attempts show whether work improved | Measure before/after attempts to prove improvement | Same; with the caveat that task difficulty must stay comparable and one success proves only the repaired path | MATCH | — | no change needed |
| The sources support shared environment changes | Closing sources section backing shared environment changes | Same, with explicit non-guarantee qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes ("You will turn one observed obstacle into a shared improvement, then compare the next equivalent attempt"). Template-label/artifact sentences: none. Front-facing paths: body links point at sibling markdown source files (`useful-instructions.md`, `recurring-mistakes.md`, `working-previews.md`, `missing-tools.md`) rather than rendered `.html` pages — a build artifact visible to readers. No hashes or tool internals.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
