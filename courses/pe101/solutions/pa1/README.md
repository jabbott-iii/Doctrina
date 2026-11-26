# PA1 answer key and grading notes

`pa1.py`, paired with `pa1.ipynb`, is the source of PA1: the model solutions, the visible tests,
and the hidden tests. Students receive `assignments/pa1/pa1.ipynb`, which
`tools/student_version.py` makes from it. Change the source, never the student version, and then
make the student version again.

The autograder awards each test cell's points when every test in it passes. Problem 6's written
answer, 1 point, is scored by hand against the model answer in the source: full credit for saying
that the trimmed requests leave out the early turns, and that the model can use only what each
request contains.

## Reasoning and common mistakes

### Problem 1: Build the request

Checking each message's role against its position catches both kinds of bad history: one that
starts with the assistant, and one with two user turns in a row. The common mistake is checking
only the last message. A second is `history + [new]`, which copies the list but shares the message
dictionaries, so a caller who edits the request edits the history too; a hidden test catches it.
Treating an empty `stop_sequences` list as "include the key" sends a useless empty list, which the
hidden tests reject.

### Problem 2: A cost report

Each response is priced by its own `model` field, so a mixed list needs a lookup per response.
Students often forget that cache writes count toward Haiku's long-prompt limit, or compare with
`>=` instead of `>`, so a prompt of exactly 100,000 tokens gets the higher price. `usage.get` with a
default handles the responses that leave out the cache fields.

### Problem 3: How many can we afford?

`budget // one` alone gives 299 for the hidden test with a 0.3-dollar budget, because
`0.3 / 0.001` is `299.99999999999994` in floating point. Rounding the quotient to a few decimal
places first, as the model solution does, or working in millionths of a dollar with integers,
avoids it. The long-prompt test checks that the prompt size picks Haiku's prices.

### Problem 4: Keep the history within budget

Without `keep_first`, dropping two messages at a time from the front until the rest fits is
enough. With it, the first exchange and the newest message stay fixed, and only the exchanges
between them are dropped. The last hidden case, where the first exchange and the newest message
don't fit together, is the one students miss: the statement says to keep the newest message only.

### Problem 5: A reply, whatever happens

The loop resends only for `"max_tokens"`, and only while `max_tokens` is below the ceiling. Two
mistakes are common: doubling past the ceiling (100, 200, 400 with a ceiling of 300), and retrying
on `"model_context_window_exceeded"`, which more room can't fix. Copying the request with
`dict(request)` is enough, since only `max_tokens` changes.

### Problem 6: What a conversation costs

Request k sends the system prompt, its kept earlier exchanges, and the new message. The common
mistake is off by one: counting k exchanges for request k instead of k − 1. The hidden tests
include the reading's worked example, 99,150 tokens, and Practice Exercise 2.7's trimmed case,
40,000.
