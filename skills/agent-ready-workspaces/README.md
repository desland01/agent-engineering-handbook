# Agent-ready workspaces

This skill prepares a repository so a cold-start agent can launch and check a working preview without extra setup guidance. You verify readiness by repeating that same path from a completely fresh start.

## Use it when setup blocks agents

Reach for this skill when cold-start agents repeatedly stall before running or testing your application.
It also helps when parallel work needs isolated previews that agents can open and inspect.
Skip it when you only need a feature changed, a failed check diagnosed, or deployment verified.
An existing workspace that already passes the readiness audit needs no duplicate preparation.

## Give the skill access and priorities

Give the skill repository access, existing ways to run the application, and outcomes your product must preserve.
If priorities remain unstated, the skill infers a small set and explains each choice.
You can override those choices when they miss a consequential product decision.
Use the repository’s existing secret handling, keeping real credentials outside any written setup steps.

## The skill will add only missing pieces

It first inspects the current setup, then adds only the capabilities that your workspace lacks.
The available pieces cover repeatable setup, isolated previews, seeded accounts, critical checks, and revision-linked evidence.
Each manual setup fix becomes a repeatable step inside the repository’s existing setup chain.
Parallel work receives separate mutable state, because separate locations alone cannot isolate databases or sessions.
Required sign-in tests use deterministic accounts managed through the repository’s existing secret handling.
The skill adds a few checks that prove essential outcomes without chasing broad test coverage.
Produced evidence identifies the tested revision, connecting later failures to the change that created them.

## A fresh start proves readiness

Run the changed setup through the same starting point that a future cold-start agent will use.
Confirm the application opens at the expected location with isolated state and required behavior.
An agent can open a local application and test its interface directly, as <a href="#cite-c0194">Boris Cherny and Catherine Wu demonstrate</a>.
Record each piece of evidence beside the tested revision that directly produced it.
Matt Pocock describes placing a video of the working change on its review <a href="#cite-c0252">for direct inspection</a>.
If evidence comes from another machine, confirm the intended agent can actually open it.
Readiness exists only when the added setup and checks pass without interaction.

## The skill stops at workspace preparation

It does not diagnose a failing check, exercise an unrelated feature, or verify a deployment.
Temporary environments follow existing lifecycles, because this skill authorizes no deployment or shared-state deletion.
Configured settings alone cannot prove readiness when the future agent never receives or uses them.
Secrets already available in your current session do not establish that another starting path receives them.
Building every capability wastes effort when a smaller gap already explains the problem.
Checks tied to implementation details become fragile during refactoring and weaken trust.

## The sources show previews need access

The cited practices support access to running software and readable evidence within the skill’s readiness test.
The <a href="#cite-c0194">first example</a> shows an agent launching an application and directly testing its interface.
The <a href="#cite-c0252">second example</a> places a working video where a reviewer can inspect the change.
Neither example proves that your repository’s complete setup is ready for another cold-start agent.

<ol id="citations"><li id="cite-c0194">Boris Cherny and Catherine Wu, video, <a href="https://www.youtube.com/watch?v=Hth_tLaC2j8&amp;t=177s">Reflecting on a year of Claude Code</a>, at 02:57. "Claude actually spins up a local desktop app and it uses computer use"</li><li id="cite-c0252">Matt Pocock, video, <a href="https://www.youtube.com/watch?v=nQwJVHCtDDY&amp;t=2020s">Building AI Coding Agents with Matt Pocock</a>, at 33:40. "you just have a video on the PR of the thing working."</li></ol>

<p id="next-action">Run this skill on one repository where a cold-start agent still cannot reach a verified working state.</p>
