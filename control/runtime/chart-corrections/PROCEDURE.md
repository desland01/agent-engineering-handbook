# Procedure — correct a Chart's heading instructions (proved on the pilot Chart, 2026-09-10)

This is the procedure that worked on `explainer`, the known-bad Chart, in one attempt: three
sentences corrected, checker 14/14, reviewed cold by a different route. Follow it per bundle.

1. Read RULE.md and restate the rule to yourself: a heading states what its section concludes,
   in the words a reader would use, tested by covering the body; a noun-phrase, word-count or
   fixed-string heading is a label and fails.
2. Read the bundle's SKILL.md and every file under references/ in full. List every sentence
   that instructs the wording of a heading, title, headline, section name, label or caption.
   The pattern is not always phrased with the word "heading": look for "name", "label",
   "title", "kicker", "section", "caption", "in this order", and tables of required section
   names.
3. Classify each listed sentence. Mark it for change only if it instructs toward a subject, a
   noun phrase, a word count, a label, or a fixed string a writer would paste in as-is. Leave
   unchanged: bans on eyebrows, kickers, overlines and reversal headings (those protect the
   claim); typography, size, spacing and count rules; evidence notes and dates.
4. For each marked sentence, rewrite it to instruct for a claim — a clause with a plain verb,
   up to eight words — and carry the cover-the-body test with the instruction. Where a
   template names required section headings, keep the section order and required elements
   but make the wording say what each heading must claim, not what it is called. Keep the
   Chart's own register; do not add rules the Chart did not have; do not reword for style.
5. Write the corrected file to out/<bundle>/<same relative path>. Frontmatter byte-identical.
   Every line you did not mark byte-identical, including line breaks and trailing whitespace.
   A file with no marked sentence is recorded clean and is not written.
6. Record every change in corrections.json: original line number, before (verbatim), after
   (verbatim), one-sentence why. Every bundle in HALF.txt once; every .md file in each bundle
   once, changed or clean. A change spanning several lines lists each line.
7. Verify before moving on: diff out/<bundle>/<file> against charts/<bundle>/<file> and confirm
   only the marked lines differ and the frontmatter is untouched; confirm corrections.json
   lists every file of the bundle.

Where the pilot went wrong, so you do not: the pilot's rewritten headings for a page carried
semicolons and ran to ten words. In Chart text that is not your concern, but where you write
an example heading inside an instruction, keep it under eight words with no semicolon.
