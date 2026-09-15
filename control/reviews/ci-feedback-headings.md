# You diagnose failed checks without copying logs: heading-reader review

Date: 2026-09-13. Subject: `lessons/ci-feedback.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Direct access removes the relay | Direct access to CI results removes the human copy-paste relay | Same | MATCH | — | no change needed |
| Run identity keeps evidence attached | Identifying runs by revision/attempt keeps evidence linked to the right change | Same; adds that an unchanged successful retry leaves the first failure unexplained | MATCH | — | no change needed |
| Readable evidence sharpens the diagnosis | Structured/readable failure output yields a more precise diagnosis | Same; complete output kept available, causal block inspected first | MATCH | — | no change needed |
| Diagnosis determines the next move | Diagnosis decides fix vs config vs environment | Same; adds naming unresolved dependencies instead of blind retry | MATCH | — | no change needed |
| The repaired revision must prove itself | The new run must prove the fix on its own evidence | Same | MATCH | — | no change needed |
| The sources show agents receive failures | Sources assert agents receive CI failures directly | Same, with qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes. No template-label sentences. No front-facing paths, hashes, or tool internals.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
