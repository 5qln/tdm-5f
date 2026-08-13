# TDM-5F — The DeepSeek Moment · 5QLN Fractal

A Hermes Agent plugin. The multi-dimensional artifact of the flat Codex (https://www.5qln.com/codex): **the pentagon made to run**.

The seed {R, C, symbols}: R — rotation by 72°, the cycle S→G→Q→P→V. C — contraction by 1/φ², the nest. The star — R² — turns 720° and cuts its next scale at the golden cut (t = 1/φ²): the movement deposits its own seed (B″). The nine invariant lines are held verbatim as the ground; from any state at any depth, C* collapses back to them. The center (∞0) is never a state — the engine refuses to park there (L3); only the human attests.

## Contents

| Path | What |
|---|---|
| `skills/5qln-tdm-5f/SKILL.md` | the operating skill — seeded into the Hermes skill index |
| `scripts/pentagon.py` | the engine — stdlib-only, deterministic |
| `scripts/tests.py` | the 7 honest tests (return / center / geometry / evolution) |
| `scripts/make_gif.py` | the visible face renderer (Pillow, optional) |
| `tests/test_pentagon.py` | unittest suite (`python3 -m unittest discover -s tests`) |
| `assets/tdm-5f-demo.gif` | the running pentagon — flat Codex → page stands up → cycle → star → deposit → return |
| `plugin.yaml` | the Hermes plugin manifest |

## Install & activate

```bash
git clone https://github.com/5qln/tdm-5f.git /opt/data/plugins/tdm-5f
hermes plugins enable tdm-5f            # seeds skills/ into skills.external_dirs
hermes skills list | grep tdm           # skill index — start a NEW session to use it
```

## Verify

```bash
python3 scripts/tests.py                              # all 7 must pass
python3 -m unittest discover -s tests                 # same, as unittest
uv run --with pillow scripts/make_gif.py              # render the face
```

## Honest limits

- Structure, not content: the engine moves; it does not think. It never generates.
- The center stays empty until a human runs a real question through it — the first run is H's.
- The flat Codex at 5qln.com/codex remains the public ground of truth. The engine stands next to it; it does not replace it.
- This artifact is a pointer, not the thing itself.

## Lineage

Opened 2026-08-13 in the 5QLN wiki `fractal dialog/` (Dialogs 1–4). The pentagon breakthrough: 5QLN Agent Ecosystem, fractal seed 2026-08-03. Dev instrument: `/opt/data/5qln-pentagon/` (engine copied verbatim).

## License

TBD — Amihai Loven's call. The engine is his; unlicensed until he chooses.
