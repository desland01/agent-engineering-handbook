# Are the skills being used, and are they working? — 2026-09-10

The owner's question, verbatim: "Are we actually using the skills, and are they working?
Can we share some evals if that is the case?" This note answers from run records and
review documents only. Where the honest answer is "not proven", it says so.

## 1. Used — what the run records show

Every worker run writes a `capsule_required_charts` event listing each required skill with
`available`, `invoked` and `invocationSucceeded`. Pulled from the run logs under
`~/.nautilus/releases/*/var/workspaces/handbook-20260910-workers/*/tmp-run.log`:

| Run | Route | Required skills | Delivered and invoked | Outcome |
| --- | --- | --- | --- | --- |
| astra-qa (design QA report) | gpt-6-astra | precise | invoked 1, succeeded 1 | completed, 17 requests |
| astra-copy (site copy rewrite) | gpt-6-astra | precise, simple | both invoked 1, succeeded 1 | blocked late by a permission gap after the copy was written; output kept |
| astra-copy-qa (task-file release) | gpt-6-astra | precise, simple | both invoked 1, succeeded 1 | blocked by `run_stdout_limit` (22 PNGs read at once); rerun split |
| astra-ideas (76 idea sections) | gpt-6-astra | precise, simple | both invoked 1, succeeded 1 | completed, 13 requests |
| astra-tickets (37-ticket graph) | gpt-6-astra | precise | invoked 1, succeeded 1 | completed, 7 requests |
| astra-uiux-rewrite (role-first draft) | gpt-6-astra | precise | invoked 1, succeeded 1 | completed, 11 requests |
| astra-ptdl-rewrite (role-first draft) | gpt-6-astra | precise | invoked 1, succeeded 1 | completed, 11 requests |
| astra-diagrams-r3 (rendered diagram review) | gpt-6-astra | precise | invoked 1, succeeded 1 | completed, 8 requests |
| astra-headings (76 headings rewritten) | gpt-6-astra | precise, simple | both invoked 1, succeeded 1 | completed |
| astra-patterns-a / -b (reference scans) | gpt-6-astra | precise | invoked 1, succeeded 1 | completed |
| glm-heading-reader (heading-only eval) | glm-5.3-flash | precise | invoked 1, succeeded 1 | completed |
| astra-diagrams (skill-packs-20260910c) | gpt-6-astra | precise | **available: false** | blocked, `run_observer_error` — the skill-packs releases report present Charts as unavailable |
| astra-diagrams-r2 | gpt-6-astra | (empty) | — | blocked, `capsule_declaration_invalid` — my capsule error, fixed |
| t3 / t4 / t5 (fleet MCP delegate) | glm-5.3-flash | precise | **not recorded** in the delegate output I kept | delivered their outputs; skill invocation for these three is unproven |

So: on the working release lines (`browser-route-20260910`, `task-file-20260910`,
`premium-tech-design-20260910b`) every required skill was delivered and invoked once,
successfully, in every completed run. The skill-packs line does not deliver skills at all;
nothing from it was accepted.

At the parent (this session, Fable): `design:ux-copy`, `premium-tech-design-language`,
`technical-seo-aeo`, `simple`, `precise` and `long-running-harness` were invoked for the
hub redesign, the copy, the page identity work and the execution shape. The eight
Higgsfield product skills are installed and governed but have not yet produced a shipped
asset: one `gpt_image_2_5` attempt with `--background transparent` came back opaque and
was not adopted (workstream B4).

## 2. Working — the evidence per skill

"Working" here means: the output the skill was meant to shape was measured or reviewed by
someone other than its maker, and the measurement held up.

- **precise (all astra runs).** The design QA report made three findings with numbers; all
  three reproduced at the parent in headless Chrome (`.rail h2` at 29.6px; 577px and 864px
  of bordered blank in the guide shelves; a 642/115px orphaned headline) and the fourth
  item was correctly reported as *not a defect* (a 230px badge that fits at 390). Record:
  `control/reviews/design-qa.md`. The 76 idea sections were checked sentence by sentence
  (230 sentences) for names, numbers and references not in the source record: none
  invented. Record: `control/reviews/idea-pages.md`.
- **simple (copy).** The copy rewrite's before/after table is
  `control/reviews/copy-rewrite.md`; the front-facing copy now passes the jargon rule in
  `check-render.js` (no code spans, hashes or file paths in leads, band heads, tiles,
  shelves, studies, tiers) at 390 and 1440.
- **technical-seo-aeo + ux-copy (parent).** Their outputs became checks in
  `build/check.py`: description ≤175 characters, title not the site name, canonical
  all-or-nothing against `SITE_URL`, hub-next on every hub. Green on 54 pages.
- **premium-tech-design-language.** In use — the vocabulary's values are the CSS tokens
  and `check-render.js` reads computed values back (button contrast ≥4.5, single drawing
  ≥96px, no eyebrow, no enclosed blank cells). **Effect unproven.** The owner's verdict on
  the result was "the design has gone to total garbage" and "I almost wonder if running
  the design with no skill would be better." That question has a designed answer — the
  controlled comparison (plan §3 C4: the same brief built with no skill, the current
  skill and the rewritten skill, by two makers, judged blind by a fresh astra) — and
  **it has not run.** Until it does, the only honest statement is: the skill is delivered,
  invoked and its values are on the page; whether it makes pages better than no skill is
  not known.
- **The role-first rewrites (ui-ux-design, premium-tech-design-language).** Drafts exist
  (`control/proposals/`), reviewed against the standard; not published, so not yet
  delivered to any worker. Owner decision 1 in the plan.

## 3. Evals that exist today, and the one that matters

| Eval | What it measures | Result | Where |
| --- | --- | --- | --- |
| Design QA reproduction | Do a reviewer's findings hold under measurement at the parent? | 3 of 3 confirmed, 1 correctly cleared | `control/reviews/design-qa.md` |
| Idea-page grounding | Sentences with unsupported names/numbers/references | 0 of 230 | `control/reviews/idea-pages.md` |
| Diagram legibility | Can a reviewer say what each drawing shows without the prose? | per-study verdicts and maker's answers | `control/reviews/diagrams.md` |
| Rendered checks | 72 checks × 2 viewports: overflow, scrollbars, reveals, scroll capture, slop rules, jargon | PASS, and each rule was proved to bite on a known-bad page before it was trusted | `build/check-render.js`, commit messages |
| **Heading-only reading** (new today) | A different route reads the 76 headings with bodies withheld and states what each section must claim; compared with the sections | 74 clear, 2 ambiguous; 1 heading contradicted its section and was rewritten, 2 simplified; 76/76 after | `control/reviews/headings.md` |
| **Controlled comparison (C4)** | No skill vs current vs rewritten, two makers, blind review | **not run** | plan §3 C4; tickets C4a–C4h |

What can be shared now: the run-record table in §1 (raw JSON is in each `tmp-run.log`),
the four review records, and the check report (`build/check-report.cjs` emits
`{version, pass, checks, failures}`). What cannot be shared yet: any claim that the design
skills improve a page. That claim waits on C4.

## 4. Theo harness execution — September 12, 2026

Two narrow runtime corrections are now active. They are rows within T08 and T13, not completion of either whole ticket or the nineteen-ticket plan. Code was written by Opus in isolated checkouts, reviewed by Astra, checked independently, installed through the existing release API, and selected through the locked activation journal. The shared dirty source tree was not changed.

| Run | Model | Required methods observed | Measured outcome |
|---|---|---|---|
| `9216ce74-33d6-4c4a-9f8a-74b2f3381227` | claude-opus-5 | precise, tdd, code-review: each available, invoked once, invocation succeeded once | Corrected-revision resume patch; 41 requests. Independent checker reproduced the red failure, then passed 48 candidate harness tests, 43 preserved baseline harness tests and 108 capsule tests. |
| `1b36fc46-03b8-4124-9353-25794d3242de` | claude-opus-5 | precise, tdd, code-review: each available, invoked once, invocation succeeded once | Schema-owned no-deadline version capability; 85 requests. Independent checker reproduced the red failure, then passed 10 new capability tests, 48 harness tests and 122 preserved capsule tests. |
| `288a9002-b13d-4f23-ace7-2e7895263515` | glm-5.3-flash | precise: available, invoked once, invocation succeeded once; v5 skill plan reported all invoked | Real admitted no-deadline v5 worker wrote marker A; 3 requests. |
| `d1c684af-ff72-4316-a78f-168e28d9b2ec` | glm-5.3-flash | precise: available, invoked once, invocation succeeded once; v5 skill plan reported all invoked | Separate admitted v5 correction wrote marker B; 3 requests. |

The live controller then rechecked B, accepted B's actual hash, and retained the original model-attempt identity. That establishes the repaired runtime behavior through real native interfaces. It does not establish semantic application of every skill: those event records still say `application: unverified`, and there was no controlled skill/no-skill comparison.

The combined current-based build passed 48 harness tests, 132 capsule tests, typecheck and build. The active release is `/Users/thebeast/.nautilus/releases/theo-version-capabilities`, digest `d1a5d994bdfaf7ed8dde73dec09e9231f29e0bbbeac0cda165b9919231941522`. Existing Anchor and Chart bytes, including the newer role-first design Charts, were preserved. The previous `design-charts-role-first` release remains on disk.

Evidence and current continuation state: [RUN.md](file:///Users/thebeast/.nautilus/releases/gsp-app-completion-kernel-fixes/var/workspaces/theo-ideas/astra-control/RUN.md). The [live proof](file:///Users/thebeast/.nautilus/releases/gsp-app-completion-kernel-fixes/var/workspaces/theo-ideas/astra-control/live-resume-fixed/final-proof.json), [activation receipt](file:///Users/thebeast/.nautilus/releases/gsp-app-completion-kernel-fixes/var/workspaces/theo-ideas/astra-control/activation-receipt.json), and per-row reviews there bind these statements to actual artifacts and runs.

Cost and failure qualifications: a checker-startup failure was misclassified and triggered an unnecessary Opus repair, stopped with 72 requests; this is part of the effort, not hidden from the totals. Another verifier initially misread indented TAP. Both failed predecessors were retained and their criteria were not waived. A v5 live probe was refused before model execution until the actual schema/admission mismatch was fixed; it was not downgraded. Billing and a causal productivity gain from the skills were not measured.
