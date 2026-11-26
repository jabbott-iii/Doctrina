# Module 2 practice

These exercises practice retrieving what the [Module 2 reading](index.md) explained. They aren't
graded. Work each one on paper first, then check your answer. The prices are the ones in the
reading's table, in US dollars per million tokens, taken on November 26, 2026. The answers are in
the collapsed blocks; open one only after you have an answer of your own.

## Worked example: a request with a cache read

A request to Opus 5.5 reports 2,000 input tokens, 10,000 cache-read tokens, and 400 output tokens.
What did it cost?

1. List each count with its price: 2,000 input tokens at 4, 10,000 cache reads at 0.20, and 400
   output tokens at 20.
2. Multiply and add: 2,000 × 4 + 10,000 × 0.20 + 400 × 20 = 8,000 + 2,000 + 8,000 = 18,000.
3. Divide by a million: 18,000 / 1,000,000 = 0.018 dollars.

The 10,000 cached tokens cost as much as the 2,000 uncached ones, because a cache read on Opus 5.5
costs a twentieth of the input price. Without the cache, those 10,000 tokens would have cost
40,000 / 1,000,000 = 0.04 dollars on their own.

### Exercise 2.1 (LO-2.1, ★, about 10 minutes)

Write the `messages` list for this conversation, ready to send so that the model writes the next
reply. The user asked "Can you true a wheel?", the assistant answered "Yes, it takes about a
day.", and the user then asked "How much does it cost?". Then say what would happen on a current
model if the list ended after the assistant's answer.

<details>
<summary>Answer</summary>

```python
[
    {"role": "user", "content": "Can you true a wheel?"},
    {"role": "assistant", "content": "Yes, it takes about a day."},
    {"role": "user", "content": "How much does it cost?"},
]
```

A list that ends with an assistant turn asks the model to continue that turn, which is a prefill.
Current Claude models reject prefills, so the API returns an error.
</details>

### Exercise 2.2 (LO-2.1, ★, about 10 minutes)

A response's `content` holds three blocks: a text block "The pads are worn. ", a `tool_use` block,
and a text block "Replace them.". What does `response["content"][0]["text"]` give, and what should
code that wants the whole answer return? Name a response for which `content[0]["text"]` raises an
error.

<details>
<summary>Answer</summary>

`content[0]["text"]` gives only "The pads are worn. ", and loses "Replace them.". Code that wants
the whole answer joins the text of every text block, in order: "The pads are worn. Replace them.".
A response whose first block is a tool call, or whose content is empty, makes `content[0]["text"]`
fail with a `KeyError` or an `IndexError`.
</details>

### Exercise 2.3 (LO-2.2, ★★, about 15 minutes)

A request to Sonnet 5.5 reports 3,000 input tokens, 20,000 cache-read tokens, and 1,200 output
tokens, of which 900 were thinking. What did it cost, and how much of that paid for the thinking?

<details>
<summary>Answer</summary>

3,000 × 2 + 20,000 × 0.10 + 1,200 × 10 = 6,000 + 2,000 + 12,000 = 20,000, so 0.02 dollars.
Thinking tokens are billed as output, so the 900 thinking tokens cost 900 × 10 / 1,000,000 =
0.009 dollars: almost half of the request, for text the user never sees.
</details>

### Exercise 2.4 (LO-2.2, ★★, about 15 minutes)

Two requests to Haiku 5.5 each produce 2,000 output tokens. One has a 99,000-token prompt and the
other a 101,000-token prompt. Compute both costs and their ratio, and suggest what a program that
usually sends prompts near 100,000 tokens should do.

<details>
<summary>Answer</summary>

- 99,000 × 0.10 + 2,000 × 0.50 = 10,900, so 0.0109 dollars.
- 101,000 tokens is over 100,000, so the whole request pays the long-prompt prices:
  101,000 × 0.50 + 2,000 × 2.50 = 55,500, so 0.0555 dollars.

The second costs about 5.1 times as much for 2% more prompt. A program near the limit should keep
its prompts at or under 100,000 tokens, for example by retrieving fewer passages or trimming
history, and should count the tokens, since an estimate can't tell 99,000 from 101,000.
</details>

### Exercise 2.5 (LO-2.2, ★★, about 15 minutes)

You need short descriptions for 200,000 products. Each request has an 800-token prompt and a
200-token answer, on Sonnet 5.5. What does the job cost, and what in the Batch API? Which saves
more: halving the prompt, or halving the answer?

<details>
<summary>Hint</summary>

Work out one request's input cost and output cost separately first.
</details>

<details>
<summary>Answer</summary>

One request: 800 × 2 + 200 × 10 = 1,600 + 2,000 = 3,600, so 0.0036 dollars. The job costs
200,000 × 0.0036 = 720 dollars, or 360 in the Batch API.

Output is 2,000 of the 3,600, more than half, although it is a fifth of the tokens. Halving the
prompt saves 800 of 3,600, about 22%; halving the answer saves 1,000, about 28%. Asking for
shorter answers saves more.
</details>

### Exercise 2.6 (LO-2.2, ★, about 10 minutes)

A prompt combines 1,200,000 characters of documentation with 2,000 tokens of instructions, and the
request sets `max_tokens` to 8,000. Estimate with 2.5 characters per token: does it fit in a
1M-token window?

<details>
<summary>Answer</summary>

The documentation is about 1,200,000 / 2.5 = 480,000 tokens. With the instructions and the
answer's room, the total is 480,000 + 2,000 + 8,000 = 490,000 tokens, well inside 1,000,000. The
estimate has plenty of margin here, so a rough count is enough.
</details>

### Exercise 2.7 (LO-2.3, ★★★, about 25 minutes)

A chat on Opus 5.5 has a 500-token system prompt; each user message is 100 tokens and each reply
300. Compute the total cost of a 20-turn conversation that resends its whole history. Then compute
it again when the program keeps only the last four exchanges of history in each request. What does
the cheaper version lose?

<details>
<summary>Hint</summary>

Request k sends the system prompt, the k − 1 earlier exchanges of 400 tokens each, and the new
message. The output is 300 tokens a turn either way.
</details>

<details>
<summary>Answer</summary>

Whole history: request k sends 500 + (k − 1) × 400 + 100 input tokens. Over 20 turns that is
20 × 600 + 400 × (0 + 1 + … + 19) = 12,000 + 400 × 190 = 88,000 input tokens. The output is
20 × 300 = 6,000 tokens. The cost is (88,000 × 4 + 6,000 × 20) / 1,000,000 = 0.472 dollars.

Last four exchanges: requests 1–5 send 600, 1,000, 1,400, 1,800, and 2,200 tokens, 7,000 in all,
and requests 6–20 send 2,200 each, 33,000 in all, for 40,000 input tokens. The cost is
(40,000 × 4 + 120,000) / 1,000,000 = 0.28 dollars, about 40% less.

From turn 6 on, the model never sees the first exchanges, so anything said only there, such as
the user's name or the problem they started with, is lost.
</details>

### Exercise 2.8 (LO-2.3, ★★, about 15 minutes)

Choose a policy for keeping each history within budget (drop the oldest exchanges, summarize them,
or pin facts in the system prompt), and justify each choice in a sentence:

1. A support chat where the customer gives their order number in the first message.
2. A brainstorming chat, where only the last few ideas matter.
3. A tutoring chat, where the student's mistakes over the whole session shape the next hint.

<details>
<summary>Answer</summary>

1. Pin the order number in the system prompt, then drop the oldest exchanges: every later turn
   needs that one fact, and little else from the start.
2. Drop the oldest exchanges: early ideas no longer matter, and dropping is the cheapest policy.
3. Summarize: the pattern of mistakes matters, but not every word, and a summary keeps the
   pattern in a few lines.

Other answers can be right too, with a reason: for example, combining a summary with a pinned
fact.
</details>

### Exercise 2.9 (LO-2.4, ★, about 10 minutes)

Say what a program should do with each response:

1. A summary with `stop_reason` `"max_tokens"`, where summaries are usually much shorter than the
   limit.
2. A response with `stop_reason` `"model_context_window_exceeded"`, to a 990,000-token prompt.
3. A response with `stop_reason` `"refusal"`.

<details>
<summary>Answer</summary>

1. Don't show the cut-off text as a summary. Since summaries are usually much shorter, the prompt
   probably invited a long answer: ask for a stated length, rather than only raising the limit.
2. Shorten the prompt, for example by sending fewer documents. More `max_tokens` can't help,
   because the window is already full.
3. Show a fallback message, and don't present any of the content as an answer.
</details>

### Exercise 2.10 (LO-2.1, LO-2.4, ★★, about 20 minutes)

This function is in a real program:

```python
def answer(model, request):
    response = model(request)
    return response["content"][0]["text"]
```

Name three ways it can fail or mislead, and write a better version that raises a clear error in
each case.

<details>
<summary>Answer</summary>

1. It never checks `stop_reason`, so it returns a cut-off answer as if it were complete.
2. It returns whatever a refusal contains, as if it were an answer.
3. It assumes the first block is text, so it fails when the first block is a tool call or thinking,
   or when `content` is empty, and it drops any text blocks after the first.

```python
class Truncated(Exception):
    pass


class Refused(Exception):
    pass


def answer(model, request):
    response = model(request)
    reason = response["stop_reason"]
    if reason in ("max_tokens", "model_context_window_exceeded"):
        raise Truncated(f"the answer was cut off ({reason})")
    if reason == "refusal":
        raise Refused("the model declined to respond")
    if reason not in ("end_turn", "stop_sequence"):
        raise ValueError(f"stop reason {reason!r} needs its own handling")
    return "".join(b["text"] for b in response["content"] if b["type"] == "text")
```
</details>
