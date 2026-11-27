# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: nbgrader,-all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # PA4: A tool-using assistant
#
# **When** After [Module 9](../../modules/09-workflows-and-agents/index.md)  
# **Time** About 3 hours  
# **Points** 20 for scoring your own work.
#
# Prepare a read-only assistant for the fictional shop. Use the local fixtures and check each
# stop reason. Write a short comparison of a single lookup, the router, and the bounded agent.
# Name one case for each and justify the added calls.
#
# Replace the indicated lines in each answer cell and run the check below it. Restart the kernel
# and run all cells before you record your result. Keep the tests unchanged. The course's
# [policies](../../README.md#policies) apply.

# %% [markdown]
# ## Setup

# %%
import json
from jsonschema import validate, ValidationError
from promptlab import ScriptedModel, make_response
from promptlab.shop_tools import MENU, TOOLS, tool_turn, run_tool, text_of, ask

SCHEMA = {
    "type": "object",
    "properties": {"queue": {"enum": ["repair", "billing", "account"]},
                   "summary": {"type": "string", "minLength": 1, "maxLength": 80}},
    "required": ["queue", "summary"],
    "additionalProperties": False,
}

# %% [markdown]
# ## Problem 1: Validate and retry once (LO-8.1, LO-2.4, 5 points)
#
# Return a valid dispatch record on end_turn. On refusal or any incomplete stop return None.
#   On JSON parse, schema, or blank-summary failure, retry once with a user message asking for
#   a valid record. Preserve the original ticket in the retry transcript.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa4-1", "schema_version": 3, "task": false}
def validated(model, ticket):
    ### BEGIN SOLUTION
    messages = [{"role": "user", "content": ticket}]
    for attempt in range(2):
        response = model({"messages": messages})
        if response["stop_reason"] != "end_turn":
            return None
        try:
            value = json.loads(text_of(response))
            validate(value, SCHEMA)
            if not value["summary"].strip():
                raise ValueError("Blank summary.")
            return value
        except (json.JSONDecodeError, ValidationError, ValueError):
            if attempt == 0:
                messages = messages + [{"role": "assistant", "content": response["content"]},
                                       {"role": "user", "content": "Return a valid dispatch record."}]
    return None
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa4-1-tests", "schema_version": 3, "task": false, "points": 5}
m = ScriptedModel(["broken", '{"queue":"repair","summary":"Flat"}'])
assert validated(m, "Flat tire")["queue"] == "repair" and m.calls == 2
assert m.requests[1]["messages"][0]["content"] == "Flat tire"
### BEGIN HIDDEN TESTS
m = ScriptedModel([make_response([], stop_reason="refusal")])
assert validated(m, "Flat") is None and m.calls == 1
assert validated(ScriptedModel(["bad", "{}"]), "Flat") is None
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 2: Use three tools (LO-8.2, LO-8.3, 6 points)
#
# Inspect the three definitions in TOOLS. Add a written note for each about when to call it.
#   Implement the tool loop from Lab 8, including correlated success and error results, returning
#   a stop reason and completed text or None.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa4-2", "schema_version": 3, "task": false}
def tool_loop(model, ticket, max_turns=4):
    ### BEGIN SOLUTION
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
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa4-2-tests", "schema_version": 3, "task": false, "points": 6}
reply = tool_turn(("p", "find_service", {"service": "brakes"}),
                    ("t", "estimate_minutes", {"service": "brakes"}),
                    ("h", "shop_hours", {"day": "Monday"}))
m = ScriptedModel([reply, "Done."])
assert tool_loop(m, "Plan a repair") == ("end_turn", "Done.")
assert [b["tool_use_id"] for b in m.requests[1]["messages"][-1]["content"]] == ["p", "t", "h"]
### BEGIN HIDDEN TESTS
m = ScriptedModel([tool_turn(("q", "find_service", {"service": "unknown"})),
                     make_response("cut off", stop_reason="max_tokens")])
assert tool_loop(m, "Plan") == ("max_tokens", None)
assert m.requests[1]["messages"][-1]["content"][0]["is_error"]
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 3: Route by result (LO-9.1, LO-6.3, 4 points)
#
# Ask the router for a known queue. Raise ValueError for an unknown route. Pass the original ticket to the selected worker and return its completed text. Explain what happens when a valid route is semantically wrong.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa4-3", "schema_version": 3, "task": false}
def routed(router, workers, ticket):
    ### BEGIN SOLUTION
    route = ask(router, ticket, "Return exactly repair or billing.")
    if route not in workers:
        raise ValueError("Unknown route.")
    return ask(workers[route], ticket, f"Handle the {route} queue.")
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa4-3-tests", "schema_version": 3, "task": false, "points": 4}
assert routed(ScriptedModel(["repair"]), {"repair": ScriptedModel(["Ready"])}, "Flat") == "Ready"
### BEGIN HIDDEN TESTS
worker = ScriptedModel([])
try:
    routed(ScriptedModel(["unlisted"]), {"repair": worker}, "Flat")
except ValueError:
    assert worker.calls == 0
else:
    raise AssertionError("Reject unknown routes before executing a worker.")
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 4: Apply both limits (LO-9.2, LO-9.3, 5 points)
#
# Implement the bounded agent from Lab 9. Reserve output tokens before each step and return
#   a status, text or None, and a trace with turn, used, spent, stop, and tools. Charge actual
#   output_tokens, and raise ValueError for usage outside the reservation or an empty tool turn.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa4-4", "schema_version": 3, "task": false}
def agent(model, task, max_turns, budget, reserve):
    ### BEGIN SOLUTION
    history = [{"role": "user", "content": task}]
    log = []
    spent = 0
    for turn in range(1, max_turns + 1):
        if spent + reserve > budget:
            return "cost_limit", None, log
        response = model({"messages": history, "tools": TOOLS, "max_tokens": reserve})
        used = response["usage"]["output_tokens"]
        if not 0 <= used <= reserve:
            raise ValueError("Scripted usage must fit the reserve.")
        spent += used
        reason = response["stop_reason"]
        blocks = response["content"]
        calls = [b for b in blocks if b["type"] == "tool_use"]
        log.append({"turn": turn, "used": used, "spent": spent,
                    "stop": reason, "tools": [b["name"] for b in calls]})
        if reason != "tool_use":
            return reason, text_of(response) if reason == "end_turn" else None, log
        if not calls:
            raise ValueError("A tool stop requires a proposal.")
        history.extend([{"role": "assistant", "content": blocks},
                        {"role": "user", "content": [run_tool(b) for b in calls]}])
    return "turn_limit", None, log
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa4-4-tests", "schema_version": 3, "task": false, "points": 5}
m = ScriptedModel([tool_turn(("p", "find_service", {"service": "flat"}), credits=2)])
status, text, log = agent(m, "Price", 3, 3, 2)
assert (status, text) == ("cost_limit", None) and log[0]["spent"] == 2
### BEGIN HIDDEN TESTS
assert agent(ScriptedModel([]), "Flat", 0, 9, 3) == ("turn_limit", None, [])
m = ScriptedModel([tool_turn(("p", "find_service", {"service": "flat"}), credits=2)])
assert agent(m, "Flat", 1, 3, 2)[0] == "turn_limit"
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Tools you used
#
# Say which tools you used and how, or write “none.”
