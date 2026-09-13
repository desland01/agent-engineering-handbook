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
    'missing-tools', 'useful-instructions', 'fresh-agent', 'shared-contracts',
    'codebase-navigation', 'better-environments',
]


def load_checker():
    spec = importlib.util.spec_from_file_location('handbook_check', Path(__file__).with_name('check.py'))
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    checker.failures = []
    return checker


class CatalogAtRealEntryTest(unittest.TestCase):
    """The reviewed catalog seam must accept the actual accepted tree."""

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


class CheckerAtRealEntryTest(unittest.TestCase):
    """The checker's independent manifest read and its bad-case coverage."""

    def test_problem_picker_labels_destinations_without_row_numbers(self):
        text = (REPO / 'public/index.html').read_text()
        panel = re.search(r'<div class="pick">(.*?)</div>\s*<figure class="hero-figure"', text, re.S).group(1)
        self.assertNotIn('class="ix"', panel)
        self.assertEqual(panel.count('<li>'), 8)
        self.assertEqual(len(re.findall(r'<span class="n">Lesson \d+</span>', panel)), 7)
        self.assertIn('<span class="n">Guide 12</span>', panel)
        self.assertIn('lessons/prove-it-works.html', panel)
        self.assertIn('guides/12-artifact-identity-and-recovery.html', panel)
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

    def test_tampered_alias_canonical_fails_the_full_check(self):
        """A legacy alias whose canonical points at itself must fail the real
        checker end to end, naming the alias."""
        with temp_root('check-') as tmp:
            self.copy_public_inputs(REPO, tmp, include_public=True)
            self.assert_no_private_entries(tmp)
            alias = tmp / 'public/ideas/01-ci-feedback-loop.html'
            text = alias.read_text()
            mutated = text.replace(
                'href="https://agent-engineering-handbook.dev/lessons/ci-feedback.html"',
                'href="https://agent-engineering-handbook.dev/ideas/01-ci-feedback-loop.html"')
            self.assertNotEqual(mutated, text, 'fixture did not change the canonical')
            alias.write_text(mutated)
            result = subprocess.run([sys.executable, 'build/check.py'], cwd=tmp,
                                    capture_output=True, text=True, timeout=300)
            self.assertNotEqual(result.returncode, 0,
                                'the tampered alias canonical passed the check')
            self.assertIn('ideas/01-ci-feedback-loop.html', result.stdout)

    def test_legacy_fragments_land_in_matching_lesson_regions(self):
        for page in (REPO / 'public/lessons').glob('*.html'):
            text = page.read_text()
            article = re.search(r'<article>(.*?)</article>', text, re.S).group(1)
            self.assertIn('id="useful"', article, page.name)
            self.assertRegex(article, r'id="apply"[^>]*></span>\s*<(?:ol|pre)\b', page.name)
            self.assertRegex(article, r'id="qualification"[^>]*></span>\s*<h2', page.name)

    def test_new_skill_pages_link_their_original_research_guides(self):
        expected = {'agent-output-verification': ['09', '13'],
                    'agent-artifact-recovery': ['12'],
                    'agent-contract-consistency': ['08', '11']}
        for name, guides in expected.items():
            text = (REPO / 'public/skills' / name / 'index.html').read_text()
            for guide in guides:
                self.assertIn(f'href="../../guides/{guide}-', text, name)
            deck = re.search(r'<p class="deck">(.*?)</p>', text, re.S).group(1)
            self.assertLess(len(deck.split()), 40, name)

    def test_legacy_index_share_url_matches_its_canonical(self):
        text = (REPO / 'public/ideas.html').read_text()
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


if __name__ == '__main__':
    unittest.main()
