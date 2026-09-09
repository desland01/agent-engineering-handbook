# 07 — Turn newcomer questions into improvements

Use this when teammates or agents repeatedly get stuck on the same first task. Their questions reveal knowledge the repository does not yet communicate, and setup that its maintainers no longer notice.

Theo describes asking newcomers to surface basic questions around [11:14](https://www.youtube.com/watch?v=xmGY276gEFY&t=674s). He argues that this helps improve the next contributor's experience. Earlier, around [07:28](https://www.youtube.com/watch?v=xmGY276gEFY&t=448s), he says teams are more receptive to tooling work. Those are experience and opinion, not measured universal outcomes.

## Capture useful friction without creating a reporting ritual

Use the task discussion, review or existing team notes. Keep the question, the attempted action, what the person expected and what actually blocked progress. Make questions easy to ask and answer them promptly. Do not withhold a helpful answer until a tool or document is written, force questions into public channels, or turn a suggested daily practice into a quota for agents.

Classify the cause before choosing a fix:

| Cause | Fitting response |
|---|---|
| A missing fact or unclear term | Improve the local explanation or domain glossary |
| A repeated code mistake | Add the smallest applicable type, lint rule or behavioral check |
| Setup differs from the documented path | Repair the bootstrap or launcher and verify that path |
| A supported operation is inaccessible | Repair the interface or add a narrow adapter |
| A consequential design decision is unresolved | Resolve it with the responsible owner and retain the reason |

Choose work by the cost and frequency of the obstacle, severity of the mistake, and how many future tasks it affects. A high-impact first occurrence can justify a fix. Do not restrict improvement to one item per week or require an artifact for every question.

## Verify the next attempt

For example, two contributors cannot run checkout tests because setup never creates the required seed data. First establish whether the seed step is safe and part of the existing bootstrap contract. Incorporate it into that path or report its absence with a useful command. A fresh setup run reaches the checkout test without the private explanation. This is an illustrative scenario, not a source-repository experiment performed here.

For instruction-only changes, review the wording and selected loading where affected. When the cause remains unclear, use the low-extra-context diagnostic in [guide 05](05-knowledge-and-instructions.md). Do not require a behavioral probe for every sentence.

Track comparable outcomes when deciding whether a larger investment paid off: first working result, repeated corrections, failed setup attempts and repair effort. A faster first PR is useful only if the work still meets its requirements; promoting trivial PRs would distort the measure.

## Apply the same principle to solo work

Theo argues around [16:54](https://www.youtube.com/watch?v=xmGY276gEFY&t=1014s) that building an environment where others can deliver is valuable engineering work, and that agents let a solo developer practice it too. Treat career benefits as his opinion, not a promise. The practical goal is that a new session can discover the domain, make a bounded change and know whether it worked.

Boris's stronger claim about equal effectiveness of non-engineers is disputed by Theo around [09:49](https://www.youtube.com/watch?v=xmGY276gEFY&t=589s) and [12:15](https://www.youtube.com/watch?v=xmGY276gEFY&t=735s). Better tools can lower contribution friction; they do not establish equal judgment or eliminate expertise.

Keep useful decisions discoverable through the existing [context method](05-knowledge-and-instructions.md), [feedback method](01-recurring-failures.md) or [workspace method](03-preview-workspaces.md). Load the method relevant to the next task rather than making every guide a required step.
