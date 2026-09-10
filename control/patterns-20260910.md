# Composition patterns from the six references — astra, 2026-09-10

Two scans of the same capture set, run in parallel from tiles ≤1600px (group A: Qodo Academy, Augment Code, Sourcegraph; group B: UX Pilot, Codecademy, the Paper capture of Sourcegraph). The owner's instruction: "break out of the systematized grids and cards (boring)… Scan those examples and find mechanical patterns that we can use as examples that will break the AI out of the slop." Each pattern names where it was seen, the mechanism, the default it breaks, a checkable property and how it transfers to the handbook. Nothing here has been applied yet.

## Group A — Qodo, Augment, Sourcegraph


These are visible structures, not a prescription to copy each site. The useful departure is from **interchangeable content boxes**, not from alignment itself.

**Evidence boundary.** Read all 11 supplied JPGs once, without cropping, tiling, re-rendering or network access, alongside `INSPO-README.md`, `VOCABULARY.md` and `GPT-TASTE.md`. The directory contains five Augment tiles, not the six named in the request: `02-augmentcode-full-part01.jpg` through `part05.jpg`; part05 is blank. Qodo part02 is only a short continuation of frame edges. Neither supplies an additional pattern. The broad white interruptions in the Augment PDF capture are capture pagination, not claimed website composition. Sourcegraph's two crops repeat areas of its main tiles; they clarify those areas rather than establish additional page sections. No animation, responsive behavior or source DOM was observed.

**How to read the checks.** Locations are approximate pixel positions within the supplied 1000px-wide tiles. Checks below are proposed DOM/CSS acceptance measurements for a handbook implementation at a comparable desktop width—not measured properties of the source DOM or inferred original CSS. `W` means the relevant section's inner width; bounding boxes exclude decorative shadows. Numeric thresholds make the mechanism testable; they are implementation recommendations, not extracted source values. A passing geometry check would not establish content quality or mobile usability.

**Transfer boundary.** The handbook inventory is nineteen ideas, thirteen guides, four skills, three investigations and twelve video frames. Applications preserve direct skill/guide paths, use existing authored drawings rather than the references' product UI, and keep video stills off the homepage as recorded in the inspiration note. Grouping or relationship proposals below require actual content relationships, not invented dependencies. Existing vocabulary motifs recur only where the check adds a structural constraint absent from that file.

1. **Offset entry axis**
   - **Where:** Qodo Academy, `01-qodo-academy-part01.jpg`, hero, approximately y=160–425.
   - **Mechanism:** The illustration occupies the left margin while the heading, introduction, actions and eligibility row share a second starting edge farther right. The hero's reading axis is therefore neither the page's center nor its normal left content edge.
   - **Default it breaks:** Automatically centering every hero, or making the visual and copy two equal-width boxed halves.
   - **Checkable property:** The hero copy's left edge sits 0.25–0.40W to the right of the hero container's left edge; heading, description and action-group left edges differ by no more than 4px; the illustration's right edge precedes the copy's left edge.
   - **Handbook application:** Put one existing drawing beside an offset introduction with direct skills and guides links, rather than opening with five equal inventory cards.

2. **Contracted reading lane**
   - **Where:** Qodo Academy, `01-qodo-academy-part01.jpg`, contributor area at y=510–845 versus chapter directory at y=1125–1600.
   - **Mechanism:** The contributor row spreads broadly across the page, but the directory below contracts to a narrower centered lane and resumes left-aligned reading inside it. Adjacent content types do not inherit a single universal container width.
   - **Default it breaks:** One max-width wrapper and the same three-column footprint for every section.
   - **Checkable property:** Directory width divided by the preceding broad section width is 0.78–0.88; their horizontal centers differ by at most 4px; chapter headings align to the directory's left edge rather than the page edge.
   - **Handbook application:** Give the nineteen ideas a broad overview but place the thirteen guide entries in a narrower reading lane, without requiring both collections to share a grid.

3. **Parent before destination**
   - **Where:** Qodo Academy, `01-qodo-academy-part01.jpg`, first chapter, approximately y=1195–1590.
   - **Mechanism:** A full-width chapter introduction contains its own title, explanation and author metadata, followed by a separator and a shallower destination row. Parent context and the next reading action have different spatial roles instead of becoming two sibling cards.
   - **Default it breaks:** Flattening a chapter and its constituent reading links into equivalent tiles; placing an identical floating button on every item.
   - **Checkable property:** The destination row is a DOM descendant of the chapter group, occupies at least 90% of its inner width, and has a height below 30% of the group's visible height; the separator falls between metadata and destination.
   - **Handbook application:** Where real relationships exist, place guide links beneath the relevant idea's explanation, retaining a separate complete index of all thirteen guides.

4. **Split section premise**
   - **Where:** Augment Code, `02-augmentcode-full-part01.jpg`, “Build your software factory…” at y≈720–780; repeated in part02 at y≈1170–1230.
   - **Mechanism:** The section title starts on the left while its short explanatory premise starts across a generous central interval on the same horizontal band. The full-width content starts below both, so this is an introduction to one composition, not another text/image feature split.
   - **Default it breaks:** Centered heading, centered subtitle, equal cards underneath—repeated at every section.
   - **Checkable property:** Heading and premise top edges differ by at most 12px; premise begins at or beyond 0.58W; neither occupies over 0.48W; the next content region spans at least 0.95W below both boxes.
   - **Handbook application:** Introduce the four skills with their collective purpose on the left and instructions for choosing on the right, above the actual skill content.

5. **Drawing before summary**
   - **Where:** Augment Code, `02-augmentcode-full-part01.jpg`, “Code review” and “Ticket to PR” units, y≈825–1120.
   - **Mechanism:** Each unit gives a wide explanatory drawing its own upper region, then places title, copy, outcome and link below it. Although the units are aligned, the composition is driven by a diagram's footprint rather than a small icon attached to a generic card heading.
   - **Default it breaks:** Shrinking every authored visual into a corner icon while repeating title/body/button boxes.
   - **Checkable property:** Each drawing box precedes its heading vertically, spans at least 70% of the unit's inner width, and consumes at least 35% of the unit height; the drawing and heading boxes do not intersect.
   - **Handbook application:** Give each of the four skill drawings an explanatory region large enough to read, followed by its real idea/guide counts rather than invented performance statistics.

6. **Shared closing statement**
   - **Where:** Augment Code, `02-augmentcode-full-part01.jpg`, below the four loop units, y≈1505–1590.
   - **Mechanism:** After individual loop entries and their separate links, a rule closes the collection and a single centered statement explains the whole. The section earns a collective conclusion instead of ending at the bottom edge of its final row.
   - **Default it breaks:** A feature grid that simply stops, or four copies of the same concluding message inside four cards.
   - **Checkable property:** Exactly one conclusion element follows the collection outside the repeated-item nodes; its center is within 4px of the collection center, its width is 40–65% of the collection width, and its top edge is below the collection's closing rule.
   - **Handbook application:** Close the four-skill overview with one statement explaining how the skills work together before sending readers into the nineteen ideas.

7. **One stage, many cues**
   - **Where:** Augment Code, `02-augmentcode-full-part02.jpg`, “Cosmos in action,” y≈235–920.
   - **Mechanism:** One large demonstration sits over three shallow explanatory segments with progress-like rules, with a small pause control outside the segment row. The observed layout separates the shared viewing area from its compact sequence cues; the screenshot does not prove that the cues change the view.
   - **Default it breaks:** Twelve thumbnails each boxed with duplicated player chrome, titles and buttons.
   - **Checkable property:** One viewer is rendered above a cue list; the list spans at least the viewer's width, each cue's height is below 25% of the viewer height, and there is no second viewer embedded in any cue node.
   - **Handbook application:** On a dedicated video page—not the homepage—present the twelve frames through one viewing area with twelve compact frame/time destinations below it.

8. **Staggered track annotations**
   - **Where:** Augment Code, `02-augmentcode-full-part02.jpg`, factory track at y≈1315–1590.
   - **Mechanism:** A continuous horizontal track carries stages while explanatory panels sit above and below it, attached at different positions. The track supplies the shared sequence; the panels are annotations to that sequence, not a row of independent service cards.
   - **Default it breaks:** A four-column “step 1–4” grid whose only indication of sequence is its numbering.
   - **Checkable property:** One track spans at least 90% of W; at least one annotation box lies wholly above it and one wholly below it; each connector's endpoint lies within its associated stage's horizontal bounds; annotation boxes do not overlap.
   - **Handbook application:** Use this for a genuinely ordered subset of the thirteen guides, leaving independent guides directly accessible rather than inventing a single learning sequence for all thirteen.

9. **Repartitioned stack layers**
   - **Where:** Augment Code, `02-augmentcode-full-part03.jpg`, architecture stack at y≈1265–1565.
   - **Mechanism:** Three horizontal layers share outer bounds but divide internally into four, five and four cells. The common width says “one system”; changing partitions prevents the viewer from reading the whole thing as a spreadsheet with false vertical correspondences.
   - **Default it breaks:** Forcing unlike content categories into the same column count, or using a central hub to explain every relationship.
   - **Checkable property:** All layer left/right edges agree within 2px; measured cell counts differ between at least two layers; at least one internal division in one layer falls inside a cell in its neighboring layer rather than aligning with a division.
   - **Handbook application:** Where the content supports a layered explanation, use four skill positions above grouped guide links and three investigation positions, without implying a one-to-one mapping between their unequal inventories.

10. **Unboxed directory columns**
    - **Where:** Augment Code, `02-augmentcode-full-part04.jpg`, footer, approximately y=875–1085.
    - **Mechanism:** Category columns start together but end naturally after different numbers of links, leaving a ragged lower contour. The longest list determines the area needed; the shorter lists are not padded with imagery, descriptions or filler destinations.
    - **Default it breaks:** Treating every navigational category as an equal-height promotional card that must be visually filled.
    - **Checkable property:** Column heading tops agree within 4px; link groups have no fixed equalizing height; with unequal link counts, at least two last-link bottom edges differ by more than one measured row pitch; repeated links have no individual panel border.
    - **Handbook application:** Provide direct indexes for nineteen ideas, thirteen guides, four skills and three investigations, plus a video-page link, allowing each directory to end at its true length.

11. **Change the reading axis**
    - **Where:** Sourcegraph, `03-sourcegraph-problem-part01.jpg`, upper split scene y≈75–300 followed by centered explanation y≈315–700; also visible near the bottom of `03-sourcegraph-part01.jpg`.
    - **Mechanism:** A left-hand statement beside an illustration gives way to a centered glyph above a centered explanation across the next full-width region. The second passage changes the reader's axis rather than mirroring the first split or continuing another row of boxes.
    - **Default it breaks:** Endless left/right, right/left zigzags; one repeated template for every argument.
    - **Checkable property:** In the first region the text center falls left of 0.40W and the visual center right of 0.65W; in the next region both visual and text centers fall within 4px of 0.50W, with the visual wholly above the text.
    - **Handbook application:** Open an investigation with a problem statement beside its authored drawing, then center its central finding below instead of presenting the three investigations as identical summaries.

12. **Persistent page rails**
    - **Where:** Sourcegraph, `03-sourcegraph-part01.jpg`, vertical boundaries around x≈100 and x≈900 running past the hero, demonstration and problem content; continued around the solution in part02.
    - **Mechanism:** Long outer rails establish a shared page field while the content inside changes width and arrangement. Containment belongs to the larger composition rather than being repeatedly rebuilt around every block.
    - **Default it breaks:** Adding a fresh rounded panel around every section to make it feel organized.
    - **Checkable property:** A single rail-bearing ancestor spans at least three consecutive content regions; rail x-coordinates remain constant within 2px; at least two internal regions use different widths, and those regions have no separate four-sided panel wrapper.
    - **Handbook application:** Hold the ideas overview, skill explanation and guide entry points inside one shared field while giving each a different internal structure.

13. **Distributed relationship field**
    - **Where:** Sourcegraph, `03-sourcegraph-graph-part01.jpg`, entire crop; repeated at the top of `03-sourcegraph-part02.jpg`.
    - **Mechanism:** Named file blocks, smaller anonymous blocks and intermediate tokens occupy staggered positions joined by routed connections. The meaningful structure is which objects connect, not a uniform row/column address or one oversized central object.
    - **Default it breaks:** Turning a relationship explanation into equal tiles, or routing everything through a decorative hub.
    - **Checkable property:** Named-node bounding boxes occupy at least three distinct horizontal center bands and three vertical center bands; widths are not all equal; each modeled edge terminates on its declared nodes; no single node is adjacent to every other named node.
    - **Handbook application:** For an investigation detail page only, map a small verified set of idea-to-guide relationships without a universal hub, retaining ordinary reading links outside the diagram.

14. **Paired controlled comparison**
    - **Where:** Sourcegraph, `03-sourcegraph-part02.jpg`, lower portion, y≈925–1315, “Coding Agent” versus “Coding Agent + Sourcegraph MCP.”
    - **Mechanism:** Two aligned panes begin with the same task and then show different responses. Repetition is purposeful here: a shared starting condition makes the divergence legible, unlike two unrelated feature cards placed side by side.
    - **Default it breaks:** Describing a benefit in a generic benefit tile instead of showing comparable evidence.
    - **Checkable property:** Exactly two comparison panes have top edges and widths agreeing within 4px; their initial task nodes have identical normalized text; their subsequent evidence nodes differ; each pane retains its own outcome label.
    - **Handbook application:** Use a documented before/after or two-approach example inside one of the three investigations, never fabricate a favorable comparison just to fill the pair.

15. **Inline extension note**
    - **Where:** Augment Code, `02-augmentcode-full-part03.jpg`, top, “BUILD YOUR OWN /” sentence around y=95–120, following the factory track from part02.
    - **Mechanism:** A compact lead-in and explanatory sentence share one running text block beneath the larger diagram. A secondary possibility is treated as an attached note, not inflated into a new heading, icon, panel and CTA section.
    - **Default it breaks:** Giving every caveat, customization option or secondary path a full promotional card.
    - **Checkable property:** The lead-in and first words of the explanation occupy the same line box at desktop width; the note spans below the preceding composition outside its item nodes; it has no independent panel wrapper or separate action-button block.
    - **Handbook application:** Add a compact note beneath the guide sequence explaining that readers can jump directly to any of the thirteen guides, rather than building another “choose your path” card section.

## Apply these three first

- **Contracted reading lane (#2):** It immediately stops nineteen ideas and thirteen guides from looking like copies of the same catalog, while keeping both collections readable and directly navigable.
- **Change the reading axis (#11):** It introduces substantial composition variation with the existing drawings and real prose; it does not depend on animation, product screenshots or invented relationships.
- **Parent before destination (#3):** It turns related idea/guide material into a useful reading hierarchy instead of a larger pile of equal cards, provided the links reflect the handbook's actual relationships.

## Group B — UX Pilot, Codecademy, Paper/Sourcegraph


These are observed arrangements, not a prescription to copy each page. I read all eleven supplied JPGs once, at their supplied size, without cropping, re-rendering, network access or delegation. Locations below use approximate vertical positions within each named tile, not original-page coordinates.

**Measurement convention:** the checks are proposed DOM/CSS acceptance conditions for a handbook implementation at a comparable desktop width (approximately 1000 CSS pixels). They are not measurements of the references' unavailable DOM. Pixel tolerances and ratio bounds are implementation targets derived from visible relationships, not recovered source values. Mobile behavior and interaction are not established by these captures.

The Paper overview (`06-paper-design-part01.jpg`) establishes the capture's arrangement in its editor, not additional website composition. `06-paper-frame-part06.jpg` is blank; the large vacant regions in frame parts 02–03 and the trailing vacancy in part 05 are not evidence for intentional pacing. No scroll animation, pinning or reveal behavior is inferred. The owner's note supplies transfer boundaries: retain direct skill/guide paths and authored drawings; do not import product screenshots, photography, logo walls or homepage video stills. Applications below are alternatives, not a requirement to put all fourteen devices on one page.

1. **Bridge the seam**
   - **Where:** Codecademy, `05-codecademy-part01.jpg`, y≈475–607: the sign-up panel crosses the bottom edge of the hero image.
   - **Mechanism:** A narrower functional panel occupies both the hero and the space below it, joining two vertical zones into one composition. It is neither a separate equal-sized card nor another section stacked with a positive gap.
   - **Default it breaks:** Every block lives in its own isolated rectangle; hero, action and next section never intersect.
   - **Checkable property:** For hero rectangle H and bridge B, assert `H.top < B.top < H.bottom < B.bottom`; target `0.70 ≤ B.width/H.width ≤ 0.85`, with the horizontal centers within 2px. Reserve flow space so the following content starts at or below `B.bottom`.
   - **Handbook application:** Let a compact direct-entry strip for the four skills bridge the introduction and the handbook body, using no sign-up form, photograph or video still.

2. **Unequal sibling widths**
   - **Where:** Codecademy, `05-codecademy-part01.jpg`, y≈852–1098: “Live Bootcamps and Workshops” beside “All Access Pass.”
   - **Mechanism:** Two siblings share a top and bottom, but one receives roughly twice the horizontal space and contains both explanation and an illustration area; the other is a compact companion. The hierarchy is structural rather than two identical cards with different content.
   - **Default it breaks:** `repeat(2, 1fr)` for every paired feature, and identical internal anatomy for unequal jobs.
   - **Checkable property:** Assert a primary-to-companion width ratio between 1.9 and 2.3, top and bottom differences ≤2px, and two internal content regions in the primary versus one main body region in the companion.
   - **Handbook application:** Give one introductory idea room for its authored drawing and explanation, with a narrower direct guide index beside it instead of promoting every one of the nineteen ideas equally.

3. **Attach the utility**
   - **Where:** Codecademy, `05-codecademy-part02.jpg`, y≈863–963: the “What do you want to learn?” field and the “Not sure?” quiz strip immediately beneath it.
   - **Mechanism:** A secondary route is attached to the bottom of the main control inside one shared envelope. It is a subordinate horizontal layer, not a second button floating nearby or a separate recommendation card.
   - **Default it breaks:** Every alternative needs its own freestanding CTA box, with no spatial relationship to the decision it supports.
   - **Checkable property:** Assert that primary control and utility share left/right edges within 2px, their adjoining edges differ by ≤1px, and utility height is less than half the primary control height; both belong to one enclosing component.
   - **Handbook application:** Attach a “Browse all thirteen guides” route beneath handbook search so readers who cannot name an idea still have a direct path without a new promo card.

4. **Keep lanes fixed**
   - **Where:** UX Pilot, `04-uxpilot-part01.jpg`, bottom from y≈1457, continuing through `04-uxpilot-part02.jpg`, y≈0–1248: four workflow rows.
   - **Mechanism:** All descriptions stay in the left lane and all visual evidence stays in the right, with continuous adjoining rows and a stable center division. Repetition establishes a comparative sequence rather than alternating unrelated left/right feature blocks.
   - **Default it breaks:** Automatic zigzag layouts and four isolated feature cards separated by large gutters.
   - **Checkable property:** Across four rows, assert equal description-lane left edges and equal visual-lane left edges within 2px, identical lane order, row-to-row vertical gaps ≤1px, and no individually enclosed description cards.
   - **Handbook application:** Present the four skills as a continuous four-row comparison, with explanation and direct guide links on the left and each skill's authored drawing on the right.

5. **Crop to the lane**
   - **Where:** UX Pilot, `04-uxpilot-part02.jpg`, right half at y≈247–508, 596–857 and 944–1206: the visual excerpts meet the outer content boundary near x≈897.
   - **Mechanism:** Visuals start inset from the central division but continue to the lane's outer edge, where their content is cut off. The result is an excerpt of a larger working surface, not a tiny complete screenshot centered with equal padding on every side.
   - **Default it breaks:** Shrinking every visual until the whole asset fits inside a symmetric padded card.
   - **Checkable property:** In a clipped visual wrapper, assert positive left inset, zero right inset within 2px, and `asset.right > wrapper.right` with horizontal overflow clipped; keep essential labels outside the clipped portion.
   - **Handbook application:** Use this on guide detail pages for selected examples among the twelve video frames when a meaningful excerpt suffices, not on the homepage and not where cropping removes instructional evidence.

6. **Number the boundaries**
   - **Where:** UX Pilot, `04-uxpilot-part01.jpg`, y≈1227 and 1457, and `04-uxpilot-part02.jpg`, y≈204, 553, 900 and 1248: paired markers on row boundaries.
   - **Mechanism:** The index lives at intersections between the outer rails and horizontal row divisions, not inside each content box. Both ends identify the same boundary, making the whole sequence one measured surface.
   - **Default it breaks:** A floating number badge added to each card without connecting it to the page structure.
   - **Checkable property:** For each indexed division, assert that the two marker centers share its y-coordinate within 2px and coincide with the two content rails within 2px; the division extends beyond both rails. This adds placement constraints absent from the drafting-guide motif in `VOCABULARY.md`.
   - **Handbook application:** Index the nineteen ideas along a continuous reading sequence with boundary markers rather than nineteen separately decorated number chips.

7. **Annotate outside frames**
   - **Where:** UX Pilot, `04-uxpilot-part01.jpg`, y≈518–564: “Made in UX Pilot in <1min” and “Generate Designs & Wireframes” sit above opposite ends of the large visual frame.
   - **Mechanism:** Supporting notes occupy the exterior margin, with short leaders returning to the frame's corners. The framed object keeps its own uninterrupted interior while metadata explains it from outside.
   - **Default it breaks:** Putting every caption, count and contextual label inside a card header, consuming the visual's area.
   - **Checkable property:** Assert that both annotation rectangles are outside the frame rectangle, one anchors to each horizontal edge, and each leader endpoint lies within 2px of its associated frame corner; annotation rectangles must not intersect the main content. This supplies geometry beyond the ruler-note vocabulary already recorded.
   - **Handbook application:** Put an idea number and a real guide reference outside an authored drawing's frame, leaving the drawing itself free of invented metrics or unrelated badges.

8. **Compress secondary routes**
   - **Where:** Codecademy, `05-codecademy-part01.jpg`, y≈742–808, and `05-codecademy-part02.jpg`, y≈151–218: team-training and AI Builder callout rows.
   - **Mechanism:** A secondary destination takes the full content width but very little height, with explanation at one end and a directional control at the other. It interrupts a collection without becoming another member of that collection's card system.
   - **Default it breaks:** Rendering every secondary route as a tall icon–title–description–button card, regardless of its importance.
   - **Checkable property:** Assert row width equals its parent content width within 2px, width/height ≥10, and the trailing control's right edge lies in the final 8% of the row; title and supporting text remain in one content region. This adds structural constraints beyond Codecademy's callout glyph motif.
   - **Handbook application:** Offer “Explore the three investigations” as one shallow cross-page route between the nineteen-idea sequence and the thirteen-guide directory.

9. **Pair unequal masses**
   - **Where:** Sourcegraph, `06-paper-frame-part01.jpg`, y≈1009–1194: the problem statement on the left and wave drawing on the right.
   - **Mechanism:** An unenclosed statement shares a horizontal band with a smaller, edge-anchored drawing; the two visible masses do not fill equal halves. The drawing supports the statement without requiring a matching text card or a mirror-image follow-up section.
   - **Default it breaks:** Every text–image pair becomes a padded 50/50 card or the first half of an automatic alternating sequence.
   - **Checkable property:** Assert disjoint horizontal bounds, a shared vertical overlap, drawing width <35% of the band, and the drawing's right edge aligned to the band's right edge within 2px; neither content block has a separate enclosing panel.
   - **Handbook application:** Introduce the three investigations with one short editorial premise and one relevant authored stroke drawing, then link directly to the investigations rather than drawing a hub-and-spoke map.

10. **Change column count**
    - **Where:** Sourcegraph, `06-paper-frame-part04.jpg`, y≈383–772 followed by y≈961–1256: three oversight columns give way to one broad evolution example.
    - **Mechanism:** Adjacent content groups retain the same outer rails while changing their internal partition from three narrow treatments to a single wide treatment. The section's subject determines the available area instead of a site-wide card width determining every subject's presentation.
    - **Default it breaks:** Reusing one three-column template for every content family or adding a fourth tile merely to preserve a grid.
    - **Checkable property:** Assert matching outer left/right bounds within 2px, three sibling columns in the first group and one full-width item in the next, with the full-width item's width at least 2.8 times one preceding column. This adds a transition rule, not another description of the existing divided-cell motif.
    - **Handbook application:** Give the three investigations a shared three-part introduction, then let a selected guide take the full following width when its explanation needs more room.

11. **Align evidence shelves**
    - **Where:** Sourcegraph, `06-paper-frame-part04.jpg`, y≈383–772: descriptions of Code Insights, Code Monitoring and Living Documentation above their different visual examples.
    - **Mechanism:** Three explanations occupy the upper zone while all evidence begins on a common lower shelf; the evidence pieces are allowed different heights and densities. Shared alignment comes from the shelf, not from forcing every child into the same complete card anatomy.
    - **Default it breaks:** Uniform image–title–body cards, or stretching every visual to identical dimensions to fill a rectangle.
    - **Checkable property:** Assert that the three evidence wrappers' top coordinates differ by ≤2px, each starts below its own description, and at least two evidence contents have different rendered heights without being stretched to match.
    - **Handbook application:** On an investigation detail page, align relevant examples from the twelve video frames beneath three claims while preserving each excerpt's aspect ratio and keeping frames off the homepage.

12. **Leave the last slot**
    - **Where:** Sourcegraph, `06-paper-frame-part04.jpg`, bottom around y≈1560, continuing into `06-paper-frame-part05.jpg`, y≈0–134: “Built for Big Code” has three text items in its first row and two in the next.
    - **Mechanism:** Five real items occupy a three-column text arrangement without manufacturing a sixth or stretching the last pair across the width. The unfilled final position is the honest consequence of the content count, not a defect requiring filler.
    - **Default it breaks:** Forced gapless bento packing, placeholder material, and equalizing the final row simply because a count is inconvenient.
    - **Checkable property:** For N real entries and C columns, assert rendered entry count = N and last-row occupancy = `N mod C` when nonzero; the remaining slot has no element or decorative filler, and last-row column widths equal earlier rows.
    - **Handbook application:** If the thirteen guides use a compact three-column index, keep the thirteenth in the first position of the final row rather than inventing two guides or making it a giant feature.

13. **Separate finding modes**
    - **Where:** Codecademy, `05-codecademy-part02.jpg`, y≈809–1247: a broad search surface precedes “Top courses,” whose catalog link sits at the opposite end of the heading row.
    - **Mechanism:** Intent-driven finding receives its own full-width row before the curated selection begins. The collection heading also provides a separate route to the complete catalog, so featured items do not pretend to be the entire information architecture.
    - **Default it breaks:** Making a decorative card gallery the only route to content, with search demoted to an inconspicuous icon.
    - **Checkable property:** Assert search width ≥95% of the collection width and `search.bottom < collectionHeading.top < firstItem.top`; assert the complete-index link sits on the heading row, outside the item grid, and resolves to a distinct complete-list destination.
    - **Handbook application:** Put handbook search before a small selected-idea display and pair its heading with “All nineteen ideas,” while keeping independent direct paths to all thirteen guides and four skills.

14. **Use ragged directories**
    - **Where:** Sourcegraph, `06-paper-frame-part05.jpg`, y≈731–897: the Platform, Solutions, Resources and Company footer lists.
    - **Mechanism:** Multiple plain link lists share a starting line but end at their own content heights; headings group links without wrapping each destination in a card. The area functions as a compact directory, not a final promotional grid.
    - **Default it breaks:** Adding descriptions, icons and equal-height containers to every link, then padding groups to matching lengths.
    - **Checkable property:** Assert group top coordinates within 2px, each link occupies its own row, group height follows its actual link count with no fixed/minimum equalizing height, and no per-link panel wrapper exists; groups with unequal counts must have unequal bottom coordinates.
    - **Handbook application:** End with separate direct-link lists for thirteen guides, four skills and three investigations, allowing their lengths to differ instead of flattening them into twenty identical destination cards.

## Apply these three first

- **4 — Keep lanes fixed:** The four skills already form a small, meaningful comparison; continuous rows give their drawings and guide links room without turning the homepage into another four-card deck.
- **10 — Change column count:** Give different content families genuinely different space allocations, especially the three investigations versus a guide that needs a broad explanation; this changes the page's composition more substantially than decorative variation inside a fixed grid.
- **14 — Use ragged directories:** Make the thirteen guides, four skills and three investigations directly reachable with compact lists; this removes the supposed need for a card per destination and leaves the main page free to explain the nineteen ideas selectively.
