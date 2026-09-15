# You navigate unfamiliar code without guessing

Start with the requested behavior, then trace evidence until you can name the responsible code. You will check the route before editing and preserve useful navigation output when its refresh fails.

## The behavior gives search a target

Describe the requested behavior in one sentence before opening files that merely sound relevant. Use the words users see and the events they trigger as your first search terms. Matt Pocock recommends exploring the repository whenever its contents can answer your question <a href="#cite-c0240">directly</a>. The first matching file remains a lead until surrounding evidence confirms its responsibility.

## Search builds a working map

Boris Cherny reports that agentic filesystem search outperformed retrieval during codebase navigation <a href="#cite-c0188">in their comparison</a>. Graham Neubig describes agents creating repository maps that help localize likely edits <a href="#cite-c0025">before changing code</a>. A useful map connects the requested behavior to an entry point, responsible definitions, consumers, and nearby checks. Paul Gauthier explains that such a map helps choose which files deserve fuller context <a href="#cite-c0360">for inspection</a>.

## Focused context exposes the route

Pull the likely files into focused context instead of loading every available source at once. Follow references both ways to learn what calls this code and what this code requires. Read definitions beside their uses, because familiar names can conceal different behavior in another project. Keep each research conclusion tied to the exact supporting location, so later navigation remains grounded.

## Planning separates evidence from action

Your exploration should end with a route from requested behavior to the planned change. Anthropic recommends separating exploration and planning from implementation to avoid solving the wrong problem <a href="#cite-c0545">during coding</a>. Name the entry point, responsible code, inspected callers, relevant checks, and remaining uncertainty. Do not begin editing while any step in that route still depends on an untested assumption.

## Limits keep the map honest

Every navigation view omits something, so record what yours cannot prove before relying upon it. Text search may miss runtime registration, while dependency views may omit timing and execution order. Generated context may also hide conditions, stale inputs, or relationships outside its selected boundary. The map guides inspection, while direct evidence confirms which code actually owns the behavior.

## Keep the old map when refresh fails

Some maps depend on successful build results and relationship records before they can answer reliably. If either preparation fails, report the missing evidence before trusting the resulting map. Restore the required inputs, then rerun the same question against the newly generated navigation view. Replace the previous useful map only after the refreshed result completes successfully. For broader tool design, continue with [the lesson about making missing operations usable](missing-tools.md).

## A checked route earns the edit

Before editing, name the requested behavior, its entry point, the responsible code, and inspected dependencies. Then state what your map cannot show and which direct evidence closed each important gap. Follow the route again from the request to the planned change without skipping an unsupported jump. If another reader can repeat that route and reach the same code, your map has succeeded.

## The sources show exploration comes first

The selected sources support direct exploration, repository maps, focused context, grounded conclusions, and separate planning. The videos report particular practitioner experiences, rather than universal performance guarantees for every repository. The documentation explains how maps narrow inspection, while the engineering guide separates research from implementation. The sources do not prove any map is complete, or that one search method always wins.

<ol id="citations">
<li id="cite-c0025">Graham Neubig, video, <a href="https://www.youtube.com/watch?v=B6PKVZq2qqo&amp;t=1242s">Latent Space LIVE! 2024 in Agents</a>, at 20:42. "they basically create a map of the repo"</li>
<li id="cite-c0188">Boris Cherny, video, <a href="https://www.youtube.com/watch?v=julbw1JuAz0&amp;t=3113s">Inside Claude Code with Boris Cherny</a>, at 51:53. "agentic search just outperformed everything."</li>
<li id="cite-c0240">Matt Pocock, video, <a href="https://www.youtube.com/watch?v=EJyuu6zlQCg&amp;t=100s">Agent Skills for Claude Code</a>, at 01:40. "if a question can be answered by exploring the codebase, explore the codebase instead."</li>
<li id="cite-c0360">Paul Gauthier, docs, <a href="https://aider.chat/docs/repomap.html#:~:text=If%20it%20needs%20to%20see%20more%20code%2C%20the">Repository map</a>, at If it needs to see more code, the. "use the map to figure out which files"</li>
<li id="cite-c0545">Anthropic, engineering guide, <a href="https://www.anthropic.com/engineering/claude-code-best-practices#explore-first-then-plan-then-code">Best practices for Claude Code</a>, at Explore first, then plan, then code. "Separate research and planning from implementation to avoid solving the wrong problem."</li>
</ol>

<p id="next-action">Trace one requested behavior from its visible effect to responsible code before making your next edit.</p>
