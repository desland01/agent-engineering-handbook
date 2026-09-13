# One shared contract prevents mismatched code

Your storage layer, your API and your interface each describe the same object slightly
differently, and every change means finding and fixing each copy. An agent makes it worse
by confidently inventing a fourth version. The answer is one authoritative contract that
every layer derives from — plus runtime validation and authorization at the boundary,
which static types cannot give you.

## What type-safe composition feels like

Theo's picture in the video is the T3 stack: Prisma turns the database into typed
functions, tRPC exposes them over an RPC layer, and type safety runs from the UI hook all
the way to the database. Theo says compositions like that used to happen once every few
years; now Theo gets them almost daily. The specifics are Theo's stack, not a requirement — the
transferable idea is single-source typed composition: if one layer produces types, make
the next layer consume them instead of re-declaring the shapes.

**Qualification:** the almost-daily cadence is anecdotal, and adopting tRPC is not the
lesson. Deriving one contract is.

## Static types, runtime validation and authorization are three different guarantees

This is where the video's argument needs the repository evidence. In T3 Code, the
[RPC contracts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/packages/contracts/src/rpc.ts)
let web, desktop and mobile clients control the same server through one typed surface, and
the architecture overview records that authentication and per-method authorization remain
distinct concerns on top of it.

In the Course Video Manager investigation, the CLI RPC layer derives its client from the
remote app's route types and checks implementations against domain service signatures —
so a renamed route is a compile error rather than a 404 an agent debugs alone. The same
codebase is explicit about the limits: the `LocalOnly` machine gate is an environment
suitability signal, not a security boundary, and the dependency rule that keeps the core
free of filesystem imports checks enumerated static imports at build time — a real,
enforced build failure that is still not a process sandbox. Token authentication and
server-side access control stay separate.

So: a valid type says nothing about whether the requester is allowed, whether the value
arriving over the network parses, or whether an old deployed client has updated. Validate
untrusted input at runtime with the real schema, and keep authorization at the server
boundary.

## Derive each consumer from one contract

1. Pick one object that crosses the application — an order, a lead, a message.
2. Trace where it is stored, transformed, returned and displayed; list every manually
   copied interface and unchecked cast.
3. Choose the authoritative contract and derive the client from it; delete the competing
   definitions for that object.
4. Add runtime validation for anything crossing the boundary, and a focused check for
   business rules the compiler cannot express.
5. Keep the domain's names: a glossary with accepted nouns stops agents from
   paraphrasing their way into a mismatch
   ([guide 11](../guides/11-domain-language-and-agent-apis.md)).

[Guide 08](../guides/08-compose-contracts.md) walks the procedure; one HTTP transport for
every caller, including the author, is ADR 0025's decision in the same repository.

## Test type drift and invalid runtime data

In an isolated copy, deliberately rename a field or route and confirm the type check names
the consumer that breaks. Restore it and confirm the legitimate path passes. Separately,
at the real server boundary, exercise an invalid-input case and an unauthorized case —
the compiler's success proves neither.

## Shared source cannot update deployed clients.

These are inspections of two codebases, not a measurement that shared contracts reduce
defect rates. For separately deployed clients, derived types cannot make an old client
update itself; use additive changes or an explicit compatibility policy.

## Sources

<span id="tip-13-type-safe-composition"></span>
**tip-13-type-safe-composition** — [13:51](https://www.youtube.com/watch?v=xmGY276gEFY&t=831s).
Theo. Compose layers so type safety runs end to end. Evidence type: Theo anecdote;
Prisma/tRPC specifics are Theo's stack, and the frequency claim is anecdotal.

Repository evidence: T3 Code
[RPC contracts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/packages/contracts/src/rpc.ts)
and [architecture overview](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/docs/internals/overview.md);
Course Video Manager [RPC layer](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/rpc-layer.ts),
[machine gate](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/local-only.ts),
[boundary rule](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/packages/core/.dependency-cruiser.cjs)
and [ADR 0025](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0025-local-remote-split-one-http-transport.md),
from the original investigations. Related:
[agent-contract-consistency skill](../skills/agent-contract-consistency/SKILL.md). Next:
[Stop getting lost in your own code](codebase-navigation.md).
