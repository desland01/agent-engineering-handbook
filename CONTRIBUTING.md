# Contributing

This handbook is Markdown-first: everything you read on the site is generated from
editable sources in this repository, and `public/` is committed output. To change
content, edit the source and regenerate — never edit files under `public/` by hand, since
the next render overwrites them.

```sh
# 1. Edit the source you want to change:
#    guides/*.md, *.md at the root, skills/*/SKILL.md, evidence/*.md|json

# 2. Regenerate public/:
python3 -m pip install -r build/requirements.txt   # Markdown==3.10.3
python3 build/render.py

# 3. Check links, file counts, hashes and rendered output:
python3 build/check.py

# 4. Preview before opening a pull request:
cd public && python3 -m http.server 8000    # http://localhost:8000
```

## What lives where

| Path | Role |
|---|---|
| `README.md`, `adoption.md`, `prompts.md`, `validation.md` | Reader entry points |
| `guides/` | The 13 implementation guides |
| `*-inspection.md` | The three repository investigation reports |
| `skills/` | Four portable skill directories |
| `evidence/` | Frame manifest, extracted ideas, verifier comparison |
| `screenshots/` | The 12 frames (do not replace without updating `evidence/frame-manifest.json`) |
| `examples/recurring-rule/` | Runnable lint demonstration (`npm ci --ignore-scripts && npm run demo`) |
| `build/` | Renderer, checker, pinned requirements |
| `build/assets/handbook.css` | The one stylesheet every page loads (tokens at the top) |
| `build/home.json` | Landing-page data not already in `README.md`: title, lead, source-grouped shelves, each guide's use-when line |
| `DESIGN.md`, `INTERACTIONS.md` | The design system and the behaviour specification the generated pages follow |
| `public/` | Generated site — committed, never edited by hand |

## Conventions

- Keep source-derived facts (what the video says, what a repository contains) separate
  from recommendation, and keep honest caveats: a screen shown in a video is not a live
  demonstration, and an author-reported benchmark is not a local measurement.
- Screenshots are quoted excerpts from the source video; see
  [ATTRIBUTION.md](ATTRIBUTION.md). Do not add third-party code or longer excerpts.
- New pages should be added to `RENDER_MD` in `build/render.py` and linked from
  [README.md](README.md). The landing page is built from the README's own tables and
  lists (problem table, guide list, investigations, skills, the 19 ideas) plus
  `build/home.json`; a new guide needs a shelf entry and a use-when line there, and
  `build/check.py` fails until the counts on the map match.
- Visual changes go through `build/assets/handbook.css` and are recorded in
  [DESIGN.md](DESIGN.md); behaviour changes in [INTERACTIONS.md](INTERACTIONS.md).

Vercel regenerates and checks the site from these sources on every deployment. Edit the
source, regenerate locally and commit both. `build/handbook-workflow.example.yml` provides
an optional GitHub Actions check for stale committed output; it is not installed because
the publishing token lacks GitHub workflow permission. Review changes to meaning and
source claims in the editable Markdown.
