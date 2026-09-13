---
name: agent-output-verification
description: "Judge whether an agent run's actual output satisfies what was asked — the real artifact exists, intermediate stages are complete, and the consumer-visible outcome holds — using properties derived from the request, not from a command's exit code or a matching old hash. Use when a run reports success but the result may be incomplete, when asked to define or check 'what counts as done' for a build/generation/export task, or when a success signal looks too good (perfect progress, green command, matching digest). Not for turning a failure into a reusable rule (agent-feedback-engineering), resuming interrupted or partially published work (agent-artifact-recovery), setting up the environment the output is produced in (agent-ready-workspaces), or testing a product user journey end to end (an end-to-end testing skill)."
metadata:
  origin: "Public edition, 2026-09-12, maintained by Desmond Landry (@desland01). Method derived from public source inspection recorded in the Agent Engineering Handbook: the Melee for Mac verifier and its tests (t3dotgg/melee4mac, pinned commits), the json-schema-to-typescript CI configuration (bcherny/json-schema-to-typescript, pinned commit), and the source video https://www.youtube.com/watch?v=xmGY276gEFY. Pinned links and evidence limits in references/source-patterns.md. Independent public skill; not affiliated with or endorsed by the cited authors."
---

# Output verification

An exit code proves only what the command or test actually checked — often
just that it ran without error, not that the work is done. Before accepting
an agent's result, decide what artifact counts as done, then check the
artifact itself — not the success message. That check need not be new: an
existing check that already covers this output is enough, as long as the
output it accepted is unchanged since it ran; the failure to avoid is reusing
a green result for output that has since changed.

## Define the accepted output first

Write down, before checking anything:

1. **The artifact** — the file or set of files that counts as done. Invoke the
   tool so the real output is produced, not a progress, plan or dry-run mode. In
   the source example, the build tool is pointed at the final executable and
   report by name because its default target can report progress without
   linking ([guide 09](https://github.com/desland01/agent-engineering-handbook/blob/main/guides/09-verification-contracts.md)).
2. **The expected properties** — derived from the request: required duration,
   row count, sections present, a semantic behavior. Use a reference hash only
   when exact identity is genuinely required. **A legitimate new output need
   not equal the old bytes**: if the request was a change, expect changed
   output, and check the property the change implies instead of demanding a
   historical hash match.
3. **The false-success paths** — the ways this task can look done while it is
   not. Each one becomes a check — the smallest one that would catch it, reusing
   existing tests where they already cover the path rather than building a new
   suite for every accepted result.

## Check in order: endpoint, intermediates, outcome

1. **The artifact exists on disk.** A successful build log is not a file. Check
   the path the consumer will read.
2. **Intermediate completeness.** A matching final result can hide incomplete
   work: in the source case the linker substitutes original objects for
   incomplete source units, so the final hash alone matched while the work was
   unfinished. Your equivalents: every segment of a stitched video present,
   every expected chapter in a transcript, no placeholder rows, every unit
   reported complete.
3. **The consumer-visible outcome.** The artifact does what the requester
   wanted: it opens, parses, plays, renders, or feeds the next stage. A
   property the compiler or builder cannot see needs its own check.

## Turn each false-success path into a test

The source verifier's test suite has one test per deception: perfect progress
with a wrong hash, a matching hash with incomplete sources, missing artifacts
while the build "succeeded", invalid counts coerced from bad types, an empty
project passing trivially. Write the smallest check that would have caught each
path you enumerated, and confirm it rejects the bad case while a known-good
case passes. Corrupt a disposable fixture deliberately and confirm the check
notices.

**Fail with a reason and a nonzero exit.** One line naming what is wrong beats
a traceback: whoever or whatever reads the log should learn what to fix.

## Name what the check did not cover

Separate partial-environment checks from full acceptance, and report the layer
you actually exercised. The source project's CI runs its tool tests but
explicitly cannot perform the final matching check, and its instructions forbid
calling CI a matching build. An aggregate gate is not proof either: in the
inspected compiler CI, the aggregate success job's expression omitted two of
its declared dependencies, so a failed minimum-runtime job did not fail the
aggregate. Trace the actual gate — the command, the configuration it loads,
the expression that decides — before trusting its name.

See [implementation.md](references/implementation.md) for worked applications
and [source-patterns.md](references/source-patterns.md) for the pinned code and
the limits of its evidence.

## Input / output contract

- **Input**: the requested change or deliverable, access to the produced
  output and the command that produced it, and any recorded expectation
  (manifest, recipe, prior version).
- **Output**: an acceptance decision with the properties actually checked, the
  rejected false-success paths with evidence, and an explicit list of what
  remains unverified in this environment.

## Acceptance

The verdict is proportional to the risk: a generated report may need existence
and one semantic property; a shipped binary may need existence, completeness of
its intermediates, and identity against a recorded reference. Say which layer
each check covered. A passing check establishes only what it measured.

## Known failure cases

- Treating exit code zero, or "the command finished", as completion — or
  reusing a prior green check for output that changed after it ran.
- Demanding an old hash match for legitimately changed output — and the
  opposite error: accepting a hash match as proof of completeness.
- Checking only the endpoint while an intermediate stage substituted or
  skipped work.
- Trusting an aggregate gate name ("all checks", `ci-ok`) without reading its
  expression, or counting skipped jobs as passing evidence.
- Rewriting the recorded expectation to obtain green instead of fixing the
  output.

## Do not activate when

- The task is encoding a recurring failure into a standing rule
  (agent-feedback-engineering owns that).
- The work is interrupted and the goal is resuming without repeating completed
  stages (agent-artifact-recovery).
- The gap is setup, previews or evidence delivery rather than judging a result
  (agent-ready-workspaces).
- The request is a user-journey test suite for the product rather than
  acceptance of one run's output.
- The gap is missing knowledge or steering rather than an unproven result
  (agent-context-calibration), or a missing capability needs an interface
  built for it (agent-tool-adapters).
