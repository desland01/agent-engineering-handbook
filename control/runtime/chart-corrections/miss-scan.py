#!/usr/bin/env python3
"""Review aid, not an acceptance check: list heading-instruction phrases in files a worker
reported clean, so the judged review looks where a miss would hide.

Its triggers are heuristic and produce legitimate non-defects - "# {Context Name}" names a
bounded context, which has nothing to claim - so it never gates a ticket. Usage:
    miss-scan.py --corrections <corrections.json> --originals <dir>
"""
import argparse, json, re
from pathlib import Path

TRIGGERS = [
    (re.compile(r'descriptive heading', re.I), 'descriptive heading'),
    (re.compile(r'\bshort,? (?:clear )?(?:title|name|label)\b', re.I), 'short title/name'),
    (re.compile(r'\b(?:title|heading|name)s? (?:that )?(?:names?|describ\w+|summari[sz]\w+)\b', re.I), 'names/describes'),
    (re.compile(r'noun[- ]phrase', re.I), 'noun phrase'),
    (re.compile(r'\b(?:one|two|three|four|five|\d+)[-\s]word\b', re.I), 'word count'),
    (re.compile(r'^#{1,4} \{[^}]*(?:title|name)[^}]*\}', re.I | re.M), 'title placeholder'),
]

a = argparse.ArgumentParser(); a.add_argument('--corrections', required=True); a.add_argument('--originals', required=True)
args = a.parse_args()
d = json.loads(Path(args.corrections).read_text()); base = Path(args.originals)
changed = {(b['bundle'], f['path']) for b in d['bundles'] for f in b['files'] if f['status'] == 'changed'}
found = 0
for b in sorted({x['bundle'] for x in d['bundles']}):
    for q in sorted((base / b).rglob('*.md')):
        rel = str(q.relative_to(base / b))
        if (b, rel) in changed:
            continue
        text = q.read_text()
        for rx, why in TRIGGERS:
            m = rx.search(text)
            if m:
                line = text[:m.start()].count('\n') + 1
                print(f'  {b}/{rel}:{line}  [{why}]  {text.splitlines()[line-1].strip()[:120]}')
                found += 1
                break
print(f'{found} candidate miss(es) for the judged review')
