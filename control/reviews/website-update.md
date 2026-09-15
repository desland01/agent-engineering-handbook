# Website source review — September 12, 2026

Scope corrected to the owner's original-research-only direction. This replaces the earlier implementation audit as the evidence record for the website proposal. Private implementation details have been removed from this file. They are not website teaching material, even if anonymized or labeled as later examples.

## Allowed educational sources

- [Original video extraction](../../evidence/video-research.md) and [nineteen structured observations](../../evidence/video-tips.json), linked to [Theo's video](https://www.youtube.com/watch?v=xmGY276gEFY).
- [Original T3 Code and Melee investigation](../../github-inspection.md), including its pinned source links and dated PR qualifications.
- [Original Course Video Manager investigation](../../matt-pocock-inspection.md), including pinned code, ADRs and open-versus-merged distinctions.
- [Original Boris Cherny investigation](../../boris-cherny-inspection.md), including pinned compiler and public engineering evidence.

An addition must be supportable from this corpus without access to private work. A guide is an index to that evidence, not independent proof that every generalization in it belongs in the new edition. Follow the underlying citation before approving a claim.

Newly searched unrelated repositories are not added to the educational source set. Tools used to build or check the website are not automatically topics to teach on it.

## What counts as an improvement

Correct a statement we got wrong, explain a point incompletely covered the first time, or recover a relevant detail missed in the original research. Consolidation and clearer prose are also allowed. Do not invent a missing point merely to give every lesson an update.

For each proposed correction record:

| Field | Required evidence |
|---|---|
| Current passage | Exact source file and passage in the existing handbook |
| Problem | Incorrect claim, omission, ambiguity, needless duplication, or no change needed |
| Original source | Video moment or pinned repository file/PR from the original corpus |
| Supported correction | What the source actually establishes, distinct from recommendation |
| Qualification | Anecdote, sponsor claim, open PR, inspected code, executed test, or other applicable limit |
| Decision | Correct, add, consolidate, retain, or exclude |

This correction ledger is a next-step deliverable. The following review targets have source support, but this record does not assert that all are currently missing.

## Source-backed review targets

1. **Output completeness.** [Guide 09](../../guides/09-verification-contracts.md) points to [Melee's verifier](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py) and [tests](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_verify.py). Explicit targets, intermediate completeness and final artifact checks answer different questions. A successful partial CI run is not a matching game build.
2. **Usable previews and tool results.** The original T3 report describes browser snapshot and artifact-delivery fixes. A returned path or response is not useful unless the intended consumer can read and act on it. Preserve the source's dates and the distinction between the original narration and later public repository evidence already in that report.
3. **Useful instructions.** The original video covers instruction ownership, steering, pushback and cold-start diagnosis. Preserve the difference between advisory prose and executable checks. Do not add private enforcement mechanisms to explain the public idea.
4. **Shared contracts.** [Guide 11](../../guides/11-domain-language-and-agent-apis.md) links Course Video Manager's [one-transport decision](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0025-local-remote-split-one-http-transport.md) and [typed client](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/rpc-layer.ts). Explain shared vocabulary, client shape, runtime parsing and error behavior without calling type checks, static-import rules or machine suitability signals security boundaries.
5. **Artifact identity and recovery.** [Guide 12](../../guides/12-artifact-identity-and-recovery.md) links the original byte-hash decision, duration checker, sidecar and produce/extract wrappers. Keep recipe identity separate from actual-byte identity. Retain the same-size replacement caveat, source-specific duration tolerance and warning that an extraction prompt does not mechanically prevent repeated side effects.
6. **Layered validation.** [Guide 13](../../guides/13-layered-validation.md) links [Boris's compiler CI](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml). Explain what fixtures, built-output tests, fuzzing and conformance each establish. Do not present inspected tests as locally executed or as exhaustive correctness.

## Three eligible skill proposals

| Skill | Original grounding | Distinction from existing skills |
|---|---|---|
| Output verification | Melee completion contract and Boris's layered validation, guides 09/13 | Judges the current output rather than creating a recurring-failure guard |
| Artifact recovery | Course Video Manager output identity and resumable work, guide 12 | Recovers interrupted work rather than preparing a clean workspace |
| Contract consistency | Video composition, T3 contracts and Course Video Manager shared transport, guides 08/11 | Reconciles existing consumers rather than building a missing tool or placing project knowledge |

Compare against the actual four public bodies: [feedback engineering](../../skills/agent-feedback-engineering/SKILL.md), [workspace readiness](../../skills/agent-ready-workspaces/SKILL.md), [context calibration](../../skills/agent-context-calibration/SKILL.md) and [tool adapters](../../skills/agent-tool-adapters/SKILL.md).

The skill-evaluation proposal and new outside-repository recommendations are withdrawn from this edition. The three remaining skills are proposals, not authored or tested downloads. New package checks should use disposable source-derived fixtures, never private project incidents. Any disclosed result must describe the public package check actually performed.

## Presentation findings, not new lesson topics

The earlier live homepage/index inspection found a long opening with multiple inventory counts, long source-derived tile titles, and navigation grouped by evidence category rather than reader problem. These observations justify the proposed reading redesign. They do not create a new educational section about our implementation work.

Keep the existing visual identity. The design proposal is a shorter entry, ten problem-led lessons, optional technical guides and clear links to original sources. Preserve caveats and attribution even when simplifying titles.

## Migration and publication boundary

The renderer rebuilds `public/` from editable sources and currently parses exact count-bearing README headings. It generates idea paths using display order plus source IDs. The custom-lint observation's source ID starts `tip-19` but its displayed page is 09. Use explicit stable mapping rather than renumbering by assumption.

The ten-lesson map in [the plan](../plan.md) retains every original observation once. Update source joins, counts, aliases, README and tests together. Existing guide and skill paths stay stable.

Review every outgoing surface: HTML, copied Markdown and JSON, skill bundles, source downloads, metadata, README and GitHub diff. No private discovery is allowed merely because its names were removed or it sits in a reference file instead of the article. Historical planning files are not public lesson inputs or approved publication content. Existing history is not rewritten by this task.

The later execution is now integrated locally: ten canonical lessons, three new source-derived skill folders, the updated reading design and legacy redirects. Original research files were preserved. Local source/catalog checks and rendered reader journeys pass; independent supplied-render review passed its stated scope. No commit, push, merge or production publication has been performed. Private execution records are not part of this source review or public website content.
