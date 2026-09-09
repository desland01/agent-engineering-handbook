# 05 — Put project knowledge where the next task needs it

Use this when an agent or newcomer repeatedly misses a project decision, convention or non-obvious fact. Start from the missed decision and choose its home: a comment, public type, executable check, scoped guide, skill or root instruction.

Boris's post, read by Theo around [09:56](https://www.youtube.com/watch?v=xmGY276gEFY&t=596s), describes encoding domain knowledge in the repository. Theo adds two useful constraints: observe what fails before adding instruction machinery ([16:02](https://www.youtube.com/watch?v=xmGY276gEFY&t=962s)), and retain human ownership of root instructions ([12:29](https://www.youtube.com/watch?v=xmGY276gEFY&t=749s)). These are related ideas with different emphases, not a single agreed prescription.

## Diagnose before expanding context

Inspect actual tasks, repeated review corrections and newcomer questions. When the cause is unclear, try a representative task with little **extra** explanation beyond the standing instructions and configured tools. Keep the task's authority, selected methods and runtime safeguards intact. A low-context probe diagnoses missing project knowledge; it does not require stripping the operating environment.

Classify what was missing:

| Missing knowledge | Useful home | Example |
|---|---|---|
| A local reason that the code cannot express | Comment beside the decision | Why this import direction avoids a dependency cycle |
| A shape or invariant the compiler can express | Public type or schema | Exhaustive variants for job outcomes |
| A recurring syntactic error | Existing lint rule or a focused custom rule | Reject a database import from the UI layer |
| A repeatable procedure with judgment | Scoped guide or skill | How to capture evidence for a failed preview |
| A durable cross-project preference | Root instruction | Use the existing secret mechanism; record evidence at the actual revision |
| A domain concept and its accepted name | Domain glossary, with ADR links | Distinguish the render recipe's identity from output-byte identity |

## Write the decision and its reason

A useful instruction tells the agent what to do, when it applies and why. A directory list alone rarely supplies that judgment. A concise task-to-entry map can still help: “For upload reuse, start at the reuse planner; it separates destination identity from content equality.” Keep volatile implementation detail close to the implementation.

For example, if direct `fetch()` calls in this project's components repeatedly bypass its authentication and caching layer, state the project-specific rule and link to the supported entry. If it is mechanically expressible, prefer the existing lint system to repeated prose reminders. Do not ban direct fetch in every project based on this one example.

Theo also suggests encoding reasons to decline features the project deliberately excludes ([13:20](https://www.youtube.com/watch?v=xmGY276gEFY&t=800s)). Record an actual owner decision and its rationale. An agent should not invent a product prohibition because it dislikes a request, or treat an old instruction as overriding a later authorized change.

## Preserve ownership and existing expertise

Human ownership means the owner decides the project's direction. It does not forbid authorized agent drafting or require another approval for an already agreed edit. Here, your request authorizes new guide and skill drafts. Apply bounded instruction edits when the task already authorizes them; raise only consequential decisions that remain unresolved.

When rules conflict, recover their sources, scope and dates before choosing which applies. Preserve exact originals and provenance. Keep uncertain expertise inactive if a migration requires replacement; do not erase it because one probe failed to show an effect. When your project keeps versioned instruction files, use its existing change journal or migration convention so the original stays recoverable.

For instruction-only changes, compare the wording against the user's requirements and inspect what the actual launcher loads when that path changes. Do not create phrase-presence tests, sentence snapshots or a probe quota. Use behavioral checks separately when executable code or configuration changes. A file on disk does not prove the agent's runtime actually loaded it.

## Keep the material current when its subject changes

Update the relevant rule or ADR when an authorized architecture change makes it stale. Split scoped material when that helps discovery. Preserve why an old decision changed; a scheduled purge of unexplained sentences can destroy useful knowledge.

Matt's [open PR #1591](https://github.com/mattpocock/course-video-manager/pull/1591) provides a concrete proposal: retain domain nouns and decisions in the glossary while relocating implementation details beside their code. It was still open at inspection, so this is a proposed change, not the current repository state. See [the Matt inspection](../matt-pocock-inspection.md) and [guide 11](11-domain-language-and-agent-apis.md).

A useful outcome identifies the observed miss, the chosen carrier, the authorized wording or implementation change, and its actual status (drafted, applied, or verified as loaded where that was checked). Use [guide 07](07-team-learning.md) to gather the next useful observation from teammates.
