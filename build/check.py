#!/usr/bin/env python3
"""Local checks for the Agent Engineering Handbook.

Run after `python3 build/render.py`:

    python3 build/check.py

Checks (repository, not third-party application, behavior):
  1. public/ exists and contains exactly 13 guide pages, 4 skill entrypoints,
     12 full-size frames, the root pages, the stylesheet, the script and 404.html.
  2. Every href/src in public/*.html resolves to a file inside public/ (no
     directory traversal, no missing target). Root-absolute links (used by
     404.html, which is served at any path) resolve against public/ itself.
  3. Screenshot SHA-256 hashes match evidence/frame-manifest.json.
  4. Skill frontmatter delimiters and required interface fields are present.
     Full YAML validation is a separate authoring check.
  5. Page semantics: one h1 per page, a skip link and a main landmark, alt text
     on every image, unique ids, every in-page anchor present.
  6. Progressive disclosure holds: the home page carries the 8 problem rows,
     4 skill tiles, 3 investigation tiles, a taste of the ideas and routes to
     ideas.html, guides.html and the gallery, with its counts strip equal to
     the sets; ideas.html holds 19 idea tiles that each open one of 19 idea
     pages; guides.html holds 13 guide tiles linking every guide page; the
     gallery holds 12 frames and the home page links each one.
  7. No network dependency in any page (no external stylesheet, script, font
     or image). Layout and visual rules are verified on real renders, not by
     searching the stylesheet for phrases.

Requires only the Python standard library.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import sys

REPO = Path(__file__).resolve().parent.parent
PUBLIC = REPO / 'public'

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


class PageScan(HTMLParser):
    """Counts and ids for one page: h1s, images without alt, ids, anchors, externals."""

    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.imgs_without_alt = 0
        self.ids = []
        self.anchors = []
        self.skip = False
        self.main = False
        self.network = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if tag == 'img' and not (a.get('alt') or '').strip():
            self.imgs_without_alt += 1
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'a':
            href = a.get('href', '')
            if href.startswith('#'):
                self.anchors.append(href[1:])
            if a.get('class') == 'skip' and href == '#main':
                self.skip = True
        if tag == 'main' and a.get('id') == 'main':
            self.main = True
        if tag in ('link', 'script', 'img', 'iframe', 'video', 'audio', 'source'):
            target = a.get('href') if tag == 'link' else a.get('src')
            if target and re.match(r'^(https?:)?//', target):
                self.network.append(target)


def main():
    check(PUBLIC.is_dir(), 'public/ is missing — run `python3 build/render.py` first')

    # 1. Counts and required files.
    guides = sorted((PUBLIC / 'guides').glob('*.html')) if (PUBLIC / 'guides').is_dir() else []
    check(len(guides) == 13, f'expected 13 guide pages in public/guides, found {len(guides)}')
    skills = sorted(p.name for p in (PUBLIC / 'skills').glob('*')) if (PUBLIC / 'skills').is_dir() else []
    check(skills == ['agent-context-calibration', 'agent-feedback-engineering',
                     'agent-ready-workspaces', 'agent-tool-adapters'],
          f'unexpected skill directories in public/skills: {skills}')
    for s in skills:
        check((PUBLIC / 'skills' / s / 'SKILL.md').is_file(), f'public/skills/{s}/SKILL.md missing')
    frames = sorted((PUBLIC / 'screenshots').glob('*.jpg')) if (PUBLIC / 'screenshots').is_dir() else []
    check(len(frames) == 12, f'expected 12 frames in public/screenshots, found {len(frames)}')
    for page in ['index.html', 'ideas.html', 'guides.html', 'README.html', 'adoption.html', 'prompts.html',
                 'validation.html', 'evidence.html', 'github-inspection.html',
                 'matt-pocock-inspection.html', 'boris-cherny-inspection.html',
                 '404.html', 'assets/handbook.css', 'assets/handbook.js']:
        check((PUBLIC / page).is_file(), f'public/{page} missing')

    # 2. href/src resolution, confined to public/.
    attrs = re.compile(r'(?:href|src)="([^"]+)"')
    external = re.compile(r'^(https?:|mailto:|data:|#)')
    pages = list(PUBLIC.rglob('*.html'))
    for page in pages:
        text = page.read_text()
        for target in attrs.findall(text):
            if external.match(target):
                continue
            path = target.split('#')[0].split('?')[0]
            if not path:
                continue
            base = PUBLIC if path.startswith('/') else page.parent
            resolved = (base / path.lstrip('/')).resolve()
            check(resolved.is_relative_to(PUBLIC.resolve()),
                  f'{page.relative_to(PUBLIC)}: link escapes public/: {target}')
            check(resolved.is_file() or (resolved.is_dir() and (resolved / "index.html").is_file()),
                  f'{page.relative_to(PUBLIC)}: unresolved link: {target}')

    # 3. Frame hashes vs the manifest.
    manifest = json.loads((PUBLIC / 'evidence/frame-manifest.json').read_text())
    for f in manifest:
        img = PUBLIC / 'screenshots' / f['file']
        digest = hashlib.sha256(img.read_bytes()).hexdigest() if img.is_file() else None
        check(digest == f['sha256'], f"hash mismatch for screenshots/{f['file']}")

    # 4. Skill frontmatter and interface metadata.
    for s in skills:
        skill = PUBLIC / 'skills' / s
        text = (skill / 'SKILL.md').read_text()
        check(text.startswith('---\n'), f'{s}/SKILL.md: missing frontmatter')
        yaml = (skill / 'agents/openai.yaml').read_text()
        check(f'${s}' in yaml, f'{s}/agents/openai.yaml: default prompt lacks ${s}')
        check('display_name' in yaml and 'short_description' in yaml,
              f'{s}/agents/openai.yaml: missing interface fields')

    # 5. Page semantics.
    for page in pages:
        rel = page.relative_to(PUBLIC)
        scan = PageScan()
        scan.feed(page.read_text())
        check(scan.h1 == 1, f'{rel}: expected exactly one h1, found {scan.h1}')
        check(scan.imgs_without_alt == 0, f'{rel}: {scan.imgs_without_alt} image(s) without alt text')
        check(scan.skip and scan.main, f'{rel}: missing skip link to #main or <main id="main">')
        dupes = sorted({i for i in scan.ids if scan.ids.count(i) > 1})
        check(not dupes, f'{rel}: duplicate ids {dupes}')
        missing = sorted({a for a in scan.anchors if a and a not in scan.ids})
        check(not missing, f'{rel}: in-page anchors without a target {missing}')
        check(not scan.network, f'{rel}: loads from the network: {scan.network}')

    # 6. Progressive disclosure: home routes out; the section pages hold the sets.
    index = (PUBLIC / 'index.html').read_text() if (PUBLIC / 'index.html').is_file() else ''
    ideas_html = (PUBLIC / 'ideas.html').read_text() if (PUBLIC / 'ideas.html').is_file() else ''
    guides_html = (PUBLIC / 'guides.html').read_text() if (PUBLIC / 'guides.html').is_file() else ''
    check(index.count('class="tile skill"') == 4, f'index.html: expected 4 skill tiles, found {index.count("class=\"tile skill\"")}')
    check(index.count('class="tile report"') == 3, f'index.html: expected 3 investigation tiles, found {index.count("class=\"tile report\"")}')
    taste = re.search(r'<ol class="ideas taste"[^>]*>(.*?)</ol>', index, re.S)
    n_taste = taste.group(1).count('<li>') if taste else 0
    check(0 < n_taste < 19, f'index.html: expected a taste of the ideas (1–18 tiles), found {n_taste}')
    pick = re.search(r'<div class="pick">.*?<ol[^>]*>(.*?)</ol>', index, re.S)
    n_pick = pick.group(1).count('<li>') if pick else 0
    check(n_pick == 8, f'index.html: expected 8 problem rows, found {n_pick}')
    for route in ('href="ideas.html"', 'href="guides.html"', 'href="evidence.html"'):
        check(route in index, f'index.html: no route {route}')
    strip = dict(re.findall(r'<li><a href="([^"]+)"><span>(\d+)</span>', index))
    check(strip == {'ideas.html': '19', 'guides.html': '13', '#skills': '4', '#reports': '3', 'evidence.html': '12'},
          f'index.html: contents strip {strip} does not match the sets')
    for s in skills:
        check(f'href="skills/{s}/SKILL.md"' in index, f'index.html: skill tile for {s} does not link to its copied SKILL.md')
    for f in manifest:
        check(f'href="evidence.html#frame-{f["seconds"]}"' in index, f'index.html: no link to frame-{f["seconds"]}')

    idea_pages = sorted((PUBLIC / 'ideas').glob('*.html')) if (PUBLIC / 'ideas').is_dir() else []
    check(len(idea_pages) == 19, f'expected 19 idea pages in public/ideas, found {len(idea_pages)}')
    n_ideas = ideas_html.count('class="tile idea"')
    check(n_ideas == 19, f'ideas.html: expected 19 idea tiles, found {n_ideas}')
    for ip in idea_pages:
        check(f'href="ideas/{ip.name}"' in ideas_html, f'ideas.html: no tile opens ideas/{ip.name}')
        text = ip.read_text()
        check('youtube.com/watch' in text, f'ideas/{ip.name}: no link to the video moment')
    check(guides_html.count('class="tile guide"') == 13, f'guides.html: expected 13 guide tiles, found {guides_html.count("class=\"tile guide\"")}')
    for g in guides:
        check(f'href="guides/{g.name}"' in guides_html, f'guides.html: no tile links to guides/{g.name}')

    if failures:
        print(f'FAIL ({len(failures)}):')
        for f in failures:
            print(f'  - {f}')
        sys.exit(1)
    print(f'PASS: {len(pages)} HTML pages, {len(guides)} guides, {len(idea_pages)} idea pages, {len(skills)} skills, '
          f'{len(frames)} frames verified; links, hashes, semantics, disclosure routes, no network loads and required metadata fields OK.')


if __name__ == '__main__':
    main()
