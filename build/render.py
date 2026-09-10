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

REPO = Path(__file__).resolve().parent.parent
# The claim line of each investigation, copied verbatim from COPY.md.
CLAIMS = {
    'github-inspection.md': "Ten of the thirteen guides trace back to this fork. It is where the video's advice met code that had to work.",
    'matt-pocock-inspection.md': 'A codebase with a glossary and one transport. The two guides on domain language and durable artifacts came from reading it.',
    'boris-cherny-inspection.md': "A compiler tested five different ways. Guide 13's layered validation is that method, generalised.",
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
SITE_URL = ''
EDITION_DATE = 'September 9, 2026'
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

# Header: four section links always visible from 760px, and a native menu
# (<details>) that lists every page. On narrow screens the menu is the whole
# navigation. Items marked primary are hidden inside the menu at wide widths.
PRIMARY_NAV = [
    ('ideas.html', 'Ideas'),
    ('guides.html', 'Guides'),
    ('skills.html', 'Skills'),
    ('investigations.html', 'Investigations'),
    ('evidence.html', 'Frames'),
]
MENU_GROUPS = [
    [('index.html', 'Home', True)] + [(t, l, True) for t, l in PRIMARY_NAV],
    [('README.html', 'Handbook index', False), ('prompts.html', 'Task prompts', False),
     ('adoption.html', 'Adopting a skill', False), ('validation.html', 'Validation', False)],
    [('github-inspection.html', 'Theo: T3 Code and Melee', False),
     ('matt-pocock-inspection.html', 'Matt Pocock: Course Video Manager', False),
     ('boris-cherny-inspection.html', 'Boris Cherny: public work', False)],
    [('ATTRIBUTION.html', 'Attribution', False), ('CONTRIBUTING.html', 'Contributing', False),
     (GITHUB, 'GitHub repository', False)],
]

# A reader page whose own h1 does not make a useful browser title. README's h1
# is the site name, which would render as "X · X" in a tab and a search result.
TITLES = {'README.md': 'Handbook index'}

# Where a non-guide reader page sits in the handbook: (context line, target page).
CONTEXT = {
    'README.md': ('The handbook index', 'guides.html'),
    'github-inspection.md': ('One of three repository investigations', 'investigations.html'),
    'matt-pocock-inspection.md': ('One of three repository investigations', 'investigations.html'),
    'boris-cherny-inspection.md': ('One of three repository investigations', 'investigations.html'),
    'evidence/video-research.md': ('Detailed extraction behind the nineteen ideas', 'ideas.html'),
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
    links = [(f'{prefix}index.html', 'Home'), (f'{prefix}ideas.html', 'Ideas'), (f'{prefix}guides.html', 'Guides'), (f'{prefix}README.html', 'Handbook index'),
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
            f'<meta name="color-scheme" content="dark">{desc}'
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
    for row in table_rows(section(text, 'Four portable skills')):
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


def guide_chip(label, path, prefix=''):
    """A small link: guide number (when the target is a guide) and its label."""
    m = GUIDE_N.search(path)
    n = f'<span class="n">{m.group(1)}</span> ' if m else ''
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
            f'{marker("Next")}<h2 id="hub-next-h">Where to go from here</h2>'
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
    'agent-feedback-engineering': 'FAILURE \u2192 CHECK',
    'agent-ready-workspaces': 'SETUP \u2192 PREVIEW \u2192 PROOF',
    'agent-context-calibration': 'MISSING \u2192 PLACED',
    'agent-tool-adapters': 'GAP \u2192 ADAPTER \u2192 VERIFIED',
}


def skill_tile(sk, prefix=''):
    """One skill as a tall hairline cell: its drawing at a size that carries,
    the caption inside the drawing, then the title, the use, the honest count
    and the routes. Four of these in a 2x2 are the skills figure."""
    cap = SKILL_CAPTIONS.get(sk['name'], '')
    return (f'<li class="tile skill"><span class="art" aria-hidden="true">{SKILLS[sk["name"]]}'
            f'<span class="cap">{cap}</span></span>'
            f'<a class="t" href="{escape(prefix + sk["href"])}">{escape(sk["title"])}</a>'
            f'<p class="when">{escape(sk["use"])}</p>'
            f'<p class="fed"><span class="n">{sk["fed_by"]}</span> {"idea feeds" if sk["fed_by"] == 1 else "ideas feed"} it</p>'
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


def report_row(r, n, prefix=''):
    """One investigation on the home page as a routing row, in the form of the
    guide shelf rows: a mono range, the title, and one line from the README."""
    kicker = r['blurb'].split(' — ')[0].split(',')[0].rstrip('.').strip()
    return (f'<li><a href="{escape(prefix + r["path"][:-3] + ".html")}">'
            f'<span class="range">Report {n:02d}</span>'
            f'<span class="t">{escape(r["title"])}</span>'
            f'<span class="k">{escape(kicker[0].lower() + kicker[1:])}</span></a></li>')


def band_head(label, heading_id, heading, description):
    return (f'<div class="band-head">{marker(label)}'
            f'<h2 id="{heading_id}">{escape(heading)}</h2><p>{inline(description)}</p></div>')


# ------------------------------------------------------------ landing page
def landing(idx, home, frames):
    """The home page: the promise, the entry by problem, one taste of each
    section, and a route out to the page that holds the full set."""
    counts = {'guides': len(idx['guides']), 'reports': len(idx['reports']),
              'skills': len(idx['skills']), 'ideas': len(idx['ideas']), 'frames': len(frames)}
    shelf_guides = [n for s in home['shelves'] for n in s['guides']]
    if sorted(shelf_guides) != sorted(g['n'] for g in idx['guides']):
        raise SystemExit(f'build/home.json shelves list {shelf_guides}; README lists guides differently')

    # The counts strip: mono badges, each a route to the page that holds the set.
    contents = ''.join(
        f'<li><a href="{href}"><span>{counts[key]}</span> {label}</a></li>'
        for key, label, href in [('ideas', 'ideas', 'ideas.html'), ('guides', 'guides', 'guides.html'),
                                 ('skills', 'skills', '#skills'), ('reports', 'investigations', '#reports'),
                                 ('frames', 'frames', 'evidence.html')])

    # Each row gets its drafting marker. The panel reads as a drawn schedule of
    # eight situations rather than a table, and the markers give the accent
    # trace something to pass as the panel scrolls through view.
    pick = ''.join(
        f'<li><span class="ix" aria-hidden="true">[{n:02d}]</span>'
        f'<span class="q">{escape(q)}</span>'
        f'<span class="a">{"".join(guide_chip(label, path) for label, path in links)}</span></li>'
        for n, (q, links) in enumerate(idx['problems'], 1))

    # All nineteen, as one horizontally scrolling track. The wrapper is the
    # scroll region and carries the focus and the label; the track inside it is
    # the list. Previous/next and the counter are added by handbook.js, so
    # without JavaScript this is still a swipeable, arrow-key-scrollable row.
    row = ''.join(idea_tile(i) for i in idx['ideas'])
    skills = ''.join(skill_tile(sk) for sk in idx['skills'])
    report_by_path = {r['path']: r for r in idx['reports']}
    shelves = ''.join(
        f'<li><a href="guides.html#{escape(s_["id"])}"><span class="range">'
        f'{"Guide " + s_["guides"][0] if len(s_["guides"]) == 1 else "Guides " + s_["guides"][0] + "–" + s_["guides"][-1]}</span>'
        f'<span class="t">{escape(s_["title"])}</span>'
        f'<span class="k">{len(s_["guides"])} {"guide" if len(s_["guides"]) == 1 else "guides"} · {escape(report_by_path[s_["investigation"]]["title"])}</span></a></li>'
        for s_ in home['shelves'])
    reports = ''.join(report_row(r, n) for n, r in enumerate(idx['reports'], 1))
    frames_line = ''.join(f'<li><a href="evidence.html#frame-{f["seconds"]}">{escape(f["timestamp"])}</a></li>' for f in frames)

    closing_links = [('README.md', 'Handbook index'), ('adoption.md', 'Adopting a skill'), ('prompts.md', 'Task prompts'),
                     ('validation.md', 'Validation'), ('examples/recurring-rule/README.md', 'Runnable lint example'),
                     ('CONTRIBUTING.md', 'Contributing'), (GITHUB, 'GitHub repository')]
    title_html = escape(home['title']).replace('agents', '<em>agents</em>', 1)

    body = f"""{site_head('', 'index.html')}
<main id="main">
<header class="opening"><div class="wrap">
  <div class="opening-copy">
    <h1>{title_html}</h1>
    <p class="lead">{escape(home['lead'])}</p>
    <div class="actions"><a class="btn primary" href="ideas.html">Browse the nineteen ideas</a><a class="btn" href="guides.html">All 13 guides</a></div>
    <ul class="contents" role="list" aria-label="Contents">{contents}</ul>
    <p class="edition"><span class="num">Edition of {EDITION_DATE}.</span> {escape(home['basis_short'])} <a href="#attribution">Full attribution</a> is at the end of the page.</p>
  </div>
  <div class="pick">
    <h2 id="problems">Start with the problem you have</h2>
    <p>Each row names a situation and the guide that addresses it.</p>
    <ol role="list" aria-labelledby="problems">{pick}</ol>
  </div>
</div></header>

<section class="band" id="ideas" aria-labelledby="ideas-h"><div class="wrap">
  {band_head('The nineteen ideas', 'ideas-h', home['ideas_heading'], 'Swipe or scroll the row for all nineteen. Each opens its own page with what was said, how to apply it, when it is useful and its qualification.')}
  <div class="ideas-row" data-row="of" tabindex="0" role="region" aria-label="The nineteen ideas, in order">
    <ol class="ideas track" role="list">{row}</ol>
  </div>
  <p class="route">{more('ideas.html', f'All {counts["ideas"]} ideas as a grid')}</p>
</div></section>

<section class="band" id="skills" aria-labelledby="skills-h"><div class="wrap">
  {band_head('Portable skills', 'skills-h', home['skills_heading'], home['skills_description'])}
  <ul class="tiles cards skills" role="list">{skills}</ul>
</div></section>

<section class="band" id="guides" aria-labelledby="guides-h"><div class="wrap">
  {band_head('Implementation', 'guides-h', 'Thirteen implementation guides', 'Grouped by the source each was adapted from. Each guide gives a concrete method, fitting use cases and verification limits.')}
  <ul class="shelves" role="list">{shelves}</ul>
  <p class="route">{more('guides.html', f'All {counts["guides"]} guides')}</p>
</div></section>

<section class="band" id="reports" aria-labelledby="reports-h"><div class="wrap">
  {band_head('Evidence', 'reports-h', home['reports_heading'], home['reports_description'])}
  <ul class="shelves" role="list">{reports}</ul>
  <p class="route">{more('investigations.html', f'All {counts["reports"]} investigations')}</p>
</div></section>

<section class="band" id="frames" aria-labelledby="frames-h"><div class="wrap">
  {band_head('Frames', 'frames-h', home['frames_heading'], home['frames_description'])}
  <ol class="timestamps" role="list" aria-label="Frames by timestamp">{frames_line}</ol>
  <p class="route">{more('evidence.html', 'Open the gallery')}</p>
</div></section>

<section class="wrap closing" id="checked">
  <div><h2>What was checked</h2>{''.join(f'<p>{p_}</p>' for p_ in idx['checked'])}</div>
  <div id="attribution"><h2>Attribution</h2><p>{idx['attribution']}</p>
    <p>Frames are short excerpts from the video, reproduced for identification and commentary; they remain © Theo / their original owners. Full attribution in <a href="ATTRIBUTION.md">ATTRIBUTION.md</a>.</p>
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
            f'{marker(marker_label)}<h1>{escape(hub["h1"])}</h1>'
            f'<p class="lead">{inline(hub["lead"])}</p>{tail}</div></header>')


def ideas_index(idx, home):
    hub = home['hubs']['ideas']
    # The three evidential tiers of note 8. Each keeps the ideas in original
    # video order — the [nn] numbers are the video order and the idea pages'
    # numbering, so a tier is a selection of the sequence, not a renumbering.
    sections = ''
    for tier in hub['tiers']:
        ideas = [i for i in idx['ideas'] if i['tier'] == tier['key']]
        if not ideas:
            raise SystemExit(f'ideas_index(): tier {tier["key"]!r} is empty; '
                             'the extraction yields no ideas for it')
        tiles = ''.join(idea_tile(i) for i in ideas)
        sections += (f'<section class="tier" id="tier-{escape(tier["key"])}" '
                     f'aria-labelledby="tier-{escape(tier["key"])}-h"><div class="wrap">'
                     f'{marker(tier["label"])}'
                     f'<h2 id="tier-{escape(tier["key"])}-h">{escape(tier["heading"])}</h2>'
                     f'<p class="tier-lead">{escape(tier["lead"])}</p>'
                     f'<ol class="ideas" role="list">{tiles}</ol></div></section>')
    # The two files that carry what a tile cannot: speaker attribution, evidence
    # type and the caveats. They used to sit inside the lead, where they made a
    # reader read plumbing before content.
    tail = ('<p class="head-links"><a href="evidence/video-research.md">Detailed extraction</a> · '
            '<a href="evidence/video-tips.json">Structured ideas file</a></p>')
    body = (site_head('', 'ideas.html') +
            hub_head('Ideas', hub, tail) +
            sections +
            f'{hub_next(hub)}</main>' +
            site_foot('', escape(home['basis_short'])))
    (OUT / 'ideas.html').write_text(document(hub['title'], '', rewrite_refs(body), hub['description'], 'ideas.html'))


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
             f'{marker("The track")}<h2 id="track-h">Thirteen stages, in the order they were adapted</h2>'
             '<p class="tier-lead">Scroll the track. Each stage is one guide; the labels above the rail say which source it came from.</p></div>'
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
    # Guides per report: the union of the home-page shelves that name it.
    guides_from = {}
    for s in home['shelves']:
        guides_from.setdefault(s['investigation'], []).extend(s['guides'])

    studies = []
    for n, r in enumerate(idx['reports'], 1):
        rel = r['path']
        text = (REPO / rel).read_text()
        words = len(text.split())
        nguides = len(guides_from.get(rel, []))
        meta = (f'REPORT {n:02d} · {nguides} GUIDE{"S" if nguides != 1 else ""} CAME FROM THIS · '
                f'{words:,} WORD{"S" if words != 1 else ""}')
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
    # What every skill page carries, said once here rather than four times. The
    # instruction to adopt one rather than all four now opens the page, where a
    # reader meets it before choosing, and the adoption route closes it.
    adopt = ('<p class="route">Each title opens that skill\'s own page, which holds its raw '
             '<code>SKILL.md</code> exactly as shipped, both reference files and its directory on GitHub.</p>')
    hub = home['hubs']['skills']
    body = (site_head('', 'skills.html') +
            hub_head('Portable skills', hub) +
            '<section class="band" aria-label="The four skills"><div class="wrap">'
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
        title = ref.stem
        h1_at = next((i for i, l in enumerate(ref_lines) if l.startswith('# ')), None)
        if h1_at is not None:
            title = inline(ref_lines[h1_at][2:].strip())
            ref_lines = ref_lines[:h1_at] + ref_lines[h1_at + 1:]
        # The badge marks a document boundary; the rail's list keeps the plain words.
        label = f'<span class="kind">Reference</span> {title}'
        plain = f'Reference: {title}'
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
            f'<p><span class="n">{sk["fed_by"]}</span> {"idea" if sk["fed_by"] == 1 else "ideas"} feed it</p>'
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
            f'<a href="{prefix}skills.html">All four skills</a></p>'
            f'<span class="art" aria-hidden="true">{SKILLS[sk["name"]]}</span>'
            f'<h1>{title}</h1><p class="deck">{escape(description)}</p></header>'
            f'{toc_mobile}<article>{body_html}{refs_html}</article>'
            f'<p class="source-note"><a href="{GITHUB}/blob/HEAD/skills/{sk["name"]}/SKILL.md">SKILL.md on GitHub</a> · '
            f'<a href="{prefix}index.html">Home</a> · {SITE_NAME}, {EDITION_DATE}</p>'
            f'</div>{rail}</main>' +
            site_foot(prefix, escape(home['basis_short'])))
    out = OUT / sk['page']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(f'Skill: {title}', prefix, rewrite_refs(page, prefix),
                            summarise(description), sk['page']))


def idea_page(i, idx, home):
    """One idea, disclosed in full: what was said, how to apply it, when it is
    useful, its qualification, the moment in the video, and where it leads."""
    prefix = '../'
    tip = i['tip']
    ideas = idx['ideas']
    prev_i = ideas[i['n'] - 2] if i['n'] > 1 else None
    next_i = ideas[i['n']] if i['n'] < len(ideas) else None
    span = f'{mmss(tip["start_seconds"])}–{mmss(tip["end_seconds"])}'
    g = i['guide']
    sk = i['skill']

    def seq(a, cls, k):
        if not a:
            return ''
        return (f'<a class="{cls}" href="{escape(prefix + a["page"])}"><span class="k">{k}</span>'
                f'<span class="n">{a["n"]:02d}</span> {escape(a["idea"])}</a>')
    seq_links = seq(prev_i, 'prev', 'Previous idea') or f'<a class="prev" href="{prefix}ideas.html"><span class="k">Start</span>All nineteen ideas</a>'
    seq_links += seq(next_i, 'next', 'Next idea') or f'<a class="next" href="{prefix}guides.html"><span class="k">After the last idea</span>The thirteen guides</a>'

    rail_seq = seq_links.replace('class="prev"', '').replace('class="next"', '')
    article = (f'<h2 id="said">What was said</h2><p>{escape(tip["source_claim_paraphrase"])}</p>'
               f'<h2 id="apply">How to apply it</h2><p>{escape(tip["how_to_apply"])}</p>'
               f'<h2 id="useful">When it is useful</h2><p>{escape(tip["when_useful"])}</p>'
               f'<h2 id="qualification">Qualification</h2><p>{escape(tip["caveat"])}</p>')
    toc = ('<nav class="toc" aria-label="Sections of this page"><ol>'
           '<li><a href="#said">What was said</a></li><li><a href="#apply">How to apply it</a></li>'
           '<li><a href="#useful">When it is useful</a></li><li><a href="#qualification">Qualification</a></li></ol></nav>')
    rail = ('<aside class="rail" aria-label="Page tools">'
            f'<div><h2>On this page</h2>{toc}</div>'
            f'<div class="place"><h2>This idea</h2><p><span class="n">{i["n"]:02d}</span> of {len(ideas)} · <a href="{prefix}ideas.html">All nineteen</a></p>'
            f'<p class="use"><span class="badge">{escape(i["evidence"])}</span></p><p class="use">{escape(tip["speaker"])}</p></div>'
            f'<div class="watch"><h2>In the video</h2><p><a class="ts" href="{escape(i["url"])}">Watch at {escape(i["ts"])} <span aria-hidden="true">&#8599;</span></a></p><p class="use">Segment {span}</p></div>'
            f'<div class="leads"><h2>Where it leads</h2>'
            f'<p>{guide_chip(g["title"], g["path"])}</p>'
            f'<p><a class="chip" href="{escape(prefix + sk["href"])}">{escape(sk["title"])}</a></p></div>'
            f'<div class="neighbours"><h2>Sequence</h2>{rail_seq}</div>'
            f'<div class="source"><h2>Source</h2><a href="{prefix}evidence/video-tips.json">Structured extraction</a> · <a href="{prefix}evidence/video-research.html">Full notes</a></div>'
            '</aside>')
    page = (site_head(prefix, '') +
            f'<main id="main" class="wrap reader idea-page"><div class="col">'
            f'<header class="page-head"><p class="context"><span class="n">Idea {i["n"]:02d}</span> <span>of {len(ideas)}</span> '
            f'<span aria-hidden="true">·</span> <a href="{prefix}ideas.html">The nineteen ideas</a></p>'
            f'<span class="art" aria-hidden="true">{IDEAS[f"{i["n"]:02d}"]}</span>'
            f'<h1>{escape(i["idea"])}</h1></header>'
            f'<details class="toc-mobile"><summary>On this page</summary>{toc}</details>'
            f'<article>{article}</article>'
            f'<nav class="guide-seq" aria-label="Idea sequence">{seq_links}</nav>'
            f'<p class="source-note"><a href="{escape(i["url"])}">Watch at {escape(i["ts"])}</a> · <a href="{prefix}index.html">Home</a> · {SITE_NAME}, {EDITION_DATE}</p>'
            f'</div>{rail}</main>' +
            site_foot(prefix, escape(home['basis_short'])))
    out = OUT / i['page']
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(f'Idea {i["n"]:02d}: {i["idea"]}', prefix, rewrite_refs(page, prefix),
                            summarise(f'{i["idea"]}. {i["tip"]["when_useful"]}'), i['page']))


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
            '<li><a href="/ideas.html">The nineteen ideas</a></li>'
            '<li><a href="/guides.html">All 13 guides</a></li>'
            '<li><a href="/README.html">The handbook index</a></li>'
            '<li><a href="/evidence.html">The frame gallery</a></li></ul></main>' +
            site_foot('/', escape(home['basis_short'])))
    # 404 is served at any path, so it gets no canonical of its own.
    (OUT / '404.html').write_text(document('Page not found', '/', body,
                                           home['page_descriptions']['404.html']))


# ------------------------------------------------------------------- main
def main():
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

    idx = enrich(read_index(REPO / 'README.md'))
    home = json.loads(HOME.read_text())
    frames = json.loads((REPO / 'evidence/frame-manifest.json').read_text())

    for rel in RENDER_MD:
        reader_page(rel, idx, home, frames)
    gallery(frames, home, idx)
    not_found(home)
    for i in idx['ideas']:
        idea_page(i, idx, home)
    ideas_index(idx, home)
    guides_index(idx, home)
    investigations_index(idx, home)
    skills_index(idx, home)
    for sk in idx['skills']:
        skill_page(sk, idx, home)
    (OUT / 'index.html').write_text(landing(idx, home, frames))

    print(f'Rendered {len(RENDER_MD)} Markdown pages, {len(idx["ideas"])} idea pages, {len(idx["skills"])} skill pages, '
          f'the ideas, guides, skills and investigations indexes, the home page ({len(idx["guides"])} guides, '
          f'{len(idx["reports"])} investigations, {len(idx["skills"])} skills, {len(idx["ideas"])} ideas, '
          f'{len(frames)} frames), the gallery and 404.html into public/.')


if __name__ == '__main__':
    main()
