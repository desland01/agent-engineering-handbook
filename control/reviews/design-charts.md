# Record — three design Charts corrected, published and selected

2026-09-12. Subject: `nautilus-core:design-implementation`, `nautilus-core:design-review`
and `nautilus-core:interaction-design`. Written after auditing the session that built the
hero, the icon set and the study diagrams, to carry what that session learned the hard way
into the methods that should have prevented it.

## What the Charts were missing

Four things, each traced to a defect that actually shipped:

1. **Figure text measured in the drawing's units instead of the reader's pixels.** A
   12.5-unit caption in a 1040-unit viewBox rendered 593px wide is 7.1px. A review flagged
   it; the fix raised the unit number to 14 (8px) and shipped. The identical fault sat in
   the phone-width rule and in all three study diagrams — 45 instances, found only when a
   rendered check was finally written.
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

## Two findings worth acting on separately

**The skill library is full.** Its limit is 2,097,152 bytes and it stood at 2,096,342 — 810
bytes of headroom, so no Core Chart could grow at all. An earlier session had already hit
this: a pending publication named `handbook-methods` sits abandoned with the same
`skill_content_library_bytes` refusal. Room was found by reclaiming 10,127 bytes of tool
leftovers — `codebase-design/SKILL.md.predesc` and `grill-with-docs/SKILL.md.pretrim`, prior
versions a local tool left inside the library, preserved in the predecessor release — and by
cutting the three new bodies from 37,927 bytes to 27,047. That leaves 121 bytes free. The
next correction to any Chart will be refused for bytes before it is refused for anything
else, and that is a decision for the owner, not a thing to work around.

**A session is bound to the release it launched in.** Activating mid-session makes every
`nautilus` command from that session refuse with `release_mismatch`, including `activate`
itself. Plan an activation as the last runtime act of a session.

One self-inflicted fault, recorded because it is easy to repeat: a worker workspace must go
in `<release-root>/var/workspaces`, beside the sealed payload, never inside
`<release-root>/release/var/`. Writing into the sealed tree changes its file map, and the
release's own CLI then refuses to start.
