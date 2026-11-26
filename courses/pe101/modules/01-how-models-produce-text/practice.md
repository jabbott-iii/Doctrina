# Module 1 practice

These exercises practice retrieving what the [Module 1 reading](index.md) explained. They aren't
graded. Work each one on paper first, then check your answer, and only then confirm it with code
from [Lab 1](lab01.ipynb) if you like. The answers are in the collapsed blocks; open one only
after you have an answer of your own.

## Worked example: applying learned merges

The reading's tokenizer learned three merges, in this order: `i d`, then `id e`, then `r ide`.
How does it split "rider" and "tide"?

To encode a word, start from its characters and apply the learned merges in the order they were
learned, each wherever it fits:

1. "rider" starts as `r i d e r`. The first merge, `i d`, fits: `r id e r`. The second, `id e`,
   fits: `r ide r`. The third, `r ide`, fits: `ride r`. No merge joins `ride` and `r`, so "rider"
   is two tokens, `ride` and `r`.
2. "tide" starts as `t i d e`. The first two merges give `t ide`. The third needs an `r` before
   `ide`, so it doesn't fit, and "tide" is two tokens, `t` and `ide`.

A word the training text never contained can still be encoded, because every merge works on
pieces. It just takes more tokens.

### Exercise 1.1 (LO-1.1, ★, about 10 minutes)

With the same three merges, split "hider" and "ridden" into tokens. The first step of "hider" is
done for you: `h i d e r` becomes `h id e r`.

<details>
<summary>Hint</summary>

A merge fits only where its two symbols sit side by side. In "ridden", look at what follows `id`
after the first merge.
</details>

<details>
<summary>Answer</summary>

"hider" is three tokens: `h id e r` becomes `h ide r`, and `r ide` doesn't fit because the `r`
comes after `ide`, not before. So the tokens are `h`, `ide`, and `r`.

"ridden" is five tokens: `r i d d e n` becomes `r id d e n`, and then no other merge fits, because
`id` is followed by `d`, not `e`. So the tokens are `r`, `id`, `d`, `e`, and `n`. A word that looks
like the training words can still split badly.
</details>

### Exercise 1.2 (LO-1.1, ★★, about 20 minutes)

Train BPE by hand on a text that contains "tap" 5 times, "tape" 3 times, and "map" twice. Learn
three merges, breaking any tie in favor of the pair you counted first. Then split "mate" into
tokens, and explain why it takes as many tokens as it has letters, although every one of its
letters appears in the training text.

<details>
<summary>Hint</summary>

Count `a p` in all three words. After each merge, rewrite the words and count again: a merged
symbol forms new pairs with its neighbors.
</details>

<details>
<summary>Answer</summary>

1. The pairs are `a p` 10 (5 + 3 + 2), `t a` 8, `p e` 3, and `m a` 2. Merge `a p`: `t ap`,
   `t ap e`, `m ap`.
2. Now `t ap` is 8, `ap e` 3, and `m ap` 2. Merge `t ap`: `tap`, `tap e`, `m ap`.
3. Now `tap e` is 3 and `m ap` 2. Merge `tap e`: `tap`, `tape`, `m ap`.

"mate" is `m a t e`, four tokens. Every merge joins a pair that "mate" doesn't contain (`a p`,
`t ap`, `tap e`): its letters are familiar, but their order isn't. What matters to BPE is which
pairs are common, not which letters.
</details>

### Exercise 1.3 (LO-1.1, ★, about 10 minutes)

A support team's assistant writes 2,000 replies a day, of about 150 English words each. Using the
rule of thumb from Anthropic's models overview, that 1M tokens is roughly 555,000 words, estimate
the output tokens a day. Then name one reason the true count could be higher.

<details>
<summary>Answer</summary>

2,000 × 150 = 300,000 words a day. At 555,000 words per 1M tokens, that is 300,000 / 555,000 ×
1,000,000 ≈ 540,000 tokens a day.

The rule of thumb is an average. Replies with order numbers, product codes, or code take more
tokens per word, and so do replies in a language the tokenizer packs less tightly. A model with
a different tokenizer counts differently too.
</details>

### Exercise 1.4 (LO-1.2, ★, about 10 minutes)

In a training text, the context "the chain" is followed by " is" 6 times, " skips" 3 times, and
"." once. Give a trigram model's probabilities for the next token after "the chain", and the
probability it gives " rattles".

<details>
<summary>Answer</summary>

The context occurs 6 + 3 + 1 = 10 times, so " is" gets 6/10 = 0.6, " skips" 0.3, and "." 0.1.
" rattles" never followed the context, so it gets 0: a trigram model can't produce a continuation
it never saw in that context.
</details>

### Exercise 1.5 (LO-1.2, ★★, about 15 minutes)

Three tokens have probabilities 0.7, 0.2, and 0.1. Compute their probabilities after temperature
0.5 and after temperature 2, to three decimal places. Then say what the probabilities approach as
the temperature grows without limit.

<details>
<summary>Hint</summary>

Raise each probability to the power 1/T, then divide each result by their sum.
</details>

<details>
<summary>Answer</summary>

- At T = 0.5: squares 0.49, 0.04, and 0.01 add up to 0.54, so 0.907, 0.074, and 0.019.
- At T = 2: square roots 0.837, 0.447, and 0.316 add up to 1.600, so 0.523, 0.279, and 0.198.

As T grows, 1/T approaches 0, and each probability raised to the power 1/T approaches 1, so the
probabilities approach 1/3 each: every token the model gave any probability becomes equally
likely. A token with probability exactly 0 stays at 0.
</details>

### Exercise 1.6 (LO-1.2, ★, about 10 minutes)

Five tokens have probabilities 0.4, 0.25, 0.2, 0.1, and 0.05. Which does top-p sampling keep with
$p = 0.6$, and with $p = 0.9$? Give the rescaled probabilities in each case.

<details>
<summary>Answer</summary>

- With p = 0.6: 0.4 is less than 0.6, and 0.4 + 0.25 = 0.65 reaches it, so keep the first two:
  0.4 / 0.65 = 0.615 and 0.25 / 0.65 = 0.385.
- With p = 0.9: 0.4 + 0.25 + 0.2 = 0.85 is less than 0.9, and adding 0.1 reaches 0.95, so keep the
  first four, each divided by 0.95: 0.421, 0.263, 0.211, and 0.105.
</details>

### Exercise 1.7 (LO-1.2, ★★, about 15 minutes)

A trigram model over words has these counts:

| Context | Next words |
| :- | :- |
| the bike | is (3), needs (1) |
| bike is | ready (2), in (1) |
| is ready | . (4) |
| ready . | the (3), call (1) |
| . the | bike (5) |

Write the first ten words that greedy decoding produces after "the bike". Explain why the text
never ends, and say at which contexts sampling at temperature 1 could leave the loop.

<details>
<summary>Answer</summary>

"is ready . the bike is ready . the bike". Greedy decoding takes "is", "ready", ".", "the", and
"bike", which brings the context back to "the bike", so the same five words repeat forever.

Sampling can leave the loop wherever a context has more than one next word: at "the bike" it
picks "needs" a quarter of the time, at "bike is" it picks "in" a third of the time, and at
"ready ." it picks "call" a quarter of the time. "is ready" and ". the" have only one next word,
so no setting changes them.
</details>

### Exercise 1.8 (LO-1.3, ★, about 10 minutes)

A chat program keeps only the last 8,000 tokens of a conversation in each request. The user's
first message, 300 tokens long, says "Answer in French from now on." Forty exchanges of about 250
tokens each follow. Is the first message still in the window? What will the user notice, and
where should a standing instruction like that go instead?

<details>
<summary>Answer</summary>

The conversation is 300 + 40 × 250 = 10,300 tokens, more than 8,000, so the oldest 2,300 tokens,
the first message among them, have been dropped. The model never sees the instruction again, so
the user will notice the answers drift back to English, with no error to explain why.

A standing instruction belongs where it is sent with every request and never trimmed: the system
prompt, which Modules 2 and 3 cover.
</details>

### Exercise 1.9 (LO-1.2, LO-1.3, ★★, about 15 minutes)

A colleague sees two different answers to the same prompt from a current Claude model and
proposes setting the temperature to 0 to make them match. In three or four sentences, explain why
that won't work, and what to do instead.

<details>
<summary>Answer</summary>

Current Claude models don't let you set a temperature: the API returns an error if a request sets
it to anything but its default. The answers differ because each token is sampled, so the
variation can't be switched off. Instead, narrow it: state the task and the output's format
clearly, and check the format in code. Then measure how often the prompt succeeds over repeated
runs, rather than judging it from one answer.
</details>

### Exercise 1.10 (LO-1.1, LO-1.3, ★★, about 20 minutes)

You want a summary of 600,000 words of meeting transcripts in one request to a model with a
1M-token context window. The instructions take 2,000 tokens, and you allow up to 4,000 tokens for
the answer. Using the rule of thumb of 555,000 words per 1M tokens, does the request fit? If not,
describe one way to do the job anyway.

<details>
<summary>Hint</summary>

The window has to hold the input and the output together.
</details>

<details>
<summary>Answer</summary>

The transcripts alone are about 600,000 / 555,000 × 1,000,000 ≈ 1,081,000 tokens, already more
than 1M, before the 2,000 tokens of instructions and the 4,000 of answer. It doesn't fit, and the
estimate is rough, so even a near miss would deserve a real count.

One way: split the transcripts into parts that fit with room to spare, summarize each part in its
own request, then summarize the summaries in a final request. Module 6 builds this kind of chain,
and Module 10 shows how to pick only the passages a question needs.
</details>
