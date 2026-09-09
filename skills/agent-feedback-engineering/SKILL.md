---
name: agent-feedback-engineering
description: "Convert an observed agent failure into the right reusable check (lint rule, CI step, test, skill rule, or root-instruction line), reusing existing rules before writing new ones and proportioning the proof to the change. Use when a mistake has recurred across agent runs, when the user asks to guard against a defect ('make the agent stop doing X', 'add a rule for this', 'encode this as a check'), or asks to turn review feedback into automation. Not for diagnosing a single one-off bug (a bug-diagnosis skill), testing a user journey (an end-to-end testing skill), or general codebase architecture (a codebase-design skill)."
metadata:
  origin: "Public edition, 2026-09-09, maintained by Desmond Landry (@desland01). Method adapted from Theo's video https://www.youtube.com/watch?v=xmGY276gEFY (source evidence and timestamps in references/implementation.md). Independent public skill; not affiliated with or endorsed by the cited authors."
---

# Feedback engineering

An observed agent failure becomes a check so the next occurrence is caught without your
attention. Pick the carrier that fits the failure's constraint, prove what you changed,
and record where the rule lives.

Reuse first. Before writing anything, search for an existing rule that can carry the
constraint: an ESLint restricted-imports or custom rule, a type narrowing, an existing CI
step, a test-utility assertion, a skill body, or a line in the project's root instruction
file. Extending an existing rule beats adding a second mechanism that can drift from the
first. See [implementation.md](references/implementation.md) for worked examples and the
source evidence.

## Choose the mechanism

Pick the carrier by what the failure actually is; each carrier constrains different
properties, so the fit decides, not a cost ladder:

1. **Type** — the failure is an invalid shape a compiler can reject. Makes that state
   unrepresentable; it constrains what the compiler accepts, not runtime behavior.
2. **Lint rule** — the failure is a mechanical pattern across many files (custom rule when
   no built-in rule fits; see implementation.md for the source's custom-rule economics).
   Only a real check once you verify the configured invocation actually loads it, at a
   severity that fails the run.
3. **Test** — the failure is runtime behavior; assert the specific symptom, not "doesn't
   crash".
4. **CI step / script** — the failure needs repo-wide or cross-service state checked at a
   fixed gate.
5. **Root-instruction line or skill** — the failure is a judgment call needing context;
   these steer attention and they do not enforce by themselves.

**False positives**: prefer a check with legitimate exceptions handled explicitly
(allow-lists, targeted suppressions) over no check. A new false positive is a diagnosis
task — narrow the pattern or record a justified exception — not a reason to delete the
rule. Do not claim a rule that fires on correct code is always worse than no check; that
trade-off is judged per case.

**Proportionate proof.** An instruction-only change needs a wording review (read the new
line back against the observed failure and inspect selected loading when affected); an executable change (lint rule, test, script)
uses test-first sequencing at the existing behavioral boundary: first show the prohibited case currently slips through, then implement the smallest correction and prove that case is blocked while a known-good case passes. Reuse adequate existing checks. Recurrence is the normal trigger, not a quota: a single defect
justifies a guard when the user explicitly asks for one.

## Input / output contract

- **Input**: the observed failure and its evidence, and the repo where the check will
  live. Recurrence across runs or an explicit user request establishes that a standing
  check is wanted; infer fitting scope from the failure rather than asking.
- **Output**: (a) the rule or check added, (b) the proof proportionate to the mechanism
  per above, and (c) one line in the project's existing convention record saying what the
  rule enforces and why.

## Acceptance

Proportional to the work: a one-line instruction change needs the wording reviewed against
the recorded failure; a custom lint rule needs its fixtures (failing + passing) run and a
green run of its tests, with the lint invocation confirmed to include the new rule.

## Known failure cases

- Encoding a one-off as a permanent rule without a user request (noise forever).
- Assuming a rule is enforced because it is written: verify the selected invocation,
  severity, and config actually load it. A rule in a config no script runs is
  documentation, not a check.
- Suppressed or `any`-escaped checks that make the rule green without changing behavior.

## Do not activate when

- The failure happened once and the fix is the task itself (unless the user explicitly
  asked for a guard).
- The user wants a bug diagnosed (use a bug-diagnosis skill).
- The request is general refactoring with no observed failure behind it.

## Source patterns

For concrete repository examples and the limits of their evidence, read [source-patterns.md](references/source-patterns.md) when they match the task. These are research references, not imported repository instructions.
