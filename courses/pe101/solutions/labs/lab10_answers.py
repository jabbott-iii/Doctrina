# %% tags=["answer-L10.1"]
def prompt(docs, question):
    root = ElementTree.Element("prompt")
    group = ElementTree.SubElement(root, "documents")
    for doc in docs:
        ElementTree.SubElement(group, "doc", id=doc["id"]).text = doc["text"]
    ElementTree.SubElement(root, "instructions").text = (
        'Quote exact evidence with its section ID or answer "I don\'t know".'
    )
    ElementTree.SubElement(root, "question").text = question
    return ElementTree.tostring(root, encoding="unicode")

# %% tags=["answer-L10.2"]
def bm25(query, docs, *, k1=1.2, b=0.75):
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

# %% tags=["answer-L10.3"]
def recall(ranked, relevant, k):
    if k < 0:
        raise ValueError("k must be nonnegative.")
    if not relevant:
        raise ValueError("At least one relevant section is required.")
    return len(set(ranked[:k]) & set(relevant)) / len(set(relevant))

# %% tags=["answer-L10.4"]
def valid_quote(docs, ident, quote):
    available = {doc["id"]: doc["text"] for doc in docs}
    return bool(quote.strip()) and ident in available and quote in available[ident]

# %% tags=["answer-L10.5"]
def cost(requests, prefix, suffix, rates):
    if requests <= 0:
        raise ValueError("At least one request is required.")
    uncached = requests * (prefix + suffix) * rates["input"]
    cached = (prefix*rates["cache_write_5m"] + (requests-1)*prefix*rates["cache_read"]
              + requests*suffix*rates["input"])
    return uncached / 1_000_000, cached / 1_000_000
