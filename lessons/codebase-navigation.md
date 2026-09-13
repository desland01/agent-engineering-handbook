# Stop getting lost in your own code

You come back to your own project after a month and cannot find where anything lives. Your
agent is in the same position each time it starts without context. The answer is to treat your own repository the
way a good team treats onboarding: a map written for the next reader, and a habit of
harvesting the questions newcomers ask — because you are the newcomer now.

## You are a beginner in a codebase only once

Theo's practice from the video: new teammates were asked to ask at least one dumb question
per day. The point is not charity — the questions reveal what is and is not working for
someone discovering the codebase, insight you only get while someone is still a beginner,
and they feed making the codebase more approachable. Theo describes this for Theo's teams; it
is a cultural practice, not a quota this handbook adopts.

Theo's second observation closes the loop for solo work: past solo projects stayed fully in
Theo's head, so Theo never felt what contributing to them was like. With agents, even Theo's solo
projects now exceed Theo's own comprehension, so Theo builds systems that keep Theo's agents — and
Theo's own attention — from getting lost. The onboarding discipline that used to be a team
concern is now a solo one too. This is Theo's self-description, not a measurement.

## A map written for the next reader

Melee's code map, inspected in the original investigation, is the concrete shape: a table
of task → entry file → named functions → deeper guide, so a reader starts from the
behavior they need, not from a directory listing. It also records its own limits — the
derived object graph is not a call graph and says nothing about callback timing. And each
parallel agent gets a worktree and an explicit list of owned files, so the map comes with
boundaries
([AGENTS.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/AGENTS.md)).

Notice the difference from what Theo says makes a bad instruction file: a bare list of
where things are wastes the budget
([Write instructions that change agent behavior](useful-instructions.md)). A map keyed by
the *task you are trying to do* is navigation; a list of folders is inventory. The map
works because it answers "where do I change X", with the deeper guide one hop away.

The Course Video Manager investigation shows the vocabulary half of the same lesson: a
glossary of domain nouns means a newcomer — human or agent — uses the codebase's words
instead of inventing synonyms for the same idea.

## Navigate from the task you need

1. Write one sentence describing the behavior you need to touch. If you cannot, you are
   not ready to edit.
2. When the repository has a task-keyed map, start from it — behavior, then entry file,
   then function. When it does not, a targeted search is the ordinary way in; what matters
   is recording what you learn (step 3).
3. After resolving an unfamiliar area, add the entry you wish had existed: task → file →
   function → guide.
4. When an agent works in parallel with others, give it an explicit scope — Melee's
   AGENTS.md pairs each parallel agent with its own worktree and an owned-file list. Scope
   discipline like that is that project's practice for parallel work; it is not a
   requirement that every agent task use a worktree.
5. Re-onboard yourself periodically: run a cold, minimal-context prompt and see what only
   lived in your head ([Find what a fresh agent actually misses](fresh-agent.md)).

Navigation tooling details — dependency views built from real artifacts, self-contained
context files for one unit of work — are in
[guide 10](../guides/10-codebase-navigation-and-tooling.md).

## Check whether the map answers the question

You can name the file and function you will change, the relationships you inspected, and
what your navigation view cannot show. A newcomer's next question that your map already
answers is the pass signal; a question it cannot answer is the next entry to write.

## Easier navigation has no measured speedup here.

Whether approachable codebases make teams measurably faster is Theo's motivation for the
T3 stack, offered as an argument, not evidence. The "exceeds my comprehension" claim is
personal.

## Sources

<span id="tip-10-newcomer-questions-signal"></span>
**tip-10-newcomer-questions-signal** — [11:14](https://www.youtube.com/watch?v=xmGY276gEFY&t=674s).
Theo. Treat newcomer questions as a signal for onboarding gaps. Evidence type: Theo
practice for Theo's teams; a cultural practice, not a daily quota, and it depends on
psychological safety.

<span id="tip-18-solo-onboarding"></span>
**tip-18-solo-onboarding** — [18:00](https://www.youtube.com/watch?v=xmGY276gEFY&t=1080s).
Theo. Solo projects now exceed your own comprehension; build systems so you and your
agents don't get lost. Evidence type: Theo anecdote and self-description.

Repository evidence: Melee
[code map](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/docs/code-map.md)
and [AGENTS.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/AGENTS.md);
Course Video Manager
[CONTEXT.md](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/CONTEXT.md),
from the original investigations. Next:
[Improve the environment your agents work in](better-environments.md).
