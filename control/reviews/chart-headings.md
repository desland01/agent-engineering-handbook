# Review record — Chart heading instructions corrected across the library, 2026-09-10

**Owner instruction.** "The explainer skill makes the same mistake with the headings… Build a
long-running harness and put two GLM agents in it. Send them through all the skill files and
make sure that the instructions are corrected. Have the Opus subagent do the final review. Have
a GLM agent fix these headings real quick as the eval before you send them on their way." And:
readopt Pilot First before any long-running harness.

**Work-list, counted.** 67 Chart bundles in the selected release; 67 `SKILL.md` and 185
reference `.md` files (252 files, 1.28 MB); no symlinks inside the bundles. Split 34 / 33
alphabetically (`halves/half-a.txt`, `half-b.txt`).

## Pilot (Pilot First, riskiest item: the known-bad `explainer` Chart)

**Maker:** glm-5.3-flash, one worker, task `chart-headings/pilot/TASK.md`. **Reviewer:** Fable
5.1, cold, a different route. **Checker:** `chart-headings/checker/check.py`, 14 checks, pass.

- `explainer/SKILL.md`: three sentences corrected — the headline rule ("states the subject" →
  states what the page concludes, with the cover-the-body test), the template rule ("plain
  noun-phrase headings" → each heading a claim its section proves, never a fixed template
  string), and the section-03 required `<h3>` (the fixed string "Why this matters to you" →
  a claim stating why the result matters). Frontmatter and every other line byte-identical.
  Reference file correctly recorded clean.
- The eval half — the page's six headings: rewritten from labels to claims, correctly read
  from each section's own text. Finding: three carried semicolons and ran to ten words,
  against the eight-word, no-semicolon limit. Fixed by the reviewer at integration
  (`~/ephemera/what-changed-today.html`); the procedure handed to the batch carries the
  warning.
- Verdict: one attempt, procedure sound → scale. Procedure: `chart-headings/PROCEDURE.md`.

## Batch (long-running harness)

Recipe `chart-headings/recipe.json` → `tickets-prepare` → `packet/plan.json`, two tickets
`correct-a`, `correct-b`, glm-5.3-flash, `precise` required, each with its half of the
Charts copied and hash-bound as inputs plus RULE.md, PROCEDURE.md and HALF.txt.
Acceptance per ticket: `check.py` against the exact delivered `corrections.json` and `out/`
tree (every bundle and file accounted for; frontmatter and unreported lines byte-identical;
no banned heading instruction survives; no stray output); craft by a different route's
review and a host-authored quality receipt. Owner state and results are appended below.

## Final review route

The owner asked for an Opus subagent. No Opus route exists in the fleet (routes:
glm-5.3-flash, gpt-6-astra, claude-fable-5-1, grok-4.5), native subagents are disabled in
this session, and inventing a model identifier is forbidden. The final review therefore runs
on gpt-6-astra, the route that owns unresolved quality judgment, with the pilot already
reviewed by Fable. If an Opus route is added, the same review capsule reruns on it.

## Publication

Corrected files are proposals. They reach workers only through `skill-publish --proposal DIR
--destination DIR` into a new release with this record as evidence; that step is the
owner's call (plan.md §6).
