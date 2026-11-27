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
# # Lab 3: Clear instructions
#
# **Objectives** LO-3.1, LO-3.2, LO-3.3  
# **Prerequisites** The [Module 3 reading](index.md)  
# **Time** About 2.5 hours.
#
# Rewrite three prompts for a bicycle repair shop and use a checker on 30 hand-written responses.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
import re
from promptlab import load_json

tickets = load_json("tickets.json")
responses = load_json("format-responses.json")
labels = ("repair", "billing", "account")

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Score a first draft
#
# Use the [prompt rubric](../../prompt-rubric.md). “Sort this” earns 1 for task and 0 for the other criteria. Read the tickets and decide how to separate each request from the stable policy.

# %%
print(tickets[0]["text"], tickets[13]["text"], tickets[18]["text"], sep="\n")

# %% [markdown]
# ### Exercise L3.1 (LO-3.1, ★★, about 25 minutes)
#
# **Rewrite three prompts.** Replace “Sort this,” “Help them,” and “Extract the info” with complete prompts for routing T01, answering T14, and extracting the requested profile change in T19. Return a list of three strings in that order. Score the drafts and revisions out of 10 on paper, with evidence for each score.

# %% tags=["answer-L3.1"]
def revisions():
    raise NotImplementedError("L3.1")

# %% tags=["raises-exception"]
assert len(revisions()) == 3
for prompt, index in zip(revisions(), [0, 13, 18], strict=True):
    assert tickets[index]["text"] in prompt, "Include the original ticket."
    assert len(prompt.split()) >= 20, "Supply the requirements and context."
print("passed")

# %% [markdown]
# ### Exercise L3.2 (LO-3.2, ★★, about 25 minutes)
#
# **Move policy out of the ticket.** Return a Messages-style request with model, max_tokens, system, and messages. Use a single user turn containing the ticket exactly. The system prompt must name all three queues and specify the output. Explain the separation in your notes.

# %% tags=["answer-L3.2"]
def route_request(ticket):
    raise NotImplementedError("L3.2")

# %% tags=["raises-exception"]
r = route_request(tickets[0]["text"])
assert all(label in r["system"] for label in labels)
assert r["messages"] == [{"role": "user", "content": tickets[0]["text"]}]
assert isinstance(r["max_tokens"], int) and r["max_tokens"] > 0
print("passed")

# %% [markdown]
# ### Exercise L3.3 (LO-3.3, ★★, about 25 minutes)
#
# **Parse the output contract.** Return the queue from a string that is exactly Label: repair, Label: billing, or Label: account. Return None for all other strings. Whole-string matching should reject even a trailing newline.

# %% tags=["answer-L3.3"]
def parse_label(text):
    raise NotImplementedError("L3.3")

# %% tags=["raises-exception"]
assert parse_label("Label: billing") == "billing"
for malformed in ["Label: other", "Label: repair\n", "label: repair", " Label: account"]:
    assert parse_label(malformed) is None, repr(malformed)
print("passed")

# %% [markdown]
# ### Exercise L3.4 (LO-3.3, ★★, about 25 minutes)
#
# **Audit 30 responses.** Return a dictionary with the counts valid and invalid. Use parse_label once per row. Explain why the resulting percentage describes the sample's formatting alone.

# %% tags=["answer-L3.4"]
def audit(rows):
    raise NotImplementedError("L3.4")

# %% tags=["raises-exception"]
assert audit(responses) == {"valid": 15, "invalid": 15}
assert audit([]) == {"valid": 0, "invalid": 0}
print(responses[0]["source"])
print("passed")

# %% [markdown]
# ## Summary
#
# You wrote task-specific instructions, split policy from data, and scored a hand-written set for format.
