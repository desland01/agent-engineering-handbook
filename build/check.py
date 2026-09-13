#!/usr/bin/env python3
"""Local checks for the Agent Engineering Handbook.

Run after `python3 build/render.py`:

    python3 build/check.py

Checks (repository, not third-party application, behavior):
  1. public/ exists and contains exactly 13 guide pages, 10 lesson pages, 7 skill
     entrypoints, 12 full-size frames, 19 legacy idea aliases plus their index alias,
     the root pages, the stylesheet, the script and 404.html.
  2. Every href/src in public/*.html resolves to a file inside public/ (no
     directory traversal, no missing target). Root-absolute links (used by
     404.html, which is served at any path) resolve against public/ itself.
  3. Screenshot SHA-256 hashes match evidence/frame-manifest.json.
  4. Skill frontmatter delimiters and required interface fields are present.
     Full YAML validation is a separate authoring check.
  5. Page semantics: one h1 per page, a skip link and a main landmark, alt text
     on every image, unique ids, every in-page anchor present.
  6. Progressive disclosure holds: the home page opens with Start with lesson 1 /
     Find my problem, one quiet derived lesson count and the 8 problem rows (most
     routing to lessons), a three-chapter lesson directory, the seven installed
     skill rows, the guide shelves and three investigation rows; lessons.html
     holds the ten canonical lessons in three chapters; each lesson page keeps
     its source anchors, video links and sequence; the nineteen legacy idea
     routes are lightweight aliases whose canonicals point at their lesson;
     guides.html holds 13 guide tiles linking every guide page; the gallery
     holds 12 frames.

  7. Lesson coverage, independently of build/lesson_catalog.py: build/lessons.json
     names exactly the ten approved lesson IDs, covers all nineteen source tip IDs
     exactly once, and every legacy route has a rendered alias.
  7. No network dependency in any page (no external stylesheet, script, font
     or image). Layout and visual rules are verified on real renders, not by
     searching the stylesheet for phrases.

Requires only the Python standard library.
"""
from pathlib import Path
from html import escape
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
from icons import GUIDES, INVESTIGATIONS, SKILLS, canonical as icon_canonical   # noqa: E402  (authored drawings)

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


VOID = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'area', 'col', 'embed', 'track', 'wbr'}


class PageScan(HTMLParser):
    """Counts and ids for one page: h1s, images without alt, ids, anchors, externals."""

    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.imgs_without_alt = 0
        self.hidden_depth = 0   # open elements marked aria-hidden="true"
        self.ids = []
        self.anchors = []
        self.skip = False
        self.main = False
        self.network = []

    def handle_endtag(self, tag):
        if self.hidden_depth and tag not in VOID:
            self.hidden_depth = max(0, self.hidden_depth - 1)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        # A decorative image takes alt="" and is hidden from the accessibility tree;
        # announcing it would only repeat what the surrounding text already says. Any
        # other image still needs real alt text.
        if a.get('aria-hidden') == 'true' and tag not in VOID:
            self.hidden_depth += 1
        decorative = a.get('aria-hidden') == 'true' or self.hidden_depth > 0
        if tag == 'img' and not (a.get('alt') or '').strip() and not (decorative and 'alt' in a):
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


# The approved lesson identity, compiled here as the independent source of
# truth the manifest must agree with (section 7). It deliberately does not
# import build/lesson_catalog.py: a seam that graded itself would prove nothing.
APPROVED_LESSON_IDS = [
    'recurring-mistakes', 'ci-feedback', 'prove-it-works', 'working-previews',
    'missing-tools', 'useful-instructions', 'fresh-agent', 'shared-contracts',
    'codebase-navigation', 'better-environments',
]
APPROVED_CHAPTERS = {
    'recurring-mistakes': 'stop-repeat-work', 'ci-feedback': 'stop-repeat-work',
    'prove-it-works': 'stop-repeat-work', 'working-previews': 'give-agents-what-they-need',
    'missing-tools': 'give-agents-what-they-need', 'useful-instructions': 'give-agents-what-they-need',
    'fresh-agent': 'give-agents-what-they-need', 'shared-contracts': 'keep-it-understandable',
    'codebase-navigation': 'keep-it-understandable', 'better-environments': 'keep-it-understandable',
}


# The legacy in-page fragments the old idea URLs may still carry: Vercel
# redirects old URL#fragment to the lesson route, so each canonical lesson must
# answer every one of these fragments with a real id.
LEGACY_FRAGMENTS = ('said', 'apply', 'useful', 'qualification')


def manifest_lessons_checked():
    """Read build/lessons.json directly and hold it against the approved
    identity above and the nineteen source records; returns the records."""
    manifest = json.loads((REPO / 'build/lessons.json').read_text())
    tips = json.loads((REPO / 'evidence/video-tips.json').read_text())
    tip_ids = {t['id'] for t in tips}
    check(manifest.get('version') == 1, 'build/lessons.json: version is not 1')
    records = manifest.get('lessons', [])
    check(len(records) == 10, f'build/lessons.json: expected 10 lessons, found {len(records)}')
    ids = [r.get('id') for r in records]
    check(sorted(ids) == sorted(APPROVED_LESSON_IDS),
          f'build/lessons.json: lesson ids {sorted(ids)} are not exactly the ten approved ids')
    check(len(set(ids)) == len(ids), 'build/lessons.json: a lesson id repeats')
    check([r.get('order') for r in records] == list(range(1, 11)),
          'build/lessons.json: orders are not exactly 1..10 in file order')
    covered = []
    for r in records:
        check(r.get('chapter') == APPROVED_CHAPTERS.get(r.get('id')),
              f'build/lessons.json: {r.get("id")} is not in its approved chapter')
        covered.extend(r.get('tip_ids', []))
    duplicated = sorted({t for t in covered if covered.count(t) > 1})
    check(not duplicated,
          'build/lessons.json: a source tip is assigned twice: ' + ', '.join(duplicated))
    check(sorted(covered) == sorted(tip_ids),
          f'build/lessons.json: covered tips are not exactly the {len(tip_ids)} source ids')
    for r in records:
        for rel in r.get('legacy_paths', []):
            check(not rel.startswith('/') and '..' not in rel,
                  f'build/lessons.json: legacy path {rel!r} escapes the site')
            check((PUBLIC / rel).is_file(), f'public/{rel} missing (legacy alias not rendered)')
        r['page'] = f'lessons/{r["id"]}.html'
    return records


ROOT = PUBLIC.parent

# Source-tree layout. One file per purpose, named by what it is; the date lives inside the
# file and in git, never in the name; handoffs and other read-once files live in
# ~/ephemera, never in the repository. `python3 build/check.py --layout` runs only this
# section (the pre-commit hook in build/hooks does), the full run includes it.
DATED_NAME = re.compile(r'(?<!\d)20\d{6}(?!\d)|20\d\d-[01]\d-[0-3]\d|(?:^|[-_.])(?:v\d+|final|latest)(?:[-_.]|$)', re.I)
ROOT_ENTRIES = {
    '.github', '.gitignore', '.vercelignore', 'vercel.json', 'ATTRIBUTION.md', 'CONTRIBUTING.md',
    'DESIGN.md', 'INTERACTIONS.md', 'README.md', 'adoption.md', 'prompts.md', 'validation.md',
    'boris-cherny-inspection.md', 'github-inspection.md', 'matt-pocock-inspection.md',
    'build', 'control', 'evidence', 'examples', 'guides', 'lessons', 'public', 'screenshots',
    'skills',
}
CONTROL_FILES = {'README.md', 'plan.md', 'tickets.md', 'patterns.md', 'skill-evals.md',
                 'design-notes.md', 'design-skill-standard.md', 'design-review-capsule.md'}
CONTROL_DIRS = {'reviews', 'proposals', 'runtime'}


def tracked_files():
    import subprocess
    try:
        out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        return [Path(p) for p in out.splitlines() if p]
    except (OSError, subprocess.CalledProcessError):
        # Source archives have no Git index. Omit generated runtime directories,
        # while keeping unknown source files visible to the layout rules.
        generated = {'.git', 'node_modules', 'public', '.scratch', '.vercel',
                     '.build-deps', '.venv', '__pycache__'}
        return [p.relative_to(ROOT) for p in ROOT.rglob('*')
                if p.is_file() and not any(part in generated for part in p.relative_to(ROOT).parts)]


def layout():
    files = tracked_files()
    for rel in files:
        top = rel.parts[0]
        check(top in ROOT_ENTRIES, f'{rel}: unexpected entry at the repository root ({top})')
        check('handoff' not in rel.name.lower(), f'{rel}: handoffs live in ~/ephemera, not in the repository')
        if top in {'screenshots', 'public'}:
            continue  # frame files are named by their timecode in the video
        if top == 'control' and rel.parts[1] == 'proposals' and len(rel.parts) > 3:
            continue  # preserved source material under a proposal keeps its original names
        check(not DATED_NAME.search(rel.stem), f'{rel}: a date, version or "final" in a file name — name it by purpose')
        if top == 'control':
            if len(rel.parts) == 2:
                check(rel.name in CONTROL_FILES, f'{rel}: not a file control/README.md lists — extend an existing purpose or add it to the README first')
            else:
                check(rel.parts[1] in CONTROL_DIRS, f'{rel}: control/ subdirectories are reviews/, proposals/, runtime/')
                if rel.parts[1] == 'reviews':
                    check(len(rel.parts) == 3, f'{rel}: reviews/ holds one record per subject, no nesting')


def selftest_page_scan():
    """The decorative-image allowance must not become a hole: an image with no alt
    outside an aria-hidden scope, and one inside it that omits alt entirely, both fail."""
    def scan(html):
        s = PageScan()
        s.feed(html)
        return s.imgs_without_alt
    assert scan('<figure aria-hidden="true"><img src="a.webp" alt=""></figure>') == 0
    assert scan('<img src="a.webp" alt="" aria-hidden="true">') == 0
    assert scan('<figure aria-hidden="true"><img src="a.webp"></figure>') == 1
    assert scan('<img src="a.webp" alt="">') == 1
    assert scan('<figure aria-hidden="true"><img src="a.webp" alt=""></figure><img src="b.webp" alt="">') == 1


def _is_alias(rel):
    """A compatibility alias points its canonical at the page it duplicates,
    so the self-canonical rule does not apply to it (section 6 checks the
    alias canonicals point at their lessons instead)."""
    rel = rel.as_posix()
    return rel == 'ideas.html' or rel.startswith('ideas/')


def main():
    selftest_page_scan()
    layout()
    if '--layout' in sys.argv:
        # Layout is a source-tree check: it must pass on a source-only checkout
        # or deployment archive that has no generated public/ output, so the
        # manifest read (which needs public/ aliases) happens only after this
        # early return.
        if failures:
            for e in failures:
                print('FAIL:', e)
            sys.exit(1)
        print('PASS: source layout')
        return

    manifest_lessons = manifest_lessons_checked()

    check(PUBLIC.is_dir(), 'public/ is missing — run `python3 build/render.py` first')

    # 1. Counts and required files.
    guides = sorted((PUBLIC / 'guides').glob('*.html')) if (PUBLIC / 'guides').is_dir() else []
    check(len(guides) == 13, f'expected 13 guide pages in public/guides, found {len(guides)}')
    skills = sorted(p.name for p in (PUBLIC / 'skills').glob('*')) if (PUBLIC / 'skills').is_dir() else []
    check(skills == ['agent-artifact-recovery', 'agent-context-calibration',
                     'agent-contract-consistency', 'agent-feedback-engineering',
                     'agent-output-verification', 'agent-ready-workspaces',
                     'agent-tool-adapters'],
          f'unexpected skill directories in public/skills: {skills}')
    for s in skills:
        check((PUBLIC / 'skills' / s / 'SKILL.md').is_file(), f'public/skills/{s}/SKILL.md missing')
    frames = sorted((PUBLIC / 'screenshots').glob('*.jpg')) if (PUBLIC / 'screenshots').is_dir() else []
    check(len(frames) == 12, f'expected 12 frames in public/screenshots, found {len(frames)}')
    lesson_pages = sorted((PUBLIC / 'lessons').glob('*.html')) if (PUBLIC / 'lessons').is_dir() else []
    check(len(lesson_pages) == 10, f'expected 10 lesson pages in public/lessons, found {len(lesson_pages)}')
    for page in ['index.html', 'ideas.html', 'lessons.html', 'guides.html', 'skills.html',
                 'investigations.html',
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
        elif rel.as_posix() != '404.html' and not _is_alias(rel):
            expect = SITE_URL + ('/' if rel.as_posix() == 'index.html' else '/' + rel.as_posix())
            check(canonical and canonical.group(1) == expect,
                  f'{rel}: canonical is {canonical.group(1) if canonical else "missing"}, expected {expect}')
            check(f'content="{expect}"' in text, f'{rel}: og:url does not match its canonical')

    # 6. Progressive disclosure: home routes out; the section pages hold the sets.
    index = (PUBLIC / 'index.html').read_text() if (PUBLIC / 'index.html').is_file() else ''
    lessons_html = (PUBLIC / 'lessons.html').read_text() if (PUBLIC / 'lessons.html').is_file() else ''
    ideas_html = (PUBLIC / 'ideas.html').read_text() if (PUBLIC / 'ideas.html').is_file() else ''
    guides_html = (PUBLIC / 'guides.html').read_text() if (PUBLIC / 'guides.html').is_file() else ''
    skills_html = (PUBLIC / 'skills.html').read_text() if (PUBLIC / 'skills.html').is_file() else ''
    reports_html = (PUBLIC / 'investigations.html').read_text() if (PUBLIC / 'investigations.html').is_file() else ''

    # Home opening: two actions with fixed labels and targets, and one quiet
    # derived lesson count. The retired five-badge strip, typed prompt line,
    # horizontal idea rail, skills figure and report file cards must be gone.
    check('<a class="btn primary" href="lessons/recurring-mistakes.html">Start with lesson 1</a>' in index,
          'index.html: the primary action is not "Start with lesson 1" opening lesson 1')
    check('<a class="btn" href="#problems">Find my problem</a>' in index,
          'index.html: the secondary action is not "Find my problem"')
    check('class="contents"' not in index, 'index.html: the retired counts strip is rendered')
    check('class="prompt"' not in index, 'index.html: the retired typed prompt line is rendered')
    check('ideas-row' not in index and 'ideas track' not in index,
          'index.html: the retired horizontal idea rail is rendered')
    check('class="lanes skills"' not in index and 'class="tile skill"' not in index,
          'index.html: the retired skills figure is rendered')
    check('class="file' not in index, 'index.html: the retired report file cards are rendered')
    check('id="frames"' not in index, 'index.html: the retired frames band is rendered')
    count_line = re.search(r'<p class="count-line"><a href="lessons.html"><span class="n">(\d+)</span> lessons</a></p>', index)
    check(count_line, 'index.html: no quiet lesson count linking lessons.html')
    check(count_line and count_line.group(1) == str(len(manifest_lessons)),
          f'index.html: lesson count {count_line.group(1) if count_line else "?"} disagrees with the validated manifest')
    pick = re.search(r'<div class="pick">.*?<ul[^>]*>(.*?)</ul>', index, re.S)
    n_pick = pick.group(1).count('<li>') if pick else 0
    check(n_pick == 8, f'index.html: expected 8 problem rows, found {n_pick}')
    check(pick and 'class="ix"' not in pick.group(1),
          'index.html: problem rows introduce a second numbering system')
    check(pick and '<span class="n">Guide 12</span>' in pick.group(1),
          'index.html: the deeper guide must not look like lesson 12')
    # Semantic order follows the accepted design contract (copy, problems,
    # figure): a screen reader or a no-style reader meets the problem rows
    # before the optional artwork, exactly as the CSS lays the page out.
    pick_at = index.find('class="pick"')
    hero_at = index.find('hero-figure')
    check(pick_at != -1 and hero_at != -1 and pick_at < hero_at,
          'index.html: the problem panel does not precede the hero figure in the page order')
    for route in ('href="lessons.html"', 'href="guides.html"', 'href="skills.html"',
                  'href="investigations.html"', 'href="evidence.html"'):
        check(route in index, f'index.html: no route {route}')

    # Problem rows route to lessons (row 8 to its guide), each chip carrying the
    # destination's order number as data.
    n_lesson_chips = len(re.findall(r'class="chip" href="lessons/[\w-]+\.html"><span class="n">Lesson \d+</span>', index))
    check(n_lesson_chips == 7, f'index.html: expected 7 problem rows opening a lesson, found {n_lesson_chips}')
    check('class="chip" href="guides/12-artifact-identity-and-recovery.html"' in index,
          'index.html: problem row 8 does not open guide 12')

    # The chapter directory: one row per declared chapter, in order, each with
    # one accent mark per lesson in that chapter.
    chapters = re.findall(r'<li><a href="lessons.html#([a-z-]+)">'
                          r'<span class="range">([^<]*)</span>'
                          r'<span class="body"><span class="t">([^<]*)</span>'
                          r'<span class="k">([^<]*)</span></span>'
                          r'<span class="marks" aria-hidden="true">(<i>)*</i></span></a></li>'.replace('(<i>)*</i>', '((?:<i></i>)*)'),
                          index)
    check([c[0] for c in chapters] == ['stop-repeat-work', 'give-agents-what-they-need',
                                       'keep-it-understandable'],
          f'index.html: chapter directory rows {[c[0] for c in chapters]} are not the three declared chapters in order')
    for cid, _, _, _, marks in chapters:
        expected_marks = sum(1 for l in manifest_lessons if l['chapter'] == cid)
        check(marks.count('<i></i>') == expected_marks,
              f'index.html: chapter {cid} shows {marks.count("<i></i>")} marks, expected {expected_marks}')

    # Skill rows: seven available, derived from the packages on disk; no
    # planned rows and no in-preparation note while every package exists.
    n_available = index.count('class="status is-available"')
    check(n_available == 7, f'index.html: expected 7 available skill rows, found {n_available}')
    check('is-planned' not in index, 'index.html: planned skill rows rendered while all packages exist')
    check('rows-note' not in index, 'index.html: an in-preparation note is rendered while all packages exist')
    for s in skills:
        check(f'href="skills/{s}/"' in index, f'index.html: no skill row opens skills/{s}/')

    # Investigations: three directory rows, no per-report guide count.
    report_rows = re.findall(r'<li><a href="([\w-]+\.html)"><span class="range">Report 0\d</span>', index)
    check(sorted(report_rows) == ['boris-cherny-inspection.html', 'github-inspection.html',
                                  'matt-pocock-inspection.html'],
          f'index.html: investigation rows {report_rows} are not the three reports')

    # The lesson hub: ten rows in three chapters, in order.
    hub_chapters = re.findall(r'<section class="chapter" id="([a-z-]+)"', lessons_html)
    check(hub_chapters == ['stop-repeat-work', 'give-agents-what-they-need', 'keep-it-understandable'],
          f'lessons.html: chapter sections {hub_chapters} are not the three declared chapters in order')
    for l in manifest_lessons:
        row = re.search(r'<li class="lesson-row"><a href="' + re.escape(l['page']) + r'">.*?</a></li>',
                        lessons_html, re.S)
        check(row, f'lessons.html: no lesson row opens {l["page"]}')
        if row:
            check(escape(l['title']) in row.group(0), f'lessons.html: row for {l["id"]} lacks its title')
            check(escape(l['summary']) in row.group(0), f'lessons.html: row for {l["id"]} lacks its summary')
            # The row's metadata carries the derived reading estimate, labelled
            # as an estimate, never as a measurement.
            check(re.search(r'About \d+ min, estimated', row.group(0)),
                  f'lessons.html: row for {l["id"]} lacks its reading estimate')
    n_rows = lessons_html.count('class="lesson-row"')
    check(n_rows == 10, f'lessons.html: expected 10 lesson rows, found {n_rows}')

    # Legacy alias index: a compatibility page, not a second directory.
    check('<link rel="canonical" href="' + SITE_URL + '/lessons.html"' in ideas_html,
          'ideas.html: its canonical does not point at lessons.html')
    check('class="tile idea"' not in ideas_html, 'ideas.html: still renders the nineteen idea tiles')
    check('tier-does' not in ideas_html, 'ideas.html: still renders the evidential tier sections')

    # Lesson pages: the ten canonical readers.
    for l in manifest_lessons:
        page = PUBLIC / l['page']
        check(page.is_file(), f'public/{l["page"]} missing')
        if not page.is_file():
            continue
        text = page.read_text()
        check(f'<link rel="canonical" href="' + SITE_URL + '/' + l['page'] + '"' in text,
              f'{l["page"]}: canonical does not name its own route')
        # Every legacy fragment an old URL may carry must land on a real id on
        # its redirect destination, not on a dead anchor.
        for frag in LEGACY_FRAGMENTS:
            check(f'id="{frag}"' in text, f'{l["page"]}: legacy fragment #{frag} has no target here')
        # The derived reading estimate must be visible without the desktop rail
        # (the lesson header), and it must say it is an estimate.
        check(re.search(r'class="read-min[^"]*"[^>]*>[^<]*About \d+ min[^<]*estimated', text)
              or re.search(r'>About \d+ min[^<]*estimated', text),
              f'{l["page"]}: no derived reading estimate in the page head')
        # Every covered tip keeps its exact source anchor and a link to the video moment.
        for tip_id in l['tip_ids']:
            check(f'id="{tip_id}"' in text, f'{l["page"]}: missing source anchor for {tip_id}')
        n_video = text.count('youtube.com/watch?v=xmGY276gEFY')
        check(n_video >= len(l['tip_ids']),
              f'{l["page"]}: {n_video} video links for {len(l["tip_ids"])} covered tips')
        # The glyphs of the video moments, labelled with their count.
        check('class="tip-glyphs"' in text and 'consolidates' in text,
              f'{l["page"]}: the video-moment glyphs or their group label are missing')
        # Sequence and source line.
        check('class="guide-seq"' in text and 'Lesson sequence' in text,
              f'{l["page"]}: no lesson sequence')
        check('lesson_catalog' not in text, f'{l["page"]}: internal build name leaked into the page')
        if l['order'] == 1:
            check('href="../lessons.html"' in text, 'lessons/recurring-mistakes.html: lesson 1 has no route back to the index')
        if l['order'] == 10:
            check('href="../guides.html"' in text, 'lessons/better-environments.html: lesson 10 has no route on to the guides')
            check('desks-figure' in text, 'lessons/better-environments.html: the environment drawing is missing')
        for g_id in l['guide_ids']:
            check(f'guides/{g_id}-' in text, f'{l["page"]}: no link into guide {g_id}')
        for s_id in l['skill_ids']:
            check(f'href="../skills/{s_id}/"' in text, f'{l["page"]}: no link into skills/{s_id}/')
        # The lesson Markdown ships beside its page.
        check((PUBLIC / l['source']).is_file(), f'public/{l["source"]} missing')

    # The nineteen legacy idea routes: lightweight aliases whose canonicals
    # point at their lesson, carrying no duplicate article.
    idea_aliases = sorted((PUBLIC / 'ideas').glob('*.html')) if (PUBLIC / 'ideas').is_dir() else []
    check(len(idea_aliases) == 19, f'expected 19 legacy idea aliases in public/ideas, found {len(idea_aliases)}')
    expected_aliases = {Path(rel).name: l for l in manifest_lessons for rel in l['legacy_paths']}
    check({p.name for p in idea_aliases} == set(expected_aliases),
          'public/ideas: the alias set is not exactly the nineteen legacy routes')
    for alias in idea_aliases:
        text = alias.read_text()
        target = expected_aliases[alias.name]
        canonical = f'<link rel="canonical" href="' + SITE_URL + '/' + target['page'] + '"'
        check(canonical in text,
              f'ideas/{alias.name}: canonical does not point at {target["page"]}')
        # The share URL must agree with the canonical: an old route that
        # announces a lesson as its address must not share the old address.
        check(f'<meta property="og:url" content="' + SITE_URL + '/' + target['page'] + '"' in text,
              f'ideas/{alias.name}: og:url does not agree with its canonical {target["page"]}')
        # The route out of the alias carries the matching fragment instead of
        # dropping it, so a reader arriving at /old-url#apply lands on the
        # lesson's own #apply region through the alias page too.
        check(all(f'href="{target["page"]}#{frag}"' in text or
                  f'href="../{target["page"]}#{frag}"' in text for frag in LEGACY_FRAGMENTS),
              f'ideas/{alias.name}: its lesson links do not carry the legacy fragments')
        check('<h2 id="said' not in text and 'data-unwritten' not in text,
              f'ideas/{alias.name}: still carries the old four-section article')
        for frag in LEGACY_FRAGMENTS:
            check(f'id="{frag}"' in text, f'ideas/{alias.name}: legacy fragment #{frag} is not reachable')

    # Guide and investigation sections unchanged in shape.
    check(guides_html.count('class="tile guide"') == 13, f'guides.html: expected 13 guide tiles, found {guides_html.count("class=\"tile guide\"")}')
    check(guides_html.count('class="stage"') == 13, f'guides.html: expected 13 track stages, found {guides_html.count("class=\"stage\"")}')
    check(guides_html.count('class="seg"') == 4, f'guides.html: expected 4 source labels on the track, found {guides_html.count("class=\"seg\"")}')
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
        check(icon_canonical(SKILLS[s]) in icon_canonical(text), f'skills/{s}/index.html: the skill\'s drawing is missing')
        check('href="SKILL.md"' in text, f'skills/{s}/index.html: no link to the copied SKILL.md')
        check(f'/tree/HEAD/skills/{s}' in text, f'skills/{s}/index.html: no link to its GitHub directory')
        check('href="../../adoption.html"' in text, f'skills/{s}/index.html: no link to the adoption page')
        fm = (PUBLIC / 'skills' / s / 'SKILL.md').read_text().split('---')[1]
        own_title = re.search(r'^name:\s*(.+)$', fm, re.M).group(1).strip()
        h1 = re.search(r'<h1>(.*?)</h1>', text, re.S); h1 = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ''
        check(bool(h1) and 'Reference' not in h1 and h1.lower() != '', f'skills/{s}/index.html: h1 is {h1!r}')
        check(not re.search(r'<h1>[^<]*(?:checks that protect|worked implementation)', text), f'skills/{s}/index.html: h1 carries a reference title')
    check(skills_html.count('class="tile skill"') == 7, f'skills.html: expected 7 skill tiles, found {skills_html.count("class=\"tile skill\"")}')
    for s in skills:
        check(f'href="skills/{s}/"' in skills_html, f'skills.html: no tile opens skills/{s}/')
    check('href="adoption.html"' in skills_html, 'skills.html: no link to the adoption page')
    check('eval/cases.json' not in skills_html and 'eval/' not in skills_html,
          'skills.html: references its unrun evaluation suites as if they were results')

    # 6b-ii. No section page dead-ends: each closes with routes to other sets,
    # and every route resolves (section 2 already proved the targets exist).
    for name in ('lessons.html', 'guides.html', 'skills.html', 'investigations.html', 'evidence.html'):
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

    # 6c. Investigations: the index is three study sections, each carrying its
    # report's drawing, a link to the report page and a 3-4 item findings list;
    # every report page shows its own drawing.
    studies = re.findall(r'<section class="study"[^>]*>(.*?)</section>', reports_html, re.S)
    check(len(studies) == 3, f'investigations.html: expected 3 study sections, found {len(studies)}')
    for rel, study in zip(INVESTIGATIONS, studies):
        page_name = rel[:-3] + '.html'
        page = PUBLIC / page_name
        check(INVESTIGATIONS[rel] in study, f'investigations.html: {page_name} study is missing its drawing')
        check(f'href="{page_name}"' in study, f'investigations.html: no card opens {page_name}')
        findings = re.search(r'<ol class="findings"[^>]*>(.*?)</ol>', study, re.S)
        n_findings = findings.group(1).count('<li>') if findings else 0
        check(3 <= n_findings <= 4, f'investigations.html: {page_name} study has {n_findings} findings, expected 3-4')
        check(page.is_file() and INVESTIGATIONS[rel] in page.read_text(),
              f'{page_name}: the investigation\'s drawing is missing')

    # 6d. Every guide page shows its own drawing.
    for g in guides:
        m = re.match(r'(\d\d)-', g.name)
        check(m and GUIDES.get(m.group(1), '') and icon_canonical(GUIDES[m.group(1)]) in icon_canonical(g.read_text()),
              f'guides/{g.name}: the guide\'s drawing is missing')

    if failures:
        print(f'FAIL ({len(failures)}):')
        for f in failures:
            print(f'  - {f}')
        sys.exit(1)
    print(f'PASS: {len(pages)} HTML pages, {len(lesson_pages)} lessons, {len(guides)} guides, '
          f'{len(skills)} skills, {len(idea_aliases)} legacy aliases, {len(frames)} frames verified; '
          f'links, hashes, semantics, ten-lesson coverage, disclosure routes, no network loads '
          f'and required metadata fields OK.')


if __name__ == '__main__':
    main()
