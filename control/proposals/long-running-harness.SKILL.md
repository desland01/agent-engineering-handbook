---
name: long-running-harness
description: "Execute a settled ticket graph or create a requested restartable harness, mission handoff, experiment loop or recurring-work packet. Use when the work needs durable continuation across sessions or the user explicitly requests a harness; ordinary audits, QA and single-task implementation use their relevant methods."
user-invocable: true
argument-hint: "[goal-or-json] [--domain frontend|api|backend|database|cms|design-system|qa|launch|research|ops|mixed] [--scale small|medium|large|whole-site|whole-system] [--mode audit|plan|fix|verify|execute] [--shape packet|sdk|auto]"
lifecycle:
  origin: "long-running agent harness skill; file birth 2026-08-14 under ~/.agents/skills/long-running-harness; linked into ~/.claude/skills; first versioned in ~/.agents at a443ea2 2026-08-12 (content path), birth on disk 2026-08-14; body re-passed under INSTRUCTIONS.md Part II 2026-08-27 (top-50 sweep batch 2)"
  class: workflow
  sunset: "retire when durable restartable harness authoring is no longer needed for multi-session agent work"
  last_verified: 2026-08-27
  boundary:
    producer: "user goal that needs a checkpointed run packet or approval-gated SDK harness"
    consumer: "agent session that must produce a resumable harness instead of a one-shot run"

---

# Execute settled work to completion

Select the smallest fitting shape:

| Work | Execution |
|---|---|
| A clear result that fits the current task | Direct execution. |
| Independent tickets or work that must survive sessions | Finite ticket owner in the existing runtime. |
| A stable optimization metric with a stopping condition | Experiment loop through the same execution boundary. |
| Explicit recurring work | Existing scheduler with durable state. |
| A request only for a packet or harness design | Deliver that artifact and report it has not started work. |

## Pilot first, then scale

Never apply the same change to a batch until one item has gone end to end. This binds every
shape above that touches more than one item: a ticket graph over many files, a sweep, a
rename across repositories, a migration, a loop over a work-list.

1. Count the work-list yourself; do not trust a supplied count. Re-scope if it differs.
2. Pick the riskiest item, never the easiest: indirection (a symlink, a pointer, a linked git
   worktree, a gitignored path), or the item already known to be bad.
3. Read that item's own contract before editing (`AGENTS.md`, `CLAUDE.md`, `.claude/rules/*`).
   It decides what a valid change is here and whether you may commit at all.
4. Change that one item through the same route the batch will use.
5. Verify by diff before anything lands: `git status` in every repository touched, the item
   diffed against its committed state. A new commit in a repository that was not the target
   means the pilot failed. Stop.
6. Write the procedure that worked into the batch's task inputs as you go.
7. Only then scale, with a fresh agent that has no memory of the pilot session. Add an
   instruction only where that agent stalls.

### Pilot the harness, not only the change

Proving the content change on one item does not prove the machine that will carry it. Before
generating the batch plan, run a pilot plan of one ticket over one or two items through the
whole path — prepare, dispatch, check, accept — and require the ticket to reach `accepted`.
A worker that delivered, a checker that never ran, and a ticket left `running` or `blocked`
are three different states, and only the third-from-last is progress. Build the pilot plan
and the batch plan from **one generator with a plan-id argument**, so the machine you proved
is the machine that runs; a hand-built pilot proves nothing about a separately hand-built
batch.

### A failed pilot is the pilot working

Fix what failed **in the machine** — the task text, the acceptance check, the workspace
layout, the capsule — and pilot again. Never repair the pilot's output by hand and scale
anyway: a defect you corrected yourself is a defect the batch reproduces on every remaining
item. Where the defect is mechanically detectable, it becomes an executable check before the
batch runs, and that check is proved to refuse the exact bad output before it is trusted.
Where it is not mechanically detectable, name it in the task text and in the judged
acceptance. Repeat the pilot after each fix; the pilot is done when it needs no
intervention, not when you are tired of it.

### Construction faults a pilot surfaces in minutes

Each of these refused every attempt of a 67-item batch, and each is invisible until a plan is
actually dispatched. Check them while building, and let the pilot prove them:

- Worker and checker workspaces must not sit inside the runtime's installation home; a
  workspace under it is refused as `workspace_overlaps_installation_home`.
- Every capsule needs non-empty required charts, tools and declared outputs — the checker's
  capsule included — and every effective tool set must sit inside the anchor tools and
  include the native `Skill` tool.
- A worker may not read an input out of the checker workspace. Keep a second copy of any
  shared list outside it and feed the worker that copy.
- The checker's argv must contain no path the check itself creates. The controller hashes
  every argv element that exists as a file, so a candidate or report path passed as an
  argument changes the environment digest between freeze and verify and blocks the ticket as
  `checker_environment_changed`. Derive those paths inside the checker from a stable
  argument.
- A relocated or edited plan needs a new plan id. Reusing the id after the first run blocks
  with `plan_changed_since_first_run`.

An item that resolves outside the batch is not in the batch. Resolve every path before
editing; if it lands outside the tree the batch is scoped to, leave it, record it, report it.
Editing it "from the other side" is the same edit. Stop conditions: the pilot needed more than
one attempt (fix the procedure, re-pilot); the pilot touched a file outside its item; the real
count differs from the supplied one.

Evidence (ablation 2026-08-15, 40 arms, scored on what the agent did): blind controls damaged
a protected branch in 8 of 20 runs; with this rule loaded, 0 of 20; Fisher exact two-tailed
p = 0.0033; both sides completed 11 of 11 real items, so the rule costs nothing in throughput.
All 20 controls detected the indirection and 8 edited through it anyway: the effect is what
the agent does after noticing, not whether it notices. Artifacts and the origin incident are
retained with the proposal (`pilot-first/eval/`). Origin: owner directive 2026-08-15, after 25
skills were restored in one bulk pass and one restore nearly destroyed a skill body through a
linked worktree.

Preserve an explicit execution shape. The retained domain, scale, mode, shape and external
flags describe the request; they do not grant authority or select an alternative provider.

Name every input by its exact accessible path — including files inside hidden directories —
in each assignment. Absence from a default glob is not absence of a declared input file:
before a worker reports an input missing, confirm the declared path itself is inaccessible.
A required input that cannot be found at its named path is a specific blocker for its
dependent tickets only; it is never filled with intuition or a fabricated value or count.

Keep the user's planning sequence: conversation, clear context, consequential grilling,
specification and tickets. Once those decisions and effects are authorized, execute without
another interview or approval. Each independent ticket delivers a useful result with known
dependencies, owned files, relevant inputs and functional/craft acceptance.

For ticket execution, load [runtime commands](references/runtime-commands.md). Use
`tickets-prepare` to copy settled task inputs and bind hashes in existing capsules, then
`tickets-start` to launch the finite owner. Retain its runtime path and owner identity;
`tickets-inspect` reads that run even after another release is selected. A Markdown packet
or skill invocation does not sustain execution. Load the
[runtime contract](references/runtime-contract.md) only when changing or connecting the
controller's admission, acceptance, repair or recovery behavior.

When selecting an executor, load [model assignment](../glm-fleet/references/model-assignment.md).
GPT-6 resolves uncertainty; GLM implements independently specified work; Fable owns visual
quality. Use a fresh agent for independent tickets. A repair receives the actual failed
behavior, existing artifact and relevant decisions; preserve useful context instead of
splitting a coupled change solely to reset an agent. The current native ticket route uses a
fresh run with saved repair inputs; it does not resume a native conversation.

Declare acceptance before dispatch: name the required report targets and each required
check there. Keep checker definitions outside worker write scope.
Prefer existing meaningful checks; use capable judgment only for unresolved quality that
those checks cannot establish. No compulsory cheap-model evaluator or reviewer chain.
A worker exit cannot accept work. The runtime binds acceptance to the actual output revision:
for every task, each required check is verified individually against the exact delivered
artifact bytes or revision, in addition to any aggregate score. For SEO page tickets this
specifically requires verification against the exact final rendered HTML bytes and each
required term, placement, link, truth and protection check. A failed required check blocks
acceptance; acceptance is never obtained by silently relaxing targets or by the aggregate
score alone, and no check is waived by task type. An unavailable
required attachment is reported as unavailable and its dependent implementation is blocked;
a prompt or plan alone is not enforcement. If a requirement conflicts with verified facts or
with another requirement, surface the conflict and block the dependent action rather than
fabricating evidence or lowering the bar.

## Carry requirements through execution

Retain the explicit user outcomes in the existing durable task state with stable identifiers,
and map each requirement to the ticket result and acceptance definitions that deliver it. Do
not omit deployment, activation or verification merely because the implementation is staged.
Distinguish acceptance from required integration in both execution records and inspection
summaries: an accepted ticket with integration outstanding is not a delivered requirement. Use
the existing integration field when delivery requires integration. Preserve the original
requirement record across resume and handoff, updating only affected decisions; topic changes
and interruptions do not cancel unfinished outcomes.

At completion, reconcile every requirement with delivered evidence and the owning runtime's
inspected state. Accepted work with required integration outstanding is incomplete, and a
missing required active readback remains incomplete. Retain the exact runtime and artifact
revisions so a later session can verify the same result. This mapping is a coordinator
obligation; do not describe prose alone as mechanical enforcement over every conversation.

Repair product defects. Treat provider/admission failures and uncertain effects as their
specific blockers. A repeated equivalent defect without progress goes to GPT-6 for diagnosis;
it does not buy another equivalent attempt. Reuse passing evidence for unchanged behavior.
Integrate through the existing project transaction and preserve later conflicting edits.
Repair is deterministic: a failed acceptance reruns the same acceptance definition against
the repaired revision. Acceptance is never weakened, redefined mid-run, or waived to obtain
a pass; missing required evidence blocks only its dependent tickets, and a completed
evidence-only or planning wave does not satisfy the goal's remaining named outcomes.

Maximize AFK time: settle known consequential decisions during planning. Record a discovered
decision with a recommendation, affected tickets and the last safe decision point. Continue
independent work; surface a blocker before its dependent action. Batch nonblocking decisions
at closeout. Silence is not authorization.

On restart, reconcile the retained owner, native attempts and completed effects before
launching anything again. Stop at the agreed acceptance, cancellation or a concrete blocker.
Use only authorized budgets and actual runtime/provider constraints; no arbitrary GLM caps,
recurring supervisor or automatic restart is implied.

Experiments additionally need a fixed metric, baseline, constraints and stopping condition.
Retain measured improvements, discard regressions and preserve evidence. Missing measurements
or weakened acceptance never establish progress.

<simple: report the accepted result, owner state, blockers and what the actual checks prove.
Do not create another planning, review, authoring or polish stage at completion.>
