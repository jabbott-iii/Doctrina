# Module 2: The anatomy of a request

**Objectives:** LO-2.1, LO-2.2, LO-2.3, LO-2.4\
**Prerequisites:** [Module 1](../01-how-models-produce-text/index.md)\
**Time:** about 6 hours: 2 for this reading, 2.5 for [Lab 2](lab02.ipynb), and 1.5 for the
[practice](practice.md); [PA1](../../assignments/pa1/pa1.ipynb) follows, and takes about 3 more

Every prompt reaches a model inside a request, and every answer comes back inside a response.
This module takes both apart, using the Claude Messages API as the example. You will build
requests as data, read the parts of a response that code must check, and work out what a request
costs before you send it. You will also see how a program holds a conversation with a model that
remembers nothing, what that costs, and what to do when the conversation outgrows its budget.
The course never sends a request, but everything here is what a real program sends and reads.

## A request is a JSON object

A program talks to the Messages API by sending an HTTP `POST` request to
`https://api.anthropic.com/v1/messages`, with three headers: `x-api-key`, which carries the
account's secret key; `anthropic-version`, which names the version of the API the program was
written for; and `content-type: application/json`. The body is a JSON object. Here is one, as the
Python dictionary that Lab 2 builds:

```python
request = {
    "model": "claude-opus-5-5",
    "max_tokens": 300,
    "system": "You answer questions for the customers of a bicycle repair shop, in one sentence.",
    "messages": [
        {"role": "user", "content": "How often should I clean my chain?"},
    ],
}
```

- **`model`** names the model by its ID. The current models are `claude-opus-5-5`,
  `claude-sonnet-5-5`, and `claude-haiku-5-5`, among others in Anthropic's models overview.
- **`max_tokens`** is the most tokens the model may write in its answer. It is a ceiling, not a
  target: the model usually stops well before it. On models that think before they answer, which
  includes Claude Opus 5.5, the thinking tokens count toward `max_tokens` too.
- **`system`** is the system prompt: instructions and context that apply to the whole
  conversation. It is a string, or a list of text blocks. Module 3 decides what belongs in it.
- **`messages`** is the conversation so far, oldest first. Each message has a `role`, `"user"`
  or `"assistant"`, and `content`, which is a string or a list of content blocks. A string is
  shorthand for a list of one text block.

The messages alternate between the user and the assistant, and the last one is the user's,
because the model writes the next turn. The API reference says it combines two user turns in a
row into one turn, so code that builds requests should alternate on purpose rather than rely on
that.

### Prefill is gone

Older guides teach **prefilling**: ending `messages` with an assistant turn that holds the start
of the answer, such as `{`, so the model continues from there. Anthropic's documentation says
that only Claude 4.5 and earlier models accept a prefill, and that all other models return an
error for it. Current models get the same effect from clear format instructions (Module 3) and
structured outputs (Module 8).

## A response is a JSON object too

Here is an illustrative response to that request, in the documented shape. A person wrote its
text for this course; no model produced it.

```python
{
    "id": "msg_standin_0001",
    "type": "message",
    "role": "assistant",
    "model": "claude-opus-5-5",
    "content": [{"type": "text", "text": "Clean it once a month, or after any ride in the rain."}],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {
        "input_tokens": 41,
        "output_tokens": 18,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    },
}
```

- **`content`** is a list of blocks, each with a `type`. A plain answer has a `"text"` block.
  Other types carry a tool call (Module 8) or the model's thinking (Module 6), so code that wants
  the answer picks out the text blocks rather than reading the first block.
- **`stop_reason`** says why the model stopped. Check it before you use the text, as the section
  on stop reasons below explains.
- **`usage`** counts the tokens the request used and the response produced. The cache fields count
  input tokens written to or read from the prompt cache, which Module 10 covers; here they are 0.
  Real responses can carry more fields than these, and their IDs look like
  `msg_01XFDUDYJgAACzvnptvVoYEL`.

The `usage` counts are the truth about what a request cost. An estimate made before the request,
from characters or words, is only a plan.

## What a request costs

Anthropic prices each model per million tokens, separately for input, output, cache writes, and
cache reads. These prices for the three current models were taken from Anthropic's pricing page on
November 26, 2026, and are in the course's `data/prices.json`:

| Model | Input | Output | Cache write (5 minutes) | Cache read |
| :- | -: | -: | -: | -: |
| Claude Opus 5.5 | `$4.00` | `$20.00` | `$5.00` | `$0.20` |
| Claude Sonnet 5.5 | `$2.00` | `$10.00` | `$2.50` | `$0.10` |
| Claude Haiku 5.5 | `$0.10` | `$0.50` | `$0.125` | `$0.01` |

The prices are in US dollars per million tokens. Prices change, so check the pricing page before
you rely on these. Four rules from the same page matter for planning:

- **Output costs five times as much as input** on all three models, so a long answer can cost
  more than a long prompt.
- **Thinking tokens are billed as output tokens,** even when the thinking text isn't returned, so
  `output_tokens` can be much larger than the visible answer.
- **The Message Batches API takes 50% off** input and output, for work that can wait for its
  results rather than needing them at once.
- **Haiku 5.5 charges more for long prompts.** A request whose prompt is over 100,000 tokens pays
  higher prices for the whole request: five times the input price and five times the output
  price. The prompt length counts every input token, including cache reads and writes.

A request's cost $C$ is each count from `usage` times its price, divided by a million:

$$C = \frac{n_\text{in} \, p_\text{in} + n_\text{out} \, p_\text{out}
      + n_\text{write} \, p_\text{write} + n_\text{read} \, p_\text{read}}{1{,}000{,}000}$$

### Worked example: one request, then ten thousand

The response above used 41 input and 18 output tokens on Opus 5.5:

$$C = \frac{41 \times 4 + 18 \times 20}{1{,}000{,}000} = \frac{164 + 360}{1{,}000{,}000}
= 0.000524 \text{ dollars}$$

That is about a twentieth of a cent. Now plan a workload: 10,000 requests, each with a
1,500-token prompt and a 300-token answer, on Opus 5.5. One request costs
(1,500 × 4 + 300 × 20) / 1,000,000 = 0.012 dollars, so the workload costs 120 dollars, or 60 in
the Batch API. On Haiku 5.5, the same workload costs 3 dollars, or 1.50 in the Batch API.
Whether Haiku does the task well enough is a separate question, which only an evaluation
(Module 7) can answer.

## Will it fit?

The context window holds the prompt and the answer together. The current Claude models each have
a 1M-token window and can write at most 128K tokens in one response, according to Anthropic's
models overview. So a request needs room for both: its prompt tokens plus its `max_tokens`
within the window, and its `max_tokens` within the output limit. If an answer does fill the
window, the response stops with the reason `model_context_window_exceeded`.

To check before you have a real count, estimate. Module 1's rule of thumb, 2.5 characters per
token, gives a 2-million-character manual about 800,000 tokens, which fits with room for a
4,000-token answer. Anthropic also offers a token-counting endpoint, free to use, which counts a
prompt exactly for a given model. This course estimates instead, since it never calls the API.

## Conversations

A model keeps nothing between requests. A chat program keeps the conversation in its own memory,
as a list of messages, and sends the whole list with each new message. The model can use an
earlier turn only because the program sent it again.

### Worked example: what a conversation costs

A support chat has a 200-token system prompt. Each user message is about 60 tokens and each reply
about 150. Request 1 sends 200 + 60 = 260 input tokens. Request 2 sends those, the first reply,
and the new message: 200 + 210 + 60 = 470. Each request sends 210 more than the one before, so
request 30 sends 200 + 29 × 210 + 60 = 6,350. Over 30 turns, the requests send 99,150 input tokens
to carry 6,300 tokens of conversation. The total grows with the square of the number of turns,
because every turn is paid for again by every request after it.

### When the history outgrows its budget

Long conversations hit two limits: the context window, and the budget you set for cost. Three
policies keep a history within a budget, and each loses something:

- **Drop the oldest exchanges.** Simple and predictable, but whatever the user said early on,
  such as their name or their bike's color, is gone. Drop whole exchanges, so the history still
  starts with a user message.
- **Summarize the dropped turns.** Replace the oldest exchanges with one short message that sums
  them up. It keeps the gist, costs a request to write, and loses detail the summary left out.
- **Pin what must last.** Move facts that every later turn needs into the system prompt, which is
  sent with every request and never trimmed.

Prompt caching, in Module 10, makes the repeated part of each request cheaper without dropping
anything, but it doesn't make a history fit a window it has outgrown.

## Why the model stopped

Every response gives a `stop_reason`. Anthropic's documentation lists seven:

| `stop_reason` | What happened | What code should do |
| :- | :- | :- |
| `"end_turn"` | The model finished its answer | Use the text |
| `"stop_sequence"` | The model wrote one of the request's `stop_sequences` | Use the text; `stop_sequence` says which one |
| `"max_tokens"` | The answer reached `max_tokens` and was cut off | Don't show it as complete; retry with more room, or shorten what you ask for |
| `"model_context_window_exceeded"` | The answer filled the context window and was cut off | Shorten the prompt; more `max_tokens` won't help |
| `"refusal"` | The model declined to respond | Show a fallback, and never present the content as an answer |
| `"tool_use"` | The model is asking to call a tool | Run the tool and send its result back (Module 8) |
| `"pause_turn"` | A loop of server-side tools reached its limit | Send the response back to let it continue; this course doesn't use server-side tools |

A cut-off answer and a refusal arrive as ordinary, successful responses. The API reports an error
only when the request itself is wrong, such as a prefill or a `temperature` on a current model.
Code that reads `content` without checking `stop_reason` will eventually show a user half an
answer as if it were whole.

## Common misconceptions

- **"`max_tokens` sets the answer's length."** It is a ceiling. The model stops when it is done,
  usually well below it, and the thinking tokens of a thinking model count toward it too. To get
  shorter answers, ask for them in the prompt.
- **"The model remembers our conversation."** It sees only the messages in the current request.
  In Lab 2, a trimmed history no longer mentions the bike's color, so no model could answer a
  question about it.
- **"A truncated answer raises an error."** It arrives as a normal response with
  `stop_reason` `"max_tokens"`. Only checking the stop reason catches it.
- **"Input is cheap, so prompt length doesn't matter."** Input costs a fifth as much as output per
  token, but every request pays for its whole prompt, and a conversation pays for its history
  again on every turn. In the worked example, 30 turns send 99,150 input tokens.
- **"My estimate is what I'll pay."** Estimates from characters or words are rough. The `usage`
  fields of each response are the actual counts, and the bill is computed from them.

## Summary

- A request is a JSON object: a model, `max_tokens`, a system prompt, and messages that alternate
  and end with the user's. A request that ends with an assistant turn is a prefill, which current
  models reject.
- A response holds content blocks, a stop reason, and token usage. Pick out the text blocks, and
  check the stop reason first.
- Cost is each kind of token times its price. Output costs five times as much as input, thinking
  is billed as output, the Batch API halves both, and Haiku 5.5 charges more above 100,000 prompt
  tokens.
- The context window must hold the prompt and the answer, and `max_tokens` has its own limit.
- A conversation lives in the program, which resends the history every time. Its cost grows with
  the square of its length, and trimming it loses what it drops.

## Self-check

1. A request's `messages` ends with an assistant turn holding `"{"`. What happens on Claude Opus
   5.5, and what should the program do instead?

   <details>
   <summary>Answer</summary>

   The API returns an error, because current models reject prefills. To get JSON, say so in the
   prompt and check the output in code (Module 3), or use structured outputs (Module 8).
   </details>

2. A response from Sonnet 5.5 reports 2,000 input tokens and 500 output tokens, with no caching.
   What did it cost?

   <details>
   <summary>Answer</summary>

   (2,000 × 2 + 500 × 10) / 1,000,000 = 9,000 / 1,000,000 = 0.009 dollars, almost a cent.
   </details>

3. A prompt is 990,000 tokens, and the request sets `max_tokens` to 16,000. Will the answer have
   room in a 1M-token window?

   <details>
   <summary>Answer</summary>

   No. 990,000 + 16,000 = 1,006,000, more than 1,000,000. If the answer runs long, it fills the
   window and stops with `model_context_window_exceeded`. Shorten the prompt or lower
   `max_tokens`.
   </details>

4. Why does a 40-turn conversation cost far more than four 10-turn conversations of the same
   messages?

   <details>
   <summary>Answer</summary>

   Each request resends the whole history, so turn k pays again for all k − 1 turns before it,
   and the total grows with the square of the number of turns. Four short conversations each start
   over with an empty history.
   </details>

5. A response has `stop_reason` `"max_tokens"`. Name two things the program could do, and say
   when each is right.

   <details>
   <summary>Answer</summary>

   Retry with a larger `max_tokens`, when the answer is legitimately long. Or change the prompt to
   ask for less, when the answers are longer than they should be. In both cases, don't show the
   cut-off text as complete.
   </details>

## Further reading

- Anthropic, [Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages).
  Requests, responses, multi-turn conversations, and the notes on prefill and sampling settings
  for current models.
- Anthropic, [Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons).
  Each stop reason, with what code should do about it.
- Anthropic, [Pricing](https://platform.claude.com/docs/en/about-claude/pricing). The current
  prices, the batch discount, the cache multipliers, and the long-prompt rule; check it before
  you plan a budget.
- Anthropic, [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview).
  Each model's ID, context window, and output limit.
