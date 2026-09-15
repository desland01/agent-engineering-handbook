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

The combined current-based build passed 48 harness tests, 132 capsule tests, typecheck and build. The release selected at that activation was `/Users/thebeast/.nautilus/releases/theo-version-capabilities`, digest `d1a5d994bdfaf7ed8dde73dec09e9231f29e0bbbeac0cda165b9919231941522`. Existing Anchor and Chart bytes, including the newer role-first design Charts, were preserved. The previous `design-charts-role-first` release remains on disk.

Evidence and current continuation state: [RUN.md](file:///Users/thebeast/.nautilus/releases/gsp-app-completion-kernel-fixes/var/workspaces/theo-ideas/astra-control/RUN.md). The [live proof](file:///Users/thebeast/.nautilus/releases/gsp-app-completion-kernel-fixes/var/workspaces/theo-ideas/astra-control/live-resume-fixed/final-proof.json), [activation receipt](file:///Users/thebeast/.nautilus/releases/gsp-app-completion-kernel-fixes/var/workspaces/theo-ideas/astra-control/activation-receipt.json), and per-row reviews there bind these statements to actual artifacts and runs.

Cost and failure qualifications: a checker-startup failure was misclassified and triggered an unnecessary Opus repair, stopped with 72 requests; this is part of the effort, not hidden from the totals. Another verifier initially misread indented TAP. Both failed predecessors were retained and their criteria were not waived. A v5 live probe was refused before model execution until the actual schema/admission mismatch was fixed; it was not downgraded. Billing and a causal productivity gain from the skills were not measured.

## 5. Passing unit tests did not establish the live journey

At the first two-draft checkpoint, neither T02 source draft was accepted. The first Opus run used 151 model requests. Its repair used 204. Those 355 requests include code and correction effort, not the separate source audits or this reviewer's work. No live journey from the new runner had been accepted at that point; the later result is recorded below.

The first independent check passed 72 new tests and the unchanged 48-test harness and 132-test capsule suites. Source review still found a checker that could not be admitted, permissive defaults for malformed templates, and byte checks that accepted extra whitespace. A separate admitted command reproduced those defects without model calls. The repaired draft passed 134 new tests and the same preserved suites, but its admission classification and several failure/resume branches still contradicted the task. A narrowly scoped follow-up is now assigned; its results are not yet evidence.

For repair run `65f8c7a2-83da-43a9-87f0-48d95915a4d5`, the records show precise, tdd and code-review available, invoked once and invocation succeeded once. The native body channel reports normalized equivalence; the raw summary also retains its `skillBody: mismatch` field. Semantic application remains `unverified`. Invocation and self-review therefore do not establish that the result meets its contract.

Two setup refusals cost no model requests: a direct checker-workspace input was removed after preparation refused it, and a used checkout exceeded the unchanged 5,000-entry scope-scan bound. The latter also reported input verification false even though all declared hashes matched, because input reads were refused after the scope failure. The old checkouts, drafts and logs were retained. Fresh checkouts carried the complete same source baseline and delivered patches; no allowance, validator or acceptance requirement was weakened.

The four supporting source audits were accepted only after source reconciliation. Their eight initial/correction GLM runs used 90 model requests. Neither that activity nor the code drafts establish a measured speedup, billing result or causal benefit from the skills.

Evidence: the existing [execution record](file:///Users/thebeast/.nautilus/releases/gsp-app-completion-kernel-fixes/var/workspaces/theo-ideas/astra-control/RUN.md), its `t02-runtime-suite/REVIEW.md`, `t02-runtime-repair/REVIEW.md`, reproduction reports and native run records. A later selection check found the earlier T08/T13 source files, compiled CLI and Anchor byte-identical in the then-selected `design-charts-normative` release; `selection-after-t02-repair.json` records that observation. It is not a new activation by this execution.

### The source runner later passed real normal and negative checks

T02 source-stage acceptance now has real evidence. A further state-flow repair used 147 Opus requests. A small task-generation correction used 73. Total completed coding effort reached 575 requests before distribution work. The first live normal attempt used 2 GLM requests and failed: it wrote the marker but never invoked its declared skill. The runtime blocked it, and the failure was retained. The correction told the worker to invoke its existing ordered skill plan; no capsule version, skill obligation or limit was weakened.

The corrected normal run (`e42836bd-ebae-4bb9-b13a-913681f5809a`) completed with 3 GLM requests, invoked precise, and delivered the exact marker. Its zero-model controller checker passed and the real ticket was accepted. The deliberate missing-output run (`9e00b5bb-e586-4375-a1bc-130cc1fc54ca`) completed with 2 GLM requests and the same skill invocation, but created no marker. The runtime and runner reported `missing_declared_output`, with no checker started without the artifact and no receipt. That is the intended negative-test result, not an accepted broken ticket.

The source-stage plan is accepted after independent checks of 154 offline tests, the unchanged 48/132 suites, exact artifact identity, source review and both real journeys. Source runner SHA256: `c2781387a732d96578e1c60395d57620c90b10de2dd992f24d864ba7ca40bb6f`. Evidence: `t02-runtime-final/live-proof.json`, `REVIEW.md`, `quality.json` and `accepted-inspection.json` under the execution record's control directory.

At that source-stage checkpoint, distribution and journaled installation were outstanding. The later distribution result is recorded below. The separate two-browser handbook journey remains undelivered. These results establish the particular runtime test, not skill causality or lower cost.

### Distribution accepted; installed live verification underway

The packaging authoring run `8a6e5bec-bb69-437a-ba54-4ddd53d5f608` used 88 Opus requests. The authored build tests start no model. Independent checks passed the real package build, manifest coverage, a standalone copy without source or dependencies, and all preserved tests. Source acceptance was re-read from the original controller after the corrected report received a fresh checker. Evidence: `t02-distribution/accepted-inspection.json`.

A separate current-based integration run `884c1999-7de0-437d-8698-ac3c6ab1669a` completed with zero model requests. It passed 5 build tests, 154 journey tests, 48 harness tests, 132 capsule tests, typecheck and build on Node v22.22.3. The existing release APIs installed an inactive candidate at `/Users/thebeast/.nautilus/releases/theo-host-worker-journey`. Its installed live proof and activation are not yet established at this update. Exact provenance and installation evidence: `t02-installation/` in the same control directory.

### Installed runtime journey delivered

The inactive candidate subsequently passed both real installed journeys and was selected through the existing activation journal. Normal worker `8f9f15e5-8e94-4652-8e11-461eeda7cce7` used 3 GLM requests. The deliberate missing-output worker `e52f9c82-84e5-41ee-939f-d607f33e06bf` used 2. Both invoked precise and passed admission. The normal ticket was accepted with exact marker bytes. The negative ticket remained blocked for missing delivery, as intended, without a checker or receipt. Skill application still reports unverified.

Evidence: `t02-installation/live-proof.json` and `activation.json`. Selected digest at activation: `58c8652063a1dfcc26e5be24e881b3579fcc9f979b3c609c34a88b8e25b5e17b`. Active readback passed. The prior `design-charts-complete` release, its source and Charts were preserved. The separate handbook browser journey remains open.

A host verifier initially looked for an optional evidence filename that did not exist. Its correction read the actual saved first CLI inspection, with the same assertions. Neither a live rerun nor a product edit was required. That setup failure is retained alongside the successful proof.

### Schema draft still needs repairs

The separate schema-generation draft used 105 Opus requests and corrected a real public TypeScript gap. Two new tests failed in the independent source archive because they read the mutable Git index. Review also found unsafe generator destinations and inconsistencies between schema descriptions, types and reference text. A generic repair was interrupted after 24 requests. The specifically reviewed repair ended after 32 requests when authentication expired. Requests 22–32 returned HTTP 401. This is a route blocker, not a new product-test failure or accepted schema change. Partial edits are preserved at `t13-schema-work/auth-expired-partial/`.

These totals include failed work and repair effort. No controlled comparison establishes skill causality, reduced cost or a speedup. Billing remains unmeasured.

## 6. Transport and triage legwork needed source correction

The T05 transport report used 9 GLM requests, followed by 6 for a specific correction. The first draft recommended accepting gaps in the required upload-only credential restriction. It also inferred credential properties from environment-variable names and media-upload support from a JSON PUT interface. Source review caught those mistakes. The corrected report received final factual prose corrections from Astra, then fresh current-byte checking through the original controller. Its acceptance proves a reviewed inventory and unresolved decision, not an approved transport or upload capability. Both worker drafts are retained under `wave-b-legwork/t05-transport/`.

The T10 first triage draft used 17 GLM requests. Its delivered file passed the delivery check, but source review blocked it for incorrect grouping, unsupported cause/fixture claims and wrong duration statements. Independent arithmetic verified 27 reason groups covering 462 blocked records. That count does not establish 462 current defects. The report correction later completed with 8 GLM requests. Its v4 records show precise/simple available but not invoked; there is no method-use claim for that correction. Astra reconciled remaining factual prose and checked every final count/range against original group metadata. Original-plan readback confirmed the final bytes accepted, with its owner completed/live false and a fresh checker. This accepts the bounded triage report, not a collector implementation. Exact source counts, reviews, failures and native identities live under `wave-b-legwork/` in the existing execution record. These two audits used 40 model requests including both corrections. Neither method presence nor invocation proves causal quality improvement.

## 7. Schema repair passed its suite but still had source-level gaps

After the isolated login was restored, the schema repair used another 150 Opus requests. Its independent checker passed the 38 new tests, 48 harness tests, 132 capsule tests, compiler red/green, typecheck and build. The report remained unaccepted after source review.

An admitted zero-model probe reproduced a hard-linked output changing a file outside the requested source root, and schema descriptions whose generated types disagreed with actual parsed values. It also verified all 32 frozen compatibility answers against the retained baseline parser, confirming the portable test fix. Both useful progress and remaining failures are retained under `t13-schema-work/`.

The used checkout exceeded the unchanged bounded path scan. A fresh complete checkout received the exact same baseline and delivered patch. The old checkout was preserved, and the protected checker and acceptance criteria were unchanged. That follow-up completed with 149 more Opus requests. Its independent checker passed 43 new tests and the unchanged 48/132 suites, typecheck and build. Astra's new zero-model probe confirmed the hard-link, scalar and added-nested-field corrections. It still reproduced a narrower named-member type mismatch for chart/purpose, which is now receiving a focused correction. No installed file was used as a write-protection probe, and no source quality receipt or schema installation is claimed. The schema code/repair attempts so far used 460 requests, including the interrupted and authentication-failed work, before that focused correction. This is recorded effort, not a measured efficiency gain.

The focused named-member correction completed with 73 further Opus requests. Independent checks passed 44 new tests, the preserved suites, compiler red/green, typecheck and build. The unchanged eight-case reviewer probe also passed. The exact source was accepted through its original controller. Total schema implementation and repair effort reached 533 requests before integration.

Current-based integration then passed 383 affected tests, the generated-reference check, typecheck and package build with zero model requests. Two installed GLM journeys used 3 and 2 requests respectively: exact marker delivery was accepted, and deliberate missing output was refused as intended. The existing journal selected `theo-schema-derived-artifacts`, digest `15b7951315a001f0c0ce87805563ce8d9e57987ca5c69f63e83150013fb214f6`, with active readback and predecessor retention verified. Evidence: `t13-installation/activation.json` and `live-proof.json` under the execution record.

The parser and generated declarations are installed. The generator and reference table remain in the retained source tree. This is not completion of owner-authored templates, every consumer or full T13. No causal skill benefit, billing result or productivity gain is established.

## 8. Current Chart discovery did not establish a lint failure

The current-body audit used 19 GLM requests plus 8 for a correction. Its initial report alleged a corrupted contract copy, skipped operating files and an excerpt-count mismatch. Host byte/hash/count checks disproved those claims. The cited path list also contained substantive rules, so it was not the claimed deterministic failing fixture. Both drafts are preserved and the final source report is accepted after factual reconciliation and current-byte checking.

The accepted conclusion is limited: the read sample did not establish a ready new Chart-body rule. Discovery matches are not defects, and 852 Markdown files totaling 5,544,677 bytes are not the runtime's library-cap accounting. No instruction was changed and no new scoping approval gate was inferred. Evidence: `t19-current-fixtures/` under the execution record.

The separate capsule-authoring lint has started with Opus in an isolated current-based checkout. Its protected checker setup passed before dispatch. It remains implementation in progress, not an accepted lint or completed T19.
