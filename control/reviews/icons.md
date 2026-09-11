# Review — the icon set and the problem panel

2026-09-11. Subject: the 36 hub icons (19 ideas, 13 guides, 4 skills) and the home page's
problem-panel drawing, remade through Higgsfield in the premium-tech idiom. Maker: Fable
(this session). Reviewer: GLM 5.3 Flash, capsule `handbook-glm-icons-review-20260911`
(round 1) and `handbook-glm-icons-review-2-20260911` (round 2), each with `precise` and
`design-review` loaded, working from tiled renders at 1440 and 390 and an icon sheet at
96 / 52 / 32 px.

## What was made

- Round 1: abstract circuit-trace glyphs (Recraft V4.1, vector), one line and one dot each.
  The owner ruled while the review ran: icons must depict their subject, not read as
  "spooky Matrix" traces. Round 1 is retained under `.scratch/icons-v2/v1-installed/`.
- Round 2 (installed): monoline pictograms of recognisable objects, one warm-white line and
  one orange dot, each from a subject sentence tied to its title; generator cut-outs turned
  into SVG masks in painter's order so the icons are true holes on any ground. The panel was
  redrawn as knot → check-marked gate → three clean traces (GPT Image 2.5, transparent).
- The three investigation diagrams keep their authored SVG (they carry mono captions).
- Icon colour moved from the accent to `--fg` everywhere a drawing is inlined, so the dot is
  the only colour.

## Round 1 — reviewer's findings and the maker's answers

## Findings

1. skills/home@1440, home@390: the "Agent feedback engineering" icon raster sits on an opaque lighter-black rectangle that does not match the tile ground, reading as an unblended pasted image.
   - Evidence: skills-0.png, top-left skill tile (visible dark square behind the glyph); home-1.png, first skill row; home-390-1.png, same tile. The other three skill glyphs blend cleanly.
   - Rule: PLAN.md — "Transparent raster, 1600x569" (panel) and "Drawn in currentColor"; DESIGN.md — "Depth: none… Structure is drawn with hairlines" — an opaque plate is a depth/ground break.
   - Proposed fix: re-export that one PNG with a transparent background (or match `--bg`/tile fill exactly) and re-render the three surfaces.
   - Severity: blocking.

2. sheet: line weight is not one value — roughly half the set is drawn at a fraction of the others' stroke.
   - Evidence: icon-sheet-96-52-32-a.png: guide-02, guide-05, guide-08, guide-09, guide-11, idea-05, idea-09, idea-13, idea-15, idea-17 are hairline-thin beside guide-06, idea-12, idea-19, skill-agent-ready-workspaces, which are visibly heavier; icon-sheet-raw-as-generated-a.png shows guide-08 and idea-05 at roughly double weight of neighbours (different-hand look).
   - Rule: PLAN.md — "one continuous warm-white line"; the set's premise (b) is one visual grammar.
   - Proposed fix: normalise all strokes to one width at the 40px master size and re-export; re-check the 20px guide renderings.
   - Severity: should.

3. sheet: the accent dot is not "one small dot" — its size varies by several times across the set.
   - Evidence: icon-sheet-96-52-32-a.png guide-08 and idea-18 (large dot) vs guide-02, guide-09, idea-05 (near-invisible dot); raw sheets confirm the same imbalance pre-recolour.
   - Rule: PLAN.md — "exactly one small orange dot on the line".
   - Proposed fix: pin the dot radius to one value at master size (and scale it, not re-derive it, at export sizes).
   - Severity: should.

4. sheet + guides@1440: several icons do not read as their subject at small sizes (question a).
   - At 32 px (icon-sheet-96-52-32-a/b): **guide-02** reads as nothing (a faint bent line; subject is a check-notched gate — the notch is lost); **guide-09** nearly invisible (subject: trace through sealed check square — same loss); **idea-05** reads as a thick "S" curl, not a bridge/socket joint; **guide-11** reads as a pipe with a valve, not two squares in series; **idea-13** reads as a rounded blob, not a trace turning aside at a barred square; **guide-13**'s fan collapses into smudge. Reading as a different subject: **guide-08** reads as plumbing/ladder rather than parallel traces with ties (arguably acceptable), and **skill-agent-context-calibration** reads as a clock rather than a calibration dial.
   - On the page (guides-0.png): guide icons render at 20 px in 34 px boxes — guide-02, guide-04, guide-11, guide-13 are unreadable marks.
   - Rule: SUBJECTS.tsv — each glyph "has its own subject tied to its title" (PLAN.md); DESIGN.md "Icon tile… a 34px bordered box holding the guide's drawing" implies the drawing carries identity there.
   - Proposed fix: at 32 px and below, keep the pictogram element (check notch, gate square, bridge square) and drop decorative tangle; for guide-04/11/13 simplify to the single subject object.
   - Severity: should.

5. home@1440 (panel): the drawing carries "tangle → gate → three clean traces," but a cold reader would describe it as "a scribble of dotted thread that straightens into three dotted lines," not "repeated mistakes become one check" (question c).
   - Evidence: home-0.png, panel under "Start with the problem you have" — the loops dominate ~70% of the width, the gate square is a few pixels of dots, and the three parallel traces fade before they read as an outcome.
   - Rule: PLAN.md — "a path tangles into three loops, passes one gate, straightens into three parallel traces."
   - Proposed fix: shorten/shrink the tangle and enlarge the gate marker and the parallel-trace segment so the before→after ratio inverts; the one orange dot at the gate is correct and should stay.
   - Severity: should.

6. home@1440 ideas band: moving the tile drawings from accent-orange to warm white cost the tiles their anchor — the page gained overall cohesion but the individual tiles got weaker (question d).
   - Evidence: home-0.png, ideas band: on the "Close the CI feedback loop" tile the glyph is a faint grey doodle that loses to the `[01]` marker and the orange timestamp; on ideas-1.png tile 07 the drawing is barely there. Colour on the page now concentrates in tiny dots, numerals and buttons.
   - Rule: DESIGN.md — `--accent-text #f37a3b … drawings` records drawings as an accent role; the new warm-white line is a deliberate re-role, but DESIGN.md "Hierarchy of the site" gives idea tiles a drawing as their lead element.
   - Proposed fix: keep the warm-white line but lift the tile glyph one contrast step (e.g. muted-fg instead of dim) or keep the dot plus the trace's node squares slightly brighter, so the drawing wins its own tile.
   - Severity: could.

7. guides@1440 scroll strip: the icon boxes are tinted (orange hairline/fill) in the strip but neutral in the shelf grids below — the same icon appears in two frame treatments on one page.
   - Evidence: guides-0.png, "+ THEO'S VIDEO" carousel boxes 01–05 vs the four-column shelf grid below them.
   - Rule: DESIGN.md — "Icon tile (`.tiles.guides .tile`): a 34px bordered box holding the guide's drawing" — one box treatment is specified.
   - Proposed fix: unify the carousel boxes on the same hairline/fill as the shelf tiles, or verify the tint is an intentional current-section state and document it.
   - Severity: could. (Composition around the art is otherwise out of scope; flagged only because the box frames the new art.)

8. sheet: corner language is mixed — some glyphs are drawn on sharp right angles, others as rounded blobs.
   - Evidence: icon-sheet-96-52-32-a.png: guide-03, guide-10, idea-19 sharp; idea-13, idea-10, idea-04 soft rounded masses.
   - Rule: PLAN.md — "right-angle and gentle bends."
   - Proposed fix: redraw idea-13 and idea-10 on the right-angle lattice the rest of the set uses.
   - Severity: could.

9. 390 question (e): nothing at 390 overflows and the halftone panel scales cleanly; the only new-art break at 390 is finding 1's opaque box, now larger relative to the tile.
   - Evidence: home-390-0.png (panel fits, dots legible); home-390-1.png (skill tile with the pasted-box artifact); home-390-2.png (remaining skill tiles clean, mono captions intact).
   - Rule: PLAN.md — transparent raster.
   - Proposed fix: covered by finding 1.
   - Severity: should (same fix as 1; no separate defect observed).

## Answers to the specific questions

- **a.** Fails at 32 px: guide-02, guide-05, guide-09, guide-11, guide-13, idea-05, idea-09, idea-13, idea-17. Reads as a different subject: guide-08 (plumbing), idea-16 and skill-agent-context-calibration (clock rather than dial). Reads correctly: idea-12 (document + pen), idea-18 (stairs), idea-03 (fan-out), idea-19 (maze with clean path).
- **b.** One grammar in concept, at least two hands in execution: the hairline-hand icons (guide-02, guide-05, guide-09, idea-05, idea-09, idea-17) and the heavy-hand icons (guide-08, idea-05 raw, idea-12, idea-19, the skill glyphs) differ in stroke weight and dot scale as detailed in findings 2–3.
- **c.** Partially. The tangle-to-traces transformation is legible; the "one check" hinge is not — see finding 5. A reader's honest description: "a knotted dotted line passing a small marker and becoming three straight dotted lines."
- **d.** Both, netting to a loss at tile level and a gain at page level — see finding 6, pointed at the "Close the CI feedback loop" tile (home-0.png ideas band) and tile 07 (ideas-1.png).
- **e.** At 390: no overflow, no illegible box, panel scales well; only defect is the opaque icon plate (finding 1, home-390-1.png). Not captured at 390: guides, ideas, skills pages — unverified at that width, stated as such.

## Verdict

Verdict: FIX FIRST — 1 blocking, 2–5 before ship, 6–8 polish.

| # | Finding | Answer |
|---|---|---|
| 1 | Opaque plate behind the feedback-engineering skill icon | **Applied.** The generator draws each outline as a filled shape plus a ground-coloured cut-out; the cut-outs were kept as ground fills. They are now converted to SVG masks in painter's order, so every icon is true holes on any background. Verified on the skill tiles (lighter `--fill` ground) in round 2 `skills-0.png`. |
| 2 | Line weight not one value | **Applied by replacement.** The pictogram set was generated from one template; round 2 `icon-sheet` shows one weight across all 36. |
| 3 | Accent dot size varies | **Applied by replacement.** Same template; dot size is uniform in round 2. |
| 4 | Several icons unreadable at 32px / not their subject | **Applied by replacement.** Every icon now depicts a nameable object tied to its title; see `SUBJECTS.tsv` (round 2) and the 32px column of the sheet. |
| 5 | Panel: tangle dominates, gate and outcome too small | **Applied.** Regenerated with a compact two-loop knot, a large check-marked gate (~¼ height) and the three parallel traces as the dominant element. New asset 1600×257, 76 KB. |
| 6 | Tiles lost their anchor when the glyph went from orange to warm white | **Overruled in part.** The one-accent rule stands (the drawings are not the page's accent role any more); the glyph colour is `--fg` at full strength, not a dim step. The pictogram set carries far more weight per tile than the traces did, which is the actual fix for the faint-doodle symptom. Re-check invited in round 2. |
| 7 | Guides carousel boxes tinted orange while shelf boxes are neutral | **Applied.** `.stage .art` and `.page-head .art` still coloured the drawing with `--accent-text`; both now use `--fg`. |
| 8 | Mixed corner language | **Applied by replacement.** |
| 9 | 390: only the opaque plate | **Applied** with 1. |

## Round 2

The reviewer named each icon's object at 32 px before opening the subject list: 26 exact matches, 7 partial, no outright miss; then found one functional miss at display size.

### Reviewer's blind read (32 px column, written before SUBJECTS.tsv)

guide-01 shield with check inside a circular arrow · guide-02 browser window with winding
route and flag · guide-03 browser window with a card in front · guide-04 document of lines
with an X and a magnifier · guide-05 folder/book with a map pin · guide-06 plug with
wrench · guide-07 speech bubble with ? pointing at a light bulb · guide-08 interlocking
puzzle pieces carrying small documents · guide-09 document with a seal and check ·
guide-10 compass on a box · guide-11 speech bubble with curly braces · guide-12 parcel box
with a fingerprint · guide-13 fanned stack with magnifier.
idea-01 window of lines with an X and share-style nodes · idea-02 two rectangles with a
check between · idea-03 gear fanning to three small boxes · idea-04 window with play
triangle and cloud · idea-05 file with up arrow beside a plug · idea-06 document with
wrench · idea-07 clock and wrench (small circle unread) · idea-08 arrows into a
shield-check · idea-09 magnifier over waves · idea-10 open book on two blocks · idea-11
person with ? bubble · idea-12 hand holding pencil on document · idea-13 open hand on a
card · idea-14 chain of cylinders and boxes · idea-15 open book with a cursor block ·
idea-16 dial gauge with plus · idea-17 signpost with check · idea-18 stairs with a small
person · idea-19 folded map with route, pin, person.
skills: scroll with gauge · circular arrow around shield-check · two windows with check ·
plug-and-socket with wrench.

## Subject match vs SUBJECTS.tsv

MATCH: guide-01, 02, 04, 05, 06, 07, 08, 09, 11, 13; idea-02, 03, 04, 05, 08, 10, 11, 12,
13, 14, 15, 16, 17, 18, 19; all four skills.
PARTIAL: guide-03 (reads as a card on a window, not a terminal cursor block — still a
usable "preview" metaphor); guide-10 (one box, not three nested folders); guide-12 (the
resume arrow survives only at 96 px; at 32 it is parcel + fingerprint); idea-01 (the git
branch reads as share/social nodes); idea-06 (the corner circular arrow is invisible below
96 px); idea-07 (the coin is an unmarked circle — cold read "clock and wrench"); idea-09
(the line of code is a bare horizontal rule; the wavy underline dominates, so the glyph
reads as water search).
MISS: none outright; idea-09 is a functional miss at its 40 px display size (finding 1).

## Round-1 findings against the new evidence

1. Opaque plate behind the feedback-engineering skill icon — **closed.** skills-0.png and
   home-1.png, home-390-1.png: all four skill glyphs sit cleanly on the lighter tile
   ground; no plate anywhere.
2. Mixed line weights — **closed.** Both sheets show one stroke weight across all 36.
3. Accent dot size varying — **closed.** Dots are uniform and small throughout, including
   at 32 px.
4. Icons unreadable / not their subject at small sizes — **closed in kind, reopened in
   part.** The set is now pictograms that name their subjects at 32 px (blind read above);
   the residuals are findings 1, 3, 4 below, not a tangle problem.
5. Panel dominated by the tangle — **closed.** home-0.png / home-390-0.png: compact
   two-loop knot, a check-marked gate of roughly a quarter of the strip's height, three
   parallel traces running to the edge; left-to-right before→after reads at both widths.
6. Tiles lost their anchor to warm white — **closed.** Full-strength `--fg` pictograms win
   their tiles (ideas-0/1.png); no faint-doodle symptom remains.
7. Carousel boxes tinted orange — **closed.** guides-strip-crop.png: boxes are neutral
   hairline; the orange dashes above them are the shelf range markers, not the box frames.
8. Mixed corner language — **closed.** One monoline rounded grammar throughout.
9. 390 — **closed.** home-390-0…4.png: no overflow, panel and icons clean.

### Findings

1. ideas@1440, home@390 ideas tile: idea-09 ("Custom lint rules became economical…")
   reads as *underwater search* at its 40 px display size — the subject's "line of code"
   is a bare rule and the wavy underline is the loudest shape. Cold readers name water,
   not code.
   - Evidence: icon-sheet-96-52-32-b.png idea-09 (32 px column), ideas-1.png `[09]` tile.
   - Rule: SUBJECTS.tsv idea-09 — "a magnifying glass over a line of code with a wavy
     underline"; the owner's ruling that icons must represent their subjects.
   - Fix: mark the horizontal element as code (two or three short segment ticks along it,
     or replace the rule with an indented two-line snippet) so the search reads as code
     search, and shorten the underline by a third.
   - Severity: blocking — it is a subject miss at the size the tile actually renders.

2. home@1440: two near-twin glyphs sit in adjacent bands — idea-02 (two browser windows
   with a check between, ideas carousel) and skill-agent-ready-workspaces (browser +
   terminal with a check, skills band). A reader moving down the page can read the skill
   as "the same thing as idea 02".
   - Evidence: home-0.png `[02]` tile vs home-1.png "Agent-ready workspaces" tile;
     SUBJECTS.tsv rows idea-02 and skill-agent-ready-workspaces.
   - Rule: PLAN.md — "Each has its own subject tied to its title"; 36 distinct drawings.
   - Fix: differentiate one of the pair — e.g. give the skill's terminal window a cursor
     block (its own distinctive element) or angle/overlap the two windows so the
     composition no longer mirrors idea-02's side-by-side-plus-check.
   - Severity: medium.

3. ideas@1440: idea-07 ("Teams are now more willing to fund tooling time") loses the coin
   at 40 px — it is a small unmarked circle, so the tile reads as "clock repair" and the
   funding half of the subject disappears.
   - Evidence: icon-sheet-96-52-32-b.png idea-07 (96 px shows a coin-like circle; 32 px
     shows only a lump), ideas-1.png `[07]` tile.
   - Rule: SUBJECTS.tsv idea-07 — "a clock face beside a wrench and a coin".
   - Fix: put one inner circle (a rim) on the coin, or enlarge it ~20%, so it names as
     money at 40 px.
   - Severity: medium.

4. guides@1440 carousel and shelf grid: at 20 px, guide-01 collapses into two overlapping
   loops — a cold reader says "refresh/undo", not "mistake becomes a permanent check".
   The other four visible strip icons (02–05) name their subjects at that size.
   - Evidence: guides-strip-crop.png box 01 vs its title "Convert recurring failures into
     permanent rules"; icon-sheet-96-52-32-a.png guide-01.
   - Rule: SUBJECTS.tsv guide-01 — "a circular repeat arrow turning into a shield with a
     check mark".
   - Fix: at 20 px let the shield dominate (~60% of the box) and shrink the arrow to a
     short hook on one side; the same fix also de-duplicates it against idea-08 and the
     feedback-engineering skill glyph, which currently draw the same object identically
     (they never share a page, so this is polish, not blocking).
   - Severity: polish.

5. guides@1440: three guide glyphs keep only their primary object at 20 px — guide-03's
   terminal cursor reads as a generic card, guide-10's three nested folders read as one
   box, guide-12's resume arrow is absent. Each still names something plausible for its
   title, so none blocks; the sheet's 96 px column carries the full subjects.
   - Evidence: guides-0.png shelf grid; icon-sheet-96-52-32-a.png at 32 px vs 96 px.
   - Rule: SUBJECTS.tsv rows guide-03, guide-10, guide-12.
   - Fix: only if cheap — strengthen the distinctive element (cursor caret for 03, a
     second nested outline for 10, a bolder corner arrow for 12) without adding strokes.
   - Severity: polish.


Verdict: FIX FIRST — item 1 (idea-09 subject miss at display size, under the owner's
represent-the-subject ruling). Items 2–3 should ship with it; 4–5 are polish.

### Maker's answers

| # | Finding | Answer |
|---|---|---|
| 1 | idea-09 reads as "water search" at 40 px | **Applied.** Regenerated: a code-editor window with three code bars, the magnifier over the second, a short wavy underline under that line only. Reads as code search with a lint mark at 96/52/32 (sheet). |
| 2 | idea-02 and the ready-workspaces skill are near-twins on the home page | **Applied.** The skill glyph is now a terminal window (prompt chevron and cursor block) overlapping in front of a browser window with a check badge; idea-02 keeps its side-by-side windows. |
| 3 | idea-07 loses the coin at 40 px | **Applied.** Regenerated with a large rimmed coin carrying a currency bar; the clock and wrench are secondary. |
| 4 | guide-01 collapses to "refresh" at 20 px; identical to idea-08 and the feedback skill | **Applied.** Shield now fills most of the square with a short repeat hook on its edge; it no longer duplicates the other two. |
| 5 | guide-03 / guide-10 / guide-12 keep only their primary object at 20 px | **Applied.** guide-03 gained a terminal prompt chevron and cursor; guide-10 a compass rose over nested folders; guide-12 a bold corner resume arrow. |

Re-render: `build/check.sh` green (54 pages, 72 rendered checks at 1440 and 390). Evidence tiles for the final state are in the handbook's `.scratch/icons-v2/evidence2/`.

