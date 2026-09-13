# Repository examples: shared vocabulary, transport and guarantees

All links point at pinned commits captured during the original investigation
recorded in the handbook's inspection reports. Unless noted, sources were
**inspected and read, not executed** by this edition.

## Video evidence

- Type-safe composition across database tooling, RPC and typed UI calls:
  described at [~13:49–14:17](https://www.youtube.com/watch?v=xmGY276gEFY&t=829s)
  with Prisma and tRPC as the speaker's examples. The video recounts the
  speaker's experience of that composition; it does not show a live
  implementation being built, so no code behavior is claimed from it. Treat
  framework choices as examples, not requirements.

## T3 Code (`pingdotgg/t3code`, snapshot `6c583620ff7ad3235b135af7107c0543467eecfa`)

- [packages/contracts/src/rpc.ts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/packages/contracts/src/rpc.ts)
  and [docs/internals/overview.md](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/docs/internals/overview.md):
  server-owned workspace files, Git, terminals and provider processes, reached
  by web, desktop and mobile clients through authenticated RPC. The overview
  keeps authentication and per-method authorization as distinct concerns —
  the shared contract carries neither by itself. Inspected, not executed.
- Acknowledgement versus completion:
  [OrchestrationEngine.ts](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/apps/server/src/orchestration/Layers/OrchestrationEngine.ts)
  commits the command receipt in one transaction with events and projections;
  a receipt proves recorded intent, not finished work. Relevant when a
  contract's success value is read as "done". Inspected, not executed.
- Documentation can disagree with the code:
  [PR #137](https://github.com/pingdotgg/t3code/pull/137) (merged March 2)
  corrected root instructions that named the wrong schema/validation layer.
  Read the executable contract, not the prose about it.

## Course Video Manager (`mattpocock/course-video-manager`, snapshot `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`)

- **One vocabulary**: [CONTEXT.md](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/CONTEXT.md)
  defines domain nouns (Course, Course Version, Section, Lesson, Video, Clip,
  Beat, Pitch, Deliverable, Publish, Bundle, Exported Video, Export Hash,
  Byte Hash, Schema Version, Remote Box), their relationships and terms to
  avoid. A Lesson and a Section are two nouns but deliberately one service
  (`LessonSectionOperationsService`) — keep such mappings stable rather than
  inventing synonyms.
- **Durable decisions vs transient code**: [ADR 0025](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0025-local-remote-split-one-http-transport.md)
  (one HTTP transport for every caller including the author's CLI; the
  accepted cost is that the CLI stops working when the deployed app is down),
  [ADR 0026](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0026-migrations-applied-by-hand.md)
  (migrations additive-only, applied by hand — it supersedes one line of ADR
  0025 only), ADR 0027 (byte hash decides the send). Note the recorded
  follow-up: PR #1550 removed automatic migrations from preview builds after
  the split, while some prose still described deploy-owned migrations —
  consult the later decision and executable configuration, not the older
  description.
- **Derived client, typed errors**:
  [rpc-layer.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/rpc-layer.ts)
  derives endpoints from the remote route type and checks implementations
  against domain service signatures, so a renamed route is a compile error
  rather than a 404 nobody sees.
  [local-only.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/local-only.ts)
  refuses machine-bound commands first, before argument validation or any
  write, with a reason an agent can report and stop on; its own docstrings
  state the two properties (names the reason, runs first). The source's own
  caution, preserved: the environment flag is an **environment suitability
  signal, not a security boundary**, and it is not an unforgeable constraint
  on an untrusted process.
- **Static rules are not sandboxes**:
  [packages/core/.dependency-cruiser.cjs](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/packages/core/.dependency-cruiser.cjs)
  rejects enumerated filesystem-bound imports, imports back into applications
  and cycles — a real, enforced build failure for the listed modules, and
  not a process sandbox or proof against every indirect runtime capability.
- **Evidence limits, preserved**: [PR #1591](https://github.com/mattpocock/course-video-manager/pull/1591)
  was **open, not merged** at the snapshot — do not describe its glossary
  cleanup as landed. [PR #1601](https://github.com/mattpocock/course-video-manager/pull/1601)
  omitted `.github/workflows/test.yml` and the file is absent at this
  snapshot, so full CI coverage is not established. Guide 11's described test
  behavior (transport tests as `fetch` handlers asserting authentication,
  expiry, the version gate and error mapping) is read from source and ADR
  prose; the suites were not executed here.

These sources are cited as research evidence; nothing from the repositories
is bundled here, and the cited authors neither endorsed nor reviewed this
skill.
