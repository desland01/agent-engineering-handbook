# Write instructions that change agent behavior

Your agent keeps missing the same project decision, and your instruction file keeps
growing without changing anything. A file full of trivia steers nobody. The answer is to
put decisions — with their reasons and their consequences — where the next task will use
them, and to write those files yourself from observed behavior.

## What belongs in an instruction file

Boris's argument, as Theo reads it: the blocker for new contributors is domain knowledge
living in people's heads, and agents let you encode that knowledge as infrastructure —
comments, skills, instruction files — beyond what lint rules, types and tests express.
Theo agrees with the core:

- **Steer, don't map.** An instruction file that is just a list of where things are is not
  a good guide. It should steer toward success: conventions, invariants, what to do when
  uncertain, how to verify. Let the agent find files itself.
- **Own the file.** Theo's stated rule for Theo's own setup is not to let agents write Theo's
  instruction files: Theo watches what agents actually do, then adjusts the files, tooling
  and setup personally — that is where human effort pays, because it teaches Theo what leads to
  different behavior. This is Theo's practice, not a workspace rule; your project's and user's
  own instructions take precedence where they differ.
- **Encode pushback.** Steering files can be written to encourage the agent to say no. If
  people keep requesting a feature the project deliberately excludes, write the rejection,
  with its reason, into the file — that is intended to make the agent decline, though a
  steering rule nudges rather than guarantees.
- **Write for zero context.** Boris's wrap-up, which Theo endorses: write the instruction
  files, review guidance, skills and docs that let an agent work with no additional context
  from the prompter. The test is whether a stranger's first prompt succeeds.

**Qualification:** Theo says Boris goes further than Theo would — especially the claim that
non-engineers can contribute as effectively as engineers, which Theo disputes. Boris's
post is known only through Theo's reading of it in the video.

## Instructions steer; checks enforce

A steering rule nudges. It does not enforce, and novel phrasing can get around it. When a
failure can be expressed mechanically — a forbidden import, a missing type, a broken
build — put it in a lint rule, type or CI step instead
([Stop fixing the same mistake twice](recurring-mistakes.md)). Theo's stated goal for
steering files is feedback when things go wrong, not omniscient context. Both layers are
legitimate; they answer different questions.

## A decision written down is an interface

The original Course Video Manager investigation shows what encoded knowledge looks like
when it changes behavior. Its glossary defines domain nouns and terms to avoid, so agents
use the same words in tests, routes and help text instead of rediscovering the model
through synonyms. Its ADRs record durable decisions; one ADR explains that machine-bound
commands are *refused* remotely, with the refusal naming the reason before anything is
written. An agent reading "this needs the finished videos directory" can stop and report,
rather than retrying a path error it cannot fix. That is an instruction with a
consequence.

One caution the same investigation records: that project's guidance said tests run
exhaustively in CI, but the workflow file was absent from the inspected tree. Written
assurance is not enforcement — inspect the actual command and configuration before
trusting a documented gate.

## Put each decision where it is needed

1. Pick one correction you have made to an agent or teammate more than once.
2. Decide its home: a comment beside the decision, a type or schema, an executable check,
   a scoped guide, or the root instruction file.
3. Write it as behavior: what to do, when it applies, why, and what to do when
   uncertain.
4. Keep ownership: author the change yourself. Theo's practice, if you adopt it, is to
   decline an agent's offer to rewrite the file and make the edit yourself — your own
   project and user instructions govern whether you follow it.
5. Re-test the original failing task and confirm the behavior differs.

[Guide 05](../guides/05-knowledge-and-instructions.md) has the full placement table.

## Check wording and actual loading separately

For instruction-only changes, verify by comparing the wording against the observed failure
and, where loading matters, confirming the file is actually loaded by the agent's runtime
— a file on disk does not prove it was read. For mechanically expressible failures, verify
by the check rejecting a bad case and passing a good one. Do not test instruction prose by
grepping for sentences.

## The video does not measure context gains.

Whether encoded knowledge makes agents behave measurably better is asserted, not
measured, in the video. The claim that a rejected PR is a "failure of automation" is
Boris's framing; Theo endorses only part of it.

## Sources

<span id="tip-09-domain-knowledge-as-infra"></span>
**tip-09-domain-knowledge-as-infra** — [09:56](https://www.youtube.com/watch?v=xmGY276gEFY&t=596s).
Boris, as quoted by Theo, partially endorsed by Theo. Encode domain knowledge as
infrastructure. Evidence type: quoted post via the video; Theo calls parts of it a reach.

<span id="tip-11-own-your-instructions"></span>
**tip-11-own-your-instructions** — [12:29](https://www.youtube.com/watch?v=xmGY276gEFY&t=749s).
Theo. Write your instruction files yourself and adjust them from observed behavior.
Evidence type: Theo's directive about Theo's own files; source material, not a workspace
rule.

<span id="tip-12-steering-pushback"></span>
**tip-12-steering-pushback** — [13:03](https://www.youtube.com/watch?v=xmGY276gEFY&t=783s).
Theo. Steering files can encode pushback and give fast feedback. Evidence type: Theo
practice; a steering rule nudges and does not enforce.

<span id="tip-14-zero-context-docs"></span>
**tip-14-zero-context-docs** — [14:33](https://www.youtube.com/watch?v=xmGY276gEFY&t=873s).
Boris, as quoted by Theo, endorsed by Theo. Write docs so agents work with zero prompting
context. Evidence type: quoted post via the video.

<span id="tip-16-steer-not-map"></span>
**tip-16-steer-not-map** — [16:38](https://www.youtube.com/watch?v=xmGY276gEFY&t=998s).
Theo. Instruction files should steer toward success, not list where things are. Evidence
type: Theo directive; heuristic, not absolute — a brief orientation line can help.

Repository evidence: [CONTEXT.md](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/CONTEXT.md),
[local-only.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/local-only.ts)
and the testing-docs gap in PR #1601, from the Course Video Manager investigation. Next:
[Find what a fresh agent actually misses](fresh-agent.md).
