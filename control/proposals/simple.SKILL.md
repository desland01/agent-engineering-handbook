---
name: simple
description: Rewrite free-form prose using the simplest exact wording while preserving evidence, context, and necessary caveats. Use for explainer pages, marketing copy, headlines, and section titles that would benefit from direct language.
audience: human
disable-model-invocation: false
user-invocable: true
lifecycle:
  origin: "2026-08 owner craft rule. Rewritten 2026-09-03 with the owner: human readers get /simple, model readers get /precise; approved verbatim in session."
  class: craft
  last_verified: 2026-09-03
  sunset: "Retired only on an explicit instruction from the owner, Desmond, that names this skill. No vendor, host, or model release retires it."
---

---

class: craft
applies_when: "Any prose a human will read: explainer pages, reports, replies, marketing copy, headlines, and section titles."
skip_when: "Text a model will read (use /precise), or the owner asked for a technical treatment in that request."

---

# Writing clearly

Use the simplest exact wording.

**Standard (owner ruling 2026-09-03).** Text a human reads is written `/simple`. Text a model
reads is written `/precise`. A technical treatment for a human is the exception and requires
the owner to ask for it in that request. Reference build, approved verbatim:
`/Users/thebeast/docs/visuals/what-happened-plain-2026-09-03.html`.

Write for one reader who has never seen the project, the tools, or the vocabulary, and who
knows how a workplace runs: managers, rules, inspectors, doors, switches. Introduce every
technical object as one of those before its real name, if its real name appears at all. Then
state the practical effect: what the reader does, how often, what changes, or what they no
longer need. End with why it matters to that reader.

Rules:

- One idea per sentence, 12 to 20 words, no semicolons.
- One analogy per concept, held for the whole piece. Never mix a second image into it.
- A technical name appears at most once, only when the reader must open or type it.
- Each number appears once, with its unit and its source.
- Never name the owner or refer to him in the third person; see Voice.

Remove:

- "Not X, but Y" constructions
- Closing sentences that only repeat the paragraph
- Three-part lists padded for rhythm
- Headlines built around a rhetorical reversal
- Needlessly complex words

Keep:

- Numbers, dates, names, paths, filenames, and commands
- Evidence and reproducible steps
- Caveats needed for accuracy

Before deferring, excluding, or rerouting a named project, explain what the project is in one or two sentences. A project name alone may lack enough context.

Delete any word, sentence, or heading whose removal preserves the meaning.

## Headings, labels and names

A heading states what its section concludes, in the words a reader would use, so that a person
who sees only the heading draws the same conclusion as a person who reads the section. Test it
with the body covered: read the heading, write what the section must be claiming, and rewrite
any heading a reasonable reader could take differently or opposite. A clause with a plain verb,
up to eight words, no semicolon. The same rule binds titles, captions, table column names and
list item names: removing a word count from a label does not turn it into a claim.

Measured 2026-09-10: "Repeated fixes spend tokens" read alone says automation costs tokens,
the reverse of its section; "Repeated failures waste tokens" passes. Across 76 sections written
to the earlier instruction - name the subject in two to five words - 72 were labels, and a
reader given only the headings misread one outright.

## The instruction is not the output

A field name, a template label, a schema key, or this method's own wording never appears in the
work as a heading, a label or a sentence. When a schema field is called `source_claim_paraphrase`,
the heading is what was actually said, in its own words, and the section is written rather than
pasted. The fingerprint is a heading repeated word for word across many pages, or one stock
sentence appearing in file after file. Where the work calls for prose, a section is at least
three sentences written from the evidence.

## Five seconds, from any viewpoint

Anyone landing at any point on any page understands what is being said within five seconds.
Front-facing text - headlines, leads, band descriptions, tile lines, table rows, captions -
carries no technical writing and no jargon: no file paths, revision hashes, code spans, format
names or tool internals. Where the technical detail matters it lives on a second page written
for that purpose, or behind a link to the repository, and the front-facing line says in plain
words what the reader would find there.

## Voice

<Directions in angle brackets are for the writer and never appear in the output.>

- The output never names the owner and never refers to him in the third person. Address the
  reader as "you". Where a third party may read it and the role matters, write "the owner".
- No praise, thanks, or deference toward the owner or the reader. Write so the page could be
  published as a plain description of what the system did.
- A register direction is an instruction to the writer, never a sentence in the output. In skill
  text, wrap every register direction in angle brackets: <written for a reader who has never seen
  the project>. Owner ruling 2026-09-03 23:44.
