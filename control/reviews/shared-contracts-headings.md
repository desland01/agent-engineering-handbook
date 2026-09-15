# You keep shared contracts consistent across layers: heading-reader review

Date: 2026-09-13. Subject: `lessons/shared-contracts.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| One contract gives every layer one meaning | One shared contract defines the shape for all layers | Same | MATCH | — | no change needed |
| Derived consumers remove competing shapes | Generate consumers from the contract to stop duplicate shapes | Same | MATCH | — | no change needed |
| Types catch drift before execution | Static types catch drift at build time | Same; with the limit that import rules prove only the imports they examine | MATCH | — | no change needed |
| Runtime checks cover what types cannot | Validate at runtime what types can't guarantee, incl. authorization | Same | MATCH | — | no change needed |
| Deployed clients still need compatibility | Deployed clients constrain contract changes | Same; additive changes, versions, compatibility windows | MATCH | — | no change needed |
| One trace proves the contract holds | An end-to-end trace demonstrates the contract works | Same; a three-check sequence (break a field, malformed data, unauthorized access) plus a stale-client test | MATCH | — | no change needed |
| The evidence supports enforced shared boundaries | Sources support enforced shared contracts | Same, with qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes. No template-label sentences. No front-facing paths, hashes, or tool internals.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
