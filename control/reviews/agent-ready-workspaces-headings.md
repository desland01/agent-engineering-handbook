# skills/agent-ready-workspaces — Agent-ready workspaces: heading-reader review

Date: 2026-09-13. Subject: `skills/agent-ready-workspaces/index.html` (reader README). Reviewer route: glm-5.3-flash, headings read with bodies withheld first, then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Use it when setup blocks agents | Use when a workspace lacks what an agent needs to start | Same: cold-start agents stall; also isolated previews; existing passing workspace needs no rework | MATCH | — | no change needed |
| Give the skill access and priorities | Input: access scope and setup priorities | Same: access, existing run paths, outcomes to preserve; inferred priorities you can override; existing secret handling | MATCH | — | no change needed |
| The skill will add only missing pieces | Fills gaps without restructuring working setup | Same: inspects first, adds only absent capabilities, extends the existing setup chain | MATCH | — | no change needed |
| A fresh start proves readiness | Flagged: destructive reset vs cold verification run | Cold-start run confirmed: run the changed setup from the future agent's starting point, confirm the app opens with isolated state, no interaction | MATCH | — | no change needed |
| The skill stops at workspace preparation | Prepares the workspace only, does not start task work | Same boundary, plus limits: no deployment or shared-state deletion, configured settings alone prove nothing, no overbuilding | MATCH | — | no change needed |
| The sources show previews need access | Sources establish previews require access | Same: both examples show access to running software or inspectable evidence, neither proves full readiness | MATCH | — | no change needed |


Maker answer to the notes: the next-action line is the standard's designed closing sentence, not a template label; no change.
