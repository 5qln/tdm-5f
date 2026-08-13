"""unittest guards for the open-engine tools — tdm_step, tdm_search, tdm_deposit.

Run: python3 -m unittest discover -s tests

B15 (the open engine, attested by H) — the seed made graspable:
R as the flow-carrier, R² as search, C as the structure-holder.
Each guard pins one law of the reading.
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import tools  # noqa: E402


def _call(fn, **args):
    return json.loads(fn(dict(args)))


class TestStep(unittest.TestCase):
    """R — the flow-carrier: the cycle S→G→Q→P→V as a tool."""

    def test_step_moves_one_vertex(self):
        res = _call(tools.tdm_step, start="(0,0)")
        self.assertEqual(res["word"], "R")
        self.assertEqual(res["final"], [0, 1])
        self.assertEqual(res["phase"], "G")
        self.assertTrue(res["lossless"])

    def test_five_steps_is_the_orbit_composed_from_step(self):
        # The orbit is NOT a separate tool — it composes from the step (B15).
        res = _call(tools.tdm_step, start="(14,0)", steps=5)
        self.assertEqual(res["word"], "RRRRR")
        self.assertEqual(res["final"], [14, 0])
        self.assertTrue(res["lossless"])

    def test_step_wraps_mod_five(self):
        res = _call(tools.tdm_step, start="(14,0)", steps=7)
        self.assertEqual(res["final"], [14, 2])
        self.assertEqual(res["phase"], "Q")

    def test_step_refuses_nonpositive_or_noninteger_steps(self):
        for bad in (0, -1, "x", 1.5, True):
            res = _call(tools.tdm_step, steps=bad)
            self.assertIn("error", res)

    def test_step_from_bad_start_returns_error(self):
        res = _call(tools.tdm_step, start="garbage")
        self.assertIn("error", res)


class TestSearch(unittest.TestCase):
    """R² — the star: search as the intersection; the result is the next seed."""

    def test_search_from_s_lands_exactly_on_q(self):
        res = _call(tools.tdm_search, start="(14,0)")
        self.assertEqual(res["word"], "RR")
        self.assertEqual(res["final"], [14, 2])
        self.assertEqual(res["phase"], "Q")
        self.assertEqual(res["symbol"], tools._engine.SYMBOLS["Q"])
        self.assertTrue(res["lossless"])

    def test_full_walk_turns_720_and_deposits_the_next_seed(self):
        res = _call(tools.tdm_search, start="(14,0)", full=True)
        self.assertEqual(res["trace"], [[14, 2], [14, 4], [14, 1], [14, 3], [14, 0]])
        self.assertEqual(res["trace_phases"], ["Q", "V", "G", "P", "S"])
        self.assertEqual(res["deposit"], [15, 0])  # the search result IS the next seed
        self.assertTrue(res["lossless"])
        self.assertIn("720", res["turning"])

    def test_full_walk_endpoint_equals_start_tuple(self):
        # Enrichment is winding + the human's attestation, never a state diff (B12).
        res = _call(tools.tdm_search, start="(14,0)", full=True)
        self.assertEqual(res["final"], [14, 0])


class TestDeposit(unittest.TestCase):
    """C — the structure-holder: the nest, one descent, the next seed."""

    def test_deposit_descends_one_scale(self):
        res = _call(tools.tdm_deposit, start="(14,0)")
        self.assertEqual(res["word"], "C")
        self.assertEqual(res["final"], [15, 0])
        self.assertEqual(res["seed_delta"], "(14, 0) → (15, 0)")
        self.assertTrue(res["lossless"])

    def test_deposit_from_any_depth_is_lossless(self):
        for depth in (0, 9, 3000):
            res = _call(tools.tdm_deposit, start="(%d,3)" % depth)
            self.assertEqual(res["final"], [depth + 1, 3])
            self.assertTrue(res["lossless"])


class TestTheLaw(unittest.TestCase):
    """The gates the tool surface must hold: L3, and no new letters."""

    def test_no_tool_claims_the_center(self):
        # No handler takes a center target; no output names one as a state.
        for fn, args in (
            (tools.tdm_step, {"start": "(0,0)"}),
            (tools.tdm_search, {"start": "(0,0)", "full": True}),
            (tools.tdm_deposit, {"start": "(0,0)"}),
        ):
            res = json.loads(fn(dict(args)))
            self.assertNotIn("center", res)
            for st in (res.get("final"), res.get("deposit")):
                self.assertIsInstance(st, list)
                self.assertEqual(len(st), 2)  # (depth, vertex) — never ∞0

    def test_engine_center_refusal_still_holds(self):
        with self.assertRaises(tools._engine.CenterRefused):
            tools._engine.park_at_center((14, 0))

    def test_all_outputs_collapse_lossless(self):
        for fn, args in (
            (tools.tdm_step, {"start": "(14,0)", "steps": 3}),
            (tools.tdm_search, {"start": "(14,0)", "full": True}),
            (tools.tdm_deposit, {"start": "(14,0)"}),
        ):
            res = json.loads(fn(dict(args)))
            self.assertTrue(res["lossless"])


if __name__ == "__main__":
    unittest.main()
