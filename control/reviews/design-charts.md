# Record — three design Charts corrected, published and selected

2026-09-12. Subject: `nautilus-core:design-implementation`, `nautilus-core:design-review`
and `nautilus-core:interaction-design`. Written after auditing the session that built the
hero, the icon set and the study diagrams, to carry what that session learned the hard way
into the methods that should have prevented it.

## What the Charts were missing

Four things, each traced to a defect that actually shipped:

1. **Figure text measured in the drawing's units instead of the reader's pixels.** A
   12.5-unit caption in a 1040-unit viewBox rendered 593px wide is 7.1px. A review flagged
   it; the fix raised the caption from 11 units to 12.5 — 6.3px to 7.1px — and shipped it
   still unreadable, because the number moved in the drawing's units and nobody converted
   what the reader would get. The identical fault sat in the phone-width rule and in all
   three study diagrams — 45 instances, found only when a rendered check was finally written.
2. **Generated artwork used where authored vector was required.** Two full rounds of image
   generation, then every icon redrawn by hand. Exactly one generated asset survived into
   the site. No Chart said when to generate and when to draw.
3. **Motion with no specification.** 83 SMIL animations, every one linear or discrete, no
   easing anywhere. Separately, a figure about absence made the robot the brightest element
   and the empty chair the dimmest.
4. **Evidence that could not show what the reviewer was asked about.** Three stills two
   seconds apart from a nine-second loop, reported as a static figure.

And the structural one: the owner's 2026-09-10 standard requires every design-family Chart
to open with a second-person role, the defaults it exists to break, a forced pre-flight
commitment and short bans. The standard was written into `control/design-skill-standard.md`
and never applied to a single Chart. Wording is not enforcement — that was the point of the
standard, and it was the first thing the audit found.

## How they were changed

Through the runtime's own path, not by editing release bytes. `nautilus skill-publish`
refuses a changed Chart without a recorded authoring run whose required Charts — `precise`
and `create-skill` — were available, invoked and delivered, and whose result is an
attestation binding each body's exact bytes. Four such runs, each admitted under a version-5
capsule naming its skill plan:

| run | what it did |
|---|---|
| `fac640a2` | authored the three bodies from the audit's findings |
| `00cf42ae` | attestation in the contract's shape |
| `b90cb92c` | fitted them inside the library's byte limit |
| `9612c9f4` | restored the role sentence the byte squeeze had removed |

Every refusal along the way was a boundary working, and each was fixed in the declaration
rather than around it: a read scope outside the launch workspace, a no-deadline lifetime the
anchor does not authorize, an authoring workspace outside the runtime's worker scope, and a
library over its byte limit.

Published as `design-charts-role-first`, digest `b29d3468`, selected 2026-09-12. Counts
unchanged at 50 core / 26 domain. Readback confirms all three open with their role.

## One finding worth acting on separately

**The skill library is full.** Its limit is 2,097,152 bytes and it stood at 2,096,342 — 810
bytes of headroom, so no Core Chart could grow at all. An earlier session had already hit
this: a pending publication named `handbook-methods` sits abandoned with the same
`skill_content_library_bytes` refusal. Room was found by reclaiming 10,127 bytes of tool
leftovers — `codebase-design/SKILL.md.predesc` and `grill-with-docs/SKILL.md.pretrim`, prior
versions a local tool left inside the library, preserved in the predecessor release — and by
cutting the three new bodies from 37,927 bytes to 27,047, which left 121 bytes free. The one
correction made since — a single line, below — spent 78 of them, and **43 bytes remain**. The
next change to any Chart will be refused for bytes before it is refused for anything else,
and that is a decision for the owner, not a thing to work around.

## Never write inside the sealed payload

A worker workspace goes in `<release-root>/var/workspaces`, beside the sealed payload, never
inside `<release-root>/release/var/`. The release digest is computed over the file map of
`release/`, so adding a single file there breaks the seal and the release's own CLI refuses
to start — its launcher runs `inspect` as a self-check before every command, so the whole
runtime goes dark, `activate` included.

**Corrected 2026-09-12.** This record first read that fault as "a session is bound to the
release it launched in; activating mid-session makes every `nautilus` command refuse." That
was wrong, and it was wrong in the expensive direction: it would have had everyone schedule
activations around a constraint that does not exist. Every `release_mismatch` observed that
day came from the broken seal above. Measured afterwards from the same session that did the
activating: `nautilus inspect` answers correctly across two subsequent activations, including
against `theo-version-capabilities`, a release published after that session started. A
session is not bound to its launch release.

## What happened next

`theo-version-capabilities` was published on top of this work and selected on 2026-09-12, and
`chart-caption-corrected` after it; the chain reads `design-charts-role-first →
theo-version-capabilities → chart-caption-corrected`. `design-review` and `interaction-design`
carried through every hop byte-identical at `4ade8e44` and `3e533969`; `design-implementation`
is now `505d7198`, one line different from the `c09e3c8f` first published here. The sealed
roster records authoring evidence for all three. A rollback therefore names
`releases/chart-caption-corrected` as its expected current, and returning as far as
`skill-plan-admitted` would discard that release's work as well as these Charts.

## Corrections to this record

**2026-09-12, the fabricated caption size.** This record first said the failed fix "raised
the unit number to 14 (8px)". Nobody ever set 14. The hero review records the actual change
as 11 → 12.5 units, which is 6.3px → 7.1px at this figure's scale. The arithmetic in the
invented version was sound, which is exactly why it survived being written down: 14 units
does render at about 8px. What made it false was the attribution — a number I supplied
reading as a measurement somebody took. It reached the published `design-implementation`
body as "14 units yields about 8px, still unreadable in the reported case". Corrected there
through the same admitted path — authoring run `0a4a169f`, published as
`chart-caption-corrected`, digest `afbd3e8c`, selected 2026-09-12 — as the single changed
line in an otherwise byte-identical body, which cost 78 of the library's remaining bytes. The
true numbers make the better instruction anyway: a fix that moved a caption 1.5 units and
cleared nothing is a sharper warning than a hypothetical that was never tried.

**2026-09-12, the session-binding claim.** Recorded above under "Never write inside the
sealed payload".
