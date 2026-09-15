---
name: agent-artifact-recovery
description: "Reconcile artifacts left by an interrupted or partially published run and resume the right stage without repeating completed work: compare actual output bytes against the recipe that was requested, validate receipts and cached measurements, decide what is safely reusable, and repair a lost result summary without redoing side effects. Use when a pipeline or agent run crashed partway, when deciding whether an existing artifact can be reused or must be re-produced, when a published result looks stale after a fix, or when structured output was lost after the work itself succeeded. Not for judging whether a completed run's output is acceptable (agent-output-verification), creating the reusable rule for a recurring failure (agent-feedback-engineering), or preparing the environment the work runs in (agent-ready-workspaces)."
metadata:
  origin: "Public edition, 2026-09-12, maintained by Desmond Landry (@desland01). Method derived from public source inspection recorded in the Agent Engineering Handbook: Matt Pocock's Course Video Manager (pinned commit 4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8) — ADR 0027, the reuse plan, duration check, digest sidecar and produce/extract run wrappers — summarized in guide 12. Pinned links and evidence limits in references/source-patterns.md. Independent public skill; not affiliated with or endorsed by the cited authors."
---

# Artifact recovery

A crash does not erase the work that finished. Recover by comparing what
exists against what was asked for, then resume only the stage that is actually
missing.

## Keep the two identities apart

- **Recipe identity** names what the work was *told to do* — inputs, order,
  format. It is knowable before any work starts, so it can address where the
  result will land and let stages overlap.
- **Actual-byte identity** is the digest of what was *produced*. It is
  knowable only after the run, and it is the only thing that can say whether
  an existing artifact is the same output you already have.

The source's failure is the cautionary case: a reuse decision keyed on the
recipe alone copied old bytes forward, cancelled the new encode, and wrote the
old digest into the new manifest — a corrected render never reached the site
because a truncated encode had landed at the same recipe address. Decide
reuse from **actual bytes, compared by hash**, never from the recipe address
matching. A re-run with changed inputs lands at a new recipe address and
uploads; a corrected renderer can produce different bytes at the same recipe
address, so the artifact, its cached measurements and its publication receipt
must be replaced together.

A digest difference establishes different bytes, not which version is correct.
The current artifact may already be the intended correction. Check its properties
against the requested inputs and outcome before deciding to produce it again.
If that evidence is missing, report what remains unknown and preserve the existing
artifact; do not infer a need to rebuild or resend from stale metadata alone.

## Accept an artifact on measured properties

Before reusing anything, check completeness on a property you can measure: for
media, measured duration against the summed clip durations; for data, row or
segment counts; for text, required sections. The source's video rule is one
worked shape, specific to that duration check: refuse only a shortfall greater
than a tolerance the source chose from its own live data, accept overruns
(container rounding must not fail a good release *there*), and refuse a file
with no readable measurement. Overrun acceptance is that rule's policy, not a
universal property of media or artifacts — choose the checks and tolerances
from the requested output. Three of that project's 93 exports were silently
short and one was live under the old exit-code-only acceptance; a positive
duration alone would have validated nothing else about those files.

**Receipt and cache validity.** A receipt carrying the fields your check
needs makes the check cost once per artifact lifetime — the source's sidecar
caches digest, content hash, size and an *optional* measured duration (older
sidecars were written before durations were recorded and legitimately hold
none), so do not assume every receipt contains a duration. Validate whatever
it does record against the file's current size on every read, and treat an
unparseable or size-mismatched receipt as *absent*: re-derive rather than
trust it. This is not a complete freshness guarantee. Replacing an artifact
with different bytes of the same size can leave a cached digest stale, so
recompute the digest when outside modification is possible, or invalidate the
cache with the artifact's generation. A missing, unparseable or archived-away
receipt means a smaller reuse plan — every artifact is uploaded exactly as it
would be anyway — never an error and never a guessed reuse. Uploading the
verified existing bytes is the fallback; it is not the same as re-producing
work that already succeeded, and lost reuse metadata alone is not a reason to
redo side effects. Read the three states separately before any authorized
replay — what was produced, what transport evidence shows was delivered, and
what the receipt records — and do not treat a lost receipt as a mandate to
upload again when delivery is already evidenced.

## Snapshot the reuse decision from immutable state

Decide what is reusable from an immutable snapshot taken up front — a
committed receipt from the previous run plus a listing of what exists — never
from state the running pipeline is still mutating. Take the snapshot before
work begins, decide the reuse batch once at the earliest moment the full set
is known, and if the batch is refused fall back to uploading the artifacts the
machine already holds — never to skipping them, and not to re-encoding work
whose bytes are verified.

## Recover the record without repeating the work

When an agent run both does side-effectful work and must emit a rigid
structured result, a malformed summary need not cost the work. The source's
split: run the work **without** the output schema so a serialization failure
cannot abort it; keep the session identity and its commits as the source of
truth; then resume that same session with an extraction prompt and the schema,
retrying in-context against the failed extraction's own session. If the
session identity is missing, report the recovery limit and inspect persisted
outputs before choosing an authorized restart.

**Produce/extract caveat, kept honest:** the extraction pass is intended to
change only serialization, but a prompt saying extraction does no work is not
enforcement. The source's retry wrapper spreads the produce options through,
so the extraction run inherits the same tool options and could commit again.
Where the host offers an admitted read-only mode for extraction, use it;
otherwise treat "extraction repeats no effects" as an invariant to verify —
compare persisted outputs or commit lists before and after — not a guarantee.
An extraction prompt alone cannot prevent repeated effects.

See [implementation.md](references/implementation.md) for worked applications
and [source-patterns.md](references/source-patterns.md) for the pinned code
and its evidence limits.

## Input / output contract

- **Input**: the interrupted or suspect run's artifacts, its recipe/request
  record, any receipts or sidecars, and the stages of the pipeline.
- **Output**: a reconciliation — what is safely reusable (with the actual-byte
  comparison that proved it), what must be re-produced rather than merely
  re-uploaded, and what receipts were replaced — and, for lost-result
  recovery, the resumed extraction plus evidence that no side effect was
  duplicated.

## Acceptance

- Reuse: the plan matches on actual-byte hashes only; a changed input lands at
  a new address and is re-produced, not copied.
- Truncation: a short artifact is refused, an overrun follows the output's
  declared policy (the source always accepts overruns for its duration check
  — that is its rule, not a general default), an unreadable artifact is
  refused.
- Recovery: resuming after a crash between work and extraction reuses the
  recorded identity and produces no duplicate effects.
- Do not blindly hash every output against prior bytes; choose checks and
  tolerances appropriate to the product.

## Known failure cases

- Reusing (or skipping) an artifact because its recipe matches, without
  comparing produced bytes.
- Trusting a cached digest after an outside modification, or a receipt whose
  size no longer matches the file.
- Re-running an entire pipeline because one stage's summary was malformed —
  duplicating commits, uploads or messages.
- Treating an extraction prompt as a read-only guarantee.
- Treating reproducibility as proven from someone else's measurement: the
  source's saving was measured on short synthetic footage, one machine, one
  encoder version. Re-measure on your own toolchain and after upgrades; the
  cost of losing reproducibility is a full re-upload of the affected
  artifacts, not a wrong release — size any tolerance to that cost.

## Do not activate when

- The question is whether a *completed* run's output is acceptable — that is
  agent-output-verification.
- The recurring failure needs a standing rule or test, not a resume
  (agent-feedback-engineering).
- The gap is setup, previews or delivering evidence to the consumer
  (agent-ready-workspaces, or a tool adapter).
- The gap is missing knowledge or steering, not interrupted output
  (agent-context-calibration), or a capability no interface provides
  (agent-tool-adapters).
- Recovery would require new external effects or credentials beyond the
  session's authorization; make the concrete proposal and request only the
  missing authorization.
