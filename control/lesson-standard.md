# Each lesson teaches one change you can check

2026-09-13. This standard applies to the ten lessons in [the approved plan](plan.md)
and each skill’s reader README. The plan’s titles, ownership and reading order stay unchanged.
The groups remain **Stop repeat work** (1–3), **Give agents what they need** (4–6),
and **Keep work understandable and recoverable** (7–10).

## The opening states the useful change

Start with the thesis in two or three sentences. Tell readers what they will understand
and be able to do after reading. Answer that need directly, without asking a question
or using “what you will know”. Keep the opening within **360 characters**, including
spaces and punctuation. This is a writing budget, not proof that it fits a screen.
Check the title and complete opening together on a narrow phone and a desktop before accepting the page.

For lesson 1, **You turn repeated mistakes into reliable checks**, the complete worked opening is:

> When the same mistake returns, turn the correction into a check that runs on each change. You will learn to choose its boundary and prove that it rejects the mistake while allowing valid work.

This is a proposed opening, not a new factual claim about anyone’s practice.
It promises the distinction lesson 1 must teach: rejecting a demonstrated mistake while permitting valid work.
Do not copy the standard’s field names or instructions into the page.

## Each section makes the next one possible

Begin with the first distinction the reader needs. Explain it from evidence, then use
it to support the next decision. Finish with enough understanding to make and check
the change named in the title. Do not fill an outline with interchangeable advice.

Each section heading states its conclusion as a clause with a plain verb, using at most
eight words. The heading must describe the section’s actual claim. A verb alone does
not make a heading useful. No heading may appear word-for-word on more than two lesson
pages, or on more than two skill pages. Navigation labels are outside this rule.

Every section below a second-level heading has at least three complete sentences.
This includes the section explaining the sources. Lists can contribute complete sentences,
but labels, fragments, code and headings cannot supply the missing explanation.
Keep the closing action separate so its single sentence cannot pad the preceding section.

## Sources support the claims beside them

Cite primary sources beside the claims they support. Every factual claim about a named
person’s practice needs a citation with a timestamp or anchor. No citation means no claim.
Preserve quoted-through attribution, sponsorship, opinion, dates and limits on what was observed.
A repository associated with someone does not establish that they wrote every change.

Near the end, give the sources their own section. Its heading must say what the sources
show, rather than merely naming the section “Sources”. Explain their contribution in
at least three sentences and list the citations there. Put the closing action after this section’s evidence.
Every source link must match an entry in that page’s citation list or point to its entry.
An unrelated page anchor does not count as a citation.
These local checks do not fetch source addresses. Research and review must establish reachability.

## The last sentence gives one next action

End the article with one separate paragraph containing one sentence. Give the reader
one concrete action they can take with their new understanding. Do not add a second task,
a summary, or a menu of next steps. Navigation and the site footer follow outside the article.
The final action has no separate second-level heading.

## Skill readers follow the same sequence

Each skill’s reader README follows the same thesis, dependent sections, primary evidence
and single next action. Explain when the skill helps, what the reader must supply,
what it does and how to check its result within that sequence. Do not substitute package
fields or agent instructions for the reader’s explanation. Reading a lesson never requires installing a skill.

The snapshot has no top-level skill READMEs. Its skill pages currently display agent
instructions and reference material. Phase 4 must write the READMEs, and later rendering
must use them for the reader pages. This phase changes neither those files nor the renderer.
The checks inspect rendered lesson and skill articles. They do not prove an absent README
exists, or that a rendered skill article matches its future README.

## Checks measure form and reviewers judge meaning

The standard gates the ordinary full check after rendering:

```sh
python3 build/check.py
```

All LS01–LS12 rules run by default. `--lessons` remains accepted as a compatibility
no-op and gives the same full-check result. `--layout` checks the source tree only,
with or without `--lessons`, and does not require generated output.
The accepted ten lessons and seven skill explanations must pass; a failing article
blocks the full check. Unrelated checks remain active.

| Rule | Checked automatically | A reviewer must decide |
| --- | --- | --- |
| LS01 | One article with an opening paragraph before its first second-level heading. | The opening teaches the approved lesson’s one useful change. |
| LS02 | The opening contains two or three sentence units. | They are complete sentences that state the thesis without asking a question. |
| LS03 | The opening stays within the stated character budget. | The title and opening fit together at the reviewed screen sizes. |
| LS04 | Visible lesson and skill page text never contains the banned phrase, ignoring case and repeated spaces. | No other wording copies an instruction or leaves the reader’s need unanswered. |
| LS05 | No authored heading is shared by more than two distinct pages of its kind. | Headings state their sections’ conclusions rather than generic topics. |
| LS06 | Every article second-level heading has at most eight words. | Every heading, including other levels, states one unambiguous claim. |
| LS07 | Every article second-level heading includes a word from the checker’s declared verb vocabulary. | That word functions as a plain verb in a complete, accurate clause. |
| LS08 | Every second-level section has at least three sentence units in its prose and lists. | They are complete, evidence-led sentences in a dependent teaching sequence. |
| LS09 | One sources heading is the last second-level heading, with one nonempty citation list in that section. | Its heading says what the sources show and its explanation preserves their limits. |
| LS10 | All source-section links resolve to that list’s entries or match their qualified source URLs. Each entry has an address with an anchor or timestamp. | The linked material is primary, reachable and actually supports the stated claim. |
| LS11 | At least one inline citation appears before the sources section. All inline citation references resolve to an entry. | Every named-person practice claim has a nearby, adequate citation with a useful locator. |
| LS12 | Exactly one marked closing paragraph ends the article and contains one sentence unit. | The sentence specifies exactly one practical next action. |

These rules apply equally to rendered skill articles. Heading comparisons count distinct
pages, not repeated appearances within a page, and keep lessons and skills separate.
Comparison ignores case and repeated whitespace but keeps punctuation.
Authored headings include the page title and article headings. Shared menus, contents rails,
footers and decorative text are excluded from heading and section checks.

The checker uses a declared vocabulary rather than guessing grammar from word endings.
An unfamiliar valid verb needs a test-backed vocabulary addition. Words such as “check”
can also be nouns, so a passing result cannot replace the heading review.
Sentence units end at a period, question mark or exclamation mark followed by whitespace
or the end of a prose block. Decimal points and common abbreviations are protected.
An unfinished trailing fragment counts as a unit for opening and closing limits, but
cannot contribute a complete sentence to a section. Reviewers still check actual grammar.
The protected abbreviations are e.g., i.e., Mr., Mrs., Ms., Dr., Prof. and vs.
Characters are decoded text characters after repeated whitespace becomes one space.
Hyphenated and apostrophised words count as one word. Code, hidden content and headings
do not pad section counts. Hidden content means HTML hidden attributes,
accessibility-hidden content and script, style, template or decorative vector elements.
The checker does not calculate visibility from stylesheets.

## The page carries invisible evidence markers

The following markup is for the writer and renderer. None of these identifiers becomes
a visible heading or label. Markdown may carry the equivalent raw HTML markers.

- Put the reader’s opening inside the page’s single `article`, before its first `h2`.
- Give the sources `h2` the identifier `sources`, with its own claim as visible text.
- In that section, use one `ol` or `ul` identified as `citations`. Give each direct
  `li` a unique identifier starting with `cite-` and at least one primary source link.
- Each listed source address uses HTTP or HTTPS with a nonempty anchor, or a timestamp
  query named `t` or `start` using seconds or an hours/minutes/seconds value.
- Link inline citations to their entries with `href="#cite-…"`. Other internal links
  remain ordinary navigation. The existing checker still checks their targets.
- Source-section links may use those same entry fragments or exactly match the qualified
  source addresses in the list. Ordinary further-reading links belong outside this section.
- Mark the single last paragraph `id="next-action"`. It follows the citation list
  and is excluded from the sources section’s sentence count. Do not append article content.

Reviewers follow [the lesson review instructions](design-review-capsule.md#review-the-lesson-as-a-reader).
Keep visible paths, hashes, code spans, format names and tool internals out of reader copy.
Use plain link labels for technical evidence and keep runnable details in their proper companions.
No check here proves source truth, successful execution, viewport fit or reader understanding.
