# How to keep one domain language and one transport when an agent calls your API

**Document type:** How-to. **Reader:** you are adding a command, route or agent
verb to a codebase that already has a glossary and a deployed API, and you want
the new surface to be usable by an unattended agent without forking the language
or the transport. Source: course-video-manager snapshot `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`.

## Step 1 — Use the glossary's nouns, not your own paraphrases

Before naming anything, read the repo's `CONTEXT.md` and `docs/adr/` for the
area you are touching. Then use the terms as defined — Course, Course Version,
Section, Lesson, Video, Clip, Beat, Pitch, Deliverable, Publish, Bundle,
Exported Video, Export Hash, Byte Hash, Schema Version, Remote Box — and do not
drift into synonyms the glossary avoids. In this codebase a Lesson and a Section
are two nouns to an agent but deliberately one service
(`LessonSectionOperationsService`); keep that mapping stable in issue titles,
test names and route groups.

If the concept you need is absent from the glossary, inspect the relevant code, tests and decisions for its established meaning. Record a real gap when you find one. Ask only when a consequential ambiguity remains after that inspection. If your change contradicts an accepted ADR, surface the conflict
explicitly instead of silently overriding it.

## Step 2 — Separate durable decisions from transient implementation

An ADR is durable; the code that happens to implement it today is not. When you
write a guide, issue or agent prompt, cite the decision, not the line number:

- **Durable:** one HTTP transport for every caller including the author's
  (ADR 0025); migrations additive-only and applied by hand (ADR 0026, which
  supersedes ADR 0025's "no `db:migrate`" line only); the Byte Hash decides the
  send, the Export Hash keeps the address (ADR 0027).
- **Transient:** which package runs `db:migrate`, where a route file lives, the
  exact exit-code numbers. A reference that hard-codes a transient detail rots
  on the next refactor.

**Marked generalized:** treat every ADR this way, not just these three.

## Step 3 — Split the boundary along "needs the machine", not "is nearby"

Decide what belongs behind the API by asking what each capability physically
needs. Here the renderer, the recording studio, the Video Files and finished
videos directories, and ffmpeg cannot leave the author's machine, while every
piece of SQL can. So `packages/core` holds all data access, `apps/remote` is the
deployed transport, and `apps/local` keeps the machine-bound commands — which
are **refused** remotely, not ported.

Two cautions from this source that are easy to over-read:

- A `LocalOnly` declaration (`CVM_LOCAL_MACHINE`) is an **environment
  suitability signal**, not a security boundary. It says "this box cannot do
  this work"; it does not constrain what an untrusted process can do.
- The dependency-cruiser rule `core-is-filesystem-free` checks **enumerated
  static imports** at build time. It is a real, enforced build failure for the
  listed modules — and it is not a process sandbox. Do not describe either as
  one. *(source)*

## Step 4 — Give humans and agents the same transport

The load-bearing decision (ADR 0025): no second in-process path "just for
local use". A path used only by the author's own machine is the one least
exercised, on the machine least watched — every argument-serialization bug and
lost error tag would be found by the agent alone, at 3am. The cost is accepted:
the CLI stops working when the deployed app is down.

**Marked generalized:** if you add a second convenience transport, you are
choosing which path your agents debug alone. Prefer deriving the client from
the deployed app's types so a renamed route is a compile error rather than a
404 nobody sees *(pattern in `rpc-layer.ts`, source; the rule is generalized)*.

## Step 5 — Make the public contract typed errors plus runtime validation

Type checking is the first half of the contract only. The type system checks the client and service shapes (`satisfies RemoteService<T>` in `rpc-layer.ts`); it does not parse values at runtime. Validate untrusted boundary data separately with the actual schema. Illustrative generic contract:

```ts
// One transport, one client type derived from the deployed route table.
type Job = { id: string; state: "queued" | "complete" };
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
export interface JobService {
  getJob(id: string): Promise<Result<Job, JobError>>;
}
type JobError =
  | { _tag: "NotFound" }            // stop
  | { _tag: "NeedsMachine"; reason: string } // stop, report
  | { _tag: "VersionDrift"; expected: number; actual: number }; // fix, retry
```

Then validate anything read back from disk, a manifest or a previous release
before trusting it — the source's `isManifestVideo` and `parseDigest` treat an
unparseable or stale value as *absent* (reuse less, upload instead), never as a
crash. *(source pattern, generalized)*

Make refusals **name the reason and run first**, before argument validation or
any write, so an agent reading "this needs the finished videos directory" stops
and reports instead of retrying an `ENOENT` it cannot fix. Distinct failure
classes that map to distinct actions (new credential, pull, stop) are the whole
point; in this codebase they surface as exit codes 5, 6 and 7.

## Step 6 — Test the interface, not the file count

The CLI test suites here are the transport's test suite: a Hono app is a
`fetch` handler, so tests call it with no server and no port, asserting
authentication, expiry, the version gate and error mapping as an exit code and
a line of stderr. Prefer that shape — exercising the public seam — over
splitting logic into many tiny files so each has "its own test". Deep modules
with one seam are easier to keep honest than shallow ones with many.

**Evidence limits.** We did not execute this application's tests;
the described test behavior is read from source and ADR prose. The repo's
testing docs claim exhaustive CI, but PR #1601 explicitly omitted
`.github/workflows/test.yml` and repository inspection confirmed it absent at this
snapshot — do not assert full CI coverage exists.

## Verify

Add a command end to end: route, one client line, one `satisfies` check. Then
confirm (a) a renamed route fails to compile, (b) the machine-gate refusal fires
before any write and names its reason, (c) an unparseable previous artifact
degrades to "upload" rather than a failure.

Related: PR #1591 (open, **not merged** at snapshot); #1542 + #1550 (one
transport, then fixing deploy-time migration behavior); ADRs 0025–0027.

## Sources (immutable at commit `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`)

- [ADR 0025](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0025-local-remote-split-one-http-transport.md)
- [ADR 0026](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0026-migrations-applied-by-hand.md)
- [domain doc](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/agents/domain.md)
- [machine gate](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/local-only.ts)
- [RPC layer](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/rpc-layer.ts)
- [boundary rule](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/packages/core/.dependency-cruiser.cjs)
