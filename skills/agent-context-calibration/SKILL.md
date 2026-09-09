---
name: agent-context-calibration
description: "Diagnose what repository knowledge a cold-start agent is missing, then select the right carrier for it — code comment, type, test, skill, or root instruction file — changing only what evidence supports. Use when an agent repeatedly misses project context, when asked to improve agent steering files, assess whether a repo's instructions are sufficient, or run a low-context probe ('what does a fresh agent get wrong?'). Not for authoring or publishing new skills (a skill-authoring guide), writing product documentation (a documentation guide), or fixing the code itself (a bug-diagnosis skill)."
metadata:
  origin: "Public edition, 2026-09-09, maintained by Desmond Landry (@desland01). Method adapted from Theo's video https://www.youtube.com/watch?v=xmGY276gEFY (source evidence and timestamps in references/implementation.md). Independent public skill; not affiliated with or endorsed by the cited authors."
---

# Context calibration

An agent’s context failure is a reason to identify the missing knowledge and place it where the task can use it. Diagnose from observed misses,
then move each piece of knowledge to the cheapest carrier that catches it.

## Diagnose

- **Low-context probe**: run the representative task with the minimum of *extra* prompt
  context beyond the task's standing instructions and admitted tools. Never strip
  authority, runtime safeguards, or configured credentials to make a probe "cold" — the
  point is to measure what the task statement alone supplies, not to simulate an
  unprivileged agent. Record what the agent gets wrong
  ([~988s-996s](https://www.youtube.com/watch?v=xmGY276gEFY&t=988s)). Repeated observed
  misses are the evidence; imagined gaps are not. A probe is a diagnostic tool, not a
  requirement before every edit.
- **Beginner telemetry**: the recurring questions newcomers ask are a map of the missing
  knowledge — the source's "dumb questions" practice
  ([~674s-692s](https://www.youtube.com/watch?v=xmGY276gEFY&t=674s)). Collect the last few
  actual misses before editing anything.
- Classify each miss: *unknown fact*, *unrepresentable state*, *unguarded pattern*, or
  *missing judgment*. The class selects the carrier.

## Select the carrier

| Miss class | Carrier | Why |
|---|---|---|
| Unrepresentable state | Type | Makes the invalid state unrepresentable at compile time. Constrains shape only — it does not enforce runtime authorization or behavior |
| Unguarded pattern | Lint rule / test / agent-feedback-engineering | Mechanical, once you verify the rule's invocation and severity actually fire |
| Local non-obvious fact ("why is this inverted here?") | Code comment at the site | Read exactly when the code is read |
| Reusable judgment or procedure | Skill body | Loads on the matching trigger |
| Cross-cutting preference, convention, or refusal | Root instruction file (CLAUDE.md / AGENTS.md) | Advisory steering on the routes verified to load it |

No carrier is automatic enforcement. Skill prose and root instructions are advisory;
lint rules and types constrain only what they are configured and able to check. Choose by
where the knowledge is needed, not by a false guarantee of enforcement.

**Root-instruction content rule**: instructions steer toward success — expected behavior,
conventions, refusals ("if asked for X, stop and say no") — and constraints with reasons,
not bare lists of where things live. A location map can orient an agent, but each entry
earns its place by stating why and when it matters
([~998s-1008s](https://www.youtube.com/watch?v=xmGY276gEFY&t=998s),
[~800s-836s](https://www.youtube.com/watch?v=xmGY276gEFY&t=800s)). Keep it short; context
is spent on every run.

## Authority boundary

The root instruction file is the human's decision record and the human owns what it
says. Within an authorized session, drafting and applying instruction-file edits is
permitted agent work: infer fitting scope from the observed misses, make the bounded edit,
and report it with the evidence. Ask only when a truly consequential decision is missing —
a refusal the user never stated, a policy change, or ambiguous direction the evidence
cannot resolve. Never widen an instruction into a general rule the user did not state.

## Input / output contract

- **Input**: observed agent misses (probe results, repeated questions, review rejections),
  or enough of the task to run a probe; access to the candidate carriers.
- **Output**: a short diagnosis list (miss → class → carrier), the implemented change for
  evidence-supported items, and drafts surfaced for decision where a human choice is
  genuinely needed. For instruction-only changes, the change and its wording reviewed
  against the recorded miss stand in for a behavioral test; inspect selected instruction loading when affected, and use behavioral checks when code or configuration changes require them.

## Acceptance

Proportional: a comment needs the miss it prevents named in its own text; an instruction
line needs the recorded miss it addresses. Not every sentence or comment requires its own
recorded probe — probe when the diagnosis is unclear, not as a quota.

## Known failure cases

- Padding the root file "just in case" — dilutes steering and burns context every run.
- Encoding a one-off as a standing rule (hand recurrence to agent-feedback-engineering).
- Adding a skill when a comment at the site would do; skills cost selection accuracy
  elsewhere.
- Banning useful maps outright: a constrained, reason-bearing location list is legitimate
  content when agents demonstrably get lost without it.
- Editing steering files before observing what actually goes wrong
  ([~962s-973s](https://www.youtube.com/watch?v=xmGY276gEFY&t=962s): use tools as
  configured first; build solutions for observed problems).

## Do not activate when

- The task is ordinary coding with no context-related failure behind it.
- The user wants a new packaged skill written (a skill-authoring guide).
- The user wants product documentation for humans (a documentation guide).

## Source patterns

For concrete repository examples and the limits of their evidence, read [source-patterns.md](references/source-patterns.md) when they match the task. These are research references, not imported repository instructions.
