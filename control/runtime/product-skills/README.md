# Product skills: the third category, shipped 2026-09-12

Owner rule: `~/.nautilus/architect/ARCHITECT.md`, "Product skills remain uncapped and
manufacturer-controlled", as amended by the owner's later requirement of **three separate
allowances of 50**: core 50, domain 50, product 50, counted and limited independently with
no borrowing. The earlier uncapped (`allowance.product: null`) implementation described in
previous versions of this file was never shipped and has been replaced.

## What is selected right now

Selected runtime: `~/.nautilus/releases/product-skills-50`, release digest
`6ab9f84288dd74870fea6bdd962e39e56d2b2e94740d61986acd0ecae13e3342`.
Counts: core 50, domain 26, product 8.

Retained for recovery, newest first:

- `~/.nautilus/releases/local-20260912171349807-240a28f7` — the same code, before the
  product tier was published. Digest `496646e90c435c43ba33f52a0d83cae0c862ff2209b6a683e6ed59d86e64552a`.
- `~/.nautilus/releases/design-assets-both` — the predecessor, unchanged.
  Digest `b08ef47e7011a0a70dc50d0df04195efcbb3ca66f0bfaa1b54295207219a4b2e`.

## What is in this directory

- `product-skills.patch` — the complete shipped change, 14 files: six `src/` modules
  against the `design-assets-both` release source, `scripts/prepare-product-skills.py`,
  and seven test files. Apply from the runtime repository root.
- `product-skills.test.ts` — the 21 tests for the third category.
- `prepare-product-skills.py` — the only path that installs a product tier into a release.
- `provenance.json` — the record now installed in the selected release: Higgsfield, eight
  skills, pinned at `fb18134b4aabe99c4bf7ff01c8f4883400efc80d`.

## What the change does

- `skill-capacity.ts` — tier `product` between domain and business. Its limit is an
  ordinary declared integer; a tier with no declared limit throws `allowance_missing_limit`.
  There is no uncapped path anywhere.
- `skill-scrutiny.ts` — `nautilus-product:<name>`, category `product` and `manufacturer`
  authority are bound together; any one without the others is `scrutiny_authority_mismatch`.
  Each category hard-stops at its own 50. Manufacturer skills sit outside the 36 to 50
  review band and never require authoring evidence, because their bytes are bound upstream.
- `skill-package.ts` — `charts/product-skills` and the `nautilus-product` plugin.
  `allowance.product` must be exactly 50; `null`, absent-with-bundles and any other number
  are refused as `policy_invalid`. `productBundleDigest()` hashes the sorted list of every
  sealed file in a bundle, so one changed byte in any file refuses the release with
  `product_skill_modified`. A product tier under a version-1 or version-2 policy refuses
  with `product_requires_classification`. The legacy version-1 policy path is untouched.
- `native-skill-configuration.ts` — projects the product plugin and resolves
  `nautilus-product:*` bodies for capsules.
- `skill-derived-documents.ts` — reports the product count in its own category, outside
  the core and domain counts.
- `skill-publication.ts` — `charts/product-skills/` is a publication surface; rosters
  never carry a manufacturer authority.
- `prepare-product-skills.py` — merges rather than wipes. Adding a second manufacturer
  preserves every other manufacturer's bundles, catalog group, provenance entries and pins.
  The earlier version deleted the whole product directory first; that defect was found and
  fixed test-first.

## Verified on the selected release, not asserted

- Installed bundles are byte-identical to upstream `fb18134b`, checked with `diff -rq`
  against a clean pinned checkout of `https://github.com/higgsfield-ai/skills.git`.
- Admission of the live release: core 50, domain 26, product 8.
- One changed byte in a vendor `SKILL.md` refuses with `product_skill_modified`.
- One changed byte in a vendor *reference* file refuses the same way.
- Relabelling a manufacturer skill as domain refuses with `policy_invalid`.
- `allowance.product` set to 51, or to `null`, refuses with `policy_invalid`.
- The native configuration projects `nautilus-core@1.0.0` and `nautilus-product@fb18134b4aab`,
  84 skills in all, and resolves a capsule body for `nautilus-product:higgsfield-generate`
  whose sha256 equals the shipped `SKILL.md` on disk. An uninstalled product id refuses
  with `capsule_required_chart_unresolvable`.
- Test suites across the blast radius: 253 passing. `product-skills` 21/0,
  `skill-package` 33/0 including the installed-vendor readback, `skill-capacity` 22/0,
  `skill-scrutiny` 16/0, `skill-derived-documents` 26/0, `skill-package-release` 8/0,
  `skill-admission-v3-publication` 14/0, `skill-publication-review` 10/0,
  `skill-publication-recovery` 13/0, `skill-review-evidence` 19/0, `release` 8/0.
- Typecheck introduces zero new diagnostics and removes 23. No diagnostic is in `src/`.

## Two suites fail for reasons that predate this change

Both were confirmed to fail identically on the unmodified `design-assets-both` release.

- `install-release-inputs` — `prior_source_mismatch` on
  `gsp-service-copy:validator-inputs/project-locations.json`. The test mutates
  `project-locations.json`, which a real project in this release binds as a validator
  input. It passes against a development tree that carries no such project.
- `native` — `invalid_installation_home`. The suite needs a full installation home.

## Open decision for the owner: which upstream commit to pin

The Anchor names `fb18134b4aabe99c4bf7ff01c8f4883400efc80d`, and that is what is installed.
Upstream has moved on to `d071406147a37b835bed09543d85ab3e9bd85c7d`. Seven of the eight
bundles are byte-identical between the two commits; `higgsfield-generate` differs. Moving
to the newer commit is a re-sync, which the rules allow when it is recorded, but it was not
requested, so it was not done. Say the word and it is one run of the preparer plus a
publication.
