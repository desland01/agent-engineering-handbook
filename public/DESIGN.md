# Design system

How the Agent Engineering Handbook looks, and why. Every generated page — the map
(`index.html`), the reader template behind the guides, investigations and other
Markdown pages, the frame gallery (`evidence.html`) and the not-found page — loads one
stylesheet, `build/assets/handbook.css`, whose first block holds the tokens listed here.
Change a value there and every page follows. Behaviour (journeys, states, keyboard,
responsive decisions) is in [INTERACTIONS.md](INTERACTIONS.md).

## The one thing to remember

**A navigable map of evidence-backed engineering methods.** The landing page is not a
funnel or a sales page: it is the whole handbook laid out on one screen — thirteen guides
grouped by the source each was adapted from, three investigations, four portable skills,
nineteen timestamped ideas and twelve frames — so a reader can see the shape of the
material and its provenance at a glance, then go straight to the one thing they need.
Every choice below serves that: large numerals instead of icons, provenance in the shelf
headings, real counts in the contents strip, and hairlines instead of decoration.

## Typography

- **Family:** the system sans (`system-ui, -apple-system, "Segoe UI", Roboto,
  "Helvetica Neue", Arial, sans-serif`) for text; the system mono (`ui-monospace,
  SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace`) for guide numerals,
  timestamps, paths, hashes and code. No web font is loaded, because the handbook is
  read on developer machines that already have good system faces, because a network font
  would be the site's only network dependency, and because the material is text-heavy —
  reading comfort matters more than a distinctive face.
- **Scale (tokens):** `--text-xs` 0.8rem (directory lines, thumbnail captions),
  `--text-sm` 0.92rem (use-when lines, table cells, notes), `--text-base` 1rem body,
  `--text-lg` 1.15rem (leads), `--text-xl` 1.5rem (shelf and reader h2), `--text-2xl`
  2.2rem (tile numerals). Titles: `--title-home` `clamp(2.4rem, 5.5vw, 4rem)` for the map's
  h1 — the largest thing on the site, because the map is the one place that announces
  the handbook — and `--title-page` `clamp(1.9rem, 4vw, 2.6rem)` for every other page,
  where the content, not the title, should dominate.
- **Weights:** 700 for headings, tile titles and the brand; 600 for problem-picker
  questions, contents-strip labels and the current nav item; 400 for everything else.
  Bold marks *what you can choose*; regular carries *what it says*.
- **Line height:** 1.6 for body text, 1.2 for headings, 1.05 for the map's title.
- **Measure:** reader pages are one column of `--measure` 48rem (about 72 characters at
  16px). The map is wider (1240px) because it is a grid of short labels, not prose.
- **Letter-spacing:** headings −0.02em, the map's title −0.035em. Familiar for a large
  sans; it keeps the big title from looking loose.

## Colour

Dark ground, near-white text, one warm accent. This palette is inherited from the
handbook's earlier pages and kept deliberately: readers arrive from a dark editor or a
dark video player, and the orange marks *the way forward* (links, focus, the numbers in
the contents strip) without competing with the frames.

| Token | Value | Role | Contrast on `--bg` / `--card` / `--muted` |
|---|---|---|---|
| `--bg` | `#0b0b0f` | page ground | — |
| `--card` | `#111114` | tiles, code blocks, blockquotes | — |
| `--muted` | `#18181b` | inline code, table header | — |
| `--border` | `#27272a` | hairlines | decorative, no requirement |
| `--border-strong` | `#8b8b95` | hovered or focused tile edge | 5.8 (non-text ≥ 3 ✓) |
| `--fg` | `#fafafa` | headings, body text | 18.8 / 18.1 / 17.0 |
| `--muted-fg` | `#a1a1aa` | leads, use-when lines, captions, nav | 7.7 / 7.4 / 6.9 |
| `--dim-fg` | `#8b8b95` | attribution line, tile numerals, directory lines | 5.8 / 5.6 / 5.3 |
| `--link` | `#f08a55` | links | 7.9 / 7.6 / 7.2 |
| `--primary` | `#ea580c` | focus ring, contents-strip numbers, gallery timestamps, blockquote rule | 5.5 / 5.3 / 5.0 |
| `--on-primary` | `#0b0b0f` | text on an orange fill (the skip link) | 5.5 on `--primary` (the same pair as `--primary` on `--bg`) |

Ratios are WCAG 2.x, computed from the hex values. Two colours were corrected from the
earlier pages because they failed AA for normal text: the dim grey was `#71717a`
(4.1 / 3.9 / 3.7 — below 4.5) and is now `#8b8b95`; the skip link was white on orange
(3.6) and is now the page ground on orange (5.5). The orange itself passes as small text
on every surface, so the contents-strip numerals and gallery timestamps may use it; the
lighter `--link` is kept for running links because underlined 16px text on a dark ground
reads better a little lighter than the accent.

The stylesheet uses `color-mix()` once, to fade link underlines to 45 % of the link
colour; browsers without it show a full-strength underline.

## Density and spacing

- **Scale:** 4, 8, 12, 16, 24, 32, 40, 64px (`--s-1` … `--s-8`). Tiles use 18/20px
  padding and 14px gaps; shelves are 40px tall blocks separated by hairlines; the map's
  header and closing section use 40–64px. Reader pages open 32px below the nav and close
  56px above the footer.
- **Gutters:** `--gutter` 24px, stepping to 18px at widths up to 400px. Blocks set
  vertical padding with `padding-block` only, so no shorthand can override the gutter —
  a regression that was found once and is guarded against by construction.
- **How dense it reads:** the map is dense on purpose — thirteen tiles, eight problem
  rows and nineteen ideas fit in a few screens — while reader pages are relaxed: one
  column, generous heading spacing, hairlines above each h2. The contrast between the two
  is the design: scan on the map, read in the page.

## Shape, depth and motion

- **Radii:** `--radius` 0.5rem for buttons-like things (frames, code blocks, the skip
  link, guide-sequence cards) and `--radius-lg` 0.7rem for tiles. Familiar values; nothing
  here needs to look sharp or pill-shaped.
- **Depth:** hairline borders only. No shadows, no gradients, no glow. Hover or keyboard
  focus on a tile lightens its border to `--border-strong`; that is the whole hover
  vocabulary. Frames sit in a 1px border on a black fill so a still-loading image shows
  a black 16:9 slot of the final size, not a jump.
- **Motion:** one transition — tile and guide-card border colour, 120ms ease-out
  (`--hover-ms`) — and smooth in-page scrolling for the contents strip and frame jumps.
  Under `prefers-reduced-motion: reduce` the transition length becomes 0ms and scrolling
  becomes instant. Nothing animates on load.

## Hierarchy of the map

1. The title, then the lead (one sentence, muted).
2. The contents strip — five real counts in orange mono, each a jump link. It is both
   the table of contents and the promise of what the map contains; the counts are
   generated from the same data as the shelves, and the build fails if they disagree.
3. The problem picker, beside the title at 980px and above; below it on narrower
   screens, after a two-line attribution. Both entry paths — *by problem* and *by
   source* — are on the first screen at desktop widths.
4. Four guide shelves grouped by source, each with a heading, a one-paragraph provenance
   note (with the pinned revision hash where there is one) and a link to the investigation
   that inspected the source. Then investigations, skills, the nineteen ideas, the twelve
   frames.
5. A closing pair: what was checked, and the full attribution.

## Components

- **Tile** (`.tile`): card surface, hairline, large dim mono numeral for guides (a
  guide number, never a metric), bold title that is the link, muted use-when line. The
  whole tile is the click and tap target (stretched link); keyboard focus outlines the
  whole tile. Investigation tiles show their source file name; skill tiles show their
  directory, which links to the same directory on GitHub, while the title opens the
  `SKILL.md` shipped with the site.
- **Problem picker** (`.pick`): hairline rows; bold question, muted answer with one or
  two links. No icons, no numbers — the question is the label.
- **Shelf head** (`.shelf-head`): heading left, provenance paragraph right at 900px and
  above. Paths and revision hashes are `code` and may wrap at any character.
- **Ideas list** (`.ideas`): hairline rows with a mono timestamp column (links to the
  video moment), the idea, and the implementing guide. Two columns at 900px and above.
- **Frame thumbnail** (`.grid-frames figure`) and **gallery frame** (`.frame`): 16:9
  image in a bordered black slot, mono timestamp, title; in the gallery the observation,
  a link to the moment in the video, the full-size frame, and the guide that applies it.
- **Reader** (`.reader`): a context line (guide number and source shelf, or the page's
  place on the map), the article, a previous/next guide pair as two cards, a source
  note with the editable Markdown and a way back to the map.
- **Tables and code** in reader pages: tables sit in a bordered, horizontally scrollable
  region that is keyboard-focusable and labelled; code blocks scroll horizontally inside
  their border. The page itself never scrolls sideways: overflow is contained in the
  region that produces it, never hidden on `html` or `body`, and that is checked on real
  renders at 320, 390, 768 and 1440px.
- **Navigation:** a top bar (brand → map, repository link) on every page; a wrapping
  row of section links on reader pages and the gallery with the current page marked; no
  navigation row on the map itself, whose contents strip and closing links do that job.
- **Not-found page:** same top bar, one heading, one sentence, four ways back in.
- **Nothing decorative above headings:** no eyebrow labels, overlines, small uppercase
  kickers or duplicate labels, and no uppercase transforms. Field labels, the nav and
  honest status text are fine.
- **Numbers beside words:** a count, guide number or timestamp that sits before a label
  (`13 guides`, `01 Convert…`, `04:07 A small test…`) is followed by a real space in the
  markup, so screen readers hear two words; the margin on the number only tops the
  space up to the intended visual gap.

## Familiar versus deliberate

Familiar, and right here: the dark palette, system faces, 16px body, hairline borders,
underlined links, a skip link, a wrapping text nav. None of these needs to be original;
originality would cost reading comfort.

Deliberate, and specific to this handbook: guides grouped by *source* rather than by
topic or number, because provenance is the handbook's discipline; large numerals as the
tile's visual anchor, because the guides really are numbered and readers refer to them
by number; real counts as the table of contents; the map's title much larger than any
page title; and the reader's "Guide 03 of 13 · From Theo's video" context line, which
keeps the map's grouping visible while reading.

## Not done, on purpose

- No light theme. Adding one would manufacture difference rather than a better
  hierarchy; the print stylesheet does flip to a light palette.
- No search or filter. The map is small enough to scan, and a filter would be the only
  script on the site.
- No icons. The numerals, timestamps and words do the work.
