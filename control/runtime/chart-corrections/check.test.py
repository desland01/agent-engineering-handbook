#!/usr/bin/env python3
"""check.py must accept a correct correction and refuse each defect it exists to catch:
an unreported line change, changed frontmatter, a surviving banned instruction, a bundle
left unreported, a missing corrected text, an over-long or semicolon example heading, and
originals it cannot read (the sandbox failure that blocked the third pilot)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
FM = '---\nname: x\ndescription: y\n---\n'
ORIG_TEXT = FM + '# X\n\nUse plain noun-phrase headings, in this order:\n\nKeep the rest.\n'
GOOD_TEXT = FM + '# X\n\nEach heading states what its section concludes, tested with the body covered:\n\nKeep the rest.\n'
LINE = 7  # the instructing line, 1-indexed, in ORIG_TEXT


def run(tmp, candidate, half=('alpha', 'explainer'), originals=True, orig_text=None):
    here = tmp / 'checker'
    here.mkdir()
    (here / 'check.py').write_text((HERE / 'check.py').read_text())
    if originals:
        for b in half:
            (here / 'originals' / b).mkdir(parents=True)
            (here / 'originals' / b / 'SKILL.md').write_text(orig_text or ORIG_TEXT)
    tag = candidate.get('half', 't')
    (here / f'half-{tag}.txt').write_text('\n'.join(half))
    (here / f'candidate-{tag}.json').write_text(json.dumps(candidate))
    r = subprocess.run([sys.executable, str(here / 'check.py'), '--half', tag], capture_output=True, text=True)
    return r.returncode, json.loads((here / 'reports' / f'report-{tag}.json').read_text())


def changed(bundle, text=GOOD_TEXT, line=LINE):
    return {'bundle': bundle, 'files': [{'path': 'SKILL.md', 'status': 'changed', 'text': text,
                                         'changes': [{'line': line, 'before': 'Use plain noun-phrase headings, in this order:',
                                                      'after': 'Each heading states...', 'why': 'claim not label'}]}]}


def clean(bundle):
    return {'bundle': bundle, 'files': [{'path': 'SKILL.md', 'status': 'clean'}]}


good = {'version': 1, 'half': 't', 'bundles': [clean('alpha'), changed('explainer')]}
cases = []


def case(name, candidate, expect_pass, expect_failure_suffix=None, **kw):
    with tempfile.TemporaryDirectory() as t:
        code, rep = run(Path(t), candidate, **kw)
    ok = (code == 0) == expect_pass and rep['pass'] == expect_pass
    if expect_failure_suffix:
        ok = ok and any(f['id'].endswith(expect_failure_suffix) or f['id'] == expect_failure_suffix for f in rep['failures'])
    assert ok, (name, rep)
    cases.append(name)


case('accepts a correct correction', good, True)
case('accepts a short example heading',
     {**good, 'bundles': [clean('alpha'), changed('explainer', GOOD_TEXT.replace(
         'tested with the body covered:', 'for example "Repeated failures waste tokens":'))]}, True)
case('refuses an unreported line change',
     {**good, 'bundles': [clean('alpha'), changed('explainer', GOOD_TEXT.replace('Keep the rest.', 'Keep the REST.'))]},
     False, 'only-named-lines')
case('refuses changed frontmatter',
     {**good, 'bundles': [clean('alpha'), changed('explainer', GOOD_TEXT.replace('description: y', 'description: z'))]},
     False, 'frontmatter')
case('refuses a surviving banned instruction',
     {**good, 'bundles': [clean('alpha'), changed('explainer', ORIG_TEXT.replace('Keep the rest.', 'Keep the rest!'))]},
     False, 'banned')
case('refuses a ten-word semicolon example heading',
     {**good, 'bundles': [clean('alpha'), changed('explainer', GOOD_TEXT.replace(
         'tested with the body covered:', 'for example "You directed three hired hands; each had fixed jobs today":'))]},
     False, 'example-heading')
case('refuses an unreported bundle', {'version': 1, 'half': 't', 'bundles': [changed('explainer')]},
     False, 'bundles-covered')
case('refuses a changed file with no text',
     {'version': 1, 'half': 't', 'bundles': [clean('alpha'),
                                             {'bundle': 'explainer', 'files': [{'path': 'SKILL.md', 'status': 'changed', 'changes': []}]}]},
     False, ':text')
case('refuses text identical to the original',
     {**good, 'bundles': [clean('alpha'), changed('explainer', ORIG_TEXT)]}, False, 'differs')
case('refuses unreadable originals (the sandbox failure)', good, False, 'originals-readable', originals=False)

case('refuses instruction leaked into a required-contents item',
     {**good, 'bundles': [clean('alpha'), changed('explainer', GOOD_TEXT.replace(
         'Keep the rest.', '- **Suggested skills**: heading claims which skills to invoke.'), line=9)]},
     False, 'no-leaked-instruction')
case('refuses the cover-the-body test repeated in a file',
     {**good, 'bundles': [clean('alpha'), changed('explainer', GOOD_TEXT.replace(
         'tested with the body covered:', 'cover the body and read it.').replace(
         'Keep the rest.', 'Also cover the body and read it.'), line=9)]},
     False, 'test-stated-once')

case('refuses a word count attached to a name',
     {**good, 'bundles': [clean('alpha'), changed('explainer', GOOD_TEXT.replace(
         'Keep the rest.', 'a table of decisions: number, two-to-four-word name, one sentence.'), line=9)]},
     False, 'banned')
case('accepts "up to eight words" as a claim limit',
     {**good, 'bundles': [clean('alpha'), changed('explainer', GOOD_TEXT.replace(
         'tested with the body covered:', 'a plain clause of up to eight words.'))]}, True)

STOCK = 'The delivered headings state claims rather than these names.'
case('refuses one stock sentence pasted across three files',
     {'version': 1, 'half': 't3', 'bundles': [
         {'bundle': b, 'files': [{'path': 'SKILL.md', 'status': 'changed',
                                  'text': GOOD_TEXT.replace('Keep the rest.', 'Keep the rest. ' + STOCK),
                                  'changes': [{'line': LINE, 'before': 'Use plain noun-phrase headings, in this order:',
                                               'after': 'Each heading states...', 'why': 'claim not label'},
                                              {'line': 9, 'before': 'Keep the rest.',
                                               'after': 'Keep the rest. ' + STOCK, 'why': 'x'}]}]}
         for b in ('alpha', 'beta', 'explainer')]},
     False, 'no-stock-sentence', half=('alpha', 'beta', 'explainer'))
case('accepts the same sentence in two files',
     {'version': 1, 'half': 't', 'bundles': [
         {'bundle': b, 'files': [{'path': 'SKILL.md', 'status': 'changed',
                                  'text': GOOD_TEXT.replace('Keep the rest.', 'Keep the rest. ' + STOCK),
                                  'changes': [{'line': LINE, 'before': 'Use plain noun-phrase headings, in this order:',
                                               'after': 'Each heading states...', 'why': 'claim not label'},
                                              {'line': 9, 'before': 'Keep the rest.',
                                               'after': 'Keep the rest. ' + STOCK, 'why': 'x'}]}]}
         for b in ('alpha', 'explainer')]}, True)

case('refuses a title template left in a clean file',
     {'version': 1, 'half': 'tt', 'bundles': [clean('alpha'), changed('explainer')]},
     False, 'clean-has-no-title-template',
     orig_text=ORIG_TEXT + '\n# {Short title of the decision}\n')
case('accepts a name placeholder left in a clean file',
     {'version': 1, 'half': 'tn', 'bundles': [clean('alpha'), changed('explainer')]},
     True, orig_text=ORIG_TEXT + '\n# {Context Name}\n')

print(f'check.py: {len(cases)} scenarios pass ({sum(1 for c in cases if c.startswith("accepts"))} accept, {sum(1 for c in cases if c.startswith("refuses"))} refuse)')
