# Handoff — 2026-09-10, end of the owner's session

Every instruction the owner gave today, what happened to it, and where it lives. "Done"
means landed on `main` with `check.sh` green. "Open" items carry their plan reference in
`control/plan.md` (§3 workstream letters) and
`control/tickets.md` (ticket ids). The earlier handoff
(`control/reviews/owner-qa.md`) covers the morning; this one supersedes its open list.

## The owner's instructions, in order

| # | Instruction (paraphrased) | Status | Where |
| --- | --- | --- | --- |
| 1 | Redesign the five hubs by taste, with ux-copy, the design language and the SEO skill | Done | commits through `c3a87d0`; `control/design-notes.md` |
| 2 | No production URL yet — leave markers | Done | `SITE_URL` in `build/render.py`; canonical all-or-nothing check |
| 3 | The problem panel is a design graphic: Higgsfield / gpt-image-2.5 + a scroll animation | **Open** — Higgsfield is set up; one transparent-background attempt came back opaque, not adopted | plan B4; ticket B4 |
| 4 | Ideas as a horizontal swipe row | Done | `.ideas-row`, `rows()` controls |
| 5 | Investigations: more creative than 3 cards + blank | Done — studies, full viewport each, CTA | `investigations_index` |
| 6 | Frames band as a scroll section | Deliberately left quiet (recorded) | `control/design-notes.md` |
| 7 | No block text on the home page; motion "big time"; hover; one terminal animation; GSAP / Framer / 3JS | Partly: 0 KB hand-written motion (typed prompt, trace, reveals, seams, hover). GSAP/3JS not adopted. **Decision open**: whether one pinned study earns the 44 KB | plan B5; ticket B5 |
| 8 | Rail scrollbar; a check to stop scrollbars | Done | `check-render.js` scrollbar chrome check |
| 9 | Gap between body and rail | Done | `.reader` grid gap |
| 10 | 19 ideas: group into tiers, not a homework list | Done | `EVIDENCE_TIER`, `.tier` |
| 11 | Guides page "blocky, FAIL" | Done for the band figures (2×2 loops, track, studies, ledger). Composition pass still open | plan B3; ticket B3 |
| 12 | Skill page has no type hierarchy | Done | reader type scale |
| 13 | Investigations: three full-viewport sections with visuals and a learn-more CTA | Done | `.study` |
| 14 | Make it irresistible to share (Theo, Matt Pocock, Boris); good copy; /simple | Plan acceptance criterion; not yet judged | plan §5 |
| 15 | Use agents to save tokens; lean heavy on astra for writing and planning | Practiced: astra wrote copy, idea pages, tickets, headings, pattern scans; glm reads | `control/skill-evals.md` §1 |
| 16 | Astra rewrites the copy; design QA as a report only | Done | `control/reviews/copy-rewrite.md`, `control/reviews/design-qa.md` |
| 17 | The 900s/60-request cap on astra is anti-Nautilus | Done — limits null | `~/.nautilus/architect/workspace/route-descriptors-20260910/gpt-6-astra.route.md` |
| 18 | Fix all design findings unless a bad suggestion | Done — 3 applied; astra's rail-label fix rejected as bad | `control/reviews/design-qa.md` "Applied" |
| 19 | Horizontal rows capture the wheel | Done — per-axis contain + wheel probe in the checker | `check-render.js` |
| 20 | Set up Higgsfield (CLI, auth, companion skills) | Done — CLI 1.1.24, signed in, 8 skills | `.agents/skills/` → `.claude/skills/` |
| 21 | Third skill category: product skills, uncapped, manufacturer-maintained, never edited | Implemented test-first in a runtime snapshot (13/13 tests); **not shipped** | `control/runtime/product-skills/`; plan D1; owner decision 4 |
| 22 | Readopt `~/.agents/skills/copy` whole | Staged; needs the authoring run | plan D2; owner decision 4 |
| 23 | Design skills open with a Role, like gpt-taste | Standard written; two drafts by astra reviewed; **not published** | `control/design-skill-standard.md`, `control/proposals/`; owner decision 1 |
| 24 | "The instruction is not the output" — headings like "What was said" | Rule + check + 19 pages rewritten | `ARCHITECT.md`; `check.py` idea-page rule |
| 25 | "Does this diagram even make sense?" | Redrawn with in-artwork captions; rendered review by astra | `control/reviews/diagrams.md` |
| 26 | A review process for parallel agents; design reviewed before it lands | Rule written; used on every worker output since; gate machinery tickets | `ARCHITECT.md`; tickets C1–C3 |
| 27 | "Would no skill be better?" — write the full plan | Plan written; the controlled comparison **has not run** | plan §3 C4; tickets C4a–C4h |
| 28 | Adopt long-running-harness execution shape | Done — ticket graph, `check-report.cjs`, qualityReceipt as the gate slot | plan §3 C |
| 29 | Rail TOC matches the new H2s | Done | `idea_page()` builds the rail from written headings |
| 30 | gpt-taste-style checks that break the model out of slop | Standard + slop checks (h1 lines, orphans, clipped headings, adjacent-band figure signature, drawing size, blank cells, contrast, emoji, eyebrows) | `check-render.js` slop section |
| 31 | No eyebrow titles; no asymmetric blank cells; break out of systematized grids; scan the references for mechanical patterns | Eyebrows removed + check; blank-cell check; **pattern scan delivered** (29 patterns); application open | `control/patterns.md`; plan B8 → B3 |
| 32 | No jargon in front-facing copy; five seconds from any viewpoint | Rule + rendered check; guide shelves rewritten | `ARCHITECT.md`; `check-render.js` jargon rule; commit `7f49982` |
| 33 | Are the skills used, and working? Share evals | Answered from run records; the one eval that answers the design question (C4) has not run | `control/skill-evals.md` |
| 34 | "Repeated fixes spend tokens" reads as the opposite — headings must be clear alone | Done — rule written; 72 of 76 rewritten by astra; heading-only read by glm found 1 contradiction (fixed) and 2 to simplify; 76/76 pass | `ARCHITECT.md`; `control/reviews/headings.md`; plan B6 |

## What is open, in the order it should go

1. **Owner decisions** (plan §6): the worked opener's voice; the five doctrine conflicts;
   guides'/skills' shared section headings; go on D1 (product skills) and D2 (copy);
   Higgsfield placement. And two from today: motion (B5) and whether `.agents/`,
   `.claude/`, `skills-lock.json` are committed or ignored (D3).
2. **C4, the controlled comparison.** It is the only thing that answers "would no skill be
   better". Everything needed exists except the frozen brief; tickets C4–C4h are prepared.
3. **B3, the home composition pass**, now with `control/patterns.md` as input:
   both scans' first picks say the same thing — give the content families genuinely
   different widths and reading axes, not one grid dressed six ways.
4. **B4, the Higgsfield graphic** for the problem panel.
5. The remaining ten skill rewrites (A3–A4f), two at a time, behind the standard.
6. Small copy item: the tip-05 "fit" section opens with a token name and a curl flag on a reader page; the jargon check covers front-facing selectors only.

## How to run things

- Build: `uv run --python 3.13 --with Markdown==3.10.3 python build/render.py`
  (no `.venv` exists in the checkout; `/opt/homebrew/bin/python3` lacks `markdown`).
- Check: `bash build/check.sh` — `check.py` (54 pages) then `check-render.js` (72 checks at
  390 and 1440, needs `cd build && npm install` once).
- Workers: `~/.nautilus/bin/nautilus-worker --workspace DIR --task DIR/TASK.md --capsule
  DIR/capsule.json --model ROUTE`, capsule v4 with non-empty `requiredCharts`, bound to the
  release under `~/.nautilus/current` at dispatch. Working release lines:
  `browser-route-20260910`, `task-file-20260910`, `premium-tech-design-20260910b`. The
  `skill-packs-*` line reports present Charts as unavailable — do not use it.
- Every worker output is reviewed by a different route before it lands (rule in
  `ARCHITECT.md`); the review record goes in `control/reviews/`.
