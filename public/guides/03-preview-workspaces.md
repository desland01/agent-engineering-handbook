# 03 — Make previews usable from the agent's environment

Use this when work happens in several worktrees or machines and a person or agent needs to inspect the actual change. Theo explains why previews become more valuable around [05:10–05:52](https://www.youtube.com/watch?v=xmGY276gEFY&t=310s). The video narrates the practice; it does not demonstrate a complete preview setup.

## Connect a revision to a reachable environment

Reuse the project's existing local runner or preview platform. Provide a supported way to obtain the preview URL and deployed revision from a branch, worktree or build record. A predictable URL can help, but a reliable lookup is sufficient; not every platform derives its URL from the branch name.

Record the checkout revision, dirty changes when relevant, origin, state directory and test-data identity. Verify the served revision before interpreting a result. Prefer a health endpoint or build record to placing implementation details in the product's customer interface.

Make state isolation explicit. Separate ports alone do not isolate a shared database, session store or output directory. Give independent workspaces separate test state where their tests mutate it. Reuse deterministic fixtures so a reviewer can reproduce the failure.

## Make the real flow testable

An agent must be able to reach the origin, authenticate through the supported test-account mechanism and exercise the critical outcome. Access protection stays in place. Robot exclusion is not authentication, and a browser's successful navigation does not prove the application's main behavior works.

Use [guide 02](02-critical-journey-tests.md) for a sender/recipient example. Preserve a useful failure trace or recording, the failing assertion and the revision that produced them. If an artifact was created on a different machine, transfer it through the existing authorized attachment path and verify that the intended consumer can read it.

For an authorized PR delivery, include the preview URL and evidence in its review material. Otherwise return them in the current task. Creating a preview or posting a comment remains subject to the task's existing authorization; this guide does not create deployments or messages by itself.

## Define lifecycle using the existing platform

Name the owner of temporary state and its retention policy. Use the platform's authorized cleanup mechanism after evidence retention and recovery needs are met. Do not add a recurring deletion job or delete somebody's shared environment merely to follow an example. A local disposable worktree may need only ordinary task cleanup.

A complete implementation lets a fresh authorized agent obtain the right URL, observe the correct revision, run the required journey and return readable evidence. Record any infrastructure that remains manually configured or not yet automated.

## Concrete public examples

T3's [PR #5586](https://github.com/pingdotgg/t3code/pull/5586) repairs inherited launcher variables and conflicting setup instructions. [PR #10501](https://github.com/pingdotgg/t3code/pull/10501) records that a setup recipe existed but had not been imported into a saved project. [PR #10572](https://github.com/pingdotgg/t3code/pull/10572) moves a desktop recording into the environment where the agent can read it. These are distinct failure modes: wrong environment, unselected configuration and inaccessible output.

See [the source inspection](../github-inspection.md) for the pinned files, dates and limits of these observations. Use [guide 04](04-ci-feedback.md) to connect failed checks to the same revision and [guide 06](06-tool-adapters.md) only if an existing tool cannot deliver the needed evidence.
