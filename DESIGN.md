# Design system

Source-only guidance for contributors: how the Agent Engineering Handbook looks and why.
It is never rendered or copied into `public/`. Every generated page — the map
(`index.html`), the reader template behind the guides, investigations and other Markdown
pages, the section pages (`ideas.html`, `guides.html`, `skills.html`, `investigations.html`),
the four skill pages (`skills/<name>/index.html`), the frame gallery (`evidence.html`) and
the not-found page — loads one stylesheet,
`build/assets/handbook.css`, whose first block holds the tokens listed here. Page
structure lives in `build/render.py`. Behaviour (journeys, states, keyboard, responsive
decisions) is in [INTERACTIONS.md](INTERACTIONS.md).

## The one thing to remember

**A numbered, sourced field manual, drawn like an instrument panel.** The handbook is
thirteen numbered methods and nineteen sourced ideas, each traceable to a video moment or
a pinned repository revision. The map lays the whole manual out; the reader keeps the
number, the source and the page's sections in view while you read.

The visual language is the premium-tech genre: a near-black ground, structure drawn with
hairlines rather than shadows, one accent, and **monospace carrying every secondary line**
— labels, metadata, numbering, timestamps and paths — so a single sans headline is the
only display voice. It was learned from six public references (Augment Code and Qodo
primary; Sourcegraph, Codecademy, UX Pilot secondary) and is recorded, with the evidence
behind each value, in the `premium-tech-design-language` method outside this repository.

## Typography

Three faces, each with one job, all from the reader's own system — no web font, so the
site has no network dependency and reads at native quality on developer machines.

- **Sans for every heading and for body text** (`--font-sans`: system-ui and its
  platform equivalents): the map's title, section and shelf headings, the reader's h1 and
  h2, investigation and skill titles, the brand. Weight 500, tracking −0.028em on
  headings. The serif voice of the earlier edition was retired when the page moved to
  this genre; `--font-serif` remains defined as an alias of `--font-sans` so no rule
  breaks.
- **The mono label** is the genre's signature and the reason the page reads as an
  instrument rather than a document: 11px (`--label-size`), uppercase, letter-spacing
  0.14em (`--label-track`), at the muted step. It carries the header navigation, the
  section markers, the count badges, the `[01]`…`[19]` idea numbers, evidence badges,
  "Watch at 05:06", frame timestamps, shelf ranges and directory paths.
- **Sans for reading and interface text** (`--font-sans`: system-ui…): body, use-when
  lines, navigation, chips, labels. Weight 650 for guide titles on the map and for h3/h4.
- **Mono for numbers and references** (`--font-mono`): guide numerals, counts,
  timestamps, revision hashes, paths, code, the edition date.
- **Scale (tokens):** `--text-xs` 0.8rem, `--text-sm` 0.9rem, `--text-base` 1rem,
  `--text-read` 1.0625rem (the reader body from 760px), `--text-lg` 1.15rem, `--text-xl`
  1.55rem (section headings), `--text-2xl` 2rem (shelf numerals). Titles:
  `--title-home` `clamp(2.1rem, 1.2rem + 3vw, 3.4rem)` on the map, `--title-page`
  `clamp(1.8rem, 1.1rem + 2.6vw, 2.75rem)` elsewhere. The map's title is no longer the
  largest thing on the site by a wide margin; the problem panel beside it carries equal
  weight.
- **Measure:** the reader column is `--measure` 39rem — about 75 characters at 17px.
  The map is 1200px wide because it is lists of short labels, not prose.
- **Line height:** 1.6 body, 1.2 headings, 1.08 the map's title, 1.12 page titles.

## Colour

A near-black ground, two lifted surfaces, one hairline value and one orange accent. The
ground moved off the earlier warm black to the genre's neutral near-black; the accent
stayed, because one restrained accent is exactly what the language asks for and orange is
already the handbook's.

| Token | Value | Role | Contrast on `--bg` / `--surface` / `--surface-2` |
|---|---|---|---|
| `--bg` | `#0b0b0c` | page ground | — |
| `--surface` | `#141416` | hovered tiles, code blocks, blockquotes, menu | — |
| `--surface-2` | `#1b1b1f` | inline code, table header, hover fill | — |
| `--border` | `rgba(247,243,239,.11)` | every hairline: grids, tiles, rules, badges | decorative |
| `--border-strong` | `rgba(247,243,239,.26)` | secondary button, marker pill, hovered edge | 3.3 on `--bg` (non-text ≥ 3 ✓) |
| `--fg` | `#f7f3ef` | headings, body, titles | 17.6 / 16.6 / 15.4 |
| `--muted-fg` | `#b4afa8` | leads, use-when lines, captions, nav, rail text | 9.4 / 8.9 / 8.2 |
| `--dim-fg` | `#948f89` | edition line, directory lines, speaker lines, rail labels | 6.9 / 6.5 / 6.0 |
| `--link` | `#f29764` | running links in prose | 8.9 / 8.4 / 7.8 |
| `--accent-text` | `#f37a3b` | the italic headline word, numerals, timestamps, counts, drawings | 7.3 / 6.9 / 6.4 |
| `--primary` | `#ea580c` | primary button, focus ring, brand mark, current-section marker, blockquote rule | 5.6 / 5.3 / 4.9 |
| `--on-primary` | `#0b0b0c` | text on the orange button and skip link | 5.6 on `--primary` |

There is one accent and no second hue: nothing on the page is coloured to carry meaning
that a label could carry instead. Ratios are WCAG 2.x, computed from the hex values;
every text colour passes AA for normal text on every surface it is used on. `--accent-text` exists because the raw
accent at small mono sizes on the warm ground read slightly dull; the lighter tint keeps
the same hue with more contrast. Link underlines fade to 40 % of the link colour with
`color-mix()`; browsers without it show a full-strength underline.

## Density and spacing

- **Scale:** 4, 8, 12, 16, 24, 32, 40, 64, 96px (`--s-1` … `--s-9`). Gutters 24px, 16px
  at 400px and below. Blocks set vertical padding with `padding-block` only so nothing
  overrides the gutter.
- **Map:** the opening block is 64/72px tall at desktop, 40/48 on phones; shelves are
  44px blocks (52px for the full-width ones) separated by hairlines; chapter rows have
  16/18px padding; cards 20px.
- **Reader:** 48px above the page head at desktop (32 on phones), 28px between page
  head, section disclosure and article; 40px above previous/next; 20px above the source
  line. Section headings sit 2em below the previous section with a hairline and 1em of
  padding above the text.
- **How dense it reads:** the map is dense on purpose — the problem panel, a chapter list
  of eight guides and the counts fit in the first two screens — while the reader is one
  relaxed column with the rail doing the orientation work.

## Shape, depth and motion

- **Radii: square.** `--radius-sm` 2px, `--radius` 4px (tiles, cards, tags, chips, count
  badges, the menu panel), `--radius-lg` 14px (the problem panel only). Buttons are 0.
  Exactly one element is a pill: the section marker, so that shape means "a new section
  starts here" and nothing else.
- **Depth: none.** No drop shadow, glass or glow anywhere in `main`. Structure is drawn
  with hairlines: grids set `gap: 1px` and each cell paints its own
  `box-shadow: 0 0 0 1px var(--border)`, so neighbouring cells meet on one hairline and a
  partly filled last row shows ground instead of an orphan block. The one soft mark on
  the page is the hero's drawn hairline grid, masked to fade out.
- **Motion:** border and background colour on hover, `--hover-ms` 140ms ease-out; smooth
  in-page scrolling. Under `prefers-reduced-motion: reduce` both become instant. Nothing
  animates on load; the current-section marker in the rail changes without transition.

## Hierarchy of the site

The home page discloses progressively: it makes the promise, offers the entry by problem,
shows one taste of each section, and routes out. The full sets live on their own pages.

1. **Header** — brand with the orange mark, five mono section links (Ideas, Guides, Skills,
   Investigations, Frames), a "More" menu listing every page, and "GitHub".
2. **Opening, two columns from 980px** — left: the title with one italic accent word, the
   one-sentence lead, two square buttons (`Browse the nineteen ideas` → `ideas.html`,
   `All 13 guides` → `guides.html`), the counts as five mono badges that each route to the
   page holding the set (the build fails if a count disagrees with the set), and the edition
   line. Right: the problem panel, eight rows — situation on the left, numbered tags naming
   the guide(s) that answer it. A drawn hairline grid sits behind, masked to fade.
3. **Ideas** — all nineteen, in order, as one horizontal row the reader swipes or
   arrows through: a focusable scroll region with proximity snapping, fading at the
   edge it overflows, with previous/next and an `01 of 19` counter added by the script
   (and honestly absent without it). Then `ALL 19 IDEAS AS A GRID →`.
4. **Skills** — all four, as a hairline row. They are the deliverable and fit in one row.
   Each tile's title opens the skill's page (`skills/<name>/`); the directory line keeps
   linking to GitHub.
5. **Guides** — the four source shelves as rows (range, title, count and investigation),
   each a route into `guides.html#shelf`, then `ALL 13 GUIDES →`.
6. **Investigations** — the three reports as routing rows in the same form as the guide
   shelves (`Report 01`, title, one line from the README), then `ALL 3 INVESTIGATIONS →`.
7. **Frames** — the twelve timestamps as a mono strip, each opening its frame in the
   gallery, then `OPEN THE GALLERY →`. No stills on the home page.
8. **Closing** — what was checked, and attribution with tag links to the index pages.

Each band opens with a section marker: a mono label in a bordered pill with a hairline
rule running from it. That is the only pill on the page.

**Section pages.** `ideas.html` holds all nineteen ideas in three tiers; `guides.html`
holds the thirteen guides under their shelves; `skills.html` holds the four skill tiles;
`investigations.html` holds the three reports as three full-viewport studies;
`evidence.html` holds the twelve frames at full size. Each opens with the same
marker-and-title head as a band, so a section page reads as the band unfolded rather than
as a different site — but a section page is not obliged to use the band's figure, and
the two below deliberately do not.

**The ideas, in three tiers.** Nineteen is a homework assignment; three groups of six or
seven is a hook. `ideas.html` sorts the ideas by what is behind each one, using the
`evidence_type` already recorded in `evidence/video-tips.json`: *What he actually does*
(`theo-practice`, `theo-anecdote`), *What he tells you to do* (`theo-directive`,
`quoted-post-via-theo`) and *What he's still working out* (`theo-opinion`, the sponsor
segment). The mapping lives in `render.py` and fails the build on an evidence type it
does not know, so nothing is silently bucketed. The `[nn]` numbers stay in video order;
the tier copy lives in `home.json` under `hubs.ideas.tiers`. The page leads with the
flattering tier and frames the third as candour, because the aim is that the people
named want to share it.

**The investigations, as three studies.** Each report gets a `min-height: 100svh`
section — min-height, never a fixed height, so a phone can grow past a viewport — with
its authored diagram at up to 640px on the left and, on the right, a mono metadata line
of counts the page can prove (`REPORT 01 · 10 GUIDES CAME FROM THIS · 2,457 WORDS`,
computed at render time), the title, one claim line, three or four findings edited to
parallel form from the report's own takeaway section, and a primary *Read the full
report* button. The findings copy lives in `home.json` under
`hubs.investigations.findings`. This is the one place on the site a drawing is the size
it deserves, and 10 / 2 / 1 is a more interesting fact than three equal cards implied.

**A section page writes its own head, and closes with a route out.** The head shares the
band's *form* — marker, title, lead — but not its *words*. A band introduces a set to
someone scrolling past it; a section page addresses someone who has arrived at that set
and now has to use it, so each carries its own heading, lead, browser title and meta
description in `build/home.json` under `hubs`. The headings say what the page is rather
than what it contains: *Thirteen guides, and what each one does not prove*, *Three
repositories, read rather than summarised*. Plumbing does not open a lead — the ideas
page's two source files sit in a mono line under it, and the skills page keeps *adopt one,
not all four* in the lead, where a reader meets it before choosing.

Every section page ends with **the closing route** (`.hub-next`): the *Next* marker,
*Where to go from here*, and two or three routing rows in the same hairline form as the
home page's shelves — the destination, and a quiet mono line saying why someone standing
here would want it. That line is mono but not uppercase; the label's 0.14em tracking makes
a sentence shout. Before this, a reader who reached the bottom of a set had nowhere to go
but back to the header. `build/check.py` fails if a section page has no closing route, if
it offers fewer than two destinations, or if one of them points back at the page itself.

**Page identity.** Every page carries a `<title>` that names it and a meta description
that says what is on it — the two things a search result and a shared link show, and the
only part of a page nobody proofreads by reading it. Hubs, the home page and 404 are
written by hand; a guide uses its title and the line saying who it is for; a skill uses its
own frontmatter description; every other page uses its opening prose, cut on a sentence
boundary or, failing that, a clause. `build/check.py` fails on a missing description, one
over 175 characters, one that ends mid-thought, or a title that is only the site's name.

**Two checkers.** `build/check.py` is pure Python and runs in the Vercel build; it can
prove structure, links and hashes but cannot see a rendered scrollbar. `build/check-render.js`
is the rendered half: it serves `public/` itself, opens nine representative pages at 390
and 1440 in headless Chromium, and fails on horizontal page overflow, on any overflowing
scroll region that draws scrollbar chrome, on a hub without its closing route, and on
console errors or failed requests. `build/check.sh` runs both and skips the rendered one
with a plain message when node or puppeteer is absent, so the deploy never depends on it.
It was proved to bite before it was trusted: setting `scrollbar-width` back to `auto`
failed five checks.

The other half of page identity — a canonical URL, and the Open Graph and Twitter tags a
shared link previews with — needs an absolute origin, and the site does not have one yet.
`SITE_URL` at the top of `build/render.py` is where it goes: set it to the production
origin, scheme and host with no trailing slash, and every page but `404.html` gains a
canonical matching its own path plus the share tags. Leave it empty and none are emitted,
because a canonical pointing at the wrong host is worse than no canonical at all, and
`404.html` never gets one because it is served at every path. `build/check.py` reads that
constant and enforces the two states: with it unset, no page may carry a canonical or an
`og:url`; with it set, every page but 404 must carry one that matches where it sits, and
its `og:url` must agree. A `rel="canonical"` is the one absolute href the no-network-loads
check permits, since it names an address rather than fetching one.

**Idea pages** (`ideas/NN-slug.html`, nineteen of them). Each idea is disclosed in full on
the reader shell: the drawing, the title, then *What was said*, *How to apply it*, *When it
is useful* and *Qualification* from the structured extraction, with a rail carrying the
evidence badge and speaker, the video moment and segment, the guide and skill it leads to,
the previous and next idea, and the source files. This is where the nineteen tiles' compact
form pays off: the tile is the disclosure control, the page is the content.

**Skill pages** (`skills/<name>/index.html`, four of them — the deliverable given pages).
The page head carries the skill's drawing, the mono `SKILL` context line with a link to
`skills.html`, the skill's own title and its frontmatter description as the deck. The body
renders the skill's own instructions from `SKILL.md` (its h1 is not repeated), followed by
each file in `references/` as a section headed `Reference: …`, so one page is the whole
skill. The rail carries *On this page*, *This skill* (the honest `N ideas feed it` count
with tags to those idea pages), *In the guides* (the guides that cite it) and *Adopt* — the
raw `SKILL.md` as shipped, the directory on GitHub, and the adoption page — so an adopter
never has to leave the page to install it, and the raw file stays where `adoption.md`
says it is.

## The reader

- **Page head:** a context line (`Guide 02` · of 13 · shelf link, or the page's place on
  the map), then the page's drawing — the guide's, the investigation's wide diagram, or the
  skill's — and the title. Guide titles come from the README's canonical list so the
  reader and the map agree; the Markdown file's own h1 is not rendered a second time.
- **Article:** first paragraph as a muted, slightly larger deck; h2 with a hairline; h3; code, tables and blockquotes on `--surface` inside `--radius`; tables in a
  focusable scroll region.
- **Rail (from 1100px, on the left of the reading column):** *On this page* (h2/h3 anchors, current one marked with
  an orange edge), *This guide* (number, shelf, use-when), *Sequence* (previous/next),
  *Evidence from the video* (up to two frames applied in this guide, linking into the
  gallery) and *Source* (the Markdown beside the page, and on GitHub). On a skill page the
  same rail carries *This skill*, *In the guides* and *Adopt* in those blocks' places.
- **Below 1100px:** the rail is gone; a native "On this page" disclosure sits under the
  title, and the applied frames follow the article. Previous/next cards and the source
  line close every guide at every width.

## Components

- **Tag** (`.chip`): 4px radius, `--fill`, hairline, mono accent number then label. Used
  for problem answers, idea → guide and idea → skill links, and the closing links. The
  whole tag is the target. It was a pill before this design; pills now mean section
  markers only.
- **Icon tile** (`.tiles.guides .tile`): a 34px bordered box holding the guide's drawing,
  then the mono number, title and use-when line; stretched link; hover lifts the cell fill.
- **Idea tile** (`.tile.idea`): the drawing, a `[nn]` marker at the top right, title,
  speaker, when-useful sentence, mono watch link, evidence badge, guide and skill tags.
- **Card** (`.tiles.cards .tile`): drawing, title, purpose line, honest count where one
  exists, mono path pinned to the bottom; stretched link with the ring around the card;
  the directory link keeps its own.
- **File card** (`.grid-frames figure`): mono timestamp, caption, `open →`. Carries no
  image; the frame itself is one click away in the gallery.
- **Section marker** (`.marker`): mono label in a bordered pill, then a hairline rule.
- **Header menu** (`details.menu`): a native disclosure, the panel absolutely positioned
  under its button; the four primary links are hidden inside it from 760px.
- **Section disclosure** (`details.toc-mobile`) and **rail** (`aside.rail`): the same
  section list markup in two places, shown at complementary widths.
- **Gallery frame**, **table region**, **not-found page**: as before, restyled with the
  tokens above. Frame thumbnails still appear in the reader's evidence rail and in the
  gallery — the homepage is the only surface that carries none.
- **No decoration above headings:** no eyebrow labels, overlines, uppercase kickers or
  duplicate labels. Rail labels ("On this page", "Sequence") are sidebar section labels,
  set small and sans, not kickers over a main heading. Numbers before words are followed
  by a real space in the markup so screen readers hear two words.

## Familiar versus deliberate

Familiar, and right here: dark ground, 16/17px body, hairlines, underlined links, a skip
link, a sticky rail with a section list, previous/next at the end of a chapter.

Deliberate: the mono label carrying every secondary line on a technical site; numerals,
timestamps and counts as the only "icons"; chapter lists instead of card grids for the
guides; the problem panel as the map's co-headline rather than a text list under the
title; evidence frames placed beside the guide they support; the neutral near-black ground.

## The homepage motifs

Each element of the landing page is one phrase from the language, chosen for the content
it carries:

- **Opening** — text-led, on the faded hairline grid. One italic accent word in the
  headline; two square buttons; the five counts as mono badges whose numbers the page can
  prove.
- **Nineteen ideas** — icon tiles in a hairline grid (three on the home page, all nineteen
  on `ideas.html`), each with its authored drawing, a `[nn]` marker, the speaker, when it
  is useful, the timestamp and an evidence badge; the title opens the idea's page. No video
  stills: the frames stay in the gallery.
- **Four skills** — a hairline row led by each drawing, with an honest count
  (`8 ideas feed it`) derived from `evidence/video-tips.json`; the title opens the skill's
  page, the directory line opens GitHub. The same tiles, with the adoption summary, are
  `skills.html`.
- **Thirteen guides** — on the home page, the four shelves as routing rows; on
  `guides.html`, icon tiles grouped under mono `+ Source` shelf labels with the guide range
  set mono at the right.
- **Three investigations** — on the home page, routing rows in the shelf form
  (`Report 01`, title, one line); on `investigations.html`, cards carrying the wide
  monoline diagrams, with the source file named in mono. Each report page shows its
  diagram wide in the page head.
- **Twelve frames** — on the home page, a mono strip of the twelve timestamps, each a
  route into the gallery, which is where full-size evidence belongs.

The 39 drawings (19 ideas, 4 skills, 13 guides, 3 investigations, all distinct) are
authored stroke SVG in `build/icons.py`, inlined at build time in `currentColor`, so the
page still loads nothing from the network.

## Not done, on purpose

- No light theme (the print stylesheet flips to a light palette).
- No search or filter; the map is small enough to scan and the header menu reaches every
  page.
- No icons or illustration; the frames are the only imagery and they are evidence.
- No web font, framework or build dependency beyond the pinned Markdown package. The one
  script is optional and every control works without it.
