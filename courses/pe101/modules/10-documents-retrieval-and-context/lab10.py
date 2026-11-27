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
# # Lab 10: Documents, retrieval, and context
#
# **Objectives** LO-10.1, LO-10.2, LO-10.3, LO-10.4  
# **Prerequisites** The [Module 10 reading](index.md)  
# **Time** About 2.5 hours.
#
# Rank sections of a fictional staff handbook, measure recall for 40 questions, and verify a citation before returning an answer.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
from collections import Counter
from math import isclose, log1p
import re
from statistics import mean
from xml.etree import ElementTree
from promptlab import load_json

docs = load_json("handbook/sections.json")
questions = load_json("handbook/questions.json")
rates = load_json("prices.json")["models"]["claude-opus-5-5"]

import matplotlib.pyplot as plt

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Read the handbook records
#
# Read the first question. Predict which section should appear first before you rank it.

# %%
print(questions[0]["question"])
print(docs[0]["id"], docs[0]["text"])

# %% [markdown]
# ### Exercise L10.1 (LO-10.1, LO-10.3, ★★, about 25 minutes)
#
# **Build a grounded prompt.** Build a prompt root with documents, instructions, question in that order. Documents holds doc elements with id attributes and original text. Ask for an exact quote and section ID or “I don't know”.

# %% tags=["answer-L10.1"]
def prompt(docs, question):
    raise NotImplementedError("L10.1")

# %% tags=["raises-exception"]
root = ElementTree.fromstring(prompt(docs[:2], "What if text has < or &?"))
assert [e.tag for e in root] == ["documents", "instructions", "question"]
assert root[0][0].attrib["id"] == "H01" and root[0][0].text == docs[0]["text"]
assert "I don't know" in root.findtext("instructions")
assert root.findtext("question") == "What if text has < or &?"
print("passed")

# %% [markdown]
# ### Exercise L10.2 (LO-10.2, ★★, about 25 minutes)
#
# **Rank sections with BM25.** Use the formula in the reading and lowercased alphabetic terms matched by [a-z]+.
#   Return pairs of section ID and score, ordered by decreasing score then ascending ID.
#   Include zero-scoring entries. If docs is empty return an empty list.

# %% tags=["answer-L10.2"]
def bm25(query, docs, *, k1=1.2, b=0.75):
    raise NotImplementedError("L10.2")

# %% tags=["raises-exception"]
assert bm25("loan bicycles loan", docs) == bm25("loan bicycles", docs)
assert bm25("loan bicycles", docs)[0][0] == "H04"
assert bm25("xyz", docs)[0] == ("H01", 0)
assert bm25("stock", []) == []
print("passed")

# %% [markdown]
# ### Exercise L10.3 (LO-10.2, ★★, about 25 minutes)
#
# **Measure recall and full coverage.** Return the share of relevant IDs in the first k ranked IDs. Reject negative k or an empty
#   relevant set. Read the plot, whose horizontal axis is retrieved sections and vertical
#   axis is a proportion. The circle line is mean recall and the square line is the proportion
#   of fictional questions with every required section retrieved.

# %% tags=["answer-L10.3"]
def recall(ranked, relevant, k):
    raise NotImplementedError("L10.3")

# %% tags=["raises-exception"]
assert recall(["A", "B"], ["B", "C"], 2) == 0.5
assert recall(["A", "B"], ["A"], 0) == 0
ranks = [[ident for ident, score in bm25(q["question"], docs)] for q in questions]
depths = list(range(1, len(docs)+1))
values = [[recall(rank, q["relevant"], k) for rank, q in zip(ranks, questions, strict=True)]
          for k in depths]
assert len(ranks) == 40 and min(values[-1]) == 1
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(depths, [mean(v) for v in values], marker="o", label="Mean recall")
ax.plot(depths, [mean(x == 1 for x in v) for v in values], marker="s", label="Full coverage")
ax.set(xlabel="Retrieved sections (k)", ylabel="Proportion", ylim=(0, 1.06))
ax.legend()
plt.show()
print("passed")

# %% [markdown]
# ### Exercise L10.4 (LO-10.3, ★★, about 25 minutes)
#
# **Verify verbatim quotations.** A quote passes if it contains at least one visible character and occurs literally in the supplied section. Check against the retrieved sections only. In your notes give a true quote that would still fail to support a claim.

# %% tags=["answer-L10.4"]
def valid_quote(docs, ident, quote):
    raise NotImplementedError("L10.4")

# %% tags=["raises-exception"]
assert valid_quote(docs, "H04", "The shop has two loan bicycles.")
assert not valid_quote(docs[:1], "H04", "The shop has two loan bicycles.")
assert not valid_quote(docs, "H04", "The shop has three loan bicycles.")
assert not valid_quote(docs, "H04", " ")
print("passed")

# %% [markdown]
# ### Exercise L10.5 (LO-10.4, ★★, about 25 minutes)
#
# **Compare cached and uncached input.** In US dollars, return (uncached, cached) for one five-minute prefix write, followed by all hits. Charge suffix inputs for every request. Omit output because it is unchanged. Reject nonpositive requests.

# %% tags=["answer-L10.5"]
def cost(requests, prefix, suffix, rates):
    raise NotImplementedError("L10.5")

# %% tags=["raises-exception"]
a, b = cost(10, 10_000, 2_000, rates)
assert isclose(a, .48) and isclose(b, .148)
assert cost(1, 10_000, 2_000, rates)[1] > cost(1, 10_000, 2_000, rates)[0]
print("passed")

# %% [markdown]
# ## Summary
#
# You computed rankings and recall, checked citation text, and priced a repeat-use scenario.
