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
# # Lab 4: Structure, data, and templates
#
# **Objectives** LO-4.1, LO-4.2, LO-4.3  
# **Prerequisites** The [Module 4 reading](index.md)  
# **Time** About 2.5 hours.
#
# Round-trip customer text through a prompt template and review two versions of the prompt.
#
# Use a fresh kernel and run the cells from top to bottom. Fill each answer cell, then run its
# check. The checks raise errors until their exercises are complete. This notebook runs locally.

# %% [markdown]
# ## Setup

# %%
import sys
from difflib import unified_diff
from string import Template
from xml.etree import ElementTree
from xml.sax.saxutils import escape
from promptlab import data_path, load_json

v1 = data_path("prompts/route-v1.txt").read_text(encoding="utf-8")
v2 = data_path("prompts/route-v2.xml").read_text(encoding="utf-8")

print("Python", sys.version.split()[0])

# %% [markdown]
# ## Predict the parse
#
# The customer values contain characters used by XML. Predict which of the two parses fails.

# %%
ticket = "Brake cable & housing < $20"
for serial in ("<ticket>" + ticket + "</ticket>", "<ticket>" + escape(ticket) + "</ticket>"):
    try:
        print(ElementTree.fromstring(serial).text)
    except ElementTree.ParseError:
        print("The XML parser rejected the text.")

# %% [markdown]
# ### Exercise L4.1 (LO-4.1, ★★, about 25 minutes)
#
# **Build the document prompt.** Use one root named prompt. Add documents, instructions, and question in that order. Documents holds doc, whose text is document. Build it with the XML library and return Unicode XML.

# %% tags=["answer-L4.1"]
def layout(document, instructions, question):
    raise NotImplementedError("L4.1")

# %% tags=["raises-exception"]
root = ElementTree.fromstring(layout("use a size < 18", "Quote the size", "Which size?"))
assert [child.tag for child in root] == ["documents", "instructions", "question"]
assert root.findtext("documents/doc") == "use a size < 18"
assert root.findtext("question") == "Which size?"
print("passed")

# %% [markdown]
# ### Exercise L4.2 (LO-4.2, ★★, about 25 minutes)
#
# **Recover literal closing tags.** Return a two-tuple containing the naive interpolation and a safe version. Both use a single outer ticket tag. Use a local XML parser to see what happens when the input contains the literal text </ticket>. Explain what the parse result says about this representation.

# %% tags=["answer-L4.2"]
def serialize_ticket(value):
    raise NotImplementedError("L4.2")

# %% tags=["raises-exception"]
value = "The label on the sample says </ticket> & is damp."
bad, good = serialize_ticket(value)
try:
    ElementTree.fromstring(bad)
except ElementTree.ParseError:
    pass
else:
    raise AssertionError("The naive representation should fail the local parser.")
assert ElementTree.fromstring(good).text == value
print("passed")

# %% [markdown]
# ### Exercise L4.3 (LO-4.2, LO-4.3, ★★, about 25 minutes)
#
# **Render exactly the declared fields.** Use string.Template. Raise ValueError for invalid templates, missing fields, or extra fields. Escape every supplied value once. Return the substituted string.

# %% tags=["answer-L4.3"]
def render(text, values):
    raise NotImplementedError("L4.3")

# %% tags=["raises-exception"]
final = ElementTree.fromstring(render(v2, {"ticket": "Pads & cables $20", "rules": "Route."}))
assert final.findtext("ticket") == "Pads & cables $20"
assert final.findtext("instructions") == "Route."
for values in ({}, {"x": "1", "y": "2"}):
    try:
        render("<x>$x</x>", values)
    except ValueError:
        pass
    else:
        raise AssertionError("Require exactly x.")
print("passed")

# %% [markdown]
# ### Exercise L4.4 (LO-4.3, ★★, about 25 minutes)
#
# **Review a version change.** Return the unified line diff from first to second as text. Label its files v1 and v2. In your notes explain the change you would expect to help with ambiguous tickets.

# %% tags=["answer-L4.4"]
def compare(first, second):
    raise NotImplementedError("L4.4")

# %% tags=["raises-exception"]
delta = compare(v1, v2)
assert delta.startswith("--- v1\n+++ v2\n")
assert "-Sort this ticket." in delta and "+  <ticket>$ticket</ticket>" in delta
assert compare(v1, v1) == ""
print("passed")

# %% [markdown]
# ## Summary
#
# You preserved the template structure, round-tripped customer text, and inspected the changes between two versions.
