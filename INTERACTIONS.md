# How the site behaves

Source-only guidance for contributors, never rendered or copied into `public/`. The
behaviour specification for the generated pages: the reader's journey, what each screen
puts first, the states that occur on a static site, and the responsive, keyboard, focus
and touch decisions. The visual system is in [DESIGN.md](DESIGN.md).

The site is static HTML and CSS with one optional script (`build/assets/handbook.js`).
There are no accounts, no search and no asynchronous data, so there are no loading
skeletons or error toasts. The states that do occur: a page that does not exist, an
image not yet loaded or unable to load, content wider than its container, and a
disclosure (menu or section list) that is open or closed.

## The journey

**1. Arrive at the map** (`index.html`). First seen: the title and lead on the left, the
problem panel on the right (from 980px) or directly below (phones). Second: the counts
strip — five pills that say what is here and jump to it. The primary element is the
title; the primary *action* is a problem row's chip or a chapter row.

**2. Choose by problem or by source.** The problem panel's eight rows name a situation
and offer numbered chips for the guide(s) that address it. The four shelves list every
guide under the source it was adapted from as a chapter list with a use-when line, so a
reader can pick without opening each one. A chapter row is one click or tap anywhere on
its surface.

**3. Read a guide.** The page head says "Guide 02 · of 13 · From Theo's video" (the shelf
link returns to that group). From 1100px the rail beside the article lists the sections
and marks the one on screen, names the guide's place and use-when, links the previous and
next guide, shows up to two frames applied in the guide, and links the Markdown source.
Below 1100px an "On this page" disclosure under the title opens the section list; the
applied frames follow the article.

**4. Reach the source, a frame or a skill.** Video timestamps open the video at that
moment in the same tab. Pinned repository links open the snapshot on GitHub. Evidence
frames open the gallery at that frame, which offers the moment in the video, the
full-size image and the guide that applies it. Skill titles open the skill's page
(`skills/<name>/`): the page's sections list, its "N ideas feed it" tags and the guides
that cite it let the reader decide, and its Adopt block links the shipped `SKILL.md`, the
directory on GitHub and the adoption page. The section links reach `skills.html` and
`investigations.html`, which hold every skill tile and every report card.

**5. Return or continue.** Previous/next cards close every guide (the first guide's
"previous" is the guide shelves; the last guide's "next" is the investigations). The
source line under them links the Markdown and the map. The brand in the header returns to
the map from any page; the four section links and the "More" menu reach every page.

## Hierarchy by screen

| Screen | First | Second | Third | Primary action |
|---|---|---|---|---|
| Map | title + problem panel | counts strip | guide shelves | a chip in the problem panel or a chapter row |
| Guide | context line + drawing + title | deck paragraph | rail (sections, place) or the section disclosure | read; next guide |
| Skill page | context line (`SKILL` · All four skills) + drawing + title | the description deck, then the skill's sections and references | rail (sections, This skill, In the guides, Adopt) or the section disclosure | read; adopt via the raw `SKILL.md`, GitHub or the adoption page |
| Skills / Investigations index | marker + title + lead | the four skill tiles / the three report cards | the closing route out of the section | open a skill page or a report |
| Investigation / other page | context line + title | deck paragraph | sections | read; header menu |
| Gallery | title + lead | timestamp strip | frames in two columns, then the closing route | open a frame's moment, image or guide |
| Not found | heading | one sentence | four links | the map |

## State table

| Screen | State | What is shown | What the reader can do |
|---|---|---|---|
| Any page | Missing page (404) | `404.html`: "That page is not in the handbook", one sentence, links to the map, the problem panel, the handbook index and the gallery. Root-absolute links, because it is served at any path. | Go back in from any link or the header. |
| Any page | Header menu closed / open | Closed: a "More" (from 760px) or "Menu" (below) button. Open: a panel under the button listing every page in four groups; the current page is tinted. Without the script it stays open until the button is used again; with it, Escape or a click outside closes it. | Pick a page; close with the button, Escape or an outside tap. |
| Guide, wide | Section on screen | The rail marks the section whose heading has passed the top of the viewport with an orange edge and brighter text. Without the script no section is marked; the list still works. | Jump to any section. |
| Guide, narrow | Section disclosure closed / open | Closed by default: "On this page" with a chevron. Open: the section list inside the same surface. | Open it, jump, or read on. |
| Map, gallery, rail | Image not loaded yet | A black 16:9 slot of the final size (width/height attributes plus `aspect-ratio`), bordered; the caption is already visible. Images are lazy-loaded. | Scroll on; nothing shifts when the image lands. |
| Map, gallery, rail | Image cannot load | Alt text "Video frame at 06:23: A narrow upload skill." inside the black slot; caption, timestamp and links are unaffected. | Use the caption's links; the full-size link fetches the original. |
| Guide, report | Wide table | Bordered, horizontally scrollable region labelled "Scrollable table", keyboard-focusable. The page never scrolls sideways. | Scroll the region by trackpad, touch, or arrow keys after focusing it. |
| Guide, report | Wide code block | Scrolls inside its own border. | Scroll the block. |
| Any | Long unbreakable text (a 40-character hash, a long path) | Wraps at any character inside `code`; grid and flex items have a zero minimum width so nothing widens the page. | Read it; select it. |
| Map | A shelf with one guide | One chapter row in the surface; the heading column says "Guide 13". | — |
| Guide with no applied frame | Evidence block | The rail and the narrow-screen evidence block are simply absent; nothing says "no evidence". | — |
| Gallery | Arrival at `#frame-<seconds>` | The frame scrolls into view with 20px above it. | Read the observation; jump to another timestamp. |
| Skill file | Opened `SKILL.md` | The browser shows or downloads the Markdown as served; the skill page's Adopt block links it as shipped. | Browser back, or the skill page's directory or adoption link. |
| Print | Any page | Light palette; header, rail, disclosure, previous/next and footer links hidden; external addresses printed after link text; tables unconstrained; code wrapped. | — |

Local preview note: `python3 -m http.server` does not serve `404.html` for missing paths;
the hosting platform does.

## Responsive decisions

Widths designed for: 320, 390, 768 and 1440px. Gutters are 24px, and 16px at 400px and
below, so a 320px phone keeps 288px of content.

- **Header, below 480px:** brand (1rem, may wrap to two lines at 320px) and the "Menu"
  button; the GitHub link moves into the menu's last group. 480–759px: brand, "Menu",
  "GitHub". From 760px: brand, four section links, "More", "GitHub". The menu panel is
  right-aligned under its button and never wider than the viewport.
- **Map, below 980px:** one column — title, lead, counts strip (wrapping pills), edition
  line, then the problem panel. Problem rows stack question over chips below 640px and
  sit side by side above. Chapter lists are one column below 720px, two above. Cards use
  `auto-fill` at a 250px minimum (one column at 320/390, two or three at 768, four at
  1440). Ideas: one column below 900px. Frames: two across, three from 640, four from
  1000.
- **Guides index, 900px and above:** each shelf head puts its title, its provenance and
  its count side by side in one row; below that they stack. The map itself carries
  routing rows rather than shelf heads, so nothing there is sticky.
- **Reader, below 1100px:** one centred column of at most 39rem; the section disclosure
  under the title; applied frames after the article in a grid of 220px-minimum
  thumbnails. Previous/next stack below 640px. The body is 16px below 760px and 17px
  above.
- **Reader, 1100px and above:** a 248px rail on the left and the reading column on the
  right, the two pinned to the page's left and right edges so the rail lines up with the
  header's title and the column with the GitHub link. The rail holds beside the article
  and takes its own scroll when it is taller than the screen, the ordinary
  table-of-contents pattern; `overscroll-behavior: contain` stops that scroll chaining
  into the page at either end, so the two sides move independently. Its scrollbar is thin
  and appears only when the rail actually overruns: on a tall desktop the investigation,
  README and adoption rails fit and show none. Below 1100px the rail is gone and the
  column is centred, unchanged.
- **Long titles:** guide 11's title is 68 characters. It wraps in the chapter row, in the
  previous/next card, in the rail and in the page title; nothing truncates.

## Keyboard, focus and screen readers

- **Skip link** first in the tab order on every page; it appears at the top left when
  focused and jumps to `<main id="main">`.
- **Tab order** follows the visual order: brand, section links, the menu button (Enter or
  Space opens it; its links follow in order; Escape closes it and returns focus to the
  button when the script is present), "GitHub", then the page. On the map: counts strip,
  attribution link, problem chips row by row, chapter rows shelf by shelf, cards, ideas,
  frames, closing links. On a guide: context link, section disclosure (narrow) or, at
  wide widths, the article first and the rail after the source line.
- **Focus ring:** 2px orange outline, offset 3px, via `:focus-visible`. Chapter rows draw
  the ring inside the row; cards around the card, matching the stretched-link target.
- **Current page** in the header carries `aria-current="page"` (an orange underline on a
  section link, tinted text in the menu). The current section in the rail carries
  `aria-current="true"`.
- **Native disclosures** (`<details>`) are used for the header menu and the section
  disclosure: they are focusable, toggle with Enter and Space, and announce their
  expanded state without any script.
- **Lists** that drop bullets carry `role="list"`. Each shelf is a labelled region.
  Chapter numerals are `aria-hidden`; the link text is prefixed with a visually hidden
  "Guide 03:". The rail is an `aside` labelled "Page tools"; the section lists are `nav`
  elements labelled "Sections of this page".
- **Tables** are wrapped in a focusable region labelled "Scrollable table".
- **Images** all have alt text of the form "Video frame at 02:44: Sponsor CI dashboard."
- **Headings** are in order on every page: one h1, then h2 sections (the build check
  fails a page with zero or several h1s). Rail and evidence-block labels are h2s that
  follow the article's sections.
- **Reduced motion** is honoured for hover transitions and smooth scrolling.
- **Language and colour scheme:** `lang="en"` and `color-scheme: dark` are declared.

## Touch

- Chapter rows, cards, previous/next cards and chips are large targets (whole surface;
  chips are at least 28px tall with 6px between them).
- Header links, the menu button and the section disclosure summary are 36–44px tall.
- No hover-only information: hover only lightens a border, fills a row or underlines.

## Resolved decisions

- **Guide titles on reader pages come from the README's canonical list**, and the file's
  own h1 is not rendered again, so the map, the rail and the page agree on the number
  and title. Non-guide pages use their own h1.
- **The header shows a short "GitHub" label, never the repository address.** The address
  was eating the phone header; the label reaches the same place.
- **The header menu is a native `<details>`**, not a script-built dropdown, so it works
  with keyboard and touch before any script runs. The script only adds Escape and
  outside-click closing.
- **The section list is rendered twice** (in the narrow-screen disclosure and in the
  rail) rather than moved by script, so both work without JavaScript and neither hides
  content on the width where it is needed.
- **The rail shows at most two applied frames** so it fits beside the article; the
  narrow-screen block after the article shows all of them; the gallery has everything.
- **Guides are grouped by source, not by number; previous/next follow guide numbers.**
  Unchanged from the earlier edition: the grouping is the map's argument about
  provenance, and a reader working through the guides expects 08 to lead to 09.
- **Skills have their own pages; the raw `SKILL.md` stays shipped and linked.** Skill
  titles used to open the raw file directly; they now open `skills/<name>/`, whose Adopt
  block links the shipped `SKILL.md`, the GitHub directory and the adoption page, so the
  installer's route is kept rather than dropped.
- **External links open in the same tab.** Unchanged.
- **The nineteen ideas are on the map, not only linked.** Unchanged.
- **One optional script.** Every behaviour is HTML and CSS first; the script is a
  convenience for the menu and the rail marker and can be removed without breaking any
  control.
- **Numbers and labels are separate words** in the markup so screen readers say
  "13 guides" and "04:07 A small test…".

Open: nothing that blocks reading. Render inspection at 320, 390, 768 and 1440 is the
remaining check for any change to this file's decisions.
