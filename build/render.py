#!/usr/bin/env python3
"""Render the public handbook site into public/.

Reads only the editable Markdown, assets and JSON in this repository (never the
generated public/ directory) and writes public/ from scratch, so rerunning is
idempotent and cannot recursively consume its own output.

Inputs:
  README.md and the other Markdown pages     -> reader pages (one shared template)
  README.md tables and lists + build/home.json -> the landing-page map (index.html)
  evidence/frame-manifest.json               -> the frame gallery (evidence.html)
  build/assets/handbook.css                  -> public/assets/handbook.css
  screenshots/, skills/, examples/, evidence/*.json -> copied verbatim

Requires Markdown==3.10.3 (build/requirements.txt). No network calls.

Usage:
    python3 build/render.py            # from anywhere; paths are script-relative
"""
from pathlib import Path
from html import escape
import json
import re
import shutil
import markdown

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'public'
ASSETS = REPO / 'build/assets'
HOME = REPO / 'build/home.json'

GITHUB = 'https://github.com/desland01/agent-engineering-handbook'
EDITION_DATE = 'September 9, 2026'

# Directories and files that are renderer *inputs*. public/, build/ and any
# virtualenv are never read as content sources.
COPY_DIRS = ['screenshots', 'skills', 'examples/recurring-rule']
COPY_FILES = [
    'evidence/frame-manifest.json',
    'evidence/video-tips.json',
    'evidence/melee-verifier-comparison.json',
]
# Markdown rendered to HTML (the .md source is copied alongside each page).
RENDER_MD = [
    'README.md', 'adoption.md', 'prompts.md', 'validation.md',
    'CONTRIBUTING.md', 'ATTRIBUTION.md', 'DESIGN.md', 'INTERACTIONS.md',
    'github-inspection.md', 'matt-pocock-inspection.md', 'boris-cherny-inspection.md',
    'evidence/video-research.md', 'examples/recurring-rule/README.md',
] + sorted(f'guides/{p.name}' for p in (REPO / 'guides').glob('*.md'))

NAV_ITEMS = [
    ('index.html', 'Map'),
    ('README.html', 'Handbook'),
    ('prompts.html', 'Prompts'),
    ('evidence.html', 'Frames'),
    ('github-inspection.html', 'Theo'),
    ('matt-pocock-inspection.html', 'Matt'),
    ('boris-cherny-inspection.html', 'Boris'),
    ('adoption.html', 'Adoption'),
    ('validation.html', 'Validation'),
]

# Where a reader page sits on the map: (context line, map anchor).
CONTEXT = {
    'github-inspection.md': ('One of three repository investigations', '#reports'),
    'matt-pocock-inspection.md': ('One of three repository investigations', '#reports'),
    'boris-cherny-inspection.md': ('One of three repository investigations', '#reports'),
    'evidence/video-research.md': ('Detailed extraction behind the nineteen ideas', '#ideas'),
    'examples/recurring-rule/README.md': ('Runnable companion to guide 01', '#guides'),
    'adoption.md': ('Adopting a guide or portable skill', '#skills'),
    'prompts.md': ('Task prompts for the guides', '#guides'),
    'DESIGN.md': ('How this site is designed', ''),
    'INTERACTIONS.md': ('How this site behaves', ''),
}

MD_EXTENSIONS = ['markdown.extensions.tables', 'markdown.extensions.fenced_code',
                 'markdown.extensions.sane_lists', 'markdown.extensions.toc']


# ------------------------------------------------------------------ helpers
def md_html(text):
    return markdown.markdown(text, extensions=MD_EXTENSIONS)


def inline(text):
    """Render one paragraph of Markdown without the wrapping <p>."""
    html = md_html(text).strip()
    if html.startswith('<p>') and html.endswith('</p>') and html.count('<p>') == 1:
        html = html[3:-4]
    return html


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


def top_bar(prefix):
    return ('<div class="wrap top">'
            f'<a class="brand" href="{prefix}index.html">Agent Engineering Handbook</a>'
            f'<a class="repo" href="{GITHUB}">github.com/desland01/agent-engineering-handbook</a>'
            '</div>')


def site_nav(out_path):
    prefix = depth_prefix(out_path)
    current = out_path.relative_to(OUT).as_posix()
    items = []
    for target, label in NAV_ITEMS:
        aria = ' aria-current="page"' if target == current else ''
        items.append(f'<a href="{escape(prefix + target)}"{aria}>{escape(label)}</a>')
    return '<nav class="wrap site-nav" aria-label="Handbook sections">' + ''.join(items) + '</nav>'


def site_foot(prefix, basis_short):
    links = [(f'{prefix}index.html', 'Map'), (f'{prefix}README.html', 'Handbook index'),
             (f'{prefix}ATTRIBUTION.html', 'Attribution'), (f'{prefix}CONTRIBUTING.html', 'Contributing'),
             (GITHUB, 'GitHub repository')]
    return ('<footer class="wrap site-foot">'
            f'<p>{basis_short} Frames are short excerpts from the video and remain © Theo / their original owners.</p>'
            '<ul>' + ''.join(f'<li><a href="{escape(u)}">{escape(t)}</a></li>' for u, t in links) + '</ul>'
            '</footer>')


def document(title, css_href, body, head_extra=''):
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="color-scheme" content="dark">'
            f'<link rel="icon" href="data:,"><title>{escape(title)} · Agent Engineering Handbook</title>'
            f'<link rel="stylesheet" href="{css_href}">{head_extra}</head>'
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


def read_index(readme):
    """The handbook's own index: problems, guides, reports, skills, ideas, checks, attribution."""
    text = readme.read_text()
    idx = {}

    idx['problems'] = [(row[0], inline(row[1])) for row in table_rows(section(text, 'Start with the problem you have'))]

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


def landing(idx, home, frames):
    guide_by_n = {g['n']: g for g in idx['guides']}
    counts = {'guides': len(idx['guides']), 'reports': len(idx['reports']),
              'skills': len(idx['skills']), 'ideas': len(idx['ideas']), 'frames': len(frames)}
    shelf_guides = [n for s in home['shelves'] for n in s['guides']]
    if sorted(shelf_guides) != sorted(guide_by_n):
        raise SystemExit(f'build/home.json shelves list {shelf_guides}; README lists {sorted(guide_by_n)}')

    contents = ''.join(
        f'<li><a href="#{anchor}"><span>{counts[key]}</span> {label}</a></li>'
        for key, label, anchor in [('guides', 'guides', 'guides'), ('reports', 'investigations', 'reports'),
                                   ('skills', 'skills', 'skills'), ('ideas', 'video ideas', 'ideas'),
                                   ('frames', 'frames', 'frames')])

    pick = ''.join(f'<li><span class="q">{escape(q)}</span><span class="a">{a}</span></li>'
                   for q, a in idx['problems'])

    report_by_path = {r['path']: r for r in idx['reports']}
    shelves = ''
    for s in home['shelves']:
        tiles = ''.join(
            f'<li class="tile guide"><span class="n" aria-hidden="true">{g["n"]}</span>'
            f'<a class="t" href="{escape(g["path"])}"><span class="sr-only">Guide {g["n"]}: </span>{escape(g["title"])}</a>'
            f'<p class="when">{escape(home["use_when"][g["n"]])}</p></li>'
            for g in (guide_by_n[n] for n in s['guides']))
        report = report_by_path[s['investigation']]
        shelves += (f'<section class="shelf" id="{escape(s["id"])}" aria-labelledby="{escape(s["id"])}-h"><div class="wrap">'
                    f'<div class="shelf-head"><h2 id="{escape(s["id"])}-h">{escape(s["title"])}</h2>'
                    f'<p>{inline(s["description"])} Investigation: <a href="{escape(report["path"])}">{escape(report["title"])}</a>.</p></div>'
                    f'<ul class="tiles" role="list">{tiles}</ul></div></section>')

    reports = ''.join(
        f'<li class="tile report"><a class="t" href="{escape(r["path"])}">{escape(r["title"])}</a>'
        f'<p class="when">{escape(r["blurb"])}</p><span class="dir">{escape(r["path"])}</span></li>'
        for r in idx['reports'])

    skills = ''.join(
        f'<li class="tile skill"><a class="t" href="{escape(sk["path"])}">{escape(sk["title"])}</a>'
        f'<p class="when">{escape(sk["use"])}</p>'
        f'<span class="dir"><a href="{GITHUB}/tree/HEAD/{escape(sk["path"].rsplit("/", 1)[0])}">{escape(sk["path"].rsplit("/", 1)[0])}/</a></span></li>'
        for sk in idx['skills'])

    ideas = ''.join(
        f'<li><span class="t"><a href="{escape(i["url"])}">{escape(i["ts"])}</a></span>'
        f'<p class="idea">{escape(i["idea"])}</p>'
        f'<span class="to"><a href="{escape(i["guide_path"])}">{escape(i["guide_label"])}</a> — {escape(guide_by_n[i["guide_path"].split("/")[1][:2]]["title"])}</span></li>'
        for i in idx['ideas'])

    frame_tiles = ''.join(
        f'<figure><a class="shot" href="evidence.html#frame-{f["seconds"]}">'
        f'<img src="screenshots/{escape(f["file"])}" width="1920" height="1080" loading="lazy" alt="{escape(frame_alt(f))}"></a>'
        f'<figcaption><span class="t">{escape(f["timestamp"])}</span> {escape(f["title"])}</figcaption></figure>'
        for f in frames)

    checked = ''.join(f'<p>{p}</p>' for p in idx['checked'])
    closing_links = [('README.md', 'Handbook index'), ('adoption.md', 'Adoption'), ('prompts.md', 'Task prompts'),
                     ('validation.md', 'Validation'), ('examples/recurring-rule/README.md', 'Runnable lint example'),
                     ('CONTRIBUTING.md', 'Contributing'), (GITHUB, 'GitHub repository')]

    body = f'''{top_bar('')}
<main id="main">
<header class="wrap opening">
  <div>
    <h1>{escape(home['title'])}</h1>
    <p class="lead">{escape(home['lead'])}</p>
    <ul class="contents" role="list" aria-label="Contents">{contents}</ul>
    <p class="basis">{escape(home['basis_short'])} <a href="#attribution">Full attribution</a> is at the end of the page.</p>
  </div>
  <div class="pick">
    <h2 id="problems">Pick by the problem you have</h2>
    <ol role="list" aria-labelledby="problems">{pick}</ol>
  </div>
</header>

<div id="guides">{shelves}</div>

<section class="shelf" id="reports" aria-labelledby="reports-h"><div class="wrap">
  <div class="shelf-head"><h2 id="reports-h">{escape(home['reports_heading'])}</h2><p>{inline(home['reports_description'])}</p></div>
  <ul class="tiles" role="list">{reports}</ul>
</div></section>

<section class="shelf" id="skills" aria-labelledby="skills-h"><div class="wrap">
  <div class="shelf-head"><h2 id="skills-h">{escape(home['skills_heading'])}</h2><p>{inline(home['skills_description'])}</p></div>
  <ul class="tiles" role="list">{skills}</ul>
</div></section>

<section class="shelf" id="ideas" aria-labelledby="ideas-h"><div class="wrap">
  <div class="shelf-head"><h2 id="ideas-h">{escape(home['ideas_heading'])}</h2><p>{inline(home['ideas_description'])}</p></div>
  <ol class="ideas" role="list">{ideas}</ol>
</div></section>

<section class="shelf" id="frames" aria-labelledby="frames-h"><div class="wrap">
  <div class="shelf-head"><h2 id="frames-h">{escape(home['frames_heading'])}</h2><p>{inline(home['frames_description'])}</p></div>
  <div class="grid-frames">{frame_tiles}</div>
</div></section>

<section class="wrap closing" id="checked">
  <div><h2>What was checked</h2>{checked}</div>
  <div id="attribution"><h2>Attribution</h2><p>{idx['attribution']}</p>
    <p>Frames are short excerpts from the video, reproduced for identification and commentary; they remain © Theo / their original owners. Full attribution in <a href="ATTRIBUTION.md">ATTRIBUTION.md</a>.</p>
    <ul>{''.join(f'<li><a href="{escape(u)}">{escape(t)}</a></li>' for u, t in closing_links)}</ul>
  </div>
</section>
</main>
'''
    return document(home['title'], 'assets/handbook.css', rewrite_refs(body))


# ------------------------------------------------------------ reader pages
def reader_page(rel, idx, home):
    path = REPO / rel
    out = (OUT / rel).with_suffix('.html')
    prefix = depth_prefix(out)
    text = path.read_text()
    if text.startswith('---\n'):
        text = text.split('---', 2)[2].lstrip()
    title = next((s.lstrip('# ') for s in text.splitlines() if s.startswith('# ')), path.stem)
    body = rewrite_tables(rewrite_refs(md_html(text)))

    context = ''
    seq = ''
    guides = idx['guides']
    pos = next((i for i, g in enumerate(guides) if g['path'] == rel), None)
    if pos is not None:
        g = guides[pos]
        shelf = next(s for s in home['shelves'] if g['n'] in s['guides'])
        context = (f'<p class="context"><span class="n">Guide {g["n"]} of {len(guides)}</span> '
                   f'<a href="{prefix}index.html#{escape(shelf["id"])}">{escape(shelf["title"])}</a></p>')
        prev_g = guides[pos - 1] if pos > 0 else None
        next_g = guides[pos + 1] if pos + 1 < len(guides) else None
        links = ''
        if prev_g:
            links += (f'<a class="prev" href="{escape(prefix + prev_g["path"][:-3] + ".html")}"><span class="k">Previous guide</span>'
                      f'<span class="n">{prev_g["n"]}</span> {escape(prev_g["title"])}</a>')
        else:
            links += f'<a class="prev" href="{prefix}index.html#guides"><span class="k">Start of the guides</span>All 13 guides on the map</a>'
        if next_g:
            links += (f'<a class="next" href="{escape(prefix + next_g["path"][:-3] + ".html")}"><span class="k">Next guide</span>'
                      f'<span class="n">{next_g["n"]}</span> {escape(next_g["title"])}</a>')
        else:
            links += f'<a class="next" href="{prefix}index.html#reports"><span class="k">After the last guide</span>The three repository investigations</a>'
        seq = f'<nav class="guide-seq" aria-label="Guide sequence">{links}</nav>'
    elif rel in CONTEXT:
        label, anchor = CONTEXT[rel]
        context = f'<p class="context"><a href="{prefix}index.html{anchor}">{escape(label)}</a></p>'

    md_name = path.name
    note = (f'<p class="source-note"><a href="{escape(md_name)}">Editable Markdown source</a> · '
            f'<a href="{prefix}index.html">Back to the map</a> · Agent Engineering Handbook, {EDITION_DATE}</p>')
    page = (top_bar(prefix) + site_nav(out) +
            f'<main id="main" class="wrap reader">{context}<article>{body}</article>{seq}{note}</main>' +
            site_foot(prefix, escape(home['basis_short'])))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(title, f'{prefix}assets/handbook.css', page))
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
    body = (top_bar('') + site_nav(out) +
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
    out.write_text(document('Video evidence', 'assets/handbook.css', body))


# -------------------------------------------------------------- not found
def not_found(home):
    # Served at any path, so its links are root-absolute.
    body = (top_bar('/') +
            '<main id="main" class="wrap notfound"><h1>That page is not in the handbook</h1>'
            '<p>The address may have been mistyped, or the page may have moved when the handbook was regenerated. '
            'Everything published here is reachable from the map.</p>'
            '<ul><li><a href="/index.html">The map: all guides, investigations, skills, ideas and frames</a></li>'
            '<li><a href="/index.html#problems">Pick by the problem you have</a></li>'
            '<li><a href="/README.html">The handbook index</a></li>'
            '<li><a href="/evidence.html">The frame gallery</a></li></ul></main>' +
            site_foot('/', escape(home['basis_short'])))
    (OUT / '404.html').write_text(document('Page not found', '/assets/handbook.css', body))


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

    idx = read_index(REPO / 'README.md')
    home = json.loads(HOME.read_text())
    frames = json.loads((REPO / 'evidence/frame-manifest.json').read_text())

    for rel in RENDER_MD:
        reader_page(rel, idx, home)
    gallery(frames, home, idx)
    not_found(home)
    (OUT / 'index.html').write_text(landing(idx, home, frames))

    print(f'Rendered {len(RENDER_MD)} Markdown pages, the map ({len(idx["guides"])} guides, '
          f'{len(idx["reports"])} investigations, {len(idx["skills"])} skills, {len(idx["ideas"])} ideas, '
          f'{len(frames)} frames), the gallery and 404.html into public/.')


if __name__ == '__main__':
    main()
