# ---
# jupyter:
#   jupytext:
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
# # PA1: Requests and costs
#
# **Objectives:** LO-2.1, LO-2.2, LO-2.3, LO-2.4, and LO-1.3 again\
# **When:** after Module 2, as the [suggested pace](../../README.md#suggested-pace) places it\
# **Points:** 23, for scoring yourself; the course has no grades\
# **Time:** about 3 hours
#
# You are building the plumbing of an assistant for a bicycle repair shop: the code that builds
# its requests, prices its responses, keeps its conversations within budget, and handles every way
# a response can stop. No cell calls a model. Where a test needs one, a `ScriptedModel` from
# `promptlab` answers from a script, with illustrative responses written for this course.
#
# Write each answer in the cell marked `# YOUR CODE HERE`, replacing the line
# `raise NotImplementedError()`. Each problem's test cell checks your answer with visible tests,
# which you can run as often as you like. An instructor or a mentor who reviews your work can also
# run hidden tests, which check the cases the problem statement describes but the visible tests
# don't, so read each statement closely and test those cases yourself.
#
# - Don't change or delete the test cells.
# - Define each function as a global, as each problem's starter code does, so the test cells can
#   call it.
# - Before you submit, restart the kernel and run every cell from the top (**Kernel** > **Restart
#   Kernel and Run All Cells**), and check that every test cell prints `passed`.
# - The course policies apply. In particular, generative AI tools may not write any part of this
#   assignment; say in the last cell which tools you used, and how, or write "none".

# %%
import sys

import promptlab
from promptlab import ScriptedModel, make_response

prices = promptlab.load_json("prices.json")
print("Python", sys.version.split()[0], "| promptlab", promptlab.__version__,
      "| prices taken", prices["taken"])

# %% [markdown]
# ## Problem 1: Build the request (LO-2.1, 3 points)
#
# Write `build_request(model, system, history, user_text, max_tokens, stop_sequences=None)`.
# `history` is the conversation so far, as a list of message dictionaries, and `user_text` is the
# user's new message. Return a request whose `messages` are a copy of the history followed by the
# new user message. Include the key `"stop_sequences"` only when `stop_sequences` is a non-empty
# list.
#
# Raise `ValueError` if the history doesn't alternate roles starting with `"user"`, or if it ends
# with a user message: with the new message added, either would put two user turns in a row. An
# empty history is fine. Don't change the history passed in.

# %% nbgrader={"grade": false, "grade_id": "build-request", "locked": false, "schema_version": 3, "solution": true, "task": false}
def build_request(model, system, history, user_text, max_tokens, stop_sequences=None):
    ### BEGIN SOLUTION
    for i, message in enumerate(history):
        expected = "user" if i % 2 == 0 else "assistant"
        if message["role"] != expected:
            raise ValueError(f"message {i} should be a {expected} turn, not {message['role']}")
    if history and history[-1]["role"] == "user":
        raise ValueError("the history ends with a user turn, so the new message would follow it")
    request = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [dict(m) for m in history] + [{"role": "user", "content": user_text}],
    }
    if stop_sequences:
        request["stop_sequences"] = list(stop_sequences)
    return request
    ### END SOLUTION


# %% nbgrader={"grade": true, "grade_id": "build-request-tests", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": false}
history = [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]
r = build_request("claude-haiku-5-5", "Be brief.", history, "Brakes?", 200)
assert r["messages"] == history + [{"role": "user", "content": "Brakes?"}], "append the new message"
assert r["model"] == "claude-haiku-5-5" and r["max_tokens"] == 200 and r["system"] == "Be brief."
assert "stop_sequences" not in r, "leave stop_sequences out when none are given"
assert len(history) == 2, "don't change the history passed in"
r = build_request("claude-haiku-5-5", "Be brief.", [], "Hi", 50, stop_sequences=["END"])
assert r["stop_sequences"] == ["END"]
try:
    build_request("claude-haiku-5-5", "Be brief.", [{"role": "user", "content": "Hi"}], "Hi?", 50)
except ValueError:
    pass
else:
    raise AssertionError("a history that ends with a user turn should raise ValueError")
### BEGIN HIDDEN TESTS
assert "stop_sequences" not in build_request("claude-haiku-5-5", "s", [], "Hi", 50, stop_sequences=[]), (
    "an empty list of stop sequences means none"
)
for bad in ([{"role": "assistant", "content": "Hello"}],
            [{"role": "user", "content": "a"}, {"role": "user", "content": "b"},
             {"role": "assistant", "content": "c"}]):
    try:
        build_request("claude-haiku-5-5", "s", bad, "Hi", 50)
    except ValueError:
        pass
    else:
        raise AssertionError(f"history {bad} doesn't alternate from a user turn")
r = build_request("claude-haiku-5-5", "s", history, "x", 50)
r["messages"][0]["content"] = "changed"
assert history[0]["content"] == "Hi", "copy the history's messages, so changing the request can't change it"
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 2: A cost report (LO-2.2, 4 points)
#
# Write `cost_report(responses, prices)`, which prices a list of responses, each by the model its
# `"model"` field names, and returns a dictionary from each model ID that appears to the total
# cost of its responses, in dollars, plus the key `"total"` for the cost of all of them. Price
# cache writes at the 5-minute price, and apply Haiku 5.5's long-prompt prices as the reading
# describes. A `usage` dictionary may leave out the two cache fields, which then count as 0.

# %% nbgrader={"grade": false, "grade_id": "cost-report", "locked": false, "schema_version": 3, "solution": true, "task": false}
def cost_report(responses, prices):
    ### BEGIN SOLUTION
    report = {}
    for response in responses:
        model, usage = response["model"], response["usage"]
        p = prices["models"][model]
        write = usage.get("cache_creation_input_tokens", 0)
        read = usage.get("cache_read_input_tokens", 0)
        if "long_prompt" in p and usage["input_tokens"] + write + read > p["long_prompt"]["above_tokens"]:
            p = p["long_prompt"]
        cost = (usage["input_tokens"] * p["input"] + usage["output_tokens"] * p["output"]
                + write * p["cache_write_5m"] + read * p["cache_read"]) / 1_000_000
        report[model] = report.get(model, 0.0) + cost
    report["total"] = sum(report.values())
    return report
    ### END SOLUTION


# %% nbgrader={"grade": true, "grade_id": "cost-report-tests", "locked": true, "points": 4, "schema_version": 3, "solution": false, "task": false}
def close(a, b):
    return abs(a - b) < 1e-12


responses = [
    make_response("a", model="claude-opus-5-5", input_tokens=1_000, output_tokens=100),
    make_response("b", model="claude-opus-5-5", input_tokens=500, output_tokens=50,
                  cache_read_input_tokens=10_000),
    make_response("c", model="claude-haiku-5-5", input_tokens=2_000, output_tokens=20),
]
report = cost_report(responses, prices)
assert set(report) == {"claude-opus-5-5", "claude-haiku-5-5", "total"}, f"keys: {set(report)}"
assert close(report["claude-opus-5-5"], (1_000 * 4 + 100 * 20 + 500 * 4 + 50 * 20 + 10_000 * 0.2) / 1e6)
assert close(report["claude-haiku-5-5"], (2_000 * 0.1 + 20 * 0.5) / 1e6)
assert close(report["total"], report["claude-opus-5-5"] + report["claude-haiku-5-5"])
assert cost_report([], prices) == {"total": 0}, "no responses cost nothing"
### BEGIN HIDDEN TESTS
long = make_response("d", model="claude-haiku-5-5", input_tokens=90_000, output_tokens=1_000,
                     cache_creation_input_tokens=20_000)
assert close(cost_report([long], prices)["total"], (90_000 * 0.5 + 1_000 * 2.5 + 20_000 * 0.625) / 1e6), (
    "cache writes count toward Haiku's long-prompt limit"
)
edge = make_response("e", model="claude-haiku-5-5", input_tokens=100_000, output_tokens=0)
assert close(cost_report([edge], prices)["total"], 100_000 * 0.1 / 1e6), "exactly 100,000 isn't over the limit"
bare = {"model": "claude-sonnet-5-5", "usage": {"input_tokens": 1_000, "output_tokens": 1_000}}
assert close(cost_report([bare], prices)["total"], (1_000 * 2 + 1_000 * 10) / 1e6), "missing cache fields count as 0"
writes = make_response("f", model="claude-sonnet-5-5", input_tokens=0, output_tokens=0,
                       cache_creation_input_tokens=4_000)
assert close(cost_report([writes], prices)["total"], 4_000 * 2.5 / 1e6), "price cache writes at the 5-minute price"
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 3: How many can we afford? (LO-2.2, 3 points)
#
# Write `affordable_requests(budget, input_each, output_each, model, prices, batch=False)`, which
# returns the largest whole number of identical requests, with no caching, whose total cost is at
# most `budget` dollars. Take the batch discount off both input and output when `batch` is true.
# Apply Haiku's long-prompt prices when each request's prompt is over the limit.

# %% nbgrader={"grade": false, "grade_id": "affordable", "locked": false, "schema_version": 3, "solution": true, "task": false}
def affordable_requests(budget, input_each, output_each, model, prices, batch=False):
    ### BEGIN SOLUTION
    p = prices["models"][model]
    if "long_prompt" in p and input_each > p["long_prompt"]["above_tokens"]:
        p = p["long_prompt"]
    one = (input_each * p["input"] + output_each * p["output"]) / 1_000_000
    if batch:
        one *= 1 - prices["batch_discount"]
    # Round the quotient before flooring it, so a budget that is an exact multiple of the cost
    # isn't lost to floating-point error (0.3 / 0.1 is 2.9999999999999996).
    return int(round(budget / one, 9) // 1)
    ### END SOLUTION


# %% nbgrader={"grade": true, "grade_id": "affordable-tests", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": false}
assert affordable_requests(120, 1_500, 300, "claude-opus-5-5", prices) == 10_000, (
    "one request costs $0.012, so $120 buys 10,000"
)
assert affordable_requests(120, 1_500, 300, "claude-opus-5-5", prices, batch=True) == 20_000
assert affordable_requests(1, 1_500, 300, "claude-opus-5-5", prices) == 83, "round down: 1 / 0.012 is 83.3"
### BEGIN HIDDEN TESTS
assert affordable_requests(0.3, 500, 0, "claude-sonnet-5-5", prices) == 300, (
    "an exact multiple of the cost must not lose a request to floating-point error"
)
assert affordable_requests(10, 150_000, 1_000, "claude-haiku-5-5", prices) == 129, (
    "a 150,000-token prompt pays Haiku's long-prompt prices: $0.0775 a request"
)
assert affordable_requests(0.001, 1_500, 300, "claude-opus-5-5", prices) == 0
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 4: Keep the history within budget (LO-2.3, 5 points)
#
# Customers often give their order number in their first message, and every later answer needs
# it. Write `budget_history(history, budget, count_tokens, keep_first=False)`, which returns a new
# list of messages whose tokens, counted with `count_tokens(text)`, add up to at most `budget`.
#
# - `history` alternates roles starting with `"user"` and ends with the user's newest message,
#   which you must always keep.
# - Drop whole exchanges, a user message and the reply after it, oldest first, until the rest
#   fits.
# - When `keep_first` is true, never drop the first exchange either: drop the oldest of the others
#   instead. If the first exchange and the newest message together are over the budget, keep the
#   newest message only.
# - Raise `ValueError` if the newest message alone is over the budget.
# - Don't change the list passed in.

# %% nbgrader={"grade": false, "grade_id": "budget-history", "locked": false, "schema_version": 3, "solution": true, "task": false}
def budget_history(history, budget, count_tokens, keep_first=False):
    ### BEGIN SOLUTION
    def total(messages):
        return sum(count_tokens(m["content"]) for m in messages)

    newest = history[-1]
    if count_tokens(newest["content"]) > budget:
        raise ValueError("the newest message alone is over the budget")
    if keep_first and len(history) >= 3:
        first, middle = history[:2], history[2:-1]
        while middle and total(first + middle + [newest]) > budget:
            middle = middle[2:]
        kept = first + middle + [newest]
        return kept if total(kept) <= budget else [newest]
    kept = list(history)
    while total(kept) > budget:
        kept = kept[2:]
    return kept
    ### END SOLUTION


# %% nbgrader={"grade": true, "grade_id": "budget-history-tests", "locked": true, "points": 5, "schema_version": 3, "solution": false, "task": false}
def words(text):
    return len(text.split())


def turns(*texts):
    return [{"role": "user" if i % 2 == 0 else "assistant", "content": t} for i, t in enumerate(texts)]


chat = turns("order 4417 is late",             # 4 words
             "sorry, checking now",            # 3
             "it was a wheel",                 # 4
             "the wheel ships today",          # 4
             "and the tube",                   # 3
             "the tube shipped yesterday",     # 4
             "when will it arrive")            # 4
assert budget_history(chat, 26, words) == chat, "26 words fit"
assert budget_history(chat, 19, words) == chat[2:], "drop the oldest exchange first"
kept = budget_history(chat, 18, words, keep_first=True)
assert kept == chat[:2] + chat[4:], f"keep the first exchange, drop the second: got {kept}"
assert len(chat) == 7, "don't change the list passed in"
try:
    budget_history(chat, 3, words)
except ValueError:
    pass
else:
    raise AssertionError("the newest message alone is over a budget of 3")
### BEGIN HIDDEN TESTS
assert budget_history(chat, 4, words) == chat[-1:], "only the newest message fits"
assert budget_history(chat, 11, words, keep_first=True) == chat[:2] + chat[-1:], (
    "keep the first exchange and the newest message when nothing else fits"
)
assert budget_history(chat, 10, words, keep_first=True) == chat[-1:], (
    "if the first exchange and the newest message don't fit together, keep the newest only"
)
assert budget_history(chat[-1:], 10, words, keep_first=True) == chat[-1:], "one message, nothing to drop"
assert budget_history(chat[:3], 100, words, keep_first=True) == chat[:3]
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 5: A reply, whatever happens (LO-2.4, 5 points)
#
# Write `reply(model, request, ceiling, fallback)`, which sends the request and returns a
# dictionary with three keys: `"text"`, the text to show the user; `"status"`, one of `"ok"`,
# `"refused"`, or `"truncated"`; and `"attempts"`, the number of requests sent.
#
# - For `"end_turn"` or `"stop_sequence"`, return the response's text with status `"ok"`.
# - For `"max_tokens"`, resend a copy of the request with `max_tokens` doubled, but never above
#   `ceiling`. If an answer is still cut off when `max_tokens` is already at the ceiling, return
#   `fallback` with status `"truncated"`.
# - For `"model_context_window_exceeded"`, return `fallback` with status `"truncated"` at once:
#   more room can't help.
# - For `"refusal"`, return `fallback` with status `"refused"`.
# - For any other stop reason, raise `ValueError`.
# - The text of a response is the text of all its text blocks, joined in order. Never change the
#   request passed in.

# %% nbgrader={"grade": false, "grade_id": "reply", "locked": false, "schema_version": 3, "solution": true, "task": false}
def reply(model, request, ceiling, fallback):
    ### BEGIN SOLUTION
    request = dict(request)
    attempts = 0
    while True:
        response = model(request)
        attempts += 1
        reason = response["stop_reason"]
        if reason in ("end_turn", "stop_sequence"):
            text = "".join(b["text"] for b in response["content"] if b["type"] == "text")
            return {"text": text, "status": "ok", "attempts": attempts}
        if reason == "refusal":
            return {"text": fallback, "status": "refused", "attempts": attempts}
        if reason == "model_context_window_exceeded" or (
                reason == "max_tokens" and request["max_tokens"] >= ceiling):
            return {"text": fallback, "status": "truncated", "attempts": attempts}
        if reason != "max_tokens":
            raise ValueError(f"stop reason {reason!r} isn't handled here")
        request["max_tokens"] = min(2 * request["max_tokens"], ceiling)
    ### END SOLUTION


# %% nbgrader={"grade": true, "grade_id": "reply-tests", "locked": true, "points": 5, "schema_version": 3, "solution": false, "task": false}
SORRY = "Sorry, I can't answer that here. Please call the shop."
base = {"model": "claude-haiku-5-5", "max_tokens": 100, "system": "Be helpful.",
        "messages": [{"role": "user", "content": "List the steps of a tune-up."}]}
cut = make_response("1. Check the tires. 2.", stop_reason="max_tokens")
model = ScriptedModel([cut, "1. Check the tires. 2. Adjust the brakes."])
assert reply(model, base, 400, SORRY) == {
    "text": "1. Check the tires. 2. Adjust the brakes.", "status": "ok", "attempts": 2}
assert [r["max_tokens"] for r in model.requests] == [100, 200], "double max_tokens on the retry"
assert base["max_tokens"] == 100, "don't change the request passed in"
refused = make_response("", stop_reason="refusal", stop_details={"type": "refusal"})
assert reply(ScriptedModel([refused]), base, 400, SORRY) == {
    "text": SORRY, "status": "refused", "attempts": 1}
### BEGIN HIDDEN TESTS
model = ScriptedModel([cut, cut, cut])
assert reply(model, base, 300, SORRY) == {"text": SORRY, "status": "truncated", "attempts": 3}
assert [r["max_tokens"] for r in model.requests] == [100, 200, 300], "never go above the ceiling"
full = make_response("partial", stop_reason="model_context_window_exceeded")
assert reply(ScriptedModel([full]), base, 400, SORRY) == {"text": SORRY, "status": "truncated", "attempts": 1}
stop = make_response("Done", stop_reason="stop_sequence", stop_sequence="END")
assert reply(ScriptedModel([stop]), base, 400, SORRY)["text"] == "Done"
tool = make_response([{"type": "tool_use", "id": "toolu_1", "name": "lookup", "input": {}}],
                     stop_reason="tool_use")
try:
    reply(ScriptedModel([tool]), base, 400, SORRY)
except ValueError:
    pass
else:
    raise AssertionError("tool_use isn't handled here, so raise ValueError")
blocks = make_response([{"type": "text", "text": "A"}, {"type": "text", "text": "B"}])
assert reply(ScriptedModel([blocks]), base, 400, SORRY)["text"] == "AB", "join every text block"
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# ## Problem 6: What a conversation costs (LO-2.3, LO-1.3, 3 points)
#
# Write `conversation_input_tokens(system, user, reply, turns, keep_last=None)`, which returns the
# total input tokens that a conversation of `turns` requests sends. Every request sends the system
# prompt (`system` tokens) and the new user message (`user` tokens), plus the earlier exchanges it
# keeps, each `user + reply` tokens. With `keep_last=None`, each request keeps every earlier
# exchange; with a number, it keeps at most that many of the most recent ones.

# %% nbgrader={"grade": false, "grade_id": "conversation-tokens", "locked": false, "schema_version": 3, "solution": true, "task": false}
def conversation_input_tokens(system, user, reply, turns, keep_last=None):
    ### BEGIN SOLUTION
    total = 0
    for turn in range(1, turns + 1):
        earlier = turn - 1 if keep_last is None else min(turn - 1, keep_last)
        total += system + earlier * (user + reply) + user
    return total
    ### END SOLUTION


# %% nbgrader={"grade": true, "grade_id": "conversation-tokens-tests", "locked": true, "points": 2, "schema_version": 3, "solution": false, "task": false}
assert conversation_input_tokens(100, 10, 20, 1) == 110, "the first request sends the system prompt and one message"
assert conversation_input_tokens(100, 10, 20, 3) == 110 + 140 + 170
assert conversation_input_tokens(100, 10, 20, 3, keep_last=1) == 110 + 140 + 140
### BEGIN HIDDEN TESTS
assert conversation_input_tokens(200, 60, 150, 30) == 99_150, "the reading's worked example"
assert conversation_input_tokens(500, 100, 300, 20, keep_last=4) == 40_000
assert conversation_input_tokens(500, 100, 300, 0) == 0, "no turns send nothing"
assert conversation_input_tokens(100, 10, 20, 3, keep_last=0) == 330
### END HIDDEN TESTS
print("passed")

# %% [markdown]
# In two or three sentences: with `keep_last=4`, what can the model no longer do from turn 6 on
# that it could do with the whole history, and why? (1 point, scored by you against the reading's
# section on conversations.)

# %% [markdown] nbgrader={"grade": true, "grade_id": "conversation-why", "locked": false, "points": 1, "schema_version": 3, "solution": true, "task": false}
# From turn 6 on, each request leaves out the first exchanges, so the model can't use anything
# said only there, such as the customer's name or the problem they started with. The model keeps
# nothing between requests: it can use only what each request contains, and the trimmed requests
# no longer contain those turns.

# %% [markdown]
# ## Tools you used
#
# Say which tools you used for this assignment, generative AI tools included, and how, or write
# "none".
#
# *Your answer here.*
