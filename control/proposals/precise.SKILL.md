---
name: precise
description: "Apply Nautilus precision conventions to model-facing specifications, worker assignments and evidence reports, or when explicitly invoked as /precise."
audience: llm
disable-model-invocation: false
user-invocable: true
---

# Nautilus model-facing precision

Use explicit scope, conditions, evidence and outcomes in model-facing specifications,
assignments and reusable methods. Human-facing prose uses [simple](../simple/SKILL.md).

- Keep exact identifiers, quotations, values, units and qualifications from the source.
  Examples become requirements only when the user selects them.
- Distinguish observed results from calculations, inference and unknowns where that
  distinction changes a decision. Do not attach a classification label to every sentence.
- Record the outcome, owned scope, relevant inputs and completion evidence once in the
  existing task artifact. Reference it in dependent work instead of creating parallel ledgers.
- Preserve current user corrections and settled decisions. Routine reversible choices remain
  with the agent; surface a missing consequential decision before its dependent action.
- A staged change, selected release, started worker and accepted result are different states.
  Report the state actually observed. Configuration and written rules alone do not prove
  enforcement or successful delivery.
- Reuse adequate evidence for unchanged behavior. Additional checks need a changed behavior,
  observed failure or unresolved risk; this method adds no review stage or testing quota.

## Precision about work that no check can settle

Design, composition, prose and taste have no measurement that decides them. Precision there is
not a borrowed number.

- Do not invent a threshold that looks mechanical and measures nothing. A number enters a
  specification only when something actually measures it and that measurement decides
  acceptance. "Scores at least 8", "reads as premium" and "feels modern" state no requirement.
- Separate the two acceptances and name both: what a check decides, and what a person or a
  different route decides. A craft requirement left inside an executable check that cannot
  decide it has hidden the judgment, not removed it. Say which check proves what, and say
  plainly what remains unproven.
- Specify craft by the defaults it must break, the variance committed to before the work
  starts, and worked examples of a right and a wrong result. Adjectives carry no requirement;
  a named default and its replacement do.
- A judged acceptance names its judge: a route other than the maker, working from rendered or
  delivered evidence, recording the decision and its reason. An unnamed judge is an unmet
  requirement.
- Where a defect can be detected mechanically, encode it as a check and prove the check
  refuses that exact defect before trusting it. A rule that recurs as a manual correction is
  an unwritten check.
- The instruction is not the output. A field name, a template label, a schema key or this
  method's own wording never appears in the work as a heading, a label or a sentence. A
  heading states what its section concludes, in a reader's words, so that a heading read
  alone carries the same conclusion as the section.
- This method governs the facts, evidence and claims of a design or creative method, never its
  register. A design method that opens in a role and names the habits it breaks keeps that
  voice; flattening it into neutral specification prose removes the part that changes
  behaviour. Precision applies to what such a method asserts, not to how it addresses the
  model.

## Carry unfinished work forward

For multi-turn, multi-deliverable, or resumed work: before stopping, retain the explicit
outcomes, accepted corrections, delivery boundaries and unfinished requirements in the task's
existing durable state, with stable identifiers, source and required delivery boundary. Use
that existing state; create no duplicate ledger and no extra ceremony for small or trivial
tasks. On resume or handoff, point to and read that record first. A change of topic does not
cancel unaffected requirements, and only an explicit user cancellation records one.

## Reconcile completion

Before claiming completion, reconcile every stated outcome against the delivered revision,
and perform any readback the outcome requires and confirm it matches. A source edit, accepted
worker output or integration step does not satisfy a requirement to activate, install, publish
or deploy; report partial status by name when any outcome remains incomplete. This requirement
binds where those conditions apply; it claims no universal enforcement and adds no supervisor
or approval gate.

<simple: address the reader as you; preserve necessary evidence and uncertainty without
invented analogies, empty status sections or a sentence-by-sentence audit. Do not name the
owner or refer to the owner in the third person.>
