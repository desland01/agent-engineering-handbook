# Find what a fresh agent actually misses

You are tempted to pre-load your agent with every skill, plugin and instruction you might
need. That adds setup and constraints you have not justified, and it can still miss the
real gap — because you never observed where it actually fails. Theo's method is the inverse: start
from the defaults, run minimal prompts, and add context only where the failure shows you
it belongs.

## The calibration loop

Theo's advice in the video: do not install every skill and plugin up front and force the
team to match; use the tools as preconfigured and build a solution when you find an actual
problem. Do not touch the instruction files until after the first few prompts show what
goes wrong. Send those first prompts with as little context as possible, to see whether
that is enough — and if it is not, what belongs in the files.

The sequence is: defaults → minimal prompt → observed failure → minimum fix → repeat. Each
addition is justified by a failure you saw, not by a failure you imagined.

**Scope of the advice:** this governs steering files and speculative plugin adoption. It
does not mean stripping standing instructions, authorized tools or safeguards; what you
minimize is *extra project explanation*, not the operating environment. It also does not
restrict deliberate skill authoring, which is a separate activity.

## What a cold start looks like in a real repository

The Course Video Manager investigation shows what that destination looks like in a
repository: its glossary defines the domain nouns; its ADRs record durable decisions; its
agent docs point to the relevant decision for each area. Inspection of those files shows
that a fresh session can find project knowledge in the repository rather than carrying it
in every prompt. The investigation did not run an unassisted cold-start task to
completion, so it shows the provision of that knowledge, not a proven stranger success.

The same point shows on the tooling side. T3's
[PR #5586](https://github.com/pingdotgg/t3code/pull/5586) found that repeated agent setup
failures came from inherited environment variables and *contradictory* instructions — a
problem no amount of extra prose would fix, because the instructions themselves disagreed.
That contradiction was surfaced from the PR's own diagnosis of the failures; inspecting
the code and configuration can also reveal it.

Melee's AGENTS.md goes further on the same theme: each parallel agent gets its own
worktree and an explicit list of owned files, so a fresh session knows its boundary
instead of guessing.

## Add context after observing the miss

1. Start a new repo or agent setup with default configuration and a minimal prompt.
2. Run a representative task. Record each failure: what was attempted, what was expected,
   what blocked progress.
3. Add the minimum fix for each observed failure — a file entry, a rule, a tool — in the
   right home (see [Write instructions that change agent behavior](useful-instructions.md)).
4. Re-run the same task. If it passes, stop adding.
5. Repeat the cold start periodically on a mature project too; onboarding yourself is the
   same diagnostic ([Stop getting lost in your own code](codebase-navigation.md)).

[Guide 05](../guides/05-knowledge-and-instructions.md) has the diagnostic procedure and
the placement table for what each kind of missing knowledge needs.

## Confirm the original miss is resolved

A low-context probe diagnoses missing project knowledge; a verification run counts only
if you check whether the originally observed miss is resolved — and, if the task now fails
somewhere new, whether that is a new, different blocker. Keep the task's authority and safeguards intact — the
probe changes how much extra explanation you supply, not the safety boundary. A single
passing probe does not prove the setup is complete; it proves that task had what it
needed.

## One passing task does not prove readiness.

The video does not measure how much context is optimal, and "minimal" depends on the task.
The verifiable core is the ordering: observe the failure, then add the minimum, rather
than pre-installing against imagined needs.

## Sources

<span id="tip-15-minimal-context-calibration"></span>
**tip-15-minimal-context-calibration** — [16:02](https://www.youtube.com/watch?v=xmGY276gEFY&t=962s).
Theo. Calibrate from a cold start: run minimal prompts first, add context only where it
fails. Evidence type: Theo's directive. Applies to steering files and plugin adoption;
authorized skill authoring is separate and remains governed by your own rules.

Repository evidence: Melee
[AGENTS.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/AGENTS.md)
(worktree and owned-file scoping) and the Course Video Manager
[glossary](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/CONTEXT.md),
from the original investigations. Related:
[agent-context-calibration skill](../skills/agent-context-calibration/SKILL.md). Next:
[One shared contract prevents mismatched code](shared-contracts.md).
