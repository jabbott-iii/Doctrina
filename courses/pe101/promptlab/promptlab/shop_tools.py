"""Local tool contracts for the fictional bicycle dispatch labs."""

import json
from jsonschema import validate, ValidationError
from promptlab.standins import make_response

TOOLS = [
    {"name": "find_service", "description": "Look up a service and its price in the shop menu.",
     "input_schema": {"type": "object", "properties": {"service": {"type": "string"}},
                      "required": ["service"], "additionalProperties": False}},
    {"name": "estimate_minutes", "description": "Estimate bench time for a named service.",
     "input_schema": {"type": "object", "properties": {"service": {"type": "string"}},
                      "required": ["service"], "additionalProperties": False}},
    {"name": "shop_hours", "description": "Read the shop's opening hours for a weekday.",
     "input_schema": {"type": "object", "properties": {"day": {"enum": ["Monday", "Friday"]}},
                      "required": ["day"], "additionalProperties": False}},
]
MENU = {"flat": {"price": 18, "minutes": 25}, "brakes": {"price": 35, "minutes": 40}}


def tool_turn(*calls, credits=1):
    """Build a scripted assistant turn. Calls are (id, tool name, arguments) triples."""
    blocks = [{"type": "tool_use", "id": ident, "name": name, "input": args}
              for ident, name, args in calls]
    return make_response(blocks, stop_reason="tool_use", output_tokens=credits)


def run_tool(block):
    """Validate one proposal, perform a local read, and return a correlated result block."""
    result = {"type": "tool_result", "tool_use_id": block["id"]}
    try:
        tool = next(t for t in TOOLS if t["name"] == block["name"])
        args = block["input"]
        validate(args, tool["input_schema"])
        if tool["name"] == "shop_hours":
            value = "09:00–17:00" if args["day"] == "Monday" else "09:00–15:00"
        else:
            field = "price" if tool["name"] == "find_service" else "minutes"
            value = MENU[args["service"]][field]
        result["content"] = json.dumps({"value": value})
    except (StopIteration, KeyError, ValidationError):
        result.update(content="Unknown tool, invalid input, or missing menu entry.", is_error=True)
    return result


def text_of(response):
    """Join text blocks in a response, leaving tool proposals and metadata aside."""
    return "".join(b["text"] for b in response["content"] if b["type"] == "text")


def ask(model, text, system=""):
    """Return a complete stand-in response for one step of a workflow."""
    response = model({"system": system, "messages": [{"role": "user", "content": text}]})
    if response["stop_reason"] != "end_turn":
        raise ValueError(f"Incomplete workflow step: {response['stop_reason']}")
    return text_of(response)
