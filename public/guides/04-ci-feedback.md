# 04 — Let the agent read and resolve CI failures

Use this when you repeatedly carry CI errors from a web page back into an agent prompt. The agent needs the failing run's identity, logs and artifacts, plus the existing authority to repair the branch.

Theo describes that manual loop around [01:53](https://www.youtube.com/watch?v=xmGY276gEFY&t=113s). Boris's post connects infrastructure work to the speed of every agent around [04:51](https://www.youtube.com/watch?v=xmGY276gEFY&t=291s). The Blacksmith segment is sponsored; its advertised prices and speedups were not independently verified. This method needs no particular CI vendor.

## Retrieve the run for the actual revision

With the repository's configured GitHub CLI, list runs for the commit you are investigating. Select the relevant workflow and run attempt; a branch can have several workflows and reruns. Do not assume the latest branch run tested your current checkout.

```bash
REV=$(git rev-parse HEAD)
gh run list --commit "$REV" \
  --json databaseId,headSha,workflowName,status,conclusion,url
# Set RUN_ID to the relevant result, then verify headSha and workflow identity.
gh run view "$RUN_ID" --json headSha,workflowName,status,conclusion,url
# Once the selected run has failed, preserve its failed-step log:
gh run view "$RUN_ID" --log-failed > ci-failed.log
```

These are an implementation example, not commands demonstrated in the video. They use [`gh run list`](https://cli.github.com/manual/gh_run_list) and [`gh run view`](https://cli.github.com/manual/gh_run_view). Keep logs in the task's existing evidence location and exclude secrets from any shared excerpt.

Read the failed step and its causal error block. Retrieve adjacent context or the specific artifact when needed. Keep the original log available: truncating everything to the first few lines can remove the cause, while stuffing an entire build log into each prompt wastes attention.

## Diagnose, repair and check the new revision

Distinguish a product failure, an environment problem and an unstable test. Make the smallest supported repair, run the relevant local check, then push and observe CI when branch delivery is authorized. Match the next run to the new commit before interpreting it. Preserve the initial failure if a retry passes; a green retry does not explain the original failure.

Continue while new evidence supports useful progress within the task's authority and actual provider limits. Do not import arbitrary retry counts from somebody else's automation. If progress requires an unavailable service, credential or unresolved decision, preserve the revision, failed run and diagnosis and state the concrete dependency. A repeated attempt with no changed hypothesis or new evidence is not a repair.

Return the outcome in the current task. Include the revision, run URL, failing check, correction and remaining uncertainty. Write a PR comment only when that external message is covered by the user's request. Use the existing service authorization; this guide does not grant new scopes, spend or recurring runs.

## Verify the loop itself

A useful verification starts with a known failing change in a disposable branch or existing test fixture. The agent retrieves the correct run without a human pasting the error, diagnoses it, and observes the repaired revision. A complete result identifies every required check and any skipped or unavailable checks; a single green badge may aggregate fewer jobs than its name suggests.

For a real example of that last failure, see [Boris's CI inspection](../boris-cherny-inspection.md) and [guide 13](13-layered-validation.md). For a recurring code pattern, move the correction into the smallest applicable check using [guide 01](01-recurring-failures.md). For preview and artifact handling, use [guide 03](03-preview-workspaces.md).
