"""Stand-ins for a language model, which answer in the shape of the Claude Messages API.

A response from the Messages API is a JSON object like this one, which ``make_response`` builds:

.. code-block:: python

    {
        "id": "msg_standin_0001",
        "type": "message",
        "role": "assistant",
        "model": "claude-opus-5-5",
        "content": [{"type": "text", "text": "Hello!"}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {
            "input_tokens": 12,
            "output_tokens": 6,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
        },
    }

Real responses can carry more fields than these, and their IDs look like
``msg_01XFDUDYJgAACzvnptvVoYEL``. A stand-in's IDs start with ``msg_standin_`` instead, so one
can never be mistaken for a real response.

A model, for the code in PE101's labs, is any function that takes a request dictionary and
returns a response dictionary. A ``ScriptedModel`` is such a function. A program that sends the
same dictionary to the API over HTTP would be another, which the course never runs.
"""

from __future__ import annotations

import copy
import itertools
import math
from collections.abc import Callable, Iterable
from typing import Any

Request = dict[str, Any]
Response = dict[str, Any]

#: The model ID that responses name when no other is given.
DEFAULT_MODEL = "claude-opus-5-5"

#: The stop reasons the Messages API documents, from its "Handling stop reasons" page.
STOP_REASONS = (
    "end_turn",
    "max_tokens",
    "stop_sequence",
    "tool_use",
    "pause_turn",
    "refusal",
    "model_context_window_exceeded",
)

_ids = itertools.count(1)


def rough_token_count(text: str) -> int:
    """Return a rough token count for ``text``: one token for every 2.5 characters, rounded up.

    The ratio comes from Anthropic's models overview, which says that 1M tokens is roughly 2.5M
    Unicode characters on the current tokenizer. It is an average over typical text, not a
    tokenizer: real counts vary with the language and the kind of text, as Lab 1 shows. The
    stand-ins use it only to fill in ``usage`` when a script doesn't give real numbers.
    """
    return math.ceil(len(text) / 2.5)


def make_response(
    content: str | list[dict[str, Any]],
    *,
    stop_reason: str = "end_turn",
    stop_sequence: str | None = None,
    model: str = DEFAULT_MODEL,
    input_tokens: int = 0,
    output_tokens: int | None = None,
    cache_creation_input_tokens: int = 0,
    cache_read_input_tokens: int = 0,
    stop_details: dict[str, Any] | None = None,
) -> Response:
    """Build a response dictionary in the shape of a Messages API response.

    ``content`` is the text of the reply, or a list of content blocks. ``output_tokens``
    defaults to ``rough_token_count`` of the reply's text. A refusal can carry
    ``stop_details``, as real refusals do.
    """
    if stop_reason not in STOP_REASONS:
        raise ValueError(f"unknown stop reason {stop_reason!r}; expected one of {STOP_REASONS}")
    if stop_sequence is not None and stop_reason != "stop_sequence":
        raise ValueError("a stop_sequence goes only with stop_reason 'stop_sequence'")
    blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content
    if output_tokens is None:
        text = "".join(block.get("text", "") for block in blocks)
        output_tokens = rough_token_count(text)
    response: Response = {
        "id": f"msg_standin_{next(_ids):04d}",
        "type": "message",
        "role": "assistant",
        "model": model,
        "content": copy.deepcopy(blocks),
        "stop_reason": stop_reason,
        "stop_sequence": stop_sequence,
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_creation_input_tokens": cache_creation_input_tokens,
            "cache_read_input_tokens": cache_read_input_tokens,
        },
    }
    if stop_details is not None:
        response["stop_details"] = copy.deepcopy(stop_details)
    return response


class ScriptExhausted(RuntimeError):
    """A ``ScriptedModel`` got more requests than its script has responses."""


class ScriptedModel:
    """A stand-in for a model, which answers each request with the next item of its script.

    Each item of ``script`` is one of:

    - a string: the reply's text, which becomes a response with ``make_response``;
    - a dictionary: a whole response, returned as it is;
    - a function: called with the request, and returning a string or a response dictionary, for
      a reply that depends on what was asked.

    The model records a copy of every request in ``requests``, so a test can check what the code
    sent. When the script runs out, the next request raises ``ScriptExhausted``: a test that
    expected three calls and got a fourth fails loudly instead of passing by accident.
    """

    def __init__(
        self,
        script: Iterable[str | Response | Callable[[Request], str | Response]],
        *,
        model: str = DEFAULT_MODEL,
    ) -> None:
        self.script = list(script)
        self.model = model
        self.requests: list[Request] = []

    def __call__(self, request: Request) -> Response:
        self.requests.append(copy.deepcopy(request))
        if not self.script:
            raise ScriptExhausted(
                f"the script has no response left for request {len(self.requests)}"
            )
        item = self.script.pop(0)
        if callable(item):
            item = item(copy.deepcopy(request))
        if isinstance(item, str):
            input_text = _request_text(request)
            return make_response(
                item,
                model=request.get("model", self.model),
                input_tokens=rough_token_count(input_text),
            )
        return copy.deepcopy(item)

    @property
    def calls(self) -> int:
        """How many requests the model has received."""
        return len(self.requests)


def _request_text(request: Request) -> str:
    """Return every piece of text in a request's system prompt and messages, joined."""
    parts: list[str] = []
    system = request.get("system", "")
    if isinstance(system, str):
        parts.append(system)
    else:
        parts.extend(block.get("text", "") for block in system)
    for message in request.get("messages", []):
        content = message.get("content", "")
        if isinstance(content, str):
            parts.append(content)
        else:
            parts.extend(block.get("text", "") for block in content if "text" in block)
    return "\n".join(parts)
