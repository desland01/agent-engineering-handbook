# One handbook teaches ten useful changes

## Give each kind of page one job

### A lesson teaches one useful change

A lesson takes one problem from explanation to a change the reader can make and check.

Current example: “Stop fixing the same mistake twice” introduces the problem, while its recurring-failures guide supplies the method.

Recommendation: make the lesson the complete human reading unit, with its method and evidence together.

### A skill gives an agent reusable instructions

A skill contains instructions an agent loads for a matching task, with supporting examples and limits. Reading a lesson should never require installing one.

Current example: Output verification gives the agent an input contract, acceptance criteria and known failure cases.

Recommendation: keep Skills as a separate section and link each package to the lessons it helps apply.

### Guides become the lessons’ practical methods

A guide could serve an experienced reader who only needs steps, but this site’s guides and lessons teach the same changes. Their different lengths do not justify competing reading sequences.

Current example: “Find what a fresh agent actually misses” and “Write instructions that change agent behavior” both lead to the same knowledge-and-instructions guide.

Recommendation: absorb the guides into ten lessons, combining diagnosis with instruction writing and adding a dedicated recovery lesson.

### Sources explain where the advice comes from

Reference material supports a claim or answers a lookup question without becoming another course. Call the evidence section Sources, and keep agent-specific reference material beside its skill.

Current example: “Find a method for the failure you face” currently opens from Reference, although it lists guides.

Recommendation: replace Reference with Sources, leading to the investigations and their evidence.

### The header serves the main reading choices

The header carries the home link, Lessons, Skills and Sources because they answer where to start, learn, apply and inspect evidence. One More menu supplies direct links to individual pages and supporting material, with the same contents under Menu on narrow screens.

Current example: Task prompts and Adopting a skill already sit in More rather than competing with Lessons.

Recommendation: keep that split and make the single menu complete, using the plain labels below.

### GitHub belongs in the single menu

The current header and menu each link to the same repository, with no distinct destination or reader task. The markup confirms duplication but does not establish why it was introduced.

Current example: GitHub repository at the foot of More repeats the separate header repository link.

Recommendation: keep one GitHub repository link at the end of the menu and remove the separate header link.

### Supporting pages join their relevant sections

Handbook index joins Home, Task prompts stays beside Lessons, and Adopting a skill stays beside Skills. Investigations becomes the Sources landing page, containing the three inspections, while Validation, Frames and Video notes become plainly labelled evidence pages.

Current example: the nineteen idea pages already say they have moved into lessons, rather than presenting nineteen full articles.

Recommendation: retain those observations as qualified lesson citations with old links preserved, using the complete placements below.

## Every address has a clear destination

The header reads **Agent Engineering Handbook** (home), **Lessons**, **Skills**, **Sources**, then **More**. On narrow screens, the same native menu is labelled **Menu** and includes Home and the three section links. Keep the current colours, typography, borders, reading width, contents rail and native menu behaviour. This changes organisation and labels, not the design language.

The menu groups are **Start here**, **Lessons**, **Skills**, **Sources**, **Help**, **Source texts**, and **Earlier links**, in that order. Group labels are navigation labels, not article headings. Each tree entry below is a direct link in this one menu, using its displayed plain label. Home and the three section links appear first. Canonical articles follow in their section and lesson order. Source-text companions follow in Source texts. Every merged or redirected address follows in Earlier links, with “Earlier:” before its label. GitHub repository is the final, single external navigation link: https://github.com/desland01/agent-engineering-handbook.

This deliberately meets the strict visitor walk: even a companion text, an old address and the missing-page explanation can be opened using only the header and this menu. Earlier links are compatibility entries, never extra lessons or a second reading sequence. The trade-off is a longer menu. Put current reading choices first and keep the single native menu rather than creating another menu or hidden section. During later implementation, constrain that menu to the viewport, allow vertical scrolling and wrap long labels. The current menu has unbounded height and non-wrapping labels, so those usability adjustments are required without changing its visual language. Keep primary-source links inside articles separate from navigation.

The tree is the route specification. Indentation states each page’s parent, and the bracketed parent makes that ownership explicit. Paths are implementation details here, never proposed display labels. “Kept” retains the address and page role, allowing later approved copy changes. “Merged into X” transfers the useful content into X and requires a permanent redirect from the old address. “Redirects to X” preserves an address whose content is already represented elsewhere. Neither disposition permits deleting originals in this phase.

Preserve superseded source bytes through the project’s approved history or control archive in later authorised work. Keep existing incoming fragments meaningful through destination anchors or an explicit fragment mapping. Each idea receives the proposed anchor `video-note-NN` on its owning lesson, using the public filename number, not the extraction’s internal tip number. These anchors do not exist yet. Preserve the old idea section fragments there too. Markdown guide addresses lead to the owning lesson’s Markdown companion, so machine readers are not sent to an unrelated page type.

The file-backed tree covers the measured **126 existing served pages: 68 HTML and 58 Markdown**. Two proposed recovery addresses are marked new. The existing directory and extensionless aliases are listed separately within the same tree specification. No other new standalone page is proposed.

<!-- sitemap:start -->
- Home | `/index.html` | parent: `Site` | kept
  - Handbook overview | `/README.html` | parent: `/index.html` | merged into /index.html
  - Handbook overview — source text | `/README.md` | parent: `/index.html` | kept
  - Lessons | `/lessons.html` | parent: `/index.html` | kept
    - Methods by problem | `/guides.html` | parent: `/lessons.html` | merged into /lessons.html
    - Video observations | `/ideas.html` | parent: `/lessons.html` | redirects to /lessons.html
    - 01 You turn repeated mistakes into reliable checks | `/lessons/recurring-mistakes.html` | parent: `/lessons.html` | kept
      - 01 You turn repeated mistakes into reliable checks — source text | `/lessons/recurring-mistakes.md` | parent: `/lessons/recurring-mistakes.html` | kept
      - Turn recurring failures into checks | `/guides/01-recurring-failures.html` | parent: `/lessons/recurring-mistakes.html` | merged into /lessons/recurring-mistakes.html
      - Turn recurring failures into checks — source text | `/guides/01-recurring-failures.md` | parent: `/lessons/recurring-mistakes.html` | merged into /lessons/recurring-mistakes.md
      - Check repeated mistakes automatically | `/ideas/08-fix-class-loops.html` | parent: `/lessons/recurring-mistakes.html` | redirects to /lessons/recurring-mistakes.html#video-note-08
      - Weigh the cost of custom checks | `/ideas/09-custom-lint-economics.html` | parent: `/lessons/recurring-mistakes.html` | redirects to /lessons/recurring-mistakes.html#video-note-09
      - A worked example of a recurring check | `/examples/recurring-rule/README.html` | parent: `/lessons/recurring-mistakes.html` | kept
        - Recurring check example — source text | `/examples/recurring-rule/README.md` | parent: `/examples/recurring-rule/README.html` | kept
    - 02 You diagnose failed checks without copying logs | `/lessons/ci-feedback.html` | parent: `/lessons.html` | kept
      - 02 You diagnose failed checks without copying logs — source text | `/lessons/ci-feedback.md` | parent: `/lessons/ci-feedback.html` | kept
      - Diagnose failed checks | `/guides/04-ci-feedback.html` | parent: `/lessons/ci-feedback.html` | merged into /lessons/ci-feedback.html
      - Diagnose failed checks — source text | `/guides/04-ci-feedback.md` | parent: `/lessons/ci-feedback.html` | merged into /lessons/ci-feedback.md
      - Read failed check logs | `/ideas/01-ci-feedback-loop.html` | parent: `/lessons/ci-feedback.html` | redirects to /lessons/ci-feedback.html#video-note-01
    - 03 You test the result users actually need | `/lessons/prove-it-works.html` | parent: `/lessons.html` | kept
      - 03 You test the result users actually need — source text | `/lessons/prove-it-works.md` | parent: `/lessons/prove-it-works.html` | kept
      - Test the essential user journey | `/guides/02-critical-journey-tests.html` | parent: `/lessons/prove-it-works.html` | merged into /lessons/prove-it-works.html
      - Test the essential user journey — source text | `/guides/02-critical-journey-tests.md` | parent: `/lessons/prove-it-works.html` | merged into /lessons/prove-it-works.md
      - Define the accepted result | `/guides/09-verification-contracts.html` | parent: `/lessons/prove-it-works.html` | merged into /lessons/prove-it-works.html
      - Define the accepted result — source text | `/guides/09-verification-contracts.md` | parent: `/lessons/prove-it-works.html` | merged into /lessons/prove-it-works.md
      - Check the output through useful views | `/guides/13-layered-validation.html` | parent: `/lessons/prove-it-works.html` | merged into /lessons/prove-it-works.html
      - Check the output through useful views — source text | `/guides/13-layered-validation.md` | parent: `/lessons/prove-it-works.html` | merged into /lessons/prove-it-works.md
      - Test two participants together | `/ideas/02-two-browser-e2e.html` | parent: `/lessons/prove-it-works.html` | redirects to /lessons/prove-it-works.html#video-note-02
    - 04 You give agents a working preview | `/lessons/working-previews.html` | parent: `/lessons.html` | kept
      - 04 You give agents a working preview — source text | `/lessons/working-previews.md` | parent: `/lessons/working-previews.html` | kept
      - Make previews usable | `/guides/03-preview-workspaces.html` | parent: `/lessons/working-previews.html` | merged into /lessons/working-previews.html
      - Make previews usable — source text | `/guides/03-preview-workspaces.md` | parent: `/lessons/working-previews.html` | merged into /lessons/working-previews.md
      - Make previews accessible | `/ideas/04-preview-environments.html` | parent: `/lessons/working-previews.html` | redirects to /lessons/working-previews.html#video-note-04
    - 05 You make missing operations usable by agents | `/lessons/missing-tools.html` | parent: `/lessons.html` | kept
      - 05 You make missing operations usable by agents — source text | `/lessons/missing-tools.md` | parent: `/lessons/missing-tools.html` | kept
      - Build a missing tool operation | `/guides/06-tool-adapters.html` | parent: `/lessons/missing-tools.html` | merged into /lessons/missing-tools.html
      - Build a missing tool operation — source text | `/guides/06-tool-adapters.md` | parent: `/lessons/missing-tools.html` | merged into /lessons/missing-tools.md
      - Provide the missing upload operation | `/ideas/05-custom-file-upload-skill.html` | parent: `/lessons/missing-tools.html` | redirects to /lessons/missing-tools.html#video-note-05
      - Learn by testing a small skill | `/ideas/06-skill-authoring-reward.html` | parent: `/lessons/missing-tools.html` | redirects to /lessons/missing-tools.html#video-note-06
    - 06 You write instructions that fix observed confusion | `/lessons/useful-instructions.html` | parent: `/lessons.html` | kept
      - 06 You write instructions that fix observed confusion — source text | `/lessons/useful-instructions.md` | parent: `/lessons/useful-instructions.html` | kept
      - Find a fresh agent’s missing context | `/lessons/fresh-agent.html` | parent: `/lessons/useful-instructions.html` | merged into /lessons/useful-instructions.html
      - Find a fresh agent’s missing context — source text | `/lessons/fresh-agent.md` | parent: `/lessons/useful-instructions.html` | merged into /lessons/useful-instructions.md
      - Place useful project knowledge | `/guides/05-knowledge-and-instructions.html` | parent: `/lessons/useful-instructions.html` | merged into /lessons/useful-instructions.html
      - Place useful project knowledge — source text | `/guides/05-knowledge-and-instructions.md` | parent: `/lessons/useful-instructions.html` | merged into /lessons/useful-instructions.md
      - Make domain knowledge available | `/ideas/10-domain-knowledge-as-infra.html` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-10
      - Own instruction decisions | `/ideas/12-own-your-instructions.html` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-12
      - Distinguish steering from enforcement | `/ideas/13-steering-pushback.html` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-13
      - Reduce extra prompting | `/ideas/15-zero-context-docs.html` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-15
      - Observe a fresh agent’s missing context | `/ideas/16-minimal-context-calibration.html` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-16
      - Write guidance that steers decisions | `/ideas/17-steer-not-map.html` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-17
    - 07 You keep shared contracts consistent across layers | `/lessons/shared-contracts.html` | parent: `/lessons.html` | kept
      - 07 You keep shared contracts consistent across layers — source text | `/lessons/shared-contracts.md` | parent: `/lessons/shared-contracts.html` | kept
      - Connect shared contracts | `/guides/08-compose-contracts.html` | parent: `/lessons/shared-contracts.html` | merged into /lessons/shared-contracts.html
      - Connect shared contracts — source text | `/guides/08-compose-contracts.md` | parent: `/lessons/shared-contracts.html` | merged into /lessons/shared-contracts.md
      - Use one domain language and transport | `/guides/11-domain-language-and-agent-apis.html` | parent: `/lessons/shared-contracts.html` | merged into /lessons/shared-contracts.html
      - Use one domain language and transport — source text | `/guides/11-domain-language-and-agent-apis.md` | parent: `/lessons/shared-contracts.html` | merged into /lessons/shared-contracts.md
      - Connect types across layers | `/ideas/14-type-safe-composition.html` | parent: `/lessons/shared-contracts.html` | redirects to /lessons/shared-contracts.html#video-note-14
    - 08 You navigate unfamiliar code without guessing | `/lessons/codebase-navigation.html` | parent: `/lessons.html` | kept
      - 08 You navigate unfamiliar code without guessing — source text | `/lessons/codebase-navigation.md` | parent: `/lessons/codebase-navigation.html` | kept
      - Find code and preserve tool output | `/guides/10-codebase-navigation-and-tooling.html` | parent: `/lessons/codebase-navigation.html` | merged into /lessons/codebase-navigation.html
      - Find code and preserve tool output — source text | `/guides/10-codebase-navigation-and-tooling.md` | parent: `/lessons/codebase-navigation.html` | merged into /lessons/codebase-navigation.md
      - Find your way through growing code | `/ideas/19-solo-onboarding.html` | parent: `/lessons/codebase-navigation.html` | redirects to /lessons/codebase-navigation.html#video-note-19
    - 09 You resume work without repeating completed steps | `/lessons/resume-work.html` | parent: `/lessons.html` | new; proposed canonical page
      - 09 You resume work without repeating completed steps — source text | `/lessons/resume-work.md` | parent: `/lessons/resume-work.html` | new; proposed canonical page
      - Reuse finished work and recover interruptions | `/guides/12-artifact-identity-and-recovery.html` | parent: `/lessons/resume-work.html` | merged into /lessons/resume-work.html
      - Reuse finished work and recover interruptions — source text | `/guides/12-artifact-identity-and-recovery.md` | parent: `/lessons/resume-work.html` | merged into /lessons/resume-work.md
    - 10 You remove obstacles for the next contributor | `/lessons/better-environments.html` | parent: `/lessons.html` | kept
      - 10 You remove obstacles for the next contributor — source text | `/lessons/better-environments.md` | parent: `/lessons/better-environments.html` | kept
      - Learn from newcomer questions | `/guides/07-team-learning.html` | parent: `/lessons/better-environments.html` | merged into /lessons/better-environments.html
      - Learn from newcomer questions — source text | `/guides/07-team-learning.md` | parent: `/lessons/better-environments.html` | merged into /lessons/better-environments.md
      - Share useful automation | `/ideas/03-automation-multiplies-agents.html` | parent: `/lessons/better-environments.html` | redirects to /lessons/better-environments.html#video-note-03
      - Discuss useful tooling work | `/ideas/07-team-buy-in.html` | parent: `/lessons/better-environments.html` | redirects to /lessons/better-environments.html#video-note-07
      - Learn from newcomer questions | `/ideas/11-newcomer-questions-signal.html` | parent: `/lessons/better-environments.html` | redirects to /lessons/better-environments.html#video-note-11
      - Qualify the career argument | `/ideas/18-career-leverage.html` | parent: `/lessons/better-environments.html` | redirects to /lessons/better-environments.html#video-note-18
    - Task prompts | `/prompts.html` | parent: `/lessons.html` | kept
      - Task prompts — source text | `/prompts.md` | parent: `/prompts.html` | kept
  - Skills | `/skills.html` | parent: `/index.html` | kept
    - Adopt a skill | `/adoption.html` | parent: `/skills.html` | kept
      - Adopt a skill — source text | `/adoption.md` | parent: `/adoption.html` | kept
    - Artifact recovery | `/skills/agent-artifact-recovery/index.html` | parent: `/skills.html` | kept
      - Artifact recovery — agent instructions | `/skills/agent-artifact-recovery/SKILL.md` | parent: `/skills/agent-artifact-recovery/index.html` | kept
      - Artifact recovery — evaluation cases | `/skills/agent-artifact-recovery/eval/README.md` | parent: `/skills/agent-artifact-recovery/index.html` | kept
      - Artifact recovery — worked examples | `/skills/agent-artifact-recovery/references/implementation.md` | parent: `/skills/agent-artifact-recovery/index.html` | kept
      - Artifact recovery — source notes | `/skills/agent-artifact-recovery/references/source-patterns.md` | parent: `/skills/agent-artifact-recovery/index.html` | kept
    - Context calibration | `/skills/agent-context-calibration/index.html` | parent: `/skills.html` | kept
      - Context calibration — agent instructions | `/skills/agent-context-calibration/SKILL.md` | parent: `/skills/agent-context-calibration/index.html` | kept
      - Context calibration — worked examples | `/skills/agent-context-calibration/references/implementation.md` | parent: `/skills/agent-context-calibration/index.html` | kept
      - Context calibration — source notes | `/skills/agent-context-calibration/references/source-patterns.md` | parent: `/skills/agent-context-calibration/index.html` | kept
    - Contract consistency | `/skills/agent-contract-consistency/index.html` | parent: `/skills.html` | kept
      - Contract consistency — agent instructions | `/skills/agent-contract-consistency/SKILL.md` | parent: `/skills/agent-contract-consistency/index.html` | kept
      - Contract consistency — evaluation cases | `/skills/agent-contract-consistency/eval/README.md` | parent: `/skills/agent-contract-consistency/index.html` | kept
      - Contract consistency — worked examples | `/skills/agent-contract-consistency/references/implementation.md` | parent: `/skills/agent-contract-consistency/index.html` | kept
      - Contract consistency — source notes | `/skills/agent-contract-consistency/references/source-patterns.md` | parent: `/skills/agent-contract-consistency/index.html` | kept
    - Feedback engineering | `/skills/agent-feedback-engineering/index.html` | parent: `/skills.html` | kept
      - Feedback engineering — agent instructions | `/skills/agent-feedback-engineering/SKILL.md` | parent: `/skills/agent-feedback-engineering/index.html` | kept
      - Feedback engineering — worked examples | `/skills/agent-feedback-engineering/references/implementation.md` | parent: `/skills/agent-feedback-engineering/index.html` | kept
      - Feedback engineering — source notes | `/skills/agent-feedback-engineering/references/source-patterns.md` | parent: `/skills/agent-feedback-engineering/index.html` | kept
    - Output verification | `/skills/agent-output-verification/index.html` | parent: `/skills.html` | kept
      - Output verification — agent instructions | `/skills/agent-output-verification/SKILL.md` | parent: `/skills/agent-output-verification/index.html` | kept
      - Output verification — evaluation cases | `/skills/agent-output-verification/eval/README.md` | parent: `/skills/agent-output-verification/index.html` | kept
      - Output verification — worked examples | `/skills/agent-output-verification/references/implementation.md` | parent: `/skills/agent-output-verification/index.html` | kept
      - Output verification — source notes | `/skills/agent-output-verification/references/source-patterns.md` | parent: `/skills/agent-output-verification/index.html` | kept
    - Agent-ready workspaces | `/skills/agent-ready-workspaces/index.html` | parent: `/skills.html` | kept
      - Agent-ready workspaces — agent instructions | `/skills/agent-ready-workspaces/SKILL.md` | parent: `/skills/agent-ready-workspaces/index.html` | kept
      - Agent-ready workspaces — worked examples | `/skills/agent-ready-workspaces/references/implementation.md` | parent: `/skills/agent-ready-workspaces/index.html` | kept
      - Agent-ready workspaces — source notes | `/skills/agent-ready-workspaces/references/source-patterns.md` | parent: `/skills/agent-ready-workspaces/index.html` | kept
    - Tool adapters | `/skills/agent-tool-adapters/index.html` | parent: `/skills.html` | kept
      - Tool adapters — agent instructions | `/skills/agent-tool-adapters/SKILL.md` | parent: `/skills/agent-tool-adapters/index.html` | kept
      - Tool adapters — worked examples | `/skills/agent-tool-adapters/references/implementation.md` | parent: `/skills/agent-tool-adapters/index.html` | kept
      - Tool adapters — source notes | `/skills/agent-tool-adapters/references/source-patterns.md` | parent: `/skills/agent-tool-adapters/index.html` | kept
  - Sources | `/investigations.html` | parent: `/index.html` | kept
    - Theo’s projects: T3 Code and Melee | `/github-inspection.html` | parent: `/investigations.html` | kept
      - Theo’s projects: T3 Code and Melee — source text | `/github-inspection.md` | parent: `/github-inspection.html` | kept
    - Matt Pocock’s course video project | `/matt-pocock-inspection.html` | parent: `/investigations.html` | kept
      - Matt Pocock’s course video project — source text | `/matt-pocock-inspection.md` | parent: `/matt-pocock-inspection.html` | kept
    - Boris Cherny’s public projects | `/boris-cherny-inspection.html` | parent: `/investigations.html` | kept
      - Boris Cherny’s public projects — source text | `/boris-cherny-inspection.md` | parent: `/boris-cherny-inspection.html` | kept
    - What was checked | `/validation.html` | parent: `/investigations.html` | kept
      - What was checked — source text | `/validation.md` | parent: `/validation.html` | kept
    - Video frames | `/evidence.html` | parent: `/investigations.html` | kept
    - Video notes | `/evidence/video-research.html` | parent: `/investigations.html` | kept
      - Video notes — source text | `/evidence/video-research.md` | parent: `/evidence/video-research.html` | kept
    - Credits and reuse | `/ATTRIBUTION.html` | parent: `/investigations.html` | kept
      - Credits and reuse — source text | `/ATTRIBUTION.md` | parent: `/ATTRIBUTION.html` | kept
  - Contribute to the handbook | `/CONTRIBUTING.html` | parent: `/index.html` | kept
    - Contribute to the handbook — source text | `/CONTRIBUTING.md` | parent: `/CONTRIBUTING.html` | kept
  - Find a missing page | `/404.html` | parent: `/index.html` | kept
<!-- sitemap:end -->

The following are additional aliases, not additional physical pages. Skill directory forms are linked by the current site. Extensionless idea forms are explicit in the hosting configuration. Root is included as the expected home alias, an assumption about the hosting entry rather than an observed live route. Their delivery has not been checked live. Include these address links at the end of Earlier links in the same menu, so the strict visitor walk covers them too. Do not invent other extensionless routes.

<!-- aliases:start -->
- Home — short address | `/` | parent: `/index.html` | kept
- Find your way through growing code — earlier short address | `/ideas/19-solo-onboarding` | parent: `/lessons/codebase-navigation.html` | redirects to /lessons/codebase-navigation.html#video-note-19
- Qualify the career argument — earlier short address | `/ideas/18-career-leverage` | parent: `/lessons/better-environments.html` | redirects to /lessons/better-environments.html#video-note-18
- Write guidance that steers decisions — earlier short address | `/ideas/17-steer-not-map` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-17
- Observe a fresh agent’s missing context — earlier short address | `/ideas/16-minimal-context-calibration` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-16
- Reduce extra prompting — earlier short address | `/ideas/15-zero-context-docs` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-15
- Connect types across layers — earlier short address | `/ideas/14-type-safe-composition` | parent: `/lessons/shared-contracts.html` | redirects to /lessons/shared-contracts.html#video-note-14
- Distinguish steering from enforcement — earlier short address | `/ideas/13-steering-pushback` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-13
- Own instruction decisions — earlier short address | `/ideas/12-own-your-instructions` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-12
- Learn from newcomer questions — earlier short address | `/ideas/11-newcomer-questions-signal` | parent: `/lessons/better-environments.html` | redirects to /lessons/better-environments.html#video-note-11
- Make domain knowledge available — earlier short address | `/ideas/10-domain-knowledge-as-infra` | parent: `/lessons/useful-instructions.html` | redirects to /lessons/useful-instructions.html#video-note-10
- Weigh the cost of custom checks — earlier short address | `/ideas/09-custom-lint-economics` | parent: `/lessons/recurring-mistakes.html` | redirects to /lessons/recurring-mistakes.html#video-note-09
- Check repeated mistakes automatically — earlier short address | `/ideas/08-fix-class-loops` | parent: `/lessons/recurring-mistakes.html` | redirects to /lessons/recurring-mistakes.html#video-note-08
- Discuss useful tooling work — earlier short address | `/ideas/07-team-buy-in` | parent: `/lessons/better-environments.html` | redirects to /lessons/better-environments.html#video-note-07
- Learn by testing a small skill — earlier short address | `/ideas/06-skill-authoring-reward` | parent: `/lessons/missing-tools.html` | redirects to /lessons/missing-tools.html#video-note-06
- Provide the missing upload operation — earlier short address | `/ideas/05-custom-file-upload-skill` | parent: `/lessons/missing-tools.html` | redirects to /lessons/missing-tools.html#video-note-05
- Make previews accessible — earlier short address | `/ideas/04-preview-environments` | parent: `/lessons/working-previews.html` | redirects to /lessons/working-previews.html#video-note-04
- Share useful automation — earlier short address | `/ideas/03-automation-multiplies-agents` | parent: `/lessons/better-environments.html` | redirects to /lessons/better-environments.html#video-note-03
- Test two participants together — earlier short address | `/ideas/02-two-browser-e2e` | parent: `/lessons/prove-it-works.html` | redirects to /lessons/prove-it-works.html#video-note-02
- Read failed check logs — earlier short address | `/ideas/01-ci-feedback-loop` | parent: `/lessons/ci-feedback.html` | redirects to /lessons/ci-feedback.html#video-note-01
- Video observations — earlier short address | `/ideas` | parent: `/lessons.html` | redirects to /lessons.html
- Artifact recovery — directory address | `/skills/agent-artifact-recovery/` | parent: `/skills/agent-artifact-recovery/index.html` | kept
- Context calibration — directory address | `/skills/agent-context-calibration/` | parent: `/skills/agent-context-calibration/index.html` | kept
- Contract consistency — directory address | `/skills/agent-contract-consistency/` | parent: `/skills/agent-contract-consistency/index.html` | kept
- Feedback engineering — directory address | `/skills/agent-feedback-engineering/` | parent: `/skills/agent-feedback-engineering/index.html` | kept
- Output verification — directory address | `/skills/agent-output-verification/` | parent: `/skills/agent-output-verification/index.html` | kept
- Agent-ready workspaces — directory address | `/skills/agent-ready-workspaces/` | parent: `/skills/agent-ready-workspaces/index.html` | kept
- Tool adapters — directory address | `/skills/agent-tool-adapters/` | parent: `/skills/agent-tool-adapters/index.html` | kept
<!-- aliases:end -->

Task prompts keeps its reusable work orders and links to the matching lessons instead of guides. Adopt a skill retains installation and combination help, with the existing exercise. Sources owns the full inspections and their qualifications. What was checked retains dated validation records and separates them from future checks. Video frames keeps its twelve captions and limits. Video notes keeps the chronological extraction. Credits and reuse keeps attribution, licences and non-endorsement information. Contribute to the handbook retains contribution and local-build help. Handbook overview — source text remains the repository-facing overview, not a second human course index.

Images, structured evidence, package metadata, evaluation case data and executable example assets are supporting files rather than additional HTML or Markdown pages. Preserve their existing addresses and links in later implementation. The seven skill directory addresses continue to open their existing overview pages. Retain the missing-page handler’s error behaviour even though its explanation is directly discoverable.

## Ten lessons own all the teaching material

Each source item below has one content owner. Related lessons may link to it, but cannot become another owner of the same source page. This replaces the current overlapping catalog assignments. No lesson, guide or idea is dropped. The guide-derived recovery lesson has no independent video idea, so the landing page must stop promising that every lesson originated in a video moment.

The reading order has three groups: **Stop repeat work** (1–3), **Give agents what they need** (4–6), and **Keep work understandable and recoverable** (7–10). These are menu and index group labels, not additional pages. Each lesson teaches the one action named in its title, while detailed cases belong inside that action.

<!-- lessons:start -->

### You turn repeated mistakes into reliable checks

Lesson 01. Turn one observed recurrence into a check that rejects the mistake and permits the valid alternative. Keep the runnable import example, actual command integration, severity, exceptions and maintenance limits.

Current lessons:
- `lessons/recurring-mistakes.md` — Stop fixing the same mistake twice

Current guides:
- `guides/01-recurring-failures.md` — 01 — Convert recurring failures into permanent rules

Current ideas:
- `public/ideas/08-fix-class-loops.html` — Move recurring fixes from per-occurrence agent corrections into executable checks (lint rule, CI step, routine)
- `public/ideas/09-custom-lint-economics.html` — Custom lint rules became economical: agents lower the cost of the code and its tests

### You diagnose failed checks without copying logs

Lesson 02. Follow one failed check from the correct revision through readable logs, diagnosis and a verified repair. Keep the original failure, run identity, retry distinction and permission limits.

Current lessons:
- `lessons/ci-feedback.md` — Stop babysitting your agent's CI failures

Current guides:
- `guides/04-ci-feedback.md` — 04 — Let the agent read and resolve CI failures

Current ideas:
- `public/ideas/01-ci-feedback-loop.html` — Close the CI feedback loop: let the agent trigger CI and read failed logs itself

### You test the result users actually need

Lesson 03. Define and test one accepted result. Use the two-participant journey, incomplete-source verifier and compiler checks as different examples of false success, not three mandatory testing systems. Preserve distributed-output and minimum-runtime checks, seeded reproduction, meaningful baselines, comparable benchmarks and inspection of the actual final gate.

Current lessons:
- `lessons/prove-it-works.md` — Passing tests can still hide broken software

Current guides:
- `guides/02-critical-journey-tests.md` — 02 — One critical journey test beats broad shallow coverage
- `guides/09-verification-contracts.md` — 09: Verification contracts
- `guides/13-layered-validation.md` — 13 — Validate the output through several useful views

Current ideas:
- `public/ideas/02-two-browser-e2e.html` — Design tiny two-actor end-to-end tests that catch whole classes of failure

### You give agents a working preview

Lesson 04. Make one preview reachable, identifiable and testable from the agent’s real starting environment. Keep setup selection, separate mutable state, served revision, lifecycle and consumer-readable evidence.

Current lessons:
- `lessons/working-previews.md` — Give every agent a working preview

Current guides:
- `guides/03-preview-workspaces.md` — 03 — Make previews usable from the agent's environment

Current ideas:
- `public/ideas/04-preview-environments.html` — Preview environments matter more now that code is built outside your machine

### You make missing operations usable by agents

Lesson 05. Bridge one demonstrated capability gap through the smallest supported interface. Preserve reuse-before-building, credentials through existing configuration, useful errors, bounded effects and a real invocation by the intended agent.

Current lessons:
- `lessons/missing-tools.md` — Give your agent the tool it's missing

Current guides:
- `guides/06-tool-adapters.md` — 06 — Build small tool adapters for capability gaps

Current ideas:
- `public/ideas/05-custom-file-upload-skill.html` — Build small tool adapters for things the CLI cannot do (video/asset uploads to PRs)
- `public/ideas/06-skill-authoring-reward.html` — Authoring and testing a small skill has a tight, low-stakes feedback loop

### You write instructions that fix observed confusion

Lesson 06. Observe one misunderstanding, place the missing decision where it is needed, and confirm the next attempt receives it. Diagnosis and writing are one loop. Preserve cold-start safeguards, human decisions and reasons, native loading, source-derived updates and the difference between steering and enforcement.

Current lessons:
- `lessons/useful-instructions.md` — Write instructions that change agent behavior
- `lessons/fresh-agent.md` — Find what a fresh agent actually misses

Current guides:
- `guides/05-knowledge-and-instructions.md` — 05 — Put project knowledge where the next task needs it

Current ideas:
- `public/ideas/10-domain-knowledge-as-infra.html` — Encode domain knowledge as infrastructure so newcomers' agents get steered too
- `public/ideas/12-own-your-instructions.html` — Write your CLAUDE.md / AGENTS.md yourself; watch agent behavior and adjust
- `public/ideas/13-steering-pushback.html` — Use steering files to make the agent say no (and to get fast feedback when things go wrong)
- `public/ideas/15-zero-context-docs.html` — Write Claude.mds, review.mds, skills, and docs so agents work with zero prompting context
- `public/ideas/16-minimal-context-calibration.html` — Calibrate from a cold start: run minimal prompts first, add context only where it fails
- `public/ideas/17-steer-not-map.html` — Instruction files should steer toward success, not list where things are

### You keep shared contracts consistent across layers

Lesson 07. Trace one domain object through its authoritative definition and all consumers. Keep domain vocabulary, durable decisions, one transport, typed errors, compatibility, runtime validation and separately checked authorization. Preserve the machine-suitability and static-dependency limits.

Current lessons:
- `lessons/shared-contracts.md` — One shared contract prevents mismatched code

Current guides:
- `guides/08-compose-contracts.md` — Keep contracts consistent across the application
- `guides/11-domain-language-and-agent-apis.md` — How to keep one domain language and one transport when an agent calls your API

Current ideas:
- `public/ideas/14-type-safe-composition.html` — Compose layers so type safety runs end to end — and expect that click more often now

### You navigate unfamiliar code without guessing

Lesson 08. Find the code responsible for one requested behavior and confirm the map leads there. Preserve dependency direction and context generation, including guide 10’s safe-tool half: check compiler and symbol failures, report missing dependencies and preserve prior useful output on failed regeneration. Link to the adapter lesson for general tool design without assigning this guide twice.

Current lessons:
- `lessons/codebase-navigation.md` — Stop getting lost in your own code

Current guides:
- `guides/10-codebase-navigation-and-tooling.md` — 10: Codebase navigation and tooling

Current ideas:
- `public/ideas/19-solo-onboarding.html` — Solo projects now exceed your own comprehension — build systems so you and your agents don't get lost

### You resume work without repeating completed steps

Lesson 09. Reconcile interrupted work before deciding what to reuse or repeat. Preserve recipe versus byte identity, measured completeness, stale same-size digest caches, immutable reuse plans, recorded stage/session identity, safe fallback from missing receipts and separate repair of malformed summaries. A read-only extraction prompt is not an enforced execution boundary.

Current lessons:
- None. This lesson comes from the existing recovery guide.

Current guides:
- `guides/12-artifact-identity-and-recovery.md` — How to make pipeline artifacts reusable, resumable and honestly complete

Current ideas:
- None. Do not manufacture a video origin.

### You remove obstacles for the next contributor

Lesson 10. Use an observed contributor obstacle to choose one shared improvement and compare the next equivalent attempt. Keep newcomer questions as evidence rather than a quota, comparable before/after work, and the video’s qualified tooling and career opinions. Link to the relevant method lesson rather than reteaching its implementation.

Current lessons:
- `lessons/better-environments.md` — Improve the environment your agents work in

Current guides:
- `guides/07-team-learning.md` — 07 — Turn newcomer questions into improvements

Current ideas:
- `public/ideas/03-automation-multiplies-agents.html` — Infra and DX automation now speeds up every agent, not just you
- `public/ideas/07-team-buy-in.html` — Teams are now more willing to fund tooling time — use it
- `public/ideas/11-newcomer-questions-signal.html` — Treat newcomer questions as a signal for onboarding gaps (Theo's dumb-questions practice)
- `public/ideas/18-career-leverage.html` — Building environments where code lands well is a career-level skill (with a grain of salt)

<!-- lessons:end -->

Instruction diagnosis moves into lesson 6 because it is the first step of deciding what to write and where. Recovery receives lesson 9 because accepting a finished result and resuming an interrupted process are different decisions. Newcomer questions move into lesson 10 with their team-learning guide. Navigation keeps the current navigation lesson and its technical guide, while linking to that contributor-feedback loop where relevant.

The skills remain seven independently selectable packages. Feedback engineering supports lessons 1–2, Agent-ready workspaces supports lesson 4, Tool adapters supports lesson 5, Context calibration supports lesson 6, Contract consistency supports lesson 7, Output verification supports lesson 3, and Artifact recovery supports lesson 9. Lessons 8 and 10 may link to those packages only when a specific task fits. No new skill package or evaluation result is implied.

## Primary sources carry each lesson’s claims

These are the sources each lesson must cite, selected from the existing inspections and video notes. Source resolution belongs to the later authorised research phase. Timestamps below already appear in the inspected evidence. Repository paths and pull-request numbers identify existing citation targets, but unverified line or section anchors remain unresolved. Do not invent them or describe an unfetched link as checked.

Theo Browne’s video is the primary source for his narration. Where he reads Boris Cherny’s advice, attribute it as “Boris Cherny, quoted by Theo Browne” at that video moment. The inspected material does not supply a verified canonical URL for Boris’s original post. Repositories associated with a person do not establish that person’s authorship of every change. Later repository work does not prove what existed during filming.

### Repeated mistakes need a demonstrated check

For lesson 1, cite:

- **Boris Cherny, quoted by Theo Browne — video**, [08:02](https://www.youtube.com/watch?v=xmGY276gEFY&t=482s), for moving repeated corrections into checks. The extraction’s segment starts at 08:00, which explains the current alias’s slightly earlier time.
- **Theo Browne — video**, [08:30](https://www.youtube.com/watch?v=xmGY276gEFY&t=510s), for the argument that custom checks became cheaper to build. This is an economic argument, not measured savings.
- **Theo Browne’s T3 Code project and its contributors — repository pull request**, [T3 Code #7209](https://github.com/pingdotgg/t3code/pull/7209), with the [pinned tooltip rule](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/oxlint-plugin-t3code/rules/no-native-title-tooltip.ts), for one narrow implemented check. Resolve anchors for its configured invocation, fixtures and exceptions before making a coverage claim.

Selection evidence: the Theo inspection and video notes. Keep static-pattern limits and distinguish the handbook’s historical local import fixture from a new run.

### Failed checks need the correct run

For lesson 2, cite:

- **Theo Browne, reading Blacksmith’s sponsor message — video**, [01:53](https://www.youtube.com/watch?v=xmGY276gEFY&t=113s), for the manual log-copying loop. Keep the sponsorship label beside this citation and leave speed and price claims unverified.
- **Theo Browne’s T3 Code project and its contributors — repository pull request**, [T3 Code #8250](https://github.com/pingdotgg/t3code/pull/8250), for an implementation case about unnecessary build dependencies. Use only the relevant diff and author-reported evidence after anchor resolution. It does not demonstrate an agent completing the whole feedback loop.

Selection evidence: the Theo inspection and video notes. Present the full diagnosis procedure as the handbook’s method, not a reproduced sponsor demonstration.

### Output checks must catch false success

For lesson 3, cite:

- **Theo Browne — video**, [03:46](https://www.youtube.com/watch?v=xmGY276gEFY&t=226s), for his two-browser Twitch recollection. The original test source was not found in the inspected material.
- **Theo Browne’s Melee fork and its contributors — repository code and repair commit**, [the original verifier commit](https://github.com/doldecomp/melee/commit/035d9711623a32fbe891cffdcf44a91a550c1947) and [the completeness repair](https://github.com/t3dotgg/melee4mac/commit/74e73873038b821bbc46b0a18434e6b7cb556c0e), for the difference between matching output and complete source work. Resolve the code and test anchors for each claimed failure case.
- **Boris Cherny’s compiler project and its contributors — repository workflow**, [the pinned final gate at line 170](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml#L170), with its [fuzz](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/fuzz/README.md), [conformance](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/test/conformance/README.md) and [benchmark notes](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/bench/README.md), for selecting useful checks and inspecting what the final gate requires.

Selection evidence: the Theo and Boris inspections and video notes. The recorded Melee tests used mocked builds and synthetic bytes. They establish no gameplay result. The compiler suites were not run here, and separate branch protection remains unverified.

### Previews must work where agents start

For lesson 4, cite:

- **Theo Browne — video**, [05:06](https://www.youtube.com/watch?v=xmGY276gEFY&t=306s), for why previews matter when work happens outside one developer’s machine. The video does not demonstrate a complete preview deployment.
- **Theo Browne’s T3 Code project and its contributors — repository pull requests**, [#5586](https://github.com/pingdotgg/t3code/pull/5586), [#10501](https://github.com/pingdotgg/t3code/pull/10501) and [#10572](https://github.com/pingdotgg/t3code/pull/10572), for launcher configuration, usable browser evidence and transferring evidence to the agent’s environment. Resolve each claim to its relevant diff or recorded result.

Selection evidence: the Theo inspection and video notes. These later changes are supporting implementation cases, not evidence of the filmed setup. Author-reported transfers were not repeated in this task.

### A tool must perform the missing operation

For lesson 5, cite:

- **Theo Browne — video**, [05:52](https://www.youtube.com/watch?v=xmGY276gEFY&t=352s), the visible instruction example at [06:23](https://www.youtube.com/watch?v=xmGY276gEFY&t=383s), and his experience at [06:30](https://www.youtube.com/watch?v=xmGY276gEFY&t=390s). Distinguish the reported upload gap, the visible interface and subjective satisfaction.
- **Theo Browne’s T3 Code project and its contributors — repository pull request**, [#10501](https://github.com/pingdotgg/t3code/pull/10501), for returning browser output an agent can use.
- **Boris Cherny — repository contribution**, [Claude Code #16549](https://github.com/anthropics/claude-code/pull/16549), for the merged example of narrowing an operation. Resolve the bounded script’s diff anchor before citing its actual limits.

Selection evidence: the Theo and Boris inspections and video notes. No upload service source or successful invocation log was found. The open Melee screenshot proposal is corroborating host evidence only, not proof of an upload implementation or merged feature.

### Observed confusion guides instruction changes

For lesson 6, cite:

- **Boris Cherny, quoted by Theo Browne — video**, [09:56](https://www.youtube.com/watch?v=xmGY276gEFY&t=596s) and [14:33](https://www.youtube.com/watch?v=xmGY276gEFY&t=873s), for shared knowledge and reducing extra prompting. Preserve Theo’s disagreement with stronger claims.
- **Theo Browne — video**, [12:29](https://www.youtube.com/watch?v=xmGY276gEFY&t=749s), [13:03](https://www.youtube.com/watch?v=xmGY276gEFY&t=783s), [16:02](https://www.youtube.com/watch?v=xmGY276gEFY&t=962s) and [16:38](https://www.youtube.com/watch?v=xmGY276gEFY&t=998s), for ownership, steering, calibration and useful guidance. Minimal context means less extra explanation, never removed safeguards.
- **Matt Pocock’s Course Video Manager and its contributors — repository glossary**, [the pinned domain context](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/CONTEXT.md), with [proposal #1591](https://github.com/mattpocock/course-video-manager/pull/1591), for durable vocabulary and proposed placement changes. Resolve the relevant glossary and proposal anchors. The proposal was open at inspection.
- **Theo Browne’s T3 Code project and its contributors — repository pull request**, [#9128](https://github.com/pingdotgg/t3code/pull/9128), for checking actual native skill delivery rather than assuming a file is loaded.

Selection evidence: the Theo and Matt inspections and video notes. Do not promise measured context savings, universal readiness, or enforcement from prose.

### Shared contracts need separately checked guarantees

For lesson 7, cite:

- **Theo Browne — video**, [13:51](https://www.youtube.com/watch?v=xmGY276gEFY&t=831s), for his account of type-safe composition. His chosen frameworks are examples, not requirements.
- **Theo Browne’s T3 Code project and its contributors — repository code**, [the pinned shared contract](https://github.com/pingdotgg/t3code/blob/6c583620ff7ad3235b135af7107c0543467eecfa/packages/contracts/src/rpc.ts), for a concrete shared interface. Resolve the schema and consumer anchors for the chosen example.
- **Matt Pocock’s Course Video Manager and its contributors — repository pull request and code**, [the one-transport change](https://github.com/mattpocock/course-video-manager/pull/1542), [the derived client](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/rpc-layer.ts) and [the machine-suitability guard](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/cli/local-only.ts). Resolve the specific contract, error and guard anchors.

Selection evidence: the Theo and Matt inspections and video notes. Keep types, runtime validation, authentication, authorization and machine suitability distinct. Source inspection did not execute the app or its tests.

### Navigation starts with the requested behavior

For lesson 8, cite:

- **Theo Browne — video**, [18:00](https://www.youtube.com/watch?v=xmGY276gEFY&t=1080s), for his experience of navigating a growing solo project. It provides no measured speedup.
- **Theo Browne’s Melee fork and its contributors — repository pull requests**, [tooling #5](https://github.com/t3dotgg/melee4mac/pull/5), [output preservation #6](https://github.com/t3dotgg/melee4mac/pull/6) and [dependency correction #7](https://github.com/t3dotgg/melee4mac/pull/7). Resolve a task-to-code anchor and each relevant failure-handling diff.

Selection evidence: the Theo inspection and video notes. Keep the map’s limits and tool failure behaviour without turning this into a second adapter-design lesson.

### Recovery preserves work that already succeeded

For lesson 9, cite:

- **Matt Pocock’s Course Video Manager and its contributors — repository architecture decision**, [the pinned byte-identity decision](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/docs/adr/0027-byte-hash-decides-the-send.md), with [repair #1564](https://github.com/mattpocock/course-video-manager/pull/1564) and [immutable submission #1501](https://github.com/mattpocock/course-video-manager/pull/1501), for deciding what can be reused.
- **Matt Pocock’s Course Video Manager and its contributors — repository code**, [the duration check](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/export-duration-check.ts) and [digest record](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/apps/local/app/services/export-sha256-sidecar.ts), for completeness and stale-record limits.
- **Matt Pocock’s Course Video Manager and its contributors — repository code and tests**, [the extraction wrapper](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-extraction.ts), [retry wrapper](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-retry.ts) and [tests](https://github.com/mattpocock/course-video-manager/blob/4c1f3f5d49417e54b185bfe737b1e1a56f29c7b8/.sandcastle/run-with-extraction.test.ts), for recovering a summary separately from productive work.

Selection evidence: the Matt inspection. Resolve section and code anchors for the identity decision, duration policy, cache freshness and inherited tool options. There is no independent video source for this lesson. The source’s tolerances are local choices, and extraction wording does not mechanically prevent repeated effects. No recovery pipeline was executed here.

### Contributor friction identifies a useful improvement

For lesson 10, cite:

- **Boris Cherny, quoted by Theo Browne — video**, [04:47](https://www.youtube.com/watch?v=xmGY276gEFY&t=287s), for the shared-automation argument.
- **Theo Browne — video**, [07:28](https://www.youtube.com/watch?v=xmGY276gEFY&t=448s), [11:14](https://www.youtube.com/watch?v=xmGY276gEFY&t=674s) and [16:54](https://www.youtube.com/watch?v=xmGY276gEFY&t=1014s), for tooling support, newcomer questions and the explicitly speculative career argument. Do not adopt a question quota or promise promotion.
- **Theo Browne’s T3 Code project and its contributors — repository pull request**, [#2928](https://github.com/pingdotgg/t3code/pull/2928), for an example of removing shared testing friction. Resolve the changed dependency and evidence anchors before citing its effect.

Selection evidence: the Theo inspection and video notes. The proposed comparable before/after exercise is the handbook’s recommendation, not a measured outcome of this Phase 1 task.

This plan selects the structure and existing citation targets only. It does not set the later lesson standard, collect new sources, write replacement lessons, change the site, or approve the next phase. The requested layout check failed on the unchanged snapshot’s extra files, as recorded in [the evidence](EVIDENCE.md). The plan is ready for your decision, while that acceptance check remains unmet.
