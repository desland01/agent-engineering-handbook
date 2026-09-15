#!/usr/bin/env python3
"""Install manufacturer skills into the release as the product tier, verbatim.

Product skills (owner amendment 2026-09-10) are published by the maker of a paid
product, installed byte-for-byte from the manufacturer's repository at a pinned
commit, never edited locally, and counted in their own product category against
the same finite limit of 50 as core and domain — never uncapped, never borrowed
from another category. This script is the only path
that puts them into a release:

  prepare-product-skills.py --source <checkout> --commit <40-hex> --manufacturer <name>
      --repository <https url> --skills a,b,c [--provenance <record>] [--apply]

The source must be proven to be the pinned commit before anything is copied. A
source that is itself a git work tree is proven by its own HEAD and a clean
status. An exported source with no VCS metadata of its own is proven only
against a pinned provenance record — `--provenance <file>`, or the conventional
`<source>/../product-skills/provenance-<commit[:8]>.json` — whose commit, per
skill file count and per skill contentDigest must all match what is about to be
installed. Without one of those two proofs the script refuses; it never trusts
an enclosing repository's HEAD.

It copies each named skill directory from the checkout into
release/charts/product-skills/bundles/<name>/ exactly (no edits, no filtering
beyond VCS metadata), merges the plugin manifest, catalog group and provenance
record for this manufacturer into whatever other manufacturers the release
already carries (only the named bundles are ever replaced), adds `productSkills`
provenance (with the content digest the runtime will verify) and
`allowance.product: 50` to release/skill-capacity.json, and adds each skill's
frontmatter description to release/skill-purposes.json. Without --apply it only
reports what it would do. Digest law matches
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

def pinned_provenance(src: Path, commit: str, explicit: str | None) -> dict | None:
    """The record that pins this commit's bytes, or None when none was given or found."""
    path = Path(explicit).resolve() if explicit else (src.parent / 'product-skills' / f'provenance-{commit[:8]}.json')
    if not path.is_file():
        if explicit: raise SystemExit(f'no provenance record at {path}')
        return None
    record = json.loads(path.read_text())
    if record.get('commit') != commit: raise SystemExit(f'{path} pins {record.get("commit")}, not {commit}')
    return record

def verify_pinned_source(src: Path, commit: str, record: dict | None) -> str:
    """Prove the source is the pinned commit: by its own VCS metadata, else by a pinned record."""
    top = subprocess.run(['git', '-C', str(src), 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    if top and Path(top).resolve() == src:
        head = subprocess.run(['git', '-C', str(src), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        if head != commit: raise SystemExit(f'source checkout is at {head}, not the pinned {commit}')
        if subprocess.run(['git', '-C', str(src), 'status', '--porcelain'], capture_output=True, text=True).stdout.strip():
            raise SystemExit('source checkout is dirty; product skills come from a clean pinned commit')
        return 'git'
    if record is None:
        raise SystemExit(f'source {src} is not a git work tree of its own, and no provenance record pins {commit} '
                         f'(pass --provenance, or place {src.parent}/product-skills/provenance-{commit[:8]}.json); '
                         'refusing to take an enclosing repository as proof of the pinned commit')
    return 'provenance'

def verify_against_record(plan: list, record: dict) -> None:
    """Every skill about to be installed must digest to the bytes the record pins."""
    pinned = record.get('skills') or {}
    for p in plan:
        want = pinned.get(p['name'])
        if want is None: raise SystemExit(f'provenance record does not pin {p["name"]}')
        if want.get('contentDigest') != p['contentDigest']:
            raise SystemExit(f'{p["name"]} digests to {p["contentDigest"]}, not the pinned {want.get("contentDigest")}')
        if want.get('files') != p['files']:
            raise SystemExit(f'{p["name"]} has {p["files"]} files, not the pinned {want.get("files")}')

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True); ap.add_argument('--commit', required=True)
    ap.add_argument('--manufacturer', required=True); ap.add_argument('--repository', required=True)
    ap.add_argument('--skills', required=True); ap.add_argument('--provenance')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    src = Path(a.source).resolve()
    if not re.fullmatch(r'[0-9a-f]{40}', a.commit): raise SystemExit('commit must be 40 hex')
    record = pinned_provenance(src, a.commit, a.provenance)
    proof = verify_pinned_source(src, a.commit, record)
    names = [n for n in a.skills.split(',') if n]
    for n in names:
        if not NAME.match(n) or not (src / n / 'SKILL.md').is_file(): raise SystemExit(f'not a skill at the pinned commit: {n}')
    dest = RELEASE / FOLDER
    plan = []
    for n in names:
        d = bundle_digest(src / n)
        plan.append({'name': n, 'files': sum(1 for x in (src / n).rglob('*') if x.is_file()), 'contentDigest': d,
                     'purpose': frontmatter_description((src / n / 'SKILL.md').read_text())})
    if record is not None: verify_against_record(plan, record)
    print(json.dumps({'release': str(RELEASE), 'folder': FOLDER, 'commit': a.commit, 'pinnedBy': proof, 'skills': plan}, indent=1))
    if not a.apply: print('(preflight only; pass --apply to write)'); return 0
    # Merge, never wipe: a release may already carry another manufacturer's
    # skills. Only the named bundles are (re)copied; every other vendor's
    # bundle, catalog group, provenance entry and pin survives untouched.
    group = a.manufacturer.lower().replace(' ', '-')
    (dest / 'bundles').mkdir(parents=True, exist_ok=True)
    for n in names:
        target = dest / 'bundles' / n
        if target.exists(): shutil.rmtree(target)
        shutil.copytree(src / n, target, ignore=shutil.ignore_patterns(*SKIP))
        if bundle_digest(target) != next(p['contentDigest'] for p in plan if p['name'] == n):
            raise SystemExit(f'copy of {n} does not digest to the source; refusing')
    manifest_path = dest / '.claude-plugin' / 'plugin.json'
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {}
    manifest.update({'name': 'nautilus-product', 'version': a.commit[:12], 'skills': './bundles/'})
    if 'description' not in manifest:
        manifest['description'] = f'Manufacturer skills installed verbatim from {a.repository} at {a.commit}. Never edited locally.'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    catalog_path = dest / 'catalog.json'
    catalog = json.loads(catalog_path.read_text()) if catalog_path.is_file() else {'schemaVersion': 1, 'generatedFrom': 'scripts/prepare-product-skills.py', 'groups': {}}
    catalog['groups'][group] = [{'name': n, 'entrypoint': f'bundles/{n}/SKILL.md', 'description': p['purpose'], 'disableModelInvocation': False, 'userInvocationRequired': False}
                                for n, p in zip(names, plan)]
    catalog_path.write_text(json.dumps(catalog, indent=2) + '\n')
    provenance_path = dest / 'provenance.json'
    provenance = json.loads(provenance_path.read_text()) if provenance_path.is_file() else {}
    provenance.update({'version': 1, 'manufacturer': a.manufacturer, 'repository': a.repository, 'commit': a.commit,
                       'rule': 'Installed verbatim; never edited locally; update only by re-syncing to a newer upstream commit and re-running this script.'})
    skills = provenance.get('skills') or {}
    for n, p in zip(names, plan):
        skills[n] = {'files': p['files'], 'contentDigest': p['contentDigest'], 'repository': a.repository, 'commit': a.commit}
    provenance['skills'] = skills
    provenance_path.write_text(json.dumps(provenance, indent=2) + '\n')
    policy_path = RELEASE / 'skill-capacity.json'; policy = json.loads(policy_path.read_text())
    # The product tier is a version-3 declaration: its own finite 50, like core
    # and domain. A version-1 or version-2 policy cannot classify manufacturer
    # skills, so refuse instead of writing a policy the runtime would reject.
    if policy.get('version') != 3:
        raise SystemExit(f'{policy_path} is version {policy.get("version")}; product skills need the version-3 policy (target 35, allowance 50 per category)')
    policy.setdefault('allowance', {})['product'] = 50
    product_skills = policy.get('productSkills') or {}
    for n, p in zip(names, plan):
        product_skills[f'nautilus-product:{n}'] = {'category': 'product', 'updateAuthority': 'manufacturer', 'manufacturer': a.manufacturer,
            'repository': a.repository, 'commit': a.commit, 'contentDigest': p['contentDigest']}
    policy['productSkills'] = product_skills
    policy_path.write_text(json.dumps(policy, indent=2) + '\n')
    purposes_path = RELEASE / 'skill-purposes.json'; purposes = json.loads(purposes_path.read_text())
    for p in plan: purposes['purposes'][f'nautilus-product:{p["name"]}'] = p['purpose']
    purposes_path.write_text(json.dumps(purposes, indent=2) + '\n')
    print(f'applied: {len(names)} product skills under {dest}; policy and purposes updated')
    return 0

if __name__ == '__main__':
    sys.exit(main())
