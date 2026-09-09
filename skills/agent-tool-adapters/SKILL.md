---
name: agent-tool-adapters
description: "Bridge a proven missing agent capability with the smallest working machine-readable interface plus an on-demand skill describing it — reusing existing transports, accounts, evidence storage and authority, and proving the agent can actually use it. Use when an agent demonstrably cannot do something the task needs (e.g. attach a binary to a PR), the user asks to build a tool/integration/skill for agents, or says 'give the agents a way to X'. Not for one-off script requests, adopting external services from advertising, or general workspace setup (agent-ready-workspaces, the sibling skill in this handbook)."
metadata:
  origin: "Public edition, 2026-09-09, maintained by Desmond Landry (@desland01). Method adapted from Theo's video https://www.youtube.com/watch?v=xmGY276gEFY (source evidence and timestamps in references/implementation.md). Independent public skill; not affiliated with or endorsed by the cited authors."
---

# Tool adapters

When an agent hits a real wall, close the gap with the smallest interface that removes it
— then write it up as a skill so other agents can find and use it, and test it inside an
agent before calling it done
([~352s-408s](https://www.youtube.com/watch?v=xmGY276gEFY&t=352s)).

Scale to the need: a small script in the repo can be the whole adapter for a recurring
useful capability. An adapter plus skill is the form for a capability other agents,
sessions, or repos will need; a one-off script is the form for this task only. Neither
form carries a quota — build when the capability is useful, not to hit a count.

## Gate: prove the gap first

Record the failed attempt, or establish the missing capability from the current interfaces and the user's requested task. Identify what is absent and why the available tools cannot supply it. An explicit request for a new capability does not need a contrived failure first.

## Reuse before building

In order: an existing CLI flag, an existing API route or MCP tool, an internal service
already paid for and authorized, a documented capability of the current harness. Build
new surface only when no existing transport can carry it. Reuse, likewise: existing
accounts and credentials (via the project's secret mechanism — never new credentials
without authorization), existing storage for evidence, and the authority boundary
already granted to the task.

## Minimal interface

- One operation per real need; no speculative options, no generic "do anything" endpoint.
- Machine-readable success and failure (exit codes, JSON status), so an agent can branch
  on the result instead of parsing prose.
- Explicit input limits (size, type, timeout) enforced by the adapter, not by agent care.
- Deployed only where the task's authority already reaches; if it needs a new external
  service, account, spend or other consequential external effect beyond existing authorization, make the proposed change concrete and request only the missing authorization. Do not ask again for an already authorized action.

## Write the skill

The skill documents the contract, not the implementation: when to use it, the command or
call, input/output examples with real values, failure modes and their meanings, and the
boundary (what it must not be used for). Keep it on-demand: description triggers on the
capability's task, not on every coding request.

## Test inside an agent

For an adapter meant to be reused, the acceptance test is an agent doing the blocked task
end to end ([~397s-408s](https://www.youtube.com/watch?v=xmGY276gEFY&t=397s)): a cold
agent, given only the skill, completes the previously impossible step. Also verify one
realistic failure path produces a readable error. Without that run, the status is "built,
unproven". A task-scoped script needs one successful run and one failure run of its own,
not a full in-agent trial.

## Input / output contract

- **Input**: the recorded failed attempts, the target capability, and access to the
  existing transport/account the adapter will reuse.
- **Output**: the adapter (script or service, at the scale the need warrants, with deploy
  state as authorized), a skill documenting it when reuse across tasks is expected, the
  test result, and one line recording which existing account/transport it rides on.

## Acceptance

Proportional: a thin CLI wrapper needs one successful end-to-end run plus one failure
run; a service with stored state needs both plus a note on where evidence lands and who
can delete it.

## Known failure cases

- Interface built before the gap is proven; ends up unused.
- Skill documents happy path only; agents then iterate blindly on the first error.
- Agent parses human-formatted output; breaks on the next format tweak — return
  structured results.
- Adapter silently exceeds its authority (new outbound endpoint, new account, customer
  data moved into shared storage).

## Do not activate when

- A single throwaway in this task would do and no reuse is expected.
- The ask is to adopt a product because an advertisement recommended it — verify the
  capability against the project's own needs first.
- The missing piece is context or setup, not capability (see agent-context-calibration
  and agent-ready-workspaces, the sibling skill in this handbook).

## Source patterns

For concrete repository examples and the limits of their evidence, read [source-patterns.md](references/source-patterns.md) when they match the task. These are research references, not imported repository instructions.
