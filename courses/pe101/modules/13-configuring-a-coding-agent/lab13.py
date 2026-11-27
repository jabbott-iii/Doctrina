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
# # Lab 13: Configuring a coding agent
#
# **Objectives** LO-13.1, LO-13.2, LO-13.3  
# **Prerequisites** The [Module 13 reading](index.md)  
# **Time** About 2.5 hours.
#
# Draft project guidance, a reusable review skill, and a deny-only hook. Test every step without starting a coding agent.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
import json
from pathlib import PurePosixPath
import subprocess
import yaml

read_event = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
              "tool_input": {"command": "python -m unittest discover -v"}}
unknown_event = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
                 "tool_input": {"command": "sample-action"}}

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Inspect an event
#
# Predict what the policy will return for each proposal. The event is sample data.

# %%
print(json.dumps([read_event, unknown_event], indent=2))

# %% [markdown]
# ### Exercise L13.1 (LO-13.1, ★★, about 25 minutes)
#
# **Write two instruction files.** Return a dictionary keyed by CLAUDE.md and .claude/rules/fixtures.md. Project instructions must name integer cents and the test command. Give the rule front matter with paths set to a list containing data/**, and add fixture-specific guidance.

# %% tags=["answer-L13.1"]
def instructions():
    raise NotImplementedError("L13.1")

# %% tags=["raises-exception"]
files = instructions()
assert "integer cents" in files["CLAUDE.md"]
assert "python -m unittest discover -v" in files["CLAUDE.md"]
rule = files[".claude/rules/fixtures.md"]
assert yaml.safe_load(rule.split("---", 2)[1]) == {"paths": ["data/**"]}
print("passed")

# %% [markdown]
# ### Exercise L13.2 (LO-13.1, ★★, about 25 minutes)
#
# **Resolve a small set of path scopes.** Return True for an exact relative path or a directory prefix ending in /**. Match whole path components using PurePosixPath. Require a descendant for the prefix case. This checker is limited to these two forms.

# %% tags=["answer-L13.2"]
def matches(path, pattern):
    raise NotImplementedError("L13.2")

# %% tags=["raises-exception"]
assert matches("data/archive/tickets.json", "data/**")
assert not matches("database/records.json", "data/**")
assert not matches("data", "data/**")
assert matches("repair_shop.py", "repair_shop.py")
print("passed")

# %% [markdown]
# ### Exercise L13.3 (LO-13.2, ★★, about 25 minutes)
#
# **Describe a review skill.** Return a complete SKILL.md string. The YAML has name review-labels and a description. The body includes steps to inspect the diff, run regression tests, and summarize evidence. Write down one bounded task you would delegate and one you would keep.

# %% tags=["answer-L13.3"]
def skill():
    raise NotImplementedError("L13.3")

# %% tags=["raises-exception"]
text = skill()
front = yaml.safe_load(text.split("---", 2)[1])
assert front["name"] == "review-labels" and front["description"].strip()
assert {"diff", "regression", "evidence"} <= set(text.lower().replace(".", "").split())
print("passed")

# %% [markdown]
# ### Exercise L13.4 (LO-13.3, ★★, about 25 minutes)
#
# **Set a permission rule.** Return a settings dictionary whose permissions allow list contains only the exact documented
#   test command using Bash(...) syntax. Configure a PreToolUse matcher for Bash with a command
#   hook running the project script .claude/hooks/review_command.py via Python. In notes explain
#   the effect of this hook and the effect of removing it.

# %% tags=["answer-L13.4"]
def settings():
    raise NotImplementedError("L13.4")

# %% tags=["raises-exception"]
config = settings()
assert config["permissions"]["allow"] == ["Bash(python -m unittest discover -v)"]
rule = config["hooks"]["PreToolUse"][0]
assert rule["matcher"] == "Bash" and rule["hooks"][0]["type"] == "command"
assert "review_command.py" in rule["hooks"][0]["command"]
print("passed")

# %% [markdown]
# ### Exercise L13.5 (LO-13.3, ★★, about 25 minutes)
#
# **Test a deny-only hook.** Return the full source for a Python script. Read one JSON event from stdin. Emit no output
#   for the exact PreToolUse Bash test proposal. For any other or malformed JSON, print an object
#   under hookSpecificOutput with hookEventName PreToolUse, permissionDecision deny, and a reason.
#   Exit zero after writing a decision. Test by piping events into a Python subprocess. The
#   handler examines the command string and never runs it.

# %% tags=["answer-L13.5"]
def hook_source():
    raise NotImplementedError("L13.5")

# %% tags=["raises-exception"]
def run_hook(payload):
    process = subprocess.run([sys.executable, "-c", hook_source()], input=payload,
                             capture_output=True, text=True, check=True, timeout=5)
    return process.stdout

assert run_hook(json.dumps(read_event)) == ""
for payload in (json.dumps(unknown_event), "{", "[]", '{"tool_input": null}'):
    decision = json.loads(run_hook(payload))["hookSpecificOutput"]
    assert decision["hookEventName"] == "PreToolUse"
    assert decision["permissionDecision"] == "deny" and decision["permissionDecisionReason"]
print("passed")

# %% [markdown]
# ## Summary
#
# You placed project guidance by scope, authored a repeatable skill, and tested a deny-only handler using piped JSON.
