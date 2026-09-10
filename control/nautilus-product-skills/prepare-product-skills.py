#!/usr/bin/env python3
"""Install manufacturer skills into the release as the product tier, verbatim.

Product skills (owner amendment 2026-09-10) are published by the maker of a paid
product, installed byte-for-byte from the manufacturer's repository at a pinned
commit, never capped and never edited locally. This script is the only path
that puts them into a release:

  prepare-product-skills.py --source <checkout> --commit <40-hex> --manufacturer <name>
      --repository <https url> --skills a,b,c [--apply]

It copies each named skill directory from the checkout into
release/charts/product-skills/bundles/<name>/ exactly (no edits, no filtering
beyond VCS metadata), writes the plugin manifest, catalog and provenance record,
adds `productSkills` provenance (with the content digest the runtime will
verify) and `allowance.product: null` to release/skill-capacity.json, and adds
each skill's frontmatter description to release/skill-purposes.json. Without
--apply it only reports what it would do. Digest law matches
src/skill-package.ts productBundleDigest: sha256 of the JSON list of
[path-relative-to-bundle, sha256(bytes)] sorted by path.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RELEASE = REPO / 'release'
FOLDER = 'charts/product-skills'
NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
SKIP = {'.git', '.DS_Store'}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def frontmatter_description(text: str) -> str:
    m = re.match(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not m:
        raise SystemExit('SKILL.md without frontmatter')
    import yaml  # PyYAML is present in the workspace toolchain
    desc = yaml.safe_load(m.group(1)).get('description')
    if not isinstance(desc, str) or not desc.strip():
        raise SystemExit('SKILL.md frontmatter without a description')
    return desc

def bundle_digest(bundle: Path) -> str:
    listed = []
    for p in sorted(x for x in bundle.rglob('*') if x.is_file() and not (set(x.relative_to(bundle).parts) & SKIP)):
        listed.append([p.relative_to(bundle).as_posix(), sha256(p.read_bytes())])
    return sha256(json.dumps(listed, separators=(',', ':')).encode())

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True); ap.add_argument('--commit', required=True)
    ap.add_argument('--manufacturer', required=True); ap.add_argument('--repository', required=True)
    ap.add_argument('--skills', required=True); ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    src = Path(a.source).resolve()
    if not re.fullmatch(r'[0-9a-f]{40}', a.commit): raise SystemExit('commit must be 40 hex')
    head = subprocess.run(['git', '-C', str(src), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    if head != a.commit: raise SystemExit(f'source checkout is at {head}, not the pinned {a.commit}')
    if subprocess.run(['git', '-C', str(src), 'status', '--porcelain'], capture_output=True, text=True).stdout.strip():
        raise SystemExit('source checkout is dirty; product skills come from a clean pinned commit')
    names = [n for n in a.skills.split(',') if n]
    for n in names:
        if not NAME.match(n) or not (src / n / 'SKILL.md').is_file(): raise SystemExit(f'not a skill at the pinned commit: {n}')
    dest = RELEASE / FOLDER
    plan = []
    for n in names:
        d = bundle_digest(src / n)
        plan.append({'name': n, 'files': sum(1 for x in (src / n).rglob('*') if x.is_file()), 'contentDigest': d,
                     'purpose': frontmatter_description((src / n / 'SKILL.md').read_text())})
    print(json.dumps({'release': str(RELEASE), 'folder': FOLDER, 'commit': a.commit, 'skills': plan}, indent=1))
    if not a.apply: print('(preflight only; pass --apply to write)'); return 0
    if dest.exists(): shutil.rmtree(dest)
    (dest / 'bundles').mkdir(parents=True)
    for n in names:
        shutil.copytree(src / n, dest / 'bundles' / n, ignore=shutil.ignore_patterns(*SKIP))
        if bundle_digest(dest / 'bundles' / n) != next(p['contentDigest'] for p in plan if p['name'] == n):
            raise SystemExit(f'copy of {n} does not digest to the source; refusing')
    (dest / '.claude-plugin').mkdir()
    (dest / '.claude-plugin/plugin.json').write_text(json.dumps({'name': 'nautilus-product', 'version': a.commit[:12], 'skills': './bundles/',
        'description': f'Manufacturer skills installed verbatim from {a.repository} at {a.commit}. Never edited locally.'}, indent=2) + '\n')
    (dest / 'catalog.json').write_text(json.dumps({'schemaVersion': 1, 'generatedFrom': 'scripts/prepare-product-skills.py',
        'groups': {a.manufacturer.lower().replace(' ', '-'): [{'name': n, 'entrypoint': f'bundles/{n}/SKILL.md', 'description': p['purpose'], 'disableModelInvocation': False, 'userInvocationRequired': False}
                   for n, p in zip(names, plan)]}}, indent=2) + '\n')
    (dest / 'provenance.json').write_text(json.dumps({'version': 1, 'manufacturer': a.manufacturer, 'repository': a.repository, 'commit': a.commit,
        'rule': 'Installed verbatim; never edited locally; update only by re-syncing to a newer upstream commit and re-running this script.',
        'skills': {p['name']: {'files': p['files'], 'contentDigest': p['contentDigest']} for p in plan}}, indent=2) + '\n')
    policy_path = RELEASE / 'skill-capacity.json'; policy = json.loads(policy_path.read_text())
    policy['allowance']['product'] = None
    policy['productSkills'] = {f'nautilus-product:{p["name"]}': {'category': 'product', 'updateAuthority': 'manufacturer', 'manufacturer': a.manufacturer,
        'repository': a.repository, 'commit': a.commit, 'contentDigest': p['contentDigest']} for p in plan}
    policy_path.write_text(json.dumps(policy, indent=2) + '\n')
    purposes_path = RELEASE / 'skill-purposes.json'; purposes = json.loads(purposes_path.read_text())
    for p in plan: purposes['purposes'][f'nautilus-product:{p["name"]}'] = p['purpose']
    purposes_path.write_text(json.dumps(purposes, indent=2) + '\n')
    print(f'applied: {len(names)} product skills under {dest}; policy and purposes updated')
    return 0

if __name__ == '__main__':
    sys.exit(main())
