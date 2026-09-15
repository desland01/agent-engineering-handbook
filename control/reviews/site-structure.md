# The local rebuild passes structural checks

Phase 5 · September 13, 2026 · local snapshot only.

The site now has ten lessons, seven skill explanations and one complete menu. The
visitor walk starts at the home page and follows only the header and that menu.
It reaches all 33 kept or new pages and directly links all 156 approved addresses.
It reports no unreachable pages or broken navigation.

## The changes address the observed defects

| Finding | Disposition | Evidence |
|---|---|---|
| Reference opened a competing guide course. | Applied: the header now says Sources; guides redirect to their owning lessons. | The default checker checks the exact page set and redirect destinations. |
| Recovery was outside the ten-lesson path. | Applied: recovery is lesson 9, and all eight problem rows open lessons. | Catalog and home-page regression tests. |
| Fresh-agent duplicated useful-instructions. | Applied: both old addresses redirect to the merged lesson or its source companion. | The catalog assigns each guide and idea once. |
| The menu omitted pages and repeated GitHub. | Applied: every approved address has its plain label in one menu; its final link is the only repository navigation link. | Menu checks on all 33 generated pages and the independent visitor walk. |
| The old menu could grow beyond the screen. | Implemented, visual result still open: its width and height are bounded, labels wrap, and the panel scrolls. | Source inspection only; the browser check could not run. |
| Reader pages added video apparatus or agent instructions around the accepted prose. | Applied: the ten lesson sources and seven skill explanations supply the articles. | Article tests check the opening, source heading, unchanged citation list and next action, and absence of the old fragment targets. All LS01–LS12 checks pass. |
| Hub copy exposed paths and described a second course. | Applied: the changed hubs use plain words and conclusion headings. | Source-text inspection and a default guard for paths, hashes, code and tool internals. |

## Browser evidence remains unavailable

No screenshots were produced or inspected. No browser session reached the site.
The following are actual failures, not passing or partial visual evidence:

- The local preview server exited 1: `PermissionError: [Errno 1] Operation not permitted`.
  It was not retried through another address, port or execution route.
- The supported local browser runner exited 1:
  `Error [ERR_MODULE_NOT_FOUND]: Cannot find module '/Users/thebeast/.npm-global/lib/node_modules/@browserbasehq/stagehand/dist/index.mjs' imported from /Users/thebeast/.nautilus/releases/seo-campaign-gated/release/charts/core-skills/bundles/browser/scripts/stagehand-local.mjs`.
- The project's rendered test exited 1: `Error: Cannot find module 'puppeteer'`.
  Its syntax check passes, but that does not establish browser behavior.
- The shell check passes its Python stages and explicitly skips its browser stage.

Viewport fit, opening-paragraph fit, menu scrolling and wrapping in a browser,
keyboard behavior, visual composition, contrast and motion remain unverified for
this revision. The existing browser suite retains these checks and adds the long
menu interaction; none is waived. Run it in an authorized environment with its
existing dependencies and local-server permission before relying on visual readiness.

No review agents were dispatched because this release prohibits dispatch. This is a
local implementation and evidence record, not the two-agent rendered review mentioned
in the historical assignment. No publishing or live redirect test was performed.

## Rendered review: two routes, every finding answered

Date: 2026-09-13. Evidence: 13 page-size tiles at 390x844 and 1440x900, captured with motion disabled after the rebuild was applied to the real repository; `node build/check-render.js` passed 108 rendered checks before and after the fixes below. Reviewers: glm-5.3-flash (composition, run 124704f9-3f28-4f84-a3d1-412ffdd3114a) and kimi-k3-256k (copy, run c09d932e-aab9-451a-80e8-f0ccc6648340), both with the design-review and precise methods invoked. Raw reviews sit in each reviewer's workspace `REVIEW.md`. Maker: Fable 5.1.

| # | Route | Finding | Impact | Disposition |
|---|---|---|---|---|
| C1 | composition | Sources page diagram: "PUBLISHED ARTIFACT" clipped at the drawing edge, "ONE HTTP TRANSPORT" collides with the capsule stroke. | high | Applied: labels shortened to "PUBLISHED" and "HTTP TRANSPORT" in `build/icons.py`; after render shows both inside the drawing. |
| C2 | composition | More menu runs past the viewport with no affordance that it scrolls. | medium | Applied: a 28px bottom fade on the menu panel, the site's rail idiom; measured after fix: scroll height 8203 vs client 754 at 390, overflow auto, mask applied. A thin scrollbar was tried and reverted because the rendered check bans scrollbar chrome. |
| C3 | composition | Lessons index repeats "Sources and one next action" on all ten rows. | medium | Applied: the constant phrases removed; only the per-lesson reading estimate remains. |
| C4 | composition | Four drawings serve seven skill cards; two pairs share a picture. | polish | Applied: the owner chose the generated set on 2026-09-13 after seeing both alternatives side by side. All seven skill icons are now Higgsfield (nano_banana_2, 14 credits) images, cleaned to transparent 256px webp in `build/assets/` and embedded inline so no page loads a network image. The drawn monoline alternatives stay in git history for recovery. Checks pass after the change. |
| C5 | composition | "From the original repository research" beside "N ideas feed it" reads as a missing value. | polish | Overruled: the honest-count-where-one-exists rule is documented in DESIGN.md; a placeholder would invent a count. |
| C6 | composition | Phone skills band repeats an AVAILABLE badge under each card. | polish | Deferred: documented deliberate choice; revisit with C4. |
| K1 | copy | Template vocabulary in reader copy: "Sources and one next action" and the home lead's "try the next action". | medium | Applied: row meta removed (same change as C3); home lead now ends "try one change". |
| K2 | copy | Skill card captions "MISTAKE → CHECK" read as field labels above headings. | medium | Applied: captions removed from the skill tiles. |
| K3 | copy | Closing route head "Choose your next step" differs from DESIGN.md's documented wording. | polish | Applied to the document: DESIGN.md now records the rendered head; the pages are unchanged. |
| K4 | copy | Menu shows "Lessons" as a Start-here link and again as a group label. | polish | Overruled: the group labels are the owner-approved plan's labels; the header is a span, not a second link. |
| K5 | copy | The unnumbered worked-example item sits between lessons 01 and 02. | polish | Overruled for now: the label is the plan's; a "Example:" prefix is queued for the next plan revision. |
| K6 | copy | Evidence defect: menu tiles showed an old problem-row title. | none | Recorded: the menu tiles were captured before the README problem rows were updated; the after capture shows the new title. |

## Home copy rewrite: reviewed before landing

Date: 2026-09-14. The owner asked for the home page copy in a trusted-advisor voice with hooks. Maker: Fable 5.1. Reviewer: kimi-k3-256k from the rendered page text (run 7c98361e-8947-42f9-b912-8de792c8b6dd, design-review and precise invoked). Verdict: fix first, blocking item the lead's reversal.

| # | Finding | Impact | Disposition |
|---|---|---|---|
| H1 | Lead pair "The fix is rarely another prompt. It is a check…" is a rhetorical reversal with a padded list. | high | Applied: "You fix it by adding a check, a working preview, or one sentence to the right file." |
| H2 | Step headings "Your problem / Your lesson / A fix to try" name topics, not conclusions. | medium | Applied: "Name what keeps going wrong", "Read the one lesson that covers it", "Try one change and check it today"; descriptions lengthened past the floor. |
| H3 | Picker lead sentences under the length floor. | medium | Applied: the reviewer's rewrite. |
| H4 | "What was checked, and what was not" is a topic, not a claim. | polish | Applied: "Every check below names what it does not prove". |
| H5 | Lessons description under the floor. | polish | Applied. |
| H6 | Skills description under the floor and not addressed to the reader. | polish | Applied. |

Also fixed in this pass at the owner's request: the Sources diagram caption "RESUMED RUN → SAME ARTIFACT, TAG #A7F3" overran the drawing and is now centred and shortened.
