# You make missing operations usable by agents

When an agent cannot complete one required operation, give it the smallest supported route through that gap. You will learn to define the missing capability, control its effects, and verify the intended agent can use it.

## Name the blocked operation precisely

First confirm the agent understands the task yet lacks an available route for one required operation. Reproduce the failure from the agent's normal environment before deciding a new tool is necessary. <a href="#cite-c0523">Ryan Lopopolo</a> asks which capability is missing and how builders can make it legible and enforceable. Describe the gap as an observable result, because vague frustration cannot define a useful interface. Your statement should name the required effect and the evidence that proves completion.

## Reuse an existing route first

Search the agent's available commands and supported service interfaces before creating another moving part. <a href="#cite-c0547">Anthropic's engineering guide</a> says existing commands use context efficiently when agents interact with external services. Reuse a suitable route when it already exposes the operation and returns enough completion evidence. A new tool is justified only when the demonstrated capability gap remains after that search.

## Make the route fit the action

<a href="#cite-c0176">Boris Cherny</a> advises builders to consider what the model wants to do before shaping its tools. Accept only the inputs needed for that action, and permit only its approved external effect. Return a stable result the agent can inspect after every successful operation. Failures should identify the correctable problem without expanding permissions or exposing secret values.

## Build only the missing interface

When no supported route exists, build only enough interface to perform the named operation reliably. <a href="#cite-c0004">Theo Browne</a> reports building a custom file-upload skill when his workflow lacked that operation. That report establishes the custom tool's purpose without proving a successful upload or complete security design. <a href="#cite-c0530">Kyle</a> describes a small command-line wrapper around the Linear service interface his team already used. These examples support thin wrappers, while leaving each environment's best implementation unresolved.

## Limit credentials and effects

Give the tool only the permissions required for its single approved operation. Load reusable credentials from existing configuration instead of copying secret values into agent instructions. Reject missing authorization, oversized inputs, and unsupported targets with specific errors the agent can correct. Record an owner and retirement condition whenever the tool creates lasting infrastructure. When a native route arrives, migrate callers, verify their results, and remove the temporary tool.

## Test through the agent's real route

Manual success establishes only that the underlying operation worked under your direct control. Run the same task through the intended agent, using its normal environment and available instructions. The agent should find the tool, supply valid inputs, handle its response, and show completion evidence. Also confirm denied or malformed requests stop safely and return guidance the agent can follow. <a href="#cite-c0562">Simon Willison's archive</a> records an agent creating a temporary branch workflow to run the real test battery. That case shows temporary infrastructure can close an environment gap without becoming a permanent dependency. Remove the route after verification when its continued access or maintenance no longer serves the workflow.

## The sources support small, verifiable interfaces

Together, these sources support defining one demonstrated capability gap before choosing the interface that closes it. They favor existing commands or thin wrappers that expose one intended action with controlled effects. The examples describe particular workflows, so they cannot prove one tool design suits every environment. The file-upload report does not establish a successful upload or disclose a complete security model. No cited example authorizes deployment, credential changes, or access beyond your approved task.

<ol id="citations">
<li id="cite-c0004">Theo Browne, video, <a href="https://www.youtube.com/watch?v=xmGY276gEFY&amp;t=375s">A Message for Passionate Devs</a>, at 06:15. "So I ended up building my own custom file upload skill".</li>
<li id="cite-c0176">Boris Cherny, video, <a href="https://www.youtube.com/watch?v=PQU9o_5rHC4&amp;t=1873s">How Anthropic Built Claude Code - Boris Cherny</a>, at 31:13. "think about the thing that the model wants to do".</li>
<li id="cite-c0523">Ryan Lopopolo, blog post, <a href="https://openai.com/index/harness-engineering/#:~:text=what%20capability%20is%20missing%2C%20and%20how%20do%20we%20make%20it%20both%20legible%20and%20enforceable">Harness engineering: leveraging Codex in an agent-first world</a>, at In practice, this meant working depth-first: breaking down. "what capability is missing, and how do we make it both legible and enforceable".</li>
<li id="cite-c0530">Kyle, blog post, <a href="https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents#:~:text=we%20wrote%20a%20small%20CLI%20that%20wraps%20the%20Linear%20API">Skill Issue: Harness Engineering for Coding Agents</a>, at At HumanLayer, we used the Linear MCP server. "we wrote a small CLI that wraps the Linear API".</li>
<li id="cite-c0547">Anthropic, engineering guide, <a href="https://www.anthropic.com/engineering/claude-code-best-practices#:~:text=CLI%20tools%20are%20the%20most%20context-efficient%20way%20to%20interact%20with%20external%20services.">Best practices for Claude Code</a>, at CLI tools are the most context-efficient way. "CLI tools are the most context-efficient way to interact with external services."</li>
<li id="cite-c0562">Simon Willison, tag archive, <a href="https://simonwillison.net/tags/coding-agents/#:~:text=run%20the%20real%20test%20battery%20via%20a%20temporary%20workflow%20on%20this%20branch">Simon Willison on coding-agents</a>, at This Claude Code container: Linux 6.18.5-fc-v20 (itself a. "run the real test battery via a temporary workflow on this branch".</li>
</ol>

<p id="next-action">Write one blocked operation as a verifiable result that names its required effect and completion evidence.</p>
