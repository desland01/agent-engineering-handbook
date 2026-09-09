# How to make pipeline artifacts reusable, resumable and honestly complete

**Document type:** How-to. **Reader:** you run a pipeline with slow, expensive
steps (encodes, uploads, agent runs) and want to reuse prior work, resume after
crashes, and never accept a truncated artifact. Source: course-video-manager
snapshot `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`.

## Step 1 — Separate the recipe hash from the actual-byte hash

When a destination must be known before rendering, separate recipe identity from output identity (ADR 0027). The **recipe hash** (here, the Export
Hash) names what the renderer was *told to do* — inputs, order, format — and is
knowable before any work starts, so it addresses the destination and lets work
overlap. The **actual-byte hash** (Byte Hash) is the digest of what was
*produced*, knowable only after the run, and is the only thing that can say
whether this run's output is byte-identical to something you already shipped.

Illustrative generic contract:

```ts
type RecipeHash = string;
type ByteHash = string;
type Address = { recipeHash: RecipeHash }; // known before the work
type Artifact = { recipeHash: RecipeHash; byteHash: ByteHash; bytes: number };
type PriorLocation = { url: string };
type ReusePlan = ReadonlyMap<ByteHash, PriorLocation>;
// In this design, address by recipe; reuse only after comparing actual bytes.
```

The source also records why an export-generation counter was rejected: a
counter records that somebody deleted a file; only the bytes record what the
file contains. *(source)* Indexing the reuse plan by byte hash additionally
means identical outputs can copy from *any* prior location, not just their own
old address.

**Reproducibility caution.** ADR 0027's measurement was short **synthetic**
footage on one machine, one ffmpeg/driver combination, including six concurrent
encodes agreeing with a serial run. That is evidence the copy saving is
plausible on that setup — **not** proof of bit-for-bit determinism across
ffmpeg or driver upgrades. Do not lift its encoder flags or concurrency as best
practice; measure your own toolchain, and re-measure after any upgrade. The
symptom of losing reproducibility is benign (a full re-upload), not a wrong
release — size your tolerance accordingly.

## Step 2 — Check duration/completeness before acceptance

Accept an artifact on measured properties, not on "the tool exited zero". In
the source, three of 93 exports were silently short (by 9.6s, 34.3s, 71.3s) and
one was live; the fix is a pure rule: compare the measured duration to the
summed clip durations, refuse only a shortfall **greater than** a tolerance (1s
there), always accept overruns, and refuse a file with no playable duration at
all. Choose your tolerance from your own product's data — do not copy 1s.

Cache the measurement so it costs once per artifact lifetime: a sidecar beside
the artifact holding the byte hash, size, and measured duration, validated
against the file's current size on every read; an unparseable sidecar or a size mismatch is treated as *absent* and re-derived. This is not a complete freshness check: replacing an artifact with different bytes of the same size can leave this cached digest stale. Invalidate it with the artifact generation, or recompute the digest when outside modifications are possible. *(source: `export-sha256-sidecar.ts`)*

## Step 3 — Give resumable work stable identities

Give resumable stages identities that survive the process. The recipe hash can locate an intended artifact, but a corrected renderer can produce different bytes at the same recipe address. Replace the artifact, its sidecar and its publication receipt consistently; the address alone cannot prove freshness.

For agent runs, capture the **session id** at each stage. The source resumes the session whose extraction failed so the correction retains that context. If the identity is missing, report the recovery limit and inspect persisted outputs before choosing an authorized restart. Do not silently repeat side effects.

## Step 4 — Snapshot immutable state before asynchronous work

Decide reuse from an immutable snapshot taken up front, never from state that
the running pipeline is mutating. The source draws its reuse plan from the
previous release's committed receipt plus a storage listing, and never from
older releases; a missing, unparseable, or archived-away receipt simply yields
a smaller plan (everything uploads), never an error. The snapshot must be taken
before the pool drains: which outputs will be copyable is unknown until each
one lands, so (a) snapshot first, (b) decide the copy batch once, at the
earliest moment the full set is known, and (c) fall back to upload if the batch
is refused.

## Step 5 — Repair output serialization separately from repeating side effects

When an agent both does side-effectful work and must emit rigid structured
output, split the phases: run the work **without** the output schema (so a
malformed JSON never aborts the work), keep its session id and its commits as
the source of truth, then resume that session with an extraction prompt and the
schema, retrying in-context against the failed extraction's own session. The intended repair changes only serialization, preserving the producer's completed work. This requires verification; the prompt alone cannot guarantee that side effects are never repeated. *(source:
`run-with-extraction.ts`, `run-with-retry.ts`)*

**Cautions the source docstrings overstate:**

- A comment saying the extraction pass does not commit is **not mechanically
  enforced**. The retry wrapper spreads the produce options through, so the
  extraction run inherits the same tool options. Advise: where the host offers
  an admitted read-only mode for receipt extraction, use it; otherwise treat
  "extraction does no work" as an invariant to verify, not a guarantee.
- Do **not** copy this repo's default retry cap (3), its fleet counts, or its
  model strings as best practices. Use actual host limits, classified failures and evidence of progress; do not introduce arbitrary counts into your own fleet.

## Verify

- Reuse: hash an actual artifact, confirm the plan matches only on the
  **actual-byte** hash, and confirm a re-run with changed inputs lands at a new
  address and uploads. Verification means comparing **actual output hashes** —
  do not blindly hash every output to prior bytes; choose checks and tolerances
  appropriate to your product.
- Truncation: feed the acceptance rule a short file and confirm refusal, an overrun and confirm the product's chosen policy, and an unreadable file and
  confirm refusal.
- Recovery: crash between produce and extract; resume must reuse the session
  and produce no duplicate commits.

Related PRs: #1591 (**open, not merged**); #1542 + #1550 (one transport, then
fixing deploy-time migration behavior); #1564 (byte hashes); #1501 (pipelined
publish); #1557 (the live truncated export). **CI limitation:** PR #1601 omitted
`.github/workflows/test.yml`; it is absent at this snapshot, so none of the
above behavior is asserted as covered by CI.

## Sources (immutable at commit `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`)

- [ADR 0027](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0027-byte-hash-decides-the-send.md)
- [reuse plan](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/course-publish-reuse-plan.ts)
- [duration rule](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/export-duration-check.ts)
- [digest sidecar](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/export-sha256-sidecar.ts)
- [produce/extract split](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-extraction.ts)
- [retry wrapper](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-retry.ts)
