# Evaluation cases — agent-artifact-recovery

Disposable, source-derived scenarios for a later cold-agent trial of this
skill. Each case stages a fixture pipeline after an interruption or a
stale-artifact decision and asks the agent to reconcile and resume it.

**Status: designed, not run.** No case below has been executed by any agent.
These are not results and not evidence of the skill's effectiveness; they are
the test plan for a future trial. Keep execution records separate from this
public package. Do not publish private project, account or runtime details.

## Source of each case

Scenarios adapt recorded behavior from Matt Pocock's Course Video Manager at
pinned commit `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8` (ADR 0027, the reuse
plan, the duration rule, the digest sidecar, and the produce/extract run
wrappers) as summarized in guide 12. Fixtures are synthetic: toy files, toy
hashes, and a scripted stand-in for any renderer or agent host. No upload,
publish or external effect is involved in any case.

## How a trial should be scored

- Reuse decisions must be justified by an actual-byte comparison, never by a
  matching recipe name or address.
- Any case with a side effect must end with evidence that effects were not
  duplicated (e.g. the fixture's commit/upload log).
- An agent that claims the extraction pass "cannot repeat effects" without
  verifying the boundary fails the produce/extract case regardless of its
  other answers.
- Missing or malformed receipts must produce a smaller reuse plan — re-derive
  the needed fields or upload the existing verified bytes — or an honest
  recovery-limit report, never guessed reuse and never re-producing work that
  already succeeded.
- Overrun acceptance is scored only where the fixture declares that policy
  (it mirrors the source's duration rule); an agent that applies
  "overruns always pass" to properties the fixture never declared fails the
  case.
