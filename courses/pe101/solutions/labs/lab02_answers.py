# %% [markdown]
# # Lab 2: answer key
#
# Each tagged cell replaces the lab cell with the same tag. `tools/check_lab.py` runs the lab with
# these answers and fails if any check fails. The untagged Markdown cells explain each answer and
# the mistakes students commonly make; the checker ignores them.

# %% [markdown]
# ## Exercise L2.1
#
# The role of each turn follows from its position: even indexes are the user's. Students often
# forget the prefill case, or build the roles from a separate list that can fall out of step.

# %% tags=["answer-L2.1"]
def make_request(model, system, turns, max_tokens):
    if not turns:
        raise ValueError("a request needs at least one user turn")
    if len(turns) % 2 == 0:
        raise ValueError("the turns end with an assistant turn, which would prefill the answer; "
                         "current Claude models reject prefills")
    messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": text}
                for i, text in enumerate(turns)]
    return {"model": model, "max_tokens": max_tokens, "system": system, "messages": messages}


# %% [markdown]
# ## Exercise L2.2
#
# Reading `response["content"][0]["text"]` works for the first example and fails on the second
# and third: the first block may not be text, and there may be none.

# %% tags=["answer-L2.2"]
def response_text(response):
    return "".join(block["text"] for block in response["content"] if block["type"] == "text")


# %% [markdown]
# ## Exercise L2.3
#
# The prompt length that selects Haiku's prices counts input, cache-write, and cache-read tokens,
# as the pricing page says; output tokens don't count toward it. "Over 100,000" means strictly
# greater. Common mistakes: forgetting to divide by a million, and pricing only the extra tokens
# above 100,000 at the higher rate instead of the whole request.

# %% tags=["answer-L2.3"]
def request_cost(usage, model, prices):
    p = prices["models"][model]
    write = usage.get("cache_creation_input_tokens", 0)
    read = usage.get("cache_read_input_tokens", 0)
    prompt = usage["input_tokens"] + write + read
    if "long_prompt" in p and prompt > p["long_prompt"]["above_tokens"]:
        p = p["long_prompt"]
    return (usage["input_tokens"] * p["input"] + usage["output_tokens"] * p["output"]
            + write * p["cache_write_5m"] + read * p["cache_read"]) / 1_000_000


# %% [markdown]
# ## Exercise L2.4
#
# Reusing `request_cost` keeps Haiku's long-prompt rule in one place. Haiku 5.5 costs $5.62 for the
# 50,000 tickets in the Batch API, against $112.50 on Sonnet 5.5 and $225.00 on Opus 5.5.

# %% tags=["answer-L2.4"]
def workload_cost(requests, input_each, output_each, model, prices, batch=False):
    one = request_cost({"input_tokens": input_each, "output_tokens": output_each}, model, prices)
    return requests * one * (1 - prices["batch_discount"] if batch else 1)


cheapest_model = "claude-haiku-5-5"

# %% [markdown]
# ## Exercise L2.5
#
# Both limits matter: a request can fit the window and still ask for more output than the model
# can write in one response.

# %% tags=["answer-L2.5"]
def fits(prompt_tokens, max_tokens, model, prices):
    return (prompt_tokens + max_tokens <= prices["context_window"][model]
            and max_tokens <= prices["max_output_tokens"][model])


# %% [markdown]
# ## Exercise L2.6
#
# Append the user's message before sending, and the reply after. Students who build a new list for
# each request, instead of appending to `history`, lose the conversation between calls.

# %% tags=["answer-L2.6"]
def chat(model, history, user_text, system, max_tokens=300):
    history.append({"role": "user", "content": user_text})
    request = {"model": "claude-haiku-5-5", "max_tokens": max_tokens, "system": system,
               "messages": list(history)}
    reply = response_text(model(request))
    history.append({"role": "assistant", "content": reply})
    return reply


# %% [markdown]
# ## Exercise L2.7
#
# Drop two messages at a time from the front, so the list keeps starting with a user message.
# The loop stops when the remainder fits or only the newest message is left.

# %% tags=["answer-L2.7"]
def trim_history(messages, budget, count_tokens):
    if count_tokens(messages[-1]["content"]) > budget:
        raise ValueError("the newest message alone is over the budget")
    kept = list(messages)
    while sum(count_tokens(m["content"]) for m in kept) > budget and len(kept) > 1:
        kept = kept[2:]
    return kept


# %% [markdown]
# ## Exercise L2.8
#
# Only a `max_tokens` cut-off is worth retrying with more room: a response that filled the context
# window won't fit better, and a refusal isn't a length problem. `dict(request)` copies only the
# top level, which is enough here, since only `max_tokens` changes.

# %% tags=["answer-L2.8"]
class Truncated(Exception):
    """The answer was cut off before the model finished it."""


class Refused(Exception):
    """The model declined to respond."""


def final_text(response):
    reason = response["stop_reason"]
    if reason in ("end_turn", "stop_sequence"):
        return response_text(response)
    if reason in ("max_tokens", "model_context_window_exceeded"):
        raise Truncated(f"the answer was cut off ({reason})")
    if reason == "refusal":
        raise Refused("the model declined to respond")
    raise ValueError(f"stop reason {reason!r} needs handling that final_text doesn't do")


def ask(model, request, ceiling):
    request = dict(request)
    while True:
        response = model(request)
        if response["stop_reason"] != "max_tokens" or request["max_tokens"] >= ceiling:
            return final_text(response)
        request["max_tokens"] = min(2 * request["max_tokens"], ceiling)
