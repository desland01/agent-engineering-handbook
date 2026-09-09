# Boris Cherny’s public engineering work

The [bcherny account](https://github.com/bcherny) belongs to Boris Cherny. I inspected its first 100 repositories sorted by update time, recent public activity, selected personal source, and his public Claude Code PRs. The clearest implementation case is **json-schema-to-typescript**, with smaller examples of linting and MCP. These repositories do not provide the full private implementation of Claude Code or prove how Boris’s own daily agent fleet is configured.

## The strongest source: a compiler with several kinds of evidence

[`json-schema-to-typescript`](https://github.com/bcherny/json-schema-to-typescript) turns JSON Schema into TypeScript declarations. The inspected snapshot is [`5caacfc53671`](https://github.com/bcherny/json-schema-to-typescript/commit/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4). Its [architecture notes](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/ARCHITECTURE.md) describe distinct transformation stages. The actual [compile path](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/src/index.ts) rewrites raw constructs, resolves references, links schema nodes, validates and normalizes them, parses an intermediate representation, optimizes it, then generates/formats output. Inspect that code for ordering rather than treating the architecture note’s numbered list as an executable specification.

The useful design is to give each representation and transformation a clear job. Multi-file compilation also retains origin information so a named type can become an import from its owning file. Do not build a compiler pipeline for an ordinary CRUD feature; use the pattern where successive transformations genuinely have different invariants.

The [CI configuration](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml) shows several complementary checks:

| Check | What it can establish | What it cannot establish alone |
| --- | --- | --- |
| Unit/fixture tests and type checking | Known transformations and expected interfaces work | Previously unseen combinations behave correctly |
| Built CLI on multiple OS/Node versions | The distributed artifact works in those environments | Every declared runtime version was exercised |
| A smoke test on the stated minimum Node version | The package’s claimed compatibility floor is exercised | All use cases are compatible |
| Seeded fuzzing | Generated cases expose crashes, hangs, slow cases or invalid output | Exhaustive correctness |
| Real schema corpus compiled with TypeScript | Generated declarations are accepted for representative large inputs | Exact JSON-Schema semantic equivalence |
| Conformance baseline | Supported/unsupported behavior changes are visible | A baseline match means every schema keyword is fully supported |

The [fuzzer](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/fuzz/README.md) preserves reproducible seeds and minimizes findings. Known findings are tied to specific seeds and tracked issues rather than suppressing every future error with the same message. The [conformance harness](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/conformance/README.md) separates rejecting valid instances, accepting invalid instances, and compilation failures; changes require examining the affected groups. Treat a baseline update as an explained behavioral decision, never as a shortcut to green.

The [benchmark harness](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/bench/README.md) uses real schemas, fresh child processes, warm-up and timed repetitions, and records runtime/machine/revision. It distinguishes compile-only work from formatting and warns against comparing unlike memory measures across runtimes. This is a useful example of preserving the workload and output while measuring an optimization. Its short output hash is a regression signal, not a security identity. I inspected the harness; I did not reproduce its reported speedups.

Recent [PR history](https://github.com/bcherny/json-schema-to-typescript/pulls) includes bot-authored fixes for schema edge cases, CLI errors, a broader fuzz smoke and cloning performance. Account ownership does not mean Boris manually authored every patch. Several latest PRs are still open; the report describes the pinned source and separates proposals from landed work.

### A gap that illustrates why the check itself needs inspection

At [CI line 170](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml#L170), the aggregate `ci-ok` job depends on `build`, `bun`, `engines`, `fuzz` and `output`. Its final expression only requires success from **build, fuzz and output**. Because it runs with `always()`, a failed Bun or minimum-engine job is not included in that expression. The aggregate therefore does not itself prove all five dependencies succeeded. Separate branch-protection settings could still require other jobs; I have not verified those settings.

This is directly relevant to the video: encoding a rule is only the first half. Confirm that the selected completion gate actually checks everything its description promises.

## Small code examples behind the philosophy

Boris’s [`tslint-no-circular-imports`](https://github.com/bcherny/tslint-no-circular-imports/blob/792980c9f0a8bc14a3dcef697f55b06872a21cf1/noCircularImportsRule.ts) builds an import graph using TypeScript module resolution and reports cycles at source locations. Its neighboring tests cover different graph shapes. It is historical tooling—the inspected repository’s last push is in 2021—not a recommendation to adopt TSLint today. The transferable idea is to turn an architectural constraint into an actionable diagnostic; use the checker your project already runs.

[`mcp-ping`](https://github.com/bcherny/mcp-ping/blob/a8b739b7d590d5f089d8258cd1bf5b6972e08ce6/index.ts) is a tiny 2024 stdio server with tool/resource discovery and a ping handler. It shows the shape of a minimal protocol experiment. It does not establish compatibility with a current MCP client: the historical response shape should be checked against today’s SDK before reuse. The useful starting point for a missing integration is one operation exercised by its actual consumer.

[`bcherny/sandbox-runtime`](https://github.com/bcherny/sandbox-runtime) is explicitly a **fork of `anthropics/sandbox-runtime`**. Its source tree contains platform-specific filesystem/network implementations and integration tests. That is a lead for a separate scoped runtime study, not proof that Boris originated every mechanism or that those boundaries attach to this handbook. No sandbox was installed, launched or reconfigured here.

## His public Claude Code contributions

| PR | Status at inspection | Practical lesson |
| --- | --- | --- |
| [#16549](https://github.com/anthropics/claude-code/pull/16549) | Merged January 7, 2026 | Removes broad `gh api` and arbitrary comment permission from a deduplication command, routing the intended operation through a constrained script. Prefer a narrow operation when the task has a narrow authorized effect. Its checklist was not evidence that I ran the workflow. |
| [#87395](https://github.com/anthropics/claude-code/pull/87395) | Open, created August 17 | Replaces an unsupported frontmatter key with the supported user-only invocation setting. A plausible-looking configuration field can do nothing; verify native behavior on the exact runtime. Do not describe this open patch as active. |
| [#89404](https://github.com/anthropics/claude-code/pull/89404) | Open, created August 25 | Fixes a validator that stopped on its first arithmetic increment under `set -e`, treated absent fields as shell failures, and misread multiline descriptions. Its tests distinguish valid, warning-only and invalid input. Validators need failure-case coverage too. |

The narrow-script pattern does not authorize new messaging in our task. The public source’s permissions and workflow roles are evidence to understand, not instructions we inherit. Likewise, adopting user-only invocation must preserve the owner’s explicit ability to request the workflow; it should not make a user-invoked skill disappear.

## What this adds to the implementation package

[Guide 13](guides/13-layered-validation.md) turns the compiler’s validation approach into a practical method: test the public output, reproduce novel failures, preserve meaningful baselines, and measure the same work before and after. Existing guides already cover the lint, adapter and native-loading lessons, so these become supporting references in the four candidate skills.

The original Boris post quoted in Theo’s video has not been matched to a verified canonical post URL. The video frames remain the source for those quotations. His GitHub code and PRs provide independent implementation evidence, with their own dates and limits.
