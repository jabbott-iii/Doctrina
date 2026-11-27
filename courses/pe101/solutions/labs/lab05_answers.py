# %% tags=["answer-L5.1"]
def examples_xml(rows):
    root = ElementTree.Element("examples")
    for row in rows:
        example = ElementTree.SubElement(root, "example")
        ElementTree.SubElement(example, "input").text = row["text"]
        ElementTree.SubElement(example, "output").text = "Label: " + row["label"]
    return ElementTree.tostring(root, encoding="unicode")

# %% tags=["answer-L5.2"]
def coverage(rows):
    return (dict(Counter(row["label"] for row in rows)),
            dict(Counter("short" if len(row["text"].split()) <= 9 else "long" for row in rows)))

# %% tags=["answer-L5.3"]
def words(text):
    return set(re.findall(r"[a-z]+", text.casefold()))

# %% tags=["answer-L5.4"]
def pick(text, rows, k):
    if not 0 <= k <= len(rows):
        raise ValueError("k must fit the candidate pool.")
    query = words(text)
    def rank(row):
        terms = words(row["text"])
        union = query | terms
        score = len(query & terms) / len(union) if union else 0
        return (-score, row["id"])
    return sorted(rows, key=rank)[:k]
