# How the site behaves

The behaviour specification for the generated pages: the reader's journey, what each
screen puts first, the states that actually occur on a static site, and the responsive,
keyboard, focus and touch decisions. The visual system is in [DESIGN.md](DESIGN.md).

This is a static site with no scripts, no search, no accounts and no asynchronous data,
so there are no loading skeletons, no error toasts and no empty result states to
design. The states that do occur are: a page that does not exist, an image that has not
loaded or cannot load, and content that is longer or wider than its container.

## The journey

**1. Arrive at the map** (`index.html`), from the video, GitHub, a search result or a
link. First thing seen: the title and lead. Second: the contents strip — five counts
that say what is here and jump to it. Third, beside the title at 980px and above or
just below it on a phone: the problem picker. The primary element is the title; the
primary *action* is the picker or a shelf, and both are within the first two screens at
every width.

**2. Choose by problem or by source.** The picker's eight rows name a situation and link
to the guide (sometimes two) that addresses it. The shelves list every guide under the
source it was adapted from, with a use-when line so the reader can pick without opening
each one. A tile is one click or tap anywhere on its surface.

**3. Read a guide.** The context line at the top says "Guide 03 of 13" and names the
shelf, linking back to it. The article is the guide's own Markdown, one column. Companion
guides and the runnable example are linked from the guide's opening paragraph as the
author wrote them; every internal link opens the generated page beside it.

**4. Reach the source, a frame or a skill.** Video timestamps in a guide open the video at
that moment in the same tab (the reader chose to leave). Pinned repository links open the
snapshot on GitHub. From the gallery, each frame offers the moment in the video, the
full-size image and the guide that applies what the frame shows. Skill tiles open the
`SKILL.md` shipped with the site; the directory line opens the same directory on GitHub.

**5. Return.** At the end of a guide, two cards: the previous and next guide (the first
guide's "previous" is the guide shelf; the last guide's "next" is the investigations).
Under them, the source note with "Back to the map". On every page the brand in the top
bar returns to the map and the nav row reaches the handbook's other entry points.

## Hierarchy by screen

| Screen | First | Second | Third | Primary action |
|---|---|---|---|---|
| Map | title | contents strip | problem picker | pick a problem row or a tile |
| Guide | context line + title | opening paragraph (muted, larger) | headings in order | read; next guide |
| Investigation / other page | context line + title | opening paragraph | headings | read; nav row |
| Gallery | title + lead | timestamp strip | frames in a two-column grid | open a frame's moment, full-size image or guide |
| Not found | heading | one sentence | four links | the map |

## State table

| Screen | State | What is shown | What the reader can do |
|---|---|---|---|
| Any page | Missing page (404) | `404.html`: "That page is not in the handbook", one sentence, links to the map, the problem picker, the handbook index (`README.html`, which lists the guides rather than containing them) and the gallery. Root-absolute links, because it is served at any path. | Go back in from any of the four links. |
| Map, gallery | Image not loaded yet | A black 16:9 slot of the final size (width/height attributes plus `aspect-ratio`), bordered; the caption is already visible. Images are lazy-loaded. | Scroll on; nothing shifts when the image lands. |
| Map, gallery | Image cannot load | Alt text "Video frame at 06:23: A narrow upload skill." inside the black slot; the caption, timestamp, observation and links are unaffected. | Use the caption's links; the full-size link fetches the original. |
| Guide, report | Wide table | Bordered horizontally scrollable region, labelled "Scrollable table", keyboard-focusable. The page does not scroll sideways. | Scroll the region with a trackpad, touch, or arrow keys after focusing it. |
| Guide, report | Wide code block | Scrolls inside its own border. | Scroll the block. |
| Any | Long unbreakable text (a 40-character hash, a long path) | Wraps at any character inside `code`; grid and flex items have a zero minimum width so nothing widens the page. | Read it; select it. |
| Map | A shelf with one guide | Renders as a single tile in the grid; the shelf's heading and provenance stay. Honest about the count. | — |
| Gallery | Arrival at `#frame-<seconds>` | The frame scrolls into view with 16px above it. | Read the observation; jump to another timestamp from the strip. |
| Skill file | Opened `SKILL.md` | The browser shows or downloads the Markdown as served; there is no generated page for it. | Browser back, or the GitHub link on the tile for a rendered view. |
| Print | Any page | Light palette, nav and guide cards hidden, external link addresses printed after the link text, tables unconstrained, code wrapped. | — |

Local preview note: `python3 -m http.server` does not serve `404.html` for missing paths;
the hosting platform does. The page's links are root-absolute, so it works only when the
site is served from a domain root.

## Responsive decisions

Widths designed for: 320, 390, 768 and 1440px. Gutters are 24px, and 18px at 400px and
below, so a 320px phone keeps 284px of content.

- **Map, 320–979px:** one column. Title, lead, contents strip (wrapping), two-line
  attribution, then the picker. Tiles: `auto-fill` at a 230px minimum, so one column at
  320 and 390, two at 768. Ideas: one column. Frame thumbnails: two across, three from
  640px. Shelf heading and its provenance paragraph stack.
- **Map, 980px and above:** title block and picker side by side (1.1fr / 0.9fr). Shelf
  heading and provenance side by side from 900px. Ideas in two columns from 900px. Frame
  thumbnails six across from 1000px. Tiles: four or five per row at 1440.
- **Reader, all widths:** one column of at most 48rem, centred. The nav row wraps onto
  two or three lines at 320px; nothing is hidden behind a menu button because the row is
  nine short words and needs no script. The previous/next cards stack below 640px.
- **Gallery:** one column below 760px, two above. Each frame keeps its heading, image,
  observation and links together.
- **Long titles:** guide 11's title is 68 characters. It wraps inside a tile, inside the
  guide-sequence card and in the reader heading; nothing truncates. Titles are never
  ellipsised anywhere on the site.

## Keyboard, focus and screen readers

- **Skip link** first in the tab order on every page; it appears at the top left when
  focused and jumps to `<main id="main">`.
- **Tab order** follows the visual order: top bar (brand, repository), nav row, context
  link, article links, guide-sequence cards, source note, footer. On the map: brand,
  repository, contents strip, attribution link, picker rows, tiles shelf by shelf,
  ideas, frames, closing links.
- **Focus ring:** 2px orange outline, offset 3px, on every focusable element via
  `:focus-visible`. On a tile the ring surrounds the whole tile, matching the click
  target; the skill tile's directory link keeps its own ring.
- **Current page** in the nav row carries `aria-current="page"` and an orange underline.
- **Lists** that drop bullets (`list-style: none`) carry `role="list"` so VoiceOver still
  announces them as lists with counts. Each shelf is a labelled region
  (`aria-labelledby` its heading). Tile numerals are `aria-hidden`; the link text is
  prefixed with a visually hidden "Guide 03:" so a screen reader hears the number with
  the title.
- **Tables** are wrapped in a region with `tabindex="0"` and the label "Scrollable
  table" so keyboard users can reach and scroll them.
- **Images** all have alt text. Frame alt text is "Video frame at 02:44: Sponsor CI
  dashboard." — the identifying facts, not a paraphrase of the caption, which follows
  as visible text.
- **Headings** are in order on every page: one h1, then h2 sections; the build check
  fails a page with zero or several h1s.
- **Reduced motion:** honoured for the one transition and for smooth scrolling.
- **Language and colour scheme:** `lang="en"` and `color-scheme: dark` are declared so
  form controls and scrollbars match the page.

## Touch

- Tiles and guide-sequence cards are large targets (whole surface).
- Contents-strip, timestamp-strip and nav links have 4–6px vertical padding, giving
  roughly 32px-tall targets; picker answers and idea links are inline text links inside
  their rows, as in any reading page.
- No hover-only information: hover only lightens a border or underlines a link.

## Resolved decisions

- **Skill links go to the shipped `SKILL.md`, not a generated page.** The skill is the
  file; a generated page would be a second copy that could drift. The GitHub directory
  link on the same tile gives a rendered view. Known cost: the browser may show or
  download the Markdown as plain text.
- **The nineteen ideas are on the map, not only linked.** The map's promise is the whole
  handbook on one page; leaving the ideas as a count that jumps to another page broke
  that promise. They sit after the skills and before the frames, both video-derived.
- **Guides are grouped by source, not by number.** The numbering is preserved on every
  tile and in the guide sequence; the grouping is the map's argument about provenance.
- **Previous/next follow guide numbers, not shelves.** A reader working through the
  guides expects 08 to lead to 09 even though the source changes; the context line shows
  the change of source.
- **External links open in the same tab.** No `target="_blank"`; readers who want a new
  tab have the modifier key, and the choice stays theirs.
- **The map has no nav row, at any width.** Its contents strip and closing links already
  reach every section and page; a nav row above the title would duplicate them. This
  was re-judged on phone renders: at 390px the contents strip sits inside the first
  screen, at 320px it starts at the bottom edge of the first screen, and the top bar
  already takes three lines there (brand plus the wrapped repository address). A nav
  row would push the title and the strip further down to reach pages the closing links
  and the brand already reach; the strip is the map's section navigation.
- **No JavaScript.** Every behaviour above is HTML and CSS. Nothing here needs a script,
  and a script would be the site's only runtime dependency.
- **Frame-to-guide links** are an editorial mapping kept in the landing-page data file,
  not inferred at build time, so they can be corrected as easily as any caption.

- **Numbers and labels are separate words.** Every count, guide number and timestamp
  that precedes a label is followed by a real space in the markup, so a screen reader
  says "13 guides" and "04:07 A small test…" rather than one run-together token. The
  visual gap is kept by a smaller margin on the number.

Open: nothing that blocks reading.
