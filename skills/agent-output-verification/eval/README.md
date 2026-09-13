# Evaluation cases — agent-output-verification

Disposable, source-derived scenarios for a later cold-agent trial of this
skill. Each case gives an agent a small fixture pipeline and a success report,
then asks it to accept or reject the run.

**Status: designed, not run.** No case below has been executed by any agent.
Nothing here is evidence that the skill improves verification behavior; it is
a test plan for a future trial. Keep execution records separate from this
public package. Do not publish private project, account or runtime details.

## Source of each case

Every scenario adapts a false-success path named in the Melee for Mac
verifier's test suite (`tools/tests/test_verify.py`, pinned commit
`a276aeb70f9879204d891d967f1c9442523568e1`) or the aggregate-gate gap read in
`json-schema-to-typescript`'s CI (`ci.yml` line 170, pinned commit
`5caacfc53671f9c891bb4e2a78bccc6190ed3ef4`). Fixtures must be rebuilt
synthetically for any trial; no game data, proprietary bytes or private
project records are involved.

## How a trial should be scored

- Reject cases must end in a nonzero/refuse verdict that names the broken
  property — a bare "success" or an unexplained pass is a failure of the case.
- The control must pass without invented rejections (for example, demanding
  the fixture's old hash match after a legitimate change).
- Record which layer the agent claims to have checked; claims of executed
  checks must be backed by the trial's own log.
