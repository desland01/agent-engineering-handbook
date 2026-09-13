# Repository examples: artifact identity, receipts and recovery

All links point at pinned commit `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`
of `mattpocock/course-video-manager`, inspected (read) during the original
investigation recorded in the handbook's inspection report. **Nothing in this
repository was executed by this edition**; behavior described below is read
from source, ADR prose and PR records at that snapshot.

- **Recipe identity vs produced bytes** —
  [ADR 0027](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0027-byte-hash-decides-the-send.md):
  the Export Hash names what the renderer was told to do (clip filenames,
  timings, order, pause, zoom, format, export version) and addresses the
  bundle; the Byte Hash, the digest of the produced video's real bytes,
  decides what is sent. The ADR records the incident it fixes: reuse keyed on
  the Export Hash copied old bytes forward, cancelled the new encode and wrote
  the old SHA256 into the new manifest, so three short exports (short by
  9.6s, 34.3s and 71.3s) shipped and one was live
  ([PR #1557](https://github.com/mattpocock/course-video-manager/pull/1557)).
  It also records why an export-generation counter was rejected: a counter
  records that somebody deleted a file; only bytes record what the file
  contains. Merged work (PRs #1564, #1501) — but described from source at the
  snapshot, not re-executed here.
- **Reuse plan** —
  [course-publish-reuse-plan.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/course-publish-reuse-plan.ts)
  and
  [course-publish-dropbox.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/course-publish-dropbox.ts):
  the plan is drawn from the previous release's committed receipt plus a
  storage listing, keyed on the byte hash; a missing, unparseable or
  archived-away receipt yields a smaller plan (everything uploads), never an
  error. The copy batch is decided once, after the export pool drains.
- **Duration completeness rule** —
  [export-duration-check.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/export-duration-check.ts):
  a pure rule refusing only a shortfall greater than one second (a tolerance
  the source chose from its own live data), always accepting overruns (that
  project's policy for its duration check, not a universal media rule), and
  refusing any file with no playable duration. Application-specific; do not
  copy the constant or the overrun policy.
- **Digest sidecar and its stated limit** —
  [export-sha256-sidecar.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/export-sha256-sidecar.ts):
  caches SHA256, content hash, size and an optional measured duration
  (`durationInSeconds: number | null` — a sidecar written before durations
  were recorded has no such field and is still treated as sound) beside the
  export.
  Its docstring argues the cache can never be stale because export names carry
  the recipe hash — but the inspection records the caveat that matters for
  recovery: the source still validates the sidecar against the file's current
  size on every read, and **replacing an artifact with different bytes of the
  same size can leave a cached digest stale**. Treat that as a documented
  limitation of the pattern: recompute or invalidate when outside
  modification is possible.
- **Produce/extract split** —
  [run-with-extraction.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-extraction.ts)
  and
  [run-with-retry.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-retry.ts),
  with tests in
  [run-with-extraction.test.ts](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-extraction.test.ts):
  the produce run carries no output schema and keeps its session id; the
  extraction pass resumes that session and retries in-context against the
  failed extraction's own session. Read honestly: the module comment says
  "extraction must not commit", but the retry wrapper spreads the produce
  options through, so the extraction run inherits the same tool options — the
  comment is intent, not a mechanical read-only boundary. The tests cover
  session preservation and failure paths; they were read, not run here.
- **CI limitation, preserved**: [PR #1601](https://github.com/mattpocock/course-video-manager/pull/1601)
  omitted `.github/workflows/test.yml` and the file is absent at this
  snapshot, so none of the above behavior is asserted as covered by CI.
  Related PRs: #1591 (**open, not merged** at the snapshot); #1542 and #1550
  (one transport, then fixing deploy-time migration behavior); #1501, #1557,
  #1564 as above.

No upload, publish or agent run from this repository was executed during the
investigation. These sources are cited as research evidence; nothing from the
repository is bundled here, and the cited author neither endorsed nor reviewed
this skill.
