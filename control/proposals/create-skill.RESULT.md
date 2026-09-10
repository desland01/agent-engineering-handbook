# Authoring result — create-skill, instructing for results and for craft

Date: 2026-09-10. Owner instruction: "update the skills — pilot first and long-running
harness. Write in a way that would have prevented the mistake from happening... Also update
precise... And the create-skill skill."

**What is added.** Two sections after the visual-design rule: "Instruct for the result, not the
shape of the result" and "Methods for work no check can settle". Nothing existing is changed;
frontmatter untouched.

**The failures each section prevents, all observed today.**

- The `explainer` Chart said "plain noun-phrase headings, in this order" and named a fixed
  `<h3>` string. It produced four label headings and one pasted string on a real page. One of
  those headings, "Repeated fixes spend tokens", read to the owner as the reverse of its
  section. The instruction was copied faithfully; the instruction was the defect.
- The earlier idea-page assignment said "two to five words naming the subject" and produced 72
  label headings across 19 pages, for the same reason.
- An example heading written inside the corrected instruction ran to ten words with a
  semicolon — the instruction broke the rule it was teaching, and that version was the one
  copied.
- The craft section carries the role-first standard (`control/design-skill-standard.md`,
  gpt-taste) and the separation of executable acceptance from judged acceptance, so that a
  method stops implying a check decides what only a reviewer can.

**What is deliberately not added.** No review stage, benchmark or trigger test: the existing
body already refuses those for an ordinary instruction edit, and the owner's standing rule is
no extra approval stages.

**Checks.** Instruction-only change: compared against the owner's requirement and the existing
body; the failures cited are recorded in `control/reviews/chart-headings.md`,
`control/reviews/headings.md` and the site's own idea pages. Not published.
