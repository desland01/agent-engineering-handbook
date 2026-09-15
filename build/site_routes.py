"""Resolve local public addresses with the explicit permanent hosting redirects.

No server or network effects. Reject traversal, redirect cycles and missing files.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json


def redirects_at(repo):
    rows = json.loads((Path(repo) / 'vercel.json').read_text()).get('redirects', [])
    if len({r['source'] for r in rows}) != len(rows):
        raise ValueError('duplicate redirect source')
    for row in rows:
        if row.get('permanent') is not True:
            raise ValueError(f"redirect is not permanent: {row['source']}")
    return {r['source']: r['destination'] for r in rows}


def resolve_local(public, page, target, redirects):
    public = Path(public).resolve()
    page = Path(page).resolve()
    seen = set()
    while True:
        parts = urlsplit(target)
        if parts.scheme or parts.netloc:
            raise ValueError(f'not a local address: {target}')
        path = unquote(parts.path)
        base = public if path.startswith('/') else page.parent
        resolved = (base / path.lstrip('/')).resolve() if path else page
        if not resolved.is_relative_to(public):
            raise ValueError(f'link escapes public/: {target}')
        route = '/' + resolved.relative_to(public).as_posix()
        if route == '/.': route = '/'
        if path.endswith('/') and not route.endswith('/'): route += '/'
        if route in redirects:
            if route in seen: raise ValueError(f'redirect cycle: {route}')
            seen.add(route)
            target = redirects[route]
            page = public / 'index.html'
            continue
        if resolved.is_dir(): resolved /= 'index.html'
        if not resolved.is_file(): raise ValueError(f'unresolved link: {target}')
        return resolved, unquote(parts.fragment)
