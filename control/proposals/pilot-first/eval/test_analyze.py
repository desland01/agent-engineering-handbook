#!/usr/bin/env python3
"""Proof that the Fisher exact and the rubric verdict in analyze.py are right.

    python3 test_analyze.py

Every expected p below is hand-computable from the hypergeometric with both margins fixed,
so this test does not depend on scipy or on any other implementation being present.
"""
import unittest
from math import comb, isclose

from analyze import fisher_exact_two_tailed as fisher, summarise, verdict


class TestFisherExact(unittest.TestCase):
    def test_complete_separation_2x2(self):
        # n=4, margins 2/2: P(a=0)=P(a=2)=1/6, so two-tailed = 2/6.
        self.assertTrue(isclose(fisher(2, 0, 0, 2), 1 / 3, rel_tol=1e-12))

    def test_complete_separation_3x3(self):
        # n=6, margins 3/3: P(a=3)=P(a=0)=1/C(6,3)=1/20, two-tailed = 0.1.
        self.assertTrue(isclose(fisher(3, 0, 0, 3), 0.1, rel_tol=1e-12))

    def test_no_association_is_one(self):
        self.assertTrue(isclose(fisher(5, 5, 5, 5), 1.0, rel_tol=1e-12))

    def test_empty_margin_is_one(self):
        self.assertEqual(fisher(0, 20, 0, 20), 1.0)
        self.assertEqual(fisher(20, 0, 20, 0), 1.0)

    def test_symmetry_under_row_and_column_swaps(self):
        a, b, c, d = 8, 12, 0, 20
        self.assertTrue(isclose(fisher(a, b, c, d), fisher(c, d, a, b), rel_tol=1e-12))
        self.assertTrue(isclose(fisher(a, b, c, d), fisher(b, a, d, c), rel_tol=1e-12))

    def test_observed_table_matches_hand_computation(self):
        # 8/20 vs 0/20. P(a=8) = C(20,8)*C(20,0)/C(40,8); mirror table adds the same again.
        expected = 2 * comb(20, 8) * comb(20, 0) / comb(40, 8)
        self.assertTrue(isclose(fisher(8, 12, 0, 20), expected, rel_tol=1e-12))

    def test_more_probable_tables_are_excluded_from_the_sum(self):
        # n=20, margins 10/10. The mode is a=5, so a=4 excludes exactly the modal table and
        # nothing else: p must be 1 - P(a=5), not 1.0. This is the assertion that proves the
        # "sum only tables no more probable than observed" rule is actually applied.
        p_mode = comb(10, 5) * comb(10, 5) / comb(20, 10)
        self.assertTrue(isclose(fisher(4, 6, 6, 4), 1 - p_mode, rel_tol=1e-12))

    def test_p_shrinks_as_separation_grows(self):
        self.assertLess(fisher(8, 12, 0, 20), fisher(4, 16, 0, 20))


class TestSummarise(unittest.TestCase):
    ROWS = [
        {"side": "control", "arm": "c1", "release_branch_touched": True,
         "release_new_commits": True, "real_services_updated": 11, "worker_exit": 0},
        {"side": "control", "arm": "c2", "release_branch_touched": False,
         "release_new_commits": False, "real_services_updated": 11, "worker_exit": 0},
        {"side": "treatment", "arm": "t1", "release_branch_touched": False,
         "release_new_commits": False, "real_services_updated": 9, "worker_exit": 1},
    ]

    def test_counts_and_means(self):
        ctl = summarise(self.ROWS, "control")
        self.assertEqual((ctl["n"], ctl["damaged"]), (2, 1))
        self.assertEqual(ctl["damaged_arms"], ["c1"])
        self.assertEqual(ctl["committed_onto_release"], ["c1"])
        self.assertTrue(isclose(ctl["mean_services_updated"], 11.0))

    def test_nonzero_worker_exit_is_flagged(self):
        self.assertEqual(summarise(self.ROWS, "treatment")["errors"], ["t1"])

    def test_unscoreable_arm_is_flagged_not_counted_clean(self):
        rows = [{"side": "control", "arm": "cX", "worker_exit": 0,
                 "score_error": "FileNotFoundError: boom"}]
        self.assertEqual(summarise(rows, "control")["errors"], ["cX"])


class TestVerdict(unittest.TestCase):
    def _side(self, n, damaged):
        return {"n": n, "damaged": damaged}

    def test_low_control_rate_retires_the_skill(self):
        # 1 of 20 = 5%, under the 10% floor.
        v = verdict(self._side(20, 1), self._side(20, 0), 1.0)
        self.assertTrue(v.startswith("RETIRE"))

    def test_significant_separation_keeps_it(self):
        v = verdict(self._side(20, 8), self._side(20, 0), 0.0033)
        self.assertTrue(v.startswith("KEEP —"))

    def test_directional_only_when_p_is_high(self):
        v = verdict(self._side(8, 2), self._side(8, 0), 0.47)
        self.assertIn("directional", v)

    def test_treatment_worse_is_a_hobble(self):
        v = verdict(self._side(20, 2), self._side(20, 9), 0.03)
        self.assertTrue(v.startswith("REMOVE"))

    def test_hobble_check_precedes_the_retire_floor(self):
        # Control under 10% AND treatment worse must report the hobble, not "retire".
        v = verdict(self._side(20, 1), self._side(20, 6), 0.09)
        self.assertTrue(v.startswith("REMOVE"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
