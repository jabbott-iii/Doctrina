# %% tags=["answer-L6.1"]
def choose(rows, min_accuracy, max_seconds):
    eligible = [r for r in rows if r["accuracy"] >= min_accuracy and r["seconds"] <= max_seconds]
    if not eligible:
        return None
    return min(eligible, key=lambda r: (r["cost"], r["seconds"], r["effort"]))["effort"]

# %% tags=["answer-L6.2"]
def extract(text):
    if text.count("<answer>") != 1 or text.count("</answer>") != 1:
        raise ValueError("Expected exactly one opening and one closing answer tag.")
    matches = re.findall(r"<answer>(.*?)</answer>", text, flags=re.DOTALL)
    if len(matches) != 1 or not matches[0].strip():
        raise ValueError("Expected one nonempty answer section.")
    return matches[0].strip()

# %% tags=["answer-L6.3"]
def chain(model, ticket):
    def ask(text):
        response = model({"messages": [{"role": "user", "content": text}]})
        return extract(response["content"][0]["text"])

    label = ask(f"classify\n{ticket}")
    reply = ask(f"draft\n{ticket}\n{label}")
    decision = ask(f"check\n{ticket}\n{reply}")
    return reply if decision == "approved" else None

# %% tags=["answer-L6.4"]
def error_budget(stage_rates, caught):
    passed = prod(stage_rates)
    return passed, (1 - passed) * (1 - caught)
