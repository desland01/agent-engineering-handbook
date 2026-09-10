#!/usr/bin/env python3
"""Build worker workspaces, the checker template and a tickets-prepare recipe.

One generator for every run of this job, so that the harness proved on a pilot is the same
machine that runs the batch. Usage:

    make-recipe.py --plan-id chart-headings-pilot-1 --half pilot:explainer,browser
    make-recipe.py --plan-id chart-headings-r1      --half a --half b

`--half NAME` uses halves/half-NAME.txt; `--half NAME:b1,b2` writes that list first. Each
half becomes one ticket with its own worker workspace. Layout, all under this directory:

  originals/<bundle>/**.md   the Chart texts as published, outside every worker write scope
  halves/half-<name>.txt     the bundle list a worker is given
  checker/                   check.py + half-<name>.txt + capsule template, outside worker scope
  workers/<name>/            charts/, RULE.md, PROCEDURE.md, HALF.txt, TASK.md -> out/, corrections.json
  recipes/<plan-id>.json     the recipe; packets land in packets/<plan-id>/
"""
import argparse
import json
import os
import shutil
from pathlib import Path

H = Path('/Users/thebeast/.nautilus/releases/browser-route-20260910/var/workspaces/chart-headings')
# The digest comes from the release this harness lives in, never from the moving `current`
# symlink: `current` changed release mid-build once today, and capsules stamped with the new
# digest were refused by the plan's own release as `release_bound: false`.
RELEASE = H.parents[2]
DIGEST = json.loads((RELEASE / 'authority/release.json').read_text())['digest']
ORIG = H / 'originals'
PY = '/usr/bin/python3'

TASK = """# Correct every Chart in this half so its heading instructions ask for a claim, never a label

FIRST invoke native Skill skill="nautilus-core:precise". Do not delegate. No network. Workspace root, absolute: {ws}. Write only inside it.

Inputs, all inside the workspace:
- {ws}/RULE.md - the two rules you apply: "A heading reads right on its own" and "The instruction is not the output".
- {ws}/PROCEDURE.md - the procedure proved on the pilot Chart. Follow it step by step; where it is silent, apply RULE.md.
- {ws}/charts/<bundle>/SKILL.md and {ws}/charts/<bundle>/references/**.md - the {n} Charts in this half, listed in {ws}/HALF.txt. Read every one of them in full; the bad pattern is not always phrased with the word "heading".

What you are looking for: any sentence that instructs headings, titles, headlines, section names, captions, labels or names toward a subject, a noun phrase, a word count, a fixed string, or a template of fixed section headings that a writer would paste in as-is. Rewrite each such sentence so it instructs for a claim (a heading states what its section concludes, in the words a reader would use, plain verb, up to eight words, no semicolon) and carries the test (cover the body, read the heading, write what the section must claim; a different or opposite reading fails). Any example heading you write inside an instruction obeys the same limit: eight words, no semicolon. Bans on eyebrow headings, kickers, overlines and reversal headings are already correct and stay. Instructions about typography, size, spacing or count of headings are not the pattern and stay.

Rewrite only sentences that instruct. A recorded observation, a finding about an example, or a note of what some past page did is evidence, not an instruction: leave it exactly as it stands. "Process step titles describe methodology, not benefits" reports what a scaffold did; rewriting it into an instruction destroys the finding and drops what it said.

The sentence saying a delivered document's headings state claims is not a stock line to paste. Write it only where a list actually hands over section names, and put it in that list's own introduction - never appended to the end of an unrelated paragraph. Across a whole half it should appear at most twice; a sentence you find yourself adding to file after file is the copying failure this job exists to remove, wearing the corrector's clothes. The checker refuses any added sentence that appears in more than two files.

A column or list item asking for a "name", "title" or "label" is the same pattern in another dress. Removing a word count from it is not enough: ask that the name state what its row claims or settles. "A short plain name" still instructs a label; "a name stating what deciding it settles" instructs a claim.

Two things the fifth pilot got wrong, so do not repeat them. A required-contents list - "Include these sections:" followed by bolded item names and what each must contain - states what the delivered document holds. It is a content requirement, not a heading instruction: leave those items describing content, and never rewrite one into "heading claims ...", which leaks the instruction into the output. If such a list also hands over the delivered document's section names, add one short sentence saying the delivered headings state claims rather than these names. And state the cover-the-body test at most once in a file: a test pasted into every item of a list is the same copying failure in another form.

Deliver exactly one file: {ws}/corrections.json. There is no out/ directory; the checker runs sandboxed to its own workspace and cannot read one, so the corrected text travels inside this file.

{{"version":1,"half":"{half}","bundles":[{{"bundle":"<name>","files":[{{"path":"SKILL.md","status":"changed","text":"<the complete corrected file, every byte>","changes":[{{"line":<original line number>,"before":"<original line, verbatim>","after":"<corrected line, verbatim>","why":"<one sentence>"}}]}},{{"path":"references/<name>.md","status":"clean"}}]}}]}}

Every bundle in HALF.txt appears exactly once; every .md file in each bundle appears exactly once, changed or clean. A clean file carries no "text". A changed file carries the complete corrected file in "text": frontmatter byte-identical, every line you did not correct byte-identical, including line breaks and trailing whitespace. Line numbers are the original file's; a change spanning several lines lists each line. Write no other file and never touch scripts.

An acceptance checker outside your workspace will refuse the ticket if a bundle or file is missing from corrections.json, a changed file's frontmatter or any unreported line differs, a banned phrasing survives, a changed file carries no text or text whose frontmatter or uncorrected lines differ, or an example heading you wrote runs over eight words or carries a semicolon. Do not reword for style. Do not add rules a Chart did not have.
"""


def capsule(ws, route, provider, charts, outputs, tools, cid):
    return {'version': 4, 'id': cid, 'releaseDigest': DIGEST, 'workspaceRoot': str(ws),
            'allowWrite': [str(ws)], 'allowRead': [], 'inputs': {}, 'requiredCharts': charts,
            'tools': tools, 'modelRoute': route, 'provider': provider,
            'limits': {'maxSeconds': None, 'maxRequests': None}, 'declaredOutputs': outputs, 'expiresAt': None}


def build_worker(name, bundles, plan_id):
    ws = H / 'workers' / name
    if ws.exists():
        shutil.rmtree(ws)
    (ws / 'tmp').mkdir(parents=True)
    inputs = []
    for b in bundles:
        for src in sorted((ORIG / b).rglob('*.md')):
            dst = ws / 'charts' / src.relative_to(ORIG)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            inputs.append({'source': str(src), 'to': str(dst)})
    for f in ('RULE.md', 'PROCEDURE.md'):
        shutil.copy2(H / f, ws / f)
        inputs.append({'source': str(H / f), 'to': str(ws / f)})
    (ws / 'HALF.txt').write_text('\n'.join(bundles) + '\n')
    inputs.append({'source': str(H / 'halves' / f'half-{name}.txt'), 'to': str(ws / 'HALF.txt')})
    task = ws / 'TASK.md'
    task.write_text(TASK.format(ws=ws, n=len(bundles), half=name))
    cap = ws / 'capsule.json'
    cap.write_text(json.dumps(capsule(ws, 'glm-5.3-flash', 'zai-coding', ['nautilus-core:precise'],
                                      [str(ws / 'corrections.json')],
                                      ['Read', 'Write', 'Edit', 'Glob', 'Grep', 'Skill'],
                                      f'{plan_id}-{name}'), indent=2))
    return ws, task, cap, inputs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan-id', required=True)
    ap.add_argument('--half', action='append', required=True, help='NAME or NAME:bundle,bundle')
    a = ap.parse_args()
    checker = H / 'checker'
    # The checker is sandboxed to its own workspace, so its copy of the originals lives
    # inside it. It stays outside every worker write scope, which is what the contract asks.
    ck_orig = checker / 'originals'
    if ck_orig.exists():
        shutil.rmtree(ck_orig)
    shutil.copytree(ORIG, ck_orig)
    (checker / 'reports').mkdir(exist_ok=True)
    tickets = []
    for spec in a.half:
        name, _, listed = spec.partition(':')
        if listed:
            (H / 'halves').mkdir(exist_ok=True)
            (H / 'halves' / f'half-{name}.txt').write_text('\n'.join(listed.split(',')) + '\n')
        bundles = (H / 'halves' / f'half-{name}.txt').read_text().split()
        # The checker reads its own copy from beside check.py; workers never read it.
        (checker / f'half-{name}.txt').write_text('\n'.join(bundles) + '\n')
        # One checker capsule per half. Tickets run in parallel and each takes an output lease
        # on its declared subtree, so a shared `reports/` directory collides:
        # `capsule_refused_lease: conflicting_active_lease`. Distinct report paths are not
        # enough - the declared output itself must differ. Every effective tool set must also
        # sit inside the anchor tools and include the native Skill tool, checkers included.
        checker_cap = checker / f'capsule-{name}.json'
        checker_cap.write_text(json.dumps(capsule(checker, 'glm-5.3-flash', 'zai-coding', ['nautilus-core:precise'],
                                                  [str(checker / 'reports' / f'report-{name}.json')],
                                                  ['Bash', 'Read', 'Skill'], f'{a.plan_id}-checker-{name}'), indent=2))
        ws, task, cap, inputs = build_worker(name, bundles, a.plan_id)
        tickets.append({
            'id': f'correct-{name}', 'needs': [],
            'result': f'Every Chart in half {name} corrected so heading instructions ask for a claim; corrections.json accounts for every file.',
            'workspace': str(ws), 'taskSource': str(task), 'capsuleTemplate': str(cap), 'inputs': inputs,
            'artifacts': [str(ws / 'corrections.json')], 'model': 'glm-5.3-flash',
            'acceptance': {
                'functional': 'corrections.json covers every bundle and file in the half; each changed file carries its complete corrected text with frontmatter and unreported lines byte-identical; no banned heading instruction survives; every example heading is eight words or fewer with no semicolon.',
                'craft': "Each corrected sentence instructs for a claim and carries the test, in the Chart's own register, without adding rules the Chart did not have.",
                'checker': {'workspace': str(checker), 'capsuleTemplate': str(checker_cap)},
                'checks': [{
                    'id': 'corrections',
                    # argv carries no path the check itself creates: the controller hashes
                    # every argv element that is a file, so a candidate or report path in
                    # argv changes the environment digest between freeze and verify.
                    'command': [PY, str(checker / 'check.py'), '--half', name],
                    'copies': [{'from': str(ws / 'corrections.json'), 'to': str(checker / f'candidate-{name}.json')}],
                    'evidence': f'reports/report-{name}.json',
                }],
            },
        })
    recipe = {'version': 1, 'id': a.plan_id,
              'goal': 'Every published Chart instructs headings as claims, never as labels; reviewed by a different route before publication.',
              'specRef': str(H / 'RULE.md'), 'tickets': tickets}
    (H / 'recipes').mkdir(exist_ok=True)
    out = H / 'recipes' / f'{a.plan_id}.json'
    out.write_text(json.dumps(recipe, indent=2) + '\n')
    print('recipe:', out, 'tickets:', [t['id'] for t in tickets], 'bundles:', [len((H / 'halves' / f"half-{t['id'][8:]}.txt").read_text().split()) for t in tickets])


if __name__ == '__main__':
    main()
