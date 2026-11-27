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
# # PA2: A prompt library
#
# **When** After [Module 4](../../modules/04-structure-data-and-templates/index.md)  
# **Time** About 3 hours  
# **Points** 19 for scoring your own work.
#
# You are preparing a versioned set of dispatch prompts for a bicycle repair shop. Write and
# score a routing prompt, a receipt-reply prompt, and a profile-change extraction prompt.
# Use the [prompt rubric](../../prompt-rubric.md) and record your draft and revised scores
# with the words that justify them. Keep both versions in your own work folder. The tests
# check coverage of key terms and exact text contracts. Read your prompts aloud to check whether
# a dispatcher could use them unaided.
#
# Replace the indicated lines in each answer cell and run the check below it. Restart the kernel
# and run all cells before you record your result. Keep the tests unchanged. The course's
# [policies](../../README.md#policies) apply.

# %% [markdown]
# ## Setup

# %%
from difflib import unified_diff
from string import Template
from xml.etree import ElementTree
from xml.sax.saxutils import escape
from promptlab import data_path, load_json

v1 = data_path("prompts/route-v1.txt").read_text(encoding="utf-8")
v2 = data_path("prompts/route-v2.xml").read_text(encoding="utf-8")

# %% [markdown]
# ## Problem 1: Assemble a request (LO-3.1, LO-3.2, LO-2.1, 5 points)
#
# Write a system prompt suitable for all dispatch tickets, naming the three queues and
#  exact label contract. Return a dictionary with model, system, max_tokens, and the single
#  user message containing ticket verbatim.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa2-1", "schema_version": 3, "task": false}
def request(ticket):
    ### BEGIN SOLUTION
    system = ("Route for the dispatcher. Use repair for service, billing for receipts and "
              "charges, and account for profiles. Prefer the current request. Return exactly "
              "Label: <queue>.")
    return {"model": "claude-opus-5-5", "system": system, "max_tokens": 60,
            "messages": [{"role": "user", "content": ticket}]}
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa2-1-tests", "schema_version": 3, "task": false, "points": 5}
r = request("Need a receipt")
assert set(r) == {"model", "system", "max_tokens", "messages"}
assert r["messages"] == [{"role": "user", "content": "Need a receipt"}]
assert all(x in r["system"] for x in ("repair", "billing", "account", "Label:"))
### BEGIN HIDDEN TESTS
other = request("profile update")
assert other["system"] == r["system"] and other["max_tokens"] > 0
assert len(other["messages"]) == 1
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 2: Check a receipt reply (LO-3.1, LO-3.3, 4 points)
#
# Write a separate prompt for a clerk who acknowledges the receipt request and may ask for
#  an invoice reference. Your checker returns True for exactly one nonempty line with at most
#  limit whitespace-separated words. Line breaks and leading or trailing spaces are disallowed.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa2-2", "schema_version": 3, "task": false}
def reply_format(text, limit=20):
    ### BEGIN SOLUTION
    return (text == text.strip() and bool(text) and len(text.splitlines()) == 1
            and 1 <= len(text.split()) <= limit)
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa2-2-tests", "schema_version": 3, "task": false, "points": 4}
assert reply_format("Could you share the invoice number?", 8)
assert not reply_format("One\nTwo", 5)
assert not reply_format("", 5)
### BEGIN HIDDEN TESTS
assert not reply_format("Lead space ", 5)
assert not reply_format("Too many words", 2)
assert not reply_format("line\rbreak", 5)
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 3: Render a versioned prompt (LO-4.1, LO-4.2, LO-4.3, 6 points)
#
# Render an XML template with string.Template. Only text nodes have fields. Require all and
#  only the declared keys. Raise ValueError for invalid templates or key mismatches. Escape each
#  value once and compare your versioned drafts to see which instructions changed.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa2-3", "schema_version": 3, "task": false}
def render_prompt(text, values):
    ### BEGIN SOLUTION
    template = Template(text)
    required = set(template.get_identifiers())
    if not template.is_valid() or set(values) != required:
        raise ValueError("Supply exactly the template fields.")
    return template.substitute({key: escape(value) for key, value in values.items()})
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa2-3-tests", "schema_version": 3, "task": false, "points": 6}
result = ElementTree.fromstring(render_prompt(v2, {"ticket": "A & B", "rules": "Route"}))
assert [child.tag for child in result] == ["ticket", "instructions", "question"]
assert result.findtext("ticket") == "A & B"
### BEGIN HIDDEN TESTS
assert render_prompt("<r>$value</r>", {"value": "</r> $9"}) == "<r>&lt;/r&gt; $9</r>"
for bad_values in ({}, {"x": "ok", "other": "extra"}):
    try:
        render_prompt("<t>$x</t>", bad_values)
    except ValueError:
        pass
    else:
        raise AssertionError("Key mismatch should fail.")
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 4: Extract and version profile changes (LO-3.1, LO-3.3, LO-4.3, 4 points)
#
# Draft a profile-field extraction prompt. Its versioned files should show an explicit
#  fallback for ambiguity. Implement a classifier for the exact answer forms `Field: email`,
#  `Field: address`, and `Field: unknown`. Return the field or None for invalid output.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa2-4", "schema_version": 3, "task": false}
def parse_field(text):
    ### BEGIN SOLUTION
    fields = {"Field: email": "email", "Field: address": "address", "Field: unknown": "unknown"}
    return fields.get(text)
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa2-4-tests", "schema_version": 3, "task": false, "points": 4}
assert parse_field("Field: unknown") == "unknown"
assert parse_field("Field: street") is None
### BEGIN HIDDEN TESTS
assert parse_field("Field: address") == "address"
assert parse_field("Field: email\n") is None
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Tools you used
#
# Say which tools you used and how, or write “none.”
