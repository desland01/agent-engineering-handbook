#!/usr/bin/env python3
"""Render the public handbook site into public/.

Reads only the editable Markdown, assets and JSON in this repository (never the
generated public/ directory) and writes public/ from scratch, so rerunning is
idempotent and cannot recursively consume its own output.

Inputs:
  README.md and the other Markdown pages     -> reader pages (one shared template)
  README.md tables and lists + build/home.json -> the landing-page map (index.html)
  evidence/frame-manifest.json               -> the frame gallery (evidence.html)
  build/icons.py                             -> the 39 authored drawings, inlined
  build/assets/handbook.css, handbook.js     -> public/assets/
  screenshots/, skills/, examples/, evidence/*.json -> copied verbatim

DESIGN.md and INTERACTIONS.md are contributor guidance and are never rendered
or copied. Requires Markdown==3.10.3 (build/requirements.txt). No network calls.

Usage:
    python3 build/render.py            # from anywhere; paths are script-relative
"""
from pathlib import Path
from html import escape, unescape
import json
import re
import shutil
import sys

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icons import IDEAS, SKILLS, GUIDES, INVESTIGATIONS
from hero import hero  # the animated hero loop
from desks import desks  # the three empty workstations
import lesson_catalog  # the reviewed ten-lesson catalog seam (load_lessons, read_minutes)

REPO = Path(__file__).resolve().parent.parent
# The claim line of each investigation, copied verbatim from COPY.md.
CLAIMS = {
    'github-inspection.md': "Ten of the thirteen guides draw on the video and this investigation of T3 Code and Melee. The report connects advice to inspected code.",
    'matt-pocock-inspection.md': 'A glossary and one HTTP transport give this codebase a shared language. Its source informed two guides on domain language and durable artifacts.',
    'boris-cherny-inspection.md': "Guide 13 adapts five validation methods: fixtures, built-artifact smoke tests, fuzzing, real-world schemas and conformance checks. Tests were inspected, not run locally.",
}
OUT = REPO / 'public'
ASSETS = REPO / 'build/assets'
HOME = REPO / 'build/home.json'

GITHUB = 'https://github.com/desland01/agent-engineering-handbook'
# The production origin, once the site has one: scheme and host, no trailing
# slash, e.g. 'https://agent-engineering-handbook.example'. Set it here and
# every page gains a canonical URL and the Open Graph and Twitter tags a shared
# link needs; leave it empty and none of them are emitted, because a canonical
# pointing at the wrong origin is worse than no canonical at all. build/check.py
# enforces that this is all-or-nothing across the 54 pages.
SITE_URL = 'https://agent-engineering-handbook.dev'
EDITION_DATE = 'September 9, 2026'

# The empty-workstations drawing is the video's own career-level claim: that
# building an environment where code lands well is the skill worth having. The
# drawing follows the subject, so it appears on lesson 10 (better-environments,
# which holds that tip) and nowhere else.
DESKS_ON_LESSON = 'better-environments'
SITE_NAME = 'Agent Engineering Handbook'

# Directories and files that are renderer *inputs*. public/, build/ and any
# virtualenv are never read as content sources.
COPY_DIRS = ['screenshots', 'skills', 'examples/recurring-rule']
COPY_FILES = [
    'evidence/frame-manifest.json',
    'evidence/video-tips.json',
    'evidence/melee-verifier-comparison.json',
]
# Markdown rendered to HTML (the .md source is copied alongside each page).
# DESIGN.md and INTERACTIONS.md are deliberately absent: source-only guidance.
RENDER_MD = [
    'README.md', 'adoption.md', 'prompts.md', 'validation.md',
    'CONTRIBUTING.md', 'ATTRIBUTION.md',
    'github-inspection.md', 'matt-pocock-inspection.md', 'boris-cherny-inspection.md',
    'evidence/video-research.md', 'examples/recurring-rule/README.md',
] + sorted(f'guides/{p.name}' for p in (REPO / 'guides').glob('*.md'))

# Header: three section links always visible from 760px, and a native menu
# (<details>) that lists every page. On narrow screens the menu is the whole
# navigation. Items marked primary are hidden inside the menu at wide widths.
PRIMARY_NAV = [
    ('lessons.html', 'Lessons'),
    ('skills.html', 'Skills'),
    ('guides.html', 'Reference'),
]
MENU_GROUPS = [
    [('index.html', 'Home', True)] + [(t, l, True) for t, l in PRIMARY_NAV],
    [('README.html', 'Handbook index', False), ('prompts.html', 'Task prompts', False),
     ('adoption.html', 'Adopting a skill', False), ('validation.html', 'Validation', False)],
    [('github-inspection.html', 'Theo: T3 Code and Melee', False),
     ('matt-pocock-inspection.html', 'Matt Pocock: Course Video Manager', False),
     ('boris-cherny-inspection.html', 'Boris Cherny: public work', False)],
    [('investigations.html', 'Investigations', False), ('evidence.html', 'Frames', False),
     ('evidence/video-research.html', 'Video notes', False)],
    [('ATTRIBUTION.html', 'Attribution', False), ('CONTRIBUTING.html', 'Contributing', False),
     (GITHUB, 'GitHub repository', False)],
]

# A reader page whose own h1 does not make a useful browser title. README's h1
# is the site name, which would render as "X · X" in a tab and a search result.
TITLES = {'README.md': 'Handbook index'}

# Where a non-guide reader page sits in the handbook: (context line, target page).
CONTEXT = {
    'README.md': ('The handbook index', 'lessons.html'),
    'github-inspection.md': ('One of three repository investigations', 'investigations.html'),
    'matt-pocock-inspection.md': ('One of three repository investigations', 'investigations.html'),
    'boris-cherny-inspection.md': ('One of three repository investigations', 'investigations.html'),
    'evidence/video-research.md': ('Detailed extraction behind the lessons', 'lessons.html'),
    'examples/recurring-rule/README.md': ('Runnable companion to guide 01', 'guides/01-recurring-failures.html'),
    'adoption.md': ('Adopting a guide or portable skill', 'skills.html'),
    'prompts.md': ('Task prompts for the guides', 'guides.html'),
    'validation.md': ('What was checked, and what was not', 'index.html#checked'),
    'ATTRIBUTION.md': ('Sources and attribution', 'index.html#attribution'),
    'CONTRIBUTING.md': ('How the handbook is built and updated', 'index.html#attribution'),
}

MD_EXTENSIONS = ['markdown.extensions.tables', 'markdown.extensions.fenced_code',
                 'markdown.extensions.sane_lists', 'markdown.extensions.toc']
MD_CONFIG = {'markdown.extensions.toc': {'toc_depth': '2-3'}}


# ------------------------------------------------------------------ helpers
def md_html(text):
    return markdown.markdown(text, extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)


def md_convert(text):
    """Render a page body and return (html, section tokens for the contents list)."""
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    html = md.convert(text)
    return html, md.toc_tokens


def inline(text):
    """Render one paragraph of Markdown without the wrapping <p>."""
    html = md_html(text).strip()
    if html.startswith('<p>') and html.endswith('</p>') and html.count('<p>') == 1:
        html = html[3:-4]
    return html


def strip_tags(html):
    return re.sub(r'<[^>]+>', '', html)


def rewrite_refs(body, prefix=''):
    # Generated HTML pages point at sibling generated HTML; asset and JSON links
    # are untouched. Editable .md files are copied next to each page, except
    # SKILL.md links, which stay on the copied skill source.
    return re.sub(
        r'href="([^"?#:]+)\.md([?#][^"]*)?"',
        lambda m: 'href="' + prefix + m.group(1) + '.html' + (m.group(2) or '') + '"'
        if not m.group(1).endswith('SKILL') else m.group(0),
        body)


def rewrite_tables(body):
    return (body
            .replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable table"><table>')
            .replace('</table>', '</table></div>'))


def depth_prefix(out_path):
    # Pages live in subdirectories (guides/, skills/..., examples/...); the
    # nav targets are repository-root relative, so prefix by depth.
    depth = len(out_path.relative_to(OUT).parent.parts)
    return '../' * depth


def site_head(prefix, current=''):
    """Brand, four section links, the all-pages menu and the repository link."""
    def link(target, label, extra=''):
        href = target if target.startswith('http') else prefix + target
        page = target.split('#')[0]
        aria = ' aria-current="page"' if page == current and '#' not in target else ''
        return f'<a href="{escape(href)}"{aria}{extra}>{escape(label)}</a>'

    primary = ''.join(link(t, l) for t, l in PRIMARY_NAV)
    groups = []
    for group in MENU_GROUPS:
        groups.append(''.join(
            f'<li{" class=\"in-primary\"" if p else ""}>{link(t, l)}</li>' for t, l, p in group))
    menu = '<li class="sep" role="presentation"></li>'.join(groups)
    return ('<header class="site-head"><div class="wrap">'
            f'<a class="brand" href="{prefix}index.html"><span class="mark" aria-hidden="true"></span>{SITE_NAME}</a>'
            f'<nav class="primary" aria-label="Handbook sections">{primary}</nav>'
            '<details class="menu"><summary><span class="l-wide">More</span><span class="l-narrow">Menu</span></summary>'
            f'<nav aria-label="All pages"><ul>{menu}</ul></nav></details>'
            f'<a class="repo" href="{GITHUB}">GitHub</a>'
            '</div></header>')


def site_foot(prefix, basis_short):
    links = [(f'{prefix}index.html', 'Home'), (f'{prefix}lessons.html', 'Lessons'), (f'{prefix}guides.html', 'Guides'), (f'{prefix}README.html', 'Handbook index'),
             (f'{prefix}ATTRIBUTION.html', 'Attribution'), (f'{prefix}CONTRIBUTING.html', 'Contributing'),
             (GITHUB, 'GitHub repository')]
    return ('<footer class="site-foot"><div class="wrap">'
            f'<p>{basis_short} Frames are short excerpts from the video and remain © Theo / their original owners.</p>'
            '<ul>' + ''.join(f'<li><a href="{escape(u)}">{escape(t)}</a></li>' for u, t in links) + '</ul>'
            '</div></footer>')


def summarise(text, limit=158):
    """A page description from its own prose: whole sentences up to the limit.

    Search results and link previews show roughly 155 characters, and a
    description cut mid-word reads as broken. So this adds whole sentences
    while they fit. When even the first sentence is longer than that — several
    skill descriptions and page openings are — it falls back to the last clause
    boundary, which still ends somewhere a reader would pause, and only then to
    a word boundary."""
    flat = re.sub(r'\s+', ' ', unescape(strip_tags(text))).strip()
    if not flat:
        return ''
    kept = []
    length = 0
    for s in re.findall(r'[^.!?]+(?:[.!?]+|$)', flat):
        s = s.strip()
        if not s:
            continue
        if length + len(s) + (1 if kept else 0) > limit:
            break
        kept.append(s)
        length += len(s) + (1 if len(kept) > 1 else 0)
    if kept:
        return ' '.join(kept)
    head = flat[:limit]
    clause = max(head.rfind(c) for c in ',;:—–-')
    if clause > limit * 0.55:
        return head[:clause].rstrip()
    return head.rsplit(' ', 1)[0].rstrip(' ,;:—–-')


def social(path, full_title, description):
    """Canonical URL and the tags a shared link shows, once SITE_URL is set.

    A link to this site currently previews as a bare URL, and a page reachable
    at more than one address has nothing saying which one is the real page.
    Both need an absolute origin, which the project does not have yet, so this
    emits nothing until SITE_URL is filled in — half of it would be worse than
    none."""
    # No SITE_URL yet, or a page with no one address of its own (404.html is
    # served at every path), means no canonical and no share tags.
    if not SITE_URL or not path:
        return ''
    # index.html is the site root; every other page is its path under public/.
    url = SITE_URL + ('/' if path == 'index.html' else '/' + path)
    tags = [('property', 'og:url', url), ('property', 'og:type', 'website'),
            ('property', 'og:site_name', SITE_NAME), ('property', 'og:title', full_title),
            ('name', 'twitter:card', 'summary')]
    if description:
        tags.insert(4, ('property', 'og:description', description))
        tags.append(('name', 'twitter:description', description))
    return (f'<link rel="canonical" href="{escape(url)}">'
            + ''.join(f'<meta {k}="{n}" content="{escape(v)}">' for k, n, v in tags))


def document(title, prefix, body, description='', path=''):
    desc = (f'<meta name="description" content="{escape(description)}">' if description else '')
    full_title = f'{title} · {SITE_NAME}'
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="color-scheme" content="dark"><script>document.documentElement.classList.add("js")</script>{desc}'
            f'{social(path, full_title, description)}'
            f'<link rel="icon" href="data:,"><title>{escape(full_title)}</title>'
            f'<link rel="stylesheet" href="{prefix}assets/handbook.css">'
            f'<script src="{prefix}assets/handbook.js" defer></script></head>'
            f'<body><a class="skip" href="#main">Skip to content</a>{body}</body></html>\n')


# ------------------------------------------------------- README as the index
def section(text, heading):
    """Lines of the README section under the given '## heading'."""
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == f'## {heading}')
    except StopIteration:
        raise SystemExit(f'README.md: section "## {heading}" not found')
    body = []
    for l in lines[start + 1:]:
        if l.startswith('## '):
            break
        body.append(l)
    return body


def table_rows(lines):
    rows = [l for l in lines if l.startswith('|')]
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    # Drop the header and the |---| separator.
    return [r for r in cells[2:] if r and not all(set(c) <= set('-: ') for c in r)]


def list_items(lines, marker):
    """Join wrapped list items ('- ' or 'N. ') into single strings."""
    items = []
    for l in lines:
        if re.match(marker, l):
            items.append(re.sub(marker, '', l, count=1).strip())
        elif items and l.startswith('  ') and l.strip():
            items[-1] += ' ' + l.strip()
    return items


def paragraphs(lines):
    paras, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l.strip())
        elif cur:
            paras.append(' '.join(cur))
            cur = []
    if cur:
        paras.append(' '.join(cur))
    return paras


LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
GUIDE_N = re.compile(r'guides/(\d\d)-')


def read_index(readme):
    """The handbook's own index: problems, guides, reports, skills, ideas, checks, attribution."""
    text = readme.read_text()
    idx = {}

    # Each problem row: the question and the links that answer it.
    idx['problems'] = [(row[0], LINK.findall(row[1]))
                       for row in table_rows(section(text, 'Start with the problem you have'))]

    guides = []
    for item in list_items(section(text, 'All 13 implementation guides'), r'^\d+\.\s+'):
        m = LINK.match(item)
        label, path = m.group(1), m.group(2)
        number, title = label.split(' — ', 1)
        guides.append({'n': number.strip(), 'title': title.strip(), 'path': path})
    idx['guides'] = guides

    reports = []
    for item in list_items(section(text, 'What the repository investigations add'), r'^-\s+'):
        m = LINK.match(item)
        blurb = item[m.end():].lstrip(' —-').strip()
        reports.append({'title': m.group(1), 'path': m.group(2), 'blurb': blurb[0].upper() + blurb[1:]})
    idx['reports'] = reports

    skills = []
    # The heading carries no count: the row set and the filesystem decide how
    # many skills exist, so renaming or growing the set needs no selector edit.
    for row in table_rows(section(text, 'Portable skills')):
        m = LINK.match(row[0])
        use = row[1] if row[1].endswith(('.', '!', '?')) else row[1] + '.'
        skills.append({'title': m.group(1), 'path': m.group(2), 'use': use})
    idx['skills'] = skills

    ideas = []
    for row in table_rows(section(text, 'The 19 useful video ideas, in order')):
        t = LINK.match(row[0])
        g = LINK.match(row[2])
        ideas.append({'ts': t.group(1), 'url': t.group(2), 'idea': row[1],
                      'guide_label': g.group(1), 'guide_path': g.group(2)})
    idx['ideas'] = ideas

    idx['checked'] = [inline(p) for p in paragraphs(section(text, 'What was checked'))]

    head = [l for l in text.splitlines()[1:]]
    head = head[:next(i for i, l in enumerate(head) if l.startswith('## '))]
    idx['attribution'] = inline(paragraphs(head)[1])
    return idx


# ------------------------------------------------------------ landing page
def frame_alt(f):
    return f'Video frame at {f["timestamp"]}: {f["title"]}.'


LESSON_SRC = re.compile(r'^lessons/([\w-]+)\.md$')


def guide_chip(label, path, prefix='', lesson_by_id=None, explicit_kind=False):
    """A destination link, with an explicit kind where lessons and guides mix."""
    m = GUIDE_N.search(path)
    if m:
        number = f'Guide {int(m.group(1))}' if explicit_kind else m.group(1)
        n = f'<span class="n">{number}</span> '
    elif lesson_by_id and LESSON_SRC.match(path):
        lesson = lesson_by_id[LESSON_SRC.match(path).group(1)]
        number = f'Lesson {lesson["order"]}' if explicit_kind else f'{lesson["order"]:02d}'
        n = f'<span class="n">{number}</span> '
    else:
        n = ''
    return f'<a class="chip" href="{escape(prefix + path)}">{n}{escape(label[0].upper() + label[1:])}</a>'


# Note 8 (DESIGN-NOTES): the evidence types collapsed by evidential force into
# three tiers. Exact types map directly; `sponsor-*` types land in `thinks` by
# prefix so a renamed sponsor segment is still bucketed rather than misfiled.
EVIDENCE_TIER = {
    'theo-practice': 'does',
    'theo-anecdote': 'does',
    'theo-directive': 'says',
    'quoted-post-via-theo': 'says',
    'theo-opinion': 'thinks',
}
EVIDENCE_TIER_PREFIX = [('sponsor-', 'thinks')]


EVIDENCE_LABEL = {
    'sponsor-ad-framing (sponsor performance claims unverified)': 'Sponsor segment',
    'theo-anecdote': 'Theo, anecdote',
    'theo-opinion': 'Theo, opinion',
    'theo-practice': 'Theo, practice',
    'theo-directive': 'Theo, directive',
    'quoted-post-via-theo': "Boris's post, read by Theo",
}


def mmss(seconds):
    return f'{seconds // 60:02d}:{seconds % 60:02d}'


def enrich(idx):
    """Join README's index rows to the structured extraction and the skills.

    Adds to each idea: its position n, page path, tip record, evidence label,
    skill and guide; to each skill: name, directory and how many ideas feed it.
    """
    tips = json.loads((REPO / 'evidence/video-tips.json').read_text())
    tip_by_start = {t['start_seconds']: t for t in tips}
    for sk in idx['skills']:
        sk['name'] = sk['path'].split('/')[1]
        sk['dir'] = sk['path'].rsplit('/', 1)[0]
        sk['href'] = f'skills/{sk["name"]}/'
        sk['page'] = f'skills/{sk["name"]}/index.html'
        sk['fed_by'] = 0
        sk['fed'] = []
        sk['guides'] = []
    layer_path = REPO / 'evidence/idea-pages.json'
    idx['idea_pages'] = json.loads(layer_path.read_text())['pages'] if layer_path.is_file() else {}
    skill_by_name = {sk['name']: sk for sk in idx['skills']}
    guide_by_n = {g['n']: g for g in idx['guides']}
    for n, i in enumerate(idx['ideas'], 1):
        seconds = int(re.search(r't=(\d+)s', i['url']).group(1))
        tip = tip_by_start[seconds]
        i['n'] = n
        i['tip'] = tip
        i['slug'] = f'{n:02d}-' + tip['id'].split('-', 2)[2]
        i['page'] = f'ideas/{i["slug"]}.html'
        i['evidence'] = EVIDENCE_LABEL[tip['evidence_type']]
        i['tier'] = EVIDENCE_TIER.get(tip['evidence_type']) or next(
            (t for pre, t in EVIDENCE_TIER_PREFIX if tip['evidence_type'].startswith(pre)), None)
        if i['tier'] is None:
            raise SystemExit(f'enrich(): unknown evidence_type {tip["evidence_type"]!r} '
                             f'(idea {n}, tip {tip["id"]}); no tier mapping')
        i['skill'] = skill_by_name[tip['suggested_skill']]
        i['skill']['fed_by'] += 1
        i['skill']['fed'].append(i)
        i['guide'] = guide_by_n[GUIDE_N.search(i['guide_path']).group(1)]
        if i['guide'] not in i['skill']['guides']:
            i['skill']['guides'].append(i['guide'])
    # Repository-derived skills have guide sources even when no original video
    # observation named that later public package directly.
    for name, numbers in json.loads(HOME.read_text()).get('skill_guides', {}).items():
        sk = skill_by_name[name]
        for number in numbers:
            guide = guide_by_n[number]
            if guide not in sk['guides']:
                sk['guides'].append(guide)
    return idx


def marker(label):
    """A section marker: a mono label in a bordered pill with a rule running from it."""
    return f'<span class="marker"><span class="pill">{escape(label)}</span></span>'


def more(href, label):
    """The mono link that routes from a teaser to the full section."""
    return f'<a class="more" href="{escape(href)}">{escape(label)} <span aria-hidden="true">&#8594;</span></a>'


def hub_next(hub, prefix=''):
    """The closing route of a section page.

    A reader who reaches the bottom of a set has finished something, and until
    now every section page ended there with nowhere to go but the header. Each
    row names the next set and says plainly why a person standing here would
    want it, so the route is a reason rather than a list of links."""
    rows = ''.join(
        f'<li><a href="{escape(prefix + href)}"><span class="t">{escape(label)}</span>'
        f'<span class="k">{escape(why)}</span></a></li>'
        for href, label, why in hub['next'])
    return ('<section class="hub-next" aria-labelledby="hub-next-h"><div class="wrap">'
            f'<h2 id="hub-next-h">Choose your next step</h2>'
            f'<ul role="list">{rows}</ul></div></section>')


# ------------------------------------------------------------- fragments
def idea_tile(i, prefix=''):
    """One idea as an icon tile. The title opens the idea's page."""
    tip = i['tip']
    return (f'<li><article class="tile idea">'
            f'<span class="ix" aria-hidden="true">[{i["n"]:02d}]</span>'
            f'<span class="art" aria-hidden="true">{IDEAS[f"{i["n"]:02d}"]}</span>'
            f'<h3><a href="{escape(prefix + i["page"])}">{escape(i["idea"])}</a></h3>'
            f'<p class="who">{escape(tip["speaker"])}</p>'
            f'<p class="when">{escape(tip["when_useful"])}</p>'
            f'<p class="meta"><span class="ts">{escape(i["ts"])}</span><span class="badge">{escape(i["evidence"])}</span></p>'
            f'</article></li>')


# The mono caption that sits inside each skill's drawing: the loop it closes,
# as the artwork's own label rather than a line placed under it.
SKILL_CAPTIONS = {
    'agent-feedback-engineering': 'MISTAKE \u2192 CHECK',
    'agent-ready-workspaces': 'SETUP \u2192 PREVIEW \u2192 CHECK',
    'agent-context-calibration': 'CONTEXT \u2192 RIGHT PLACE',
    'agent-tool-adapters': 'GAP \u2192 TOOL \u2192 CHECK',
    # The three source-derived packages reuse the existing thematic drawing
    # whose loop matches their method; the captions name that loop truthfully.
    'agent-output-verification': 'OUTPUT \u2192 CHECK',
    'agent-artifact-recovery': 'ARTIFACT \u2192 REUSE / RESUME',
    'agent-contract-consistency': 'CONTRACT \u2192 CALLERS',
}


def fed_line(sk):
    """The honest count line under a skill tile: how many video observations
    route to it, or the plain fact that none does."""
    if not sk['fed_by']:
        return 'From the original repository research'
    return (f'<span class="n">{sk["fed_by"]}</span> '
            f'{"idea feeds" if sk["fed_by"] == 1 else "ideas feed"} it')


def skill_tile(sk, prefix=''):
    """One skill as a tall hairline cell: its drawing at a size that carries,
    the caption inside the drawing, then the title, the use, the honest count
    and the routes. These tiles are the skills figure on skills.html."""
    cap = SKILL_CAPTIONS.get(sk['name'], '')
    return (f'<li class="tile skill"><span class="art" aria-hidden="true">{SKILLS[sk["name"]]}'
            f'<span class="cap">{cap}</span></span>'
            f'<a class="t" href="{escape(prefix + sk["href"])}">{escape(sk["title"])}</a>'
            f'<p class="when">{escape(sk["use"])}</p>'
            f'<p class="fed">{fed_line(sk)}</p>'
            f'<span class="routes"><span class="more">Open the skill <span aria-hidden="true">&#8594;</span></span>'
            f'<span class="dir"><a href="{GITHUB}/tree/HEAD/{escape(sk["dir"])}">{escape(sk["dir"])}/</a></span></span></li>')


def guide_tile(g, home, prefix=''):
    return (f'<li class="tile guide"><span class="glyph-box" aria-hidden="true">{GUIDES[g["n"]]}</span>'
            f'<div><a class="t" href="{escape(prefix + g["path"])}"><span class="n" aria-hidden="true">{g["n"]}</span>'
            f'<span class="sr-only">Guide {g["n"]}: </span>{escape(g["title"])}</a>'
            f'<p class="when">{escape(home["use_when"][g["n"]])}</p></div></li>')


def report_tile(r, prefix=''):
    return (f'<li class="tile report"><span class="art" aria-hidden="true">{INVESTIGATIONS[r["path"]]}</span>'
            f'<a class="t" href="{escape(prefix + r["path"])}">{escape(r["title"])}</a>'
            f'<p class="when">{escape(r["blurb"])}</p><span class="dir">{escape(r["path"])}</span></li>')


def report_facts(idx, home):
    """What the page can prove about each report: how many guides the home
    shelves trace to it and how many words it runs to. Shared by the home
    page's file cards and the investigations page's studies so the two never
    disagree. Keyed by the report's Markdown path."""
    guides_from = {}
    for s in home['shelves']:
        guides_from.setdefault(s['investigation'], []).extend(s['guides'])
    facts = {}
    for n, r in enumerate(idx['reports'], 1):
        rel = r['path']
        words = len((REPO / rel).read_text().split())
        nguides = len(guides_from.get(rel, []))
        facts[rel] = {
            'n': n, 'guides': nguides, 'words': words,
            'meta': (f'REPORT {n:02d} · {nguides} GUIDE{"S" if nguides != 1 else ""} CAME FROM THIS · '
                     f'{words:,} WORD{"S" if words != 1 else ""}'),
        }
    return facts


def report_card(r, facts, primary=False, prefix=''):
    """One investigation on the home page as a wired file card: the authored
    diagram at a size that reads, the title, one line from the README, and the
    mono metadata the renderer computed. The report most of the guides came
    from takes the primary card (the whole top row on wide screens, twice a
    companion's width), so 10 / 2 / 1 is visible as space rather than implied
    by three equal boxes. The modifier is report-specific, `file-primary`:
    the header's section navigation owns the bare `primary` class, which is
    hidden on narrow screens and set as mono labels, and sharing it hid the
    leading report on phones and set its title as navigation on desktop."""
    kicker = r['blurb'].split(' — ')[0].split(',')[0].rstrip('.').strip()
    return (f'<li class="file{" file-primary" if primary else ""}"><a href="{escape(prefix + r["path"][:-3] + ".html")}">'
            f'<span class="art" aria-hidden="true">{INVESTIGATIONS[r["path"]]}</span>'
            f'<span class="t">{escape(r["title"])}</span>'
            f'<span class="k">{escape(kicker[0].lower() + kicker[1:])}</span>'
            f'<span class="meta">{escape(facts["meta"])}</span></a></li>')


def shelf_row(s_, report, prefix=''):
    """One source shelf on the home page as a directory row inside the
    contracted lane: the guide range, the shelf's title with its count and
    investigation, and one accent stage mark per guide, so 8 / 2 / 2 / 1 is
    read as length rather than as four equal rows."""
    ns = s_['guides']
    span = f'Guide {ns[0]}' if len(ns) == 1 else f'Guides {ns[0]}–{ns[-1]}'
    marks = ''.join('<i></i>' for _ in ns)
    return (f'<li><a href="{escape(prefix)}guides.html#{escape(s_["id"])}">'
            f'<span class="range">{span}</span>'
            f'<span class="body"><span class="t">{escape(s_["title"])}</span>'
            f'<span class="k">{len(ns)} {"guide" if len(ns) == 1 else "guides"} · {escape(report["title"])}</span></span>'
            f'<span class="marks" aria-hidden="true">{marks}</span></a></li>')


def band_head(label, heading_id, heading, description, form=''):
    # No eyebrow above the heading (owner rule, 2026-09-10): the label that used
    # to sit in a mono pill here is dropped; the heading carries the section.
    # `form` varies the head's reading axis: 'split' puts the description
    # across from the heading on the same line; 'centered' centres both.
    cls = ' ' + form if form else ''
    return (f'<div class="band-head{cls}">'
            f'<h2 id="{heading_id}">{escape(heading)}</h2><p>{inline(description)}</p></div>')


# ------------------------------------------------------------ landing page
def landing(idx, home, lessons, frames):
    """The home page: the promise, the entry by problem, one taste of each
    section, and a route out to the page that holds the full set."""
    lesson_by_id = {l['id']: l for l in lessons}
    shelf_guides = [n for s in home['shelves'] for n in s['guides']]
    if sorted(shelf_guides) != sorted(g['n'] for g in idx['guides']):
        raise SystemExit(f'build/home.json shelves list {shelf_guides}; README lists guides differently')
    if len(lessons) != 10:
        raise SystemExit(f'landing(): expected the ten approved lessons, found {len(lessons)}')

    # The one quiet count in the opening: derived from the validated manifest,
    # never free text. Guide and skill counts live in their own bands' headings.
    n_lessons = len(lessons)

    # These are independent problems, not a second lesson sequence.
    pick = ''.join(
        f'<li><span class="q">{escape(q)}</span>'
        f'<span class="a">{"".join(guide_chip(label, path, lesson_by_id=lesson_by_id, explicit_kind=True) for label, path in links)}</span></li>'
        for q, links in idx['problems'])

    # Chapter directory: one row per manifest chapter, its mark count derived
    # from the validated lesson set, never from copy.
    def chapter_rows():
        rows = ''
        for ch in home['chapters']:
            here = [l for l in lessons if l['chapter'] == ch['id']]
            if not here:
                raise SystemExit(f'landing(): chapter {ch["id"]!r} holds no lessons')
            marks = ''.join('<i></i>' for _ in here)
            rows += (f'<li><a href="lessons.html#{escape(ch["id"])}">'
                     f'<span class="range">{escape(ch["range"])}</span>'
                     f'<span class="body"><span class="t">{escape(ch["label"])}</span>'
                     f'<span class="k">{escape(ch["k"])}</span></span>'
                     f'<span class="marks" aria-hidden="true">{marks}</span></a></li>')
        return rows

    # Skill availability is derived from the public packages on disk, never
    # fixed in copy: a row is available when skills/<name>/SKILL.md exists.
    def skill_is_available(name):
        return (REPO / 'skills' / name / 'SKILL.md').is_file()

    def skill_rows(entries, planned=False):
        lis = ''
        for sk in entries:
            name = sk['name']
            if planned:
                glyph = '<span class="pending" aria-hidden="true">\u00b7\u00b7\u00b7</span>'
                title = f'<span class="t">{escape(sk["title"])}</span>'
                status = '<span class="status">Planned</span>'
                dir_html = f'<span class="dir">skills/{escape(name)}/</span>'
                cls = ' class="is-planned"'
            else:
                glyph = SKILLS[name]
                title = f'<a class="t" href="skills/{escape(name)}/">{escape(sk["title"])}</a>'
                status = '<span class="status is-available">Available</span>'
                dir_html = (f'<span class="dir"><a href="{GITHUB}/tree/HEAD/skills/{escape(name)}">'
                            f'skills/{escape(name)}/</a></span>')
                cls = ''
            lis += (f'<li{cls}><span class="glyph-box" aria-hidden="true">{glyph}</span>'
                    f'{title}<span class="when">{escape(sk["use"])}</span>'
                    f'<span class="meta">{status}{dir_html}</span></li>')
        return f'<ul class="skill-rows" role="list">{lis}</ul>'

    available = [sk for sk in idx['skills'] if skill_is_available(sk['name'])]
    installed_names = {sk['name'] for sk in available}
    planned = [dict(name=p['name'], title=p['title'], use=p['when'])
               for p in home['skills_planned'] if p['name'] not in installed_names]
    for p in planned:  # a planned entry whose package shipped is a copy defect
        if skill_is_available(p['name']):
            raise SystemExit(f'landing(): skills_planned lists {p["name"]!r}, whose public package exists')
    skills_html = skill_rows(available)
    if planned:
        skills_html += ('<p class="rows-note">In preparation \u2014 not available yet, '
                        'no package checks run</p>' + skill_rows(planned, planned=True))

    report_by_path = {r['path']: r for r in idx['reports']}
    shelves = ''.join(shelf_row(s_, report_by_path[s_['investigation']]) for s_ in home['shelves'])

    # The three investigations as directory rows; no per-report guide count, so
    # report 01 is not misread through a number its own evidence does not carry.
    report_rows = ''.join(
        f'<li><a href="{escape(r["path"][:-3] + ".html")}">'
        f'<span class="range">Report {n:02d}</span>'
        f'<span class="body"><span class="t">{escape(r["title"])}</span>'
        f'<span class="k">{escape(home["reports_topics"][r["path"]])}</span></span></a></li>'
        for n, r in enumerate(idx['reports'], 1))

    closing_links = [('README.md', 'Handbook index'), ('adoption.md', 'Adopting a skill'), ('prompts.md', 'Task prompts'),
                     ('validation.md', 'Validation'), ('examples/recurring-rule/README.md', 'Runnable lint example'),
                     ('CONTRIBUTING.md', 'Contributing'), (GITHUB, 'GitHub repository')]
    em = home.get('title_em', '')
    title_html = escape(home['title']).replace(em, f'<em>{em}</em>', 1) if em else escape(home['title'])

    # The closing ledger: every row a status the page can defend, so the
    # foot of the page is a record rather than two columns of prose.
    ledger = ''.join(
        f'<li><span class="st st-{escape(s.lower().replace(" ", "-"))}">{escape(s)}</span><span class="what">{escape(w)}</span></li>'
        for s, w in home['ledger']['rows'])
    credits = ''.join(
        f'<div><dt>{escape(k)}</dt><dd>{escape(v)}{(" <span class=" + chr(34) + "h" + chr(34) + ">" + escape(x) + "</span>") if x else ""}</dd></div>'
        for k, v, x in home['ledger']['credits'])
    body = f"""{site_head('', 'index.html')}
<main id="main">
<header class="opening"><div class="wrap">
  <div class="opening-copy">
    <h1>{title_html}</h1>
    <p class="lead">{escape(home['lead'])}</p>
    <div class="actions"><a class="btn primary" href="lessons/recurring-mistakes.html">Start with lesson 1</a><a class="btn" href="#problems">Find my problem</a></div>
    <p class="count-line"><a href="lessons.html"><span class="n">{n_lessons}</span> lessons</a></p>
  </div>
  <div class="pick">
    <h2 id="problems">Start with the problem you have</h2>
    <p>Find what keeps going wrong. Open the matching lesson—or the deeper guide.</p>
    <figure class="pick-figure">
      <img src="assets/problem-to-lesson.webp" width="1400" height="354" alt="Illustration of a browser warning leading to a handbook and a checklist." decoding="async">
      <figcaption><span>Your problem</span> <span>Your lesson</span> <span>A fix to try</span></figcaption>
    </figure>
    <ul role="list" aria-labelledby="problems">{pick}</ul>
  </div>
  <figure class="hero-figure">{hero()}</figure>
</div></header>

<section class="band" id="lessons" aria-labelledby="lessons-band-h"><div class="wrap"><div class="lane">
  {band_head('The lessons', 'lessons-band-h', home['lessons_heading'], home['lessons_description'])}
  <ul class="directory" role="list">{chapter_rows()}</ul>
  <p class="route">{more('lessons.html', f'All {n_lessons} lessons')}</p>
</div></div></section>

<section class="band" id="skills" aria-labelledby="skills-h"><div class="wrap">
  {band_head('Portable skills', 'skills-h', f'{len(available)} skills you can use today', home['skills_description'], 'split')}
  {skills_html}
  <p class="route">{more('skills.html', 'Choose a skill')}</p>
</div></section>

<section class="band" id="guides" aria-labelledby="guides-h"><div class="wrap"><div class="lane">
  {band_head('Implementation', 'guides-h', home['guides_heading'], home['guides_description'])}
  <ul class="directory" role="list">{shelves}</ul>
  <p class="route">{more('guides.html', f'All {len(idx["guides"])} guides')}</p>
</div></div></section>

<section class="band" id="reports" aria-labelledby="reports-h"><div class="wrap">
  {band_head('Evidence', 'reports-h', home['reports_heading'], home['reports_description'], 'centered')}
  <ol class="directory" role="list">{report_rows}</ol>
  <p class="route centered">{more('investigations.html', f'All {len(idx["reports"])} investigations')}</p>
</div></section>

<section class="wrap closing" id="checked">
  <div class="ledger-col"><h2>What was checked, and what was not</h2>
    <ol class="ledger" role="list">{ledger}</ol>
    <p class="route">{more('validation.md', 'The full validation record')}</p>
  </div>
  <div id="attribution" class="credits-col"><h2>Attribution</h2>
    <dl class="credits">{credits}</dl>
    <p class="attr">{idx['attribution']}</p>
    <p class="attr">Frames are short excerpts from the video, reproduced for identification and commentary; they remain \u00a9 Theo / their original owners. Full attribution in <a href="ATTRIBUTION.md">ATTRIBUTION.md</a>.</p>
    <ul>{''.join(f'<li><a class="chip" href="{escape(u)}">{escape(t)}</a></li>' for u, t in closing_links)}</ul>
  </div>
</section>
</main>
{site_foot('', escape(home['basis_short']))}"""
    return document(home['title'], '', rewrite_refs(body), home['page_descriptions']['index.html'],
                    'index.html')


# ------------------------------------------------------------ section pages
def hub_head(marker_label, hub, tail=''):
    """The head of a section page: marker, the page's own h1 and its lead."""
    return ('<main id="main"><header class="section-head"><div class="wrap">'
            f'<h1>{escape(hub["h1"])}</h1>'
            f'<p class="lead">{inline(hub["lead"])}</p>{tail}</div></header>')


def lessons_index(idx, home, lessons):
    """The lesson hub: the ten canonical lessons in three chapters, each row
    one link carrying its number, title, summary and optional depth."""
    hub = home['hubs']['lessons']
    tail = ('<p class="head-links"><a href="evidence/video-research.md">Detailed extraction</a> \u00b7 '
            '<a href="evidence/video-tips.json">Structured ideas file</a></p>')
    sections = ''
    for ch in home['chapters']:
        here = [l for l in lessons if l['chapter'] == ch['id']]
        if not here:
            raise SystemExit(f'lessons_index(): chapter {ch["id"]!r} holds no lessons')
        rows = ''
        for l in here:
            brief = ' \u00b7 '.join(f'Guide {g}' for g in l['guide_ids'])
            brief += ' \u00b7 optional skill' + (' (planned)' if l['skill_planned'] else '')
            full = ' \u00b7 '.join(f'Guide {g}' for g in l['guide_ids'])
            full += ' \u00b7 ' + ' \u00b7 '.join(l['skill_ids'])
            if l['skill_planned']:
                full += ' (planned)'
            # One derived reading estimate per row: computed from the lesson's
            # own text at 220 words per minute and labelled as an estimate.
            minutes = lesson_catalog.read_minutes((REPO / l['source']).read_text())
            estimate = f'About {minutes} min, estimated'
            rows += (f'<li class="lesson-row"><a href="{escape(l["page"])}">'
                     f'<span class="n" aria-hidden="true">{l["order"]:02d}</span>'
                     f'<span class="sr-only">Lesson {l["order"]}: </span>'
                     f'<span class="body"><span class="t">{escape(l["title"])}</span>'
                     f'<span class="s">{escape(l["summary"])}</span></span>'
                     f'<span class="meta"><span class="m-brief">{escape(brief)}</span>'
                     f'<span class="m-full">{escape(full)}</span>'
                     f'<span class="min">{escape(estimate)}</span></span>'
                     f'</a></li>')
        sections += (f'<section class="chapter" id="{escape(ch["id"])}" '
                     f'aria-labelledby="{escape(ch["id"])}-h"><div class="wrap">'
                     f'<div class="chapter-head"><h2 id="{escape(ch["id"])}-h"><span class="label">{escape(ch["label"])}</span></h2>'
                     f'<span class="range">{escape(ch["range"])}</span></div>'
                     f'<p class="chapter-lead">{escape(ch["lead"])}</p>'
                     f'<ol class="lesson-list" role="list">{rows}</ol></div></section>')

    body = (site_head('', 'lessons.html') +
            hub_head('Lessons', hub, tail) +
            sections +
            f'{hub_next(hub)}</main>' +
            site_foot('', escape(home['basis_short'])))
    (OUT / 'lessons.html').write_text(document(hub['title'], '', rewrite_refs(body), hub['description'], 'lessons.html'))


def guides_index(idx, home):
    guide_by_n = {g['n']: g for g in idx['guides']}
    report_by_path = {r['path']: r for r in idx['reports']}
    shelves = ''
    for s_ in home['shelves']:
        ns = s_['guides']
        span = f'Guide {ns[0]}' if len(ns) == 1 else f'Guides {ns[0]}–{ns[-1]}'
        report = report_by_path[s_['investigation']]
        tiles = ''.join(guide_tile(guide_by_n[n], home) for n in ns)
        shelves += (f'<section class="shelf" id="{escape(s_["id"])}" aria-labelledby="{escape(s_["id"])}-h"><div class="wrap">'
                    f'<div class="shelf-head"><h2 id="{escape(s_["id"])}-h">+ {escape(s_["title"])}</h2>'
                    f'<p>{inline(s_["description"])} Investigation: <a href="{escape(report["path"])}">{escape(report["title"])}</a>.</p>'
                    f'<span class="count">{span}</span></div>'
                    f'<ul class="tiles guides" role="list">{tiles}</ul></div></section>')
    hub = home['hubs']['guides']
    # The track: thirteen stages on one rail, grouped by source. The first
    # stage of each group carries the group's mono label above the rail.
    stages = ''
    for s_ in home['shelves']:
        for k, n in enumerate(s_['guides']):
            g = guide_by_n[n]
            seg = f'<span class="seg" aria-hidden="true">+ {escape(s_["title"])}</span>' if k == 0 else ''
            stages += (f'<li class="stage" data-shelf="{escape(s_["id"])}">{seg}<span class="bar" aria-hidden="true"></span>'
                       f'<span class="art" aria-hidden="true">{GUIDES[n]}</span>'
                       f'<a class="t" href="{escape(g["path"])}"><span class="n" aria-hidden="true">{n}</span>'
                       f'<span class="sr-only">Guide {n}: </span>{escape(g["title"])}</a>'
                       f'<p class="when">{escape(home["use_when"][n])}</p></li>')
    track = ('<section class="band track-band" aria-labelledby="track-h"><div class="wrap">'
             f'<h2 id="track-h">Browse the guides by source</h2>'
             '<p class="tier-lead">Scroll across the thirteen guides and use the labels above them to identify each source.</p></div>'
             '<div class="wrap"><div class="track-row" data-row="of" tabindex="0" role="region" aria-label="The thirteen guides as a track">'
             f'<ol class="track" role="list">{stages}</ol></div></div></section>')
    body = (site_head('', 'guides.html') +
            hub_head('Guides', hub) + track +
            f'<div class="band shelves-band">{shelves}</div>{hub_next(hub)}</main>' +
            site_foot('', escape(home['basis_short'])))
    (OUT / 'guides.html').write_text(document(hub['title'], '', rewrite_refs(body), hub['description'], 'guides.html'))


def investigations_index(idx, home):
    """The investigations page as three full-viewport studies, one per report.

    Each study leads with its authored diagram at the size the drawing deserves,
    then the counted evidence that this report earned its shelf, the claim, the
    findings edited from the report's own takeaway section, and the route to the
    full write-up. Findings copy lives in home.json so it stays editable."""
    hub = home['hubs']['investigations']
    findings = hub['findings']
    facts = report_facts(idx, home)

    studies = []
    for n, r in enumerate(idx['reports'], 1):
        rel = r['path']
        meta = facts[rel]['meta']
        items = ''.join(f'<li><span class="ix" aria-hidden="true">[{i:02d}]</span>{escape(t)}</li>'
                        for i, t in enumerate(findings[rel], 1))
        studies.append(
            f'<section class="study" id="study-{n:02d}" aria-labelledby="study-{n:02d}-h"><div class="wrap">'
            f'<figure class="study-figure" aria-hidden="true">{INVESTIGATIONS[rel]}</figure>'
            f'<div class="study-body"><p class="study-meta">{escape(meta)}</p>'
            f'<h2 id="study-{n:02d}-h">{escape(r["title"])}</h2>'
            f'<p class="claim">{escape(CLAIMS[rel])}</p>'
            f'<ol class="findings" role="list">{items}</ol>'
            f'<p class="study-cta"><a class="btn primary" href="{rel[:-3]}.html">Read the full report</a>'
            f'<a class="more" href="{rel}">Editable Markdown</a></p></div></section>')
    # The .md links above must stay .md, so the studies bypass rewrite_refs;
    # everything else goes through it as usual.
    body = (rewrite_refs(site_head('', 'investigations.html') + hub_head('Investigations', hub)) +
            ''.join(studies) + hub_next(hub) + '</main>' +
            rewrite_refs(site_foot('', escape(home['basis_short']))))
    (OUT / 'investigations.html').write_text(document(hub['title'], '', body, hub['description'],
                                                     'investigations.html'))


def skills_index(idx, home):
    tiles = ''.join(skill_tile(sk) for sk in idx['skills'])
    # What every skill page carries, said once here rather than seven times. The
    # instruction to adopt one rather than all of them now opens the page, where a
    # reader meets it before choosing, and the adoption route closes it.
    adopt = ('<p class="route">Open a skill to read its instructions and both reference files. The page links its unchanged '
             '<code>SKILL.md</code> and its directory on GitHub. Choose the one that fits the problem; '
             'do not load all of them for every task.</p>')
    hub = home['hubs']['skills']
    body = (site_head('', 'skills.html') +
            hub_head('Portable skills', hub) +
            '<section class="band" aria-label="The portable skills"><div class="wrap">'
            f'<ul class="tiles cards skills" role="list">{tiles}</ul>{adopt}</div></section>'
            f'{hub_next(hub)}</main>' +
            site_foot('', escape(home['basis_short'])))
    (OUT / 'skills.html').write_text(document(hub['title'], '', rewrite_refs(body), hub['description'], 'skills.html'))


# ------------------------------------------------------------- skill pages
def flat_toc(tokens):
    """[(depth, id, name)] for the rail/disclosure list."""
    out = []

    def walk(ts, d=0):
        for t in ts:
            out.append((d, t['id'], t['name']))
            walk(t.get('children') or [], d + 1)
    walk(tokens)
    return out


def toc_flat(entries):
    if not entries:
        return ''
    items = ''.join(f'<li class="d{d}"><a href="#{escape(i)}">{escape(n)}</a></li>'
                    for d, i, n in entries)
    return f'<ol>{items}</ol>'


def ref_anchor(name):
    """In-page id for a skill reference file: references/foo.md -> ref-foo."""
    return 'ref-' + Path(name).stem


def skill_page(sk, idx, home):
    """One portable skill as a designed page: its own instructions, its
    references as sections, and the routes an adopter needs."""
    prefix = '../../'
    src = REPO / 'skills' / sk['name']
    text = (src / 'SKILL.md').read_text()
    fm = re.search(r'^description:\s*"(.*)"\s*$', text.split('---', 2)[1] if text.startswith('---\n') else '', re.M)
    description = fm.group(1) if fm else ''
    body_text = text.split('---', 2)[2].lstrip() if text.startswith('---\n') else text
    lines = body_text.splitlines()
    h1_at = next((i for i, l in enumerate(lines) if l.startswith('# ')), None)
    title = inline(lines[h1_at][2:].strip()) if h1_at is not None else escape(sk['title'])
    if h1_at is not None:
        lines = lines[:h1_at] + lines[h1_at + 1:]
    body_md = re.sub(r'\]\((references/[^)]+\.md)\)',
                     lambda m: f'](#{ref_anchor(m.group(1))})', '\n'.join(lines))
    body_html, toc = md_convert(body_md)

    refs_html, ref_entries = '', []
    for ref in sorted((src / 'references').glob('*.md')):
        rid = ref_anchor(ref.name)
        ref_lines = ref.read_text().splitlines()
        # The reference's own h1 titles the section; it does not repeat inside it.
        ref_title = ref.stem
        h1_at = next((i for i, l in enumerate(ref_lines) if l.startswith('# ')), None)
        if h1_at is not None:
            ref_title = inline(ref_lines[h1_at][2:].strip())
            ref_lines = ref_lines[:h1_at] + ref_lines[h1_at + 1:]
        # The badge marks a document boundary; the rail's list keeps the plain words.
        label = f'<span class="kind">Reference</span> {ref_title}'
        plain = f'Reference: {ref_title}'
        frag, _ = md_convert(re.sub(r'(?m)^(#{1,5}) ', r'#\1 ', '\n'.join(ref_lines)))
        frag = re.sub(r'id="', f'id="{rid}-', frag)
        frag = re.sub(r'href="#', f'href="#{rid}-', frag)
        refs_html += f'<section class="skill-ref" id="{rid}"><h2 id="{rid}-h">{label}</h2>{frag}</section>'
        ref_entries.append((0, rid + '-h', plain))
    entries = flat_toc(toc) + ref_entries

    toc_html = toc_flat(entries)
    toc_nav = f'<nav class="toc" aria-label="Sections of this page">{toc_html}</nav>' if toc_html else ''
    toc_mobile = (f'<details class="toc-mobile"><summary>On this page</summary>{toc_nav}</details>'
                  if toc_html else '')
    fed = ''.join(f'<p><a class="chip" href="{prefix}{i["page"]}">'
                  f'<span class="n">{i["n"]:02d}</span>{escape(i["idea"])}</a></p>'
                  for i in sk['fed'])
    cites = ''.join(f'<p>{guide_chip(g["title"], g["path"])}</p>' for g in sk['guides'])
    gh = f'{GITHUB}/tree/HEAD/skills/{sk["name"]}'
    rail = ('<aside class="rail" aria-label="Page tools">'
            f'<div><h2>On this page</h2>{toc_nav}</div>'
            f'<div class="place"><h2>This skill</h2>'
            f'<p>{fed_line(sk)}</p>'
            f'<div class="use">{fed}</div></div>'
            f'<div class="leads"><h2>In the guides</h2>{cites or "<p>No idea in the set routes here through a guide.</p>"}</div>'
            f'<div class="source"><h2>Adopt</h2>'
            f'<p><a href="SKILL.md">Raw SKILL.md as shipped</a></p>'
            f'<p><a href="{gh}">Directory on GitHub <span aria-hidden="true">&#8599;</span></a></p>'
            f'<p><a href="{prefix}adoption.html">How to install or combine</a></p></div>'
            '</aside>')
    page = (site_head(prefix, f'skills/{sk["name"]}/index.html') +
            f'<main id="main" class="wrap reader skill-page"><div class="col">'
            f'<header class="page-head">'
            f'<p class="context"><span class="n">SKILL</span> <span aria-hidden="true">·</span> '
            f'<a href="{prefix}skills.html">All skills</a></p>'
            f'<span class="art" aria-hidden="true">{SKILLS[sk["name"]]}</span>'
            f'<h1>{title}</h1><p class="deck">{escape(sk["use"])}</p></header>'
            f'{toc_mobile}<article>{body_html}{refs_html}</article>'
            f'<p class="source-note"><a href="{GITHUB}/blob/HEAD/skills/{sk["name"]}/SKILL.md">SKILL.md on GitHub</a> · '
            f'<a href="{prefix}index.html">Home</a> · {SITE_NAME}, {EDITION_DATE}</p>'
            f'</div>{rail}</main>' +
            site_foot(prefix, escape(home['basis_short'])))
    out = OUT / sk['page']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(f'Skill: {title}', prefix, rewrite_refs(page, prefix),
                            summarise(description), sk['page']))


def lesson_page(lesson, idx, home, lessons):
    """One canonical lesson: the authored Markdown, the video moments it
    consolidates, its optional depth, and its place in the ten-lesson order."""
    prefix = '../'
    tip_ideas = {i['tip']['id']: i for i in idx['ideas']}
    here = [tip_ideas[t] for t in lesson['tip_ids']]
    here.sort(key=lambda i: i['tip']['start_seconds'])
    pos = lesson['order']
    chapter = next(c for c in home['chapters'] if c['id'] == lesson['chapter'])
    prev_l = lessons[pos - 2] if pos > 1 else None
    next_l = lessons[pos] if pos < len(lessons) else None

    def seq(a, cls, k):
        if not a:
            return ''
        return (f'<a class="{cls}" href="{escape(prefix + a["page"])}"><span class="k">{k}</span>'
                f'<span class="n">{a["order"]:02d}</span> {escape(a["title"])}</a>')
    seq_links = seq(prev_l, 'prev', 'Previous lesson') or f'<a class="prev" href="{prefix}lessons.html"><span class="k">Start of the lessons</span>All ten lessons</a>'
    seq_links += seq(next_l, 'next', 'Next lesson') or f'<a class="next" href="{prefix}guides.html"><span class="k">After the last lesson</span>The thirteen guides</a>'
    rail_seq = seq_links.replace('class="prev"', '').replace('class="next"', '')

    glyphs = ''.join(
        f'<figure><span class="g" aria-hidden="true">{IDEAS[f"{i["n"]:02d}"]}</span>'
        f'<figcaption><a class="ts" href="{escape(i["url"])}">{escape(i["ts"])}</a></figcaption></figure>'
        for i in here)
    n = len(here)
    glyphs_label = (f'The {n} video moments this lesson consolidates' if n > 1
                    else 'The video moment this lesson consolidates')

    # The lesson's own Markdown is the article; its accepted prose carries the
    # source anchors and citations unchanged.
    text = (REPO / lesson['source']).read_text()
    lines = [l for l in text.splitlines() if not l.startswith('# ')]
    while lines and not lines[0].strip():
        lines.pop(0)
    body_md = '\n'.join(lines)
    body_html, toc = md_convert(body_md)
    body = rewrite_tables(rewrite_refs(body_html))
    # Incoming legacy fragments resolve to actual content regions. Keep the
    # opening paragraph first so its existing lead styling is preserved.
    body = body.replace('<p>', '<p id="said">', 1)
    opening_end = body.find('</p>') + len('</p>')
    body = body[:opening_end] + '<span id="useful" class="anchor" aria-hidden="true"></span>' + body[opening_end:]
    action = re.search(r'<(?:ol|pre)\b', body)
    if action is None:
        raise ValueError(f'{lesson["source"]}: missing action list or command example')
    body = body[:action.start()] + '<span id="apply" class="anchor" aria-hidden="true"></span>' + body[action.start():]
    headings = list(re.finditer(r'<h2\b[^>]*>.*?</h2>', body, re.S))
    substantive = [h for h in headings if strip_tags(h.group()).strip().lower() != 'sources']
    if not substantive:
        raise ValueError(f'{lesson["source"]}: missing qualification section')
    last = substantive[-1].start()
    body = body[:last] + '<span id="qualification" class="anchor" aria-hidden="true"></span>' + body[last:]
    toc_html = toc_list(toc)
    toc_nav = f'<nav class="toc" aria-label="Sections of this page">{toc_html}</nav>' if toc_html else ''
    toc_mobile = (f'<details class="toc-mobile"><summary>On this page</summary>{toc_nav}</details>'
                  if toc_html else '')

    guide_chips = ''.join(
        # The chip target is finished HTML, so no later rewrite may add the
        # page prefix a second time.
        f'<p>{guide_chip(g["title"], g["path"][:-3] + ".html", prefix=prefix)}</p>'
        for g in idx['guides'] if g['n'] in lesson['guide_ids'])
    skill_by_name = {sk['name']: sk for sk in idx['skills']}
    skill_chips = ''.join(f'<p><a class="chip" href="{escape(prefix)}skills/{escape(s)}/">'
                          f'{escape(skill_by_name[s]["title"])}</a></p>'
                          for s in lesson['skill_ids'])
    watch_first = (f'<p><a class="ts" href="{escape(here[0]["url"])}">Watch at {escape(here[0]["ts"])} '
                   f'<span aria-hidden="true">&#8599;</span></a></p>')
    moments = ', '.join(escape(i['ts']) for i in here)
    rail = ('<aside class="rail" aria-label="Page tools">'
            + (f'<div><h2>On this page</h2>{toc_nav}</div>' if toc_html else '')
            + f'<div class="place"><h2>This lesson</h2>'
              f'<p><span class="n">{pos:02d}</span> of {len(lessons)} \u00b7 '
              f'<a href="{prefix}lessons.html#{escape(lesson["chapter"])}">{escape(chapter["label"])}</a></p>'
              f'<p class="use">{escape(lesson["summary"])}</p>'
              f'<p class="use">About {lesson_catalog.read_minutes(text)} min, estimated from the text</p></div>'
            + f'<div class="watch"><h2>In the video</h2>{watch_first}'
              f'<p class="use">{n} moment{"s" if n != 1 else ""}: {moments}</p></div>'
            + f'<div class="leads"><h2>Where it leads</h2>{guide_chips}{skill_chips}</div>'
            + f'<div class="neighbours"><h2>Sequence</h2>{rail_seq}</div>'
            + f'<div class="source"><h2>Source</h2><a href="{Path(lesson["source"]).name}">Lesson Markdown</a> \u00b7 '
              f'<a href="{prefix}evidence/video-tips.json">Structured extraction</a> \u00b7 '
              f'<a href="{prefix}evidence/video-research.html">Full notes</a></div>'
            '</aside>')
    desks_figure = f'<figure class="desks-figure" aria-hidden="true">{desks()}</figure>' if lesson['id'] == DESKS_ON_LESSON else ''
    page = (site_head(prefix, '') +
            f'<main id="main" class="wrap reader lesson-page"><div class="col">'
            f'<header class="page-head">'
            f'<p class="context"><span class="n">Lesson {pos:02d}</span> <span>of {len(lessons)}</span> '
            f'<span aria-hidden="true">\u00b7</span> '
            f'<a href="{prefix}lessons.html#{escape(lesson["chapter"])}">{escape(chapter["label"])}</a></p>'
            + (f'<div class="tip-glyphs" role="group" aria-label="{escape(glyphs_label)}">{glyphs}</div>' if glyphs else '')
            + f'<h1>{escape(lesson["title"])}</h1>'
            + f'<p class="read-min">About {lesson_catalog.read_minutes(text)} min read, estimated from the text</p>'
            + f'{desks_figure}</header>'
            f'{toc_mobile}<article>{body}</article>'
            f'<nav class="guide-seq" aria-label="Lesson sequence">{seq_links}</nav>'
            f'<p class="source-note"><a href="{Path(lesson["source"]).name}">Lesson Markdown</a> \u00b7 '
            f'<a href="{prefix}index.html">Home</a> \u00b7 {SITE_NAME}, {EDITION_DATE}</p>'
            f'</div>{rail}</main>' +
            site_foot(prefix, escape(home['basis_short'])))
    out = OUT / lesson['page']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(f'Lesson {pos:02d}: {lesson["title"]}', prefix, page,
                            summarise(f'{lesson["title"]}. {lesson["summary"]}'),
                            lesson['page']))
    # The lesson's Markdown ships beside its page, like every other reader page.
    shutil.copy2(REPO / lesson['source'], (OUT / lesson['source']))  # lessons/<id>.md


# The legacy layer: the old nineteen idea routes stay reachable as lightweight
# alias pages that hand the reader to the lesson covering that observation, so
# no old full article survives as duplicate canonical content. Each old region
# keeps its name and carries it through: the alias links into the lesson with
# the matching fragment instead of dropping it, and the lesson answers the
# fragment with a real anchor (see lesson_page).
LEGACY_FRAGMENTS = (
    ('said', 'What was said'),
    ('apply', 'How to apply it'),
    ('useful', 'Where this leads'),
    ('qualification', 'Sources and limits'),
)


def legacy_ideas_index(idx, home, lessons):
    """ideas.html as a lightweight alias of the lesson index."""
    lesson_by_tip = {}
    for l in lessons:
        for t in l['tip_ids']:
            lesson_by_tip[t] = l
    links = ''.join(
        f'<li><a href="{escape(l["page"])}"><span class="n">{l["order"]:02d}</span> '
        f'{escape(l["title"])}</a></li>'
        for l in lessons)
    body = (site_head('', 'ideas.html') +
            '<main id="main" class="wrap reader"><div class="col">'
            '<header class="page-head"><p class="context"><a href="lessons.html">The ten lessons</a></p>'
            '<h1>The nineteen video ideas, consolidated into ten lessons</h1></header>'
            '<article><p>Every observation from the video now lives inside the lesson that '
            'covers it, with its exact video moment and qualification attached. The old '
            'per-idea pages are lightweight aliases; the canonical reading order is the '
            '<a href="lessons.html">lesson index</a>, and the original evidence remains in the '
            '<a href="evidence/video-research.html">detailed extraction</a> and the '
            '<a href="evidence/video-tips.json">structured ideas file</a>.</p>'
            f'<ol class="lesson-list" role="list">{links}</ol></article>'
            f'<p class="source-note"><a href="lessons.html">All ten lessons</a> \u00b7 '
            f'<a href="index.html">Home</a> \u00b7 {SITE_NAME}, {EDITION_DATE}</p>'
            f'</div></main>' +
            site_foot('', escape(home['basis_short'])))
    out = OUT / 'ideas.html'
    out.write_text(document('The video ideas, consolidated into ten lessons', '', rewrite_refs(body),
                            'Each of the nineteen video observations now lives inside the lesson '
                            'that covers it. Routes to the canonical lesson index.', 'ideas.html'))
    # The canonical of a compatibility alias points at the canonical index, not
    # at itself.
    text = out.read_text().replace(
        '<link rel="canonical" href="' + SITE_URL + '/ideas.html">',
        '<link rel="canonical" href="' + SITE_URL + '/lessons.html">')
    text = text.replace(
        '<meta property="og:url" content="' + SITE_URL + '/ideas.html">',
        '<meta property="og:url" content="' + SITE_URL + '/lessons.html">')
    out.write_text(text)


def legacy_idea_page(i, lesson, home):
    """One old ideas/<slug>.html route as a lightweight alias of its lesson,
    keeping the old in-page fragments (said, apply, useful, qualification)
    reachable on the way through."""
    prefix = '../'
    fragments = ''.join(
        f'<p><span id="{frag}"></span>'
        f'<a href="{escape(prefix + lesson["page"])}#{frag}">{escape(label)}</a></p>'
        for frag, label in LEGACY_FRAGMENTS)
    body = (site_head(prefix, '') +
            f'<main id="main" class="wrap reader"><div class="col">'
            f'<header class="page-head"><p class="context"><span class="n">Moved</span> '
            f'<span aria-hidden="true">\u00b7</span> <a href="{prefix}lessons.html">The ten lessons</a></p>'
            f'<h1>{escape(i["idea"])}</h1></header>'
            f'<article><p>This observation is now part of <a href="{escape(prefix + lesson["page"])}">'
            f'Lesson {lesson["order"]:02d}, {escape(lesson["title"])}</a>, together with the other '
            f'observations that lesson covers. The video moment: '
            f'<a href="{escape(i["url"])}">{escape(i["ts"])}</a>. The evidence behind it stays in the '
            f'<a href="{prefix}evidence/video-research.html">detailed extraction</a>.</p>{fragments}</article>'
            f'<p class="source-note"><a href="{escape(prefix + lesson["page"])}">The lesson</a> \u00b7 '
            f'<a href="{prefix}lessons.html">All ten lessons</a> \u00b7 <a href="{prefix}index.html">Home</a></p>'
            f'</div></main>' +
            site_foot(prefix, escape(home['basis_short'])))
    out = OUT / i['page']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(f'{i["idea"]} (moved into a lesson)', prefix, rewrite_refs(body),
                            f'This video observation moved into lesson {lesson["order"]:02d}, '
                            f'{lesson["title"]}.', i['page']))
    # The alias announces its lesson as its address: canonical and og:url must
    # agree, so a shared old URL previews and resolves as the lesson it became.
    lesson_url = SITE_URL + '/' + lesson['page']
    text = out.read_text()
    text = text.replace(
        '<link rel="canonical" href="' + SITE_URL + '/' + i['page'] + '">',
        '<link rel="canonical" href="' + lesson_url + '">')
    text = text.replace(
        '<meta property="og:url" content="' + SITE_URL + '/' + i['page'] + '">',
        '<meta property="og:url" content="' + lesson_url + '">')
    out.write_text(text)


# ------------------------------------------------------------ reader pages
def toc_list(tokens):
    """Nested list of the page's h2 (and h3) sections from the toc extension."""
    def items(tokens):
        out = ''
        for t in tokens:
            children = items(t['children']) if t.get('children') else ''
            out += f'<li><a href="#{escape(t["id"])}">{escape(t["name"])}</a>{children}</li>'
        return f'<ol>{out}</ol>' if out else ''
    return items(tokens)


def evidence_figures(frames_for_page, prefix):
    return ''.join(
        f'<figure><a class="shot" href="{prefix}evidence.html#frame-{f["seconds"]}">'
        f'<img src="{prefix}screenshots/{escape(f["file"])}" width="1920" height="1080" loading="lazy" alt="{escape(frame_alt(f))}"></a>'
        f'<figcaption><span class="t">{escape(f["timestamp"])}</span> {escape(f["title"])}</figcaption></figure>'
        for f in frames_for_page)


def reader_page(rel, idx, home, frames):
    path = REPO / rel
    out = (OUT / rel).with_suffix('.html')
    prefix = depth_prefix(out)
    current = out.relative_to(OUT).as_posix()
    text = path.read_text()
    if text.startswith('---\n'):
        text = text.split('---', 2)[2].lstrip()

    # The page's own h1 becomes the designed page head; the article starts after it.
    lines = text.splitlines()
    h1_at = next((i for i, l in enumerate(lines) if l.startswith('# ')), None)
    own_title = inline(lines[h1_at][2:].strip()) if h1_at is not None else escape(path.stem)
    if h1_at is not None:
        lines = lines[:h1_at] + lines[h1_at + 1:]
    body_html, toc = md_convert('\n'.join(lines))
    body = rewrite_tables(rewrite_refs(body_html))

    guides = idx['guides']
    pos = next((i for i, g in enumerate(guides) if g['path'] == rel), None)
    frames_here = []
    context = ''
    place = ''
    neighbours = ''
    seq = ''
    art = ''
    if pos is not None:
        g = guides[pos]
        title_html = escape(g['title'])
        art = f'<span class="art" aria-hidden="true">{GUIDES[g["n"]]}</span>'
        shelf = next(s for s in home['shelves'] if g['n'] in s['guides'])
        shelf_href = f'{prefix}guides.html#{escape(shelf["id"])}'
        context = (f'<p class="context"><span class="n">Guide {g["n"]}</span> <span>of {len(guides)}</span> '
                   f'<span aria-hidden="true">·</span> <a href="{shelf_href}">{escape(shelf["title"])}</a></p>')
        place = (f'<div class="place"><h2>This guide</h2><p><span class="n">{g["n"]}</span> of {len(guides)} · '
                 f'<a href="{shelf_href}">{escape(shelf["title"])}</a></p>'
                 f'<p class="use">{escape(home["use_when"][g["n"]])}</p></div>')
        prev_g = guides[pos - 1] if pos > 0 else None
        next_g = guides[pos + 1] if pos + 1 < len(guides) else None
        seq_links, rail_links = '', ''
        if prev_g:
            href = escape(prefix + prev_g['path'][:-3] + '.html')
            seq_links += (f'<a class="prev" href="{href}"><span class="k">Previous guide</span>'
                          f'<span class="n">{prev_g["n"]}</span> {escape(prev_g["title"])}</a>')
            rail_links += f'<a href="{href}"><span class="k">Previous</span><span class="n">{prev_g["n"]}</span> {escape(prev_g["title"])}</a>'
        else:
            seq_links += f'<a class="prev" href="{prefix}guides.html"><span class="k">Start of the guides</span>All 13 guides</a>'
            rail_links += f'<a href="{prefix}guides.html"><span class="k">Previous</span>All 13 guides</a>'
        if next_g:
            href = escape(prefix + next_g['path'][:-3] + '.html')
            seq_links += (f'<a class="next" href="{href}"><span class="k">Next guide</span>'
                          f'<span class="n">{next_g["n"]}</span> {escape(next_g["title"])}</a>')
            rail_links += f'<a href="{href}"><span class="k">Next</span><span class="n">{next_g["n"]}</span> {escape(next_g["title"])}</a>'
        else:
            seq_links += f'<a class="next" href="{prefix}index.html#reports"><span class="k">After the last guide</span>The three repository investigations</a>'
            rail_links += f'<a href="{prefix}index.html#reports"><span class="k">Next</span>The three repository investigations</a>'
        seq = f'<nav class="guide-seq" aria-label="Guide sequence">{seq_links}</nav>'
        neighbours = f'<div class="neighbours"><h2>Sequence</h2>{rail_links}</div>'
        frames_here = [f for f in frames if home['frame_guides'].get(str(f['seconds'])) == g['n']]
    else:
        title_html = own_title
        if rel in INVESTIGATIONS:
            art = f'<span class="art wide" aria-hidden="true">{INVESTIGATIONS[rel]}</span>'
        if rel in CONTEXT:
            label, anchor = CONTEXT[rel]
            context = f'<p class="context"><a href="{prefix}{anchor}">{escape(label)}</a></p>'
            place = f'<div class="place"><h2>Where this sits</h2><p><a href="{prefix}{anchor}">{escape(label)}</a></p></div>'

    md_name = path.name
    toc_html = toc_list(toc)
    sections = f'<nav class="toc" aria-label="Sections of this page">{toc_html}</nav>' if toc_html else ''
    toc_mobile = (f'<details class="toc-mobile"><summary>On this page</summary>{sections}</details>'
                  if toc_html else '')
    evidence = ''
    evidence_mobile = ''
    if frames_here:
        more = f'<p class="rail-note"><a href="{prefix}evidence.html">All twelve frames</a></p>'
        # The rail shows at most two frames so it fits beside the article;
        # narrow screens have no rail, so every applied frame follows the article.
        evidence = f'<div class="evidence"><h2>Evidence from the video</h2>{evidence_figures(frames_here[:2], prefix)}{more}</div>'
        evidence_mobile = (f'<section class="evidence-mobile" aria-label="Evidence from the video"><h2>Evidence from the video</h2>'
                           f'<div class="figs">{evidence_figures(frames_here, prefix)}</div>{more}</section>')
    rail = ('<aside class="rail" aria-label="Page tools">'
            + (f'<div><h2>On this page</h2>{sections}</div>' if toc_html else '')
            + place + neighbours + evidence
            + f'<div class="source"><h2>Source</h2><a href="{escape(md_name)}">Editable Markdown</a> · <a href="{GITHUB}/blob/main/{escape(rel)}">On GitHub</a></div>'
            '</aside>')
    note = (f'<p class="source-note"><a href="{escape(md_name)}">Editable Markdown source</a> · '
            f'<a href="{prefix}index.html">Home</a> · {SITE_NAME}, {EDITION_DATE}</p>')
    page = (site_head(prefix, current) +
            f'<main id="main" class="wrap reader"><div class="col">'
            f'<header class="page-head">{context}{art}<h1>{title_html}</h1></header>'
            f'{toc_mobile}<article>{body}</article>{evidence_mobile}{seq}{note}</div>{rail}</main>' +
            site_foot(prefix, escape(home['basis_short'])))
    out.parent.mkdir(parents=True, exist_ok=True)
    # A guide's opening paragraph trails into its companion-guide list, which
    # describes the shelf rather than the guide. Its canonical title and the
    # one line saying who it is for do the job instead. Every other reader page
    # opens with prose written to introduce itself, so that prose is the deck
    # and the description both.
    if pos is not None:
        # Method then who it is for. Four of the thirteen pairs are too long
        # together, and there the who-it-is-for line is the better half to keep:
        # the title is already the browser title, so repeating it alone would
        # spend a search result's whole line saying nothing new.
        title_text, use_when = guides[pos]['title'], home['use_when'][guides[pos]['n']]
        description = summarise(f'{title_text}. {use_when}')
        if description.rstrip('.') == title_text.rstrip('.'):
            description = summarise(use_when)
    else:
        first_p = re.search(r'<p>(.*?)</p>', body, re.S)
        description = summarise(first_p.group(1) if first_p else title_html)
    out.write_text(document(TITLES.get(rel, unescape(strip_tags(title_html))), prefix, page,
                            description, out.relative_to(OUT).as_posix()))
    shutil.copy2(path, out.with_suffix('.md'))


# ---------------------------------------------------------------- gallery
def gallery(frames, home, idx):
    out = OUT / 'evidence.html'
    guide_by_n = {g['n']: g for g in idx['guides']}
    strip = ''.join(f'<li><a href="#frame-{f["seconds"]}">{escape(f["timestamp"])}</a></li>' for f in frames)

    def applied(f):
        n = home['frame_guides'].get(str(f['seconds']))
        if not n:
            return ''
        g = guide_by_n[n]
        return f' · Applied in <a href="{escape(g["path"][:-3] + ".html")}">guide {n}, {escape(g["title"])}</a>'

    sections = ''.join(
        f'<section class="frame" id="frame-{f["seconds"]}" aria-labelledby="frame-{f["seconds"]}-h">'
        f'<h2 id="frame-{f["seconds"]}-h"><span class="t">{escape(f["timestamp"])}</span> {escape(f["title"])}</h2>'
        f'<figure><a class="shot" href="screenshots/{escape(f["file"])}">'
        f'<img loading="lazy" width="1920" height="1080" src="screenshots/{escape(f["file"])}" alt="{escape(frame_alt(f))}"></a>'
        f'<figcaption>{escape(f["observation"])}'
        f'<span class="links"><a href="{escape(f["url"])}">Watch this moment</a> · '
        f'<a href="screenshots/{escape(f["file"])}">Full-size frame</a>{applied(f)}</span></figcaption></figure></section>'
        for f in frames)
    hub = home['hubs']['frames']
    body = (site_head('', 'evidence.html') +
            '<main id="main">'
            '<div class="wrap"><header class="gallery-head">'
            f'<h1>{escape(hub["h1"])}</h1><p class="lead">{inline(hub["lead"])}</p>'
            '<p class="links"><a href="evidence/frame-manifest.json">Extraction commands and SHA-256 hashes</a> · '
            '<a href="evidence/video-research.html">Full extraction notes</a></p>'
            f'<ol class="strip" role="list" aria-label="Jump to a frame">{strip}</ol></header>'
            f'<div class="gallery">{sections}</div></div>'
            f'{hub_next(hub)}</main>' +
            site_foot('', escape(home['basis_short'])))
    out.write_text(document(hub['title'], '', body, hub['description'], 'evidence.html'))


# -------------------------------------------------------------- not found
def not_found(home):
    # Served at any path, so its links are root-absolute.
    body = (site_head('/') +
            '<main id="main" class="wrap notfound"><h1>That page is not in the handbook</h1>'
            '<p>The address may have been mistyped, or the page may have moved when the handbook was regenerated. '
            'Everything published here is reachable from the home page.</p>'
            '<ul><li><a href="/index.html">Home: start with the problem you have</a></li>'
            '<li><a href="/lessons.html">The ten lessons</a></li>'
            '<li><a href="/guides.html">All 13 guides</a></li>'
            '<li><a href="/README.html">The handbook index</a></li>'
            '<li><a href="/evidence.html">The frame gallery</a></li></ul></main>' +
            site_foot('/', escape(home['basis_short'])))
    # 404 is served at any path, so it gets no canonical of its own.
    (OUT / '404.html').write_text(document('Page not found', '/', body,
                                           home['page_descriptions']['404.html']))


# ------------------------------------------------------------------- main
def load_catalog():
    """The ten approved lessons through the reviewed catalog seam, plus the
    derived per-lesson facts the renderer adds (never re-parsing the manifest
    here): whether each linked skill's public package exists yet."""
    lessons = lesson_catalog.load_lessons(REPO)
    for l in lessons:
        l['skill_planned'] = any(
            not (REPO / 'skills' / s / 'SKILL.md').is_file() for s in l['skill_ids'])
    return lessons


def sync_readme(write=False):
    """Verify (or, with --sync-readme, write) the README lesson table between
    its markers. Ordinary renders only verify: no hidden README mutation."""
    readme = REPO / 'README.md'
    lessons = load_catalog()
    if write:
        readme.write_text(lesson_catalog.sync_readme_lessons(readme.read_text(), lessons))
        print('README lesson table synced from the validated manifest.')
    else:
        lesson_catalog.sync_readme_lessons(readme.read_text(), lessons, check=True)


def main():
    sync = '--sync-readme' in sys.argv
    if sync:
        sync_readme(write=True)
        return

    # Read and validate every input first: the README index, the landing-page
    # data, the frame manifest, the lesson manifest through the catalog seam,
    # and the README lesson table. Any defect raises here, while the previous
    # public/ output is still untouched, so a malformed input never destroys
    # the last usable preview. Only after all inputs are proven does the render
    # replace public/.
    idx = enrich(read_index(REPO / 'README.md'))
    home = json.loads(HOME.read_text())
    frames = json.loads((REPO / 'evidence/frame-manifest.json').read_text())
    # The canonical lessons come from the reviewed catalog seam; a manifest or
    # lesson defect fails the build here, before anything is written.
    lessons = load_catalog()
    # The README lesson table must already match the manifest: the render
    # verifies it and fails on drift rather than silently fixing the README.
    sync_readme(write=False)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    # Static assets, copied verbatim.
    for d in COPY_DIRS:
        src = REPO / d
        dst = OUT / d
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst,
                        ignore=shutil.ignore_patterns('node_modules', '__pycache__', '.DS_Store'))
    for f in COPY_FILES:
        dst = OUT / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / f, dst)
    (OUT / 'assets').mkdir()
    shutil.copy2(ASSETS / 'handbook.css', OUT / 'assets/handbook.css')
    shutil.copy2(ASSETS / 'handbook.js', OUT / 'assets/handbook.js')
    # The problem panel's drawing: authored through the Higgsfield route on the owner's
    # instruction, transparent, and the one generated raster the design language allows.
    shutil.copy2(ASSETS / 'problem-to-lesson.webp', OUT / 'assets/problem-to-lesson.webp')

    for rel in RENDER_MD:
        reader_page(rel, idx, home, frames)
    gallery(frames, home, idx)
    not_found(home)
    for l in lessons:
        lesson_page(l, idx, home, lessons)
    lessons_index(idx, home, lessons)
    legacy_ideas_index(idx, home, lessons)
    by_tip = lesson_by_tip(lessons)
    for i in idx['ideas']:
        legacy_idea_page(i, by_tip[i['tip']['id']], home)
    guides_index(idx, home)
    investigations_index(idx, home)
    skills_index(idx, home)
    for sk in idx['skills']:
        skill_page(sk, idx, home)
    (OUT / 'index.html').write_text(landing(idx, home, lessons, frames))

    n_skills = len(idx['skills'])
    print(f'Rendered {len(RENDER_MD)} Markdown pages, {len(lessons)} lesson pages, '
          f'{len(idx["ideas"])} legacy idea aliases, {n_skills} skill pages, '
          f'the lessons, guides, skills and investigations indexes, the home page '
          f'({len(lessons)} lessons, {len(idx["guides"])} guides, '
          f'{len(idx["reports"])} investigations, {n_skills} skills, '
          f'{len(frames)} frames), the gallery and 404.html into public/.')


def lesson_by_tip(lessons):
    """tip id -> its one primary lesson; every source tip has exactly one."""
    out = {}
    for l in lessons:
        for t in l['tip_ids']:
            out[t] = l
    return out


if __name__ == '__main__':
    main()
