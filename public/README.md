# Agent Engineering Handbook

Build better coding environments for agents: turn a repeated correction into an
executable check, a confusing decision into discoverable knowledge, and a missing
operation into a usable tool.

An independent, public handbook maintained by **Desmond Landry (@desland01)**, based on
Theo's [video](https://www.youtube.com/watch?v=xmGY276gEFY) (*Claude Code's creator has
some really good advice*, July 21, 2026) and extended through direct inspection of
Theo's T3 Code and Melee fork, Matt Pocock's Course Video Manager, and Boris Cherny's
public engineering work. With attribution and thanks to **Theo (@t3dotgg)**,
**Matt Pocock (@mattpocock)**, and **Boris Cherny (@bcherny)** — none of whom endorses
this handbook. Research snapshot: **September 9, 2026**; later pull requests are
identified as later evidence.

The source-derived facts (what the video says, what the inspected repositories contain)
are kept separate from author recommendations and from this edition's own local checks.
See [validation.md](validation.md) for exactly what was run and what was not.

Read the [live handbook](https://agent-engineering-handbook.dev/) or its
[GitHub source](https://github.com/desland01/agent-engineering-handbook).

## Ten lessons

Ten short lessons are the canonical reading path. Work through them in order, or open
the one that names your problem. Each lesson cites its evidence; recovery comes from the existing guide, not a separate video idea.
This table is generated from `build/lessons.json` between the markers below — see
[CONTRIBUTING.md](CONTRIBUTING.md) for the sync command, and never edit it by hand.

<!-- lessons:start -->
| Lesson | Summary |
|---|---|
| [You turn repeated mistakes into reliable checks](lessons/recurring-mistakes.md) | Catch a repeated mistake with a check that rejects it. |
| [You diagnose failed checks without copying logs](lessons/ci-feedback.md) | Give the agent access to the failed check and its logs. |
| [You test the result users actually need](lessons/prove-it-works.md) | Verify the real result, not just a successful command. |
| [You give agents a working preview](lessons/working-previews.md) | Make the running change reachable from the agent’s environment. |
| [You make missing operations usable by agents](lessons/missing-tools.md) | Bridge a real capability gap with the smallest useful interface. |
| [You write instructions that fix observed confusion](lessons/useful-instructions.md) | Put decisions where the next task can use them. |
| [You keep shared contracts consistent across layers](lessons/shared-contracts.md) | Keep the language, types and runtime boundary in agreement. |
| [You navigate unfamiliar code without guessing](lessons/codebase-navigation.md) | Make the codebase understandable when you return to it. |
| [You resume work without repeating completed steps](lessons/resume-work.md) | Reuse finished work and resume only the missing stage. |
| [You remove obstacles for the next contributor](lessons/better-environments.md) | Choose a recurring obstacle worth removing for future work. |
<!-- lessons:end -->

## Start with the problem you have

| Current problem | Start here |
|---|---|
| You keep correcting the same mistake | [You turn repeated mistakes into reliable checks](lessons/recurring-mistakes.md) |
| You relay CI errors by hand | [You diagnose failed checks without copying logs](lessons/ci-feedback.md) |
| Tests pass but the actual feature fails | [You test the result users actually need](lessons/prove-it-works.md) |
| A new agent cannot run or inspect the app | [You give agents a working preview](lessons/working-previews.md) |
| The agent cannot perform a required operation | [You make missing operations usable by agents](lessons/missing-tools.md) |
| Agents repeatedly miss project decisions | [You write instructions that fix observed confusion](lessons/useful-instructions.md) |
| Types, docs and runtime disagree | [You keep shared contracts consistent across layers](lessons/shared-contracts.md) |
| Your project is becoming hard to navigate | [You navigate unfamiliar code without guessing](lessons/codebase-navigation.md) |
| Long jobs redo finished work | [You resume work without repeating completed steps](lessons/resume-work.md) |
| Every new contributor hits the same setup wall | [You remove obstacles for the next contributor](lessons/better-environments.md) |

The last row opens lesson 9, which absorbs the recovery guide. The
[runnable lint example](examples/recurring-rule/README.md) accompanies lesson 1.
The former guide sources below are retained for provenance, remain unrendered,
and their public addresses permanently redirect to their owning lessons.

## All 13 implementation guides

1. [01 — Convert recurring failures into permanent rules](guides/01-recurring-failures.md)
2. [02 — One critical journey test beats broad shallow coverage](guides/02-critical-journey-tests.md)
3. [03 — Make previews usable from the agent's environment](guides/03-preview-workspaces.md)
4. [04 — Let the agent read and resolve CI failures](guides/04-ci-feedback.md)
5. [05 — Put project knowledge where the next task needs it](guides/05-knowledge-and-instructions.md)
6. [06 — Build small tool adapters for capability gaps](guides/06-tool-adapters.md)
7. [07 — Turn newcomer questions into improvements](guides/07-team-learning.md)
8. [08 — Keep contracts consistent across the application](guides/08-compose-contracts.md)
9. [09 — Verification contracts](guides/09-verification-contracts.md)
10. [10 — Codebase navigation and tooling](guides/10-codebase-navigation-and-tooling.md)
11. [11 — One domain language and one transport when an agent calls your API](guides/11-domain-language-and-agent-apis.md)
12. [12 — Make pipeline artifacts reusable, resumable and honestly complete](guides/12-artifact-identity-and-recovery.md)
13. [13 — Validate the output through several useful views](guides/13-layered-validation.md)

Each guide gives a concrete method, fitting use cases and verification limits. Code
sketches are labeled as illustrative; the bundled lint example is separately runnable
and tested (see [examples/recurring-rule](examples/recurring-rule/README.md) for the
`npm` demo).

## What the repository investigations add

- [Theo: T3 Code and Melee](github-inspection.md) — architecture, custom lint, native
  skill dispatch, preview evidence, all 13 fork PRs, the linked verifier commit, and
  the source-completeness verifier repair.
- [Matt Pocock: Course Video Manager](matt-pocock-inspection.md) — domain vocabulary,
  one HTTP transport, static import boundaries, publication identity, resumable agent
  work, subprocess output draining and gaps between documentation and CI.
- [Boris Cherny: public engineering work](boris-cherny-inspection.md) — a staged
  compiler architecture, seeded fuzzing, generated-output validation, benchmarks, CLI
  compatibility, narrow tools and instruction-validator repairs.

The reports distinguish inspected code, author-reported results, remote CI records and
local execution. They link to pinned source snapshots wherever possible. Finding code
under an account does not mean the account owner personally authored every change; open
PRs are separated from merged work.

## Portable skills

Standalone, portable skill directories you can adopt into any agent setup that reads
Markdown. Each keeps its reusable expertise and its owner-authorization boundaries, and
ships scoped references plus OpenAI-compatible interface metadata. Availability below
means the public package exists in this repository; it is not a claim that the skill
has been evaluated in real trials.

| Skill | Use it for |
|---|---|
| [Agent feedback engineering](skills/agent-feedback-engineering/SKILL.md) | Choose and prove a reusable response to an observed failure |
| [Agent-ready workspaces](skills/agent-ready-workspaces/SKILL.md) | Repair the setup, preview or outcome-check gap that blocks a fresh agent |
| [Agent context calibration](skills/agent-context-calibration/SKILL.md) | Diagnose missing project knowledge and select the right place for it |
| [Agent tool adapters](skills/agent-tool-adapters/SKILL.md) | Bridge a missing capability and verify the intended agent can use it |
| [Agent output verification](skills/agent-output-verification/SKILL.md) | Judge whether a run's actual output satisfies what was asked |
| [Agent artifact recovery](skills/agent-artifact-recovery/SKILL.md) | Resume interrupted work without repeating completed stages |
| [Agent contract consistency](skills/agent-contract-consistency/SKILL.md) | Keep vocabulary, shared types and runtime behavior in agreement |

Each directory includes `SKILL.md`, `references/implementation.md`,
`references/source-patterns.md`, and `agents/openai.yaml` interface metadata whose
default prompt references the skill's own `$skill-name`. See
[adoption.md](adoption.md) for how to install one or combine it into an existing skill.
Do not load all of them for every task.

Use the relevant guide with your existing workflow today. [Task prompts](prompts.md)
make the input and expected evidence concrete.

## The 19 useful video ideas, in order

Each of these observations now lives inside the lesson that covers it — see
[Ten lessons](#ten-lessons) for the canonical reading path. This table remains the
source-evidence reference: it maps every observation to the moment in the video where
it was made and the guidance that implements it. See
[detailed extraction](evidence/video-research.md) and
[structured ideas](evidence/video-tips.json) for speaker attribution, evidence type and
caveats.

| Video | Idea | Implement |
|---|---|---|
| [01:53](https://www.youtube.com/watch?v=xmGY276gEFY&t=113s) | Close the CI feedback loop: let the agent trigger CI and read failed logs itself | [Guide 04](guides/04-ci-feedback.md) |
| [03:46](https://www.youtube.com/watch?v=xmGY276gEFY&t=226s) | Design tiny two-actor end-to-end tests that catch whole classes of failure | [Guide 02](guides/02-critical-journey-tests.md) |
| [04:47](https://www.youtube.com/watch?v=xmGY276gEFY&t=287s) | Infra and DX automation now speeds up every agent, not just you | [Guide 04](guides/04-ci-feedback.md) |
| [05:06](https://www.youtube.com/watch?v=xmGY276gEFY&t=306s) | Preview environments matter more now that code is built outside your machine | [Guide 03](guides/03-preview-workspaces.md) |
| [05:52](https://www.youtube.com/watch?v=xmGY276gEFY&t=352s) | Build small tool adapters for things the CLI cannot do (video/asset uploads to PRs) | [Guide 06](guides/06-tool-adapters.md) |
| [06:30](https://www.youtube.com/watch?v=xmGY276gEFY&t=390s) | Authoring and testing a small skill has a tight, low-stakes feedback loop | [Guide 06](guides/06-tool-adapters.md) |
| [07:28](https://www.youtube.com/watch?v=xmGY276gEFY&t=448s) | Teams are now more willing to fund tooling time — use it | [Guide 07](guides/07-team-learning.md) |
| [08:00](https://www.youtube.com/watch?v=xmGY276gEFY&t=480s) | Move recurring fixes from per-occurrence agent corrections into executable checks (lint rule, CI step, routine) | [Guide 01](guides/01-recurring-failures.md) |
| [08:30](https://www.youtube.com/watch?v=xmGY276gEFY&t=510s) | Custom lint rules became economical: agents lower the cost of the code and its tests | [Guide 01](guides/01-recurring-failures.md) |
| [09:56](https://www.youtube.com/watch?v=xmGY276gEFY&t=596s) | Encode domain knowledge as infrastructure so newcomers' agents get steered too | [Guide 05](guides/05-knowledge-and-instructions.md) |
| [11:14](https://www.youtube.com/watch?v=xmGY276gEFY&t=674s) | Treat newcomer questions as a signal for onboarding gaps (Theo's dumb-questions practice) | [Guide 07](guides/07-team-learning.md) |
| [12:29](https://www.youtube.com/watch?v=xmGY276gEFY&t=749s) | Write your CLAUDE.md / AGENTS.md yourself; watch agent behavior and adjust | [Guide 05](guides/05-knowledge-and-instructions.md) |
| [13:03](https://www.youtube.com/watch?v=xmGY276gEFY&t=783s) | Use steering files to make the agent say no (and to get fast feedback when things go wrong) | [Guide 05](guides/05-knowledge-and-instructions.md) |
| [13:51](https://www.youtube.com/watch?v=xmGY276gEFY&t=831s) | Compose layers so type safety runs end to end — and expect that click more often now | [Guide 08](guides/08-compose-contracts.md) |
| [14:33](https://www.youtube.com/watch?v=xmGY276gEFY&t=873s) | Write Claude.mds, review.mds, skills, and docs so agents work with zero prompting context | [Guide 05](guides/05-knowledge-and-instructions.md) |
| [16:02](https://www.youtube.com/watch?v=xmGY276gEFY&t=962s) | Calibrate from a cold start: run minimal prompts first, add context only where it fails | [Guide 05](guides/05-knowledge-and-instructions.md) |
| [16:38](https://www.youtube.com/watch?v=xmGY276gEFY&t=998s) | Instruction files should steer toward success, not list where things are | [Guide 05](guides/05-knowledge-and-instructions.md) |
| [16:54](https://www.youtube.com/watch?v=xmGY276gEFY&t=1014s) | Building environments where code lands well is a career-level skill (with a grain of salt) | [Guide 07](guides/07-team-learning.md) |
| [18:00](https://www.youtube.com/watch?v=xmGY276gEFY&t=1080s) | Solo projects now exceed your own comprehension — build systems so you and your agents don't get lost | [Guide 10](guides/10-codebase-navigation-and-tooling.md) |

## What was checked

The local lint demonstration proves that the unwanted import passes without its
restriction and is rejected with the restriction while the supported import passes. The
Melee verifier's original nine tests and current fifteen tests pass; a separate
synthetic comparison reproduces the completeness gap and the repair. These are verifier
tests with mocked builds, not a real game build.

For this edition, the ten-lesson catalog is checked at every build: the exact ten
approved lesson IDs, all nineteen video observations covered exactly once, valid
guide/skill relations, present source anchors and lesson prose, and a README lesson
table that matches the manifest (see [validation.md](validation.md)). The per-skill
evaluation suites shipped under each new package's `eval/` directory define their
cases but have not been run in this edition.

See [validation.md](validation.md) for the exact scope, screenshot hashes and
rendered-page checks. The public applications, upload service and private agent systems
were not executed. Sponsor claims and universal career/productivity claims remain
unverified.

## Build and preview locally

The site is static HTML generated from the Markdown in this repository; the generated
`public/` directory is committed for local reading. Vercel rebuilds it from the
editable sources and checks the result on each deployment.

```sh
# Regenerate public/ from the editable sources (idempotent):
python3 -m pip install -r build/requirements.txt   # Markdown==3.10.3
python3 build/render.py
python3 build/check.py                             # links, counts, hashes

# If the lesson set changed, regenerate the README table between its markers:
python3 build/render.py --sync-readme
```

`build/render.py` reads only the editable Markdown, assets and JSON — never `public/`
— and rewrites `public/` from scratch, so rerunning cannot feed on its own output. An
ordinary render verifies the README lesson table against `build/lessons.json` and fails
on drift; only `--sync-readme` writes the README.

Run the lint demo:

```sh
cd examples/recurring-rule
npm ci --ignore-scripts
npm run demo        # detects the bad import; accepts the supported import
```

## Keep or rebuild this handbook

The Markdown, images, JSON evidence, `lessons/` sources and seven skill directories are
the editable sources; everything in `public/` is generated. `build/render.py`
regenerates the pages and gallery using Python Markdown 3.10.3
(`build/requirements.txt` pins that dependency). The lesson manifest
(`build/lessons.json`) owns the lesson order and relations; the lesson Markdown owns
the prose; `build/lesson_catalog.py` validates both — manifest shape and version, the
exact approved lesson set and order, chapter assignment, source/guide/skill references,
the nineteen legacy routes, per-lesson anchors and prose minimums — and fails the build
when any of those specific checks is violated.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the update flow and
[ATTRIBUTION.md](ATTRIBUTION.md) for source attribution. The original long-form video
is not redistributed here and no complete transcript or repository clone is bundled.
