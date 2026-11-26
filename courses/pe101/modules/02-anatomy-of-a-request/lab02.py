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
# # Lab 2: The anatomy of a request
#
# **Objectives:** LO-2.1, LO-2.2, LO-2.3, LO-2.4\
# **Prerequisites:** the [Module 2 reading](index.md) and [Lab 1](../01-how-models-produce-text/lab01.ipynb)\
# **Time:** about 2.5 hours
#
# In this lab you build Messages API requests as Python dictionaries, read responses, price them,
# and plan a workload's cost and its fit in the context window. Then you write a chat function
# that keeps a conversation's history, trim that history to a budget, and handle every way a
# response can stop.
#
# No cell sends anything over the network. Where a cell needs a model, a `ScriptedModel` from
# `promptlab` answers instead, from a script written in the cell. Its responses have the shape
# of real ones, but a person wrote their text, so they are illustrative, not model output.
#
# Each exercise ends with a check cell that prints `passed` or fails with a message. Run the
# cells in order, from the top. Some cells fail on purpose until you finish the exercise above
# them.

# %% [markdown]
# ## Setup

# %%
import json
import sys

import matplotlib
import matplotlib.pyplot as plt

import promptlab
from promptlab import ScriptedModel, make_response

prices = promptlab.load_json("prices.json")
print("Python", sys.version.split()[0], "| matplotlib", matplotlib.__version__,
      "| promptlab", promptlab.__version__)
print("prices taken", prices["taken"], "from", prices["source"])

# %% [markdown]
# ## 1. A request is data
#
# A request to the Messages API is a JSON object. In Python, it is a dictionary. This one asks for
# a one-sentence answer:

# %%
request = {
    "model": "claude-opus-5-5",
    "max_tokens": 300,
    "system": "You answer questions for the customers of a bicycle repair shop, in one sentence.",
    "messages": [
        {"role": "user", "content": "How often should I clean my chain?"},
    ],
}
print(json.dumps(request, indent=2))

# %% [markdown]
# `model` names the model, `max_tokens` caps the length of the answer, `system` holds the
# instructions that apply to the whole conversation, and `messages` holds the conversation's
# turns, oldest first, each with a `role` of `"user"` or `"assistant"`. The last turn is the
# user's, because the model writes the next one.
#
# ### Exercise L2.1 (LO-2.1, ★★, about 20 minutes)
#
# Write `make_request(model, system, turns, max_tokens)`. `turns` is a list of strings, the
# conversation so far, starting with the user and alternating. Return the request dictionary,
# with the turns as messages whose roles alternate `"user"`, `"assistant"`, `"user"`, and so on.
#
# Raise `ValueError` with a message that says what is wrong when `turns` is empty, or when it
# ends with an assistant turn. A request that ends with an assistant turn asks the model to
# continue that text, which is called prefilling, and current Claude models reject it.

# %% tags=["answer-L2.1"]
def make_request(model, system, turns, max_tokens):
    raise NotImplementedError("Exercise L2.1")


# %% tags=["raises-exception"]
r = make_request("claude-haiku-5-5", "Be brief.", ["Hi", "Hello! How can I help?", "Brakes"], 100)
assert r == {
    "model": "claude-haiku-5-5",
    "max_tokens": 100,
    "system": "Be brief.",
    "messages": [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello! How can I help?"},
        {"role": "user", "content": "Brakes"},
    ],
}, f"got {r}"
for bad in ([], ["Hi", "Hello!"]):
    try:
        make_request("claude-haiku-5-5", "Be brief.", bad, 100)
    except ValueError as error:
        print(f"{bad!r} -> ValueError: {error}")
    else:
        raise AssertionError(f"turns {bad!r} should raise ValueError")
print("passed")

# %% [markdown]
# ## 2. Reading a response
#
# A response is a JSON object too. The model's reply is in `content`, a list of blocks, each with
# a `type`. A plain answer has one block of type `"text"`; Modules 6 and 8 meet other types.
# `stop_reason` says why the model stopped, and `usage` counts the tokens the request used. Here
# is an illustrative response built by `make_response`, in the documented shape:

# %%
response = make_response(
    [{"type": "text", "text": "Clean it once a month, "},
     {"type": "text", "text": "or after any ride in the rain."}],
    input_tokens=41, output_tokens=18,
)
print(json.dumps(response, indent=2))

# %% [markdown]
# ### Exercise L2.2 (LO-2.1, ★, about 10 minutes)
#
# Write `response_text(response)`, which returns the text of every `"text"` block, joined in
# order with nothing between them. Skip blocks of any other type.

# %% tags=["answer-L2.2"]
def response_text(response):
    raise NotImplementedError("Exercise L2.2")


# %% tags=["raises-exception"]
assert response_text(response) == "Clean it once a month, or after any ride in the rain."
mixed = make_response([{"type": "text", "text": "A"},
                       {"type": "tool_use", "id": "toolu_1", "name": "lookup", "input": {}},
                       {"type": "text", "text": "B"}])
assert response_text(mixed) == "AB", "skip blocks that aren't text"
assert response_text(make_response([])) == "", "a response with no text blocks gives ''"
print("passed")

# %% [markdown]
# ## 3. What a request costs
#
# Prices are per million tokens, and differ for input, output, cache writes, and cache reads.
# The price table in `data/prices.json` was taken from Anthropic's pricing page on the date it
# names. Output tokens cost five times as much as input tokens on all three models:

# %%
for model, p in prices["models"].items():
    print(f"{model:18} input ${p['input']:6.3f}  output ${p['output']:6.3f}  "
          f"cache write ${p['cache_write_5m']:6.3f}  cache read ${p['cache_read']:6.3f}")

# %% [markdown]
# A request's cost $C$ adds up each kind of token times its price, divided by a million:
#
# $$C = \frac{n_\text{in} \, p_\text{in} + n_\text{out} \, p_\text{out}
#       + n_\text{write} \, p_\text{write} + n_\text{read} \, p_\text{read}}{1{,}000{,}000}$$
#
# where each $n$ is a count from `usage` and each $p$ a price from the table. Haiku 5.5 has one
# more rule: if a request's prompt, which counts its input, cache-write, and cache-read tokens
# together, is over 100,000 tokens, the whole request pays the `long_prompt` prices.
#
# ### Exercise L2.3 (LO-2.2, ★★, about 25 minutes)
#
# Write `request_cost(usage, model, prices)`, which returns a request's cost in dollars from its
# `usage` dictionary. Price cache writes at the 5-minute price. Apply Haiku's long-prompt prices
# when the model's entry has a `long_prompt` and the prompt is over its `above_tokens`.

# %% tags=["answer-L2.3"]
def request_cost(usage, model, prices):
    raise NotImplementedError("Exercise L2.3")


# %% tags=["raises-exception"]
def usage(i, o, write=0, read=0):
    return {"input_tokens": i, "output_tokens": o,
            "cache_creation_input_tokens": write, "cache_read_input_tokens": read}


assert abs(request_cost(usage(41, 18), "claude-opus-5-5", prices) - 0.000524) < 1e-12, (
    "41 input tokens at $4 and 18 output tokens at $20 per million cost $0.000524"
)
assert abs(request_cost(usage(1_000, 500, write=10_000, read=0), "claude-sonnet-5-5", prices)
           - (1_000 * 2 + 500 * 10 + 10_000 * 2.5) / 1e6) < 1e-12, "count cache writes too"
assert abs(request_cost(usage(1_000, 500, read=10_000), "claude-sonnet-5-5", prices)
           - (1_000 * 2 + 500 * 10 + 10_000 * 0.1) / 1e6) < 1e-12, "count cache reads too"
short = request_cost(usage(100_000, 1_000), "claude-haiku-5-5", prices)
long = request_cost(usage(100_001, 1_000), "claude-haiku-5-5", prices)
assert abs(short - 0.0105) < 1e-12, f"100,000 prompt tokens is not over the limit: expected $0.0105, got {short}"
assert abs(long - (100_001 * 0.5 + 1_000 * 2.5) / 1e6) < 1e-12, "100,001 prompt tokens use long_prompt prices"
mixed_long = request_cost(usage(60_000, 0, read=50_000), "claude-haiku-5-5", prices)
assert abs(mixed_long - (60_000 * 0.5 + 50_000 * 0.05) / 1e6) < 1e-12, "cache reads count toward the prompt"
print(f"passed: one more prompt token costs ${long - short:.4f} more on Haiku 5.5")

# %% [markdown]
# The last line shows the long-prompt rule's cliff: at 100,001 prompt tokens, every token of the
# request costs five times as much. The next cell plots the cost of one request with 1,000 output
# tokens against its prompt length, for Haiku 5.5 and Sonnet 5.5, on a logarithmic scale so both
# fit. Before you run it, predict whether the Haiku line ever crosses the Sonnet line.

# %% tags=["raises-exception"]
lengths = list(range(10_000, 200_001, 2_000))
fig, ax = plt.subplots(figsize=(7, 4))
for model, color, style in [("claude-haiku-5-5", "#E69F00", "-"), ("claude-sonnet-5-5", "#0072B2", "--")]:
    ax.plot([n / 1000 for n in lengths],
            [request_cost(usage(n, 1_000), model, prices) for n in lengths],
            color=color, linestyle=style, label=model)
ax.set_yscale("log")
ax.set_xlabel("prompt length (thousands of tokens)")
ax.set_ylabel("cost of one request (US dollars, log scale)")
ax.set_title("Haiku 5.5's price jumps at 100,000 prompt tokens")
ax.legend()
plt.show()

# %% [markdown]
# The Haiku line, solid and orange, jumps fivefold at 100,000 tokens but stays well below the
# dashed blue Sonnet line, which costs 20 times as much per input token at short prompts and
# 4 times as much at long ones.
#
# ### Exercise L2.4 (LO-2.2, ★★, about 15 minutes)
#
# Plan a workload before you run it. Write `workload_cost(requests, input_each, output_each, model,
# prices, batch=False)`: the cost of `requests` requests with the same usage, with no caching,
# taking the batch discount off both input and output when `batch` is true. Then use it to answer
# the question in the check cell.

# %% tags=["answer-L2.4"]
def workload_cost(requests, input_each, output_each, model, prices, batch=False):
    raise NotImplementedError("Exercise L2.4")


cheapest_model = None  # the model ID that answers the check cell's question

# %% tags=["raises-exception"]
assert abs(workload_cost(10_000, 1_500, 300, "claude-opus-5-5", prices) - 120.0) < 1e-9, (
    "10,000 requests of 1,500 input and 300 output tokens on Opus 5.5 cost $120"
)
assert abs(workload_cost(10_000, 1_500, 300, "claude-opus-5-5", prices, batch=True) - 60.0) < 1e-9
# The question: which of the three models classifies 50,000 tickets, each a 2,000-token prompt with
# a 50-token answer, for the least money in the Batch API? Set cheapest_model above.
costs = {m: workload_cost(50_000, 2_000, 50, m, prices, batch=True) for m in prices["models"]}
for m, c in costs.items():
    print(f"{m:18} ${c:8.2f}")
assert cheapest_model == min(costs, key=costs.get), "compare the three costs printed above"
print("passed")

# %% [markdown]
# The cheapest model isn't automatically the right one: it has to do the task well enough, which
# only an evaluation can tell you. Module 7 builds one, and Module 6 weighs cost against accuracy.
#
# ## 4. Will it fit?
#
# The context window must hold the prompt and the answer together. Each current model's window
# and its largest answer are in the price file, from Anthropic's models overview. Before you have
# a real token count, `promptlab.rough_token_count` estimates one from the overview's rule of
# thumb of 2.5 characters per token.
#
# ### Exercise L2.5 (LO-2.2, ★, about 10 minutes)
#
# Write `fits(prompt_tokens, max_tokens, model, prices)`, which is true when the prompt plus the
# whole answer fit in the model's context window, and `max_tokens` is within the model's output
# limit.

# %% tags=["answer-L2.5"]
def fits(prompt_tokens, max_tokens, model, prices):
    raise NotImplementedError("Exercise L2.5")


# %% tags=["raises-exception"]
assert fits(900_000, 100_000, "claude-opus-5-5", prices), "exactly 1M tokens fits"
assert not fits(900_001, 100_000, "claude-opus-5-5", prices), "one token over doesn't"
assert not fits(1_000, 200_000, "claude-opus-5-5", prices), "max_tokens is over the 128K output limit"
manual = "x" * 2_000_000  # stands in for a 2-million-character manual
estimate = promptlab.rough_token_count(manual)
print(f"estimated {estimate:,} tokens; fits with a 4,000-token answer: "
      f"{fits(estimate, 4_000, 'claude-sonnet-5-5', prices)}")
print("passed")

# %% [markdown]
# ## 5. Conversations
#
# The model keeps nothing between requests. To hold a conversation, a program keeps the history
# itself and sends all of it with each new message. The next exercise builds that loop, and a
# `ScriptedModel` plays the model: it answers from its script and records each request, so you
# can see what your code sent.
#
# ### Exercise L2.6 (LO-2.3, ★★, about 20 minutes)
#
# Write `chat(model, history, user_text, system, max_tokens=300)`. `model` is a function that
# takes a request and returns a response, and `history` is a list of message dictionaries, which
# `chat` changes in place. Append the user's message, send a request for the model
# `"claude-haiku-5-5"` with the whole history, then append the reply as an assistant message and
# return its text. Use `response_text`.

# %% tags=["answer-L2.6"]
def chat(model, history, user_text, system, max_tokens=300):
    raise NotImplementedError("Exercise L2.6")


# %% tags=["raises-exception"]
shop = "You answer questions for the customers of a bicycle repair shop."
stand_in = ScriptedModel(["Hello! What does your bike need?",
                          "A tube change takes about 20 minutes.",
                          "You said a flat tire."])
history = []
chat(stand_in, history, "Hi, I have a flat tire.", shop)
chat(stand_in, history, "How long does it take?", shop)
reply = chat(stand_in, history, "What did I say was wrong?", shop)
assert reply == "You said a flat tire."
assert len(history) == 6, f"three exchanges make six messages, not {len(history)}"
assert [len(r["messages"]) for r in stand_in.requests] == [1, 3, 5], "send the whole history each time"
assert all(r["system"] == shop for r in stand_in.requests), "send the system prompt with every request"
print("passed")
for n, sent in enumerate(stand_in.requests, start=1):
    count = len(sent["messages"])
    print(f"request {n} sent {count} message{'s' if count > 1 else ''}, "
          f"ending with {sent['messages'][-1]['content']!r}")

# %% [markdown]
# The third reply could mention the flat tire only because the third request contained the first
# message. The scripted model didn't read it, of course, but a real one could only answer from
# what that request held.
#
# Resending the history has a price: every request pays again for every earlier turn. The next
# cell estimates the input tokens of a 30-turn conversation, with a 200-token system prompt,
# 60-token user messages, and 150-token replies, and plots them.

# %%
system_tokens, user_tokens, reply_tokens = 200, 60, 150
per_request = [system_tokens + (turn - 1) * (user_tokens + reply_tokens) + user_tokens
               for turn in range(1, 31)]
total = sum(per_request)
print(f"request 1 sends {per_request[0]} input tokens; request 30 sends {per_request[-1]:,}")
print(f"all 30 requests send {total:,} input tokens, for {30 * (user_tokens + reply_tokens):,} "
      "tokens of conversation")
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.bar(range(1, 31), per_request, color="#0072B2")
ax.set_xlabel("turn of the conversation")
ax.set_ylabel("input tokens sent in that request")
ax.set_title("Each request resends the whole history")
plt.show()

# %% [markdown]
# The bars grow by 210 tokens a turn, so the total grows with the square of the number of turns:
# 30 turns send about 99,000 input tokens to carry 6,300 tokens of conversation. Prompt caching,
# in Module 10, makes the repeated part cheaper; trimming the history makes it shorter.
#
# ### Exercise L2.7 (LO-2.3, ★★★, about 30 minutes)
#
# Write `trim_history(messages, budget, count_tokens)`, which returns a new list: the most recent
# messages whose tokens, counted with `count_tokens(text)`, add up to no more than `budget`. Drop
# whole exchanges, a user message and the reply after it, from the oldest end, so the list still
# starts with a user message. Always keep the last message, the user's newest. Raise `ValueError`
# if that message alone is over the budget. Don't change the list passed in.

# %% tags=["answer-L2.7"]
def trim_history(messages, budget, count_tokens):
    raise NotImplementedError("Exercise L2.7")


# %% tags=["raises-exception"]
def words(text):
    return len(text.split())


talk = [{"role": "user", "content": "My bike is blue"},           # 4 words
        {"role": "assistant", "content": "Noted"},                # 1
        {"role": "user", "content": "The chain skips a lot"},     # 5
        {"role": "assistant", "content": "Bring it in today"},    # 4
        {"role": "user", "content": "What color is it"}]          # 4
assert trim_history(talk, 100, words) == talk, "under budget, keep everything"
kept = trim_history(talk, 13, words)
assert kept == talk[2:], f"drop the oldest exchange to get from 18 words to 13; kept {kept}"
assert trim_history(talk, 12, words) == talk[4:], "over 4 + 5 + 4 = 13, keep only the newest"
assert len(talk) == 5, "don't change the list passed in"
try:
    trim_history(talk, 3, words)
except ValueError:
    pass
else:
    raise AssertionError("the newest message alone is 4 words, over a budget of 3")
print("passed")
print("the trimmed request no longer says the bike is blue:", kept[0]["content"])

# %% [markdown]
# Dropping the oldest exchange is the simplest policy, and it loses facts like the bike's color.
# The reading describes two others: summarize the dropped turns into one short message, or move
# facts that must last, such as the customer's name, into the system prompt.
#
# ## 6. Why the model stopped
#
# Every response says why it stopped. Code that reads `content` without checking `stop_reason`
# will one day show a user half an answer, or an empty one. The API documentation lists seven
# stop reasons:

# %%
from promptlab.standins import STOP_REASONS

print(STOP_REASONS)

# %% [markdown]
# - `"end_turn"`: the model finished its answer.
# - `"stop_sequence"`: the model wrote one of the request's `stop_sequences`.
# - `"max_tokens"`: the answer reached the request's `max_tokens` and was cut off.
# - `"model_context_window_exceeded"`: the answer filled the context window and was cut off.
# - `"refusal"`: the model declined to respond.
# - `"tool_use"`: the model is asking to call a tool, which Module 8 handles.
# - `"pause_turn"`: a loop of server-side tools reached its limit, which this course doesn't use.
#
# ### Exercise L2.8 (LO-2.4, ★★, about 25 minutes)
#
# 1. Write `final_text(response)`. Return the text for `"end_turn"` and `"stop_sequence"`. Raise
#    `Truncated` for the two cut-off reasons and `Refused` for a refusal. For any other reason,
#    raise `ValueError` naming it.
# 2. Write `ask(model, request, ceiling)`, which sends the request and returns `final_text` of
#    the response. If the answer was cut off by `max_tokens`, send a copy of the request with
#    `max_tokens` doubled, up to `ceiling`, and try again. If it is still cut off at the ceiling,
#    let `Truncated` propagate. Never change the request passed in.

# %% tags=["answer-L2.8"]
class Truncated(Exception):
    """The answer was cut off before the model finished it."""


class Refused(Exception):
    """The model declined to respond."""


def final_text(response):
    raise NotImplementedError("Exercise L2.8")


def ask(model, request, ceiling):
    raise NotImplementedError("Exercise L2.8")


# %% tags=["raises-exception"]
assert final_text(make_response("Done.")) == "Done."
assert final_text(make_response("Done", stop_reason="stop_sequence", stop_sequence="END")) == "Done"
for reason, error in [("max_tokens", Truncated), ("model_context_window_exceeded", Truncated),
                      ("refusal", Refused), ("tool_use", ValueError), ("pause_turn", ValueError)]:
    try:
        final_text(make_response("partial", stop_reason=reason))
    except error:
        pass
    else:
        raise AssertionError(f"stop reason {reason!r} should raise {error.__name__}")

base = make_request("claude-haiku-5-5", "Be thorough.", ["List every step of a chain clean."], 100)
cut = make_response("1. Put the bike in the stand. 2. Hold a rag", stop_reason="max_tokens")
stand_in = ScriptedModel([cut, cut, "1. Put the bike in the stand. 2. ... 7. Wipe off the oil."])
answer = ask(stand_in, base, ceiling=800)
assert answer.endswith("Wipe off the oil."), "return the complete answer"
assert [r["max_tokens"] for r in stand_in.requests] == [100, 200, 400], (
    f"double max_tokens on each retry; sent {[r['max_tokens'] for r in stand_in.requests]}"
)
assert base["max_tokens"] == 100, "don't change the request passed in"
try:
    ask(ScriptedModel([cut, cut]), base, ceiling=200)
except Truncated:
    pass
else:
    raise AssertionError("still cut off at the ceiling: let Truncated propagate")
print("passed")

# %% [markdown]
# Doubling `max_tokens` is right only when the answer was legitimately long. If a prompt makes
# answers longer than they should be, more room just costs more: fix the prompt instead, as
# Module 3 does. A refusal is a different case: it isn't a length problem, so more room won't
# change it.
#
# ## Summary
#
# - A request is a dictionary: a model, `max_tokens`, a system prompt, and alternating messages
#   that end with the user's. A response holds content blocks, a stop reason, and token usage.
# - Cost is each kind of token times its price. Output costs five times as much as input on the
#   current models, the Batch API halves both, and Haiku 5.5 charges more for prompts over 100,000
#   tokens.
# - The context window holds the prompt and the answer together, and `max_tokens` has its own
#   limit.
# - A conversation lives in the program, which resends the whole history every time. Its cost grows
#   with the square of its length, and trimming it loses what it drops.
# - Check `stop_reason` before you use the text: a cut-off answer and a refusal are normal
#   responses, not errors the API reports.
#
# Next, do the [Module 2 practice](practice.md), then [PA1](../../assignments/pa1/pa1.ipynb).
