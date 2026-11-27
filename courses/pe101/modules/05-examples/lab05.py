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
# # Lab 5: Examples
#
# **Objectives** LO-5.1, LO-5.2, LO-5.3  
# **Prerequisites** The [Module 5 reading](index.md)  
# **Time** About 2.5 hours.
#
# Inspect the ticket pool, write demonstrations, and compare selection policies using their coverage.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
from collections import Counter
import re
from promptlab import load_json

pool = load_json("tickets.json")

from xml.etree import ElementTree

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Contrast cases
#
# The same word can appear in tickets for different queues. Inspect the two uses of brake.

# %%
print([(row["text"], row["label"]) for row in pool if "brake" in row["text"].lower()][:4])

# %% [markdown]
# ### Exercise L5.1 (LO-5.1, ★★, about 25 minutes)
#
# **Put examples in their own section.** Return XML with an examples root. For each row add example containing input and output text. The output uses Label: <queue>. Write your own contrast pair in your notes before checking.

# %% tags=["answer-L5.1"]
def examples_xml(rows):
    raise NotImplementedError("L5.1")

# %% tags=["raises-exception"]
tree = ElementTree.fromstring(examples_xml([pool[0], pool[13]]))
assert [e.findtext("output") for e in tree] == ["Label: repair", "Label: billing"]
assert tree[1].findtext("input") == pool[13]["text"]
print("passed")

# %% [markdown]
# ### Exercise L5.2 (LO-5.2, ★★, about 25 minutes)
#
# **Audit labels and lengths.** Return the label counts and short or long counts as two dictionaries. Split on whitespace. A short example has at most nine words. Compare the first four rows with the full pool and identify missing queues.

# %% tags=["answer-L5.2"]
def coverage(rows):
    raise NotImplementedError("L5.2")

# %% tags=["raises-exception"]
labels, lengths = coverage(pool)
assert labels == {"repair": 8, "billing": 8, "account": 8}
assert lengths["short"] + lengths["long"] == 24
assert coverage(pool[:4])[0] == {"repair": 4}
print("passed")

# %% [markdown]
# ### Exercise L5.3 (LO-5.3, ★★, about 25 minutes)
#
# **Tokenize into word sets.** Use the lowercased alphabetic runs matched by [a-z]+. Keep unique words only.

# %% tags=["answer-L5.3"]
def words(text):
    raise NotImplementedError("L5.3")

# %% tags=["raises-exception"]
assert words("Brake, BRAKE! Pad") == {"brake", "pad"}
assert words("$20") == set()
print("passed")

# %% [markdown]
# ### Exercise L5.4 (LO-5.3, LO-5.2, ★★, about 25 minutes)
#
# **Compare fixed and dynamic selections.** Implement Jaccard ranking over word sets. Break ties by ascending ID. If both sets are
#   empty, score zero. Return k rows and raise ValueError when k is outside the available range.
#   Compare the label counts of the dynamic results with a hand-picked balanced set for three
#   new queries. Hold the prompt template constant when you compare selections.

# %% tags=["answer-L5.4"]
def pick(text, rows, k):
    raise NotImplementedError("L5.4")

# %% tags=["raises-exception"]
query = "How do I update the email on my profile?"
assert pick(query, pool, 3)[0]["id"] == "T17"
assert pick("", pool[:3][::-1], 2) == pool[:2]
print("Fixed set:", coverage([pool[0], pool[8], pool[16]])[0])
print("Nearest set:", coverage(pick(query, pool, 3))[0])
print("passed")

# %% [markdown]
# ## Summary
#
# You built and inspected a demonstration pool. Nearest examples and balanced examples serve different aims.
