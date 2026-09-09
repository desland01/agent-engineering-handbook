# Attribution

The Agent Engineering Handbook is an independent public edition maintained by
**Desmond Landry ([@desland01](https://github.com/desland01))**. It is based on public
work by three engineers, with thanks — none of whom endorses this handbook or has
reviewed it:

- **Theo ([@t3dotgg](https://github.com/t3dotgg))** — the source video
  [*Claude Code's creator has some really good advice*](https://www.youtube.com/watch?v=xmGY276gEFY)
  (July 21, 2026), his [T3 Code](https://github.com/pingdotgg/t3code) repository, and his
  [Melee fork](https://github.com/t3dotgg/melee4mac).
- **Matt Pocock ([@mattpocock](https://github.com/mattpocock))** — his public
  Course Video Manager repository.
- **Boris Cherny ([@bcherny](https://github.com/bcherny))** — his public engineering
  repositories, including `json-schema-to-typescript` and the `sandbox-runtime` fork.

## Screenshots

The 12 frames under `screenshots/` are short excerpts captured from the video above and
are reproduced here for identification and commentary. They remain © Theo / their
original owners; this repository claims no license over them. The full video is not redistributed.

## Third-party code

Code this handbook links to — ESLint's `no-restricted-imports` documentation, the
inspected repositories, and every pinned commit referenced in
[validation.md](validation.md) — remains the property of its authors under their own
licenses. This repository claims no license over that work. Nothing from those
repositories is bundled here except short quoted excerpts and descriptions with links
back to their sources.

## This repository's own content

The guides, skills, examples and build tooling written for this edition are the
handbook's own text, adapted from the cited public sources and from the authors' direct
inspection of them, with source-derived facts kept separate from author recommendation.
See the provenance notes in each skill's frontmatter and
[validation.md](validation.md). The site design is this edition's own and is recorded
in [DESIGN.md](DESIGN.md); the earlier landing-page template,
`build/workflows-source.html`, is retained in this repository for reference and is no
longer used by the renderer.

The renderer depends on [Python Markdown](https://github.com/Python-Markdown/markdown)
3.10.3 (BSD license), used as an unmodified installed dependency; the lint example
depends on [ESLint](https://eslint.org/) 10.10.0 (MIT license) as pinned in its
`package.json`. Neither is redistributed in modified form.
