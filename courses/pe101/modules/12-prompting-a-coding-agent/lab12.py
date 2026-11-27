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
# # Lab 12: Prompting a coding agent
#
# **Objectives** LO-12.1, LO-12.2, LO-12.3  
# **Prerequisites** The [Module 12 reading](index.md)  
# **Time** About 2.5 hours.
#
# Trace an illustrative session, write two coding task prompts, and test an untouched copy of the fictional shop package before reviewing three diffs.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
import shutil
import subprocess
from tempfile import TemporaryDirectory
from promptlab import data_path, load_json

task = load_json("agent/task.json")
session = load_json("agent/session.json")
diffs = load_json("agent/diffs.json")
starter = data_path("agent/task.json").parents[2] / "starter-repo"

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Identify information sources
#
# Predict which event tells the agent how underscores work. Then inspect the trace.

# %%
print(session["source"])
for turn in session["turns"]:
    print(turn["event"], turn["origin"], turn["detail"], sep=" | ")

# %% [markdown]
# ### Exercise L12.1 (LO-12.1, ★★, about 25 minutes)
#
# **Find a decision following evidence.** Return zero-based positions of model events whose origin is tool_result. If an evidence field is absent, do not count the event. Explain exactly what the preceding tool outputs supplied.

# %% tags=["answer-L12.1"]
def decision_positions(turns):
    raise NotImplementedError("L12.1")

# %% tags=["raises-exception"]
assert decision_positions(session["turns"]) == [3, 5]
assert decision_positions([{"event": "model"}]) == []
print("passed")

# %% [markdown]
# ### Exercise L12.2 (LO-12.2, ★★, about 25 minutes)
#
# **Write a checkable agent task.** Return a prompt with the goal verbatim, both file names, each constraint, and the verification command. Score it with the prompt rubric. Draft a second prompt for preventing a pricing regression and score it in your notes.

# %% tags=["answer-L12.2"]
def task_prompt(task):
    raise NotImplementedError("L12.2")

# %% tags=["raises-exception"]
prompt = task_prompt(task)
assert all(item in prompt for item in [task["goal"], task["verification"],
                                       *task["files"], *task["constraints"]])
assert "Report" in prompt
print("passed")

# %% [markdown]
# ### Exercise L12.3 (LO-12.3, ★★, about 25 minutes)
#
# **Supply a local check command.** Copy the starter to a scratch directory. Implement a function that invokes the current Python with unittest discover -v. Run it in the supplied path, capture text output, and return the return code. Use an argument list and let subprocess run without a shell.

# %% tags=["answer-L12.3"]
def check_package(path):
    raise NotImplementedError("L12.3")

# %% tags=["raises-exception"]
with TemporaryDirectory() as scratch:
    work = shutil.copytree(starter, scratch, dirs_exist_ok=True)
    assert check_package(work) == 0
print("passed")

# %% [markdown]
# ### Exercise L12.4 (LO-12.3, ★★, about 25 minutes)
#
# **Review three diffs.** For A, B, and C, return a dictionary keyed by IDs with the values accept, regression, or out_of_scope. Read the actual diffs and write the exact changed line that supports each review. Do not apply any draft.

# %% tags=["answer-L12.4"]
def reviews():
    raise NotImplementedError("L12.4")

# %% tags=["raises-exception"]
for draft in diffs:
    print(draft["id"], draft["source"], draft["diff"], sep="\n")
assert reviews() == {"A": "accept", "B": "regression", "C": "out_of_scope"}
print("passed")

# %% [markdown]
# ## Summary
#
# You reconstructed a session, scored reproducible task prompts, ran a trusted local check, and reviewed three illustrative changes.
