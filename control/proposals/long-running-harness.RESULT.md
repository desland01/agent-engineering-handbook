# Authoring result — long-running-harness + Pilot first

Date: 2026-09-10. Owner instruction: readopt the `pilot-first` skill from `~/.agents/skills` so that
"before starting any long-running harness, we do a Pilot First".

**Why a combination, not a new Chart.** The release counts 50 Core skills, the hard maximum.
Pilot First is a process method that applies to every batch shape; `long-running-harness` is
where batch shapes are selected and started, so the rule belongs at the point of dispatch. The
new section sits between the shape table and the execution-shape rule, so it is read before
`tickets-prepare`. If the owner prefers a distinct Chart, one existing Core skill must be
removed with justification (plan.md §6).

**What is preserved.** `pilot-first/SKILL.original.md` is the verbatim source; `pilot-first/eval/`
carries the ablation results, rubric, prompt and analysis script. The section keeps the loop,
the "outside the batch" rule, the stop conditions, the fresh-agent handover and the measured
evidence with its numbers. Dropped: the file:/// links into `~/.claude/skills`, which no longer
resolve, and the `builder-proof` probe reference, which is not part of this release.

**Owner correction, 2026-09-10, folded in.** "The point of Pilot First is not to give up after
they fail on the first try... pilot it, fix what didn't work, pilot it again... Not 'pilot it,
didn't work, okay I'll just do it myself.'" The section now carries: a failed pilot is the
pilot working; fix the machine, not the output; the pilot's defect becomes an executable check
before the batch; one generator builds both plans; piloting the content change is not piloting
the harness. This is the same rule the handbook's own tip-08 states - encode the repeated
correction - applied to the harness.

**Applied today before publication.** The Chart-heading correction across 67 Charts ran a pilot
on the known-bad Chart (`explainer`) with one GLM worker, was reviewed cold, and its procedure
became an input to the two batch workers. Record: `control/reviews/chart-headings.md`.

**Publication.** `skill-publish --proposal <dir> --destination <new release>` with this file as
evidence; not run. Frontmatter `last_verified` should move to 2026-09-10 at publication.
