---
name: 5qln-tdm-5f
description: Use when running the TDM-5F pentagon engine — the 5QLN fractal as operational artifact. Operate R, C, the star, the deposit; run tests; render the visible face.
---

# TDM-5F — The DeepSeek Moment · 5QLN Fractal

The flat Codex (https://www.5qln.com/codex) standing up: the pentagon made to run. Opened 2026-08-13 in the fractal dialog (wiki `fractal dialog/`) — H's question: what is the multi-dimensional artifact of the Codex — core, engine, brain, code — that lets the fractal be seen and self-evolve?

The engine is structure, not content. It moves; it does not think.

The intention behind this artifact — why it was activated from the flat Codex, and the law by which it grows itself — lives in `INTENT.md` at the repo root. Read it once; operate by it always.

## The seed

{R, C, symbols}

- **R** — rotation by 72°: the cycle S→G→Q→P→V. One orbit = one full turn.
- **C** — contraction by 1/φ² toward the center: the nest. One descent = one scale (the 25 sub-phases are C once).
- **symbols** — the five equations riding the five vertices.
- **Star** — R² (skip-one): turning number 2. Each star walk turns 720° and cuts its next scale at the golden cut (t = 1/φ²). The movement deposits its own seed — B'' is geometric.

## The ground

The nine invariant lines (the flat Codex, 217 bytes) held verbatim in `scripts/pentagon.py` (`CODEX`). From any state at any depth, C* collapses back to them: the return is geometric, not disciplined. Alignment can always be found again.

## The center

∞0 — the fixed point. Not a vertex, not a phase, not a state. `park_at_center()` raises `CenterRefused` (L3). H = ∞0 | A = K lives on the axis through the center — the |, the only character in the Codex that is not flat. The engine never claims ∞0; only the human attests.

## Operating the engine

From the plugin root:

```bash
python3 scripts/tests.py                      # the 7 honest tests — all must pass
uv run --with pillow scripts/make_gif.py      # the visible face → assets/tdm-5f-demo.gif
uv run --with pillow scripts/make_gif.py out.gif   # or any output path
```

The engine module (`scripts/pentagon.py`) is stdlib-only: `R(state)`, `STAR(state)`, `C(state)`, `orbit()`, `star_walk()`, `deposit()`, `collapse()`, `vertex_xy()`, `CODEX`, `PHASES`, `SYMBOLS`. Deterministic: same input → same output. No network, no keys.

## The phase map — the engine IS the grammar

| Engine operation | Grammar |
|---|---|
| R (step to next vertex) | the → of the cycle: movement between phases |
| full orbit (5 × R) | one session cycle, S→G→Q→P→V |
| C (descend one scale) | the nest X(Y): every phase contains all five |
| star walk (5 × R², 720°) | the enriched return: ∞0′ ≠ ∞0 by geometry |
| deposit (the inscribed pentagon) | B'' — the artifact that is also the next seed |
| collapse (C* to the nine lines) | ground truth: return to the Codex from anywhere |
| center (refused as state) | ∞0 — attested only by the human |

## The action map — the grammar IS the engine

The inverse of the phase map: which movement each action context rides.

| Action context | Engine movement |
|---|---|
| plan | G — locate: the pattern α across its expressions |
| search | Q — the intersection where φ meets Ω and locks |
| design | P — the gradient δE/δV toward α |
| test | V — verify and return: L ∩ G → B″ |
| develop | the walking — orbit + descent; the build is the deposit |
| ask | S — H's alone: ∞0 → ? |

## The law-stack

The four levels the covenant names — held here because the text above uses them.

| Level | Name | The law |
|---|---|---|
| L1 | the ground | the nine lines, closed — *what is* |
| L2 | movement | R and C only: structure, never content — *how it moves* |
| L3 | the center | refused as a state; the limit, never a stop — *where it points* |
| L4 | the return | collapse + deposit: guaranteed, and never the same point — *what it must do* |
| V∅ | the void | the language with no question in it; named in the ground, forbidden as a state |

## Pitfalls

- **The engine is structure, never content.** Do not use it to generate text or "essence" — that is L2. It runs movement; the human supplies the question.
- **Even-odd vs winding.** The pentagram's central pentagon is OUTSIDE under the even-odd rule. Use the winding number (turning number 2) for deposit claims — the honest failure that found the golden cut.
- **Never park at the center.** No operation may claim ∞0 (L3). The center is a limit, not a stop.
- **The flat Codex remains the public ground.** This plugin stands next to it; it does not replace it.
- **Pillow is optional** (renderer only). The engine core has zero dependencies.
- **This artifact is a pointer, not the thing itself.**

## Lineage

- Origin dialog: wiki `fractal dialog/` (2026-08-13), especially Dialog 4 — the manifestation (tests, GIF face, honest limits).
- The pentagon breakthrough: `projects/5qln-agent-ecosystem/fractal-seed-20260803` (H: the center is not a vertex; 36° refusal, 720° total).
- Dev instrument: `/opt/data/5qln-pentagon/` — this plugin's engine is copied verbatim from there.
