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
# # Lab 7: Evaluating prompts
#
# **Objectives** LO-7.1, LO-7.2, LO-7.3, LO-7.4  
# **Prerequisites** The [Module 7 reading](index.md)  
# **Time** About 2.5 hours.
#
# Evaluate two prompt versions using 40 hand-written ticket cases, three illustrative runs per version, and 30 paired grader judgments.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
from collections import Counter
from math import isclose, sqrt
from random import Random
import re
from statistics import mean
from promptlab import load_json

cases = load_json("evaluation/cases.json")
judgments = load_json("evaluation/judgments.json")

import matplotlib
import matplotlib.pyplot as plt

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Inspect provenance and coverage
#
# Before looking at B, predict which kind of error the exact grader catches. Keep the holdout split for the final check.

# %%
print(cases[0]["source"])
print(Counter(row["kind"] for row in cases))
print(Counter(row["split"] for row in cases))

# %% [markdown]
# ### Exercise L7.1 (LO-7.1, LO-7.4, ★★, about 25 minutes)
#
# **Split by case rather than response.** Return development and held-out lists without dropping or duplicating a case. Raise ValueError if an ID repeats or a split label is unfamiliar. In your notes add one case of each kind with its rationale.

# %% tags=["answer-L7.1"]
def split_rows(rows):
    raise NotImplementedError("L7.1")

# %% tags=["raises-exception"]
dev, holdout = split_rows(cases)
assert (len(dev), len(holdout)) == (30, 10)
assert {x["id"] for x in dev}.isdisjoint({x["id"] for x in holdout})
assert {"typical", "edge", "adversarial"} == {r["kind"] for r in cases}
print("passed")

# %% [markdown]
# ### Exercise L7.2 (LO-7.2, ★★, about 25 minutes)
#
# **Separate format from correctness.** Return a dictionary with format and correct booleans. A correct response passes format and has the expected label. Match the entire text.

# %% tags=["answer-L7.2"]
def grade(text, expected):
    raise NotImplementedError("L7.2")

# %% tags=["raises-exception"]
assert grade("Label: repair", "billing") == {"format": True, "correct": False}
assert grade("billing", "billing") == {"format": False, "correct": False}
assert grade("Label: billing", "billing") == {"format": True, "correct": True}
print("passed")

# %% [markdown]
# ### Exercise L7.3 (LO-7.2, ★★, about 25 minutes)
#
# **Measure judge agreement.** For rows with boolean human and judge labels, return observed agreement and kappa. Raise ValueError for zero rows and return None for kappa when chance agreement is one.

# %% tags=["answer-L7.3"]
def agreement(rows):
    raise NotImplementedError("L7.3")

# %% tags=["raises-exception"]
observed, kappa = agreement(judgments)
assert isclose(observed, 0.8)
assert 0 < kappa < observed
assert agreement([{"human": True, "judge": True}]) == (1, None)
print("passed")

# %% [markdown]
# ### Exercise L7.4 (LO-7.3, ★★, about 25 minutes)
#
# **Implement Wilson's score interval.** Return lower and upper endpoints from the reading's formula. Clamp roundoff to the range from 0 to 1. Raise ValueError for nonpositive total or a count outside the range.

# %% tags=["answer-L7.4"]
def wilson(successes, total, z=1.96):
    raise NotImplementedError("L7.4")

# %% tags=["raises-exception"]
low, high = wilson(8, 10)
assert 0.48 < low < 0.50 and 0.94 < high < 0.95
assert isclose(wilson(0, 6)[0], 0, abs_tol=1e-12)
assert isclose(wilson(6, 6)[1], 1, abs_tol=1e-12)
print("passed")

# %% [markdown]
# ### Exercise L7.5 (LO-7.3, LO-7.4, ★★, about 25 minutes)
#
# **Bootstrap pairs and read the plot.** Implement a paired percentile bootstrap that returns estimate, lower, and upper.
#   Match case means by position and resample differences with a fresh seeded Random.
#   For each resample draw len(a) differences with replacement. Use sorted sample positions
#   int(0.025*(repeats-1)) and int(0.975*(repeats-1)). Compare on development, then inspect
#   held-out data once. This plot's horizontal axis is B minus A, in proportion points.
#   Its two lines show 95% paired bootstrap intervals for development and held-out cases.

# %% tags=["answer-L7.5"]
def paired(a, b, repeats=2000, seed=101):
    raise NotImplementedError("L7.5")

# %% tags=["raises-exception"]
assert paired([0, 0], [1, 1]) == (1, 1, 1)

def case_scores(rows, version):
    return [mean(grade(reply, r["expected"])["correct"] for reply in r[version]) for r in rows]

fig, ax = plt.subplots(figsize=(7, 3))
for position, (label, rows) in enumerate([("Development", dev), ("Held out", holdout)]):
    estimate, lower, upper = paired(case_scores(rows, "A"), case_scores(rows, "B"))
    ax.hlines(position, lower, upper, color="black")
    ax.plot(estimate, position, "o", color="tab:blue")
    print(label, f"change={estimate:.3f}, interval [{lower:.3f}, {upper:.3f}]")
ax.set_yticks([0, 1], ["Development", "Held out"])
ax.axvline(0, color="0.5", linestyle="--")
ax.set_xlabel("B minus A (proportion points)")
ax.set_title("Paired case intervals on illustrative responses")
plt.show()
print("passed")

# %% [markdown]
# ## Summary
#
# You built a grader, measured agreement, and used a case-level interval to compare illustrative versions.
