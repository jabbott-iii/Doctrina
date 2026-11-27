# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: tags,-all
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
# # Lab 8: Structured output and tools
#
# **Objectives** LO-8.1, LO-8.2, LO-8.3  
# **Prerequisites** The [Module 8 reading](index.md)  
# **Time** About 2.5 hours.
#
# Validate dispatch records, design three named read-only tools, and test the tool exchange with a scripted stand-in.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
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

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Predict validity
#
# The two objects are valid JSON. Predict which one satisfies the schema.

# %%
for example in ({"queue": "repair", "summary": "Flat tire"}, {"queue": "repair"}):
    try:
        validate(example, SCHEMA)
        print("valid", example)
    except ValidationError:
        print("invalid", example)

# %% [markdown]
# ### Exercise L8.1 (LO-8.1, ★★, about 25 minutes)
#
# **Check the response contract.** Parse the JSON, validate it against SCHEMA, and return the record. Treat a blank or spaces-only summary as invalid. Translate expected parse and schema errors to ValueError.

# %% tags=["answer-L8.1"]
def parse_record(text):
    raise NotImplementedError("L8.1")

# %% tags=["raises-exception"]
assert parse_record('{"queue":"account","summary":"Reset email"}')["queue"] == "account"
for bad in ("oops", '{"queue":"unknown","summary":"A"}', '{"queue":"repair","summary":" "}'):
    try:
        parse_record(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("An invalid record was accepted.")
print("passed")

# %% [markdown]
# ### Exercise L8.2 (LO-8.2, ★★, about 25 minutes)
#
# **Write tool specifications.** Return a list of three tool definitions with name, description, and input_schema. Use the names, fields, and constraints shown in the reading and in the setup's TOOLS. Write descriptions that distinguish price from time. The local runner already maps these names to fictional data.

# %% tags=["answer-L8.2"]
def specs():
    raise NotImplementedError("L8.2")

# %% tags=["raises-exception"]
defs = specs()
assert [x["name"] for x in defs] == [x["name"] for x in TOOLS]
assert [x["input_schema"] for x in defs] == [x["input_schema"] for x in TOOLS]
assert len({x["description"] for x in defs}) == 3
print("passed")

# %% [markdown]
# ### Exercise L8.3 (LO-8.3, ★★, about 25 minutes)
#
# **Handle completed and incomplete turns.** Return the final text for end_turn. For all other stop reasons, return the reason and None. The return type is a pair with the stop reason first.

# %% tags=["answer-L8.3"]
def terminal(response):
    raise NotImplementedError("L8.3")

# %% tags=["raises-exception"]
assert terminal(make_response("Ready")) == ("end_turn", "Ready")
assert terminal(make_response("Partial", stop_reason="max_tokens")) == ("max_tokens", None)
assert terminal(make_response([], stop_reason="refusal")) == ("refusal", None)
print("passed")

# %% [markdown]
# ### Exercise L8.4 (LO-8.3, ★★, about 25 minutes)
#
# **Complete the loop.** Implement the reading's tool exchange with the setup's local run_tool and tool definitions. Return the terminal pair or ('turn_limit', None). A tool stop without any tool proposals should raise ValueError. Keep every assistant block when forwarding history.

# %% tags=["answer-L8.4"]
def tool_loop(model, ticket, max_turns=4):
    raise NotImplementedError("L8.4")

# %% tags=["raises-exception"]
model = ScriptedModel([tool_turn(("price", "find_service", {"service": "flat"}),
                                 ("bad", "shop_hours", {"day": "Sunday"})), "$18."])
assert tool_loop(model, "Price a flat and check hours.") == ("end_turn", "$18.")
last = model.requests[1]["messages"][-1]
assert last["role"] == "user"
assert [b["tool_use_id"] for b in last["content"]] == ["price", "bad"]
assert last["content"][1]["is_error"]
assert tool_loop(ScriptedModel([]), "Flat", 0) == ("turn_limit", None)
print("passed")

# %% [markdown]
# ## Summary
#
# A schema describes a record. Local validation and a bounded loop decide which actions to run.
