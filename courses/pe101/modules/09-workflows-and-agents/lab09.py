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
# # Lab 9: Workflows and agents
#
# **Objectives** LO-9.1, LO-9.2, LO-9.3  
# **Prerequisites** The [Module 9 reading](index.md)  
# **Time** About 2.5 hours.
#
# Implement four coordination patterns with scripted responses. Compare them with a bounded agent that can propose only local shop reads.
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

from concurrent.futures import ThreadPoolExecutor

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Trace an independent branch
#
# This branch does not need another branch's answer. Predict the result key you would log.

# %%
print(ask(ScriptedModel(["25 minutes"]), "Flat tire", "Estimate time."))

# %% [markdown]
# ### Exercise L9.1 (LO-9.1, ★★, about 25 minutes)
#
# **Route to a known worker.** Obtain the route with ask and dispatch to the named worker. Use the ticket as that worker's input. Raise ValueError for an unknown route.

# %% tags=["answer-L9.1"]
def routed(router, workers, ticket):
    raise NotImplementedError("L9.1")

# %% tags=["raises-exception"]
billing = ScriptedModel(["Ask for the invoice ID."])
repair = ScriptedModel([])
assert routed(ScriptedModel(["billing"]), {"billing": billing, "repair": repair}, "Receipt")
assert billing.calls == 1 and repair.calls == 0
print("passed")

# %% [markdown]
# ### Exercise L9.2 (LO-9.1, ★★, about 25 minutes)
#
# **Run parallel reads.** Use a ThreadPoolExecutor with two workers. Submit one ask per named stand-in with the same ticket, then return a dictionary from job names to results. Use separate stand-ins for independent jobs.

# %% tags=["answer-L9.2"]
def parallel(workers, ticket):
    raise NotImplementedError("L9.2")

# %% tags=["raises-exception"]
workers = {"parts": ScriptedModel(["$18"]), "labor": ScriptedModel(["25 minutes"])}
assert parallel(workers, "Flat tire") == {"parts": "$18", "labor": "25 minutes"}
print("passed")

# %% [markdown]
# ### Exercise L9.3 (LO-9.1, ★★, about 25 minutes)
#
# **Check an orchestration plan.** The orchestrator replies with a JSON array of unique job names. Reject anything else, including unknown jobs, before running workers. Pass the whole ticket to each. Return results keyed by job in plan order.

# %% tags=["answer-L9.3"]
def orchestrate(planner, workers, ticket):
    raise NotImplementedError("L9.3")

# %% tags=["raises-exception"]
jobs = {"parts": ScriptedModel(["Flat kit"])}
assert orchestrate(ScriptedModel(['["parts"]']), jobs, "Flat") == {"parts": "Flat kit"}
try:
    orchestrate(ScriptedModel(['["parts", "missing"]']), jobs, "Flat")
except ValueError:
    assert jobs["parts"].calls == 1
else:
    raise AssertionError("Unknown job should fail before dispatch.")
print("passed")

# %% [markdown]
# ### Exercise L9.4 (LO-9.1, ★★, about 25 minutes)
#
# **Revise with a bounded evaluator.** Call draft on the ticket followed by any prior review. Call judge on the ticket and the result. Return the first draft whose review is exactly pass, or None after max_drafts attempts.

# %% tags=["answer-L9.4"]
def optimize(draft, judge, ticket, max_drafts):
    raise NotImplementedError("L9.4")

# %% tags=["raises-exception"]
draft = ScriptedModel(["Done!", "Could you share the invoice ID?"])
judge = ScriptedModel(["Include an invoice request.", "pass"])
assert optimize(draft, judge, "Receipt", 2) == "Could you share the invoice ID?"
assert "Include an invoice request." in draft.requests[1]["messages"][0]["content"]
assert optimize(ScriptedModel([]), ScriptedModel([]), "Receipt", 0) is None
print("passed")

# %% [markdown]
# ### Exercise L9.5 (LO-9.2, LO-9.3, ★★, about 25 minutes)
#
# **Trace both budget stops.** Implement a local tool loop. Before each call, reserve the specified maximum output tokens.
#   Stop with cost_limit if that would exceed budget. Charge actual output_tokens and raise ValueError
#   if a fixture violates its reserve. Return a triple of status, completed text or None, and a log.
#   Each log entry has turn starting at 1, used, spent, stop, and tools. Reuse TOOLS and run_tool.
#   For a pricing question, compare the loop with one direct fixture lookup and write your choice.

# %% tags=["answer-L9.5"]
def agent(model, task, max_turns, budget, reserve):
    raise NotImplementedError("L9.5")

# %% tags=["raises-exception"]
read = tool_turn(("one", "find_service", {"service": "flat"}), credits=2)
assert agent(ScriptedModel([read]), "Price", 1, 10, 3)[0] == "turn_limit"
model = ScriptedModel([read])
status, result, log = agent(model, "Price", 5, 4, 3)
assert status == "cost_limit" and result is None and model.calls == 1
assert log == [{"turn": 1, "used": 2, "spent": 2, "stop": "tool_use",
                "tools": ["find_service"]}]
assert agent(ScriptedModel([read, make_response("$18", output_tokens=2)]),
             "Price", 5, 5, 3)[0:2] == ("end_turn", "$18")
print("passed")

# %% [markdown]
# ## Summary
#
# You tried four scripted workflows and traced a loop bounded by spend and turns.
