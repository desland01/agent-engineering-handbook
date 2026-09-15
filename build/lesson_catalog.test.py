#!/usr/bin/env python3
"""Tests for build/lesson_catalog.py — the ten-lesson catalog seam.

Self-contained: every fixture is written into a temporary directory from
constants in this file. The approved lesson identity (ten IDs, their tip
mapping and their authored titles) is copied here from the approved manifest
as the independent source of truth the implementation must agree with, so no
test recomputes an expectation from the code it tests.

Run:  python3 build/lesson_catalog.test.py
"""
from pathlib import Path
import os
import json
import re
import shutil
import tempfile
import unittest

import lesson_catalog as lc

# The approved lesson identities, verbatim from the approved build/lessons.json.
# Fixed fixtures transcribed from the approved Phase 5 sitemap.
APPROVED = [('recurring-mistakes',
  1,
  'stop-repeat-work',
  'You turn repeated mistakes into reliable checks',
  ['tip-08-fix-class-loops', 'tip-19-custom-lint-economics']),
 ('ci-feedback',
  2,
  'stop-repeat-work',
  'You diagnose failed checks without copying logs',
  ['tip-01-ci-feedback-loop']),
 ('prove-it-works',
  3,
  'stop-repeat-work',
  'You test the result users actually need',
  ['tip-02-two-browser-e2e']),
 ('working-previews',
  4,
  'give-agents-what-they-need',
  'You give agents a working preview',
  ['tip-04-preview-environments']),
 ('missing-tools',
  5,
  'give-agents-what-they-need',
  'You make missing operations usable by agents',
  ['tip-05-custom-file-upload-skill', 'tip-06-skill-authoring-reward']),
 ('useful-instructions',
  6,
  'give-agents-what-they-need',
  'You write instructions that fix observed confusion',
  ['tip-09-domain-knowledge-as-infra',
   'tip-11-own-your-instructions',
   'tip-12-steering-pushback',
   'tip-14-zero-context-docs',
   'tip-15-minimal-context-calibration',
   'tip-16-steer-not-map']),
 ('shared-contracts',
  7,
  'keep-it-understandable',
  'You keep shared contracts consistent across layers',
  ['tip-13-type-safe-composition']),
 ('codebase-navigation',
  8,
  'keep-it-understandable',
  'You navigate unfamiliar code without guessing',
  ['tip-18-solo-onboarding']),
 ('resume-work',
  9,
  'keep-it-understandable',
  'You resume work without repeating completed steps',
  []),
 ('better-environments',
  10,
  'keep-it-understandable',
  'You remove obstacles for the next contributor',
  ['tip-03-automation-multiplies-agents',
   'tip-07-team-buy-in',
   'tip-10-newcomer-questions-signal',
   'tip-17-career-leverage'])]

SUMMARIES = {'recurring-mistakes': 'Catch a repeated mistake with a check that rejects it.',
 'ci-feedback': 'Give the agent access to the failed check and its logs.',
 'prove-it-works': 'Verify the real result, not just a successful command.',
 'working-previews': 'Make the running change reachable from the agent’s environment.',
 'missing-tools': 'Bridge a real capability gap with the smallest useful interface.',
 'useful-instructions': 'Put decisions where the next task can use them.',
 'shared-contracts': 'Keep the language, types and runtime boundary in agreement.',
 'codebase-navigation': 'Make the codebase understandable when you return to it.',
 'resume-work': 'Reuse finished work and resume only the missing stage.',
 'better-environments': 'Choose a recurring obstacle worth removing for future work.'}

GUIDES = {'recurring-mistakes': ['01'],
 'ci-feedback': ['04'],
 'prove-it-works': ['02', '09', '13'],
 'working-previews': ['03'],
 'missing-tools': ['06'],
 'useful-instructions': ['05'],
 'shared-contracts': ['08', '11'],
 'codebase-navigation': ['10'],
 'resume-work': ['12'],
 'better-environments': ['07']}

SKILLS = {'recurring-mistakes': ['agent-feedback-engineering'],
 'ci-feedback': ['agent-feedback-engineering'],
 'prove-it-works': ['agent-output-verification'],
 'working-previews': ['agent-ready-workspaces'],
 'missing-tools': ['agent-tool-adapters'],
 'useful-instructions': ['agent-context-calibration'],
 'shared-contracts': ['agent-contract-consistency'],
 'codebase-navigation': ['agent-context-calibration'],
 'resume-work': ['agent-artifact-recovery'],
 'better-environments': ['agent-feedback-engineering']}

LEGACY = {'recurring-mistakes': ['guides/01-recurring-failures.html',
                        'guides/01-recurring-failures.md',
                        'ideas/08-fix-class-loops.html',
                        'ideas/09-custom-lint-economics.html',
                        'ideas/09-custom-lint-economics',
                        'ideas/08-fix-class-loops'],
 'ci-feedback': ['guides/04-ci-feedback.html',
                 'guides/04-ci-feedback.md',
                 'ideas/01-ci-feedback-loop.html',
                 'ideas/01-ci-feedback-loop'],
 'prove-it-works': ['guides/02-critical-journey-tests.html',
                    'guides/02-critical-journey-tests.md',
                    'guides/09-verification-contracts.html',
                    'guides/09-verification-contracts.md',
                    'guides/13-layered-validation.html',
                    'guides/13-layered-validation.md',
                    'ideas/02-two-browser-e2e.html',
                    'ideas/02-two-browser-e2e'],
 'working-previews': ['guides/03-preview-workspaces.html',
                      'guides/03-preview-workspaces.md',
                      'ideas/04-preview-environments.html',
                      'ideas/04-preview-environments'],
 'missing-tools': ['guides/06-tool-adapters.html',
                   'guides/06-tool-adapters.md',
                   'ideas/05-custom-file-upload-skill.html',
                   'ideas/06-skill-authoring-reward.html',
                   'ideas/06-skill-authoring-reward',
                   'ideas/05-custom-file-upload-skill'],
 'useful-instructions': ['lessons/fresh-agent.html',
                         'lessons/fresh-agent.md',
                         'guides/05-knowledge-and-instructions.html',
                         'guides/05-knowledge-and-instructions.md',
                         'ideas/10-domain-knowledge-as-infra.html',
                         'ideas/12-own-your-instructions.html',
                         'ideas/13-steering-pushback.html',
                         'ideas/15-zero-context-docs.html',
                         'ideas/16-minimal-context-calibration.html',
                         'ideas/17-steer-not-map.html',
                         'ideas/17-steer-not-map',
                         'ideas/16-minimal-context-calibration',
                         'ideas/15-zero-context-docs',
                         'ideas/13-steering-pushback',
                         'ideas/12-own-your-instructions',
                         'ideas/10-domain-knowledge-as-infra'],
 'shared-contracts': ['guides/08-compose-contracts.html',
                      'guides/08-compose-contracts.md',
                      'guides/11-domain-language-and-agent-apis.html',
                      'guides/11-domain-language-and-agent-apis.md',
                      'ideas/14-type-safe-composition.html',
                      'ideas/14-type-safe-composition'],
 'codebase-navigation': ['guides/10-codebase-navigation-and-tooling.html',
                         'guides/10-codebase-navigation-and-tooling.md',
                         'ideas/19-solo-onboarding.html',
                         'ideas/19-solo-onboarding'],
 'resume-work': ['guides/12-artifact-identity-and-recovery.html',
                 'guides/12-artifact-identity-and-recovery.md'],
 'better-environments': ['guides/07-team-learning.html',
                         'guides/07-team-learning.md',
                         'ideas/03-automation-multiplies-agents.html',
                         'ideas/07-team-buy-in.html',
                         'ideas/11-newcomer-questions-signal.html',
                         'ideas/18-career-leverage.html',
                         'ideas/18-career-leverage',
                         'ideas/11-newcomer-questions-signal',
                         'ideas/07-team-buy-in',
                         'ideas/03-automation-multiplies-agents']}

# The nineteen original tip IDs in observed video order (start_seconds order);
# position gives the idea number that names its legacy path.
TIP_IDS_IN_VIDEO_ORDER = [
    'tip-01-ci-feedback-loop', 'tip-02-two-browser-e2e', 'tip-03-automation-multiplies-agents',
    'tip-04-preview-environments', 'tip-05-custom-file-upload-skill',
    'tip-06-skill-authoring-reward', 'tip-07-team-buy-in', 'tip-08-fix-class-loops',
    'tip-19-custom-lint-economics', 'tip-09-domain-knowledge-as-infra',
    'tip-10-newcomer-questions-signal', 'tip-11-own-your-instructions',
    'tip-12-steering-pushback', 'tip-13-type-safe-composition', 'tip-14-zero-context-docs',
    'tip-15-minimal-context-calibration', 'tip-16-steer-not-map', 'tip-17-career-leverage',
    'tip-18-solo-onboarding',
]

GUIDE_FILES = [
    '01-recurring-failures', '02-critical-journey-tests', '03-preview-workspaces',
    '04-ci-feedback', '05-knowledge-and-instructions', '06-tool-adapters',
    '07-team-learning', '08-compose-contracts', '09-verification-contracts',
    '10-codebase-navigation-and-tooling', '11-domain-language-and-agent-apis',
    '12-artifact-identity-and-recovery', '13-layered-validation',
]

LESSON_PROSE = (
    'You fix the same bug twice and the fix does not hold. Short answer: turn the '
    'correction into a check that rejects the mistake before it lands.\n\n'
    '## Why the fix does not stick\n\n'
    'A correction held in memory disappears with the next task. A check survives it. '
    'Write the failing case first, then keep the rule that caught it.\n\n'
    '## Try it\n\n'
    'Add the smallest check that fails on the repeated mistake, and run it on every '
    'change. This is an illustration of the source pattern, not a measured result.\n\n'
    '## Sources\n\n'
    'Original video segments and repository inspections cited in the lesson text.'
)


def _temp_root():
    """Keep every test effect inside the supplied workspace."""
    base = Path(__file__).resolve().parent.parent / '.scratch'
    base.mkdir(exist_ok=True)
    return Path(tempfile.mkdtemp(prefix='lesson-catalog-', dir=base))


class Fixture:
    """A disposable source tree with the approved manifest and lesson files."""

    def __init__(self):
        self.root = _temp_root()
        self.build = self.root / 'build'
        self.build.mkdir()
        (self.root / 'evidence').mkdir()
        (self.root / 'guides').mkdir()
        (self.root / 'skills').mkdir()
        (self.root / 'lessons').mkdir()
        self.tips = [{'id': tip_id, 'start_seconds': 100 + i * 30}
                     for i, tip_id in enumerate(TIP_IDS_IN_VIDEO_ORDER)]
        (self.root / 'evidence/video-tips.json').write_text(json.dumps(self.tips))
        for name in GUIDE_FILES:
            (self.root / f'guides/{name}.md').write_text(f'# {name}\n\nProse.\n')
        for skill in ['agent-feedback-engineering', 'agent-ready-workspaces',
                      'agent-context-calibration', 'agent-tool-adapters',
                      'agent-output-verification', 'agent-artifact-recovery',
                      'agent-contract-consistency']:
            d = self.root / 'skills' / skill
            d.mkdir()
            (d / 'SKILL.md').write_text('---\nname: x\n---\nBody.\n')
        self.manifest = {'version': 1, 'lessons': [self.record(i) for i in APPROVED],
                         'legacy_paths': ['README.html', 'guides.html', 'ideas.html', 'ideas']}
        self.write_manifest()
        for lesson_id, _, _, title, tips in APPROVED:
            self.write_lesson(lesson_id, title, tips)

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def record(self, item):
        lesson_id, order, chapter, title, tips = item
        return {
            'id': lesson_id, 'order': order, 'chapter': chapter, 'title': title,
            'summary': SUMMARIES[lesson_id], 'source': f'lessons/{lesson_id}.md',
            'tip_ids': list(tips), 'guide_ids': list(GUIDES[lesson_id]),
            'skill_ids': list(SKILLS[lesson_id]), 'legacy_paths': list(LEGACY[lesson_id]),
        }

    def write_manifest(self):
        (self.build / 'lessons.json').write_text(json.dumps(self.manifest))

    def write_lesson(self, lesson_id, title, tips, prose=LESSON_PROSE):
        anchors = '\n'.join(f'<span id="{tip}"></span>' for tip in tips)
        (self.root / f'lessons/{lesson_id}.md').write_text(
            f'# {title}\n\n{anchors}\n\n{prose}\n')

    def load(self):
        return lc.load_lessons(self.root)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)

    # ------------------------------------------------------------ good path
    def test_complete_manifest_loads_ten_lessons_in_order(self):
        lessons = self.fx.load()
        self.assertEqual([l['id'] for l in lessons], [i[0] for i in APPROVED])
        self.assertEqual([l['order'] for l in lessons], list(range(1, 11)))
        self.assertEqual([l['page'] for l in lessons],
                         [f'lessons/{i[0]}.html' for i in APPROVED])
        for lesson, (_, _, _, title, tips) in zip(lessons, APPROVED):
            self.assertEqual(lesson['title'], title)
            self.assertEqual(lesson['tip_ids'], tips)
            self.assertEqual(lesson['source'], f'lessons/{lesson["id"]}.md')

    def test_all_nineteen_source_ids_covered_exactly_once(self):
        lessons = self.fx.load()
        seen = [t for l in lessons for t in l['tip_ids']]
        self.assertEqual(sorted(seen), sorted(TIP_IDS_IN_VIDEO_ORDER))
        self.assertEqual(len(seen), len(set(seen)), 'a source tip is assigned twice')

    # ------------------------------------------------- manifest-level fails
    def test_missing_manifest_is_an_error_not_an_empty_list(self):
        (self.fx.build / 'lessons.json').unlink()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('lessons.json', str(cm.exception))

    def test_missing_evidence_file_is_an_error(self):
        (self.fx.root / 'evidence/video-tips.json').unlink()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('video-tips.json', str(cm.exception))

    def test_wrong_version_fails(self):
        self.fx.manifest['version'] = 2
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('version', str(cm.exception))

    def test_missing_lesson_record_fails(self):
        self.fx.manifest['lessons'].pop()
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('10', str(cm.exception))

    def test_duplicate_order_fails(self):
        self.fx.manifest['lessons'][1]['order'] = self.fx.manifest['lessons'][0]['order']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('order', str(cm.exception))

    def test_out_of_range_order_fails(self):
        self.fx.manifest['lessons'][0]['order'] = 11
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('order', str(cm.exception))

    def test_duplicate_id_fails(self):
        self.fx.manifest['lessons'][1]['id'] = self.fx.manifest['lessons'][0]['id']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('recurring-mistakes', str(cm.exception))

    def test_unsafe_slug_id_fails(self):
        self.fx.manifest['lessons'][0]['id'] = '../escape'
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('../escape', str(cm.exception))

    def test_source_mismatch_fails(self):
        self.fx.manifest['lessons'][0]['source'] = 'lessons/someone-else.md'
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('lessons/recurring-mistakes.md', str(cm.exception))

    def test_empty_title_fails(self):
        self.fx.manifest['lessons'][2]['title'] = ''
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('prove-it-works', str(cm.exception))

    def test_empty_summary_fails(self):
        self.fx.manifest['lessons'][2]['summary'] = '   '
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('prove-it-works', str(cm.exception))

    def test_empty_chapter_fails(self):
        self.fx.manifest['lessons'][2].pop('chapter')
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('prove-it-works', str(cm.exception))

    # ------------------------------------------------------------ tip fails
    def test_unknown_tip_id_fails(self):
        self.fx.manifest['lessons'][0]['tip_ids'] = ['tip-08-fix-class-loops', 'tip-99-made-up']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('tip-99-made-up', str(cm.exception))

    def test_tip_renamed_mapping_fails(self):
        # The approved mapping is fixed: lesson 2 must carry tip-01 and nothing else.
        self.fx.manifest['lessons'][1]['tip_ids'] = ['tip-08-fix-class-loops']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('ci-feedback', str(cm.exception))

    def test_duplicate_tip_across_lessons_fails(self):
        # The approved mapping assigns tip-08 once; moving it onto lesson 2 as
        # well is a reassignment and must fail, naming the affected tip.
        self.fx.manifest['lessons'][1]['tip_ids'] = ['tip-08-fix-class-loops']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('tip-08-fix-class-loops', str(cm.exception))

    def test_tip_missing_from_all_lessons_fails(self):
        self.fx.manifest['lessons'][1]['tip_ids'] = []
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('tip-01-ci-feedback-loop', str(cm.exception))

    # ---------------------------------------------------- guide/skill fails
    def test_unknown_guide_id_fails(self):
        self.fx.manifest['lessons'][0]['guide_ids'] = ['99']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('99', str(cm.exception))

    def test_non_two_digit_guide_id_fails(self):
        self.fx.manifest['lessons'][0]['guide_ids'] = ['1']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('1', str(cm.exception))

    def test_unknown_skill_name_fails(self):
        self.fx.manifest['lessons'][0]['skill_ids'] = ['someone-elses-skill']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('someone-elses-skill', str(cm.exception))

    def test_non_string_skill_id_element_fails(self):
        # A malformed skill_ids entry (an object/list) must be refused with the
        # actionable ValueError naming the entry, not an internal TypeError.
        self.fx.manifest['lessons'][0]['skill_ids'] = [{'name': 'agent-tool-adapters'}]
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('skill_ids', str(cm.exception))

    def test_nested_list_skill_id_element_fails(self):
        self.fx.manifest['lessons'][4]['skill_ids'] = [['agent-tool-adapters']]
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('skill_ids', str(cm.exception))

    def test_skill_directory_without_skill_md_fails(self):
        d = self.fx.root / 'skills/agent-tool-adapters'
        (d / 'SKILL.md').unlink()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('agent-tool-adapters', str(cm.exception))

    # ------------------------------------------------------- legacy path fails
    def test_legacy_path_mismatch_fails(self):
        self.fx.manifest['lessons'][0]['legacy_paths'] = ['ideas/08-fix-class-loops.html']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('ideas/09-custom-lint-economics.html', str(cm.exception))

    def test_duplicate_legacy_route_fails(self):
        self.fx.manifest['lessons'][1]['legacy_paths'] = ['ideas/08-fix-class-loops.html']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('ideas/08-fix-class-loops.html', str(cm.exception))

    def test_legacy_path_traversal_fails(self):
        self.fx.manifest['lessons'][1]['legacy_paths'] = ['../lessons/ci-feedback.html']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('traversal', str(cm.exception))

    def test_absolute_legacy_path_fails(self):
        self.fx.manifest['lessons'][1]['legacy_paths'] = ['/ideas/01-ci-feedback-loop.html']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('absolute', str(cm.exception))

    # ------------------------------------------------------ authored lesson fails
    def test_missing_lesson_file_fails(self):
        (self.fx.root / 'lessons/ci-feedback.md').unlink()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('lessons/ci-feedback.md', str(cm.exception))

    def test_empty_lesson_file_fails(self):
        (self.fx.root / 'lessons/ci-feedback.md').write_text('')
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('lessons/ci-feedback.md', str(cm.exception))

    def test_wrong_h1_fails(self):
        self.fx.write_lesson('ci-feedback', 'A different title',
                             self.fx.manifest['lessons'][1]['tip_ids'])
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('h1', str(cm.exception))

    def test_thin_prose_fails(self):
        self.fx.write_lesson('ci-feedback', APPROVED[1][3],
                             self.fx.manifest['lessons'][1]['tip_ids'], prose='Too short.')
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('prose', str(cm.exception))

    def test_reader_source_needs_no_video_apparatus(self):
        self.fx.write_lesson('recurring-mistakes', APPROVED[0][3], [])
        self.assertEqual(self.fx.load()[0]['id'], 'recurring-mistakes')

    def test_anchor_as_heading_id_is_accepted(self):
        lesson_id, _, _, title, tips = APPROVED[1]
        (self.fx.root / f'lessons/{lesson_id}.md').write_text(
            f'# {title}\n\n## The failed check <a id="{tips[0]}"></a>\n\n{LESSON_PROSE}\n')
        lessons = self.fx.load()
        self.assertEqual(lessons[1]['id'], lesson_id)

    # ------------------------------------------- regression: published catalog
    def test_linked_proposed_skill_without_directory_fails(self):
        # All seven linked skills must exist on disk with a SKILL.md; there is
        # no prepublication bypass for catalog loading.
        shutil.rmtree(self.fx.root / 'skills/agent-contract-consistency')
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('agent-contract-consistency', str(cm.exception))

    def test_legacy_routes_swapped_between_lessons_fails(self):
        # The same nineteen routes overall, but each must stay with the lesson
        # whose assigned tips they redirect from.
        a, b = self.fx.manifest['lessons'][0], self.fx.manifest['lessons'][1]
        a['legacy_paths'], b['legacy_paths'] = b['legacy_paths'], a['legacy_paths']
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('legacy paths', str(cm.exception))
        self.assertIn('recurring-mistakes', str(cm.exception))

    def test_missing_merged_guide_address_fails(self):
        self.fx.manifest['lessons'][8]['legacy_paths'].remove('guides/12-artifact-identity-and-recovery.md')
        self.fx.write_manifest()
        with self.assertRaisesRegex(ValueError, 'legacy paths'):
            self.fx.load()

    def test_single_quoted_exact_anchor_is_accepted(self):
        lesson_id, _, _, title, tips = APPROVED[1]
        (self.fx.root / f'lessons/{lesson_id}.md').write_text(
            f"# {title}\n\n<a id='{tips[0]}'></a>\n\n{LESSON_PROSE}\n")
        self.assertEqual(self.fx.load()[1]['id'], lesson_id)

    def test_guide_cannot_move_to_another_owner(self):
        self.fx.manifest['lessons'][8]['guide_ids'] = ['07']
        self.fx.write_manifest()
        with self.assertRaisesRegex(ValueError, 'approved unique ownership'):
            self.fx.load()

    def test_null_manifest_is_a_valueerror(self):
        (self.fx.build / 'lessons.json').write_text('null')
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('lessons.json', str(cm.exception))

    def test_list_manifest_is_a_valueerror(self):
        (self.fx.build / 'lessons.json').write_text('[]')
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('lessons.json', str(cm.exception))

    def test_boolean_version_fails(self):
        self.fx.manifest['version'] = True
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('version', str(cm.exception))

    def test_non_object_record_fails(self):
        self.fx.manifest['lessons'][3] = 'nope'
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('lessons.json', str(cm.exception))

    def test_non_object_tip_record_fails(self):
        tips = json.loads((self.fx.root / 'evidence/video-tips.json').read_text())
        tips[2] = 42
        (self.fx.root / 'evidence/video-tips.json').write_text(json.dumps(tips))
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('video-tips.json', str(cm.exception))

    def test_duplicate_source_record_fails(self):
        tips = json.loads((self.fx.root / 'evidence/video-tips.json').read_text())
        tips.append(dict(tips[0]))
        (self.fx.root / 'evidence/video-tips.json').write_text(json.dumps(tips))
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('tip-01-ci-feedback-loop', str(cm.exception))

    def test_invalid_start_seconds_fails(self):
        tips = json.loads((self.fx.root / 'evidence/video-tips.json').read_text())
        tips[4]['start_seconds'] = 'late'
        (self.fx.root / 'evidence/video-tips.json').write_text(json.dumps(tips))
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('start_seconds', str(cm.exception))

    def test_boolean_start_seconds_fails(self):
        tips = json.loads((self.fx.root / 'evidence/video-tips.json').read_text())
        tips[4]['start_seconds'] = True
        (self.fx.root / 'evidence/video-tips.json').write_text(json.dumps(tips))
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('start_seconds', str(cm.exception))

    def test_non_list_tip_ids_fails(self):
        self.fx.manifest['lessons'][5]['tip_ids'] = 'tip-16-steer-not-map'
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('tip_ids', str(cm.exception))

    def test_non_string_tip_id_element_fails(self):
        self.fx.manifest['lessons'][0]['tip_ids'] = ['tip-08-fix-class-loops', 19]
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('19', str(cm.exception))

    def test_loading_does_not_mutate_manifest(self):
        before = json.dumps(self.fx.manifest, sort_keys=True)
        self.fx.load()
        self.assertEqual(json.dumps(self.fx.manifest, sort_keys=True), before)

    # --------------------------------------------------- regression: chapters
    def test_unknown_chapter_fails(self):
        self.fx.manifest['lessons'][6]['chapter'] = 'misc-thoughts'
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('misc-thoughts', str(cm.exception))

    def test_chapter_whitespace_is_normalized_in_returned_record(self):
        # A manifest chapter with surrounding whitespace passes validation (it
        # strips to the approved group), so the returned record must carry the
        # normalized value equal to its approved renderer group.
        self.fx.manifest['lessons'][6]['chapter'] = '  keep-it-understandable\n'
        self.fx.write_manifest()
        lessons = self.fx.load()
        self.assertEqual(lessons[6]['chapter'], 'keep-it-understandable')

    def test_chapter_reassigned_between_declared_groups_fails(self):
        # The approved lesson-to-chapter mapping is fixed; moving a lesson into
        # a different declared group silently regroups it for readers.
        self.fx.manifest['lessons'][0]['chapter'] = 'keep-it-understandable'
        self.fx.write_manifest()
        with self.assertRaises(ValueError) as cm:
            self.fx.load()
        self.assertIn('recurring-mistakes', str(cm.exception))


class ReadMinutesTests(unittest.TestCase):
    def test_word_count_over_220_words_per_minute_rounds_up(self):
        text = ' '.join(['word'] * 441)
        self.assertEqual(lc.read_minutes(text), 3)  # 441/220 = 2.005 -> 3

    def test_short_text_is_at_least_one_minute(self):
        self.assertEqual(lc.read_minutes('one two three'), 1)
        self.assertEqual(lc.read_minutes(''), 1)

    def test_html_tags_and_link_urls_are_not_counted(self):
        tagged = '<p>' + ' '.join(['word'] * 10) + '</p>'
        self.assertEqual(lc.read_minutes(tagged), 1)
        with_links = '[' + ' '.join(['word'] * 5) + '](https://example.com/very/long/path)'
        self.assertEqual(lc.read_minutes(with_links), 1)
        self.assertEqual(lc.read_minutes('word ' * 220 + ' https://example.com/a/b/c'), 1)

    def test_exact_boundary_counts_as_one_minute(self):
        self.assertEqual(lc.read_minutes('word ' * 220), 1)


class ReadmeTableTests(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)
        self.lessons = self.fx.load()

    def test_table_links_each_source_with_title_and_summary_in_order(self):
        table = lc.readme_lessons_table(self.lessons)
        lines = table.splitlines()
        self.assertTrue(lines[0].startswith('|'))
        for line, lesson in zip(lines[2:], self.lessons):
            self.assertIn(f']({lesson["source"]})', line)
            self.assertIn(lesson['title'], line)
            self.assertIn(lesson['summary'], line)
        self.assertEqual(len(lines), 2 + len(self.lessons))

    def test_table_is_deterministic(self):
        self.assertEqual(lc.readme_lessons_table(self.lessons),
                         lc.readme_lessons_table(list(self.lessons)))


README_HEAD = '# Agent Engineering Handbook\n\nIntro prose.\n\n'
README_MARKED = (README_HEAD + '<!-- lessons:start -->\nold table\n<!-- lessons:end -->\n'
                 + '\n## More\n\nTail.\n')


class SyncReadmeTests(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)
        self.lessons = self.fx.load()
        self.table = lc.readme_lessons_table(self.lessons)

    def test_replaces_content_between_markers_and_returns_new_string(self):
        out = lc.sync_readme_lessons(README_MARKED, self.lessons)
        self.assertIn(self.table, out)
        self.assertNotIn('old table', out)
        self.assertTrue(out.startswith(README_HEAD))
        self.assertTrue(out.rstrip().endswith('Tail.'))
        # No filesystem writes happened.
        self.assertEqual(self.fx.manifest, json.loads(
            (self.fx.build / 'lessons.json').read_text()))

    def test_missing_markers_fail(self):
        with self.assertRaises(ValueError) as cm:
            lc.sync_readme_lessons(README_HEAD, self.lessons)
        self.assertIn('lessons:start', str(cm.exception))

    def test_duplicate_start_marker_fails(self):
        text = README_MARKED.replace('Intro prose.',
                                     'Intro prose.\n\n<!-- lessons:start -->\n')
        with self.assertRaises(ValueError) as cm:
            lc.sync_readme_lessons(text, self.lessons)
        self.assertIn('lessons:start', str(cm.exception))

    def test_reversed_markers_fail(self):
        text = README_MARKED.replace('<!-- lessons:start -->', '@@S@@').replace(
            '<!-- lessons:end -->', '@@E@@').replace('@@S@@', '<!-- lessons:end -->').replace(
            '@@E@@', '<!-- lessons:start -->')
        with self.assertRaises(ValueError) as cm:
            lc.sync_readme_lessons(text, self.lessons)
        self.assertIn('reversed', str(cm.exception))

    def test_check_mode_passes_when_content_matches(self):
        synced = lc.sync_readme_lessons(README_MARKED, self.lessons)
        self.assertEqual(lc.sync_readme_lessons(synced, self.lessons, check=True), synced)

    def test_check_mode_fails_on_drift_instead_of_mutating(self):
        with self.assertRaises(ValueError) as cm:
            lc.sync_readme_lessons(README_MARKED, self.lessons, check=True)
        self.assertIn('drift', str(cm.exception))

    def test_check_mode_passes_when_only_whitespace_around_markers_differs(self):
        text = README_MARKED.replace('<!-- lessons:start -->\n',
                                     '<!-- lessons:start -->\n\n')
        synced = lc.sync_readme_lessons(text, self.lessons)
        self.assertEqual(lc.sync_readme_lessons(synced, self.lessons, check=True), synced)


class IntegrationShapeTests(unittest.TestCase):
    def test_no_third_party_imports(self):
        source = (Path(lc.__file__).read_text())
        imports = set(re.findall(r'^(?:import|from)\s+([a-zA-Z_][\w.]*)', source, re.M))
        allowed = {'pathlib', 'json', 're', 'math'}
        self.assertEqual(imports - allowed, set(), 'standard library only')


if __name__ == '__main__':
    unittest.main()
