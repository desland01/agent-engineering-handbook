# Give your agent the tool it's missing

Your agent stops halfway through a task. Not because it lacks knowledge — because no tool
it has can do the step. The file exists on a machine it cannot reach; the upload has no
command-line route; the evidence lands where nothing can read it. The answer is to close
that one gap with the smallest useful interface, document it as a skill, and verify the
actual agent can use it.

## The gap Theo hit

Theo's agents could not attach videos to pull requests: GitHub's web UI accepts
drag-and-drop uploads, but the CLI and programmatic PR tools had no equivalent. Theo built a
small file-upload skill backed by Theo's own service on Cloudflare (files.tslop.org), with a
key deployed across Theo's machines, so a machine can upload a file and post the link in the
PR. A SKILL.md is visible on screen at 06:23; full-resolution inspection of that frame
found it names `FILE_HOST_TOKEN`, uses `curl --fail-with-body` over HTTP PUT, and takes
the public URL from the response body.

Two independent pieces of repository evidence support the pattern. Melee
[PR #13](https://github.com/t3dotgg/melee4mac/pull/13) embeds before/after stage
screenshots from that exact host, showing the public host really carries PR evidence —
though the upload service's server code and this PR's invocation logs were not found. And
T3's [PR #10572](https://github.com/pingdotgg/t3code/pull/10572) shows the same shape
inside one product: a desktop-local recording moved through the existing attachment path
so the remote agent can read it.

**Qualification:** the frame inspection describes the skill file's contents only. It does
not prove a real upload succeeded, and it does not establish the service's endpoints or
security model. Theo's service puts an access key on a fleet; any equivalent needs its own
key-handling review, and nothing here authorizes deploying a service.

## Why the small build is worth it now

Theo's separate observation is that authoring and testing a small skill has a tight,
low-stakes feedback loop: assemble a few parts, find out what works, write it up, watch
the agent use it. The cost of a failed iteration is far smaller than the cost of a broken
team environment used to be. That is Theo's experience report, not a measurement.

There is a second half to the lesson, from the T3 investigation: consuming a tool is a
different thing from having it. T3's
[PR #9128](https://github.com/pingdotgg/t3code/pull/9128) fixed a skill picker whose
output worked differently across providers — a skill name appearing in a menu was not
proof the skill was invoked. Verify from the consumer's environment.

## Build only the missing operation

1. Write the gap in one sentence, precisely enough to verify: "agents cannot attach a
   video to a PR they created."
2. Search the existing CLI and API surface before building anything; build only the
   missing piece.
3. Choose the smallest service shape, reusing existing authentication and storage.
4. Write the skill so the agent can use it unaided: when to use it, the exact call, the
   credential-loader name (never the secret value), actual size limits, and a result
   example.
5. Protect the key: scope it to upload-only, distribute per machine, allow rotation, keep
   it out of the repository.
6. Test inside the agent: run the blocked operation through the actual tool route, end to
   end, with no extra hints.

Full procedure, failure modes and the retirement plan are in
[guide 06](../guides/06-tool-adapters.md).

## Let the intended agent use the tool

The acceptance test is the agent completing the blocked step end to end, unaided, through
the real tool route — not the skill existing in a directory. A successful call in a
hand-run terminal proves the command works; it does not prove the agent can find and use
it.

## The upload service was not executed here.

Whether Theo's upload ever succeeded is not established by the evidence. The reward of
skill authoring is a subjective report. And a one-off service with an auth key is a
liability the day the workflow changes — it needs an owner and an end date.

## Sources

<span id="tip-05-custom-file-upload-skill"></span>
**tip-05-custom-file-upload-skill** — [05:52](https://www.youtube.com/watch?v=xmGY276gEFY&t=352s).
Theo. Build small tool adapters for operations the CLI cannot do. Evidence type: Theo
anecdote plus full-resolution frame inspection at 06:23; upload success unproved, service
endpoints and security model unknown beyond the frame.

<span id="tip-06-skill-authoring-reward"></span>
**tip-06-skill-authoring-reward** — [06:30](https://www.youtube.com/watch?v=xmGY276gEFY&t=390s).
Theo. Authoring and testing a small skill has a tight, low-stakes feedback loop. Evidence
type: opinion/subjective experience.

Repository evidence: [Melee PR #13](https://github.com/t3dotgg/melee4mac/pull/13) (open at
inspection) and [T3 PR #10572](https://github.com/pingdotgg/t3code/pull/10572) as recorded in
the original investigations. Related:
[agent-tool-adapters skill](../skills/agent-tool-adapters/SKILL.md). Next:
[Write instructions that change agent behavior](useful-instructions.md).
