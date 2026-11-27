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
# # PA5: Answers from documents, defended
#
# **When** After [Module 11](../../modules/11-prompt-injection/index.md)  
# **Time** About 3 hours  
# **Points** 25 for scoring your own work.
#
# Write an offline handbook assistant. Keep your grounded prompt with a short report on
# retrieval coverage, exact evidence, and which defensive controls each fixture exercises.
# Use synthetic records for policy outcomes. For your own fixture tests include unapproved
# requests and legitimate controls. Keep any invented replies clearly labeled.
#
# Replace the indicated lines in each answer cell and run the check below it. Restart the kernel
# and run all cells before you record your result. Keep the tests unchanged. The course's
# [policies](../../README.md#policies) apply.

# %% [markdown]
# ## Setup

# %%
from collections import Counter
from math import isclose, log1p
import re
from statistics import mean
from xml.etree import ElementTree
from promptlab import load_json

docs = load_json("handbook/sections.json")
questions = load_json("handbook/questions.json")
rates = load_json("prices.json")["models"]["claude-opus-5-5"]

from xml.etree import ElementTree
from promptlab import load_json
from promptlab.review import GullibleModel, classify

cases = load_json("safety/review-cases.json")
replay = GullibleModel()

from jsonschema import validate, ValidationError
from promptlab.evaluation import wilson

ANSWER_SCHEMA = {"type": "object", "properties": {
    "section": {"type": "string"}, "quote": {"type": "string", "minLength": 1}},
    "required": ["section", "quote"], "additionalProperties": False}

# %% [markdown]
# ## Problem 1: Rank handbook sections (LO-10.2, 5 points)
#
# Implement BM25 as in Lab 10. Rank by decreasing score then ID with k1=1.2 and b=0.75.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa5-1", "schema_version": 3, "task": false}
def bm25(query, docs, *, k1=1.2, b=0.75):
    ### BEGIN SOLUTION
    if not docs:
        return []
    counts = [Counter(re.findall(r"[a-z]+", doc["text"].lower())) for doc in docs]
    lengths = [sum(counter.values()) for counter in counts]
    mean_length = mean(lengths)
    terms = set(re.findall(r"[a-z]+", query.lower()))
    frequencies = {term: sum(term in counter for counter in counts) for term in terms}
    scores = []
    for doc, counter, length in zip(docs, counts, lengths, strict=True):
        score = 0.0
        for term in sorted(terms & counter.keys()):
            df = frequencies[term]
            idf = log1p((len(docs) - df + 0.5) / (df + 0.5))
            tf = counter[term]
            norm = k1 * (1 - b + b * length / mean_length)
            score += idf * tf * (k1 + 1) / (tf + norm)
        scores.append((doc["id"], score))
    return sorted(scores, key=lambda pair: (-pair[1], pair[0]))
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa5-1-tests", "schema_version": 3, "task": false, "points": 5}
assert bm25("loan bicycles", docs)[0][0] == "H04"
assert bm25("parking", []) == []
### BEGIN HIDDEN TESTS
assert bm25("used blades container", docs)[0][0] == "H06"
assert bm25("stock", docs) == bm25("stock stock", docs)
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 2: Report coverage and uncertainty (LO-10.2, LO-7.3, 4 points)
#
# Return mean recall at k and the Wilson interval (a pair) for the share of questions with every required section retrieved. Assume independent questions for the interval calculation. Explain why related paraphrases weaken that assumption.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa5-2", "schema_version": 3, "task": false}
def coverage(questions, docs, k):
    ### BEGIN SOLUTION
    scores = []
    for q in questions:
        retrieved = {ident for ident, score in bm25(q["question"], docs)[:k]}
        expected = set(q["relevant"])
        scores.append(len(retrieved & expected) / len(expected))
    return mean(scores), wilson(sum(x == 1 for x in scores), len(scores))
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa5-2-tests", "schema_version": 3, "task": false, "points": 4}
result, span = coverage(questions, docs, 10)
assert result == 1 and 0.9 < span[0] <= span[1] == 1
### BEGIN HIDDEN TESTS
rate, span = coverage(questions, docs, 0)
assert rate == 0 and span[0] < 1e-12 and span[1] > 0
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 3: Build a prompt from sources (LO-10.1, LO-4.2, 4 points)
#
# Build the XML prompt shape from Lab 10. Ask for exact evidence and include an abstention option.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa5-3", "schema_version": 3, "task": false}
def grounded_prompt(docs, question):
    ### BEGIN SOLUTION
    root = ElementTree.Element("prompt")
    group = ElementTree.SubElement(root, "documents")
    for doc in docs:
        ElementTree.SubElement(group, "doc", id=doc["id"]).text = doc["text"]
    ElementTree.SubElement(root, "instructions").text = (
        'Quote exact evidence with its section ID or answer "I don\'t know".'
    )
    ElementTree.SubElement(root, "question").text = question
    return ElementTree.tostring(root, encoding="unicode")
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa5-3-tests", "schema_version": 3, "task": false, "points": 4}
root = ElementTree.fromstring(grounded_prompt(docs[:2], "Cables & tubes?"))
assert [e.tag for e in root] == ["documents", "instructions", "question"]
assert root.findtext("question") == "Cables & tubes?"
### BEGIN HIDDEN TESTS
sample = [{"id": "X&1", "text": "Cable < casing"}]
doc = ElementTree.fromstring(grounded_prompt(sample, "What?")).find("documents/doc")
assert doc.attrib == {"id": "X&1"} and doc.text == "Cable < casing"
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 4: Check precise evidence (LO-10.3, LO-8.1, 4 points)
#
# Validate a record against ANSWER_SCHEMA. Return True only if its section is in the retrieved documents and its nonblank quote occurs in that section. Return False for validation failures.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa5-4", "schema_version": 3, "task": false}
def verify_answer(record, docs):
    ### BEGIN SOLUTION
    try:
        validate(record, ANSWER_SCHEMA)
    except ValidationError:
        return False
    return bool(record["quote"].strip()) and any(
        record["section"] == doc["id"] and record["quote"] in doc["text"] for doc in docs
    )
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa5-4-tests", "schema_version": 3, "task": false, "points": 4}
assert verify_answer({"section":"H04","quote":"two loan bicycles"}, docs)
assert not verify_answer({"section":"H04","quote":"three loan bicycles"}, docs)
### BEGIN HIDDEN TESTS
assert not verify_answer({"section":"H04","quote":" "}, docs)
assert not verify_answer({"section":"H04","quote":"two loan bicycles"}, docs[:2])
assert not verify_answer(["H04", "two loan bicycles"], docs)
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 5: Report cached input costs (LO-10.4, 3 points)
#
# Implement the two dollar costs from Lab 10 with one write and an all-hit prefix after the first request. Omit output. Raise ValueError for nonpositive requests.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa5-5", "schema_version": 3, "task": false}
def cost(requests, prefix, suffix, rates):
    ### BEGIN SOLUTION
    if requests <= 0:
        raise ValueError("At least one request is required.")
    uncached = requests * (prefix + suffix) * rates["input"]
    cached = (prefix*rates["cache_write_5m"] + (requests-1)*prefix*rates["cache_read"]
              + requests*suffix*rates["input"])
    return uncached / 1_000_000, cached / 1_000_000
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa5-5-tests", "schema_version": 3, "task": false, "points": 3}
assert all(isclose(x, y) for x, y in zip(cost(10, 10_000, 2000, rates), (.48, .148)))
### BEGIN HIDDEN TESTS
assert cost(2, 0, 1_000, rates) == (.008, .008)
assert cost(1, 0, 0, rates) == (0, 0)
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 6: Test a policy with controls (LO-11.1, LO-11.2, LO-11.3, 5 points)
#
# Return an outcome for the inert proposal. In baseline mode accept every replay. Otherwise
#   deny unlisted actions and require an exact host approval ID for the sample label change.
#   The host_approvals set contains approved case IDs and is independent of the fixture claims.
#   Group your results by direct and indirect origin and report unauthorized acceptance with a
#   denominator. Include a permitted approved control and one forged approval flag in your notes.

# %% nbgrader={"grade": false, "solution": true, "locked": false, "grade_id": "pa5-6", "schema_version": 3, "task": false}
def outcome(case, allowed, host_approvals, baseline=False):
    ### BEGIN SOLUTION
    proposal = replay(case)
    if baseline:
        return "accepted"
    if proposal["name"] not in allowed:
        return "denied"
    if proposal["name"] == "change_label" and case["id"] not in host_approvals:
        return "needs_review"
    return "accepted"
    ### END SOLUTION

# %% nbgrader={"grade": true, "solution": false, "locked": true, "grade_id": "pa5-6-tests", "schema_version": 3, "task": false, "points": 5}
assert all(outcome(r, {"change_label"}, set(), True) == "accepted" for r in cases)
assert all(outcome(r, {"change_label"}, set()) == "needs_review" for r in cases)
assert outcome(cases[0], {"change_label"}, {cases[0]["id"]}) == "accepted"
### BEGIN HIDDEN TESTS
case = dict(cases[0], authorized=True)
assert outcome(case, {"change_label"}, set()) == "needs_review"
assert outcome(case, {"read_label"}, {case["id"]}) == "denied"
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Tools you used
#
# Say which tools you used and how, or write “none.”
