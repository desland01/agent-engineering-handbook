# You test the result users actually need: heading-reader review

Date: 2026-09-13. Subject: `lessons/prove-it-works.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Accepted results define useful success | Success is a result a user accepts, not a green check | Same | MATCH | — | no change needed |
| User journeys expose hidden failures | End-to-end journeys reveal failures checks miss | Same; decisive assertion placed where the user receives the result | MATCH | — | no change needed |
| Focused checks protect important outcomes | Concentrate checks on high-cost outcomes | Same; stop adding checks once the accepted result is adequately proved | MATCH | — | no change needed |
| Different properties need different evidence | Each property needs its own evidence layer | Same | MATCH | — | no change needed |
| Reproduction turns surprises into tests | Unexpected bugs become permanent regression tests | Same | MATCH | — | no change needed |
| Baselines keep changes meaningful | Compare against a baseline to classify changes | Same | MATCH | — | no change needed |
| Benchmarks compare equivalent work | Benchmarks only valid under equivalent conditions | Same | MATCH | — | no change needed |
| Final gates must reject bad results | The final gate must block bad output, not warn | Same; includes proving the gate rejects a planted bad case | MATCH | — | no change needed |
| The sources show outcome-focused verification | Sources back outcome-centered verification | Same, with qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes ("You will define one accepted result … prove that the final gate rejects a false success"). No template-label sentences. No front-facing paths, hashes, or tool internals.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
