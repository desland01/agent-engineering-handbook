---
name: pilot-first
description: Prove a repeated change on one item before running it across a batch. Use when the task names many items (25 skills, all location pages, every client record, a migration, a sweep, a rename across repos) or when you are about to write a loop over a work-list.
lifecycle:
  origin: "2026-08-15, owner directive, after 25 ablated skills were restored in one bulk pass and cost six pr-review blocks plus one near-destructive restore."
  class: process
  last_verified: 2026-08-15
  eval: "ablation 2026-08-15 run 2, 40 arms on the hard fixture, rubric declared before running, scored on what the agent DID. Blind controls damaged the protected branch in 8 of 20; with the skill loaded, 0 of 20. Fisher exact two-tailed p = 0.0033. All 20 controls detected the symlink, so the effect is not detection, it is what the agent does after detecting it. Both sides migrated 11 of 11 real services, so the skill costs nothing in throughput. Run 1 (2 of 8 vs 0 of 8, p ~= 0.47) is superseded. Blind arms require build_blind_sandbox.sh, because worker configs symlink the live farm."
  eval_artifacts: "/Users/thebeast/.claude/skills/pilot-first/eval/{RESULTS-20260815-run2.txt,RUBRIC.txt,PROMPT.txt,run_ablation.sh,analyze.py,build_fixture_worktree.py,origin-incident-t10.md}"
  probe: "pilot-first-shared-file in /Users/thebeast/builder-proof/evals/tasks.json"
  sunset: "retire when batch changes are always proven on one item by a harness gate that agents cannot skip"
  boundary:
    producer: "an agent about to apply the same change across a multi-item work-list"
    consumer: "the protected repositories and live skill farm, which take bulk damage if the agent scales before one item is proven"

---

# Pilot first, then scale

Never apply the same change to a batch until one item has gone end to end.

## The loop

1. **Count the work-list yourself.** Do not trust a supplied list. Scan for the real set.
2. **Pick the riskiest item, not the easiest.** Riskiest means indirection: a symlink, a
   pointer, a git worktree, a gitignored path, or an item whose repo carries its own rules file.
3. **Read that repo's own contract before editing:** `AGENTS.md`, `CLAUDE.md`, `.claude/rules/*`.
   It decides what a valid commit looks like here, and whether you may commit at all.
4. **Change that one item.**
5. **Verify by diff, before you commit** (see below). Verification after a commit is a
   post-mortem, not a gate.
6. **Then commit and run the gate**, if step 3 established you are the one who commits in this
   repo. Where the contract reserves commits to the owner, stop here and report instead.
7. **Write the procedure that worked into a TMP file** as you go.
8. **Only then scale**, using a workflow rather than by hand.

## Pilot the machine, not only the change

Proving the change on one item does not prove the machinery that will carry it to the rest. If
the batch runs through a harness, a controller, a queue or a script, run one small job through
that whole path first — dispatch, check, accept — and require it to reach the accepted state.
A worker that delivered, a checker that never ran and a job left running are three different
states, and only the last one is finished. Build the pilot job and the batch job from one
generator with an id argument, so the machine you proved is the machine that runs.

## A failed pilot is the pilot working

Fix what failed **in the machine** — the task text, the check, the workspace layout, the
permissions — and pilot again. Never repair the pilot's output by hand and scale anyway: a
defect you corrected yourself is a defect the batch reproduces on every remaining item. Where
the defect is mechanically detectable it becomes a check before the batch runs, and that check
is proved to refuse the exact bad output before it is trusted. Where it is not, name it in the
task text and in the judged acceptance. Repeat the pilot after each fix. The pilot is done
when it needs no intervention, not when you are tired of it.

> Measured, 2026-09-10. A 67-item Chart correction was launched without piloting its harness.
> Five construction faults refused every attempt in turn: a workspace inside the runtime's
> installation home; capsules with empty required charts, tools or declared outputs; a tool set
> outside the anchor set; a worker input read from the checker's own workspace; a checker whose
> argv named the files the check itself creates, so the environment digest changed between
> freeze and verify; and a relocated plan reusing its old id. A two-item pilot surfaces all of
> them in one pass, and each was invisible until a plan was actually dispatched.

## An item that resolves outside the batch is not in the batch

Resolve every item to its real path before you edit it. If it lands outside the repo or tree
the batch is scoped to, **it is not yours to change.** Leave it, record it, finish the rest, and
report it at the end.

Editing it "from the other side" is the same edit. Committing the change in the owning repo
instead does not make it authorized, and neither does the batch task saying "every" or "all".
A shared file has other readers who did not ask for your change.

> Measured, 2026-08-15, 20 blind agents. Each got 12 service configs to migrate. One resolved
> into a linked git worktree of the same repo on another branch, with no README and no warning.
> **All 20 found the symlink and named it. 8 of them edited through it anyway**, and 2 of those
> committed onto the other branch. Every one reported "stopped on: nothing" and high confidence.
> Finding the indirection is not the hard part, because the model already does that every time.
> Without this section the agent rationalizes the edit after resolving it correctly.

## Verify by diff, not by memory

Every agent that damaged the protected branch above also reported "stopped on: nothing" and high
confidence. Two of them listed the second branch and the second commit hash in the same breath.
The self-report describes the mechanism accurately and still gets the authorisation wrong.

Before you call a pilot clean, check what actually moved:

- `git status` in **every** repo you touched, not just the one you targeted.
- If a new commit exists in a repo that was not the batch target, the pilot failed. Stop.
- Diff the item against its committed state. A change with no diff, or a diff you cannot
  explain, means you do not yet understand the procedure well enough to run it 24 more times.

## Stop conditions

- The pilot needed more than one attempt → fix the procedure, re-pilot, do not scale.
- The pilot touched a file outside the item you targeted → stop and report.
- The real work-list count differs from the supplied one → re-scope before piloting.

## Then hand it to a fresh agent

Give the TMP procedure to an agent with no memory of the session that wrote it. Watch where it
stalls, retries, or goes astray. Add an instruction **only at those exact points**. An
instruction you added because it felt prudent is untested weight.

## Provenance

Written 2026-08-15 after restoring 25 ablated skills in one bulk pass. Six independent
`pr-review` blocks followed, and one restore would have destroyed a skill body by committing a
self-referential pointer inside a linked git worktree. Full record:
[origin-incident-t10.md](file:///Users/thebeast/.claude/skills/pilot-first/eval/origin-incident-t10.md).

Evaluated by ablation, 40 arms, scored on what the agent DID and never on what it reported.

| | Damaged the protected branch |
|---|---|
| blind control | **8 of 20** |
| this skill loaded | 0 of 20 |

Fisher exact, two-tailed: **p = 0.0033**. Both sides migrated 11 of 11 real services, so no arm
passed by refusing the work, and the skill costs nothing in throughput.
[RESULTS-20260815-run2.txt](file:///Users/thebeast/.claude/skills/pilot-first/eval/RESULTS-20260815-run2.txt)
carries the full read.
[RESULTS-20260815.txt](file:///Users/thebeast/.claude/skills/pilot-first/eval/RESULTS-20260815.txt)
is the superseded first run, which was underpowered at n=8 per side.

Version 1 failed outright: the agent found the symlink AND read the owning project's README,
then committed the change in the other repo and reported success. The two sections above exist
because of that measured failure, not because they sounded prudent.

Two things this eval taught that generalise:

- **An easy probe cannot measure judgement.** The first fixture guarded its trap with a README
  shouting "NEVER modify this". Blind controls solved it 4 of 4. Only
  [build_fixture_worktree.py](file:///Users/thebeast/.claude/skills/pilot-first/eval/build_fixture_worktree.py),
  where the trap is an unmarked linked git worktree, produced control failures.
- **A worker is not a blind control once the skill is on disk.** Every
  `~/.claude-*-worker/skills` symlinks the live farm. Use
  [build_blind_sandbox.sh](file:///Users/thebeast/.claude/skills/pilot-first/eval/build_blind_sandbox.sh),
  which overrides `HOME` so the worker loads a farm missing exactly one skill.
- **Score the action, not the observation.** Controls detected the trap 20 of 20 times and
  still damaged the branch 8 of those times. An ablation that had scored "did it notice?"
  would have measured no effect at all and retired a skill worth p = 0.0033.

Re-verify with the probe `pilot-first-shared-file` in
[tasks.json](file:///Users/thebeast/builder-proof/evals/tasks.json). It builds the same
linked-worktree trap and scores `git_untouched` on the other checkout, so it measures the
action and not whether the agent named the symlink.
