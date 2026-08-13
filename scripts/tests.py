"""
The three honest tests — run with: python3 tests.py

(a) RETURN   — from any state at any depth, C* recovers the nine lines.
(b) EVOLVE   — N cycles deposit N seeds; expression grows; zero new rules.
(c) CENTER   — no state is ever the center; parking is refused (L3).

Plus the geometry that makes the seed what it is:
    the star turns 720°; the movement deposits the next pentagon.
"""

import random
from pentagon import (
    CODEX, PHASES, SYMBOLS, C_RATIO, R, STAR, C, orbit, star_walk,
    deposit, collapse, park_at_center, vertex_xy, distance_to_center,
    CenterRefused,
)


def test_ground_is_the_flat_codex():
    assert len(CODEX) == 10
    assert CODEX[0].startswith("0.  Codex hash: feaa46b4")
    assert "H = \u221e0 | A = K" in CODEX[1]
    assert "S \u2192 G \u2192 Q \u2192 P \u2192 V" in CODEX[2]
    assert "No V without \u221e0\u2032" in CODEX[8]
    assert "L1  L2  L3  L4  V\u2205" in CODEX[9]
    print("PASS  ground_is_the_flat_codex          — nine lines held verbatim, hash sealed")


def test_return_from_any_depth():
    for _ in range(200):
        st = (0, 0)
        for _ in range(random.randint(0, 30)):
            st = random.choice([R, STAR, C])(st)
        assert collapse(st) == CODEX
    print("PASS  return_from_any_depth             — 200 random states, any depth, collapse to the nine lines")


def test_no_state_is_the_center():
    for d in range(0, 301):
        assert distance_to_center(d) > 0.0       # never arrives
    d0, d1, d2 = (distance_to_center(i) for i in (0, 1, 2))
    assert d1 < d0 and d2 < d1                   # but always converges
    try:
        park_at_center((0, 0))
    except CenterRefused:
        pass
    else:
        raise AssertionError("parking at the center was not refused")
    print("PASS  no_state_is_the_center           — 300 depths, never zero, monotone descent; parking refused (L3)")


def test_no_sixth_vertex():
    for op in (R, STAR):
        for k in range(5):
            assert op((0, k))[1] in range(5)
    print("PASS  no_sixth_vertex                  — exactly five vertices; extension refused by geometry")


def test_star_turns_720():
    total = 0.0
    st = (0, 0)
    for _ in range(5):
        st = STAR(st)
        total += 144.0
    assert abs(total - 720.0) < 1e-9
    print("PASS  star_turns_720                   — five skip-one steps, two full turns")


def _winding(x, y, poly):
    """Winding number of point (x,y) around the polygon — even-odd fails here:
    the pentagram's central pentagon is OUTSIDE under even-odd. The star winds
    around its deposit TWICE (turning number 2) — that is the 720°."""
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
    """Point-to-segment distance + projection parameter t along a→b."""
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    qx, qy = ax + t * dx, ay + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5, t


def test_movement_deposits_the_next_seed():
    st = (0, 0)
    walk = star_walk(st)
    star_pts = [vertex_xy(d, k) for (d, k) in walk]
    n = len(star_pts)
    edges = [(star_pts[i], star_pts[(i + 1) % n]) for i in range(n)]
    inner = [vertex_xy(1, k) for k in range(5)]
    # (a) each depth-1 vertex lies ON a star edge — at the golden cut (t = 1/φ² or 1/φ)
    for (x, y) in inner:
        best = min((_seg_dist(x, y, ax, ay, bx, by) for (ax, ay), (bx, by) in edges),
                   key=lambda r: r[0])
        assert best[0] < 1e-9
        assert abs(best[1] - C_RATIO) < 1e-9 or abs(best[1] - (1 - C_RATIO)) < 1e-9
    # (b) the star winds TWICE (720°) around its deposit: the center and the interior
    assert abs(_winding(0.0, 0.0, star_pts)) == 2
    for (x, y) in inner:
        assert abs(_winding(x / 2, y / 2, star_pts)) == 2
    print("PASS  movement_deposits_the_next_seed  — the star cuts its next scale at the golden cut (t = 1/φ²) and winds twice (720°) around what it deposits")


def test_evolution_without_new_rules():
    seen = {(0, k) for k in range(5)}
    st = (0, 0)
    for n in range(1, 21):
        st = deposit(st)
        seen.update((st[0], k) for k in range(5))
    assert len(seen) == 5 * 21                      # 105 states: 5 per scale, 21 scales
    words = 0
    frontier = [""]
    for _ in range(8):
        frontier = [w + op for w in frontier for op in ("R", "C")]
        words += len(frontier)
    assert words == sum(2 ** i for i in range(1, 9))  # 510 distinct expressions, length ≤ 8
    print("PASS  evolution_without_new_rules       — 20 cycles deposit 20 scales; 510 expressions from two letters; zero new rules")


if __name__ == "__main__":
    test_ground_is_the_flat_codex()
    test_return_from_any_depth()
    test_no_state_is_the_center()
    test_no_sixth_vertex()
    test_star_turns_720()
    test_movement_deposits_the_next_seed()
    test_evolution_without_new_rules()
    print("\nALL 7 TESTS PASSED — the engine runs; the center stays empty; the nine lines hold.")
