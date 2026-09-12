# T3 Code can shorten the Nautilus implementation plan

2026-09-11. Source audit and final reconciliation by Astra, following four GLM reading assignments.

**Recommendation:** use T3 Code as an implementation reference before writing the affected Nautilus tickets. It already contains substantial examples for custom lint, shared schemas, independent workspaces, browser evidence, native skill invocation, and durable command handling. These can replace design guesswork. They do not make the nineteen Nautilus tickets implemented or accepted.

Audited repository: [pingdotgg/t3code](https://github.com/pingdotgg/t3code/tree/7bd7f99e6cab940892ff9240549c507bfd066aee), pinned at `7bd7f99e6cab940892ff9240549c507bfd066aee`. The root [MIT license](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/LICENSE#L1-L20) permits reuse with its copyright and permission notice retained. Dependencies and imported skill bundles have separate provenance and license obligations.

This was a **source-and-test reading**, not a test run, live product verification, comprehensive security audit, or recommendation to install T3 Code. No dependencies were installed and no repository script, browser, deployment, upload, or provider authentication was executed. The original Nautilus implementation plan remains paused.

## Start with these mechanisms

### 1. Test new rules through the real tool

**Helps T08 and T19. This is the clearest direct match.**

T3 Code has [six custom lint rules](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/oxlint-plugin-t3code/index.ts#L10-L21). Its test helper creates a temporary source fixture and lint configuration, launches the installed linter, and checks both the exit behavior and the named diagnostic. It does not stop at unit-testing a rule function.

- [Real-linter fixture harness](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/oxlint-plugin-t3code/test/utils.ts#L93-L178).
- [Example rule with actionable messages](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/oxlint-plugin-t3code/rules/no-inline-schema-compile.ts#L99-L153).
- [Permitted and prohibited fixtures](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/oxlint-plugin-t3code/rules/no-inline-schema-compile.test.ts#L7-L82).
- [Production severities](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/vite.config.ts#L122-L126) and [CI check invocation](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/.github/workflows/ci.yml#L49-L56).

**Change to our approach:** reuse the fixture-harness shape for Nautilus's existing validator. Keep each rule's failing example, permitted example, rule name, and replacement instruction together. Do not adopt T3's particular style rules without a recurring Nautilus failure to justify them.

**Limit:** one registered rule is configured as a warning, while the others shown are errors. A rule appearing in the plugin does not mean it blocks CI. The fixture helper deliberately raises the tested rule to error inside its own test configuration. T3 also has per-file legacy ceilings; those are not permission to raise a Nautilus allowance to get a pass.

### 2. Derive editor-facing schemas from the same runtime definition

**Helps T13. There is an actual generator, not just an architectural claim.**

The project-file definition in the contracts package feeds a decoder and a JSON Schema generator. The marketing app serves the generated schema for editor support.

- [Shared contract consumption and generation](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/packages/shared/src/t3ProjectFile.ts#L4-L42).
- [Schema-serving route](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/marketing/src/pages/schema/t3.json.ts#L1-L10).
- [Tests for schema identity, supported fields, and serialization](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/packages/shared/src/t3ProjectFile.test.ts#L12-L59).

**Change to our approach:** make the existing capsule definition the source for validation, templates, argument handling, and generated reference material. Use this example to settle the composition pattern, rather than designing a second declaration format.

**Limits:** T3 uses Effect Schema. Adopting that dependency is not required to copy the principle. Its optional project-file parser returns `null` for malformed input; that behavior is appropriate for optional defaults, not for fail-closed capsule admission. This example does not supply Nautilus's complete duplicate-declaration detector or generated documentation table.

### 3. Give each workspace its own state and predictable starting ports

**Helps T03/T04 and the workspace prerequisite. It does not clear P1.**

T3 identifies linked Git worktrees from their Git-directory pointer and derives a local `.t3` state directory. Its dev runner derives a starting port offset from the worktree path and separately handles availability.

- [Worktree identification and local state directory](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/packages/shared/src/devHome.ts#L16-L103).
- [Deterministic starting offset](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/scripts/dev-runner.ts#L229-L277).
- [Tests for explicit-home precedence and isolation from an ambient shared home](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/scripts/dev-runner.test.ts#L1269-L1317).
- [Agent procedure for retaining the environment across turns](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/.agents/skills/test-t3-app/SKILL.md#L13-L43).

**Change to our approach:** make state-directory identity part of workspace preparation, and record the actual selected URL and ports. Do not reuse a developer's live database accidentally. Do not tear down a useful preview merely because one assistant turn ended.

**Limits:** hashed offsets can collide, so they are not a guarantee of unique ports. Nothing here establishes Nautilus's slowest launch step or a measured speedup. Existing dirty work still needs the owner decision specified by P1.

### 4. Reuse the preview operation and evidence contract

**Helps T04 substantially. It is not a ready-made Nautilus `preview-check`.**

The repository has more than screenshot instructions. It defines callable preview operations, brokers them to a browser host, and implements evidence capture in the desktop app.

- [Preview status, opening, navigation, resize, and screenshot tool contracts](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/mcp/toolkits/preview/tools.ts#L53-L142).
- [Per-session host assignment tied to a live connection](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/mcp/PreviewAutomationBroker.ts#L85-L99).
- [Actual capture: accessibility tree, PNG, console entries, network entries, and action history](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/desktop/src/preview/Manager.ts#L3609-L3652).

**Change to our approach:** specify one evidence response containing the URL, viewport, screenshot file, diagnostics, and action results. Return a typed unavailable-host error when the real capability is absent. Keep the agent's browser assignment stable during a flow.

**Limits:** this implementation depends on T3's desktop/browser infrastructure. The requested 1440/390 captures, reduced motion, maximum tile dimensions on both axes, seeded-error acceptance, and capsule-authorized host access remain Nautilus work. Resizing CSS layout is not equivalent to testing a real mobile browser.

### 5. Reuse the per-PR preview workflow pattern, subject to authorization

**Also helps T04. Deployment and verification are separate pieces.**

A `preview:web` label opts a same-repository PR into a non-production Vercel deployment. The workflow checks out the PR's exact head commit and updates a marker-identified comment with the deployment URL and revision.

- [Scope, label gate, and exact commit checkout](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/.github/workflows/web-preview.yml#L18-L55).
- [Deployment and URL-comment implementation](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/.github/workflows/web-preview.yml#L67-L132).

**Change to our approach:** retain a branch/revision-to-preview relationship and update a standing evidence comment instead of scattering URLs. The workflow's runner vendor is not part of the portable lesson.

**Limits:** reading this workflow proves configuration exists, not that a deployment succeeded. It uses T3's own authorized project and secrets. It grants no authority to deploy ours, and a successful deployment still needs the worker's real preview check.

### 6. Match the native skill-invocation protocol

**Helps T06, with a useful lesson for recent handoff friction.**

T3 has a small adapter that turns a recognized `$skill` mention into the slash-command text block Claude Code expects. It preserves surrounding text and leaves unknown dollar tokens alone.

- [Dispatch transformation and its stated native-protocol assumptions](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/provider/Drivers/ClaudeSkillDispatch.ts#L1-L79).
- [Transformation tests](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/provider/Drivers/ClaudeSkillDispatch.test.ts).
- [Instructions omitted when their tools are not attached](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/provider/CodexDeveloperInstructions.ts#L22-L43).

**Change to our approach:** a tryout should use the provider's supported invocation route, then inspect the actual invocation event. Merely delivering a skill body or mentioning its name is insufficient. Extra instructions should match attached capabilities.

**Limits:** the CLI behavior is documented by T3 and supported by string-transformation tests here, not reproduced in this audit. This does not override our harness's manual-only skill restrictions. It does not implement a skill-publication tryout gate or prove semantic application.

### 7. Borrow real multi-client tests and deterministic async waiting

**Helps T02. The repository has stronger evidence than the first audit slice found.**

A server test opens three real WebSocket clients, dispatches a turn through one client, waits for both thread clients to reach the final event sequence, then disconnects and reconnects another client from an earlier cursor.

- [Multi-client dispatch and observation](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/server.test.ts#L11485-L11609).
- [Reconnect from retained cursors](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/server.test.ts#L11625-L11638).
- [Drainable worker: completion waits for queued and in-flight work](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/packages/shared/src/DrainableWorker.ts#L1-L69).
- [Test that enqueues more work while processing is active](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/packages/shared/src/DrainableWorker.test.ts).

**Change to our approach:** use the real command/subscription interface and explicit completion signals. Do not equate an empty queue with an idle worker. Add the plan's unique marker and prohibited-delivery failure to Nautilus's own journey.

**Limits:** this is a protocol/integration test, not two authenticated browsers asserting rendered DOM. It uses test-provider infrastructure, not proof of a paid provider round trip. Neither this test nor the proposed Nautilus journey ran during the audit.

### 8. Separate committed intent, external effects, and accepted delivery

**Helps T02/T10/T13 and recovery, without replacing Nautilus's receipts.**

The orchestration engine checks durable command receipts before deciding again. It rejects reuse of a command ID against another aggregate. Event appends, projected state, and the accepted command receipt commit in one database transaction. Publication to subscribers follows that commit.

- [Receipt lookup and aggregate-conflict check](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/orchestration/Layers/OrchestrationEngine.ts#L144-L172).
- [Transaction followed by publication](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/orchestration/Layers/OrchestrationEngine.ts#L273-L327).
- [Test: failed projection rolls back the command's events, and retry writes them once](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/orchestration/Layers/OrchestrationEngine.test.ts#L1594-L1713).
- [Explicit distinction between acknowledgement and effect completion](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/docs/internals/overview.md#L44-L83).

**Change to our approach:** make each receipt say which milestone it proves. Keep durable intent and its derived state consistent, then record effects separately. Use command IDs and expected state to reject stale or contradictory retries.

**Limits:** a database command receipt is not a SHA-256-bound quality acceptance receipt. The transaction does not include external provider calls or filesystem effects. Replay is not exactly-once execution of those effects. T3's production `RuntimeReceiptBus` is intentionally a no-op for a test-only signal, so that bus is not the acceptance mechanism to copy.

### 9. Reuse upload validation primitives, not a claimed PR uploader

**Helps part of T05. The proposed external transport remains unresolved.**

There is a real attachment-upload implementation outside the initial workspace audit's assigned slice. It signs metadata including expected size and expiry, rejects invalid/expired tokens, writes through a temporary file, checks the received byte count, and removes partial files.

- [Token and upload handling](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/assets/AttachmentUpload.ts#L96-L221).
- [Expected bytes, generic files, and oversized-stream tests](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/assets/AttachmentUpload.test.ts#L130-L200).

**Change to our approach:** use the signed-size, expiry, staging-file, and cleanup patterns when evaluating an authorized existing transport.

**Limits:** these are attachments stored by T3, not a demonstrated GitHub PR-media upload service. The CI rule [forbidding committed PR-only assets](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/.github/workflows/ci.yml#L30-L36) is policy enforcement, not an uploader. This does not establish the plan's per-machine, upload-only, rotatable credential contract or complete T05.

## Two implementations we must not transplant unchanged

### Permission modes are not capsule admission

T3's [new-thread default is Full access](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/docs/user/permission-modes.md#L3-L14). Its [Codex translation](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/provider/Layers/CodexSessionRuntime.ts#L509-L541) maps that mode to no approval prompts and full access. [OpenCode's full-access branch](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/provider/opencodeRuntime.ts#L484-L519) returns broad allow rules before its environment-file protections are considered.

This does not mean T3 has no authorization. It has provider approval handling and [MCP toolkit-capability checks](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/mcp/McpInvocationContext.ts#L11-L55). It means those controls are not the same as a release-bound Nautilus capsule and OS-enforced workspace boundary.

A useful narrower example is [rescoped session-only approval](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/provider/Layers/ClaudeAdapter.ts#L183-L213), with [tests preventing a session choice from becoming a persistent local setting](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/provider/Layers/ClaudeAdapter.test.ts#L5968-L6020). Reuse the scope-preservation lesson, not broader defaults or new authority.

Likewise, [T3's model manifest supports remote updates](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/provider/ModelManifest.ts#L1-L44). Its cross-reference validation is useful. Allowing a network-updated catalog to change executable model authority would conflict with the plan's immutable release binding.

### Checkpoint restore does not preserve arbitrary later edits

The concrete Git driver [restores the checkpoint into the worktree/index, cleans untracked paths, and resets the index](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/vcs/GitVcsDriver.ts#L801-L834). This is deliberate workspace-revert behavior, not conflict-safe recovery of a mixed shared tree.

The reactor does [check provider rollback support before restoring files](https://github.com/pingdotgg/t3code/blob/7bd7f99e6cab940892ff9240549c507bfd066aee/apps/server/src/orchestration/Layers/CheckpointReactor.ts#L754-L795). That is useful ordering, but filesystem restore still precedes later provider rollback. It is not an atomic transaction spanning both systems, and a recorded failure is not proof that no partial effect happened.

**Keep Nautilus's journaled landing, prior-release retention, and protection of conflicting later edits. Do not use this restore operation to resolve P1.**

## What changes in the nineteen-ticket plan

These are proposed implementation inputs, not changed acceptance criteria or permission to resume the paused plan.

| Ticket | Evidence available here | Recommended adjustment |
|---|---|---|
| T01 | PR/check presentation, linking, workflow examples | Reuse useful presentation pieces. Still prove the worker triggers CI and reads failed logs without a human relay. We did not establish that path here. |
| T02 | Real multi-client protocol/reconnect tests and deterministic async waiting | Adapt the journey structure. Retain the unique marker, real Nautilus interfaces, negative seed, and separate rendered-DOM journey. |
| T03 | Workspace setup patterns and CI optimization configuration | Treat them as candidates. P2 measurements must still select the bottleneck and establish the ten-run comparison. |
| T04 | Browser tool contracts, desktop evidence capture, PR preview workflow | Start from these concrete interfaces rather than inventing the shape. Keep authorization, capture policy, and seeded console-error checks. |
| T05 | Signed attachment-upload primitives and partial-upload tests | Reuse validation ideas. Authorized transport, GitHub-facing evidence, rotation, and agent-only-skill acceptance remain unresolved. |
| T06 | Native skill-dispatch adapter and practical test skills | Reuse invocation protocol and operational writing. Still implement and verify the recorded tryout/publication gate. |
| T07 | No evidence deciding our tooling cadence | Remains an owner proposal. Do not infer team consent from upstream practice. |
| T08 | Rules with real-tool fixtures and actionable diagnostics | Adopt the test-harness pattern for evidence-backed recurring Nautilus corrections. |
| T09 | Shared schemas, runtime instruction builders, practical steering files | Use as examples. Still prove the specific ARCHITECT rule reached a fresh worker before trimming it. |
| T10 | Structured failures and durable event records | Useful collector inputs. We did not establish the required weekly newcomer-question triage process. |
| T11 | Instructions exist, but no verified owner-only authorship enforcement | Do not infer human authorship or a worker-write prohibition. Keep the owner decision and behavioral refusal test. |
| T12 | Reasoned refusals and provider permission translation | Reuse clarity and scope-preserving translation. Our standing refusal rules and admission enforcement remain separate. |
| T13 | Concrete schema → decoder → generated JSON Schema composition | Use this to settle the single-source design. Keep strict admission and our drift/propagation acceptance. |
| T14 | Detailed onboarding and troubleshooting skills | Reuse the instructional structure. We did not establish the required controlled cold-start improvement test. |
| T15 | Instructions conditional on attached tools | Apply that narrow lesson. No measured equivalence of our minimal-profile completion rate is established. |
| T16 | Judgment-heavy instructions alongside on-demand source references | Use as editorial examples, not authorization to rewrite owner instructions or proof that the cold start will not regress. |
| T17 | Named metrics and observable shared mechanisms | Useful evidence sources for our ledger. No career payoff or corrections-removed count is established. |
| T18 | Environment retention and restart guidance | Useful procedure. No verified counterpart to our owner-initiated monthly prompt-packet schedule. |
| T19 | Six custom rules with fixtures and explicit CI severity | Strong implementation reference. Our three specific lint families and runtime budget still need their own tests. |

P0, P1, and T-lib are not solved by finding this repository. T3's model/catalog design is not an admission receipt for our Opus route. Its workspace helpers do not identify which existing dirty files can be set aside. Its instruction approach does not create room under our Chart byte limit.

## What the final source check corrected

The GLM reports were useful reading leads, not final authority. Astra followed the consequential claims into production code and test assertions, including source outside the workers' assigned slices.

- **Environment-file protection:** the first execution draft overstated it. OpenCode's protection applies to the supervised modes shown, not Full access.
- **Authorization:** “T3 has no authorization” was too broad. Toolkit checks and provider approvals exist; Nautilus-equivalent admission was not established.
- **Session-scoped approval tests:** these exist in `ClaudeAdapter.test.ts`; the reading slice had missed them.
- **Two-client testing:** a claim based on an incomplete slice missed the server's real multi-client/reconnect test. It still is not the requested two-browser DOM test.
- **Schema generation:** the generator and its serving route exist. They are stronger evidence than a comment asserting publication.
- **Media upload:** the PR-assets policy does not prove a working PR uploader. The separate attachment-upload implementation is useful but solves a different storage path.
- **CI feedback:** linking a PR and showing check results does not prove an agent consumed failed-step logs.
- **Recovery:** the concrete Git restore driver rules out describing the whole revert path as protection for arbitrary later edits. Capability checks, metadata compare-and-swap, and filesystem conflict preservation are different claims.
- **Input availability:** the contracts package was supplied to the recovery worker. Its claim that those files were unavailable was incorrect; not reading a file is not missing access.

## Audit execution limits

The four source-reading assignments ran through admitted GLM capsules on the pinned Nautilus release. Their first automated checks rejected malformed or out-of-range citations. Fresh repair attempts were made. The execution and recovery JSON files retained string-valued `tests` references where the fixed checker expected `{path, start, end}` objects, so the controller stopped those repeated defects for architect diagnosis rather than continuing equivalent retries.

The task's illustrative `tests: []` shape did not explain element types well enough, and the generic failure “undefined not assigned” was poor repair guidance. That is an audit-contract problem to correct before reusing this packet. The checker was not weakened, and rejected drafts received no quality receipt.

**This report is the final reconciliation of source-verified recommendations, not certification of every raw worker report or completion of the native ticket plan.** The raw drafts, native run IDs, checker evidence, and remaining states are retained in [the audit run record](file:///Users/thebeast/.nautilus/releases/gsp-app-completion-kernel-fixes/var/workspaces/theo-ideas/astra-t3code/RUN.md). No T3 test execution or Nautilus implementation acceptance is claimed.
