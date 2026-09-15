#!/usr/bin/env python3
"""Local checks for the Agent Engineering Handbook.

Run after render.py. Enforces the approved 33-page inventory, ten lessons,
seven skill explanations, twelve unchanged frames, permanent legacy redirects,
complete menu, file/link confinement, source ownership, metadata, illustrations,
progressive disclosure, semantic accessibility and no network resource loads.
LS01–LS12 gate every default full run; --lessons is a compatible no-op.
--layout remains source-only and requires no generated output.
Source truth, grammar, actual next-action meaning and visual fit require evidence
beyond these structural checks. No network calls; standard library only.
"""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import parse_qs, unquote, urlsplit
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

from site_routes import redirects_at, resolve_local

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
    'missing-tools', 'useful-instructions', 'shared-contracts',
    'codebase-navigation', 'resume-work', 'better-environments',
]
APPROVED_CHAPTERS = {
    'recurring-mistakes': 'stop-repeat-work', 'ci-feedback': 'stop-repeat-work',
    'prove-it-works': 'stop-repeat-work', 'working-previews': 'give-agents-what-they-need',
    'missing-tools': 'give-agents-what-they-need', 'useful-instructions': 'give-agents-what-they-need',
    'resume-work': 'keep-it-understandable', 'shared-contracts': 'keep-it-understandable',
    'codebase-navigation': 'keep-it-understandable', 'better-environments': 'keep-it-understandable',
}

APPROVED_OWNERSHIP = {'recurring-mistakes': ('You turn repeated mistakes into reliable checks',
                        ['01'],
                        ['tip-08-fix-class-loops', 'tip-19-custom-lint-economics']),
 'ci-feedback': ('You diagnose failed checks without copying logs',
                 ['04'],
                 ['tip-01-ci-feedback-loop']),
 'prove-it-works': ('You test the result users actually need',
                    ['02', '09', '13'],
                    ['tip-02-two-browser-e2e']),
 'working-previews': ('You give agents a working preview', ['03'], ['tip-04-preview-environments']),
 'missing-tools': ('You make missing operations usable by agents',
                   ['06'],
                   ['tip-05-custom-file-upload-skill', 'tip-06-skill-authoring-reward']),
 'useful-instructions': ('You write instructions that fix observed confusion',
                         ['05'],
                         ['tip-09-domain-knowledge-as-infra',
                          'tip-11-own-your-instructions',
                          'tip-12-steering-pushback',
                          'tip-14-zero-context-docs',
                          'tip-15-minimal-context-calibration',
                          'tip-16-steer-not-map']),
 'shared-contracts': ('You keep shared contracts consistent across layers',
                      ['08', '11'],
                      ['tip-13-type-safe-composition']),
 'codebase-navigation': ('You navigate unfamiliar code without guessing',
                         ['10'],
                         ['tip-18-solo-onboarding']),
 'resume-work': ('You resume work without repeating completed steps', ['12'], []),
 'better-environments': ('You remove obstacles for the next contributor',
                         ['07'],
                         ['tip-03-automation-multiplies-agents',
                          'tip-07-team-buy-in',
                          'tip-10-newcomer-questions-signal',
                          'tip-17-career-leverage'])}


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
    check(manifest.get('legacy_paths') == ['README.html', 'guides.html', 'ideas.html', 'ideas'],
          'build/lessons.json: hub-level legacy_paths differ from the approved earlier addresses')
    records = manifest.get('lessons', [])
    check(len(records) == 10, f'build/lessons.json: expected 10 lessons, found {len(records)}')
    ids = [r.get('id') for r in records]
    check(ids == APPROVED_LESSON_IDS,
          f'build/lessons.json: lesson ids {sorted(ids)} are not exactly the ten approved ids')
    check(len(set(ids)) == len(ids), 'build/lessons.json: a lesson id repeats')
    check([r.get('order') for r in records] == list(range(1, 11)),
          'build/lessons.json: orders are not exactly 1..10 in file order')
    covered = []
    for r in records:
        check(r.get('chapter') == APPROVED_CHAPTERS.get(r.get('id')),
              f'build/lessons.json: {r.get("id")} is not in its approved chapter')
        expected = APPROVED_OWNERSHIP.get(r.get('id'))
        check(expected == (r.get('title'), r.get('guide_ids'), r.get('tip_ids')),
              f'{r.get("id")}: title, guides or video ownership differ from approved sitemap')
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
            redirects = redirects_at(REPO)
            dest = redirects.get('/' + rel, '')
            check(dest.split('#')[0] in (f'/lessons/{r["id"]}.html', f'/lessons/{r["id"]}.md'),
                  f'{rel}: legacy destination does not name its owning lesson')
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
                 'design-notes.md', 'design-skill-standard.md', 'design-review-capsule.md',
                 'lesson-standard.md', 'harness.md', 'harness-state.json', 'citation-map.md'}
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


class ReadingNode:
    """Small HTML tree for authored prose; independent of existing PageScan checks."""

    def __init__(self, tag='', attrs=(), parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children = []

    def visible(self):
        return (self.tag not in {'script', 'style', 'template', 'svg'}
                and 'hidden' not in self.attrs
                and self.attrs.get('aria-hidden', '').lower() != 'true')

    def nodes(self):
        if self.visible():
            yield self
            for child in self.children:
                if isinstance(child, ReadingNode):
                    yield from child.nodes()

    def text(self, *, prose=False):
        if not self.visible() or (prose and self.tag in {'code', 'pre'}):
            return ''
        # Count a prose block's own words once. Nested paragraphs/list items
        # are counted at their own boundaries, including a parent's lead-in.
        excluded = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'nav', 'aside', 'footer'}
        parts = [('' if prose and c.tag in excluded else c.text(prose=prose))
                 if isinstance(c, ReadingNode) else c for c in self.children]
        text = ''.join(parts)
        if self.tag in {'p', 'li', 'div', 'section', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            text = ' ' + text + ' '
        return text

    def content_nodes(self):
        """Yield owners of non-whitespace text and empty media in reading order."""
        if not self.visible():
            return
        if self.tag in VOID or self.tag in {'video', 'audio', 'iframe'}:
            yield self
        for child in self.children:
            if isinstance(child, ReadingNode):
                yield from child.content_nodes()
            elif child.strip():
                yield self

    def within(self, ancestor):
        node = self
        while node is not None:
            if node is ancestor:
                return True
            node = node.parent
        return False


class ReadingScan(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = ReadingNode()
        self.stack = [self.root]
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = ReadingNode(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def reading_text(node, *, prose=False):
    return ' '.join(node.text(prose=prose).split())


# A transparent vocabulary, not POS tagging. No suffix guessing: "settings"
# is not admitted merely because it ends in s/ing. Review checks grammar and
# may request a tested vocabulary extension for an unfamiliar valid verb.
HEADING_VERBS = set("""
am is are was were be been being do does did have has had can could will would
shall should may might must
accept accepts accepted add adds added allow allows allowed apply applies applied
ask asks asked avoid avoids avoided build builds built catch catches caught
change changes changed check checks checked choose chooses chose chosen cite cites
cited collect collects collected compare compares compared confirm confirms confirmed
connect connects connected contain contains contained cover covers covered decide
decides decided define defines defined depend depends depended describe describes
described determine determines determined diagnose diagnoses diagnosed distinguish
distinguishes distinguished end ends ended explain explains explained fail fails
failed find finds found fix fixes fixed follow follows followed give gives gave given
help helps helped include includes included keep keeps kept learn learns learned
leave leaves left limit limits limited link links linked list lists listed load
loads loaded make makes made measure measures measured name names named need needs
needed observe observes observed permit permits permitted preserve preserves preserved
prevent prevents prevented prove proves proved read reads record records recorded
reject rejects rejected remove removes removed repeat repeats repeated require
requires required resolve resolves resolved resume resumes resumed return returns
returned reveal reveals revealed run runs ran say says said select selects selected
separate separates separated share shares shared ship ships shipped show shows showed
sharpen sharpens sharpened expose exposes exposed supply supplies supplied guide guides guided
receive receives received
shown start starts started state states stated stop stops stopped store stores stored
support supports supported take takes took taken teach teaches taught test tests
tested trace traces traced trust trusts trusted turn turns turned use uses used
validate validates validated verify verifies verified win wins won work works worked
write writes wrote written pay pays paid
belong belongs belonged close closes closed derive derives derived feel feels felt
hit hits map maps mapped remain remains remained reuse reuses reused
""".split())


def heading_words(text):
    return re.findall(r"[^\W_]+(?:[-’'][^\W_]+)*", text, re.UNICODE)


def sentence_units(text, *, complete_only=False):
    """Deterministic prose counter, not a grammar claim. Preserve decimal/URL dots.

    Common abbreviations are protected; reviewers resolve other abbreviations,
    fragments and punctuation ambiguity. A trailing fragment consumes an opening
    or closing unit, but never pads a section's minimum complete-sentence count.
    """
    text = ' '.join(text.split())
    text = re.sub(r'\b(?:e\.g\.|i\.e\.|Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|vs\.)',
                  lambda m: m.group().replace('.', '․'), text, flags=re.I)
    ends = list(re.finditer(r"""[.!?]+[\"”’')\]]*(?=\s|$)""", text))
    count = sum(bool(re.search(r'\w', text[(ends[i-1].end() if i else 0):m.start()]))
                for i, m in enumerate(ends))
    rest = text[ends[-1].end():] if ends else text
    return count + (int(bool(re.search(r'\w', rest))) if not complete_only else 0)


def qualified_source_url(href):
    """Local URL-shape check only; no fetching or claim-support inference."""
    try:
        url = urlsplit(href)
        if url.scheme not in {'http', 'https'} or not url.hostname or re.search(r'\s', href):
            return False
        if unquote(url.fragment).strip():
            return True
        query = parse_qs(url.query)
        return any(re.fullmatch(r'(?:\d+|(?=\d)(?:\d+h)?(?:\d+m)?(?:\d+s)?)', value)
                   for key in ('t', 'start') for value in query.get(key, []))
    except ValueError:
        return False


def lesson_standard():
    """Check rendered lesson/skill articles; callable without any command-line flag.

    Authored prose excludes navigation, rails and hidden decoration. The default
    main check opts in only with --lessons until later phases rewrite the pages.
    """
    shared_headings = {}
    pages = sorted((PUBLIC / 'lessons').glob('*.html'))
    pages += sorted((PUBLIC / 'skills').glob('*/index.html'))
    for page in pages:
        rel = page.relative_to(PUBLIC).as_posix()
        doc = ReadingScan(page.read_text()).root
        articles = [n for n in doc.nodes() if n.tag == 'article']
        article = articles[0] if len(articles) == 1 else ReadingNode()
        chrome = [n for n in doc.nodes() if n.tag in {'nav', 'aside', 'footer'}]
        nodes = [n for n in article.nodes() if not any(n.within(c) for c in chrome)]
        headings = [n for n in nodes if n.tag == 'h2']
        paragraphs = [n for n in nodes if n.tag == 'p']
        opening = paragraphs[0] if paragraphs else ReadingNode()
        check(len(articles) == 1 and bool(headings) and bool(paragraphs)
              and nodes.index(opening) < nodes.index(headings[0])
              and bool(reading_text(opening)),
              f'{rel}: LS01: expected one article with an opening paragraph before its h2 sections')
        opening_text = reading_text(opening)
        opening_count = sentence_units(opening_text)
        check(2 <= opening_count <= 3,
              f'{rel}: LS02: opening has {opening_count} sentence units; expected 2–3')

        check(len(opening_text) <= 360,
              f'{rel}: LS03: opening has {len(opening_text)} characters; maximum 360')

        check('what you will know' not in reading_text(doc).casefold(),
              f'{rel}: LS04: page contains the banned phrase "what you will know"')

        kind = 'lesson' if rel.startswith('lessons/') else 'skill'
        authored = [n for n in doc.nodes()
                    if re.fullmatch(r'h[1-6]', n.tag)
                    and (n.within(article) or (n.tag == 'h1' and any(
                        n.within(m) for m in doc.nodes() if m.tag == 'main')))
                    and not any(n.within(a) for a in chrome)]
        for heading in authored:
            label = reading_text(heading)
            key = (kind, label.casefold())
            shared_headings.setdefault(key, (label, set()))[1].add(rel)
        for heading in headings:
            label = reading_text(heading)
            word_count = len(heading_words(label))
            check(word_count <= 8,
                  f'{rel}: LS06: h2 {label!r} has {word_count} words; maximum 8')

        for heading in headings:
            label = reading_text(heading)
            check(bool(set(w.casefold() for w in heading_words(label)) & HEADING_VERBS),
                  f'{rel}: LS07: h2 {label!r} has no declared plain verb; '
                  'use a claim with a verb or add a tested vocabulary entry')

        sections = []
        for i, heading in enumerate(headings):
            start = nodes.index(heading)
            end = nodes.index(headings[i + 1]) if i + 1 < len(headings) else len(nodes)
            section_nodes = nodes[start + 1:end]
            sections.append((heading, section_nodes))
            prose_blocks = [n for n in section_nodes if n.tag in {'p', 'li'}
                            and n.attrs.get('id') != 'next-action'
                            and not any(n.within(a) for a in nodes if a.tag in {'pre', 'code'})]
            count = sum(sentence_units(reading_text(n, prose=True), complete_only=True)
                        for n in prose_blocks)
            check(count >= 3,
                  f'{rel}: LS08: section {reading_text(heading)!r} has {count} complete '
                  'sentence units; minimum 3')

        source_sections = [(h, ns) for h, ns in sections if h.attrs.get('id') == 'sources']
        source_nodes = source_sections[0][1] if len(source_sections) == 1 else []
        citation_lists = [n for n in nodes if n.attrs.get('id') == 'citations']
        citation_list = citation_lists[0] if len(citation_lists) == 1 else ReadingNode()
        entries = [n for n in citation_list.nodes() if n.tag == 'li' and n.parent is citation_list]
        citation_ids = [n.attrs.get('id', '') for n in entries]
        check(len(source_sections) == 1 and source_sections[0][0] is headings[-1]
              and len(citation_lists) == 1 and citation_list in source_nodes
              and citation_list.tag in {'ol', 'ul'} and bool(entries)
              and all(re.fullmatch(r'cite-[\w-]+', cid) for cid in citation_ids)
              and len(citation_ids) == len(set(citation_ids)),
              f'{rel}: LS09: expected one final sources h2 with one nonempty '
              'local citation list and unique cite- entry ids')

        source_urls = set()
        for entry in entries:
            urls = [n.attrs.get('href', '') for n in entry.nodes() if n.tag == 'a']
            qualified = {u for u in urls if qualified_source_url(u)}
            source_urls.update(qualified)
            check(bool(qualified),
                  f'{rel}: LS10: citation #{entry.attrs.get("id", "")} lacks an HTTP(S) '
                  'source URL with an anchor or timestamp')
        for link in source_nodes:
            if link.tag != 'a' or any(link.within(n) for n in nodes
                                     if n.attrs.get('id') == 'next-action'):
                continue
            href = link.attrs.get('href', '')
            target = unquote(href[1:]) if href.startswith('#') else None
            check((target in citation_ids) if target is not None else (href in source_urls),
                  f'{rel}: LS10: source link {href!r} does not resolve within '
                  'this page’s qualified citation list')

        actions = [n for n in nodes if n.attrs.get('id') == 'next-action']
        action = actions[0] if len(actions) == 1 else ReadingNode()
        source_start = nodes.index(source_sections[0][0]) if len(source_sections) == 1 else len(nodes)
        inline = [n for n in nodes[:source_start] if n.tag == 'a'
                  and unquote(n.attrs.get('href', '')).startswith('#cite-')]
        check(bool(inline), f'{rel}: LS11: no inline citation before the sources section')
        all_inline = [n for n in nodes if n.tag == 'a'
                      and unquote(n.attrs.get('href', '')).startswith('#cite-')
                      and (n not in source_nodes or n.within(action))]
        for link in all_inline:
            href = link.attrs.get('href', '')
            check(unquote(href[1:]) in citation_ids,
                  f'{rel}: LS11: inline citation {href!r} is not an entry in this page’s citation list')

        final_children = [c for c in article.children
                          if (isinstance(c, ReadingNode) and c.visible())
                          or (isinstance(c, str) and c.strip())]
        after_list = nodes[nodes.index(citation_list) + 1:] if citation_list in nodes else []
        # Every node after the evidence belongs to the list itself or the sole
        # closing paragraph; no second unmarked action can hide beside it.
        tail_ok = all(n.within(citation_list) or n.within(action) for n in after_list)
        content = list(article.content_nodes())
        list_positions = [i for i, n in enumerate(content) if n.within(citation_list)]
        tail_ok = tail_ok and bool(list_positions) and all(
            n.within(action) for n in content[max(list_positions) + 1:])
        action_text = reading_text(action)
        check(len(actions) == 1 and action.tag == 'p' and action.parent is article
              and bool(final_children) and final_children[-1] is action
              and citation_list in nodes and nodes.index(action) > nodes.index(citation_list)
              and tail_ok and sentence_units(action_text) == 1
              and sentence_units(action_text, complete_only=True) == 1,
              f'{rel}: LS12: end the article after its citation list with exactly one '
              'standalone next-action paragraph containing one complete sentence')


    for (kind, _), (label, owners) in sorted(shared_headings.items()):
        check(len(owners) <= 2,
              f'LS05: {kind} heading {label!r} appears on {len(owners)} pages: '
              + ', '.join(sorted(owners)))



def hub_copy_checked():
    """Front copy uses plain words; lexical checks do not certify grammar."""
    forbidden = re.compile(r'\b(?:[a-f0-9]{12,}|[\w.-]+/[\w./-]+|SKILL\.md|Markdown|JSON|YAML|OpenAI-compatible|lesson_catalog)\b', re.I)
    for name in ('index.html', 'lessons.html', 'skills.html', 'investigations.html'):
        page = PUBLIC / name
        if not page.is_file():
            check(False, f'{name}: missing hub')
            continue
        scan = ReadingScan(page.read_text())
        main = next((n for n in scan.root.nodes() if n.tag == 'main'), None)
        if main is None:
            check(False, f'{name}: missing main')
            continue
        nodes = list(main.nodes())
        title = next((n for n in nodes if n.tag == 'h1'), None)
        words = heading_words(reading_text(title)) if title else []
        check(title and len(words) <= 8 and bool({w.casefold() for w in words} & HEADING_VERBS),
              f'{name}: h1 must state a conclusion with a plain verb, at most eight words')
        check(not any(n.tag == 'code' for n in nodes) and not forbidden.search(reading_text(main)),
              f'{name}: front copy must use plain words, not paths, hashes, code or tool internals')


def sitemap_checked():
    """Check exact page inventory, menu entries and permanent destinations."""
    entries = json.loads((REPO / 'build/sitemap.json').read_text())
    redirects = redirects_at(REPO)
    expected = {e['path'][1:] for e in entries if e['path'].endswith('.html') and 'destination' not in e}
    actual = {p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob('*.html')}
    check(len(expected) == 33 and actual == expected,
          f'approved HTML inventory differs: missing {sorted(expected-actual)}, extra {sorted(actual-expected)}')
    planned_redirects = {e['path']: e['destination'] for e in entries if 'destination' in e}
    check(set(redirects) == set(planned_redirects), 'permanent redirect address set differs from approved sitemap')
    for e in entries:
        route = e['path']
        if 'destination' in e:
            check(redirects.get(route) == e['destination'], f'{route}: redirect destination differs from approved sitemap')
        try:
            resolved, fragment = resolve_local(PUBLIC, PUBLIC / 'index.html', route, redirects)
            if fragment and resolved.suffix == '.html':
                scan = PageScan(); scan.feed(resolved.read_text())
                check(fragment in scan.ids, f'{route}: redirect destination fragment is missing')
        except ValueError as exc:
            check(False, f'{route}: {exc}')
    for page in PUBLIC.rglob('*.html'):
        text = page.read_text()
        header = re.search(r'<header class="site-head">.*?</header>', text, re.S)
        check(header, f'{page.name}: missing shared header')
        if not header: continue
        menu = re.search(r'<details class="menu">.*?</details>', header.group(), re.S)
        check(menu and header.group().count('<details') == 1, f'{page.name}: expected one menu')
        if not menu: continue
        links = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', menu.group(), re.S)
        gh = 'https://github.com/desland01/agent-engineering-handbook'
        check(header.group().count(gh) == 1 and links[-1][0] == gh,
              f'{page.name}: repository link must occur once and last in menu')
        menu_routes = {}
        for href, label in links[:-1]:
            base = PUBLIC if href.startswith('/') else page.parent
            path = (base / href.lstrip('/')).resolve()
            route = '/' + path.relative_to(PUBLIC.resolve()).as_posix() if path.is_relative_to(PUBLIC.resolve()) else 'ESCAPE'
            if route == '/.': route = '/'
            if href.endswith('/') and not route.endswith('/'): route += '/'
            menu_routes[route] = unescape(re.sub('<[^>]+>', '', label))
        check(menu_routes == {e['path']: e['label'] for e in entries},
              f'{page.relative_to(PUBLIC)}: menu addresses or labels differ from approved sitemap')
        groups = re.findall(r'<li class="menu-group"><span>(.*?)</span>', menu.group())
        check(groups == ['Start here', 'Lessons', 'Skills', 'Sources', 'Help', 'Source texts', 'Earlier links'],
              f'{page.name}: menu groups differ from approved order')
        primary = re.search(r'<nav class="primary".*?</nav>', header.group(), re.S)
        check(primary and re.findall(r'>([^<>]+)</a>', primary.group()) == ['Lessons','Skills','Sources'],
              f'{page.name}: primary navigation labels differ')


def main():
    # --lessons remains a compatible no-op; the full check always includes LS01–LS12.
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
    check(not guides, f'guide pages must be redirects, found {len(guides)} rendered guides')
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
    for page in ['index.html', 'lessons.html', 'skills.html',
                 'investigations.html',
                 'adoption.html', 'prompts.html',
                 'validation.html', 'evidence.html', 'github-inspection.html',
                 'matt-pocock-inspection.html', 'boris-cherny-inspection.html',
                 '404.html', 'assets/handbook.css', 'assets/handbook.js']:
        check((PUBLIC / page).is_file(), f'public/{page} missing')

    # 2. Resolve files and declared redirects without allowing traversal.
    attrs = re.compile(r'(?:href|src)="([^"]+)"')
    pages = list(PUBLIC.rglob('*.html'))
    redirects = redirects_at(REPO)
    sitemap_checked()
    hub_copy_checked()
    for page in pages:
        for target in attrs.findall(page.read_text()):
            target = unescape(target)
            if re.match(r'^(https?:|mailto:|data:|#)', target): continue
            try:
                resolved, fragment = resolve_local(PUBLIC, page, target, redirects)
                # Redirect destinations are authored stable targets; historical incoming
                # fragments are intentionally not copied onto merged lesson articles.
                if fragment and resolved.suffix == '.html' and target.split('#')[0].startswith('/'):
                    scan = PageScan(); scan.feed(resolved.read_text())
                    check(fragment in scan.ids, f'{page.relative_to(PUBLIC)}: missing destination fragment {target}')
            except ValueError as exc:
                check(False, f'{page.relative_to(PUBLIC)}: {exc}')

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
    check(n_pick == len(manifest_lessons), f'index.html: expected one problem row per lesson ({len(manifest_lessons)}), found {n_pick}')
    check(pick and 'class="ix"' not in pick.group(1),
          'index.html: problem rows introduce a second numbering system')
    check(pick and '<span class="n">Lesson 9</span>' in pick.group(1),
          'index.html: recovery must open lesson 9')
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
    check(n_lesson_chips == len(manifest_lessons), f'index.html: expected {len(manifest_lessons)} problem rows opening a lesson, found {n_lesson_chips}')
    chip_order = [int(n) for n in re.findall(r'class="chip" href="lessons/[\w-]+\.html"><span class="n">Lesson (\d+)</span>', index)]
    check(chip_order == sorted(chip_order), f'index.html: problem rows are not in lesson order: {chip_order}')
    check('class="chip" href="lessons/resume-work.html"' in index,
          'index.html: problem row 8 does not open lesson 9')

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

    for retired in ('ideas.html', 'guides.html', 'README.html', 'lessons/fresh-agent.html'):
        check(not (PUBLIC / retired).exists(), f'{retired}: retired page is still rendered')
    check('id="guides"' not in index, 'index.html: retired guide course is rendered')

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
            check(f'id="{frag}"' not in text, f'{l["page"]}: obsolete legacy fragment #{frag} remains')
        # The derived reading estimate must be visible without the desktop rail
        # (the lesson header), and it must say it is an estimate.
        check(re.search(r'class="read-min[^"]*"[^>]*>[^<]*About \d+ min[^<]*estimated', text)
              or re.search(r'>About \d+ min[^<]*estimated', text),
              f'{l["page"]}: no derived reading estimate in the page head')
        check('class="tip-glyphs"' not in text and 'In the video</h2>' not in text,
              f'{l["page"]}: retired video apparatus is rendered')
        for rel in l['legacy_paths']:
            if rel.startswith('ideas/') and rel.endswith('.html'):
                number = Path(rel).name[:2]
                check(f'<span id="video-note-{number}" class="legacy-target" aria-hidden="true"></span>' in text,
                      f'{l["page"]}: missing invisible video-note-{number} destination')
        # Sequence and source line.
        check('class="guide-seq"' in text and 'Lesson sequence' in text,
              f'{l["page"]}: no lesson sequence')
        check('lesson_catalog' not in text, f'{l["page"]}: internal build name leaked into the page')
        if l['order'] == 1:
            check('href="../lessons.html"' in text, 'lessons/recurring-mistakes.html: lesson 1 has no route back to the index')
        if l['order'] == 10:
            check('href="../skills.html"' in text, 'lessons/better-environments.html: lesson 10 has no route on to skills')
            check('desks-figure' in text, 'lessons/better-environments.html: the environment drawing is missing')
        for s_id in l['skill_ids']:
            check(f'href="../skills/{s_id}/"' in text, f'{l["page"]}: no link into skills/{s_id}/')
        # The lesson Markdown ships beside its page.
        check((PUBLIC / l['source']).is_file(), f'public/{l["source"]} missing')

    idea_aliases = list((PUBLIC / 'ideas').glob('*.html'))
    check(not idea_aliases, 'ideas: retired articles must be redirects, not physical pages')

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
    skill_front = re.search(r'<main.*?</main>', skills_html, re.S).group(0)
    check('eval/cases.json' not in skill_front and 'eval/' not in skill_front,
          'skills.html: references its unrun evaluation suites as if they were results')

    # 6b-ii. No section page dead-ends: each closes with routes to other sets,
    # and every route resolves (section 2 already proved the targets exist).
    for name in ('lessons.html', 'skills.html', 'investigations.html', 'evidence.html'):
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

    lesson_standard()

    if failures:
        print(f'FAIL ({len(failures)}):')
        for f in failures:
            print(f'  - {f}')
        sys.exit(1)
    print(f'PASS: {len(pages)} HTML pages, {len(lesson_pages)} lessons, {len(guides)} guides, '
          f'{len(skills)} skills, {len(redirects)} permanent redirects, {len(frames)} frames verified; '
          f'links, hashes, semantics, ten-lesson coverage, disclosure routes, no network loads '
          f'and required metadata fields OK.')


if __name__ == '__main__':
    main()
