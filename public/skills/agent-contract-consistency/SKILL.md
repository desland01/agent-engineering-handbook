---
name: agent-contract-consistency
description: "Keep an existing interface in agreement across its layers: trace the shared vocabulary, the authoritative schema or derived client, runtime validation of boundary data, callers of a changed route, and error behavior — catching mismatches a rename, a new field or a dropped error tag would otherwise leave behind. Use when agents repeatedly invent mismatched data shapes between storage, API and interface, when a route, field or error class changes and its consumers must be found, or when told to 'make the types agree', 'share one contract', or 'stop inventing shapes'. Not for supplying a capability no interface provides (agent-tool-adapters), placing missing project knowledge (agent-context-calibration), encoding a recurring failure as a rule (agent-feedback-engineering), or claiming that types or environment markers enforce authorization — they do not."
metadata:
  origin: "Public edition, 2026-09-12, maintained by Desmond Landry (@desland01). Method derived from public source inspection recorded in the Agent Engineering Handbook: the source video https://www.youtube.com/watch?v=xmGY276gEFY (type-safe composition segment), Theo's T3 Code RPC contracts (pinned commit 6c583620ff7ad3235b135af7107c0543467eecfa), and Matt Pocock's Course Video Manager glossary, ADRs and RPC layer (pinned commit 4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8), summarized in guides 08 and 11. Pinned links and evidence limits in references/source-patterns.md. Independent public skill; not affiliated with or endorsed by the cited authors."
---

# Contract consistency

When every layer of an application invents its own shape for the same data,
the mismatches surface at runtime, in production, found by whoever is
watching. Keep one vocabulary, one contract, and one transport — then check
the things types cannot check.

## Work from one object and one authoritative contract

Pick the single object that crosses the application — a lead, order, video,
message. Trace where it is stored, transformed, returned and displayed. Find
the manually copied interfaces and unchecked casts along that path, then
choose the **existing authoritative contract**: the external API's schema and
generated client, or the server procedure's inferred output. Derive the
client contract from it and remove the competing manual definitions. Do not
change frameworks to imitate a source example; the point is one derived
contract, whichever mechanism provides it.

## Use the project's vocabulary, not a paraphrase

Before naming anything, read the project's glossary and decision records, and
use the terms as defined — in code, issue titles, test names and route
groups. A domain may deliberately map two nouns to one service; keep that
mapping stable instead of inventing synonyms. If a concept is absent, inspect
code, tests and decisions for its established meaning; if your change
contradicts an accepted decision record, surface the conflict rather than
silently overriding it. Cite the durable decision, not the line number that
happens to implement it today.

## Separate the guarantees — this is the skill's core distinction

| Guarantee | What it actually constrains |
|---|---|
| Shared type or derived client | What the compiler accepts. A renamed route becomes a compile error instead of a 404 nobody sees. It says nothing about runtime values, deployed clients, or permissions. |
| Runtime validation | What untrusted boundary data actually contains. Parse anything read from the network, disk, a manifest or a previous release — but the failure differs by case. An invalid *request* from an untrusted caller is rejected with a typed, useful error, never silently absorbed. Corrupt *optional prior-reuse metadata* (a stale cache, an old manifest) is treated as absent and degraded, never crashed on. Required authoritative data that fails to parse is an error, not a silent fallback. |
| Authorization | What a requester may do. Lives at the server boundary. A valid type, a machine-suitability flag or a passing build is **not** a security boundary. |
| Static import or dependency rules | The enumerated imports they were configured to check. A real, enforced build failure for the listed modules — and not a process sandbox. |

Treat each source's own caution as binding: the inspected machine gate's
environment flag is an environment-suitability signal, not an unforgeable
boundary; token authentication and server-side access control remain separate
concerns. Never describe a type system, a build rule or a suitability marker
as enforcement of authorization.

## Map errors to actions

The source's one narrow pattern, kept narrow: a *known precondition or
suitability check* (there, the machine gate in `local-only.ts`) raises a
typed, named error before any write — "this needs the finished videos
directory" lets an agent stop and report, while an `ENOENT` on an unknown
path gets retried. That early-refusal rule covers known preconditions only.
Error values do not execute, so nothing "runs before" them; normal
schema-validation ordering stands — invalid arguments are refused by the
validation that checks them, as typed errors after that validation. A
precondition refusal should also not disclose resource details the caller is
not yet authorized to see. Distinct failure classes should map to distinct
next actions (supply a credential, pull data, stop and report, fix and
retry), with stable identifiers an agent can branch on.

## Verify the consistency, including the negative cases

In an isolated working copy:

1. **A renamed route or field fails to compile** in every consumer derived
   from the shared contract — that is the intended benefit, so prove it by
   deliberately breaking one thing.
2. **Invalid boundary data is rejected at runtime** by the actual schema, not
   only by the compiler.
3. **A dropped or renamed error tag is caught** — an error class a caller
   matches on is part of the contract; renaming it silently reroutes every
   error handler to its fallback.
4. **A consistent control passes**: the legitimate path, end to end, through
   the real client and server seam.
5. **Unauthorized access is still refused** — separately, at the server
   boundary, because the type system never addressed it.

For separately deployed clients, use additive changes or an explicit
compatibility policy: shared source types cannot make an old deployed client
update itself.

See [implementation.md](references/implementation.md) for worked applications
and [source-patterns.md](references/source-patterns.md) for the pinned code
and its evidence limits.

## Input / output contract

- **Input**: the interface and its consumers (storage, API, clients, agent
  callers), the change under consideration or the observed mismatch, and the
  project's glossary and decision records where they exist.
- **Output**: the reconciled contract (shared schema or derived client,
  removed duplicates), runtime validation and error mapping at the boundary,
  the evidence from the negative cases above, and an honest statement of what
  remains unenforced (deployed clients, permissions, non-enumerated imports).

## Acceptance

The mismatch you reconciled is demonstrated caught: the renamed route fails
where it should, invalid boundary data is refused, the dropped error tag is
found, and the consistent control passes through the real seam. Authorization
behavior is checked separately and reported as its own concern, never as
implied by type safety.

## Known failure cases

- Manually duplicated interfaces that drift: the copy compiles while the real
  contract moved.
- Trusting compile-time checks for runtime values, or runtime validation for
  permissions.
- Renaming an error tag or exit code that callers branch on, silently sending
  every failure to a generic handler.
- A second convenience transport "just for local use": it is the path
  exercised least and debugged alone. Prefer deriving every caller from the
  deployed contract, and accept the recorded cost (the CLI stops working when
  the service is down) explicitly.
- Describing a type, build rule or machine-suitability flag as a sandbox or
  authorization boundary.

## Do not activate when

- The missing thing is a capability no interface provides — build the adapter
  (agent-tool-adapters).
- The problem is knowledge placement or steering, not interface agreement
  (agent-context-calibration).
- The ask is a standing rule for a recurring failure (agent-feedback-engineering).
- The repo cannot run, preview or deliver evidence at all — that is workspace
  readiness (agent-ready-workspaces).
- A brand-new API is being designed from scratch with no existing contract or
  consumers to reconcile — that is ordinary design work, though the
  vocabulary and guarantee-separation sections still apply.
