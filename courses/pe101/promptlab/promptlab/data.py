"""Find and read PE101's bundled data sets, in ``courses/pe101/data/``.

Every data set there was written for the course, and none holds a real person's data. Files of
illustrative responses say so in their own records: they were written for PE101 and aren't model
output.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

#: The course's data folder: ``courses/pe101/data``, two levels above this package's folder.
DATA = pathlib.Path(__file__).resolve().parents[2] / "data"


def data_path(name: str) -> pathlib.Path:
    """Return the path of the bundled file ``name``, such as ``"corpus/prose.txt"``.

    Raises ``FileNotFoundError``, naming the folder it looked in, if there is no such file.
    """
    path = DATA / name
    if not path.is_file():
        raise FileNotFoundError(f"no data file {name!r} in {DATA}")
    return path


def load_json(name: str) -> Any:
    """Read the bundled JSON file ``name`` and return its value."""
    with data_path(name).open(encoding="utf-8") as file:
        return json.load(file)


def load_jsonl(name: str) -> list[dict[str, Any]]:
    """Read the bundled JSON Lines file ``name``: one JSON object on each non-blank line."""
    records = []
    with data_path(name).open(encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as error:
                    raise ValueError(f"{name}, line {number}: {error.msg}") from error
    return records
