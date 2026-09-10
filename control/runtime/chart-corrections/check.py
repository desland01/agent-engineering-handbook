#!/usr/bin/env python3
"""Acceptance check for one Chart-correction ticket.

The checker runs sandboxed to its own workspace, so it reads only what lives inside it:
`originals/<bundle>/**.md` (a static copy, outside every worker write scope) and
`candidate-<half>.json` (the controller's copy of the worker's single declared artifact).
The worker therefore delivers the corrected text inside that JSON; a worker `out/` tree
would be unreadable here, and checker copies are file-only and must be declared artifacts.

Proves: every bundle and file of the half is accounted for; each changed file's frontmatter
is byte-identical; only the lines the worker reported differ; no banned heading instruction
survives; every example heading inside an instruction is eight words or fewer with no
semicolon; the known-bad `explainer` Chart is changed. Does not prove the rewritten sentences
are good - that is the judged acceptance, by a route other than the maker.

Writes report.json as {version, pass, checks, failures[{id, expected, actual}]}.
"""
import argparse
import json
from collections import Counter
import os
import re
import sys
from pathlib import Path

BANNED = [
    (re.compile(r'noun[- ]phrase heading', re.I), 'instructs a noun-phrase heading'),
    (re.compile(r'heading[s]? (?:that )?names? (?:the|its) subject', re.I), 'instructs a heading that names a subject'),
    (re.compile(r'\b(?:two|three|2|3) to (?:four|five|4|5) words?\b.*\b(?:heading|title)', re.I), 'instructs a word-count label'),
    (re.compile(r'(?:heading|title)[^.\n]{0,40}\b(?:label|kicker)\b(?!s? (?:is|are) (?:banned|forbidden|not)|s?, decorative)', re.I), 'instructs a label heading'),
    # A word count attached to a name is a label instruction wherever it appears, hyphenated or
    # not, and whether the thing is called a heading, a title or a name. The sixth pilot left
    # "two-to-four-word name" standing because the earlier pattern wanted the word "heading".
    (re.compile(r'\b(?:one|two|three|four|five|six|seven|eight|\d+)[-\s]word\s+(?:name|heading|title|label|headline)\b', re.I),
     'attaches a word count to a name, which is a label instruction'),
]
FRONT = re.compile(r'\A---\n.*?\n---\n', re.S)
# An example heading written inside an instruction obeys the rule it teaches: a claim of at
# most eight words with no semicolon. The pilot produced ten-word, semicolon headings twice;
# this is that correction encoded rather than repeated by hand.
EXAMPLE = re.compile(r'(?:heading|headline|title)[^."\n]{0,60}?["“]([^"”\n]{4,120})["”]', re.I)


def bad_examples(line):
    out = []
    for m in EXAMPLE.finditer(line):
        text = m.group(1).strip()
        if text.startswith(('#', '<', '{', '/')) or text.endswith(('.md', '.py', '.json')):
            continue  # a file or tag name, not an example heading
        words = len(text.split())
        if words > 8 or ';' in text:
            out.append(f'{text!r} ({words} words{", semicolon" if ";" in text else ""})')
    return out


# Two defects the fifth pilot delivered that no earlier check could see. A required-contents
# list ("Include these sections: **Name**: what goes in it") states what the document must
# contain; rewriting those items into instructions about headings leaks the instruction into
# the output, the very thing the rule forbids. And the cover-the-body test belongs once in a
# file, not pasted into every item of a list.
LEAKED_INSTRUCTION = re.compile(r'\*\*[^*\n]{2,60}\*\*\s*:\s*(?:the\s+)?heading\s+claims\b', re.I)
TEST_PHRASE = re.compile(r'cover the body', re.I)
TITLE_TEMPLATE = re.compile(r'^#{1,4} \{[^}]*\btitle\b[^}]*\}', re.I)


def frontmatter(text):
    m = FRONT.match(text)
    return m.group(0) if m else ''


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--half', default=os.environ.get('HALF'))
    # The candidate, originals and report paths are derived from the checker's own directory,
    # never passed as argv: the controller hashes every argv element that exists as a file, so
    # a path this run creates would change the environment digest between freeze and verify.
    p.add_argument('--candidate')
    p.add_argument('--originals')
    p.add_argument('--report')
    a = p.parse_args(argv)
    here = Path(__file__).resolve().parent
    a.candidate = a.candidate or str(here / f'candidate-{a.half}.json')
    a.originals = a.originals or str(here / 'originals')
    if not a.report:
        (here / 'reports').mkdir(exist_ok=True)
        a.report = str(here / 'reports' / f'report-{a.half}.json')

    checks, failures = 0, []

    def check(cid, ok, expected, actual):
        nonlocal checks
        checks += 1
        if not ok:
            failures.append({'id': cid, 'expected': expected, 'actual': actual})

    try:
        data = json.loads(Path(a.candidate).read_text())
    except Exception as e:  # noqa: BLE001
        data = None
        check('candidate-json', False, 'valid corrections.json', f'{e}')
    originals = Path(a.originals)
    half_file = here / f'half-{a.half}.txt'
    expected_bundles = sorted(half_file.read_text().split()) if half_file.is_file() else []
    check('half-list', bool(expected_bundles), 'a half list beside the checker', str(half_file))
    check('originals-readable', any(originals.rglob('*.md')) if originals.is_dir() else False,
          'the original Charts readable inside the checker workspace', str(originals))

    if data is not None and expected_bundles and originals.is_dir():
        reported = {b.get('bundle'): b for b in data.get('bundles', [])}
        check('bundles-covered', sorted(reported) == expected_bundles,
              f'{len(expected_bundles)} bundles reported once each',
              f'{len(reported)} reported; missing {sorted(set(expected_bundles) - set(reported))[:5]}; '
              f'extra {sorted(set(reported) - set(expected_bundles))[:5]}')
        changed_any = 0
        for bundle in expected_bundles:
            rec = reported.get(bundle)
            if not rec:
                continue
            orig_files = sorted(str(q.relative_to(originals / bundle)) for q in (originals / bundle).rglob('*.md'))
            rep_files = {f.get('path'): f for f in rec.get('files', [])}
            check(f'{bundle}:files-listed', sorted(rep_files) == orig_files,
                  f'every .md file listed once ({len(orig_files)})', f'{sorted(rep_files)}')
            for rel, f in rep_files.items():
                src = originals / bundle / rel
                if not src.is_file() or f.get('status') == 'clean':
                    check(f'{bundle}:{rel}:clean-carries-no-text', not f.get('text'),
                          'a clean file carries no corrected text', 'text present')
                    # A heading template asking for a *title* asks for a claim, so a file
                    # carrying one cannot be clean. "{Short title of the decision}" was
                    # corrected twice and missed once. A *name* placeholder is excluded on
                    # purpose: "# {Context Name}" names a bounded context and claims nothing.
                    if src.is_file():
                        left = [i + 1 for i, line in enumerate(src.read_text().split('\n'))
                                if TITLE_TEMPLATE.match(line)]
                        check(f'{bundle}:{rel}:clean-has-no-title-template', not left,
                              'a file reported clean carries no "{... title ...}" heading template',
                              f'lines {left[:4]}')
                    continue
                changed_any += 1
                n = f.get('text')
                if not isinstance(n, str) or not n.strip():
                    check(f'{bundle}:{rel}:text', False, 'the corrected file text in "text"', f'{type(n).__name__}')
                    continue
                o = src.read_text()
                check(f'{bundle}:{rel}:differs', o != n, 'corrected text differs from the original', 'identical')
                check(f'{bundle}:{rel}:frontmatter', frontmatter(o) == frontmatter(n), 'frontmatter byte-identical', 'changed')
                named = {c.get('line') for c in f.get('changes', [])}
                ol, nl = o.split('\n'), n.split('\n')
                check(f'{bundle}:{rel}:length', abs(len(nl) - len(ol)) <= max(6, len(ol) // 10),
                      'line count within 10% or 6 lines', f'{len(ol)} -> {len(nl)}')
                if len(nl) == len(ol):
                    unnamed = [i + 1 for i, (x, y) in enumerate(zip(ol, nl)) if x != y and (i + 1) not in named]
                    check(f'{bundle}:{rel}:only-named-lines', not unnamed, 'only reported lines change',
                          f'unreported changes at {unnamed[:8]}')
                for rx, why in BANNED:
                    hits = [i + 1 for i, line in enumerate(nl) if rx.search(line)]
                    check(f'{bundle}:{rel}:banned', not hits, f'no line that {why}', f'lines {hits[:6]}')
                bad = [(i + 1, b) for i, line in enumerate(nl)
                       if (i + 1) in named or len(nl) != len(ol) for b in bad_examples(line)]
                check(f'{bundle}:{rel}:example-heading', not bad,
                      'every example heading is eight words or fewer with no semicolon', f'{bad[:4]}')
                leaked = [i + 1 for i, line in enumerate(nl) if LEAKED_INSTRUCTION.search(line)]
                check(f'{bundle}:{rel}:no-leaked-instruction', not leaked,
                      'a required-contents item states what the document contains, not how to write its heading',
                      f'lines {leaked[:6]}')
                repeats = [i + 1 for i, line in enumerate(nl) if TEST_PHRASE.search(line)]
                check(f'{bundle}:{rel}:test-stated-once', len(repeats) <= 1,
                      'the cover-the-body test appears at most once in a file',
                      f'{len(repeats)} times, lines {repeats[:6]}')
        # Half b delivered one stock sentence pasted into ten of eleven changes, appended to
        # whatever paragraph ended the section. A sentence repeated across files is the
        # copying failure this job exists to remove, wearing the corrector's clothes.
        stock = Counter()
        where = {}
        for bundle in expected_bundles:
            for f in (reported.get(bundle) or {}).get('files', []):
                if f.get('status') != 'changed':
                    continue
                seen = set()
                for ch in f.get('changes', []):
                    before, after = ch.get('before', ''), ch.get('after', '')
                    for sent in re.split(r'(?<=[.!?])\s+', after):
                        sent = sent.strip()
                        if len(sent) > 25 and sent not in before and sent not in seen:
                            seen.add(sent)
                            stock[sent] += 1
                            where.setdefault(sent, []).append(f"{bundle}/{f.get('path')}")
        repeated = [(t, n) for t, n in stock.items() if n > 2]
        check('no-stock-sentence', not repeated,
              'no added sentence appears in more than two files of the half',
              '; '.join(f'{n}x {t[:60]!r} in {", ".join(where[t][:4])}' for t, n in repeated[:3]))
        if 'explainer' in expected_bundles:
            check('explainer-changed',
                  any(f.get('status') == 'changed' for f in reported.get('explainer', {}).get('files', [])),
                  'the known-bad explainer Chart is changed', 'not changed')
        check('some-change', changed_any > 0, 'at least one file corrected', '0')

    report = {'version': 1, 'pass': not failures, 'checks': checks, 'failures': failures}
    Path(a.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'pass': report['pass'], 'checks': checks, 'failures': len(failures)}))
    return 0 if report['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
