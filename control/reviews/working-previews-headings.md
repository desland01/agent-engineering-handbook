# You give agents a working preview: heading-reader review

Date: 2026-09-13. Subject: `lessons/working-previews.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| A preview needs running software | A preview must actually run, not be described | Same; address must work from the agent's machine | MATCH | — | no change needed |
| Each change needs an isolated preview | Every change gets its own isolated environment | Same; adds separate mutable data and named cleanup ownership | MATCH | — | no change needed |
| The agent tests the real flow | The agent exercises the real user journey | Same; page load alone proves nothing | MATCH | — | no change needed |
| Evidence must reach the reviewer | Evidence is delivered in a reviewer-consumable form | Same | MATCH | — | no change needed |
| A fresh run confirms the preview | A clean fresh-agent run confirms reproducibility | Same | MATCH | — | no change needed |
| The sources show previews in use | Sources show preview practices in use | Same, with qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes. No template-label sentences. No front-facing paths, hashes, or tool internals.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
