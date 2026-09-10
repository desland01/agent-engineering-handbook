# Authoring result — precise, craft caveat

Date: 2026-09-10. Owner instruction: "update precise to include the caveat about how we should
be writing design skills or things that are harder to mechanically verify."

**What is added.** One section, "Precision about work that no check can settle", between the
core conventions and "Carry unfinished work forward". Nothing existing is changed; frontmatter
untouched.

**Why each line is there, from measured failures today.**

- *No invented thresholds.* The design language's numeric values are real measurements read
  from live CSS; the temptation is to invent similar-looking numbers for quality. Rejected.
- *Name both acceptances.* The Chart-heading harness passes an executable checker that proves
  coverage, byte-identity and banned phrasing, and cannot decide whether a rewritten sentence
  is good. That judgment is a named route, not a hidden assumption inside the checker.
- *Defaults, variance, worked examples.* Carried from the role-first design standard
  (`control/design-skill-standard.md`) and gpt-taste, which the owner named as the model.
- *A judged acceptance names its judge.* The design review gate in `ARCHITECT.md`.
- *Encode a recurring correction as a proved check.* The site's own tip-08, and the failure the
  owner caught today: the same heading defect corrected by hand twice instead of once as a check.
- *The instruction is not the output; a heading states its claim.* Both `ARCHITECT.md` rules,
  restated here because they are precision requirements on model-facing text.
- *Facts, not register.* The owner's ruling of 2026-09-10: precision governs what a design
  skill asserts, never how it addresses the model.

**Checks.** Instruction-only change: compared against the owner's requirement and the existing
body. No behavioural check applies. Not published; `skill-publish --proposal DIR --destination
DIR` with this file as evidence remains the owner's call.
