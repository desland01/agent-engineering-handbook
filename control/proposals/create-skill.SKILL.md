---
name: create-skill
description: "Create or revise a Nautilus skill, wrapper or skill description, or answer an Agent Skills format question. Use for /create-skill and explicit skill-authoring or packaging work."
user-invocable: true
argument-hint: [skill-name]
metadata:
  origin: "Claude Code skill-authoring guide, rebuilt on the agentskills.io standard 2026-08-26 and consolidated with its local mirror under this name; rewritten as a native Nautilus Chart 2026-09-05"
  standard-mirrored: "2026-08-26"
---

# Create or revise a Nautilus skill

Use [precise](../precise/SKILL.md) for model-facing text and
[simple](../simple/SKILL.md) for the human-facing result. Current user instructions determine
this revision's scope; a skill cannot grant authority or turn an example into a requirement.

Keep knowledge the model lacks: business decisions, actual tool contracts, non-obvious
failure modes, useful craft distinctions and explicitly selected workflows. Remove generic
training and repeated rules already supplied by the platform or project. Preserve uncertain
expertise inactive with its original provenance instead of silently discarding it.

Keep one coherent purpose per skill. The description states the actual task trigger; a common
word such as accuracy, testing or audit is insufficient by itself. Put tool details and
conditional methods in references with an explicit load condition. Load the relevant method,
not the whole catalog. Do not prescribe a model review, trigger benchmark or test loop for an
ordinary instruction edit.

For rewrites, preserve exact originals and provenance through the existing release process.
Keep name, directory, user-invocation settings and argument fields compatible. Identify each
narrowed trigger in the human report. Retain supporting files and useful craft guidance. Do
not edit a third-party original; Nautilus adaptations and explicitly authorized wrappers have
their own controlled authoring path. An unresolved source or permission problem blocks only
its dependent work.

Visual-design methods retain the owner rule: no eyebrow headings, decorative overlines,
small uppercase kickers or duplicate labels above the main heading. Useful field labels,
navigation and honest task status remain.

## Instruct for the result, not the shape of the result

An instruction is copied. Whatever shape it names, the work comes back in that shape, so name
the property the result must have and never a template the writer can paste.

- Instruct for a claim, never a subject. "Name the subject in two to five words" returns
  labels: a label carries no claim, so the reader supplies one, sometimes the opposite one.
  Ask for what the section concludes, in a reader's words, and ship the test with the
  instruction: cover the body, read the heading, write what it must claim; a different or
  opposite reading fails. This applies to every heading, title, caption, section name and
  example an instruction produces, including examples written inside the instruction itself.
- A fixed string in a template is a label. A required-sections table names each section's
  order and required elements; it does not hand over the words.
- The instruction is not the output. A field name, a schema key, a rule's own wording and this
  method's phrasing never appear in the work as a heading, a label or a sentence.
- Any example you write inside an instruction obeys the rule it teaches. An example that
  breaks its own rule is the version that gets copied.

## Methods for work no check can settle

Design, composition, prose and taste have no measurement that decides them. Write those
methods to change behaviour, and be honest about what remains judged:

- Open in a role, name the defaults the model falls into in that domain so it recognises them
  in its own output, and require a forced-variance commitment before any work starts. Neutral
  specification prose does not break a default. `precise` governs what such a method asserts,
  never its register.
- Give short absolute bans with their reasons, and worked examples of a right and a wrong
  result. Adjectives — premium, clean, modern — carry no requirement.
- Separate the acceptances and name both: what a check decides, and which route decides the
  rest from rendered evidence. Never invent a number that looks mechanical and measures
  nothing.
- Where a defect can be detected mechanically, ship the check with the method and prove it
  refuses that exact defect before trusting it. A correction that keeps returning by hand is
  an unwritten check. Where it cannot, say so in the method rather than implying coverage.
- A revision earns its way in from an observed failure. Record the failure the sentence
  prevents; an instruction added because it felt prudent is untested weight.

Before deciding a new skill is needed for an observed context failure, identify the actual
missing fact or decision and pick its carrier: a local comment, a type, the glossary, an
existing skill's conditional reference, or grounded owner instructions; root instruction
files carry judgment, not file inventories. Use a
low-extra-context probe only for real diagnostic uncertainty, preserving standing
instructions and admitted tools; never invent a rule or discard expertise over one
inconclusive probe. Each category targets 35 active skills with a hard maximum of 50; Core
and domain are counted separately and neither borrows places from the other. While places
remain between 35 and 50, a distinct new skill must justify why extending an existing skill
cannot serve its purpose. At the cap, combine the expertise into an existing skill or
justify retiring an unneeded one as its replacement, retaining originals — uniqueness alone
admits no further skill, and categories are classified by purpose without relabeling to
evade the cap. See [references/knowledge-carriers.md](references/knowledge-carriers.md).

Select references when needed:

- Format/frontmatter/layout: [specification](references/specification.md).
- Content selection: [best practices](references/best-practices.md).
- Trigger changes: [descriptions](references/optimizing-descriptions.md). Its suggested
  experiments are optional research methods, not required authoring stages.
- Bundled tools: [scripts](references/using-scripts.md); repeated successful workflows:
  [fixture extraction](references/script-fixture-extraction.md).
- Explicit skill experiments: [evaluation](references/evaluating-skills.md).
- Harness-specific fields: [harness format](references/harness-format.md).
- Registry integration: [sidecar metadata](references/registry-sidecar-metadata.md).
- Concrete instruction patterns: [exemplars](references/exemplar-techniques.md).

The bundled Agent Skills mirror is dated 2026-08-26; live standard pages win on a conflict.
Inspect syntax, pointers, requested preservation and actual selected loading for this edit.
Use the existing native authoring/publication mechanism; instruction checks do not prove
runtime behavior. Keep bodies below 500 lines and about 5,000 tokens; these are ceilings,
not targets.

<simple: report the substantive change, narrowed triggers, actual checks and selected or
staged status. State a specific unresolved dependency when one remains.>
