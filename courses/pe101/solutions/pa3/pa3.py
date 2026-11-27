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
# # PA3: An evaluated classifier
#
# **When** After [Module 7](../../modules/07-evaluating-prompts/index.md)  
# **Time** About 3 hours  
# **Points** 20 for scoring your own work.
#
# Build and audit a small dispatch evaluation. Use the bundled cases for the numeric checks
# and write a separate six-case test set of your own. Include typical tickets, edge cases, and
# misleading wording. Reserve at least two cases for a final check and write one sentence
# explaining the expected queue for each. Label every illustrative response you write.
#
# Replace the indicated lines in each answer cell and run the check below it. Restart the kernel
# and run all cells before you record your result. Keep the tests unchanged. The course's
# [policies](../../README.md#policies) apply.

# %% [markdown]
# ## Setup

# %%
from collections import Counter
from math import isclose, sqrt
from random import Random
import re
from statistics import mean
from promptlab import load_json

cases = load_json("evaluation/cases.json")
judgments = load_json("evaluation/judgments.json")

from promptlab.evaluation import paired_bootstrap
from xml.etree import ElementTree

# %% [markdown]
# ## Problem 1: Select a contrast set (LO-5.1, LO-5.2, LO-5.3, 4 points)
#
# Select exactly one example from each queue in the order repair, billing, account. Use Jaccard similarity on lowercased alphabetic word sets. Break ties by ID. Raise ValueError if a queue has no examples. Write the selected rows as input/output example blocks in your prompt draft.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa3-1", "schema_version": 3, "task": false}
def select(query, pool):
    ### BEGIN SOLUTION
    words = lambda text: set(re.findall(r"[a-z]+", text.lower()))
    query_words = words(query)
    def score(row):
        terms = words(row["text"])
        return (-len(query_words & terms) / max(1, len(query_words | terms)), row["id"])
    out = []
    for label in ("repair", "billing", "account"):
        out.append(min((r for r in pool if r["label"] == label), key=score))
    return out
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa3-1-tests", "schema_version": 3, "task": false, "points": 4}
pool = load_json("tickets.json")
examples = select(pool[13]["text"], pool)
assert [r["label"] for r in examples] == ["repair", "billing", "account"]
assert examples[1]["id"] == "T14"
### BEGIN HIDDEN TESTS
assert [row["id"] for row in select("", pool)] == ["T01", "T09", "T17"]
assert select("", list(reversed(pool))) == select("", pool)
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 2: Parse and grade a classifier (LO-6.2, LO-3.3, LO-7.2, 3 points)
#
# Parse each response using the exact label contract. Return the number of correct runs for a row and version. Compare text to the reference exactly. In a separate prompt draft, ask for tagged evidence and exactly one tagged answer and explain what would be validated.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa3-2", "schema_version": 3, "task": false}
def correct_runs(row, version):
    ### BEGIN SOLUTION
    return sum(response == f"Label: {row['expected']}" for response in row[version])
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa3-2-tests", "schema_version": 3, "task": false, "points": 3}
assert correct_runs({"expected": "repair", "A": ["Label: repair", "repair"]}, "A") == 1
### BEGIN HIDDEN TESTS
assert correct_runs({"expected": "billing", "A": ["Label: billing\n"]}, "A") == 0
assert correct_runs({"expected": "account", "B": []}, "B") == 0
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 3: Require one final section (LO-6.2, 3 points)
#
# Extract exactly one nonempty answer tag, trimming its contents. Raise ValueError for malformed or repeated sections. Use re.DOTALL.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa3-3", "schema_version": 3, "task": false}
def extract(text):
    ### BEGIN SOLUTION
    if text.count("<answer>") != 1 or text.count("</answer>") != 1:
        raise ValueError("Expected exactly one opening and one closing answer tag.")
    matches = re.findall(r"<answer>(.*?)</answer>", text, flags=re.DOTALL)
    if len(matches) != 1 or not matches[0].strip():
        raise ValueError("Expected one nonempty answer section.")
    return matches[0].strip()
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa3-3-tests", "schema_version": 3, "task": false, "points": 3}
assert extract("<why>invoice</why><answer>billing</answer>") == "billing"
### BEGIN HIDDEN TESTS
for text in ("", "<answer> </answer>", "<answer>x</answer><answer>y</answer>",
             "<answer><answer>billing</answer>"):
    try:
        extract(text)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid answer passed.")
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 4: Keep cases paired (LO-7.1, LO-7.3, LO-7.4, 5 points)
#
# Use only rows in split. For each version compute normalized case scores in the input order. Return paired_bootstrap on those scores using the helper defaults. Explain how you protect split integrity.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa3-4", "schema_version": 3, "task": false}
def compare(rows, split):
    ### BEGIN SOLUTION
    group = [r for r in rows if r["split"] == split]
    scores = [[correct_runs(r, version) / len(r[version]) for r in group]
              for version in ("A", "B")]
    return paired_bootstrap(*scores)
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa3-4-tests", "schema_version": 3, "task": false, "points": 5}
estimate, lo, hi = compare(cases, "dev")
assert lo <= estimate <= hi and estimate > 0
### BEGIN HIDDEN TESTS
one = {"split": "holdout", "expected": "repair", "A": [""], "B": ["Label: repair"]}
assert compare([one], "holdout") == (1, 1, 1)
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 5: Agreement and intervals (LO-7.2, LO-7.3, 5 points)
#
# Implement agreement from Lab 7 and Wilson's interval using z=1.96. Return a four-tuple with observed agreement, kappa (None when undefined), and the Wilson interval endpoints around passes of total.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa3-5", "schema_version": 3, "task": false}
def stats(rows, passes, total):
    ### BEGIN SOLUTION
    n = len(rows)
    if not n or total <= 0 or not 0 <= passes <= total:
        raise ValueError("Need judgments and a valid trial count.")
    observed = sum(r["human"] == r["judge"] for r in rows) / n
    p, q = (sum(r[key] for r in rows) / n for key in ("human", "judge"))
    expected = p*q + (1-p)*(1-q)
    kappa = (observed-expected) / (1-expected) if expected < 1 else None
    z = 1.96
    rate = passes / total
    scale = 1 + z**2 / total
    center = (rate + z**2 / (2*total)) / scale
    radius = z * sqrt(rate*(1-rate)/total + z**2/(4*total**2)) / scale
    return observed, kappa, max(0, center-radius), min(1, center+radius)
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa3-5-tests", "schema_version": 3, "task": false, "points": 5}
obs, k, lo, hi = stats(judgments, 8, 10)
assert isclose(obs, 0.8) and 0 < k < obs
assert 0.48 < lo < 0.50 and 0.94 < hi < 0.95
### BEGIN HIDDEN TESTS
obs, k, lo, hi = stats([{"human": False, "judge": False}], 0, 10)
assert obs == 1 and k is None and isclose(lo, 0, abs_tol=1e-12) and 0 < hi < 0.5
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Tools you used
#
# Say which tools you used and how, or write “none.”
