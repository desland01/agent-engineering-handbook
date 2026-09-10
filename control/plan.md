# Getting the premium-tech design system going — plan of record, 2026-09-10

## Resumed execution on September 10

The instruction to read and execute the handoff resumed the ready work. Current delivery:

| Work | Observed state |
|---|---|
| Domain and deployment | Live at `https://agent-engineering-handbook.dev`; Vercel production is READY. Desktop and mobile inspected, with no overflow or console/page errors. See `reviews/deployment.md`. |
| Corrected Charts | Published and selected as `handbook-heading-corrections`; 17 files match the exact 28 reviewed line replacements. Prior release retained. Native Explainer delivery read back; see `reviews/chart-headings.md`. |
| D3 local agent files | Ignored by Git and excluded from deployments; preserved on disk. |
| Local preview | Running at `http://localhost:8000/`, serving this repository's `public/`. |
| B3/B5 composition and motion | Fable refinement `d8f5d038-e27c-4d8b-b4ce-36d51dbc1540` reviewed and integrated. Real build and 72 rendered checks pass, including the mobile report regression; final desktop/mobile renders and three study scroll reveals inspected. Native motion selected; no GSAP or pin. See `reviews/home-composition.md`. |
| B4 graphic | Concurrent commit `67f3bd8` landed the 40,298-byte problem drawing and scroll reveal. Preserved during composition integration. This run also generated six transparent candidates, retained unused in `.scratch/handbook-graphic/`. |
| B9 headings and upload copy | Astra run `d3718553-c2e5-40e0-99e6-ba1b104f5fe4` ended blocked: HTTP 429, all credentials for the requested route cooling down. No source changes or substitute route. |
| C4 blind comparison | Still unrun; its requested Astra reviewer is currently unavailable with the same provider cooldown. |
| D1 product runtime | The named shared runtime source still has 5,460 dirty entries; the handoff's clear-tree prerequisite is unmet. No patch applied there. |

The three method additions (Precise, Create Skill and Pilot First combined into Long-running
Harness) completed native authoring, but publication refused `skill_content_library_bytes`.
The selected library occupies 2,096,342 of 2,097,152 bytes; the proposal adds 11,063 bytes
and exceeds the limit by 10,253. No allowance was raised or existing expertise removed.
See `reviews/method-publication.md`. The role-first drafts and whole-copy readoption also
remain staged. The active release contains only the reviewed heading corrections.

Written 2026-09-10 from the day's feedback, in the order it arrived: the hubs were
thin; the whole page was blocky; nineteen was homework; the type had no hierarchy; the
scrollbars; the copy; the Higgsfield graphic never landed; the schema labels shipped as
headings; the diagrams mean nothing at size; and finally — coding productivity is great and
design has gone to garbage, and maybe no skill at all would do better. This plan takes all
of that as true and says what to do about it, with the tools now in hand.

## 1. What is actually wrong — three causes, one fix each

| Cause | Evidence today | Fix |
|---|---|---|
| **The design skills speak in spec register.** `precise` claims "reusable methods," so every design skill opens with a task, a provenance note and a procedure. One of twelve opens with a role. | Every band the same grid; drawings at 52px; a correct, careful, dull page | Role-first skills: the model is put in a role, told the defaults it will fall into, forced to commit to variance in a pre-flight plan, and banned from the cheap moves. `gpt-taste` is the model; the standard and a worked opener are in `control/design-skill-standard.md`. |
| **No counterweight.** The engineering rules — no reviewer, no chain, no stages — were applied to design, so one route made every visual call. | Every time a second route looked, it found a real defect the maker missed: astra's QA, the copy run, the owner's pass | The design review gate, now in `ARCHITECT.md`: rendered work is reviewed by a different route before it lands; two reviewers in parallel; the maker answers in writing. |
| **The instruction became the output.** Schema field names as headings; one-line field values as sections. | 76 headings across 19 pages; "What was said" ×19 | The rule in `ARCHITECT.md` and a check that refuses it: headings name their subject, no heading repeats, prose is at least three sentences. Red now; the writer is running. |

Everything else — the diagrams, the Higgsfield graphic, the motion — follows from these.

## 2. The tools, and what each is for

| Tool | Use |
|---|---|
| **Fable 5.1** (this route) | Maker: composition, type, illustration, direct rendered refinement |
| **gpt-6-astra** | Reviewer and writer: design QA reports from tiled evidence; copy under strict grounding rules. Proven today on both. Evidence images ≤2000px on each axis; bind the workspace and digest at dispatch. |
| **GLM 5.3 Flash** | Parallel implementation and a second reviewer (composition/taste while astra takes copy). Proven on three tickets today. |
| **Higgsfield CLI + eight product skills** (installed, authenticated, 5,841 credits) | `higgsfield-generate` for the problem-panel graphic and seam textures; `higgsfield-brandkit` if the handbook wants a mark; `higgsfield-video-explainer` later for a share clip. Product skills, verbatim, never edited. |
| **gpt-taste** | The model for the skill rewrites — voice, structure, bans, pre-flight. |
| **`build/check.py` + `build/check-render.js`** | The gate's machinery: structure, links, hashes; overflow, scrollbars, reveals, and now headings and sentence counts. |
| **The design language** (`premium-tech-design-language`, its vocabulary and six references) | The scale, motifs and phrasing rules — to be rewritten role-first but not thrown away: its facts are right; its voice is wrong. |

## 3. Workstreams

### A — Make the skills (the system itself)

1. **Rewrite `ui-ux-design` first** using the worked opener in the standard: role; defaults
   to break; pre-flight `<design_plan>` with figure-per-band, focal points, headline line
   counts, one accent, meaning-carrying motion, ban sweep, and the line *no heading or
   sentence in the output is the instruction that produced it*; then the existing
   interview, routes and verification, unchanged below.
2. **Then `premium-tech-design-language`** — keep every measured value and motif, replace
   the opening with the role and the defaults, and turn the motifs into the *menu* the
   pre-flight chooses from. Resolve the five doctrine conflicts (below) inside it.
3. **Then `design-review`** — its findings must name the default the maker fell into, not
   only the deviation from a token.
4. Then `design-implementation`, `interaction-design`, `design-system`,
   `design-exploration`, `conversion-layout`, `explainer`, `prototype`,
   `design-language-transfer`. `codebase-design` is not visual and stays.
5. **Amend `precise`**: it governs facts and reports, never the register of a creative
   method. One sentence.
6. **Governance.** Each is a publisher core skill at the 50 cap: replacement in place,
   purposes unchanged so no review is triggered, authoring evidence per skill through
   `skill-publish`. Eleven publications. Fable writes; astra reviews each body against
   gpt-taste before publication (does it put the model in a role? does it name defaults?
   does it force variance?).

### B — Prove it on the handbook

The handbook is the proving ground: every change below runs through the gate.

1. **Idea pages** (in flight). Astra is writing the 76 sections under grounding rules. On
   delivery: a GLM reviewer checks every section against `video-tips.json` and
   `video-research.md` for invented claims in parallel with my integration; `check.py`
   must go green; two pages rendered and read by the owner.
2. **Investigation diagrams.** Redraw the three as drawings *of the finding*, with mono
   captions inside the artwork: T3/Melee — main line, fork, `13 PRs`, `VERIFIER ✓`; Course
   Video Manager — `GLOSSARY`, `ONE TRANSPORT`, `RESUMABLE`; Boris — the staged compiler
   with five validation layers named. Maker Fable; rendered review by astra at 640px
   before commit; the review must be able to say what each drawing shows without the text.
3. **Home page composition pass**, now under the rewritten `ui-ux-design`: a pre-flight
   plan naming a distinct figure per band, a focal point per band, headline line counts;
   then build; then two reviewers in parallel (GLM on composition, astra on copy); then the
   maker's written answer to every finding; then the owner.
4. **The Higgsfield graphic.** Through `higgsfield-generate`, GPT Image 2.5: three prompts
   × two variants for the problem-panel figure, and the seam strips; transparency measured
   in PIL, luminance-keyed if opaque, under 150 KB shipped; placed behind the rows at
   0.18–0.28 opacity or as a third column at 1200px+. The design language's line against
   generated raster is reversed by the owner and recorded when the asset lands.
5. **Motion.** The typed prompt, the drafting trace, the reveals and seams exist. The
   rewritten skill decides whether a pinned, scrubbed study earns the 44 KB of GSAP; if it
   does, one, on the investigations page.
6. **Headings that read right alone** (owner, 2026-09-10: "Repeated fixes spend tokens"
   read alone means the reverse of its section). Rule in `ARCHITECT.md`: a heading states
   the section's claim in a plain-verb clause, up to eight words; instruct for a claim,
   never for a subject. Done for the 76 idea headings (astra rewrite, 72 changed,
   `control/reviews/headings.md`). The eval: a different route reads the headings
   with bodies withheld and writes what each must claim; mismatches are rewritten before
   the page lands. Applies to every heading the site writes from here on, including B3.
7. **Front-facing copy carries no jargon** (owner: "understand exactly what we're saying in
   under 5 seconds from any viewpoint"). Rule in `ARCHITECT.md`; `check-render.js` flags
   code spans, hashes and file paths in leads, band heads, tiles, shelves, studies and
   tiers. Green after the two guide shelves were rewritten in words.
8. **Composition patterns from the references** (owner: "scan those examples and find
   mechanical patterns that break the AI out of the slop"). Delivered:
   `control/patterns.md` — 29 patterns from two parallel astra scans of the six
   references, each with the mechanism, the default it breaks, a checkable property and
   its transfer to the handbook. Both scans' first picks converge on the same move: give
   the content families genuinely different widths and reading axes (contracted reading
   lane, change the reading axis, change column count, ragged directories) instead of one
   card grid dressed six ways. These are the input to B3 and to the A-series skill
   rewrites; nothing from them is applied yet.
9. **Repeated headings elsewhere.** Guides share "When to apply / Implementation /
   Acceptance / Failure modes and maintenance"; skills share five section names. Those are
   document templates the owner chose, not copied instructions — but the rule is the rule.
   Decision needed (§6); the check covers idea pages until then.

### C — The gate as machinery, not a memo

**Execution shape (adopted from `long-running-harness`, 2026-09-10).** The plan runs as a
finite ticket graph in the existing runtime — `tickets-prepare` from astra's `TICKETS.md`
turned into a recipe, `tickets-start`, `tickets-inspect` — bound to the immutable release
path at start, so a moved `current` no longer breaks a dispatch. Every visual ticket
declares, before dispatch: `acceptance.checks` = the JSON report from
`build/check-report.cjs` (structure, rendered, headings, sentences, scroll, reveal) bound
to the exact delivered bytes; and `acceptance.qualityReceipt` = the host-authored craft
receipt written only after a different route's rendered review, with the reviewer's
report path in its `reason`. That is the design gate expressed in the harness's own
terms: not a reviewer chain, a declared acceptance target that checks alone cannot
establish. A repair ticket carries the render, the finding and the maker's answer. The
controlled comparison runs as an experiment loop: metric = defaults fallen into per blind
review; baseline = no skill; stop when the rewritten skills beat both conditions on both
makers or fail to. Non-blocking decisions batch at closeout; silence authorizes nothing.

1. A **design-review capsule template**: reviewer route, `design-review` in role-first form,
   evidence directory of tiles ≤2000px, the design language, the maker's pre-flight plan,
   the report format (page@width, what, evidence, rule, proposed fix). Astra and GLM run it
   in parallel from the same inputs.
2. **The maker's answer file** next to the report: applied / overruled with reason, per
   finding. `control/reviews/design-qa.md` is the first one.
3. **`check-render.js` grows** to catch what reviewers found today so it cannot come back:
   headline line count ≤3 at 390 and 1440; no article heading repeated across pages; no
   scroll capture over horizontal regions; balanced last lines. `check.sh` is the gate.
4. **A controlled comparison**, because the owner asked whether no skill would do better:
   the same brief (one new page for the handbook) built three ways by GLM — no skill,
   the current skills, the rewritten skills — and by Fable the same three ways; six
   renders reviewed blind by astra against the design language. Whichever wins, we know.
   This runs as soon as A1 and A2 exist.

### D — The runtime

1. Apply the product-skills patch, run the preparer, publish, switch — the steps in
   `control/runtime/product-skills/README.md`. Then the Higgsfield skills are governed,
   verbatim, and delivered to workers.
2. Readopt `copy` whole: authoring run for evidence, then `skill-publish`.
3. Commit or ignore `.agents/`, `.claude/`, `skills-lock.json` in this repo.

## 4. Sequence and parallelism

```
now      B1 writer (astra) ──────────► B1 review (GLM) ∥ integrate (Fable) ──► green
         A1 ui-ux-design rewrite (Fable) ──► A1 review (astra) ──► publish
         B2 diagrams (Fable) ──► rendered review (astra) ──► commit
then     A2 design-language rewrite ──► review ──► publish
         C4 controlled comparison (GLM ×3 ∥ Fable ×3) ──► blind review (astra)
then     B3 home pass under the new skill ──► GLM ∥ astra reviews ──► answers ──► owner
         B4 Higgsfield graphic ∥ B5 motion decision
         A3–A4 remaining skills, two at a time, each reviewed
         D1–D3 runtime, when the other session's tree is clear
```

Nothing in a row above waits on the row below. Everything visual passes the gate.

## 5. What "going" means — acceptance

- A new page built by a GLM worker from the rewritten skills alone passes two-route review
  with no high finding and no reviewer verdict of "looks like every AI site."
- The handbook home page passes the same, and the owner's own QA pass finds nothing on the
  list from today.
- `check.sh` green: structure, rendered, headings, sentences, scroll, jargon.
- Every new heading passes the heading-only read by a different route.
- The skill question is answered by evidence, not assertion: `control/skill-evals.md` carries the run records and the C4 result.
- The controlled comparison shows the rewritten skills beating no-skill and current-skill
  output on the blind review; if they do not, the skills are wrong and we say so.
- The owner would send the link to Theo, Matt Pocock and Boris Cherny.

## 6. Decisions the owner makes

1. The worked opener's voice — approve, or mark what to change, before it goes across eleven.
2. The five doctrine conflicts between gpt-taste and the design language (numbered
   markers only where the number is data; motion rule not library; spacing principle not
   values; no font blacklist; no stock photography) — confirm or change.
3. Guides' and skills' shared section headings: keep as document templates, or rewrite.
4. Go on the runtime work (D1) and the `copy` authoring run (D2).
5. The Higgsfield placement once the first set renders.
6. **Final-review route for the Chart corrections.** The owner asked for an Opus subagent; no
   Opus route exists in the fleet and native subagents are disabled. The review is running on
   gpt-6-astra as the different route. Add an Opus route and rerun, or accept astra's review.
7. **Publish the corrected Charts.** Two GLM workers' corrections land as proposals; they reach
   workers only through `skill-publish` into a new release. Go, or hold.
8. **Pilot First: combination or distinct Chart.** Core is at its cap of 50. The proposal folds
   the method into `long-running-harness` at the point of dispatch. A distinct Chart means
   naming the Core skill it replaces.
9. **The domain.** `agent-engineering-handbook.dev` is the site address in every page now;
   attaching it to the Vercel project and deploying is a production change awaiting go.

## 7. Risks, named

- **The maker's taste is the ceiling.** The gate is the counterweight; without it this plan
  reproduces today. Do not let the gate lapse for speed.
- **Rewritten skills could be worse.** That is what the controlled comparison is for.
- **Governance cost.** Eleven publications with authoring evidence is real work; it is
  also the only path that keeps the skills selected and delivered to workers.
- **Moving releases.** `current` moved four times today; every dispatch binds at launch.
