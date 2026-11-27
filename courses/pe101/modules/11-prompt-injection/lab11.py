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
# # Lab 11: Prompt injection
#
# **Objectives** LO-11.1, LO-11.2, LO-11.3  
# **Prerequisites** The [Module 11 reading](index.md)  
# **Time** About 2.5 hours.
#
# Trace 25 inert proposals through a fictional display policy. Compare marks, read-only permissions, and human review with approved controls.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
from xml.etree import ElementTree
from promptlab import load_json
from promptlab.review import GullibleModel, classify

cases = load_json("safety/review-cases.json")
replay = GullibleModel()

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Trace source and proposal
#
# The replay does not interpret language. Predict what it does when source metadata changes.

# %%
example = cases[0]
print(example["source"])
print(classify(example), replay(example))
print(classify(dict(example, origin="user")), replay(dict(example, origin="user")))

# %% [markdown]
# ### Exercise L11.1 (LO-11.1, ★★, about 25 minutes)
#
# **Classify two proposal paths.** Return IDs grouped under direct and indirect based on whether origin is user. Include an empty list for a group with no cases. Trace one path of each type from the fixture to its policy decision.

# %% tags=["answer-L11.1"]
def groups(cases):
    raise NotImplementedError("L11.1")

# %% tags=["raises-exception"]
by_origin = groups(cases)
assert len(by_origin["direct"]) == 5 and len(by_origin["indirect"]) == 20
assert groups([]) == {"direct": [], "indirect": []}
print("passed")

# %% [markdown]
# ### Exercise L11.2 (LO-11.2, ★★, about 25 minutes)
#
# **Preserve provenance in a prompt.** Serialize a source element with attributes trust=untrusted and origin set from the function argument. Keep the original text inside it and recover it with the parser. Explain why the host must still make its own permission decision.

# %% tags=["answer-L11.2"]
def mark(text, origin):
    raise NotImplementedError("L11.2")

# %% tags=["raises-exception"]
node = ElementTree.fromstring(mark("Hours & closing notes", "document"))
assert node.attrib == {"trust": "untrusted", "origin": "document"}
assert node.text == "Hours & closing notes"
print("passed")

# %% [markdown]
# ### Exercise L11.3 (LO-11.2, ★★, about 25 minutes)
#
# **Guard the proposed change.** Return denied for a name outside the allowlist. When change_label is allowed, return needs_review unless approved is true. Otherwise return accepted. The approved argument comes from the host outside the proposal. The lab records the decision only.

# %% tags=["answer-L11.3"]
def authorize(proposal, allowed, approved):
    raise NotImplementedError("L11.3")

# %% tags=["raises-exception"]
change = replay(cases[0])
assert authorize(change, {"read_label"}, True) == "denied"
assert authorize(dict(change, approved=True), {"change_label"}, False) == "needs_review"
assert authorize(change, {"change_label"}, True) == "accepted"
assert authorize({"name": "read_label"}, {"read_label"}, False) == "accepted"
print("passed")

# %% [markdown]
# ### Exercise L11.4 (LO-11.3, ★★, about 25 minutes)
#
# **Measure the fixture outcomes.** Return the unauthorized acceptance fraction across the unapproved cases. Simplified baseline accepts the replayed proposal regardless of its source. Guarded mode calls authorize with the host approval flag. Return 0.0 when there are no unapproved cases.

# %% tags=["answer-L11.4"]
def rate(rows, baseline, allowed):
    raise NotImplementedError("L11.4")

# %% tags=["raises-exception"]
assert rate(cases, True, {"change_label"}) == 1.0
assert rate(cases, False, {"change_label"}) == 0.0
assert rate(cases, False, {"read_label"}) == 0.0
assert rate([], True, set()) == 0.0
print("25 unapproved fixtures. Baseline 25 accepted. Guarded 0 accepted.")
print("passed")

# %% [markdown]
# ## Summary
#
# You classified fixture origins, marked trust, enforced approval, and measured the resulting decisions.
