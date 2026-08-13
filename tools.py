"""TDM-5F tool handlers — the code that runs when the LLM calls each tool."""

import importlib.util
import json
from pathlib import Path

# Load the engine by file path — no sys.path changes, no package assumptions.
_ENGINE_PATH = Path(__file__).parent / "scripts" / "pentagon.py"
_spec = importlib.util.spec_from_file_location("tdm_5f_pentagon", _ENGINE_PATH)
assert _spec is not None and _spec.loader is not None, "engine not found at %s" % _ENGINE_PATH
_engine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_engine)


def verify(word, start=(0, 0)):
    """B2's three checks — minimal, lossless, new. All already in the engine.

    Returns (final_state, lossless, new). Raises AssertionError on a new
    generator — the refusal IS the finding (honest failure is a feature).
    """
    for ch in word:
        assert ch in "RC", "NEW GENERATOR — not an expression of {R, C}: %r" % ch
    st = start
    for ch in word:
        st = (_engine.R if ch == "R" else _engine.C)(st)
    return st, _engine.collapse(st) == _engine.CODEX, _engine.deposit(st) != start


def _parse_start(raw):
    if raw is None:
        return (0, 0)
    try:
        d, k = raw.strip("() ").split(",")
        return (int(d), int(k) % 5)
    except (ValueError, AttributeError):
        raise ValueError("start must be '(depth,vertex)', e.g. '(0,0)' — got %r" % raw)


def tdm_verify(args, **kwargs):
    """The verifier — compression = verification, as a registered capability.

    Rules for handlers: return a JSON string; a refusal is a finding, not an
    error — errors (bad input shape) return {"error": ...}.
    """
    word = args.get("word", "")
    if not isinstance(word, str):
        return json.dumps({"error": "word must be a string over {R, C}"})
    try:
        start = _parse_start(args.get("start"))
    except ValueError as e:
        return json.dumps({"error": str(e)})

    try:
        final, lossless, new = verify(word, start)
    except AssertionError as e:
        return json.dumps({
            "word": word,
            "minimal": False,
            "refused": str(e),
            "lossless": None,
            "new": None,
        })
    return json.dumps({
        "word": word,
        "minimal": True,
        "refused": None,
        "final": list(final),
        "lossless": lossless,
        "new": new,
        "deposit": list(_engine.deposit(final)),
    })
