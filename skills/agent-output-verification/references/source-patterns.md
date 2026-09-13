# Repository examples: verification contracts and their evidence limits

All links below point at pinned commits captured during the original
investigation recorded in the handbook's inspection reports. Unless a row says
otherwise, the source was **inspected and read, not executed** by this
edition.

- **Melee for Mac verifier** (`t3dotgg/melee4mac`, head `a276aeb70f9879204d891d967f1c9442523568e1`):
  [tools/verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py)
  builds the named final executable and report, requires every source unit
  complete in the report, and re-hashes the artifact against a recorded
  manifest. Its comment states the reason: the linker can use original objects
  for incomplete source units, so the final hash alone cannot prove the work
  was finished. Its
  [test suite](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_verify.py)
  has one test per false-success path, including
  `test_perfect_progress_does_not_hide_hash_mismatch` and
  `test_original_object_fallback_does_not_hide_incomplete_source`.
  The earlier verifier commit
  ([035d9711623a32fbe891cffdcf44a91a550c1947](https://github.com/doldecomp/melee/commit/035d9711623a32fbe891cffdcf44a91a550c1947))
  checked build/diff success and a reference hash but not source completeness;
  the follow-up
  ([74e73873038b821bbc46b0a18434e6b7cb556c0e](https://github.com/t3dotgg/melee4mac/commit/74e73873038b821bbc46b0a18434e6b7cb556c0e))
  closed that gap. **Executed evidence, and its exact scope**: the original
  investigation ran both verifiers' test suites locally (9 and 15 tests
  passing) and a synthetic comparison — mocked build/diff subprocesses,
  synthetic bytes, no Nintendo data and no real game build — in which the
  initial verifier accepted an incomplete-source fixture and the current
  verifier rejected it. That run validates the Python verifier behavior only;
  it does not certify a real Melee executable, gameplay or performance. The
  commit is visible in the fork comparison with the upstream repository; that
  visibility does not establish an upstream merge, and the visible integration
  record is fork [PR #1](https://github.com/t3dotgg/melee4mac/pull/1).
- **Melee CI limits**: at the same pinned head,
  [.github/workflows/build.yml](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/.github/workflows/build.yml)
  runs tool tests and a library build and explicitly cannot perform the
  game-data matching check, and
  [AGENTS.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/AGENTS.md)
  forbids reporting CI as a matching build. Inspected source, not executed.
- **Aggregate gates can undercount** (`bcherny/json-schema-to-typescript`,
  commit `5caacfc53671f9c891bb4e2a78bccc6190ed3ef4`): the
  [CI workflow](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml)
  declares `ci-ok` as needing `build`, `bun`, `engines`, `fuzz` and `output`,
  but its final expression requires success only from `build`, `fuzz` and
  `output` (at the pinned line 170), and it runs with `always()`, so a failed
  Bun or minimum-engine job does not fail the aggregate. Branch-protection
  settings outside the repository were not verified. Inspected, not executed;
  the project's fuzz, conformance and benchmark documentation
  ([test/fuzz/README.md](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/fuzz/README.md),
  [test/conformance/README.md](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/conformance/README.md))
  was read for its layered-check design, and its compiler suite was not run.
- **What each identifier proves**: Course Video Manager's
  [ADR 0027](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0027-byte-hash-decides-the-send.md)
  records that a recipe hash names what a renderer was told to do while only
  the digest of the produced bytes can establish identity of output — the
  boundary between this skill (judge produced output) and recovery
  (reconcile it). See the artifact-recovery skill's source patterns for that
  side.

Choose the invariant appropriate to the product. Exact bytes suit matching
decompilation; they are not a universal acceptance condition for renderers,
refactors or generated code. These sources are cited as research evidence;
nothing from the repositories is bundled here, and the cited authors neither
endorsed nor reviewed this skill.
