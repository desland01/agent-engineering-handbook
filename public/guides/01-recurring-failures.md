# 01 — Convert recurring failures into permanent rules

Practical guide for a developer on a team where the same mistake keeps coming back.
Companion guides: [02](02-critical-journey-tests.md) · [03](03-preview-workspaces.md) ·
[04](04-ci-feedback.md) · [05](05-knowledge-and-instructions.md) · [06](06-tool-adapters.md) ·
[07](07-team-learning.md). Runnable companion: [examples/recurring-rule](../examples/recurring-rule/).

Source: [Theo's video](https://www.youtube.com/watch?v=xmGY276gEFY). Quotes below are from
that video unless marked otherwise. Boris quotes are Boris as quoted by Theo in the video.

## The idea and where it comes from

Boris's post, as Theo reads it at [t=482s](https://www.youtube.com/watch?v=xmGY276gEFY&t=482s):
an agent could fix the same issue every time it appears, but that costs tokens and misses
cases; if the agent instead writes a lint rule, CI step, or routine, the whole class of issue
is automated permanently. Theo agrees at [t=496s](https://www.youtube.com/watch?v=xmGY276gEFY&t=496s)
and adds the economics at
[t=510s](https://www.youtube.com/watch?v=xmGY276gEFY&t=510s): a custom lint rule that needs
400 lines to check something odd was never worth writing by hand, because code review caught
it more cheaply. Now that the code and its tests are cheap to produce, rules like that pay
for themselves. He repeats the example of his file-upload service at
[t=545s](https://www.youtube.com/watch?v=xmGY276gEFY&t=545s).

Theo also names the accounting you should use at
[t=749s](https://www.youtube.com/watch?v=xmGY276gEFY&t=749s): do not let your agents write
your CLAUDE.md or AGENTS.md. This guide is the general form of that: *you* decide what the
rule says; the agent drafts the mechanics. That principle is the user's settled decision here
too, and it is a team practice, not a tool rule.

**Suggested (not demonstrated in the video):** the decision procedure, the cost test, and
the acceptance steps below.

## When to apply

Write a rule when the expected savings justify the rule's cost. A repeated failure is the
normal trigger, but the repeat count is a signal, not a prerequisite: one painful, expensive
occurrence justifies a rule on its own, and an explicit request for a standing guard does
not need to wait for a second occurrence at all.
- The failure is detectable from text or logs, not only from runtime behavior. Runtime
  failures belong in a journey test — see [guide 02](02-critical-journey-tests.md).
- The cost of the rule is less than the cost of the next few manual fixes, including the
  agent's correction cost when it makes the mistake again (tokens, review time, waiting).

For a mistake seen once and cheap to fix, note it and wait for a repeat before spending
rule-building effort — unless the user has explicitly asked for a guard, in which case
record the request and build the smallest one that satisfies it.

## Implementation

1. **Collect the instances.** Find the two or more real occurrences: the files, the import
   path, the call shape. Keep the actual examples; they become your test fixtures.
2. **Pick the mechanism that fits the constraint, preferring what already exists.** Start
   from the constraint's shape, not from a fixed cost ladder: an existing lint rule
   (for example ESLint's built-in
   [`no-restricted-imports`](https://eslint.org/docs/latest/rules/no-restricted-imports)),
   a type or schema constraint, an existing test, lint or CI configuration, or a
   conditional method can each carry it; move up to a custom lint rule
   ([writing guide](https://eslint.org/docs/latest/extend/custom-rules),
   [tutorial](https://eslint.org/docs/latest/extend/custom-rule-tutorial)) only when no
   existing mechanism can express the constraint. Extend an existing rule before adding a
   second mechanism that can drift from the first.
3. **Prove the failure first (red), for executable enforcement.** Run the check with the
   rule absent or disabled and confirm the bad code passes. Keep that output. Without it you
   cannot later show the rule changed anything. This before/after proof applies to
   executable checks; an instruction-only change is verified by wording review against the
   observed failure and, where loading matters, by confirming the instruction is actually
   loaded.
4. **Enable the rule and fix the live violations (green).** The rule's first run will list
   every existing instance. Fix them in the same change that lands the rule, so the rule
   starts green for everyone else.
5. **Ship the rule with adequate fixture coverage**: at least one file that must fail and
   one that must pass. Reuse existing fixtures where they already cover the rule; add a
   pair only when none does. If the project runs checks in CI, cover the rule there so a
   future linter upgrade that changes behavior breaks visibly instead of silently; an
   instruction-only change needs no new fixtures or CI wiring.

## Concrete example

A UI component importing the database client directly keeps reappearing. This repository
contains a working demonstration in
[examples/recurring-rule](../examples/recurring-rule/): ESLint's built-in
`no-restricted-imports` configured for `src/ui/**`, an offending file
(`src/ui/UserCard.js`), an approved file (`src/ui/UserList.js`, importing the API layer),
a red configuration with the rule removed, and `run-demo.sh` which captures the red pass and
the green failure into `evidence/`. It uses no custom rule and needs no network at run time.

## Acceptance

- Red run (rule absent): offending file passes, output preserved.
- Green run (rule enabled): exactly the offending import is reported, by rule name, with a
  message that says what to do instead; approved imports produce no findings.
- CI runs the rule on every PR, and a test fixture pair keeps the rule honest.

## Failure modes and maintenance

- **Rules nobody remembers.** The error message is the documentation. It must name the
  approved path, as the demo's message does.
- **Silent rule rot.** Linter major versions change behavior. The fixture pair turns that
  into a visible CI failure.
- **Rule sprawl.** Review a rule that fires almost never or covers almost nothing on its
  merits: retire it when it is redundant, obsolete, or provably wrong, and keep it when it
  still prevents a real, costly failure. A rare but expensive catch justifies a rule that
  almost never fires; "delete what rarely fires" is not a maintenance rule on its own.
- **Boundary honesty.** Static linting is a guardrail, not a security boundary. It cannot
  prove every bypass impossible (dynamic imports, build-time codegen). Say so in the rule
  message or README rather than overselling it.
- **Escalation order.** If the same class of failure keeps slipping past lint, it may be a
  runtime property — move it to a test, not to a bigger regex.
