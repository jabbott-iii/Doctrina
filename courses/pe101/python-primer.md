# Python for the labs

The labs are in Python 3.12. If you know another language, this page teaches the Python they use,
by example. Every example ran on Python 3.12, and the output under each is what it printed. Read
the page before Module 1, try the examples in a notebook cell, and come back when a lab uses
something you don't recognize.

You can skip this page if you already write Python. It covers only what the labs need, not the
whole language.

## Values and names

A name refers to a value, and you don't declare its type. Python has integers, floating-point
numbers, strings, booleans (`True` and `False`), and `None`, which means "no value". `type`
reports a value's type. A `#` starts a comment.

```python
price = 4.0          # dollars per million tokens
tokens = 1_250       # an int; the underscore only groups digits
name = "Opus"
cached = False
reply = None
print(type(price), type(tokens), type(name), type(cached), type(reply))
```

```text
<class 'float'> <class 'int'> <class 'str'> <class 'bool'> <class 'NoneType'>
```

`/` always gives a float, and `//` gives a whole-number quotient, rounded down.

## f-strings

A string with `f` before its opening quote is an f-string: each `{…}` inside it is replaced by the
value of the expression it holds. A format specification after a colon controls how the value is
written: `:,` adds thousands separators, `:.4f` gives four decimal places, and `:.1%` multiplies
by 100 and adds a percent sign.

```python
cost = tokens / 1_000_000 * price
print(f"{name}: {tokens:,} tokens cost ${cost:.4f}")
print(f"{0.4567:.1%}")
```

```text
Opus: 1,250 tokens cost $0.0050
45.7%
```

## Lists

A list holds values in order. Indexes start at 0, a negative index counts from the end, and a
slice `[start:stop]` copies part of the list. `append` adds to the end, and `len` gives the length.

```python
words = ["route", "refund", "repair"]
print(words[0], words[-1], words[1:])
words.append("rate")
print(len(words), words)
```

```text
route repair ['refund', 'repair']
4 ['route', 'refund', 'repair', 'rate']
```

A list comprehension builds a new list from an old one, optionally keeping only the items that
pass a test. The labs use comprehensions often:

```python
lengths = [len(w) for w in words]
long_words = [w for w in words if len(w) > 4]
print(lengths, long_words)
```

```text
[5, 6, 6, 4] ['route', 'refund', 'repair']
```

## Dictionaries

A dictionary maps keys to values, like a map or a hash table in other languages. The requests and
responses in this course are dictionaries that hold lists of more dictionaries, so you reach into
them one step at a time. `get` returns a default instead of failing when a key is missing, and
`items` gives each key with its value.

```python
request = {
    "model": "claude-opus-5-5",
    "max_tokens": 200,
    "messages": [{"role": "user", "content": "Hello"}],
}
print(request["messages"][0]["content"])
request["messages"].append({"role": "assistant", "content": "Hi!"})
print(len(request["messages"]))
print(request.get("system", "no system prompt"))
for key, value in request.items():
    print(key, "->", value)
```

```text
Hello
2
no system prompt
model -> claude-opus-5-5
max_tokens -> 200
messages -> [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi!'}]
```

Reading a missing key with square brackets, such as `request["system"]`, raises a `KeyError`.

## Functions

`def` defines a function, and `return` gives its result. A parameter can have a default value,
and a caller can name an argument (`price=2.0`) instead of relying on its position. The labs
annotate parameters and results with their types (`requests: int`, `-> float`). Python doesn't
check these annotations when the code runs; they document what the function expects. The string
on the first line of the body is the function's docstring, which says what it does.

```python
def batch_cost(requests: int, tokens_each: int, price: float = 4.0) -> float:
    """Return the cost in dollars of `requests` requests of `tokens_each` input tokens."""
    return requests * tokens_each / 1_000_000 * price

print(batch_cost(1000, 500))
print(batch_cost(1000, 500, price=2.0))
```

```text
2.0
1.0
```

Python marks blocks by indentation, not braces: the body of a function, a loop, or an `if` is the
lines indented under it, usually by four spaces.

## Loops

A `for` loop runs once for each item of a list, a string, a dictionary's keys, or anything else
that can be iterated. `enumerate` counts the items as it goes, and `zip` walks two lists side by
side. `sorted` returns a new, sorted list, and its `key` argument sorts by a function of each item.

```python
labels = ["billing", "repair", "billing"]
for number, label in enumerate(labels, start=1):
    print(number, label)
for label, score in zip(labels, [0.9, 0.4, 0.7]):
    print(label, score)
print(sorted(["repair", "billing", "account"]))
print(sorted(["repair", "billing", "account"], key=len))
```

```text
1 billing
2 repair
3 billing
billing 0.9
repair 0.4
billing 0.7
['account', 'billing', 'repair']
['repair', 'billing', 'account']
```

The last line sorts by length: "repair" has six letters, and the other two keep their order
because each has seven.

## Strings and regular expressions

Strings have methods for the common jobs: `strip` removes spaces and newlines from both ends,
`split` cuts a string into a list, and `join` glues a list together. `in` tests whether one string
contains another. `repr` shows a string with its quotes, which makes spaces and newlines visible.

```python
text = "  Category: billing\n"
print(repr(text.strip()))
print(text.strip().split(": "))
print(", ".join(["a", "b", "c"]))
print("bill" in text, text.strip().startswith("Category"))
```

```text
'Category: billing'
['Category', 'billing']
a, b, c
True True
```

The `re` module matches regular expressions, which the labs use to check the format of a
response. `re.fullmatch` succeeds only if the whole string matches, and a group in parentheses
captures part of the match. `re.findall` returns every match. Write patterns as raw strings
(`r"…"`), so that a backslash reaches `re` unchanged.

```python
import re
match = re.fullmatch(r"Category: (\w+)", text.strip())
print(match.group(1))
print(re.findall(r"\d+", "3 tickets, 12 replies"))
```

```text
billing
['3', '12']
```

When nothing matches, `re.fullmatch` returns `None`, so check the result before you use it.

## JSON

The `json` module converts between JSON text and Python values: a JSON object becomes a
dictionary, an array a list, `true` and `false` become `True` and `False`, and `null` becomes
`None`. `json.loads` reads a string, and `json.dumps` writes one.

```python
import json
record = json.loads('{"id": 7, "label": "repair", "urgent": true}')
print(record["label"], record["urgent"])
print(json.dumps({"id": 7, "tags": ["a", "b"]}))
print(json.dumps({"id": 7}, indent=2))
```

```text
repair True
{"id": 7, "tags": ["a", "b"]}
{
  "id": 7
}
```

`json.loads` raises `json.JSONDecodeError` when the text isn't valid JSON, which matters when the
text came from a model.

## Assertions and exceptions

`assert` checks that a condition is true and fails with an `AssertionError` if it isn't. The
message after the comma says what went wrong. Every check cell in the labs is a list of
assertions. `!r` in an f-string writes a value with `repr`, quotes included.

```python
def check_label(label):
    assert label in {"billing", "repair", "account"}, f"unknown label {label!r}"

check_label("repair")
try:
    check_label("refund")
except AssertionError as error:
    print("AssertionError:", error)
```

```text
AssertionError: unknown label 'refund'
```

The `{"billing", "repair", "account"}` in that example is a set: an unordered collection with no
duplicates, which answers `in` quickly.

`raise` signals an error of your own, and `try` with `except` handles one. Raise a specific type,
such as `ValueError` for a bad value, with a message that says what was expected:

```python
def parse_price(text):
    if not text.startswith("$"):
        raise ValueError(f"expected a price like $4.00, got {text!r}")
    return float(text[1:])

print(parse_price("$4.00"))
try:
    parse_price("4 dollars")
except ValueError as error:
    print("ValueError:", error)
```

```text
4.0
ValueError: expected a price like $4.00, got '4 dollars'
```

## Modules from the standard library

`import` loads a module. Two from Python's standard library appear in many labs: `Counter`, from
`collections`, counts how often each value occurs, and `random` makes pseudo-random choices. Seed
`random` with a fixed number, and it makes the same choices every run, which keeps a lab
repeatable:

```python
from collections import Counter
import random

counts = Counter(["billing", "repair", "billing", "account", "billing"])
print(counts.most_common(2))
random.seed(42)
print(random.choice(["a", "b", "c"]), random.random())
random.seed(42)
print(random.choice(["a", "b", "c"]), random.random())
```

```text
[('billing', 3), ('repair', 1)]
c 0.11133106816568039
c 0.11133106816568039
```

The two seeded lines print the same values, because each starts from the same seed. With a
different seed, or none, they would differ.

## Files

`open` opens a file, and a `with` block closes it when the block ends, even if an error occurs.
Pass `encoding="utf-8"` so that text reads the same on every operating system. Looping over a file
gives one line at a time, each ending with its newline.

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("first line\nsecond line\n")
with open("notes.txt", encoding="utf-8") as file:
    for line in file:
        print(line.rstrip("\n"))
```

```text
first line
second line
```

## Virtual environments

A virtual environment is a folder that holds a Python interpreter and its own set of installed
packages, so one project's packages don't conflict with another's. [Setting up your
environment](setup.md) creates one in `.venv/` at the root of the repository, and every command in
the course runs the tools inside it, such as `.venv/bin/jupyter`. The Jupyter notebooks run in the
same environment, so `import promptlab` works in every lab.

## Where to learn more

- [The Python Tutorial](https://docs.python.org/3.12/tutorial/), from the Python documentation, is
  the place to go next. Chapters 3–5 cover values, lists, dictionaries, loops, and functions;
  chapter 7 covers files and JSON, chapter 8 exceptions, and chapter 12 virtual environments.
