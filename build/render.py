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
OUT = REPO / 'public'
ASSETS = REPO / 'build/assets'
HOME = REPO / 'build/home.json'

GITHUB = 'https://github.com/desland01/agent-engineering-handbook'
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
    ('index.html#guides', 'Guides'),
    ('index.html#reports', 'Investigations'),
    ('index.html#skills', 'Skills'),
    ('evidence.html', 'Frames'),
]
MENU_GROUPS = [
    [('index.html', 'Map', True)] + [(t, l, True) for t, l in PRIMARY_NAV],
    [('README.html', 'Handbook index', False), ('prompts.html', 'Task prompts', False),
     ('adoption.html', 'Adopting a skill', False), ('validation.html', 'Validation', False)],
    [('github-inspection.html', 'Theo: T3 Code and Melee', False),
     ('matt-pocock-inspection.html', 'Matt Pocock: Course Video Manager', False),
     ('boris-cherny-inspection.html', 'Boris Cherny: public work', False)],
    [('ATTRIBUTION.html', 'Attribution', False), ('CONTRIBUTING.html', 'Contributing', False),
     (GITHUB, 'GitHub repository', False)],
]

# Where a non-guide reader page sits on the map: (context line, map anchor).
CONTEXT = {
    'README.md': ('The handbook index', '#guides'),
    'github-inspection.md': ('One of three repository investigations', '#reports'),
    'matt-pocock-inspection.md': ('One of three repository investigations', '#reports'),
    'boris-cherny-inspection.md': ('One of three repository investigations', '#reports'),
    'evidence/video-research.md': ('Detailed extraction behind the nineteen ideas', '#ideas'),
    'examples/recurring-rule/README.md': ('Runnable companion to guide 01', '#guides'),
    'adoption.md': ('Adopting a guide or portable skill', '#skills'),
    'prompts.md': ('Task prompts for the guides', '#guides'),
    'validation.md': ('What was checked, and what was not', '#checked'),
    'ATTRIBUTION.md': ('Sources and attribution', '#attribution'),
    'CONTRIBUTING.md': ('How the handbook is built and updated', '#attribution'),
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
    links = [(f'{prefix}index.html', 'Map'), (f'{prefix}README.html', 'Handbook index'),
             (f'{prefix}ATTRIBUTION.html', 'Attribution'), (f'{prefix}CONTRIBUTING.html', 'Contributing'),
             (GITHUB, 'GitHub repository')]
    return ('<footer class="site-foot"><div class="wrap">'
            f'<p>{basis_short} Frames are short excerpts from the video and remain © Theo / their original owners.</p>'
            '<ul>' + ''.join(f'<li><a href="{escape(u)}">{escape(t)}</a></li>' for u, t in links) + '</ul>'
            '</div></footer>')


def document(title, prefix, body):
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="color-scheme" content="dark">'
            f'<link rel="icon" href="data:,"><title>{escape(title)} · {SITE_NAME}</title>'
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


EVIDENCE_LABEL = {
    'sponsor-ad-framing (sponsor performance claims unverified)': 'Sponsor segment',
    'theo-anecdote': 'Theo, anecdote',
    'theo-opinion': 'Theo, opinion',
    'theo-practice': 'Theo, practice',
    'theo-directive': 'Theo, directive',
    'quoted-post-via-theo': "Boris's post, read by Theo",
}


def marker(label):
    """A section marker: a mono label in a bordered pill with a rule running from it."""
    return f'<span class="marker"><span class="pill">{escape(label)}</span></span>'


def landing(idx, home, frames):
    """The landing page, in the premium tech design language.

    One accent, hairline structure, monospace for every secondary line, and the
    39 authored drawings carrying the illustration. No hub-and-spoke diagram and
    no video stills: the twelve frames appear here as file cards that open the
    gallery, where the full-size images live.
    """
    guide_by_n = {g['n']: g for g in idx['guides']}
    counts = {'guides': len(idx['guides']), 'reports': len(idx['reports']),
              'skills': len(idx['skills']), 'ideas': len(idx['ideas']), 'frames': len(frames)}
    shelf_guides = [n for s in home['shelves'] for n in s['guides']]
    if sorted(shelf_guides) != sorted(guide_by_n):
        raise SystemExit(f'build/home.json shelves list {shelf_guides}; README lists {sorted(guide_by_n)}')

    tips = json.loads((REPO / 'evidence/video-tips.json').read_text())
    tip_by_start = {t['start_seconds']: t for t in tips}
    skill_by_name = {sk['path'].split('/')[1]: sk for sk in idx['skills']}
    for sk in idx['skills']:
        sk['name'] = sk['path'].split('/')[1]
        sk['dir'] = sk['path'].rsplit('/', 1)[0]
        sk['fed_by'] = 0
    for i in idx['ideas']:
        seconds = int(re.search(r't=(\d+)s', i['url']).group(1))
        tip = tip_by_start[seconds]
        i['tip'] = tip
        i['skill'] = skill_by_name[tip['suggested_skill']]
        i['skill']['fed_by'] += 1
        i['evidence'] = EVIDENCE_LABEL[tip['evidence_type']]

    # Contents: mono badges. The markup shape is what build/check.py counts.
    contents = ''.join(
        f'<li><a href="#{anchor}"><span>{counts[key]}</span> {label}</a></li>'
        for key, label, anchor in [('ideas', 'ideas', 'ideas'), ('guides', 'guides', 'guides'),
                                   ('skills', 'skills', 'skills'), ('reports', 'investigations', 'reports'),
                                   ('frames', 'frames', 'frames')])

    pick = ''.join(
        f'<li><span class="q">{escape(q)}</span>'
        f'<span class="a">{"".join(guide_chip(label, path) for label, path in links)}</span></li>'
        for q, links in idx['problems'])

    # The nineteen ideas: icon tiles on dashed guides, each with its [nn] marker.
    ideas = ''.join(
        f'<li><article class="tile idea" id="idea-{n:02d}">'
        f'<span class="ix" aria-hidden="true">[{n:02d}]</span>'
        f'<span class="art" aria-hidden="true">{IDEAS[f"{n:02d}"]}</span>'
        f'<h3>{escape(i["idea"])}</h3>'
        f'<p class="who">{escape(i["tip"]["speaker"])}</p>'
        f'<p class="when">{escape(i["tip"]["when_useful"])}</p>'
        f'<p class="meta"><a class="ts" href="{escape(i["url"])}">Watch at {escape(i["ts"])} <span aria-hidden="true">&#8599;</span></a>'
        f'<span class="badge">{escape(i["evidence"])}</span></p>'
        f'<span class="to">{guide_chip(guide_by_n[GUIDE_N.search(i["guide_path"]).group(1)]["title"], i["guide_path"])}'
        f'<a class="chip" href="{escape(i["skill"]["path"])}">{escape(i["skill"]["title"])}</a></span>'
        f'</article></li>'
        for n, i in enumerate(idx['ideas'], 1))

    # Four skills: a hairline grid, each cell led by its drawing.
    skills = ''.join(
        f'<li class="tile skill"><span class="art" aria-hidden="true">{SKILLS[sk["name"]]}</span>'
        f'<a class="t" href="{escape(sk["path"])}">{escape(sk["title"])}</a>'
        f'<p class="when">{escape(sk["use"])}</p>'
        f'<p class="fed"><span class="n">{sk["fed_by"]}</span> {"idea" if sk["fed_by"] == 1 else "ideas"} feed it</p>'
        f'<span class="dir"><a href="{GITHUB}/tree/HEAD/{escape(sk["dir"])}">{escape(sk["dir"])}/</a></span></li>'
        for sk in idx['skills'])

    # Thirteen guides: icon tiles grouped under mono shelf labels.
    report_by_path = {r['path']: r for r in idx['reports']}
    shelves = ''
    for s_ in home['shelves']:
        ns = s_['guides']
        span = f'Guide {ns[0]}' if len(ns) == 1 else f'Guides {ns[0]}–{ns[-1]}'
        tiles = ''.join(
            f'<li class="tile guide"><span class="glyph-box" aria-hidden="true">{GUIDES[g["n"]]}</span>'
            f'<div><a class="t" href="{escape(g["path"])}"><span class="n" aria-hidden="true">{g["n"]}</span>'
            f'<span class="sr-only">Guide {g["n"]}: </span>{escape(g["title"])}</a>'
            f'<p class="when">{escape(home["use_when"][g["n"]])}</p></div></li>'
            for g in (guide_by_n[n] for n in ns))
        report = report_by_path[s_['investigation']]
        shelves += (f'<section class="shelf" id="{escape(s_["id"])}" aria-labelledby="{escape(s_["id"])}-h"><div class="wrap">'
                    f'<div class="shelf-head"><h3 id="{escape(s_["id"])}-h">+ {escape(s_["title"])}</h3>'
                    f'<p>{inline(s_["description"])} Investigation: <a href="{escape(report["path"])}">{escape(report["title"])}</a>.</p>'
                    f'<span class="count">{span}</span></div>'
                    f'<ul class="tiles guides" role="list">{tiles}</ul></div></section>')

    reports = ''.join(
        f'<li class="tile report"><span class="art" aria-hidden="true">{INVESTIGATIONS[r["path"]]}</span>'
        f'<a class="t" href="{escape(r["path"])}">{escape(r["title"])}</a>'
        f'<p class="when">{escape(r["blurb"])}</p><span class="dir">{escape(r["path"])}</span></li>'
        for r in idx['reports'])

    # Twelve frames as file cards. The images themselves stay in the gallery.
    frame_tiles = ''.join(
        f'<figure><a href="evidence.html#frame-{f["seconds"]}">'
        f'<span class="t">{escape(f["timestamp"])}</span>'
        f'<figcaption>{escape(f["title"])}</figcaption>'
        f'<span class="open">open <span aria-hidden="true">&#8594;</span></span></a></figure>'
        for f in frames)

    checked = ''.join(f'<p>{p}</p>' for p in idx['checked'])
    closing_links = [('README.md', 'Handbook index'), ('adoption.md', 'Adopting a skill'), ('prompts.md', 'Task prompts'),
                     ('validation.md', 'Validation'), ('examples/recurring-rule/README.md', 'Runnable lint example'),
                     ('CONTRIBUTING.md', 'Contributing'), (GITHUB, 'GitHub repository')]

    title_html = escape(home['title']).replace('agents', '<em>agents</em>', 1)

    body = f'''{site_head('', 'index.html')}
<main id="main">
<header class="opening"><div class="wrap">
  <div class="opening-copy">
    <h1>{title_html}</h1>
    <p class="lead">{escape(home['lead'])}</p>
    <div class="actions"><a class="btn primary" href="#ideas">Browse the nineteen ideas</a><a class="btn" href="#guides">All 13 guides</a></div>
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
  <div class="band-head">{marker('The nineteen ideas')}
    <h2 id="ideas-h">{escape(home['ideas_heading'])}</h2><p>{inline(home['ideas_description'])}</p></div>
  <ol class="ideas" role="list">{ideas}</ol>
</div></section>

<section class="band" id="skills" aria-labelledby="skills-h"><div class="wrap">
  <div class="band-head">{marker('Portable skills')}
    <h2 id="skills-h">{escape(home['skills_heading'])}</h2><p>{inline(home['skills_description'])}</p></div>
  <ul class="tiles cards skills" role="list">{skills}</ul>
</div></section>

<section class="band" id="guides" aria-labelledby="guides-h"><div class="wrap">
  <div class="band-head">{marker('Implementation')}
    <h2 id="guides-h">All 13 implementation guides</h2>
    <p>Each guide gives a concrete method, fitting use cases and verification limits, grouped by the source it was adapted from.</p></div>
</div>{shelves}</section>

<section class="band" id="reports" aria-labelledby="reports-h"><div class="wrap">
  <div class="band-head">{marker('Evidence')}
    <h2 id="reports-h">{escape(home['reports_heading'])}</h2><p>{inline(home['reports_description'])}</p></div>
  <ul class="tiles cards" role="list">{reports}</ul>
</div></section>

<section class="band" id="frames" aria-labelledby="frames-h"><div class="wrap">
  <div class="band-head">{marker('Frames')}
    <h2 id="frames-h">{escape(home['frames_heading'])}</h2><p>{inline(home['frames_description'])}</p></div>
  <div class="grid-frames">{frame_tiles}</div>
</div></section>

<section class="wrap closing" id="checked">
  <div><h2>What was checked</h2>{checked}</div>
  <div id="attribution"><h2>Attribution</h2><p>{idx['attribution']}</p>
    <p>Frames are short excerpts from the video, reproduced for identification and commentary; they remain © Theo / their original owners. Full attribution in <a href="ATTRIBUTION.md">ATTRIBUTION.md</a>.</p>
    <ul>{''.join(f'<li><a class="chip" href="{escape(u)}">{escape(t)}</a></li>' for u, t in closing_links)}</ul>
  </div>
</section>
</main>
{site_foot('', escape(home['basis_short']))}'''
    return document(home['title'], '', rewrite_refs(body))


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
    if pos is not None:
        g = guides[pos]
        title_html = escape(g['title'])
        shelf = next(s for s in home['shelves'] if g['n'] in s['guides'])
        shelf_href = f'{prefix}index.html#{escape(shelf["id"])}'
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
            seq_links += f'<a class="prev" href="{prefix}index.html#guides"><span class="k">Start of the guides</span>All 13 guides on the map</a>'
            rail_links += f'<a href="{prefix}index.html#guides"><span class="k">Previous</span>All 13 guides on the map</a>'
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
        if rel in CONTEXT:
            label, anchor = CONTEXT[rel]
            context = f'<p class="context"><a href="{prefix}index.html{anchor}">{escape(label)}</a></p>'
            place = f'<div class="place"><h2>On the map</h2><p><a href="{prefix}index.html{anchor}">{escape(label)}</a></p></div>'

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
            f'<a href="{prefix}index.html">Back to the map</a> · {SITE_NAME}, {EDITION_DATE}</p>')
    page = (site_head(prefix, current) +
            f'<main id="main" class="wrap reader"><div class="col">'
            f'<header class="page-head">{context}<h1>{title_html}</h1></header>'
            f'{toc_mobile}<article>{body}</article>{evidence_mobile}{seq}{note}</div>{rail}</main>' +
            site_foot(prefix, escape(home['basis_short'])))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(unescape(strip_tags(title_html)), prefix, page))
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
    body = (site_head('', 'evidence.html') +
            '<main id="main" class="wrap">'
            '<header class="gallery-head"><h1>The video, with visible evidence</h1>'
            f'<p class="lead">{len(frames)} frames extracted with ffmpeg and inspected at full resolution. '
            'Each caption distinguishes what is visible from what Theo only describes; a post on screen is not a live demonstration.</p>'
            '<p class="links"><a href="evidence/frame-manifest.json">Extraction commands and SHA-256 hashes</a> · '
            '<a href="evidence/video-research.html">Full extraction notes</a> · '
            '<a href="index.html#ideas">The nineteen ideas on the map</a></p>'
            f'<ol class="strip" role="list" aria-label="Jump to a frame">{strip}</ol></header>'
            f'<div class="gallery">{sections}</div></main>' +
            site_foot('', escape(home['basis_short'])))
    out.write_text(document('Video evidence', '', body))


# -------------------------------------------------------------- not found
def not_found(home):
    # Served at any path, so its links are root-absolute.
    body = (site_head('/') +
            '<main id="main" class="wrap notfound"><h1>That page is not in the handbook</h1>'
            '<p>The address may have been mistyped, or the page may have moved when the handbook was regenerated. '
            'Everything published here is reachable from the map.</p>'
            '<ul><li><a href="/index.html">The map: all guides, investigations, skills, ideas and frames</a></li>'
            '<li><a href="/index.html#problems">Start with the problem you have</a></li>'
            '<li><a href="/README.html">The handbook index</a></li>'
            '<li><a href="/evidence.html">The frame gallery</a></li></ul></main>' +
            site_foot('/', escape(home['basis_short'])))
    (OUT / '404.html').write_text(document('Page not found', '/', body))


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

    idx = read_index(REPO / 'README.md')
    home = json.loads(HOME.read_text())
    frames = json.loads((REPO / 'evidence/frame-manifest.json').read_text())

    for rel in RENDER_MD:
        reader_page(rel, idx, home, frames)
    gallery(frames, home, idx)
    not_found(home)
    (OUT / 'index.html').write_text(landing(idx, home, frames))

    print(f'Rendered {len(RENDER_MD)} Markdown pages, the map ({len(idx["guides"])} guides, '
          f'{len(idx["reports"])} investigations, {len(idx["skills"])} skills, {len(idx["ideas"])} ideas, '
          f'{len(frames)} frames), the gallery and 404.html into public/.')


if __name__ == '__main__':
    main()
