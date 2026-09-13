# Give every agent a working preview

Your agent finished the change on a machine you never touch — a cloud sandbox, a worktree,
a background tab. You cannot see what it built, and the agent cannot see it either, so
neither of you can say whether it works. The answer is a preview the agent can reach,
test, and hand back evidence from.

## Why this changed

Theo used to push back on preview environments: everyone builds locally, so who needs
them. Theo's argument in the video is that the premise died. Code is now built by agents in
cloud sandboxes, background tabs, worktrees and other machines on your network, so a
reachable preview — plus a way for the agent to test it, find bugs, and post the results —
is back to being valuable. This is an argument from Theo, not a measurement.

## Evidence from the repositories, not the video

The original T3 Code investigation shows what "usable" means in practice, through three
merged PRs that each fix a different consumer failure:

- [PR #10501](https://github.com/pingdotgg/t3code/pull/10501) (merged September 8, 2026)
  fixes browser tool output that was returned but unusable: enormous snapshot text lost
  useful locators to truncation, non-object evaluation results broke structured output,
  and screenshots had no saved artifact path. The fix bounds the text, wraps the results,
  and saves PNGs.
- [PR #10572](https://github.com/pingdotgg/t3code/pull/10572) fixes an ownership problem:
  a recording saved on a desktop-local path could not be read by the remote agent that
  needed it. The file is transferred through the existing attachment path into the agent's
  environment. The PR reports a transfer with matching hashes; the investigation inspected
  that claim without repeating it.
- [PR #5586](https://github.com/pingdotgg/t3code/pull/5586) shows the environment itself
  failing: repeated agent setup failures traced to inherited service-launcher variables
  and contradictory instructions, repaired by sanitizing the environment before the dev
  server starts.

The shared lesson: a tool returning data or a path is insufficient if the consumer cannot
use it. And note what one PR did *not* prove — T3's checked-in `t3.json` setup recipe
existed, yet PR #10501 records that it had never been imported for a particular saved
project. A checked-in recipe is not proof that setup runs.

## Make the preview reachable and identifiable

1. Reuse the project's existing local runner or preview platform; do not add a second
   mechanism for one environment.
2. Give each agent workspace a preview URL it can reach from where it runs, plus a
   reliable way to confirm which revision is being served before interpreting any result.
3. Pair the URL with a scripted check the agent can run: a key flow, a screenshot, console
   errors.
4. Keep state isolated between independent workspaces — separate ports do not isolate a
   shared database or session store.
5. Move artifacts created on one machine into the environment of the agent that needs
   them, through the existing authorized attachment path.

Method details and lifecycle guidance live in [guide 03](../guides/03-preview-workspaces.md).

## Return evidence the next reader can open

Have a fresh agent do the whole chain: obtain the URL, confirm the served revision, run
the journey, and return readable evidence. A screenshot nobody can open and a log left on
another machine are both failures of this lesson, not successes. If an artifact transfer
was reported rather than observed, say so.

## Preview value was argued, not measured.

The video makes the case for previews as an opinion; it does not measure their effect. The
repository PRs show that each failure mode occurred and was repaired; they do not show a
measured improvement in review speed. Setting up previews may involve deployments, which
stays subject to your own authorization.

## Sources

<span id="tip-04-preview-environments"></span>
**tip-04-preview-environments** — [05:06](https://www.youtube.com/watch?v=xmGY276gEFY&t=306s).
Theo. Preview environments matter more now that code is built outside your machine.
Evidence type: Theo's opinion/argument, not a measured result.

Repository evidence: T3 PRs
[#10501](https://github.com/pingdotgg/t3code/pull/10501),
[#10572](https://github.com/pingdotgg/t3code/pull/10572) and
[#5586](https://github.com/pingdotgg/t3code/pull/5586), with pinned files and limits in
the original T3 investigation. Related:
[agent-ready-workspaces skill](../skills/agent-ready-workspaces/SKILL.md). Next:
[Give your agent the tool it's missing](missing-tools.md).
