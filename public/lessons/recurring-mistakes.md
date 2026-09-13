# Stop fixing the same mistake twice

When you find yourself correcting the same mistake again — another review comment, another
reprimand to your agent, another quick patch — nothing remembers the fix, so the mistake
keeps coming back. The answer, once you observe the recurrence rather than anticipate it,
is to convert that correction into a check that runs on every change and rejects the whole
class of mistake — a lint rule, a CI step, or a small script — instead of fixing the next
occurrence by hand.

## Why the check wins

Boris's argument, as Theo reads it in the video, is an accounting one. Each per-occurrence
fix spends attention (or agent tokens), and each pass can miss a case. A written check can
catch the cases it was configured for on later changes, including ones nobody is watching
for; it is not complete coverage, and the rule itself needs maintenance. The same lesson's
own example shows the boundary: the shipped T3 rule covers the direct `title` attribute but
not custom-component props or spread attributes, so some native tooltips remain outside it.
Theo adds a separate economic point: rules that were never worth hand-writing are now
worth writing, because producing the rule and the tests that prove it has become cheap. A
custom rule that needs around 400 lines to check a very specific oddity used to stay as
manual code review forever. That price has dropped.

These are two adjacent claims, not one. Boris's is about automating a class instead of
instances. Theo's is about when the build is worth the price. Both are arguments, not
measurements.

## A check that actually shipped

This comes from the original T3 Code investigation, not the video. A tooltip regression
kept reappearing in T3 Code. Instead of another round of fixes, the team added a custom
Oxlint rule, [`no-native-title-tooltip`](https://github.com/pingdotgg/t3code/pull/7209),
in PR #7209 (merged August 16, 2026): it visits JSX elements, flags the direct `title`
attribute that caused the regressions, allows the specific accessibility uses that are
legitimate, and fixes the existing occurrences in the same PR. Its valid/invalid fixtures
and successful PR check runs are observable in the public source.

Note the limits the inspection records: the rule is narrow. Custom-component props and
spread attributes are outside it, so it does not prove every possible native tooltip is
prevented. That honesty is part of the pattern — say what the check covers.

## Make the recurring correction automatic

1. Collect the observed instances: file, import, call shape.
2. Prefer an existing mechanism — a built-in lint rule, a type, an existing CI step —
   before writing a custom AST rule. Write a custom rule only when nothing existing can
   express the failure.
3. Prove the failure first: with the rule absent, the bad code passes. Keep that output.
4. Enable the rule, fix the live violations, and ship at least one fixture that must fail
   and one that must pass.
5. Make the error message name the approved alternative. The message is the documentation
   the next reader gets.

The handbook keeps a runnable demonstration of this loop in
[guide 01](../guides/01-recurring-failures.md) and the
[lint example](../examples/recurring-rule/README.md). It uses the built-in
`no-restricted-imports` rule: without the restriction, the unwanted import passes; with
the restriction in place, the unwanted import fails while the permitted import still
passes. The full procedure, including
maintenance and rule retirement, lives there; this lesson is the decision, not the
implementation.

## Check both forbidden and permitted cases

A check that never rejects anything is decoration. Confirm the forbidden case now fails
with a clear message and a permitted case still passes, through the command your project
actually runs. Then check whether the check is wired into CI: a rule run only by hand has
no automatic invocation, so it fires only when someone remembers to run it. Review a new
rule like any other code: an over-broad rule silently blocks good
changes.

## Maintenance still determines whether a rule pays.

The claim that automated fixes now cost less than manual review is an economic argument,
not a measured result, and rule maintenance cost is real. Whether a given rule pays for
itself depends on your codebase.

## Sources

<span id="tip-08-fix-class-loops"></span>
**tip-08-fix-class-loops** — [08:02](https://www.youtube.com/watch?v=xmGY276gEFY&t=482s).
Boris, as quoted by Theo. Move recurring fixes into executable checks. Evidence type:
quoted post via the video; argument, not measurement. A wrong or over-broad check blocks
good changes, so review it.

<span id="tip-19-custom-lint-economics"></span>
**tip-19-custom-lint-economics** — [08:30](https://www.youtube.com/watch?v=xmGY276gEFY&t=510s).
Theo. Custom lint rules became economical because the code and its verifying tests are
cheap to produce. Evidence type: Theo's opinion; the ~400-line figure is Theo's example.

Repository evidence: [T3 Code PR #7209](https://github.com/pingdotgg/t3code/pull/7209) and
the [plugin index](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/oxlint-plugin-t3code/index.ts),
from the original T3 investigation. Method details:
[guide 01](../guides/01-recurring-failures.md). Next:
[Passing tests can still hide broken software](prove-it-works.md).
