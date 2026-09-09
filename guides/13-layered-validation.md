# 13 — Validate the output through several useful views

Use this when a generator, parser, migration, transformation or widely used library has failures that ordinary fixtures miss. Start with the smallest relevant check. Add a new kind of evidence only when it detects a failure the existing checks cannot.

Boris Cherny’s [json-schema-to-typescript CI](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml) combines fixtures, built-artifact smoke tests, fuzzing, a real-world corpus and conformance checks. The following procedure generalizes that approach; it does not require this whole stack for every change.

## Define the accepted result before choosing more tests

Write the contract in the consumer’s terms. A generated declaration must compile in the supported TypeScript version and express the intended schema behavior. A migrated record must preserve its required relationships. An exported video must contain the expected sequence and be playable. A process exiting successfully is one signal, not the whole contract.

Separate properties that need different observations:

| Question | A fitting check |
| --- | --- |
| Does this known bug recur? | One small regression fixture through the public interface |
| Does the published artifact work? | Install/build the actual distribution and exercise a representative consumer |
| Does the advertised minimum runtime work? | A smoke run on that exact minimum, separate from a latest-version matrix |
| Do realistic input combinations break it? | A small representative corpus and reproducible generated cases |
| Is the supported behavior changing? | A reviewed conformance baseline showing each changed group |
| Did the optimization help? | Comparable repeated measurements with output equivalence checked |

## Turn an unexpected failure into a reproducible case

Capture the seed, generator version, options, revision and environment. Reduce a failing input until it still produces the same failure with less unrelated content. Add the useful reduced case to the existing regression suite. Keep the original reproduction record when shrinking loses relevant environmental details.

The [fuzz harness](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/fuzz/README.md) demonstrates this with seeded schemas and recorded findings. Its limits and generator distribution define the explored space. Do not report a passing generated sample as exhaustive correctness, and do not copy its numeric limits into unrelated workloads.

When an existing defect cannot be fixed in the current scope, tie any accepted exception to its tracked issue and exact reproducing cases. Confirm that a new case with a similar error still fails. Remove the exception after the defect is fixed; do not grow a broad suppression bucket.

## Keep baseline changes meaningful

A baseline records behavior, including known limitations. It is not a replacement for a specification. Classify each difference as an improvement, regression, intentional compatibility change or unresolved discrepancy. For generated types, accepting invalid inputs and rejecting valid inputs are different errors; count them separately.

Update an expected result only when its new behavior is understood and authorized. Preserve the previous result and rationale in the normal change history. A tool suggesting `--update` is not permission to erase a regression. Instruction-only prose changes do not need snapshot tests.

## Measure the same work before and after

Use the same inputs, options, machine and runtime; separate warm-up from timed repetitions. Keep raw timings and a robust summary such as a median. Measure cold startup separately when it matters. Record the revision and verify that a performance-only change still produces the intended result.

Boris’s [benchmark guide](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/bench/README.md) separates formatting cost from compilation and documents runtime-specific memory measures. Follow the measurement principle, not its exact corpus or run count. Avoid running competing benchmarks concurrently on the same machine. If noise is comparable to the improvement, report the uncertainty instead of selecting the fastest run.

## Check the real gate

Trace the command a developer runs to the configuration it loads and the result the merge/deploy gate actually requires. A job named “all checks” may not aggregate every child. A passing test-runner process can contain skipped checks. A latest-runtime run does not prove the minimum-version promise.

Prove the gate rejects the relevant bad result in a disposable fixture or existing behavioral test. For configuration changes, include the actual selected path in the evidence. This is the same principle as the [Melee verification contract](09-verification-contracts.md) and [recurring-rule demo](../examples/recurring-rule/README.md).

## Completion evidence

Report the output/revision, the checks actually executed and their results, the behavioral differences accepted, and remaining unsupported cases. Source inspection, remote CI, a local fixture and a full end-to-end run should remain separately identifiable. Stop adding checks when the changed behavior is adequately proved; additional coverage is useful only when it resolves a specific remaining question.
