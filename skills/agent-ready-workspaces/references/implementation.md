# Workspaces: implementing the missing piece

Theo describes preview environments and agent-visible evidence around [05:10–05:52](https://www.youtube.com/watch?v=xmGY276gEFY&t=310s). The video does not show a complete preview deployment. Apply the idea to the current stack's runner and actual access mechanisms.

## From fresh checkout to first working result

Read the existing bootstrap commands, package scripts and configured launch or setup path. Establish the starting state, dependencies, environment-variable names, data fixtures and expected origin. Use the configured credential delivery mechanism. A developer's populated shell is not proof that an agent starting through a different setup path receives the same inputs.

Fix only the missing steps. Prefer an idempotent existing setup chain. Separate mutable test state across independent workspaces; separate ports alone do not isolate a database or session store. Obtain the actual URL and served revision through a supported lookup rather than assuming a directory or branch name determines them.

## Exercise one meaningful outcome

Use the critical product outcome, not a count of tests. For independent participants, create separate authenticated browser contexts and unique fixture data. Capture evidence at the revision exercised, including dirty changes where relevant.

When using Playwright, configure capture for manually created contexts explicitly. Close every created context even on failure so videos are finalized. Read the project's version and [video options](https://playwright.dev/docs/videos) before assuming successful runs retain footage. Traces expose [actions and state](https://playwright.dev/docs/trace-viewer), but their existence alone does not establish a passing journey.

## Verify selection and delivery

Run the changed setup path through the same entry point future agents will use. Verify the served origin, state isolation and required behavior. If output is produced on another machine, use an existing authorized attachment mechanism and confirm the consumer can read it. A returned desktop-local filename does not give a remote agent access.

Record what is configured versus still manual, and the actual revision tested. Follow the existing lifecycle for temporary environments and retained evidence; this method does not authorize new deployments, recurring cleanup or deletion of shared state.
