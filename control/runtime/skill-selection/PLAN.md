# Selecting skills is a step the run must take, and the runtime can measure whether it did

2026-09-11. Deliverable for the Nautilus runtime and the selected Charts. One rule in four
places: at intake every route names the skills it will use — plural — in the order they
apply; a delegated worker gets that list in its capsule beside its contract; and a run that
declared a skill it never invoked ends blocked instead of completed. One of the four is
applied; the rest are staged here. The status table at the end says which is which.

## The selection step exists nowhere today

| Surface | What it says now | What that produces |
| --- | --- | --- |
| `ARCHITECT.md` | "Use `precise` and relevant domain/implementation skills." | A reminder, no intake step, no plural, no order |
| `charts/operating.md` ¶1 | "Choose the methods needed to complete it within those requirements." | No named step, nothing to check against |
| `charts/core-skills/CORE.md` ¶1 | "Use the applicable method for the current deliverable." | Singular by construction |
| Capsule declaration | `requiredCharts` is required and non-empty; its bodies are sealed into the run's system context | Skills are *present*, never *applied* |

Nothing asks the model to look at the catalog before it starts, nothing says the answer is
usually more than one, and nothing distinguishes a skill that shaped the work from a skill
whose bytes rode along in the prompt.

## The runtime already measures the thing it does not enforce

`chartEvidenceTracker` (`src/capsule-runtime.mjs:181`) counts, per required Chart,
`available / invoked / invocationSucceeded / failed`, and `summary()` returns
`withoutSuccessfulInvocation`. Probed on 2026-09-11 against the source tree at
`~/Documents/Codex/2026-09-04/ca/outputs/nautilus`, three declared Charts and one invoked:

```
withoutSuccessfulInvocation: ["nautilus-core:ui-ux-design", "nautilus-core:design-review"]
```

`src/runtime.ts` pushes that summary into the run record as a `capsule_required_charts`
event and reads it nowhere — line 426 in the selected release, 433 in the source tree this
patch targets. The comment ten lines below it says so outright: *"No post-hoc required-Chart
gate: presence of the required bytes was a precondition of every forwarded model request."*
Every other line number in this plan is the source tree's; `runtime.ts` is the one file where
the two copies differ, by an unrelated `nextTask` addition ahead of the release.
Byte presence is the whole obligation. Read down the completion path and nothing consults
that summary, so a worker that declares five skills and invokes none still finishes
`completed` — read from the code, not from an observed run. It is the same defect class as
`worker-egress`: the run did not do what it was told, and said it was done.

## Two constraints any design has to live inside, both enforced today

**A child may not require a Chart its parent lacks.** `childSubsetViolations`
(`src/capsule-admission.mjs:59-66`, read in source and exercised by the suite's existing
parent-subset test) refuses both directions: the child omitting a mandatory
parent Chart, and *the child requiring a Chart the parent does not*. So a parent cannot
discover mid-flight that a worker needs `design-review` and hand it over. Selection for the
whole assignment tree happens once, before the first dispatch, in the parent's own
declaration. That is a feature — it forces the plural answer up front — but it must be
written down, because the failure mode is an admission refusal at dispatch time.

**There is no room in the skill library for a new method.** `skill-capacity.json` declares
50 core skills against an allowance of 50, and 26 domain against 50. Summing the release's
bundle files gives 2,096,342 of the 2,097,152-byte library limit — 810 bytes of headroom —
and `assertSkillContentBounds` (`src/skill-content.ts:19`) counts only
`charts/(core|business)-skills/bundles/**`, so the Charts themselves are not counted. So the
selection rule goes in `operating.md` and `CORE.md`, where it belongs anyway: a skill cannot
be the instruction to look for skills, because nothing would have loaded it.

## The rule, in the words that ship

For `charts/operating.md`, replacing the last sentence of ¶1 and adding one paragraph:

> Before the first substantive action, read the available skill catalog and name the
> skills this task needs. More than one is the ordinary answer: work spanning research
> and implementation, or design and copy, takes a chain, where the earlier skill's
> output is the next one's input. Name them in the order they apply and load each one
> where it applies, not all at the start. A skill you selected and never invoked is a
> defect, not a saving. When nothing in the catalog fits, say what you looked for and
> continue.

For `charts/core-skills/CORE.md`, removing "Use the applicable method for the current
deliverable." from ¶1, reflowing that paragraph, and inserting two sections immediately
before "## Classification and capacity":

> ## Most tasks need more than one method
>
> Read the catalog at intake, before the first substantive action, and name every method the
> task needs. The ordinary answer is several. A long or composite assignment is a chain —
> plan, then implement, then review — where each stage's output is the next stage's input.
> State the chain before starting and load each method at the point it applies rather than
> all at once. Invoking none of the methods you named is the failure this step exists to
> prevent; where nothing in the catalog fits, say what you looked for and continue.
>
> ## A worker is given its methods, not left to guess
>
> Delegated work carries the same selection, made by the parent. The capsule names the
> worker's methods in the order they apply, beside the assignment, inputs, write ownership,
> limits, deliverable and completion evidence. Admission refuses a method the parent does not
> itself require, so the parent selects for the whole assignment tree before the first
> dispatch rather than discovering a missing method at hand-off.

## The capsule declares the plan, and the Watch settles it

Capsule schema version 5 adds one field:

```json
"skillPlan": [
  {"chart": "nautilus-core:engineering-plan", "purpose": "settle the interfaces first"},
  {"chart": "nautilus-core:tdd",              "purpose": "failing check before the fix"},
  {"chart": "nautilus-core:code-review",      "purpose": "review the diff before handing back"}
]
```

Rules, all refusable at parse or admission:

1. Non-empty in version 5. Array order is the chain order; no duplicates.
2. Every `chart` appears in this capsule's `requiredCharts`; `purpose` is a non-empty string.
3. A child's `skillPlan` charts stay inside the parent's `requiredCharts`. The existing
   subset rule already refuses this case on the `requiredCharts` dimension;
   `childSubsetViolations` gains a `skillPlan` dimension that fires alongside it, so the
   violation list names the plan as well as the chart.
4. Versions 1-4 keep their exact current behaviour: no plan, no new refusal. Version 5
   inherits the version 3 null-deadline and version 4 null-request-cap opt-ins, so the
   version gates in `capsule-schema.mjs` move from `=== 3`/`=== 4` to `>= 3`/`>= 4`, which
   leaves every version 1-4 declaration evaluated exactly as before.

Enforcement, at the end of a run rather than before it, because invocation is only knowable
afterwards: `runtime.ts` reads `capsuleRun.charts.summary().withoutSuccessfulInvocation`,
intersects it with the declared plan, records a `capsule_skill_plan` event either way, and
where the intersection is non-empty sets `record.reason` to `capsule_skill_plan_uninvoked`.
The existing `if(record.reason)throw` below it raises, and the catch at `runtime.ts:458` sets
`record.status='blocked'` with that reason. That last step is read from the source, not
exercised: the staged tests cover the contract and the verdict as functions, and a run whose
status was observed end to end would need a live capsule run.
Charts that are in `requiredCharts` but not in the plan keep today's behaviour exactly —
present, never obligatory — so no existing run changes status.

The Anchor gains the matching constant, so the obligation is a user decision rather than a
code detail:

```json
{"id": "N009",
 "statement": "A run must invoke every skill its capsule selected.",
 "tier": "user-decision",
 "check": {"field": "skill_plan_invoked", "kind": "boolean", "op": "==", "value": true}}
```

`skill_plan_invoked` is measured once per run, at termination, from the tracker. It says a
planned method was invoked and its result was not an error; whether the method shaped the
work is not measured anywhere in this runtime, and the statement does not claim it. It is not a
per-request fact: a request forwarded before the second skill in a chain is invoked is
legitimate, and gating requests on it would make every chain unrunnable.

## What has to be proved, in this order

1. **Red.** A version 5 capsule whose plan names three Charts, of which one is invoked,
   finishes `completed` today. Assert it, watch it pass, and keep it as the regression.
2. **Parse.** Version 5 refuses: absent plan, empty plan, duplicate chart, a plan chart
   outside `requiredCharts`, an empty purpose, a plan on versions 1-4.
3. **Green.** The same run from step 1 now yields a verdict of
   `{allInvoked: false, uninvoked: [...]}` naming the two skills, and `record.reason`
   becomes `capsule_skill_plan_uninvoked`.
4. **Permitted work still runs.** A run invoking every planned Chart finishes `completed`;
   a version 4 capsule with unused `requiredCharts` still finishes `completed`.
5. **Delegation.** A child whose plan names a Chart the parent does not require is refused at
   admission, with the plan dimension in the violation.
6. **Charts.** The two Chart edits are byte-checked into the release, the composed system
   context re-derives to its digest, and a worker's initial context is read back to confirm
   the new text arrived.

Steps 1-5 are `tests/capsules/skill-plan.test.mjs` under the existing
`tsx --test` runner. Step 6 uses the chart-correction mechanism already proved in
`control/runtime/chart-corrections/`.

## What this deliverable does not do

It cannot prove a skill was *applied*, only invoked: `application` stays `'unverified'` in
the tracker and no measurement here changes that. It does not touch the parent Claude Code
or Codex sessions, which have no capsule — for those the rule is instruction-only, in
`ARCHITECT.md`, and the honest claim is wording, not enforcement. And it is staged, not
applied: the runtime source tree at `~/Documents/Codex/2026-09-04/ca/outputs/nautilus` still
carries 5,460 dirty entries, so the patch and its tests land here until that tree is clean.

## Status on 2026-09-11

| Piece | State | Evidence, and what it does not cover |
| --- | --- | --- |
| The rule for the Codex architect route | Applied to `~/.nautilus/architect/ARCHITECT.md`, section "Pick the skills before the work" | Readback: `launch.py --check` builds the prompt and finds the amended contract in the constructed frames exactly once (`nautilus_architect`, `contract_delivered_once`, `native_profile_contract` all true, `modelCalls: 0`). That check's own stated scope is prompt construction; Desktop task instructions are not observed by it. Original at `backups/skill-selection-20260911/` with `change.json`. |
| The rule for the interactive Claude route | Same file, same edit | Configuration only. `nautilus-claude` reads the file into `--append-system-prompt` at `bin/nautilus-claude:25`, and `--check` reports `contract` as that path with `"status": "configuration-only"`. No delivered prompt was read back on this route. |
| The intake step on the interactive Claude route | Applied: `~/.nautilus/bin/skill-intake-reminder` (new) bound as a `UserPromptSubmit` hook in the settings `nautilus-claude` passes | Readback, twice. The CLI's debug log records `UserPromptSubmit (/Users/thebeast/.nautilus/bin/skill-intake-reminder) provided additionalContext (338 chars)`, matching the script's own output exactly; a second bounded print-mode run asked the model for the injected line's first six words and got "Skill check, before the first substantive" back. Non-blocking by construction: the hook only adds context, and the launcher omits it if the script is missing or not executable. A session already running keeps the settings it started with. Original launcher at `backups/skill-intake-hook-20260911/`. |
| The rule for every worker | Staged, not published: `charts/operating.md` and `charts/core-skills/CORE.md` here, with `chart-edits.json` carrying before/after digests | Wording only. 1,777→2,221 and 5,225→6,211 bytes. Neither file is counted by `assertSkillContentBounds`, which measures `charts/(core|business)-skills/bundles/**` alone; that library holds 2,096,342 of 2,097,152 bytes, and `skill-capacity.json` declares 50 core of an allowance of 50, 26 domain of 50. |
| The capsule contract and the terminal verdict | Staged, not applied: `skill-plan.patch` against four source files and two existing tests, `provenance.json` pinning their pre-patch digests | On copies of `src/`, `vendor/` and `tests/` outside the dirty source tree, under `tsx --test`: unpatched copy with the new test installed, 4 pass / 7 fail; `git apply --check -p1` clean; the patch applied to a fresh copy, `tests/capsules/*.test.mjs` 118 pass / 0 fail with the new file included. What that proves is the declaration contract and the verdict as functions. The `blocked` status is read from `runtime.ts:458`, not exercised, and semantic application is measured nowhere. |
| The Anchor constant `N009` | Written in this plan, not staged as a file | No evidence, and none is claimable: an Anchor edit travels with the release that carries the patch, and staging the constant alone would assert a measurement the selected runtime cannot make. |

Against the six steps above: 1 through 5 are proved by those runs. Step 6, the Chart edits
in a composed release with a worker's context read back, is not started.

One test in the suite is intermittent and it is not this deliverable's:
`lease-contention.test.mjs` fails `capsule_lease_store_busy` under the full parallel run on
both trees — once in three full runs of the unpatched tree, none in three of the patched
tree — and passes five of five standalone on each. It touches `capsule-leases.mjs`, which
this patch does not change.

The two existing tests that pinned the old contract version are updated inside the patch:
`capsule-role.test.mjs` expects `[1, 2, 3, 4, 5]`, and `capsule.test.mjs` moves its
invalid-version sentinel from 5 to 6.
