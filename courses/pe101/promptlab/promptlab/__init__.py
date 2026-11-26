"""promptlab: what PE101's labs share, so that every lab runs offline and costs nothing.

PE101 never calls a language model. Its labs build requests, read responses, and test the code
around a model with stand-ins instead:

- ``make_response`` builds a dictionary in the shape of a Claude Messages API response.
- ``ScriptedModel`` is a stand-in for a model. It answers each request with the next response in
  its script, and records every request, so a test can check what the code sent.
- ``data_path``, ``load_json``, and ``load_jsonl`` read the course's bundled data sets, every one
  of them written for the course.

A stand-in only fakes the shape of a model's answers, never their quality: its replies come from
a script that a person wrote. Code tested with one is code whose plumbing works, which is what
production code tests without a model too.
"""

from __future__ import annotations

from promptlab.data import data_path, load_json, load_jsonl
from promptlab.standins import ScriptedModel, ScriptExhausted, make_response, rough_token_count

__version__ = "1.0.0"

__all__ = [
    "ScriptExhausted",
    "ScriptedModel",
    "__version__",
    "data_path",
    "load_json",
    "load_jsonl",
    "make_response",
    "rough_token_count",
]
