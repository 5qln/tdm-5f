"""unittest guards for the tdm_verify tool — run: python3 -m unittest discover -s tests"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import tools  # noqa: E402


class TestVerifier(unittest.TestCase):
    def test_valid_words_pass_all_three_checks(self):
        for word in ("", "R", "RRRRR", "C", "RCRCR", "R" * 10 + "C"):
            final, lossless, new = tools.verify(word, (0, 0))
            self.assertTrue(lossless)
            self.assertTrue(new)

    def test_new_generator_refused(self):
        with self.assertRaises(AssertionError):
            tools.verify("X", (0, 0))
        with self.assertRaises(AssertionError):
            tools.verify("RCR-X", (0, 0))

    def test_handler_returns_json_for_valid_word(self):
        out = tools.tdm_verify({"word": "RCRCR", "start": "(0,0)"})
        res = json.loads(out)
        self.assertTrue(res["minimal"])
        self.assertIsNone(res["refused"])
        self.assertTrue(res["lossless"])
        self.assertTrue(res["new"])
        self.assertEqual(res["final"], [2, 3])   # R C R C R from (0, 0)

    def test_handler_returns_refusal_json_for_new_generator(self):
        out = tools.tdm_verify({"word": "XR"})
        res = json.loads(out)
        self.assertFalse(res["minimal"])
        self.assertIn("NEW GENERATOR", res["refused"])

    def test_handler_error_on_bad_start(self):
        out = tools.tdm_verify({"word": "C", "start": "garbage"})
        res = json.loads(out)
        self.assertIn("error", res)

    def test_deep_collapse_still_lossless(self):
        final, lossless, new = tools.verify("RCRCR" * 400, (0, 0))
        self.assertTrue(lossless)


if __name__ == "__main__":
    unittest.main()
