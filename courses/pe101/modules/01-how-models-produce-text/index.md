# Module 1: How language models produce text

**Objectives:** LO-1.1, LO-1.2, LO-1.3\
**Prerequisites:** the course's prerequisites, and [Python for the labs](../../python-primer.md) if
you are new to Python; this is the first module\
**Time:** about 7 hours: 2 for this reading, 3 for [Lab 1](lab01.ipynb), and 2 for the
[practice](practice.md)

Every technique in this course works on one mechanism: a language model reads a sequence of
tokens and predicts the next one, over and over. This module takes that mechanism apart, so the
rest of the course has something concrete to build on. You will see how text becomes tokens and
why the count of tokens, which sets both cost and limits, differs from the count of words. You
will see where next-token probabilities come from, how a model turns them into text, and why
the same prompt can give different answers. Last, you will see what the context window is and
why a model remembers nothing it can't see.

In Lab 1 you build a tokenizer and a small language model yourself. They are tiny, but they work
the same way as the real thing in every respect this module covers but one, which the reading
names.

## Text in, tokens out

A model doesn't read characters or words. It reads **tokens**: pieces of text from a fixed
vocabulary, each with a number. A common word is often one token. A rare word, a name, or a word
in a language the vocabulary saw little of is split into several. A **tokenizer** turns text
into tokens and back.

Most tokenizers for large language models learn their vocabulary with a method called byte-pair
encoding (BPE), which Sennrich, Haddow, and Birch adapted from data compression to split rare
words into pieces. BPE starts with single characters and repeats one step: find the pair of
adjacent symbols that occurs most often in a training text, and merge it into a new symbol.

### Worked example: three merges

Take a training text with three words: "ride" 4 times, "rider" twice, and "hide" 3 times. Start
with each word as a sequence of characters, and count every adjacent pair, weighted by how often
its word occurs:

| Pair | Where it occurs | Count |
| :- | :- | -: |
| `i d` | ride (4), rider (2), hide (3) | 9 |
| `d e` | ride (4), rider (2), hide (3) | 9 |
| `r i` | ride (4), rider (2) | 6 |
| `h i` | hide (3) | 3 |
| `e r` | rider (2) | 2 |

1. The most frequent pairs tie at 9. Break the tie by taking the pair counted first, `i d`, and
   merge it into the new symbol `id`. The words are now `r id e`, `r id e r`, and `h id e`.
2. Count again. `id e` now occurs 9 times and wins, so merge it into `ide`: `r ide`,
   `r ide r`, `h ide`.
3. Count again. `r ide` occurs 6 times, more than `h ide` (3) or `ide r` (2), so merge it:
   `ride`, `ride r`, `h ide`.

After three merges, "ride" is a single token, "rider" is two (`ride` and `r`), and "hide" is two
(`h` and `ide`). The vocabulary favors what the training text repeats most. A tokenizer for a
real model makes tens of thousands of merges over a huge training text, and then applies them,
in the order it learned them, to any new text.

### Why token counts differ from word counts

Because the merges come from the training text, a tokenizer packs text like its training text
tightly and splits other text into more pieces. In Lab 1, a tokenizer trained on English notes
about a bicycle shop gives 3.2 characters per token on those notes, and only about 1.5 on a
Spanish version of them and on a Python program. The word "mechanic" is one token, and
"mecánico" is five: `" mec"`, `"á"`, `"n"`, `"ic"`, and `"o"`.

Four consequences follow for anyone who writes prompts:

- **Cost and limits are counted in tokens, not words.** Anthropic's models overview gives a rule
  of thumb for the current Claude tokenizer: 1M tokens is roughly 555,000 words, or 2.5M
  characters. That is about 1.8 tokens per word, and the ratio is worse for code, numbers, and
  many other languages.
- **Token counts don't carry over between tokenizers.** Anthropic's pricing page says that Claude
  models from version 4.7 on use a newer tokenizer, which produces about 30% more tokens for the
  same text than the one before. The token-counting documentation says to recount prompts
  against the model you plan to use.
- **Tokens don't line up with words.** In Lab 1, "They" becomes `"The"` and `"y"`. A model that
  is asked to count letters, reverse a word, or match a rhyme works on pieces whose boundaries it
  never chose.
- **Spaces are part of tokens.** `" mechanic"`, with its leading space, and `"mechanic"`, without
  one, are different tokens. A prompt template that adds or drops a space changes the tokens the
  model reads.

## Next-token probabilities

A language model, given a sequence of tokens, returns a probability for every token in its
vocabulary: how likely that token is to come next. Write the probability that the next token is
$w$, given the context $c$ before it, as $P(w \mid c)$.

The simplest way to get these probabilities is to count. An **n-gram model** looks only at the
last $n - 1$ tokens. A trigram model ($n = 3$) uses the last two. For each pair of tokens in the
training text, it counts which tokens followed it, and divides:

$$P(w \mid c) = \frac{\text{count}(c, w)}{\sum_{w'} \text{count}(c, w')}$$

Shannon built text this way in 1948, sampling letters and words by their counts in English to
show how statistical structure makes text look more and more like language as $n$ grows.

### Worked example: a trigram's probabilities

Suppose the training text contains "the bike" 4 times: followed by " is" 3 times and " needs"
once. Then

$$P(\text{" is"} \mid \text{"the bike"}) = \frac{3}{4} = 0.75, \qquad
P(\text{" needs"} \mid \text{"the bike"}) = \frac{1}{4} = 0.25,$$

and every other token gets probability 0. A context the model never saw gets no probabilities at
all, which is the n-gram model's great weakness.

### What real models do differently

A large language model computes $P(w \mid c)$ with a neural network, the **transformer**, instead
of a table of counts. It looks at the whole context, up to many thousands of tokens, not only
the last two, and it gives sensible probabilities for contexts it never saw, because it has
learned patterns rather than memorizing sequences. This course doesn't teach how a transformer
works, because prompt engineering doesn't need it. Everything else in this module, from the
tokens going in to the sampling that comes out, works the same way for a transformer as for the
trigram model in Lab 1.

## From probabilities to text

The model's probabilities don't say which token to write. A **decoding** rule decides. Text comes
from a loop: get the probabilities for the context, choose a token, append it to the context,
and repeat, until the model chooses a token that ends its turn or reaches a length limit.

**Greedy decoding** always takes the most likely token. It sounds safe, but it fails. In Lab 1,
greedy decoding from "The mechanic" produces "The mechanic puts the bike in the tire. Then the
mechanic puts the bike in the tire. Then…" forever: once a sequence repeats, the most likely
continuation repeats with it. Holtzman and colleagues showed that large neural models fail the
same way, producing repetitive, bland text when decoding always favors the likeliest tokens.

**Sampling** instead picks each token at random, in proportion to its probability. A token with
probability 0.55 is chosen about 55 times in 100. Two settings reshape the probabilities before
the draw.

### Temperature

**Temperature** $T$ raises each probability $p_i$ to the power $1/T$, then rescales them so they
add up to 1:

$$p_i' = \frac{p_i^{1/T}}{\sum_j p_j^{1/T}}$$

Below 1, temperature sharpens the distribution toward the likeliest tokens; as $T$ approaches 0,
sampling approaches greedy decoding. Above 1, it flattens the distribution toward unlikely
tokens. At exactly 1, nothing changes.

**Worked example.** Take three tokens with probabilities 0.6, 0.3, and 0.1.

- At $T = 0.5$, the power is 2: 0.36, 0.09, and 0.01, which add up to 0.46. Dividing gives
  0.783, 0.196, and 0.022. The likeliest token went from 60% to 78%.
- At $T = 2$, the power is 0.5: square roots 0.775, 0.548, and 0.316, which add up to 1.639.
  Dividing gives 0.473, 0.334, and 0.193. The unlikely token almost doubled.

If one token has probability 1, every temperature leaves it at 1: temperature can't create a
choice where the model saw none.

### Top-p

**Top-p sampling**, also called nucleus sampling, from Holtzman and colleagues, keeps only the
most likely tokens whose probabilities add up to at least $p$, drops the rest, and rescales.

**Worked example.** With 0.6, 0.3, and 0.1, and $p = 0.8$: the first token alone reaches 0.6,
which is less than 0.8, so add the second, reaching 0.9. Keep those two, and rescale: 0.6 / 0.9 =
0.667 and 0.3 / 0.9 = 0.333. The third token can no longer be chosen. Top-p cuts off the tail of
unlikely tokens, where nonsense tends to come from, while leaving variety among the likely ones.

## Why one prompt gives different answers

Because each token is sampled, two runs of the same prompt can choose differently at the first
uncertain token, and every later token then follows a different context. In Lab 1, three seeds
for the random number generator give three different continuations of "The mechanic". The same
seed gives the same text every time, but that is a property of the lab's code: a hosted model
gives you no seed.

On current Claude models you can't turn the variety down with temperature either. Anthropic's
documentation for the Messages API says that Claude models from version 4.7 on don't support
`temperature`, `top_p`, or `top_k`: a request that sets one to anything but its default returns an
error, and with API version 2026-10-21 or later, a request that sets one at all does. So variety
is a fact of working with these models, and the course treats it that way:

- A clear prompt narrows the range of good answers, so the samples differ less in what matters.
  Modules 3 and 4 write such prompts.
- A required output format, checked in code, turns "different wording" into "same structure".
  Module 3 checks formats, and Module 8 uses structured outputs.
- Repeated runs measure how often a prompt succeeds, instead of trusting one sample. Module 7
  builds that measurement.

## The context window

A model reads a limited number of tokens at once: its **context window**. Anything outside the
window can't affect the prediction, however important it is. The trigram model's window is two
tokens. The current Claude models have a 1M-token context window, and can write up to 128K
tokens in one response, according to Anthropic's models overview.

A model also keeps nothing between requests. Each request is read from scratch: the model
doesn't remember an earlier conversation, an earlier answer, or an instruction you gave
yesterday. A chat program seems to remember because it sends the whole conversation again with
each new message. Module 2 builds that history, and keeps it inside the window.

### Worked example: will it fit?

A 300-page manual has about 90,000 words. At the overview's rule of thumb of 555,000 words per
1M tokens, it takes about 90,000 / 555,000 × 1,000,000 ≈ 162,000 tokens. It fits in a 1M-token
window with room for instructions and an answer. Count with the real tokenizer before you rely
on it: the rule of thumb is an average, and code, numbers, and many languages take more tokens
per word.

## Common misconceptions

- **"A token is a word."** It is a piece of text from the tokenizer's vocabulary. In Lab 1,
  "mecánico" takes five tokens and "They" takes two. Estimate tokens from characters or words
  only as a rough guide, and count with the model's tokenizer when it matters.
- **"A token count is a token count."** Counts depend on the tokenizer. Anthropic's newer
  tokenizer produces about 30% more tokens for the same text than the one before it, so a
  budget measured on an older model is wrong for a newer one.
- **"Lower temperature makes a model more accurate."** It makes the model more predictable, not
  more correct. The likeliest token can be wrong: the trigram model's greedy text, "puts the bike
  in the tire", is its likeliest output and makes no sense.
- **"Higher temperature makes a model more creative."** It only shifts probability toward tokens
  the model already rated unlikely. It adds no knowledge, and at a high enough temperature it
  mostly adds mistakes.
- **"The model remembers what I told it before."** It sees only what is in the current request,
  and only the part of that inside its context window. In Lab 1, a note at the start of a long
  text vanishes from a 500-token window, and nothing in the window says it was ever there.

## Summary

- A tokenizer turns text into tokens. BPE learns its vocabulary by merging the most frequent pair
  of symbols, so it packs text like its training text tightly and splits other text into more
  tokens. Costs and limits are counted in tokens, and counts differ between tokenizers.
- A language model gives a probability for every possible next token. An n-gram model counts; a
  transformer computes, from the whole context.
- Text comes from a decoding loop. Greedy decoding repeats itself; sampling varies. Temperature
  sharpens or flattens the probabilities, and top-p drops the unlikely tail.
- One prompt gives different outputs because each token is sampled. Current Claude models don't
  let you set a temperature, so prompts narrow the variety and evaluations measure it.
- A model sees only its context window, and nothing carries over between requests.

## Self-check

Answer each question before you open its answer.

1. A tokenizer was trained only on English. Will it give more or fewer tokens per word for French
   text than for English, and why?

   <details>
   <summary>Answer</summary>

   More. Its merges were learned from English, so common English words and word pieces are
   single tokens, while French words split into smaller pieces of the English merges.
   </details>

2. A next token has probability 0.2. After temperature 0.5 is applied, is its new probability
   higher, lower, or impossible to tell without the other probabilities?

   <details>
   <summary>Answer</summary>

   Impossible to tell. The new value is 0.2 squared, 0.04, divided by the sum of every squared
   probability, so it depends on the others. Next to one token at 0.8, it falls to
   0.04 / (0.64 + 0.04), about 0.059. Among five tokens at 0.2 each, it stays at 0.2.
   </details>

3. With probabilities 0.5, 0.3, 0.15, and 0.05, which tokens does top-p sampling with $p = 0.9$
   keep?

   <details>
   <summary>Answer</summary>

   The first three: 0.5 + 0.3 = 0.8 is less than 0.9, and adding 0.15 reaches 0.95. The token at
   0.05 is dropped.
   </details>

4. Why can't you make a current Claude model give the same answer every time by setting its
   temperature to 0?

   <details>
   <summary>Answer</summary>

   Current Claude models don't let you set one: the API returns an error if a request sets the
   temperature to anything but its default. Their outputs vary from run to run, so you narrow the
   variety with the prompt and measure it with repeated runs.
   </details>

5. A user tells a chat assistant their name in one conversation, and the next day, in a new
   conversation, the assistant doesn't know it. What happened?

   <details>
   <summary>Answer</summary>

   Nothing went wrong. The model keeps nothing between requests, and the new conversation's
   requests don't contain the earlier one. The assistant could know the name only if the program
   put it into the new request.
   </details>

## Further reading

- Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal*, 1948.
  Section 3, on approximations to English, builds text from letter and word counts, the idea
  behind Lab 1's trigram model, with striking examples.
- Sennrich, Haddow, and Birch, "Neural Machine Translation of Rare Words with Subword Units," ACL
  2016, [doi:10.18653/v1/P16-1162](https://doi.org/10.18653/v1/P16-1162). The paper that brought
  BPE to language processing; its first algorithm is a few lines of Python, close to Lab 1's.
- Holtzman, Buys, Du, Forbes, and Choi, "The Curious Case of Neural Text Degeneration," ICLR 2020,
  [arXiv:1904.09751](https://arxiv.org/abs/1904.09751). Why likely text is bland and repetitive,
  and the case for top-p sampling.
- Anthropic, [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview).
  Each current model's context window and output limit, and the rule of thumb for words per
  token.
- Anthropic, [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting).
  How to count a prompt's tokens against a particular model, and why counts from another model
  don't carry over.
