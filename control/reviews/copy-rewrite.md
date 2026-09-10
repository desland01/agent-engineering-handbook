<!-- Copy rewrite by the gpt-6-astra route, 2026-09-10, executed by owner instruction and applied in commit 74925be. The worker's report, verbatim. Its 'candidate diff' at the end is the patch that was applied. -->

# Copy rewrite

The opening now names the engineering task: “Build a codebase agents can work in”. The copy keeps the evidence limits visible and helps readers choose a guide or skill.

## Delivery

- Requested base: `5e6787066851acfae61f0dc18ade9e1a1698f075`. This commit is absent from the workspace's available Git history.
- Available base: `233e535e1ad29df2d86b05643e15c9e079559b0f`, whose commit subject is `baseline 989e0d92acc00c32223c8ca8c06bb502e975e648`.
- `deliverable.patch` contains the exact stdout of the requested diff command: zero bytes because the command failed. It is **not a usable patch**.
- A usable candidate diff against the available base is included at the end of this report. It is not substituted for the requested baseline comparison.
- Changed strings: 98 JSON fields and 15 renderer copy units. The table below includes each change, with the adoption paragraph shown as its concatenated literal.
- No code, HTML structure, links, IDs, classes, tier keys or ledger statuses changed. Existing unrelated files were preserved.
- The patch is local only. Nothing was committed, published or fetched from the network.

## Requested patch comparison is blocked

The exact requested command exited 128:

```sh
git diff 5e6787066851acfae61f0dc18ade9e1a1698f075 -- build/home.json build/render.py
```

Its stdout was empty. Its stderr was:

```text
fatal: bad object 5e6787066851acfae61f0dc18ade9e1a1698f075
```

`git cat-file -t` also failed for this commit. `git log --all` showed only the available root commit named above. No history was fetched or rewritten. The before/after table and candidate diff use the available workspace base, which matched both source files before editing. Supplying the requested commit object, or authorizing the available base instead, is necessary to complete the requested patch delivery.

## Evidence and limits

The build and package check both exited successfully. The runner printed `PASS` only after each successful exit. The renderer itself prints a build summary, without a PASS token. The native check prints its own PASS line. Exact native output and the runner's final markers appear below.

Additional local assertions passed:

- Every changed JSON field is on the permitted list. JSON keys, array lengths, Markdown links and inline code spans match the baseline.
- Replaying only the listed renderer text substitutions reproduces the edited file byte for byte. The executable syntax tree matches after string contents are masked.
- All 54 generated pages retain the baseline HTML tag structure and attributes, excluding changed meta-description content.
- The hero title is 35 characters. Its emphasis is one complete word in that title.
- The three idea tiers retain their keys and order. The evidence file yields practice/advice/opinion counts of 6/7/6.
- The non-endorsement remains unchanged in the hero edition line and is explicit in the credits.
- The ledger wording was compared with `README.md` under “What was checked” and `validation.md`. Its RUN entries describe the existing research record, not new lint or verifier executions during this rewrite.
- The source report and shelf data support the guide counts and grouped compiler-validation methods. “Three investigations” replaces the inaccurate claim of three repositories read line by line. Ten guides belong to the video and T3 Code/Melee investigation together, not the fork alone.
- `git diff --check` passed without output.

### Spelling

American spelling was selected from the source copy before editing. A case-insensitive whole-word comparison found 94 American occurrences against 5 British occurrences across the paired terms below.

The sample combined the Markdown pages rendered by the build, skill Markdown, home JSON and renderer string literals. It excluded duplicate `public/` files, fenced code, inline code and URLs. Renderer literals include explanatory strings, so this measures source-copy usage, not a count of words painted on screen.

| British form | Count | American form | Count |
|---|---:|---|---:|
| behaviour | 2 | behavior | 41 |
| behaviours | 0 | behaviors | 1 |
| generalised | 2 | generalized | 4 |
| summarised | 1 | summarized | 1 |
| labelled | 0 | labeled | 1 |
| colour | 0 | color | 1 |
| authorisation | 0 | authorization | 18 |
| authorised | 0 | authorized | 27 |

The other sampled pairs had no occurrences: labelling/labeling, colours/colors, optimised/optimized, organised/organized, centre/center, centred/centered, normalise/normalize and normalised/normalized. New copy uses American spelling. Protected identifiers and source prose outside the permitted fields remain unchanged.

### Meta descriptions

| Hub | Characters |
|---|---:|
| ideas | 153 |
| guides | 148 |
| skills | 167 |
| investigations | 164 |
| frames | 164 |

Each description is within 90–175 characters and ends on a complete sentence.

### Visual inspection could not run

The required local browser route exited 1 before opening a page. It could not import its installed dependency:

```text
Error [ERR_MODULE_NOT_FOUND]: Cannot find module '/Users/thebeast/.npm-global/lib/node_modules/@browserbasehq/stagehand/dist/index.mjs' imported from /Users/thebeast/.nautilus/releases/browser-route-20260910/release/charts/core-skills/bundles/browser/scripts/stagehand-local.mjs
```

The attempted command was:

```sh
node /Users/thebeast/.nautilus/releases/browser-route-20260910/release/charts/core-skills/bundles/browser/scripts/stagehand-local.mjs --url file:///Users/thebeast/.nautilus/releases/browser-route-20260910/var/workspaces/handbook-20260910-workers/astra-copy/public/index.html --out /Users/thebeast/.nautilus/releases/browser-route-20260910/var/workspaces/handbook-20260910-workers/astra-copy/tmp/browser --viewport 1440x1100,390x850
```

No screenshot, layout measurement or console result was obtained. No alternate browser route or dependency installation was attempted. The headline length is checked, but its rendered line count and the changed copy's desktop/mobile fit remain unverified. Inspect the rebuilt pages at those widths when the required browser dependency is available.

## Exact build output

Command, from the supplied workspace:

```sh
.venv/bin/python build/render.py
```

Native stdout, exit 0 (stderr empty):

```text
Rendered 24 Markdown pages, 19 idea pages, 4 skill pages, the ideas, guides, skills and investigations indexes, the home page (13 guides, 3 investigations, 4 skills, 19 ideas, 12 frames), the gallery and 404.html into public/.
```

Runner's final marker, emitted after the successful exit:

```text
PASS
```

## Exact check output

Command, from the supplied workspace:

```sh
.venv/bin/python build/check.py
```

Native stdout, exit 0 (stderr empty):

```text
PASS: 54 HTML pages, 13 guides, 19 idea pages, 4 skills, 12 frames verified; links, hashes, semantics, disclosure routes, no network loads and required metadata fields OK.
```

Runner's final marker, emitted after the successful exit:

```text
PASS
```

These commands used the supplied workspace's `.venv/bin/python`, with `PYTHONDONTWRITEBYTECODE=1`. Output was captured locally without altering either checker or its success criteria.

## Every changed string

JSON paths use zero-based array indexes. Renderer rows name the copy literal, not the unchanged surrounding HTML. The adoption row retains its HTML to show the unchanged code span.

| Field or literal | Before | After | Why |
|---|---|---|---|
| home.json title | Theo's advice, turned into a system you can run | Build a codebase agents can work in | Names the engineering task before requiring the reader to know Theo or the project. |
| home.json lead | Nineteen ideas from his video, thirteen guides that state their own limits, four skills you can drop into any agent, and three repositories read line by line. Every claim carries the check behind it, or says plainly that it has none. | Turn recurring agent mistakes into checks, clear instructions and usable tools. This handbook connects nineteen video ideas to thirteen guides, four portable skills and three source investigations. Each guide states what its checks can prove. | Leads with repeatable engineering work, retains the set counts and removes unsupported line-by-line and universal-check claims. |
| home.json shelves&#91;0&#93;.title | From Theo's video | Theo's video | Names the source directly without repeating the surrounding source-group label. |
| home.json shelves&#91;0&#93;.description | Eight guides adapted from the July 21, 2026 video. Quotes in these guides are from the video; Boris quotes are Boris as quoted by Theo. | Eight guides adapted from the July 21, 2026 video. All quotations come from the video, including Boris's words as quoted by Theo. | Keeps the guide count and video date, and makes indirect Boris quotation explicit. |
| home.json shelves&#91;1&#93;.title | From the Melee for Mac snapshot | Melee for Mac | Names the source directly without repeating the surrounding source-group label. |
| home.json shelves&#91;1&#93;.description | Two guides adapted from &#96;tools/verify.py&#96;, &#96;docs/code-map.md&#96; and related tooling in t3dotgg/melee4mac at head &#96;a276aeb70f9879204d891d967f1c9442523568e1&#96;. | Two guides adapted from &#96;tools/verify.py&#96;, &#96;docs/code-map.md&#96; and related tools in t3dotgg/melee4mac at revision &#96;a276aeb70f9879204d891d967f1c9442523568e1&#96;. | Keeps both code paths, the exact revision and the guide count while replacing snapshot jargon. |
| home.json shelves&#91;2&#93;.title | From Course Video Manager | Matt Pocock's Course Video Manager | Names the source directly without repeating the surrounding source-group label. |
| home.json shelves&#91;2&#93;.description | Two guides adapted from Matt Pocock's course-video-manager snapshot &#96;4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8&#96;. | Two guides adapted from Matt Pocock's course-video-manager at revision &#96;4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8&#96;. | Keeps the guide count and exact revision while shortening the source description. |
| home.json shelves&#91;3&#93;.title | From Boris Cherny's public work | Boris Cherny's public work | Names the source directly without repeating the surrounding source-group label. |
| home.json shelves&#91;3&#93;.description | One guide generalised from the json-schema-to-typescript CI (fixtures, built-artifact smoke tests, fuzzing, a real-world corpus and conformance checks). | One guide adapted from json-schema-to-typescript CI checks: fixtures, built-artifact smoke tests, fuzzing, a real-world corpus and conformance checks. | Retains the guide count and all five check types while replacing an abstract adaptation phrase. |
| home.json use_when.01 | For a developer on a team where the same mistake keeps coming back. | When your team keeps correcting the same mistake instead of checking for it automatically. | Describes the recurring team mistake and the reason to introduce a check. |
| home.json use_when.02 | For a team whose product has one path that must never silently break. | When your product has a critical user journey that must never break silently. | Names the critical user journey and preserves the silent-breakage condition. |
| home.json use_when.03 | When work happens in several worktrees or machines and a person or agent needs to inspect the actual change. | When people or agents need to inspect changes across different worktrees or machines. | Keeps people, agents, worktrees and machines while shortening the situation. |
| home.json use_when.04 | When you repeatedly carry CI errors from a web page back into an agent prompt. | When you keep copying CI errors from a web page into an agent prompt. | Describes the manual copying the guide addresses in everyday wording. |
| home.json use_when.05 | When an agent or newcomer repeatedly misses a project decision, convention or non-obvious fact. | When agents or newcomers keep missing project decisions, conventions or facts that are easy to overlook. | Keeps decisions, conventions and easily missed facts as distinct knowledge gaps. |
| home.json use_when.06 | For closing a specific gap between what your agent needs to do and what its existing tools can do. | When your agent needs an operation that its current tools do not support. | Names the missing operation without the extra explanation of a capability gap. |
| home.json use_when.07 | When teammates or agents repeatedly get stuck on the same first task. | When teammates or agents keep getting stuck on the same first task. | Uses direct wording for repeated difficulty with the same first task. |
| home.json use_when.08 | When agents repeatedly invent mismatched data shapes between storage, APIs and the interface. | When agents create mismatched data shapes across storage, APIs and the user interface. | Keeps storage, APIs and interface data shapes while removing accusatory wording. |
| home.json use_when.09 | Make “done” mean a checked artifact, not a finished command. | When a finished command leaves you unsure whether the output meets its requirements. | Names the uncertainty between command completion and verified output without a rhetorical reversal. |
| home.json use_when.10 | Find where to change code in an unfamiliar codebase, and wrap external tools so their failures are safe. | When you need to navigate unfamiliar code and handle failures from external tools safely. | Keeps both unfamiliar-code navigation and safe external-tool failure handling. |
| home.json use_when.11 | You are adding a command, route or agent verb to a codebase that already has a glossary and a deployed API. | When you add a command, route or agent operation to a codebase with a glossary and deployed API. | Keeps the existing glossary and deployed API as conditions, and replaces agent-verb jargon. |
| home.json use_when.12 | You run a pipeline with slow, expensive steps and want to reuse prior work, resume after crashes, and never accept a truncated artifact. | When slow, expensive work needs reusable outputs, recovery after crashes and checks for truncated artifacts. | Retains expense, reuse, crash recovery and truncated-output checks in one shorter sentence. |
| home.json use_when.13 | When a generator, parser, migration, transformation or widely used library has failures that ordinary fixtures miss. | When ordinary fixtures miss failures in a generator, parser, migration, transformation or widely used library. | Leads with the fixture gap and retains each supported class of software. |
| home.json reports_heading | Three repository investigations | Check the sources behind the guides | Explains why the reader would open an investigation. |
| home.json reports_description | Each report distinguishes inspected code, author-reported results, remote CI records and local execution, and links pinned snapshots wherever possible. Open PRs are separated from merged work. | The three reports separate inspected code, author reports, remote CI records and local runs. They link to pinned snapshots where possible and distinguish open pull requests from merged work. | Retains all evidence categories, pinned-source limits and open-versus-merged distinctions in shorter sentences. |
| home.json skills_heading | Four portable skills | Choose a skill for the problem you have | Helps the reader choose by their current problem rather than by the size of the set. |
| home.json skills_description | A skill is a plain directory any agent that reads Markdown can load. Adopt the one that matches the failure you actually have; loading all four for every task makes each of them worse. | Each skill is a folder of instructions for an agent setup that reads Markdown. Choose the one you need rather than loading all four for every task. | Defines the folder format and retains selective adoption without claiming that loading all skills worsens performance. |
| home.json ideas_heading | Nineteen ideas, in the order they were said | Start with the advice behind the methods | Offers a reason to read the ideas instead of making the set size the headline. |
| home.json frames_heading | Twelve frames from the video | See what was on screen | Gives the gallery a clear purpose while leaving the count to its description. |
| home.json frames_description | Extracted with ffmpeg and captioned to separate what is visible from what is narrated. Each opens the &#91;gallery&#93;(evidence.html), which has full-size images, observations and extraction hashes. | Twelve frames extracted with ffmpeg separate visible evidence from narration. Each opens the &#91;gallery&#93;(evidence.html) for full-size images, observations and extraction hashes. | Retains extraction, visible-versus-narrated evidence, the gallery link and image/hash details. |
| home.json hubs.ideas.title | Nineteen ideas, sorted by what's behind them | The evidence behind Theo's advice | Gives the browser tab a clear identity without repeating a set-size headline. |
| home.json hubs.ideas.h1 | What Theo does, what he tells you to do, and what he's still working out | What backs Theo's advice? | States what the reader can do on this page in one idea. |
| home.json hubs.ideas.lead | Nineteen ideas from the July 21, 2026 video, sorted by what is behind each one — a practice he runs, a directive he gives, or an opinion he offers as one. Every idea opens the video at the second it was said. | Explore nineteen ideas from Theo's July 21, 2026 video, grouped by practice, advice and opinion. Each idea links to the moment in the video where it was said. | Keeps the count, date, categories and timed video links without overstating timestamp precision. |
| home.json hubs.ideas.description | Nineteen ideas from Theo's agent engineering video, sorted into what he actually does, what he tells you to do, and what he offers as opinion. Each timestamped. | Explore nineteen ideas from Theo's video, grouped by what he does, what he tells you to do and what he offers as opinion. Each links to its video moment. | Summarizes this page in complete sentences within the required metadata length. |
| home.json hubs.ideas.tiers&#91;0&#93;.label | 01 / What he does | 01 / Practice | Uses a short evidence-category label while preserving the key and tier order. |
| home.json hubs.ideas.tiers&#91;0&#93;.lead | Backed by something Theo did: a practice he runs, or a story from a real codebase. | Theo describes practices he uses and recounts his experience of work in real codebases. | Keeps the practice-and-anecdote scope without suggesting independent validation of every anecdote. |
| home.json hubs.ideas.tiers&#91;1&#93;.label | 02 / What he tells you | 02 / Advice | Uses a short evidence-category label while preserving the key and tier order. |
| home.json hubs.ideas.tiers&#91;1&#93;.lead | Directives — Theo's own, and Boris's as Theo quoted and endorsed them on camera. | Theo gives his own advice and quotes Boris, with endorsement or qualifications where recorded. | Preserves direct advice and quoted Boris posts without claiming blanket endorsement by Theo. |
| home.json hubs.ideas.tiers&#91;2&#93;.label | 03 / Still working out | 03 / Opinion | Uses a short evidence-category label while preserving the key and tier order. |
| home.json hubs.ideas.tiers&#91;2&#93;.heading | What he's still working out | What he offers as opinion | Labels the third tier as opinion without implying these views are unresolved work. |
| home.json hubs.ideas.tiers&#91;2&#93;.lead | Offered as opinion, and flagged as opinion. The video says so itself for several of these. | These ideas are offered as opinion, including several the video explicitly qualifies as such. This group also includes the sponsor segment, whose performance claims remain unverified. | Keeps opinion qualifications and makes the included sponsor segment's unverified claims explicit. |
| home.json hubs.ideas.next&#91;0&#93;&#91;1&#93; | The thirteen guides | Implementation guides | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.ideas.next&#91;0&#93;&#91;2&#93; | the methods these ideas turn into | turn an idea into a method you can apply | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.ideas.next&#91;1&#93;&#91;1&#93; | The twelve frames | Video frames | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.ideas.next&#91;1&#93;&#91;2&#93; | what was visible on screen while they were said | see what appeared on screen at these moments | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.guides.title | Thirteen implementation guides | Methods for recurring agent problems | Gives the browser tab a clear identity without repeating a set-size headline. |
| home.json hubs.guides.h1 | Thirteen guides, and what each one does not prove | Find a method for the failure you face | States what the reader can do on this page in one idea. |
| home.json hubs.guides.lead | Each guide names one recurring failure, gives a method concrete enough to run this week, says who it fits, and states the limits of what it verifies. They are grouped by the source each was adapted from: the video, two repository snapshots, and Boris Cherny's public work. | Each of the thirteen guides gives a concrete method, when to use it and what it can verify. Browse by source: the video, the Melee and Course Video Manager snapshots, or Boris Cherny's public work. | Keeps methods, fitting situations, verification limits and all source groups without a this-week promise. |
| home.json hubs.guides.description | Thirteen implementation guides for agent coding environments. Each gives a concrete method, the situations it fits, and the limits of what it actually verifies. | Find thirteen guides for recurring problems in agent coding environments. Each explains a method, when to use it and the limits of what it verifies. | Summarizes this page in complete sentences within the required metadata length. |
| home.json hubs.guides.next&#91;0&#93;&#91;2&#93; | the input and expected evidence for every guide | define the input and expected evidence for each guide | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.guides.next&#91;1&#93;&#91;1&#93; | The runnable example | Run the lint example | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.guides.next&#91;1&#93;&#91;2&#93; | guide 01 as a lint rule you can execute | try the executable companion to guide 01 | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.guides.next&#91;2&#93;&#91;1&#93; | The four skills | Portable skills | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.guides.next&#91;2&#93;&#91;2&#93; | the same methods, packaged for an agent | give an agent instructions drawn from these methods | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.skills.title | Four portable agent skills | Portable instructions for coding agents | Gives the browser tab a clear identity without repeating a set-size headline. |
| home.json hubs.skills.h1 | Four skills, portable to any agent setup | Give your agent the instructions it needs | States what the reader can do on this page in one idea. |
| home.json hubs.skills.lead | A skill here is a plain directory any agent that reads Markdown can load: the instructions themselves, two reference files, and OpenAI-compatible interface metadata. Adopt the one that matches the failure you actually have. Loading all four for every task makes each of them worse. | Choose the skill that fits your problem rather than loading all four for every task. Each is a Markdown folder with instructions, two reference files and OpenAI-compatible interface metadata. Use it with an agent setup that reads Markdown. | Keeps selective adoption, folder contents and compatible setups without an unsupported performance claim. |
| home.json hubs.skills.description | Four portable agent skills as plain Markdown directories: feedback engineering, agent-ready workspaces, context calibration and tool adapters. Adopt one, not all four. | Choose from four Markdown skills for agent feedback, workspace setup, project context and tool adapters. Each includes instructions, references and interface metadata. | Summarizes this page in complete sentences within the required metadata length. |
| home.json hubs.skills.next&#91;0&#93;&#91;1&#93; | Adopting a skill | Install a skill | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.skills.next&#91;0&#93;&#91;2&#93; | how to install one or fold it into a skill you already run | add one or combine it with a skill you already use | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.skills.next&#91;1&#93;&#91;1&#93; | The thirteen guides | Implementation guides | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.skills.next&#91;1&#93;&#91;2&#93; | the reasoning each skill was distilled from | read the methods behind the instructions | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.investigations.title | Three repository investigations | Source investigations behind the handbook | Gives the browser tab a clear identity without repeating a set-size headline. |
| home.json hubs.investigations.h1 | Three repositories, read rather than summarised | Follow the guides back to the source | States what the reader can do on this page in one idea. |
| home.json hubs.investigations.lead | Each report separates the code that was actually inspected from the results its author reported, remote CI records from runs on this machine, and open pull requests from merged work. Source snapshots are pinned wherever the repository allowed it. | Three reports distinguish inspected code, author-reported results, remote CI records and local runs. Each separates open pull requests from merged work and links pinned source snapshots where possible. Work under an account is not necessarily written by that person. | Preserves evidence and snapshot limits, corrects the repository/report conflation and clarifies account authorship. |
| home.json hubs.investigations.description | Three repository investigations that separate inspected code from author-reported results, remote CI records from local runs, and open pull requests from merged work. | Read three source investigations separating inspected code, author reports, remote CI records and local runs. Open pull requests are distinguished from merged work. | Summarizes this page in complete sentences within the required metadata length. |
| home.json hubs.investigations.findings.github-inspection.md&#91;0&#93; | A completion contract names the real output, the completeness its inputs need, and the outcome the consumer actually sees. | A completion contract specifies the real output, how complete its inputs must be and the outcome its consumer sees. | Keeps the output, input completeness and consumer-visible outcome in concrete wording. |
| home.json hubs.investigations.findings.github-inspection.md&#91;1&#93; | Recurring mistakes belong in existing lint, type, test and build boundaries, with both rejection and legitimate success proved. | Recurring mistakes need checks at existing lint, type, test and build boundaries that reject bad changes and accept valid ones. | Retains existing check boundaries and proof of both rejection and legitimate success. |
| home.json hubs.investigations.findings.github-inspection.md&#91;2&#93; | Explicit ownership isolates agent writes and test state, hides provider quirks behind adapters, and verifies remote artifact access. | Explicit ownership separates agent writes and test state, contains provider quirks in adapters and checks remote access to artifacts. | Keeps separate writes, test state, provider adapters and remote artifact access. |
| home.json hubs.investigations.findings.github-inspection.md&#91;3&#93; | Calibrated knowledge keeps decisions beside their code, and evidence carries provenance: local run, CI, author report or untested hardware. | Project decisions stay beside relevant code, while evidence distinguishes local runs, remote CI, author reports and untested hardware. | Retains code-adjacent decisions and every named category of evidence. |
| home.json hubs.investigations.findings.matt-pocock-inspection.md&#91;0&#93; | Domain vocabulary, durable decisions, bounded modules and callable agent APIs became the guide on speaking a codebase's language. | Shared vocabulary, lasting decisions, bounded modules and callable agent APIs inform the guide to speaking a codebase's language. | Retains vocabulary, durable decisions, bounded modules and callable APIs as the guide's sources. |
| home.json hubs.investigations.findings.matt-pocock-inspection.md&#91;1&#93; | Output identity, resumable work and result-format recovery became the guide on artifacts that survive an interruption. | Output identity, resumable work and recovery from malformed results inform the guide to artifacts that survive interruptions. | Retains identity, interruption recovery and malformed-result recovery as distinct lessons. |
| home.json hubs.investigations.findings.matt-pocock-inspection.md&#91;2&#93; | The most transferable habit is to make a desired outcome easy to invoke and hard to misreport. | The report recommends making the intended outcome easy to request and hard to misreport. | Attributes the recommendation to the report instead of presenting a superlative as fact. |
| home.json hubs.investigations.findings.boris-cherny-inspection.md&#91;0&#93; | Guide 13's layered validation tests the public output, reproduces novel failures, and preserves meaningful baselines. | Guide 13 adapts layered validation to test public output, reproduce new failures and preserve meaningful baselines. | Keeps public-output tests, novel-failure reproduction and meaningful baselines tied to the guide. |
| home.json hubs.investigations.findings.boris-cherny-inspection.md&#91;1&#93; | The same work is measured before and after a change, so improvement is a comparison rather than an impression. | Before-and-after measurements compare the same work to establish whether a change improved the result. | Keeps the same-work comparison without a rhetorical contrast or a claimed measured speedup. |
| home.json hubs.investigations.findings.boris-cherny-inspection.md&#91;2&#93; | Lessons the guides already cover, like lint, adapters and native loading, become supporting references in the four skills. | Existing lessons on lint, adapters and native loading provide supporting references for the four skills. | Retains existing-guide lessons and their supporting role in the four skills. |
| home.json hubs.investigations.next&#91;0&#93;&#91;1&#93; | The thirteen guides | Implementation guides | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.investigations.next&#91;0&#93;&#91;2&#93; | five of them were adapted from these repositories | read the five guides adapted from the inspected repositories | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.investigations.next&#91;1&#93;&#91;1&#93; | Validation and provenance | Checks and source records | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.investigations.next&#91;1&#93;&#91;2&#93; | how every claim on this site was checked | see what was checked and what remains unverified | Removes the unsupported implication that every site claim was checked. |
| home.json hubs.frames.title | Twelve frames from the video | Video frames and what they show | Gives the browser tab a clear identity without repeating a set-size headline. |
| home.json hubs.frames.h1 | The video, with visible evidence | See the evidence in the video frames | States what the reader can do on this page in one idea. |
| home.json hubs.frames.lead | Twelve frames extracted with ffmpeg and inspected at full resolution. Each caption separates what is visible in the frame from what the speaker only describes — a post on screen is not a live demonstration. | Twelve frames were extracted with ffmpeg and inspected at full resolution. Captions distinguish what appears on screen from what the speaker describes. A visible post does not establish that a live demonstration took place. | Keeps full-resolution inspection and the distinction between a visible post and a live demonstration. |
| home.json hubs.frames.description | Twelve frames extracted from Theo's agent engineering video, captioned to separate what is visible on screen from what the speaker only describes. | Inspect twelve full-size frames from Theo's video. Captions distinguish what appears on screen from what the speaker describes, with extraction commands and hashes. | Summarizes this page in complete sentences within the required metadata length. |
| home.json hubs.frames.next&#91;0&#93;&#91;1&#93; | The nineteen ideas | Video ideas | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.frames.next&#91;0&#93;&#91;2&#93; | the takeaways these moments belong to | read the takeaways from these moments | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json hubs.frames.next&#91;1&#93;&#91;1&#93; | Validation and provenance | Checks and source records | Names the destination in terms a reader can recognize without knowing the site. |
| home.json hubs.frames.next&#91;1&#93;&#91;2&#93; | extraction commands and SHA-256 hashes | inspect the extraction commands and SHA-256 hashes | States the reason to follow this existing link while preserving its destination and factual scope. |
| home.json title_em | system | codebase | Emphasizes the object being improved and remains one word in the title. |
| home.json ideas_band | Swipe the row. Or open the full set sorted by what is behind each idea: a practice he runs, a directive he gives, or an opinion he offers as one. | Browse the ideas in video order, or open the full set grouped by practice, advice and opinion. | Keeps video order and the three evidence groups while shortening the browsing directions. |
| home.json ledger.rows&#91;0&#93;&#91;1&#93; | The lint demonstration: the unwanted import passes without its rule, is rejected with it, and the supported import still passes. | The lint demo accepts the unwanted import without its rule, rejects it with the rule and accepts the supported import. | Preserves the unrestricted bad-import pass, restricted rejection and supported-import pass. |
| home.json ledger.rows&#91;1&#93;&#91;1&#93; | The Melee verifier: its original nine tests and its current fifteen pass. | The Melee verifier passed its original nine tests and the current set of fifteen. | Reports the original and current verifier test counts as completed research checks. |
| home.json ledger.rows&#91;2&#93;&#91;1&#93; | A synthetic comparison that reproduces the verifier's completeness gap, and the repair. | A synthetic comparison reproduced the completeness gap: the original verifier accepted incomplete source metrics, while the repaired version rejected them. | Explains the synthetic completeness failure and repaired rejection without implying a real build. |
| home.json ledger.rows&#91;3&#93;&#91;1&#93; | Those are verifier tests against mocked builds. No real game build was run. | The verifier tests used mocked builds and establish verifier behavior only. No real game build was run. | Retains mocked builds and explicitly limits the result to verifier behavior. |
| home.json ledger.rows&#91;4&#93;&#91;1&#93; | The public applications, the upload service and the private agent systems. | The public applications, upload service and private agent systems were not executed for this research. | Makes the fixed NOT RUN status a complete statement about the research scope. |
| home.json ledger.rows&#91;5&#93;&#91;1&#93; | Sponsor performance claims, and the universal career and productivity claims. | Sponsor performance claims and universal claims about careers and productivity have not been verified. | Keeps sponsor performance and universal career/productivity claims explicitly unverified. |
| home.json ledger.credits&#91;2&#93;&#91;1&#93; | None of them endorses this handbook | Theo, Matt Pocock and Boris Cherny do not endorse this handbook. | Makes the non-endorsement explicit by name. |
| home.json ledger.credits&#91;3&#93;&#91;2&#93; | later pull requests are later evidence | later pull requests are identified as later evidence | Keeps later pull requests distinct from the dated research snapshot. |
| render.py CLAIMS&#91;'github-inspection.md'&#93; | Ten of the thirteen guides trace back to this fork. It is where the video's advice met code that had to work. | Ten of the thirteen guides draw on the video and this investigation of T3 Code and Melee. The report connects advice to inspected code. | Corrects the fork-only attribution using the video shelf and the T3 Code/Melee report, while retaining the guide count. |
| render.py CLAIMS&#91;'matt-pocock-inspection.md'&#93; | A codebase with a glossary and one transport. The two guides on domain language and durable artifacts came from reading it. | A glossary and one HTTP transport give this codebase a shared language. Its source informed two guides on domain language and durable artifacts. | Names HTTP and keeps the two guides tied to inspected source, without claiming application execution. |
| render.py CLAIMS&#91;'boris-cherny-inspection.md'&#93; | A compiler tested five different ways. Guide 13's layered validation is that method, generalised. | Guide 13 adapts five validation methods: fixtures, built-artifact smoke tests, fuzzing, real-world schemas and conformance checks. Tests were inspected, not run locally. | Names the five grouped methods from the source shelf and states that compiler tests were not run locally. |
| render.py SKILL_CAPTIONS&#91;'agent-feedback-engineering'&#93; | FAILURE → CHECK | MISTAKE → CHECK | Uses a familiar word for the repeated error that motivates the check. |
| render.py SKILL_CAPTIONS&#91;'agent-ready-workspaces'&#93; | SETUP → PREVIEW → PROOF | SETUP → PREVIEW → CHECK | Names a check rather than implying unrestricted proof of the workspace. |
| render.py SKILL_CAPTIONS&#91;'agent-context-calibration'&#93; | MISSING → PLACED | CONTEXT → RIGHT PLACE | Explains placement without restricting project knowledge to instruction files. |
| render.py SKILL_CAPTIONS&#91;'agent-tool-adapters'&#93; | GAP → ADAPTER → VERIFIED | GAP → TOOL → CHECK | Makes the capability gap and its check readable without adapter vocabulary. |
| render.py hub_next() heading | Where to go from here | Choose your next step | Turns the closing heading into a direct invitation to choose a destination. |
| render.py landing() primary button | Read the ideas | Explore the ideas | Matches the destination, where readers browse ideas grouped by evidence. |
| render.py landing() secondary button | Open the guides | Find a guide | States the purpose of opening the guide index. |
| render.py landing() guides band heading | Thirteen implementation guides | Find a guide for your next change | Leads with the reader's task while keeping the count in the adjacent description. |
| render.py landing() guides band description | Grouped by the source each was adapted from. Each guide gives a concrete method, fitting use cases and verification limits. | Thirteen guides grouped by source, each with a method, fitting use cases and verification limits. | Keeps the set, source grouping and verification limits in a single scan line. |
| render.py guides_index() track h2 | Thirteen stages, in the order they were adapted | Browse the guides by source | Describes the actual grouping without implying a chronological sequence of stages. |
| render.py guides_index() track lead | Scroll the track. Each stage is one guide; the labels above the rail say which source it came from. | Scroll across the thirteen guides and use the labels above them to identify each source. | Explains the horizontal control without track-and-rail terminology or a semicolon. |
| render.py skills_index() adopt paragraph (concatenated literal) | &lt;p class="route"&gt;Each title opens that skill's own page, which holds its raw &lt;code&gt;SKILL.md&lt;/code&gt; exactly as shipped, both reference files and its directory on GitHub.&lt;/p&gt; | &lt;p class="route"&gt;Open a skill to read its instructions and both reference files. The page links its unchanged &lt;code&gt;SKILL.md&lt;/code&gt; and its directory on GitHub.&lt;/p&gt; | Distinguishes the instructions and references displayed on the page from the unchanged raw file and GitHub directory links. |

## Working tree and recovery

The requested build regenerated `public/` for checking. Its pre-task bytes were then restored from a temporary workspace copy, so delivery changes only the permitted source files and the two declared artifacts. Rebuild after applying the patch to produce the revised pages. All task-created temporary files were removed.

To undo this copy rewrite, save the candidate diff below to a local workspace file, then run `git apply --reverse --check` with that file. Only if the check succeeds, run `git apply --reverse` with the same file. Stop if the check fails, because later edits may overlap. Do not use the empty `deliverable.patch` for recovery. The candidate diff does not touch unrelated files present at task start.

## Candidate diff against the available base

This is a usable local-workspace diff, not the requested comparison against the missing commit. Its reverse applicability was checked against the rewritten source files. No equivalence to the missing baseline is claimed.

```diff
diff --git a/build/home.json b/build/home.json
index 27b9ad0..b0bec91 100644
--- a/build/home.json
+++ b/build/home.json
@@ -1,13 +1,13 @@
 {
   "_comment": "Landing-page data that is not already in README.md: the title and lead, the short header attribution, the source-grouped shelves and each guide's one-line use-when. Everything else on the landing page (problem table, guide titles, investigations, skills, the 19 ideas, the attribution and what-was-checked paragraphs) is parsed from README.md; frames come from evidence/frame-manifest.json. Inline `code` spans in descriptions are rendered as <code> so long paths and revision hashes can wrap.",
-  "title": "Theo's advice, turned into a system you can run",
-  "lead": "Nineteen ideas from his video, thirteen guides that state their own limits, four skills you can drop into any agent, and three repositories read line by line. Every claim carries the check behind it, or says plainly that it has none.",
+  "title": "Build a codebase agents can work in",
+  "lead": "Turn recurring agent mistakes into checks, clear instructions and usable tools. This handbook connects nineteen video ideas to thirteen guides, four portable skills and three source investigations. Each guide states what its checks can prove.",
   "basis_short": "An independent public edition by Desmond Landry (@desland01), built from Theo's video and direct inspection of three repositories. Theo, Matt Pocock and Boris Cherny do not endorse it.",
   "shelves": [
     {
       "id": "guides-video",
-      "title": "From Theo's video",
-      "description": "Eight guides adapted from the July 21, 2026 video. Quotes in these guides are from the video; Boris quotes are Boris as quoted by Theo.",
+      "title": "Theo's video",
+      "description": "Eight guides adapted from the July 21, 2026 video. All quotations come from the video, including Boris's words as quoted by Theo.",
       "guides": [
         "01",
         "02",
@@ -22,8 +22,8 @@
     },
     {
       "id": "guides-melee",
-      "title": "From the Melee for Mac snapshot",
-      "description": "Two guides adapted from `tools/verify.py`, `docs/code-map.md` and related tooling in t3dotgg/melee4mac at head `a276aeb70f9879204d891d967f1c9442523568e1`.",
+      "title": "Melee for Mac",
+      "description": "Two guides adapted from `tools/verify.py`, `docs/code-map.md` and related tools in t3dotgg/melee4mac at revision `a276aeb70f9879204d891d967f1c9442523568e1`.",
       "guides": [
         "09",
         "10"
@@ -32,8 +32,8 @@
     },
     {
       "id": "guides-course-video-manager",
-      "title": "From Course Video Manager",
-      "description": "Two guides adapted from Matt Pocock's course-video-manager snapshot `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`.",
+      "title": "Matt Pocock's Course Video Manager",
+      "description": "Two guides adapted from Matt Pocock's course-video-manager at revision `4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8`.",
       "guides": [
         "11",
         "12"
@@ -42,8 +42,8 @@
     },
     {
       "id": "guides-boris-cherny",
-      "title": "From Boris Cherny's public work",
-      "description": "One guide generalised from the json-schema-to-typescript CI (fixtures, built-artifact smoke tests, fuzzing, a real-world corpus and conformance checks).",
+      "title": "Boris Cherny's public work",
+      "description": "One guide adapted from json-schema-to-typescript CI checks: fixtures, built-artifact smoke tests, fuzzing, a real-world corpus and conformance checks.",
       "guides": [
         "13"
       ],
@@ -51,25 +51,25 @@
     }
   ],
   "use_when": {
-    "01": "For a developer on a team where the same mistake keeps coming back.",
-    "02": "For a team whose product has one path that must never silently break.",
-    "03": "When work happens in several worktrees or machines and a person or agent needs to inspect the actual change.",
-    "04": "When you repeatedly carry CI errors from a web page back into an agent prompt.",
-    "05": "When an agent or newcomer repeatedly misses a project decision, convention or non-obvious fact.",
-    "06": "For closing a specific gap between what your agent needs to do and what its existing tools can do.",
-    "07": "When teammates or agents repeatedly get stuck on the same first task.",
-    "08": "When agents repeatedly invent mismatched data shapes between storage, APIs and the interface.",
-    "09": "Make “done” mean a checked artifact, not a finished command.",
-    "10": "Find where to change code in an unfamiliar codebase, and wrap external tools so their failures are safe.",
-    "11": "You are adding a command, route or agent verb to a codebase that already has a glossary and a deployed API.",
-    "12": "You run a pipeline with slow, expensive steps and want to reuse prior work, resume after crashes, and never accept a truncated artifact.",
-    "13": "When a generator, parser, migration, transformation or widely used library has failures that ordinary fixtures miss."
+    "01": "When your team keeps correcting the same mistake instead of checking for it automatically.",
+    "02": "When your product has a critical user journey that must never break silently.",
+    "03": "When people or agents need to inspect changes across different worktrees or machines.",
+    "04": "When you keep copying CI errors from a web page into an agent prompt.",
+    "05": "When agents or newcomers keep missing project decisions, conventions or facts that are easy to overlook.",
+    "06": "When your agent needs an operation that its current tools do not support.",
+    "07": "When teammates or agents keep getting stuck on the same first task.",
+    "08": "When agents create mismatched data shapes across storage, APIs and the user interface.",
+    "09": "When a finished command leaves you unsure whether the output meets its requirements.",
+    "10": "When you need to navigate unfamiliar code and handle failures from external tools safely.",
+    "11": "When you add a command, route or agent operation to a codebase with a glossary and deployed API.",
+    "12": "When slow, expensive work needs reusable outputs, recovery after crashes and checks for truncated artifacts.",
+    "13": "When ordinary fixtures miss failures in a generator, parser, migration, transformation or widely used library."
   },
-  "reports_heading": "Three repository investigations",
-  "reports_description": "Each report distinguishes inspected code, author-reported results, remote CI records and local execution, and links pinned snapshots wherever possible. Open PRs are separated from merged work.",
-  "skills_heading": "Four portable skills",
-  "skills_description": "A skill is a plain directory any agent that reads Markdown can load. Adopt the one that matches the failure you actually have; loading all four for every task makes each of them worse.",
-  "ideas_heading": "Nineteen ideas, in the order they were said",
+  "reports_heading": "Check the sources behind the guides",
+  "reports_description": "The three reports separate inspected code, author reports, remote CI records and local runs. They link to pinned snapshots where possible and distinguish open pull requests from merged work.",
+  "skills_heading": "Choose a skill for the problem you have",
+  "skills_description": "Each skill is a folder of instructions for an agent setup that reads Markdown. Choose the one you need rather than loading all four for every task.",
+  "ideas_heading": "Start with the advice behind the methods",
   "ideas_description": "Distinct takeaways, including qualified opinions. Each timestamp opens the video at that moment; each idea names the guide that implements it. Speaker attribution, evidence type and caveats are in the [detailed extraction](evidence/video-research.md) and the [structured ideas file](evidence/video-tips.json).",
   "frame_guides": {
     "_comment": "Frame seconds -> the guide that applies what the frame shows; used by the gallery's 'applied in' link.",
@@ -86,141 +86,141 @@
     "884": "05",
     "1021": "07"
   },
-  "frames_heading": "Twelve frames from the video",
-  "frames_description": "Extracted with ffmpeg and captioned to separate what is visible from what is narrated. Each opens the [gallery](evidence.html), which has full-size images, observations and extraction hashes.",
+  "frames_heading": "See what was on screen",
+  "frames_description": "Twelve frames extracted with ffmpeg separate visible evidence from narration. Each opens the [gallery](evidence.html) for full-size images, observations and extraction hashes.",
   "_hubs_comment": "Copy for the five section pages. A band on the home page introduces a set to someone scrolling past it; a section page addresses someone who has arrived at that set, so each carries its own heading, lead, browser title and meta description rather than reusing the band's. `next` is the closing route: where a reader who has finished this set should go, as [href, label, why] rows.",
   "hubs": {
     "ideas": {
-      "title": "Nineteen ideas, sorted by what's behind them",
-      "h1": "What Theo does, what he tells you to do, and what he's still working out",
-      "lead": "Nineteen ideas from the July 21, 2026 video, sorted by what is behind each one — a practice he runs, a directive he gives, or an opinion he offers as one. Every idea opens the video at the second it was said.",
-      "description": "Nineteen ideas from Theo's agent engineering video, sorted into what he actually does, what he tells you to do, and what he offers as opinion. Each timestamped.",
+      "title": "The evidence behind Theo's advice",
+      "h1": "What backs Theo's advice?",
+      "lead": "Explore nineteen ideas from Theo's July 21, 2026 video, grouped by practice, advice and opinion. Each idea links to the moment in the video where it was said.",
+      "description": "Explore nineteen ideas from Theo's video, grouped by what he does, what he tells you to do and what he offers as opinion. Each links to its video moment.",
       "tiers": [
         {
           "key": "does",
-          "label": "01 / What he does",
+          "label": "01 / Practice",
           "heading": "What he actually does",
-          "lead": "Backed by something Theo did: a practice he runs, or a story from a real codebase."
+          "lead": "Theo describes practices he uses and recounts his experience of work in real codebases."
         },
         {
           "key": "says",
-          "label": "02 / What he tells you",
+          "label": "02 / Advice",
           "heading": "What he tells you to do",
-          "lead": "Directives — Theo's own, and Boris's as Theo quoted and endorsed them on camera."
+          "lead": "Theo gives his own advice and quotes Boris, with endorsement or qualifications where recorded."
         },
         {
           "key": "thinks",
-          "label": "03 / Still working out",
-          "heading": "What he's still working out",
-          "lead": "Offered as opinion, and flagged as opinion. The video says so itself for several of these."
+          "label": "03 / Opinion",
+          "heading": "What he offers as opinion",
+          "lead": "These ideas are offered as opinion, including several the video explicitly qualifies as such. This group also includes the sponsor segment, whose performance claims remain unverified."
         }
       ],
       "next": [
         [
           "guides.html",
-          "The thirteen guides",
-          "the methods these ideas turn into"
+          "Implementation guides",
+          "turn an idea into a method you can apply"
         ],
         [
           "evidence.html",
-          "The twelve frames",
-          "what was visible on screen while they were said"
+          "Video frames",
+          "see what appeared on screen at these moments"
         ]
       ]
     },
     "guides": {
-      "title": "Thirteen implementation guides",
-      "h1": "Thirteen guides, and what each one does not prove",
-      "lead": "Each guide names one recurring failure, gives a method concrete enough to run this week, says who it fits, and states the limits of what it verifies. They are grouped by the source each was adapted from: the video, two repository snapshots, and Boris Cherny's public work.",
-      "description": "Thirteen implementation guides for agent coding environments. Each gives a concrete method, the situations it fits, and the limits of what it actually verifies.",
+      "title": "Methods for recurring agent problems",
+      "h1": "Find a method for the failure you face",
+      "lead": "Each of the thirteen guides gives a concrete method, when to use it and what it can verify. Browse by source: the video, the Melee and Course Video Manager snapshots, or Boris Cherny's public work.",
+      "description": "Find thirteen guides for recurring problems in agent coding environments. Each explains a method, when to use it and the limits of what it verifies.",
       "next": [
         [
           "prompts.html",
           "Task prompts",
-          "the input and expected evidence for every guide"
+          "define the input and expected evidence for each guide"
         ],
         [
           "examples/recurring-rule/README.html",
-          "The runnable example",
-          "guide 01 as a lint rule you can execute"
+          "Run the lint example",
+          "try the executable companion to guide 01"
         ],
         [
           "skills.html",
-          "The four skills",
-          "the same methods, packaged for an agent"
+          "Portable skills",
+          "give an agent instructions drawn from these methods"
         ]
       ]
     },
     "skills": {
-      "title": "Four portable agent skills",
-      "h1": "Four skills, portable to any agent setup",
-      "lead": "A skill here is a plain directory any agent that reads Markdown can load: the instructions themselves, two reference files, and OpenAI-compatible interface metadata. Adopt the one that matches the failure you actually have. Loading all four for every task makes each of them worse.",
-      "description": "Four portable agent skills as plain Markdown directories: feedback engineering, agent-ready workspaces, context calibration and tool adapters. Adopt one, not all four.",
+      "title": "Portable instructions for coding agents",
+      "h1": "Give your agent the instructions it needs",
+      "lead": "Choose the skill that fits your problem rather than loading all four for every task. Each is a Markdown folder with instructions, two reference files and OpenAI-compatible interface metadata. Use it with an agent setup that reads Markdown.",
+      "description": "Choose from four Markdown skills for agent feedback, workspace setup, project context and tool adapters. Each includes instructions, references and interface metadata.",
       "next": [
         [
           "adoption.html",
-          "Adopting a skill",
-          "how to install one or fold it into a skill you already run"
+          "Install a skill",
+          "add one or combine it with a skill you already use"
         ],
         [
           "guides.html",
-          "The thirteen guides",
-          "the reasoning each skill was distilled from"
+          "Implementation guides",
+          "read the methods behind the instructions"
         ]
       ]
     },
     "investigations": {
-      "title": "Three repository investigations",
-      "h1": "Three repositories, read rather than summarised",
-      "lead": "Each report separates the code that was actually inspected from the results its author reported, remote CI records from runs on this machine, and open pull requests from merged work. Source snapshots are pinned wherever the repository allowed it.",
-      "description": "Three repository investigations that separate inspected code from author-reported results, remote CI records from local runs, and open pull requests from merged work.",
+      "title": "Source investigations behind the handbook",
+      "h1": "Follow the guides back to the source",
+      "lead": "Three reports distinguish inspected code, author-reported results, remote CI records and local runs. Each separates open pull requests from merged work and links pinned source snapshots where possible. Work under an account is not necessarily written by that person.",
+      "description": "Read three source investigations separating inspected code, author reports, remote CI records and local runs. Open pull requests are distinguished from merged work.",
       "_findings_comment": "The findings shown on each study of investigations.html, edited from the report's own takeaway section: github-inspection.md -> 'What to take away', matt-pocock-inspection.md -> 'How this changes our guides', boris-cherny-inspection.md -> 'What this adds to the implementation package'. One sentence each, at most 22 words, beginning with a noun phrase.",
       "findings": {
         "github-inspection.md": [
-          "A completion contract names the real output, the completeness its inputs need, and the outcome the consumer actually sees.",
-          "Recurring mistakes belong in existing lint, type, test and build boundaries, with both rejection and legitimate success proved.",
-          "Explicit ownership isolates agent writes and test state, hides provider quirks behind adapters, and verifies remote artifact access.",
-          "Calibrated knowledge keeps decisions beside their code, and evidence carries provenance: local run, CI, author report or untested hardware."
+          "A completion contract specifies the real output, how complete its inputs must be and the outcome its consumer sees.",
+          "Recurring mistakes need checks at existing lint, type, test and build boundaries that reject bad changes and accept valid ones.",
+          "Explicit ownership separates agent writes and test state, contains provider quirks in adapters and checks remote access to artifacts.",
+          "Project decisions stay beside relevant code, while evidence distinguishes local runs, remote CI, author reports and untested hardware."
         ],
         "matt-pocock-inspection.md": [
-          "Domain vocabulary, durable decisions, bounded modules and callable agent APIs became the guide on speaking a codebase's language.",
-          "Output identity, resumable work and result-format recovery became the guide on artifacts that survive an interruption.",
-          "The most transferable habit is to make a desired outcome easy to invoke and hard to misreport."
+          "Shared vocabulary, lasting decisions, bounded modules and callable agent APIs inform the guide to speaking a codebase's language.",
+          "Output identity, resumable work and recovery from malformed results inform the guide to artifacts that survive interruptions.",
+          "The report recommends making the intended outcome easy to request and hard to misreport."
         ],
         "boris-cherny-inspection.md": [
-          "Guide 13's layered validation tests the public output, reproduces novel failures, and preserves meaningful baselines.",
-          "The same work is measured before and after a change, so improvement is a comparison rather than an impression.",
-          "Lessons the guides already cover, like lint, adapters and native loading, become supporting references in the four skills."
+          "Guide 13 adapts layered validation to test public output, reproduce new failures and preserve meaningful baselines.",
+          "Before-and-after measurements compare the same work to establish whether a change improved the result.",
+          "Existing lessons on lint, adapters and native loading provide supporting references for the four skills."
         ]
       },
       "next": [
         [
           "guides.html",
-          "The thirteen guides",
-          "five of them were adapted from these repositories"
+          "Implementation guides",
+          "read the five guides adapted from the inspected repositories"
         ],
         [
           "validation.html",
-          "Validation and provenance",
-          "how every claim on this site was checked"
+          "Checks and source records",
+          "see what was checked and what remains unverified"
         ]
       ]
     },
     "frames": {
-      "title": "Twelve frames from the video",
-      "h1": "The video, with visible evidence",
-      "lead": "Twelve frames extracted with ffmpeg and inspected at full resolution. Each caption separates what is visible in the frame from what the speaker only describes — a post on screen is not a live demonstration.",
-      "description": "Twelve frames extracted from Theo's agent engineering video, captioned to separate what is visible on screen from what the speaker only describes.",
+      "title": "Video frames and what they show",
+      "h1": "See the evidence in the video frames",
+      "lead": "Twelve frames were extracted with ffmpeg and inspected at full resolution. Captions distinguish what appears on screen from what the speaker describes. A visible post does not establish that a live demonstration took place.",
+      "description": "Inspect twelve full-size frames from Theo's video. Captions distinguish what appears on screen from what the speaker describes, with extraction commands and hashes.",
       "next": [
         [
           "ideas.html",
-          "The nineteen ideas",
-          "the takeaways these moments belong to"
+          "Video ideas",
+          "read the takeaways from these moments"
         ],
         [
           "validation.html",
-          "Validation and provenance",
-          "extraction commands and SHA-256 hashes"
+          "Checks and source records",
+          "inspect the extraction commands and SHA-256 hashes"
         ]
       ]
     }
@@ -230,34 +230,34 @@
     "index.html": "An evidence-backed handbook for building coding environments agents work well in: nineteen ideas, thirteen guides, four portable skills and three repository investigations.",
     "404.html": "That page is not in the handbook. Routes to the ideas, guides, skills, investigations and the handbook index."
   },
-  "title_em": "system",
-  "ideas_band": "Swipe the row. Or open the full set sorted by what is behind each idea: a practice he runs, a directive he gives, or an opinion he offers as one.",
+  "title_em": "codebase",
+  "ideas_band": "Browse the ideas in video order, or open the full set grouped by practice, advice and opinion.",
   "ledger": {
     "_comment": "The closing ledger: what was run, what was not, and what is only a claim. Each row is [status, text]; status is one of RUN, LIMIT, NOT RUN, UNVERIFIED and must agree with README.md's What was checked and validation.md.",
     "rows": [
       [
         "RUN",
-        "The lint demonstration: the unwanted import passes without its rule, is rejected with it, and the supported import still passes."
+        "The lint demo accepts the unwanted import without its rule, rejects it with the rule and accepts the supported import."
       ],
       [
         "RUN",
-        "The Melee verifier: its original nine tests and its current fifteen pass."
+        "The Melee verifier passed its original nine tests and the current set of fifteen."
       ],
       [
         "RUN",
-        "A synthetic comparison that reproduces the verifier's completeness gap, and the repair."
+        "A synthetic comparison reproduced the completeness gap: the original verifier accepted incomplete source metrics, while the repaired version rejected them."
       ],
       [
         "LIMIT",
-        "Those are verifier tests against mocked builds. No real game build was run."
+        "The verifier tests used mocked builds and establish verifier behavior only. No real game build was run."
       ],
       [
         "NOT RUN",
-        "The public applications, the upload service and the private agent systems."
+        "The public applications, upload service and private agent systems were not executed for this research."
       ],
       [
         "UNVERIFIED",
-        "Sponsor performance claims, and the universal career and productivity claims."
+        "Sponsor performance claims and universal claims about careers and productivity have not been verified."
       ]
     ],
     "credits": [
@@ -273,13 +273,13 @@
       ],
       [
         "Endorsement",
-        "None of them endorses this handbook",
+        "Theo, Matt Pocock and Boris Cherny do not endorse this handbook.",
         ""
       ],
       [
         "Snapshot",
         "September 9, 2026",
-        "later pull requests are later evidence"
+        "later pull requests are identified as later evidence"
       ]
     ]
   }
diff --git a/build/render.py b/build/render.py
index 7fd625c..fe45020 100644
--- a/build/render.py
+++ b/build/render.py
@@ -34,9 +34,9 @@ from icons import IDEAS, SKILLS, GUIDES, INVESTIGATIONS
 REPO = Path(__file__).resolve().parent.parent
 # The claim line of each investigation, copied verbatim from COPY.md.
 CLAIMS = {
-    'github-inspection.md': "Ten of the thirteen guides trace back to this fork. It is where the video's advice met code that had to work.",
-    'matt-pocock-inspection.md': 'A codebase with a glossary and one transport. The two guides on domain language and durable artifacts came from reading it.',
-    'boris-cherny-inspection.md': "A compiler tested five different ways. Guide 13's layered validation is that method, generalised.",
+    'github-inspection.md': "Ten of the thirteen guides draw on the video and this investigation of T3 Code and Melee. The report connects advice to inspected code.",
+    'matt-pocock-inspection.md': 'A glossary and one HTTP transport give this codebase a shared language. Its source informed two guides on domain language and durable artifacts.',
+    'boris-cherny-inspection.md': "Guide 13 adapts five validation methods: fixtures, built-artifact smoke tests, fuzzing, real-world schemas and conformance checks. Tests were inspected, not run locally.",
 }
 OUT = REPO / 'public'
 ASSETS = REPO / 'build/assets'
@@ -463,7 +463,7 @@ def hub_next(hub, prefix=''):
         f'<span class="k">{escape(why)}</span></a></li>'
         for href, label, why in hub['next'])
     return ('<section class="hub-next" aria-labelledby="hub-next-h"><div class="wrap">'
-            f'{marker("Next")}<h2 id="hub-next-h">Where to go from here</h2>'
+            f'{marker("Next")}<h2 id="hub-next-h">Choose your next step</h2>'
             f'<ul role="list">{rows}</ul></div></section>')
 
 
@@ -484,10 +484,10 @@ def idea_tile(i, prefix=''):
 # The mono caption that sits inside each skill's drawing: the loop it closes,
 # as the artwork's own label rather than a line placed under it.
 SKILL_CAPTIONS = {
-    'agent-feedback-engineering': 'FAILURE \u2192 CHECK',
-    'agent-ready-workspaces': 'SETUP \u2192 PREVIEW \u2192 PROOF',
-    'agent-context-calibration': 'MISSING \u2192 PLACED',
-    'agent-tool-adapters': 'GAP \u2192 ADAPTER \u2192 VERIFIED',
+    'agent-feedback-engineering': 'MISTAKE \u2192 CHECK',
+    'agent-ready-workspaces': 'SETUP \u2192 PREVIEW \u2192 CHECK',
+    'agent-context-calibration': 'CONTEXT \u2192 RIGHT PLACE',
+    'agent-tool-adapters': 'GAP \u2192 TOOL \u2192 CHECK',
 }
 
 
@@ -595,7 +595,7 @@ def landing(idx, home, frames):
   <div class="opening-copy">
     <h1>{title_html}</h1>
     <p class="lead">{escape(home['lead'])}</p>
-    <div class="actions"><a class="btn primary" href="ideas.html">Read the ideas</a><a class="btn" href="guides.html">Open the guides</a></div>
+    <div class="actions"><a class="btn primary" href="ideas.html">Explore the ideas</a><a class="btn" href="guides.html">Find a guide</a></div>
     <ul class="contents" role="list" aria-label="Contents">{contents}</ul>
     <a class="prompt" href="skills.html" aria-label="The four skills, each invoked as a slash command"><span aria-hidden="true"><span class="ps">&#8811;</span> <span class="typed" data-lines="{escape('|'.join('/' + sk['name'] for sk in idx['skills']))}">/{escape(idx['skills'][0]['name'])}</span><span class="cursor">&#9612;</span></span></a>
     <p class="edition"><span class="num">Edition of {EDITION_DATE}.</span> {escape(home['basis_short'])} <a href="#attribution">Full attribution</a> is at the end of the page.</p>
@@ -621,7 +621,7 @@ def landing(idx, home, frames):
 </div></section>
 
 <section class="band" id="guides" aria-labelledby="guides-h"><div class="wrap">
-  {band_head('Implementation', 'guides-h', 'Thirteen implementation guides', 'Grouped by the source each was adapted from. Each guide gives a concrete method, fitting use cases and verification limits.')}
+  {band_head('Implementation', 'guides-h', 'Find a guide for your next change', 'Thirteen guides grouped by source, each with a method, fitting use cases and verification limits.')}
   <ul class="shelves" role="list">{shelves}</ul>
   <p class="route">{more('guides.html', f'All {counts["guides"]} guides')}</p>
 </div></section>
@@ -723,8 +723,8 @@ def guides_index(idx, home):
                        f'<span class="sr-only">Guide {n}: </span>{escape(g["title"])}</a>'
                        f'<p class="when">{escape(home["use_when"][n])}</p></li>')
     track = ('<section class="band track-band" aria-labelledby="track-h"><div class="wrap">'
-             f'{marker("The track")}<h2 id="track-h">Thirteen stages, in the order they were adapted</h2>'
-             '<p class="tier-lead">Scroll the track. Each stage is one guide; the labels above the rail say which source it came from.</p></div>'
+             f'{marker("The track")}<h2 id="track-h">Browse the guides by source</h2>'
+             '<p class="tier-lead">Scroll across the thirteen guides and use the labels above them to identify each source.</p></div>'
              '<div class="wrap"><div class="track-row" data-row="of" tabindex="0" role="region" aria-label="The thirteen guides as a track">'
              f'<ol class="track" role="list">{stages}</ol></div></div></section>')
     body = (site_head('', 'guides.html') +
@@ -781,8 +781,8 @@ def skills_index(idx, home):
     # What every skill page carries, said once here rather than four times. The
     # instruction to adopt one rather than all four now opens the page, where a
     # reader meets it before choosing, and the adoption route closes it.
-    adopt = ('<p class="route">Each title opens that skill\'s own page, which holds its raw '
-             '<code>SKILL.md</code> exactly as shipped, both reference files and its directory on GitHub.</p>')
+    adopt = ('<p class="route">Open a skill to read its instructions and both reference files. The page links its unchanged '
+             '<code>SKILL.md</code> and its directory on GitHub.</p>')
     hub = home['hubs']['skills']
     body = (site_head('', 'skills.html') +
             hub_head('Portable skills', hub) +
```
