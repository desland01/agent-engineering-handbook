# Record — the design Charts against the ui-skills instruction set

2026-09-12. Source: the seven skills published at `github.com/ibelick/ui-skills`, commit
`f5dd1de`, plus that repo's `AGENTS.md`. Subject: six selected design Charts. Three passes,
as the owner asked, each one a separate admitted run.

## What the six Charts were missing

Not a single `MUST`, `NEVER` or `SHOULD` between them. Every rule was prose describing a
preference, which a model reads as advice. The reference set writes each rule as a directive
with a strength, and that difference is the whole gap: 388 normative keywords now stand
where there were none.

And all six told the model to check its own work. `design-implementation` and `design-review`
said inspect the rendered result; `ui-ux-design` said render, inspect, correct, repeat;
`design-system` said refine what you actually see; `design-exploration` said look at the
actual result and name the visible differences. A maker grading its own output is not
verification, and the Charts were written as though it were.

## The verification rule, in the owner's order of preference

1. **A code check** — an assertion a build runs and fails on, wherever the property is
   measurable. The Charts now name thresholds rather than intentions: text contrast below
   4.5:1 (3:1 at 24px or bold 18.66px), meaningful graphics below 3:1, animation outside
   `transform`/`opacity`, feedback at or over 200ms, off-screen loops still running, empty
   computed accessible names, keyboard-unreachable controls, absent visible focus, more than
   one accent per view, an empty state whose action count is not exactly one, drawing sizes
   below their floors.
2. **A subagent eval** — where the property needs judgement, a different agent works from
   rendered evidence against stated criteria and returns pass/fail with corrections. Motion
   must be judged from recordings, never from stills — the defect this project already paid
   for. For a design exploration the judge of competing variants is the owner or another
   agent, never the agent that drew them.

`NEVER self-grade` is now written in the Charts in those words.

## The three passes

**Pass 1** (`gpt-6-astra`, three runs) converted `design-implementation`, `design-review` and
`interaction-design` to directives and installed the verification rule. Priority tables,
"when to apply" lists, "how to use" blocks and before/after code snippets were deliberately
left out: good conventions, no room.

**Pass 2** (`glm-5.3-flash`, one run) audited all six Charts against the reference as a
different route, and earned its place. It found nine absent rules, two stated vaguely where
the reference is precise, and one over-correction — our ban on animating anything but
compositor properties is *stricter* than the reference, which allows paint or layout
animation on small isolated surfaces and one-shot effects. A rule agents must hack around is
a worse rule. It also confirmed zero self-verification survived in the three rewritten
Charts, and located the four remaining instances in the three untouched ones.

**Pass 3** (`gpt-6-astra`, two runs) closed the audit's misses and converted the remaining
three Charts. Nothing was skipped. The Charts gained the accessibility interaction contract
they had never carried — focus trapped in dialogs, initial focus set, focus restored to the
trigger, Escape closes, errors bound to their fields with `aria-describedby` and `aria-invalid`
and placed next to the action, a toast never the sole carrier of critical information — plus
primitives-first with no hand-rolled focus behaviour, confirmation on destructive actions, the
motion machinery (no unbounded `requestAnimationFrame`, no scroll-position-driven animation,
measure once then batch reads before writes, blur small and one-shot only, `will-change` only
while animating), viewport and input hygiene, and the typographic means of hitting the
headline checks our own assertions measure. `design-review` gained the falsification pass it
lacked — re-open every cited source and try to break each candidate before reporting — with
ordering by confidence and impact and a hard stop at three findings.

## It cost nothing

| Chart | before | after | keywords |
| --- | --- | --- | --- |
| design-implementation | 9,574 | 9,567 | 108 |
| design-review | 8,886 | 8,866 | 76 |
| interaction-design | 8,691 | 8,676 | 79 |
| ui-ux-design | 6,475 | 6,456 | 43 |
| design-system | 4,606 | 4,594 | 43 |
| design-exploration | 4,570 | 4,570 | 39 |

Directives are denser than prose. The library went from 31 free bytes to 90.

## What is still open

The reference's own craft rules that need bytes we do not have: `create-design-md`'s full
evidence and validation gates for `design-system` (~600 bytes, or ~150 for a pointer), and
page metadata, which no Chart covers at all (~200 bytes, or a decision that it is out of
scope). Both are the owner's call, because at 90 free bytes every addition is a trade.

Releases: `design-charts-normative` (`9185b9c4`), `design-charts-uiskills` (`73f71527`),
`design-charts-complete` (`d3007383`), each admitted with authoring evidence and selected in
turn. Runs `ed10868d`, `253b7550`, `540c43e9`, `0ac8282c`, `04008e3e`, `a17f0a69`.
