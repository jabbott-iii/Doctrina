"""A reference BM25 implementation for PE101's retrieval notebooks."""

from collections import Counter
from math import log1p
import re
from statistics import mean


def bm25(query, docs, *, k1=1.2, b=0.75):
    """Return (section ID, score) pairs, sorted by descending score and then ID."""
    if not docs:
        return []
    counts = [Counter(re.findall(r"[a-z]+", doc["text"].lower())) for doc in docs]
    lengths = [sum(counter.values()) for counter in counts]
    mean_length = mean(lengths)
    terms = set(re.findall(r"[a-z]+", query.lower()))
    frequencies = {term: sum(term in counter for counter in counts) for term in terms}
    scores = []
    for doc, counter, length in zip(docs, counts, lengths, strict=True):
        score = 0.0
        for term in sorted(terms & counter.keys()):
            df = frequencies[term]
            idf = log1p((len(docs) - df + 0.5) / (df + 0.5))
            tf = counter[term]
            norm = k1 * (1 - b + b * length / mean_length)
            score += idf * tf * (k1 + 1) / (tf + norm)
        scores.append((doc["id"], score))
    return sorted(scores, key=lambda pair: (-pair[1], pair[0]))
