# The composition repair passes rendered review

September 10, 2026. Maker: Fable 5.1. Reviewers: GPT-6 parent and GLM 5.3 Flash.
Scope: handoff B3/B5, the home page's content families and the investigations-page motion.
The shared problem-panel graphic from commit `67f3bd8` must survive integration.

The first maker run, `b0df5bab-ecd7-470c-9784-99142faea53a`, delivered a three-file patch in
the retained `skill-packs-20260910d` runtime's `var/workspaces/fable-handbook-design/out/`.
The parent ran the real Markdown build; all 54 pages passed structure/link/hash checks.
The existing 72 rendered checks passed. Stagehand local-browser captures at 1440 and 390
were scrolled through, tiled below 2000 pixels per axis, and opened by both reviewers.
The initial full-page captures before scroll traversal were replaced, not treated as defects.

## A navigation class hid the lead report

The parent found that the lead investigation disappeared entirely at 390. At 1440 its title
inherited uppercase navigation typography. The new report used `primary`, a class already
reserved by the navigation's responsive display and text rules. The parent added a behavioral
assertion that the three report destinations have nonzero rendered boxes at each viewport;
it failed on the candidate with `investigation destination hidden or missing — github-inspection.html`.

The patch also conflicts with the newer problem-panel CSS. Fable's repair must preserve that
graphic and use a report-specific modifier instead of changing navigation behavior. A report-only
finding corrects the maker's asset-weight comparison: 44 KB is 2.5 times its stated 17.6 KB
baseline, not 3.7 times.

## Section captures separated effects from defects

GLM review run `d5f7fffa-60e8-412b-a0ee-ae1ba487ebbf` inspected all ten tiles and flagged:
missing guide-count marks, an absent connecting wire, hard clipping of the next idea card,
small companion-diagram labels, excessive skill-row space, and repeated source text in guide rows.
The earlier review packet lacked exact filenames and a listing tool; it returned no visual
verdict. Its packet was corrected before this successful image review.

Additional captures placed the guides and reports inside the viewport. The count marks and
wire are present: their timelines had reset when the full-page capture returned to the top.
Desktop marks and both in-view wires had identity transforms; the last mobile mark was still
growing as it entered. The parent opened all four section captures. Fable has these images
and measurements to answer those two findings without removing working motion.

The repair run is `d8f5d038-e27c-4d8b-b4ce-36d51dbc1540`, under the selected
`handbook-heading-corrections` runtime at `var/workspaces/fable-handbook-refinement`.
The maker supplied an applied/overruled answer for every finding. Read-once screenshots are in
`~/ephemera/handbook-composition/`, `handbook-guides-in-view/` and `handbook-reports-in-view/`.

## The repaired candidate was accepted and integrated

The parent opened all ten final home tiles at 1440 and 390, the two final report-section
captures, and both investigations-page captures. All three report destinations render on
mobile; the primary title uses the intended sans typography on desktop. The stronger ideas
fade and tighter skill rows are accepted. The report diagrams now occupy a full-width
primary row and two companion columns. Their smallest labels remain small on phones;
full study views remain the reading destination.

The parent accepts each written maker disposition below. Guide marks and wire findings were
capture artifacts, confirmed with in-viewport evidence; guide source labels correctly distinguish
a shelf from its source report. The tiny hover/stem gap is a harmless motion detail. No source
claims or headings were rewritten in this lane. The separate Astra copy assignment remains
blocked, and this review does not claim the entire existing site's copy is plain.

The real Markdown build passed. The new mobile-report assertion first failed against the
initial candidate and then passed with the repair; all 72 rendered checks passed at 390/1440.
After integration, all three source files, the regression checker and affected built outputs
were byte-identical to that checked candidate. The archive regression and 54-page structural
check also passed in the shared repository; no duplicate full browser suite was needed.

Stagehand used provider `local`, origin `launched`. Home and studies at both widths had no
page overflow, console errors or page errors. Each of the three study SVG masks changed from
a partial position to `0% 0px` as the reader scrolled. Reduced-motion guards were inspected in
CSS, but reduced-motion emulation was not run. No library was added; this means zero library
bytes, not zero CSS bytes. Compressed CSS + JS grow from 18,050 to 21,258 bytes against the
current base, including the preserved problem graphic's CSS. No GSAP or pinned section was
needed for the selected reveal.

Final images: `~/ephemera/handbook-repaired-home/`, `handbook-repaired-reports/` and
`handbook-repaired-studies/`. One concurrent Stagehand initialization timed out; the same
route succeeded on a sequential retry. The failed initialization supplied no visual verdict.

## The maker answered every finding

The following is the maker's final written response, retained here with the parent acceptance
above so it outlives the worker workspace.

# B3/B5 refinement — answers to the root and GLM reviews

Fable, 2026-09-10. Workspace `var/workspaces/fable-handbook-refinement`.

Deliverable: `out/deliverable.patch` (paths `a/build/…` → `b/build/…`, three files) against the exact current shared files preserved under `out/base/build/` before any mutation (render.py `974292f9…f415`, handbook.css `b2c4bfaf…fe18`, handbook.js `25721abf…444e`, byte-identical to `site/build/` at the start of this run). `git apply --check` and `git apply` on a copy of `out/base` both succeed and the result is byte-identical to the working files in `site/build/`.

Mode: evolve. Inputs: ROOT-REVIEW.md, GLM-REVIEW.md, the ten full-page tiles in `evidence/`, the four in-viewport captures in `evidence-guides/` and `evidence-reports/` with their `evidence.json`, `maker.md`, `original/`, `candidate/`, `site/build/` (render.py, handbook.css, handbook.js, check.py, check-render.js, icons.py), `DESIGN.md`, `control/plan.md`.

What was verified here and what was not: `python3 -m py_compile` and `node --check` pass; the CSS has balanced braces; string checks confirm the reconciled content (listed under R2). `markdown` is not installed on this host and installs are not authorized, so there is no real build here and no shim was created; there is no browser here. Every rendered statement below is either an observation from the supplied screenshots, or a calculation from the CSS and the SVG sources and marked as such. You run the real build and the browser checks.

## Root findings

### R1 (HIGH) — report card hidden at 390 and set as navigation at 1440. Applied.

Observed in `shot-390x850-part-4.png` (only Matt and Boris stacked) and `shot-1440x1100-part-3.png` (the T3 title in uppercase mono). Cause confirmed in the base CSS: `.primary { display: none; gap: 2px; }` with `display: flex` only from 760px, and `.primary a` sets the mono uppercase nav label; `report_card()` emitted `class="file primary"`.

Change: `render.py` `report_card()` now emits `class="file file-primary"`; every `.file.primary` selector in the CSS is now `.file-primary`. Navigation rules are untouched (`.primary { display: none; gap: 2px; }` and `.primary a, .repo, .menu summary {…}` are byte-identical to the base). No rule in the stylesheet hides `.file-primary` at any width, so the three destinations `github-inspection.html`, `matt-pocock-inspection.html`, `boris-cherny-inspection.html` are laid out at 390 and 1440. The new `inspectPage` assertion was not run here; it is not claimed as passed.

Docstring and CSS comment record why the modifier is report-specific so the collision is not reintroduced.

### R2 — reconcile onto the current shared source. Applied.

Method: `git merge-file` three-way (base `original/`, ours `site/`, theirs `candidate/`) on each of the three files — no line-level conflicts; then the now-unused seam removed by hand. Result:

- Kept from the current site, byte-identical: the `<figure class="pick-figure" aria-hidden="true"><img src="assets/problem-loop.webp" width="1600" height="644" alt="" decoding="async"></figure>` markup in `landing()`; the `shutil.copy2(ASSETS / 'problem-loop.webp', …)` static copy; the `.pick-figure` rules (margins, `opacity: 0.9`, 620px and 760px caps); the `pick-draw` mask animation with `animation-range: entry 45% cover 40%` and its keyframes; the `.pick { … padding: 22px 20px 20px; }` rule itself.
- Dropped from my candidate: `position: relative; isolation: isolate; overflow: hidden` on `.pick`, the `.pick > *` lift and the `.pick > .graphic` rule and comment. Nothing references `.graphic` now.
- Kept from my candidate, on purpose: the panel trace's zero state (`transform: scaleY(0)`) moved into the `@supports (animation-timeline: view())` + `no-preference` block. It is independent of the graphic, and it makes the base comment true ("browsers without scroll-driven animations get the finished drawing"): with `scaleY(0)` on the base rule, such a browser shows no trace at all. It was listed as a fix in `maker.md` §1. If you want the base behaviour instead, revert that one hunk; nothing else depends on it.
- Everything else from the candidate carries over unchanged (report_facts / report_card / shelf_row / band_head forms, the bleed, lanes, lane + directory, files, the guarded motion, the B5 sweep, the REVEAL selector).

### R3 — B5 weight comparison. Corrected (report only).

Measured with `gzip -9`, decimal KB:

- Before my pass (`original/`): CSS 13,924 B + JS 3,709 B = 17,633 B = 17.6 KB. 44 KB ÷ 17.6 KB = **2.5×**, not 3.7×.
- Current shared base (`out/base/`, with the panel graphic CSS): 14,341 + 3,709 = 18,050 B = 18.1 KB. The base also ships `problem-loop.webp`, 40,298 B raw (a raster; gzip does not apply).
- After this patch (`site/build/`): 17,443 + 3,815 = 21,258 B = 21.3 KB; 44 ÷ 21.3 = 2.1×.

The 44 KB figure for GSAP is the number in `control/plan.md` item 5, not measured here (no network). The B5 decision and its reasoning are unchanged: native, unpinned, 0 KB; the ratio only says what a library would cost against the site's own text assets. `maker.md` §4 point 3 should read "2.5× the site's entire text asset weight before this pass (2.1× after it)".

## GLM findings

### H1 — guide stage marks absent. Overruled: capture context, with evidence.

`evidence-guides/evidence.json` at 1440×900 (scrollY 3023) records the four `.marks` boxes at x 1064.5 with widths 140 / 32 / 32 / 14 px and transform `matrix(1, 0, 0, 1, 0, 0)` — exactly 8, 2, 2 and 1 marks of 14px at 4px pitch — and `evidence-guides/shot-1440x900.png` shows them right-aligned in the 140px column. At 390 (scrollY 4686) the first three are identity and the fourth is `scaleX(0.708)` because at y 607 of an 850px viewport it is still inside its `entry 45% cover 40%` range. The full-page tiles were captured after returning to the top, which puts every `view()` timeline below the fold at its start state; that is what the tiles show, not the at-rest state a reader sees. Under `prefers-reduced-motion: reduce`, and in browsers without scroll-driven animations, the marks are complete because the zero state lives inside the guard. No change. The range is one token (`entry 45% cover 40%`) if you want the marks complete lower in the viewport.

### H2 — ideas bleed cuts text mid-word with no fade. Applied.

The 40px fade was applied but too weak to read over body text. Sampled from the exact tiles (max luminance of the text band per column): 1440 tile 1, x 1400 → 172, x 1410 → 130, x 1420 → 92, x 1424 → 71; 390 tile 2, x 345 → 244, x 365 → 153, x 374 → 101. So only the last ~25px dimmed, and "local" / "class" stayed legible to the edge (crops in `out/crop-1440-edge.png`, `out/crop-390-edge.png`).

Change: `.bleed .ideas-row { --fade: clamp(64px, 10vw, 144px); }` and the shared `.ideas-row.is-overflowing` mask now reads `calc(100% - var(--fade, 40px))`, so the row elsewhere keeps 40px. Calculated: at 1440 the fade is 144px, 43% of the 336px card that is cut, so the fourth card dissolves across its last third; at 390 it is 64px against the 54px slice of card 02 that shows, so that slice dissolves entirely instead of stopping mid-word. The script contract is unchanged: the fade lifts at the end of the row.

### M1 — companion diagrams illegible at 1440. Applied.

Measured from `icons.py`: all three report drawings are `viewBox 0 0 160 80` with labels at 2.8–3.2 units, so a label renders at width ÷ 160 × 3 px. At the companions' ~228px (a 1fr column of `2fr 1fr 1fr` inside the 1152px wrap, minus 48px padding) that is 4.3px; even the primary at 480px is 9.0px. No one-row 2 : 1 : 1 inside a 1200px page can make the companions legible, so the row is restructured rather than tuned:

- ≥ 900px: `.files` is two columns; the primary spans both as a landscape card (diagram in a `1.15fr` lane on the left, title 1.55rem / line / metadata as one block centred on the right); the two companions share the row beneath. Widths at 1440: 1104 : 540 : 540 — 2 : 1 : 1 by width, so 10 / 2 / 1 is still read as space.
- One register for all three: `.file .art { max-width: 480px }` at every width, `max-width: none` inside the two-column layout. Calculated at 1440: primary diagram ≈ 541px (labels ≈ 9.5–10.1px), companions ≈ 516px (≈ 9.0–9.7px); the study page's 640px (12px) remains the fullest rendering. At 900–1079px the companions fall to 366–450px (6.9–8.4px); the breakpoint is one token if you would rather stack below 1080.
- The wire is one hairline bus between the rows (`.file-primary::after`, 22px under the primary), with a stem down from the primary and a stem up into each companion; the row gap is 45px so the stems meet the bus. Under 900px the layout is unchanged: the rail above the stack and a stem into each card. The bus takes the same `grow-x` guard and range as the rail.
- Cost, calculated: the band is roughly 400px taller at 1440 (≈ 330px primary row + 45px + ≈ 440px companions, against ≈ 360px before). It is filled by legible figures, not by space.

Note for your in-view probe: at ≥ 900px `.files::before` is `display: none`; the drawn wire is `.file-primary::after`. If the probe reads `.files::before` at 1440 it will now report the hidden rail, not the bus.

Known minor property: the 2px hover lift is on the card's `a`, the stems on the `li`, so lifting the primary opens a 2px gap above its stem on desktop (before, the same lift overlapped the stem above). Left as is; say if you want the lift dropped on the primary.

### M2 — investigations wire not visible; stems float. Overruled: capture context, with evidence.

`evidence-reports/evidence.json` records the wire transform `matrix(1, 0, 0, 1, 0, 0)` at both 1440×900 (scrollY 3635) and 390×850 (scrollY 5431), and both `evidence-reports/shot-*.png` show the hairline spanning the cards with a stem into each. The full-page tiles show the `scaleX(0)` start state for the same reason as H1. Under reduced motion and without scroll-driven animations the wire is complete. The device is kept; its desktop form is now the bus described under M1, same guard and range, and at 390 the rail-and-stems form your capture shows.

### M3 — skills lanes: dead band under the text. Applied.

Observed in `shot-1440x1100-part-2.png`: rows ≈ 270px from the 220px art box, text ≈ 130px, top-aligned. Changes, at 760px and up: art box 220 → 192px, drawing 150 → 136px (caption clear of the drawing: drawing spans y 28–164, caption at 166–180), row padding 28/26 → 24/22, and the text lane centred against the drawing with `grid-template-rows: 1fr auto auto auto auto 1fr` (title, use, count and routes placed in rows 2–5, the art spanning all rows with `align-self: center`). Calculated: a row is ≈ 238px with the ≈ 160–176px text block centred, so no hollow under the text; where the text is taller (three-line uses near 760px) the drawing centres against the text instead. Under 760px unchanged (180px box, 120px drawing). Markup untouched, so `check.py`'s four `tile skill` count holds on both pages.

### P1 — guide rows state the source twice. Overruled, with reason.

The mono line names the report the shelf traces to, not the shelf: "Theo's video" and "Melee for Mac" both resolve to "Theo: T3 Code and Melee", which is a fact the row states nowhere else (two shelves, one report). GLM's condition was "with H1 unfixed it is also the row's only secondary information"; the marks are present at rest (H1 evidence), so the count is carried visibly and the line is not the row's only secondary information. Wording of front-facing lines is the separate copy lane, which is rate-limited and not replaced here. No change.

### Observation — typed prompt shows `/ |` at 390. Acknowledged, no change.

That is the typing animation's start state: the static markup carries the first slash command, and `handbook.js` begins typing 1400ms after load; stills cannot judge it.

## What to look at in your renders

1. `#reports` at 390: T3 first, then Matt, then Boris, each with a stem to the one above and the rail on top; the regression assertion on the three hrefs.
2. `#reports` at 1440: the landscape primary across the top, the two companions beneath, one bus with three stems; diagram labels around 9–10px on all three; the title in sans, not mono.
3. Ideas row at both widths: the cut card dissolving over its last 144px (1440) / the whole 54px slice (390); `01 of 19` and no page overflow.
4. Skills rows at 1440: text centred against a 192px art box, no hollow; four drawings still a right-hand column.
5. Guides and reports motion: marks and wire complete at rest, complete under reduced motion.

## Reversible token values introduced or changed

`--fade: clamp(64px, 10vw, 144px)`; art box 192px / drawing 136px; primary lane `1.15fr`; primary title 1.55rem; row gap 45px; the 900px breakpoint for the two-column reports.
