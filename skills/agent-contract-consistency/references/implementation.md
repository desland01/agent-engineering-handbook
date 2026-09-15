# Contract consistency: applying the reconciliation

The method comes from the video's type-safe composition segment, T3 Code's RPC
contracts, and Course Video Manager's glossary, ADRs and RPC layer, studied in
[guide 08](https://github.com/desland01/agent-engineering-handbook/blob/main/guides/08-compose-contracts.md)
and
[guide 11](https://github.com/desland01/agent-engineering-handbook/blob/main/guides/11-domain-language-and-agent-apis.md).
The video describes the satisfaction of composing database tooling, RPC and
typed UI calls; it does not demonstrate an implementation. The procedure is an
adaptation of what the repositories show.

## Worked case: one object traced end to end

A `Course` is stored in the database, shaped by a service, returned by the
API, and rendered by a client.

1. Trace the object's path and list every shape it takes. Flag manual
   `interface Course { ... }` copies and unchecked casts.
2. Name the authoritative contract — the server procedure's inferred output
   type, or the published schema — and derive the client from it. Delete the
   copies.
3. Decide what the public response exposes: keep private storage fields out of
   it, and define the client contract from that public response.
4. Check the vocabulary: if the glossary distinguishes `Course` from
   `CourseVersion`, a field named `course` holding a version id is a
   vocabulary bug, not a naming preference.
5. Validate at the boundary: parse the request body with the actual schema at
   runtime and reject an invalid request with a useful typed error. For
   *optional prior-reuse metadata* (an old manifest, a stale cache), treat an
   unparseable value as absent and degrade to the safe path (re-upload what
   the machine already holds) rather than crash. Required authoritative data
   that fails to parse is an error, not a silent fallback.

## Worked case: the rename that must be caught

The public field `displayName` becomes `name`.

- Compile time: with a derived client, every consumer reading `displayName`
  fails to compile. Prove it in an isolated working copy: make the change,
  run the existing type check, confirm it names the consumer needing update,
  then complete or revert deliberately.
- Runtime: stale deployed clients still send or expect the old field. Shared
  source types cannot update them — so use an additive change or a stated
  compatibility policy, and validate incoming data at the boundary either way.
- Errors: if an error tag `NotFound` becomes `Missing`, callers matching on
  the old tag fall through to their generic handler. Error names and codes
  are contract surface; change them only with the callers, and test the
  mapping.

## Worked case: what the guarantees do not do

In the inspected source project:

- The machine gate refuses local-only commands on a remote machine and names
  the reason before any read or write. This is the source's one
  known-precondition guard — a suitability refusal that runs ahead of any
  write; it is not a claim that typed errors precede validation generally.
  Useful, and its own docs' caution holds: the environment flag is a
  suitability signal, not an unforgeable boundary. Authentication and
  server-side access control are separate.
- The dependency rule rejecting filesystem-bound imports in the core package
  is an enforced build failure for the enumerated static imports — and not a
  process sandbox or protection against indirect runtime capability.
- The RPC layer derives client endpoints from the deployed route type, so a
  renamed route is a compile error; argument serialization and error tags
  still need runtime validation and tests, which the project exercises by
  calling the app as a plain `fetch` handler — the public seam, no server, no
  port.

When you report the reconciliation, keep these separations explicit: what the
type system now guarantees, what runtime validation guarantees, what the
server's authorization guarantees, and what remains unenforced.

## Verifying at the public seam

Exercise the real transport the agent or client uses: call the handler or
start the actual server, then confirm (a) the renamed route fails where it
should, (b) the machine or precondition refusal fires before any write and
names its reason without disclosing resource details the caller is not
authorized to see, (c) an unparseable *optional* cached value degrades to the
safe path while an invalid *request* is still rejected with a typed error,
and (d) an unauthorized request is refused — checked at the boundary,
not inferred from types. Prefer a few checks through the public seam over
many tests of private internals.

## Relation to the sibling skills

- If no interface provides the needed capability at all, the fix is a new
  adapter (agent-tool-adapters), not a contract change.
- If agents keep missing the glossary or decision records, the fix is placing
  the knowledge where it is read (agent-context-calibration).
- If the same mismatch has already caused repeated failures and a standing
  check is wanted, that check belongs to agent-feedback-engineering; this
  skill finds and reconciles the current mismatches.
