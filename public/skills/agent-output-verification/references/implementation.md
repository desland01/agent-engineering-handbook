# Output verification: applying the contract

The general method comes from the Melee for Mac verifier, studied in
[guide 09](https://github.com/desland01/agent-engineering-handbook/blob/main/guides/09-verification-contracts.md),
and from the layered-validation habit in
[guide 13](https://github.com/desland01/agent-engineering-handbook/blob/main/guides/13-layered-validation.md).
The pattern generalizes; the specific hashes, report formats and unit model do not.

## Worked case: a generation task with a completeness report

Suppose an agent is asked to transcribe a two-hour recording into chapters, and
it reports the transcription command succeeded.

1. **Artifact**: the transcript file exists at the path the next stage reads.
2. **Expected property**: chapters covering the full requested span. Derive the
   expected span from the request, not from the previous run — a legitimate
   re-transcription can differ in wording, so a byte or line-count equality
   check against the old file is the wrong expectation here.
3. **Intermediates**: every source segment consumed, no placeholder or empty
   chapters. This is the Melee lesson: its verifier re-reads the build report
   and requires every source unit complete, because the final executable can
   be correct while hiding unfinished work behind substituted originals.
4. **False-success paths**: the command "succeeds" but writes nowhere; the
   report claims counts the artifacts do not contain; an empty input passes
   trivially. Check each deliberately, then keep the smallest check that would
   have caught it.
5. **Verdict wording**: "verified existence, chapter coverage and segment
   completeness locally; the final published form was not exercised here."

## Worked case: a changed output, honestly checked

Suppose the request is to re-encode a video at a lower bitrate. The old file's
hash is now the wrong expectation: matching it would mean nothing changed. The
right expectations come from the request itself — a playable file exists, its
duration still matches the source within tolerance, the bitrate is in the
requested range. Reserve exact-hash identity for tasks whose whole point is
byte-identical preservation. This mirrors the source distinction: Melee's
matching check fits a preservation build; it is not a universal acceptance
condition for renderers, refactors or generated code.

## Worked case: trusting the wrong gate

Suppose CI is green and a reviewer treats that as full validation. Read what
the gate actually required. In the inspected `json-schema-to-typescript` CI,
the aggregate job's success expression named only three of its five declared
dependencies, and it ran with `always()` so other results were not counted.
Branch protection might require more; that setting was not verified. The
transferable action: trace the real command a merge depends on to the
expression that decides it, and prove the gate rejects a relevant bad result
in a disposable fixture before relying on it.

## Proportionality and honest reporting

- Name the layer each check covered: source inspection, isolated fixture,
  mocked command, local execution, remote CI.
- Reuse adequate existing checks instead of building a new suite for every
  accepted result — provided the output those checks accepted is unchanged
  since they last ran. State which prior check is being relied on and why it
  still binds.
- If a property cannot be checked in the current environment (no game data, no
  display, no production credentials), report it as unverified rather than
  widening the claim.
- Partial-environment runs keep their own name. The source project's CI runs
  tool tests and a library build while explicitly documenting that it cannot
  perform the game-data matching check, and its instructions forbid reporting
  CI as a matching build.

## Relation to the sibling skills

- This skill judges **one run's result**. If the same failure has recurred and
  the ask is a standing rule, hand off to agent-feedback-engineering.
- If the output is fine but earlier stages were interrupted and must be
  resumed without repeating completed work, that is agent-artifact-recovery.
- If the artifact cannot reach its consumer (a path on another machine, an
  unreadable attachment), the delivery gap is agent-ready-workspaces' or the
  tool-adapter problem, not a verdict change.
