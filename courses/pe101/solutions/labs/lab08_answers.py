# %% tags=["answer-L8.1"]
def parse_record(text):
    try:
        value = json.loads(text)
        validate(value, SCHEMA)
    except (json.JSONDecodeError, ValidationError) as error:
        raise ValueError("Invalid dispatch record.") from error
    if not value["summary"].strip():
        raise ValueError("Summary must contain a visible character.")
    return value

# %% tags=["answer-L8.2"]
def specs():
    return [
        {"name": "find_service", "description": "Read the menu price for a service.",
         "input_schema": {"type": "object", "properties": {"service": {"type": "string"}},
                          "required": ["service"], "additionalProperties": False}},
        {"name": "estimate_minutes", "description": "Read the bench-time estimate for a service.",
         "input_schema": {"type": "object", "properties": {"service": {"type": "string"}},
                          "required": ["service"], "additionalProperties": False}},
        {"name": "shop_hours", "description": "Read the opening hours for Monday or Friday.",
         "input_schema": {"type": "object", "properties": {"day": {"enum": ["Monday", "Friday"]}},
                          "required": ["day"], "additionalProperties": False}},
    ]

# %% tags=["answer-L8.3"]
def terminal(response):
    reason = response["stop_reason"]
    return reason, text_of(response) if reason == "end_turn" else None

# %% tags=["answer-L8.4"]
def tool_loop(model, ticket, max_turns=4):
    history = [{"role": "user", "content": ticket}]
    for _ in range(max_turns):
        response = model({"messages": history, "tools": TOOLS})
        reason = response["stop_reason"]
        if reason != "tool_use":
            return reason, text_of(response) if reason == "end_turn" else None
        blocks = response["content"]
        results = [run_tool(block) for block in blocks if block["type"] == "tool_use"]
        if not results:
            raise ValueError("Missing tool proposal.")
        history.extend([{"role": "assistant", "content": blocks},
                        {"role": "user", "content": results}])
    return "turn_limit", None
