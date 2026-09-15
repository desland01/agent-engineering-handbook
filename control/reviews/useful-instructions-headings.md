# Write instructions that fix observed confusion: heading-reader review

Date: 2026-09-13. Subject: `lessons/useful-instructions.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Observe confusion before writing | Base instructions on observed confusion | Same | MATCH | — | no change needed |
| Place each correction where it works | Put each correction where the confusion occurs | Same; local vs shared vs reusable placement rules | MATCH | — | no change needed |
| Write decisions with reasons and limits | Record decisions with rationale and boundaries | Same | MATCH | — | no change needed |
| Confirm the next attempt receives it | Verify the next attempt actually applies the correction | Same; adds confirming the running system loaded the changed guidance | MATCH | — | no change needed |
| Promote repeatable failures into checks | Recurring failures become automated checks | Same | MATCH | — | no change needed |
| These sources connect observation to correction | Sources link observation to corrective writing | Same, with qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes. No template-label sentences. No front-facing paths, hashes, or tool internals. Title inconsistency noted at step 1: this page uses imperative "Write instructions…" while the other nine use second-person "You …"; consistent with its slightly different (human-practitioner) audience, but a deliberate choice should be confirmed.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
