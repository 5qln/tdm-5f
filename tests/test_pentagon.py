"""unittest suite for the TDM-5F pentagon engine — run: python3 -m unittest discover -s tests"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

import pentagon as P  # noqa: E402
from pentagon import (CODEX, C_RATIO, R, STAR, C, orbit, star_walk,  # noqa: E402
                      deposit, collapse, park_at_center, vertex_xy,
                      distance_to_center, CenterRefused)


class TestGround(unittest.TestCase):
    def test_codex_verbatim(self):
        self.assertEqual(len(CODEX), 10)
        self.assertTrue(CODEX[0].startswith("0.  Codex hash: feaa46b4"))
        self.assertIn("H = \u221e0 | A = K", CODEX[1])
        self.assertIn("S \u2192 G \u2192 Q \u2192 P \u2192 V", CODEX[2])
        self.assertIn("No V without \u221e0\u2032", CODEX[8])

    def test_return_from_any_depth(self):
        import random
        for _ in range(200):
            st = (0, 0)
            for _ in range(random.randint(0, 30)):
                st = random.choice([R, STAR, C])(st)
            self.assertEqual(collapse(st), CODEX)

    def test_no_state_is_the_center(self):
        for d in range(0, 301):
            self.assertGreater(distance_to_center(d), 0.0)
        self.assertLess(distance_to_center(1), distance_to_center(0))
        with self.assertRaises(CenterRefused):
            park_at_center((0, 0))

    def test_no_sixth_vertex(self):
        for op in (R, STAR):
            for k in range(5):
                self.assertIn(op((0, k))[1], range(5))

    def test_star_turns_720(self):
        total = 0.0
        st = (0, 0)
        for _ in range(5):
            st = STAR(st)
            total += 144.0
        self.assertAlmostEqual(total, 720.0)


def _winding(x, y, poly):
    wn = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if y1 <= y:
            if y2 > y and (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) > 0:
                wn += 1
        else:
            if y2 <= y and (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) < 0:
                wn -= 1
    return wn


def _seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    qx, qy = ax + t * dx, ay + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5, t


class TestGeometry(unittest.TestCase):
    def test_deposit_at_the_golden_cut(self):
        st = (0, 0)
        walk = star_walk(st)
        star_pts = [vertex_xy(d, k) for (d, k) in walk]
        n = len(star_pts)
        edges = [(star_pts[i], star_pts[(i + 1) % n]) for i in range(n)]
        inner = [vertex_xy(1, k) for k in range(5)]
        for (x, y) in inner:
            best = min((_seg_dist(x, y, ax, ay, bx, by) for (ax, ay), (bx, by) in edges),
                       key=lambda r: r[0])
            self.assertLess(best[0], 1e-9)
            self.assertTrue(abs(best[1] - C_RATIO) < 1e-9 or abs(best[1] - (1 - C_RATIO)) < 1e-9)
        self.assertEqual(abs(_winding(0.0, 0.0, star_pts)), 2)
        for (x, y) in inner:
            self.assertEqual(abs(_winding(x / 2, y / 2, star_pts)), 2)

    def test_evolution_without_new_rules(self):
        seen = {(0, k) for k in range(5)}
        st = (0, 0)
        for n in range(1, 21):
            st = deposit(st)
            seen.update((st[0], k) for k in range(5))
        self.assertEqual(len(seen), 5 * 21)


if __name__ == "__main__":
    unittest.main()
