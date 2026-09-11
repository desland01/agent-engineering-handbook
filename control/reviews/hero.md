# Review — the home page hero loop

2026-09-11. Subject: the animated hero on the home page — an authored SVG loop
(`build/hero.py`) with five agent robots (`build/robots.py`, drawn by a `claude-opus-5`
worker, capsule `handbook-claude-hero-robots-20260911`). Maker: Fable. Reviewer: GLM 5.3
Flash, capsule `handbook-glm-hero-review-20260911`, `precise` and `design-review` loaded,
from five timed frames at 1440, the in-page viewport, a 390 capture and the robot sheet.
Seam continuity is checked by the maker's own measurement, not by the reviewer: element
positions read at t and t + 12 s are identical while control frames differ.

An earlier Higgsfield route (GPT Image 2.5 still driven by Seedance 2.0, first frame = last)
was built for comparison and set aside: bolder as a picture, but 1.6 MB against 14 KB, a
0.5 % first-to-last frame difference, and tokens drifting off the track mid-clip. Its still
is retained in `.scratch/hero-hf/`.

### 1 · Before the plan

**home-1440-viewport.png, two sentences.** The site is a handbook for engineering codebases that AI coding agents can work in: it turns agent mistakes into checks, instructions and skills, and connects a source video's ideas to guides, skills and investigations. The hero promises "build a codebase agents can work in," and the right-hand figure shows agents working against a codebase with some kind of check in the middle.

**The five moments, in order (t0_3 → t2 → t4 → t6_5 → t9), three sentences.** An orange × travels along the dashed track from the agents' side toward the check, and the check flashes orange as it arrives — the mistake being caught. The CHECKS cell then highlights with an orange edge and a new rule bar writes itself in while the CI dot goes orange, and the item re-emerges as an ivory ✓ running the bottom track (CONTEXT · WHAT THE AGENT READS) back toward the agents. Meanwhile each of the five agent windows types its prompt line at its own pace, with the next orange × already forming on a different agent's line (Gemini at t6_5), so the mistake → catch → rule cycle is clearly repeating.

### 2 · Against the plan

Landed unaided: the overall story (agents make changes; a check catches the bad ones; a rule gets written into the codebase), the one-accent discipline, the five named agents, the terminal-window framing, the closed loop. The maker's brief — "shows what the site is about at a glance," "plain language," "mistake caught at the check, rule written into CHECKS" — is met by the picture without the plan.

Needed the plan to fully understand: that every third change is the mistake (reads as "sometimes" from stills, which is fine); that the burst at the catch is dots by design rather than a glow (it reads as dots either way — the plan only confirms intent); that the loop is 12 s and seamless (unverifiable from stills; not checked, and I do not claim it); and that reduced motion pauses it (no evidence supplied either way — unverified). One plan/evidence mismatch: the plan names five robots, but robots-sheet.png calibrates only three (claude, codex, gemini) at 22/60/160 px; Kimi and Z.AI are judged only as they appear in the hero.

### 3 · Findings

1. **page@1440 (viewport, in place)** — At the size the hero actually renders on the page, the mono sub-captions ("CI · LINT RULES · TESTS", "CLAUDE.MD · AGENTS.MD", "TOOLS THE AGENT CAN CALL", "PREVIEWS · TYPES · DOCS") sit at the floor of legibility: small, dim grey, and they read as texture rather than words. Evidence: home-1440-viewport.png right column. Rule: brief — "readable text". Fix: one step up in caption size or one step up from dim to muted for the cell sub-captions only. **Should.**
2. **page@390** — At phone width the hero shrinks to a thumbnail of itself: labels ("CODEBASE", "AGENT 01", "CONTEXT") render around 6 px and are unreadable, the robots collapse to dashes, and the substituted generic labels ("AGENT 01/02/03", "+ TOOLS") lose the named-agent story entirely. It reads as decoration, contradicting the brief's "captions that are decoration" anti-goal. Evidence: home-390-hero.png. Fix: at this width either scale the figure up to a full-width band with legible labels, or replace it with a deliberately simpler crop (e.g. two agents and the check only, labels omitted on purpose) rather than a uniformly scaled-down duplicate. **Should.**
3. **hero t0_3** — The ivory ✓ track marker sits on top of the INSTRUCTIONS sub-caption, partially covering "AGENTS.MD". Evidence: hero-1440-t0_3.png, left panel. Rule: brief — "readable text"; captions not decoration. Fix: inset the vertical track segment a few px from the cells, or pad the caption clear of the track line. **Could.**
4. **hero, all moments** — The Codex robot's brand mark reads as a dark scribble blob at hero size (~30 px), while Claude's burst and Gemini's sparkle read clearly; the five still read as one family, but Codex is the weakest identifier. Evidence: hero-1440-t2.png vs robots-sheet.png (where the knot only resolves at 60 px+). Fix: simplify the Codex knot to a heavier, fewer-strand mark that survives small sizes. **Could.**
5. **robots-sheet.png** — The calibration sheet shows only three of the five robots, so the 22 px legibility of the Kimi "K" and Z.AI "Z" marks is unmeasured; in the hero they read, but the sheet as a working document is incomplete against the plan's five. Evidence: robots-sheet.png vs PLAN.md ("Claude, Codex, Gemini, Kimi, Z.ai"). Fix: add kimi and z.ai rows at the same three sizes. **Could.**
6. **hero t9** — Three orange elements are live at once (the × on the top track, an orange cursor on Gemini's line, an orange segment on Z.AI's line). This stays inside the plan's allowed accent set (mistake, catch, cursor), but at a glance the top-right of the figure carries three separate orange points, slightly diluting the mistake as *the* event. Evidence: hero-1440-t9.png. Fix: stagger cursor activity so a live mistake never coincides with more than one other orange cursor. **Could.**

Not findings, checked and passing: no second hue anywhere in the figure (one-accent rule holds); the catch burst is dots, no glow, gradient or blur observed in any moment; "PULL REQUESTS", "THE CHECK", "CONTEXT · WHAT THE AGENT READS" are words a developer would actually say — no internal/system jargon ("CI" is ordinary developer vocabulary).

### 4 · Direct answers

- **Is every caption readable at 1440?** At the full-size hero moments, yes — all captions read, including "CLAUDE.MD · AGENTS.MD" except where finding 3's marker crosses it. At the in-page 1440 viewport, the four cell sub-captions do not comfortably read (finding 1). None is fully illegible at either size.
- **Does any caption read as internal or system jargon?** No. All captions are plain developer language.
- **Do the five robots read as one family and as agents, and are brand marks legible at hero size?** Yes — same body, feet, antenna and terminal window throughout; they read as little agent robots, and the name labels (CLAUDE…Z.AI) disambiguate. Marks are legible at hero size except Codex's, which is the weak one (finding 4). At 22 px (sheet) no mark is legible; the hero does not use that size.
- **Does the mistake → catch → rule story land without the plan?** Yes. The orange ×, the orange flash at the check, the highlighted CHECKS cell with a new bar, and the ivory ✓ returning are legible as a repeating cycle from the stills alone. What does not land without the plan is the *cadence* (every third) — acceptable, since it is rhythm, not meaning.
- **Anything breaking the one-accent or no-glow rules?** No. Only orange appears as chromatic colour, and every orange use is a mistake, a catch, or a cursor — the plan's allowed set. The burst is dots; no glow or blur observed in any of the five moments.
- **At 390, does the hero read or need a different crop?** It does not read as content — it needs a different treatment (finding 2). The current uniform down-scale with renamed generic labels is the weakest thing in the set.

### Verdict

**SHIP** at 1440 — no blocking items. Before or shortly after ship, address finding 2 (the 390 crop) and finding 1 (sub-caption legibility in place); the rest are polish.

Unverified, stated plainly: loop seamlessness at t = t+12 s, reduced-motion behavior, and the live rendering at any viewport — all judged from five stills and two viewport captures only.


## Maker's answers

| # | Finding | Answer |
|---|---|---|
| 1 | Cell sub-captions at the floor of legibility in place at 1440 | **Applied.** Size 11 → 12.5 units and colour dim → muted at 80%. |
| 2 | At 390 the hero is a thumbnail; labels ~6px; generic AGENT 01 labels | **Applied, with a correction to the evidence.** The 390 capture supplied was from the previous hero (AGENT 01 labels); the reviewed build already names the agents. The size problem was real: below 640px the figure now bleeds to the gutters and its captions are re-set by CSS — labels 24 units, agent names 18, sub-captions and track captions off — so the same drawing reads at phone width instead of a uniform shrink. Re-captured at 390. |
| 3 | Track marker crosses "CLAUDE.md · AGENTS.md" | **Applied.** The track's left leg moved from the cells' centre (x 214) to inside their right edge (x 318), clear of every caption and bar. |
| 4 | Codex mark reads as a blob at hero size | **Overruled.** The mark is OpenAI's own; simplifying it would be redrawing a trademark, and the window's CODEX label carries the identification. Left as delivered. |
| 5 | Robot sheet showed three of five | **Applied.** The sheet was cropped by my screenshot viewport, not by the worker; re-captured full-page with all five rows. |
| 6 | Three orange points live at once at t9 | **Overruled.** Cursors are within the language's permitted accent placements (small markers) and the mistake is the only orange *object on the track*; staggering five typing phases against three catch moments would cost the independent rhythm that makes the agents read as working. |

Re-render: `build/check.sh` green; seam re-verified (positions at t and t+12 s identical, control differs).


## Revision after the review — the robots ride the track

The owner's correction, 2026-09-11: the moving squares were meant to be the robots. Rebuilt
accordingly: the five robots walk the track themselves (one per agent, terminal windows kept
as their names and typing lines); no parcels and no brand marks on the track — on its lap a
robot *is* the mistake, orange with an × on its chest, and turns ivory with a ✓ when the
check catches it. The mistake rotates through the five robots so no one tool is "the one
that gets it wrong"; the full cycle is therefore five laps (60 s). Measured: positions
repeat every 12 s, full state (colour and chest mark) repeats exactly at 60 s, and states
differ between laps. `check.sh` green. This revision has not been re-reviewed by a second
route; the composition, captions and 390 treatment the reviewer passed are unchanged, the
moving element is what changed.
