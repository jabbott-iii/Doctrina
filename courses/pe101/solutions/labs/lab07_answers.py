# %% tags=["answer-L7.1"]
def split_rows(rows):
    seen = set()
    groups = {"dev": [], "holdout": []}
    for row in rows:
        if row["id"] in seen or row["split"] not in groups:
            raise ValueError("Each case needs a unique ID and a known split.")
        seen.add(row["id"])
        groups[row["split"]].append(row)
    return groups["dev"], groups["holdout"]

# %% tags=["answer-L7.2"]
def grade(text, expected):
    match = re.fullmatch(r"Label: (repair|billing|account)", text)
    valid = match is not None
    return {"format": valid, "correct": valid and match[1] == expected}

# %% tags=["answer-L7.3"]
def agreement(rows):
    n = len(rows)
    if not n:
        raise ValueError("Provide at least one pair.")
    observed = sum(row["human"] == row["judge"] for row in rows) / n
    p = sum(row["human"] for row in rows) / n
    q = sum(row["judge"] for row in rows) / n
    expected = p*q + (1-p)*(1-q)
    return observed, (observed - expected) / (1 - expected) if expected < 1 else None

# %% tags=["answer-L7.4"]
def wilson(successes, total, z=1.96):
    if total <= 0 or not 0 <= successes <= total:
        raise ValueError("Provide a positive total and a valid success count.")
    p = successes / total
    scale = 1 + z**2 / total
    center = (p + z**2 / (2 * total)) / scale
    radius = z * sqrt(p * (1-p) / total + z**2 / (4 * total**2)) / scale
    return max(0, center-radius), min(1, center+radius)

# %% tags=["answer-L7.5"]
def paired(a, b, repeats=2000, seed=101):
    if len(a) != len(b) or not a or repeats < 2:
        raise ValueError("Need aligned nonempty scores and at least two samples.")
    deltas = [y - x for x, y in zip(a, b, strict=True)]
    rng = Random(seed)
    samples = sorted(mean(rng.choices(deltas, k=len(deltas))) for _ in range(repeats))
    return mean(deltas), samples[int(0.025 * (repeats-1))], samples[int(0.975 * (repeats-1))]
