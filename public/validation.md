# Validation and provenance

Research performed September 9, 2026. This page identifies what was actually checked and
where an implementation claim remains limited.

## Sources and collection

The source video is [xmGY276gEFY](https://www.youtube.com/watch?v=xmGY276gEFY), titled
*Claude Code's creator has some really good advice*, published July 21, 2026 by Theo. Its
duration is approximately 19 minutes 12 seconds. The complete captions were read; useful
ideas were extracted and reconciled against timestamps and visible frames. Segment
boundaries are approximate caption timestamps, not frame-accurate edit points.

The downloaded 1920×1080 video has SHA-256
`d81e3d3c29a6e02c9798e6fe37d362589e00d72ee4dcb95ab624f43e1a400944`. The video itself is
not redistributed in this repository.

For each frame, ffmpeg performed a timestamp seek and exported one JPEG:

```bash
ffmpeg -hide_banner -loglevel error -ss 383 \
  -i source/xmGY276gEFY.mp4 \
  -frames:v 1 -q:v 2 screenshots/06-23-upload-skill.jpg
```

(Paths above are relative; the extraction used a local copy of the video retained outside
this repository.) All 12 frames were visually inspected at full resolution. [The frame
manifest](evidence/frame-manifest.json) records each command, timestamp, output hash and
observation. The upload-skill screen at 06:23 is visible evidence of instructions, not
proof that an upload succeeded.

## Repository snapshots

| Source | Inspected revision | Scope |
|---|---|---|
| T3 Code | `6c583620ff7ad3235b135af7107c0543467eecfa` | Selected architecture, custom rules, launcher, tool adapters and PR evidence |
| T3 Code at end of publication day | `23c18fda7a969634a30888e36b2da45f6d66a83b` | Historical instruction, lint and test configuration comparison |
| Theo's Melee fork | `a276aeb70f9879204d891d967f1c9442523568e1` | Fork comparison, all 13 PR records, selected tools/native architecture and verifier execution |
| Original Melee verifier | `035d9711623a32fbe891cffdcf44a91a550c1947` | Exact linked commit and its nine verifier tests |
| Matt's Course Video Manager | `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8` | Latest 100 PR records, selected diffs and source; no application execution |
| Boris's json-schema-to-typescript | `5caacfc53671f9c891bb4e2a78bccc6190ed3ef4` | Compiler stages, validation, benchmarks, CI and selected PRs; no compiler test execution |

Moving PR/branch pages can change after this snapshot. Large PR file lists can be paginated
or truncated; the reports do not claim complete line-by-line review of every change. PR
performance figures remain author-reported measurements.

## Executed behavioral checks

**Lint demonstration.** Node 22.22.3, ESLint 10.10.0. `npm run demo` succeeded after
installing the lockfile dependencies. Without the restriction, the offending import passes
with exit 0. With it, ESLint exits 1 and reports exactly the forbidden UI-to-database
import; the approved API import produces no finding. The driver treats an execution/config
error as failure. [Red evidence](examples/recurring-rule/evidence/red.txt), [green
evidence](examples/recurring-rule/evidence/green.txt),
[reproduction instructions](examples/recurring-rule/README.md).

**Melee verifier.** `python3 -m unittest discover -s tools/tests -p test_verify.py -v`
passed at the original verifier snapshot (9 tests) and current fork (15 tests). A separate
fixture gave both verifiers matching synthetic bytes and successful mocked build/diff
commands, but incomplete source metrics. The initial version accepted it; the current
version rejected it. [Comparison result](evidence/melee-verifier-comparison.json).

The Melee build/diff subprocesses were mocked. No Nintendo assets were downloaded and no
game, native renderer or performance benchmark was executed. These results establish
verifier behavior only. The public applications, upload service and any private agent
systems were not executed.

## Static package checks

The final edition checks, run locally against this repository:

- All Markdown links and image targets inside the rendered pages resolve to files that
  exist; no link escapes the repository or, in `public/`, the generated root.
- Exactly 13 guide pages, 4 skill entrypoints and 12 full-size frames are present, with
  all screenshot SHA-256 hashes matching the extraction manifest.
- The renderer (`build/render.py`, Markdown pinned to 3.10.3 in
  `build/requirements.txt`) runs without network access and
  produces byte-identical `public/` output on a second run (checked by directory
  checksum before and after).
- The four `SKILL.md` files have valid Agent Skills frontmatter, and the
  `agents/openai.yaml` files parse with a display name, short description and a default
  prompt that references their own `$skill-name`.

These are repository and renderer checks, not tests of the inspected third-party
applications. See [CONTRIBUTING.md](CONTRIBUTING.md) to rerun them.

## What is not claimed

- No full transcript or copy of the video is redistributed, and no third-party repository
  is cloned into this repository.
- No deployed site, service or upload was exercised. The expected public URLs are recorded
  in the delivery notes only until confirmed.
- Sponsor claims and universal career/productivity claims remain unverified.
- Qualifications in the guides (for example, that a skill shown on screen does not prove a
  real upload succeeded) are carried through to the [detailed
  extraction](evidence/video-research.md) and the structured
  [ideas file](evidence/video-tips.json).
