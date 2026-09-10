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
SITE_NAME = 'Agent Engineering Handbook'
# render.py's production origin, read rather than imported: this checker runs
# on a plain interpreter, and importing render would drag in Markdown with it.
SITE_URL = re.search(r"^SITE_URL = '([^']*)'", (REPO / 'build/render.py').read_text(),
                     re.M).group(1)
sys.path.insert(0, str(REPO / 'build'))
from icons import GUIDES, INVESTIGATIONS, SKILLS   # noqa: E402  (authored drawings)

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
            # rel="canonical" names this page's own address for a crawler. It
            # is metadata, not a fetch, and is the one absolute href the page
            # is allowed to carry.
            if a.get('rel') == 'canonical':
                target = None
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
    for page in ['index.html', 'ideas.html', 'guides.html', 'skills.html', 'investigations.html',
                 'README.html', 'adoption.html', 'prompts.html',
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

        # Page identity: a title that names the page and a description that
        # says what is on it. Both are what a search result or a shared link
        # shows, and neither is visible while reading, so only a check keeps
        # them honest. The length bound is the roughly 155 characters a result
        # displays; a description cut mid-word reads as broken.
        title = re.search(r'<title>(.*?)</title>', page.read_text(), re.S)
        title = title.group(1).strip() if title else ''
        check(title and title != SITE_NAME and not title.startswith(f'{SITE_NAME} · '),
              f'{rel}: title does not name the page: {title!r}')
        desc = re.search(r'<meta name="description" content="([^"]*)"', page.read_text())
        desc = desc.group(1).strip() if desc else ''
        check(desc, f'{rel}: no meta description')
        check(len(desc) <= 175, f'{rel}: meta description is {len(desc)} characters, over 175')
        check(not desc.endswith(('...', '…')), f'{rel}: meta description is truncated: {desc!r}')

        # Canonical URL and share tags are all-or-nothing. Until render.py's
        # SITE_URL names a production origin they must be absent everywhere: a
        # canonical pointing at the wrong host is worse than none. Once it is
        # set, every page but 404.html — served at any path, so it has no one
        # address — must carry one that matches where the page actually sits.
        text = page.read_text()
        canonical = re.search(r'<link rel="canonical" href="([^"]*)"', text)
        if not SITE_URL:
            check(not canonical, f'{rel}: has a canonical URL while SITE_URL is unset')
            check('og:url' not in text, f'{rel}: has Open Graph tags while SITE_URL is unset')
        elif rel.as_posix() != '404.html':
            expect = SITE_URL + ('/' if rel.as_posix() == 'index.html' else '/' + rel.as_posix())
            check(canonical and canonical.group(1) == expect,
                  f'{rel}: canonical is {canonical.group(1) if canonical else "missing"}, expected {expect}')
            check(f'content="{expect}"' in text, f'{rel}: og:url does not match its canonical')

    # 6. Progressive disclosure: home routes out; the section pages hold the sets.
    index = (PUBLIC / 'index.html').read_text() if (PUBLIC / 'index.html').is_file() else ''
    ideas_html = (PUBLIC / 'ideas.html').read_text() if (PUBLIC / 'ideas.html').is_file() else ''
    guides_html = (PUBLIC / 'guides.html').read_text() if (PUBLIC / 'guides.html').is_file() else ''
    skills_html = (PUBLIC / 'skills.html').read_text() if (PUBLIC / 'skills.html').is_file() else ''
    reports_html = (PUBLIC / 'investigations.html').read_text() if (PUBLIC / 'investigations.html').is_file() else ''
    check(index.count('class="tile skill"') == 4, f'index.html: expected 4 skill tiles, found {index.count("class=\"tile skill\"")}')
    # The home page carries all nineteen ideas as one horizontal row inside a
    # focusable scroll region, and still routes out to the grid. Previous/next
    # and the counter are script-added, so the markup must not contain them.
    row = re.search(r'<div class="ideas-row"[^>]*>\s*<ol class="ideas track"[^>]*>(.*?)</ol>', index, re.S)
    n_row = row.group(1).count('class="tile idea"') if row else 0
    check(n_row == 19, f'index.html: expected all 19 ideas in the row, found {n_row}')
    check(row and 'role="region"' in index.split('<ol class="ideas track"')[0][-300:],
          'index.html: the ideas row is not a labelled, focusable scroll region')
    check('row-controls' not in index, 'index.html: row controls are rendered in markup; they must be script-added')
    pick = re.search(r'<div class="pick">.*?<ol[^>]*>(.*?)</ol>', index, re.S)
    n_pick = pick.group(1).count('<li>') if pick else 0
    check(n_pick == 8, f'index.html: expected 8 problem rows, found {n_pick}')
    for route in ('href="ideas.html"', 'href="guides.html"', 'href="evidence.html"',
                  'href="skills.html"', 'href="investigations.html"'):
        check(route in index, f'index.html: no route {route}')
    strip = dict(re.findall(r'<li><a href="([^"]+)"><span>(\d+)</span>', index))
    check(strip == {'ideas.html': '19', 'guides.html': '13', '#skills': '4', '#reports': '3', 'evidence.html': '12'},
          f'index.html: contents strip {strip} does not match the sets')
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

    # 6b. Skill pages: every skill directory has a generated page that carries
    # the skill's drawing and links the raw SKILL.md, its GitHub directory and
    # the adoption page. skills.html lists the whole set.
    for s in skills:
        page = PUBLIC / 'skills' / s / 'index.html'
        check(page.is_file(), f'public/skills/{s}/: no generated skill page (skills/{s}/index.html)')
        if not page.is_file():
            continue
        text = page.read_text()
        check(SKILLS[s] in text, f'skills/{s}/index.html: the skill\'s drawing is missing')
        check('href="SKILL.md"' in text, f'skills/{s}/index.html: no link to the copied SKILL.md')
        check(f'/tree/HEAD/skills/{s}' in text, f'skills/{s}/index.html: no link to its GitHub directory')
        check('href="../../adoption.html"' in text, f'skills/{s}/index.html: no link to the adoption page')
    check(skills_html.count('class="tile skill"') == 4, f'skills.html: expected 4 skill tiles, found {skills_html.count("class=\"tile skill\"")}')
    for s in skills:
        check(f'href="skills/{s}/"' in skills_html, f'skills.html: no tile opens skills/{s}/')
        check(f'href="adoption.html"' in skills_html, 'skills.html: no link to the adoption page')

    # 6b-ii. No section page dead-ends: each closes with routes to other sets,
    # and every route resolves (section 2 already proved the targets exist).
    for name in ('ideas.html', 'guides.html', 'skills.html', 'investigations.html', 'evidence.html'):
        hub = PUBLIC / name
        if not hub.is_file():
            continue
        text = hub.read_text()
        block = re.search(r'<section class="hub-next".*?</section>', text, re.S)
        check(block, f'{name}: no closing route out of the section')
        n = len(re.findall(r'<li><a href=', block.group(0))) if block else 0
        check(n >= 2, f'{name}: closing route offers {n} destinations, expected at least 2')
        if block:
            targets = set(re.findall(r'<li><a href="([^"#]+)', block.group(0)))
            check(name not in targets, f'{name}: its closing route points back at itself')

    # 6c. Investigations: the index carries the three report cards and links
    # each report; every report page shows its own drawing.
    check(reports_html.count('class="tile report"') == 3, f'investigations.html: expected 3 report tiles, found {reports_html.count("class=\"tile report\"")}')
    for rel in INVESTIGATIONS:
        page_name = rel[:-3] + '.html'
        page = PUBLIC / page_name
        check(f'href="{page_name}"' in reports_html, f'investigations.html: no card opens {page_name}')
        check(page.is_file() and INVESTIGATIONS[rel] in page.read_text(),
              f'{page_name}: the investigation\'s drawing is missing')

    # 6d. Every guide page shows its own drawing.
    for g in guides:
        m = re.match(r'(\d\d)-', g.name)
        check(m and GUIDES.get(m.group(1), '') and GUIDES[m.group(1)] in g.read_text(),
              f'guides/{g.name}: the guide\'s drawing is missing')

    if failures:
        print(f'FAIL ({len(failures)}):')
        for f in failures:
            print(f'  - {f}')
        sys.exit(1)
    print(f'PASS: {len(pages)} HTML pages, {len(guides)} guides, {len(idea_pages)} idea pages, {len(skills)} skills, '
          f'{len(frames)} frames verified; links, hashes, semantics, disclosure routes, no network loads and required metadata fields OK.')


if __name__ == '__main__':
    main()
