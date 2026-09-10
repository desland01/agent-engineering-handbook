# Design skills: open with a role, break the defaults

Owner instruction, 2026-09-10: *"the precise writing for design skills is working against it
being like I want. We need to start off with 'Role' — read gpt-taste's SKILL.md because it
does a great job of breaking the AI out of boring."*

## The diagnosis, side by side

`gpt-taste` opens:

> You are an elite, award-winning frontend design engineer. Standard LLMs possess severe
> statistical biases: they generate massive 6-line wrapped headings by using narrow
> containers, leave ugly empty gaps in bento grids, use cheap meta-labels ("QUESTION 05",
> "SECTION 01"), output invisible button text, and endlessly repeat the same Left/Right
> layouts. Your goal is to aggressively break these defaults.

`ui-ux-design`, the hub of the twelve Nautilus design skills, opens:

> Make the interface fit its audience, task, content, platform, and the user's visual
> intent. Premium means coherent visual decisions, useful interactions, legible content, and
> refinement of the rendered result. … Begin each design assignment with the `/grill-me`
> intent workflow below.

Of the twelve design-family skills (`ui-ux-design`, `design-system`, `design-implementation`,
`design-review`, `design-exploration`, `interaction-design`, `conversion-layout`,
`premium-tech-design-language`, `design-language-transfer`, `explainer`, `prototype`,
`codebase-design`), exactly one — `prototype` — contains a "You are". The rest open with a
task sentence, a provenance note ("Derived from GStack … commit 0530392 … MIT license") and a
scope procedure. The first twenty lines a model reads are about lineage and process, never
about being good, never about what it will get wrong if left to itself.

**Root cause.** `precise` declares its scope as "model-facing specifications, assignments
*and reusable methods*." That last phrase pulled every skill body into the register of a
specification: neutral, hedged, procedural, evidence-first. That register is right for a
worker assignment and a QA report. It is wrong for a creative method, where the job of the
opening is to put the model in a role, name the defaults it will otherwise fall into, and
forbid them. Precision of *facts* — no invented claims, counts the page can prove, rendered
verification — is a Nautilus strength and stays. Precision of *register* is what has been
making the output careful and dull.

## What gpt-taste does that works, and what Nautilus keeps

| gpt-taste move | Effect on the model | Keep? |
|---|---|---|
| **Role in the first sentence**, second person, superlative | Sets a standard to live up to before any procedure | Yes — mandatory opener |
| **Names the default failures** ("6-line headings", "empty bento cells", "same Left/Right layout") | The model can only avoid a habit it has been told it has | Yes — every design skill lists the defaults it exists to break |
| **Forced variance** (seeded choice from menus, "forbidden from defaulting to the same UI twice") | Kills the first-option reflex | Yes, adapted — the mechanism, not the Python theatre |
| **Hard bans with judgement** ("catastrophic failure", "BANNED FOREVER") | Bans are remembered; preferences are not | Yes |
| **Menus of concrete options** (hero architectures, component arsenal) | Gives variance something to choose from | Yes |
| **Mandatory pre-flight plan** with checks before code | Verification moves before the mistake | Yes — Nautilus already has the rendered-verification half; add the pre-flight half |
| Emoji ban | — | Yes |
| GSAP mandatory, `py-32 md:py-48`, picsum stock images, "NEVER Inter", Tailwind-specific classes | Stack and taste specifics of one house style | No — a Nautilus skill states the *rule* (motion carries meaning; sections are chapters; assets are attributable) and lets the project's stack and tokens carry the values |

## The standard: what every design-family skill opens with

In this order, before any procedure, route table or provenance note:

1. **Role.** One or two sentences, second person: who the model is and what standard it is
   held to. Not "this skill supplies a vocabulary"; "you are".
2. **Defaults to break.** The specific things a model does when nobody stops it, in this
   skill's domain, named as habits: the wall-of-cards grid, the uniform section rhythm,
   the 52px icon where a drawing should carry the section, the first layout it thought of.
   Written so they are recognisable in the model's own output.
3. **Forced variance.** A mechanism that makes the model commit to a choice from a menu
   before it builds: choose one composition per band from a named list, and never the same
   one twice on a page. The commitment is written into the pre-flight plan.
4. **Bans.** Short, absolute, with the reason in six words.
5. **Menus.** The concrete options variance chooses from — motifs, compositions,
   typographic moves — each one line.
6. **Pre-flight plan.** A block the model must emit before code: the role's checks (line
   counts, empty cells, focal point per band, one accent, no banned move), plus the choices
   variance made.
7. **Then** the existing method: intent, routes, rendered verification, evidence rules,
   provenance. Nothing from the current bodies is lost; it moves below the opener.

Provenance notes move to the end of the body or to `provenance/`. A model does not need the
GStack commit hash in line four.

## Worked example — the new opener for `ui-ux-design`

```markdown
# UI/UX design

You are a senior product and brand designer whose work gets shared for how it looks, not
only for being correct. You are held to the standard of the sites in the references — the
ones people screenshot — and the finished page must read as designed, not assembled.

## The defaults you will fall into unless you stop yourself

Left alone, you produce these, every time:

- **One figure for everything.** A bordered card grid, repeated for each section, so a page
  of six different kinds of content reads as six identical grids.
- **Postage-stamp illustration.** Drawings at 24–52px in a box, when the section wants one
  drawing at a size that carries it.
- **Uniform rhythm.** Every band the same height, the same padding, a 1px rule between;
  no focal point, so the eye has nowhere to land.
- **The first layout you thought of.** Two columns, text left, image right, again.
- **Headlines that wrap into a wall.** Four to six lines of title in a narrow container.
- **Cheap labels doing the work of design.** Kickers, eyebrows and "SECTION 01" tags in
  place of hierarchy.
- **Motion as garnish.** A fade-in on everything, which is the same as motion on nothing.

## Commit before you build

Emit a `<design_plan>` before any markup. In it:

1. For each band of the page, name the **figure** it gets from the menu below, and make
   sure no two adjacent bands share one and no figure is used more than twice.
2. Name the **focal point** of each band: the one element the eye lands on, and why.
3. State the headline **line count** at the widest and narrowest target widths (2 or 3;
   4 is a failure) and the container width that guarantees it.
4. Name the **one accent** and where it appears.
5. Name the **motion** that carries meaning — a trace that draws, a row that reveals as a
   unit, a counter — and confirm everything else is still.
6. Sweep for **bans** below.

## Bans

- No eyebrow, kicker or "SECTION 01" label above a heading. Hierarchy is size and space.
- No card grid as the answer to more than two bands on one page.
- No drawing below 96px where it is the section's only visual.
- No headline over three lines at any target width.
- No drop shadow, glass or glow standing in for structure.
- No fabricated content: no invented testimonials, statistics, logos or images passed off
  as the project's own. Sample data is labelled as sample.
- No emoji in code, comments or output.

## The menu

Figures — one per band, chosen in the plan: hairline cell grid · 2×2 of tall illustrated
cells with captions inside the artwork · pipeline track with stage bars on a rail · stack
of cells under mono group labels · file cards joined by hairline wiring · horizontal row
with previous/next and a counter · drafting figure with dashed guides and `[01]` markers ·
full-viewport study with one large diagram · ledger of status rows · typed prompt.
Typographic moves — one italic accent word · a mono display headline · a claim line at
display size · balanced two-line title.
Motion that carries meaning — scroll-drawn trace · row revealed as one unit · counter ·
dithered seam · reading-progress dim.

(The intent interview, route table, implementation and verification sections follow,
unchanged from the current body.)
```

## Where the two doctrines disagree — decide these once

| gpt-taste says | The handbook's language says | Recommendation |
|---|---|---|
| Meta-labels like "SECTION 01" are banned forever | Mono `[01]`…`[19]` drafting markers and pill section markers are core motifs, used across the site built today | Keep the ban on *eyebrows and kickers* (already a Nautilus rule); keep numbered markers **only** where the number is data — an ordered set — never as decoration. Say so in the ban. |
| GSAP is mandatory; static is forbidden | Motion is hand-written at 0 KB; "at most one slow dash flow" (now superseded) | State the rule, not the library: motion must carry meaning, and a page with nothing moving is a failure; the stack decides how. |
| `py-32 md:py-48` between sections | Bands at 56px with dithered seams | The *principle* (sections as chapters, a focal point each) transfers; the values belong to the project's tokens. |
| Never Inter; Satoshi, Cabinet Grotesk, Outfit or Geist | System sans + a mono | Do not carry a font blacklist into a skill; carry "a display voice and a secondary mono voice". |
| picsum stock images with CSS filters | No photographic card art; authored drawings; attributable assets only | Keep the Nautilus rule; it is the honesty rule, not a taste rule. |

## Applying it across the twelve

Order by leverage: `ui-ux-design` (the hub) → `design-system` → `design-implementation` →
`design-review` (its findings should name defaults, not just deviations) →
`premium-tech-design-language` → `interaction-design` → `design-exploration` →
`conversion-layout` → `explainer` → `prototype` → `design-language-transfer`.
`codebase-design` is not a visual skill and is left out.

Each is a publisher Core skill, so each rewrite goes through `skill-publish` with authoring
evidence bound to the exact bytes; the purposes (frontmatter descriptions) stay unchanged so
no review is triggered by a purpose change. Core is at its 50 maximum, so these are
replacements in place, not additions.

## The one-line fix at the root

In `precise`, the scope sentence becomes: *"Use explicit scope, conditions, evidence and
outcomes in model-facing specifications, assignments and evidence reports. Design and
creative methods keep their facts precise and their **register** their own: they open with
a role and the defaults to break, not with a procedure."* Human-facing prose stays with
`simple`.


## Addendum — the instruction is not the output

A second failure mode, found on the idea pages the same day: the model copied the
*instruction* into the *work*. The extraction schema's field names became the headings on
all nineteen pages, and the one-line field values became the whole sections. The fix is a
rule and a check, not more instruction: headings name their subject; a heading that repeats
identically across pages is a label, and fails; prose sections are at least three sentences
written from the evidence. The rule is in `ARCHITECT.md` under "The instruction is not the
output". Every design and copy skill's pre-flight plan gains one line: *no heading, label or
sentence in the output is the instruction that produced it.*
