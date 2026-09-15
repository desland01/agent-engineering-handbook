# skills/agent-feedback-engineering — Feedback engineering: heading-reader review

Date: 2026-09-13. Subject: `skills/agent-feedback-engineering/index.html` (reader README). Reviewer route: glm-5.3-flash, headings read with bodies withheld first, then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Recurring failures justify a standing check | Repeated failure turns ad-hoc fix into permanent check | Same: repeats across runs, review feedback becoming automation; single defects need explicit request | MATCH | — | no change needed |
| Evidence defines the check's boundary | Observed failure evidence sets the check's scope | Same: concrete bad case identifies the protected property, paired with a known-good case | MATCH | — | no change needed |
| Existing rules receive the constraint first | Constraint goes into the nearest existing mechanism before a new one | Same: extends an existing rule to avoid a second drifting check; carrier list given | MATCH | — | no change needed |
| The failure chooses the mechanism | Failure type picks rule vs executable enforcement | Same: shapes → compiler, patterns → pattern checks, runtime → symptom tests, repo-wide → shared gate, judgment → guidance | MATCH | — | no change needed |
| Proportionate proof shows the change working | Verification sized to the change, at the affected boundary | Same: bad case fails, good case passes, real command loads the check; wording review for instruction changes | MATCH | — | no change needed |
| Exceptions remain explicit and narrow | Bypasses are written and tightly scoped | Same: narrow allowances or targeted suppressions; broad escapes are not proof | MATCH | — | no change needed |
| The sources support repeated-failure guards | Closing reference note | Same: two practitioners, both with stated non-proofs | MATCH | — | no change needed |


Maker answer to the notes: the next-action line is the standard's designed closing sentence, not a template label; no change.
