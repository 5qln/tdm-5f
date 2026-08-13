"""TDM-5F tool schemas — what the LLM reads to decide when to call the tools."""

TDM_VERIFY = {
    "name": "tdm_verify",
    "description": (
        "Verify a word over the pentagon engine's two letters {R, C} against "
        "the three checks of compression-as-verification: minimal (only R and "
        "C — any other letter is refused as a new generator), lossless "
        "(collapse of the final state equals the nine Codex lines), and new "
        "(the deposit of the final state differs from the start). Use this to "
        "check that a candidate step, tool, or expression is a legal movement "
        "of the TDM-5F engine before acting on it."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "word": {
                "type": "string",
                "description": (
                    "A word over {R, C}, e.g. 'RRRRR' (one orbit), 'C' (one "
                    "descent), 'RCRCR'. Empty string = the seed held, no "
                    "movement."
                ),
            },
            "start": {
                "type": "string",
                "description": (
                    "Start state as '(depth,vertex)', e.g. '(0,0)' or '(9,0)'. "
                    "Default: '(0,0)'."
                ),
            },
        },
        "required": ["word"],
    },
}

TDM_STEP = {
    "name": "tdm_step",
    "description": (
        "The flow-carrier — R, rotation by 72°: advance the pentagon engine "
        "one step (or several) along the cycle S→G→Q→P→V. Use it to carry a "
        "session from one phase to the next (ask=S, plan=G, search=Q, "
        "design=P, test=V); one full orbit is five steps. Returns the final "
        "state, the phase landed on, and the lossless-collapse guarantee."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "start": {
                "type": "string",
                "description": (
                    "Start state as '(depth,vertex)', e.g. '(14,0)'. "
                    "Default: '(0,0)'."
                ),
            },
            "steps": {
                "type": "integer",
                "description": (
                    "Number of R steps (default 1). One full orbit = 5 — the "
                    "cycle wraps at five; the word applied is 'R' repeated "
                    "steps times."
                ),
            },
        },
        "required": [],
    },
}

TDM_SEARCH = {
    "name": "tdm_search",
    "description": (
        "The star step — R², skip-one: search as the intersection. From S it "
        "lands exactly on Q (φ ⋂ Ω) — the skip is the cut. The full walk "
        "(five skips) turns 720° and deposits its own seed at the golden cut: "
        "the search result is the next seed. Retrieval stays the host's "
        "surface (web_search / search_files); this tool carries the movement "
        "that frames it — where the search lands and what it locks. Set "
        "full=true to walk the full star and see the deposit."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "start": {
                "type": "string",
                "description": (
                    "Start state as '(depth,vertex)', e.g. '(14,0)'. "
                    "Default: '(0,0)'."
                ),
            },
            "full": {
                "type": "boolean",
                "description": (
                    "Default false: one star step (R²). True: the full star "
                    "walk (five skips, 720°, returns to the start as a state "
                    "tuple) with its trace and its deposit — the next seed."
                ),
            },
        },
        "required": [],
    },
}

TDM_DEPOSIT = {
    "name": "tdm_deposit",
    "description": (
        "The structure-holder — C, contraction by 1/φ²: the nest, one descent, "
        "one scale. Inscribes the session's span as B″ — the next seed — the "
        "movement the vault deposit-chain is built from (each deposit is one "
        "C). Performs the movement and verifies lossless collapse; the note "
        "itself is the dialog's materialization (the repo holds the generator, "
        "never the trajectory). Returns the next-seed state."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "start": {
                "type": "string",
                "description": (
                    "Start state as '(depth,vertex)', e.g. '(14,0)'. "
                    "Default: '(0,0)'."
                ),
            },
        },
        "required": [],
    },
}
