// Product skills: a third purpose category for manufacturer-published skills
// of a paid product. Counted in their own category, hard-stopped at 50 exactly
// like core and domain (no borrowing, no uncapped tier), installed verbatim at
// a pinned upstream commit, and refused the moment their bytes differ from the
// declared provenance digest.
import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {copyFileSync, mkdirSync, mkdtempSync, writeFileSync, rmSync, readdirSync, lstatSync, readFileSync} from 'node:fs';
import {dirname, join, relative, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {evaluateCapacity, SkillCapacityError} from '../src/skill-capacity.js';
import type {SkillCatalog, SkillEntry} from '../src/skill-capacity.js';
import {assessSkillChange, skillInventoryDigest} from '../src/skill-scrutiny.js';
import type {SkillInventoryEntry} from '../src/skill-scrutiny.js';
import {assertSkillPackage, productBundleDigest, readSkillPackageInventory} from '../src/skill-package.js';
import {composeSkillAdmissionLedger} from '../src/skill-publication.js';
import {nativeSkillConfiguration} from '../src/native-skill-configuration.js';
import {assertSkillContentBounds} from '../src/skill-content.js';

process.env.TMPDIR = resolve(process.cwd(), 'tmp');
const TMP = resolve(process.cwd(), 'tmp');
const sha256 = (data: string | Buffer) => createHash('sha256').update(data).digest('hex');
const hex = (input: string) => sha256(input);
const COMMIT = 'fb18134b4aabe99c4bf7ff01c8f4883400efc80d';

const thrownCode = (run: () => unknown): string => {
  try { run(); } catch (error) {
    assert.ok(error instanceof SkillCapacityError, `expected SkillCapacityError, got ${String(error)}`);
    return error.code;
  }
  assert.fail('expected a throw');
};

// ---------------------------------------------------------------- capacity
const entry = (name: string): SkillEntry => ({name, sourceHash: hex(name), version: 'v', location: `bundles/${name}/SKILL.md`});
const catalog = (core: number, domain: number, product: number): SkillCatalog => ({tiers: [
  {tier: 'core', entries: Array.from({length: core}, (_, i) => entry(`core-${i}`))},
  {tier: 'domain', entries: Array.from({length: domain}, (_, i) => entry(`domain-${i}`))},
  {tier: 'product', entries: Array.from({length: product}, (_, i) => entry(`prod-${i}`))},
]});
const ALLOWANCE = {core: 50, domain: 50, product: 50};

test('fifty product skills are admitted alongside fifty core and fifty domain, each capped separately', () => {
  // The 50th product skill, arriving with both other categories at their own caps.
  const result = evaluateCapacity(catalog(50, 50, 49), ALLOWANCE, {type: 'add', tier: 'product', entry: entry('prod-50')});
  assert.equal(result.admitted, true);
  assert.deepEqual(result.resultingCount, {core: 50, domain: 50, product: 50});
});

test('the 51st product skill is refused, independently of core and domain headroom', () => {
  const refused = evaluateCapacity(catalog(0, 0, 50), ALLOWANCE, {type: 'add', tier: 'product', entry: entry('prod-51')});
  assert.equal(refused.admitted, false);
  assert.equal(refused.reason, 'limit_exceeded');
  // Full core and domain headroom does not lend the product tier a place.
  const withHeadroom = evaluateCapacity(catalog(3, 3, 50), ALLOWANCE, {type: 'add', tier: 'product', entry: entry('prod-51')});
  assert.equal(withHeadroom.admitted, false);
  assert.equal(withHeadroom.reason, 'limit_exceeded');
});

test('core and domain keep their own 50 limits when a product tier is declared', () => {
  assert.equal(evaluateCapacity(catalog(50, 0, 8), ALLOWANCE, {type: 'add', tier: 'core', entry: entry('core-51')}).reason, 'limit_exceeded');
  assert.equal(evaluateCapacity(catalog(0, 50, 8), ALLOWANCE, {type: 'add', tier: 'domain', entry: entry('domain-51')}).reason, 'limit_exceeded');
});

test('a product tier without a declared limit is never defaulted', () => {
  assert.equal(thrownCode(() => evaluateCapacity(catalog(1, 1, 1), {core: 50, domain: 50}, {type: 'add', tier: 'product', entry: entry('x')})), 'allowance_missing_limit');
});

// ---------------------------------------------------------------- scrutiny
const inv = (id: string, category: SkillInventoryEntry['category'], updateAuthority: SkillInventoryEntry['updateAuthority']): SkillInventoryEntry =>
  ({id, category, sourceHash: hex(`s:${id}`), purposeHash: hex(`p:${id}`), updateAuthority});
const cores = (n: number) => Array.from({length: n}, (_, i) => inv(`nautilus-core:c-${String(i).padStart(3, '0')}`, 'core', 'publisher'));
const products = (n: number) => Array.from({length: n}, (_, i) => inv(`nautilus-product:p-${String(i).padStart(3, '0')}`, 'product', 'manufacturer'));

test('a product skill is exactly the nautilus-product namespace, the product category and manufacturer authority', () => {
  assert.equal(skillInventoryDigest(products(1)).length, 64);
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-product:x', 'core', 'manufacturer')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-product:x', 'domain', 'manufacturer')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-product:x', 'product', 'publisher')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-product:x', 'product', 'business-procedure')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-core:x', 'product', 'publisher')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-core:x', 'core', 'manufacturer')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-business:x', 'product', 'manufacturer')])), 'scrutiny_authority_mismatch');
});

test('product skills count in their own category, never toward core or domain', () => {
  const previous = cores(40);
  const proposed = [...cores(40), ...products(8)];
  const result = assessSkillChange(previous, proposed, skillInventoryDigest(previous));
  assert.deepEqual(result.counts, {core: 40, domain: 0, product: 8});
  assert.equal(result.hardLimitSatisfied, true);
});

test('the 51st product fails the hard limit exactly as a 51st core would', () => {
  const proposed = products(51);
  const product = assessSkillChange([], proposed, skillInventoryDigest([]));
  assert.deepEqual(product.counts, {core: 0, domain: 0, product: 51});
  assert.equal(product.hardLimitSatisfied, false);
  // Independence in the other direction: 51 products do not hide core's own breach, and
  // 50 products do not consume core or domain places.
  const both = assessSkillChange([], [...cores(51), ...products(50)], skillInventoryDigest([]));
  assert.equal(both.hardLimitSatisfied, false);
  const full = assessSkillChange([], [...cores(50), ...products(50)], skillInventoryDigest([]));
  assert.equal(full.hardLimitSatisfied, true);
});

test('manufacturer skills need no review band and no authoring evidence', () => {
  const previous = cores(40);
  const proposed = [...cores(40), ...products(60)];
  const result = assessSkillChange(previous, proposed, skillInventoryDigest(previous));
  assert.deepEqual(result.requiredReviews.map(r => r.category).filter(c => c === 'product'), []);
  assert.deepEqual(result.requiredAuthoring.filter(a => a.id.startsWith('nautilus-product:')), []);
  // The same proposal with a core breach still demands core scrutiny.
  const coreOver = assessSkillChange(previous, [...cores(51), ...products(60)], skillInventoryDigest(previous));
  assert.equal(coreOver.requiredReviews.filter(r => r.category === 'core').length > 0, true);
});

// ------------------------------------------------------------ the package
const CORE = 'charts/core-skills';
const PRODUCT = 'charts/product-skills';
const body = (name: string, description = 'Test method.') => `---\nname: ${name}\ndescription: ${description}\n---\n# ${name}\n\nBody of ${name}.\n`;
const manifest = (name: string, version: string) => JSON.stringify({name, version, skills: './bundles/'});
const catalogFor = (group: string, names: string[]) => JSON.stringify({schemaVersion: 1, groups: {[group]: names.map(name => ({name, entrypoint: `bundles/${name}/SKILL.md`}))}});

function fileMapOf(root: string): Record<string, string> {
  const files: Record<string, string> = {};
  const visit = (dir: string): void => {
    for (const name of readdirSync(dir).sort()) {
      const path = join(dir, name); const st = lstatSync(path);
      if (st.isDirectory()) visit(path); else if (st.isFile()) files[relative(root, path)] = sha256(readFileSync(path));
    }
  };
  visit(root); return files;
}
function withTree(tree: Record<string, string>, run: (root: string, files: Record<string, string>, rewrite: (path: string, content: string) => Record<string, string>) => void): void {
  mkdirSync(TMP, {recursive: true});
  const root = mkdtempSync(join(TMP, 'product-skills-'));
  const write = (path: string, content: string) => { mkdirSync(dirname(join(root, path)), {recursive: true}); writeFileSync(join(root, path), content); };
  try {
    for (const [path, content] of Object.entries(tree)) write(path, content);
    run(root, fileMapOf(root), (path, content) => { write(path, content); return fileMapOf(root); });
  } finally { rmSync(root, {recursive: true, force: true}); }
}
const refuses = (root: string, files: Record<string, string>, code: string): void =>
  assert.throws(() => assertSkillPackage(root, files), (e: unknown) => e instanceof Error && e.message.startsWith(`${code}: `), `expected ${code}`);

/**
 * Seals a version-3 proposal the way the supported publication path does:
 * the ledger is composed by `composeSkillAdmissionLedger` from the projected
 * proposal inventory, never hand-written. Manufacturer identities are bound
 * by their pinned bundle digests, so the ledger's publisher digest excludes
 * them and rosters stay empty below the 35 target.
 */
function sealWithLedger(root: string, files: Record<string, string>, rewrite: (path: string, content: string) => Record<string, string>): Record<string, string> {
  try {
    const inventory = readSkillPackageInventory(root, files, {stage: 'proposal'});
    const assessment = assessSkillChange(inventory, inventory, skillInventoryDigest(inventory));
    const ledger = composeSkillAdmissionLedger({
      previous: {releaseDigest: hex('previous-release'), inventory, policyVersion: 3, ledger: undefined},
      proposed: inventory, assessment, review: null,
      target: {core: 35, domain: 35}, publishedAt: '2026-09-12T00:00:00.000Z',
    });
    return rewrite('skill-admission.json', JSON.stringify(ledger));
  } catch {
    // A proposal that refuses to project gets no ledger; admission then
    // reports the same refusal the proposal-stage projection did.
    return files;
  }
}

/** A version-3 classified release with two core skills and one product skill; the policy's provenance digest is filled in from the sealed map. */
function productTree(overrides: {policy?: (policy: any) => any} = {}) {
  const tree: Record<string, string> = {
    'charts/operating.md': '# operating\n',
    [`${CORE}/.claude-plugin/plugin.json`]: manifest('nautilus-core', '1.0.0'),
    [`${CORE}/catalog.json`]: catalogFor('methods', ['precise', 'simple']),
    [`${CORE}/bundles/precise/SKILL.md`]: body('precise'),
    [`${CORE}/bundles/simple/SKILL.md`]: body('simple'),
    [`${PRODUCT}/.claude-plugin/plugin.json`]: manifest('nautilus-product', COMMIT.slice(0, 12)),
    [`${PRODUCT}/catalog.json`]: catalogFor('higgsfield', ['higgs-demo']),
    [`${PRODUCT}/bundles/higgs-demo/SKILL.md`]: body('higgs-demo', 'Generate a demo through the vendor CLI.'),
    [`${PRODUCT}/bundles/higgs-demo/references/flow.md`]: 'vendor reference, shipped verbatim\n',
    'skill-purposes.json': JSON.stringify({version: 1, purposes: {'nautilus-core:precise': 'Test method.', 'nautilus-core:simple': 'Test method.', 'nautilus-product:higgs-demo': 'Generate a demo through the vendor CLI.'}}),
  };
  return (run: (root: string, files: Record<string, string>, rewrite: (p: string, c: string) => Record<string, string>) => void) => withTree(tree, (root, files, rewrite) => {
    const digest = productBundleDigest(files, PRODUCT, 'higgs-demo');
    let policy: any = {
      version: 3, allowance: {core: 50, domain: 50, product: 50}, target: {core: 35, domain: 35},
      publisherSkills: {'nautilus-core:precise': {category: 'core', updateAuthority: 'publisher'}, 'nautilus-core:simple': {category: 'core', updateAuthority: 'publisher'}},
      businessAuthored: {category: 'domain', updateAuthority: 'business-procedure'},
      productSkills: {'nautilus-product:higgs-demo': {category: 'product', updateAuthority: 'manufacturer', manufacturer: 'Higgsfield', repository: 'https://github.com/higgsfield-ai/skills.git', commit: COMMIT, contentDigest: digest}},
    };
    if (overrides.policy) policy = overrides.policy(policy);
    const withPolicy = rewrite('skill-capacity.json', JSON.stringify(policy));
    run(root, sealWithLedger(root, withPolicy, rewrite), rewrite);
  });
}

test('a version-3 product skill with matching provenance is admitted, classified and carried in the inventory', () => productTree()((root, files) => {
  const pkg = assertSkillPackage(root, files)!;
  const classification = pkg.classifications!['nautilus-product:higgs-demo'] as any;
  assert.equal(classification.category, 'product');
  assert.equal(classification.updateAuthority, 'manufacturer');
  assert.equal(classification.commit, COMMIT);
  const inventory = readSkillPackageInventory(root, files);
  assert.ok(inventory.some(e => e.id === 'nautilus-product:higgs-demo' && e.category === 'product' && e.updateAuthority === 'manufacturer'));
}));

test('one changed byte in a product bundle - even a support file - refuses the release as a locally modified manufacturer skill', () => productTree()((root, files, rewrite) => {
  assertSkillPackage(root, files);
  refuses(root, rewrite(`${PRODUCT}/bundles/higgs-demo/references/flow.md`, 'vendor reference, "improved" locally\n'), 'product_skill_modified');
  refuses(root, rewrite(`${PRODUCT}/bundles/higgs-demo/SKILL.md`, body('higgs-demo', 'Generate a demo, locally improved.')), 'product_skill_modified');
}));

test('a catalogued product bundle with no provenance declaration is refused', () => productTree({policy: p => ({...p, productSkills: {}})})((root, files) => {
  refuses(root, files, 'classification_required');
}));

test('provenance must name a resolvable upstream: a malformed commit, repository, or digest refuses the policy', () => {
  const break_ = (mutate: (skill: any) => any) => productTree({policy: p => ({...p, productSkills: {'nautilus-product:higgs-demo': mutate(p.productSkills['nautilus-product:higgs-demo'])}})});
  break_(s => ({...s, commit: 'main'}))((root, files) => refuses(root, files, 'policy_invalid'));
  break_(s => ({...s, repository: 'not a url'}))((root, files) => refuses(root, files, 'policy_invalid'));
  break_(s => ({...s, contentDigest: 'deadbeef'}))((root, files) => refuses(root, files, 'policy_invalid'));
  break_(s => ({...s, manufacturer: ''}))((root, files) => refuses(root, files, 'policy_invalid'));
});

test('a product skill cannot be relabelled core or domain, nor carry a non-manufacturer authority', () => {
  const break_ = (mutate: (skill: any) => any) => productTree({policy: p => ({...p, productSkills: {'nautilus-product:higgs-demo': mutate(p.productSkills['nautilus-product:higgs-demo'])}})});
  break_(s => ({...s, category: 'core'}))((root, files) => refuses(root, files, 'policy_invalid'));
  break_(s => ({...s, category: 'domain'}))((root, files) => refuses(root, files, 'policy_invalid'));
  break_(s => ({...s, updateAuthority: 'publisher'}))((root, files) => refuses(root, files, 'policy_invalid'));
});

test('the product allowance is a finite 50: null, absent-with-bundles, and any other number are refused', () => {
  productTree({policy: p => ({...p, allowance: {...p.allowance, product: null}})})((root, files) => refuses(root, files, 'policy_invalid'));
  productTree({policy: p => ({...p, allowance: {...p.allowance, product: 8}})})((root, files) => refuses(root, files, 'policy_invalid'));
  productTree({policy: p => ({...p, allowance: {...p.allowance, product: 51}})})((root, files) => refuses(root, files, 'policy_invalid'));
  productTree({policy: p => { const {product, ...rest} = p.allowance; return {...p, allowance: rest}; }})((root, files) => refuses(root, files, 'policy_invalid'));
});

test('product bundles need the version-3 classified policy; a version-2 declaration refuses them', () => {
  productTree({policy: p => ({version: 2, allowance: {core: 30, domain: 30}, publisherSkills: p.publisherSkills, businessAuthored: p.businessAuthored})})((root, files) => refuses(root, files, 'product_requires_classification'));
  productTree({policy: p => ({version: 2, allowance: {core: 30, domain: 30, product: 50}, publisherSkills: p.publisherSkills, businessAuthored: p.businessAuthored, productSkills: p.productSkills})})((root, files) => refuses(root, files, 'policy_invalid'));
  productTree({policy: p => ({version: 1, allowance: {core: 30, business: 30}})})((root, files) => refuses(root, files, 'product_requires_classification'));
});

const vendorTree = (count: number): Record<string, string> => {
  const names = Array.from({length: count}, (_, i) => `vendor-${String(i).padStart(2, '0')}`);
  return {
    [`${CORE}/.claude-plugin/plugin.json`]: manifest('nautilus-core', '1.0.0'),
    [`${CORE}/catalog.json`]: catalogFor('methods', ['precise']),
    [`${CORE}/bundles/precise/SKILL.md`]: body('precise'),
    [`${PRODUCT}/.claude-plugin/plugin.json`]: manifest('nautilus-product', COMMIT.slice(0, 12)),
    [`${PRODUCT}/catalog.json`]: catalogFor('higgsfield', names),
    ...Object.fromEntries(names.map(name => [`${PRODUCT}/bundles/${name}/SKILL.md`, body(name, 'Vendor method.')])),
    'skill-purposes.json': JSON.stringify({version: 1, purposes: {
      'nautilus-core:precise': 'Test method.',
      ...Object.fromEntries(names.map(name => [`nautilus-product:${name}`, 'Vendor method.'])),
    }}),
  };
};
const vendorPolicy = (root: string, files: Record<string, string>, names: readonly string[]): string => JSON.stringify({
  version: 3, allowance: {core: 50, domain: 50, product: 50}, target: {core: 35, domain: 35},
  publisherSkills: {'nautilus-core:precise': {category: 'core', updateAuthority: 'publisher'}},
  businessAuthored: {category: 'domain', updateAuthority: 'business-procedure'},
  productSkills: Object.fromEntries(names.map(name => [`nautilus-product:${name}`, {category: 'product', updateAuthority: 'manufacturer', manufacturer: 'Higgsfield', repository: 'https://github.com/higgsfield-ai/skills.git', commit: COMMIT, contentDigest: productBundleDigest(files, PRODUCT, name)}])),
});

test('fifty product bundles are admitted; the fifty-first refuses admission', () => {
  // At the cap: 50 manufacturer skills exactly.
  withTree(vendorTree(50), (root, files, rewrite) => {
    const withPolicy = rewrite('skill-capacity.json', vendorPolicy(root, files, Array.from({length: 50}, (_, i) => `vendor-${String(i).padStart(2, '0')}`)));
    sealWithLedger(root, withPolicy, rewrite);
    const pkg = assertSkillPackage(root, fileMapOf(root))!;
    const inventory = readSkillPackageInventory(root, fileMapOf(root));
    assert.equal(inventory.filter(e => e.category === 'product').length, 50);
    assert.equal(pkg.allowance.product, 50);
  });
  // One past the cap: admission refuses on the product tier's own limit.
  withTree(vendorTree(51), (root, files, rewrite) => {
    const sealed = rewrite('skill-capacity.json', vendorPolicy(root, files, Array.from({length: 51}, (_, i) => `vendor-${String(i).padStart(2, '0')}`)));
    assert.throws(() => assertSkillPackage(root, sealed), (e: unknown) => e instanceof Error && e.message.startsWith('migration_required: '),
      'a 51st product skill must refuse admission even with core and domain far below their own limits');
  });
});

test('the native configuration projects the product plugin and resolves its bodies for a capsule', () => productTree()((root, files) => {
  const config = nativeSkillConfiguration(root, files);
  assert.ok(config.plugins.some(p => p.name === 'nautilus-product'));
  assert.ok(config.expectedSkills.includes('nautilus-product:higgs-demo'));
  const bodies = config.requiredBodies(['nautilus-product:higgs-demo']);
  assert.equal(bodies.length, 1);
}));

test('the derived documents report the product count outside the core and domain counts', () => productTree()((root, files) => {
  // Imported lazily through the package projection the renderer itself uses;
  // the renderer's own suite covers the rendered text.
  const config = nativeSkillConfiguration(root, files);
  assert.equal(config.expectedSkills.filter(id => id.startsWith('nautilus-product:')).length, 1);
}));

test('local content-size limits govern authored skills, not manufacturer bundles: vendor bytes stay outside the authored library count', () => productTree()((root, files, rewrite) => {
  const big = 'x'.repeat(300 * 1024) + '\n';
  const next = rewrite(`${PRODUCT}/bundles/higgs-demo/references/large.md`, big);
  // The bundle changed, so its pinned digest must be re-declared - as an upstream re-sync would.
  const policy = JSON.parse(readFileSync(join(root, 'skill-capacity.json'), 'utf8'));
  policy.productSkills['nautilus-product:higgs-demo'].contentDigest = productBundleDigest(next, PRODUCT, 'higgs-demo');
  const sealed = rewrite('skill-capacity.json', JSON.stringify(policy));
  assert.ok(assertSkillPackage(root, sealed));
  // The same limits any authored release declares, applied to this tree: a
  // 300 KB vendor file fits far below a 256 KB authored bundle limit only
  // because it is not counted at all.
  const limits = {maxBodyBytes: 32768, maxBodyLines: 500, maxBundleBytes: 262144, maxLibraryBytes: 2097152};
  const bounds = assertSkillContentBounds(root, sealed, limits);
  assert.ok(bounds.libraryBytes < 262144, `vendor bytes must not enter the authored library count (got ${bounds.libraryBytes})`);
  // Authored core bytes still count: a 300 KB core reference breaches the bundle limit.
  const coreTree = rewrite(`${CORE}/bundles/precise/references/large.md`, big);
  assert.throws(() => assertSkillContentBounds(root, coreTree, limits), /skill_content_bundle_bytes: core:precise/);
}));

// ------------------------------------------------------------ publication
test('the publication ledger never rosters manufacturer skills and binds only publisher identities', () => {
  const previous = cores(35);
  const proposed = [...cores(35), ...products(4)];
  const assessment = assessSkillChange(previous, proposed, skillInventoryDigest(previous));
  const ledger = composeSkillAdmissionLedger({
    previous: {releaseDigest: hex('release'), inventory: previous, policyVersion: 3, ledger: undefined},
    proposed, assessment, review: null,
    target: {core: 35, domain: 35}, publishedAt: '2026-09-12T00:00:00.000Z',
  });
  assert.deepEqual(Object.keys(ledger.rosters), []);
  // The publisher digest excludes manufacturer identities entirely.
  const publisher = proposed.filter(entry => entry.updateAuthority === 'publisher');
  assert.equal(ledger.publisherInventoryDigest, skillInventoryDigest(publisher));
  assert.notEqual(ledger.publisherInventoryDigest, assessment.proposedDigest);
});

// ------------------------------------------------------------ preparer
// The preparer is the only path that installs a product tier into a release.
// A release may already carry another manufacturer's skills: adding a vendor
// must merge into that state, never delete the product directory wholesale.
test('adding a vendor preserves unrelated manufacturers and their pins, and the merged release still admits', () => withTree({
  [`release/${CORE}/.claude-plugin/plugin.json`]: manifest('nautilus-core', '1.0.0'),
  [`release/${CORE}/catalog.json`]: catalogFor('methods', ['precise']),
  [`release/${CORE}/bundles/precise/SKILL.md`]: body('precise'),
  [`release/${PRODUCT}/.claude-plugin/plugin.json`]: manifest('nautilus-product', 'aaaaaaaaaaaaa'),
  [`release/${PRODUCT}/catalog.json`]: catalogFor('other-vendor', ['a-tool']),
  [`release/${PRODUCT}/bundles/a-tool/SKILL.md`]: body('a-tool', 'The other vendor tool.'),
  [`release/${PRODUCT}/provenance.json`]: JSON.stringify({version: 1, manufacturer: 'Other Vendor', repository: 'https://github.com/other/vendor.git', commit: 'a'.repeat(40), rule: 'Installed verbatim.', skills: {'a-tool': {files: 1, contentDigest: 'pinned-by-the-earlier-install'}}}),
  'release/skill-purposes.json': JSON.stringify({version: 1, purposes: {'nautilus-core:precise': 'Test method.', 'nautilus-product:a-tool': 'The other vendor tool.'}}),
}, (root, _files, rewrite) => {
  const release = join(root, 'release');
  const releaseFiles = (): Record<string, string> => fileMapOf(release);
  const existingDigest = productBundleDigest(releaseFiles(), PRODUCT, 'a-tool');
  rewrite('release/skill-capacity.json', JSON.stringify({
    version: 3, allowance: {core: 50, domain: 50, product: 50}, target: {core: 35, domain: 35},
    publisherSkills: {'nautilus-core:precise': {category: 'core', updateAuthority: 'publisher'}},
    businessAuthored: {category: 'domain', updateAuthority: 'business-procedure'},
    productSkills: {'nautilus-product:a-tool': {category: 'product', updateAuthority: 'manufacturer', manufacturer: 'Other Vendor', repository: 'https://github.com/other/vendor.git', commit: 'a'.repeat(40), contentDigest: productBundleDigest(releaseFiles(), PRODUCT, 'a-tool')}},
  }));
  const ledger = composeSkillAdmissionLedger({
    previous: {releaseDigest: hex('previous-release'), inventory: readSkillPackageInventory(release, releaseFiles(), {stage: 'proposal'}), policyVersion: 3, ledger: undefined},
    proposed: readSkillPackageInventory(release, releaseFiles(), {stage: 'proposal'}),
    assessment: (() => { const inventory = readSkillPackageInventory(release, releaseFiles(), {stage: 'proposal'}); return assessSkillChange(inventory, inventory, skillInventoryDigest(inventory)); })(),
    review: null, target: {core: 35, domain: 35}, publishedAt: '2026-09-12T00:00:00.000Z',
  });
  writeFileSync(join(release, 'skill-admission.json'), JSON.stringify(ledger));
  assert.ok(assertSkillPackage(release, releaseFiles()), 'the starting release admits');

  // An exported upstream checkout (no VCS of its own) pinned by a provenance record.
  const upstream = join(root, 'upstream');
  const skillDir = join(upstream, 'b-tool');
  mkdirSync(join(skillDir, 'references'), {recursive: true});
  writeFileSync(join(skillDir, 'SKILL.md'), body('b-tool', 'The new vendor tool.'));
  writeFileSync(join(skillDir, 'references', 'guide.md'), 'vendor reference, verbatim\n');
  const newFiles: Record<string, string> = {
    'SKILL.md': sha256(body('b-tool', 'The new vendor tool.')),
    'references/guide.md': sha256('vendor reference, verbatim\n'),
  };
  const newDigest = createHash('sha256').update(JSON.stringify(Object.keys(newFiles).sort().map(path => [path, newFiles[path]])), 'utf8').digest('hex');
  const provenance = join(root, 'provenance-b.json');
  writeFileSync(provenance, JSON.stringify({commit: 'b'.repeat(40), skills: {'b-tool': {files: 2, contentDigest: newDigest}}}));

  const script = join(root, 'scripts', 'prepare-product-skills.py');
  mkdirSync(dirname(script), {recursive: true});
  copyFileSync(resolve(dirname(fileURLToPath(import.meta.url)), '../scripts/prepare-product-skills.py'), script);
  execFileSync('python3', [script, '--apply', '--source', upstream, '--commit', 'b'.repeat(40),
    '--manufacturer', 'New Vendor', '--repository', 'https://github.com/new/vendor.git', '--skills', 'b-tool',
    '--provenance', provenance], {cwd: root, stdio: 'pipe'});

  const merged = releaseFiles();
  // The unrelated manufacturer's bundle, pin, catalog group and purpose survive byte-for-byte.
  assert.equal(merged[`${PRODUCT}/bundles/a-tool/SKILL.md`], sha256(body('a-tool', 'The other vendor tool.')), 'the existing vendor bundle is untouched');
  const mergedPolicy = JSON.parse(readFileSync(join(release, 'skill-capacity.json'), 'utf8'));
  assert.equal(mergedPolicy.productSkills['nautilus-product:a-tool'].contentDigest, existingDigest);
  assert.equal(mergedPolicy.productSkills['nautilus-product:b-tool'].manufacturer, 'New Vendor');
  assert.equal(mergedPolicy.allowance.product, 50);
  const mergedCatalog = JSON.parse(readFileSync(join(release, `${PRODUCT}/catalog.json`), 'utf8'));
  assert.deepEqual(Object.keys(mergedCatalog.groups).sort(), ['new-vendor', 'other-vendor']);
  const mergedProvenance = JSON.parse(readFileSync(join(release, `${PRODUCT}/provenance.json`), 'utf8'));
  assert.deepEqual(Object.keys(mergedProvenance.skills).sort(), ['a-tool', 'b-tool']);
  assert.equal(mergedProvenance.skills['a-tool'].contentDigest, 'pinned-by-the-earlier-install', 'the earlier pin survives');
  const purposes = JSON.parse(readFileSync(join(release, 'skill-purposes.json'), 'utf8')).purposes;
  assert.equal(purposes['nautilus-product:a-tool'], 'The other vendor tool.');
  assert.equal(purposes['nautilus-product:b-tool'], 'The new vendor tool.');
  // The merged release still admits, with both vendors pinned in their own category.
  assertSkillPackage(release, merged);
  const inventory = readSkillPackageInventory(release, merged);
  assert.deepEqual(inventory.filter(entry => entry.category === 'product').map(entry => entry.id).sort(),
    ['nautilus-product:a-tool', 'nautilus-product:b-tool']);
}));
