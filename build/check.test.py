"""Source layout behaves the same in Git checkouts and deployment archives.

The integration tests run the catalog seam and the checker against the actual
accepted tree, including deliberately bad cases at the real entry."""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parent.parent
# Fixture roots live inside the checkout's own scratch directory, not /tmp: the
# test runner may not be able to write outside the workspace, and .scratch is
# already in the checker's generated-directory ignore set.
SCRATCH = REPO / '.scratch'


class temp_root:
    """A temporary directory inside the checkout's scratch directory, removed
    on exit."""

    def __init__(self, prefix):
        self.prefix = prefix
        self.path = None

    def __enter__(self):
        SCRATCH.mkdir(exist_ok=True)
        self.path = Path(tempfile.mkdtemp(prefix=self.prefix, dir=SCRATCH))
        return self.path

    def __exit__(self, *exc):
        shutil.rmtree(self.path, ignore_errors=True)
        return False


class ArchiveLayoutTest(unittest.TestCase):
    def test_generated_files_are_ignored_but_source_violations_are_rejected(self):
        spec = importlib.util.spec_from_file_location('handbook_check', Path(__file__).with_name('check.py'))
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        with temp_root('layout-') as directory:
            checker.ROOT = directory
            for name in ['.vercel/project.json', '.build-deps/markdown/core.py',
                         'control/plan-20260910.md', 'unexpected.txt', 'guides/test.md']:
                target = checker.ROOT / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('fixture')
            with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, ['git'])):
                files = {str(path) for path in checker.tracked_files()}
                checker.layout()
            self.assertEqual(files, {'control/plan-20260910.md', 'unexpected.txt', 'guides/test.md'})
            self.assertTrue(any('unexpected entry' in failure for failure in checker.failures))
            self.assertTrue(any('a date, version' in failure for failure in checker.failures))
            self.assertFalse(any('guides/test.md' in failure for failure in checker.failures))


REPO = Path(__file__).resolve().parent.parent

# The ten approved lesson ids, as the independent source of truth for the
# integration tests (mirrors the compiled list in check.py on purpose: two
# independent literals must agree).
APPROVED_IDS = [
    'recurring-mistakes', 'ci-feedback', 'prove-it-works', 'working-previews',
    'missing-tools', 'useful-instructions', 'shared-contracts',
    'codebase-navigation', 'resume-work', 'better-environments',
]


def load_checker():
    spec = importlib.util.spec_from_file_location('handbook_check', Path(__file__).with_name('check.py'))
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    checker.failures = []
    return checker


class CatalogAtRealEntryTest(unittest.TestCase):
    """The reviewed catalog seam must accept the actual accepted tree."""

    def test_approved_sitemap_replaces_fresh_agent_with_recovery(self):
        records = json.loads((REPO / 'build/lessons.json').read_text())['lessons']
        self.assertEqual([r['id'] for r in records], APPROVED_IDS)
        self.assertEqual(records[8]['tip_ids'], [])
        self.assertEqual(records[8]['guide_ids'], ['12'])
        self.assertIn('guides/12-artifact-identity-and-recovery.md', records[8]['legacy_paths'])
        guides = [g for r in records for g in r['guide_ids']]
        self.assertEqual(sorted(guides), [f'{n:02d}' for n in range(1, 14)])

    def test_real_manifest_loads_the_ten_approved_lessons(self):
        sys_path = str(Path(__file__).resolve().parent)
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)
        import lesson_catalog
        lessons = lesson_catalog.load_lessons(REPO)
        self.assertEqual([l['id'] for l in lessons], APPROVED_IDS)
        self.assertEqual([l['order'] for l in lessons], list(range(1, 11)))
        tips = [t for l in lessons for t in l['tip_ids']]
        self.assertEqual(len(tips), 19)
        self.assertEqual(len(set(tips)), 19, 'a source tip is assigned twice')
        evidence_ids = {t['id'] for t in json.loads(
            (REPO / 'evidence/video-tips.json').read_text())}
        self.assertEqual(set(tips), evidence_ids,
                         'covered tips are not exactly the nineteen source ids')

    def test_committed_readme_table_is_in_sync(self):
        sys_path = str(Path(__file__).resolve().parent)
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)
        import lesson_catalog
        lessons = lesson_catalog.load_lessons(REPO)
        # check=True raises on drift, so this asserts the committed README
        # matches the manifest without writing anything.
        lesson_catalog.sync_readme_lessons(
            (REPO / 'README.md').read_text(), lessons, check=True)


class ApprovedSiteTest(unittest.TestCase):
    def test_public_sitemap_transcription_matches_approved_plan(self):
        plan = (REPO / 'control/plan.md').read_text()
        expected = {}
        for name in ('sitemap', 'aliases'):
            block = plan.split(f'<!-- {name}:start -->')[1].split(f'<!-- {name}:end -->')[0]
            for label, path, parent, status in re.findall(r'^\s*- (.*?) \| `([^`]+)` \| parent: `([^`]+)` \| (.*)$', block, re.M):
                earlier = name == 'aliases' or status.startswith(('merged into ', 'redirects to '))
                expected[path] = ('Earlier: ' if earlier else '') + label
        actual = json.loads((REPO / 'build/sitemap.json').read_text())
        self.assertEqual({e['path']: e['label'] for e in actual}, expected)
        self.assertEqual(len(expected), 156)
        manifest = json.loads((REPO / 'build/lessons.json').read_text())
        legacy = set(manifest.get('legacy_paths', []))
        legacy.update(p for l in manifest['lessons'] for p in l['legacy_paths'])
        self.assertEqual(legacy, {e['path'][1:] for e in actual if 'destination' in e})

    def test_local_link_resolution_rejects_escape_cycles_and_missing_targets(self):
        from site_routes import resolve_local
        with temp_root('route-boundary-') as root:
            public = root / 'public'; public.mkdir()
            page = public / 'index.html'; page.write_text('Home')
            destination = public / 'lesson.html'; destination.write_text('Lesson')
            self.assertEqual(resolve_local(public, page, '/old', {'/old': '/lesson.html#sources'}), (destination, 'sources'))
            for target, redirects in [('../private.md', {}), ('/%2e%2e/private.md', {}),
                                      ('/missing.html', {}), ('/old', {'/old': '/other', '/other': '/old'})]:
                with self.subTest(target=target), self.assertRaises(ValueError):
                    resolve_local(public, page, target, redirects)

    def test_changed_hubs_reject_internal_copy(self):
        checker = load_checker()
        with temp_root('hub-copy-') as root:
            CheckerAtRealEntryTest().copy_public_inputs(REPO, root, include_public=True)
            checker.PUBLIC = root / 'public'
            page = checker.PUBLIC / 'lessons.html'
            page.write_text(re.sub(r'<h1>.*?</h1>', '<h1>Read <code>build/lessons.json</code></h1>', page.read_text()))
            checker.hub_copy_checked()
            self.assertTrue(any('lessons.html' in f and 'plain' in f for f in checker.failures))

    def test_public_inventory_and_permanent_dispositions(self):
        self.assertEqual(len(list((REPO / 'public').rglob('*.html'))), 33)
        redirects = {r['source']: r for r in json.loads((REPO / 'vercel.json').read_text())['redirects']}
        self.assertEqual(redirects['/guides/12-artifact-identity-and-recovery.md']['destination'], '/lessons/resume-work.html')
        self.assertIs(redirects['/README.html']['permanent'], True)
        self.assertFalse((REPO / 'public/guides.html').exists())

    def test_checker_rejects_missing_and_misdirected_legacy_routes(self):
        checker = load_checker()
        with temp_root('redirects-') as root:
            CheckerAtRealEntryTest().copy_public_inputs(REPO, root, include_public=True)
            checker.REPO, checker.PUBLIC = root, root / 'public'
            config = json.loads((root / 'vercel.json').read_text())
            for row in config['redirects']:
                if row['source'] == '/guides/12-artifact-identity-and-recovery.md':
                    row['destination'] = '/lessons/ci-feedback.html'
            (root / 'vercel.json').write_text(json.dumps(config))
            checker.sitemap_checked()
            self.assertTrue(any('guides/12-artifact-identity-and-recovery.md' in f and 'destination' in f for f in checker.failures))

    def test_header_has_complete_menu_and_one_repository_link(self):
        from html.parser import HTMLParser
        from urllib.parse import urljoin
        text = (REPO / 'public/index.html').read_text()
        header = re.search(r'<header class="site-head">.*?</header>', text, re.S).group()
        self.assertEqual(header.count('https://github.com/desland01/agent-engineering-handbook'), 1)
        self.assertIn('>Sources</a>', header)
        menu = re.search(r'<details class="menu">.*?</details>', header, re.S).group()
        links = re.findall(r'href="([^"]+)"', menu)
        expected = json.loads((REPO / 'build/sitemap.json').read_text())
        self.assertTrue({e['path'] for e in expected}.issubset({urljoin('/', h) for h in links}))
        self.assertEqual(links[-1], 'https://github.com/desland01/agent-engineering-handbook')
        for label in ['Start here', 'Lessons', 'Skills', 'Sources', 'Help', 'Source texts', 'Earlier links']:
            self.assertIn(label, menu)

    def test_articles_use_accepted_sources_without_video_chrome(self):
        paths = [(l['source'], l['source'].replace('.md', '.html')) for l in json.loads((REPO / 'build/lessons.json').read_text())['lessons']]
        paths += [(str(p.relative_to(REPO)), str(p.relative_to(REPO).parent / 'index.html')) for p in (REPO / 'skills').glob('*/README.md')]
        for source, route in paths:
            with self.subTest(route=route):
                text = (REPO / 'public' / route).read_text()
                article = re.search(r'<article>(.*?)</article>', text, re.S).group(1).strip()
                self.assertTrue(article.startswith('<p>'))
                self.assertIn('<h2 id="sources">', article)
                self.assertNotRegex(text, r'id="(?:said|apply|useful|qualification)"')
                self.assertNotIn('class="tip-glyphs"', text)
                self.assertNotIn('In the video</h2>', text)
                md = (REPO / source).read_text()
                for pattern in [r'<ol id="citations">.*?</ol>', r'<p id="next-action">.*?</p>']:
                    raw = re.search(pattern, md, re.S).group()
                    self.assertIn(raw, article)
        self.assertIn('<pre><code', (REPO / 'public/lessons/recurring-mistakes.html').read_text())


class CheckerAtRealEntryTest(unittest.TestCase):
    """The checker's independent manifest read and its bad-case coverage."""

    def test_problem_picker_labels_destinations_without_row_numbers(self):
        text = (REPO / 'public/index.html').read_text()
        panel = re.search(r'<div class="pick">(.*?)</div>\s*<figure class="hero-figure"', text, re.S).group(1)
        self.assertNotIn('class="ix"', panel)
        rows = re.search(r'<ul role="list" aria-labelledby="problems">(.*?)</ul>', panel, re.S).group(1)
        self.assertEqual(rows.count('<li>'), 10)
        numbers = [int(n) for n in re.findall(r'<span class="n">Lesson (\d+)</span>', rows)]
        # One row per lesson, in lesson order: a reader scanning the numbers sees 1 to 10.
        self.assertEqual(numbers, list(range(1, 11)))
        self.assertIn('lessons/prove-it-works.html', panel)
        self.assertIn('lessons/resume-work.html', panel)
        self.assertNotIn('assets/problem-loop.webp', panel)

    def test_checker_reads_the_real_manifest_without_failures(self):
        checker = load_checker()
        records = checker.manifest_lessons_checked()
        self.assertEqual([r['id'] for r in records], APPROVED_IDS)
        self.assertEqual(checker.failures, [])

    def _temp_site(self):
        """A fixture root inside the checkout's scratch directory."""
        SCRATCH.mkdir(exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix='manifest-', dir=SCRATCH))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        return tmp

    def test_tampered_manifest_is_rejected(self):
        # A duplicate tip assignment must be refused, naming the tip.
        tmp = self._temp_site()
        shutil.copytree(REPO / 'build', tmp / 'build',
                        ignore=shutil.ignore_patterns('node_modules', '__pycache__'))
        shutil.copytree(REPO / 'evidence', tmp / 'evidence')
        shutil.copytree(REPO / 'lessons', tmp / 'lessons')
        shutil.copytree(REPO / 'skills', tmp / 'skills')
        shutil.copytree(REPO / 'guides', tmp / 'guides')
        (tmp / 'guides').mkdir(exist_ok=True)
        shutil.copy2(REPO / 'vercel.json', tmp / 'vercel.json')
        manifest = json.loads((tmp / 'build/lessons.json').read_text())
        manifest['lessons'][1]['tip_ids'] = ['tip-08-fix-class-loops']
        (tmp / 'build/lessons.json').write_text(json.dumps(manifest))
        checker = load_checker()
        original = checker.REPO
        checker.REPO = tmp
        try:
            # check() records a failure instead of raising, so the manifest is
            # still returned; the rejection shows up in checker.failures.
            records = checker.manifest_lessons_checked()
        finally:
            checker.REPO = original
        rejection = [f for f in checker.failures if 'tip-08-fix-class-loops' in f]
        self.assertTrue(rejection,
                        f'no failure names the duplicated tip: {checker.failures}')
        self.assertTrue(any('source ids' in f for f in checker.failures))

    # The explicit public fixture input set. Nothing outside this list is ever
    # copied into a fixture root: no .env, no .git, no private control/, no
    # local agent installs, no arbitrary symlinks. public/ is a generated
    # directory (not a delivery artifact) and is copied only when a test needs
    # to run the checker or renderer end to end.
    FIXTURE_DIRS = {
        'build': shutil.ignore_patterns('node_modules', '__pycache__', '.scratch'),
        'evidence': None, 'guides': None, 'lessons': None, 'skills': None,
        'screenshots': None, 'examples': None,
    }
    FIXTURE_FILES = ['README.md', 'ATTRIBUTION.md', 'CONTRIBUTING.md', 'DESIGN.md',
                     'INTERACTIONS.md', 'adoption.md', 'prompts.md', 'validation.md',
                     'github-inspection.md', 'matt-pocock-inspection.md',
                     'boris-cherny-inspection.md', 'vercel.json']
    FORBIDDEN_IN_FIXTURE = {'.env', '.env.local', '.git', 'control', 'node_modules',
                            '.vercel', '.scratch', '.build-deps'}

    def copy_public_inputs(self, source, dest, *, include_public=False):
        """Copy the explicit public fixture input set from source to dest.

        Never walks the source root: it touches only the allowlisted entries
        above, skips anything that is a symbolic link, and never copies the
        forbidden private/runtime entries even when they exist in source."""
        dest.mkdir(parents=True, exist_ok=True)

        def exclude_private(directory, names):
            return [name for name in names
                    if name in self.FORBIDDEN_IN_FIXTURE
                    or name in {'.agents', '.claude', '.serena', '__pycache__'}
                    or name.startswith('.env')
                    or (Path(directory) / name).is_symlink()]

        for name in self.FIXTURE_DIRS:
            src = source / name
            if not src.is_dir() or src.is_symlink():
                continue
            shutil.copytree(src, dest / name, ignore=exclude_private)
        for name in self.FIXTURE_FILES:
            src = source / name
            if src.is_file() and not src.is_symlink():
                shutil.copy2(src, dest / name)
        if include_public and (source / 'public').is_dir() and not (source / 'public').is_symlink():
            shutil.copytree(source / 'public', dest / 'public', ignore=exclude_private)

    def assert_no_private_entries(self, root):
        found = [p.relative_to(root).as_posix() for p in root.rglob('*')
                 if p.name in self.FORBIDDEN_IN_FIXTURE or p.is_symlink()]
        self.assertEqual(found, [],
                         f'fixture contains private/runtime entries or symlinks: {found}')

    def test_fixture_helper_excludes_private_sentinels(self):
        """Harmless private-named sentinels in a bounded toy source tree must
        never reach the fixture. No production .env/.git/control file is
        opened or copied by this test — the sentinels are written here."""
        toy = temp_root('toy-')
        fixture = temp_root('fixture-')
        with toy, fixture:
            toy, fixture = toy.path, fixture.path
            self._write_toy_tree(toy)
            self.copy_public_inputs(toy, fixture)
            self.assert_no_private_entries(fixture)
            self.assertTrue((fixture / 'build/lessons.json').is_file())
            self.assertTrue((fixture / 'lessons/ci-feedback.md').is_file())
            self.assertFalse((fixture / 'evidence/link.json').exists())
            self.assertFalse((fixture / 'examples/fixture/node_modules').exists())
            self.assertFalse((fixture / 'skills/agent-tool-adapters/.env.local').exists())

    def _write_toy_tree(self, toy):
        for name in ['build/lessons.json', 'evidence/video-tips.json',
                     'guides/01-recurring-failures.md', 'lessons/ci-feedback.md',
                     'skills/agent-tool-adapters/SKILL.md', 'screenshots/f.jpg',
                     'README.md', 'vercel.json']:
            target = toy / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('fixture')
        for name in ['.env', '.env.local', 'control/plan.md', 'node_modules/pkg/index.js',
                     '.vercel/project.json', 'examples/fixture/node_modules/pkg/index.js',
                     'skills/agent-tool-adapters/.env.local']:
            target = toy / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('SENTINEL: fixture-only, contains no real material')
        (toy / '.git').mkdir()
        (toy / '.git/HEAD').write_text('ref: SENTINEL')
        (toy / 'evidence/link.json').symlink_to(toy / 'README.md')

    def test_tampered_canonical_fails_the_full_check(self):
        """Canonical protection still rejects a reader claiming another address."""
        with temp_root('check-') as tmp:
            self.copy_public_inputs(REPO, tmp, include_public=True)
            self.assert_no_private_entries(tmp)
            page = tmp / 'public/lessons/ci-feedback.html'
            text = page.read_text()
            mutated = text.replace(
                'href="https://agent-engineering-handbook.dev/lessons/ci-feedback.html"',
                'href="https://agent-engineering-handbook.dev/ideas/01-ci-feedback-loop.html"')
            self.assertNotEqual(mutated, text)
            page.write_text(mutated)
            result = subprocess.run([sys.executable, 'build/check.py'], cwd=tmp,
                                    capture_output=True, text=True, timeout=300)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('canonical', result.stdout)
            self.assertIn('lessons/ci-feedback.html', result.stdout)

    def test_idea_destinations_are_invisible_outside_reader_articles(self):
        for page in (REPO / 'public/lessons').glob('*.html'):
            text = page.read_text()
            article = re.search(r'<article>(.*?)</article>', text, re.S).group(1)
            self.assertNotRegex(article, r'id="(?:said|apply|useful|qualification|video-note-\d+)"')
        text = (REPO / 'public/lessons/useful-instructions.html').read_text()
        self.assertIn('<span id="video-note-16" class="legacy-target" aria-hidden="true"></span>', text)

    def test_skill_explanations_link_owning_lessons_and_agent_companions(self):
        expected = {'agent-output-verification': 'prove-it-works',
                    'agent-artifact-recovery': 'resume-work',
                    'agent-contract-consistency': 'shared-contracts'}
        for name, lesson in expected.items():
            text = (REPO / 'public/skills' / name / 'index.html').read_text()
            self.assertIn(f'href="../../lessons/{lesson}.html"', text)
            for companion in ['SKILL.md','references/implementation.md','references/source-patterns.md']:
                self.assertIn(f'href="{companion}"', text)
            self.assertNotIn('class="skill-ref"', text)

    def test_legacy_index_redirects_to_self_canonical_lesson_hub(self):
        redirects = {r['source']: r for r in json.loads((REPO / 'vercel.json').read_text())['redirects']}
        self.assertEqual(redirects['/ideas.html']['destination'], '/lessons.html')
        self.assertIs(redirects['/ideas.html']['permanent'], True)
        text = (REPO / 'public/lessons.html').read_text()
        self.assertIn('<meta property="og:url" content="https://agent-engineering-handbook.dev/lessons.html">', text)

    def test_layout_check_passes_without_generated_public_output(self):
        """--layout is a source-only check: it must pass on an archive-style
        tree with no public/ directory, not fake a pass or demand one."""
        with temp_root('archive-') as tmp:
            self.copy_public_inputs(REPO, tmp, include_public=False)
            self.assertFalse((tmp / 'public').exists(), 'fixture unexpectedly has public/')
            result = subprocess.run([sys.executable, 'build/check.py', '--layout'], cwd=tmp,
                                    capture_output=True, text=True, timeout=300)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('PASS: source layout', result.stdout)

    def _markdown_parent(self):
        spec = importlib.util.find_spec('markdown')
        if spec is None or spec.origin is None:
            self.fail('Markdown is required: install build/requirements.txt before running the checks')
        return Path(spec.origin).resolve().parent.parent

    def _public_byte_map(self, root):
        return {p.relative_to(root).as_posix(): p.read_bytes()
                for p in (root / 'public').rglob('*') if p.is_file()}

    def test_render_with_invalid_input_leaves_previous_output_untouched(self):
        """A malformed lesson manifest must fail the render before it deletes
        the existing public/ directory, so the last usable preview survives."""
        markdown_parent = self._markdown_parent()
        tmp = temp_root('render-')
        with tmp:
            self.copy_public_inputs(REPO, tmp.path, include_public=True)
            root = tmp.path
            before = self._public_byte_map(root)
            manifest = json.loads((root / 'build/lessons.json').read_text())
            manifest['lessons'][0]['id'] = 'not-an-approved-lesson'
            (root / 'build/lessons.json').write_text(json.dumps(manifest))
            env = dict(subprocess.os.environ, PYTHONPATH=str(markdown_parent))
            result = subprocess.run([sys.executable, 'build/render.py'], cwd=root,
                                    capture_output=True, text=True, timeout=300, env=env)
            self.assertNotEqual(result.returncode, 0,
                                'the render accepted a manifest naming a non-approved lesson')
            self.assertIn('not-an-approved-lesson', result.stderr)
            self.assertEqual(self._public_byte_map(root), before,
                             'the failed render destroyed or altered the previous public/ output')


class LessonStandardTest(unittest.TestCase):
    OPENING = 'A repeated mistake needs a reliable check. You can test its boundary before trusting it.'
    BODY = ('<h2>Checks reject repeated mistakes</h2>'
            '<p>The bad case fails. The good case passes. '
            'The example names the boundary <a href="#cite-demo">at the source</a>.</p>')
    SOURCES = ('<h2 id="sources">The example shows the boundary</h2>'
               '<p>The source records the failure. It also records the valid case. '
               'It does not prove wider coverage.</p>'
               '<ol id="citations"><li id="cite-demo">'
               '<a href="https://example.test/demo#boundary">The source example</a>'
               '</li></ol>')
    CLOSE = '<p id="next-action">Test one repeated mistake against its permitted alternative.</p>'

    def page(self, *, opening=None, body=None, sources=None, close=None):
        return ('<html><body><main><h1>You test a repeated mistake</h1><article><p>'
                + (self.OPENING if opening is None else opening) + '</p>'
                + (self.BODY if body is None else body)
                + (self.SOURCES if sources is None else sources)
                + (self.CLOSE if close is None else close)
                + '</article></main></body></html>')

    def scan_pages(self, pages):
        checker = load_checker()
        with temp_root('lesson-standard-') as root:
            checker.PUBLIC = root / 'public'
            for name, html in pages.items():
                target = checker.PUBLIC / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(html)
            checker.lesson_standard()
            return checker.failures

    def assert_rule(self, code, bad, good=None):
        for name in ['lessons/demo.html', 'skills/demo/index.html']:
            with self.subTest(page=name):
                failures = self.scan_pages({name: bad})
                self.assertTrue(any(code in f and name in f for f in failures), failures)
                self.assertEqual(self.scan_pages({name: good or self.page()}), [])

    def test_article_requires_opening_before_sections(self):
        for bad in [self.page().replace('<article>', '<div>').replace('</article>', '</div>'),
                    self.page().replace('<p>' + self.OPENING + '</p>', ''),
                    self.page(body='', sources=''),
                    self.page().replace('</main>', '<article><p>Extra.</p></article></main>')]:
            self.assert_rule('LS01', bad)


    def test_opening_has_two_or_three_sentences(self):
        for opening in ['Only one sentence.', 'One. Two. Three. Four.',
                        'One. Two. Three. An unfinished fourth']:
            self.assert_rule('LS02', self.page(opening=opening))
        for opening in ['One. Two. Three.', 'Dr. Smith checks version 2.5. You test the result.',
                        'A check fails, e.g. on the bad case. You verify the valid case.']:
            self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(opening=opening)}), [])


    def test_opening_respects_360_character_budget(self):
        # Independent boundary literals: 356 letters plus ". B." = 360 characters.
        at_limit = 'A' * 356 + '. B.'
        self.assert_rule('LS03', self.page(opening='A' * 357 + '. B.'),
                         self.page(opening=at_limit))
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(
            opening='<em>' + 'A' * 354 + '</em>&amp;B.\n   C.')}), [])


    def test_pages_never_use_the_learning_prompt_phrase(self):
        for phrase in ['what you will know', 'WHAT you\n will know',
                       'what <em>you</em> will&nbsp;know']:
            self.assert_rule('LS04', self.page().replace('</article>',
                             '</article><footer><p>' + phrase + '</p></footer>'))
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page().replace(
            '</body>', '<script>"what you will know"</script></body>')}), [])


    def test_headings_are_shared_by_at_most_two_pages_per_kind(self):
        for kind in ['lessons', 'skills']:
            def name(i):
                return f'lessons/{i}.html' if kind == 'lessons' else f'skills/{i}/index.html'
            # The shared headings include h1, h2 and h3; two pages are permitted.
            html = self.page(body=self.BODY + '<h3>Compare the boundary</h3>')
            failures = self.scan_pages({name(i): html for i in range(3)})
            for heading in ['You test a repeated mistake', 'Checks reject repeated mistakes',
                            'Compare the boundary']:
                self.assertTrue(any('LS05' in f and heading in f and name(0) in f
                                    and name(1) in f and name(2) in f for f in failures), failures)
            self.assertEqual(self.scan_pages({name(i): html for i in range(2)}), [])
        self.assertEqual(self.scan_pages({'lessons/1.html': self.page(),
                                         'lessons/2.html': self.page(),
                                         'skills/1/index.html': self.page(),
                                         'skills/2/index.html': self.page()}), [])
        # Chrome headings never enter the authored-heading comparison.
        pages = {f'lessons/{i}.html': self.page().replace('mistake', f'mistake {i}').replace(
            'The example shows the boundary', f'The example shows boundary {i}').replace(
            '</main>', '</main><aside><h2>On this page</h2></aside>') for i in range(3)}
        self.assertEqual(self.scan_pages(pages), [])


    def test_h2_headings_have_at_most_eight_words(self):
        self.assert_rule('LS06', self.page(body=self.BODY.replace(
            'Checks reject repeated mistakes', 'You test one useful boundary before trusting every result')),
            self.page(body=self.BODY.replace('Checks reject repeated mistakes',
                                            'You test one useful boundary before trusting results')))
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(body=self.BODY.replace(
            'Checks reject repeated mistakes', "You check the agent’s well-defined boundary before trusting"))}), [])


    def test_h2_headings_include_a_declared_plain_verb(self):
        for label in ['Sources', 'Useful evidence and examples', 'Reliable boundaries',
                      'Recurring mistakes', 'The latest processing settings']:
            self.assert_rule('LS07', self.page(body=self.BODY.replace(
                'Checks reject repeated mistakes', label)))
        for label in ['The example shows the boundary', 'A check that actually shipped',
                      'You can keep valid work', 'Failures reveal the boundary']:
            self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(body=self.BODY.replace(
                'Checks reject repeated mistakes', label))}), [])


    def test_each_h2_section_has_three_complete_sentences(self):
        for short in ['<p>One sentence. Another sentence.</p>',
                      '<p>One sentence. Another sentence. An unfinished fragment</p>',
                      '<p>Dr. Smith tested version 2.5. The case passed.</p>',
                      '<p>One. Two.</p><pre>Fake. Extra. Prose.</pre>',
                      '<p>One. Two.</p><p hidden>Fake. Extra. Prose.</p>',
                      '<p>One. Two.</p><h3>Fake. Extra. Prose.</h3>',
                      '<ul><li><p>Only one sentence.</p></li></ul>']:
            self.assert_rule('LS08', self.page(body='<h2>Checks reject errors</h2>' + short + self.BODY))
        # The closing sentence cannot pad the sources section's two sentences.
        self.assert_rule('LS08', self.page(sources=self.SOURCES.replace(
            ' It does not prove wider coverage.', '')))
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(body=
            '<h2>Checks reject errors</h2><ul><li>One.</li><li>Two.</li><li>Three.</li></ul>'
            + self.BODY)}), [])


    def test_sources_section_has_one_nonempty_local_citation_list(self):
        for sources in ['', self.SOURCES.replace('id="sources"', 'id="other"'),
                        self.SOURCES.replace('id="citations"', 'id="other"'),
                        self.SOURCES.replace('<ol id="citations">', '<div id="citations">').replace('</ol>', '</div>'),
                        self.SOURCES.replace('<li id="cite-demo">', '<li>'),
                        self.SOURCES.replace('<li id="cite-demo">', '<li id="demo">'),
                        re.sub(r'<li.*?</li>', '', self.SOURCES),
                        self.SOURCES + self.SOURCES,
                        self.SOURCES + self.BODY]:
            self.assert_rule('LS09', self.page(sources=sources))
        self.assert_rule('LS09', self.page(body=self.SOURCES + self.BODY,
                                          sources='<h2 id="sources">Sources show the limit</h2>'
                                                  '<p>One. Two. Three.</p>'))
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(sources=self.SOURCES.replace(
            '<ol', '<ul').replace('</ol>', '</ul>'))}), [])


    def test_source_links_resolve_only_to_qualified_citation_entries(self):
        for href in ['#missing', '#sources', 'other.html#cite-demo',
                     'https://example.test/unlisted#part', 'https://example.test/demo']:
            self.assert_rule('LS10', self.page(sources=self.SOURCES.replace(
                'The source records the failure.',
                f'The source records the <a href="{href}">failure</a>.')))
        for href in ['https://example.test/demo', 'https://example.test/demo#',
                     'https://example.test/demo?t=later', 'https://example.test/demo?t=',
                     'javascript:alert(1)', '/local#part', 'https:///demo#part']:
            self.assert_rule('LS10', self.page(sources=self.SOURCES.replace(
                'https://example.test/demo#boundary', href)))
        self.assert_rule('LS10', self.page(sources=re.sub(
            r'<a href="https:.*?</a>', 'An entry without evidence', self.SOURCES)))
        for href in ['#cite-demo', 'https://example.test/demo#boundary']:
            self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(sources=self.SOURCES.replace(
                'The source records the failure.',
                f'The source records the <a href="{href}">failure</a>.'))}), [])
        for href in ['https://example.test/watch?v=demo&amp;t=482s',
                     'https://example.test/watch?start=0',
                     'https://example.test/watch?t=1h2m3s']:
            self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(sources=self.SOURCES.replace(
                'https://example.test/demo#boundary', href))}), [])


    def test_inline_citations_exist_and_resolve_to_the_page_list(self):
        for body in [self.BODY.replace('<a href="#cite-demo">at the source</a>', 'at the source'),
                     self.BODY.replace('#cite-demo', '#cite-missing'),
                     self.BODY.replace('#cite-demo', '#sources')]:
            self.assert_rule('LS11', self.page(body=body))
        self.assert_rule('LS11', self.page(body=self.BODY.replace('#cite-demo', '#cite-outside')
                         + '<span id="cite-outside"></span>'))
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(body=self.BODY.replace(
            '#cite-demo', '#cite%2Ddemo'))}), [])


    def test_article_ends_with_one_single_sentence_action_paragraph(self):
        for close in ['', '<p>Test one case.</p>',
                      '<p id="next-action">Test one case. Then test another.</p>',
                      '<p id="next-action"></p>',
                      '<p id="next-action">An unfinished action</p>',
                      self.CLOSE + self.CLOSE,
                      self.CLOSE + '<p>Read something else.</p>',
                      '<p>Take another action.</p>' + self.CLOSE,
                      '<div id="next-action">Test one case.</div>',
                      self.CLOSE + 'Trailing unwrapped text.',
                      self.CLOSE + '<img src="extra.png" alt="Extra">',
                      '<ul><li>' + self.CLOSE + '</li></ul>']:
            self.assert_rule('LS12', self.page(close=close))
        self.assert_rule('LS12', self.page(body=self.BODY + self.CLOSE, close=''))
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(close=
            '<p id="next-action">Test <strong>one case</strong>.</p>').replace(
            '</article>', '</article><nav><p>Next lesson</p></nav>')}), [])



    def test_section_counts_ignore_article_chrome_without_losing_nested_list_prose(self):
        bad = self.page(body='<h2>Checks reject errors</h2><p>One. Two.</p>'
                        '<nav><p>Fake third sentence.</p></nav>' + self.BODY)
        self.assert_rule('LS08', bad)
        good = self.page(body='<h2>Checks reject errors</h2>'
                        '<ul><li>A parent sentence.<ul><li>A child sentence.</li>'
                        '<li>Another child sentence.</li></ul></li></ul>' + self.BODY)
        self.assertEqual(self.scan_pages({'lessons/demo.html': good}), [])
        # Nested page tools are not authored section headings.
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page().replace(
            '<article>', '<article><aside><h2>On this page</h2><p>Read here.</p></aside>')}), [])


    def test_closing_cannot_hide_unwrapped_extra_text_or_broken_citations(self):
        self.assert_rule('LS12', self.page(close='Take another action. ' + self.CLOSE))
        self.assert_rule('LS11', self.page(close=self.CLOSE.replace(
            'one repeated mistake', '<a href="#cite-missing">one repeated mistake</a>')))
        self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(close=self.CLOSE.replace(
            'one repeated mistake', '<a href="#cite-demo">one repeated mistake</a>'))}), [])


    def test_verb_vocabulary_accepts_plain_verbs_observed_in_current_headings(self):
        # Inspection found these valid verbs missing from the initial vocabulary.
        # Acceptance here does not certify the rest of each heading's grammar.
        for heading in ['Derive each consumer from one contract', 'Reuse before building',
                        'Map errors to actions', "The sponsor's speed claims remain unverified.",
                        'One concrete way to close it', 'The gap Theo hit',
                        'What type-safe composition feels like', 'What belongs in an instruction file',
                        # Phase 4 writers used these plain verbs; observed 2026-09-13.
                        'Readable evidence sharpens the diagnosis', 'Focused context exposes the route',
                        'User journeys expose hidden failures', 'Your project supplies the authority',
                        'One contract guides every consumer', 'Existing rules receive the constraint first']:
            with self.subTest(heading=heading):
                self.assertEqual(self.scan_pages({'lessons/demo.html': self.page(body=self.BODY.replace(
                    'Checks reject repeated mistakes', heading))}), [])
        self.assert_rule('LS07', self.page(body=self.BODY.replace(
            'Checks reject repeated mistakes', 'An arbitrary noun phrase')))


class LessonStandardEntryTest(unittest.TestCase):
    def test_default_check_enforces_lessons_and_flag_is_compatible(self):
        helper = CheckerAtRealEntryTest()
        with temp_root('lesson-cli-') as root:
            helper.copy_public_inputs(REPO, root, include_public=True)
            page = root / 'public/lessons/recurring-mistakes.html'
            page.write_text(page.read_text().replace('<article>', '<div>').replace('</article>', '</div>'))
            for args in [[], ['--lessons']]:
                result = subprocess.run([sys.executable, 'build/check.py'] + args,
                                        cwd=root, capture_output=True, text=True, timeout=300)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('LS01', result.stdout)
                self.assertIn('lessons/recurring-mistakes.html', result.stdout)

    def test_layout_accepts_registered_standard_and_harness_files_only(self):
        checker = load_checker()
        with temp_root('standard-layout-') as root:
            checker.ROOT = root
            control = root / 'control'
            control.mkdir()
            for name in ['lesson-standard.md', 'harness.md', 'harness-state.json']:
                (control / name).write_text('Registered control document')
            # Exercise source-archive layout rather than a temporary Git index.
            with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, ['git'])):
                checker.layout()
            self.assertEqual(checker.failures, [])
            (control / 'unregistered.md').write_text('Must still fail')
            with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, ['git'])):
                checker.layout()
            self.assertTrue(any('unregistered.md' in f for f in checker.failures))


    def test_layout_and_compatible_flag_remain_source_only(self):
        with temp_root('lesson-flags-') as root:
            CheckerAtRealEntryTest().copy_public_inputs(REPO, root, include_public=False)
            result = subprocess.run([sys.executable, 'build/check.py', '--layout', '--lessons'],
                                    cwd=root, capture_output=True, text=True, timeout=300)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('PASS: source layout', result.stdout)


if __name__ == '__main__':
    unittest.main()
