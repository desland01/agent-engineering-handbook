// Product skills: a third category for manufacturer-published skills of a
// paid product. Uncapped, installed verbatim at a pinned upstream commit, and
// refused the moment their bytes differ from the declared provenance digest.
// Owner amendment of 2026-09-10 (ARCHITECT.md, "Product skills").
import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {mkdirSync, mkdtempSync, writeFileSync, rmSync, readdirSync, lstatSync, readFileSync} from 'node:fs';
import {dirname, join, relative, resolve} from 'node:path';
import {evaluateCapacity, SkillCapacityError} from '../src/skill-capacity.js';
import type {SkillCatalog, SkillEntry} from '../src/skill-capacity.js';
import {assessSkillChange, skillInventoryDigest} from '../src/skill-scrutiny.js';
import type {SkillInventoryEntry} from '../src/skill-scrutiny.js';
import {assertSkillPackage, productBundleDigest, readSkillPackageInventory} from '../src/skill-package.js';
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
const catalog = (core: number, product: number): SkillCatalog => ({tiers: [
  {tier: 'core', entries: Array.from({length: core}, (_, i) => entry(`core-${i}`))},
  {tier: 'product', entries: Array.from({length: product}, (_, i) => entry(`prod-${i}`))},
]});

test('the product tier is uncapped: a null allowance admits any count', () => {
  const result = evaluateCapacity(catalog(3, 300), {core: 50, product: null}, {type: 'add', tier: 'product', entry: entry('prod-more')});
  assert.equal(result.admitted, true);
  assert.equal(result.resultingCount.product, 301);
});

test('the product tier refuses a numeric limit: a cap on manufacturer skills is not a policy this runtime accepts', () => {
  assert.equal(thrownCode(() => evaluateCapacity(catalog(3, 1), {core: 50, product: 5}, {type: 'add', tier: 'product', entry: entry('x')})), 'product_uncapped');
});

test('core stays capped exactly as before when a product tier is present', () => {
  const result = evaluateCapacity(catalog(50, 8), {core: 50, product: null}, {type: 'add', tier: 'core', entry: entry('core-extra')});
  assert.equal(result.admitted, false);
  assert.equal(result.reason, 'limit_exceeded');
});

test('lowering allowances leaves the product tier untouched and never counts it as over', () => {
  const result = evaluateCapacity(catalog(10, 200), {core: 50, product: null}, {type: 'lowerAllowance', allowance: {core: 40, product: null}});
  assert.equal(result.admitted, true);
});

// ---------------------------------------------------------------- scrutiny
const inv = (id: string, category: SkillInventoryEntry['category'], updateAuthority: SkillInventoryEntry['updateAuthority']): SkillInventoryEntry =>
  ({id, category, sourceHash: hex(`s:${id}`), purposeHash: hex(`p:${id}`), updateAuthority});
const cores = (n: number) => Array.from({length: n}, (_, i) => inv(`nautilus-core:c-${String(i).padStart(3, '0')}`, 'core', 'publisher'));
const products = (n: number) => Array.from({length: n}, (_, i) => inv(`nautilus-product:p-${String(i).padStart(3, '0')}`, 'product', 'manufacturer'));

test('a product skill is exactly the nautilus-product namespace, the product category and manufacturer authority', () => {
  assert.equal(skillInventoryDigest(products(1)).length, 64);
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-product:x', 'core', 'manufacturer')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-product:x', 'product', 'publisher')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-core:x', 'product', 'publisher')])), 'scrutiny_authority_mismatch');
  assert.equal(thrownCode(() => skillInventoryDigest([inv('nautilus-core:x', 'core', 'manufacturer')])), 'scrutiny_authority_mismatch');
});

test('product skills count in their own category, never toward core or domain, and need no review or authoring', () => {
  const previous = cores(40);
  const proposed = [...cores(40), ...products(60)];
  const result = assessSkillChange(previous, proposed, skillInventoryDigest(previous));
  assert.deepEqual(result.counts, {core: 40, domain: 0, product: 60});
  assert.equal(result.hardLimitSatisfied, true);
  assert.deepEqual(result.requiredReviews.map(r => r.category).filter(c => c === 'product'), []);
  assert.deepEqual(result.requiredAuthoring.filter(a => a.id.startsWith('nautilus-product:')), []);
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

/** A version-2 classified release with two core skills and one product skill; the policy's provenance digest is filled in from the sealed map. */
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
      version: 2, allowance: {core: 30, domain: 30, product: null},
      publisherSkills: {'nautilus-core:precise': {category: 'core', updateAuthority: 'publisher'}, 'nautilus-core:simple': {category: 'core', updateAuthority: 'publisher'}},
      businessAuthored: {category: 'domain', updateAuthority: 'business-procedure'},
      productSkills: {'nautilus-product:higgs-demo': {category: 'product', updateAuthority: 'manufacturer', manufacturer: 'Higgsfield', repository: 'https://github.com/higgsfield-ai/skills.git', commit: COMMIT, contentDigest: digest}},
    };
    if (overrides.policy) policy = overrides.policy(policy);
    run(root, rewrite('skill-capacity.json', JSON.stringify(policy)), rewrite);
  });
}

test('a product skill with matching provenance is admitted, classified and carried in the inventory', () => productTree()((root, files) => {
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
}));

test('a catalogued product bundle with no provenance declaration is refused', () => productTree({policy: p => ({...p, productSkills: {}})})((root, files) => {
  refuses(root, files, 'classification_required');
}));

test('provenance must name a resolvable upstream: a malformed commit or repository refuses the policy', () => {
  productTree({policy: p => ({...p, productSkills: {'nautilus-product:higgs-demo': {...p.productSkills['nautilus-product:higgs-demo'], commit: 'main'}}})})((root, files) => refuses(root, files, 'policy_invalid'));
  productTree({policy: p => ({...p, productSkills: {'nautilus-product:higgs-demo': {...p.productSkills['nautilus-product:higgs-demo'], repository: 'not a url'}}})})((root, files) => refuses(root, files, 'policy_invalid'));
});

test('a product skill cannot be relabelled core or domain, and a numeric product allowance is refused', () => {
  productTree({policy: p => ({...p, productSkills: {'nautilus-product:higgs-demo': {...p.productSkills['nautilus-product:higgs-demo'], category: 'core'}}})})((root, files) => refuses(root, files, 'policy_invalid'));
  productTree({policy: p => ({...p, allowance: {...p.allowance, product: 8}})})((root, files) => refuses(root, files, 'policy_invalid'));
});

test('the native configuration projects the product plugin and resolves its bodies for a capsule', () => productTree()((root, files) => {
  const config = nativeSkillConfiguration(root, files);
  assert.ok(config.plugins.some(p => p.name === 'nautilus-product'));
  assert.ok(config.expectedSkills.includes('nautilus-product:higgs-demo'));
  const bodies = config.requiredBodies(['nautilus-product:higgs-demo']);
  assert.equal(bodies.length, 1);
}));

test('local content-size limits govern authored skills, not manufacturer bundles: a 300 KB vendor reference is admitted as shipped', () => productTree()((root, files, rewrite) => {
  const big = 'x'.repeat(300 * 1024) + '\n';
  const next = rewrite(`${PRODUCT}/bundles/higgs-demo/references/large.md`, big);
  // The bundle changed, so its pinned digest must be re-declared - as an upstream re-sync would.
  const policy = JSON.parse(readFileSync(join(root, 'skill-capacity.json'), 'utf8'));
  policy.productSkills['nautilus-product:higgs-demo'].contentDigest = productBundleDigest(next, PRODUCT, 'higgs-demo');
  const sealed = rewrite('skill-capacity.json', JSON.stringify(policy));
  assert.ok(assertSkillPackage(root, sealed));
  // The declaration as the release actually ships it, not a hand-written copy.
  const limits = JSON.parse(readFileSync(resolve(process.cwd(), 'release/skill-content-limits.json'), 'utf8'));
  const bounds = assertSkillContentBounds(root, sealed, limits);
  assert.ok(bounds.libraryBytes < 262144, `vendor bytes must not enter the authored library count (got ${bounds.libraryBytes})`);
}));
