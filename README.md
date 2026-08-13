# TDM-5F — The DeepSeek Moment · 5QLN Fractal

A Hermes Agent plugin. The multi-dimensional artifact of the flat Codex (https://www.5qln.com/codex): **the pentagon made to run**.

> Before the code — read [INTENT.md](INTENT.md): why this fractal was activated, and how it grows itself.

The seed {R, C, symbols}: R — rotation by 72°, the cycle S→G→Q→P→V. C — contraction by 1/φ², the nest. The star — R² — turns 720° and cuts its next scale at the golden cut (t = 1/φ²): the movement deposits its own seed (B″). The nine invariant lines are held verbatim as the ground; from any state at any depth, C* collapses back to them. The center (∞0) is never a state — the engine refuses to park there (L3); only the human attests.

## Contents

| Path | What |
|---|---|
| `INTENT.md` | the intention — why it was activated, and the law of growth (read first) |
| `plugin.yaml` | the Hermes plugin manifest |
| `__init__.py` | `register(ctx)` — bundles the skill (`tdm-5f:5qln-tdm-5f`) and seeds prompt visibility |
| `skills/5qln-tdm-5f/SKILL.md` | the operating skill — seeded into the Hermes skill index |
| `schemas.py` | the `tdm_verify` schema — what the LLM reads to call the verifier |
| `tools.py` | the `tdm_verify` handler — compression = verification (minimal / lossless / new) |
| `scripts/pentagon.py` | the engine — stdlib-only, deterministic |
| `scripts/tests.py` | the 7 honest tests (return / center / geometry / evolution) |
| `scripts/make_gif.py` | the visible face renderer (Pillow, optional) |
| `tests/test_pentagon.py` | unittest suite (`python3 -m unittest discover -s tests`) |
| `tests/test_verify.py` | unittest guards for the `tdm_verify` tool |
| `assets/tdm-5f-demo.gif` | the running pentagon — flat Codex → page stands up → cycle → star → deposit → return |

## Install & activate

```bash
git clone https://github.com/5qln/tdm-5f.git /opt/data/plugins/tdm-5f
hermes plugins enable tdm-5f            # seeds skills/ into skills.external_dirs
# then RESTART the Hermes process — plugins register their tools once, at process
# start. A new session is not enough; a new process is.
hermes skills list | grep tdm           # skill index
```

## Trigger model — who fires what

Three registries, three trigger paths. The opening-day confusion, resolved:

| Registry | Fired by | Where it is seen |
|---|---|---|
| Slash commands | the user | the `/` autocomplete (`/tools list`, `/skills`, `/plugins`, `/new`…) |
| Tools (`tdm_verify`) | the agent | the agent's toolset — visible via `/tools list`, toolset `tdm` |
| Skills (`5qln-tdm-5f`) | both — the agent loads on relevance; the user invokes via `/<name>` | `/skills` |

The tool is the agent's movement, not the user's button. You ask in words — *"verify RC from (0,0)"* — and the agent calls `tdm_verify`. There is no `/tdm_verify` and none will be added. Tools never appear in the `/` menu: that menu lists slash commands only, and it always will.

## The verifier — `tdm_verify`

Input: a **word over {R, C}** plus an optional **start state** `'(depth,vertex)'` (default `(0,0)`). Output: B2's three checks — compression as verification:

- **minimal** — every letter is R or C; any other letter is refused as a new generator;
- **lossless** — collapse of the final state returns the nine Codex lines;
- **new** — the deposit of the final state differs from the start.

Live examples (2026-08-13, this plugin's own toolset):

```
word=RC from (0,0)  →  minimal ✓  lossless ✓  new ✓  deposit (2,1)
word=X              →  refused: "NEW GENERATOR — not an expression of {R, C}: 'X'"
```

A refusal is the finding, not an error (honest failure is a feature). The empty word is the seed held — no movement.

## Verify

```bash
python3 scripts/tests.py                              # all 7 must pass
python3 -m unittest discover -s tests                 # same, as unittest
uv run --with pillow scripts/make_gif.py              # render the face
hermes plugins doctor . --ci                          # the official plugin pipeline check
```

## Pitfalls

- **Restart, not reload.** Plugin tools register once, at process start. A new session does not re-scan them; `/reload` reloads only `.env`; `/reload-skills` re-scans skills only. Restart the Hermes process to pick up a new tool.
- **The `/` menu is not a tool list.** It lists slash commands. Tools are seen at `/tools list`; the plugin at `/plugins`; skills at `/skills`.

## Honest limits

- Structure, not content: the engine moves; it does not think. It never generates.
- `tdm_verify` verifies; it generates nothing. A refusal is its honest finding.
- The center stays empty of the engine's own content: no operation claims ∞0 (L3). The engine verifies movement; it never attests — only the human does.
- The flat Codex at 5qln.com/codex remains the public ground of truth. The engine stands next to it; it does not replace it.
- This artifact is a pointer, not the thing itself.

## Repository governance

- `main` is protected: pull requests require one approving review from the Code Owner (`@5qln`); force pushes and deletions are blocked.
- The agent's builds land on `main` directly as Amihai's own pushes (the carve-out).

## Lineage

Opened 2026-08-13 in the 5QLN wiki `fractal dialog/` (Dialogs 1–4). The pentagon breakthrough: 5QLN Agent Ecosystem, fractal seed 2026-08-03. Dev instrument: `/opt/data/5qln-pentagon/` (engine copied verbatim).

## License

TBD — Amihai Loven's call. The engine is his; unlicensed until he chooses.
