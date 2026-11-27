# %% tags=["answer-L4.1"]
def layout(document, instructions, question):
    root = ElementTree.Element("prompt")
    docs = ElementTree.SubElement(root, "documents")
    ElementTree.SubElement(docs, "doc").text = document
    ElementTree.SubElement(root, "instructions").text = instructions
    ElementTree.SubElement(root, "question").text = question
    return ElementTree.tostring(root, encoding="unicode")

# %% tags=["answer-L4.2"]
def serialize_ticket(value):
    return f"<ticket>{value}</ticket>", f"<ticket>{escape(value)}</ticket>"

# %% tags=["answer-L4.3"]
def render(text, values):
    template = Template(text)
    required = set(template.get_identifiers())
    if not template.is_valid() or set(values) != required:
        raise ValueError("Supply exactly the template fields.")
    return template.substitute({key: escape(value) for key, value in values.items()})

# %% tags=["answer-L4.4"]
def compare(first, second):
    return "\n".join(unified_diff(first.splitlines(), second.splitlines(),
                                  fromfile="v1", tofile="v2", lineterm=""))
