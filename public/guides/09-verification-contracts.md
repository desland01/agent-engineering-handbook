# 09: Verification contracts

How-to: make "done" mean a checked artifact, not a finished command. Adapted from
`tools/verify.py` and `tools/tests/test_verify.py` in the Melee for Mac snapshot
(`t3dotgg/melee4mac`, head `a276aeb70f9879204d891d967f1c9442523568e1`); the pattern generalizes, the specific
hashes and unit model do not. Companion guide: [10-codebase-navigation-and-tooling.md](10-codebase-navigation-and-tooling.md).

## The idea

A build command exiting 0 reports success for the selected target. A verification contract states
what artifact must exist, what property it must have, and which false-green paths the
check rejects — then a single script enforces all of it. Melee's contract has three
layers: build the exact target by name, require per-unit completeness in a report, and
re-hash the final artifact against a recorded expected value ([tools/verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py)).
Choose the properties your pipeline actually needs; exact binary identity is specific to a matching build.

## Steps

1. **Name the accepted artifact.** Write down the file (or set) that counts as done —
   an encoded video, a transcript, a report. Melee points Ninja at `main.dol` and
   `report.json` explicitly because the default target "can report progress without
   linking" it ([tools/verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py)). Your equivalent: invoke the tool so the real
   output is produced, not a progress or plan mode.
2. **Record the expected identity before you build.** Use a known reference hash only when exact identity is required. Otherwise derive the required duration, stream count, rows or semantic behavior from the requested change; a legitimate new output need not equal old bytes. Melee keeps one
   40-hex SHA-1 per artifact in a manifest and validates the manifest itself — exactly
   one valid entry, or stop before building ([tools/verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py)). Storing the
   expectation in a file, not in your memory of the last run, makes the check repeatable.
3. **Check intermediate completeness, not just the endpoint.** The linker can substitute
   originals for incomplete units, so a matching final hash alone is insufficient
   ([tools/verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py)); the report check requires every unit to be complete
   (in the linked source). Your equivalent: every segment of a stitched video present, every
   expected chapter in a transcript, no placeholder rows.
4. **Verify after building, in this order.** Build → confirm artifacts exist on disk →
   check the report → recompute the hash. Tests in the snapshot pin the order: a build
   failure stops before the diff step, and a diff failure does not pass because the hash
   matched ([tools/tests/test_verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_verify.py)).
5. **Turn each relevant false-success path into a test.** The Melee suite has one test
   per deception: perfect progress with a wrong hash, a matching hash with an incomplete
   source, missing artifacts while the build "succeeded", invalid counts coerced from
   bad types, an empty project passing trivially ([tools/tests/test_verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_verify.py)).
   Write the smallest test that would have caught each one.
6. **Fail with a reason and a nonzero exit.** The CLI catches build, OS, and validation
   errors and prints one line starting "Verification failed:" without a traceback
   ([tools/verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py), tested at [tools/tests/test_verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_verify.py)). An agent
   or a human reading the log should learn what to fix, not that something failed.
7. **Separate partial-environment checks from full acceptance.** Melee's CI runs tool
   tests and a library build but explicitly cannot perform the game-data matching check
   ([.github/workflows/build.yml](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/.github/workflows/build.yml)), and its rules forbid reporting CI as a
   matching build ([AGENTS.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/AGENTS.md)). Name what your sandboxed or partial run actually
   proved when you report it.

## Acceptance evidence

- The contract script exits 0 on the good case and nonzero, with the specific message,
  for each false-green case you enumerated.
- A test run (or a recorded run in the project's log) shows the failure-path tests
  passing. A passing check establishes only what it measured — say which layer it
  covered.

## Reuse and troubleshooting

Reuse existing tooling before writing new: project test runners (`unittest`, `pytest`),
the build system's explicit-target mode, `shasum`/`sha256sum`. If a check keeps passing
when it should fail, corrupt a disposable fixture deliberately and confirm the check notices —
that is `test_perfect_progress_does_not_hide_hash_mismatch` ([tools/tests/test_verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_verify.py))
as a manual habit. If you cannot check a property in the current environment, report it
as unverified rather than widening the claim.
