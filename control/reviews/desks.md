# Review — the empty workstations on idea 18

2026-09-11. Subject: the three-station figure at the head of idea 18, the page carrying the
video's career-level claim. Maker: Fable. Reviewer: GLM 5.3 Flash, capsule
`handbook-desks-review-20260911`, `precise` and `design-review` loaded, from the page at
1440 and 390 and three moments of the figure.

The first dispatch was refused: `workspace_overlaps_installation_home`. The runtime admits a
workspace inside the installation only under the *current* release's `var/workspaces`, and
`current` had moved to `skill-selection-charts` mid-session. Re-dispatched with the root and
the digest read from `current` at launch. Nothing was weakened to get the run through.

### Pre-read impression (written before reading PLAN.md)

The figure shows three framed workspaces — a stream desk, a course desk, an interview set — each with a screen landing a green check, a chair pushed back, and a small robot at the desk. It is saying that the people behind this content aren't here: the systems they describe keep producing output without them, echoing the headline's claim that building such environments is the career-level skill.

Is it funny? Mildly at best. "ON AIR · NO" and the two empty interview chairs are a quiet smirk rather than a laugh, and because the robot is the brightest thing in every panel, the first read is "cute robot at desks" — you have to work to get "nobody's here," which is the opposite of how a joke should land.

### Answers to the specific questions

- **Three empty workstations, or three generic desks with robots?** Three *stations*, yes — mic arm, camera, and the two-chair interview set distinguish them. But not obviously *empty* workstations: the robot is the highest-contrast element in every panel, so the eye reads "robot at a desk" first and "nobody here" second. The joke's subject (absence) is the dimmest thing in the drawing (page-1440.png, all three panels).
- **Empty on purpose?** Not visually obvious. The pushed-back chairs help, but the stream and course chairs partially merge into the desk hairlines at rendered size, and nothing in framing or spacing foregrounds the absence. The status lines ("ON AIR · NO", "GUEST · AWAY") do the telling — the picture alone doesn't.
- **Does the joke land without a caption?** Partly: the mono status lines are micro-captions and they carry it. Without them, no. For a reader who has never seen the source video, it still reads as "empty studios, the work continues," but the bridge to the headline's *career-level skill* argument is made by the reader, not the figure — it reads as "creators away," not "the environment outlives its maker."
- **Are the three stations distinguishable at rendered size?** At 1440, yes. At 390, no as a composition: the strip scrolls in its own region, only ~1.7 panels are visible, and the second panel is cut mid-desk with its caption clipped (page-390.png). Within a visible panel, the stations are distinct.
- **One-accent rule?** Within spirit but at the limit. Orange appears on the landing check (×3), the playhead, the lamp's three light strokes, and the robots' own accent pixels. Per-panel it is roughly the check plus one more element, but "The Interview" stacks lamp-light + check + robot accent. Quoted rule (DESIGN.md): "There is one accent and no second hue: nothing on the page is coloured to carry meaning that a label could carry instead."
- **No-glow rule?** Passes. The lamp's "light" is three hairline strokes, not a glow — the right reading of the rule. Quoted rule (DESIGN.md): "**Depth: none.** No drop shadow, glass or glow anywhere in `main`."
- **No drawings of people?** Passes. No faces, figures or silhouettes; the empty chairs carry it, exactly as PLAN.md commits ("nobody is named and nobody is drawn").
- **Caption readability?** All six captions legible at 1440. At 390, "THE COURSE" panel's caption is clipped by the scroll viewport on first view ("THE COURSE RENDER…" runs off); readable after scrolling, truncated as first seen.

### Findings

1. **page@390 / moment: n/a — blocking.** The second panel is cut mid-frame on first view and its caption is clipped ("THE COURSE RENDER…"), so a phone reader sees one and a half desks with a truncated label before scrolling. Evidence: page-390.png. Rule (PLAN.md): "below the two-column breakpoint it scrolls in its own region rather than shrinking" — the region exists but the panel boundaries land mid-desk with no snap or edge fade signalling more content. Fix: snap the scroll region to panel starts (proximity snapping, as the ideas row already does) and add the same fading edge the home page's idea row uses, so a clipped panel reads as "scroll for more," not as a rendering mistake.
2. **All moments — blocking.** The figure doesn't read as *empty* workstations at first glance: the robot is the brightest, highest-contrast element in every panel while the empty chairs are dim hairlines, inverting the joke's subject and punchline. Evidence: figure-t1.png, all three panels. Rule (PLAN.md): "The joke is carried by the empty chairs and the mono status lines instead" — currently the robot carries it. Fix: rebalance emphasis without a glow — dim the robots one step toward the muted range and/or give the chairs a slightly stronger stroke (e.g. `--border-strong`) so the vacancy, not the robot, is the first read. Re-render and compare before/after.
3. **All moments — should.** The connection between the empty stations and the headline's "career-level skill" claim is left entirely to the reader; nothing visually links "the environment keeps working" to the checks landing on their own. Evidence: page-1440.png — the headline says career-level skill; the panels say "creators away." Rule (PLAN.md): "each station has a screen that keeps landing green checks on its own" — that idea is drawn but the check is a small, static-seeming element at page size. Fix: give the check a subtle periodic appearance (part of the existing 9-second loop, paused under reduced motion) so "landing on its own" is observed, not implied; if that's too much motion, accept and document this as a deliberate gap.
4. **page@1440 / The Interview — should.** Accent density is highest in the third panel: lamp's three orange strokes + orange check + orange robot accent pixels, pushing against the one-accent rule inside a single frame. Evidence: figure-t1.png, third panel. Rule (DESIGN.md): "nothing on the page is coloured to carry meaning that a label could carry instead." Fix: drop the robot's accent pixels in this panel (or all panels) to neutral — the lamp already owns the panel's warmth.
5. **page@390 — could.** The interview panel's two chairs + mic + lamp compress to the point where the "two empty chairs" — the strongest single image of the joke — is the least legible part at phone width, and the reader must scroll to reach it at all. Evidence: page-390.png (interview panel off-screen), figure-t5_5.png. Fix: optional — order the panels so the interview set is not last on phones, or accept the scroll; the desktop composition is the primary experience.
6. **t1 vs t3, The Stream panel — could.** The chat "keeps scrolling" per PLAN.md, but between the supplied moments the only visible changes are the check and the playhead; no chat motion is discernible in the evidence, so the stream panel reads static compared to its description. Evidence: figure-t1.png vs figure-t3.png, first panel. This may be a limitation of only three sampled moments (t1/t3 differ by 2s of a 9s loop) rather than a defect — flagged as unverified, not as a confirmed failure. Fix if real: give the chat lines a visible stepped scroll within the loop.
7. **All moments — could (passes, noted for the record).** Caption contrast and size conform: 11px uppercase mono at the muted step matches the vocabulary key and DESIGN.md's mono-label role; all six captions read cleanly at 1440. No action needed.
8. **All moments — could (passes, noted for the record).** No people drawn, no glow, hairline-only structure, square 4px-ish frames — all consistent with DESIGN.md's depth and illustration rules, and with PLAN.md's defensible decision to name nobody.

### Verdict

**FIX FIRST** — items 1 and 2:

1. Phone-width panel clipping without snap or fade cue makes the figure read as broken at 390.
2. Emphasis inversion: the robot, not the emptiness, is the first read, so the joke doesn't land as drawn.


## Maker's answers

| # | Finding | Answer |
|---|---|---|
| 1 | At 390 the strip cuts mid-desk with no snap or fade, so it reads as broken | **Applied.** The figure was one wide drawing; it is now three drawings in a scrolling row. Each station is a scroll-snap target, one fills the column at phone width with the next peeking, and the row carries the same trailing fade the nineteen-idea row uses. Measured at 390: station 308px in a 358px row, `is-overflowing` set, snapping on. |
| 2 | The robot is the brightest thing, so "robot at a desk" reads before "nobody here" | **Applied.** The reviewer is right that the joke's subject was the dimmest element. The robots drop to half-strength ink and lose their accent pixel in this figure; the chairs go up to 0.85 stroke at 1.8 width. The empty chair is now the brightest thing in each panel. |
| 3 | The check reads as static, so "landing on its own" is implied rather than observed | **Overruled on the evidence, not on the point.** The check is already animated: it appears on a row, holds, and clears, once per station per 9-second loop, which is why the seam test at t and t + 9 s is identical while control frames differ. Three stills two seconds apart in a nine-second loop cannot show it. No change; the reviewer could not have known from the evidence supplied, which is a fault in my evidence, not in the drawing. |
| 4 | Accent density highest in the interview panel: lamp + check + robot pixels | **Applied**, by the same change as 2 — the robots carry no accent here, so the panel is lamp and check only. |
| 5 | At 390 the interview panel is last and least legible | **Accepted as a known limit.** Desktop is the primary reading of this figure; with 1 fixed, reaching the third station is an ordinary scroll with a visible affordance rather than a clipped frame. Not reordered: the three read left to right as a sequence. |
| 6 | The stream's chat looks static between the sampled moments | **Overruled on the evidence**, same reason as 3: the chat lines step on a fifth of the loop. Unverifiable from three stills. |
| 7, 8 | Captions, no people, no glow, hairline structure — pass | Noted. |

Re-render after the fixes: `build/check.sh` green; seam re-measured identical at t and t + 9 s across all three drawings, control frames differ.

