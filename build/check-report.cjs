#!/usr/bin/env node
// Runs both checkers and emits the report shape the ticket controller reads:
// {pass, checks: [{id, pass, detail}], failures: [{id, expected, actual}]}.
// Every visual ticket binds this as acceptance.checks; a nonzero exit never
// passes, and the report is written on success and failure alike.
const {spawnSync} = require('node:child_process');
const {writeFileSync, existsSync} = require('node:fs');
const {resolve} = require('node:path');
const root = resolve(__dirname, '..');
const out = process.argv[2] ? resolve(process.argv[2]) : resolve(root, 'build/report.json');
const python = process.env.CHECK_PYTHON || 'python3';
const checks = []; const failures = [];
function run(id, cmd, args, expected) {
  const r = spawnSync(cmd, args, {cwd: root, encoding: 'utf8', timeout: 600000});
  const text = (r.stdout || '') + (r.stderr || '');
  const pass = r.status === 0 && /(^|\n)PASS\b/.test(text);
  const last = text.trim().split('\n').filter(Boolean).slice(-1)[0] || '';
  checks.push({id, pass, detail: last.slice(0, 300)});
  if (!pass) {
    const lines = text.split('\n').filter((l) => /^(FAIL|  - |not ok)/.test(l)).slice(0, 40);
    failures.push({id, expected, actual: lines.length ? lines.join('\n') : `exit ${r.status}: ${last.slice(0, 300)}`});
  }
}
run('structure', python, ['build/check.py'], 'check.py PASS: pages, links, hashes, semantics, headings, sentences, page identity');
const renderCheck = resolve(root, 'build/check-render.js');
if (existsSync(resolve(root, 'build/node_modules/puppeteer'))) {
  run('rendered', 'node', [renderCheck], 'check-render.js PASS: no overflow, no scrollbar chrome, routes present, no console errors, nothing left hidden, no scroll capture');
} else {
  checks.push({id: 'rendered', pass: false, detail: 'puppeteer not installed under build/'});
  failures.push({id: 'rendered', expected: 'rendered check executed', actual: 'build/node_modules/puppeteer absent (cd build && npm install)'});
}
const report = {version: 1, pass: failures.length === 0, checks, failures};
writeFileSync(out, JSON.stringify(report, null, 2) + '\n');
console.log(`${report.pass ? 'PASS' : 'FAIL'}: ${checks.filter((c) => c.pass).length}/${checks.length} checks; report ${out}`);
process.exit(report.pass ? 0 : 1);
