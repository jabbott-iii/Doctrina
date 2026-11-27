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
# # Lab 6: Reasoning and chains
#
# **Objectives** LO-6.1, LO-6.2, LO-6.3  
# **Prerequisites** The [Module 6 reading](index.md)  
# **Time** About 2.5 hours.
#
# Choose an effort level from fictional observations, validate answer boundaries, and trace a three-stage scripted chain.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
from math import prod, isclose
import re
from promptlab import ScriptedModel

measurements = [
    {"effort": "low", "accuracy": 0.85, "seconds": 1.2, "cost": 4},
    {"effort": "medium", "accuracy": 0.92, "seconds": 2.0, "cost": 7},
    {"effort": "high", "accuracy": 0.94, "seconds": 3.4, "cost": 12},
]

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Set constraints first
#
# These values are illustrative. Predict which row meets 90% accuracy and 2.5 seconds at least cost.

# %%
for row in measurements:
    print(row)

# %% [markdown]
# ### Exercise L6.1 (LO-6.1, ★★, about 25 minutes)
#
# **Find the cheapest qualifying row.** Use inclusive accuracy and latency thresholds. Break cost ties by lower latency, then effort name. Return the effort string or None when no level qualifies.

# %% tags=["answer-L6.1"]
def choose(rows, min_accuracy, max_seconds):
    raise NotImplementedError("L6.1")

# %% tags=["raises-exception"]
assert choose(measurements, 0.9, 2.5) == "medium"
assert choose(measurements, 0.92, 2) == "medium"
assert choose(measurements, 0.99, 10) is None
print("passed")

# %% [markdown]
# ### Exercise L6.2 (LO-6.2, ★★, about 25 minutes)
#
# **Extract a final answer.** Extract one exact lowercase answer section, stripping its surrounding whitespace. Use re.DOTALL to match multiline text. Raise ValueError for a missing, empty, or repeated section.

# %% tags=["answer-L6.2"]
def extract(text):
    raise NotImplementedError("L6.2")

# %% tags=["raises-exception"]
assert extract("<evidence>receipt</evidence><answer> billing </answer>") == "billing"
for text in ("no answer", "<answer> </answer>", "<answer>a</answer><answer>b</answer>",
             "<answer><answer>billing</answer>"):
    try:
        extract(text)
    except ValueError:
        pass
    else:
        raise AssertionError("Reject malformed final answers.")
print("passed")

# %% [markdown]
# ### Exercise L6.3 (LO-6.3, ★★, about 25 minutes)
#
# **Pass the original input forward.** Call the stand-in three times with one user turn, beginning each turn with classify, draft,
#   or check followed by a newline. Include the original ticket at each step. Include the extracted
#   label in draft and the extracted reply in check. Return the reply when the final extracted
#   answer is approved and None otherwise.

# %% tags=["answer-L6.3"]
def chain(model, ticket):
    raise NotImplementedError("L6.3")

# %% tags=["raises-exception"]
model = ScriptedModel(["<answer>billing</answer>", "<answer>Please share the invoice ID.</answer>",
                       "<answer>approved</answer>"])
assert chain(model, "Please send the receipt") == "Please share the invoice ID."
assert model.calls == 3
assert "billing" in model.requests[1]["messages"][0]["content"]
assert "Please share the invoice ID." in model.requests[2]["messages"][0]["content"]
print("passed")

# %% [markdown]
# ### Exercise L6.4 (LO-6.3, ★★, about 25 minutes)
#
# **Measure error propagation.** Return a tuple with all-correct probability and undetected-failure probability. Multiply
#   conditional stage success probabilities. The check catches fraction caught of the remaining
#   failures. Assume it accepts the correct ones.

# %% tags=["answer-L6.4"]
def error_budget(stage_rates, caught):
    raise NotImplementedError("L6.4")

# %% tags=["raises-exception"]
passed, missed = error_budget([0.9, 0.9, 0.9], 0.5)
assert isclose(passed, 0.729) and isclose(missed, 0.1355)
assert error_budget([0.5, 0.5], 1) == (0.25, 0.0)
print("passed")

# %% [markdown]
# ## Summary
#
# You compared effort settings with practice measurements, extracted a final answer, and measured the effect of a check step.
