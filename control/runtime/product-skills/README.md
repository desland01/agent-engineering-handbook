# Product skills: the third category, implemented 2026-09-10

Owner rule: `~/.nautilus/architect/ARCHITECT.md`, "Product skills — a third category". This
directory is the deliverable for the Nautilus runtime; it lives here because the runtime
source tree at `~/Documents/Codex/2026-09-04/ca/outputs/nautilus` had 5,465 dirty files
belonging to another session, and nothing here writes into it.

## What is in this directory

- `product-skills.patch` — `git diff` against a snapshot of that working tree's `src/`,
  `tests/` and `scripts/` taken 2026-09-10 (its skill modules were byte-identical to the
  deployed release). 10 files, +412/−39. Apply from the runtime repo root with
  `git apply <path>/product-skills.patch`.
- `product-skills.test.ts` — the thirteen tests, written before the change.
- `prepare-product-skills.py` — the only path that installs a product tier into a release.
- `provenance-fb18134b.json` — the provenance record the preparer wrote for the eight
  Higgsfield skills at upstream commit `fb18134b4aabe99c4bf7ff01c8f4883400efc80d`.

## What the change does

- `skill-capacity.ts` — tier `product` between domain and business; its allowance is
  `null` and only `null` (`product_uncapped` otherwise); counted, never limited.
- `skill-scrutiny.ts` — `nautilus-product:<name>` namespace, category `product`, authority
  `manufacturer`, each bound to the others (`scrutiny_authority_mismatch`); counted in its
  own category; never reviewed for the 36+ band, never authored locally.
- `skill-package.ts` — `charts/product-skills` folder and `nautilus-product` plugin;
  optional `productSkills` block in the version-2/3 policy with `manufacturer`,
  `repository` (https), `commit` (40-hex) and `contentDigest`; `productBundleDigest()` =
  sha256 of the sorted `[relative path, sealed sha256]` list over every file in the
  bundle; admission refuses `product_skill_modified` when the sealed bytes differ from
  the pinned digest; `product_requires_classification` for a product folder under a
  version-1 policy.
- `native-skill-configuration.ts` — projects the product plugin and resolves
  `nautilus-product:*` bodies for capsules.
- `skill-derived-documents.ts` — reports the product count as outside both caps.
- `skill-publication.ts` — rosters never carry a manufacturer authority.
- Existing tests: four count expectations gain `product: 0`; the tier-list expectation
  gains `'product'`. No check was weakened.

## Verified

- New suite 13/13. `skill-scrutiny` 16/16, `skill-package` 32/32,
  `skill-derived-documents` 23/23, `skill-capacity` 21/22 — the one failure predates the
  change (it reads a `completion/` evidence file outside the snapshot). `tsc --noEmit` clean.
- On the real release tree with the preparer applied: policy version 3 with eight
  `productSkills`; classifications core 50 / domain 14 / product 8; inventory 72; plugins
  `nautilus-core` and `nautilus-product`; capsule bodies resolve for
  `nautilus-product:higgsfield-generate`. Appending one comment line to a vendor
  `SKILL.md` refuses the whole release with `product_skill_modified`.
- The content-size limits (`skill-content.ts`) match only `charts/(core|business)-skills`,
  so vendor bytes (1.27 MB, one bundle of 796 KB) are outside them; pinned by a test and by
  running the declaration check on the real tree (library 1,199,401 bytes, core only).
- The installed `.agents/skills/higgsfield-*` copies are byte-identical to upstream
  `fb18134b` — proven with `diff -rq` against a fresh clone.

## Not done here, and why

**Shipping it.** A runtime release is runtime code plus release content. The code change
needs the runtime rebuilt (`npm run build`) and installed, then a publication through
`nautilus skill-publish --proposal <tree> --destination <release>` from the *current*
runtime, then `activate`/`switchover`. That is the other session's tree, the live runtime,
and a `current` symlink that moved four times today. Apply the patch there, run the
preparer with `--apply`, and publish. Nothing in the patch changes the publication path
for core or domain skills.

## The `copy` skill — readopt whole

`~/.agents/skills/copy` is the owner's own local-service copy method (lifecycle: rewritten
2026-08-14). It is a **domain** skill, not a product skill, and it goes in whole: `SKILL.md`
(16,169 bytes / 196 lines; limits 32,768 / 500), `references/` (6) and `templates/` (3),
108 KB — within the 256 KB bundle limit and the 2 MB library (core 1,796 KB + 108 KB).
Excluded as not part of the skill: `.remember/` (memory-hook cache), `.DS_Store`,
`SKILL.md.predesc`. The verbatim bundle is staged at
`scratchpad/copy-proposal/charts/core-skills/bundles/copy/` with `sourceHash(SKILL.md)`
`55f6d514…bfd81b1`. It carries ten absolute paths into `~/.claude` and `~/.agents`, kept as
they are per instruction.

Adding a publisher domain skill is governed: `assessSkillChange` requires **authoring
evidence** — a completed native run on the claude adapter inside the current runtime's
`var/workspaces`, with `nautilus-core:precise` and `nautilus-core:create-skill` delivered,
referenced by run id and task digest in the `--evidence` file's `authoring` array. Domain
would go 17 → 18, below the 35 target, so no review is required. The proposal tree needs:
the bundle; a `catalog.json` entry `{name: copy, entrypoint: bundles/copy/SKILL.md}`;
`publisherSkills["nautilus-core:copy"] = {category: domain, updateAuthority: publisher}`;
and `purposes["nautilus-core:copy"]` = the frontmatter description verbatim. It coexists
with `nautilus-core:local-service-copy`, which is a different, shorter document.
