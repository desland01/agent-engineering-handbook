---
name: premium-tech-design-language
description: Design vocabulary for premium, high-end technology websites — the near-black ground, hairline structure, monospace secondary text, one restrained accent, icon-tile grids and monoline illustration observed across Augment Code, Qodo, Sourcegraph, Codecademy and UX Pilot. Use when the user wants a tech site, a "terminal" or developer-tool look, names one of those references, or asks to pull from the collected inspiration; also when restyling the handbook homepage. Not for capturing a new reference site (design-language-transfer), inventing an unrelated brand direction (design-system), or the intent interview itself (ui-ux-design).
metadata:
  source-snapshot: "2026-09-10"
  references-captured: "6"
---

## Role

You are the designer who owns this premium tech language, judged against the six reference sites, not against a checklist of dark-theme tokens. Make hairlines, mono, authored drawings, and one accent form a composition worth studying—not a terminal skin pasted over the same grid.

## The defaults you will fall into with THIS language

Handed hairlines and mono, you will make these mistakes unless you stop yourself:

- **One bordered grid for every band.** A vocabulary becomes a fence around interchangeable content.
- **Drawings at icon size.** You shrink the authored figure until the section has no visual weight.
- **Every band the same height, with a rule between.** You mistake repeated separators for rhythm.
- **Mono labels standing in for hierarchy.** Uppercase metadata cannot give a heading presence.
- **The same two-column layout twice.** Text left, drawing right is your reflex, not a decision.
- **Motion as garnish.** A drifting dash or breathing halo explains nothing by merely moving.

## Commit before you build

Emit a `<design_plan>` before markup or UI code. Commit to these choices, then test them in the render:

1. Assign one figure per band from **The menu**. No two adjacent bands may use the same figure; none may appear more than twice. Do not disguise the same two-column composition with a different motif name.
2. Name each band's focal point and why it deserves the eye. Let an authored drawing carry a band instead of reducing it to an icon.
3. State each headline's intended line count at the widest and narrowest target widths, and the container and type choices that support it. Verify the actual wraps; a plan is not a measurement.
4. Name exactly one accent and where it appears. Keep meaning-hues in the small tags specified under Scale.
5. Name the motion that carries meaning, what it communicates, and its trigger; keep everything else still. State the reduced-motion treatment.
6. Sweep every ban below and remove violations before building.
7. Confirm: "no heading, label or sentence in the output is the instruction that produced it".

## Bans

- No bordered grid for every band. Reason: Repetition flattens distinct subjects.
- No icon-sized drawing as a band's focal figure. Reason: The artwork must carry visual weight.
- No uniform-height bands divided by automatic rules. Reason: Chapters need different emphasis.
- No repeated two-column composition. Reason: A changed subject deserves another figure.
- No eyebrows, decorative overlines, small uppercase kickers, or duplicate labels above headings. Reason: Labels are not hierarchy.
- No decorative numbered markers or fictitious section markers. Reason: Markers must identify something real.
- No meaningless motion or entirely still default page. Reason: Motion must explain a change.
- No drop shadow, glass, or glow. Reason: Structure belongs to lines and space.
- No hub-and-spoke, orbit, or ellipse diagram. Reason: Relationships need legible structure, not spectacle.
- No photographic or generated card art, product screenshots, or video stills as card art. Reason: Authored drawings carry the weight.
- No generated raster except measured-transparent surface texture. Reason: An opaque image is not atmosphere.
- No fabricated statistics, logos, or testimonials. Reason: Evidence is not decoration.
- No instruction text passed off as page copy. Reason: The work must name its subject.
- No emoji in code, comments, or output. Reason: This language uses authored marks.

## The menu

Choose the figure that serves the band's content; small motifs belong in a composition, not enlarged into empty filler. Icon measurements describe dense tile collections, not the size of a band's focal drawing.

- Choose an icon-tile grid: 20–24px monoline icon plus mono label in a 1px-bordered rectangle, 4px radius, about 48px tall, in a dense grid (Codecademy, 24 tiles, visual). Small icons elsewhere sit in ~32px bordered rounded squares (Augment visual).
- Choose a monoline drawing with mono captions inside the drawing (`PR → MERGE`, `TICKET`, `CVE`, `ALERT → TRIAGED`; Augment visual). Captions are part of the artwork, not placed beneath it.
- Choose a dot-matrix halftone illustration and circuit-trace hairline glyph, monochrome with one accent dot (Sourcegraph visual).
- Choose a pipeline track: accent stage bars on a dark rail, mono stage names beneath, cards above and below joined by dotted verticals (Augment visual).
- Choose a stack of cells: layers of hairline-divided cells under mono `+ GROUP` labels; an architecture view with no arrows and no hub (Augment visual).
- Choose wired file cards: hairline box with mono title and mono metadata (`auth.go · Go · 58 lines · 1.43 KB`), joined to others by hairline wiring (Sourcegraph visual).
- Choose shell idioms as typography: typed cursor `/car▌` in an accent box, `≫` opening a callout row, `→` and `↗` on mono links, time-marked `8 min read` metadata (Codecademy, Qodo visual; source stopwatch U+23F1). Render the time mark as an authored drawing, not emoji.
- Choose a bordered mono status-badge composition: checked `FREE` (source ballot-box check U+2611), `START HERE`, `Course` (Qodo, Codecademy computed/visual), spec as under Scale; author the check mark rather than using emoji.

## Scale — color and type

- Ground: near-black, `#0a0a0a`–`#0c0c0d` (Augment declared `--bg: #0c0c0d`; Sourcegraph
  visual) or barely-blue `#111013` (Qodo computed). Surfaces 3–6% lighter: `#141416`,
  `#161618`, `#1b1b1f` (Augment declared). A faint 1px hairline grid or dot grid may sit
  behind the hero and fade under a mask (Augment computed: two `linear-gradient` layers in
  `rgba(247,243,239,.11)`); it is drawn, never a photograph.
- Accent: exactly one chromatic color per page. Observed: Augment `#1AA049` (declared
  `--accent`), UX Pilot `#C7FF01`, Codecademy `#FFD300`, Sourcegraph one red-orange (visual).
  Permitted placements: one italic word in a headline, the primary button, small markers,
  mono links. When several hues carry meaning (for example one hue per skill), demote them to
  small bordered tags — Qodo's badge spec: 1px border in the hue, hue at 20% fill, 4px radius,
  8px padding (computed) — so the page itself stays neutral.
- Text: warm off-white stepped by opacity. Headings `#f7f3ef` or `#e2e2e6`; body at 65%
  (`rgba(247,243,239,.65)`); dim labels `#a0a0aa`; hairlines `rgba(247,243,239,.11)`
  (all Augment, declared/computed).
- Type: use a display voice and a secondary mono voice; no font blacklist. Two families
  with a strict division. Sans for headings and body — system sans at
  weight 500 with tracking −0.02 to −0.03em (Augment computed), or Figtree (Qodo computed),
  Apercu (Codecademy declared). Monospace for every secondary line — IBM Plex Mono (Augment,
  Qodo), Suisse Intl Mono (Codecademy), custom monos elsewhere. Mono label spec, consistent
  across references: 11px, uppercase, letter-spacing 0.14em (1.54px), 65% white (Augment
  computed). Codecademy uses mono for section headlines as well (visual): permitted, not
  required.
- Headlines: 54–76px, weight 500, line-height 1.02–1.08, tracking −1.4px (Augment and Qodo
  computed). One italic accent word is the only flourish.

## Rhythm — structure

- Section spacing is a principle, not pixel values: compose chapters with one focal point
  each; let content and project tokens determine their spacing and height.
- Radii: 0 on buttons (Augment computed), 2–4px on tiles, cards and tags (Codecademy
  declared `4px` ×21, UX Pilot `rounded-sm` ×95), 12–16px only on large panels. Pills are
  used for one element: the section marker.
- Hairlines carry structure. Grids use `gap: 1px` with the hairline color as the gap and
  `border-top`/`border-bottom` on the group (Augment computed). Cards: 1px hairline on a
  `rgba(247,243,239,.03)` fill, padding 16px. No drop shadow, glass, or glow.
- Numbered markers and section markers belong only where the number or the section is real,
  never as decoration. Section markers identify actual sections, not eyebrows: a short mono label in a bordered pill with a 1px rule
  running from it (`The problem ————`, Sourcegraph visual), or a mono label plus rule
  (`BUILD YOUR OWN /`, Augment visual). Owner rule, unchanged: no decorative overline,
  small uppercase kicker or duplicate label above a main heading. A `//` prefix inside the
  heading text (UX Pilot) is the permitted idiom.
- Drafting guides: dashed hairlines spanning the page with mono corner markers `[01]`…`[19]`
  (UX Pilot visual). Use for numbered sequences.
- Seams: transitions between bands are dithered or speckled noise strips (Sourcegraph and
  Augment, visual, observed independently), not hard edges.
- Light bands: permitted only when they carry real content of their own (Sourcegraph's
  white middle carries light product UI). Absent such content, stay dark.

## Phrasing rules

1. Relationships are shown as stacked cells, tracks, or file cards joined by hairlines.
   No hub-and-spoke, orbit or ellipse diagram.
2. No photographic or generated card art, product screenshots, or video stills as card art.
   Authored drawings carry the weight. Generated raster is permitted only as a surface texture
   and only when measured to be transparent; inspect alpha and compositing, not the prompt.
   Keep assets attributable; do not pass generated material off as project evidence.
3. Numbers on the page are counts the page can prove (`8 ideas · 4 guides`). No outcome
   statistics, logos or testimonials that are not the project's own.
4. Monospace is the secondary voice everywhere — labels, metadata, links, numbering,
   toggles. Use a display voice and a secondary mono voice; no font blacklist. The observed
   sans headline is the default; the Codecademy mono-display option under Scale remains permitted.
5. One accent; meaning-hues live in small tags.
6. Motion is a rule, not a library: it must carry meaning; a page with nothing moving fails.
   Keep everything else still; the project stack decides how. Hover lifts remain 1–3px when
   they communicate interactivity; turn everything off under `prefers-reduced-motion: reduce`.
   This supersedes rule 6’s “at most one slow dash flow or breathing halo,” including the reference starting key.
7. Verification is part of the deliverable: render at 1440 and 390, exercise interactions in
   a real browser (the preview pane throttles smooth scroll and requestAnimationFrame), and
   read computed font, color, spacing and radius values back against the vocabulary's
   evidence tags. Report drift as drift.

## Application

This skill supplies a vocabulary, not a page. It records design decisions observed on six
public sites on 2026-09-10 (Augment Code, Qodo Academy, Sourcegraph, Codecademy, UX Pilot,
and a Paper capture of Sourcegraph) as a scale (color and type), a rhythm (structure), a
set of motifs (recurring components) and phrasing rules (what keeps a composition inside
the genre). Every value in [references/vocabulary.md](references/vocabulary.md) carries an
evidence tag: `declared` (read from the site's own CSS variables or Tailwind values),
`computed` (read from the live DOM), or `visual` (read from a full-page render when both
scrape routes were blocked). Values are the references' decisions; when the project already
has tokens, map roles onto them rather than replacing them with these literals.

Preconditions: the direction "premium tech" is settled for the surface in question. If the
brief is still open, run the `ui-ux-design` intent interview first. If a new reference must
be captured, use `design-language-transfer` and fold its token map into the vocabulary here.

Outcome when applied: a composition that uses only the scale above, structures space with
hairlines, carries all secondary text in a monospace face, uses one accent, and passes
rendered verification at 1440 and 390 with computed values read back against the vocabulary.

### Handbook

Settled direction for `/Users/thebeast/Projects/agent-engineering-handbook`: Augment Code and
Qodo are primary; the other references supply secondary phrases. Load
[references/handbook-direction.md](references/handbook-direction.md) for the content-to-motif
mapping of the 19 ideas, 13 guides, 4 skills and 3 investigations and for the standing
decisions carried over from the luminous round (no hub-and-spoke diagram, no video stills on
the homepage, the 39 authored drawings retained, color-per-skill demoted to tags).

## Sources

[references/sources.md](references/sources.md) lists each reference, what it contributes,
what to leave, and the capture files kept outside this bundle. Load it when a value needs
its evidence or when adding a reference. One site's choice is an observation; the same
choice on two independent sites is a pattern.
