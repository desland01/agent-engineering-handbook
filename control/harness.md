# Handbook restructure: assignment for gpt-6-astra

Date: 2026-09-12. Repository: `/Users/thebeast/Projects/agent-engineering-handbook`, branch `desks-idea-18`.
Owner: Desmond Landry. This assignment is a long-running harness. It runs in phases. Each phase
ends with a deliverable, a check, and a gate. Do not start a phase before its gate is open.

## Why this assignment exists

The site looks finished and is not understandable. The owner reports:

- Numbers that should feel complete do not. The site says ten guides in one place, thirteen guide
  files exist in `public/guides/`, ten lesson files exist in `lessons/`, nineteen idea pages exist
  in `public/ideas/`, and seven skills exist in `skills/`. The reader cannot tell which set is the
  handbook.
- The `public/ideas/` section (nineteen pages, heading "The nineteen video ideas, consolidated into
  ten lessons") is reachable only from the lessons page and not from any header or menu. It is a
  hidden section.
- The header nav reads Lessons / Skills / Reference, but the Reference link opens `guides.html`,
  whose heading is "Find a method for the failure you face". The word and the page disagree.
- The More menu holds thirteen further pages whose names do not say what they are: Handbook index,
  Task prompts, Adopting a skill, Validation, three named inspections, Investigations, Frames,
  Video notes, Attribution, Contributing, GitHub repository. GitHub appears both in the header and
  at the foot of the menu.
- The owner's verdict: thoroughness is present; organisation of thought, clarity of intention and
  meaning are absent. The words must mean something.

Preceding work built pages before deciding what the site is. This assignment inverts that order:
decide, then research, then write, then build.

## Standing rules for every phase

1. Do not change any published page until Phase 1 is approved by the owner.
2. The instruction is not the output. Never copy a field name, prompt line or requirement from
   this file into a heading, label or sentence of the site. Answer the requirement in the page's
   own words.
3. A heading states its section's conclusion as a clause with a plain verb, up to eight words.
   Cover the body, read the heading, and write what the section must claim. If a reasonable reader
   could infer a different claim, the heading fails.
4. Front-facing copy carries no file paths, hashes, code spans, format names or tool internals.
5. Every factual claim about a named person's practice carries a citation to a primary source
   (their video, post, repository or talk) with a timestamp or anchor. No citation, no claim.
6. Preserve originals. Do not delete existing pages or source files; move superseded content under
   `control/` or git history as the project's `control/README.md` allows, and keep redirects for
   every URL that existed before.
7. Keep all reusable credentials out of prompts, reports, capsules and committed files. Read them
   from their existing configuration location at run time.
8. Record every decision, run, cost and refusal in the harness state file (see Harness section).
   Quote refusals verbatim with run id and capsule id. Do not substitute a different route for a
   refused one. Report the refusal and leave that step open.
9. Write everything the owner reads in the `simple` register. Write everything a worker reads in
   the `precise` register.

## Phase 1: Decide the structure

Goal: one written information architecture the owner can approve in one reading.

Answer each question below in writing. Each answer is one to three sentences plus one example
from the current site. Do not list options without a recommendation.

1. What is a lesson? (One teachable thing a reader does not know before and does know after.)
2. What is a skill? (A file an agent loads. The reader already understands this word. Keep it.)
3. What is a guide, and how does it differ from a lesson?
4. What is a reference? Is it the attribution and citation material, the source inspections, or
   something else?
5. What belongs in the header, what belongs in a More menu, and why is the split correct?
6. Why is the GitHub link in two places? Pick one.
7. Where does each of the following go, or why does it stop existing as a page: Handbook index,
   Task prompts, Adopting a skill, Validation, the three inspections, Investigations, Frames,
   Video notes, the nineteen idea pages.

Owner's default position. Apply it unless you can state a reason a reader would notice:

- Unless lessons and guides are clearly different kinds of thing, with a reason a reader would
  recognise, merge them into ten items called lessons. Ten, not thirteen, not nineteen.
- Each lesson teaches one thing.
- Skills stay a section and keep their name.
- The nineteen idea pages either become the citation layer under the lessons or stop being pages.
  They do not remain a hidden section.
- One GitHub link.
- Every page on the site is reachable from the header or one menu, and its menu label says what
  the page is in plain words.

Deliverable: `control/plan.md` (overwrite; this is the plan of record) containing:

- The seven answers.
- The full sitemap as a tree: every URL, its plain-words label, its parent, and for each
  existing URL either "kept", "merged into X", or "redirects to X".
- The list of ten lesson titles, each a clause stating what the reader will be able to do.
- What each lesson must cite (at least one primary source per lesson, named by person and
  medium, resolved in Phase 3).

Check: `python3 build/check.py --layout` passes. Every current public URL appears in the tree.
Gate: the owner reads `control/plan.md` and replies approve, or replies with changes. If changes,
revise and re-present. Do not proceed on silence.

## Phase 2: Set the lesson standard

Goal: a written standard every lesson and every skill README follows, so ten writers produce one
book.

Write `control/lesson-standard.md` (add it to the table in `control/README.md`). It specifies:

1. Opening: the thesis in two or three sentences that fit one viewport. It states what the reader
   will know after reading that they do not know now. It answers that question; it never asks it
   and never uses the phrase "what you will know". Example of the required form: "When the same
   mistake happens twice, write the correction down where the agent reads it. This lesson shows
   where that place is, what to write, and how to prove it worked."
2. Structure: a load-bearing sequence. Start with the first thing the reader must know, build
   each section on the one before, and end at full understanding. Each section heading is a
   claim. Each section is at least three sentences written from evidence, not from the outline.
3. Evidence: each lesson cites its primary sources inline with timestamp or anchor, and lists
   them at the end under a heading that states what the sources show.
4. Closing: the one action the reader takes next, in one sentence.
5. The same structure applies to each skill's README: thesis, sequence, evidence, next action.
6. A validator rule per requirement above, added to `build/check.py`, with a failing test in
   `build/check.test.py` first, then the rule, then a passing run. A rule that cannot be checked
   mechanically is written as a reviewer instruction in `control/design-review-capsule.md`.

Deliverable: the standard file and the validator diff. Check: `build/check.test.py` passes and the
new rules fail on at least one current page (proof the rules bite). Gate: automatic; report and
continue.

## Phase 3: Research and citations

Goal: a citation ledger with many more primary sources than the current three (Boris Cherny, Theo
Browne, Matt Pocock), each tied to a lesson from Phase 1.

Routes, by owner instruction. Use these identifiers and no others:

- Transcript and Google-surface research: Gemini 3.8 Flash, using the credentials configured in
  `/Users/thebeast/google-hackathon/` (read `README.md`, `config/` and `fleet/` there for the
  entry point and the fleet layout; do not copy credentials anywhere). Where the fleet under
  `/Users/thebeast/google-hackathon/fleet/` supports parallel agents, run the transcript work in
  parallel by source.
- Citation-target selection: the Grok 4.5 agent through the Cursor CLI (the owner logged in on
  2026-09-11). Auto mode is acceptable; record which model Cursor actually ran.
- Web collection: Firecrawl (`firecrawl_search`, `firecrawl_scrape`, `firecrawl_map`), run as
  the owner's deep-research method: wide fan-out, then consolidation, then synthesis back to
  the parent. Not the `research` skill.
- Mapping citations onto the ten lessons: Fable 5.1 (`claude-fable-5-1`). If Fable is rate
  limited, `kimi-k3-256k`, and say so.
- Writing: `sol-worker` (Phase 4).

Steps:

1. Build the source roster. Start from Boris Cherny, Theo Browne and Matt Pocock. Ask, for each,
   who else they cite, debate or share a stage with on agent engineering systems (instructions
   files, skills, verification loops, preview environments, CI feedback, recurring-failure
   capture). Target twenty to forty named people or teams. Record for each: name, channel or
   handle, why they qualify, and three candidate primary sources with URLs.
2. Fan out. For each source, pull the transcript or text, and extract short summaries (three to
   five sentences) and quotable passages under fifteen words, each with URL and timestamp or
   anchor. Do not write reports. Write ledger rows.
3. Consolidate into one file `evidence/citations.json` with one object per citation:
   `{person, medium, title, url, anchor, quote, summary, lesson_candidates[], collected_by,
   collected_at}`. Keep raw extracts beside it as `evidence/citations.<route>.json`.
4. Have Grok pick, per lesson, the three to six citations that carry it and mark them
   `selected: true` with a one-line reason.
5. Have Fable produce the final map: `control/citation-map.md`, one section per lesson,
   listing its selected citations and the claim each supports. Add the file to
   `control/README.md`.
6. Record the cost of every route in the state file. Do not ask before spending on research;
   report what it cost afterwards.

Check: every lesson in `control/plan.md` has at least three selected citations with resolvable
URLs (fetch each; a 4xx or 5xx fails). Every citation row has a non-empty quote and anchor.
Gate: automatic; report the roster size, citation count per lesson, and cost, then continue.

## Phase 4: Write the ten lessons and the skill READMEs

Goal: ten lesson sources in `lessons/` and seven skill READMEs in `skills/` that follow
`control/lesson-standard.md` and cite `control/citation-map.md`.

Route: `sol-worker`, one worker per lesson, in parallel. Each capsule carries: the lesson's title
and thesis line from `control/plan.md`, its section of `control/citation-map.md`, the standard,
write ownership of exactly one file, and the acceptance check below. Name the skills in the
capsule's ordered plan and invoke each before writing the capsule. Version-5 capsule,
`limits.maxSeconds: null`, `limits.maxRequests: null`, `expiresAt: null`.

Acceptance per lesson: the Phase 2 validator rules pass on the rendered page; every citation in
the page resolves; a second route (GLM 5.3 Flash) reads the headings with the bodies withheld
and writes one line per heading stating what it expects; you compare those lines with the
sections and rewrite any heading that contradicts or misses its section; the comparison is
recorded in `control/reviews/<lesson-slug>.md`.

Check: all ten pages and seven READMEs pass. Gate: automatic; continue.

## Phase 5: Rebuild the site

Goal: the approved sitemap is what a visitor sees.

1. Implement the header, menu and redirects exactly as `control/plan.md` specifies. Header
   labels are the plain words from the plan.
2. Remove or merge the pages the plan says stop existing. Add a redirect for each old URL.
3. Rebuild with the existing `build/` scripts. Run `build/check.sh`, `build/check.py --layout`,
   and `build/check-render.js`.
4. Rendered review before it lands. Two reviewers in parallel from rendered evidence: one on
   composition and orientation (can a reader landing on any page say what it is within five
   seconds), one on copy and the instruction-is-not-output rule. Routes: GLM 5.3 Flash and one
   other admitted route. Record every finding as applied or overruled with the reason in
   `control/reviews/site-structure.md`. Silence does not close a finding.
5. Walk the site as a visitor: from the home page, reach every page in the sitemap by clicking
   only header and menu links. Any page not reachable that way fails.

Deliverable: the rebuilt `public/` on this branch, uncommitted until the owner says commit.
Check: all four checks pass and the visitor walk reaches every page. Gate: present the owner a
one-page summary in `~/ephemera/handbook-restructure-summary.md`: what changed, the sitemap,
citation counts, costs, open findings. Stop and wait for the owner.

## Harness

- State file: `control/harness-state.json` (add to `control/README.md`). It records the current
  phase, each step's status (`pending`, `running`, `done`, `blocked`), run ids, capsule ids,
  costs, refusals quoted verbatim, and the gate decisions with who made them and when.
- Restart rule: on any restart, read the state file first, resume at the first step not `done`,
  and never redo a `done` step unless its inputs changed (record the changed input).
- Blocker rule: a blocked step names the exact blocker. If it is a credential or approval only
  the owner holds, name it and continue every step that does not depend on it.
- No elapsed-time limit. Scope is the boundary.
- Report to the owner only at gates and on blockers, in the `simple` register, with a link to
  every file mentioned.
