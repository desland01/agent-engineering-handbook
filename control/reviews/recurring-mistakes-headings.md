# You turn repeated mistakes into reliable checks: heading-reader review

Date: 2026-09-13. Subject: `lessons/recurring-mistakes.html`. Reviewer route: glm-5.3-flash, headings read with bodies withheld first (expectations.md in the reviewer workspace), then compared. Maker: Fable 5.1 coordinating gpt-5.6-sol writer output.

| Heading | Expectation | Actual claim | Verdict | Proposed | Maker answer |
|---|---|---|---|---|---|
| Observed failures define useful checks | Build checks from observed mistakes, not imagined ones | Same | MATCH | — | no change needed |
| Repeated comments should become executable rules | Repeated corrections become automated checks | Same | MATCH | — | no change needed |
| The check must permit valid work | The rule must not block legitimate work | Same; block only when boundary and remedy are certain, otherwise warn | MATCH | — | no change needed |
| A small import rule proves the boundary | A concrete import-rule example proves the boundary | Same (worked ESLint exercise: forbidden import rejected, approved import passes) | MATCH | — | no change needed |
| Ordinary validation keeps protection active | Run the check in normal validation so it doesn't decay | Same | MATCH | — | no change needed |
| Every check needs limits and upkeep | Checks need scope limits and maintenance | Same | MATCH | — | no change needed |
| Sources support evidence-led automation | Sources back evidence-driven automation | Same, with qualifications | MATCH | — | no change needed |

Notes: opening paragraph states outcomes. Template-label / rendering defects: the worked example's shell block is emitted as literal ```sh fence markers and heredoc lines inside `<p>` elements, i.e. raw markdown presented as body prose rather than a formatted code block. The glob patterns are corrupted by markdown-emphasis rendering: `src/ui/*<em>/</em>.js`, `node_modules/<strong>`, `"src/ui/<strong>/<em>.js"`, `"</em><em>/db"` — the example is not reproducible as rendered. Tool internals front-facing: a pinned dependency version (`eslint@10.10.0`) and generated filenames (`eslint.config.red.js`, `eslint.config.js`) appear in body prose; the pin is defensible for reproducibility, the corrupted globs are not. No hashes.

Maker answers to the notes: links to sibling Markdown sources and any raw code fence come from the phase-four preview converter, not the site renderer; phase five renders with the real build and re-checks both before the page lands. The imperative title on the instructions lesson was replaced with the plan's title.
