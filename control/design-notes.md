# Design notes — home page

Notes captured 2026-09-10, from a live review of the home page. Nothing here is
decided design; it is what was asked for, in the requester's terms, plus what
was found while looking. Not rendered into the site (`build/render.py`'s
`RENDER_MD` list does not include it), so it stays out of `public/`.

## 1. The problem panel — "this should just be a design graphic"

Element: `div.pick` in `main#main > header.opening > div.wrap` — *Start with the
problem you have*, eight rows of situation → guide chips.

**Asked for:** it should read as a design graphic rather than a plain table.
Named tools that are not available in this session: Higgsfield, `gpt-image-2.5`,
a `/scrollcraft` skill (searched both enabled skills and the catalogue — no
match; the only image generation connected here is nano-banana/Gemini). A scroll
animation matching the premium-tech design language was wanted.

**Concern raised, and the reading taken.** This panel is the home page's
problem → guide router: eight situations, eleven links into the guides, and one
of the four jobs `DESIGN.md` says the home page does. A pure decorative graphic
would delete the main way a reader with a problem finds the right guide, and
`build/check.py` asserts `n_pick == 8`. So "should just be a design graphic" was
read as *it looks like a plain table and should look designed* — a graphic that
still routes. **If the links really should go, that has not been done and is a
small change.**

**State: built, verified, NOT committed.** The panel is now the design
language's drafting-guide figure — a dashed hairline spine down the left, mono
`[01]`–`[08]` markers on the spine, and one accent trace that draws down it as
the panel passes through view, with the markers turning accent as the trace
reaches them. Radius dropped from the 14px `--radius-lg` (it was the only use of
that token on the site) to the ordinary 4px. Motion is CSS scroll-driven
(`animation-timeline: view()`), behind `@supports` and
`prefers-reduced-motion: no-preference`, so browsers without it get the finished
drawing and nothing animates on load. Rendered and screenshotted at 1440.

## 2. The nineteen ideas band — horizontal swipe row

Element: `section#ideas`, heading *Nineteen ideas from the video, in order*.

**Asked for:** a horizontal scroll section that shows the cards for all nineteen
by swipe scrolling, rather than the three-card taste.

**What this changes.** The home page currently discloses progressively — three
ideas, then `ALL 19 IDEAS →` (commit `e1e5d62`). `build/check.py` enforces it:
`0 < n_taste < 19`. Showing all nineteen on the home page reverses that stated
principle, so both the check and `DESIGN.md`'s hierarchy section need rewriting
to the new intent rather than being weakened or deleted.

`premium-tech-design-language`'s handbook direction already anticipates this row
and names its requirements: native `scroll-snap`, previous/next, arrow keys,
*View all 19*, and one known defect to avoid — the trailing counter drifts,
reading `16 of 19` at maximum scroll while *next* stays enabled; *next* must
disable when `scrollLeft` reaches `scrollWidth − clientWidth`.

**State: PARTIAL, and the build currently FAILS.** Done: `render.py` emits all
nineteen tiles in a focusable `role="region"` wrapper around an
`ol.ideas.track`, and the CSS has the track, proximity snapping, the control
styles, and the row added to the shared scroll-region rule. Not done:
`handbook.js` never got the previous/next and counter code, so the controls are
styled but absent; `build/check.py` still asserts the three-card taste and fails
with `expected a taste of the ideas (1–18 tiles), found 0`; `DESIGN.md` is
un-updated; nothing was rendered-verified. The two touched files are
`build/render.py` and `build/assets/handbook.css`, both uncommitted.

## 3. The investigations band — "more creative than 3 cards with a 4th blank spot"

Element: `section#reports > div.wrap` — *Three repository investigations*, three
`ul.shelves` rows in a two-column grid, so the fourth cell is empty.

**Asked for:** something more creative than three cards with a blank fourth.

**State: NOT STARTED.** No work done, no approach chosen.

Worth knowing before choosing one: the empty cell is a property of the shared
`.shelves` two-column grid, which the guides band also uses — the guides band
has four shelves and fills it, the investigations band has three and does not.
So the fix is either a layout of its own for three items, or a composition that
does not want a fourth. The design language's own suggestion for this content is
the file-card motif — hairline boxes with mono metadata (`melee · 15 verifier
tests`) joined by hairline wiring — and each investigation already has an
authored wide diagram in `build/icons.py` (`INVESTIGATIONS`) that the band does
not currently show; the cards on `investigations.html` do show them. Standing
decision that constrains this: no hub-and-spoke or ring composition, rejected
explicitly.

## 4. The frames band — "also make this a scroll section"

Element: `section#frames > div.wrap` — *Twelve frames from the video*, currently
`ol.timestamps`: a strip of twelve mono timestamp links into the gallery.

**Asked for:** make this a scroll section too, following note 2's row.

**State: NOT STARTED.**

The conflict to settle first. Note 2's row works because an idea tile is a card
with something to look at. A frame's card art would be the frame itself, and
there is a standing decision against exactly that: *no video-frame stills on the
homepage — the twelve evidence frames remain on `evidence.html`* (recorded
2026-09-09/10 in the design language's handbook direction, alongside the
rejection of the hub-and-spoke hero). A horizontal row of twelve timestamps with
no images would scroll, but it is a strip already and gains little; a row that
earns the treatment probably wants the stills, which is the decision to revisit.

Three ways out, unchosen: revisit the no-stills decision for this band only;
build the row from each frame's caption and its *applied in guide NN* link,
which is real content the strip currently hides, with no image; or leave the
strip and treat the band as deliberately quiet next to two scrolling rows above
it — three scroll sections in one page may be two too many.

Also relevant to notes 2 and 4 together: the home page would then carry a
nineteen-card row, a twelve-item row, and whatever note 3 becomes. That is a lot
of horizontal gesture on one page, and it is worth deciding the set together
rather than band by band.

## 5. Standing rule and the motion direction

**New rule asked for: no block text on the home page.** Prompted by
`section#checked.closing` — *What was checked* and *Attribution*, two columns of
dense prose at the foot of the page. Explanation may stay where it is genuinely
needed, but it must carry premium typography, follow the design methods, and
have a visual aspect. It must look good.

**Motion.** The site is static and flat and needs life: GSAP scroll animation or
Framer-Motion-style fade-in / slide-in / slide-up reveals, hover states, and one
small piece of Three.js fun — a terminal or another coding-specific animation,
not overdone. Pull from the sites collected for the premium-tech design
language. The bar: Theo, Matt Pocock and Boris Cherny should want to share it.

**Tooling, corrected.** Higgsfield *is* available — not as an MCP connector,
which is all I checked the first time, but as a CLI: `@higgsfield/cli@1.1.13` at
`~/.local/bin/higgsfield`, authenticated, with `generate`, `model`, `workflow`,
`upload` and `marketing-studio` subcommands. There is still no `gpt-image-2.5`
and no `/scrollcraft` skill.

**Constraints this has to live inside.** `build/check.py` fails any page that
loads from the network, so GSAP and Three.js must be vendored into
`public/assets/` rather than pulled from a CDN, and their weight is then part of
the page. The site is static Python-rendered with no JS bundler. Every control
must still work with the script absent — that is a stated property of
`handbook.js`. And the design language's own motion rule is currently *at most
one slow dash flow or breathing halo; hover lifts 1-3px* — "motion, big time"
supersedes it, and the rule needs rewriting rather than quietly breaking.

## 6. No scrollbars anywhere — "we need some check.sh to stop the scroll bars"

Prompted by the reader's rail, which still shows a scrollbar when its six blocks
overrun the viewport. Commits `6d3b8e2` and `8b0da64` deliberately gave it a
*thin quiet* scrollbar and recorded that only trimming the rail's contents would
remove it. That decision is now reversed: no scrollbars.

**State: PARTIAL, uncommitted, unverified.** `handbook.css` now hides scrollbar
chrome on all four in-page scroll regions (`scrollbar-width: none`,
`::-webkit-scrollbar` zeroed) and fades the region at the edge it overflows
instead — a `mask-image` that lifts once the reader reaches the end, so the page
never implies more content than exists. `handbook.js` gained the controller that
toggles `is-overflowing` / `is-at-end`. Nothing has been rendered or looked at.

**The check does not exist and is the harder half.** `build/check.py` is pure
Python with no browser, so it cannot see a rendered scrollbar; it can only
assert that the CSS declarations are present, which is not the same claim. A
real check has to measure `scrollWidth`/`clientWidth` and computed styles in a
browser — a rendered check, which means node and a headless browser become
project dependencies of a site that currently has exactly one dependency
(`Markdown==3.10.3`) and a build command Vercel runs with plain `python3`. Worth
deciding deliberately: a `build/check-render.js` plus a `build/check.sh` that
runs both, versus keeping the checker dependency-free and accepting that
scrollbars are verified by eye.

Related decision still open from the CSS above: tables and code blocks were the
two regions whose scrollbar *was* the only signal they scroll sideways. They are
focusable keyboard scroll regions, and the rows have previous/next, but hiding
every bar site-wide should be looked at on a touch device before it is kept.

## 7. Too much space between the reading column and the rail

Element: `main#main.wrap.reader` on a guide page.

**Asked for:** the gap between the main body text and the side rail is far too
wide.

**State: NOT STARTED.**

The measurement, for whoever picks it up: at 1100px and above the reader is
`grid-template-columns: 248px minmax(0, var(--measure))` with
`column-gap: 72px` and `justify-content: space-between`
(`build/assets/handbook.css:381`). `space-between` is what actually causes it —
the two columns are pushed to the page's outer edges and the leftover width all
collects in the middle, so the real gap is 72px *plus* whatever the page is
wider than `248px + --measure`. At 1440 that is far more than 72. The comment on
that rule says both columns sit at the page's edges deliberately, to line up
with the header and footer, so the fix is a genuine trade between that alignment
and a readable relationship between rail and text.

## 8. Nineteen is a homework assignment, not a hook

**Asked for:** either combine the nineteen ideas into ten or fewer, or break
them into two or more categories. Lists say *top 7* or *top 10* because that is
a hook; *Nineteen ideas, each timestamped and mapped to a guide* — my headline,
pointed at twice — reads as an assignment and will make visitors bounce.

Agreed, and it is my error: I optimised that headline for precision about the
set and never asked whether anyone wants a set of nineteen.

**The data already contains two groupings.** Counted from
`evidence/video-tips.json`, not invented:

| Cut | Groups | Sizes |
|---|---|---|
| By `suggested_skill` | 4 | 8 / 4 / 4 / 3 |
| By `evidence_type`, collapsed by evidential force | 3 | 6 / 7 / 6 |

Also true and unused: **all nineteen carry a `caveat` field**, and the speaker
breakdown is 12 Theo, 5 Boris-as-quoted-by-Theo (three of them endorsed or
partially endorsed), 1 Theo recounting Twitch, 1 sponsor segment.

### Option A — four patterns, by the skill each feeds

Groups of 8 / 4 / 4 / 3 under the four skills. Honest, costs no new editorial
claim, and makes the ideas-to-skills relationship visible for the first time —
right now that mapping exists in the data and is shown only as a small tag. The
8 is lopsided, and the group names are internal vocabulary rather than a hook.

### Option B — three tiers, by what is actually behind each idea (recommended)

`theo-practice` + `theo-anecdote` = **6, things he actually does**;
`theo-directive` + `quoted-post-via-theo` = **7, things he tells you to do**;
`theo-opinion` + `sponsor-ad-framing` = **6, things he only reckons** (5 + 1; an earlier draft of this note said 5, which does not sum to 19 — the T5 worker caught it).

Why this one:

- It is a genuine hook, and the hook is the handbook's whole argument. Every
  other summary of that video gives you a flat list; this one tells you which
  advice is backed by something and which is a man thinking out loud. That is a
  reason to click and a reason to share.
- Three groups of 6 to 7 is exactly the scannable size the *top 7* instinct is
  reaching for — three times over, without discarding anything.
- It costs no new editorial judgement. The `evidence_type` values were extracted
  and published already; this only groups by a field the cards are colouring in
  anyway.
- It is the site's stated ethic — separating inspected code from author-reported
  results — applied to the ideas instead of only to the investigations.

**The risk, and it is real.** A cut that separates a named person's practice
from his opinions can read as a takedown, and the goal is that Theo, Matt and
Boris *want* to share this. Handling: the tier that leads is *things he actually
does*, which is the flattering one; the third tier is framed as candour rather
than as a demerit, and the video itself flags several of these as speculative —
idea 18 is literally labelled *with a grain of salt* by Theo. Wording matters
more than structure here. *Things he only reckons* is probably too arch for the
page even if it is the honest gloss; *what he is still working out* or *offered
as opinion* keeps the same separation without the smirk.

### Option C — an editorial top seven

Promote seven, keep the rest behind *all nineteen*. Strongest possible hook,
but it is the one option that requires a judgement the handbook has so far
refused to make, and the ranking would be unfalsifiable — awkward for a site
whose selling point is that every claim is traceable. Available if wanted; not
recommended as the default.

### Knock-ons whichever is chosen

The home row from note 2, the ideas hub, `home.json`'s ideas copy, and
`check.py`'s idea assertions all key off a flat set of nineteen and would each
need rewriting. Headline candidates to replace the current one: *What Theo does,
what he tells you to do, and what he is still working out*, or the shorter
*Nineteen ideas, sorted by what is behind them*.

## 9. "This whole page is too blocky and boring. FAIL"

A verdict on the guides page, and it lands on the whole site. It is also the
most useful note here, because it says the other eight are aimed at the wrong
level: I have been planning local repairs to a composition whose problem is
global.

### The diagnosis, measured

**The site has one figure and uses it for everything.** Six different content
types are drawn as the same `gap: 1px` bordered cell grid — `.ideas`,
`.tiles.cards`, `.tiles.guides`, `.grid-frames`, `.shelves`, and the
`.hub-next ul` I added two commits ago. Nineteen ideas, thirteen guides, four
skills, three investigations, twelve frames and a set of routes are six
genuinely different kinds of thing, and a reader meets them as six grids of
rectangles. That is the blockiness: not any one band, but the absence of any
reason to look at one band differently from the last.

**The drawings are treated as decoration.** There are 39 authored stroke
drawings — the most distinctive asset the project has — rendered at 20px inside
a 34px box on a guide tile, 40px on an idea tile, 52px on a skill tile. Only the
three investigation diagrams get real size at 190px, and they are the only
figures on the site anyone would call striking. The illustration set is doing
almost no visual work.

**The design language already names the fix and the site ignores it.** The
premium-tech vocabulary lists five distinct motifs — the icon-tile grid, the
monoline drawing with mono captions *inside* the artwork, the pipeline track,
the stack of hairline cells under `+ GROUP` labels, and the file card joined by
hairline wiring. The site implements the first one, six times. Augment does not
put its loops, its pipeline and its architecture in three grids; it uses a
2x2 of tall illustrated cells, a track, and a layered stack. That variation is
most of what makes those pages feel designed.

Three further contributors, smaller: every band is separated by the same 1px
rule where two independent references use dithered halftone seams; every heading
is the same sans at nearly the same size, where Codecademy uses mono as a
display face for section headlines; and nothing on the page varies in scale, so
there is no focal point in any band and therefore nowhere for the eye to land.

### What this changes about the plan

Adding motion to six identical grids gets six identical grids that move. The
composition has to come first: **give each band the figure its content actually
wants**, then animate what is there.

A band-by-band proposal, each drawn from a motif already in the vocabulary:

| Band | Now | Proposed figure |
|---|---|---|
| Four skills | grid of 4 cards, 52px glyph | Augment's *loops*: 2x2 hairline cells, each carrying its drawing at full size with mono captions inside the artwork |
| Thirteen guides | four grids of small tiles | a **track** — numbered stages on a rail, grouped by source, the pipeline motif |
| Nineteen ideas | grid of 19 identical tiles | note 8's three tiers, as a drafting figure with `[01]`-`[19]` markers on dashed guides |
| Three investigations | 3 cards in a 2-col grid with a hole | note 11: three full-viewport sections on the hub, diagram at full size, ending in a CTA |
| Twelve frames | mono timestamp strip | leave quiet, deliberately — it is the contrast that lets the others breathe |
| Closing prose | two columns of block text | note 5: typographic, with the reading-progress dim |

Plus: raise the drawings to a size where they carry weight; dithered seams
between bands instead of hard rules; and one mono display headline somewhere to
break the sans monotony.

### An honest note on the work so far

Commits `e88d6b4` and `f4157b1` improved the writing, the routing and the page
identity, and did nothing whatsoever about composition. On the axis this note is
judging, that work does not defend itself, and the FAIL is fair.

## 10. No typographic hierarchy inside the reader

**Asked for:** the rail differentiates the sections, but the article itself gives
no typographic signal of where a section starts. A design failure.

Confirmed, and it is measurable. Computed values from
`skills/agent-feedback-engineering/index.html` at 1440:

| Element | Size | Weight | Step down from the level above |
|---|---|---|---|
| `h1` | 44.0px | 500 | — |
| `h2` | 24.8px | 500 | **1.77x** |
| `h3` | 20.1px | **650** | **1.23x** |
| body | 17.0px | 400 | 1.18x |

Two defects, and the second is a plain bug.

**The scale collapses after the title.** A 1.77x drop from `h1` to `h2`, then
1.23x, then 1.18x. Almost the whole range is spent between the page title and
the first section heading, leaving `h2`, `h3` and body inside four points of
each other. By the time a reader is in the article there is no size signal left
to spend.

**Heading weight is inverted.** `handbook.css:79-80` sets `h1, h2` to weight 500
and `h3, h4` to **650**. So an `h3` is 21% smaller than an `h2` and 30% heavier.
On screen the subsection reads as *more* emphatic than the section that contains
it — which is exactly the reported symptom, and it is one line of CSS.

**What is actually marking sections today** is `border-top: 1px` on `.reader h2`
(`handbook.css:465`). A hairline is a graphic device, not typographic hierarchy;
it is doing a job the type should be doing, and it is why the sections read as
undifferentiated when you are inside the prose rather than scanning the rail.

**A third problem specific to skill pages.** The generated `Reference: ...`
headings are `h2`, the same level as the skill's own sections, so *this is a
different document now* and *this is the next part of the same argument* look
identical. Those want a level of their own — the vocabulary's `+ GROUP` mono
label over a rule would separate a whole appended document from a section
heading without inventing a fifth size.

**Fix direction.** Re-space the scale so the steps are even rather than
front-loaded (roughly 1.4x between adjacent levels), correct the weight
inversion so heading weight descends monotonically, and let `h2` carry more of
its own signal — size, space above, and optionally a mono section number — so
the hairline becomes reinforcement rather than the only cue. This is one of the
cheapest high-value items on the whole list: it is a handful of declarations and
it improves all 54 pages at once.

## 11. The three investigations as three full-viewport sections

**Asked for:** turn the three investigation cards into three sections, each
roughly a full viewport, that explain why the investigation matters, carry
visuals, and end with a *learn more* call to action opening the full write-up.

This also answers note 3 ("more creative than three cards with a fourth blank
spot") and gives note 9's biggest complaint — that the authored drawings are
rendered as postage stamps — the one place on the site where a diagram can be
the size it deserves.

### What already exists to fill three viewports

| | Theo: T3 Code and Melee | Matt Pocock: Course Video Manager | Boris Cherny: public work |
|---|---|---|---|
| Full report | 2,457 words | 1,646 words | 1,122 words |
| Authored diagram | yes, `160x80` viewBox, scales to any size | yes | yes |
| Guides traceable to it | **10** (01-10) | **2** (11-12) | **1** (13) |
| "Why it matters" copy | `## What to take away`, 155 words, 4 numbered points | `## How this changes our guides`, 82 words, prose | `## What this adds...`, 91 words, prose |

So the argument for each is already written — it is just filed under three
different headings and in three different shapes.

### The structure each section wants

1. A **claim** in display type — why this repository is worth reading. *New copy,
   three lines total, and the only genuinely new writing this needs.*
2. The **diagram**, finally at full size, as the section's visual weight.
3. **Two to four concrete findings**, from the existing takeaway sections,
   edited to parallel form so all three read alike.
4. **Honest metadata**, mono: `10 GUIDES CAME FROM THIS · 2,457 WORDS · SNAPSHOT
   a276aeb`. The guide counts above are real and traceable, and 10 / 2 / 1 is a
   more interesting fact than three equal-looking cards imply.
5. The **CTA** into the full report.

### Three things to decide before building it

**Where this lives.** Three full viewports belong on `investigations.html`,
whose entire job is these three. Putting them on the home page adds three
screens to a page that already has six bands, and the home band should stay a
compact route. Recommend: rebuild the hub, leave the home band alone.

**`100vh` is the wrong unit.** On mobile it means the viewport *including* the
browser chrome that disappears on scroll, so a section sized that way jumps and
clips. `100svh` with a `min-height` rather than a fixed height, so a section can
grow past a viewport when its content needs to, is the safe form. At 390x844
with a large diagram, a title, four findings and a CTA, the honest answer is
that it will exceed one viewport on a phone, and it should be allowed to.

**This is the one place GSAP might earn its 44 KB.** A pinned section whose
diagram draws itself as the reader scrolls through it is exactly the effect
ScrollTrigger exists for. Native `animation-timeline: view()` can do a
reveal and a scrub for 0 KB but cannot pin. Worth prototyping the native version
first and only reaching for the library if pinning turns out to be the thing
that makes it feel good.

### The risk

Three full-viewport sections is the most common way a site becomes tedious —
scroll-jail with one idea per screen. What protects it here is that each section
carries a real diagram, real counts and a real argument rather than a headline
and a gradient. If a section cannot fill a viewport with substance, it should
not take one.

## Research findings

Measured 2026-09-10, not estimated.

**What the site weighs now.** `handbook.css` 10 KB gzipped, `handbook.js` 2 KB.
Twelve kilobytes of assets for fifty-four pages. That is the number every
library below has to justify itself against.

**Library weights, as the single file we would vendor** (nothing may come from a
CDN — `check.py` fails any page that loads from the network):

| Library | gzipped | multiple of the site's current assets |
|---|---|---|
| GSAP core + ScrollTrigger | 44 KB | 3.7x |
| Motion (Framer's vanilla build) | 45 KB | 3.8x |
| Three.js (`three.module.js`, the smaller build) | 128 KB | 10.7x |

**Higgsfield, corrected twice over.** It is installed and authenticated
(`@higgsfield/cli@1.1.13`), the account is on the ultra plan with 5,847 credits,
and `gpt_image_2_5` — GPT Image 2.5, the exact model asked for — is in its model
list, taking `aspect_ratio`, `quality` up to `max`, `resolution` up to 4k and,
importantly, `background: transparent`. My first two answers, that neither was
available, were both wrong: I checked MCP connectors and never checked the
shell. There are also text-to-3D and image-to-3D models, but anything they
produce needs a 3D renderer to show, which puts it behind the Three.js number
above.

**The references already contain a motion vocabulary**, which is better than
inventing one. From `sources.md`:

- **Sourcegraph: reading-progress fade** — body text dims past the point the
  reader has reached. This is the answer to note 5: it makes prose visual and
  moving without adding a picture to it.
- **Codecademy: the typed `/car▌` cursor in an accent box**, and `≫` as a
  shell-prompt glyph. This is the coding-specific set piece, and it is *text* —
  no 3D library can make it better.
- **Augment and Sourcegraph, independently: dithered / speckled halftone seams**
  between bands rather than hard edges. Two independent sites doing it makes it
  a pattern rather than a quirk, and it is the one place a generated raster
  would genuinely help.
- **UX Pilot: dashed drafting guides with `[01]` corner markers** — already
  shipped, in note 1's problem panel.

## The plan

### Recommendations, with the reasoning

1. **Write the motion by hand; do not vendor GSAP.** The reveal vocabulary asked
   for — fade in, slide up, slide in, hover — is `IntersectionObserver` plus CSS
   transitions, and scroll-linked effects are native
   `animation-timeline: view()`, which is already working in this codebase in
   note 1's panel. Cost: 0 KB. It also preserves the site's stated property that
   every control works with the script absent. Revisit GSAP only if a pinned,
   scrubbed set piece is wanted that native cannot express — a real possibility,
   and 44 KB is affordable for one genuine centrepiece, but not for fade-ups.
2. **Do not vendor Three.js.** 128 KB gzipped against a 12 KB site, for
   decoration, on a page whose whole argument is that it is careful. If GPU
   effects are wanted, a hand-written WebGL fragment shader for the dithered
   seam is roughly 2 KB and delivers the one motif two references share. The
   terminal piece does not want 3D at all.
3. **Use Higgsfield for texture, not for card art.** Generate the halftone and
   dither seam strips with `gpt_image_2_5 --background transparent`, monochrome,
   to sit on the near-black ground. The 39 authored drawings stay the
   illustration identity; a generated raster earns a place as a *surface*, which
   is what both reference sites use it for. This keeps the standing decision
   against photographic card art intact.

### Phases

Reordered after note 9. Composition leads; motion decorates what is already
worth looking at. Notes 8 and 9 together decide the shape of most of the page,
so they come before any polish that would otherwise be done twice.

- **Phase A - decide the two shapes.** Note 8's grouping and note 9's
  band-by-band figures. These are decisions, not code, and everything below
  depends on them.
- **Phase B - recompose the bands.** The table in note 9, one band at a time,
  starting with the skills 2x2 and the guides track, since those are the two the
  FAIL was aimed at. Includes raising the drawings to a size that carries.
- **Phase C - seams and type.** Note 10's reader scale first — it is a handful
  of declarations and it fixes all 54 pages, including the weight inversion,
  which is a one-line bug. Then dithered band seams, one mono display headline,
  and the scale variation that gives each band a focal point.
- **Phase D - motion.** Only now, over compositions worth animating.
- **Phase E - the set piece and the closing section.** The typed terminal, and
  note 5's no-block-text rule.

The original phases below still hold as the repair backlog and slot underneath:

- **Phase 0 - unblock.** Finish note 2 (previous/next and counter exist in
  `handbook.js` but have never been run), rewrite the taste assertion in
  `check.py`, verify note 6's scrollbar hiding and fades render, update
  `DESIGN.md`. Get to PASS and commit, with note 1's finished panel.
- **Phase 1 - the rail gap.** Note 7. Small, self-contained, and it makes every
  guide page better.
- **Phase 2 - the motion system.** Reveal-on-scroll for band heads, tiles and
  rows; hover lifts; the reading-progress dim on long prose. Hand-written,
  behind `prefers-reduced-motion`, degrading to the finished layout. Amend the
  design language's motion rule, which currently says *at most one slow dash
  flow*, to whatever this actually becomes.
- **Phase 3 - the closing section.** Note 5's no-block-text rule, using the
  reading-progress dim plus a typographic restructure.
- **Phase 4 - the set piece.** The typed terminal, authored, in the hero or the
  closing band.
- **Phase 5 - seams and texture.** The dithered band seams, with Higgsfield
  generating the strips; optionally the 2 KB shader if a static strip is not
  enough.
- **Phase 6 - the remaining bands.** Notes 3 and 4: investigations, frames.
- **Phase 8 - regroup the nineteen.** Note 8. Sequenced late only because it
  needs a decision; if the answer comes early it should move to the front, since
  it changes the home row, the ideas hub and their copy, and doing it after
  those are polished means polishing them twice.
- **Phase 7 - the scrollbar check.** Note 6's second half. Needs a browser, so
  it means `build/check-render.js` and a `build/check.sh` that runs both, with
  node and a headless browser as *developer* dependencies only — Vercel's build
  command keeps running plain `python3` and must not start needing them.

## Delegation log

Three tickets ran on `glm-5.3-flash` through `nautilus_fleet.delegate` on 2026-09-10:
T3 (investigations studies), T5 (idea tiers), T4 (rendered check). All three delivered
`deliverable.patch` + `RESULT.md`, applied cleanly to baseline `e260f6c`, passed
`check.py` in isolation, and were integrated with one append-conflict in `handbook.css`
(both appended a block at the end; both kept). First admission was refused on
`scope_canonical`: a `python3 -m venv` puts symlinks to the system interpreter inside
the workspace. `python3 -m venv --copies` fixes it. T5 caught an arithmetic error in
note 8 (6/7/6, not 6/7/5). T4's script was unexecuted in the sandbox (no browser) and
ran green at the parent first time, then was proved to fail when the rule it guards was
broken.

**Fleet gap, 2026-09-10 15:18.** A fourth ticket (T9, the motion system) was admitted
under the new current release `skill-packs-20260910b` but ended `blocked` with
`run_observer_error` after zero model requests. Both required Charts reported
`available: false`: that release has no `charts/core-skills/bundles` directory at all,
so no Chart can be delivered to any worker on it. The route is unavailable until the
release carries its Charts; the assignment was small and fully specified, so it was done
at the parent instead. Also learned: `~/.nautilus/current` moved between dispatches, and a
workspace is only exempt from the installation-home overlap check when it sits under the
*current* release's `var/workspaces` — a workspace built under the previous release is
refused with `workspace_overlaps_installation_home`.

**Higgsfield, tried and not adopted (2026-09-10 15:25).** One `gpt_image_2_5` job,
5.5 credits, 21:9 at 2k, `background: transparent`, prompting for a crisp monochrome
Bayer-dither strip on a transparent ground. The result is 2688x1152, 2.8 MB, and
100% opaque: a painted light-grey wash with a soft blurred edge and sparse white dots,
not a dither and not transparent. Kept for evidence at
`scratchpad/hf/seam-raw.png` (outside the repo). The seam was built instead as an
authored CSS halftone - two dot layers at 4px and 7px pitch, each masked to thin
downward - which is crisp, 0 bytes of assets, and matches the two references' idiom.
Conclusion for this site: generated raster texture did not earn a place next to the
39 authored drawings; the terminal set piece needed no 3D and no library either.

**Route cap removed, 2026-09-10.** The `gpt-6-astra` route descriptor carried
`limits: {maxSeconds: 900, maxRequests: 60}` while the release anchor's entry for that
route has `limits: null`, like every other admitted route. A descriptor narrower than the
authority imposed an arbitrary cap the founding principles forbid; on the owner's
direction it is now `null / null`, matching the anchor and the other three descriptors,
with a dated note in the descriptor. `verify-routes.py` passes all four. What remains and
is *not* a route cap: the anchor's top-level `maxSeconds: 600`, a runtime setting changed
only through `nautilus settings propose --max-seconds N` then `apply`.

**The moving release.** `~/.nautilus/current` changed three times in one session
(premium-tech-design → skill-packs → premium-tech-design → task-file). A capsule is sealed
to one release digest and a workspace is exempt from the installation-home check only
under the *current* release's `var/workspaces`, so a dispatch prepared against one release
and launched after a switch is refused — `release_mismatch` or
`workspace_overlaps_installation_home`. The reliable pattern is to bind the workspace and
digest at the moment of dispatch, in the same step as the launch.

**gpt-6-astra, two runs, 2026-09-10.** The first combined run (copy + QA, 22 full-page
PNGs as evidence) died on `run_stdout_limit` after 12 requests and 23 Reads with nothing
delivered: reading large images is what fills the stdout budget. Split into two runs. The
QA-only run (8 JPEGs at 800px wide) completed in 17 requests and delivered
`control/design-qa-20260910.md`; four of its eight images still failed the route's image
reader because full-page captures are 5,000-9,000px tall and the reader refuses anything
over 2000px on either axis — tile evidence to ≤2000px both ways. Its three findings were
confirmed by measurement at the parent; two mobile concerns were checked and are not
defects. Report-only by owner instruction; nothing applied.

**gpt-6-astra copy run, 2026-09-10.** Completed and delivered 98 JSON fields and 15
renderer literals rewritten, with a before/after/why table for every one, American
spelling made consistent (the count favoured it 41:2), every meta description 148-167
characters. Its `deliverable.patch` came back empty because my task named the *parent
repo's* commit hash as the diff base and the worker's checkout has its own root commit;
the worker reported this exactly and did not guess. The patch was generated at the parent
from the workspace (`git diff HEAD -- build/home.json build/render.py`), applied cleanly,
and passed both checkers in isolation. Lesson: give a worker a base it can resolve — its
own `HEAD` — never a hash from another repository.

## Open questions

1. Should the problem panel keep its eleven guide links, or become decoration
   with the routing moved somewhere else?
2. With all nineteen ideas on the home page, what is the ideas *band* for that
   `ideas.html` is not? Both would now carry the full set.
3. Is a Higgsfield / `gpt-image-2.5` route going to be connected? Raster art
   would be the first non-authored, non-SVG image on a site whose identity is 39
   monoline drawings in `currentColor` that follow the theme, and the design
   language currently rules out photographic card art.
4. How many horizontal scroll sections should the home page have? Notes 2 and 4
   each ask for one, and note 3 may want a third.
5. Does the no-video-stills-on-the-homepage decision still hold? Note 4's band
   is hard to make worth scrolling without it.

## Working state

Executing since "build out the plan and execute". Commits, newest first:

```
7d9865e Type the four skills as slash commands under the hero
99e867f Say what the site is, close it with a ledger, and let the page move
983cbb5 Draw the four skills as loops and the thirteen guides as a track
078c87d Sort the ideas into three tiers, give each investigation a full viewport, and add a rendered check
e260f6c Give the reader a type scale that steps evenly, and close the rail gap
06b2168 Carry all nineteen ideas on the home page as a row, and draw no scrollbars
f4157b1 Leave one place to fill in the production origin
e88d6b4 Write each section page its own head, and a route out of it
8b0da64 Give every scroll region on the site the same treatment
```

Done: notes 1, 2, 5, 6 (both halves), 7, 8, 9 (skills, guides, ideas, investigations,
seams, drawings at size), 10, 11; the hero copy; the motion system; the typed prompt.
Deliberately left: note 4 (the frames band stays a quiet timestamp strip, as the
contrast between two rows above it — see note 4's own reasoning). Not adopted: Three.js,
GSAP, the Higgsfield raster (all recorded above with the numbers). Every commit passed
`check.py` (54 pages) and, from `078c87d` on, `check-render.js` (72 rendered checks) at
1440 and 390.

- Committed and clean: `e88d6b4` (section-page heads, closing routes, meta
  descriptions), `f4157b1` (the `SITE_URL` marker for canonical and share tags).
- Uncommitted: `build/render.py`, `build/assets/handbook.css`,
  `build/assets/handbook.js`, and this file.
- **`python3 build/check.py` FAILS**: `index.html: expected a taste of the ideas
  (1-18 tiles), found 0`. Note 2 replaced the three-card taste with all nineteen
  and the assertion was never rewritten to match.
- `public/` has been rebuilt from that partial source, so it matches neither
  commit.
- What is finished in the working tree: note 1 (the problem panel, verified by
  screenshot). What is half-finished: note 2 (row renders, `handbook.js` now has
  the previous/next and counter code but it has never been run) and note 6 (CSS
  and JS written, never rendered).
- Two clean ways back: commit note 1 alone and revert the rest, or finish note 2
  and note 6 and get to PASS. The second is roughly where phase 0 of the plan
  was heading when it stopped.
