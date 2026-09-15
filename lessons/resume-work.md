# You resume work without repeating completed steps

After an interruption, you can identify finished work, reuse verified results, and restart only the uncertain stage. You will learn to separate intended work from actual results, measure completeness, and preserve recovery evidence.

## Durable records preserve finished decisions

Work held only in an active conversation can disappear when the process stops or context changes. Write the goal, completed stages, current stage, decisions, and remaining uncertainty into a durable record. Dexter Horthy explains that saved artifacts let teams <a href="#cite-c0089">resume where they stopped</a> without depending on compressed conversation history. Ryan Lopopolo likewise describes <a href="#cite-c0526">execution plans carrying progress and decision logs</a> for complex work. Together, those records show the next worker which decisions remain settled and where uncertainty begins.

## Recipes identify intended work

Before expensive work begins, record the inputs, order, settings, and tools that define the intended result. That recipe can name expected work early, while the produced result remains unavailable for inspection. Greg Kamradt's repository <a href="#cite-c0475">stores the recipe instead of each enormous rendered context</a>, keeping records compact and repeatable. A matching recipe proves that instructions match, although it cannot prove the resulting content matches. Keep recipe identity separate because software changes can produce different results from identical instructions.

## Content identity proves reusable results

After production finishes, create a separate identity from the content that actually exists. Reuse an accepted result only when this content identity matches the candidate you are considering. Kamradt's reconstruction process <a href="#cite-c0476">recreates the exact prior input</a> from its compact recipe without repeating the model run. Exact input reconstruction helps investigation, although it does not prove the earlier response was complete or correct. If exact identity cannot be established, treat reuse as uncertain and perform the authorized work again.

## Completeness decides whether reuse is safe

A successful finish signal cannot establish that the result contains everything your reader or customer needs. Choose a measurable property that exposes truncation, such as duration, item count, or expected coverage. Set any tolerance from your own product evidence, because another system's threshold may hide meaningful loss. Store the measurement beside the result, then confirm that saved evidence still belongs to current content. An equally sized replacement can leave a saved identity stale, so refresh it after outside changes. Reject missing measurements and measured shortfalls, while applying your product's separate rule to extra material.

## Stable names reveal the restart point

Give each workflow, stage, and run a stable name that survives the active process. Record the accepted result and evidence beside that name before moving to the next stage. When an identity is missing, inspect persisted results before deciding whether an authorized restart remains necessary. Never repeat external actions silently, because their effects may survive even when the active process disappears. Stable names connect the durable plan to the exact evidence that justifies resuming after interruption.

## Decide reuse from one fixed snapshot

Build each reuse decision from the last accepted state before the current process begins changing anything. Keep that snapshot unchanged while new results arrive, so every reuse choice shares one reference point. A missing or unreadable completion record should reduce reuse instead of blocking otherwise authorized work. Upload or rebuild unmatched results when allowed, then record the new accepted state for future recovery. If a batch reuse attempt is refused, fall back only to the already authorized individual action. Never widen existing permissions merely because the faster recovery route was refused or unavailable.

## Checkpoints limit repeated work

Save a restart point only after a stage has produced accepted evidence and recorded its identity. Kamradt's runner uses <a href="#cite-c0478">resumption to skip completed cells</a> when an interrupted sweep starts again. Harrison Chase describes checkpoints that let users <a href="#cite-c0488">return to earlier steps and rerun</a> from there. Changing an earlier input invalidates later work that depended on it, even when those stages once passed. Keep independent accepted stages, then rerun only the uncertain stage and anything its changes affect.

## Summary repair stays separate from completed work

Sometimes completed work survives, while its required summary is missing, malformed, or rejected. Preserve the completed effects and their identity, then retry only the summary from the same context. Instructions asking for summary-only recovery express intent, but they cannot prevent available actions from running. Verify that the repair sent no messages, changed no records, and repeated no completed effects. If isolation remains unproven, report the recovery limit before authorizing any wider repetition. Treat accepted results as the source of truth when summaries disagree with completed evidence.

## The sources show durable recovery works

These sources connect durable plans with compact recipes, exact reconstruction, saved restart points, and completed-work skipping. They support reusing verified stages while isolating the smallest uncertain, stale, or failed portion. They do not establish that every stored result is complete, fresh, or safe for automatic reuse.

<ol id="citations"><li id="cite-c0089">Dexter Horthy, video, <a href="https://www.youtube.com/watch?v=YwZR6tc7qYg&amp;t=1586s">From RPI to QRSPI - Lessons Learned Rolling out Research/Plan/Implement to thousands of engineers</a>, at 26:26. "you can always resume from where you left off"</li><li id="cite-c0475">Greg Kamradt, repo, <a href="https://github.com/gkamradt/LLMTest_NeedleInAHaystack#:~:text=We%20don%27t%20store%20the%20rendered%20200k-token%20context%20per%20row">needle-in-a-haystack</a>, at Each row in the JSONL is small (a. "We don't store the rendered 200k-token context per row"</li><li id="cite-c0476">Greg Kamradt, repo, <a href="https://github.com/gkamradt/LLMTest_NeedleInAHaystack#:~:text=produces%20a%20byte-identical%20string%20of%20what%20the%20model%20actually%20saw">needle-in-a-haystack</a>, at niah reconstruct walks the recipe and produces a. "produces a byte-identical string of what the model actually saw"</li><li id="cite-c0478">Greg Kamradt, repo, <a href="https://github.com/gkamradt/LLMTest_NeedleInAHaystack#:~:text=runner%3A%20concurrency%3A%202%20retries%3A%202%20resume%3A%20true">needle-in-a-haystack</a>, at run_name: "uuid-chain-opus" model: "anthropic-opus-4-medium" # resolved. "runner: concurrency: 2 retries: 2 resume: true"</li><li id="cite-c0488">Harrison Chase, blog, <a href="https://blog.langchain.dev/how-to-think-about-agent-frameworks/#:~:text=go%20back%20to%20earlier%20steps%20and%20then%20rerun">How to think about agent frameworks</a>, at Besides allowing the user to affect the agent. "go back to earlier steps and then rerun"</li><li id="cite-c0526">Ryan Lopopolo, blog post, <a href="https://openai.com/index/harness-engineering/#:~:text=complex%20work%20is%20captured%20in%20execution%20plans%20with%20progress%20and%20decision%20logs">Harness engineering: leveraging Codex in an agent-first world</a>, at Plans are treated as first-class artifacts. Ephemeral. "complex work is captured in execution plans with progress and decision logs"</li></ol>

<p id="next-action">Mark the last accepted stage in your current work and attach the evidence needed to reuse it.</p>
