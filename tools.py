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


def tdm_step(args, **kwargs):
    """The flow-carrier — R: the cycle S→G→Q→P→V as a tool.

    One step is one vertex; five steps are one orbit. The orbit is the same
    tool, not a second one (minimality refuses what composes). Runs the
    movement and returns the phase landed on with the lossless guarantee.
    """
    steps = args.get("steps", 1)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        return json.dumps({"error": "steps must be a positive integer"})
    try:
        start = _parse_start(args.get("start"))
    except ValueError as e:
        return json.dumps({"error": str(e)})

    word = "R" * steps
    st = start
    for _ in range(steps):
        st = _engine.R(st)
    return json.dumps({
        "word": word,
        "start": list(start),
        "final": list(st),
        "phase": _engine.PHASES[st[1]],
        "steps": steps,
        "lossless": _engine.collapse(st) == _engine.CODEX,
        "deposit": list(_engine.deposit(st)),
    })


def tdm_search(args, **kwargs):
    """The star — R²: search as the intersection (B15).

    One star step lands two vertices ahead; from S it lands exactly on Q —
    the intersection (φ ⋂ Ω), the skip is the cut. The full walk (five
    skips) turns 720° and deposits its own seed: the search result is the
    next seed. Retrieval stays the host's surface; this tool carries the
    movement that frames it.
    """
    try:
        start = _parse_start(args.get("start"))
    except ValueError as e:
        return json.dumps({"error": str(e)})

    if not bool(args.get("full", False)):
        st = _engine.STAR(start)
        return json.dumps({
            "word": "RR",
            "start": list(start),
            "final": list(st),
            "phase": _engine.PHASES[st[1]],
            "symbol": _engine.SYMBOLS[_engine.PHASES[st[1]]],
            "lossless": _engine.collapse(st) == _engine.CODEX,
            "deposit": list(_engine.deposit(st)),
        })

    trace = _engine.star_walk(start)
    end = trace[-1]
    return json.dumps({
        "word": "R" * 10,
        "start": list(start),
        "final": list(end),
        "trace": [list(s) for s in trace],
        "trace_phases": [_engine.PHASES[s[1]] for s in trace],
        "turning": (
            "720° — two full turns. The endpoint equals the start as a state "
            "tuple; the enrichment is the human's attestation, never a state "
            "difference (B12)."
        ),
        "lossless": _engine.collapse(end) == _engine.CODEX,
        "deposit": list(_engine.deposit(end)),
    })


def tdm_deposit(args, **kwargs):
    """The structure-holder — C: the nest as a tool (B15).

    One descent, one scale: the movement the vault deposit-chain is built
    from. Performs the movement and verifies lossless collapse; the note
    itself is the dialog's materialization — the repo holds the generator,
    never the trajectory (B11).
    """
    try:
        start = _parse_start(args.get("start"))
    except ValueError as e:
        return json.dumps({"error": str(e)})

    st = _engine.C(start)
    return json.dumps({
        "word": "C",
        "start": list(start),
        "final": list(st),
        "seed_delta": "(%d, %d) → (%d, %d)" % (start[0], start[1], st[0], st[1]),
        "deposit": list(st),  # the movement IS the deposit: its final is B″, the next seed
        "lossless": _engine.collapse(st) == _engine.CODEX,
    })
