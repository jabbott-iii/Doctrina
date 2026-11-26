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
# # Lab 1: How language models produce text
#
# **Objectives:** LO-1.1, LO-1.2, LO-1.3\
# **Prerequisites:** the [Module 1 reading](index.md)\
# **Time:** about 3 hours
#
# In this lab you build the two halves of a tiny language model from scratch. First, a
# byte-pair encoding (BPE) tokenizer, which you train on a short text about a bicycle repair shop
# and use to count tokens in prose, Spanish, Python code, and numbers. Second, a trigram model,
# which predicts the next token from the two before it. Then you generate text with it, change
# the temperature and top-p settings, measure how they change the output's variety, and watch
# what falls out of a context window.
#
# No cell calls a real language model. The model here is the one you build, and every text it
# learns from was written for this course.
#
# Each exercise ends with a check cell. Run it after your answer: it prints `passed` or fails
# with a message that says what is wrong. Run the cells in order, from the top. Some cells fail
# on purpose until you finish the exercise above them: each check, and the cells that use your
# answer.

# %% [markdown]
# ## Setup
#
# The first cell imports what the lab uses and prints the versions it was written for. Every
# random choice in this lab uses a seed that the cell names, so every run gives the same results.

# %%
import random
import re
import sys
from collections import Counter, defaultdict

import matplotlib
import matplotlib.pyplot as plt

import promptlab

print("Python", sys.version.split()[0], "| matplotlib", matplotlib.__version__,
      "| promptlab", promptlab.__version__)

# %% [markdown]
# ## 1. Characters, words, and tokens
#
# The corpus, the text the model learns from, is a set of notes on how a bicycle repair shop
# works. Three more texts test the tokenizer on other kinds of writing: part of the notes in
# Spanish, a short Python program, and a list of prices and measurements. The next cell reads
# all four and counts their characters and words.

# %%
texts = {
    "prose": promptlab.data_path("corpus/shop-notes.txt").read_text(encoding="utf-8"),
    "spanish": promptlab.data_path("corpus/notas-del-taller.txt").read_text(encoding="utf-8"),
    "code": promptlab.data_path("corpus/repair_board.py.txt").read_text(encoding="utf-8"),
    "numbers": promptlab.data_path("corpus/numbers.txt").read_text(encoding="utf-8"),
}
for name, text in texts.items():
    print(f"{name:8} {len(text):6,} characters {len(text.split()):6,} words")

# %% [markdown]
# ## 2. A byte-pair encoding tokenizer
#
# A tokenizer turns text into a list of tokens, the units a model reads and writes. Byte-pair
# encoding builds its vocabulary from a training text. It starts with single characters, then
# repeats one step: find the pair of adjacent symbols that occurs most often, and merge it into
# a new symbol. After many merges, common words and word pieces have become single tokens, and
# rare words are still split into pieces.
#
# Real tokenizers first split the text into chunks that a merge may not cross, so that a token
# never spans two words. This one makes each chunk a run of letters with the space before it, a
# single digit with the space before it, a run of punctuation, a run of underscores, or a run of
# whitespace. Joining the chunks gives back the text exactly, which the cell checks.

# %%
CHUNK = re.compile(r" ?[^\W\d_]+| ?\d| ?[^\w\s]+| ?_+|\s+")


def chunks(text):
    """Split text into the chunks that a merge may not cross."""
    return CHUNK.findall(text)


print(chunks("The mechanic checks 2 brakes, then_rides."))
assert "".join(chunks(texts["code"])) == texts["code"], "chunking lost or changed characters"

# %% [markdown]
# Training counts each chunk once, with the number of times it occurs, as a tuple of symbols.
# `count_pairs` counts every adjacent pair of symbols, weighted by how often its chunk occurs.
# `merge_pair` replaces each occurrence of one pair in a chunk with the merged symbol, scanning
# from left to right.

# %%
def count_pairs(words):
    """Count adjacent symbol pairs in a Counter that maps symbol tuples to their frequencies."""
    pairs = Counter()
    for symbols, count in words.items():
        for pair in zip(symbols, symbols[1:]):
            pairs[pair] += count
    return pairs


def merge_pair(symbols, pair):
    """Return the symbol tuple with every occurrence of pair merged into one symbol."""
    merged, i = [], 0
    while i < len(symbols):
        if i + 1 < len(symbols) and (symbols[i], symbols[i + 1]) == pair:
            merged.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            merged.append(symbols[i])
            i += 1
    return tuple(merged)


def train_bpe(text, num_merges):
    """Learn up to num_merges merges from text, in the order they were learned."""
    words = Counter(tuple(chunk) for chunk in chunks(text))
    merges = []
    for _ in range(num_merges):
        pairs = count_pairs(words)
        if not pairs:
            break
        best = pairs.most_common(1)[0][0]  # a tie goes to the pair counted first
        merges.append(best)
        words = Counter({merge_pair(symbols, best): n for symbols, n in words.items()})
    return merges


def encode(text, merges):
    """Split text into tokens: apply the learned merges to each chunk, earliest merge first."""
    rank = {pair: i for i, pair in enumerate(merges)}
    tokens = []
    for chunk in chunks(text):
        symbols = tuple(chunk)
        while len(symbols) > 1:
            ranked = [(rank[p], p) for p in zip(symbols, symbols[1:]) if p in rank]
            if not ranked:
                break
            symbols = merge_pair(symbols, min(ranked)[1])
        tokens.extend(symbols)
    return tokens


# %% [markdown]
# `train_bpe` keeps each chunk's frequency, so merging is fast even on a long text: a chunk such
# as `" the"` is merged once for all of its occurrences. Here is a tiny training text, the
# classic example from the BPE paper's tradition, with words repeated so their counts differ.

# %%
tiny = "low " * 5 + "lower " * 2 + "newest " * 6 + "widest " * 3
print(Counter(chunks(tiny)))

# %% [markdown]
# ### Exercise L1.1 (LO-1.1, ★, about 15 minutes)
#
# Predict the first three merges that `train_bpe(tiny, 3)` learns, before you run it. Work them
# out by hand: list the chunks with their counts, count the adjacent pairs, merge the most
# frequent, and count again. Notice that each chunk except the first starts with a space, which
# is a symbol like any other. Write your answer as a list of three pairs, each a tuple of two
# strings, such as `[("a", "b"), ("ab", "c"), …]`.
#
# <details>
# <summary>Hint</summary>
#
# The chunk `" newest"` occurs six times, so each of its pairs starts with a count of 6. A pair
# that also occurs in another chunk gets that chunk's count added. After a merge, the new symbol
# can pair with its neighbors.
# </details>

# %% tags=["answer-L1.1"]
predicted_merges = []  # your three pairs, in order

# %% tags=["raises-exception"]
actual = train_bpe(tiny, 3)
assert len(predicted_merges) == 3, f"predict exactly three merges, not {len(predicted_merges)}"
for n, (guess, real) in enumerate(zip(predicted_merges, actual), start=1):
    assert tuple(guess) == real, (
        f"merge {n}: you predicted {guess!r}, and the tokenizer learned {real!r}"
    )
print("passed:", actual)

# %% [markdown]
# Now train on the shop notes with 300 merges, and encode a few sentences. The tokenizer prints
# each token in quotes, so you can see where the spaces went.

# %%
merges = train_bpe(texts["prose"], 300)
print("first ten merges:", merges[:10])
for sentence in ["The mechanic fixed the flat tire.",
                 "They replaced the derailleur.",
                 "El mecánico reparó la llanta.",
                 "total 132.48"]:
    print(encode(sentence, merges))

# %% [markdown]
# Words that are common in the training text, such as `" mechanic"`, became single tokens. A word
# the text never uses, such as `" replaced"`, splits into pieces, and so does nearly every Spanish
# word, because the merges were learned from English. Every digit is its own token, because the
# chunking splits digits apart. Real tokenizers make their own choices about digits, which is
# one reason a token count from one tokenizer doesn't carry over to another.

# %% [markdown]
# ### Exercise L1.2 (LO-1.1, ★★, about 20 minutes)
#
# 1. Write `chars_per_token(text, merges)`, which returns the number of characters in `text`
#    divided by the number of tokens `encode` gives it. More characters per token means the
#    tokenizer packs the text more tightly, so the text costs fewer tokens.
# 2. Before you measure the four texts, predict their order, from most characters per token to
#    fewest, and write it in `my_ranking`, using the names in `texts`. Then run the check, which
#    measures them.

# %% tags=["answer-L1.2"]
def chars_per_token(text, merges):
    raise NotImplementedError("Exercise L1.2")


my_ranking = []  # the four names, most characters per token first

# %% tags=["raises-exception"]
assert chars_per_token("ab", []) == 1.0, "with no merges, every character is a token"
assert chars_per_token("aaaa", [("a", "a")]) == 2.0, "one merge turns 'aaaa' into two tokens"
measured = {name: chars_per_token(text, merges) for name, text in texts.items()}
for name, value in sorted(measured.items(), key=lambda item: -item[1]):
    print(f"{name:8} {value:.2f} characters per token")
actual_ranking = sorted(measured, key=measured.get, reverse=True)
assert sorted(my_ranking) == sorted(texts), f"rank exactly these four: {sorted(texts)}"
assert my_ranking == actual_ranking, (
    f"you predicted {my_ranking}, and the measured order is {actual_ranking}: "
    "find the reason for each difference before you change your answer"
)
print("passed")

# %% [markdown]
# ### Exercise L1.3 (LO-1.1, ★★, about 20 minutes)
#
# A bigger vocabulary, from more merges, packs text into fewer tokens. Does it help every kind
# of text equally? Write `tokens_by_merges(text, merge_counts)`, which trains a tokenizer on the
# prose (`texts["prose"]`) once for each number in `merge_counts`, and returns the list of token
# counts that each gives `text`, in the same order.
#
# <details>
# <summary>Hint</summary>
#
# Train once per count with `train_bpe(texts["prose"], n)`, then `len(encode(text, ...))`. Since
# training is the slow part, you may train once with the largest count and use the first `n`
# merges of the result for each smaller `n`: the first `n` merges never depend on later ones.
# </details>

# %% tags=["answer-L1.3"]
def tokens_by_merges(text, merge_counts):
    raise NotImplementedError("Exercise L1.3")


# %% tags=["raises-exception"]
merge_counts = [0, 50, 150, 300, 600]
results = {name: tokens_by_merges(text, merge_counts) for name, text in texts.items()}
for name, counts in results.items():
    assert counts[0] == len(texts[name]), f"with 0 merges, {name} has one token per character"
    assert counts == sorted(counts, reverse=True), (
        f"more merges never add tokens, but {name} got {counts}"
    )
assert results["prose"][-1] == len(encode(texts["prose"], train_bpe(texts["prose"], 600)))
print("passed")

# %% [markdown]
# The next cell plots tokens per 100 characters against the number of merges, for each text.
# The four lines use colors and markers that readers with color vision deficiencies can tell
# apart. Before you run it, predict which line falls furthest.

# %% tags=["raises-exception"]
fig, ax = plt.subplots(figsize=(7, 4))
styles = {"prose": ("#0072B2", "o"), "spanish": ("#E69F00", "s"),
          "code": ("#009E73", "^"), "numbers": ("#CC79A7", "D")}
for name, counts in results.items():
    color, marker = styles[name]
    per_100 = [100 * n / len(texts[name]) for n in counts]
    ax.plot(merge_counts, per_100, color=color, marker=marker, label=name)
ax.set_xlabel("merges learned from the English prose")
ax.set_ylabel("tokens per 100 characters")
ax.set_title("More merges help most the kind of text they were learned from")
ax.legend()
plt.show()

# %% [markdown]
# The chart starts every line at 100 tokens per 100 characters, because with no merges each
# character is a token. The prose line falls furthest, to about 25 by 600 merges, because every
# merge was learned from it. The other three level off between about 60 and 75. The numbers line
# falls least, because digits are never merged: only the words and punctuation around them get
# shorter. A tokenizer is cheapest on text like its training text, and a model's tokenizer is
# trained on far more text than this one.

# %% [markdown]
# ## 3. Next-token probabilities
#
# A language model gives, for every context, a probability for each token that could come next.
# A trigram model gets them by counting: for each pair of tokens in the training text, it counts
# which token followed that pair, and how often. The probability of a next token is its count
# divided by the total for that context:
#
# $$P(w \mid c) = \frac{\text{count}(c, w)}{\sum_{w'} \text{count}(c, w')}$$
#
# The next cell encodes the prose with the 300-merge tokenizer and counts every trigram.

# %%
corpus_tokens = encode(texts["prose"], merges)
trigram_counts = defaultdict(Counter)
for a, b, c in zip(corpus_tokens, corpus_tokens[1:], corpus_tokens[2:]):
    trigram_counts[(a, b)][c] += 1
print(f"{len(corpus_tokens):,} tokens, {len(trigram_counts):,} contexts")
print(trigram_counts[(".", " The")].most_common(5))

# %% [markdown]
# ### Exercise L1.4 (LO-1.2, ★, about 15 minutes)
#
# Write `next_token_probabilities(counts, context)`, which returns a dictionary from each token
# that followed `context` to its probability, using the formula above. For a context the model
# never saw, return an empty dictionary. `counts` maps each context, a tuple of two tokens, to a
# `Counter` of the tokens that followed it, like `trigram_counts`.

# %% tags=["answer-L1.4"]
def next_token_probabilities(counts, context):
    raise NotImplementedError("Exercise L1.4")


# %% tags=["raises-exception"]
toy = {("the", "bike"): Counter({" is": 3, " needs": 1})}
assert next_token_probabilities(toy, ("the", "bike")) == {" is": 0.75, " needs": 0.25}
assert next_token_probabilities(toy, ("a", "car")) == {}, "an unseen context has no next tokens"
probs = next_token_probabilities(trigram_counts, (".", " The"))
assert abs(sum(probs.values()) - 1) < 1e-9, "the probabilities must add up to 1"
print("passed")
print(sorted(probs.items(), key=lambda item: -item[1])[:5])

# %% [markdown]
# ## 4. Choosing the next token
#
# A model's probabilities don't say which token to write. A decoding rule does. The simplest is
# greedy decoding: always take the most likely token. The next cell generates 40 tokens after
# "The mechanic" that way. Before you run it, predict what goes wrong.

# %% tags=["raises-exception"]
def greedy(prompt, n_tokens):
    tokens = encode(prompt, merges)
    for _ in range(n_tokens):
        probs = next_token_probabilities(trigram_counts, tuple(tokens[-2:]))
        if not probs:
            break
        tokens.append(max(probs, key=lambda token: (probs[token], token)))
    return "".join(tokens)


print(greedy("The mechanic", 40))

# %% [markdown]
# Greedy decoding falls into a loop: once the last two tokens repeat, the most likely next token
# repeats too, and nothing can break the cycle. Large models loop less, but Holtzman and
# colleagues showed that always choosing likely tokens makes their text repetitive and bland as
# well. Sampling instead picks each token at random, in proportion to its probability.
#
# Two settings reshape the probabilities before sampling. **Temperature** $T$ raises each
# probability to the power $1/T$ and rescales them to add up to 1. Below 1 it sharpens the
# distribution toward the likeliest tokens; above 1 it flattens it toward the unlikely ones.
# **Top-p**, or nucleus sampling, keeps only the most likely tokens whose probabilities add up to
# at least $p$, and rescales those.

# %% [markdown]
# ### Exercise L1.5 (LO-1.2, ★★, about 15 minutes)
#
# Write `apply_temperature(probs, temperature)`, which returns a new dictionary of probabilities:
# each $p_i^{1/T}$, divided by their sum. Raise `ValueError` if the temperature isn't positive.
#
# Predict first: for `{"a": 0.5, "b": 0.25, "c": 0.25}` at temperature 0.5, what is the new
# probability of `"a"`?

# %% tags=["answer-L1.5"]
def apply_temperature(probs, temperature):
    raise NotImplementedError("Exercise L1.5")


# %% tags=["raises-exception"]
abc = {"a": 0.5, "b": 0.25, "c": 0.25}
sharp = apply_temperature(abc, 0.5)
flat = apply_temperature(abc, 2.0)
assert abs(sharp["a"] - 2 / 3) < 1e-9, (
    f"at T = 0.5, 'a' should get 0.25 / 0.375 = 2/3, not {sharp['a']}"
)
assert abs(flat["a"] - 0.5 ** 0.5 / (0.5 ** 0.5 + 2 * 0.25 ** 0.5)) < 1e-9, "check T = 2"
assert apply_temperature(abc, 1.0) == abc, "T = 1 leaves the probabilities unchanged"
assert apply_temperature({"only": 1.0}, 3.0) == {"only": 1.0}, "a certain token stays certain"
assert abc == {"a": 0.5, "b": 0.25, "c": 0.25}, (
    "return a new dictionary; don't change the one passed in"
)
try:
    apply_temperature(abc, 0)
except ValueError:
    pass
else:
    raise AssertionError("a temperature of 0 should raise ValueError")
print("passed")

# %% [markdown]
# ### Exercise L1.6 (LO-1.2, ★★, about 20 minutes)
#
# Write `top_p_filter(probs, p)`. Sort the tokens from most to least likely, breaking ties by the
# token's text in alphabetical order. Keep tokens from the top until their probabilities add up
# to at least `p`, then rescale the kept ones to add up to 1. With `p` of 1, keep every token.

# %% tags=["answer-L1.6"]
def top_p_filter(probs, p):
    raise NotImplementedError("Exercise L1.6")


# %% tags=["raises-exception"]
abc = {"a": 0.5, "b": 0.3, "c": 0.2}
assert top_p_filter(abc, 0.5) == {"a": 1.0}, "'a' alone reaches 0.5"
kept = top_p_filter(abc, 0.7)
assert set(kept) == {"a", "b"}, (
    f"'a' and 'b' reach 0.8, which is at least 0.7; you kept {set(kept)}"
)
assert abs(kept["a"] - 0.625) < 1e-9, "rescale: 0.5 / 0.8 = 0.625"
assert top_p_filter(abc, 1.0) == abc, "p = 1 keeps every token"
assert top_p_filter({"y": 0.4, "x": 0.4, "z": 0.2}, 0.3) == {"x": 1.0}, "break ties alphabetically"
print("passed")

# %% [markdown]
# With both settings in place, `generate` samples a continuation of a prompt. It takes a seed, so
# one seed always gives the same text, and different seeds give different draws.

# %% tags=["raises-exception"]
def generate(prompt, n_tokens, seed, temperature=1.0, top_p=1.0):
    rng = random.Random(seed)
    tokens = encode(prompt, merges)
    for _ in range(n_tokens):
        probs = next_token_probabilities(trigram_counts, tuple(tokens[-2:]))
        if not probs:
            break
        probs = top_p_filter(apply_temperature(probs, temperature), top_p)
        choices = sorted(probs)
        tokens.append(rng.choices(choices, weights=[probs[t] for t in choices])[0])
    return "".join(tokens)


for seed in range(3):
    print(repr(generate("The mechanic", 25, seed)))
print(repr(generate("The mechanic", 25, 0)))

# %% [markdown]
# The first and last lines match, because they use the same seed. The three seeds give three
# different texts from one prompt: sampling, not the prompt, is where the variety comes from.
#
# ### Exercise L1.7 (LO-1.2, LO-1.3, ★★, about 25 minutes)
#
# Write `continuations(prompt, n_tokens, runs, temperature=1.0, top_p=1.0)`, which returns a list
# of `runs` continuations, one for each seed from 0 to `runs - 1`. Return only the generated part
# of each text, without the prompt.
#
# Then predict, before you run the check: of 50 continuations of "The bike is ready. The", how
# many start with the token `" mechanic"` at temperatures 0.5, 1, and 2? The context
# `(".", " The")` gives that token a probability of about 0.55. Write your guesses in
# `my_guesses`; they aren't checked, so guess honestly. The check counts the word "mechanic" alone,
# not the token `" mechanics"`, which also follows this context.

# %% tags=["answer-L1.7"]
def continuations(prompt, n_tokens, runs, temperature=1.0, top_p=1.0):
    raise NotImplementedError("Exercise L1.7")


my_guesses = {0.5: None, 1.0: None, 2.0: None}

# %% tags=["raises-exception"]
prompt = "The bike is ready. The"
assert continuations(prompt, 4, 3) == continuations(prompt, 4, 3), (
    "the same seeds give the same texts"
)
assert len(continuations(prompt, 4, 7)) == 7, "return one continuation per run"
assert not continuations(prompt, 4, 1)[0].startswith("The bike"), "leave the prompt out"
print("setting          distinct  ' mechanic'  your guess")
share = {}
for temperature, top_p in [(0.5, 1.0), (1.0, 1.0), (2.0, 1.0), (1.0, 0.5)]:
    outs = continuations(prompt, 4, 50, temperature, top_p)
    share[temperature, top_p] = sum(bool(re.match(r" mechanic\b", o)) for o in outs)
    guess = my_guesses.get(temperature, "") if top_p == 1.0 else ""
    print(f"T={temperature}, top_p={top_p}  {len(set(outs)):8}  "
          f"{share[temperature, top_p]:11}  {guess}")
assert share[0.5, 1.0] > share[1.0, 1.0] > share[2.0, 1.0], (
    "a higher temperature should pick ' mechanic' less often"
)
print("passed")

# %% [markdown]
# A lower temperature concentrates the draws on `" mechanic"`; a higher one spreads them over
# rarer tokens. Top-p of 0.5 keeps only `" mechanic"` in this context, since its probability alone
# passes 0.5, so every draw starts with it. Neither setting makes the model know more: they only
# change how often it takes a token it already rated unlikely.
#
# The next cell draws the probabilities of all ten tokens that followed `(".", " The")` in the
# prose, at three temperatures. Each temperature has its own color and hatching. Before you run
# it, predict which bars grow and which shrink at temperature 2.

# %% tags=["raises-exception"]
base = next_token_probabilities(trigram_counts, (".", " The"))
ranked = sorted(base, key=lambda t: (-base[t], t))
fig, ax = plt.subplots(figsize=(9, 4))
width = 0.27
for i, (temperature, color, hatch) in enumerate([(0.5, "#0072B2", ""), (1.0, "#E69F00", "//"),
                                                 (2.0, "#009E73", "..")]):
    scaled = apply_temperature(base, temperature)
    positions = [x + (i - 1) * width for x in range(len(ranked))]
    ax.bar(positions, [scaled[t] for t in ranked], width, color=color, hatch=hatch,
           edgecolor="black", label=f"T = {temperature}")
ax.set_xticks(range(len(ranked)), [repr(t) for t in ranked], rotation=30)
ax.set_xlabel("next token after '.' and ' The'")
ax.set_ylabel("probability")
ax.set_title("Temperature sharpens or flattens the same prediction")
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# At temperature 0.5, `" mechanic"` takes about 0.90 of the probability and the rest nearly
# vanish. At temperature 2, it drops to about 0.28, and the seven tokens seen only once each
# rise from about 0.03 to about 0.07. One of them is `"y"`, the piece left over when the
# tokenizer splits "They" into `" The"` and `"y"`: a model chooses tokens, not words.
#
# Current Claude models don't let you set a temperature: the API documentation says that a
# request that sets `temperature`, `top_p`, or `top_k` to anything but its default returns an
# error. Their outputs still vary from run to run, so you can't switch the variety off. Module 3
# narrows it with clearer prompts, and Module 7 measures it with repeated runs.

# %% [markdown]
# ## 5. The context window
#
# A model reads only a limited number of tokens at once: its context window. The trigram model's
# window is two tokens, so nothing earlier in the text can change its prediction. A real model's
# window is far larger, 1M tokens for the current Claude models, but anything outside it is just
# as invisible. A model also keeps nothing between requests: a chat program resends the
# conversation each time, as Module 2 shows.
#
# ### Exercise L1.8 (LO-1.3, ★, about 15 minutes)
#
# Write `fit_to_window(tokens, window)`, which returns the last `window` tokens of the list, the
# part a model with that window would see. Raise `ValueError` if `window` is less than 1. Then run
# the check, which puts a note at the start of a long text and shows what a 500-token window keeps.

# %% tags=["answer-L1.8"]
def fit_to_window(tokens, window):
    raise NotImplementedError("Exercise L1.8")


# %% tags=["raises-exception"]
assert fit_to_window(["a", "b", "c"], 2) == ["b", "c"]
assert fit_to_window(["a", "b"], 5) == ["a", "b"], "a short text fits whole"
try:
    fit_to_window(["a"], 0)
except ValueError:
    pass
else:
    raise AssertionError("a window of 0 should raise ValueError")
note = "Note for the mechanic: the customer's bike is blue. "
long_text = encode(note + texts["prose"], merges)
seen = "".join(fit_to_window(long_text, 500))
print(f"the text has {len(long_text):,} tokens; the window keeps the last 500")
assert "blue" not in seen, "the note at the start falls outside the window"
print("passed: the note is gone, and nothing in the window says the bike is blue")

# %% [markdown]
# A model with a 500-token window would answer "What color is the bike?" without the note, and a
# model that has no fact to use may still write a confident answer. Long inputs need a plan for
# what stays inside the window, which Modules 2 and 10 build.
#
# To compare with a real window, the next cell estimates how many copies of the shop notes would
# fit in 1M tokens. Anthropic's models overview says 1M tokens is roughly 2.5M characters on the
# current Claude tokenizer, so the estimate uses 2.5 characters per token instead of this lab's
# tokenizer.

# %%
estimated_tokens = len(texts["prose"]) / 2.5
copies = 1_000_000 / estimated_tokens
print(f"about {estimated_tokens:,.0f} tokens; about {copies:,.0f} copies fit in 1M tokens")

# %% [markdown]
# ## Summary
#
# - A tokenizer turns text into tokens. BPE learns its vocabulary by merging the most frequent
#   pair of symbols, again and again, so it packs text like its training text tightly and splits
#   unfamiliar text, such as another language, code, or numbers, into more tokens.
# - A language model gives a probability for every possible next token. The trigram model gets
#   them by counting; a real model computes them with a neural network, from the whole context.
# - Text comes from repeatedly choosing a next token. Greedy choice loops; sampling varies.
#   Temperature sharpens or flattens the probabilities, and top-p cuts off the unlikely tail.
# - One prompt gives different outputs because each token is sampled. Current Claude models don't
#   let you set a temperature, so their variety is managed with the prompt and measured with
#   repeated runs.
# - A model sees only what fits in its context window, and remembers nothing between requests.
#
# Next, do the [Module 1 practice](practice.md).
