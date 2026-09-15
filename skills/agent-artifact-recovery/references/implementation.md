# Artifact recovery: applying the method

The method is studied from Matt Pocock's Course Video Manager at pinned commit
`4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`, summarized in
[guide 12](https://github.com/desland01/agent-engineering-handbook/blob/main/guides/12-artifact-identity-and-recovery.md).
The pattern generalizes; the source's specific hashes, tolerances, retry cap
and fleet counts do not — do not copy them as best practice.

## Worked case: was the interrupted export finished?

An encode run dies halfway through a batch. For each existing output file:

1. **Measure**, don't assume: read the real duration (or rows, or sections).
   The source's `isExportUnacceptablyShort` refuses a file with no playable
   duration at all, refuses a shortfall greater than the tolerance, and always
   accepts an overrun — that overrun policy is the source's choice for its
   duration check (container rounding must not fail a good release *there*),
   not a general media rule. Pick the tolerance and the overrun policy from
   your own product's data; the source chose one second from live data, not as
   a universal constant, and a positive duration validates nothing else about
   the file.
2. **Check the receipt**: does the digest sidecar's recorded size equal the
   file's current size? The source's sidecar records digest, content hash,
   size and an optional measured duration — a sidecar written before
   durations were recorded legitimately has none. Unparseable or size-
   mismatched means *absent* — re-derive the digest, do not guess.
3. **Decide reuse on bytes**: hash the file and compare against prior actual
   outputs. The recipe (which clips, what order, which format) decides only
   where the result belongs, never whether it is already shipped.

## Worked case: a fix that must reach the destination

A renderer bug is fixed. The re-render lands at the same recipe address as
the truncated output it replaces. If the publish step decides reuse from the
recipe, it copies the old broken bytes forward and cancels the corrected
encode — exactly the source's recorded incident, where three short exports
shipped and one was live. The fix is procedural: the digest of the produced
bytes decides what is sent; the corrected artifact, its sidecar and its
publication receipt are replaced together.

## Worked case: a lost run summary after completed work

An agent implementation run commits its changes, then its structured summary
comes back malformed.

1. Confirm the work itself is persisted: commits, branch, uploaded files. The
   commits are the source of truth, not the summary.
2. Resume the recorded session with an extraction prompt and the output
   schema; retries stay in-context against the failed extraction's session.
3. **Verify the produce/extract boundary**: compare persisted outputs or
   commit lists before and after extraction. The source's retry wrapper
   passes the produce options through, so nothing mechanically prevents the
   extraction pass from acting again. If persisted state changed, treat the
   boundary as violated and reconcile before reporting done.
4. If no session identity was recorded, do not silently restart: report the
   recovery limit, inspect what persisted, and choose an authorized restart.

## Snapshotting and fallback

Draw the reuse plan from an immutable snapshot — the previous release's
committed receipt plus a current listing — and take it before the pipeline
starts mutating state. Copyability is settled per artifact only once that
artifact has landed, so decide the copy batch once, at the earliest moment
the full set is known; a refused or unlaunchable batch falls back to
uploading the artifacts the machine already holds — never to skipping them,
and never to re-producing work whose bytes are verified. The source says the
same: a plan without entries means every Video "uploads exactly as it does
today".

## Evidence limits carried from the source

- The reuse saving was measured on **short synthetic footage, one machine,
  one ffmpeg/driver combination**, including six concurrent encodes agreeing
  with a serial run. That is plausibility on that setup, not proof of
  bit-for-bit determinism across encoder or driver upgrades. Losing
  reproducibility costs a full re-upload, not a wrong release — size your
  tolerance to that.
- The source's default retry cap, fleet counts and model strings are its
  choices, not policy. Use actual host limits, classified failures and
  evidence of progress.

## Relation to the sibling skills

- Deciding whether a *finished* run's output meets the request is
  agent-output-verification; this skill starts from interruption, staleness or
  a lost record and decides what to reuse versus redo.
- Encoding a *recurring* interruption pattern into a standing check belongs to
  agent-feedback-engineering once recovery has handled the case.
- If artifacts keep being unreadable where they land, the delivery surface is
  agent-ready-workspaces or a tool adapter.
