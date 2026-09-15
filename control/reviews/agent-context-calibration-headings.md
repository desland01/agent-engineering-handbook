# skills/agent-context-calibration — Context calibration: heading-reader review

Date: 2026-09-13. Subject: `skills/agent-context-calibration/index.html` (reader README). Reviewer route: glm-5.3-flash, headings read with bodies withheld first, then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Repeated confusion makes the skill useful | Trigger: agent repeatedly misses project knowledge | Same, plus reviewing steering instructions and probing a fresh agent | MATCH | — | no change needed |
| Your evidence defines the diagnosis | Collected evidence, not opinion, defines the problem | Same: misses, repeated questions, rejections, or a probe task; probe changes nothing standing | MATCH | — | no change needed |
| The agent chooses the nearest carrier | Flagged: nearest existing file/store vs transport mechanism | Different main claim: the agent classifies each miss (fact / shape / pattern / judgment), and the class determines the carrier (comment, rule, check, skill, standing instruction). "Nearest" is not the operative idea | PARTIAL | Miss class determines the carrier | applied: Miss class determines the carrier |
| Checks show whether the change landed | Checks demonstrate the calibration took effect | Same: wording comparison and loading confirmation for instructions, behavioral checks at the boundary for code/config | MATCH | — | no change needed |
| Boundaries keep the change proportional | Change stays proportional to evidence; no blanket rewrites | Same: only observed misses, no deletion of expertise on one inconclusive probe, no padding | MATCH | — | no change needed |
| The sources support evidence-led changes | Closing reference note backing evidence-led changes | Same, with explicit non-proofs for each source | MATCH | — | no change needed |


Maker answer to the notes: the next-action line is the standard's designed closing sentence, not a template label; no change.
