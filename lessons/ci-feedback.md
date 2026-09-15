# You diagnose failed checks without copying logs

Give your agent direct access to the failed check, then make it diagnose before changing anything. You can verify the repair by matching both results to the revisions they actually tested.

## Direct access removes the relay

Manual copying separates the failure from the revision, run, and surrounding evidence that produced it. Mitchell Hashimoto described frustration with copying command output between tools during work on existing projects <a href="#cite-c0369">in his account</a>. That transfer can omit context, preserve stale excerpts, or introduce accidental changes before diagnosis begins. Theo Browne proposes letting the agent trigger the check, retrieve logs, and repair directly <a href="#cite-c0001">in his example</a>. His example supports the feedback loop, without independently proving any vendor's speed or cost claims.

## Run identity keeps evidence attached

Record the tested revision, check name, attempt, and result before interpreting any failure. A branch can contain several revisions and repeated attempts, so the newest result may test different work. Keep the original failed output available, then focus first on the causal error and nearby context. Retrieve more surrounding evidence only when the initial output cannot explain what failed or where. An unchanged successful retry leaves the first failure unexplained, even when the latest result appears healthy.

## Readable evidence sharpens the diagnosis

Boris demonstrates sending a large raw log directly into the agent for analysis <a href="#cite-c0211">during his demonstration</a>. Direct access preserves more context than selected excerpts, especially when the cause appears before the final error. Repeatedly reading every line can bury useful evidence and consume the attention needed for diagnosis. Keep the complete output available, then inspect the failed step, causal block, and nearby context first. Next.js forwards browser failures into agent-readable development output, extending direct feedback to client-side problems <a href="#cite-c0346">in its guidance</a>.

## Diagnosis determines the next move

Classify the evidence before editing as a product defect, environment failure, unstable check, or unavailable dependency. Each class needs a different response, because changing product code cannot repair every failed environment. Choose the smallest supported change that addresses the observed cause within your existing authority. If diagnosis needs unavailable credentials, services, or permissions, preserve the evidence and name the unresolved dependency. A repeated attempt without changed evidence or a new hypothesis only repeats the same uncertainty.

## The repaired revision must prove itself

Run the narrowest relevant check nearby when available, then observe the authorized shared check. Confirm that the successful result tested the repaired revision rather than an earlier or later change. Compare the original failure with the new result, showing how the correction addresses the diagnosed cause. If an unchanged retry passes, record the instability because the first failure remains unexplained. A complete result names the tested revision, failed check, diagnosis, correction, verification, and remaining uncertainty.

## The sources show agents receive failures

Together, these sources support direct access to check output while leaving diagnosis and verification as separate responsibilities. <a href="#cite-c0001">Theo Browne</a> and <a href="#cite-c0211">Boris</a> show agents receiving check output directly, without requiring a human relay. <a href="#cite-c0346">Next.js</a> extends that visibility to browser failures, while <a href="#cite-c0369">Mitchell Hashimoto</a> identifies manual transfer as practical friction. These sources do not establish that every failure is repairable, or that unrestricted retries are safe.

<ol id="citations"><li id="cite-c0001">Theo Browne, video, <a href="https://www.youtube.com/watch?v=xmGY276gEFY&amp;t=133s">A Message for Passionate Devs</a>, at 02:13. "your agent could trigger it directly, get the logs, and fix things yourself"</li><li id="cite-c0211">Boris, video, <a href="https://www.youtube.com/watch?v=kNByBNS5mS8&amp;t=1326s">Practical Tips and Tricks for Claude Code</a>, at 22:06. "read, you know, like a giant log and pipe it in"</li><li id="cite-c0346">Next.js, docs, <a href="https://nextjs.org/docs/app/guides/ai-agents#:~:text=carries%20the%20client-side%20failures%20they%27re%20asked%20to%20fix">Guides: AI Coding Agents | Next.js</a>, at First, next dev forwards browser console errors and. "carries the client-side failures they're asked to fix."</li><li id="cite-c0369">Mitchell Hashimoto, blog, <a href="https://mitchellh.com/writing/my-ai-adoption-journey#:~:text=frustrated%20copying%20and%20pasting%20code%20and%20command%20output">My AI Adoption Journey</a>, at In the context of brownfield projects, I found. "frustrated copying and pasting code and command output"</li></ol>

<p id="next-action">Give your agent direct access to the complete original output from one failed check.</p>
