# Matt Pocock’s Course Video Manager: methods visible in the PRs

The [PR page you linked](https://github.com/mattpocock/course-video-manager/pulls) adds a useful third case study. I inspected the latest 100 PR records across states, selected detailed diffs, and the repository at [`4c1f3f5d4941`](https://github.com/mattpocock/course-video-manager/commit/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8) on September 9, 2026. This is a focused source inspection, not a claim to have reviewed every historical change or run the app.

The strongest pattern is **turning domain decisions into interfaces, executable rules, and recoverable workflows**. The project also makes its own gaps visible: an open documentation cleanup, a missing CI workflow described as present in guidance, and follow-up repairs after major changes. Read those alongside the successful designs.

## A concrete map of the architecture

The current [root guidance](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/CLAUDE.md) and package manifests describe a Turborepo with two applications and shared packages:

| Area | Responsibility | Why it matters to agent work |
| --- | --- | --- |
| `apps/local` | Editing UI, CLI, local media/OBS/ffmpeg and publishing operations | Hardware and local-file work stays on the machine that owns it. |
| `apps/remote` | Authenticated Hono RPC API | Remote agents access domain operations through a supported interface. |
| `packages/core` | Database schema, operations and shared pure domain logic | The remote API can consume the domain without importing desktop-only machinery. |
| `packages/lucide-icons` | Shared icon data and transformation entrypoints | Shared consumers reuse one bounded package. |
| `packages/overlay-renderer` | Standalone media renderer | The local app invokes its built executable; root Turbo filters exclude it, so its checks must be considered separately. |

The [core dependency rules](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/packages/core/.dependency-cruiser.cjs) reject enumerated filesystem-bound imports, imports back into applications, and cycles. This is stronger than simply asking agents to keep the core portable. It remains static dependency checking, not a process sandbox or proof against every indirect runtime capability.

The [CLI RPC layer](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/rpc-layer.ts) derives endpoints from the remote application’s route type, checks implementations against domain service signatures, and forwards argument tuples through a common helper. Most CLI domain operations use the same HTTP path for the author and remote agents. Machine-local commands have explicit entry guards in [local-only.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/local-only.ts). That guard explains why a command cannot run on a remote machine before work begins; its environment flag is a suitability signal, not an unforgeable security boundary. Token authentication and server-side access control are separate.

## Useful PRs and what to carry forward

### Keep vocabulary and decisions durable

[CONTEXT.md](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/CONTEXT.md) defines domain nouns, their relationships and terms to avoid. For example, a Course, CourseVersion, Draft, Pending and Published Version have distinct meanings. Agents can use the same nouns in command help, tests and implementation instead of rediscovering the model through synonyms. [Domain-document guidance](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/agents/domain.md) points to relevant ADRs without demanding that nonexistent documents be created before useful work can start.

[PR #1591](https://github.com/mattpocock/course-video-manager/pull/1591), **still open**, proposes removing changing implementation details from that glossary while retaining fields, invariants, refusals and vocabulary. It relocates missing rationale beside the code that owns it. This is a good template for preserving knowledge during a cleanup, but the proposal must not be described as the state already merged into main.

[PR #1608](https://github.com/mattpocock/course-video-manager/pull/1608), merged September 4, shows why domain language must affect the implementation. A move planner wrote an ordering-derived path into a section title. Removing numbered path prefixes eliminated the renumbering machinery that kept corrupting the actual identity field. The useful lesson is to simplify the model when redundant derived state creates bugs, rather than adding more synchronization around it.

[PR #1611](https://github.com/mattpocock/course-video-manager/pull/1611), merged September 6, links Beats to Learning Goals and adds warnings. Its title sounds absolute, but the implementation deliberately keeps those warnings out of publication blockers. A planning preference and a release invariant need different consequences. Preserve that distinction when writing a skill.

### Prove one real end-to-end path before expanding a platform

[PR #1542](https://github.com/mattpocock/course-video-manager/pull/1542), merged August 11, organizes the local/remote split around sub-issues, including a tracer bullet: mint a token and execute one CLI search remotely. Shared domain operations then expand behind that verified transport, with typed failures and schema-version handling. Existing CLI tests become the transport test surface instead of being replaced by tests of private internals.

The follow-up [PR #1550](https://github.com/mattpocock/course-video-manager/pull/1550), merged later that day, removes automatic migrations from preview builds. The current [remote package](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/remote/package.json) builds core code during deployment without invoking migration. [ADR 0026](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0026-migrations-applied-by-hand.md) records the correction. The original split’s description and some root guidance still mention deploy-owned migrations; consult current executable configuration and the later decision before copying those instructions.

**Apply:** choose one vertical slice that crosses the actual boundary, validate it from the caller’s environment, and only then scale the pattern. A successful local shortcut does not validate remote execution.

### Reuse actual output bytes, not just the requested recipe

[PR #1501](https://github.com/mattpocock/course-video-manager/pull/1501), merged August 4, overlaps exports and uploads, makes progress visible per video, and plans for interrupted work. It moves the immutable submission boundary before media work so later writes cannot alter what is being published.

[PR #1564](https://github.com/mattpocock/course-video-manager/pull/1564), merged August 21, repairs an incorrect reuse decision. The render recipe identifies where an output belongs, but only the produced bytes can establish whether a previous output is identical. A corrected render at the same recipe address must reach the destination. Inspect [the reuse decision](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/course-publish-dropbox.ts) and [ADR 0027](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0027-byte-hash-decides-the-send.md).

The [duration check](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/export-duration-check.ts) rejects nonpositive duration and excessive shortfall against the expected clip duration. Its one-second tolerance and acceptance of overruns are deliberate rules for this application, not general validation of all video defects. The [digest sidecar](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/export-sha256-sidecar.ts) caches hashes and size; it is not an independent guarantee against an arbitrary same-size file replacement outside the managed workflow. Recompute or strengthen cache invalidation when your system allows that kind of mutation.

This complements Melee’s verifier: a hash can be the correct invariant for exact binary preservation, while a recipe hash is an insufficient invariant for media reuse. State what each identifier proves before designing the cache.

### Keep process supervision alive when progress reporting fails

[PR #1551](https://github.com/mattpocock/course-video-manager/pull/1551), merged August 19, investigates an ffmpeg hang associated with progress-pipe drainage. A callback exception could stop consuming output while the child process continued writing. The change isolates callback failures per chunk, drains stdout and stderr concurrently, and keeps useful stderr evidence. The PR describes the production cause as highly likely, so I do not upgrade that diagnosis to an independently reproduced incident.

**Apply:** treat telemetry delivery and child-process lifetime as separate responsibilities. An observer disconnecting should not silently stop the drain that lets a process finish. Test a throwing progress callback and enough output to exercise backpressure.

### Preserve completed work while repairing result formatting

[run-with-extraction.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-extraction.ts) runs production work first and then resumes the same session to extract structured output. [run-with-retry.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-retry.ts) retries a structured-output failure with feedback instead of blindly rerunning the original assignment. Callers include review, update-branch, implement-PR and architecture-review drivers; [tests](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-extraction.test.ts) cover session preservation and failure cases.

This avoids repeating commits or other effects merely because the result summary was malformed. However, the extraction call inherits execution options; the comment that extraction should not commit is not a mechanical read-only boundary. In your own setup, preserve execution receipts and keep any separate extraction/recovery step inside the scope already authorized. Do not copy the source’s model strings, scheduling, credential names, or retry counts as universal policy.

### Place stable prompt material before changing material

[PR #1506](https://github.com/mattpocock/course-video-manager/pull/1506), merged August 5, restructures an article writer’s prompt for caching. Stable instructions and source material precede changing related fields and the current document; the tool definitions stay stable across draft/edit phases. The useful method is to measure actual cache usage and avoid needless prefix changes. Cache limits, retention windows and pricing are provider/version-specific, and a provider switch must follow the owner’s configured route. This report does not repeat the PR’s savings as measurements from our environment.

## What the automation files do—and what their presence does not prove

The repository has GitHub workflows for implementation, review, PRD expansion and architecture proposals. The [implementation workflow](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.github/workflows/agent-implement.yml) reacts to labels, checks issue shape and existing PRs, and passes work to a driver. The [architecture workflow](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.github/workflows/architecture-review.yml) contains a weekday schedule; the [project skill](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.claude/skills/improve-codebase-architecture-project/SKILL.md) seeks deep-module improvements, checks prior proposals, and hands structured output to the driver.

These are concrete orchestration assets, but source inspection alone does not show whether their secrets, permissions or scheduled runs are currently healthy. We have not started them or copied their automatic publishing behavior into this handbook. The project’s approximate per-file token check is a local heuristic, not evidence that every smaller module is deeper or easier to maintain.

The most revealing gap is [PR #1601](https://github.com/mattpocock/course-video-manager/pull/1601), merged September 3. It introduces guidance saying to target tests locally and rely on exhaustive CI. Its body explicitly says `.github/workflows/test.yml` was omitted because the credential could not publish workflow files. The file is still absent from the inspected Git tree, while [testing.md](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/agents/testing.md) says it runs on every PR. The root `test` script also excludes the standalone overlay renderer. Therefore “everything is checked in CI” is not established by the checked-in implementation. A successful isolated retry also does not by itself prove a failure was only resource contention, despite the stronger wording in those testing notes.

**Apply:** inspect the actual command, configuration, selected environment and result before trusting a documented gate. Keep a required manual step visibly incomplete until readback proves it happened. Do not make local testing depend on a safety net that is only described in prose.

## How this changes our guides

[Guide 11](guides/11-domain-language-and-agent-apis.md) covers domain vocabulary, durable decisions, bounded modules and callable agent APIs. [Guide 12](guides/12-artifact-identity-and-recovery.md) covers output identity, resumable work and result-format recovery. The four companion skills include these methods as references rather than as separate overlapping workflows.

Across Matt’s project, Theo’s T3 Code and Melee, the most transferable habit is to make a desired outcome easy to invoke and hard to misreport: precise domain operations, small checks with known coverage, explicit execution ownership, and evidence tied to the artifact actually produced.
