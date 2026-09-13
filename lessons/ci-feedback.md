# Stop babysitting your agent's CI failures

Your agent opens a pull request. CI fails with an error that did not appear locally. You
open the web page, dig the error out of the log, paste it into the agent, wait for another
run, and repeat. That human copy-paste hop is an extra manual handoff in the loop — and it
is removable. Give the agent two abilities: trigger a check run itself, and fetch the
failing portion of the logs itself.

## The loop, and who said it

The observation comes from the video's sponsor segment, read by Theo: agent PR, random CI
failure, human copies the log, agent fixes, human waits again. The sponsor's pitch is that
its CI product closes that loop. The portable idea survives without the product: wherever
a human relays a check failure an agent could have retrieved, that relay is the gap.

**Qualification you should keep:** this is a paid advertisement. Its speed, cost, workload
and falling-failure-rate claims are unverified. Do not choose a vendor from it. Take the
loop shape, not the product.

The video's related point, from Boris's post via Theo, is that shared infrastructure work
speeds up every agent that uses the environment — which is why the relay is worth removing
([Improve the environment your agents work in](better-environments.md)).

## One concrete way to close it

With the repository's configured GitHub CLI, the agent can select the run for the actual
commit and keep only the failed steps:

```bash
REV=$(git rev-parse HEAD)
# List the runs for that revision, then pick the RUN_ID of the run you are
# investigating from the databaseId field of the listing:
gh run list --commit "$REV" \
  --json databaseId,headSha,workflowName,status,conclusion,url
# Replace the placeholder below with the databaseId you picked above:
RUN_ID='REPLACE_WITH_DATABASE_ID'
gh run view "$RUN_ID" --json headSha,workflowName,status,conclusion,url
gh run view "$RUN_ID" --log-failed > ci-failed.log
```

This is an implementation example from [guide 04](../guides/04-ci-feedback.md), not
something demonstrated in the video; it uses the documented
[`gh run list`](https://cli.github.com/manual/gh_run_list) and
[`gh run view`](https://cli.github.com/manual/gh_run_view) commands. Two details matter
more than the commands: match the run to the revision you are actually investigating (a
branch can have several workflows and reruns), and keep the failing-step log rather than
either truncating to a few lines or pasting the whole build log.

## Diagnose the failed run before repairing

Diagnose before repairing: a product failure, an environment problem and an unstable test
have different fixes. Make the smallest supported repair, run the relevant local check,
then push and confirm the next run matches the new commit. Preserve the original failure
if a retry passes — a green retry does not explain the original red. A repeated attempt
with no changed hypothesis is not a repair.

## Check the full feedback loop

Test the loop itself, on a disposable branch with a known failing change. A complete
verification shows the agent retrieving the correct run, diagnosing without a human-pasted
error, and observing the repaired revision. Check what your green badge actually
aggregates: in Boris Cherny's inspected `json-schema-to-typescript`, the aggregate
[`ci-ok` job](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml)
requires success from build, fuzz and output but not from the `bun` and
`engines` matrix jobs it also names — so "all checks" checked less than its name suggests.
Caveat: branch-protection settings for that repository were not inspected, so this finding
shows what the job requires, not what the repository blocks on. Method context:
[guide 13](../guides/13-layered-validation.md) presents the layered-validation
table.

## The sponsor's speed claims remain unverified.

Whether closing this loop makes your team faster is not established by the video; the
sponsor segment contains no verified measurements. The verifiable claim is narrower: the
manual relay is a step, and steps an agent can self-serve remove a handoff.

## Sources

<span id="tip-01-ci-feedback-loop"></span>
**tip-01-ci-feedback-loop** — [01:53](https://www.youtube.com/watch?v=xmGY276gEFY&t=113s).
Sponsor segment (Blacksmith), read by Theo. Agents can trigger CI and read failed logs
without a human relay. Evidence type: sponsor-ad framing. Blacksmith's performance and
cost claims, the ~3,000-jobs-in-7-days figure and falling failure rates are sponsor
claims, unverified; the portable lesson is the loop shape, not the vendor.

Related: [guide 04](../guides/04-ci-feedback.md) for the full method, the
[agent-feedback-engineering skill](../skills/agent-feedback-engineering/SKILL.md) for
turning a known failure into a reusable response. Next:
[Passing tests can still hide broken software](prove-it-works.md).
