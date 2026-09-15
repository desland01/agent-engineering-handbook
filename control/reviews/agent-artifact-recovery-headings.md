# skills/agent-artifact-recovery — Artifact recovery: heading-reader review

Date: 2026-09-13. Subject: `skills/agent-artifact-recovery/index.html` (reader README). Reviewer route: glm-5.3-flash, headings read with bodies withheld first, then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Use it when work stops midway | Trigger: interrupted run with partial completion | Same: crashes with completed outputs, stale corrected results, lost structured summaries; routes other problems elsewhere | MATCH | — | no change needed |
| Give it records and real artifacts | Inputs: task records plus actual artifacts | Same: all artifacts, work order, receipts, delivery evidence, session identity | MATCH | — | no change needed |
| The agent compares intention with reality | Agent diffs intended outcomes against actual artifacts | Same, via byte fingerprints of finished artifacts; fingerprint difference proves different bytes, not correctness | MATCH | — | no change needed |
| Measured properties decide whether work survived | Survival judged by measurable properties, not narrative | Mostly; main claim is that you choose the completeness property, tolerance, and overrun policy, and measurement gates reuse | MATCH | — | no change needed |
| Recovery resumes only the missing stage | Only unfinished stages are redone; finished work preserved | Same: snapshot before mutation, reuse decisions after the full batch is known, fallback to verified artifacts | MATCH | — | no change needed |
| Its report makes each decision visible | Report names each recovery decision and why | Same: separates produced / delivery-proven / receipt-recorded, includes comparisons justifying reuse | MATCH | — | no change needed |
| The limits prevent unsafe recovery | Boundaries against destructive or overconfident recovery | Same: fingerprints don't identify versions, receipts go stale, no credential/external authorization | MATCH | — | no change needed |
| Selected evidence supports resumable work | Ambiguous in headings; curated vs per-task evidence | One selected source (one qualified example) supports resumable work; does not prove the package; trial cases unexecuted | MATCH | — | no change needed |


Maker answer to the notes: the next-action line is the standard's designed closing sentence, not a template label; no change.
