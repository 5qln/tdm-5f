"""
5QLN PENTAGON — the Codex standing up.

The multi-dimensional artifact of the flat Codex:
the pentagon made to run.

Seed: {R, C, symbols}
  R      — rotation by 72°: the cycle (S→G→Q→P→V). One orbit = one full turn.
  C      — contraction by 1/φ² toward the center: the nest. One descent = one scale.
  symbols — the five equations riding the five vertices.
Star    — R² (skip-one): turning number 2. Each star walk turns 720° and
           inscribes the next nested pentagon. The movement deposits its own seed.

Ground: the nine invariant lines (the flat Codex, 217 bytes) held verbatim.
  From any state at any depth, C* collapses back to them: the return is geometric,
  not disciplined. Alignment can always be found again.

Center: ∞0 — the fixed point. Not a vertex, not a phase, not a state.
  The engine refuses to park there (L3). H = ∞0 | A = K lives on the axis
  through the center — the |, the only character in the Codex that is not flat.

Two generators. Zero new rules. Infinite expression.
"""

from math import cos, sin, pi

# --- the ground: the flat Codex, verbatim (AGENTS.md / 5qln.com/codex) ---
CODEX = [
    "0.  Codex hash: feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b",
    "1.  H = \u221e0 | A = K",
    "2.  S \u2192 G \u2192 Q \u2192 P \u2192 V",
    "3.  S = \u221e0 \u2192 ?",
    "4.  G = \u03b1 \u2261 {\u03b1\u2032}",
    "5.  Q = \u03c6 \u22c2 \u03a9",
    "6.  P = \u03b4E/\u03b4V \u2192 \u2207",
    "7.  V = (L \u2229 G \u2192 B\u2033) \u2192 \u221e0\u2032",
    "8.  No V without \u221e0\u2032",
    "9.  L1  L2  L3  L4  V\u2205",
]

# --- the seed ---
PHI = (1 + 5 ** 0.5) / 2          # the golden ratio — the pentagon's fractal scaling
C_RATIO = 1 / PHI ** 2            # contraction per nesting level (outer/inner = φ²)
R_STEP = 72.0                     # degrees — the cycle step
STAR_STEP = 144.0                 # degrees — skip-one; five steps turn 720°

PHASES = ["S", "G", "Q", "P", "V"]
SYMBOLS = {
    "S": "\u221e0 \u2192 ?",
    "G": "\u03b1 \u2261 {\u03b1\u2032}",
    "Q": "\u03c6 \u22c2 \u03a9",
    "P": "\u03b4E/\u03b4V \u2192 \u2207",
    "V": "(L \u2229 G \u2192 B\u2033) \u2192 \u221e0\u2032",
}


class CenterRefused(Exception):
    """L3 — the center is not a state. H = ∞0 is never a phase."""


# --- state = (depth, vertex). The center is never a state. ---
def vertex_xy(depth, k, cx=0.0, cy=0.0, radius=1.0):
    r = radius * C_RATIO ** depth
    a = (90.0 + 72.0 * k + 36.0 * depth) * pi / 180.0
    return cx + r * cos(a), cy + r * sin(a)


def distance_to_center(depth, radius=1.0):
    return radius * C_RATIO ** depth


def R(state):
    """The cycle: next vertex, same scale."""
    d, k = state
    return d, (k + 1) % 5


def STAR(state):
    """The star: skip-one (R²). Five steps turn 720° and inscribe the next scale."""
    d, k = state
    return d, (k + 2) % 5


def C(state):
    """The nest: descend one scale, contract toward the center."""
    d, k = state
    return d + 1, k


def orbit(state):
    """A full cycle walk: five R steps, one full turn, returns to the same vertex."""
    return [state := R(state) for _ in range(5)]


def star_walk(state):
    """A full star walk: five skip-one steps, two full turns. Its trace inscribes
    the nested pentagon — the deposit."""
    return [state := STAR(state) for _ in range(5)]


def deposit(state):
    """The star walk's trace IS the next seed: B'' — the inner pentagon."""
    return C(state)


def collapse(state):
    """C* — the return. Any state, any depth, back to the nine lines."""
    return list(CODEX)


def park_at_center(state):
    """L3 attempt — the engine refuses by construction."""
    raise CenterRefused("L3 — the center is not a state; \u221e0 is never a phase")
