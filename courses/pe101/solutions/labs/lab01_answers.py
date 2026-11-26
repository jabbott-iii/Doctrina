# %% [markdown]
# # Lab 1: answer key
#
# Each tagged cell replaces the lab cell with the same tag. `tools/check_lab.py` runs the lab with
# these answers and fails if any check fails. The untagged Markdown cells explain each answer and
# the mistakes students commonly make; the checker ignores them.

# %% [markdown]
# ## Exercise L1.1
#
# The chunks are `"low"` once, `" low"` 4 times, `" lower"` twice, `" newest"` 6 times,
# `" widest"` 3 times, and a final `" "`. At the start, the most frequent pairs are `("e", "s")`
# and `("s", "t")`, 9 each (6 from `" newest"` and 3 from `" widest"`), then `("w", "e")` with 8
# (6 from `" newest"` and 2 from `" lower"`), then `("l", "o")` and `("o", "w")` with 7 each
# (1 + 4 + 2). `("e", "s")` is counted before `("s", "t")`, so the tie goes to it.
#
# After the first merge, `" newest"` reads `" n e w es t"`, so `("es", "t")` has 9 and is second,
# and `("w", "e")` drops to 2, because the `e` of `" newest"` now belongs to `"es"`. Third is
# `("l", "o")`, with 7, which ties with `("o", "w")` and wins because the chunk `"low"` is counted
# first.
#
# Students often forget the leading space, forget that one pair can occur in several chunks, or
# keep counting a pair whose symbols an earlier merge used up.

# %% tags=["answer-L1.1"]
predicted_merges = [("e", "s"), ("es", "t"), ("l", "o")]

# %% [markdown]
# ## Exercise L1.2
#
# The measured order is prose, then Spanish, then code, then numbers. The prose is the training
# text, so its common words are single tokens. The Spanish uses the same alphabet but different
# words, so it splits into short pieces of the English merges. Code mixes English words with
# punctuation, underscores, indentation, and names the prose never uses. Numbers are worst,
# because every digit is its own token. A common wrong prediction puts code last; numbers lose
# because this tokenizer never merges digits.

# %% tags=["answer-L1.2"]
def chars_per_token(text, merges):
    return len(text) / len(encode(text, merges))


my_ranking = ["prose", "spanish", "code", "numbers"]

# %% [markdown]
# ## Exercise L1.3
#
# Training once with the largest count and slicing is faster, and gives the same merges, because
# training is greedy: the first `n` merges never depend on the ones after them.

# %% tags=["answer-L1.3"]
def tokens_by_merges(text, merge_counts):
    learned = train_bpe(texts["prose"], max(merge_counts))
    return [len(encode(text, learned[:n])) for n in merge_counts]


# %% [markdown]
# ## Exercise L1.4
#
# A common mistake is to divide by the number of distinct next tokens instead of the total count.

# %% tags=["answer-L1.4"]
def next_token_probabilities(counts, context):
    followers = counts.get(context)
    if not followers:
        return {}
    total = sum(followers.values())
    return {token: n / total for token, n in followers.items()}


# %% [markdown]
# ## Exercise L1.5
#
# At T = 0.5, each probability is squared: 0.25, 0.0625, and 0.0625, which add up to 0.375, so
# `"a"` gets 0.25 / 0.375 = 2/3. Students who multiply by T instead of raising to 1/T get the
# direction right and the numbers wrong. Using `counts.get` on a `defaultdict` avoids creating an
# empty entry for an unseen context.

# %% tags=["answer-L1.5"]
def apply_temperature(probs, temperature):
    if temperature <= 0:
        raise ValueError(f"temperature must be positive, not {temperature}")
    scaled = {token: p ** (1 / temperature) for token, p in probs.items()}
    total = sum(scaled.values())
    return {token: s / total for token, s in scaled.items()}


# %% [markdown]
# ## Exercise L1.6
#
# The test `total >= p` comes after the token is added, so the token that crosses the threshold
# is kept. Forgetting to rescale leaves probabilities that add up to less than 1.

# %% tags=["answer-L1.6"]
def top_p_filter(probs, p):
    ordered = sorted(probs, key=lambda token: (-probs[token], token))
    kept, total = [], 0.0
    for token in ordered:
        kept.append(token)
        total += probs[token]
        if total >= p:
            break
    kept_total = sum(probs[token] for token in kept)
    return {token: probs[token] / kept_total for token in kept}


# %% [markdown]
# ## Exercise L1.7
#
# With 50 runs, the token " mechanic" starts 46 continuations at T = 0.5, 32 at T = 1, and 15 at
# T = 2, and all 50 at top-p 0.5. The counts are near 50 times each temperature's probability
# (about 45, 27, and 14), but not equal to it, because 50 draws are a small sample. Most students
# guess the direction right and underestimate how far T = 2 moves the share.

# %% tags=["answer-L1.7"]
def continuations(prompt, n_tokens, runs, temperature=1.0, top_p=1.0):
    return [generate(prompt, n_tokens, seed, temperature, top_p)[len(prompt):]
            for seed in range(runs)]


my_guesses = {0.5: 45, 1.0: 30, 2.0: 20}

# %% [markdown]
# ## Exercise L1.8
#
# Slicing with a negative start, `tokens[-window:]`, keeps the last `window` items and returns
# the whole list when it is shorter.

# %% tags=["answer-L1.8"]
def fit_to_window(tokens, window):
    if window < 1:
        raise ValueError(f"window must be at least 1, not {window}")
    return tokens[-window:]
