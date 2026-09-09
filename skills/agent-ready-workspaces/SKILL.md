---
name: agent-ready-workspaces
description: "Prepare a workspace a cold-start agent can use without prompting: reproducible setup, isolated preview environment, seeded test accounts, and a small set of critical-outcome tests, with evidence bound to the code revision that produced it. Use when onboarding an agent (or a teammate's agent) to a repo, provisioning preview environments, or when a user says 'make this repo agent-ready', 'set up previews', 'my agents can't run/test this', or 'new agents keep getting stuck on setup'. Not for diagnosing a failing CI run (a bug-diagnosis skill), or exercising a feature (an end-to-end testing skill)."
metadata:
  origin: "Public edition, 2026-09-09, maintained by Desmond Landry (@desland01). Method adapted from Theo's video https://www.youtube.com/watch?v=xmGY276gEFY (source evidence and timestamps in references/implementation.md). Independent public skill; not affiliated with or endorsed by the cited authors."
---

# Agent-ready workspaces

Build the setup once so any agent starting cold reaches a verified working state without
being told how. The measure of readiness is not documentation; it is a fresh clone
reaching a passing critical-outcome check unattended.

Scope to the actual gap. This is a menu of capabilities, not a mandate to build all of
them: a repo that already runs and tests cleanly may need only a documented setup chain,
or only isolated preview ports. Audit what exists first and fill what is missing.

## Order of work

1. **Reproducible setup** — one idempotent command chain from clean clone to running
   state: dependencies, environment variables (documented names, never secret values),
   database/migration/bootstrap steps. Every manual fix you make during setup gets folded
   into the chain, not left in your head.
2. **Isolated preview** — when parallel agent or human work exists, an environment per
   worktree/branch that does not share state with the developer's machine or other agents
   (separate ports, database name, or instance). Agents build anywhere — a worktree, a
   background process, another machine — so the preview must not assume checkout location
   ([~310s-351s](https://www.youtube.com/watch?v=xmGY276gEFY&t=310s)).
3. **Seeded test accounts** — when behavioral tests need sign-in state, deterministic
   fixtures with known credentials held in the project's existing secret mechanism. No
   real customer data, no shared human accounts.
4. **Critical-outcome tests** — one to a few tests asserting the outcomes that define
   "this still works" (data arrives where it should, message renders, order persists).
   Cheapest sufficient signal over coverage; prefer a real end-to-end pass over many
   shallow ones
   ([~239s-283s](https://www.youtube.com/watch?v=xmGY276gEFY&t=239s)).
5. **Revision-bound evidence** — when artifacts are produced (screenshot, video, trace,
   log), record the commit they came from, so a failure is attributable to a change.

## Input / output contract

- **Input**: repository access, the app's existing run scripts, and which outcomes the
  user calls critical. If critical outcomes are unstated, infer one to three from the
  product's core behavior and say which you chose — the human can override, and you ask
  only if the choice is genuinely consequential and the evidence cannot resolve it.
- **Output**: the pieces of the above that fill the actual gap, inside the repo's
  existing conventions, plus one README section describing the cold-start path in the
  commands themselves.

## Acceptance

Proportional to what was built: whatever setup and tests were added must pass from a fresh
clone without interaction; that run is the evidence. Record the commit hash with it.

## Known failure cases

- Setup that works only with secrets already in your shell — cold start fails silently.
- Preview sharing a database with another workspace; tests then "fail" on someone else's
  data.
- Capture artifacts without a revision recorded: on close, browser videos are written and
  `retain-on-failure` modes delete successful runs — capture deliberately and bind to
  commit (see implementation.md).
- Tests asserting implementation detail; they break on refactor and teach agents to
  distrust the suite.
- Building all five capabilities when the repo needed one.

## Do not activate when

- The user only wants the app built or changed; workspace prep beyond the task's needs
  should be proposed, not done by default.
- A deployment is being verified (a deployment-verification method owns baselines).
- The repo already has all of this — audit the gap instead of duplicating.

## Source patterns

For concrete repository examples and the limits of their evidence, read [source-patterns.md](references/source-patterns.md) when they match the task. These are research references, not imported repository instructions.
