# Design system

Source-only guidance for contributors: how the Agent Engineering Handbook looks and why.
It is never rendered or copied into `public/`. Every generated page — the map
(`index.html`), the reader template behind the guides, investigations and other Markdown
pages, the frame gallery (`evidence.html`) and the not-found page — loads one stylesheet,
`build/assets/handbook.css`, whose first block holds the tokens listed here. Page
structure lives in `build/render.py`. Behaviour (journeys, states, keyboard, responsive
decisions) is in [INTERACTIONS.md](INTERACTIONS.md).

## The one thing to remember

**A numbered, sourced field manual.** The handbook is thirteen numbered methods, each
traceable to a video moment or a pinned repository revision. The map lays the whole
manual out grouped by source; the reader keeps the number, the source and the page's
sections in view while you read. Everything below serves that: serif titles that read as
a manual rather than a dashboard, mono numerals and timestamps as the wayfinding
vocabulary, warm surfaces with hairlines instead of floating cards, and a reader with a
rail instead of a bare column of text.

## Typography

Three faces, each with one job, all from the reader's own system — no web font, so the
site has no network dependency and reads at native quality on developer machines.

- **Serif for titles and section headings** (`--font-serif`: Iowan Old Style, Charter,
  Georgia, Palatino Linotype…): the map's title, shelf headings, the reader's h1 and h2,
  investigation and skill titles, the brand. Weight 600, tracking −0.012em. This is the
  handbook's voice; it is the one deliberate departure from the generic
  system-sans-everywhere look the earlier edition had.
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

A warm near-black ground, two lifted surfaces and one orange accent — the warm character
of the earlier pages, shifted off pure neutral so the orange belongs to the ground rather
than sitting on it.

| Token | Value | Role | Contrast on `--bg` / `--surface` / `--surface-2` |
|---|---|---|---|
| `--bg` | `#100f0d` | page ground | — |
| `--surface` | `#17150f` | panels, chapter lists, cards, code blocks, blockquotes, menu | — |
| `--surface-2` | `#1f1c17` | chips, inline code, table header, hover fill | — |
| `--border` | `#2c2822` | hairlines | decorative |
| `--border-strong` | `#6f675c` | hovered card or chip edge | 3.4 / 3.3 / 3.0 (non-text ≥ 3 ✓) |
| `--fg` | `#f2ece2` | headings, body, titles | 16.3 / 15.5 / 14.5 |
| `--muted-fg` | `#aca69b` | leads, use-when lines, captions, nav, rail text | 7.9 / 7.5 / 7.0 |
| `--dim-fg` | `#8d867b` | edition line, directory lines, rail labels | 5.3 / 5.1 / 4.7 |
| `--link` | `#f29764` | running links in prose | 8.6 / 8.2 / 7.6 |
| `--accent-text` | `#f37a3b` | numerals, timestamps, counts, chip numbers, "Guide 02" | 7.0 / 6.7 / 6.2 |
| `--primary` | `#ea580c` | focus ring, brand mark, current-section marker, blockquote rule, skip link fill | 5.4 / 5.1 / 4.8 |
| `--on-primary` | `#100f0d` | text on the orange skip link | 5.4 on `--primary` |

Ratios are WCAG 2.x, computed from the hex values; every text colour passes AA for
normal text on every surface it is used on. `--accent-text` exists because the raw
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

- **Radii:** `--radius-sm` 6px (thumbnails, buttons, small blocks), `--radius` 10px
  (code, tables, blockquotes, previous/next, the menu panel, the section disclosure),
  `--radius-lg` 14px (the problem panel, chapter lists, cards); chips and count pills are
  fully round.
- **Depth:** hairlines and surface steps. The only shadow is under the open header menu,
  because it floats over content. Frames sit on black inside a hairline so a lazy image
  shows a correctly sized 16:9 slot before it lands.
- **Motion:** border and background colour on hover, `--hover-ms` 140ms ease-out; smooth
  in-page scrolling. Under `prefers-reduced-motion: reduce` both become instant. Nothing
  animates on load; the current-section marker in the rail changes without transition.

## Hierarchy of the map

1. **Header** — brand with the orange mark, four section links (Guides, Investigations,
   Skills, Frames), a "More" menu listing every page, and "GitHub". Never the full
   repository address.
2. **Opening, two columns from 980px** — left: the title, one-sentence lead, the counts
   strip as five pills (each a jump link; the counts are generated from the same data as
   the shelves and the build fails if they disagree), the edition line with the
   attribution sentence. Right: the problem panel, a surface with eight rows — bold
   situation on the left, numbered chips on the right naming the guide(s) that answer it.
   Both entry paths, *by problem* and *by source*, are on the first screen at desktop.
3. **Four guide shelves grouped by source.** From 900px each shelf is a sticky heading
   column (serif heading, provenance paragraph with the pinned revision, investigation
   link, "Guides 01–08" in mono) beside a **chapter list**: one bordered surface, two
   columns from 720px, hairlines between rows, a large accent numeral, the title and the
   use-when line. Rows, not cards: the guides are numbered chapters and read as a
   contents page.
4. **Investigations and skills** as cards (serif title, purpose line, mono file or
   directory), full width with the heading row above so four skills fit in one row.
5. **Nineteen ideas** as a timeline: accent timestamp, the idea, a chip naming the
   implementing guide; two columns from 900px.
6. **Twelve frames** as a filmstrip, four across from 1000px, three from 640, two below.
7. **Closing:** what was checked, and attribution with chip links to the index pages.

## The reader

- **Page head:** a context line (`Guide 02` · of 13 · shelf link, or the page's place on
  the map) and the serif title. Guide titles come from the README's canonical list so the
  reader and the map agree; the Markdown file's own h1 is not rendered a second time.
- **Article:** first paragraph as a muted, slightly larger deck; serif h2 with a hairline;
  sans h3; code, tables and blockquotes on `--surface` inside `--radius`; tables in a
  focusable scroll region.
- **Rail (from 1100px), sticky:** *On this page* (h2/h3 anchors, current one marked with
  an orange edge), *This guide* (number, shelf, use-when), *Sequence* (previous/next),
  *Evidence from the video* (up to two frames applied in this guide, linking into the
  gallery) and *Source* (the Markdown beside the page, and on GitHub).
- **Below 1100px:** the rail is gone; a native "On this page" disclosure sits under the
  title, and the applied frames follow the article. Previous/next cards and the source
  line close every guide at every width.

## Components

- **Chip** (`.chip`): pill, `--surface-2`, hairline, mono accent number then label. Used
  for problem answers, idea → guide links and the closing links. Whole pill is the target.
- **Chapter row** (`.tiles.guides .tile`): numeral column + title/use-when; stretched
  link; hover fills the row; focus ring drawn inside the row.
- **Card** (`.tiles.cards .tile`): serif title, purpose line, mono path pinned to the
  bottom; stretched link with the ring around the card; the directory link keeps its own.
- **Header menu** (`details.menu`): a native disclosure, the panel absolutely positioned
  under its button; the four primary links are hidden inside it from 760px.
- **Section disclosure** (`details.toc-mobile`) and **rail** (`aside.rail`): the same
  section list markup in two places, shown at complementary widths.
- **Frame thumbnail**, **gallery frame**, **table region**, **not-found page**: as
  before, restyled with the tokens above.
- **No decoration above headings:** no eyebrow labels, overlines, uppercase kickers or
  duplicate labels. Rail labels ("On this page", "Sequence") are sidebar section labels,
  set small and sans, not kickers over a main heading. Numbers before words are followed
  by a real space in the markup so screen readers hear two words.

## Familiar versus deliberate

Familiar, and right here: dark ground, 16/17px body, hairlines, underlined links, a skip
link, a sticky rail with a section list, previous/next at the end of a chapter.

Deliberate: the serif voice on a technical site; numerals, timestamps and counts as the
only "icons"; chapter lists instead of card grids for the guides; the problem panel as
the map's co-headline rather than a text list under the title; evidence frames placed
beside the guide they support; a warm rather than neutral ground.

## Not done, on purpose

- No light theme (the print stylesheet flips to a light palette).
- No search or filter; the map is small enough to scan and the header menu reaches every
  page.
- No icons or illustration; the frames are the only imagery and they are evidence.
- No web font, framework or build dependency beyond the pinned Markdown package. The one
  script is optional and every control works without it.
