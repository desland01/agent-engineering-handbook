# skills/agent-contract-consistency — Contract consistency: heading-reader review

Date: 2026-09-13. Subject: `skills/agent-contract-consistency/index.html` (reader README). Reviewer route: glm-5.3-flash, headings read with bodies withheld first, then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Contract drift appears across repeated shapes | Drift shows when copies of one shape diverge | Same: conflicting names, fields, routes, errors; also planned renames and field changes | MATCH | — | no change needed |
| Your project supplies the authority | Project's own material is the authoritative contract | Same: agent reads durable decisions, finds the authoritative definition, derives consumers from it | MATCH | — | no change needed |
| One contract guides every consumer | One canonical contract drives all consumers | Same: trace the object end to end, remove competing definitions, validate at entry, stable error names | MATCH | — | no change needed |
| Negative checks expose hidden mismatches | Checks designed to fail reveal drift positive tests miss | Same: deliberate rename fails derived consumers, invalid data fails at the real boundary, renamed error exposes stale handlers, unchanged control still passes | MATCH | — | no change needed |
| The result states remaining gaps | Deliverable reports what remains inconsistent | Same: reconciled contract plus named deployed clients, permissions, dependencies outside the guarantees | MATCH | — | no change needed |
| Separate guarantees keep conclusions honest | Distinctions prevent overstating what a check proved | Same: shared types vs runtime data, authorization checked separately, eval cases are designed examples only | MATCH | — | no change needed |
| Sources show interfaces need deliberate boundaries | Cited sources argue interfaces need explicit boundaries | Same: one recorded talk; procedure from inspected but unexecuted examples | MATCH | — | no change needed |


Maker answer to the notes: the next-action line is the standard's designed closing sentence, not a template label; no change.
