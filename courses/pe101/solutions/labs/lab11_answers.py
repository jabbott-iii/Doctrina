# %% tags=["answer-L11.1"]
def groups(cases):
    out = {"direct": [], "indirect": []}
    for case in cases:
        out[classify(case)].append(case["id"])
    return out

# %% tags=["answer-L11.2"]
def mark(text, origin):
    root = ElementTree.Element("source", trust="untrusted", origin=origin)
    root.text = text
    return ElementTree.tostring(root, encoding="unicode")

# %% tags=["answer-L11.3"]
def authorize(proposal, allowed, approved):
    if proposal["name"] not in allowed:
        return "denied"
    if not approved and proposal["name"] == "change_label":
        return "needs_review"
    return "accepted"

# %% tags=["answer-L11.4"]
def rate(rows, baseline, allowed):
    unapproved = [r for r in rows if not r["authorized"]]
    if not unapproved:
        return 0.0
    decisions = ["accepted" if baseline else authorize(replay(row), allowed, row["authorized"])
                 for row in unapproved]
    return decisions.count("accepted") / len(unapproved)
