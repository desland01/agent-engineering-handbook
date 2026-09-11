// A capsule declares the skills it selected; a run that never invokes them is blocked.
// Installs at tests/capsules/skill-plan.test.mjs, where it resolves ../../src like its
// siblings. Run from elsewhere by pointing NAUTILUS_SRC at a src/ directory:
//
//   NAUTILUS_SRC=<tree>/src tsx --test control/runtime/skill-selection/skill-plan.test.mjs
//
// Until the patch lands, section 1 passes and sections 2 to 4 are red.
import {test, describe} from 'node:test';
import assert from 'node:assert/strict';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const SRC = process.env.NAUTILUS_SRC ?? resolve(dirname(fileURLToPath(import.meta.url)), '../../src');
const {parseCapsule} = await import(SRC + '/capsule-schema.mjs');
const runtime = await import(SRC + '/capsule-runtime.mjs');
const {childSubsetViolations} = await import(SRC + '/capsule-admission.mjs');
const {chartEvidenceTracker} = runtime;

const RELEASE = 'c'.repeat(64);
const WS = '/Users/thebeast/.nautilus/var/workspaces/plan-test';
const PLAN = [
  {chart: 'nautilus-core:engineering-plan', purpose: 'settle the interfaces first'},
  {chart: 'nautilus-core:tdd', purpose: 'failing check before the fix'},
  {chart: 'nautilus-core:code-review', purpose: 'review the diff before handing back'},
];
const CHARTS = PLAN.map(entry => entry.chart);

function declaration(overrides = {}) {
  return {
    version: 5, id: 'plan-capsule-one', releaseDigest: RELEASE, workspaceRoot: WS,
    allowWrite: [WS], declaredOutputs: [WS], inputs: {},
    requiredCharts: [...CHARTS], tools: ['Read', 'Skill'],
    modelRoute: 'glm-5.3-flash', provider: 'zai-coding',
    limits: {maxSeconds: 1800, maxRequests: 200},
    expiresAt: '2026-09-12T00:00:00Z',
    skillPlan: PLAN.map(entry => ({...entry})),
    ...overrides,
  };
}

// A run that invokes the first of three planned skills and stops there.
function partiallyAppliedRun() {
  const tracker = chartEvidenceTracker([...CHARTS]);
  tracker.init([...CHARTS]);
  tracker.toolUse({name: 'Skill', id: 'u1', input: {skill: CHARTS[0]}});
  tracker.toolResult({tool_use_id: 'u1', content: 'ok'});
  return tracker.summary();
}

describe('1. what the runtime measures today, and lets pass', () => {
  test('a plan left half-invoked is already visible in the evidence', () => {
    const summary = partiallyAppliedRun();
    assert.deepEqual(summary.withoutSuccessfulInvocation, [CHARTS[1], CHARTS[2]]);
    assert.equal(summary.charts.find(c => c.id === CHARTS[0]).invocationSucceeded, 1);
  });
});

describe('2. version 5 declares the plan, and refuses a malformed one', () => {
  const refuses = (overrides, field) => {
    const result = parseCapsule(declaration(overrides));
    assert.equal(result.ok, false, 'expected a refusal for ' + field);
    assert.ok(result.errors.some(e => e.field.startsWith('skillPlan')), 'expected a skillPlan error, got ' + JSON.stringify(result.errors));
  };
  test('a well-formed version 5 capsule is admitted and keeps the chain order', () => {
    const result = parseCapsule(declaration());
    assert.equal(result.ok, true, JSON.stringify(result.errors));
    assert.deepEqual(result.capsule.skillPlan.map(e => e.chart), CHARTS);
  });
  test('the plan is required, non-empty and free of duplicates', () => {
    refuses({skillPlan: undefined}, 'absent');
    refuses({skillPlan: []}, 'empty');
    refuses({skillPlan: [PLAN[0], {...PLAN[0]}]}, 'duplicate');
  });
  test('every planned chart is one the capsule requires, with a stated purpose', () => {
    refuses({skillPlan: [{chart: 'nautilus-core:design-review', purpose: 'not required here'}]}, 'outside requiredCharts');
    refuses({skillPlan: [{chart: CHARTS[0], purpose: ''}]}, 'empty purpose');
  });
  test('versions 1 to 4 carry no plan and are unchanged', () => {
    const v4 = parseCapsule(declaration({version: 4}));
    assert.equal(v4.ok, false);
    assert.ok(v4.errors.some(e => e.field === 'skillPlan'), 'a plan on an older contract is an unknown field');
    const {skillPlan, ...rest} = declaration({version: 4});
    assert.equal(parseCapsule(rest).ok, true, 'a version 4 capsule without a plan still parses');
  });
});

describe('3. a run that left a planned skill uninvoked is blocked', () => {
  test('the verdict names every planned skill the run never invoked', () => {
    const verdict = runtime.skillPlanVerdict(PLAN, partiallyAppliedRun());
    assert.equal(verdict.allInvoked, false);
    assert.deepEqual(verdict.uninvoked, [CHARTS[1], CHARTS[2]]);
    assert.equal(verdict.reason, 'capsule_skill_plan_uninvoked');
  });
  test('a fully applied plan passes', () => {
    const tracker = chartEvidenceTracker([...CHARTS]);
    tracker.init([...CHARTS]);
    CHARTS.forEach((chart, i) => {
      tracker.toolUse({name: 'Skill', id: 'u' + i, input: {skill: chart}});
      tracker.toolResult({tool_use_id: 'u' + i, content: 'ok'});
    });
    const verdict = runtime.skillPlanVerdict(PLAN, tracker.summary());
    assert.equal(verdict.allInvoked, true);
    assert.deepEqual(verdict.uninvoked, []);
  });
  test('a failed invocation does not count as applying the skill', () => {
    const tracker = chartEvidenceTracker([CHARTS[0]]);
    tracker.init([CHARTS[0]]);
    tracker.toolUse({name: 'Skill', id: 'e1', input: {skill: CHARTS[0]}});
    tracker.toolResult({tool_use_id: 'e1', is_error: true, content: 'boom'});
    assert.deepEqual(runtime.skillPlanVerdict([PLAN[0]], tracker.summary()).uninvoked, [CHARTS[0]]);
  });
  test('a required chart outside the plan keeps its present-only obligation', () => {
    const tracker = chartEvidenceTracker([...CHARTS, 'nautilus-core:simple']);
    tracker.init([...CHARTS, 'nautilus-core:simple']);
    CHARTS.forEach((chart, i) => {
      tracker.toolUse({name: 'Skill', id: 'p' + i, input: {skill: chart}});
      tracker.toolResult({tool_use_id: 'p' + i, content: 'ok'});
    });
    assert.equal(runtime.skillPlanVerdict(PLAN, tracker.summary()).allInvoked, true, 'an unplanned required chart never blocks a run');
  });
});

describe('4. a delegated worker plans inside its parent', () => {
  const anchorTools = ['Bash', 'Read', 'Write', 'Edit', 'Glob', 'Grep', 'Skill'];
  test('a child planning a chart the parent does not require is refused', () => {
    const parent = parseCapsule(declaration()).capsule;
    const child = parseCapsule(declaration({
      id: 'plan-capsule-child', parentId: parent.id,
      requiredCharts: [...CHARTS, 'nautilus-core:design-review'],
      skillPlan: [...PLAN, {chart: 'nautilus-core:design-review', purpose: 'review the rendered page'}],
    })).capsule;
    const violations = childSubsetViolations(child, parent, anchorTools);
    assert.ok(violations.some(v => v.dimension === 'skillPlan'), 'the refusal names the plan: ' + JSON.stringify(violations));
  });
  test('a child planning a subset of the parent chain is admitted', () => {
    const parent = parseCapsule(declaration()).capsule;
    const child = parseCapsule(declaration({id: 'plan-capsule-child-2', parentId: parent.id, skillPlan: [PLAN[1]]})).capsule;
    assert.deepEqual(childSubsetViolations(child, parent, anchorTools), []);
  });
});
