# How Theo’s systems are actually made

Theo’s public account is [t3dotgg](https://github.com/t3dotgg). Two repositories give useful, different views: [T3 Code](https://github.com/pingdotgg/t3code) is a multi-client coding-agent application; [Melee for Mac](https://github.com/t3dotgg/melee4mac) is a fork that its owner explicitly labels an automated experiment. The latter is particularly strong evidence of the workflow you are interested in: preserve a hard invariant, make verification executable, improve navigation and tooling, then integrate bounded batches with recorded results.

This report combines direct source inspection, GitHub PR and check-run metadata, and a small local execution of the Melee verifier tests. It does not claim that we rebuilt either application or reproduced their gameplay/performance results. The video was published **July 21, 2026**. Melee’s inspected changes are **September 8**, and many T3 improvements below are August or September; they show later applications of the ideas, not proof they were the exact implementation used during filming.

## The strongest direct connections

| Video idea | Concrete public evidence | What this establishes |
| --- | --- | --- |
| Replace repeated corrections with code | T3 has a real custom Oxlint plugin; a tooltip regression became a configured lint error in [PR #7209](https://github.com/pingdotgg/t3code/pull/7209). | Rule implementation, valid/invalid fixtures, config integration, and successful PR Check/Test runs are observable. |
| Agents need usable previews and artifacts | [PR #10501](https://github.com/pingdotgg/t3code/pull/10501) repairs unusable browser snapshot output; [#10572](https://github.com/pingdotgg/t3code/pull/10572) transfers recordings to the environment where the agent can read them. | A tool returning data or a path is insufficient if the consumer cannot use it. |
| A small upload skill closes an integration gap | Video frames show `files.tslop.org`; [Melee PR #13](https://github.com/t3dotgg/melee4mac/pull/13) embeds before/after stage screenshots from that exact host. | Direct evidence that the public host is used for PR evidence. The upload service’s server code and this PR’s invocation logs were not found. |
| Teach shared project knowledge | Both repos have root guidance and task-specific docs; T3 has an isolated-app-testing skill, Melee has ownership and source-navigation guides. | These are concrete knowledge assets; their existence alone does not prove every agent loaded them. |
| Protect the actual outcome | Melee’s verifier requires a matching executable **and** complete source reports. | Local synthetic tests reproduce the difference between hash-only success and complete-source verification. |
| Reduce repeated setup friction | T3 sanitizes inherited launcher environment; Melee automates the tested Mac compiler wrapper and preserves installed tools on failed downloads. | Durable tooling changes replace per-agent workarounds. |

## T3 Code: boundaries that make agent work tractable

Read the [architecture overview](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/docs/internals/overview.md) alongside the [RPC contracts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/packages/contracts/src/rpc.ts). The server owns workspace files, Git, terminals, and provider processes. Web, desktop, and mobile clients control that environment through authenticated RPC. Shared client connection/domain state lives in `packages/client-runtime`; provider differences live behind adapters. This localizes changes and makes ownership explicit. Authentication and per-method authorization remain distinct.

The event path is concrete in [OrchestrationEngine.ts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/apps/server/src/orchestration/Layers/OrchestrationEngine.ts): a command reaches the decider; generated events, projections, and a durable command receipt commit in one SQL transaction; in-memory state and event publication follow commit. Reactors perform later external work. An acknowledgement therefore proves recorded intent, not finished work. Apply that distinction to a job queue, deployment, or import before considering whether your system needs event sourcing at all.

Tests have a separate completion mechanism. [DrainableWorker.ts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/packages/shared/src/DrainableWorker.ts) tracks outstanding work across enqueue and completion so `drain` waits for the current item as well as queued items. [RuntimeReceiptBus.ts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/apps/server/src/orchestration/Layers/RuntimeReceiptBus.ts) provides test milestones; its production implementation is intentionally a no-op. Do not mistake those runtime receipts for durable command receipts or use a test-only bus as production truth.

### Their lint rules are working policy, with explicit limits

The [plugin index](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/oxlint-plugin-t3code/index.ts) registers six rules. [vite.config.ts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/vite.config.ts) loads the plugin and selects severities/scopes. Examples:

- [`no-inline-schema-compile`](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/oxlint-plugin-t3code/rules/no-inline-schema-compile.ts) identifies selected immediately invoked Schema compiler calls inside functions, where recompilation is avoidable. [Fixtures](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/oxlint-plugin-t3code/rules/no-inline-schema-compile.test.ts) distinguish hoisted decoders and dynamic factory cases. It is configured as a **warning**, so the rule’s presence alone does not establish a blocking CI gate.
- [`no-native-title-tooltip`](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/oxlint-plugin-t3code/rules/no-native-title-tooltip.ts) visits JSX intrinsic elements and flags direct `title` attributes while allowing specific accessibility uses. It is an **error**. Custom-component props and spread attributes are outside this narrow check; it does not prove that every possible native tooltip is prevented.
- [PR #9300](https://github.com/pingdotgg/t3code/pull/9300) moves exception policy into configuration, updates stale per-file ceilings, and enables unused-disable reporting in the command CI actually runs. A rule with an obsolete exception budget can silently allow new regressions.

**Apply:** start with the [runnable built-in-rule example](examples/recurring-rule/README.md). Introduce a custom AST rule only when an existing rule cannot express the failure. Test the forbidden case, legitimate exceptions, and the exact editor/CI entrypoint. Use diagnostics that identify the approved replacement.

### Environment setup must be exercised, not merely documented

The [test-t3-app skill](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/.agents/skills/test-t3-app/SKILL.md) describes per-worktree test state, the dev runner’s actual origin, and pairing/recovery. [PR #5586](https://github.com/pingdotgg/t3code/pull/5586), merged August 7, ties repeated agent setup failures to inherited service-launcher variables and contradictory instructions. The code now removes the misleading variables before starting a development server; the skill and root instructions agree on the intended workflow. Its session counts and timing range are the PR author’s audit, not measurements repeated here.

[`t3.json`](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/t3.json) contains a worktree setup recipe. However, PR #10501 records that this recipe had not been imported for a particular saved project. A checked-in setup recipe was therefore insufficient to prove setup would run. Its `.env` symlinks are repository-specific; use your project’s existing scoped credential mechanism when adapting this pattern.

**Apply:** launch from a fresh worktree, verify the resulting origin and state directory, and test the actual configured entry point the agent will use. Keep the user’s working app and data distinct from the test instance. Record what is configured versus still manual.

### Tool adapters must preserve the intended operation

[PR #9128](https://github.com/pingdotgg/t3code/pull/9128), merged September 2, fixes a skill picker whose output worked differently across providers. The Claude adapter translates the selected skill into the CLI’s native invocation shape and handles user-only/disabled discovery semantics. Inspect [ClaudeSkillDispatch.ts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/apps/server/src/provider/Drivers/ClaudeSkillDispatch.ts) and its neighboring tests. The PR reports behavior tested against a specific Claude Code version; do not treat that parser behavior as a timeless cross-provider standard.

[PR #10501](https://github.com/pingdotgg/t3code/pull/10501), merged September 8, addresses three real consumer failures: enormous snapshot text lost useful locators to truncation, non-object evaluation results broke structured output, and screenshots lacked a saved artifact path. The implementation bounds text, wraps evaluation results, and can save PNGs. Configuration can still be wrong even after the code fix.

[PR #10572](https://github.com/pingdotgg/t3code/pull/10572), also merged September 8, repairs a different ownership problem: a desktop-local recording path was unreadable by a remote agent. [browserRecordingUpload.ts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/apps/web/src/browser/browserRecordingUpload.ts) transfers the finalized file through the existing attachment path; the broker claims it in the agent environment. The PR reports a real transfer with matching hashes. I inspected that code and evidence claim, but did not repeat the transfer.

**Apply:** validate the operation from the consumer’s environment. A skill name appearing in a menu is not invocation proof; a returned local filename is not artifact-delivery proof. Keep useful structured detail and bounded readable output, and expose the resulting file to the intended recipient.

## PR history: changes, dates, and evidence

The inspected T3 snapshot is [`6c583620ff7a`](https://github.com/pingdotgg/t3code/commit/6c583620ff7ad3235b135af7107c0543467eecfa). The latest commit at the end of the video’s publication day is [`23c18fda7a96`](https://github.com/pingdotgg/t3code/commit/23c18fda7a969634a30888e36b2da45f6d66a83b); this is a day-level cutoff, not the exact recording time.

| PR | Merged | Useful finding |
| --- | --- | --- |
| [#137](https://github.com/pingdotgg/t3code/pull/137) | March 2 | Corrects root instructions from Zod to the actual Effect Schema contract layer. Documentation can send agents toward the wrong implementation. |
| [#1032](https://github.com/pingdotgg/t3code/pull/1032) | March 17 | Sends selected terminal output into chat, with screenshot and video attachment links in the PR. This is observed evidence packaging, not the later upload skill’s source. |
| [#2928](https://github.com/pingdotgg/t3code/pull/2928) | June 4 | Prebundles a dependency that was reloading browser-test sessions mid-run. Fixes the environment-induced failure rather than increasing retries. |
| [#5586](https://github.com/pingdotgg/t3code/pull/5586) | August 7 | Replaces recurring setup workarounds with environment sanitization and consistent instructions. |
| [#7209](https://github.com/pingdotgg/t3code/pull/7209) | August 16 | Converts repeated tooltip regressions into a lint error and fixes existing occurrences. |
| [#8250](https://github.com/pingdotgg/t3code/pull/8250) | August 26 | Removes a duplicate web build and unnecessary release-job dependencies; the author reports an audit of 60 release runs. The measured saving is not independently reproduced here. |
| [#8243](https://github.com/pingdotgg/t3code/pull/8243) | August 27 | Makes authorized preview builds downloadable on headless devices; separates PR-code execution from the privileged artifact-publish job. |
| [#9128](https://github.com/pingdotgg/t3code/pull/9128) | September 2 | Verifies provider-native skill dispatch rather than assuming a UI mention invokes the requested skill. |
| [#9300](https://github.com/pingdotgg/t3code/pull/9300) | September 3 | Repairs drifting lint exemptions and checks the CI entrypoint. |
| [#10572](https://github.com/pingdotgg/t3code/pull/10572), [#10501](https://github.com/pingdotgg/t3code/pull/10501) | September 8 | Makes browser evidence readable and accessible to the agent that needs it. |

Four custom rules already appear in the [July 21 plugin](https://github.com/pingdotgg/t3code/blob/23c18fda7a969634a30888e36b2da45f6d66a83b/oxlint-plugin-t3code/index.ts); the tooltip and mobile-theme rules are later additions. Both the July 21 and September 9 web package configurations select a `unit` test project. PR #2928 proves historical browser-test work; it does **not** establish that a dedicated browser-test job is still wired into today’s CI. The current application-testing skill describes integrated browser checks. The specific Twitch two-account sentinel described in the video was not located in these inspected public sources.

## Melee: the verification command you linked

Your [comparison](https://github.com/doldecomp/melee/compare/master...t3dotgg:melee4mac:master) contains **123 commits and 207 changed files** at inspection. The fork is 123 commits ahead and 12 behind the compared upstream; its common ancestor is `05a1394faea2aac458e4bdd030621d8a5631ae62`. These are moving-branch counts; the inspected fork head is [`a276aeb70f98`](https://github.com/t3dotgg/melee4mac/commit/a276aeb70f9879204d891d967f1c9442523568e1).

The [September 8 commit you linked](https://github.com/doldecomp/melee/commit/035d9711623a32fbe891cffdcf44a91a550c1947) adds a 75-line verifier and nine focused tests. It explicitly builds the final executable and report, runs the existing diff target, checks that required artifacts exist, and compares the output to the expected manifest hash. Failed commands stop success reporting even if an old artifact exists. This makes a precise outcome callable through one command.

The [follow-up commit](https://github.com/t3dotgg/melee4mac/commit/74e73873038b821bbc46b0a18434e6b7cb556c0e) closes another false-success path: a matching executable can still link original objects where source work is incomplete. Its `verify_report` requires matching and complete code/data counts, matching functions, complete units, positive totals, and per-unit completion. The manifest is the fixed reference for this project, not something an agent should rewrite to obtain green.

The commit being accessible under `doldecomp/melee` does not establish an upstream merge. It is present in the fork comparison. The visible integration record is [fork PR #1](https://github.com/t3dotgg/melee4mac/pull/1), which combines the verifier with matching-preserving cleanup and explicit documentation of what public CI cannot check.

### What I executed locally

- The original verifier’s **9 tests passed**.
- The inspected current verifier’s **15 tests passed**.
- A [synthetic comparison](evidence/melee-verifier-comparison.json) gave both implementations a matching fixture hash and successful mocked build/diff commands, with incomplete source measures. The initial verifier accepted it; the current verifier rejected it before printing success.

These runs validate the Python verifier behavior. Build commands were mocked and the fixture bytes were synthetic. They do not certify a real Melee executable, native application, gameplay, or performance. [Guide 09](guides/09-verification-contracts.md) turns this into a general method for defining a completion contract.

## Melee’s implementation path and supporting tools

The [native runtime overview](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/native/macos/README.md) and [build script](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/native/macos/build.py) show the actual path: produce and verify the GameCube executable, translate it and the disc loader into C with pinned recompilation dependencies, then compile ARM64 code against a Dolphin-derived compatibility runtime. This is static recompilation, not simply compiling the decompiled game C against native macOS APIs. Original memory-layout assumptions remain in guest memory. Strict native mode rejects uncovered CPU execution rather than silently falling back to a PowerPC interpreter or JIT.

Keep the invariants separate. A matching input GameCube executable does not prove that later rendering hooks preserve every native behavior. [PR #12](https://github.com/t3dotgg/melee4mac/pull/12) adds predicted rendering between 60 Hz simulation updates and optional textures; its author explicitly leaves physical 120 Hz display validation open. [PR #13](https://github.com/t3dotgg/melee4mac/pull/13) is **open** at inspection, and its lighting changes are not part of the inspected master snapshot. Its screenshot pairs and stated test conditions are evidence to assess, not proof we ran the game.

The earlier PRs provide a useful sequence of infrastructure improvements:

| Fork PR | Mechanism worth studying | Limit recorded in the evidence |
| --- | --- | --- |
| [#3](https://github.com/t3dotgg/melee4mac/pull/3) | Automates the tested Mac compiler wrapper; retains explicit override; documents queue and allocator ownership. | The PR’s matching build is a reported local result. |
| [#5](https://github.com/t3dotgg/melee4mac/pull/5) | Repairs symbol parsing and strong/weak provider selection using real build objects. | A dependency graph is not a call graph or final linker resolution. |
| [#6](https://github.com/t3dotgg/melee4mac/pull/6) | Makes context generation fail on unreadable input and preserve previous output on failure. | Textual include expansion does not evaluate conditional compilation. |
| [#7](https://github.com/t3dotgg/melee4mac/pull/7) | Corrects dependency direction and matching-leaf selection, with small graph fixtures. | Analysis tooling can be confidently wrong until checked against concrete cases. |
| [#10](https://github.com/t3dotgg/melee4mac/pull/10) | Integrates an explicit upstream revision and verifies the combined tree. | Earlier passing batches are not evidence for a new integration. |
| [#11](https://github.com/t3dotgg/melee4mac/pull/11) | Adds the pinned native pipeline, separate saves, strict execution checks, and scenario-specific measurements. | Timings apply to the stated machine and workload; software controller tests do not verify Bluetooth hardware. |
| [#12](https://github.com/t3dotgg/melee4mac/pull/12) | Adds extraction, texture-quality checks, rendering changes, and explicit measurement limits. | Public code excludes generated private artwork; a physical 120 Hz display still needs checking. |

GitHub’s check-run API reports successful Linux/macOS/Windows tool tests, style checks, and a native-library build on the inspected heads of Melee PRs #12 and #13. Those public checks have no original game data and cannot establish a matching game build. For T3 #7209 and #10501, the relevant Check/Test runs succeeded; several preview jobs were skipped. Skipped preview jobs are not preview-validation evidence. Compact check snapshots were kept in the research workspace and are summarized here rather than reproduced.

## What to take away

1. **A completion contract:** name the actual output, the source/input completeness requirement, and the consumer-visible outcome. Reject a plausible proxy result when it leaves the requirement unproved.
2. **Small executable feedback:** encode recurring mistakes in existing lint/type/test/build boundaries, then prove both rejection and legitimate success.
3. **Explicit ownership:** isolate agent writes and test state; put provider quirks behind adapters; verify remote artifact accessibility where it matters.
4. **Calibrated knowledge:** keep durable decisions and surprising constraints close to their relevant code. Use source maps as entry points and generated dependency data as evidence with known limits.
5. **Evidence with provenance:** distinguish local execution, remote CI, PR-author reports, and untested hardware. Keep source and native-output invariants separate.

These extend the four companion skills and the [implementation guides](README.md). They do not justify a mandatory event-sourcing rewrite, copying Theo’s stack, or adopting another repository’s authority rules. Choose the smallest mechanism that fixes a recurring failure in your actual system.
