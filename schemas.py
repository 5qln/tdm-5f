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
