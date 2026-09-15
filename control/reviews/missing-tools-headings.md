# You make missing operations usable by agents: heading-reader review

Date: 2026-09-13. Subject: `lessons/missing-tools.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Name the blocked operation precisely | State exactly which operation the agent cannot perform | Same; gap described as an observable result with completion evidence | MATCH | — | no change needed |
| Reuse an existing route first | Prefer existing routes before building | Same | MATCH | — | no change needed |
| Make the route fit the action | Shape the interface to the one action | Same | MATCH | — | no change needed |
| Build only the missing interface | Minimal scope | Same | MATCH | — | no change needed |
| Limit credentials and effects | Least privilege for the new route | Same; adds retirement condition and migration when a native route arrives | MATCH | — | no change needed |
| Test through the agent's real route | Verify via the agent's own invocation path | Same | MATCH | — | no change needed |
| The sources support small, verifiable interfaces | Sources back minimal tool interfaces | Same, with explicit non-authorization qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes. No template-label sentences. No front-facing paths, hashes, or tool internals.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
