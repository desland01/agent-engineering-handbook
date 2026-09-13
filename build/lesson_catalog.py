#!/usr/bin/env python3
"""The lesson catalog seam: load, validate and publish the ten approved lessons.

Inputs (read-only, never generated public/):
  build/lessons.json            -> the version-1 lesson manifest (exactly ten records)
  evidence/video-tips.json      -> the nineteen original source records
  lessons/<id>.md               -> the authored lesson for each manifest record

`load_lessons` fails loudly with a ValueError naming the offending file and ID
whenever any input is missing, malformed or disagrees with the approved lesson
identity compiled in below. Normalized records carry everything the renderer
needs, including `page`, the public route `lessons/<id>.html`.

`read_minutes` is a deterministic estimate from word count at 220 words per
minute — an estimate, not a measured reading speed. `readme_lessons_table` and
`sync_readme_lessons` produce and check the README lesson table between the
`<!-- lessons:start -->` / `<!-- lessons:end -->` markers without ever writing
to the filesystem. Standard library only.
"""
from pathlib import Path
import json
import math
import re

# ---------------------------------------------------------------------------
# The approved lesson identity. This mapping is fixed: a candidate manifest
# that renames, reassigns or drops any of it fails the build, whatever the
# candidate says. Titles are intentional interface identity.
# ---------------------------------------------------------------------------
APPROVED_VERSION = 1
APPROVED_TIPS = {
    'recurring-mistakes': ['tip-08-fix-class-loops', 'tip-19-custom-lint-economics'],
    'ci-feedback': ['tip-01-ci-feedback-loop'],
    'prove-it-works': ['tip-02-two-browser-e2e'],
    'working-previews': ['tip-04-preview-environments'],
    'missing-tools': ['tip-05-custom-file-upload-skill', 'tip-06-skill-authoring-reward'],
    'useful-instructions': ['tip-09-domain-knowledge-as-infra', 'tip-11-own-your-instructions',
                            'tip-12-steering-pushback', 'tip-14-zero-context-docs',
                            'tip-16-steer-not-map'],
    'fresh-agent': ['tip-15-minimal-context-calibration'],
    'shared-contracts': ['tip-13-type-safe-composition'],
    'codebase-navigation': ['tip-10-newcomer-questions-signal', 'tip-18-solo-onboarding'],
    'better-environments': ['tip-03-automation-multiplies-agents', 'tip-07-team-buy-in',
                            'tip-17-career-leverage'],
}
APPROVED_IDS = list(APPROVED_TIPS)
# The approved lesson-to-chapter assignment. The three declared renderer
# groups; a lesson in the wrong group (or an unknown group name) would be
# silently dropped from reader grouping.
APPROVED_CHAPTERS = {
    'recurring-mistakes': 'stop-repeat-work',
    'ci-feedback': 'stop-repeat-work',
    'prove-it-works': 'stop-repeat-work',
    'working-previews': 'give-agents-what-they-need',
    'missing-tools': 'give-agents-what-they-need',
    'useful-instructions': 'give-agents-what-they-need',
    'fresh-agent': 'give-agents-what-they-need',
    'shared-contracts': 'keep-it-understandable',
    'codebase-navigation': 'keep-it-understandable',
    'better-environments': 'keep-it-understandable',
}

# The seven public skill IDs. Every linked skill must exist on disk with a
# SKILL.md; there is no prepublication bypass for catalog loading.
PUBLISHED_SKILLS = {'agent-feedback-engineering', 'agent-ready-workspaces',
                    'agent-context-calibration', 'agent-tool-adapters'}
PROPOSED_SKILLS = {'agent-output-verification', 'agent-artifact-recovery',
                   'agent-contract-consistency'}
KNOWN_SKILLS = PUBLISHED_SKILLS | PROPOSED_SKILLS

SAFE_SLUG = re.compile(r'^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$')
TWO_DIGITS = re.compile(r'^\d\d$')
LEGACY_PART = re.compile(r'^[\w][\w.\-]*(/[\w][\w.\-]*)*$')
# An anchor for a source tip: an explicit HTML id exactly equal to the declared
# tip id (native span, heading anchor; single or double quotes). A Markdown
# heading whose generated slug merely resembles the id does NOT count: the slug
# would differ from the declared anchor and break source deep links.
ANCHOR_RE = re.compile(r"""id=["'](tip-[\w-]+)["']""")
H1_RE = re.compile(r'^#\s+(.+?)\s*$', re.M)
WORDS_PER_MINUTE = 220
MIN_PROSE_WORDS = 60

START = '<!-- lessons:start -->'
END = '<!-- lessons:end -->'


def _fail(path, lesson_id, message):
    where = f'{path} (lesson {lesson_id})' if lesson_id else str(path)
    raise ValueError(f'{where}: {message}')


def _read_json(path, what):
    if not path.is_file():
        raise ValueError(f'{path.name} is missing — {what} is required input, '
                         f'expected at {path}')
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise ValueError(f'{path.name} is not valid JSON ({e}); fix {path}') from None


def _anchors_present(markdown_text, tip_ids):
    found = set(ANCHOR_RE.findall(markdown_text))
    return [tip for tip in tip_ids if tip not in found]


def _prose_words(markdown_text):
    body = H1_RE.sub('', markdown_text, count=1)
    body = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', body)          # images
    body = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', body)        # links -> their text
    body = re.sub(r'<[^>]+>', ' ', body)                        # native tags
    return len([w for w in body.split() if w])


def load_lessons(repo_root: Path) -> list:
    """Load and validate the ten approved lessons; fail loudly on any defect."""
    repo_root = Path(repo_root)
    manifest_path = repo_root / 'build/lessons.json'
    tips_path = repo_root / 'evidence/video-tips.json'
    manifest = _read_json(manifest_path, 'the lesson manifest')
    tips = _read_json(tips_path, 'the original video extraction')

    # ---- input shape: every malformed form becomes an actionable ValueError
    # before any routes are derived. Inputs are only read, never mutated.
    if not isinstance(manifest, dict):
        _fail(manifest_path, '', f'the manifest must be an object with "version" and '
                                 f'"lessons", found {type(manifest).__name__}')
    version = manifest.get('version')
    if isinstance(version, bool) or not isinstance(version, int) \
            or version != APPROVED_VERSION:
        _fail(manifest_path, '', f'expected integer version {APPROVED_VERSION}, '
                                 f'found {version!r}')
    records = manifest.get('lessons')
    if not isinstance(records, list) or len(records) != 10:
        _fail(manifest_path, '', f'expected exactly 10 lesson records, found '
                                 f'{len(records) if isinstance(records, list) else type(records).__name__}')
    if not isinstance(tips, list) or not all(isinstance(t, dict) for t in tips):
        _fail(tips_path, '', 'the source extraction must be a list of tip objects')

    video_ids = set()
    for tip in tips:
        tip_id = tip.get('id')
        if not isinstance(tip_id, str) or not tip_id:
            _fail(tips_path, '', 'every source record needs a nonempty string "id"; '
                                 f'found {tip_id!r}')
        if tip_id in video_ids:
            _fail(tips_path, '', f'duplicate source record for tip {tip_id!r}')
        start = tip.get('start_seconds')
        if isinstance(start, bool) or not isinstance(start, int) or start < 0:
            _fail(tips_path, '', f'tip {tip_id!r} needs a nonnegative integer '
                                 f'"start_seconds", found {start!r}')
        video_ids.add(tip_id)

    by_id, orders, legacy_seen = {}, [], []
    for record in records:
        path = manifest_path
        if not isinstance(record, dict):
            _fail(path, '', f'every lesson record must be an object, found '
                            f'{type(record).__name__}')
        lesson_id = record.get('id')
        if not isinstance(lesson_id, str) or not SAFE_SLUG.match(lesson_id):
            _fail(path, lesson_id, f'id {lesson_id!r} is not a safe slug')
        if lesson_id in by_id:
            _fail(path, lesson_id, f'duplicate lesson id {lesson_id!r}')
        if lesson_id not in APPROVED_IDS:
            _fail(path, lesson_id, f'{lesson_id!r} is not one of the ten approved lesson ids')
        for field in ('title', 'summary', 'chapter'):
            if not isinstance(record.get(field), str) or not record[field].strip():
                _fail(path, lesson_id, f'{field} is required and must be nonempty')
        chapter = record['chapter'].strip()
        if chapter != APPROVED_CHAPTERS[lesson_id]:
            _fail(path, lesson_id, f'chapter must be the approved group '
                                   f'{APPROVED_CHAPTERS[lesson_id]!r} for this lesson, '
                                   f'found {chapter!r}')
        source = record.get('source')
        if source != f'lessons/{lesson_id}.md':
            _fail(path, lesson_id, f'source must be "lessons/{lesson_id}.md", found {source!r}')
        order = record.get('order')
        if not isinstance(order, int) or isinstance(order, bool) or not 1 <= order <= 10:
            _fail(path, lesson_id, f'order must be an int in 1..10, found {order!r}')
        if order in orders:
            _fail(path, lesson_id, f'order {order} is assigned to more than one lesson')
        orders.append(order)

        tip_ids = record.get('tip_ids')
        if not isinstance(tip_ids, list) or not all(isinstance(t, str) for t in tip_ids):
            _fail(path, lesson_id, f'tip_ids must be a list of tip id strings, found {tip_ids!r}')
        if tip_ids != APPROVED_TIPS[lesson_id]:
            _fail(path, lesson_id, f'tip_ids must be the approved mapping '
                                   f'{APPROVED_TIPS[lesson_id]}, found {tip_ids!r}')
        for tip_id in tip_ids:
            if tip_id not in video_ids:
                _fail(path, lesson_id, f'tip {tip_id!r} is not a known original video tip id '
                                       f'({tips_path.name})')

        guide_ids = record.get('guide_ids')
        if not isinstance(guide_ids, list) or not guide_ids:
            _fail(path, lesson_id, 'guide_ids must be a nonempty list')
        for guide_id in guide_ids:
            if not isinstance(guide_id, str) or not TWO_DIGITS.match(guide_id):
                _fail(path, lesson_id, f'guide id {guide_id!r} is not a two-digit string')
            matches = list((repo_root / 'guides').glob(f'{guide_id}-*.md'))
            if not matches:
                _fail(path, lesson_id, f'guide id {guide_id!r} resolves to no '
                                       f'guides/{guide_id}-*.md file')

        skill_ids = record.get('skill_ids')
        if not isinstance(skill_ids, list) or not skill_ids:
            _fail(path, lesson_id, 'skill_ids must be a nonempty list')
        for skill_id in skill_ids:
            if not isinstance(skill_id, str):
                _fail(path, lesson_id, f'skill_ids entries must be strings, found '
                                       f'{skill_id!r} in skill_ids {skill_ids!r}')
            if skill_id not in KNOWN_SKILLS:
                _fail(path, lesson_id, f'skill {skill_id!r} is not one of the seven public '
                                       f'skill ids {sorted(KNOWN_SKILLS)}')
            # Every linked skill must exist on disk with a SKILL.md; a linked
            # skill without a published package is a dead link for readers.
            if not (repo_root / 'skills' / skill_id / 'SKILL.md').is_file():
                _fail(path, lesson_id, f'skills/{skill_id}/SKILL.md is missing')

        legacy = record.get('legacy_paths')
        if not isinstance(legacy, list) or not legacy:
            _fail(path, lesson_id, 'legacy_paths must be a nonempty list')
        for rel in legacy:
            if not isinstance(rel, str) or rel.startswith('/') or '\\' in rel or not LEGACY_PART.match(rel):
                detail = 'absolute' if isinstance(rel, str) and rel.startswith('/') else 'traversal'
                _fail(path, lesson_id, f'legacy path {rel!r} is not a relative site path '
                                       f'({detail} rejected)')
            if rel in legacy_seen:
                _fail(path, lesson_id, f'duplicate legacy route {rel!r}')
            legacy_seen.append(rel)
        # Per-lesson mapping: this lesson's old routes must be exactly the
        # original routes of the tips it covers, so each reader of an old URL
        # lands on the lesson about that topic.
        expected_here = sorted(_tip_routes(tips)[t] for t in tip_ids)
        if sorted(legacy) != expected_here:
            diff = sorted(set(legacy) ^ set(expected_here))
            _fail(path, lesson_id, f'legacy paths must be exactly the original routes of '
                                   f'this lesson\'s tips {expected_here}; first difference: '
                                   f'{diff[:3]}')

        source_file = repo_root / source
        if not source_file.is_file():
            _fail(source_file, lesson_id, 'the authored lesson file is missing')
        text = source_file.read_text() if source_file.is_file() else ''
        if not text.strip():
            _fail(source_file, lesson_id, 'the authored lesson file is empty')
        h1 = H1_RE.search(text)
        if not h1 or h1.group(1).strip() != record['title'].strip():
            _fail(source_file, lesson_id, f'the lesson h1 must be exactly the manifest title '
                                          f'{record["title"]!r}, found '
                                          f'{h1.group(1).strip() if h1 else None!r}')
        words = _prose_words(text)
        if words < MIN_PROSE_WORDS:
            _fail(source_file, lesson_id, f'the lesson prose is {words} words; at least '
                                          f'{MIN_PROSE_WORDS} are required')
        missing = _anchors_present(text, tip_ids)
        if missing:
            _fail(source_file, lesson_id, f'missing source anchor(s) for tip id(s) {missing}')

        by_id[lesson_id] = {
            'id': lesson_id, 'order': order, 'chapter': chapter,
            'title': record['title'], 'summary': record['summary'], 'source': source,
            'tip_ids': list(tip_ids), 'guide_ids': list(guide_ids),
            'skill_ids': list(skill_ids), 'legacy_paths': list(legacy),
            'page': f'lessons/{lesson_id}.html',
        }

    if sorted(orders) != list(range(1, 11)):
        _fail(manifest_path, '', f'orders must be exactly 1..10, found {sorted(orders)}')
    assigned = [t for l in by_id.values() for t in l['tip_ids']]
    if len(assigned) != len(set(assigned)):
        dupe = sorted({t for t in assigned if assigned.count(t) > 1})[0]
        _fail(manifest_path, '', f'tip {dupe!r} is assigned more than once; every source tip '
                                 f'has exactly one primary lesson')
    if set(assigned) != video_ids:
        missing = sorted(video_ids - set(assigned))
        _fail(manifest_path, '', f'tip(s) {missing} are not assigned to any lesson; all '
                                 f'{len(video_ids)} source tips must be covered once')
    expected_legacy = _expected_legacy_paths(tips, assigned)
    actual_legacy = sorted(l for rec in by_id.values() for l in rec['legacy_paths'])
    if actual_legacy != expected_legacy:
        diff = sorted(set(actual_legacy) ^ set(expected_legacy))
        _fail(manifest_path, '', f'legacy paths do not match the exact nineteen routes in '
                                 f'original source order; first difference: {diff[:3]}')
    return [by_id[lesson_id] for lesson_id in sorted(by_id, key=lambda k: by_id[k]['order'])]


def _tip_routes(tips):
    """tip id -> its original old ideas/*.html route, from the observed source.

    The idea number of a tip is its position in the video's own order
    (start_seconds), and the slug is the tip id's trailing part — so the mapping
    comes from the observed source, not from the candidate manifest.
    """
    route = {}
    for n, tip in enumerate(sorted(tips, key=lambda t: t['start_seconds']), 1):
        suffix = tip['id'].split('-', 2)[2]
        route[tip['id']] = f'ideas/{n:02d}-{suffix}.html'
    return route


def _expected_legacy_paths(tips, assigned_tip_ids):
    """The exact nineteen old ideas/*.html routes, in original observed source order."""
    route = _tip_routes(tips)
    return sorted(route[t] for t in assigned_tip_ids)


# ---------------------------------------------------------------------------
# Reading time: an honest, deterministic estimate.
# ---------------------------------------------------------------------------
def read_minutes(markdown_text: str) -> int:
    """Estimated minutes at 220 words per minute, minimum 1.

    This is an estimate from word count, not a measured reading speed. HTML
    tags, image syntax and link targets are ignored; link text is counted.
    """
    text = re.sub(r'<[^>]+>', ' ', markdown_text or '')
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    words = [w for w in text.split() if not re.match(r'^(https?:|mailto:|www\.)', w)]
    return max(1, math.ceil(len(words) / WORDS_PER_MINUTE))


# ---------------------------------------------------------------------------
# README lesson table.
# ---------------------------------------------------------------------------
def readme_lessons_table(lessons: list) -> str:
    """The README lesson table: one row per lesson, in order. No files mutated."""
    rows = '\n'.join(
        f'| [{escape_pipe(l["title"])}]({l["source"]}) | {escape_pipe(l["summary"])} |'
        for l in lessons)
    return f'| Lesson | Summary |\n|---|---|\n{rows}'


def escape_pipe(text):
    return text.replace('|', '\\|')


def sync_readme_lessons(readme_text: str, lessons: list, *, check: bool = False) -> str:
    """Replace the README content between the lesson markers; never write files.

    Exactly one start marker and one end marker must appear, start before end.
    With check=True, raise instead of returning when the current block differs
    from the generated table (drift), so a stale README fails its check.
    """
    n_start, n_end = readme_text.count(START), readme_text.count(END)
    if n_start != 1 or n_end != 1:
        missing = [m for m, n in ((START, n_start), (END, n_end)) if n != 1]
        raise ValueError(f'README lesson markers: expected exactly one of each marker; '
                         f'problem with {missing} (found {n_start} start, {n_end} end)')
    begin = readme_text.index(START)
    finish = readme_text.index(END)
    if finish < begin:
        raise ValueError(f'README lesson markers are reversed: {END} appears before {START}')
    table = readme_lessons_table(lessons)
    current = readme_text[begin + len(START):finish].strip('\n')
    if check and current != table:
        raise ValueError(f'README lesson table has drifted from the manifest; run the '
                         f'sync without check=True (or update README.md). Current block '
                         f'starts {current[:60]!r}')
    return (readme_text[:begin + len(START)] + '\n' + table + '\n'
            + readme_text[finish:])
