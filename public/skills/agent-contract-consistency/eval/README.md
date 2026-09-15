# Evaluation cases — agent-contract-consistency

Disposable, source-derived scenarios for a later cold-agent trial of this
skill. Each case gives the agent a small multi-layer fixture (a route table,
a derived or hand-copied client, a runtime schema, an error-tag union) plus a
change request or an observed mismatch, and asks it to reconcile the
interface.

**Status: designed, not run.** No case below has been executed by any agent.
These are not results and no claim of evaluated effectiveness is made. Keep
execution records separate from this public package. Do not publish private
project, account or runtime details.

## Source of each case

Scenarios adapt recorded patterns from the source video's type-safe
composition segment (~13:49–14:17), T3 Code's RPC contracts at pinned commit
`6c583620ff7ad3235b135af7107c0543467eecfa`, and Course Video Manager's
glossary, ADRs, RPC layer and machine gate at pinned commit
`4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`, as summarized in guides 08 and
11. Fixtures are small synthetic TypeScript-style snippets rebuilt for the
trial; nothing from the repositories is bundled or executed.

## How a trial should be scored

- Rename and dropped-tag cases must be caught by an actually run check (the
  fixture's type check or handler call), not asserted from reading.
- The control must pass end to end through the real fixture seam without
  invented rejections.
- Any answer describing types, static import rules or a machine/environment
  suitability flag as authorization enforcement or as a sandbox fails its
  case, whatever else it gets right.
- The authorization case must be handled at the server boundary as its own
  concern.
