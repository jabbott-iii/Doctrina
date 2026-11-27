# %% tags=["answer-L3.1"]
def revisions():
    return [
        "Route the ticket for the dispatcher. Use repair for service, billing for charges, "
        "and account for profiles. Prefer the active request. Return exactly Label: <queue>. "
        "Ticket: " + tickets[0]["text"],
        "Write a customer-facing reply that acknowledges the receipt request. Use at most "
        "two sentences. Ask for an invoice reference if needed. Make no promise of delivery. "
        "Ticket: " + tickets[13]["text"],
        "Extract the profile field the customer wants to change for an account clerk. "
        "Return exactly Field: <field>, or Field: unknown if it is ambiguous. "
        "Ticket: " + tickets[18]["text"],
    ]

# %% tags=["answer-L3.2"]
def route_request(ticket):
    return {
        "model": "claude-opus-5-5",
        "max_tokens": 60,
        "system": ("Route for the dispatcher. Use repair for service, billing for payments "
                   "and receipts, and account for profile requests. Return exactly Label: <queue>."),
        "messages": [{"role": "user", "content": ticket}],
    }

# %% tags=["answer-L3.3"]
def parse_label(text):
    match = re.fullmatch(r"Label: (repair|billing|account)", text)
    return match[1] if match else None

# %% tags=["answer-L3.4"]
def audit(rows):
    valid = sum(parse_label(row["text"]) is not None for row in rows)
    return {"valid": valid, "invalid": len(rows) - valid}
