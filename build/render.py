#!/usr/bin/env python3
"""Render the public handbook site into public/.

Reads only the editable Markdown, assets and JSON in this repository (never the
generated public/ directory) and writes public/ from scratch, so rerunning is
idempotent and cannot recursively consume its own output.

Requires Markdown==3.10.3 (build/requirements.txt). No network calls.

Usage:
    python3 build/render.py            # from anywhere; paths are script-relative
    PYTHONPATH=inputs/python-libs python3 output/repo/build/render.py
"""
from pathlib import Path
from html import escape
import json
import re
import shutil
import markdown

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'public'
SOURCE_HTML = REPO / 'build/workflows-source.html'

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
    'CONTRIBUTING.md', 'ATTRIBUTION.md',
    'github-inspection.md', 'matt-pocock-inspection.md', 'boris-cherny-inspection.md',
    'evidence/video-research.md', 'examples/recurring-rule/README.md',
] + sorted(f'guides/{p.name}' for p in (REPO / 'guides').glob('*.md'))

source = SOURCE_HTML.read_text()
css = re.search(r'<style>(.*?)</style>', source, re.S).group(1)
css += '''
  a { text-decoration: underline; text-underline-offset: 3px; }
  .site-nav { display:flex; flex-wrap:wrap; gap:10px 20px; margin:0 0 32px; padding:0 0 18px; border-bottom:1px solid var(--border); font-size:.94rem; }
  .site-nav a { color:var(--fg); }
  p, li, td, th { overflow-wrap:anywhere; }
  h3 { margin:28px 0 12px; }
  .phase h3 { margin:0; }
  h4 { margin:22px 0 8px; }
  li { margin:6px 0; }
  blockquote { margin:20px 0; padding:12px 20px; border-left:3px solid var(--primary); background:var(--card); }
  code { font-family:var(--font-mono); font-size:.87em; background:var(--muted); padding:2px 5px; border-radius:4px; overflow-wrap:anywhere; }
  pre { padding:18px; border:1px solid var(--border); border-radius:8px; background:var(--card); overflow-x:auto; max-width:100%; }
  pre code { background:none; padding:0; overflow-wrap:normal; }
  .table-scroll { max-width:100%; overflow-x:auto; margin:20px 0 28px; }
  table { width:100%; border-collapse:collapse; font-size:.92rem; min-width:580px; }
  th,td { padding:12px; border:1px solid var(--border); text-align:left; vertical-align:top; }
  th { background:var(--muted); }
  figure { margin:24px 0 40px; }
  figure img { display:block; width:100%; height:auto; border:1px solid var(--border); border-radius:8px; }
  figcaption { margin-top:12px; color:var(--muted-fg); }
  .source-note { margin-top:48px; padding-top:18px; border-top:1px solid var(--border); color:var(--muted-fg); font-size:.9rem; }
  .quick-start { padding:20px 24px; border:1px solid var(--border); border-radius:8px; margin:24px 0; }
  .quick-start ul { margin-bottom:0; }
  @media(max-width:600px) {
    main { padding:28px 18px 56px; }
    h1 { font-size:2rem; }
    h2 { font-size:1.45rem; margin-top:40px; }
    .phase { padding:20px 16px; }
    .step { grid-template-columns:32px 1fr; gap:10px; }
    .takeaways { padding:20px; }
    .site-nav { gap:8px 16px; }
  }
  @media print {
    :root { --fg:#111; --muted-fg:#444; --card:#fff; --muted:#eee; --border:#ccc; }
    .site-nav { display:none; }
    pre { white-space:pre-wrap; }
    table { min-width:0; }
  }
'''

NAV_ITEMS = [
    ('index.html', 'Start here'),
    ('README.html', 'Handbook'),
    ('prompts.html', 'Prompts'),
    ('evidence.html', 'Frames'),
    ('github-inspection.html', 'Theo'),
    ('matt-pocock-inspection.html', 'Matt'),
    ('boris-cherny-inspection.html', 'Boris'),
    ('adoption.html', 'Adoption'),
    ('validation.html', 'Validation'),
]


def nav(out_path):
    # Pages live in subdirectories (guides/, skills/..., examples/...); the
    # nav targets are repository-root relative, so prefix by depth.
    depth = len(out_path.relative_to(OUT).parent.parts) if out_path else 0
    prefix = '../' * depth
    return '<nav class="site-nav" aria-label="Handbook">' + ''.join(
        f'<a href="{escape(prefix + Path(t).as_posix())}">{escape(label)}</a>'
        for t, label in NAV_ITEMS) + '</nav>'


def wrap(out_path, title, body):
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<link rel="icon" href="data:,"><title>{escape(title)} · Agent engineering</title>'
            f'<style>{css}</style></head><body><main>{nav(out_path)}{body}</main></body></html>\n')


def rewrite_refs(body):
    # Generated HTML pages point at sibling generated HTML; asset and JSON links
    # are untouched. Editable .md files are copied next to each page, except
    # SKILL.md links, which stay on the copied skill source.
    return re.sub(
        r'href="([^"?#:]+)\.md([?#][^"]*)?"',
        lambda m: 'href="' + m.group(1) + '.html' + (m.group(2) or '') + '"'
        if not m.group(1).endswith('SKILL') else m.group(0),
        body)


def rewrite_tables(body):
    return (body
            .replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable table"><table>')
            .replace('</table>', '</table></div>'))


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

    # Markdown pages: render HTML, keep the editable source beside it.
    count = 0
    for rel in RENDER_MD:
        path = REPO / rel
        text = path.read_text()
        if text.startswith('---\n'):
            text = text.split('---', 2)[2].lstrip()
        title = next((s.lstrip('# ') for s in text.splitlines() if s.startswith('# ')), path.stem)
        body = markdown.markdown(text, extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.sane_lists',
            'markdown.extensions.toc'])
        body = rewrite_tables(rewrite_refs(body))
        md_name = path.name
        body += (f'<p class="source-note"><a href="{escape(md_name)}">Editable Markdown source</a>'
                 f' · Agent Engineering Handbook, September 9, 2026</p>')
        out = OUT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.with_suffix('.html').write_text(wrap(out, title, body))
        shutil.copy2(path, out)
        count += 1

    # Frame gallery.
    frames = json.loads((REPO / 'evidence/frame-manifest.json').read_text())
    body = ('<h1>The video, with visible evidence</h1>'
            '<p class="lead">12 frames extracted with ffmpeg and inspected at full resolution. '
            'Each caption distinguishes what is visible from what Theo only describes.</p>'
            '<p><a href="evidence/frame-manifest.json">Extraction commands and SHA-256 hashes</a> · '
            '<a href="evidence/video-research.html">Full extraction notes</a></p>')
    body += '<ul>' + ''.join(
        f'<li><a href="#frame-{f["seconds"]}">{escape(f["timestamp"])} — {escape(f["title"])}</a></li>'
        for f in frames) + '</ul>'
    for f in frames:
        body += (f'<section id="frame-{f["seconds"]}"><h2>{escape(f["timestamp"])} — {escape(f["title"])}</h2>'
                 f'<figure><a href="screenshots/{escape(f["file"])}">'
                 f'<img loading="lazy" width="1920" height="1080" src="screenshots/{escape(f["file"])}" '
                 f'alt="{escape(f["title"])} at {escape(f["timestamp"])}"></a>'
                 f'<figcaption>{escape(f["observation"])} '
                 f'<a href="{escape(f["url"])}">Watch this moment</a> · '
                 f'<a href="screenshots/{escape(f["file"])}">Full-size frame</a></figcaption></figure></section>')
    (OUT / 'evidence.html').write_text(wrap(OUT / 'evidence.html', 'Video evidence', body))

    # Landing page from the existing workflow template.
    body = re.search(r'<main>(.*?)</main>', source, re.S).group(1)
    body = re.sub(r'\s*<(span|div) class="(?:eyebrow|phase-index)">.*?</\1>', '', body, flags=re.S)
    body = re.sub(r'<div><span class="k">Time</span>.*?</div>', '', body, flags=re.S)
    body = body.replace(
        'Seven detailed implementation guides and a local lint example.',
        'Thirteen implementation guides, three repository investigations and a tested local lint example.')
    quick = ('<section class="quick-start"><p><strong>Explore the complete handbook</strong></p><ul>'
             '<li><a href="README.html">All 13 guides, 19 video ideas and four portable skills</a></li>'
             '<li><a href="evidence.html">12 timestamped screenshots</a></li>'
             '<li><a href="github-inspection.html">Theo’s architecture and PRs</a> · '
             '<a href="matt-pocock-inspection.html">Matt’s course manager</a> · '
             '<a href="boris-cherny-inspection.html">Boris’s public code</a></li>'
             '<li><a href="adoption.html">Adopt a skill or fold the methods into your own workflow</a></li>'
             '</ul></section>')
    body = body.replace('</header>', '</header>' + quick, 1)
    body = rewrite_refs(body)
    (OUT / 'index.html').write_text(wrap(OUT / 'index.html', 'Build better coding environments for agents', body))

    print(f'Rendered {count} Markdown pages, workflow index and {len(frames)}-frame gallery into public/.')


if __name__ == '__main__':
    main()
